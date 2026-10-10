"""
calibrate.py — la calibración como **mecanismo**, no como constantes

`TASK_calibrate_mecanismo_v1`, CP1. delamor:

> La calibración del instrumento es cada vez que es necesaria, como en todo
> instrumento. No es una vez en su vida útil y nunca más; por lo cual el
> instrumento no podría estar calibrado para todos los casos posibles.
> **Implementar la calibración y ver si se calibra. MECANISMO.**

Hasta hoy `D_CKM_THRESHOLD = 0.40` y `FRAC_REC_MIN = 0.60` son constantes en
`coco.py:94-96`. Este módulo **no cambia esos valores**: da una forma de
obtenerlos, y de decir cuándo no se obtuvieron.

**Lo que el docstring de `coco.py` dice, y el código solo no decía** (L17-18):

> *"Los umbrales D_CKM_THRESHOLD y FRAC_REC_MIN se calibraron sobre la forma
> lineal por conteo (REG_destruccion_recuperacion_v1) y NO se recalibraron."*

O sea: **se calibraron contra una cantidad que ya no es la que se compara.** La
forma lineal por conteo es `deprecated_d_ckm` desde el 5 oct 2026; lo que hoy
entra al umbral es `d_ckm`, la forma logarítmica por masa de cuenca. Y `coco.py`
**no tiene ninguna marca `calibrado=False`** —esas están en
`UmbralesCriterioLocal` y en `ckm_landscape_config`—: lo que tiene es esta
declaración en su docstring, que es más fuerte y más precisa que una marca.

No es una contradicción escondida: está escrita. Lo anoto acá porque es la
razón por la que este módulo existe, y porque el número `0.40` **no es
comparable** con el que sale de este mecanismo.

## El patrón no tiene magnitud propia

Si el patrón trajera una escala, habría que calibrar el patrón. Así que los
extremos se sacan **de la misma W** y la interpolación es sin dimensión:

    W_λ = (1 − λ)·W + λ·W_extremo,      λ ∈ [0, 1]

- **colapso**: `W'` con todos los acoplamientos positivos e iguales a la escala
  de W (`max|W|`). Todo tira para el mismo lado: el paisaje pierde órbitas.
- **expansión**: el signo invertido en una **fracción** de los pares.

`calibrate` busca un umbral que **separe** λ=0 (COCO no dispara) de λ=1 (COCO
dispara), y registra el **margen**. Si ninguno separa: **no calibrado**, sin
inventar un valor.

## La W vigente no se toca nunca

Todo corre sobre `W.copy()`. Es la foto de la meseta: *simular sobre la copia,
nada entra* (definición del 6 oct). Hay un test que verifica que la W que entra
sale igual, bit a bit.

## Lo que devuelve: un registro, no valores

delamor: *un umbral sin sus condiciones es una etiqueta sin origen.* Así que
sale `{valores, estado, condiciones}` — contra qué W (`w_sha`), con qué patrón,
con qué grilla, con qué margen y con cuántas corridas.

## Los tres estados (delamor, 10 oct) — nombres PROVISIONALES

| estado | qué dice |
|---|---|
| `calibrado` | se ejecutó y **separa**: hay umbral con margen |
| `no_calibrado` | **se ejecutó y no separa**, con la causa |
| `nulo_calibrado` | **no hubo calibración**: no se ejecutó, o no hay registro |

`nulo_calibrado` es **el UNKNOWN de la calibración**, y **no es lo mismo que
`no_calibrado`**: uno es "miré y no encontré", el otro es "no miré". Los dos
dejan `valores` vacío y son distintos, así que son constantes distintas y hay un
test que exige que nunca se confundan — es el mismo criterio que separó
`OP_SILENCE` de `UNKNOWN` de `SKIP` en el canal, y un archivo roto de un estado
de otra meseta en `should_rebuild`.

**Los nombres los decide delamor.** Estos son provisionales y coherentes con la
marca `calibrado=False` que ya existe (`UmbralesCriterioLocal`,
`ckm_landscape_config`).

**Un cuarto estado está propuesto y NO implementado**: calibración existente
para otro sha ("fuera de condiciones"). Espera la confirmación de delamor. Hoy
ese caso no se produce acá, porque el CP1 no lee registros guardados — eso es el
CP2.

## Recursos

El costo de estimar `N_eff` crece con N y con `n_runs`: cada punto de la grilla
es un `count_attractors`. Queda **declarado** en `condiciones.n_runs` y
`condiciones.n_evaluaciones`, no escondido en un default.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from landscape_engine import count_attractors, d_ckm

# ── los tres estados. Provisionales: los nombres los decide delamor ─────────
CALIBRADO = "calibrado"
NO_CALIBRADO = "no_calibrado"
NULO_CALIBRADO = "nulo_calibrado"

ESTADOS = (CALIBRADO, NO_CALIBRADO, NULO_CALIBRADO)

# Grilla de λ por default. **Declarada, no calibrada**: es el grano con el que
# se busca el umbral. La traza de W_{i−1} la concentra donde las deformaciones
# de verdad ocurren, y eso es el CP4.
GRILLA_LAMBDA_DEFAULT = (0.0, 0.25, 0.5, 0.75, 1.0)

# Fracción de pares con el signo invertido en el extremo de expansión.
# Declarada, no calibrada.
FRACCION_EXPANSION_DEFAULT = 0.5

N_RUNS_DEFAULT = 200   # el de Monitor es 1000; acá es por punto de la grilla
SEED_DEFAULT = 0


def escala_de(W: np.ndarray) -> float:
    """
    La escala de W: `max|W|` fuera de la diagonal.

    De acá sale la magnitud de los extremos, y por eso el patrón **no tiene
    magnitud propia**: la toma de la W que se está calibrando.

    `0.0` si W es toda ceros — y entonces no hay escala, que es una de las
    causas de `no_calibrado`.
    """
    if W.size == 0:
        return 0.0
    fuera = ~np.eye(W.shape[0], dtype=bool)
    return float(np.max(np.abs(W[fuera]))) if fuera.any() else 0.0


def extremo_colapso(W: np.ndarray) -> np.ndarray:
    """
    `W'` con **todos los acoplamientos positivos e iguales a la escala de W**.

    Todo tira para el mismo lado: el paisaje pierde órbitas y `N_eff → 1`. Es
    el extremo "colapso" del patrón, conocido **por construcción** y no por
    haberlo medido.
    """
    e = escala_de(W)
    out = np.full(W.shape, e, dtype=float)
    np.fill_diagonal(out, 0.0)
    return out


def extremo_expansion(W: np.ndarray, *, fraccion: float = FRACCION_EXPANSION_DEFAULT,
                      seed: int = SEED_DEFAULT) -> np.ndarray:
    """
    El signo invertido en una **fracción** de los pares (simétrico).

    `seed` fija qué pares: sin semilla, dos calibraciones de la misma W darían
    extremos distintos y el margen no sería comparable entre mesetas.
    """
    out = W.astype(float).copy()
    n = W.shape[0]
    iu = np.triu_indices(n, k=1)
    if len(iu[0]) == 0:
        return out
    rng = np.random.default_rng(seed)
    cuantos = int(round(fraccion * len(iu[0])))
    elegidos = rng.choice(len(iu[0]), size=cuantos, replace=False)
    i, j = iu[0][elegidos], iu[1][elegidos]
    out[i, j] *= -1.0
    out[j, i] = out[i, j]
    return out


def interpolar(W: np.ndarray, W_extremo: np.ndarray, lam: float) -> np.ndarray:
    """`W_λ = (1 − λ)·W + λ·W_extremo`. Sin dimensión: λ no tiene unidades."""
    return (1.0 - lam) * W.astype(float) + lam * W_extremo.astype(float)


def registro_nulo(causa: str, *, w_sha: Optional[str] = None) -> dict:
    """
    El registro de **`nulo_calibrado`**: no hubo calibración.

    Existe como función para que *"no se calibró"* tenga la **misma forma** que
    *"se calibró"*. Si el no-registro fuera `None`, quien lo consuma tendría que
    inventar la diferencia entre "no miré" y "miré y no encontré", y ahí es
    donde se cuela el relleno de ausencias.
    """
    return {
        "valores": {},
        "estado": NULO_CALIBRADO,
        "condiciones": {"causa": causa, "w_sha": w_sha},
    }


def calibrate(
    W: Optional[np.ndarray],
    *,
    w_sha: Optional[str] = None,
    representacion: str = "presencia",
    grilla_lambda: Sequence[float] = GRILLA_LAMBDA_DEFAULT,
    n_runs: int = N_RUNS_DEFAULT,
    seed: int = SEED_DEFAULT,
    clock: Optional[dict] = None,
    escala_desde_traza: Optional[str] = None,
) -> dict:
    """
    Calibra sobre **una copia** de W y devuelve el registro.

    Qué hace, en una línea: mide `D_ckm` a lo largo de `W_λ` y busca un umbral
    que separe λ=0 de λ=1. El umbral es el **punto medio** del salto y el
    **margen** es el salto: un margen chico dice que el umbral está apoyado en
    poco, y eso viaja en el registro en vez de quedar afuera.

    `W = None` o vacía → **`nulo_calibrado`**: no se ejecutó. No se confunde
    con `no_calibrado`, que es haber corrido y no encontrar separación.

    `clock` es el del canal, si quien llama lo tiene. Sin él, `reloj` queda
    `"desconocido"` y no se inventa un `time.time()` que diría otra cosa que el
    resto de la traza.

    `escala_desde_traza` es el sha de W_{i−1} cuando la grilla viene concentrada
    por la traza de la meseta anterior (CP4). Hoy entra como dato declarado y
    **este CP1 no la usa para nada más**; sin ella queda `None`, que es el
    primer ciclo.
    """
    if W is None or getattr(W, "size", 0) == 0:
        return registro_nulo("sin_W", w_sha=w_sha)

    # **La vigente no se toca.** Todo lo de abajo corre sobre la copia.
    W_orig = W
    Wc = np.asarray(W, dtype=float).copy()

    cond = {
        "w_sha": w_sha,
        "representacion": representacion,
        "patron": "extremos + lambda",
        "grilla_lambda": list(grilla_lambda),
        "escala_desde_traza": escala_desde_traza,
        "n_runs": n_runs,
        "seed": seed,
        "escala_de_W": escala_de(Wc),
        "reloj": (clock or {}).get("reloj", "desconocido"),
        "t": (clock or {}).get("t"),
        "n_evaluaciones": len(grilla_lambda),
        "estados_provisionales": True,
    }

    if cond["escala_de_W"] == 0.0:
        cond["causa"] = "W_sin_escala"
        return {"valores": {}, "estado": NO_CALIBRADO, "condiciones": cond}

    W_col = extremo_colapso(Wc)
    A0 = count_attractors(Wc, n_runs=n_runs, seed=seed)

    curva = []
    for lam in grilla_lambda:
        W_lam = interpolar(Wc, W_col, lam)
        A = count_attractors(W_lam, n_runs=n_runs, seed=seed)
        curva.append({
            "lambda": float(lam),
            "n_eff": float(A),
            "d_ckm": d_ckm(A, A0),
            # frac_rec es A(t)/A0, lo que COCO compara contra FRAC_REC_MIN
            "frac_rec": (float(A) / float(A0)) if A0 else None,
        })
    cond["curva"] = curva

    d_sin_cambio = curva[0]["d_ckm"]
    d_colapso = curva[-1]["d_ckm"]

    if d_sin_cambio is None or d_colapso is None:
        # `d_ckm` devuelve None con N_eff0 ≤ 1: no hay distancia que medir.
        # Corrió y no separa — no es "no miré".
        cond["causa"] = "d_ckm_no_medible"
        cond["d_sin_cambio"] = d_sin_cambio
        cond["d_colapso"] = d_colapso
        return {"valores": {}, "estado": NO_CALIBRADO, "condiciones": cond}

    # **La curva no es monótona, medido.** Con una W sintética de N=12, D_ckm
    # da 0.0 → 0.749 → 0.745 → 0.606 → 0.601: el **extremo de colapso no es el
    # punto de mayor deformación**, y λ intermedios dan menos N_eff que λ=1.
    #
    # El patrón es de delamor —el colapso es λ=1 **por construcción**— así que
    # **no cambio la definición por mi cuenta**: el margen sigue siendo entre
    # los extremos. Lo que sí hago es **declarar el máximo y dónde cae**, para
    # que un margen chico por no-monotonía no se lea como poca separación.
    d_medibles = [(p["lambda"], p["d_ckm"]) for p in curva if p["d_ckm"] is not None]
    if d_medibles:
        lam_max, d_max = max(d_medibles, key=lambda x: x[1])
        cond["d_max"] = float(d_max)
        cond["lambda_de_d_max"] = float(lam_max)
        cond["curva_monotona"] = all(
            d_medibles[i][1] <= d_medibles[i + 1][1]
            for i in range(len(d_medibles) - 1)
        )
        cond["colapso_es_el_maximo"] = (lam_max == float(grilla_lambda[-1]))

    margen = d_colapso - d_sin_cambio
    cond["margen_separacion"] = float(margen)
    cond["d_sin_cambio"] = float(d_sin_cambio)
    cond["d_colapso"] = float(d_colapso)

    if margen <= 0.0:
        # El extremo de colapso no dio más D_ckm que la W sin tocar: **ningún
        # umbral separa**. No se inventa un valor.
        cond["causa"] = "sin_separacion"
        return {"valores": {}, "estado": NO_CALIBRADO, "condiciones": cond}

    umbral_d = float(d_sin_cambio + margen / 2.0)

    fr_sin_cambio = curva[0]["frac_rec"]
    fr_colapso = curva[-1]["frac_rec"]
    if fr_sin_cambio is None or fr_colapso is None or fr_colapso >= fr_sin_cambio:
        # D_ckm separó y frac_rec no. Se declara: el registro sale `calibrado`
        # con **un** valor y el otro en UNKNOWN, no con los dos inventados.
        frac_rec_min = "UNKNOWN"
        cond["frac_rec_no_separa"] = True
    else:
        frac_rec_min = float(fr_colapso + (fr_sin_cambio - fr_colapso) / 2.0)
        cond["margen_frac_rec"] = float(fr_sin_cambio - fr_colapso)

    # la vigente salió igual que entró
    assert np.array_equal(np.asarray(W_orig, dtype=float), Wc), (
        "calibrate modificó la W que recibió"
    )

    return {
        "valores": {"D_CKM_THRESHOLD": umbral_d, "FRAC_REC_MIN": frac_rec_min},
        "estado": CALIBRADO,
        "condiciones": cond,
    }
