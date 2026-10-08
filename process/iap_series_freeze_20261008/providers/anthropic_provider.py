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
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": turns}
        if system is not None:
            kwargs["system"] = system
        response = await self._client.messages.create(**kwargs)
        if response.stop_reason == "max_tokens":
            print(
                f"[AnthropicProvider WARNING] response truncated at "
                f"max_tokens={kwargs['max_tokens']} (model={self.model}) — "
                f"raise max_tokens if this recurs"
            )
        return "".join(block.text for block in response.content if block.type == "text")
