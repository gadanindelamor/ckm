"""
gatekeeper_c1.py — C1 del gatekeeper, con theta_W declarado

Único criterio del gatekeeper que decide algo hoy (D1). C2 acepta todo, C3 y
C4 no se ejercen — ver docs/tasks/TASK_gatekeeper_C1_theta_W_v1.md.

Semántica sin cambios respecto de CKMGraph.gatekeeper en
process/initial_static_model/core.py:

    max|W(nodo, activos)| ≥ theta_W

theta_W es obligatorio y **sin fórmula**: lo declara quien llama, igual que el
estado activo sigma. theta_W es de este módulo — salió de
CKMlandscapeConfig en el CP3 de TASK_CKMlandscapeConfig_v3 (decisión de
delamor, 7 oct 2026): pertenece a W estática, no al landscape.

**La fórmula de theta_W sigue abierta**, y la propiedad que tendría que
cumplir, que antes vivía en CKMlandscapeConfig.theta_W_formula, es ésta:
con la normalización de W declarada, al menos el núcleo A del corpus pasa C1
(max|W(nodo, activos)| ≥ theta_W). Ver PROPUESTA v4, Paso 3 / D1. Mientras no
exista, theta_W es parámetro obligatorio y nadie le pone default.
"""

from __future__ import annotations

import numpy as np


def c1_max_conn(W: np.ndarray, sigma: np.ndarray, node: int) -> float:
    """max|W(node, j)| sobre los j con sigma == 1. 0.0 si no hay activos."""
    active_idx = np.where(sigma == 1)[0]
    if len(active_idx) == 0:
        return 0.0
    return float(np.max(np.abs(W[node, active_idx])))


def c1(W: np.ndarray, sigma: np.ndarray, node: int, *, theta_W: float) -> bool:
    """C1: el nodo tiene al menos una conexión ≥ theta_W con el estado activo."""
    return c1_max_conn(W, sigma, node) >= theta_W
