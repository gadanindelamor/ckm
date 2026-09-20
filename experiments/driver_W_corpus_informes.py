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

Uso:
    python experiments/driver_W_corpus_informes.py [--top-k 32] [--json out.json]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-k", type=int, default=32)
    ap.add_argument("--json")
    args = ap.parse_args()

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
