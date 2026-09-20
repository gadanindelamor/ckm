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
    a = ap.parse_args()
    for nom in (CORPORA if a.todos else [a.corpus]):
        correr(nom, a.top_k, a.nulos, a.seed, not a.sin_neel)


if __name__ == "__main__":
    main()
