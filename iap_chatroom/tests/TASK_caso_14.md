TASK_caso_14.md
*Jul 2026 — gadanin.delamor*

## Descripción

Caso 0.14 — Caso 0.13 + leak fix + una variable aislada.

Dos cambios respecto a 0.13, ambos explícitos:

1. **Leak fix ya aplicado** (misma sesión, antes de este caso):
   `build_goal_directed_agent` (`agent_device_skin.py`) y
   `build_search_grounded_agent` (`groq_research_agent.py`) detectan
   el sentinel por contención (`silence_sentinel in text.upper()`),
   no por igualdad exacta. Verificar que ambos archivos tienen el fix
   antes de correr — no asumirlo.

2. **`TinkerBellucio`'s prompt, completamente en inglés.** Caso 0.13
   tuvo la única palabra en español de los tres prompts —
   "Be precise. Be trazable." — dentro del `goal_system_prompt` de
   Tinker. Tinker (Sonnet) fue el único device, en toda la serie
   0.4-0.13, que respondió en español — sus 3 mensajes reales,
   persistente a través de toda la corrida, rodeada de inglés en cada
   lectura de historial. Caso 0.14 aísla esa variable: mismo diseño
   exacto, mismos tres devices, misma dependencia estructural, mismo
   topic — cambia únicamente "trazable" → "traceable" en el prompt de
   Tinker. Si el idioma de publicación de Tinker cambia a inglés, la
   hipótesis de la palabra-semilla queda reforzada (n=1, no
   confirmada, pero consistente). Si Tinker sigue en español pese al
   prompt ahora 100% inglés, la causa no es (solo) esa palabra.

## Devices — idénticos a 0.13, con el cambio de prompt en Tinker

| device_id | rol | mecanismo | provider/modelo |
|---|---|---|---|
| `PeterPlam` | orquestador | `AgentDeviceSkin` + `build_goal_directed_agent` | Anthropic, `claude-haiku-4-5-20251001` |
| `TinkerBellucio` | analista | `AgentDeviceSkin` + `build_goal_directed_agent` | Anthropic, `claude-sonnet-5` |
| `MarkOpolus` | forecaster | `AgentDeviceSkin` + `build_search_grounded_agent` | Groq, `llama-3.3-70b-versatile` |

Único cambio de texto: en `TINKER_GOAL_PROMPT`, la línea
`"Publish your map in the channel. Be precise. Be trazable."` pasa a
`"Publish your map in the channel. Be precise. Be traceable."`

Todo lo demás — topic, dependencia estructural, join simultáneo,
DURATION=120s, POLL_INTERVAL=2.0s, gate prompts combinados —
idéntico a `TASK_caso_13.md`.

## Lo que CKM va a medir (además de lo ya medido en 0.13)

- Idioma real de publicación de `TinkerBellucio` — español, inglés, o
  mixto.
- 0 fugas de sentinel esperadas en `PeterPlam`/`MarkOpolus` (fix ya
  aplicado) — verificar contra el crudo, no asumir por el fix estar
  aplicado.

## Pendiente explícito

n=1 — este caso no reemplaza a 0.13 como dato, lo complementa. Si el
resultado difiere, ninguno de los dos es "el" resultado — son dos
puntos de una misma variable, y hace falta más de un run para tratar
cualquiera de los dos como patrón.
