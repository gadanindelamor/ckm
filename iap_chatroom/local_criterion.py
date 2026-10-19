"""
Criterio local: el filtro sin LLM que decide **si vale la pena llamar a D**.

Propuesta de delamor (7 oct 2026), habilitada como CP2b (DECISIONES `e737e78`).
No decide *qué* hacer — eso es de D. Decide si esta vuelta paga una llamada.

----------------------------------------------------------------------------
EL SILENCIO ABSORBENTE ES DEL FILTRO, NO DEL DEVICE  (correccion de Opus)
----------------------------------------------------------------------------

El filtro esta **entre O y D**. Es el unico de los dos que tiene estado ahi, y
por eso el unico que puede hacer absorbente al silencio:

    criterio = "cambio algo?" mirando solo los mensajes
    -> canal callado: no cambio nada
    -> no llama a D
    -> el device no decide
    -> el canal sigue callado

El silencio se vuelve **punto fijo del lazo**, no decision del modelo. Y desde
afuera se ve igual que un `OP_SILENCE`: es el par vivo 01 / vivo 02 otra vez
(`{'UNKNOWN': 24}` por infraestructura vs `{'OP_SILENCE': 23}` por decision),
con el filtro en el lugar del provider caido.

De ahi las dos piezas que **no** son calibracion:

1. **El piso** (`piso_vueltas`): deterministico. Pasadas N **vueltas** sin
   llamar, se llama. Es lo que impide que el silencio sea punto fijo, y lo que hace que el
   test pueda fallar **por el motivo correcto**.

2. **La auditoria** (`tasa_auditoria`): al azar, sobre las dos caras. Rompe el
   punto fijo **en distribucion**, pero Opus: *"no puede ser lo unico que lo
   rompa: si no, la iniciativa queda en manos de la suerte."* Con tasa p hay
   probabilidad positiva de cero llamadas en N vueltas. La auditoria mide el
   **costo del sesgo**; el piso sostiene la **iniciativa**. No se reemplazan.

Nota sobre los Δt como criterio (derivacion de Code, confirmada por Opus): el
Δt desde el ultimo mensaje ajeno crece monotono bajo silencio. Si lo resetea la
**llamada**, ese criterio *es* el piso con otro nombre; si lo resetea solo un
**mensaje**, satura y el filtro deja de filtrar justo donde mas silencio hay.
Por eso aca los Δt entran como **informacion que viaja en el registro**, y el
piso es una pieza propia y no una perilla al lado de ellos.

----------------------------------------------------------------------------
LO QUE NO ESTA, Y SE DECLARA AUSENTE
----------------------------------------------------------------------------

La especificacion nombra tambien el **estado del objetivo (K)** y el
**presupuesto**. No existen todavia: el objetivo es del **caso Z (CP3,
delamor)**. Entran como `None` **declarado ausente** y no como `0` ni `False`:
la ausencia es el estado del observador, no un valor de la escala (§19). Esos
dos, cuando existan, cambian **por fuera del lazo** y por eso no colapsan en el
piso como los Δt.

La **zona horaria propia del device** la TASK la marca opcional (*"si el device
quiere"*). No esta implementada.

----------------------------------------------------------------------------
CP3: EL CORAZON YA NO ESTA ACA  (`TASK_ckm_trust_rule_v1`, orden de delamor)
----------------------------------------------------------------------------

Hasta el CP2 este archivo tenia **su propio corazon**: la cascada de `if` que
decidia, con el empate, el piso y el origen escritos aca adentro. Era "la traza
de como era antes". Desde el CP3 **no decide**: arma su instancia de
`CkmTrustRule` y **lee** la `Decision`. Los pasos 1-4 viven una sola vez, en
`services/ckm_trust_rule.py`.

El mapeo es el del CP0 del CP2 (`c620d70`, aceptado por delamor) y verificado
bit a bit en `tests/test_local_criterion_como_instancia.py` (24/24 sobre el vivo
03). Aca va **tal cual**, mas la unica pieza que el CP2 no podia poner:

- **`tick = None` entra por el piso.** El CP2 lo dejo declarado como alineado
  (decision 5 del 12 oct) y **no medible** en el vivo 03 (0 de 24). La forma de
  decirlo es `trace_streak = None`: *sin el tick no se puede saber si el piso
  vencio*, que es literalmente el docstring de `evaluar`. El engine marca
  `FLOOR_UNKNOWN`, la traza **no decide** y la duda sube -> se llama a D. El
  resultado es el mismo de siempre; lo que cambia es que ahora **sale de la
  regla** y no de un `if` puesto antes de todo.

**`motivo` y `via` son rotulos, no la decision.** Salen de leer el registro del
engine (`trace_present`, `floor_reached`, `field_inputs`) y las entradas
propias (`tick`). Leer el registro no es reimplementar un paso: por eso el piso
**no se recalcula aca** -- se lee `record["floor_reached"]`.

**LA DIFERENCIA, declarada (no se corrige en silencio).** Hay un caso donde el
rotulo cambia respecto de la cascada anterior: cuando el piso **y** el campo
dan los dos al mismo tiempo (`vueltas_sin_llamar >= piso_vueltas` **y**
`n_nuevos + nombrado > 0`). La cascada evaluaba el piso **antes** que el campo
y rotulaba `piso` / `VIA_PISO`; la forma dice que el campo decide primero, asi
que el engine nunca llega a evaluar el piso y el rotulo es
`mensajes_nuevos`/`nombrado` / `VIA_CRITERIO`.

- **No se pierde la decision: se pierde el rotulo.** `llamar` es la misma en ese
  caso y en todos. Lo medido esta en `tests/test_local_criterion_cp3.py`, que
  barre el espacio de entradas **completo** (312 combinaciones) contra una copia
  congelada de la cascada anterior: 0 difieren en `llamar`, 60 en `motivo` y las
  mismas 60 en `via`, todas la colision.
- **Decision de delamor, 13 oct:** el piso **no se recalcula afuera de la regla**,
  y el rotulo `piso` **se pierde** en la colision, declarado como perdida. No es
  rotulable desde el registro sin ese recalculo, que seria el segundo corazon que
  el CP3 viene a sacar.
- En el vivo 03 ocurre **0 de 24 veces** (lo mide el CP2).

Lo que **no** cambio: la firma de `evaluar`, la forma del registro (las mismas
claves, ninguna nueva), el sorteo de la auditoria y el de `auditado_pase` --con
su orden, que es lo que hace deterministico un RNG con semilla--, el estado
interno y `divergencia_auditoria`.

**EL DOMINIO: la equivalencia vale para `n_nuevos >= 0`.** Afuera cambia la
**decision**, no un rotulo. Con `n_nuevos < 0` y `nombrado=True` la cascada
llamaba --`if nombrado:` iba antes que cualquier cuenta-- y la forma no:
`f = n_nuevos + nombrado <= 0`, asi que el candidato queda empatado (`f = 0 =
kappa`) o por debajo del corte, y la traza conserva el silencio. Lo leyo Opus el
13 oct y esta corrido en
`test_fuera_del_dominio_n_nuevos_negativo_la_decision_cambia`. **Fijado, no
corregido:** corregirlo es una decision sobre el modelo. Desde el lazo vivo no
llega --`autonomous_device.py:711` pasa `len(nuevos)`--, pero `evaluar` es
publica y no valida su entrada.

**UNA RUTA NUEVA: `evaluar` ahora puede levantar.** Antes del CP3 no levantaba
nunca. El `AssertionError` de mas abajo salta cuando la regla dice *llamar* y el
mapeo no tiene rotulo para esa combinacion. **Es alcanzable** --con `f` no
medible (`n_nuevos` NaN) el engine devuelve `ESCALATED · field_value_unknown`
sin haber evaluado el piso, y ninguna rama de rotulo agarra--, y **no llega
desde el lazo vivo** por la misma razon que lo anterior. Se declara en vez de
inventar un motivo, que es lo que el `raise` evita.

**La auditoria no entra en la forma** (CP2): no resuelve un empate, **mide la
regla**. Queda donde estaba, leyendose encima de la decision.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

# El corazon. CP3: este archivo ya no implementa los pasos, los instancia.
from services.ckm_trust_rule import (
    DECLARED,
    FIELD,
    CkmTrustRule,
    RuleParams,
    Threshold,
)

# El tercer valor del vocabulario de salida. Hoy hay dos formas de terminar una
# vuelta sin accion, y son distintas:
#
#   OP_SILENCE  — el modelo decidio no hacer nada     (vivo 02: 23/23)
#   UNKNOWN     — el provider fallo, no hubo decision (vivo 01: 24/24)
#
# El skip es la tercera: **no se llamo**. Va con las otras dos en la traza y se
# distingue de las dos. Es el pedido de Opus: que el par "filtro callo / modelo
# callo" se separe igual que el par 01/02.
DECISION_SKIP = "SKIP"

# Motivos. El motivo va en el registro **del turno**, no en un contador: un
# contador dice cuantos, no cuales, y cuales es lo que hace falta para saber si
# el silencio estaba decidido.
MOTIVO_PISO = "piso"
MOTIVO_AUDITORIA = "auditoria"
MOTIVO_NOMBRADO = "nombrado"
MOTIVO_MENSAJES = "mensajes_nuevos"
MOTIVO_SIN_CAMBIO = "sin_cambio"
MOTIVO_PRIMERA = "primera_vuelta"

# Via por la que se llamo a D. "Por que se llamo" queda tan trazable como "por
# que no": sin esto, una llamada del piso y una del criterio se ven iguales, y
# la tasa de divergencia de la auditoria se mezclaria con las demas.
VIA_CRITERIO = "criterio"
VIA_PISO = "piso"
VIA_AUDITORIA = "auditoria"


# ── El mapeo a la forma (CP3). Los nombres del casillero, una sola vez ──────
#
# `TASK_ckm_trust_rule_v1`, CP0 del CP2 (`c620d70`). Lo que aca se declara es
# **el mapeo**, no `local_criterion`: la kappa = 0 sale de leer `if n_nuevos > 0`,
# y la epsilon no existe en este filtro, asi que va `None` **declarado**.
ORDEN = "b0 — la vuelta del device"   # el orden donde rige esta instancia
CANDIDATO = "llamar"                  # C: un solo candidato, la vuelta
ESCALA_A = "b1 — el LLM"              # ↑k: llamar al modelo **es** escalar

_MAPEO = "el mapeo del CP2 (TASK_ckm_trust_rule_v1, c620d70)"


@dataclass(frozen=True)
class LocalCriterionThresholds:
    """
    Los umbrales del filtro. **`calibrado=False` por defecto, y ese False viaja
    en cada registro** — no en un comentario.

    delamor/Opus: *"los umbrales son declarados (son de Calibracion) y no los
    inventa Code"*. Sin valores no hay codigo, asi que los valores de aca son
    **provisorios y lo dicen de si mismos**: todo registro que sale del filtro
    lleva `umbrales_calibrados: False`, y cualquier lectura que se haga de una
    corrida con este default esta leyendo numeros sin calibrar.

    Si Calibracion entrega numeros, se reemplazan y se pone `calibrado=True`.

    `piso_vueltas` **no es un umbral de calibracion en el mismo sentido**: su
    valor es calibrable, pero que exista y sea finito no lo es — es lo que
    impide que el silencio sea absorbente.

    Por eso **`piso_vueltas <= 0` levanta `ValueError`** (Opus, 9 oct): antes se
    aceptaba, y un `0` desactivaba el piso. El docstring decia que el piso "no
    es opcional" y la configuracion permitia apagarlo: **el texto afirmaba una
    cosa y el constructor otra**. Volver absorbente el silencio no puede ser una
    configuracion valida. El test que exhibe la absorcion sin piso la produce por
    **inversion** (monkeypatch de la rama), que es lo que es.
    """

    def __post_init__(self) -> None:
        if self.piso_vueltas <= 0:
            raise ValueError(
                "piso_vueltas tiene que ser > 0: el piso es lo que impide que "
                "el silencio sea punto fijo del lazo, y apagarlo no es una "
                "configuracion valida (CP2b, Opus 9 oct)"
            )

    # Δt minimo desde la ultima llamada para que el criterio por si solo llame.
    # Provisorio: el orden de magnitud sale del `poll_interval=5.0` de los dos
    # vivos. Sin calibrar.
    dt_minimo_s: float = 5.0

    # Vueltas sin llamar tras las cuales se llama igual. Ver el docstring: que
    # exista no es calibracion.
    piso_vueltas: int = 12

    # LAS DOS TASAS DE AUDITORIA, las dos declaradas y sin calibrar (Opus:
    # "las dos van al azar, con la tasa declarada como 'no calibrada', igual
    # que los umbrales").
    #
    # `tasa_auditoria` — **cara del skip**: el filtro dijo que no y se llama a
    # D igual. Mide lo que cuesta el sesgo de saltear. **Este muestreo cuesta
    # una llamada** por cada vuelta sorteada.
    tasa_auditoria: float = 0.1

    # `tasa_auditoria_pase` — **cara del pase**: el filtro dijo que si y se
    # registra si D termino no actuando. Mide cuantas llamadas dejo pasar sin
    # necesidad; sin esta cara no se puede saber si el filtro "no cuesta".
    #
    # **Este muestreo no cuesta nada**, porque la llamada ya se hizo: lo unico
    # que sortea es si la vuelta queda marcada como auditada. Por eso la cara
    # del pase reporta ademas el **censo** sobre todas las vueltas que pasaron,
    # que es gratis y no descarta nada. Las dos lecturas conviven y cada una
    # dice de donde sale.
    tasa_auditoria_pase: float = 0.1

    calibrado: bool = False


@dataclass
class LocalCriterion:
    """
    El filtro. Tiene estado: cuando fue la ultima llamada a D.

    Ese estado es exactamente lo que lo hace capaz de volver absorbente al
    silencio, y tambien lo que permite el piso. No se puede tener uno sin el
    otro: por eso el piso no es opcional.
    """

    umbrales: LocalCriterionThresholds = field(default_factory=LocalCriterionThresholds)
    # RNG inyectable: con la auditoria al azar y sin semilla, un test de
    # "el filtro llama alguna vez" saldria flaky y no distinguiria un filtro
    # absorbente de una tirada de moneda.
    rng: random.Random = field(default_factory=random.Random)

    # Estado interno. **`None` es "nunca llamo"** (Opus, 9 oct). Antes era `-1`,
    # que representa una ausencia con un valor de la escala: el mismo relleno
    # que vengo sacando de todo el resto, puesto por mi en el archivo nuevo.
    _tick_ultima_llamada: Optional[int] = None
    _vueltas_sin_llamar: int = 0

    def evaluar(
        self,
        *,
        tick: Optional[int],
        n_nuevos: int,
        nombrado: bool = False,
        dt_desde_ajeno: Optional[float] = None,
        dt_desde_que_hable: Optional[float] = None,
        estado_objetivo: Optional[dict] = None,
        presupuesto: Optional[dict] = None,
    ) -> dict:
        """
        Devuelve el **registro** de la vuelta, no un `bool`.

        `n_nuevos` cuenta **solo mensajes ajenos** (TASK §1: el propio mensaje
        entra como "Δt desde que hable", que es informacion y no disparador).
        Quien llama se lo garantiza: el lazo ya filtra
        `m["device_id"] != self.device_id`.

        Los Δt vienen de los **timestamps del canal**, nunca del reloj del
        device (TASK §0.4). `None` es UNKNOWN y no 0: no haber medido un Δt no
        es que el Δt sea cero.

        `tick=None` es el clock UNKNOWN. **Se llama a D.** Sin el tick no se
        puede saber si el piso vencio, y el filtro no se arroga el silencio
        sobre una dimension que no observo.

        Desde el CP3 eso **no es un `if` previo**: entra por el piso. Sin tick,
        `trace_streak=None` -> el engine marca `FLOOR_UNKNOWN`, la traza no
        decide y la duda sube. Mismo resultado, y ahora sale de la regla.

        Devuelve las mismas claves que antes del CP3. **Ninguna nueva**: la
        `Decision` del engine se lee y no se guarda, para que el gate `f96c234`
        valga tambien sobre la forma del registro.
        """
        umb = self.umbrales
        deltas = {
            "n_nuevos": n_nuevos,
            "nombrado": nombrado,
            "dt_desde_ajeno": dt_desde_ajeno,
            "dt_desde_que_hable": dt_desde_que_hable,
            # Declarados ausentes: no existen hasta el caso Z. None, no 0.
            "estado_objetivo": estado_objetivo,
            "presupuesto": presupuesto,
            "vueltas_sin_llamar": self._vueltas_sin_llamar,
        }

        def registro(llamar: bool, motivo: str, via: Optional[str]) -> dict:
            r = {
                "llamar": llamar,
                "motivo": motivo,
                "via": via,
                "tick": tick,
                "deltas": deltas,
                # El False viaja en el registro, no en un comentario.
                "umbrales_calibrados": umb.calibrado,
                "umbrales": {
                    "dt_minimo_s": umb.dt_minimo_s,
                    "piso_vueltas": umb.piso_vueltas,
                    "tasa_auditoria": umb.tasa_auditoria,
                    "tasa_auditoria_pase": umb.tasa_auditoria_pase,
                },
            }
            if llamar:
                # El sorteo de la cara del pase: no decide si se llama (ya se
                # llama), sino si esta vuelta entra a la muestra.
                if via in (VIA_CRITERIO, VIA_PISO):
                    r["auditado_pase"] = (
                        self.rng.random() < umb.tasa_auditoria_pase
                    )
                # el tick de la llamada, o None si el clock estaba UNKNOWN:
                # no se sabe en que tick se llamo, y eso no es el tick -1
                self._tick_ultima_llamada = tick
                self._vueltas_sin_llamar = 0
            else:
                self._vueltas_sin_llamar += 1
            return r

        # ── LA REGLA DECIDE. Los pasos 1-4 no estan aca (CP3) ───────────
        dec = self._regla(n_nuevos=n_nuevos, nombrado=nombrado).decide(
            [CANDIDATO],
            # `capacity=None`: no hay lugares que contar, asi que la exencion
            # del paso 1 no aplica. Con `capacity=1` el empate exacto tendria
            # un lugar libre y daria **llamar**: invertiria el skip (medido en
            # el CP2, 17 de 24).
            capacity=None,
            # T: el silencio. En la primera vuelta **no hay traza**.
            trace=None if self._sin_traza() else frozenset(),
            # P: sin el tick el piso **no es evaluable**. `None` declarado, no
            # 0 (decision 5 del 12 oct). De aca sale el viejo `tick_UNKNOWN`.
            trace_streak=None if tick is None else self._vueltas_sin_llamar,
            turn_ref={"tick": tick},
            # f es la suma, asi que pierde cual de los dos disparo: el registro
            # del engine los conserva por separado.
            field_inputs={"n_nuevos": n_nuevos, "nombrado": nombrado},
        )
        # `ESCALATED` -> llamar es literal: llamar al modelo **es** escalar.
        llamar = (dec.value is None) or (CANDIDATO in dec.value)

        # ── Los rotulos: se LEEN del registro, no se vuelven a decidir ──────
        # El orden de abajo es el de los rotulos de siempre, para que la traza
        # siga diciendo lo mismo. No es el orden de la decision: eso ya paso.
        if llamar:
            if tick is None:
                # el piso no se pudo evaluar, y la unica razon posible aca es
                # que no hubo tick: `piso_vueltas > 0` lo garantiza el
                # __post_init__, y el piso siempre esta declarado.
                return registro(True, "tick_UNKNOWN", VIA_CRITERIO)
            if not dec.record["trace_present"]:
                return registro(True, MOTIVO_PRIMERA, VIA_CRITERIO)
            if dec.record.get("floor_reached"):
                return registro(True, MOTIVO_PISO, VIA_PISO)
            if dec.origin == FIELD:
                # LA DIFERENCIA declarada en el docstring: si el piso tambien
                # estaba vencido, el engine no llego a evaluarlo y el rotulo
                # es el del campo. La decision es la misma; el rotulo no.
                return registro(
                    True,
                    MOTIVO_NOMBRADO if nombrado else MOTIVO_MENSAJES,
                    VIA_CRITERIO,
                )
            # No hay rotulo para esto. El mapeo se declara total y, si no lo
            # es, lo dice: inventar un motivo seria afirmar lo que no se sabe.
            raise AssertionError(
                f"llamar sin rotulo: origin={dec.origin!r} reason={dec.reason!r} "
                f"record={dec.record!r}"
            )

        # La auditoria **no es de la regla**: no resuelve un empate, la mide.
        # Se llama aunque la regla diga que no, para ver el costo del sesgo. No
        # sostiene la iniciativa — eso es el paso 3 sin traza.
        if self.rng.random() < umb.tasa_auditoria:
            return registro(True, MOTIVO_AUDITORIA, VIA_AUDITORIA)

        # El skip, con su motivo y sus deltas.
        return registro(False, MOTIVO_SIN_CAMBIO, None)

    # ------------------------------------------------------------------
    def _sin_traza(self) -> bool:
        """
        T no existe: **nunca llamo** no es "llamo hace 0 vueltas".

        El estado del filtro arranca en UNKNOWN, y arrogarse el silencio sobre
        un device que todavia no decidio nada es el mismo relleno de ausencias
        que vengo sacando de todo el resto. Ademas sostiene la iniciativa desde
        la vuelta 1 y no desde la 12.

        Llenar el casillero T es del instanciador; **decidir con el** es del
        engine (paso 2).
        """
        return self._tick_ultima_llamada is None and self._vueltas_sin_llamar == 0

    def _regla(self, *, n_nuevos: int, nombrado: bool) -> CkmTrustRule:
        """
        La instancia de la vuelta: ``Regla_k = <C, f, R, kappa, eps, T, P, g, ^k>``.

        Se arma por vuelta porque **f es de la vuelta**: cierra sobre
        `n_nuevos` y `nombrado`. Los umbrales no cambian; f si.

        | casillero | que es aca |
        |---|---|
        | **C** | la vuelta. Un candidato: `"llamar"` |
        | **f** | `n_nuevos + nombrado` |
        | **kappa** | **0**, `DECLARED` **por el mapeo**: sale de leer `if n_nuevos > 0` |
        | **eps** | `None` **declarado**: este filtro no tiene epsilon |
        | **T** | el silencio (`_sin_traza`), y `P` = `piso_vueltas` |
        | **g** | **no hay**. La auditoria no es un `g`: mide la regla |
        | **^k** | el LLM. `ESCALATED` -> llamar |

        `g=None` quiere decir que **no hay paso 4**: sin traza y sin piso, la
        duda sube y no se resuelve aca (I5).
        """
        umb = self.umbrales
        return CkmTrustRule(
            order=ORDEN,
            params=RuleParams(
                cut=Threshold(
                    value=0.0, produced_by_order=_MAPEO, provenance=DECLARED,
                    source="sale de leer `if n_nuevos > 0`, la cascada anterior",
                ),
                tolerance=Threshold(
                    value=None, produced_by_order=_MAPEO, provenance=DECLARED,
                    source="local_criterion no declara epsilon (TASK, 11 oct)",
                ),
                floor=Threshold(
                    value=umb.piso_vueltas, produced_by_order=_MAPEO,
                    provenance=DECLARED,
                    source=("LocalCriterionThresholds.piso_vueltas, "
                            f"calibrado={umb.calibrado}"),
                ),
            ),
            field_criterion=lambda _c: n_nuevos + int(bool(nombrado)),
            context=None,
            escalate_to=ESCALA_A,
        )


def divergencia_auditoria(registros: list[dict]) -> dict:
    """
    El costo del sesgo, **sobre las dos caras** (spec: *"auditoria al azar
    sobre las dos caras"*; Opus: *"que no se le vea a uno solo de los lados"*).

    Las dos caras del filtro no son simetricas, y por eso se miden distinto:

    | cara | que seria el error | como se mira |
    |---|---|---|
    | **el filtro dijo "no"** | tapo una decision | **muestreo**: la auditoria llama igual, al azar |
    | **el filtro dijo "si"** | pago una llamada de mas | **muestreo** con su tasa declarada, **mas el censo**, que es gratis |

    Las dos tasas van **declaradas y sin calibrar**, igual que los umbrales
    (Opus, CP0: *"las dos van al azar, con la tasa declarada"*).

    **Lo que medi, y lo digo porque lo medi:** el muestreo de las dos caras no
    cuesta lo mismo. En la cara del skip, cada vuelta sorteada **cuesta una
    llamada** —es lo que paga por ver lo que el filtro tapaba—. En la cara del
    pase **la llamada ya se hizo**, asi que el sorteo no ahorra nada y lo unico
    que hace es descartar observaciones gratis. Por eso esa cara lleva las dos
    lecturas: la muestra con su tasa declarada, y el **censo** sobre todas las
    vueltas que pasaron. No elijo por el lector: las dos estan, etiquetadas.

    Lo que devuelve, por cara: cuantas vueltas, cuantas con decision mirable, y
    cuantas **divergieron** — D hizo algo distinto de nada en la cara del skip
    (el filtro tapaba), o D no hizo nada en la cara del "si" (el filtro pago de
    mas).

    `tasa=None` cuando no hay nada mirable en esa cara. **No es 0.0**: 0.0
    afirma que se miro y no divergio.
    """
    sin_accion = ("OP_SILENCE", "UNKNOWN", DECISION_SKIP)

    def cara(regs: list[dict], divergio) -> dict:
        con_decision = [r for r in regs if r.get("decision") is not None]
        div = [r for r in con_decision if divergio(r["decision"])]
        return {
            "n_vueltas": len(regs),
            "n_con_decision": len(con_decision),
            # no haber mirado no es haber visto que no
            "n_sin_decision": len(regs) - len(con_decision),
            "n_divergieron": len(div),
            "tasa": (len(div) / len(con_decision)) if con_decision else None,
        }

    auditados = [r for r in registros if r.get("via") == VIA_AUDITORIA]
    pasaron = [
        r for r in registros
        if r.get("llamar") and r.get("via") in (VIA_CRITERIO, VIA_PISO)
    ]

    return {
        # la cara invisible: se muestrea
        "dijo_no": {
            "metodo": "muestreo",
            **cara(auditados, lambda d: d not in sin_accion),
            "que_mide": "el filtro tapaba una decision",
        },
        # La cara del pase. **Dos lecturas, y cada una dice de donde sale:**
        # la muestra al azar con su tasa declarada (Opus, CP0), y el censo
        # sobre todas las vueltas que pasaron. El censo es gratis —la llamada
        # ya se hizo— y no descarta nada; la muestra existe porque la tasa
        # quedo declarada para las dos caras.
        "dijo_si": {
            "metodo": "muestreo+censo",
            **cara([r for r in pasaron if r.get("auditado_pase")],
                   lambda d: d in sin_accion),
            "censo": cara(pasaron, lambda d: d in sin_accion),
            "que_mide": "el filtro pago una llamada de mas",
        },
        # compatibilidad con la lectura de una sola cara, que es la que pedia
        # la spec original. Queda, y dice de que cara habla.
        "n_auditados": len(auditados),
        "n_con_decision": cara(auditados, lambda d: True)["n_con_decision"],
        "n_sin_decision": cara(auditados, lambda d: True)["n_sin_decision"],
        "n_divergieron": cara(auditados, lambda d: d not in sin_accion)["n_divergieron"],
        "tasa": cara(auditados, lambda d: d not in sin_accion)["tasa"],
    }


def dt_desde(clock_t: Optional[float], timestamp_iso: Optional[str]) -> Optional[float]:
    """
    Δt entre el tick observado y un mensaje, **los dos del reloj del canal**.

    TASK §0.4: *"Los Δt que entran a D (y al criterio local) se calculan con
    los timestamps del canal, nunca mezclando el reloj del device con el del
    canal."* `clock_t` sale de `get_clock()` y `timestamp_iso` del mensaje:
    ambos los puso `ChatChannel._ahora()`.

    Devuelve `None` —UNKNOWN— si falta alguno de los dos o si el timestamp no
    se puede leer. **No devuelve 0.0**: que no se haya podido medir el Δt no es
    que el Δt sea cero, y un 0.0 ahi haria que el criterio lea "recien ahora"
    sobre algo que nunca midio.
    """
    if clock_t is None or not timestamp_iso:
        return None
    try:
        from datetime import datetime

        return clock_t - datetime.fromisoformat(timestamp_iso).timestamp()
    except (ValueError, TypeError):
        return None
