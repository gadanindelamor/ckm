"""
driver_unidad_texto.py — la unidad de texto medida contra W

*(delamor: la unidad de texto es dependiente de W.)* Párrafo y página son
unidades tipográficas: vienen del formato del documento, no del campo. Este
driver mide, para varios tamaños de ventana y para los corpus del canal IAP,
qué le pasa a W: activación por texto y distribución de co-ocurrencias.

Dos tablas:
  --activacion  largo del texto y nodos activos por texto, por género.
  --coocurrencia  pares por texto (percentiles) y pares distintos sobre los
                  posibles — cuánta estructura (ceros) le queda a W.

Medido (Sep 2026, top_k=32, stopwords 703):
  - Los mensajes del canal NO son tweets: mediana 73–224 palabras. Más cerca
    de un párrafo de paper.
  - Por activación, caso09 (7 nodos/texto) coincide con páginas de 100
    palabras, aunque difieran en palabras (76 vs 108).
  - Con párrafos, el 61% de los textos no aporta ningún par.
  - Los pares DISTINTOS saturan enseguida: desde páginas de 40 palabras hay
    451 de 496 posibles. W queda sin ceros y el paisaje colapsa.
  - caso09 es el menos saturado: 307/496 (62%). caso14 llega a 492/496.

Uso:
    python experiments/driver_unidad_texto.py [--activacion] [--coocurrencia]
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))
sys.path.insert(0, str(REPO / "experiments"))
from corpus_service import CorpusService                      # noqa: E402
from node_extractor import NodeExtractorService, _STOPWORDS   # noqa: E402
from corpus_informes_limpio import paginar                    # noqa: E402

PAT = r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ_][a-záéíóúüñA-ZÁÉÍÓÚÜÑ_]{2,}"
PARRAFOS = REPO / "process/corpus_informes/corpus_informes.txt"
IAP = {"IAP caso09": "1784685610_caso09_run2", "IAP caso13": "1785135692_caso13",
       "IAP caso14": "1785214255_caso14_run2"}
VENTANAS = (0, 40, 60, 100, 150, 200, 300, 500)


def corpora():
    P = [l.strip() for l in PARRAFOS.read_text(encoding="utf8").splitlines() if l.strip()]
    for w in VENTANAS:
        yield ("párrafo" if w == 0 else f"página {w}"), (P if w == 0 else paginar(P, w))
    for nom, f in IAP.items():
        p = REPO / f"process/iap/corpus_state.json.bak_{f}"
        if p.exists():
            yield nom, json.loads(p.read_text())["texts"]


def _W(textos, k):
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"), min_texts=len(textos),
                      top_k=k, rebuild_suspendido=True)
    c.ingest(textos)
    return c.get_W(), c.get_nodes()


def activacion(k=32):
    print(f'{"corpus":16s} {"txts":>5} {"pal p10/med/p90":>18} {"act med":>8} {"0 nodos":>8} {"dens":>6} {"neg":>5}')
    for nom, T in corpora():
        W, n = _W(T, k)
        ii, jj = np.triu_indices(len(W), 1)
        u = W[ii, jj]
        X = TfidfVectorizer(vocabulary=list(n), ngram_range=(1, 2), token_pattern=PAT,
                            stop_words=sorted(_STOPWORDS)).fit_transform(T)
        act = np.asarray((X > 0).sum(axis=1)).ravel()
        pal = np.array([len(t.split()) for t in T])
        print(f'{nom:16s} {len(T):5d} {np.percentile(pal,10):5.0f}/{np.median(pal):5.0f}/{np.percentile(pal,90):5.0f} '
              f'{np.median(act):8.0f} {(act==0).mean():7.0%} {(u!=0).mean():6.3f} {int((u<0).sum()):5d}')


def coocurrencia(k=32):
    posibles = k * (k - 1) // 2
    print(f'{"corpus":16s} {"txts":>5} {"pares":>7} {"p10":>5} {"med":>6} {"p90":>6} {"máx":>5} '
          f'{"0 pares":>8} {"distintos":>10} {"/posibles":>9} {"p/100pal":>9}')
    for nom, T in corpora():
        r = NodeExtractorService(top_k=k).accumulate(T)
        pares = np.array([len(d) for d in r["pairs_by_text"]])
        pal = np.array([len(t.split()) for t in T])
        print(f'{nom:16s} {len(T):5d} {int(pares.sum()):7d} {np.percentile(pares,10):5.0f} {np.median(pares):6.0f} '
              f'{np.percentile(pares,90):6.0f} {pares.max():5d} {(pares==0).mean():7.0%} '
              f'{len(r["pairs"]):10d} {len(r["pairs"])/posibles:8.0%} {pares.sum()/pal.sum()*100:9.2f}')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--activacion", action="store_true")
    ap.add_argument("--coocurrencia", action="store_true")
    ap.add_argument("--top-k", type=int, default=32)
    a = ap.parse_args()
    if a.activacion or not a.coocurrencia:
        activacion(a.top_k)
    if a.coocurrencia or not a.activacion:
        print()
        coocurrencia(a.top_k)
