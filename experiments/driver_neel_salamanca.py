"""
driver_neel_salamanca.py — ¿existe la frontera, y qué sucede entre T0 y T1?

TASK_neel_separabilidad_v1. Dos pasos, en orden.

  Paso 1 — SALAMANCA: ¿existen T0/T1 en W_pos? Corte espectral (normalized
  cut, sin semilla) contra un ensemble nulo: el mismo corpus barajado
  palabra por palabra, con W reconstruida por los servicios reales. Conserva
  frecuencias y largos de texto, destruye la co-ocurrencia.

      "Lo que natura non da, SALAMANCA non presta" — y no se fía.
      (delamor: el cartel a mano en el almacén de Don Basilio Salamanca,
      Cipolletti, Río Negro.)

  Paso 2 — Néel: barrido de β sobre W_pos con la partición del paso 1 FIJA.
  Reajustarla en cada β es reajustarla al ruido: S sobre la mejor partición
  es un máximo sobre particiones, y da > 0 aun con spins independientes
  (0.030 con 200 muestras, 0.014 con 1000, 0.005 con 5000).

Qué se guarda (delamor: qué sucede entre ellos): C_ij(β) POR PAR CRUZANTE,
no sólo la media. Los pares no sueltan todos juntos — cada uno tiene su
β_Néel, y la frontera es un perfil, no una línea. El promedio se deriva al
leer, como el registro de borde de REG_seleccion_nodos.

Pre-registro (declarado antes de correr, para que el criterio pueda fallar):
  caso09 (debate, dos posiciones por diseño) -> T0/T1 existen
  informes CKM (autor único)                -> no existen
  canal IAP caso13/caso14 (coordinación)     -> no existen

Uso:
    python experiments/driver_neel_salamanca.py [--corpus caso09] [--nulos 20]
    python experiments/driver_neel_salamanca.py --todos
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))
sys.path.insert(0, str(REPO / "experiments"))
from corpus_service import CorpusService                      # noqa: E402
from landscape_engine import boltzmann_warmup, beta_c_landscape, sample_s0  # noqa: E402


# ── corpus ──────────────────────────────────────────────────────────────────

def corpus(nombre: str) -> list:
    iap = {"caso09": "1784685610_caso09_run2", "caso13": "1785135692_caso13",
           "caso14": "1785214255_caso14_run2"}
    if nombre in iap:
        p = REPO / f"process/iap/corpus_state.json.bak_{iap[nombre]}"
        return json.loads(p.read_text())["texts"] if p.exists() else []
    if nombre == "informes_version":
        from driver_unidad_texto import por_version
        return por_version()
    if nombre == "informes_pagina300":
        p = REPO / "process/corpus_informes/corpus_informes_paginas300.txt"
        return [l.strip() for l in p.read_text(encoding="utf8").splitlines() if l.strip()]
    raise ValueError(nombre)


def barajar(textos: list, seed: int) -> list:
    """Nulo: mismas palabras, mismos largos, co-ocurrencia destruida."""
    rng = np.random.default_rng(seed)
    pool = [w for t in textos for w in t.split()]
    rng.shuffle(pool)
    out, i = [], 0
    for t in textos:
        n = len(t.split())
        out.append(" ".join(pool[i:i + n])); i += n
    return out


def W_pos(textos: list, top_k: int) -> tuple:
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"), min_texts=len(textos),
                      top_k=top_k, rebuild_suspendido=True, force_w_pos=True)
    c.ingest(textos)
    return c.get_W(), c.get_nodes()


# ── paso 1 — SALAMANCA ──────────────────────────────────────────────────────

def particion_espectral(W: np.ndarray) -> tuple:
    """Fiedler del laplaciano normalizado. Devuelve (mascara_T0, ncut)."""
    A = np.abs(W).copy()
    np.fill_diagonal(A, 0.0)
    d = A.sum(axis=1)
    if (d <= 0).any() or len(A) < 4:
        return None, None
    dm = 1.0 / np.sqrt(d)
    L = np.eye(len(A)) - (dm[:, None] * A * dm[None, :])
    w, v = np.linalg.eigh(L)
    f = v[:, 1] * dm                       # Fiedler, des-normalizado
    g = f > np.median(f)                   # mediana: parte en dos mitades
    if g.all() or (~g).all():
        return None, None
    return g, ncut(A, g)


def ncut(A: np.ndarray, g: np.ndarray) -> float:
    cut = A[np.ix_(g, ~g)].sum()
    vol0, vol1 = A[g].sum(), A[~g].sum()
    if vol0 <= 0 or vol1 <= 0:
        return float("inf")
    return float(cut * (1.0 / vol0 + 1.0 / vol1))


def salamanca(textos: list, top_k: int, n_nulos: int, seed: int) -> dict:
    W, nodos = W_pos(textos, top_k)
    g, obs = particion_espectral(W)
    nulos = []
    for s in range(n_nulos):
        Wn, _ = W_pos(barajar(textos, seed + s), top_k)
        _, n = particion_espectral(Wn)
        if n is not None:
            nulos.append(n)
    nulos = np.array(nulos)
    # el ncut observado tiene que ser MENOR que el nulo: corte mas barato
    p = float((nulos <= obs).mean()) if len(nulos) else float("nan")
    return {"W": W, "nodos": nodos, "T0": g, "ncut": obs,
            "nulo_med": float(nulos.mean()) if len(nulos) else float("nan"),
            "nulo_p10": float(np.percentile(nulos, 10)) if len(nulos) else float("nan"),
            "p": p, "existe": bool(len(nulos) and p < 0.05)}


# ── paso 2 — Néel ───────────────────────────────────────────────────────────

def correlaciones(W: np.ndarray, beta: float, n_muestras: int,
                  n_warmup: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    N = W.shape[0]
    S = np.empty((n_muestras, N))
    for m in range(n_muestras):
        S[m] = boltzmann_warmup(rng, sample_s0(rng, N, None), W, beta, n_warmup)
    C = np.corrcoef(S.T)
    return np.nan_to_num(C)


def neel(W: np.ndarray, g: np.ndarray, *, n_betas=15, n_muestras=200,
         n_warmup=400, seed=0) -> tuple:
    bc = beta_c_landscape(W) or 1.0
    betas = np.geomspace(bc * 8, bc / 8, n_betas)      # frío -> caliente
    ii, jj = np.triu_indices(W.shape[0], 1)
    cruza = g[ii] != g[jj]
    curva, por_par = [], []
    for b in betas:
        C = correlaciones(W, float(b), n_muestras, n_warmup, seed)
        u = C[ii, jj]
        curva.append({"beta": float(b),
                      "C_interno": float(u[~cruza].mean()),
                      "C_cruzado": float(u[cruza].mean()),
                      "S": float(u[~cruza].mean() - u[cruza].mean())})
        por_par.append(u[cruza].copy())
    return betas, curva, np.array(por_par), (ii[cruza], jj[cruza])


# ── ejecución ───────────────────────────────────────────────────────────────

CORPORA = ["caso09", "caso13", "caso14", "informes_version", "informes_pagina300"]
ESPERADO = {"caso09": "existe", "caso13": "no", "caso14": "no",
            "informes_version": "no", "informes_pagina300": "no"}


def correr(nombre: str, top_k: int, n_nulos: int, seed: int, con_neel: bool):
    textos = corpus(nombre)
    if not textos:
        print(f"{nombre}: corpus no disponible"); return
    r = salamanca(textos, top_k, n_nulos, seed)
    veredicto = "EXISTEN" if r["existe"] else "no existen"
    ok = "✓" if (r["existe"] == (ESPERADO[nombre] == "existe")) else "✗ CONTRA EL PRE-REGISTRO"
    print(f"\n=== {nombre} ({len(textos)} textos, N={len(r['nodos'])})")
    print(f"  ncut observado {r['ncut']:.4f} | nulo med {r['nulo_med']:.4f} "
          f"p10 {r['nulo_p10']:.4f} | p={r['p']:.3f}")
    print(f"  SALAMANCA: T0/T1 {veredicto}   [esperado: {ESPERADO[nombre]}]  {ok}")
    if r["existe"]:
        g = r["T0"]; nodos = r["nodos"]
        print(f"  T0 ({int(g.sum())}): {', '.join(np.array(nodos)[g][:10])}")
        print(f"  T1 ({int((~g).sum())}): {', '.join(np.array(nodos)[~g][:10])}")
    if not (con_neel and r["existe"]):
        return
    betas, curva, por_par, (pi, pj) = neel(r["W"], r["T0"], seed=seed)
    print("  Néel — barrido de β (frío → caliente):")
    for c in curva:
        print(f"    β {c['beta']:8.4f}  interno {c['C_interno']:+.3f}  "
              f"cruzado {c['C_cruzado']:+.3f}  S {c['S']:+.3f}")
    # β_Néel por par: primer β (de frío a caliente) donde el par pierde correlación
    nodos = np.array(r["nodos"])
    print("  pares cruzantes que más resisten (β donde |C| cae bajo 0.1):")
    resist = []
    for k in range(por_par.shape[1]):
        col = np.abs(por_par[:, k])
        idx = np.argmax(col < 0.1) if (col < 0.1).any() else len(col) - 1
        resist.append((idx, float(betas[idx]), nodos[pi[k]], nodos[pj[k]]))
    for idx, b, a, c in sorted(resist)[-8:][::-1]:
        print(f"    {a} — {c}: suelta en β {b:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="caso09")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--top-k", type=int, default=32)
    ap.add_argument("--nulos", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sin-neel", action="store_true")
    ap.add_argument("--periodos", action="store_true", help="F1: distribucion de periodos")
    ap.add_argument("--adaptador", action="store_true", help="F2: adaptador y control")
    ap.add_argument("--salamanca", action="store_true", help="S1: SALAMANCA desde W")
    ap.add_argument("--solo", help="corpus separados por coma")
    a = ap.parse_args()
    if a.periodos:
        paso_F1(a.top_k)
        return
    if a.adaptador:
        paso_F2(a.top_k)
        return
    if a.salamanca:
        paso_S1(a.top_k, a.nulos, solo=(a.solo.split(",") if a.solo else None))
        return
    for nom in (CORPORA if a.todos else [a.corpus]):
        correr(nom, a.top_k, a.nulos, a.seed, not a.sin_neel)



# ── F1 — distribucion de periodos (TASK_representacion_atractores_adaptador) ──
# Antes de elegir la representacion que entra a cluster_nodes: medir. Con
# GOLES el periodo es 1 o 2, nunca mas (DEFS §4.2). Si no hay periodo 2, el
# conjunto de nodos activos NO pierde nada y el peso es discutible sobre un
# caso que no existe.

def periodos(W: np.ndarray, *, n_runs=1000, seed=0) -> dict:
    """Orbitas alcanzadas desde n_runs sigma_0 uniformes, con su periodo y
    su masa de cuenca. Consume el RNG igual que count_attractors/mean_cS."""
    from landscape_engine import relax_orbit, sample_s0
    rng = np.random.default_rng(seed)
    N = W.shape[0]
    cuenta: dict = {}
    per: dict = {}
    for _ in range(n_runs):
        orb, p, _, _ = relax_orbit(sample_s0(rng, N, None), W)
        cuenta[orb] = cuenta.get(orb, 0) + 1
        per[orb] = p
    total = sum(cuenta.values())
    masa_p2 = sum(c for o, c in cuenta.items() if per[o] > 1) / total
    return {"orbitas": len(cuenta),
            "p1": sum(1 for o in cuenta if per[o] == 1),
            "p2": sum(1 for o in cuenta if per[o] == 2),
            "p_mayor": sum(1 for o in cuenta if per[o] > 2),
            "masa_en_p2": masa_p2,
            "cuenta": cuenta, "periodo": per}


def paso_F1(top_k=32, n_runs=1000, seeds=(0, 1, 2)):
    print(f"F1 — distribucion de periodos (W_pos, top_k {top_k}, n_runs {n_runs})\n")
    print(f'{"corpus":22s} {"N":>3} {"seed":>5} {"orbitas":>8} {"p=1":>5} {"p=2":>5} '
          f'{"p>2":>5} {"masa en p2":>11}')
    for nom in CORPORA + ["categorias"]:
        if nom == "categorias":
            import json as _json
            priv = REPO / "process/replay/_private/tramo_categorias_originales.json"
            if not priv.exists():
                continue
            T = [t["texto"] for t in _json.loads(priv.read_text(encoding="utf8"))]
        else:
            T = corpus(nom)
        if not T:
            continue
        W, nodos = W_pos(T, top_k)
        if W is None:
            print(f"{nom:22s} — sin W")
            continue
        for s in seeds:
            r = periodos(W, n_runs=n_runs, seed=s)
            print(f"{nom:22s} {len(nodos):3d} {s:5d} {r['orbitas']:8d} {r['p1']:5d} "
                  f"{r['p2']:5d} {r['p_mayor']:5d} {r['masa_en_p2']:10.3f}")

# ── F2 — adaptador de representacion de atractores ──────────────────────────
# TASK_representacion_atractores_adaptador_v1. cluster_nodes/copresence_matrix
# esperan dict[frozenset(nodos activos), int]; relax_orbit devuelve frozenset
# de ESTADOS completos en bytes. Misma forma, contenido distinto.
#
# Eleccion (Code, Opus 5): (b) CON PESO, masa de la orbita repartida entre sus
# estados. Motivo medido: copresence_matrix descarta el int que recibe (una
# fila por clave), asi que una orbita del 0.1% de masa pesa igual que una del
# 50%. En caso09/informes el 99.9% de la masa esta en dos orbitas (todo en +1
# y todo en -1) y las de periodo 2 ocurren 1 vez en 1000.
# El reparto entre estados: una orbita es UNA cuenca con UNA masa, y el
# sistema alterna entre sus estados. Media cada uno.

def atractores_para_clusters(W: np.ndarray, *, n_runs=1000, seed=0,
                             pesado=True) -> dict:
    """{frozenset(indices en +1): peso}. pesado=False reproduce el trato
    actual de copresence_matrix (toda clave vale 1)."""
    r = periodos(W, n_runs=n_runs, seed=seed)
    out: dict = {}
    for orb, c in r["cuenta"].items():
        estados = sorted(orb)
        peso = (c / len(estados)) if pesado else 1.0
        for b in estados:
            e = np.frombuffer(b, dtype=np.float64)
            k = frozenset(int(i) for i in np.nonzero(e > 0)[0])
            out[k] = out.get(k, 0.0) + peso
    return out


def copresencia_pesada(claves: dict, N: int) -> np.ndarray:
    """Pearson de co-presencia con peso por clave. Con pesos uniformes tiene
    que dar exactamente analytics.copresence_matrix (verificado en F2)."""
    ks = list(claves.keys())
    X = np.zeros((len(ks), N))
    for idx, k in enumerate(ks):
        for i in k:
            if i < N:
                X[idx, i] = 1.0
    w = np.array([claves[k] for k in ks], dtype=float)
    w = w / w.sum()
    mu = w @ X
    Xc = X - mu
    cov = (Xc * w[:, None]).T @ Xc
    sd = np.sqrt(np.diag(cov))
    den = np.outer(sd, sd)
    with np.errstate(invalid="ignore", divide="ignore"):
        corr = np.where(den > 0, cov / den, 0.0)
    return np.nan_to_num(corr, nan=0.0)


def paso_F2(top_k=32, n_runs=1000, seed=0):
    sys.path.insert(0, str(REPO / "services"))
    from analytics import copresence_matrix
    print(f"F2 — adaptador (top_k {top_k}, n_runs {n_runs}, seed {seed})\n")
    print("control de impacto cero: pesos uniformes vs analytics.copresence_matrix")
    for nom in CORPORA:
        T = corpus(nom)
        if not T:
            continue
        W, nodos = W_pos(T, top_k)
        N = len(nodos)
        sin = atractores_para_clusters(W, n_runs=n_runs, seed=seed, pesado=False)
        mia = copresencia_pesada(sin, N)
        suya = copresence_matrix({k: int(v) for k, v in sin.items()}, N)
        d = float(np.abs(mia - suya).max())
        con = atractores_para_clusters(W, n_runs=n_runs, seed=seed, pesado=True)
        mc = copresencia_pesada(con, N)
        ii, jj = np.triu_indices(N, 1)
        print(f"  {nom:20s} claves {len(sin):3d} · max|dif| vs analytics {d:.2e} · "
              f"corr media sin peso {mia[ii, jj].mean():+.3f} · con peso {mc[ii, jj].mean():+.3f} "
              f"· pares con corr>0.999 con peso: {int((mc[ii, jj] > 0.999).sum())}/{len(ii)}")


# ── S1 — SALAMANCA desde W (TASK_salamanca_neel_coercividad_v4 §13-§14) ──────
# Metodo declarado ANTES de correr, en la TASK. El nulo vuelve a particionar
# cada W barajada con el mismo metodo y el mismo k: reusar la particion
# observada mediria la particion, no la estructura.

K_RANGO   = range(2, 9)
N_NULOS   = 20
SAT_MAX   = 0.98     # (a) W saturada: sin ceros no hay corte barato
COLA_MAX  = 3.0      # (b) nulo inestable: p90 > 3 * mediana
P_CORTE   = 0.05
# Correccion por comparaciones multiples: se prueban 7 valores de k por
# corpus, asi que el umbral por k es 0.05/7. Con n barajados la resolucion
# de p es 1/n: con 100 no se puede resolver 0.0071 y hace falta n=1000.
N_K       = 7
P_BONF    = P_CORTE / N_K


def particion_k(W: np.ndarray, k: int, seed: int = 0):
    """Espectral: k primeros autovectores del laplaciano normalizado, filas
    normalizadas, k-means determinista. None si algun nodo tiene grado 0."""
    A = np.abs(W).copy()
    np.fill_diagonal(A, 0.0)
    d = A.sum(axis=1)
    if (d <= 0).any() or len(A) < k:
        return None
    dm = 1.0 / np.sqrt(d)
    L = np.eye(len(A)) - (dm[:, None] * A * dm[None, :])
    _, v = np.linalg.eigh(L)
    X = v[:, :k]
    nrm = np.linalg.norm(X, axis=1, keepdims=True)
    X = X / np.where(nrm > 0, nrm, 1.0)
    rng = np.random.default_rng(seed)
    cen = X[rng.choice(len(X), k, replace=False)].copy()
    lab = np.zeros(len(X), dtype=int)
    for _ in range(100):
        lab = np.argmin(((X[:, None, :] - cen[None]) ** 2).sum(-1), axis=1)
        nue = np.array([X[lab == c].mean(0) if (lab == c).any() else cen[c]
                        for c in range(k)])
        if np.allclose(nue, cen):
            break
        cen = nue
    return lab


# POST-HOC, declarado: el corte de 8 pares se fijo DESPUES de ver el dato
# (las candidatas de caso09 k=3 tenian 60-160 pares cruzando; los casos que
# explotaban, 6-32). Elegir un umbral mirando el resultado es lo que este
# trabajo viene evitando, asi que no se adopta a ciegas: se reporta la
# sensibilidad en 4, 8 y 16, y si el veredicto no cambia, la guarda no esta
# decidiendo nada.
GUARDAS_PARES = (4, 8, 16)


def coercitividades(W: np.ndarray, nodos: list, k: int, seed: int = 0):
    """Devuelve (vals, chicos, opos, separados).

    vals = [(porosidad, coercitividad, clave, n_pares_inter)]. Se compara la POROSIDAD
    (inter / min(intra)), que es finita siempre; la coercitividad es su
    inverso y explota cuando inter -> 0, rompiendo los percentiles del nulo.
    El orden se conserva: menos poroso = mas coercitivo.
    Excluidos: cluster de 1 nodo (intra = 0, se lee porosa por el servicio),
    inter < 0 ("oposicion", otro regimen), inter = 0 (separados: resistencia
    maxima, se cuentan aparte), y inter sobre menos de MIN_PARES_INTER pares.
    """
    from cluster_frontier_density import cluster_frontier_density, OPOSICION
    lab = particion_k(W, k, seed)
    if lab is None:
        return None, 0, 0, 0, []
    clusters = {f"C{c+1}": [nodos[i] for i in range(len(nodos)) if lab[i] == c]
                for c in range(k)}
    chicos = {lbl for lbl, ns in clusters.items() if len(ns) < 2}
    r = cluster_frontier_density(clusters, nodos, W)
    tams = sorted(len(ns) for ns in clusters.values())
    vals, opos, sep = [], 0, 0
    for clave, h in r["coercivity"].items():
        a, b = clave.split("|")
        if a in chicos or b in chicos:
            continue
        if h == OPOSICION:
            opos += 1
            continue
        if not np.isfinite(h):
            sep += 1
            continue
        # coercitividad 0 = min(intra) 0: cluster sin peso interno, porosidad
        # maxima. Se conserva con inf: es valido y nunca es el minimo.
        poro = (1.0 / float(h)) if float(h) > 0 else float("inf")
        vals.append((poro, float(h), clave, int(r["n_pairs"][clave])))
    return vals, len(chicos), opos, sep, tams


def paso_S1(top_k=32, n_nulos=100, seed=0, solo=None):
    """SALAMANCA desde W. Estadistico pareado: el nulo es la distribucion del
    MINIMO de porosidad POR BARAJADO, no el pool de todas sus fronteras —
    comparar el minimo observado contra valores individuales del nulo sesga
    hacia FRONTERA."""
    import json as _json
    print(f"S1 — SALAMANCA desde W · k 2..8 · {n_nulos} barajados · seed {seed}")
    print(f"nulo = minimo de porosidad POR barajado (estadistico pareado)")
    print(f"guarda de pares de inter barrida en {GUARDAS_PARES} (post-hoc, declarada)\n")
    for nom in CORPORA + ["categorias"]:
        if solo and nom not in solo:
            continue
        if nom == "categorias":
            priv = REPO / "process/replay/_private/tramo_categorias_originales.json"
            if not priv.exists():
                continue
            T = [t["texto"] for t in _json.loads(priv.read_text(encoding="utf8"))]
        else:
            T = corpus(nom)
        if not T:
            continue
        W, nodos = W_pos(T, top_k)
        if W is None:
            print(f"{nom:20s} NO MEDIBLE — sin W\n")
            continue
        N = len(nodos)
        ii, jj = np.triu_indices(N, 1)
        sat = float((W[ii, jj] != 0).mean())
        print(f"{nom:20s} N {N} · saturación {sat:.3f}")
        if sat >= SAT_MAX:
            print(f"   NO MEDIBLE (a) — saturación {sat:.3f} ≥ {SAT_MAX}\n")
            continue
        Wn = [W_pos(barajar(T, sx), top_k) for sx in range(n_nulos)]
        # coercitividades crudas una sola vez por (W, k); las guardas filtran
        obs_k, nul_k, tam_k, sep_k = {}, {}, {}, {}
        for k in range(2, 9):
            if N < 4 * k:
                continue
            o, chicos, opos, sep, tams = coercitividades(W, nodos, k, seed)
            if not o:
                continue
            obs_k[k], tam_k[k], sep_k[k] = o, tams, sep
            lista = []
            for Wx, nx in Wn:
                if Wx is None:
                    continue
                v, _, _, _, _ = coercitividades(Wx, nx, k, seed)
                if v:
                    lista.append(v)
            nul_k[k] = lista
        if not obs_k:
            print("   => NO MEDIBLE — ningún k con fronteras evaluables\n")
            continue
        for g in GUARDAS_PARES:
            pasaron, nulos_mas_coerc = [], []
            print(f"   guarda ≥{g:2d} pares:", end="")
            lineas = []
            for k in sorted(obs_k):
                o = [x for x in obs_k[k] if x[3] >= g]
                if not o:
                    lineas.append(f"      k={k}: sin fronteras tras la guarda")
                    continue
                nul = [min(x[0] for x in v if x[3] >= g)
                       for v in nul_k[k] if any(x[3] >= g for x in v)]
                if len(nul) < 20:
                    lineas.append(f"      k={k}: nulo con {len(nul)} barajados — no legible")
                    continue
                nul = np.array(nul)
                poro, coerc, clave, npar = min(o)
                cuenta = int((nul <= poro).sum())
                pv = cuenta / len(nul)
                res = 1.0 / len(nul)
                ptxt = f"<{res:.4f}" if cuenta == 0 else f"{pv:.4f}"
                ef = float(np.median(nul)) / poro if poro > 0 else float("inf")
                # criterio (e): el nulo es MAS coercitivo que el observado
                e_flag = float(np.median(nul)) < poro
                nulos_mas_coerc.append(e_flag)
                # con cuenta = 0 lo unico afirmable es p < 1/n: para sostener
                # el umbral corregido hace falta que esa resolucion alcance.
                ok = (pv < P_BONF) and (cuenta > 0 or res <= P_BONF)
                marca = f"FRONTERA {ef:5.2f}x" if ok else ("" if not e_flag else "(e)")
                if ok:
                    pasaron.append(k)
                lineas.append(f"      k={k}: {len(o):2d} front · coerc {coerc:6.2f} ({clave}) "
                              f"· poros {poro:.3f} vs nulo med {np.median(nul):.3f} p10 "
                              f"{np.percentile(nul,10):.3f} · p={ptxt:>7s} · cl.mín {tam_k[k][0]} "
                              f"· sep {sep_k[k]}  {marca}")
            if pasaron:
                print(f" FRONTERA (Bonferroni p<{P_BONF:.4f}) en k={pasaron}")
            elif nulos_mas_coerc and sum(nulos_mas_coerc) > len(nulos_mas_coerc) / 2:
                print(f" NO MEDIBLE (e) — el nulo es más coercitivo que el "
                      f"observado en {sum(nulos_mas_coerc)}/{len(nulos_mas_coerc)} k")
            else:
                print(" NADA")
            for ln in lineas:
                print(ln)
        print()


if __name__ == "__main__":
    main()
