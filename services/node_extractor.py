"""
node_extractor.py — NodeExtractorService

Dispositivo MIND, stateless.
Transforma texto en co-activaciones para CorpusService / MonitorService.

Dos modos:
  accumulate(texts)        → pares (nodo_i, nodo_j) co-ocurrentes + conteos
  evaluate(text, nodes)    → σ ∈ {+1,-1}^N sobre nodos conocidos

Sin LLM. Sin estado entre llamadas.
"""

from __future__ import annotations
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# ---------------------------------------------------------------------------
# Stopwords ES + EN mínimas para el dominio
# ---------------------------------------------------------------------------
# Stopwords ES + EN
#
# 703 términos: union de NLTK 3.10.3 spanish (313) y english
# (198), sklearn ENGLISH_STOP_WORDS (318) y las
# 112 minimas que tenia el proyecto. Embebidas: sin dependencia en
# runtime. Decision de delamor (sep 2026) al medir el corpus de informes, donde
# 9 de 32 nodos eran palabras funcion en castellano (sin, sobre, desde, entre,
# cuando, antes...). Quedan afuera de toda lista estandar: "puede", "solo",
# "dos", "hacia" — extension propia NO adoptada.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Cómo se reconoce un término — DECLARADO ACÁ, no delegado a la librería
# ---------------------------------------------------------------------------
# S0 del CP-S (`TASK_node_extractor_regla_v1`, 13 oct). Hasta acá el
# `token_pattern`, las stopwords, el `ngram_range` y el `lowercase` se los
# pasaba a `TfidfVectorizer` y los aplicaba sklearn. Ahora el analizador es
# propio, y por eso **sklearn ignoraria esos cuatro parametros**: dejarlos
# puestos emite cuatro warnings y no hace nada. Pasan a ser declaraciones de
# este modulo (CP0a: siete filas se mueven de "default de libreria" a
# "declarado").
#
# **S0 NO CAMBIA NINGUN COMPORTAMIENTO.** Reproduce lo que hacia sklearn, bit a
# bit, incluido el orden de la lista. Lo que venga despues cambia *adentro* del
# analizador.
#
# El `_` esta DENTRO de la clase de caracteres, y eso importa: hay nodos que
# dependen de el (`delta_r`, `d_ckm`, `operador_stop_coco` estan en el pool de
# ARM40). Sacarlo partiria esos terminos.
#
# S1 del CP-S (13 oct): **cualquier letra Unicode**, en vez de la lista
# ES+EN que habia. `[^\W\d]` es "caracter de palabra que no es digito", o sea
# **letra de cualquier alfabeto, o `_`**. El patron anterior era
#
#     [a-záéíóúüñA-ZÁÉÍÓÚÜÑ_][a-záéíóúüñA-ZÁÉÍÓÚÜÑ_]{2,}
#
# y **no rechazaba lo que no entraba: lo TRUNCABA, en silencio**. `"português"`
# salia `"portugu"`, `"ação"` desaparecia, y `"informacion"` en NFD salia
# `"informacio"` porque el acento combinante cortaba el token. Un termino
# truncado **no es un termino que no entro**: es un nodo distinto, que nadie
# declaro, con la forma de un nodo legitimo.
#
# **El largo minimo (3) NO se toca** (delamor, 13 oct): las palabras de dos
# letras son **definicion de nodo**, y eso no es de este paso.
# (el patron vive en el perfil desde S0b; ver PERFIL_ES_EN)

_STOPWORDS = {
    "a", "about", "above", "across", "after", "afterwards", "again",
    "against", "ain", "al", "algo", "algunas", "algunos", "all", "almost",
    "alone", "along", "already", "also", "although", "always", "am",
    "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "ante", "antes", "any", "anyhow", "anyone", "anything", "anyway",
    "anywhere", "are", "aren", "aren't", "around", "as", "at", "back", "be",
    "became", "because", "become", "becomes", "becoming", "been", "before",
    "beforehand", "behind", "being", "below", "beside", "besides",
    "between", "beyond", "bill", "both", "bottom", "but", "by", "call",
    "can", "cannot", "cant", "co", "como", "con", "contra", "could",
    "couldn", "couldn't", "couldnt", "cry", "cual", "cuando", "d", "de",
    "del", "describe", "desde", "detail", "did", "didn", "didn't", "do",
    "does", "doesn", "doesn't", "doing", "don", "don't", "donde", "done",
    "down", "due", "durante", "during", "e", "each", "eg", "eight",
    "either", "el", "eleven", "ella", "ellas", "ellos", "else", "elsewhere",
    "empty", "en", "enough", "entre", "era", "erais", "eran", "eras",
    "eres", "es", "esa", "esas", "ese", "eso", "esos", "esta", "estaba",
    "estabais", "estaban", "estabas", "estad", "estada", "estadas",
    "estado", "estados", "estamos", "estando", "estar", "estaremos",
    "estará", "estarán", "estarás", "estaré", "estaréis", "estaría",
    "estaríais", "estaríamos", "estarían", "estarías", "estas", "este",
    "estemos", "esto", "estos", "estoy", "estuve", "estuviera",
    "estuvierais", "estuvieran", "estuvieras", "estuvieron", "estuviese",
    "estuvieseis", "estuviesen", "estuvieses", "estuvimos", "estuviste",
    "estuvisteis", "estuviéramos", "estuviésemos", "estuvo", "está",
    "estábamos", "estáis", "están", "estás", "esté", "estéis", "estén",
    "estés", "etc", "even", "ever", "every", "everyone", "everything",
    "everywhere", "except", "few", "fifteen", "fifty", "fill", "find",
    "fire", "first", "five", "for", "former", "formerly", "forty", "found",
    "four", "from", "front", "fue", "fuera", "fuerais", "fueran", "fueras",
    "fueron", "fuese", "fueseis", "fuesen", "fueses", "fui", "fuimos",
    "fuiste", "fuisteis", "full", "further", "fuéramos", "fuésemos", "get",
    "give", "go", "ha", "habida", "habidas", "habido", "habidos",
    "habiendo", "habremos", "habrá", "habrán", "habrás", "habré", "habréis",
    "habría", "habríais", "habríamos", "habrían", "habrías", "habéis",
    "había", "habíais", "habíamos", "habían", "habías", "had", "hadn",
    "hadn't", "han", "has", "hasn", "hasn't", "hasnt", "hasta", "have",
    "haven", "haven't", "having", "hay", "haya", "hayamos", "hayan",
    "hayas", "hayáis", "he", "he'd", "he'll", "he's", "hemos", "hence",
    "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers",
    "herself", "him", "himself", "his", "how", "however", "hube", "hubiera",
    "hubierais", "hubieran", "hubieras", "hubieron", "hubiese", "hubieseis",
    "hubiesen", "hubieses", "hubimos", "hubiste", "hubisteis", "hubiéramos",
    "hubiésemos", "hubo", "hundred", "i", "i'd", "i'll", "i'm", "i've",
    "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "isn",
    "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "just", "keep",
    "la", "las", "last", "latter", "latterly", "le", "least", "les", "less",
    "ll", "lo", "los", "ltd", "m", "ma", "made", "many", "may", "me",
    "meanwhile", "mi", "might", "mightn", "mightn't", "mill", "mine", "mis",
    "more", "moreover", "most", "mostly", "move", "much", "mucho", "muchos",
    "must", "mustn", "mustn't", "muy", "my", "myself", "más", "mí", "mía",
    "mías", "mío", "míos", "nada", "name", "namely", "needn", "needn't",
    "neither", "never", "nevertheless", "next", "ni", "nine", "no",
    "nobody", "none", "noone", "nor", "nos", "nosotras", "nosotros", "not",
    "nothing", "now", "nowhere", "nuestra", "nuestras", "nuestro",
    "nuestros", "o", "of", "off", "often", "on", "once", "one", "only",
    "onto", "or", "os", "other", "others", "otherwise", "otra", "otras",
    "otro", "otros", "our", "ours", "ourselves", "out", "over", "own",
    "para", "part", "per", "perhaps", "pero", "please", "poco", "por",
    "porque", "put", "que", "quien", "quienes", "qué", "rather", "re", "s",
    "same", "se", "sea", "seamos", "sean", "seas", "see", "seem", "seemed",
    "seeming", "seems", "sentid", "sentida", "sentidas", "sentido",
    "sentidos", "ser", "seremos", "serious", "será", "serán", "serás",
    "seré", "seréis", "sería", "seríais", "seríamos", "serían", "serías",
    "several", "seáis", "shan", "shan't", "she", "she'd", "she'll", "she's",
    "should", "should've", "shouldn", "shouldn't", "show", "si", "side",
    "siente", "sin", "since", "sincere", "sintiendo", "six", "sixty", "so",
    "sobre", "sois", "some", "somehow", "someone", "something", "sometime",
    "sometimes", "somewhere", "somos", "son", "soy", "still", "su", "such",
    "sus", "suya", "suyas", "suyo", "suyos", "system", "sí", "t", "take",
    "también", "tanto", "te", "ten", "tendremos", "tendrá", "tendrán",
    "tendrás", "tendré", "tendréis", "tendría", "tendríais", "tendríamos",
    "tendrían", "tendrías", "tened", "tenemos", "tenga", "tengamos",
    "tengan", "tengas", "tengo", "tengáis", "tenida", "tenidas", "tenido",
    "tenidos", "teniendo", "tenéis", "tenía", "teníais", "teníamos",
    "tenían", "tenías", "than", "that", "that'll", "the", "their", "theirs",
    "them", "themselves", "then", "thence", "there", "thereafter",
    "thereby", "therefore", "therein", "thereupon", "these", "they",
    "they'd", "they'll", "they're", "they've", "thick", "thin", "third",
    "this", "those", "though", "three", "through", "throughout", "thru",
    "thus", "ti", "tiene", "tienen", "tienes", "to", "todo", "todos",
    "together", "too", "top", "toward", "towards", "tu", "tus", "tuve",
    "tuviera", "tuvierais", "tuvieran", "tuvieras", "tuvieron", "tuviese",
    "tuvieseis", "tuviesen", "tuvieses", "tuvimos", "tuviste", "tuvisteis",
    "tuviéramos", "tuviésemos", "tuvo", "tuya", "tuyas", "tuyo", "tuyos",
    "twelve", "twenty", "two", "tú", "un", "una", "unas", "under", "uno",
    "unos", "until", "up", "upon", "us", "ve", "very", "via", "vosotras",
    "vosotros", "vuestra", "vuestras", "vuestro", "vuestros", "was", "wasn",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "well", "were",
    "weren", "weren't", "what", "whatever", "when", "whence", "whenever",
    "where", "whereafter", "whereas", "whereby", "wherein", "whereupon",
    "wherever", "whether", "which", "while", "whither", "who", "whoever",
    "whole", "whom", "whose", "why", "will", "with", "within", "without",
    "won", "won't", "would", "wouldn", "wouldn't", "y", "ya", "yet", "yo",
    "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "él", "éramos",
}


# ---------------------------------------------------------------------------
# EL PERFIL DE IDIOMA — los criterios que dependen de la lengua, en UN lugar
# ---------------------------------------------------------------------------
# S0b del CP-S (`TASK_node_extractor_regla_v1`, 13 oct). delamor: *"identificar
# los criterios que dependen de esa declaracion. Aislarlos de alguna forma
# simple, de manera que no se tomen como invariantes."*
#
# Estaban sueltos por el modulo y se leian como si fueran propiedades del
# instrumento. **No lo son: son una declaracion sobre el idioma del corpus.**
# Juntarlos no los hace verdaderos; los hace **visibles y citables**, y le da a
# cada salida la condicion bajo la cual se extrajo.
#
# **NO SE DETECTA EL IDIOMA.** El perfil no valida nada: un corpus en chino se
# extrae igual, con este perfil declarado encima. **El perfil no protege:
# declara.** Comparar el perfil con el corpus es de otro orden.


@dataclass(frozen=True)
class PerfilDeIdioma:
    """
    Los criterios de extraccion que **dependen del idioma**, declarados juntos.

    Inmutable a proposito: si alguien necesita otros criterios, declara **otro
    perfil**, y entonces la diferencia queda escrita en vez de quedar en un
    valor cambiado a mano.

    - `nombre` — como se lo cita. Viaja en la salida y en `save()`.
    - `alcance` — **hasta donde vale**, en palabras. Lo que esta afuera del
      alcance no es "invalido": es **no se sabe**.
    - `token_pattern` — que cuenta como un termino.
    - `largo_minimo` — cuantos caracteres. **Declarado aparte del patron**
      aunque salga de el, porque es una decision propia: en ES y EN las
      palabras de menos de 3 letras son casi siempre funcion, **en otras
      lenguas no**.
    - `lowercase` — si plegar mayusculas. Supone que no pierde significado;
      hay escrituras **sin caja**, y el turco tiene la `i` con y sin punto.
    - `normalizacion` — la forma Unicode canonica, o `None` si no se normaliza.
    - `stopwords` / `stopwords_origen` — la lista y **de donde salio**.
    - `separador_de_palabras` — **lo que el patron no matchea**. Estaba por
      omision y no escrito en ningun lado; escribirlo es la mitad del punto.
    """

    nombre                : str
    alcance               : str
    token_pattern         : str
    largo_minimo          : int
    lowercase             : bool
    normalizacion         : Optional[str]
    stopwords             : frozenset
    stopwords_origen      : str
    separador_de_palabras : str

    def __post_init__(self) -> None:
        if not self.nombre or not self.alcance:
            raise ValueError(
                "nombre y alcance son obligatorios: un perfil sin alcance "
                "escrito se vuelve a leer como invariante, que es lo que S0b "
                "viene a sacar"
            )
        if self.largo_minimo < 1:
            raise ValueError("largo_minimo tiene que ser >= 1")
        if not self.stopwords_origen:
            raise ValueError(
                "stopwords_origen es obligatorio: una lista de stopwords sin "
                "de donde salio es un valor sin origen"
            )

    def to_dict(self) -> dict:
        """Lo que viaja en la salida y en `save()`. **La lista entera no**: su
        tamano y su origen, que es lo que hace falta para saber bajo que
        condicion se extrajo."""
        return {
            "nombre"               : self.nombre,
            "alcance"              : self.alcance,
            "token_pattern"        : self.token_pattern,
            "largo_minimo"         : self.largo_minimo,
            "lowercase"            : self.lowercase,
            "normalizacion"        : self.normalizacion,
            "n_stopwords"          : len(self.stopwords),
            "stopwords_origen"     : self.stopwords_origen,
            "separador_de_palabras": self.separador_de_palabras,
        }


PERFIL_ES_EN = PerfilDeIdioma(
    nombre="es_en_v1",
    alcance=(
        "castellano e ingles, alfabeto con espacios. "
        "Fuera de esto: NO SE SABE -- no esta medido ni validado, y la "
        "extraccion corre igual."
    ),
    token_pattern=r"[^\W\d][^\W\d]{2,}",
    largo_minimo=3,
    lowercase=True,
    normalizacion="NFC",
    stopwords=frozenset(_STOPWORDS),
    stopwords_origen=(
        "703: union de NLTK 3.10.3 spanish (313) e english (198), "
        "sklearn ENGLISH_STOP_WORDS (318) y 112 propias del proyecto "
        "(decision de delamor, sep 2026)"
    ),
    separador_de_palabras=(
        "lo que el token_pattern NO matchea: espacios, puntuacion y digitos. "
        "Supone que las palabras van separadas -- chino, japones y tailandes "
        "no lo hacen"
    ),
)

class NodeExtractorService:
    """
    Stateless. Cada método puede llamarse de forma independiente.

    accumulate_mode:
        Dado un corpus de textos, extrae los términos más relevantes (nodos)
        y los pares que co-ocurren en el mismo texto.

    evaluate_mode:
        Dado un texto y una lista de nodos conocidos, devuelve σ ∈ {+1,-1}^N.
    """

    def __init__(self, top_k: int = 20, ngram_max: int = 2, window: int = 1,
                 perfil: "PerfilDeIdioma" = PERFIL_ES_EN):
        """
        top_k    — cuántos términos retener como nodos candidatos
        ngram_max — máximo largo de n-grama (1=unigramas, 2=bigramas)
        window   — no usado aún; reservado para ventana de co-ocurrencia intra-texto
        perfil   — **los criterios que dependen del idioma** (S0b). El default es
                   `PERFIL_ES_EN`, y **el default también es una declaración**: todo
                   lo que se extrajo sin elegir perfil se extrajo bajo ése.
        """
        self.top_k     = top_k
        self.ngram_max = ngram_max
        self.perfil    = perfil
        self._token_re = re.compile(perfil.token_pattern)

    def analizar(self, texto: str) -> List[str]:
        """
        **El analizador. Único lugar donde se define cómo se reconoce un
        término** (S0 del CP-S, 13 oct).

        **S0** reprodujo **bit a bit** lo que hacía `TfidfVectorizer` con
        `analyzer="word"`. **S1 cambia dos cosas adentro, y nada más** (13 oct):
        **normaliza a NFC** antes de tokenizar, y el patrón acepta **cualquier
        letra Unicode**. Ver `_TOKEN_PATTERN`.

        El orden es:

        1. **normalizar a NFC** (S1) + `lowercase` explícito;
        2. **tokenize:** `_TOKEN_RE.findall(texto)`;
        3. **`_word_ngrams`:** saca las stopwords **primero** y **después** arma
           los n-gramas **sobre los que quedaron**.

        **El paso 3 es la causa de que `"control of guns"` dé `"control guns"`**:
        la stopword se va antes de que los bigramas existan, así que `control` y
        `guns` quedan adyacentes. **S1 no lo arregla**, y S0 tampoco lo hacía: el
        arreglo es **S3**, y espera (hay traza que leer antes: C-value, RAKE,
        Nothman et al.). Lo mismo con los **bigramas anidados** (S2) y con el
        **contrato de `accumulate` con corpus vacío** (S4).

        El orden de la lista también se reproduce: **unigramas primero** —los que
        pasaron el filtro— y después los bigramas **en orden de aparición**. No es
        un detalle gratuito: que coincida la **lista** y no sólo el **conjunto** es
        lo que hace verificable el "bit a bit".
        """
        # S1: NFC **antes** de tokenizar. Sin esto, la misma palabra en NFD
        # —`"información"` con tilde combinante— se parte en el acento y sale
        # `"informacio"`: dos nodos distintos para una palabra, segun como
        # vino codificada. El `lower()` va explicito porque con un `analyzer`
        # invocable sklearn **no** aplica su `lowercase`.
        #
        # S0b: los cuatro criterios de abajo —normalizacion, lowercase, patron
        # y stopwords— salen **del perfil**, no de constantes del modulo. Si
        # hacen falta otros, se declara **otro perfil**.
        perfil = self.perfil
        if perfil.normalizacion:
            texto = unicodedata.normalize(perfil.normalizacion, texto)
        if perfil.lowercase:
            texto = texto.lower()
        tokens = self._token_re.findall(texto)
        # las stopwords salen ANTES de armar los n-gramas (sklearn `_word_ngrams`)
        tokens = [w for w in tokens if w not in perfil.stopwords]
        salida = list(tokens)
        for n in range(2, self.ngram_max + 1):
            for i in range(len(tokens) - n + 1):
                salida.append(" ".join(tokens[i:i + n]))
        return salida

    def _vectorizer(self, **extra) -> TfidfVectorizer:
        """
        El vectorizador, con **el analizador propio** (`analizar`).

        `accumulate()` lo ajusta sobre el corpus; `evaluate()` usa su analizador
        sobre el texto. Las dos ramas no pueden volver a divergir: antes
        `evaluate` buscaba substring crudo (`"now"` dentro de `"know"`) mientras W
        salía de esta tokenización. `TASK_extraccion_una_rama_v1`.

        **No se le pasan `ngram_range`, `stop_words`, `token_pattern` ni
        `lowercase`:** con un `analyzer` invocable sklearn **los ignora** y emite
        un warning por cada uno. Los cuatro viven ahora en `analizar` y en las
        constantes del módulo. Lo que **sigue** siendo de la librería es el resto
        —`norm="l2"`, `smooth_idf`, `use_idf`, `min_df`/`max_df`,
        `sublinear_tf`—, y eso está en la tabla del CP0a.
        """
        return TfidfVectorizer(analyzer=self.analizar, **extra)

    # ------------------------------------------------------------------
    # Modo acumulación
    # ------------------------------------------------------------------

    # Tolerancia DE LA REGLA de desempate (no del registro): dos puntajes a
    # esta distancia del corte son indistinguibles para el criterio.
    TOL_EMPATE = 1e-12

    def accumulate(
        self,
        texts: List[str],
        seleccion_anterior: Optional[List[str]] = None,
    ) -> Dict:
        """
        Extrae nodos y co-activaciones desde un corpus de textos.

        Selección: top_k por TF-IDF medio, dentro de los top_k·3 más
        frecuentes. En el borde del top_k, un empate es indecidible con el
        propio criterio; se resuelve con la regla de la relajación (h = 0 →
        conserva el estado): con seleccion_anterior, un término empatado en el
        borde conserva su pertenencia; sin ella (bootstrap: el estado inicial
        es "ningún nodo") los empatados quedan afuera. N puede diferir de
        top_k. TASK_desempate_seleccion_nodos_v1.

        Returns:
            {
              "nodes":  [str, ...]          — seleccionados, orden por puntaje
              "pairs":  {(ni, nj): count}   — pares que co-ocurren en mismo texto
              "node_freq": {str: int}       — frecuencia por nodo
              "pairs_by_text": [dict, ...]  — pares por texto, alineado
              "registro_borde": [dict, ...] — por término del pool: score,
                    distancia_al_corte (con signo), pertenencia_anterior.
                    Continuo: no guarda categorías; "empate" se deriva al
                    leer, con la tolerancia que se elija entonces.
              "perfil": dict                — **bajo qué condición se extrajo**
                    (S0b): nombre, alcance, y los criterios que dependen del
                    idioma. Va en **las tres** salidas, también en las vacías.
                    No se detecta el idioma: se declara.
            }
        """
        if not texts:
            return {"nodes": [], "pairs": {}, "node_freq": {},
                    "perfil": self.perfil.to_dict()}
        n_original = len(texts)
        idx_orig   = [k for k, t in enumerate(texts) if t and t.strip()]
        texts      = [texts[k] for k in idx_orig]
        if not texts:
            return {"nodes": [], "pairs": {}, "node_freq": {},
                    "perfil": self.perfil.to_dict()}

        # pool: los top_k·3 términos MÁS FRECUENTES del corpus; de ese pool,
        # los top_k de mayor TF-IDF medio. La selección es "TF-IDF entre los
        # más frecuentes", no TF-IDF sobre todo el vocabulario.
        vec = self._vectorizer(max_features=self.top_k * 3)

        tfidf_matrix = vec.fit_transform(texts)
        terms        = vec.get_feature_names_out()

        mean_scores  = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        nodes, registro = self._seleccionar(terms, mean_scores, seleccion_anterior)
        node_set     = set(nodes)

        # Co-ocurrencias: pares que aparecen en el mismo texto
        pairs: Dict[Tuple[str, str], int] = defaultdict(int)
        node_freq: Dict[str, int]         = defaultdict(int)
        # pares de cada texto entre NODOS GLOBALES — para quien necesite
        # rutear por texto (CorpusService: pos/neg) sin volver a extraer.
        # Volver a llamar accumulate([texto]) hace otro top_k dentro del
        # texto y pierde pares. TASK_pares_por_texto_nodos_globales_v1.
        # alineado con la lista RECIBIDA: textos vacíos quedan con {}.
        pairs_by_text: List[Dict[Tuple[str, str], int]] = [{} for _ in range(n_original)]

        for row_idx in range(tfidf_matrix.shape[0]):
            row      = tfidf_matrix[row_idx]
            active   = [terms[i] for i in row.nonzero()[1] if terms[i] in node_set]
            for node in active:
                node_freq[node] += 1
            del_texto: Dict[Tuple[str, str], int] = {}
            for a, b in combinations(sorted(active), 2):
                pairs[(a, b)] += 1
                del_texto[(a, b)] = 1
            pairs_by_text[idx_orig[row_idx]] = del_texto

        return {
            "nodes"         : nodes,
            "pairs"         : dict(pairs),
            "node_freq"     : dict(node_freq),
            "pairs_by_text" : pairs_by_text,
            "registro_borde": registro,
            # S0b: bajo QUÉ condición se extrajo. Va en las tres salidas,
            # también en las vacías: el perfil rige aunque no salga nada.
            "perfil"        : self.perfil.to_dict(),
        }

    def _seleccionar(self, terms, scores, anterior):
        """
        Top_k con la regla de desempate de la relajación.

        corte = puntaje del top_k-ésimo. Por encima del corte (más allá de
        TOL_EMPATE) entra; por debajo, queda afuera; a distancia ≤ TOL_EMPATE
        del corte es empate: conserva su pertenencia anterior, o queda afuera
        si no hay anterior. Si los empatados caben todos en los lugares que
        quedan, no hay empate que decidir y entran.
        """
        orden = sorted(range(len(terms)), key=lambda i: (-scores[i], terms[i]))
        if len(orden) <= self.top_k:
            elegidos = orden
            corte = scores[orden[-1]] if orden else 0.0
        else:
            corte = scores[orden[self.top_k - 1]]
            arriba = [i for i in orden if scores[i] - corte > self.TOL_EMPATE]
            empate = [i for i in orden if abs(scores[i] - corte) <= self.TOL_EMPATE]
            libres = self.top_k - len(arriba)
            if len(empate) <= libres:
                elegidos = arriba + empate
            elif anterior is None:
                elegidos = arriba
            else:
                prev = set(anterior)
                elegidos = arriba + [i for i in empate if terms[i] in prev]
        prev = set(anterior) if anterior is not None else None
        registro = [
            {
                "termino"             : str(terms[i]),
                "score"               : float(scores[i]),
                "distancia_al_corte"  : float(scores[i] - corte),
                "pertenencia_anterior": (terms[i] in prev) if prev is not None else None,
            }
            for i in orden
        ]
        return [str(terms[i]) for i in elegidos], registro

    # ------------------------------------------------------------------
    # Modo evaluación
    # ------------------------------------------------------------------

    def evaluate(self, text: str, nodes: List[str]) -> np.ndarray:
        """
        Dado un texto y una lista de nodos conocidos, devuelve σ ∈ {+1,-1}^N.

        σ_i = +1 si el nodo_i está entre los términos que produce el
        analizador de accumulate() sobre el texto — misma tokenización,
        mismas stopwords, mismos bigramas. σ_i = -1 si no.
        """
        terminos = set(self._vectorizer().build_analyzer()(text))
        return np.array([1.0 if n in terminos else -1.0 for n in nodes])


# ---------------------------------------------------------------------------
# Test mínimo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    prompts = [
        "gun control reduces violence and saves lives in urban areas",
        "the second amendment protects the right to bear arms against government overreach",
        "background checks and gun laws do not stop criminals from getting weapons",
        "assault weapons bans reduce mass shootings and gun violence statistics",
        "gun rights are constitutional rights that should not be restricted by the government",
        "mental health is the real cause of gun violence not access to firearms",
    ]

    svc    = NodeExtractorService(top_k=12, ngram_max=2)
    result = svc.accumulate(prompts)

    print("=== MODO ACUMULACIÓN ===")
    print(f"Nodos extraídos ({len(result['nodes'])}):")
    for n in result["nodes"]:
        freq = result["node_freq"].get(n, 0)
        print(f"  {n:<30} freq={freq}")

    print(f"\nPares co-ocurrentes ({len(result['pairs'])}):")
    top_pairs = sorted(result["pairs"].items(), key=lambda x: -x[1])[:8]
    for (a, b), cnt in top_pairs:
        print(f"  ({a}, {b})  →  {cnt}")

    print("\n=== MODO EVALUACIÓN ===")
    nodes  = result["nodes"]
    prompt = "gun control laws reduce violence and protect rights"
    sigma  = svc.evaluate(prompt, nodes)
    activos = [nodes[i] for i, s in enumerate(sigma) if s > 0]
    print(f"Prompt: '{prompt}'")
    print(f"Nodos activos ({len(activos)}): {activos}")
