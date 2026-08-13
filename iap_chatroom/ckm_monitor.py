"""
ckm_monitor.py — CKMMonitor

Observador CKM de la chatroom. Se registra como callback en ChatChannel
y acumula cada mensaje en el corpus; W emerge de la interacción, no se
precarga. No participa en el chat — solo observa.

Nota de integración con services/:
  - CorpusService.ingest(texts) es el método real de acumulación (no
    "accumulate" como se llama en NodeExtractorService).
  - MonitorService.evaluate(text, device_id=None) requiere el texto de
    cada evaluación — no es un evaluate() sin argumentos.
  - FirmaService.firmar(corpus, monitor, n_agentes) es stateless; no
    guarda referencia a corpus/monitor por sí sola.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
if str(_SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(_SERVICES_DIR))

from behavior_graph import BehaviorGraph  # noqa: E402
from corpus_service import CorpusService  # noqa: E402
from firma_ckm import FirmaService  # noqa: E402
from monitor_service import MonitorService  # noqa: E402
from node_extractor import NodeExtractorService  # noqa: E402

_STATE_DIR = Path(__file__).resolve().parent / "_state"
_STATE_DIR.mkdir(exist_ok=True)


class CKMMonitor:
    _instance: "CKMMonitor | None" = None

    def __new__(cls) -> "CKMMonitor":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, min_texts: int = 3) -> None:
        if self._initialized:
            return
        self._initialized = True

        self._extractor = NodeExtractorService(top_k=32)
        self._corpus = CorpusService(
            storage_path=str(_STATE_DIR / "corpus_state.json"),
            min_texts=min_texts,  # default=3; configurable por el caller
            top_k=32,
        )
        # G corre en paralelo real a {W, Delta_W} -- cada mensaje que
        # entra a self._corpus tambien entra a self._behavior_graph,
        # via MonitorService.evaluate() (services/monitor_service.py).
        # Autorizado explicitamente (Caso 0.15, gadanin.delamor) --
        # cambio quirurgico, unico punto de integracion real posible
        # sin volver G retroactivo.
        self._behavior_graph = BehaviorGraph(
            storage_path=str(_STATE_DIR / "corpus_G_state.json"),
            min_texts=min_texts,
        )
        self._monitor = MonitorService(
            self._corpus,
            storage_path=str(_STATE_DIR / "monitor_trajectory.jsonl"),
            behavior_graph=self._behavior_graph,
        )
        self._firma = FirmaService()

        self._message_count = 0
        self._devices_seen: set[str] = set()
        self._last_panel: dict | None = None

    def on_message(self, message) -> None:
        """Callback registrado en ChatChannel.add_callback."""
        signal = self._corpus.coco.landscape_history() if self._corpus.coco is not None else None
        self._corpus.ingest([message.text], landscape_signal=signal)
        self._message_count += 1
        self._devices_seen.add(message.device_id)

        if self._message_count >= self._corpus.min_texts:
            self._last_panel = self._monitor.evaluate(message.text, device_id=message.device_id)

    def get_state(self) -> dict:
        status = self._corpus.status()

        d_ckm = None
        temp_signal = None
        if self._last_panel and "D_ckm" in self._last_panel:
            d_ckm = self._last_panel["D_ckm"]
            thermostat = self._last_panel.get("thermostat")
            temp_signal = thermostat["temp_signal"] if thermostat else "NOMINAL"

        corpus_status = "operational" if status["mode"] == "evaluation" else "accumulating"

        return {
            "corpus_size": status["n_texts"],
            "n_nodes": status["n_nodes"],
            "message_count": self._message_count,
            "D_ckm": d_ckm,
            "temp_signal": temp_signal,
            "n_agentes": len(self._devices_seen),
            "corpus_status": corpus_status,
        }

    def get_firma(self) -> dict | None:
        if self._corpus.status()["n_texts"] == 0:
            return None
        firma = self._firma.firmar(
            self._corpus,
            self._monitor,
            n_agentes=len(self._devices_seen) or 1,
        )
        return firma.to_dict() if firma is not None else None
