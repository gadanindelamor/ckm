"""
ckm/hopfield.py — Hopfield Dynamics

Asynchronous deterministic and stochastic update.
Attractor mapping, basin analysis, hysteresis measurement.
"""

from __future__ import annotations

from collections import Counter
from typing import Optional

import numpy as np

from .core import CKMGraph, CKMConfig


# ─── Relaxation ───────────────────────────────────────────────────────────────

def relax(
    graph: CKMGraph,
    sigma_init: Optional[np.ndarray] = None,
    max_iter: int = 1000,
    beta: Optional[float] = None,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Asynchronous Hopfield relaxation.

    beta=None  : deterministic update (default)
    beta=float : stochastic (temperature = 1/beta)
                 Working zone: beta ∈ [3, 100] (T ∈ [0.01, 0.30])

    Returns final state sigma.
    """
    if seed is not None:
        np.random.seed(seed)

    sigma = (sigma_init if sigma_init is not None else graph.sigma).copy()
    N = graph.N
    W = graph.W

    for _ in range(max_iter * N):
        i = np.random.randint(N)
        h = float(np.dot(W[i], sigma))

        if beta is None:
            sigma[i] = 1.0 if h > 0 else (-1.0 if h < 0 else sigma[i])
        else:
            p = 1.0 / (1.0 + np.exp(-2.0 * beta * h))
            sigma[i] = 1.0 if np.random.rand() < p else -1.0

    return sigma


def relax_steps(
    graph: CKMGraph,
    sigma_init: Optional[np.ndarray] = None,
    max_iter: int = 1000,
) -> tuple[np.ndarray, int]:
    """
    Relax and count convergence rounds (steps).
    Returns (final_sigma, n_rounds).
    Used for P3 temporal asymmetry measurement.
    """
    sigma = (sigma_init if sigma_init is not None else graph.sigma).copy()
    N = graph.N
    W = graph.W
    steps = 0
    changed = True

    while changed and steps < max_iter:
        changed = False
        steps += 1
        order = np.random.permutation(N)
        for i in order:
            h = float(np.dot(W[i], sigma))
            new_val = 1.0 if h > 0 else (-1.0 if h < 0 else sigma[i])
            if new_val != sigma[i]:
                sigma[i] = new_val
                changed = True

    return sigma, steps


# ─── Attractor mapping ────────────────────────────────────────────────────────

def find_attractors(
    graph: CKMGraph,
    n_runs: int = 300,
    seed: int = 42,
    n_flips: int = 2,
    max_iter: int = 1000,
) -> dict[frozenset, int]:
    """
    Map attractor space by relaxing from random near-full initial conditions.

    Initial condition: all +1 except n_flips random nodes.
    Returns: {attractor_frozenset: frequency}
    """
    np.random.seed(seed)
    N = graph.N
    counter: Counter = Counter()

    for _ in range(n_runs):
        sigma = np.ones(N)
        sigma[np.random.choice(N, n_flips, replace=False)] = -1.0
        final = relax(graph, sigma_init=sigma, max_iter=max_iter)
        attr = frozenset(i for i in range(N) if final[i] == 1)
        counter[attr] += 1

    return dict(counter)


def attractor_presence(
    attractors: dict[frozenset, int],
    nodes: list[str],
) -> dict[str, float]:
    """
    Fraction of unique attractors where each node appears.
    Returns {node_name: presence_fraction}.
    """
    N = len(nodes)
    unique = list(attractors.keys())
    n_unique = len(unique)
    presence = {node: 0.0 for node in nodes}

    for attr in unique:
        for i in attr:
            if i < N:
                presence[nodes[i]] += 1

    return {node: count / n_unique for node, count in presence.items()}


def find_core_nodes(
    attractors: dict[frozenset, int],
    nodes: list[str],
    threshold: float = 0.80,
) -> list[str]:
    """Nodes present in >= threshold fraction of unique attractors."""
    presence = attractor_presence(attractors, nodes)
    return [node for node, p in presence.items() if p >= threshold]


# ─── Hysteresis (P1) ─────────────────────────────────────────────────────────

def hysteresis_loop(
    graph: CKMGraph,
    n_sequences: int = 200,
    seed: int = 42,
) -> dict:
    """
    Measure macroscopic hysteresis loop in c(S).
    UP branch: add nodes one by one → measure c(S).
    DOWN branch: remove nodes one by one → measure c(S).
    Returns trajectories and loop area.
    """
    from scipy import stats as sp_stats

    np.random.seed(seed)
    N = graph.N
    rho_grid = np.linspace(1 / N, 1.0, N)

    all_up, all_down = [], []

    for _ in range(n_sequences):
        order_up = np.random.permutation(N).tolist()
        order_dn = np.random.permutation(N).tolist()

        # UP branch
        active: set = set()
        traj_up = []
        for nd in order_up:
            active.add(nd)
            sigma = np.array([1.0 if i in active else -1.0 for i in range(N)])
            traj_up.append((len(active) / N, graph.cS(sigma)))
        all_up.append(traj_up)

        # DOWN branch
        active = set(range(N))
        traj_dn = []
        for nd in order_dn:
            active.discard(nd)
            sigma = np.array([1.0 if i in active else -1.0 for i in range(N)])
            traj_dn.append((len(active) / N, graph.cS(sigma)))
        all_down.append(traj_dn)

    def interp_grid(trajs, grid):
        out = np.zeros((len(trajs), len(grid)))
        for t, traj in enumerate(trajs):
            rhos = np.array([p[0] for p in traj])
            css = np.array([p[1] for p in traj])
            out[t] = np.interp(grid, rhos, css)
        return out

    up_g = interp_grid(all_up, rho_grid)
    dn_g = interp_grid(all_down, rho_grid)
    up_m = np.mean(up_g, axis=0)
    dn_m = np.mean(dn_g, axis=0)
    diff = dn_m - up_m

    area = float(np.trapezoid(np.abs(diff), rho_grid))
    max_diff_idx = int(np.argmax(np.abs(diff)))

    # Statistical test in critical zone
    mid_mask = (rho_grid >= 0.35) & (rho_grid <= 0.70)
    _, p_val = sp_stats.wilcoxon(
        up_g[:, mid_mask].mean(axis=1),
        dn_g[:, mid_mask].mean(axis=1),
    )

    return {
        "area": area,
        "max_diff": float(diff[max_diff_idx]),
        "max_diff_rho": float(rho_grid[max_diff_idx]),
        "p_value": float(p_val),
        "confirmed": p_val < 0.05,
        "up_mean": up_m,
        "down_mean": dn_m,
        "rho_grid": rho_grid,
    }
