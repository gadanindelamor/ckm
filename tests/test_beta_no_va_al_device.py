"""
test_beta_no_va_al_device.py — **el β de cada device no va a ningún device**

Punto 2 de `TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md` (delamor:
*"lo que NO VA AL DEVICE es β de device"*). Ni el suyo ni el de los otros.

### Qué es cada β, porque son tres y sólo uno está prohibido

- **β_i** — el de **un device**: `COCO.beta_i(device_id)`, uno por device, y
  vive en `beta_status()["devices"]`, que `MonitorService.panel()` publica en
  `panel["thermostat"]["beta"]`. **Éste es el que no va.**
- **β_collective** — la mediana de los β_i: `beta_status()["beta_collective"]`.
  Va con ellos, en el mismo bloque, y **tampoco va**: es una función de los
  β_i y nombrarla en el prompt sería publicar su agregado.
- **β_c** — el del **corpus**: sale de μ_W, no de ningún device, y el bloque
  `coco` del panel del canal lo lleva junto con μ_W. **Éste sí está**, y el
  CP1 lo pide ahí (`test_a_beta_c_infinito_se_muestra_y_no_se_oculta`).

Confundirlos haría que este test pasara prohibiendo lo que el CP1 exige, o
que fallara por el β que no es. Por eso cada uno se mira por su nombre y por
su valor.

### Qué se mide, y por qué el test puede fallar

El texto dice: *"Según la lectura de Opus ya es así. Si el test pasa, no se
toca código."* Un test que confirma una lectura **tiene que poder
desmentirla**, así que acá no se busca la ausencia de la palabra `beta` —eso
pasaría igual si los β_i no existieran—. Se hacen las dos cosas:

1. **se fuerza que haya β_i**, llamando a `register_device_eval` sobre el COCO
   vivo con tres device_id, y se verifica que
   `panel["thermostat"]["beta"]["devices"]` los trae con su valor; si no los
   trae, el test **falla** por fixture insuficiente y no por ausencia;
2. recién entonces se verifica que **ninguno de esos valores ni de esas claves**
   aparece en lo que el device recibe (`get_state()`) ni en su prompt
   (`GATE_PROMPT_CONTINUO` formateado por `_decide`, con ese mismo panel como
   campo, y el system prompt y el historial de `_generate`).

El inverso también está: `test_el_instrumento_agarra_un_beta_filtrado` inyecta
β_i en el panel a mano y comprueba que estos tests fallarían.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from iap_chatroom.channel import ChatChannel                      # noqa: E402
from iap_chatroom.ckm_monitor import CKMMonitor                   # noqa: E402

from test_oda_continuo import (                                   # noqa: E402
    ClientStub, ProviderStub, _correr, _device,
)
from test_serie2_caso0_cp1 import TEXTOS, _Msg                    # noqa: E402

# Los tres device_id a los que se les fuerza un β_i. Son los que después se
# buscan en el prompt: si el filtro fuera por nombre y no por valor, un
# device_id que no estuviera en el panel no probaría nada.
DEVICES = ("device_a", "device_b", "device_c")

# Los `fi` con los que se fuerza. Distintos entre sí **a propósito**: con el
# mismo fi los tres β_i serían el mismo número, y encontrarlo en el prompt no
# diría de quién es.
FI = (0.5, 0.25, 0.125)


@pytest.fixture
def monitor(tmp_path, monkeypatch):
    """
    Un `CKMMonitor` real, en su propio `state_dir`, con panel y con COCO.

    El corpus entra por `on_message`, que es el camino del canal, y no por
    `ingest`: lo que se mide es el panel que el device ve en vivo.
    """
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    monkeypatch.setattr(ChatChannel, "_instance", None)
    m = CKMMonitor(state_dir=tmp_path / "state", min_texts=3)
    for i, t in enumerate(TEXTOS):
        m.on_message(_Msg(DEVICES[i % len(DEVICES)], t))
    assert m._last_panel is not None, "el fixture necesita un panel evaluado"
    return m


@pytest.fixture
def con_beta_i(monitor):
    """
    El monitor del fixture **con β_i forzados y verificados**.

    `register_device_eval` es el camino público por el que Monitor le pasa a
    COCO el `fabrication_index` de cada device; acá se lo llama directo para
    no depender de que una corrida de 8 textos produzca rechazos.
    """
    coco = monitor._monitor._thermostat
    assert coco is not None, "el fixture necesita COCO"
    for did, fi in zip(DEVICES, FI):
        coco.register_device_eval(did, fi)

    # **Y una evaluación más, para que `_last_panel` se arme CON los β_i.**
    # `_last_panel` es lo que `get_state()` lee, y lo dejó la última
    # `evaluate`: sin este mensaje, el panel que el device ve sería anterior a
    # los β_i forzados y el test mediría un panel que no los tenía.
    monitor.on_message(_Msg(DEVICES[0], "the aqueduct upstream is the source"))

    beta = coco.beta_status()
    # **Si esto falla, falla el fixture, no el punto 2.** Sin β_i no hay nada
    # cuya ausencia verificar, y el test de abajo pasaría vacío.
    assert set(beta["devices"]) == set(DEVICES), (
        f"el fixture no produjo β_i por device: {beta}"
    )
    assert beta["beta_collective"] is not None
    # **Tres valores distintos y positivos**, sin decir cuáles.
    #
    # Acá tenía `== [2.0, 4.0, 8.0]`, que es `1/fi` para los tres `FI`. Lo
    # escribí contra la fórmula de `beta_i` y la corrida lo desmintió: la
    # evaluación del corpus del fixture **ya había registrado** sus propios
    # `fi` por device, así que `beta_i` promedia esos más los forzados y da
    # `[6.0, 12.0, 16.0]`. Lo que el fixture tiene que garantizar es que haya
    # un β_i por device y que **se distingan entre sí** —para que encontrar uno
    # en el prompt diga de quién es—, no un número que sale de repetir el
    # código en el test.
    vals = list(beta["devices"].values())
    assert all(v is not None and v > 0 for v in vals), beta
    assert len(set(vals)) == len(DEVICES), (
        f"los β_i no se distinguen entre sí: {beta}"
    )
    assert monitor._last_panel is not None
    return monitor


def _valores_prohibidos(monitor) -> list[str]:
    """
    Los β_i y el β_collective, como texto. Lo que no puede aparecer.

    Se buscan **los valores**, no la palabra: un panel que publicara el β_i
    bajo otra clave pasaría un test que sólo mirara nombres.
    """
    beta = monitor._monitor._thermostat.beta_status()
    vals = [repr(v) for v in beta["devices"].values()]
    vals += [repr(beta["beta_collective"])]
    return vals


# ── (1) el β_i existe y está donde Opus dijo ─────────────────────────────────

def test_beta_i_vive_en_el_panel_de_monitor_y_no_en_el_del_canal(con_beta_i):
    """
    La lectura de Opus, medida: `panel["thermostat"]["beta"]` lo tiene,
    `CKMMonitor.get_state()` no. Las dos mitades en el mismo test, porque la
    afirmación es que están en lugares distintos.
    """
    panel = con_beta_i._monitor.evaluate(
        "who pays for the new aqueduct", device_id=DEVICES[0]
    )
    assert "devices" in panel["thermostat"]["beta"]
    assert panel["thermostat"]["beta"]["devices"], "el panel de Monitor lo tiene"

    estado = con_beta_i.get_state()
    assert "thermostat" not in estado, (
        "el panel del canal publicaría el bloque entero, β_i incluido"
    )


def test_el_estado_que_recibe_un_device_no_trae_ningun_beta_i(con_beta_i):
    """
    `get_state()` es **literalmente** lo que `get_monitor_state` devuelve al
    device (`mcp_server.get_monitor_state`). Se serializa entero y se busca
    cada β_i por su valor y cada clave por su nombre.
    """
    estado = con_beta_i.get_state()
    crudo = json.dumps(estado, default=str)

    for v in _valores_prohibidos(con_beta_i):
        assert v not in crudo, f"β de device en el estado del device: {v}"
    for clave in ("beta_i", "beta_collective", "beta_status", "thermostat"):
        assert clave not in crudo, f"clave de β de device en el estado: {clave}"


def test_el_beta_c_del_corpus_si_esta_y_no_se_confunde_con_el_del_device(
    con_beta_i
):
    """
    **El que sí va.** β_c sale de μ_W, no de ningún device, y el CP1 lo pide en
    el bloque `coco`. Este test existe para que el punto 2 no se cumpla
    borrando lo que el CP1 exige.
    """
    coco = con_beta_i.get_state()["coco"]
    assert coco["connected"] is True
    assert "beta_c" in coco and "mu_W" in coco
    # y no es ninguno de los β_i
    assert repr(coco["beta_c"]) not in _valores_prohibidos(con_beta_i)


# ── (2) el prompt ────────────────────────────────────────────────────────────

class _ClientConPanelReal(ClientStub):
    """
    El `ClientStub` de `test_oda_continuo`, con **el panel de verdad** en
    `get_monitor_state`.

    El stub original devuelve un campo fijo con los cinco valores en `None`.
    Eso alcanza para el ODA y **no alcanza acá**: con un campo inventado, que
    el prompt no tenga β_i no dice nada del panel real. Se hereda en vez de
    duplicarse, para que el resto del transporte siga siendo el mismo.
    """

    def __init__(self, canal, monitor, device_id="device_a"):
        super().__init__(canal, device_id=device_id)
        self.monitor = monitor

    async def call_tool(self, nombre, args=None):
        if nombre == "get_monitor_state":
            class _R:
                def __init__(self, data): self.data = data
            self.llamadas.append(nombre)
            return _R(self.monitor.get_state())
        return await super().call_tool(nombre, args)


def _prompts_vistos(con_beta_i, monkeypatch) -> list[str]:
    """
    Todo lo que el provider recibió en una corrida: el gate de `_decide` y el
    historial de `_generate`, system prompts incluidos.

    El device corre de verdad —`run` → `_one_turn` → `_decide` → `_interact`—
    así que el prompt sale del código, no de una copia del `.format`.
    """
    monkeypatch.setattr(ChatChannel, "_instance", None)
    canal = ChatChannel()
    provider = ProviderStub(["INTERACT", "A first thing about the water."])
    dev = _device(provider, device_id="device_a")
    cliente = _ClientConPanelReal(canal, con_beta_i, device_id="device_a")
    _correr(dev, cliente, duration=0.05)

    assert provider.llamadas, "el device no llamó al provider: no hay prompt"
    return [m["content"] for llamada in provider.llamadas for m in llamada]


def test_el_prompt_del_device_no_trae_ningun_beta_i(con_beta_i, monkeypatch):
    """Ni el suyo ni el de los otros dos."""
    prohibidos = _valores_prohibidos(con_beta_i)
    for texto in _prompts_vistos(con_beta_i, monkeypatch):
        bajo = texto.lower()
        assert "beta" not in bajo, f"la palabra beta en el prompt: {texto!r}"
        assert "β" not in texto, f"β en el prompt: {texto!r}"
        for v in prohibidos:
            assert v not in texto, f"valor de β de device en el prompt: {v}"


def test_el_gate_no_tiene_ninguna_ranura_para_un_beta(con_beta_i):
    """
    Lo estructural: el gate interpola **cinco** campos del panel, y β no es
    ninguno. Mientras eso sea así, ningún panel puede filtrar β al prompt por
    más que lo publique.
    """
    from iap_chatroom.autonomous_device import GATE_PROMPT_CONTINUO

    assert "beta" not in GATE_PROMPT_CONTINUO.lower()
    import string
    ranuras = {n for _, n, _, _ in string.Formatter().parse(GATE_PROMPT_CONTINUO)
               if n}
    assert ranuras == {
        "d_ckm", "temp", "c_s", "fi", "delta_r",
        "tick", "clock_source", "tick_period_s", "previous_tick",
        "history", "n_new", "incoming",
    }, ranuras


# ── el inverso: el instrumento tiene que poder agarrarlo ─────────────────────

def test_el_instrumento_agarra_un_beta_filtrado(con_beta_i, monkeypatch):
    """
    **Por inversión.** Se filtra el bloque de β al panel del canal y se
    comprueba que los dos tests de arriba fallarían. Sin esto, "no hay β en el
    prompt" podría ser cierto por un detector que no mira.
    """
    beta = con_beta_i._monitor._thermostat.beta_status()
    estado_real = CKMMonitor.get_state

    def con_fuga(self):
        d = estado_real(self)
        d["thermostat"] = {"beta": beta}
        return d

    monkeypatch.setattr(CKMMonitor, "get_state", con_fuga)

    crudo = json.dumps(con_beta_i.get_state(), default=str)
    assert any(v in crudo for v in _valores_prohibidos(con_beta_i)), (
        "con la fuga puesta, el estado tendría que traer los β_i"
    )
    # y el prompt no: el gate no tiene ranura para β. Eso es la segunda
    # barrera, y queda declarado cuál de las dos protege qué.
    for texto in _prompts_vistos(con_beta_i, monkeypatch):
        assert "beta" not in texto.lower()
