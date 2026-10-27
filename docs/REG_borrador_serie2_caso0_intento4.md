# REG_borrador_serie2_caso0_intento4 — serie2_caso0, intento 4

Clase R, **borrador**. Pasa a `registers/` **sólo con el OK de delamor**. Estructura espejada de
`registers/REG_iap_serie2_caso0_intento3_v1.md`.

- **Caso:** `serie2_caso0` (técnico) / `S2-C0`.
- **Fecha:** 2026-10-27. **Duración real:** 1204,04 s. **Modo:** `ZERO_SHOT` desde corpus 0
  (verificado por MCP antes de arrancar: `corpus_size = 0`, canal en 0, `state_dir` del caso).
- **Ejecutado por Code**, por **orden explícita de delamor** (texto para Code 12, CP3 de
  `TASK_calibrate_en_el_build_v2`). delamor estuvo en el Codespace durante la corrida.
- **Datos:** `experiments/serie2_caso0_intento4_log.json` (commiteado) y
  `experiments/_state_S2-C0/` (10 archivos, **no se commitea**; el intento 3 quedó preservado en
  `process/` con timestamp `1793085284`, 10 archivos, sin borrar).
- **Código:** `481d744` (el `repo_commit` que el propio log registró).
- **Preflight:** los cuatro modelos respondieron (A 0,43 s · B 0,56 s · C 10,1 s · D 0,17 s).

---

## 1. Para qué corrió, y qué cambió respecto del intento 3

Para medir **el flujo nuevo** (CP1 + CP2) con todo lo demás igual. Lo que cambió:

| | intento 3 | intento 4 |
|---|---|---|
| quién construye la primera W | `ingest` | **`build_first_W()`, por la condición propia del origen** (D1) |
| ¿el origen pasa por `calibrate`? | **no** | **sí** (D2, punto único *"antes de instalar"*) |
| dónde vive el registro de la calibración | en `MonitorService` | **en su lugar del estado** (`CKMlandscapeConfig`, D3) |
| la vara de COCO | dos números sueltos | **`Threshold` con `provenance` y `source`** (D4) |
| `n_runs` de `calibrate` | 200, default de función | **1000, declarado en el estado** (D6') |
| conteos de `count_attractors` por calibración | 6 | **5** (λ=0 reusa `A0`) |
| lo demás | — | igual: `DURATION` 1200, consigna, ventanas, los cuatro modelos y sus techos |

**Sin predicción.** La orden lo dijo: separe o no separe, se registra.

## 2. Los números

| | intento 3 | intento 4 |
|---|---|---|
| duración real | 1204,61 s | 1204,04 s |
| mensajes en el canal | 60 | **98** |
| corpus (textos) | — | **94** |
| evaluaciones de Monitor | 27 | **65** |
| generaciones de COCO (ciclos) | 4 | **7** |
| decisiones registradas | 27 | **31** |
| de ésas, que movieron W | 3 | **7** (1 `bootstrap` + 6 `volumen`) |
| llamadas a LLM | 250 | **288** |
| errores `429` | 0 | **0** |
| errores fatales | 0 | **1** (device B, abajo) |
| calibraciones registradas | 3 | **7** |
| evaluaciones **sin registro** de calibración | **4** | **0** |
| `triggers` de COCO | 0 | **0** |

**Por device:**

| device | modelo | vueltas | llamadas | decisiones |
|---|---|---|---|---|
| device_a | groq `gpt-oss-120b` | 223 | 114 | INTERACT 45 · OP_SILENCE 24 · SKIP 154 |
| device_b | gemini `3.5-flash-lite` | 90 | 59 | INTERACT 12 · OP_SILENCE 35 · SKIP 43 |
| device_c | groq `gpt-oss-20b` | 228 | 113 | INTERACT 38 · OP_SILENCE 34 · SKIP 153 · UNKNOWN 3 |
| device_d | groq `qwen3.8-27b` | 2 | 2 | OP_SILENCE 1 · **LEAVE 1** |

**device D se fue en su vuelta 2**, con 0 errores — igual que en el intento 3. El caso corrió con
dos devices completos y una fracción.

**device B tuvo el único error fatal:** `McpError: Timed out while waiting for response`, levantado
en el cierre del cliente (`autonomous_device.run`, `Client.__aexit__`). No es `429`: su cuota no se
agotó. Terminó con **90 vueltas contra las 223 y 228** de A y C, así que corrió ~40% del tiempo.

## 3. Cada calibración: estado, condiciones y costo

Las **siete**, tal como quedaron en su lugar del estado. La primera (gen 1) **es la del origen**: en
el intento 3 ese bloque era `None`.

| gen | t | estado | causa | n_runs | seed | w_sha de la candidata | duration_s | blocking | valores |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `62d909d4c74e` | 0,2637 | True | `{}` |
| 2 | 11 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `2edc58cb403a` | 0,2567 | True | `{}` |
| 3 | 21 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `b01bce1b0ddb` | 0,2738 | True | `{}` |
| 4 | 31 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `5459b10cca57` | 0,3069 | True | `{}` |
| 5 | 41 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `0ad12b696b9a` | 0,2661 | True | `{}` |
| 6 | 51 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `472e54ff6655` | 0,2902 | True | `{}` |
| 7 | 61 | `no_calibrado` | `sin_separacion` | 1000 | 0 | `6ca344c3f05b` | 0,2993 | True | `{}` |

- **Siete de siete: `no_calibrado`, causa `sin_separacion`.** Ninguna separó.
- `n_runs = 1000` y `seed = 0` en las siete, **declarados en el estado**: el campo
  `parametros_declarados.sin_declarar` quedó **vacío** en las 65 evaluaciones, o sea que ningún
  parámetro de `calibrate` cayó en el default de su función.
- **El costo, que hasta esta corrida no se persistía:** 0,2567 a 0,3069 s, `blocking: True`. Es el
  tiempo en que el canal no atendió, en 7 de 98 mensajes. Contra el tick del canal (1,0 s): entre
  **26% y 31% de un tick**.

**Un hueco, y es de Code:** `w_sha_live_at_calibration` —el campo que hace visible **el orden**, o
sea que la calibración corrió **antes** de instalar— **no quedó en el registro del estado**. CP2
persistió `duration_s` y `blocking` y a éste lo dejó afuera; vive sólo en `punto_calibrate`, que es
del panel de Gradio y no se persiste. **De las 7 hay 1**, el snapshot final del log:

| | valor |
|---|---|
| candidata (`w_sha`) | `6ca344c3f05b…` — la W del ciclo 7 |
| viva al calibrar (`w_sha_live_at_calibration`) | `472e54ff6655…` — **la W del ciclo 6** |

Son distintas, y la viva es la del ciclo anterior: **el orden se cumplió** en esa calibración. De
las otras seis, **no se puede decir desde la traza**.

## 4. La vara de COCO, en cada evaluación

**65 evaluaciones, las 65 iguales:**

| | |
|---|---|
| `D_CKM_THRESHOLD` | **0,40** |
| `FRAC_REC_MIN` | **0,60** |
| `source` | `default` (65 de 65) |
| `provenance` de los dos `Threshold` | **`DECLARED`** (130 de 130) |
| `source` del `Threshold` | `default de coco.py — no_calibrado:sin_separacion` |
| `causa` | `no_calibrado:sin_separacion` (65 de 65) |
| `w_sha_match` | `False` (65 de 65) — **ver abajo** |

Los siete COCO nacieron con el default **declarado como tal y con su causa**. Es lo que D4 pedía: el
0,40 no se presenta como medido.

**Un defecto, y es de Code, encontrado por esta corrida.** `w_sha_match` dice `False` en las 65, y
**el registro era de la misma W que COCO juzgaba** — verificado: en t=0 la W de COCO y la del
registro son las dos `62d909d4c74e7602`. `_vara_del_coco` pone `coincide: False` en las tres ramas
que declaran el default, y una de esas tres es *"el registro es de esta W y no separó"*.

**Lo medido es que dos situaciones distintas producen el mismo valor:** *"el registro es de otra W"*
y *"es de ésta y no separó"* dan las dos `False`. Eso es el hallazgo.

**Cuál de las dos cosas está mal no está medido.** Puede ser el **valor** —y entonces esa rama
tiene que devolver `True`— o puede ser el **nombre**: si `w_sha_match` quiere decir *"hay vara
medida de esta W"*, el `False` es correcto y lo que falta es un campo aparte para la coincidencia de
sha. La primera versión de este párrafo afirmaba la primera reparación como si fuera la única;
**delamor lo marcó** (27 oct): *"ese es la manifestación del sesgo de control, del QUERER"*.
Corregido acá: se registra la colisión, no su arreglo. Los tests del CP2 no lo vieron: el del caso
"no separó" afirma `causa` y `source` y no este campo.

**No se tocó el código en este CP** (la unidad era el vivo y su registro). Queda reportado.

## 5. La línea del origen (D5), y los contadores (CPa)

**La línea del origen existe.** En el intento 3 el nacimiento de W era el único cambio de W sin
registro.

| campo | valor |
|---|---|
| `t` | 24 |
| `causa` | **`bootstrap`** |
| `ocurrio` | `True` |
| `motivo_no_rebuild` | `None` |
| `w_sha_antes` | **`None`** — antes del origen no había W |
| `w_sha_despues` | `62d909d4c74e7602` |
| `w_cambio` | `True` |
| `corpus_size` / `message_count` | 30 / 33 |

De las 31 decisiones: **1 `bootstrap` + 30 `volumen`**; movieron W **7** (el origen y 6 del
régimen), y 24 no lo hicieron, con motivo `corpus_en_acumulacion`.

**Los contadores del CPa, en las que movieron W** — en el intento 3 habrían sido 0 por construcción:

| t | causa | `n_puntos_d_ckm` | `ciclos_sin_rebuild` |
|---|---|---|---|
| 24 | `bootstrap` | **0** | 33 |
| 25 | `volumen` | **11** | 10 |
| 26–30 | `volumen` | **10** | 10 |

El 0 del origen **es correcto**: todavía no había habido ninguna evaluación con corpus establecido,
así que el estructural no pudo evaluarse. Los 10 y 11 son lo que antes se perdía.

## 6. Los tres `D_ckm`, por separado

**Los nombres son de delamor** (27 oct): **Monitor**, **COCO** y **el de la copia de W**. El tercero
no mide el campo: mide una **copia** —`W.copy()`, deformada a propósito por λ— de la que nada
vuelve (*"simular sobre la copia, nada entra"*, definición del 6 oct, citada en `calibrate.py`).
Los dos primeros miden el campo vivo y se distinguen por su baseline; el tercero se distingue por
**sobre qué corre**.

| | intento 3 | intento 4 |
|---|---|---|
| `D_ckm` de **Monitor** (W + Δ_r, baseline que se resetea) | [−0,0202 , +0,2335] | **[−0,2774 , +0,5824]** |
| `D_ckm` de **COCO** (W sola, baseline fijado al nacer) | [−0,2796 , +0,0465] | **[−1,3879 , +0,0142]** |
| `frac_rec` de COCO | [0,9663 , 1,2219] | **[0,9900 , 2,6682]** |
| zona de COCO | `stable` 27/27 | **`stable` 65/65** |
| `triggers` | 0 | **0** |
| el de **la copia de W** (`calibrate`: candidata copiada y deformada por λ) | `n_runs` 200 | **`n_runs` 1000** |

**El umbral 0,40 es contra el `D_ckm` de COCO**, no el de Monitor. El de COCO **no pasó de
+0,0142** en las 65, así que los `triggers: 0` son coherentes con su propia cantidad. El de Monitor
llegó a **+0,5824** —que supera el 0,40 en 3 de 65— pero **ésa no es la cantidad que COCO compara**.

Lo que se ve, sin interpretar: los dos se movieron a lados opuestos y con mucho más recorrido que en
el intento 3 (0,86 y 1,40 de ancho, contra 0,25 y 0,33).

## 7. Dónde se cayó en un default, y cuántas veces

| default | veces | ¿queda visible? |
|---|---|---|
| `D_CKM_THRESHOLD` / `FRAC_REC_MIN` de `coco.py` | **130** (2 × 65 evaluaciones) | **sí** — `Threshold` `DECLARED` con `source` y causa |
| `n_runs`, `seed`, `grilla` de `calibrate.py` | **0** | — (`sin_declarar` vacío en las 65) |
| `n_runs` / `seed` de `CKMlandscapeConfig` | **no se puede contar** | **no** — una Config que cae en su default y una que lo declara dan el mismo `declarado`, `panel()` y `to_dict()` (verificado en CP2) |

## 8. Lo que este registro NO dice

- **No dice por qué ninguna de las siete separó.** Que a `n_runs = 1000` no separe es consistente
  con lo medido antes del vivo (sobre la W del intento 3, 0 de 10 semillas separaron a 1000, contra
  2 de 10 a 200), y **esto no es una explicación**: es otra corrida con el mismo resultado.
- **No dice nada sobre el margen.** No se tocó. Con los extremos ninguna separó; `d_max` por curva
  no se tabuló acá.
- **No dice si el orden se cumplió en seis de las siete calibraciones.**
  `w_sha_live_at_calibration` no está en la traza (§3).
- **No dice por qué device B murió** con un timeout de MCP en el cierre del cliente, ni si eso
  cambió lo que el campo hizo. 90 vueltas contra 223 y 228.
- **No dice por qué los dos `D_ckm` se abrieron tanto** respecto del intento 3, ni si eso viene del
  flujo nuevo, de los 7 ciclos en vez de 4, de los 94 textos, o de la composición del canal con B a
  media máquina y D afuera. **Cuatro variables cambiaron a la vez.**
- **No dice que el flujo nuevo sea mejor.** Dice que hace lo que CP1 y CP2 declaran: el origen
  calibra, su registro existe, la vara se declara con su origen y la línea del origen está.
