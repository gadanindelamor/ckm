from __future__ import annotations

import os
from typing import List

from google import genai

from .base import ChatMessage, Provider


class GeminiProvider(Provider):
    name = "gemini"

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.0-flash"):
        super().__init__(api_key=api_key or os.getenv("GOOGLE_API_KEY"), model=model)
        self._client = genai.Client(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        contents = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        response = await self._client.aio.models.generate_content(
            model=self.model,
            contents=contents,
        )
        return response.text or ""
