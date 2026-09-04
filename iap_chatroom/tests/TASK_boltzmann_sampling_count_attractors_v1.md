# TASK_boltzmann_sampling_count_attractors_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Para: Code Opus*

---

## Objetivo

Agregar `mode="boltzmann"` como tercer modo de muestreo de σ₀ en
`_count_attractors()` de `coco.py`.

El modo uniforme y el modo ponderado tienen sesgos documentados
(REG_situacion_medicion_ago2026_v1, REG_stochastic_eval_v2).
Este modo propone muestreo termodinámicamente fundamentado desde
la distribución de Boltzmann del landscape.

---

## Paso 0 — verificar en repo antes de cualquier modificación

```bash
# Verificar que relax(beta=float) existe en hopfield.py
grep -n "beta" services/hopfield.py

# Verificar _count_attractors en coco.py
grep -n "_count_attractors\|_sample_s0\|_relax" services/coco.py

# Estado actual de modos disponibles
grep -n "weighted\|uniform\|mode" services/coco.py | head -30
```

Si `relax(beta=float)` no existe en hopfield.py con la firma esperada,
detener y reportar a delamor antes de continuar.

---

## Qué implementar

### β_c calculado desde W en runtime

```
β_c = 1 / (ρ* · N · μ_W)

donde:
  ρ*  = densidad óptima = 0.5 (P4, N=32)
  N   = W.shape[0]
  μ_W = np.mean(W[W > 0])   # media sobre pesos no-nulos
```

β_c es un parámetro calculado — no hardcodeado.

### Calentamiento Boltzmann

Para cada run en `_count_attractors`:

1. Partir de σ₀ aleatorio uniforme (estado inicial)
2. Correr `n_warmup` pasos de `relax(beta=β_c)` de `hopfield.py`
   — relajación estocástica que lleva el estado hacia la distribución
   de Boltzmann
3. Usar el estado resultante como σ₀ para el relax determinístico habitual

`n_warmup` como parámetro configurable. Valor inicial propuesto: `n_warmup = N`.
No hay garantía de mezcla completa — n_warmup óptimo es una pregunta abierta.

### Firma resultante

```python
def _count_attractors(self, W_eff, weighted=False, boltzmann=False, n_warmup=None):
    ...
```

`boltzmann=True` tiene precedencia sobre `weighted`. Si ambos son False:
modo uniforme (comportamiento actual sin cambio).

---

## Criterio de éxito

```bash
python tests/test_coco.py   # todos los tests existentes pasan sin cambio

# Verificar que el nuevo modo corre sin error
python -c "
from services.coco import COCO
import json, numpy as np

with open('services/W_ckm_corpus_v2.json') as f:
    d = json.load(f)
W = np.array(d['W'])

coco = COCO(W=W, n_runs=20, seed=42)
a_unif = coco._count_attractors(W, boltzmann=False)
a_bolt = coco._count_attractors(W, boltzmann=True, n_warmup=32)
print(f'uniforme={a_unif}  boltzmann={a_bolt}')
# No asumir dirección del resultado — registrar y documentar
"
```

Agregar al panel de `monitor_service.py` (si thermostat presente):

```python
panel["thermostat"]["sampling_mode"] = "boltzmann" if boltzmann else \
                                        "weighted"  if weighted else \
                                        "uniform"
```

Para trazabilidad del modo activo en cada decisión de STOP.

---

## NO modificar

- Comportamiento de `weighted=False, boltzmann=False` — sin regresión
- Tests existentes de coco.py y monitor_service.py
- REGs históricos
- ALPHA_MIN, ALPHA_MAX, D_CKM_THRESHOLD
- Lógica de OPERADOR_STOP_COCO

---

## Archivos a modificar

```
services/coco.py          — _count_attractors(), β_c helper
services/monitor_service.py — panel sampling_mode (si corresponde)
```

---

## Lo que este TASK no cierra

- n_warmup óptimo: abierto, depende de tiempo de mezcla del landscape
- Si mode="boltzmann" da mejor cobertura de cuencas que uniforme o ponderado:
  empírico, requiere REG posterior con los resultados
- ρ* para W_mixta: se usa 0.5 (de P4 W_base). Puede diferir para W_mixta.

---

*Repo: gadanindelamor/ckm · Para Code Opus*
