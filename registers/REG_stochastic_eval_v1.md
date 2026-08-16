# REG_stochastic_eval_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Módulo `experiments/stochastic_attractor_eval.py` (`TASK_stochastic_attractor_eval_v5.md`),
diseñado para aislar `seed` y `n_runs` como variables independientes de
`_count_attractors()` (`services/coco.py`), sin modificar ese archivo.
Confirma con estadística propia (10 seeds × 10 valores de `n_runs`, 100
combinaciones) el hallazgo de `REG_n_runs_sweep_armstrong_v1.md`, que
había corrido con un solo seed por punto.

Módulo: `experiments/stochastic_attractor_eval.py`
Datos: `process/experiments/stochastic_eval/`
  - `runs_42e76ebc_20260815T214604.jsonl` (smoke test, 6 registros)
  - `runs_42e76ebc_20260815T214649.jsonl` (corrida completa, 100 registros)
  - `index_42e76ebc.json` (100 entradas, deduplicadas por `run_hash`)

---

## Diseño verificado

- `run_one(W, seed, n_runs)` — función pura, instancia un `COCO` nuevo
  por combinación (no hay forma de pasar seed/n_runs a `_count_attractors`
  directamente — son atributos fijados en `COCO.__init__()`).
- `_write_result()` — sección crítica protegida por `fcntl.flock` sobre
  un archivo `.lock` dedicado. Funciona igual entre workers de un pool
  interno (`ProcessPoolExecutor`) y entre invocaciones externas
  simultáneas — no depende de un proceso padre común.
- Verificado con `max_workers=2` en el smoke test: `process_id` distintos
  (22238, 22239) en los registros, índice sin corrupción pese a escritura
  concurrente.
- `run_hash = sha256(seed:n_runs:W_sha:A_observed)` — determinístico.
  La corrida completa incluía las 6 combinaciones del smoke test como
  subconjunto; el índice quedó con 100 entradas, no 106 — las 6
  coincidentes se deduplicaron solas por compartir `run_hash`, sin
  lógica extra para eso. Confirma que el hash captura identidad real,
  no solo un contador de eventos.

---

## Resultado — confirma H (coupon-collector), con n=10 seeds por punto

| n_runs | mean(A_observed) | min | max | seeds |
|--------|------------------:|----:|----:|------:|
| 10     | 9.9               | 9   | 10  | 10    |
| 20     | 19.7              | 19  | 20  | 10    |
| 30     | 29.6              | 29  | 30  | 10    |
| 40     | 38.9              | 37  | 40  | 10    |
| 50     | 48.4              | 46  | 50  | 10    |
| 60     | 57.8              | 56  | 60  | 10    |
| 70     | 66.4              | 64  | 69  | 10    |
| 80     | 75.7              | 74  | 79  | 10    |
| 100    | 94.2              | 91  | 98  | 10    |
| 150    | 136.2             | 134 | 140 | 10    |

`mean(A_observed)/n_runs` se mantiene entre 0.90 y 1.00 en todo el rango
— nunca cae, nunca se estabiliza por debajo. A n_runs=150, captura 90.8%
en promedio. El rango min-max por punto es angosto (ej. en n_runs=150:
134–140, spread de 6 sobre una media de 136) — **el patrón no es un
artefacto de un seed particular**: los 10 seeds coinciden en la forma de
la curva, solo varían en el detalle fino.

Esto reproduce, con base estadística más amplia, lo ya encontrado en
`REG_n_runs_sweep_armstrong_v1.md` §Hallazgos H2 (ahí con un único seed
por valor de `n_runs`, sobre corridas completas de 20 evaluaciones
Armstrong en vez de una llamada aislada a `_count_attractors`). Coincide
en dirección y en magnitud aproximada (crecimiento ~1:1, sin saturar
hasta n_runs=150–200).

---

## Lo que este módulo NO establece

- No verifica H2 de `REG_n_runs_sweep_armstrong_v1.md` (si `A0` sobre W
  sola y `A_actual` sobre W+Δ_r crecen a tasas distintas) — el módulo
  puede llamar `_count_attractors()` sobre ambos por separado, pero esta
  corrida solo evaluó W sola. Queda para una extensión, como ya estaba
  planeado (§H2 de la task, "no incluir en v1").
- No interpreta si esto es "correcto" o "incorrecto" para el umbral
  `D_CKM_THRESHOLD=0.40` — eso es una decisión de diseño posterior, no
  parte del alcance de este módulo (`NO agrega lógica de threshold`).

---

## Estado

- Módulo, datos y REG pendientes de commit — mismo criterio que
  `process/n_runs_sweep/`: lo que este REG cita tiene que ser auditable.
- `.gitignore` actualizado: `process/experiments/stochastic_eval/*.lock`
  (coordinación efímera, no evidencia).
- Tests: `tests/test_coco.py` 28/28, `tests/test_monitor_services.py`
  35/35, `tests/test_firma_ckm.py` 10/10, `tests/test_w_version.py`
  9/9 — 82/82 combinado, sin regresiones.

---

## Archivos relacionados

- `experiments/stochastic_attractor_eval.py` — módulo
- `process/experiments/stochastic_eval/` — datos crudos
- `registers/REG_n_runs_sweep_armstrong_v1.md` — hallazgo original, single-seed
- `iap_chatroom/tests/TASK_stochastic_attractor_eval_v5.md` — spec ejecutada
- `services/coco.py` — `_count_attractors()` (sin modificar)
- `services/firma_ckm.py` — `_sha256()` (reusado)

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
