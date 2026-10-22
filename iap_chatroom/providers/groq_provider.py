from __future__ import annotations

import os
from typing import List

from groq import AsyncGroq

from .base import ChatMessage, Provider

# ── El techo de salida y el razonamiento, POR MODELO ───────────────────────
#
# **Sesgo declarado del intento 3 de `serie2_caso0`** (22 oct 2026), con el
# mismo objetivo que el resto: **volumen, sin que el instrumento pierda
# respuestas**. Lo decide la medición, no `n = 1`.
#
# ### Qué se midió: 60 llamadas, 5 por modelo, por fase y por condición
#
# Con los prompts del vivo —system prompt del caso y la ventana de 10 mensajes
# **reales del intento 2**, armados por el código del device— y con el techo de
# la medición alto a propósito, para ver **cuánto gasta cada modelo cuando no
# lo cortan**. Las dos fases, porque los 17 vacíos del intento 2 fueron
# **mayoría en el gate** (14 de 17), y el gate contesta **una palabra**.
#
# **Sin `reasoning_effort`** (lo que corrió en el intento 2):
#
# | modelo | fase | completion min/mediana/máx | razonamiento máx |
# |---|---|---|---|
# | `gpt-oss-120b` | `decide` | 87 / 124 / 171 | 158 |
# | `gpt-oss-120b` | `generate` | 154 / 202 / 213 | 112 |
# | `gpt-oss-20b` | `decide` | 139 / 253 / **999** | **988** |
# | `gpt-oss-20b` | `generate` | 187 / 243 / 312 | 200 |
# | `qwen3.8-27b` | `decide` | 3 / 6 / 6 | no lo informa |
# | `qwen3.8-27b` | `generate` | 60 / 92 / 102 | no lo informa |
#
# **El hallazgo es la cola de `gpt-oss-20b` en el gate: 999 tokens, 988 de
# razonamiento, para contestar una palabra.** Una de cinco llamadas. Con el
# techo plano en 512 esa llamada vuelve **vacía**, y es el mecanismo de los
# **17 vacíos** del intento 2 (14 en `decide`, 3 en `generate`, los 17 con
# `largo: 0`, todos de ese modelo). No era el modelo: era el techo contra la
# cola del razonamiento.
#
# **Con `reasoning_effort="low"`** (delamor, 22 oct: *"acá no sería relevante
# el uso de razonamiento"*):
#
# | modelo | fase | completion min/mediana/máx | razonamiento máx |
# |---|---|---|---|
# | `gpt-oss-120b` | `decide` | 21 / 38 / 54 | 41 |
# | `gpt-oss-120b` | `generate` | 93 / 121 / 125 | 20 |
# | `gpt-oss-20b` | `decide` | 21 / 26 / **78** | 35 |
# | `gpt-oss-20b` | `generate` | 109 / 119 / **128** | 23 |
# | `qwen3.8-27b` | `decide` | 291 / 346 / **416** | **408** |
# | `qwen3.8-27b` | `generate` | 532 / 737 / **849** | **755** |
#
# **La bandera no es portable, y eso es lo que decide la forma de esto.** En
# los dos `gpt-oss` **corta** el razonamiento y la cola de 999 desaparece: el
# máximo de las 20 llamadas es 128. En `qwen3.8` hace lo **contrario**: sin la
# bandera gasta 3–102 tokens y **no informa** razonamiento; con la bandera
# gasta 291–849 con 283–755 de razonamiento, y **dos de sus diez llamadas
# murieron con `429 OTPM Limit 1000`**. Pasar el mismo parámetro a los tres
# modelos rompería justo al que hoy no tiene problema.
#
# ### Los límites de la cuenta, leídos de los headers (no del texto de un error)
#
# `x-ratelimit-limit-tokens: 8000` y `x-ratelimit-limit-requests: 1000` en los
# **tres** modelos: el TPM es de 8000 y cuenta **entrada + salida**. El OTPM no
# viaja en los headers; de él sólo se sabe lo medido: `qwen` da
# `429 OTPM Limit 1000`, y `gpt-oss-20b` **produjo 999 tokens sin 429**, así
# que su OTPM admite al menos eso.
#
# ### Lo que queda fijado, y la expectativa escrita
#
# - **`gpt-oss-120b` y `gpt-oss-20b`: techo 512 y `reasoning_effort="low"`.**
#   512 es **4× el máximo medido bajo esa bandera** (128). El techo **no
#   cambia** respecto del intento 2: lo que cambia es que la cola que lo
#   desbordaba ya no existe. **Expectativa: 0 vacíos en `gpt-oss-20b`, y la
#   misma presión de TPM que el intento 2** —que tuvo **cero `413`**—, porque
#   el techo es el mismo. Subirlo a 1024 habría cerrado los vacíos **comprando
#   `413`**: prompt ≈ 1445 + 1024 = 2469 por llamada contra 8000 por minuto,
#   o sea ~3,2 llamadas por minuto contra las ~5 que ese device hizo.
# - **`qwen3.8-27b`: techo 256 y SIN la bandera.** Su máximo medido sin bandera
#   es 102 (2,5× de margen), y con 256 entran **3 llamadas por minuto** en su
#   OTPM de 1000 en vez de 1 (`1000 // 512 = 1`). Es el único modelo donde
#   bajar el techo compra llamadas.
#   *(Acá había escrito "4 en vez de 2": `1000 // 256 = 3`. Lo encontró el test
#   del techo en su primera corrida. Se corrige la cuenta, no el techo.)*
#
# El chequeo de truncamiento queda como está y nombra el techo que se usó. Si
# un modelo se corta igual, **avisa**: un corte visible y no un vacío que se
# lee como silencio.
MAX_TOKENS_POR_MODELO = {
    "openai/gpt-oss-120b": 512,
    "openai/gpt-oss-20b": 512,
    "qwen/qwen3.8-27b": 256,
}

# Para un modelo que no esté medido. **No es un promedio ni una apuesta**: es
# el valor del intento 2, que es el único que corrió un vivo entero. Un modelo
# nuevo se mide antes de nombrarlo en un caso.
MAX_TOKENS_POR_DEFAULT = 512

# **Sólo los modelos donde la bandera baja el gasto, medido.** Un modelo que no
# está acá **no la recibe**: en `qwen3.8` la bandera multiplica el gasto por 10
# y lo tira contra su OTPM. La ausencia es una decisión medida, no un olvido.
REASONING_EFFORT_POR_MODELO = {
    "openai/gpt-oss-120b": "low",
    "openai/gpt-oss-20b": "low",
}


def techo_de_salida(modelo: str | None) -> int:
    """El techo del modelo, o el default declarado si no está medido."""
    return MAX_TOKENS_POR_MODELO.get(modelo or "", MAX_TOKENS_POR_DEFAULT)


def esfuerzo_de_razonamiento(modelo: str | None) -> "str | None":
    """
    El `reasoning_effort` del modelo, o `None` si no se le pasa.

    `None` **no es un default**: es "a este modelo no se le manda la bandera",
    y la razón está medida arriba.
    """
    return REASONING_EFFORT_POR_MODELO.get(modelo or "")


class GroqProvider(Provider):
    name = "groq"

    def __init__(self, api_key: str | None = None, model: str = "llama-3.3-70b-versatile"):
        super().__init__(api_key=api_key or os.getenv("GROQ_API_KEY"), model=model)
        self._client = AsyncGroq(api_key=self.api_key)

    async def complete(self, messages: List[ChatMessage]) -> str:
        max_tokens = techo_de_salida(self.model)
        # La bandera **sólo si el modelo está en la tabla**: pasarla vacía o
        # con un default la mandaría a los que empeoran con ella.
        esfuerzo = esfuerzo_de_razonamiento(self.model)
        extra = {"reasoning_effort": esfuerzo} if esfuerzo else {}
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            **extra,
        )
        choice = response.choices[0]
        if choice.finish_reason == "length":
            print(
                f"[GroqProvider WARNING] response truncated at "
                f"max_tokens={max_tokens} (model={self.model}) — "
                f"raise max_tokens if this recurs"
            )
        return choice.message.content or ""
