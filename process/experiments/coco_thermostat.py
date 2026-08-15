"""
coco_thermostat.py — COCO-thermostat (prototipo mínimo)

No almacena capacidades declaradas (eso es COCO-registry, se vuelve stale).
Observa D_ckm(t) del corpus colectivo emergido de interacción real A2A.
Emite señal STOP cuando el campo cruza umbral de degradación.
Aplica STOP (Delta → alpha * Delta) sobre el CorpusService compartido.

Ref: REG_destruccion_recuperacion_v1.md
     REG_iap_coco_convergence_v1.md
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ── Umbrales derivados del sweep (REG_destruccion_recuperacion_v1) ──────────
D_CKM_THRESHOLD = 0.40   # D_ckm > 0.40 → zona degradación sostenida
ALPHA_STAR       = 0.10   # alpha óptimo empírico (A_post_max en sweep AMP=40)
FRAC_REC_MIN     = 0.60   # si A(t)/A0 < 0.60 → campo en degradación profunda

# ── Calibración dinámica alpha ───────────────────────────────────────────────
ALPHA_MIN        = 0.05   # D_ckm → 1.0 (degradación profunda) → STOP fuerte
ALPHA_MAX        = 0.30   # D_ckm → threshold (justo en umbral) → STOP suave


@dataclass
class ThermostatState:
    t            : int   = 0
    D_ckm        : float = 0.0
    A_current    : int   = 0
    A0           : int   = 0
    frac_rec     : float = 1.0
    stop_applied : bool  = False
    alpha_used   : float = 1.0
    zone         : str   = "stable"   # stable | degrading | deep


class COCOThermostat:
    """
    Termostato colectivo de campo CKM.

    Recibe el corpus compartido (CorpusService) y el Delta acumulado
    de interacciones A2A reales. Evalúa estado del campo en cada ciclo
    y emite señal STOP cuando D_ckm cruza umbral.

    No sabe quién es cada agente. No usa AgentCards.
    Trabaja con lo que el campo rechazó — Δ_r.
    """

    def __init__(
        self,
        W              : np.ndarray,
        d_ckm_threshold: float = D_CKM_THRESHOLD,
        alpha_star     : float = ALPHA_STAR,
        frac_rec_min   : float = FRAC_REC_MIN,
        dynamic_alpha  : bool  = True,
        n_runs         : int   = 80,
        seed           : int   = 0,
    ):
        self.W               = W
        self.N               = W.shape[0]
        self.threshold       = d_ckm_threshold
        self.alpha_star      = alpha_star
        self.frac_rec_min    = frac_rec_min
        self.dynamic_alpha   = dynamic_alpha
        self._n_runs         = n_runs
        self._seed           = seed

        self._A0             : Optional[int]        = None
        self._Delta          : np.ndarray           = np.zeros((self.N, self.N))
        self._history        : list[ThermostatState] = []
        self._t              : int                  = 0

    # ── API pública ──────────────────────────────────────────────────────────

    def observe(self, Delta_new: np.ndarray) -> ThermostatState:
        """
        Recibe el Delta acumulado actual del corpus colectivo.
        Evalúa estado del campo. Aplica STOP si corresponde.
        Devuelve ThermostatState con diagnóstico.
        """
        self._Delta = Delta_new.copy()
        self._t    += 1

        W_eff    = self.W + self._Delta
        A_current = self._count_attractors(W_eff)

        if self._A0 is None:
            self._A0 = self._count_attractors(self.W)  # baseline sin Delta

        D_ckm    = (self._A0 - A_current) / self._A0 if self._A0 > 0 else 0.0
        frac_rec = A_current / self._A0 if self._A0 > 0 else 1.0

        zone = self._classify_zone(D_ckm, frac_rec)

        stop_applied = False
        alpha_used   = 1.0

        if zone in ("degrading", "deep"):
            alpha_used   = self._alpha_for(D_ckm)
            self._Delta  = alpha_used * self._Delta
            stop_applied = True

        state = ThermostatState(
            t            = self._t,
            D_ckm        = round(D_ckm, 4),
            A_current    = A_current,
            A0           = self._A0,
            frac_rec     = round(frac_rec, 4),
            stop_applied = stop_applied,
            alpha_used   = alpha_used,
            zone         = zone,
        )
        self._history.append(state)
        return state

    def delta_state(self) -> np.ndarray:
        """Delta actual después de posibles STOPs aplicados."""
        return self._Delta.copy()

    def history(self) -> list[ThermostatState]:
        return list(self._history)

    def status(self) -> dict:
        if not self._history:
            return {"t": 0, "zone": "uninitialized"}
        s = self._history[-1]
        return {
            "t"           : s.t,
            "A0"          : s.A0,
            "A_current"   : s.A_current,
            "D_ckm"       : s.D_ckm,
            "frac_rec"    : s.frac_rec,
            "zone"        : s.zone,
            "stop_applied": s.stop_applied,
            "alpha_used"  : s.alpha_used,
        }

    # ── Calibración dinámica ─────────────────────────────────────────────────

    def _alpha_for(self, D_ckm: float) -> float:
        """
        Alpha decrece monotonamente con D_ckm.
        Mayor degradación → STOP más agresivo.

        D_ckm en [threshold, 1.0] → alpha en [ALPHA_MAX, ALPHA_MIN]
        Si dynamic_alpha=False, devuelve alpha_star fijo.
        """
        if not self.dynamic_alpha:
            return self.alpha_star
        t = self.threshold
        # normalizar D_ckm al rango [threshold, 1.0]
        ratio = min(1.0, max(0.0, (D_ckm - t) / (1.0 - t)))
        return ALPHA_MAX + (ALPHA_MIN - ALPHA_MAX) * ratio

    # ── Clasificación de zona ─────────────────────────────────────────────────

    def _classify_zone(self, D_ckm: float, frac_rec: float) -> str:
        if D_ckm < 0:
            return "stable"          # campo expandido — acumulación suma atractores
        if D_ckm < self.threshold:
            return "stable"          # degradación menor al umbral
        if frac_rec < self.frac_rec_min:
            return "deep"            # degradación profunda — STOP urgente
        return "degrading"           # cruzó umbral — STOP recomendado

    # ── Hopfield ─────────────────────────────────────────────────────────────

    def _relax(self, sigma: np.ndarray, W: np.ndarray, max_iter: int = 200) -> np.ndarray:
        for _ in range(max_iter):
            h  = W @ sigma
            s2 = np.where(h > 0, 1., np.where(h < 0, -1., sigma))
            if np.allclose(s2, sigma):
                break
            sigma = s2
        return sigma

    def _count_attractors(self, W_eff: np.ndarray) -> int:
        rng = np.random.default_rng(self._seed)
        attractors = set()
        for _ in range(self._n_runs):
            n_act = max(1, int(round(rng.uniform(0.3, 0.7) * self.N)))
            s0    = np.full(self.N, -1.)
            s0[rng.choice(self.N, n_act, replace=False)] = 1.
            attractors.add(tuple(self._relax(s0, W_eff).tolist()))
        return len(attractors)


