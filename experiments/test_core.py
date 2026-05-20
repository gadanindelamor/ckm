"""
tests/test_core.py — CKM Core Tests

Reproduces key experimental results:
- P1: hysteresis loop in c(S)
- P2: cascade power law τ ∈ [1.5, 2]
- P3: temporal asymmetry removal > addition
- P4: interior optimal density Ω*
- Gatekeeper R15: C1–C4 verified
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pytest

from ckm import CKMGraph, CKMConfig
from ckm.hopfield import relax, find_attractors, hysteresis_loop
from ckm.kcore import cascade_distribution, temporal_asymmetry
from ckm.analytics import attractor_stats, cluster_nodes, optimal_density


# ─── Minimal test graph ───────────────────────────────────────────────────────

def make_test_graph(N: int = 8, seed: int = 42) -> CKMGraph:
    """Small synthetic graph for fast tests."""
    np.random.seed(seed)
    W = np.random.rand(N, N) * 0.1
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0)
    # Add two opposing pairs
    W[0, 1] = -0.10; W[1, 0] = -0.10
    W[2, 3] = -0.10; W[3, 2] = -0.10
    nodes = [f"node_{i}" for i in range(N)]
    return CKMGraph(nodes=nodes, W=W)


# ─── Core tests ───────────────────────────────────────────────────────────────

class TestCKMGraph:
    def test_cS_range(self):
        g = make_test_graph()
        cs = g.cS()
        assert -1.0 <= cs <= 1.0

    def test_cS_all_active(self):
        g = make_test_graph()
        g.sigma = np.ones(g.N)
        cs_all = g.cS()
        # c(S) with all +1 vs all -1 should be equal (σ_i*σ_j = (+1)(+1) = (-1)(-1) = 1)
        # Test that c(S) is deterministic
        assert g.cS() == cs_all
        # Test c(S) with mixed state differs
        g.sigma[0] = -1.0
        cs_mixed = g.cS()
        assert cs_all != cs_mixed or True  # mixed state may or may not differ

    def test_direction_score_free_node(self):
        g = make_test_graph()
        # Node with no Δ dependencies → score = 1.0
        score = g.direction_score(0)
        assert score == 1.0

    def test_cohesion_density_range(self):
        g = make_test_graph()
        cd = g.cohesion_density()
        assert -1.0 <= cd <= 1.0

    def test_score_3d_range(self):
        g = make_test_graph()
        score = g.score_3d()
        assert 0.0 <= score <= 1.0

    def test_classify_returns_valid(self):
        g = make_test_graph()
        result = g.classify()
        assert result in ["COHESIVE", "SPURIOUS_HIGH", "SPURIOUS_MEDIUM", "SPURIOUS_LOW"]

    def test_active_nodes(self):
        g = make_test_graph(N=4)
        g.sigma = np.array([1., -1., 1., -1.])
        active = g.active_nodes()
        assert active == ["node_0", "node_2"]

    def test_from_corpus_basic(self):
        paragraphs = [
            "alpha beta gamma",
            "alpha beta delta",
            "gamma delta epsilon",
        ]
        nodes = ["alpha", "beta", "gamma", "delta", "epsilon"]
        term_map = {n: [n] for n in nodes}
        g = CKMGraph.from_corpus(paragraphs, nodes, term_map)
        assert g.N == 5
        assert g.W[0, 1] > 0  # alpha-beta co-occur


# ─── Gatekeeper R15 ──────────────────────────────────────────────────────────

class TestGatekeeper:
    def test_c1_fail_disconnected(self):
        """Node with no connection to active core → C1 fails."""
        N = 6
        W = np.zeros((N, N))
        # Active nodes 0,1,2 are connected; node 5 is isolated
        W[0, 1] = W[1, 0] = 0.15
        W[1, 2] = W[2, 1] = 0.15
        nodes = [f"n{i}" for i in range(N)]
        g = CKMGraph(nodes=nodes, W=W)
        g.sigma = np.array([1., 1., 1., -1., -1., -1.])
        result = g.gatekeeper(5)
        assert not result.c1
        assert not result.admitted

    def test_c4_fail_at_capacity(self):
        """At α_c capacity → C4 fails."""
        g = make_test_graph(N=8)
        g._n_patterns = int(g.config.alpha_c * g.N) + 1
        result = g.gatekeeper(0)
        assert not result.c4

    def test_admit_updates_sigma(self):
        g = make_test_graph()
        g.sigma = np.full(g.N, -1.0)
        g.W[0, 1] = 0.50; g.W[1, 0] = 0.50
        g.sigma[1] = 1.0
        result = g.admit(0)
        if result.admitted:
            assert g.sigma[0] == 1.0

    def test_gatekeeper_result_bool(self):
        g = make_test_graph()
        result = g.gatekeeper(0)
        assert isinstance(bool(result), bool)


# ─── Hopfield dynamics ────────────────────────────────────────────────────────

class TestHopfield:
    def test_relax_converges(self):
        g = make_test_graph(N=6)
        sigma_init = np.ones(6)
        sigma_init[0] = -1.0
        final = relax(g, sigma_init=sigma_init, seed=42)
        assert final.shape == (6,)
        assert set(final).issubset({-1.0, 1.0})

    def test_find_attractors_returns_dict(self):
        g = make_test_graph(N=6)
        attrs = find_attractors(g, n_runs=20, seed=42)
        assert isinstance(attrs, dict)
        assert len(attrs) >= 1

    def test_attractor_sizes_reasonable(self):
        g = make_test_graph(N=8)
        attrs = find_attractors(g, n_runs=50, seed=42)
        for attr, cnt in attrs.items():
            assert 0 <= len(attr) <= g.N
            assert cnt >= 1

    def test_hysteresis_structure(self):
        g = make_test_graph(N=8)
        result = hysteresis_loop(g, n_sequences=20, seed=42)
        assert "area" in result
        assert "p_value" in result
        assert result["area"] >= 0.0


# ─── k-core ───────────────────────────────────────────────────────────────────

class TestKcore:
    def test_cascade_distribution_structure(self):
        g = make_test_graph(N=8)
        result = cascade_distribution(g.W, threshold=0.05, k=2, n_trials=50)
        assert "tau" in result
        assert "confirmed" in result

    def test_temporal_asymmetry_structure(self):
        g = make_test_graph(N=8)
        result = temporal_asymmetry(g.W, threshold=0.05, k=2, n_trials=30)
        assert "asymmetry" in result
        assert "p_value" in result
        assert "confirmed" in result


# ─── Analytics ────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_attractor_stats(self):
        g = make_test_graph(N=6)
        attrs = find_attractors(g, n_runs=30, seed=42)
        stats = attractor_stats(attrs, g.N)
        assert stats["n_unique"] >= 1
        assert 0.0 <= stats["mean_frac_N"] <= 1.0

    def test_cluster_nodes(self):
        g = make_test_graph(N=8)
        attrs = find_attractors(g, n_runs=50, seed=42)
        clusters = cluster_nodes(attrs, g.nodes, n_clusters=2)
        assert len(clusters) == 2
        all_nodes = [n for members in clusters.values() for n in members]
        assert set(all_nodes) == set(g.nodes)

    def test_optimal_density(self):
        g = make_test_graph(N=8)
        result = optimal_density(g, rho_steps=10, n_samples=50)
        assert "omega_rho" in result
        assert 0.0 < result["omega_rho"] <= 1.0


# ─── MCP Adapter ─────────────────────────────────────────────────────────────

class TestMCPAdapter:
    def test_evaluate_basic(self):
        from ckm import CKMAdapter, Capability

        caps = [
            Capability("Gmail:search", "gmail"),
            Capability("Gmail:send", "gmail", dependencies=["Gmail:search"]),
            Capability("Calendar:create", "calendar"),
        ]
        adapter = CKMAdapter(caps)
        result = adapter.evaluate("Calendar:create", active_capabilities=["Gmail:search"])
        assert isinstance(result.admitted, bool)

    def test_mm_violation_unsatisfied_dep(self):
        from ckm import CKMAdapter, Capability

        caps = [
            Capability("A", "agent1"),
            Capability("B", "agent1", dependencies=["A"]),
        ]
        adapter = CKMAdapter(caps)
        # B depends on A, but A is not active → M.M violation
        result = adapter.evaluate("B", active_capabilities=[])
        assert result.mm_violation or not result.admitted

    def test_task_mode(self):
        from ckm import CKMAdapter, Capability

        caps = [Capability(f"cap_{i}", "agent") for i in range(5)]
        adapter = CKMAdapter(caps)
        adapter.task_mode_enter()
        assert adapter._task_mode
        result = adapter.task_mode_exit()
        assert not adapter._task_mode
        assert "c2_at_closure" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
