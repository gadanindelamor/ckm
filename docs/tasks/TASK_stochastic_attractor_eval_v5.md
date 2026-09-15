
# TASK_stochastic_attractor_eval_v5.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v5 changes from v4:*
*— Resuelve lo que v4 dejaba diferido ("acceso concurrente: no necesario*
*  resolver en v1"). Se pide paralelismo — diseño de locking agregado.*
*— El proceso no es singleton (nunca lo fue) y ahora corre en paralelo*
*  de dos formas simultáneas posibles: pool interno de workers dentro de*
*  una invocación, y/o invocaciones externas separadas sobre la misma W.*
*  Ambas protegidas por el mismo mecanismo de lock.*
*— Resto igual a v4 (Hallazgos del Paso 0, W como parámetro, commit*
*  acotado, ubicación de outputs).*

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
2. **`n_runs` actúa como un estimador tipo coupon-collector**: crece sin
   convergencia clara. Verificado en `REG_n_runs_sweep_armstrong_v1.md`
   (n_runs 10→200, D_ckm_tail 0.30→0.54, sin saturación).
3. **Consecuencia**: `D_CKM_THRESHOLD = 0.40` es propiedad del instrumento
   a los valores de `n_runs`/`seed` usados en P1–P5, no del campo.

Esta tarea construye un módulo que **aísla seed y n_runs como variables
independientes** sin tocar ningún código existente (NO MODIFICAR).

---

## Hallazgos del Paso 0 (ya verificados, esta sesión)

- **Firma real de `_count_attractors`**: `def _count_attractors(self, W_eff: np.ndarray) -> int`.
  Lee `self._seed`/`self._n_runs`/`self.N` — no son parámetros del método.
- **Bloqueo explícito de v2 no se dispara** — seed configurable vía
  constructor, no hardcodeado. Un COCO nuevo por combinación (seed, n_runs).
- **`firma_ckm.py`**: tiene `_sha256(arr) -> str`, reusar para `W_sha`.
- **`experiments/coco_thermostat.py`**: ya movido a `process/experiments/`.
- **Conteo de tests**: 28+35+10+9 = **82**.

---

## Diseño concreto (Claude Code)

### `run_one(W, seed, n_runs) -> dict`

Función pura, sin I/O. Instancia `COCO(W=W, seed=seed, n_runs=n_runs)`,
cronometra `_count_attractors(W)`, calcula `W_sha`/`run_hash`, devuelve
el dict de §Reporte. No escribe nada — eso es responsabilidad de otra capa.

### Paralelismo — dos niveles, un mismo mecanismo de lock

**No es singleton.** Nada impide múltiples procesos operando sobre la
misma W al mismo tiempo, de dos formas:

1. **Pool interno**: una invocación reparte las combinaciones (seed,
   n_runs) entre varios workers con `concurrent.futures.ProcessPoolExecutor(max_workers=N)`.
   Cada worker corre `run_one` (CPU-bound — cómputo real en paralelo,
   no I/O esperando). Los workers no escriben directamente: devuelven
   el dict al proceso principal, que va escribiendo a medida que cada
   uno termina (`as_completed()`).

2. **Invocaciones externas simultáneas**: dos `python3 experiments/stochastic_attractor_eval.py`
   corriendo a la vez sobre la misma W (ej. dos terminales, o dos rangos
   de seed distintos apuntando al mismo índice). Estas sí escriben cada
   una por su cuenta — no hay proceso padre coordinando.

Ambos casos convergen en el mismo punto de riesgo: escritura concurrente
sobre `index_{W_sha8}.json` (read-modify-write) y sobre el JSONL.
Se protegen con el mismo mecanismo, sin importar si el escritor es un
worker interno o una invocación externa separada.

### `_write_result(record, jsonl_path, index_path)` — sección crítica con lock

```
lock_path = index_path + ".lock"
con fcntl.flock() sobre lock_path (bloqueante, LOCK_EX):
    abrir jsonl_path en modo append, escribir la línea del record, cerrar
    leer index_path si existe (o {} si no), agregar la entrada
        run_hash -> {seed, n_runs, W_sha, status, jsonl_path, timestamp},
    escribir index_path completo de nuevo
liberar el lock (automático al cerrar el file descriptor)
```

`fcntl.flock` funciona entre procesos no relacionados (workers de un
pool, o invocaciones externas independientes) — no depende de que
compartan un padre común. Es el mismo mecanismo para los dos niveles
de paralelismo de arriba.

### Señales (SIGTERM/SIGINT)

Con pool interno: al recibir la señal, el proceso principal deja de
enviar nuevas combinaciones a los workers, espera las que ya están en
vuelo (vía `_write_result`, cada una protegida por su propio lock), y
sale. No mata workers a mitad de una llamada a `_count_attractors`.

Con invocación externa: cada proceso maneja su propia señal igual —
termina su combinación en curso, la escribe con lock, sale. No afecta
a otras invocaciones corriendo en paralelo sobre la misma W, porque el
lock serializa solo la sección crítica de escritura, no la ejecución.

### De dónde sale W

Parámetro del módulo, agnóstico de corpus — depende del experimento
(IAP series, fourforums SQL, etc.). Para esta corrida: W del corpus
Armstrong (`test_armstrong_stop_coco.py`, `WARMUP_TEXTS`), la misma que
usa `REG_n_runs_sweep_armstrong_v1.md`, para comparabilidad directa.

---

## Módulo — especificación mínima viable

### Scope — lo que hace

- Recibe: rango de seeds, rango de n_runs, W, `max_workers` (default 1
  = secuencial, sin pool)
- Por cada combinación: `run_one(W, seed, n_runs)`, escrita vía
  `_write_result` con lock
- Reporta: raw, sin interpretación

### Scope — lo que NO hace

- **NO modifica** `_count_attractors()`, `coco.py`, ningún archivo existente
- **NO interpreta** los resultados
- **NO toca** los experimentos P1–P5 ni sus scripts
- **NO agrega** lógica de threshold ni de STOP

### Inputs

```python
seeds: list[int]          # 0–9 para la corrida real
n_runs_range: list[int]   # [10, 20, 30, 40, 50, 60, 70, 80, 100, 150]
max_workers: int          # default 1
```

Alcance de "corrida completa" para efectos de commit — no un compromiso
abierto a escalas mayores sin revisar de nuevo.

### PRNG

`np.random.default_rng(seed)` únicamente. Registrado en cada run.

### Reporte — raw únicamente

```
seed            int
n_runs          int
A_observed      int
prng_method     str        # "numpy.default_rng"
numpy_version   str
execution_time  float
process_id      int        # distingue qué worker/invocación produjo cada run
run_hash        str        # sha256(f"{seed}:{n_runs}:{W_sha}:{A_observed}")
W_sha           str
```

Sin campos de interpretación.

### Logging

```
process/experiments/stochastic_eval/runs_{W_sha8}_{timestamp}.jsonl
process/experiments/stochastic_eval/index_{W_sha8}.json
process/experiments/stochastic_eval/index_{W_sha8}.json.lock  # no se commitea, es efímero
```

---

## H2 — verificación pendiente (no bloquea esta tarea)

`REG_n_runs_sweep_armstrong_v1.md` declara H2 como "propuesto, no verificado":
si `A0` (sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a tasas
distintas con `n_runs`, `D_ckm` hereda ese sesgo. El módulo permite
verificarlo llamando `_count_attractors()` sobre ambos por separado.
**No incluir en v1.**

---

## Criterio de éxito

```bash
python3 tests/test_coco.py
python3 tests/test_monitor_services.py
python3 tests/test_firma_ckm.py
python3 tests/test_w_version.py
```
→ 82/82 combinado, sin regresiones.

Prueba mínima: `seeds=[0,1,2]`, `n_runs_range=[10,50]`, `max_workers=2`
(ejercita el pool, no solo el camino secuencial) → JSONL con 6 registros,
índice con 6 entradas `status="completed"`, `run_hash` único por
combinación, sin corrupción del índice pese a escritura concurrente.

---

## Convenciones de archivos

- **Módulo**: `experiments/stochastic_attractor_eval.py`
- **Outputs**: `process/experiments/stochastic_eval/`
- **Commit**: SÍ — corrida completa (seeds 0–9, n_runs de §Inputs), mismo
  criterio que `process/n_runs_sweep/`. El archivo `.lock` no se commitea
  (es coordinación efímera, no evidencia).
- **REG**: `registers/REG_stochastic_eval_v1.md` — tras primera ejecución
  completa, no antes

---

## NO modificar

- `_count_attractors()`, `coco.py`, ningún archivo existente
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
