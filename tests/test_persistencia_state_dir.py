"""
test_persistencia_state_dir.py — **todo junto en el mismo directorio**

Punto 3 de `TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md` (delamor):
*"IAP escribe todo en el mismo `state_dir` privado, sin lógica en los
drivers"*, append-only y **durante** la corrida, nombres en inglés, y los
archivos tienen que **sobrevivir a un corte a mitad de camino**.

### Lo que el texto enumera, y dónde se verifica cada cosa

| lo pedido | dónde |
|---|---|
| lo que ya iba (corpus, G, trayectoria, decisiones y estado de rebuild) | `test_lo_que_ya_iba_sigue_en_el_mismo_directorio` |
| el historial de versiones de W (*version manager*) | `test_el_historial_de_versiones_de_W_ya_esta_en_el_directorio` |
| mensajes del canal, con texto entero, id, device, tick, timestamp y reloj | `test_los_mensajes_del_canal_con_todo_lo_pedido` |
| intentos rechazados | `test_los_intentos_rechazados_quedan_escritos` |
| traza de decisiones de cada device | `test_la_traza_de_decisiones_queda_escrita` |
| registros del filtro de llamadas | `test_los_registros_del_filtro_quedan_escritos` |
| log de ticks del canal | `test_el_log_de_ticks_queda_escrito_incluido_el_silencio` |
| todos los logs | `test_todos_los_logs_quedan_escritos` |
| append-only y **durante** la corrida | `test_los_archivos_crecen_durante_la_corrida` |
| sobrevive a un corte a mitad de camino | `test_un_corte_a_mitad_de_camino_no_se_lleva_lo_escrito` |
| nombres en inglés | `test_los_nombres_de_los_archivos_estan_en_ingles` |
| sin lógica en los drivers | `test_el_driver_solo_pasa_el_state_dir` |
| lo de COCO sigue sin publicarse en el canal | `test_lo_de_coco_no_se_publica_en_el_canal` |

### El corte, medido y no simulado

*"Sobreviven a un corte a mitad de camino"* no se puede verificar con un
`try/except`: lo que puede fallar ahí es el buffer de Python, y un `except` lo
cierra igual. Así que el corte es **un `SIGKILL` a un subproceso de verdad**
(`test_un_corte_a_mitad_de_camino_no_se_lleva_lo_escrito`): el proceso escribe,
se lo mata con la señal que no se puede atrapar, y después se lee el archivo.
Sin el `flush()` de `run_store.append` ese test falla — está corrido por
inversión en `test_sin_flush_el_corte_se_lleva_las_lineas`.
"""

from __future__ import annotations

import asyncio
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from iap_chatroom import run_store                                # noqa: E402
from iap_chatroom.channel import ChatChannel, message_id          # noqa: E402
from iap_chatroom.ckm_monitor import CKMMonitor                   # noqa: E402
from iap_chatroom.autonomous_device import (                      # noqa: E402
    AutonomousDevice,
    DECISION_END_OF_CASE,
)
from iap_chatroom.local_criterion import (                        # noqa: E402
    LocalCriterion,
    LocalCriterionThresholds,
)

from test_oda_continuo import (                                   # noqa: E402
    ClientStub, ProviderStub, _correr, _device,
)
from test_serie2_caso0_cp1 import TEXTOS, _Msg                    # noqa: E402


@pytest.fixture
def state(tmp_path):
    """El `state_dir` de la corrida, fijado como lo fija un vivo."""
    d = tmp_path / "_state_caso"
    run_store.set_state_dir(d)
    return d


@pytest.fixture
def canal(monkeypatch):
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


@pytest.fixture
def monitor(tmp_path, monkeypatch):
    """
    Un `CKMMonitor` en su propio directorio. **Él es quien lo declara** para
    todo el proceso, así que después de este fixture el canal escribe ahí.
    """
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    monkeypatch.setattr(ChatChannel, "_instance", None)
    d = tmp_path / "_state_caso"
    return CKMMonitor(state_dir=d, min_texts=3)


# ── lo que ya iba, y el version manager ──────────────────────────────────────

def _alimentar(monitor) -> None:
    """
    El corpus, por el camino del canal (`on_message`), **con dos devices**.

    Dos y no uno porque `min_devices_first_W = 2`: con un solo device el
    corpus acumula y **W no se construye**, así que no hay trayectoria ni
    `corpus_G_state.json` que ver. Lo escribí con uno y los tests lo dijeron.
    """
    for i, t in enumerate(TEXTOS):
        monitor.on_message(_Msg("device_a" if i % 2 == 0 else "device_b", t))


def test_lo_que_ya_iba_sigue_en_el_mismo_directorio(monitor):
    """
    Los cinco que el texto lista como *"lo que ya va"*. Está acá para que el
    punto 3 no se cumpla moviendo lo nuevo a otro lado.
    """
    _alimentar(monitor)
    d = monitor.state_dir
    for f in ("corpus_state.json", "corpus_G_state.json",
              "monitor_trajectory.jsonl"):
        assert (d / f).exists(), f"falta {f} en {d}"
    # los dos del rebuild por decisión: sus rutas las declara el panel
    estado = monitor.get_state()
    assert Path(estado["rebuild_decisions_path"]).parent == d


def test_el_historial_de_versiones_de_W_ya_esta_en_el_directorio(monitor):
    """
    *"El historial de versiones de W (version manager)"*.

    **No hubo que agregar nada**, y eso es el hallazgo: ya viaja dentro de
    `corpus_state.json`, que `CorpusService` escribe en el `state_dir`
    (`w_version_history`, con `to_list()`/`from_list()`). Se verifica en vez de
    escribirlo de nuevo — un segundo archivo con lo mismo sería dos verdades
    sobre la misma W.
    """
    _alimentar(monitor)
    estado = json.loads((monitor.state_dir / "corpus_state.json").read_text())
    assert "w_version_history" in estado
    hist = estado["w_version_history"]
    assert hist, "el fixture no llegó a construir W: no hay historial que ver"
    for marca in hist:
        for clave in ("timestamp", "sha256", "corpus_size", "causal_event"):
            assert clave in marca, f"falta {clave} en la marca de W"


# ── lo que vivía en memoria ──────────────────────────────────────────────────

@pytest.mark.anyio
async def test_los_mensajes_del_canal_con_todo_lo_pedido(state, canal):
    """
    *"Mensajes del canal, con texto entero, id, device, tick, timestamp y
    reloj"*. Las seis cosas, y el texto **entero**: no truncado.
    """
    largo = "water " * 400
    await canal.publish("device_a", "AI", largo)
    await canal.publish("device_b", "AI", "who pays for it")

    lineas = run_store.read(run_store.CHANNEL_MESSAGES, state)
    assert len(lineas) == 2
    assert lineas[0]["text"] == largo, "el texto no quedó entero"
    assert lineas[0]["message_id"] == message_id(0)
    assert lineas[1]["message_id"] == message_id(1)
    for ln, did in zip(lineas, ("device_a", "device_b")):
        assert ln["device_id"] == did
        assert ln["device_type"] == "AI"
        assert isinstance(ln["tick"], int)
        assert ln["timestamp"].endswith("+00:00")
        assert ln["reloj"] == "channel"


@pytest.mark.anyio
async def test_el_id_escrito_es_el_que_el_device_recibe(state, canal):
    """
    El id del archivo y el id que el device ve por `get_messages` salen de
    **la misma función**. Con la fórmula repetida en dos lugares podían
    separarse, y el id es lo que ata una línea del archivo a una decisión.
    """
    await canal.publish("device_a", "AI", "upstream")
    ln = run_store.read(run_store.CHANNEL_MESSAGES, state)[0]
    indice = len(canal.messages) - 1
    assert ln["message_id"] == message_id(indice)


@pytest.mark.anyio
async def test_los_intentos_rechazados_quedan_escritos(state, canal):
    """*"Intentos rechazados"*. Con quién, cuándo y qué se rechazó."""
    assert await canal.publish("device_a", "AI", "   ") is None
    assert await canal.publish("device_b", "AI", "") is None

    lineas = run_store.read(run_store.REJECTED_ATTEMPTS, state)
    assert len(lineas) == 2
    assert [ln["device_id"] for ln in lineas] == ["device_a", "device_b"]
    for ln in lineas:
        assert ln["reason"] == "empty_text"
        assert "received" in ln and "tick" in ln and "timestamp" in ln
    # y los dos vacíos se distinguen: uno tenía espacios y el otro no
    assert lineas[0]["length"] == 3 and lineas[1]["length"] == 0
    # el rechazo no dejó mensaje
    assert run_store.read(run_store.CHANNEL_MESSAGES, state) == []


def test_el_log_de_ticks_queda_escrito_incluido_el_silencio(state, canal):
    """
    *"Log de ticks del canal"*. Un tick observado **sin mensajes** es una
    entrada: el silencio entre mensajes es el dato que no se puede
    reconstruir desde los mensajes, y era lo único que medía el silencio y
    vivía sólo en memoria.
    """
    canal.get_clock()
    lineas = run_store.read(run_store.CHANNEL_TICKS, state)
    assert len(lineas) == 1
    assert lineas[0]["con_mensajes"] is False, "este tick fue de silencio"
    assert lineas[0]["reloj"] == "channel"
    assert lineas[0]["n_mensajes"] == 0
    # preguntar dos veces en el mismo tick no agrega una línea: el log es de
    # ticks, no de consultas
    canal.get_clock()
    assert len(run_store.read(run_store.CHANNEL_TICKS, state)) == 1
    assert len(run_store.read(run_store.CHANNEL_TICKS, state)) == \
        len(canal.clock_log())


def test_la_traza_de_decisiones_queda_escrita(state, canal):
    """*"Traza de decisiones de cada device"*, una línea por vuelta."""
    dev = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="device_a")
    dev._state_dir = state
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.05)

    lineas = run_store.read(run_store.DEVICE_DECISIONS, state)
    assert lineas, "no se escribió ninguna decisión"
    assert len(lineas) == len(dev.decisiones()), (
        "lo escrito no coincide con la traza en memoria"
    )
    for ln, mem in zip(lineas, dev.decisiones()):
        assert ln["vuelta"] == mem["vuelta"]
        assert ln["decision"] == mem["decision"]
        assert ln["device_id"] == "device_a", "la línea tiene que decir de quién es"


def test_los_registros_del_filtro_quedan_escritos(state, canal):
    """
    *"Registros del filtro de llamadas"*, con el motivo de cada skip — que es
    lo único que distingue un silencio decidido de uno que el filtro produjo.
    """
    dev = _device(
        ProviderStub(["OP_SILENCE"] * 20), device_id="device_a",
        local_criterion=LocalCriterion(
            umbrales=LocalCriterionThresholds(piso_vueltas=2)
        ),
    )
    dev._state_dir = state
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.08)

    lineas = run_store.read(run_store.CALL_FILTER_RECORDS, state)
    assert lineas, "no se escribió ningún registro del filtro"
    assert len(lineas) == len(dev.registros_criterio())
    for ln in lineas:
        for clave in ("llamar", "motivo", "via", "vuelta",
                      "umbrales_calibrados"):
            assert clave in ln, f"falta {clave} en el registro del filtro"


def test_todos_los_logs_quedan_escritos(state, canal):
    """
    *"Todos los logs"*. Lo que el device imprimía con `print` y se perdía en
    el scrollback de quien lanzó el vivo, más el principio y el fin del run.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="device_a")
    dev._state_dir = state
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.05)

    lineas = run_store.read(run_store.DEVICE_LOG, state)
    eventos = [ln["event"] for ln in lineas]
    assert "run_start" in eventos and "run_end" in eventos
    assert eventos.count("decision") == len(dev.decisiones()), (
        "cada decisión imprimida tiene que tener su línea"
    )
    fin = [ln for ln in lineas if ln["event"] == "run_end"][0]
    assert fin["costo"]["llamadas_llm"] == dev.costo()["llamadas_llm"]
    # y el panel del device declara dónde escribió
    assert dev.costo()["state_dir"] == str(state)
    assert dev.costo()["write_failures"] == 0


def test_los_errores_del_provider_quedan_escritos_en_el_momento(state, canal):
    """
    Un 429 que corta un vivo tiene que dejar escrito **el 429**. Hasta el
    punto 3 los errores sobrevivían sólo si el driver llegaba a volcar
    `costo()`: el vivo cortado por un error perdía el registro del error.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 20, falla_en={1}),
                  device_id="device_a")
    dev._state_dir = state
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.05)

    errores = [ln for ln in run_store.read(run_store.DEVICE_LOG, state)
               if ln["event"] == "provider_error"]
    assert errores, "el error del provider no quedó escrito"
    assert errores[0]["fase"] in ("decide", "generate")
    assert "rate_limit" in errores[0] and "rate_limit_segun" in errores[0]


# ── append-only, durante la corrida ──────────────────────────────────────────

def test_los_archivos_crecen_durante_la_corrida(state, canal):
    """
    *"Append-only y durante la corrida, no sólo al final"*.

    Se mide **mientras el device corre**, no después: el gancho
    `publicados_entre` del `ClientStub` corre entre `get_clock` y
    `get_messages` de una vuelta, y ahí se lee el archivo. Si la escritura
    fuera un volcado al final, en ese momento el archivo no existiría.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="device_a")
    dev._state_dir = state
    cliente = ClientStub(canal, device_id="device_a")

    visto: list[int] = []

    def mirar():
        visto.append(len(run_store.read(run_store.DEVICE_LOG, state)))

    cliente.publicados_entre = mirar
    _correr(dev, cliente, duration=0.05)

    assert visto, "el gancho no corrió: el test no midió nada"
    assert visto[0] >= 1, (
        "en plena vuelta el log ya tiene que tener el run_start escrito"
    )
    # y al final tiene más: creció, no se escribió de una sola vez
    assert len(run_store.read(run_store.DEVICE_LOG, state)) > visto[0]


def test_append_only_lo_escrito_no_se_reescribe(state, canal):
    """Las líneas viejas no se tocan: el archivo sólo crece por el final."""
    run_store.append(run_store.DEVICE_LOG, {"event": "primera"}, state)
    primera = (state / run_store.DEVICE_LOG).read_text()
    run_store.append(run_store.DEVICE_LOG, {"event": "segunda"}, state)
    segunda = (state / run_store.DEVICE_LOG).read_text()
    assert segunda.startswith(primera), "la línea anterior se reescribió"
    assert len(run_store.read(run_store.DEVICE_LOG, state)) == 2


# ── el corte ─────────────────────────────────────────────────────────────────

_GUION_DEL_CORTE = '''
import sys, time
sys.path.insert(0, {raiz!r})
from iap_chatroom import run_store
run_store.set_state_dir({dir!r})
for i in range(10000):
    run_store.append(run_store.DEVICE_LOG, {{"event": "tick", "i": i}})
    print(i, flush=True)
    time.sleep(0.005)
'''


def test_un_corte_a_mitad_de_camino_no_se_lleva_lo_escrito(tmp_path):
    """
    **El corte, de verdad: `SIGKILL` a un subproceso.**

    `SIGKILL` no se puede atrapar ni diferir, así que el proceso muere sin
    cerrar el archivo y sin correr ningún `finally`. Lo que quede en disco es
    exactamente lo que el `flush()` bajó. Un `try/except` no mediría esto: el
    `except` corre dentro del mismo proceso y el cierre del archivo pasa igual.
    """
    d = tmp_path / "_state_corte"
    guion = tmp_path / "escribiendo.py"
    guion.write_text(_GUION_DEL_CORTE.format(raiz=str(RAIZ), dir=str(d)))

    p = subprocess.Popen([sys.executable, str(guion)],
                         stdout=subprocess.PIPE, text=True)
    try:
        # Se espera a que haya escrito unas cuantas, leyendo su stdout: así el
        # test no depende de un `sleep` calibrado a ojo.
        for _ in range(12):
            if p.stdout.readline() == "":
                break
        os.kill(p.pid, signal.SIGKILL)
    finally:
        p.wait(timeout=10)

    assert p.returncode == -signal.SIGKILL, (
        f"el proceso no murió por SIGKILL: returncode={p.returncode}"
    )
    lineas = run_store.read(run_store.DEVICE_LOG, d)
    assert len(lineas) >= 10, (
        f"el corte se llevó lo escrito: sólo {len(lineas)} líneas"
    )
    # Y lo que quedó es legible: líneas JSON completas, no una cortada al
    # medio. Si hubiera una cortada, `read` la devuelve como `_unparsed`.
    assert all("_unparsed" not in ln for ln in lineas), (
        f"quedó una línea partida: {[l for l in lineas if '_unparsed' in l]}"
    )
    assert [ln["i"] for ln in lineas] == list(range(len(lineas))), (
        "las líneas no quedaron en orden ni completas"
    )


_GUION_SIN_FLUSH = '''
import json, sys, time
sys.path.insert(0, {raiz!r})
from pathlib import Path
d = Path({dir!r}); d.mkdir(parents=True, exist_ok=True)
f = open(d / "sin_flush.jsonl", "a")
for i in range(10000):
    f.write(json.dumps({{"i": i}}) + "\\n")     # sin flush, a propósito
    print(i, flush=True)
    time.sleep(0.005)
'''


def test_sin_flush_el_corte_se_lleva_las_lineas(tmp_path):
    """
    **Por inversión: el `flush()` es lo que hace pasar al test de arriba.**

    El mismo guión sin el `flush()`. Si esto también sobreviviera, el test del
    corte estaría pasando por otra razón y no mediría el mecanismo.
    """
    d = tmp_path / "_state_sin_flush"
    guion = tmp_path / "sin_flush.py"
    guion.write_text(_GUION_SIN_FLUSH.format(raiz=str(RAIZ), dir=str(d)))

    p = subprocess.Popen([sys.executable, str(guion)],
                         stdout=subprocess.PIPE, text=True)
    try:
        for _ in range(12):
            if p.stdout.readline() == "":
                break
        os.kill(p.pid, signal.SIGKILL)
    finally:
        p.wait(timeout=10)

    ruta = d / "sin_flush.jsonl"
    quedaron = len(ruta.read_text().splitlines()) if ruta.exists() else 0
    assert quedaron == 0, (
        f"sin flush quedaron {quedaron} líneas: el buffer de Python alcanzó "
        f"para bajarlas, y entonces el test del corte no mide el flush"
    )


# ── las reglas ───────────────────────────────────────────────────────────────

def test_los_nombres_de_los_archivos_estan_en_ingles():
    """
    *"Nombres en inglés"*. Los de los archivos que nacen acá. Las claves que
    vienen de otro módulo viajan como ese módulo las nombró — está declarado
    en el docstring de `run_store`, y el test lo fija para que no se cambie
    sin querer.
    """
    castellano = ("mensaje", "canal", "device_decisiones", "decisiones",
                  "intentos", "rechazados", "registros", "criterio", "reloj")
    for f in run_store.ARCHIVOS:
        assert f.endswith(".jsonl"), f
        for palabra in castellano:
            assert palabra not in f, f"{f} tiene {palabra!r}"
    assert set(run_store.ARCHIVOS) == {
        "channel_messages.jsonl", "rejected_attempts.jsonl",
        "channel_ticks.jsonl", "device_decisions.jsonl",
        "call_filter_records.jsonl", "device_log.jsonl",
    }


def test_el_driver_solo_pasa_el_state_dir(state, canal):
    """
    *"Sin lógica en los drivers"*. Lo único que hace quien lanza el caso es
    pasar el directorio: la decisión de qué se escribe y cuándo está en IAP.

    Se mide así: un device construido **sólo** con `state_dir=` deja los tres
    archivos del device, sin que nadie llame a nada más.
    """
    dev = AutonomousDevice(
        device_id="device_a",
        provider=ProviderStub(["OP_SILENCE"] * 20),
        system_prompt="You are device_a.",
        poll_interval=0.0,
        state_dir=state,
        local_criterion=LocalCriterion(
            umbrales=LocalCriterionThresholds(piso_vueltas=2)
        ),
    )
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.08)
    for f in (run_store.DEVICE_DECISIONS, run_store.CALL_FILTER_RECORDS,
              run_store.DEVICE_LOG):
        assert (state / f).exists(), f"el device no escribió {f}"


def test_un_device_sin_state_dir_no_escribe_en_ninguna_parte(canal, tmp_path):
    """
    `None` es *"nadie lo pidió"*, igual que en `startup`. Un device de un test
    unitario no deja archivos por ahí — que es cómo aparecieron
    `channel_messages.jsonl` y `channel_ticks.jsonl` en el `_state` del repo
    mientras escribía esto (ver `conftest.py`).
    """
    run_store.set_state_dir(None)
    dev = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="device_a")
    assert dev._state_dir is None
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.03)
    assert dev.decisiones(), "el device tiene que haber corrido igual"
    assert dev.costo()["state_dir"] is None
    assert list(tmp_path.iterdir()) == []


def test_una_falla_de_escritura_no_mata_la_corrida_y_queda_registrada(
    canal, tmp_path
):
    """
    Un disco que no acepta la línea no puede matar un vivo de 70 mensajes.
    Pero tampoco se traga: queda en `failures()` con su archivo y su
    excepción, y el panel del device lo publica.
    """
    imposible = tmp_path / "archivo_no_directorio"
    imposible.write_text("no soy un directorio")
    dev = _device(ProviderStub(["OP_SILENCE"] * 20), device_id="device_a")
    dev._state_dir = imposible

    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.03)

    assert dev.decisiones(), "la corrida siguió"
    fallas = run_store.failures()
    assert fallas, "la falla de escritura se tragó"
    assert fallas[0]["file"] in run_store.ARCHIVOS
    assert "exception" in fallas[0] and "message" in fallas[0]
    assert dev.costo()["write_failures"] == len(fallas)


def test_lo_de_coco_no_se_publica_en_el_canal(monitor):
    """
    *"Lo de COCO sigue sin publicarse en el canal"*. Queda en
    `monitor_trajectory.jsonl`, como hoy. El punto 3 mueve a disco lo que
    vivía en memoria; **no** mueve al canal lo que es de Monitor.
    """
    _alimentar(monitor)
    assert (monitor.state_dir / "monitor_trajectory.jsonl").exists()

    textos = " ".join(m.text for m in ChatChannel().get_history())
    for palabra in ("coco", "COCO", "D_ckm", "beta_c", "mu_W", "Delta_r"):
        assert palabra not in textos, f"{palabra} se publicó en el canal"
    # y los mensajes escritos tampoco lo traen: el archivo del canal es del
    # canal, no un segundo panel
    for ln in run_store.read(run_store.CHANNEL_MESSAGES, monitor.state_dir):
        assert "coco" not in json.dumps(ln)


def test_el_directorio_lo_declara_el_monitor_una_sola_vez(tmp_path, monkeypatch):
    """
    Quién fija el directorio del proceso: `CKMMonitor.__init__`, con el mismo
    valor que usa para el corpus. Si cada parte de IAP resolviera el suyo
    podrían quedar distintos y el log de un vivo quedaría repartido — que es
    el problema que F3a ya encontró una vez.
    """
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    monkeypatch.setattr(ChatChannel, "_instance", None)
    run_store.set_state_dir(None)
    assert run_store.state_dir() is None

    d = tmp_path / "_state_caso"
    m = CKMMonitor(state_dir=d, min_texts=3)
    assert run_store.state_dir() == d == m.state_dir


# ── la forma de la traza, que el punto 3 vuelve visible ──────────────────────

def test_la_fila_del_fin_del_caso_tiene_las_mismas_claves_que_una_vuelta(
    state, canal
):
    """
    **Un JSONL con filas de forma distinta no se puede leer.**

    `END_OF_CASE` escribía siete claves y una vuelta completa dieciocho, y los
    consumidores de `decisiones()` leen las otras once: `sum(d["n_nuevos"])`,
    `all(d["llamadas_llm"] == 1)`. Con esa fila adentro cada uno levanta
    `KeyError`.

    **No lo vi antes porque la rama casi nunca corría**: el corte por fin de
    caso pide que la vuelta tarde más que lo que queda, y con stubs una vuelta
    era demasiado rápida. Lo destapó el punto 3 — con las escrituras puestas,
    `test_un_mensaje_sellado_en_el_corte_no_se_pierde` falló 2 de 6 corridas;
    en HEAD, 8 de 8 verdes. El defecto es anterior, el disparador es mío.

    Lo que no se sabe va `None`, no 0: una vuelta cortada no observó cero
    mensajes, no se sabe cuántos observó.
    """
    class ProviderLento(ProviderStub):
        """
        Un provider que tarda **cediendo el loop**.

        Con `time.sleep` no sirve: bloquea el hilo, el `wait_for` de `run` no
        llega a dispararse y la vuelta nunca se corta. Lo escribí así y el
        test dijo *"necesita una vuelta cortada"*. Tiene que ser
        `asyncio.sleep`, que es además lo que hace un provider de verdad
        esperando la red.
        """

        async def complete(self, messages):
            await asyncio.sleep(0.05)
            return await super().complete(messages)

    dev = _device(ProviderLento(["OP_SILENCE"] * 20), device_id="device_a")
    dev._state_dir = state
    _correr(dev, ClientStub(canal, device_id="device_a"), duration=0.02)

    ds = dev.decisiones()
    cortadas = [d for d in ds if d["decision"] == DECISION_END_OF_CASE]
    assert cortadas, "el test necesita una vuelta cortada por fin de caso"
    completas = [d for d in ds if d["decision"] != DECISION_END_OF_CASE]

    esperadas = {
        "vuelta", "tick", "tick_observation", "tick_action", "action_result",
        "tick_anterior", "reloj", "n_nuevos", "trigger", "decision",
        "trigger_mode", "criterio_motivo", "criterio_via",
        "umbrales_calibrados", "ventana", "llamadas_llm", "errores_llm",
        "ilegibles",
    }
    assert set(cortadas[0]) == esperadas, set(cortadas[0]) ^ esperadas
    if completas:
        assert set(completas[0]) == set(cortadas[0])

    # lo no sabido, declarado ausente y no en cero
    assert cortadas[0]["n_nuevos"] is None
    assert cortadas[0]["llamadas_llm"] is None
    assert cortadas[0]["ventana"] == "UNKNOWN"

    # y la fila escrita tiene la misma forma que la de memoria
    escritas = run_store.read(run_store.DEVICE_DECISIONS, state)
    cortada_escrita = [e for e in escritas
                       if e["decision"] == DECISION_END_OF_CASE]
    assert cortada_escrita, "la vuelta cortada no quedó escrita"
    assert esperadas <= set(cortada_escrita[0])
