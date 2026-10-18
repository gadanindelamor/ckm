"""
test_declaracion_ejecutable.py — CP2 de TASK_declaracion_extraccion_v1

**Un test por operador, con ejemplos chicos fijados acá**, que muestra que el
código hace lo que dice `docs/defs/DECLARACION_extraccion_W_v1.md`.

El CP1 comparó los **valores** declarados (el patrón, 703, 44, los defaults).
Esto corre los **ejemplos**: los que aparecieron el 13–14 oct mirando el
extractor desde abajo, y que son los que alguien va a probar al leer el paper.

Varios de estos ejemplos **no son errores que haya que arreglar**: son
condiciones declaradas. `"control of guns"` da el bigrama `"control guns"`
porque la stopword se va **antes** de armar los n-gramas (S3 lo cambiaría y
está en espera), y `"but"` adentro de `"distribution"` marca oposición porque
la búsqueda es **por subcadena**. Los tests los fijan **como condición**, para
que no se "arreglen" sin decidirlo.

Regla del CP2: si algo acá difiere de la declaración, **se corrige el
documento**, se reporta, y el extractor no se toca.
"""

from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
from services.node_extractor import NodeExtractorService, PERFIL_ES_EN   # noqa: E402
from services.corpus_service import CorpusService                        # noqa: E402


@pytest.fixture
def svc():
    return NodeExtractorService(top_k=20, ngram_max=2)


def tokens(svc, texto):
    """Sólo el operador 2: el patrón, sin filtrado ni n-gramas."""
    return svc._token_re.findall(texto.lower())


# ---------------------------------------------------------------------------
# Operador 1 — normalización
# ---------------------------------------------------------------------------

def test_op1_nfc_y_nfd_dan_el_mismo_token(svc):
    """
    `año` escrito con ñ precompuesta y con n + tilde combinante es **el mismo
    token**. Sin el NFC del operador 1, la forma NFD se parte en el acento y
    sale `ano`: dos nodos para una palabra, según cómo vino codificada.
    """
    nfc = unicodedata.normalize("NFC", "año")
    nfd = unicodedata.normalize("NFD", "año")
    assert nfc != nfd, "el fixture no prueba nada si las dos formas son iguales"
    assert svc.analizar(nfc) == svc.analizar(nfd) == ["año"]


def test_op1_la_enie_pasa_y_ano_es_otro_nodo(svc):
    """`año` y `ano` son nodos distintos: la normalización no pliega la ñ."""
    assert svc.analizar("año") == ["año"]
    assert svc.analizar("ano") == ["ano"]


def test_op1_minusculas():
    uni = NodeExtractorService(top_k=20, ngram_max=1)
    assert uni.analizar("Violencia VIOLENCIA violencia") == ["violencia"] * 3


# ---------------------------------------------------------------------------
# Operador 2 — tokenización
# ---------------------------------------------------------------------------

def test_op2_peter_pan_es_un_token(svc):
    """`_` cuenta como letra: `[^\\W\\d]` acepta todo `\\w` que no sea dígito."""
    assert tokens(svc, "peter_pan") == ["peter_pan"]


def test_op2_co_alinear_pierde_el_co(svc):
    """
    El guion no es carácter de palabra, así que corta. `co` tiene 2 letras y el
    patrón pide 3: **no existe**. Queda `alinear` solo.
    """
    assert tokens(svc, "co-alinear") == ["alinear"]


def test_op2_las_palabras_de_dos_letras_no_existen(svc):
    """1 + 2 = 3 caracteres mínimo, y el largo mínimo está declarado aparte."""
    assert PERFIL_ES_EN.largo_minimo == 3
    assert tokens(svc, "de la el un si no") == []
    assert tokens(svc, "sol") == ["sol"]


def test_op2_las_urls_entran_como_palabras(svc):
    """
    Al nivel del patrón, que es donde el documento lo afirma: la barra, los
    puntos y la arroba cortan como espacios.
    """
    assert tokens(svc, "https://www.x.com/y") == ["https", "www", "com"]
    assert tokens(svc, "x@ejemplo.com") == ["ejemplo", "com"]
    assert tokens(svc, r"C:\Users\pgada") == ["users", "pgada"]


def test_op2_la_barra_corta_como_un_espacio(svc):
    """`sí/no` y `la/el` desaparecen: los cuatro son de 2 letras."""
    assert tokens(svc, "sí/no la/el") == []


def test_op2_lo_que_no_puede_llegar_a_W(svc):
    """Puntuación, guiones sueltos, asteriscos, emojis y dígitos."""
    assert tokens(svc, "... --- *** 🙂 123 4567") == []
    assert tokens(svc, "gun2") == ["gun"]      # el dígito corta, no se incluye


# ---------------------------------------------------------------------------
# Operador 3 — filtrado
# ---------------------------------------------------------------------------

def test_op3_las_stopwords_se_van(svc):
    assert "of" in PERFIL_ES_EN.stopwords
    assert "guns" not in PERFIL_ES_EN.stopwords
    assert svc.analizar("control of guns") == ["control", "guns", "control guns"]


# ---------------------------------------------------------------------------
# Operador 4 — n-gramas
# ---------------------------------------------------------------------------

def test_op4_control_of_guns_da_control_guns(svc):
    """
    **Condición declarada, no bug.** La contigüidad se mide **después** del
    filtrado: `of` se va y `control` y `guns` quedan pegados. Cambiarlo es S3,
    que está en espera (hay traza que leer antes: C-value, RAKE, Nothman).
    """
    assert "control guns" in svc.analizar("control of guns")


def test_op4_una_palabra_corta_no_rompe_la_adyacencia_pero_no_es_nodo(svc):
    """
    La otra cara de lo mismo: una palabra de 2 letras **tampoco** separa,
    porque desaparece antes. Está fijado para que la diferencia con S3 —donde
    el largo mínimo sí va a cortar— quede visible el día que S3 entre.
    """
    assert "control guns" in svc.analizar("control de guns")


def test_op4_el_separador_es_un_espacio_y_es_reversible(svc):
    """Ningún token tiene espacios, así que el bigrama se puede partir."""
    salida = svc.analizar("gun control reduces violence")
    bigramas = [t for t in salida if " " in t]
    assert bigramas == ["gun control", "control reduces", "reduces violence"]
    for b in bigramas:
        for parte in b.split(" "):
            assert parte in salida


def test_op4_ngram_max_1_no_arma_bigramas():
    uni = NodeExtractorService(top_k=20, ngram_max=1)
    assert uni.analizar("control of guns") == ["control", "guns"]


# ---------------------------------------------------------------------------
# Operador 5 — selección
# ---------------------------------------------------------------------------

def test_op5_el_pool_es_top_k_por_tres(svc):
    d = svc.declaracion()["operadores"]["5_seleccion"]["parametros"]
    assert d["max_features"] == d["top_k"] * 3


def test_op5_con_empate_N_puede_no_ser_top_k():
    """
    Declarado en el paso 5. Con textos simétricos los puntajes empatan en el
    borde y, sin selección anterior (bootstrap), los empatados quedan afuera.
    """
    ex = NodeExtractorService(top_k=2, ngram_max=1)
    r = ex.accumulate(["alfa beta", "gama delta"])
    assert len(r["nodes"]) != 2, "sin empate este test no mide la condición"
    assert len(r["nodes"]) < 2


def test_op5_empate_total_en_el_bootstrap_no_da_nodos_ni_W(tmp_path):
    """
    **El caso límite del paso 5, encontrado corriendo el CP2.**

    Si **ningún término queda estrictamente por encima del corte**, el grupo
    empatado **no cabe** en `top_k` y **no hay selección anterior**
    (bootstrap), no entra ninguno: `N = 0`. Y entonces `_rebuild` vuelve antes
    de construir nada, así que **W se queda en `None`**.

    Las tres condiciones son la precisión de delamor (14 oct) sobre la primera
    redacción de Code, que decía *"si el grupo empatado tiene más miembros que
    top_k"*: eso no es lo que decide. `N = len(arriba)`
    (`node_extractor.py:_seleccionar`), así que **N = 0 sólo si `arriba` está
    vacío**.

    No es una falla: es la regla de la relajación (h = 0 conserva, y en el
    bootstrap el estado anterior es "ningún nodo") llevada a su límite. Pasa
    con corpus chicos sin vocabulario compartido, donde todos los términos
    aparecen en un solo texto y tienen el mismo TF-IDF medio.

    El documento decía *"con empates, la cantidad de nodos puede no ser
    top_k"*; **no decía que puede ser 0 y dejar el corpus sin W**. Se corrigió
    el documento (CP2, 14 oct), no el código.
    """
    # las tres condiciones, verificadas y no supuestas.
    #
    # **Con `min_df = 1`** (v2, 18 oct): este corpus **no llega** a la regla de
    # desempate con el `min_df = 2` declarado, porque ningún término aparece en
    # dos textos y el pool queda vacío antes. Son dos caminos distintos al
    # mismo resultado declarado —N = 0, no se construye W— y acá se verifican
    # los dos: primero el desempate, con el `min_df` que lo deja llegar;
    # después el de la v2, abajo.
    sin_vocabulario_comun = [
        "gun control reduces violence in urban areas",
        "however the second amendment protects arms",
        "assault weapons bans reduce mass shootings",
    ]
    ex = NodeExtractorService(top_k=6, min_df=1)
    r  = ex.accumulate(sin_vocabulario_comun)
    reg   = r["registro_borde"]
    tol   = NodeExtractorService.TOL_EMPATE
    arriba = [d for d in reg if d["distancia_al_corte"] > tol]
    empate = [d for d in reg if abs(d["distancia_al_corte"]) <= tol]
    assert arriba == [],              "1) nada estrictamente arriba del corte"
    assert len(empate) > 6,           "2) el grupo empatado no cabe en top_k"
    assert all(d["pertenencia_anterior"] is None for d in reg), "3) bootstrap"
    assert r["nodes"] == []

    # El otro camino, el de la v2: con `min_df = 2` no queda pool, y la salida
    # es **la misma salida vacía**, no un error.
    r2 = NodeExtractorService(top_k=6).accumulate(sin_vocabulario_comun)
    assert r2["nodes"] == []
    assert r2["pairs"] == {}

    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3, top_k=6)
    c.ingest(sin_vocabulario_comun)
    assert c.get_nodes() == []
    assert c.get_W() is None
    # y la traza no inventa una marca de W que no existe
    assert c.w_sha() is None


# ---------------------------------------------------------------------------
# Operador 6 — presencia, 1 por unidad
# ---------------------------------------------------------------------------

def test_op6_cada_par_cuenta_1_por_unidad():
    """
    Aunque los dos términos aparezcan muchas veces en el **mismo** texto, el
    par suma **1**. W cuenta unidades, no repeticiones.
    """
    ex = NodeExtractorService(top_k=4, ngram_max=1)
    repetido = " ".join(["violencia armas"] * 20)
    r = ex.accumulate([repetido, "violencia armas"])
    assert r["pairs"][("armas", "violencia")] == 2    # dos unidades, no 42
    for del_texto in r["pairs_by_text"]:
        assert set(del_texto.values()) <= {1}


def test_op6_sigma_es_mas_uno_o_menos_uno(svc):
    sigma = svc.evaluate("control of guns", ["control", "guns", "violencia"])
    assert list(sigma) == [1.0, 1.0, -1.0]


# ---------------------------------------------------------------------------
# Operador 7 — signo
# ---------------------------------------------------------------------------

def test_op7_but_adentro_de_distribution_YA_NO_marca_oposicion():
    """
    **Se dio vuelta con la declaración v2** (18 oct 2026, CP1 de la Serie 2).

    Hasta la v1 este test fijaba la **subcadena como condición declarada**:
    `but` adentro de `distribution` marcaba oposición, y eso era lo que el
    review v28 (M4) señalaba. La v2 exige **palabra completa**, así que el
    mismo ejemplo ahora da False. **No es que el test se "arregló": cambió la
    condición**, y el test cambia con ella — en el mismo commit que el código
    y que el documento.

    Lo que **no** cambió: el operador 7 sigue sin resultado nulo. La palabra
    completa lo vuelve menos sensible, no falsable.
    """
    assert CorpusService._has_opposition("the distribution is fair") is False
    assert CorpusService._has_opposition("the data is fair") is False
    # y el marcador suelto, que es lo que la v2 sí quiere agarrar
    assert CorpusService._has_opposition("the data is fair but incomplete") is True


def test_op7_el_texto_se_normaliza_a_NFC_igual_que_el_operador_1():
    """
    La otra mitad de la v2. Con los 44 marcadores ASCII de hoy **no cambia
    ningún resultado**, así que lo que se fija es el mecanismo: las dos formas
    Unicode de la misma palabra tienen que dar lo mismo.
    """
    import re as _re
    from services import corpus_service as cs
    nfc = unicodedata.normalize("NFC", "año")
    nfd = unicodedata.normalize("NFD", "año")
    assert nfc != nfd
    original = cs._OPPOSITION_RE
    try:
        cs._OPPOSITION_RE = _re.compile(r"(?<!\w)" + _re.escape(nfc) + r"(?!\w)")
        assert CorpusService._has_opposition(f"hace un {nfd} de esto") is True
    finally:
        cs._OPPOSITION_RE = original


def test_op7_un_marcador_de_verdad_tambien():
    assert CorpusService._has_opposition("no estoy de acuerdo con eso") is True
    assert CorpusService._has_opposition("I disagree") is True


def test_op7_force_w_pos_anula_el_signo(tmp_path):
    # **Vocabulario compartido a propósito** (v2): con `min_df = 2` un corpus
    # donde cada término vive en un solo texto no produce nodos, y entonces no
    # hay W que contrastar. El contraste que este test mide es el del signo,
    # no el del pool.
    textos = [
        "gun control reduces gun violence in urban areas",
        "however gun control in urban areas protects nobody",
        "gun violence in urban areas does not stop but it changes",
    ]
    normal = CorpusService(storage_path=str(tmp_path / "n.json"), min_texts=3, top_k=6)
    normal.ingest(textos)
    forzada = CorpusService(storage_path=str(tmp_path / "f.json"), min_texts=3,
                            top_k=6, force_w_pos=True)
    forzada.ingest(textos)

    assert (normal.get_W() < 0).any(), "sin negativos el contraste no mide nada"
    assert not (forzada.get_W() < 0).any()
    # y queda MARCADA en la traza, para que no se confunda con una W natural
    assert forzada._w_versions.history()[-1].causal_event == "rebuild_debug_force_w_pos"
    assert forzada.declaracion_extraccion()[
        "operadores"]["7_signo"]["parametros"]["force_w_pos"] is True


# ---------------------------------------------------------------------------
# Operador 8 — W
# ---------------------------------------------------------------------------

def test_op8_diagonal_cero_y_rango(tmp_path):
    # vocabulario COMPARTIDO: sin él los puntajes empatan y no hay nodos
    # (ver test_op5_empate_total_en_el_bootstrap_no_da_nodos_ni_W)
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3, top_k=6)
    c.ingest([
        "gun control reduces gun violence",
        "gun control laws and gun rights",
        "violence and gun violence again",
    ])
    W = c.get_W()
    assert (W.diagonal() == 0).all()
    assert W.min() >= -1.0 and W.max() <= 1.0
    assert abs(W).max() == pytest.approx(1.0)   # normalizada por máx|·|
    assert (W == W.T).all()
