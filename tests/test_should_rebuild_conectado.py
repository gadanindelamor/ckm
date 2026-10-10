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


# Con el volumen por ciclo (CP3) hacen falta `min_texts*2` textos **después**
# del primer rebuild, y el primero ocurre al cruzar `min_texts`. Con
# `min_texts=3`: W en el texto 3, y el volumen dispara en el **9**.
TEXTOS_EXTRA = [
    "policy debates about firearms lack shared evidence",
    "analysts dispute the weapons statistics",
    "the evidence base on guns is contested by both sides",
    "regulation of weapons divides the available data",
]
TODOS = TEXTOS + TEXTOS_EXTRA           # 9 textos


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


def test_cp3_la_ventana_sin_senal_llega_hasta_2x_min_texts_POR_CICLO(monitor) -> None:
    """
    **Este test estaba escrito al revés, y es el mismo test.**

    En el CP1 decía: *"el criterio de volumen es `len(_texts) >= min_texts*2`
    sobre el **total del corpus**, así que a partir del texto 6 la señal queda
    en True para siempre y la ventana de 'sin señal' se cierra"*, y afirmaba
    justamente eso — con la nota de que **cuando el volumen contara por ciclo
    tenía que fallar, y que alguien viniera a leerlo**.

    Falló en el CP3, como estaba anunciado. **No se borra** (instrucción de
    Opus): se convierte en la afirmación del comportamiento nuevo, con la traza
    de por qué fallaba arriba.

    Lo que afirma ahora: el volumen cuenta **desde el último rebuild**, así que
    la ventana no se cierra en el texto 6 sino en el **9** — `min_texts=3`, W en
    el 3, y `min_texts*2 = 6` textos más.
    """
    cm = monitor
    for i, txt in enumerate(TODOS[:8], start=1):
        cm.on_message(_Msg(txt))
        assert cm._last_rebuild_signal is False, (
            f"la señal se levantó en el texto {i} con "
            f"{cm._textos_desde_rebuild} desde el rebuild"
        )

    # el texto 9: seis desde el rebuild del texto 3
    cm.on_message(_Msg(TODOS[8]))
    assert cm._textos_desde_rebuild == 0, "el salto no reinició la cuenta"
    assert cm._last_rebuild_causa == "volumen"

    # **Y el total ya había pasado 2*min_texts hace rato**: eso es lo que antes
    # disparaba y ahora no.
    assert len(cm._corpus._texts) > cm._corpus.min_texts * 2


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
    # **La serie que disparó ya no está** (CP4): el salto reinicia la historia,
    # así que el ciclo nuevo arranca sin la pendiente de la meseta anterior.
    # Antes del CP4 esta línea afirmaba
    # `cm._d_ckm_history[-5:] == [-0.4, -0.3, -0.2, -0.1, 0.0]` —la serie
    # sobrevivía al salto— y falló en el CP4, como correspondía.
    assert cm._d_ckm_history == [], (
        f"la historia sobrevivió al salto: {cm._d_ckm_history}"
    )

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
    for t in TODOS[:8]:                        # ocho: todavía sin señal
        cm.on_message(_Msg(t))
    assert cm._last_rebuild_causa is None
    sha_antes = cm._corpus.w_sha()

    cm.on_message(_Msg(TODOS[8]))              # el 9º: seis desde el rebuild

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
    for t in TODOS[:8]:
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
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    sha_antes = cm._corpus.w_sha()
    cm.on_message(_Msg(TODOS[8]))
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
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    panel = cm.get_state()
    assert panel["rebuild_senal"] is False
    assert panel["rebuild_causa"] is None, "None es 'no hubo', no 'no sé'"
    assert panel["ultimo_rebuild_por_decision"] is None

    cm.on_message(_Msg(TODOS[8]))
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
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    assert cm.get_state()["punto_calibrate"] is None, "no hubo salto todavía"

    cm.on_message(_Msg(TODOS[8]))
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


# ── CP3: el volumen cuenta desde el último rebuild ─────────────────────────

def test_cp3_no_dispara_en_el_mensaje_siguiente_al_rebuild(monitor) -> None:
    """
    **CP3, el test que pide la TASK.** Con el volumen sobre el total, después de
    `2*min_texts` la señal quedaba en `True` **para siempre**: con el CP2 eso
    dispara **un rebuild por mensaje**, que es el rebuild continuo que delamor
    descartó. El CP2 solo no lo arreglaba — lo movía de lugar.
    """
    cm = monitor
    for t in TODOS:                            # llega al salto por volumen
        cm.on_message(_Msg(t))
    assert cm._last_rebuild_causa == "volumen"
    assert cm._textos_desde_rebuild == 0

    # el mensaje siguiente al salto: NO dispara
    cm.on_message(_Msg("more contested claims about weapons and evidence"))
    assert cm._textos_desde_rebuild == 1
    assert cm._last_rebuild_causa is None, (
        "disparó en el mensaje siguiente al rebuild: el volumen sigue contando "
        "el total"
    )
    assert cm._last_rebuild_signal is False


def test_cp3_el_volumen_vuelve_a_disparar_al_completar_el_ciclo(monitor) -> None:
    """
    No dispara al siguiente **y sí vuelve a disparar** cuando el ciclo nuevo
    junta sus `2*min_texts`. Sin esto, "no dispara" podría ser "no dispara
    nunca más", que sería la otra forma de romperlo.
    """
    cm = monitor
    for t in TODOS:
        cm.on_message(_Msg(t))
    assert cm._last_rebuild_causa == "volumen"          # primer salto

    vueltas = []
    for i in range(1, 7):                               # seis más
        cm.on_message(_Msg(f"contested evidence number {i} about weapons"))
        vueltas.append((i, cm._textos_desde_rebuild, cm._last_rebuild_causa))

    causas = [c for _, _, c in vueltas]
    assert causas[:5] == [None] * 5, f"disparó antes de completar: {vueltas}"
    assert causas[5] == "volumen", f"no volvió a disparar: {vueltas}"


def test_cp3_la_cuenta_se_reinicia_tambien_en_el_rebuild_por_ingesta(monitor) -> None:
    """
    El reset está atado al **sha**, no a la vía: la primera W la construye la
    ingesta, y el ciclo que nace ahí arranca su cuenta en cero igual.

    Si el reset estuviera sólo en el camino de la decisión, el primer ciclo
    contaría los textos de la acumulación y dispararía antes de tiempo.
    """
    cm = monitor
    cm.on_message(_Msg(TODOS[0]))
    assert cm._textos_desde_rebuild == 1
    cm.on_message(_Msg(TODOS[1]))
    assert cm._textos_desde_rebuild == 2
    cm.on_message(_Msg(TODOS[2]))              # acá nace W
    assert cm._corpus.w_sha() is not None
    assert cm._textos_desde_rebuild == 0, (
        "el ciclo que nace con la primera W arrancó con la cuenta de la "
        "acumulación"
    )


def test_cp3_el_umbral_no_se_toco(monitor) -> None:
    """
    **Lo que el CP3 cambió es sobre qué se cuenta, no el umbral.** `2*min_texts`
    sigue siendo el valor de antes: su calibración no es de este TASK.
    """
    cm = monitor
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    assert cm._textos_desde_rebuild == cm._corpus.min_texts * 2 - 1
    assert cm._last_rebuild_causa is None
    cm.on_message(_Msg(TODOS[8]))
    assert cm._last_rebuild_causa == "volumen"


# ── CP2b: la decisión se persiste en el state_dir ──────────────────────────

def test_cp2b_una_decision_sin_cambio_de_W_queda_en_el_jsonl(monitor) -> None:
    """
    **El caso que no dejaba traza en ningún lado.** `w_version` deduplica por
    sha (*"si W es idéntica, no crea marca duplicada"*), así que una decisión
    que no mueve W **no deja versión**. Y antes del CP2b tampoco dejaba nada en
    disco: vivía en `get_state()` y se iba con el proceso.

    Acá se fuerza: dos rebuild por decisión seguidos sobre los mismos textos.
    El segundo produce la misma W.
    """
    cm = monitor
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    sha = cm._corpus.w_sha()

    # **Dos rebuild seguidos, sin textos nuevos en medio.** Mi primera versión
    # hacía uno solo y suponía que daba la misma W: era falso, porque el último
    # rebuild había sido con 3 textos y ahora hay 8, así que W cambia. La misma
    # W aparece recién al reconstruir **lo mismo dos veces**.
    cm._corpus.rebuild_por_decision("volumen")           # esta sí mueve W
    sha = cm._corpus.w_sha()
    st = cm._corpus.rebuild_por_decision("volumen")      # esta no
    assert st["rebuild"] is True
    assert cm._corpus.w_sha() == sha, "el test necesita que W no se mueva"
    n_versiones_antes = len(cm._corpus._w_versions.history())

    # el registro lo escribe el camino del monitor, así que se invoca derecho
    reg = cm._registrar_decision("volumen", st, sha, {"t": 1.0, "tick": 7,
                                                      "reloj": "canal"})
    assert reg["w_cambio"] is False, "no se declaró que W no se movió"
    assert reg["w_sha_antes"] == reg["w_sha_despues"] == sha
    assert reg["ocurrio"] is True, "la decisión sí se tomó"
    assert reg["reloj"] == "canal", "el reloj tiene que ser el del canal"

    # y `w_version` no registró nada nuevo: por eso hace falta el jsonl
    assert len(cm._corpus._w_versions.history()) == n_versiones_antes

    en_disco = cm.decisiones_de_rebuild()
    assert en_disco[-1]["w_cambio"] is False
    assert cm._decisiones_path.exists()


def test_cp2b_la_decision_con_salto_queda_con_w_cambio_true(monitor) -> None:
    """El otro lado: cuando W se mueve, la misma línea lo dice."""
    cm = monitor
    for t in TODOS:
        cm.on_message(_Msg(t))
    assert cm._last_rebuild_causa == "volumen"

    d = cm.decisiones_de_rebuild()
    assert d, "no se registró ninguna decisión"
    assert d[-1]["causa"] == "volumen"
    assert d[-1]["w_cambio"] is True
    assert d[-1]["w_sha_antes"] != d[-1]["w_sha_despues"]
    assert d[-1]["reloj"] == "canal", "no se usó el reloj del canal"
    assert d[-1]["n_puntos_d_ckm"] is not None


def test_cp2b_las_vueltas_sin_senal_no_se_registran(monitor) -> None:
    """
    Acordado: **una línea por mensaje sería el ruido** que el filtro del canal
    existe para evitar. Que la señal nunca se levantó se lee de que el archivo
    esté vacío, más el panel.
    """
    cm = monitor
    for t in TODOS[:8]:                        # ninguna señal
        cm.on_message(_Msg(t))
    assert cm.decisiones_de_rebuild() == []
    assert cm.get_state()["n_decisiones_registradas"] == 0


def test_cp2b_un_reinicio_a_mitad_de_meseta_no_reinicia_los_contadores(
    tmp_path, monkeypatch
) -> None:
    """
    **El cambio de comportamiento, declarado.** Hasta el CP2b
    `_ciclos_sin_rebuild` vivía en memoria, así que **el criterio de tiempo
    arrancaba de cero en cada reinicio**: con `MAX_CICLOS = 10`, un canal que
    se reiniciaba cada menos de 10 mensajes **no disparaba por tiempo nunca**, y
    nada lo decía.

    Acá se simula el reinicio: se tira la instancia y se construye otra sobre
    el mismo `state_dir`.
    """
    state = tmp_path / "_state"

    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm1 = CKMMonitor(min_texts=3, state_dir=state)
    for t in TODOS[:7]:
        cm1.on_message(_Msg(t))
    textos_antes = cm1._textos_desde_rebuild
    ciclos_antes = cm1._ciclos_sin_rebuild
    hist_antes = list(cm1._d_ckm_history)
    assert textos_antes > 0, "el test necesita estar a mitad de meseta"

    # ── el reinicio ──
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm2 = CKMMonitor(min_texts=3, state_dir=state)

    assert cm2._textos_desde_rebuild == textos_antes, (
        f"la cuenta de volumen se reinició: {cm2._textos_desde_rebuild} "
        f"contra {textos_antes}"
    )
    assert cm2._ciclos_sin_rebuild == ciclos_antes, (
        "el criterio de tiempo volvió a arrancar de cero"
    )
    assert cm2._d_ckm_history == hist_antes
    assert cm2._rebuild_state_error is None
    monkeypatch.setattr(CKMMonitor, "_instance", None)


def test_cp2b_el_jsonl_sobrevive_al_reinicio_y_la_cuenta_sigue(
    tmp_path, monkeypatch
) -> None:
    """Append-only: el reinicio no pisa lo registrado, y `t` sigue de donde iba."""
    state = tmp_path / "_state"

    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm1 = CKMMonitor(min_texts=3, state_dir=state)
    for t in TODOS:
        cm1.on_message(_Msg(t))
    assert len(cm1.decisiones_de_rebuild()) == 1

    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm2 = CKMMonitor(min_texts=3, state_dir=state)
    assert len(cm2.decisiones_de_rebuild()) == 1, "el reinicio pisó el jsonl"
    assert cm2._n_decisiones == 1, "el índice `t` no siguió de donde iba"
    monkeypatch.setattr(CKMMonitor, "_instance", None)


def test_cp2b_un_estado_ilegible_no_se_tapa_con_los_defaults(
    tmp_path, monkeypatch
) -> None:
    """
    Un archivo roto **no se lee como "arrancá de cero"**: los contadores
    arrancan de cero —que es lo de antes del CP2b— y el panel **lo dice**.
    Taparlo haría que un estado perdido se viera igual que un canal nuevo.
    """
    state = tmp_path / "_state"
    state.mkdir(parents=True)
    (state / "rebuild_state.json").write_text("{esto no es json")

    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm = CKMMonitor(min_texts=3, state_dir=state)
    assert cm._ciclos_sin_rebuild == 0
    assert cm._rebuild_state_error is not None
    # el nombre de la excepción, cualquiera sea: lo que importa es que quede
    assert cm._rebuild_state_error.split(":")[0] in (
        "JSONDecodeError", "ValueError", "TypeError", "KeyError", "OSError"
    ), cm._rebuild_state_error
    assert cm.get_state()["rebuild_state_error"] is not None
    monkeypatch.setattr(CKMMonitor, "_instance", None)


def test_cp2b_los_dos_archivos_van_en_el_mismo_state_dir(monitor, tmp_path) -> None:
    """
    Criterio de congruencia de delamor: **mismo `state_dir`, mismos
    mecanismos** — JSONL para eventos, JSON para estado.
    """
    cm = monitor
    for t in TODOS:
        cm.on_message(_Msg(t))
    nombres = {f.name for f in cm.state_dir.iterdir()}
    assert "rebuild_decisions.jsonl" in nombres
    assert "rebuild_state.json" in nombres
    assert "corpus_state.json" in nombres          # los de siempre siguen
    assert "monitor_trajectory.jsonl" in nombres


def test_cp4_la_historia_de_d_ckm_se_persiste_POR_CICLO(monitor) -> None:
    """
    **Este test estaba escrito al revés, y es el mismo test.**

    En el CP2b decía: *"se persiste como está hoy: acumulada. Reiniciarla en el
    salto es el CP4, y el archivo lo declara para que no se lea como si ya lo
    fuera"*, y afirmaba `d_ckm_history_es_por_ciclo is False`.

    Falló en el CP4, como estaba anunciado. **No se borra**: se convierte en la
    afirmación del comportamiento nuevo, con la traza arriba — igual que el test
    de la ventana del CP1 en el CP3.
    """
    import json as _json
    cm = monitor
    for t in TODOS:
        cm.on_message(_Msg(t))
    d = _json.loads((cm.state_dir / "rebuild_state.json").read_text())
    assert "d_ckm_history" in d
    assert d["d_ckm_history_es_por_ciclo"] is True
    # y lo persistido es la del ciclo vigente: el salto la dejó vacía
    assert d["d_ckm_history"] == []


def test_cp2b_los_contadores_de_una_meseta_no_pasan_a_otra(
    tmp_path, monkeypatch
) -> None:
    """
    **Pedido de delamor.** El JSON de estado guarda el `w_sha` del ciclo, y al
    arrancar, si no coincide con la W del corpus, **los contadores se descartan
    y queda escrita la causa**.

    Es la misma forma que el CP0 encontró en la Firma: un número de un ciclo
    sellado con la identidad de otro. Restaurar acá haría que el volumen y el
    tiempo de la meseta anterior corrieran contra la W nueva, y el panel diría
    una cuenta que no es de esta meseta.

    Se simula: se guarda el estado, se mueve W por otro camino (sin que el
    estado se actualice) y se reinicia.
    """
    import json as _json
    state = tmp_path / "_state"

    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm1 = CKMMonitor(min_texts=3, state_dir=state)
    for t in TODOS[:7]:
        cm1.on_message(_Msg(t))
    assert cm1._textos_desde_rebuild > 0

    d = _json.loads((state / "rebuild_state.json").read_text())
    assert d["w_sha"] == cm1._corpus.w_sha(), "el estado no guarda su w_sha"

    # W se mueve y el estado queda con el sha viejo
    cm1._corpus.rebuild_por_decision("volumen")
    assert cm1._corpus.w_sha() != d["w_sha"]
    cm1._corpus.save()

    # ── el reinicio ──
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm2 = CKMMonitor(min_texts=3, state_dir=state)

    assert cm2._textos_desde_rebuild == 0, "se arrastró la cuenta de otra meseta"
    assert cm2._ciclos_sin_rebuild == 0
    assert cm2._d_ckm_history == []

    desc = cm2._rebuild_state_descartado
    assert desc is not None, "se descartó en silencio"
    assert desc["causa"] == "w_sha_distinto"
    assert desc["w_sha_guardado"] == d["w_sha"]
    assert desc["w_sha_del_corpus"] == cm2._corpus.w_sha()
    assert set(desc["descartados"]) == {
        "ciclos_sin_rebuild", "textos_desde_rebuild", "d_ckm_history"
    }
    assert cm2.get_state()["rebuild_state_descartado"]["causa"] == "w_sha_distinto"
    # y no es un error: son dos cosas distintas con la misma consecuencia
    assert cm2._rebuild_state_error is None
    monkeypatch.setattr(CKMMonitor, "_instance", None)


def test_cp2b_descartado_y_error_no_se_colapsan(tmp_path, monkeypatch) -> None:
    """
    Un archivo roto y un estado de otra meseta **dejan los contadores en cero
    igual**, y son distintos. Si fueran un solo campo, no se podría saber si el
    estado se perdió o si cambió la meseta.
    """
    state = tmp_path / "_state"
    state.mkdir(parents=True)
    (state / "rebuild_state.json").write_text("{roto")

    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm = CKMMonitor(min_texts=3, state_dir=state)
    assert cm._rebuild_state_error is not None
    assert cm._rebuild_state_descartado is None, (
        "un archivo roto se reportó como un descarte por meseta"
    )
    monkeypatch.setattr(CKMMonitor, "_instance", None)


# ── CP4: la historia de D_ckm es por ciclo ─────────────────────────────────

def test_cp4_el_salto_reinicia_la_historia(monitor) -> None:
    """
    **CP4.** `D_ckm` se mide contra el baseline de **su** ciclo (`N_eff0` se
    fija al nacer), así que un gradiente que cruza un salto compara dos cosas
    medidas contra baselines distintos: el criterio estructural leería una
    pendiente que no existe en ninguna de las dos mesetas.
    """
    cm = monitor
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    assert cm._d_ckm_history, "el test necesita historia antes del salto"

    cm.on_message(_Msg(TODOS[8]))              # salto por volumen
    assert cm._last_rebuild_causa == "volumen"
    assert cm._d_ckm_history == [], (
        f"la historia cruzó el salto: {cm._d_ckm_history}"
    )


def test_cp4_el_punto_del_mensaje_del_salto_queda_en_la_meseta_que_cierra(
    monitor
) -> None:
    """
    El orden importa y se declara: en el camino **por decisión** el reset va
    **después** de que `evaluate` corrió, así que el punto de ese mensaje —que
    se midió contra la W **anterior** al salto— pertenece a la meseta que se
    cierra, no a la que nace.

    En el camino **por ingesta** el reset va **antes** de `evaluate`, porque
    ahí W ya cambió cuando el punto se mide: ese punto es el primero del ciclo
    nuevo. **Son dos órdenes distintos a propósito.**
    """
    cm = monitor
    cm.on_message(_Msg(TODOS[0]))
    cm.on_message(_Msg(TODOS[1]))
    cm.on_message(_Msg(TODOS[2]))              # acá nace W, por ingesta
    # el punto de este mensaje se midió con la W nueva: arranca el ciclo
    assert len(cm._d_ckm_history) <= 1, (
        f"el ciclo nuevo arrancó con puntos de la acumulación: "
        f"{cm._d_ckm_history}"
    )


def test_cp4_el_estructural_necesita_sus_n_mas_1_puntos_dentro_del_ciclo(
    monitor
) -> None:
    """
    Consecuencia de la historia por ciclo, declarada: después de un salto el
    estructural **no puede disparar** hasta que el ciclo nuevo junte sus `n+1`
    puntos. Eso **endurece** el criterio, y es lo que se quería: un gradiente
    de cuatro puntos repartidos entre dos mesetas no es una pendiente.
    """
    cm = monitor
    for t in TODOS:
        cm.on_message(_Msg(t))                 # salto
    assert cm._d_ckm_history == []
    assert cm._corpus.should_rebuild(cm._d_ckm_history, n=3) is False, (
        "el estructural disparó con la historia vacía"
    )


def test_cp4_monitor_sigue_invalidando_delta_r(monitor) -> None:
    """
    **D2 no se toca.** La invalidación de Δ_r en el cambio de W es de
    `MonitorService` y sigue como hoy: se lee en `panel["Delta_r_reset"]`.

    Se verifica que el campo **existe en el panel** y que el canal no lo
    reemplazó: tocar Monitor pide parar y reportar, y este CP4 no lo tocó.
    """
    cm = monitor
    for t in TODOS[:4]:
        cm.on_message(_Msg(t))
    assert cm._last_panel is not None
    assert "Delta_r_reset" in cm._last_panel, (
        "el panel de Monitor dejó de declarar la invalidación de Δ_r"
    )


def test_cp4_el_estado_persistido_guarda_la_historia_del_ciclo(monitor) -> None:
    """La historia que se persiste es la del ciclo vigente, no la acumulada."""
    import json as _json
    cm = monitor
    for t in TODOS[:8]:
        cm.on_message(_Msg(t))
    d = _json.loads((cm.state_dir / "rebuild_state.json").read_text())
    assert d["d_ckm_history"] == [float(x) for x in cm._d_ckm_history]
    assert d["d_ckm_history_es_por_ciclo"] is True
