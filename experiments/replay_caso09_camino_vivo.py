"""
replay_caso09_camino_vivo.py — caso09_run2 por el camino de CKMMonitor.on_message

Clase T. Mide, sin conectar nada, sobre qué base operaría COCO en el canal vivo.

Mismo camino que iap_chatroom/ckm_monitor.py: CorpusService(min_texts=3,
top_k=32) y MonitorService con defaults (n_runs=50, uniform, sin thermostat).
Por cada mensaje: ingest y, desde el tercero, evaluate. BehaviorGraph se omite
(no toca Δ_r ni D_ckm).

Por mensaje registra: rebuild (sha de W), N, si cambió el orden o el conjunto
de nodos, pesos negativos, reset de Δ_r (D2), pares metabolizados,
Delta_r_sum, D_ckm, A0 y fabrication_index.

Uso:
    python experiments/replay_caso09_camino_vivo.py              # services/ actual
    python experiments/replay_caso09_camino_vivo.py --ref 5b52992  # services/ de un commit

Medido (Sep 2026), 24 textos, 22 evaluados:
  - W se reconstruye en los 22 y el CONJUNTO de nodos cambia en los 22.
  - antes de D2 (--ref 5b52992): Δ_r acumula hasta 2316 sobre conjuntos de
    nodos distintos; A0=4 fijado con N=19 y nunca recalculado; D_ckm entre
    −1.0 y 0.5 — se mueve pero no mide.
  - desde D2 (341f612): reset en cada mensaje; D_ckm = 0.0 en los 22, por
    construcción (A0 y A_actual sobre la misma W_eff).
  En ninguno D_ckm tiene campo: el conjunto de nodos no se estabiliza.
"""

import argparse
import json
import subprocess
import sys
import tarfile
import tempfile
import time
from io import BytesIO
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CASO = REPO / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"


def _services_dir(ref):
    if ref is None:
        return REPO / "services"
    out = Path(tempfile.mkdtemp())
    data = subprocess.run(["git", "-C", str(REPO), "archive", ref, "services"],
                          check=True, capture_output=True).stdout
    tarfile.open(fileobj=BytesIO(data)).extractall(out)
    return out / "services"


def replay(services):
    sys.path.insert(0, str(services))
    from corpus_service import CorpusService
    from monitor_service import MonitorService

    textos = json.loads(CASO.read_text())["texts"]
    tmp = Path(tempfile.mkdtemp())
    jsonl = str(tmp / "traj.jsonl")
    corpus = CorpusService(storage_path=str(tmp / "c.json"), min_texts=3, top_k=32,
                           monitor_jsonl_path=jsonl)
    monitor = MonitorService(corpus, storage_path=jsonl)

    filas, prev = [], None
    for i, texto in enumerate(textos, start=1):
        sha_a = corpus.w_sha()
        corpus.ingest([texto])
        nodes = corpus.get_nodes()
        fila = {
            "i": i,
            "rebuild": sha_a != corpus.w_sha(),
            "N": len(nodes),
            "orden_cambia": prev is not None and nodes != prev,
            "conjunto_cambia": prev is not None and set(nodes) != set(prev),
            "W_neg": int((corpus.get_W() < 0).sum()) if corpus.mode == "evaluation" else None,
        }
        prev = nodes
        if i >= corpus.min_texts:
            p = monitor.evaluate(texto, device_id=f"c09_{i:02d}")
            fila.update(
                evaluado=True,
                reset=p.get("Delta_r_reset", "n/a"),
                pares=p["n_rejected_pairs"],
                Dr_sum=p["Delta_r_sum"],
                D_ckm=p["D_ckm"],
                A0=monitor._A0,
                fi=p["fabrication_index"],
            )
        filas.append(fila)
    return filas


def imprimir(filas):
    cols = ["i", "rebuild", "N", "orden_cambia", "conjunto_cambia", "W_neg",
            "reset", "pares", "Dr_sum", "D_ckm", "A0", "fi"]
    print(" ".join(f"{c[:7]:>7}" for c in cols))
    for f in filas:
        print(" ".join(f"{str(f.get(c, '')):>7}" for c in cols))
    ev = [f for f in filas if f.get("evaluado")]
    print(f"\nmensajes {len(filas)} | evaluados {len(ev)} | "
          f"rebuilds {sum(f['rebuild'] for f in filas)} | "
          f"conjunto cambia {sum(f['conjunto_cambia'] for f in filas)} | "
          f"D_ckm != 0: {sum(f['D_ckm'] != 0 for f in ev)} | "
          f"Delta_r_sum final {ev[-1]['Dr_sum']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", help="commit cuyos services/ usar (default: árbol actual)")
    ap.add_argument("--json", help="guardar filas en este archivo")
    args = ap.parse_args()

    t0 = time.time()
    filas = replay(_services_dir(args.ref))
    imprimir(filas)
    print(f"services: {args.ref or 'árbol actual'} | {time.time() - t0:.1f}s")
    if args.json:
        Path(args.json).write_text(json.dumps(filas, indent=1))
