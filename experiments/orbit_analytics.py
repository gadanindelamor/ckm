"""
orbit_analytics.py — Analitica de orbitas y conjuntos invariantes

Driver que REGENERA todas las mediciones citadas en
registers/REG_orbitas_conjuntos_invariantes_v1.md, mas las de la sesion
posterior sobre fragilidad numerica.

Motivo de existir: ese REG se escribio citando mediciones corridas como
heredocs inline, que no quedaron en ningun archivo. La evidencia emerge al
ejecutar; sin driver no hay con que volver a ejecutar. Este archivo cierra
esa brecha.

Uso:
    python experiments/orbit_analytics.py            # todo
    python experiments/orbit_analytics.py --seccion D  # una seccion

Secciones:
    A  corpus y sus caracteristicas (diadico, densidad, valores)
    B  fragilidad al orden de suma — sincrono y asincrono
    C  W normalizada vs W cruda: orbitas, conjuntos, calibracion
    D  enumeracion exhaustiva 2^N — verdad de terreno (solo N<=22)
    E  muestreo contra verdad: A, top-k, N_eff

Salida: process/experiments/orbitas/<seccion>_<timestamp>.json
No pisa corridas anteriores.

Reproducibilidad: no depende del directorio desde el que se invoca — todas
las rutas se resuelven desde __file__. No usa storage persistente para los
corpus: cada construccion va a tempfile. Es la correccion de los dos
problemas hallados en exp_monitor_trajectory.py (ruta relativa a un insumo
ausente) y en el __main__ de stochastic_attractor_eval.py (storage_path
persistente que duplica el corpus en cada corrida).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "services"))

from corpus_service import CorpusService          # noqa: E402
from node_extractor import NodeExtractorService   # noqa: E402
from coco import COCO, BETA_RHO_STAR              # noqa: E402

OUT_DIR = _REPO / "process/experiments/orbitas"
CASO09  = _REPO / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"
W_V2    = _REPO / "services/W_ckm_corpus_v2.json"
ARMSTRONG = _REPO / "iap_chatroom/tests/test_armstrong_stop_coco.py"


# ── corpus ───────────────────────────────────────────────────────────────────

def _warmup_texts() -> list[str]:
    spec = importlib.util.spec_from_file_location("armstrong", ARMSTRONG)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return list(m.WARMUP_TEXTS)


def _caso09_texts() -> list[str]:
    return json.loads(CASO09.read_text())["texts"]


def _build_W(textos: list[str], force_w_pos: bool = False, min_texts: int = 3):
    """W via CorpusService, siempre sobre storage temporal — nunca persistente."""
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"),
                      min_texts=min_texts, force_w_pos=force_w_pos)
    c.ingest(textos)
    return c.get_W(), c._nodes


def W_cruda(textos: list[str], nodes: list[str],
            force_w_pos: bool = False) -> np.ndarray:
    """
    Conteos ENTEROS previos a la normalizacion de CorpusService.

    Replica `_rebuild` hasta justo antes de `W = raw / max|raw|`:
    pos_counts - neg_counts, con el MISMO ruteo por marcadores de oposicion.
    force_w_pos=True saltea el ruteo, igual que el servicio.

    El ruteo importa: sin el, para el regimen natural esto no devuelve "la
    misma W sin normalizar" sino la W del regimen forzado sin normalizar —
    otra matriz, otro paisaje. La comparacion normalizada/cruda dejaria de
    aislar el redondeo y pasaria a mezclar dos efectos.
    """
    ex  = NodeExtractorService(top_k=len(nodes), ngram_max=2)
    idx = {n: i for i, n in enumerate(nodes)}
    N   = len(nodes)
    pos = np.zeros((N, N))
    neg = np.zeros((N, N))
    for t in textos:
        opp = (not force_w_pos) and CorpusService._has_opposition(t)
        dst = neg if opp else pos
        for (a, b), k in ex.accumulate([t]).get("pairs", {}).items():
            if a in idx and b in idx:
                i, j = idx[a], idx[b]
                dst[i, j] += k
                dst[j, i] += k
    return pos - neg


def corpora() -> dict:
    wt = _warmup_texts()
    tx = _caso09_texts()
    W_warm, _        = _build_W(wt, min_texts=15)
    W_nat,  nodes_n  = _build_W(tx)
    W_forz, nodes_f  = _build_W(tx, force_w_pos=True)
    W_v2 = np.array(json.loads(W_V2.read_text())["W"])
    return {
        "WARMUP":          dict(W=W_warm, textos=wt, nodes=None),
        "caso09 natural":  dict(W=W_nat,  textos=tx, nodes=nodes_n),
        "caso09 forzado":  dict(W=W_forz, textos=tx, nodes=nodes_f),
        "W_ckm_corpus_v2": dict(W=W_v2,   textos=None, nodes=None),
    }


# ── primitivas ───────────────────────────────────────────────────────────────

def es_diadico(W: np.ndarray, bits: int = 20) -> bool:
    """True si todo peso no nulo es exactamente representable en binario.
    Los empates (h==0) solo son exactos si los pesos lo son."""
    v = np.unique(W[W != 0])
    return bool(v.size) and all(float(x * 2 ** bits).is_integer() for x in v)


def relax_orbit(sigma, W, max_iter: int = 200):
    """(orbita, periodo, cola, estado_en_max_iter). Misma implementacion que
    COCO._relax_orbit / MonitorService._relax_orbit."""
    visto: dict = {}
    seq: list = []
    s = sigma
    for t in range(max_iter):
        k = s.tobytes()
        prev = visto.get(k)
        if prev is not None:
            per = t - prev
            idx = prev + ((max_iter - prev) % per)
            return frozenset(a.tobytes() for a in seq[prev:]), per, prev, seq[idx]
        visto[k] = t
        seq.append(s)
        h = W @ s
        s = np.where(h > 0, 1., np.where(h < 0, -1., s))
    return frozenset([s.tobytes()]), 0, -1, s


def sigma0(rng, N, modo="hipercubo", W=None, co=None):
    """hipercubo = uniforme sobre {-1,+1}^N (medida de referencia canonica).
    banda / weighted / boltzmann = los modos de COCO."""
    if modo == "hipercubo":
        return np.where(rng.random(N) < 0.5, 1., -1.)
    probs = co._node_probs(W, modo == "weighted") if modo != "boltzmann" else None
    s = co._sample_s0(rng, probs)
    if modo == "boltzmann":
        beta = co._beta_c_landscape(W)
        if beta is not None:
            s = co._boltzmann_warmup(rng, s, W, beta, co._n_warmup)
    return s


def muestrear(W, n_runs, modo="hipercubo", seed=42):
    """Devuelve (n_orbitas, masas ordenadas desc). Las masas son
    P(sigma_0 cae en esa orbita) bajo la medida `modo`."""
    N  = W.shape[0]
    co = COCO(W=W, n_runs=n_runs, seed=seed)
    rng = np.random.default_rng(seed)
    cu: Counter = Counter()
    for _ in range(n_runs):
        o, _, _, _ = relax_orbit(sigma0(rng, N, modo, W, co), W)
        cu[o] += 1
    tot = sum(cu.values())
    return len(cu), np.array(sorted((v / tot for v in cu.values()), reverse=True))


def n_eff(masas: np.ndarray) -> float:
    """Numero efectivo de orbitas — inverso de Simpson, 1/sum(m^2).
    Se comporta como un conteo pero converge como una masa."""
    return float(1.0 / np.square(masas).sum())


def enumerar_exhaustivo(W: np.ndarray):
    """Enumera los 2^N estados. Verdad de terreno, no estimacion.
    Devuelve (n_orbitas, volumenes ordenados desc, |L|).
    Usa W @ s — el mismo orden de suma que services/_relax."""
    N = W.shape[0]
    if N > 22:
        raise ValueError(f"N={N}: 2^{N} no es enumerable con este metodo")
    M = 1 << N
    pot = 1 << np.arange(N)
    sig = np.empty(M, dtype=np.int64)
    for x in range(M):
        s = np.where((x & pot) > 0, 1., -1.)
        h = W @ s                                  # orden de suma de services
        s2 = np.where(h > 0, 1., np.where(h < 0, -1., s))
        sig[x] = int(((s2 > 0) * pot).sum())
    memo = np.full(M, -1, dtype=np.int64)
    nid = 0
    per: dict = {}
    for x0 in range(M):
        if memo[x0] >= 0:
            continue
        cam: list = []
        vis: dict = {}
        x = x0
        while True:
            if memo[x] >= 0:
                oid = memo[x]
                break
            if x in vis:
                oid = nid
                nid += 1
                per[oid] = len(cam) - vis[x]
                break
            vis[x] = len(cam)
            cam.append(x)
            x = int(sig[x])
        for y in cam:
            memo[y] = oid
    vol = np.bincount(memo, minlength=nid).astype(float) / M
    return nid, np.array(sorted(vol, reverse=True)), int(sum(per.values()))


# ── secciones ────────────────────────────────────────────────────────────────

def seccion_A(C) -> dict:
    print("\n═══ A — corpus ═══")
    print(f"{'corpus':<24} {'N':>3} {'valores':>8} {'diadico':>8} {'densidad':>9} {'h==0':>7}")
    out = {}
    for nom, d in C.items():
        W = d["W"]; N = W.shape[0]
        rng = np.random.default_rng(0); z = 0
        for _ in range(500):
            s = np.where(rng.random(N) < 0.5, 1., -1.)
            z += int(((W @ s) == 0).sum())
        r = dict(N=N, valores=int(np.unique(W[W != 0]).size), diadico=es_diadico(W),
                 densidad=float((W != 0).sum() / (N * N - N)), h_cero=z / (500 * N))
        out[nom] = r
        print(f"{nom:<24} {N:>3} {r['valores']:>8} {str(r['diadico']):>8} "
              f"{r['densidad']:>9.3f} {r['h_cero']:>7.3f}")
    return out


def seccion_B(C, n=2000) -> dict:
    print("\n═══ B — fragilidad al orden de suma ═══")
    print("Sincrono: W@s contra s@W. Identicos en algebra (W simetrica),")
    print("distintos en punto flotante — la suma no es asociativa.\n")
    print(f"{'corpus':<24} {'diadico':>8} {'pasos que cambian':>19}")
    out = {}
    for nom, d in C.items():
        W = d["W"]; N = W.shape[0]
        rng = np.random.default_rng(0); dif = 0
        for _ in range(n):
            s = np.where(rng.random(N) < 0.5, 1., -1.)
            h1 = W @ s
            h2 = (s[None, :] @ W)[0]
            s1 = np.where(h1 > 0, 1., np.where(h1 < 0, -1., s))
            s2 = np.where(h2 > 0, 1., np.where(h2 < 0, -1., s))
            if not np.array_equal(s1, s2):
                dif += 1
        out[nom] = dict(diadico=es_diadico(W), pasos_distintos=dif, n=n)
        print(f"{nom:<24} {str(es_diadico(W)):>8} {dif:>14}/{n}")

    # asincrono, sobre el corpus mas fragil
    nom = "caso09 forzado"
    W = C[nom]["W"]; N = W.shape[0]
    print(f"\nAsincrono sobre {nom} — BLAS contra suma exacta (math.fsum):")

    def relax_async(s0, W, dot, pasos=4000, seed=1):
        r = np.random.default_rng(seed); s = s0.copy()
        for _ in range(pasos):
            i = int(r.integers(N)); h = dot(W[i], s)
            s[i] = 1. if h > 0 else (-1. if h < 0 else s[i])
        return s

    dots = {"BLAS": lambda w, s: float(w @ s),
            "numpy": lambda w, s: float(np.sum(w * s)),
            "exacta": lambda w, s: math.fsum(w * s)}
    rng = np.random.default_rng(7); dif = {k: 0 for k in dots if k != "exacta"}; m = 300
    for _ in range(m):
        s0 = np.where(rng.random(N) < 0.5, 1., -1.)
        ref = relax_async(s0, W, dots["exacta"])
        for k in dif:
            if not np.array_equal(relax_async(s0, W, dots[k]), ref):
                dif[k] += 1
    for k, v in dif.items():
        print(f"  {k:<8} difiere del exacto en {v}/{m} trayectorias ({v/m:.1%})")
    out["_asincrono"] = dict(corpus=nom, n=m, difs=dif)
    return out


def seccion_C(C, n_runs=3000) -> dict:
    print("\n═══ C — W normalizada contra W cruda ═══")
    print("Normalizar es dividir por max|W|, un escalar POSITIVO.")
    print("sign(W@s) es invariante a eso en algebra. En la maquina, no.\n")
    out = {}
    for nom in ("caso09 natural", "caso09 forzado"):
        d = C[nom]
        Wn, textos, nodes = d["W"], d["textos"], d["nodes"]
        raw = W_cruda(textos, nodes, force_w_pos=(nom == "caso09 forzado"))
        N = Wn.shape[0]
        ii, jj = np.triu_indices(N, k=1)

        def orbs(W):
            co = COCO(W=W, n_runs=n_runs, seed=42)
            rng = np.random.default_rng(42); s = set()
            for _ in range(n_runs):
                o, _, _, _ = relax_orbit(sigma0(rng, N, "hipercubo"), W)
                s.add(o)
            return s

        on, orw = orbs(Wn), orbs(raw)
        bn = 1.0 / (BETA_RHO_STAR * N * float(np.mean(Wn[ii, jj])))
        br = 1.0 / (BETA_RHO_STAR * N * float(np.mean(raw[ii, jj])))
        r = dict(
            enteros=bool(np.all(raw == np.round(raw))),
            orb_norm=len(on), orb_cruda=len(orw),
            identicas=(on == orw),
            solo_norm=len(on - orw), solo_cruda=len(orw - on),
            comunes=len(on & orw),
            mu_norm=float(np.mean(Wn[ii, jj])), mu_cruda=float(np.mean(raw[ii, jj])),
            beta_c_norm=bn, beta_c_cruda=br,
        )
        out[nom] = r
        print(f"── {nom} ── (W cruda entera: {r['enteros']})")
        print(f"   orbitas   normalizada={r['orb_norm']}   cruda={r['orb_cruda']}   "
              f"identicas={r['identicas']}")
        print(f"   conjuntos comunes={r['comunes']}  solo_norm={r['solo_norm']}  "
              f"solo_cruda={r['solo_cruda']}")
        print(f"   mu_W  {r['mu_norm']:.6f} -> {r['mu_cruda']:.6f}     "
              f"beta_c  {bn:.4f} -> {br:.4f}")
        print("   (D_ckm, ALPHA_MIN/MAX no se tocan: son adimensionales)")
    return out


def seccion_D(C) -> dict:
    print("\n═══ D — enumeracion exhaustiva (verdad de terreno) ═══")
    print(f"{'corpus':<24} {'2^N':>9} {'orbitas':>9} {'|L|':>7} {'vol max':>9} "
          f"{'top-10':>8} {'N_eff':>8} {'t'}")
    out = {}
    for nom, d in C.items():
        W = d["W"]
        if W.shape[0] > 22:
            print(f"{nom:<24} {'—':>9}  no enumerable (N={W.shape[0]})")
            continue
        t0 = time.perf_counter()
        A, vol, L = enumerar_exhaustivo(W)
        dt = time.perf_counter() - t0
        out[nom] = dict(orbitas=A, L=L, vol=vol[:200].tolist(),
                        n_eff=n_eff(vol), segundos=dt)
        print(f"{nom:<24} {1<<W.shape[0]:>9} {A:>9} {L:>7} {vol[0]:>9.4f} "
              f"{vol[:10].sum():>8.4f} {n_eff(vol):>8.2f}  ({dt:.0f}s)")
    return out


def seccion_E(C, verdad: dict) -> dict:
    print("\n═══ E — muestreo contra verdad ═══")
    print("Las masas convergen; los conteos no.\n")
    out = {}
    for nom, d in C.items():
        if nom not in verdad:
            continue
        W = d["W"]; v = np.array(verdad[nom]["vol"]); A_r = verdad[nom]["orbitas"]
        ne_r = verdad[nom]["n_eff"]
        print(f"── {nom} ── (real: {A_r} orbitas, N_eff={ne_r:.2f})")
        print(f"{'n_runs':>9} {'A':>7} {'err A':>7} {'top-1':>8} {'top-10':>8} "
              f"{'N_eff':>8} {'err N_eff':>10}")
        filas = []
        for n in (1000, 10000, 100000):
            A, m = muestrear(W, n)
            fila = dict(n_runs=n, A=A, err_A=abs(A - A_r) / A_r, top1=float(m[0]),
                        top10=float(m[:10].sum()), n_eff=n_eff(m),
                        err_n_eff=abs(n_eff(m) - ne_r) / ne_r)
            filas.append(fila)
            print(f"{n:>9} {A:>7} {fila['err_A']:>6.0%} {m[0]:>8.4f} "
                  f"{m[:10].sum():>8.4f} {fila['n_eff']:>8.2f} {fila['err_n_eff']:>9.1%}")
        print(f"{'REAL':>9} {A_r:>7} {'--':>7} {v[0]:>8.4f} {v[:10].sum():>8.4f} "
              f"{ne_r:>8.2f}\n")
        out[nom] = filas
    return out


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seccion", default="ABCDE",
                    help="letras de las secciones a correr (default: ABCDE)")
    args = ap.parse_args()
    sel = args.seccion.upper()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    C = corpora()
    res: dict = {"timestamp": ts, "secciones": sel}

    if "A" in sel: res["A"] = seccion_A(C)
    if "B" in sel: res["B"] = seccion_B(C)
    if "C" in sel: res["C"] = seccion_C(C)
    verdad = res["D"] = seccion_D(C) if "D" in sel else {}
    if "E" in sel and verdad: res["E"] = seccion_E(C, verdad)

    out = OUT_DIR / f"orbit_analytics_{ts}.json"
    out.write_text(json.dumps(res, indent=2, default=float))
    print(f"\nResultados: {out}")


if __name__ == "__main__":
    main()
