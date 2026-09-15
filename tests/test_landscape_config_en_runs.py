"""
test_landscape_config_en_runs.py — verificación de TASK_landscape_config_en_runs_v1

Ejecutar:
    pytest tests/test_landscape_config_en_runs.py -v
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from corpus_service import CorpusService
from monitor_service import MonitorService
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
PROMPTS = ["gun control laws reduce violence", "armed citizens protect rights"]


@pytest.fixture
def corpus(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "corpus.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    assert c.mode == "evaluation"
    return c


def _lineas(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def test_sin_config_panel_none(corpus, tmp_path):
    jsonl = tmp_path / "m.jsonl"
    m = MonitorService(corpus, storage_path=str(jsonl), n_runs_attractors=10)
    panel = m.evaluate(PROMPTS[0])
    assert panel["landscape_config"] is None
    assert all(r["panel"]["landscape_config"] is None for r in _lineas(jsonl))


def test_sampling_mode_distinto_falla_en_construccion(corpus, tmp_path):
    cfg = CKMlandscapeConfig.from_W(
        corpus.get_W(), theta_W=0.01, sampling_mode="boltzmann", scale="log",
    )
    with pytest.raises(ValueError):
        MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       sampling_mode="uniform", landscape_config=cfg)


def test_con_config_cada_linea_recarga_igual(corpus, tmp_path):
    cfg = CKMlandscapeConfig.from_W(
        corpus.get_W(), theta_W=0.01, sampling_mode="uniform", scale="log",
    )
    jsonl = tmp_path / "m.jsonl"
    m = MonitorService(corpus, storage_path=str(jsonl), n_runs_attractors=10,
                       landscape_config=cfg)
    for p in PROMPTS:
        m.evaluate(p)

    lineas = _lineas(jsonl)
    assert len(lineas) == len(PROMPTS)
    for r in lineas:
        assert CKMlandscapeConfig.from_dict(r["panel"]["landscape_config"]) == cfg


def test_gatekeeper_c1_presente_y_none(corpus, tmp_path):
    """D4 — traza de admisión: nadie evalúa C1 todavía."""
    cfg = CKMlandscapeConfig.from_W(
        corpus.get_W(), theta_W=0.01, sampling_mode="uniform", scale="log",
    )
    for config in (None, cfg):
        jsonl = tmp_path / f"m_{config is None}.jsonl"
        m = MonitorService(corpus, storage_path=str(jsonl), n_runs_attractors=10,
                           landscape_config=config)
        panel = m.evaluate(PROMPTS[0])
        assert "gatekeeper_c1" in panel and panel["gatekeeper_c1"] is None
        assert all(r["panel"]["gatekeeper_c1"] is None for r in _lineas(jsonl))
