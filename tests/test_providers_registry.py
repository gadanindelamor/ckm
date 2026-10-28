"""
test_providers_registry.py — el registro de providers que declara IAP

**P14 punto 3** (delamor, 27 oct 2026: *"un driver de test lo sabe. hay que
llevar ese knowhow a IAP"*), texto para Code 16, punto 1.

Lo que fija: el registro tiene **los cuatro** providers, cada nombre construye
**su** clase, y un nombre que no existe falla **diciendo cuáles hay**. Más una
cosa que no estaba pedida y es la que evita que el hueco vuelva: que el nombre
**no esté escrito dos veces** — el registro se arma desde el `name` de cada
clase, así que no hay un segundo lugar donde pueda divergir.

Sin red y sin claves: los providers se construyen con una `api_key` de prueba,
que es lo único que sus `__init__` necesitan (arman el cliente del SDK y no
llaman a nada).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from iap_chatroom.providers import (                                  # noqa: E402
    PROVIDER_CLASSES,
    PROVIDERS,
    AnthropicProvider,
    GeminiProvider,
    GroqProvider,
    OpenAIProvider,
    Provider,
    UnknownProvider,
    build_provider,
    provider_class,
    provider_names,
)

LOS_CUATRO = {
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "groq": GroqProvider,
    "openai": OpenAIProvider,
}


def test_el_registro_tiene_los_cuatro() -> None:
    """Los cuatro que hay en `iap_chatroom/providers/`, ni uno menos."""
    assert provider_names() == ("anthropic", "gemini", "groq", "openai")
    assert set(PROVIDERS) == set(LOS_CUATRO)


@pytest.mark.parametrize("nombre,clase", sorted(LOS_CUATRO.items()))
def test_cada_nombre_da_su_clase(nombre, clase) -> None:
    assert provider_class(nombre) is clase


@pytest.mark.parametrize("nombre,clase", sorted(LOS_CUATRO.items()))
def test_cada_nombre_construye_su_clase(nombre, clase) -> None:
    """
    `build_provider` devuelve una instancia de la clase, con el modelo que se
    le declara. El modelo es del caso, no del registro (inventario de
    defaults §6).
    """
    p = build_provider(nombre, model="un-modelo", api_key="clave-de-prueba")
    assert isinstance(p, clase)
    assert isinstance(p, Provider)
    assert p.model == "un-modelo"


def test_sin_modelo_queda_el_default_de_la_clase() -> None:
    """
    `model=None` **no** pisa el default de la clase con un `None`: lo deja.
    Es la diferencia entre "no declaré modelo" y "declaré ninguno".
    """
    por_el_registro = build_provider("groq", api_key="clave-de-prueba")
    directo = GroqProvider(api_key="clave-de-prueba")
    assert por_el_registro.model is not None
    assert por_el_registro.model == directo.model, \
        "pedir el provider por el registro no da lo mismo que construirlo"


def test_un_nombre_que_no_existe_dice_cuales_hay() -> None:
    """
    El dato que falta en ese momento es la lista. Un `KeyError` pelado la deja
    afuera; `UnknownProvider` la trae en el mensaje.
    """
    with pytest.raises(UnknownProvider) as exc:
        provider_class("llama")
    mensaje = str(exc.value)
    assert "llama" in mensaje
    for nombre in LOS_CUATRO:
        assert nombre in mensaje, f"el mensaje no nombra a {nombre}"

    # y por el mismo camino cuando se pide construir
    with pytest.raises(UnknownProvider):
        build_provider("llama", api_key="clave-de-prueba")


def test_el_nombre_no_esta_escrito_dos_veces() -> None:
    """
    **Lo que evita que el hueco vuelva.** El registro no repite el nombre: lo
    toma del `name` de cada clase. Si alguien agrega un provider y se olvida
    del registro, o escribe el nombre distinto en los dos lugares, esto falla.
    """
    for clase in PROVIDER_CLASSES:
        assert PROVIDERS[clase.name] is clase
    assert len(PROVIDERS) == len(PROVIDER_CLASSES), \
        "dos clases declaran el mismo `name` y una tapó a la otra"
    # el registro cubre **todas** las subclases importables de Provider
    importadas = {c for c in (AnthropicProvider, GeminiProvider, GroqProvider,
                              OpenAIProvider)}
    assert set(PROVIDER_CLASSES) == importadas


def test_importar_el_registro_no_construye_nada(monkeypatch) -> None:
    """
    Importarlo no toca una clave ni arma un cliente: lo que el registro tiene
    son **clases**. Se verifica borrando las variables de entorno y volviendo
    a importarlo.
    """
    import importlib

    for var in ("GROQ_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY",
                "OPENAI_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    mod = importlib.import_module("iap_chatroom.providers.registry")
    importlib.reload(mod)
    assert mod.provider_names() == ("anthropic", "gemini", "groq", "openai")
