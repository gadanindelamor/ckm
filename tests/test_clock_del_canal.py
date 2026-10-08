"""
test_clock_del_canal.py — CP1 de TASK_canal_iap_clock_iniciativa_v2

Las tres decisiones de delamor (8 oct, E3):
  1. el canal genera los ticks con su propio reloj, el mismo que sella mensajes;
  2. la Config **registra** el tick; el canal no lee la Config;
  3. cada tiempo declara de qué reloj viene.

El test que más importa es el del canal callado: el CLOCK existe justamente para
que el silencio sea dato, y `message_id` no servía porque avanza sólo con
mensajes.
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
sys.path.insert(0, str(RAIZ))
from ckm_landscape_config import CKMlandscapeConfig        # noqa: E402
from iap_chatroom.channel import (                          # noqa: E402
    RELOJ_CANAL,
    TICK_PERIODO_S,
    ChatChannel,
)


@pytest.fixture
def canal(monkeypatch):
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


# ── decisión 1: el canal genera, con su propio reloj ───────────────────────

def test_los_ticks_son_monotonos(canal) -> None:
    vistos = [canal.tick() for _ in range(40)]
    assert all(b >= a for a, b in zip(vistos, vistos[1:])), \
        f"el tick retrocedió: {vistos}"


def test_un_canal_sin_mensajes_tambien_avanza_ticks(canal) -> None:
    """
    El test del CP1. `message_id = "msg-{index}"` falla acá por construcción:
    avanza sólo con mensajes.
    """
    t0 = canal.tick()
    assert len(canal.messages) == 0, "el test necesita el canal callado"
    time.sleep(TICK_PERIODO_S * 1.2)
    t1 = canal.tick()
    assert len(canal.messages) == 0, "nadie publicó durante la espera"
    assert t1 > t0, f"el canal callado no avanzó: {t0} → {t1}"


def test_el_tick_no_depende_de_que_alguien_pregunte(canal) -> None:
    """Se deriva del reloj, no se incrementa en una consulta."""
    t0 = canal.tick()
    time.sleep(TICK_PERIODO_S * 1.2)          # sin llamar a tick() en el medio
    assert canal.tick() > t0


def test_el_tick_sale_del_mismo_reloj_que_sella_los_mensajes(canal, monkeypatch) -> None:
    """
    Decisión 1: una sola fuente. Si el tick saliera de otro reloj
    (`time.time()`, `monotonic`), este test falla.
    """
    import asyncio

    falso = canal._t0 + TICK_PERIODO_S * 7.5
    monkeypatch.setattr(ChatChannel, "_ahora", staticmethod(lambda: falso))

    m = asyncio.run(canal.publish("d0", "AI", "hola"))
    assert canal.tick() == 7
    assert m.tick == 7, "el tick del mensaje no sale del mismo reloj que el CLOCK"
    epoch_del_mensaje = datetime.fromisoformat(m.timestamp).timestamp()
    assert epoch_del_mensaje == pytest.approx(falso, abs=1e-6), \
        "el timestamp del mensaje no sale del reloj del canal"


def test_el_reloj_del_canal_es_el_de_pared_UTC(canal) -> None:
    """
    Decisión 1, la parte que faltaba: el reloj del canal es
    `datetime.now(timezone.utc)`, **no** `time.monotonic()` ni otro.

    Lo encontré invirtiendo: cambiando `_ahora()` a `time.monotonic()` pasaban
    los 302 tests. El test de arriba compara que el tick y el mensaje salgan
    del **mismo** `_ahora`, y con monotonic siguen siendo consistentes entre
    sí — consistentes y equivocados. Lo que no estaba protegido era que
    `_ahora` sea el reloj que sella los mensajes.

    Dos aserciones, y la segunda es la que no se puede falsear con un reloj
    arbitrario: el ISO del mensaje tiene que dar una fecha plausible. Con
    `monotonic` (segundos desde el arranque de la máquina) la fecha cae en
    1970.
    """
    import asyncio

    ahora_real = datetime.now(timezone.utc).timestamp()
    assert canal._ahora() == pytest.approx(ahora_real, abs=5.0), \
        "_ahora() no es el reloj de pared UTC"

    m = asyncio.run(canal.publish("d0", "AI", "hola"))
    fecha = datetime.fromisoformat(m.timestamp)
    assert fecha.tzinfo is not None, "el timestamp tiene que llevar zona"
    assert fecha.year >= 2026, \
        f"el timestamp dio {fecha.isoformat()}: el reloj del canal no es de pared"
    assert fecha.utcoffset().total_seconds() == 0, "tiene que ser UTC"


def test_el_t0_del_canal_tambien_es_de_pared(canal) -> None:
    """
    El t=0 del CLOCK sale del mismo reloj. Si no, el tick vigente sería un
    número enorme o negativo desde el primer momento.
    """
    assert canal._t0 == pytest.approx(datetime.now(timezone.utc).timestamp(), abs=30.0)
    assert 0 <= canal.tick() < 60, f"tick inicial fuera de rango: {canal.tick()}"


# ── decisión 3: cada tiempo declara su reloj ───────────────────────────────

def test_el_clock_declara_su_reloj(canal) -> None:
    c = canal.get_clock()
    assert c["reloj"] == RELOJ_CANAL == "canal"
    assert c["periodo_s"] == TICK_PERIODO_S
    assert set(c) >= {"tick", "t", "reloj", "periodo_s", "t0"}


def test_el_mensaje_declara_su_reloj(canal) -> None:
    import asyncio
    m = asyncio.run(canal.publish("d0", "AI", "hola"))
    assert m.reloj == RELOJ_CANAL
    assert m.to_dict()["reloj"] == RELOJ_CANAL
    assert m.tick >= 0


def test_un_message_sin_reloj_dice_desconocido() -> None:
    """Los JSONL históricos no tienen estos campos: el default es UNKNOWN."""
    from iap_chatroom.channel import Message
    m = Message(device_id="d", device_type="AI", text="t", timestamp="2026-01-01T00:00:00+00:00")
    assert m.reloj == "desconocido"
    assert m.tick == -1


# ── el silencio queda como dato ────────────────────────────────────────────

def test_el_log_registra_los_ticks_sin_mensajes(canal) -> None:
    canal.get_clock()
    time.sleep(TICK_PERIODO_S * 1.2)
    canal.get_clock()
    log = canal.clock_log()
    assert len(log) >= 2, "cada tick observado tiene que quedar registrado"
    assert all(e["con_mensajes"] is False for e in log), \
        "nadie publicó: todos los ticks son de silencio"
    assert all(e["reloj"] == RELOJ_CANAL for e in log)
    ticks = [e["tick"] for e in log]
    assert ticks == sorted(ticks) and len(set(ticks)) == len(ticks), \
        "el log es de ticks, no de consultas: uno por tick, en orden"


def test_dos_consultas_en_el_mismo_tick_registran_una(canal) -> None:
    for _ in range(5):
        canal.get_clock()
    assert len(canal.clock_log()) == 1


def test_un_tick_con_mensajes_queda_marcado(canal) -> None:
    import asyncio
    asyncio.run(canal.publish("d0", "AI", "hola"))
    canal.get_clock()
    assert canal.clock_log()[-1]["con_mensajes"] is True


def test_el_clock_no_calcula_nada_por_el_device(canal) -> None:
    """
    §1: *"El canal no calcula nada por el device: no entrega 'ticks sin
    mensajes' ni 'quién habló último' ya procesados."*
    """
    c = canal.get_clock()
    for prohibido in ("ticks_sin_mensajes", "ultimo_hablante", "delta_t",
                      "quien_hablo_ultimo", "silencio"):
        assert prohibido not in c, f"el canal procesó {prohibido} por el device"


# ── get_messages sigue igual que antes ─────────────────────────────────────

def test_get_messages_sigue_funcionando_igual(canal) -> None:
    """El CP1 no toca el `since` del device: eso es el CP2."""
    import asyncio
    from iap_chatroom import mcp_server

    monkeypatch_canal = mcp_server.channel
    mcp_server.channel = canal
    try:
        asyncio.run(canal.publish("d0", "AI", "uno"))
        corte = canal._ahora()
        time.sleep(0.01)
        asyncio.run(canal.publish("d1", "AI", "dos"))

        todos = asyncio.run(mcp_server.get_messages(None))
        assert [m["text"] for m in todos] == ["uno", "dos"]
        assert [m["message_id"] for m in todos] == ["msg-0", "msg-1"]

        desde = asyncio.run(mcp_server.get_messages(corte))
        assert [m["text"] for m in desde] == ["dos"], \
            "el filtro since cambió de comportamiento"

        # las claves de antes siguen estando, y se agregan las nuevas
        assert set(todos[0]) >= {"device_id", "device_type", "text",
                                 "timestamp", "message_id"}
        assert {"tick", "reloj"} <= set(todos[0])
    finally:
        mcp_server.channel = monkeypatch_canal


def test_la_tool_get_clock_devuelve_lo_del_canal(canal) -> None:
    import asyncio
    from iap_chatroom import mcp_server
    anterior = mcp_server.channel
    mcp_server.channel = canal
    try:
        fn = getattr(mcp_server.get_clock, 'fn', mcp_server.get_clock)
        c = asyncio.run(fn())
        assert c["reloj"] == RELOJ_CANAL
        assert c["tick"] == canal.tick()
    finally:
        mcp_server.channel = anterior


# ── decisión 2: la Config registra; el canal no la lee ─────────────────────

def test_la_config_registra_el_tick_con_su_reloj() -> None:
    cfg = CKMlandscapeConfig(sampling_mode="uniform")
    assert cfg.tick is None, "sin canal no hay tick, y eso es UNKNOWN, no 0"
    assert cfg.tick_reloj is None
    cfg.registrar_tick(7, "canal")
    assert cfg.tick == 7 and cfg.tick_reloj == "canal"
    assert cfg.panel()["tick"] == 7
    assert cfg.panel()["tick_reloj"] == "canal"


def test_registrar_tick_no_abre_ciclos(W_corpus) -> None:
    """Dos ejes del mismo objeto: el tick avanza siempre, el ciclo no."""
    cfg = CKMlandscapeConfig.create(W_corpus, sampling_mode="uniform")
    antes = len(cfg.ciclos)
    for t in range(5):
        cfg.registrar_tick(t, "canal")
    assert len(cfg.ciclos) == antes, "un tick no puede abrir un ciclo"
    assert cfg.tick == 4


def test_el_canal_no_lee_la_config(canal) -> None:
    """
    Decisión 2: la dependencia no se invierte. `channel.py` no importa ni
    nombra la Config.
    """
    src = (RAIZ / "iap_chatroom" / "channel.py").read_text()
    assert "CKMlandscapeConfig" not in src
    assert "ckm_landscape_config" not in src
    assert not hasattr(canal, "_landscape_config")


def test_monitor_anota_el_tick_que_le_dan(W_corpus, tmp_path) -> None:
    """Monitor registra; no genera. Y sin clock el tick queda en None."""
    from corpus_service import CorpusService
    from monitor_service import MonitorService

    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest([
        "gun control reduces violence and saves lives",
        "the second amendment protects the right to bear arms",
        "background checks prevent criminals from buying weapons",
        "assault weapons bans reduce mass shootings",
        "gun rights are constitutional rights not subject to restriction",
    ])
    cfg = CKMlandscapeConfig.create(c.get_W(), sampling_mode="uniform", n_runs=10)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10, landscape_config=cfg)

    m.evaluate("gun control laws reduce violence")
    assert cfg.tick is None, "sin clock el tick queda UNKNOWN, no 0"

    m.evaluate("gun control laws reduce violence",
               clock={"tick": 42, "reloj": "canal"})
    assert cfg.tick == 42 and cfg.tick_reloj == "canal"


@pytest.fixture(scope="module")
def W_corpus():
    import numpy as np
    d = json.loads((RAIZ / "services" / "W_ckm_corpus_v2.json").read_text())
    return np.array(d["W"], dtype=float)


# ── el canal de punta a punta ──────────────────────────────────────────────

def test_el_canal_le_pasa_el_tick_a_la_config(monkeypatch) -> None:
    """Punta a punta: publicar en el canal deja el tick en la Config."""
    import asyncio
    import iap_chatroom.ckm_monitor as mod

    monkeypatch.setattr(mod, "_STATE_DIR", Path(tempfile.mkdtemp()))
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    monkeypatch.setattr(ChatChannel, "_instance", None)
    canal = ChatChannel()
    cm = mod.CKMMonitor(min_texts=5)
    canal.add_callback(cm.on_message)

    async def main():
        for t in ("gun control reduces violence and saves lives",
                  "the second amendment protects the right to bear arms",
                  "background checks prevent criminals from buying weapons",
                  "assault weapons bans reduce mass shootings",
                  "gun rights are constitutional rights not subject to restriction",
                  "mental health is the real cause of gun violence"):
            await canal.publish("d0", "AI", t)
    asyncio.run(main())

    assert cm._landscape_config.tick is not None, "el canal no le pasó el tick"
    assert cm._landscape_config.tick_reloj == RELOJ_CANAL
    assert cm._last_panel is not None
    assert canal.clock_log(), "el canal tiene que haber registrado ticks"
