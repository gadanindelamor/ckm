"""
test_criterio_local.py — CP2b de TASK_canal_iap_clock_iniciativa_v2

El criterio local: el filtro sin LLM que decide **si** se llama a D.

El test central es el del **silencio no absorbente**, y corre con la
**auditoría apagada** (`tasa_auditoria=0.0`) a propósito: con la auditoría
puesta, "el filtro llamó alguna vez" sale flaky y no distingue *un filtro
absorbente* de *una tirada de moneda*. Opus: *"la auditoría no puede ser lo
único que lo rompa: si no, la iniciativa queda en manos de la suerte."*

Hay dos tests que **afirman el agujero** en vez de taparlo:
`test_sin_piso_el_silencio_ES_absorbente` y
`test_la_auditoria_sola_puede_no_llamar_nunca`. Son la inversión escrita como
test: si el piso dejara de hacer falta, esos dos fallarían y habría que venir
a leerlos.

Todo con stubs. No hay providers ni red.
"""

from __future__ import annotations

import asyncio
import random
import sys
from pathlib import Path
from typing import List, Optional

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom.autonomous_device import AutonomousDevice           # noqa: E402
from iap_chatroom.channel import ChatChannel                          # noqa: E402
from iap_chatroom.criterio_local import (                             # noqa: E402
    DECISION_SKIP,
    MOTIVO_AUDITORIA,
    MOTIVO_PISO,
    MOTIVO_PRIMERA,
    MOTIVO_SIN_CAMBIO,
    VIA_AUDITORIA,
    VIA_CRITERIO,
    VIA_PISO,
    CriterioLocal,
    UmbralesCriterioLocal,
    divergencia_auditoria,
    dt_desde,
)
from iap_chatroom.providers.base import ChatMessage, Provider         # noqa: E402

from tests.test_oda_continuo import ClientStub, ProviderStub, _publicar_sync


# ── helpers ─────────────────────────────────────────────────────────────────

def _piso_fuera_del_horizonte(**kw) -> CriterioLocal:
    """
    Un filtro cuyo piso está **más lejos que la ventana que se observa**.

    `piso_vueltas <= 0` ya no se puede configurar (`ValueError`, Opus 9 oct), y
    además, con la guarda `> 0` afuera de `evaluar`, un `0` haría que el piso
    dispare **todas** las vueltas: lo contrario de apagarlo. Así que la absorción
    no se exhibe poniendo el piso en cero.

    Se exhibe así: **un piso fuera del horizonte es indistinguible de no tener
    piso.** Eso es más preciso que "sin piso el silencio es absorbente", y dice
    algo que el enunciado anterior no decía: que `piso_vueltas` sea finito **no
    alcanza** — tiene que caer dentro de la ventana que se mira. Eso es
    calibración, y es exactamente por qué los umbrales van declarados sin
    calibrar.
    """
    kw.setdefault("tasa_auditoria", 0.0)
    kw.setdefault("tasa_auditoria_pase", 0.0)
    return CriterioLocal(umbrales=UmbralesCriterioLocal(piso_vueltas=10 ** 9, **kw),
                         rng=random.Random(0))


def _filtro(**kw) -> CriterioLocal:
    """Filtro con auditoría apagada y RNG sembrado, salvo que se pida otra cosa."""
    kw.setdefault("tasa_auditoria", 0.0)
    return CriterioLocal(umbrales=UmbralesCriterioLocal(**kw),
                         rng=random.Random(0))


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
    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    mod.Client = lambda url: client
    try:
        asyncio.run(dev.run(duration=duration))
    finally:
        mod.Client = orig


def _silencio(filtro, vueltas: int, desde: int = 1) -> List[dict]:
    """`vueltas` evaluaciones con el canal callado."""
    return [filtro.evaluar(tick=t, n_nuevos=0)
            for t in range(desde, desde + vueltas)]


# ── EL test: el silencio no es absorbente ───────────────────────────────────

def test_el_silencio_no_vuelve_absorbente_al_filtro() -> None:
    """
    **El test que pide la especificación** (DECISIONES `e737e78`): canal callado
    N vueltas → `llamadas a D > 0` **y** `skips != N`.

    Corre con la auditoría **apagada**: lo que sostiene la iniciativa acá es el
    piso, y es determinístico. Si pasara por la auditoría, el test pasaría o no
    según el RNG y no mediría el filtro.

    El silencio absorbente es del **filtro**, no del device (Opus): el filtro
    está entre O y D y es el único con estado ahí. Si su criterio sólo mira los
    mensajes, con el canal callado no cambió nada → no llama a D → el device no
    decide → el canal sigue callado.
    """
    N = 40
    filtro = _filtro(piso_vueltas=5)
    regs = _silencio(filtro, N)

    llamadas = [r for r in regs if r["llamar"]]
    skips = [r for r in regs if not r["llamar"]]

    assert len(llamadas) > 0, \
        "el filtro no llamó nunca a D: el silencio es punto fijo del lazo"
    assert len(skips) != N, "todas las vueltas fueron skip"
    # y no es que llamó una sola vez de casualidad: el piso es periódico
    assert len(llamadas) >= N // 10


def test_un_piso_fuera_del_horizonte_ES_absorbente() -> None:
    """
    **Afirma el agujero.** Con `piso_vueltas=0` y sin auditoría, el filtro no
    llama nunca: el silencio es absorbente.

    Este test no está para que el código pase: está para que quede escrito que
    **lo que rompe el punto fijo es el piso**, y que apagarlo lo devuelve. Es la
    inversión del test de arriba, como test.

    **Y el piso 0 ya no se puede configurar** (`ValueError`). Más: con la guarda
    `> 0` afuera de `evaluar`, un `0` haría disparar el piso **siempre**. Así que
    la absorción no se exhibe apagando el piso: se exhibe con un piso **fuera del
    horizonte**, que es indistinguible de no tenerlo.

    Eso dice algo que "sin piso es absorbente" no decía: **que el piso sea finito
    no alcanza**, tiene que caer dentro de la ventana que se observa. Eso es
    calibración, y es por qué los umbrales van declarados sin calibrar.
    """
    with pytest.raises(ValueError):
        UmbralesCriterioLocal(piso_vueltas=0)   # por configuración, no se llega

    filtro = _piso_fuera_del_horizonte()
    regs = _silencio(filtro, 40)

    # la primera vuelta llama igual: "nunca llamó" no es "llamó hace 0 vueltas"
    assert regs[0]["motivo"] == MOTIVO_PRIMERA
    # de ahí en adelante, nada
    assert all(not r["llamar"] for r in regs[1:]), \
        "sin piso algo llamó: revisar qué, porque el test de arriba se apoya en esto"


def test_la_auditoria_sola_puede_no_llamar_nunca() -> None:
    """
    **Afirma el otro agujero**, el que nombró Opus: con la auditoría como única
    pieza, *"la iniciativa queda en manos de la suerte"*.

    Con tasa 0.1 hay probabilidad positiva de cero llamadas en N vueltas. Acá se
    exhibe con una semilla concreta: no es un argumento, es una corrida.
    """
    # semilla buscada para que no salga ninguna auditoría en 20 vueltas
    semilla = next(
        s for s in range(500)
        if all(random.Random(s).random() >= 0.1 for _ in range(20))
    )
    # piso fuera del horizonte: dentro de las 20 vueltas que se miran, el
    # piso no existe, y lo único que podría llamar es la auditoría
    filtro = CriterioLocal(
        umbrales=UmbralesCriterioLocal(piso_vueltas=10 ** 9, tasa_auditoria=0.1),
        rng=random.Random(semilla),
    )
    regs = _silencio(filtro, 20)
    assert all(not r["llamar"] for r in regs[1:]), \
        f"con la semilla {semilla} salió una auditoría; buscar otra"


def test_el_piso_es_periodico_y_deterministico() -> None:
    """Dos filtros iguales, con la misma entrada, llaman en las mismas vueltas."""
    a = _silencio(_filtro(piso_vueltas=7), 30)
    b = _silencio(_filtro(piso_vueltas=7), 30)
    assert [r["llamar"] for r in a] == [r["llamar"] for r in b]
    assert [r["motivo"] for r in a].count(MOTIVO_PISO) >= 3


# ── el skip es distinguible de OP_SILENCE y de UNKNOWN ──────────────────────

def test_skip_no_es_OP_SILENCE_ni_UNKNOWN() -> None:
    """
    **Pedido de Opus:** en la traza, un skip tiene que ser distinguible de un
    `OP_SILENCE`. Si no, el par *"filtro calló / modelo calló"* se ve igual
    desde afuera, que es el par vivo 01 / vivo 02 con el filtro en el lugar del
    provider caído.

    Las tres terminan la vuelta sin acción y las tres son distintas:
    `OP_SILENCE` lo decidió el modelo, `UNKNOWN` fue el provider, `SKIP` es el
    filtro no habiendo llamado.
    """
    assert DECISION_SKIP not in ("OP_SILENCE", "UNKNOWN")
    assert len({DECISION_SKIP, "OP_SILENCE", "UNKNOWN"}) == 3


def test_en_la_traza_del_device_el_skip_se_distingue(canal) -> None:
    """Y la distinción llega al log del device, no sólo a la constante."""
    dev = _device(ProviderStub(["OP_SILENCE"] * 50),
                  criterio_local=_filtro(piso_vueltas=3))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    tipos = {d["decision"] for d in dev.decisiones()}
    assert DECISION_SKIP in tipos, "ninguna vuelta fue skip: subir las vueltas"
    # y cada skip trae su motivo
    for d in dev.decisiones():
        if d["decision"] == DECISION_SKIP:
            assert d["criterio_motivo"] == MOTIVO_SIN_CAMBIO
            assert d["criterio_via"] is None


def test_un_skip_no_publica_nada(canal) -> None:
    """
    **Lo que el instrumento tiene que garantizar**, y lo que casi se me pasa.

    `_interact` cae **por default** a generar y publicar: sus ramas son
    UNKNOWN, OP_SILENCE y LEAVE, y cualquier otra palabra sigue de largo. Al
    agregar `DECISION_SKIP` la vuelta que el filtro skipeaba **publicaba un
    mensaje**.

    Lo encontré con `test_un_skip_no_gasta_una_llamada`, que mira la llamada al
    LLM. Ese test es **más débil que el defecto**: una llamada de más es costo,
    una publicación de más es el canal cambiado por el filtro. Lo vi de costado
    y por eso este test existe aparte, midiendo lo que hay que medir.

    El fallthrough queda como está: hoy sólo lo alcanza INTERACT, porque
    `_decide` manda toda palabra desconocida a UNKNOWN. Va reportado como
    mecanismo, no corregido de paso.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 50),
                  criterio_local=_filtro(piso_vueltas=3))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    skips = [d for d in dev.decisiones() if d["decision"] == DECISION_SKIP]
    assert skips, "ninguna vuelta fue skip: el test no mide nada"
    publicados = [m for m in canal.messages if m.device_id == dev.device_id]
    assert not publicados, \
        f"el filtro skipeó y el device publicó {len(publicados)} mensaje(s)"


def test_un_skip_no_gasta_una_llamada(canal) -> None:
    """Lo que el filtro es para: la vuelta que skipea no llama al LLM."""
    dev = _device(ProviderStub(["OP_SILENCE"] * 50),
                  criterio_local=_filtro(piso_vueltas=3))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    for d in dev.decisiones():
        if d["decision"] == DECISION_SKIP:
            assert d["llamadas_llm"] == 0, "un skip gastó una llamada"


# ── el motivo va en el turno, no en un contador ─────────────────────────────

def test_cada_vuelta_lleva_su_motivo() -> None:
    """
    **Pedido de Opus, precisado acá:** el motivo va en el registro **del
    turno**. Un contador dice cuántos, no cuáles, y cuáles es lo que hace falta
    para saber si el silencio estaba decidido.
    """
    regs = _silencio(_filtro(piso_vueltas=4), 20)
    assert all(r["motivo"] for r in regs), "una vuelta quedó sin motivo"
    assert all("deltas" in r for r in regs)
    # los motivos no son todos el mismo: el piso se distingue del sin_cambio
    assert {MOTIVO_PISO, MOTIVO_SIN_CAMBIO} <= {r["motivo"] for r in regs}


def test_la_via_dice_por_que_SI_se_llamo() -> None:
    """
    *Por qué se llamó* queda tan trazable como *por qué no*. Sin la vía, una
    llamada del piso y una del criterio se ven iguales, y la divergencia de la
    auditoría se mezclaría con el resto.
    """
    f = _filtro(piso_vueltas=3)
    regs = [f.evaluar(tick=1, n_nuevos=0),          # primera
            f.evaluar(tick=2, n_nuevos=2),          # mensajes
            f.evaluar(tick=3, n_nuevos=0),
            f.evaluar(tick=4, n_nuevos=0),
            f.evaluar(tick=5, n_nuevos=0),
            f.evaluar(tick=6, n_nuevos=0)]          # piso
    vias = [r["via"] for r in regs if r["llamar"]]
    assert VIA_CRITERIO in vias and VIA_PISO in vias
    assert all(r["via"] is None for r in regs if not r["llamar"])


def test_la_auditoria_queda_marcada_como_tal() -> None:
    """Una llamada de auditoría no se confunde con una del criterio."""
    # el piso puesto lejos para que no estorbe: eso sí es configuración válida
    f = CriterioLocal(umbrales=UmbralesCriterioLocal(piso_vueltas=99,
                                                     tasa_auditoria=1.0),
                      rng=random.Random(0))
    f.evaluar(tick=1, n_nuevos=0)                   # primera vuelta
    r = f.evaluar(tick=2, n_nuevos=0)
    assert r["llamar"] and r["motivo"] == MOTIVO_AUDITORIA
    assert r["via"] == VIA_AUDITORIA


# ── los umbrales, declarados no calibrados ──────────────────────────────────

def test_los_umbrales_nacen_sin_calibrar() -> None:
    """*"Los umbrales son de Calibración y no los inventa Code."*"""
    assert UmbralesCriterioLocal().calibrado is False


def test_el_sin_calibrar_viaja_en_cada_registro() -> None:
    """No en un comentario del código: en el registro de cada vuelta."""
    for r in _silencio(_filtro(piso_vueltas=4), 10):
        assert r["umbrales_calibrados"] is False
        assert r["umbrales"]["piso_vueltas"] == 4


def test_el_panel_declara_los_umbrales_sin_calibrar(canal) -> None:
    """**Pedido de Opus:** umbrales declarados "no calibrados" **en el panel**."""
    dev = _device(ProviderStub(["OP_SILENCE"] * 50),
                  criterio_local=_filtro(piso_vueltas=3))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    panel = dev.panel_criterio()
    assert panel is not None
    assert panel["calibrado"] is False
    assert panel["umbrales"]["piso_vueltas"] == 3
    assert panel["n_skips"] + panel["n_llamadas"] == panel["vueltas_evaluadas"]
    assert dev.costo()["criterio_local"]["calibrado"] is False


def test_sin_filtro_el_panel_es_None_no_un_panel_en_cero(canal) -> None:
    """
    Cero skips porque no hay filtro y cero skips porque el filtro llamó siempre
    son dos cosas distintas. La ausencia es el estado del observador (§19).
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 50))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)
    assert dev.panel_criterio() is None
    assert dev.costo()["criterio_local"] is None


# ── los deltas: del reloj del canal, y ausentes los que no existen ──────────

def test_los_dt_salen_del_reloj_del_canal() -> None:
    """
    TASK §0.4: *"los Δt se calculan con los timestamps del canal, nunca
    mezclando el reloj del device con el del canal."*
    """
    from datetime import datetime, timezone
    t0 = datetime(2026, 10, 9, 5, 0, 0, tzinfo=timezone.utc)
    assert dt_desde(t0.timestamp() + 30.0, t0.isoformat()) == pytest.approx(30.0)


def test_un_dt_que_no_se_pudo_medir_es_None_no_cero() -> None:
    """
    `0.0` diría "recién ahora" sobre algo que nunca se midió, y el criterio lo
    leería como actividad.
    """
    assert dt_desde(None, "2026-10-09T05:00:00+00:00") is None
    assert dt_desde(1000.0, None) is None
    assert dt_desde(1000.0, "") is None
    assert dt_desde(1000.0, "no es una fecha") is None


def test_objetivo_y_presupuesto_van_ausentes_declarados() -> None:
    """
    No existen hasta el caso Z (CP3, delamor). Van `None`, no `0` ni `False`:
    la ausencia es el estado del observador, no un valor de la escala.
    """
    r = _filtro(piso_vueltas=4).evaluar(tick=1, n_nuevos=0)
    assert r["deltas"]["estado_objetivo"] is None
    assert r["deltas"]["presupuesto"] is None


def test_el_clock_UNKNOWN_llama_a_D() -> None:
    """
    Sin tick no se puede saber si el piso venció. El filtro no se arroga el
    silencio sobre una dimensión que no observó.
    """
    f = _filtro(piso_vueltas=4)
    f.evaluar(tick=1, n_nuevos=0)                   # gasta la primera vuelta
    r = f.evaluar(tick=None, n_nuevos=0)
    assert r["llamar"] and r["motivo"] == "tick_UNKNOWN"


def test_nombrar_al_device_llama_a_D() -> None:
    f = _filtro(piso_vueltas=99)
    f.evaluar(tick=1, n_nuevos=0)
    r = f.evaluar(tick=2, n_nuevos=0, nombrado=True)
    assert r["llamar"] and r["motivo"] == "nombrado"


def test_delta_mensajes_cuenta_solo_ajenos(canal) -> None:
    """
    TASK §1: *"Δ mensajes cuenta sólo los mensajes ajenos. El propio mensaje
    entra como 'Δt desde que hablé', es información y no disparador."*

    Se verifica en el lazo, que es quien le pasa `n_nuevos` al filtro: ya filtra
    `m["device_id"] != self.device_id`. El device publica y después calla; sus
    propios mensajes no pueden contar como mensajes nuevos.
    """
    dev = _device(ProviderStub(["INTERACT"] + ["OP_SILENCE"] * 50),
                  criterio_local=_filtro(piso_vueltas=99))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    propios = [m for m in canal.messages if m.device_id == dev.device_id]
    assert propios, "el device no publicó: el test no mide nada"
    # ninguna vuelta posterior a la publicación vio mensajes nuevos
    regs = dev.registros_criterio()
    assert all(r["deltas"]["n_nuevos"] == 0 for r in regs), \
        "el propio mensaje contó como mensaje nuevo"


# ── el costo del sesgo ──────────────────────────────────────────────────────

def test_sin_auditorias_la_tasa_es_None_no_cero() -> None:
    """`0.0` afirma que se auditó y no divergió. Son dos cosas distintas."""
    d = divergencia_auditoria(_silencio(_filtro(piso_vueltas=4), 10))
    assert d["n_auditados"] == 0
    assert d["tasa"] is None


def test_un_auditado_sin_decision_no_cuenta_como_que_no_divergio() -> None:
    """No haber mirado no es haber visto que no."""
    d = divergencia_auditoria([{"via": VIA_AUDITORIA, "llamar": True}])
    assert d["n_sin_decision"] == 1
    assert d["n_con_decision"] == 0
    assert d["tasa"] is None


def test_la_divergencia_cuenta_lo_que_D_habria_hecho() -> None:
    """
    *"Se registra si D habría hecho algo distinto de 'nada'. La tasa de
    divergencia mide el costo del sesgo."*
    """
    regs = [
        {"via": VIA_AUDITORIA, "llamar": True, "decision": "INTERACT"},
        {"via": VIA_AUDITORIA, "llamar": True, "decision": "OP_SILENCE"},
        {"via": VIA_AUDITORIA, "llamar": True, "decision": "UNKNOWN"},
        {"via": VIA_CRITERIO, "llamar": True, "decision": "INTERACT"},
    ]
    d = divergencia_auditoria(regs)
    assert d["n_auditados"] == 3            # el del criterio no cuenta
    assert d["n_divergieron"] == 1          # sólo el INTERACT
    assert d["tasa"] == pytest.approx(1 / 3)


# ── lo que el CP2b NO cambió ────────────────────────────────────────────────

def test_sin_criterio_local_D_corre_en_cada_vuelta(canal) -> None:
    """
    El default es **sin filtro**: el comportamiento del CP2a y el de los dos
    vivos. Si el filtro entrara por default, la línea de base del vivo 02 (23
    llamadas, 23 `OP_SILENCE`) dejaría de ser comparable sin que nada lo dijera.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 50))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    ds = dev.decisiones()
    assert ds, "no corrió ninguna vuelta"
    assert all(d["decision"] != DECISION_SKIP for d in ds)
    assert all(d["criterio_motivo"] is None for d in ds)
    assert all(d["llamadas_llm"] >= 1 for d in ds)


def test_los_deltas_NO_entran_al_prompt_del_gate(canal) -> None:
    """
    **Tensión anotada por Opus antes de arrancar.** La TASK §1 dice que los
    deltas *"entran como información a D cuando sí se lo llama"*, y eso
    cambiaría el texto del gate, **que está congelado** (delamor). En el CP2b
    los deltas se registran en la traza y **no entran al prompt**. Si hace falta
    que D los vea, se para y se reporta.
    """
    prov = ProviderStub(["OP_SILENCE"] * 50)
    dev = _device(prov, criterio_local=_filtro(piso_vueltas=3))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    import json
    enviado = json.dumps(prov.llamadas, default=str)
    for marca in ("dt_desde_ajeno", "dt_desde_que_hable", "vueltas_sin_llamar",
                  "piso_vueltas", "tasa_auditoria", "umbrales"):
        assert marca not in enviado, f"{marca} se filtró al prompt del gate"


def test_el_texto_del_gate_sigue_congelado() -> None:
    """El CP2b no toca el gate. Se verifica contra el texto, no contra el diff."""
    from iap_chatroom.autonomous_device import GATE_PROMPT_CONTINUO
    assert "You are not obligated to act." in GATE_PROMPT_CONTINUO
    # "(ninguno)" se sustituye en {incoming} al formatear; en la plantilla va el
    # hueco. Mi aserción pedía el valor y no el molde, y el test falló por mí.
    assert "Incoming: {incoming}" in GATE_PROMPT_CONTINUO
    assert "INTERACT (publish), LEAVE (leave the channel), or OP_SILENCE" \
        in GATE_PROMPT_CONTINUO
    assert "criterio" not in GATE_PROMPT_CONTINUO.lower()
    assert "skip" not in GATE_PROMPT_CONTINUO.lower()


# ── las dos caras (Opus: "que no se le vea a uno solo de los lados") ────────

def test_la_auditoria_mira_las_dos_caras() -> None:
    """
    Spec: *"auditoría al azar **sobre las dos caras**"*. Esto me faltaba: mi
    primera versión sólo medía la cara del skip, y la otra quedaba sin medir.

    Las dos caras no son simétricas y por eso se miden distinto:

    - **dijo "no"** → muestreo. Es invisible sin muestrearla: no se llamó, no
      hay decisión que mirar. El error de esa cara es *tapar una decisión*.
    - **dijo "sí"** → censo. Es visible por construcción: toda vuelta que pasa
      el filtro llama a D y deja su decisión. El error de esa cara es *pagar
      una llamada de más*.

    La asimetría no es una elección: muestrear lo que ya se ve entero no
    agregaría nada, y no muestrear lo que no se ve dejaría una cara sin medir.
    """
    regs = [
        # cara "no": auditadas. Una tapaba un INTERACT.
        {"via": VIA_AUDITORIA, "llamar": True, "decision": "INTERACT"},
        {"via": VIA_AUDITORIA, "llamar": True, "decision": "OP_SILENCE"},
        # cara "sí": pasaron el filtro. Una no hizo nada → llamada de más.
        # `auditado_pase` marca las que el sorteo tomó para la muestra.
        {"via": VIA_CRITERIO, "llamar": True, "decision": "INTERACT",
         "auditado_pase": True},
        {"via": VIA_PISO, "llamar": True, "decision": "OP_SILENCE",
         "auditado_pase": True},
        # skips sin auditar: no entran a ninguna cara, no se miraron
        {"via": None, "llamar": False, "motivo": MOTIVO_SIN_CAMBIO},
    ]
    d = divergencia_auditoria(regs)

    assert d["dijo_no"]["metodo"] == "muestreo"
    assert d["dijo_no"]["n_divergieron"] == 1          # el INTERACT tapado
    assert d["dijo_no"]["tasa"] == pytest.approx(0.5)

    # Las dos lecturas de la cara del pase, y cada una dice de dónde sale.
    assert d["dijo_si"]["metodo"] == "muestreo+censo"
    assert d["dijo_si"]["n_vueltas"] == 2              # las sorteadas
    assert d["dijo_si"]["n_divergieron"] == 1          # el OP_SILENCE de más
    assert d["dijo_si"]["tasa"] == pytest.approx(0.5)
    # el censo cubre todas las que pasaron, sorteadas o no
    assert d["dijo_si"]["censo"]["n_vueltas"] == 2
    assert d["dijo_si"]["censo"]["tasa"] == pytest.approx(0.5)


def test_las_dos_caras_distinguen_sus_errores() -> None:
    """
    Un filtro que nunca tapa nada pero llama siempre de más **no** es un buen
    filtro, y con una sola cara se vería perfecto.
    """
    regs = [{"via": VIA_AUDITORIA, "llamar": True, "decision": "OP_SILENCE"}] * 5 \
        + [{"via": VIA_PISO, "llamar": True, "decision": "OP_SILENCE",
            "auditado_pase": True}] * 5
    d = divergencia_auditoria(regs)
    assert d["dijo_no"]["tasa"] == 0.0        # no tapó nada
    assert d["dijo_si"]["tasa"] == 1.0        # y pagó todas de más
    assert d["dijo_si"]["censo"]["tasa"] == 1.0


def test_una_cara_sin_datos_da_None_y_no_cero() -> None:
    """`0.0` afirmaría que se miró esa cara y no divergió."""
    d = divergencia_auditoria([{"via": None, "llamar": False,
                                "motivo": MOTIVO_SIN_CAMBIO}])
    assert d["dijo_no"]["tasa"] is None
    assert d["dijo_si"]["tasa"] is None
    assert d["dijo_si"]["censo"]["tasa"] is None


def test_el_panel_lleva_las_dos_caras(canal) -> None:
    """Y las dos caras llegan al panel, que es donde se leen."""
    dev = _device(ProviderStub(["OP_SILENCE"] * 50),
                  criterio_local=_filtro(piso_vueltas=3))
    _correr(dev, ClientStub(canal, dev.device_id), duration=0.05)

    div = dev.panel_criterio()["divergencia_auditoria"]
    assert set(div) >= {"dijo_no", "dijo_si"}
    assert div["dijo_si"]["n_vueltas"] > 0, "ninguna vuelta pasó el filtro"


def test_las_dos_tasas_van_declaradas_sin_calibrar() -> None:
    """
    Opus (CP0): *"las dos van al azar, con la tasa declarada como 'no
    calibrada', igual que los umbrales."*
    """
    u = UmbralesCriterioLocal()
    assert u.tasa_auditoria == pytest.approx(0.1)
    assert u.tasa_auditoria_pase == pytest.approx(0.1)
    assert u.calibrado is False
    # y las dos viajan en el registro de cada vuelta, con su valor. La
    # aserción que había acá era `== 0.0 or "..." in r["umbrales"]`, que es
    # verdadera casi siempre: no podía fallar. Es el mismo patrón que vengo
    # sacando de los tests ajenos toda la sesión, esta vez mío.
    f = CriterioLocal(
        umbrales=UmbralesCriterioLocal(piso_vueltas=4, tasa_auditoria=0.3,
                                       tasa_auditoria_pase=0.7),
        rng=random.Random(0),
    )
    r = f.evaluar(tick=1, n_nuevos=0)
    assert r["umbrales"]["tasa_auditoria"] == pytest.approx(0.3)
    assert r["umbrales"]["tasa_auditoria_pase"] == pytest.approx(0.7)
    assert r["umbrales_calibrados"] is False


def test_el_muestreo_del_pase_no_cuesta_una_llamada() -> None:
    """
    **Lo que medí, y la razón de que la cara del pase lleve además el censo.**

    En la cara del skip, cada vuelta sorteada cuesta una llamada: es lo que se
    paga por ver lo que el filtro tapaba. En la cara del pase la llamada **ya
    se hizo**, así que el sorteo no ahorra nada — lo único que decide es si la
    vuelta entra a la muestra.

    Se verifica así: con la tasa del pase en 0 y en 1, las vueltas que llaman
    son **las mismas**. Lo que cambia es cuántas quedan marcadas.
    """
    def correr(tasa_pase):
        f = CriterioLocal(
            umbrales=UmbralesCriterioLocal(piso_vueltas=3, tasa_auditoria=0.0,
                                           tasa_auditoria_pase=tasa_pase),
            rng=random.Random(7),
        )
        regs = _silencio(f, 20)
        return ([r["llamar"] for r in regs],
                sum(1 for r in regs if r.get("auditado_pase")))

    llamadas_0, marcadas_0 = correr(0.0)
    llamadas_1, marcadas_1 = correr(1.0)

    assert llamadas_0 == llamadas_1, \
        "el sorteo del pase cambió qué vueltas llaman: no debería"
    assert marcadas_0 == 0 and marcadas_1 > 0, \
        "el sorteo del pase no cambió qué vueltas quedan en la muestra"


# ── los cuatro ajustes de Opus (9 oct) ──────────────────────────────────────

def test_el_piso_cuenta_vueltas_y_el_nombre_lo_dice() -> None:
    """
    **Ajuste 1.** Se llamaba `piso_ticks` y lo que mide es `_vueltas_sin_llamar`.
    El nombre decía otra cosa que lo medido, y con `poll_interval` y el período
    del tick distintos los dos números se separan.

    Se verifica que cuenta **vueltas**: con el tick quieto —el mismo número en
    todas las evaluaciones— el piso igual dispara.
    """
    assert not hasattr(UmbralesCriterioLocal(), "piso_ticks")
    f = _filtro(piso_vueltas=4)
    regs = [f.evaluar(tick=7, n_nuevos=0) for _ in range(12)]   # tick QUIETO
    assert any(r["motivo"] == MOTIVO_PISO for r in regs), \
        "con el tick quieto el piso no disparó: estaría contando ticks"


def test_apagar_el_piso_no_es_una_configuracion_valida() -> None:
    """
    **Ajuste 2.** El docstring decía que el piso "no es opcional" y el
    constructor dejaba pasar un `0` que lo apagaba: **el texto afirmaba una cosa
    y el código permitía la otra.**
    """
    for v in (0, -1, -100):
        with pytest.raises(ValueError, match="piso_vueltas"):
            UmbralesCriterioLocal(piso_vueltas=v)
    assert UmbralesCriterioLocal(piso_vueltas=1).piso_vueltas == 1


def test_publicar_exige_INTERACT_explicito(canal, capsys) -> None:
    """
    **Ajuste 3.** `_interact` caía por default a generar y publicar: toda palabra
    que no fuera UNKNOWN/SKIP/OP_SILENCE/LEAVE terminaba en `send_message`.

    Hoy `_decide` acota el vocabulario, así que no era un defecto vivo. Pero
    **el relleno de la ausencia era una acción sobre el canal**, y el CP2b ya
    mostró lo que pasa cuando entra un valor nuevo: el skip publicaba.

    Una decisión que no se reconoce no autoriza nada, y se registra como UNKNOWN
    igual que la que no existió.
    """
    dev = _device(ProviderStub(["OP_SILENCE"]))
    client = ClientStub(canal, dev.device_id)

    import iap_chatroom.autonomous_device as mod
    orig = mod.Client
    mod.Client = lambda url: client
    try:
        asyncio.run(client.call_tool(
            "join_channel", {"device_id": dev.device_id, "device_type": "AI"}))
        asyncio.run(dev._interact(client, "PALABRA_QUE_NO_EXISTE",
                                  {"field": None}))
    finally:
        mod.Client = orig

    publicados = [m for m in canal.messages if m.device_id == dev.device_id]
    assert not publicados, "una decisión desconocida publicó un mensaje"

    # Y quedó registrada como UNKNOWN, no como la palabra cruda. `_log` imprime
    # y no guarda, así que se lee de la salida — no de un atributo que no
    # existe. Las dos aserciones que había acá (`== [] or True` y un `if
    # hasattr(...) else True`) **no podían fallar**: el mismo patrón, en el
    # test que escribí para el patrón.
    salida = capsys.readouterr().out
    assert "UNKNOWN" in salida, "la decisión desconocida no se registró"
    assert "PALABRA_QUE_NO_EXISTE" not in salida, \
        "la palabra cruda entró al log en vez de UNKNOWN"


def test_nunca_llamo_es_None_y_no_un_tick() -> None:
    """
    **Ajuste 4.** `_tick_ultima_llamada` arrancaba en `-1`: una ausencia
    representada con un valor de la escala. Es el mismo relleno que vengo
    sacando de todo el resto de la sesión, puesto por mí en el archivo nuevo.

    Y hay un segundo caso: si el clock está UNKNOWN, **no se sabe en qué tick se
    llamó**, y eso tampoco es el tick `-1`.
    """
    f = _filtro(piso_vueltas=4)
    assert f._tick_ultima_llamada is None, "nunca llamó se representa con None"

    f.evaluar(tick=3, n_nuevos=0)
    assert f._tick_ultima_llamada == 3

    f2 = _filtro(piso_vueltas=4)
    f2.evaluar(tick=1, n_nuevos=0)          # gasta la primera vuelta
    f2.evaluar(tick=None, n_nuevos=0)       # clock UNKNOWN → llama
    assert f2._tick_ultima_llamada is None, \
        "un tick UNKNOWN quedó registrado como el tick -1"


def test_el_panel_declara_si_el_piso_cupo_en_la_corrida() -> None:
    """
    **Consecuencia de calibración que nombró Opus:** un piso más largo que la
    ventana observada es, en la práctica, lo mismo que no tener piso. Con 12
    vueltas de piso y un vivo de 11, el silencio es absorbente **dentro de lo
    que se observa**.

    El umbral es de Calibración. Lo del instrumento es **declarar si esta
    corrida pudo verlo**: si hubo skips y el piso no disparó nunca, la corrida
    no puede decir si el silencio era absorbente, y eso es UNKNOWN y no "no
    era".
    """
    import iap_chatroom.autonomous_device as mod

    dev = AutonomousDevice(device_id="d", provider=ProviderStub([]),
                           system_prompt="s", poll_interval=0.0,
                           criterio_local=_filtro(piso_vueltas=5))
    # 4 vueltas de silencio: menos de las que el piso necesita
    dev._registros_criterio = _silencio(_filtro(piso_vueltas=5), 4)
    panel = dev.panel_criterio()
    assert panel["piso_dentro_del_horizonte"] is False, \
        "la corrida afirmó haber visto un piso que no alcanzó a disparar"
    assert panel["vueltas_para_ver_el_piso"] == 7

    # con vueltas de sobra, el piso sí cupo
    dev._registros_criterio = _silencio(_filtro(piso_vueltas=5), 30)
    assert dev.panel_criterio()["piso_dentro_del_horizonte"] is True


def test_sin_skips_el_horizonte_no_aplica() -> None:
    """`False` diría "el piso no cupo"; sin skips la pregunta no se hizo."""
    dev = AutonomousDevice(device_id="d", provider=ProviderStub([]),
                           system_prompt="s", poll_interval=0.0,
                           criterio_local=_filtro(piso_vueltas=5))
    f = _filtro(piso_vueltas=5)
    dev._registros_criterio = [f.evaluar(tick=i, n_nuevos=3) for i in range(1, 6)]
    assert dev.panel_criterio()["n_skips"] == 0
    assert dev.panel_criterio()["piso_dentro_del_horizonte"] is None


@pytest.mark.parametrize("piso", [1, 2, 3, 5, 12, 23])
def test_vueltas_para_ver_el_piso_coincide_con_la_corrida(piso) -> None:
    """
    El campo se compara con **la vuelta en que el piso dispara de verdad**, no
    con una fórmula.

    Tenía `piso_vueltas + 1` y el test lo confirmaba, porque lo había escrito
    contra el código. Un test que repite la cuenta del código no puede
    encontrar un off-by-one: sólo lo encuentra correr el filtro y mirar.

    Lo correcto es `piso + 2`: la vuelta 1 la consume `primera_vuelta` —llama y
    deja el contador en 0— y de ahí el contador necesita `piso` skips más.
    """
    f = _filtro(piso_vueltas=piso)
    primera = next(
        v for v in range(1, piso + 50)
        if f.evaluar(tick=v, n_nuevos=0)["motivo"] == MOTIVO_PISO
    )
    dev = AutonomousDevice(device_id="d", provider=ProviderStub([]),
                           system_prompt="s", poll_interval=0.0,
                           criterio_local=_filtro(piso_vueltas=piso))
    dev._registros_criterio = _silencio(_filtro(piso_vueltas=piso), 1)
    assert dev.panel_criterio()["vueltas_para_ver_el_piso"] == primera


def test_el_piso_por_default_no_habria_disparado_en_un_vivo_como_el_02() -> None:
    """
    **Corrección de un número mío, medida en el log del vivo 02.**

    Reporté *"el vivo 02 corrió 23 vueltas, así que el piso de 12 entraba"*.
    **23 era el total de llamadas entre los DOS devices**; por device fueron
    **11 y 12** (`vivo_02_groq_gptoss20b_log.json`, `costo.vueltas`). Leí un
    agregado como un conteo por unidad — la misma confusión que el `n_agentes`
    de esta mañana.

    El piso es estado **por device**, así que el horizonte real son 11-12
    vueltas. Con el default de 12 hacen falta **14**: el piso **no habría
    disparado nunca**. No estaba "en el borde": estaba afuera.
    """
    f = _filtro(piso_vueltas=12)
    regs = _silencio(f, 12)          # las vueltas que tuvo el device más largo
    assert all(r["motivo"] != MOTIVO_PISO for r in regs), \
        "el piso de 12 disparó dentro de 12 vueltas: revisar la cuenta"

    dev = AutonomousDevice(device_id="d", provider=ProviderStub([]),
                           system_prompt="s", poll_interval=0.0,
                           criterio_local=_filtro(piso_vueltas=12))
    dev._registros_criterio = regs
    panel = dev.panel_criterio()
    assert panel["piso_dentro_del_horizonte"] is False
    assert panel["vueltas_para_ver_el_piso"] == 14
