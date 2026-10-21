# Estado al cortar — 21 oct 2026
*Opus 5.5 para la próxima instancia. Reemplaza a `ESTADO_al_cortar_20oct2026.md`. Decisiones con cita: `decisiones_en_el_acto.md` (desde el 19 oct; lo anterior en `decisiones_en_el_acto_13a15oct2026.md`).*

## 0. Al cortar (actualizado al cierre, 21 oct)
- **El Codespace llegó al 100 % del límite** y se cerró. Lo último de Code **puede no estar pusheado**: la re-verificación de los cuatro modelos y un cambio al prompt del generate (*"con el prompt nuevo"*). Code lo hizo con un texto que Opus ya había reemplazado (error de Opus: tres textos seguidos para la misma pausa). Al volver: que Code diga qué tiene sin pushear y lo pushee **sin seguir**.
- **Nada se toca en servicios ni IAP sin verificar antes** (delamor). La propuesta de Opus sobre `OP_SILENCE` en el generate es **lectura, no orden**. El pedido *"Please write your message…"* **no hace falta** según las definiciones (`BLOQUE_COMUN`, convención de chat); si Code lo agregó, se verifica antes de decidir si se saca.
- **Verificar lo de Code con la política de tests** (lista en `decisiones_en_el_acto.md`): completitud, predicción antes del arreglo, suite entera, `test_caso_*` no pytest, stubs antes del vivo, `None` ≠ `UNKNOWN`.
- **Pregunta abierta para delamor:** la ventana del gate en 4, ¿sigue? El gate estaba **congelado en `f96c234`** por delamor (9 oct) y Opus no lo citó al proponerla.
- El server de Code (`:7860`, corpus 0) murió con el Codespace: al volver hay que arrancarlo limpio otra vez antes del vivo. El estado del intento 1 está preservado en `process/`.
- Regla de Opus: **un solo texto para Code por pausa**, cuando la decisión está cerrada.

## 1. En curso
- **Code, parte B del intento 2 de `serie2_caso0`** (texto: `textos_para_code/TEXTO_PARA_CODE_intento2_21oct2026.md`, más la respuesta de Opus a T1–T7 en `decisiones_en_el_acto.md`). Preparar, **no correr**: `max_tokens` Groq ≤ 1000; ventana del gate 10 → 4 y del generate → 10; pedido de mensajes cortos en la consigna; `DURATION` 1200; reporte del `McpError` de `device_d` + registro de su causa interna (A1.PAUSA en B.5); **ZERO_SHOT** con `--reset` y reinicio del server; lectura de qué hace CONTINUA con los json y con el canal.
- El intento 2 **espera la orden de delamor**. Al darla: lanzar en background, no seguirlo; leer el resumen, no el log entero.

## 2. Hecho hoy
- Parte A (Code): REG del intento 1 en `registers/REG_iap_serie2_caso0_intento1_v1.md` (`88ff77e`); operador 5 declara el pool con ≤ top_k (`595d0b7`); reversión de ediciones de traza en `docs/opus/` (`9322256`).
- **Las dos series de IAP son testing**, no experimentos (delamor).
- **El sesgo del paper, nombrado:** "COCO no se conectó nunca a un vivo de IAP" era **la única ausencia nombrada**. La frase **se retira** del paper, sin reemplazo. El objetivo del vivo sigue: **que suceda**.
- **Ver la conexión de COCO en vivo no es necesario** (tests y drivers ya lo chequean). La condición de `connected` (hoy: existe el objeto; `None` antes de la primera evaluación) queda como está.
- Git: en el Codespace, pull y push los hace Code. En la PC, Opus commitea en `docs/opus/` y delamor sube.

## 3. Abierto (de delamor, sin apuro)
- Qué cuenta el umbral del primer W (hoy 30 mensajes; alternativas: unidades con ≥ 2 nodos, o medir cuándo se estabiliza). No se mueve después de un intento fallido sin declararlo como sesgo.
- Pseudoaleatoriedad para perturbar el sesgo (pregunta abierta de delamor).
- Si el intento 2 no llega: CONTINUA (según la lectura de B.7) o el piso de `local_criterion` (de reserva).
- **`CONTINUA` queda sin usar hasta que se arregle lo que la lectura de B.7 encontró** (Opus, 21 oct; línea agregada por Code a pedido de Opus). Dos cosas, medidas: (a) los contadores del rebuild cruzan de un intento al otro —`rebuild_state.json` guarda `w_sha: null` y el guard compara `w_sha`, así que "sin W" es igual a "sin W" y se restauran— y los `message_id` se duplican, porque salen de la posición en el historial en memoria; (b) con el server reiniciado el **canal arranca vacío mientras el corpus tiene los textos**: dos memorias distintas del mismo caso, y W se construiría sobre textos que ningún device presente leyó. El intento 2 va **ZERO_SHOT**.
- La experiencia "leído completo" con Sonnet u otra instancia: delamor la va a señalar.
- Límites de uso: delamor va a pasar dónde publica Anthropic las indicaciones; evaluar estrategia ahí.

## 4. Sin cambio
- Sombra de `calibrate` (propuesta), coordinar REG/BANDEJA/decisiones, mail IAC, CP-N, paper v29 (se revisa con las DEFS v17 y sin la frase de COCO).
