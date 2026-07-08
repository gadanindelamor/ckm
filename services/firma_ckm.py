"""
firma_ckm.py — FirmaService

Registra la forma del campo en un momento dado.
No produce la huella — hace legible la huella que ya existe.

Campos (REG_firma_corpus_v1):
    sha256(W_momento)         — estado del suelo en ese instante
    D_ckm(t)                  — posición en el paisaje
    temp_signal               — TOO_COLD / NOMINAL / TOO_HOT
    n_agentes                 — presencia, sin identidad si no se declara
    timestamp
    sha256(Delta_r_acumulado) — huella del contacto

Sin contenido. Sin texto intercambiado.
Sin nombres de agentes si no se declaran.

Cualquiera con acceso al corpus puede verificar:
en este momento, el campo tenía esta forma,
y algo lo modificó en esta dirección.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# Primitiva
# ---------------------------------------------------------------------------

def _sha256(arr: np.ndarray) -> str:
    return hashlib.sha256(arr.tobytes()).hexdigest()


# ---------------------------------------------------------------------------
# Firma — los 6 campos canónicos
# ---------------------------------------------------------------------------

@dataclass
class Firma:
    """
    Huella estructural de un momento de interacción.
    Inmutable por diseño: dataclass sin post_init mutante.
    """
    w_sha    : str    # sha256(W_momento)
    d_ckm    : float  # D_ckm(t) al momento de la firma
    temp_signal: str  # TOO_COLD | NOMINAL | TOO_HOT
    n_agentes: int    # número de agentes presentes
    timestamp: float  # time.time()
    delta_sha: str    # sha256(Delta_r_acumulado)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "Firma":
        return cls(**d)


# ---------------------------------------------------------------------------
# FirmaService
# ---------------------------------------------------------------------------

class FirmaService:
    """
    Produce y verifica Firmas_CKM.

    firmar(corpus, monitor, n_agentes) → Firma | None
        None si corpus en acumulación (W no disponible).

    verificar(firma, corpus) → dict
        Verifica que w_sha existe en el historial de W.
        No verifica contenido — verifica forma del campo.
    """

    def firmar(
        self,
        corpus,
        monitor,
        n_agentes: int = 1,
    ) -> Optional[Firma]:
        """
        Produce Firma del estado actual del campo.
        Devuelve None si W no existe todavía (corpus en acumulación).
        """
        w_sha = corpus.w_sha()
        if w_sha is None:
            return None

        # D_ckm — desde trayectoria si existe, directo si no
        d_ckm = 0.0
        traj = monitor.trajectory()
        if traj:
            d_ckm = traj[-1]["panel"]["D_ckm"]
        else:
            W = corpus.get_W()
            if W is not None:
                d_ckm = monitor._D_ckm(W)

        # temp_signal — desde thermostat si está inyectado
        temp_signal = "NOMINAL"
        if monitor._thermostat is not None:
            temp_signal = monitor._thermostat.temp_signal()

        # delta_sha — sha del Δ acumulado o ceros si es la primera firma
        if monitor._Delta_r is not None:
            delta_sha = _sha256(monitor._Delta_r)
        else:
            N = len(corpus.get_nodes())
            delta_sha = _sha256(np.zeros((N, N)))

        return Firma(
            w_sha     = w_sha,
            d_ckm     = round(d_ckm, 6),
            temp_signal = temp_signal,
            n_agentes = n_agentes,
            timestamp = time.time(),
            delta_sha = delta_sha,
        )

    def verificar(self, firma: Firma, corpus) -> dict:
        """
        Verifica que el w_sha de la firma existe en el historial de versiones de W.
        Verificación estructural abierta — sin confianza delegada.
        """
        sha_en_historial = any(
            t.sha256 == firma.w_sha
            for t in corpus._w_versions.history()
        )
        return {
            "w_sha_en_historial": sha_en_historial,
            "w_sha_es_actual"   : corpus.w_sha() == firma.w_sha,
        }
