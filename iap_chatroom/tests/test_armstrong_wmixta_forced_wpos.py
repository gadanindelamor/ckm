"""
test_armstrong_wmixta_forced_wpos.py

Verificacion de comportamiento del instrumento sobre un corpus CON tension
estructural: los 24 textos del caso IAP 09_run2. SOLO se toma el texto de
ese caso — ni su Delta_r, ni su W, ni su historia.

Dos regimenes de W sobre el MISMO corpus y la MISMA secuencia:
  - natural : CorpusService rutea por marcadores -> W con pesos negativos
  - forzado : force_w_pos=True saltea el ruteo    -> W = (pos+neg)/max

El regimen forzado NO es alcanzable por el ciclo natural de servicios. No es
una comparacion entre dos estados del campo: es verificacion del instrumento.
La W forzada queda marcada en la traza (causal_event=rebuild_debug_force_w_pos,
forced_w_pos=True en el estado persistido).

Cuatro condiciones de muestreo por regimen: uniform / weighted / boltzmann /
sin thermostat. n_runs=200 en los DOS contadores. track_landscape=True.
Estado aislado por condicion.

Spec: TASK_armstrong_boltzmann_comparison_wmixta_v1.md, reformulada tras
verificar que el corpus Armstrong (WARMUP_TEXTS) no admite W_mixta —
0 marcadores de oposicion en sus 40 textos.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "services"))

from coco import COCO                       # noqa: E402
from corpus_service import CorpusService    # noqa: E402
from monitor_service import MonitorService  # noqa: E402

CASO    = _REPO_ROOT / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"
OUT_DIR = _REPO_ROOT / "process/experiments/wmixta_forced_wpos"
N_RUNS  = 200
SEED    = 42


def run_condition(regimen: str, force_w_pos: bool, label: str, mode: str | None) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = f"{regimen}_{label}"
    corpus_path = OUT_DIR / f"corpus_{tag}.json"
    traj_path   = OUT_DIR / f"trajectory_{tag}.jsonl"
    for p in (corpus_path, traj_path):
        p.unlink(missing_ok=True)

    textos = json.loads(CASO.read_text())["texts"]
    corpus = CorpusService(storage_path=str(corpus_path), min_texts=3,
                           force_w_pos=force_w_pos)
    corpus.ingest(textos)
    assert corpus.mode == "evaluation", f"{tag}: modo {corpus.mode}"
    W = corpus.get_W()

    th = None
    if mode is not None:
        th = COCO(W=W, n_runs=N_RUNS, seed=SEED, track_landscape=True,
                  sampling_mode=mode)

    monitor = MonitorService(corpus, storage_path=str(traj_path),
                             n_runs_attractors=N_RUNS, thermostat=th)

    evals = []
    for i, text in enumerate(textos):
        panel = monitor.evaluate(text, device_id=f"c09_{i:02d}")
        t = panel.get("thermostat")
        hist = th.history()[-1] if th is not None and th.history() else None
        evals.append({
            "i": i,
            "D_ckm_panel" : panel["D_ckm"],
            "D_ckm_coco"  : t["D_ckm"] if t else None,
            "A_actual"    : hist.A_current if hist else None,
            "A0"          : hist.A0 if hist else None,
            "frac_rec"    : t["frac_rec"] if t else None,
            "zone"        : t["zone"] if t else None,
            "stop_applied": bool(t["stop_applied"]) if t else False,
            "alpha_used"  : t["alpha_used"] if t else None,
            "delta_A"     : (t["landscape_delta"] or {}).get("delta_A") if t else None,
            "Delta_r_sum" : panel["Delta_r_sum"],
            "c_S"         : panel["c_S"],
            "sampling_mode": t["sampling_mode"] if t else None,
        })

    return {
        "regimen"      : regimen,
        "force_w_pos"  : force_w_pos,
        "label"        : label,
        "sampling_mode": mode or "sin_thermostat",
        "N"            : int(W.shape[0]),
        "W_neg"        : int((W < 0).sum()),
        "W_pos"        : int((W > 0).sum()),
        "n_texts"      : len(textos),
        "n_stops"      : sum(1 for e in evals if e["stop_applied"]),
        "evals"        : evals,
    }


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    results = []
    for regimen, force in (("natural", False), ("forzado", True)):
        for label, mode in (("uniform", "uniform"), ("weighted", "weighted"),
                            ("boltzmann", "boltzmann"), ("sin_thermostat", None)):
            print(f"--- {regimen}/{label} ...", flush=True)
            r = run_condition(regimen, force, label, mode)
            results.append(r)
            e0 = r["evals"][0]
            print(f"    W<0={r['W_neg']:>3} STOPs={r['n_stops']:>2}/{r['n_texts']}  "
                  f"A0={e0['A0']}", flush=True)

    out = OUT_DIR / f"wmixta_forced_{ts}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResultados: {out}")
    print(f"\n{'regimen':<9} {'modo':<15} {'W<0':>4} {'STOPs':>6} {'A0':>5} "
          f"{'A_fin':>6} {'D_coco_fin':>11} {'D_panel_fin':>12}")
    for r in results:
        e = r["evals"][-1]
        print(f"{r['regimen']:<9} {r['label']:<15} {r['W_neg']:>4} "
              f"{r['n_stops']:>6} {str(e['A0']):>5} {str(e['A_actual']):>6} "
              f"{str(e['D_ckm_coco']):>11} {str(e['D_ckm_panel']):>12}")


if __name__ == "__main__":
    main()
