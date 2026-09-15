"""
landscape_engine.py — rutinas de paisaje compartidas por COCO y MonitorService

Cierra la duplicación que REG_monitor_service_unificar_rutinas_v1 dejó
declarada como pendiente: la opción C copió el código de `coco.py` dentro de
`monitor_service.py` y quedaron dos implementaciones sincronizadas a mano.
Acá viven una sola vez, como funciones puras; los dos servicios delegan.

Alcance: `coco.py` y `monitor_service.py` únicamente. `fabrication_service.py`
tiene una tercera copia y queda afuera — se reescribe de cero.

Lo que NO se unifica: la W sobre la que cuenta cada instrumento.

    COCO:            W_eff = W + Δ_r
    MonitorService:  W_eff = W + (Δ_r / max(Δ_r)) · mean(W>0)

Esa divergencia es lo que distingue a los dos instrumentos —COCO ve dirección
y magnitud de Δ_r, Monitor sólo dirección— y `_combine_W_Delta` no se toca.

N sale de `W_eff.shape[0]` en cada llamada: en COCO es fijo al construir, en
Monitor se reconstruye con el corpus.

Ver docs/tasks/TASK_landscape_engine_v1.md.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

BETA_RHO_STAR = 0.5   # ρ* — identidad algebraica relax(-σ) = -relax(σ)


# ── Hopfield ────────────────────────────────────────────────────────────────

def relax_orbit(sigma: np.ndarray, W: np.ndarray, max_iter: int = 200) -> tuple:
    """
    Relajación de Hopfield síncrona, devolviendo la ÓRBITA alcanzada.

    Returns: (orbita, periodo, cola, estado_en_max_iter)
      orbita  — frozenset de los estados del conjunto invariante, SIN orden.
                Un punto fijo es la órbita de un elemento.
      periodo — |orbita|. 1 = punto fijo, 2 = órbita de dos elementos.
      cola    — pasos hasta entrar en la órbita.
      estado_en_max_iter — qué estado habría devuelto el loop de max_iter
                iteraciones. Es lo que retorna relax().

    Detección exacta, no heurística: el espacio de estados es finito
    ({-1,+1}^N) y el mapa es determinista, así que toda trayectoria entra en
    una órbita en tiempo finito (LaSalle, con V no creciente y espacio
    acotado). Se guarda cada estado visto con su paso; al repetirse uno, la
    órbita es el tramo entre las dos apariciones.

    La fase devuelta por el loop original depende de (max_iter - cola) mod
    periodo. Se reconstruye ese índice en vez de iterar hasta el final: mismo
    estado, sin recorrer el ciclo. Verificado bit a bit contra el loop previo,
    500/500 en tres corpus.
    """
    visto : dict = {}
    seq   : list = []
    s = sigma
    for t in range(max_iter):
        k    = s.tobytes()
        prev = visto.get(k)
        if prev is not None:
            per = t - prev
            idx = prev + ((max_iter - prev) % per)
            orbita = frozenset(a.tobytes() for a in seq[prev:])
            return orbita, per, prev, seq[idx]
        visto[k] = t
        seq.append(s)
        h = W @ s
        s = np.where(h > 0, 1., np.where(h < 0, -1., s))
    # max_iter agotado sin cerrar órbita — no observado en ningún corpus del
    # proyecto (0 de 800 runs), se preserva como salida defensiva.
    return frozenset([s.tobytes()]), 0, -1, s


def relax(sigma: np.ndarray, W: np.ndarray, max_iter: int = 200) -> np.ndarray:
    """Estado tras max_iter pasos de relajación síncrona — ver relax_orbit."""
    return relax_orbit(sigma, W, max_iter)[3]


# ── Muestreo de sigma_0 ─────────────────────────────────────────────────────

def node_probs(W_eff: np.ndarray, weighted: bool) -> Optional[np.ndarray]:
    """
    Distribución sobre nodos para el muestreo de sigma_0.

    weighted=False → None (uniforme). weighted=True → fi / fi.sum(), con
    fi = |W_eff|.sum(axis=1): actividad marginal de cada nodo en el paisaje
    que se evalúa.

    Fallback a uniforme (None) sin error si fi.sum()==0, o si hay menos nodos
    con peso no nulo que el n_act máximo posible (0.7·N) — rng.choice sin
    reposición no puede muestrear más nodos que los de probabilidad > 0.
    """
    if not weighted:
        return None
    N  = W_eff.shape[0]
    fi = np.abs(W_eff).sum(axis=1)
    fi_sum = fi.sum()
    if fi_sum <= 0:
        return None
    n_act_max = max(1, int(round(0.7 * N)))
    if int(np.count_nonzero(fi)) < n_act_max:
        return None
    return fi / fi_sum


def beta_c_landscape(W_eff: np.ndarray) -> Optional[float]:
    """
    β_c del paisaje que se evalúa, para el calentamiento Boltzmann:

        β_c = 1 / (ρ* · N · μ_W)     con μ_W = mean(W_eff[W_eff > 0])

    NO es el mismo número que COCO.beta_c_corpus(): ese usa μ_W sobre el
    triángulo superior incluyendo ceros y sobre self.W. Medido en
    W_ckm_corpus_v2.json: beta_c_corpus()=13.83, éste=10.46. Son dos
    temperaturas distintas — beta_c_corpus() es la referencia de TEMP_SIGNAL,
    ésta es sólo la temperatura de muestreo.

    None si W_eff no tiene pesos positivos; el llamador cae a uniforme.
    """
    pos = W_eff[W_eff > 0]
    if pos.size == 0:
        return None
    mu_W = float(np.mean(pos))
    if mu_W <= 0:
        return None
    return 1.0 / (BETA_RHO_STAR * W_eff.shape[0] * mu_W)


def boltzmann_warmup(
    rng      : np.random.Generator,
    sigma    : np.ndarray,
    W_eff    : np.ndarray,
    beta     : float,
    n_warmup : int,
) -> np.ndarray:
    """
    Calentamiento estocástico asíncrono a temperatura 1/beta:

        p(σ_i = +1) = 1 / (1 + exp(-2·β·h_i))    con h_i = Σ_j W_ij σ_j

    Misma regla que la rama estocástica de relax() en hopfield.py, que no se
    importa: usa el estado global de numpy, lo que rompería el aislamiento de
    semilla del que dependen experiments/stochastic_attractor_eval.py y
    REG_stochastic_eval_v1/v2.

    n_warmup se cuenta en actualizaciones de UN nodo, con reposición: n_warmup
    = N equivale a un barrido en promedio, no a un barrido completo. No hay
    garantía de mezcla; n_warmup óptimo es pregunta abierta.
    """
    N = W_eff.shape[0]
    sigma = sigma.copy()
    for _ in range(n_warmup):
        i = int(rng.integers(N))
        h = float(W_eff[i] @ sigma)
        p = 1.0 / (1.0 + np.exp(-2.0 * beta * h))
        sigma[i] = 1.0 if rng.random() < p else -1.0
    return sigma


def sample_s0(rng: np.random.Generator, N: int, probs: Optional[np.ndarray]) -> np.ndarray:
    """
    Un sigma_0 ∈ {+1,-1}^N con 30–70% de nodos activos.

    Compartido por count_attractors() y mean_cS() para que ambos consuman el
    RNG en la misma secuencia con la misma semilla. probs=None → uniforme.
    """
    n_act = max(1, int(round(rng.uniform(0.3, 0.7) * N)))
    s0    = np.full(N, -1.)
    s0[rng.choice(N, n_act, replace=False, p=probs)] = 1.
    return s0


def _setup(W_eff, seed, weighted, boltzmann, n_warmup):
    """rng, beta y probs del modo activo. boltzmann tiene precedencia."""
    rng   = np.random.default_rng(seed)
    beta  = beta_c_landscape(W_eff) if boltzmann else None
    probs = None if boltzmann else node_probs(W_eff, weighted)
    n_w   = n_warmup if n_warmup is not None else W_eff.shape[0]
    return rng, beta, probs, n_w


def _muestra(rng, W_eff, probs, beta, n_w) -> np.ndarray:
    s0 = sample_s0(rng, W_eff.shape[0], probs)
    if beta is not None:
        s0 = boltzmann_warmup(rng, s0, W_eff, beta, n_w)
    return s0


# ── Cantidades del paisaje ──────────────────────────────────────────────────

def count_attractors(
    W_eff    : np.ndarray,
    *,
    n_runs   : int,
    seed     : int,
    weighted : bool = False,
    boltzmann: bool = False,
    n_warmup : Optional[int] = None,
) -> int:
    """
    Atractores distintos alcanzados en n_runs reinicios sobre W_eff.

    No satura: el conteo crece ~linealmente con n_runs en corpus chicos
    (verificado hasta n_runs=200) — es una cota inferior sesgada por n_runs,
    no un valor convergente.

    Tres modos de muestreo de sigma_0, mutuamente excluyentes:
      - uniforme (default) — P(nodo) = 1/N.
      - ponderado (weighted=True) — P(nodo) ∝ |W_eff|.sum(axis=1).
      - Boltzmann (boltzmann=True) — sigma_0 uniforme + calentamiento a β_c
        del paisaje. Los otros dos son estáticos; éste usa el campo local.

    boltzmann=True tiene precedencia sobre weighted. Los dos sesgos —n_runs y
    uniformidad sobre nodos— son independientes: ningún modo corrige el
    primero.
    """
    rng, beta, probs, n_w = _setup(W_eff, seed, weighted, boltzmann, n_warmup)
    attractors = set()
    for _ in range(n_runs):
        s0 = _muestra(rng, W_eff, probs, beta, n_w)
        attractors.add(tuple(relax(s0, W_eff).tolist()))
    return len(attractors)


def mean_cS(
    W_eff    : np.ndarray,
    *,
    n_runs   : int,
    seed     : int,
    weighted : bool = False,
    boltzmann: bool = False,
    n_warmup : Optional[int] = None,
) -> float:
    """
    Media de c(S) sobre las mismas muestras que count_attractors(): mismo
    seed, mismo n_runs, misma secuencia de sigma_0. Para que ambas cantidades
    describan las mismas muestras hay que pasarles los mismos valores.

    c(S) = mean(W_eff_ij · sigma_i · sigma_j) sobre pares i<j, sobre W_eff
    (= W + Δ), no sobre W sola.
    """
    rng, beta, probs, n_w = _setup(W_eff, seed, weighted, boltzmann, n_warmup)
    ii, jj = np.triu_indices(W_eff.shape[0], k=1)
    cs_values = []
    for _ in range(n_runs):
        s0    = _muestra(rng, W_eff, probs, beta, n_w)
        sigma = relax(s0, W_eff)
        cs_values.append(float(np.mean(W_eff[ii, jj] * sigma[ii] * sigma[jj])))
    return float(np.mean(cs_values))
