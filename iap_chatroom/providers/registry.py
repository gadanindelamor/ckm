"""
registry.py — el registro de providers, declarado por IAP

**P14 punto 3, decidido por delamor (27 oct 2026):** *"un driver de test lo
sabe. hay que llevar ese knowhow a IAP"*. Texto para Code 16, punto 1.

Qué hueco cierra. Hasta hoy `iap_chatroom/providers/` tenía las cuatro clases y
**ningún registro nombre → clase**: el único mapa del repo era
`_PROVIDERS = {"groq": …, "gemini": …}` dentro del driver del caso
(`iap_chatroom/tests/test_caso_serie2_caso0.py`), que cubría **2 de 4**. Un
driver sabía algo que IAP no declaraba, y cada driver nuevo lo volvía a
escribir —y podía escribirlo distinto.

**El nombre no se repite acá.** Cada clase ya declara el suyo (`Provider.name`:
`anthropic`, `gemini`, `groq`, `openai`), así que el registro se arma **desde
las clases** y no hay un segundo lugar donde el nombre pueda divergir. Si una
clase cambia su `name`, el registro cambia con ella.

**Qué NO hace:** no construye nada al importarse, no lee variables de entorno y
no sabe qué modelos existen en cada cuenta. Un nombre de modelo es del caso;
el nombre del provider es de IAP. Y el registro **no dice qué provider usar**:
sólo responde cuáles hay y cómo se construye cada uno.
"""

from __future__ import annotations

from typing import Mapping, Optional, Type

from .anthropic_provider import AnthropicProvider
from .base import Provider
from .gemini_provider import GeminiProvider
from .groq_provider import GroqProvider
from .openai_provider import OpenAIProvider

# Las clases que IAP conoce. El orden es alfabético y no significa prioridad.
PROVIDER_CLASSES: tuple[Type[Provider], ...] = (
    AnthropicProvider,
    GeminiProvider,
    GroqProvider,
    OpenAIProvider,
)

# nombre → clase, armado desde el `name` de cada clase.
PROVIDERS: Mapping[str, Type[Provider]] = {
    cls.name: cls for cls in PROVIDER_CLASSES
}


class UnknownProvider(ValueError):
    """
    El nombre pedido no está en el registro.

    Lleva los nombres que **sí** hay en el mensaje: un `KeyError` pelado deja a
    quien lo lee sin saber contra qué comparar, y la lista es exactamente el
    dato que falta en ese momento.
    """


def provider_names() -> tuple[str, ...]:
    """Los nombres registrados, ordenados. Es lo que un driver puede pedir."""
    return tuple(sorted(PROVIDERS))


def provider_class(name: str) -> Type[Provider]:
    """
    La clase de `name`. `UnknownProvider` si no está, **diciendo cuáles hay**.
    """
    try:
        return PROVIDERS[name]
    except KeyError:
        raise UnknownProvider(
            f"provider desconocido: {name!r}. "
            f"Registrados: {', '.join(provider_names())}"
        ) from None


def build_provider(name: str, *, model: Optional[str] = None,
                   api_key: Optional[str] = None) -> Provider:
    """
    Construye el provider de `name`.

    `model=None` deja el default de la clase, que **no es necesariamente el que
    corre** en un caso: el caso declara su modelo (inventario de defaults §6).
    `api_key=None` deja que la clase lea su variable de entorno, que es donde
    vive el secreto.
    """
    cls = provider_class(name)
    kw: dict = {}
    if model is not None:
        kw["model"] = model
    if api_key is not None:
        kw["api_key"] = api_key
    return cls(**kw)
