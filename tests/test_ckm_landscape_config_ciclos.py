"""
test_ckm_landscape_config_ciclos.py — verificación de TASK_CKMlandscapeConfig_v2
(criterio, I1–I7, transición única) y v3 (D1–D3).

Lo que cada test cierra está en su docstring. Los que pueden fallar por diseño
—el de hilos y el de la señal posterior al rebuild— están marcados.

No testea la clase congelada CKMlandscapeConfigV1: eso es
tests/test_ckm_landscape_config.py, que sigue en pie hasta el CP3.
"""

from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

import numpy as np
import pytest

_SERVICES = Path(__file__).resolve().parent.parent / "services"
if str(_SERVICES) not in sys.path:
    sys.path.insert(0, str(_SERVICES))

from ckm_landscape_config import (          # noqa: E402
    CAUSA_BOOTSTRAP,
    CKMlandscapeConfig,
    Ciclo,
    ciclo_desde_registro_plano_v1,
    medido,
)
from coco import COCO                        # noqa: E402

_W_PATH = _SERVICES / "W_ckm_corpus_v2.json"

# Valores medidos declarados en la TASK v2/v3 para W_ckm_corpus_v2.
MU_NONZERO = 0.005977
MU_GLOBAL  = 0.004519


@pytest.fixture(scope="module")
def W() -> np.ndarray:
    return np.array(json.loads(_W_PATH.read_text())["W"], dtype=float)


@pytest.fixture
def W_otra(W: np.ndarray) -> np.ndarray:
    """Otra W con el mismo N: un par distinto alcanza para cambiar el sha."""
    W2 = W.copy()
    W2[0, 1] = W2[1, 0] = W2[0, 1] + 0.5
    return W2


@pytest.fixture
def cfg(W: np.ndarray) -> CKMlandscapeConfig:
    return CKMlandscapeConfig.create(W, sampling_mode="uniform", scale="log")


# ── valores medidos ──────────────────────────────────────────────────────────

def test_medido_coincide_con_los_valores_declarados(W: np.ndarray) -> None:
    """Lo medido de v2 da los mismos números que v1 sobre la misma W."""
    m = medido(W)
    assert m["N"] == 32
    assert round(m["mu_W_nonzero"], 6) == MU_NONZERO
    assert round(m["mu_W_global"], 6) == MU_GLOBAL


def test_beta_c_global_coincide_con_coco(W: np.ndarray) -> None:
    """β_c global es la misma fórmula que COCO.beta_c_corpus (criterio v2)."""
    m = medido(W)
    assert m["beta_c_global"] == pytest.approx(COCO(W=W).beta_c_corpus(), rel=1e-12)


def test_medido_rechaza_W_no_cuadrada() -> None:
    with pytest.raises(ValueError, match="cuadrada"):
        medido(np.zeros((3, 4)))


# ── I1: inmutabilidad en el registro ─────────────────────────────────────────

def test_I1_un_ciclo_cerrado_no_cambia(cfg: CKMlandscapeConfig, W_otra: np.ndarray) -> None:
    """La config gana ciclos; los anteriores quedan iguales por valor."""
    antes = cfg.ciclos[0]
    copia = Ciclo(**antes.to_dict())
    assert cfg.abrir_ciclo(W_otra, "rebuild", time.time()) is True
    assert cfg.ciclos[0] == copia
    assert len(cfg.ciclos) == 2


def test_I1_el_ciclo_es_inmutable(cfg: CKMlandscapeConfig) -> None:
    with pytest.raises(Exception):
        cfg.ciclo_vigente.causa = "otra"          # frozen dataclass


def test_I1_ciclos_es_tupla(cfg: CKMlandscapeConfig) -> None:
    """Devolver una tupla es lo que impide editar la traza desde afuera."""
    assert isinstance(cfg.ciclos, tuple)


# ── I2: ciclo vigente único ──────────────────────────────────────────────────

def test_I2_hay_un_ciclo_desde_la_construccion(cfg: CKMlandscapeConfig) -> None:
    assert len(cfg.ciclos) == 1
    assert cfg.ciclo_vigente is cfg.ciclos[-1]
    assert cfg.ciclo_vigente.causa == CAUSA_BOOTSTRAP


def test_I2_el_vigente_es_siempre_el_ultimo(cfg: CKMlandscapeConfig, W_otra: np.ndarray) -> None:
    cfg.abrir_ciclo(W_otra, "rebuild", time.time())
    assert cfg.ciclo_vigente is cfg.ciclos[-1]
    assert cfg.ciclo_vigente.w_version_id != cfg.ciclos[0].w_version_id


def test_I2_sin_ciclos_el_get_levanta(W: np.ndarray) -> None:
    """Una config sin ciclo no tiene vigencia que devolver; no devuelve None."""
    vacia = CKMlandscapeConfig(sampling_mode="uniform")
    with pytest.raises(RuntimeError, match="ningún ciclo"):
        _ = vacia.ciclo_vigente


# ── I3: vigencia ─────────────────────────────────────────────────────────────

def test_I3_vigente_con_su_W_y_no_con_otra(cfg, W, W_otra) -> None:
    assert cfg.vigente(W) is True
    assert cfg.vigente(W_otra) is False


# ── I4: separación de origen ─────────────────────────────────────────────────

def test_I4_sampling_mode_es_obligatorio() -> None:
    with pytest.raises(TypeError):
        CKMlandscapeConfig()                       # type: ignore[call-arg]


def test_I4_sampling_mode_invalido_falla() -> None:
    with pytest.raises(ValueError, match="sampling_mode"):
        CKMlandscapeConfig(sampling_mode="ninguno")


def test_I4_scale_es_opcional_y_validada() -> None:
    """I4 revisada (7 oct): lo declarado se exige según quién lo usa.

    scale hoy sólo lo usa la UI, así que es opcional; si se pasa, se valida.
    """
    assert CKMlandscapeConfig(sampling_mode="uniform").scale is None
    with pytest.raises(ValueError, match="scale"):
        CKMlandscapeConfig(sampling_mode="uniform", scale="cuadratica")


def test_I4_theta_W_no_es_campo_de_la_config(cfg: CKMlandscapeConfig) -> None:
    """θ_W salió de la config (delamor, 7 oct): es parámetro del Gatekeeper."""
    assert not hasattr(cfg, "theta_W")
    assert "theta_W" not in cfg.to_dict()
    assert "theta_W" not in cfg.ciclo_vigente.to_dict()


def test_I4_lo_medido_no_es_parametro(W: np.ndarray) -> None:
    with pytest.raises(TypeError):
        CKMlandscapeConfig(sampling_mode="uniform", N=32)   # type: ignore[call-arg]


# ── I5: dependencia ──────────────────────────────────────────────────────────

def test_I5_misma_W_no_abre_ciclo(cfg: CKMlandscapeConfig, W: np.ndarray) -> None:
    """Mismo w_version_id ⇒ mismo medido ⇒ un ciclo nuevo no agrega nada."""
    assert cfg.abrir_ciclo(W, "rebuild", time.time()) is False
    assert len(cfg.ciclos) == 1


def test_I5_dos_ciclos_con_el_mismo_sha_tienen_el_mismo_medido(W, W_otra) -> None:
    c = CKMlandscapeConfig.create(W, sampling_mode="uniform")
    c.abrir_ciclo(W_otra, "rebuild", time.time())
    c.abrir_ciclo(W, "rebuild", time.time())       # vuelve a la primera W
    primero, tercero = c.ciclos[0], c.ciclos[2]
    assert primero.w_version_id == tercero.w_version_id
    campos = ("N", "mu_W_nonzero", "mu_W_global", "beta_c_nonzero", "beta_c_global")
    assert all(getattr(primero, k) == getattr(tercero, k) for k in campos)


def test_rebuild_con_nodos_distintos_y_el_mismo_N_abre_ciclo(cfg, W_otra) -> None:
    """D7, medido 4/4: la señal es el sha de W, no su tamaño."""
    assert len(W_otra) == cfg.ciclos[0].N          # mismo N
    assert cfg.abrir_ciclo(W_otra, "estructural", time.time()) is True
    assert cfg.ciclos[1].N == cfg.ciclos[0].N      # y el ciclo se abrió igual


# ── I6: tiempo ───────────────────────────────────────────────────────────────

def test_I6_con_senal_la_deriva_es_no_negativa(W: np.ndarray) -> None:
    t0 = time.time()
    c = CKMlandscapeConfig.create(W, sampling_mode="uniform", t_senal=t0)
    assert c.deriva() >= 0


def test_I6_sin_senal_la_deriva_es_nula_no_cero(cfg: CKMlandscapeConfig) -> None:
    """Nula, no cero: no hubo deriva que medir."""
    assert cfg.ciclo_vigente.t_senal is None
    assert cfg.deriva() is None


def test_I6_senal_posterior_al_rebuild_falla(W: np.ndarray) -> None:
    """Puede fallar por diseño: t_senal > t_rebuild no es un estado válido."""
    t = time.time()
    c = CKMlandscapeConfig(sampling_mode="uniform")
    with pytest.raises(ValueError, match="t_senal"):
        c.abrir_ciclo(W, "rebuild", t, t_senal=t + 10.0)


def test_I6_la_deriva_mide_lo_que_opero_sobre_una_W_obsoleta(W: np.ndarray) -> None:
    c = CKMlandscapeConfig(sampling_mode="uniform")
    c.abrir_ciclo(W, "rebuild", 1000.0, t_senal=970.0)
    assert c.deriva() == pytest.approx(30.0)


# ── I7: traza en el panel ────────────────────────────────────────────────────

def test_I7_el_panel_lleva_identidad_declarado_y_vigente_sin_historia(cfg, W_otra) -> None:
    cfg.abrir_ciclo(W_otra, "rebuild", time.time())
    p = cfg.panel()
    assert p["config_id"] == cfg.config_id
    assert p["sampling_mode"] == "uniform"
    assert p["ciclo_vigente"]["w_version_id"] == cfg.ciclo_vigente.w_version_id
    assert "ciclos" not in p                       # la historia no viaja


def test_I7_el_panel_es_serializable(cfg: CKMlandscapeConfig) -> None:
    json.dumps(cfg.panel())


# ── D2: el set es síncrono ───────────────────────────────────────────────────

def test_D2_al_retornar_abrir_ciclo_el_nuevo_ya_es_el_vigente(cfg, W_otra) -> None:
    sha_antes = cfg.ciclo_vigente.w_version_id
    abrio = cfg.abrir_ciclo(W_otra, "rebuild", time.time())
    assert abrio is True
    assert cfg.ciclo_vigente.w_version_id != sha_antes
    assert cfg.vigente(W_otra) is True


# ── D3: el get es consistente ────────────────────────────────────────────────

def test_D3_el_get_nunca_devuelve_un_ciclo_mezclado(W, W_otra) -> None:
    """
    Puede fallar: si el reemplazo y la lectura no fueran atómicos, un lector
    vería un ciclo con el sha de una W y el medido de la otra.

    Hay concurrencia real medida en el canal (BANDEJA, REPORTE CP0 punto 2):
    lector en un hilo de Gradio, escritor en el event loop.
    """
    cfg = CKMlandscapeConfig.create(W, sampling_mode="uniform")
    esperado = {
        cfg.ciclos[0].w_version_id: medido(W)["mu_W_global"],
        __import__("w_version").sha256_W(W_otra): medido(W_otra)["mu_W_global"],
    }
    parar = threading.Event()
    mezclados: list[tuple] = []

    def lector() -> None:
        while not parar.is_set():
            c = cfg.ciclo_vigente
            if esperado.get(c.w_version_id) != c.mu_W_global:
                mezclados.append((c.w_version_id, c.mu_W_global))

    h = threading.Thread(target=lector, daemon=True)
    h.start()
    try:
        for i in range(200):
            cfg.abrir_ciclo(W_otra if i % 2 == 0 else W, "rebuild", time.time())
    finally:
        parar.set()
        h.join(timeout=5)

    assert mezclados == [], f"ciclos mezclados: {mezclados[:3]}"


def test_D3_el_panel_no_se_parte_con_un_set_concurrente(W, W_otra) -> None:
    """El panel se arma bajo el mismo lock que el reemplazo."""
    cfg = CKMlandscapeConfig.create(W, sampling_mode="uniform")
    parar = threading.Event()
    malos: list[dict] = []

    def lector() -> None:
        while not parar.is_set():
            p = cfg.panel()
            cv = p["ciclo_vigente"]
            if cv is None or set(cv) != set(cfg.ciclos[0].to_dict()):
                malos.append(p)

    h = threading.Thread(target=lector, daemon=True)
    h.start()
    try:
        for i in range(200):
            cfg.abrir_ciclo(W_otra if i % 2 == 0 else W, "rebuild", time.time())
    finally:
        parar.set()
        h.join(timeout=5)

    assert malos == []


# ── serialización con historia ───────────────────────────────────────────────

def test_serializacion_completa_recarga_igual(cfg, W_otra) -> None:
    cfg.abrir_ciclo(W_otra, "rebuild", time.time(), t_senal=time.time() - 1)
    otra = CKMlandscapeConfig.from_json(cfg.to_json())
    assert otra.config_id == cfg.config_id
    assert otra.timestamp == cfg.timestamp
    assert otra.declarado == cfg.declarado
    assert otra.ciclos == cfg.ciclos            # misma historia, por valor
    assert otra.deriva() == cfg.deriva()


def test_to_dict_lleva_la_historia_y_el_panel_no(cfg, W_otra) -> None:
    cfg.abrir_ciclo(W_otra, "rebuild", time.time())
    assert len(cfg.to_dict()["ciclos"]) == 2
    assert "ciclos" not in cfg.panel()


# ── lectura de la traza vieja (P4) ───────────────────────────────────────────

def test_registro_plano_de_v1_se_lee_como_un_ciclo_bootstrap() -> None:
    """No se reescribe ningún archivo histórico: se lee con este mapeo."""
    plano = {
        "N": 32, "mu_W_nonzero": MU_NONZERO, "mu_W_global": MU_GLOBAL,
        "beta_c_nonzero": 10.457544, "beta_c_global": 13.831845,
        "w_version_id": "a" * 64, "theta_W": float("nan"),
        "sampling_mode": "uniform", "scale": "log",
        "config_id": "deadbeef", "timestamp": 1000.0,
    }
    c = ciclo_desde_registro_plano_v1(plano)
    assert c.causa == CAUSA_BOOTSTRAP
    assert c.t_senal is None
    assert c.t_rebuild == 1000.0
    assert c.deriva is None
    assert "theta_W" not in c.to_dict()


def test_el_jsonl_historico_real_se_lee(tmp_path: Path) -> None:
    """Sobre el único JSONL con config v1 serializada que hay en el repo."""
    p = Path(__file__).resolve().parent.parent / "P1P4" / "run_conteo_vs_masa_04oct" / "log_conteo_vs_masa.jsonl"
    if not p.exists():
        pytest.skip(f"no está {p}")
    leidos = 0
    for linea in p.read_text().splitlines():
        if not linea.strip():
            continue
        d = json.loads(linea)
        if d.get("tipo") == "config":
            c = ciclo_desde_registro_plano_v1(d)
            assert c.N > 0 and c.causa == CAUSA_BOOTSTRAP
            leidos += 1
    assert leidos > 0, "el JSONL no tenía ningún registro tipo=config"
