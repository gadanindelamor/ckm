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

    def __init__(self, respuestas: List[str]):
        super().__init__(api_key=None, model="stub")
        self.respuestas = list(respuestas)
        self.llamadas: List[List[ChatMessage]] = []

    async def complete(self, messages: List[ChatMessage]) -> str:
        self.llamadas.append(messages)
        if not self.respuestas:
            return "OP_SILENCE"
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
    prov = ProviderStub(["OP_SILENCE"] * 20)
    dev = _device(prov)
    _correr(dev, ClientStub(canal), duration=0.08)

    ds = dev.decisiones()
    assert len(ds) >= 3, f"el ciclo se detuvo con el canal callado: {len(ds)} vueltas"
    assert all(d["decision"] == "OP_SILENCE" for d in ds)
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


def test_una_palabra_desconocida_cae_a_silencio(canal) -> None:
    """No actuar es la salida segura: una respuesta que no se entiende no
    autoriza una acción."""
    dev = _device(ProviderStub(["QUIZAS"]))     # el resto cae al default
    _correr(dev, ClientStub(canal), duration=0.02)
    assert dev.decisiones()[0]["decision"] == "OP_SILENCE"
    assert all(d["decision"] == "OP_SILENCE" for d in dev.decisiones())
    assert len(canal.get_history()) == 0


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


def test_el_corte_se_atrasa_una_vuelta(canal, monkeypatch) -> None:
    """
    El corte de la vuelta sale de **dos** lecturas atrás, no de la anterior.

    Reemplaza a `test_el_clock_observado_es_el_que_fija_el_corte`, cuya
    afirmación **dejó de ser cierta a propósito**: el solape de una vuelta es
    lo que cubre el borde `timestamp == since` del filtro estricto de
    `get_messages` (señalado por Opus sobre el CP2a).
    """
    t0 = canal._t0
    reloj = {"t": t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))

    client = ClientStub(canal)
    original = client.call_tool
    ts_leidos = []
    cortes_usados = []

    async def registrando(nombre, args=None):
        if nombre == "get_clock":
            reloj["t"] += TICK_PERIODO_S * 1.5
        r = await original(nombre, args)
        if nombre == "get_clock":
            ts_leidos.append(r.data["t"])
        if nombre == "get_messages" and args.get("since") is not None:
            cortes_usados.append(args["since"])
        return r

    client.call_tool = registrando
    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.03)

    assert len(ts_leidos) >= 4, "hacen falta varias vueltas para medirlo"
    # ts_leidos[0] es la lectura inicial, anterior al join. La vuelta n usa
    # ts_leidos[n-1], que es la lectura de DOS vueltas atrás contando la
    # inicial: el solape de una vuelta.
    for k, corte in enumerate(cortes_usados):
        esperado = ts_leidos[max(0, k - 1)]
        assert corte == esperado, \
            f"vuelta {k}: corte {corte} != lectura de dos atrás {esperado}"
        assert corte != ts_leidos[k + 1], \
            "el corte salió de la lectura de ESTA vuelta: no hay solape"


def test_el_borde_timestamp_igual_al_corte_SIGUE_ABIERTO(canal, monkeypatch) -> None:
    """
    **El borde de T2 con el reloj congelado NO está cubierto, y este test lo
    mide en vez de evitarlo.**

    Opus pidió un test con el reloj congelado donde *"un mensaje sellado en el
    corte aparece en alguna vuelta"*. **No puede pasar con el solape**, y lo
    medí antes de afirmarlo: con el reloj quieto **todos los cortes son el
    mismo número**, igual al sello del mensaje, y `get_messages` filtra con
    `timestamp > since`, estricto. El solape mueve **cuál** corte se usa;
    cuando todos son el mismo, mover cuál no cambia nada.

    Medido: 256 vueltas, 0 mensajes vistos, 1 corte distinto.

    **El solape sí cubre el caso real** —el reloj avanzando— y eso lo verifica
    `test_el_solape_no_duplica_mensajes` junto con los del `since`. Lo que
    queda abierto es el reloj congelado, y el arreglo sería `>=` en
    `get_messages` más el descarte por `message_id` que el device ya hace.
    **Eso toca `get_messages`, que el enunciado excluyó: no lo toqué y lo
    escalé.**

    Este test afirma el estado actual. **Si algún día se arregla, este test
    falla**, y eso es correcto: hay que borrarlo y poner el que Opus pidió.
    """
    congelado = canal._t0 + TICK_PERIODO_S * 3
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: congelado))

    client = ClientStub(canal)
    cortes = []
    original = client.call_tool

    async def registrando(nombre, args=None):
        if nombre == "get_messages" and (args or {}).get("since") is not None:
            cortes.append(args["since"])
        return await original(nombre, args)

    client.call_tool = registrando
    client.publicados_entre = lambda: _publicar_sync(canal, "otro", "en el corte")

    dev = _device(ProviderStub(["OP_SILENCE"] * 10))
    _correr(dev, client, duration=0.02)

    sellado = _epoch(canal.get_history()[0].timestamp)
    assert sellado == congelado, "el test necesita el mensaje sellado en el corte"
    assert len(set(cortes)) == 1, \
        "con el reloj congelado todos los cortes tienen que ser el mismo"
    assert set(cortes) == {sellado}, "y tienen que ser iguales al sello"
    assert len(dev.decisiones()) > 10, "hubo muchas vueltas, no una"

    vistos = sum(d["n_nuevos"] for d in dev.decisiones())
    assert vistos == 0, (
        "el borde se arregló: borrar este test y poner el que pidió Opus "
        "—un mensaje sellado en el corte aparece en alguna vuelta—"
    )


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
