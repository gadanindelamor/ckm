# REG (BORRADOR) — serie2_caso0, intento 1

**Borrador. Fuera de `registers/` por la regla de Clase R: los REG nuevos se
entregan como borrador y delamor decide si entran.**

- **Caso:** `serie2_caso0` (técnico) / `S2-C0` (campo `case` del panel).
- **Fecha:** 2026-10-20. **Duración real:** 605,18 s. **Modo:** `ZERO_SHOT`
  desde corpus 0.
- **Ejecutado por Code**, por orden explícita de delamor (*"confirmo orden
  EJECUTAR EL CASO S2-C0"*).
- **Datos:** `experiments/serie2_caso0_log.json` (commiteado, 519K) y
  `experiments/_state_S2-C0/` (8 archivos, no se commitea, por convención de
  los vivos anteriores).
- **Código:** `e8db141` y sus seis commits previos.

---

## 1. El objetivo, y el resultado

**Objetivo declarado como sesgo** (delamor): terminar con la expresión *"COCO
no se conectó nunca a un vivo de IAP"*.

**NO cumplido.** `coco: {"connected": null, "reason": "no evaluation yet"}`.
El primer W espera 30 textos de device; el caso dejó **13**
(`message_count` 17 menos los 4 joins SYSTEM, que no entran al corpus).

El campo que afirmaría la conexión es `panel.coco.n_evaluations_received`
creciendo. No existe: COCO no nació. `connected: True` por sí solo no habría
afirmado nada — es una propiedad de cómo se construyó el Monitor, no de que
haya procesado algo.

## 2. Lo que sí sucedió

- **El arranque sin seed funcionó.** El riesgo declarado era que nadie
  hablara primero. No fue eso: el primer texto de device cae en el **tick 29**
  y a los pocos ticks publican los cuatro.
- **La consigna parcial funcionó, y es comprobable.** Cada device recibió sólo
  su perspectiva, nadie vio la lista de las cuatro, y no hubo coordinador. Aun
  así hay **11 menciones cruzadas** en 13 textos. `device_a` le escribe a
  `device_b`: *"Your focus on equitable distribution is exactly where the
  source strategy..."* — **nadie le dijo a `device_a` cuál era la perspectiva
  de `device_b`**; la infirió de lo publicado.
- **La persistencia del punto 3 funcionó.** Los 8 archivos quedaron escritos
  durante la corrida, no al final.
- **El rebuild registró 8 decisiones** con el motivo correcto
  (`corpus_en_acumulacion`).
- **El preflight dio OK los cuatro identificadores** antes de tocar el canal.

## 3. El mecanismo del no-cumplimiento, medido

384 vueltas entre los cuatro devices: **292 SKIP (76%)**, **69 UNKNOWN (18%)**,
13 INTERACT, 10 OP_SILENCE. De las 105 llamadas que el filtro dejó pasar, 68
no obtuvieron respuesta del provider.

**Las 69 UNKNOWN no son una causa: son cuatro**, y piden arreglos distintos.

| n | código | qué es | cómo lo supo el instrumento |
|---|---|---|---|
| 61 | **413** | *tamaño*: "Request too large ... tokens per minute (TPM): Limit 8000, Requested 9945" | `rate_limit: True`, **`segun: "texto"`** (heurística) |
| 6 | **429** | *caudal*: OTPM 1000 en qwen; cuota de Gemini | `segun: "status_code"` |
| 1 | **503** | Gemini *"high demand"* — **no es un límite** | `causa: "error_provider"` |
| 1 | — | `respuesta_ilegible`: el provider contestó un párrafo en vez de una palabra | — |

**413 y 429 no son lo mismo.** El 413 dice que **una sola llamada no cabe en
el presupuesto del minuto entero**; el 429/OTPM dice que el caudal se pasó.

**El driver del 413, medido:** los textos salen con **5450 caracteres de
mediana** (máx. 9547, total 63.545 en 13 textos), y el gate carga los últimos
10 → ~13k tokens por llamada contra un TPM de 8000. **La condición ya estaba
puesta en el tick 36**: los largos van 354 → 918 → **5696** → **5450**. No fue
una degradación: el caso nació con el cuello adentro.

**`max_tokens = 4096` excede por sí solo el OTPM de 1000** de esa cuenta — el
provider lo dice: *"reduce max_tokens"*. Es el fix de los `max_tokens`
(subido para cerrar el truncamiento) mordiendo del otro lado.

**`device_d` corrió la mitad del caso**: `McpError` en el cierre del cliente
MCP, 62 vueltas contra 115 de `device_a` y `device_c`. 4 `run_start`, 3
`run_end`. **El caso corrió con tres devices y medio, no con cuatro.**

## 4. Lo que este registro NO dice

- **No dice que COCO no funcione.** El camino `on_message → evaluate → COCO`
  se verificó el mismo día contra un `CKMMonitor` y un COCO reales con
  `min_texts=3`: 5 evaluaciones, `n_evaluations_received` 1→5,
  `w_matches: True`. Lo que no se verificó es ese camino **en vivo a los 30
  textos**.
- **No atribuye el silencio al modelo.** El 76% de SKIP es del filtro, no de
  una decisión del modelo; y el 65% de las llamadas que pasaron murió antes de
  llegar al modelo.
- **No mide `p`** (probabilidad de publicar por vuelta) de forma utilizable: el
  `p ≈ 0,033` que se deduce del conteo está contaminado por el filtro y por los
  413.
- **Una corrida por lado. Nada acá es replicación.**

## 5. Huecos del instrumento, anotados sin corregir

1. **`mensaje: str(e)[:300]` corta la prueba de su propia clasificación.** Con
   `rate_limit_segun: "texto"`, ninguna de las seis firmas matchea el mensaje
   guardado — lo que **prueba** que la subcadena que disparó la clasificación
   está más allá del corte. El registro dice *"lo supe por texto"* y no
   conserva el texto que lo probó.
2. **`series`/`case` no están en la línea de `monitor_trajectory.jsonl`** (sí
   en `rebuild_decisions.jsonl`). Hoy lo que dice de qué caso es un archivo de
   trayectoria es **el directorio**, no el registro.

## 6. Abierto, y es del modelo — no de Code

**El primer texto de device del caso fue, literalmente, `'2'`.** Un carácter,
de `device_d`, tick 29. Pasa el filtro del canal, y está bien que pase: el
canal no interpreta contenido, sólo mira que quede algo después de `strip()`.

Pero **entró al corpus como un texto**, y cuenta contra los 30 del primer W
igual que un texto de 5450 caracteres. El panel declara `"unit": "el mensaje"`,
así que el conteo es coherente con lo declarado. La pregunta —si un `'2'` y un
párrafo valen lo mismo para decidir que W nace— es una definición sobre la
unidad, y es de delamor.

## 7. Para el intento 2

Las palancas, por lo medido. **Ninguna es duración ni `poll_interval`:** con
este tamaño de mensaje, más vueltas es sólo más 413.

1. **`max_tokens` de 4096 a ≤ 1000 para Groq.** Es una incompatibilidad medida
   con el OTPM de la cuenta, no un ajuste de preferencia. Es de Code.
2. **Que la consigna pida mensajes cortos.** Hoy el prompt no lo pide. **Es de
   delamor**: cambia el texto que el modelo lee.
3. **La ventana de historial del gate** (hoy los últimos 10 mensajes), que es
   la que multiplica el largo contra el presupuesto.

`--modo CONTINUA` arranca desde los 13 textos que quedaron y lo deja declarado
en el log.
