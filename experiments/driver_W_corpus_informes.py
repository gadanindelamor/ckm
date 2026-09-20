"""
driver_W_corpus_informes.py — W del corpus de informes, por unidad de texto

Construye W con los servicios reales (una sola ingesta, rebuild suspendido)
desde el corpus de informes, y compara qué cambia según qué sea un "texto":
párrafo o página. CKM define la co-ocurrencia *en el mismo texto*, así que la
unidad decide qué significa co-ocurrir.

Corpus: `experiments/corpus_informes_limpio.py` (870 párrafos únicos, 15.557
palabras, 27 informes). Página = párrafos completos hasta ~300 palabras.

Medido (Sep 2026, top_k=32, stopwords 703, rebuild suspendido):

| unidad | textos | palabras/texto | densidad | neg | mu_W | N_eff@1000 | N_eff@5000 |
|---|---:|---:|---:|---:|---:|---:|---:|
| párrafo | 870 | 17.9 | 0.766 | 1 | 0.1094 | 2.00 | 2.01 |
| página 300 | 50 | 311.1 | 0.831 | 210 | 0.0294 | 9.52 | 9.68 |

  - Por párrafo el paisaje colapsa: N_eff = 2 (todo encendido y su espejo),
    régimen G2 de DEFS §13.
  - Por página hay paisaje (N_eff ≈ 9.5, estable entre 1000 y 5000 runs),
    pero los 210 pares negativos NO son más tensión: el ruteo por marcadores
    es por texto, y un texto largo tiene más chance de contener uno. Textos
    con marcador: 4% por párrafo, 50% por página, con casi las mismas
    ocurrencias de "pero" (25 vs 19). Tensión estructural y longitud del
    texto quedan confundidas.

Barridos (--barrido):
  - top_k 32/64/128/256 en las dos unidades: van en sentidos opuestos. Con
    párrafos, subir top_k mejora cobertura (textos sin ningún nodo 34% → 4%)
    y el paisaje sigue en N_eff = 2. Con páginas, llena cada texto de nodos
    (51.9 de 256 activos) y hace explotar los negativos (9656): N_eff cae de
    9.52 a 2.01.
  - tamaño de página con top_k=64: sólo la de 300 palabras da paisaje
    (N_eff 6.68); 40, 60, 100 y 150 colapsan en 2.00 aunque tengan hasta 249
    pares negativos. No es gradual.
  - contrafáctico force_w_pos (misma W sin traducir marcadores a negativos):
    N_eff = 2.00 EXACTO con top_k 32 y 64. Todo el paisaje de este corpus
    viene de la frustración que introducen los negativos, y los negativos
    vienen del largo del texto:
        largo → chance de contener un marcador → pares negativos →
        frustración → N_eff.
    En este corpus N_eff mide densidad de marcadores, no estructura
    conceptual. Néel (DEFS §15) sería la forma de elicitar pares sin que la
    longitud los produzca.

Uso:
    python experiments/driver_W_corpus_informes.py [--top-k 32] [--json out.json]
    python experiments/driver_W_corpus_informes.py --barrido
"""

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))
from corpus_service import CorpusService          # noqa: E402
from landscape_engine import basin_masses, count_attractors, n_eff  # noqa: E402

CORPUS = REPO / "process/corpus_informes"
UNIDADES = {"párrafo": CORPUS / "corpus_informes.txt",
            "página 300": CORPUS / "corpus_informes_paginas300.txt"}


def medir(path: Path, etiqueta: str, top_k: int, n_runs=(1000, 5000)) -> dict:
    textos = [l.strip() for l in path.read_text(encoding="utf8").splitlines() if l.strip()]
    t0 = time.time()
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"),
                      min_texts=len(textos), top_k=top_k, rebuild_suspendido=True)
    c.ingest(textos)
    W, nodos = c.get_W(), c.get_nodes()
    ii, jj = np.triu_indices(len(W), 1)
    u = W[ii, jj]
    con_marcador = sum(CorpusService._has_opposition(t) for t in textos)
    fila = {
        "unidad": etiqueta, "textos": len(textos),
        "palabras_por_texto": round(sum(len(t.split()) for t in textos) / len(textos), 1),
        "con_marcador": con_marcador,
        "frac_con_marcador": round(con_marcador / len(textos), 3),
        "N": len(nodos), "densidad": round(float((u != 0).mean()), 3),
        "pares_negativos": int((u < 0).sum()), "aislados": int((~W.any(axis=1)).sum()),
        "mu_W": round(float(u.mean()), 4), "segundos_build": round(time.time() - t0, 2),
        "nodos": nodos,
    }
    for nr in n_runs:
        masas = basin_masses(W, n_runs=nr, seed=0)
        fila[f"A_{nr}"] = count_attractors(W, n_runs=nr, seed=0)
        fila[f"N_eff_{nr}"] = round(n_eff(masas), 2)
        fila[f"saturacion_{nr}"] = round(n_eff(masas) / nr, 4)
    return fila


def barrido():
    """top_k por unidad, tamaño de página con top_k=64, y el contrafáctico."""
    sys.path.insert(0, str(REPO / "experiments"))
    from corpus_informes_limpio import paginar

    print("== top_k por unidad")
    for etq, p in UNIDADES.items():
        for k in (32, 64, 128, 256):
            f = medir(p, etq, k, n_runs=(1000,))
            print(f"{etq:11s} top_k {k:4d} | dens {f['densidad']:.3f} | neg {f['pares_negativos']:5d} "
                  f"| A {f['A_1000']:4d} | N_eff {f['N_eff_1000']:6.2f}")

    print("\n== tamaño de página, top_k=64")
    parrafos = [l.strip() for l in (CORPUS / "corpus_informes.txt").read_text(encoding="utf8").splitlines() if l.strip()]
    for w in (0, 40, 60, 100, 150, 300):
        textos = parrafos if w == 0 else paginar(parrafos, w)
        tmp = Path(tempfile.mktemp(suffix=".txt"))
        tmp.write_text("\n".join(textos), encoding="utf8")
        f = medir(tmp, "párrafo" if w == 0 else f"página {w}", 64, n_runs=(1000,))
        print(f"{f['unidad']:11s} | textos {f['textos']:4d} | c/marcador {f['frac_con_marcador']:5.0%} "
              f"| neg {f['pares_negativos']:5d} | N_eff {f['N_eff_1000']:6.2f}")

    print("\n== contrafáctico force_w_pos (página 300)")
    textos = [l.strip() for l in (UNIDADES["página 300"]).read_text(encoding="utf8").splitlines() if l.strip()]
    for k in (32, 64):
        for forzada in (False, True):
            c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"), min_texts=len(textos),
                              top_k=k, rebuild_suspendido=True, force_w_pos=forzada)
            c.ingest(textos)
            W = c.get_W()
            ii, jj = np.triu_indices(len(W), 1)
            neg = int((W[ii, jj] < 0).sum())
            ne = n_eff(basin_masses(W, n_runs=1000, seed=0))
            print(f"top_k {k} | {'W_pos forzada' if forzada else 'natural':14s} | neg {neg:5d} | N_eff {ne:6.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--barrido", action="store_true", help="top_k, tamaño de página y contrafáctico")
    ap.add_argument("--top-k", type=int, default=32)
    ap.add_argument("--json")
    args = ap.parse_args()

    if args.barrido:
        barrido()
        return

    filas = [medir(p, etq, args.top_k) for etq, p in UNIDADES.items() if p.exists()]
    if not filas:
        sys.exit("falta el corpus: correr experiments/corpus_informes_limpio.py")

    cols = [c for c in filas[0] if c != "nodos"]
    print(" | ".join(cols))
    for f in filas:
        print(" | ".join(str(f[c]) for c in cols))
    if len(filas) == 2:
        a, b = (set(f["nodos"]) for f in filas)
        print("\nnodos sólo en", filas[0]["unidad"], ":", sorted(a - b))
        print("nodos sólo en", filas[1]["unidad"], ":", sorted(b - a))
    if args.json:
        Path(args.json).write_text(json.dumps(filas, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
