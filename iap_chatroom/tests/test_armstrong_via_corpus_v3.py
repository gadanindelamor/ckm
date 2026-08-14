"""
test_armstrong_via_corpus_v3.py
Armstrong replica seed=123 — COCO instanciado por CorpusService.
Verifica landscape_history() acumulado post T5b.
Historia previa desde JSONL: pendiente (T5c).
"""
import json
from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "services"))

from corpus_service import CorpusService
from monitor_service import MonitorService
from coco import COCO

import importlib.util
spec = importlib.util.spec_from_file_location(
    "armstrong_orig",
    _REPO_ROOT / "iap_chatroom/tests/test_armstrong_stop_coco.py"
)
orig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orig)

CORPUS_PATH = str(_REPO_ROOT / "process/experiments/armstrong_via_corpus_v3_state.json")
OUTPUT_PATH = str(_REPO_ROOT / "process/experiments/armstrong_via_corpus_v3.jsonl")

# CorpusService instancia COCO en _rebuild()
corpus = CorpusService(storage_path=CORPUS_PATH, min_texts=15)
corpus.ingest(orig.WARMUP_TEXTS)

assert corpus.mode == "evaluation", f"mode={corpus.mode}"
assert corpus.coco is not None, "corpus.coco es None — verificar _rebuild()"

# Reemplazar con seed=123 (Opción A — sin tocar CorpusService)
corpus._coco = COCO(W=corpus.get_W(), seed=123, track_landscape=True)

print(f"corpus.coco: seed=123, track_landscape=True")
print(f"beta_c_corpus: {corpus.coco.beta_c_corpus():.4f}")
print(f"landscape_history al inicio: {len(corpus.coco.landscape_history())} entradas")

# MonitorService usa corpus.coco como thermostat
monitor = MonitorService(
    corpus,
    storage_path=OUTPUT_PATH,
    n_runs_attractors=50,
    thermostat=corpus.coco,
)

stops = []
for i, text in enumerate(orig.TEXTS):
    panel = monitor.evaluate(text, device_id=f"test_{i:02d}")
    ts = panel.get("thermostat", {}) or {}
    stop = ts.get("stop_applied", False)
    d_ckm = ts.get("D_ckm", 0)
    zone = ts.get("zone", "?")

    if stop:
        ld = ts.get("landscape_delta")
        stops.append({
            "t": i,
            "alpha_used": ts.get("alpha_used"),
            "D_ckm_coco": d_ckm,
            "zone": zone,
            "delta_A": ld["delta_A"] if ld else None,
            "delta_cS": ld["delta_cS"] if ld else None,
        })
        print(f"  *** ARMSTRONG t={i}: D_ckm={d_ckm:.4f} "
              f"delta_A={ld['delta_A'] if ld else '?'} "
              f"delta_cS={ld['delta_cS'] if ld else '?'}")
    else:
        print(f"  t={i:2d}: D_ckm={d_ckm:.4f} zone={zone} stop=False")

history = corpus.coco.landscape_history()
print(f"\nSTOPs: {len(stops)}/{len(orig.TEXTS)}")
print(f"landscape_history acumulado: {len(history)} entradas")

assert len(history) == len(stops), \
    f"landscape_history ({len(history)}) != stops ({len(stops)})"

print(f"\nResultado esperado: 3/20")
if len(stops) != 3:
    print("DIVERGENCIA — documentar, no asumir bug")

summary = {
    "stops": stops,
    "landscape_history": history,
    "n_stops": len(stops),
    "expected_n_stops": 3,
    "seed": 123,
    "via_corpus": True,
}
out = _REPO_ROOT / "process/experiments/armstrong_via_corpus_v3_summary.json"
out.write_text(json.dumps(summary, indent=2))
print(f"Summary: {out}")
