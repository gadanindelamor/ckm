"""
cluster_frontier_density — Cluster Frontier Coercivity

Función propuesta para analytics.py (CKM).

Qué mide: densidad de peso W intra-cluster vs inter-cluster.
Técnica: partición de pares por cluster + mean(W_ij) por grupo.
Representación estructural CKM: coercitividad de cada frontera entre clusters
— cuánto más cohesionado es cada cluster internamente respecto a sus bordes.

Alta coercitividad(Ci, Cj): la frontera resiste el cruce.
Baja coercitividad: clusters porosos, la distinción es débil.
inf: sin aristas inter-cluster (clusters completamente separados en W).
"oposicion": inter < 0 — oposición estructural activa entre clusters. Otro
    régimen: min(intra)/inter no aplica. Semánticamente opuesto a inf.
Cluster de 1 nodo: intra = 0 → coercividad 0, se lee como porosa (anotado).

Claves de frontera: "Ca|Cb" (serializable a JSON).
Ver docs/tasks/TASK_neff_y_frontera_logica_v1.md.
"""

from __future__ import annotations
import numpy as np

OPOSICION = "oposicion"


def cluster_frontier_density(
    clusters: dict[str, list[str]],
    nodes: list[str],
    W: np.ndarray,
) -> dict:
    """
    Intra- and inter-cluster mean W weight density.

    Parameters
    ----------
    clusters : dict[str, list[str]]
        Partition from cluster_nodes(). {label: [node_names]}
    nodes : list[str]
        Node list matching W row/col order.
    W : np.ndarray
        N×N weight matrix (W_pos or W_mixta).

    Returns
    -------
    dict with keys:
        "intra"      : {label: float}         — mean W within cluster
        "inter"      : {"Ca|Cb": float}       — mean W across cluster pair
        "coercivity" : {"Ca|Cb": float | "oposicion"}
                       inter > 0 → min(intra_a, intra_b) / inter
                       inter = 0 → inf
                       inter < 0 → "oposicion"
        "n_pairs"    : {label or "Ca|Cb": int} — pair counts for each entry
    """
    node_idx = {n: i for i, n in enumerate(nodes)}
    labels = list(clusters.keys())

    # ── intra-cluster ─────────────────────────────────────────────────────────
    intra: dict[str, float] = {}
    n_pairs_intra: dict[str, int] = {}
    for label, members in clusters.items():
        idxs = [node_idx[m] for m in members if m in node_idx]
        if len(idxs) < 2:
            intra[label] = 0.0
            n_pairs_intra[label] = 0
            continue
        pairs = [(idxs[i], idxs[j])
                 for i in range(len(idxs))
                 for j in range(i + 1, len(idxs))]
        intra[label] = float(np.mean([W[i, j] for i, j in pairs]))
        n_pairs_intra[label] = len(pairs)

    # ── inter-cluster and coercivity ──────────────────────────────────────────
    inter: dict[str, float] = {}
    coercivity: dict[str, object] = {}
    n_pairs_inter: dict[str, int] = {}
    for ai in range(len(labels)):
        for bi in range(ai + 1, len(labels)):
            a, b = labels[ai], labels[bi]
            a_idxs = [node_idx[m] for m in clusters[a] if m in node_idx]
            b_idxs = [node_idx[m] for m in clusters[b] if m in node_idx]
            if not a_idxs or not b_idxs:
                continue
            pairs = [(i, j) for i in a_idxs for j in b_idxs]
            inter_val = float(np.mean([W[i, j] for i, j in pairs]))
            clave = f"{a}|{b}"
            inter[clave] = inter_val
            n_pairs_inter[clave] = len(pairs)
            if inter_val > 1e-12:
                coercivity[clave] = min(intra[a], intra[b]) / inter_val
            elif inter_val < -1e-12:
                coercivity[clave] = OPOSICION
            else:
                coercivity[clave] = float("inf")

    return {
        "intra": intra,
        "inter": inter,
        "coercivity": coercivity,
        "n_pairs": {**n_pairs_intra, **n_pairs_inter},
    }


# ── uso típico ────────────────────────────────────────────────────────────────
#
# from ckm.analytics import cluster_nodes
# from cluster_frontier_density import cluster_frontier_density
#
# clusters = cluster_nodes(attractors, nodes, n_clusters=4)
# result = cluster_frontier_density(clusters, nodes, graph.W)
#
# for clave, h in result["coercivity"].items():
#     ca, cb = clave.split("|")
#     print(f"{ca}↔{cb}  coercivity={h}  "
#           f"intra=({result['intra'][ca]:.4f}, {result['intra'][cb]:.4f})  "
#           f"inter={result['inter'][clave]:.4f}")
