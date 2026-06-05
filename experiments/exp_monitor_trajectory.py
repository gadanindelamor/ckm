"""
exp_monitor_trajectory.py — Trayectoria cohesiva → FabricationService

[SNIPPET]  = código directo del snippet de sesión "Take your time"
[INFERRED] = reconstruido desde REG + estructura

Diferencia vs original: sigma inicia parcialmente activo (rho=0.5)
para que fi sea no-trivial desde t=0. En el original sigma era parcial
por construcción del loop — reconstruido aquí explícitamente.
"""

import json, shutil
import numpy as np
from fabrication_service_dev import FabricationService

# Parámetros                                          [SNIPPET]
SEED = 42; T_STEPS = 80; N_RUNS = 100; ETA_FACTOR = 1.0; AMP = 15
np.random.seed(SEED)

with open("W_ckm_corpus_v2.json") as f:
    data = json.load(f)
nodes = data["nodes"]; N = len(nodes)
W_base = np.array(data["W"])
mean_W = W_base[W_base > 0].mean(); ETA = ETA_FACTOR * mean_W

W_mixta = W_base.copy()                              # [SNIPPET]
for i, j in [(13,22),(15,16),(18,20)]:
    W_mixta[i,j] = -W_base[i,j]*AMP; W_mixta[j,i] = -W_base[i,j]*AMP

def relax(sigma, W, max_iter=100):                   # [SNIPPET]
    for _ in range(max_iter):
        h = W @ sigma
        s2 = np.where(h>0, 1., np.where(h<0, -1., sigma))
        if np.allclose(s2, sigma): break
        sigma = s2
    return sigma

ii_all, jj_all = np.triu_indices(N, k=1)            # [SNIPPET]
w_probs = W_base[ii_all,jj_all] / W_base[ii_all,jj_all].sum()

for W_label, W_start in [("W_base", W_base), ("W_mixta", W_mixta)]:

    shutil.rmtree(f"storage/{W_label}", ignore_errors=True)
    svc = FabricationService(                        # [SNIPPET]
        W_label, W_start, nodes,
        storage_dir=f"storage/{W_label}", n_runs=N_RUNS
    )
    Delta = np.zeros((N,N))
    np.random.seed(SEED)

    # sigma inicial: parcial (rho=0.5) para fi no-trivial  [INFERRED]
    n_act = int(N * 0.5)
    sigma = np.full(N, -1.)
    sigma[np.random.choice(N, n_act, replace=False)] = 1.
    sigma = relax(sigma, W_start)

    print(f"\n── {W_label} ──")
    print(f"{'t':>3} | {'quad':<20} | {'c_S':>7} | {'D_ckm':>6} | {'fi':>5} | {'R':>5} | críticos")
    print("-"*85)

    for t in range(T_STEPS):
        k = np.random.choice(len(ii_all), p=w_probs)
        i, j = ii_all[k], jj_all[k]
        Delta[i,j] += ETA; Delta[j,i] += ETA

        sigma = relax(sigma, W_start)               # trayectoria cohesiva
        panel = svc.snapshot(sigma, Delta, t)

        if t % 10 == 0 or t < 3:
            c = ", ".join(panel["criticos"][:2]) if panel["criticos"] else "—"
            print(f"{t:>3} | {panel['quadrant']:<20} | "
                  f"{panel['c_S']:>7.5f} | {panel['D_ckm']:>6.3f} | "
                  f"{panel['fabrication_index']:>5.3f} | {panel['recovery']:>5.3f} | {c}")

    sig = svc.stop_signal(window=10)                # [SNIPPET]
    print(f"\nstop_signal: {sig['direction']} | fi_trend={sig['fi_trend']} | D_trend={sig['D_trend']}")
