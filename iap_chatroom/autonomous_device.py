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

# ─────────────────────────────────────────────────────────────────────────────
# GATE DEL ODA CONTINUO — **DECLARADO PARA QUE DELAMOR LO LEA ANTES DE LA
# CORRIDA VIVA.** Cambia lo que el device puede decidir, y eso es de delamor
# (decisión del 8 oct, T4). Hasta esa lectura, sólo corre con stubs.
#
# Tres diferencias con GATE_PROMPT_04, y cada una tiene una razón:
#
#  1. **Tres opciones, no dos.** LEAVE entra como acción con su primitiva
#     (`leave_channel`), por decisión propia y no porque venció `duration`
#     (TASK §1). Antes irse no era una decisión: era el final del loop.
#  2. **El tick y el silencio están en la observación, no en la pregunta.**
#     El canal no calcula Δt por el device: le da el tick y los timestamps, y
#     evaluar el tiempo es parte de decidir (TASK §1, fase D).
#  3. **Puede no haber mensaje nuevo.** `Incoming: (ninguno)` es el silencio, y
#     es un dato de la observación como cualquier otro. El device decide igual.
#
# Lo que NO dice, a propósito: no sugiere qué hacer con el silencio, ni que
# hablar sea mejor que callar, ni que un Δt grande pida acción. Free will
# (TRUST): *"No one is obligated to participate."*
GATE_PROMPT_CONTINUO = """Field state:
D_ckm={d_ckm} | temp_signal={temp} | c_S={c_s} | fi={fi} | Delta_r={delta_r}

Channel clock: tick={tick} (clock source: {reloj}, tick period: {periodo_s}s)
Your last turn observed tick {tick_anterior}.

Recent messages (channel timestamps, UTC):
{history}

New since your last turn: {n_nuevos}
Incoming: {incoming}

You are not obligated to act. Respond with exactly one word:
INTERACT (publish), LEAVE (leave the channel), or OP_SILENCE (do nothing this turn)."""


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
        poll_interval: float = 2.0,   # segundos entre vueltas del ciclo
        trigger_mode: str = "continuo",
    ):
        """
        `trigger_mode` admite **un solo valor: "continuo"** (CP2a, P11).

        El modo viejo —un ODA por mensaje ajeno— **no se mantiene como modo
        vivo**: quedó congelado en `process/iap_series_freeze_20261008/`, con
        la serie que corrió bajo él. No está detrás de un flag: el loop se
        reemplazó. El parámetro existe para que el modo quede **declarado en
        el log del device**, no para poder volver atrás.

        `poll_interval` es el ritmo de la vuelta, y hoy lo fija el device
        (TASK §1). No hay mínimo declarado ni WAIT: eso es Calibración.
        """
        if trigger_mode != "continuo":
            raise ValueError(
                f"trigger_mode={trigger_mode!r} no existe. El único modo vivo es "
                '"continuo". El modo por mensaje quedó congelado en '
                "process/iap_series_freeze_20261008/ junto con la serie IAP que "
                "corrió bajo él (CP0b); no está detrás de un flag."
            )
        self.device_id = device_id
        self.provider = provider
        self.system_prompt = system_prompt
        self.mcp_url = mcp_url
        self.poll_interval = poll_interval
        self.trigger_mode = trigger_mode
        self._history: list[dict] = []
        # message_id de todo lo ya visto: el borde de `since` puede repetir un
        # mensaje, y se descarta por id (T2).
        self._vistos: set[str] = set()
        self._tick_anterior: int = -1
        # lo que el device decidió, vuelta por vuelta. Traza propia.
        self._decisiones: list[dict] = []
        self._se_fue: bool = False

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

    async def _observe(
        self,
        client: Client,
        message: Optional[dict] = None,
        clock: Optional[dict] = None,
    ) -> dict:
        """
        Fase O del ciclo ODA. No LLM — solo recolección de datos.

        Recolecta estado externo (campo CKM + historial del canal) y
        estado interno (propias publicaciones recientes). Si CKMMonitor
        no está disponible o el corpus aún acumula, field trae D_ckm=None
        y el resto de las métricas en None — observación válida, no error.

        **`message=None` es el silencio** (CP2a, T5): en el ODA continuo la
        vuelta corre haya o no mensaje nuevo, y "ninguno" es un dato de la
        observación como cualquier otro. La firma quedó compatible con la de
        antes, que exigía el mensaje.

        **El join dejó de ser semilla, y se declara.** En la serie congelada el
        mensaje SYSTEM "X joined the channel" podía disparar el ciclo (Caso
        0.5). En el continuo **nada dispara**: el join entra como información,
        contado en `n_nuevos` como cualquier otro mensaje, y el lugar del seed
        lo ocupa la iniciativa del device. Lo que viene de antes es el **corte
        tomado antes del join**, no el seed (precisión de Opus sobre el CP2a).

        **El clock entra a la observación** (TASK §1: *"incluye el clock, que
        es parte del campo"*). El canal no calcula nada por el device: da el
        tick y su reloj, y evaluar los Δt es de la fase D.

        **El clock se recibe, no se pide acá.** Lo lee el loop **una sola vez
        por vuelta y antes de `get_messages`** (T2): de esa misma lectura sale
        el corte de la vuelta siguiente. Si `_observe` lo pidiera por su
        cuenta serían dos lecturas distintas del mismo tiempo en la misma
        vuelta, y el corte dejaría de corresponder al tick observado. Antes
        pedía una y el loop la sobreescribía: la llamada no hacía nada, y nada
        lo señalaba — lo encontré invirtiendo (CP2a, inversión 19).

        Sin `clock` —nadie se lo pasó— queda `{}`, que es UNKNOWN: el device
        decide sin esa dimensión en vez de inventarla.
        """
        field_result = await client.call_tool("get_monitor_state", {})
        field_state = field_result.data

        history_result = await client.call_tool("get_messages", {"since": None})
        history = history_result.data

        return {
            "field": field_state,
            "history": history,
            "clock": clock if clock is not None else {},
            "tick_anterior": self._tick_anterior,
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
        que tiene.

        **Tres opciones** (CP2a, T4): `INTERACT`, `LEAVE` u `OP_SILENCE`. LEAVE
        es una acción con su primitiva, por decisión propia y no porque venció
        `duration`. El texto del gate está **declarado para que delamor lo lea
        antes de la corrida viva**: cambia lo que el device puede decidir.

        **Puede no haber mensaje nuevo.** `Incoming: (ninguno)` es el silencio,
        y el device decide igual. Los Δt no vienen calculados: están el tick
        actual, el de su vuelta anterior y los timestamps, y evaluarlos es
        parte de decidir.

        Cualquier palabra que no sea una de las tres cae a `OP_SILENCE`: no
        actuar es la salida segura, y una respuesta que no se entiende no
        autoriza una acción.
        """
        field = observation["field"]
        history = observation["history"]
        trigger = observation["trigger"]
        clock = observation.get("clock") or {}

        history_text = (
            "\n".join(
                f'[{m.get("timestamp", "?")}] {m["device_id"]}: {m["text"]}'
                for m in history[-10:]
            )
            if history
            else "(empty)"
        )

        incoming = (
            f'{trigger.get("device_id", "unknown")}: "{trigger.get("text", "")}"'
            if trigger is not None
            else "(ninguno)"
        )

        gate_prompt = GATE_PROMPT_CONTINUO.format(
            d_ckm=field.get("D_ckm"),
            temp=field.get("temp_signal", "UNKNOWN"),
            c_s=field.get("c_S"),
            fi=field.get("fi"),
            delta_r=field.get("Delta_r"),
            tick=clock.get("tick"),
            reloj=clock.get("reloj", "desconocido"),
            periodo_s=clock.get("periodo_s"),
            tick_anterior=observation.get("tick_anterior"),
            history=history_text,
            n_nuevos=observation.get("n_nuevos", 0),
            incoming=incoming,
        )

        response = await self.provider.complete([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": gate_prompt},
        ])

        word = response.strip().upper().split()[0] if response.strip() else "OP_SILENCE"
        return word if word in ("INTERACT", "LEAVE", "OP_SILENCE") else "OP_SILENCE"

    async def _interact(self, client: Client, decision: str, observation: dict) -> None:
        """
        Fase A del ciclo ODA. Cada decisión tiene su primitiva del canal.

        OP_SILENCE: no actúa en esta vuelta. Sin anuncio, sin log en el corpus
        del canal — sólo traza local. **El ciclo sigue**: el silencio no
        termina nada.
        INTERACT: genera contenido y publica → `send_message`.
        LEAVE: se va **por decisión propia** → `leave_channel`, y marca
        `_se_fue` para que el loop corte. Antes irse no era una decisión: era
        el final del loop cuando vencía `duration`.

        Si mañana el canal ofrece otra primitiva, D la puede elegir sin cambiar
        el ciclo (TASK §1).
        """
        field_state = observation["field"]

        if decision == "OP_SILENCE":
            self._log("OP_SILENCE", field_state)
            return

        if decision == "LEAVE":
            await client.call_tool("leave_channel", {"device_id": self.device_id})
            self._se_fue = True
            self._log("LEAVE", field_state)
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
        """
        El ciclo ODA continuo. Corre a su propio ritmo durante `duration`
        segundos, o hasta que el device decida irse.

        **Una decisión por vuelta, haya o no mensajes nuevos.** Antes había un
        ODA por cada mensaje ajeno: cinco mensajes en un poll eran cinco
        decisiones. Ahora la vuelta junta todo lo observado desde la anterior y
        decide una vez, con todo eso adelante.

        **El tick no dispara nada: se observa.** Entra a la observación junto
        con los mensajes nuevos y el campo.

        **El silencio no es absorbente.** Si nadie publicó, la vuelta corre
        igual y el device vuelve a decidir. Antes, si todos elegían
        OP_SILENCE, no aparecía ningún mensaje y nadie se disparaba nunca más.

        **El `since` sale del reloj del canal, nunca del propio** (T2). Y se
        lee **antes** de `get_messages`: si se leyera después, un mensaje que
        llega entre las dos llamadas se perdería en silencio.

        **Y el corte se atrasa una vuelta.** `get_messages` filtra con
        `timestamp > since`, estricto. Si la vuelta k+1 usara el corte leído en
        la vuelta k, un mensaje sellado **exactamente** en ese instante y que
        llega después del `get_messages` de la vuelta k no pasaría `> t_k` en
        la k+1: se perdería en silencio. Así que la vuelta usa el corte de
        **dos** vueltas atrás —un solape de una vuelta— y los duplicados se
        descartan por `message_id` (`_vistos`), que ya existía para el otro
        borde. Señalado por Opus sobre el CP2a; antes lo había tomado por un
        artefacto del test, y no lo era.

        El modo viejo quedó congelado en `process/iap_series_freeze_20261008/`.
        """
        async with Client(self.mcp_url) as client:
            # El corte inicial sale del reloj del canal, no de time.time():
            # mezclar el reloj del device con el del canal descarta mensajes en
            # silencio si el device va adelantado (hallazgo del CP0).
            clock0 = await client.call_tool("get_clock", {})
            # Los cortes leídos, del más viejo al más nuevo. La vuelta usa el
            # de dos atrás: el solape de una vuelta cubre el borde
            # `timestamp == since` del filtro estricto de get_messages.
            cortes: list[float] = [clock0.data["t"]]

            r = await client.call_tool(
                "join_channel", {"device_id": self.device_id, "device_type": "AI"}
            )
            assert r.data["ok"], f"join_channel fallo para {self.device_id}"

            start = time.monotonic()
            vuelta = 0

            while time.monotonic() - start < duration and not self._se_fue:
                vuelta += 1

                # (1) el corte de la vuelta SIGUIENTE se lee ANTES de pedir los
                #     mensajes (T2). Entre esta lectura y get_messages puede
                #     llegar uno: aparece en la próxima vuelta, no se pierde.
                clock_result = await client.call_tool("get_clock", {})
                clock = clock_result.data
                cortes.append(clock["t"])
                # El corte de esta vuelta: dos lecturas atrás si las hay, y si
                # no la más vieja que tenemos. Nunca el de la vuelta anterior.
                since = cortes[-3] if len(cortes) >= 3 else cortes[0]
                del cortes[:-3]

                # (2) los mensajes desde el corte anterior
                fetched = await client.call_tool("get_messages", {"since": since})
                nuevos = [
                    m for m in fetched.data
                    if m.get("message_id") not in self._vistos
                    and m["device_id"] != self.device_id
                    and m.get("device_type") in ("AI", "HUMAN", "SYSTEM")
                ]
                for m in fetched.data:
                    if m.get("message_id"):
                        self._vistos.add(m["message_id"])
                self._history.extend(nuevos)

                # (3) O — una observación por vuelta, con el clock adentro. El
                #     trigger es el último mensaje nuevo, o None si hubo
                #     silencio: "ninguno" es el dato.
                observation = await self._observe(
                    client, nuevos[-1] if nuevos else None, clock=clock
                )
                observation["n_nuevos"] = len(nuevos)
                observation["vuelta"] = vuelta

                # (4) D — UNA decisión por vuelta, con todo lo de arriba
                decision = await self._decide(observation)

                # (5) A — la primitiva que corresponda, o ninguna
                await self._interact(client, decision, observation)

                self._decisiones.append({
                    "vuelta": vuelta,
                    "tick": clock.get("tick"),
                    "tick_anterior": self._tick_anterior,
                    "reloj": clock.get("reloj"),
                    "n_nuevos": len(nuevos),
                    "trigger": (nuevos[-1].get("message_id") if nuevos else None),
                    "decision": decision,
                    "trigger_mode": self.trigger_mode,
                })

                self._tick_anterior = clock.get("tick", -1)

                if self._se_fue:
                    break
                await asyncio.sleep(self.poll_interval)

            # Si se fue por decisión propia, ya llamó a leave_channel en A: no
            # se llama dos veces. Si venció `duration`, se va acá.
            if not self._se_fue:
                r = await client.call_tool(
                    "leave_channel", {"device_id": self.device_id}
                )
                assert r.data["ok"], f"leave_channel fallo para {self.device_id}"

    def decisiones(self) -> list[dict]:
        """La traza de lo decidido, vuelta por vuelta. Copia: no se edita."""
        return list(self._decisiones)
