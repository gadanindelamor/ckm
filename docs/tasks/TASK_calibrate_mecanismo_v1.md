# TASK_calibrate_mecanismo_v1 — CONFIRMADO por delamor (10 oct)

*10 oct 2026 — Opus (Cowork), desde la sugerencia de delamor.*

## El concepto (delamor, 10 oct)

> La calibración del instrumento es cada vez que es necesaria, como en todo instrumento. No es una vez en su vida útil y nunca más; por lo cual el instrumento no podría estar calibrado para todos los casos posibles. **Implementar la calibración y ver si se calibra. MECANISMO.** De esa manera es consistente con la supuesta verdad y no sugiere ni carencia, ni falla, ni falta, ni universalidad.

## Qué se propone

1. **`calibrate` como mecanismo del instrumento**, no como constantes. Entra: una W (la foto de la meseta) y un **patrón de respuesta conocida**. Sale: los umbrales (`D_CKM_THRESHOLD`, `FRAC_REC_MIN`, y los que se decida) **y el estado de la calibración**, declarado junto con el sha de W y las condiciones (corpus, unidad, régimen). Antecedentes ya decididos: se calibra **antes**, contra un patrón; en la meseta, simulando sobre la foto (nada entra); no se calibra con las mediciones de la misma meseta que se mide (círculo). Lugar reservado: `ckm_landscape_config.py:187` ("proceso aparte, D6"); marca existente `calibrado=False`.
2. **Cuándo:** cada vez que hace falta. Como mínimo, en cada salto (`rebuild_calibrate`, diagrama de delamor: el salto es rebuild y calibrate juntos).
3. **Verificar que calibra:** con el campo plantado (`TASK_tests_instrumento_v1` CP6) como patrón, `calibrate` tiene que devolver umbrales con los que COCO dispara en los casos degradados conocidos y no dispara en los estables. Si no los encuentra, lo dice (estado no calibrado), no inventa un valor.

## Dónde se guarda (delamor, 10 oct)

> El criterio de dónde se guarda el JSON es **el mismo que para el resto de los datos que se guardan**. Congruencia conceptual y consistencia en la implementación del criterio.

La calibración se persiste como JSON en el mismo `state_dir` que `corpus_state.json`, `corpus_G_state.json` y la trayectoria (`CKMMonitor(state_dir=...)`, fix 2, `9140de5`), con el mismo mecanismo de escritura y lectura. Ningún lugar propio, ningún camino aparte.

## Sigue abierto

Qué patrón se usa para el canal vivo; los nombres de los estados de la calibración. Con delamor, antes de implementar esas partes.

## Recursos (criterio de delamor, 10 oct)

Cada test se verifica con los recursos al alcance del proyecto (local, Codespace, Groq). Lo que necesite un recurso fuera de alcance se implementa igual y queda **declarado** en el REPORTE con el recurso que falta; no se verifica hasta tenerlo.
