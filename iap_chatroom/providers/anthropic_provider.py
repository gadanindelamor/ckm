from __future__ import annotations

import os
from typing import List

from anthropic import AsyncAnthropic

from .base import ChatMessage, Provider


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-5"):
        super().__init__(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"), model=model)
        self._client = AsyncAnthropic(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        system = "\n".join(m["content"] for m in messages if m["role"] == "system") or None
        turns = [m for m in messages if m["role"] != "system"]
        response = await self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system,
            messages=turns,
        )
        return "".join(block.text for block in response.content if block.type == "text")
