# TASK_h2_a0_vs_aactual_v4.md
*Ago 2026 — gadanin.delamor + Claude Code*

*v4 changes from v3 — Paso 0 ejecutado, diseño final:*
*— fourforums descartado para esta corrida (SQL vive en el codespace*
*  `ckmdatasets`, no en `ckm`) — se posterga, no se investiga acá.*
*— Fuente real: `process/iap/corpus_state.json.bak_*` — ~29 casos*
*  reales de la serie IAP (0.4 a 0.14), cada uno con texto completo,*
*  no truncado (a diferencia de `monitor_trajectory.jsonl.bak_*`, que*
*  trunca a 80 chars — por eso se usa el corpus_state, no el trajectory).*
*— Dos ejes de "seed" separados: `case_id` (qué camino real — indexa*
*  entre los casos disponibles, cada uno con su propio W y su propio*
*  Δ_r final) y `count_seed` (el seed de `_count_attractors`, para ver*
*  si el sesgo del instrumento es robusto entre casos).*
*— Un Δ_r por caso (el estado final real de esa conversación), no*
*  checkpoints artificiales dentro de un camino — cada camino se*
*  camina completo, hasta donde realmente llegó.*

---

## Objetivo

Verificar H2 (`REG_n_runs_sweep_armstrong_v1.md`): ¿`A0` (sobre W sola)
y `A_actual` (sobre W+Δ_r) crecen a tasas distintas con `n_runs`?

---

## Fuente de datos — 10 casos reales de la serie IAP

```
process/iap/corpus_state.json.bak_1784524220_caso04
process/iap/corpus_state.json.bak_1784527004_caso04a
process/iap/corpus_state.json.bak_1784529369_caso04b
process/iap/corpus_state.json.bak_1784594633_caso06_run1
process/iap/corpus_state.json.bak_1784595012_caso06_run2
process/iap/corpus_state.json.bak_1784601161_caso07
process/iap/corpus_state.json.bak_1784670163_caso08_run2
process/iap/corpus_state.json.bak_1784685610_caso09_run2
process/iap/corpus_state.json.bak_1784776454_caso10_run1
process/iap/corpus_state.json.bak_1784777737_caso11_run1
```

`case_id` 0–9 indexa esta lista en orden. Cada archivo trae `texts`
(completo, real, orden cronológico real de esa conversación), `nodes`,
`W` ya construida por `CorpusService` en su momento.

Por cada caso: reconstruir `W_case` desde `texts` (mismo proceso que
originalmente — `CorpusService.ingest(texts)`), luego generar
`Delta_r_case` corriendo `MonitorService` (**sin thermostat**) sobre
esos mismos `texts` en su orden real, Δ_r libre sin compresión STOP.
Es el estado final real de esa conversación — no un checkpoint
artificial a mitad de camino.

---

## Diseño — `run_pair` (sin cambios de v2/v3)

```python
def run_pair(W, Delta_r, seed, n_runs) -> dict:
    """Compara A0 (W sola) vs A_actual (W+Delta_r), mismo seed/n_runs."""
```

## Sweep — dos ejes

```
case_id     : 0..9        (qué camino real — W y Δ_r cambian juntos)
count_seed  : 0..9        (seed de _count_attractors — fijo entre casos)
n_runs      : [10,30,100,300,1000,3000,10000]  (checkpoints logarítmicos)
```

10 × 10 × 7 = 700 combinaciones máximo, menos por el corte de
CONVERGENCIA_REAL (ver abajo).

## Criterios de evento (sin cambios de v2/v3)

**CONVERGENCIA_REAL** (corta la corrida para esa combinación
case_id×count_seed): pendiente local < 0.10, evaluada en `A0` y
`A_actual` por separado.

**RIESGO_CONFOUND** (marcador): ratio `A_observed/n_runs` < 0.95,
primera vez que cruza.

**COLAPSO** (marcador, solo H2): `|A_actual-A0|/A0` < 0.02, primera
vez que cruza. Umbral tentativo.

## Paso previo — distribución de `fi` por caso

Antes del sweep de cada caso: calcular `fi` (row-sums de `W_case`) y
registrar la forma de la distribución (CV, skewness) junto al
resultado — predicción cualitativa de qué tan rápido debería saturar
`representación`, comparable después contra el comportamiento real de
`A0`/`A_actual` de ese caso.

---

## Scope — lo que NO hace

- **NO modifica** `coco.py`, `monitor_service.py`, `run_one()` existente
- **NO usa thermostat/STOP** al generar Δ_r
- **NO reordena** ningún caso — texto real, orden real
- **NO toca** fourforums/`ckmdatasets` — queda para otra task, en el
  otro ambiente, si hace falta más adelante

---

## Criterio de éxito

```bash
python3 tests/test_coco.py
python3 tests/test_monitor_services.py
python3 tests/test_firma_ckm.py
python3 tests/test_w_version.py
```
→ 82/82, sin regresiones.

Smoke mínimo: 2 casos, `count_seed=[0,1]`, checkpoints `[10,30,100]` →
`run_pair` con `A_actual != A0` en algún caso, eventos evaluados y en
el JSONL.

---

## Convenciones de archivos

- **Módulo**: extensión de `experiments/stochastic_attractor_eval.py`
- **Outputs**: `process/experiments/stochastic_eval/h2_*`
- **Commit**: sí — corrida completa, mismo criterio que el resto
- **REG**: `registers/REG_h2_a0_vs_aactual_v1.md` — tras corrida completa

---

## NO modificar

- `services/coco.py`, `services/monitor_service.py`
- `run_one()` en `stochastic_attractor_eval.py`
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
