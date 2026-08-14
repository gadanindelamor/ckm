"""
test_armstrong_n_runs_sweep.py
Sweep de n_runs (única variable) sobre la réplica Armstrong seed=123,
vía CorpusService._rebuild() (mismo camino que
test_armstrong_via_corpus_v3.py).

Origen: TASK_armstrong_replica_seed123_via_corpus_v3 corrió con seed=123
y n_runs=80 (default, no especificado en el script de la task) y dio
20/20 STOPs — divergente del 3/20 esperado (réplica manual, n_runs=50).
Un test aislado (n_runs=50, mismo seed, mismo W) reprodujo 3/20 exacto.
Esta sweep traza la transición: para qué valores de n_runs el resultado
es 3/20, para cuáles 20/20, y dónde está el punto de quiebre.

Reporta además, por cada n_runs, cuántos STOPs tienen delta_A < 0 —
la Extensión 2 (TASK_coco_landscape_observation_v1) documentó "STOP
nunca pierde atractores" como hallazgo central; el run con n_runs=80
mostró 6/20 STOPs con delta_A negativo. Esta sweep verifica si eso es
específico de n_runs=80 o aparece en un rango más amplio.

Seed fijo en 123 — única variable es n_runs (misma disciplina que la
réplica seed=123 original: una variable por vez).

NO modifica: test_armstrong_stop_coco.py, test_armstrong_replica_seed123.py,
test_armstrong_via_corpus_v3.py, REGs existentes, coco.py, corpus_service.py.
Solo lectura + instanciación vía API pública ya existente.
"""
import json
import shutil
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "services"))

from corpus_service import CorpusService  # noqa: E402
from monitor_service import MonitorService  # noqa: E402
from coco import COCO  # noqa: E402

import importlib.util
spec = importlib.util.spec_from_file_location(
    "armstrong_orig",
    _REPO_ROOT / "iap_chatroom/tests/test_armstrong_stop_coco.py",
)
orig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orig)

SEED = 123
SWEEP_N_RUNS = [10, 20, 30, 40, 50, 60, 70, 80, 100, 150, 200]

OUT_DIR = _REPO_ROOT / "process/experiments/n_runs_sweep"


def run_one(n_runs: int) -> dict:
    """Corre Armstrong completo (WARMUP + TEXTS) con n_runs dado, seed=123.
    Estado aislado por n_runs — sin contaminación entre puntos de la sweep."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus_path = OUT_DIR / f"corpus_nruns_{n_runs}.json"
    output_path = OUT_DIR / f"trajectory_nruns_{n_runs}.jsonl"
    for p in (corpus_path, output_path):
        if p.exists():
            p.unlink()

    corpus = CorpusService(storage_path=str(corpus_path), min_texts=15)
    corpus.ingest(orig.WARMUP_TEXTS)
    assert corpus.mode == "evaluation", f"n_runs={n_runs}: mode={corpus.mode}"

    corpus._coco = COCO(W=corpus.get_W(), n_runs=n_runs, seed=SEED, track_landscape=True)

    monitor = MonitorService(
        corpus,
        storage_path=str(output_path),
        n_runs_attractors=50,
        thermostat=corpus.coco,
    )

    stops = []
    for i, text in enumerate(orig.TEXTS):
        panel = monitor.evaluate(text, device_id=f"test_{i:02d}")
        ts = panel.get("thermostat", {}) or {}
        if ts.get("stop_applied"):
            ld = ts.get("landscape_delta")
            stops.append({
                "t": i,
                "D_ckm": ts.get("D_ckm"),
                "alpha_used": ts.get("alpha_used"),
                "delta_A": ld["delta_A"] if ld else None,
                "delta_cS": ld["delta_cS"] if ld else None,
            })

    n_negative_delta_A = sum(1 for s in stops if s["delta_A"] is not None and s["delta_A"] < 0)
    last_D_ckm = None
    if len(orig.TEXTS) > 0:
        last_panel_ts = panel.get("thermostat", {}) or {}
        last_D_ckm = last_panel_ts.get("D_ckm")

    return {
        "n_runs": n_runs,
        "seed": SEED,
        "n_stops": len(stops),
        "n_negative_delta_A": n_negative_delta_A,
        "first_3_delta_A": [s["delta_A"] for s in stops[:3]],
        "D_ckm_tail": last_D_ckm,
        "stops": stops,
    }


def main():
    results = []
    print(f"Sweep n_runs {SWEEP_N_RUNS}, seed={SEED} fijo\n")
    print(f"{'n_runs':>7}  {'n_stops':>7}  {'neg_delta_A':>11}  {'D_ckm_tail':>10}")
    for n_runs in SWEEP_N_RUNS:
        r = run_one(n_runs)
        results.append(r)
        print(f"{n_runs:>7}  {r['n_stops']:>7}  {r['n_negative_delta_A']:>11}  "
              f"{r['D_ckm_tail']:>10.4f}" if r['D_ckm_tail'] is not None
              else f"{n_runs:>7}  {r['n_stops']:>7}  {r['n_negative_delta_A']:>11}  {'?':>10}")

    out = OUT_DIR / "n_runs_sweep_summary.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nSummary: {out}")

    print("\nReferencia — puntos ya conocidos manualmente:")
    print("  n_runs=50, seed=123 -> 3/20  (réplica manual, REG addendum)")
    print("  n_runs=80, seed=123 -> 20/20 (TASK_armstrong_replica_seed123_via_corpus_v3)")


if __name__ == "__main__":
    main()
