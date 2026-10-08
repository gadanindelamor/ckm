"""
cp1_paridad_y_dos_existencias.py — CP1 de TASK_monitor_coco_ciclo_orbita_v2

**ESTO MIDE.** No es una reconstrucción de nada: no hay resultado previo al que
llegar. Driver nuevo, escrito para este CP1.

No toca `services/`: importa de ahí y mide. No escribe en el repo fuera de su
propio log, con escritura atómica (`.tmp` y después rename).

===========================================================================
PRE-REGISTRO — escrito antes de correr, 2026-10-08
===========================================================================

Dos cosas se miden, las dos de la §0 de la TASK.

--- A. PARIDAD -------------------------------------------------------------

`MonitorService._relax` devuelve `relax_orbit(...)[3]`: la fase que cae en
`max_iter`, elegida por `(max_iter − cola) mod periodo`. Con periodo 2, cambiar
`max_iter` de 200 a 201 cambia de fase. De ese estado salen `_rejected_pairs`,
`Δ_r_pares`, `c_S` y `fabrication_index`.

Se recorre el corpus texto por texto, como lo hace Monitor, y por cada texto se
calculan las DOS fases desde el mismo σ_prompt y la misma W_eff:

    R_A = pares expulsados con max_iter = 200
    R_B = pares expulsados con max_iter = 201

y se registra: periodo de la órbita, cola, |R_A|, |R_B|, |R_A △ R_B|,
c(S) de cada fase, y el fabrication_index de cada fase.

Δ_r se acumula por separado en dos matrices —una por paridad— arrastrando cada
una su propia historia, porque Δ_r entra a W_eff y por lo tanto la divergencia
se compone a lo largo del recorrido. Al final se reporta
‖Δ_r^A − Δ_r^B‖₁ y la diferencia máxima celda a celda.

**UMBRAL DECLARADO, y el test puede fallar.** La paridad "pesa" si alguna de
las tres se cumple:

    (U1) algún texto tiene |R_A △ R_B| > 0;
    (U2) ‖Δ_r^A − Δ_r^B‖₁ > 0 al final del recorrido;
    (U3) alguna |c(S)_A − c(S)_B| > 1e-9.

Si ninguna se cumple, la respuesta es **"la paridad no pesa en este corpus"**,
y se registra así. Es un resultado, no un fracaso.

**Expectativa declarada (Opus, antes de correr).** El docstring de
`MonitorService._relax` dice que en WARMUP_TEXTS 141 de 200 runs llegan a punto
fijo, y la §0 de la TASK dice que en caso09_run2 natural 136 de 200 terminan en
periodo 2. Pero esos números son del muestreo de σ₀ de `count_attractors`, NO
de la relajación de σ_prompt, que es un solo punto de partida por texto y está
determinado por el texto. **Así que espero pocos textos con periodo 2, y es
posible que ninguno.** Si ninguno, U1–U3 dan todas negativas y el CP1 cierra
con "no pesa", que es una respuesta sobre σ_prompt y no contradice lo
registrado sobre σ₀.

--- B. DOS EXISTENCIAS -----------------------------------------------------

`CorpusService._rebuild()` crea un COCO nuevo; `MonitorService` se queda con el
que recibió. Se reproduce el patrón real: se lee `corpus.coco` UNA vez, se lo
pasa como `thermostat`, y después se ingesta de a un texto para forzar
rebuilds.

Se registra por evaluación: `id()` de `corpus.coco`, `id()` de
`monitor._thermostat`, si son el mismo objeto, el `w_version_id` de cada uno,
el `Delta_r_reset` del panel, y el `Δ_r_compresiones` de COCO.

**Lo que se busca:** los incrementos negativos de `Δ_r_compresiones`.
`TASK_delta_compresiones_coco_v1` §Abierto registra 56 con W de 8 nodos, α=0.1 y
un reset de Monitor. Acá el corpus es otro, así que **el número no tiene por
qué ser 56**: lo que se mide es si aparecen, cuántos y con qué signo.
Un incremento negativo significa que la serie acumulada de COCO decreció, y una
serie de compresiones acumuladas no puede decrecer si el campo es uno.

**UMBRAL DECLARADO:** "las dos existencias divergen" si
`son_el_mismo_objeto == False` en alguna evaluación **o** si hay al menos un
incremento negativo. Si los dos salen negativos, se registra que no divergen en
este corpus.

--- Lo que este driver NO hace ---------------------------------------------

- No cambia nada de `services/`. Monitor y COCO se usan como están.
- No mide la torsión por pares aceptado/expulsado/torsión: eso es el CP2.
- No decide qué entra a Δ_r: eso es el CP3, y es de delamor.
- No corre `coco_lifetime_analytics.py`; reusa su patrón de construcción (A/F).

Uso:
    python experiments/cp1_paridad_y_dos_existencias.py [salida.json]
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))

from coco import COCO                                    # noqa: E402
from corpus_service import CorpusService                 # noqa: E402
from landscape_engine import relax_orbit                 # noqa: E402
from monitor_service import MonitorService               # noqa: E402
from node_extractor import NodeExtractorService          # noqa: E402

CASO09 = RAIZ / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"
WARMUP = RAIZ / "iap_chatroom/tests/test_armstrong_stop_coco.py"

MAX_ITER_A = 200
MAX_ITER_B = 201
SEED = 0
N_RUNS = 50          # bajo a propósito: acá no se mide N_eff, se mide paridad
UMBRAL_CS = 1e-9


# ── corpus ──────────────────────────────────────────────────────────────────

def textos_caso09() -> list[str]:
    return json.loads(CASO09.read_text())["texts"]


def textos_warmup() -> list[str]:
    """WARMUP_TEXTS se lee del archivo donde está definido, sin importar el
    módulo: importarlo arrastra el server del canal."""
    src = WARMUP.read_text()
    i = src.index("WARMUP_TEXTS = [")
    j = src.index("]", i)
    return [l.strip().rstrip(",").strip('"')
            for l in src[i + len("WARMUP_TEXTS = ["):j].strip().splitlines()
            if l.strip()]


# ── A. paridad ──────────────────────────────────────────────────────────────

def _rejected_pairs(sigma_p: np.ndarray, sigma_r: np.ndarray) -> set:
    """Misma operación que MonitorService._rejected_pairs, como set."""
    declared = np.where(sigma_p > 0)[0]
    rechazados = set(np.where(sigma_r < 0)[0])
    out = set()
    for a in range(len(declared)):
        for b in range(a + 1, len(declared)):
            i, j = declared[a], declared[b]
            if i in rechazados or j in rechazados:
                out.add((int(i), int(j)))
    return out


def _cS(sigma: np.ndarray, W: np.ndarray) -> float:
    ii, jj = np.triu_indices(len(sigma), k=1)
    return float(np.mean(W[ii, jj] * sigma[ii] * sigma[jj]))


def _combine(W: np.ndarray, Delta: np.ndarray) -> np.ndarray:
    """Misma normalización que MonitorService._combine_W_Delta."""
    if Delta is None or not Delta.any():
        return W
    pos = W[W > 0]
    escala = float(pos.mean()) if len(pos) else 1.0
    return W + (Delta / Delta.max()) * escala


def medir_paridad(textos: list[str], nombre: str) -> dict:
    corpus_tmp = RAIZ / f".cp1_corpus_{nombre}.json"
    try:
        c = CorpusService(storage_path=str(corpus_tmp), min_texts=len(textos),
                          top_k=32, rebuild_suspendido=True)
        c.ingest(textos)
        W = c.get_W()
        if W is None:
            return {"corpus": nombre, "error": "W es None: el corpus no distingue"}
        nodos = c.get_nodes()
        N = len(nodos)
        ex = NodeExtractorService()

        dA = np.zeros((N, N))
        dB = np.zeros((N, N))
        por_texto = []

        for k, texto in enumerate(textos):
            sp = ex.evaluate(texto, nodos)
            WeA, WeB = _combine(W, dA), _combine(W, dB)

            orbA = relax_orbit(sp.copy(), WeA, MAX_ITER_A)
            orbB = relax_orbit(sp.copy(), WeB, MAX_ITER_B)
            sA, sB = orbA[3], orbB[3]

            RA = _rejected_pairs(sp, sA)
            RB = _rejected_pairs(sp, sB)
            for i, j in RA:
                dA[i, j] += 1; dA[j, i] += 1
            for i, j in RB:
                dB[i, j] += 1; dB[j, i] += 1

            cA, cB = _cS(sA, WeA), _cS(sB, WeB)
            por_texto.append({
                "i": k,
                "declarados": int((sp > 0).sum()),
                "periodo_A": orbA[1], "cola_A": orbA[2],
                "periodo_B": orbB[1], "cola_B": orbB[2],
                "n_RA": len(RA), "n_RB": len(RB),
                "n_simetrica": len(RA ^ RB),
                "pares_simetrica": sorted(RA ^ RB),
                "cS_A": cA, "cS_B": cB, "d_cS": cA - cB,
                "estados_iguales": bool(np.array_equal(sA, sB)),
            })

        dif = np.abs(dA - dB)
        max_d_cS = max(abs(t["d_cS"]) for t in por_texto) if por_texto else 0.0
        U1 = any(t["n_simetrica"] > 0 for t in por_texto)
        U2 = float(dif.sum()) > 0
        U3 = max_d_cS > UMBRAL_CS

        return {
            "corpus": nombre, "N": N, "n_textos": len(textos),
            "nodos": nodos,
            "textos_con_periodo_2_A": sum(1 for t in por_texto if t["periodo_A"] == 2),
            "textos_con_periodo_2_B": sum(1 for t in por_texto if t["periodo_B"] == 2),
            "textos_con_estados_distintos": sum(1 for t in por_texto
                                                if not t["estados_iguales"]),
            "L1_Delta_r_A_menos_B": float(dif.sum()),
            "max_celda_Delta_r": float(dif.max()),
            "max_abs_d_cS": max_d_cS,
            "U1_alguna_simetrica": U1,
            "U2_Delta_r_difiere": U2,
            "U3_cS_difiere": U3,
            "LA_PARIDAD_PESA": bool(U1 or U2 or U3),
            "por_texto": por_texto,
        }
    finally:
        corpus_tmp.unlink(missing_ok=True)


# ── B. dos existencias ──────────────────────────────────────────────────────

def medir_dos_existencias(textos: list[str]) -> dict:
    """
    Patrón real: se lee corpus.coco UNA vez y se lo pasa como thermostat.
    Después se ingesta de a un texto, que con rebuild_suspendido=False
    reconstruye W en cada ingest y hace que Corpus cree un COCO nuevo.
    """
    corpus_tmp = RAIZ / ".cp1_corpus_dos.json"
    traj_tmp   = RAIZ / ".cp1_traj.jsonl"
    try:
        corte = max(5, len(textos) // 3)
        c = CorpusService(storage_path=str(corpus_tmp), min_texts=5, top_k=32)
        c.ingest(textos[:corte])
        if c.get_W() is None:
            return {"error": "W es None tras la ingesta inicial"}

        th = c.coco                      # se lee UNA vez, como el patrón real
        if th is None:
            return {"error": "corpus.coco es None"}
        m = MonitorService(c, storage_path=str(traj_tmp),
                           n_runs_attractors=N_RUNS, thermostat=th)

        filas = []
        for k, texto in enumerate(textos[corte:]):
            c.ingest([texto])
            panel = m.evaluate(texto)
            if panel is None or panel.get("mode") == "accumulation":
                continue
            comp = list(th._Delta_r_compresiones) if hasattr(th, "_Delta_r_compresiones") else []
            filas.append({
                "i": k,
                "id_corpus_coco": id(c.coco),
                "id_monitor_thermostat": id(m._thermostat),
                "son_el_mismo_objeto": c.coco is m._thermostat,
                "w_sha_corpus": c.w_sha()[:12] if c.w_sha() else None,
                "Delta_r_reset": panel.get("Delta_r_reset"),
                "n_compresiones": len(comp),
                "ultima_compresion": comp[-1] if comp else None,
            })

        serie = [f["n_compresiones"] for f in filas]
        incs = [serie[i] - serie[i - 1] for i in range(1, len(serie))]
        negativos = [i for i in incs if i < 0]

        # la serie acumulada de COCO, celda a celda
        acum = []
        if hasattr(th, "_Delta_r_compresiones"):
            acum = [float(np.sum(x)) if isinstance(x, np.ndarray) else x
                    for x in th._Delta_r_compresiones]
        inc_acum = [acum[i] - acum[i - 1] for i in range(1, len(acum))]
        neg_acum = [x for x in inc_acum if x < 0]

        mismo_siempre = all(f["son_el_mismo_objeto"] for f in filas)
        return {
            "n_evaluaciones": len(filas),
            "ids_distintos_de_corpus_coco": len({f["id_corpus_coco"] for f in filas}),
            "son_el_mismo_objeto_siempre": mismo_siempre,
            "resets_de_monitor": [f["Delta_r_reset"] for f in filas],
            "n_resets": sum(1 for f in filas if f["Delta_r_reset"] is not None),
            "serie_n_compresiones": serie,
            "incrementos_negativos_en_conteo": len(negativos),
            "serie_suma_compresiones": acum,
            "incrementos_negativos_en_suma": len(neg_acum),
            "valores_negativos": neg_acum[:10],
            "LAS_DOS_EXISTENCIAS_DIVERGEN": bool(not mismo_siempre or neg_acum),
            "por_evaluacion": filas,
        }
    finally:
        corpus_tmp.unlink(missing_ok=True)
        traj_tmp.unlink(missing_ok=True)


# ── main ────────────────────────────────────────────────────────────────────

def main() -> None:
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "experiments/cp1_paridad_log.json"
    t0 = time.time()
    sha = subprocess.run(["git", "-C", str(RAIZ), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()

    res = {
        "que_es": "ESTO MIDE — CP1 de TASK_monitor_coco_ciclo_orbita_v2",
        "repo_commit": sha,
        "seed": SEED,
        "max_iter_A": MAX_ITER_A,
        "max_iter_B": MAX_ITER_B,
        "n_runs_attractors": N_RUNS,
        "umbral_cS": UMBRAL_CS,
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "donde": "Codespace ckm",
        "variables_no_consideradas": "todas las que no están en este log",
    }

    res["A_paridad"] = {}
    for nombre, textos in (("caso09_run2_natural", textos_caso09()),
                           ("WARMUP_TEXTS", textos_warmup())):
        print(f"[A] paridad · {nombre} · {len(textos)} textos", flush=True)
        res["A_paridad"][nombre] = medir_paridad(textos, nombre)
        r = res["A_paridad"][nombre]
        print(f"    pesa={r.get('LA_PARIDAD_PESA')} · "
              f"periodo2_A={r.get('textos_con_periodo_2_A')} · "
              f"L1={r.get('L1_Delta_r_A_menos_B')}", flush=True)

    print("[B] dos existencias · caso09_run2_natural", flush=True)
    res["B_dos_existencias"] = medir_dos_existencias(textos_caso09())
    b = res["B_dos_existencias"]
    print(f"    divergen={b.get('LAS_DOS_EXISTENCIAS_DIVERGEN')} · "
          f"mismo_objeto_siempre={b.get('son_el_mismo_objeto_siempre')} · "
          f"neg={b.get('incrementos_negativos_en_suma')}", flush=True)

    res["segundos"] = round(time.time() - t0, 1)

    tmp = salida.with_suffix(salida.suffix + ".tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    tmp.replace(salida)
    print(f"\nlog → {salida}")


if __name__ == "__main__":
    main()
