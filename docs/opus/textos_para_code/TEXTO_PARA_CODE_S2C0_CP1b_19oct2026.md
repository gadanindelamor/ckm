DELAMOR A CODE (texto de Opus):

Soy delamor. `git pull` antes de nada.

Leí el REPORTE del CP1 (`10a6bf1`). Confirmo tus decisiones: **`min_df = 2` default de CKM**, y el estado del caso en **`experiments/_state_S2-C0/`**, no en `registers/`. Están en `docs/opus/decisiones_en_el_acto.md` (19 oct).

**Sobre `calibrate`:** el diseño del 10 oct (`TASK_calibrate_mecanismo_v1`, punto 3) es calibrar durante la meseta sobre una W en sombra; lo que implementaste —en el salto, sobre la W nueva— es el camino de respaldo, y venía de cómo Opus escribió la condición 5. **Decido: S2-C0 va así, con la calibración en el salto, declarada** (en el salto `calibrate` corre en el hilo del mensaje y mientras calibra el canal no atiende: se declara). **La sombra queda como propuesta para más adelante.** La TASK actualizada está en `docs/opus/TASK_iap_serie2_caso0_v1.md`: copiala a `docs/tasks/` en un commit propio.

**Ahora: el CP1b** como está en la TASK (medir D_ckm dentro de un ciclo con la escala actual de Δ_r y alternativas, y con las dos combinaciones, la de Monitor y la de COCO). **Agregado:** medí también **cuánto tarda `calibrate` en el salto** con la W del canal. Predicción antes, REPORTE y **A1.PAUSA**. No se elige escala: se mide.

Reglas de siempre: archivos nombrados uno por uno, sin `git add -A`; sin regresiones ni compatibilidad hacia atrás; no se ejecuta código ajeno; donde se duda, A1.PAUSA.
