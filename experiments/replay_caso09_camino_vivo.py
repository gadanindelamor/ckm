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
    python experiments/replay_caso09_camino_vivo.py --sin-rebuild [--bootstrap K]

--sin-rebuild: W se construye UNA vez, cuando el corpus llega a K textos
(default K = min_texts = 3, como el canal). Después los textos se acumulan
sin reconstruir W — nodos fijos, Δ_r y A0 sobre el mismo campo. La señal de
rebuild se calcula igual que CKMMonitor.on_message (estructural >
volumen > tiempo) y se registra, pero nadie la ejecuta. services/ no se
toca: tras el bootstrap se sube corpus.min_texts para que ingest() no
reconstruya; la señal usa el min_texts del canal (3).

Medido (Sep 2026), 24 textos, 22 evaluados:
  - W se reconstruye en los 22 y el CONJUNTO de nodos cambia en los 22.
  - antes de D2 (--ref 5b52992): Δ_r acumula por índice hasta 2316; A0=4 se
    fija en la primera evaluación (N=19) y se conserva; D_ckm entre −1.0 y
    0.5. Es lo que ese marco define: índice como identidad de par, A0 del
    primer campo evaluado.
  - desde D2 (341f612): el marco toma a los nodos como identidad y resetea
    Δ_r y A0 cuando W cambia. Como W cambia en cada mensaje, A0 y A_actual
    se calculan sobre la misma W_eff y D_ckm = 0.0 en los 22 — consecuencia
    de la definición, no una medición.
  Lo que ambos marcos comparten: el conjunto de nodos no se estabiliza, y el
  instrumento reporta D_ckm, una métrica con los sesgos del conteo de
  atractores del que sale — n_runs (el conteo no satura:
  REG_orbitas_conjuntos_invariantes_v1, terminales y órbitas no convergen;
  la masa de cuenca sí) y la distribución de sigma_0. Cada relajación
  converge (LaSalle); el sesgo está en el conteo.

Medido --sin-rebuild (Sep 2026), árbol actual:
  bootstrap  N  W_neg  A0  D_ckm                          señal E
      3     19     0    4  0.0 salvo −0.25 al final; fi≈1   nunca
      8     32    16   12  0 → −0.42 (expande)             nunca
     12     32    28   25  0 → 0.72, cruza 0.40 en el msj 15  nunca
     16     32    36   17  0.12 – 0.35                     nunca
  - El instrumento opera sobre W estable: D_ckm se mueve y su signo depende
    del bootstrap.
  - V (volumen: textos ≥ 6) es verdadera desde el mensaje 6 y no vuelve a
    apagarse; T (10 ciclos sin rebuild) igual, una vez congelada W.
  - E (should_rebuild: gradiente > 0 en 3 pasos seguidos) no emite nunca,
    tampoco con bootstrap 12, donde D_ckm sube por encima del umbral: la
    grilla de D_ckm (paso 1/A0) produce mesetas que cortan la racha.

CONDICIÓN EMPÍRICA REGISTRADA (delamor, Sep 2026): para caso09_run2,
bootstrap = 12 textos. Es el punto medido donde W (N=32, 28 pesos negativos,
A0=25) da a D_ckm grilla fina y recorrido que cruza D_CKM_THRESHOLD. Vale
para este caso y este camino (min_texts=3, top_k=32, n_runs=50, uniform);
no es un default del instrumento.

CORRECCIÓN (Sep 2026, REG_hipotesis_distancia_contextual_v3): la W de
bootstrap 12 tiene 3 nodos aislados (conversation, about, low). Δ_r los va
acoplando en W_eff: 2 aislados al fijar A0 (msj 12), 1 desde el msj 15. El
cruce de 0.40 en el msj 15 coincide con el acople de "conversation" — A pierde
un factor 2 que A0 conserva. Sin aislados, D queda plano 0.45–0.64 desde el
msj 13. La subida 0 → 0.72 está mezclada con ese cambio de factor.

W CORREGIDA (5aa3504, REG_hipotesis_distancia_contextual_v4): los aislados
venían de la re-extracción por texto en CorpusService. Con pares entre nodos
globales, bootstrap 12 tiene 0 aislados, A0 = 5 y D_ckm 0 → −1.8 (Δ_r
expande). La condición de bootstrap 12 y las mediciones de arriba valen en
el marco de la W recortada; con la W corregida caso09 no tiene todavía
condición de referencia.
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


MIN_TEXTS_CANAL = 3
MAX_CICLOS = 10   # iap_chatroom/ckm_monitor.py


def replay(services, sin_rebuild=False, bootstrap=MIN_TEXTS_CANAL, panel_jsonl=None):
    sys.path.insert(0, str(services))
    from corpus_service import CorpusService
    from monitor_service import MonitorService

    textos = json.loads(CASO.read_text())["texts"]
    tmp = Path(tempfile.mkdtemp())
    jsonl = panel_jsonl or str(tmp / "traj.jsonl")
    Path(jsonl).unlink(missing_ok=True)
    corpus = CorpusService(storage_path=str(tmp / "c.json"),
                           min_texts=bootstrap if sin_rebuild else MIN_TEXTS_CANAL,
                           top_k=32, monitor_jsonl_path=jsonl)
    monitor = MonitorService(corpus, storage_path=jsonl)

    filas, prev = [], None
    d_hist, ciclos_sin_rebuild = [], 0
    for i, texto in enumerate(textos, start=1):
        sha_a = corpus.w_sha()
        corpus.ingest([texto])
        if sin_rebuild and corpus.mode == "evaluation":
            corpus.min_texts = 10**9          # congelar W desde el bootstrap
        nodes = corpus.get_nodes()
        ciclos_sin_rebuild = 0 if sha_a != corpus.w_sha() else ciclos_sin_rebuild + 1
        fila = {
            "i": i,
            "rebuild": sha_a != corpus.w_sha(),
            "N": len(nodes),
            "orden_cambia": prev is not None and nodes != prev,
            "conjunto_cambia": prev is not None and set(nodes) != set(prev),
            "W_neg": int((corpus.get_W() < 0).sum()) if corpus.mode == "evaluation" else None,
        }
        prev = nodes
        if corpus.mode == "evaluation" and i >= MIN_TEXTS_CANAL:
            p = monitor.evaluate(texto, device_id=f"c09_{i:02d}")
            d_hist.append(p["D_ckm"])
            estructural = corpus.should_rebuild(d_hist, n=3)
            volumen = len(corpus._texts) >= MIN_TEXTS_CANAL * 2
            tiempo = ciclos_sin_rebuild >= MAX_CICLOS
            fila["senal"] = ("E" if estructural else "") + ("V" if volumen else "") + ("T" if tiempo else "") or "-"
            fila.update(
                evaluado=True,
                reset=p.get("Delta_r_reset", "n/a"),
                pares=p["n_rejected_pairs"],
                Dr_sum=p["Delta_r_sum"],
                D_ckm=p["D_ckm"],
                A0=monitor._A0,
                fi=p["fabrication_index"],
                N_eff=p.get("N_eff", "n/a"),
                N_eff0=p.get("N_eff0", "n/a"),
            )
        filas.append(fila)
    return filas


def imprimir(filas):
    cols = ["i", "rebuild", "N", "orden_cambia", "conjunto_cambia", "W_neg",
            "reset", "pares", "Dr_sum", "D_ckm", "A0", "fi", "N_eff", "N_eff0", "senal"]
    print(" ".join(f"{c[:7]:>7}" for c in cols))
    for f in filas:
        print(" ".join(f"{str(f.get(c, '')):>7}" for c in cols))
    ev = [f for f in filas if f.get("evaluado")]
    print(f"\nmensajes {len(filas)} | evaluados {len(ev)} | "
          f"rebuilds {sum(f['rebuild'] for f in filas)} | "
          f"conjunto cambia {sum(f['conjunto_cambia'] for f in filas)} | "
          f"D_ckm != 0: {sum(f['D_ckm'] != 0 for f in ev)} | "
          f"Delta_r_sum final {ev[-1]['Dr_sum']} | "
          f"señal E (estructural): {[f['i'] for f in ev if 'E' in f['senal']]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", help="commit cuyos services/ usar (default: árbol actual)")
    ap.add_argument("--json", help="guardar filas en este archivo")
    ap.add_argument("--panel-jsonl", help="conservar el JSONL de paneles de Monitor en este archivo")
    ap.add_argument("--sin-rebuild", action="store_true",
                    help="W una sola vez en el bootstrap; la señal se registra, no se ejecuta")
    ap.add_argument("--bootstrap", type=int, default=MIN_TEXTS_CANAL,
                    help="textos al bootstrap con --sin-rebuild (default 3)")
    args = ap.parse_args()

    t0 = time.time()
    filas = replay(_services_dir(args.ref), args.sin_rebuild, args.bootstrap,
                   args.panel_jsonl)
    imprimir(filas)
    modo = f"sin rebuild, bootstrap={args.bootstrap}" if args.sin_rebuild else "rebuild por mensaje"
    print(f"services: {args.ref or 'árbol actual'} | {modo} | {time.time() - t0:.1f}s")
    if args.json:
        Path(args.json).write_text(json.dumps(filas, indent=1))
