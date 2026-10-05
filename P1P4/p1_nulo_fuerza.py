"""p1_nulo_fuerza.py — corrección del 4 oct (Opus 5.5). El nulo N_grado de verificacion_p1_p3.py
casi no mezcla en grafos densos (W_viejo: 6.5% de pesos movidos, corr 0.98 con W) — era un nulo
inválido. Este reemplaza N_grado por N_fuerza: conserva exactamente la fuerza de cada nodo y mezcla.
Mismo P1, misma dinámica, 200 nulos, seed 0. Se reporta también la correlación media nulo–W."""
import sys, json, numpy as np
REPO, OUT = sys.argv[1], sys.argv[2]
src = open("verificacion_p1_p3.py").read().split("# ── main")[0]
sys.argv = ["x", REPO, "/dev/null"]; ns = {}; exec(src, ns); exec(open("nulo_fuerza.py").read(), ns)
rng = np.random.default_rng(0); res = {}
for nombre in ["W_viejo", "W_nuevo"]:
    W = ns[nombre](); iu = np.triu_indices(len(W), 1)
    A, nc = ns["area_lazo"](W, rng); Ns, cs = [], []
    for _ in range(200):
        M = ns["nulo_fuerza"](W, rng); cs.append(np.corrcoef(M[iu], W[iu])[0, 1]); Ns.append(ns["area_lazo"](M, rng)[0])
    Ns = np.array(Ns)
    res[nombre] = dict(A_real=A, no_conv=nc, N_fuerza=dict(media=float(Ns.mean()), p5=float(np.percentile(Ns, 5)),
        p95=float(np.percentile(Ns, 95)), max=float(Ns.max()), p=float(((Ns >= A).sum() + 1) / 201),
        corr_media_con_W=float(np.mean(cs))))
    print(nombre, json.dumps(res[nombre]), flush=True)
json.dump(res, open(OUT, "w"), indent=1)
