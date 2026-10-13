"""
ckm_trust_rule.py — la regla CKM TRUST como **un solo corazón**

`TASK_ckm_trust_rule_v1`, CP1. delamor: *"que evite duplicar el corazón en cada
aplicación de la regla"*. Los pasos 1–4, el empate con ε, el piso, el origen y el
registro viven **una sola vez**: acá. Cada aplicación es una **instancia** que le
pasa sus elementos al engine y **no reimplementa ningún paso**.

**El módulo es puro**: no importa nada del repo, no escribe nada, no tiene
estado entre llamadas.

**CP3 (13 oct, orden de delamor): ya lo llama alguien.** `iap_chatroom/
criterio_local.py` es la primera instancia en producción: le pasa sus
casilleros y lee la `Decision`. El gate `f96c234` se sostuvo donde importa —las
24 decisiones del vivo 03 y las 312 combinaciones del barrido dan lo mismo que
antes—, y la única diferencia es un **rótulo** en la colisión piso-campo, que
está declarada en el docstring de ese archivo y medida en
`tests/test_criterio_local_cp3.py`.

## La forma, con el nombre largo de cada letra

Fuente: `REG_regla_ckm_trust_v1` §1 y §3 (la regla es textual, de delamor), más
las decisiones del 12 oct en `docs/tasks/DECISIONES_opus.md`. Los nombres largos
van acá para que **una instancia que arranca en frío** entienda el módulo sin la
conversación (condición de delamor).

    Regla_k = ⟨ C, f, R, κ, ε, T, P, g, ↑k ⟩

- **C — candidates:** los candidatos sobre los que se decide (pares, nodos,
  estados, órdenes, o la única cosa que se decide esta vuelta).
- **f — field_criterion:** el criterio **de campo**, `f: C → ℝ`. **Hay uno solo**
  (delamor, 12 oct): el piso y la regla de contexto son casilleros propios, no
  criterios en cascada.
- **R — Decision.record:** el registro de la decisión. Trae `f` por candidato, su
  distancia al corte, los umbrales con su origen, los marcadores y la referencia
  de la vuelta. "R" es **sólo** esto: un nombre, una cosa.
- **κ — cut:** el umbral de la decisión.
- **ε — tolerance:** la tolerancia **de la regla**, no numérica. Obligatoria y sin
  default. `None` se acepta sólo como *"no se sabe"*, **declarado**.
- **T — trace:** la selección, el estado o la órbita **anterior**. El paso 2
  conserva: *"gana el que ya está, ya estuvo, ya ganó"*.
- **P — floor:** el piso. Cuántas veces puede decidir la traza **sin que el campo
  decida** antes de que la duda tenga que subir. Sin piso, el silencio es
  absorbente.
- **g — context:** un criterio que **no sale del campo** (orden alfabético,
  semilla, primera aparición, una clasificación hecha a mano). Es sesgo potencial,
  y por eso va **nombrado**.
- **↑k — escalate_to:** el **nombre** del orden de arriba. Ver "I5, estructural".

## Los cuatro pasos

    0. κ no se sabe, o `f` no pudo medir a algún candidato (NaN):
       `f` no se puede aplicar sobre ese conjunto: la duda SUBE.
                                                        origin = ESCALATED
    1. |f(c) − κ| > ε           → decide f              origin = FIELD
       · si el empate cabe en los lugares libres, entra  origin = FIELD
    2. empate y existe T        → decide T (conserva)   origin = TRACE
       · si el piso P se cumplió → 3
       · si el piso **no se puede evaluar** → 3
       · si lo que la traza conserva **no cabe** en los lugares libres → 3
    3. no hay T (o el piso se cumplió, o no se pudo evaluar, o la traza no
       alcanzó) → NO_TRACE: la duda SUBE.               origin = ESCALATED
    4. **sin ↑k** y con un g declarado de otro orden
                                → decide g              origin = CONTEXT

El paso 0 es la rama *"¿se aplicó f? no"* del paso 3, no un paso 1 que falla: sin
corte no se inventa un corte, y sin poder medir a un candidato no se decide sobre
un conjunto que lo perdió. Y el paso 4 **no corre si hay ↑k**: mientras el orden
de arriba no haya hablado, la duda está arriba y no en el `g`.

## `f` que no pudo medir — NaN no es "afuera"

Si `f(c)` devuelve **NaN**, todas las comparaciones contra el corte dan `False`,
así que el candidato **no queda ni arriba, ni abajo, ni empatado**: se cae de la
decisión **sin marca**. Eso es I2 por la puerta de atrás — una ausencia con el
valor "afuera".

Acá no se descarta nada: el candidato queda en el registro, nombrado en
`record["field_value_unknown"]`, con `field_value` y `distance_to_cut` en `None`
declarado; la decisión lleva el marcador `FIELD_VALUE_UNKNOWN`; y **no puede ser
`FIELD`**, porque sería campo sobre un conjunto que perdió un candidato. **La duda
sube.**

`f` tiene que devolver un `float`. Si devuelve `None`, `float(None)` levanta
`TypeError` y **eso no está cubierto acá**: cuando `f` no puede medir a un
candidato, devuelve NaN y el módulo lo declara.

## Las cuatro decisiones del 12 oct, y cómo están en el código

**F2 — son dos órdenes, no una contradicción** (delamor). En el orden k rige I5:
quedarse, no resolver — el equivalente mecánico de *TRY TO STAY THERE*. El `g` del
paso 4 es de **otro** orden: el de quien lo declaró, y **llega declarado antes**,
como traza. No decide el orden k.

- **I5, estructural:** `escalate_to` es un **`str`**, no un invocable. El módulo lo
  **registra y nunca lo llama**. Si lo llamara, resolvería el paso 3, que es justo
  lo que I5 prohíbe. Así que I5 no es una convención de uso: no hay cómo violarla.
- Con `escalate_to` puesto, el paso 3 devuelve `ESCALATED` nombrando a quién sube,
  y **no aplica `g`**: el orden de arriba todavía no habló.
- Sin `escalate_to` y **sin** `context`, devuelve `ESCALATED` con
  `escalate_to=None` y la duda queda registrada. **No resuelve.**
- *"↑k no decide"* **no se puede representar en una llamada pura.** Quien llama lo
  expresa volviendo a llamar **sin** `escalate_to`, una vez que ↑k no decidió.
  Queda dicho acá porque es la única forma de llegar al paso 4 teniendo ↑k.
- El módulo **nunca inventa un `g`**: sin `context` declarado, no hay paso 4.

**Un solo criterio de campo** (delamor). `field_criterion` es uno. El mapeo de
`should_rebuild`, que hoy tiene tres criterios en cascada, es:
estructural → `f`, tiempo → `P` (vueltas sin decisión del campo), volumen → `g`
declarado. **No son tres `f`: era la implementación.** El mapeo se declara acá;
no se renombra nada de lo que existe.

**κ y ε con origen** (delamor, *"A ∪ B: el alguien que declaró es la
recursividad"*). No hay "κ que entra" y "κ que sale": es el **mismo** κ visto desde
dos órdenes. Todo umbral lo produce el orden de arriba, **midiendo** (`MEASURED`,
`calibrate`) o **declarando** (`DECLARED`: alguien, una sesión). Por eso cada
`Threshold` lleva `produced_by_order`, `provenance` y `source`, y **`provenance` es
obligatoria siempre**: un *"no se sabe"* también se declara, y la ausencia conserva
su origen (I1). Nunca 0 implícito (I2).

**La hélice** (delamor). `device → texto → corpus → W → device` no es un ciclo:
cada vuelta ocurre sobre **otra** W, así que la recursión tiene caso base. Cada
`Decision` lleva `turn_ref`, la referencia de la vuelta que le pasa quien llama
(por ejemplo un `w_version_id`). **El módulo no la interpreta: la guarda.**

## ε desconocida — lo único derivable sin inventar un número

Con `tolerance.value = None` **"cerca del corte" no está definido**. Lo que sí se
deriva: `|f(c) − κ| = 0` es empate **bajo cualquier ε ≥ 0**, así que la igualdad
exacta **es** empate aunque ε no se sepa. Y toda decisión viaja marcada
`TOLERANCE_UNKNOWN`, porque no se puede saber si lo de al lado del corte era
empate.

**No es lo mismo que `ε = 0`:** con ε = 0 nada se marca. En la igualdad exacta las
dos coinciden, y **esa coincidencia queda declarada acá**. El precedente es del
propio repo: `landscape_engine.py:74` (`h = 0` conserva `s_i`) hace exactamente
eso, con ε = 0 implícito.

## El piso pide un reloj, y el módulo no se lo inventa

`P` cuenta repeticiones, y contar pide estado entre llamadas. El módulo es puro:
el contador lo pasa **quien llama**, en `trace_streak`. La ausencia del contador
**no es 0**.

**Si el piso no se puede evaluar, la traza NO sigue decidiendo** (delamor, 12
oct): el paso 2 **no aplica** y la duda **sube** — `ESCALATED`, con el marcador
`FLOOR_UNKNOWN` y `record["floor_missing"]` diciendo cuál de los tres casos fue.

El motivo es el mismo que `criterio_local` aplica con `tick=None` (9 oct): *"el
filtro no se arroga el silencio sobre una dimensión que no observó"*. Dejar
decidir a la traza cuando no se sabe cuántas veces ya decidió **es** el silencio
absorbente de F1: el paso 2 se vuelve absorbente justo donde no hay con qué
frenarlo. delamor: *"es exacto. la arrogancia de dictar… ESA es"*.

**Esto corrige lo que el CP1 había aprobado**, donde la traza seguía decidiendo
con `FLOOR_UNKNOWN` puesto.

## La capacidad

El paso 1 dice: *"si E cabe en los lugares libres, no hay empate que decidir"*.
Eso es **capacidad**, y sin ella la exención no se puede expresar.

- `capacity = k` → si los empatados caben en los lugares que quedan, **entran
  todos** y la decisión es `FIELD`.
- `capacity = None` → **no hay lugares que contar**, así que la exención **no
  aplica** y todo empate hay que decidirlo. Es el caso de una sola decisión
  (`criterio_local`, `should_rebuild`).

## I4 — el orden no es del campo

`Decision.value` es un **`frozenset`** de los candidatos seleccionados: si el orden
decidiera algo, sería contexto. Los candidatos tienen que ser **hashables**. El
registro sí es una lista, y su orden es **el que entró**: no se ordena por puntaje,
porque ordenar por puntaje mete un desempate alfabético por la puerta de atrás
(medido en el REPORTE CP0 del 12 oct: `w_sha` y las estimaciones por muestreo
dependen de ese orden).

## I3 — el registro guarda el valor, no la categoría

Cada candidato lleva su `field_value` y su `distance_to_cut` **exactos**. La
categoría "empate" **se deriva al leer**, comparando contra la `tolerance` que el
registro también trae. No hay un booleano `tie` por candidato.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field as _field
from typing import Any, Callable, Optional

# ── I1 — los cuatro orígenes. Toda decisión lleva el suyo, nunca implícito ────
# Constantes `str` más tupla de válidos: la convención del repo
# (`calibrate.ESTADOS`, `criterio_local.VIA_*`). El repo no usa `Enum`.
FIELD     = "FIELD"       # f  — field criterion: lo decidió el campo (paso 1)
TRACE     = "TRACE"       # T  — trace: lo decidió la selección anterior (paso 2)
ESCALATED = "ESCALATED"   # ↑k — la duda subió al orden de arriba (paso 3)
CONTEXT   = "CONTEXT"     # g  — context rule declarada por otro orden (paso 4)
ORIGINS   = (FIELD, TRACE, ESCALATED, CONTEXT)

# ── La procedencia de un umbral: quién lo produjo, y cómo ─────────────────────
MEASURED = "MEASURED"     # el orden de arriba lo MIDIÓ (p. ej. `calibrate`)
DECLARED = "DECLARED"     # el orden de arriba lo DECLARÓ (alguien, una sesión)
PROVENANCES = (MEASURED, DECLARED)

# ── El estado del paso 3 y los marcadores de lo que no se pudo evaluar ────────
NO_TRACE          = "NO_TRACE"           # SIN_TRAZA en la forma escrita
TOLERANCE_UNKNOWN = "tolerance_unknown"  # ε es None: no se sabe. Nunca 0 (I2)
FLOOR_UNKNOWN     = "floor_unknown"      # el piso no se pudo evaluar (I2)
CUT_UNKNOWN       = "cut_unknown"        # κ es None: `f` no se pudo aplicar
FIELD_VALUE_UNKNOWN = "field_value_unknown"  # `f` devolvió NaN para algún candidato

# ── Los motivos ───────────────────────────────────────────────────────────────
REASON_FIELD            = "field_decided"            # paso 1, sin empate
REASON_TIE_FITS         = "tie_fits_free_slots"      # paso 1, el empate cabe
REASON_TRACE            = "trace_conserves"          # paso 2
REASON_FLOOR_REACHED    = "floor_reached"            # paso 2 → 3 por el piso
REASON_NO_TRACE         = NO_TRACE                   # paso 3, sin traza
REASON_FIELD_NOT_APPLIED = "field_criterion_not_applied"  # paso 3, no se aplicó f
REASON_FIELD_VALUE_UNKNOWN = "field_value_unknown"   # paso 3, f no pudo medir (NaN)
REASON_TRACE_SHORT      = "trace_exceeds_free_slots"  # paso 2 → 3, la traza no alcanza
REASON_FLOOR_UNKNOWN    = "floor_not_evaluable"       # paso 2 → 3, el piso no se evalúa
REASON_CONTEXT          = "context_declared_decides"  # paso 4


@dataclass(frozen=True, kw_only=True)
class Threshold:
    """
    Un umbral con su origen: κ (**cut**), ε (**tolerance**) o P (**floor**).

    delamor, 12 oct: *"A ∪ B: el alguien que declaró es la recursividad"*. No hay
    umbral que entra y umbral que sale — es el mismo, visto desde dos órdenes.
    Todo umbral lo produce **el orden de arriba**: midiendo (`MEASURED`) o
    declarando (`DECLARED`).

    - `value` — el número. **`None` es "no se sabe"**, y se declara igual.
    - `produced_by_order` — qué orden lo produjo. Obligatorio y no vacío.
    - `provenance` — `MEASURED` o `DECLARED`. **Obligatoria siempre**: un "no se
      sabe" también se declara, y la ausencia conserva su origen (I1).
    - `source` — **por quién**, o con qué registro. Obligatorio cuando
      `value is None`: un desconocido sin dueño no es un desconocido declarado.

    `value=None` exige `provenance=DECLARED`: no se puede haber **medido** un
    desconocido.
    """

    value             : Optional[float]
    produced_by_order : str
    provenance        : Optional[str]
    source            : Optional[str] = None

    def __post_init__(self) -> None:
        if not self.produced_by_order:
            raise ValueError(
                "produced_by_order es obligatorio: un umbral sin el orden que lo "
                "produjo es un valor sin origen"
            )
        if self.provenance not in PROVENANCES:
            raise ValueError(
                f"provenance tiene que ser uno de {PROVENANCES}, llegó "
                f"{self.provenance!r}. Un 'no se sabe' TAMBIÉN se declara "
                f"(delamor, 12 oct): la ausencia conserva su origen (I1)"
            )
        if self.value is None:
            if self.provenance != DECLARED:
                raise ValueError(
                    "value=None sólo puede ser DECLARED: no se puede haber "
                    "MEASURED un desconocido"
                )
            if not self.source:
                raise ValueError(
                    "value=None exige `source`: quién declaró que no se sabe. "
                    "Un desconocido sin dueño no es un desconocido declarado"
                )

    @property
    def unknown(self) -> bool:
        """`True` si el valor no se sabe. Es lectura, no un valor del dominio."""
        return self.value is None

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "produced_by_order": self.produced_by_order,
            "provenance": self.provenance,
            "source": self.source,
        }


@dataclass(frozen=True, kw_only=True)
class RuleParams:
    """
    Los parámetros de la regla: κ, ε y P, **cada uno con su origen**.

    `tolerance` **no tiene default**: delamor, 11 oct — *"sin épsilon el engine no
    va a funcionar"*. Un empate sin ε declarada es un empate que nadie ve. Si no
    se sabe, va un `Threshold` con `value=None` y `DECLARED`, nunca 0.

    `floor=None` quiere decir **que no hay piso declarado**, y eso es distinto de
    "hay piso con valor desconocido" y de "hay piso y no sé cuántas veces decidió
    la traza" (`trace_streak=None`). Los **tres** marcan `FLOOR_UNKNOWN`, y
    `record["floor_missing"]` dice cuál fue: `floor_absent`,
    `floor_value_unknown` o `trace_streak_unknown`.
    """

    cut       : Threshold              # κ — cut, el umbral de la decisión
    tolerance : Threshold              # ε — tolerance, de la REGLA
    floor     : Optional[Threshold] = None   # P — floor, el piso del paso 2

    def __post_init__(self) -> None:
        # ε negativa **no define empate**: `|f − κ| ≤ ε` con ε < 0 es vacío
        # siempre, así que no es "una tolerancia chica", es una tolerancia que no
        # existe — y entonces el casillero estaría ocupado sin estar puesto.
        # Si no se sabe, va `value=None` DECLARED, nunca un número negativo.
        if self.tolerance.value is not None and self.tolerance.value < 0:
            raise ValueError(
                f"tolerance.value tiene que ser >= 0, llegó {self.tolerance.value!r}: "
                "una ε negativa no define empate (|f − κ| <= ε queda vacío siempre). "
                "Si no se sabe, va un Threshold con value=None y DECLARED"
            )

    @property
    def calibrated(self) -> bool:
        """
        Derivado, no un campo: `True` sólo si **todos** los umbrales presentes se
        midieron.

        El TASK listaba `calibrated` como campo. Un `bool` no puede decir **cuál**
        se midió ni **quién** lo declaró, y por eso el dato vive en cada
        `Threshold`. Esto se conserva como lectura para no perder el nombre.
        """
        presentes = [t for t in (self.cut, self.tolerance, self.floor) if t is not None]
        return all(t.provenance == MEASURED for t in presentes)

    def to_dict(self) -> dict:
        return {
            "cut": self.cut.to_dict(),
            "tolerance": self.tolerance.to_dict(),
            "floor": self.floor.to_dict() if self.floor is not None else None,
            "calibrated": self.calibrated,
        }


@dataclass(frozen=True, kw_only=True)
class ContextRule:
    """
    g — **context**: un criterio que no sale del campo, y por eso va nombrado.

    delamor, 12 oct (F2): el `g` del paso 4 es de **otro orden** — el de quien lo
    declaró — y **llega declarado antes**, como traza. El módulo **nunca inventa
    un g**: sin uno declarado, no hay paso 4.

    `select(tied, free_slots, record)` devuelve los candidatos empatados que
    entran. Recibe los empatados **como `frozenset`** (I4: si el orden decidiera,
    sería otro contexto encima de este).
    """

    select            : Callable
    declared_by       : str
    produced_by_order : str

    def __post_init__(self) -> None:
        if not callable(self.select):
            raise ValueError("select tiene que ser invocable")
        if not self.declared_by:
            raise ValueError(
                "declared_by es obligatorio: el paso 4 decide con un g NOMBRADO. "
                "Un g sin quién lo declaró es sesgo presentado como campo"
            )
        if not self.produced_by_order:
            raise ValueError("produced_by_order es obligatorio")

    def to_dict(self) -> dict:
        return {
            "declared_by": self.declared_by,
            "produced_by_order": self.produced_by_order,
        }


@dataclass(frozen=True, kw_only=True)
class Decision:
    """
    R — la decisión con su registro.

    - `value` — `frozenset` de los candidatos seleccionados (I4). **`None` quiere
      decir que NO se decidió**, y sólo es admisible con `ESCALATED`.
    - `origin` — uno de `ORIGINS` (I1).
    - `record` — el registro: `f` por candidato con su distancia al corte, los
      umbrales con su origen, los marcadores, `turn_ref`, los insumos de `f`.
    - `reason` — uno de los `REASON_*`.
    """

    value  : Optional[frozenset]
    origin : str
    record : dict
    reason : str

    def __post_init__(self) -> None:
        if self.origin not in ORIGINS:
            raise ValueError(f"origin tiene que ser uno de {ORIGINS}, llegó {self.origin!r}")
        if self.value is None and self.origin != ESCALATED:
            raise ValueError(
                f"value=None es 'no se decidió' y sólo va con {ESCALATED}; "
                f"llegó con origin={self.origin!r}. Una decisión sin valor con "
                f"origen de campo, traza o contexto afirma lo que no decidió"
            )

    @property
    def escalate_to(self) -> Optional[str]:
        """
        El ↑k **declarado por la instancia**, tal como quedó en el registro: va en
        toda decisión, no sólo en las que escalaron.

        Con `origin = ESCALATED` es **a quién subió la duda**, y `None` ahí es I5:
        no hay a quién subir y la regla **se queda**.
        """
        return self.record.get("escalate_to")

    @property
    def markers(self) -> tuple:
        return tuple(self.record.get("markers", ()))


class CkmTrustRule:
    """
    El engine de la regla CKM TRUST. **Un solo corazón.**

    Una instancia por **orden** (`order`). Los pasos 1–4 están acá y en ningún
    otro lado; cada aplicación le pasa sus elementos y no reimplementa nada.

    - `order` — el nombre del orden donde rige esta instancia.
    - `params` — κ, ε y P, cada uno con su origen.
    - `field_criterion` — **f**, uno solo: `f(candidate) → float`.
    - `context` — **g** declarado, o `None` (y entonces no hay paso 4).
    - `escalate_to` — **↑k**, el **nombre** del orden de arriba. **Nunca se
      llama** (I5 estructural).
    """

    def __init__(
        self,
        *,
        order           : str,
        params          : RuleParams,
        field_criterion : Callable,
        context         : Optional[ContextRule] = None,
        escalate_to     : Optional[str] = None,
    ) -> None:
        if not order:
            raise ValueError("order es obligatorio: la regla rige en un orden")
        if not callable(field_criterion):
            raise ValueError("field_criterion tiene que ser invocable")
        if escalate_to is not None and not isinstance(escalate_to, str):
            raise ValueError(
                "escalate_to es el NOMBRE del orden de arriba, un str, y no un "
                "invocable: si el módulo pudiera llamarlo, resolvería el paso 3, "
                "que es lo que I5 prohíbe"
            )
        self.order = order
        self.params = params
        self.field_criterion = field_criterion
        self.context = context
        self.escalate_to = escalate_to

    # ------------------------------------------------------------------
    def decide(
        self,
        candidates,
        *,
        capacity     : Optional[int] = None,
        trace        : Optional[Any] = None,
        trace_streak : Optional[int] = None,
        turn_ref     : Optional[Any] = None,
        field_inputs : Optional[dict] = None,
    ) -> Decision:
        """
        Los cuatro pasos, una vez.

        - `candidates` — C. Hashables (I4: el valor sale como `frozenset`).
        - `capacity` — los lugares libres. `None` = no hay lugares que contar, así
          que la exención del paso 1 **no** aplica.
        - `trace` — T, la selección anterior. Un contenedor con `in`.
        - `trace_streak` — cuántas veces decidió la traza sin que el campo
          decidiera. `None` = no se sabe → `FLOOR_UNKNOWN`, **no 0**, y la traza
          **no decide**: la duda sube (delamor, 12 oct).
        - `turn_ref` — la vuelta de la hélice. Se guarda sin interpretarse.
        - `field_inputs` — los insumos de `f`, para el registro.

        Cuatro salidas que **no** son el paso 1: κ desconocida y `f` que
        devuelve NaN suben la duda antes de empezar (paso 0); y en el paso 2 la
        traza puede **no alcanzar** —si lo que conserva no entra en los lugares
        libres, elegir cuáles entran sería otro desempate, y ése no es de la
        traza— o **no poder decidir**, cuando el piso no se puede evaluar.
        """
        cands = list(candidates)
        cut = self.params.cut
        tol = self.params.tolerance
        markers: list = []
        if tol.unknown:
            markers.append(TOLERANCE_UNKNOWN)
        if cut.unknown:
            markers.append(CUT_UNKNOWN)

        base_record = {
            "order": self.order,
            "params": self.params.to_dict(),
            "capacity": capacity,
            "trace_present": trace is not None,
            "trace_streak": trace_streak,
            # La hélice: la referencia de la vuelta, guardada sin interpretar
            "turn_ref": turn_ref,
            "field_inputs": field_inputs,
            "escalate_to": self.escalate_to,
            "context": self.context.to_dict() if self.context is not None else None,
            "markers": markers,
        }

        # ── κ desconocida: `f` no se puede aplicar ────────────────────────────
        # No es el paso 1 fallando: es el paso 3 por la rama "¿se aplicó f? no".
        # Mecánicamente, I5: se queda y sube la duda. No se inventa un corte.
        if cut.unknown:
            base_record["candidates"] = [
                {"candidate": c, "field_value": None, "distance_to_cut": None}
                for c in cands
            ]
            return Decision(value=None, origin=ESCALATED, record=base_record,
                            reason=REASON_FIELD_NOT_APPLIED)

        # ── Paso 1 — f decide, con su registro ───────────────────────────────
        # I3: se guardan el valor y la distancia EXACTOS. "Empate" se deriva al
        # leer, contra la `tolerance` que el registro también trae.
        valores = {c: float(self.field_criterion(c)) for c in cands}
        # `f` no pudo medir: NaN no es "afuera". El candidato NO se descarta — va
        # al registro con `None` declarado y nombrado, y la decisión no puede ser
        # FIELD sobre un conjunto que lo perdió.
        sin_medir = [c for c in cands if math.isnan(valores[c])]
        if sin_medir:
            markers.append(FIELD_VALUE_UNKNOWN)
            base_record["field_value_unknown"] = list(sin_medir)
            base_record["candidates"] = [
                {"candidate": c,
                 "field_value": None if math.isnan(valores[c]) else valores[c],
                 "distance_to_cut": (None if math.isnan(valores[c])
                                     else valores[c] - float(cut.value))}
                for c in cands
            ]
            return Decision(value=None, origin=ESCALATED, record=base_record,
                            reason=REASON_FIELD_VALUE_UNKNOWN)

        dist = {c: valores[c] - float(cut.value) for c in cands}
        base_record["candidates"] = [
            {"candidate": c, "field_value": valores[c], "distance_to_cut": dist[c]}
            for c in cands
        ]

        if tol.unknown:
            # Lo único derivable sin inventar un número: la igualdad exacta es
            # empate bajo CUALQUIER ε ≥ 0. Lo de al lado del corte no se sabe, y
            # por eso la decisión viaja marcada.
            above = [c for c in cands if dist[c] > 0.0]
            below = [c for c in cands if dist[c] < 0.0]
            tied  = [c for c in cands if dist[c] == 0.0]
        else:
            e = float(tol.value)
            above = [c for c in cands if dist[c] > e]
            below = [c for c in cands if dist[c] < -e]
            tied  = [c for c in cands if abs(dist[c]) <= e]
        base_record["n_above"] = len(above)
        base_record["n_below"] = len(below)
        base_record["n_tied"] = len(tied)

        if not tied:
            return Decision(value=frozenset(above), origin=FIELD,
                            record=base_record, reason=REASON_FIELD)

        # "Si E cabe en los lugares libres, no hay empate que decidir."
        # Sin capacidad no hay lugares que contar: la exención no aplica.
        free = None
        if capacity is not None:
            free = capacity - len(above)
            base_record["free_slots"] = free
            if len(tied) <= free:
                return Decision(value=frozenset(above) | frozenset(tied),
                                origin=FIELD, record=base_record,
                                reason=REASON_TIE_FITS)

        # ── Paso 2 — la traza conserva, salvo que el piso se haya cumplido ────
        # El piso se evalúa **sólo si hay traza**: sin T el paso 2 no aplica, y
        # marcar FLOOR_UNKNOWN ahí sería ruido sobre algo que no se iba a usar.
        floor_reached = False
        floor_unknown = False
        trace_short = False
        if trace is not None:
            floor = self.params.floor
            if floor is None:
                floor_unknown, falta = True, "floor_absent"
            elif floor.unknown:
                floor_unknown, falta = True, "floor_value_unknown"
            elif trace_streak is None:
                floor_unknown, falta = True, "trace_streak_unknown"
            else:
                floor_reached = trace_streak >= float(floor.value)
            if floor_unknown:
                # La traza NO sigue decidiendo (delamor, 12 oct): sin saber
                # cuántas veces ya decidió, dejarla decidir es arrogarse el
                # silencio sobre lo que no se observó — el mismo criterio que
                # `criterio_local` con `tick=None` (9 oct).
                markers.append(FLOOR_UNKNOWN)
                base_record["floor_missing"] = falta
            base_record["floor_reached"] = floor_reached

            if not floor_unknown and not floor_reached:
                conserva = [c for c in tied if c in trace]
                base_record["trace_conserves"] = len(conserva)
                # La traza puede no alcanzar: si lo que conserva no entra en los
                # lugares libres, el paso 2 **no decide** —elegir cuáles de los
                # conservados entran sería otro desempate, y no es de la traza—.
                if free is not None and len(conserva) > free:
                    trace_short = True
                else:
                    return Decision(value=frozenset(above) | frozenset(conserva),
                                    origin=TRACE, record=base_record,
                                    reason=REASON_TRACE)

        # ── Paso 3 — NO_TRACE: la duda sube. No resuelve (I5) ────────────────
        # Con ↑k puesto, el paso 4 NO corre: el orden de arriba todavía no habló.
        # "↑k no decide" se expresa volviendo a llamar sin `escalate_to`.
        if floor_unknown:
            reason3 = REASON_FLOOR_UNKNOWN
        elif trace_short:
            reason3 = REASON_TRACE_SHORT
        elif floor_reached:
            reason3 = REASON_FLOOR_REACHED
        else:
            reason3 = REASON_NO_TRACE
        if self.escalate_to is not None:
            return Decision(value=None, origin=ESCALATED, record=base_record,
                            reason=reason3)

        # ── Paso 4 — sólo con un g que llegó declarado de otro orden ─────────
        if self.context is None:
            # Sin g declarado no hay paso 4. Se queda: TRY TO STAY THERE.
            return Decision(value=None, origin=ESCALATED, record=base_record,
                            reason=reason3)

        free = (capacity - len(above)) if capacity is not None else None
        elegidos = self.context.select(frozenset(tied), free, dict(base_record))
        elegidos = frozenset(elegidos)
        sobrantes = elegidos - frozenset(tied)
        if sobrantes:
            raise ValueError(
                f"el g declarado por {self.context.declared_by!r} devolvió "
                f"candidatos que no estaban empatados: {sorted(map(str, sobrantes))}"
            )
        base_record["context_applied"] = True
        return Decision(value=frozenset(above) | elegidos, origin=CONTEXT,
                        record=base_record, reason=REASON_CONTEXT)
