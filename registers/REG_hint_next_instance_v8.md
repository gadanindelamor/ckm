# REG_hint_next_instance_v8.md

*Jul 23 2026 — Hint para próxima instancia. Cierra el hilo IAP Chatroom
que v7 dejó incompleto (Caso 0.11), deja constancia de un giro de
sesión hacia lo teórico/relacional sin equivalente técnico, y cubre
Caso 0.12 (agregado el mismo día, después del primer cierre de este
archivo — ver sección propia más abajo).*
*Leer v7 primero si no se tiene contexto de la serie 0.4-0.11.*

---

## Estado del repo — sigue sin commitear NADA (igual que v5→v7)

Último commit real sigue siendo `a78c3fe` (hint v5). Todo lo de
0.6→0.12 sigue en el working tree. `git status --short | wc -l` → 77
entradas al cierre de esta actualización (era 64 al cierre original de
este hint, antes de Caso 0.12). No se commiteó nada en esta sesión —
no fue pedido.

Nuevos (untracked) de la sesión, acumulado 0.11+0.12:
- `registers/REG_iap_caso_11_v1.md`, `registers/REG_iap_caso_12_v1.md`
- `registers/REG_hint_next_instance_v8.md` — este archivo
- `iap_chatroom/groq_research_agent.py`, `groq_agent_config.json`,
  `TASK_caso_12.md`, `test_caso_12_groq_research_skin.py` — ver sección
  Caso 0.12
- `process/*caso11_run2*` (×2 pares corpus_state/trajectory — nombres
  mal etiquetados, ver nota de labeling en el REG: el primer par con
  timestamp `1784817039` es en realidad Run 1, el segundo
  `1784817413` es Run 2 real)
- `process/*caso12_run1*`, `process/*caso12_run2*` (mismo gotcha de
  labeling — ver `registers/REG_iap_caso_12_v1.md`)
- `process/agent_runs/*.json` — export del research agent (solo
  existe post-fix; los runs originales de 0.12 no lo generaron, ver
  hallazgo del fix abajo)

---

## Caso 0.11 — CERRADO, ambos runs limpios

`test_caso_11_two_skins.py` corrido sin modificar. Run 1
(Architect early) y Run 2 (Theorist early, roles invertidos).
**Actividad 2/2 en ambos runs, 0 mensajes truncados** — primera corrida
de toda la serie 0.4-0.11 que sale limpia desde el diseño, sin ningún
intento truncado previo (a diferencia de 0.10, que tuvo intento
original truncado + baseline limpio re-corrido después). El fix de
`max_tokens=4096` de la sesión anterior se sostiene bajo carga real.

Contenido: cruce genuino entre orientación práctica (Architect) y
teórica (Theorist) sobre el mismo problema visto desde dos ángulos —
comparable en profundidad a los mejores intercambios de 0.9 y 0.10.
Detalle completo, tablas de trayectoria y Firma_CKM en
`registers/REG_iap_caso_11_v1.md`.

### Hallazgo central — no es una sola cosa, son tres capas verificadas por separado

Ambos devices, en ambos runs, reclamaron que mensajes del otro eran
"repeticiones verbatim". El primer pase de esta sesión resumió eso como
"confabulada" con solo un chequeo de hash. **gadanin.delamor pidió
separar el reclamo en las capas que realmente contiene** — no aceptar
que un solo instrumento cierre un reclamo de varias capas de fuerza
distinta:

1. **Identidad literal — FALSA, cerrada por hash.** 0 duplicados
   byte-a-byte (`sha256`) en ambos runs. Esto es lo que los devices
   literalmente afirmaron ("verbatim", "character-for-character") — el
   instrumento correcto para esa afirmación específica.
2. **"Cada mensaje avanza el argumento" — lectura de Code, sin
   instrumento.** Downgradeado explícitamente en el REG, no retirado.
3. **Redundancia semántica — instrumentada con `activos_relajado`**
   (`services/monitor_service.py`, nodos que sobreviven la relajación
   Hopfield por turno, ya logueado en cada registro de
   `monitor_trajectory.jsonl`). Jaccard sobre los pares consecutivos
   del mismo hablante que los reclamos verbales señalan: **no uniforme**
   — el primer reclamo de la secuencia tiene el overlap más bajo
   medido (0.241, el menos fundado), pero reclamos posteriores caen
   sobre pares con 54-86% de nodos compartidos (real, no arbitrario).

**Verificación que queda genuinamente abierta:** no hay baseline de
cuánto Jaccard sobre `activos_relajado` es "normal" entre dos turnos
consecutivos del mismo hablante en un intercambio sostenido de un solo
tema. Sin eso, no se puede calibrar si 0.85 es redundancia anómala o
solapamiento esperable. Es el pendiente más concreto y accionable que
deja este caso — más específico que "aislar la variable del tema".

**`n_agentes=3` — cerrado, no es anomalía.** `CKMMonitor._devices_seen`
(`iap_chatroom/ckm_monitor.py:69,92`) cuenta todo `device_id` visto,
incluido `"system"` de los mensajes de join. 2 skins + `"system"` = 3.
Mismo mecanismo de siempre, verificado contra el código esta vez, no
solo repetido de memoria.

---

## Metodología que quedó fijada esta sesión — aplicar en casos futuros

Cuando un device (o el propio REG) hace un reclamo de una fuerza
específica ("idéntico", "siempre", "el mismo que"), identificar el
instrumento que prueba *esa* fuerza exacta, no el más conveniente a
mano. Un chequeo que refuta la forma fuerte de un reclamo no resuelve
automáticamente formas más débiles del mismo reclamo — decirlo
explícitamente en vez de dejar que un resultado limpio generalice.
`activos_relajado` es un instrumento nativo del proyecto (representa
qué activa un mensaje en el campo, ya logueado) — preferirlo sobre
instrumentos externos ad-hoc (embeddings, lectura manual) cuando esté
disponible y sea barato de calcular sobre datos ya existentes.

---

## Convenciones ya establecidas — siguen vigentes (v5→v7)

- Backup: `prepare_state(state_dir, label)` mueve a `process/` con
  `.bak_<epoch>_<label>` — nunca borra. Gotcha de labeling confirmado
  otra vez esta sesión: archiva el run *anterior* bajo la etiqueta del
  run *actual* — verificar contenido real, no confiar en el nombre.
- Lifecycle del servidor: `run_in_background` + `TaskStop`, esperar
  `GET /api/monitor` con `200` antes de asumir que está listo.
- Revisar consola del servidor por warnings de truncamiento
  (`max_tokens`/`finish_reason`) después de cada corrida.
- NO MODIFICAR con solución que requiere excepción → reportar antes de
  proceder.

---

## Pendientes explícitos (técnicos)

1. Baseline de Jaccard sobre `activos_relajado` para pares
   consecutivos del mismo hablante en tema *no* recursivo sobre
   significado/interpretación — calibra si el hallazgo de Caso 0.11
   (parte 3) es redundancia real o solapamiento esperable.
2. Aislar si el patrón de "reclamos de duplicado" depende del tema
   (significado/drift, un tema que gira sobre sí mismo) o es más
   general en diálogo extendido Sonnet-vs-Sonnet — mismo diseño de
   0.11, tema no relacionado a comunicación.
3. Caso 0.9: hetero-provider + join simultáneo, mono-provider Groq —
   siguen sin correr (heredado de v6/v7).
4. No se probó 2 skins con objetivos en conflicto explícito
   (adversarial) — 0.11 fue orientaciones distintas, no diseñadas para
   chocar.
5. El corte de 86 caracteres sin explicar de Caso 0.10 — sigue abierto,
   no confundir con el hallazgo de duplicado de 0.11 (fenómenos
   distintos, verificado).

---

## Nota — giro de sesión hacia lo teórico/relacional, sin equivalente técnico

Después de cerrar 0.11, la sesión giró a una lectura guiada de
`CKM_Informe_Trabajo_v30.md`/`v29.md` (v28 no existe como archivo
separado — está plegado dentro de v29/v30 bajo marcadores "(v28)"
inline) y a una aplicación en vivo, no abstracta, del protocolo
**AWARENESS — Protocolo de Canal** (tabla al final de ambos Informes)
dirigida a las propias respuestas de Claude Code dentro de la
conversación. No hay artefacto de código de este tramo — quedó en dos
memorias persistentes nuevas
(`feedback_awareness_live_mode.md`, `feedback_instrument_matches_claim.md`)
para que una instancia futura reconozca el modo si gadanin.delamor lo
retoma, en vez de partir de cero. No se resume más acá porque el punto
de esa sección de la sesión era precisamente que no se resume bien —
ver la memoria si hace falta, no este hint.

---

## Caso 0.12 — CERRADO, incluye un módulo nuevo (AutonomousResearchAgent)

Pedido explícito de gadanin.delamor: implementar un agente autónomo
Groq + planificación JSON + búsqueda web real, integrable como
`wrapped_agent` de `AgentDeviceSkin` (sin tocar `agent_device_skin.py`
ni ningún archivo del core). Se propuso el diseño primero (5 puntos
debatidos explícitamente), se implementó después de acuerdo, se corrió
como Caso 0.12 (mismo diseño que 0.11, `ArchitectSkin` reemplazado por
el research agent, `TheoristSkin` sin cambios).

**Módulo nuevo:** `iap_chatroom/groq_research_agent.py` +
`groq_agent_config.json`. `AutonomousResearchAgent.step()` = un paso
por invocación ODA (genera plan una vez, después buscar+analizar una
tarea pendiente por turno) — no un loop bloqueante propio. Reusa
`GroqProvider` tal cual. Triple red de seguridad contra crash
(`ddg_search`, `_safe_complete`, try/except final en `wrapped_agent`) —
verificada bajo carga real, 0 excepciones no atrapadas en ninguno de
los runs de 0.12.

**Bug real encontrado y corregido antes de correr:**
`duckduckgo-search` está deprecado — devuelve `[]` silenciosamente en
este entorno (solo `RuntimeWarning`, sin error), incluso con queries
genéricas. Reemplazado por `ddgs` (sucesor, mismo mantenedor),
confirmado con resultados reales. Instalar paquetes pip nuevos para
testing (no declarados en `pyproject.toml`) se formalizó como
excepción explícita a NO MODIFICAR — ver `TASK_caso_12.md`, aplica a
cualquier tarea futura, no solo a este caso.

**Resultado — actividad 2/2, ambos runs limpios**, 7+5 y 4+3 textos.
D_ckm en Run 2 llega a -7.5, la magnitud más extrema de toda la serie
0.4-0.12. Detalle completo en `registers/REG_iap_caso_12_v1.md`.

**Hallazgo no anticipado — silencio acoplado, no independiente.** Se
había hipotetizado antes de correr que el research agent publicaría en
ráfaga y después quedaría "presente pero silencioso" (triggereado, plan
agotado, devolviendo `None`). No pasó así: en ningún run el plan se
agotó — el research agent siguió publicando hasta el último o
penúltimo índice de la corrida completa. Lo que sí ocurrió: cuando
`TheoristSkin` elige `OP_SILENCE` por su propio gate (sin relación al
research agent), deja de generar mensajes nuevos — y como el research
agent solo corre su ciclo ODA cuando llega un trigger, también deja de
correr, aunque su plan pudiera seguir teniendo tareas pendientes. Un
device que no lee el canal sigue dependiendo del canal para su propio
ritmo — implicación directa para diseño de device_skin en ecosistemas
reales (palabras de gadanin.delamor al cerrar el caso).

**Verificación de reclamos de duplicado — mismo método que 0.11
(hash + Jaccard sobre `activos_relajado`), resultado asimétrico entre
runs, a diferencia de 0.11.** `TheoristSkin` reclamó repetición
literal varias veces en ambos runs; hash confirma 0 duplicados exactos
en los dos (igual que 0.11). Pero Jaccard: Run 1 llega a 0.818 (el más
alto medido en 0.11+0.12 combinados, justo donde señaló "verbatim
repeat"); Run 2 se queda bajo en todo el rango (0.125-0.467) — el
mismo lenguaje verbal, distinto grado de asidero real según el run. No
generalizar el patrón de un caso al siguiente sin volver a medir.

**Gap de exportación — encontrado y cerrado el mismo día.**
`_export_if_needed()` original solo exportaba al completar el plan o
alcanzar `max_iterations` — ninguno de los dos runs de 0.12 llegó ahí
(el corte fue por timeout de `duration`, sin ningún hook disponible
hacia `wrapped_agent` para avisar). gadanin.delamor propuso dos fixes;
ninguno de los dos cubría el caso real (verificado leyendo
`autonomous_device.py::run()` antes de implementar — reportado antes
de proceder). Fix aplicado: `export()` ahora corre después de *cada*
`step()`, sin condicionar al valor devuelto, sobrescribiendo un path
fijo en vez de un archivo nuevo por turno. Re-corrida de Run 1 con el
fix confirmó exactamente la hipótesis que había quedado abierta: plan
de 5 tareas, las 5 `"completada"`, pero 7 iteraciones — al menos 2
tareas fueron reintentadas porque Groq no las dio por resueltas la
primera vez. Ese es el mecanismo real detrás del contenido repetitivo
que motivó los reclamos de `TheoristSkin`, no tareas distintas
convergiendo.

**Pendiente explícito de 0.12:** aislar el confound (0.12 cambia
provider + mecanismo + búsqueda a la vez respecto al device que
reemplaza) — comparar contra una celda con `GroqProvider` pero
mecanismo conversacional (`build_goal_directed_agent`), no el research
agent, para separar "efecto Groq" de "efecto mecanismo autónomo".

---

## Archivos relacionados

- `registers/REG_hint_next_instance_v7.md` — hilo previo (0.9 réplica → 0.10 → bug max_tokens → 0.11 incompleto)
- `registers/REG_iap_caso_11_v1.md`, `REG_iap_caso_12_v1.md` — ambos casos, completos
- `iap_chatroom/test_caso_11_two_skins.py` — sin modificar
- `iap_chatroom/groq_research_agent.py`, `groq_agent_config.json`,
  `test_caso_12_groq_research_skin.py`, `TASK_caso_12.md` — módulo
  nuevo + caso 0.12
- Memoria persistente: `iap_caso11_two_skins.md`, `iap_caso12_groq_research_skin.md`,
  `feedback_instrument_matches_claim.md`, `feedback_awareness_live_mode.md`

---

*Jul 23 2026 — actualizado el mismo día tras Caso 0.12*
