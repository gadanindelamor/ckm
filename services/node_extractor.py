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
_STOPWORDS = {
    # ES
    "el","la","los","las","un","una","unos","unas","de","del","al","a","en",
    "y","e","o","que","con","por","para","es","son","se","su","sus","lo",
    "no","si","más","pero","como","este","esta","estos","estas","ese","esa",
    "esos","esas","ser","hay","tiene","tienen","está","están","fue","han",
    "les","le","me","te","nos","yo","él","ella","ellos","ellas","ser","una",
    # EN
    "the","a","an","of","in","and","or","to","is","are","was","were","be",
    "it","its","this","that","these","those","for","on","with","as","at",
    "by","from","not","but","have","has","had","do","does","did","will",
    "can","could","would","should","may","might","i","you","he","she","we",
    "they","their","there","what","which","who","how","when","where","than",
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
