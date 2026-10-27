"""
ckm_monitor.py — CKMMonitor

Observador CKM de la chatroom. Se registra como callback en ChatChannel;
W emerge de la interacción, no se precarga. No participa en el chat — solo
observa.

**Qué entra al corpus.** No todos los mensajes: **en las condiciones
actuales**, los de `device_type == "SYSTEM"` (joins, leaves) **quedan afuera**
(F3b, 9 oct 2026). Tampoco cuentan como agentes (F4).

Lo que lo motivó, medido en los vivos 01 y 02: **8 de los 12 textos del corpus
eran "X joined the channel"** — dos tercios de lo que construía W.

**No es una regla permanente, y la diferencia importa.** delamor lo precisó al
día siguiente: *"los mensajes de SYSTEM son campo, y debemos estudiar con calma
y atención cómo tratarlos. Mi decisión 'no, nunca' corresponde a las
circunstancias en las que decidí"* — se lee **"no, nunca en estas
condiciones"**. Su propósito fue cortar de cuajo un análisis que pedía otras
condiciones para existir, en medio de una implementación con tiempo acotado.
**Cómo tratar SYSTEM como campo queda abierto, sin apuro.**

Y hay dos lugares distintos: SYSTEM sale del **corpus** —lo que construye W— y
**sigue en la observación** del device (`n_nuevos`, `history`).

Este docstring decía *"acumula cada mensaje en el corpus"* y quedó
desactualizado el mismo día de F3b; se corrige acá.

**Dónde escribe.** `state_dir` es parámetro (F3a), con el default de siempre
(`iap_chatroom/_state/`). El server lo recibe como `--state-dir`
(`startup.py`), así que cada vivo puede arrancar de un estado conocido y el
panel declara dónde escribió.

**El rebuild lo decide esta clase, no la ingesta** (TASK_should_rebuild_
conectado_v1):
  - la señal se calcula con la jerarquía **estructural > volumen > tiempo**,
    y `_last_rebuild_causa` dice **cuál** de los tres disparó (CP2);
  - **cuáles votan** lo decide `criterios_rebuild`. El default son los tres, o
    sea el comportamiento de siempre. Existe por la PoC que pidió delamor
    (*"que no sea criterio min_texts… nulo"*), y **"peso nulo" se implementa
    sacando al criterio de la votación, no bajándole el umbral**: con
    `min_texts = 0` el volumen queda en `>= 0` —verdadero siempre— y como está
    antes del tiempo en la jerarquía **los otros dos no llegan a operar**. Un
    umbral 0 no quita el criterio: lo vuelve dominante, y además convierte la
    ausencia en un valor (I2);
  - cuando hay señal, se llama a `CorpusService.rebuild_por_decision(causa)`,
    que **no** está bloqueado por `rebuild_suspendido` —ese flag impide el
    rebuild automático **por ingesta**— y deja la causa en el `causal_event`
    de `w_version`;
  - el **volumen cuenta desde el último rebuild**, no el total del corpus
    (CP3): sobre el total quedaba en True para siempre y el rebuild volvía a
    ser continuo;
  - la **historia de `D_ckm` es por ciclo** y se reinicia en cada rebuild
    (CP4): `D_ckm` se mide contra el baseline de su ciclo, así que un
    gradiente que cruza un salto compara dos cosas medidas contra baselines
    distintos.

**Qué se persiste** (CP2b), en el mismo `state_dir` y con los mecanismos que
ese directorio ya usaba:
  - `rebuild_decisions.jsonl` — **append-only**, una línea por decisión
    tomada, con `w_sha_antes` / `w_sha_despues` / `w_cambio`. Ese par es el
    núcleo: `w_version` deduplica por sha, así que una decisión que no mueve W
    **no deja versión** y sin esta línea no quedaría en ningún lado. Las
    vueltas **sin** señal no se registran.
  - `rebuild_state.json` — los contadores, restaurados al arrancar. **Esto
    cambia el comportamiento**: el criterio de tiempo sobrevive al reinicio
    (antes `_ciclos_sin_rebuild` vivía en memoria). El archivo guarda el
    `w_sha` del ciclo, y si al arrancar no coincide con la W del corpus **los
    contadores se descartan y la causa queda escrita**: los de una meseta no
    pasan a otra.

**Lo medido en la PoC (11 oct), con 30 mensajes de un corpus chico:** con los
tres criterios dispara **sólo el volumen**, cada `min_texts*2 = 6` mensajes; sin
el volumen gobierna el **tiempo**, cada `MAX_CICLOS = 10`. **El estructural no
dispara en ninguno de los dos**: `D_ckm` sale `0.0` constante, así que el
gradiente es 0 y `should_rebuild` pide `> 0`. Coincide con la medición del 28
sep. Así que hoy el volumen **no es un criterio que pesa demasiado: es el único
que vota.**

**Lo que esta clase NO hace:** no toca `MonitorService`, la Config ni COCO.
La invalidación de Δ_r en el cambio de W sigue siendo de Monitor (D2), y se
lee en `panel["Delta_r_reset"]`.

**`calibrate` corre desde el 19 oct** (delamor), sobre la W candidata y antes
del rebuild: el punto dejó de ser un marcador vacío. En el intento 3 de
`serie2_caso0` **produjo los umbrales que COCO usó** (`D_CKM_THRESHOLD =
0.00571`, `FRAC_REC_MIN = 0.99488`, `source: "calibrate"` en 3 de 27
evaluaciones). Acá decía *"existe y no hace nada"*, que era la versión
anterior del mecanismo (`TASK_calibrate_mecanismo_v1`); corregido el 24 oct
2026 al chequear los docstrings contra el código.

Nota de integración con services/:
  - CorpusService.ingest(texts) es el método real de acumulación (no
    "accumulate" como se llama en NodeExtractorService).
  - MonitorService.evaluate(text, device_id=None) requiere el texto de
    cada evaluación — no es un evaluate() sin argumentos.
  - FirmaService.firmar(corpus, monitor, n_agentes) es stateless; no
    guarda referencia a corpus/monitor por sí sola. `n_agentes` es
    **obligatorio y sin default** desde el 9 oct: un default no es un conteo.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

_SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
if str(_SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(_SERVICES_DIR))

from behavior_graph import BehaviorGraph  # noqa: E402
from ckm_landscape_config import CKMlandscapeConfig  # noqa: E402
from corpus_service import CorpusService  # noqa: E402
from firma_ckm import FirmaService  # noqa: E402
from monitor_service import MonitorService  # noqa: E402
from calibrate import calibrate, NULO_CALIBRADO  # noqa: E402
from w_version import sha256_W  # noqa: E402
from landscape_engine import D_CKM_FORMA  # noqa: E402
from node_extractor import MIN_DF, PERFIL_ES_EN, DECLARACION_REF  # noqa: E402
from iap_chatroom import run_store  # noqa: E402
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

# **Qué criterios VOTAN.** El default son los tres, que es el comportamiento de
# hoy: el `criterios_rebuild` del constructor no cambia nada si no se pasa.
#
# Existe porque delamor pidió una PoC: *"que should_rebuild no sea dominado por
# min_texts… el peso que tiene min_texts en el criterio está sumando demasiado.
# Por eso digo cero… que no sea criterio min_texts… nulo"*.
#
# **Cero quiere decir peso nulo, no umbral 0.** Con `min_texts = 0` el criterio
# de volumen queda en `>= 0` —verdadero siempre— y como está antes del tiempo en
# la jerarquía, los otros dos **no llegan a operar**: un umbral 0 no quita el
# criterio, lo vuelve dominante. Eso además convierte la ausencia en un valor
# (I2). Así que "peso nulo" se implementa **sacando al criterio de la votación**,
# no bajándole el umbral.
CRITERIOS_POR_DEFAULT = (CAUSA_ESTRUCTURAL, CAUSA_VOLUMEN, CAUSA_TIEMPO)

# ───────────────────────────────────────────────────────────────────────────
# Serie 2 del canal IAP — la identificación y los parámetros de la tabla
# (`docs/tasks/TASK_iap_serie2_caso0_v1.md`, CP1 (c) y (d)).
#
# **La Serie 2 no tiene nada que ver con la serie 1** (casos 0.4–0.15,
# congelada en `process/iap_series_freeze_20261008/`): no se compara con ella,
# no la continúa y no la reinterpreta. Por eso la identificación viaja en el
# panel y en cada decisión registrada, y no se deduce de la fecha.
SERIES = "S2"
CASE = "S2-C0"

# Los "parámetros sensatos mínimos" de la TASK. **Declarados, no calibrados.**
# Cada uno con la razón por la que no es ridículo, que es todo lo que la TASK
# les pide:
#
#   - `TOP_K = 20` y pool ×3: los ya declarados. Antes el canal usaba 32 — una
#     tercera configuración, distinta de la del módulo y de la del paper.
#   - `MIN_DF` sale de `node_extractor` (2): un nodo que aparece en un solo
#     mensaje no co-ocurre con nada fuera de él.
#   - `MIN_TEXTS_FIRST_W = 30` y `MIN_DEVICES_FIRST_W = 2`: con 7–24 textos
#     N_eff se mueve 3–34× más por la extracción que por el muestreo (CP-E), y
#     una W de un solo device no es interacción.
#   - `REBUILD_EVERY = 10` mensajes: una W por mensaje no es sensato, y
#     `min_texts*2` ataba el rebuild al umbral del primer W — con el 30, el
#     rebuild habría sido cada 60 mensajes sin que nadie lo decidiera.
TOP_K = 20
MIN_TEXTS_FIRST_W = 30
MIN_DEVICES_FIRST_W = 2
REBUILD_EVERY = 10


class CKMMonitor:
    _instance: "CKMMonitor | None" = None

    def __new__(cls, *args, **kwargs) -> "CKMMonitor":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, min_texts: int = MIN_TEXTS_FIRST_W,
                 state_dir: "str | Path | None" = None,
                 criterios_rebuild: "tuple | None" = None,
                 series: str = SERIES, case: str = CASE,
                 rebuild_every: int = REBUILD_EVERY,
                 min_devices_first_w: int = MIN_DEVICES_FIRST_W) -> None:
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
        # **El directorio de la corrida, declarado una sola vez** (punto 3 de
        # `serie2_caso0`). Desde acá lo leen `ChatChannel` —que se construye
        # antes que este monitor y no podría recibirlo por parámetro— y
        # cualquier otra parte de IAP que escriba lo suyo. Si cada uno
        # resolviera su propio directorio, podrían quedar distintos y el log de
        # un vivo quedaría repartido sin que nada lo dijera, que es el problema
        # que F3a ya había encontrado una vez.
        run_store.set_state_dir(state)
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

        # **El extractor muerto se fue** (CP1 (e), decisión de delamor del 15
        # oct). Acá vivía `NodeExtractorService(top_k=32)`, construido y nunca
        # usado: se leía como si alguien evaluara con `top_k=32`, y nadie lo
        # hacía. En el camino vivo queda **un solo extractor**, el de
        # `CorpusService`, que construye W y evalúa σ.
        self._corpus = CorpusService(
            storage_path=str(state / "corpus_state.json"),
            min_texts=min_texts,   # Serie 2: 30 — el primer W espera
            top_k=TOP_K,           # Serie 2: 20, el declarado (antes 32)
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

        # Identificación de la Serie 2 (CP1 (d)). Viaja en el panel y en cada
        # decisión de rebuild registrada.
        self._series = series
        self._case = case
        # Cada cuántos mensajes nuevos vota el criterio de volumen. Antes era
        # `min_texts*2`, que acoplaba el rebuild al umbral del primer W.
        self._rebuild_every = rebuild_every
        # Cuántos devices distintos tienen que haber aportado texto **antes**
        # de que se construya la primera W.
        self._min_devices_first_w = min_devices_first_w

        self._message_count = 0
        self._devices_seen: set[str] = set()
        self._last_panel: dict | None = None
        self._d_ckm_history: list[float] = []
        self._ciclos_sin_rebuild = 0
        # Los criterios que votan. `None` es "los de siempre" y **no** es lo
        # mismo que `()`, que es "ninguno vota": el primero es el default, el
        # segundo es una decisión.
        self._criterios_rebuild = (
            tuple(CRITERIOS_POR_DEFAULT) if criterios_rebuild is None
            else tuple(criterios_rebuild)
        )
        desconocidos = set(self._criterios_rebuild) - set(CRITERIOS_POR_DEFAULT)
        if desconocidos:
            raise ValueError(
                f"criterios_rebuild desconocidos: {sorted(desconocidos)}. "
                f"Los que hay: {CRITERIOS_POR_DEFAULT}"
            )
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
        # El registro de la última corrida de `calibrate`. **Corre**, desde el
        # 19 oct: lo llena `_calibrate()` antes de cada rebuild. `None` hasta
        # que haya habido uno — y por eso **el build de la primera W lo deja
        # en `None`**: no pasa por ese punto
        # (`registers/REG_calibrate_no_corre_en_el_build_v1.md`, 24 oct; el
        # borrador que esta línea citaba en `docs/` ya no existe).
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
            # El device se cuenta **antes** de la ingesta: la condición del
            # primer W mira cuántos devices aportaron texto, y este mensaje es
            # uno de ellos. Contarlo después dejaría el W del mensaje 30
            # decidido con el censo del 29.
            self._devices_seen.add(message.device_id)
            self._corpus.ingest(
                [message.text],
                landscape_signal=signal,
                # **El primer W espera ≥ 30 mensajes de ≥ 2 devices** (tabla
                # de la Serie 2). La cantidad la mira `CorpusService` con su
                # `min_texts`; cuántos devices hay sólo lo sabe el canal.
                #
                # **Acá se probó `allow_first_W=False` el 24 oct 2026 (CP1 de
                # `TASK_calibrate_en_el_build_v1`) y se revirtió el mismo
                # día.** La idea era que `ingest` no construyera ninguna W,
                # para que la primera naciera por el camino de la decisión y
                # pasara por `calibrate`. **La suite lo tumbó: 30 failed, 6
                # errors.**
                #
                # El motivo, medido: el bloque de la decisión construye la
                # primera W **sólo si algún criterio vota**, y el de volumen
                # pide `_textos_desde_rebuild >= rebuild_every`. En el vivo
                # eso se cumple —`min_texts = 30` contra `rebuild_every = 10`,
                # el contador ya pasó 10 cuando el corpus llega a 30—, pero
                # **en las configuraciones donde `min_texts < rebuild_every`
                # W nace más tarde o no nace**, y media suite usa
                # `min_texts = 3` o `5`.
                #
                # Así que `ingest` **no es sólo una segunda puerta: es la que
                # hace que W nazca cuando el corpus alcanza su umbral,
                # independientemente del ritmo del rebuild.** Eso no estaba en
                # la TASK y es lo que la suite agregó.
                allow_first_W=(
                    len(self._devices_seen) >= self._min_devices_first_w
                ),
            )
        sha_after = self._corpus.w_sha()

        self._message_count += 1

        # ── F4 — `"system"` no cuenta como agente ──────────────────────────
        # `_devices_seen` cuenta **device_ids que publicaron**, y el
        # pseudo-device del canal entraba como uno: en los dos vivos, con dos
        # devices que nunca publicaron, `n_agentes` dio **1** y ese 1 era el
        # canal. El canal no es un participante.
        # (el alta de `_devices_seen` ya ocurrió arriba, antes de la ingesta)

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
            # **Y con su historia de D_ckm vacía** (CP4). Va acá, antes de que
            # `evaluate` agregue el punto de este mensaje: ese punto es el
            # primero del ciclo nuevo, medido contra la W nueva.
            #
            # Por qué por ciclo: `D_ckm` se mide **contra el baseline de su
            # ciclo** (`N_eff0` se fija al nacer), así que un gradiente que
            # cruza un salto compara dos cosas medidas contra baselines
            # distintos. El criterio estructural leería una pendiente que no
            # existe en ninguna de las dos mesetas.
            self._d_ckm_history = []
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
        # Cada criterio vota **sólo si está en `_criterios_rebuild`**. La
        # jerarquía no cambia: el orden de los `elif` es el mismo.
        vota = self._criterios_rebuild
        if (CAUSA_ESTRUCTURAL in vota
                and self._corpus.should_rebuild(self._d_ckm_history, n=3)):
            self._last_rebuild_causa = CAUSA_ESTRUCTURAL
        elif (CAUSA_VOLUMEN in vota
                and self._textos_desde_rebuild >= self._rebuild_every):
            # **Por ciclo, no el total** (CP3). El umbral es `rebuild_cada`
            # —10 mensajes en la Serie 2— y **ya no es `2*min_texts`**: con el
            # primer W esperando 30 mensajes, aquella fórmula habría puesto el
            # rebuild cada 60 sin que nadie lo decidiera. Sigue siendo un valor
            # declarado y no calibrado.
            self._last_rebuild_causa = CAUSA_VOLUMEN
        elif (CAUSA_TIEMPO in vota
                and self._ciclos_sin_rebuild >= MAX_CICLOS):
            self._last_rebuild_causa = CAUSA_TIEMPO
        else:
            self._last_rebuild_causa = None

        self._last_rebuild_signal = self._last_rebuild_causa is not None

        # ── la decisión manda el rebuild (TASK, punto 1) ──────────────────
        # `rebuild_suspendido=True` sigue impidiendo el rebuild automático por
        # ingesta; este no pasa por ahí.
        if self._last_rebuild_signal:
            sha_antes = self._corpus.w_sha()
            # ── los contadores CON LOS QUE SE DECIDIÓ (27 oct 2026) ────────
            # Se capturan **acá**, antes de `calibrate`, del rebuild y de los
            # resets de más abajo. `_registrar_decision` los leía al final, o
            # sea **después** de que el bloque de `st.get("rebuild")` los
            # pusiera en cero: toda decisión que movía W registraba
            # `ciclos_sin_rebuild: 0` y `n_puntos_d_ckm: 0` **por
            # construcción**, y el campo que mostraría la evidencia del
            # criterio que disparó valía 0 justamente cuando había disparado.
            #
            # Lo encontró el V1 del texto 08 (hallazgo A, BANDEJA 26 oct) en la
            # única decisión `estructural` de un vivo: necesitó 4 puntos para
            # disparar y la línea decía 0.
            #
            # Entre este punto y el registro **nada toca estos contadores**:
            # `_calibrate` escribe `_punto_calibrate` y los umbrales de
            # Monitor, y `rebuild_por_decision` toca el corpus. Así que esto es
            # el valor que tenían al votar (`:469-484`).
            contadores_al_decidir = {
                "ciclos_sin_rebuild": self._ciclos_sin_rebuild,
                "n_puntos_d_ckm": len(self._d_ckm_history),
            }
            allow_first_w = (
                len(self._devices_seen) >= self._min_devices_first_w
            )
            # ── `calibrate`, ANTES del rebuild (delamor, 19 oct) ───────────
            # Sólo si el rebuild va a ocurrir: calibrar una W que no se va a
            # instalar sería calibrar contra nada. El motivo lo da el corpus,
            # que es quien tiene la condición.
            reason = self._corpus.no_rebuild_reason(allow_first_w)
            if reason is None:
                self._punto_calibrate = self._calibrate(clock)
            else:
                # **No se calibró, y se ve por qué.** No es "calibró y no
                # separó" (`no_calibrado`): es que no hubo salto que calibrar.
                self._punto_calibrate = {
                    "existe": True,
                    "implementado": True,
                    "task": "TASK_calibrate_mecanismo_v1",
                    "state": NULO_CALIBRADO,
                    "values": {},
                    "reason": reason,
                    "moment": "antes del rebuild, sobre la W candidata",
                }
            st = self._corpus.rebuild_por_decision(
                self._last_rebuild_causa,
                # **El mismo permiso que en la ingesta.** Sin esto, el criterio
                # de volumen construía la primera W con un solo device.
                allow_first_W=allow_first_w,
            )
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
                # La historia de D_ckm, por ciclo (CP4). Acá el reset va
                # **después** de que `evaluate` corrió: el punto de este
                # mensaje se midió contra la W **anterior** al salto, así que
                # pertenece a la meseta que se cierra y no a la que nace.
                self._d_ckm_history = []
                # (`calibrate` ya corrió, **arriba y antes** del rebuild,
                # sobre la W candidata. Acá no queda nada de él: el 18 oct
                # corría en este punto —después de instalar W— y eso era el
                # camino de respaldo puesto como regla.)
            # La decisión queda en el jsonl **haya movido W o no** (CP2b): el
            # caso que no la mueve es justamente el que `w_version` no registra.
            self._ultimo_rebuild["registro"] = self._registrar_decision(
                self._last_rebuild_causa, st, sha_antes, clock,
                contadores_al_decidir,
            )

        # El estado de la decisión, en cada mensaje: mismo mecanismo que el
        # `save()` de CorpusService, que también guarda en cada ingesta.
        self._guardar_rebuild_state()

    def _calibrate(self, clock: "dict | None" = None) -> dict:
        """
        Corre `calibrate` **sobre la W candidata, antes de instalarla**, y deja
        los umbrales para el COCO que nace con el ciclo siguiente.

        **Dónde va esto en el flujo** (delamor, 19 oct, corrigiendo la
        condición 5 de la TASK): *"el punto es `should_rebuild`, allí… en ese
        momento del flujo, allí se calibra; antes del rebuild, digamos"*.
        Decidido el rebuild, se calibra la W que el rebuild **va a** instalar,
        todavía dentro del ciclo i; recién después se instala y nace el COCO
        del ciclo i+1 con esos umbrales. **Los números son los mismos** —es la
        misma W—; lo que cambia es el orden, y el orden es el del diseño del 10
        oct: la calibración pertenece al cierre del ciclo i, no a la apertura
        del siguiente.

        **Lo que esto NO es:** la sombra. El diseño confirmado el 10 oct
        (`TASK_calibrate_mecanismo_v1`, punto 3) calibra **durante la meseta**
        sobre una W candidata en sombra y compara el sha en el salto. S2-C0 va
        **sin sombra** (delamor, 19 oct, opción B) y eso se declara: acá
        `calibrate` corre **en el hilo del mensaje**, y mientras calibra **el
        canal no atiende**. La sombra queda como propuesta.

        Devuelve lo que va al panel. `estado` es uno de los tres de
        `calibrate.py`: `calibrado` (separa), `no_calibrado` (corrió y no
        separa) o `nulo_calibrado` (no se ejecutó). Además lleva dos shas que
        son los que permiten ver el orden desde afuera: el de la **candidata**
        (`w_sha`) y el de la que estaba **viva al calibrar**
        (`w_sha_live_at_calibration`). Si fueran iguales habiendo cambiado W,
        la calibración habría corrido después de instalar.

        **Sólo lo llama el camino del rebuild** (`on_message`, el bloque de la
        decisión). La primera W la construye `ingest()` antes de ese bloque,
        así que **no pasa por acá** y el COCO del primer ciclo arranca con los
        defaults. Medido en las dos corridas vivas: su `calibration.estado` es
        `None` —ni siquiera `nulo_calibrado`—, 11 de 51 evaluaciones en el
        intento 2 y 4 de 27 en el 3
        (`registers/REG_calibrate_no_corre_en_el_build_v1.md`, que es el REG
        con el OK de delamor; el borrador en `docs/` ya no existe).

        No instancia nada nuevo: usa `services/calibrate.py` donde está, y le
        pasa una copia que `calibrate` vuelve a copiar y no toca.
        """
        t0 = time.monotonic()
        sha_vigente = self._corpus.w_sha()
        W = self._corpus.candidate_W()
        sha_candidata = sha256_W(W) if W is not None else None
        registro = calibrate(W, w_sha=sha_candidata, clock=clock)
        self._monitor.set_coco_thresholds(registro.get("valores"), registro)
        return {
            "existe": True,
            "implementado": True,
            "task": "TASK_calibrate_mecanismo_v1",
            # La W **candidata**: la que se calibró y la que el rebuild
            # instala a continuación.
            "w_sha": sha_candidata,
            # La que estaba viva **en el momento de calibrar**. Es el dato que
            # hace visible el orden.
            "w_sha_live_at_calibration": sha_vigente,
            "moment": "antes del rebuild, sobre la W candidata",
            "state": registro["estado"],
            "values": registro.get("valores") or {},
            "conditions": registro.get("condiciones"),
            # Qué se hizo con el resultado: los umbrales entran en el COCO del
            # ciclo SIGUIENTE, no en el que está corriendo.
            "applied_to": "el COCO del proximo ciclo",
            # **Cuánto tardó, medido.** Corre en el hilo del mensaje: esto es
            # el tiempo que el canal no atendió. Va al panel porque es el
            # insumo de la propuesta de la sombra.
            "duration_s": round(time.monotonic() - t0, 4),
            "blocking": True,
        }

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
            # **Por ciclo desde el CP4.** Hasta el CP2b se persistía acumulada
            # y el archivo lo declaraba así; ahora se reinicia en cada rebuild.
            "d_ckm_history_es_por_ciclo": True,
            "nota": "d_ckm_history del ciclo vigente; se reinicia en el rebuild",
        }, ensure_ascii=False))

    def _registrar_decision(self, causa: str, st: dict,
                            sha_antes: "str | None", clock: dict,
                            contadores: dict) -> dict:
        """
        Una línea en `rebuild_decisions.jsonl` por **decisión tomada**.

        El núcleo es el par `w_sha_antes` / `w_sha_despues` con `w_cambio`
        explícito: `w_version` **deduplica por sha**, así que una decisión que
        no mueve W **no deja versión**, y sin esta línea no quedaría en ningún
        lado. Con `w_cambio` se distingue de un salto.

        `contadores` son los de **el momento de decidir**, capturados por
        `on_message` antes de los resets, y es un parámetro **obligatorio y sin
        default** (misma forma que `causa` y que `n_agentes`): leerlos acá los
        leía después del reset, y entonces `ciclos_sin_rebuild` y
        `n_puntos_d_ckm` valían 0 en toda decisión que movía W. El sentido de
        `n_puntos_d_ckm` es poder saber si el estructural **pudo evaluarse**
        —con menos de `n+1` no se evaluó, que no es lo mismo que haberse
        evaluado y dado False (CP2b)— y con el 0 por construcción no se podía.
        Corregido el 27 oct 2026 (CPa de `TASK_calibrate_en_el_build_v2`).

        **`textos_desde_rebuild` sigue sin estar en la línea**, y es el
        contador del criterio que más dispara: está propuesto desde el ítem 5
        del 22 oct y agregar un campo es otra decisión, no ésta.

        `reloj` viene del **mismo reloj del canal** que sella los mensajes
        (`ChatChannel.get_clock()`), no de un `time.time()` aparte.

        Las vueltas **sin** señal no se registran (acordado): una línea por
        mensaje sería el ruido que el filtro del CP2b del canal existe para
        evitar.
        """
        sha_despues = self._corpus.w_sha()
        reg = {
            # La identificación va en **cada registro**, no sólo en el panel:
            # un jsonl suelto tiene que decir de qué serie es (CP1 (d)).
            "series": self._series,
            "case": self._case,
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
            # Los dos del momento de decidir, no los de después del reset.
            "ciclos_sin_rebuild": contadores["ciclos_sin_rebuild"],
            "n_puntos_d_ckm": contadores["n_puntos_d_ckm"],
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

        # El bloque de COCO sale del panel de Monitor, que es quien lo tiene.
        # Sin panel todavía —nadie evaluó— se dice así y no se inventa un
        # "conectado: False", que diría otra cosa.
        if self._last_panel is not None:
            coco = self._last_panel.get("coco")
        else:
            coco = {"connected": None,
                    "reason": "no evaluation yet"}
        tick = ChatChannel().tick()

        return {
            # ── identificación (CP1 (d)) ──────────────────────────────────
            # Va **primero y siempre**, aunque no haya nada medido: un panel
            # suelto tiene que poder decir de qué serie y de qué caso es. La
            # Serie 2 no se mezcla con la serie 1.
            "series": self._series,
            "case": self._case,
            "corpus_size": status["n_texts"],
            "n_nodes": status["n_nodes"],
            "message_count": self._message_count,
            # D_ckm es **la forma por masas de cuenca** y la única que el panel
            # de la Serie 2 lleva (CP1 (b)): 1 − ln N_eff / ln N_eff_0, con
            # N_eff = 1/Σm². El **conteo de atractores no se reporta** acá ni
            # como D_ckm ni como medida del campo.
            "D_ckm": d_ckm,
            "D_ckm_form": D_CKM_FORMA,
            "temp_signal": temp_signal,
            # El bloque de COCO: la conexión, comprobable durante el caso.
            "coco": coco,
            # ── el reloj del canal, en el panel (CP1 (f)) ─────────────────
            # Se lee con `tick()`, que **deriva el tick del reloj y no lo
            # registra**: mirar el panel no puede dejar una entrada en el log
            # de ticks observados, que es de los devices.
            "tick": tick,
            "n_agentes": len(self._devices_seen),
            "corpus_status": corpus_status,
            # ── los parámetros declarados de la extracción (CP1 (c)) ──────
            # En el panel para que una corrida no haya que reconstruirla desde
            # el código que la corrió. Son valores **declarados, no
            # calibrados**.
            "parameters": {
                "top_k": TOP_K,
                "min_df": MIN_DF,
                "pool": TOP_K * 3,
                "n_stopwords": len(PERFIL_ES_EN.stopwords),
                "ngram_max": 2,
                "min_texts_first_W": self._corpus.min_texts,
                "min_devices_first_W": self._min_devices_first_w,
                "rebuild_every": self._rebuild_every,
                "n_runs": self._landscape_config.n_runs,
                "unit": "el mensaje",
                "system_to_corpus": False,
                "declaration": DECLARACION_REF,
            },
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
            # **Quiénes votaron.** Sin esto, una corrida con el volumen fuera
            # se vería igual que una donde el volumen no llegó a su umbral.
            "criterios_rebuild": list(self._criterios_rebuild),
            "criterios_por_default": (
                tuple(self._criterios_rebuild) == CRITERIOS_POR_DEFAULT
            ),
            "rebuild_senal": self._last_rebuild_signal,
            "rebuild_causa": self._last_rebuild_causa,
            "ultimo_rebuild_por_decision": self._ultimo_rebuild,
            # El registro de la última corrida de `calibrate`, en el panel
            # para que no haya que buscarlo. **Corre** desde el 19 oct; acá
            # decía "existe y no hace nada", de la versión anterior del
            # mecanismo (corregido el 24 oct al chequear los docstrings).
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
