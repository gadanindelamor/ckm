"""
test_pares_por_orbita.py — CP2a de TASK_monitor_coco_ciclo_orbita_v2

La órbita es el objeto, no la fase que cae en max_iter. Acá se fija la función
pura: las tres clases, su independencia del orden, y la invariante de
compatibilidad en un punto fijo.

No toca Monitor ni COCO: eso es el CP2b.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from landscape_engine import (          # noqa: E402
    fases_de_orbita,
    pares_por_orbita,
    relax_orbit,
)


def _rejected_pairs_de_hoy(sigma_p: np.ndarray, sigma_r: np.ndarray) -> set:
    """Copia literal de MonitorService._rejected_pairs, para comparar."""
    declared = np.where(sigma_p > 0)[0]
    caidos = set(np.where(sigma_r < 0)[0])
    return {(int(declared[a]), int(declared[b]))
            for a in range(len(declared))
            for b in range(a + 1, len(declared))
            if declared[a] in caidos or declared[b] in caidos}


# ── las tres clases ─────────────────────────────────────────────────────────

def test_las_tres_clases_particionan_los_pares_declarados() -> None:
    """Todo par declarado cae en exactamente una clase."""
    sp = np.array([1., 1., 1., 1., -1.])
    fa = np.array([1., -1., 1., 1., 1.])      # cae el 1
    fb = np.array([1., 1., -1., 1., 1.])      # cae el 2
    ac, ex, to = pares_por_orbita(sp, [fa, fb])

    declarados = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert ac | ex | to == set(declarados)
    assert ac & ex == set() and ac & to == set() and ex & to == set()


def test_la_torsion_es_el_par_que_cae_en_una_sola_fase() -> None:
    sp = np.array([1., 1., 1., 1., -1.])
    fa = np.array([1., -1., 1., 1., 1.])
    fb = np.array([1., 1., -1., 1., 1.])
    ac, ex, to = pares_por_orbita(sp, [fa, fb])

    assert (1, 2) in ex                      # toca a los dos nodos que caen
    assert (0, 1) in to and (1, 3) in to     # sólo en la fase A
    assert (0, 2) in to and (2, 3) in to     # sólo en la fase B
    assert ac == {(0, 3)}                    # ninguno de los dos cae


def test_el_nodo_no_declarado_no_entra_en_ninguna_clase() -> None:
    """Sólo se clasifican pares de nodos que sigma_prompt declaró activos."""
    sp = np.array([1., 1., -1.])
    ac, ex, to = pares_por_orbita(sp, [np.array([1., 1., -1.])])
    assert ac | ex | to == {(0, 1)}


# ── independencia del orden ─────────────────────────────────────────────────

def test_intercambiar_las_fases_no_cambia_nada() -> None:
    sp = np.array([1., 1., 1., 1.])
    fa = np.array([1., -1., 1., 1.])
    fb = np.array([1., 1., -1., 1.])
    assert pares_por_orbita(sp, [fa, fb]) == pares_por_orbita(sp, [fb, fa])


def test_repetir_una_fase_no_cambia_nada() -> None:
    """La órbita es un conjunto: una fase listada dos veces no pesa doble."""
    sp = np.array([1., 1., 1.])
    fa = np.array([1., -1., 1.])
    assert pares_por_orbita(sp, [fa]) == pares_por_orbita(sp, [fa, fa])


# ── la invariante de compatibilidad ─────────────────────────────────────────

def test_en_un_punto_fijo_no_hay_torsion_y_expulsados_es_lo_de_hoy() -> None:
    """
    Con una sola fase, `expulsados` es exactamente lo que devuelve
    _rejected_pairs hoy, y la torsión es vacía.

    Es la invariante de compatibilidad de la TASK §1, y vale **a igual
    W_eff** — que es la condición que el CP1 midió que falta a lo largo de un
    recorrido.
    """
    rng = np.random.default_rng(0)
    for _ in range(50):
        N = 6
        sp = rng.choice([1., -1.], size=N)
        fa = rng.choice([1., -1.], size=N)
        ac, ex, to = pares_por_orbita(sp, [fa])
        assert to == set(), "un punto fijo no puede tener torsión"
        assert ex == _rejected_pairs_de_hoy(sp, fa)


def test_con_torsion_vacia_expulsados_sigue_siendo_lo_de_hoy() -> None:
    """Período 2 pero las dos fases expulsan lo mismo: idéntico a hoy."""
    sp = np.array([1., 1., 1.])
    fa = np.array([1., -1., 1.])
    fb = np.array([-1., -1., 1.])            # el 1 cae en las dos
    ac, ex, to = pares_por_orbita(sp, [fa, fb])
    assert (0, 1) in ex and (1, 2) in ex
    assert to == {(0, 2)}                    # el 0 cae sólo en B


def test_sin_fases_levanta() -> None:
    with pytest.raises(ValueError, match="al menos una fase"):
        pares_por_orbita(np.array([1., 1.]), [])


# ── enganche con relax_orbit ────────────────────────────────────────────────

def test_fases_de_orbita_reconstruye_los_estados() -> None:
    """Lo que relax_orbit guarda como bytes vuelve a ser el mismo array."""
    rng = np.random.default_rng(1)
    N = 8
    W = rng.normal(size=(N, N)); W = (W + W.T) / 2; np.fill_diagonal(W, 0.)
    sigma = rng.choice([1., -1.], size=N)
    orbita, periodo, cola, estado = relax_orbit(sigma, W)

    fases = fases_de_orbita(orbita, N)
    assert len(fases) == periodo
    assert all(f.shape == (N,) for f in fases)
    assert any(np.array_equal(f, estado) for f in fases), \
        "el estado que devuelve relax() tiene que ser una de las fases"


def test_sobre_una_W_simetrica_el_periodo_es_1_o_2() -> None:
    """Goles-Chacc et al. (1985): con W simétrica y dinámica síncrona, punto
    fijo o período 2. No se reclama la prueba; se verifica el supuesto."""
    rng = np.random.default_rng(2)
    for _ in range(30):
        N = 10
        W = rng.normal(size=(N, N)); W = (W + W.T) / 2; np.fill_diagonal(W, 0.)
        sigma = rng.choice([1., -1.], size=N)
        assert relax_orbit(sigma, W)[1] in (1, 2)


def test_la_torsion_aparece_sobre_una_orbita_real_de_periodo_2() -> None:
    """
    Construida a mano: dos nodos acoplados negativamente oscilan, y un par
    declarado que los toca queda en torsión.
    """
    W = np.array([[0., -1., 0.],
                  [-1., 0., 0.],
                  [0., 0., 0.]])
    sigma = np.array([1., 1., 1.])
    orbita, periodo, cola, _ = relax_orbit(sigma, W)
    assert periodo == 2, f"se esperaba período 2, dio {periodo}"

    ac, ex, to = pares_por_orbita(sigma, fases_de_orbita(orbita, 3))
    assert to, "con período 2 y nodos que alternan tiene que haber torsión"
    assert ac | ex | to == {(0, 1), (0, 2), (1, 2)}
