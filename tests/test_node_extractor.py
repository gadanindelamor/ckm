"""
test_node_extractor.py — suite de NodeExtractorService

El servicio que decide qué existe (los N nodos que se vuelven el espacio).
Hasta sep 2026 tenía 6 tests de forma (claves, no vacío, σ binario) que no
habrían detectado ni la re-extracción por texto (5aa3504) ni la búsqueda
por substring (7bf485b). Esta suite verifica el criterio.

Ejecutar:
    pytest tests/test_node_extractor.py -v
"""

from __future__ import annotations
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "services"))
from node_extractor import NodeExtractorService, _STOPWORDS

CASO09 = ROOT / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]


def _caso09():
    if not CASO09.exists():
        pytest.skip("corpus caso09 no disponible")
    return json.loads(CASO09.read_text())["texts"]


def _activos(ex, textos, nodes):
    """Nodos presentes en cada texto según el mismo analizador."""
    m = ex._vectorizer(vocabulary=nodes).fit_transform(textos)
    return [{nodes[i] for i in m[k].nonzero()[1]} for k in range(len(textos))]


# ── 1. Pares correctos ──────────────────────────────────────────────────────

@pytest.mark.parametrize("fuente", ["tests", "caso09"])
def test_pares_son_la_copresencia_por_texto(fuente):
    textos = TEXTS if fuente == "tests" else _caso09()
    ex = NodeExtractorService(top_k=10 if fuente == "tests" else 32)
    r = ex.accumulate(textos)
    esperado = {}
    for act in _activos(ex, textos, r["nodes"]):
        for a, b in combinations(sorted(act), 2):
            esperado[(a, b)] = esperado.get((a, b), 0) + 1
    assert r["pairs"] == esperado


@pytest.mark.parametrize("fuente", ["tests", "caso09"])
def test_suma_de_pares_por_texto_es_el_global(fuente):
    textos = TEXTS if fuente == "tests" else _caso09()
    r = NodeExtractorService(top_k=10 if fuente == "tests" else 32).accumulate(textos)
    suma = {}
    for d in r["pairs_by_text"]:
        for par, v in d.items():
            suma[par] = suma.get(par, 0) + v
    assert suma == r["pairs"]


def test_node_freq_es_textos_donde_aparece():
    ex = NodeExtractorService(top_k=10)
    r = ex.accumulate(TEXTS)
    act = _activos(ex, TEXTS, r["nodes"])
    for n in r["nodes"]:
        assert r["node_freq"].get(n, 0) == sum(n in a for a in act)


# ── 2. Criterio de selección ────────────────────────────────────────────────

def test_top_k_nodos_y_pool_por_frecuencia():
    """Nodos ⊂ pool de top_k·3 más frecuentes; son los de mayor TF-IDF medio
    dentro de ese pool (sin contar el desempate, ver §3)."""
    textos = _caso09()
    ex = NodeExtractorService(top_k=32)
    r = ex.accumulate(textos)
    v = ex._vectorizer(max_features=96)
    m = v.fit_transform(textos)
    pool = set(v.get_feature_names_out())
    assert len(r["nodes"]) == 32
    assert set(r["nodes"]) <= pool
    sc = dict(zip(v.get_feature_names_out(), np.asarray(m.mean(axis=0)).ravel()))
    umbral = min(sc[n] for n in r["nodes"])
    fuera = [t for t in pool if t not in r["nodes"]]
    assert all(sc[t] <= umbral + 1e-12 for t in fuera)


# ── 3. Empates en el borde del top_k ────────────────────────────────────────

@pytest.mark.xfail(strict=True, reason=(
    "Medido sep 2026: 94/210 W con empate en el borde del top-32; en 85 la "
    "selección depende del orden de desempate (argsort no estable sobre el "
    "orden alfabético de sklearn). Criterio de desempate: decisión pendiente."))
def test_seleccion_no_depende_del_orden_de_desempate():
    textos = _caso09()[:10]          # caso09 con empate en el borde que cambia
                                     # la selección: k = 4–10 y 18 (medido)
    ex = NodeExtractorService(top_k=32)
    v = ex._vectorizer(max_features=96)
    sc = np.asarray(v.fit_transform(textos).mean(axis=0)).ravel()
    a = set(np.argsort(sc)[::-1][:32])
    b = set(np.argsort(-sc, kind="stable")[:32])
    assert a == b


# ── 4. Stopwords y bigramas ─────────────────────────────────────────────────

def test_bigrama_se_arma_despues_de_sacar_stopwords():
    ex = NodeExtractorService()
    terminos = set(ex._vectorizer().build_analyzer()("Mark joined the channel"))
    assert "joined channel" in terminos
    assert "the" not in terminos


def test_stopwords_no_son_nodos():
    r = NodeExtractorService(top_k=20).accumulate(TEXTS)
    assert not set(r["nodes"]) & _STOPWORDS
    for n in r["nodes"]:
        assert not set(n.split()) & _STOPWORDS


def test_bigrama_implica_sus_unigramas_en_el_texto():
    """Documenta, no corrige: si un bigrama y su unigrama son ambos nodos,
    co-ocurren en todo texto donde aparece el bigrama (TASK_extraccion_una_rama,
    'no resuelve bigramas que contienen unigramas nodo')."""
    ex = NodeExtractorService()
    act = _activos(ex, ["gun control laws"], ["gun control", "gun", "control"])[0]
    assert act == {"gun control", "gun", "control"}


# ── 5. Alineación de pairs_by_text ──────────────────────────────────────────

def test_pairs_by_text_alineado_con_vacios():
    ex = NodeExtractorService(top_k=10)
    textos = [TEXTS[0], "", TEXTS[4], "   ", TEXTS[5]]
    r = ex.accumulate(textos)
    assert len(r["pairs_by_text"]) == len(textos)
    assert r["pairs_by_text"][1] == {} and r["pairs_by_text"][3] == {}
    assert r["pairs_by_text"][0] == ex.accumulate(
        [TEXTS[0], TEXTS[4], TEXTS[5]])["pairs_by_text"][0]


# ── 6. Determinismo ─────────────────────────────────────────────────────────

def test_mismos_textos_mismos_nodos_mismo_orden():
    textos = _caso09()
    a = NodeExtractorService(top_k=32).accumulate(textos)
    b = NodeExtractorService(top_k=32).accumulate(list(textos))
    assert a["nodes"] == b["nodes"] and a["pairs"] == b["pairs"]


# ── 7. Tokenización ─────────────────────────────────────────────────────────

def test_minusculas_acentos_y_minimo_tres_letras():
    an = NodeExtractorService()._vectorizer().build_analyzer()
    t = set(an("Canción ÑANDÚ ok ab abc GUN"))
    assert {"canción", "ñandú", "abc", "gun"} <= t
    assert "ok" not in t and "ab" not in t


def test_evaluate_no_activa_por_substring():
    ex = NodeExtractorService()
    sig = ex.evaluate("someone knows where", ["one", "now", "here", "someone"])
    assert list(sig) == [-1.0, -1.0, -1.0, 1.0]
