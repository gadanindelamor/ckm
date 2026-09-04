# REG_wmixta_forzado_paso3_v1.md

*Sep 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Descripción

Paso 1 y Paso 3 de `TASK_armstrong_boltzmann_comparison_wmixta_v5.md`.
Corpus: los **24 textos** del caso IAP `09_run2` — solo el texto, ni su Δ_r,
ni su W, ni su historia.

Régimen **forzado**: `CorpusService(force_w_pos=True)` saltea el ruteo por
marcadores de oposición; todos los pares van a `pos_counts`, con lo cual
`W = (pos + neg)/max`. El corpus conserva su tensión, el servicio no la
codifica. **No es un estado alcanzable por el ciclo natural de servicios.**
La W queda marcada en la traza: `causal_event="rebuild_debug_force_w_pos"`,
`forced_w_pos: true` en el estado persistido.

Objetivo declarado: **completitud** — observar cómo funciona COCO y cómo
caen los STOPs en este régimen. **No es comparación** con corridas
anteriores.

El Paso 2 (régimen natural) queda **postergado** por decisión de delamor —
razón de recursos, no de diseño.

Datos: `process/experiments/wmixta_forzado_paso3/result_forzado_*.json`
Driver: `iap_chatroom/tests/test_wmixta_forzado_paso3.py`
Parámetros: `n_runs=50`, `seed=42`, `track_landscape=False`, 24 evaluaciones.

---

## Paso 1 — A0 por régimen (n_runs=150, seed=42)

Protocolo del script de calibración (`experiments/calibrate_W_mixta.py`):
ρ~U(0.3,0.7), empate conserva σ. **Verificado idéntico** al
`_count_attractors` de COCO en los dos regímenes — es el mismo protocolo,
no dos parecidos.

| régimen | N | W<0 | W>0 | densidad | **A0** | h=0 |
|---|---:|---:|---:|---:|---:|---:|
| natural | 20 | 56 | 66 | 0.321 | **58** | 16.2% |
| forzado | 20 | 0 | 140 | 0.368 | **4** | 7.6% |

Los pesos negativos multiplican por ~14 los atractores accesibles. Medido
por servicio, sin elegir pares a mano.

Piso estimado de D_ckm (perturbando W con Δ_r sintética de magnitud 1e−9 y
el soporte del propio corpus — **estimación, no piso medido**):

| régimen | A0 | A con Δ_r mínima | D_ckm piso | vs threshold 0.40 |
|---|---:|---:|---:|---|
| natural | 58 | 66 | **−0.1379** | debajo |
| forzado | 4 | 2 | **+0.5000** | encima |

---

## Paso 3 — resultado

| modo | A0 | STOPs | A_final | D_ckm final | delta_A por STOP |
|---|---:|---:|---:|---:|---|
| uniform | 3 | **0**/24 | 4 | −0.3333 | — |
| weighted | 4 | **7**/24 | 3 | +0.25 | `[0, 1, 0, 1, 0, 0, 1]` |
| boltzmann | 3 | **0**/24 | 2 | +0.3333 | — |
| sin thermostat | — | 0/24 | — | — | — |

**Solo `weighted` produce STOPs.** `uniform` y `boltzmann` no disparan
ninguno en 24 evaluaciones y permanecen en zona `stable` de punta a punta.

---

## Hallazgo — el umbral cae en un hueco de los valores alcanzables

`D_ckm = (A0 − A)/A0` con A entero. En un paisaje de este tamaño **D_ckm
está cuantizado**, y la grilla la fija A0:

| A0 | valores de D_ckm alcanzables | primero por encima de 0.40 | requiere |
|---:|---|---|---|
| 3 (uniform, boltzmann) | …, −0.333, 0, **0.333**, 0.667, 1.0 | 0.667 | A = 1 |
| 4 (weighted) | …, −0.25, 0, 0.25, **0.5**, 0.75, 1.0 | 0.5 | A = 2 |

Con A0=3 el valor inmediatamente superior a 0.333 es **0.667**, que exige
que el paisaje colapse a **un solo atractor**. El mínimo observado en las
24 evaluaciones fue A=2. Con A0=4, en cambio, A=2 da 0.5 y cruza — y A=2
ocurre siete veces.

**`uniform` y `boltzmann` no es que hayan encontrado el campo estable: no
tenían cómo cruzar el umbral.** `D_CKM_THRESHOLD = 0.40` cae entre dos
valores que la grilla de A0=3 no contiene.

Esto no es un defecto del corpus ni del umbral por separado: es la relación
entre los dos. Y el modo de muestreo de σ₀ es lo que fija A0 — es decir,
**el modo decide la grilla, y la grilla decide si COCO puede actuar**.

Nota conexa: A0 depende de `n_runs` (sesgo ya registrado en
`REG_stochastic_eval_v1/v2`). Con `n_runs=150` el Paso 1 midió A0=4 para el
forzado; con `n_runs=50` la corrida midió 3 (uniform/boltzmann) y 4
(weighted). **La grilla se mueve con `n_runs`**, así que la capacidad de
COCO de disparar en este régimen depende también de ese parámetro.

---

## Δ_r — el STOP se ve, y no destruye

| modo | i=0 | i=5 | i=12 | i=23 |
|---|---:|---:|---:|---:|
| uniform | 2.0 | 106 | 220 | **404** |
| sin thermostat | 2.0 | 106 | 220 | **404** |
| weighted | 2.0 | 82.1 | 26.9 | **2.33** |

`uniform` y `sin_thermostat` tienen trayectoria de Δ_r **idéntica** — es
esperable: `uniform` nunca comprimió nada, así que su Δ_r evoluciona como
si no hubiera thermostat. `weighted`, con 7 STOPs, mantiene Δ_r acotada:
404 contra 2.33 al final.

`delta_A` en los 7 STOPs: `[0, 1, 0, 1, 0, 0, 1]` — **ningún negativo**.
Tres STOPs suman un atractor, cuatro son neutros. En este régimen STOP no
produjo pérdida en ninguna aplicación.

---

## Sobre el D_ckm del panel — lo que esta corrida NO vuelve a demostrar

Los conjuntos de valores del panel:

| modo | valores | último |
|---|---|---:|
| uniform | −1.5, −0.5, −0.25, 0, 0.25, 0.5 | 0.25 |
| boltzmann | −1.5, −0.5, −0.25, 0, 0.25, 0.5 | 0.25 |
| sin thermostat | −1.5, −0.5, −0.25, 0, 0.25, 0.5 | 0.25 |
| weighted | −1.5, −1.0, 0, 0.25, 0.5 | 0.0 |

Los tres primeros coinciden exactamente — **pero eso acá es trivial**: ninguno
de los tres aplicó un solo STOP, así que sus Δ_r son literalmente la misma
secuencia. **No es evidencia de la cancelación algebraica** de
`_combine_W_Delta`. Esa evidencia sigue siendo la de
`REG_armstrong_boltzmann_comparison_v1`, donde los tres modos **sí**
comprimieron y aun así el panel dio idéntico.

Lo que sí aporta esta corrida: `weighted`, el único que comprimió, es el
único cuyo panel diverge. Consistente con que el panel responde al soporte
de Δ_r y no a su magnitud — pero con n=1 modo, no es demostración.

---

## Lo que este REG no establece

- **Nada sobre el régimen natural.** El Paso 2 no se corrió. Los A0 de
  Paso 1 (58 contra 4) son lo único medido de ese lado, y son A0, no
  trayectoria.
- **No es comparación con la corrida Armstrong** (W_pos, `WARMUP_TEXTS`,
  `n_runs=200`, `track_landscape=True`). Otro corpus, otros parámetros,
  otro objetivo. Que allá `weighted` fuera el que **no** disparaba y acá sea
  el único que **sí** dispara es una observación, no un resultado pareado.
- **No dice que el umbral 0.40 esté mal.** Dice que en un paisaje con A0≈3
  el umbral cae en un hueco de la grilla. Con qué A0 tiene sentido operar es
  una decisión del modelo.
- **El piso de Paso 1 es estimado**, con Δ_r sintética. El piso real depende
  del soporte que genere la secuencia real de rechazos.
- **`delta_A` se calculó en el driver**, no vía `track_landscape` (apagado
  por costo): tras cada STOP se cuenta sobre `W + Δ_r` comprimida — la misma
  cuenta que COCO hace internamente, con una relajación extra en vez de tres.
  `coco.py` no fue modificado.
- **Sin commit.**

---

## Archivos

- `iap_chatroom/tests/test_wmixta_forzado_paso3.py` — driver reanudable
- `process/experiments/wmixta_forzado_paso3/result_forzado_*.json` — 4 condiciones
- `services/corpus_service.py` — flag `force_w_pos` (desarrollo, default off, marcada en traza)
- `iap_chatroom/tests/TASK_armstrong_boltzmann_comparison_wmixta_v5.md` — spec
- `registers/REG_armstrong_boltzmann_comparison_v1.md` — corrida W_pos previa
- `registers/REG_stochastic_eval_v2.md` — sesgo n_runs y sensibilidad al modo

---

*Sep 2026 — Codespace ckm — bash/Linux*
