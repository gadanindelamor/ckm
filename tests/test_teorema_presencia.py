"""
test_teorema_presencia.py — CP-T de TASK_condiciones_del_paper_v1

**El teorema de presencia es un teorema** (`DEFS_CKM_estado_actual_v16.md`
§1.1 h): *"Con presencia sola no hay triángulo con producto de signos negativo
y T(W) = 0 por construcción."* La demostración es de una línea:

1. Con `force_w_pos` —o con textos sin marcadores— todo par va a `pos_counts`
   (`corpus_service.py:322-331`), así que `raw = pos − neg ≥ 0`, y dividir por
   `max_abs = |raw|.max() ≥ 0` no cambia el signo. ⇒ **ningún Wᵢⱼ < 0**.
2. El producto de tres números ≥ 0 es ≥ 0. ⇒ **0 triángulos frustrados**.
3. T = Σ|Wᵢⱼ| sobre los negativos / Σ|Wᵢⱼ|. Sin negativos el numerador es 0.
   ⇒ **T(W) = 0**.

**Entonces este archivo no verifica la matemática: verifica el INSTRUMENTO.**
Que el código haga lo que dice el álgebra. Es lo que la TASK pide cuando
escribe *"si falla, el instrumento hace otra cosa que la matemática"*. Por eso
los casos son **los caminos que podrían romperlo** —el flag, el texto, la W de
ceros— y no un barrido de corpus: correr el teorema sobre N corpus es correr N
veces lo demostrable.

**El control es la mitad del test.** Afirmar "no hay negativos" sobre un corpus
que nunca los tuvo no distingue nada. `test_el_control_si_tiene_negativos` es
lo que hace que los demás midan algo.

`T(W)` **no está en el código**: no existe en `services/` ni en
`iap_chatroom/`. Se computa acá, desde la definición de DEFS v16, y es del
test, no del servicio.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
from services.corpus_service import CorpusService   # noqa: E402


# Mismo vocabulario compartido en todos: sin él los puntajes empatan y no hay
# nodos (ver test_op5_empate_total_en_el_bootstrap_no_da_nodos_ni_W).
CON_MARCADORES = [
    "gun control reduces gun violence in cities",
    "however gun control laws do not reduce gun violence",
    "gun violence and gun control but the data is unclear",
    "gun rights and gun control although violence persists",
]
SIN_MARCADORES = [
    "gun control reduces gun violence in cities",
    "gun control laws shape gun violence outcomes",
    "gun violence and gun control appear together",
    "gun rights and gun control share gun violence framing",
]


def T(W: np.ndarray) -> float:
    """
    T(W) = Σ|Wᵢⱼ| sobre los Wᵢⱼ < 0, dividido Σ|Wᵢⱼ|.

    DEFS v16, tabla. **No está en `services/`**: se computa acá.
    """
    total = np.abs(W).sum()
    if total == 0:
        return 0.0
    return float(np.abs(W[W < 0]).sum() / total)


def frustrados(W: np.ndarray) -> int:
    """Triángulos con producto de los 3 signos < 0, saltando los nulos.
    Misma definición que `experiments/orbit_analytics.py:405`."""
    S = np.sign(W)
    n = 0
    for i, j, k in itertools.combinations(range(W.shape[0]), 3):
        a, b, c = S[i, j], S[j, k], S[i, k]
        if a and b and c and a * b * c < 0:
            n += 1
    return n


def _W(tmp_path, nombre, textos, **kw):
    c = CorpusService(storage_path=str(tmp_path / f"{nombre}.json"),
                      min_texts=3, top_k=8, **kw)
    c.ingest(textos)
    W = c.get_W()
    assert W is not None, f"{nombre}: sin W el caso no mide nada"
    return c, W


# ---------------------------------------------------------------------------
# El control: sin él los demás no distinguen nada
# ---------------------------------------------------------------------------

def test_el_control_si_tiene_negativos(tmp_path):
    """
    El mismo corpus **sin forzar y con marcadores** tiene que dar negativos.
    Si no los diera, los tests de abajo pasarían sobre una W que nunca pudo
    tener un negativo, y no estarían midiendo el teorema.
    """
    _, W = _W(tmp_path, "control", CON_MARCADORES)
    assert (W < 0).any(), "sin negativos acá, el resto del archivo es vacío"
    assert T(W) > 0


# ---------------------------------------------------------------------------
# Los dos caminos al teorema
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("nombre,textos,kw", [
    # el flag: saltea el ruteo aunque el texto TENGA marcadores
    ("forzada", CON_MARCADORES, {"force_w_pos": True}),
    # el texto: `is_opp` sale falso por el corpus, no por el flag
    ("sin_marcadores", SIN_MARCADORES, {}),
])
def test_ningun_W_negativo(tmp_path, nombre, textos, kw):
    _, W = _W(tmp_path, nombre, textos, **kw)
    assert not (W < 0).any(), f"{nombre}: {(W < 0).sum()} entradas negativas"


@pytest.mark.parametrize("nombre,textos,kw", [
    ("forzada", CON_MARCADORES, {"force_w_pos": True}),
    ("sin_marcadores", SIN_MARCADORES, {}),
])
def test_cero_triangulos_frustrados(tmp_path, nombre, textos, kw):
    _, W = _W(tmp_path, nombre, textos, **kw)
    assert frustrados(W) == 0


@pytest.mark.parametrize("nombre,textos,kw", [
    ("forzada", CON_MARCADORES, {"force_w_pos": True}),
    ("sin_marcadores", SIN_MARCADORES, {}),
])
def test_T_de_W_es_cero(tmp_path, nombre, textos, kw):
    _, W = _W(tmp_path, nombre, textos, **kw)
    assert T(W) == 0.0


def test_la_forzada_queda_marcada_en_la_traza(tmp_path):
    """
    Que el teorema valga **no puede** hacer indistinguible una W forzada de una
    natural: la condición bajo la que vale tiene que estar escrita.
    """
    c, _ = _W(tmp_path, "marcada", CON_MARCADORES, force_w_pos=True)
    assert c._w_versions.history()[-1].causal_event == "rebuild_debug_force_w_pos"
    assert c.declaracion_extraccion()[
        "operadores"]["7_signo"]["parametros"]["force_w_pos"] is True


# ---------------------------------------------------------------------------
# El borde: W de ceros
# ---------------------------------------------------------------------------

def test_una_W_de_ceros_tambien_cumple():
    """
    `max_abs == 0` no divide (`corpus_service.py:339`). Una W de ceros no tiene
    negativos, no tiene triángulos con signo, y T = 0 por el guard del
    denominador — no por el teorema. Queda fijado para que la diferencia se
    vea.
    """
    W = np.zeros((5, 5))
    assert not (W < 0).any()
    assert frustrados(W) == 0
    assert T(W) == 0.0
