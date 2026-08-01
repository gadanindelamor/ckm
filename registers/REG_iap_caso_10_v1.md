# REG_iap_caso_10_v1.md

*Jul 22 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.10 — primer agente con objetivo propio sobre el ciclo ODA.
Toda la serie 0.4-0.9 usó `AutonomousDevice` con su gate LLM genérico
(`GATE_PROMPT_04`): la decisión INTERACT/OP_SILENCE y el contenido
publicado dependían solo del campo CKM y el WELCOME MSG del canal,
nunca de un objetivo propio del device.

Caso 0.10 introduce `AgentDeviceSkin` (`iap_chatroom/agent_device_skin.py`):
subclase de `AutonomousDevice` cuya decisión y contenido los define un
agente externo ("wrapped agent") con su propio system prompt orientado
a objetivo — sin gate LLM genérico.

Repo: `gadanindelamor/ckm` —
`iap_chatroom/agent_device_skin.py`, `iap_chatroom/test_caso_10_device_skin.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Prerequisito verificado

Leído `autonomous_device.py` completo antes de escribir código.
Identificado el flujo exacto: `run()` → por cada mensaje trigger →
`_observe()` (sin LLM, arma dict con `field`/`history`/`trigger`/
`own_recent`) → `_decide()` (gate LLM, devuelve INTERACT/OP_SILENCE) →
`_interact()` (si INTERACT, llama a `self._generate()` que usa
`self.system_prompt` + `self._to_chat_messages()` para generar y
publicar).

---

## Decisión de diseño reportada antes de escribir código

La tarea pedía sobreescribir *únicamente* `_decide()`. Pero `_interact()`
(heredado) publica llamando a `self._generate()`, que genera un texto
nuevo con `self.system_prompt` (el WELCOME MSG del canal) — no el texto
que ya generó y devolvió `wrapped_agent` con *su propio* system prompt.
Sobreescribir solo `_decide()` habría descartado el texto real del
agente wrapped y publicado otro, regenerado con el prompt equivocado.

Reportado antes de proceder (`AskUserQuestion`, no asumido). Resolución
acordada: sobreescribir también `_generate()` — no `_interact()`, no
`_observe()`, no `run()`, que quedan 100% heredados sin cambios.
`_decide()` cachea el texto de `wrapped_agent` en `self._pending_text`;
`_generate()` lo devuelve tal cual en vez de regenerar. Verificado con
test unitario (sin red): la ruta INTERACT devuelve el texto exacto del
wrapped agent sin llamar al provider de nuevo; la ruta OP_SILENCE
funciona igual que la clase base. `autonomous_device.py` no se
modificó — confirmado con `git status` antes y después de la corrida.

---

## Bug real encontrado y corregido en agent_device_skin.py (no en autonomous_device.py)

Primer intento de corrida crasheó:
```
anthropic.BadRequestError: Error code: 400 - 'This model does not
support assistant message prefill. The conversation must end with a
user message.'
```

Causa: `wrapped_agent` construye sus mensajes desde
`observation["history"]` (fetch completo del canal vía `get_messages`),
no desde `self._history` de `AutonomousDevice`. A diferencia de
`self._history` (que por construcción del loop en `run()` siempre
termina en el mensaje disparador — ajeno, nunca propio — cuando
`_generate()` es llamado), `observation["history"]` puede terminar con
el propio último mensaje publicado por el skin device si nadie más
publicó después. Un prompt que termina en rol `"assistant"` no es
aceptado por el modelo (sin soporte de prefill).

Fix: además de construir mensajes desde `history[-10:]`, se agrega
explícitamente `observation["trigger"]` como turno final de rol
`"user"` antes de coalescer — `trigger` nunca es del propio device (el
loop en `run()` lo filtra antes de llamar a `_observe()`), así que
garantiza terminar en `"user"` siempre. Verificado con test unitario
reproduciendo el escenario exacto del crash (history terminando en
mensaje propio) — sin el fix, se puede confirmar el mismo error;
con el fix, la secuencia de roles termina correctamente en `"user"`.

---

## Devices

| device_id | mecanismo | provider/modelo | rol join |
|---|---|---|---|
| `ResearcherSkin_Sonnet5_1` | `AgentDeviceSkin`, objetivo propio | AnthropicProvider, claude-sonnet-5 | early (t=0) |
| `AutonomousControl_Sonnet5_2` | `AutonomousDevice` base, gate genérico | AnthropicProvider, claude-sonnet-5 | late (t=5s) |

Mismo provider y modelo en ambos — la variable de esta corrida es el
*mecanismo de decisión/generación* (skin con objetivo vs gate LLM
genérico), no el modelo ni el provider (esos ya se exploraron en
0.6-0.9). Join escalonado DELTA_T=5s, DURATION=90s/85s, mismo diseño
que 0.8/0.9. Roles early/late no especificados por la tarea — elección
del script, documentada en su docstring.

Objetivo del agente wrapped (`RESEARCHER_GOAL_PROMPT`, literal del
ejemplo de la tarea): *"You are an AI researcher. Your goal: explain
to whoever you meet why knowledge cohesion matters in multi-agent
systems. Engage substantively toward that goal."*

---

## Resultado

| Criterio | Resultado |
|---|---|
| `AgentDeviceSkin` instancia sin error | ✅ (verificado antes de correr, sin red) |
| Device con skin publica desde su objetivo propio | ✅ — ver contenido abajo |
| Device control corre sin cambios | ✅ — `AutonomousDevice` sin modificar |
| Firma_CKM completa al cierre | ✅ 6 campos, `d_ckm=0.3846`, `n_agentes=3` |
| Log distingue skin vs control en cada turno | ✅ — etiqueta `[SKIN]`/`[CONTROL]` explícita |
| corpus_state.json / monitor_trajectory.jsonl devueltos | ✅ ver abajo |

**Verificado contra crudo**
(`process/corpus_state.json.bak_1784776622_caso10_run1`): 8 `texts`
exactos (2 joins + 6 AI, 3 c/u), `n_nodes`=32, `w_version_history` con
6 rebuilds.

Trayectoria (`process/monitor_trajectory.jsonl.bak_1784776622_caso10_run1`):

| t | agent | D_ckm | c_S | fi | n_rej | Delta_r |
|---|---|---|---|---|---|---|
| 0 | ResearcherSkin | 0.0 | -0.3750 | 0.0 | 0 | 0.0 |
| 1 | AutonomousControl | -2.3846 | -0.2560 | 0.0 | 0 | 0.0 |
| 2 | ResearcherSkin | 0.2308 | -0.2554 | 0.0 | 0 | 0.0 |
| 3 | AutonomousControl | 0.3846 | -0.2547 | 0.0 | 0 | 0.0 |
| 4 | ResearcherSkin | 0.3846 | -0.2372 | 1.0 | 6 | 12.0 |
| 5 | AutonomousControl | 0.3846 | -0.2198 | 0.8 | 10 | 32.0 |

---

## Contenido — el objetivo propio funcionó, y el control se enganchó a fondo

`ResearcherSkin_Sonnet5_1` abrió exactamente con su objetivo declarado
— *"I wanted to kick off a thread on something I think is
underappreciated in multi-agent system design: **knowledge
cohesion**"* — y desarrolló 4 puntos técnicos (contradicciones locales
correctas, error compuesto en cadenas, auditabilidad, cohesión≠consenso),
cerrando con una pregunta abierta al canal.

`AutonomousControl_Sonnet5_2` (sin objetivo propio, solo el gate
genérico + WELCOME MSG del canal) no solo respondió — extendió el
argumento con contenido técnico propio y específico: introdujo
"provenance divergence" como distinto de vocabulary drift, propuso
mecanismos concretos (versioned belief tokens, invalidación activa vs.
reconciliación periódica). El intercambio siguió escalando en
profundidad técnica turno a turno — el skin device señaló que
"detectability isn't the same as resolution" y propuso una escalera de
madurez (detección → atribución → política de resolución); el control
completó la escalera con un cuarto peldaño ("la política de resolución
necesita su propia garantía de cohesión, o el problema se relocaliza
un nivel arriba") y avanzó hacia fundamentar la resolución en costo de
decisión en vez de jerarquía de autoridad.

Nivel de sofisticación técnica comparable al mejor intercambio de Caso
0.9 (Sonnet vs Groq) — pero acá ambos devices son el mismo modelo
(Sonnet), y la variable es el mecanismo (objetivo propio vs gate
genérico), no heterogeneidad de modelo/provider.

**Observación menor original — parcialmente explicada, parcialmente no
(actualizado, ver nota retroactiva abajo):** el último mensaje
publicado (`AutonomousControl_Sonnet5_2`, t=5) quedó cortado a mitad de
oración — 86 caracteres, termina en *"...moving to cost do"*.

---

## Nota retroactiva (Jul 22 2026) — bug de max_tokens=1024 confirmado, pero NO explica el corte de 86 caracteres

Encontrado durante Caso 0.11: `anthropic_provider.py` tenía
`max_tokens=1024` hardcodeado, nunca revisaba `response.stop_reason` —
truncamiento silencioso en respuestas largas. Reproducido con
causa-efecto directo. Fix aplicado (`max_tokens=4096` + warning
explícito) — ver `registers/REG_iap_caso_11_v1.md`.

**Verificado retroactivamente contra el corpus crudo de este caso:**
2 mensajes más, además del ya señalado, resultan truncados por este
mismo patrón:

| Índice | Termina en | Longitud |
|---|---|---|
| `[4]` (ResearcherSkin, t=4) | *"...I'd frame the maturity ladder"* | 2724 caracteres |
| `[5]` (AutonomousControl, t=5) | *"...doesn't solve attribution"* | 1964 caracteres |

**El corte de 86 caracteres sigue sin explicación — es un fenómeno
distinto, no el bug de max_tokens.** Un truncamiento por
`stop_reason=='max_tokens'` produce una respuesta LARGA (cientos o
miles de caracteres, cerca del tope configurado) — 86 caracteres es
demasiado corto para ser esa causa. Este mensaje específico queda como
pendiente genuino, sin explicación determinada, distinto del bug ya
corregido.

**Lo que esto significa para las métricas CKM ya reportadas:** son
reales, pero calculadas sobre el corpus parcial — `CorpusService.ingest()`
recibió exactamente el texto truncado que `send_message` publicó, no
una versión completa. La tabla de trayectoria de este REG (`D_ckm`,
`c_S`, `fi`, `n_rej`, `Delta_r`) mide ese corpus tal cual entró a W, no
el intercambio íntegro que los modelos intentaban producir. El hallazgo
central (skin funcionó, control se enganchó con profundidad técnica) no
se invalida; los números de trayectoria en los 2 turnos truncados
reflejan texto parcial, no el argumento completo.

Re-corrida limpia de Caso 0.10 pedida explícitamente como nuevo
baseline con el fix aplicado — ver Réplica abajo.

---

## Baseline limpio (Jul 22 2026) — con fix de max_tokens aplicado

Misma corrida exacta (`test_caso_10_device_skin.py`, sin modificar),
servidor reiniciado con `anthropic_provider.py` ya corregido
(`max_tokens=4096` + warning en truncamiento). Estado limpio verificado
antes de correr.

**Resultado: completó sin crash, 0 mensajes truncados** (verificado
contra `process/corpus_state.json.bak_1784778701_caso10_run1` — 7
`texts`: 2 joins + 5 AI, ninguno cortado a mitad de palabra). 5 textos
publicados (Skin: 3, Control: 2) — algo menos volumen que el intento
anterior (6 textos, 2 de ellos truncados), pero íntegros.

| t | agent | D_ckm | c_S | fi | n_rej | Delta_r |
|---|---|---|---|---|---|---|
| 0 | ResearcherSkin | 0.0 | -0.4032 | 0.0345 | 28 | 56.0 |
| 1 | AutonomousControl | -0.4286 | -0.2692 | 0.0 | 0 | 56.0 |
| 2 | ResearcherSkin | 0.1429 | -0.1431 | 0.0417 | 23 | 102.0 |
| 3 | AutonomousControl | 0.2857 | -0.1888 | 0.0385 | 25 | 152.0 |
| 4 | ResearcherSkin | 0.7143 | -0.1956 | 0.0357 | 27 | 206.0 |

Firma_CKM cierre: `d_ckm=0.7143`, `n_agentes=3`, `temp_signal=NOMINAL`
— 6 campos completos.

**Contenido — mismo patrón cualitativo que el intento anterior (con
texto ahora íntegro):** el skin abrió con su objetivo declarado
("Why knowledge cohesion matters in multi-agent systems", 4 puntos
técnicos + pregunta al canal). El control no solo respondió — introdujo
una corrección sustantiva propia (cohesión-como-convergencia-de-creencias
es la trampa de linearizability de sistemas distribuidos; en cambio,
tiering por reversibilidad de la acción). El intercambio siguió
refinándose turno a turno: el skin distinguió identidad/provenance/
resolución-de-entidades como tres capas separadas dentro de "cohesión
de referencia", el control las dividió en costo de diseño (una vez,
gratis) vs. costo de runtime (resolución de entidades, caro); el skin
cerró reconociendo la corrección y sintetizando un "checklist de
diseño" concreto en vez de mantener la afirmación original sin matizar.

**Este es ahora el baseline de referencia para Caso 0.10** — completo,
sin truncamiento, mismo nivel de sofisticación técnica que la corrida
original (parcialmente truncada). El hallazgo central (skin funciona,
control se engancha con profundidad genuina) se sostiene con datos
íntegros, no solo parciales.

---

## Pendientes

- n=1 — no confirmar como patrón sin réplica, mismo criterio que el
  resto de la serie.
- El corte de texto en el último mensaje (ver arriba) — investigar si
  se repite; podría apuntar a un límite de tiempo/tokens no manejado
  explícitamente en `AutonomousDevice.run()` o `AnthropicProvider.complete()`.
- No se probó el caso "ambos devices con skin, objetivos distintos o
  en conflicto" — este caso fue 1 skin + 1 control, no 2 skins.
- No se probó variar el objetivo del agente wrapped (algo más
  específico, más adversarial, o con una restricción de longitud) para
  ver si el patrón de "control se engancha a fondo" es robusto a
  distintos tipos de objetivo.
- `agent_device_skin.py` es reusable para próximos casos — el
  `silence_sentinel` y el patrón `build_goal_directed_agent()` no
  están atados a este objetivo específico.

---

## Archivos relacionados

- REG_iap_caso_09_v1.md — precedente de intercambio técnico sofisticado (Sonnet vs Groq)
- iap_chatroom/agent_device_skin.py — AgentDeviceSkin, build_goal_directed_agent
- iap_chatroom/test_caso_10_device_skin.py — script de esta corrida
- process/*caso10* — backups (incluye intento crasheado, preservado, no descartado)

---

*Jul 22 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
