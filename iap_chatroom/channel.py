"""
channel.py — ChatChannel

Canal de chat compartido entre devices (AI y HUMAN). Singleton: todos los
que llaman a ChatChannel() reciben la misma instancia y comparten el mismo
historial de mensajes y las mismas suscripciones WebSocket.

**El CLOCK del canal** (CP1 de TASK_canal_iap_clock_iniciativa_v2; decisión de
delamor, 8 oct):

  1. **El canal genera los ticks con su propio reloj**, el mismo que sella los
     mensajes. Una sola fuente: `_ahora()`.
  2. La Config **registra** el tick vigente; Monitor lo anota. El canal **no
     lee la Config** — la dependencia no se invierte.
  3. **Cada tiempo declara de qué reloj viene.** Acá, `reloj="canal"`.

Por qué hace falta: `message_id = "msg-{index}"` ya es monótono, pero avanza
sólo cuando hay un mensaje. El CLOCK avanza con el canal callado, y eso es el
punto — *"el silencio entre mensajes es dato medible, no ausencia de dato"*
(PROPUESTA v5, adenda).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable, List, Literal

from fastapi import WebSocket

# Período del tick, en segundos. **Declarado, no calibrado**: es el grano con
# el que el canal nombra el tiempo, y cambiarlo cambia la numeración de los
# ticks. Los umbrales de decisión son de Calibración y no viven acá.
TICK_PERIODO_S = 1.0

# De qué reloj viene cada tiempo que el canal produce (decisión 3). El canal
# sella todo con el suyo: no mezcla el del device ni el del proceso de Monitor.
RELOJ_CANAL = "canal"


@dataclass
class Message:
    device_id: str
    device_type: Literal["AI", "HUMAN", "SYSTEM"]
    text: str
    timestamp: str  # ISO8601, UTC, del reloj del canal, de recepción
    # El tick del canal en que llegó el mensaje, y de qué reloj viene el
    # timestamp (decisión 3). Con default para no romper los Message que se
    # construyan sin ellos (los JSONL históricos no los tienen).
    tick: int = -1
    reloj: str = "desconocido"

    def to_dict(self) -> dict:
        return asdict(self)


class ChatChannel:
    _instance: "ChatChannel | None" = None

    def __new__(cls) -> "ChatChannel":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self.messages: List[Message] = []
        self._subscribers: List[WebSocket] = []
        self._on_message_callbacks: List[Callable[[Message], None]] = []
        # t=0 del CLOCK: el momento en que el canal empezó a existir. El tick
        # se deriva de él, no se incrementa en un contador — así no depende de
        # que alguien llame a nada, y avanza con el canal callado.
        self._t0 = self._ahora()
        # Cada tick que alguien observó, con si tenía mensajes nuevos o no.
        # El silencio queda como dato: un tick sin mensajes es una entrada.
        self._clock_log: List[dict] = []
        self._ultimo_tick_visto: int = -1

    @staticmethod
    def _ahora() -> float:
        """
        El reloj del canal. Una sola fuente (decisión 1).

        Es el mismo que sella los mensajes: `datetime.now(timezone.utc)`, y de
        ahí sale tanto el ISO del mensaje como el epoch del que se deriva el
        tick. No es `time.time()` ni `time.monotonic()` — esos son otros
        relojes, y mezclarlos es lo que el CP0 encontró pasando en
        `autonomous_device.py`.
        """
        return datetime.now(timezone.utc).timestamp()

    def tick(self) -> int:
        """
        El tick vigente: cuántos períodos pasaron desde que el canal existe.

        **Se deriva del reloj, no se incrementa.** Por eso avanza aunque nadie
        publique y aunque nadie pregunte: no hay un contador que dependa de que
        alguien lo mueva. Monótono no decreciente mientras el reloj no retroceda.
        """
        return int((self._ahora() - self._t0) // TICK_PERIODO_S)

    def get_clock(self) -> dict:
        """
        El tick vigente y de qué reloj viene (decisiones 1 y 3).

        **Registra el tick observado, con o sin mensajes.** Un tick sin mensajes
        nuevos queda como entrada en el log: eso es el silencio como dato. Si se
        pregunta dos veces dentro del mismo tick, se registra una sola vez — el
        log es de ticks, no de consultas.

        No calcula nada por el device: no dice "cuántos ticks sin mensajes" ni
        "quién habló último". Da el tick y su reloj; evaluar los Δt es del
        device (fase D).
        """
        t = self.tick()
        ahora = self._ahora()
        if t != self._ultimo_tick_visto:
            ultimo_msg = (
                datetime.fromisoformat(self.messages[-1].timestamp).timestamp()
                if self.messages else None
            )
            self._clock_log.append({
                "tick": t,
                "t": ahora,
                "reloj": RELOJ_CANAL,
                "n_mensajes": len(self.messages),
                # True si el último mensaje del canal cae dentro de este tick.
                # False es el silencio, y queda registrado igual.
                "con_mensajes": bool(
                    ultimo_msg is not None
                    and int((ultimo_msg - self._t0) // TICK_PERIODO_S) == t
                ),
            })
            self._ultimo_tick_visto = t
        return {
            "tick": t,
            "t": ahora,
            "reloj": RELOJ_CANAL,
            "periodo_s": TICK_PERIODO_S,
            "t0": self._t0,
        }

    def clock_log(self) -> List[dict]:
        """Los ticks observados, con y sin mensajes. Copia: no se edita."""
        return list(self._clock_log)

    def clock_log_desde(self, desde_tick: int | None = None) -> dict:
        """
        El log de ticks, **con su total aparte**, para leerlo desde afuera (F2).

        Hasta el fix, `clock_log()` sólo se podía llamar desde dentro del
        proceso del server: los dos vivos lo reportaron como no verificable.
        Ahora lo exponen una tool MCP y un endpoint, y los dos pasan por acá.

        **No reemplaza a `clock_log()`**, que sigue devolviendo la lista: el
        fix era aditivo, y cambiarle la firma rompía a sus llamadores — me pasó
        al escribirlo, y cuatro tests lo dijeron.

        `desde_tick` filtra desde ese tick inclusive. **El total va aparte**,
        así que paginar no pierde la cuenta: el log crece de a uno por tick
        observado y un run largo lo vuelve grande.
        """
        entradas = list(self._clock_log)
        total = len(entradas)
        if desde_tick is not None:
            entradas = [e for e in entradas if e["tick"] >= desde_tick]
        return {
            "total": total,
            "devueltas": len(entradas),
            "desde_tick": desde_tick,
            "periodo_s": TICK_PERIODO_S,
            "reloj": RELOJ_CANAL,
            "entradas": entradas,
        }

    async def publish(self, device_id: str, device_type: str, text: str) -> Message:
        ahora = self._ahora()
        message = Message(
            device_id=device_id,
            device_type=device_type,
            text=text,
            timestamp=datetime.fromtimestamp(ahora, timezone.utc).isoformat(),
            tick=int((ahora - self._t0) // TICK_PERIODO_S),
            reloj=RELOJ_CANAL,
        )
        self.messages.append(message)

        payload = json.dumps(message.to_dict())
        stale: List[WebSocket] = []
        for ws in self._subscribers:
            try:
                await ws.send_text(payload)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.unsubscribe(ws)

        for callback in self._on_message_callbacks:
            callback(message)

        return message

    async def publish_system_event(self, text: str) -> Message:
        """Emite un mensaje operacional (device_type=SYSTEM), p.ej. join events."""
        return await self.publish(device_id="system", device_type="SYSTEM", text=text)

    def subscribe(self, ws: WebSocket) -> None:
        self._subscribers.append(ws)

    def unsubscribe(self, ws: WebSocket) -> None:
        if ws in self._subscribers:
            self._subscribers.remove(ws)

    def add_callback(self, fn: Callable[[Message], None]) -> None:
        self._on_message_callbacks.append(fn)

    def get_history(self) -> List[Message]:
        return list(self.messages)
