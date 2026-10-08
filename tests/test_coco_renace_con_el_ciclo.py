"""
test_coco_renace_con_el_ciclo.py — CP2b de TASK_monitor_coco_ciclo_orbita_v2

Una sola existencia: Monitor y COCO nacen, viven y mueren juntos, y el reloj es
el ciclo vigente de la Config, que Monitor abre.

El primer test reproduce la condición exacta que el CP1 midió rompiendo
(`ValueError: shapes (31,31) (28,28)`) y verifica que ahora no rompe. Falla si
el renacimiento se saca.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
from ckm_landscape_config import CKMlandscapeConfig        # noqa: E402
from coco import COCO                                      # noqa: E402
from corpus_service import CorpusService                    # noqa: E402
from monitor_service import MonitorService                  # noqa: E402

CASO09 = RAIZ / "process/iap/corpus_state.json.bak_1784685610_caso09_run2"

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
]
NUEVOS = [
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
    "red flag laws remove weapons from dangerous people",
]
PROMPT = "gun control laws reduce violence"

COCO_CONFIG = {"track_landscape": True}


@pytest.fixture
def corpus(tmp_path) -> CorpusService:
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest(TEXTS)
    assert c.mode == "evaluation"
    return c


def _monitor(corpus, tmp_path, cfg, **kw) -> MonitorService:
    return MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                          n_runs_attractors=10, landscape_config=cfg, **kw)


# ── el ValueError del CP1 ───────────────────────────────────────────────────

def test_el_rebuild_con_N_creciente_ya_no_rompe(tmp_path) -> None:
    """
    La condición que el CP1 midió rompiendo, sobre el mismo corpus: caso09_run2
    natural, se lee COCO una vez y se ingesta de a un texto.

    Antes del CP2b: ValueError por shapes (31,31) contra (28,28) en coco.py:254,
    en la PRIMERA evaluación posterior al rebuild, porque COCO se quedaba con la
    N de su W y Monitor crecía.
    """
    if not CASO09.exists():
        pytest.skip(f"no está {CASO09}")
    textos = json.loads(CASO09.read_text())["texts"]
    corte = max(5, len(textos) // 3)

    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest(textos[:corte])
    assert c.get_W() is not None

    cfg = CKMlandscapeConfig.create(c.get_W(), sampling_mode="uniform", n_runs=10)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10, landscape_config=cfg,
                       coco_config=COCO_CONFIG)

    renacimientos = 0
    for texto in textos[corte:]:
        c.ingest([texto])
        panel = m.evaluate(texto)              # antes: ValueError acá
        if panel and panel.get("coco_renace"):
            renacimientos += 1
        if panel and m._thermostat is not None:
            assert m._thermostat.W.shape[0] == m._Delta_r.shape[0], \
                "la N de COCO tiene que ser la de la W del ciclo vigente"

    assert renacimientos >= 1, "con N creciendo tuvo que renacer al menos una vez"
    assert cfg.vigente(c.get_W())


# ── renace si y solo si se abre un ciclo ────────────────────────────────────

@pytest.mark.parametrize("ciclo_ya_abierto", [False, True])
def test_coco_nace_con_el_bootstrap(corpus, tmp_path, ciclo_ya_abierto) -> None:
    """
    Nace con el bootstrap, lo haya abierto Monitor o lo trajera ya abierto la
    Config.

    El segundo caso lo encontró este test: con `create()` el ciclo bootstrap ya
    está abierto antes de que Monitor exista, así que `abrir_ciclo` nunca
    devuelve True y COCO no tenía nacimiento. Por eso el renacimiento se ata al
    `w_version_id` del ciclo vigente y no al evento.
    """
    cfg = (CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
           if ciclo_ya_abierto
           else CKMlandscapeConfig(sampling_mode="uniform", n_runs=10))
    m = _monitor(corpus, tmp_path, cfg, coco_config=COCO_CONFIG)
    assert m._thermostat is None                   # no nace en el constructor
    panel = m.evaluate(PROMPT)
    assert m._thermostat is not None
    assert panel["coco_renace"] is True
    assert panel["coco_generacion"] == 1
    assert cfg.ciclo_vigente.causa == "bootstrap"


def test_sin_cambio_de_W_no_renace(corpus, tmp_path) -> None:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    m = _monitor(corpus, tmp_path, cfg, coco_config=COCO_CONFIG)
    primero = m.evaluate(PROMPT)
    gen = primero["coco_generacion"]
    for _ in range(3):
        panel = m.evaluate(PROMPT)
        assert panel["coco_renace"] is False
        assert panel["coco_generacion"] == gen
    assert len(cfg.ciclos) == 1


def test_renace_en_el_mismo_paso_que_el_reset_de_delta_r(corpus, tmp_path) -> None:
    """Una sola existencia: el renacimiento y el reset son el mismo bloque."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    m = _monitor(corpus, tmp_path, cfg, coco_config=COCO_CONFIG)
    m.evaluate(PROMPT)
    corpus.ingest(NUEVOS)
    panel = m.evaluate(PROMPT)
    assert panel["Delta_r_reset"] is not None
    assert panel["coco_renace"] is True
    assert panel["coco_generacion"] == 2
    assert float(np.sum(m._Delta_r)) >= 0


def test_el_coco_nuevo_nace_vacio(corpus, tmp_path) -> None:
    """Δ propio en ceros y A0 en None: la primera división es contra el vacío."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    m = _monitor(corpus, tmp_path, cfg, coco_config=COCO_CONFIG)
    m.evaluate(PROMPT)
    corpus.ingest(NUEVOS)
    antes = id(m._thermostat)
    m._invalidar_si_W_cambio(corpus.get_nodes())
    th = m._thermostat
    assert id(th) != antes
    assert not th._Delta.any()
    assert th._A0 is None


# ── n_runs, seed y sampling_mode salen de la Config (P9) ───────────────────

def test_coco_toma_n_runs_y_seed_de_la_config(corpus, tmp_path) -> None:
    """Uno solo para Monitor y COCO: COCO ya no tiene default propio."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform",
                                    n_runs=17, seed=99)
    m = _monitor(corpus, tmp_path, cfg, coco_config=COCO_CONFIG)
    m.evaluate(PROMPT)
    assert m._thermostat._n_runs == 17
    assert m._thermostat._seed == 99
    assert m._thermostat._sampling_mode == "uniform"


def test_coco_config_puede_pisar_lo_de_la_config_y_queda_declarado(corpus, tmp_path) -> None:
    """Si coco_config trae n_runs, gana — y es explícito, no un default."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=17)
    m = _monitor(corpus, tmp_path, cfg, coco_config={"n_runs": 5, "track_landscape": True})
    m.evaluate(PROMPT)
    assert m._thermostat._n_runs == 5


def test_la_configuracion_es_la_misma_antes_y_despues_de_renacer(corpus, tmp_path) -> None:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform",
                                    n_runs=11, seed=7)
    m = _monitor(corpus, tmp_path, cfg, coco_config=COCO_CONFIG)
    m.evaluate(PROMPT)
    a = (m._thermostat._n_runs, m._thermostat._seed,
         m._thermostat._sampling_mode, m._thermostat._track_landscape)
    corpus.ingest(NUEVOS)
    m.evaluate(PROMPT)
    b = (m._thermostat._n_runs, m._thermostat._seed,
         m._thermostat._sampling_mode, m._thermostat._track_landscape)
    assert a == b


# ── la instancia externa no renace ─────────────────────────────────────────

def test_la_instancia_externa_no_renace_y_queda_declarada(corpus, tmp_path) -> None:
    """Aceptada sólo en transición: es el camino de los tests Armstrong."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    th = COCO(W=corpus.get_W(), n_runs=10)
    m = _monitor(corpus, tmp_path, cfg, thermostat=th)
    panel = m.evaluate(PROMPT)
    assert panel["coco_externo"] is True
    assert panel["coco_renace"] is False
    assert m._thermostat is th
    assert m._coco_config is None


def test_thermostat_y_coco_config_juntos_fallan(corpus, tmp_path) -> None:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    with pytest.raises(ValueError, match="excluyentes"):
        _monitor(corpus, tmp_path, cfg, thermostat=COCO(W=corpus.get_W(), n_runs=10),
                 coco_config=COCO_CONFIG)


# ── sin COCO, el panel queda igual que hoy ─────────────────────────────────

def test_sin_coco_el_panel_queda_igual(corpus, tmp_path) -> None:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform", n_runs=10)
    m = _monitor(corpus, tmp_path, cfg)
    panel = m.evaluate(PROMPT)
    assert panel["thermostat"] is None
    assert panel["coco_renace"] is False
    assert panel["coco_generacion"] == 0
    assert panel["coco_externo"] is False


def test_coco_config_sin_config_se_rechaza(corpus, tmp_path) -> None:
    """
    Una sola existencia necesita un solo reloj.

    Sin Config no se abre ningún ciclo, así que COCO nacería una vez y en el
    primer rebuild que cambie N volvería el ValueError que el CP1 midió.
    Lo encontró este mismo test: primero lo escribí esperando que COCO naciera
    una vez y no renaciera, y el test falló con
    `ValueError: shapes (22,22) (3,3)`. No se acepta una configuración cuya
    falla está garantizada: se rechaza en la construcción.
    """
    with pytest.raises(ValueError, match="requiere landscape_config"):
        MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10, coco_config=COCO_CONFIG)
