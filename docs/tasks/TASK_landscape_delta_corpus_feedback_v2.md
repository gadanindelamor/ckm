# TASK_landscape_delta_corpus_feedback_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*v2 — reescrita con hallazgos de lectura previa de Code*

---

## Objetivo

Cerrar el circuito O₂→W: el `landscape_delta` acumulado por COCO durante
la fase de evaluación informa la siguiente fase de acumulación.

---

## Principio de diseño (decisión de gadanin.delamor)

**COCO nace y muere con W.**
CorpusService es quien sabe cuándo W cambia — es su evento interno.
El lugar correcto para instanciar COCO es dentro de `_rebuild()`, no CKMMonitor.

---

## Contexto — hallazgos de lectura previa (Code)

- `COCO._last_landscape_delta` guarda solo el último STOP — se sobreescribe.
  No hay historial acumulado. `_alpha_trajectory` tiene `{t, alpha, D_ckm, delta_A}`
  pero no `cS_antes/cS_despues`. Nunca persistido por sí solo.
- `rebuild_W()` público no existe — es `_rebuild()` interno, disparado desde
  `ingest()` cuando `len(texts) >= min_texts`.
- `CKMMonitor` no instancia COCO — `MonitorService` se crea sin `thermostat=`.
  COCO solo vive en test scripts. Esta task cierra ese gap.

---

## Implementar

### 1. `COCO` — agregar `landscape_history()`

En `__init__`:
```python
self._landscape_history: list[dict] = []
```

En `observe()`, rama `track_landscape`, después del assign a `_last_landscape_delta`:
```python
self._landscape_history.append(self._last_landscape_delta.copy())
```

Getter público:
```python
def landscape_history(self) -> list[dict]:
    """Full history of landscape_delta dicts from all STOP events."""
    return list(self._landscape_history)
```

### 2. `CorpusService` — COCO nace con W

En `_rebuild()`, al final:
```python
from coco import COCO
self._coco = COCO(W=self._W, track_landscape=True)
```

Property pública:
```python
@property
def coco(self):
    """Active COCO instance. None if corpus in accumulation mode."""
    return getattr(self, '_coco', None)
```

### 3. `CorpusService.ingest()` — recibe landscape_signal

```python
def ingest(self, texts, landscape_signal=None):
    ...
    if landscape_signal is not None:
        self._last_landscape_signal = landscape_signal
    # resto sin cambios
```

La ponderación basada en `landscape_signal` queda fuera de alcance — solo plomería.

### 4. `CKMMonitor` — leer corpus.coco, pasar señal

CKMMonitor no gestiona el ciclo de vida de COCO — solo lo lee:
```python
if self._corpus.coco is not None:
    signal = self._corpus.coco.landscape_history()
    # pasar en próximo ingest
    self._corpus.ingest(new_texts, landscape_signal=signal)
```

---

## Criterio de éxito

```bash
python services/test_coco.py   # sin regresiones

python3 -c "
from services.corpus_service import CorpusService
from services.coco import COCO
corpus = CorpusService(storage_path='/tmp/test_cs.json', min_texts=3)
corpus.ingest(['text one about knowledge', 'text two about field', 'text three about attractor'])
assert corpus.mode == 'evaluation', f'mode={corpus.mode}'
assert corpus.coco is not None, 'coco is None'
assert isinstance(corpus.coco, COCO), 'not COCO instance'
assert hasattr(corpus.coco, 'landscape_history'), 'no landscape_history'
print('OK — corpus.coco instanciado en rebuild')
print(f'landscape_history: {corpus.coco.landscape_history()}')
"
```

---

## NO modificar

- Lógica de `_alpha_for()` — retrospectiva, sin cambios
- Lógica de ponderación en `_rebuild()` — no existe, no inventar
- REGs históricos
- `agent_device_skin.py`, `groq_research_agent.py`

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
