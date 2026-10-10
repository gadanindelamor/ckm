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

import json
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

# Las tres causas del rebuild por decisión, con la jerarquía en el orden en que
# se evalúan. Escritas acá para que no haya dos spellings sueltos: el mismo
# string va al `causal_event` de `w_version` y al panel.
CAUSA_ESTRUCTURAL = "estructural"
CAUSA_VOLUMEN = "volumen"
CAUSA_TIEMPO = "tiempo"


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
        # ── CP2b: la decisión de rebuild, persistida ───────────────────────
        # **Dos archivos y dos mecanismos, los mismos que ya usa este
        # directorio** (criterio de congruencia de delamor):
        #   - JSONL append-only para **eventos en el tiempo**, como
        #     `monitor_trajectory.jsonl`;
        #   - JSON snapshot para **estado**, como `corpus_state.json`.
        # Una decisión de rebuild es un evento; los contadores son estado.
        self._decisiones_path = state / "rebuild_decisions.jsonl"
        self._rebuild_state_path = state / "rebuild_state.json"

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
        # **Textos desde el último rebuild** (CP3, TASK punto 3). El criterio de
        # volumen contaba el total del corpus, y pasado `2*min_texts` quedaba en
        # `True` **para siempre**: con el CP2 eso dispara un rebuild por
        # mensaje, que es el rebuild continuo que delamor descartó
        # —*"la ingesta no debe implicar rebuilds continuos"*—.
        #
        # Arranca en 0 y cuenta hacia arriba; se reinicia en cada rebuild real,
        # detectado por sha como el contador de ciclos.
        self._textos_desde_rebuild = 0
        # Lo persistido manda sobre los defaults de arriba.
        self._n_decisiones = len(self.decisiones_de_rebuild())
        self._cargar_rebuild_state()
        # Cuál de los tres criterios levantó la señal. `None` es "ninguno", y
        # se distingue de `False`: el bool dice si hubo señal, esto dice de qué.
        self._last_rebuild_causa: "str | None" = None
        # El último rebuild por decisión, o None si no hubo ninguno todavía.
        self._ultimo_rebuild: "dict | None" = None
        # El lugar donde va `calibrate`. Existe y no hace nada: declarado.
        self._punto_calibrate: "dict | None" = None

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
        # Un texto más desde el último rebuild. Va **antes** del chequeo de
        # sha: el texto de esta ingesta cuenta para el ciclo en curso, y si el
        # rebuild ocurre en esta misma vuelta el reset de abajo lo lleva a 0.
        self._textos_desde_rebuild += 1

        if sha_after != sha_before:
            self._ciclos_sin_rebuild = 0
            # rebuild por ingesta (la primera W, o el régimen no suspendido):
            # el ciclo nuevo arranca con su cuenta en cero
            self._textos_desde_rebuild = 0
        else:
            self._ciclos_sin_rebuild += 1

        if self._message_count >= self._corpus.min_texts:
            self._last_panel = self._monitor.evaluate(
                message.text, device_id=message.device_id, clock=clock
            )
            d_ckm = self._last_panel.get("D_ckm") if self._last_panel else None
            if d_ckm is not None:
                self._d_ckm_history.append(d_ckm)

        # ── la señal, y ahora CUÁL criterio ───────────────────────────────
        # Jerarquía declarada: estructural (gradiente D_ckm) > volumen >
        # tiempo. Antes la señal era un `bool` y el comentario decía "no fuerza
        # el rebuild todavía": se calculaba y su resultado no llegaba al punto
        # de decisión, que estaba adentro de `ingest()`. El CP0 lo nombró como
        # uno de los cinco mecanismos construidos sin consumidor.
        #
        # **`_last_rebuild_signal` sigue siendo el bool y no se renombra**
        # (TASK: no se renombra nada). La causa va al lado, porque un bool no
        # puede decir cuál de los tres disparó, y eso es lo que tiene que
        # quedar en `causal_event`.
        if self._corpus.should_rebuild(self._d_ckm_history, n=3):
            self._last_rebuild_causa = CAUSA_ESTRUCTURAL
        elif self._textos_desde_rebuild >= self._corpus.min_texts * 2:
            # **Por ciclo, no el total** (CP3). El umbral `2*min_texts` no se
            # toca: su valor es calibración. Lo que cambia es **sobre qué se
            # cuenta**.
            self._last_rebuild_causa = CAUSA_VOLUMEN
        elif self._ciclos_sin_rebuild >= MAX_CICLOS:
            self._last_rebuild_causa = CAUSA_TIEMPO
        else:
            self._last_rebuild_causa = None

        self._last_rebuild_signal = self._last_rebuild_causa is not None

        # ── la decisión manda el rebuild (TASK, punto 1) ──────────────────
        # `rebuild_suspendido=True` sigue impidiendo el rebuild automático por
        # ingesta; este no pasa por ahí.
        if self._last_rebuild_signal:
            sha_antes = self._corpus.w_sha()
            st = self._corpus.rebuild_por_decision(self._last_rebuild_causa)
            self._ultimo_rebuild = {
                "causa": self._last_rebuild_causa,
                "causal_event": (
                    f"rebuild_por_decision:{self._last_rebuild_causa}"
                    if st.get("rebuild") else None
                ),
                "ocurrio": bool(st.get("rebuild")),
                "motivo_no_rebuild": st.get("motivo_no_rebuild"),
                "w_sha": self._corpus.w_sha(),
            }
            if st.get("rebuild"):
                # El contador de ciclos arranca de nuevo en el salto: lo que
                # cuenta es cuántos ciclos van SIN rebuild.
                self._ciclos_sin_rebuild = 0
                # Y la cuenta de volumen del ciclo nuevo (CP3). Sin esto, el
                # volumen quedaría en `True` desde el primer mensaje posterior
                # al salto y el rebuild volvería a ser continuo.
                self._textos_desde_rebuild = 0
                # **Acá va `calibrate`** (`TASK_calibrate_mecanismo_v1`,
                # confirmado). El punto existe y **no hace nada todavía**, y se
                # declara así: dejarlo sin marca haría que mañana el lugar se
                # buscara de nuevo.
                self._punto_calibrate = {
                    "existe": True,
                    "implementado": False,
                    "task": "TASK_calibrate_mecanismo_v1",
                    "w_sha": self._corpus.w_sha(),
                }
            # La decisión queda en el jsonl **haya movido W o no** (CP2b): el
            # caso que no la mueve es justamente el que `w_version` no registra.
            self._ultimo_rebuild["registro"] = self._registrar_decision(
                self._last_rebuild_causa, st, sha_antes, clock
            )

        # El estado de la decisión, en cada mensaje: mismo mecanismo que el
        # `save()` de CorpusService, que también guarda en cada ingesta.
        self._guardar_rebuild_state()

    def _cargar_rebuild_state(self) -> None:
        """
        Restaura los contadores de la decisión desde el `state_dir`.

        **Esto cambia el comportamiento** (declarado): hasta el CP2b
        `_ciclos_sin_rebuild` vivía sólo en memoria, así que **el criterio de
        tiempo arrancaba de cero en cada reinicio del server** — con
        `MAX_CICLOS = 10`, un canal que se reiniciaba cada menos de 10 mensajes
        no disparaba por tiempo nunca, y nada lo decía. Ahora el tiempo
        sobrevive al reinicio.

        Un archivo ilegible **no se tapa con los defaults en silencio**: se
        deja el aviso en `_rebuild_state_error` y los contadores arrancan de
        cero, que es lo mismo que pasaba antes del CP2b.
        """
        self._rebuild_state_error = None
        # **Se distingue del error**: un estado descartado no es un archivo
        # roto. Las dos cosas dejan los contadores en cero y son distintas, así
        # que no se colapsan en un campo.
        self._rebuild_state_descartado = None
        if not self._rebuild_state_path.exists():
            return
        try:
            d = json.loads(self._rebuild_state_path.read_text())
            sha_guardado = d.get("w_sha")
            sha_actual = self._corpus.w_sha()
            if sha_guardado != sha_actual:
                # **Los contadores de una meseta no pasan a otra** (delamor).
                # Se descartan y la causa queda escrita: restaurarlos acá haría
                # que el volumen y el tiempo del ciclo anterior corrieran contra
                # la W nueva, y el panel diría una cuenta que no es de esta
                # meseta.
                self._rebuild_state_descartado = {
                    "causa": "w_sha_distinto",
                    "w_sha_guardado": sha_guardado,
                    "w_sha_del_corpus": sha_actual,
                    "descartados": ["ciclos_sin_rebuild",
                                    "textos_desde_rebuild", "d_ckm_history"],
                }
                return
            self._ciclos_sin_rebuild = int(d["ciclos_sin_rebuild"])
            self._textos_desde_rebuild = int(d["textos_desde_rebuild"])
            self._d_ckm_history = [float(x) for x in d["d_ckm_history"]]
        except (ValueError, KeyError, TypeError, OSError) as e:
            self._rebuild_state_error = f"{type(e).__name__}: {e}"

    def _guardar_rebuild_state(self) -> None:
        """
        El estado de la decisión, con el mismo mecanismo que
        `corpus_state.json`: un JSON que se sobreescribe.

        `d_ckm_history` se guarda **como está hoy**, que es acumulada y no por
        ciclo: reiniciarla en el salto es el **CP4**. Persistirla ahora **no la
        vuelve por ciclo**, y decirlo acá evita que el archivo se lea como si
        ya lo fuera.
        """
        self._rebuild_state_path.write_text(json.dumps({
            # **El w_sha del ciclo al que pertenecen estos contadores.**
            # Sin esto, los contadores de una meseta se restauran sobre otra
            # meseta y nadie lo dice: es la misma forma que el CP0 encontró en
            # la Firma —un número de un ciclo sellado con la identidad de otro—.
            "w_sha": self._corpus.w_sha(),
            "ciclos_sin_rebuild": self._ciclos_sin_rebuild,
            "textos_desde_rebuild": self._textos_desde_rebuild,
            "d_ckm_history": [float(x) for x in self._d_ckm_history],
            "d_ckm_history_es_por_ciclo": False,
            "nota": "d_ckm_history acumulada; por ciclo es el CP4",
        }, ensure_ascii=False))

    def _registrar_decision(self, causa: str, st: dict,
                            sha_antes: "str | None", clock: dict) -> dict:
        """
        Una línea en `rebuild_decisions.jsonl` por **decisión tomada**.

        El núcleo es el par `w_sha_antes` / `w_sha_despues` con `w_cambio`
        explícito: `w_version` **deduplica por sha**, así que una decisión que
        no mueve W **no deja versión**, y sin esta línea no quedaría en ningún
        lado. Con `w_cambio` se distingue de un salto.

        `reloj` viene del **mismo reloj del canal** que sella los mensajes
        (`ChatChannel.get_clock()`), no de un `time.time()` aparte.

        Las vueltas **sin** señal no se registran (acordado): una línea por
        mensaje sería el ruido que el filtro del CP2b del canal existe para
        evitar.
        """
        sha_despues = self._corpus.w_sha()
        reg = {
            "t": self._n_decisiones,
            "ts": clock.get("t"),
            "tick": clock.get("tick"),
            "reloj": clock.get("reloj", "desconocido"),
            "causa": causa,
            "ocurrio": bool(st.get("rebuild")),
            "motivo_no_rebuild": st.get("motivo_no_rebuild"),
            "w_sha_antes": sha_antes,
            "w_sha_despues": sha_despues,
            "w_cambio": sha_antes != sha_despues,
            "corpus_size": len(self._corpus._texts),
            "message_count": self._message_count,
            "ciclos_sin_rebuild": self._ciclos_sin_rebuild,
            "n_puntos_d_ckm": len(self._d_ckm_history),
        }
        with open(self._decisiones_path, "a") as f:
            f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
        self._n_decisiones += 1
        return reg

    def decisiones_de_rebuild(self) -> list:
        """Las decisiones registradas, leídas del `state_dir`."""
        if not self._decisiones_path.exists():
            return []
        return [json.loads(l) for l in
                self._decisiones_path.read_text().splitlines() if l.strip()]

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
            # ── el rebuild por decisión, en el panel (TASK, punto 2) ───────
            #
            # `None` en `rebuild_causa` es **"no hubo rebuild por decisión"**,
            # y no "no sé": si hubo, el campo trae cuál de los tres criterios
            # disparó. Va acá —el panel que el canal expone— y no en el panel
            # de `MonitorService`: tocar Monitor pide parar y reportar.
            "rebuild_senal": self._last_rebuild_signal,
            "rebuild_causa": self._last_rebuild_causa,
            "ultimo_rebuild_por_decision": self._ultimo_rebuild,
            # El punto donde va `calibrate`: existe y no hace nada. Declarado
            # en el panel para que no haya que buscarlo de nuevo.
            "punto_calibrate": self._punto_calibrate,
            # ── CP2b: dónde quedó la decisión, y qué se restauró ──────────
            "rebuild_decisions_path": str(self._decisiones_path),
            "n_decisiones_registradas": self._n_decisiones,
            "textos_desde_rebuild": self._textos_desde_rebuild,
            "ciclos_sin_rebuild": self._ciclos_sin_rebuild,
            # `None` es "se leyó bien o no había nada"; un string es el error.
            # Un estado ilegible no se tapa con los defaults en silencio.
            "rebuild_state_error": self._rebuild_state_error,
            # `None` es "no se descartó nada"; un dict dice qué y por qué.
            "rebuild_state_descartado": self._rebuild_state_descartado,
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
