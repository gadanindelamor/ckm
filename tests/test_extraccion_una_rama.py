"""
test_extraccion_una_rama.py — paridad accumulate / evaluate
(TASK_extraccion_una_rama_v1)

Las dos ramas de NodeExtractorService deben reconocer los mismos nodos en el
mismo texto. Si este test falla, W y σ_prompt están hablando de cosas
distintas con los mismos nombres.

Ejecutar:
    pytest tests/test_extraccion_una_rama.py -v
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "services"))
from node_extractor import NodeExtractorService

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


def _activos_accumulate(r, k):
    """Nodos activos del texto k según accumulate: los que forman pares, más
    los que aparecen solos (node_freq no es por texto — se reconstruye)."""
    return {a for par in r["pairs_by_text"][k] for a in par}


def _paridad(textos, top_k):
    ex = NodeExtractorService(top_k=top_k)
    r = ex.accumulate(textos)
    nodes = r["nodes"]
    vec = ex._vectorizer(vocabulary=nodes)
    m = vec.fit_transform(textos)
    for k, texto in enumerate(textos):
        acc = {nodes[i] for i in m[k].nonzero()[1]}
        sig = ex.evaluate(texto, nodes)
        ev = {n for n, s in zip(nodes, sig) if s > 0}
        assert acc == ev, f"texto {k}: sólo W {acc - ev} | sólo σ {ev - acc}"
        # los que forman pares son subconjunto de los activos
        assert _activos_accumulate(r, k) <= ev


def test_paridad_textos_de_tests():
    _paridad(TEXTS, top_k=10)


@pytest.mark.skipif(not CASO09.exists(), reason="corpus caso09 no disponible")
def test_paridad_caso09():
    textos = json.loads(CASO09.read_text())["texts"]
    _paridad(textos, top_k=32)


def test_substring_ya_no_activa():
    """'now' no se activa por 'know'; 'here' no por 'where'."""
    ex = NodeExtractorService()
    sig = ex.evaluate("I know where it is", ["now", "here", "know"])
    assert list(sig) == [-1.0, -1.0, 1.0]


def test_bigrama_con_stopword_en_medio_se_reconoce():
    """'joined the channel' produce el bigrama 'joined channel' en las dos ramas."""
    ex = NodeExtractorService()
    sig = ex.evaluate("Mark joined the channel today", ["joined channel"])
    assert sig[0] == 1.0
