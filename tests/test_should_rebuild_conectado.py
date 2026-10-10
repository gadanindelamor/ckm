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
