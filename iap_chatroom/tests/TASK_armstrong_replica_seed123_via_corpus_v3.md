# TASK_armstrong_replica_seed123_via_corpus_v3.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*v3 — agrega criterio delta_cS ≠ 0.0 en al menos un STOP*

---

## Objetivo

Armstrong con seed=123 usando COCO tal como vive ahora en producción:
- instanciado por CorpusService en `_rebuild()` (T5b)
- `landscape_history()` acumula los STOPs en memoria (T5b)
- historia desde JSONL previo: **pendiente** (T5c — siguiente task)

Verifica end-to-end: corpus rebuilds W → COCO nace → MonitorService usa
`corpus.coco` como thermostat → `landscape_history` acumula → resultado
comparado contra réplica manual (3/20 STOPs esperados).

---

## Precondiciones

```bash
python services/test_coco.py              # 28/28
python services/test_monitor_services.py  # 35/35
python services/test_firma_ckm.py        # 10/10
python services/test_w_version.py         # 9/9
```

---

## Script

Guardar como `iap_chatroom/tests/test_armstrong_via_corpus_v3.py`:

```python
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
```

---

## Criterio de éxito

```
1. corpus.coco instanciado con seed=123 (no None)
2. len(stops) == 3  (igual que réplica manual seed=123)
3. len(landscape_history()) == len(stops)
4. delta_A > 0 en los 3 STOPs
5. delta_cS != 0.0 en al menos 1 STOP
   — si todos son 0.0: no es bug, documentar como hallazgo
6. armstrong_via_corpus_v3_summary.json generado con stops + landscape_history
```

Si `len(stops) != 3`: reportar D_ckm de t=3 en adelante — puede ser diferencia
en W reconstruida vs réplica manual. No asumir bug.

Si `delta_cS == 0.0` en todos los STOPs: el paisaje cambió en atractores
pero no en cohesión media. Documentar — no corregir en esta task.

---

## Commit

```bash
git add iap_chatroom/tests/test_armstrong_via_corpus_v3.py \
        process/experiments/armstrong_via_corpus_v3_summary.json \
        process/experiments/armstrong_via_corpus_v3.jsonl
git commit -m "feat: Armstrong via corpus v3 — landscape_history + criterio delta_cS, seed=123"
git push
```

---

## NO modificar

- `test_armstrong_stop_coco.py` — canónico seed=42
- `test_armstrong_replica_seed123.py` — réplica manual
- REGs existentes

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
