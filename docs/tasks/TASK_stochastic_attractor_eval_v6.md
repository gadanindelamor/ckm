# TASK_stochastic_attractor_eval_v6.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v6 changes from v5:*
*— `run_one` y `run_pair` actualizados: pasan `weighted=True` a*
*  `_count_attractors()` (disponible desde REG_count_attractors_bias_v1.md).*
*— n_act por reinicio usa distribución uniforme `rng.uniform(0.3, 0.7) * N`*
*  — no distribución normal. Documentado explícitamente en docstring.*
*— n_runs_range permanece como lista de checkpoints fijos — no sampleado*
*  desde ninguna distribución.*
*— Experimento re-ejecutado con los mismos parámetros que v5.*
*— REG nuevo: REG_stochastic_eval_v2.md*

---

## Convención de versiones

Cada versión es un archivo nuevo con sufijo `_vN.md`.
No sobreescribir versiones anteriores.
La versión activa para Code es siempre la de número más alto.

---

## Contexto

`REG_count_attractors_bias_v1.md` (Ago 2026) agrega `weighted=True` a
`_count_attractors(W_eff, weighted=False)` y `_mean_cS(W_eff, weighted=False)`
en `services/coco.py`. El default es `False` — `observe()` no fue
modificado. El modo ponderado es de uso manual/experimental.

`experiments/stochastic_attractor_eval.py` llama `_count_attractors`
directamente. Esta tarea lo actualiza para usar `weighted=True` y
re-ejecuta el experimento, produciendo resultados comparables con v5.

---

## Paso 0 — obligatorio antes de tocar nada

Leer literalmente (no de memoria):
- `services/coco.py` — firma actual de `_count_attractors` y `_mean_cS`.
  Confirmar que `weighted: bool = False` existe y que `_node_probs` y
  `_sample_s0` están en su lugar.
- `experiments/stochastic_attractor_eval.py` — todas las llamadas a
  `_count_attractors` y `_mean_cS`.
- `registers/REG_stochastic_eval_v1.md` — parámetros exactos de la
  corrida anterior (seeds, n_runs_range, W usada, max_workers).

Reportar:
- Firma real de `_count_attractors` encontrada en coco.py.
- Líneas exactas que llaman `_count_attractors` o `_mean_cS` en el módulo.
- Parámetros de la corrida v1 (del REG).

Si `weighted` no existe en coco.py → STOP. Reportar a delamor.

---

## Cambios al módulo

**Archivo único**: `experiments/stochastic_attractor_eval.py`

### Tarea 1 — `run_one`

```python
# antes
a_observed = coco._count_attractors(W)

# después
a_observed = coco._count_attractors(W, weighted=True)
```

Agregar al dict de retorno: `"weighted": True`

### Tarea 2 — `run_pair`

```python
# antes
a0       = coco._count_attractors(W)
a_actual = coco._count_attractors(W + Delta_r)

# después
a0       = coco._count_attractors(W,            weighted=True)
a_actual = coco._count_attractors(W + Delta_r,  weighted=True)
```

Agregar al dict de retorno: `"weighted": True`

### Tarea 3 — docstring del módulo

Agregar al docstring existente:

```
v6 (Ago 2026): _count_attractors llamado con weighted=True.
Distribución de nodos: ponderada por fi = |W_eff|.sum(axis=1).
n_act por reinicio: uniform(0.3, 0.7) * N — no distribución normal.
n_runs_range: checkpoints fijos — no sampleados desde ninguna distribución.
```

---

## Ejecución

Mismos parámetros que la corrida documentada en `registers/REG_stochastic_eval_v1.md`
(leer en Paso 0 — no asumir valores). Si el REG no especifica max_workers,
usar `max_workers=2`.

Output en `process/experiments/stochastic_eval/` con timestamp nuevo —
no sobreescribir archivos de corridas anteriores.

---

## Criterio de éxito

```bash
python tests/test_coco.py    # 28/28 sin regresión
python experiments/stochastic_attractor_eval.py   # corre sin error
```

JSONL generado con campo `"weighted": true` en todos los registros.
Índice sin corrupción.

---

## REG

Crear `registers/REG_stochastic_eval_v2.md` — archivo nuevo, no modificar v1.
*Clase R.*

Contenido mínimo:
- Descripción: corrida con `weighted=True`, referencia a v1 para comparación.
- Parámetros usados (seeds, n_runs_range, W_sha, max_workers).
- Tabla comparativa donde existan ambos valores:
  `seed | n_runs | A_observed_uniform (v1) | A_observed_weighted (v6)`
- Lo que no establece esta corrida (misma disciplina que REG_count_attractors_bias_v1).

---

## NO modificar

- `services/coco.py`
- `tests/test_coco.py`
- `registers/REG_stochastic_eval_v1.md`
- Ningún archivo en `process/`

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
