from __future__ import annotations

import os
from typing import List

from groq import AsyncGroq

from .base import ChatMessage, Provider

# **El techo de la generación, declarado como sesgo del intento 2 de
# `serie2_caso0`** (delamor, 21 oct 2026), con su objetivo: volumen, para que
# nazca el primer W. Baja de 4096, que es lo que dejó el fix de los
# `max_tokens` (`8789a9d` y los dos commits de providers), a 512.
#
# **De dónde sale el número, medido en el intento 1**
# (`registers/REG_iap_serie2_caso0_intento1_v1.md` §3):
#
# - **El techo que corrige.** `qwen/qwen3.8-27b` devolvió un `429` por
#   **OTPM** (*output* tokens per minute): `Limit 1000, Requested 1246`, con
#   el provider diciendo *"reduce max_tokens"*. Con 4096, **una sola llamada
#   no cabe en el presupuesto de salida del minuto entero**. 512 sí: ninguna
#   llamada puede, por sí sola, pasarse del OTPM.
# - **Lo que NO corrige, y hay que decirlo.** Los **61 `413`** del intento 1
#   son de **entrada**: `TPM Limit 8000` con Requested mediana **14326** en
#   los dos `gpt-oss`, e `ITPM Limit 7000` con mediana **13137** en qwen.
#   Bajar 4096 → 512 resta 3584 del lado de la salida; el que falta es el
#   historial que entra. Eso lo corrigen la ventana del gate (10 → 4) y el
#   pedido de mensajes cortos de la consigna, **no este número**.
# - **El OTPM es por minuto, no por llamada.** Con `Limit 1000`, 512 deja
#   caber **dos** llamadas por minuto en qwen, y después el minuto se agota.
#   **Ningún valor de `max_tokens` hace desaparecer ese techo**: lo que acota
#   es cuántas llamadas con generación entran en un minuto.
# - **El margen contra el truncamiento.** La consigna del intento 2 pide
#   *"around 80 words or fewer"* ≈ **110 tokens**: 512 es 4,7× eso, así que
#   hay lugar para un preámbulo de razonamiento y para un device que **no**
#   respete el pedido. El chequeo de truncamiento queda como está y avisa si
#   igual se corta — que es el defecto que el fix de los `max_tokens` cerró y
#   que este sesgo **no** reabre en silencio.
#
# El de Gemini **no se toca** (`gemini_provider.MAX_OUTPUT_TOKENS = 4096`):
# los seis errores de ese device fueron cuota del plan y un 503, ninguno de
# techo de salida, y `gemini-2.5-flash` cuenta los tokens de *thinking*
# adentro de `max_output_tokens` — bajarlo devuelve texto vacío. El de
# Anthropic tampoco: no corre en este caso.
MAX_TOKENS = 512


class GroqProvider(Provider):
    name = "groq"

    def __init__(self, api_key: str | None = None, model: str = "llama-3.3-70b-versatile"):
        super().__init__(api_key=api_key or os.getenv("GROQ_API_KEY"), model=model)
        self._client = AsyncGroq(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=MAX_TOKENS,
        )
        choice = response.choices[0]
        if choice.finish_reason == "length":
            print(
                f"[GroqProvider WARNING] response truncated at "
                f"max_tokens={MAX_TOKENS} (model={self.model}) — "
                f"raise max_tokens if this recurs"
            )
        return choice.message.content or ""
