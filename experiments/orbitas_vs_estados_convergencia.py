"""
orbitas_vs_estados_convergencia.py — ¿contar órbitas requiere menos runs que
contar estados terminales?

Afirmación a verificar (delamor, sep 2026): con relax orbital, D_ckm estima L
contando órbitas; no converge, pero **requiere menos runs que el conteo de
estados**. Y: ~70% de las trayectorias terminan en ciclos de período 2.

Qué hace:

1. **Verdad de terreno exacta** por mapa sucesor sobre los 2^N estados (N ≤ 20).
   El mapa síncrono es determinista y cada estado tiene un único sucesor, así
   que el espacio es un grafo funcional: se resuelve por iteración, sin
   simular trayectoria por trayectoria. Da órbitas reales, |L| real,
   distribución de períodos y masas de cuenca exactas bajo medida uniforme.

2. **Terminal exacto por estado**, con la misma regla que `relax()`:
   idx = cola + ((max_iter − cola) mod período). Permite la verdad de terreno
   del conteo de ESTADOS, que es la cantidad contra la que se compara.

3. **Curvas de cobertura** vs n_runs, con el muestreo del instrumento
   (`sample_s0`: banda 30–70% de activación), para órbitas y para terminales.
   La pregunta se responde comparando cuántos runs necesita cada uno para
   alcanzar el mismo porcentaje de su propia verdad de terreno.

4. **Verificación de `relax_orbit`** contra el mapa exhaustivo: mismo estado
   terminal y misma órbita, sobre una muestra.

No decide nada sobre el modelo. Mide.
"""

from __future__ import annotations

import argparse
import ast
import glob
import hashlib
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))

from corpus_service import CorpusService          # noqa: E402
from landscape_engine import relax_orbit, sample_s0, n_eff  # noqa: E402

MAX_ITER_DEFECTO = 200
N_RUNS_GRILLA = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 30000]


# ── corpus ──────────────────────────────────────────────────────────────────

def _warmup():
    # encoding explícito: en Windows read_text() usa cp1252 y los corpus IAP
    # tienen UTF-8. Los drivers del repo lo omiten porque corren en Codespace.
    src = (REPO / "iap_chatroom/tests/test_armstrong_stop_coco.py").read_text(
        encoding="utf-8")
    for nodo in ast.parse(src).body:
        if isinstance(nodo, ast.Assign) and getattr(nodo.targets[0], "id", "") == "WARMUP_TEXTS":
            return ast.literal_eval(nodo.value)
    return []


def corpus_disponibles(min_textos=12):
    vistos, out = set(), []
    for f in sorted(glob.glob(str(REPO / "process/iap/corpus_state.json.bak_*"))):
        try:
            textos = json.loads(
                Path(f).read_text(encoding="utf-8")).get("texts", [])
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            continue
        h = hashlib.sha256("\n".join(textos).encode()).hexdigest()
        if len(textos) >= min_textos and h not in vistos:
            vistos.add(h)
            out.append((Path(f).name.split("_", 2)[-1], textos))
    w = _warmup()
    if w:
        out.append(("WARMUP_TEXTS", w))
    return out


def construir_W(textos, k, top_k, force_w_pos=False):
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"),
                      min_texts=k, top_k=top_k, force_w_pos=force_w_pos)
    c.ingest(textos[:k])
    return c.get_W()


# ── verdad de terreno: grafo funcional sobre 2^N ────────────────────────────

def mapa_sucesor(W: np.ndarray, chunk: int = 1 << 16) -> np.ndarray:
    """
    succ[i] = índice del estado siguiente de i bajo el paso síncrono.

    Estado i: bit b del entero i es el nodo b; bit 1 → σ=+1, bit 0 → σ=−1.
    Regla de empate GOLES: h == 0 conserva σ (igual que relax_orbit).
    """
    N = len(W)
    total = 1 << N
    succ = np.empty(total, dtype=np.int64)
    bits = (1 << np.arange(N, dtype=np.int64))
    for ini in range(0, total, chunk):
        fin = min(ini + chunk, total)
        idx = np.arange(ini, fin, dtype=np.int64)[:, None]
        S = np.where((idx & bits) > 0, 1.0, -1.0)      # (m, N) en ±1
        H = S @ W.T
        S2 = np.where(H > 0, 1.0, np.where(H < 0, -1.0, S))
        succ[ini:fin] = (((S2 > 0).astype(np.int64)) * bits).sum(axis=1)
    return succ


def ciclos_y_colas(succ: np.ndarray):
    """
    Grafo funcional: cada nodo tiene un sucesor. Devuelve
      cid   — id de órbita por estado (int32)
      cola  — pasos hasta entrar en la órbita
      orbes — lista de arrays con los estados de cada órbita, en orden de
              recorrido (para poder elegir la fase)
    Iterativo, sin recursión: marca por color de visita.
    """
    total = len(succ)
    cid = np.full(total, -1, dtype=np.int64)
    cola = np.full(total, -1, dtype=np.int64)
    estado = np.zeros(total, dtype=np.int8)   # 0 sin ver, 1 en camino, 2 hecho
    orbes: list = []

    for inicio in range(total):
        if estado[inicio]:
            continue
        camino = []
        x = inicio
        while estado[x] == 0:
            estado[x] = 1
            camino.append(x)
            x = succ[x]
        if estado[x] == 1:                      # cerró una órbita nueva
            corte = camino.index(x)
            ciclo = camino[corte:]
            k = len(orbes)
            orbes.append(np.array(ciclo, dtype=np.int64))
            for s in ciclo:
                cid[s], cola[s] = k, 0
            resto = camino[:corte]
            for j, s in enumerate(resto):
                cid[s], cola[s] = k, len(resto) - j
        else:                                   # llegó a algo ya resuelto
            base_cid, base_cola = cid[x], cola[x]
            for j, s in enumerate(camino):
                cid[s] = base_cid
                cola[s] = base_cola + (len(camino) - j)
        for s in camino:
            estado[s] = 2
    return cid, cola, orbes


def verdad_de_terreno(W, max_iter):
    N = len(W)
    t0 = time.time()
    succ = mapa_sucesor(W)
    t_succ = time.time() - t0

    t0 = time.time()
    cid, cola, orbes = ciclos_y_colas(succ)
    t_ciclos = time.time() - t0

    total = 1 << N
    periodos = np.array([len(o) for o in orbes], dtype=np.int64)
    masas = np.bincount(cid, minlength=len(orbes)).astype(float) / total

    # terminal exacto: avanzar cada estado `cola` pasos da la entrada al ciclo;
    # después aplicar la fase de relax(). Se hace por niveles de cola.
    entrada = np.arange(total, dtype=np.int64)
    max_cola = int(cola.max())
    pend = cola.copy()
    for _ in range(max_cola):
        mov = pend > 0
        if not mov.any():
            break
        entrada[mov] = succ[entrada[mov]]
        pend[mov] -= 1

    # índice de la entrada dentro de su órbita
    idx_en_orbita = np.zeros(total, dtype=np.int64)
    for k, orb in enumerate(orbes):
        pos = {int(s): i for i, s in enumerate(orb)}
        sel = np.flatnonzero(cid == k)
        idx_en_orbita[sel] = [pos[int(e)] for e in entrada[sel]]

    per_de = periodos[cid]
    avance = (max_iter - cola) % per_de
    fase = (idx_en_orbita + avance) % per_de
    term = np.empty(total, dtype=np.int64)
    for k, orb in enumerate(orbes):
        sel = np.flatnonzero(cid == k)
        term[sel] = orb[fase[sel]]

    return {
        "N": N, "total": total,
        "orbitas": len(orbes),
        "L": int(periodos.sum()),
        "terminales": int(np.unique(term).size),
        "frac_periodo2_estados": float((per_de == 2).mean()),
        "frac_periodo2_orbitas": float((periodos == 2).mean()),
        "masa_periodo2": float(masas[periodos == 2].sum()),
        "N_eff_exacto": float(n_eff(masas)),
        "masa_max": float(masas.max()),
        "t_succ_s": round(t_succ, 2),
        "t_ciclos_s": round(t_ciclos, 2),
        "_cid": cid, "_term": term, "_masas": masas,
    }


# ── muestreo: cobertura vs n_runs ───────────────────────────────────────────

def curva_cobertura(W, gt, n_runs_max, seed, max_iter):
    """Conteo acumulado de órbitas y de terminales distintos, por n_runs."""
    N = len(W)
    rng = np.random.default_rng(seed)
    vistos_orb, vistos_term = set(), set()
    filas, hitos = [], set(N_RUNS_GRILLA)
    n_orbita_p2 = 0
    for r in range(1, n_runs_max + 1):
        s0 = sample_s0(rng, N, None)
        orb, per, _cola, est = relax_orbit(s0, W, max_iter)
        vistos_orb.add(orb)
        vistos_term.add(est.tobytes())
        if per == 2:
            n_orbita_p2 += 1
        if r in hitos:
            filas.append({
                "n_runs": r,
                "orbitas": len(vistos_orb),
                "terminales": len(vistos_term),
                "cob_orb": len(vistos_orb) / gt["orbitas"],
                "cob_term": len(vistos_term) / gt["terminales"],
                "frac_p2_muestreo": n_orbita_p2 / r,
            })
    return filas


def runs_para(filas, clave, objetivo):
    for f in filas:
        if f[clave] >= objetivo:
            return f["n_runs"]
    return None


# ── verificación de relax_orbit contra el mapa exhaustivo ───────────────────

def verificar_relax(W, gt, succ_term, n=300, seed=0):
    N = len(W)
    rng = np.random.default_rng(seed)
    bits = (1 << np.arange(N, dtype=np.int64))
    ok = 0
    for _ in range(n):
        s0 = sample_s0(rng, N, None)
        i0 = int((((s0 > 0).astype(np.int64)) * bits).sum())
        _orb, _per, _cola, est = relax_orbit(s0, W, MAX_ITER_DEFECTO)
        i_term = int((((est > 0).astype(np.int64)) * bits).sum())
        ok += int(i_term == int(succ_term[i0]))
    return ok, n


# ── main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="caso09", help="subcadena del nombre")
    ap.add_argument("--k", type=int, default=24, help="textos a ingerir")
    ap.add_argument("--top-k", type=int, default=20, help="top_k → N")
    ap.add_argument("--n-runs", type=int, default=30000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-iter", type=int, default=MAX_ITER_DEFECTO)
    ap.add_argument("--force-w-pos", action="store_true")
    a = ap.parse_args()

    disponibles = corpus_disponibles()
    elegidos = [(n, t) for n, t in disponibles if a.corpus.lower() in n.lower()]
    if not elegidos:
        print(f"sin corpus que matcheen {a.corpus!r}. Disponibles:")
        for n, t in disponibles:
            print(f"  {n}  ({len(t)} textos)")
        return
    nombre, textos = elegidos[0]

    W = construir_W(textos, min(a.k, len(textos)), a.top_k, a.force_w_pos)
    if W is None:
        print("corpus en acumulación — el dato no distingue con ese k/top_k")
        return
    N = len(W)
    if N > 22:
        print(f"N={N} — 2^{N} es demasiado para enumerar. Bajá --top-k.")
        return

    print(f"corpus={nombre}  k={min(a.k, len(textos))}  N={N}  "
          f"negativos={int((W < 0).sum()) // 2}  "
          f"aislados={int((~W.any(axis=1)).sum())}  "
          f"force_w_pos={a.force_w_pos}")
    print(f"enumerando 2^{N} = {1 << N} estados...")

    gt = verdad_de_terreno(W, a.max_iter)
    print(f"\n=== VERDAD DE TERRENO (exacta, {gt['t_succ_s']}s + {gt['t_ciclos_s']}s) ===")
    print(f"  órbitas reales      : {gt['orbitas']}")
    print(f"  |L| (estados)       : {gt['L']}")
    print(f"  terminales distintos: {gt['terminales']}   ← lo que cuenta _count_attractors")
    print(f"  N_eff exacto        : {gt['N_eff_exacto']:.3f}")
    print(f"  masa de cuenca máx  : {gt['masa_max']:.4f}")
    print(f"  período 2 — órbitas : {gt['frac_periodo2_orbitas']:.1%}")
    print(f"  período 2 — estados : {gt['frac_periodo2_estados']:.1%}  ← trayectorias sobre TODO el espacio")
    print(f"  período 2 — masa    : {gt['masa_periodo2']:.1%}")

    ok, n = verificar_relax(W, gt, gt["_term"], n=300, seed=a.seed + 77)
    print(f"\n=== relax_orbit contra mapa exhaustivo === {ok}/{n} terminales idénticos")

    print(f"\n=== COBERTURA vs n_runs (muestreo del instrumento, seed={a.seed}) ===")
    filas = curva_cobertura(W, gt, a.n_runs, a.seed, a.max_iter)
    print(f"{'n_runs':>7} {'órbitas':>8} {'cob':>7} {'terminales':>11} {'cob':>7} {'p2 muestreo':>12}")
    for f in filas:
        print(f"{f['n_runs']:>7} {f['orbitas']:>8} {f['cob_orb']:>6.1%} "
              f"{f['terminales']:>11} {f['cob_term']:>6.1%} {f['frac_p2_muestreo']:>11.1%}")

    print("\n=== RUNS NECESARIOS PARA CUBRIR ===")
    print(f"{'objetivo':>9} {'órbitas':>9} {'terminales':>11}")
    for obj in (0.50, 0.80, 0.90, 0.95):
        ro = runs_para(filas, "cob_orb", obj)
        rt = runs_para(filas, "cob_term", obj)
        print(f"{obj:>8.0%} {str(ro):>9} {str(rt):>11}")

    ult = filas[-1]
    print(f"\nA n_runs={ult['n_runs']}: órbitas {ult['cob_orb']:.1%} de {gt['orbitas']}, "
          f"terminales {ult['cob_term']:.1%} de {gt['terminales']}.")


if __name__ == "__main__":
    main()
