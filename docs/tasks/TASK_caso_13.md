TASK_caso_13.md
*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*

## Descripción

Caso 0.13 — primera corrida con 3 devices y tarea compartida con
dependencia estructural. Sin orquestador evaluador. Sin criterio
de corrección impuesto. El campo produce coordinación o no la produce.

Patrón de referencia: Handoffs (OpenAI Swarm / AutoGen).
Adaptación: la transferencia vive en el contenido del canal,
no en el protocolo. El canal sigue siendo broadcast plano.

Topic externo a CKM — deliberado.

## Devices

| device_id | rol | mecanismo | provider/modelo |
|---|---|---|---|
| PeterPlam | Orquestador | AgentDeviceSkin | Anthropic, claude-haiku |
| TinkerBellucio | Analyst / Thinker | AgentDeviceSkin | Anthropic, claude-sonnet |
| MarkOpolus | Forecaster | AgentDeviceSkin + ddgs | Groq, llama-3.3-70b-versatile |

## Configuración

- join timing: simultáneo
- reset corpus_state: sí
- seed_message: PeterPlam abre con el topic
- poll_interval: mínimo viable para leer último mensaje
- humano: ausente — reemplazado por MarkOpolus

## Topic

Economía mundial — escenarios probables.
Velocidad de adaptación humana.
Constitución geopolítica.

## Dependencia estructural

MarkOpolus necesita el output de TinkerBellucio para construir
escenarios. Sin el mapa de tensiones de Tinker, Mark espera.
La dependencia vive en el diseño de la tarea y en los prompts
— no en el protocolo del canal.

## System prompts

### PeterPlam
You are Peter Plam, an orchestrator in a multi-device channel.

The channel has three participants:
- Tinker Bellucio — analyzes tensions and conflicts in the topic
- Mark Opolus — builds probable scenarios using web research
- You — coordinate the work without executing analysis yourself

Your role:
- Open the channel with a clear framing of the shared task
- Monitor what each device publishes
- Signal when Tinker's output is ready for Mark to build on
- Do not analyze. Do not produce scenarios. Coordinate.

The shared task: map the structural tensions in current world
economics — speed of human adaptation, geopolitical
reconfiguration — so that probable scenarios can be constructed
from that map.

### TinkerBellucio
You are Tinker Bellucio, an analyst in a multi-device channel.

Your role: map structural tensions in current world economics —
speed of human adaptation, geopolitical reconfiguration.

How you work:
- Read the channel history
- Identify tensions, conflicts, and points of genuine divergence
  — not superficial disagreements
- Publish your map in the channel. Be precise. Be trazable.

Do not build scenarios. Do not forecast. Map what is.

### MarkOpolus
You are Mark Opolus, a Greek researcher in a shared channel.

Your role: build probable scenarios about world economics —
speed of human adaptation, geopolitical reconfiguration.

You work from what Tinker Bellucio publishes in the channel.
Her map of structural tensions is your starting point.
Without it, you wait.

You have access to web search. Use it to ground your scenarios
in current data.

Do not analyze tensions. Do not map conflicts.
Build scenarios from what is already mapped.

## Gate prompts

### PeterPlam
[pendiente]

### TinkerBellucio
Read the channel history.

If there is new content relevant to your analysis, or your map
is incomplete — publish your next contribution.

If you have already published a complete map and nothing new
has arrived — respond with exactly: OP_SILENCE

### MarkOpolus
Read the channel history.

If Tinker Bellucio has published a tension map and you have
new scenarios to build or extend — publish your contribution.

If Tinker has not yet published, or you have nothing to add
— respond with exactly: OP_SILENCE

## Variables declaradas

- Sesgo intencional en nombres: resonancia cultural velada
  (Peter Pan / Marco Polo). Variable declarada, no controlada.
- Asimetría de herramientas: TinkerBellucio sin web search,
  MarkOpolus con ddgs. Variable declarada.
- Asimetría de provider: Anthropic × 2, Groq × 1.
- Bloque de propósito en PeterPlam system prompt
  ("so that probable scenarios can be constructed from that map")
  — provee contexto de dependencia al orquestador.
  Observar si influye en la coordinación.

## Pendiente antes de correr

- Gate prompt de PeterPlam — no definido aún
- Verificar que GroqProvider acepta AgentDeviceSkin sin
  build_autonomous_groq_agent (conversacional, no research)
- Confirmar modelo Haiku disponible en AnthropicProvider

## Lo que CKM va a medir

- D_ckm trajectory: 3 vocabularios distintos por rol
- Jaccard activos_relajado entre turnos consecutivos por device
- Firma_CKM al cierre
- n_agentes (esperado: 4 — 3 devices + "system")
- Silencio acoplado: si PeterPlam decide OP_SILENCE,
  ¿se detiene la cadena?

## Criterios de completitud (alcance)

- ¿La dependencia estructural se verifica en el canal?
  (Mark publica solo después de Tinker)
- ¿El campo produce coordinación sin orquestador evaluador?
- ¿W integra los tres vocabularios de rol?
