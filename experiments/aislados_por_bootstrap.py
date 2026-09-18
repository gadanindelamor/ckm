"""
aislados_por_bootstrap.py — frecuencia y dispersión de nodos aislados en W

Clase T. Un nodo aislado tiene su fila de W entera en cero: su campo local es
siempre 0 y conserva el valor que tenga. Con a aislados, cada atractor
acoplado aparece en 2^a copias triviales — infla A0, el conteo de atractores y
N_eff, y da d(σ) = 1 por el flip del nodo aislado.

Encontrado en caso09 bootstrap 12 (N=32, 3 aislados). Esta exploración mira si
es un rasgo de ese punto o de las W del proyecto en general.

Para cada corpus (textos distintos, respaldos duplicados se descartan) y cada
bootstrap k (W construida una vez con los primeros k textos, top_k=32):
N, pesos negativos y nodos aislados.

Corpus: casos IAP con ≥ MIN_TEXTOS textos en process/iap/ y WARMUP_TEXTS
(teoría CKM). Otro dominio (fourforums, CreateDebate) no está en el repo: sus
pipelines leen un dump SQL que pertenece a ckmdatasets.

Uso:
    python experiments/aislados_por_bootstrap.py [--json salida.json]

Medido (Sep 2026): 15 corpus, 217 W.
  - 113/217 (52%) con al menos un aislado; media 1.12, desvío 1.65, máx 10/32
    (caso11_run2, k=4). Sólo 1 corpus sin ninguno (caso12_run2).
  - Se concentran temprano (N ya en 32, pocos textos) y tienden a bajar con
    más textos, no monótono. caso09 (referencia): 3 en k=12, 1 en k=16.
  - Mecanismo probable, NO verificado: top_k=32 fija N aunque los textos aún
    no conecten ese vocabulario; un término entra por TF-IDF sin co-ocurrir
    con ningún otro de los 32.
  - Consecuencia: en la mitad de las W, A0 / conteo / N_eff llevan un factor
    2^a de copias triviales, y d(σ)=1 aparece por el flip del aislado.
"""

import argparse
import ast
import glob
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))
from corpus_service import CorpusService  # noqa: E402

MIN_TEXTOS = 12
TOP_K = 32
K_MIN = 3


def _warmup():
    src = (REPO / "iap_chatroom/tests/test_armstrong_stop_coco.py").read_text()
    arbol = ast.parse(src)
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and getattr(nodo.targets[0], "id", "") == "WARMUP_TEXTS":
            return ast.literal_eval(nodo.value)
    return []


def corpus_disponibles():
    vistos, out = set(), []
    for f in sorted(glob.glob(str(REPO / "process/iap/corpus_state.json.bak_*"))):
        try:
            textos = json.loads(Path(f).read_text()).get("texts", [])
        except (json.JSONDecodeError, OSError):
            continue
        h = hashlib.sha256("\n".join(textos).encode()).hexdigest()
        if len(textos) >= MIN_TEXTOS and h not in vistos:
            vistos.add(h)
            out.append((Path(f).name.split("_", 2)[-1], textos))
    w = _warmup()
    if w:
        out.append(("WARMUP_TEXTS", w))
    return out


def medir(textos, k):
    c = CorpusService(storage_path=tempfile.mktemp(suffix=".json"),
                      min_texts=k, top_k=TOP_K)
    c.ingest(textos[:k])
    W = c.get_W()
    if W is None:
        return None
    return {"k": k, "N": len(W), "neg": int((W < 0).sum()) // 2,
            "aislados": int((~W.any(axis=1)).sum())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    resultado = {}
    for nombre, textos in corpus_disponibles():
        filas = [f for f in (medir(textos, k) for k in range(K_MIN, len(textos) + 1)) if f]
        resultado[nombre] = filas
        a = np.array([f["aislados"] for f in filas])
        frac = np.array([f["aislados"] / f["N"] for f in filas])
        print(f"\n── {nombre} ({len(textos)} textos)")
        print("   k:        " + " ".join(f"{f['k']:>3}" for f in filas))
        print("   N:        " + " ".join(f"{f['N']:>3}" for f in filas))
        print("   aislados: " + " ".join(f"{f['aislados']:>3}" for f in filas))
        print(f"   con aislados {int((a > 0).sum())}/{len(a)} bootstraps | "
              f"media {a.mean():.2f} | desvío {a.std():.2f} | máx {a.max()} | "
              f"fracción de N media {frac.mean():.3f}")

    todas = [f for fs in resultado.values() for f in fs]
    a = np.array([f["aislados"] for f in todas])
    print(f"\nTOTAL {len(resultado)} corpus, {len(todas)} W | con aislados "
          f"{int((a > 0).sum())}/{len(a)} ({(a > 0).mean():.0%}) | media {a.mean():.2f} "
          f"| desvío {a.std():.2f} | máx {a.max()}")
    if args.json:
        Path(args.json).write_text(json.dumps(resultado, indent=1))


if __name__ == "__main__":
    main()
