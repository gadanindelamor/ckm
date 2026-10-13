"""
S0 — el analizador propio reproduce el de sklearn **bit a bit**

`TASK_node_extractor_regla_v1`, CP-S, S0. **Sin cambio de comportamiento.** La
predicción está en `f38a146`, commiteada antes del cambio.

## El oráculo

`_ANALIZADOR_VIEJO` es **la configuración de sklearn que había antes de S0**:
`ngram_range=(1, ngram_max)`, `stop_words=list(_STOPWORDS)` y el `token_pattern`
literal de `node_extractor.py` en `25dbaaf`. No es mi lectura de lo que hacía: es
sklearn haciéndolo.

Este oráculo queda para **los tests con números viejos** (decisión de Opus, 13 oct):
los conteos de A.3, de la relajación y del CP1 se midieron con él, y se pueden
seguir verificando contra él aunque el analizador del repo cambie.
"""

import json
import unicodedata
from pathlib import Path

import numpy as np
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer

from services.node_extractor import NodeExtractorService, _STOPWORDS

RAIZ = Path(__file__).resolve().parent.parent
TOKEN_PATTERN_VIEJO = r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ_][a-záéíóúüñA-ZÁÉÍÓÚÜÑ_]{2,}"

CORPUS = {
    "ARM40": RAIZ / "process/experiments/armstrong_replica_seed123_corpus_state.json",
    "A24":   RAIZ / "process/experiments/wmixta_paso2_natural/corpus_natural_uniform.json",
    "D12":   RAIZ / "iap_chatroom/_state/corpus_state.json",
    "E7":    RAIZ / "process/iap/corpus_state.json",
}


def analizador_viejo(ngram_max: int = 2):
    """**La copia congelada**: sklearn con la configuración de `25dbaaf`."""
    return TfidfVectorizer(
        ngram_range=(1, ngram_max),
        stop_words=list(_STOPWORDS),
        token_pattern=TOKEN_PATTERN_VIEJO,
    ).build_analyzer()


# Textos de borde, elegidos para tocar cada cosa que el analizador decide
BORDES = [
    "",
    "   ",
    "a",
    "ab",
    "abc",
    "Gun Control Reduces Violence",
    "control of guns",
    "control with guns",
    "ação português naive",
    "información importante",
    unicodedata.normalize("NFD", "información") + " importante",
    "delta_r d_ckm operador_stop_coco",
    "don't isn't won't",
    "mu nu xi",
    "123 456 abc789",
    "UPPER lower MiXeD",
    "uno",
    "uno dos",
    "**CHANNEL OPEN — PeterPlam Orchestrating**",
    "TinkerBellucio joined the channel",
]


# ── Bit a bit: la misma LISTA, no el mismo conjunto ───────────────────────

@pytest.mark.parametrize("texto", BORDES, ids=lambda t: repr(t[:24]))
def test_la_misma_lista_en_el_mismo_orden(texto) -> None:
    """**El resultado de S0.** No el mismo `set`: **la misma secuencia**."""
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    assert svc.analizar(texto) == analizador_viejo(2)(texto)


def test_bit_a_bit_sobre_los_cuatro_corpus(subtests=None) -> None:
    """Los **textos reales**, uno por uno, no sólo los bordes elegidos."""
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    viejo = analizador_viejo(2)
    total = 0
    for k, ruta in CORPUS.items():
        if not ruta.exists():
            continue
        for t in json.loads(ruta.read_text())["texts"]:
            assert svc.analizar(t) == viejo(t), f"{k}: divergió en {t[:60]!r}"
            total += 1
    assert total >= 80, f"se compararon {total} textos"


@pytest.mark.parametrize("ngram_max", [1, 2, 3])
def test_bit_a_bit_con_otros_ngram_max(ngram_max) -> None:
    """`ngram_max` lo usa el analizador propio; que coincida con sklearn para 1, 2
    y 3 verifica el bucle de n-gramas y no sólo el caso configurado."""
    svc = NodeExtractorService(top_k=20, ngram_max=ngram_max)
    viejo = analizador_viejo(ngram_max)
    for t in BORDES:
        assert svc.analizar(t) == viejo(t), f"ngram_max={ngram_max}: {t[:40]!r}"


# ── Lo que S0 reproduce y NO arregla ──────────────────────────────────────

def test_S0_reproduce_y_no_arregla() -> None:
    """
    Las tres cosas que el CP0 encontró **siguen exactamente igual**. S0 no es el
    arreglo: es el lugar donde el arreglo va a poder hacerse.
    """
    an = NodeExtractorService(top_k=20, ngram_max=2).analizar
    # (b) el bigrama cruza la stopword
    assert an("control of guns") == ["control", "guns", "control guns"]
    # (c) el truncamiento silencioso
    assert an("ação português naive") == ["portugu", "naive", "portugu naive"]
    assert an(unicodedata.normalize("NFD", "información"))[0] == "informacio"
    # (d) las contracciones se pierden por el fragmento
    assert an("don't isn't won't") == []


def test_el_guion_bajo_sigue_adentro_de_la_clase() -> None:
    """El riesgo nombrado en la predicción: hay nodos que dependen del `_`
    (`delta_r`, `d_ckm`, `operador_stop_coco` están en el pool de ARM40). Si el
    analizador lo perdiera, esos términos se partirían."""
    an = NodeExtractorService(top_k=20, ngram_max=1).analizar
    assert an("delta_r d_ckm operador_stop_coco") == [
        "delta_r", "d_ckm", "operador_stop_coco"]


# ── Mismos términos y mismos nodos en los cuatro corpus ───────────────────

@pytest.mark.parametrize("clave", list(CORPUS), ids=list(CORPUS))
def test_mismo_pool_y_mismos_nodos(clave) -> None:
    """Punto 2 de la predicción: pool idéntico y conjunto de nodos idéntico, con
    `_seleccionar` sin tocar."""
    ruta = CORPUS[clave]
    if not ruta.exists():
        pytest.skip(f"corpus ausente: {ruta.name}")
    textos = [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]
    svc = NodeExtractorService(top_k=20, ngram_max=2)

    def corrida(analyzer):
        vec = TfidfVectorizer(analyzer=analyzer, max_features=60)
        M = vec.fit_transform(textos)
        terms = vec.get_feature_names_out()
        sc = np.asarray(M.mean(axis=0)).flatten()
        return list(terms), svc._seleccionar(terms, sc, None)[0]

    t_n, n_n = corrida(svc.analizar)
    t_v, n_v = corrida(analizador_viejo(2))
    assert t_n == t_v, f"{clave}: el pool cambió"
    assert n_n == n_v, f"{clave}: los nodos cambiaron"
    assert (len(t_n), len(n_n)) == {"ARM40": (60, 19), "A24": (60, 20),
                                    "D12": (60, 20), "E7": (55, 12)}[clave]


# ── El vectorizador: una sola rama, y sin warnings ────────────────────────

def test_una_sola_rama_y_sin_warnings() -> None:
    """`evaluate` usa `build_analyzer()` del mismo vectorizador. Con un `analyzer`
    invocable sklearn lo envuelve en su decoder: **se mide que sea equivalente**, no
    se supone (punto 5 de la predicción). Y los cuatro parámetros que sklearn
    ignoraría ya no se pasan: **cero warnings**."""
    import warnings

    svc = NodeExtractorService(top_k=20, ngram_max=2)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        svc._vectorizer(max_features=60).fit(["gun control reduces violence"])
        de_sklearn = [x for x in w if "will not be used" in str(x.message)]
    assert de_sklearn == []

    envuelto = svc._vectorizer().build_analyzer()
    for t in BORDES:
        assert envuelto(t) == svc.analizar(t), f"build_analyzer divergió: {t[:40]!r}"
