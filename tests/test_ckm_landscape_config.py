"""
test_ckm_landscape_config.py — verificación de TASK_CKMlandscapeConfig_v1

Ejecutar:
    pytest tests/test_ckm_landscape_config.py -v
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pytest

SERVICES = Path(__file__).parent.parent / "services"
sys.path.insert(0, str(SERVICES))
from ckm_landscape_config import CKMlandscapeConfig
from coco import COCO


@pytest.fixture(scope="module")
def W():
    d = json.loads((SERVICES / "W_ckm_corpus_v2.json").read_text())
    return np.array(d["W"], dtype=float)


def _cfg(W):
    return CKMlandscapeConfig.from_W(W, theta_W=0.01, sampling_mode="uniform", scale="log")


def test_mu_W_ambas_formas(W):
    c = _cfg(W)
    assert c.N == 32
    assert c.mu_W_nonzero == pytest.approx(0.005977, abs=1e-6)
    assert c.mu_W_global  == pytest.approx(0.004519, abs=1e-6)


def test_beta_c_global_coincide_con_coco(W):
    c = _cfg(W)
    assert c.beta_c_global == pytest.approx(COCO(W=W).beta_c_corpus())


@pytest.mark.parametrize("falta", ["theta_W", "sampling_mode", "scale"])
def test_parametros_obligatorios(W, falta):
    kw = dict(theta_W=0.01, sampling_mode="uniform", scale="log")
    del kw[falta]
    with pytest.raises(TypeError):
        CKMlandscapeConfig.from_W(W, **kw)


def test_theta_W_formula_no_implementada():
    with pytest.raises(NotImplementedError):
        CKMlandscapeConfig.theta_W_formula(0.005, 32)


def test_json_roundtrip(W):
    c = _cfg(W)
    assert CKMlandscapeConfig.from_json(c.to_json()) == c


def test_identidades(W):
    a, b = _cfg(W), _cfg(W)
    assert a.w_version_id == b.w_version_id
    assert a.config_id != b.config_id


def test_w_version_id_cambia_con_W(W):
    W2 = W.copy()
    W2[0, 1] = W2[1, 0] = W2[0, 1] + 0.01
    assert _cfg(W).w_version_id != _cfg(W2).w_version_id
