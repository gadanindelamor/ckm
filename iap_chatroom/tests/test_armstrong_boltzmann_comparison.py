"""
test_armstrong_boltzmann_comparison.py

Corre el experimento Armstrong con los tres modos de muestreo de sigma_0
disponibles en COCO (uniform / weighted / boltzmann), mas un baseline sin
thermostat. n_runs=200 fijo en TODAS las corridas — condicion controlada.

Spec: TASK_armstrong_boltzmann_comparison_v1.md.

NO modifica test_armstrong_stop_coco.py: lo importa y reusa WARMUP_TEXTS y
TEXTS. Mismo patron que test_armstrong_n_runs_sweep.py — estado aislado por
corrida, sin contaminacion entre modos.

Dos n_runs, los dos en 200 (decision de delamor, Ago 2026):
  - COCO._n_runs                     -> D_ckm que decide STOP
  - MonitorService._n_runs_attractors -> D_ckm del panel
Son contadores INDEPENDIENTES con implementaciones distintas: el de
MonitorService (monitor_service.py:276) tiene default_rng(0) hardcodeado, no
acepta modos, y normaliza con _combine_W_Delta. Por eso se registran los dos
D_ckm por evaluacion y su diferencia — la divergencia entre instrumentos
queda trazada, no promediada.

"Mismo seed" NO implica "mismos sigma_0" entre modos: el calentamiento
Boltzmann consume tiradas extra del RNG, asi que la secuencia de estados
iniciales diverge desde el primer run. La comparacion no es pareada.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "services"))

from coco import COCO                      # noqa: E402
from corpus_service import CorpusService   # noqa: E402
from monitor_service import MonitorService # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "armstrong_orig", _REPO_ROOT / "iap_chatroom/tests/test_armstrong_stop_coco.py"
)
orig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orig)

OUT_DIR  = _REPO_ROOT / "process/experiments/boltzmann_comparison"
N_RUNS   = 200
SEED     = 42
MIN_TEXTS = 15


def run_condition(label: str, sampling_mode: str | None) -> dict:
    """
    Una corrida Armstrong completa bajo una condicion.

    sampling_mode=None -> baseline: MonitorService SIN thermostat. Ese caso
    no es "COCO en modo uniforme": es la otra implementacion de
    _count_attractors, con su propio RNG y su propio A0.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus_path = OUT_DIR / f"corpus_{label}.json"
    traj_path   = OUT_DIR / f"trajectory_{label}.jsonl"
    for p in (corpus_path, traj_path):
        p.unlink(missing_ok=True)   # estado aislado — no reingestar corpus previo

    corpus = CorpusService(storage_path=str(corpus_path), min_texts=MIN_TEXTS)
    corpus.ingest(orig.WARMUP_TEXTS)
    assert corpus.mode == "evaluation", f"{label}: corpus en modo {corpus.mode}"
    W = corpus.get_W()

    th = None
    if sampling_mode is not None:
        th = COCO(
            W               = W,
            n_runs          = N_RUNS,
            seed            = SEED,
            track_landscape = True,
            sampling_mode   = sampling_mode,
        )

    monitor = MonitorService(
        corpus,
        storage_path      = str(traj_path),
        n_runs_attractors = N_RUNS,
        thermostat        = th,
    )

    evals, stops = [], []
    for i, text in enumerate(orig.TEXTS):
        panel = monitor.evaluate(text, device_id=f"cmp_{i:02d}")
        t = panel.get("thermostat")
        hist = th.history()[-1] if th is not None and th.history() else None

        rec = {
            "i"            : i,
            "D_ckm_panel"  : panel["D_ckm"],
            "D_ckm_coco"   : t["D_ckm"] if t else None,
            "delta_D_ckm"  : (round(t["D_ckm"] - panel["D_ckm"], 4) if t else None),
            "A_actual"     : hist.A_current if hist else None,
            "A0"           : hist.A0 if hist else None,
            "frac_rec"     : t["frac_rec"] if t else None,
            "zone"         : t["zone"] if t else None,
            "stop_applied" : bool(t["stop_applied"]) if t else False,
            "alpha_used"   : t["alpha_used"] if t else None,
            "sampling_mode": t["sampling_mode"] if t else None,
            "n_warmup"     : t["n_warmup"] if t else None,
            "Delta_r_sum"  : panel["Delta_r_sum"],
            "c_S"          : panel["c_S"],
            "delta_A"      : (t["landscape_delta"] or {}).get("delta_A") if t else None,
        }
        evals.append(rec)
        if rec["stop_applied"]:
            stops.append(rec)

    return {
        "label"          : label,
        "sampling_mode"  : sampling_mode if sampling_mode else "sin_thermostat",
        "n_runs_coco"    : N_RUNS if th else None,
        "n_runs_monitor" : N_RUNS,
        "seed"           : SEED,
        "N"              : int(W.shape[0]),
        "n_warmup"       : (th._n_warmup if th and sampling_mode == "boltzmann" else None),
        "beta_c_corpus"  : round(th.beta_c_corpus(), 4) if th else None,
        "n_stops"        : len(stops),
        "n_evals"        : len(evals),
        "evals"          : evals,
    }


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    conditions = [
        ("uniform",         "uniform"),
        ("weighted",        "weighted"),
        ("boltzmann",       "boltzmann"),
        ("sin_thermostat",  None),
    ]
    results = []
    for label, mode in conditions:
        print(f"--- {label} (n_runs={N_RUNS}, seed={SEED}) ...", flush=True)
        r = run_condition(label, mode)
        results.append(r)
        print(f"    STOPs={r['n_stops']}/{r['n_evals']}  "
              f"A0={r['evals'][0]['A0']}  sampling_mode={r['evals'][0]['sampling_mode']}",
              flush=True)

    out = OUT_DIR / f"comparison_{ts}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResultados: {out}")

    print(f"\n{'condicion':<16} {'STOPs':>6} {'A0':>5} {'A_fin':>6} "
          f"{'D_ckm_coco_fin':>15} {'D_ckm_panel_fin':>16}")
    for r in results:
        e = r["evals"][-1]
        print(f"{r['label']:<16} {r['n_stops']:>6} {str(e['A0']):>5} "
              f"{str(e['A_actual']):>6} {str(e['D_ckm_coco']):>15} {str(e['D_ckm_panel']):>16}")


if __name__ == "__main__":
    main()
