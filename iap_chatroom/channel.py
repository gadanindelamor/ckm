"""
channel.py — ChatChannel

Canal de chat compartido entre devices (AI y HUMAN). Singleton: todos los
que llaman a ChatChannel() reciben la misma instancia y comparten el mismo
historial de mensajes y las mismas suscripciones WebSocket.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable, List, Literal

from fastapi import WebSocket


@dataclass
class Message:
    device_id: str
    device_type: Literal["AI", "HUMAN"]
    text: str
    timestamp: str  # ISO8601

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

    async def publish(self, device_id: str, device_type: str, text: str) -> Message:
        message = Message(
            device_id=device_id,
            device_type=device_type,
            text=text,
            timestamp=datetime.now(timezone.utc).isoformat(),
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

    def subscribe(self, ws: WebSocket) -> None:
        self._subscribers.append(ws)

    def unsubscribe(self, ws: WebSocket) -> None:
        if ws in self._subscribers:
            self._subscribers.remove(ws)

    def add_callback(self, fn: Callable[[Message], None]) -> None:
        self._on_message_callbacks.append(fn)

    def get_history(self) -> List[Message]:
        return list(self.messages)
