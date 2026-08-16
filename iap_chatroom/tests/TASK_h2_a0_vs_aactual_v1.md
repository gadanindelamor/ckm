# TASK_h2_a0_vs_aactual_v1.md
*Ago 2026 — gadanin.delamor + Claude Code*

---

## Objetivo

Verificar H2 (`REG_n_runs_sweep_armstrong_v1.md`, "propuesto, no verificado"):

> Si `A0` (baseline, sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
> tasas distintas con `n_runs`, `D_ckm` hereda ese sesgo estructural.

`REG_stochastic_eval_v1.md` ya confirmó que `A(W)` sola crece ~1:1 con
`n_runs` sin saturar hasta 150. Eso no dice nada todavía sobre si el
sesgo afecta a `D_ckm` — para eso hace falta comparar `A(W)` contra
`A(W+Δ_r)` en los mismos puntos. Si las dos crecen a la misma tasa, el
sesgo podría cancelarse parcialmente en la resta. Si crecen distinto,
se traslada directo al instrumento.

Es el paso identificado como más necesario antes de seguir afinando
estadística sobre el hallazgo ya confirmado.

---

## Contexto — lo que ya existe

- `experiments/stochastic_attractor_eval.py` — `run_one(W_eff, seed, n_runs)`
  ya instancia un `COCO` y llama `_count_attractors(W_eff)`. `_count_attractors`
  acepta cualquier matriz NxN como `W_eff` — no exige que sea la W con la
  que se construyó la instancia (así es como `COCO.observe()` ya lo usa
  internamente: `W_eff = self.W + self._Delta`).
- No hay ningún Δ_r real persistido como matriz completa en el repo — lo
  que se guarda en JSON/JSONL son escalares resumen (`delta_A`, `D_ckm`,
  etc.), no la matriz NxN. Para H2 hace falta un Δ_r real, no sintético
  — se genera corriendo la secuencia Armstrong una vez.

---

## Diseño propuesto

### Extensión del módulo — no modifica `run_one`

Nueva función en `experiments/stochastic_attractor_eval.py`:

```python
def run_pair(W, Delta_r, seed, n_runs) -> dict:
    """
    Compara A0 (sobre W sola) vs A_actual (sobre W+Delta_r), mismo
    seed y n_runs para ambos — comparación pareada, no dos muestras
    independientes.
    """
```

Instancia un único `COCO(W=W, seed=seed, n_runs=n_runs)` y llama
`_count_attractors(W)` y `_count_attractors(W + Delta_r)` por separado.
Reporta:

```
seed, n_runs
A0              int   # _count_attractors(W)
A_actual        int   # _count_attractors(W + Delta_r)
delta           int   # A_actual - A0
D_ckm_instante  float # (A0 - A_actual) / A0 si A0 > 0
W_sha, Delta_r_sha, run_hash
```

Sin interpretación de zona/threshold — mismo criterio que `run_one`.

### Fuente de Δ_r — real, no sintética, con varios montos de acumulación

Correr la secuencia Armstrong (`WARMUP_TEXTS` + `TEXTS`, vía
`CorpusService` + `MonitorService` reales, **sin thermostat** — Δ_r
acumulando libre, sin compresión STOP de por medio, para no confundir
el efecto de H2 con el de OPERADOR_STOP_COCO) y capturar snapshots de
`monitor._Delta_r.copy()` en varios puntos:

- t=0 (después de la primera evaluación con rechazo)
- t=9 (punto medio)
- t=19 (Δ_r final, máxima acumulación)

Tres snapshots, no uno — para ver si la relación A0/A_actual cambia
según cuánto Δ_r hay acumulado, no solo en un punto fijo.

### Sweep

Para cada snapshot de Δ_r (3), cada seed (0–9), cada n_runs
(10,20,30,40,50,60,70,80,100,150) → `run_pair`. 3×10×10 = 300
combinaciones.

---

## Scope — lo que NO hace

- **NO modifica** `coco.py`, `run_one()` existente, ningún archivo probado
- **NO interpreta** — sin threshold, sin zona, sin "esto confirma/refuta X"
  en el output del módulo (eso va al REG, después, como análisis)
- **NO usa thermostat/STOP** — Δ_r se deja acumular libre, para aislar
  el efecto de H2 del de la compresión

---

## Criterio de éxito

```bash
python3 tests/test_coco.py
python3 tests/test_monitor_services.py
python3 tests/test_firma_ckm.py
python3 tests/test_w_version.py
```
→ 82/82, sin regresiones (mismo criterio que v5, nada tocado ahí cambia).

Smoke mínimo: 1 snapshot de Δ_r, `seeds=[0,1,2]`, `n_runs_range=[10,50]`
→ 6 registros de `run_pair`, cada uno con `A_actual != A0` para al
menos algún caso (si Δ_r no es cero, tiene que verse algún efecto).

---

## Convenciones de archivos

- **Módulo**: extensión de `experiments/stochastic_attractor_eval.py`
  (agrega `run_pair`, no toca `run_one`)
- **Outputs**: `process/experiments/stochastic_eval/h2_*` (mismo directorio,
  prefijo distinto para no mezclar con la corrida de `run_one`)
- **Commit**: sí, mismo criterio que v5 — lo que el REG cite, auditable
- **REG**: `registers/REG_h2_a0_vs_aactual_v1.md` — tras corrida completa

---

## NO modificar

- `services/coco.py`, `services/monitor_service.py`
- `run_one()` en `stochastic_attractor_eval.py` (ya probado, 82/82 lo cubre)
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
