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
from landscape_engine import (
    basin_masses, count_attractors, d_ckm, deprecated_count_attractors,
    deprecated_d_ckm, n_eff,
)
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

# ── deprecated_d_ckm — la distancia por conteo (TASK_d_ckm_al_engine_v1) ────
# Desde el 5 de octubre de 2026 `d_ckm` mide masa de cuenca y delega en
# d_masa_cuencas; la forma lineal por conteo quedo en `deprecated_d_ckm`.
# Estos cuatro tests hacen la operacion lineal y por eso la llaman a ella.
# Se testea la operacion, haciendola: no se verifica contra la formula
# escrita en ningun lado.

def test_d_ckm_hace_la_operacion():
    """Usa deprecated_d_ckm: la operacion lineal (A0 - A) / A0 ya no es la
    de d_ckm."""
    assert deprecated_d_ckm(4, 10) == 0.6          # 10 - 4 = 6; 6 / 10 = 0.6
    assert deprecated_d_ckm(10, 10) == 0.0         # sin cambio
    assert deprecated_d_ckm(1, 4) == 0.75


def test_d_ckm_negativo_cuando_el_paisaje_gano_atractores():
    """Usa deprecated_d_ckm. Negativo no es deficit: A_actual > A0 es mas
    atractores que el baseline. El nombre "distancia" es incorrecto en ese
    sentido y se conserva por regresion."""
    assert deprecated_d_ckm(15, 10) == -0.5
    assert deprecated_d_ckm(32, 2) == -15.0        # el caso que da la base de COCO


def test_d_ckm_borde_A0_cero_devuelve_cero():
    """Usa deprecated_d_ckm, que conserva el borde tal cual de los dos
    servicios: 0.0 aunque diga "sin cambio" donde no hubo medicion. d_ckm
    devuelve None en ese borde, como d_masa_cuencas — ver
    test_d_ckm_es_d_masa_cuencas."""
    assert deprecated_d_ckm(3, 0) == 0.0


def test_d_ckm_devuelve_float_de_python():
    """Usa deprecated_d_ckm. d_ckm devuelve np.float64 (el de np.log en
    d_masa_cuencas), que es subclase de float pero no `float`."""
    assert type(deprecated_d_ckm(4, 10)) is float


# ── d_ckm — masa de cuenca, escala log (delega en d_masa_cuencas) ───────────

def test_d_ckm_es_d_masa_cuencas():
    """d_ckm hace 1 - ln A / ln A0. Mismos valores y mismo borde que
    d_masa_cuencas: baseline <= 1 no tiene distancia que medir -> None."""
    assert d_ckm(4.0, 4.0) == pytest.approx(0.0)       # sin cambio
    assert d_ckm(2.0, 4.0) == pytest.approx(0.5)       # ln 2 / ln 4 = 1/2
    assert d_ckm(1.0, 4.0) == pytest.approx(1.0)       # colapso
    assert d_ckm(8.0, 4.0) == pytest.approx(-0.5)      # gana diversidad
    assert d_ckm(3.0, 1.0) is None
    assert d_ckm(3.0, 0.0) is None


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
    el conteo de estados terminales puede dar más. Usa
    deprecated_count_attractors: count_attractors ya no cuenta terminales,
    devuelve N_eff."""
    W = _W(N=12, seed=5)
    masas = basin_masses(W, n_runs=100, seed=0)
    terminales = deprecated_count_attractors(W, n_runs=100, seed=0)
    assert len(masas) <= terminales


# ── La formula canonica, de punta a punta ───────────────────────────────────
# D_ckm = 1 - ln N_eff / ln N_eff0, con N_eff = 1 / sum(m^2) sobre las masas
# de cuenca. Cada test hace la cuenta a mano desde las masas y la compara con
# lo que devuelve el codigo; no llama a n_eff ni a d_masa_cuencas para
# obtener el valor esperado.

def test_count_attractors_es_n_eff_sobre_masas():
    """count_attractors conserva el nombre y devuelve 1 / sum(m^2)."""
    W = _W(N=12, seed=5)
    masas = basin_masses(W, n_runs=100, seed=0)
    a_mano = 1.0 / float(np.sum(masas ** 2))
    assert count_attractors(W, n_runs=100, seed=0) == pytest.approx(a_mano)
    assert a_mano != len(masas)                 # no es el conteo de orbitas


def test_d_ckm_es_la_formula_canonica_sobre_masas():
    """d_ckm(count_attractors(W_t), count_attractors(W_0)) es
    1 - ln N_eff / ln N_eff0, hecho a mano desde las masas."""
    W0 = _W(N=12, seed=5)
    Wt = _W(N=12, seed=6)
    m0 = basin_masses(W0, n_runs=100, seed=0)
    mt = basin_masses(Wt, n_runs=100, seed=0)
    n0 = 1.0 / float(np.sum(m0 ** 2))
    nt = 1.0 / float(np.sum(mt ** 2))
    a_mano = 1.0 - np.log(nt) / np.log(n0)
    D = d_ckm(count_attractors(Wt, n_runs=100, seed=0),
              count_attractors(W0, n_runs=100, seed=0))
    assert D == pytest.approx(a_mano)
    assert a_mano != 0.0                        # las dos W difieren


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

    # texto que cambia los nodos con N igual BAJO LA REGLA DE DESEMPATE
    # (conserva precedente): el anterior ("police response…") ahora sube N.
    c.ingest(["bans reduce assault weapons and gun violence"])
    p3 = m.evaluate("rights weapons")
    assert p3["Delta_r_reset"] == "nodos"
    assert p3["N_eff0"] == p3["N_eff"]            # nuevo baseline con la W nueva

    lineas = [json.loads(l) for l in (tmp_path / "m.jsonl").read_text().splitlines()]
    assert all("N_eff" in r["panel"] and "N_eff0" in r["panel"] for r in lineas)


def test_panel_D_ckm_es_la_formula_canonica(tmp_path):
    """En el panel de Monitor, D_ckm es 1 - ln N_eff / ln N_eff0 con los
    N_eff y N_eff0 del mismo panel, y coincide con D_masa_cuencas."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"), n_runs_attractors=20)

    paneles = [m.evaluate(t) for t in ("rights weapons", "rights bans",
                                       "gun violence", "background checks")]
    assert any(p["N_eff"] != p["N_eff0"] for p in paneles)   # hay algo que medir
    for p in paneles:
        assert p["N_eff0"] > 1.0
        a_mano = 1.0 - np.log(p["N_eff"]) / np.log(p["N_eff0"])
        assert p["D_ckm"] == pytest.approx(a_mano, abs=1e-3)  # panel redondea a 4
        assert p["D_ckm"] == p["D_masa_cuencas"]


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


def test_panel_declara_condicion_W(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"), n_runs_attractors=20)
    cw = m.evaluate("rights weapons")["condicion_W"]
    assert cw["w_sha"] == c.w_sha() and cw["N"] == len(c.get_nodes())
    assert cw["n_runs"] == 20 and cw["count_seed"] == 0
    # la clave "D_ckm" cambio de cantidad el 5 oct 2026: el panel declara cual
    assert cw["D_ckm_forma"] == "masa_log"
    W = c.get_W()
    assert cw["aislados_W"] == [c.get_nodes()[i] for i in range(len(W)) if not W[i].any()]
    assert set(cw["aislados_W_eff"]) <= set(cw["aislados_W"])


def test_panel_lleva_senal_de_saturacion(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"), n_runs_attractors=40)
    p = m.evaluate("rights weapons")
    s = p["saturacion"]
    assert s["N_eff_sobre_n_runs"] == pytest.approx(p["N_eff"] / 40, abs=1e-3)
    assert 0.0 <= s["orbitas_unicas_frac"] <= 1.0


def test_n_runs_default_es_1000(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"))
    assert m.evaluate("rights weapons")["condicion_W"]["n_runs"] == 1000
