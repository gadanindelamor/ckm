# REG_h2_a0_vs_aactual_v1.md

*Ago 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Descripción

Verificación de H2 (`REG_n_runs_sweep_armstrong_v1.md`, "propuesto, no
verificado"): ¿`A0` (sobre W sola) y `A_actual` (sobre W+Δ_r) crecen a
tasas distintas con `n_runs`? Ejecutada vía
`TASK_h2_a0_vs_aactual_v4.md`, módulo `experiments/stochastic_attractor_eval.py`
(`run_pair`, `run_h2_case`, `build_case_w_and_delta_r`).

Fuente de datos: 10 casos reales de la serie IAP (0.4–0.12), texto
completo real (no truncado), Δ_r generado corriendo `MonitorService`
sin thermostat sobre ese texto en su orden real — no `WARMUP_TEXTS`
("WARM es sesgo", ya descartado), no reordenado, no sintético.

Datos: `process/experiments/stochastic_eval/h2_runs_run1_20260815T234700.jsonl`
(238 registros), `h2_index_run1_20260815T234700.json` (238 entradas).
Etiquetado `run1` deliberado — el ejercicio se va a repetir, nada de
esta corrida se pisa.

---

## Los 10 casos reales usados

| case_id | archivo fuente | n_texts | Δ_r.sum() | Δ_r_sha8 |
|---|---|---|---|---|
| 0 | `corpus_state.json.bak_1784524220_caso04` | 8 | 124.0 | b22fe770 |
| 1 | `corpus_state.json.bak_1784527004_caso04a` | 6 | 6.0 | 8b999925 |
| 2 | `corpus_state.json.bak_1784529369_caso04b` | 9 | 320.0 | 28c62c4f |
| 3 | `corpus_state.json.bak_1784594633_caso06_run1` | 4 | 70.0 | 52898c2a |
| 4 | `corpus_state.json.bak_1784595012_caso06_run2` | 8 | 256.0 | 26fa15bb |
| 5 | `corpus_state.json.bak_1784671093_caso05_replica1` | 4 | 32.0 | b326bdc7 |
| 6 | `corpus_state.json.bak_1784778701_caso10_run1` | 7 | **0.0** | 5a312281 |
| 7 | `corpus_state.json.bak_1784777737_caso11_run1` | 12 | 220.0 | 1edb20f9 |
| 8 | `corpus_state.json.bak_1784685610_caso09_run2` | 24 | 632.0 | cc14b088 |
| 9 | `corpus_state.json.bak_1784839643_caso12_run2` | 9 | 60.0 | 0bb3fd5f |

`case_id=6` es un control natural: Δ_r=0 exacto — ese caso no tuvo
ningún rechazo real. Todos N=20 (mismo tamaño de vocabulario extraído
por caso, coincidencia del corpus, no impuesto).

---

## Resultado — 3 casos convergen a n_runs=30, 6 no distinguen, uno
## (case_id=9) traza suficiente para responder H2 directamente

De los 10 casos, **9 dispararon `CONVERGENCIA` ya en el segundo
checkpoint (n_runs=30)** — pendiente < 0.10 casi de inmediato. Muy
distinto de `WARMUP_TEXTS`, que no convergía ni a n_runs=150. Corpus
reales, chicos (4–24 textos), con vocabulario más acotado, saturan
mucho antes.

`case_id=9` (el más largo, 24 textos) fue el único con rango
suficiente para trazar la curva completa hasta n_runs=3000:

| n_runs | A0 | A_actual | delta | D_ckm | ratio_A0 | ratio_A_actual |
|---|---|---|---|---|---|---|
| 10 | 8 | 7 | −1 | 0.1250 | 0.800 | 0.700 |
| 30 | 16 | 14 | −2 | 0.1250 | 0.533 | 0.467 |
| 100 | 37 | 31 | −6 | 0.1622 | 0.370 | 0.310 |
| 300 | 75 | 67 | −8 | 0.1067 | 0.250 | 0.223 |
| 1000 | 179 | 137 | −42 | 0.2346 | 0.179 | 0.137 |
| 3000 | 318 | 239 | −79 | 0.2484 | 0.106 | 0.080 |

---

## Respuesta a H2 — parcial, no total

**El sesgo estructural existe en ambas series por separado.** Ni `A0`
ni `A_actual` convergen — ambas siguen creciendo hasta n_runs=3000
(318 y 239 respectivamente, sin señal de techo). Es el mismo sesgo de
`_count_attractors` ya confirmado en `REG_stochastic_eval_v1.md`, ahora
visto en las dos series a la vez.

**Pero `D_ckm` no hereda el sesgo completo — se cancela parcialmente.**
`A0` crece 318/8 ≈ 40x entre n_runs=10 y 3000. `A_actual` crece
239/7 ≈ 34x en el mismo rango. Si el sesgo fuera independiente en cada
serie, `D_ckm = (A0-A_actual)/A0` heredaría esa magnitud de deriva. En
cambio, `D_ckm` va de 0.125 a 0.248 — duplica, no se dispara 40x. La
resta cancela la mayor parte del sesgo compartido (ambas series crecen
por el mismo mecanismo coupon-collector, sobre la misma `W_eff` base),
pero no todo — queda una deriva real de ~2x en el rango observado.

**Conclusión de H2**: la hipótesis original decía "si A0 y A_actual
crecen a tasas distintas, D_ckm hereda ese sesgo" — la premisa es
cierta (crecen a tasas *ligeramente* distintas, `ratio_A0 > ratio_A_actual`
en todos los checkpoints), y la consecuencia también, pero *atenuada*:
D_ckm no es invariante a n_runs, pero es mucho más estable que
cualquiera de las dos series que lo componen. `D_CKM_THRESHOLD=0.40`
sigue siendo sensible a n_runs (0.125 a n_runs=10 vs 0.248 a
n_runs=3000 — casi el doble, podría cruzar o no cruzar el umbral según
dónde se mida), pero no con la magnitud catastrófica que tendría si el
sesgo no se cancelara en absoluto.

---

## Los otros 9 casos — evidencia complementaria, un solo checkpoint útil

Con convergencia a n_runs=30, solo hay un punto de comparación real
por caso (`case_id=6`, Δ_r=0, control: `delta=0` exacto, como debía
ser). Los demás muestran `D_ckm` en n_runs=30 entre 0.0 y 0.92 — rango
amplio, consistente con que la magnitud de Δ_r real (6.0 a 632.0 según
el caso) produce grados de "degradación" muy distintos, cosa esperable
y no parte de lo que H2 pregunta. No se puede trazar la forma de la
curva en estos 9 — saturan antes de que haya suficientes checkpoints
para verlo.

**Implicación de diseño para la repetición**: si se repite el
ejercicio, casos más largos (más texto real, más rechazos) van a dar
más rango para ver la curva completa — `case_id=9` (24 textos) fue el
único suficientemente largo. Elegir casos con más texto real
aportaría más que agregar más seeds de conteo sobre casos cortos que
ya convergieron.

---

## Eventos registrados

```
RIESGO_CONFOUND_SALIDA: 110
COLAPSO_SENAL:           36
CONVERGENCIA:           100
```

`COLAPSO_SENAL` (|A_actual-A0|/A0 < 0.02) disparó 36 veces —
principalmente en los casos con Δ_r chico o cero, donde A0≈A_actual
desde el principio. Consistente con su definición: el instrumento deja
de distinguir W de W+Δ_r cuando Δ_r es chico relativo a la estructura
de W.

---

## Predicción por distribución de `fi` — registrada, no analizada en profundidad

Cada registro incluye `fi_prediction` (mean, std, CV, skewness de las
row-sums de W_case). No se cruzó formalmente contra la velocidad de
convergencia observada en esta pasada — queda como trabajo pendiente
si se repite el ejercicio con más casos largos.

---

## Trazabilidad — reproducible

```python
from stochastic_attractor_eval import build_case_w_and_delta_r, run_h2_case
W, Delta_r, n_texts = build_case_w_and_delta_r(
    "process/iap/corpus_state.json.bak_1784839643_caso12_run2"  # case_id=9
)
run_h2_case(W, Delta_r, case_id=9, count_seeds=list(range(10)),
            checkpoints=[10,30,100,300,1000,3000,10000],
            jsonl_path=..., index_path=...)
```

`_smoke_corpus_state.json`, `runs_42e76ebc_*`, `index_42e76ebc.json` en
el mismo directorio son de la task anterior (`TASK_stochastic_attractor_eval_v5.md`),
sin relación con H2 — no confundir.

`h2_delta_snapshots/delta_r_t{0,9,19}.npy` son de un diseño anterior
de esta misma task (v2, sobre `WARMUP_TEXTS`, descartado por sesgo de
ese corpus) — preservados como traza del proceso, no usados en este
resultado.

---

## Estado

- 82/82 tests, sin regresiones
- `run1` — primera ejecución. Se va a repetir; el nombrado con
  timestamp asegura que la próxima corrida no pisa esta
- Pendiente, explícito: casos más largos para trazar la curva completa
  en más de un caso; cruzar `fi_prediction` contra velocidad de
  convergencia real

---

## Archivos relacionados

- `experiments/stochastic_attractor_eval.py` — `run_pair`, `run_h2_case`, `build_case_w_and_delta_r`
- `process/experiments/stochastic_eval/h2_runs_run1_20260815T234700.jsonl`
- `process/experiments/stochastic_eval/h2_index_run1_20260815T234700.json`
- `iap_chatroom/tests/TASK_h2_a0_vs_aactual_v4.md` — spec ejecutada
- `registers/REG_stochastic_eval_v1.md` — hallazgo base (A(W) sola, sesgo confirmado)
- `registers/REG_n_runs_sweep_armstrong_v1.md` — H2 propuesta original
- `process/iap/corpus_state.json.bak_*` — los 10 casos fuente

---

*Ago 2026 — gadanin.delamor + Claude Code*
*Codespace ckm — bash/Linux*
