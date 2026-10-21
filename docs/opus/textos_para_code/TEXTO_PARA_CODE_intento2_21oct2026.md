# Texto para Code — 21 oct 2026 (completo)

*Este texto **incluye** al `TEXTO_PARA_CODE_REG_y_pool_21oct2026.md` (parte A). Si ya pegaste aquel, la parte A ya está hecha o en curso: decilo y seguí con la B.*

**Antes de tocar nada: evaluá todo el texto contra el repo y decí las tensiones que veas.** Si hay alguna, A1.PAUSA y lo decís antes de seguir. Una parte a la vez, con reporte al cerrar cada una.

---

## Parte A — REG y declaración

### A1. El REG del intento 1 entra a `registers/`
delamor, 20 oct: *"si pasa a REG"*.
- Mové `docs/REG_borrador_serie2_caso0_intento1.md` a `registers/` con un nombre en la línea de los que ya están (p. ej. `REG_iap_serie2_caso0_intento1_v1.md`); el nombre lo decidís vos y lo declarás en el commit.
- Sacá la marca de "Borrador" y dejá una línea: *aprobado por delamor el 20 oct 2026*. **El contenido no cambia.** Actualizá las referencias al path viejo.

### A2. Hueco de declaración: pool con ≤ top_k términos
- `services/node_extractor.py`, `_seleccionar` (~561): si `len(orden) <= self.top_k`, entran todos los términos del pool, sin regla de empate, y N = |pool| < top_k.
- `docs/defs/DECLARACION_extraccion_W_v2.md`, operador 5, no lo dice (sólo empates y N = 0). Es un criterio que **no aplica por volumen**.
- **Declararlo, no cambiar el código:** una frase en el operador 5 (p. ej. *"Si el pool tiene ≤ top_k términos, entran todos: N = |pool| < top_k y la regla de empate no actúa."*); si `declaracion()` tiene que coincidir con el documento, los dos juntos con su docstring; un test que fije el caso.

A1.PAUSA con el reporte de A.

---

## Parte B — preparar el intento 2 de `serie2_caso0` (sin correrlo)

delamor, 21 oct: de acuerdo con todo lo que sigue. **El sesgo va en lo que entra (canal, consigna), no en CKM**: el 30, `min_df`, `top_k` y el resto de la declaración **no se tocan**. Lo que se cambia, se declara como sesgo con su objetivo: volumen para que nazca el primer W.

1. **`max_tokens` de Groq ≤ 1000** (`iap_chatroom/providers/groq_provider.py:19`). Incompatibilidad medida con el OTPM (REG §3). El valor lo elegís vos y lo declarás, con el chequeo de truncamiento como está. Si eso pide algo en Gemini, decilo.
2. **Ventana del gate de 10 a 4 mensajes** (`autonomous_device.py:506`, `history[-10:]`). Es la que multiplica el largo contra el presupuesto. Mirá también `history[-20:]` (`:467`) y decí si entra o no en lo mismo.
3. **Consigna: se agrega un pedido, no una condición** (delamor: *"un pedido, no una orden con forma de condición… son LLMs, no se trata de presionar"*). En `iap_chatroom/tests/test_caso_serie2_caso0.py:284`, al final de `CONSIGNA`, agregar:
   > *Please keep your messages short if you can: a few sentences, around 80 words or fewer.*

   Sólo en inglés, como el resto. Nada más cambia en la consigna.
4. **`DURATION` de 600 a 1200 s** (`:263`), declarado: con mensajes cortos la duración vuelve a ser palanca (con mensajes largos sólo sumaba 413).
5. **`device_d` y el `McpError`** (corrió la mitad del caso): leé la causa y **reportala antes de arreglar nada**. A1.PAUSA ahí.
6. **Modo `CONTINUA`** (delamor: *"si activamos el modo"*), desde los 13 textos. Verificá que el `state_dir` del intento 1 (`experiments/_state_S2-C0/`) esté en el Codespace con sus 13 textos; si no está, A1.PAUSA.

**No se corre.** Al terminar B: A1.PAUSA, reporte, y el intento 2 espera la orden de delamor. Durante el vivo, sin intervenciones (regla vigente).

**Fuera de alcance:** la condición de "COCO conectado" (delamor, 21 oct: verla en vivo no es necesario; tests y drivers ya lo chequean); el conteo del umbral de 30; el piso de `local_criterion` (queda de reserva, si con esto no llega).

Para Code: partes A y B, en ese orden, con A1.PAUSA al cerrar cada una.
