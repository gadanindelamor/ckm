from __future__ import annotations

import os
from typing import List

from groq import AsyncGroq

from .base import ChatMessage, Provider


class GroqProvider(Provider):
    name = "groq"

    def __init__(self, api_key: str | None = None, model: str = "llama-3.3-70b-versatile"):
        super().__init__(api_key=api_key or os.getenv("GROQ_API_KEY"), model=model)
        self._client = AsyncGroq(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""
