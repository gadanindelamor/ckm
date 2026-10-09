"""
test_oda_continuo.py — CP2a de TASK_canal_iap_clock_iniciativa_v2

El ODA continuo, **sin criterio local** (eso es el CP2b). Todo con stubs: no
hay llamadas a providers ni a la red. La corrida viva espera las claves.

Lo que se verifica es que **el diseño lo permita**, no que un modelo lo haga:
la TASK dice *"no se le exige que hable; se verifica que el diseño se lo
permite"*.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import List, Optional

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom.autonomous_device import AutonomousDevice      # noqa: E402
from iap_chatroom.channel import ChatChannel, TICK_PERIODO_S     # noqa: E402
from iap_chatroom.providers.base import ChatMessage, Provider    # noqa: E402


# ── stubs ───────────────────────────────────────────────────────────────────

class ProviderStub(Provider):
    """Devuelve respuestas de una lista. Sin red, sin claves."""

    name = "stub"

    def __init__(self, respuestas: List[str], falla_en: Optional[set] = None,
                 model: str = "stub"):
        super().__init__(api_key=None, model=model)
        self.respuestas = list(respuestas)
        self.llamadas: List[List[ChatMessage]] = []
        # índices de llamada (1-based) en los que simula una falla del provider
        self.falla_en = set(falla_en or ())

    async def complete(self, messages: List[ChatMessage]) -> str:
        """
        **Agotado devuelve vacío, no `OP_SILENCE`** (pedido de Opus, CP2v).

        Antes el default era `"OP_SILENCE"`, y eso **fabricaba decisiones**:
        una vuelta sin respuesta guionada producía un "el modelo decidió
        callar" que nadie decidió. Un instrumento de medición que inventa el
        dato más tranquilizador es el peor lugar donde tener este error.

        Vacío entra al camino de respuesta ilegible → `UNKNOWN`, que es lo que
        de verdad pasó: no hubo decisión. Varios tests cambiaron por esto, y
        el cambio **es el punto**: medían contra decisiones del instrumento.
        """
        self.llamadas.append(messages)
        if len(self.llamadas) in self.falla_en:
            raise RuntimeError("provider caido (simulado)")
        if not self.respuestas:
            return ""
        return self.respuestas.pop(0)


class ClientStub:
    """
    Stub del Client MCP contra un ChatChannel real.

    El canal es el de verdad —con su CLOCK, su reloj y su log—, así que lo que
    se testea del canal no es un doble. Lo que se stubbea es el transporte MCP
    y el campo CKM, que es de Monitor y no entra en el CP2a.
    """

    def __init__(self, canal: ChatChannel, device_id: str = "dev"):
        self.canal = canal
        self.device_id = device_id
        self.llamadas: List[str] = []
        self.publicados_entre: Optional[callable] = None

    async def __aenter__(self): return self
    async def __aexit__(self, *a): return False

    async def call_tool(self, nombre: str, args: dict | None = None):
        args = args or {}
        self.llamadas.append(nombre)

        class _R:
            def __init__(self, data): self.data = data

        if nombre == "get_clock":
            return _R(self.canal.get_clock())
        if nombre == "get_messages":
            since = args.get("since")
            msgs = []
            for i, m in enumerate(self.canal.get_history()):
                d = m.to_dict(); d["message_id"] = f"msg-{i}"
                if since is None or _epoch(m.timestamp) > since:
                    msgs.append(d)
            # gancho para publicar justo entre get_clock y get_messages
            if self.publicados_entre is not None:
                gancho, self.publicados_entre = self.publicados_entre, None
                gancho()
            return _R(msgs)
        if nombre == "get_monitor_state":
            return _R({"D_ckm": None, "temp_signal": "UNKNOWN", "c_S": None,
                       "fi": None, "Delta_r": None})
        if nombre == "join_channel":
            return _R({"ok": True})
        if nombre == "leave_channel":
            return _R({"ok": True})
        if nombre == "send_message":
            await self.canal.publish(args["device_id"], "AI", args["text"])
            return _R({"ok": True})
        raise AssertionError(f"tool inesperada: {nombre}")


def _publicar_sync(canal, device_id: str, text: str) -> None:
    """Publica sin pasar por await: el canal es local y la lista es una lista."""
    from datetime import datetime, timezone
    from iap_chatroom.channel import Message
    ahora = canal._ahora()
    canal.messages.append(Message(
        device_id=device_id, device_type="AI", text=text,
        timestamp=datetime.fromtimestamp(ahora, timezone.utc).isoformat(),
        tick=canal.tick(), reloj="canal",
    ))


def _epoch(iso: str) -> float:
    from datetime import datetime
    return datetime.fromisoformat(iso).timestamp()


@pytest.fixture
def canal(monkeypatch):
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


def _device(provider, **kw) -> AutonomousDevice:
    return AutonomousDevice(device_id=kw.pop("device_id", "dev"),
                            provider=provider,
                            system_prompt="stub",
                            poll_interval=0.0, **kw)


def _correr(dev, client, duration=0.05):
    """Corre el loop con el Client stubbeado."""
    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    mod.Client = lambda url: client
    try:
        asyncio.run(dev.run(duration=duration))
    finally:
        mod.Client = orig


# ── trigger_mode (P11) ──────────────────────────────────────────────────────

def test_el_unico_modo_vivo_es_continuo() -> None:
    d = _device(ProviderStub([]))
    assert d.trigger_mode == "continuo"


def test_on_message_ya_no_existe_como_modo() -> None:
    """El modo viejo quedó congelado; no está detrás de un flag."""
    with pytest.raises(ValueError, match="no existe"):
        _device(ProviderStub([]), trigger_mode="on_message")
    with pytest.raises(ValueError, match="freeze"):
        _device(ProviderStub([]), trigger_mode="on_message")


def test_el_modo_queda_declarado_en_la_traza(canal) -> None:
    dev = _device(ProviderStub(["OP_SILENCE"] * 3))
    _correr(dev, ClientStub(canal))
    assert all(d["trigger_mode"] == "continuo" for d in dev.decisiones())


# ── una decisión por vuelta ─────────────────────────────────────────────────

def test_una_decision_por_vuelta_aunque_entren_varios_mensajes(canal) -> None:
    """
    Antes había un ODA por mensaje: cinco mensajes eran cinco decisiones.
    """
    client = ClientStub(canal)
    # Los cinco se publican DESPUÉS del join: un device que se suma no ve como
    # "nuevo" lo que ya estaba —el corte inicial se toma al unirse—, y eso es
    # el comportamiento de siempre, no algo que el CP2a cambie.
    client.publicados_entre = lambda: [
        _publicar_sync(canal, "otro", f"m{i}") for i in range(5)
    ]

    prov = ProviderStub(["OP_SILENCE"] * 5)
    dev = _device(prov)
    _correr(dev, client, duration=0.04)

    ds = dev.decisiones()
    con_mensajes = [d for d in ds if d["n_nuevos"] > 0]
    assert len(con_mensajes) == 1, \
        f"los cinco tenían que entrar a UNA vuelta, entraron a {len(con_mensajes)}"
    assert con_mensajes[0]["n_nuevos"] == 5, "los cinco en la MISMA vuelta"
    assert len(prov.llamadas) == len(ds), "una llamada al gate por vuelta"


def test_los_ticks_no_disparan_decisiones(canal, monkeypatch) -> None:
    """El tick se observa; no dispara. Muchos ticks, una vuelta."""
    t0 = canal._t0
    reloj = {"t": t0 + TICK_PERIODO_S * 50}    # 50 ticks ya pasaron
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))

    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, ClientStub(canal), duration=0.02)

    ds = dev.decisiones()
    assert ds, "tuvo que haber al menos una vuelta"
    assert all(d["tick"] == 50 for d in ds), "el tick se observa"
    assert all(d["n_nuevos"] == 0 for d in ds)
    # Lo nítido: **varias vueltas dentro del MISMO tick**. Si el tick disparara
    # el ciclo, un tick daría una vuelta. El ritmo lo fija el device.
    assert len(ds) > 1, "hacen falta varias vueltas para que el test mida algo"
    assert len({d["tick"] for d in ds}) == 1, \
        "el tick cambió: el test no prueba lo que dice"
    assert ds[0]["tick_anterior"] == -1 and ds[1]["tick_anterior"] == 50, \
        "el device recuerda el tick de su vuelta anterior, y es el mismo"


# ── el silencio no es absorbente ────────────────────────────────────────────

def test_el_silencio_no_es_absorbente(canal) -> None:
    """
    Nadie publica nunca, y el device sigue decidiendo vuelta tras vuelta.

    Antes, si todos elegían OP_SILENCE no aparecía ningún mensaje nuevo y
    nadie volvía a dispararse: el silencio terminaba el proceso.
    """
    # 2000 respuestas explícitas: el silencio que este test mide tiene que ser
    # DECIDIDO, no el default del stub. Con el default viejo (`OP_SILENCE`) una
    # parte de estas vueltas medía una decisión que nadie tomó.
    prov = ProviderStub(["OP_SILENCE"] * 2000)
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.08)

    ds = dev.decisiones()
    assert len(ds) >= 3, f"el ciclo se detuvo con el canal callado: {len(ds)} vueltas"
    assert all(d["decision"] == "OP_SILENCE" for d in ds), \
        "alguna vuelta no decidió: el test necesita respuestas para todas"
    assert all(d["n_nuevos"] == 0 for d in ds)
    assert len(canal.get_history()) == 0, "nadie publicó, y el ciclo siguió igual"


def test_iniciativa_el_diseno_permite_hablar_primero(canal) -> None:
    """
    Con el canal en silencio, el device **puede** publicar primero.

    No se le exige que hable: se verifica que el diseño se lo permite (TASK).
    """
    prov = ProviderStub(["INTERACT", "hola, soy el primero", "OP_SILENCE"])
    dev = _device(prov)
    assert len(canal.get_history()) == 0, "el canal arranca callado"
    _correr(dev, ClientStub(canal), duration=0.0001)

    hist = canal.get_history()
    assert len(hist) == 1, "el device no pudo hablar primero"
    assert hist[0].device_id == "dev"
    assert dev.decisiones()[0]["n_nuevos"] == 0, \
        "habló sin que nadie le hablara: eso es iniciativa"


# ── LEAVE por decisión propia ───────────────────────────────────────────────

def test_leave_por_decision_propia_antes_de_duration(canal) -> None:
    client = ClientStub(canal)
    prov = ProviderStub(["LEAVE"])
    dev = _device(prov)
    _correr(dev, client, duration=10.0)        # duration largo: no vence

    ds = dev.decisiones()
    assert len(ds) == 1, "se fue en la primera vuelta"
    assert ds[0]["decision"] == "LEAVE"
    assert dev._se_fue is True
    assert client.llamadas.count("leave_channel") == 1, \
        "leave_channel se llama una vez, no dos"


def test_si_vence_duration_tambien_se_va(canal) -> None:
    client = ClientStub(canal)
    dev = _device(ProviderStub(["OP_SILENCE"] * 5))
    _correr(dev, client, duration=0.03)
    assert dev._se_fue is False
    assert client.llamadas.count("leave_channel") == 1


def test_una_palabra_desconocida_es_UNKNOWN_no_silencio(canal) -> None:
    """
    **Una respuesta ilegible es UNKNOWN, no OP_SILENCE.**

    No actuar sigue siendo la salida segura, pero el nombre no puede ser una
    decisión que nadie tomó. Antes este test pedía `OP_SILENCE`; lo corrigió
    la segunda mitad de la nota de Opus sobre el CP2v, que delamor me pasó.
    """
    dev = _device(ProviderStub(["QUIZAS"] + ["OP_SILENCE"] * 2000))
    _correr(dev, ClientStub(canal), duration=0.02)
    ds = dev.decisiones()
    assert ds[0]["decision"] == "UNKNOWN"
    assert ds[0]["ilegibles"] == 1
    assert all(d["decision"] == "OP_SILENCE" for d in ds[1:]), \
        "las vueltas siguientes tienen respuesta explícita y son legibles"
    assert len(canal.get_history()) == 0, "UNKNOWN no autoriza ninguna acción"

    c = dev.costo()
    assert c["ilegibles"] == 1
    assert c["errores_llm"] == 0, \
        "el provider respondió: no es un error de infraestructura"

    # la respuesta CRUDA, con su causa (pedido de delamor para el vivo con 8B)
    ej = c["ejemplos_ilegibles"][0]
    assert ej["causa"] == "respuesta_ilegible"
    assert ej["respuesta_cruda"] == "QUIZAS"
    assert ej["truncada"] is False and ej["largo"] == 6
    assert ej["model"] == "stub"


def test_la_respuesta_cruda_queda_entera_y_sin_normalizar(canal) -> None:
    """
    **Cruda**: sin `strip`, sin `upper`. En el vivo con el 8B, esa respuesta es
    lo que va a mostrar si el problema está en el gate —el prompt pide una
    palabra y el modelo contesta una frase— o en el modelo.
    """
    cruda = "  Creo que lo mejor sería esperar un momento antes de responder.\n"
    dev = _device(ProviderStub([cruda]))
    _correr(dev, ClientStub(canal), duration=0.0001)

    ej = dev.costo()["ejemplos_ilegibles"][0]
    assert ej["respuesta_cruda"] == cruda, \
        "la respuesta se guardó normalizada: se pierde lo que hay que mirar"
    assert ej["causa"] == "respuesta_ilegible"
    assert dev.decisiones()[0]["decision"] == "UNKNOWN"


def test_una_respuesta_larga_se_trunca_y_se_declara(canal) -> None:
    larga = "x" * 900
    dev = _device(ProviderStub([larga]))
    _correr(dev, ClientStub(canal), duration=0.0001)
    ej = dev.costo()["ejemplos_ilegibles"][0]
    assert len(ej["respuesta_cruda"]) == 500
    assert ej["truncada"] is True and ej["largo"] == 900


def test_una_respuesta_vacia_tambien_es_ilegible(canal) -> None:
    dev = _device(ProviderStub([""]))
    _correr(dev, ClientStub(canal), duration=0.0001)
    ds = dev.decisiones()
    assert ds[0]["decision"] == "UNKNOWN" and ds[0]["ilegibles"] == 1
    assert dev.costo()["ejemplos_ilegibles"][0]["respuesta_cruda"] == ""


def test_los_errores_llevan_su_causa(canal) -> None:
    """`error_provider` o `rate_limit`, para poder filtrar la traza."""
    prov = ProviderStub(["OP_SILENCE"] * 5, falla_en={1})
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.02)
    assert dev.costo()["errores"][0]["causa"] == "error_provider"


# ── dos publicaciones seguidas, sin reaccionar a la propia ──────────────────

def test_dos_publicaciones_seguidas_sin_reaccion_a_la_propia(canal) -> None:
    """
    El device publica dos veces por decisión, y **ninguna** queda registrada
    como reacción a la anterior (TASK §1, precisión del 7 oct).
    """
    prov = ProviderStub(["INTERACT", "primero", "INTERACT", "segundo",
                         "OP_SILENCE"])
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.03)

    hist = canal.get_history()
    textos = [m.text for m in hist if m.device_id == "dev"]
    assert textos[:2] == ["primero", "segundo"], f"publicó {textos}"

    ds = [d for d in dev.decisiones() if d["decision"] == "INTERACT"]
    assert len(ds) >= 2
    for d in ds:
        assert d["trigger"] is None, \
            "una publicación quedó registrada como reacción a algo"
        assert d["n_nuevos"] == 0, \
            "el propio mensaje se contó como mensaje nuevo"


# ── requisito 1: el since sale del canal ────────────────────────────────────

def test_el_since_sale_del_reloj_del_canal_no_del_device(canal, monkeypatch) -> None:
    """
    Requisito 1. Si el `since` saliera de `time.time()` del device y el device
    estuviera adelantado, los mensajes se descartarían en silencio — el
    hallazgo del CP0.

    Se simula el desfasaje: el reloj del canal queda MUY atrás del de la
    máquina. Con el `since` del device, el corte caería en el futuro del canal
    y nada pasaría el filtro.
    """
    # El reloj del canal queda MUY atrás del de la máquina, y avanza de a poco:
    # si se congelara, todo caería exactamente en el corte y `>` nunca pasaría
    # —artefacto del test, no del código—.
    reloj = {"t": 1_000_000.0}                # ~1970, muy anterior a time.time()

    def _ahora_atrasado():
        reloj["t"] += 0.001
        return reloj["t"]

    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(_ahora_atrasado))
    monkeypatch.setattr(canal, "_t0", 1_000_000.0 - 5.0)

    client = ClientStub(canal)
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "mensaje del canal")

    dev = _device(ProviderStub(["OP_SILENCE"] * 4))
    _correr(dev, client, duration=0.04)

    # Con el since del device (time.time(), ~1.79e9) el corte caería en el
    # futuro del canal (1e6) y el mensaje no pasaría nunca el filtro.
    vistos = sum(d["n_nuevos"] for d in dev.decisiones())
    assert vistos == 1, \
        "el since no salió del reloj del canal: el mensaje se descartó"


def test_get_messages_con_el_since_real_del_device(canal) -> None:
    """
    Requisito 3: probado con el `since` que el device **usa**, no con
    `canal._ahora()` escrito en el test.
    """
    client = ClientStub(canal)
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "uno")
    dev = _device(ProviderStub(["OP_SILENCE"] * 8))

    _correr(dev, client, duration=0.05)
    ds = dev.decisiones()
    con = [i for i, d in enumerate(ds) if d["n_nuevos"] > 0]
    assert len(con) == 1, \
        f"'uno' se contó en {len(con)} vueltas: el since no avanzó"
    assert ds[con[0]]["n_nuevos"] == 1


def test_un_mensaje_entre_get_clock_y_get_messages_no_se_pierde(canal) -> None:
    """
    La condición de orden que señaló Opus (T2): el `since` de la vuelta
    siguiente se lee ANTES de `get_messages`. Un mensaje que llega en el medio
    aparece en la vuelta siguiente.
    """
    client = ClientStub(canal)

    def publicar_en_el_medio():
        asyncio.get_event_loop_policy()
        asyncio.run_coroutine_threadsafe if False else None
        # publicación sincrónica: el canal es local
        from iap_chatroom.channel import Message
        from datetime import datetime, timezone
        ahora = canal._ahora()
        canal.messages.append(Message(
            device_id="otro", device_type="AI", text="en el medio",
            timestamp=datetime.fromtimestamp(ahora, timezone.utc).isoformat(),
            tick=canal.tick(), reloj="canal",
        ))

    client.publicados_entre = publicar_en_el_medio
    dev = _device(ProviderStub(["OP_SILENCE"] * 6))
    _correr(dev, client, duration=0.05)

    vistos = sum(d["n_nuevos"] for d in dev.decisiones())
    assert vistos == 1, \
        f"el mensaje publicado entre get_clock y get_messages se perdió (vistos={vistos})"


# ── requisito 2: el ODA observa el clock en silencio ───────────────────────

def test_el_log_del_canal_crece_con_el_canal_callado(canal, monkeypatch) -> None:
    """
    Requisito 2. **Reloj controlado**, no `sleep`: cada vuelta avanza más de un
    período de tick, así que cada vuelta observa un tick nuevo y el log crece.

    Inversión: con el reloj quieto, el log no crece y este test falla.
    """
    t0 = canal._t0
    reloj = {"t": t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))

    prov = ProviderStub(["OP_SILENCE"] * 10)
    dev = _device(prov)

    client = ClientStub(canal)
    original = client.call_tool

    async def avanzando(nombre, args=None):
        if nombre == "get_clock":
            reloj["t"] += TICK_PERIODO_S * 1.5     # el reloj corre
        return await original(nombre, args)

    client.call_tool = avanzando
    _correr(dev, client, duration=0.05)

    log = canal.clock_log()
    assert len(canal.get_history()) == 0, "el canal tiene que estar callado"
    assert len(log) >= 3, f"el log no creció con el canal callado: {len(log)}"
    assert all(e["con_mensajes"] is False for e in log)
    ticks = [e["tick"] for e in log]
    assert ticks == sorted(ticks) and len(set(ticks)) == len(ticks)


def test_el_clock_se_lee_una_vez_por_vuelta(canal) -> None:
    """
    Una sola lectura del clock por vuelta, y es la que fija el corte (T2).

    Antes `_observe` pedía `get_clock` por su cuenta y el loop sobreescribía
    ese valor dos líneas después: la llamada no hacía nada. Lo encontré
    invirtiendo —sacarla pasaba los 319— y no leyendo.
    """
    client = ClientStub(canal)
    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.02)

    vueltas = len(dev.decisiones())
    clocks = client.llamadas.count("get_clock")
    # 1 del corte inicial, antes del join + 1 por vuelta
    assert clocks == vueltas + 1, \
        f"{clocks} lecturas de get_clock para {vueltas} vueltas: no es una por vuelta"


def test_el_corte_se_atrasa_un_tick(canal, monkeypatch) -> None:
    """
    El corte es `t − periodo_s`: una ventana **en tiempo**, no en vueltas.

    Reemplaza a `test_el_corte_se_atrasa_una_vuelta`, que fijaba el solape por
    vueltas. Ese solape **no cubría el borde**: con el reloj congelado todos
    los cortes son el mismo número y mover cuál se usa no cambia nada (medido:
    256 vueltas, 0 vistos). La corrección es de Opus.
    """
    t0 = canal._t0
    reloj = {"t": t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))

    client = ClientStub(canal)
    original = client.call_tool
    ts_leidos, cortes_usados = [], []

    async def registrando(nombre, args=None):
        if nombre == "get_clock":
            reloj["t"] += TICK_PERIODO_S * 1.5
        r = await original(nombre, args)
        if nombre == "get_clock":
            ts_leidos.append(r.data["t"])
        if nombre == "get_messages" and (args or {}).get("since") is not None:
            cortes_usados.append(args["since"])
        return r

    client.call_tool = registrando
    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.03)

    assert len(cortes_usados) >= 3, "hacen falta varias vueltas"
    for k, corte in enumerate(cortes_usados):
        assert corte == pytest.approx(ts_leidos[k] - TICK_PERIODO_S), \
            f"vuelta {k}: el corte no es la lectura menos un tick"
        assert corte < ts_leidos[k], "el corte tiene que quedar ESTRICTAMENTE antes"


def test_un_mensaje_sellado_en_el_corte_no_se_pierde(canal, monkeypatch) -> None:
    """
    **El borde de T2, con el reloj CONGELADO.** El test que Opus pidió y que la
    primera versión —solape por vueltas— no podía pasar.

    Con el reloj quieto, todas las lecturas dan el mismo instante, y un mensaje
    sellado ahí no pasaría `> since` si el corte fuera ese mismo instante. Con
    la ventana en tiempo el corte queda **estrictamente antes**, así que pasa.

    Y pasa **una sola vez**: la ventana lo devuelve en varias vueltas y
    `_vistos` descarta las repeticiones.
    """
    congelado = canal._t0 + TICK_PERIODO_S * 3
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: congelado))

    client = ClientStub(canal)
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "en el corte")

    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.02)

    sellado = _epoch(canal.get_history()[0].timestamp)
    assert sellado == congelado, "el test necesita el mensaje sellado en el corte"

    vistos = sum(d["n_nuevos"] for d in dev.decisiones())
    assert vistos >= 1, \
        "el mensaje sellado exactamente en el instante del corte se perdió"
    assert vistos == 1, f"se contó {vistos} veces: _vistos no descartó el solape"


def test_el_solape_no_duplica_mensajes(canal) -> None:
    """El solape de una vuelta repite mensajes, y `_vistos` los descarta."""
    client = ClientStub(canal)
    client.publicados_entre = lambda: [
        _publicar_sync(canal, "otro", f"m{i}") for i in range(3)
    ]
    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.04)

    vistos = sum(d["n_nuevos"] for d in dev.decisiones())
    assert vistos == 3, f"con el solape se contaron {vistos} de 3 mensajes"


def test_el_join_no_dispara_el_ciclo(canal) -> None:
    """
    El join dejó de ser semilla: entra como información, no como disparador.

    En la serie congelada el SYSTEM "joined" podía disparar el ciclo (Caso
    0.5). En el continuo nada dispara — y el lugar del seed lo ocupa la
    iniciativa.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 5))
    _correr(dev, ClientStub(canal), duration=0.02)

    ds = dev.decisiones()
    assert ds, "el ciclo corre igual, sin ningún disparador"
    # el ClientStub no publica el SYSTEM del join; lo que importa es que el
    # ciclo no dependió de ningún mensaje para arrancar
    assert ds[0]["n_nuevos"] == 0
    assert ds[0]["trigger"] is None


def test_dos_devices_el_silencio_no_es_absorbente_entre_ellos(canal) -> None:
    """
    **Dos devices a la vez**, que es el fenómeno de la serie y no estaba
    testeado (punto ciego que señaló Opus).

    Los dos eligen OP_SILENCE siempre. Antes eso terminaba el proceso: sin
    mensajes nuevos nadie se disparaba. Ahora los dos siguen decidiendo.
    """
    d1 = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="d1")
    d2 = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="d2")
    c1, c2 = ClientStub(canal, "d1"), ClientStub(canal, "d2")

    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    clientes = {"d1": c1, "d2": c2}

    async def ambos():
        await asyncio.gather(d1.run(duration=0.06), d2.run(duration=0.06))

    try:
        mod.Client = lambda url: clientes.pop(next(iter(clientes)))
        asyncio.run(ambos())
    finally:
        mod.Client = orig

    assert len(d1.decisiones()) >= 3, "d1 se detuvo con el canal callado"
    assert len(d2.decisiones()) >= 3, "d2 se detuvo con el canal callado"
    assert len(canal.get_history()) == 0, "nadie publicó, y los dos siguieron"


def test_dos_devices_uno_habla_y_el_otro_lo_ve(canal) -> None:
    """Con dos devices, lo que uno publica entra a la observación del otro."""
    # d1 calla las primeras vueltas: si publicara en la vuelta 1, podría
    # hacerlo ANTES de que d2 tomara su corte inicial, y entonces para d2 eso
    # sería historia y no mensaje nuevo. No es un fallo: un device que se suma
    # no ve como nuevo lo que ya estaba. Era una carrera en el test.
    d1 = _device(ProviderStub(["OP_SILENCE"] * 20 + ["INTERACT", "hola d2"]
                              + ["OP_SILENCE"] * 50), device_id="d1")
    d2 = _device(ProviderStub(["OP_SILENCE"] * 200), device_id="d2")
    c1, c2 = ClientStub(canal, "d1"), ClientStub(canal, "d2")

    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    pendientes = [c1, c2]

    async def ambos():
        await asyncio.gather(d1.run(duration=0.12), d2.run(duration=0.12))

    try:
        mod.Client = lambda url: pendientes.pop(0)
        asyncio.run(ambos())
    finally:
        mod.Client = orig

    assert any(m.text == "hola d2" for m in canal.get_history()), "d1 no publicó"
    assert sum(d["n_nuevos"] for d in d2.decisiones()) >= 1, \
        "d2 no vio lo que publicó d1"
    assert all(d["n_nuevos"] == 0 for d in d1.decisiones()), \
        "d1 contó su propio mensaje como nuevo"


def test_lo_publicado_antes_del_corte_no_cuenta_pero_esta_en_history(
    canal, monkeypatch
) -> None:
    """
    **El lado opuesto de la carrera del join**, con orden fijo (lo pidió Opus).

    Si d1 publica **antes** de que d2 tome su corte, d2 **no** lo cuenta en
    `n_nuevos` —no es nuevo para él— pero **sí lo tiene en `history`**, porque
    `_observe` pide el historial con `since=None`.

    Eso es lo que el CP2a llamó "el comportamiento de siempre": un device que
    se suma no ve como nuevo lo que ya estaba, y lo de antes del corte entra
    como historia.

    **Más de un tick antes**: la ventana del corte inicial (`t − periodo_s`)
    alcanza hacia atrás, así que lo publicado *dentro* de ese tick sí cuenta
    como nuevo. Eso lo mide `test_la_ventana_inicial_alcanza_un_tick_hacia_atras`.
    """
    reloj = {"t": canal._t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))

    asyncio.run(canal.publish("otro", "AI", "antes del corte"))
    reloj["t"] += TICK_PERIODO_S * 3          # el device arranca 3 ticks después
    assert len(canal.get_history()) == 1

    dev = _device(ProviderStub(["OP_SILENCE"] * 5), device_id="d2")
    client = ClientStub(canal, "d2")
    historias = []
    original = client.call_tool

    async def registrando(nombre, args=None):
        r = await original(nombre, args)
        if nombre == "get_messages" and (args or {}).get("since") is None:
            historias.append([m["text"] for m in r.data])
        return r

    client.call_tool = registrando
    _correr(dev, client, duration=0.02)

    assert all(d["n_nuevos"] == 0 for d in dev.decisiones()), \
        "contó como nuevo algo publicado más de un tick antes de su corte"
    assert all(d["trigger"] is None for d in dev.decisiones())
    assert historias, "_observe tiene que haber pedido el historial"
    assert all("antes del corte" in h for h in historias), \
        "lo de antes del corte tiene que estar en history, aunque no sea nuevo"


def test_la_ventana_inicial_alcanza_un_tick_hacia_atras(canal, monkeypatch) -> None:
    """
    **Efecto de la ventana, medido y declarado.**

    El corte inicial es `t − periodo_s`, así que lo publicado **dentro de ese
    tick**, antes de que el device existiera, **cuenta como nuevo**. Está
    acotado a un tick y es el precio de cerrar el borde `timestamp == since`.

    Lo encontró este test: lo escribí esperando que nada de antes del join
    contara, y la ventana lo desmintió.
    """
    congelado = canal._t0 + TICK_PERIODO_S * 2
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: congelado))

    asyncio.run(canal.publish("otro", "AI", "dentro del tick"))

    dev = _device(ProviderStub(["OP_SILENCE"] * 5), device_id="d3")
    _correr(dev, ClientStub(canal, "d3"), duration=0.02)

    vistos = sum(d["n_nuevos"] for d in dev.decisiones())
    assert vistos == 1, (
        "lo publicado dentro del tick anterior al corte inicial tiene que "
        "contar como nuevo: es el alcance de la ventana, acotado a un tick"
    )


def test_un_clock_sin_periodo_s_es_UNKNOWN_y_el_ciclo_sigue(canal) -> None:
    """
    **Sin `periodo_s` el corte no avanza, y queda UNKNOWN en la traza.**
    Lo preguntó delamor: *"¿UNKNOWN? ¿podría ser?"*.

    Mi primera respuesta fue `or 0.0` —que reintroducía el agujero en
    silencio— y la segunda levantar, que **mata el instrumento**. El criterio
    del proyecto es el tercero: UNKNOWN **no autoriza una acción** —acá, elegir
    un corte nuevo— pero **no termina el proceso**. Quedarse atrás da
    duplicados, que `_vistos` descarta, y nunca pérdidas.
    """
    client = ClientStub(canal)
    original = client.call_tool

    async def sin_periodo(nombre, args=None):
        r = await original(nombre, args)
        if nombre == "get_clock":
            d = dict(r.data); d.pop("periodo_s", None)
            class _R:
                data = d
            return _R()
        return r

    client.call_tool = sin_periodo
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "igual lo veo")

    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.02)       # no levanta

    ds = dev.decisiones()
    assert ds, "el ciclo tiene que seguir corriendo"
    assert all(d["ventana"] == "UNKNOWN" for d in ds), \
        "la ausencia del grano tiene que quedar nombrada en la traza"
    vistos = sum(d["n_nuevos"] for d in ds)
    assert vistos == 1, \
        f"con el corte quieto el mensaje no se pierde ni se duplica (vistos={vistos})"


@pytest.mark.parametrize("malo", [None, 0, 0.0, -1.0, "un segundo", True])
def test_un_periodo_s_invalido_es_UNKNOWN(canal, malo) -> None:
    """Cero, negativo, no numérico y `True` —que es `int` en Python—."""
    dev = _device(ProviderStub(["OP_SILENCE"]))
    assert dev._ventana({"t": 1.0, "periodo_s": malo}) is None


def test_el_ancho_de_la_ventana_es_el_periodo_declarado(canal) -> None:
    """La ventana sale del clock, no de una constante cableada en el device."""
    dev = _device(ProviderStub(["OP_SILENCE"]))
    assert dev._ventana({"t": 1.0, "periodo_s": 2.5}) == 2.5
    assert dev._ventana({"t": 1.0, "periodo_s": TICK_PERIODO_S}) == TICK_PERIODO_S


def test_con_grano_la_traza_lleva_la_ventana(canal) -> None:
    dev = _device(ProviderStub(["OP_SILENCE"] * 5))
    _correr(dev, ClientStub(canal), duration=0.02)
    assert all(d["ventana"] == TICK_PERIODO_S for d in dev.decisiones())


def test_sin_grano_Y_con_reloj_congelado_el_corte_quieto_salva_el_mensaje(
    canal, monkeypatch
) -> None:
    """
    **El caso donde "no avanzar el corte" es lo que salva.**

    Lo encontré invirtiendo: con el reloj avanzando, dejar que el corte avance
    a `t` exacto **igual deja pasar** el mensaje —porque el sello queda después
    de la lectura— así que los 337 pasaban. El riesgo está con el reloj
    congelado: ahí `t` **es** el sello, y avanzar el corte lo pierde para
    siempre.

    Sin grano el corte no avanza —se queda en `None`, el inicial— y el mensaje
    aparece.
    """
    congelado = canal._t0 + TICK_PERIODO_S * 3
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: congelado))

    client = ClientStub(canal)
    original = client.call_tool

    async def sin_periodo(nombre, args=None):
        r = await original(nombre, args)
        if nombre == "get_clock":
            d = dict(r.data); d.pop("periodo_s", None)
            class _R:
                data = d
            return _R()
        return r

    client.call_tool = sin_periodo
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "sellado en t")

    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.02)

    ds = dev.decisiones()
    assert all(d["ventana"] == "UNKNOWN" for d in ds)
    assert _epoch(canal.get_history()[0].timestamp) == congelado, \
        "el test necesita el mensaje sellado en el instante del corte"
    vistos = sum(d["n_nuevos"] for d in ds)
    assert vistos >= 1, (
        "con el reloj congelado y sin grano, el corte tiene que quedarse "
        "quieto: si avanzara a t exacto, el mensaje se perdería para siempre"
    )
    assert vistos == 1, f"se contó {vistos} veces: _vistos no descartó"


# ── instrumentación para el primer vivo (pedido de delamor) ─────────────────

def test_las_llamadas_al_llm_se_cuentan_no_se_infieren(canal) -> None:
    """
    Cada vuelta registra **cuántas llamadas al LLM hizo de verdad**.

    Hoy toda vuelta llama al gate, así que vueltas == llamadas. Con el criterio
    local (CP2b) deja de ser cierto —una vuelta con skip cuesta cero— y la
    inferencia se rompe justo cuando el filtro entra. Por eso se cuentan.
    """
    prov = ProviderStub(["OP_SILENCE"] * 10)
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.02)

    ds = dev.decisiones()
    assert all(d["llamadas_llm"] == 1 for d in ds), \
        "una vuelta que calla cuesta una llamada: la del gate"
    assert sum(d["llamadas_llm"] for d in ds) == len(prov.llamadas), \
        "lo contado no coincide con lo que el provider recibió"
    assert dev.costo()["llamadas_llm"] == len(prov.llamadas)


def test_una_vuelta_que_publica_cuesta_dos_llamadas(canal) -> None:
    """Gate + generación. Es el `1 + p` del costo estimado."""
    dev = _device(ProviderStub(["INTERACT", "hola"] + ["OP_SILENCE"] * 10))
    _correr(dev, ClientStub(canal), duration=0.02)

    ds = dev.decisiones()
    publicaron = [d for d in ds if d["decision"] == "INTERACT"]
    assert publicaron, "el test necesita al menos una publicación"
    assert all(d["llamadas_llm"] == 2 for d in publicaron)
    assert all(d["llamadas_llm"] == 1 for d in ds if d["decision"] == "OP_SILENCE")


def test_un_error_del_provider_queda_registrado_y_el_ciclo_sigue(canal) -> None:
    """
    Una falla del provider **no mata el run**, y **no se traga**.

    Sin registro, un vivo silencioso no se puede atribuir entre el modelo que
    calla, el canal que pierde y la infraestructura que falla. Con registro, sí.
    """
    prov = ProviderStub(["OP_SILENCE"] * 10, falla_en={1, 2})
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.03)   # no levanta

    ds = dev.decisiones()
    assert len(ds) >= 3, "el ciclo tiene que seguir después del error"
    assert ds[0]["errores_llm"] == 1 and ds[1]["errores_llm"] == 1
    assert ds[0]["decision"] == "UNKNOWN", \
        "un error del provider no es OP_SILENCE: no hubo decisión"
    assert ds[0]["ilegibles"] == 0, \
        "el provider no respondió: no es una respuesta ilegible"

    c = dev.costo()
    assert c["errores_llm"] == 2
    assert all(e["fase"] == "decide" for e in c["errores"])
    assert all(e["provider"] == "stub" for e in c["errores"])
    assert c["llamadas_llm"] >= 2, \
        "una llamada que falló igual se hizo: cuenta para el costo"


def test_un_error_al_generar_no_publica_nada(canal) -> None:
    """Decidió INTERACT pero el provider falló al generar: no se publica."""
    # llamada 1 = gate (INTERACT), llamada 2 = generate (falla)
    prov = ProviderStub(["INTERACT", "no deberia publicarse"], falla_en={2})
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.0001)

    assert len(canal.get_history()) == 0, "publicó pese a que la generación falló"
    c = dev.costo()
    assert c["errores_llm"] == 1
    assert c["errores"][0]["fase"] == "generate"
    assert dev.decisiones()[0]["llamadas_llm"] == 2, \
        "las dos llamadas se hicieron, aunque la segunda falló"


def test_el_costo_registra_provider_y_modelo(canal) -> None:
    """
    El modelo es **parte de las condiciones** (README del freeze), así que cada
    run queda etiquetado: lo medido con un modelo barato no se transfiere a uno
    de frontera.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 2000,
                               model="llama-3.3-70b-versatile"))
    _correr(dev, ClientStub(canal), duration=0.02)

    c = dev.costo()
    assert c["provider"] == "stub"
    assert c["model"] == "llama-3.3-70b-versatile"
    assert c["device_id"] == "dev"
    assert c["vueltas"] == len(dev.decisiones())
    assert c["llamadas_por_vuelta"] == pytest.approx(
        c["llamadas_llm"] / c["vueltas"], abs=1e-3
    )
    assert c["decisiones_por_tipo"] == {"OP_SILENCE": c["vueltas"]}


def test_el_costo_cuenta_las_vueltas_con_ventana_unknown(canal) -> None:
    """Para atribuir: una vuelta con el grano UNKNOWN es del canal, no del modelo."""
    client = ClientStub(canal)
    original = client.call_tool

    async def sin_periodo(nombre, args=None):
        r = await original(nombre, args)
        if nombre == "get_clock":
            d = dict(r.data); d.pop("periodo_s", None)
            class _R:
                data = d
            return _R()
        return r

    client.call_tool = sin_periodo
    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.02)

    c = dev.costo()
    assert c["vueltas_con_ventana_unknown"] == c["vueltas"] > 0


def test_error_e_ilegible_se_registran_por_separado(canal) -> None:
    """
    **Dos causas, una consecuencia.** Las dos dan UNKNOWN y ninguna actúa,
    pero se cuentan aparte: para atribuir un vivo silencioso no es lo mismo
    que falle la infraestructura que el modelo conteste algo ilegible.
    """
    prov = ProviderStub(["QUIZAS"], falla_en={2})
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.02)

    c = dev.costo()
    assert c["ilegibles"] >= 1 and c["errores_llm"] >= 1
    ds = dev.decisiones()
    assert ds[0]["ilegibles"] == 1 and ds[0]["errores_llm"] == 0
    assert ds[1]["errores_llm"] == 1 and ds[1]["ilegibles"] == 0
    assert all(d["decision"] == "UNKNOWN" for d in ds[:2])


def test_un_429_queda_marcado_aparte(canal) -> None:
    """
    El rate limit se distingue del resto: no dice "algo se rompió", dice "vas
    demasiado rápido". Es información sobre el ritmo.
    """
    class _Prov(ProviderStub):
        async def complete(self, messages):
            self.llamadas.append(messages)
            raise RuntimeError("Error code: 429 - rate limit exceeded")

    dev = _device(_Prov([]))
    _correr(dev, ClientStub(canal), duration=0.02)

    c = dev.costo()
    assert c["errores_llm"] >= 1
    assert c["errores_rate_limit"] == c["errores_llm"], \
        "el 429 tiene que quedar marcado como rate_limit"
    assert all(e["rate_limit"] for e in c["errores"])
    assert all(d["decision"] == "UNKNOWN" for d in dev.decisiones())


def test_un_error_que_no_es_429_no_se_marca_como_rate_limit(canal) -> None:
    """Y si no matchea, queda como genérico — pero se registra igual."""
    prov = ProviderStub(["OP_SILENCE"] * 5, falla_en={1})
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.02)
    c = dev.costo()
    assert c["errores_llm"] == 1
    assert c["errores_rate_limit"] == 0
    assert c["errores"][0]["rate_limit"] is False


def test_el_ritmo_declarado_no_invent_el_limite_de_la_cuenta(canal) -> None:
    """
    El ritmo se declara; **el límite del provider es UNKNOWN** y se lee en su
    consola. No lo invento.
    """
    dev = AutonomousDevice(device_id="d", provider=ProviderStub([]),
                           system_prompt="s", poll_interval=2.0)
    r = dev.ritmo_declarado(n_devices=2)
    assert r["poll_interval_s"] == 2.0
    assert r["vueltas_por_minuto_por_device"] == 30.0
    assert r["llamadas_por_minuto_piso"] == 60.0    # 30 x 2 devices
    assert r["llamadas_por_minuto_techo"] == 120.0  # el doble si actúa siempre
    assert r["limite_de_la_cuenta"].startswith("UNKNOWN")


def test_sin_pausa_el_ritmo_no_se_puede_declarar(canal) -> None:
    """Con poll_interval=0 el ritmo lo fija la latencia del provider."""
    dev = AutonomousDevice(device_id="d", provider=ProviderStub([]),
                           system_prompt="s", poll_interval=0.0)
    r = dev.ritmo_declarado()
    assert r["vueltas_por_minuto_por_device"] is None
    assert r["llamadas_por_minuto_piso"] is None
    assert "latencia" in r["nota"]


# ── las cuatro correcciones de Opus al CP2v ────────────────────────────────

def test_el_stub_agotado_no_fabrica_decisiones(canal) -> None:
    """
    **El instrumento no inventa el dato más tranquilizador.**

    El stub agotado devuelve vacío → `UNKNOWN`, no `OP_SILENCE`. Antes
    producía un "el modelo decidió callar" que nadie decidió, y tres tests
    estaban midiendo contra eso.
    """
    prov = ProviderStub([])                      # ninguna respuesta guionada
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.02)

    ds = dev.decisiones()
    assert ds, "el ciclo corre igual"
    assert all(d["decision"] == "UNKNOWN" for d in ds), \
        "el stub agotado fabricó una decisión"
    assert all(d["ilegibles"] == 1 for d in ds)
    assert dev.costo()["ejemplos_ilegibles"][0]["respuesta_cruda"] == ""


def test_un_429_por_status_code_se_lee_del_dato(canal) -> None:
    """
    **`status_code` primero, texto como respaldo.** Un 429 en el atributo es un
    dato; inferirlo del mensaje es una heurística, y la traza dice cuál fue.
    """
    class _Prov(ProviderStub):
        async def complete(self, messages):
            self.llamadas.append(messages)
            e = RuntimeError("algo pasó")        # el texto NO dice 429
            e.status_code = 429
            raise e

    dev = _device(_Prov([]))
    _correr(dev, ClientStub(canal), duration=0.0001)

    err = dev.costo()["errores"][0]
    assert err["rate_limit"] is True
    assert err["rate_limit_segun"] == "status_code", \
        "se leyó del texto cuando el status_code estaba"
    assert err["causa"] == "rate_limit"


def test_un_429_sin_status_code_se_infiere_del_texto_y_se_declara(canal) -> None:
    """Sin el atributo, el respaldo heurístico — y queda dicho que es texto."""
    class _Prov(ProviderStub):
        async def complete(self, messages):
            self.llamadas.append(messages)
            raise RuntimeError("Error code: 429 - rate limit exceeded")

    dev = _device(_Prov([]))
    _correr(dev, ClientStub(canal), duration=0.0001)

    err = dev.costo()["errores"][0]
    assert err["rate_limit"] is True
    assert err["rate_limit_segun"] == "texto"


def test_un_error_comun_no_se_marca_y_dice_como_se_supo(canal) -> None:
    prov = ProviderStub(["OP_SILENCE"] * 2000, falla_en={1})
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.02)
    err = dev.costo()["errores"][0]
    assert err["rate_limit"] is False
    assert err["rate_limit_segun"] is None
    assert err["causa"] == "error_provider"


def test_un_status_code_que_no_es_429_no_se_marca(canal) -> None:
    """Un 500 es una falla, no un límite de ritmo."""
    class _Prov(ProviderStub):
        async def complete(self, messages):
            self.llamadas.append(messages)
            e = RuntimeError("server error")
            e.status_code = 500
            raise e

    dev = _device(_Prov([]))
    _correr(dev, ClientStub(canal), duration=0.0001)
    err = dev.costo()["errores"][0]
    assert err["rate_limit"] is False and err["rate_limit_segun"] is None


def test_un_provider_sin_nombre_queda_en_None_no_en_interrogacion(canal) -> None:
    """La ausencia no se rellena con un valor inventado como "?"."""
    class _SinNombre(ProviderStub):
        pass
    _SinNombre.name = None

    dev = _device(_SinNombre(["OP_SILENCE"] * 2000))
    _correr(dev, ClientStub(canal), duration=0.0001)
    assert dev.costo()["provider"] is None


def test_un_mensaje_sin_timestamp_dice_UNKNOWN_en_el_prompt(canal) -> None:
    """
    Esto entra al prompt que el modelo lee: "?" no le dice nada, UNKNOWN le
    dice que el dato no estaba.
    """
    prov = ProviderStub(["OP_SILENCE"] * 2000)
    dev = _device(prov)
    client = ClientStub(canal)
    original = client.call_tool

    async def sin_timestamp(nombre, args=None):
        r = await original(nombre, args)
        if nombre == "get_messages":
            msgs = [dict(m) for m in r.data]
            for m in msgs:
                m["timestamp"] = None
            class _R:
                data = msgs
            return _R()
        return r

    client.call_tool = sin_timestamp
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "sin sello")
    _correr(dev, client, duration=0.03)

    prompts = [m[-1]["content"] for m in prov.llamadas]
    con_hist = [p for p in prompts if "sin sello" in p]
    assert con_hist, "el historial tenía que llegar al prompt"
    assert all("[UNKNOWN] " in p for p in con_hist), \
        "un timestamp ausente llegó al prompt como algo distinto de UNKNOWN"
    assert not any('[?]' in p for p in prompts)
