"""
test_delta_compresiones_coco.py — verificación de TASK_delta_compresiones_coco_v1 (D3)

Ejecutar:
    pytest tests/test_delta_compresiones_coco.py -v
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from coco import COCO
from corpus_service import CorpusService
from monitor_service import MonitorService

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]
# Prompts elegidos para que el campo metabolice pares (medido: "rights
# weapons" y "rights bans" dejan pares en Δ_r con este corpus y top_k=10).
PROMPTS = [
    "rights weapons",
    "rights bans",
    "gun control laws reduce violence",
    "rights weapons",
    "rights bans",
    "rights weapons",
]


def _W(N=8, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.uniform(-1, 1, (N, N))
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0)
    return W


def _sym(rng, N, hi=3):
    D = rng.integers(0, hi, (N, N)).astype(float)
    D = D + D.T
    np.fill_diagonal(D, 0)
    return D


# ── COCO aislado ────────────────────────────────────────────────────────────

def test_nace_en_ceros():
    c = COCO(W=_W())
    assert np.all(c.delta_state() == 0)


def test_sin_compresion_iguala_al_de_monitor():
    """Umbral inalcanzable: sólo incrementos incorporados → igual al total."""
    W = _W()
    c = COCO(W=W, d_ckm_threshold=10.0, n_runs=10)
    rng = np.random.default_rng(1)
    monitor_delta = np.zeros_like(W)
    for _ in range(4):
        monitor_delta = monitor_delta + _sym(rng, W.shape[0])
        ts = c.observe(monitor_delta)
        assert not ts.stop_applied
        assert np.array_equal(c.delta_state(), monitor_delta)


def test_con_compresion_diverge_y_persiste():
    """Umbral en 0: comprime siempre. Lo comprimido no se pisa con el total."""
    W = _W()
    c = COCO(W=W, d_ckm_threshold=0.0, dynamic_alpha=False, alpha_star=0.5, n_runs=10)
    rng = np.random.default_rng(2)
    d1 = _sym(rng, W.shape[0]) + 1 - np.eye(W.shape[0])
    ts = c.observe(d1)
    if not ts.stop_applied:
        pytest.skip("D_ckm < 0 en esta W — no comprime")
    assert np.allclose(c.delta_state(), 0.5 * d1)

    inc = _sym(rng, W.shape[0])
    d2 = d1 + inc
    ts2 = c.observe(d2)
    esperado = 0.5 * d1 + inc
    if ts2.stop_applied:
        esperado = 0.5 * esperado
    assert np.allclose(c.delta_state(), esperado)
    assert not np.allclose(c.delta_state(), d2)


def test_observe_no_muta_la_entrada():
    W = _W()
    c = COCO(W=W, d_ckm_threshold=0.0, dynamic_alpha=False, alpha_star=0.1, n_runs=10)
    d = _sym(np.random.default_rng(3), W.shape[0])
    copia = d.copy()
    c.observe(d)
    assert np.array_equal(d, copia)


# ── Monitor + COCO ──────────────────────────────────────────────────────────

@pytest.fixture
def corpus(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    return c


def _correr(corpus, tmp_path, nombre, thermostat):
    m = MonitorService(corpus, storage_path=str(tmp_path / f"{nombre}.jsonl"),
                       n_runs_attractors=10, thermostat=thermostat)
    panels = [m.evaluate(p) for p in PROMPTS]
    return m, panels


def test_delta_r_de_monitor_no_depende_de_coco(corpus, tmp_path):
    """Con y sin thermostat, Δ_r de Monitor es idéntico panel a panel."""
    th = COCO(W=corpus.get_W(), d_ckm_threshold=0.0, dynamic_alpha=False,
              alpha_star=0.05, n_runs=10)
    m_sin, p_sin = _correr(corpus, tmp_path, "sin", None)
    m_con, p_con = _correr(corpus, tmp_path, "con", th)

    assert p_sin[-1]["Delta_r_sum"] > 0, "sin pares metabolizados — el test no discrimina"
    assert [p["Delta_r_sum"] for p in p_sin] == [p["Delta_r_sum"] for p in p_con]
    assert np.array_equal(m_sin._Delta_r, m_con._Delta_r)
    assert any(p["thermostat"]["stop_applied"] for p in p_con), "no hubo compresión"
    assert not np.allclose(th.delta_state(), m_con._Delta_r)


def test_monitor_no_reasigna_desde_coco():
    src = (Path(__file__).parent.parent / "services" / "monitor_service.py").read_text()
    evaluate = src.split("def evaluate(")[1].split("\n    def ")[0]
    assert "delta_state" not in evaluate
