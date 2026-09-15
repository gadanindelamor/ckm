"""
test_gatekeeper_c1.py — verificación de TASK_gatekeeper_C1_theta_W_v1 (D1)

Condiciones declaradas:
  - W = W_ckm_corpus_v2.json — W_pos, 0 pesos negativos.
  - Núcleo A = los 16 nodos de mayor para_counts. No es la fi de DEFS §7
    (no se reproduce con este JSON).
  - sigma es parámetro: activos=A y activos=todos.

Ejecutar:
    pytest tests/test_gatekeeper_c1.py -v -s
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "services"))
from gatekeeper_c1 import c1, c1_max_conn
from ckm_landscape_config import CKMlandscapeConfig

N_A = 16
MIN_CONN_A = 0.01399   # medida en el análisis previo a la TASK


@pytest.fixture(scope="module")
def corpus():
    d = json.loads((ROOT / "services" / "W_ckm_corpus_v2.json").read_text())
    W = np.array(d["W"], dtype=float)
    freq = np.array([d["para_counts"][n] for n in d["nodes"]])
    orden = np.argsort(-freq, kind="stable")
    return W, orden[:N_A], orden[N_A:], d["nodes"]


def _sigma(N, activos):
    s = np.full(N, -1.0)
    s[activos] = 1.0
    return s


SIGMAS = ["A", "todos"]


def _sigma_de(nombre, W, A):
    N = W.shape[0]
    return _sigma(N, A) if nombre == "A" else np.ones(N)


def _pasan(W, sigma, nodos, theta):
    return sum(c1(W, sigma, int(i), theta_W=theta) for i in nodos)


def test_condicion_W_pos(corpus):
    W, *_ = corpus
    assert (W < 0).sum() == 0


@pytest.mark.parametrize("sigma_nombre", SIGMAS)
def test_theta_010_rechaza_A(corpus, sigma_nombre):
    W, A, B, _ = corpus
    assert _pasan(W, _sigma_de(sigma_nombre, W, A), A, 0.10) == 0


@pytest.mark.parametrize("sigma_nombre", SIGMAS)
def test_A_pasa_bajo_min_conn(corpus, sigma_nombre):
    W, A, B, _ = corpus
    s = _sigma_de(sigma_nombre, W, A)
    assert min(c1_max_conn(W, s, int(i)) for i in A) == pytest.approx(MIN_CONN_A, abs=1e-5)
    assert _pasan(W, s, A, MIN_CONN_A - 1e-5) == N_A


@pytest.mark.parametrize("sigma_nombre", SIGMAS)
def test_semantica_igual_a_core(corpus, sigma_nombre):
    sys.path.insert(0, str(ROOT / "process" / "initial_static_model"))
    from core import CKMGraph, CKMConfig

    W, A, B, nodes = corpus
    s = _sigma_de(sigma_nombre, W, A)
    for theta in (0.10, 0.00598, MIN_CONN_A):
        g = CKMGraph(nodes=nodes, W=W, config=CKMConfig(theta_W=theta))
        g.sigma = s.copy()
        for i in range(W.shape[0]):
            assert g.gatekeeper(i).c1 == c1(W, s, i, theta_W=theta)


@pytest.mark.parametrize("sigma_nombre", SIGMAS)
def test_tabla_medicion(corpus, sigma_nombre):
    """Valores declarados, no fórmula. Imprime la tabla (-s)."""
    W, A, B, _ = corpus
    cfg = CKMlandscapeConfig.from_W(W, theta_W=0.0, sampling_mode="uniform", scale="log")
    s = _sigma_de(sigma_nombre, W, A)
    filas = [
        ("mu_W_global",    cfg.mu_W_global),
        ("0.1*max|W|",     0.1 * np.abs(W).max()),
        ("mu_W_nonzero",   cfg.mu_W_nonzero),
        ("2*mu_W_nonzero", 2 * cfg.mu_W_nonzero),
    ]
    print(f"\nactivos={sigma_nombre}")
    for nombre, t in filas:
        a, b = _pasan(W, s, A, t), _pasan(W, s, B, t)
        print(f"  {nombre:15s} {t:.5f}  A {a}/{N_A}  B {b}/{len(B)}")
        assert a == N_A   # todas las candidatas quedan bajo MIN_CONN_A
