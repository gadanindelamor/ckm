"""
A.3 — las dos mediciones de hoy sobre los corpus **trackeados** del repo

Pedido de delamor/Opus. La predicción está en `2396465`, **commiteada antes**.
`node_extractor.py` no se toca.

## Qué corpus, y por qué estos tres

Del inventario (`7c72296`) y de la contención (`2396465`): de los **6** corpus
distintos del repo, los **independientes** son tres.

| | n | origen | se mide |
|---|---|---|---|
| **A** | 24 | interacción (canal IAP), capturada en experimento | **sí** |
| **D** | 12 | interacción (canal IAP) | **sí** |
| **E** | 7 | no se sabe | **sí** — y es el único donde el pool **no corta** |
| B | 20 | autor único, escrito a mano | no: **prefijo de ARM40**, ya medido |
| F | 8 | interacción | no: **prefijo de `D`** — medir `D` lo cubre |
| C | 4 | interacción | no: **subconjunto** de `D` y de `F`, **no prefijo** |

**Conteos, no porcentajes:** los corpus van de 7 a 24 textos.

## Los dos hallazgos que esto encontró

1. **`_seleccionar` puede devolver MÁS de `top_k` nodos.** Medido: **26** con
   `top_k = 20`. Pasa en la rama de la traza, cuando lo conservado no cabe en los
   libres y se suma igual.
2. **`corpus_service.py:175` dice *"con N fijo en top_k"*.** Es falso, y lo contradice
   el productor: `node_extractor.py:192` dice *"N puede diferir de top_k"*.
"""

import json
from pathlib import Path

import numpy as np
import pytest

from services.node_extractor import NodeExtractorService

TOL = NodeExtractorService.TOL_EMPATE
TOP_K = 20
RAIZ = Path(__file__).resolve().parent.parent
CORPUS = {
    "A24": RAIZ / "process/experiments/wmixta_paso2_natural/corpus_natural_uniform.json",
    "D12": RAIZ / "iap_chatroom/_state/corpus_state.json",
    "E7":  RAIZ / "process/iap/corpus_state.json",
}


def _reconstruir(ruta):
    """Reconstrucción por prefijos, encadenando cada selección como `anterior`.
    **No es la historia real**: declarado en `2396465`."""
    textos = [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]
    svc = NodeExtractorService(top_k=TOP_K, ngram_max=2)
    anterior, filas = None, []
    for n in range(3, len(textos) + 1):
        vec = svc._vectorizer(max_features=TOP_K * 3)
        M = vec.fit_transform(textos[:n])
        terms = vec.get_feature_names_out()
        sc = np.asarray(M.mean(axis=0)).flatten()
        if len(terms) <= TOP_K:
            continue
        orden = sorted(range(len(terms)), key=lambda i: (-sc[i], terms[i]))
        corte = sc[orden[TOP_K - 1]]
        arr = [i for i in orden if sc[i] - corte > TOL]
        emp = [i for i in orden if abs(sc[i] - corte) <= TOL]
        lib = TOP_K - len(arr)
        hoy = svc._seleccionar(terms, sc, anterior)[0]
        prev = set(anterior) if anterior is not None else set()
        consv = ([str(terms[i]) for i in arr]
                 + [str(terms[i]) for i in emp if str(terms[i]) in prev])
        filas.append(dict(n=n, pool=len(terms), emp=len(emp), lib=lib,
                          cabe=len(emp) <= lib,
                          fuera=sum(1 for i in emp if str(terms[i]) not in prev),
                          N_hoy=len(hoy), N_cons=len(consv),
                          cambia=set(hoy) != set(consv),
                          sin_ant=anterior is None))
        anterior = hoy
    return filas


@pytest.fixture(scope="module")
def medido():
    out = {}
    for k, r in CORPUS.items():
        if not r.exists():
            pytest.skip(f"falta {r.name}")
        out[k] = _reconstruir(r)
    return out


# ── Los regímenes, en conteos ──────────────────────────────────────────────

def test_los_regimenes_por_corpus(medido) -> None:
    """
    **Lo medido.** La predicción de `2396465` acertó en `A` y en `E`, y **falló en
    `D`** — ver el reporte.

    `(b)` el empate cabe · `(c)` no cabe con `anterior` · `(d)` no cabe sin
    `anterior` (el primer rebuild).
    """
    def reg(filas):
        return (sum(1 for r in filas if r["cabe"]),
                sum(1 for r in filas if not r["cabe"] and not r["sin_ant"]),
                sum(1 for r in filas if not r["cabe"] and r["sin_ant"]))

    assert len(medido["A24"]) == 21 and reg(medido["A24"]) == (15, 5, 1)
    assert len(medido["D12"]) == 9 and reg(medido["D12"]) == (1, 7, 1)
    assert len(medido["E7"]) == 5 and reg(medido["E7"]) == (0, 4, 1)


def test_la_meseta_sigue_al_vocabulario(medido) -> None:
    """
    **El mecanismo que la predicción puso a prueba, y se sostiene.** La meseta del
    corte aparece cuando el pool se llena de términos **indistinguibles**. `A` tiene
    vocabulario 1411 y desde `n = 10` su empate es **siempre 1**; `D` (237) y `E`
    (55) mantienen mesetas de 4 a 43.
    """
    a_desde_10 = [r["emp"] for r in medido["A24"] if r["n"] >= 10]
    assert set(a_desde_10) == {1}, "A: la meseta se cierra"
    assert max(r["emp"] for r in medido["D12"]) == 43
    assert min(r["emp"] for r in medido["E7"]) == 9


# ── La exención, en los rebuilds (b) ──────────────────────────────────────

def test_la_exencion_en_los_tres_corpus(medido) -> None:
    """
    Qué cambiaría si la traza decidiera donde el empate cabe. **Conteos.**

    Mi predicción era *"cambia en aproximadamente la mitad"*: **4 de 16**. Es la
    **tercera** predicción del día que falla **hacia arriba**.
    """
    b = {k: [r for r in v if r["cabe"]] for k, v in medido.items()}
    assert (len(b["A24"]), len(b["D12"]), len(b["E7"])) == (15, 1, 0)
    assert sum(1 for r in b["A24"] if r["cambia"]) == 4
    assert sum(r["fuera"] for r in b["A24"]) == 4
    assert sum(1 for r in b["D12"] if r["cambia"]) == 0
    # la relación exacta del reporte anterior se mantiene
    for filas in b.values():
        for r in filas:
            assert r["N_hoy"] - r["N_cons"] == r["fuera"]


# ── El hallazgo: N puede pasarse de top_k ─────────────────────────────────

def test_seleccionar_puede_devolver_MAS_de_top_k(medido) -> None:
    """
    **Hallazgo de A.3.** `_seleccionar` devuelve hasta **26** nodos con
    `top_k = 20`. Pasa en la rama de la traza: cuando lo conservado **no cabe** en
    los libres, se suma igual —`arriba + [empatados en prev]`— sin mirar la
    capacidad.

    El engine **no** hace esto: tiene la guarda `len(conserva) > free →
    trace_short`, y entonces **escala** en vez de pasarse. Es otra cara de la
    divergencia que el CP1 ya había medido.
    """
    maximos = {k: max(r["N_hoy"] for r in v) for k, v in medido.items()}
    assert maximos["E7"] == 26, maximos
    assert maximos["A24"] == 21, maximos
    assert maximos["D12"] == 20, maximos
    # y los que se pasan son siempre de la rama de la traza
    for v in medido.values():
        for r in v:
            if r["N_hoy"] > TOP_K:
                assert not r["cabe"] and not r["sin_ant"]


def test_el_docstring_del_consumidor_dice_lo_contrario() -> None:
    """
    **Cohesión código–docstring** (regla del 10 oct). `corpus_service.py:175` dice
    *"con N fijo en top_k"*; medido arriba, N llega a 26 con `top_k = 20`.

    El **productor** lo dice bien: `node_extractor.py:192`, *"N puede diferir de
    top_k"*. **No se corrige acá** —toca código vivo—: se declara.
    """
    cs = (RAIZ / "services/corpus_service.py").read_text()
    ne = (RAIZ / "services/node_extractor.py").read_text()
    assert "con N fijo en top_k" in cs, "cambió el docstring: revisar el reporte de A.3"
    assert "N puede diferir de" in ne


# ── E: la única medida de `_seleccionar` sin el pool encima ───────────────

def test_E_es_la_unica_sin_pool(medido) -> None:
    """
    `E` tiene vocabulario **55** y `max_features = 60`, así que **el pool no corta**
    en sus dos últimos rebuilds: ahí `C` es el vocabulario entero y no hay
    re-puntuación del pool (CP0 g). Es la **única** medida de `_seleccionar` limpia
    de la vía (ii).

    Y ahí la regla igual no se cumple: `empate = 9`, `libres = 8`, **no cabe**, y
    `_seleccionar` conserva — devolviendo **21**, más que `top_k`.
    """
    sin_pool = [r for r in medido["E7"] if r["pool"] < TOP_K * 3]
    assert len(sin_pool) == 5, "en E el pool nunca llena los 60"
    ultimos = [r for r in medido["E7"] if r["n"] >= 6]
    assert all(r["pool"] == 55 for r in ultimos)
    assert all(r["emp"] == 9 and r["lib"] == 8 and not r["cabe"] for r in ultimos)
    assert all(r["N_hoy"] == 21 for r in ultimos)
