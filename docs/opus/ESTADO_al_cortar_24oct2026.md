# ESTADO al cortar — 24 oct 2026, actualizado el 26 oct (Opus 5.5, Cowork)

Traza completa en `docs/opus/decisiones_en_el_acto.md`, entradas del 24 oct. Esto es solo el mapa.

## Hecho hoy
- Code (madrugada, sin Opus, por los límites de uso): el build de W no calibra.
  - REG: ahora `registers/REG_calibrate_no_corre_en_el_build_v1.md`, con el OK de delamor.
  - TASK: `docs/tasks/TASK_calibrate_en_el_build_v1.md`.
  - El CP1 (`bootstrap`) se commiteó y se revirtió solo en el código (`7040a02`). El vivo no se corrió.
- Review del v32 hecho por Kimi, sin acceso al repo: `docs/paper/REVIEW_REPORT_PAPER_v32.md` (sin commitear) y `contexto_claude/`.
- Opus: `docs/opus/CONSIDERACIONES_v33_24oct2026.md`, que es el plan del v33 con el review de Kimi verificado contra el repo.
- Push al día: `ffdc77b`.

## Lo que sigue
- **Opus:** armar el v33 en dos archivos, `_borrador` y `_print`, siguiendo las CONSIDERACIONES. Antes de escribir:
  - leer el CP-E (el 15.52 → 5.27 del §4.3.2);
  - leer la cita de P2 en Goltsev 2006;
  - leer el criterio estructural de rebuild;
  - buscar en `DECISIONES` el origen del baseline de Monitor.
  - Después, ajustar `cold-referee` y el pedido de review para que apunten al `_print`.
- **Opus → Code (ckm, Codespace), tarea chica, primero en la próxima sesión.** Las tres declaraciones de fourforums v8n:
  1. **Extracción:** O1–O7 y la cadena v8h→v8n, que ya están declaradas.
  2. **LandscapeConfig de cada una de las 8 W:** `CKMlandscapeConfig.create(W, sampling_mode="uniform", n_runs, seed)` y un `Ciclo` con `w_version_id = sha256_W`, N, μ_W y β_c en sus dos formas. Se guarda junto a los resultados y no se vuelve a medir.
  3. **Calibración: "no se ejecutó"** (`nulo_calibrado`), porque las W son primeros builds y lo medido no usa umbrales.

  También declarar lo que hoy no coincide con la Config:
  - la semilla 20261023 contra la 0 de la Config;
  - las muestras 1000, 5000 y 20000 contra las 1000 declaradas;
  - el REG reporta `beta_c_landscape` (media de los positivos), que no es `beta_c_nonzero` ni `beta_c_global`;
  - la identidad de cada W es el sha del archivo, no `sha256_W` (sin verificar si coinciden).

  Opcional, como punto aparte: correr `calibrate` offline sobre las 8 W, como medición, sin predecir el resultado. Fuente: `decisiones_en_el_acto.md`, 24 oct.
- **delamor:**
  - qué hacer con las 13 de `test_should_rebuild_conectado.py`: acotarlas o archivarlas. Code retoma en dos días;
  - P13 y P14;
  - la definición del margen de `calibrate`: extremos o máximo interno (E3);
  - J1, J2, los subgrafos chicos y si se versiona `W_asim`, que vienen del 23;
  - la figura Monitor contra COCO, si la querés.
- **Sin dueño:** en `docs/paper/` hay copias sin commitear del v31, el v32 y el review del v31, idénticas a las de `docs/opus/`, más el review del v32.

## Refuerzo (delamor, 24 oct) — para todas las instancias, Opus y Code
**Los `.py` se leen completos: docstring y código.**
- Si el acceso es solo de lectura, se leen **1 vez**, enteros.
- Si es de lectura y escritura, se leen **2 veces**: entero antes de modificar y entero después.
- **Las divergencias entre el docstring y el código se declaran y se corrigen.** Ninguna afirmación sobre un `.py` sin haber cotejado las dos cosas.

*(Lectura de Opus de "2 veces 1 vez": 2 para lectura-escritura y 1 para lectura. Si es al revés, delamor lo corrige.)*

## Pendientes de delamor — qué es cada uno, en una línea, y qué hay que decidir
1. **Las 13 de `test_should_rebuild_conectado.py`.**
   - Qué es: el cambio para que la primera W pase por `calibrate` (causa `bootstrap`) hace fallar esos 13 tests, que codifican tu prueba de concepto de dominancia.
   - Hay que decidir: actualizarlos acotados a lo que pasa después del origen y volver a aplicar el cambio (`a7d065f`), o dejarlo archivado, con la primera W sin calibrar y declarado. Code retoma en dos días.
2. **El margen de `calibrate`.**
   - Qué es: para decidir si separa, `calibrate` mira solo los extremos de la curva (λ = 0 y λ = 1). En el intento 3 el máximo de adentro (λ = 0.25) ya era 4,9 veces el umbral desde el primer rebuild, y el margen lo descartó tres veces.
   - Hay que decidir: si mira los extremos o el máximo interno. Cambia lo que mide el instrumento (E3).
3. **P13, una línea suelta en `iap_chatroom/_state/channel_ticks.jsonl`.**
   - Qué es: al correr la suite en paralelo (`-n 4`) el aislamiento se rompió y quedaron 2 líneas en un archivo de estado. No entra a git.
   - Hay que decidir: (a) si esas líneas se guardan en `process/` con fecha o se borran; (b) si la suite se corre en paralelo de ahora en más. En este Codespace el paralelo no acelera: 169 s contra 95 s.
   - Default vigente: no tocar la línea, y paralelo solo para medir.
4. **P14, el guardia de "sin lógica en los drivers".**
   - Qué es: el caso necesita leer `run_store`, y un guardia le prohibía siquiera nombrarlo. Tu regla es *"quien escribe es IAP"*. Code lo afinó: el caso puede leer y no puede escribir (`append`, `set_state_dir`, `reset_failures`).
   - Hay que decidir: si queda así (default) o vuelve el guardia absoluto. Con el guardia absoluto el caso lee el archivo a mano y repite su nombre.
5. **El REG del intento 2.**
   - Qué es: el REG nuevo del calibrate dice que al del intento 2 le faltan tres cosas: (1) que el primer ciclo no podía calibrarse; (2) que la curva no subió en ningún punto (`d_max = 0`); (3) que los umbrales fueron los default en las 51 evaluaciones. Sin eso, los "0 disparos" se leen como un dato del campo.
   - Hay que decidir: si se le agrega una nota. El REG es Clase R.
6. **J1, quién cita a quién en dos REGs viejos.**
   - Qué es: `REG_qr_asymmetry` y `REG_c6c_asim` leen "T0_quotes_T1" como "T0 cita a T1". Por la nomenclatura del pipeline, T0 es el citado. Los números no cambian; cambia el sentido de la flecha. Detalle en `registers/REG_fourforums_v8h_nombres_C6c_v1.md`.
   - Hay que decidir: si se corrigen esos dos REGs con una nota.
7. **J2, los votos "unsure" de fourforums.**
   - Qué es: el 16,2 % de los votos de los anotadores son "unsure". Desde v8j se reportan y no se usan para el signo.
   - Hay que decidir: si siguen afuera (lo de hoy) o entran de alguna forma.
8. **Subgrafos chicos de fourforums.**
   - Qué es: con 146 nodos el instrumento está en su techo (cada muestra da una órbita distinta) y no separa la W observada de las nulas. Propuesta de Opus: subgrafos de 18–20 nodos, elegidos con extracción declarada, con enumeración exacta de los 2^N estados, como en el CP6.
   - Hay que decidir: sí o no.
9. **`W_asim_v8h.json` en el repo.**
   - Qué es: tiene pares autor–autor con sus ids, que son dato a nivel de fila del IAC.
   - Hay que decidir: si se versiona o se espera a la consulta de licencia del IAC (Rob Abbott). Default: no se versiona.
10. **La figura de D_ckm^Monitor contra D_ckm^COCO**, a lo largo de las 51 y las 27 evaluaciones.
    - Qué es: un gráfico que sale de los JSON que ya existen, para verlo.
    - Hay que decidir: sí o no. Si es sí, Opus escribe el texto para Code.
11. **Copias sueltas en `docs/paper/`.**
    - Qué es: el v31, el v32 y el review del v31 duplican los de `docs/opus/`, y el review del v32 de Kimi está sin commitear.
    - Hay que decidir: si Opus commitea el review del v32 en `docs/opus/` y las copias quedan como están. Menor.

## Raro
- En `.git/objects` hay cientos de `tmp_obj_*` sobrantes de sesiones anteriores. No son locks y no se tocaron.
- Uso al 95% del límite semanal; se repone en un día.


---
## 26 oct — plan del v33, después de leer el v32 entero (1117 líneas)
Decisiones de delamor del 26 oct en `decisiones_en_el_acto.md`. Cambios por lugar del v32 (líneas del v32):
- **Bloque de arriba del `_borrador`:** el bloque del v33 y, debajo, las secciones **Traza** (los bloques v29–v32 tal como están), **Pendientes** y **Retirado**. Lo retirado va al `_borrador`, nunca al `_print`.
- **Premisas → F** (l.65–67, l.98, l.219–220, l.258–272): se va "premise/premises" para P1–P7. F1, F3 y F4 quedan como *formulaciones matemáticas que se verifican sobre W estática*, sin "(formerly Pn)". El párrafo de P2 (l.272) va a Retirado. **Premisas solo en W dinámica** (delamor, 26 oct: *"las premisas entiendo serían solo para W dinámica?… sí. anotalo"*). W dinámica tiene una sola premisa (§4.2.4: el campo es continuo, lo que salta es la medición). W estática no tiene premisas, solo F verificadas y declaraciones. De las tres de l.260–264: **el determinismo** (Goles, regla de desempate) pasa a ser una **F**; **el productor declarado** y **la medida de referencia** (σ₀ uniforme) pasan a ser **declaraciones**, como la de extracción y la LandscapeConfig.
- **§5.2 P2, P5, P6, P7** (l.400–420) → Retirado. P5–P7 *"esperan condiciones"*. Arrastran §5.3 (l.424), el abstract (l.67), §8.1 (l.738–741) y §8.5 (l.802, l.832, l.865–872). **Respondido (delamor):** el nulo del signo por marcadores (l.404–416) **queda** como medición, sin la predicción P5.
- **§4.2 y §4.2.4** (l.297, l.334): *"what jumps is its measurement"*, con la tensión declarada; sale *"[Propuesta — decide delamor.]"*.
- **§4.2.3 CKMLandscapeConfig** (l.326) está mal contra el código: el threshold **no** está en la Config (`ckm_landscape_config.py:186`, D6). Se corrige así: declarado = `sampling_mode`, `n_runs`, `seed`, `scale`; medido por ciclo = `w_version_id`, N, μ_W y β_c en sus dos formas.
- **§4.2.1 / §6.4 / §8.2:** la primera W de cada corrida no pasa por `calibrate` (`registers/REG_calibrate_no_corre_en_el_build_v1.md`); el intento 2 tiene `d_max = 0` en los 4 rebuilds; el umbral queda por debajo de la dispersión del muestreo, como conclusión (M4).
- **β (M3):** un párrafo con `β_i`, `β_collective`, `beta_c_corpus`, `beta_c_landscape` y `beta_c_nonzero/global`, según el código (CONSIDERACIONES §3). Ninguno entra en la relajación del vivo (`uniform`).
- **§4.3.1 baselines (M5):** el de COCO es una decisión de delamor del 8 oct (`coco.py:240`); el de Monitor, tal como está en el código.
- **§4.3.2** (l.370): el texto de CONSIDERACIONES §3 M2. El *"15.52 → 5.27"* va a Pendientes (a verificar en el CP-E, `0e042ac`).
- **REG del intento 3** (l.531, l.553, l.567): → `registers/REG_iap_serie2_caso0_intento3_v1.md`; sale *"register in draft"*.
- **IAC v2:** l.398 y l.900 → se obtiene de https://nlds.engineering.ucsc.edu/iac2/; sale *"[Permiso de uso pedido — pendiente]"*.
- **§8.3** (l.768): el gap de representación como forma (círculo que no cierra, hélice), *no medido*.
- **Al `_print` no van:** `[a verificar.]` (l.396), la nota en castellano de §7.6 (l.724), los `[VERIFY]` (a Pendientes), el placeholder del release y la fecha (a Pendientes).
- **Respondido (delamor: *"si sostiene algo se quedan"*):** fourforums v8i–v8n **entra al §5** con las tres declaraciones y sus límites. Fuentes: los REGs de ckmdatasets del 23 oct y `registers/REG_ckm_W_fourforums_v8n_2026-10-23.md`.
- **Falta leer antes de escribir:** el CP-E, el criterio estructural de rebuild y el baseline de Monitor en `DECISIONES`.
- **Recomendación de Opus, por el uso:** escribir el v33 en una sesión nueva, que arranque de este ESTADO. Esta conversación ya es muy larga.

## Próxima sesión de Opus (sesión nueva, por la estrategia de uso)
1. **v33** (`_borrador` + `_print`) según el plan de arriba — **después del reporte de Code (texto 08)**; el plan de calibración/primer build cambia.
2. **DEFS v19** sobre la v18, con lo del 26 oct: las premisas solo en W dinámica (las F y las declaraciones en W estática); P1–P7 retiradas como premisas; la Config (lo declarado y lo medido, sin umbrales); el primer build sin calibrar; las capas del repo (`X_alcance_CKM_IAP_devices_26oct2026.md`); la nueva ubicación de `P1P4/` → `process/model_properties_front_20261004/`.
3. **Para Code** (texto a escribir): correr la suite (el test movido, `test_el_jsonl_historico_real_se_lee`, tiene que correr y no saltearse) y la tarea de las tres declaraciones de fourforums.

---
## 26 oct, tarde — después del arranque
- Respuestas de delamor al Feedback X: registradas (`902a586`).
- Docstring de `calibrate.py`: declara que `calibrate()` usa sólo el extremo de colapso (`8e3ff3b`).
- **Pendientes del repo, reordenados por delamor (sus ejes):**
  1. **Bootstrap:** primero entender cómo nace la primera W por el camino del rebuild (condiciones, flujo limpio o no); después evaluar las 13. No es "dejarlo como está".
  2. **Dominancia en los criterios de `should_rebuild`:** sin decisión todavía.
  3. **Defaults de `LandscapeConfig`:** el docstring dice que `n_runs` y `seed` son obligatorios; el código les da default. Espera la decisión.
  - **calibrate:** *"debe empezar por los defaults para saber que curva es lambda"*; pregunta abierta, ver decisiones del 26 oct.
- **Code primero:** `docs/opus/TEXTO_PARA_CODE_08_REPO_CKM_verificar_bootstrap_umbrales_26oct2026.md` (verificación V1–V6, sin implementar). Opus lee su reporte en la BANDEJA antes que delamor.
- **Próxima sesión de Opus (propuesta):** leer el reporte de Code y, si hace falta, partir de "la punta del ovillo" (decisiones, 26 oct: los casos 1 y 2 en que COCO_i juzga con una vara que no sale de W_i). Leer completos `iap_chatroom/ckm_monitor.py` (869 líneas), el diff de `a7d065f` y `corpus_service.ingest`/`no_rebuild_reason`, y dibujar el flujo del primer build con sus condiciones (con figura, para delamor). Sin código corrido. El v33 queda después.
