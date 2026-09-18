"""
monitor_service.py — Collective MonitorService

Stateful. Evalúa prompts contra el corpus acumulado.
Mide fabricación: lo que σ_prompt declaró y el campo rechazó.

Δ_r acumula co-ocurrencias de rechazos:
  pares (i,j) que σ_prompt declaró activos pero relax expulsó.
  Δ_r[i,j] += 1 por cada evaluación donde el par fue rechazado.

Rango de W (heredado de CorpusService): W ∈ [−1, +1]. `_rebuild()` calcula
(pos_counts − neg_counts) / max|·|, y rutea a neg_counts los textos con
marcador de oposición. c(S) es informativo cuando hay tensión estructural,
que es justamente lo que codifican los pesos negativos.

COCO (thermostat) es opcional — `thermostat=None` por defecto. Sin él no
hay compresión de Δ_r, ni β, ni temp_signal, y `panel["thermostat"]` es
None; el resto del panel se emite igual. Con él, COCO lee Δ_r y comprime
su propia representación (Δ_r_compresiones); Δ_r no recibe nada de COCO
(D3, ver evaluate()).

Este docstring describe lo que el código no dice de sí mismo. La firma del
constructor, el cuerpo de evaluate() y la escala de _combine_W_Delta viven
en el código, y ahí se leen — copiarlos acá crea una rama que se congela
sin señal de estar desactualizada.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional

import numpy as np

from node_extractor import NodeExtractorService
from corpus_service  import CorpusService
from coco import COCO, ThermostatState, BETA_RHO_STAR
from ckm_landscape_config import CKMlandscapeConfig
from landscape_engine import (
    beta_c_landscape,
    boltzmann_warmup,
    basin_masses,
    count_attractors,
    d_masa_cuencas,
    n_eff,
    node_probs,
    relax,
    relax_orbit,
    sample_s0,
)

try:
    from behavior_graph import BehaviorGraph as _BehaviorGraph
    _HAS_G = True
except ImportError:
    _HAS_G = False


class MonitorService:

    def __init__(
        self,
        corpus          : CorpusService,
        storage_path    : str = "monitor_trajectory.jsonl",
        n_runs_attractors: int = 50,
        thermostat      : Optional[COCO] = None,
        behavior_graph  : Optional[object] = None,   # BehaviorGraph | None
        count_seed      : int = 0,
        sampling_mode   : str = "uniform",
        n_warmup        : Optional[int] = None,
        landscape_config: Optional[CKMlandscapeConfig] = None,
    ):
        """
        count_seed / sampling_mode / n_warmup gobiernan el muestreo de
        sigma_0 en _count_attractors(). Sus defaults —seed=0, uniform—
        son los valores que este servicio usaba hardcodeados, de modo que
        el comportamiento numerico no cambia. Ver TASK_monitor_service_
        unificar_rutinas_v1.md: la equivalencia con COCO(seed=0) fue
        verificada exacta antes de unificar.

        landscape_config: config que produjo este run, ya construida por
        quien arma el run — Monitor no decide calibración. Viaja serializada
        en cada panel como "landscape_config" (None si no se pasa). Es la
        config del contador de Monitor, no la de COCO. Se fija una vez por
        run: tras un rebuild su w_version_id puede no coincidir con la W
        vigente (D7). Ver docs/tasks/TASK_landscape_config_en_runs_v1.md.
        """
        self.corpus    = corpus
        self._storage  = Path(storage_path)
        self._extractor = NodeExtractorService()
        self._n_runs   = n_runs_attractors
        self._thermostat = thermostat
        self._g         = behavior_graph

        if sampling_mode not in ("uniform", "weighted", "boltzmann"):
            raise ValueError(
                f"sampling_mode invalido: {sampling_mode!r} — "
                "esperado 'uniform', 'weighted' o 'boltzmann'."
            )
        self._count_seed    = count_seed
        self._sampling_mode = sampling_mode
        self._n_warmup      = n_warmup
        if landscape_config is not None and landscape_config.sampling_mode != sampling_mode:
            raise ValueError(
                f"landscape_config.sampling_mode={landscape_config.sampling_mode!r} "
                f"no coincide con sampling_mode={sampling_mode!r} de este Monitor — "
                "el panel llevaría una config que no describe cómo contó."
            )
        self._landscape_config = landscape_config

        self._Delta_r : Optional[np.ndarray] = None
        self._A0    : Optional[int]        = None
        self._N_eff0: Optional[float]      = None   # baseline de N_eff, vive con A0
        # versión de W bajo la que se acumuló Δ_r — ver _invalidar_si_W_cambio
        self._w_sha   : Optional[str]       = None
        self._w_nodes : Optional[list]      = None

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def evaluate(self, text: str, device_id: Optional[str] = None) -> Optional[dict]:
        """
        Evalúa un prompt. Devuelve panel o None si corpus en acumulación.
        """
        if self.corpus.mode == "accumulation":
            return {"mode": "accumulation", "message": "corpus insuficiente — guardando traza"}

        W     = self.corpus.get_W()
        nodes = self.corpus.get_nodes()
        N     = len(nodes)

        reset_cause = self._invalidar_si_W_cambio(nodes)

        if self._Delta_r is None or self._Delta_r.shape != (N, N):
            self._Delta_r = np.zeros((N, N))

        # σ declarado por el prompt
        sigma_prompt = self._extractor.evaluate(text, nodes)

        # σ que el campo acepta
        sigma_relaxed = self._relax(sigma_prompt.copy(), self._combine_W_Delta(W, self._Delta_r))

        # pares rechazados → acumular en Δ
        rejected = self._rejected_pairs(sigma_prompt, sigma_relaxed)
        for i, j in rejected:
            self._Delta_r[i, j] += 1
            self._Delta_r[j, i] += 1

        # métricas
        c_s   = self._cS(sigma_relaxed, W)
        fi    = self._fabrication_index(sigma_prompt, sigma_relaxed)
        D_ckm = self._D_ckm(W)
        N_eff = self._N_eff(W)

        # G_state — paralelo a {W, Δ_W}, no retroactivo
        g_state_panel = None
        if self._g is not None:
            self._g.ingest([text])
            g_state_panel = self._g.g_state()
            g_state_panel["active_behavior"] = self._g.active_nodes(text)

        panel = {
            "c_S"              : round(c_s,  6),
            "fabrication_index": round(fi,   4),
            "D_ckm"            : round(D_ckm, 4),
            # N_eff = 1/Σm² sobre masas de cuenca por órbita, misma W_eff y
            # mismas muestras que D_ckm. N_eff0 es su baseline (se fija y se
            # resetea como A0). D_masa_cuencas en escala log (delamor):
            # 1 − ln N_eff / ln N_eff0; None si N_eff0 ≤ 1.
            "N_eff"            : round(N_eff, 4),
            "N_eff0"           : round(self._N_eff0, 4) if self._N_eff0 is not None else None,
            "D_masa_cuencas"   : (lambda d: round(d, 4) if d is not None else None)(
                                     d_masa_cuencas(N_eff, self._N_eff0)),
            # Condiciones de la medición — no se excluye nada, se declara.
            # Un aislado (fila de W en cero) duplica cada atractor acoplado;
            # Δ_r puede acoplarlo en W_eff durante el run (REG v3 §4).
            # REG_hipotesis_distancia_contextual_v4.
            "condicion_W"      : self._condicion_W(W, nodes),
            "n_rejected_pairs" : len(rejected),
            "Delta_r_sum"        : float(np.sum(self._Delta_r)),
            "activos_prompt"   : [nodes[i] for i, s in enumerate(sigma_prompt)   if s > 0],
            "activos_relajado" : [nodes[i] for i, s in enumerate(sigma_relaxed)  if s > 0],
            "rechazados"       : [(nodes[i], nodes[j]) for i, j in rejected],
            # modo con el que ESTE servicio conto atractores para D_ckm.
            # Distinto del de panel["thermostat"]["sampling_mode"], que es
            # el de COCO: son dos contadores independientes.
            "sampling_mode"    : self._sampling_mode,
            "thermostat"       : None,
            "G_state"          : g_state_panel,
            # None si Δ_r siguió acumulando; "N" | "nodos" | "pesos" si esta
            # evaluación empezó con Δ_r y A0 en cero por reconstrucción de W.
            "Delta_r_reset"    : reset_cause,
            # Admisión (node-level, C1) y metabolización (pair-level, Δ_r)
            # son objetos distintos. Nadie evalúa C1 todavía: None dice que
            # esta Δ_r se acumuló sin admisión previa. Cuando alguien lo
            # conecte, esta clave lleva al menos el θ_W usado.
            # Ver docs/tasks/TASK_traza_gatekeeper_c1_v1.md.
            "gatekeeper_c1"    : None,
            "landscape_config" : (
                self._landscape_config.to_dict()
                if self._landscape_config is not None else None
            ),
        }

        # COCO lee Δ_r y regula su propia representación (D3). La
        # regulación no llega a Δ_r: Monitor es su único escritor.
        if self._thermostat is not None:
            if device_id is not None:
                self._thermostat.register_device_eval(device_id, fi)
            ts = self._thermostat.observe(self._Delta_r)
            panel["thermostat"] = {
                "zone"        : ts.zone,
                "D_ckm"       : ts.D_ckm,
                "frac_rec"    : ts.frac_rec,
                "stop_applied": ts.stop_applied,
                "alpha_used"  : ts.alpha_used,
                "beta"        : self._thermostat.beta_status(),
                "temp_signal" : self._thermostat.temp_signal(),
                "landscape_delta": getattr(self._thermostat, "_last_landscape_delta", None),
                "landscape_component": (
                    self._thermostat._last_landscape_component
                    if getattr(self._thermostat, "_track_landscape", False)
                    else None
                ),
                "gamma"  : getattr(self._thermostat, "_gamma", None),
                "n_runs" : getattr(self._thermostat, "_n_runs", None),
                # modo de muestreo de sigma_0 que produjo este D_ckm —
                # uniform | weighted | boltzmann. Trazabilidad: el mismo
                # Δ_r puede caer de un lado u otro de D_CKM_THRESHOLD
                # según el modo (REG_stochastic_eval_v2).
                "sampling_mode": getattr(self._thermostat, "_sampling_mode", None),
                "n_warmup": (
                    getattr(self._thermostat, "_n_warmup", None)
                    if getattr(self._thermostat, "_sampling_mode", None) == "boltzmann"
                    else None
                ),
            }

        self._persist(text, panel, device_id)
        return panel

    def _invalidar_si_W_cambio(self, nodes: list) -> Optional[str]:
        """
        Δ_r y A0 se descartan en cualquier reconstrucción de W (D2).

        Aunque los índices sean los mismos, los pesos que produjeron esa Δ_r
        ya no son los vigentes; y A0 sería el baseline de otro campo. La
        señal es w_version_id. Devuelve la causa —"N" | "nodos" | "pesos"—
        o None si W no cambió. COCO queda fuera de alcance: sigue operando
        con la W de su construcción.
        Ver docs/tasks/TASK_invalidacion_delta_r_v1.md.
        """
        sha_actual = self.corpus.w_sha()
        if self._w_sha is None:                       # primera evaluación
            self._w_sha, self._w_nodes = sha_actual, list(nodes)
            return None
        if sha_actual == self._w_sha:
            return None

        cambio = self.corpus.w_change_since(self._w_sha, self._w_nodes)
        if cambio["N_old"] != cambio["N_new"]:
            causa = "N"
        elif cambio["nodes_changed"]:
            causa = "nodos"
        else:
            causa = "pesos"

        self._Delta_r = np.zeros((len(nodes), len(nodes)))
        self._A0      = None
        self._N_eff0  = None
        self._w_sha, self._w_nodes = sha_actual, list(nodes)
        return causa

    def trajectory(self) -> list:
        if not self._storage.exists():
            return []
        with open(self._storage) as f:
            return [json.loads(l) for l in f if l.strip()]

    def stop_signal(self, window: int = 5) -> dict:
        traj = self.trajectory()
        if len(traj) < 2:
            return {"signal": False, "reason": "trayectoria insuficiente"}

        recent   = traj[-window:]
        fi_vals  = [r["panel"]["fabrication_index"] for r in recent]
        D_vals   = [r["panel"]["D_ckm"]             for r in recent]
        fi_trend = fi_vals[-1] - fi_vals[0]
        D_trend  = D_vals[-1]  - D_vals[0]
        signal   = fi_trend > 0.05 and D_trend > 0.02

        return {
            "signal"   : signal,
            "fi_trend" : round(fi_trend, 4),
            "D_trend"  : round(D_trend,  4),
            "direction": "CONVERGING" if fi_trend < -0.05 else "DIVERGING" if signal else "STABLE",
        }

    # ------------------------------------------------------------------
    # Operaciones internas
    # ------------------------------------------------------------------

    def _relax_orbit(self, sigma, W, max_iter: int = 200) -> tuple:
        """Órbita alcanzada — landscape_engine.relax_orbit."""
        return relax_orbit(sigma, W, max_iter)

    def _relax(self, sigma: np.ndarray, W: np.ndarray, max_iter: int = 200) -> np.ndarray:
        """
        Estado alcanzado tras max_iter pasos de relajación síncrona —
        landscape_engine.relax.

        max_iter 100 y 200 son ambos PARES: una órbita de periodo 2 devuelve
        la misma fase en los dos, y el test que separa los casos es 100
        contra 101. Medido así: en caso09_run2 natural, 136 de 200 runs NO
        llegan a punto fijo; en WARMUP_TEXTS, 141 de 200; en
        W_ckm_corpus_v2 (N=32), 3 de 200.
        """
        return relax(sigma, W, max_iter)


    def _combine_W_Delta(self, W: np.ndarray, Delta: np.ndarray) -> np.ndarray:
        """
        Combina W y Delta_r en escalas compatibles.

        W ∈ [−1, +1] (normalizado por CorpusService: (pos − neg)/max|·|).
        Delta_r ∈ [0, ∞) (conteos enteros de rechazos).

        Normalización: Delta_r / max(Delta_r) → [0,1],
        luego escala por la media de los pesos POSITIVOS de W para
        preservar magnitud relativa. Si Delta es cero (inicio de sesión),
        devuelve W sin modificar.

        La escala usa solo W>0 — no |W| ni todos los no-cero. Data de
        cuando W era positiva y `W_nonzero` y `W>0` eran el mismo conjunto.
        Se mantiene el comportamiento; queda dicho que es una elección,
        no una consecuencia del rango de W.
        """
        delta_max = Delta.max()
        if delta_max == 0:
            return W
        W_nonzero = W[W > 0]
        scale = W_nonzero.mean() if len(W_nonzero) > 0 else 1.0
        Delta_norm = (Delta / delta_max) * scale
        return W + Delta_norm

    def _rejected_pairs(self, sigma_p: np.ndarray, sigma_r: np.ndarray):
        """Pares que sigma_prompt declaró activos pero relax expulsó."""
        declared = np.where(sigma_p > 0)[0]
        rejected_nodes = set(np.where(sigma_r < 0)[0])
        pairs = []
        for i in range(len(declared)):
            for j in range(i + 1, len(declared)):
                ni, nj = declared[i], declared[j]
                if ni in rejected_nodes or nj in rejected_nodes:
                    pairs.append((int(ni), int(nj)))
        return pairs

    def _cS(self, sigma: np.ndarray, W: np.ndarray) -> float:
        ii, jj = np.triu_indices(len(sigma), k=1)
        return float(np.mean(W[ii, jj] * sigma[ii] * sigma[jj]))

    def _fabrication_index(self, sigma_p: np.ndarray, sigma_r: np.ndarray) -> float:
        """Fracción de nodos declarados activos que fueron rechazados."""
        declared = (sigma_p > 0).sum()
        if declared == 0:
            return 0.0
        rejected = ((sigma_p > 0) & (sigma_r < 0)).sum()
        return float(rejected / declared)

    def _D_ckm(self, W: np.ndarray) -> float:
        """D_ckm = (A0 - A_actual) / A0. Puede ser negativo.

        A0 se fija en la primera llamada con corpus establecido (mode != accumulation).
        Se usa _combine_W_Delta para escala compatible W + Delta_r.
        """
        Delta    = self._Delta_r if self._Delta_r is not None else np.zeros_like(W)
        W_eff    = self._combine_W_Delta(W, Delta)
        A_actual = self._count_attractors(W_eff)
        if self._A0 is None:
            if A_actual == 0:
                return 0.0   # corpus vacío — diferir A0
            self._A0 = A_actual
        return float((self._A0 - A_actual) / self._A0) if self._A0 > 0 else 0.0

    def _condicion_W(self, W: np.ndarray, nodes: list) -> dict:
        """Bajo qué W y con qué muestreo se midió este panel."""
        W_eff = self._combine_W_Delta(W, self._Delta_r)
        return {
            "w_sha"         : self.corpus.w_sha(),
            "N"             : len(nodes),
            "n_runs"        : self._n_runs,
            "count_seed"    : self._count_seed,
            "aislados_W"    : [nodes[i] for i in np.where(~W.any(axis=1))[0]],
            "aislados_W_eff": [nodes[i] for i in np.where(~W_eff.any(axis=1))[0]],
        }

    def _N_eff(self, W: np.ndarray) -> float:
        """N_eff sobre la misma W_eff que _D_ckm. Fija N_eff0 en la primera
        llamada del ciclo de W (como A0)."""
        Delta = self._Delta_r if self._Delta_r is not None else np.zeros_like(W)
        W_eff = self._combine_W_Delta(W, Delta)
        masas = basin_masses(
            W_eff, n_runs=self._n_runs, seed=self._count_seed,
            weighted=self._sampling_mode == "weighted",
            boltzmann=self._sampling_mode == "boltzmann",
            n_warmup=self._n_warmup,
        )
        valor = n_eff(masas)
        if self._N_eff0 is None:
            self._N_eff0 = valor
        return valor

    # ── Paisaje — delegado en landscape_engine ───────────────────────────
    # Cierra la duplicación que REG_monitor_service_unificar_rutinas_v1 dejó
    # declarada: la opción C había copiado estas rutinas desde coco.py. Ahora
    # viven una sola vez en services/landscape_engine.py y los dos servicios
    # delegan. Lo que NO se unifica es _combine_W_Delta: la W sobre la que
    # cuenta cada instrumento es lo que los distingue.
    # Ver docs/tasks/TASK_landscape_engine_v1.md.

    def _node_probs(self, W_eff: np.ndarray, weighted: bool) -> Optional[np.ndarray]:
        """Distribución de nodos para sigma_0 — landscape_engine.node_probs."""
        return node_probs(W_eff, weighted)

    def _beta_c_landscape(self, W_eff: np.ndarray) -> Optional[float]:
        """β_c de muestreo del paisaje — landscape_engine.beta_c_landscape."""
        return beta_c_landscape(W_eff)

    def _sample_s0(self, rng, N: int, probs: Optional[np.ndarray]) -> np.ndarray:
        """sigma_0 con 30-70% activos — landscape_engine.sample_s0."""
        return sample_s0(rng, N, probs)

    def _boltzmann_warmup(self, rng, sigma: np.ndarray, W_eff: np.ndarray,
                          beta: float, n_warmup: int) -> np.ndarray:
        """Calentamiento estocástico — landscape_engine.boltzmann_warmup."""
        return boltzmann_warmup(rng, sigma, W_eff, beta, n_warmup)

    def _count_attractors(
        self,
        W        : np.ndarray,
        weighted : Optional[bool] = None,
        boltzmann: Optional[bool] = None,
        n_warmup : Optional[int]  = None,
    ) -> int:
        """
        Atractores distintos en n_runs reinicios sobre W —
        landscape_engine.count_attractors, donde están los sesgos (n_runs sin
        saturar, distribución de sigma_0) y los tres modos documentados.

        weighted/boltzmann en None toman self._sampling_mode. Pasarlos
        explicitos permite un conteo puntual en otro modo sin cambiar la
        configuracion del servicio.
        """
        if weighted is None and boltzmann is None:
            weighted  = self._sampling_mode == "weighted"
            boltzmann = self._sampling_mode == "boltzmann"
        else:
            weighted  = bool(weighted)
            boltzmann = bool(boltzmann)

        return count_attractors(
            W, n_runs=self._n_runs, seed=self._count_seed,
            weighted=weighted, boltzmann=boltzmann,
            n_warmup=n_warmup if n_warmup is not None else self._n_warmup,
        )


    def _persist(self, text: str, panel: dict, device_id: Optional[str] = None) -> None:
        t = len(self.trajectory())
        with open(self._storage, "a") as f:
            f.write(
                json.dumps({"t": t, "device_id": device_id, "text": text[:80], "panel": panel})
                + "\n"
            )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile, os
    from coco import COCO

    tmp_corpus  = tempfile.mktemp(suffix=".json")
    tmp_monitor = tempfile.mktemp(suffix=".jsonl")

    # 1. Construir corpus
    corpus = CorpusService(storage_path=tmp_corpus, min_texts=5, top_k=10)
    corpus.ingest([
        "gun control reduces violence and saves lives",
        "the second amendment protects the right to bear arms",
        "background checks prevent criminals from buying weapons",
        "assault weapons bans reduce mass shootings",
        "gun rights are constitutional rights not subject to restriction",
        "mental health is the real cause of gun violence",
        "armed citizens deter crime and protect communities",
    ])
    print(f"T1 corpus: {corpus.status()}")
    assert corpus.mode == "evaluation", "FAIL T1"

    # T2 — sin thermostat: panel["thermostat"] == None
    monitor = MonitorService(corpus, storage_path=tmp_monitor)
    r = monitor.evaluate("gun control laws reduce violence")
    assert r["thermostat"] is None, "FAIL T2"
    print("T2 OK — sin thermostat, panel['thermostat']=None")

    os.unlink(tmp_monitor)
    tmp_monitor = tempfile.mktemp(suffix=".jsonl")

    # T3 — con thermostat: panel incluye zone y beta
    th = COCO(W=corpus.get_W(), n_runs=30, seed=0)
    monitor2 = MonitorService(corpus, storage_path=tmp_monitor, thermostat=th)

    prompts = [
        ("gun control laws reduce violence",           "deviceA"),
        ("chocolate ice cream prevents gun violence",  "deviceB"),  # fabricado
        ("rights protected by constitution",           "deviceA"),
        ("mental health backgrosund checks reduce crime","deviceB"),
    ]

    print("\n=== T3 evaluaciones con thermostat + device_id ===")
    for text, device in prompts:
        r = monitor2.evaluate(text, device_id=device)
        ts = r["thermostat"]
        print(f"  [{device}] fi={r['fabrication_index']}  zone={ts['zone']}  betsa={ts['beta']['devices']}")

    # T4 — beta_status refleja historial por device
    beta = th.beta_status()
    assert "deviceA" in beta["devices"] or "deviceB" in beta["devices"]
    print(f"\nT4 OK — beta_status: {beta}")

    # T5 — Δ_r de Monitor y Δ_r_compresiones de COCO: objetos distintos
    d_monitor  = monitor2._Delta_r.sum()
    d_thermo   = th.delta_state().sum()
    print(f"\nT5 Delta — monitor={d_monitor:.4f}  thermostat={d_thermo:.4f}")
    print(f"   divergen={'SI' if abs(d_monitor - d_thermo) > 1e-6 else 'NO (ambos en 0)'}")

    # T6 — stop_signal independiente del thermostat
    sig = monitor2.stop_signal()
    assert "signal" in sig and "direction" in sig, "FAIL T6"
    print(f"\nT6 OK — stop_signal: {sig}")

    os.unlink(tmp_corpus)
    os.unlink(tmp_monitor)
    print("\nTodos los tests OK")
