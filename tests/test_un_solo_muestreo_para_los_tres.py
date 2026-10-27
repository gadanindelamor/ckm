"""
test_un_solo_muestreo_para_los_tres.py — n_runs y seed en un solo lugar

Verifica el punto 1 del texto 13 (27 oct 2026), dirección de delamor: Monitor,
COCO y la **copia de W** de `calibrate` muestrean `sigma_0` con el mismo
concepto —el mismo argumento de la misma función,
`landscape_engine.count_attractors`— y por lo tanto leen **un solo campo** de
`CKMlandscapeConfig`. La revisión que lo decidió está en BANDEJA_code, REPORTE
1a (27 oct 2026).

Qué afirma cada test:

  - sin declaración, los tres leen el mismo valor, y cambiar el de la Config
    mueve a los tres (1b);
  - con una declaración de driver, **sólo** el caso declarado cambia, y la
    traza muestra qué caso, qué parámetro, qué valor y quién lo declaró (1c);
  - un valor propio sin `declared_by` no se acepta: un número distinto que
    nadie firma es justamente lo que 1c no quiere;
  - `calibrate_declarado` ya no puede reportar `n_runs` ni `seed` como "sin
    declarar": el lugar de los tres siempre tiene valor.

Ejecutar:
    pytest tests/test_un_solo_muestreo_para_los_tres.py -v
"""

from __future__ import annotations
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from corpus_service import CorpusService
from monitor_service import MonitorService
from ckm_landscape_config import (CKMlandscapeConfig, N_RUNS_DEFAULT,
                                  SEED_DEFAULT, SAMPLING_CASES)

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]
PROMPT = "gun control laws reduce violence"


@pytest.fixture
def corpus(tmp_path):
    c = CorpusService(storage_path=str(tmp_path / "corpus.json"),
                      min_texts=5, top_k=10)
    c.ingest(TEXTS)
    assert c.mode == "evaluation"
    return c


# ── 1b: un solo campo, leído por los tres ────────────────────────────────────

def test_el_default_es_uno_para_los_tres(corpus):
    """Sin declaración, los tres casos devuelven el mismo par (n_runs, seed)."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    valores = {c: (cfg.sampling_for(c)["n_runs"], cfg.sampling_for(c)["seed"])
               for c in SAMPLING_CASES}
    assert len(set(valores.values())) == 1, valores
    assert valores["monitor"] == (N_RUNS_DEFAULT, SEED_DEFAULT)
    # Y ninguno tiene nada propio: la lista de `propios` está vacía en los tres.
    assert all(cfg.sampling_for(c)["propios"] == [] for c in SAMPLING_CASES)
    assert all(cfg.sampling_for(c)["declared_by"] is None for c in SAMPLING_CASES)


def test_cambiar_el_valor_de_la_config_mueve_a_los_tres(corpus, tmp_path):
    """El test que pide el texto 13: un valor, y los tres lo siguen."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform",
                                    n_runs=7, seed=13)
    # la copia de W de `calibrate`
    assert cfg.calibrate_declarado["n_runs"] == 7
    assert cfg.calibrate_declarado["seed"] == 13
    # Monitor
    m = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       landscape_config=cfg)
    assert m._n_runs == 7 and m._count_seed == 13
    panel = m.evaluate(PROMPT)
    assert panel["condicion_W"]["n_runs"] == 7
    assert panel["condicion_W"]["count_seed"] == 13
    # COCO, que nace del renacimiento con el ciclo
    m2 = MonitorService(corpus, storage_path=str(tmp_path / "m2.jsonl"),
                        landscape_config=cfg, coco_config={"track_landscape": True})
    m2.evaluate(PROMPT)
    assert m2._thermostat._n_runs == 7 and m2._thermostat._seed == 13


def test_monitor_sin_config_cae_en_el_mismo_lugar(corpus, tmp_path):
    """Sin Config no se inventa un default nuevo: es el del lugar único."""
    m = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"))
    assert m._n_runs == N_RUNS_DEFAULT and m._count_seed == SEED_DEFAULT


# ── 1c: la excepción se declara, y se ve ─────────────────────────────────────

def test_declarar_un_valor_propio_mueve_solo_a_ese_caso(corpus):
    """Monitor con 1000 y COCO con 333: se puede, declarándolo."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    cfg.declare_sampling_override("coco", declared_by="driver_de_prueba",
                                  n_runs=333)
    assert cfg.sampling_for("coco")["n_runs"] == 333
    assert cfg.sampling_for("monitor")["n_runs"] == N_RUNS_DEFAULT
    assert cfg.calibrate_declarado["n_runs"] == N_RUNS_DEFAULT
    # la seed no se declaró, así que sigue siendo la de los tres
    assert cfg.sampling_for("coco")["seed"] == SEED_DEFAULT
    assert cfg.sampling_for("coco")["propios"] == ["n_runs"]


def test_la_traza_muestra_que_caso_tiene_valor_propio_y_quien_lo_declaro(corpus):
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    cfg.declare_sampling_override("coco", declared_by="driver_de_prueba",
                                  n_runs=333)
    for vista in (cfg.panel(), cfg.to_dict()):
        assert vista["sampling_overrides"] == {
            "coco": {"n_runs": 333, "declared_by": "driver_de_prueba"}
        }
    # y la declaración sobrevive la recarga
    recargada = CKMlandscapeConfig.from_dict(cfg.to_dict())
    assert recargada.sampling_for("coco")["n_runs"] == 333
    assert recargada.sampling_for("coco")["declared_by"] == "driver_de_prueba"


def test_sin_declaracion_la_traza_no_muestra_ninguno(corpus):
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    assert cfg.panel()["sampling_overrides"] == {}
    assert cfg.to_dict()["sampling_overrides"] == {}


def test_monitor_con_n_runs_explicito_lo_declara_en_la_config(corpus, tmp_path):
    """Pasarlo por la firma es una declaración, y queda firmada y visible."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10, landscape_config=cfg)
    assert m._n_runs == 10
    decl = cfg.panel()["sampling_overrides"]["monitor"]
    assert decl["n_runs"] == 10
    # quién lo declaró: este archivo de test, que es quien construyó el Monitor
    assert "test_un_solo_muestreo_para_los_tres.py" in decl["declared_by"]
    # y los otros dos casos no se movieron
    assert cfg.sampling_for("coco")["n_runs"] == N_RUNS_DEFAULT
    assert cfg.calibrate_declarado["n_runs"] == N_RUNS_DEFAULT


def test_coco_config_con_n_runs_propio_queda_declarado(corpus, tmp_path):
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       landscape_config=cfg,
                       coco_config={"track_landscape": True, "n_runs": 12})
    m.evaluate(PROMPT)
    assert m._thermostat._n_runs == 12
    assert cfg.panel()["sampling_overrides"]["coco"]["n_runs"] == 12
    assert "coco_config" in cfg.panel()["sampling_overrides"]["coco"]["declared_by"]
    assert cfg.sampling_for("monitor")["n_runs"] == N_RUNS_DEFAULT


# ── lo que no se acepta ──────────────────────────────────────────────────────

def test_un_valor_propio_sin_quien_lo_declaro_no_entra(corpus):
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    with pytest.raises(ValueError, match="declared_by"):
        CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform",
                                  sampling_overrides={"coco": {"n_runs": 333}})
    with pytest.raises(ValueError, match="declared_by"):
        cfg.declare_sampling_override("coco", declared_by="   ", n_runs=333)


@pytest.mark.parametrize("overrides, match", [
    ({"monitorr": {"n_runs": 5, "declared_by": "x"}}, "caso desconocido"),
    ({"coco": {"n_rums": 5, "declared_by": "x"}}, "desconocidos"),
    ({"coco": {"declared_by": "x"}}, "ningún parámetro"),
    ({"coco": {"n_runs": 0, "declared_by": "x"}}, "n_runs inválido"),
    ({"coco": {"seed": 1.5, "declared_by": "x"}}, "seed inválida"),
    ({"coco": "333"}, "declaración inválida"),
])
def test_declaraciones_invalidas(corpus, overrides, match):
    with pytest.raises(ValueError, match=match):
        CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform",
                                  sampling_overrides=overrides)


def test_caso_desconocido_en_sampling_for(corpus):
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    with pytest.raises(ValueError, match="caso desconocido"):
        cfg.sampling_for("gatekeeper")


# ── lo que dejó de ser posible ───────────────────────────────────────────────

def test_calibrate_no_tiene_n_runs_ni_seed_propios(corpus):
    """Salieron del lugar: eran el mismo concepto con otro nombre."""
    with pytest.raises(TypeError):
        CKMlandscapeConfig(sampling_mode="uniform", calibrate_n_runs=1000)
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    # `sin_declarar` sólo puede hablar de la grilla
    assert cfg.calibrate_declarado["sin_declarar"] == ["grilla_lambda"]
    cfg2 = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    assert "n_runs" not in cfg2.calibrate_declarado["sin_declarar"]
