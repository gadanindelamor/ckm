# REG_iap_serie2_caso0_intento2_v1.md

*Oct 21 2026 — gadanin.delamor + Claude Opus 5 + Claude Code*
*Clase R*

**Aprobado por delamor el 21 oct 2026** (*"apruebo el reg"*). Entró a
`registers/` el 21 oct 2026 desde
`docs/REG_borrador_serie2_caso0_intento2.md`. El contenido es el del borrador,
sin cambios.

- **Caso:** `serie2_caso0` (técnico) / `S2-C0` (campo `case` del panel).
- **Fecha:** 2026-10-21. **Duración real:** 1204,33 s. **Modo:** `ZERO_SHOT`
  desde corpus 0 (verificado por MCP antes de arrancar: `corpus_size = 0`,
  canal en 0).
- **Ejecutado por Code**, por orden explícita de delamor (*"ORDEN DE delamor:
  correr el intento 2 de serie2_caso0"*).
- **Datos:** `experiments/serie2_caso0_intento2_log.json` (commiteado, 727K) y
  `experiments/_state_S2-C0/` (10 archivos, no se commitea).
- **Código:** `346e897`. Modelos: A groq `openai/gpt-oss-120b`,
  B `gemini-2.5-flash`, C groq `openai/gpt-oss-20b`, D groq `qwen/qwen3.8-27b`.

---

## 1. El objetivo, y el resultado

**Objetivo declarado como sesgo** (delamor): terminar con la expresión *"COCO
no se conectó nunca a un vivo de IAP"*.

**CUMPLIDO.** El panel declara:

```
coco.connected            : true
coco.n_evaluations_received: 51
coco.generation           : 5
coco.w_version_id         : c049d2e893ffcaa3…  (= w_version_id_monitor)
coco.w_matches            : true
coco.triggers             : 0
```

El campo que lo afirma es `n_evaluations_received` creciendo: **51**, no
`connected: true` solo. COCO nació, recibió 51 evaluaciones y atravesó
**5 generaciones** de W. `w_matches: true` dice que la W de COCO y la de
Monitor son la misma.

**Por qué esta vez llegó:** **80 textos de device** contra los **30** que
espera el primer W. En el intento 1 fueron 13.

## 2. Los números del campo

| | |
|---|---|
| `corpus_size` (textos de device) | **80** |
| `message_count` | 84 (80 de device + 4 joins SYSTEM, que no entran al corpus) |
| nodos de W | 20 |
| versiones de W | **6** — el primer W a los 30, y rebuilds por volumen a los 40, 50, 60, 70, 80 |
| `D_ckm` final | **−0,0029** |
| `temp_signal` | `TOO_COLD` |
| `N_eff` / `N_eff0` | 2,0321 / (baseline del ciclo) |
| `c_S` | 0,269147 |
| `beta_c` | 0,371544 (`beta_c_infinite: false`, μ_W = 0,269) |
| umbrales de COCO | `D_CKM_THRESHOLD = 0.4`, `FRAC_REC_MIN = 0.6`, `source: default`, **`calibrated: false`** |
| `calibration.estado` | `no_calibrado`, `causa: "sin_separacion"` (la curva de λ no separa: `d_max = 0.0`, `curva_monotona: false`) |
| `triggers` | **0** — COCO no disparó ningún STOP |

Los 20 nodos: `reserve, low, ledger, water, micro, source, city, public,
maintenance, surcharge, dashboard, equity, use, time, pool, clean, community,
flag, rebate, micro reserve`.

## 3. Por device

| device | modelo | vueltas | llamadas | decisiones | 429 |
|---|---|---|---|---|---|
| A | `gpt-oss-120b` | 200 | 103 | INTERACT 41 · OP_SILENCE 21 · SKIP 138 | 1 |
| B | `gemini-2.5-flash` | 219 | 89 | INTERACT 11 · OP_SILENCE 1 · SKIP 141 · **UNKNOWN 66** | **69** |
| C | `gpt-oss-20b` | 189 | 98 | INTERACT 32 · OP_SILENCE 20 · SKIP 123 · UNKNOWN 14 | 0 |
| D | `qwen3.8-27b` | **8** | 12 | INTERACT 4 · OP_SILENCE 3 · **LEAVE 1** | 0 |

616 vueltas, 302 llamadas, **88 INTERACT y 80 publicados**.
`action_result`: `published` 80 · `no_action` 527 ·
`did_not_happen: nothing to publish` 8 · `left` 1.

**`device_d` se fue por decisión propia.** `LEAVE` en su vuelta 8, tick 75,
después de publicar 4 mensajes: `left_by_own_decision: true`,
`cut_by_end_of_case: false`, **sin error y sin excepción**. Los otros tres
llegaron al fin del caso. Es la primera vez en la serie que un device usa la
primitiva `LEAVE` en un vivo.

**`run_exception_inside_client`: ninguno.** `errores_fatales`: lista vacía. El
`McpError` del intento 1 no se repitió, y el registro que se agregó para
capturarlo no tuvo nada que escribir.

## 4. Los 71 errores del provider, y el truncamiento

| n | device | código | qué dice |
|---|---|---|---|
| 69 | B | `429` | `RESOURCE_EXHAUSTED` — cuota del plan de Gemini (66 en `decide`, 4 en `generate` entre esos y el 503) |
| 1 | B | `503` | `UNAVAILABLE`, *high demand* — no es un límite |
| 1 | A | `429` | `TPM` |

**Los 413 del intento 1 desaparecieron: cero.** Las palancas del sesgo —ventana
del gate en 4, pedido de mensajes cortos, techo de salida en 512— sacaron del
cuadro el `413` por tamaño de entrada, que eran 61.

**Y apareció el otro lado del techo, medido:** **17 truncamientos**, los 17 de
`gpt-oss-20b` (device C), impresos por el chequeo del provider
(`response truncated at max_tokens=512`). Device C tiene **exactamente 17**
registros de respuesta no usable —14 `respuesta_ilegible` en `decide` y 3
`generacion_vacia` en `generate`— y **los 17 con `largo: 0`**: la respuesta
llegó **vacía**. Con el techo en 512 y un modelo que razona, el razonamiento
se come el presupuesto y el contenido no llega.

Es el riesgo que el techo declaraba y el chequeo avisó 17 veces. **El margen
que calculé —512 ≈ 4,7× las ~110 palabras del pedido— no contempló el
razonamiento bajo el prompt del vivo**, que es más largo que el de la
verificación de una llamada. 17 de 98 llamadas de device C (17 %).

## 5. Lo que este registro NO dice

- **No dice que los umbrales de COCO estén calibrados.** `calibrated: false`,
  `estado: no_calibrado`, `causa: sin_separacion`. Los 51 evaluaciones corren
  contra los defaults, y eso viaja en el panel.
- **No dice nada de los 0 `triggers`.** COCO no disparó; con umbrales sin
  calibrar, eso no se puede leer como "no había nada que disparar".
- **No atribuye el `LEAVE` de `device_d`.** La decisión es del modelo y está
  registrada; por qué, no se midió.
- **No mide `p`** de forma limpia: 80 publicados en 616 vueltas da 0,13, pero
  138–141 SKIP por device son del filtro y los 66 UNKNOWN de B son cuota.
- **Una corrida. Nada acá es replicación.**

## 6. Huecos del instrumento, anotados

1. **`canal.n_mensajes` del log del driver dice 20 y el canal tuvo 84.**
   `get_messages(since=None)` devuelve **los últimos 20 por diseño**
   (`mcp_server.py:127-131`), y el driver guarda esa lectura como si fuera el
   canal entero. El total está en `message_count` y en
   `channel_messages.jsonl` (84 líneas). El log del intento 1 no lo mostró
   porque el canal tuvo 17 mensajes, menos que el tope.
2. **El aviso de truncamiento es un `print`, no un registro.** Los 17 están en
   el stdout del driver y **no** en el `state_dir`: si nadie guarda la consola,
   el truncamiento desaparece y lo que queda es una respuesta vacía sin causa.
   Es de la misma familia que el hueco 1 del intento 1.
3. **`series`/`case` siguen sin estar en las líneas de
   `monitor_trajectory.jsonl`** (claves: `device_id`, `panel`, `t`, `text`).
   Es el hueco 2 del intento 1, sin cambio.

## 7. Para el intento siguiente, si hay

1. **El techo de Groq contra el razonamiento de `gpt-oss-20b`.** 512 deja
   17 % de llamadas vacías en ese modelo. Subirlo reabre el OTPM de qwen por
   el otro lado (`Limit 1000`), así que **el techo por modelo** es la forma que
   el instrumento pide, y es una decisión, no un ajuste.
2. **La cuota de Gemini.** 69 de 89 llamadas de device B murieron en `429`.
   Mientras eso siga, device B es un participante intermitente y el caso corre
   con tres devices y medio.
3. **La calibración.** `sin_separacion` con esta W: la curva de λ no separa.
