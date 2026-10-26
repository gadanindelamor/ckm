"""
p1_relajado.py — Opus 5.5 (Cowork), 4 oct 2026. Driver fuera del repo, corre en el
contenedor de Cowork (no en el Codespace ni en la PC de delamor). Autorizado por delamor
("ustedes lo hacen", "doy permisos").

P1 con dinámica. Parámetro de control k = nodos incorporados (fijados en +1) según un
orden. Los demás nodos quedan LIBRES y relajan (Hopfield asíncrono, regla GOLES h=0
conserva σ), partiendo del estado anterior (memoria del camino).
  UP:   k = 0..N   — se fija order[:k] en +1; el estado se arrastra desde k-1.
  DOWN: k = N..0   — se libera order[k]; el estado se arrastra desde k+1.
A igual k, el conjunto fijado es EL MISMO en UP y DOWN: toda diferencia del estado
relajado es dependencia del camino.
Medidas: m(k) = fracción de nodos en +1; c(S) del estado relajado.
Estadístico: área del lazo A = mean_k |m_up(k) − m_down(k)|.
NULO: la misma W con sus pesos del triángulo superior permutados al azar (conserva la
distribución de pesos y la simetría; destruye la estructura). 200 nulos.
PRE-REGISTRO (Opus, antes de correr): con W ≥ 0 el lazo aparece por física de Ising con
campo, y aparece también en el nulo. Si A_real cae dentro del nulo, P1 es propiedad del
modelo (de cualquier W positiva), no del corpus.
"""
import json, sys, time, platform, subprocess
import numpy as np

REPO, OUT = sys.argv[1], sys.argv[2]
W = np.array(json.load(open(f"{REPO}/process/experiments/W_ckm_corpus_v2.json"))["W"], float)
np.fill_diagonal(W, 0.0)
N = len(W)
N_ORD, N_NULOS, MAX_SWEEPS, SEED = 100, 200, 100, 0

def relajar(s, W, libres, rng):
    for _ in range(MAX_SWEEPS):
        cambio = False
        for i in rng.permutation(libres):
            h = W[i] @ s
            nuevo = 1.0 if h > 0 else (-1.0 if h < 0 else s[i])
            if nuevo != s[i]:
                s[i] = nuevo; cambio = True
        if not cambio:
            return s, True
    return s, False

def lazo(W, order, rng):
    s = -np.ones(N); m_up = np.empty(N + 1); m_dn = np.empty(N + 1); noconv = 0
    for k in range(N + 1):
        if k: s[order[k - 1]] = 1.0
        libres = order[k:]
        s, ok = relajar(s, W, libres, rng); noconv += (not ok)
        m_up[k] = (s > 0).mean()
    for k in range(N, -1, -1):
        libres = order[k:]
        s, ok = relajar(s, W, libres, rng); noconv += (not ok)
        m_dn[k] = (s > 0).mean()
    return m_up, m_dn, noconv

def area(W, rng):
    A, MU, MD, nc = [], [], [], 0
    for _ in range(N_ORD):
        order = rng.permutation(N)
        mu, md, c = lazo(W, order, rng); nc += c
        A.append(np.abs(mu - md).mean()); MU.append(mu); MD.append(md)
    return float(np.mean(A)), np.mean(MU, 0), np.mean(MD, 0), nc

rng = np.random.default_rng(SEED)
t0 = time.time()
A_real, mu, md, nc = area(W, rng)
iu = np.triu_indices(N, 1); w = W[iu]
nulos = []
for _ in range(N_NULOS):
    Wn = np.zeros_like(W); Wn[iu] = rng.permutation(w); Wn = Wn + Wn.T
    nulos.append(area(Wn, np.random.default_rng(rng.integers(1 << 31)))[0])
nulos = np.array(nulos)
sha = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
res = {"repo_commit": sha, "W": "process/experiments/W_ckm_corpus_v2.json (marco previo a las correcciones de sep)",
       "N": N, "W_min": float(W.min()), "W_max": float(W.max()), "media_W": float(w.mean()),
       "n_ordenes": N_ORD, "n_nulos": N_NULOS, "max_sweeps": MAX_SWEEPS, "seed": SEED,
       "dinamica": "Hopfield asíncrono, orden aleatorio por barrido, GOLES h=0 conserva",
       "A_real": A_real, "nulo_media": float(nulos.mean()), "nulo_p5": float(np.percentile(nulos, 5)),
       "nulo_p95": float(np.percentile(nulos, 95)), "nulo_min": float(nulos.min()), "nulo_max": float(nulos.max()),
       "p_mayor": float(((nulos >= A_real).sum() + 1) / (len(nulos) + 1)),
       "p_menor": float(((nulos <= A_real).sum() + 1) / (len(nulos) + 1)),
       "no_convergencias_real": int(nc),
       "m_up_medio": [round(x, 4) for x in mu], "m_down_medio": [round(x, 4) for x in md],
       "python": sys.version.split()[0], "numpy": np.__version__, "platform": platform.platform(),
       "segundos": round(time.time() - t0, 1),
       "variables_no_consideradas": "todas las que no están en este log (delamor)"}
json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in res.items() if not k.startswith("m_")}, indent=1, ensure_ascii=False))
print("m_up  :", res["m_up_medio"][::4]); print("m_down:", res["m_down_medio"][::4])
