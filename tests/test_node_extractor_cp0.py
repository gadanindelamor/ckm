"""
CP0 de `TASK_node_extractor_regla_v1` — correctitud de **C**

Qué llega como **candidato** a la decisión de `_seleccionar`. Seis puntos, cada uno
con su test chico. **`services/node_extractor.py` no se toca** (gate `f96c234`):
esto mide, no arregla.

## Qué queda `xfail(strict=True)` y qué queda afirmado, y por qué

`xfail` es para **lo que hoy está mal**. "Mal" acá quiere decir: *el instrumento
produce algo que no viene del campo, y decidirlo no es de delamor*. Donde el
veredicto **sí** es de delamor —qué cuenta como un nodo, que es el orden n3 del
CP0a— el test **afirma el comportamiento** y declara de quién es la decisión. No
marco como defecto algo cuya definición todavía no está tomada.

| | qué | cómo queda | por qué |
|---|---|---|---|
| **a** | bigramas anidados → W positiva por construcción | **`xfail` strict** | W deja de salir del campo. No depende de qué es un nodo |
| **b** | bigramas que atraviesan stopwords | **afirmado** | si `"control guns"` es un nodo legítimo es **n3** |
| **c** | NFD y letras fuera del alfabeto → **truncamiento silencioso** | **`xfail` strict** | la misma palabra da dos nodos distintos según cómo venga codificada |
| **d** | 45 stopwords que el `token_pattern` nunca produce | **afirmado** | son **inertes**: no cambian ninguna salida |
| **e** | corpus vacío devuelve 3 claves y no 5 | **`xfail` strict** | el contrato de `accumulate` no es el mismo según la entrada |
| **f** | el pool desempata por **orden alfabético**, sin nombrarlo y sin R | **afirmado** | es un `g` sin nombre: el CP0 lo reporta, no lo corrige |

Medido contra **scikit-learn 1.9.0** (declarada en `pyproject.toml` desde el CP0a;
el `>=` registra un piso, **no** la versión).
"""

import unicodedata

import pytest

from services.node_extractor import NodeExtractorService, _STOPWORDS

SKLEARN_MEDIDA = "1.9.0"


def _analizador(top_k=20, ngram_max=2):
    return NodeExtractorService(top_k=top_k, ngram_max=ngram_max)._vectorizer().build_analyzer()


def test_la_version_contra_la_que_se_midio() -> None:
    """El CP0 (f) y las siete filas de "default de librería" del CP0a dependen de
    la versión. Queda dicho contra cuál se midió; si cambia, este test lo dice."""
    import sklearn
    assert sklearn.__version__ == SKLEARN_MEDIDA, (
        f"medido contra {SKLEARN_MEDIDA}, corre {sklearn.__version__}: "
        "revisar el CP0 (f) y los defaults del CP0a"
    )


# ── a — bigramas anidados ──────────────────────────────────────────────────

def test_a_el_analizador_produce_el_unigrama_y_el_bigrama_del_mismo_texto() -> None:
    """La evidencia, sin juicio: de un texto salen **las dos** formas."""
    t = _analizador()("gun control reduces violence")
    assert "gun" in t and "gun control" in t


@pytest.mark.xfail(strict=True, reason=(
    "CP0 (a): si el unigrama y el bigrama que lo contiene son los dos nodos, "
    "co-ocurren en TODO texto donde está el bigrama. W positiva por construcción, "
    "no por campo. No se arregla acá (gate f96c234)"))
def test_a_el_bigrama_anidado_no_arrastra_a_su_unigrama() -> None:
    """
    **Lo que debería valer y no vale.** Si `"gun"` y `"gun control"` entran los dos
    como nodos, el par `("gun", "gun control")` cuenta **una vez por cada texto que
    tiene el bigrama**: la arista no mide co-ocurrencia de dos cosas, mide que una
    contiene a la otra.
    """
    svc = NodeExtractorService(top_k=6, ngram_max=2)
    textos = [
        "gun control reduces violence in urban areas",
        "gun control laws reduce violence",
        "gun control saves lives",
        "gun control and violence statistics",
    ]
    r = svc.accumulate(textos)
    nodes = set(r["nodes"])
    assert {"gun", "gun control"} <= nodes, "el caso necesita los dos como nodos"

    par = tuple(sorted(("gun", "gun control")))
    n_con_bigrama = sum(1 for t in textos if "gun control" in t)
    # la aserción que falla: el par no debería aparecer en TODOS los textos que
    # tienen el bigrama, porque eso es contención y no co-ocurrencia
    assert r["pairs"].get(par, 0) < n_con_bigrama


# ── b — bigramas que atraviesan stopwords ──────────────────────────────────

def test_b_el_bigrama_atraviesa_la_stopword() -> None:
    """
    **Confirmado.** La stopword se saca **antes** de armar los n-gramas, así que
    `"control of guns"` produce `"control guns"`: un término que **no está en el
    texto**.

    **Afirmado, no marcado como defecto:** si `"control guns"` es un nodo legítimo
    es *qué es un nodo*, el orden **n3** del CP0a, y eso es de delamor.
    """
    t = _analizador()("control of guns")
    assert t == ["control", "guns", "control guns"]
    assert "of" not in " ".join(t)


# ── c — Unicode ────────────────────────────────────────────────────────────

def test_c_la_evidencia_del_truncamiento() -> None:
    """Sin juicio: qué sale. **No rechaza: trunca, y en silencio.**"""
    an = _analizador()
    nfc = "información"
    nfd = unicodedata.normalize("NFD", nfc)
    assert an(nfc + " importante")[0] == "información"
    # el acento combinante corta el token y deja una palabra que no existe
    assert an(nfd + " importante")[0] == "informacio"
    # letras fuera de la clase del token_pattern: lo mismo
    assert _analizador()("ação português naive") == ["portugu", "naive", "portugu naive"]


@pytest.mark.xfail(strict=True, reason=(
    "CP0 (c): NFC y NFD de la misma palabra dan dos nodos distintos, y el de NFD "
    "es una palabra truncada que no existe. El token_pattern asume precompuesto y "
    "strip_accents=None; ninguna de las dos condiciones está declarada (CP0a §3)"))
def test_c_la_misma_palabra_da_el_mismo_nodo_venga_como_venga() -> None:
    """**Lo que debería valer y no vale.** La normalización Unicode del texto de
    entrada no debería cambiar qué nodo sale."""
    an = _analizador()
    nfc = "información"
    assert an(nfc)[0] == an(unicodedata.normalize("NFD", nfc))[0]


# ── d — stopwords que el token_pattern nunca produce ───────────────────────

def test_d_las_45_stopwords_con_apostrofo_son_inertes() -> None:
    """
    **Confirmado, y sin efecto.** 45 de 703 stopwords llevan apóstrofo
    (`"don't"`, `"isn't"`…) y el `token_pattern` **no tiene el apóstrofo en su
    clase**, así que nunca produce un token que las active.

    **Afirmado, no marcado como defecto: son inertes.** No cambian ninguna salida.
    Lo que sí cambia la salida es otra cosa, y queda medida acá: las contracciones
    se pierden igual, pero por el **fragmento** —`"don"`, `"isn"`, `"won"` **sí**
    están en la lista—, no por la entrada con apóstrofo.
    """
    con_apostrofo = {w for w in _STOPWORDS if "'" in w}
    assert len(con_apostrofo) == 45
    assert len(_STOPWORDS) == 703

    an = _analizador()
    # ninguna de las 45 puede salir del analizador
    for w in sorted(con_apostrofo):
        assert w not in an(w), f"{w!r} salió del analizador"
    # y las contracciones desaparecen por el fragmento, no por la entrada
    assert an("don't isn't won't") == []
    assert {"don", "isn", "won"} <= _STOPWORDS


# ── e — corpus vacío ───────────────────────────────────────────────────────

def test_e_la_evidencia_del_contrato_partido() -> None:
    """Sin juicio: qué claves salen en cada caso."""
    svc = NodeExtractorService(top_k=5)
    assert set(svc.accumulate([])) == {"nodes", "pairs", "node_freq"}
    assert set(svc.accumulate(["  ", ""])) == {"nodes", "pairs", "node_freq"}
    assert set(svc.accumulate(["gun control reduces violence"])) == {
        "nodes", "pairs", "node_freq", "pairs_by_text", "registro_borde"}


@pytest.mark.xfail(strict=True, reason=(
    "CP0 (e): con corpus vacío o sólo blancos, accumulate devuelve 3 claves y no "
    "5: faltan pairs_by_text y registro_borde (node_extractor.py:206 y :211). "
    "Quien lee el registro del borde no puede distinguir 'no hubo corpus' de 'no "
    "hubo empate' — I2: la ausencia sin marca"))
def test_e_accumulate_devuelve_el_mismo_contrato_siempre() -> None:
    """**Lo que debería valer y no vale.** Las cinco claves, con el corpus que sea."""
    svc = NodeExtractorService(top_k=5)
    esperado = {"nodes", "pairs", "node_freq", "pairs_by_text", "registro_borde"}
    assert set(svc.accumulate([])) == esperado


# ── f — el pool: el corte por frecuencia y su empate ───────────────────────

def test_f_el_pool_desempata_por_orden_alfabetico_y_no_lo_nombra() -> None:
    """
    **El pool es una segunda decisión, y no tiene R.** `max_features = top_k*3`
    corta por frecuencia; cuando el corte cae sobre un empate, el que entra lo
    decide **el nombre del término**, no el campo.

    Medido con cuatro términos de **frecuencia idéntica** y el corte en 2:

    - **estable contra el orden de los documentos** — el mismo corpus al revés da
      lo mismo, así que no es azar ni orden de inserción;
    - **cambia si el término se escribe distinto** — renombrar `alfa` → `omega` da
      vuelta cuál entra.

    Eso es un **`g` (contexto: orden alfabético) sin nombrar**, exactamente el
    mismo que el CP0 del otro TASK encontró en `_seleccionar`. **Afirmado, no
    marcado como defecto:** el CP0 reporta; corregirlo sería nombrar un `g`, y eso
    no es de Code.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer

    def pool(textos, maxf=2):
        v = TfidfVectorizer(max_features=maxf, token_pattern=r"[a-z]{3,}",
                            stop_words=None, ngram_range=(1, 1))
        v.fit(textos)
        return sorted(v.get_feature_names_out())

    base = ["alfa", "beta", "gama", "zeta"]          # frecuencia 1 cada uno
    assert pool(base) == ["alfa", "beta"]
    assert pool(list(reversed(base))) == ["alfa", "beta"]      # estable al orden
    assert pool(["omega", "beta", "gama", "zeta"]) == ["beta", "gama"]  # al nombre


def test_f_el_pool_no_deja_registro() -> None:
    """La otra mitad del punto (f): el `registro_borde` es **del `_seleccionar`**,
    no del pool. Los términos que el pool dejó afuera **no aparecen en ningún
    lado**: no hay cómo saber cuántos eran ni a qué distancia del corte quedaron."""
    svc = NodeExtractorService(top_k=3, ngram_max=1)
    # quince términos de 4+ letras: ninguno se pierde por el largo mínimo
    textos = ["alfa beta gama delta", "epsilon zeta theta iota",
              "kappa lambda sigma omega", "tango bravo echo"]
    todos = set(_analizador(ngram_max=1)(" ".join(textos)))
    assert len(todos) == 15, "el caso necesita los quince tokenizables"

    r = svc.accumulate(textos)
    # el pool se queda con top_k*3 = 9 de los 15
    assert len(r["registro_borde"]) == 9
    vistos = {x["termino"] for x in r["registro_borde"]}
    fuera = todos - vistos
    assert len(fuera) == 6, "el pool dejó 6 afuera"
    # y ninguno de los 6 deja rastro en la salida
    assert not (fuera & set(r["nodes"]))
    assert all(t not in str(r["registro_borde"]) for t in fuera)
