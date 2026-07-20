"""
autonomous_device.py — AutonomousDevice

Device AI autónomo para IAP Chatroom. A diferencia de los scripts de
simulación (test_iap_simulation*.py), que orquestan turnos en secuencia
fija, AutonomousDevice corre su propio loop asíncrono de polling MCP.

Caso 0.4: el loop implementa el ciclo ODA (Observación · Decisión ·
Acción) explícito. _observe() recolecta campo CKM + historial del canal
(sin LLM). _decide() evalúa esa observación con el gate LLM y devuelve
INTERACT u OP_SILENCE. _interact() ejecuta la decisión: publica o no.

Sin bootstrap bypass: D_ckm=None es una observación de campo válida
(el corpus todavía está acumulando), no un caso especial que salte el
gate. El device decide igual, con el campo que haya.
"""

from __future__ import annotations

import asyncio
import re
import time
from typing import Optional

from fastmcp import Client

from iap_chatroom.providers.base import ChatMessage, Provider

GATE_PROMPT_04 = """Field state:
D_ckm={d_ckm} | temp_signal={temp} | c_S={c_s} | fi={fi} | Delta_r={delta_r}

Recent messages:
{history}

Incoming: {sender}: "{text}"

Respond with exactly one word: INTERACT or OP_SILENCE."""


def _strip_own_prefix(text: str, device_id: str) -> str:
    """
    Elimina prefijos `[device_id]:` anidados al inicio del texto.

    El modelo ve `[device_id]: texto` en su propio historial (formato
    de _to_chat_messages) e imita el prefijo en su propia respuesta;
    sin este strip, el prefijo se anida uno por turno.
    """
    pattern = rf"^(\[{re.escape(device_id)}\]:\s*)+"
    return re.sub(pattern, "", text).strip()


def _coalesce(messages: list[ChatMessage]) -> list[ChatMessage]:
    """Fusiona mensajes consecutivos del mismo role (requisito de alternancia de Anthropic)."""
    if not messages:
        return messages
    merged: list[ChatMessage] = [dict(messages[0])]
    for m in messages[1:]:
        if m["role"] == merged[-1]["role"]:
            merged[-1]["content"] = merged[-1]["content"] + "\n" + m["content"]
        else:
            merged.append(dict(m))
    return merged


class AutonomousDevice:
    """
    Device AI autónomo para IAP Chatroom.
    Loop: recibe mensajes via polling MCP → ciclo ODA (observar campo +
    historial, decidir INTERACT/OP_SILENCE, actuar) → OP_SILENCE es
    salida real, no omisión.
    """

    def __init__(
        self,
        device_id: str,
        provider: Provider,        # de iap_chatroom/providers/
        system_prompt: str,
        mcp_url: str = "http://localhost:7860/mcp",
        poll_interval: float = 2.0,   # segundos entre polls
    ):
        self.device_id = device_id
        self.provider = provider
        self.system_prompt = system_prompt
        self.mcp_url = mcp_url
        self.poll_interval = poll_interval
        self._history: list[dict] = []

    def _to_chat_messages(self) -> list[ChatMessage]:
        chat: list[ChatMessage] = [{"role": "system", "content": self.system_prompt}]
        for m in self._history:
            role = "assistant" if m["device_id"] == self.device_id else "user"
            chat.append({"role": role, "content": f"[{m['device_id']}]: {m['text']}"})
        system_msgs = [c for c in chat if c["role"] == "system"]
        turn_msgs = _coalesce([c for c in chat if c["role"] != "system"])
        return system_msgs + turn_msgs

    async def _generate(self) -> str:
        """Construye el prompt con historial acumulado del canal y llama al provider."""
        text = await self.provider.complete(self._to_chat_messages())
        return _strip_own_prefix(text, self.device_id)

    async def _observe(self, client: Client, message: dict) -> dict:
        """
        Fase O del ciclo ODA. No LLM — solo recolección de datos.

        Recolecta estado externo (campo CKM + historial del canal) y
        estado interno (propias publicaciones recientes). Si CKMMonitor
        no está disponible o el corpus aún acumula, field trae D_ckm=None
        y el resto de las métricas en None — observación válida, no error.
        """
        field_result = await client.call_tool("get_monitor_state", {})
        field_state = field_result.data

        history_result = await client.call_tool("get_messages", {"since": None})
        history = history_result.data

        return {
            "field": field_state,
            "history": history,
            "trigger": message,
            "own_recent": [
                m for m in history[-20:] if m.get("device_id") == self.device_id
            ],
        }

    async def _decide(self, observation: dict) -> str:
        """
        Fase D del ciclo ODA. LLM evalúa la observación y decide.

        CKM orienta — no impone. Sin bypass: D_ckm=None llega al prompt
        igual que cualquier otro valor de campo, el device decide con lo
        que tiene. Devuelve "INTERACT" o "OP_SILENCE".
        """
        field = observation["field"]
        history = observation["history"]
        trigger = observation["trigger"]

        history_text = (
            "\n".join(f'{m["device_id"]}: {m["text"]}' for m in history[-10:])
            if history
            else "(empty)"
        )

        gate_prompt = GATE_PROMPT_04.format(
            d_ckm=field.get("D_ckm"),
            temp=field.get("temp_signal", "UNKNOWN"),
            c_s=field.get("c_S"),
            fi=field.get("fi"),
            delta_r=field.get("Delta_r"),
            history=history_text,
            sender=trigger.get("device_id", "unknown"),
            text=trigger.get("text", ""),
        )

        response = await self.provider.complete([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": gate_prompt},
        ])

        word = response.strip().upper().split()[0] if response.strip() else "OP_SILENCE"
        return word if word in ("INTERACT", "OP_SILENCE") else "OP_SILENCE"

    async def _interact(self, client: Client, decision: str, observation: dict) -> None:
        """
        Fase A del ciclo ODA.

        OP_SILENCE: no publica. Sin anuncio, sin log en el corpus del
        canal — solo log local de proceso.
        INTERACT: genera contenido (con el historial completo del canal,
        vía _to_chat_messages/_generate) y publica.
        """
        field_state = observation["field"]

        if decision == "OP_SILENCE":
            self._log("OP_SILENCE", field_state)
            return

        text = await self._generate()
        await client.call_tool(
            "send_message", {"device_id": self.device_id, "text": text}
        )
        self._history.append(
            {"device_id": self.device_id, "device_type": "AI", "text": text}
        )
        self._log("INTERACT", field_state)

    def _log(self, decision: str, field_state: Optional[dict] = None) -> None:
        if field_state is not None:
            d_ckm = field_state.get("D_ckm")
            temp = field_state.get("temp_signal", "UNKNOWN")
            print(f"[{self.device_id}] {decision} (D_ckm={d_ckm}, temp={temp})")
        else:
            print(f"[{self.device_id}] {decision}")

    async def run(self, duration: float = 60.0) -> None:
        """Loop principal. Corre durante `duration` segundos."""
        async with Client(self.mcp_url) as client:
            # last_ts se captura ANTES de join_channel, no después: el
            # join emite un mensaje SYSTEM en el propio channel.publish()
            # (ver mcp_server.py) — si last_ts se tomara después, ese
            # evento quedaría más viejo que el cutoff del primer poll y
            # get_messages(since=last_ts) lo descartaría en silencio.
            last_ts = time.time()

            r = await client.call_tool(
                "join_channel", {"device_id": self.device_id, "device_type": "AI"}
            )
            assert r.data["ok"], f"join_channel fallo para {self.device_id}"

            start = time.monotonic()

            while time.monotonic() - start < duration:
                fetched = await client.call_tool("get_messages", {"since": last_ts})
                new_messages = fetched.data
                last_ts = time.time()

                for message in new_messages:
                    # Regla estructural — no comunicacional: nunca triggerear
                    # sobre el propio mensaje visto en el poll.
                    if message["device_id"] == self.device_id:
                        continue

                    self._history.append(message)

                    # Regla estructural: solo AI/HUMAN/SYSTEM disparan el
                    # ciclo ODA (Caso 0.5 — el join event SYSTEM puede
                    # actuar como seed). Otros tipos no-LNH quedan fuera.
                    if message.get("device_type") not in ("AI", "HUMAN", "SYSTEM"):
                        continue

                    observation = await self._observe(client, message)
                    decision = await self._decide(observation)
                    await self._interact(client, decision, observation)

                await asyncio.sleep(self.poll_interval)

            r = await client.call_tool("leave_channel", {"device_id": self.device_id})
            assert r.data["ok"], f"leave_channel fallo para {self.device_id}"
