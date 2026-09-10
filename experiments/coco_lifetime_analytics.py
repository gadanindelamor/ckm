"""
coco_lifetime_analytics.py — Vida de las instancias de COCO y W congelada

Driver que REGENERA todas las mediciones citadas en
registers/REG_coco_w_congelada_v1.md.

Motivo de existir: el hallazgo se produjo leyendo codigo en una conversacion.
Sin driver, el REG seria una afirmacion sobre el codigo, no evidencia. Este
archivo permite volver a correr cada numero. Mismo criterio que
orbit_analytics.py.

Secciones:
    A  identidad de instancias — corpus.coco vs monitor._thermostat en el tiempo
    B  W congelada vs W actual — divergencia acumulada por ingesta
    C  beta — que acumula y que se reinicia, en cada instancia
    D  los dos D_ckm sobre la misma evaluacion
    E  censo de variantes de rutinas duplicadas (AST, sin docstrings)
    F  quien inyecta thermostat — alcance real del hallazgo

Uso:
    python experiments/coco_lifetime_analytics.py
    python experiments/coco_lifetime_analytics.py --seccion B

Salida: process/experiments/coco_lifetime/<seccion>_<timestamp>.json
No pisa corridas anteriores.

Reproducibilidad: rutas resueltas desde __file__. Storage siempre temporal.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))

from corpus_service import CorpusService          # noqa: E402
from monitor_service import MonitorService        # noqa: E402
from coco import COCO                             # noqa: E402

SALIDA = RAIZ / "process" / "experiments" / "coco_lifetime"


# ── corpus de prueba ─────────────────────────────────────────────────────────

CASO09 = RAIZ / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"

# Corpus de respaldo — sintetico, sin marcadores de oposicion fuertes.
# Sirve para verificar el mecanismo; NO produce Delta_r suficiente para que
# D_ckm de COCO se mueva. Se usa solo si el corpus de caso09 no esta.
TEXTOS_SINTETICOS = [
    "la cohesion estructural del campo de conocimiento compartido",
    "atractores multiples y volumen de cuenca en el espacio de estados",
    "la relajacion sincrona converge siempre a un conjunto invariante",
    "sin embargo el conteo de estados terminales no mide la diversidad",
    "la frustracion topologica depende solo de los signos de los pesos",
    "el espectro de una matriz simetrica es real y esta ordenado",
    "la masa de cuenca es una probabilidad y no un conteo de resultados",
    "el corpus crece y la matriz se reconstruye en cada ingesta nueva",
    "no obstante la oposicion estructural introduce pesos negativos",
    "la traza registra el sha de cada version distinta del campo",
    "un punto fijo es una orbita degenerada de un solo elemento",
    "el principio de invariancia de lasalle no elige que se debe contar",
]


def _textos() -> tuple[list[str], str]:
    """Corpus de trabajo. caso09_run2 (regimen natural, 24 textos, con
    oposicion real) si esta disponible — es el mismo que citan
    REG_wmixta_natural_paso2_v1 y TASK_monitor_service_unificar_rutinas_v1,
    asi que las mediciones quedan comparables. Sintetico si no."""
    if CASO09.exists():
        return json.loads(CASO09.read_text())["texts"], CASO09.name
    return TEXTOS_SINTETICOS, "sinteticos (caso09 ausente)"


TEXTOS, FUENTE_TEXTOS = _textos()


def _usar_sinteticos() -> None:
    """Fuerza el corpus sintetico. Con el, N ya satura en top_k desde la
    tercera ingesta y los shapes calzan siempre: muestra la divergencia
    SILENCIOSA. Con caso09, N crece y muestra la EXCEPCION. Los dos
    desenlaces del mismo defecto."""
    global TEXTOS, FUENTE_TEXTOS
    TEXTOS, FUENTE_TEXTOS = TEXTOS_SINTETICOS, "sinteticos (forzado)"


def _corpus_monitor(n_iniciales: int = 3):
    """Corpus con n_iniciales textos ya ingestados, monitor con COCO inyectado.

    Reproduce el patron real de construccion: se lee corpus.coco UNA vez y se
    pasa al constructor de MonitorService (asi lo hacen los tests del repo).
    """
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"), min_texts=3)
    c.ingest(TEXTOS[:n_iniciales])
    th = c.coco
    m = MonitorService(c, storage_path=tempfile.mktemp(suffix=".jsonl"),
                       n_runs_attractors=30, thermostat=th)
    return c, m, th


# ── A — identidad de instancias ──────────────────────────────────────────────

def seccion_A() -> dict:
    c, m, th_inicial = _corpus_monitor()
    id_inicial = id(th_inicial)
    filas = []
    for k, t in enumerate(TEXTOS[3:], start=4):
        c.ingest([t])
        filas.append({
            "n_textos": len(c._texts),
            "id_corpus_coco": id(c.coco),
            "id_monitor_thermostat": id(m._thermostat),
            "son_el_mismo_objeto": c.coco is m._thermostat,
            "monitor_sigue_con_el_inicial": id(m._thermostat) == id_inicial,
        })
    return {
        "corpus": FUENTE_TEXTOS,
        "id_inicial": id_inicial,
        "ingestas": filas,
        "corpus_coco_cambio_de_objeto": len({f["id_corpus_coco"] for f in filas}),
        "monitor_thermostat_cambio_de_objeto": len({f["id_monitor_thermostat"] for f in filas}),
        "veces_que_coincidieron": sum(f["son_el_mismo_objeto"] for f in filas),
        "total_ingestas": len(filas),
    }


# ── B — W congelada vs W actual ──────────────────────────────────────────────

def seccion_B() -> dict:
    c, m, th = _corpus_monitor()
    W_construccion = th.W.copy()
    N_construccion = th.N
    filas = []
    for t in TEXTOS[3:]:
        c.ingest([t])
        W_actual = c.get_W()
        misma_forma = W_actual.shape == W_construccion.shape
        d = float(np.abs(W_actual - W_construccion).max()) if misma_forma else None
        rel = None
        if misma_forma and np.abs(W_construccion).max() > 0:
            rel = float(d / np.abs(W_construccion).max())
        filas.append({
            "n_textos": len(c._texts),
            "N_actual": W_actual.shape[0],
            "N_de_COCO": N_construccion,
            "misma_forma": misma_forma,
            "max_abs_dif": None if d is None else round(d, 6),
            "dif_relativa": None if rel is None else round(rel, 4),
            "sha_W_actual": hashlib.sha256(W_actual.tobytes()).hexdigest()[:10],
        })
    # mu_W y beta_c: derivan de W. Congelada W, congelados los dos.
    # mu_W con la MISMA definicion que COCO.beta_c_corpus (coco.py:372-373):
    # media del triangulo superior INCLUYENDO ceros. No es la media de los
    # no-nulos ni de los valores absolutos — usar otra da un numero que no
    # se corresponde con el beta_c reportado.
    W_final = c.get_W()
    def mu(W):
        ii, jj = np.triu_indices(W.shape[0], k=1)
        return float(np.mean(W[ii, jj]))
    return {
        "corpus": FUENTE_TEXTOS,
        "N_de_COCO": N_construccion,
        "N_actual_estable_en": sorted({f["N_actual"] for f in filas}),
        "N_de_COCO_coincide_con_el_actual": all(
            f["N_actual"] == N_construccion for f in filas),
        "shapes_siempre_calzaron": all(f["misma_forma"] for f in filas),
        "ingestas": filas,
        "mu_W_de_COCO": round(mu(W_construccion), 8),
        "mu_W_actual": round(mu(W_final), 8),
        "beta_c_de_COCO": round(th.beta_c_corpus(), 6),
        "beta_c_si_fuese_actual": round(COCO(W=W_final).beta_c_corpus(), 6),
        "nota": ("si N crece despues de construir COCO, self.W + self._Delta "
                 "rompe con ValueError. Si N ya saturo en top_k, los shapes "
                 "calzan y la divergencia es silenciosa. Los dos desenlaces "
                 "dependen del corpus, no del codigo."),
    }


# ── C — beta: que acumula y que se reinicia ──────────────────────────────────

def seccion_C() -> dict:
    c, m, th = _corpus_monitor()
    filas = []
    for t in TEXTOS[3:]:
        c.ingest([t])
        try:
            m.evaluate(t, device_id="deviceA")
            excepcion = None
        except ValueError as e:
            # N crecio despues de construir COCO: self.W + self._Delta rompe.
            # Es el desenlace real, no un fallo del driver. Se registra.
            excepcion = f"{type(e).__name__}: {e}"
        regulador = m._thermostat
        fresco = c.coco
        if excepcion:
            filas.append({
                "n_textos": len(c._texts),
                "N_actual": len(c._nodes),
                "N_de_COCO": regulador.N,
                "excepcion": excepcion,
            })
            break
        filas.append({
            "n_textos": len(c._texts),
            "evals_en_el_regulador": len(regulador._rejections_per_device.get("deviceA", [])),
            "evals_en_corpus_coco": len(fresco._rejections_per_device.get("deviceA", [])),
            "beta_regulador": regulador.beta_i("deviceA"),
            "beta_corpus_coco": fresco.beta_i("deviceA"),
        })
    con_datos = [f for f in filas if "evals_en_el_regulador" in f]
    ult = con_datos[-1] if con_datos else {}
    corte = [f for f in filas if "excepcion" in f]
    return {
        "corte_por_excepcion": corte[0] if corte else None,
        "corpus": FUENTE_TEXTOS,
        "ingestas": filas,
        "hallazgo": (
            "Con N saturado: el que regula ACUMULA beta porque es el objeto "
            "viejo; corpus.coco, que tiene la W actual, nunca observa y su "
            "historia es 0 en todas las ingestas. Adoptar el fresco daria W "
            "actual y beta reiniciado. Con N creciendo: no llega a acumular "
            "nada, revienta en la primera evaluacion."
        ),
        "evals_acumuladas_regulador": ult.get("evals_en_el_regulador"),
        "evals_acumuladas_corpus_coco": ult.get("evals_en_corpus_coco"),
    }


# ── D — los dos D_ckm ────────────────────────────────────────────────────────

def seccion_D() -> dict:
    c, m, th = _corpus_monitor()
    filas = []
    excepcion = None
    for t in TEXTOS[3:]:
        c.ingest([t])
        try:
            p = m.evaluate(t, device_id="deviceA")
        except ValueError as e:
            excepcion = {"n_textos": len(c._texts), "N_actual": len(c._nodes),
                         "N_de_COCO": m._thermostat.N,
                         "excepcion": f"{type(e).__name__}: {e}"}
            break
        if not p:
            continue
        term = p.get("thermostat") or {}
        filas.append({
            "n_textos": len(c._texts),
            "D_ckm_monitor": p.get("D_ckm"),
            "D_ckm_coco": term.get("D_ckm"),
            "stop_applied": term.get("stop_applied"),
            "Delta_r_sum": p.get("Delta_r_sum"),
        })
    dm = [f["D_ckm_monitor"] for f in filas]
    dc = [f["D_ckm_coco"] for f in filas if f["D_ckm_coco"] is not None]
    return {
        "corpus": FUENTE_TEXTOS,
        "corte_por_excepcion": excepcion,
        "evaluaciones": filas,
        "D_ckm_monitor_valores_distintos": len(set(dm)),
        "D_ckm_coco_valores_distintos": len(set(dc)),
        "coinciden_alguna_vez": sum(
            1 for f in filas if f["D_ckm_monitor"] == f["D_ckm_coco"]),
        "n_stops": sum(1 for f in filas if f["stop_applied"]),
        "nota": ("D_ckm_monitor sale de _combine_W_Delta sobre la W ACTUAL; "
                 "D_ckm_coco sale de self.W + Delta sobre la W de construccion "
                 "(DEFS §10 documenta que el primero es ciego a STOP)"),
    }


# ── E — censo de variantes ───────────────────────────────────────────────────

ARCHIVOS_CENSO = [
    "process/experiments/coco_thermostat.py",
    "services/coco.py",
    "services/fabrication_service.py",
    "services/monitor_service.py",
    "experiments/monitor_service_dev.py",
    "experiments/monitor_service.py",
    "experiments/fabrication_service_dev.py",
    "experiments/orbit_analytics.py",
]


def _huella(path: Path, nombre: str):
    """AST de la funcion SIN docstring. Ni comentarios ni formato influyen."""
    try:
        arbol = ast.parse(path.read_text())
    except (OSError, SyntaxError):
        return None
    for n in ast.walk(arbol):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == nombre:
            cuerpo = list(n.body)
            if (cuerpo and isinstance(cuerpo[0], ast.Expr)
                    and isinstance(cuerpo[0].value, ast.Constant)
                    and isinstance(cuerpo[0].value.value, str)):
                cuerpo = cuerpo[1:]
            dump = ast.dump(ast.Module(body=cuerpo, type_ignores=[]))
            return (hashlib.sha256(dump.encode()).hexdigest()[:8],
                    n.end_lineno - n.lineno + 1)
    return None


def seccion_E() -> dict:
    out = {}
    for nombre in ("_relax", "_relax_orbit", "relax_orbit",
                   "_count_attractors", "_cS"):
        grupos: dict = {}
        for rel in ARCHIVOS_CENSO:
            r = _huella(RAIZ / rel, nombre)
            if r is None:
                continue
            h, n = r
            grupos.setdefault(h, []).append({"archivo": rel, "lineas": n})
        if grupos:
            out[nombre] = {
                "variantes": len(grupos),
                "archivos": sum(len(v) for v in grupos.values()),
                "grupos": grupos,
            }
    return out


# ── main ─────────────────────────────────────────────────────────────────────

def seccion_F() -> dict:
    """Quien construye MonitorService, y si le pasa thermostat.

    Por AST: se buscan las llamadas reales a MonitorService(...) y se mira
    si entre sus keywords esta `thermostat`. Un grep sobre "thermostat="
    no sirve — cae en docstrings, prints y lookups de dict.
    """
    def lineas_de_main(arbol) -> set:
        """Lineas que viven dentro de un `if __name__ == "__main__"`."""
        out = set()
        for n in ast.walk(arbol):
            if isinstance(n, ast.If) and isinstance(n.test, ast.Compare):
                izq = n.test.left
                if isinstance(izq, ast.Name) and izq.id == "__name__":
                    for hijo in ast.walk(n):
                        if hasattr(hijo, "lineno"):
                            out.add(hijo.lineno)
        return out

    filas = []
    for f in sorted(RAIZ.rglob("*.py")):
        if ".git" in f.parts:
            continue
        try:
            arbol = ast.parse(f.read_text())
        except (OSError, SyntaxError):
            continue
        for n in ast.walk(arbol):
            if not isinstance(n, ast.Call):
                continue
            fn = n.func
            nombre = getattr(fn, "id", None) or getattr(fn, "attr", None)
            if nombre != "MonitorService":
                continue
            kw = [k.arg for k in n.keywords if k.arg]
            filas.append({
                "archivo": str(f.relative_to(RAIZ)),
                "linea": n.lineno,
                "en_main_del_modulo": n.lineno in lineas_de_main(arbol),
                "pasa_thermostat": "thermostat" in kw,
                "keywords": kw,
            })
    def es_produccion(a: str) -> bool:
        return not (a.startswith(("tests/", "experiments/", "process/"))
                    or "/tests/" in a or a.endswith("_dev.py"))
    prod = [f for f in filas
            if es_produccion(f["archivo"]) and not f["en_main_del_modulo"]]
    return {
        "construcciones": filas,
        "total": len(filas),
        "con_thermostat": sum(f["pasa_thermostat"] for f in filas),
        "en_produccion": prod,
        "produccion_con_thermostat": sum(f["pasa_thermostat"] for f in prod),
        "hallazgo": ("la unica construccion de produccion es "
                     "iap_chatroom/ckm_monitor.py y NO pasa thermostat: en el "
                     "canal vivo COCO nunca regula, panel['thermostat'] es "
                     "None siempre. El defecto de W congelada es alcanzable "
                     "solo desde tests y drivers."),
    }


SECCIONES = {"A": seccion_A, "B": seccion_B, "C": seccion_C,
             "D": seccion_D, "E": seccion_E, "F": seccion_F}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seccion", choices=sorted(SECCIONES), default=None)
    ap.add_argument("--sinteticos", action="store_true",
                    help="fuerza el corpus sintetico (N saturado): muestra la "
                         "divergencia silenciosa en vez de la excepcion")
    args = ap.parse_args()
    if args.sinteticos:
        _usar_sinteticos()

    SALIDA.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cuales = [args.seccion] if args.seccion else sorted(SECCIONES)

    for s in cuales:
        print(f"\n{'='*70}\nSECCION {s}\n{'='*70}")
        r = SECCIONES[s]()
        print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        p = SALIDA / f"{s}_{ts}.json"
        p.write_text(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        print(f"\n-> {p.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
