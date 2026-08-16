# TASK_stochastic_attractor_eval_v3.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v3 changes from v2:*
*— Paso 0 ya ejecutado (esta sesión, Claude Code) — hallazgos confirmados,*
*  ver sección "Hallazgos del Paso 0" en vez de re-verificar desde cero.*
*— Bloqueo explícito de v2 NO se dispara: `_count_attractors(self, W_eff)`*
*  no recibe seed/n_runs como parámetros — los lee de `self._seed`/*
*  `self._n_runs`, fijados una vez en `COCO.__init__()`. No está*
*  hardcodeado (sí es configurable), solo no es parámetro del método.*
*  Resolución: instanciar un COCO nuevo por cada combinación (seed, n_runs).*
*— Outputs: "no commitear" de v2 revertido. Lo que un REG cita tiene que*
*  ser auditable — en la práctica de este repo, commiteado. Mismo criterio*
*  que ya se aplicó a `process/n_runs_sweep/` (commiteado completo).*
*  Alcance del "completo": los seeds/n_runs que esta task ya especifica*
*  (§Inputs) — no un compromiso abierto a cualquier escala futura.*
*— Confirmado: `firma_ckm.py` tiene `_sha256(arr)` — reusar, no reimplementar.*
*— Criterio de éxito: `python -m pytest tests/ -q` no corre en este entorno*
*  (pytest no instalado para este intérprete). Usar los runners existentes*
*  (`python3 tests/test_*.py` individual) — mismo criterio, otra invocación.*

---

## Convención de versiones de esta TASK

Cada versión es un archivo nuevo con sufijo `_vN.md`.
No sobreescribir versiones anteriores — son traza del proceso.
La versión activa para Code es siempre la de número más alto.

---

## Contexto — por qué existe esta tarea

`_count_attractors()` en `services/coco.py` genera estados iniciales
pseudoaleatorios vía `np.random.default_rng(self._seed)`. Esto implica:

1. **`seed` fija una secuencia determinística**, no una muestra aleatoria.
   `seed=42` y `seed=123` son dos muestras fijas distintas del espacio de
   estados — no son réplicas, no son variación del campo.

2. **`n_runs` actúa como un estimador tipo coupon-collector**: el número
   de atractores únicos hallados crece con `n_runs` sin convergencia clara.
   Verificado en `REG_n_runs_sweep_armstrong_v1.md` (n_runs 10→200, D_ckm_tail
   0.30→0.54, sin saturación).

3. **Consecuencia**: el umbral `D_CKM_THRESHOLD = 0.40` no es propiedad
   del campo — es propiedad del instrumento a los valores de `n_runs` y
   `seed` usados en la campaña P1–P5. El confound afecta la interpretación
   de los resultados "confirmados".

Esta tarea construye un módulo que **aísla seed y n_runs como variables
independientes** sin tocar ningún código existente (NO MODIFICAR).

---

## Hallazgos del Paso 0 (ya verificados, esta sesión)

- **Firma real de `_count_attractors`**: `def _count_attractors(self, W_eff: np.ndarray) -> int`.
  Solo recibe `W_eff`. `seed`, `n_runs` y `N` vienen de `self._seed`,
  `self._n_runs`, `self.N` — atributos de instancia fijados en
  `COCO.__init__()`, no argumentos del método.
- **Llamadas dentro de `coco.py`**: 3, todas dentro de `observe()` — línea
  con `A_current`, línea con `self._A0` (baseline sobre `self.W` solo),
  línea con `A_despues` (dentro de la rama `track_landscape`).
- **Decisión de diseño que esto resuelve**: el módulo instancia un `COCO`
  nuevo por cada combinación `(seed, n_runs)` — construir uno es barato,
  no corre relajaciones en `__init__`.
- **`firma_ckm.py`**: tiene `_sha256(arr) -> str` (`hashlib.sha256(arr.tobytes()).hexdigest()`),
  privada pero importable. Reusar para `W_sha`.
- **`experiments/coco_thermostat.py`**: prototipo pre-COCO stale, ya movido
  a `process/experiments/coco_thermostat.py` (traza, no código operativo).
  No importar de ahí — el módulo nuevo importa de `services/coco.py`.
- **Conteo de tests**: `tests/test_coco.py` (28) + `tests/test_monitor_services.py` (35)
  + `tests/test_firma_ckm.py` (10) + `tests/test_w_version.py` (9) = **82**.
  Coincide con lo que el README declara.

---

## Módulo — especificación mínima viable

### Función

Ejecutar `_count_attractors()` bajo rangos configurables de `seed` y
`n_runs`, producir distribuciones de resultados, reportar raw.

### Scope — lo que hace

- Recibe: rango de seeds, rango de n_runs, W (matriz sobre la que instanciar
  cada COCO)
- Por cada combinación (seed, n_runs): instancia `COCO(W=W, seed=seed, n_runs=n_runs)`,
  llama `_count_attractors(W)` (y opcionalmente sobre `W + Δ_r` si se
  extiende a H2 — no en v1), registra el resultado
- Produce: distribución de A_observed por (seed, n_runs) combinación
- Reporta: raw, sin interpretación (ver §Reporte)

### Scope — lo que NO hace

- **NO modifica** `_count_attractors()`, `coco.py`, ningún archivo existente
- **NO interpreta** los resultados (sin conclusiones en el output del módulo)
- **NO toca** los experimentos P1–P5 ni sus scripts
- **NO agrega** lógica de threshold ni de STOP al módulo

### Inputs — configuración

```python
seeds: list[int]          # ej. [0, 1, 2, ..., 9]  — rango, no seed única
n_runs_range: list[int]   # [10, 20, 30, 40, 50, 60, 70, 80, 100, 150]
```

Configuración mínima para primera ejecución:
- `seeds`: 0–9 (10 valores)
- `n_runs_range`: los mismos valores de `REG_n_runs_sweep_armstrong_v1.md`,
  para permitir comparación directa

Este es el alcance de "corrida completa" para efectos de qué se commitea
(ver §Convenciones de archivos) — no un compromiso abierto a escalas
mayores sin revisar de nuevo.

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

**`W_sha`**: usar `_sha256()` de `services/firma_ckm.py` — confirmado que
existe, no reimplementar.

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
completados hasta ese momento.

**Acceso concurrente al índice**: en v1 (secuencial) no es necesario
resolver. Si en la ejecución se decide paralela, agregar lock de
archivo antes.

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

`REG_n_runs_sweep_armstrong_v1.md` declara H2 como "propuesto, no verificado":

> Si `A0` (baseline, sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
> tasas distintas con `n_runs`, `D_ckm` hereda ese sesgo estructural.

El módulo, al poder llamar `_count_attractors()` sobre W solo (sin Δ_r)
y sobre W+Δ_r por separado, permite verificar H2 como extensión natural.

**No incluir en v1.** Registrar como extensión cuando el módulo esté
operativo.

---

## Criterio de éxito

```bash
python3 tests/test_coco.py
python3 tests/test_monitor_services.py
python3 tests/test_firma_ckm.py
python3 tests/test_w_version.py
```
→ 82/82 combinado, sin regresiones.

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
- **Outputs**: `process/experiments/stochastic_eval/`
- **Commit**: SÍ — la corrida completa (seeds 0–9, n_runs de §Inputs) se
  commitea, mismo criterio que `process/n_runs_sweep/`. Lo que el
  `REG_stochastic_eval_v1.md` cite tiene que ser auditable por cualquier
  device; eso significa commiteado, no local. No es un compromiso abierto
  a corridas de escala mayor sin revisar de nuevo esta decisión.
- **REG**: `registers/REG_stochastic_eval_v1.md` — generar tras primera
  ejecución completa, no antes

---

## NO modificar

- `_count_attractors()`, `coco.py`, ningún archivo existente
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
