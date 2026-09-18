"""
test_invalidacion_delta_r.py — verificación de TASK_invalidacion_delta_r_v1 (D2)

Ejecutar:
    pytest tests/test_invalidacion_delta_r.py -v
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
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
PROMPT = "gun control laws reduce violence"


def _monitor(corpus, tmp_path):
    return MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                          n_runs_attractors=10)


@pytest.fixture
def corpus(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    assert c.mode == "evaluation"
    return c


def test_sin_rebuild_acumula(corpus, tmp_path):
    m = _monitor(corpus, tmp_path)
    p1 = m.evaluate(PROMPT)
    A0 = m._A0
    p2 = m.evaluate("armed citizens protect rights")
    assert p1["Delta_r_reset"] is None and p2["Delta_r_reset"] is None
    assert m._A0 == A0
    assert p2["Delta_r_sum"] >= p1["Delta_r_sum"]


def test_reset_por_nodos(corpus, tmp_path):
    m = _monitor(corpus, tmp_path)
    m.evaluate(PROMPT)
    nodes_antes = corpus.get_nodes()
    # texto que cambia los nodos con N igual BAJO LA REGLA DE DESEMPATE
    # (conserva precedente): el anterior ("police response…") ahora sube N.
    corpus.ingest(["bans reduce assault weapons and gun violence"])
    assert len(corpus.get_nodes()) == len(nodes_antes)   # N igual
    assert corpus.get_nodes() != nodes_antes             # nodos distintos

    panel = m.evaluate(PROMPT)
    assert panel["Delta_r_reset"] == "nodos"


def test_reset_por_N(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=2, top_k=20)
    c.ingest(["gun control", "gun rights"])
    m = _monitor(c, tmp_path)
    m.evaluate("gun control")
    c.ingest(TEXTS)
    assert len(c.get_nodes()) != 2
    panel = m.evaluate("gun control")
    assert panel["Delta_r_reset"] == "N"
    assert m._Delta_r.shape == (len(c.get_nodes()),) * 2


def test_reset_por_pesos(corpus, tmp_path):
    """Mismos nodos, mismo orden, pesos distintos: registrar la W nueva."""
    m = _monitor(corpus, tmp_path)
    m.evaluate(PROMPT)
    nodes = corpus.get_nodes()

    W2 = corpus.get_W() * 0.5
    corpus._W = W2
    corpus._w_versions.register(W2, len(corpus._texts), causal_event="test_pesos")
    assert corpus.get_nodes() == nodes

    panel = m.evaluate(PROMPT)
    assert panel["Delta_r_reset"] == "pesos"
    assert m._A0 is not None   # recalculado sobre la W nueva


def test_delta_r_y_A0_en_cero_tras_reset(corpus, tmp_path):
    m = _monitor(corpus, tmp_path)
    m.evaluate(PROMPT)
    A0_viejo = m._A0
    # texto que cambia los nodos con N igual BAJO LA REGLA DE DESEMPATE
    # (conserva precedente): el anterior ("police response…") ahora sube N.
    corpus.ingest(["bans reduce assault weapons and gun violence"])

    # estado justo después de invalidar, antes de volver a acumular
    causa = m._invalidar_si_W_cambio(corpus.get_nodes())
    assert causa == "nodos"
    assert np.all(m._Delta_r == 0)
    assert m._A0 is None and A0_viejo is not None
