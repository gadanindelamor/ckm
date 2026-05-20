"""
ckm_topology_module.py
CKM — Invariantes topológicos y cadenas de orientabilidad

Implementa la conexión con Sciamarella (2001):
    H₀, H₁, H₂  sobre el complejo simplicial del grafo CKM
    Cadenas de orientabilidad → operador candidato para R12

Interpretación CKM:
    H₀ = componentes conexas del conocimiento
    H₁ = ciclos independientes (núcleos de cohesión, k-cores análogos)
    H₂ = cavidades cerradas (zonas de conocimiento faltante)
    Orientabilidad:
        complejo orientable   → cilindro → divergencia resoluble
        complejo no-orientable → Möbius  → inconmensurabilidad estructural (R12)

Uso:
    from ckm_topology_module import run_topology
    results = run_topology(W, nodes, label="ckm_corpus")

    # Comparar dos perspectivas
    from ckm_topology_module import compare_perspectives
    r12 = compare_perspectives(W, nodes, vp_a_nodes, vp_b_nodes)

Requisitos:
    numpy scipy networkx
"""

import json
import numpy as np
import networkx as nx
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ── Construcción del complejo simplicial ──────────────────────────────────────

def build_complex(W, nodes, theta):
    """
    Construye el complejo simplicial de Vietoris-Rips desde W.

    0-simplices: nodos
    1-simplices: aristas con W[i,j] > theta
    2-simplices: triángulos (3-cliques del grafo)

    Retorna:
        G          : nx.Graph
        edges      : list[(i,j)]     — 1-simplices orientados i<j
        triangles  : list[(i,j,k)]   — 2-simplices orientados i<j<k
    """
    N = len(nodes)
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(i + 1, N):
            if W[i, j] > theta:
                G.add_edge(i, j)

    edges = sorted(G.edges())
    triangles = []
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) == 3:
            triangles.append(tuple(sorted(clique)))

    return G, edges, triangles


# ── Matrices de borde ─────────────────────────────────────────────────────────

def boundary_matrix_1(nodes, edges):
    """
    ∂₁ : C₁ → C₀
    ∂₁[v, e] = +1 si v es el extremo final de e
               -1 si v es el extremo inicial de e
    """
    N = len(nodes)
    E = len(edges)
    B1 = np.zeros((N, E), dtype=int)
    for col, (i, j) in enumerate(edges):
        B1[i, col] = -1
        B1[j, col] = +1
    return B1


def boundary_matrix_2(edges, triangles):
    """
    ∂₂ : C₂ → C₁
    ∂₂[e, t] = +1/-1 según orientación del borde del triángulo t que contiene e
    """
    edge_idx = {e: idx for idx, e in enumerate(edges)}
    E = len(edges)
    T = len(triangles)
    B2 = np.zeros((E, T), dtype=int)

    for col, (i, j, k) in enumerate(triangles):
        # Borde del triángulo (i,j,k) con orientación estándar:
        # ∂(i,j,k) = (j,k) - (i,k) + (i,j)
        for edge, sign in [((j, k), +1), ((i, k), -1), ((i, j), +1)]:
            e = tuple(sorted(edge))
            if e in edge_idx:
                # Corregir signo si la orientación del edge está invertida
                if edge[0] > edge[1]:
                    sign = -sign
                B2[edge_idx[e], col] = sign

    return B2


# ── Invariantes de homología ──────────────────────────────────────────────────

def compute_homology(B1, B2, N, E, T):
    """
    H₀, H₁, H₂ del complejo simplicial sobre Z/2Z (campo — sin torsión).

    Usa eliminación gaussiana mod 2 para calcular rangos.

    Retorna:
        h0, h1, h2 : int
        betti      : dict
    """
    def rank_mod2(M):
        """Rango de M sobre GF(2) — eliminación gaussiana."""
        if M.size == 0:
            return 0
        A = M % 2
        rows, cols = A.shape
        rank = 0
        for col in range(cols):
            # Buscar pivot
            pivot = None
            for row in range(rank, rows):
                if A[row, col] == 1:
                    pivot = row
                    break
            if pivot is None:
                continue
            A[[rank, pivot]] = A[[pivot, rank]]
            for row in range(rows):
                if row != rank and A[row, col] == 1:
                    A[row] = (A[row] + A[rank]) % 2
            rank += 1
        return rank

    rank_B1 = rank_mod2(B1)
    rank_B2 = rank_mod2(B2)

    # Fórmulas de Euler-Poincaré
    h0 = N - rank_B1
    h1 = E - rank_B1 - rank_B2
    h2 = T - rank_B2  # aproximación — H2 exacto requiere ∂₃

    return {
        "H0": max(0, h0),
        "H1": max(0, h1),
        "H2": max(0, h2),
        "rank_B1": int(rank_B1),
        "rank_B2": int(rank_B2),
        "chi": N - E + T   # característica de Euler
    }


# ── Orientabilidad ────────────────────────────────────────────────────────────

def check_orientability(edges, triangles):
    """
    Test de orientabilidad del complejo 2-dimensional.

    Un complejo 2D es orientable si y solo si existe una asignación
    consistente de orientaciones a todos los 2-simplices.

    Algoritmo: grafo dual de triángulos.
    - Nodos = triángulos
    - Aristas = pares de triángulos que comparten una arista
    - Peso = +1 si la arista compartida tiene orientación COMPATIBLE
             -1 si es INCOMPATIBLE (requiere invertir orientación)
    El complejo es no-orientable si hay un ciclo de peso negativo impar.

    Retorna:
        orientable     : bool
        n_mobius_loops : int   — ciclos de torsión detectados
        detail         : str
    """
    if not triangles:
        return {"orientable": True, "n_mobius_loops": 0,
                "detail": "sin 2-simplices — orientabilidad trivial"}

    # Índice de aristas → triángulos que la contienen
    edge_to_tris = defaultdict(list)
    for t_idx, (i, j, k) in enumerate(triangles):
        for e in [(i, j), (j, k), (i, k)]:
            edge_to_tris[tuple(sorted(e))].append(t_idx)

    # Grafo dual: triángulos como nodos, aristas compartidas como conexiones
    # Etiquetar si la orientación es compatible o no
    n_tri = len(triangles)
    orientation = {}  # t_idx → +1 o -1 (relativo al primero)

    mobius_loops = 0
    orientation[0] = +1

    # BFS sobre el grafo dual
    from collections import deque
    visited = {0}
    queue = deque([0])

    def shared_edge_sign(t1_idx, t2_idx):
        """
        Retorna +1 si los triángulos t1, t2 induces orientaciones compatibles
        en su arista compartida, -1 si son incompatibles.
        """
        tri1 = triangles[t1_idx]
        tri2 = triangles[t2_idx]
        # Encontrar arista compartida
        shared = set(tri1) & set(tri2)
        if len(shared) != 2:
            return None
        a, b = sorted(shared)

        # Signo de (a,b) según la fórmula de borde: d(i,j,k) = +(j,k) - (i,k) + (i,j)
        # (i,j) → +1,  (j,k) → +1,  (i,k) → -1
        def _edge_sign(tri, a, b):
            i, j, k = tri
            if (a, b) == (i, j) or (a, b) == (j, k):
                return +1
            elif (a, b) == (i, k):
                return -1
            return None  # no debería ocurrir con aristas ordenadas

        sign1 = _edge_sign(tri1, a, b)
        sign2 = _edge_sign(tri2, a, b)

        if sign1 is None or sign2 is None:
            return None

        # Compatible = signos opuestos (se cancelan en el borde del borde)
        return +1 if (sign1 * sign2 == -1) else -1

    while queue:
        t = queue.popleft()
        for e, tris in edge_to_tris.items():
            if t not in tris or len(tris) != 2:
                continue
            t2 = tris[0] if tris[1] == t else tris[1]
            sign = shared_edge_sign(t, t2)
            if sign is None:
                continue

            expected_orient = orientation[t] * sign
            if t2 not in visited:
                orientation[t2] = expected_orient
                visited.add(t2)
                queue.append(t2)
            else:
                # Ya visitado: verificar consistencia
                if orientation[t2] != expected_orient:
                    mobius_loops += 1

    orientable = (mobius_loops == 0)
    detail = ("cilindro — divergencia resoluble" if orientable
              else f"Möbius — {mobius_loops} bucle(s) de torsión — inconmensurabilidad estructural")

    return {
        "orientable": orientable,
        "n_mobius_loops": mobius_loops,
        "detail": detail
    }


# ── Perfil topológico completo ────────────────────────────────────────────────

def topological_profile(W, nodes, thetas=None):
    """
    Perfil topológico del grafo CKM a múltiples thresholds.
    Análogo a homología persistente — tracking de invariantes.

    Retorna lista de dicts, uno por theta.
    """
    if thetas is None:
        thetas = [0.0002, 0.001, 0.005, 0.010, 0.020]

    N = len(nodes)
    profile = []

    for theta in thetas:
        G, edges, triangles = build_complex(W, nodes, theta)
        E, T = len(edges), len(triangles)

        if E == 0:
            profile.append({"theta": theta, "H0": N, "H1": 0, "H2": 0,
                             "E": 0, "T": 0, "orientable": True})
            continue

        B1 = boundary_matrix_1(nodes, edges)
        B2 = boundary_matrix_2(edges, triangles) if T > 0 else np.zeros((E, 0), dtype=int)

        hom = compute_homology(B1, B2, N, E, T)
        orient = check_orientability(edges, triangles)

        profile.append({
            "theta": theta,
            "N": N, "E": E, "T": T,
            **hom,
            "orientable": orient["orientable"],
            "n_mobius_loops": orient["n_mobius_loops"],
            "detail": orient["detail"]
        })

    return profile


# ── Comparación de perspectivas (R12) ─────────────────────────────────────────

def compare_perspectives(W, nodes, vp_a_indices, vp_b_indices, theta=0.001):
    """
    Operador R12: compara dos perspectivas-subgrafo.

    Parámetros:
        W             : ndarray (N×N)
        nodes         : list[str]
        vp_a_indices  : list[int]  — índices de nodos en VP_A
        vp_b_indices  : list[int]  — índices de nodos en VP_B
        theta         : float

    Retorna: dict con
        vp_a_topology : invariantes de VP_A
        vp_b_topology : invariantes de VP_B
        comparison    : diferencias H0/H1/H2
        r12_verdict   : "RESOLUBLE" | "INCONMENSURABLE" | "EQUIVALENTE"
        reason        : str
    """
    def subgraph_topology(indices):
        idx = sorted(set(indices))
        sub_nodes = [nodes[i] for i in idx]
        sub_W = W[np.ix_(idx, idx)]
        _, edges, triangles = build_complex(sub_W, sub_nodes, theta)
        N_sub = len(idx)
        E_sub, T_sub = len(edges), len(triangles)

        if E_sub == 0:
            return {"H0": N_sub, "H1": 0, "H2": 0, "orientable": True,
                    "n_mobius_loops": 0, "N": N_sub, "E": 0, "T": 0}

        B1 = boundary_matrix_1(sub_nodes, edges)
        B2 = (boundary_matrix_2(edges, triangles) if T_sub > 0
              else np.zeros((E_sub, 0), dtype=int))
        hom = compute_homology(B1, B2, N_sub, E_sub, T_sub)
        orient = check_orientability(edges, triangles)

        return {**hom, "orientable": orient["orientable"],
                "n_mobius_loops": orient["n_mobius_loops"],
                "N": N_sub, "E": E_sub, "T": T_sub}

    topo_a = subgraph_topology(vp_a_indices)
    topo_b = subgraph_topology(vp_b_indices)

    # Determinar veredicto R12
    same_orient = topo_a["orientable"] == topo_b["orientable"]
    same_h = (topo_a["H0"] == topo_b["H0"] and
              topo_a["H1"] == topo_b["H1"] and
              topo_a["H2"] == topo_b["H2"])

    if same_orient and same_h:
        verdict = "EQUIVALENTE"
        reason  = "mismos invariantes H0/H1/H2 y orientabilidad"
    elif not same_orient:
        verdict = "INCONMENSURABLE"
        reason  = (f"torsión diferente: VP_A={'Möbius' if not topo_a['orientable'] else 'cilindro'}"
                   f" vs VP_B={'Möbius' if not topo_b['orientable'] else 'cilindro'}")
    else:
        verdict = "RESOLUBLE"
        reason  = f"misma orientabilidad, H diferente: ΔH1={topo_b['H1']-topo_a['H1']}"

    return {
        "vp_a": topo_a,
        "vp_b": topo_b,
        "comparison": {
            "delta_H0": topo_b["H0"] - topo_a["H0"],
            "delta_H1": topo_b["H1"] - topo_a["H1"],
            "delta_H2": topo_b["H2"] - topo_a["H2"],
        },
        "r12_verdict": verdict,
        "reason": reason
    }


# ── Runner principal ──────────────────────────────────────────────────────────

def run_topology(W, nodes, label="corpus", output_dir=".",
                 thetas=None, write_reg=True):
    """
    Corre el análisis topológico completo y escribe REG.

    Retorna: dict con perfil + baseline a theta=0.0002
    """
    if thetas is None:
        thetas = [0.0002, 0.001, 0.005, 0.010, 0.020]

    print(f"\n=== CKM Topología — {label} ===")
    print(f"N={len(nodes)}")

    profile = topological_profile(W, nodes, thetas)

    print(f"\n  {'theta':>8}  {'E':>5}  {'T':>6}  "
          f"{'H0':>4}  {'H1':>5}  {'H2':>4}  {'orient':>12}")
    print(f"  {'-'*60}")
    for p in profile:
        ort = "cilindro" if p.get("orientable") else f"Möbius({p.get('n_mobius_loops',0)})"
        print(f"  {p['theta']:>8.4f}  {p.get('E',0):>5}  {p.get('T',0):>6}  "
              f"{p.get('H0',0):>4}  {p.get('H1',0):>5}  {p.get('H2',0):>4}  {ort:>12}")

    # Baseline: theta mínimo con H0=1
    baseline = next((p for p in profile if p.get("H0") == 1), profile[0])
    print(f"\n  Baseline (theta={baseline['theta']}):")
    print(f"    H0={baseline['H0']} H1={baseline['H1']} H2={baseline['H2']}")
    print(f"    {baseline.get('detail', baseline.get('orientable'))}")

    reg = {
        "label": label,
        "N": len(nodes),
        "nodes": nodes,
        "thresholds": profile,
        "baseline": baseline,
        "date": datetime.now().strftime('%Y-%m-%d')
    }

    if write_reg:
        out = Path(output_dir)
        out.mkdir(exist_ok=True)
        path = out / f"REG_topology_{label}.json"
        path.write_text(__import__('json').dumps(reg, ensure_ascii=False, indent=2))
        print(f"\n  REG escrito: {path.name}")

    return reg


# ── Standalone ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))

    # Cargar corpus CKM
    corpus_path = Path(__file__).parent / "W_ckm_corpus_v2.json"
    if not corpus_path.exists():
        print(f"No se encontró {corpus_path}")
        sys.exit(1)

    with open(corpus_path) as f:
        d = __import__('json').load(f)

    nodes = d['nodes']
    W = np.array(d['W'])

    results = run_topology(W, nodes, label="ckm_corpus_v2",
                           output_dir=".", write_reg=True)

    # Ejemplo de comparación de perspectivas (R12)
    # VP_A: nodos de cluster C3 "motor" (índices 0-12 aproximados)
    # VP_B: nodos de cluster C4 "suelo" (índices 13-16 aproximados)
    print("\n--- Ejemplo comparación R12 ---")
    mid = len(nodes) // 2
    r12 = compare_perspectives(W, nodes,
                                vp_a_indices=list(range(mid)),
                                vp_b_indices=list(range(mid, len(nodes))))
    print(f"VP_A (nodos 0-{mid-1}): H0={r12['vp_a']['H0']} H1={r12['vp_a']['H1']} "
          f"orient={'cilindro' if r12['vp_a']['orientable'] else 'Möbius'}")
    print(f"VP_B (nodos {mid}-{len(nodes)-1}): H0={r12['vp_b']['H0']} H1={r12['vp_b']['H1']} "
          f"orient={'cilindro' if r12['vp_b']['orientable'] else 'Möbius'}")
    print(f"R12: {r12['r12_verdict']} — {r12['reason']}")
