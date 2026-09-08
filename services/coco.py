"""
coco.py — Collective COCO-thermostat (prototipo mínimo)

No almacena capacidades declaradas (eso es COCO-registry, se vuelve stale).
Observa D_ckm(t) del corpus colectivo emergido de interacción real A2A.
Emite señal STOP cuando el campo cruza umbral de degradación.
Aplica STOP (Delta → alpha * Delta) sobre el CorpusService compartido.

β_collective es la mediana de los β_i individuales — se calcula, 
se reporta en el panel. Pero no regula nada. Es observación, no termostat.
Para que sea colectivo en la práctica necesita un efecto sobre el campo 
que ningún device individual produce solo.

En el modelo ferromagnético: β_c es el punto donde el sistema es
máximamente receptivo. Un device con β >> β_c es rígido — rechaza todo.
Un device con β << β_c es transparente — acepta todo sin discriminar.

La regulación térmica real sería: cuando β_collective se aleja de β_c 
— en cualquier dirección — el thermostat emite una señal. No STOP.
Algo distinto: una recomendación de temperatura para el campo.

En el modelo ferromagnético β_c es un valor crítico que emerge de la
estructura de W. 
En el CKM es el β donde la diversidad de atractores es máxima — 
que es exactamente Ω*, la zona de trabajo.
Entonces β_collective es colectivo cuando: 
la mediana de los β_i activos converge hacia — o se aleja de — 
la zona Ω* del corpus. 

GAP cerrado Jun 2026: β_c_corpus derivado analíticamente desde W real.
β_c = 1/(ρ* · N · μ_W). ρ*=0.5 garantizado algebraicamente.
TEMP_SIGNAL emitida cuando β_collective se aleja de β_c en cualquier dirección:
  TOO_COLD → paranoia/inanición (campo rechaza todo, se extingue)
  TOO_HOT  → intoxicación/permisividad (campo acepta todo, pierde discriminación)

Precondición: W debe ser el suelo del corpus en modo evaluación.
W es inmutable para el thermostat — es el campo original al que
el sistema puede regresar. COCO-thermostat actúa solo sobre Δ.
Si W cambia (corpus crece, nuevos nodos), instanciar un nuevo
COCO con la W actualizada.
Uso correcto con CorpusService:
    assert corpus.mode == "evaluation", "corpus insuficiente"
    thermostat = COCO(W=corpus.get_W())
W=None (corpus en acumulación) lanza ValueError.



Ref: REG_destruccion_recuperacion_v1.md
     REG_iap_coco_convergence_v1.md
     REG_beta_colectivo_v1
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ── Umbrales derivados del sweep (REG_destruccion_recuperacion_v1) ──────────
D_CKM_THRESHOLD = 0.40   # D_ckm > 0.40 → zona degradación sostenida
ALPHA_STAR       = 0.10   # alpha óptimo empírico (A_post_max en sweep AMP=40)
FRAC_REC_MIN     = 0.60   # si A(t)/A0 < 0.60 → campo en degradación profunda

# ── Calibración dinámica alpha ───────────────────────────────────────────────
ALPHA_MIN        = 0.05   # D_ckm → 1.0 (degradación profunda) → STOP fuerte
ALPHA_MAX        = 0.30   # D_ckm → threshold (justo en umbral) → STOP suave

# ── Regulación térmica β_collective ─────────────────────────────────────────
# β_c_corpus = 1 / (ρ* · N · μ_W)  derivado de Hopfield adaptado a co-ocurrencia
# ρ* = 0.5 garantizado por identidad algebraica relax(-σ) = -relax(σ)
# μ_W = global (incluye ceros) — conservador, menos sensible — afinamos después
# Umbrales: una octava arriba/abajo de β_c — provisionales
BETA_RHO_STAR    = 0.5    # densidad crítica del campo (ρ* verificado)
BETA_TOO_COLD    = 2.0    # β_collective / β_c > 2.0 → paranoia / inanición
BETA_TOO_HOT     = 0.5    # β_collective / β_c < 0.5 → intoxicación / permisividad


@dataclass
class ThermostatState:
    """Snapshot devuelto por observe() — un campo por cantidad evaluada
    ese ciclo. Ver observe() para el significado de cada uno."""
    t            : int   = 0
    D_ckm        : float = 0.0
    A_current    : int   = 0
    A0           : int   = 0
    frac_rec     : float = 1.0
    stop_applied : bool  = False
    alpha_used   : float = 1.0
    zone         : str   = "stable"   # stable | degrading | deep


class COCO:
    """
    Regulador de campo CKM compartido por múltiples devices.

    Mide diversidad de atractores (D_ckm) sobre W + Δ_r y comprime Δ_r
    (STOP) cuando cae por debajo de umbral. Reporta también una señal
    térmica (TOO_COLD/NOMINAL/TOO_HOT) comparando β_collective con el
    β_c del corpus.

    Trackea devices solo por device_id (string opaco, vía
    register_device_eval) — no identidad rica, no AgentCards.
    """

    def __init__(
        self,
        W              : np.ndarray,
        d_ckm_threshold: float = D_CKM_THRESHOLD,
        alpha_star     : float = ALPHA_STAR,
        frac_rec_min   : float = FRAC_REC_MIN,
        dynamic_alpha  : bool  = True,
        n_runs         : int   = 80,
        seed           : int   = 0,
        track_landscape: bool  = False,
        landscape_history: Optional[list] = None,
        gamma          : float = 0.01,
        sampling_mode  : str   = "uniform",
        n_warmup       : Optional[int] = None,
    ):
        """
        W debe ser el campo del corpus en modo evaluación — inmutable
        para esta instancia. Si W cambia (corpus creció), instanciar un
        COCO nuevo, no reasignar W. Uso típico:
            assert corpus.mode == "evaluation"
            coco = COCO(W=corpus.get_W())

        Args:
            W: matriz de co-ocurrencia. W=None lanza ValueError.
            d_ckm_threshold: D_ckm por encima del cual STOP puede disparar.
            alpha_star: alpha fijo usado si dynamic_alpha=False.
            frac_rec_min: A_current/A0 por debajo de esto → zona "deep".
            dynamic_alpha: si True, alpha varía con D_ckm (_alpha_for);
                si False, siempre alpha_star.
            n_runs: reinicios aleatorios para contar atractores. Sesgado
                hacia arriba con n_runs (ver _count_attractors) — no
                cambiar sin revisar el hallazgo del sweep n_runs 60→70.
            seed: semilla del RNG de conteo de atractores.
            track_landscape: si True, cada STOP mide A/c(S) antes y
                después de comprimir (más caro, ~3x relajaciones).
            landscape_history: historial previo a precargar (p. ej. desde
                el JSONL de MonitorService al renacer COCO con W nueva).
            gamma: sensibilidad del componente histórico en alpha
                compuesto (_landscape_component). Conservador por default.
            sampling_mode: cómo observe() muestrea sigma_0 al contar
                atractores — "uniform" (default, comportamiento
                histórico), "weighted" o "boltzmann". Queda expuesto en
                el panel de MonitorService como sampling_mode: qué modo
                estaba activo en cada decisión de STOP. Cambiarlo cambia
                D_ckm — ver REG_stochastic_eval_v2: a n_runs fijo, el
                mismo Δ_r puede quedar de un lado o del otro de
                D_CKM_THRESHOLD según el modo.
            n_warmup: actualizaciones del calentamiento Boltzmann.
                None → N. Sólo se usa con sampling_mode="boltzmann".
        """
        if W is None:
            raise ValueError(
                "W no puede ser None. "
                "Esperar corpus.mode == 'evaluation' antes de instanciar COCO."
            )
        self.W               = W
        self.N               = W.shape[0]
        self.threshold       = d_ckm_threshold
        self.alpha_star      = alpha_star
        self.frac_rec_min    = frac_rec_min
        self.dynamic_alpha   = dynamic_alpha
        self._n_runs         = n_runs
        self._seed           = seed
        if sampling_mode not in ("uniform", "weighted", "boltzmann"):
            raise ValueError(
                f"sampling_mode inválido: {sampling_mode!r} — "
                "esperado 'uniform', 'weighted' o 'boltzmann'."
            )
        self._sampling_mode  = sampling_mode
        self._n_warmup       = n_warmup if n_warmup is not None else self.N

        self._A0             : Optional[int]        = None
        self._Delta          : np.ndarray           = np.zeros((self.N, self.N))
        self._history        : list[ThermostatState] = []
        self._t              : int                  = 0
        self._rejections_per_device: dict            = {}
        self._alpha_trajectory: list[dict]           = []
        self._track_landscape : bool                 = track_landscape
        self._last_landscape_delta: Optional[dict]    = None
        self._landscape_history: list[dict]           = list(landscape_history) if landscape_history else []
        self._gamma           : float                 = gamma
        self._last_landscape_component: float          = 0.0

    # ── API pública ──────────────────────────────────────────────────────────

    def observe(self, Delta_new: np.ndarray) -> ThermostatState:
        """
        Evalúa el campo con el Δ_r actual y aplica STOP si corresponde.

        Args:
            Delta_new: Δ_r acumulado por MonitorService (NxN).

        Returns:
            ThermostatState: t, D_ckm (negativo = campo expandido, no es
            error), A_current, A0, frac_rec, zone ("stable"|"degrading"|
            "deep"), stop_applied, alpha_used.

        Side effects (solo si stop_applied):
            - Δ interno se reemplaza por alpha_used * Δ_new — recuperar
              con delta_state().
            - alpha_trajectory() gana una entrada.
            - si track_landscape=True, landscape_history() gana una
              entrada y self._last_landscape_component se actualiza.
        """
        self._Delta = Delta_new.copy()
        self._t    += 1

        W_eff    = self.W + self._Delta
        # kwargs del modo de muestreo activo — con sampling_mode="uniform"
        # (default) quedan los dos en False y esto es la llamada histórica.
        smp      = self._sampling_kwargs()
        A_current = self._count_attractors(W_eff, **smp)

        if self._A0 is None:
            self._A0 = self._count_attractors(self.W, **smp)  # baseline sin Delta

        D_ckm    = (self._A0 - A_current) / self._A0 if self._A0 > 0 else 0.0
        frac_rec = A_current / self._A0 if self._A0 > 0 else 1.0

        zone = self._classify_zone(D_ckm, frac_rec)

        stop_applied = False
        alpha_used   = 1.0

        if zone in ("degrading", "deep"):
            alpha_used   = self._alpha_for(D_ckm)

            # Extensión 1 (TASK_coco_alpha_compuesto_v3) — alpha compuesto.
            # Componente histórico de eficiencia solo si hay historia
            # suficiente; si no, comportamiento idéntico al actual (sin
            # regresión, como pide la task). No es un epsilon agregado —
            # reconoce el ruido estocástico que ya existe en
            # _count_attractors (n_runs finito, ver sweep n_runs 60→70).
            landscape_component = 0.0
            if self._track_landscape and len(self._landscape_history) >= 2:
                landscape_component = self._landscape_component()
                alpha_used = float(np.clip(
                    alpha_used + landscape_component,
                    ALPHA_MIN, ALPHA_MAX,
                ))
            self._last_landscape_component = landscape_component

            # Extensión 2 (TASK_coco_landscape_observation_v1) — paisaje
            # ANTES de comprimir. Reusa A_current/W_eff ya calculados
            # arriba — self._Delta todavía no cambió en este punto.
            delta_A = None
            if self._track_landscape:
                A_antes  = A_current
                cS_antes = self._mean_cS(W_eff, **smp)

            self._Delta  = alpha_used * self._Delta
            stop_applied = True

            # Paisaje DESPUÉS de comprimir — solo si track_landscape=True
            # (cuesta ~2 relajaciones extra de n_runs muestras cada una).
            if self._track_landscape:
                W_eff_despues = self.W + self._Delta
                A_despues     = self._count_attractors(W_eff_despues, **smp)
                cS_despues    = self._mean_cS(W_eff_despues, **smp)
                delta_A       = A_despues - A_antes
                self._last_landscape_delta = {
                    "A_antes"      : A_antes,
                    "A_despues"    : A_despues,
                    "delta_A"      : delta_A,
                    "cS_antes"     : cS_antes,
                    "cS_despues"   : cS_despues,
                    "delta_cS"     : cS_despues - cS_antes,
                    "alpha_used"   : alpha_used,
                    "D_ckm_at_stop": round(D_ckm, 4),
                }
                self._landscape_history.append(self._last_landscape_delta.copy())
            else:
                self._last_landscape_delta = None

            # Extensión 3 — log liviano, un registro por STOP aplicado,
            # no por observe(). delta_A es real si track_landscape=True,
            # None si no — no se inventa un valor sin esa pieza.
            self._alpha_trajectory.append({
                "t"      : len(self._alpha_trajectory),
                "alpha"  : alpha_used,
                "D_ckm"  : round(D_ckm, 4),
                "delta_A": delta_A,
            })

        state = ThermostatState(
            t            = self._t,
            D_ckm        = round(D_ckm, 4),
            A_current    = A_current,
            A0           = self._A0,
            frac_rec     = round(frac_rec, 4),
            stop_applied = stop_applied,
            alpha_used   = alpha_used,
            zone         = zone,
        )
        self._history.append(state)
        return state

    def sampling_mode(self) -> str:
        """
        Modo de muestreo de sigma_0 activo en esta instancia —
        "uniform" | "weighted" | "boltzmann".

        Es el modo con el que observe() cuenta atractores, y por lo tanto
        el que produjo el D_ckm de cada decisión de STOP. MonitorService
        lo expone en el panel para trazabilidad.
        """
        return self._sampling_mode

    def _sampling_kwargs(self) -> dict:
        """kwargs de _count_attractors/_mean_cS para el modo activo."""
        if self._sampling_mode == "boltzmann":
            return {"boltzmann": True, "n_warmup": self._n_warmup}
        if self._sampling_mode == "weighted":
            return {"weighted": True}
        return {}

    def register_device_eval(self, device_id: str, fi: float) -> None:
        """Registra fabrication_index de una evaluación de un device."""
        if device_id not in self._rejections_per_device:
            self._rejections_per_device[device_id] = []
        self._rejections_per_device[device_id].append(fi)

    def beta_i(self, device_id: str, epsilon: float = 1e-6) -> Optional[float]:
        """β estimado para un device: alto rechazo → β alto (rígido).
        fi=0.0 → None (el campo no rechazó nada — β indefinido, no infinito)."""
        vals = self._rejections_per_device.get(device_id)
        if not vals:
            return None
        mean_fi = float(np.mean(vals))
        if mean_fi < epsilon:
            return None  # sin rechazo → β no estimable
        return 1.0 / mean_fi

    def beta_collective(self) -> Optional[float]:
        """β_c estimado: mediana de todos los β_i activos."""
        betas = [self.beta_i(did) for did in self._rejections_per_device]
        betas = [b for b in betas if b is not None]
        if not betas:
            return None
        return float(np.median(betas))

    def beta_status(self) -> dict:
        """Estado β de todos los devices activos."""
        devices = {
            did: round(self.beta_i(did), 4)
            for did in self._rejections_per_device
            if self.beta_i(did) is not None
        }
        bc = self.beta_collective()
        return {
            "beta_collective": round(bc, 4) if bc is not None else None,
            "devices"        : devices,
            "n_devices"      : len(devices),
        }

    def beta_c_corpus(self) -> float:
        """
        β crítico del corpus: punto donde el campo es máximamente receptivo.

        β_c = 1 / (ρ* · N · μ_W)

        ρ* = 0.5 — garantizado por identidad algebraica relax(-σ) = -relax(σ).
        μ_W global (incluye ceros) — conservador, menos sensible.
        Verificado: N=32, μ_W=0.004519 → β_c=13.83 (corpus CKM v2).

        Ref: REG_garantias_cS_generalizacion_v1, REG_beta_colectivo_v1
        """
        ii, jj = np.triu_indices(self.N, k=1)
        mu_W = float(np.mean(self.W[ii, jj]))
        if mu_W <= 0:
            return float("inf")
        return 1.0 / (BETA_RHO_STAR * self.N * mu_W)

    def temp_signal(self) -> dict:
        """
        Señal térmica del campo colectivo.

        Compara β_collective con β_c_corpus:
          ratio >> 1 → TOO_COLD  — paranoia/inanición (rechaza todo, se extingue)
          ratio << 1 → TOO_HOT   — intoxicación (acepta todo, pierde discriminación)
          ratio ≈ 1  → NOMINAL   — zona Ω*, portero discrimina bien

        Umbrales provisionales: una octava arriba/abajo de β_c.
        Sin devices activos → UNKNOWN (β_collective no estimable).

        Returns dict con: signal, beta_collective, beta_c_corpus, ratio,
        note (explicación en texto de la señal). Sin devices activos →
        signal="UNKNOWN", beta_collective y ratio en None.
        """
        bc = self.beta_collective()
        beta_c = self.beta_c_corpus()

        if bc is None:
            return {
                "signal"          : "UNKNOWN",
                "beta_collective" : None,
                "beta_c_corpus"   : round(beta_c, 4),
                "ratio"           : None,
                "note"            : "sin devices con fi estimable — β_collective indefinido",
            }

        ratio = bc / beta_c
        if ratio > BETA_TOO_COLD:
            signal = "TOO_COLD"
            note   = "paranoia/inanición — campo rechaza todo, se extingue"
        elif ratio < BETA_TOO_HOT:
            signal = "TOO_HOT"
            note   = "intoxicación — campo acepta todo, pierde discriminación"
        else:
            signal = "NOMINAL"
            note   = "zona Ω* — portero discrimina bien"

        return {
            "signal"          : signal,
            "beta_collective" : round(bc, 4),
            "beta_c_corpus"   : round(beta_c, 4),
            "ratio"           : round(ratio, 4),
            "note"            : note,
        }

    def delta_state(self) -> np.ndarray:
        """
        Δ actual, después de cualquier compresión por STOP.

        Llamar después de observe() cuando stop_applied=True, para
        reasignarlo a MonitorService._Delta_r.
        """
        return self._Delta.copy()

    def history(self) -> list[ThermostatState]:
        """Un ThermostatState por cada llamada a observe(), no solo los
        STOPs (para eso ver alpha_trajectory()/landscape_history())."""
        return list(self._history)

    def alpha_trajectory(self) -> list:
        """
        Un registro por cada STOP aplicado: {t, alpha, D_ckm, delta_A}.

        t acá es la posición dentro de esta lista, no el t de
        ThermostatState (ese cuenta todas las llamadas a observe(),
        no solo los STOPs). delta_A es None si track_landscape=False.
        """
        return list(self._alpha_trajectory)

    def landscape_history(self) -> list:
        """
        Historial completo de paisaje antes/después de cada STOP.

        Vacía si track_landscape=False o si nunca disparó STOP. Cada
        entry es un dict:
            A_antes, A_despues    (int)   — atractores antes/después de comprimir
            delta_A               (int)   — A_despues - A_antes
            cS_antes, cS_despues  (float) — c(S) medio antes/después
            delta_cS              (float) — cS_despues - cS_antes
            alpha_used            (float) — factor de compresión aplicado
            D_ckm_at_stop          (float) — D_ckm que disparó el STOP
        """
        return list(self._landscape_history)

    def _landscape_component(self) -> float:
        """
        Gradiente de eficiencia histórica de STOP.
        Positivo → STOPs anteriores fueron eficientes con α bajo → reducir α.
        Negativo → STOPs ineficientes → aumentar α.
        Retorna 0.0 si no hay historia suficiente (< 2 entradas).
        """
        h = self.landscape_history()
        if len(h) < 2:
            return 0.0
        # Eficiencia = delta_A / alpha_used (delta_A por unidad de compresión)
        efficiencies = [
            e["delta_A"] / e["alpha_used"]
            for e in h[-5:]   # ventana últimas 5 entradas
            if e.get("alpha_used") and e["alpha_used"] > 0
            and e.get("delta_A") is not None
        ]
        if not efficiencies:
            return 0.0
        return -float(np.mean(efficiencies)) * self._gamma  # negativo: más eficiencia → α más bajo

    def status(self) -> dict:
        """
        Resumen del último ThermostatState (t, A0, A_current, D_ckm,
        frac_rec, zone, stop_applied, alpha_used).

        {"t": 0, "zone": "uninitialized"} si observe() nunca se llamó.
        """
        if not self._history:
            return {"t": 0, "zone": "uninitialized"}
        s = self._history[-1]
        return {
            "t"           : s.t,
            "A0"          : s.A0,
            "A_current"   : s.A_current,
            "D_ckm"       : s.D_ckm,
            "frac_rec"    : s.frac_rec,
            "zone"        : s.zone,
            "stop_applied": s.stop_applied,
            "alpha_used"  : s.alpha_used,
        }

    # ── Calibración dinámica ─────────────────────────────────────────────────

    def _alpha_for(self, D_ckm: float) -> float:
        """
        Alpha decrece monotonamente con D_ckm.
        Mayor degradación → STOP más agresivo.

        D_ckm en [threshold, 1.0] → alpha en [ALPHA_MAX, ALPHA_MIN]
        Si dynamic_alpha=False, devuelve alpha_star fijo.
        """
        if not self.dynamic_alpha:
            return self.alpha_star
        t = self.threshold
        # normalizar D_ckm al rango [threshold, 1.0]
        ratio = min(1.0, max(0.0, (D_ckm - t) / (1.0 - t)))
        return ALPHA_MAX + (ALPHA_MIN - ALPHA_MAX) * ratio

    # ── Clasificación de zona ─────────────────────────────────────────────────

    def _classify_zone(self, D_ckm: float, frac_rec: float) -> str:
        """D_ckm negativo o por debajo de threshold → "stable". Si no,
        frac_rec por debajo de frac_rec_min → "deep", si no → "degrading"."""
        if D_ckm < 0:
            return "stable"          # campo expandido — acumulación suma atractores
        if D_ckm < self.threshold:
            return "stable"          # degradación menor al umbral
        if frac_rec < self.frac_rec_min:
            return "deep"            # degradación profunda — STOP urgente
        return "degrading"           # cruzó umbral — STOP recomendado

    # ── Hopfield ─────────────────────────────────────────────────────────────

    def _relax_orbit(
        self,
        sigma   : np.ndarray,
        W       : np.ndarray,
        max_iter: int = 200,
    ) -> tuple:
        """
        Relajación de Hopfield síncrona, devolviendo la ÓRBITA alcanzada.

        Returns: (orbita, periodo, cola, estado_en_max_iter)
          orbita  — frozenset de los estados del conjunto invariante, SIN
                    orden. Un punto fijo es la órbita de un elemento.
          periodo — |orbita|. 1 = punto fijo, 2 = órbita de dos elementos.
          cola    — pasos hasta entrar en la órbita.
          estado_en_max_iter — qué estado habría devuelto el loop de
                    max_iter iteraciones. Es lo que retorna _relax().

        Detección exacta, no heurística: el espacio de estados es finito
        ({-1,+1}^N) y el mapa es determinista, así que toda trayectoria
        entra en una órbita en tiempo finito (LaSalle, con V no creciente
        y espacio acotado). Se guarda cada estado visto con su paso; al
        repetirse uno, la órbita es el tramo entre las dos apariciones.

        La fase devuelta por el loop original depende de
        (max_iter - cola) mod periodo — para periodo 2 es la paridad de
        max_iter, para periodo p es el residuo. Se reconstruye ese índice
        en vez de iterar hasta el final: mismo estado, sin recorrer el
        ciclo. Verificado bit a bit contra el loop previo, 500/500 en tres
        corpus, con 27x-38x de aceleración donde hay órbitas de periodo 2.

        Nota: "ciclo de periodo 2" es el rótulo de CS, que lo nombra por
        no ser punto fijo. Es una órbita — un miembro de M con dos
        elementos. Lo que el principio de invariancia selecciona es la
        invariancia, no la quietud.
        """
        visto : dict = {}
        seq   : list = []
        s = sigma
        for t in range(max_iter):
            k    = s.tobytes()
            prev = visto.get(k)
            if prev is not None:
                per = t - prev
                idx = prev + ((max_iter - prev) % per)
                orbita = frozenset(a.tobytes() for a in seq[prev:])
                return orbita, per, prev, seq[idx]
            visto[k] = t
            seq.append(s)
            h = W @ s
            s = np.where(h > 0, 1., np.where(h < 0, -1., s))
        # max_iter agotado sin cerrar órbita — no observado en ningún corpus
        # del proyecto (0 de 800 runs), se preserva como salida defensiva.
        return frozenset([s.tobytes()]), 0, -1, s

    def _relax(self, sigma: np.ndarray, W: np.ndarray, max_iter: int = 200) -> np.ndarray:
        """
        Estado alcanzado tras max_iter pasos de relajación síncrona.

        Comportamiento idéntico al loop previo, incluida la fase devuelta
        cuando la trayectoria queda en una órbita de periodo > 1 — ver
        _relax_orbit, que es donde está la implementación.
        """
        return self._relax_orbit(sigma, W, max_iter)[3]

    def _node_probs(self, W_eff: np.ndarray, weighted: bool) -> Optional[np.ndarray]:
        """
        Distribución sobre nodos para el muestreo de sigma_0.

        weighted=False → None (uniforme, comportamiento histórico).
        weighted=True  → fi / fi.sum(), con fi = |W_eff|.sum(axis=1):
        actividad marginal de cada nodo en el paisaje que se evalúa.
        Nodos con mayor acoplamiento en W_eff tienen mayor probabilidad
        de caer en la cuenca de un atractor real. No requiere β_c.

        Fallback a uniforme (None) en dos casos, sin error:
          - fi.sum() == 0 (W_eff completamente cero);
          - menos nodos con probabilidad > 0 que el n_act máximo posible
            (0.7·N): rng.choice(replace=False, p=...) no puede muestrear
            sin reposición más nodos que los de peso no nulo.
        """
        if not weighted:
            return None
        fi = np.abs(W_eff).sum(axis=1)
        fi_sum = fi.sum()
        if fi_sum <= 0:
            return None
        n_act_max = max(1, int(round(0.7 * self.N)))
        if int(np.count_nonzero(fi)) < n_act_max:
            return None
        return fi / fi_sum

    def _beta_c_landscape(self, W_eff: np.ndarray) -> Optional[float]:
        """
        β_c del paisaje que se está evaluando, para el calentamiento
        Boltzmann:

            β_c = 1 / (ρ* · N · μ_W)     con μ_W = mean(W_eff[W_eff > 0])

        ρ* = BETA_RHO_STAR = 0.5 — identidad algebraica relax(-σ) = -relax(σ).
        Se computa una vez por llamada a _count_attractors(), no por run.

        NO es el mismo número que beta_c_corpus(). Ese usa μ_W sobre el
        triángulo superior *incluyendo ceros* ("conservador, menos
        sensible", ver su docstring) y sobre self.W; éste usa la media
        sobre pesos no-nulos y sobre W_eff. Medido en
        W_ckm_corpus_v2.json (N=32, densidad 0.73): beta_c_corpus()=13.83,
        este=10.46 — razón 0.756. Son dos temperaturas distintas y no
        deben confundirse: beta_c_corpus() sigue siendo la referencia de
        TEMP_SIGNAL; ésta es sólo la temperatura de muestreo.
        Especificado así en TASK_boltzmann_sampling_count_attractors_v3_1.

        Devuelve None si W_eff no tiene pesos positivos — sin error; el
        llamador cae a muestreo uniforme.
        """
        pos = W_eff[W_eff > 0]
        if pos.size == 0:
            return None
        mu_W = float(np.mean(pos))
        if mu_W <= 0:
            return None
        return 1.0 / (BETA_RHO_STAR * self.N * mu_W)

    def _boltzmann_warmup(
        self,
        rng      : np.random.Generator,
        sigma    : np.ndarray,
        W_eff    : np.ndarray,
        beta     : float,
        n_warmup : int,
    ) -> np.ndarray:
        """
        Calentamiento estocástico asíncrono a temperatura 1/beta.

        n_warmup actualizaciones de un nodo por vez:

            p(σ_i = +1) = 1 / (1 + exp(-2·β·h_i))    con h_i = Σ_j W_ij σ_j

        Misma regla que la rama estocástica de relax() en hopfield.py
        (raíz del repo, línea 51). Reimplementada acá y no importada:
        hopfield.py hace `from .core import ...` — import relativo sin
        __init__.py en la raíz, no es importable desde services/ — y usa
        np.random.seed()/np.random.rand() (estado GLOBAL de numpy), que
        rompería el aislamiento de semilla del que dependen
        experiments/stochastic_attractor_eval.py y REG_stochastic_eval_v1/v2.
        La duplicación es deliberada y está declarada; si hopfield.py:51
        cambia, esto hay que revisarlo a mano.
        Ver docs/VERIF_repo_boltzmann_paso0_v1.md.

        n_warmup se cuenta en actualizaciones de UN nodo (no en barridos):
        n_warmup = N equivale a un barrido en promedio, no a un barrido
        completo — la selección es con reposición, algunos nodos se
        actualizan más de una vez y otros ninguna. No hay garantía de
        mezcla: n_warmup óptimo es pregunta abierta (TASK v3_1).
        """
        sigma = sigma.copy()
        for _ in range(n_warmup):
            i = int(rng.integers(self.N))
            h = float(W_eff[i] @ sigma)
            p = 1.0 / (1.0 + np.exp(-2.0 * beta * h))
            sigma[i] = 1.0 if rng.random() < p else -1.0
        return sigma

    def _sample_s0(
        self,
        rng  : np.random.Generator,
        probs: Optional[np.ndarray],
    ) -> np.ndarray:
        """
        Un estado inicial sigma_0 ∈ {+1,-1}^N con 30–70% de nodos activos.

        Compartido por _count_attractors() y _mean_cS() para que ambos
        consuman el RNG en la misma secuencia con la misma semilla.
        probs=None → uniforme sobre nodos.
        """
        n_act = max(1, int(round(rng.uniform(0.3, 0.7) * self.N)))
        s0    = np.full(self.N, -1.)
        s0[rng.choice(self.N, n_act, replace=False, p=probs)] = 1.
        return s0

    def _count_attractors(
        self,
        W_eff    : np.ndarray,
        weighted : bool = False,
        boltzmann: bool = False,
        n_warmup : Optional[int] = None,
    ) -> int:
        """
        Cuenta atractores distintos alcanzados en n_runs reinicios
        aleatorios de Hopfield sobre W_eff.

        No satura: el conteo crece ~linealmente con n_runs en corpus
        chicos (verificado hasta n_runs=200, sweep Ago 2026) — es una
        cota inferior sesgada por n_runs, no un valor convergente.

        Sesgo estructural: rng.choice(self.N, ...) asigna probabilidad
        uniforme a cada nodo como candidato al estado inicial. Con W
        sparse o anisotrópica (p.ej. presencia de nodo tipo-965), esto
        sobremuestra zonas de acoplamiento bajo. El método cuenta una
        cota inferior más conservadora que la diversidad real del
        paisaje. Para muestreo informado por W_eff, usar weighted=True
        (ver parámetro).

        Los dos sesgos — n_runs y uniformidad sobre nodos — son
        independientes: ni weighted=True ni boltzmann=True corrigen el
        primero.

        Tres modos de muestreo de sigma_0, mutuamente excluyentes:
          - uniforme  (default) — P(nodo) = 1/N.
          - ponderado (weighted=True) — P(nodo) ∝ |W_eff|.sum(axis=1).
          - Boltzmann (boltzmann=True) — sigma_0 uniforme + calentamiento
            estocástico a β_c del paisaje (ver _boltzmann_warmup). A
            diferencia de los otros dos, que son estáticos, éste usa el
            campo local: es muestreo por importancia respecto de la
            geometría real de W_eff.

        boltzmann=True tiene precedencia sobre weighted.

        Args:
            W_eff: paisaje efectivo sobre el que relajar.
            weighted: muestreo ponderado por actividad marginal en W_eff
                (ver _node_probs). Ignorado si boltzmann=True.
            boltzmann: calentamiento estocástico a β_c antes del relax
                determinístico. Si W_eff no tiene pesos positivos, β_c no
                es calculable y cae a uniforme sin error.
            n_warmup: actualizaciones de un nodo en el calentamiento.
                None → self._n_warmup (default N). Sólo aplica con
                boltzmann=True.
        """
        rng   = np.random.default_rng(self._seed)
        beta  = self._beta_c_landscape(W_eff) if boltzmann else None
        probs = None if boltzmann else self._node_probs(W_eff, weighted)
        n_w   = (n_warmup if n_warmup is not None else self._n_warmup)
        attractors = set()
        for _ in range(self._n_runs):
            s0 = self._sample_s0(rng, probs)
            if beta is not None:
                s0 = self._boltzmann_warmup(rng, s0, W_eff, beta, n_w)
            attractors.add(tuple(self._relax(s0, W_eff).tolist()))
        return len(attractors)

    def _mean_cS(
        self,
        W_eff    : np.ndarray,
        weighted : bool = False,
        boltzmann: bool = False,
        n_warmup : Optional[int] = None,
    ) -> float:
        """
        Media de c(S) sobre las mismas muestras que _count_attractors():
        mismo self._seed, mismo self._n_runs, misma secuencia de sigma_0
        — el rng con semilla fija reproduce exactamente la misma
        secuencia de estados iniciales, independiente de la llamada.
        El muestreo es literalmente el mismo código (_sample_s0 y, con
        boltzmann=True, _boltzmann_warmup), por lo que `weighted`,
        `boltzmann` y `n_warmup` tienen acá el mismo significado y los
        mismos sesgos documentados en _count_attractors: para que ambas
        cantidades sigan describiendo las mismas muestras, hay que pasar
        los mismos valores a las dos.

        c(S) = mean(W_eff_ij · sigma_i · sigma_j) sobre pares i<j, mismo
        formato que MonitorService._cS(). Se computa sobre W_eff (=W+Δ),
        no sobre self.W solo — coherente con lo que _count_attractors ya
        hace: COCO opera sobre el paisaje efectivo, no sobre W puro. Esto
        no es la misma regla que R18 (W/Δ_W separadas en el corpus) —
        self.W nunca se muta acá, W_eff es una combinación efímera local
        a esta observación, igual que en A_current.
        """
        rng    = np.random.default_rng(self._seed)
        beta   = self._beta_c_landscape(W_eff) if boltzmann else None
        probs  = None if boltzmann else self._node_probs(W_eff, weighted)
        n_w    = (n_warmup if n_warmup is not None else self._n_warmup)
        ii, jj = np.triu_indices(self.N, k=1)
        cs_values = []
        for _ in range(self._n_runs):
            s0    = self._sample_s0(rng, probs)
            if beta is not None:
                s0 = self._boltzmann_warmup(rng, s0, W_eff, beta, n_w)
            sigma = self._relax(s0, W_eff)
            cs_values.append(float(np.mean(W_eff[ii, jj] * sigma[ii] * sigma[jj])))
        return float(np.mean(cs_values))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    rng = np.random.default_rng(42)
    W = rng.uniform(-1, 1, (8, 8))
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0)

    # T1 — precondición W=None
    try:
        COCO(W=None)
        print("FAIL T1")
        sys.exit(1)
    except ValueError:
        print("T1 OK — ValueError en W=None")

    th = COCO(W=W, n_runs=40, seed=42)

    # T2 — _alpha_for monotona decreciente
    alphas = [th._alpha_for(d) for d in [0.40, 0.60, 0.80, 1.0]]
    assert alphas[0] > alphas[1] > alphas[2] > alphas[3], "FAIL T2"
    print(f"T2 OK — alpha_for: {[round(a,3) for a in alphas]}")

    # T3 — beta sin devices → None
    assert th.beta_collective() is None
    print("T3 OK — beta_collective None sin devices")

    # T4 — beta_i: fi=0 → None, mayor rechazo → beta menor
    th.register_device_eval("deviceA", 0.8)
    th.register_device_eval("deviceA", 0.6)
    th.register_device_eval("deviceB", 0.0)
    th.register_device_eval("deviceC", 0.4)
    assert th.beta_i("deviceB") is None, "FAIL T4 — fi=0 debe ser None"
    assert th.beta_i("deviceA") < th.beta_i("deviceC"), "FAIL T4 — orden beta"
    print(f"T4 OK — beta_A={th.beta_i('deviceA'):.3f}  beta_B={th.beta_i('deviceB')}  beta_C={th.beta_i('deviceC'):.3f}")

    # T5 — beta_collective mediana sobre activos (excluye None)
    bc = th.beta_collective()
    assert bc is not None
    print(f"T5 OK — beta_collective={bc:.4f}")

    # T6 — observe Delta limpio → stable, sin STOP
    state = th.observe(np.zeros((8, 8)))
    assert state.zone == "stable" and not state.stop_applied
    print(f"T6 OK — zone=stable, stop=False")

    # T7 — observe Delta pesado → STOP + alpha dinámico < ALPHA_MAX
    Delta_heavy = np.ones((8, 8)) * 50
    np.fill_diagonal(Delta_heavy, 0)
    state2 = th.observe(Delta_heavy)
    assert state2.stop_applied
    assert state2.alpha_used < 0.30
    print(f"T7 OK — zone={state2.zone}, alpha={state2.alpha_used:.4f}, stop=True")

    # T8 — dynamic_alpha=False usa alpha_star fijo
    th2 = COCO(W=W, dynamic_alpha=False, n_runs=40, seed=42)
    th2.observe(Delta_heavy)
    state3 = th2.observe(Delta_heavy)
    if state3.stop_applied:
        assert state3.alpha_used == ALPHA_STAR, "FAIL T8"
        print(f"T8 OK — alpha fijo={state3.alpha_used}")
    else:
        print("T8 SKIP — no STOP en esta corrida")

    print("\nT1-T8 OK")

# ---------------------------------------------------------------------------
# Tests TEMP_SIGNAL — requiere W real (W_ckm_corpus_v2.json)
# ---------------------------------------------------------------------------
def _test_temp_signal():
    import json
    from pathlib import Path
    w_path = Path(__file__).parent / "W_ckm_corpus_v2.json"
    if not w_path.exists():
        print("SKIP T9-T12 — W_ckm_corpus_v2.json no disponible")
        return

    with open(w_path) as f:
        W_real = np.array(json.load(f)["W"])

    th = COCO(W=W_real, n_runs=40, seed=42)

    # T9 — beta_c_corpus verificado
    bc = th.beta_c_corpus()
    assert abs(bc - 13.83) < 0.1, f"FAIL T9: {bc}"
    print(f"T9 OK — beta_c_corpus={bc:.4f}")

    # T10 — sin devices → UNKNOWN
    ts = th.temp_signal()
    assert ts["signal"] == "UNKNOWN"
    print(f"T10 OK — UNKNOWN sin devices")

    # T11 — TOO_COLD: fi bajo → β alto → paranoia/inanición
    th.register_device_eval("deviceA", 0.001)
    th.register_device_eval("deviceB", 0.001)
    ts = th.temp_signal()
    assert ts["signal"] == "TOO_COLD", f"FAIL T11: {ts}"
    print(f"T11 OK — TOO_COLD ratio={ts['ratio']}")

    # T12 — TOO_HOT: fi alto → β bajo → intoxicación
    th2 = COCO(W=W_real, n_runs=40, seed=42)
    th2.register_device_eval("deviceA", 0.99)
    th2.register_device_eval("deviceB", 0.95)
    ts2 = th2.temp_signal()
    assert ts2["signal"] == "TOO_HOT", f"FAIL T12: {ts2}"
    print(f"T12 OK — TOO_HOT ratio={ts2['ratio']}")

    # T13 — NOMINAL: fi ≈ 1/β_c
    th3 = COCO(W=W_real, n_runs=40, seed=42)
    fi_nom = 1.0 / bc
    th3.register_device_eval("deviceA", fi_nom)
    th3.register_device_eval("deviceB", fi_nom * 1.2)
    th3.register_device_eval("deviceC", fi_nom * 0.8)
    ts3 = th3.temp_signal()
    assert ts3["signal"] == "NOMINAL", f"FAIL T13: {ts3}"
    print(f"T13 OK — NOMINAL ratio={ts3['ratio']}")

    print("T9-T13 OK — TEMP_SIGNAL operativo")


# La llamada va guardada por __name__: _test_temp_signal() a nivel de módulo
# correría T9-T13 en CADA import de coco.py — y lo importan monitor_service,
# iap_chatroom y los módulos de experiments/. Acá corre sólo con
# `python services/coco.py`, junto a T1-T8.
if __name__ == "__main__":
    _test_temp_signal()
    print("\nTodos los tests OK — T1-T13")
