"""
piso_del_colapso.py — el piso de N_eff en el extremo de colapso, por enumeración

Texto para Code 14, punto 2 (Opus 5.5, 27 oct 2026; delamor: *"si. CONFIRMO"*, y
la pregunta: *"N es variable, y sería una referencia de piso variable también? y
sería en qué condiciones? en qué se sostiene?"*).
**Mide y registra. No elige ningún umbral, margen ni percentil**, y no toca
`services/`.

## En qué se sostiene el piso (el lema, que es lo que hace exacta la cuenta)

Con `extremo_colapso` —todos los acoplamientos iguales a la escala `e > 0` y la
diagonal en 0 (`calibrate.extremo_colapso`)— el campo local de un estado σ es

    h_i = Σ_j W_ij σ_j = e · (S − σ_i),      S = Σ_j σ_j

o sea **el campo depende de σ sólo a través de S**. Con la dinámica síncrona de
`relax_orbit` y la regla de empate *"h = 0 conserva σ_i"*
(`landscape_engine.py:73-74`):

- `S ≥ 1` → para todo i, `S − σ_i ≥ 0`, y es 0 sólo si σ_i = +1 (que se
  conserva): **en un paso, todos +1**, que es punto fijo.
- `S ≤ −1` → simétrico: **en un paso, todos −1**.
- `S = 0` (sólo posible con N par) → `h_i = −e·σ_i`: **todos los signos se dan
  vuelta**, y el paso siguiente vuelve a σ. Órbita de período 2 `{σ, −σ}`.

De ahí sale que el piso **no depende de la escala** (`e` sólo multiplica, no
cambia signos) ni de los detalles de la W: depende de **N**, de la **paridad**
de N, de la **regla de empate** y de la **medida con que se sortea σ₀**. Con N
impar no hay estados de S = 0, hay exactamente dos órbitas y el piso es
**2 exacto** bajo cualquier medida simétrica. Con N par aparecen las órbitas de
período 2, y el piso es **mayor que 2** y tiende a 2 cuando N crece.

Por eso esto no se corre para saber el número: el número es un teorema. Las
enumeraciones de abajo **verifican el lema** y las masas que salen de él.

## Qué hace, en orden

1. **Verifica la dinámica y la regla de empate** contra el código: llama a
   `relax_orbit` sobre **todos** los 2^N estados para N = 10, 11, 12, 13, y
   compara la órbita devuelta con la que predice el lema. Con N = 19, 20, 21
   enumera los 2^N estados por el paso vectorizado (el mismo `np.where` de
   `relax_orbit`) y además corre `relax_orbit` real sobre una muestra
   estratificada por cantidad de nodos activos.
2. **Enumera** los 2^N estados y calcula `N_eff` exacto bajo las dos medidas:
   - la **uniforme sobre el hipercubo** `{−1,+1}^N` (la del paper v32), donde
     cada estado pesa `2^-N`;
   - la **del código** (`sample_s0`), donde la fracción de nodos activos es
     uniforme en [0,3; 0,7] y después se eligen los nodos: un estado con `a`
     activos pesa `P(a)/C(N,a)`, con
     `P(a) = |[(a−0,5)/N, (a+0,5)/N) ∩ [0,3; 0,7]| / 0,4`.
   Las dos se comparan contra la forma cerrada del lema.
3. **Verifica la medida del código** contra el muestreo real: `sample_s0` con
   muchas corridas, comparado con `P(a)`.
4. **La pregunta (d)**: qué puede dar el muestreo con `n_runs = 200` alrededor
   del valor exacto. Dos caminos independientes:
   - la distribución **exacta** de `N_eff` sobre las realizaciones
     `(n₊, n₋, n₀)` del multinomial `(P(S>0), P(S<0), P(S=0))`, con el término
     de colisiones entre órbitas de período 2 tratado aparte;
   - el muestreo **real**: `landscape_engine.count_attractors` sobre la W del
     colapso con 1000 semillas, y en qué cuantil cae la semilla 0.

Salida: `experiments/piso_del_colapso_resultado.json` (escritura atómica) y una
tabla por stdout.
"""

from __future__ import annotations

import json
import sys
from math import comb
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "services"))

from calibrate import extremo_colapso                       # noqa: E402
from landscape_engine import count_attractors, relax_orbit   # noqa: E402

ESCALA = 1.0   # la del vivo (max|W| = 1,0). El piso no depende de ella.


def W_colapso(N: int, escala: float = ESCALA) -> np.ndarray:
    """La W del extremo de colapso para N nodos, por la función del repo."""
    return extremo_colapso(np.full((N, N), escala))


# ── 1. la dinámica, contra el código ───────────────────────────────────────

def orbita_predicha(sigma: np.ndarray) -> frozenset:
    """
    La órbita que el lema predice para σ bajo el colapso.

    `S > 0` → todos +1; `S < 0` → todos −1; `S = 0` → `{σ, −σ}`.
    Devuelve el mismo tipo que `relax_orbit`: frozenset de `tobytes()`.
    """
    N = sigma.size
    S = float(sigma.sum())
    if S > 0:
        return frozenset([np.full(N, 1.0).tobytes()])
    if S < 0:
        return frozenset([np.full(N, -1.0).tobytes()])
    return frozenset([sigma.tobytes(), (-sigma).tobytes()])


def estados(N: int) -> np.ndarray:
    """Los 2^N estados de {−1,+1}^N, uno por fila. Enumeración completa."""
    bits = ((np.arange(2 ** N, dtype=np.uint32)[:, None] >>
             np.arange(N, dtype=np.uint32)) & 1).astype(np.float64)
    return bits * 2.0 - 1.0


def verificar_exhaustivo(N: int) -> dict:
    """
    `relax_orbit` real sobre **todos** los 2^N estados, contra el lema.

    Reporta también el período y la cola, que es donde se vería que el paso no
    es uno.
    """
    W = W_colapso(N)
    S = estados(N)
    malos, periodos, colas = 0, {}, {}
    for k in range(S.shape[0]):
        sig = S[k].copy()
        orb, per, cola, _ = relax_orbit(sig, W)
        if orb != orbita_predicha(S[k]):
            malos += 1
        periodos[per] = periodos.get(per, 0) + 1
        colas[cola] = colas.get(cola, 0) + 1
    return {
        "N": N, "estados": int(S.shape[0]), "discrepancias": malos,
        "periodos": {str(k): v for k, v in sorted(periodos.items())},
        "colas": {str(k): v for k, v in sorted(colas.items())},
    }


def verificar_paso_vectorizado(N: int) -> dict:
    """
    Enumeración de los 2^N estados por el paso vectorizado — el mismo
    `np.where(h > 0, 1, np.where(h < 0, -1, s))` de `relax_orbit`, aplicado a
    todos los estados a la vez y comparado con la predicción del lema.

    Es la enumeración completa de la dinámica; lo que no hace es llamar a
    `relax_orbit` 2^N veces. Que el paso vectorizado y `relax_orbit` coincidan
    queda verificado por `verificar_exhaustivo` en los N chicos y por la
    muestra estratificada acá abajo.
    """
    W = W_colapso(N)
    malos = 0
    bloque = 1 << 16
    total = 1 << N
    for ini in range(0, total, bloque):
        fin = min(ini + bloque, total)
        idx = np.arange(ini, fin, dtype=np.uint32)
        bits = ((idx[:, None] >> np.arange(N, dtype=np.uint32)) & 1).astype(np.float64)
        s = bits * 2.0 - 1.0
        h = s @ W.T
        s1 = np.where(h > 0, 1.0, np.where(h < 0, -1.0, s))
        Ssum = s.sum(axis=1)
        # lo que predice el lema para el PRIMER paso
        pred = np.where(Ssum[:, None] > 0, 1.0,
                        np.where(Ssum[:, None] < 0, -1.0, -s))
        malos += int((s1 != pred).any(axis=1).sum())
    return {"N": N, "estados": total, "discrepancias_en_el_primer_paso": malos}


def verificar_muestra_estratificada(N: int, por_a: int = 50, seed: int = 7) -> dict:
    """
    `relax_orbit` real sobre una muestra con `por_a` estados de **cada** valor
    de nodos activos `a = 0..N`, contra el lema. Cubre los dos bordes y S = 0.
    """
    W = W_colapso(N)
    rng = np.random.default_rng(seed)
    malos, n = 0, 0
    for a in range(N + 1):
        for _ in range(por_a):
            s = np.full(N, -1.0)
            if a:
                s[rng.choice(N, a, replace=False)] = 1.0
            if relax_orbit(s.copy(), W)[0] != orbita_predicha(s):
                malos += 1
            n += 1
    return {"N": N, "muestreados": n, "por_a": por_a, "discrepancias": malos}


# ── 2. las dos medidas ─────────────────────────────────────────────────────

def p_activos_codigo(N: int) -> np.ndarray:
    """
    `P(a)` bajo `sample_s0`: la fracción activa es uniforme en [0,3; 0,7] y
    `a = max(1, round(u·N))`.

    `round(u·N) = a` ⟺ `u ∈ [(a − 0,5)/N, (a + 0,5)/N)`. Se intersecta con
    [0,3; 0,7] y se divide por 0,4. El `max(1, ·)` no corrige nada para N ≥ 2:
    `a = 0` pediría `u < 0,5/N ≤ 0,25 < 0,3`.
    """
    p = np.zeros(N + 1)
    for a in range(N + 1):
        lo, hi = max((a - 0.5) / N, 0.3), min((a + 0.5) / N, 0.7)
        if hi > lo:
            p[a] = (hi - lo) / 0.4
    return p


def masas_por_enumeracion(N: int, medida: str) -> dict:
    """
    Las masas de las órbitas del colapso, enumerando los 2^N estados.

    `medida = "hipercubo"` → cada estado pesa `2^-N`.
    `medida = "codigo"`    → un estado con `a` activos pesa `P(a)/C(N,a)`.

    Agrupa por órbita según el lema: todos +1, todos −1, y una órbita por cada
    par `{σ, −σ}` con S = 0. Devuelve Σm², N_eff y la verificación de que los
    pesos suman 1.
    """
    popcount = np.bitwise_count(np.arange(2 ** N, dtype=np.uint32))
    conteo_por_a = np.bincount(popcount, minlength=N + 1)

    if medida == "hipercubo":
        peso_estado = np.full(N + 1, 2.0 ** (-N))
    else:
        pa = p_activos_codigo(N)
        peso_estado = np.array([pa[a] / comb(N, a) for a in range(N + 1)])

    # peso total por valor de a, enumerando (conteo_por_a[a] == C(N,a))
    peso_a = conteo_por_a * peso_estado
    suma = float(peso_a.sum())

    a_mitad = N / 2.0
    m_mas = float(peso_a[[a for a in range(N + 1) if a > a_mitad]].sum())
    m_menos = float(peso_a[[a for a in range(N + 1) if a < a_mitad]].sum())
    if N % 2 == 0:
        a0 = N // 2
        m_cada_orbita_0 = 2.0 * peso_estado[a0]
        n_orbitas_0 = comb(N, a0) // 2
        aporte_0 = n_orbitas_0 * m_cada_orbita_0 ** 2
        masa_0 = float(peso_a[a0])
    else:
        m_cada_orbita_0, n_orbitas_0, aporte_0, masa_0 = 0.0, 0, 0.0, 0.0

    theta = m_mas ** 2 + m_menos ** 2 + aporte_0
    return {
        "N": N, "medida": medida,
        "estados_enumerados": int(2 ** N),
        "C(N,a)_coincide_con_la_enumeracion": bool(
            all(int(conteo_por_a[a]) == comb(N, a) for a in range(N + 1))),
        "pesos_suman_1": suma,
        "masa_todos_mas": m_mas, "masa_todos_menos": m_menos,
        "masa_total_S0": masa_0,
        "n_orbitas_periodo_2": int(n_orbitas_0),
        "masa_de_cada_orbita_periodo_2": m_cada_orbita_0,
        "aporte_de_la_cola_a_sigma_m2": aporte_0,
        "simpson": theta, "n_eff_exacto": 1.0 / theta,
    }


def forma_cerrada(N: int, medida: str) -> float:
    """
    `N_eff` por la forma cerrada del lema, para contrastar con la enumeración.

    N impar → 2 exacto bajo las dos medidas (las dos son simétricas en σ ↔ −σ
    y [0,3; 0,7] es simétrico alrededor de 0,5).
    N par, hipercubo → `1 / ((1 − p0)²/2 + p0·2^(1−N))`, `p0 = C(N,N/2)/2^N`.
    N par, código    → `1 / ((1 − q0)²/2 + 2·q0²/C(N,N/2))`, `q0 = 2,5/N`.
    """
    if N % 2 == 1:
        return 2.0
    if medida == "hipercubo":
        p0 = comb(N, N // 2) / 2.0 ** N
        return 1.0 / ((1.0 - p0) ** 2 / 2.0 + p0 * 2.0 ** (1 - N))
    q0 = 2.5 / N
    return 1.0 / ((1.0 - q0) ** 2 / 2.0 + 2.0 * q0 ** 2 / comb(N, N // 2))


def verificar_sample_s0(N: int, n: int = 200000, seed: int = 11) -> dict:
    """`P(a)` contra `sample_s0` real: la medida del código, medida."""
    from landscape_engine import sample_s0
    rng = np.random.default_rng(seed)
    cuenta = np.zeros(N + 1)
    for _ in range(n):
        cuenta[int((sample_s0(rng, N, None) > 0).sum())] += 1
    emp = cuenta / n
    teo = p_activos_codigo(N)
    return {"N": N, "muestras": n,
            "max_abs_dif": float(np.abs(emp - teo).max()),
            "P_S0_teorica": float(teo[N // 2]) if N % 2 == 0 else 0.0,
            "P_S0_empirica": float(emp[N // 2]) if N % 2 == 0 else 0.0}


# ── 4. qué puede dar n_runs = 200 ──────────────────────────────────────────

def distribucion_exacta(N: int, n_runs: int, medida: str = "codigo") -> dict:
    """
    La distribución de `N_eff` estimado con `n_runs` muestras, exacta sobre
    `(n₊, n₋, n₀)` ~ multinomial.

    Con `n₀` muestras de S = 0, cada una cae en una de las
    `C(N,N/2)/2` órbitas de período 2. El Σc² de esa cola es `n₀` más dos por
    cada par de muestras que coinciden en la misma órbita; la probabilidad de
    coincidencia de un par es `1/(C(N,N/2)/2)`. Se reporta la distribución
    **sin** colisiones (que es la de casi toda la masa) y, aparte, el aporte
    esperado de las colisiones, para que se vea su tamaño.
    """
    ex = masas_por_enumeracion(N, medida)
    p_mas, p_menos = ex["masa_todos_mas"], ex["masa_todos_menos"]
    p_0 = ex["masa_total_S0"]
    n_orb0 = max(ex["n_orbitas_periodo_2"], 1)

    from math import lgamma
    log_fact = lambda k: lgamma(k + 1)          # noqa: E731
    vals, probs = [], []
    for n_mas in range(n_runs + 1):
        for n_menos in range(n_runs - n_mas + 1):
            n0 = n_runs - n_mas - n_menos
            logp = (log_fact(n_runs) - log_fact(n_mas) - log_fact(n_menos)
                    - log_fact(n0))
            for k, p in ((n_mas, p_mas), (n_menos, p_menos), (n0, p_0)):
                if k:
                    if p <= 0:
                        logp = -np.inf
                        break
                    logp += k * np.log(p)
            if logp == -np.inf:
                continue
            pr = float(np.exp(logp))
            if pr < 1e-15:
                continue
            theta = (n_mas ** 2 + n_menos ** 2 + n0) / n_runs ** 2
            vals.append(1.0 / theta)
            probs.append(pr)
    v = np.array(vals); w = np.array(probs)
    orden = np.argsort(v)
    v, w = v[orden], w[orden]
    w = w / w.sum()
    acum = np.cumsum(w)
    q = lambda x: float(v[np.searchsorted(acum, x)])    # noqa: E731
    media = float((v * w).sum())
    return {
        "N": N, "n_runs": n_runs, "medida": medida,
        "masa_cubierta": float(np.array(probs).sum()),
        "n_eff_exacto": ex["n_eff_exacto"],
        "media": media,
        "sesgo_media_menos_exacto": media - ex["n_eff_exacto"],
        "sd": float(np.sqrt(((v - media) ** 2 * w).sum())),
        "q": {"0.5%": q(0.005), "2.5%": q(0.025), "25%": q(0.25),
              "50%": q(0.5), "75%": q(0.75), "97.5%": q(0.975),
              "99.5%": q(0.995)},
        "min": float(v[0]), "max": float(v[-1]),
        "colisiones_esperadas_en_la_cola":
            float(n_runs * (n_runs - 1) / 2 * p_0 ** 2 / n_orb0),
    }


def cuantil_de(valor: float, dist: dict, N: int, n_runs: int,
               medida: str = "codigo") -> float:
    """P(N_eff estimado ≤ valor) bajo la distribución exacta. Se recalcula la
    grilla porque `distribucion_exacta` devuelve resumen, no la grilla."""
    ex = masas_por_enumeracion(N, medida)
    p_mas, p_menos, p_0 = (ex["masa_todos_mas"], ex["masa_todos_menos"],
                           ex["masa_total_S0"])
    from math import lgamma
    acum = 0.0
    for n_mas in range(n_runs + 1):
        for n_menos in range(n_runs - n_mas + 1):
            n0 = n_runs - n_mas - n_menos
            logp = (lgamma(n_runs + 1) - lgamma(n_mas + 1) - lgamma(n_menos + 1)
                    - lgamma(n0 + 1))
            ok = True
            for k, p in ((n_mas, p_mas), (n_menos, p_menos), (n0, p_0)):
                if k:
                    if p <= 0:
                        ok = False
                        break
                    logp += k * np.log(p)
            if not ok:
                continue
            theta = (n_mas ** 2 + n_menos ** 2 + n0) / n_runs ** 2
            if 1.0 / theta <= valor:
                acum += float(np.exp(logp))
    return acum


def muestreo_real(N: int, n_runs: int, n_semillas: int = 1000) -> dict:
    """
    El muestreo real del instrumento: `count_attractors` sobre la W del
    colapso, con `n_semillas` semillas. Dónde cae la semilla 0.
    """
    W = W_colapso(N)
    vals = np.array([count_attractors(W, n_runs=n_runs, seed=s)
                     for s in range(n_semillas)])
    v0 = float(count_attractors(W, n_runs=n_runs, seed=0))
    return {
        "N": N, "n_runs": n_runs, "n_semillas": int(n_semillas),
        "seed0": v0,
        "media": float(vals.mean()), "sd": float(vals.std(ddof=1)),
        "min": float(vals.min()), "max": float(vals.max()),
        "q2.5": float(np.quantile(vals, 0.025)),
        "q50": float(np.quantile(vals, 0.5)),
        "q97.5": float(np.quantile(vals, 0.975)),
        "cuantil_de_seed0": float((vals <= v0).mean()),
    }


def main() -> None:
    res: dict = {
        "que": "el piso de N_eff en el extremo de colapso, por enumeración",
        "texto": "docs/opus/TEXTO_PARA_CODE_14_REPO_CKM_simpson_y_piso_del_"
                 "colapso_27oct2026.md, punto 2",
        "escala": ESCALA,
        "nota_escala": "el piso no depende de la escala: e>0 sólo multiplica h "
                       "y no cambia signos",
    }

    print("== (a) la dinámica y la regla de empate, contra el código ==")
    res["exhaustivo"] = [verificar_exhaustivo(N) for N in (10, 11, 12, 13)]
    for d in res["exhaustivo"]:
        print(f"  N={d['N']:>2} relax_orbit sobre los {d['estados']:>6} estados: "
              f"discrepancias con el lema = {d['discrepancias']} | "
              f"periodos {d['periodos']} | colas {d['colas']}")

    res["paso_vectorizado"] = [verificar_paso_vectorizado(N) for N in (19, 20, 21)]
    for d in res["paso_vectorizado"]:
        print(f"  N={d['N']:>2} enumeración de los {d['estados']:>9} estados "
              f"(paso vectorizado): discrepancias = "
              f"{d['discrepancias_en_el_primer_paso']}")

    res["muestra_estratificada"] = [verificar_muestra_estratificada(N)
                                    for N in (19, 20, 21)]
    for d in res["muestra_estratificada"]:
        print(f"  N={d['N']:>2} relax_orbit real, {d['muestreados']} estados "
              f"({d['por_a']} por cada a): discrepancias = {d['discrepancias']}")

    print("\n== (b) y (c) N_eff exacto por enumeración, bajo las dos medidas ==")
    print(f"  {'N':>3} {'medida':>10} {'N_eff enum':>12} {'N_eff cerrada':>14} "
          f"{'suma pesos':>11} {'órbitas per2':>13} {'cola a Σm²':>12}")
    res["enumeracion"] = []
    for N in (10, 11, 12, 13, 19, 20, 21, 40):
        for medida in ("hipercubo", "codigo"):
            if N == 40 and True:
                # 2^40 no se enumera: la forma cerrada lo cubre y el lema ya
                # quedó verificado. Se reporta sólo la cerrada.
                fc = forma_cerrada(N, medida)
                res["enumeracion"].append({"N": N, "medida": medida,
                                           "n_eff_exacto": None,
                                           "n_eff_forma_cerrada": fc,
                                           "enumerado": False})
                print(f"  {N:>3} {medida:>10} {'—':>12} {fc:>14.6f} "
                      f"{'—':>11} {'—':>13} {'—':>12}")
                continue
            d = masas_por_enumeracion(N, medida)
            d["n_eff_forma_cerrada"] = forma_cerrada(N, medida)
            d["enum_igual_a_cerrada"] = bool(
                abs(d["n_eff_exacto"] - d["n_eff_forma_cerrada"]) < 1e-9)
            d["enumerado"] = True
            res["enumeracion"].append(d)
            print(f"  {N:>3} {medida:>10} {d['n_eff_exacto']:>12.6f} "
                  f"{d['n_eff_forma_cerrada']:>14.6f} {d['pesos_suman_1']:>11.9f} "
                  f"{d['n_orbitas_periodo_2']:>13} "
                  f"{d['aporte_de_la_cola_a_sigma_m2']:>12.3e}")

    print("\n== la medida del código, contra sample_s0 real ==")
    res["sample_s0"] = [verificar_sample_s0(N) for N in (20, 21)]
    for d in res["sample_s0"]:
        print(f"  N={d['N']} {d['muestras']} muestras: max|P(a) teórica − "
              f"empírica| = {d['max_abs_dif']:.5f} | P(S=0) teórica "
              f"{d['P_S0_teorica']:.5f} empírica {d['P_S0_empirica']:.5f}")

    print("\n== (d) qué puede dar el muestreo alrededor del exacto, N=20 ==")
    res["distribucion_exacta"] = [distribucion_exacta(20, n) for n in (200, 1000)]
    for d in res["distribucion_exacta"]:
        q = d["q"]
        print(f"  n_runs={d['n_runs']}: exacto {d['n_eff_exacto']:.4f} | "
              f"media {d['media']:.4f} (sesgo {d['sesgo_media_menos_exacto']:+.4f}) "
              f"| sd {d['sd']:.4f}")
        print(f"     IC95 por cuantiles [{q['2.5%']:.4f}, {q['97.5%']:.4f}] | "
              f"99% [{q['0.5%']:.4f}, {q['99.5%']:.4f}] | "
              f"rango [{d['min']:.4f}, {d['max']:.4f}] | "
              f"colisiones esperadas {d['colisiones_esperadas_en_la_cola']:.3f}")

    res["cuantil_de_lo_medido"] = {
        "2.4369_con_n_runs_200": cuantil_de(2.4369, res["distribucion_exacta"][0],
                                            20, 200),
        "2.5353_con_n_runs_1000": cuantil_de(2.5353, res["distribucion_exacta"][1],
                                             20, 1000),
    }
    print(f"  P(N_eff estimado ≤ 2,4369) con n_runs=200  = "
          f"{res['cuantil_de_lo_medido']['2.4369_con_n_runs_200']:.4f}")
    print(f"  P(N_eff estimado ≤ 2,5353) con n_runs=1000 = "
          f"{res['cuantil_de_lo_medido']['2.5353_con_n_runs_1000']:.4f}")

    print("\n== el muestreo real del instrumento, 1000 semillas ==")
    res["muestreo_real"] = [muestreo_real(20, n) for n in (200, 1000)]
    for d in res["muestreo_real"]:
        print(f"  n_runs={d['n_runs']}: seed0 {d['seed0']:.4f} | media "
              f"{d['media']:.4f} sd {d['sd']:.4f} | rango [{d['min']:.4f}, "
              f"{d['max']:.4f}] | IC95 empírico [{d['q2.5']:.4f}, {d['q97.5']:.4f}] "
              f"| cuantil de seed0 {d['cuantil_de_seed0']:.3f}")

    salida = ROOT / "experiments" / "piso_del_colapso_resultado.json"
    tmp = salida.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.rename(salida)
    print(f"\nsalida: {salida}")


if __name__ == "__main__":
    main()
