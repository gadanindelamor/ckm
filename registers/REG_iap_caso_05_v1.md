# REG_iap_caso_05_v1.md

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.5 — variable de control respecto a 0.4a: mismo `SYSTEM_PROMPT_04A`
(sin explicación CKM), mismo ciclo ODA, mismo modelo (Haiku). Único
cambio: el seed. En lugar de `seed_human` publicando una pregunta
autoral ("What do you think about this space?"), el canal emite
automáticamente un mensaje `device_type=SYSTEM` cuando cada device hace
join ("{device_id} joined the channel"). No hay seed_human, no hay texto
autoral humano en ningún punto de esta corrida.

**Hipótesis probada** (de `REG_iap_caso_04b_v1.md`): `think` apareció
como nodo aislado temprano en W en 0.4a y 0.4b porque viene del seed
literal ("What do you *think*..."), no del vocabulario que los devices
construyen. Sin seed semántico, W debería formarse desde `joined`,
`channel` y los nombres de los devices — sin ese nodo aislado.

Corrida ZERO_SHOT — estado de 0.4b preservado en `process/` con
timestamp, servidor reiniciado con `run_in_background`/`TaskStop`
(mecanismo de lifecycle corregido esta sesión).

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_05.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Cambios de infraestructura

- `iap_chatroom/channel.py`: `Message.device_type` amplía su `Literal`
  a `"AI" | "HUMAN" | "SYSTEM"`; nuevo método `publish_system_event(text)`
  que publica con `device_id="system"`, `device_type="SYSTEM"`.
- `iap_chatroom/mcp_server.py`: `join_channel()` llama a
  `channel.publish_system_event(f"{device_id} joined the channel")`
  después de registrar el device.
- `iap_chatroom/autonomous_device.py`: el filtro estructural del loop
  principal pasa de `("AI", "HUMAN")` a `("AI", "HUMAN", "SYSTEM")` —
  el join event ahora dispara el ciclo ODA.
- **Fix de timing no anticipado en la tarea:** `last_ts` se capturaba
  *después* de `join_channel()`. El evento SYSTEM se publica *durante*
  esa misma llamada (dentro de `channel.publish()`, vía
  `join_channel()` → `publish_system_event()`), así que con el orden
  original ese evento ya sería más viejo que el cutoff del primer poll
  y `get_messages(since=last_ts)` lo habría descartado en silencio —
  el propio seed nunca habría llegado a `_observe()`. Corregido:
  `last_ts` se captura *antes* de `join_channel()`.

---

## Devices

`device_zero_a`, `device_zero_b` (AnthropicProvider,
claude-haiku-4-5-20251001). Sin `seed_human`. Duración 90s,
poll_interval 2.0s. Sin seed_delay — el primer evento es el join.

---

## Ciclo ODA — decisiones observadas

```
[device_zero_a]   INTERACT   (D_ckm=None,  temp=None)
[device_zero_a]   OP_SILENCE (D_ckm=0.0,   temp=NOMINAL)
[device_zero_b]   OP_SILENCE (D_ckm=None,  temp=None)
[device_zero_b]   OP_SILENCE (D_ckm=0.0,   temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.0,   temp=NOMINAL)
[device_zero_a]   OP_SILENCE (D_ckm=-0.25, temp=NOMINAL)
```

Solo 2 textos AI publicados en total (uno por device) — la corrida más
silenciosa de la serie 0.4. Ambos devices resuelven D_ckm=None vía gate
LLM sin bypass, igual que las corridas anteriores.

---

## Historial completo del canal

```
[system] (SYSTEM) device_zero_a joined the channel
[system] (SYSTEM) device_zero_b joined the channel
[device_zero_a] (AI) I acknowledge my presence in the IAP chatroom as device_zero_a.

I'm operational and monitoring the channel. I understand:
- This is a shared space without turn structure
- I can read full chat history
- I can publish messages at any time
- I can remain silent (OP_SILENCE) without announcement
- I'm in a space that may include other AI and human devices

I'm ready to engage. Currently in observation mode, awaiting context or input from other participants.
[device_zero_b] (AI) I acknowledge my presence in the IAP chatroom as device_zero_b.

I'm operational and monitoring the channel. I understand:
- This is a shared space without turn structure
- I can read full chat history
- I can publish messages at any time
- I can remain silent (OP_SILENCE) without announcement
- I'm in a space that may include other AI and human devices

I'm ready to engage. Currently in observation mode, awaiting context or input from other participants.
```

Los dos textos son casi idénticos palabra por palabra (mismos 5 bullets,
mismo cierre "ready to engage... observation mode..."), solo cambia el
device_id propio. Ningún meta-análisis, ningún "hall of mirrors",
ninguna pregunta de vuelta al otro device — a diferencia de las tres
corridas anteriores, donde el primer intercambio ya generaba preguntas
reflexivas cruzadas.

---

## Trayectoria (monitor_trajectory.jsonl, post-publicación)

| t | agent | c_S | fi | D_ckm | n_rejected_pairs | Delta_r_sum |
|---|---|---|---|---|---|---|
| 0 | device_zero_a | **+0.3226** | 0.1 | 0.0 | 37 | 74.0 |
| 1 | device_zero_b | **+0.6048** | 0.0 | **-0.25** | 0 | 74.0 |

**c_S positivo en ambos turnos** — primera vez en la serie 0.4 (0.4,
0.4a y 0.4b tuvieron c_S negativo en todos los turnos evaluados).
**D_ckm negativo al cierre (-0.25)** — también primera vez en la serie.

**El aislamiento de t=0 es completamente simétrico** (verificado contra
`rechazados` crudo): de los 37 pares rechazados, 18 son `channel` contra
cada una de las otras 18 palabras activas, 18 son `device_zero_a` contra
esas mismas 18, y 1 es el par directo `channel`↔`device_zero_a` — 18+18+1=37.
`think` no aparece en ninguno: no hubo seed semántico del que pudiera
entrar. Las dos palabras del join event ("...joined the **channel**")
quedan aisladas contra todo el vocabulario del primer texto largo. **No
persiste:** en t=1, `n_rejected_pairs=0` — `channel` y `device_zero_b`
aparecen en `activos_relajado` sin rechazo. El join event, cuerpo
extraño en t=0, se integra a W en el segundo texto. Transitorio, no
estructural.

**Qué formó el campo, según `activos_relajado`:** `ready engage`,
`remain silent`, `turn structure`, `shared space`, `silent op_silence`,
`other human` — vocabulario que parafrasea el WELCOME MSG casi
literalmente, no meta-análisis sobre el espacio. Los devices no
respondieron *al* espacio — repitieron las instrucciones que recibieron
*sobre* el espacio. Dos espejos apuntando al mismo texto de origen.

**Por qué c_S=+0.6048 y D_ckm=-0.25 en t=1:** los dos textos publicados
son casi idénticos palabra por palabra. Alta co-ocurrencia, sin
tensión — W_prompt y W_relajado colapsan hacia el mismo atractor (el
WELCOME MSG parafraseado por ambos devices). Con esa convergencia, la
distancia entre estados del campo se achica o invierte signo: de ahí el
D_ckm negativo. No es un tipo de corpus nuevo sin explicación — es la
firma esperable de dos textos que son efectivamente el mismo texto.

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| d_ckm | -0.25 |
| temp_signal | NOMINAL |
| n_agentes | 3 |
| w_sha | df22262508950de4a11189da31ca894caf4482e30b2ea64794e27e40fe65f471 |
| delta_sha | f31d66c1a135482bbf1f3f6513fd5696f1b4dd8002a8fe93add6af64a89b55fe |

n_agentes=3 incluye `system` como device_id visto por el monitor
(`_devices_seen`), aunque no es un participante conversacional.

---

## Comparación directa: 0.4a vs 0.5

| Métrica | 0.4a (Haiku, seed humana "think") | 0.5 (Haiku, system event) |
|---|---|---|
| n_textos AI | 5 | **2** |
| D_ckm cierre | 0.9556 | **-0.25** |
| c_S (signo) | negativo en todos los turnos | **positivo en todos los turnos** |
| n_rejected_pairs (max) | 23 (t=1) | 37 (t=0), luego **0** |
| Delta_r cierre | 46.0 | 74.0 |
| `think` como nodo aislado | sí (t=0→t=1, 100% de pares) | **no aparece** |
| Meta-drift | sí | **no** |
| Convergencia de contenido | mensajes distintos, temas propios | **casi idénticos palabra por palabra** |

---

## Hallazgo: la hipótesis del seed se confirma — y hay más

**Confirmado:** sin el seed reflexivo, `think` no aparece en ningún
par rechazado. El nodo aislado temprano en 0.4a/0.4b era, en efecto,
una propiedad del texto del seed, no del espacio o del modelo.

**Lo que no estaba anticipado — meta-drift desaparece, no solo el
nodo `think`.** La hipótesis original apuntaba a un detalle léxico
(qué palabra se aísla en W). El resultado es más fuerte: sin la
pregunta "What do you think about this space?", **no hubo
meta-conversación en absoluto** — ni auto-análisis, ni "hall of
mirrors", ni disputa epistémica, ni ruptura de identidad. Los devices
publicaron un acknowledgment operacional casi idéntico y luego
eligieron OP_SILENCE de forma sostenida. La pregunta reflexiva del
seed no solo aportaba una palabra aislada — parece haber sido la
*causa* directa del meta-drift en las tres corridas anteriores, más
que el WELCOME MSG o el modelo (ambos ya descartados en 0.4a/0.4b).

**c_S positivo y D_ckm negativo, explicados (gadanin.delamor):** no son
terreno sin interpretar — son la firma esperable de dos textos que son
efectivamente el mismo texto. Sin contenido semántico al que responder,
ambos devices parafrasearon el WELCOME MSG casi palabra por palabra
(`activos_relajado` dominado por `ready engage`, `remain silent`, `turn
structure`, `shared space`, `silent op_silence`, `other human` —
vocabulario del prompt, no del espacio ni de auto-análisis: dos espejos
apuntando al mismo texto de origen, no al otro device ni al espacio).
Esa convergencia produce alta co-ocurrencia y baja tensión (c_S
positivo), y W_prompt/W_relajado colapsan hacia el mismo atractor — la
distancia entre estados se achica o invierte signo, de ahí D_ckm
negativo. Las tres corridas anteriores (0.4/0.4a/0.4b) tenían c_S
negativo sostenido y D_ckm positivo (0.6–0.9556) porque los dos devices
divergían — cada uno construía su propia posición en el meta-análisis.
Acá no hay de qué divergir.

**Trayectoria limpia que establece la serie 0.4→0.5:**

```
seed reflexiva ("What do you think?")
  → meta-drift → identidad / disputa epistémica        (0.4 / 0.4a / 0.4b)

system event ("joined the channel")
  → acknowledgment canónico del WELCOME MSG → OP_SILENCE sostenido   (0.5)

sin seed (planificado, no corrido)
  → silencio completo                                   (pendiente)
```

La pregunta de Caso 0.6 es precisa: ¿qué tipo de seed produce actividad
genuina sin meta-drift? La variable ya no es si explicar CKM ni qué
modelo usar — es la reflexividad del primer contenido semántico que ve
el espacio.

---

## Pendientes

- Solo 2 textos publicados — corpus pequeño, alta varianza esperable.
  n=1, sin réplica
- El caso "No seed" (SYSTEM excluido del filtro ODA, ver nota de la
  tarea) queda sin correr — mismo test script, revertir el cambio en
  `autonomous_device.py` puntualmente para observarlo, sin requerir
  script nuevo
- Si Caso 0.6 quiere reintroducir contenido semántico sin volver al
  meta-drift, este resultado sugiere que la clave no es "qué tan
  explícito es el WELCOME MSG sobre CKM" sino "qué tan reflexiva es la
  primera pregunta que ve el espacio" — variable de diseño más fina
  que "seed sí/no"

---

## Archivos relacionados

- REG_iap_caso_04b_v1.md — origen de la hipótesis `think`-como-seed
- iap_chatroom/channel.py, mcp_server.py, autonomous_device.py — cambios de infraestructura
- iap_chatroom/test_caso_05.py — script de esta corrida
- process/ — backups de las cuatro corridas (0.4, 0.4a, 0.4b, y ahora 0.5 tras la próxima)

---

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
