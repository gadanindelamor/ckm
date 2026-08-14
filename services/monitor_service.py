"""
monitor_service.py — Collective MonitorService

Stateful. Evalúa prompts contra el corpus acumulado.
Mide fabricación: lo que σ_prompt declaró y el campo rechazó.
        # σ declarado por el prompt
        sigma_prompt = self._extractor.evaluate(text, nodes)

        # σ que el campo acepta
        sigma_relaxed = self._relax(sigma_prompt.copy(), self._combine_W_Delta(W, self._Delta_r))

Combina W y Delta_r en escalas compatibles.
    W ∈ [0,1] (normalizado por CorpusService).
    Delta_r ∈ [0, ∞) (conteos enteros de rechazos).

    Normalización: Delta_r / max(Delta_r) → [0,1],
    luego escala por mean(W_nonzero) para preservar magnitud relativa de W.
    Si Delta es cero (inicio de sesión), devuelve W sin modificar.

Δ acumula co-ocurrencias de rechazos:
  pares (i,j) que σ_prompt declaró activos pero relax expulsó.
  Δ[i,j] += 1 por cada evaluación donde el par fue rechazado.

Integrado a COCO thermostat (Inyectado)

  Limitación v1 (heredada de CorpusService):
  W positiva. c(S) informativo solo cuando hay tensión estructural.

Inicializacion:
    def __init__(
        self,
        corpus          : CorpusService,
        storage_path    : str = "monitor_trajectory.jsonl",
        n_runs_attractors: int = 50,
        thermostat      : Optional[COCO] = None,
    ):
        self.corpus    = corpus
        self._storage  = Path(storage_path)
        self._extractor = NodeExtractorService()
        self._n_runs   = n_runs_attractors
        self._thermostat = thermostat

        self._Delta_r : Optional[np.ndarray] = None
        self._A0    : Optional[int]        = None

  """

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional

import numpy as np

from node_extractor import NodeExtractorService
from corpus_service  import CorpusService
from coco import COCO, ThermostatState

try:
    from behavior_graph import BehaviorGraph as _BehaviorGraph
    _HAS_G = True
except ImportError:
    _HAS_G = False


class MonitorService:

    def __init__(
        self,
        corpus          : CorpusService,
        storage_path    : str = "monitor_trajectory.jsonl",
        n_runs_attractors: int = 50,
        thermostat      : Optional[COCO] = None,
        behavior_graph  : Optional[object] = None,   # BehaviorGraph | None
    ):
        self.corpus    = corpus
        self._storage  = Path(storage_path)
        self._extractor = NodeExtractorService()
        self._n_runs   = n_runs_attractors
        self._thermostat = thermostat
        self._g         = behavior_graph

        self._Delta_r : Optional[np.ndarray] = None
        self._A0    : Optional[int]        = None

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def evaluate(self, text: str, device_id: Optional[str] = None) -> Optional[dict]:
        """
        Evalúa un prompt. Devuelve panel o None si corpus en acumulación.
        """
        if self.corpus.mode == "accumulation":
            return {"mode": "accumulation", "message": "corpus insuficiente — guardando traza"}

        W     = self.corpus.get_W()
        nodes = self.corpus.get_nodes()
        N     = len(nodes)

        if self._Delta_r is None or self._Delta_r.shape != (N, N):
            self._Delta_r = np.zeros((N, N))

        # σ declarado por el prompt
        sigma_prompt = self._extractor.evaluate(text, nodes)

        # σ que el campo acepta
        sigma_relaxed = self._relax(sigma_prompt.copy(), self._combine_W_Delta(W, self._Delta_r))

        # pares rechazados → acumular en Δ
        rejected = self._rejected_pairs(sigma_prompt, sigma_relaxed)
        for i, j in rejected:
            self._Delta_r[i, j] += 1
            self._Delta_r[j, i] += 1

        # métricas
        c_s   = self._cS(sigma_relaxed, W)
        fi    = self._fabrication_index(sigma_prompt, sigma_relaxed)
        D_ckm = self._D_ckm(W)

        # G_state — paralelo a {W, Δ_W}, no retroactivo
        g_state_panel = None
        if self._g is not None:
            self._g.ingest([text])
            g_state_panel = self._g.g_state()
            g_state_panel["active_behavior"] = self._g.active_nodes(text)

        panel = {
            "c_S"              : round(c_s,  6),
            "fabrication_index": round(fi,   4),
            "D_ckm"            : round(D_ckm, 4),
            "n_rejected_pairs" : len(rejected),
            "Delta_r_sum"        : float(np.sum(self._Delta_r)),
            "activos_prompt"   : [nodes[i] for i, s in enumerate(sigma_prompt)   if s > 0],
            "activos_relajado" : [nodes[i] for i, s in enumerate(sigma_relaxed)  if s > 0],
            "rechazados"       : [(nodes[i], nodes[j]) for i, j in rejected],
            "thermostat"       : None,
            "G_state"          : g_state_panel,
        }

        # thermostat observa el Delta acumulado real
        # sincroniza _Delta solo si STOP fue aplicado — si no, divergen libremente
        if self._thermostat is not None:
            if device_id is not None:
                self._thermostat.register_device_eval(device_id, fi)
            ts = self._thermostat.observe(self._Delta_r)
            if ts.stop_applied:
                self._Delta_r = self._thermostat.delta_state()
            panel["thermostat"] = {
                "zone"        : ts.zone,
                "D_ckm"       : ts.D_ckm,
                "frac_rec"    : ts.frac_rec,
                "stop_applied": ts.stop_applied,
                "alpha_used"  : ts.alpha_used,
                "beta"        : self._thermostat.beta_status(),
                "temp_signal" : self._thermostat.temp_signal(),
                "landscape_delta": getattr(self._thermostat, "_last_landscape_delta", None),
                "landscape_component": (
                    self._thermostat._last_landscape_component
                    if getattr(self._thermostat, "_track_landscape", False)
                    else None
                ),
                "gamma"  : getattr(self._thermostat, "_gamma", None),
                "n_runs" : getattr(self._thermostat, "_n_runs", None),
            }

        self._persist(text, panel, device_id)
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

        Normalización: Delta_r / max(Delta_r) → [0,1],
        luego escala por mean(W_nonzero) para preservar magnitud relativa de W.
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
        Delta    = self._Delta_r if self._Delta_r is not None else np.zeros_like(W)
        W_eff    = self._combine_W_Delta(W, Delta)
        A_actual = self._count_attractors(W_eff)
        if self._A0 is None:
            if A_actual == 0:
                return 0.0   # corpus vacío — diferir A0
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

    def _persist(self, text: str, panel: dict, device_id: Optional[str] = None) -> None:
        t = len(self.trajectory())
        with open(self._storage, "a") as f:
            f.write(
                json.dumps({"t": t, "device_id": device_id, "text": text[:80], "panel": panel})
                + "\n"
            )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile, os
    from coco import COCO

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
    print(f"T1 corpus: {corpus.status()}")
    assert corpus.mode == "evaluation", "FAIL T1"

    # T2 — sin thermostat: panel["thermostat"] == None
    monitor = MonitorService(corpus, storage_path=tmp_monitor)
    r = monitor.evaluate("gun control laws reduce violence")
    assert r["thermostat"] is None, "FAIL T2"
    print("T2 OK — sin thermostat, panel['thermostat']=None")

    os.unlink(tmp_monitor)
    tmp_monitor = tempfile.mktemp(suffix=".jsonl")

    # T3 — con thermostat: panel incluye zone y beta
    th = COCO(W=corpus.get_W(), n_runs=30, seed=0)
    monitor2 = MonitorService(corpus, storage_path=tmp_monitor, thermostat=th)

    prompts = [
        ("gun control laws reduce violence",           "deviceA"),
        ("chocolate ice cream prevents gun violence",  "deviceB"),  # fabricado
        ("rights protected by constitution",           "deviceA"),
        ("mental health backgrosund checks reduce crime","deviceB"),
    ]

    print("\n=== T3 evaluaciones con thermostat + device_id ===")
    for text, device in prompts:
        r = monitor2.evaluate(text, device_id=device)
        ts = r["thermostat"]
        print(f"  [{device}] fi={r['fabrication_index']}  zone={ts['zone']}  betsa={ts['beta']['devices']}")

    # T4 — beta_status refleja historial por device
    beta = th.beta_status()
    assert "deviceA" in beta["devices"] or "deviceB" in beta["devices"]
    print(f"\nT4 OK — beta_status: {beta}")

    # T5 — _Delta diverge libremente sin STOP
    d_monitor  = monitor2._Delta_r.sum()
    d_thermo   = th.delta_state().sum()
    print(f"\nT5 Delta — monitor={d_monitor:.4f}  thermostat={d_thermo:.4f}")
    print(f"   divergen={'SI' if abs(d_monitor - d_thermo) > 1e-6 else 'NO (ambos en 0)'}")

    # T6 — stop_signal independiente del thermostat
    sig = monitor2.stop_signal()
    assert "signal" in sig and "direction" in sig, "FAIL T6"
    print(f"\nT6 OK — stop_signal: {sig}")

    os.unlink(tmp_corpus)
    os.unlink(tmp_monitor)
    print("\nTodos los tests OK")
