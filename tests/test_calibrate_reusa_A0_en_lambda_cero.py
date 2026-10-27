"""
test_calibrate_reusa_A0_en_lambda_cero.py — el 17% de `calibrate`, verificado

27 oct 2026, CP2 de `TASK_calibrate_en_el_build_v2`, commit aparte.

`calibrate` hacía **6** llamadas a `count_attractors` con una grilla de 5 puntos
y sólo **5** eran distintas: `A0 = count_attractors(Wc)` y el punto λ=0, que es
`interpolar(Wc, W_col, 0.0)` — o sea `1.0·Wc + 0.0·W_col`—, contado con el mismo
`n_runs` y la misma seed.

**Estos tests verifican la premisa, no el ahorro.** Si la premisa no se cumpliera
—si esa interpolación no diera un resultado idéntico con la misma semilla— el
cambio no entra. La condición la puso Opus en el texto 11: *"con un test que
verifique resultado idéntico con la misma semilla. Si no sale idéntico, no entra,
y se reporta."*

No se toca el patrón: ni la grilla, ni los extremos, ni el margen.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
from calibrate import (                                        # noqa: E402
    GRILLA_LAMBDA_DEFAULT,
    N_RUNS_DEFAULT,
    SEED_DEFAULT,
    calibrate,
    extremo_colapso,
    interpolar,
)
from landscape_engine import count_attractors                  # noqa: E402

W_DEL_VIVO = RAIZ / "experiments/_state_S2-C0/corpus_state.json"


def _W_sintetica(n: int = 12, seed: int = 7) -> np.ndarray:
    """Una W con signo mixto y diagonal en cero, como las del corpus."""
    rng = np.random.default_rng(seed)
    A = rng.uniform(-1.0, 1.0, size=(n, n))
    W = (A + A.T) / 2.0
    np.fill_diagonal(W, 0.0)
    return W


def _Ws():
    """Las W sobre las que se verifica. La del vivo si está."""
    out = [("sintetica_N12", _W_sintetica()), ("sintetica_N20", _W_sintetica(20, 3))]
    if W_DEL_VIVO.exists():
        crudo = json.loads(W_DEL_VIVO.read_text()).get("W")
        if crudo is not None:
            out.append(("vivo_S2-C0", np.array(crudo)))
    return out


# ── la premisa: la interpolación en λ=0 devuelve la misma W ─────────────────

@pytest.mark.parametrize("nombre,W", _Ws())
def test_interpolar_en_lambda_cero_devuelve_la_misma_W(nombre, W) -> None:
    """
    `(1−0)·Wc + 0·W_extremo` tiene que ser `Wc`. **Se compara bit a bit.**

    Es lo único que podría no cumplirse: `0.0 · x` da `-0.0` donde `x` es
    negativo, y `-0.0 + 0.0` da `+0.0`. Por eso se mira, en vez de suponerlo.
    """
    Wc = np.asarray(W, dtype=float).copy()
    W_lam0 = interpolar(Wc, extremo_colapso(Wc), 0.0)
    assert np.array_equal(W_lam0, Wc), (
        f"[{nombre}] la interpolación en λ=0 no devolvió la misma W"
    )


@pytest.mark.parametrize("nombre,W", _Ws())
def test_el_conteo_en_lambda_cero_es_identico_al_baseline(nombre, W) -> None:
    """
    **Lo que justifica el reuso**: el mismo W, el mismo `n_runs` y la misma
    seed dan el **mismo** `N_eff`. Igualdad exacta, no tolerancia.
    """
    Wc = np.asarray(W, dtype=float).copy()
    A0 = count_attractors(Wc, n_runs=N_RUNS_DEFAULT, seed=SEED_DEFAULT)
    W_lam0 = interpolar(Wc, extremo_colapso(Wc), 0.0)
    A_lam0 = count_attractors(W_lam0, n_runs=N_RUNS_DEFAULT, seed=SEED_DEFAULT)
    assert A_lam0 == A0, (
        f"[{nombre}] el conteo en λ=0 ({A_lam0}) no es el baseline ({A0}): el "
        "reuso de A0 no entra"
    )


# ── el resultado: la curva sale igual ───────────────────────────────────────

@pytest.mark.parametrize("nombre,W", _Ws())
def test_el_punto_lambda_cero_de_la_curva_es_exactamente_cero(nombre, W) -> None:
    """
    Consecuencia directa: con `A = A0`, `d_ckm(A0, A0)` es exactamente `0.0` y
    `frac_rec` exactamente `1.0`. **Es lo que se ve en las 7 curvas de los dos
    vivos**, que corrieron antes del reuso: la igualdad ya ocurría.
    """
    reg = calibrate(np.asarray(W, dtype=float))
    curva = reg["condiciones"]["curva"]
    assert curva[0]["lambda"] == 0.0
    assert curva[0]["d_ckm"] == 0.0, "el baseline no se mide contra sí mismo"
    assert curva[0]["frac_rec"] == 1.0


def test_la_grilla_y_el_numero_de_puntos_no_cambiaron() -> None:
    """
    **El patrón no se toca.** El ahorro es de cómputo: la grilla sigue siendo la
    de siempre y la curva sigue teniendo un punto por cada λ. `n_evaluaciones`
    declara **puntos de la curva**, no conteos.
    """
    reg = calibrate(_W_sintetica())
    cond = reg["condiciones"]
    assert tuple(cond["grilla_lambda"]) == tuple(GRILLA_LAMBDA_DEFAULT)
    assert cond["n_evaluaciones"] == len(GRILLA_LAMBDA_DEFAULT)
    assert len(cond["curva"]) == len(GRILLA_LAMBDA_DEFAULT)
