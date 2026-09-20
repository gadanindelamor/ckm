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
from collections import defaultdict
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

class NodeExtractorService:
    """
    Stateless. Cada método puede llamarse de forma independiente.

    accumulate_mode:
        Dado un corpus de textos, extrae los términos más relevantes (nodos)
        y los pares que co-ocurren en el mismo texto.

    evaluate_mode:
        Dado un texto y una lista de nodos conocidos, devuelve σ ∈ {+1,-1}^N.
    """

    def __init__(self, top_k: int = 20, ngram_max: int = 2, window: int = 1):
        """
        top_k    — cuántos términos retener como nodos candidatos
        ngram_max — máximo largo de n-grama (1=unigramas, 2=bigramas)
        window   — no usado aún; reservado para ventana de co-ocurrencia intra-texto
        """
        self.top_k     = top_k
        self.ngram_max = ngram_max

    def _vectorizer(self, **extra) -> TfidfVectorizer:
        """
        Único lugar donde se define cómo se reconoce un término.

        accumulate() lo ajusta sobre el corpus; evaluate() usa su analizador
        sobre el texto. Las dos ramas no pueden volver a divergir: antes
        evaluate buscaba substring crudo ("now" dentro de "know") mientras W
        salía de esta tokenización. TASK_extraccion_una_rama_v1.
        """
        return TfidfVectorizer(
            ngram_range   = (1, self.ngram_max),
            stop_words    = list(_STOPWORDS),
            token_pattern = r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ_][a-záéíóúüñA-ZÁÉÍÓÚÜÑ_]{2,}",
            **extra,
        )

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
            }
        """
        if not texts:
            return {"nodes": [], "pairs": {}, "node_freq": {}}
        n_original = len(texts)
        idx_orig   = [k for k, t in enumerate(texts) if t and t.strip()]
        texts      = [texts[k] for k in idx_orig]
        if not texts:
            return {"nodes": [], "pairs": {}, "node_freq": {}}

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
