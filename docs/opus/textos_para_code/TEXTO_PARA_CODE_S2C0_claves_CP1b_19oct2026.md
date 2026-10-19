DELAMOR A CODE (texto de Opus):

Retomamos desde `1223623` (tu NOTA) y `5973d9e`. Hay dos pasos, en este orden. Vale lo de siempre: no se toca el vivo, sin alias, sin compatibilidad hacia atrás y cada paso cierra en verde.

**(1) Claves del panel en inglés, desde `git stash@{0}`.**
- Aplicá el stash. Las claves que nacieron en S2-C0 CP1 se **publican en inglés**.
- Las claves heredadas que otros módulos leen en castellano se **leen como están**: `calibrate` → `estado`/`valores`/`condiciones`, Monitor → `condicion_W`, criterio local → `umbrales_calibrados`. Es el arreglo que vos propusiste, y en este paso no se traducen.
- En el commit, declará la lista de esas claves heredadas como pendientes de pasar a inglés cuando se toque cada módulo. Si delamor decide otra cosa, eso va en un paso aparte.
- Criterio: la suite completa en verde. Si no cierra, no commitees: decí qué queda rojo y por qué.
- Cuando cierre, borrá el stash. No debe quedar trabajo que exista sólo en el Codespace.

**(2) CP1b, según la TASK S2-C0 (`docs/tasks/TASK_iap_serie2_caso0_v1.md`).**
- **Antes de correr nada, commiteá la predicción.**
- Medí D_ckm con:
  - la escala actual de Δ_r en `_combine_W_Delta` (Δ_r / max Δ_r × media de W > 0);
  - las alternativas que lista la TASK;
  - las dos combinaciones: Monitor escalado y COCO crudo.
- Usá el mismo conjunto de mensajes del CP1. Declará cuál es y su sha.
- Medí también **cuánto tarda `calibrate` en el salto** (`duracion_s`, varias corridas, mediana y rango). Ese dato es el insumo de la propuesta de la sombra.
- **No elijas escala.** Entregá la tabla y lo que no se pueda afirmar; la escala la elige delamor.

Al terminar: commits, estado de los tests, y avisá para el push.
