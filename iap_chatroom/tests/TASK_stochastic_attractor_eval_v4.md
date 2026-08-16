# TASK_stochastic_attractor_eval_v4.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v4 changes from v3:*
*— Agrega sección "Diseño concreto (Claude Code)" — arquitectura propuesta*
*  antes de escribir código, para confirmar ejecución.*
*— Resuelve de dónde sale W para la corrida real: depende del corpus del*
*  experimento en cuestión (IAP series, fourforums SQL, etc.) — el módulo*
*  recibe W como parámetro, agnóstico. Para esta corrida específica*
*  (comparabilidad con REG_n_runs_sweep_armstrong_v1.md), W es la del*
*  corpus Armstrong — mismo W que esa REG usó.*
*— Resto igual a v3 (Hallazgos del Paso 0, bloqueo que no se dispara,*
*  commit acotado al alcance especificado, ubicación de outputs).*

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
- **Bloqueo explícito de v2 no se dispara** — seed no está hardcodeado,
  es configurable vía constructor. Resolución: instanciar un COCO nuevo
  por cada combinación (seed, n_runs).
- **`firma_ckm.py`**: tiene `_sha256(arr) -> str`, privada pero importable.
  Reusar para `W_sha`.
- **`experiments/coco_thermostat.py`**: prototipo pre-COCO stale, ya movido
  a `process/experiments/coco_thermostat.py`. No importar de ahí.
- **Conteo de tests**: 28+35+10+9 = **82**, coincide con el README.

---

## Diseño concreto (Claude Code)

Un archivo, dos capas: una función atómica testeable sola, y un runner
que arma el sweep sobre ella.

### `run_one(W, seed, n_runs) -> dict`

La unidad de trabajo. Instancia `COCO(W=W, seed=seed, n_runs=n_runs)`,
cronometra la llamada a `_count_attractors(W)`, calcula `W_sha` con
`_sha256()` de `firma_ckm.py`, arma `run_hash` desde
`seed:n_runs:W_sha:A_observed`, devuelve el dict con los 9 campos de
§Reporte. Sin interpretación — ningún `if A_observed > threshold` acá.

### Sweep

Itera el producto cartesiano `seeds × n_runs_range`. Por cada combinación:
llama `run_one`, escribe el resultado al JSONL apenas termina (no
acumula en memoria hasta el final), actualiza el índice
`index_{W_sha8}.json` con esa entrada en `status="completed"`.
`timestamp` se genera una vez al arrancar el sweep — todos los registros
de una misma invocación van al mismo JSONL.

### Señales (SIGTERM/SIGINT)

Interrumpir `_count_attractors` a mitad de sus reinicios internos sin
tocar `coco.py` no es limpio — la combinación en curso siempre termina.
Al recibir la señal: dejar terminar la combinación actual, escribir su
resultado, no arrancar la siguiente. El índice queda con lo completado
en `status="completed"`; lo planeado-pero-no-corrido no aparece (no se
inventa un estado intermedio).

### De dónde sale W

El módulo recibe `W` como parámetro — agnóstico de corpus, reusable
para cualquier experimento (IAP series, fourforums SQL, lo que sea).

**Para esta corrida específica**: `W` del corpus Armstrong — la misma
que construye `test_armstrong_stop_coco.py` vía `CorpusService` +
`WARMUP_TEXTS` — porque es la que usa `REG_n_runs_sweep_armstrong_v1.md`,
y esta task pide comparabilidad directa con esos resultados.

---

## Módulo — especificación mínima viable

### Scope — lo que hace

- Recibe: rango de seeds, rango de n_runs, W
- Por cada combinación (seed, n_runs): `run_one(W, seed, n_runs)`
- Produce: distribución de A_observed por combinación
- Reporta: raw, sin interpretación

### Scope — lo que NO hace

- **NO modifica** `_count_attractors()`, `coco.py`, ningún archivo existente
- **NO interpreta** los resultados (sin conclusiones en el output del módulo)
- **NO toca** los experimentos P1–P5 ni sus scripts
- **NO agrega** lógica de threshold ni de STOP al módulo

### Inputs — configuración

```python
seeds: list[int]          # 0–9 para la corrida real
n_runs_range: list[int]   # [10, 20, 30, 40, 50, 60, 70, 80, 100, 150]
```

Este es el alcance de "corrida completa" para efectos de qué se commitea
— no un compromiso abierto a escalas mayores sin revisar de nuevo.

### PRNG

Un único método: `np.random.default_rng(seed)`. No agregar otros en v1.
Se registra en cada run (`prng_method`, `numpy_version`).

### Reporte — raw únicamente

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

Sin campos de interpretación. Sin `threshold_comparison`, `stop_triggered`, `zone`.

### Logging

```
process/experiments/stochastic_eval/runs_{W_sha8}_{timestamp}.jsonl
process/experiments/stochastic_eval/index_{W_sha8}.json
```

`W_sha8` = primeros 8 caracteres del sha256(W). `timestamp` = ISO 8601
compacto. Índice mapea `run_hash → {seed, n_runs, W_sha, status, jsonl_path, timestamp}`,
actualizado por cada run completado.

Acceso concurrente al índice: no necesario resolver en v1 (secuencial).

---

## H2 — verificación pendiente (no bloquea esta tarea)

`REG_n_runs_sweep_armstrong_v1.md` declara H2 como "propuesto, no verificado":

> Si `A0` (baseline, sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
> tasas distintas con `n_runs`, `D_ckm` hereda ese sesgo estructural.

El módulo, al poder llamar `_count_attractors()` sobre W solo (sin Δ_r)
y sobre W+Δ_r por separado, permite verificar H2 como extensión natural.

**No incluir en v1.** Registrar como extensión cuando el módulo esté operativo.

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
- `W_sha` coincide con `sha256(W_momento)` de `Firma_CKM` para el mismo W

---

## Convenciones de archivos

- **Módulo**: `experiments/stochastic_attractor_eval.py`
- **Outputs**: `process/experiments/stochastic_eval/`
- **Commit**: SÍ — la corrida completa (seeds 0–9, n_runs de §Inputs),
  mismo criterio que `process/n_runs_sweep/`. Lo que
  `REG_stochastic_eval_v1.md` cite tiene que ser auditable — commiteado,
  no local.
- **REG**: `registers/REG_stochastic_eval_v1.md` — generar tras primera
  ejecución completa, no antes

---

## NO modificar

- `_count_attractors()`, `coco.py`, ningún archivo existente
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
