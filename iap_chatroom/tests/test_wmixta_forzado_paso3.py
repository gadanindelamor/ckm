"""
test_wmixta_forzado_paso3.py

TASK_armstrong_boltzmann_comparison_wmixta_v5.md — Paso 3.

Corrida del REGIMEN FORZADO (W_pos contrafactico) sobre los 24 textos del
caso IAP 09_run2. Solo el texto de ese caso: ni su Delta_r, ni su W, ni su
historia.

force_w_pos=True saltea el ruteo por marcadores de oposicion en
CorpusService: todos los pares van a pos_counts, W = (pos+neg)/max. El
corpus conserva su tension; el servicio no la codifica. No es un estado
alcanzable por el ciclo natural — la W queda marcada en la traza
(causal_event=rebuild_debug_force_w_pos, forced_w_pos=True).

Objetivo: completitud — observar como funciona COCO y como caen los STOPs
en este regimen. NO es comparacion con corridas anteriores.

Paso 1 ya medido (n_runs=150, seed=42):
    regimen forzado  A0 = 4    piso D_ckm estimado = +0.50  (> threshold 0.40)
    regimen natural  A0 = 58   piso D_ckm estimado = -0.14  (< threshold 0.40)

Parametros de esta corrida: n_runs=50, seed=42, track_landscape=False.

delta_A se calcula en el driver, no via track_landscape: tras un STOP se
cuenta sobre W + Delta_r ya comprimida — identico a lo que COCO hace
internamente, pero 1 relajacion extra en vez de 3 (track_landscape mide
ademas c(S) antes y despues).

Reanudable: cada condicion guarda su propio JSON; al relanzar, las
condiciones ya completas se saltean.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "services"))

from coco import COCO                       # noqa: E402
from corpus_service import CorpusService    # noqa: E402
from monitor_service import MonitorService  # noqa: E402

CASO    = _REPO_ROOT / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"
OUT_DIR = _REPO_ROOT / "process/experiments/wmixta_forzado_paso3"
N_RUNS  = 50
SEED    = 42
REGIMEN = "forzado"
FORCE_W_POS = True

CONDICIONES = [
    ("uniform",        "uniform"),
    ("weighted",       "weighted"),
    ("boltzmann",      "boltzmann"),
    ("sin_thermostat", None),
]


def _done(path: Path, n_esperado: int) -> bool:
    """Condicion completa = JSON existe y tiene todas las evaluaciones."""
    if not path.exists():
        return False
    try:
        d = json.loads(path.read_text())
        return len(d.get("evals", [])) == n_esperado
    except Exception:
        return False


def run_condition(label: str, mode: str | None) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag         = f"{REGIMEN}_{label}"
    result_path = OUT_DIR / f"result_{tag}.json"
    textos      = json.loads(CASO.read_text())["texts"]

    if _done(result_path, len(textos)):
        print(f"    [salteada — ya completa]", flush=True)
        return json.loads(result_path.read_text())

    corpus_path = OUT_DIR / f"corpus_{tag}.json"
    traj_path   = OUT_DIR / f"trajectory_{tag}.jsonl"
    for p in (corpus_path, traj_path, result_path):
        p.unlink(missing_ok=True)

    corpus = CorpusService(storage_path=str(corpus_path), min_texts=3,
                           force_w_pos=FORCE_W_POS)
    corpus.ingest(textos)
    assert corpus.mode == "evaluation", f"{tag}: modo {corpus.mode}"
    W = corpus.get_W()
    assert (W < 0).sum() == 0, f"{tag}: la W forzada no deberia tener negativos"

    th = None
    if mode is not None:
        th = COCO(W=W, n_runs=N_RUNS, seed=SEED, track_landscape=False,
                  sampling_mode=mode)

    monitor = MonitorService(corpus, storage_path=str(traj_path),
                             n_runs_attractors=N_RUNS, thermostat=th)
    smp = th._sampling_kwargs() if th is not None else {}

    evals = []
    for i, text in enumerate(textos):
        panel = monitor.evaluate(text, device_id=f"c09f_{i:02d}")
        t     = panel.get("thermostat")
        hist  = th.history()[-1] if th is not None and th.history() else None

        # delta_A sin track_landscape: A tras la compresion, misma cuenta que
        # COCO haria internamente (1 relajacion extra, no 3).
        delta_A = None
        if t and t["stop_applied"] and hist is not None:
            A_post  = th._count_attractors(th.W + monitor._Delta_r, **smp)
            delta_A = int(A_post - hist.A_current)

        evals.append({
            "i": i,
            "D_ckm_panel"  : panel["D_ckm"],
            "D_ckm_coco"   : t["D_ckm"] if t else None,
            "A_actual"     : hist.A_current if hist else None,
            "A0"           : hist.A0 if hist else None,
            "frac_rec"     : t["frac_rec"] if t else None,
            "zone"         : t["zone"] if t else None,
            "stop_applied" : bool(t["stop_applied"]) if t else False,
            "alpha_used"   : t["alpha_used"] if t else None,
            "delta_A"      : delta_A,
            "Delta_r_sum"  : panel["Delta_r_sum"],
            "c_S"          : panel["c_S"],
            "sampling_mode": t["sampling_mode"] if t else None,
        })

    result = {
        "regimen"      : REGIMEN,
        "force_w_pos"  : FORCE_W_POS,
        "label"        : label,
        "sampling_mode": mode or "sin_thermostat",
        "n_runs"       : N_RUNS,
        "seed"         : SEED,
        "track_landscape": False,
        "N"            : int(W.shape[0]),
        "W_neg"        : int((W < 0).sum()),
        "W_pos"        : int((W > 0).sum()),
        "n_texts"      : len(textos),
        "n_stops"      : sum(1 for e in evals if e["stop_applied"]),
        "timestamp"    : datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"),
        "evals"        : evals,
    }
    result_path.write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    results = []
    for label, mode in CONDICIONES:
        print(f"--- {REGIMEN}/{label} (n_runs={N_RUNS}) ...", flush=True)
        r = run_condition(label, mode)
        results.append(r)
        e0 = r["evals"][0]
        print(f"    W<0={r['W_neg']} STOPs={r['n_stops']}/{r['n_texts']} "
              f"A0={e0['A0']}", flush=True)

    print(f"\n{'modo':<15} {'STOPs':>6} {'A0':>4} {'A_fin':>6} "
          f"{'D_coco_fin':>11} {'D_panel_fin':>12} {'delta_A por STOP'}")
    for r in results:
        e  = r["evals"][-1]
        dA = [x["delta_A"] for x in r["evals"] if x["delta_A"] is not None]
        print(f"{r['label']:<15} {r['n_stops']:>6} {str(e['A0']):>4} "
              f"{str(e['A_actual']):>6} {str(e['D_ckm_coco']):>11} "
              f"{str(e['D_ckm_panel']):>12} {dA}")
    print(f"\nResultados: {OUT_DIR}/result_{REGIMEN}_*.json")


if __name__ == "__main__":
    main()
