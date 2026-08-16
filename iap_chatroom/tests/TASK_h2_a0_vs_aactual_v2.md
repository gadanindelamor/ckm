# TASK_h2_a0_vs_aactual_v2.md
*Ago 2026 — gadanin.delamor + Claude Code*

*v2 changes from v1:*
*— n_runs pasa de lista fija [10..150] a checkpoints logarítmicos hasta*
*  10.000: [10, 30, 100, 300, 1000, 3000, 10000].*
*— Agrega tres criterios de evento evaluados en cada checkpoint:*
*  CONVERGENCIA (corta la corrida), RIESGO_CONFOUND (marcador),*
*  COLAPSO (marcador, solo H2). Ver sección "Criterios de evento".*

---

## Objetivo

Verificar H2 (`REG_n_runs_sweep_armstrong_v1.md`, "propuesto, no verificado"):

> Si `A0` (baseline, sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
> tasas distintas con `n_runs`, `D_ckm` hereda ese sesgo estructural.

`REG_stochastic_eval_v1.md` confirmó que `A(W)` sola crece ~1:1 con
`n_runs` sin saturar hasta 150 — no dice nada todavía sobre si el sesgo
afecta a `D_ckm`. Esta task compara `A(W)` contra `A(W+Δ_r)` en los
mismos puntos, extendiendo el rango hasta n_runs=10.000 para ver si la
curva de alguna de las dos (o ambas) eventualmente dobla.

---

## Contexto — lo que ya existe

- `experiments/stochastic_attractor_eval.py` — `run_one(W_eff, seed, n_runs)`
  ya instancia un `COCO` y llama `_count_attractors(W_eff)`. Acepta
  cualquier matriz NxN — no exige que sea la W de construcción (así lo
  usa `COCO.observe()` internamente: `W_eff = self.W + self._Delta`).
- No hay Δ_r real persistido como matriz completa en el repo — se genera
  corriendo la secuencia Armstrong una vez.
- `_count_attractors` arranca `np.random.default_rng(self._seed)` desde
  cero en cada llamada — los primeros k draws de n_runs=N son idénticos
  a los primeros k draws de n_runs=M>k, mismo seed. Los checkpoints se
  recomputan de forma independiente (no tracking interno) — el costo lo
  domina el checkpoint más grande, los chicos son baratos en comparación.
  No duplica lógica de `coco.py`.

---

## Diseño — `run_pair`

Nueva función en `experiments/stochastic_attractor_eval.py`, no toca `run_one`:

```python
def run_pair(W, Delta_r, seed, n_runs) -> dict:
    """
    Compara A0 (sobre W sola) vs A_actual (sobre W+Delta_r), mismo
    seed y n_runs para ambos — comparación pareada.
    """
```

Instancia un único `COCO(W=W, seed=seed, n_runs=n_runs)`, llama
`_count_attractors(W)` y `_count_attractors(W + Delta_r)` por separado. Reporta:

```
seed, n_runs
A0              int
A_actual        int
delta           int    # A_actual - A0
D_ckm_instante  float  # (A0 - A_actual) / A0 si A0 > 0
W_sha, Delta_r_sha, run_hash
```

Sin interpretación de zona/threshold en el campo — eso lo hacen los
criterios de evento (abajo), que son datos, no lógica de STOP.

---

## Checkpoints — logarítmicos hasta 10.000

```
n_runs_checkpoints = [10, 30, 100, 300, 1000, 3000, 10000]
```

Por cada `(Δ_r_snapshot, seed)`, se recorren los checkpoints en orden
creciente. En cada uno: correr `run_pair`, evaluar los tres criterios
de evento contra el checkpoint anterior de la misma combinación.

---

## Criterios de evento

### CONVERGENCIA_REAL — corta la corrida

- **Objeto**: que el umbral no dispare prematuramente.
- **Criterio**: pendiente local entre checkpoints consecutivos < 0.10.
- **Diseño**:
  ```
  pendiente = (A(n_k) - A(n_{k-1})) / (n_k - n_{k-1})
  ```
  Aplicado a `A0` y a `A_actual` por separado (pueden converger en
  puntos distintos — eso es justo lo que H2 pregunta). Si **cualquiera
  de las dos** cruza pendiente < 0.10 → evento `CONVERGENCIA`, se
  registra cuál (`A0`, `A_actual`, o ambas) y en qué checkpoint.
- **Efecto**: corta la corrida para esa combinación — no sigue a los
  checkpoints mayores. Es el ahorro de cómputo real que motiva esto.

### RIESGO_CONFOUND — marcador, no corta

- **Objeto**: marcar dónde se sale de la zona n_runs≈A_observed.
- **Criterio**: ratio `A_observed/n_runs` < 0.95.
- **Diseño**: evaluado en `A0` y `A_actual` por separado en cada
  checkpoint. Primera vez que cruza por debajo → evento
  `RIESGO_CONFOUND_SALIDA`, registrando cuál serie y en qué checkpoint.
- **Efecto**: no corta — sigue ejecutando los checkpoints siguientes igual.

### COLAPSO — marcador, no corta, solo H2

- **Objeto**: detectar cuándo el instrumento deja de distinguir W de W+Δ_r.
- **Criterio**: `|A_actual - A0| / A0` < 0.02.
- **Diseño**: solo tiene sentido en `run_pair` (compara las dos series
  entre sí, no cada una contra n_runs). Evaluado en cada checkpoint.
  Si cruza por debajo → evento `COLAPSO_SENAL`.
- **Efecto**: no corta — no se asume monotonía (podría "recolapsar" o
  no, se registra sin interpretar). Umbral tentativo — sin datos
  previos de H2 para calibrarlo, puede necesitar ajuste después de ver
  la primera corrida.

Los tres eventos se registran como campos adicionales en el JSONL de
cada checkpoint (`event: null | "CONVERGENCIA" | "RIESGO_CONFOUND_SALIDA" | "COLAPSO_SENAL"`,
puede haber más de uno por checkpoint) — no en un log separado.

---

## Fuente de Δ_r — real, no sintética, tres montos de acumulación

Correr la secuencia Armstrong (`WARMUP_TEXTS` + `TEXTS`, `CorpusService`
+ `MonitorService` reales, **sin thermostat** — Δ_r libre, sin
compresión STOP, para no mezclar el efecto de H2 con el de
OPERADOR_STOP_COCO). Capturar `monitor._Delta_r.copy()` en:

- t=0 (primera evaluación con rechazo)
- t=9 (punto medio)
- t=19 (Δ_r final, máxima acumulación)

---

## Scope — lo que NO hace

- **NO modifica** `coco.py`, `run_one()` existente, ningún archivo probado
- **NO interpreta** más allá de los tres criterios de evento ya definidos
  — sin conclusiones nuevas no especificadas en el output del módulo
- **NO usa thermostat/STOP** en la generación de Δ_r
- **NO asume monotonía** de RIESGO_CONFOUND ni COLAPSO — se registran,
  no se fuerza una narrativa sobre ellos

---

## Criterio de éxito

```bash
python3 tests/test_coco.py
python3 tests/test_monitor_services.py
python3 tests/test_firma_ckm.py
python3 tests/test_w_version.py
```
→ 82/82, sin regresiones.

Smoke mínimo: 1 snapshot de Δ_r, `seeds=[0,1,2]`, checkpoints
`[10,30,100]` (subconjunto chico) → verificar que:
- `run_pair` devuelve `A_actual != A0` para al menos algún caso
- los tres criterios de evento se evalúan y quedan en el JSONL
  (aunque no disparen con checkpoints tan chicos)
- si CONVERGENCIA dispara en algún caso de prueba, la corrida corta ahí
  y no sigue a checkpoints que no estaban en el subconjunto de prueba

---

## Convenciones de archivos

- **Módulo**: extensión de `experiments/stochastic_attractor_eval.py`
  (agrega `run_pair` + evaluación de eventos, no toca `run_one`)
- **Outputs**: `process/experiments/stochastic_eval/h2_*`
- **Commit**: sí, mismo criterio que v5 — lo que el REG cite, auditable
- **REG**: `registers/REG_h2_a0_vs_aactual_v1.md` — tras corrida completa

---

## NO modificar

- `services/coco.py`, `services/monitor_service.py`
- `run_one()` en `stochastic_attractor_eval.py`
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
