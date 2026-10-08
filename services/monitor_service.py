"""
monitor_service.py — Collective MonitorService

Stateful. Evalúa prompts contra el corpus acumulado.
Mide fabricación: lo que σ_prompt declaró y el campo no sostuvo.

Δ_r acumula la metabolización del campo:
  pares (i,j) que σ_prompt declaró activos y la relajación no sostuvo
  (al menos uno de los dos queda en −1). Quedan adentro, como deformación en
  W_eff — no se expulsan. Δ_r[i,j] += 1 por cada evaluación.
  Los nombres en código (`_rejected_pairs`, panel["rechazados"]) se conservan:
  son claves de JSONLs históricos. DEFS v12 §9, PROPUESTA v5 D4.

σ_prompt sale del mismo analizador que construye W (NodeExtractor, una sola
rama — 7bf485b). Δ_r y A0 se descartan en cualquier reconstrucción de W (D2).

Rango de W (heredado de CorpusService): W ∈ [−1, +1]. `_rebuild()` calcula
(pos_counts − neg_counts) / max|·|, y rutea a neg_counts los textos con
marcador de oposición. c(S) es informativo cuando hay tensión estructural,
que es justamente lo que codifican los pesos negativos.

COCO (thermostat) es opcional — `thermostat=None` por defecto. Sin él no
hay compresión de Δ_r, ni β, ni temp_signal, y `panel["thermostat"]` es
None; el resto del panel se emite igual. Con él, COCO lee Δ_r y comprime
su propia representación (Δ_r_compresiones); Δ_r no recibe nada de COCO
(D3, ver evaluate()).

Este docstring describe lo que el código no dice de sí mismo. La firma del
constructor, el cuerpo de evaluate() y la escala de _combine_W_Delta viven
en el código, y ahí se leen — copiarlos acá crea una rama que se congela
sin señal de estar desactualizada.
"""

from __future__ import annotations
import json
import time
from pathlib import Path
from typing import List, Optional

import numpy as np

from node_extractor import NodeExtractorService
from corpus_service  import CorpusService
from coco import COCO, ThermostatState, BETA_RHO_STAR
from ckm_landscape_config import CAUSA_BOOTSTRAP, CKMlandscapeConfig
from landscape_engine import (
    fases_de_orbita,
    pares_por_orbita,
    d_ckm,
    D_CKM_FORMA,
    beta_c_landscape,
    boltzmann_warmup,
    basin_masses,
    count_attractors,
    d_masa_cuencas,
    n_eff,
    node_probs,
    relax,
    relax_orbit,
    sample_s0,
)

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
        n_runs_attractors: int = 1000,
        thermostat      : Optional[COCO] = None,
        coco_config     : Optional[dict] = None,
        behavior_graph  : Optional[object] = None,   # BehaviorGraph | None
        count_seed      : int = 0,
        sampling_mode   : str = "uniform",
        n_warmup        : Optional[int] = None,
        landscape_config: Optional[CKMlandscapeConfig] = None,
    ):
        """
        count_seed / sampling_mode / n_warmup gobiernan el muestreo de
        sigma_0 en _count_attractors(). Sus defaults —seed=0, uniform—
        son los valores que este servicio usaba hardcodeados, de modo que
        el comportamiento numerico no cambia. Ver TASK_monitor_service_
        unificar_rutinas_v1.md: la equivalencia con COCO(seed=0) fue
        verificada exacta antes de unificar.

        n_runs_attractors: muestras de sigma_0 para contar atractores (D_ckm)
        y masas de cuenca (N_eff). Default 1000: en casos IAP N_eff converge
        ahí (±2% de 5000); con 50 quedaba 5–20% bajo. El conteo de A no
        satura con ningún n_runs. El panel lleva "saturacion" para cuando
        N_eff tampoco converge. TASK_n_runs_panel_saturacion_v1.

        landscape_config: config del instrumento, ya construida por quien
        arma el run — Monitor no decide calibración. Es la config del
        contador de Monitor, no la de COCO.

        **Monitor abre los ciclos (D4).** Cuando W cambia,
        _invalidar_si_W_cambio llama a config.abrir_ciclo con la misma causa
        que devuelve, en el mismo bloque donde descarta Δ_r y A0. Ningún otro
        servicio lo llama, y Monitor ya no detecta el cambio de ciclo por su
        cuenta: lo detecta una vez y lo escribe en la config (I2).

        Esto cierra el gap D7: la config ya no se queda atrás tras un
        rebuild, porque gana un ciclo en vez de quedar vieja. El panel lleva
        config.panel() —identidad, declarado y ciclo vigente, sin la
        historia (I7)—, no la config completa.

        Ver docs/tasks/TASK_CKMlandscapeConfig_v3.md y
        docs/tasks/TASK_landscape_config_en_runs_v1.md.
        """
        self.corpus    = corpus
        self._storage  = Path(storage_path)
        self._extractor = NodeExtractorService()
        self._n_runs   = n_runs_attractors
        # ── COCO: configuración, no instancia (D4 + §1 de
        # TASK_monitor_coco_ciclo_orbita_v2) ─────────────────────────────────
        # Monitor y COCO son aspectos de lo mismo: nacen, viven y mueren
        # juntos. El reloj es el ciclo vigente de la Config, que Monitor abre.
        # Por eso Monitor recibe CÓMO construir a COCO y lo construye él, en
        # el mismo bloque donde abre el ciclo.
        #
        # `thermostat=COCO(...)` sigue aceptado **sólo en transición**: una
        # instancia externa NO renace, y eso se declara en el panel como
        # coco_externo=True. Es el camino de los tests Armstrong, que son
        # traza y no se modifican.
        self._coco_config = dict(coco_config) if coco_config else None
        if thermostat is not None and coco_config is not None:
            raise ValueError(
                "thermostat y coco_config son excluyentes: o se pasa una "
                "instancia externa (que no renace) o se pasa cómo construirla"
            )
        if coco_config is not None and landscape_config is None:
            # Una sola existencia necesita un solo reloj, y el reloj es el
            # ciclo vigente de la Config. Sin Config no se abre ningún ciclo,
            # así que COCO nacería una vez y no volvería a renacer: en el
            # primer rebuild que cambie N, observe() rompería con
            # ValueError de shapes — es lo que el CP1 midió. No se acepta una
            # configuración cuya falla está garantizada.
            raise ValueError(
                "coco_config requiere landscape_config: COCO renace con el "
                "ciclo, y sin Config no hay ciclo que abrir. Para un COCO que "
                "no renace, pasarlo como thermostat= y queda declarado como "
                "instancia externa."
            )
        self._coco_externo = thermostat is not None
        self._thermostat = thermostat
        self._g         = behavior_graph

        if sampling_mode not in ("uniform", "weighted", "boltzmann"):
            raise ValueError(
                f"sampling_mode invalido: {sampling_mode!r} — "
                "esperado 'uniform', 'weighted' o 'boltzmann'."
            )
        self._count_seed    = count_seed
        self._sampling_mode = sampling_mode
        self._n_warmup      = n_warmup
        if landscape_config is not None and landscape_config.sampling_mode != sampling_mode:
            raise ValueError(
                f"landscape_config.sampling_mode={landscape_config.sampling_mode!r} "
                f"no coincide con sampling_mode={sampling_mode!r} de este Monitor — "
                "el panel llevaría una config que no describe cómo contó."
            )
        self._landscape_config = landscape_config

        self._Delta_r : Optional[np.ndarray] = None
        self._A0    : Optional[float]        = None
        self._N_eff0: Optional[float]      = None   # baseline de N_eff, vive con A0
        # versión de W bajo la que se acumuló Δ_r — ver _invalidar_si_W_cambio
        self._w_sha   : Optional[str]       = None
        self._w_nodes : Optional[list]      = None
        # traza del renacimiento de COCO — se expone en el panel
        self._coco_renacio     : bool          = False
        self._coco_generacion  : int           = 0
        self._coco_id_anterior : Optional[int] = None
        # w_version_id del ciclo al que pertenece el COCO vigente
        self._coco_sha         : Optional[str] = None

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

        reset_cause = self._invalidar_si_W_cambio(nodes)

        if self._Delta_r is None or self._Delta_r.shape != (N, N):
            self._Delta_r = np.zeros((N, N))

        # σ declarado por el prompt
        sigma_prompt = self._extractor.evaluate(text, nodes)

        # σ que el campo acepta
        W_eff_prompt = self._combine_W_Delta(W, self._Delta_r)
        # La órbita es el objeto (§1). Se mide sobre las dos fases; qué entra a
        # Δ_r NO cambia todavía — eso es el CP3 y es de delamor. sigma_relaxed
        # sigue siendo la fase que cae en max_iter, igual que hoy.
        orbita, periodo, cola, sigma_relaxed = self._relax_orbit(
            sigma_prompt.copy(), W_eff_prompt
        )
        aceptados, expulsados, torsion = pares_por_orbita(
            sigma_prompt, fases_de_orbita(orbita, N)
        )

        # pares rechazados → acumular en Δ
        rejected = self._rejected_pairs(sigma_prompt, sigma_relaxed)
        for i, j in rejected:
            self._Delta_r[i, j] += 1
            self._Delta_r[j, i] += 1

        # métricas
        c_s   = self._cS(sigma_relaxed, W)
        fi    = self._fabrication_index(sigma_prompt, sigma_relaxed)
        D_ckm = self._D_ckm(W)
        N_eff = self._N_eff(W)

        # G_state — paralelo a {W, Δ_W}, no retroactivo
        g_state_panel = None
        if self._g is not None:
            self._g.ingest([text])
            g_state_panel = self._g.g_state()
            g_state_panel["active_behavior"] = self._g.active_nodes(text)

        panel = {
            "c_S"              : round(c_s,  6),
            "fabrication_index": round(fi,   4),
            "D_ckm"            : round(D_ckm, 4) if D_ckm is not None else None,
            # N_eff = 1/Σm² sobre masas de cuenca por órbita, misma W_eff y
            # mismas muestras que D_ckm. N_eff0 es su baseline (se fija y se
            # resetea como A0). D_masa_cuencas en escala log (delamor):
            # 1 − ln N_eff / ln N_eff0; None si N_eff0 ≤ 1.
            "N_eff"            : round(N_eff, 4),
            "N_eff0"           : round(self._N_eff0, 4) if self._N_eff0 is not None else None,
            "D_masa_cuencas"   : (lambda d: round(d, 4) if d is not None else None)(
                                     d_masa_cuencas(N_eff, self._N_eff0)),
            "saturacion"       : self._saturacion,
            # Condiciones de la medición — no se excluye nada, se declara.
            # Un aislado (fila de W en cero) duplica cada atractor acoplado;
            # Δ_r puede acoplarlo en W_eff durante el run (REG v3 §4).
            # REG_hipotesis_distancia_contextual_v4.
            "condicion_W"      : self._condicion_W(W, nodes),
            "n_rejected_pairs" : len(rejected),
            "Delta_r_sum"        : float(np.sum(self._Delta_r)),
            "activos_prompt"   : [nodes[i] for i, s in enumerate(sigma_prompt)   if s > 0],
            "activos_relajado" : [nodes[i] for i, s in enumerate(sigma_relaxed)  if s > 0],
            "rechazados"       : [(nodes[i], nodes[j]) for i, j in rejected],
            # modo con el que ESTE servicio conto atractores para D_ckm.
            # Distinto del de panel["thermostat"]["sampling_mode"], que es
            # el de COCO: son dos contadores independientes.
            "sampling_mode"    : self._sampling_mode,
            "thermostat"       : None,
            "G_state"          : g_state_panel,
            # None si Δ_r siguió acumulando; "N" | "nodos" | "pesos" si esta
            # evaluación empezó con Δ_r y A0 en cero por reconstrucción de W.
            # La órbita completa, no la fase que cayó en max_iter (§1).
            # `rechazados` y `n_rejected_pairs` siguen saliendo de la fase, que
            # es lo que hoy entra a Δ_r; estas tres clases se registran al lado
            # y no se promedian: la torsión es la marca del período 2, y el
            # coseno la llevaría a 0. Qué entra a Δ_r es el CP3.
            "periodo_orbita"   : periodo,
            "cola_orbita"      : cola,
            "n_aceptados"      : len(aceptados),
            "n_expulsados"     : len(expulsados),
            "n_torsion"        : len(torsion),
            "pares_torsion"    : [(nodes[i], nodes[j]) for i, j in sorted(torsion)],
            "Delta_r_reset"    : reset_cause,
            # COCO renace con el ciclo, en el mismo bloque y con la misma
            # causa que Delta_r_reset (§1). True sólo en la evaluación del
            # renacimiento. coco_externo=True: instancia pasada desde afuera,
            # que NO renace — aceptada sólo en transición.
            "coco_renace"      : self._coco_renacio,
            "coco_generacion"  : self._coco_generacion,
            "coco_externo"     : self._coco_externo,
            # Admisión (node-level, C1) y metabolización (pair-level, Δ_r)
            # son objetos distintos. Nadie evalúa C1 todavía: None dice que
            # esta Δ_r se acumuló sin admisión previa. Cuando alguien lo
            # conecte, esta clave lleva al menos el θ_W usado.
            # Ver docs/tasks/TASK_traza_gatekeeper_c1_v1.md.
            "gatekeeper_c1"    : None,
            # I7: identidad + declarado + ciclo vigente. La historia de
            # ciclos vive en la config, no viaja en cada panel.
            "landscape_config" : (
                self._landscape_config.panel()
                if self._landscape_config is not None else None
            ),
        }

        self._coco_renacio = False      # se consumió en este panel

        # COCO lee Δ_r y regula su propia representación (D3). La
        # regulación no llega a Δ_r: Monitor es su único escritor.
        if self._thermostat is not None:
            if device_id is not None:
                self._thermostat.register_device_eval(device_id, fi)
            ts = self._thermostat.observe(self._Delta_r)
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
                # modo de muestreo de sigma_0 que produjo este D_ckm —
                # uniform | weighted | boltzmann. Trazabilidad: el mismo
                # Δ_r puede caer de un lado u otro de D_CKM_THRESHOLD
                # según el modo (REG_stochastic_eval_v2).
                "sampling_mode": getattr(self._thermostat, "_sampling_mode", None),
                "n_warmup": (
                    getattr(self._thermostat, "_n_warmup", None)
                    if getattr(self._thermostat, "_sampling_mode", None) == "boltzmann"
                    else None
                ),
            }

        self._persist(text, panel, device_id)
        return panel

    def _invalidar_si_W_cambio(self, nodes: list) -> Optional[str]:
        """
        Δ_r y A0 se descartan en cualquier reconstrucción de W (D2), y la
        config abre un ciclo nuevo (D4).

        Aunque los índices sean los mismos, los pesos que produjeron esa Δ_r
        ya no son los vigentes; y A0 sería el baseline de otro campo. La
        señal es w_version_id. Devuelve la causa —"N" | "nodos" | "pesos"—
        o None si W no cambió. COCO queda fuera de alcance: sigue operando
        con la W de su construcción.

        **Monitor es el único que abre ciclos (D4).** Lo hace acá, en el
        mismo bloque donde descarta Δ_r: la detección del cambio de W ocurre
        una sola vez y queda escrita en la config, así que ningún consumidor
        tiene que detectarla por su cuenta (I2). La causa que viaja al ciclo
        es la misma que devuelve este método — el vocabulario de causas de
        Monitor ("N" | "nodos" | "pesos") es más fino que el de la TASK v2
        ("rebuild" | "estructural" | "volumen"), y `Ciclo.causa` es str
        libre, así que entra sin traducirse.

        En la **primera** evaluación Δ_r no se descarta —no hay nada que
        descartar— pero la config igual puede estar atrás: se construyó con
        una W y W pudo cambiar antes de la primera llamada. Ahí también se
        abre ciclo. Si la W es la misma, `abrir_ciclo` devuelve False y no
        pasa nada (I5).

        Ver docs/tasks/TASK_invalidacion_delta_r_v1.md y
        docs/tasks/TASK_CKMlandscapeConfig_v3.md.
        """
        sha_actual = self.corpus.w_sha()

        if self._w_sha is None:                       # primera evaluación
            self._w_sha, self._w_nodes = sha_actual, list(nodes)
            self._abrir_ciclo_si_cambio(sha_actual)
            return None

        if sha_actual == self._w_sha:
            return None

        causa = self._causa_cambio(self._w_sha, self._w_nodes)

        self._Delta_r = np.zeros((len(nodes), len(nodes)))
        self._A0      = None
        self._N_eff0  = None
        self._w_sha, self._w_nodes = sha_actual, list(nodes)
        self._abrir_ciclo_si_cambio(sha_actual, causa)
        return causa

    def _causa_cambio(self, sha_viejo: str, nodes_viejos: Optional[list]) -> str:
        """Por qué cambió W: "N" si cambió el tamaño, "nodos" si las
        etiquetas, "pesos" si sólo los valores."""
        cambio = self.corpus.w_change_since(sha_viejo, nodes_viejos)
        if cambio["N_old"] != cambio["N_new"]:
            return "N"
        if cambio["nodes_changed"]:
            return "nodos"
        return "pesos"

    def _abrir_ciclo_si_cambio(
        self, sha_actual: str, causa: Optional[str] = None
    ) -> bool:
        """
        Le pide a la config un ciclo nuevo para la W vigente (D4).

        Sin config no hay nada que abrir. Si la config ya está en este
        w_version_id, `abrir_ciclo` devuelve False por I5 y no se agrega
        nada. Cuando `causa` es None —primera evaluación— se calcula contra
        el ciclo vigente de la config, no contra el sha de Monitor, porque
        lo que quedó atrás es la config.

        No pasa `t_senal`: la señal de rebuild existe (`should_rebuild` en
        ckm_monitor.py) pero no llega hasta acá, así que la deriva queda
        nula —no cero— que es lo que I6 pide cuando nadie señaló.

        **La causa contra la config no siempre es derivable.** Cuando hay
        que calcularla contra el ciclo vigente —primera evaluación— sólo se
        puede distinguir "N", porque el ciclo guarda N pero no las
        etiquetas: `nodes` quedó fuera de lo medido (P5, porque no es
        función de W) y `CorpusService.w_change_since` las necesita del que
        consulta, ya que no se persisten por versión. Con N igual no se
        puede decir si cambiaron las etiquetas o sólo los pesos, y la causa
        es **"W_distinta"**: el sha es otro, y con lo que el ciclo guarda no
        se puede decir más. No se inventa una causa más precisa.
        """
        abrio = self._abrir_ciclo(sha_actual, causa)
        self._sincronizar_coco_con_el_ciclo()
        return abrio

    def _sincronizar_coco_con_el_ciclo(self) -> None:
        """
        Una existencia de COCO por ciclo. Renace cuando el ciclo cambia.

        La §1 dice "COCO renace si y solo si se abrió un ciclo nuevo". Se
        implementa comparando el `w_version_id` del ciclo vigente contra el del
        COCO que hay, en vez de mirar si `abrir_ciclo` devolvió True. Son
        equivalentes mientras Monitor sea el único que abre ciclos (I2), y la
        comparación cubre además el caso que el evento no cubre: una Config
        construida con `create()` **ya trae su ciclo bootstrap abierto** antes
        de que Monitor exista, así que no se abre ninguno y COCO no tendría
        nacimiento. Lo encontró un test del CP2b.

        El invariante queda más fuerte: el COCO vigente es siempre el del ciclo
        vigente, sin importar quién abrió el ciclo ni cuándo.
        """
        if self._coco_config is None:
            return
        cfg = self._landscape_config
        if cfg is None or not cfg.ciclos:
            return
        sha = cfg.ciclo_vigente.w_version_id
        if sha != self._coco_sha:
            self._renacer_coco()
            self._coco_sha = sha

    def _renacer_coco(self) -> None:
        """
        COCO nace de nuevo con el ciclo. Una sola existencia (§1).

        Renace **si y solo si** se abrió un ciclo, en el mismo bloque y con la
        misma causa. Nace vacío: Δ propio en ceros, A0 y N_eff0 en None, igual
        que Δ_r y A0 de Monitor. La primera división del ciclo nuevo se hace
        contra ese vacío, y el vacío se declara — no se lee como estabilidad
        (CP2c).

        Sin `coco_config` no hay nada que renacer: o no hay COCO, o es una
        instancia externa que se declaró como tal y **no renace**. Ésa es la
        divergencia que el CP1 midió rompiendo con
        `ValueError: shapes (31,31) (28,28)`: COCO se quedaba con la N de su W
        y Monitor crecía. Con el renacimiento, la N de COCO es siempre la de la
        W del ciclo vigente.

        `n_runs`, `seed` y `sampling_mode` **salen de la Config** (declarado,
        P9): no son defaults de COCO. Lo demás —`track_landscape`, `n_warmup`,
        `gamma`, umbrales— viene de `coco_config`.
        """
        if self._coco_config is None:
            return
        cfg = self._landscape_config
        kw = dict(self._coco_config)
        if cfg is not None:
            kw.setdefault("n_runs", cfg.n_runs)
            kw.setdefault("seed", cfg.seed)
            kw.setdefault("sampling_mode", cfg.sampling_mode)
        else:
            kw.setdefault("n_runs", self._n_runs)
            kw.setdefault("seed", self._count_seed)
            kw.setdefault("sampling_mode", self._sampling_mode)
        anterior = self._thermostat
        self._thermostat = COCO(W=self.corpus.get_W(), **kw)
        self._coco_renacio = True
        self._coco_generacion += 1
        self._coco_id_anterior = id(anterior) if anterior is not None else None

    def _abrir_ciclo(
        self, sha_actual: str, causa: Optional[str] = None
    ) -> bool:
        cfg = self._landscape_config
        if cfg is None:
            return False

        if not cfg.ciclos:
            # Config construida antes de que W existiera — es el caso del
            # canal: el corpus arranca en acumulación y W aparece recién al
            # cruzar min_texts. El primer ciclo lo abre Monitor acá, con
            # causa "bootstrap": el primer rebuild no es degradación, es el
            # origen (PROPUESTA v5).
            return cfg.abrir_ciclo(
                self.corpus.get_W(), CAUSA_BOOTSTRAP, time.time()
            )

        vigente = cfg.ciclo_vigente
        if vigente.w_version_id == sha_actual:
            return False
        if causa is None:
            causa = "N" if vigente.N != len(self.corpus.get_nodes()) else "W_distinta"
        return cfg.abrir_ciclo(self.corpus.get_W(), causa, time.time())

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
        # D_ckm None (baseline ≤ 1) en un extremo de la ventana: no hay
        # tendencia que medir y no hay señal.
        D_trend  = (D_vals[-1] - D_vals[0]
                    if D_vals[-1] is not None and D_vals[0] is not None else None)
        signal   = fi_trend > 0.05 and D_trend is not None and D_trend > 0.02

        return {
            "signal"   : signal,
            "fi_trend" : round(fi_trend, 4),
            "D_trend"  : round(D_trend,  4) if D_trend is not None else None,
            "direction": "CONVERGING" if fi_trend < -0.05 else "DIVERGING" if signal else "STABLE",
        }

    # ------------------------------------------------------------------
    # Operaciones internas
    # ------------------------------------------------------------------

    def _relax_orbit(self, sigma, W, max_iter: int = 200) -> tuple:
        """Órbita alcanzada — landscape_engine.relax_orbit."""
        return relax_orbit(sigma, W, max_iter)

    def _relax(self, sigma: np.ndarray, W: np.ndarray, max_iter: int = 200) -> np.ndarray:
        """
        Estado alcanzado tras max_iter pasos de relajación síncrona —
        landscape_engine.relax.

        max_iter 100 y 200 son ambos PARES: una órbita de periodo 2 devuelve
        la misma fase en los dos, y el test que separa los casos es 100
        contra 101. Medido así: en caso09_run2 natural, 136 de 200 runs NO
        llegan a punto fijo; en WARMUP_TEXTS, 141 de 200; en
        W_ckm_corpus_v2 (N=32), 3 de 200.
        """
        return relax(sigma, W, max_iter)


    def _combine_W_Delta(self, W: np.ndarray, Delta: np.ndarray) -> np.ndarray:
        """
        Combina W y Delta_r en escalas compatibles.

        W ∈ [−1, +1] (normalizado por CorpusService: (pos − neg)/max|·|).
        Delta_r ∈ [0, ∞) (conteos enteros de rechazos).

        Normalización: Delta_r / max(Delta_r) → [0,1],
        luego escala por la media de los pesos POSITIVOS de W para
        preservar magnitud relativa. Si Delta es cero (inicio de sesión),
        devuelve W sin modificar.

        La escala usa solo W>0 — no |W| ni todos los no-cero. Data de
        cuando W era positiva y `W_nonzero` y `W>0` eran el mismo conjunto.
        Se mantiene el comportamiento; queda dicho que es una elección,
        no una consecuencia del rango de W.
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

    def _D_ckm(self, W: np.ndarray) -> Optional[float]:
        """D_ckm es la formula canonica, landscape_engine.d_ckm:
        1 - ln N_eff / ln N_eff0. A_actual y A0 SON N_eff y N_eff0 — solo se
        llaman distinto: _count_attractors devuelve n_eff(basin_masses). Por
        eso el panel lleva el mismo numero en "D_ckm" y en "D_masa_cuencas".
        None si el baseline es <= 1. Aca vive lo que NO se unifica: de donde
        sale A0.

        A0 se fija en la primera llamada con corpus establecido (mode !=
        accumulation), se cuenta sobre _combine_W_Delta(W, Delta_r) — escala
        compatible W + Delta_r — y se resetea cuando W cambia. COCO fija el
        suyo sobre W sola y no lo resetea: una cantidad, dos baselines.
        """
        Delta    = self._Delta_r if self._Delta_r is not None else np.zeros_like(W)
        W_eff    = self._combine_W_Delta(W, Delta)
        A_actual = self._count_attractors(W_eff)
        if self._A0 is None:
            if A_actual == 0:
                return 0.0   # corpus vacío — diferir A0
            self._A0 = A_actual
        return d_ckm(A_actual, self._A0)

    def _condicion_W(self, W: np.ndarray, nodes: list) -> dict:
        """Bajo qué W y con qué muestreo se midió este panel."""
        W_eff = self._combine_W_Delta(W, self._Delta_r)
        return {
            "w_sha"         : self.corpus.w_sha(),
            "N"             : len(nodes),
            "n_runs"        : self._n_runs,
            "count_seed"    : self._count_seed,
            # qué cantidad hay bajo "D_ckm" — ausente en paneles históricos,
            # que llevan la forma por conteo. Ver landscape_engine.D_CKM_FORMA.
            "D_ckm_forma"   : D_CKM_FORMA,
            "aislados_W"    : [nodes[i] for i in np.where(~W.any(axis=1))[0]],
            "aislados_W_eff": [nodes[i] for i in np.where(~W_eff.any(axis=1))[0]],
        }

    def _N_eff(self, W: np.ndarray) -> float:
        """N_eff sobre la misma W_eff que _D_ckm. Fija N_eff0 en la primera
        llamada del ciclo de W (como A0)."""
        Delta = self._Delta_r if self._Delta_r is not None else np.zeros_like(W)
        W_eff = self._combine_W_Delta(W, Delta)
        masas = basin_masses(
            W_eff, n_runs=self._n_runs, seed=self._count_seed,
            weighted=self._sampling_mode == "weighted",
            boltzmann=self._sampling_mode == "boltzmann",
            n_warmup=self._n_warmup,
        )
        valor = n_eff(masas)
        # señal de saturación — continua, sin umbral: cerca de 1, N_eff es del
        # muestreo y no del paisaje. TASK_n_runs_panel_saturacion_v1.
        self._saturacion = {
            "N_eff_sobre_n_runs" : round(valor / self._n_runs, 4),
            "orbitas_unicas_frac": round(float(np.mean(masas * self._n_runs < 1.5)), 4),
        }
        if self._N_eff0 is None:
            self._N_eff0 = valor
        return valor

    # ── Paisaje — delegado en landscape_engine ───────────────────────────
    # Cierra la duplicación que REG_monitor_service_unificar_rutinas_v1 dejó
    # declarada: la opción C había copiado estas rutinas desde coco.py. Ahora
    # viven una sola vez en services/landscape_engine.py y los dos servicios
    # delegan. Lo que NO se unifica es _combine_W_Delta: la W sobre la que
    # cuenta cada instrumento es lo que los distingue.
    # Ver docs/tasks/TASK_landscape_engine_v1.md.

    def _node_probs(self, W_eff: np.ndarray, weighted: bool) -> Optional[np.ndarray]:
        """Distribución de nodos para sigma_0 — landscape_engine.node_probs."""
        return node_probs(W_eff, weighted)

    def _beta_c_landscape(self, W_eff: np.ndarray) -> Optional[float]:
        """β_c de muestreo del paisaje — landscape_engine.beta_c_landscape."""
        return beta_c_landscape(W_eff)

    def _sample_s0(self, rng, N: int, probs: Optional[np.ndarray]) -> np.ndarray:
        """sigma_0 con 30-70% activos — landscape_engine.sample_s0."""
        return sample_s0(rng, N, probs)

    def _boltzmann_warmup(self, rng, sigma: np.ndarray, W_eff: np.ndarray,
                          beta: float, n_warmup: int) -> np.ndarray:
        """Calentamiento estocástico — landscape_engine.boltzmann_warmup."""
        return boltzmann_warmup(rng, sigma, W_eff, beta, n_warmup)

    def _count_attractors(
        self,
        W        : np.ndarray,
        weighted : Optional[bool] = None,
        boltzmann: Optional[bool] = None,
        n_warmup : Optional[int]  = None,
    ) -> float:
        """
        N_eff en n_runs reinicios sobre W — landscape_engine.count_attractors,
        que devuelve n_eff(basin_masses) y conserva el nombre por regresión.
        Los tres modos de muestreo de sigma_0 están documentados en
        landscape_engine.deprecated_count_attractors.

        weighted/boltzmann en None toman self._sampling_mode. Pasarlos
        explicitos permite un conteo puntual en otro modo sin cambiar la
        configuracion del servicio.
        """
        if weighted is None and boltzmann is None:
            weighted  = self._sampling_mode == "weighted"
            boltzmann = self._sampling_mode == "boltzmann"
        else:
            weighted  = bool(weighted)
            boltzmann = bool(boltzmann)

        return count_attractors(
            W, n_runs=self._n_runs, seed=self._count_seed,
            weighted=weighted, boltzmann=boltzmann,
            n_warmup=n_warmup if n_warmup is not None else self._n_warmup,
        )


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

    # T5 — Δ_r de Monitor y Δ_r_compresiones de COCO: objetos distintos
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
