"""
test_rebuild_consulta_w_version.py — verificación de TASK_rebuild_consulta_w_version_v1 (D7)

Ejecutar:
    pytest tests/test_rebuild_consulta_w_version.py -v
"""

from __future__ import annotations
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from corpus_service import CorpusService
from ckm_landscape_config import CKMlandscapeConfig

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]


@pytest.fixture
def corpus(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    assert c.mode == "evaluation"
    return c


def _snapshot(c):
    return c.w_sha(), c.get_nodes()


def test_sin_rebuild(corpus):
    sha, nodes = _snapshot(corpus)
    r = corpus.w_change_since(sha, nodes)
    assert r["changed"] is False
    assert r["nodes_changed"] is False
    assert r["w_version_id_old"] == r["w_version_id_new"]
    assert r["N_old"] == r["N_new"]


def test_rebuild_N_igual_nodos_distintos(corpus):
    sha, nodes = _snapshot(corpus)
    # texto que cambia los nodos con N igual BAJO LA REGLA DE DESEMPATE
    # (conserva precedente): el anterior ("police response…") ahora sube N.
    corpus.ingest(["bans reduce assault weapons and gun violence"])
    r = corpus.w_change_since(sha, nodes)
    assert r["N_old"] == r["N_new"] == 10
    assert r["changed"] is True
    assert r["nodes_changed"] is True


def test_rebuild_N_distinto(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=2, top_k=20)
    c.ingest(["gun control", "gun rights"])
    sha, nodes = _snapshot(c)
    c.ingest(TEXTS)
    r = c.w_change_since(sha, nodes)
    assert r["changed"] is True
    assert r["N_old"] != r["N_new"]


def test_id_nuevo_coincide_con_config(corpus):
    sha, nodes = _snapshot(corpus)
    # texto que cambia los nodos con N igual BAJO LA REGLA DE DESEMPATE
    # (conserva precedente): el anterior ("police response…") ahora sube N.
    corpus.ingest(["bans reduce assault weapons and gun violence"])
    r = corpus.w_change_since(sha, nodes)
    cfg = CKMlandscapeConfig.from_W(corpus.get_W(), theta_W=0.01,
                                    sampling_mode="uniform", scale="log")
    assert r["w_version_id_new"] == cfg.w_version_id


def test_corpus_sin_distincion_sigue_en_acumulacion(tmp_path):
    """Un texto: todos los términos empatan; sin precedente no hay nodos, no
    hay W — el corpus sigue en acumulación hasta que el dato distinga."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=1, top_k=10)
    c.ingest(["gun control reduces violence and saves lives"])
    assert c.mode == "accumulation" and c.get_nodes() == []
    c.ingest(TEXTS)
    assert c.mode == "evaluation" and c.get_nodes()


def test_rebuild_suspendido_construye_una_vez_y_acumula(tmp_path):
    """Rebuild suspendido: W se construye cuando el dato distingue y no se
    reconstruye con textos nuevos (delamor, sep 2026 — también en vivo)."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5,
                      top_k=10, rebuild_suspendido=True)
    c.ingest(TEXTS)
    sha, nodes, n = c.w_sha(), c.get_nodes(), len(c._texts)
    c.ingest(["bans reduce assault weapons and gun violence"])
    assert c.w_sha() == sha and c.get_nodes() == nodes
    assert len(c._texts) == n + 1                       # el texto se acumula
    assert c.status()["rebuild_suspendido"] is True


def test_rebuild_suspendido_espera_a_que_el_dato_distinga(tmp_path):
    """Sin W todavía (dato que no distingue), la suspensión no impide el
    primer build: sigue intentando hasta que haya nodos."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=1,
                      top_k=10, rebuild_suspendido=True)
    c.ingest(["gun control reduces violence and saves lives"])
    assert c.mode == "accumulation"
    c.ingest(TEXTS)
    assert c.mode == "evaluation" and c.get_nodes()
