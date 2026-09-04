# REG_stochastic_eval_v2.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Re-ejecución del sweep de `REG_stochastic_eval_v1.md` con
`_count_attractors(..., weighted=True)` — el modo de muestreo ponderado
agregado en `REG_count_attractors_bias_v1.md`. Mismos parámetros, misma
W, mismo módulo. La única variable que cambia es la distribución sobre
nodos de la que se sortea σ₀.

Spec ejecutada: `iap_chatroom/tests/TASK_stochastic_attractor_eval_v6.md`.
Archivo modificado: `experiments/stochastic_attractor_eval.py` únicamente.

---

## Paso 0 — verificación previa

**Firma real encontrada en `services/coco.py`:**

```python
def _count_attractors(self, W_eff: np.ndarray, weighted: bool = False) -> int
def _mean_cS(self, W_eff: np.ndarray, weighted: bool = False) -> float
```

`_node_probs(W_eff, weighted)` y `_sample_s0(rng, probs)` presentes.
No hubo STOP.

**Llamadas en `experiments/stochastic_attractor_eval.py`** (líneas de la
versión previa a esta task):

| Línea | Llamada | Función |
|---|---|---|
| 53 | `coco._count_attractors(W)` | `run_one` |
| 183 | `coco._count_attractors(W)` | `run_pair` |
| 184 | `coco._count_attractors(W + Delta_r)` | `run_pair` |

Ninguna llamada a `_mean_cS` en el módulo.

**Parámetros de la corrida v1** (leídos del REG y verificados contra el
JSONL crudo, no asumidos):

| Parámetro | Valor | Fuente |
|---|---|---|
| seeds | `[0..9]` (10) | `runs_42e76ebc_20260815T214649.jsonl` |
| n_runs_range | `[10,20,30,40,50,60,70,80,100,150]` | idem |
| W_sha | `42e76ebc…c8ca55c` (N=20, de `WARMUP_TEXTS`) | idem |
| max_workers | no especificado para la corrida completa | REG cita `max_workers=2` solo para el smoke test; el JSONL v1 muestra 4 `process_id` distintos |
| combinaciones | 100 | REG §Descripción |

Se usó `max_workers=2` según la instrucción de la TASK. El número de
workers no afecta resultados: `run_one` es pura y la escritura está
serializada por `flock`.

---

## Hallazgo previo a la corrida — contaminación de `_smoke_corpus_state.json`

El primer intento de ejecutar `python experiments/stochastic_attractor_eval.py`
(criterio de éxito de la TASK) produjo **W_sha `ca767fb4`, no `42e76ebc`**.

Causa: el bloque `__main__` construye el corpus con
`storage_path=process/experiments/stochastic_eval/_smoke_corpus_state.json`
— un path **persistente**, versionado en git. En la corrida v1 ese archivo
no existía; al correr de nuevo, `CorpusService` cargó los 20 textos ya
guardados y `ingest(WARMUP_TEXTS)` agregó los mismos 20 otra vez → 40
textos → otra W. Verificado: el state en disco tenía 40 textos tras la
corrida; reconstruido desde un `storage_path` limpio, el sha vuelve a ser
`42e76ebc`.

**Es un bug preexistente del `__main__`, no de esta task.** El smoke test
no es idempotente: cada ejecución duplica el corpus y evalúa una W
distinta.

Acciones: `_smoke_corpus_state.json` restaurado con `git checkout`; los
dos artefactos `*_ca767fb4_*` generados por ese intento fueron borrados
por inválidos. `process/` quedó como estaba. El sweep de este REG se
lanzó con un driver externo que construye W desde un `storage_path`
temporal — como hizo v1 — y **verifica el sha contra `42e76ebc` antes de
correr**.

No se corrigió el `__main__`: la TASK declara archivo único y no incluye
ese cambio. Queda anotado.

---

## Cambios al módulo

- `run_one`: `_count_attractors(W, weighted=True)`; `"weighted": True` en el dict.
- `run_pair`: `_count_attractors(W, weighted=True)` y
  `_count_attractors(W + Delta_r, weighted=True)`; `"weighted": True` en el dict.
- Docstring del módulo: bloque v6 (ponderación por
  `fi = |W_eff|.sum(axis=1)`; `n_act = uniform(0.3,0.7)·N`, no normal;
  `n_runs_range` = checkpoints fijos, no sampleados).

---

## Ejecución

| | |
|---|---|
| Datos | `process/experiments/stochastic_eval/runs_42e76ebc_20260821T074545.jsonl` |
| Registros | 100, todos con `"weighted": true` (verificado por assert) |
| Índice | `index_42e76ebc.json` — 193 entradas |
| Tests | `tests/test_coco.py` → 28/28, sin regresión |

**Sobre las 193 entradas del índice.** 100 (v1) + 100 (v6) = 200; el
índice quedó en 193 porque `run_hash = sha256(seed:n_runs:W_sha:A_observed)`
**no incluye `weighted`**. Las 7 combinaciones donde el conteo ponderado
coincidió con el uniforme colapsaron sobre la entrada de v1, sobrescribiéndola.
El índice no está corrupto — es consistente y parseable — pero **ya no
distingue corrida uniforme de ponderada**. Los dos JSONL son archivos
separados e íntegros: la evidencia por registro está preservada y es la
fuente para la tabla de abajo. Corregir el `run_hash` implicaría tocar la
identidad de los registros de v1; no se hizo.

---

## Resultado — el muestreo ponderado baja el conteo de forma sistemática

| n_runs | A uniform v1 (mean) | min | max | A weighted v6 (mean) | min | max | diff | iguales |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 10  | 9.9   | 9   | 10  | 9.5  | 9  | 10 | −0.4  | 6/10 |
| 20  | 19.7  | 19  | 20  | 17.9 | 17 | 20 | −1.8  | 0/10 |
| 30  | 29.6  | 29  | 30  | 25.4 | 23 | 29 | −4.2  | 1/10 |
| 40  | 38.9  | 37  | 40  | 32.1 | 28 | 35 | −6.8  | 0/10 |
| 50  | 48.4  | 46  | 50  | 38.7 | 34 | 44 | −9.7  | 0/10 |
| 60  | 57.8  | 56  | 60  | 45.1 | 39 | 52 | −12.7 | 0/10 |
| 70  | 66.4  | 64  | 69  | 50.2 | 45 | 56 | −16.2 | 0/10 |
| 80  | 75.7  | 74  | 79  | 53.8 | 48 | 60 | −21.9 | 0/10 |
| 100 | 94.2  | 91  | 98  | 62.6 | 56 | 70 | −31.6 | 0/10 |
| 150 | 136.2 | 134 | 140 | 83.2 | 78 | 93 | −53.0 | 0/10 |

Pareado por (seed, n_runs), sobre 100 combinaciones: **v6 < v1 en 92,
igual en 7, v6 > v1 en 1** (una combinación, por +1). Media de la
diferencia: −15.8.

**La saturación aparece bajo muestreo ponderado:**

| n_runs | A/n_runs v1 | A/n_runs v6 | pendiente local v6 |
|---|---:|---:|---:|
| 10  | 0.990 | 0.950 | — |
| 20  | 0.985 | 0.895 | +0.840 |
| 30  | 0.987 | 0.847 | +0.750 |
| 40  | 0.972 | 0.802 | +0.670 |
| 50  | 0.968 | 0.774 | +0.660 |
| 60  | 0.963 | 0.752 | +0.640 |
| 70  | 0.949 | 0.717 | +0.510 |
| 80  | 0.946 | 0.672 | +0.360 |
| 100 | 0.942 | 0.626 | +0.440 |
| 150 | 0.908 | 0.555 | +0.412 |

En v1 el cociente `A/n_runs` se mantenía entre 0.91 y 0.99 en todo el
rango — crecimiento ~1:1, sin saturar. Bajo `weighted=True` cae
monótonamente de 0.95 a 0.56, y la pendiente local baja de +0.84 a ~+0.41.
El régimen coupon-collector del v1 **se atenúa** bajo muestreo ponderado
en esta W. El rango min-max por punto se ensancha (en n_runs=150: 78–93,
spread 15, contra 6 en v1): la varianza entre seeds sube.

---

## Lo que esta corrida NO establece

- **No establece que el conteo ponderado sea más correcto.** Mide una
  cantidad distinta con la misma etiqueta: número de atractores alcanzados
  desde una distribución inicial diferente. Sin conteo exhaustivo de
  atractores en esta W no hay referencia contra la cual llamar a uno
  "mejor". La dirección observada (menos atractores) es la **opuesta** a
  la que anticipaba `TASK_count_attractors_bias_v1.md` — allí el argumento
  era que el muestreo uniforme *subestima* por sobremuestrear zonas
  muertas. Es la segunda vez que la dirección observada contradice esa
  expectativa (ver `REG_count_attractors_bias_v1.md`, W sintética con hub:
  8 < 13). Dos observaciones consistentes entre sí, ninguna explicada.
- **No establece que el sesgo n_runs esté resuelto.** El conteo sigue
  creciendo con n_runs en todo el rango medido, sin plateau. La pendiente
  baja; no llega a cero. Extrapolar saturación más allá de n_runs=150 no
  está sostenido por estos datos.
- **No toca `observe()`.** `services/coco.py` no fue modificado; el
  default sigue siendo `weighted=False`. Nada en el runtime CKM cambió
  de comportamiento por esta corrida.
- **Una sola W (N=20, `WARMUP_TEXTS`).** No es el corpus CKM operativo
  (N=32) ni una W_mixta con nodo tipo-965 — el caso que motivaba el modo
  ponderado sigue sin probarse.
- **`run_pair` fue actualizado pero no re-ejecutado.** La corrida H2
  (`h2_runs_run1_*.jsonl`) es de v1, uniforme. Los resultados H2 de
  `REG_stochastic_eval_v1.md` y posteriores no fueron re-medidos bajo
  ponderación, y dado el tamaño del efecto de arriba, **no deben
  compararse con registros ponderados futuros**.

---

## Sección v7 — `run_hash` con `weighted`, y H2 re-ejecutado ponderado

*Ago 2026 — `TASK_stochastic_attractor_eval_v7.md`. Sección agregada a
este REG, no archivo nuevo. Nada de la corrida v6 documentada arriba
fue modificado.*

### Paso 0 — qué cambió v6 en el módulo

Diff verificado contra `HEAD` (v5): bloque v6 en el docstring del
módulo; `weighted=True` en las tres llamadas a `_count_attractors`
(líneas 53 de `run_one`, 183/184 de `run_pair`); campo `"weighted": True`
en los dos dicts de retorno. Nada más. `REG_stochastic_eval_v2.md`
registraba ese estado correctamente.

### Objetivo 1 — `weighted` entra en el `run_hash`

**Impedimento encontrado:** `weighted` no existía como nombre en el
módulo. Estaba escrito como literal `True` dentro de la llamada y otra
vez como literal en el dict — meterlo al f-string del hash habría dado
`NameError`. Se convirtió en **parámetro** `weighted: bool = True` de
`run_one` y `run_pair`, con passthrough desde `run_h2_case`. Ahora la
llamada a `_count_attractors`, el input del hash y el campo del registro
salen de la misma variable; el default preserva el comportamiento v6.
`weighted=False` reproduce el modo uniforme de v1 con hashes propios.

En `run_pair` el parámetro aplica a las **dos** mediciones del par —
documentado en el docstring: la comparación es pareada y mezclar modos
la rompería.

Además, la entrada del índice ahora incluye `weighted` — el índice es
legible por modo sin abrir el JSONL.

**Verificación de la colisión concreta.** No alcanza con que dos hashes
cualesquiera difieran: el caso que colapsaba en v6 es aquel donde ambos
modos dan el **mismo** `A_observed`. Se buscó uno (seed=0, n_runs=10,
A=2 en los dos modos) y se comprobó hash distinto. `run_pair` idem.
`tests/test_coco.py` → 28/28.

### Objetivo 2 — H2 ponderado

Mismos 10 casos IAP, mismos `count_seeds=range(10)`, mismos checkpoints
`[10,30,100,300,1000,3000,10000]` que `REG_h2_a0_vs_aactual_v1.md`.
Correspondencia `case_id → archivo` idéntica (verificada contra la tabla
de ese REG y contra los `Delta_r_sha` del JSONL de v1).

| | |
|---|---|
| Datos | `process/experiments/stochastic_eval/h2_runs_run2w_20260821T083359.jsonl` |
| Índice | `h2_index_run2w_20260821T083359.json` — 225 entradas, 225 registros |
| Colisiones con el índice de v1 | **0 hashes compartidos** (criterio de éxito cumplido) |

**El control se sostiene:** `case_id=6` (Δ_r = 0.0 exacto) da `delta=0` y
`D_ckm=0.0` en todos los checkpoints también bajo ponderación.

**Pero la profundidad de la traza se movió, en las dos direcciones:**

| case | n_runs máx v1 | n_runs máx v7 |
|---|---:|---:|
| 0, 1, 3, 6, 7 | 30 | 30 |
| 2, 4, 5, 8 | 30 | **100** |
| 9 | **3000** | **300** |

Cuatro casos cortos llegan más lejos; `case_id=9` — el único que en v1
tenía rango suficiente para trazar la curva completa y **el que respondió
H2** — corta en 300. `CONVERGENCIA` (pendiente < 0.10) dispara antes
porque bajo ponderación los conteos crecen a ~la mitad de velocidad
(ver tabla de saturación de la sección v6). El umbral `CONVERGENCIA_SLOPE
= 0.10` fue calibrado sobre conteos uniformes; aplicado a conteos
ponderados corta a otra altura. *[Propuesto: el mecanismo es
consistente con lo observado, pero no se corrió un control con el umbral
reescalado — sin eso no está verificado.]*

### `case_id=9` — lo que se puede y no se puede comparar

| n_runs | A0 v1 | A_act v1 | D_ckm v1 | A0 v7 | A_act v7 | D_ckm v7 | seeds v7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 10   | 7.6   | 7.5   | 0.0017 | 5.6  | 4.0  | 0.2833 | 10 |
| 30   | 16.7  | 14.9  | 0.1023 | 10.1 | 7.9  | 0.1828 | 10 |
| 100  | 33.5  | 31.4  | 0.0597 | 21.0 | 19.1 | 0.0769 | 9 |
| 300  | 68.3  | 64.1  | 0.0611 | 40.7 | 34.7 | 0.1354 | 7 |
| 1000 | 160.2 | 137.1 | 0.1420 | —    | —    | —      | 0 |
| 3000 | 317.5 | 231.2 | 0.2716 | —    | —    | —      | 0 |

En el rango común (10→300): A0 crece ×9.0 uniforme contra ×7.3
ponderado; `D_ckm` va de 0.0017→0.0611 uniforme y de 0.2833→0.1354
ponderado — **en direcciones opuestas dentro del mismo rango**.

### `D_ckm` a n_runs=30 — no es invariante al modo de muestreo

Punto común a los 10 casos:

| case | D_ckm v1 | D_ckm v7 | A0 v1 | A0 v7 |
|---|---:|---:|---:|---:|
| 0 | −0.0667 | −0.0667 | 2.1 | 2.1 |
| 1 | 0.1317 | −0.0333 | 3.0 | 2.6 |
| 2 | 0.3202 | 0.5203 | 6.4 | 7.2 |
| 3 | 0.7670 | **0.4500** | 8.8 | 3.8 |
| 4 | 0.9044 | 0.8742 | 26.4 | 21.7 |
| 5 | 0.5095 | **0.0317** | 8.6 | 4.2 |
| 6 | 0.0000 | 0.0000 | 2.6 | 2.3 |
| 7 | 0.5367 | 0.5267 | 8.7 | 4.8 |
| 8 | 0.8570 | 0.8491 | 22.0 | 18.5 |
| 9 | 0.1023 | 0.1828 | 16.7 | 10.1 |

Seis casos se mueven poco; **`case_id=3` cae de 0.767 a 0.450 y
`case_id=5` de 0.510 a 0.032** — el segundo cruza de lado a lado de
`D_CKM_THRESHOLD = 0.40`. Con los mismos textos, el mismo Δ_r y el mismo
`n_runs`, cambiar solo la distribución de la que se sortea σ₀ cambia si
COCO habría disparado STOP o no. El caso 1 cambia de signo (0.132 →
−0.033): campo "degradado" o "expandido" según el muestreo.

`D_ckm` heredaba un sesgo por `n_runs` (atenuado, según
`REG_h2_a0_vs_aactual_v1.md`); esto es un **segundo eje de sensibilidad,
independiente del primero** — a `n_runs` fijo.

Eventos: `CONVERGENCIA` 100 (igual que v1), `RIESGO_CONFOUND_SALIDA` 101
(v1: 110), `COLAPSO_SENAL` 40 (v1: 36).

### Objetivo 3 — bug de idempotencia del `__main__` (evaluado, no tocado)

**Causa, leída en el código:** `CorpusService.__init__` llama `_load()`
si el `storage_path` existe y tiene contenido
(`services/corpus_service.py:67`); `ingest()` hace
`self._texts.extend(texts)` **sin deduplicar** (`:79`). El `__main__` del
módulo pasa un path persistente y versionado en git
(`process/experiments/stochastic_eval/_smoke_corpus_state.json`), así que
cada ejecución agrega otra copia de `WARMUP_TEXTS`: 20 → 40 → 60 textos,
y W distinta en cada corrida. Es lo que produjo `W_sha=ca767fb4` durante
la ejecución de v6.

No es un defecto de `CorpusService`: `extend` sin dedup es el
comportamiento correcto para un corpus en streaming. El defecto es usar
un archivo persistente como fixture de un smoke test.

Opciones, sin ejecutar ninguna:

1. **`tempfile` en el `__main__`**, borrado al final — el smoke queda
   idempotente y el fixture sale de `process/`. Es lo que ya hacen
   `build_case_w_and_delta_r` y los drivers de v6/v7. Costo: se pierde el
   archivo como traza; es reconstruible desde `WARMUP_TEXTS`.
2. **Borrar el archivo al inicio del `__main__`** si existe. Idempotente
   también, pero sigue escribiendo en `process/` y deja el path
   versionado — la trampa queda armada para el próximo.
3. **Dejarlo y documentarlo** en el docstring. Es el estado actual; ya
   costó una W equivocada una vez.

Recomendación: opción 1. Pendiente de instrucción de delamor.

### Lo que la corrida v7 NO establece

- **No re-responde H2 bajo ponderación.** La respuesta de
  `REG_h2_a0_vs_aactual_v1.md` se apoyaba en `case_id=9` hasta
  n_runs=3000. Bajo ponderación esa serie corta en 300 y no hay ninguna
  otra que llegue más lejos. El rango observado no alcanza para decidir
  si la cancelación parcial del sesgo en `D_ckm` se mantiene.
- **No dice cuál modo mide mejor.** Igual que en las dos corridas
  anteriores: sin conteo exhaustivo de atractores no hay referencia.
- **No explica la inversión de `D_ckm` en `case_id=9`** dentro del rango
  común. Está registrada, no interpretada.
- **No se corrió el control del umbral `CONVERGENCIA_SLOPE` reescalado**
  — el corte temprano de `case_id=9` queda como mecanismo propuesto.
- **Nada fue commiteado**, según la TASK.

### Observación sobre `REG_h2_a0_vs_aactual_v1.md` (no modificado)

Ese REG describe a `case_id=9` como *"el más largo, 24 textos"*. Su
propia tabla mapea `case_id=9 → caso12_run2` (9 textos) y
`case_id=8 → caso09_run2` (24 textos). La corrida v7 confirma el mapeo
de la tabla: case 9 tiene 9 textos, case 8 tiene 24. La descripción en
prosa está equivocada; la tabla y los datos son correctos, y la
comparación de arriba usa el mismo mapeo que v1, así que es válida. Se
reporta acá porque los REGs históricos no se modifican.

---

## Archivos relacionados

- `experiments/stochastic_attractor_eval.py` — módulo (modificado en esta task)
- `process/experiments/stochastic_eval/h2_runs_run2w_20260821T083359.jsonl` — datos H2 ponderados (v7)
- `registers/REG_h2_a0_vs_aactual_v1.md` — corrida H2 uniforme, sin modificar
- `iap_chatroom/tests/TASK_stochastic_attractor_eval_v7.md` — spec de la sección v7
- `process/experiments/stochastic_eval/runs_42e76ebc_20260821T074545.jsonl` — datos v6
- `registers/REG_stochastic_eval_v1.md` — corrida uniforme, sin modificar
- `registers/REG_count_attractors_bias_v1.md` — origen de `weighted`
- `iap_chatroom/tests/TASK_stochastic_attractor_eval_v6.md` — spec ejecutada
- `services/coco.py` — sin modificar

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
