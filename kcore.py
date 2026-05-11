"""
ckm/kcore.py — k-core Decomposition and Cascade Analysis

k-core structural stability, cascade distribution (P2),
temporal asymmetry (P3), critical zone identification.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

import numpy as np
from scipy import stats as sp_stats


# ─── Graph construction ───────────────────────────────────────────────────────

def build_adj(W: np.ndarray, threshold: float) -> dict[int, set]:
    """Build adjacency dict from weight matrix W: edge if |W[i,j]| >= threshold."""
    N = W.shape[0]
    adj: dict[int, set] = defaultdict(set)
    for i in range(N):
        for j in range(i + 1, N):
            if abs(W[i, j]) >= threshold:
                adj[i].add(j)
                adj[j].add(i)
    for i in range(N):
        if i not in adj:
            adj[i] = set()
    return dict(adj)


# ─── k-core decomposition ─────────────────────────────────────────────────────

def kcore(adj: dict[int, set], k: int, N: Optional[int] = None) -> tuple[frozenset, int]:
    """
    Compute k-core of graph. Returns (core_nodes, n_rounds).
    n_rounds = convergence steps (used for P3 asymmetry).
    """
    if N is None:
        N = max(adj.keys()) + 1 if adj else 0

    removed: set = set()
    rounds = 0
    changed = True

    while changed:
        changed = False
        rounds += 1
        for v in range(N):
            if v not in removed:
                neighbors_active = len(adj.get(v, set()) - removed)
                if neighbors_active < k:
                    removed.add(v)
                    changed = True

    return frozenset(range(N)) - removed, rounds


# ─── Cascade measurement ──────────────────────────────────────────────────────

def cascade_after_removal(
    adj: dict[int, set],
    k: int,
    node: int,
    N: Optional[int] = None,
) -> int:
    """
    Size of k-core cascade after removing a node.
    Returns 0 if node was not in the core.
    """
    if N is None:
        N = max(adj.keys()) + 1 if adj else 0

    core_before, _ = kcore(adj, k, N)
    if node not in core_before:
        return 0

    # Remove node
    adj_new = {v: set(nbrs) for v, nbrs in adj.items()}
    for nbr in list(adj_new.get(node, set())):
        adj_new[nbr].discard(node)
    adj_new[node] = set()

    core_after, _ = kcore(adj_new, k, N)
    return len(core_before - core_after - {node})


def cascade_after_addition(
    adj: dict[int, set],
    k: int,
    node: int,
    new_edges: list[int],
    N: Optional[int] = None,
) -> tuple[int, int]:
    """
    k-core relaxation steps after adding a node with new_edges.
    Returns (cascade_size, n_rounds).
    """
    if N is None:
        N = max(adj.keys()) + 1 if adj else 0

    adj_new = {v: set(nbrs) for v, nbrs in adj.items()}
    for nbr in new_edges:
        adj_new[node].add(nbr)
        adj_new[nbr].add(node)

    core_before, _ = kcore(adj, k, N)
    core_after, rounds = kcore(adj_new, k, N)
    cascade = len(core_after) - len(core_before)
    return cascade, rounds


# ─── P2: Cascade distribution ─────────────────────────────────────────────────

def cascade_distribution(
    W: np.ndarray,
    threshold: float,
    k: int = 2,
    n_trials: int = 500,
    seed: int = 42,
) -> dict:
    """
    Measure cascade size distribution at given threshold.
    Returns tau (power-law exponent), sizes, and whether τ ∈ [1.5, 2].
    """
    np.random.seed(seed)
    N = W.shape[0]
    adj = build_adj(W, threshold)
    core, _ = kcore(adj, k, N)

    if len(core) < 3:
        return {"tau": None, "sizes": [], "confirmed": False, "core_size": len(core)}

    sizes = []
    for _ in range(n_trials):
        current_core, _ = kcore(adj, k, N)
        if not current_core:
            break
        node = np.random.choice(list(current_core))
        s = cascade_after_removal(adj, k, node, N)
        if s > 0:
            sizes.append(s)

    if len(sizes) < 10:
        return {"tau": None, "sizes": sizes, "confirmed": False, "core_size": len(core)}

    arr = np.array(sizes, dtype=float)
    # MLE estimator for discrete power law
    tau = 1.0 + len(arr) / float(np.sum(np.log(arr / 0.5)))

    return {
        "tau": float(tau),
        "sizes": sizes,
        "confirmed": 1.5 <= tau <= 2.0,
        "core_size": len(core),
        "n_cascades": len(sizes),
    }


def critical_zone(
    W: np.ndarray,
    k: int = 2,
    thresholds: Optional[list[float]] = None,
    n_trials: int = 500,
    seed: int = 42,
) -> dict[float, dict]:
    """
    Find θ range where P(s) ∝ s^-τ with τ ∈ [1.5, 2].
    Returns {threshold: distribution_result}.
    """
    if thresholds is None:
        thresholds = [0.001, 0.002, 0.003, 0.005, 0.007, 0.010, 0.015, 0.020]

    results = {}
    for theta in thresholds:
        res = cascade_distribution(W, theta, k=k, n_trials=n_trials, seed=seed)
        if res["tau"] is not None:
            results[theta] = res

    return results


# ─── P3: Temporal asymmetry ───────────────────────────────────────────────────

def temporal_asymmetry(
    W: np.ndarray,
    threshold: float,
    k: int = 2,
    n_trials: int = 300,
    seed: int = 42,
) -> dict:
    """
    Measure relaxation asymmetry: removal vs addition.
    P3 prediction: removal relaxes slower than addition near criticality.
    Returns asymmetry value and statistical test.
    """
    np.random.seed(seed)
    N = W.shape[0]
    adj = build_adj(W, threshold)
    core, _ = kcore(adj, k, N)

    steps_rem, steps_add = [], []

    for _ in range(n_trials):
        # Removal
        if core:
            node_rem = np.random.choice(list(core))
            adj_rem = {v: set(nbrs) for v, nbrs in adj.items()}
            for nbr in list(adj_rem.get(node_rem, set())):
                adj_rem[nbr].discard(node_rem)
            adj_rem[node_rem] = set()
            _, steps = kcore(adj_rem, k, N)
            steps_rem.append(steps)

        # Addition
        outside = [i for i in range(N) if i not in core]
        if outside and core:
            node_add = np.random.choice(outside)
            n_edges = min(k + 1, len(core))
            new_nbrs = list(np.random.choice(list(core), n_edges, replace=False))
            _, steps = cascade_after_addition(adj, k, node_add, new_nbrs, N)
            steps_add.append(steps)

    if not steps_rem or not steps_add:
        return {"asymmetry": 0.0, "p_value": 1.0, "confirmed": False}

    rem_mean = float(np.mean(steps_rem))
    add_mean = float(np.mean(steps_add))
    asym = (rem_mean - add_mean) / (rem_mean + add_mean + 1e-10)

    _, p_val = sp_stats.mannwhitneyu(steps_rem, steps_add, alternative="two-sided")

    return {
        "asymmetry": float(asym),
        "p_value": float(p_val),
        "confirmed": p_val < 0.05 and asym > 0,
        "rem_mean": rem_mean,
        "add_mean": add_mean,
        "core_size": len(core),
    }
