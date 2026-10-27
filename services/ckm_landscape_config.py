"""
ckm_landscape_config.py — CKMlandscapeConfig (con ciclos) y Ciclo

Contrato vivo del instrumento (DEFS v11 §0 Modelo Conceptual). No es una
bolsa de constantes: lo que se puede medir de W se mide de W; lo que todavía
es decisión abierta se exige como parámetro, sin default.

Independiente de CKMConfig (process/initial_static_model/core.py): no hereda,
no toma sus valores.

**Criterio (TASK v2).** Cada campo se ubica según *qué lo hace cambiar*. Dos
campos con causas de cambio distintas no comparten objeto inmutable:

  medido     cambia si y solo si cambia w_version_id  → vive en el Ciclo
  declarado  cambia si alguien lo declara             → vive en la config
  identidad  se fija al crear la instancia            → vive en la config

La config no es una foto de una W: es la traza de los ciclos por los que pasó.
La inmutabilidad pasa del objeto a la traza (I1).

Dos identidades distintas:
  w_version_id — sha256(W) vía w_version.py. Identifica a W.
  config_id    — uuid por instancia, con timestamp. Identifica a la config.

**theta_W no es un campo de esta config** (delamor, 7 oct 2026): es parámetro
del Gatekeeper, que lo recibe en c1(..., theta_W=). Pertenece a W estática, no
al landscape. La clase v1 que lo tenía adentro salió en el CP3; su traza está
en git y los JSONL ya escritos se leen con ciclo_desde_registro_plano_v1.

Spec: docs/tasks/TASK_CKMlandscapeConfig_v2.md (criterio, clases, I1–I7,
transición única) y docs/tasks/TASK_CKMlandscapeConfig_v3.md (D1–D6).
Decisiones: docs/tasks/DECISIONES_opus.md.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Optional

import numpy as np

from w_version import sha256_W

SAMPLING_MODES = ("uniform", "weighted", "boltzmann")
SCALES = ("linear", "log")
RHO_STAR = 0.5   # misma ρ* que coco.BETA_RHO_STAR

CAUSA_BOOTSTRAP = "bootstrap"

# n_runs = 1000: decisión de delamor (8 oct, P9) — "n 1000". Es donde N_eff
# converge en los casos IAP, ±2% respecto de 5000; con 50 quedaba 5-20% por
# debajo. Uno solo para Monitor y COCO.
N_RUNS_DEFAULT = 1000
# seed: la elige Code y la declara (P9, resuelto por Opus bajo el umbral). 0 es
# la que Monitor ya usaba por default en count_seed, así que no mueve nada de lo
# que ya está medido.
SEED_DEFAULT = 0


# ── medido ───────────────────────────────────────────────────────────────────

def medido(W: np.ndarray) -> dict:
    """
    Lo medido de W, función de W sola (I5).

    Dos W con el mismo sha256 dan el mismo medido. No toma ningún parámetro
    declarado y no devuelve ninguno: la separación de origen es I4.

    mu_W se porta en sus dos formas, con nombre explícito. Cada consumidor
    declara cuál usa; la config no elige. beta_c sigue a mu_W: una por cada
    forma (coco.beta_c_corpus usa la global).

    Nota sobre `nodes`: la TASK v2 lo lista en la clase "medido", pero las
    etiquetas de los nodos no son función de W —W no las lleva— y eso
    rompería I5. Queda afuera, como en v1. Si hace falta, entra como campo
    declarado del lado de quien las tiene (NodeExtractor), no acá.
    """
    W = np.asarray(W, dtype=float)
    if W.ndim != 2 or W.shape[0] != W.shape[1]:
        raise ValueError(f"W debe ser cuadrada, shape={W.shape}")

    N = W.shape[0]
    ii, jj = np.triu_indices(N, k=1)
    pares = W[ii, jj]
    no_nulos = pares[pares != 0]
    mu_global  = float(pares.mean()) if len(pares) else 0.0
    mu_nonzero = float(no_nulos.mean()) if len(no_nulos) else 0.0

    return dict(
        N              = N,
        mu_W_nonzero   = mu_nonzero,
        mu_W_global    = mu_global,
        beta_c_nonzero = _beta_c(N, mu_nonzero),
        beta_c_global  = _beta_c(N, mu_global),
    )


# ── el ciclo ─────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Ciclo:
    """
    Un ciclo de vida de W: la W que lo identifica, lo medido de esa W, por qué
    se abrió, y los dos tiempos.

    Inmutable (I1). Un ciclo cerrado no se modifica nunca: la config gana
    ciclos, no los edita.

    t_senal — cuándo se señaló que W debía cambiar. None si nadie lo señaló.
              El nombre va sin tilde: en este repo ningún identificador la
              lleva (la spec de la v2 lo escribe `t_señal`).
    t_rebuild — cuándo W cambió efectivamente.
    """
    w_version_id   : str
    N              : int
    mu_W_nonzero   : float
    mu_W_global    : float
    beta_c_nonzero : float
    beta_c_global  : float
    causa          : str
    t_senal        : Optional[float]
    t_rebuild      : float

    def __post_init__(self) -> None:
        if self.t_senal is not None and self.t_senal > self.t_rebuild:
            raise ValueError(
                f"t_senal={self.t_senal} > t_rebuild={self.t_rebuild} — "
                "la señal no puede ser posterior al rebuild (I6)"
            )

    @property
    def deriva(self) -> Optional[float]:
        """
        Cuánto operó el sistema sobre una W ya señalada como obsoleta (I6).

        Sin señal es **nula, no cero**: no hubo deriva que medir, que es
        distinto de una deriva de duración cero.
        """
        if self.t_senal is None:
            return None
        return self.t_rebuild - self.t_senal

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Ciclo":
        return cls(**d)


# ── la config ────────────────────────────────────────────────────────────────

class CKMlandscapeConfig:
    """
    Identidad + declarado + la traza de ciclos. El ciclo vigente es el último.

    **Get consistente (D3).** `ciclo_vigente` devuelve el objeto `Ciclo`
    entero en una sola operación, bajo el mismo lock con el que `abrir_ciclo`
    lo reemplaza. No hay getters por campo que un set pueda partir al medio.
    Hay concurrencia real medida en el canal: un lector en un hilo de Gradio
    (gr.Timer cada 3 s → get_state) y un escritor en el event loop
    (ChatChannel.publish → on_message). Ver BANDEJA_code, REPORTE CP0 punto 2.

    **Set síncrono (D2).** Cuando `abrir_ciclo` retorna, el ciclo nuevo ya es
    el vigente. No hay sets diferidos ni en cola.

    **Declarado (I4, revisada el 7 oct; corregido el 27 oct 2026).** Lo
    declarado se exige según quién lo usa, no siempre:
      sampling_mode — **el único exigido**: es keyword-only y sin default, y
                      Monitor valida el suyo contra éste (`ValueError` si no
                      coinciden).
      n_runs        — **con default** `N_RUNS_DEFAULT` (1000): muestras de
                      sigma_0 para contar órbitas.
      seed          — **con default** `SEED_DEFAULT` (0): la seed de ese
                      muestreo.
      scale         — opcional: hoy sólo lo usa la UI.
    theta_W no está: es del Gatekeeper.

    **Esas tres líneas decían "obligatorio" para `n_runs` y `seed`, y el código
    les da default.** Era una divergencia docstring/código, encontrada por Code
    el 26 oct (V3 del texto 08) y corregida acá el 27: **el docstring dice lo
    que el código hace.** El valor de esos defaults **no se decide** (delamor, 27
    oct: *"ahora cualquiera da lo mismo. Esa es la respuesta correcta"*); lo que
    importa es que **caer en uno se pueda ver**, y hoy **no se ve**: una Config
    construida sin `n_runs` y una construida con `n_runs=1000` dan el mismo
    `declarado`, el mismo `panel()` y el mismo `to_dict()`. Verificado y
    declarado; el mecanismo que lo haría visible es otra TASK.

    **Y las otras dos afirmaciones de este bloque también eran falsas**, y van
    corregidas acá (medido en el V3 del texto 08):
      - decía *"n_runs y seed son UNO SOLO para Monitor y COCO"* (delamor, 8
        oct: "n 1000"; P9). **COCO sí los toma de acá** (`_renacer_coco`,
        `setdefault`). **Monitor no**: cuenta con su propio
        `n_runs_attractors` y su `count_seed`, y no lee esta Config para eso.
        Coinciden **por default** (1000 y 0 en los dos lados), no por
        construcción, y nada lo verifica — `sampling_mode` sí tiene guardia y
        estos dos no.
      - decía *"COCO ya no tiene un default propio"*. **Lo tiene**:
        `coco.py` declara `n_runs = 80` y `seed = 0` en su firma. Lo que pasa es
        que el `setdefault` del renacimiento los pisa cuando hay Config; el 80
        no se usa en el canal y sigue ahí.

    **Los umbrales de COCO** (`d_ckm_threshold`, `frac_rec_min`): **D6 se
    revisó el 27 oct 2026** (D3 y D4 de `TASK_calibrate_en_el_build_v2`).
    Siguen **sin entrar como campos declarados** —la calibración es un proceso
    aparte—, pero **el resultado de la calibración sí vive acá**, en su lugar
    (`calibracion`, `registrar_calibracion`), firmado con el `w_sha` de la W
    calibrada, y de ahí deriva COCO su vara. `alpha_star`, `track_landscape`,
    `n_warmup` y `gamma` quedan en la configuración de COCO.
    """

    __slots__ = ("_sampling_mode", "_n_runs", "_seed", "_scale", "_config_id",
                 "_timestamp", "_ciclos", "_lock", "_tick", "_tick_reloj",
                 # ── el lugar de la calibración (D3, 27 oct 2026) ───────────
                 # `_calibracion` es el registro de la última calibración, con
                 # su `w_sha`. Los tres `_calibrate_*` son los parámetros
                 # **declarados** con los que corre `calibrate`: dejaron de ser
                 # defaults de función (D6'). `None` en cualquiera de ellos es
                 # **"nadie lo declaró"** (UNKNOWN), no un número.
                 "_calibracion", "_calibrate_n_runs", "_calibrate_seed",
                 "_calibrate_grilla")

    def __init__(
        self,
        *,
        sampling_mode: str,
        n_runs       : int = N_RUNS_DEFAULT,
        seed         : int = SEED_DEFAULT,
        scale        : Optional[str] = None,
        config_id    : Optional[str] = None,
        timestamp    : Optional[float] = None,
        ciclos       : tuple[Ciclo, ...] = (),
        calibrate_n_runs : Optional[int] = None,
        calibrate_seed   : Optional[int] = None,
        calibrate_grilla : Optional[tuple] = None,
        calibracion      : Optional[dict] = None,
    ) -> None:
        """
        Uso normal: `CKMlandscapeConfig.create(W, sampling_mode=...)`.

        **Los cuatro últimos son el lugar de la calibración** (D3 y D6', 27 oct
        2026). Los tres `calibrate_*` son lo **declarado**: con qué va a correr
        `calibrate`. `calibracion` es lo **medido**: el registro de la última
        corrida. **`None` en los cuatro quiere decir "nadie lo declaró / no hubo
        registro"**, que es UNKNOWN — no es `nulo_calibrado`, que es un estado
        de `calibrate` y significa *"no se ejecutó"*. La diferencia importa en
        `from_dict`: un estado guardado antes de hoy no tiene estas claves, y
        leerlas como `nulo_calibrado` afirmaría algo que nadie registró (I2).

        **Esta Config no importa `calibrate`.** Los valores llegan de quien
        arma la corrida —el canal—, igual que el tick: acá se **registran**, no
        se generan. Así el estado no depende del instrumento.
        """
        if sampling_mode not in SAMPLING_MODES:
            raise ValueError(
                f"sampling_mode inválido: {sampling_mode!r} — esperado {SAMPLING_MODES}"
            )
        if scale is not None and scale not in SCALES:
            raise ValueError(f"scale inválida: {scale!r} — esperado {SCALES}")
        if not isinstance(n_runs, int) or n_runs < 1:
            raise ValueError(f"n_runs inválido: {n_runs!r} — entero >= 1")
        if not isinstance(seed, int):
            raise ValueError(f"seed inválida: {seed!r} — entero")
        # Los declarados de `calibrate`: se validan **sólo si llegaron**.
        # `None` es "nadie lo declaró" y es un valor legítimo del lugar.
        if calibrate_n_runs is not None and (
            not isinstance(calibrate_n_runs, int) or calibrate_n_runs < 1
        ):
            raise ValueError(
                f"calibrate_n_runs inválido: {calibrate_n_runs!r} — entero >= 1 "
                "o None (nadie lo declaró)"
            )
        if calibrate_seed is not None and not isinstance(calibrate_seed, int):
            raise ValueError(
                f"calibrate_seed inválida: {calibrate_seed!r} — entero o None"
            )
        if calibrate_grilla is not None:
            if not calibrate_grilla:
                raise ValueError(
                    "calibrate_grilla vacía: una grilla sin puntos no es una "
                    "grilla declarada; para 'nadie la declaró' va None"
                )
            if not all(isinstance(x, (int, float)) for x in calibrate_grilla):
                raise ValueError(
                    f"calibrate_grilla inválida: {calibrate_grilla!r} — números"
                )

        self._sampling_mode = sampling_mode
        self._n_runs        = n_runs
        self._seed          = seed
        self._scale         = scale
        self._config_id     = config_id if config_id is not None else uuid.uuid4().hex
        self._timestamp     = timestamp if timestamp is not None else time.time()
        self._ciclos        = tuple(ciclos)
        self._lock          = threading.RLock()
        # El tick del canal, registrado por Monitor. None hasta que alguien lo
        # anote: sin canal no hay tick, y eso es UNKNOWN, no 0.
        self._tick          : Optional[int] = None
        self._tick_reloj    : Optional[str] = None
        # ── el lugar de la calibración (D3, 27 oct 2026) ────────────────────
        # Lo declarado y lo medido, en el mismo lugar y distinguidos: los tres
        # `_calibrate_*` son con qué va a correr `calibrate`; `_calibracion` es
        # el registro de lo que salió. Un escritor —el punto único del canal,
        # `CKMMonitor._calibrar_antes_de_instalar`— y muchos lectores.
        self._calibrate_n_runs : Optional[int]   = calibrate_n_runs
        self._calibrate_seed   : Optional[int]   = calibrate_seed
        self._calibrate_grilla : Optional[tuple] = (
            tuple(calibrate_grilla) if calibrate_grilla is not None else None
        )
        self._calibracion      : Optional[dict]  = (
            dict(calibracion) if calibracion is not None else None
        )

    # ── construcción ─────────────────────────────────────────────────────────

    @classmethod
    def create(
        cls,
        W            : np.ndarray,
        *,
        sampling_mode: str,
        n_runs       : int = N_RUNS_DEFAULT,
        seed         : int = SEED_DEFAULT,
        scale        : Optional[str] = None,
        causa        : str = CAUSA_BOOTSTRAP,
        t_senal      : Optional[float] = None,
    ) -> "CKMlandscapeConfig":
        """
        Crea la config y **abre el primer ciclo** con causa "bootstrap".

        El primer rebuild no es degradación: es el origen (PROPUESTA v5). Por
        eso `len(ciclos) >= 1` desde la construcción (I2).
        """
        cfg = cls(sampling_mode=sampling_mode, n_runs=n_runs, seed=seed, scale=scale)
        cfg.abrir_ciclo(W, causa, time.time(), t_senal=t_senal)
        return cfg

    # ── identidad y declarado ────────────────────────────────────────────────

    @property
    def sampling_mode(self) -> str:
        return self._sampling_mode

    @property
    def n_runs(self) -> int:
        return self._n_runs

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def scale(self) -> Optional[str]:
        return self._scale

    @property
    def config_id(self) -> str:
        return self._config_id

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def declarado(self) -> dict:
        return {"sampling_mode": self._sampling_mode, "n_runs": self._n_runs,
                "seed": self._seed, "scale": self._scale}

    @property
    def identidad(self) -> dict:
        return {"config_id": self._config_id, "timestamp": self._timestamp}

    # ── ciclos ───────────────────────────────────────────────────────────────

    @property
    def ciclos(self) -> tuple[Ciclo, ...]:
        """La traza completa, del primero al vigente. Tupla: no se edita."""
        with self._lock:
            return self._ciclos

    @property
    def ciclo_vigente(self) -> Ciclo:
        """
        El ciclo vigente, entero, en una sola operación bajo el lock (D3, I2).

        Levanta si todavía no hay ninguno: una config sin ciclo no tiene
        vigencia que devolver, y devolver None dejaría al consumidor
        decidiendo qué significa. Con `create` nunca pasa.
        """
        with self._lock:
            if not self._ciclos:
                raise RuntimeError(
                    "la config no tiene ningún ciclo — se construye con "
                    "CKMlandscapeConfig.create(W, ...), que abre el bootstrap"
                )
            return self._ciclos[-1]

    def abrir_ciclo(
        self,
        W         : np.ndarray,
        causa     : str,
        t_rebuild : float,
        *,
        t_senal   : Optional[float] = None,
    ) -> bool:
        """
        Transición única. Devuelve True si abrió un ciclo nuevo.

        Si la W es la misma que la del ciclo vigente (mismo sha256) no hace
        nada y devuelve False: el mismo w_version_id tiene el mismo medido
        (I5), así que un ciclo nuevo no agregaría información.

        Síncrono (D2): al retornar True, `ciclo_vigente` ya es el nuevo. El
        reemplazo es **un solo cambio de referencia** de la tupla, bajo el
        mismo lock que la lectura.
        """
        sha = sha256_W(np.asarray(W, dtype=float))
        nuevo = Ciclo(
            w_version_id = sha,
            causa        = causa,
            t_senal      = t_senal,
            t_rebuild    = float(t_rebuild),
            **medido(W),
        )
        with self._lock:
            if self._ciclos and self._ciclos[-1].w_version_id == sha:
                return False                                   # I5
            self._ciclos = self._ciclos + (nuevo,)             # I1: gana, no edita
            return True

    def vigente(self, W: np.ndarray) -> bool:
        """I3: la config está vigente para W si el ciclo vigente es el de W."""
        with self._lock:
            if not self._ciclos:
                return False
            return self._ciclos[-1].w_version_id == sha256_W(np.asarray(W, dtype=float))

    def deriva(self, i: int = -1) -> Optional[float]:
        """La deriva del ciclo i (por defecto, el vigente). None si no hubo señal."""
        with self._lock:
            return self._ciclos[i].deriva

    # ── panel y serialización ────────────────────────────────────────────────

    def registrar_tick(self, tick: int, reloj: str) -> None:
        """
        Anota el tick vigente del canal. **La Config registra; no genera.**

        Decisión de delamor (8 oct, E3): el canal genera los ticks con su
        propio reloj, y la Config los *porta* en el sentido de registrarlos —
        como dimensión del landscape. **La dependencia no se invierte:** acá
        entra un número que alguien trajo, y la Config no llama al canal ni lo
        conoce. Quien lo trae es Monitor.

        `reloj` dice de qué reloj viene (decisión 3): la diferencia entre el
        reloj del canal, el del proceso de Monitor y el del device **no se
        borra, se nombra**. Los `Ciclo` se sellan con el del proceso de
        Monitor; esto viene del canal, y por eso lo dice.

        No abre ni cierra ciclos: el tick avanza siempre y un ciclo se abre
        sólo cuando cambia W (I5). Son dos ejes del mismo objeto.
        """
        with self._lock:
            self._tick = int(tick)
            self._tick_reloj = str(reloj)

    @property
    def tick(self) -> Optional[int]:
        """El último tick registrado, o None si nadie lo anotó todavía."""
        with self._lock:
            return self._tick

    @property
    def tick_reloj(self) -> Optional[str]:
        """De qué reloj viene el tick registrado (decisión 3)."""
        with self._lock:
            return self._tick_reloj

    # ── el lugar de la calibración (D3) ──────────────────────────────────────

    def registrar_calibracion(self, registro: Optional[dict]) -> None:
        """
        Anota el registro de la última calibración. **Un solo escritor.**

        Lo llama `CKMMonitor._calibrar_antes_de_instalar`, que es el punto único
        de *"antes de instalar una W"* (D2). Nadie más escribe acá: es lo que la
        visión de delamor pide —*"cada uno guarda lo suyo, con su atribución, en
        **su lugar**… es DONDE, ese es el candado"*—.

        **La Config registra; no genera** (igual que `registrar_tick`): acá entra
        un registro que alguien produjo, y la Config no llama a `calibrate` ni lo
        conoce.

        **El lugar es perpetuo** (delamor, 27 oct: *"EL LUGAR DONDE NACE ES
        PERPETUO. es el estado"*): el registro se escribe **cuando se produce**,
        que es **antes** de que exista el ciclo al que describe —`calibrate`
        corre sobre la W candidata y el ciclo lo abre Monitor después de
        instalarla—. Por eso no vive dentro del `Ciclo`, que es `frozen` y nace
        más tarde: el ciclo que nace lo **referencia** por su `w_sha`.

        `None` lo deja en *"no hubo registro"*. No se mezcla con
        `nulo_calibrado`, que es un estado de `calibrate` y dice *"no se
        ejecutó"*: uno es "nadie anotó", el otro es "alguien anotó que no corrió".
        """
        with self._lock:
            self._calibracion = dict(registro) if registro is not None else None

    @property
    def calibracion(self) -> Optional[dict]:
        """
        El registro de la última calibración, o `None` si no hubo ninguno.

        Copia: el lugar no se edita desde afuera. `w_sha` adentro dice **de qué
        W** es, y es lo que permite ver si la vara que usa un COCO salió de la W
        que ese COCO juzga.
        """
        with self._lock:
            return dict(self._calibracion) if self._calibracion is not None else None

    @property
    def calibrate_declarado(self) -> dict:
        """
        Con qué corre `calibrate`, **declarado acá y no como default de
        función** (D6', 27 oct 2026).

        `None` en un campo es **"nadie lo declaró"**, y entonces quien llame a
        `calibrate` cae en el default de `calibrate.py` — que es exactamente lo
        que este lugar existe para hacer visible. No se rellena con un número.
        """
        with self._lock:
            return {
                "n_runs": self._calibrate_n_runs,
                "seed": self._calibrate_seed,
                "grilla_lambda": (list(self._calibrate_grilla)
                                  if self._calibrate_grilla is not None else None),
                # Qué campos nadie declaró. Va explícito para que una lectura
                # del panel no tenga que deducirlo de los `null`.
                "sin_declarar": sorted(
                    k for k, v in (("n_runs", self._calibrate_n_runs),
                                   ("seed", self._calibrate_seed),
                                   ("grilla_lambda", self._calibrate_grilla))
                    if v is None
                ),
            }

    def panel(self) -> dict:
        """
        I7: identidad + declarado + el ciclo vigente, **sin la historia**.

        Un panel es una foto del momento en que se produjo. La traza de ciclos
        vive en la config, no viaja en cada panel.
        """
        with self._lock:
            return {
                **self.identidad,
                **self.declarado,
                "ciclo_vigente": self._ciclos[-1].to_dict() if self._ciclos else None,
                # El tick del canal y de qué reloj viene. None si nadie lo
                # anotó: sin canal no hay tick, y eso es UNKNOWN, no 0.
                "tick": self._tick,
                "tick_reloj": self._tick_reloj,
            }

    def to_dict(self) -> dict:
        """La config completa, con la historia. Es lo que recarga from_dict."""
        with self._lock:
            return {
                **self.identidad,
                **self.declarado,
                "ciclos": [c.to_dict() for c in self._ciclos],
            }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def from_dict(cls, d: dict) -> "CKMlandscapeConfig":
        """Recarga: mismos valores, mismo config_id, misma historia de ciclos."""
        return cls(
            sampling_mode = d["sampling_mode"],
            n_runs        = d.get("n_runs", N_RUNS_DEFAULT),
            seed          = d.get("seed", SEED_DEFAULT),
            scale         = d.get("scale"),
            config_id     = d["config_id"],
            timestamp     = d["timestamp"],
            ciclos        = tuple(Ciclo.from_dict(c) for c in d.get("ciclos", ())),
        )

    @classmethod
    def from_json(cls, s: str) -> "CKMlandscapeConfig":
        return cls.from_dict(json.loads(s))

    def __repr__(self) -> str:
        with self._lock:
            n = len(self._ciclos)
            sha = self._ciclos[-1].w_version_id[:8] if n else "—"
        return (f"CKMlandscapeConfig(sampling_mode={self._sampling_mode!r}, "
                f"n_runs={self._n_runs}, seed={self._seed}, "
                f"ciclos={n}, vigente={sha}…)")


# ── lectura de la traza vieja ────────────────────────────────────────────────

def ciclo_desde_registro_plano_v1(d: dict) -> Ciclo:
    """
    Lee un registro plano de la config v1 como **un único ciclo**.

    Los JSONL ya escritos (`process/model_properties_front_20261004/run_conteo_vs_masa_04oct/log_conteo_vs_masa.jsonl`,
    antes `P1P4/`)
    llevan la config v1 serializada plana. **No se reescriben**: se leen con
    este mapeo, declarado en el CP0 (BANDEJA_code, pregunta P4):

        plano → (causa="bootstrap", t_senal=None, t_rebuild=timestamp)

    theta_W y scale del registro viejo no entran al Ciclo: el primero es del
    Gatekeeper y el segundo es declarado, no medido. Quedan en el registro
    como dato histórico.
    """
    return Ciclo(
        w_version_id   = d["w_version_id"],
        N              = d["N"],
        mu_W_nonzero   = d["mu_W_nonzero"],
        mu_W_global    = d["mu_W_global"],
        beta_c_nonzero = d["beta_c_nonzero"],
        beta_c_global  = d["beta_c_global"],
        causa          = CAUSA_BOOTSTRAP,
        t_senal        = None,
        t_rebuild      = float(d["timestamp"]),
    )


def _beta_c(N: int, mu_W: float) -> float:
    """β_c = 1 / (ρ* · N · μ_W). Misma fórmula que COCO.beta_c_corpus."""
    if mu_W <= 0:
        return float("inf")
    return 1.0 / (RHO_STAR * N * mu_W)
