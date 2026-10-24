# Consideraciones para el v33 — Opus 5.5 (Cowork), 24 oct 2026

Para leer antes de que arme el v33. Si algo está mal, se corrige acá, que es más barato que rehacer el paper.
Todo lo que dice "leído" lo leí hoy en el archivo y la línea que se nombran. Lo que no leí está dicho como no leído.

---

## 0. Lo único que necesito de vos

**¿El REG `docs/REG_borrador_calibrate_no_corre_en_el_build.md` (Code, hoy) pasa a `registers/`?**
- Si pasa, el hallazgo entra al cuerpo del §6.4 con su fuente.
- Si no pasa, va a *Pendientes*, en el bloque de arriba, y el cuerpo no lo menciona.

El resto lo decido yo y queda registrado abajo.

---

## 1. Cómo se arma el v33 (ya decidido por vos, 23 oct)

- **Dos archivos.** `_borrador` lleva el bloque de arriba (cambios, traza y *Pendientes*) y el cuerpo. `_print` lleva solo el cuerpo. El review va sobre el `_print`.
- **Nada pendiente en el cuerpo.** Va a *Pendientes*: lo que falta verificar, el caso nulo, los `[VERIFY]` de citas y la licencia del IAC.
- **La premisa del campo.** El v32 dice *"what jumps is its representation"* (l.334 y §4.2). Pasa a la medición: el campo es continuo y lo que salta es la medición. La tensión queda declarada: si el instrumento es parte del campo, la medición también.
- **§8.3, el gap de representación.** La circularidad pasa a ser la forma de la definición, no su falla: un círculo que no cierra (área 0.000862, `REG_octava_ckm_v1`), que con el tiempo como eje es una hélice. Se escribe como **no medido**.
- **El path del REG del intento 3.** El v32 cita `docs/REG_borrador_serie2_caso0_intento3.md`, que Code borró hoy. Pasa a `registers/REG_iap_serie2_caso0_intento3_v1.md`, y se va la frase *"a register still in draft"*.

---

## 2. Lo de hoy que toca al paper: el build de W no calibra

Fuente: el REG borrador de Code (ver §0).
- La **primera W de cada corrida** nunca pasa por `calibrate`. Su estado es `None`, ni siquiera `nulo_calibrado`. Es así **por construcción**: `ingest()` construye la W antes del bloque de la decisión (`ckm_monitor.py:368` y `:458`).
- Por eso, en el primer ciclo COCO corre siempre con los defaults 0.40 / 0.60. Fueron **11 de 51** evaluaciones en el intento 2 y **4 de 27** en el intento 3.
- En el intento 2, los cuatro rebuilds dieron `d_max = 0.0000` en λ = 0: la curva nunca subió.
- En el intento 3, el máximo cae adentro de la curva (λ = 0.25) y crece: 0.0280, 0.1760 y 0.2312. El margen mira solo los extremos y cruza el cero recién en el último rebuild. El máximo interno del primer rebuild ya era 4,9 veces el umbral que se adoptó al final.

**Qué cambia en el v33:**
- §6.4 y §8.2 dicen *"did not separate in attempt 2 and separated in attempt 3"*. Les falta decir que el primer ciclo no podía calibrarse, y que en el intento 2 la curva no subió en ningún punto. Se agregan los hechos, sin lectura.
- La definición del margen (extremos o máximo interno) es E3 y te toca a vos. **No va en el paper como propuesta**: va a *Pendientes*, si querés.

---

## 3. El review de Kimi (v32), punto por punto

Kimi no tiene acceso al repo. Su *verified* es contra los documentos que le pasaste. Lo que sigue está verificado contra el repo.

**M1 — lo que falta verificar.** Va entero a *Pendientes*, no al cuerpo, por tu regla del 23 oct. Se agrega uno que el v32 ya marcaba: en el §4.3.2 dice *"moves N_eff by 66% in A24 (15.52 → 5.27)"*, y 5.27 es el N_eff de D12. Puede ser un error de copia. Se verifica contra el CP-E (`0e042ac`).

**M2 — "3 to 34 times".** Kimi tiene razón, y lo verifiqué con la tabla del propio paper (l.364–368). El stop list en E7 da 0.04, por debajo de la dispersión por semilla (0.07). Dividiendo cada rango por la dispersión por semilla de su propio corpus:
- A24 (semilla 0.07): 9.4–12.4
- D12 (semilla 0.09): 3.1–26.6
- E7 (semilla 0.07): 6.1–25.0, más el stop list, que da 0.57

**El arreglo que propone Kimi también está mal:** *"an order of magnitude"* no vale para 3.1 ni para 6.1. Texto para el v33: *"Except for the stop list on E7 (0.04, below its seed spread), every parameter moves N_eff between 3 and 27 times its own corpus's seed spread."* Es solo aritmética.

**M3 — los β.** Kimi cuenta tres. En el código hay más, y el paper no los nombra:
- `β_i` = 1 / (media de los rechazos de cada device), en `coco.py:403`.
- `β_collective` = la mediana de los `β_i` (`coco.py:414`). El docstring dice que *"se calcula, se reporta en el panel. Pero no regula nada"*. Es lo mismo que en el §8.2 aparece como *"β inferred from rejection history"*: no es un tercero, es el mismo con otro nombre.
- `β_c`, en dos funciones que su propio docstring dice que no dan lo mismo (`landscape_engine.py:186-189`: 13.83 contra 10.46):
  - `coco.beta_c_corpus`, que es la referencia de TEMP_SIGNAL;
  - `landscape_engine.beta_c_landscape`, sobre W_eff, que se usa solo con muestreo `boltzmann`.
- La Config lleva además `beta_c_nonzero` y `beta_c_global`.
- **En las corridas vivas no entró ningún β en la relajación:** `ckm_monitor.py:271` usa `sampling_mode="uniform"`, y `_setup` usa β solo en `boltzmann`. Eso responde la pregunta 5 de Kimi.

En el v33 va un párrafo que nombra cada β, dónde se calcula y qué hace. Sin nombres nuevos.

**M4 — la calibración "separó".** De acuerdo, en parte. El v32 ya dice que el umbral 0.00571 es menor que la dispersión del muestreo, y que *"what it separates is not established here"*. Esa frase sube a conclusión del §6.4 y se repite en el §8.2. **No tomo** el agregado de Kimi, *"corpus scale is the binding constraint"*: es una atribución.

**M5 — la asimetría de baselines.** La pregunta que se contesta con el repo:
- **El baseline de COCO es una decisión tuya:** *"el baseline se fija al nacer el ciclo"*, 8 oct, CP3 punto 3, citado en `coco.py:240`.
- **El de Monitor** se fija en la primera evaluación con corpus establecido, sobre W + Δ_r, y se resetea cuando cambia W (`monitor_service.py:833-837`). El código lo llama *"lo único que no se unifica"*. **No encontré una decisión registrada sobre el de Monitor.** La busqué solo en los docstrings; me falta mirar `DECISIONES` y las TASK que lo nombran.

En el v33: lo de COCO con su fuente, y lo de Monitor tal como está. **No tomo** la otra pregunta de Kimi, *"what does it regulate, and against what?"*: es interpretación.

**M6 — la traza adentro del paper.** Ya está resuelto con el `_print`.

**Menores:**
- 1, el marcador *"decide delamor"* en §4.2.4: se cae con el cambio de premisa del §1.
- 2, *"free will"* en el §6.1: es tu término (22 oct: *"free will — ODA continuo"*). No lo cambio.
- 3, la cita de P2 (l.402): sale Bak, Tang & Wiesenfeld y entra Goltsev et al. 2006, que ya está en las referencias (l.951). **No verifiqué en Goltsev que diga τ ∈ [1.5, 2.0]**, así que la cita va con `[VERIFY]` a *Pendientes*.
- 4, figuras: va abajo, como propuesta.
- 5, AUTO-1/2: no se tocan.
- 6: no.
- 7, qué secciones caen si el IAC no da permiso: una frase condicional en *Pendientes*.
- 8: no, porque es atribución.

**Preguntas de Kimi:**
- Q1 es la de M5.
- Q2, cuánto depende `calibrate` de la semilla: se puede medir offline con las W del intento 3, en el Codespace. Queda como posible tarea para Code.
- Q3, si el criterio estructural de rebuild tiene un umbral declarado: no lo leí todavía. Lo leo antes del v33.
- Q4: el review del v31 está en `docs/opus/REVIEW_PAPER_v31_2026-10-22.md`.
- Q5 la contesta M3: ningún β.

**La recomendación de Kimi ("minor revision") no la tomo como veredicto.**

---

## 4. Propuesta, no bloquea

La figura de D_ckm^Monitor contra D_ckm^COCO a lo largo de las 51 y las 27 evaluaciones. Sale de los JSON que ya existen y se haría en el Codespace (Code). Vos valorás ver. Quedaría en el repo como prueba visual. Si decís que sí, armo el texto para Code.

---

## 5. Lo que no hice

- No re-verifiqué el resto del v32 pasaje por pasaje.
- No leí el CP-E para el 15.52 → 5.27, ni Goltsev, ni el criterio estructural de rebuild, ni `DECISIONES` sobre el baseline de Monitor.
- No corrí nada.
