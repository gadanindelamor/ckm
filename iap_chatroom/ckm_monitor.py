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
from ckm_landscape_config import CKMlandscapeConfig  # noqa: E402
from corpus_service import CorpusService  # noqa: E402
from firma_ckm import FirmaService  # noqa: E402
from monitor_service import MonitorService  # noqa: E402
from node_extractor import NodeExtractorService  # noqa: E402

from iap_chatroom.channel import ChatChannel  # noqa: E402

_STATE_DIR = Path(__file__).resolve().parent / "_state"
_STATE_DIR.mkdir(exist_ok=True)

# Jerarquía de señales de rebuild (TASK_coco_alpha_compuesto_v3, Extensión 2):
# estructural (gradiente D_ckm) > volumen > tiempo. MAX_CICLOS provisional —
# no especificado por la task, ajustable sin cambiar la jerarquía.
MAX_CICLOS = 10


class CKMMonitor:
    _instance: "CKMMonitor | None" = None

    def __new__(cls, *args, **kwargs) -> "CKMMonitor":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, min_texts: int = 3, state_dir: "str | Path | None" = None) -> None:
        """
        `state_dir`: dónde viven `corpus_state.json`, `corpus_G_state.json` y
        `monitor_trajectory.jsonl`. **Default: el de siempre**
        (`iap_chatroom/_state/`), así que nada cambia para quien no lo pase.

        **Por qué existe (F3a).** El estado se acumulaba entre vivos: el corpus
        pasó de 10 a 12 textos entre el vivo 01 y el 02, y nadie lo declaraba.
        Con un directorio por vivo, cada corrida arranca de un estado conocido.
        **El de agosto no se borra**: se deja de usar, y queda como traza
        —8 de sus 12 textos son joins, que es la condición en la que corrió la
        serie congelada—.
        """
        if self._initialized:
            return
        self._initialized = True

        state = Path(state_dir) if state_dir is not None else _STATE_DIR
        state.mkdir(parents=True, exist_ok=True)
        self._state_dir = state
        _monitor_jsonl_path = str(state / "monitor_trajectory.jsonl")

        self._extractor = NodeExtractorService(top_k=32)
        self._corpus = CorpusService(
            storage_path=str(state / "corpus_state.json"),
            min_texts=min_texts,  # default=3; configurable por el caller
            top_k=32,
            # rebuild suspendido también en vivo (delamor): W se construye
            # cuando el dato distingue y no se reconstruye por mensaje.
            rebuild_suspendido=True,
            monitor_jsonl_path=_monitor_jsonl_path,
        )
        # G corre en paralelo real a {W, Delta_W} -- cada mensaje que
        # entra a self._corpus tambien entra a self._behavior_graph,
        # via MonitorService.evaluate() (services/monitor_service.py).
        # Autorizado explicitamente (Caso 0.15, gadanin.delamor) --
        # cambio quirurgico, unico punto de integracion real posible
        # sin volver G retroactivo.
        self._behavior_graph = BehaviorGraph(
            storage_path=str(state / "corpus_G_state.json"),
            min_texts=min_texts,
        )
        # Config del instrumento. Se construye **sin W**: el corpus arranca
        # en acumulación y W aparece recién al cruzar min_texts, así que no
        # hay nada que medir todavía. Monitor abre el primer ciclo —causa
        # "bootstrap"— en su primera evaluación, y los siguientes en cada
        # rebuild (D4). Sin theta_W ni scale: theta_W es del Gatekeeper y
        # scale sólo lo usa la UI, y por I4 lo declarado se exige según
        # quién lo usa. sampling_mode es el default de MonitorService.
        # Ver docs/tasks/TASK_CKMlandscapeConfig_v3.md y DECISIONES_opus.md.
        self._landscape_config = CKMlandscapeConfig(sampling_mode="uniform")
        # COCO es de Monitor (CP4). El canal ya no lo lee de CorpusService,
        # que dejó de crearlo: le pasa CÓMO construirlo y Monitor lo hace
        # nacer con el ciclo bootstrap y renacer en cada rebuild (D4).
        # track_landscape=True es lo que CorpusService declaraba antes.
        # n_runs, seed y sampling_mode salen de la Config (P9), no de acá.
        self._monitor = MonitorService(
            self._corpus,
            storage_path=_monitor_jsonl_path,
            behavior_graph=self._behavior_graph,
            landscape_config=self._landscape_config,
            coco_config={"track_landscape": True},
        )
        self._firma = FirmaService()

        self._message_count = 0
        self._devices_seen: set[str] = set()
        self._last_panel: dict | None = None
        self._d_ckm_history: list[float] = []
        self._ciclos_sin_rebuild = 0
        self._last_rebuild_signal = False

    @property
    def state_dir(self) -> Path:
        """Dónde vive el estado de este CKMMonitor. Declarable por vivo (F3a)."""
        return self._state_dir

    def on_message(self, message) -> None:
        """Callback registrado en ChatChannel.add_callback."""
        # El historial del paisaje sale del COCO de Monitor, no de Corpus
        # (CP4). Por la decisión 2(b), un COCO recién nacido lo tiene vacío.
        # El CLOCK del canal entra a la observación. El canal lo genera con su
        # propio reloj; Monitor lo anota en la Config (CP1, decisión de delamor).
        # get_clock() además registra el tick, con o sin mensajes: el silencio
        # queda como dato aunque nadie publique.
        clock = ChatChannel().get_clock()

        # ── F3b — delamor, 9 oct: "no, nunca." ──────────────────────────────
        # **Los mensajes SYSTEM no entran al corpus.** Los joins y los leaves
        # son eventos operacionales del canal, no texto de la interacción, y
        # hasta hoy entraban: medido en los vivos 01 y 02, **8 de los 12
        # textos del corpus eran "X joined the channel"** — dos tercios de lo
        # que construye W.
        #
        # El corpus de agosto **queda como está**, como traza: la serie
        # congelada corrió con los joins adentro, y la serie nueva no se
        # compara con ella (CP0b).
        #
        # Siguen contándose en `message_count` y siguen llegando a los devices
        # por `get_messages`: lo que no hacen es entrar a W.
        es_system = getattr(message, "device_type", None) == "SYSTEM"

        th = self._monitor.thermostat
        signal = th.landscape_history() if th is not None else None
        sha_before = self._corpus.w_sha()
        if not es_system:
            self._corpus.ingest([message.text], landscape_signal=signal)
        sha_after = self._corpus.w_sha()

        self._message_count += 1

        # ── F4 — `"system"` no cuenta como agente ──────────────────────────
        # `_devices_seen` cuenta **device_ids que publicaron**, y el
        # pseudo-device del canal entraba como uno: en los dos vivos, con dos
        # devices que nunca publicaron, `n_agentes` dio **1** y ese 1 era el
        # canal. El canal no es un participante.
        if not es_system:
            self._devices_seen.add(message.device_id)

        # rebuild real (_rebuild() corrió y cambió W) detectado por sha,
        # no un flag que ingest() no expone — reset del contador de ciclos.
        if sha_after != sha_before:
            self._ciclos_sin_rebuild = 0
        else:
            self._ciclos_sin_rebuild += 1

        if self._message_count >= self._corpus.min_texts:
            self._last_panel = self._monitor.evaluate(
                message.text, device_id=message.device_id, clock=clock
            )
            d_ckm = self._last_panel.get("D_ckm") if self._last_panel else None
            if d_ckm is not None:
                self._d_ckm_history.append(d_ckm)

        # Jerarquía: estructural (gradiente D_ckm) > volumen > tiempo.
        # Señal observable — no fuerza el rebuild todavía (eso sigue
        # gobernado por el chequeo de volumen interno de ingest()).
        self._last_rebuild_signal = (
            self._corpus.should_rebuild(self._d_ckm_history, n=3)
            or len(self._corpus._texts) >= self._corpus.min_texts * 2
            or self._ciclos_sin_rebuild >= MAX_CICLOS
        )

    def get_state(self) -> dict:
        status = self._corpus.status()

        d_ckm = None
        temp_signal = None
        if self._last_panel and "D_ckm" in self._last_panel:
            d_ckm = self._last_panel["D_ckm"]
            thermostat = self._last_panel.get("thermostat")
            # panel["thermostat"]["temp_signal"] es el dict de COCO; acá va la
            # señal. Sin thermostat: UNKNOWN, no NOMINAL — no se midió.
            ts = thermostat.get("temp_signal") if thermostat else None
            temp_signal = ts["signal"] if isinstance(ts, dict) else (ts or "UNKNOWN")

        corpus_status = "operational" if status["mode"] == "evaluation" else "accumulating"

        return {
            "corpus_size": status["n_texts"],
            "n_nodes": status["n_nodes"],
            "message_count": self._message_count,
            "D_ckm": d_ckm,
            "temp_signal": temp_signal,
            "n_agentes": len(self._devices_seen),
            "corpus_status": corpus_status,
            # **Dónde está escribiendo esto.** Va al panel para que cada vivo
            # deje dicho dónde escribió, y no haya que deducirlo del comando
            # que lo lanzó (delamor/Opus, fix 2). El vivo 02 acumuló estado
            # entre corridas y nadie lo declaraba.
            "state_dir": str(self._state_dir),
        }

    def get_firma(self) -> dict | None:
        if self._corpus.status()["n_texts"] == 0:
            return None
        firma = self._firma.firmar(
            self._corpus,
            self._monitor,
            # **Sin `or 1`** (delamor, 9 oct: *"sí"*). `n_agentes` en la
            # firma es el conteo real: **0 si no hubo agentes**. El `or 1`
            # hacía que con cero devices vistos la firma certificara 1 agente
            # — NOMINAL por ausencia en lo que certifica el estado
            # estructural. Verificado antes de sacarlo: **nada divide por
            # `n_agentes`** en el repo; sólo se guarda y se lee.
            n_agentes=len(self._devices_seen),
        )
        return firma.to_dict() if firma is not None else None
