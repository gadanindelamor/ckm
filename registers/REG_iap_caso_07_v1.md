# REG_iap_caso_07_v1.md

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.7 — MCP Resource vs tool para leer el canal en la fase
`_observe()` del ciclo ODA. Variable de control respecto a 0.5: mismo
`SYSTEM_PROMPT_04A` (sin explicación CKM), mismo mecanismo de seed
(join event SYSTEM, sin seed_human), 2 devices con join simultáneo (sin
stagger — a diferencia de Caso 0.6). Lo que cambia: cómo cada device lee
el historial del canal.

- `ClaudeHaiku_4-5-20251001_1` → lee vía **MCP Resource**
  (`iap://canal/mensajes`, `client.read_resource()`)
- `ClaudeSonnet_5_2` → lee vía **tool** `get_messages` (control, sin cambios)

Repo: `gadanindelamor/ckm` — `iap_chatroom/mcp_server.py`,
`iap_chatroom/test_caso_07.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Prerequisito verificado antes de escribir código

`fastmcp==3.4.4` (`pip show fastmcp`). Probado en un servidor FastMCP
descartable, no solo inferido de la documentación:

- `Client` no expone `subscribe`/`subscribe_resource` — solo
  `read_resource`/`read_resource_mcp` (pull, no push).
- `FastMCP` (servidor) no expone un helper público para emitir
  `ResourceUpdatedNotification` — solo `resource`/`add_resource`/`get_resource`.
- El protocolo MCP subyacente (`mcp.types`) sí define
  `SubscribeRequest`/`ResourceUpdatedNotification`, pero fastmcp no los
  envuelve en su API pública en esta versión.

Conclusión: solo lectura (pull) implementada. Sin push/notificaciones —
documentado en el docstring de `canal_mensajes()` en `mcp_server.py`.
No se instaló otra versión de fastmcp para esto.

---

## Cambios de infraestructura

- `iap_chatroom/mcp_server.py`: nuevo `@mcp.resource("iap://canal/mensajes")`
  → `canal_mensajes()`, devuelve la lista completa de mensajes del canal
  desde t=0, mismo formato que `get_messages()` (incluye `message_id`).
  Verificado en proceso antes de la corrida real: responde `[]` con
  canal vacío, formato correcto.
- `iap_chatroom/test_caso_07.py`: `ResourceReadingDevice(AutonomousDevice)`
  — subclase que sobreescribe únicamente `_observe()` para usar
  `client.read_resource("iap://canal/mensajes")` en vez de
  `client.call_tool("get_messages", ...)`. `_decide()`, `_interact()`,
  el polling de mensajes nuevos y join/leave en `run()` quedan
  heredados sin cambios.

**`autonomous_device.py`, `channel.py`, `ckm_monitor.py`, `server.py` no
se modificaron** — confirmado con `git status --porcelain` antes de
correr. La necesidad de decidir entre "tocar `autonomous_device.py`" y
"subclasear" se reportó a gadanin.delamor antes de ejecutar, aun cuando
la solución (subclase) no requería la excepción — ver
`registers/REG_iap_caso_06_v1.md` y memoria de sesión sobre la regla
NO MODIFICAR.

---

## Run 1 — resultado

| Criterio | Resultado |
|---|---|
| Resource accesible, devuelve historial correcto | ✅ |
| Haiku_1 lee vía resource (verificable en log) | ✅ — `_observe via RESOURCE` en cada ciclo |
| Sonnet_2 lee vía tool (control) | ✅ — sin cambios, `AutonomousDevice` base |
| corpus_size crece con cada texto publicado | ❌ — no se llegó a probar, 0 textos AI publicados |
| Firma_CKM completa al cierre (6 campos) | ❌ — `None`, corpus nunca alcanzó `min_texts=3` |
| Log distingue resource vs tool | ✅ |

**Verificado contra `process/corpus_state.json.bak_1784601161_caso07`:**
`texts` = 2 exactos (`"ClaudeHaiku_4-5-20251001_1 joined the channel"`,
`"ClaudeSonnet_5_2 joined the channel"`), `w_version_history` = `[]`
(W nunca se construyó). No existe `monitor_trajectory.jsonl.bak_*_caso07`
— cero evaluaciones ocurrieron (corpus nunca llegó a 3 textos).

## Log de decisiones

```
[ClaudeHaiku_4-5-20251001_1] _observe via RESOURCE (iap://canal/mensajes)
[ClaudeHaiku_4-5-20251001_1] OP_SILENCE (D_ckm=None, temp=None)
[ClaudeHaiku_4-5-20251001_1] _observe via RESOURCE (iap://canal/mensajes)
[ClaudeSonnet_5_2] OP_SILENCE (D_ckm=None, temp=None)
[ClaudeHaiku_4-5-20251001_1] OP_SILENCE (D_ckm=None, temp=None)
[ClaudeSonnet_5_2] OP_SILENCE (D_ckm=None, temp=None)
```

Ambos devices en OP_SILENCE en cada decisión. Ningún texto AI publicado.
Historial completo del canal al cierre: solo los 2 join events SYSTEM.

---

## Run 1.1 — segunda pasada, misma configuración exacta

Réplica pedida por gadanin.delamor para descartar varianza de sampling
antes de sacar conclusiones. Mismo script, mismos devices, mismo
mecanismo, corpus limpio (estado de Run 1 preservado en
`process/*_1784601161_caso07` antes de reiniciar servidor).

**Resultado: réplica exacta.** Mismo patrón de decisiones
(Haiku OP_SILENCE → Sonnet OP_SILENCE → Haiku OP_SILENCE → Sonnet
OP_SILENCE), mismo corpus final. Verificado contra
`process/corpus_state.json.bak_1784602904_caso07`: `texts` = exactamente
los mismos 2 strings que Run 1 (`"ClaudeHaiku_4-5-20251001_1 joined the
channel"`, `"ClaudeSonnet_5_2 joined the channel"`), `w_version_history`
= `[]`. Cero divergencia entre las dos corridas.

---

## Lectura — infraestructura validada, silencio confirmado robusto (2/2)

El objetivo técnico de Caso 0.7 (resource vs tool como mecanismo de
lectura) se cumple: el resource funciona, Haiku_1 lo usó en cada ciclo
sin error en ambas corridas, el log distingue ambos mecanismos con
claridad. Pero ninguna de las dos corridas generó corpus suficiente
para comparar el efecto del mecanismo de lectura sobre el contenido —
silencio total no deja nada que comparar entre "lo que vio Haiku_1 vía
resource" y "lo que vio Sonnet_2 vía tool", más allá de que ambos
vieron lo mismo (2 join events) y ambos callaron, dos veces seguidas.

**Punto que no se puede pasar por alto — contradicción con Caso 0.6,
ahora con dos corridas de respaldo:** Caso 0.5 (2 devices, mismo
mecanismo de join simultáneo sin stagger, pero 2 **Haiku idénticos**)
produjo actividad — 2 textos publicados. Acá, con Haiku+Sonnet
(**heterogéneo**) bajo el mismo tipo de join simultáneo, silencio total
— replicado dos veces. Es el resultado opuesto al que predeciría la
hipótesis de ruptura de simetría propuesta en `REG_iap_caso_06_v1.md`
("heterogeneidad en el grupo → rompe el equilibrio de silencio"), y ya
no se explica fácilmente como varianza de sampling de una sola muestra
— dos corridas independientes dieron el mismo resultado exacto.

**Sigue sin poder aislarse la causa entre las dos corridas de Caso
0.7 mismas:** (1) composición de modelos (mono→hetero respecto a 0.5) y
(2) mecanismo de lectura de Haiku_1 (tool→resource) cambian juntas
respecto al baseline de 0.5. La réplica exacta descarta "fue ruido de
sampling en Run 1", pero no distingue entre esas dos causas — para eso
hace falta la corrida de control descrita en Pendientes (Haiku+Sonnet
por tool en ambos, sin resource).

---

## Run 2 — control sin resource (aísla la causa)

Script separado: `iap_chatroom/test_caso_07_run2.py`. Mismos 2 devices
(Haiku_1, Sonnet_2), mismo join simultáneo sin stagger, mismo
`SYSTEM_PROMPT_04A` — pero ambos usan `AutonomousDevice` base sin
subclase, ambos leen vía tool `get_messages`. Sin resource en absoluto.

**Resultado: silencio total, otra vez idéntico.** Mismo patrón de
decisiones (Haiku OP_SILENCE → Sonnet OP_SILENCE → Haiku OP_SILENCE →
Sonnet OP_SILENCE), mismo corpus final. Verificado contra
`process/corpus_state.json.bak_1784667824_caso07_run2`: `texts` =
exactamente los mismos 2 strings que Run 1 y Run 1.1
(`"ClaudeHaiku_4-5-20251001_1 joined the channel"`,
`"ClaudeSonnet_5_2 joined the channel"`), `w_version_history` = `[]`.

**Conclusión — causa aislada:** el resource NO explica el silencio.
Run 2 (sin resource, ambos por tool) replica exactamente el mismo
resultado que Run 1/1.1 (Haiku por resource). Tres corridas
independientes, mismo resultado exacto, con y sin la variable resource
presente. El silencio es propiedad de la combinación **Haiku+Sonnet
bajo join simultáneo** — no del mecanismo de lectura del canal.

Esto deja la contradicción con la hipótesis de ruptura de simetría de
Caso 0.6 (`REG_iap_caso_06_v1.md`) más firme, no más débil: con la
variable resource descartada, el contraste directo es Caso 0.5 (2 Haiku
idénticos, join simultáneo → actividad) vs Caso 0.7 (Haiku+Sonnet
heterogéneo, mismo tipo de join simultáneo → silencio, 3/3).
Heterogeneidad de modelo no rompió el silencio acá — lo sostuvo.

**Patrón cruzado, verificado contra las 4 configuraciones corridas
hasta ahora** (0.5, 0.6 R1/R2/R3, 0.7 R1/R1.1/R2) — no solo
heterogeneidad, también el *timing* del join (simultáneo vs
escalonado, DELTA_T=5s):

| | join simultáneo | join escalonado (DELTA_T=5s) |
|---|---|---|
| **mono-modelo** | 0.5: actividad (1/1) | 0.6 R2, R3: silencio (2/2) |
| **hetero-modelo** | 0.7 R1, R1.1, R2: silencio (3/3) | 0.6 R1: actividad (1/1) |

Patrón sin excepciones en los datos recolectados: actividad aparece en
las combinaciones "misma condición en ambos ejes" (mono+simultáneo,
hetero+escalonado); silencio aparece en las combinaciones "cruzadas"
(mono+escalonado, hetero+simultáneo). Ni "heterogeneidad" ni "timing"
solos explican el patrón completo — la interacción entre ambos sí, al
menos con los datos disponibles. Nota: 0.5/0.7 son corridas de 2
devices, 0.6 de 4 — el tamaño del grupo es una variable más sin
controlar, no incluida en esta tabla.

n=1 a 3 por celda, ninguna celda con réplica cruzada de tamaño de
grupo. Patrón interesante para próximas sesiones, no una conclusión
cerrada.

---

## Pendientes

Corridas de Caso 0.7 completas: Run 1, Run 1.1 (réplica exacta) y
Run 2 (control sin resource) — las tres documentadas arriba. Causa ya
aislada: el resource no explica el silencio. Lo que sigue pendiente:

- El patrón cruzado heterogeneidad × timing de join (tabla arriba) no
  tiene ninguna celda con réplica controlando tamaño de grupo — 0.5/0.7
  son corridas de 2 devices, 0.6 de 4. Un Caso 0.8 con 2 devices
  hetero + join escalonado (o 2 devices mono + simultáneo repetido)
  llenaría la tabla sin ese confound.
- No se probó ningún caso de Caso 0.7 con contenido real publicado —
  el objetivo original de comparar qué ve cada device (resource vs
  tool) sobre un corpus con texto AI queda sin ejercitar en las tres
  corridas. Considerar sembrar un mensaje SYSTEM o HUMAN adicional para
  forzar corpus_size ≥ 3 y poder comparar contenido real.
- Sin notificaciones push en esta versión de fastmcp — si en el futuro
  se actualiza fastmcp, revisar si expone `subscribe`/`resource_updated`
  y reabrir esa parte de la tarea (opcional, no bloqueante).

---

## Archivos relacionados

- REG_iap_caso_06_v1.md — hipótesis de ruptura de simetría, posible
  contradicción con este resultado
- REG_iap_caso_05_v1.md — baseline de 2 devices, join simultáneo, mono-modelo
- iap_chatroom/mcp_server.py — resource `canal_mensajes()`
- iap_chatroom/test_caso_07.py — script de esta corrida, `ResourceReadingDevice`
- process/corpus_state.json.bak_1784601161_caso07 — datos crudos de Run 1

---

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
