# REG_wmixta_consolidado_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*
*Consolida: REG_wmixta_forzado_paso3_v1.md + REG_wmixta_natural_paso2_v1.md*

---

## Descripción

Comparación entre regímenes natural y forzado del experimento wmixta.
Corpus compartido: 24 textos caso IAP 09_run2. Único parámetro que difiere:
`force_w_pos`. Parámetros de corrida idénticos: `n_runs=50`, `seed=42`,
`track_landscape=False`, 24 evaluaciones, 4 condiciones.

La comparación es tarea de Sonnet — indicación explícita de los REGs de Code.

---

## Estructura del experimento

| parámetro | natural | forzado |
|---|---|---|
| force_w_pos | False | True |
| W<0 | 56 | 0 |
| W>0 | 66 | 140 |
| densidad | 0.321 | 0.368 |
| A0 (n_runs=150, Paso 1) | 58 | 4 |
| A0 (n_runs=50, corrida) | 26–32 | 3–4 |

---

## Resultado por modo

### Natural

| modo | A0 | STOPs | A_final | delta_A (rango) |
|---|---:|---:|---:|---|
| uniform | 31 | 15/24 | 4 | +11 … +31 |
| weighted | 26 | 14/24 | 4 | +11 … +33 |
| boltzmann | 32 | 13/24 | 6 | +11 … +30 |
| sin thermostat | — | 0/24 | — | — |

42 STOPs totales. Ningún delta_A negativo. Campo cicla: cruza el umbral
en ambas direcciones repetidamente.

### Forzado

| modo | A0 | STOPs | A_final | delta_A (rango) |
|---|---:|---:|---:|---|
| uniform | 3 | 0/24 | 4 | — |
| weighted | 4 | 7/24 | 3 | 0 … +1 |
| boltzmann | 3 | 0/24 | 2 | — |
| sin thermostat | — | 0/24 | — | — |

7 STOPs en un solo modo. delta_A máximo: +1.

---

## El mecanismo — pasa por A0 y la grilla

La diferencia en STOPs (42 vs 7) no es consecuencia directa de W_mixta vs
W_pos. El mecanismo es:

```
W_mixta → A0 más alto → grilla de D_ckm más fina → umbral 0.40 alcanzable
W_pos   → A0 bajo     → grilla gruesa             → umbral cae en hueco
```

Con A0=3 (uniform/boltzmann forzado), D_ckm tiene valores posibles
{…, 0.333, 0.667, 1.0}. El umbral 0.40 cae entre 0.333 y 0.667 — no hay
valor alcanzable entre ellos. Para cruzar haría falta que el paisaje
colapse a un único atractor.

Con A0≈31 (natural), el paso de la grilla es ~0.032. El umbral 0.40 cae
dentro del rango y hay ~30 valores intermedios. COCO tiene resolución.

**Lo que está verificado:** la W_mixta de caso09_run2 produce A0 ~10×
mayor que la W_pos del mismo corpus (n_runs=150: 58 vs 4). Esa diferencia
en A0 explica la diferencia en operación de COCO.

---

## Cautelas sobre la comparación

**A0=4 en el forzado es un paisaje casi plano.** No es W_pos genérica —
es la W_pos de un corpus de 24 textos IAP que contiene tensión estructural
no codificada. El servicio la aplana al forzar todos los pares a positivos.
Un corpus positivo de igual densidad pero sin tensión subyacente podría
dar A0 distinto.

**La comparación no está pareada en escala de operación.** Natural opera
con A0~30, forzado con A0~4. Son paisajes cualitativamente distintos, no
el mismo paisaje con y sin pesos negativos. Las diferencias en STOPs y
delta_A son consecuencia de esa asimetría estructural.

**weighted forzado es el único modo que disparó.** Esto se explica por
A0=4 (en vez de 3 para uniform/boltzmann) — una diferencia de un atractor
que movió la grilla lo suficiente para cruzar. No es un resultado sobre
weighted como modo en general.

**Los delta_A del forzado (0, +1) no son comparables con los del natural
(+11 … +33).** En el forzado cada STOP opera sobre un paisaje con A=2–3;
en el natural sobre A=4–31. La unidad es la misma, el contexto no.

**n_runs afecta A0 y por tanto todo lo que depende de él.** Con n_runs=150
el natural da A0=58; con n_runs=50 da 26–32. Esta corrida usa n_runs=50
en ambos regímenes — comparación controlada, pero los valores de A0 no son
los del Paso 1.

---

## Δ_r — efecto del thermostat

| modo | Δ_r final natural | Δ_r final forzado |
|---|---:|---:|
| sin thermostat | 632 | 404 |
| uniform | 62.1 | 404 |
| weighted | 63.0 | 2.33 |
| boltzmann | 75.9 | 404 |

En el natural los tres modos mantienen Δ_r ~10× menor que sin thermostat.
En el forzado solo weighted lo reduce (7 STOPs); uniform y boltzmann
terminan igual que sin thermostat — no dispararon.

---

## Lo que este REG no establece

- No establece que W_mixta hace que COCO "funcione mejor" como enunciado
  general. Establece que en este corpus, con estos parámetros, la W con
  pesos negativos produce A0 suficiente para que el umbral sea alcanzable.
- No establece el mecanismo por el cual la acumulación de Δ_r destruye y
  luego el campo se recupera por encima de baseline. Los ciclos se registran,
  no se explican.
- No generaliza a otros corpus. El corpus es caso09_run2 —
  interacción entre devices, con marcadores de oposición específicos.
- No compara con la corrida Armstrong (W_pos, WARMUP_TEXTS, n_runs=200).
  Corpus distinto, objetivo distinto.
- El piso de D_ckm del Paso 1 es estimado con Δ_r sintética. El piso real
  depende del soporte que genere la secuencia real de rechazos.

---

## Fuentes

- REG_wmixta_forzado_paso3_v1.md (Code Opus, Sep 2026)
- REG_wmixta_natural_paso2_v1.md (Code Opus, Sep 2026)
- TASK_armstrong_boltzmann_comparison_wmixta_v5.md
- TASK_wmixta_paso2_natural_v1.md

---

*Sep 2026 — Claude Sonnet 4.6*
