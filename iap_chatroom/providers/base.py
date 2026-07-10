"""
base.py — Provider

Interfaz comun para los wrappers de proveedores LLM usados como AI devices
en la chatroom. No existia iap/providers/ en el repo para copiar, asi que
esta interfaz y sus implementaciones son minimas y se escriben desde cero.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypedDict


class ChatMessage(TypedDict):
    role: str  # "user" | "assistant" | "system"
    content: str


class Provider(ABC):
    name: str = "base"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def complete(self, messages: List[ChatMessage]) -> str:
        """Devuelve la respuesta de texto del modelo dado un historial de mensajes."""
        raise NotImplementedError
