"""
`_seleccionar` y el pool como **instancia** de `CkmTrustRule` — CP1

`TASK_node_extractor_regla_v1`, CP1. **`services/node_extractor.py` NO se toca**:
se lo expresa en la forma acá y se compara contra el código de hoy.

**La predicción está escrita y commiteada ANTES de este archivo** (`2f9ead0`, en la
BANDEJA). Lo que sigue la verifica.

## La instancia

| casillero | qué es |
|---|---|
| **C** | los términos del **pool** |
| **f** | el TF-IDF **medio** del término |
| **κ** | `scores[orden[top_k-1]]` — **un cuantil de `C`**, ver abajo |
| **ε** | `1e-12`, `DECLARED`, *"numérica, no medida"* (delamor/Opus, 13 oct) |
| **T** | `seleccion_anterior`, **colapsada** por `self._nodes or None` |
| **P** | `None` declarado — no hay reloj (**F1**) |
| **g** | `None`: el orden alfabético queda **afuera** |
| **↑k** | `None` → `ESCALATED` |
| **capacity** | `top_k` — `libres = top_k - len(arriba)` **es** el `free` del engine |

## `empate` nunca está vacío

`corte = scores[orden[top_k-1]]`, así que el término del corte tiene distancia
**exactamente 0** y siempre cae en `empate`. Por eso el caso normal **no** es *"no
hay empate"*: es *"el empate es el propio término del corte, y entra"*.

## κ sale de adentro del propio orden

La forma dice que todo umbral lo produce **el orden de arriba** (12 oct). Acá el
corte es un **cuantil de `C`**: se calcula con los mismos datos sobre los que se
decide. `produced_by_order` no tiene qué poner que sea verdad, y se declara así.
Va a *"Lo que la forma no nombra"*. **No se resuelve acá.**
"""

import json
from pathlib import Path

import numpy as np
import pytest

from services.ckm_trust_rule import (
    DECLARED, ESCALATED, FIELD, FLOOR_UNKNOWN, MEASURED, NO_TRACE,
    REASON_FLOOR_UNKNOWN, REASON_TIE_FITS, CkmTrustRule, RuleParams, Threshold,
)
from services.node_extractor import NodeExtractorService

RAIZ = Path(__file__).resolve().parent.parent
CORPUS_REGISTRADOS = [
    RAIZ / "process/experiments/armstrong_replica_seed123_corpus_state.json",
    RAIZ / "process/experiments/armstrong_via_corpus_v3_state.json",
]
TOL = NodeExtractorService.TOL_EMPATE


# ── La copia congelada de `_seleccionar` (`94208a5`), el oráculo ───────────

def _SELECCIONAR_CONGELADO(terms, scores, anterior, top_k, tol=TOL):
    """`node_extractor.py:256-296` en `94208a5`, copiado sin tocar nada salvo
    sacarlo del objeto. Devuelve sólo los elegidos: el registro no se compara."""
    orden = sorted(range(len(terms)), key=lambda i: (-scores[i], terms[i]))
    if len(orden) <= top_k:
        elegidos = orden
    else:
        corte = scores[orden[top_k - 1]]
        arriba = [i for i in orden if scores[i] - corte > tol]
        empate = [i for i in orden if abs(scores[i] - corte) <= tol]
        libres = top_k - len(arriba)
        if len(empate) <= libres:
            elegidos = arriba + empate
        elif anterior is None:
            elegidos = arriba
        else:
            prev = set(anterior)
            elegidos = arriba + [i for i in empate if terms[i] in prev]
    return [str(terms[i]) for i in elegidos]


# ── La instancia ───────────────────────────────────────────────────────────

def _regla(terms, scores, top_k) -> CkmTrustRule:
    orden = sorted(range(len(terms)), key=lambda i: (-scores[i], terms[i]))
    corte = scores[orden[top_k - 1]] if len(orden) > top_k else scores[orden[-1]]
    puntaje = {str(terms[i]): float(scores[i]) for i in range(len(terms))}
    return CkmTrustRule(
        order="n1 — el corpus, una vuelta de accumulate",
        params=RuleParams(
            cut=Threshold(
                value=float(corte),
                # LA DECLARACIÓN INCÓMODA: no hay orden de arriba. El corte es un
                # cuantil de C, calculado con los datos sobre los que se decide.
                produced_by_order="n1 — el propio corpus (cuantil de C)",
                provenance=MEASURED,
                source="scores[orden[top_k-1]], node_extractor.py:271",
            ),
            tolerance=Threshold(
                value=TOL, produced_by_order="n2 — los parámetros de extracción",
                provenance=DECLARED, source="numérica, no medida (delamor/Opus, 13 oct)",
            ),
            floor=None,     # P: no hay reloj (F1). None declarado, nunca 0
        ),
        field_criterion=lambda t: puntaje[t],
        context=None,       # el orden alfabético queda AFUERA de la instancia
        escalate_to=None,   # ↑k: no hay. ESCALATED con escalate_to=None (I5)
    )


def _decidir(terms, scores, anterior, top_k):
    cands = [str(t) for t in terms]
    return _regla(terms, scores, top_k).decide(
        cands,
        capacity=top_k,
        trace=None if anterior is None else frozenset(anterior),
        trace_streak=None,          # no hay reloj: nunca se supo
        turn_ref={"n_candidatos": len(cands), "top_k": top_k},
    )


def _conjunto(dec):
    """El conjunto que la instancia eligió, o `None` si no decidió."""
    return None if dec.value is None else set(dec.value)


# ── El régimen 1: el empate cabe → la forma y el código coinciden ──────────

def test_CP4_el_empate_que_cabe_ya_NO_coincide_con_seleccionar() -> None:
    """
    **El CP4 se llevó el único régimen donde la instancia coincidía.**

    Hasta el 13 oct esto era el *"régimen 1"* del CP1: `len(empate) <= libres` →
    `FIELD · tie_fits_free_slots`, **mismo conjunto** que `_seleccionar`. Era el
    caso normal —sin empate real, el empate es sólo el término del corte y cabe—.

    **Sacada la exención**, el empate va al paso 2; acá no hay traza, así que la
    duda **sube**. `_seleccionar` sigue metiendo al término del corte: **conserva su
    copia de la exención hasta el CP2** de este TASK, y la divergencia queda
    declarada.
    """
    terms = np.array(["alfa", "beta", "gama", "delta", "epsilon"])
    scores = np.array([0.9, 0.7, 0.5, 0.3, 0.1])
    top_k = 3
    hoy = _SELECCIONAR_CONGELADO(terms, scores, None, top_k)
    dec = _decidir(terms, scores, None, top_k)

    assert set(hoy) == {"alfa", "beta", "gama"}, "_seleccionar no cambió"
    assert dec.origin == ESCALATED and dec.reason == NO_TRACE
    assert _conjunto(dec) is None
    # la capacidad sigue registrada: se fue su salida del paso 1, no ella
    assert dec.record["n_tied"] == 1 and dec.record["free_slots"] == 1


def test_empate_nunca_esta_vacio() -> None:
    """La lectura en la que se apoya todo lo anterior: el término del corte tiene
    distancia **exactamente 0**, así que siempre cae en el empate."""
    for n, top_k in ((5, 3), (10, 4), (60, 20)):
        terms = np.array([f"t{i:03d}" for i in range(n)])
        scores = np.linspace(1.0, 0.1, n)
        dec = _decidir(terms, scores, None, top_k)
        assert dec.record["n_tied"] >= 1
        assert dec.record["free_slots"] >= 1


# ── El régimen 2: el empate no cabe → la instancia NO decide ───────────────

def _caso_con_empate_que_no_cabe(top_k=3):
    """Dos términos empatados exactamente en el corte, con un solo lugar libre."""
    terms = np.array(["alfa", "beta", "gama", "delta", "epsilon"])
    #                   0.9    0.7    0.5    0.5     0.1
    scores = np.array([0.9, 0.7, 0.5, 0.5, 0.1])
    return terms, scores, top_k


def test_cuando_el_empate_no_cabe_y_no_hay_traza_la_instancia_escala() -> None:
    """**Régimen 2, variante T=None.** El paso 2 no aplica: `NO_TRACE`, **sin**
    `FLOOR_UNKNOWN`. Hoy devuelve `arriba`."""
    terms, scores, top_k = _caso_con_empate_que_no_cabe()
    hoy = _SELECCIONAR_CONGELADO(terms, scores, None, top_k)
    dec = _decidir(terms, scores, None, top_k)

    assert hoy == ["alfa", "beta"], "hoy: los empatados quedan afuera"
    assert dec.origin == ESCALATED
    assert dec.reason == NO_TRACE
    assert FLOOR_UNKNOWN not in dec.markers, "sin traza, el piso ni se mira"
    assert dec.escalate_to is None, "I5: no hay a quién subir, y se queda"
    assert _conjunto(dec) is None


def test_cuando_el_empate_no_cabe_y_hay_traza_escala_por_el_piso() -> None:
    """**Régimen 2, variante T presente.** Hay traza y el piso **no se evalúa**:
    `floor_not_evaluable`, **con** `FLOOR_UNKNOWN` y `floor_missing`. Hoy conserva."""
    terms, scores, top_k = _caso_con_empate_que_no_cabe()
    anterior = ["alfa", "gama"]
    hoy = _SELECCIONAR_CONGELADO(terms, scores, anterior, top_k)
    dec = _decidir(terms, scores, anterior, top_k)

    assert hoy == ["alfa", "beta", "gama"], "hoy: la traza conserva a 'gama'"
    assert dec.origin == ESCALATED
    assert dec.reason == REASON_FLOOR_UNKNOWN
    assert FLOOR_UNKNOWN in dec.markers
    assert dec.record["floor_missing"] == "floor_absent"
    assert _conjunto(dec) is None


def test_P_y_T_escalan_por_razones_DISTINTAS_y_el_registro_las_separa() -> None:
    """
    **La predicción que importa:** las dos convergen en *"no decidí"*, y el registro
    **las distingue**. Si salieran iguales, el colapso de `T`
    (`corpus_service.py:298`, `self._nodes or None`) sería invisible también en la
    forma.
    """
    terms, scores, top_k = _caso_con_empate_que_no_cabe()
    sin_t = _decidir(terms, scores, None, top_k)
    con_t = _decidir(terms, scores, ["alfa", "gama"], top_k)

    assert sin_t.value is con_t.value is None          # la misma decisión
    assert sin_t.reason != con_t.reason                 # y razones distintas
    assert (sin_t.reason, FLOOR_UNKNOWN in sin_t.markers) == (NO_TRACE, False)
    assert (con_t.reason, FLOOR_UNKNOWN in con_t.markers) == (REASON_FLOOR_UNKNOWN, True)


# ── La frontera: `len(empate) > libres` y nada más ─────────────────────────

def test_CP4_el_barrido_ya_no_coincide_en_ningun_regimen() -> None:
    """
    **El CP4 borró la frontera.** El CP1 había medido **30 coinciden / 60 divergen**,
    y la frontera era exactamente `len(empate) > libres`.

    **Sacada la exención, divergen los 90.** La causa es la misma de siempre —**P =
    `None`**: sin piso evaluable el paso 2 no corre y la instancia escala—, y ahora
    sin la exención que le tapaba un régimen.

    **La divergencia entre la forma y `_seleccionar` pasa de un régimen a todos.**
    """
    casos, difs, iguales = 0, 0, 0
    for n in (4, 5, 8, 12):
        for top_k in (2, 3, 5):
            if top_k >= n:
                continue
            for n_empatados in (1, 2, 3):
                for anterior in (None, ["t000"], ["t000", "t002"]):
                    terms = np.array([f"t{i:03d}" for i in range(n)])
                    scores = np.linspace(1.0, 0.2, n)
                    # plantar el empate exacto alrededor del corte
                    for j in range(n_empatados):
                        if top_k - 1 + j < n:
                            scores[top_k - 1 + j] = scores[top_k - 1]
                    casos += 1
                    hoy = set(_SELECCIONAR_CONGELADO(terms, scores, anterior, top_k))
                    dec = _decidir(terms, scores, anterior, top_k)
                    if _conjunto(dec) == hoy:
                        iguales += 1
                    else:
                        # todas escalan: ni una decide
                        assert _conjunto(dec) is None
                        assert dec.origin == ESCALATED
                        difs += 1
    assert casos == 90
    assert (iguales, difs) == (0, 90), "el CP4 dejó alguna coincidencia"


# ── ε: indistinguible hoy, visible sólo si algo cae en la banda ────────────

def test_epsilon_declarada_no_cambia_nada_fuera_de_la_banda() -> None:
    """`ε = 1e-12` contra el `TOL_EMPATE` del código: **el mismo número**, así que
    por construcción no puede divergir. Lo que el CP1 verifica es lo otro: que en
    los corpus registrados **nada cae en la banda**, ya medido (0 de 121)."""
    assert TOL == 1e-12
    terms = np.array(["alfa", "beta", "gama", "delta"])
    # un puntaje DENTRO de la banda: a 5e-13 del corte
    scores = np.array([0.9, 0.5, 0.5 + 5e-13, 0.1])
    dec = _decidir(terms, scores, None, top_k=2)
    assert dec.record["n_tied"] == 2, "los dos de la banda son empate con ε=1e-12"
    # con ε = 0 serían dos cosas distintas: ahí la declaración se vuelve visible
    r0 = CkmTrustRule(
        order="n1", field_criterion=lambda t: dict(zip(map(str, terms), scores))[t],
        params=RuleParams(
            cut=Threshold(value=0.5, produced_by_order="n1", provenance=MEASURED),
            tolerance=Threshold(value=0.0, produced_by_order="n2", provenance=DECLARED),
            floor=None),
    ).decide([str(t) for t in terms], capacity=2, trace=None)
    assert r0.record["n_tied"] == 1, "con ε=0 el de la banda queda arriba"


# ── Los corpus registrados ─────────────────────────────────────────────────

@pytest.mark.parametrize("ruta", CORPUS_REGISTRADOS, ids=lambda p: p.stem)
def test_los_corpus_registrados_dan_lo_predicho(ruta) -> None:
    """
    **Los números de la predicción**: pool 60, `arriba` 19, `empate` 3, `libres` 1.
    `3 > 1` → hoy **19 nodos**, la instancia **"no decidí"**, con las dos variantes
    de T.

    Los archivos **no están trackeados**: se saltea si faltan. El barrido de arriba
    cubre los dos regímenes sin depender de ellos.
    """
    if not ruta.exists():
        pytest.skip(f"corpus registrado ausente (no trackeado): {ruta.name}")

    textos = [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    vec = svc._vectorizer(max_features=60)
    M = vec.fit_transform(textos)
    terms = vec.get_feature_names_out()
    scores = np.asarray(M.mean(axis=0)).flatten()
    top_k = 20

    for anterior in (None, list(json.loads(ruta.read_text())["nodes"])):
        hoy = _SELECCIONAR_CONGELADO(terms, scores, anterior, top_k)
        dec = _decidir(terms, scores, anterior, top_k)
        assert len(terms) == 60
        assert dec.record["n_above"] == 19
        assert dec.record["n_tied"] == 3
        assert dec.record["free_slots"] == 1
        assert len(hoy) == 19
        assert _conjunto(dec) is None, "la instancia no decide"
        assert dec.origin == ESCALATED


# ── El pool: predicho que NO entra en la forma ─────────────────────────────

def test_el_pool_no_entra_en_la_forma() -> None:
    """
    **La predicción, verificada.** El pool le arma el `C` a `_seleccionar` **y
    además le mueve el `f`** (CP0 g: la norma l2 se calcula sólo sobre el pool).

    En la forma, `C` y `f` son **dos casilleros distintos de la misma regla**, y
    nada los escribe a los dos a la vez desde afuera. Un `C` que cambia el `f` del
    paso siguiente **no es un `C`**.

    Acá se mide lo que haría falta para que fuera sólo `C`: que los puntajes de los
    candidatos **no dependan** de cuáles son los candidatos. **No se cumple.**

    **No entra. Es falla, y va al CP0b de `TASK_ckm_trust_rule_v1`.** No se lo deja
    afuera como `C`: delamor descartó esa lectura el 13 oct.
    """
    svc = NodeExtractorService(top_k=3, ngram_max=1)
    textos = [
        "alfa beta gama ruido uno dos tres cuatro cinco seis",
        "alfa beta gama",
        "alfa beta siete ocho nueve",
        "alfa gama diez once doce trece",
        "beta gama catorce",
        "alfa beta gama quince dieciseis",
    ]
    vp = svc._vectorizer(max_features=9)
    Mp = vp.fit_transform(textos)
    tp, sp = vp.get_feature_names_out(), np.asarray(Mp.mean(axis=0)).flatten()

    va = svc._vectorizer()
    Ma = va.fit_transform(textos)
    ta, sa = va.get_feature_names_out(), np.asarray(Ma.mean(axis=0)).flatten()
    mapa = {t: i for i, t in enumerate(ta)}
    s_sin = np.array([sa[mapa[t]] for t in tp])

    # si el pool fuera sólo C, esto tendría que valer, y no vale
    assert not np.allclose(sp, s_sin), (
        "si el pool fuera sólo C, restringirlo no cambiaría el f de los que quedan"
    )
    # y la consecuencia: la decisión del paso siguiente cambia
    assert (_SELECCIONAR_CONGELADO(tp, sp, None, 3)
            != _SELECCIONAR_CONGELADO(tp, s_sin, None, 3))
