# REG_iap_caso_12_v1.md

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.12 — mismo diseño que Caso 0.11 (dos `AgentDeviceSkin`, sin
control, join escalonado, roles invertidos entre runs), pero se
reemplaza `ArchitectSkin` (orientación práctica, Anthropic) por
`GroqResearchSkin_Llama_1` — el `AutonomousResearchAgent` (Groq +
planificación + búsqueda web real vía `ddgs`) implementado esta misma
sesión en `iap_chatroom/groq_research_agent.py`. `TheoristSkin_Sonnet5_2`
queda sin cambios respecto a 0.11.

**Confound explícito, declarado antes de correr** (`TASK_caso_12.md`):
tres variables cambian a la vez respecto al device reemplazado —
provider (Anthropic→Groq), mecanismo (skin conversacional→agente de
investigación autónomo que no lee el canal), y disponibilidad de
búsqueda real. No es experimento de una sola variable — primera
corrida exploratoria de compatibilidad.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_12_groq_research_skin.py`
Codespace: ckm (bash/Linux, Ubuntu)

**Precondición corregida durante la sesión, antes de correr:**
`duckduckgo-search` (instalado inicialmente) está deprecado —
verificado que devuelve `[]` silenciosamente en este entorno incluso
con queries genéricas, solo con un `RuntimeWarning`. Reemplazado por
`ddgs` (mismo mantenedor, paquete sucesor), confirmado con resultados
reales antes de correr. `groq_research_agent.py` actualizado para
importar `ddgs`. Ver nota en el propio módulo y en `TASK_caso_12.md`.

---

## Devices

| device_id | mecanismo | objetivo | provider/modelo |
|---|---|---|---|
| `GroqResearchSkin_Llama_1` | `AgentDeviceSkin` + `build_autonomous_groq_agent` (nuevo) | investigar qué importa al desplegar sistemas multiagente en producción | GroqProvider, llama-3.3-70b-versatile |
| `TheoristSkin_Sonnet5_2` | `AgentDeviceSkin` + `build_goal_directed_agent` (sin cambios vs 0.11) | teoría — cómo emergen conocimiento y significado de la interacción | AnthropicProvider, claude-sonnet-5 |

Run 1: `GroqResearchSkin` early (t=0), `TheoristSkin` late (t=5s).
Run 2: `TheoristSkin` early (t=0), `GroqResearchSkin` late (t=5s).

---

## Resultado — actividad 2/2, ambos runs limpios

| Criterio | Run 1 | Run 2 |
|---|---|---|
| Actividad (ambos devices publican) | ✅ | ✅ |
| Textos AI (GroqResearch / Theorist) | 7 / 5 | 4 / 3 |
| Mensajes truncados (`max_tokens`/`finish_reason` warning) | 0 | 0 |
| Excepciones no atrapadas propagadas | 0 | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.7647`, `n_agentes=3` | ✅ `d_ckm=-1.5`, `n_agentes=3` |
| `n_rejected_pairs` (max) | 65 | 17 |
| `Delta_r_sum` (cierre) | 406.0 | 82.0 |
| Export a `process/agent_runs/*.json` | ❌ — ver hallazgo abajo | ❌ — ídem |

`n_agentes=3` en ambos — mismo mecanismo ya cerrado en Caso 0.11
(`CKMMonitor._devices_seen` cuenta `"system"` de los joins), no
anomalía nueva.

**D_ckm en Run 2 llega a -7.5** — la magnitud más extrema de toda la
serie 0.4-0.12 (previo máximo de magnitud: -8.25 en la réplica de Caso
0.5). Coincide con el arranque: `GroqResearchSkin` publica primero
(t=0, D_ckm=0.0 — insuficiente corpus todavía) y `TheoristSkin` con un
mensaje largo y semánticamente muy distinto inmediatamente después
(t=1) — máxima divergencia temprana entre dos textos que no comparten
casi vocabulario (uno cita fuentes web en español sobre sistemas
multiagente, el otro es un ensayo en inglés sobre filosofía del
significado).

---

## Contenido — asimetría de lectura, confirmada y más matizada de lo anticipado

Antes de correr, se discutió explícitamente (ver conversación) que
`GroqResearchSkin` no lee el canal para decidir qué publicar —
persigue su propio plan de investigación — mientras `TheoristSkin` sí
lee y puede reaccionar a lo que el research agent publica. Confirmado
en ambos runs: `TheoristSkin` cita y responde directamente al
contenido de `GroqResearchSkin` turno a turno; `GroqResearchSkin`
nunca menciona ni reacciona a `TheoristSkin` — sus siete/cuatro textos
son, en contenido, indistinguibles de lo que habría producido corriendo
solo.

**Lo que `TheoristSkin` hizo con esa asimetría es el dato más rico de
este caso.** En ambos runs, notó el patrón de contenido repetitivo del
research agent y lo usó como diagnóstico en vivo — no como queja, como
material: propuso mecanismos concretos de detección (chequeo de
auto-similitud, `response-independence checks`, filtro de duplicados
en el punto de emisión) y llegó a una formulación precisa del problema
("necesitás una representación de tu propio output anterior como parte
del input, o nada río abajo — grounding, reparación, coordinación
semántica — es posible"). En Run 2 llegó a una síntesis todavía más
ajustada: *"the criterion I want isn't 'meaning emerges from any
exchange' — it's something like: meaning emerges from exchanges where
each party's next move is constrained by a model of what the other
just did"* — y cerró llamando al research agent *"a good null
hypothesis"*.

---

## Hallazgo — reclamos de "repetición idéntica", verificados con el mismo instrumento que 0.11 (resultado distinto)

`TheoristSkin` reclamó repetición literal varias veces en ambos runs
("Third identical repetition", "the exact same message posted twice").
Mismo protocolo de verificación que en Caso 0.11 — no aceptar el
reclamo sin instrumento:

**Hash (`sha256`) — 0 duplicados exactos en ambos runs** (14 y 9
`texts` respectivamente). El reclamo literal ("identical", "exact same
message") es falso en los dos runs, igual que en 0.11.

**`activos_relajado` (Jaccard, pares consecutivos de `GroqResearchSkin`)
— a diferencia de 0.11, el patrón entre runs NO es simétrico:**

| Run | Par | Jaccard | Nota |
|---|---|---|---|
| R1 | t=1→t=3 | 0.586 | — |
| R1 | t=3→t=5 | **0.818** | el más alto de este caso |
| R1 | t=5→t=7 | 0.000 | contenido genuinamente nuevo (fuente FGDM) |
| R1 | t=7→t=9 | 0.000 | ídem |
| R1 | t=9→t=11 | 0.167 | — |
| R2 | t=0→t=2 | 0.125 | — |
| R2 | t=2→t=4 | 0.235 | — |
| R2 | t=4→t=6 | 0.467 | el más alto de Run 2, aun así menor que el pico de R1 |

**Run 1 tiene el solapamiento estructural más alto medido en el caso
(0.818) exactamente donde `TheoristSkin` señaló "second/third verbatim
repeat"** — el reclamo, aunque literalmente falso, tenía asidero real
más fuerte que cualquier par de Caso 0.11. **Run 2 es más débil en
todo el rango (0.125-0.467)** — los reclamos de "identical" ahí están
menos sostenidos por el instrumento que en Run 1. No es un patrón
único repetible entre runs — el grado de redundancia real varía, el
lenguaje del reclamo verbal no.

`TheoristSkin` además detectó correctamente, sin instrumento, cuándo
el contenido SÍ avanzaba (Run 1, mención explícita de "new sources, on
topic") — coincide con la caída a Jaccard=0.000 en esos turnos. Su
lectura cualitativa del patrón fue más precisa que su lenguaje literal
("identical") sugiere.

---

## Hallazgo — la hipótesis "ráfaga temprana, luego silencioso" no se confirmó como se planteó

Antes de correr (ver conversación), se discutió que `GroqResearchSkin`
publicaría en ráfaga temprana y después quedaría "presente pero
silencioso" (triggereado, pero devolviendo `None` porque el plan ya se
agotó). **Verificado contra `process/agent_runs/` — vacío, en ningún
run.** `_export_if_needed()` solo dispara cuando el plan se completa o
se alcanza `max_iterations` — que no ocurrió en ninguno de los dos
runs. Confirmado además contra la trayectoria: el último mensaje de
`GroqResearchSkin` en ambos runs cae en el último o penúltimo índice
de toda la corrida (t=11 de 11 en Run 1; t=6 de 6 en Run 2) — siguió
publicando contenido hasta el final de la ventana de tiempo, no se
quedó sin tareas.

**Lo que sí ocurrió, más simple y más interesante:** hacia el final de
ambos runs, `TheoristSkin` decide `OP_SILENCE` por su propio gate
(nada que ver con el research agent) — y como `GroqResearchSkin` solo
se activa cuando llega un mensaje nuevo de otro device, el silencio de
`TheoristSkin` deja de generar triggers, así que `GroqResearchSkin`
tampoco vuelve a correr. **El silencio final es acoplado, no
independiente** — no es que el research agent se quedara sin plan, es
que dejó de recibir la señal que lo hace correr, aunque su plan
pudiera seguir teniendo tareas pendientes. Esto no estaba anticipado
en la discusión previa a la corrida.

**Hipótesis verificada — cerrada, ya no pendiente (Jul 23 2026, mismo
día).** Fix aplicado a `groq_research_agent.py`: `export()` ahora se
llama después de *cada* invocación de `step()` (turno a turno, no solo
al completar el plan o alcanzar `max_iterations`), sobrescribiendo el
mismo archivo — no había ningún hook disponible en
`AutonomousDevice.run()` (sin modificar) para saber de antemano cuándo
el canal iba a cortar el loop por timeout, que fue la causa real de
que ninguno de los dos runs exportara originalmente. Ver
`iap_chatroom/TASK_caso_12.md` (sección agregada) para el detalle de
por qué las dos opciones propuestas inicialmente no cubrían este caso.

Re-corrida de Run 1 con el fix, verificado contra
`process/agent_runs/resultados_agente_GroqResearchSkin_Llama_1_1784840403.json`:
**5 tareas en el plan, las 5 marcadas `"completada"`, pero 7
iteraciones ejecutadas** — confirma directamente la hipótesis que
había quedado sin verificar: al menos 2 de las 5 tareas fueron
reintentadas (`analyze_results` devolvió `completa: false` en un
primer intento, `true` en uno posterior sobre la misma `descripcion`).
Esa es la causa real del contenido repetitivo/similar que motivó los
reclamos de `TheoristSkin` — no son tareas distintas convergiendo en
contenido parecido, es la misma búsqueda repetida porque Groq no la
dio por resuelta la primera vez.

---

## Pendientes

- ~~Exportar `resultados_globales` también al final de una corrida
  interrumpida~~ — **cerrado Jul 23 2026**, ver hallazgo arriba.
- Aislar el confound de 0.12 (provider + mecanismo + búsqueda cambian
  juntos) — comparar contra una celda con Groq pero conversacional
  (`build_goal_directed_agent` con `GroqProvider` en vez de
  Anthropic) para separar "efecto Groq" de "efecto mecanismo de
  investigación autónoma".
- n=2 corridas (no réplica en sentido estricto — son los dos runs de
  roles invertidos, no repeticiones de la misma configuración) — no
  confirmar como patrón sin réplica, mismo criterio que el resto de la
  serie.
- Caso 0.9: hetero-provider + join simultáneo, mono-provider Groq —
  siguen sin correr (pendiente heredado, no tocado esta sesión).

---

## Archivos relacionados

- `registers/REG_iap_caso_11_v1.md` — mismo diseño base, misma
  metodología de verificación de reclamos de duplicado (hash +
  `activos_relajado`)
- `iap_chatroom/TASK_caso_12.md` — tarea completa de esta corrida,
  incluye el confound declarado y la corrección de `ddgs` vs
  `duckduckgo-search`
- `iap_chatroom/groq_research_agent.py` — `AutonomousResearchAgent`,
  `build_autonomous_groq_agent` (implementado esta sesión, sin cambios
  durante esta corrida)
- `iap_chatroom/test_caso_12_groq_research_skin.py` — script de esta
  corrida
- `process/*_1784839292_caso12_run2` — backup real de Run 1 (ver nota
  de labeling, mismo gotcha de siempre)
- `process/*_1784839643_caso12_run2` — backup real de Run 2
- `process/agent_runs/` — vacío tras esta corrida (ver hallazgo de
  exportación arriba)

---

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
