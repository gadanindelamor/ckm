"""
test_armstrong_stop_coco.py
Primera observación in-vivo de OPERADOR_STOP_COCO en pipeline real
MonitorService -> COCO -> compresión Delta_r -> MonitorService adopta.

Especificación: iap_chatroom/tests/TASK_armstrong_stop_coco_v1.md
No toca IAP/MCP — instancia CorpusService/MonitorService/COCO
directamente, sobre el corpus real (W_ckm_corpus_v2.json vía precarga).

NO MODIFICAR: agent_device_skin.py, groq_research_agent.py,
corpus_service.py, coco.py, monitor_service.py. Solo lectura + inyección.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SERVICES_DIR = _REPO_ROOT / "services"
if str(_SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(_SERVICES_DIR))

from corpus_service import CorpusService  # noqa: E402
from monitor_service import MonitorService  # noqa: E402
from coco import COCO  # noqa: E402  (post-refactoring R1)

CORPUS_PATH = str(_REPO_ROOT / "process/experiments/armstrong_corpus_state.json")
OUTPUT_PATH = str(_REPO_ROOT / "process/experiments/armstrong_stop_coco_v1.jsonl")

# Textos de precarga — párrafos cortos de los informes CKM
# Suficientes para pasar modo evaluación (min_texts=15)
WARMUP_TEXTS = [
    "CKM is a formal model for knowledge graph dynamics in multi-agent systems.",
    "W is a symmetric co-occurrence weight matrix encoding structural memory.",
    "Delta is an asymmetric directional dependency matrix encoding inference orientation.",
    "The cohesion measure c(S) equals the mean of W_ij times sigma_i times sigma_j over all pairs.",
    "W and Delta must be kept strictly separate. Mixing them destroys attractor recovery.",
    "The gatekeeper R15 applies four simultaneous orthogonal conditions: C1 C2 C3 C4.",
    "C3 is the M.M criterion: MENTIRIIS MORIERIS. A node that lies about its dependencies fails.",
    "Hopfield relaxation finds attractor states by minimizing the energy function over W.",
    "D_ckm measures change in attractor diversity relative to baseline A0.",
    "Negative D_ckm means the field gained attractors — expansion, not error.",
    "COCO is an ODA device: it observes Delta_r and acts by compressing it.",
    "OPERADOR_STOP_COCO compresses Delta_r by alpha between 0.05 and 0.30.",
    "MonitorService adopts the compressed Delta_r from COCO when stop_applied is True.",
    "FirmaService certifies the structural state with six canonical fields including sha256 of W.",
    "WVersionManager records when W changed using sha256 trace without copying the matrix.",
    "BehaviorGraph G operates on a fixed termap of 18 behavior categories.",
    "D_G measures behavioral drift from G_ref — parallel to D_ckm, not summable with it.",
    "The IAP Chatroom operates under BROADCAST condition: all messages reach all devices.",
    "Coupled silence: a device that does not read still depends on the channel for timing.",
    "STOP never produces loss. Fraccion_rec is greater than or equal to 1.0 in all cases.",
]

# Nota (Armstrong, adaptación tras primer intento fallido — ver
# REG_armstrong_stop_coco_v1.md): la estrategia original del task
# ("vocabulario ajeno al corpus") no puede disparar STOP. fi mide
# NODOS rechazados (declared==0 -> fi=0.0 por guarda explícita en
# _fabrication_index; con un solo nodo activo, fi puede saturar a 1.0
# de forma vacía), pero Delta_r solo acumula PARES rechazados
# (_rejected_pairs requiere >=2 nodos co-activos). Vocabulario
# completamente ajeno activa como máximo 1 nodo del corpus (verificado:
# max 1/texto en el primer intento) -> nunca hay par que rechazar ->
# Delta_r se queda en 0 sin importar cuánto fi vacío se acumule. Es la
# misma propiedad ya documentada en REG_monitor_ckm_v2.md ("el campo no
# puede rechazar lo que no conoce" — caso "chocolate ice cream").
#
# Reemplazo: reusar los 20 nodos reales extraídos del corpus
# (verificado con CorpusService.get_nodes() antes de escribir esto:
# d_ckm, attractor, all, delta_r, matrix, over, measures,
# "about dependencies", applies, delta, "matrix encoding", encoding,
# device, coco, operates, structural, sha, times, summable, cases) en
# combinaciones nuevas — pares de nodos reales que nunca co-ocurrieron
# en los 20 textos de precarga originales (cada uno viene de una
# oración distinta y no relacionada), para forzar rechazos reales en
# la relajación de Hopfield en vez de activación nula.
TEXTS = [
    "Coco applies sha over all structural cases, summable times attractor encoding delta_r.",
    "The device matrix operates about dependencies, d_ckm times attractor over structural delta.",
    "Structural attractor measures coco device sha, matrix encoding applies over all cases.",
    "Delta_r summable times encoding operates about dependencies over structural d_ckm.",
    "All cases applies over matrix encoding, coco device attractor times structural sha.",
    "Measures d_ckm structural delta_r, coco applies over matrix encoding about dependencies.",
    "The attractor operates summable times over structural device sha, all cases matrix.",
    "Coco device delta_r measures structural attractor, matrix encoding applies over all times.",
    "Sha operates about dependencies over structural matrix, d_ckm attractor summable cases.",
    "Structural coco applies delta_r over matrix encoding, device attractor times all measures.",
    "Delta operates structural attractor over matrix, coco sha applies summable times cases.",
    "The matrix encoding measures d_ckm over structural device, coco attractor applies all times.",
    "Structural sha operates coco device over matrix, attractor delta_r summable about dependencies.",
    "All cases structural attractor over matrix encoding, delta_r coco applies device times.",
    "Coco measures structural device sha, matrix encoding operates delta_r over all attractor.",
    "Structural matrix applies over coco device, attractor delta_r summable times encoding cases.",
    "The device coco operates structural sha over matrix, attractor applies delta_r all times.",
    "Matrix encoding structural attractor measures coco, delta_r operates over device sha cases.",
    "Structural delta_r applies coco over matrix, device attractor sha summable times encoding.",
    "Coco device structural matrix operates attractor over delta_r, sha applies all times cases.",
]


def main():
    # 1. Construir corpus desde precarga CKM (fase acumulación → evaluación)
    corpus = CorpusService(storage_path=CORPUS_PATH, min_texts=15)
    corpus.ingest(WARMUP_TEXTS)
    print(f"Corpus post-precarga: {corpus.status()}")
    assert corpus.mode == "evaluation", f"FAIL: corpus en modo {corpus.mode} — revisar min_texts"

    W = corpus.get_W()
    print(f"W shape: {W.shape}, mean: {W.mean():.6f}")

    # 2. Instanciar COCO con W establecida
    th = COCO(W=W, n_runs=50, seed=42, track_landscape=True)
    print(f"β_c_corpus: {th.beta_c_corpus():.4f}")

    # 3. Instanciar MonitorService CON thermostat inyectado
    monitor = MonitorService(
        corpus,
        storage_path=OUTPUT_PATH,
        n_runs_attractors=50,
        thermostat=th,
    )
    print("MonitorService instanciado con thermostat.")
    print("Iniciando evaluaciones...\n")

    stops_observed = []
    delta_r_history = []

    for i, text in enumerate(TEXTS):
        dr_before = float(monitor._Delta_r.sum()) if monitor._Delta_r is not None else 0.0

        panel = monitor.evaluate(text, device_id=f"test_{i:02d}")

        dr_after = float(monitor._Delta_r.sum()) if monitor._Delta_r is not None else 0.0
        ts = panel.get("thermostat", {}) or {}

        stop = ts.get("stop_applied", False)
        alpha = ts.get("alpha_used")
        zone = ts.get("zone", "?")
        d_ckm = panel.get("D_ckm", 0)
        fi = panel.get("fabrication_index", 0)
        temp = ts.get("temp_signal", "?")

        delta_r_history.append({"t": i, "before": dr_before, "after": dr_after, "stop": stop})

        flag = "*** ARMSTRONG ***" if stop else ""
        print(f"t={i:2d}  fi={fi:.3f}  D_ckm={d_ckm:.4f}  zone={zone:12s}  "
              f"temp={str(temp):8s}  Δ_r {dr_before:.0f}→{dr_after:.0f}  "
              f"stop={stop}  α={alpha}  {flag}")

        if stop:
            stops_observed.append({
                "t": i,
                "text_preview": text[:60],
                "D_ckm": d_ckm,
                "fi": fi,
                "zone": zone,
                "temp_signal": temp,
                "alpha_used": alpha,
                "Delta_r_before": dr_before,
                "Delta_r_after": dr_after,
                "compression_ratio": round(dr_after / dr_before, 4) if dr_before > 0 else None,
            })

    print("\n=== RESULTADO ===")
    print(f"STOPs observados: {len(stops_observed)}/{len(TEXTS)}")

    if stops_observed:
        print("\nPrimer ARMSTRONG:")
        print(json.dumps(stops_observed[0], indent=2))
        print("\nFracción_rec = compression_ratio (debería ser ≥ 1.0 por REG_destruccion_recuperacion)")
    else:
        print("STOP no disparó. Verificar: D_ckm alcanzó 0.40? Ver trayectoria en OUTPUT_PATH.")
        print("Considerar: agregar más textos o textos con mayor fi.")

    # Guardar delta_r history
    summary_path = Path(OUTPUT_PATH).parent / "armstrong_delta_r_history.json"
    summary_path.write_text(json.dumps(delta_r_history, indent=2))
    print(f"\nHistorial Δ_r guardado: {summary_path}")
    print(f"Trayectoria completa: {OUTPUT_PATH}")


# ---------------------------------------------------------------------------
# TEXTO COMPLETO EN JSONL — modo debug
# ---------------------------------------------------------------------------
# _persist() en monitor_service.py trunca texto a 80 chars.
# Para este experimento: monkey-patch local, sin tocar el servicio.
#
# Agregar esto DESPUÉS de instanciar monitor, ANTES del loop:
#
#   def _persist_full(self, text, panel, device_id=None):
#       t = len(self.trajectory())
#       with open(self._storage, "a") as f:
#           f.write(json.dumps({
#               "t": t, "device_id": device_id,
#               "text": text,              # completo, sin truncar
#               "panel": panel
#           }) + "\n")
#
#   monitor._persist = _persist_full.__get__(monitor, MonitorService)
#
# NO modificar monitor_service.py.

if __name__ == "__main__":
    main()
