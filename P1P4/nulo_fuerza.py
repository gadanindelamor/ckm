import numpy as np
def nulo_fuerza(W, rng, pasos_por_par=20):
    """Nulo que conserva EXACTAMENTE la fuerza (suma de pesos) de cada nodo y la no-negatividad.
    Paso: i,j,k,l distintos; δ se suma a W_ij y W_kl y se resta a W_il y W_kj.
    δ uniforme en el rango que mantiene los cuatro pesos >= 0."""
    M = W.copy(); N = len(M); n_pares = N * (N - 1) // 2
    for _ in range(pasos_por_par * n_pares):
        i, j, k, l = rng.choice(N, 4, replace=False)
        lo = -min(M[i, j], M[k, l]); hi = min(M[i, l], M[k, j])
        if hi - lo <= 0: continue
        d = rng.uniform(lo, hi)
        for a, b, s in ((i, j, d), (k, l, d), (i, l, -d), (k, j, -d)):
            M[a, b] += s; M[b, a] += s
    return M
