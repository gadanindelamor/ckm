"""
baseline_d_ckm.py — línea de base para la extracción de d_ckm al engine

Mismo proceso que TASK_monitor_service_unificar_rutinas_v1: la base se toma
ANTES de tocar los servicios, y el criterio es cero diferencias exactas, no
diferencias chicas. El script de la base anterior no quedó guardado; este sí.

No consulta `process/`: eso es pasado (delamor). El corpus va literal en
este archivo para que la base sea reproducible sin depender de nada de
afuera, y la W de COCO sale de `services/W_ckm_corpus_v2.json`.

Dos bloques:
  Monitor — ingesta incremental del corpus declarado abajo, régimen
            natural, n_runs_attractors=50. Por evaluación: D_ckm, c_S,
            fabrication_index, n_rejected_pairs, Delta_r_sum,
            activos_relajado, N_eff, D_masa_cuencas.
  COCO    — W_ckm_corpus_v2 + Delta sintética, 3 modos x 2 seeds. Por
            observe: D_ckm, A0, A_current, frac_rec, zone, alpha_used,
            stop_applied, y el TIPO de D_ckm (coco no tiene float()).

Dos bases guardadas (TASK_d_ckm_formula_canonica_v1):
  baseline_d_ckm.json          — forma lineal por conteo, la de la extracción.
                                 Se conserva; el código de hoy ya no la reproduce.
  baseline_d_ckm_canonica.json — forma canónica, 1 − ln N_eff / ln N_eff0,
                                 tomada el 5 oct 2026. D_ckm puede ser None
                                 (baseline ≤ 1, sin distancia que medir).

MonitorService escribe monitor_trajectory.jsonl en el directorio desde donde
se corre: correrlo desde la raíz del repo agrega líneas a ese archivo.

Uso:
    python experiments/baseline_d_ckm.py --salida experiments/baseline_d_ckm_canonica.json
    python experiments/baseline_d_ckm.py --comparar experiments/baseline_d_ckm_canonica.json
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))

W_V2   = REPO / "services/W_ckm_corpus_v2.json"

# Corpus declarado, no importado: 12 textos de debate con marcadores de
# oposicion, para que W quede mixta y el conteo tenga algo que contar.
TEXTOS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
    "bans reduce assault weapons and gun violence",
    "more guns mean more deaths but fewer guns mean fewer deaths",
    "criminals ignore gun laws however checks still stop some sales",
    "police response time matters more than weapons in the home",
    "the data on gun deaths is contested although trends are clear",
]
MODOS  = ("uniform", "weighted", "boltzmann")
SEEDS  = (0, 42)


def _monitor() -> list:
    from corpus_service import CorpusService
    from monitor_service import MonitorService
    textos = TEXTOS
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"), min_texts=3)
    m = MonitorService(corpus=c, n_runs_attractors=50)
    filas = []
    for i, t in enumerate(textos):
        c.ingest([t])
        if c.get_W() is None:
            continue
        p = m.evaluate(t, device_id="d1")
        filas.append({
            "i": i,
            "D_ckm": p["D_ckm"], "c_S": p["c_S"],
            "fabrication_index": p["fabrication_index"],
            "n_rejected_pairs": p["n_rejected_pairs"],
            "Delta_r_sum": p["Delta_r_sum"],
            "activos_relajado": p["activos_relajado"],
            "N_eff": p["N_eff"], "D_masa_cuencas": p["D_masa_cuencas"],
            "D_ckm_tipo": type(p["D_ckm"]).__name__,
        })
    return filas


def _coco() -> list:
    from coco import COCO
    W = np.array(json.loads(W_V2.read_text())["W"], dtype=float)
    N = W.shape[0]
    rng = np.random.default_rng(7)                 # Delta sintética fija
    D = np.zeros((N, N))
    ii, jj = np.triu_indices(N, 1)
    sel = rng.choice(len(ii), size=max(1, len(ii) // 10), replace=False)
    for k in sel:
        v = float(rng.uniform(0.1, 0.5))
        D[ii[k], jj[k]] = D[jj[k], ii[k]] = v
    filas = []
    for modo in MODOS:
        for seed in SEEDS:
            th = COCO(W=W, n_runs=50, seed=seed, sampling_mode=modo)
            s = th.observe(D)
            filas.append({
                "modo": modo, "seed": seed,
                "D_ckm": None if s.D_ckm is None else float(s.D_ckm), "A0": s.A0, "A_current": s.A_current,
                "frac_rec": float(s.frac_rec), "zone": s.zone,
                "alpha_used": float(s.alpha_used), "stop_applied": s.stop_applied,
                "D_ckm_tipo": type(s.D_ckm).__name__,
            })
    return filas


def tomar() -> dict:
    return {"monitor": _monitor(), "coco": _coco()}


def _igual(x, y) -> bool:
    """nan == nan cuenta como igual: el nan es parte de lo que la base
    capturo (monitor[3].c_S lo es hoy) y no se arregla cambiando el corpus."""
    import math
    if isinstance(x, float) and isinstance(y, float):
        if math.isnan(x) and math.isnan(y):
            return True
    return x == y


def comparar(base: dict, ahora: dict) -> int:
    difs = 0
    for bloque in ("monitor", "coco"):
        b, a = base[bloque], ahora[bloque]
        if len(b) != len(a):
            print(f"  {bloque}: CANTIDAD distinta {len(b)} vs {len(a)}")
            difs += 1
            continue
        for fb, fa in zip(b, a):
            for k in fb:
                if not _igual(fb[k], fa.get(k)):
                    print(f"  {bloque}[{fb.get('i', fb.get('modo'))}] {k}: "
                          f"{fb[k]!r} -> {fa.get(k)!r}")
                    difs += 1
    return difs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida")
    ap.add_argument("--comparar")
    a = ap.parse_args()
    if a.comparar:
        base = json.loads(Path(a.comparar).read_text())
        ahora = tomar()
        d = comparar(base, ahora)
        print(f"\n{'CERO diferencias' if d == 0 else str(d) + ' DIFERENCIAS'} "
              f"· monitor {len(ahora['monitor'])} evaluaciones · coco {len(ahora['coco'])} casos")
        return
    base = tomar()
    destino = Path(a.salida or "experiments/baseline_d_ckm.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(base, ensure_ascii=False, indent=1))
    print(f"monitor: {len(base['monitor'])} evaluaciones · coco: {len(base['coco'])} casos")
    print(f"tipos de D_ckm — monitor {base['monitor'][0]['D_ckm_tipo'] if base['monitor'] else '-'} "
          f"· coco {base['coco'][0]['D_ckm_tipo']}")
    print(f"-> {destino}")


if __name__ == "__main__":
    main()
