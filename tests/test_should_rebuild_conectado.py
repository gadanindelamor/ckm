"""
test_should_rebuild_conectado.py — TASK_should_rebuild_conectado_v1

CP1: **con el canal vivo, ingesta sin señal → W no cambia (sha igual).**

Es el invariante que tiene que seguir valiendo **después** de que la señal mande
el rebuild: si `_last_rebuild_signal` es False, no hay salto. Se escribe antes de
implementar, así que hoy pasa por el comportamiento de hoy
(`rebuild_suspendido=True` construye W una vez y no la reconstruye) y mañana
tiene que pasar por el nuevo camino. **Un test que pasa antes y después del
cambio sólo sirve si lo que afirma es el invariante, no el mecanismo** — por eso
afirma el sha y la señal, no cómo se decidió.

### La ventana en la que "sin señal" existe hoy, medida

La señal es `estructural or volumen or tiempo`, con:

- volumen: `len(_texts) >= min_texts * 2` → con `min_texts=3`, **a partir de 6
  textos queda en True para siempre**;
- tiempo: `_ciclos_sin_rebuild >= MAX_CICLOS` (10);
- estructural: gradiente de `D_ckm` positivo en 3 pasos.

Así que **"sin señal" sólo existe con menos de 6 textos**. Eso no es una
limitación del test: es el punto 3 de la TASK (el volumen tiene que contar desde
el último rebuild). El test lo declara y se queda dentro de esa ventana; cuando
el volumen pase a contar por ciclo, la ventana se abre y este test sigue valiendo.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom.ckm_monitor import MAX_CICLOS, CKMMonitor   # noqa: E402

# Textos que distinguen: el corpus necesita vocabulario para extraer nodos.
TEXTOS = [
    "gun control reduces violence",
    "gun control does not reduce violence",
    "the data on firearms is contested",
    "statistics on weapons are disputed",
    "rights and weapons are in tension",
]


class _Msg:
    """Un mensaje del canal, con lo que `on_message` lee."""

    def __init__(self, text: str, device_id: str = "d1", device_type: str = "AI"):
        self.text, self.device_id, self.device_type = text, device_id, device_type


@pytest.fixture
def monitor(tmp_path, monkeypatch):
    """
    Monitor con `state_dir` aislado. `CKMMonitor` es singleton: sin resetear
    `_instance`, un test se quedaría con el corpus del anterior.

    El `state_dir` sale del **fix 2**; antes había que ir por un launcher.
    """
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm = CKMMonitor(min_texts=3, state_dir=tmp_path / "_state")
    assert cm.state_dir == tmp_path / "_state"
    yield cm
    monkeypatch.setattr(CKMMonitor, "_instance", None)


# ── CP1 ─────────────────────────────────────────────────────────────────────

def test_cp1_sin_senal_W_no_cambia(monitor) -> None:
    """
    **CP1.** Ingesta en el canal vivo sin que la señal se levante: el sha de W
    queda igual desde que W existe.

    Se verifica el **sha**, no `rebuild_suspendido`: el flag es el mecanismo de
    hoy y el invariante es que sin señal no hay salto.
    """
    cm = monitor
    shas, señales = [], []

    for t in TEXTOS:                      # 5 textos: menos de min_texts*2 = 6
        cm.on_message(_Msg(t))
        shas.append(cm._corpus.w_sha())
        señales.append(cm._last_rebuild_signal)

    # W aparece recién al cruzar min_texts=3
    assert shas[0] is None and shas[1] is None, f"W antes de min_texts: {shas}"
    assert shas[2] is not None, "W no se construyó al cruzar min_texts"

    # **El invariante:** desde que existe, no cambia
    desde_que_existe = shas[2:]
    assert len(set(desde_que_existe)) == 1, (
        f"W cambió sin señal: {[s[:8] if s else None for s in desde_que_existe]}"
    )

    # y no cambió porque **no hubo señal**, no por casualidad
    assert señales == [False] * len(TEXTOS), (
        f"la señal se levantó dentro de la ventana: {señales}"
    )


def test_cp1_la_ventana_sin_senal_se_cierra_en_2x_min_texts(monitor) -> None:
    """
    **Lo que el CP1 no puede cubrir hoy, medido y declarado.**

    El criterio de volumen es `len(_texts) >= min_texts * 2` sobre el **total
    del corpus**, así que a partir del texto 6 la señal queda en True **para
    siempre** y la ventana de "sin señal" se cierra.

    Este test afirma ese límite en vez de taparlo: es el punto 3 de la TASK.
    Cuando el volumen cuente desde el último rebuild, **este test tiene que
    fallar** y alguien tiene que venir a leer esto.
    """
    cm = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    assert cm._last_rebuild_signal is False, "la ventana se cerró antes de 6"

    cm.on_message(_Msg("weapons policy and evidence are contested"))   # el 6º
    assert len(cm._corpus._texts) >= cm._corpus.min_texts * 2
    assert cm._last_rebuild_signal is True, (
        "el volumen no levantó la señal en 2*min_texts: revisar la cuenta"
    )


def test_cp1_el_criterio_de_tiempo_no_participa_en_la_ventana(monitor) -> None:
    """
    Que la señal siga en False dentro de la ventana no es porque el tiempo lo
    permita por poco: `_ciclos_sin_rebuild` se queda muy lejos de `MAX_CICLOS`.

    Sin esto, el CP1 podría estar pasando por un margen de uno y nadie lo vería.
    """
    cm = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    assert cm._ciclos_sin_rebuild < MAX_CICLOS
    assert MAX_CICLOS - cm._ciclos_sin_rebuild >= 5, (
        f"el criterio de tiempo está al borde: {cm._ciclos_sin_rebuild}/{MAX_CICLOS}"
    )


def test_cp1_el_estructural_no_emitio_y_se_declara(monitor) -> None:
    """
    El tercer criterio: el estructural (gradiente de `D_ckm` positivo en 3
    pasos) **no emitió** en la ventana.

    Y se declara **por qué no se puede afirmar más que eso**: la medición previa
    del 28 sep dice que en vivo *"el estructural no emitía con D_ckm
    cuantizado"*. Así que un False acá **no prueba que el criterio funcione**;
    prueba que no emitió con estas cinco entradas. Que emita cuando debe es el
    **CP2**, con entrada conocida.
    """
    cm = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    assert cm._corpus.should_rebuild(cm._d_ckm_history, n=3) is False
    # cuántos puntos de D_ckm hubo: si son menos de n, el criterio no pudo
    # evaluarse y eso es distinto de haber evaluado y dado False
    assert len(cm._d_ckm_history) <= 3, (
        f"hubo {len(cm._d_ckm_history)} puntos de D_ckm: declarar si el "
        f"criterio se evaluó de verdad"
    )


# ── CP2: cada criterio dispara con entrada conocida y deja su causal_event ──

def _ultimo_causal_event(cm) -> str:
    """El `causal_event` de la última versión de W registrada."""
    return cm._corpus._w_versions.history()[-1].causal_event


def test_cp2_estructural_dispara_con_gradiente_positivo(monitor) -> None:
    """
    **CP2, estructural.** Historia de `D_ckm` construida a mano (pedido de
    Opus), con **n+1 puntos y gradiente positivo en los tres pasos**.

    Se construye a mano y no se espera que el canal la produzca, porque la
    medición del 28 sep dice que en vivo *"el estructural no emitía con D_ckm
    cuantizado"*. Con entrada conocida se prueba el **criterio**; que el canal
    la produzca es otra cosa y no se afirma acá.
    """
    cm = monitor
    for t in TEXTOS[:3]:                      # W existe, sin llegar al volumen
        cm.on_message(_Msg(t))
    assert cm._corpus.w_sha() is not None

    # **El canal agrega un punto de `D_ckm` real después de que yo ponga la
    # historia**, así que una historia ascendente que termine arriba deja el
    # último gradiente negativo y el criterio en False. Mi primera versión de
    # este test ponía `[0.10, 0.20, 0.30, 0.40]` y fallaba por eso: la entrada
    # "conocida" no lo era.
    #
    # Así que la historia se construye **por debajo** del valor que el canal
    # agrega, y el test **declara de qué depende**: si ese valor cambia, acá
    # falla en vez de pasar por otro motivo.
    d_del_canal = cm._d_ckm_history[-1]
    assert d_del_canal == 0.0, (
        f"el canal ahora agrega D_ckm={d_del_canal}: rearmar la historia"
    )
    cm._d_ckm_history = [-0.4, -0.3, -0.2, -0.1]   # n+1 = 4 puntos, ascendentes
    assert cm._corpus.should_rebuild(cm._d_ckm_history, n=3) is True

    sha_antes = cm._corpus.w_sha()
    cm.on_message(_Msg("evidence about weapons is disputed by analysts"))
    # con el punto del canal (0.0) la serie sigue ascendiendo
    assert cm._d_ckm_history[-5:] == [-0.4, -0.3, -0.2, -0.1, 0.0]

    assert cm._last_rebuild_causa == "estructural", (
        f"disparó otro criterio: {cm._last_rebuild_causa}"
    )
    assert cm._ultimo_rebuild["ocurrio"] is True
    assert _ultimo_causal_event(cm) == "rebuild_por_decision:estructural"
    assert cm._corpus.w_sha() != sha_antes, "la decisión no movió W"


def test_cp2_estructural_no_dispara_si_no_llega_a_n(monitor) -> None:
    """
    **El caso que no llega a `n`** (pedido de Opus). `should_rebuild` pide
    `n+1` puntos: con **exactamente n=3** devuelve False.

    Importa la diferencia: con menos de `n+1` el criterio **no pudo
    evaluarse**, y eso no es lo mismo que haberlo evaluado y que el gradiente
    no fuera positivo. Las dos cosas devuelven `False` y son distintas.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))

    cm._d_ckm_history = [0.10, 0.20, 0.30]        # 3 puntos: uno menos que n+1
    assert cm._corpus.should_rebuild(cm._d_ckm_history, n=3) is False
    # y con el cuarto, el mismo gradiente sí dispara: lo que faltaba era el punto
    assert cm._corpus.should_rebuild([0.10, 0.20, 0.30, 0.40], n=3) is True


def test_cp2_estructural_no_dispara_con_gradiente_no_monotono(monitor) -> None:
    """Cuatro puntos pero un gradiente negativo en medio: no es sostenido."""
    cm = monitor
    assert cm._corpus.should_rebuild([0.10, 0.30, 0.20, 0.40], n=3) is False


def test_cp2_volumen_dispara_y_deja_su_causal_event(monitor) -> None:
    """
    **CP2, volumen.** Entrada conocida: los textos necesarios para cruzar
    `min_texts * 2` sin que el estructural ni el tiempo participen.
    """
    cm = monitor
    for t in TEXTOS:                           # 5 textos: todavía sin señal
        cm.on_message(_Msg(t))
    assert cm._last_rebuild_causa is None
    sha_antes = cm._corpus.w_sha()

    cm.on_message(_Msg("weapons policy and evidence are contested"))   # el 6º

    assert cm._last_rebuild_causa == "volumen"
    assert cm._ultimo_rebuild["ocurrio"] is True
    assert _ultimo_causal_event(cm) == "rebuild_por_decision:volumen"
    assert cm._corpus.w_sha() != sha_antes


def test_cp2_tiempo_dispara_y_deja_su_causal_event(monitor) -> None:
    """
    **CP2, tiempo.** Se arma la entrada poniendo `_ciclos_sin_rebuild` en el
    umbral, con el estructural sin puntos y el volumen por debajo.

    Es el único de los tres que **no se puede producir con textos** dentro de
    la ventana sin que el volumen gane primero: con `min_texts=3` el volumen
    dispara en el texto 6 y el tiempo necesita 10 mensajes sin rebuild. Así que
    la entrada se arma a mano, **y queda declarado**.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))
    cm._d_ckm_history = []                     # el estructural no participa
    cm._ciclos_sin_rebuild = MAX_CICLOS        # el tiempo, en el umbral
    sha_antes = cm._corpus.w_sha()

    cm.on_message(_Msg("the firearms debate has no shared evidence base"))

    assert cm._last_rebuild_causa == "tiempo", (
        f"con 4 textos el volumen no debería ganar: {cm._last_rebuild_causa}"
    )
    assert _ultimo_causal_event(cm) == "rebuild_por_decision:tiempo"
    assert cm._corpus.w_sha() != sha_antes


def test_cp2_la_jerarquia_se_respeta(monitor) -> None:
    """
    **Estructural > volumen > tiempo.** Con los tres criterios en True a la
    vez, la causa es `estructural`.

    Sin este test, la jerarquía estaría sólo en un comentario: el `elif` podría
    reordenarse y nada lo diría.
    """
    cm = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))                 # volumen quedará en True
    cm._d_ckm_history = [-0.4, -0.3, -0.2, -0.1]   # estructural (ver el test
    #                                        de arriba: el canal agrega 0.0)
    cm._ciclos_sin_rebuild = MAX_CICLOS        # tiempo en True

    cm.on_message(_Msg("analysts disagree about the firearms evidence"))
    assert cm._last_rebuild_causa == "estructural"
    assert _ultimo_causal_event(cm) == "rebuild_por_decision:estructural"


def test_cp2_rebuild_suspendido_no_bloquea_la_decision(monitor) -> None:
    """
    **TASK, punto 1.** El flag impide el rebuild automático **por ingesta**; el
    rebuild por decisión no pasa por ahí.
    """
    cm = monitor
    assert cm._corpus._rebuild_suspendido is True, "el canal vivo va suspendido"
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    sha_antes = cm._corpus.w_sha()
    cm.on_message(_Msg("weapons policy and evidence are contested"))
    assert cm._corpus.w_sha() != sha_antes, (
        "rebuild_suspendido bloqueó un rebuild por decisión"
    )


def test_cp2_una_causa_vacia_no_es_una_decision(monitor) -> None:
    """
    `rebuild_por_decision` **exige la causa**. Un rebuild sin causa declarada
    no es una decisión: es un rebuild sin nombre, y su `causal_event` mentiría.

    Misma forma que `n_agentes` esta mañana: no hay default.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))
    for vacia in ("", None):
        with pytest.raises(ValueError, match="causa"):
            cm._corpus.rebuild_por_decision(vacia)


def test_cp2_en_acumulacion_no_reconstruye_y_lo_dice(monitor) -> None:
    """
    Con el corpus en acumulación no hay W que reconstruir. **Devolver un status
    normal haría que un rebuild que no ocurrió se viera igual que uno que sí.**
    """
    cm = monitor
    cm.on_message(_Msg(TEXTOS[0]))             # 1 texto: por debajo de min_texts
    st = cm._corpus.rebuild_por_decision("volumen")
    assert st["rebuild"] is False
    assert st["motivo_no_rebuild"] == "corpus_en_acumulacion"
    assert st["causa_pedida"] == "volumen"


def test_cp2_el_panel_lleva_la_causa(monitor) -> None:
    """El `causal_event` en el panel (TASK, punto 2)."""
    cm = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    panel = cm.get_state()
    assert panel["rebuild_senal"] is False
    assert panel["rebuild_causa"] is None, "None es 'no hubo', no 'no sé'"
    assert panel["ultimo_rebuild_por_decision"] is None

    cm.on_message(_Msg("weapons policy and evidence are contested"))
    panel = cm.get_state()
    assert panel["rebuild_senal"] is True
    assert panel["rebuild_causa"] == "volumen"
    assert panel["ultimo_rebuild_por_decision"]["causal_event"] == \
        "rebuild_por_decision:volumen"


def test_cp2_el_punto_de_calibrate_existe_y_no_hace_nada(monitor) -> None:
    """
    **TASK, punto 5.** El lugar donde va `calibrate` queda marcado y declarado
    como no implementado. Sin la marca, mañana habría que buscarlo de nuevo.
    """
    cm = monitor
    for t in TEXTOS:
        cm.on_message(_Msg(t))
    assert cm.get_state()["punto_calibrate"] is None, "no hubo salto todavía"

    cm.on_message(_Msg("weapons policy and evidence are contested"))
    pc = cm.get_state()["punto_calibrate"]
    assert pc["existe"] is True
    assert pc["implementado"] is False
    assert pc["task"] == "TASK_calibrate_mecanismo_v1"


def test_cp2_el_marcador_force_w_pos_no_se_pierde_con_la_causa(tmp_path) -> None:
    """
    `force_w_pos` marca en la traza que esa W fue forzada, y **dos tests lo usan
    como traza** (`test_wmixta_forzado_paso3`, `test_armstrong_wmixta_forced_wpos`).
    Al agregar la causa, el marcador tenía que seguir estando: una W forzada por
    decisión no puede verse como una W normal.
    """
    from corpus_service import CorpusService

    # `rebuild_suspendido=True` para que la segunda ingesta NO reconstruya, y
    # así el rebuild por decisión sea el que produce esa W.
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3,
                      top_k=8, force_w_pos=True, rebuild_suspendido=True)
    c.ingest(TEXTOS[:3])                       # primera W, por ingesta
    assert c._w_versions.history()[-1].causal_event == "rebuild_debug_force_w_pos"

    # **`register` deduplica por sha** ("si W es idéntica, no crea marca
    # duplicada", `w_version.py:79-84`). Mi primera versión de este test
    # reconstruía los mismos textos: W salía idéntica, no se registraba marca
    # nueva, y lo que leía era el `causal_event` de la ingesta. Por eso acá
    # entra un texto más: para que W cambie de verdad.
    c.ingest(TEXTOS[3:5])                      # suspendido: no reconstruye
    c.rebuild_por_decision("volumen")

    ev = c._w_versions.history()[-1].causal_event
    assert ev == "rebuild_por_decision:volumen+debug_force_w_pos", ev
