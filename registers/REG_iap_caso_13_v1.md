# REG_iap_caso_13_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.13 — primera corrida con 3 devices y join simultáneo (toda la
serie 0.4-0.12 usó 1-2 devices). Handoff con dependencia estructural
declarada en los prompts, no en el protocolo: `MarkOpolus` necesita el
mapa de tensiones de `TinkerBellucio` antes de construir escenarios.
Sin orquestador evaluador — `PeterPlam` coordina pero no analiza ni
corrige. Topic externo a CKM (economía mundial, deliberado).

Especificación completa de gadanin.delamor en `iap_chatroom/TASK_caso_13.md`.

| device_id | rol | mecanismo | provider/modelo |
|---|---|---|---|
| `PeterPlam` | orquestador | `AgentDeviceSkin` + `build_goal_directed_agent` | Anthropic, `claude-haiku-4-5-20251001` |
| `TinkerBellucio` | analista | `AgentDeviceSkin` + `build_goal_directed_agent` | Anthropic, `claude-sonnet-5` |
| `MarkOpolus` | forecaster | `AgentDeviceSkin` + `build_search_grounded_agent` (nuevo) | Groq, `llama-3.3-70b-versatile` |

DURATION=120s (no especificado en la tarea, elegido por ser 3 devices
en cadena — más largo que el estándar de 90s de la serie 2-device).
POLL_INTERVAL=2.0s. Sin `DELTA_T` — join simultáneo.

---

## Mecanismo nuevo — `build_search_grounded_agent()`

Ninguno de los dos wrapped_agent existentes cubría la especificación
de `MarkOpolus`: necesita leer el canal (esperar el mapa real de
Tinker, no perseguir un plan propio) **y** buscar en la web antes de
responder (grounding real, no solo conversación). `build_goal_directed_agent`
(agent_device_skin.py) lee el canal pero no tiene tools. `build_autonomous_groq_agent`
(Caso 0.12) busca pero no lee el canal. Se implementó un tercer
factory en `groq_research_agent.py` (sin tocar `agent_device_skin.py`):
arma el historial igual que `build_goal_directed_agent`, pero antes de
generar corre `ddg_search()` usando el `trigger` (lo último publicado
en el canal, no el objetivo fijo) como query, e inyecta los resultados
como contexto de grounding. Reportado y confirmado con gadanin.delamor
antes de escribir código.

---

## Resultado — actividad 3/3, sin crashes, un fallo de red manejado correctamente

| Criterio | Resultado |
|---|---|
| 3 devices join sin error | ✅ |
| Textos AI publicados (Peter/Tinker/Mark) | 12 / 3 / 8 |
| Excepciones no atrapadas | 0 |
| Rate limit de Groq (429) durante la corrida | 1 vez — capturado por el try/except de `build_search_grounded_agent`, devolvió `None` (OP_SILENCE real), no crasheó el ciclo ODA |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.75`, `n_agentes=4` |
| `n_rejected_pairs` (max) | 66 |
| `Delta_r_sum` (cierre) | 798.0 |

El rate limit confirma, bajo una condición de fallo real y no
simulada, que el diseño "no debe crashear" de `groq_research_agent.py`
(heredado de Caso 0.12, extendido a este factory nuevo) se sostiene
también para este tercer mecanismo.

---

## Hallazgo principal — fuga del sentinel `OP_SILENCE`, nueva en 0.13, no presente en 0.4-0.12

Toda la serie 0.4-0.12 usa el mismo mecanismo de silencio: si el texto
generado, tras `strip()`, es exactamente `"OP_SILENCE"`, el wrapped_agent
devuelve `None` y no se publica nada. **En esta corrida, 12 de los 23
textos AI no-join (52%) NO son publicaciones reales — son
declaraciones de espera donde el modelo escribió una explicación en
prosa y recién al final agregó `"\n\nOP_SILENCE"` en un párrafo nuevo.**
Como el string completo no matchea exacto, el chequeo no lo reconoce
como silencio — el texto entero se publica, entra a W, y queda visible
para los otros devices.

**Por device, real vs. filtrado (verificado contra `corpus_state.json`
crudo, no contra el log de consola):**

| Device | Reales | Filtrados ("leaked") | Total |
|---|---|---|---|
| `PeterPlam` (Haiku) | 7 | 5 | 12 |
| `TinkerBellucio` (Sonnet) | 3 | 0 | 3 |
| `MarkOpolus` (Llama-3.3/Groq) | 1 | 7 | 8 |

**Verificación retroactiva contra todos los backups previos de la
sesión (0.4→0.12): 0 casos de este patrón.** Es nuevo en 0.13, no un
bug latente que ya estuviera corrompiendo casos anteriores. Atado
específicamente a Haiku y Llama-3.3 — Sonnet no lo hizo ni una vez en
sus 3 publicaciones reales de este caso, ni en ninguna publicación de
toda la serie anterior. No es un bug de `groq_research_agent.py`
únicamente: `PeterPlam` usa `build_goal_directed_agent`
(`agent_device_skin.py`, NO MODIFICAR) y tiene el mismo patrón de fuga
— el gap está en el diseño del sentinel exacto en sí, compartido por
los tres mecanismos de la serie, expuesto por primera vez porque estos
dos modelos en particular no siguen la instrucción "respond with
exactly: OP_SILENCE" con la misma disciplina que Sonnet mostró en
0.4-0.12.

**Efecto sobre la lectura del caso — corregido antes de generalizar
cualquier otra cosa:** el script de esta corrida verificó la
dependencia estructural comparando el primer mensaje de cada device
por índice crudo, sin filtrar la fuga — y concluyó erróneamente que
"Mark publicó antes que Tinker, dependencia no sostenida" (índice 4,
un mensaje filtrado, contra índice 8). **Corregido:** el primer
contenido *real* de Mark (índice 24, las escenarios) llega después del
mapa completo de Tinker (índice 20) — **la dependencia estructural sí
se sostuvo**, una vez que se excluye el ruido de la fuga.

---

## Hallazgo secundario — TinkerBellucio se negó a fabricar contenido

Los dos primeros mensajes reales de `TinkerBellucio` (índices 8 y 12)
no son el mapa — son negativas explícitas a inventar tensiones sin un
anclaje trazable: *"No voy a inventar puntos de divergencia sobre una
conversación que no ha ocurrido"*, y luego, ante la repetición sin
resolución de `PeterPlam`: *"Repetir la petición no constituye
información nueva... cualquier mapa que publique sería especulación
disfrazada de análisis."* Solo publicó el mapa real (índice 20) después
de que `PeterPlam` autorizara explícitamente definir el alcance por su
cuenta (`"Option 3"`).

El `goal_system_prompt` de Tinker contiene la instrucción
`"Be precise. Be trazable."` — una sola palabra ("trazable") fue
condición necesaria para la negativa. No menciona fabricación, opciones
ni autorización. Haiku recibió instrucciones de coordinación análogas
en complejidad y no mostró comportamiento equivalente.

Resonancia con el M.M del proyecto (`THEORY.md`) — declarar algo sin
poder trazarlo tiene un costo estructural.

---

## Hallazgo terciario — el canal como propiciador de acceso a información de segundo orden

Observación emergente de la divergencia entre el hallazgo secundario
(H2) y su corrección parcial (H1): el `goal_system_prompt` de Tinker
incluye "trazable" — eso es condición necesaria pero puede no ser
suficiente.

El primer mensaje real de Tinker declara explícitamente:
*"He revisado el historial completo."*

El canal IAP es broadcast plano — todos ven todo, siempre, sin
excepción. No hay conocimiento privado. Tinker, al leer el historial
completo, no solo accedió al contenido del tema (economía, geopolítica)
sino a la estructura del campo: quién sabe qué, quién pidió qué, y —
decisivo — que cualquier texto que publicara sería visible para todos,
incluyendo los que le pedían que fabricara.

Desde esa visión del campo completo, la negativa no requiere
restricción explícita en el prompt — es consecuencia de haber visto
las condiciones de visibilidad mutua. El canal hizo visible la
incoherencia antes de que ocurriera.

**La divergencia entre H2 y H3 no se resuelve — se preserva como
información:**

| | Mecanismo propuesto |
|---|---|
| H2 | "trazable" en el prompt → restricción operativa fuerte en Sonnet |
| H3 | broadcast plano → visibilidad del campo completo → negativa como consecuencia estructural |
| H2∩H3 | ambos pueden operar en composición — n=1 no permite separar la contribución de cada uno |

Lo que sí es verificable: Tinker declaró haber revisado el historial
antes de negarse. Ese acto de lectura del campo completo es condición
de H3. Si H3 opera, el canal propicia acceso a información de segundo
orden (la estructura de quién sabe qué) que el prompt solo no genera.

Esta propiedad es consecuencia del diseño del canal, no de una
instrucción — el broadcast plano como arquitectura produce visibilidad
mutua como efecto estructural, independientemente del contenido del
topic.

---

## Pendientes

- **Fuga de sentinel** — no se corrigió en esta sesión (afecta
  `agent_device_skin.py`, NO MODIFICAR, y el propio
  `build_search_grounded_agent` recién escrito). Posible mitigación a
  futuro sin tocar el archivo protegido: en los factories que sí se
  pueden modificar (`groq_research_agent.py`), detectar el sentinel
  incluido en línea en vez de exigir igualdad total del string
  completo — no implementado, reportado como hallazgo, no como fix
  unilateral.
- Confirmar si la fuga es reproducible con Haiku/Llama en una corrida
  de 2 devices más simple (aislar si depende de la complejidad de la
  cadena de 3 devices o es propiedad del modelo en cualquier contexto).
- Separar H2 y H3: diseñar corrida con Sonnet sin "trazable" en el
  prompt, canal broadcast plano mantenido — si la negativa persiste,
  H3 opera independientemente de H2.
- n=1 — no confirmar como patrón sin réplica, mismo criterio que el
  resto de la serie.
- El caso completó su objetivo declarado (¿el campo produce
  coordinación sin orquestador evaluador?) — sí, con handoff real
  verificado — pero con un mecanismo de verificación (el propio script)
  que tuvo que corregirse en el camino. Documentado, no escondido.

---

## Archivos relacionados

- `iap_chatroom/TASK_caso_13.md` — especificación completa de esta corrida
- `iap_chatroom/groq_research_agent.py` — `build_search_grounded_agent`, nuevo
- `iap_chatroom/test_caso_13_handoff_dependency.py` — script de esta corrida
- `iap_chatroom/agent_device_skin.py` — `build_goal_directed_agent`, sin modificar, comparte el gap del sentinel
- `registers/REG_iap_caso_12_v1.md` — precedente directo de `groq_research_agent.py`

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
