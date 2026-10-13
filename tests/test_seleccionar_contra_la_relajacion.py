"""
¿`_seleccionar` cumple la regla de la relajación? — verificación previa al CP2

Pedido de delamor/Opus, 13 oct. **`services/node_extractor.py` no se toca.** La
predicción está escrita y commiteada **antes** de este archivo (`ab4e987`, BANDEJA).

## La regla contra la que se compara

`services/landscape_engine.py:74`:

    s = np.where(h > 0, 1., np.where(h < 0, -1., s))

**`h == 0` exacto → conserva `s`.** ε = 0 implícito.

**Mapeo:** `s = +1` en la selección, `−1` afuera · `h` = distancia al corte.

## Los cinco casos

| | caso | resultado |
|---|---|---|
| **a** | arriba / abajo del corte | **coincide** — y no es conservación: el campo decide |
| **b** | empate que **cabe** en los libres | **NO conserva**: entran todos, aunque estuvieran afuera. **Es el caso normal** |
| **c** | empate que **no cabe**, con `anterior` | **conserva**, y en **las dos** direcciones |
| **d** | empate que **no cabe**, sin `anterior` | **dos descripciones de la misma salida**, y el test no puede separarlas |
| **e** | ε | la relajación usa `h == 0`; `_seleccionar` usa `1e-12` |
"""

import json
from pathlib import Path

import numpy as np
import pytest

from services.node_extractor import NodeExtractorService

TOL = NodeExtractorService.TOL_EMPATE
RAIZ = Path(__file__).resolve().parent.parent
CORPUS_REGISTRADOS = [
    RAIZ / "process/experiments/armstrong_replica_seed123_corpus_state.json",
    RAIZ / "process/experiments/armstrong_via_corpus_v3_state.json",
]


# ── La relajación, tal cual `landscape_engine.py:74` ──────────────────────

def _relajacion(h, s_previo):
    """`h > 0 → +1` · `h < 0 → −1` · **`h == 0` → conserva**. ε = 0 implícito."""
    return np.where(h > 0, 1.0, np.where(h < 0, -1.0, s_previo))


def _s_de(terms, elegidos):
    """`σ` de una selección: `+1` adentro, `−1` afuera."""
    sel = set(elegidos)
    return np.array([1.0 if str(t) in sel else -1.0 for t in terms])


def _seleccionar(terms, scores, anterior, top_k):
    svc = NodeExtractorService(top_k=top_k, ngram_max=2)
    return svc._seleccionar(terms, scores, anterior)[0]


def _h(scores, terms, top_k):
    """`h` = distancia al corte, con el corte de `_seleccionar`."""
    orden = sorted(range(len(terms)), key=lambda i: (-scores[i], terms[i]))
    corte = scores[orden[top_k - 1]] if len(orden) > top_k else scores[orden[-1]]
    return np.asarray(scores) - corte


# ── a — arriba y abajo del corte: coincide ────────────────────────────────

def test_a_arriba_y_abajo_del_corte_coinciden_con_la_relajacion() -> None:
    """**Confirmado.** Donde el campo decide, las dos dan lo mismo — y **no es
    conservación**: el estado previo no interviene."""
    terms = np.array(["alfa", "beta", "gama", "delta", "epsilon"])
    scores = np.array([0.9, 0.7, 0.5, 0.3, 0.1])
    top_k = 3
    h = _h(scores, terms, top_k)

    for previo in (["alfa"], ["delta", "epsilon"], [], None):
        s_prev = _s_de(terms, previo or [])
        s_relax = _relajacion(h, s_prev)
        s_sel = _s_de(terms, _seleccionar(terms, scores, previo, top_k))
        # los que NO están en el corte: las dos reglas coinciden siempre
        fuera_del_corte = np.abs(h) > TOL
        assert np.array_equal(s_relax[fuera_del_corte], s_sel[fuera_del_corte])
    # y el estado previo no cambió nada ahí: no fue conservación
    a = _seleccionar(terms, scores, ["delta", "epsilon"], top_k)
    b = _seleccionar(terms, scores, None, top_k)
    assert set(a) == set(b) == {"alfa", "beta", "gama"}


# ── b — el empate que cabe NO conserva, y es el caso normal ───────────────

def test_b_el_empate_que_cabe_no_conserva() -> None:
    """
    **Confirmado, y es la violación.** El término del corte tiene `h == 0`
    **exactamente**, así que la relajación dice **conservar su `s`**. Pero si cabe
    en los libres, `_seleccionar` lo **mete**, viniera de donde viniera.
    """
    terms = np.array(["alfa", "beta", "gama", "delta", "epsilon"])
    scores = np.array([0.9, 0.7, 0.5, 0.3, 0.1])
    top_k = 3
    h = _h(scores, terms, top_k)
    i_corte = list(terms).index("gama")
    assert h[i_corte] == 0.0, "el término del corte tiene h exactamente 0"

    # venía de estar AFUERA: la relajación lo deja afuera, _seleccionar lo mete
    previo = ["alfa", "beta"]
    s_relax = _relajacion(h, _s_de(terms, previo))
    s_sel = _s_de(terms, _seleccionar(terms, scores, previo, top_k))
    assert s_relax[i_corte] == -1.0, "la relajación conserva el −1"
    assert s_sel[i_corte] == +1.0, "_seleccionar lo mete"
    assert not np.array_equal(s_relax, s_sel)


def test_b_es_el_caso_normal_no_la_excepcion() -> None:
    """**El término del corte siempre está en el empate** (CP1), y sin empate real
    `len(empate) = 1` y `libres = 1`: **cabe siempre**. Así que la violación de (b)
    no es un borde: es el camino por defecto."""
    for n, top_k in ((5, 3), (10, 4), (40, 20), (60, 20)):
        terms = np.array([f"t{i:03d}" for i in range(n)])
        scores = np.linspace(1.0, 0.1, n)      # sin empates reales
        h = _h(scores, terms, top_k)
        i_corte = int(np.argmin(np.abs(h)))
        assert h[i_corte] == 0.0
        # con el término del corte afuera en el estado previo
        previo = [str(t) for k, t in enumerate(terms) if k != i_corte][:top_k - 1]
        s_relax = _relajacion(h, _s_de(terms, previo))
        s_sel = _s_de(terms, _seleccionar(terms, scores, previo, top_k))
        assert s_relax[i_corte] == -1.0
        assert s_sel[i_corte] == +1.0, f"n={n}: no entró, revisar el caso"


# ── c — el empate que no cabe conserva, en las dos direcciones ────────────

def _caso_empate_que_no_cabe():
    terms = np.array(["alfa", "beta", "gama", "delta", "epsilon"])
    scores = np.array([0.9, 0.7, 0.5, 0.5, 0.1])    # gama y delta empatados
    return terms, scores, 3


def test_c_conserva_el_mas_uno() -> None:
    """**Confirmado.** El empatado que ya estaba adentro se queda."""
    terms, scores, top_k = _caso_empate_que_no_cabe()
    h = _h(scores, terms, top_k)
    sel = _seleccionar(terms, scores, ["alfa", "gama"], top_k)
    s_relax = _relajacion(h, _s_de(terms, ["alfa", "gama"]))
    i = list(terms).index("gama")
    assert s_relax[i] == +1.0
    assert _s_de(terms, sel)[i] == +1.0
    assert sel == ["alfa", "beta", "gama"]


def test_c_conserva_tambien_el_menos_uno() -> None:
    """
    **Lo que agregué a la predicción de Opus.** El empatado que **no** estaba
    adentro se queda **afuera**, y eso también es conservar: `s = −1`.

    Es lo que pasa en los dos armstrong, donde `pertenencia_anterior` es `False` en
    los tres empatados.
    """
    terms, scores, top_k = _caso_empate_que_no_cabe()
    h = _h(scores, terms, top_k)
    previo = ["alfa", "delta"]          # gama estaba AFUERA, delta adentro
    sel = _seleccionar(terms, scores, previo, top_k)
    s_relax = _relajacion(h, _s_de(terms, previo))
    s_sel = _s_de(terms, sel)
    i_gama, i_delta = list(terms).index("gama"), list(terms).index("delta")
    assert (s_relax[i_gama], s_relax[i_delta]) == (-1.0, +1.0)
    assert (s_sel[i_gama], s_sel[i_delta]) == (-1.0, +1.0)
    # el vector entero coincide: en este caso _seleccionar ES la relajación
    assert np.array_equal(s_relax, s_sel)


# ── d — dos descripciones de la misma salida ──────────────────────────────

def test_d_el_arranque_en_frio_no_se_puede_distinguir_por_la_salida() -> None:
    """
    **Lo predicho: el test no puede separarlas.**

    - **`g` (lectura de Opus):** no hay traza, algo de contexto resuelve → afuera.
    - **T declarada (mía):** el docstring declara *"bootstrap: el estado inicial es
      'ningún nodo'"*, o sea `s = −1` para todos → **conservar**.

    Las dos dan **el mismo vector**. Lo único que el test puede hacer es exhibirlo.
    Es la pregunta abierta del arranque en frío (`REG_regla_ckm_trust_v1` §4):
    *"ningún nodo"* ¿es traza o es contexto? **No se resuelve acá.**
    """
    terms, scores, top_k = _caso_empate_que_no_cabe()
    h = _h(scores, terms, top_k)
    sel = _seleccionar(terms, scores, None, top_k)
    assert sel == ["alfa", "beta"], "sin anterior, los empatados quedan afuera"

    # la lectura "T declarada": el estado inicial es ningún nodo, s = −1 ∀i
    s_bootstrap = np.full(len(terms), -1.0)
    s_relax = _relajacion(h, s_bootstrap)
    assert np.array_equal(_s_de(terms, sel), s_relax), (
        "bajo el bootstrap declarado, quedar afuera ES conservar"
    )
    # y las dos descripciones son indistinguibles por la salida
    assert np.array_equal(s_relax, _s_de(terms, sel))


# ── e — la banda de ε ─────────────────────────────────────────────────────

def test_e_la_relajacion_decide_donde_seleccionar_empata() -> None:
    """
    **Confirmado.** La relajación usa `h == 0` **exacto**; `_seleccionar` trata como
    empate toda la banda `|h| ≤ 1e-12`. En esa banda las dos **difieren por
    construcción**: la relajación ve `h > 0` y mete, `_seleccionar` ve empate y
    aplica su propia regla.

    Ya medido en las tensiones (`0adde50`): **0 de 121 filas** de los corpus
    registrados caen en la banda. **Estructuralmente distinto, no observado.**

    El caso pide cuidado al armarlo: si el término de la banda **es** el del corte,
    su `h` es `0` y no hay banda que mostrar. Acá `gama` es el corte y `delta` queda
    a `−5e-13` de él.
    """
    terms = np.array(["alfa", "beta", "gama", "delta", "epsilon"])
    #                   0.9   0.8   0.5+5e-13  0.5    0.1
    scores = np.array([0.9, 0.8, 0.5 + 5e-13, 0.5, 0.1])
    top_k = 3
    h = _h(scores, terms, top_k)
    i_delta = list(terms).index("delta")
    assert h[list(terms).index("gama")] == 0.0, "gama es el corte"
    assert 0 < abs(h[i_delta]) <= TOL, "delta está DENTRO de la banda"

    previo = ["alfa", "beta", "delta"]      # delta venía de ADENTRO
    s_relax = _relajacion(h, _s_de(terms, previo))
    sel = _seleccionar(terms, scores, previo, top_k)
    assert s_relax[i_delta] == -1.0, "para la relajación h < 0: sale"
    assert _s_de(terms, sel)[i_delta] == +1.0, "para _seleccionar es empate: conserva"
    assert sel == ["alfa", "beta", "delta"]


# ── (b) frente a (c) en los corpus registrados ───────────────────────────

@pytest.mark.parametrize("ruta", CORPUS_REGISTRADOS, ids=lambda p: p.stem)
def test_cuantas_veces_b_frente_a_c(ruta) -> None:
    """
    **Reconstrucción, no la historia real.** Los corpus registrados son un
    **snapshot final**: no tengo la secuencia de rebuilds. Se reconstruye corriendo
    la selección sobre **prefijos crecientes** de `texts`, encadenando cada
    selección como `anterior` de la siguiente — que es lo que `_rebuild` hace.
    **Declarado antes de correr** (`ab4e987`).

    Los archivos no están trackeados: se saltea si faltan.

    ## LA PREDICCIÓN QUEDÓ REFUTADA

    Predije *"(b) muy por encima de (c), (c) por debajo del 15 %"*. **Al revés:**
    (c) es **29 de 38**, el **76 %**; (b) es **8**. La aserción de abajo fija lo
    medido, no lo predicho.

    **El mecanismo, que es lo que importa:** mi razonamiento era *"la igualdad
    exacta es rara"*. **En TF-IDF sobre un corpus chico no es rara: es la norma al
    fondo del ranking.** Los términos que aparecen en los **mismos** documentos con
    los **mismos** conteos tienen vectores idénticos y por lo tanto medias
    idénticas; en un corpus de 40 textos hay muchos términos que aparecen una vez
    en un solo documento, y **entre ellos son indistinguibles**.

    Medido: `len(empate)` va de **1 a 12**, y vale **1 en 1 de 38** rebuilds.
    **El corte cae sobre una meseta, no sobre un punto.**
    """
    if not ruta.exists():
        pytest.skip(f"corpus registrado ausente (no trackeado): {ruta.name}")

    textos = [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    cuenta = {"b_cabe": 0, "c_no_cabe_con_anterior": 0, "d_no_cabe_sin_anterior": 0}
    anterior = None

    for n in range(3, len(textos) + 1):
        vec = svc._vectorizer(max_features=60)
        M = vec.fit_transform(textos[:n])
        terms = vec.get_feature_names_out()
        scores = np.asarray(M.mean(axis=0)).flatten()
        if len(terms) <= 20:
            continue
        orden = sorted(range(len(terms)), key=lambda i: (-scores[i], terms[i]))
        corte = scores[orden[20 - 1]]
        arriba = [i for i in orden if scores[i] - corte > TOL]
        empate = [i for i in orden if abs(scores[i] - corte) <= TOL]
        libres = 20 - len(arriba)
        if len(empate) <= libres:
            cuenta["b_cabe"] += 1
        elif anterior is None:
            cuenta["d_no_cabe_sin_anterior"] += 1
        else:
            cuenta["c_no_cabe_con_anterior"] += 1
        anterior = svc._seleccionar(terms, scores, anterior)[0]

    total = sum(cuenta.values())
    assert total == 38, f"la reconstrucción cambió de tamaño: {cuenta}"
    # LO MEDIDO, que refuta lo predicho
    assert cuenta == {"b_cabe": 8, "c_no_cabe_con_anterior": 29,
                      "d_no_cabe_sin_anterior": 1}, cuenta
    assert cuenta["c_no_cabe_con_anterior"] / total > 0.75, "(c) domina"
    print(f"\n  {ruta.stem}: {cuenta}  (total {total})")


@pytest.mark.parametrize("ruta", CORPUS_REGISTRADOS, ids=lambda p: p.stem)
def test_el_corte_cae_sobre_una_meseta(ruta) -> None:
    """
    **El mecanismo detrás del número**, y la razón por la que mi predicción falló.
    `len(empate) == 1` —el caso que yo suponía normal— se da **1 de 38** veces. El
    resto del tiempo el corte cae sobre un grupo de **2 a 12** términos con la
    **misma** media de TF-IDF.

    No es coincidencia numérica: términos que aparecen en los mismos documentos con
    los mismos conteos son **indistinguibles** para este `f`.
    """
    if not ruta.exists():
        pytest.skip(f"corpus registrado ausente (no trackeado): {ruta.name}")

    textos = [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    tamanos = []
    for n in range(3, len(textos) + 1):
        vec = svc._vectorizer(max_features=60)
        M = vec.fit_transform(textos[:n])
        terms = vec.get_feature_names_out()
        scores = np.asarray(M.mean(axis=0)).flatten()
        if len(terms) <= 20:
            continue
        orden = sorted(range(len(terms)), key=lambda i: (-scores[i], terms[i]))
        corte = scores[orden[19]]
        tamanos.append(sum(1 for i in orden if abs(scores[i] - corte) <= TOL))

    assert len(tamanos) == 38
    assert min(tamanos) == 1 and max(tamanos) == 12
    assert tamanos.count(1) == 1, "el corte casi nunca cae sobre un solo término"
