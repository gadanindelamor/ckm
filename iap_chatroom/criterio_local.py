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

1. **El piso** (`piso_ticks`): deterministico. Pasados N ticks sin llamar, se
   llama. Es lo que impide que el silencio sea punto fijo, y lo que hace que el
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
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

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


@dataclass(frozen=True)
class UmbralesCriterioLocal:
    """
    Los umbrales del filtro. **`calibrado=False` por defecto, y ese False viaja
    en cada registro** — no en un comentario.

    delamor/Opus: *"los umbrales son declarados (son de Calibracion) y no los
    inventa Code"*. Sin valores no hay codigo, asi que los valores de aca son
    **provisorios y lo dicen de si mismos**: todo registro que sale del filtro
    lleva `umbrales_calibrados: False`, y cualquier lectura que se haga de una
    corrida con este default esta leyendo numeros sin calibrar.

    Si Calibracion entrega numeros, se reemplazan y se pone `calibrado=True`.

    `piso_ticks` **no es un umbral de calibracion en el mismo sentido**: su
    valor es calibrable, pero que exista y sea finito no lo es — es lo que
    impide que el silencio sea absorbente. `piso_ticks=0` desactiva el piso y
    el filtro vuelve a ser absorbente; hay un test que lo afirma.
    """

    # Δt minimo desde la ultima llamada para que el criterio por si solo llame.
    # Provisorio: el orden de magnitud sale del `poll_interval=5.0` de los dos
    # vivos. Sin calibrar.
    dt_minimo_s: float = 5.0

    # Vueltas sin llamar tras las cuales se llama igual. Ver el docstring: que
    # exista no es calibracion.
    piso_ticks: int = 12

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
class CriterioLocal:
    """
    El filtro. Tiene estado: cuando fue la ultima llamada a D.

    Ese estado es exactamente lo que lo hace capaz de volver absorbente al
    silencio, y tambien lo que permite el piso. No se puede tener uno sin el
    otro: por eso el piso no es opcional.
    """

    umbrales: UmbralesCriterioLocal = field(default_factory=UmbralesCriterioLocal)
    # RNG inyectable: con la auditoria al azar y sin semilla, un test de
    # "el filtro llama alguna vez" saldria flaky y no distinguiria un filtro
    # absorbente de una tirada de moneda.
    rng: random.Random = field(default_factory=random.Random)

    # Estado interno. -1 es "nunca llamo", no "llamo en el tick -1".
    _tick_ultima_llamada: int = -1
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
                    "piso_ticks": umb.piso_ticks,
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
                self._tick_ultima_llamada = tick if tick is not None else -1
                self._vueltas_sin_llamar = 0
            else:
                self._vueltas_sin_llamar += 1
            return r

        # (a) El clock UNKNOWN: se llama. No se puede evaluar el piso sin tick.
        if tick is None:
            return registro(True, "tick_UNKNOWN", VIA_CRITERIO)

        # (b) La primera vuelta: **nunca llamo** no es "llamo hace 0 vueltas".
        #     El estado del filtro arranca en UNKNOWN, y arrogarse el silencio
        #     sobre un device que todavia no decidio nada es el mismo relleno
        #     de ausencias que vengo sacando de todo el resto. Ademas sostiene
        #     la iniciativa desde la vuelta 1 y no desde la 12.
        if self._tick_ultima_llamada == -1 and self._vueltas_sin_llamar == 0:
            return registro(True, MOTIVO_PRIMERA, VIA_CRITERIO)

        # (c) El piso, deterministico. Va antes que todo lo demas
        #     para que ningun criterio posterior pueda dejarlo sin efecto.
        if umb.piso_ticks > 0 and self._vueltas_sin_llamar >= umb.piso_ticks:
            return registro(True, MOTIVO_PISO, VIA_PISO)

        # (d) El criterio propiamente: lo que cambio.
        if nombrado:
            return registro(True, MOTIVO_NOMBRADO, VIA_CRITERIO)
        if n_nuevos > 0:
            return registro(True, MOTIVO_MENSAJES, VIA_CRITERIO)

        # (e) La auditoria: se llama aunque el criterio diga que no, para medir
        #     el costo del sesgo. No sostiene la iniciativa — eso es (b).
        if self.rng.random() < umb.tasa_auditoria:
            return registro(True, MOTIVO_AUDITORIA, VIA_AUDITORIA)

        # (f) El skip, con su motivo y sus deltas.
        return registro(False, MOTIVO_SIN_CAMBIO, None)


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
