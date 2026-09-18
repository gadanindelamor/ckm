"""
test_neff_y_frontera.py — verificación de TASK_neff_y_frontera_logica_v1

Lógica antes que datos: N_eff y cluster_frontier_density con entradas
armadas a mano.

Ejecutar:
    pytest tests/test_neff_y_frontera.py -v
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from landscape_engine import basin_masses, count_attractors, n_eff
from cluster_frontier_density import OPOSICION, cluster_frontier_density
from corpus_service import CorpusService
from monitor_service import MonitorService


def _W(N=10, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.uniform(-1, 1, (N, N))
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0)
    return W


# ── N_eff ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("k", [1, 2, 5, 17])
def test_n_eff_masas_uniformes_da_k(k):
    assert n_eff(np.ones(k) / k) == pytest.approx(k)


def test_n_eff_dominada_por_la_cuenca_grande():
    # una cuenca de 0.9 y nueve de 0.0111: se comporta cerca de 1, no de 10
    m = np.array([0.9] + [0.1 / 9] * 9)
    assert 1.0 < n_eff(m) < 1.3


def test_basin_masses_suma_uno_y_es_reproducible():
    W = _W()
    a = basin_masses(W, n_runs=80, seed=3)
    b = basin_masses(W, n_runs=80, seed=3)
    assert a.sum() == pytest.approx(1.0)
    assert np.array_equal(a, b)
    assert np.all(np.diff(a) <= 0)                  # ordenadas desc
    assert 1 <= len(a) <= 80


def test_basin_masses_agrupa_orbitas_no_terminales():
    """Una órbita de período 2 alcanzada por sus dos fases es UNA entrada;
    count_attractors cuenta estados terminales y puede dar más."""
    W = _W(N=12, seed=5)
    masas = basin_masses(W, n_runs=100, seed=0)
    terminales = count_attractors(W, n_runs=100, seed=0)
    assert len(masas) <= terminales


# ── cluster_frontier_density ────────────────────────────────────────────────

NODES = ["a", "b", "c", "d", "e"]


def _W_bloques(intra_A, intra_B, inter):
    """A = {a,b}, B = {c,d}, e aislado en su propio cluster."""
    W = np.zeros((5, 5))
    W[0, 1] = W[1, 0] = intra_A
    W[2, 3] = W[3, 2] = intra_B
    for i in (0, 1):
        for j in (2, 3):
            W[i, j] = W[j, i] = inter
    return W


CL = {"A": ["a", "b"], "B": ["c", "d"]}


def test_frontera_positiva():
    r = cluster_frontier_density(CL, NODES, _W_bloques(0.8, 0.6, 0.2))
    assert r["coercivity"]["A|B"] == pytest.approx(min(0.8, 0.6) / 0.2)
    assert r["inter"]["A|B"] == pytest.approx(0.2)


def test_frontera_nula_es_inf():
    r = cluster_frontier_density(CL, NODES, _W_bloques(0.8, 0.6, 0.0))
    assert r["coercivity"]["A|B"] == float("inf")


def test_frontera_negativa_es_oposicion_no_inf():
    r = cluster_frontier_density(CL, NODES, _W_bloques(0.8, 0.6, -0.3))
    assert r["coercivity"]["A|B"] == OPOSICION
    assert r["coercivity"]["A|B"] != float("inf")
    assert r["inter"]["A|B"] == pytest.approx(-0.3)


def test_cluster_de_un_nodo_da_intra_cero():
    cl = {"A": ["a", "b"], "E": ["e"]}
    W = _W_bloques(0.8, 0.6, 0.0)
    W[0, 4] = W[4, 0] = 0.4
    W[1, 4] = W[4, 1] = 0.4
    r = cluster_frontier_density(cl, NODES, W)
    assert r["intra"]["E"] == 0.0
    assert r["n_pairs"]["E"] == 0
    assert r["coercivity"]["A|E"] == 0.0          # porosa — anotado, no se cambia


def test_intra_negativo_da_coercividad_negativa():
    r = cluster_frontier_density(CL, NODES, _W_bloques(-0.5, 0.6, 0.2))
    assert r["coercivity"]["A|B"] == pytest.approx(-0.5 / 0.2)


def test_salida_serializable_a_json():
    r = cluster_frontier_density(CL, NODES, _W_bloques(0.8, 0.6, -0.3))
    vuelta = json.loads(json.dumps(r))
    assert vuelta["coercivity"]["A|B"] == OPOSICION


# ── Panel de Monitor ────────────────────────────────────────────────────────

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]


def test_panel_lleva_n_eff_y_baseline_que_se_resetea(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"), n_runs_attractors=20)

    p1 = m.evaluate("rights weapons")
    assert p1["N_eff"] >= 1.0
    assert p1["N_eff0"] == p1["N_eff"]            # primera del ciclo
    base = m._N_eff0

    m.evaluate("rights bans")
    assert m._N_eff0 == base                      # se conserva sin cambio de W

    c.ingest(["police response times matter for community safety"])
    p3 = m.evaluate("rights weapons")
    assert p3["Delta_r_reset"] == "nodos"
    assert p3["N_eff0"] == p3["N_eff"]            # nuevo baseline con la W nueva

    lineas = [json.loads(l) for l in (tmp_path / "m.jsonl").read_text().splitlines()]
    assert all("N_eff" in r["panel"] and "N_eff0" in r["panel"] for r in lineas)


# ── D_masa_cuencas (log) ────────────────────────────────────────────────────

from landscape_engine import d_masa_cuencas  # noqa: E402


def test_d_masa_log_valores():
    assert d_masa_cuencas(4.0, 4.0) == pytest.approx(0.0)
    assert d_masa_cuencas(1.0, 4.0) == pytest.approx(1.0)       # colapso
    assert d_masa_cuencas(8.0, 4.0) == pytest.approx(-0.5)      # gana diversidad
    assert d_masa_cuencas(2.0, 4.0) == pytest.approx(0.5)


@pytest.mark.parametrize("n0", [None, 1.0, 0.5])
def test_d_masa_borde_none(n0):
    assert d_masa_cuencas(3.0, n0) is None
