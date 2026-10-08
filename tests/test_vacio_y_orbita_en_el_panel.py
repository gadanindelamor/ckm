"""
test_vacio_y_orbita_en_el_panel.py — CP2c de TASK_monitor_coco_ciclo_orbita_v2

Dos cosas:

1. **El vacío se declara, no se disfraza de medición.** Sin baseline la zona es
   UNKNOWN y `frac_rec` es None, no "stable" y 1.0. Mismo criterio que
   `c06db07` (temp_signal UNKNOWN, no NOMINAL) y que SALAMANCA: "no medible" no
   es "nada".
2. **La órbita entra al panel.** Las tres clases se registran; qué entra a
   `Δ_r_pares` **no cambia** — eso es el CP3 y es de delamor.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
from ckm_landscape_config import CKMlandscapeConfig        # noqa: E402
from coco import COCO, ThermostatState, ZONA_UNKNOWN       # noqa: E402
from corpus_service import CorpusService                    # noqa: E402
from monitor_service import MonitorService                  # noqa: E402

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
]
NUEVOS = ["mental health is the real cause of gun violence",
          "armed citizens deter crime and protect communities"]
PROMPT = "gun control laws reduce violence"


@pytest.fixture
def corpus(tmp_path) -> CorpusService:
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest(TEXTS)
    return c


def _monitor(corpus, tmp_path, **kw) -> MonitorService:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    return MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                          n_runs_attractors=10, landscape_config=cfg, **kw), cfg


# ── 1. el vacío ─────────────────────────────────────────────────────────────

def test_sin_medicion_la_zona_es_UNKNOWN_no_stable() -> None:
    """El cambio del CP2c: antes esto devolvía "stable"."""
    th = COCO(W=np.array([[0., .5], [.5, 0.]]), n_runs=5)
    assert th._classify_zone(None, 1.0) == ZONA_UNKNOWN
    assert th._classify_zone(None, 1.0) != "stable"


def test_sin_baseline_frac_rec_es_None_no_1_0() -> None:
    """Antes, la ausencia de baseline se leía como recuperación total."""
    th = COCO(W=np.array([[0., .5], [.5, 0.]]), n_runs=5)
    assert th._classify_zone(0.5, None) == ZONA_UNKNOWN


def test_el_estado_por_defecto_no_afirma_un_campo_estable() -> None:
    """
    Latente, encontrado en el CP0: `ThermostatState()` tenía por defecto
    D_ckm=0.0, frac_rec=1.0 y zone="stable", o sea que un estado sin construir
    se leía como campo medido, estable y sin divergencia. Nadie lo construía
    así, pero el valor estaba.
    """
    s = ThermostatState()
    assert s.zone == ZONA_UNKNOWN
    assert s.D_ckm is None and s.frac_rec is None
    assert s.A0 is None and s.A_current is None


def test_UNKNOWN_no_dispara_stop(corpus, tmp_path) -> None:
    """Sin medición no se aplica STOP — el efecto que ya era correcto."""
    m, cfg = _monitor(corpus, tmp_path, coco_config={"track_landscape": True})
    panel = m.evaluate(PROMPT)
    th = panel["thermostat"]
    if th["zone"] == ZONA_UNKNOWN:
        assert th["stop_applied"] is False


def test_el_panel_nunca_dice_stable_sin_D_ckm(corpus, tmp_path) -> None:
    """Recorrido real: ninguna evaluación puede decir "stable" con D_ckm None."""
    m, cfg = _monitor(corpus, tmp_path, coco_config={"track_landscape": True})
    paneles = [m.evaluate(PROMPT)]
    corpus.ingest(NUEVOS)
    paneles.append(m.evaluate(PROMPT))
    for p in paneles:
        th = p.get("thermostat")
        if th is None:
            continue
        if th["D_ckm"] is None or th["frac_rec"] is None:
            assert th["zone"] == ZONA_UNKNOWN, \
                f'zona {th["zone"]!r} sin medición'


# ── 2. la órbita en el panel ────────────────────────────────────────────────

def test_el_panel_lleva_las_tres_clases_y_el_periodo(corpus, tmp_path) -> None:
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    for k in ("periodo_orbita", "cola_orbita", "n_aceptados",
              "n_expulsados", "n_torsion", "pares_torsion"):
        assert k in p, f"falta {k} en el panel"
    assert p["periodo_orbita"] in (1, 2)
    assert isinstance(p["pares_torsion"], list)


def test_las_tres_clases_suman_los_pares_declarados(corpus, tmp_path) -> None:
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    d = len(p["activos_prompt"])
    assert p["n_aceptados"] + p["n_expulsados"] + p["n_torsion"] == d * (d - 1) // 2


def test_en_punto_fijo_no_hay_torsion_y_expulsados_es_lo_de_hoy(corpus, tmp_path) -> None:
    """
    La invariante de compatibilidad, sobre UNA evaluación — que es la condición
    bajo la que vale (medido en el CP1: a lo largo de un recorrido no vale,
    porque Δ_r entra a W_eff).
    """
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    if p["periodo_orbita"] == 1:
        assert p["n_torsion"] == 0
        assert p["n_expulsados"] == p["n_rejected_pairs"]


def test_la_torsion_no_se_promedia_viaja_con_sus_pares(corpus, tmp_path) -> None:
    """Los pares van por nombre de nodo, no agregados a un número."""
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    assert len(p["pares_torsion"]) == p["n_torsion"]
    for a, b in p["pares_torsion"]:
        assert a in p["activos_prompt"] and b in p["activos_prompt"]


def test_delta_r_no_cambio_todavia(corpus, tmp_path) -> None:
    """
    Qué entra a Δ_r sigue saliendo de la fase, no de la órbita: eso es el CP3.
    `n_rejected_pairs` tiene que seguir contando los pares de la fase.
    """
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    # expulsados ⊆ fase ⊆ expulsados ∪ torsión
    assert p["n_expulsados"] <= p["n_rejected_pairs"]
    assert p["n_rejected_pairs"] <= p["n_expulsados"] + p["n_torsion"]
