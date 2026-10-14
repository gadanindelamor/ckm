"""
corpus_service.py — CorpusService  v2

Stateful. Acumula prompts, construye W desde co-activaciones.
Transición automática acumulación → evaluación al cruzar `min_texts`.

**Cuándo se reconstruye W, los tres regímenes.** El docstring decía sólo
"transición automática" y no decía lo que pasa **después** de la primera W; se
completa acá (regla del 10 oct: el docstring se actualiza con el código).

  1. `rebuild_suspendido=False` (**default**): `ingest` reconstruye W en **cada
     ingesta** una vez cruzado `min_texts`. delamor: *"la ingesta no debe
     implicar rebuilds continuos"* — este régimen es el que esa frase descarta,
     y queda como el de los tests y drivers que ya lo usaban.
  2. `rebuild_suspendido=True` (**el canal vivo**): W se construye **una vez** y
     la ingesta no la reconstruye más.
  3. **Por decisión**: `rebuild_por_decision(causa)`, con la `causa`
     **obligatoria y sin default** — un rebuild sin causa declarada no es una
     decisión. **`rebuild_suspendido` no lo bloquea**: ese flag impide el
     rebuild automático por ingesta, no el salto decidido. La causa queda en el
     `causal_event` de `w_version`, y con el corpus en acumulación **no
     reconstruye y lo dice** (`rebuild: False`, `motivo_no_rebuild`).

Quién decide el salto no vive acá: lo decide `CKMMonitor` con la jerarquía
estructural > volumen > tiempo (`TASK_should_rebuild_conectado_v1`). `_rebuild`
acepta `causa=None` para que el rebuild por ingesta **no cambie de marca**.

**Nota sobre la traza:** `w_version.register` **deduplica por sha** ("si W es
idéntica, no crea marca duplicada"), así que un rebuild por decisión que no
mueve W **no deja versión**. Esa decisión queda en el `rebuild_decisions.jsonl`
de `CKMMonitor`, no acá.

v2: W mixta — pesos negativos por marcadores de oposición (elicitación sin sesgo).
  - Si un texto contiene un marcador de oposición → co-ocurrencias contribuyen
    negativamente: w_ij -= freq / norm.
  - Si no → contribuyen positivamente: w_ij += freq / norm.
  - W resultante ∈ [−1, +1]. Tensión estructural real.
  - Los marcadores son la señal — no se asume oposición; el texto la declara.
"""

from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from node_extractor import (NodeExtractorService, DECLARACION_REF,
                            hash_fuente, hash_lista)
from w_version import WVersionManager


# ---------------------------------------------------------------------------
# Marcadores de oposición — elicitación sin sesgo
# El texto declara la oposición; el diseñador no la asume.
# Cobertura: ES + EN, debate real, registro formal e informal.
# ---------------------------------------------------------------------------
_OPPOSITION_MARKERS: set[str] = {
    # español
    "no estoy de acuerdo", "en desacuerdo", "discrepo", "discrepa",
    "incorrecto", "es falso", "eso es falso", "es mentira",
    "al contrario", "por el contrario", "sin embargo", "pero",
    "aunque", "a pesar de", "no obstante", "contradice", "niega",
    "refuta", "rechaza", "se opone", "opuesto a", "contrario a",
    # english
    "i disagree", "disagree", "that's wrong", "that is wrong",
    "incorrect", "false", "not true", "on the contrary",
    "however", "but", "although", "despite", "contradicts",
    "refutes", "opposes", "opposite", "against", "unlike",
    "wrong", "misleading", "no evidence", "debunked",
}


class CorpusService:

    def __init__(
        self,
        storage_path : str  = "corpus_state.json",
        min_texts    : int  = 3,    # umbral para pasar a modo evaluación
        top_k        : int  = 20,
        ngram_max    : int  = 2,
        monitor_jsonl_path: Optional[str] = None,
        force_w_pos  : bool = False,
        rebuild_suspendido: bool = False,
    ):
        self.storage_path = Path(storage_path)
        self.min_texts    = min_texts
        self._extractor   = NodeExtractorService(top_k=top_k, ngram_max=ngram_max)
        self._monitor_jsonl_path = monitor_jsonl_path
        # FLAG DE DESARROLLO — no usar en operacion normal.
        # force_w_pos=True saltea el ruteo por marcadores de oposicion en
        # _rebuild(): todos los pares van a pos_counts, con lo cual
        # W = (pos + neg)/max en vez de (pos - neg)/max. Es el contrafactico
        # exacto "mismo corpus, sin codificar su tension": el corpus conserva
        # los marcadores, el servicio no los traduce a pesos negativos.
        # No es un estado alcanzable por el ciclo natural de servicios — solo
        # sirve para verificar comportamiento del instrumento.
        # La W resultante queda MARCADA en la traza (causal_event y
        # forced_w_pos en el estado persistido) para que no sea
        # indistinguible de una W natural.
        self._force_w_pos = force_w_pos
        # Rebuild suspendido (delamor, sep 2026 — también en vivo): W se
        # construye UNA vez, cuando el dato distingue (primer build con
        # nodos), y después los textos se acumulan sin reconstruir. Con la
        # regla de desempate ese primer build es el bootstrap: sin
        # precedente, empatados afuera. REG_seleccion_nodos_desempate_v1.
        self._rebuild_suspendido = rebuild_suspendido

        # estado
        self._texts     : List[str]            = []
        self._nodes     : List[str]            = []
        self._W         : Optional[np.ndarray] = None
        self._w_versions: WVersionManager      = WVersionManager()
        # Las declaraciones de extraccion vistas, indexadas por su sha. Cada
        # marca de w_version apunta aca. Una sola copia por declaracion.
        self._declaraciones: Dict[str, Dict]   = {}

        if self.storage_path.exists() and self.storage_path.stat().st_size > 0:
            self._load()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def ingest(self, texts: List[str], landscape_signal: Optional[list] = None) -> dict:
        """
        Agrega textos al corpus. Reconstruye W si hay suficientes datos.
        Devuelve estado actual.
        """
        self._texts.extend(texts)
        if landscape_signal is not None:
            self._last_landscape_signal = landscape_signal
        if len(self._texts) >= self.min_texts:
            if not (self._rebuild_suspendido and self._W is not None):
                self._rebuild()
        self.save()
        return self.status()

    @property
    def mode(self) -> str:
        return "evaluation" if self._W is not None else "accumulation"

    def get_W(self) -> Optional[np.ndarray]:
        return self._W.copy() if self._W is not None else None

    @property
    def coco(self):
        """
        **DEPRECADA (CP4, 8 oct 2026).** Devuelve None: CorpusService ya no
        crea COCO.

        COCO es de Monitor, que lo hace nacer y renacer con el ciclo vigente
        de la Config. Quien lo necesite, lo pide a `MonitorService.thermostat`.

        No se borra todavía porque la traza Armstrong
        (`iap_chatroom/tests/test_armstrong_via_corpus_v3.py`,
        `test_armstrong_n_runs_sweep.py`) la usa, y esos tests son traza
        registrada y no se modifican. Siguen pudiendo asignar `_coco` a mano,
        que es lo que ya hacen; lo que ya no pasa es que el rebuild lo cree.
        """
        return getattr(self, '_coco', None)

    def w_sha(self) -> Optional[str]:
        """sha256 de W en el momento actual. Para Firma_CKM."""
        return self._w_versions.current_sha()

    def w_changed_since(self, sha: str) -> bool:
        """True si W cambió desde la versión sha. Señal de invalidación beta_c_corpus."""
        return self._w_versions.changed_since(sha)

    def w_change_since(self, sha: str, nodes: List[str]) -> dict:
        """
        Cómo cambió W desde la versión con la que opera quien consulta.

        Quien consulta pasa su sha y los nodos con los que opera: los nodos
        por versión no se persisten. Notifica, no invalida — qué hacer con
        Δ_r, A0 o la config es D2. Ver
        docs/tasks/TASK_rebuild_consulta_w_version_v1.md.

        nodes_changed cubre conjunto u orden: con N fijo en top_k, cada
        rebuild puede re-extraer otros nodos en las mismas posiciones.
        """
        nodes_new = self.get_nodes()
        return {
            "changed"         : self.w_changed_since(sha),
            "w_version_id_old": sha,
            "w_version_id_new": self.w_sha(),
            "N_old"           : len(nodes),
            "N_new"           : len(nodes_new),
            "nodes_changed"   : list(nodes) != nodes_new,
        }

    def get_nodes(self) -> List[str]:
        return list(self._nodes)

    def should_rebuild(self, d_ckm_history: List[float], n: int = 3) -> bool:
        """
        Retorna True si el gradiente de D_ckm es positivo sostenido por n pasos.
        Señal estructural de rebuild — complementa el criterio de volumen.
        """
        if len(d_ckm_history) < n + 1:
            return False
        recent = d_ckm_history[-(n + 1):]
        gradients = [recent[i + 1] - recent[i] for i in range(n)]
        return all(g > 0 for g in gradients)

    def status(self) -> dict:
        W = self._W
        neg_frac = None
        if W is not None:
            total   = W.size - W.shape[0]
            n_neg   = int(np.sum(W < 0))
            n_pos   = int(np.sum(W > 0))
            neg_frac = round(n_neg / total, 3) if total > 0 else 0.0
        return {
            "mode"       : self.mode,
            "n_texts"    : len(self._texts),
            "n_nodes"    : len(self._nodes),
            "min_texts"  : self.min_texts,
            "W_shape"    : list(W.shape) if W is not None else None,
            "W_sparsity" : self._sparsity() if W is not None else None,
            "W_neg_frac" : neg_frac,
            "w_sha"      : self._w_versions.current_sha(),   # Firma_CKM
            "rebuild_suspendido": self._rebuild_suspendido,
        }

    # ------------------------------------------------------------------
    # La declaración
    # ------------------------------------------------------------------

    def declaracion_extraccion(self) -> Dict:
        """
        **Los 8 operadores, como dato.** La del extractor (1–6) más el signo
        (7) y W (8), que son de acá.

        Canónica: `docs/defs/DECLARACION_extraccion_W_v1.md`. Hay un test que
        verifica que el código y el documento digan lo mismo; si no coinciden
        **se corrige el documento**, no el extractor (regla de delamor, 14 oct).

        Viaja atada al `sha256` de W: cada marca de `w_version` guarda el
        `declaracion_sha` de la declaración bajo la que se produjo **esa** W.
        Los dicts viven una sola vez, en `self._declaraciones`.
        """
        d = self._extractor.declaracion()
        d["productor"] = {
            "nombre"    : "CKM NodeExtractorService + CorpusService",
            "sha_fuente": {
                "node_extractor.py": d["productor"]["sha_fuente"],
                "corpus_service.py": hash_fuente(Path(__file__)),
            },
        }
        d["operadores"]["7_signo"] = {
            "que_hace": (
                "s(u) = -1 si u, pasado a minusculas, contiene algun marcador de "
                "oposicion (busqueda de SUBCADENA sobre el texto entero), +1 si no"
            ),
            "parametros": {
                "n_marcadores": len(_OPPOSITION_MARKERS),
                "hash"        : hash_lista(_OPPOSITION_MARKERS),
                "origen"      : ("ES + EN, debate real, registro formal e informal; "
                                 "embebidos en corpus_service.py"),
                "force_w_pos" : self._force_w_pos,
            },
            # La condicion (b) del CP0, DECLARADA por decision de delamor
            # (14 oct): no se toca el codigo, se escribe lo que hace.
            "condicion_declarada": (
                "el texto NO se normaliza a NFC antes de buscar marcadores, a "
                "diferencia del operador 1; hoy sin efecto porque los marcadores "
                "son ASCII. force_w_pos anula el signo."
            ),
            "referencia": "review v28 M4: este operador no tiene resultado nulo",
        }
        d["operadores"]["8_W"] = {
            "que_hace": ("W_ij = suma_u s(u)*chi_i(u)*chi_j(u) / max|.|, W_ii = 0; "
                         "cada par cuenta 1 POR UNIDAD, no por repeticion"),
            "parametros": {
                "conteo_por_unidad": 1,
                "normalizacion"    : "max|pos - neg|, o sin dividir si es 0",
                "diagonal"         : 0.0,
                "rango"            : [-1.0, 1.0],
            },
            "referencia": "Salton, Wong & Yang 1975",
        }
        return d

    @staticmethod
    def _sha_declaracion(d: Dict) -> str:
        """sha256 de la declaración, con las claves ordenadas: mismo contenido,
        mismo sha, para que dos W bajo la misma declaración la compartan."""
        crudo = json.dumps(d, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(crudo.encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Construcción de W  (v2 — mixta)
    # ------------------------------------------------------------------

    @staticmethod
    def _has_opposition(text: str) -> bool:
        """True si el texto contiene al menos un marcador de oposición."""
        t = text.lower()
        return any(m in t for m in _OPPOSITION_MARKERS)

    def _accumulate_safe(self, texts: List[str], seleccion_anterior=None) -> Dict:
        """
        Wrapper de self._extractor.accumulate() que absorbe el ValueError de
        TfidfVectorizer cuando un texto (o el batch) no aporta vocabulario
        tras stopwords + token_pattern — p.ej. mensajes muy cortos como
        "ok", "[quiet]" o textos de una sola stopword. Sin este guard, un
        solo mensaje degenerado tumba _rebuild() y deja self._texts
        envenenado (el texto ya fue extend()-ido antes de rebuild), lo que
        rompe todo ingest() futuro hasta reiniciar el proceso.
        """
        try:
            return self._extractor.accumulate(texts, seleccion_anterior=seleccion_anterior)
        except ValueError:
            return {"nodes": [], "pairs": {}, "node_freq": {}}

    def rebuild_por_decision(self, causa: str) -> dict:
        """
        Rebuild **por decisión**, no por ingesta. Devuelve `status()`.

        `causa` es **obligatoria y sin default** (misma forma que `n_agentes`
        esta mañana): un rebuild sin causa declarada no es una decisión, es un
        rebuild sin nombre. Queda en `causal_event` de `w_version`.

        **`rebuild_suspendido` no lo bloquea** (TASK, punto 1): ese flag impide
        el rebuild **automático por ingesta**, que es lo que delamor descartó
        —*"la ingesta no debe implicar rebuilds continuos"*—. El rebuild por
        decisión es lo contrario de eso: es el salto entre mesetas.

        Con el corpus en acumulación **no reconstruye y lo dice**: la primera W
        se construye al cruzar `min_texts`, como hoy. Devolver un status normal
        acá haría que un rebuild que no ocurrió se viera igual que uno que sí.
        """
        if not causa:
            raise ValueError(
                "rebuild_por_decision necesita una causa declarada: un rebuild "
                "sin causa no es una decisión"
            )
        if len(self._texts) < self.min_texts:
            st = self.status()
            st["rebuild"] = False
            st["motivo_no_rebuild"] = "corpus_en_acumulacion"
            st["causa_pedida"] = causa
            return st
        self._rebuild(causa=causa)
        self.save()
        st = self.status()
        st["rebuild"] = True
        st["causa"] = causa
        return st

    def _rebuild(self, causa: Optional[str] = None) -> None:
        """
        Reconstruye nodos y W desde todos los textos acumulados.

        `causa` llega sólo desde `rebuild_por_decision`. Sin ella el
        `causal_event` es el de siempre, así que el rebuild por ingesta no
        cambia de marca.

        Ruteo por texto:
          - sin marcador → pares suman a pos_counts
          - con marcador → pares suman a neg_counts
        W[i,j] = (pos[i,j] - neg[i,j]) / max(|pos - neg|)
        Rango resultante: [−1, +1].
        """
        # la selección anterior resuelve los empates en el borde del top_k
        # (regla de la relajación: empate conserva). TASK_desempate_seleccion_nodos_v1.
        result = self._accumulate_safe(self._texts, seleccion_anterior=self._nodes or None)
        nodes  = result["nodes"]

        if not nodes:
            return

        N        = len(nodes)
        node_idx = {n: i for i, n in enumerate(nodes)}

        pos_counts = np.zeros((N, N))
        neg_counts = np.zeros((N, N))

        # pares por texto entre los NODOS GLOBALES, de la misma extracción
        # que eligió los nodos. Antes se re-extraía cada texto con
        # accumulate([texto]), que hace otro top_k dentro del texto y
        # perdía pares (46% en caso09 bootstrap 12; nodos aislados).
        # TASK_pares_por_texto_nodos_globales_v1.
        por_texto = result.get("pairs_by_text", [])
        for k, text in enumerate(self._texts):
            t_pairs     = por_texto[k] if k < len(por_texto) else {}
            is_opp      = False if self._force_w_pos else self._has_opposition(text)

            for (ni, nj), count in t_pairs.items():
                if ni in node_idx and nj in node_idx:
                    i, j = node_idx[ni], node_idx[nj]
                    if is_opp:
                        neg_counts[i, j] += count
                        neg_counts[j, i] += count
                    else:
                        pos_counts[i, j] += count
                        pos_counts[j, i] += count

        raw = pos_counts - neg_counts
        max_abs = np.abs(raw).max()

        if max_abs > 0:
            W = raw / max_abs
        else:
            W = raw   # todo ceros — corpus sin señal aún

        np.fill_diagonal(W, 0.0)
        self._nodes = nodes
        self._W     = W
        # La declaracion y el registro del borde DESCRIBEN LA W QUE ESTÁ VIVA,
        # así que se escriben acá, con ella, y no apenas vuelve `accumulate`.
        #
        # Antes se asignaban arriba, antes del `return` por `nodes` vacío
        # (divergencia (a) del CP0, 14 oct). Una extracción que falla hace que
        # `_accumulate_safe` devuelva un dict **sin** `"perfil"`, así que la W
        # anterior quedaba viva y su declaración en `None`. El `None` de
        # `_load` dice "no se sabe bajo qué condición se extrajo" y es cierto;
        # aquél decía lo mismo y era falso. Es I2 al revés: no se completa de
        # más, se borra de menos. `tests/test_extraccion_fallida_no_borra.py`.
        #
        # CP1: la declaracion de los 8 operadores bajo la que se produjo esta
        # W. Se guarda UNA vez, indexada por su sha, y la marca de w_version
        # apunta a ella.
        declaracion = self.declaracion_extraccion()
        decl_sha    = self._sha_declaracion(declaracion)
        self._declaraciones[decl_sha] = declaracion
        self._declaracion_sha   = decl_sha
        self._registro_borde    = result.get("registro_borde", [])
        # El `causal_event`, con la causa de la decisión si hubo.
        #
        # El marcador `force_w_pos` **no se pierde** cuando hay causa: lo usan
        # dos tests como traza de que esa W fue forzada
        # (`test_wmixta_forzado_paso3`, `test_armstrong_wmixta_forced_wpos`), y
        # borrarlo al agregar la causa haría que una W forzada por decisión se
        # viera como una W normal.
        if causa:
            evento = f"rebuild_por_decision:{causa}"
            if self._force_w_pos:
                evento += "+debug_force_w_pos"
        else:
            evento = (
                "rebuild_debug_force_w_pos" if self._force_w_pos else "rebuild"
            )
        self._w_versions.register(W, len(self._texts), causal_event=evento,
                                  declaracion_sha=decl_sha)

        # CorpusService ya no crea COCO (CP4 de TASK_monitor_coco_ciclo_orbita_v2;
        # delamor: "Que deje en paz a COCO. COCO es con Monitor").
        # Construye W y la versiona; eso es todo. COCO vive dentro de Monitor,
        # que lo hace nacer y renacer con el ciclo vigente de la Config.
        #
        # Lo que esto arregla: antes quedaban dos COCO vivos —el de acá, con la
        # W nueva y que nunca observaba, y el que Monitor había recibido, con la
        # W congelada—. El CP1 lo midió rompiendo:
        # ValueError: shapes (31,31) (28,28) en coco.py:254.

    def _sparsity(self) -> float:
        if self._W is None:
            return 1.0
        total    = self._W.size - self._W.shape[0]   # excluye diagonal
        nonzero  = np.count_nonzero(self._W) - np.count_nonzero(np.diag(self._W))
        return round(1 - nonzero / total, 3) if total > 0 else 1.0

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------

    def save(self) -> None:
        state = {
            "texts"           : self._texts,
            "nodes"           : self._nodes,
            "W"               : self._W.tolist() if self._W is not None else None,
            "w_version_history": self._w_versions.to_list(),
            "forced_w_pos"    : self._force_w_pos,
            # registro continuo del borde de la última selección de nodos
            "registro_borde"  : getattr(self, "_registro_borde", []),
            # CP1: las declaraciones de extraccion vistas, por sha. El perfil
            # de idioma (S0b) vive ADENTRO de cada una, no duplicado afuera.
            # Cada marca de `w_version_history` dice con cual se produjo su W;
            # `declaracion_sha: null` ahi quiere decir **no se sabe**, y NO se
            # rellena con la de hoy: poner la de hoy en una W de ayer
            # afirmaría una condición que nadie registró (I2).
            "declaraciones"    : getattr(self, "_declaraciones", {}),
            "declaracion_sha"  : getattr(self, "_declaracion_sha", None),
        }
        self.storage_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def _load(self) -> None:
        state       = json.loads(self.storage_path.read_text())
        self._texts = state.get("texts", [])
        self._nodes = state.get("nodes", [])
        raw_W       = state.get("W")
        self._W     = np.array(raw_W) if raw_W is not None else None
        self._w_versions.from_list(state.get("w_version_history", []))
        self._registro_borde = state.get("registro_borde", [])
        # `None` / `{}` declarados: los estados anteriores al CP1 no los
        # tienen, y sus marcas quedan con `declaracion_sha: None` — no se sabe.
        self._declaraciones   = state.get("declaraciones", {})
        self._declaracion_sha = state.get("declaracion_sha")


# ---------------------------------------------------------------------------
# Test mínimo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile, os

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name

    corpus = CorpusService(storage_path=tmp, min_texts=5, top_k=10)

    # batch con textos de debate — oposición explícita
    batch_1 = [
        "gun control reduces violence and saves lives",
        "the second amendment protects the right to bear arms",
        "background checks prevent criminals from buying weapons",
    ]
    batch_2 = [
        "assault weapons bans reduce mass shootings",
        "however, gun rights are constitutional rights not subject to restriction",   # marcador
        "mental health is the real cause of gun violence, not guns",                  # marcador implícito
        "i disagree — armed citizens deter crime and protect communities",            # marcador explícito
    ]

    print("=== INGEST batch 1 ===")
    print(corpus.ingest(batch_1))

    print("\n=== INGEST batch 2 ===")
    status = corpus.ingest(batch_2)
    print(status)

    if corpus.mode == "evaluation":
        W = corpus.get_W()
        print(f"\nNodos: {corpus.get_nodes()}")
        print(f"W shape: {W.shape}")
        print(f"W min: {W.min():.3f}  W max: {W.max():.3f}")
        print(f"Pesos negativos: {(W < 0).sum()}  positivos: {(W > 0).sum()}")
        print(f"W_neg_frac: {status['W_neg_frac']}")

        # muestra los pares más negativos (tensión estructural)
        nodes = corpus.get_nodes()
        pairs_neg = []
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if W[i, j] < 0:
                    pairs_neg.append((W[i, j], nodes[i], nodes[j]))
        pairs_neg.sort()
        print("\nTop pares negativos (tensión):")
        for w, a, b in pairs_neg[:5]:
            print(f"  {a} — {b}  : {w:.3f}")

    os.unlink(tmp)
