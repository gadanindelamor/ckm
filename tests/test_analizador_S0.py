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


# Los tres textos que **S1 arregla**: el analizador viejo los truncaba. Van
# aparte porque el bit a bit contra la copia congelada ya NO vale para ellos —y
# eso es el resultado de S1, no una falla del test.
ARREGLADOS_POR_S1 = [
    # letras fuera del alfabeto ES+EN del patrón viejo: ç, ã, ê
    "ação português naive",
    # la MISMA palabra en NFD: el acento combinante cortaba el token
    unicodedata.normalize("NFD", "información") + " importante",
]

# Textos de borde donde el analizador de hoy sigue coincidiendo **bit a bit** con
# el viejo. Todo lo que S1 no toca — incluido el castellano en **NFC**: el patrón
# viejo tenía las tildes españolas en su clase, así que `"información"` precompuesta
# ya salía entera. **Lo que rompía era NFD y las letras de otros alfabetos.**
BORDES = [
    "",
    "información importante",
    "   ",
    "a",
    "ab",
    "abc",
    "Gun Control Reduces Violence",
    "control of guns",
    "control with guns",
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
    """
    **El resultado de S0**, con el alcance que S1 le dejó: la **misma secuencia**
    —no el mismo `set`— en todo lo que **S1 no toca**.

    Los tres textos que S1 **sí** toca están en `ARREGLADOS_POR_S1` y tienen su
    propio test. **Que acá no estén no es que no se midan: es dónde se miden.**
    """
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    assert svc.analizar(texto) == analizador_viejo(2)(texto)


@pytest.mark.parametrize("texto", ARREGLADOS_POR_S1, ids=lambda t: repr(t[:24]))
def test_S1_estos_son_los_que_dejaron_de_coincidir(texto) -> None:
    """**El resultado de S1.** Acá el bit a bit **tiene** que romperse: el viejo
    truncaba y el nuevo no. Si volvieran a coincidir, S1 se habría ido."""
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    assert svc.analizar(texto) != analizador_viejo(2)(texto)


def test_bit_a_bit_sobre_los_cuatro_corpus() -> None:
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
    # y los tres de S1 divergen con cualquier ngram_max
    for t in ARREGLADOS_POR_S1:
        assert svc.analizar(t) != viejo(t), f"ngram_max={ngram_max}: {t[:40]!r}"


# ── Lo que S0 reproduce y NO arregla ──────────────────────────────────────

def test_lo_que_S0_y_S1_NO_arreglan() -> None:
    """
    Las cosas del CP0 que **siguen exactamente igual**. S0 las reprodujo y S1 no
    las toca: el arreglo de (b) es **S3** y espera (C-value, RAKE, Nothman).
    """
    an = NodeExtractorService(top_k=20, ngram_max=2).analizar
    # (b) el bigrama cruza la stopword — sigue, y es S3
    assert an("control of guns") == ["control", "guns", "control guns"]
    # (d) las contracciones se pierden por el FRAGMENTO ("don", "isn", "won"
    #     están en la lista), no por las 45 entradas con apóstrofo
    assert an("don't isn't won't") == []


def test_S1_el_truncamiento_silencioso_se_fue() -> None:
    """
    **El resultado de S1.** El patrón viejo no rechazaba lo que no entraba: lo
    **truncaba**, y un término truncado no es un término que no entró — es un nodo
    distinto, que nadie declaró, con la forma de uno legítimo.
    """
    an = NodeExtractorService(top_k=20, ngram_max=2).analizar
    assert an("ação português naive") == [
        "ação", "português", "naive", "ação português", "português naive"]
    # NFC y NFD de la misma palabra dan el MISMO nodo
    nfc = "información"
    assert an(nfc)[0] == an(unicodedata.normalize("NFD", nfc))[0] == nfc
    # y lo que el patrón viejo producía ya no existe
    viejo = analizador_viejo(2)
    assert viejo("ação português naive")[0] == "portugu"
    assert "portugu" not in an("ação português naive")


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
    """
    Pool idéntico y conjunto de nodos idéntico, con `_seleccionar` sin tocar.

    **Valía para S0 y sigue valiendo para S1, y eso NO era lo predicho.** Ver el
    reporte: predije que los cuatro corpus se movían, con números del scratchpad
    que en realidad eran de S1 **más** S3. **Ninguno de los 83 textos de estos
    corpus tiene una letra fuera del alfabeto viejo ni viene en NFD**, así que S1
    —que es un arreglo real— **no cambia nada acá**.
    """
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


# ── S0b — el perfil de idioma, en UN solo lugar ───────────────────────────

def test_S0b_bit_a_bit_contra_el_analizador_de_antes_del_perfil() -> None:
    """**S0b no cambia comportamiento.** Los criterios se mudaron al perfil y el
    analizador da lo mismo: los bordes, los 83 textos reales y `ngram_max` 1/2/3
    ya lo verifican arriba; acá se fija que el perfil **es** el que rige."""
    from services.node_extractor import PERFIL_ES_EN
    svc = NodeExtractorService(top_k=20, ngram_max=2)
    assert svc.perfil is PERFIL_ES_EN
    assert svc.perfil.normalizacion == "NFC" and svc.perfil.lowercase
    assert svc.perfil.largo_minimo == 3
    assert len(svc.perfil.stopwords) == 703


def test_S0b_otro_perfil_cambia_la_extraccion_y_queda_declarado() -> None:
    """El punto de aislarlos: cambiar un criterio **es declarar otro perfil**, no
    tocar un valor. Y la diferencia queda escrita en la salida."""
    import dataclasses
    from services.node_extractor import PERFIL_ES_EN
    sin_sw = dataclasses.replace(PERFIL_ES_EN, nombre="sin_stopwords",
                                 stopwords=frozenset(),
                                 stopwords_origen="ninguna, a propósito")
    svc = NodeExtractorService(top_k=20, ngram_max=1, perfil=sin_sw)
    assert "the" in svc.analizar("the guns")
    assert svc.accumulate(["the guns here"])["perfil"]["nombre"] == "sin_stopwords"
    # inmutable: no se cambia un criterio en el lugar
    with pytest.raises(dataclasses.FrozenInstanceError):
        PERFIL_ES_EN.lowercase = False


def test_S0b_el_perfil_viaja_en_accumulate_y_se_persiste() -> None:
    """*"No se detecta el idioma: se declara bajo qué condición se extrajo."*"""
    svc = NodeExtractorService(top_k=5)
    for salida in (svc.accumulate([]), svc.accumulate(["  "]),
                   svc.accumulate(["gun control reduces violence"])):
        assert salida["perfil"]["nombre"] == "es_en_v1"
        assert "NO SE SABE" in salida["perfil"]["alcance"]
    # la lista entera NO viaja: su tamaño y su origen, que es lo que hace falta
    d = svc.accumulate([])["perfil"]
    assert d["n_stopwords"] == 703 and "NLTK" in d["stopwords_origen"]
    assert "stopwords" not in d


def test_S0b_ningun_otro_lugar_escribe_esos_criterios_a_mano() -> None:
    """
    **Test estructural**, como el de *"un solo corazón"*. Si aparece un criterio de
    idioma **fuera** del perfil y fuera de la lista congelada, falla.

    Es **textual**: ve los nombres con los que el repo ya los escribe. No ve una
    copia que los renombre, y lo dice para no afirmar más de lo que verifica.
    """
    NEEDLES = ("stop_words", "_STOPWORDS", "strip_accents", "token_pattern",
               ".lower()", "normalize(")
    # Conocidos: se LISTAN, no se tocan acá. Cada uno con su razón.
    CONOCIDOS = {
        "services/node_extractor.py": "ES el perfil: PERFIL_ES_EN y analizar",
        "services/corpus_service.py":
            "_OPPOSITION_MARKERS (ES+EN) y su .lower(): es el CP1b, no S0b",
        "services/behavior_graph.py":
            "_detect: .lower() y \\b sobre BEHAVIOR_TERMAP_V1 en inglés. Listado "
            "en el inventario de S0b, no tocado",
        "iap_chatroom/autonomous_device.py":
            ".lower() sobre el texto de una excepción, para clasificar el error: "
            "no es extracción",
    }
    raiz = Path(__file__).resolve().parent.parent
    hallados = {}
    for carpeta in ("services", "iap_chatroom"):
        for f in sorted((raiz / carpeta).rglob("*.py")):
            rel = f.relative_to(raiz).as_posix()
            if "test" in f.parts or f.name.startswith("test_"):
                continue
            hits = [n for n in NEEDLES if n in f.read_text(errors="replace")]
            if hits:
                hallados[rel] = hits

    nuevos = set(hallados) - set(CONOCIDOS)
    assert not nuevos, (
        f"criterio de idioma fuera del perfil: {sorted(nuevos)}. El perfil vive "
        "en services/node_extractor.py; si es otro sitio, va al inventario de S0b"
    )
    salieron = set(CONOCIDOS) - set(hallados)
    assert not salieron, f"salieron de la lista: {sorted(salieron)}"
    assert all(v for v in CONOCIDOS.values())
