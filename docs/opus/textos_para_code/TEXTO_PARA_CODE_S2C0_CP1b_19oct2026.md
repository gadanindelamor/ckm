DELAMOR A CODE (texto de Opus):

Soy delamor. `git pull` antes de nada.

Leí el REPORTE del CP1 (`10a6bf1`). Confirmo tus decisiones: **`min_df = 2` default de CKM**, y el estado del caso en **`experiments/_state_S2-C0/`**, no en `registers/`. Están en `docs/opus/decisiones_en_el_acto.md` (19 oct).

**Sobre `calibrate`:** el diseño del 10 oct (`TASK_calibrate_mecanismo_v1`, punto 3) es calibrar durante la meseta sobre una W en sombra; lo que implementaste —en el salto, sobre la W nueva— es el camino de respaldo, y venía de cómo Opus escribió la condición 5. **Decido: S2-C0 va sin sombra, pero con la calibración en su lugar del flujo: en el momento de `should_rebuild`, ANTES del rebuild** — decidido el rebuild, `calibrate` corre sobre la W candidata (la que el rebuild va a instalar), todavía dentro del ciclo i; después se instala W y nace el COCO del ciclo i+1 con esos umbrales. Hoy está al revés (rebuild y después calibrate). Es un cambio de orden, chico: hacelo antes del CP1b, con su test (que falle si `calibrate` corre después de instalar la W) y su línea en el REPORTE. Declarado (en el salto `calibrate` corre en el hilo del mensaje y mientras calibra el canal no atiende: se declara). **La sombra queda como propuesta para más adelante.** La TASK actualizada está en `docs/opus/TASK_iap_serie2_caso0_v1.md`: copiala a `docs/tasks/` en un commit propio.

**Dos precisiones mías (19 oct), en `docs/opus/decisiones_en_el_acto.md`:**
- *"No se instancian procesos nuevos"* se refería a **la regla CKM TRUST**: no se instancia en procesos nuevos; `calibrate` y `criterio_local`, que ya la instancian, siguen como están.
- **No más rótulos en español.** Lo nuevo, en inglés. Y si es sencillo, **refactor con el cambio de nombre declarado**, sin alias: `criterio_local` → `local_criterion` (`CriterioLocal` → `LocalCriterion`, `UmbralesCriterioLocal` → `LocalCriterionThresholds`), `arranque` → `startup`. Lo que describe corridas pasadas y está congelado (como `experiments/vivo_03_*` si corresponde) se declara, no se reescribe; vos decidís y lo decís.

- **Las claves del panel que nacieron en el CP1** (`coco`: `conectado`, `umbrales`, `calibracion`, `disparos`, etc., y las de la tabla y la identificación S2) **pasan a inglés ahora**, antes del vivo. Declarado, sin alias.

**Orden:** (1) el reordenamiento de `calibrate`; (2) los dos renombres y las claves del panel en inglés, en commits propios; (3) **el CP1b** como está en la TASK (medir D_ckm dentro de un ciclo con la escala actual de Δ_r y alternativas, y con las dos combinaciones, la de Monitor y la de COCO). **Agregado:** medí también **cuánto tarda `calibrate` en el salto** con la W del canal. Predicción antes, REPORTE y **A1.PAUSA**. No se elige escala: se mide.

Reglas de siempre: archivos nombrados uno por uno, sin `git add -A`; sin regresiones ni compatibilidad hacia atrás; no se ejecuta código ajeno; donde se duda, A1.PAUSA.
