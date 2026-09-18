"""
test_basin_distance.py — verificación de TASK_distancia_frontera_d_sigma_v1

Ejecutar:
    pytest tests/test_basin_distance.py -v
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from landscape_engine import basin_distance, relax_orbit


def _ferro(N=7):
    """Todos acoplados +1: dos cuencas, todo +1 y todo −1 (N impar, sin empates
    en el estado de mayoría)."""
    W = np.ones((N, N))
    np.fill_diagonal(W, 0)
    return W


def test_interior_de_cuenca_d_es_mayoria():
    """Desde todo +1 con N=7, hay que voltear 4 para caer en la otra cuenca."""
    W = _ferro(7)
    r = basin_distance(np.ones(7), W, k_max=5, k_exhaustivo=5)
    assert r["d"] == 4 and r["exacto"]


def test_frontera_d_es_uno():
    """4 en +1 y 3 en −1 relaja a +1; voltear un +1 lo pasa a −1."""
    W = _ferro(7)
    s = np.array([1, 1, 1, 1, -1, -1, -1], dtype=float)
    assert relax_orbit(s, W)[0] == relax_orbit(np.ones(7), W)[0]
    r = basin_distance(s, W, k_max=3)
    assert r["d"] == 1 and r["exacto"]
    assert r["evaluadas"] <= 7


def test_sin_cambio_hasta_k_max_devuelve_none():
    W = _ferro(7)
    r = basin_distance(np.ones(7), W, k_max=3, k_exhaustivo=3)
    assert r["d"] is None and r["exacto"]


def test_otra_fase_de_la_misma_orbita_no_es_cambio():
    """Órbita de período 2: (1,1) ↔ (−1,−1). Son la MISMA órbita; la
    comparación de basin_distance es sobre este frozenset, no sobre el estado."""
    W = np.array([[0., -1.], [-1., 0.]])
    o1, per1, _, _ = relax_orbit(np.array([1., 1.]), W)
    o2, per2, _, _ = relax_orbit(np.array([-1., -1.]), W)
    assert per1 == per2 == 2
    assert o1 == o2


def test_d_mayor_o_igual_a_uno_y_determinista():
    rng = np.random.default_rng(0)
    W = rng.uniform(-1, 1, (12, 12))
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0)
    s = np.where(rng.random(12) > 0.5, 1., -1.)
    a = basin_distance(s, W, k_max=4, seed=7)
    b = basin_distance(s, W, k_max=4, seed=7)
    assert a == b
    assert a["d"] is None or a["d"] >= 1


def test_muestreo_se_declara_no_exacto():
    """k > k_exhaustivo con C(N,k) > n_muestras → exacto=False."""
    W = _ferro(15)
    r = basin_distance(np.ones(15), W, k_max=8, k_exhaustivo=1, n_muestras=50)
    assert r["d"] == 8 and r["exacto"] is False
