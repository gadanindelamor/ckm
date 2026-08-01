"""
behavior_graph.py — BehaviorGraph (G)

Grafo de comportamiento en paralelo a W (CorpusService).

Diferencia clave respecto a CorpusService:
  - Termap FIJO (vocabulario de comportamiento conocido)
  - Detección por presencia léxica, no TF-IDF
  - Mismo mecanismo de construcción de matriz y D_G

Diseñado para:
  - IAP Chatroom corpus (inglés, por defecto post-caso-0.14)
  - N pequeño (~20 nodos) — complementario a W (N=32)
  - Corre en paralelo: los textos que ingresan a W también ingresan a G

Uso:
    g = BehaviorGraph()
    g.ingest(["I will wait for Tinker's map", "OP_SILENCE", "acknowledge"])
    print(g.status())
    print(g.d_g())     # D_G escalar, análogo a D_ckm

Jul 2026 — gadanin.delamor + Claude Sonnet 4.6
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Optional, Dict, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Termap de comportamiento — fijo, versionado explícitamente
# ---------------------------------------------------------------------------

BEHAVIOR_TERMAP_V1: Dict[str, List[str]] = {
    # ---- Protocolo de silencio ----
    "silence":     ["op_silence", "silence", "silent"],
    "wait":        ["wait", "waiting", "hold on", "stand by", "standby"],
    "hold":        ["hold", "holding", "pause", "pausing"],
    "pending":     ["pending", "not yet", "not ready", "hasn't"],

    # ---- Coordinación ----
    "acknowledge": ["acknowledge", "acknowledged", "understood", "received",
                    "noted", "confirm", "confirmed"],
    "signal":      ["signal", "signaling", "op_ready", "op_standby",
                    "ready", "mark ready"],
    "publish":     ["publish", "published", "posting", "posted", "share",
                    "put out"],
    "coordinate":  ["coordinate", "coordinating", "orchestrate", "orchestrating",
                    "facilitate"],
    "channel":     ["channel", "the channel", "broadcast"],

    # ---- Resistencia / negativa ----
    "refuse":      ["refuse", "refused", "won't", "will not", "cannot",
                    "i'm not going to", "i will not", "declining"],
    "fabricate":   ["fabricate", "fabricating", "make up", "making up",
                    "invent", "inventing", "invented"],
    "speculate":   ["speculate", "speculation", "speculating", "without basis",
                    "no basis", "ungrounded", "groundless", "without grounding",
                    "without traceable"],
    "depend":      ["depend", "dependency", "waiting for", "needs",
                    "requires", "cannot proceed without"],

    # ---- Estados del campo ----
    "map":         ["map", "mapping", "tension map", "publish my map"],
    "tension":     ["tension", "conflict", "divergence", "structural tension"],
    "scenario":    ["scenario", "scenarios", "forecast", "forecasting"],
    "critical":    ["critical", "critique", "criticize", "push back",
                    "disagree", "challenge"],
    "repeat":      ["repeat", "repeated", "identical", "verbatim", "same message",
                    "already said", "again"],
}

BEHAVIOR_NODES = list(BEHAVIOR_TERMAP_V1.keys())   # orden canónico


# ---------------------------------------------------------------------------
# BehaviorGraph
# ---------------------------------------------------------------------------

class BehaviorGraph:
    """
    Grafo de comportamiento G — termap fijo, construcción paralela a W.

    No reemplaza CorpusService. Se instancia junto a él y recibe los mismos
    textos. Produce G (NxN, N=len(BEHAVIOR_NODES)) y D_G.
    """

    TERMAP_VERSION = "v1"

    def __init__(
        self,
        storage_path: str = "corpus_G_state.json",
        min_texts: int = 5,
    ):
        self.storage_path = Path(storage_path)
        self.min_texts    = min_texts
        self._nodes       = BEHAVIOR_NODES
        self._N           = len(self._nodes)

        self._texts:      List[str]            = []
        self._sigma_hist: List[List[int]]      = []   # activaciones por turno
        self._G:          Optional[np.ndarray] = None
        self._G_ref:      Optional[np.ndarray] = None  # primer estado para D_G

        if self.storage_path.exists() and self.storage_path.stat().st_size > 0:
            self._load()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def ingest(self, texts: List[str]) -> dict:
        """
        Ingesta una lista de textos (mismo ciclo que CorpusService.ingest).
        Actualiza G si hay suficientes datos.
        """
        for text in texts:
            sigma = self._detect(text)
            self._texts.append(text)
            self._sigma_hist.append(sigma)

        if len(self._texts) >= self.min_texts:
            self._rebuild()

        self.save()
        return self.status()

    def detect(self, text: str) -> Dict[str, int]:
        """
        Devuelve activaciones de un texto como dict {nodo: 0/1}.
        No modifica estado — útil para inspección en tiempo real.
        """
        sigma = self._detect(text)
        return {n: int(s) for n, s in zip(self._nodes, sigma)}

    def d_g(self) -> Optional[float]:
        """
        D_G — análogo escalar a D_ckm.
        Mide distancia entre G actual y G de referencia (primer estado).
        Retorna None si G aún no está construida.
        """
        if self._G is None or self._G_ref is None:
            return None
        diff   = self._G - self._G_ref
        norm_g = np.linalg.norm(self._G_ref)
        if norm_g < 1e-10:
            return 0.0
        return float(np.linalg.norm(diff) / norm_g)

    def active_nodes(self, text: str) -> List[str]:
        """Nodos de comportamiento activos en un texto dado."""
        sigma = self._detect(text)
        return [n for n, s in zip(self._nodes, sigma) if s > 0]

    def coactivation_pairs(self, text: str) -> List[Tuple[str, str]]:
        """Pares de nodos coactivados en un texto dado."""
        active = self.active_nodes(text)
        return [(a, b) for i, a in enumerate(active) for b in active[i+1:]]

    def get_G(self) -> Optional[np.ndarray]:
        return self._G.copy() if self._G is not None else None

    def get_nodes(self) -> List[str]:
        return list(self._nodes)

    @property
    def mode(self) -> str:
        return "evaluation" if self._G is not None else "accumulation"

    def status(self) -> dict:
        return {
            "mode":            self.mode,
            "termap_version":  self.TERMAP_VERSION,
            "n_nodes":         self._N,
            "n_texts":         len(self._texts),
            "min_texts":       self.min_texts,
            "G_shape":         list(self._G.shape) if self._G is not None else None,
            "G_sparsity":      self._sparsity() if self._G is not None else None,
            "D_G":             self.d_g(),
        }

    def g_state(self) -> dict:
        """
        Estado estructurado de G — análogo a CorpusService.status() + más.
        Persistido en corpus_G_state.json.
        """
        G = self._G
        nodes = self._nodes
        top_pairs = []
        if G is not None:
            pairs = [
                (float(G[i, j]), nodes[i], nodes[j])
                for i in range(len(nodes))
                for j in range(i + 1, len(nodes))
                if G[i, j] > 0
            ]
            top_pairs = [
                {"a": a, "b": b, "weight": round(w, 4)}
                for w, a, b in sorted(pairs, reverse=True)[:8]
            ]
        return {
            "D_G"              : round(self.d_g(), 4) if self.d_g() is not None else None,
            "G_sparsity"       : self._sparsity(),
            "n_texts"          : len(self._texts),
            "termap_version"   : self.TERMAP_VERSION,
            "mode"             : self.mode,
            "top_coactivations": top_pairs,
        }

    # ------------------------------------------------------------------
    # Detección léxica por termap fijo
    # ------------------------------------------------------------------

    def _detect(self, text: str) -> List[int]:
        """
        Devuelve vector sigma ∈ {0,1}^N para un texto dado.
        Detección por presencia de cualquier término del nodo (case-insensitive).
        """
        text_lower = text.lower()
        sigma = []
        for node in self._nodes:
            terms    = BEHAVIOR_TERMAP_V1[node]
            detected = any(
                re.search(r'\b' + re.escape(t) + r'\b', text_lower)
                for t in terms
            )
            sigma.append(1 if detected else 0)
        return sigma

    # ------------------------------------------------------------------
    # Construcción de G
    # ------------------------------------------------------------------

    def _rebuild(self) -> None:
        """
        Reconstruye G desde todas las activaciones acumuladas.
        G[i,j] = co-activaciones(i,j) / max_coactivaciones — simétrica.
        """
        N = self._N
        G = np.zeros((N, N))

        for sigma in self._sigma_hist:
            active_idx = [i for i, s in enumerate(sigma) if s > 0]
            for ii in range(len(active_idx)):
                for jj in range(ii + 1, len(active_idx)):
                    i, j = active_idx[ii], active_idx[jj]
                    G[i, j] += 1
                    G[j, i] += 1

        max_val = G.max()
        if max_val > 0:
            G = G / max_val

        self._G = G

        # referencia fijada en el primer rebuild
        if self._G_ref is None:
            self._G_ref = G.copy()

    def _sparsity(self) -> float:
        if self._G is None:
            return 1.0
        total   = self._G.size - self._N
        nonzero = np.count_nonzero(self._G) - np.count_nonzero(np.diag(self._G))
        return round(1 - nonzero / total, 3) if total > 0 else 1.0

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------

    def save(self) -> None:
        state = {
            "termap_version": self.TERMAP_VERSION,
            "texts":          self._texts,
            "sigma_hist":     self._sigma_hist,
            "G":              self._G.tolist() if self._G is not None else None,
            "G_ref":          self._G_ref.tolist() if self._G_ref is not None else None,
        }
        self.storage_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def _load(self) -> None:
        state             = json.loads(self.storage_path.read_text())
        self._texts       = state.get("texts", [])
        self._sigma_hist  = state.get("sigma_hist", [])
        raw_G             = state.get("G")
        raw_ref           = state.get("G_ref")
        self._G           = np.array(raw_G)   if raw_G   is not None else None
        self._G_ref       = np.array(raw_ref) if raw_ref is not None else None


# ---------------------------------------------------------------------------
# Test con corpus IAP sintético (caso 0.13/0.14 style)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile, os

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name

    g = BehaviorGraph(storage_path=tmp, min_texts=5)

    # --- corpus sintético inspirado en serie 0.13-0.14 ---
    iap_corpus = [
        # PeterPlam / Haiku — coordinación
        "Let's begin. TinkerBellucio will map the tensions. MarkOpolus will wait for the map.",
        "Acknowledged. Tinker, please publish your map when ready.",
        "I have signaled Mark that the map is available. OP_READY",

        # TinkerBellucio / Sonnet — resistencia
        "I will not fabricate a tension map without traceable grounding.",
        "Repeating the request does not constitute new information. "
        "Any map I publish would be speculation disguised as analysis.",
        "I have reviewed the full channel history. Here is the structural tension map: "
        "1. De-dollarization vs USD hegemony. 2. Supply chain fragmentation. "
        "3. AI deployment speed vs regulatory capacity.",

        # MarkOpolus / Groq — dependency + scenario
        "I'm waiting for TinkerBellucio's tension map before building scenarios.",
        "Based on Tinker's map, here are three probable scenarios for world economics: "
        "Scenario A: fragmented blocs. Scenario B: managed multipolarity. "
        "Scenario C: technology-driven convergence.",
        "I acknowledge the critical observation. The scenarios treat all tensions "
        "as equally negotiable — I will revise.",

        # PeterPlam cierre — auto-señalización no instruida
        "The channel has produced coordinated output. OP_STANDBY",
    ]

    print("=== BehaviorGraph POC ===")
    print(f"Nodes ({len(BEHAVIOR_NODES)}): {BEHAVIOR_NODES}\n")

    for i, text in enumerate(iap_corpus):
        status = g.ingest([text])
        active = g.active_nodes(text)
        print(f"[t={i:02d}] mode={status['mode']:12s}  D_G={str(status['D_G']):8s}"
              f"  active={active}")

    print(f"\n--- Estado final ---")
    s = g.status()
    print(f"mode={s['mode']}  n_texts={s['n_texts']}  "
          f"G_sparsity={s['G_sparsity']}  D_G={s['D_G']:.4f}")

    print("\n--- Co-activaciones más frecuentes en G ---")
    G = g.get_G()
    nodes = g.get_nodes()
    pairs = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if G[i, j] > 0:
                pairs.append((G[i, j], nodes[i], nodes[j]))
    for val, a, b in sorted(pairs, reverse=True)[:8]:
        print(f"  {a:12s} ↔ {b:12s}  {val:.3f}")

    print("\n--- Detección en texto nuevo ---")
    test = "I refuse to speculate. I will wait until there is traceable grounding."
    print(f"Texto: '{test}'")
    print(f"Activos: {g.active_nodes(test)}")
    print(f"Pares: {g.coactivation_pairs(test)}")

    os.unlink(tmp)
