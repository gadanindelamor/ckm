"""
test_declaracion_extraccion.py — CP1 de TASK_declaracion_extraccion_v1

**CKM no extrae nodos ni tokeniza** (delamor, 14 oct): mide la geometría de lo
que le entra. La extracción, la tokenización y el signo **se declaran**, y la
declaración **viaja en la traza**. Así la dependencia queda adentro de la
afirmación —*"con W producida así, pasa esto"*— en vez de escondida debajo.

Lo que el CP0 encontró invisible y este test exige que esté: `ngram_max` y
`top_k`, el **hash** de las dos listas largas, los defaults de TF-IDF, las
versiones de sklearn y de Python, y la fórmula de W.

Y lo que el CP0 encontró peor: había **una** declaración por estado, suelta de
la W. Ahora cada marca de `w_version` dice con cuál se produjo **su** W.

El último test es el que importa para el paper: **la declaración que produce el
código coincide con `docs/defs/DECLARACION_extraccion_W_v2.md`**. Si no
coinciden, se corrige **el documento** —no el extractor— y se reporta
(regla 2 de la TASK).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
from services.corpus_service import CorpusService          # noqa: E402

# La canónica es la **v2** desde el 18 oct (CP1 de la Serie 2). La v1
# queda en el repo como traza del 14 oct y no se edita.
DOC = RAIZ / "docs" / "defs" / "DECLARACION_extraccion_W_v2.md"

TEXTOS = [
    "gun control reduces violence and saves lives in urban areas",
    "the second amendment protects the right to bear arms",
    "background checks do not stop criminals from getting weapons",
    "assault weapons bans reduce mass shootings and gun violence",
]


@pytest.fixture
def corpus(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3, top_k=6)
    c.ingest(TEXTOS)
    assert c.get_W() is not None, "el fixture no construyó W: el test no mide nada"
    return c


# ---------------------------------------------------------------------------
# Los 8 operadores, y lo que antes era invisible
# ---------------------------------------------------------------------------

def test_los_ocho_operadores(corpus):
    ops = corpus.declaracion_extraccion()["operadores"]
    assert list(ops) == [
        "1_normalizacion", "2_tokenizacion", "3_filtrado", "4_ngramas",
        "5_seleccion", "6_presencia", "7_signo", "8_W",
    ]
    for nombre, op in ops.items():
        assert op["que_hace"], f"{nombre} no dice qué hace"
        assert "referencia" in op, f"{nombre} no tiene campo de referencia"


def test_lo_que_el_cp0_encontro_invisible(corpus):
    """`ngram_max`, `top_k`, los hashes, los defaults, las versiones y W."""
    d = corpus.declaracion_extraccion()

    assert d["parametros_del_servicio"] == {"top_k": 6, "ngram_max": 2,
                                            "min_df": 2}

    # las dos listas largas: hash, no sólo conteo
    assert len(d["perfil"]["stopwords_hash"]) == 64
    assert d["perfil"]["n_stopwords"] == 703
    assert len(d["operadores"]["7_signo"]["parametros"]["hash"]) == 64
    assert d["operadores"]["7_signo"]["parametros"]["n_marcadores"] == 44

    defaults = d["operadores"]["5_seleccion"]["parametros"]["tfidf_defaults"]
    assert defaults == {"smooth_idf": True, "norm": "l2",
                        "use_idf": True, "sublinear_tf": False}
    assert d["operadores"]["5_seleccion"]["parametros"]["max_features"] == 6 * 3

    assert set(d["entorno"]) == {"python", "sklearn", "numpy"}
    assert all(d["entorno"].values())

    w = d["operadores"]["8_W"]["parametros"]
    assert w["conteo_por_unidad"] == 1
    assert w["diagonal"] == 0.0
    assert "max" in w["normalizacion"]

    assert d["productor"]["sha_fuente"].keys() == {
        "node_extractor.py", "corpus_service.py"}


def test_el_perfil_no_se_duplica(corpus, tmp_path):
    """
    El perfil de idioma (S0b) es **una parte** de la declaración, y no hay una
    segunda copia suelta en el estado.
    """
    estado = json.loads(Path(corpus.storage_path).read_text())
    assert "perfil_extraccion" not in estado
    decl = estado["declaraciones"][estado["declaracion_sha"]]
    assert decl["perfil"]["nombre"] == "es_en_v1"
    # el conteo y el origen de las stopwords viven SÓLO en el perfil
    assert "stopwords" not in decl


# ---------------------------------------------------------------------------
# Atada al sha256 de W
# ---------------------------------------------------------------------------

def test_cada_marca_de_w_dice_bajo_que_declaracion_se_produjo(corpus):
    estado = json.loads(Path(corpus.storage_path).read_text())
    marcas = estado["w_version_history"]
    assert marcas, "sin marcas no se mide nada"
    for m in marcas:
        assert m["declaracion_sha"] in estado["declaraciones"]


def test_la_declaracion_se_guarda_una_vez_por_sha(corpus):
    """Dos W bajo la misma declaración no la guardan dos veces."""
    corpus.ingest(["mental health is the real cause of gun violence"])
    corpus.ingest(["assault rifles are weapons of war however they persist"])
    estado = json.loads(Path(corpus.storage_path).read_text())
    assert len(estado["w_version_history"]) > 1
    assert len(estado["declaraciones"]) == 1


def test_una_W_sin_declaracion_queda_marcada_como_tal(tmp_path):
    """
    Un estado anterior al CP1 carga con `declaracion_sha: None` en sus marcas:
    **no se sabe** bajo qué condición se produjo esa W. **Nunca se completa
    con la de hoy** (I2).
    """
    viejo = {
        "texts": list(TEXTOS),
        "nodes": ["gun", "violence"],
        "W": [[0.0, 1.0], [1.0, 0.0]],
        "w_version_history": [{
            "timestamp": 1.0, "sha256": "abc", "corpus_size": 4,
            "causal_event": "rebuild",
        }],
        "forced_w_pos": False,
        "registro_borde": [],
    }
    ruta = tmp_path / "viejo.json"
    ruta.write_text(json.dumps(viejo))

    c = CorpusService(storage_path=str(ruta), min_texts=99)   # min_texts alto: no reconstruye
    assert c._declaraciones == {}
    assert c._declaracion_sha is None
    assert c._w_versions.history()[0].declaracion_sha is None
    assert c._w_versions.current_declaracion_sha() is None


# ---------------------------------------------------------------------------
# La declaración del código contra el documento canónico
# ---------------------------------------------------------------------------

def _doc() -> str:
    assert DOC.exists(), f"falta la declaración canónica: {DOC}"
    return DOC.read_text(encoding="utf-8")


def test_el_codigo_dice_lo_mismo_que_el_documento(corpus):
    """
    Los valores verificables se leen **del documento** y se comparan con los
    que produce el código. Si no coinciden: se corrige el documento, se
    reporta, y el extractor **no se toca**.
    """
    doc = _doc()
    d   = corpus.declaracion_extraccion()

    # operador 2 — el patrón, tal cual está escrito en el documento
    patron_doc = re.search(r"`(\[\^\\W\\d\][^`]*)`", doc).group(1)
    assert d["perfil"]["token_pattern"] == patron_doc

    # operador 2 — el largo mínimo
    largo_doc = int(re.search(r"≥ (\d+) caracteres de palabra", doc).group(1))
    assert d["perfil"]["largo_minimo"] == largo_doc

    # operador 3 — el tamaño de la lista
    s_doc = int(re.search(r"\|S\| = (\d+)", doc).group(1))
    assert d["perfil"]["n_stopwords"] == s_doc

    # operador 7 — cuántos marcadores
    marcadores_doc = int(re.search(r"(\d+) marcadores", doc).group(1))
    assert d["operadores"]["7_signo"]["parametros"]["n_marcadores"] == marcadores_doc

    # operador 1 — la forma Unicode
    assert "NFC" in doc and d["perfil"]["normalizacion"] == "NFC"

    # operador 5 — los defaults que el documento nombra
    assert "`smooth_idf=True`" in doc and "`norm=\"l2\"`" in doc
    defaults = d["operadores"]["5_seleccion"]["parametros"]["tfidf_defaults"]
    assert defaults["smooth_idf"] is True and defaults["norm"] == "l2"
    assert "`max_features`" in doc
    assert d["operadores"]["5_seleccion"]["parametros"]["max_features"] == \
        d["parametros_del_servicio"]["top_k"] * 3

    # operador 5 — el pool con ≤ top_k términos, declarado en los dos lados
    # (hueco cerrado el 21 oct 2026: la rama existía en el código y el
    # documento nombraba sólo los empates y el N = 0)
    assert "N = |pool| < top_k" in doc
    assert "N = |pool| < top_k" in \
        d["operadores"]["5_seleccion"]["que_hace"]

    # operador 8 — la diagonal y el conteo por unidad
    assert "Wᵢᵢ = 0" in doc
    assert d["operadores"]["8_W"]["parametros"]["diagonal"] == 0.0
    assert "cada par cuenta 1 por unidad" in doc
    assert d["operadores"]["8_W"]["parametros"]["conteo_por_unidad"] == 1


def test_la_condicion_declarada_del_signo_esta_en_los_dos_lados(corpus):
    """
    **Se dio vuelta con la v2** (18 oct). La divergencia (b) del CP0 —
    `_has_opposition` no normalizaba a NFC— se **declaraba** en la v1 por
    decisión de delamor. En la v2 se corrigió, junto con la subcadena, y lo
    que tiene que estar en los dos lados es la condición **nueva**: palabra
    completa y NFC.
    """
    doc = _doc()
    assert "palabra completa" in doc
    assert "**normalizado a NFC**" in doc
    cond = corpus.declaracion_extraccion()["operadores"]["7_signo"]["condicion_declarada"]
    assert "palabra completa" in cond
    assert "NFC" in cond and "ASCII" in cond


def test_la_declaracion_apunta_al_documento(corpus):
    assert corpus.declaracion_extraccion()["referencia"] == \
        "docs/defs/DECLARACION_extraccion_W_v2.md"
