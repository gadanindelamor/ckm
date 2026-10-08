"""
test_corpus_suelta_a_coco.py — CP4 de TASK_monitor_coco_ciclo_orbita_v2

delamor: *"Que deje en paz a COCO. COCO es con Monitor."*

CorpusService construye W y la versiona; eso es todo. COCO vive dentro de
Monitor, y el canal le pasa cómo construirlo en vez de leerlo de Corpus.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
sys.path.insert(0, str(RAIZ))
from corpus_service import CorpusService                    # noqa: E402

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]


# ── CorpusService suelta a COCO ─────────────────────────────────────────────

def test_el_rebuild_ya_no_crea_coco(tmp_path) -> None:
    """Tras varios rebuilds reales, Corpus no tiene ningún COCO."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest(TEXTS[:5])
    assert c.get_W() is not None, "el test necesita que W exista"
    for t in TEXTS[5:]:
        c.ingest([t])
    assert c.coco is None, "CorpusService volvió a crear COCO en el rebuild"


def test_la_property_coco_quedo_deprecada_y_devuelve_none(tmp_path) -> None:
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest(TEXTS)
    assert c.coco is None
    assert "DEPRECADA" in (type(c).coco.__doc__ or ""), \
        "la property tiene que decir que está deprecada"


def test_load_landscape_history_ya_no_existe(tmp_path) -> None:
    """Se fue con el CP4: su único uso era el COCO que creaba _rebuild."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    assert not hasattr(c, "_load_landscape_history")


# ── el canal ────────────────────────────────────────────────────────────────

@pytest.fixture
def canal(monkeypatch):
    """CKMMonitor con su _state en un tmp, y su singleton reseteado."""
    import iap_chatroom.ckm_monitor as mod
    d = Path(tempfile.mkdtemp())
    monkeypatch.setattr(mod, "_STATE_DIR", d)
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    cm = mod.CKMMonitor(min_texts=5)

    class _Msg:
        def __init__(self, text, device_id="d0"):
            self.text, self.device_id = text, device_id

    for i, t in enumerate(TEXTS):
        cm.on_message(_Msg(t, f"dev{i % 2}"))
    return cm


def test_el_canal_le_pasa_coco_config_a_monitor(canal) -> None:
    """El canal declara cómo construir COCO; no lo lee de Corpus."""
    assert canal._monitor._coco_config == {"track_landscape": True}
    assert canal._monitor.thermostat is not None
    assert canal._corpus.coco is None


def test_el_coco_del_canal_toma_n_runs_de_la_config(canal) -> None:
    """P9: un solo n_runs, y en el canal llega por la Config."""
    assert canal._monitor.thermostat._n_runs == canal._landscape_config.n_runs


def test_el_canal_no_toca_corpus_coco(canal, monkeypatch) -> None:
    """
    `on_message` ya no lee `corpus.coco`.

    Se le pone a Corpus un `_coco` centinela que estalla si alguien le pide la
    historia. Si el canal volviera a leerlo, el test rompe.
    """
    class _Bomba:
        def landscape_history(self):
            raise AssertionError("el canal leyó corpus.coco")

    # raising=False: el atributo ya no existe, justamente porque Corpus
    # dejó de crear COCO. Se lo pone a mano para que la property lo devuelva.
    monkeypatch.setattr(canal._corpus, "_coco", _Bomba(), raising=False)
    assert canal._corpus.coco is not None, "el centinela tiene que estar puesto"

    class _Msg:
        text = "red flag laws remove weapons from dangerous people"
        device_id = "dev0"

    canal.on_message(_Msg())          # no debe estallar


def test_el_panel_del_canal_lleva_la_orbita(canal) -> None:
    """Las seis claves del CP2c/CP3i llegan al panel del canal."""
    p = canal._last_panel
    assert p is not None, "el canal tiene que haber producido un panel"
    for k in ("periodo_orbita", "cola_orbita", "n_aceptados", "n_expulsados",
              "n_torsion", "pares_torsion", "Delta_r_torsion_sum"):
        assert k in p, f"falta {k} en el panel del canal"


def test_el_jsonl_del_canal_lleva_la_orbita(canal) -> None:
    import json
    jl = Path(canal._monitor._storage)
    ls = [json.loads(l) for l in jl.read_text().splitlines() if l.strip()]
    assert ls, "el canal tiene que haber escrito el JSONL"
    pr = ls[-1]["panel"]
    assert "n_torsion" in pr and "Delta_r_torsion_sum" in pr
