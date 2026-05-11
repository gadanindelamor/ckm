"""
ckm/core.py — CKM Core

Graph W+Δ, cohesion function c(S), and Gatekeeper R15.

Design principle: W and Δ are kept as strictly separate layers.
Mixing them destroys recovery capacity (verified: 0.02 vs 0.78).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np


# ─── Configuration ────────────────────────────────────────────────────────────

@dataclass
class CKMConfig:
    """CKM runtime configuration. All parameters calibrated on real corpus N=16."""

    # Gatekeeper R15
    theta_W: float = 0.10       # C1: minimum connection weight
    epsilon: float = 0.005      # C2: c(S) tolerance
    alpha_c: float = 0.138      # C4: capacity limit (fraction of N)

    # 3D Score
    score_threshold: float = 0.630
    alpha_score: float = 0.20   # c(S) weight
    beta_score: float = 0.50    # direction_score weight
    gamma_score: float = 0.30   # cohesion_density weight

    # W_mixta
    w_neg: float = 0.10         # negative pair weight

    # Hopfield
    max_iter: int = 1000
    seed: int = 42


# ─── Gatekeeper result ────────────────────────────────────────────────────────

@dataclass
class GatekeeperResult:
    admitted: bool
    c1: bool            # minimum connection
    c2: bool            # cohesion delta
    c3: bool            # direction score (M.M)
    c4: bool            # capacity
    score: float
    reason: str = ""

    def __bool__(self):
        return self.admitted


# ─── CKM Graph ────────────────────────────────────────────────────────────────

class CKMGraph:
    """
    CKM knowledge graph.

    W : symmetric co-occurrence weight matrix  (N × N)
    Δ : asymmetric directional dependency matrix (N × N)
    sigma : current state vector {+1, -1}^N
    """

    def __init__(
        self,
        nodes: list[str],
        W: np.ndarray,
        delta: Optional[np.ndarray] = None,
        config: Optional[CKMConfig] = None,
    ):
        self.nodes = nodes
        self.N = len(nodes)
        self.node_index = {n: i for i, n in enumerate(nodes)}

        assert W.shape == (self.N, self.N), "W must be N×N"
        assert np.allclose(W, W.T, atol=1e-8), "W must be symmetric"

        self.W = W.copy()
        self.delta = delta.copy() if delta is not None else np.zeros((self.N, self.N))
        self.sigma = np.ones(self.N)  # default: all active
        self.config = config or CKMConfig()

        # Track patterns stored (for C4 capacity check)
        self._n_patterns: int = 0

    # ─── Class methods ────────────────────────────────────────────────────────

    @classmethod
    def from_corpus(
        cls,
        paragraphs: list[str],
        nodes: list[str],
        term_map: dict[str, list[str]],
        negative_pairs: Optional[list[tuple[str, str]]] = None,
        config: Optional[CKMConfig] = None,
    ) -> "CKMGraph":
        """Build CKMGraph from a text corpus via co-occurrence."""
        cfg = config or CKMConfig()
        N = len(nodes)
        cooc = np.zeros((N, N))

        for para in paragraphs:
            para_l = para.lower()
            present = [
                i for i, node in enumerate(nodes)
                if any(t.lower() in para_l for t in term_map.get(node, []))
            ]
            for a in range(len(present)):
                for b in range(a + 1, len(present)):
                    i, j = present[a], present[b]
                    cooc[i, j] += 1
                    cooc[j, i] += 1

        W = cooc / max(len(paragraphs), 1)

        # Add negative weights for structural tension
        if negative_pairs:
            node_idx = {n: i for i, n in enumerate(nodes)}
            for na, nb in negative_pairs:
                if na in node_idx and nb in node_idx:
                    i, j = node_idx[na], node_idx[nb]
                    W[i, j] = -cfg.w_neg
                    W[j, i] = -cfg.w_neg

        return cls(nodes=nodes, W=W, config=cfg)

    @classmethod
    def from_json(cls, path: str | Path, config: Optional[CKMConfig] = None) -> "CKMGraph":
        """Load a saved CKMGraph from JSON."""
        data = json.loads(Path(path).read_text())
        nodes = data["nodes"]
        W = np.array(data["W"])
        delta = np.array(data["delta"]) if "delta" in data else None
        return cls(nodes=nodes, W=W, delta=delta, config=config)

    # ─── Persistence ──────────────────────────────────────────────────────────

    def save(self, path: str | Path) -> None:
        """Save graph to JSON."""
        Path(path).write_text(json.dumps({
            "nodes": self.nodes,
            "W": self.W.tolist(),
            "delta": self.delta.tolist(),
            "sigma": self.sigma.tolist(),
        }, indent=2))

    # ─── Cohesion ─────────────────────────────────────────────────────────────

    def cS(self, sigma: Optional[np.ndarray] = None) -> float:
        """
        Cohesion c(S) = mean(W_ij * σ_i * σ_j) over all pairs i<j.
        Negative of normalized Hopfield energy. Measures W/state alignment.
        """
        s = sigma if sigma is not None else self.sigma
        pairs = [(i, j) for i in range(self.N) for j in range(i + 1, self.N)]
        if not pairs:
            return 0.0
        return float(np.mean([self.W[i, j] * s[i] * s[j] for i, j in pairs]))

    def cS_delta(self, node_idx: int) -> float:
        """Delta c(S) after activating node_idx (+1)."""
        sigma_post = self.sigma.copy()
        sigma_post[node_idx] = 1
        return self.cS(sigma_post) - self.cS()

    def direction_score(self, node_idx: int) -> float:
        """
        Fraction of node's directional dependencies satisfied in current state.
        Uses Δ matrix (asymmetric layer). Free nodes (Δ≈0) return 1.0.
        M.M criterion: fails when declared dependencies are not satisfied.
        """
        outgoing = self.delta[node_idx]
        dep_mask = np.abs(outgoing) > 1e-8
        if not np.any(dep_mask):
            return 1.0  # free node — no dependencies
        satisfied = np.sum(dep_mask & (self.sigma == 1))
        total = np.sum(dep_mask)
        return float(satisfied / total)

    def cohesion_density(self, sigma: Optional[np.ndarray] = None) -> float:
        """
        c(S_active) / c(S_max_possible_for_n_active).
        Measures whether active nodes are the most connected among themselves.
        """
        s = sigma if sigma is not None else self.sigma
        active_idx = np.where(s == 1)[0]
        n_active = len(active_idx)
        if n_active < 2:
            return 0.0

        cs_active = float(np.mean([
            self.W[i, j] * s[i] * s[j]
            for i in active_idx for j in active_idx if i < j
        ]))

        # Max possible: top n_active*(n_active-1)/2 weights
        all_weights = [self.W[i, j] for i in range(self.N) for j in range(i + 1, self.N)]
        n_pairs = n_active * (n_active - 1) // 2
        if n_pairs == 0:
            return 0.0
        max_possible = float(np.mean(sorted(all_weights, reverse=True)[:n_pairs]))
        if abs(max_possible) < 1e-10:
            return 0.0
        return float(np.clip(cs_active / max_possible, -1.0, 1.0))

    def score_3d(self, sigma: Optional[np.ndarray] = None) -> float:
        """
        Combined 3D classification score.
        score = α·c(S)_norm + β·direction_score + γ·cohesion_density
        Threshold 0.630 → COHESIVE.
        """
        s = sigma if sigma is not None else self.sigma
        cfg = self.config

        cs = self.cS(s)
        # Normalize c(S) to [0,1] range (empirical max ≈ 0.10)
        cs_norm = float(np.clip((cs + 0.05) / 0.10, 0.0, 1.0))

        # Mean direction score over active nodes
        active_idx = np.where(s == 1)[0]
        if len(active_idx) == 0:
            ds = 0.0
        else:
            ds = float(np.mean([self.direction_score(i) for i in active_idx]))

        cd = self.cohesion_density(s)

        return cfg.alpha_score * cs_norm + cfg.beta_score * ds + cfg.gamma_score * cd

    def classify(self, sigma: Optional[np.ndarray] = None) -> str:
        """
        Classify current state.
        Returns: 'COHESIVE' | 'SPURIOUS_HIGH' | 'SPURIOUS_MEDIUM' | 'SPURIOUS_LOW'
        """
        score = self.score_3d(sigma)
        if score >= self.config.score_threshold:
            return "COHESIVE"
        elif score >= 0.50:
            return "SPURIOUS_HIGH"
        elif score >= 0.30:
            return "SPURIOUS_MEDIUM"
        return "SPURIOUS_LOW"

    # ─── Gatekeeper R15 ───────────────────────────────────────────────────────

    def gatekeeper(self, node: str | int) -> GatekeeperResult:
        """
        R15 Gatekeeper — O(N) per node.

        C1: W(node, j) ≥ θ_W for at least one active node j
        C2: c(S)_post ≥ c(S)_current − ε
        C3: direction_score(node) > 0 (M.M criterion)
        C4: current_patterns / N < α_c
        """
        cfg = self.config
        idx = self.node_index[node] if isinstance(node, str) else node

        # C1 — minimum connection
        active_idx = np.where(self.sigma == 1)[0]
        max_conn = float(np.max(np.abs(self.W[idx, active_idx]))) if len(active_idx) else 0.0
        c1 = max_conn >= cfg.theta_W

        # C2 — cohesion delta
        cs_current = self.cS()
        cs_post = self.cS(self._sigma_with(idx, 1))
        c2 = (cs_post >= cs_current - cfg.epsilon)

        # C3 — direction score (M.M)
        ds = self.direction_score(idx)
        c3 = (ds > 0 or float(np.sum(np.abs(self.delta[idx]))) < 1e-8)

        # C4 — capacity
        c4 = (self._n_patterns / self.N) < cfg.alpha_c

        admitted = c1 and c2 and c3 and c4
        score = self.score_3d(self._sigma_with(idx, 1))

        reasons = []
        if not c1:
            reasons.append(f"C1 fail: max_conn={max_conn:.4f} < θ_W={cfg.theta_W}")
        if not c2:
            reasons.append(f"C2 fail: Δc(S)={cs_post - cs_current:.5f} < -ε")
        if not c3:
            reasons.append(f"C3 fail: direction_score={ds:.3f} (M.M violation)")
        if not c4:
            reasons.append(f"C4 fail: capacity {self._n_patterns}/{self.N} ≥ α_c={cfg.alpha_c}")

        return GatekeeperResult(
            admitted=admitted,
            c1=c1, c2=c2, c3=c3, c4=c4,
            score=score,
            reason=" | ".join(reasons) if reasons else "OK",
        )

    def admit(self, node: str | int) -> GatekeeperResult:
        """Evaluate and, if admitted, incorporate the node into sigma."""
        result = self.gatekeeper(node)
        if result.admitted:
            idx = self.node_index[node] if isinstance(node, str) else node
            self.sigma[idx] = 1
        return result

    # ─── Hebbian learning ─────────────────────────────────────────────────────

    def hebb_W(self, pattern: np.ndarray, lr: float = 1.0) -> None:
        """
        Store a pattern via Hebbian learning on W.
        W += lr/N * outer(pattern, pattern); diagonal zeroed.
        WARNING: modifies W — use only when deliberate. See THEORY.md W/Δ separation.
        """
        self.W += (lr / self.N) * np.outer(pattern, pattern)
        np.fill_diagonal(self.W, 0)
        self._n_patterns += 1

    def hebb_delta(self, pattern: np.ndarray, lr: float = 1.0) -> None:
        """
        Accumulate spark orientation in Δ (asymmetric layer).
        Δ[i,j] += lr * pattern[i] * (pattern[j] > 0)
        Preserves W intact — correct destination for spark traces.
        """
        for i in range(self.N):
            for j in range(self.N):
                if i != j and pattern[j] > 0:
                    self.delta[i, j] += lr * pattern[i]

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _sigma_with(self, idx: int, val: float) -> np.ndarray:
        s = self.sigma.copy()
        s[idx] = val
        return s

    def active_nodes(self) -> list[str]:
        return [self.nodes[i] for i in range(self.N) if self.sigma[i] == 1]

    def reset(self) -> None:
        self.sigma = np.ones(self.N)

    def set_state(self, active: list[str]) -> None:
        self.sigma = np.full(self.N, -1.0)
        for node in active:
            if node in self.node_index:
                self.sigma[self.node_index[node]] = 1.0

    def __repr__(self) -> str:
        return (
            f"CKMGraph(N={self.N}, "
            f"active={int(np.sum(self.sigma == 1))}/{self.N}, "
            f"c(S)={self.cS():.5f})"
        )
