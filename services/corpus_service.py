"""
corpus_service.py — CorpusService  v2

Stateful. Acumula prompts, construye W desde co-activaciones.
Transición automática acumulación → evaluación cuando hay suficientes datos.

v2: W mixta — pesos negativos por marcadores de oposición (elicitación sin sesgo).
  - Si un texto contiene un marcador de oposición → co-ocurrencias contribuyen
    negativamente: w_ij -= freq / norm.
  - Si no → contribuyen positivamente: w_ij += freq / norm.
  - W resultante ∈ [−1, +1]. Tensión estructural real.
  - Los marcadores son la señal — no se asume oposición; el texto la declara.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from node_extractor import NodeExtractorService
from w_version import WVersionManager


# ---------------------------------------------------------------------------
# Marcadores de oposición — elicitación sin sesgo
# El texto declara la oposición; el diseñador no la asume.
# Cobertura: ES + EN, debate real, registro formal e informal.
# ---------------------------------------------------------------------------
_OPPOSITION_MARKERS: set[str] = {
    # español
    "no estoy de acuerdo", "en desacuerdo", "discrepo", "discrepa",
    "incorrecto", "es falso", "eso es falso", "es mentira",
    "al contrario", "por el contrario", "sin embargo", "pero",
    "aunque", "a pesar de", "no obstante", "contradice", "niega",
    "refuta", "rechaza", "se opone", "opuesto a", "contrario a",
    # english
    "i disagree", "disagree", "that's wrong", "that is wrong",
    "incorrect", "false", "not true", "on the contrary",
    "however", "but", "although", "despite", "contradicts",
    "refutes", "opposes", "opposite", "against", "unlike",
    "wrong", "misleading", "no evidence", "debunked",
}


class CorpusService:

    def __init__(
        self,
        storage_path : str  = "corpus_state.json",
        min_texts    : int  = 3,    # umbral para pasar a modo evaluación
        top_k        : int  = 20,
        ngram_max    : int  = 2,
    ):
        self.storage_path = Path(storage_path)
        self.min_texts    = min_texts
        self._extractor   = NodeExtractorService(top_k=top_k, ngram_max=ngram_max)

        # estado
        self._texts     : List[str]            = []
        self._nodes     : List[str]            = []
        self._W         : Optional[np.ndarray] = None
        self._w_versions: WVersionManager      = WVersionManager()

        if self.storage_path.exists() and self.storage_path.stat().st_size > 0:
            self._load()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def ingest(self, texts: List[str]) -> dict:
        """
        Agrega textos al corpus. Reconstruye W si hay suficientes datos.
        Devuelve estado actual.
        """
        self._texts.extend(texts)
        if len(self._texts) >= self.min_texts:
            self._rebuild()
        self.save()
        return self.status()

    @property
    def mode(self) -> str:
        return "evaluation" if self._W is not None else "accumulation"

    def get_W(self) -> Optional[np.ndarray]:
        return self._W.copy() if self._W is not None else None

    def w_sha(self) -> Optional[str]:
        """sha256 de W en el momento actual. Para Firma_CKM."""
        return self._w_versions.current_sha()

    def w_changed_since(self, sha: str) -> bool:
        """True si W cambió desde la versión sha. Señal de invalidación beta_c_corpus."""
        return self._w_versions.changed_since(sha)

    def get_nodes(self) -> List[str]:
        return list(self._nodes)

    def status(self) -> dict:
        W = self._W
        neg_frac = None
        if W is not None:
            total   = W.size - W.shape[0]
            n_neg   = int(np.sum(W < 0))
            n_pos   = int(np.sum(W > 0))
            neg_frac = round(n_neg / total, 3) if total > 0 else 0.0
        return {
            "mode"       : self.mode,
            "n_texts"    : len(self._texts),
            "n_nodes"    : len(self._nodes),
            "min_texts"  : self.min_texts,
            "W_shape"    : list(W.shape) if W is not None else None,
            "W_sparsity" : self._sparsity() if W is not None else None,
            "W_neg_frac" : neg_frac,
            "w_sha"      : self._w_versions.current_sha(),   # Firma_CKM
        }

    # ------------------------------------------------------------------
    # Construcción de W  (v2 — mixta)
    # ------------------------------------------------------------------

    @staticmethod
    def _has_opposition(text: str) -> bool:
        """True si el texto contiene al menos un marcador de oposición."""
        t = text.lower()
        return any(m in t for m in _OPPOSITION_MARKERS)

    def _accumulate_safe(self, texts: List[str]) -> Dict:
        """
        Wrapper de self._extractor.accumulate() que absorbe el ValueError de
        TfidfVectorizer cuando un texto (o el batch) no aporta vocabulario
        tras stopwords + token_pattern — p.ej. mensajes muy cortos como
        "ok", "[quiet]" o textos de una sola stopword. Sin este guard, un
        solo mensaje degenerado tumba _rebuild() y deja self._texts
        envenenado (el texto ya fue extend()-ido antes de rebuild), lo que
        rompe todo ingest() futuro hasta reiniciar el proceso.
        """
        try:
            return self._extractor.accumulate(texts)
        except ValueError:
            return {"nodes": [], "pairs": {}, "node_freq": {}}

    def _rebuild(self) -> None:
        """
        Reconstruye nodos y W desde todos los textos acumulados.

        Ruteo por texto:
          - sin marcador → pares suman a pos_counts
          - con marcador → pares suman a neg_counts
        W[i,j] = (pos[i,j] - neg[i,j]) / max(|pos - neg|)
        Rango resultante: [−1, +1].
        """
        result = self._accumulate_safe(self._texts)
        nodes  = result["nodes"]

        if not nodes:
            return

        N        = len(nodes)
        node_idx = {n: i for i, n in enumerate(nodes)}

        pos_counts = np.zeros((N, N))
        neg_counts = np.zeros((N, N))

        # reconstruir pares por texto individual (granularidad texto)
        for text in self._texts:
            text_result = self._accumulate_safe([text])
            t_pairs     = text_result.get("pairs", {})
            is_opp      = self._has_opposition(text)

            for (ni, nj), count in t_pairs.items():
                if ni in node_idx and nj in node_idx:
                    i, j = node_idx[ni], node_idx[nj]
                    if is_opp:
                        neg_counts[i, j] += count
                        neg_counts[j, i] += count
                    else:
                        pos_counts[i, j] += count
                        pos_counts[j, i] += count

        raw = pos_counts - neg_counts
        max_abs = np.abs(raw).max()

        if max_abs > 0:
            W = raw / max_abs
        else:
            W = raw   # todo ceros — corpus sin señal aún

        np.fill_diagonal(W, 0.0)
        self._nodes = nodes
        self._W     = W
        self._w_versions.register(W, len(self._texts), causal_event="rebuild")

    def _sparsity(self) -> float:
        if self._W is None:
            return 1.0
        total    = self._W.size - self._W.shape[0]   # excluye diagonal
        nonzero  = np.count_nonzero(self._W) - np.count_nonzero(np.diag(self._W))
        return round(1 - nonzero / total, 3) if total > 0 else 1.0

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------

    def save(self) -> None:
        state = {
            "texts"           : self._texts,
            "nodes"           : self._nodes,
            "W"               : self._W.tolist() if self._W is not None else None,
            "w_version_history": self._w_versions.to_list(),
        }
        self.storage_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def _load(self) -> None:
        state       = json.loads(self.storage_path.read_text())
        self._texts = state.get("texts", [])
        self._nodes = state.get("nodes", [])
        raw_W       = state.get("W")
        self._W     = np.array(raw_W) if raw_W is not None else None
        self._w_versions.from_list(state.get("w_version_history", []))


# ---------------------------------------------------------------------------
# Test mínimo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile, os

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name

    corpus = CorpusService(storage_path=tmp, min_texts=5, top_k=10)

    # batch con textos de debate — oposición explícita
    batch_1 = [
        "gun control reduces violence and saves lives",
        "the second amendment protects the right to bear arms",
        "background checks prevent criminals from buying weapons",
    ]
    batch_2 = [
        "assault weapons bans reduce mass shootings",
        "however, gun rights are constitutional rights not subject to restriction",   # marcador
        "mental health is the real cause of gun violence, not guns",                  # marcador implícito
        "i disagree — armed citizens deter crime and protect communities",            # marcador explícito
    ]

    print("=== INGEST batch 1 ===")
    print(corpus.ingest(batch_1))

    print("\n=== INGEST batch 2 ===")
    status = corpus.ingest(batch_2)
    print(status)

    if corpus.mode == "evaluation":
        W = corpus.get_W()
        print(f"\nNodos: {corpus.get_nodes()}")
        print(f"W shape: {W.shape}")
        print(f"W min: {W.min():.3f}  W max: {W.max():.3f}")
        print(f"Pesos negativos: {(W < 0).sum()}  positivos: {(W > 0).sum()}")
        print(f"W_neg_frac: {status['W_neg_frac']}")

        # muestra los pares más negativos (tensión estructural)
        nodes = corpus.get_nodes()
        pairs_neg = []
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if W[i, j] < 0:
                    pairs_neg.append((W[i, j], nodes[i], nodes[j]))
        pairs_neg.sort()
        print("\nTop pares negativos (tensión):")
        for w, a, b in pairs_neg[:5]:
            print(f"  {a} — {b}  : {w:.3f}")

    os.unlink(tmp)
