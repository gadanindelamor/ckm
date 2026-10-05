"""
replica_fig5.py — Replicación independiente de la "modularidad óptima" de
Aiyappa, Flammini & Ahn (Sci. Adv. 2024, doi 10.1126/sciadv.adh4439), Fig. 5.
Opus 5.5 (Cowork), 4 oct 2026, a pedido de delamor. Port 1:1 de
github.com/rachithaiyappa/beliefnet @ 2289c39: scripts/optimalmodularity.jl + src/beliefnet/function.jl.
Loop de dinámica en C (dyn.c); red, semillas y aleatorios en numpy.

PRE-REGISTRO (escrito antes de correr):
  Parámetros del README del repo: α=2.0, β=1.0, σ=0.2. N=100, M=1500, T=2·M·N.
  μ: los 20 valores de LinRange(0.01, 0.5, 20) redondeados a 2 decimales (como el Julia).
  ρ0 (fracción de semillas): {0.05, 0.10, 0.15, 0.20, 0.25, 0.30}. 10 ensembles por celda.
  Dos condiciones: "dual_stable" (contagio complejo, la del paper) y "unstable" (contagio simple, control).
  Medida: fracción final stable_plus (los tres pesos > 0), como final_fraction del Julia.
  Criterio "SE SOSTIENE" (complejo): para al menos un ρ0, el μ que maximiza la media es interior
    (no entre los 2 primeros ni los 2 últimos de la grilla) y su media supera a la de μ_min y a la de
    μ_max por más de 2 errores estándar combinados.
  Criterio "NO SE SOSTIENE": para ningún ρ0 se cumple lo anterior.
  Control (simple): se espera que NO haya óptimo interior en ese sentido. Si lo hay, se reporta.
  No se ajusta nada después de ver el dato.
"""
import ctypes, json, sys, time, platform
from itertools import combinations, product
import numpy as np

lib = ctypes.CDLL("./libdyn.so")
P_i = np.ctypeslib.ndpointer(dtype=np.int32, flags="C_CONTIGUOUS")
P_d = np.ctypeslib.ndpointer(dtype=np.float64, flags="C_CONTIGUOUS")
lib.dinamica.argtypes = [ctypes.c_int, P_i, P_i, P_i, P_i, P_i, P_d, P_d, P_i,
                         ctypes.c_double, ctypes.c_double, ctypes.c_double]
lib.dinamica.restype = None

N, M = 100, 1500
T = 2 * M * N
ALPHA, BETA, SIGMA = 2.0, 1.0, 0.2
MUS = [round(float(x), 2) for x in np.linspace(0.01, 0.5, 20)]
RHO0 = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
ENS = 10

def red_sbm(rng, mu):
    intra = int(np.ceil((1 - mu) * M)); inter = M - intra
    comm1 = rng.choice(N, int(np.ceil(N / 2)), replace=False)
    comm2 = np.array(sorted(set(range(N)) - set(comm1.tolist())))
    intra_all = list(combinations(comm1.tolist(), 2)) + list(combinations(comm2.tolist(), 2))
    inter_all = list(product(comm1.tolist(), comm2.tolist()))
    e_in = [intra_all[i] for i in rng.choice(len(intra_all), intra, replace=False)]
    e_out = [inter_all[i] for i in rng.choice(len(inter_all), inter, replace=False)]
    E = np.array(e_in + e_out, dtype=np.int32)
    E = np.unique(np.sort(E, axis=1), axis=0)          # SimpleGraph colapsa duplicados
    return E, comm1, comm2

def correr(rng, mu, n_semillas, cond):
    E, comm1, comm2 = red_sbm(rng, mu)
    fijos = rng.choice(comm2, n_semillas, replace=False)
    fijo = np.zeros(N, dtype=np.int32); fijo[fijos] = 1
    B = np.empty((N, 3))
    for i in range(N):
        if fijo[i]: B[i] = (1, 1, 1)
        else: B[i] = (1, -1, -1) if cond == "dual_stable" else (-1, 1, 1)
    eidx = rng.integers(0, len(E), T).astype(np.int32)
    dirr = rng.integers(0, 2, T).astype(np.int32)
    focal = rng.integers(0, 3, T).astype(np.int32)
    gauss = rng.standard_normal(T)
    B = np.ascontiguousarray(B)
    lib.dinamica(T, np.ascontiguousarray(E[:, 0]), np.ascontiguousarray(E[:, 1]), eidx, dirr, focal,
                 gauss, B, fijo, ALPHA, BETA, SIGMA)
    stable_plus = float(np.mean(np.all(B > 0, axis=1)))
    return stable_plus

def criterio(tab):
    """tab[mu][rho] = lista de ENS valores. Devuelve detalle por rho y veredicto."""
    out = {}
    for r in RHO0:
        med = np.array([np.mean(tab[m][r]) for m in MUS]); se = np.array([np.std(tab[m][r], ddof=1) / np.sqrt(ENS) for m in MUS])
        k = int(np.argmax(med)); interior = 2 <= k <= len(MUS) - 3
        sep_min = med[k] - med[0] > 2 * np.hypot(se[k], se[0])
        sep_max = med[k] - med[-1] > 2 * np.hypot(se[k], se[-1])
        out[str(r)] = dict(mu_opt=MUS[k], media_opt=round(float(med[k]), 3), media_mu_min=round(float(med[0]), 3),
                           media_mu_max=round(float(med[-1]), 3), interior=bool(interior),
                           supera_extremos=bool(sep_min and sep_max), cumple=bool(interior and sep_min and sep_max),
                           medias=[round(float(x), 3) for x in med])
    return out, any(v["cumple"] for v in out.values())

if __name__ == "__main__":
    OUT = sys.argv[1]
    rng = np.random.default_rng(0); t0 = time.time(); res = {}
    for cond in ("dual_stable", "unstable"):
        tab = {m: {r: [] for r in RHO0} for m in MUS}
        for e in range(ENS):
            for m in MUS:
                for r in RHO0:
                    tab[m][r].append(correr(rng, m, int(round(r * N)), cond))
        det, ver = criterio(tab)
        res[cond] = dict(veredicto_optimo_interior=ver, por_rho0=det)
        print(cond, "óptimo interior:", ver, round(time.time() - t0, 1), "s", flush=True)
    res["meta"] = dict(fuente="github.com/rachithaiyappa/beliefnet @ 2289c39 (optimalmodularity.jl)", N=N, M=M, T=T,
                       alpha=ALPHA, beta=BETA, sigma=SIGMA, mus=MUS, rho0=RHO0, ensembles=ENS, seed=0,
                       python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(),
                       segundos=round(time.time() - t0, 1))
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
