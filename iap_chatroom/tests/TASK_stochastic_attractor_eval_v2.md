# TASK_stochastic_attractor_eval_v2.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v2 changes from v1:*
*— Versioning explícito: bloque de cambios al inicio, nuevo archivo por versión (no sobreescribir).*
*— Índice diferenciable: `index.json` → `index_{W_sha8}.json` — un índice por estado de W,*
*  no por corrida. Evita colisión entre entornos con mismo nombre de archivo.*
*— JSONL de runs: `runs_{W_sha8}_{timestamp}.jsonl` — W_sha8 agrega diferenciación de campo.*

---

## Convención de versiones de esta TASK

Cada versión es un archivo nuevo con sufijo `_vN.md`.
No sobreescribir versiones anteriores — son traza del proceso.
La versión activa para Code es siempre la de número más alto.

---

## Contexto — por qué existe esta tarea

`_count_attractors(n_runs, seed)` en `services/coco.py` genera estados
iniciales pseudoaleatorios vía `np.random.default_rng(seed)`. Esto implica:

1. **`seed` fija una secuencia determinística**, no una muestra aleatoria.
   `seed=42` y `seed=123` son dos muestras fijas distintas del espacio de
   estados — no son réplicas, no son variación del campo.

2. **`n_runs` actúa como un estimador tipo coupon-collector**: el número
   de atractores únicos hallados crece con `n_runs` sin convergencia clara.
   Verificado en REG_n_runs_sweep_armstrong_v1.md (n_runs 10→200, D_ckm_tail
   0.30→0.54, sin saturación).

3. **Consecuencia**: el umbral `D_CKM_THRESHOLD = 0.40` no es propiedad
   del campo — es propiedad del instrumento a los valores de `n_runs` y
   `seed` usados en la campaña P1–P5. El confound afecta la interpretación
   de los resultados "confirmados".

Esta tarea construye un módulo que **aísla seed y n_runs como variables
independientes** sin tocar ningún código existente (NO MODIFICAR).

---

## Paso 0 — Verificación previa OBLIGATORIA

**Leer antes de construir nada. Reportar hallazgos a delamor antes de
continuar.**

```bash
cat services/coco.py
```

Verificar y reportar:
- Firma real de `_count_attractors()` — parámetros exactos, tipos, defaults
- Cómo llama a `np.random.default_rng(seed)` internamente (¿seed se pasa
  directo? ¿existe lógica adicional?)
- Qué devuelve exactamente (tipo, campos)
- Dónde en `coco.py` se invoca `_count_attractors` (cuántas veces, desde
  qué métodos: `observe()`, `_landscape_component()`, etc.)

```bash
cat tests/test_coco.py
ls process/experiments/
cat process/experiments/n_runs_sweep/n_runs_sweep_summary.json 2>/dev/null | head -5
```

Verificar:
- Cómo los tests existentes llaman a COCO (¿seed y n_runs explícitos?)
- Si existe ya algún script de sweep que pueda servir como referencia
  de diseño (no copiar — entender estructura)

```bash
ls experiments/
```

Ubicación del módulo: **`experiments/`** — ya existe, contiene pipelines de
validación externa (`fourforums_pipeline_v8h.py`, `calibrate_W_mixta.py`).
El módulo va ahí, como archivo Python nuevo.

Ubicación de los outputs (JSONL, índice): **`process/experiments/stochastic_eval/`**
— `process/` es estado experimental y backups. No mezclar con código.

---

## Módulo — especificación mínima viable

### Función

Ejecutar `_count_attractors()` bajo rangos configurables de `seed` y
`n_runs`, producir distribuciones de resultados, reportar raw.

### Scope — lo que hace

- Recibe: rango de seeds, rango de n_runs, referencia a instancia COCO
  (o a W+Δ_r para construirla internamente — decisión según lo que
  encuentre en Paso 0)
- Por cada combinación (seed, n_runs): llama `_count_attractors()`
  y registra el resultado
- Produce: distribución de A_observed por (seed, n_runs) combinación
- Reporta: raw, sin interpretación (ver §Reporte)

### Scope — lo que NO hace

- **NO modifica** `_count_attractors()`, `coco.py`, ningún archivo existente
- **NO interpreta** los resultados (sin conclusiones en el output del módulo)
- **NO toca** los experimentos P1–P5 ni sus scripts
- **NO agrega** lógica de threshold ni de STOP al módulo

### Inputs — configuración

```python
seeds: list[int]          # ej. [0, 1, 2, ..., 49]  — rango, no seed única
n_runs_range: list[int]   # ej. [10, 20, 30, 50, 80, 100, 150]
```

Configuración mínima para primera ejecución:
- `seeds`: al menos 10 valores distintos (sugerencia: 0–9)
- `n_runs_range`: coincidir con los valores ya en REG_n_runs_sweep_armstrong_v1.md
  para permitir comparación directa (10, 20, 30, 40, 50, 60, 70, 80, 100, 150)

### PRNG

Un único método: `np.random.default_rng(seed)`.
No agregar otros métodos en v1.
El método PRNG y su versión se registran en cada run (ver §Logging).

### Ejecución

Cada combinación (seed, n_runs) es una unidad de trabajo independiente.
Las combinaciones pueden ejecutarse en cualquier orden.

Si el proceso es interrumpido (timeout, kill), debe haber escrito al
menos el último estado parcial completo antes de morir — ver §Timeout.

### Reporte — raw únicamente

El módulo produce un registro por combinación (seed, n_runs). Campos
obligatorios:

```
seed            int
n_runs          int
A_observed      int        # resultado de _count_attractors()
prng_method     str        # "numpy.default_rng"
numpy_version   str        # np.__version__ real en runtime
execution_time  float      # segundos
process_id      int        # os.getpid()
run_hash        str        # sha256(f"{seed}:{n_runs}:{W_sha}:{A_observed}")
W_sha           str        # sha256 de W al momento de la evaluación
```

**Sin campos de interpretación.** Sin `threshold_comparison`, sin
`stop_triggered`, sin `zone`. Eso es capa separada.

**`W_sha`**: usar el mismo método que `Firma_CKM` para sha256(W) si
existe una función canónica — verificar en `firma_ckm.py` antes de
reimplementar.

### Logging

**JSONL de runs** — cada run escribe su resultado en el momento en que
termina, no al final de la ejecución completa:

```
process/experiments/stochastic_eval/runs_{W_sha8}_{timestamp}.jsonl
```

`W_sha8` = primeros 8 caracteres del sha256(W). Diferencia corridas sobre
distintos estados de W. `timestamp` = ISO 8601 compacto (ej. `20260814T153022`).

**Índice** — un índice por estado de W, no uno global:

```
process/experiments/stochastic_eval/index_{W_sha8}.json
```

Mapea: `run_hash → {seed, n_runs, W_sha, status, jsonl_path, timestamp}`

El índice `index_{W_sha8}.json` se actualiza por cada run completado sobre
ese W. Si el proceso muere, el índice refleja exactamente los runs
completados hasta ese momento. Múltiples entornos o corridas sobre el
mismo W actualizan el mismo índice — si hay concurrencia, ver §Acceso.

**Acceso concurrente al índice**: en v1 (secuencial) no es necesario
resolver. Si en Paso 0 se decide ejecución paralela, agregar lock de
archivo antes de construir.

### Timeout

Si el proceso recibe SIGTERM o SIGINT:
1. Finalizar el run en curso si está a menos de N segundos de terminar
   (N configurable, default 5s) — o cancelarlo limpiamente
2. Escribir estado parcial al JSONL antes de salir
3. Actualizar el índice con `status="interrupted"` para runs no completados
4. Salir limpiamente

Los runs interrumpidos son válidos para análisis posterior — registrar
como tales, no descartar.

---

## H2 — verificación pendiente (no bloquea esta tarea)

REG_n_runs_sweep_armstrong_v1.md declara H2 como "propuesto, no verificado":

> Si `A0` (baseline, sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
> tasas distintas con `n_runs`, `D_ckm` hereda ese sesgo estructural.

El módulo, al poder llamar `_count_attractors()` sobre W solo (sin Δ_r)
y sobre W+Δ_r por separado, permite verificar H2 como extensión natural.

**No incluir en v1.** Registrar como extensión cuando el módulo esté
operativo.

---

## Criterio de éxito

```bash
python -m pytest tests/ -q
```
→ Sin regresiones. Verificar número actual de tests antes de correr
(README declara 82/82 total — confirmar).

El módulo corre una ejecución de prueba mínima:
- `seeds=[0, 1, 2]`, `n_runs_range=[10, 50]`
- Produce JSONL `runs_{W_sha8}_{timestamp}.jsonl` con 6 registros
- Produce `index_{W_sha8}.json` con 6 entradas, todas `status="completed"`
- `run_hash` único por combinación
- `W_sha` en el reporte coincide con `sha256(W_momento)` de `Firma_CKM`
  para el mismo W

---

## Convenciones de archivos

- **Módulo**: `experiments/stochastic_attractor_eval.py`
- **Outputs**: `process/experiments/stochastic_eval/` — no commitear
- **`.gitignore`**: agregar `process/experiments/stochastic_eval/` si no está
- **REG**: `registers/REG_stochastic_eval_v1.md` — generar tras primera
  ejecución completa, no antes

---

## Bloqueo explícito

Si `_count_attractors()` no acepta `seed` como parámetro externo
(seed hardcodeado internamente): **detener y reportar** — no modificar.
Resolver con delamor antes de continuar.

---

*gadanin.delamor + Claude Sonnet 4.6 · Agosto 2026*
