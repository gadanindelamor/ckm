"""
test_calibrate_mecanismo.py — TASK_calibrate_mecanismo_v1, CP1

`calibrate` como función: recibe **una copia** de W y devuelve el registro
(`valores`, `estado`, `condiciones`).

Los tres estados (delamor, 10 oct; **nombres provisionales**):

| estado | qué dice |
|---|---|
| `calibrado` | se ejecutó y **separa** |
| `no_calibrado` | **se ejecutó y no separa**, con la causa |
| `nulo_calibrado` | **no hubo calibración**: el UNKNOWN de la calibración |

Hay un test por estado y uno que exige que **`nulo_calibrado` nunca se confunda
con `no_calibrado`**: los dos dejan `valores` vacío y son distintos — uno es
"miré y no encontré", el otro es "no miré".

El cuarto estado propuesto —calibración de otro sha, "fuera de condiciones"—
**no está implementado**: espera la confirmación de delamor. Hay un test que
afirma que hoy no existe, para que si aparece sea por una decisión y no de
costado.

**`n_runs` bajo a propósito.** Cada punto de la grilla es un
`count_attractors`, y el costo crece con N y con `n_runs`. Los tests usan N y
`n_runs` chicos y **lo declaran**: lo que verifican es el mecanismo y los
estados, no el valor de ningún umbral.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
from calibrate import (                                       # noqa: E402
    CALIBRADO,
    ESTADOS,
    GRILLA_LAMBDA_DEFAULT,
    NO_CALIBRADO,
    NULO_CALIBRADO,
    calibrate,
    escala_de,
    extremo_colapso,
    extremo_expansion,
    interpolar,
    registro_nulo,
)

N_RUNS_TEST = 120          # chico a propósito: ver el docstring del módulo


def _W_con_tension(n: int = 12, seed: int = 0) -> np.ndarray:
    """Una W simétrica con signos mezclados: el caso que tiene que separar."""
    rng = np.random.default_rng(seed)
    W = rng.uniform(-1.0, 1.0, size=(n, n))
    W = (W + W.T) / 2.0
    np.fill_diagonal(W, 0.0)
    return W


# ── el patrón no tiene magnitud propia ─────────────────────────────────────

def test_la_escala_sale_de_la_misma_W() -> None:
    """
    Si el patrón trajera su escala, habría que calibrar el patrón. La toma de
    la W que se está calibrando.
    """
    W = _W_con_tension()
    assert escala_de(W) == pytest.approx(np.max(np.abs(W)))

    W_col = extremo_colapso(W)
    fuera = ~np.eye(W.shape[0], dtype=bool)
    assert np.allclose(W_col[fuera], escala_de(W)), "el colapso no usa la escala de W"
    assert np.allclose(np.diag(W_col), 0.0), "la diagonal del extremo no es cero"


def test_el_colapso_es_todo_positivo_e_igual() -> None:
    """Todo tira para el mismo lado: el paisaje pierde órbitas."""
    W_col = extremo_colapso(_W_con_tension())
    fuera = ~np.eye(W_col.shape[0], dtype=bool)
    assert (W_col[fuera] > 0).all()
    assert len(set(np.round(W_col[fuera], 12))) == 1


def test_la_expansion_invierte_una_fraccion_y_es_simetrica() -> None:
    W = _W_con_tension()
    W_exp = extremo_expansion(W, fraccion=0.5, seed=0)
    assert np.allclose(W_exp, W_exp.T), "el extremo dejó de ser simétrico"
    iu = np.triu_indices(W.shape[0], k=1)
    invertidos = int(np.sum(np.sign(W_exp[iu]) != np.sign(W[iu])))
    # la fracción pedida, sobre los pares que tenían signo
    assert invertidos == pytest.approx(0.5 * len(iu[0]), abs=2)


def test_la_expansion_con_la_misma_semilla_da_lo_mismo() -> None:
    """
    Sin semilla, dos calibraciones de la misma W darían extremos distintos y el
    margen no sería comparable entre mesetas.
    """
    W = _W_con_tension()
    assert np.array_equal(extremo_expansion(W, seed=7),
                          extremo_expansion(W, seed=7))
    assert not np.array_equal(extremo_expansion(W, seed=7),
                              extremo_expansion(W, seed=8))


def test_la_interpolacion_no_tiene_dimension() -> None:
    """`λ=0` es W y `λ=1` es el extremo. Sin unidades en el medio."""
    W = _W_con_tension()
    W_col = extremo_colapso(W)
    assert np.allclose(interpolar(W, W_col, 0.0), W)
    assert np.allclose(interpolar(W, W_col, 1.0), W_col)
    assert np.allclose(interpolar(W, W_col, 0.5), (W + W_col) / 2.0)


# ── la W vigente no se toca nunca ──────────────────────────────────────────

def test_la_W_que_entra_sale_igual_bit_a_bit() -> None:
    """
    *Simular sobre la foto: nada entra* (definición del 6 oct). Es la condición
    para que calibrar en la meseta no sea medir la meseta que se está midiendo.
    """
    W = _W_con_tension()
    antes = W.copy()
    calibrate(W, w_sha="x", n_runs=N_RUNS_TEST)
    assert np.array_equal(W, antes), "calibrate modificó la W que recibió"


# ── un test por estado ─────────────────────────────────────────────────────

def test_estado_calibrado_cuando_el_umbral_separa() -> None:
    """
    **Respuesta conocida.** Con una W con tensión real, el extremo de colapso
    pierde órbitas, así que hay un umbral entre "sin cambio" y "colapso".
    """
    r = calibrate(_W_con_tension(), w_sha="sha_de_prueba", n_runs=N_RUNS_TEST)
    assert r["estado"] == CALIBRADO
    assert r["valores"]["D_CKM_THRESHOLD"] is not None
    c = r["condiciones"]
    assert c["margen_separacion"] > 0
    assert c["d_sin_cambio"] == pytest.approx(0.0), (
        "λ=0 tiene que dar D_ckm 0: es la misma W contra su propio baseline"
    )
    # el umbral cae ENTRE los dos extremos, no en uno de ellos
    assert c["d_sin_cambio"] < r["valores"]["D_CKM_THRESHOLD"] < c["d_colapso"]


def test_estado_no_calibrado_cuando_no_hay_separacion() -> None:
    """
    **Se ejecutó y no separa**, con la causa. Caso construido: una W que **ya
    es** el extremo de colapso, así que λ=0 y λ=1 son la misma matriz y no hay
    nada que separar.

    Y **no inventa un valor**: `valores` queda vacío.
    """
    W_ya_colapsada = extremo_colapso(_W_con_tension())
    r = calibrate(W_ya_colapsada, w_sha="x", n_runs=N_RUNS_TEST)
    assert r["estado"] == NO_CALIBRADO, r["condiciones"].get("causa")
    assert r["valores"] == {}, "inventó un umbral sin separación"
    assert r["condiciones"]["causa"] in ("sin_separacion", "d_ckm_no_medible")


def test_estado_no_calibrado_con_W_sin_escala() -> None:
    """Una W toda ceros no tiene escala de la que sacar el extremo."""
    r = calibrate(np.zeros((8, 8)), w_sha="x", n_runs=N_RUNS_TEST)
    assert r["estado"] == NO_CALIBRADO
    assert r["condiciones"]["causa"] == "W_sin_escala"
    assert r["valores"] == {}


def test_estado_nulo_calibrado_cuando_no_se_ejecuto() -> None:
    """
    **El UNKNOWN de la calibración.** No hubo calibración: no se ejecutó.
    """
    for W in (None, np.array([])):
        r = calibrate(W, w_sha="x", n_runs=N_RUNS_TEST)
        assert r["estado"] == NULO_CALIBRADO
        assert r["valores"] == {}
        assert r["condiciones"]["causa"] == "sin_W"

    r = registro_nulo("no_hay_registro", w_sha="y")
    assert r["estado"] == NULO_CALIBRADO
    assert r["condiciones"]["causa"] == "no_hay_registro"


def test_nulo_calibrado_NUNCA_se_confunde_con_no_calibrado() -> None:
    """
    **Pedido de delamor.** Los dos dejan `valores` vacío y son distintos: uno
    es *"miré y no encontré"*, el otro es *"no miré"*.

    Es el mismo criterio que separó `OP_SILENCE` de `UNKNOWN` de `SKIP` en el
    canal, y un archivo roto de un estado de otra meseta en `should_rebuild`:
    **el mismo efecto por dos causas distintas no es un estado.**
    """
    assert NULO_CALIBRADO != NO_CALIBRADO
    assert len(set(ESTADOS)) == 3

    nulo = calibrate(None, w_sha="x")
    no_cal = calibrate(extremo_colapso(_W_con_tension()), w_sha="x",
                       n_runs=N_RUNS_TEST)

    assert nulo["valores"] == no_cal["valores"] == {}, (
        "el test necesita que los dos dejen valores vacío"
    )
    assert nulo["estado"] != no_cal["estado"], (
        "los dos estados colapsaron en uno: no se puede saber si se miró"
    )
    # y la causa distingue POR QUÉ, no sólo que son distintos
    assert nulo["condiciones"]["causa"] == "sin_W"
    assert no_cal["condiciones"]["causa"] != "sin_W"


def test_no_hay_un_cuarto_estado_todavia() -> None:
    """
    El cuarto —calibración de otro sha, *"fuera de condiciones"*— está
    **propuesto y no implementado**: espera la confirmación de delamor.

    Este test afirma que hoy no existe, **para que si aparece sea por una
    decisión y no de costado**. Cuando se confirme, tiene que fallar.
    """
    assert len(ESTADOS) == 3, (
        f"apareció un estado nuevo sin pasar por la decisión: {ESTADOS}"
    )
    assert "fuera_de_condiciones" not in ESTADOS


# ── el registro: las condiciones viajan con los valores ────────────────────

def test_el_registro_declara_las_condiciones() -> None:
    """
    delamor: *un umbral sin sus condiciones es una etiqueta sin origen.*
    """
    r = calibrate(_W_con_tension(), w_sha="sha_abc", representacion="presencia",
                  n_runs=N_RUNS_TEST, escala_desde_traza=None)
    c = r["condiciones"]
    assert c["w_sha"] == "sha_abc"
    assert c["representacion"] == "presencia"
    assert c["patron"] == "extremos + lambda"
    assert c["grilla_lambda"] == list(GRILLA_LAMBDA_DEFAULT)
    assert c["n_runs"] == N_RUNS_TEST
    assert c["n_evaluaciones"] == len(GRILLA_LAMBDA_DEFAULT)
    assert c["escala_desde_traza"] is None, "primer ciclo: sólo extremos"
    assert c["estados_provisionales"] is True


def test_sin_clock_el_reloj_queda_desconocido_y_no_se_inventa() -> None:
    """
    Inventar un `time.time()` acá haría que la traza de la calibración dijera
    otro reloj que el resto de la del canal, sin decirlo.
    """
    r = calibrate(_W_con_tension(), w_sha="x", n_runs=N_RUNS_TEST)
    assert r["condiciones"]["reloj"] == "desconocido"
    assert r["condiciones"]["t"] is None

    r2 = calibrate(_W_con_tension(), w_sha="x", n_runs=N_RUNS_TEST,
                   clock={"reloj": "canal", "t": 123.0})
    assert r2["condiciones"]["reloj"] == "canal"
    assert r2["condiciones"]["t"] == 123.0


def test_la_curva_entera_queda_en_el_registro() -> None:
    """
    Sin la curva, el margen es un número sin de dónde salió. Con ella se puede
    ver la forma, que es lo que el test de abajo mide.
    """
    r = calibrate(_W_con_tension(), w_sha="x", n_runs=N_RUNS_TEST)
    curva = r["condiciones"]["curva"]
    assert len(curva) == len(GRILLA_LAMBDA_DEFAULT)
    assert [p["lambda"] for p in curva] == list(GRILLA_LAMBDA_DEFAULT)
    assert all("n_eff" in p and "d_ckm" in p and "frac_rec" in p for p in curva)


def test_la_no_monotonia_queda_declarada() -> None:
    """
    **Medido, no supuesto.** Con N=12 la curva da
    `0.0 → 0.749 → 0.745 → 0.606 → 0.601`: el **extremo de colapso no es el
    punto de mayor deformación**, y λ intermedios dan menos `N_eff` que λ=1.

    El patrón es de delamor —el colapso es λ=1 **por construcción**—, así que
    `calibrate` **no cambia la definición**: el margen sigue siendo entre los
    extremos. Lo que hace es **declarar el máximo y dónde cae**, para que un
    margen chico por no-monotonía no se lea como poca separación.

    Este test no exige que la curva sea no monótona —eso depende de la W—:
    exige que el registro **diga cuál de las dos cosas pasó**.
    """
    r = calibrate(_W_con_tension(), w_sha="x", n_runs=N_RUNS_TEST)
    c = r["condiciones"]
    assert "curva_monotona" in c
    assert "colapso_es_el_maximo" in c
    assert "d_max" in c and "lambda_de_d_max" in c
    assert c["d_max"] >= c["d_colapso"], "el máximo es menor que el extremo"
    if not c["colapso_es_el_maximo"]:
        assert c["lambda_de_d_max"] != GRILLA_LAMBDA_DEFAULT[-1]


def test_el_mismo_seed_da_el_mismo_registro() -> None:
    """Sin esto, dos calibraciones de la misma W no serían comparables."""
    W = _W_con_tension()
    a = calibrate(W, w_sha="x", n_runs=N_RUNS_TEST, seed=3)
    b = calibrate(W, w_sha="x", n_runs=N_RUNS_TEST, seed=3)
    assert a["valores"] == b["valores"]
    assert a["condiciones"]["margen_separacion"] == \
        b["condiciones"]["margen_separacion"]


def test_el_umbral_calibrado_no_es_el_hardcodeado() -> None:
    """
    **Lo que el CP1 NO afirma.** `coco.py` tiene `D_CKM_THRESHOLD = 0.40` con
    `calibrado=False` al lado. El umbral que sale de acá **no tiene por qué
    coincidir**, y que se parezca no valida nada: es una W sintética, un `seed`
    y un `n_runs` chico.

    El test afirma que el mecanismo **devuelve un número propio**, no que ese
    número sea el correcto. Lo segundo necesita el campo plantado
    (`TASK_tests_instrumento_v1` CP6), que no está acá.
    """
    r = calibrate(_W_con_tension(), w_sha="x", n_runs=N_RUNS_TEST)
    v = r["valores"]["D_CKM_THRESHOLD"]
    assert isinstance(v, float)
    assert 0.0 < v < 1.0, f"el umbral cayó fuera de [0,1]: {v}"
