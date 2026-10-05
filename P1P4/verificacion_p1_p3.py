"""
verificacion_p1_p3.py — Opus 5.5 (Cowork), 4 oct 2026.
Autorizado por delamor (constancia escrita en el chat): pruebas que se ajusten a la ciencia,
sin su participación. Corre en el contenedor de Cowork. No toca código del repo: lo importa
de services/ sólo para construir W.

PRE-REGISTRO (escrito antes de correr; Opus):
  Dos W:
    W_viejo : process/experiments/W_ckm_corpus_v2.json (marco previo a las correcciones de sep;
              es la W sobre la que el paper reporta P1–P4 con N=32).
    W_nuevo : informes, unidad párrafo (870 textos), CorpusService actual, top_k=32,
              force_w_pos=True (el corpus no tiene tensión: SALAMANCA / REG_unidad_texto §5).
  Dos nulos por W (200 c/u):
    N_perm  : pesos del triángulo superior permutados al azar (conserva distribución de pesos).
    N_grado : intercambios dobles de aristas (Maslov–Sneppen) con el peso viajando con la arista
              (conserva el grado binario de cada nodo y la distribución de pesos).
  P1 — histéresis con relajación. Control k = nodos fijados en +1 según un orden; el resto libre,
       Hopfield asíncrono, GOLES. UP k=0..N, DOWN k=N..0, estado arrastrado. A igual k el conjunto
       fijado es el mismo. Estadístico: área A = mean_k |m_up − m_down|. Test: A_real > nulo (una cola).
  P2 — cascadas k-core (k=2) tras remover un nodo del core, sobre grafos umbral θ. θ = cuantiles
       {0.3, 0.5, 0.7} de los pesos positivos (declarados, iguales para todas las W).
       Ajuste discreto truncado [s_min=2, N]: ley de potencia vs exponencial, razón de
       verosimilitud normalizada (Vuong). Se reporta τ y el rango en décadas disponible.
  P3 — asimetría remoción/re-adición en k-core: remover nodo → rondas de poda;
       re-adicionar con sus aristas → rondas de bootstrap y fracción del core recuperada.
       Estadístico: diferencia de rondas (rem − add) y recuperación < 1 (irreversibilidad).
       Comparado contra N_perm.
  P4 — no se corre: requiere W_mixta de un corpus con tensión estructural por diseño. Las W
       disponibles no la tienen (informes: autor único). Veredicto declarado: NO MEDIBLE.
  Comparaciones: P1 2 W × 2 nulos = 4. P2 2 W × 3 θ = 6. P3 2 W × 3 θ = 6. Total 16.
  Bonferroni α = 0.05/16 = 0.003125. Con 200 nulos la resolución de p es 1/201 ≈ 0.005 >
  0.003125 → p mínimo resoluble NO alcanza Bonferroni en P1/P3. Se declara y se reporta igual
  (p < 0.005 = ningún nulo alcanza al real).
"""
import json, sys, time, platform, subprocess, tempfile
import numpy as np
import networkx as nx

REPO, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, f"{REPO}/services")
SEED = 0
N_NULOS = 200
N_ORD = 60
MAX_SWEEPS = 100

# ── W ──────────────────────────────────────────────────────────────────────
def W_viejo():
    W = np.array(json.load(open(f"{REPO}/process/experiments/W_ckm_corpus_v2.json"))["W"], float)
    np.fill_diagonal(W, 0.0); return W

def W_nuevo():
    from corpus_service import CorpusService
    txt = [l.strip() for l in open(f"{REPO}/process/corpus_informes/corpus_informes.txt", encoding="utf-8") if l.strip()]
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"), min_texts=len(txt), top_k=32,
                      force_w_pos=True, rebuild_suspendido=True)
    c.ingest(txt); W = np.array(c.get_W(), float); np.fill_diagonal(W, 0.0); return W

# ── nulos ──────────────────────────────────────────────────────────────────
def nulo_perm(W, rng):
    N = len(W); iu = np.triu_indices(N, 1)
    M = np.zeros_like(W); M[iu] = rng.permutation(W[iu]); return M + M.T

def nulo_grado(W, rng, n_swaps_por_arista=10):
    N = len(W); M = W.copy()
    aristas = [(i, j) for i in range(N) for j in range(i + 1, N) if M[i, j] != 0]
    E = len(aristas)
    for _ in range(n_swaps_por_arista * E):
        a, b = rng.choice(E, 2, replace=False)
        (i, j), (k, l) = aristas[a], aristas[b]
        if rng.random() < 0.5: k, l = l, k
        if len({i, j, k, l}) < 4 or M[i, l] != 0 or M[k, j] != 0: continue
        wa, wb = M[i, j], M[k, l]
        M[i, j] = M[j, i] = 0; M[k, l] = M[l, k] = 0
        M[i, l] = M[l, i] = wa; M[k, j] = M[j, k] = wb
        aristas[a], aristas[b] = (min(i, l), max(i, l)), (min(k, j), max(k, j))
    return M

# ── P1 ─────────────────────────────────────────────────────────────────────
def relajar(s, W, libres, rng):
    for _ in range(MAX_SWEEPS):
        cambio = False
        for i in rng.permutation(libres):
            h = W[i] @ s
            n = 1.0 if h > 0 else (-1.0 if h < 0 else s[i])
            if n != s[i]: s[i] = n; cambio = True
        if not cambio: return s, True
    return s, False

def area_lazo(W, rng):
    N = len(W); A = []; nc = 0
    for _ in range(N_ORD):
        order = rng.permutation(N); s = -np.ones(N); mu = np.empty(N + 1); md = np.empty(N + 1)
        for k in range(N + 1):
            if k: s[order[k - 1]] = 1.0
            s, ok = relajar(s, W, order[k:], rng); nc += not ok; mu[k] = (s > 0).mean()
        for k in range(N, -1, -1):
            s, ok = relajar(s, W, order[k:], rng); nc += not ok; md[k] = (s > 0).mean()
        A.append(np.abs(mu - md).mean())
    return float(np.mean(A)), nc

# ── k-core: P2 y P3 ────────────────────────────────────────────────────────
def grafo(W, theta):
    N = len(W); G = nx.Graph(); G.add_nodes_from(range(N))
    ii, jj = np.where(np.triu(W, 1) > theta); G.add_edges_from(zip(ii.tolist(), jj.tolist())); return G

def poda(G, core, k):
    core = set(core); rondas = 0
    while True:
        fuera = [n for n in core if sum(1 for m in G[n] if m in core) < k]
        if not fuera: return core, rondas
        core -= set(fuera); rondas += 1

def bootstrap(G, core, k):
    core = set(core); rondas = 0
    while True:
        dentro = [n for n in G.nodes if n not in core and sum(1 for m in G[n] if m in core) >= k]
        if not dentro: return core, rondas
        core |= set(dentro); rondas += 1

def cascadas(W, theta, k=2):
    G = grafo(W, theta); core0 = set(nx.k_core(G, k).nodes)
    tam, rem_r, add_r, recup = [], [], [], []
    for i in sorted(core0):
        G2 = G.copy(); G2.remove_node(i)
        core1, r = poda(G2, core0 - {i}, k)
        tam.append(len(core0) - len(core1)); rem_r.append(r)
        core2, a = bootstrap(G, core1 | {i}, k)
        add_r.append(a); recup.append(len(core2 & core0) / len(core0))
    return dict(core=len(core0), tam=tam, rem=rem_r, add=add_r, recup=recup)

def ajuste(s, N):
    s = np.array([x for x in s if x >= 2]); n = len(s)
    if n < 10: return dict(n=n, tau=None, R=None, p=None, decadas=None)
    xs = np.arange(2, N + 1)
    def ll_pl(t): Z = np.sum(xs ** -t); return -t * np.log(s).sum() - n * np.log(Z), -t * np.log(s) - np.log(Z)
    def ll_ex(l): Z = np.sum(np.exp(-l * xs)); return -l * s.sum() - n * np.log(Z), -l * s - np.log(Z)
    ts = np.linspace(1.01, 6, 500); t = ts[np.argmax([ll_pl(x)[0] for x in ts])]
    ls = np.linspace(1e-3, 3, 600); l = ls[np.argmax([ll_ex(x)[0] for x in ls])]
    d = ll_pl(t)[1] - ll_ex(l)[1]; R = d.sum(); sd = d.std(ddof=1)
    from math import erfc, sqrt
    z = R / (sd * np.sqrt(n)) if sd > 0 else 0.0; p = erfc(abs(z) / sqrt(2))
    return dict(n=n, tau=round(float(t), 3), R=round(float(R), 3), z=round(float(z), 3), p=round(float(p), 4),
                decadas=round(float(np.log10(s.max() / 2)), 3), s_max=int(s.max()))

# ── main ───────────────────────────────────────────────────────────────────
t0 = time.time(); rng = np.random.default_rng(SEED)
sha = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
res = dict(repo_commit=sha, seed=SEED, n_nulos=N_NULOS, n_ordenes=N_ORD, bonferroni_alpha=0.05 / 16,
           python=sys.version.split()[0], numpy=np.__version__, networkx=nx.__version__,
           platform=platform.platform(), donde="contenedor Cowork",
           variables_no_consideradas="todas las que no están en este log (delamor)", W={})
for nombre, W in [("W_viejo", W_viejo()), ("W_nuevo", W_nuevo())]:
    N = len(W); iu = np.triu_indices(N, 1); pos = W[iu][W[iu] > 0]
    r = dict(N=N, media=float(W[iu].mean()), max=float(W.max()), densidad=float((W[iu] > 0).mean()))
    A, nc = area_lazo(W, rng); r["P1"] = dict(A_real=A, no_conv=nc)
    for nn, f in [("N_perm", nulo_perm), ("N_grado", nulo_grado)]:
        Ns = np.array([area_lazo(f(W, rng), rng)[0] for _ in range(N_NULOS)])
        r["P1"][nn] = dict(media=float(Ns.mean()), p5=float(np.percentile(Ns, 5)), p95=float(np.percentile(Ns, 95)),
                           max=float(Ns.max()), p=float(((Ns >= A).sum() + 1) / (N_NULOS + 1)))
    r["P2"], r["P3"] = {}, {}
    for q in (0.3, 0.5, 0.7):
        th = float(np.quantile(pos, q)); c = cascadas(W, th)
        r["P2"][f"q{q}"] = dict(theta=th, core=c["core"], **ajuste(c["tam"], N))
        d_real = float(np.mean(c["rem"]) - np.mean(c["add"])) if c["rem"] else None
        rec_real = float(np.mean(c["recup"])) if c["recup"] else None
        Nd, Nr = [], []
        for _ in range(N_NULOS):
            cn = cascadas(nulo_perm(W, rng), th)
            if cn["rem"]: Nd.append(np.mean(cn["rem"]) - np.mean(cn["add"])); Nr.append(np.mean(cn["recup"]))
        Nd, Nr = np.array(Nd), np.array(Nr)
        r["P3"][f"q{q}"] = dict(theta=th, core=c["core"], rem_medio=float(np.mean(c["rem"])) if c["rem"] else None,
            add_medio=float(np.mean(c["add"])) if c["add"] else None, dif_real=d_real, recup_real=rec_real,
            nulo_dif_media=float(Nd.mean()) if len(Nd) else None,
            p_dif=float(((Nd >= d_real).sum() + 1) / (len(Nd) + 1)) if len(Nd) and d_real is not None else None,
            nulo_recup_media=float(Nr.mean()) if len(Nr) else None,
            p_recup_menor=float(((Nr <= rec_real).sum() + 1) / (len(Nr) + 1)) if len(Nr) and rec_real is not None else None)
    res["W"][nombre] = r
    print(nombre, json.dumps(r, indent=1, ensure_ascii=False), flush=True)
res["P4"] = "NO MEDIBLE — sin W_mixta de un corpus con tensión estructural por diseño en este entorno"
res["segundos"] = round(time.time() - t0, 1)
json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
