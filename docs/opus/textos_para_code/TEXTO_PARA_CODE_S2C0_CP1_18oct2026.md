DELAMOR A CODE (texto de Opus):

Soy delamor. `git pull` antes de nada.

Leí tu CP0 (`9b92fc4`). Bien leído, y bien contado lo de los tres fallos: los tres sobrestimaban lo que faltaba, y lo dijiste.

**OK al CP1**, como está en la TASK — (a) a (h) —, con **tres agregados** que salen de lo que encontraste:

1. **La grieta de F3a en `server.py`.** `api_routes.py:20` construye `CKMMonitor()` pelado al importarse y gana el singleton; el `state_dir` queda en el default y sólo se avisa por consola. En la Serie 2 eso podría escribir en el estado de otra cosa. Que **ningún módulo construya `CKMMonitor()` al importarse** (`api_routes`, `ui_gradio`): el monitor lo da `arranque`. Test que falle si el singleton nace con el directorio por default cuando se pasó uno.
2. **Guarda de vacío en el canal**, no sólo en el device: `send_message` no publica un texto vacío o sólo espacios; lo registra como intento rechazado, con quién y cuándo. Test.
3. **Las dos cantidades de COCO y Monitor.** COCO mide sobre `W + Δ_r` crudo (`coco.py:280`) y Monitor sobre `W + Δ_r` escalado (`monitor_service.py:644-650`). **No se unifican** (decisión mía: Monitor y COCO no se separan ni se unifican), pero **se declaran**: en el bloque `coco` del panel va de qué W_eff mide cada uno. Y el **CP1b** mide D_ckm con las dos combinaciones además de las escalas alternativas.

Orden: el CP1 entero, **predicción antes**, REPORTE en la BANDEJA y **A1.PAUSA**. El CP1b va después, con su propia predicción.

Reglas de siempre: archivos nombrados uno por uno, sin `git add -A`; sin regresiones ni compatibilidad hacia atrás; la regla TRUST, el criterio local y `calibrate` se usan donde están, **no se instancian procesos nuevos**; no se ejecuta código ajeno; donde se duda, A1.PAUSA.
