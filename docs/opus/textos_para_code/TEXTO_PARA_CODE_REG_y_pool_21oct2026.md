# Texto para Code — 21 oct 2026

Dos cosas chicas, en este orden. **Antes de tocar nada: evaluá el texto contra el repo y decí las tensiones que veas.** Si hay alguna, A1.PAUSA y me lo decís antes de seguir.

## 1. El REG del intento 1 entra a `registers/`

delamor, 20 oct: *"si pasa a REG"*.

- Mové `docs/REG_borrador_serie2_caso0_intento1.md` a `registers/`, con un nombre en la línea de los que ya están (p. ej. `REG_iap_serie2_caso0_intento1_v1.md`). El nombre lo decidís vos; declaralo en el commit.
- Sacá la marca de "Borrador" del encabezado y dejá una línea: *aprobado por delamor el 20 oct 2026*.
- **El contenido no cambia.** Las referencias que apunten al path viejo, actualizalas (`grep -rn REG_borrador_serie2_caso0_intento1`).

## 2. Hueco de declaración: pool con ≤ top_k términos

Lo encontré leyendo, no corriendo nada:

- `services/node_extractor.py`, `_seleccionar` (~línea 561): si `len(orden) <= self.top_k`, **entran todos los términos del pool**, sin regla de empate, y N = |pool| < top_k.
- `docs/defs/DECLARACION_extraccion_W_v2.md`, operador 5: dice "con empates, la cantidad de nodos puede no ser top_k" y el caso límite N = 0, pero **no dice este caso**. Con corpus chicos y `min_df = 2` puede pasar: es un criterio que **no aplica por volumen**, y hoy nadie lo decidió en voz alta.

Pedido: **declararlo, no cambiar el código.**
- Una frase en el operador 5 de la v2, por ejemplo: *"Si el pool tiene ≤ top_k términos, entran todos: N = |pool| < top_k y la regla de empate no actúa."* Si leés el código distinto, corregí la frase (regla 2) y decímelo.
- Si `declaracion()` del extractor tiene que coincidir con el documento (hay un test para eso), actualizá los dos juntos, con su docstring.
- Un test que fije este caso: un corpus chico donde menos de top_k términos llegan a `min_df`, y que N sea el tamaño del pool.

**Fuera de alcance:** la condición de "COCO conectado" (abierta, es de delamor), el intento 2 (la consigna con mensajes cortos todavía no está decidida) y el conteo del umbral de 30.

A1.PAUSA al terminar, con el reporte.

Para Code: lo de arriba, nada más.
