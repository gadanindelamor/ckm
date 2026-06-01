"""
node_extractor_dev.py — NodeExtractorService

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
from typing import Dict, List, Tuple

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

    # ------------------------------------------------------------------
    # Modo acumulación
    # ------------------------------------------------------------------

    def accumulate(self, texts: List[str]) -> Dict:
        """
        Extrae nodos y co-activaciones desde un corpus de textos.

        Returns:
            {
              "nodes":  [str, ...]          — top_k términos por TF-IDF
              "pairs":  {(ni, nj): count}   — pares que co-ocurren en mismo texto
              "node_freq": {str: int}       — frecuencia por nodo
            }
        """
        if not texts:
            return {"nodes": [], "pairs": {}, "node_freq": {}}
        texts = [t for t in texts if t and t.strip()]
        if not texts:
            return {"nodes": [], "pairs": {}, "node_freq": {}}

        vec = TfidfVectorizer(
            ngram_range   = (1, self.ngram_max),
            stop_words    = list(_STOPWORDS),
            max_features  = self.top_k * 3,   # pool amplio, luego filtramos
            token_pattern = r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ_][a-záéíóúüñA-ZÁÉÍÓÚÜÑ_]{2,}",
        )

        tfidf_matrix = vec.fit_transform(texts)
        terms        = vec.get_feature_names_out()

        # Top-k por TF-IDF promedio
        mean_scores  = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        top_idx      = np.argsort(mean_scores)[::-1][: self.top_k]
        nodes        = [terms[i] for i in top_idx]
        node_set     = set(nodes)

        # Co-ocurrencias: pares que aparecen en el mismo texto
        pairs: Dict[Tuple[str, str], int] = defaultdict(int)
        node_freq: Dict[str, int]         = defaultdict(int)

        for row_idx in range(tfidf_matrix.shape[0]):
            row      = tfidf_matrix[row_idx]
            active   = [terms[i] for i in row.nonzero()[1] if terms[i] in node_set]
            for node in active:
                node_freq[node] += 1
            for a, b in combinations(sorted(active), 2):
                pairs[(a, b)] += 1

        return {
            "nodes"    : nodes,
            "pairs"    : dict(pairs),
            "node_freq": dict(node_freq),
        }

    # ------------------------------------------------------------------
    # Modo evaluación
    # ------------------------------------------------------------------

    def evaluate(self, text: str, nodes: List[str]) -> np.ndarray:
        """
        Dado un texto y una lista de nodos conocidos, devuelve σ ∈ {+1,-1}^N.

        σ_i = +1 si el nodo_i (o su raíz) aparece en el texto
        σ_i = -1 si no

        Matching: substring case-insensitive sobre el texto normalizado.
        """
        text_lower = text.lower()
        sigma      = np.full(len(nodes), -1.0)
        for i, node in enumerate(nodes):
            if node.lower() in text_lower:
                sigma[i] = 1.0
        return sigma


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
