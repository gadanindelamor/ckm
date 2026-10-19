DELAMOR A CODE (texto de Opus):

Soy delamor. `git pull` antes de nada.

Leí el REPORTE del CP1 (`10a6bf1`). Confirmo tus decisiones: **`min_df = 2` default de CKM**, y el estado del caso en **`experiments/_state_S2-C0/`**, no en `registers/`. Están en `docs/opus/decisiones_en_el_acto.md` (19 oct).

**Una corrección a la condición 5, que es de Opus, no tuya:** la TASK decía "en cada rebuild, `calibrate` corre sobre la W nueva", y eso implementaste. El diseño que confirmé el 10 oct (`TASK_calibrate_mecanismo_v1`, punto 3) es otro: **calibrar durante la meseta, sobre la W candidata en sombra, antes de que termine el ciclo i**; en el salto, comparar sha y usar la de la sombra o recalibrar y declarar; **nada se descarta: la W sombra y su calibración se guardan siempre**. Lo que hiciste es el camino de respaldo. Y hoy, en el salto, `calibrate` corre en el hilo del mensaje: **mientras calibra, el canal no atiende** — el mundo espera, y eso choca con la condición 4.

La TASK está actualizada en `docs/opus/TASK_iap_serie2_caso0_v1.md` (condición 5 y **CP1c** nuevo). Copiá esa versión a `docs/tasks/` en un commit propio.

**Ahora: el CP1c** (la sombra), con **predicción antes**, REPORTE y **A1.PAUSA**. Antes de diseñar, **medí cuánto tarda hoy `calibrate` en el salto** con la W del canal y ponelo en la predicción. Cómo correrla sin frenar al canal lo proponés vos, **sin procesos nuevos**. Optimizaciones posteriores (la traza de W_{i−1} para la grilla) **se declaran para más adelante**.

Después del CP1c, el CP1b.

Reglas de siempre: archivos nombrados uno por uno, sin `git add -A`; sin regresiones ni compatibilidad hacia atrás; no se ejecuta código ajeno; donde se duda, A1.PAUSA.
