"""
w_version.py — WVersionManager

Registro de versiones de W como marcas de traza livianas.
No es una copia de W — es la huella de que W cambió.

Plano separado de STOP/Δ: STOP opera sobre Δ, nunca alcanza las marcas de W.
Requerido por Firma_CKM: sha256(W_momento) debe estar disponible
en el momento del evento a certificar.

Diseño (REG_firma_corpus_v1):
  - W es invariante intra-ciclo
  - Cambios entre instancias de corpus invalidan beta_c_corpus
  - Las marcas señalan invalidación sin disparar recalculación
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, asdict
from typing import List, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Primitivas
# ---------------------------------------------------------------------------

def sha256_W(W: np.ndarray) -> str:
    """sha256 determinístico de una matriz numpy."""
    return hashlib.sha256(W.tobytes()).hexdigest()


@dataclass
class WTracePoint:
    """
    Marca liviana de versión de W.
    No almacena W — almacena que W cambió, cuándo, y en qué contexto.
    """
    timestamp: float
    sha256: str
    corpus_size: int
    causal_event: str   # "rebuild" | "load" | str libre


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class WVersionManager:
    """
    Historial de versiones de W como secuencia de WTracePoints.

    API pública:
        register(W, corpus_size, causal_event) → str   sha256 actual
        current_sha()                           → Optional[str]
        current_corpus_size()                   → Optional[int]
        changed_since(sha)                      → bool
        history()                               → List[WTracePoint]
        to_list() / from_list()                 → serialización
    """

    def __init__(self) -> None:
        self._traces: List[WTracePoint] = []

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def register(
        self,
        W: np.ndarray,
        corpus_size: int,
        causal_event: str = "rebuild",
    ) -> str:
        """
        Registra marca si W cambió respecto al estado anterior.
        Si W es idéntica, no crea marca duplicada.
        Devuelve sha256 actual.
        """
        sha = sha256_W(W)
        if self._traces and self._traces[-1].sha256 == sha:
            return sha  # W sin cambios — no se crea marca

        self._traces.append(WTracePoint(
            timestamp=time.time(),
            sha256=sha,
            corpus_size=corpus_size,
            causal_event=causal_event,
        ))
        return sha

    def current_sha(self) -> Optional[str]:
        """sha256 de la versión actual de W. None si nunca fue registrada."""
        return self._traces[-1].sha256 if self._traces else None

    def current_corpus_size(self) -> Optional[int]:
        """corpus_size de la versión actual."""
        return self._traces[-1].corpus_size if self._traces else None

    def changed_since(self, sha: str) -> bool:
        """
        True si W cambió desde la versión identificada por sha.
        Señal de invalidación para beta_c_corpus sin disparar recalculación.
        """
        return self.current_sha() != sha

    def history(self) -> List[WTracePoint]:
        """Lista completa de marcas de versión."""
        return list(self._traces)

    def __len__(self) -> int:
        return len(self._traces)

    # ------------------------------------------------------------------
    # Serialización
    # ------------------------------------------------------------------

    def to_list(self) -> list:
        return [asdict(t) for t in self._traces]

    def from_list(self, data: list) -> None:
        self._traces = [WTracePoint(**d) for d in data]
