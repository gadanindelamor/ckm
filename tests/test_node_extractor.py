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


# ── 3. Empates en el borde del top_k — regla de la relajación ─────────────
# TASK_desempate_seleccion_nodos_v1. Empate = indecidible con el propio
# criterio. Con precedente: conserva. Sin precedente (bootstrap): afuera.

# El caso tiene que ser uno donde la regla DECIDA: más empatados que lugares
# libres. Con menos empatados que lugares, entran todos y no hay nada que
# decidir. Medido con la lista de stopwords vigente: k = 8 (28 arriba,
# 9 empatados, 4 libres).
K_EMPATE = 8


def _borde(textos, top_k=32):
    """(arriba del corte, empatados en el corte, lugares libres)."""
    ex = NodeExtractorService(top_k=top_k)
    sc = np.asarray(ex._vectorizer(max_features=top_k * 3)
                    .fit_transform(textos).mean(axis=0)).ravel()
    if len(sc) <= top_k:
        return 0, 0, top_k
    corte = np.sort(sc)[::-1][top_k - 1]
    arriba = int((sc - corte > 1e-12).sum())
    empatados = int((np.abs(sc - corte) <= 1e-12).sum())
    return arriba, empatados, top_k - arriba


def test_caso09_tiene_empate_que_decide():
    arriba, empatados, libres = _borde(_caso09()[:K_EMPATE])
    assert empatados > libres > 0


def test_bootstrap_empatados_quedan_afuera():
    ex = NodeExtractorService(top_k=32)
    r = ex.accumulate(_caso09()[:K_EMPATE])
    reg = {d["termino"]: d for d in r["registro_borde"]}
    empatados = [t for t, d in reg.items() if abs(d["distancia_al_corte"]) <= 1e-12]
    assert empatados and not set(empatados) & set(r["nodes"])
    assert all(reg[n]["distancia_al_corte"] > 1e-12 for n in r["nodes"])


def test_con_precedente_empatados_conservan():
    ex = NodeExtractorService(top_k=32)
    textos = _caso09()[:K_EMPATE]
    reg = ex.accumulate(textos)["registro_borde"]
    empatados = [d["termino"] for d in reg if abs(d["distancia_al_corte"]) <= 1e-12]
    previos = empatados[: len(empatados) // 2]
    r = ex.accumulate(textos, seleccion_anterior=previos)
    assert set(previos) <= set(r["nodes"])
    assert not (set(empatados) - set(previos)) & set(r["nodes"])


def test_fuera_de_empate_manda_el_dato():
    """Precedente con términos claramente fuera del corte: no los conserva."""
    ex = NodeExtractorService(top_k=32)
    textos = _caso09()
    reg = ex.accumulate(textos)["registro_borde"]
    lejos = [d["termino"] for d in reg if d["distancia_al_corte"] < -1e-6][:5]
    r = ex.accumulate(textos, seleccion_anterior=lejos)
    assert not set(lejos) & set(r["nodes"])


def test_registro_borde_es_continuo_y_completo():
    ex = NodeExtractorService(top_k=32)
    r = ex.accumulate(_caso09(), seleccion_anterior=["gun"])
    claves = {"termino", "score", "distancia_al_corte", "pertenencia_anterior"}
    assert r["registro_borde"] and all(set(d) == claves for d in r["registro_borde"])
    assert all(isinstance(d["distancia_al_corte"], float) for d in r["registro_borde"])


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
    """Términos de contenido: los de antes ("one", "now", "here", "someone")
    pasaron a ser stopwords con la lista ampliada."""
    ex = NodeExtractorService()
    sig = ex.evaluate("gunfire and weapons downtown", ["gun", "arm", "gunfire"])
    assert list(sig) == [-1.0, -1.0, 1.0]
