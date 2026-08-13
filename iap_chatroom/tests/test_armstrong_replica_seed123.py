"""
test_armstrong_replica_seed123.py
Réplica de test_armstrong_stop_coco.py — única variable cambiada: seed
(42 -> 123) en la instancia de COCO. Mismo corpus, mismos TEXTS, mismo
n_runs, track_landscape=True. Output separado, no pisa el Intento 2
canónico.

Ver registers/REG_armstrong_stop_coco_v1.md, sección "Réplica —
seed=123, única variable cambiada".
"""
import sys
import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "services"))

from corpus_service import CorpusService
from monitor_service import MonitorService
from coco import COCO

import importlib.util
spec = importlib.util.spec_from_file_location(
    "armstrong_orig", _REPO_ROOT / "iap_chatroom/tests/test_armstrong_stop_coco.py"
)
orig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orig)

CORPUS_PATH = str(_REPO_ROOT / "process/experiments/armstrong_replica_seed123_corpus_state.json")
OUTPUT_PATH = str(_REPO_ROOT / "process/experiments/armstrong_replica_seed123.jsonl")

corpus = CorpusService(storage_path=CORPUS_PATH, min_texts=15)
corpus.ingest(orig.WARMUP_TEXTS)
assert corpus.mode == "evaluation"

W = corpus.get_W()
th = COCO(W=W, n_runs=50, seed=123, track_landscape=True)  # única variable: seed
monitor = MonitorService(corpus, storage_path=OUTPUT_PATH, n_runs_attractors=50, thermostat=th)

stops = []
for i, text in enumerate(orig.TEXTS):
    panel = monitor.evaluate(text, device_id=f"test_{i:02d}")
    ts = panel.get("thermostat", {}) or {}
    if ts.get("stop_applied"):
        ld = ts.get("landscape_delta")
        stops.append({
            "t": i,
            "alpha_used": ts["alpha_used"],
            "D_ckm_coco": ts["D_ckm"],
            "delta_A": ld["delta_A"] if ld else None,
            "delta_cS": ld["delta_cS"] if ld else None,
        })

print(f"STOPs: {len(stops)}/{len(orig.TEXTS)}")
for s in stops[:5]:
    print(s)

Path(_REPO_ROOT / "process/experiments/armstrong_replica_seed123_summary.json").write_text(
    json.dumps(stops, indent=2)
)
