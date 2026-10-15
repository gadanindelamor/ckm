"""
driver_cpm_nulo_marcadores.py — CP-M de TASK_condiciones_del_paper_v1

**El nulo de marcadores** (review v28, M4). Mismos textos, **la misma cantidad**
marcada como oposición, pero la marca puesta **al azar**: si la caída de N_eff
con la marca real no se distingue de la de las barajadas, el signo no lleva
información de oposición **más allá del procedimiento declarado**.

El CP-M es **opcional**: el paper afirma lo que pasa **bajo** el procedimiento
de marcadores, que está declarado (`docs/defs/DECLARACION_extraccion_W_v1.md`,
paso 7). El nulo le sirve a quien quiera leer el signo como "oposición", y esa
lectura es del lector. Esto **no valida ni invalida** lo que el paper afirma:
acota qué más se puede decir.

## Por qué no se re-extrae por permutación

**El conjunto de nodos no depende del signo.** Los nodos salen de
`accumulate`, que nunca ve `s(u)`: el signo se aplica recién en
`CorpusService._rebuild`, ruteando pares **ya extraídos** a `pos` o a `neg`.
Así que se extrae **una vez** y se re-firma.

Para que eso no sea "la fórmula del driver" en vez de la del repo,
`verificar_contra_el_repo()` **compara la W de la marca real contra la de
`CorpusService`** y aborta si difieren. Sin esa verificación, todo lo demás
mide otra cosa.

No toca `services/` ni el gate (`f96c234`). No arregla nada: mide.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

from services.node_extractor import NodeExtractorService            # noqa: E402
from services.corpus_service import CorpusService                   # noqa: E402
from services.landscape_engine import count_attractors              # noqa: E402

TOP_K   = 20
N_RUNS  = 1000
SEEDS   = list(range(5))
N_PERM  = 200
SEED_PERM = 20261015

CORPUS = {
    "A24": RAIZ / "process/experiments/wmixta_paso2_natural/corpus_natural_uniform.json",
    "D12": RAIZ / "iap_chatroom/_state/corpus_state.json",
    "E7" : RAIZ / "process/iap/corpus_state.json",
}


def textos_de(ruta: Path) -> list[str]:
    return [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]


def extraer(textos):
    """Una sola vez: nodos y pares por texto. El signo no entra acá."""
    ex = NodeExtractorService(top_k=TOP_K, ngram_max=2)
    r  = ex.accumulate(textos)
    return r["nodes"], r.get("pairs_by_text", [])


def W_con_marcas(nodes, pairs_by_text, marcados: set[int]) -> np.ndarray | None:
    """
    Misma construcción que `CorpusService._rebuild`: pos − neg, normalizada por
    máx|·| (sin dividir si es 0), diagonal 0.
    """
    if not nodes:
        return None
    N   = len(nodes)
    idx = {n: i for i, n in enumerate(nodes)}
    pos = np.zeros((N, N))
    neg = np.zeros((N, N))
    for k, del_texto in enumerate(pairs_by_text):
        destino = neg if k in marcados else pos
        for (ni, nj), cuenta in del_texto.items():
            if ni in idx and nj in idx:
                i, j = idx[ni], idx[nj]
                destino[i, j] += cuenta
                destino[j, i] += cuenta
    raw = pos - neg
    m   = np.abs(raw).max()
    W   = raw / m if m > 0 else raw
    np.fill_diagonal(W, 0.0)
    return W


def verificar_contra_el_repo(textos, nodes, pbt, reales) -> None:
    """Sin esto, el driver mide su propia fórmula y no la del repo."""
    c = CorpusService(storage_path="/dev/null", min_texts=10**9, top_k=TOP_K)
    c._texts = list(textos)
    c._rebuild()
    W_repo = c.get_W()
    assert c.get_nodes() == nodes, "los nodos del driver no son los del repo"
    W_mio = W_con_marcas(nodes, pbt, reales)
    assert np.allclose(W_repo, W_mio), "la W del driver NO es la del repo"


def neff(W) -> list[float]:
    return [count_attractors(W, n_runs=N_RUNS, seed=s) for s in SEEDS]


def main() -> None:
    print(f"CP-M — nulo de marcadores   (top_k={TOP_K}, n_runs={N_RUNS}, "
          f"{len(SEEDS)} seeds por W, {N_PERM} permutaciones)\n")

    for nombre, ruta in CORPUS.items():
        if not ruta.exists():
            print(f"## {nombre}: NO ESTÁ — se declara y se sigue\n")
            continue
        textos = textos_de(ruta)
        n      = len(textos)
        dups   = n - len(set(textos))
        reales = {i for i, t in enumerate(textos)
                  if CorpusService._has_opposition(t)}
        k = len(reales)

        print(f"## {nombre} — {n} textos, {dups} repetidos")
        print(f"   k (con marcador real) = {k} de {n}  ({100*k/n:.0f}%)")

        nodes, pbt = extraer(textos)
        if not nodes:
            print("   sin nodos: no hay W. Se declara y se sigue.\n")
            continue
        verificar_contra_el_repo(textos, nodes, pbt, reales)
        print(f"   W del driver == W de CorpusService  (N={len(nodes)})")

        if k == 0 or k == n:
            print(f"   **NO HAY NULO POSIBLE**: con k={k} y n={n} toda barajada "
                  f"es la misma marca. Se reporta y se sigue.\n")
            continue

        W_pos   = W_con_marcas(nodes, pbt, set())
        W_real  = W_con_marcas(nodes, pbt, reales)
        v_pos   = neff(W_pos)
        v_real  = neff(W_real)
        base    = statistics.mean(v_pos)
        caida_r = base - statistics.mean(v_real)

        rng = np.random.default_rng(SEED_PERM)
        caidas, sds = [], []
        for _ in range(N_PERM):
            baraja = set(rng.choice(n, size=k, replace=False).tolist())
            v = neff(W_con_marcas(nodes, pbt, baraja))
            caidas.append(base - statistics.mean(v))
            sds.append(statistics.stdev(v))
        caidas = np.array(caidas)

        pct = float((caidas <= caida_r).mean())
        print(f"   N_eff(W_pos)   = {base:7.3f}   (sd entre seeds "
              f"{statistics.stdev(v_pos):.3f})")
        print(f"   N_eff(W_mixta real) = {statistics.mean(v_real):7.3f}   "
              f"caída real = {caida_r:+.3f}")
        print(f"   caída barajada: media {caidas.mean():+.3f}  "
              f"sd {caidas.std(ddof=1):.3f}  "
              f"[{caidas.min():+.3f}, {caidas.max():+.3f}]")
        print(f"   ruido de muestreo dentro de una W: sd media "
              f"{statistics.mean(sds):.3f}")
        print(f"   la caída real está en el percentil {100*pct:.1f} del nulo")
        print(f"   ¿afuera del rango de las {N_PERM} barajadas? "
              f"{'SÍ' if (caida_r < caidas.min() or caida_r > caidas.max()) else 'NO'}\n")

    print("No se fija umbral (CP-M). El percentil se reporta, no se compara "
          "contra un corte.")


if __name__ == "__main__":
    main()
