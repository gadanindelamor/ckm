"""
fabrication_service_dev.py — FabricationService

Reconstrucción desde snippets sesión "Take your time" + REG_monitor_ckm_v1.md
[SNIPPET]   = código directo del snippet
[INFERRED]  = reconstruido desde REG

Limitaciones documentadas en REG:
- fi saturado con W homogénea (bug en _direction_score, no corregido aquí)
- Δ = Δ_acumulado, no Δ_declarado
- Umbrales de cuadrante no calibrados
"""

from __future__ import annotations
import json
from pathlib import Path
import numpy as np

_CS_THR = 0.003   # [INFERRED from REG]
_T_THR  = 0.05    # [INFERRED from REG]
_A0_THR = 5       # [INFERRED from REG]


class FabricationService:

    def __init__(self, name, W, nodes, storage_dir="storage", n_runs=100):  # [SNIPPET]
        self.name      = name
        self.W         = W.copy()
        self.nodes     = nodes
        self.N         = len(nodes)
        self.n_runs    = n_runs
        self._storage  = Path(storage_dir)
        self._storage.mkdir(parents=True, exist_ok=True)
        self._traj_path = self._storage / "trajectory.jsonl"
        self._A0: int | None = None   # fijado en t=0, semilla constante

    def _relax(self, sigma, W=None, max_iter=100):  # [FIX v1: W+Delta como CONDITIONS]
        if W is None:
            W = self.W
        for _ in range(max_iter):
            h  = W @ sigma
            s2 = np.where(h > 0, 1., np.where(h < 0, -1., sigma))
            if np.allclose(s2, sigma):
                break
            sigma = s2
        return sigma

    def _cS(self, sigma, W=None):               # [FIX v1: W+Delta como CONDITIONS]
        if W is None:
            W = self.W
        ii, jj = np.triu_indices(self.N, k=1)
        return float(np.mean(W[ii, jj] * sigma[ii] * sigma[jj]))

    def _direction_score(self, sigma, Delta):  # [INFERRED from REG description]
        """
        fi = fracción de nodos con Δ>0 que están inactivos.
        Bug conocido: con W homogénea y sigma parcial → fi≈1.0 siempre.
        """
        declared = np.sum(Delta, axis=1) > 0
        inactive = sigma < 0
        n_declared = declared.sum()
        if n_declared == 0:
            return 0.0
        return float((declared & inactive).sum() / n_declared)

    def _count_attractors_W(self, W, seed=0):  # [FIX v1: cuenta sobre W arbitrario]
        rng = np.random.default_rng(seed)
        attractors = set()
        for _ in range(self.n_runs):
            rho    = rng.uniform(0.3, 0.7)
            n_act  = max(1, int(round(rho * self.N)))
            s0     = np.full(self.N, -1.)
            s0[rng.choice(self.N, n_act, replace=False)] = 1.
            attractors.add(tuple(self._relax(s0, W).tolist()))
        return len(attractors)

    def _count_attractors(self, seed=0):       # [INFERRED — semilla fija para estabilidad]
        rng = np.random.default_rng(seed)
        attractors = set()
        for _ in range(self.n_runs):
            rho    = rng.uniform(0.3, 0.7)
            n_act  = max(1, int(round(rho * self.N)))
            s0     = np.full(self.N, -1.)
            s0[rng.choice(self.N, n_act, replace=False)] = 1.
            attractors.add(tuple(self._relax(s0).tolist()))
        return len(attractors)

    def _classify_quadrant(self, cs, T, A0):   # [INFERRED from REG thresholds]
        if cs > _CS_THR and T > _T_THR:
            return "COHESION_FABRICADA"
        if cs > _CS_THR and A0 >= _A0_THR:
            return "LOCKED"
        if cs <= _CS_THR and T > _T_THR:
            return "TENSION_SIN_COHESION"
        return "LIBRE"

    def snapshot(self, sigma, Delta, t, mu_W=None):  # [FIX v1: W+Delta, r, D_ckm sin clip]
        W_eff = self.W + Delta
        cs  = self._cS(sigma, self.W)   # c(S) sobre W base — comparable con percentiles G1
        fi  = self._direction_score(sigma, Delta)
        T   = float(np.mean(np.abs(Delta)))
        A0  = int((sigma > 0).sum())

        # D_ckm: contar atractores sobre W+Delta — puede ser negativo
        A_current = self._count_attractors_W(W_eff, seed=0)
        if self._A0 is None:
            self._A0 = A_current
        D_ckm = float((self._A0 - A_current) / self._A0) if self._A0 > 0 else 0.0
        recovery = float(A_current / max(self._A0, 1))

        r = float(cs / mu_W) if mu_W and mu_W != 0 else None

        quad = self._classify_quadrant(cs, T, A0)

        delta_out = np.sum(np.abs(Delta), axis=1)
        active    = np.where(sigma > 0)[0]
        criticos  = (
            [self.nodes[i] for i in active[np.argsort(delta_out[active])[::-1][:3]]]
            if len(active) else []
        )

        panel = {
            "c_S"               : round(cs,    6),
            "r"                 : round(r, 4) if r is not None else None,
            "fabrication_index" : round(fi,    4),
            "D_ckm"             : round(D_ckm, 4),
            "T"                 : round(T,     6),
            "A0"                : A0,
            "A_current"         : A_current,
            "recovery"          : round(recovery, 4),
            "quadrant"          : quad,
            "criticos"          : criticos,
        }

        with open(self._traj_path, "a") as f:
            f.write(json.dumps({
                "t": t, "state_id": f"{self.name}_{t:04d}",
                "sigma": sigma.tolist(),
                "Delta_sum": float(np.sum(np.abs(Delta))),
                "panel": panel,
            }) + "\n")
        return panel

    def trajectory(self):                      # [SNIPPET — código directo]
        if not self._traj_path.exists():
            return []
        with open(self._traj_path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def stop_signal(self, window=5):           # [SNIPPET — código directo]
        traj = self.trajectory()
        if len(traj) < 2:
            return {"signal": False, "reason": "trayectoria insuficiente"}

        recent    = traj[-window:]
        fi_vals   = [r["panel"]["fabrication_index"] for r in recent]
        D_vals    = [r["panel"]["D_ckm"]             for r in recent]
        quad_vals = [r["panel"]["quadrant"]           for r in recent]

        fi_trend = fi_vals[-1] - fi_vals[0]
        D_trend  = D_vals[-1]  - D_vals[0]

        inflections = [
            {"t": recent[i+1]["t"], "from": quad_vals[i], "to": quad_vals[i+1]}
            for i in range(len(quad_vals) - 1)
            if quad_vals[i] != quad_vals[i+1]
        ]
        signal = (fi_trend > 0.02) and (D_trend > 0.02)

        return {
            "signal"       : signal,
            "fi_trend"     : round(fi_trend, 4),
            "D_trend"      : round(D_trend,  4),
            "window"       : len(recent),
            "current_quad" : quad_vals[-1],
            "inflections"  : inflections,
            "direction"    : (
                "CONVERGING" if fi_trend < -0.02 and D_trend < -0.02 else
                "DIVERGING"  if signal else
                "STABLE"
            ),
        }
