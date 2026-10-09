"""
test_fixes_vivos.py — los cinco fixes medidos en los vivos 01 y 02

F1  el endpoint REST y la tool MCP devuelven lo mismo (no era bug: era la ruta)
F2  clock_log legible desde afuera del proceso del server
F3a estado de partida aislable por vivo, con default igual al de hoy
F3b los mensajes SYSTEM NO entran al corpus (delamor: "no, nunca")
F4  "system" no cuenta como agente
F5  ritmo observado junto al declarado

Sin claves ni red: el canal y el monitor se usan en proceso.
"""

from __future__ import annotations

import asyncio
import json
import sys
import tempfile
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom.channel import RELOJ_CANAL, TICK_PERIODO_S, ChatChannel  # noqa: E402


class _Msg:
    """Un mensaje del canal, con su tipo. El tipo es lo que F3b/F4 miran."""

    def __init__(self, text: str, device_id: str = "d1", device_type: str = "AI"):
        self.text, self.device_id, self.device_type = text, device_id, device_type


TEXTOS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
]


@pytest.fixture
def canal(monkeypatch):
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


@pytest.fixture
def monitor(monkeypatch):
    """CKMMonitor con `state_dir` propio: nada toca el _state del repo."""
    import iap_chatroom.ckm_monitor as mod
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    d = Path(tempfile.mkdtemp())
    return mod.CKMMonitor(min_texts=5, state_dir=d), d


# ── F3a — el estado se puede aislar, y el default no cambia ────────────────

def test_el_state_dir_por_defecto_es_el_de_siempre(monkeypatch) -> None:
    """Quien no lo pase no ve ningún cambio."""
    import iap_chatroom.ckm_monitor as mod
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    d = Path(tempfile.mkdtemp())
    monkeypatch.setattr(mod, "_STATE_DIR", d)
    cm = mod.CKMMonitor(min_texts=5)
    assert cm.state_dir == d


def test_el_state_dir_se_puede_declarar_por_vivo(monitor) -> None:
    cm, d = monitor
    assert cm.state_dir == d
    assert (d / "monitor_trajectory.jsonl").parent == d
    cm.on_message(_Msg(TEXTOS[0]))
    assert (d / "corpus_state.json").exists(), \
        "el estado tiene que escribirse en el directorio declarado"


def test_dos_vivos_con_state_dir_distinto_no_se_acumulan(monkeypatch) -> None:
    """
    Lo que F3a vino a resolver: el corpus pasó de 10 a 12 textos entre el vivo
    01 y el 02 porque los dos escribían en el mismo `_state`.
    """
    import iap_chatroom.ckm_monitor as mod

    def nuevo():
        monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
        return mod.CKMMonitor(min_texts=5, state_dir=Path(tempfile.mkdtemp()))

    a = nuevo()
    for t in TEXTOS:
        a.on_message(_Msg(t))
    n_a = a._corpus.status()["n_texts"]
    assert n_a == len(TEXTOS)

    b = nuevo()
    assert b._corpus.status()["n_texts"] == 0, \
        "el segundo vivo arrancó con el corpus del primero"


# ── F3b — SYSTEM nunca entra al corpus (delamor: "no, nunca") ─────────────

def test_un_mensaje_SYSTEM_no_entra_al_corpus(monitor) -> None:
    cm, d = monitor
    cm.on_message(_Msg("GroqGptOss20B_1 joined the channel",
                       device_id="system", device_type="SYSTEM"))
    assert cm._corpus.status()["n_texts"] == 0, \
        "el join entró al corpus: es lo que delamor dijo que nunca pasa"
    assert cm._message_count == 1, \
        "pero sigue contándose como mensaje del canal"


def test_los_mensajes_AI_y_HUMAN_si_entran(monitor) -> None:
    cm, d = monitor
    cm.on_message(_Msg(TEXTOS[0], device_type="AI"))
    cm.on_message(_Msg(TEXTOS[1], device_id="h1", device_type="HUMAN"))
    assert cm._corpus.status()["n_texts"] == 2


def test_el_corpus_de_un_vivo_no_tiene_joins(monitor) -> None:
    """
    El escenario de los dos vivos: dos joins y después textos. Antes, 8 de 12
    textos del corpus eran "X joined the channel".
    """
    cm, d = monitor
    cm.on_message(_Msg("A joined the channel", device_id="system",
                       device_type="SYSTEM"))
    cm.on_message(_Msg("B joined the channel", device_id="system",
                       device_type="SYSTEM"))
    for t in TEXTOS:
        cm.on_message(_Msg(t))

    textos = json.loads((d / "corpus_state.json").read_text())["texts"]
    assert len(textos) == len(TEXTOS)
    assert not any("joined the channel" in x for x in textos), \
        "un join llegó al corpus"
    assert cm._message_count == len(TEXTOS) + 2


# ── F4 — "system" no cuenta como agente ───────────────────────────────────

def test_system_no_cuenta_como_agente(monitor) -> None:
    """
    En los dos vivos `n_agentes` dio **1**, y ese 1 era el canal: los únicos
    mensajes fueron los joins, cuyo device_id es "system".
    """
    cm, d = monitor
    cm.on_message(_Msg("A joined the channel", device_id="system",
                       device_type="SYSTEM"))
    cm.on_message(_Msg("B joined the channel", device_id="system",
                       device_type="SYSTEM"))
    assert cm._devices_seen == set(), "el canal se contó como participante"
    assert cm.get_state()["n_agentes"] == 0, \
        "con dos devices que no publicaron, los agentes vistos son 0"


def test_los_devices_que_publican_si_cuentan(monitor) -> None:
    cm, d = monitor
    cm.on_message(_Msg("A joined the channel", device_id="system",
                       device_type="SYSTEM"))
    cm.on_message(_Msg(TEXTOS[0], device_id="d1"))
    cm.on_message(_Msg(TEXTOS[1], device_id="d2"))
    cm.on_message(_Msg(TEXTOS[2], device_id="d1"))
    assert cm._devices_seen == {"d1", "d2"}
    assert cm.get_state()["n_agentes"] == 2


# ── F2 — clock_log legible desde afuera ───────────────────────────────────

def test_clock_log_sigue_devolviendo_la_lista(canal) -> None:
    """El fix era aditivo: no se le cambió la firma al método que ya existía."""
    canal.get_clock()
    log = canal.clock_log()
    assert isinstance(log, list) and log


def test_clock_log_desde_lleva_el_total_aparte(canal, monkeypatch) -> None:
    reloj = {"t": canal._t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))
    for _ in range(5):
        canal.get_clock()
        reloj["t"] += TICK_PERIODO_S * 1.5

    p = canal.clock_log_desde()
    assert p["total"] == 5 and p["devueltas"] == 5
    assert p["periodo_s"] == TICK_PERIODO_S and p["reloj"] == RELOJ_CANAL
    assert [e["tick"] for e in p["entradas"]] == sorted(
        e["tick"] for e in p["entradas"]
    )


def test_clock_log_desde_pagina_sin_perder_la_cuenta(canal, monkeypatch) -> None:
    reloj = {"t": canal._t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))
    for _ in range(6):
        canal.get_clock()
        reloj["t"] += TICK_PERIODO_S * 2

    todos = canal.clock_log_desde()
    corte = todos["entradas"][3]["tick"]
    p = canal.clock_log_desde(desde_tick=corte)
    assert p["total"] == 6, "el total tiene que ser el del log, no el de la página"
    assert p["devueltas"] == 3
    assert all(e["tick"] >= corte for e in p["entradas"])


def test_la_tool_mcp_get_clock_log_devuelve_lo_del_canal(canal, monkeypatch) -> None:
    from iap_chatroom import mcp_server
    monkeypatch.setattr(mcp_server, "channel", canal)
    canal.get_clock()
    fn = getattr(mcp_server.get_clock_log, "fn", mcp_server.get_clock_log)
    p = asyncio.run(fn())
    assert p["total"] == len(canal.clock_log())
    assert p["reloj"] == RELOJ_CANAL


def test_el_endpoint_del_clock_log_devuelve_lo_mismo_que_la_tool(canal, monkeypatch) -> None:
    from iap_chatroom import api_routes, mcp_server
    monkeypatch.setattr(api_routes, "channel", canal)
    monkeypatch.setattr(mcp_server, "channel", canal)
    canal.get_clock()
    fn_t = getattr(mcp_server.get_clock_log, "fn", mcp_server.get_clock_log)
    assert asyncio.run(api_routes.get_clock_log()) == asyncio.run(fn_t())


def test_el_log_leido_desde_afuera_crece_con_el_canal_callado(canal, monkeypatch) -> None:
    """
    El test de F2: **con el canal callado, el log leído desde afuera crece.**
    Reloj controlado, no `sleep`.
    """
    from iap_chatroom import mcp_server
    monkeypatch.setattr(mcp_server, "channel", canal)
    fn = getattr(mcp_server.get_clock_log, "fn", mcp_server.get_clock_log)
    reloj = {"t": canal._t0}
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: reloj["t"]))

    totales = []
    for _ in range(4):
        canal.get_clock()
        totales.append(asyncio.run(fn())["total"])
        reloj["t"] += TICK_PERIODO_S * 1.5

    assert len(canal.messages) == 0, "el canal tiene que estar callado"
    assert totales == sorted(totales) and totales[-1] > totales[0], \
        f"el log no creció con el canal callado: {totales}"
    assert all(not e["con_mensajes"] for e in asyncio.run(fn())["entradas"])


# ── F1 — el endpoint y la tool coinciden (no era bug: era la ruta) ────────

def test_el_endpoint_monitor_y_la_tool_devuelven_lo_mismo(monitor, monkeypatch) -> None:
    """
    F1 no era un bug del canal: la ruta es `/api/monitor`, y el vivo 02 usó
    `/api/monitor/state`, que da 404. El `.get(k)` sobre el cuerpo del 404
    devolvía None por campo, y eso se reportó como bug.
    """
    from iap_chatroom import api_routes, mcp_server
    cm, d = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    monkeypatch.setattr(api_routes, "ckm_monitor", cm)
    monkeypatch.setattr(mcp_server, "ckm_monitor", cm)

    fn_t = getattr(mcp_server.get_monitor_state, "fn", mcp_server.get_monitor_state)
    assert asyncio.run(api_routes.get_monitor_state()) == asyncio.run(fn_t())


def test_la_ruta_del_monitor_es_monitor_y_no_monitor_state() -> None:
    """La ruta, leída del router: es lo único que faltaba saber en el vivo 02."""
    from iap_chatroom.api_routes import router
    rutas = {r.path for r in router.routes}
    assert "/monitor" in rutas
    assert "/monitor/state" not in rutas, \
        "si esta ruta existiera, el reporte del vivo 02 habría sido correcto"


# ── la firma: n_agentes es el conteo real, 0 si no hubo ───────────────────

def test_con_cero_devices_la_firma_dice_0(monitor) -> None:
    """
    **delamor, 9 oct: `n_agentes` en la firma es el conteo real.**

    Antes había dos `1`: el `or 1` de `ckm_monitor.py` y el default `= 1` de
    `FirmaService.firmar`. Con cero devices vistos la firma certificaba **un**
    agente — NOMINAL por ausencia en lo que certifica el estado estructural.

    Verificado antes de sacarlos: **nada divide por `n_agentes`** en el repo.
    Sólo se guarda (`firma_ckm.py:132`) y se lee.
    """
    cm, d = monitor
    # sólo joins: ningún device publicó, así que no hay agentes vistos
    cm.on_message(_Msg("A joined the channel", device_id="system",
                       device_type="SYSTEM"))
    cm.on_message(_Msg("B joined the channel", device_id="system",
                       device_type="SYSTEM"))
    # y textos reales de otro origen, para que W exista y la firma se pueda emitir
    for t in TEXTOS:
        cm.on_message(_Msg(t, device_id="d1"))
    cm._devices_seen.clear()          # se simula el caso: cero agentes vistos

    f = cm.get_firma()
    assert f is not None, "el test necesita que la firma se pueda emitir"
    assert f["n_agentes"] == 0, \
        "la firma certificó un agente que no existió"


def test_firmar_sin_n_agentes_levanta_TypeError() -> None:
    """
    **Opus, 9 oct: `n_agentes` es obligatorio y no tiene default.**

    Hasta ayer el default era `1` y la firma certificaba un agente que no
    existió. Ponerlo en `0` arreglaba el número y dejaba el hueco: el `0` que
    nadie pasó es tan inventado como el `1`. Un default no es un conteo.

    Este test reemplaza a `test_el_default_de_firmar_es_0_no_1`, que afirmaba
    algo más débil — que el default fuera 0 — y que ahora sería falso.
    """
    import inspect

    from firma_ckm import FirmaService
    sig = inspect.signature(FirmaService.firmar)
    assert sig.parameters["n_agentes"].default is inspect.Parameter.empty, \
        "n_agentes volvió a tener default; un default no es un conteo"

    # y el TypeError de verdad, no sólo la firma inspeccionada
    with pytest.raises(TypeError):
        FirmaService().firmar(object(), object())


def test_nada_divide_por_n_agentes() -> None:
    """
    La condición que delamor puso antes de sacar los dos `1`: si algo dividiera
    por `n_agentes`, un 0 cambiaría de "dato honesto" a `ZeroDivisionError`.

    Se verifica sobre el código vivo, no sobre `process/` (que es traza).
    """
    import re

    sospechoso = re.compile(r"/\s*\(?\s*(self\.)?n_agentes|n_agentes\s*\)?\s*\)?\s*$")
    for f in list((RAIZ / "services").glob("*.py")) + list(
        (RAIZ / "iap_chatroom").glob("*.py")
    ):
        for i, linea in enumerate(f.read_text().splitlines(), 1):
            if "n_agentes" not in linea:
                continue
            assert "/ n_agentes" not in linea and "/n_agentes" not in linea, \
                f"{f.name}:{i} divide por n_agentes: {linea.strip()}"
