from __future__ import annotations

import os
from typing import List

from openai import AsyncOpenAI

from .base import ChatMessage, Provider


class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        super().__init__(api_key=api_key or os.getenv("OPENAI_API_KEY"), model=model)
        self._client = AsyncOpenAI(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""
