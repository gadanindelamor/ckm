"""
tests de `services/ckm_trust_rule.py` — la regla CKM TRUST como un solo corazón

`TASK_ckm_trust_rule_v1`, CP1. Cubre lo que el TASK pide —los cuatro orígenes, el
empate con ε, el piso que lleva del paso 2 al 3, `None` declarado, el paso 3 sin
`escalate_to`— y las tensiones T1–T12 del REPORTE CP0 del 12 oct, más las dos
correcciones de delamor: `provenance` obligatoria siempre y `source` en el
`Threshold` (`record` queda sólo para `Decision.record`).

Cada test dice **qué decisión del 12 oct o qué invariante** verifica.
"""

from pathlib import Path

import pytest

from services.ckm_trust_rule import (
    CONTEXT, CUT_UNKNOWN, DECLARED, ESCALATED, FIELD, FLOOR_UNKNOWN, MEASURED,
    NO_TRACE, ORIGINS, REASON_CONTEXT, REASON_FIELD, REASON_FIELD_NOT_APPLIED,
    REASON_FLOOR_REACHED, REASON_TIE_FITS, REASON_TRACE, TOLERANCE_UNKNOWN,
    TRACE, CkmTrustRule, ContextRule, Decision, RuleParams, Threshold,
)

PUNTAJES = {"a": 0.90, "b": 0.50, "c": 0.50, "d": 0.10}
F = lambda c: PUNTAJES[c]          # noqa: E731 — f, el criterio de campo


def _th(value, *, provenance=MEASURED, order="k3", source="calibrate"):
    return Threshold(value=value, produced_by_order=order,
                     provenance=provenance, source=source)


def _eps_desconocida():
    """ε declarada como 'no se sabe' — delamor, 11 oct: nunca 0."""
    return Threshold(value=None, produced_by_order="k3", provenance=DECLARED,
                     source="delamor, 11 oct: 'si no se conoce, tal cual: se declara'")


def _regla(*, cut=0.50, tolerance=0.0, floor=None, context=None, escalate_to=None):
    return CkmTrustRule(
        order="k2",
        params=RuleParams(
            cut=_th(cut),
            tolerance=_th(tolerance) if not isinstance(tolerance, Threshold) else tolerance,
            floor=_th(floor, order="k3", source="piso declarado") if isinstance(floor, (int, float)) else floor,
        ),
        field_criterion=F,
        context=context,
        escalate_to=escalate_to,
    )


# ── Los cuatro orígenes ───────────────────────────────────────────────────────

def test_origen_FIELD_sin_empate() -> None:
    """Paso 1: sin empate decide `f`, y el origen es FIELD (I1)."""
    d = _regla(cut=0.30, tolerance=0.05).decide(["a", "b", "c", "d"], capacity=3)
    assert d.origin == FIELD and d.reason == REASON_FIELD
    assert d.value == frozenset({"a", "b", "c"})


def test_origen_TRACE_el_empate_lo_decide_la_traza() -> None:
    """Paso 2: `b` y `c` empatan en el corte; la traza conserva a `b`."""
    d = _regla(cut=0.50, tolerance=0.01, floor=3).decide(
        ["a", "b", "c"], capacity=2, trace={"b"}, trace_streak=0)
    assert d.origin == TRACE and d.reason == REASON_TRACE
    assert d.value == frozenset({"a", "b"})


def test_origen_ESCALATED_sin_traza() -> None:
    """Paso 3: hay empate que decidir y no hay traza → la duda sube."""
    d = _regla(cut=0.50, tolerance=0.01, escalate_to="k3").decide(
        ["a", "b", "c"], capacity=2)
    assert d.origin == ESCALATED and d.reason == NO_TRACE
    assert d.value is None and d.escalate_to == "k3"


def test_origen_CONTEXT_con_g_declarado_y_sin_escalate_to() -> None:
    """Paso 4: sin ↑k y con un `g` declarado por otro orden, decide `g`."""
    g = ContextRule(select=lambda tied, free, rec: {sorted(tied)[0]},
                    declared_by="delamor", produced_by_order="k3")
    d = _regla(cut=0.50, tolerance=0.01, context=g).decide(
        ["a", "b", "c"], capacity=2)
    assert d.origin == CONTEXT and d.reason == REASON_CONTEXT
    assert d.value == frozenset({"a", "b"})
    assert d.record["context"]["declared_by"] == "delamor"


def test_los_cuatro_origenes_son_los_cuatro() -> None:
    assert ORIGINS == (FIELD, TRACE, ESCALATED, CONTEXT)


# ── El empate con ε ───────────────────────────────────────────────────────────

def test_epsilon_define_el_empate() -> None:
    """ε es de la REGLA: con ε chica `b` y `c` no empatan con el corte; con ε
    grande, sí. Mismo campo, misma κ, dos empates distintos."""
    chica = _regla(cut=0.45, tolerance=0.01).decide(["a", "b", "c", "d"], capacity=3)
    assert chica.record["n_tied"] == 0 and chica.origin == FIELD
    grande = _regla(cut=0.45, tolerance=0.10).decide(["a", "b", "c", "d"], capacity=3)
    assert grande.record["n_tied"] == 2


def test_tolerance_es_obligatoria_y_sin_default() -> None:
    """delamor, 11 oct: *"sin épsilon el engine no va a funcionar"*. `RuleParams`
    sin `tolerance` no se puede construir."""
    with pytest.raises(TypeError):
        RuleParams(cut=_th(0.5))            # type: ignore[call-arg]


def test_epsilon_None_marca_tolerance_unknown_y_NO_decide_como_cero() -> None:
    """
    T3. Con ε `None`, **toda** decisión viaja marcada: no se puede saber si lo de
    al lado del corte era empate. Con ε = 0 **no** se marca. Las dos cosas en el
    mismo test, porque la diferencia es el punto.
    """
    d_none = _regla(cut=0.45, tolerance=_eps_desconocida()).decide(["a", "b"], capacity=2)
    assert TOLERANCE_UNKNOWN in d_none.markers

    d_cero = _regla(cut=0.45, tolerance=0.0).decide(["a", "b"], capacity=2)
    assert TOLERANCE_UNKNOWN not in d_cero.markers


def test_con_epsilon_desconocida_la_igualdad_exacta_ES_empate() -> None:
    """
    T3, lo único derivable sin inventar un número: `|f − κ| = 0` es empate bajo
    **cualquier** ε ≥ 0, así que la igualdad exacta es empate aunque ε no se sepa.

    Precedente del repo: `landscape_engine.py:74` (`h = 0` conserva `s_i`), que el
    REPORTE CP0 clasificó como paso 2 con ε = 0 implícito.
    """
    d = _regla(cut=0.50, tolerance=_eps_desconocida(), floor=3).decide(
        ["a", "b", "c"], capacity=2, trace={"c"}, trace_streak=0)
    assert d.record["n_tied"] == 2            # b y c valen exactamente 0.50
    assert d.origin == TRACE and d.value == frozenset({"a", "c"})
    assert TOLERANCE_UNKNOWN in d.markers


# ── El piso que lleva del paso 2 al 3 ────────────────────────────────────────

def test_el_piso_lleva_del_paso_2_al_3() -> None:
    """P: con la traza decidiendo `floor` veces sin que el campo decida, la duda
    sube. Sin el piso, el silencio es absorbente (F1 del CP0b)."""
    r = _regla(cut=0.50, tolerance=0.01, floor=3, escalate_to="k3")
    antes = r.decide(["a", "b", "c"], capacity=2, trace={"b"}, trace_streak=2)
    assert antes.origin == TRACE

    cumplido = r.decide(["a", "b", "c"], capacity=2, trace={"b"}, trace_streak=3)
    assert cumplido.origin == ESCALATED
    assert cumplido.reason == REASON_FLOOR_REACHED
    assert cumplido.record["floor_reached"] is True


def test_trace_streak_None_marca_floor_unknown_y_no_es_cero() -> None:
    """T4 (I2). El módulo es puro: el contador lo pasa quien llama. Sin contador,
    el piso **no se puede evaluar** y la decisión lo declara — no se asume 0."""
    d = _regla(cut=0.50, tolerance=0.01, floor=3).decide(
        ["a", "b", "c"], capacity=2, trace={"b"}, trace_streak=None)
    assert d.origin == TRACE
    assert FLOOR_UNKNOWN in d.markers
    assert d.record["floor_missing"] == "trace_streak_unknown"


def test_sin_piso_declarado_el_silencio_absorbe_y_queda_declarado() -> None:
    """F1: sin P, la traza gana siempre. El módulo **no lo arregla** —no es de este
    CP— pero lo **declara**: `floor_absent`."""
    d = _regla(cut=0.50, tolerance=0.01, floor=None).decide(
        ["a", "b", "c"], capacity=2, trace={"b"}, trace_streak=999)
    assert d.origin == TRACE
    assert FLOOR_UNKNOWN in d.markers
    assert d.record["floor_missing"] == "floor_absent"


def test_sin_traza_el_piso_no_se_evalua_ni_se_marca() -> None:
    """Sin T el paso 2 no aplica, así que marcar el piso sería ruido sobre algo
    que no se iba a usar."""
    d = _regla(cut=0.50, tolerance=0.01, floor=None, escalate_to="k3").decide(
        ["a", "b", "c"], capacity=2)
    assert d.origin == ESCALATED and FLOOR_UNKNOWN not in d.markers


# ── `None` declarado — las dos correcciones de delamor ───────────────────────

def test_threshold_value_None_sin_provenance_levanta() -> None:
    """**Corrección 1 de delamor, 12 oct:** un "no se sabe" **también se declara**.
    `provenance` es obligatoria siempre; la ausencia conserva su origen (I1)."""
    with pytest.raises(ValueError, match="provenance"):
        Threshold(value=None, produced_by_order="k3", provenance=None,
                  source="delamor")


def test_threshold_value_None_no_puede_ser_MEASURED() -> None:
    """No se puede haber **medido** un desconocido."""
    with pytest.raises(ValueError, match="DECLARED"):
        Threshold(value=None, produced_by_order="k3", provenance=MEASURED,
                  source="calibrate")


def test_threshold_value_None_exige_source() -> None:
    """Un desconocido **sin dueño** no es un desconocido declarado."""
    with pytest.raises(ValueError, match="source"):
        Threshold(value=None, produced_by_order="k3", provenance=DECLARED)


def test_threshold_exige_el_orden_que_lo_produjo() -> None:
    """κ y ε con origen (delamor, 12 oct): todo umbral lo produce el orden de
    arriba, midiendo o declarando."""
    with pytest.raises(ValueError, match="produced_by_order"):
        Threshold(value=0.4, produced_by_order="", provenance=DECLARED,
                  source="alguien")


def test_calibrated_es_derivado_y_mira_todos_los_umbrales() -> None:
    """T1: un `bool` no puede decir **cuál** se midió ni **quién** lo declaró, y
    por eso el dato vive en cada `Threshold`. `calibrated` se conserva como
    lectura, y es `True` sólo si **todos** los presentes se midieron."""
    todos = RuleParams(cut=_th(0.4), tolerance=_th(0.01), floor=_th(3))
    assert todos.calibrated is True
    uno_declarado = RuleParams(cut=_th(0.4), tolerance=_eps_desconocida())
    assert uno_declarado.calibrated is False


def test_kappa_desconocida_no_se_inventa_un_corte() -> None:
    """κ `None`: `f` no se puede aplicar. Es la rama *"¿se aplicó f? no"* del paso
    3, no un paso 1 que falla."""
    cut_none = Threshold(value=None, produced_by_order="k3", provenance=DECLARED,
                         source="nadie lo calibró")
    r = CkmTrustRule(order="k2",
                     params=RuleParams(cut=cut_none, tolerance=_th(0.01)),
                     field_criterion=F)
    d = r.decide(["a", "b"], capacity=1)
    assert d.origin == ESCALATED and d.reason == REASON_FIELD_NOT_APPLIED
    assert CUT_UNKNOWN in d.markers and d.value is None


# ── El paso 3 sin `escalate_to`, e I5 estructural ───────────────────────────

def test_paso_3_sin_escalate_to_se_queda_y_no_resuelve() -> None:
    """
    **F2 / I5 (delamor, 12 oct):** en el orden k rige quedarse, no resolver — el
    equivalente mecánico de *TRY TO STAY THERE*. Sin a quién subir, devuelve
    `ESCALATED` con `escalate_to=None` y la duda queda registrada.
    """
    d = _regla(cut=0.50, tolerance=0.01).decide(["a", "b", "c"], capacity=2)
    assert d.origin == ESCALATED and d.reason == NO_TRACE
    assert d.escalate_to is None and d.value is None


def test_escalate_to_invocable_levanta_I5_es_estructural() -> None:
    """T5. Si el módulo pudiera llamar a ↑k, **resolvería** el paso 3. `escalate_to`
    es un **nombre**: así I5 no es una convención de uso, no hay cómo violarla."""
    with pytest.raises(ValueError, match="I5"):
        CkmTrustRule(order="k2",
                     params=RuleParams(cut=_th(0.5), tolerance=_th(0.01)),
                     field_criterion=F,
                     escalate_to=lambda *a: "decidido")   # type: ignore[arg-type]


def test_sin_g_declarado_NO_hay_paso_4() -> None:
    """Decisión 1: el módulo **nunca inventa un g**. Sin `context`, queda
    `ESCALATED` — no se cae al paso 4 solo (I5)."""
    d = _regla(cut=0.50, tolerance=0.01, context=None).decide(
        ["a", "b", "c"], capacity=2)
    assert d.origin == ESCALATED and d.record["context"] is None


def test_con_escalate_to_el_paso_4_NO_corre_aunque_haya_g() -> None:
    """Mientras el orden de arriba no haya hablado, la duda está arriba y no en el
    `g`. *"↑k no decide"* se expresa volviendo a llamar **sin** `escalate_to`."""
    g = ContextRule(select=lambda tied, free, rec: {sorted(tied)[0]},
                    declared_by="delamor", produced_by_order="k3")
    con_arriba = _regla(cut=0.50, tolerance=0.01, context=g, escalate_to="k3")
    d1 = con_arriba.decide(["a", "b", "c"], capacity=2)
    assert d1.origin == ESCALATED and "context_applied" not in d1.record

    sin_arriba = _regla(cut=0.50, tolerance=0.01, context=g)
    d2 = sin_arriba.decide(["a", "b", "c"], capacity=2)
    assert d2.origin == CONTEXT and d2.record["context_applied"] is True


def test_el_g_va_nombrado() -> None:
    """*"Decide g, **nombrado**"*: un `g` sin quién lo declaró es sesgo presentado
    como campo."""
    with pytest.raises(ValueError, match="declared_by"):
        ContextRule(select=lambda *a: set(), declared_by="",
                    produced_by_order="k3")


def test_el_g_no_puede_elegir_fuera_del_empate() -> None:
    g = ContextRule(select=lambda tied, free, rec: {"d"},
                    declared_by="delamor", produced_by_order="k3")
    with pytest.raises(ValueError, match="no estaban empatados"):
        _regla(cut=0.50, tolerance=0.01, context=g).decide(
            ["a", "b", "c"], capacity=2)


# ── La capacidad (T12) ───────────────────────────────────────────────────────

def test_el_empate_que_cabe_en_los_lugares_libres_no_es_empate() -> None:
    """Paso 1: *"si E cabe en los lugares libres, no hay empate que decidir"*."""
    d = _regla(cut=0.50, tolerance=0.01).decide(["a", "b", "c"], capacity=3)
    assert d.origin == FIELD and d.reason == REASON_TIE_FITS
    assert d.value == frozenset({"a", "b", "c"})
    assert d.record["free_slots"] == 2


def test_capacity_None_no_exime_el_empate() -> None:
    """T12: `None` es **no hay lugares que contar**, no "caben todos". Es el caso
    de una sola decisión (`criterio_local`, `should_rebuild`)."""
    d = _regla(cut=0.50, tolerance=0.01, escalate_to="k3").decide(
        ["a", "b", "c"], capacity=None)
    assert d.origin == ESCALATED and "free_slots" not in d.record


# ── La hélice, I3, I4 y el valor ausente ────────────────────────────────────

def test_la_helice_guarda_la_vuelta_sin_interpretarla() -> None:
    """Decisión 4 (delamor, 12 oct): cada vuelta ocurre sobre otra W, así que la
    recursión tiene caso base. El módulo **no interpreta** `turn_ref`: la guarda."""
    ref = {"w_version_id": "fea41e52", "tick": 7}
    d = _regla(cut=0.30, tolerance=0.01).decide(["a"], capacity=1, turn_ref=ref)
    assert d.record["turn_ref"] == ref


def test_sin_turn_ref_queda_None_declarado_y_no_vuelta_cero() -> None:
    d = _regla(cut=0.30, tolerance=0.01).decide(["a"], capacity=1)
    assert d.record["turn_ref"] is None


def test_I3_el_registro_guarda_el_valor_exacto_y_no_la_categoria() -> None:
    """I3: el registro guarda el valor y la distancia **exactos**; la categoría
    "empate" **se deriva al leer**, contra la `tolerance` que el registro trae."""
    d = _regla(cut=0.50, tolerance=0.01).decide(["a", "b", "c", "d"], capacity=4)
    filas = {f["candidate"]: f for f in d.record["candidates"]}
    assert filas["a"]["field_value"] == 0.90
    assert filas["a"]["distance_to_cut"] == pytest.approx(0.40)
    assert filas["b"]["distance_to_cut"] == pytest.approx(0.0)
    assert all("tie" not in f for f in d.record["candidates"])
    # la categoría se deriva: |distancia| <= ε
    eps = d.record["params"]["tolerance"]["value"]
    derivado = {c for c, f in filas.items() if abs(f["distance_to_cut"]) <= eps}
    assert derivado == {"b", "c"}


def test_I4_el_valor_es_un_frozenset() -> None:
    """I4: si el orden decidiera algo, sería contexto. Medido en el REPORTE CP0:
    `w_sha` y las estimaciones por muestreo dependen del orden de los nodos."""
    d = _regla(cut=0.30, tolerance=0.01).decide(["a", "b", "c"], capacity=3)
    assert isinstance(d.value, frozenset)


def test_value_None_con_FIELD_levanta() -> None:
    """T7. Una decisión sin valor con origen de campo afirma lo que no decidió."""
    with pytest.raises(ValueError, match="no se decidió"):
        Decision(value=None, origin=FIELD, record={}, reason=REASON_FIELD)
    # con ESCALATED sí es admisible: es "no se decidió"
    assert Decision(value=None, origin=ESCALATED, record={},
                    reason=NO_TRACE).value is None


def test_origin_fuera_de_ORIGINS_levanta() -> None:
    with pytest.raises(ValueError, match="origin"):
        Decision(value=frozenset(), origin="CAMPO", record={}, reason=REASON_FIELD)


# ── "Un solo corazón" — el test estructural ─────────────────────────────────
#
# **Qué verifica, y qué NO.** Es un test **TEXTUAL**: busca los nombres con los
# que el repo YA escribe empate, piso y origen. Ve una copia que use esos nombres
# y **no ve una que los renombre**. Lo dice acá para no afirmar más de lo que
# verifica (regla del proyecto: una aserción que repite la fórmula del código no
# encuentra un off-by-one).
#
# La lista está **medida**, no supuesta: sale del inventario del REPORTE CP0 del
# 12 oct, corriendo este mismo barrido. Y va en **dos partes**, porque un archivo
# que sólo usa los nombres no es un corazón (sugerencia de delamor, 12 oct).

NEEDLES = {
    "empate": ("TOL_EMPATE", "empate"),
    "traza":  ("seleccion_anterior", "pertenencia_anterior"),
    "piso":   ("piso_vueltas", "_ciclos_sin_rebuild", "_vueltas_sin_llamar"),
    "origen": ("MOTIVO_", "VIA_", "rebuild_causa", "_last_rebuild_causa"),
}

# Corazones conocidos: **reimplementan** empate, piso u origen. Cada uno es un
# alineamiento **pendiente**, no un aval. El gate `f96c234` prohíbe tocarlos.
CORAZONES_CONOCIDOS = {
    "iap_chatroom/criterio_local.py":
        "exceptuado por el TASK: la traza de cómo era antes. No se toca hasta el CP3",
    "services/node_extractor.py":
        "_seleccionar: empate (TOL_EMPATE), traza (seleccion_anterior) y g (orden alfabético)",
    "services/corpus_service.py":
        "should_rebuild con `> 0` estricto y sin ε; rebuild_suspendido deja ganar la traza para siempre",
    "iap_chatroom/ckm_monitor.py":
        "la cascada de elif: f + piso + g en el mismo if (DECISIONES 12 oct: eran tres casilleros, no tres f)",
    "services/landscape_engine.py":
        "relax: h = 0 conserva s_i — paso 2 con ε = 0 implícito",
}

# Coincidencias textuales **sin corazón**: sólo usan los nombres. Cada una es la
# prueba del límite del test.
SOLO_TEXTO = {
    "iap_chatroom/autonomous_device.py":
        "pasa piso_vueltas a CriterioLocal: es consumidor, no implementación",
}

RAIZ = Path(__file__).resolve().parent.parent
# El módulo nuevo se excluye a propósito: ES el corazón, y eso es el punto.
EXCLUIDOS = {"services/ckm_trust_rule.py"}


def _barrido() -> dict:
    halladas = {}
    for carpeta in ("services", "iap_chatroom"):
        for f in sorted((RAIZ / carpeta).rglob("*.py")):
            rel = f.relative_to(RAIZ).as_posix()
            if rel in EXCLUIDOS or "test" in f.parts or f.name.startswith("test_"):
                continue
            texto = f.read_text(errors="replace")
            hits = {k: [n for n in ns if n in texto] for k, ns in NEEDLES.items()}
            hits = {k: v for k, v in hits.items() if v}
            if hits:
                halladas[rel] = hits
    return halladas


def test_un_solo_corazon_no_aparece_ninguno_nuevo() -> None:
    """
    **Un solo corazón** (delamor, 11 oct). Si aparece una segunda copia **fuera de
    la lista**, este test falla.

    Falla también si un archivo **sale** de la lista: eso quiere decir que alguien
    alineó un corazón, y entonces el inventario del CP0 hay que actualizarlo. Las
    dos direcciones son información.
    """
    halladas = set(_barrido())
    declaradas = set(CORAZONES_CONOCIDOS) | set(SOLO_TEXTO)
    nuevas = halladas - declaradas
    assert not nuevas, (
        "apareció un corazón fuera de la lista congelada: "
        f"{sorted(nuevas)}. El engine vive en services/ckm_trust_rule.py; "
        "si es un corazón nuevo, va al inventario del CP0 con su razón"
    )
    desaparecidas = declaradas - halladas
    assert not desaparecidas, (
        f"salieron de la lista: {sorted(desaparecidas)}. Si se alinearon, hay que "
        "actualizar el inventario del REPORTE CP0"
    )


def test_la_lista_congelada_no_mezcla_corazones_con_coincidencias() -> None:
    """Sugerencia de delamor, 12 oct: que el inventario no se infle. Un archivo que
    sólo usa los nombres **no es un corazón**, y cada parte lleva su razón."""
    assert not (set(CORAZONES_CONOCIDOS) & set(SOLO_TEXTO))
    assert all(v for v in CORAZONES_CONOCIDOS.values())
    assert all(v for v in SOLO_TEXTO.values())


def test_el_falso_positivo_es_la_prueba_del_limite() -> None:
    """`autonomous_device.py` entra al barrido **sólo** por `piso_vueltas`, que
    pasa a `CriterioLocal`. Es el límite textual, medido."""
    hits = _barrido()["iap_chatroom/autonomous_device.py"]
    assert hits == {"piso": ["piso_vueltas"]}


def test_el_engine_esta_excluido_a_proposito() -> None:
    """El módulo nuevo también usa la palabra "empate": se excluye porque **es** el
    corazón. Sin esta exclusión el test se delataría a sí mismo."""
    assert "empate" in (RAIZ / "services/ckm_trust_rule.py").read_text()
    assert "services/ckm_trust_rule.py" not in _barrido()
