"""
test_generacion_vacia.py — el fix del hallazgo del vivo 03

En el vivo 03 un device decidió INTERACT, el provider devolvió `""`, y **se
publicó un mensaje vacío que entró al corpus** (`corpus_size = 2`, uno de los
dos textos era de largo 0). `_interact` chequeaba `if text is None`, y un vacío
no es `None`: la guarda miraba el **marcador de ausencia** y no el **valor
vacío**.

delamor: *"corregirlo"*. Alcance definido por Opus: una generación vacía o sólo
espacios **no se publica**; se registra con `causa: "generacion_vacia"` y la
respuesta cruda. Test + inversión.

**Y lo que NO se toca:** el otro texto del vivo 03 era `'[assistant]'`. Filtrar
contenido sería interpretar (**Opus**, `1535ff9`), así que sigue publicándose y
hay un test que lo afirma — para que no se "arregle" después sin decidirlo.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom.autonomous_device import AutonomousDevice      # noqa: E402
from iap_chatroom.channel import ChatChannel                     # noqa: E402

from tests.test_oda_continuo import ClientStub, ProviderStub


@pytest.fixture
def canal(monkeypatch):
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


def _device(provider, **kw) -> AutonomousDevice:
    return AutonomousDevice(device_id=kw.pop("device_id", "dev"),
                            provider=provider,
                            system_prompt="stub",
                            poll_interval=0.0, **kw)


def _una_vuelta(canal, generacion, device_id="dev"):
    """
    Ejercita la fase A con decisión INTERACT ya tomada.

    `_interact` se llama **directo**, así que `_decide` no corre y la primera
    respuesta del stub va a `_generate`: el stub lleva **sólo la generación**.
    Mi primera versión le pasaba dos y la de D terminaba publicada como texto
    — el test decía "se publica el texto" y publicaba la palabra del gate.
    """
    prov = ProviderStub([generacion])
    dev = _device(prov, device_id=device_id)
    client = ClientStub(canal, dev.device_id)

    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    mod.Client = lambda url: client
    try:
        asyncio.run(client.call_tool(
            "join_channel", {"device_id": dev.device_id, "device_type": "AI"}))
        asyncio.run(dev._interact(client, "INTERACT", {"field": None}))
    finally:
        mod.Client = orig
    return dev, [m for m in canal.messages if m.device_id == dev.device_id]


# ── el fix ──────────────────────────────────────────────────────────────────

def test_una_generacion_vacia_no_se_publica(canal) -> None:
    """**El hallazgo del vivo 03**, con el string exacto que se publicó: `''`."""
    dev, publicados = _una_vuelta(canal, "")
    assert not publicados, "se publicó un mensaje vacío"


@pytest.mark.parametrize("vacia", ["", " ", "   ", "\n", "\t\n ", " "])
def test_tambien_la_que_es_solo_espacios(canal, vacia) -> None:
    """
    Opus fijó el alcance en *"vacía o sólo espacios"*. `not text.strip()` cubre
    los dos, incluido el espacio duro `\\u00a0`, que no se ve al leer el log.
    """
    dev, publicados = _una_vuelta(canal, vacia)
    assert not publicados, f"se publicó {vacia!r}"


def test_queda_registrada_con_su_causa_y_su_cruda(canal) -> None:
    """
    No alcanza con no publicar: si no queda registro, un INTERACT sin texto se
    vuelve indistinguible de un INTERACT que publicó. Es el mismo criterio que
    separó `OP_SILENCE` de `UNKNOWN` de `SKIP`.
    """
    dev, _ = _una_vuelta(canal, "   ")
    vacias = [x for x in dev._ilegibles if x["causa"] == "generacion_vacia"]
    assert len(vacias) == 1
    r = vacias[0]
    assert r["respuesta_cruda"] == "   "      # la cruda, sin strip
    assert r["largo"] == 3
    assert r["fase"] == "generate"
    assert dev.costo()["ilegibles_por_causa"]["generacion_vacia"] == 1


def test_se_registra_como_INTERACT_SIN_TEXTO(canal, capsys) -> None:
    """La decisión fue INTERACT y no hubo qué publicar: eso es lo que se loguea."""
    _una_vuelta(canal, "")
    assert "INTERACT_SIN_TEXTO" in capsys.readouterr().out


# ── las dos causas de un vacío, que se veían iguales ────────────────────────

def test_distingue_el_vacio_del_provider_del_que_dejo_el_strip(canal) -> None:
    """
    Un vacío tiene **dos orígenes distintos** y el registro los separa:

    - el provider devolvió vacío;
    - el provider devolvió algo y `_strip_own_prefix` lo dejó en nada — un
      mensaje que era sólo el prefijo de identidad del propio device.

    El segundo es de la familia del leak de prefijo del Caso 0.14
    (`[TinkerBellucio]:` dentro del mensaje de Mark). Sin esta distinción, el
    log diría "generación vacía" en los dos y el stripper quedaría invisible.
    """
    dev, pub = _una_vuelta(canal, "", device_id="d1")
    r = [x for x in dev._ilegibles if x["causa"] == "generacion_vacia"][0]
    assert r["vacia_antes_de_strip"] is True
    assert r["la_vacio_el_strip"] is False

    # ahora uno que el strip vacía: el texto es sólo el prefijo del device
    canal.messages.clear()
    dev2, pub2 = _una_vuelta(canal, "[d2]: ", device_id="d2")
    assert not pub2, "publicó un mensaje que era sólo su propio prefijo"
    r2 = [x for x in dev2._ilegibles if x["causa"] == "generacion_vacia"][0]
    assert r2["respuesta_cruda"] == "[d2]: ", "se perdió la cruda de antes del strip"
    assert r2["vacia_antes_de_strip"] is False
    assert r2["la_vacio_el_strip"] is True, \
        "no se registró que el stripper fue lo que lo vació"


# ── la palabra del protocolo como mensaje (21 oct 2026) ─────────────────────
#
# Medido con el prompt real del generate, una llamada por modelo:
# `qwen/qwen3.8-27b` devolvió `OP_SILENCE`. No está vacío, así que el canal lo
# habría publicado y habría entrado al corpus como un texto. Opus (`1cc11dc`):
# no se publica, y se registra como OP_SILENCE con `fase: generate` — el device
# eligió callar, que no es un provider que falló.

@pytest.mark.parametrize("palabra", [
    "OP_SILENCE", "INTERACT", "LEAVE",
    "op_silence", " OP_SILENCE ", "Leave\n",
])
def test_una_palabra_del_protocolo_no_se_publica(canal, palabra) -> None:
    """
    Las tres palabras, y sin distinguir mayúsculas ni espacios de los bordes:
    la comparación es sobre el texto **entero** después del `strip()`.
    """
    dev, publicados = _una_vuelta(canal, palabra)
    assert not publicados, f"se publicó {palabra!r}"
    assert dev._silencio_en_generate is not None
    assert dev._silencio_en_generate["word"] == palabra.strip().upper()
    assert dev._silencio_en_generate["respuesta_cruda"] == palabra  # sin strip
    assert dev._silencio_en_generate["fase"] == "generate"


def test_se_registra_como_OP_SILENCE_y_no_como_INTERACT_SIN_TEXTO(canal, capsys) -> None:
    """
    **La diferencia es el punto.** Un provider que falla y un device que
    contesta `OP_SILENCE` dejan los dos un INTERACT sin publicar, y son dos
    cosas distintas: la primera es infraestructura, la segunda es una decisión
    del modelo. Si las dos se loguearan igual, el vivo no se podría atribuir.
    """
    out = capsys.readouterr      # se consume después de cada vuelta
    _una_vuelta(canal, "OP_SILENCE")
    salida = out().out
    assert "OP_SILENCE" in salida
    assert "INTERACT_SIN_TEXTO" not in salida

    _una_vuelta(canal, "", device_id="dev2")
    salida = out().out
    assert "INTERACT_SIN_TEXTO" in salida


def test_el_action_result_dice_en_que_fase_fue_el_silencio(canal) -> None:
    """
    El `action_result` de la vuelta, que es lo que lee la traza: el silencio
    del generate **no** se confunde con el que decidió el gate.
    """
    prov = ProviderStub(["OP_SILENCE"])
    dev = _device(prov)
    client = ClientStub(canal, dev.device_id)
    asyncio.run(client.call_tool(
        "join_channel", {"device_id": dev.device_id, "device_type": "AI"}))
    r = asyncio.run(dev._interact(client, "INTERACT", {"field": None}))
    assert r["result"] == "no_action: op_silence in generate"
    assert r["tick_action"] is None


def test_la_linea_queda_escrita_en_el_state_dir(canal, tmp_path) -> None:
    """
    Y queda **en disco**, con el mismo mecanismo que todo lo demás del punto 3:
    un registro que no se escribe es indistinguible de uno que no ocurrió.
    """
    from iap_chatroom import run_store

    d = tmp_path / "_state"
    run_store.set_state_dir(d)
    prov = ProviderStub(["OP_SILENCE"])
    dev = _device(prov)
    dev._state_dir = d
    client = ClientStub(canal, dev.device_id)
    asyncio.run(client.call_tool(
        "join_channel", {"device_id": dev.device_id, "device_type": "AI"}))
    asyncio.run(dev._interact(client, "INTERACT", {"field": None}))

    lineas = [ln for ln in run_store.read(run_store.DEVICE_LOG, d)
              if ln["event"] == "op_silence_in_generate"]
    assert len(lineas) == 1, lineas
    assert lineas[0]["word"] == "OP_SILENCE"
    assert lineas[0]["causa"] == "protocol_word_as_message"


def test_un_mensaje_que_EMPIEZA_con_una_palabra_del_protocolo_se_publica(canal) -> None:
    """
    **La comparación es sobre el texto entero, a propósito.** El gate mira la
    primera palabra (`split()[0]`); acá eso descartaría un mensaje de verdad
    que arranca nombrando el protocolo, que es justo de lo que estos devices
    hablan entre ellos.
    """
    texto = "OP_SILENCE is not what I would choose here: the aquifer needs a decision."
    dev, publicados = _una_vuelta(canal, texto)
    assert len(publicados) == 1
    assert publicados[0].text == texto
    assert dev._silencio_en_generate is None


def test_el_pedido_va_al_final_del_prompt_del_generate(canal) -> None:
    """
    El pedido (`PEDIDO_GENERATE`) es **lo único del prompt del generate que no
    viene del canal**, y va **al final**. Sin él, el prompt era el system
    prompt más el historial: ninguna línea pedía escribir, y con el prompt real
    `qwen` devolvió `OP_SILENCE`.

    Y **sin prefijo de identidad**: si `_coalesce` lo junta con el último
    mensaje del canal, se sigue distinguiendo de él.
    """
    from iap_chatroom.autonomous_device import PEDIDO_GENERATE

    dev = _device(ProviderStub([]))
    dev._history = [
        {"device_id": "otro", "text": "the source is the constraint"},
    ]
    messages = dev._to_chat_messages()
    assert messages[-1]["content"].endswith(PEDIDO_GENERATE)
    assert not PEDIDO_GENERATE.startswith("[")
    assert f"[{dev.device_id}]" not in PEDIDO_GENERATE
    # y está en inglés, como todo lo que llega al modelo
    sys.path.insert(0, str(RAIZ / "tests"))
    from test_prompt_solo_ingles import castellano
    assert castellano(PEDIDO_GENERATE) == []


def test_sin_el_pedido_el_prompt_no_pide_nada(canal) -> None:
    """
    La inversión, para que el test anterior no sea decorado: sin
    `PEDIDO_GENERATE` el prompt del generate no contiene ninguna forma de
    pedido — que es el estado en el que se midió el `OP_SILENCE` de `qwen`.
    """
    import iap_chatroom.autonomous_device as mod

    dev = _device(ProviderStub([]))
    dev._history = [{"device_id": "otro", "text": "the source is the constraint"}]
    anterior = mod.PEDIDO_GENERATE
    mod.PEDIDO_GENERATE = ""
    try:
        sin_pedido = " ".join(m["content"] for m in dev._to_chat_messages())
    finally:
        mod.PEDIDO_GENERATE = anterior
    assert "write your message" not in sin_pedido.lower()
    con_pedido = " ".join(m["content"] for m in dev._to_chat_messages())
    assert "write your message" in con_pedido.lower()


# ── lo que NO se toca ───────────────────────────────────────────────────────

def test_assistant_SIGUE_publicandose(canal) -> None:
    """
    **No se toca `[assistant]`** (**Opus**, `1535ff9`). Era el otro texto del
    vivo 03 y filtrarlo sería interpretar el contenido: nadie decidió que
    `[assistant]` no sea un mensaje.

    Lo que dijo delamor fue *"corregirlo"*, y era sobre el **mensaje vacío**.
    Atribuí a delamor la frase sobre no filtrar, que es de Opus: tercera vez hoy
    que una atribución se me corre, y las tres en el mismo sentido — hacia
    delamor.

    Este test existe para que no se "arregle" de paso. Si algún día se decide
    filtrarlo, **este test tiene que fallar primero** y alguien tiene que venir
    a leer esto.
    """
    dev, publicados = _una_vuelta(canal, "[assistant]")
    assert len(publicados) == 1
    assert publicados[0].text == "[assistant]"
    assert not [x for x in dev._ilegibles if x["causa"] == "generacion_vacia"]


def test_un_texto_de_verdad_se_publica_igual(canal) -> None:
    """Que el fix no se coma lo que sí tiene contenido."""
    dev, publicados = _una_vuelta(canal, "hola, estoy acá")
    assert len(publicados) == 1
    assert publicados[0].text == "hola, estoy acá"
    assert dev.costo()["ilegibles"] == 0


def test_las_dos_causas_no_se_mezclan_en_el_contador(canal) -> None:
    """
    `ilegibles` juntaría una respuesta del gate ilegible con una generación
    vacía, y son dos cosas: la primera es el modelo contestando fuera del
    vocabulario, la segunda es el modelo no diciendo nada.
    """
    # dos respuestas y no tres: la primera la consume `_decide`, la segunda
    # `_generate`. Con una tercera en medio se publicaba la palabra del gate.
    prov = ProviderStub(["esto no es una palabra del gate", ""])
    dev = _device(prov)
    client = ClientStub(canal, dev.device_id)

    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    mod.Client = lambda url: client
    try:
        asyncio.run(client.call_tool(
            "join_channel", {"device_id": dev.device_id, "device_type": "AI"}))
        # `field` tiene que ser un dict: `_decide` lee D_ckm de ahí. Con None
        # rompe, y romper no es lo que este test mide.
        d = asyncio.run(dev._decide({"field": {}, "history": [], "clock": {},
                                     "tick_anterior": -1, "trigger": None,
                                     "own_recent": [], "n_nuevos": 0}))
        assert d == "UNKNOWN"
        asyncio.run(dev._interact(client, "INTERACT", {"field": None}))
    finally:
        mod.Client = orig

    por_causa = dev.costo()["ilegibles_por_causa"]
    assert por_causa["respuesta_ilegible"] == 1
    assert por_causa["generacion_vacia"] == 1
    assert dev.costo()["ilegibles"] == 2
