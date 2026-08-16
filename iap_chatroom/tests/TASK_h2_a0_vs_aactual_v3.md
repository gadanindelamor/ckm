# TASK_h2_a0_vs_aactual_v3.md
*Ago 2026 — gadanin.delamor + Claude Code*

*v3 changes from v2:*
*— Fuente de Δ_r cambia: no más `WARMUP_TEXTS`/Armstrong ("WARM es*
*  sesgo" — corpus definicional, no dominio real). Pasa a un corpus*
*  real (fourforums/CreateDebate). El seed elige QUÉ camino real mirar*
*  (qué hilo de conversación real que ya ocurrió), no reordena nada —*
*  "el orden de los textos es exactamente el camino".*
*— Agrega Paso 0 nuevo: verificar si hay texto real de posts de*
*  fourforums accesible (no solo estadísticas agregadas por par autor)*
*  antes de comprometerse al diseño — bloqueante si no existe.*
*— Agrega paso previo al sweep: calcular distribución de `fi`*
*  (frecuencia marginal, row-sums de W) del corpus elegido ANTES de*
*  correr el sweep completo — sirve de predicción de dónde satura*
*  `representación(k)`, comparable después contra el resultado real.*
*— Resto igual a v2 (run_pair, checkpoints logarítmicos, los tres*
*  criterios de evento).*

---

## Objetivo

Verificar H2 (`REG_n_runs_sweep_armstrong_v1.md`, "propuesto, no verificado"):

> Si `A0` (baseline, sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
> tasas distintas con `n_runs`, `D_ckm` hereda ese sesgo estructural.

---

## Paso 0 — verificación previa OBLIGATORIA, nueva en v3

**Antes de construir nada, reportar hallazgos:**

```bash
find . -iname "*fourforums*" | grep -v ".json$\|.py$\|.png$"
ls experiments/*.sql 2>/dev/null
grep -rn "post_text\|body\|raw_text" experiments/fourforums_pipeline_v8h.py | head -20
```

Pregunta a responder: ¿hay texto real de posts de fourforums accesible
(no solo `neg_pairs_config_fourforums_v8h.json`, que trae `quoter`,
`responder`, `n`, `mean_da`, `weight` — estadísticas agregadas por par
de autores, sin el texto de ningún post individual)?

**Si NO hay texto real accesible**: no se puede correr `MonitorService`
sobre posts reales de fourforums para generar Δ_r — esa ruta queda
bloqueada. Alternativas a decidir con delamor, no a inventar:
(a) usar CreateDebate si tiene texto accesible, (b) reconstruir texto
desde el SQL original si está disponible, (c) otra fuente real que sí
tenga texto.

**Si SÍ hay texto real accesible**: seguir con el diseño de abajo.

---

## Diseño — `run_pair` (igual a v2, sin cambios)

```python
def run_pair(W, Delta_r, seed, n_runs) -> dict:
    """
    Compara A0 (sobre W sola) vs A_actual (sobre W+Delta_r), mismo
    seed y n_runs para ambos — comparación pareada.
    """
```

Instancia un único `COCO(W=W, seed=seed, n_runs=n_runs)`, llama
`_count_attractors(W)` y `_count_attractors(W + Delta_r)` por separado.
Reporta `seed, n_runs, A0, A_actual, delta, D_ckm_instante, W_sha,
Delta_r_sha, run_hash`. Sin interpretación de zona/threshold.

---

## Fuente de Δ_r — corpus real, seed elige el camino

**No usar `WARMUP_TEXTS`/`TEXTS` (Armstrong)** — son oraciones
definicionales sobre CKM, no dominio real, y ya vimos que satura
en 2 textos (poca profundidad de pares rechazables).

**Diseño**: `seed` selecciona **qué hilo de conversación real** mirar
— por ejemplo, un autor específico y su secuencia real de respuestas
(orden cronológico real, no barajado). Distintos seeds → distintos
hilos reales que ya existieron, cada uno con su propio orden intacto.
Los checkpoints se toman en los puntos reales de ese camino según fue
caminado — no en índices reordenados ni sintéticos.

Correr `MonitorService` real (**sin thermostat** — Δ_r libre, sin
compresión STOP, para no mezclar el efecto de H2 con el de
OPERADOR_STOP_COCO) sobre ese hilo real, capturando `monitor._Delta_r.copy()`
en los checkpoints logarítmicos definidos abajo.

---

## Paso previo al sweep — distribución de `fi` como predicción

Antes de correr el sweep completo sobre un hilo real elegido:

1. Calcular `fi` (row-sums de W, frecuencia marginal por nodo) del
   corpus resultante.
2. Con esa distribución, predecir cualitativamente la forma esperada
   de `representación(k)`: distribución muy sesgada (pocos nodos de
   `fi` alto dominando) → saturación rápida esperada, `k*` chico.
   Distribución pareja → cola larga esperada, `k*` grande.
3. Correr el sweep real.
4. Comparar la predicción cualitativa (paso 2) contra el resultado
   real (paso 3) — reportar si coincidieron o no, sin forzar que
   coincidan.

Esto no reemplaza el sweep — es una predicción a registrar y
contrastar, no un atajo para no correrlo.

---

## Checkpoints — logarítmicos hasta 10.000 (igual a v2)

```
n_runs_checkpoints = [10, 30, 100, 300, 1000, 3000, 10000]
```

## Criterios de evento (igual a v2)

**CONVERGENCIA_REAL** (corta la corrida): pendiente local entre
checkpoints consecutivos < 0.10, evaluada en `A0` y `A_actual` por
separado.

**RIESGO_CONFOUND** (marcador, no corta): ratio `A_observed/n_runs`
< 0.95, primera vez que cruza.

**COLAPSO** (marcador, no corta, solo H2): `|A_actual - A0| / A0`
< 0.02, primera vez que cruza. Umbral tentativo, sin calibrar todavía.

Los tres se registran como campo `events` en cada checkpoint del JSONL.

---

## Scope — lo que NO hace

- **NO modifica** `coco.py`, `run_one()` existente, ningún archivo probado
- **NO interpreta** más allá de los tres criterios de evento y la
  comparación predicción-vs-real de `fi`
- **NO usa thermostat/STOP** en la generación de Δ_r
- **NO reordena** ningún hilo real — el orden es el camino, no un
  parámetro
- **NO asume** que hay texto real de fourforums accesible — eso lo
  decide el Paso 0

---

## Criterio de éxito

```bash
python3 tests/test_coco.py
python3 tests/test_monitor_services.py
python3 tests/test_firma_ckm.py
python3 tests/test_w_version.py
```
→ 82/82, sin regresiones.

Paso 0 completo y reportado antes de cualquier otra cosa. Si bloquea,
la task se detiene ahí — no se improvisa una fuente de Δ_r distinta
sin decidirlo con delamor.

Smoke mínimo (solo si Paso 0 no bloquea): 1 hilo real, checkpoints
`[10,30,100]` → `run_pair` con `A_actual != A0` en algún caso, los
tres criterios evaluados y en el JSONL, predicción de `fi` registrada
junto al resultado real.

---

## Convenciones de archivos

- **Módulo**: extensión de `experiments/stochastic_attractor_eval.py`
- **Outputs**: `process/experiments/stochastic_eval/h2_*`
- **Commit**: sí, mismo criterio que v5 de la task base — lo que el
  REG cite, auditable
- **REG**: `registers/REG_h2_a0_vs_aactual_v1.md` — tras corrida completa

---

## NO modificar

- `services/coco.py`, `services/monitor_service.py`
- `run_one()` en `stochastic_attractor_eval.py`
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
