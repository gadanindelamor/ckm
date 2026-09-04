# TASK_coco_load_landscape_history_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Objetivo

COCO nace con W y muere con W. Su traza no muere — está en el JSONL de
MonitorService. Al nacer, COCO debe poder cargar esa historia a memoria.

La elipse se abre con memoria persistida.

---

## Contexto

Post T5b: `CorpusService._rebuild()` instancia `COCO(W=self._W, track_landscape=True)`.
COCO arranca con `_landscape_history = []` — sin memoria de ciclos previos.

El JSONL de MonitorService (`storage_path`) contiene cada `evaluate()` como
línea JSON. Cada línea que tuvo `stop_applied=True` tiene
`panel["thermostat"]["landscape_delta"]` con el dict completo
(`A_antes`, `A_despues`, `delta_A`, `cS_antes`, `cS_despues`, `delta_cS`,
`alpha_used`, `D_ckm`).

Esa es la traza persistida. COCO al nacer debe leerla.

---

## Diseño

### `COCO.__init__` — agregar parámetro `landscape_history`

```python
def __init__(
    self,
    W: np.ndarray,
    n_runs: int = 50,
    seed: int = 42,
    dynamic_alpha: bool = True,
    track_landscape: bool = False,
    landscape_history: list[dict] | None = None,   # ← nuevo
):
    ...
    self._landscape_history: list[dict] = list(landscape_history) if landscape_history else []
```

### `CorpusService` — función de carga desde JSONL

```python
def _load_landscape_history(self, jsonl_path: str | None) -> list[dict]:
    """
    Lee el JSONL de MonitorService y extrae los landscape_delta
    de todas las evaluaciones donde stop_applied=True.
    Devuelve lista vacía si el archivo no existe o no hay STOPs.
    """
    if not jsonl_path or not Path(jsonl_path).exists():
        return []
    history = []
    with open(jsonl_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                ld = record.get("panel", {}).get("thermostat", {}).get("landscape_delta")
                if ld is not None:
                    history.append(ld)
            except (json.JSONDecodeError, AttributeError):
                continue
    return history
```

### `CorpusService._rebuild()` — pasar historia al nuevo COCO

```python
def _rebuild(self):
    # ... lógica existente de rebuild W ...
    history = self._load_landscape_history(getattr(self, '_monitor_jsonl_path', None))
    self._coco = COCO(
        W=self._W,
        track_landscape=True,
        landscape_history=history,
    )
```

### `CorpusService` — registrar el path del JSONL

CorpusService necesita saber dónde está el JSONL de MonitorService.
Opciones:

**Opción A (mínima):** agregar `monitor_jsonl_path: str | None = None`
a `CorpusService.__init__()`. CKMMonitor lo pasa al construir CorpusService.

**Opción B:** CorpusService no conoce el path — MonitorService lo pasa
explícitamente antes del rebuild via `corpus.set_monitor_path(path)`.

Elegir **Opción A** — más directa, sin estado mutable extra.

---

## Criterio de éxito

```bash
python services/test_coco.py        # 28/28 sin regresiones
python services/test_monitor_services.py  # 35/35

# Verificar carga desde JSONL:
python3 -c "
from services.corpus_service import CorpusService
import json, tempfile, os

# Crear JSONL mínimo con un landscape_delta
ld = {'A_antes': 10, 'A_despues': 13, 'delta_A': 3,
      'cS_antes': 0.004, 'cS_despues': 0.005, 'delta_cS': 0.001,
      'alpha_used': 0.15, 'D_ckm': 0.45}
record = {'panel': {'thermostat': {'stop_applied': True, 'landscape_delta': ld}}}

with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
    f.write(json.dumps(record) + '\n')
    jsonl_path = f.name

corpus = CorpusService(storage_path='/tmp/test_load.json',
                       min_texts=3,
                       monitor_jsonl_path=jsonl_path)
corpus.ingest(['text one about knowledge', 'text two about field', 'text three about attractor'])
assert corpus.mode == 'evaluation'
assert corpus.coco is not None
history = corpus.coco.landscape_history()
assert len(history) == 1, f'esperado 1, got {len(history)}'
assert history[0]['delta_A'] == 3
print(f'OK — landscape_history cargada: {history}')
os.unlink(jsonl_path)
"
```

---

## NO modificar

- Lógica de `_alpha_for()` — retrospectiva, sin cambios
- Lógica de ponderación en `_rebuild()` — no existe, no inventar
- REGs históricos
- `agent_device_skin.py`, `groq_research_agent.py`

---

## Archivos a modificar

```
services/coco.py          — landscape_history param en __init__
services/corpus_service.py — _load_landscape_history(), monitor_jsonl_path param,
                             _rebuild() pasa history al COCO nuevo
```

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
