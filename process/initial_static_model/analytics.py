"""
ckm/analytics.py — Attractor Analytics

Co-presence clustering, attractor hierarchy, optimal density (P4).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform

from .core import CKMGraph


# ─── Co-presence clustering ───────────────────────────────────────────────────

def copresence_matrix(
    attractors: dict[frozenset, int],
    N: int,
) -> np.ndarray:
    """
    Pearson correlation of co-presence across unique attractors.
    Returns N×N correlation matrix.

    Nodos con presencia constante (varianza=0, ej: traza_inferencia al 84%+)
    producen NaN en corrcoef. Se reemplazan por 0.0: sin información de
    co-presencia diferencial, no correlación artificial.
    """
    unique = list(attractors.keys())
    n_unique = len(unique)

    attr_matrix = np.zeros((n_unique, N))
    for idx, attr in enumerate(unique):
        for i in attr:
            if i < N:
                attr_matrix[idx, i] = 1

    corr = np.corrcoef(attr_matrix.T)
    np.nan_to_num(corr, nan=0.0, copy=False)  # NaN → 0 (nodo core-invariante)
    return corr


def cluster_nodes(
    attractors: dict[frozenset, int],
    nodes: list[str],
    n_clusters: int = 4,
) -> dict[str, list[str]]:
    """
    Cluster nodes by co-movement in attractor space.
    Returns {cluster_label: [node_names]}.
    """
    N = len(nodes)
    corr = copresence_matrix(attractors, N)

    dist = 1 - corr
    dist = (dist + dist.T) / 2
    np.fill_diagonal(dist, 0)
    dist = np.clip(dist, 0, 2)

    condensed = squareform(dist)
    Z = linkage(condensed, method="ward")
    labels = fcluster(Z, n_clusters, criterion="maxclust")

    clusters: dict[str, list[str]] = {}
    for c in range(1, n_clusters + 1):
        clusters[f"C{c}"] = [nodes[i] for i in range(N) if labels[i] == c]

    return clusters


def perfect_oppositions(
    attractors: dict[frozenset, int],
    nodes: list[str],
    threshold: float = -0.90,
) -> list[tuple[str, str, float]]:
    """
    Find node pairs with strong negative co-presence correlation.
    Returns [(node_a, node_b, correlation)] sorted by correlation.
    """
    N = len(nodes)
    corr = copresence_matrix(attractors, N)

    pairs = []
    for i in range(N):
        for j in range(i + 1, N):
            if corr[i, j] <= threshold:
                pairs.append((nodes[i], nodes[j], float(corr[i, j])))

    return sorted(pairs, key=lambda x: x[2])


# ─── Attractor statistics ─────────────────────────────────────────────────────

def attractor_stats(
    attractors: dict[frozenset, int],
    N: int,
) -> dict:
    """Summary statistics of the attractor distribution."""
    unique = list(attractors.keys())
    sizes_unique = [len(a) for a in unique]
    sizes_weighted = []
    for attr, cnt in attractors.items():
        sizes_weighted.extend([len(attr)] * cnt)

    total_runs = sum(attractors.values())
    presence = np.zeros(N)
    for attr in unique:
        for i in attr:
            if i < N:
                presence[i] += 1
    presence /= max(len(unique), 1)

    return {
        "n_unique": len(unique),
        "n_runs": total_runs,
        "mean_size_unique": float(np.mean(sizes_unique)) if sizes_unique else 0.0,
        "mean_size_weighted": float(np.mean(sizes_weighted)) if sizes_weighted else 0.0,
        "mean_frac_N": float(np.mean(sizes_weighted)) / N if sizes_weighted else 0.0,
        "std_size": float(np.std(sizes_unique)) if sizes_unique else 0.0,
        "min_size": int(min(sizes_unique)) if sizes_unique else 0,
        "max_size": int(max(sizes_unique)) if sizes_unique else 0,
        "n_saturated": sum(1 for s in sizes_unique if s / N >= 0.85),
        "n_asymmetric": sum(1 for s in sizes_unique if s / N < 0.85),
        "node_presence": presence.tolist(),
    }


# ─── P4: Optimal density Ω* ──────────────────────────────────────────────────

def optimal_density(
    graph: CKMGraph,
    rho_steps: int = 30,
    n_samples: int = 300,
    seed: int = 42,
) -> dict:
    """
    Measure c(S) vs density for W_base and W_mixta.
    P4 prediction: W_mixta has interior Ω* in ρ ∈ [0.5, 0.8].
    """
    np.random.seed(seed)
    N = graph.N
    rho_grid = np.linspace(0.05, 1.0, rho_steps)

    def cs_at_rho(W, rho):
        n_active = max(1, int(rho * N))
        vals = []
        for _ in range(n_samples):
            active = np.random.choice(N, n_active, replace=False)
            sigma = np.full(N, -1.0)
            sigma[active] = 1.0
            pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
            vals.append(float(np.mean([W[i, j] * sigma[i] * sigma[j] for i, j in pairs])))
        return float(np.mean(vals)), float(np.std(vals))

    cs_means, cs_stds = [], []
    for rho in rho_grid:
        m, s = cs_at_rho(graph.W, rho)
        cs_means.append(m)
        cs_stds.append(s)

    cs_means = np.array(cs_means)
    omega_idx = int(np.argmax(cs_means))
    omega_rho = float(rho_grid[omega_idx])
    omega_interior = omega_rho < 0.95

    # Advantage in zone [0.5, 0.8]
    zone_mask = (rho_grid >= 0.5) & (rho_grid <= 0.8)

    return {
        "rho_grid": rho_grid.tolist(),
        "cs_means": cs_means.tolist(),
        "cs_stds": cs_stds,
        "omega_rho": omega_rho,
        "omega_interior": omega_interior,
        "omega_cs": float(cs_means[omega_idx]),
        "zone_mean_cs": float(np.mean(cs_means[zone_mask])),
        "confirmed": omega_interior,
    }
