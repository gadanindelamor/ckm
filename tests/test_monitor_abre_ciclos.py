"""
test_monitor_abre_ciclos.py — verificación del CP2 de TASK_CKMlandscapeConfig_v3

D4: Monitor abre el ciclo, en el mismo bloque que _invalidar_si_W_cambio, y es
el único que lo hace. I7: el panel lleva config.panel(), no la config completa.
Y el gap D7 queda cerrado: la config ya no se queda atrás tras un rebuild.

Los cuatro primeros tests **fallan sin el CP2** (medido antes de commitear: ver
BANDEJA_code, REPORTE CP2). Los demás fijan lo que no debe cambiar.

Ejecutar:
    pytest tests/test_monitor_abre_ciclos.py -v
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from ckm_landscape_config import CAUSA_BOOTSTRAP, CKMlandscapeConfig   # noqa: E402
from coco import COCO                                                  # noqa: E402
from corpus_service import CorpusService                               # noqa: E402
from monitor_service import MonitorService                             # noqa: E402

CAUSAS_MONITOR = ("N", "nodos", "pesos")

TEXTS = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
]
TEXTS_NUEVOS = [
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
    "red flag laws remove weapons from dangerous people",
]
PROMPT = "gun control laws reduce violence"


@pytest.fixture
def corpus(tmp_path) -> CorpusService:
    """rebuild_suspendido=False: cada ingest posterior reconstruye W."""
    c = CorpusService(storage_path=str(tmp_path / "corpus.json"), min_texts=5, top_k=10)
    c.ingest(TEXTS)
    assert c.mode == "evaluation"
    return c


def _monitor(corpus, tmp_path, cfg, nombre="m.jsonl") -> MonitorService:
    return MonitorService(corpus, storage_path=str(tmp_path / nombre),
                          n_runs_attractors=10, landscape_config=cfg)


def _lineas(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


# ── D4: Monitor abre el ciclo ────────────────────────────────────────────────

def test_D4_monitor_abre_ciclo_cuando_W_cambia(corpus, tmp_path) -> None:
    """Falla sin el CP2: la config se quedaba con el ciclo del bootstrap."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    assert len(cfg.ciclos) == 1

    corpus.ingest(TEXTS_NUEVOS)                 # W se reconstruye
    panel = m.evaluate(PROMPT)

    assert len(cfg.ciclos) == 2
    assert cfg.ciclos[0].causa == CAUSA_BOOTSTRAP
    assert cfg.ciclos[1].causa in CAUSAS_MONITOR
    assert panel["Delta_r_reset"] in CAUSAS_MONITOR


def test_D4_la_causa_del_ciclo_es_la_que_reporta_el_panel(corpus, tmp_path) -> None:
    """La causa no se traduce: Monitor la pasa tal cual al ciclo."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    corpus.ingest(TEXTS_NUEVOS)
    panel = m.evaluate(PROMPT)
    assert cfg.ciclo_vigente.causa == panel["Delta_r_reset"]


def test_D7_la_config_sigue_vigente_tras_el_rebuild(corpus, tmp_path) -> None:
    """
    Falla sin el CP2, y es el gap D7: antes la config quedaba describiendo
    una W que ya no era la vigente.
    """
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    corpus.ingest(TEXTS_NUEVOS)
    m.evaluate(PROMPT)
    assert cfg.vigente(corpus.get_W()) is True
    assert cfg.ciclo_vigente.w_version_id == corpus.w_sha()


def test_D4_una_config_atrasada_abre_ciclo_en_la_primera_evaluacion(corpus, tmp_path) -> None:
    """
    Falla sin el CP2. W cambió entre construir la config y la primera
    evaluación: Δ_r no tiene nada que descartar, pero la config sí está atrás.
    """
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    sha_viejo = cfg.ciclo_vigente.w_version_id
    corpus.ingest(TEXTS_NUEVOS)                 # W cambia ANTES del primer evaluate
    m = _monitor(corpus, tmp_path, cfg)
    panel = m.evaluate(PROMPT)

    assert panel["Delta_r_reset"] is None       # primera evaluación: nada que resetear
    assert len(cfg.ciclos) == 2                 # y aun así el ciclo se abrió
    assert cfg.ciclo_vigente.w_version_id != sha_viejo
    assert cfg.vigente(corpus.get_W()) is True
    # La causa no es derivable con lo que el ciclo guarda: N no cambió y las
    # etiquetas no están (P5). "W_distinta" dice exactamente eso.
    assert cfg.ciclo_vigente.causa == "W_distinta"


# ── I5: sin cambio de W no hay ciclo nuevo ───────────────────────────────────

def test_sin_cambio_de_W_no_se_abre_ciclo(corpus, tmp_path) -> None:
    """
    Tres evaluaciones sobre la misma W: un solo ciclo (I5).

    La segunda mitad está para que el test pueda fallar: sin el CP2 la
    primera mitad pasa trivialmente, porque nunca se abre ningún ciclo.
    """
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = _monitor(corpus, tmp_path, cfg)
    for _ in range(3):
        m.evaluate(PROMPT)
    assert len(cfg.ciclos) == 1

    corpus.ingest(TEXTS_NUEVOS)
    m.evaluate(PROMPT)
    assert len(cfg.ciclos) == 2


def test_dos_rebuilds_abren_dos_ciclos(corpus, tmp_path) -> None:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    for t in TEXTS_NUEVOS:
        corpus.ingest([t])
        m.evaluate(PROMPT)
    shas = [c.w_version_id for c in cfg.ciclos]
    assert len(shas) == len(set(shas)), "no hay dos ciclos con el mismo sha (I5)"
    assert len(cfg.ciclos) >= 2


# ── I2: Monitor es el único que abre ciclos ──────────────────────────────────

def test_solo_monitor_abre_ciclos_coco_no(corpus, tmp_path) -> None:
    """Con COCO conectado, un rebuild agrega UN ciclo, no dos."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    th = COCO(W=corpus.get_W())
    m = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10, landscape_config=cfg, thermostat=th)
    m.evaluate(PROMPT)
    n_antes = len(cfg.ciclos)
    corpus.ingest(TEXTS_NUEVOS)
    m.evaluate(PROMPT)
    assert len(cfg.ciclos) == n_antes + 1


# ── I6: nadie señaló, así que la deriva es nula ──────────────────────────────

def test_la_deriva_del_ciclo_que_abre_monitor_es_nula(corpus, tmp_path) -> None:
    """
    Nula, no cero: la señal de rebuild existe en ckm_monitor.py pero no llega
    hasta acá. Cuando llegue, este test cambia y se reporta.
    """
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    corpus.ingest(TEXTS_NUEVOS)
    m.evaluate(PROMPT)
    # Sin esta primera línea el test pasaba aunque no se abriera ningún ciclo:
    # el bootstrap también tiene t_senal None. Medido.
    assert len(cfg.ciclos) == 2, "el ciclo que se mide tiene que ser uno nuevo"
    assert cfg.ciclo_vigente.causa != CAUSA_BOOTSTRAP
    assert cfg.ciclo_vigente.t_senal is None
    assert cfg.deriva() is None


# ── I7: el panel lleva panel(), no la config completa ────────────────────────

def test_I7_el_panel_no_lleva_la_historia(corpus, tmp_path) -> None:
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    jsonl = tmp_path / "m.jsonl"
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    corpus.ingest(TEXTS_NUEVOS)
    panel = m.evaluate(PROMPT)

    lc = panel["landscape_config"]
    assert "ciclos" not in lc
    assert lc["ciclo_vigente"]["w_version_id"] == corpus.w_sha()
    assert lc["config_id"] == cfg.config_id
    for r in _lineas(jsonl):
        assert "ciclos" not in r["panel"]["landscape_config"]


def test_cada_panel_lleva_el_ciclo_de_su_momento(corpus, tmp_path) -> None:
    """Un panel es una foto: el de antes del rebuild no lleva el ciclo nuevo."""
    cfg = CKMlandscapeConfig.create(corpus.get_W(), sampling_mode="uniform")
    jsonl = tmp_path / "m.jsonl"
    m = _monitor(corpus, tmp_path, cfg)
    m.evaluate(PROMPT)
    corpus.ingest(TEXTS_NUEVOS)
    m.evaluate(PROMPT)

    primera, segunda = _lineas(jsonl)
    sha1 = primera["panel"]["landscape_config"]["ciclo_vigente"]["w_version_id"]
    sha2 = segunda["panel"]["landscape_config"]["ciclo_vigente"]["w_version_id"]
    assert sha1 != sha2
    assert sha2 == corpus.w_sha()


# ── sin config, nada cambia ──────────────────────────────────────────────────

def test_sin_config_el_rebuild_no_rompe_nada(corpus, tmp_path) -> None:
    m = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10)
    m.evaluate(PROMPT)
    corpus.ingest(TEXTS_NUEVOS)
    panel = m.evaluate(PROMPT)
    assert panel["landscape_config"] is None
    assert panel["Delta_r_reset"] in CAUSAS_MONITOR


# ── el canal IAP: CKMMonitor construye la config ─────────────────────────────

def test_el_canal_construye_la_config_sin_W_y_sin_theta_W(tmp_path, monkeypatch) -> None:
    """
    CKMMonitor arma la Config en __init__, cuando W todavía no existe, y sin
    θ_W ni scale (decisión de delamor, 7 oct — opción iv).

    Es singleton, así que se resetea la instancia y se redirige su _state a
    tmp_path para no escribir en el repo.
    """
    import iap_chatroom.ckm_monitor as mod

    monkeypatch.setattr(mod, "_STATE_DIR", tmp_path)
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    cm = mod.CKMMonitor(min_texts=5)

    cfg = cm._landscape_config
    assert cfg.sampling_mode == "uniform"
    assert cfg.scale is None
    assert not hasattr(cfg, "theta_W")
    assert cfg.ciclos == ()                      # sin W no hay nada que medir
    assert cm._monitor._landscape_config is cfg


def test_el_canal_abre_el_bootstrap_y_con_rebuild_suspendido_no_abre_mas(
    tmp_path, monkeypatch
) -> None:
    """
    En el canal vivo la config tiene **un solo ciclo**: el bootstrap.

    Medido, y no es un fallo: `CKMMonitor` construye su CorpusService con
    `rebuild_suspendido=True` (decisión de delamor: W se construye cuando el
    dato distingue y no se reconstruye por mensaje), así que W no vuelve a
    cambiar y D4 no tiene nada más que abrir. La segunda mitad del test
    levanta la suspensión y verifica que ahí sí abre — sin eso, este test no
    podría fallar.
    """
    from dataclasses import dataclass

    import iap_chatroom.ckm_monitor as mod

    monkeypatch.setattr(mod, "_STATE_DIR", tmp_path)
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    cm = mod.CKMMonitor(min_texts=5)
    cfg = cm._landscape_config

    @dataclass
    class _Msg:
        text: str
        device_id: str = "d1"

    for texto in TEXTS:                          # 5 mensajes: cruza min_texts
        cm.on_message(_Msg(text=texto))
    assert len(cfg.ciclos) == 1
    assert cfg.ciclos[0].causa == CAUSA_BOOTSTRAP
    assert cfg.vigente(cm._corpus.get_W()) is True

    for texto in TEXTS_NUEVOS:                   # W no se reconstruye
        cm.on_message(_Msg(text=texto))
    assert len(cfg.ciclos) == 1, "con rebuild suspendido no hay ciclo nuevo"

    # Levantada la suspensión, el siguiente mensaje reconstruye W y Monitor
    # abre ciclo. Toca un privado del corpus a propósito: es la única forma
    # de ejercitar D4 en el canal sin cambiar su configuración declarada.
    cm._corpus._rebuild_suspendido = False
    cm.on_message(_Msg(text="red flag laws remove weapons from dangerous people"))

    assert len(cfg.ciclos) == 2, "el canal no abrió ciclo tras un rebuild real"
    assert cfg.ciclos[1].causa in (*CAUSAS_MONITOR, "W_distinta")
    assert cfg.vigente(cm._corpus.get_W()) is True
