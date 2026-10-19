"""
`LocalCriterion` expresado como **instancia** de `CkmTrustRule` — CP2

`TASK_ckm_trust_rule_v1`, CP2. **`iap_chatroom/local_criterion.py` NO se toca**: se
lo expresa en la forma, acá, y se compara contra sus propios registros.

*(Vale en su marco: el CP3 —13 oct— sí lo tocó, y ahí `local_criterion` pasó a
instanciar el engine. Este archivo queda como lo que midió el CP2, el mapeo
escrito **afuera**. El replay del mismo log **por `local_criterion` mismo** está en
`tests/test_local_criterion_cp3.py`.)*

Entrada: `experiments/vivo_03_criterio_local_log.json` — el vivo 03, **24
registros** de 2 devices, `piso_vueltas = 6`, `calibrado: false`.

## El mapeo (CP0 del CP2, `c620d70`, aceptado por delamor)

| casillero | qué es en `local_criterion` |
|---|---|
| **C** | la vuelta. **Un** candidato: `"llamar"` |
| **f** | `n_nuevos + nombrado` — `local_criterion.py:271-274` |
| **κ** | **0**, `DECLARED` **por el mapeo**, no por `local_criterion`: sale de leer `if n_nuevos > 0` |
| **ε** | `None` **declarado**: `local_criterion` no tiene ε |
| **T** | **el silencio**, `frozenset()`. En la primera vuelta **no hay traza**: `None` |
| **P** | `piso_vueltas`, leído del registro; `trace_streak` = `deltas.vueltas_sin_llamar` |
| **g** | **no hay** `g` declarado. La auditoría **no es un `g`** (ver abajo) |
| **↑k** | **el LLM**. `ESCALATED` → **llamar** es literal: llamar al modelo **es** escalar |

**`capacity = None`**, no 1. Con `capacity = 1` el empate exacto de `sin_cambio`
tendría un lugar libre, caería en la exención del paso 1 y daría **llamar**:
invertiría 17 de 24. Hay un test que lo mide.

**`field_inputs` lleva `n_nuevos` y `nombrado` POR SEPARADO**, aunque `f` sea la
suma: así `R` conserva **cuál** de los dos disparó, que es lo que la suma pierde.

**La auditoría no entra en la forma.** No resuelve un empate: **mide la regla**.
Se aplica como **overlay leído del registro** (`via == "auditoria"`), **sin
re-sortear**: re-sortear haría que el test midiera el RNG y no el mapeo.

**`tick=None` quedó alineado** por la decisión 5 del 12 oct (el piso no evaluable
sube la duda, igual que `local_criterion` con `tick=None`), y **no es medible en
`vivo_03`**: 0 de 24.

## La predicción, escrita en `c620d70` ANTES de correr

17 `sin_cambio` → `TRACE` · 2 `primera_vuelta` → **`FIELD`** (f = 3 > κ, no
`ESCALATED`) · 2 `mensajes_nuevos` → `FIELD` · 2 `piso` → `ESCALATED` por
`floor_reached` · 1 `auditoria` → la regla dice **skip** y el overlay lo da vuelta.
**24/24 en `llamar`/`no llamar`.** Las diferencias quedan en el **origen y el
motivo**, no en la decisión.
"""

import json
from pathlib import Path

import pytest

from services.ckm_trust_rule import (
    DECLARED, ESCALATED, FIELD, FLOOR_UNKNOWN, REASON_FLOOR_REACHED,
    REASON_TIE_FITS, TRACE, CkmTrustRule, RuleParams, Threshold,
)

LOG = Path(__file__).resolve().parent.parent / "experiments" / "vivo_03_criterio_local_log.json"
CANDIDATO = "llamar"
ORDEN = "b0 — la vuelta del device"


@pytest.fixture(scope="module")
def registros() -> list:
    """Los 24 registros, en orden, con el índice de su device."""
    d = json.loads(LOG.read_text())
    return [(i, r) for i, dev in enumerate(d["por_device"])
            for r in dev["registros_criterio"]]


def _regla_de(reg: dict, *, capacity_override=None) -> CkmTrustRule:
    """La instancia, armada con los umbrales **del propio registro**."""
    umb = reg["umbrales"]
    return CkmTrustRule(
        order=ORDEN,
        params=RuleParams(
            # κ = 0: lo declara el MAPEO, no local_criterion
            cut=Threshold(value=0.0, produced_by_order="el mapeo del CP2",
                          provenance=DECLARED,
                          source="sale de leer `if n_nuevos > 0` en local_criterion.py:273"),
            # ε: local_criterion no tiene. None declarado, nunca 0 implícito
            tolerance=Threshold(value=None, produced_by_order="el mapeo del CP2",
                                provenance=DECLARED,
                                source="local_criterion no declara ε (TASK, 11 oct)"),
            floor=Threshold(value=umb["piso_vueltas"], produced_by_order="b1",
                            provenance=DECLARED,
                            source="declarado en el log del vivo 03, calibrado: false"),
        ),
        field_criterion=lambda c: (reg["deltas"]["n_nuevos"]
                                   + int(bool(reg["deltas"]["nombrado"]))),
        context=None,          # local_criterion no declara un g para el empate
        escalate_to="b1 — el LLM",
    )


def _decidir(reg: dict, *, capacity=None):
    """Una vuelta, en la forma. Devuelve la `Decision`."""
    d = reg["deltas"]
    primera = reg["motivo"] == "primera_vuelta"
    return _regla_de(reg).decide(
        [CANDIDATO],
        capacity=capacity,
        # T: el silencio. En la primera vuelta NO hay traza.
        trace=None if primera else frozenset(),
        trace_streak=d["vueltas_sin_llamar"],
        turn_ref={"tick": reg["tick"], "vuelta": reg["vuelta"]},
        # f es la suma; field_inputs conserva CUÁL disparó
        field_inputs={"n_nuevos": d["n_nuevos"], "nombrado": d["nombrado"]},
    )


def _llamar(dec, reg: dict) -> bool:
    """`ESCALATED` → llamar: llamar al modelo **es** escalar. Y la auditoría se
    aplica **como overlay del registro**, sin re-sortear."""
    de_la_regla = (dec.value is None) or (CANDIDATO in dec.value)
    if reg["via"] == "auditoria":
        return True                      # overlay, no es de la regla
    return de_la_regla


# ── El resultado: bit a bit ──────────────────────────────────────────────────

def test_24_de_24_bit_a_bit_en_llamar(registros) -> None:
    """**El resultado del CP2.** Mismas entradas, misma decisión `llamar`/`no
    llamar` que `local_criterion`, registro por registro."""
    difs = []
    for dev, reg in registros:
        dec = _decidir(reg)
        if _llamar(dec, reg) != reg["llamar"]:
            difs.append((dev, reg["vuelta"], reg["motivo"], reg["llamar"],
                         dec.origin, dec.reason))
    assert len(registros) == 24
    assert not difs, f"diferencias en llamar/no llamar: {difs}"


def test_sin_el_overlay_la_UNICA_diferencia_es_la_auditoria(registros) -> None:
    """La auditoría **no es de la regla**: no resuelve un empate, mide la regla.
    Sin el overlay queda **una** diferencia, y es exactamente ésa."""
    difs = [(dev, reg["vuelta"], reg["motivo"])
            for dev, reg in registros
            if ((_decidir(reg).value is None)
                or (CANDIDATO in _decidir(reg).value)) != reg["llamar"]]
    assert len(difs) == 1
    assert difs[0][2] == "auditoria"


# ── El origen y el motivo, por motivo ───────────────────────────────────────

def test_el_origen_por_motivo_es_el_predicho(registros) -> None:
    """
    La predicción escrita en `c620d70` antes de correr. Donde `local_criterion` y la
    forma difieren es acá —en el **origen**—, no en la decisión.
    """
    por_motivo: dict = {}
    for _, reg in registros:
        dec = _decidir(reg)
        por_motivo.setdefault(reg["motivo"], set()).add((dec.origin, dec.reason))

    assert por_motivo["sin_cambio"] == {(TRACE, "trace_conserves")}
    assert por_motivo["mensajes_nuevos"] == {(FIELD, "field_decided")}
    assert por_motivo["piso"] == {(ESCALATED, REASON_FLOOR_REACHED)}
    assert por_motivo["auditoria"] == {(TRACE, "trace_conserves")}
    # la diferencia declarada en el CP0: primera_vuelta cae por FIELD, no por
    # ESCALATED, porque f = 3 > κ y el paso 2 ni se alcanza
    assert por_motivo["primera_vuelta"] == {(FIELD, "field_decided")}


def test_primera_vuelta_cae_por_FIELD_y_no_por_falta_de_traza(registros) -> None:
    """La diferencia que el mapeo propuesto no tenía. El módulo **no tiene el
    concepto "primera vuelta"**: lo que `local_criterion` codifica como *"nunca
    llamé"* es *"no hay traza"*, y con señal de campo la ausencia de traza es
    irrelevante."""
    primeras = [(dev, reg) for dev, reg in registros
                if reg["motivo"] == "primera_vuelta"]
    assert len(primeras) == 2
    for _, reg in primeras:
        assert reg["deltas"]["n_nuevos"] + int(reg["deltas"]["nombrado"]) == 3
        dec = _decidir(reg)
        assert dec.origin == FIELD, "con f > κ el paso 2 ni se alcanza"
        assert reg["via"] == "criterio"      # local_criterion también lo llama campo


# ── `field_inputs`: R conserva lo que la suma pierde ────────────────────────

def test_field_inputs_conserva_cual_de_los_dos_disparo(registros) -> None:
    """`f` es la suma, así que pierde si disparó `nombrado` o `n_nuevos`.
    `field_inputs` lo conserva por separado, en el registro de cada decisión."""
    for _, reg in registros:
        fi = _decidir(reg).record["field_inputs"]
        assert fi == {"n_nuevos": reg["deltas"]["n_nuevos"],
                      "nombrado": reg["deltas"]["nombrado"]}
    # y el caso donde la suma sí pierde información: nombrado=True
    con_nombrado = [r for _, r in registros if r["deltas"]["nombrado"]]
    assert len(con_nombrado) == 2
    assert all(r["motivo"] == "primera_vuelta" for r in con_nombrado), (
        "motivo=nombrado nunca aparece: los dos con nombrado=True son "
        "primera_vuelta, que va antes en el orden de local_criterion"
    )


def test_la_helice_queda_en_cada_registro(registros) -> None:
    """Decisión 4: la referencia de la vuelta se guarda **sin interpretarse**."""
    for _, reg in registros:
        assert _decidir(reg).record["turn_ref"] == {"tick": reg["tick"],
                                                    "vuelta": reg["vuelta"]}


# ── La decisión 5 no mueve ninguna fila, y se verifica ──────────────────────

def test_la_decision_5_no_mueve_ninguna_fila_en_vivo_03(registros) -> None:
    """
    La predicción se escribió **antes** de la decisión 5 (el piso no evaluable sube
    la duda), así que corresponde chequear si sigue en pie.

    Sigue: el piso es **siempre evaluable** acá —`piso_vueltas` declarado y
    `vueltas_sin_llamar` presente en los 24—, así que ninguna fila cae en
    `floor_missing`. **Un `FLOOR_UNKNOWN` acá sería divergencia, no ajuste.**
    """
    for _, reg in registros:
        dec = _decidir(reg)
        assert FLOOR_UNKNOWN not in dec.markers
        assert "floor_missing" not in dec.record
        assert reg["deltas"]["vueltas_sin_llamar"] is not None


# ── Las tres cosas que este corpus NO puede medir ───────────────────────────

def test_lo_que_vivo_03_no_puede_medir(registros) -> None:
    """
    Del CP0, y va al reporte para que el 24/24 no parezca confirmar lo que no
    midió:

    1. **`tick=None`: 0 de 24.** La diferencia quedó alineada por la decisión 5 y
       el log no tiene con qué medirla.
    2. **Ninguna colisión piso-vs-campo:** los dos `piso` tienen `f = 0`, así que
       la diferencia de orden —`local_criterion` evalúa `tick`, `primera_vuelta` y
       el piso **antes** que el campo— no produce divergencia acá.
    3. **`motivo = nombrado`: 0 de 24.**
    """
    assert sum(1 for _, r in registros if r["tick"] is None) == 0
    colisiones = [r for _, r in registros
                  if r["deltas"]["vueltas_sin_llamar"] >= r["umbrales"]["piso_vueltas"]
                  and (r["deltas"]["n_nuevos"] + int(r["deltas"]["nombrado"])) > 0]
    assert colisiones == []
    assert sum(1 for _, r in registros if r["motivo"] == "nombrado") == 0


# ── El contrafáctico que el CP0 encontró ────────────────────────────────────

def test_CP4_con_capacity_1_ya_NO_se_invierte_ninguna(registros) -> None:
    """
    **El contrafáctico del CP0 desapareció con el CP4.**

    El CP0 había encontrado que con `capacity=1` el empate exacto caía en la
    exención del paso 1 y daba **llamar**: **17 de 24** se daban vuelta, y por eso
    el mapeo fijó `capacity=None`.

    **Sacada la exención** (13 oct, orden de delamor), con `capacity=1` el empate
    va al **paso 2**: hay traza, el piso es evaluable y no está cumplido, lo que la
    traza conserva es **nada**, y `0 ≤ 1` lugares libres → `TRACE` con valor vacío →
    **no llamar**. **0 inversiones.**

    Dice algo que vale dejar escrito: **`capacity=1` ya no es peligroso acá.** La
    razón por la que el mapeo eligió `capacity=None` era la exención, y la exención
    no está. `capacity=None` sigue siendo lo correcto por otro motivo —*"no hay
    lugares que contar"* en una decisión única—, no por este contrafáctico.
    """
    invertidos = []
    for dev, reg in registros:
        dec = _decidir(reg, capacity=1)
        llamar = (dec.value is None) or (CANDIDATO in dec.value)
        if llamar != reg["llamar"] and reg["via"] != "auditoria":
            invertidos.append((reg["motivo"], dec.origin, dec.reason))
    assert invertidos == []
    # y la decisión con capacity=1 coincide con la de capacity=None, las 24
    for dev, reg in registros:
        assert ((_decidir(reg, capacity=1).value is None)
                == (_decidir(reg).value is None))
