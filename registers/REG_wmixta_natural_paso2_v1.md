# REG_wmixta_natural_paso2_v1.md

*Sep 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Descripción

Paso 2 de `TASK_wmixta_paso2_natural_v1.md`: **régimen natural**.

Corpus: los **24 textos** del caso IAP `09_run2` — solo el texto, ni su Δ_r,
ni su W, ni su historia. `CorpusService` sin `force_w_pos` (default): rutea
por marcadores de oposición y produce **W con 56 pesos negativos / 66
positivos**. Es el ciclo natural de servicios, no una condición forzada.

Parámetros: `n_runs=50`, `seed=42`, `track_landscape=False`, 24 evaluaciones
por condición, 4 condiciones (uniform / weighted / boltzmann / sin
thermostat), estado aislado y reanudable.

`delta_A` calculado en el driver tras cada STOP —cuenta sobre `W + Δ_r` ya
comprimida, misma cuenta que COCO hace internamente, 1 relajación extra en
vez de 3. `coco.py` no fue modificado.

Datos: `process/experiments/wmixta_paso2_natural/result_natural_*.json`
Driver: `iap_chatroom/tests/test_wmixta_natural_paso2.py`

**Este REG registra los datos del régimen natural. No compara con Paso 3**
— indicación explícita de la TASK; esa comparación es tarea aparte.

---

## Paso 0 — verificación previa

- Driver del Paso 3 leído como referencia. El Paso 2 replica su estructura
  con tres cambios: `force_w_pos=False`, `OUT_DIR` propio, y el assert
  invertido (`(W<0).sum() > 0` — acá la W **debe** traer negativos).
- Bak verificado: `corpus_state.json.bak_1784685610_caso09_run2`, 24 textos,
  sha256 `315fec91c938f3ab…`, sin cambios en git desde 22 Jul. Es el mismo
  archivo que leyeron Paso 1 y Paso 3.
- Sin resultados previos de Paso 2 en `wmixta_paso2_natural/`.
- Restos de la corrida abortada del 31 Ago (8 de 24 evaluaciones,
  `n_runs=200`, `track_landscape=True`) **renombrados a `ABORTADA_*`** con
  un `ABORTADA_LEEME.md` que documenta hasta dónde llegó y con qué
  parámetros. Se preservan como traza, no como dato. Decisión de delamor:
  marcar, no borrar.

---

## A0 por modo — y el efecto de n_runs

| modo | A0 (n_runs=50) |
|---|---:|
| uniform | 31 |
| weighted | 26 |
| boltzmann | 32 |

Paso 1 midió **A0 = 58** para este mismo régimen con `n_runs=150`. La
diferencia se registra **sin corregir**, como pide la TASK: es el sesgo
`n_runs` ya documentado en `REG_stochastic_eval_v1/v2` — el conteo crece
con `n_runs` sin saturar.

Resolución de la grilla: con A0≈31 los pasos de D_ckm son de ~0.032. El
umbral 0.40 es alcanzable y quedan ~30 valores intermedios.

---

## Resultado

| modo | A0 | STOPs | A_final | D_ckm final | rango de α |
|---|---:|---:|---:|---:|---|
| uniform | 31 | **15**/24 | 4 | 0.8710 | 0.104 – 0.292 |
| weighted | 26 | **14**/24 | 4 | 0.8462 | 0.114 – 0.242 |
| boltzmann | 32 | **13**/24 | 6 | 0.8125 | 0.076 – 0.297 |
| sin thermostat | — | 0/24 | — | — | — |

Los tres modos con thermostat disparan STOP. α recorre casi toda la banda
`[ALPHA_MIN, ALPHA_MAX] = [0.05, 0.30]` — el α dinámico opera de verdad,
no queda fijo en un valor.

---

## delta_A por STOP — orden cronológico

**uniform** (15 STOPs, en i = 5, 7, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 21, 22, 23):
```
[18, 28, 20, 14, 11, 21, 19, 29, 22, 13, 25, 20, 20, 31, 31]
```

**weighted** (14 STOPs, en i = 5, 7, 8, 10, 11, 12, 13, 14, 15, 18, 19, 21, 22, 23):
```
[15, 24, 32, 22, 20, 21, 23, 11, 33, 26, 20, 19, 28, 27]
```

**boltzmann** (13 STOPs, en i = 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 18, 21, 23):
```
[11, 15, 20, 28, 20, 19, 30, 17, 22, 19, 28, 25, 22]
```

**42 STOPs en total, ningún `delta_A` negativo.** Mínimo +11, máximo +33.
Cada compresión recuperó atractores, en todos los casos y en los tres modos.

---

## Trayectoria de D_ckm — ciclos, no estado absorbente

`uniform`, D_ckm por evaluación (i = 0…23):
```
-0.323 -0.161 -0.194 -0.097  0.323  0.613  0.097  0.806
 0.548  0.419  0.323  0.548  0.613  0.548  0.839  0.548
 0.613  0.355  0.613  0.452  0.000  0.677  0.839  0.871
```

Zonas: `stable` en i=0..4, después alterna `deep`/`stable` — el campo cruza
el umbral en las dos direcciones repetidamente. i=20 vuelve a D_ckm = 0.000
exacto (A = A0 = 31) tras haber estado en 0.452.

`boltzmann` muestra los ciclos más marcados: A_actual pasa por **2** en
i=12 (D_ckm = 0.938) y vuelve a **37** en i=16 (D_ckm = −0.156), campo
expandido por encima de baseline.

`weighted` en i=16 llega a A = 43 con A0 = 26 → D_ckm = **−0.654**.

Los tres arrancan con D_ckm negativo (campo expandido) en las primeras 3–4
evaluaciones antes de que la acumulación empiece a destruir.

---

## Δ_r — el thermostat la mantiene acotada

| modo | i=0 | i=5 | i=12 | i=23 |
|---|---:|---:|---:|---:|
| sin thermostat | 2.0 | 70 | 250 | **632** |
| uniform | 2.0 | 70 | 53.1 | **62.1** |
| weighted | 2.0 | 70 | 47.7 | **63.0** |
| boltzmann | 2.0 | 33.5 | 46.0 | **75.9** |

Sin thermostat Δ_r crece monótona hasta 632. Con thermostat queda entre 62 y
76 al cierre — un orden de magnitud menos. Los tres modos divergen de la
serie sin thermostat desde el primer STOP.

---

## D_ckm del panel — con resolución en este régimen

Valores distintos por modo, sobre 24 evaluaciones:

| modo | n valores distintos | rango |
|---|---:|---|
| uniform | 16 | 0.000 … 0.675 |
| weighted | 14 | −0.025 … 0.600 |
| boltzmann | 15 | −0.050 … 0.600 |
| sin thermostat | 15 | 0.000 … 0.500 |

Los cuatro difieren entre sí. A diferencia del régimen anterior, acá los
tres modos comprimieron, y sus Δ_r divergen en soporte además de magnitud.

---

## Lo que este REG no establece

- **No compara con Paso 3.** Indicación de la TASK. Los datos del régimen
  forzado están en `REG_wmixta_forzado_paso3_v1.md`; ponerlos lado a lado es
  tarea aparte.
- **No dice cuál modo es mejor.** Los tres disparan, con conteos de STOP
  parecidos (15/14/13) y `delta_A` del mismo orden. Nada acá discrimina.
- **A0 no es estable respecto de `n_runs`** — 58 con 150, 26–32 con 50. Todo
  lo que dependa de A0 (D_ckm, la grilla, el piso) hereda esa dependencia.
- **`sin_thermostat` no es "el mismo instrumento sin COCO"**: usa la
  implementación propia de `_count_attractors` de MonitorService
  (`default_rng(0)`, sin modos). Es referencia, no cuarta condición de la
  misma serie.
- **Los ciclos `deep`/`stable` no están explicados.** Se registra que
  ocurren y que el campo se recupera por encima de baseline varias veces.
  Por qué la acumulación destruye y vuelve a construir en este corpus no se
  investigó.
- **Sin commit.**

---

## Archivos

- `iap_chatroom/tests/test_wmixta_natural_paso2.py` — driver reanudable
- `process/experiments/wmixta_paso2_natural/result_natural_*.json` — 4 condiciones
- `process/experiments/wmixta_forced_wpos/ABORTADA_*` — traza de la corrida interrumpida
- `iap_chatroom/tests/TASK_wmixta_paso2_natural_v1.md` — spec
- `registers/REG_wmixta_forzado_paso3_v1.md` — Paso 1 y Paso 3
- `registers/REG_stochastic_eval_v1.md`, `v2` — sesgo n_runs

---

*Sep 2026 — Codespace ckm — bash/Linux*
