"""
stochastic_attractor_eval.py

Aísla seed y n_runs como variables independientes de _count_attractors()
(services/coco.py). No modifica coco.py — llama al método real vía una
instancia de COCO por combinación (seed, n_runs).

Motivación: TASK_stochastic_attractor_eval_v5.md. _count_attractors usa
np.random.default_rng(self._seed) y self._n_runs, ninguno de los dos
parámetro del método — solo configurables al instanciar COCO. n_runs se
comporta como estimador tipo coupon-collector (ver REG_n_runs_sweep_armstrong_v1.md,
n_runs 10->200 sin saturar D_ckm_tail). Este módulo produce distribuciones
raw de A_observed por (seed, n_runs), sin interpretación.

v6 (Ago 2026): _count_attractors llamado con weighted=True.
Distribución de nodos: ponderada por fi = |W_eff|.sum(axis=1).
n_act por reinicio: uniform(0.3, 0.7) * N — no distribución normal.
n_runs_range: checkpoints fijos — no sampleados desde ninguna distribución.

Uso:
    from stochastic_attractor_eval import run_sweep
    run_sweep(W, seeds=[0,1,2], n_runs_range=[10,50], out_dir="...", max_workers=2)
"""

from __future__ import annotations

import fcntl
import json
import os
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np

_SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
if str(_SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(_SERVICES_DIR))

from coco import COCO  # noqa: E402
from firma_ckm import _sha256  # noqa: E402


def run_one(W: np.ndarray, seed: int, n_runs: int, weighted: bool = True) -> dict:
    """
    Unidad de trabajo atómica. Sin I/O.

    Instancia un COCO nuevo (seed y n_runs solo son configurables al
    construir la instancia, _count_attractors() no los recibe como
    parámetros), corre _count_attractors(W), reporta raw.

    weighted: default True desde v6 — el valor usado en la corrida
    registrada en REG_stochastic_eval_v2.md. Es parámetro y no literal
    (v7) para que la llamada, el `run_hash` y el campo `weighted` del
    registro salgan de la misma fuente; poner weighted=False reproduce
    la corrida uniforme de REG_stochastic_eval_v1.md con hashes propios.
    """
    coco = COCO(W=W, seed=seed, n_runs=n_runs)
    t0 = time.perf_counter()
    a_observed = coco._count_attractors(W, weighted=weighted)
    execution_time = time.perf_counter() - t0

    w_sha = _sha256(W)
    # `weighted` entra en el hash (v7): dos corridas con los mismos
    # (seed, n_runs, W) pero distinta distribución de muestreo son
    # observaciones distintas, no la misma repetida. Sin esto, las
    # coincidencias de A_observed entre modos colapsan en el índice
    # (ver REG_stochastic_eval_v2.md §Ejecución, 193 entradas).
    run_hash_input = f"{seed}:{n_runs}:{w_sha}:{a_observed}:weighted={weighted}"
    run_hash = _sha256(np.frombuffer(run_hash_input.encode(), dtype=np.uint8))

    return {
        "seed": seed,
        "n_runs": n_runs,
        "A_observed": a_observed,
        "prng_method": "numpy.default_rng",
        "numpy_version": np.__version__,
        "execution_time": execution_time,
        "process_id": os.getpid(),
        "run_hash": run_hash,
        "W_sha": w_sha,
        "weighted": weighted,
    }


def _write_result(record: dict, jsonl_path: Path, index_path: Path) -> None:
    """
    Sección crítica protegida por fcntl.flock — segura entre procesos no
    relacionados (workers de un pool interno, o invocaciones externas
    separadas apuntando al mismo índice). Serializa solo la escritura,
    no la ejecución de run_one.
    """
    lock_path = Path(str(index_path) + ".lock")
    lock_path.touch(exist_ok=True)

    with open(lock_path, "r+") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            with open(jsonl_path, "a") as f:
                f.write(json.dumps(record) + "\n")

            index = {}
            if index_path.exists() and index_path.stat().st_size > 0:
                index = json.loads(index_path.read_text())

            index[record["run_hash"]] = {
                "seed": record["seed"],
                "n_runs": record["n_runs"],
                "W_sha": record["W_sha"],
                "weighted": record.get("weighted"),
                "status": "completed",
                "jsonl_path": str(jsonl_path),
                "timestamp": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"),
            }
            index_path.write_text(json.dumps(index, indent=2))
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def run_sweep(
    W: np.ndarray,
    seeds: list[int],
    n_runs_range: list[int],
    out_dir: str,
    max_workers: int = 1,
) -> tuple[Path, Path]:
    """
    Corre run_one() sobre el producto cartesiano seeds x n_runs_range.
    max_workers=1 (default): secuencial, sin pool. max_workers>1: pool
    de procesos vía ProcessPoolExecutor — los workers solo computan,
    la escritura queda en el proceso que llama run_sweep.

    Devuelve (jsonl_path, index_path).
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    w_sha8 = _sha256(W)[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    jsonl_path = out / f"runs_{w_sha8}_{timestamp}.jsonl"
    index_path = out / f"index_{w_sha8}.json"

    combinations = [(s, n) for s in seeds for n in n_runs_range]

    interrupted = {"flag": False}

    def _handle_signal(signum, frame):
        interrupted["flag"] = True

    prev_sigterm = signal.signal(signal.SIGTERM, _handle_signal)
    prev_sigint = signal.signal(signal.SIGINT, _handle_signal)

    try:
        if max_workers <= 1:
            for seed, n_runs in combinations:
                if interrupted["flag"]:
                    break
                record = run_one(W, seed, n_runs)
                _write_result(record, jsonl_path, index_path)
        else:
            with ProcessPoolExecutor(max_workers=max_workers) as pool:
                futures = {
                    pool.submit(run_one, W, seed, n_runs): (seed, n_runs)
                    for seed, n_runs in combinations
                }
                for future in as_completed(futures):
                    record = future.result()
                    _write_result(record, jsonl_path, index_path)
                    if interrupted["flag"]:
                        for f in futures:
                            f.cancel()
                        break
    finally:
        signal.signal(signal.SIGTERM, prev_sigterm)
        signal.signal(signal.SIGINT, prev_sigint)

    return jsonl_path, index_path


# ---------------------------------------------------------------------------
# H2 — A0 (W sola) vs A_actual (W+Delta_r), TASK_h2_a0_vs_aactual_v4.md
# ---------------------------------------------------------------------------

H2_CHECKPOINTS = [10, 30, 100, 300, 1000, 3000, 10000]
CONVERGENCIA_SLOPE = 0.10
RIESGO_CONFOUND_RATIO = 0.95
COLAPSO_DIFF_REL = 0.02


def run_pair(
    W       : np.ndarray,
    Delta_r : np.ndarray,
    seed    : int,
    n_runs  : int,
    weighted: bool = True,
) -> dict:
    """
    Compara A0 (sobre W sola) vs A_actual (sobre W+Delta_r), mismo seed
    y n_runs para ambos — comparación pareada, no dos muestras
    independientes. Sin I/O.

    weighted aplica a las DOS mediciones del par, nunca a una sola: la
    comparación es pareada y mezclar modos la rompería. Ver nota en
    run_one sobre por qué es parámetro y no literal.
    """
    coco = COCO(W=W, seed=seed, n_runs=n_runs)
    a0 = coco._count_attractors(W,                weighted=weighted)
    a_actual = coco._count_attractors(W + Delta_r, weighted=weighted)
    delta = a_actual - a0
    d_ckm_instante = (a0 - a_actual) / a0 if a0 > 0 else 0.0

    w_sha = _sha256(W)
    delta_r_sha = _sha256(Delta_r)
    run_hash_input = (
        f"{seed}:{n_runs}:{w_sha}:{delta_r_sha}:{a0}:{a_actual}:weighted={weighted}"
    )
    run_hash = _sha256(np.frombuffer(run_hash_input.encode(), dtype=np.uint8))

    return {
        "seed": seed,
        "n_runs": n_runs,
        "A0": a0,
        "A_actual": a_actual,
        "delta": delta,
        "D_ckm_instante": round(d_ckm_instante, 6),
        "W_sha": w_sha,
        "Delta_r_sha": delta_r_sha,
        "run_hash": run_hash,
        "weighted": weighted,
    }


def _fi_distribution(W: np.ndarray) -> dict:
    """Distribución de frecuencias marginales (row-sums de W) — predicción
    cualitativa de dónde debería saturar representación(k). No interpreta,
    solo reporta CV/skewness para comparar después contra el resultado real."""
    fi = np.abs(W).sum(axis=1)
    mean = float(fi.mean())
    std = float(fi.std())
    cv = std / mean if mean > 0 else None
    skew = float(np.mean(((fi - mean) / std) ** 3)) if std > 0 else None
    return {"mean_fi": mean, "std_fi": std, "cv_fi": cv, "skewness_fi": skew}


def _detect_events(prev: Optional[dict], curr: dict) -> list[dict]:
    events = []
    if prev is not None:
        dn = curr["n_runs"] - prev["n_runs"]
        if dn > 0:
            slope_a0 = (curr["A0"] - prev["A0"]) / dn
            slope_aa = (curr["A_actual"] - prev["A_actual"]) / dn
            which = []
            if slope_a0 < CONVERGENCIA_SLOPE:
                which.append("A0")
            if slope_aa < CONVERGENCIA_SLOPE:
                which.append("A_actual")
            if which:
                events.append({
                    "type": "CONVERGENCIA",
                    "which": which,
                    "slope_A0": round(slope_a0, 4),
                    "slope_A_actual": round(slope_aa, 4),
                })
    ratio_a0 = curr["A0"] / curr["n_runs"]
    ratio_aa = curr["A_actual"] / curr["n_runs"]
    if ratio_a0 < RIESGO_CONFOUND_RATIO or ratio_aa < RIESGO_CONFOUND_RATIO:
        which = []
        if ratio_a0 < RIESGO_CONFOUND_RATIO:
            which.append("A0")
        if ratio_aa < RIESGO_CONFOUND_RATIO:
            which.append("A_actual")
        events.append({
            "type": "RIESGO_CONFOUND_SALIDA",
            "which": which,
            "ratio_A0": round(ratio_a0, 4),
            "ratio_A_actual": round(ratio_aa, 4),
        })
    if curr["A0"] > 0:
        diff_rel = abs(curr["A_actual"] - curr["A0"]) / curr["A0"]
        if diff_rel < COLAPSO_DIFF_REL:
            events.append({"type": "COLAPSO_SENAL", "diff_rel": round(diff_rel, 4)})
    return events


def run_h2_case(
    W: np.ndarray,
    Delta_r: np.ndarray,
    case_id: int,
    count_seeds: list[int],
    checkpoints: list[int],
    jsonl_path: Path,
    index_path: Path,
    weighted  : bool = True,
) -> None:
    """
    Un caso real (W, Delta_r ya construidos) x varios count_seeds x
    checkpoints logarítmicos. CONVERGENCIA corta la corrida de ESA
    combinación (case_id, count_seed) — no sigue a checkpoints mayores.
    RIESGO_CONFOUND y COLAPSO son marcadores, no cortan, y solo se
    registran la primera vez que cruzan (por serie, por combinación).
    """
    fi_pred = _fi_distribution(W)
    for count_seed in count_seeds:
        prev = None
        confound_fired: set[str] = set()
        colapso_fired = False
        for n_runs in checkpoints:
            record = run_pair(W, Delta_r, count_seed, n_runs, weighted=weighted)
            record["case_id"] = case_id
            record["fi_prediction"] = fi_pred

            events = _detect_events(prev, record)
            # RIESGO_CONFOUND y COLAPSO solo la primera vez que cruzan
            filtered = []
            for e in events:
                if e["type"] == "RIESGO_CONFOUND_SALIDA":
                    new_which = [w for w in e["which"] if w not in confound_fired]
                    if not new_which:
                        continue
                    confound_fired.update(new_which)
                    e = {**e, "which": new_which}
                elif e["type"] == "COLAPSO_SENAL":
                    if colapso_fired:
                        continue
                    colapso_fired = True
                filtered.append(e)
            record["events"] = filtered

            _write_result(record, jsonl_path, index_path)
            prev = record

            if any(e["type"] == "CONVERGENCIA" for e in filtered):
                break


def build_case_w_and_delta_r(corpus_state_path: str) -> tuple[np.ndarray, np.ndarray, int]:
    """
    Reconstruye W_case desde el texto real completo de un
    corpus_state.json.bak_* (no truncado, a diferencia de
    monitor_trajectory.jsonl.bak_*), y genera Delta_r_case corriendo
    MonitorService SIN thermostat sobre esos mismos textos, en su
    orden real — Delta_r libre, sin compresión STOP.

    Devuelve (W, Delta_r, n_texts_reales).
    """
    from corpus_service import CorpusService
    from monitor_service import MonitorService
    import tempfile

    state = json.loads(Path(corpus_state_path).read_text())
    texts = state["texts"]

    tmp_corpus = tempfile.mktemp(suffix=".json")
    tmp_traj = tempfile.mktemp(suffix=".jsonl")
    try:
        corpus = CorpusService(storage_path=tmp_corpus, min_texts=3)
        corpus.ingest(texts)
        if corpus.mode != "evaluation":
            raise ValueError(f"{corpus_state_path}: no alcanzó modo evaluation con {len(texts)} textos")
        W = corpus.get_W()

        monitor = MonitorService(corpus, storage_path=tmp_traj, n_runs_attractors=50)
        for i, text in enumerate(texts):
            monitor.evaluate(text, device_id=f"replay_{i:03d}")
        Delta_r = monitor._Delta_r.copy() if monitor._Delta_r is not None else np.zeros_like(W)
        return W, Delta_r, len(texts)
    finally:
        Path(tmp_corpus).unlink(missing_ok=True)
        Path(tmp_traj).unlink(missing_ok=True)


if __name__ == "__main__":
    # Corrida de prueba mínima — ver TASK_stochastic_attractor_eval_v5.md
    import importlib.util

    _REPO_ROOT = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(
        "armstrong_orig",
        _REPO_ROOT / "iap_chatroom/tests/test_armstrong_stop_coco.py",
    )
    orig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(orig)

    sys.path.insert(0, str(_REPO_ROOT / "services"))
    from corpus_service import CorpusService

    _OUT_DIR = _REPO_ROOT / "process/experiments/stochastic_eval"
    _OUT_DIR.mkdir(parents=True, exist_ok=True)

    corpus = CorpusService(
        storage_path=str(_OUT_DIR / "_smoke_corpus_state.json"),
        min_texts=15,
    )
    corpus.ingest(orig.WARMUP_TEXTS)
    W = corpus.get_W()

    jsonl_path, index_path = run_sweep(
        W,
        seeds=[0, 1, 2],
        n_runs_range=[10, 50],
        out_dir=str(_REPO_ROOT / "process/experiments/stochastic_eval"),
        max_workers=2,
    )
    print(f"JSONL: {jsonl_path}")
    print(f"Index: {index_path}")
    print(f"Entradas: {len(json.loads(index_path.read_text()))}")
