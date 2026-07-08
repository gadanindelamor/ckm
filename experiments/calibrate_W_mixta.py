"""
calibrate_W_mixta.py
====================
Calibra AMP -> A0 para W_mixta (N=32, 3 pares negativos).
Verifica anclas documentadas y genera sweep completo AMP=0..80.

PROTOCOLO _count_attractors (mismo que coco_thermostat.py):
  rho ~ U(0.3, 0.7), n_act = round(rho*N)
  sigma0: n_act nodos en +1, resto -1
  relax sincronico: h=W@sigma, sign con empate->mantiene
  A0 = |{atractores distintos}| sobre N_RUNS corridas

PARAMETROS:
  SEED=42, N_RUNS=150
  W_base: W_ckm_corpus_v2.json
  Pares negativos: (13,22) cohesion_fabricada<->M_M
                   (15,16) atractor_espurio<->portero
                   (18,20) sentido_comun<->inconmensurabilidad
  W_mixta[i,j] = -W_base[i,j] * AMP

ANCLAS DOCUMENTADAS:
  AMP=0  -> A0=2   (REG_sweep_stop_perdida_v2.md)
  AMP=15 -> A0=5   (REG_sweep_stop_perdida_v2.md, REG_sweep_stop_g1_operativo_v1.md)
  AMP=40 -> A0=25  (sweep_amp40_results.json)

Uso:
  python calibrate_W_mixta.py [--log calibrate_W_mixta.log]

Output:
  calibrate_W_mixta.json  — resultados completos
  calibrate_W_mixta.log   — log con timestamps
"""

from __future__ import annotations
import json
import argparse
import sys
from datetime import datetime
from pathlib import Path

import numpy as np


# ── Parametros ──────────────────────────────────────────────────────────────
SEED      = 42
N_RUNS    = 150
MAX_ITER  = 200
NEG_PAIRS = [(13, 22), (15, 16), (18, 20)]
AMP_SWEEP = list(range(0, 85, 5))

ANCHORS = {0: 2, 15: 5, 40: 25}

W_BASE_CANDIDATES = [
    Path("W_ckm_corpus_v2.json"),
    Path("../W_ckm_corpus_v2.json"),
    Path(__file__).parent / "W_ckm_corpus_v2.json",
    Path(__file__).parent.parent / "W_ckm_corpus_v2.json",
]


# ── Logger ───────────────────────────────────────────────────────────────────
class Logger:
    def __init__(self, log_path: str):
        self._path = Path(log_path)
        self._f    = open(self._path, "w", buffering=1)
        self._start = datetime.now()

    def log(self, msg: str = ""):
        ts  = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        self._f.write(line + "\n")

    def close(self):
        elapsed = (datetime.now() - self._start).total_seconds()
        self.log(f"Tiempo total: {elapsed:.1f}s")
        self._f.close()


# ── Hopfield ─────────────────────────────────────────────────────────────────
def relax(sigma: np.ndarray, W: np.ndarray, max_iter: int = MAX_ITER) -> np.ndarray:
    for _ in range(max_iter):
        h  = W @ sigma
        s2 = np.where(h > 0, 1., np.where(h < 0, -1., sigma))
        if np.allclose(s2, sigma):
            break
        sigma = s2
    return sigma


def count_attractors(W: np.ndarray, seed: int = SEED, n_runs: int = N_RUNS) -> int:
    N   = W.shape[0]
    rng = np.random.default_rng(seed)
    attractors: set = set()
    for _ in range(n_runs):
        rho   = rng.uniform(0.3, 0.7)
        n_act = max(1, int(round(rho * N)))
        s0    = np.full(N, -1.)
        s0[rng.choice(N, n_act, replace=False)] = 1.
        attractors.add(tuple(relax(s0, W).tolist()))
    return len(attractors)


# ── Construccion W_mixta ──────────────────────────────────────────────────────
def build_W_mixta(W_base: np.ndarray, amp: float) -> np.ndarray:
    W = W_base.copy()
    if amp > 0:
        for i, j in NEG_PAIRS:
            W[i, j] = -W_base[i, j] * amp
            W[j, i] = -W_base[i, j] * amp
    return W


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log", default="calibrate_W_mixta.log")
    parser.add_argument("--out", default="calibrate_W_mixta.json")
    args = parser.parse_args()

    log = Logger(args.log)
    log.log(f"calibrate_W_mixta.py  SEED={SEED}  N_RUNS={N_RUNS}  neg_pairs={NEG_PAIRS}")
    log.log()

    # ── Cargar W_base ─────────────────────────────────────────────────────
    W_base_path = None
    for c in W_BASE_CANDIDATES:
        if c.exists():
            W_base_path = c
            break
    if W_base_path is None:
        log.log(f"ERROR: W_ckm_corpus_v2.json no encontrado. Candidatos: {W_BASE_CANDIDATES}")
        sys.exit(1)

    data   = json.loads(W_base_path.read_text())
    W_base = np.array(data["W"])
    N      = W_base.shape[0]
    log.log(f"W_base: {W_base_path}  N={N}  nonzero={np.count_nonzero(W_base)}")
    log.log()

    # ── PASO 1: Verificar anclas ──────────────────────────────────────────
    log.log("=" * 60)
    log.log("PASO 1 — verificacion de anclas documentadas")
    log.log(f"{'AMP':>5}  {'A0_obtenido':>12}  {'A0_esperado':>12}  {'match':>6}")
    log.log("-" * 42)

    anchor_results = {}
    all_match = True
    for amp, expected in sorted(ANCHORS.items()):
        W   = build_W_mixta(W_base, amp)
        A0  = count_attractors(W)
        match = (A0 == expected)
        all_match = all_match and match
        log.log(f"{amp:5d}  {A0:12d}  {expected:12d}  {'OK' if match else 'NO MATCH':>6}")
        anchor_results[amp] = {"A0": A0, "expected": expected, "match": match}

    log.log()
    log.log(f"Anclas: {'TODAS OK' if all_match else 'HAY DISCREPANCIAS — revisar protocolo'}")
    log.log()

    # ── PASO 2: Sweep AMP ────────────────────────────────────────────────
    log.log("=" * 60)
    log.log(f"PASO 2 — sweep AMP {AMP_SWEEP[0]}..{AMP_SWEEP[-1]}  (paso 5)")
    log.log(f"{'AMP':>5}  {'A0':>6}  {'nota':>20}")
    log.log("-" * 36)

    sweep_results = {}
    prev_A0 = None
    for amp in AMP_SWEEP:
        W   = build_W_mixta(W_base, amp)
        A0  = count_attractors(W)
        nota = ""
        if amp in ANCHORS:
            nota = f"<- ancla({ANCHORS[amp]})"
        if prev_A0 is not None and abs(A0 - prev_A0) >= 20:
            nota += " <-- SALTO"
        log.log(f"{amp:5d}  {A0:6d}  {nota}")
        sweep_results[amp] = A0
        prev_A0 = A0

    # ── Guardar resultados ───────────────────────────────────────────────
    output = {
        "meta": {
            "seed": SEED, "n_runs": N_RUNS, "max_iter": MAX_ITER,
            "neg_pairs": NEG_PAIRS, "W_base": str(W_base_path), "N": N,
        },
        "anchors": anchor_results,
        "sweep": sweep_results,
    }
    Path(args.out).write_text(json.dumps(output, indent=2))
    log.log()
    log.log(f"Guardado: {args.out}")
    log.close()


if __name__ == "__main__":
    main()
