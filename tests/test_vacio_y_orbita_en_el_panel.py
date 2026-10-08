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


# ── 3. qué entra a Δ_r — decisión de delamor, CP3 punto 1(a) ────────────────

def test_a_delta_r_entran_solo_los_expulsados(corpus, tmp_path) -> None:
    """
    A Δ_r entran los pares expulsados en TODAS las fases, no los de la fase
    que cayó en max_iter.

    Decisión de delamor (8 oct, CP3 punto 1(a)). Antes entraban los de una
    sola fase, que es lo que el CP1 midió divergiendo según la paridad.
    """
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    assert float(np.sum(m._Delta_r)) == 2 * p["n_expulsados"], \
        "Δ_r cuenta cada par expulsado dos veces (simétrica)"


def test_la_torsion_se_acumula_aparte(corpus, tmp_path) -> None:
    """Δ_r_torsion es un objeto propio y viaja en el panel."""
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    assert float(np.sum(m._Delta_r_torsion)) == 2 * p["n_torsion"]
    assert p["Delta_r_torsion_sum"] == float(np.sum(m._Delta_r_torsion))


def test_la_torsion_se_resetea_con_el_ciclo(corpus, tmp_path) -> None:
    """Δ_r_torsion muere con el ciclo, igual que Δ_r."""
    m, cfg = _monitor(corpus, tmp_path)
    m.evaluate(PROMPT)
    corpus.ingest(NUEVOS)
    m._invalidar_si_W_cambio(corpus.get_nodes())
    assert not m._Delta_r_torsion.any()


def test_en_punto_fijo_delta_r_es_lo_mismo_que_antes(corpus, tmp_path) -> None:
    """
    La invariante de compatibilidad, ahora sobre Δ_r: con torsión vacía,
    expulsados == los pares de la fase, así que Δ_r queda idéntico a lo que
    escribía antes del cambio.
    """
    m, cfg = _monitor(corpus, tmp_path)
    p = m.evaluate(PROMPT)
    if p["periodo_orbita"] == 1:
        assert p["n_expulsados"] == p["n_rejected_pairs"]
        assert float(np.sum(m._Delta_r)) == 2 * p["n_rejected_pairs"]
        assert not m._Delta_r_torsion.any()


# ── W sintética, declarada ──────────────────────────────────────────────────
#
# Construida a mano para esta prueba. **No sale de ningún corpus.** Se la buscó
# barriendo W simétricas de 4 nodos con pesos en {−1, −0.5, 0, 0.5, 1} hasta
# encontrar una que, desde sigma_prompt = [1, 1, 1, −1], relaja a una órbita de
# **período 2 en la que la fase que cae en max_iter expulsa MÁS pares que los
# expulsados en toda la órbita**. Es la condición que hace que la decisión 1(a)
# se pueda distinguir de la implementación anterior; en el corpus de estos
# tests la órbita es de período 1 y las dos coinciden.
#
# Medido sobre esta W: período 2, cola 1, fase en max_iter = [1, −1, −1, −1].
#   expulsados (en las dos fases) = {(0,1), (0,2)}      → 2
#   torsión    (en una sola)      = {(1,2)}             → 1
#   la fase que cae en max_iter   = {(0,1), (0,2), (1,2)} → 3
# O sea que (1,2) entraba a Δ_r con la implementación vieja y ahora va a la
# torsión, que no entra a W_eff.
W_SINTETICA = np.array([
    [0.0,  0.5,  0.0,  1.0],
    [0.5,  0.0, -0.5,  0.0],
    [0.0, -0.5,  0.0, -0.5],
    [1.0,  0.0, -0.5,  0.0],
])
SIGMA_SINTETICA = np.array([1., 1., 1., -1.])


@pytest.fixture
def monitor_sintetico(tmp_path, monkeypatch):
    """
    Monitor sobre la W sintética, con la relajación **real**.

    No se parchea la órbita: se parchea de dónde sale W y qué declara el
    prompt, y la órbita de período 2 la produce `relax_orbit` sobre esos dos
    datos. Es lo que pidió delamor para dar el test por bueno.
    """
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=5, top_k=32)
    c.ingest(TEXTS)
    monkeypatch.setattr(c, "get_W", lambda: W_SINTETICA)
    monkeypatch.setattr(c, "get_nodes", lambda: ["n0", "n1", "n2", "n3"])
    cfg = CKMlandscapeConfig.create(W_SINTETICA, sampling_mode="uniform", n_runs=10)
    m = MonitorService(c, storage_path=str(tmp_path / "m.jsonl"),
                       n_runs_attractors=10, landscape_config=cfg)
    monkeypatch.setattr(m._extractor, "evaluate",
                        lambda texto, ns: SIGMA_SINTETICA.copy())
    return m, c


def test_la_W_sintetica_relaja_a_periodo_2_de_verdad(monitor_sintetico) -> None:
    """Primero se verifica el supuesto: la órbita sale de la dinámica."""
    m, c = monitor_sintetico
    p = m.evaluate(PROMPT)
    assert p["periodo_orbita"] == 2
    assert p["cola_orbita"] == 1
    assert p["n_expulsados"] == 2
    assert p["n_torsion"] == 1
    assert p["n_rejected_pairs"] == 3, \
        "la fase que cae en max_iter expulsa 3; los expulsados en la órbita son 2"


def test_con_periodo_2_real_delta_r_NO_es_la_fase(monitor_sintetico) -> None:
    """
    El test que distingue. Los anteriores no podían fallar.

    Medido: con el corpus de estos tests la órbita es de período 1, así que
    `expulsados == rejected` y volver Δ_r a la fase pasaba los 272 tests. Con
    la W sintética, la fase expulsa 3 pares y los expulsados de la órbita son
    2, así que Δ_r tiene que llevar 2 y no 3.

    Si Δ_r volviera a escribirse desde la fase, este test falla. Verificado al
    revés antes de darlo por bueno (ver REPORTE CP3i).
    """
    m, c = monitor_sintetico
    p = m.evaluate(PROMPT)

    assert float(np.sum(m._Delta_r)) == 2 * 2, \
        "si Δ_r se escribiera desde la fase, acá valdría 6 y no 4"
    assert m._Delta_r[0, 1] == 1 and m._Delta_r[0, 2] == 1
    assert m._Delta_r[1, 2] == 0, "(1,2) es torsión: no entra a Δ_r"

    assert float(np.sum(m._Delta_r_torsion)) == 2 * 1
    assert m._Delta_r_torsion[1, 2] == 1
    assert p["pares_torsion"] == [("n1", "n2")]


def test_la_torsion_NO_entra_a_W_eff(monitor_sintetico, monkeypatch) -> None:
    """
    W_eff se arma con Δ_r sola. Si la torsión entrara, este test falla.

    Dos pasadas de corrección, las dos medidas al revés y las dos declaradas:

    1. La primera versión sólo comprobaba que W_eff *sería* distinta con la
       torsión, no que Monitor use Δ_r sola. Sumándole la torsión a W_eff
       pasaban los 273.
    2. La segunda capturaba el Δ que Monitor pasa a `_combine_W_Delta`, pero
       miraba **sólo la última llamada**. Y `evaluate` lo llama varias veces
       (L211 para la relajación del prompt, y otra vez en el bloque de
       métricas), así que la última era una que sí usa Δ_r y el test seguía
       pasando con el experimento puesto.

    Esta versión mira **todas** las llamadas: ninguna puede llevar la torsión.
    """
    m, c = monitor_sintetico
    original = m._combine_W_Delta
    vistos = []
    monkeypatch.setattr(m, "_combine_W_Delta",
                        lambda W, D: (vistos.append(np.array(D, copy=True)),
                                      original(W, D))[1])
    p1 = m.evaluate(PROMPT)  # Δ_r y torsión arrancan en cero
    m.evaluate(PROMPT)       # ya hay torsión acumulada

    # Primero el supuesto: si no hubiera torsión, este test pasaría por no
    # tener nada que medir, y eso sería UNKNOWN, no OK.
    assert p1["n_torsion"] > 0, "sin pares de torsión el test no mide nada"
    assert m._Delta_r_torsion.any(), "el test necesita torsión acumulada"
    assert len(vistos) >= 2, "evaluate llama a _combine_W_Delta más de una vez"
    con_torsion = float(np.sum(m._Delta_r + m._Delta_r_torsion))
    for k, D in enumerate(vistos):
        assert float(np.sum(D)) != con_torsion, \
            f"la llamada {k} a _combine_W_Delta lleva la torsión, y no debería"


# ── decisión 4: el ciclo nuevo nace con la órbita, no con una fase ──────────

def test_el_ciclo_nuevo_nace_con_la_orbita_no_con_una_fase(
    monitor_sintetico, monkeypatch
) -> None:
    """
    Decisión de delamor (8 oct, CP3 punto 4): si el salto cae en un período 2,
    el ciclo nuevo **hereda la órbita, no una fase**.

    Mecánicamente: la **primera** escritura de Δ_r del ciclo nuevo —la
    evaluación en la que `abrir_ciclo` devolvió True y Δ_r quedó en ceros—
    tiene que venir de los expulsados de toda la órbita, no de la fase que cayó
    en max_iter.

    Se fuerza el salto cambiando el sha del corpus (que es la señal de ciclo)
    mientras `get_W` sigue devolviendo la W sintética, así la órbita sigue
    siendo de período 2 a los dos lados del salto.
    """
    m, c = monitor_sintetico
    p1 = m.evaluate(PROMPT)
    assert p1["n_torsion"] > 0, "sin torsión el test no mide nada"
    assert p1["Delta_r_reset"] is None

    # el salto: otro sha, misma W sintética
    monkeypatch.setattr(c, "w_sha", lambda: "f" * 64)
    p2 = m.evaluate(PROMPT)

    assert p2["Delta_r_reset"] is not None, "el salto tiene que resetear Δ_r"
    assert p2["periodo_orbita"] == 2
    assert p2["n_expulsados"] == 2 and p2["n_rejected_pairs"] == 3

    # Δ_r del ciclo nuevo: los 2 expulsados de la órbita, no los 3 de la fase
    assert float(np.sum(m._Delta_r)) == 2 * 2, \
        "el ciclo nuevo nació con la fase (6) y no con la órbita (4)"
    assert m._Delta_r[1, 2] == 0, "(1,2) es torsión: no entra al Δ_r del ciclo nuevo"
    assert float(np.sum(m._Delta_r_torsion)) == 2 * 1, \
        "la torsión del ciclo nuevo también arranca de cero y se acumula aparte"
