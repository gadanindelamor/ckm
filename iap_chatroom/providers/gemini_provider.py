from __future__ import annotations

import os
from typing import List

from google import genai

from .base import ChatMessage, Provider

# El default. **`gemini-2.0-flash` ya no existe**: medido el 20 oct 2026 contra
# la clave de este repo, devuelve `404 NOT_FOUND ... is no longer available`.
# Un default que no responde hace que `GeminiProvider()` sin argumentos falle
# con un 404 que se lee como un problema de clave y no de modelo.
MODELO_POR_DEFAULT = "gemini-2.5-flash"

# El techo de la generación. **Declarado y al lado del chequeo de
# truncamiento**, como en `groq_provider` y `anthropic_provider`: los dos lo
# tienen desde el fix de los `max_tokens`, y acá faltaba.
MAX_OUTPUT_TOKENS = 4096


class GeminiProvider(Provider):
    """
    Wrapper de Gemini.

    **Dos cosas declaradas, porque este provider no se comporta como los otros
    dos y en `serie2_caso0` uno de los cuatro devices es Gemini:**

    1. **Aplana los roles.** `generate_content` recibe un solo string, así que
       el system prompt y los turnos se concatenan con su rol como prefijo
       (`system: ...`, `user: ...`). Groq y Anthropic reciben la lista de
       mensajes con el system aparte. Es una asimetría real del instrumento
       entre el device B y los otros tres, y **queda declarada sin
       corregirse**: cambiarla cambia la estructura del prompt que un device
       lee, y eso es del modelo.
    2. **El truncamiento se mira.** Faltaba: el fix de los `max_tokens`
       (`anthropic_provider`, `groq_provider`) agregó el chequeo en los otros
       dos porque una respuesta cortada en la mitad **se leía como una
       respuesta corta**, y retroactivamente afectó a los Casos 0.9 y 0.10.
       Acá no había ni techo declarado ni chequeo, así que el mismo defecto
       seguía abierto en este camino. Ahora el techo está declarado y un corte
       avisa, con la misma forma que los otros dos.
    """

    name = "gemini"

    def __init__(self, api_key: str | None = None,
                 model: str = MODELO_POR_DEFAULT):
        super().__init__(api_key=api_key or os.getenv("GOOGLE_API_KEY"), model=model)
        self._client = genai.Client(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        contents = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        response = await self._client.aio.models.generate_content(
            model=self.model,
            contents=contents,
            config={"max_output_tokens": MAX_OUTPUT_TOKENS},
        )
        # `finish_reason` vive en el candidato, y puede no haber candidatos (un
        # bloqueo del prompt los deja en None). **Ausencia es ausencia**: no se
        # rellena con "STOP", que diría que terminó bien.
        candidatos = getattr(response, "candidates", None) or []
        motivo = getattr(candidatos[0], "finish_reason", None) if candidatos else None
        if motivo is not None and getattr(motivo, "name", str(motivo)) == "MAX_TOKENS":
            print(
                f"[GeminiProvider WARNING] response truncated at "
                f"max_output_tokens={MAX_OUTPUT_TOKENS} (model={self.model}) — "
                f"raise max_output_tokens if this recurs"
            )
        return response.text or ""
