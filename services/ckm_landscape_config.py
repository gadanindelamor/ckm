"""
ckm_landscape_config.py — CKMlandscapeConfig

Contrato vivo del instrumento (DEFS v11 §0 Modelo Conceptual). No es una
bolsa de constantes: lo que se puede medir de W se mide de W; lo que todavía
es decisión abierta se exige como parámetro, sin default.

Independiente de CKMConfig (process/initial_static_model/core.py): no hereda,
no toma sus valores. Todavía no la consume ningún servicio (TASK v1).

Dos identidades distintas:
  w_version_id — sha256(W) vía w_version.py. Identifica a W.
  config_id    — uuid por instancia, con timestamp. Identifica a la config.

Spec: docs/tasks/TASK_CKMlandscapeConfig_v1.md
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, asdict

import numpy as np

from w_version import sha256_W

SAMPLING_MODES = ("uniform", "weighted", "boltzmann")
SCALES = ("linear", "log")
RHO_STAR = 0.5   # misma ρ* que coco.BETA_RHO_STAR


@dataclass(frozen=True)
class CKMlandscapeConfig:
    N               : int
    mu_W_nonzero    : float
    mu_W_global     : float
    beta_c_nonzero  : float
    beta_c_global   : float
    theta_W         : float
    sampling_mode   : str
    scale           : str
    w_version_id    : str
    config_id       : str
    timestamp       : float

    @classmethod
    def from_W(
        cls,
        W            : np.ndarray,
        *,
        theta_W      : float,
        sampling_mode: str,
        scale        : str,
    ) -> "CKMlandscapeConfig":
        """
        Construye la config midiendo W. theta_W, sampling_mode y scale son
        obligatorios: no hay default hasta que el modelo los decida.

        mu_W se porta en sus dos formas, con nombre explícito. Cada
        consumidor declara cuál usa; la config no elige. beta_c sigue a
        mu_W: una por cada forma (coco.beta_c_corpus usa la global).
        """
        W = np.asarray(W, dtype=float)
        if W.ndim != 2 or W.shape[0] != W.shape[1]:
            raise ValueError(f"W debe ser cuadrada, shape={W.shape}")
        if sampling_mode not in SAMPLING_MODES:
            raise ValueError(f"sampling_mode inválido: {sampling_mode!r} — esperado {SAMPLING_MODES}")
        if scale not in SCALES:
            raise ValueError(f"scale inválida: {scale!r} — esperado {SCALES}")

        N = W.shape[0]
        ii, jj = np.triu_indices(N, k=1)
        pares = W[ii, jj]
        no_nulos = pares[pares != 0]
        mu_global  = float(pares.mean()) if len(pares) else 0.0
        mu_nonzero = float(no_nulos.mean()) if len(no_nulos) else 0.0

        return cls(
            N              = N,
            mu_W_nonzero   = mu_nonzero,
            mu_W_global    = mu_global,
            beta_c_nonzero = _beta_c(N, mu_nonzero),
            beta_c_global  = _beta_c(N, mu_global),
            theta_W        = float(theta_W),
            sampling_mode  = sampling_mode,
            scale          = scale,
            w_version_id   = sha256_W(W),
            config_id      = uuid.uuid4().hex,
            timestamp      = time.time(),
        )

    @staticmethod
    def theta_W_formula(mu_W: float, N: int) -> float:
        """
        Fórmula de theta_W como función de mu_W y N — NO decidida.

        Propiedad requerida (PROPUESTA v4, Paso 3 / D1): con la normalización
        de W declarada, al menos el núcleo A del corpus pasa C1
        (max|W(nodo, activos)| ≥ theta_W). Mientras no exista, theta_W es
        parámetro obligatorio de from_W.
        """
        raise NotImplementedError("fórmula de theta_W abierta — ver docstring")

    # ── serialización ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def from_dict(cls, d: dict) -> "CKMlandscapeConfig":
        """Recarga una config serializada: mismos valores, mismo config_id."""
        return cls(**d)

    @classmethod
    def from_json(cls, s: str) -> "CKMlandscapeConfig":
        return cls.from_dict(json.loads(s))


def _beta_c(N: int, mu_W: float) -> float:
    """β_c = 1 / (ρ* · N · μ_W). Misma fórmula que COCO.beta_c_corpus."""
    if mu_W <= 0:
        return float("inf")
    return 1.0 / (RHO_STAR * N * mu_W)
