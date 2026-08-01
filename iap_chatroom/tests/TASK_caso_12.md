Repo: gadanindelamor/ckm
Entorno: Codespace ckm (bash/Linux)

TAREA
-----
Caso 0.12 — mismo diseño exacto que Caso 0.11 (dos `AgentDeviceSkin`,
sin control genérico, join escalonado, roles invertidos entre runs),
pero uno de los dos skins deja de ser un `AgentDeviceSkin` conversacional
sobre Anthropic y pasa a ser el `AutonomousResearchAgent` (Groq +
planificación + búsqueda DuckDuckGo) implementado esta sesión en
`iap_chatroom/groq_research_agent.py` — sin modificar ese archivo ni
`agent_device_skin.py`, ambos ya listos y smoke-testeados.

Caso 0.11 confirmó actividad 2/2 con dos skins conversacionales, mismo
modelo (Sonnet), orientaciones distintas (práctica vs teoría). Caso
0.12 cambia el mecanismo de uno de los dos devices: en vez de un
wrapped_agent que lee `observation["history"]`/`["trigger"]` y responde
conversacionalmente turno a turno (`build_goal_directed_agent`), el
device reemplazado ejecuta su propio plan de investigación
(`build_autonomous_groq_agent`) — genera un plan una vez, después un
paso de buscar+analizar por invocación, e ignora por diseño el
contenido del canal (ver docstring de `build_autonomous_groq_agent()`,
sección "Nota de diseño").

**Se reemplaza `ArchitectSkin` (orientación práctica), se mantiene
`TheoristSkin` (orientación teórica) sin cambios respecto a 0.11** —
mismo `THEORIST_GOAL_PROMPT`, mismo provider (Anthropic, claude-sonnet-5).
El objetivo del nuevo device Groq usa el mismo tema que `ArchitectSkin`
tenía en 0.11 (qué importa al desplegar sistemas multiagente en
producción), reformulado como objetivo de investigación en vez de
prompt conversacional — para mantener la comparación con 0.11 lo más
controlada posible dado que el mecanismo cambia.

**Confound explícito, no oculto:** este caso cambia TRES cosas a la vez
respecto al device que reemplaza — provider (Anthropic→Groq), mecanismo
(skin conversacional→agente de investigación autónomo), y posiblemente
disponibilidad de búsqueda real (ver "Verificar antes de correr" abajo).
No aísla cuál de las tres es responsable de cualquier diferencia con
0.11 — es una primera corrida exploratoria de compatibilidad e
interacción, no un experimento de una sola variable. Si el resultado
amerita seguir esta línea, aislar variables (mismo provider, mismo
mecanismo con distinto objetivo, etc.) queda para un caso posterior.

VERIFICAR ANTES DE CORRER
--------------------------
1. `iap_chatroom/groq_research_agent.py` y `groq_agent_config.json`
   existen, sin modificar desde que se implementaron esta sesión.
   `iap_chatroom/agent_device_skin.py` sin modificar (confirmar con
   `git status`/diff si aplica).
2. **Resuelto en sesión:** `ddgs` instalado (`pip install ddgs`, sin
   tocar `pyproject.toml` — sigue siendo dependencia opcional no
   declarada). **No es `duckduckgo-search`** — ese paquete está
   deprecado (renombrado por el mismo mantenedor); verificado en esta
   sesión que `duckduckgo-search==8.1.1` devuelve `[]` silenciosamente
   en este entorno incluso con queries genéricas ("python programming
   language"), solo con un `RuntimeWarning` fácil de perder — no un
   error. `ddgs==9.14.4` con la misma query trae resultados reales.
   `groq_research_agent.py` ya actualizado para importar `ddgs`. Sin
   el paquete instalado, `ddg_search()` sigue sin crashear (placeholder
   de error) — pero con `ddgs` instalado y confirmado funcional, este
   caso puede ejercitar búsqueda real.
3. `GROQ_API_KEY` configurada en `.env` (ya usada en Caso 0.9, debería
   seguir presente — confirmar, no asumir).
4. `max_tokens=4096` presente en `anthropic_provider.py` y
   `groq_provider.py` (fix de la sesión previa) — verificar que sigue
   ahí antes de correr, no asumirlo.

PARÁMETROS
----------
Idénticos a Caso 0.11: DURATION=90s (early)/85s (late), POLL_INTERVAL=2.0s,
DELTA_T=5s. Sin seed_human. SYSTEM_PROMPT_04A (WELCOME MSG del canal,
sin explicación CKM) — requerido por el constructor de
`AutonomousDevice`/`AgentDeviceSkin` para ambos devices, pero no genera
contenido publicado en ninguno de los dos (el `TheoristSkin` genera vía
su propio `goal_system_prompt`; el device Groq ni siquiera lee el
canal para decidir qué publicar).

DEVICES
-------
| device_id | mecanismo | objetivo | provider/modelo |
|---|---|---|---|
| `TheoristSkin_Sonnet5_2` | `AgentDeviceSkin` + `build_goal_directed_agent` (sin cambios vs 0.11) | teoría — cómo emergen conocimiento y significado de la interacción | AnthropicProvider, claude-sonnet-5 |
| `GroqResearchSkin_Llama_1` | `AgentDeviceSkin` + `build_autonomous_groq_agent` (nuevo) | investigar qué importa al desplegar sistemas multiagente en producción | GroqProvider, llama-3.3-70b-versatile |

`GroqResearchSkin_Llama_1` se construye:
```python
groq_provider = GroqProvider(model="llama-3.3-70b-versatile")
wrapped = build_autonomous_groq_agent(
    device_id="GroqResearchSkin_Llama_1",
    objetivo="Investigar qué importa al desplegar sistemas multiagente en producción: fallos, coordinación, observabilidad.",
    provider=groq_provider,
)
device = AgentDeviceSkin(
    device_id="GroqResearchSkin_Llama_1",
    provider=groq_provider,
    system_prompt=SYSTEM_PROMPT_04A.format(device_id="GroqResearchSkin_Llama_1"),
    mcp_url=MCP_URL,
    poll_interval=POLL_INTERVAL,
    wrapped_agent=wrapped,
)
```

RUNS
----
Run 1: early=`GroqResearchSkin_Llama_1`, late=`TheoristSkin_Sonnet5_2`
Run 2: early=`TheoristSkin_Sonnet5_2`, late=`GroqResearchSkin_Llama_1`
(roles invertidos, mismo patrón que 0.8/0.9/0.10/0.11)

SECUENCIA POR RUN
-----------------
1. `prepare_state(label=f"caso12_run{n}")` — backup canónico, mismo
   mecanismo que toda la serie (nunca borra, mueve a `process/` con
   sufijo `.bak_<epoch>_<label>`).
2. Detener servidor si está corriendo. Verificar `_state/` vacío.
   Reiniciar con `run_in_background`/`TaskStop`. Esperar `GET
   /api/monitor` con `200` antes de continuar.
3. Join device early (t=0).
4. Sleep `DELTA_T` segundos.
5. Join device late.
6. Ciclo ODA corre `DURATION` para early, `DURATION - DELTA_T` para
   late (cierran juntos).
7. Al cierre: loguear Firma_CKM + trayectoria + historial completo del
   canal (`get_messages(since=0.0)`).
8. Revisar consola del servidor por warnings de truncamiento
   (`[AnthropicProvider WARNING]`/`[GroqProvider WARNING]`) y por
   warnings propios del nuevo módulo
   (`[groq_research_agent WARNING]`) — estos últimos no son errores
   fatales (el módulo está diseñado para no crashear) pero si aparecen
   documentarlos, no ignorarlos.
9. Preservar `corpus_state.json`/`monitor_trajectory.jsonl` con label
   del run antes del siguiente.

CRITERIO
--------
Si `GroqResearchSkin_Llama_1` publica contenido → primera vez que un
device que no lee el canal (no responde a `TheoristSkin`, no reacciona
al contenido conversacional) coexiste con uno que sí lo hace. Pregunta
abierta: ¿`TheoristSkin` reacciona al contenido del research agent
(que sí puede leer, vía `history`) aunque el research agent no le
devuelva la atención? Si es así, el intercambio sería asimétrico por
diseño — un patrón nuevo, distinto a todo lo visto en 0.4-0.11, donde
ambos devices siempre podían (aunque no siempre lo hicieran) responder
al otro.

Si `GroqResearchSkin_Llama_1` no publica nada (plan vacío, o
`max_iterations` agotado sin resultados útiles) → el caso se reduce a
`TheoristSkin` solo, sin device con quien cruzar — compararlo contra
el patrón de silencio/monólogo ya visto cuando un solo device tiene
contenido real y el otro no (ver Caso 0.6 Run 1: un device saluda, el
resto no tiene a qué responder).

`ddgs` instalado y confirmado funcional (ver "Verificar antes de
correr") — este caso ejercita búsqueda real, no el placeholder de
error. Si de todas formas alguna tarea del plan no trae resultados
útiles, es dato real de la búsqueda, no degradación del módulo.

CRITERIOS DE ÉXITO
------------------
Por run:
- 2 devices join sin error
- Log distingue mecanismo (`[SKIN-CONVERSACIONAL]`/`[SKIN-RESEARCH]`
  o equivalente) y qué modelo/provider usa cada uno
- 0 mensajes truncados por `max_tokens`/`finish_reason`, o
  documentados si aparecen
- 0 excepciones no atrapadas propagadas fuera del ciclo ODA (el
  research agent está diseñado para nunca lanzar — confirmar que se
  sostiene bajo la corrida real, no solo en el smoke test aislado)
- Firma_CKM o `None` documentado
- n_textos AI publicados por device
- corpus_state.json / monitor_trajectory.jsonl preservados con label
  del run
- Si `GroqResearchSkin_Llama_1` exportó a
  `process/agent_runs/resultados_agente_*.json`, referenciarlo en el
  resultado (auditoría del plan + búsquedas + análisis crudo)

NO MODIFICAR
------------
`autonomous_device.py`, `channel.py`, `ckm_monitor.py`, `server.py`,
`mcp_server.py`, `agent_device_skin.py`, `groq_research_agent.py`,
`groq_provider.py`, `anthropic_provider.py`.

Si la única forma correcta de correr este caso pasa por tocar alguno
de estos archivos → reportar antes de continuar, no proceder con una
excepción sin avisar (mismo criterio ya aplicado toda la sesión).

**Excepción explícita — dependencias de entorno para testing:**
NO MODIFICAR se refiere a los archivos del proyecto (código
trackeado). Instalar paquetes pip nuevos en el entorno
(`pip install <paquete>`) para poder correr smoke tests o los propios
casos de test **no** es una modificación cubierta por esta regla — es
una acción de entorno, reversible, que no toca ningún archivo de la
lista de arriba. No requiere reportar antes de proceder, a diferencia
de tocar `pyproject.toml` para declarar una dependencia formal del
proyecto — eso sigue requiriendo aviso previo (ver la decisión ya
tomada de mantener `ddgs` como dependencia opcional NO declarada en
`pyproject.toml`, punto 2 de "Verificar antes de correr"). Precedente
de esta misma sesión: instalar `duckduckgo-search` y después `ddgs`
(al descubrir que el primero está deprecado) no violó NO MODIFICAR en
ningún momento — son dos cosas distintas. Este criterio no es
específico de Caso 0.12; aplica igual a cualquier TASK_caso_*.md
futura que necesite una dependencia de entorno para testing básico.

Nota: si `GroqResearchSkin_Llama_1` no produce ningún texto en 2-3
iteraciones del `step()` (por ejemplo, porque el plan generado por Groq
resulta vacío tras normalización), no es necesariamente un bug del
módulo — puede ser una corrida real de "silencio", igual de válida
como dato que la actividad. No forzar contenido ni reintentar fuera de
lo que el propio diseño de `AutonomousResearchAgent.step()` ya hace.

---
*Jul 23 2026*
