"""
agent_device_skin.py — AgentDeviceSkin

Subclase de AutonomousDevice que delega la decisión ODA (INTERACT vs
OP_SILENCE) — y el contenido publicado — a un agente externo ("wrapped
agent") con objetivo propio, en vez del gate LLM genérico de
autonomous_device.py.

------------------------------------------------------------------
Desviación explícita de la tarea original, acordada antes de escribir
código (ver conversación — pregunta directa, respuesta: opción
recomendada):
------------------------------------------------------------------
La tarea pedía sobreescribir ÚNICAMENTE _decide(). Pero _interact()
(heredado) publica llamando a self._generate(), que arma el prompt con
self.system_prompt (el WELCOME MSG del canal) y genera un texto nuevo
—no el texto que ya generó y devolvió wrapped_agent con SU PROPIO
system prompt. Sobreescribir solo _decide() habría descartado el texto
real del agente wrapped y publicado un texto distinto, regenerado con
el prompt equivocado.

Fix mínimo: además de _decide(), se sobreescribe _generate() — no
_interact(), no _observe(), no run(), que quedan 100% heredados sin
cambios, tal como pedía la tarea. _decide() cachea el texto que
devolvió wrapped_agent en self._pending_text; _generate() (heredado
originalmente vía self.provider.complete + self.system_prompt) ahora
devuelve ese texto cacheado en vez de generar uno nuevo. autonomous_device.py
no se modificó — confirmado con git status.
"""

from __future__ import annotations

from typing import Awaitable, Callable, Optional

from iap_chatroom.autonomous_device import (
    AutonomousDevice,
    _coalesce,
    _strip_own_prefix,
)
from iap_chatroom.providers.base import Provider

# observation: dict devuelto por AutonomousDevice._observe() —
#   {"field": {...D_ckm, temp_signal, fi...}, "history": [...],
#    "trigger": {...}, "own_recent": [...]}
# Debe ser una corrutina (async def) — internamente llama a un
# Provider.complete(), que es async.
WrappedAgent = Callable[[dict], Awaitable[Optional[str]]]


class AgentDeviceSkin(AutonomousDevice):
    """
    AutonomousDevice cuya decisión ODA la toma un agente externo con
    objetivo propio, no el gate LLM genérico (GATE_PROMPT_04).

    wrapped_agent(observation) -> Optional[str]:
        - Recibe el dict completo de _observe() (historial + campo crudo).
        - Devuelve str  → INTERACT, ese str es el texto publicado tal cual.
        - Devuelve None → OP_SILENCE.

    Sin gate LLM propio — la decisión y el contenido los define
    enteramente wrapped_agent. self.system_prompt (WELCOME_MSG del
    canal) sigue existiendo en la instancia pero no se usa para generar
    el texto publicado — solo el objetivo propio del agente wrapped.
    """

    def __init__(self, *args, wrapped_agent: WrappedAgent, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrapped_agent = wrapped_agent
        self._pending_text: Optional[str] = None

    async def _decide(self, observation: dict) -> str:
        result = await self.wrapped_agent(observation)
        if result is None:
            self._pending_text = None
            return "OP_SILENCE"
        self._pending_text = result
        return "INTERACT"

    async def _generate(self) -> str:
        """
        Devuelve el texto que wrapped_agent ya generó y cacheó en
        _decide() — no vuelve a llamar al provider con self.system_prompt.
        Fallback a la generación heredada solo por robustez defensiva;
        en operación normal _pending_text siempre está seteado cuando
        _interact() (heredado) llama a este método, porque _decide()
        solo devuelve "INTERACT" cuando wrapped_agent devolvió texto.
        """
        if self._pending_text is not None:
            text = self._pending_text
            self._pending_text = None
            return _strip_own_prefix(text, self.device_id)
        return await super()._generate()


def build_goal_directed_agent(
    device_id: str,
    provider: Provider,
    goal_system_prompt: str,
    silence_sentinel: str = "OP_SILENCE",
) -> WrappedAgent:
    """
    Helper para construir un wrapped_agent orientado a objetivo.

    Arma su propio historial de chat (mismo formato que
    AutonomousDevice._to_chat_messages: assistant=propio, user=ajeno,
    prefijo "[device_id]: "), pero con `goal_system_prompt` en vez del
    WELCOME MSG del canal — el objetivo es del agente, no del canal.
    Reusa _coalesce/_strip_own_prefix de autonomous_device.py en vez de
    reimplementar la lógica de alternancia de roles.

    Si el texto generado contiene `silence_sentinel` (en cualquier
    posición, no solo como string exacto — o texto vacío), el agente
    elige no publicar — wrapped_agent devuelve None. Fix quirúrgico
    (Jul 2026, ver REG_iap_caso_13_v1.md): antes exigía igualdad
    exacta, lo que dejaba pasar como contenido real cualquier texto
    que antepusiera prosa antes de "OP_SILENCE" — 12/23 textos no-join
    de Caso 0.13. No es la solución definitiva — hay una propuesta más
    completa en curso para más adelante. Riesgo conocido y no resuelto:
    si algún día un device menciona "OP_SILENCE" como parte de
    contenido real (discutiendo el propio mecanismo), también se
    suprimiría — no ocurrió en los datos vistos hasta ahora.
    """

    async def wrapped_agent(observation: dict) -> Optional[str]:
        history = observation["history"]
        trigger = observation["trigger"]

        messages = [{"role": "system", "content": goal_system_prompt}]
        for m in history[-10:]:
            role = "assistant" if m["device_id"] == device_id else "user"
            messages.append(
                {"role": role, "content": f"[{m['device_id']}]: {m['text']}"}
            )
        # Garantiza que la secuencia termine en rol "user": history es
        # el fetch completo del canal (get_messages), no self._history
        # de AutonomousDevice — puede terminar con el propio último
        # mensaje publicado si nadie más habló después, y el modelo
        # rechaza un prompt que termina en "assistant" (sin prefill).
        # trigger nunca es propio (run() lo filtra antes de llamar acá),
        # así que agregarlo al final garantiza terminar en "user";
        # _coalesce() lo fusiona si history ya terminaba en el mismo rol.
        trigger_sender = trigger.get("device_id", "unknown")
        trigger_text = trigger.get("text", "")
        messages.append({
            "role": "user",
            "content": f"[{trigger_sender}]: {trigger_text}",
        })
        system_msgs = [c for c in messages if c["role"] == "system"]
        turn_msgs = _coalesce([c for c in messages if c["role"] != "system"])
        messages = system_msgs + turn_msgs

        raw = await provider.complete(messages)
        text = _strip_own_prefix(raw, device_id).strip()

        if not text or silence_sentinel in text.upper():
            return None
        return text

    return wrapped_agent
