"""
check_orientability no mide balance de grafo con signo — xfail por CONCEPTO

CP6 de `TASK_tests_instrumento_v1`, punto 2 del agregado del 11-12 oct. El
xfail es **estricto y conceptual**, no de umbral: no hay valor de `theta` que lo
haga pasar.

Tres razones leídas en `experiments/ckm_topology_module.py`, no de memoria:

1. `build_complex` (`:57`) arma las aristas con `if W[i, j] > theta`. Con
   `theta >= 0` **los negativos no entran**, y con `theta < 0` entran pero
   mezclados con los positivos, sin distinguirse: la arista existe o no, y no
   lleva signo.
2. El BFS de `check_orientability` (`:242`) saltea toda arista con
   `len(tris) != 2`. En un complejo de cliques una arista suele estar en más de
   dos triángulos, así que el grafo dual queda casi vacío y la respuesta tiende
   a "orientable" por falta de aristas duales, no por ausencia de torsión.
3. `check_orientability(edges, triangles)` **no recibe W**: el signo nunca llega
   a la función. Lo que mide es orientabilidad simplicial —el signo de borde
   `d(i,j,k) = +(j,k) − (i,k) + (i,j)`, que depende sólo del ORDEN de los
   índices— y no el balance de Harary, que depende del signo de los pesos.

El caso real: el campo plantado de CP6. Tres grupos que se evitan, un triángulo
con un nodo de cada grupo tiene (−)(−)(−) = − y está **frustrado por
construcción**; `check_orientability` lo informa orientable. Acá se reproduce
el campo mínimo que hace falta para mostrarlo: un triángulo con signos
(+, −, −), balanceado, y otro con (−, −, −), frustrado. Las dos respuestas son
la misma.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_RAIZ))
sys.path.insert(0, str(_RAIZ / "experiments"))

pytest.importorskip("networkx",
                    reason="ckm_topology_module requiere networkx "
                           "(declarado en pyproject.toml)")

from ckm_topology_module import build_complex, check_orientability  # noqa: E402


def _W_tres_grupos() -> np.ndarray:
    """Un nodo por grupo, tres grupos que se evitan: todos los pares entre
    grupos son negativos. Producto de signos (−)(−)(−) = −: frustrado."""
    W = np.array([
        [0.0, -0.5, -0.5],
        [-0.5, 0.0, -0.5],
        [-0.5, -0.5, 0.0],
    ])
    return W


def _W_balanceada() -> np.ndarray:
    """Dos nodos de un grupo y uno de otro: (+)(−)(−) = +. Balanceado."""
    return np.array([
        [0.0, +0.5, -0.5],
        [+0.5, 0.0, -0.5],
        [-0.5, -0.5, 0.0],
    ])


def _indice_frustracion(W: np.ndarray) -> float:
    """Convención de `orbit_analytics.seccion_F.frustracion`: triángulo con
    algún signo 0 no se cuenta. Sin usar la letra `T`, que en
    `topological_profile` es el número de triángulos."""
    import itertools
    S = np.sign(W)
    tot = fr = 0
    for i, j, k in itertools.combinations(range(W.shape[0]), 3):
        a, b, c = S[i, j], S[j, k], S[i, k]
        if 0 in (a, b, c):
            continue
        tot += 1
        if a * b * c < 0:
            fr += 1
    return fr / tot if tot else 0.0


def test_el_indice_de_frustracion_SI_distingue_los_dos_campos() -> None:
    """Control del xfail: el campo frustrado y el balanceado **son
    distinguibles** — con el índice de frustración, que sí lee el signo. Sin
    este control, el xfail de abajo podría ser "los dos campos son iguales"."""
    assert _indice_frustracion(_W_tres_grupos()) == 1.0
    assert _indice_frustracion(_W_balanceada()) == 0.0


@pytest.mark.xfail(strict=True,
                   reason="check_orientability no recibe W y build_complex "
                          "filtra con W > theta: el signo no llega a la "
                          "funcion. Mide orientabilidad simplicial, no balance "
                          "de grafo con signo. Caso real: campo plantado de "
                          "CP6, experiments/sintetico_campo_plantado.py")
@pytest.mark.parametrize("theta", [-1.0, -0.75, -0.25, 0.0, 0.25])
def test_check_orientability_distingue_frustrado_de_balanceado(theta) -> None:
    """**xfail estricto, por concepto.** Si `check_orientability` midiera
    balance, el campo frustrado por construcción y el balanceado tendrían
    respuestas distintas. Se barre `theta` por los dos lados del 0 para que el
    rojo no se lea como un umbral mal elegido: no hay `theta` que lo salve.

    Con `theta >= 0` ninguna arista negativa entra y los dos complejos quedan
    vacíos o iguales; con `theta < 0` las aristas entran pero sin signo.
    """
    r_fr = check_orientability(*build_complex(_W_tres_grupos(), [0, 1, 2], theta)[1:])
    r_ba = check_orientability(*build_complex(_W_balanceada(), [0, 1, 2], theta)[1:])
    assert r_fr["orientable"] != r_ba["orientable"], (
        f"theta={theta}: frustrado -> {r_fr}, balanceado -> {r_ba}"
    )
