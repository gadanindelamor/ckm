"""
monitor_service.py — MonitorService

Stateful. Evalúa prompts contra el corpus acumulado.
Mide fabricación: lo que σ_prompt declaró y el campo rechazó.

Δ acumula co-ocurrencias de rechazos:
  pares (i,j) que σ_prompt declaró activos pero relax expulsó.
  Δ[i,j] += 1 por cada evaluación donde el par fue rechazado.

Limitación v1 (heredada de CorpusService):
  W positiva. c(S) informativo solo cuando hay tensión estructural.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional

import numpy as np

from node_extractor import NodeExtractorService
from corpus_service  import CorpusService


class MonitorService:

    def __init__(
        self,
        corpus          : CorpusService,
        storage_path    : str = "monitor_trajectory.jsonl",
        n_runs_attractors: int = 50,
    ):
        self.corpus    = corpus
        self._storage  = Path(storage_path)
        self._extractor = NodeExtractorService()
        self._n_runs   = n_runs_attractors

        self._Delta : Optional[np.ndarray] = None   # acumulado de rechazos
        self._A0    : Optional[int]        = None   # atractores en t=0

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def evaluate(self, text: str) -> Optional[dict]:
        """
        Evalúa un prompt. Devuelve panel o None si corpus en acumulación.
        """
        if self.corpus.mode == "accumulation":
            return {"mode": "accumulation", "message": "corpus insuficiente — guardando traza"}

        W     = self.corpus.get_W()
        nodes = self.corpus.get_nodes()
        N     = len(nodes)

        if self._Delta is None:
            self._Delta = np.zeros((N, N))

        # σ declarado por el prompt
        sigma_prompt = self._extractor.evaluate(text, nodes)

        # σ que el campo acepta
        sigma_relaxed = self._relax(sigma_prompt.copy(), self._combine_W_Delta(W, self._Delta))

        # pares rechazados → acumular en Δ
        rejected = self._rejected_pairs(sigma_prompt, sigma_relaxed)
        for i, j in rejected:
            self._Delta[i, j] += 1
            self._Delta[j, i] += 1

        # métricas
        c_s   = self._cS(sigma_relaxed, W)
        fi    = self._fabrication_index(sigma_prompt, sigma_relaxed)
        D_ckm = self._D_ckm(W)

        panel = {
            "c_S"              : round(c_s,  6),
            "fabrication_index": round(fi,   4),
            "D_ckm"            : round(D_ckm, 4),
            "n_rejected_pairs" : len(rejected),
            "Delta_sum"        : float(np.sum(self._Delta)),
            "activos_prompt"   : [nodes[i] for i, s in enumerate(sigma_prompt)   if s > 0],
            "activos_relajado" : [nodes[i] for i, s in enumerate(sigma_relaxed)  if s > 0],
            "rechazados"       : [(nodes[i], nodes[j]) for i, j in rejected],
        }

        self._persist(text, panel)
        return panel

    def trajectory(self) -> list:
        if not self._storage.exists():
            return []
        with open(self._storage) as f:
            return [json.loads(l) for l in f if l.strip()]

    def stop_signal(self, window: int = 5) -> dict:
        traj = self.trajectory()
        if len(traj) < 2:
            return {"signal": False, "reason": "trayectoria insuficiente"}

        recent   = traj[-window:]
        fi_vals  = [r["panel"]["fabrication_index"] for r in recent]
        D_vals   = [r["panel"]["D_ckm"]             for r in recent]
        fi_trend = fi_vals[-1] - fi_vals[0]
        D_trend  = D_vals[-1]  - D_vals[0]
        signal   = fi_trend > 0.05 and D_trend > 0.02

        return {
            "signal"   : signal,
            "fi_trend" : round(fi_trend, 4),
            "D_trend"  : round(D_trend,  4),
            "direction": "CONVERGING" if fi_trend < -0.05 else "DIVERGING" if signal else "STABLE",
        }

    # ------------------------------------------------------------------
    # Operaciones internas
    # ------------------------------------------------------------------

    def _relax(self, sigma: np.ndarray, W: np.ndarray, max_iter: int = 100) -> np.ndarray:
        for _ in range(max_iter):
            h  = W @ sigma
            s2 = np.where(h > 0, 1., np.where(h < 0, -1., sigma))
            if np.allclose(s2, sigma):
                break
            sigma = s2
        return sigma

    def _combine_W_Delta(self, W: np.ndarray, Delta: np.ndarray) -> np.ndarray:
        """
        Combina W y Delta_r en escalas compatibles.

        W ∈ [0,1] (normalizado por CorpusService).
        Delta_r ∈ [0, ∞) (conteos enteros de rechazos).

        Normalización: Delta_r / max(Delta_r) para llevarlo a [0,1]
        antes de escalar por mean(W_nonzero), preservando la magnitud
        relativa de W como referencia de escala.

        Si Delta es cero (inicio de sesión), devuelve W sin modificar.
        """
        delta_max = Delta.max()
        if delta_max == 0:
            return W
        W_nonzero = W[W > 0]
        scale = W_nonzero.mean() if len(W_nonzero) > 0 else 1.0
        Delta_norm = (Delta / delta_max) * scale
        return W + Delta_norm

    def _rejected_pairs(self, sigma_p: np.ndarray, sigma_r: np.ndarray):
        """Pares que sigma_prompt declaró activos pero relax expulsó."""
        declared = np.where(sigma_p > 0)[0]
        rejected_nodes = set(np.where(sigma_r < 0)[0])
        pairs = []
        for i in range(len(declared)):
            for j in range(i + 1, len(declared)):
                ni, nj = declared[i], declared[j]
                if ni in rejected_nodes or nj in rejected_nodes:
                    pairs.append((int(ni), int(nj)))
        return pairs

    def _cS(self, sigma: np.ndarray, W: np.ndarray) -> float:
        ii, jj = np.triu_indices(len(sigma), k=1)
        return float(np.mean(W[ii, jj] * sigma[ii] * sigma[jj]))

    def _fabrication_index(self, sigma_p: np.ndarray, sigma_r: np.ndarray) -> float:
        """Fracción de nodos declarados activos que fueron rechazados."""
        declared = (sigma_p > 0).sum()
        if declared == 0:
            return 0.0
        rejected = ((sigma_p > 0) & (sigma_r < 0)).sum()
        return float(rejected / declared)

    def _D_ckm(self, W: np.ndarray) -> float:
        """D_ckm = (A0 - A_actual) / A0. Puede ser negativo.

        A0 se fija en la primera llamada con corpus establecido (mode != accumulation).
        Se usa _combine_W_Delta para escala compatible W + Delta_r.
        """
        Delta    = self._Delta if self._Delta is not None else np.zeros_like(W)
        W_eff    = self._combine_W_Delta(W, Delta)
        A_actual = self._count_attractors(W_eff)
        if self._A0 is None:
            if A_actual == 0:
                return 0.0  # corpus vacío — diferir A0
            self._A0 = A_actual
        return float((self._A0 - A_actual) / self._A0) if self._A0 > 0 else 0.0

    def _count_attractors(self, W: np.ndarray) -> int:
        N   = W.shape[0]
        rng = np.random.default_rng(0)
        attractors = set()
        for _ in range(self._n_runs):
            n_act = max(1, int(round(rng.uniform(0.3, 0.7) * N)))
            s0    = np.full(N, -1.)
            s0[rng.choice(N, n_act, replace=False)] = 1.
            attractors.add(tuple(self._relax(s0, W).tolist()))
        return len(attractors)

    def _persist(self, text: str, panel: dict) -> None:
        t = len(self.trajectory())
        with open(self._storage, "a") as f:
            f.write(json.dumps({"t": t, "text": text[:80], "panel": panel}) + "\n")


# ---------------------------------------------------------------------------
# Test mínimo — loop completo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile, os

    tmp_corpus  = tempfile.mktemp(suffix=".json")
    tmp_monitor = tempfile.mktemp(suffix=".jsonl")

    # 1. Construir corpus
    corpus = CorpusService(storage_path=tmp_corpus, min_texts=5, top_k=10)
    corpus.ingest([
        "gun control reduces violence and saves lives",
        "the second amendment protects the right to bear arms",
        "background checks prevent criminals from buying weapons",
        "assault weapons bans reduce mass shootings",
        "gun rights are constitutional rights not subject to restriction",
        "mental health is the real cause of gun violence",
        "armed citizens deter crime and protect communities",
    ])
    print(f"Corpus: {corpus.status()}")

    # 2. Monitorear prompts nuevos
    monitor = MonitorService(corpus, storage_path=tmp_monitor)

    prompts = [
        "gun control laws reduce violence in communities",           # coherente con corpus
        "chocolate ice cream prevents all forms of gun violence",    # fabricado — chocolate no tiene historia
        "rights and weapons are protected by the constitution",      # coherente
        "mental health background checks reduce crime rates",        # parcialmente coherente
    ]

    print("\n=== EVALUACIONES ===")
    for p in prompts:
        result = monitor.evaluate(p)
        print(f"\n› {p[:60]}")
        print(f"  fi={result['fabrication_index']}  c_S={result['c_S']}  rechazados={result['rechazados']}")

    print(f"\n=== STOP SIGNAL ===")
    print(monitor.stop_signal())

    os.unlink(tmp_corpus)
    os.unlink(tmp_monitor)
