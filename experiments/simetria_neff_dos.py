"""
simetria_neff_dos.py — N_eff ≥ 2 por la simetría σ ↔ −σ: la condición exacta

Texto para Code 20, punto 2 (Opus 5.5, 29 oct 2026; respalda el Pendiente R3 del
paper v33, que dice "salvo órbitas autosimétricas dominantes").
**Mide y registra. No elige ningún umbral, margen ni percentil**, y no toca
`services/` ni `iap_chatroom/`.

## La parte (a) es un teorema: se demuestra, no se corre

Regla del proyecto (CLAUDE.md): *"No se corre lo que se demuestra."* La prueba
ocupa cuatro líneas y queda acá; lo que se corre es sólo lo que la prueba **no**
decide, que es cuánta masa autoconjugada hay de hecho (puntos b y c).

**(i) El mapa es impar.** `h(−σ) = W(−σ) = −h(σ)`, y el paso de
`landscape_engine.py:73-74` es `σ'_i = +1 si h_i > 0; −1 si h_i < 0; σ_i si
h_i = 0`. Con `−h`: donde `h_i < 0` da `+1 = −σ'_i`; donde `h_i > 0` da
`−1 = −σ'_i`; y donde `h_i = 0` también `−h_i = 0`, así que conserva `−σ_i =
−σ'_i`. Entonces `f(−σ) = −f(σ)`, **para los tres casos de la regla**. En
float64 vale igual: la negación de IEEE754 es exacta y no cambia el orden de
suma, así que `h(−σ)` es exactamente `−h(σ)`, ceros incluidos. Es decir: la
divergencia entre el paso de float64 y el paso exacto que midió el punto 1
**no toca esto**.

**(ii) La medida es invariante.** `sample_s0` sortea la fracción activa uniforme
en [0,3; 0,7] y después los nodos uniformemente sin reposición, así que un
estado con `a` activos pesa `P(a)/C(N,a)`. La conjugación `σ → −σ` lleva `a` a
`N − a`, y `C(N,a) = C(N,N−a)`, de modo que la invariancia equivale a
`P(a) = P(N−a)`. `P(a)` es la longitud de `[(a−0,5)/N, (a+0,5)/N) ∩ [0,3; 0,7]`
sobre 0,4, y los dos intervalos son simétricos alrededor de 1/2 y de `N/2`
respectivamente: la intersección de `a` y la de `N − a` son reflejo una de la
otra, con la misma longitud. Se verifica acá para N = 2..21 contra la forma
cerrada y contra `sample_s0` real.

**(iii) Las órbitas vienen en pares de igual masa, con puntos fijos.** Por (i),
`O ↦ −O` manda órbitas en órbitas y es una involución; por (ii), preserva la
masa. Una involución no "aparea" todo: tiene **puntos fijos**, que son las
órbitas con `O = −O` (**autoconjugadas**). El ejemplo mínimo es `{σ, −σ}` de
período 2, que en el colapso con N par ocurre en los estados balanceados.

**(iv) La condición exacta.** Sea `α` la masa total de las órbitas
autoconjugadas y `μ` la masa de la mayor de ellas. Las no autoconjugadas vienen
en pares `(m, m)`, que aportan `2m²`:

    Σm²  =  Σ_{O=−O} m²  +  2·Σ_{pares} m_p²
         ≤  μ·α + (1−α)²/2   ≤   α² + (1−α)²/2

(la primera cota es `Σ m² ≤ μ Σ m` sobre las autoconjugadas; la segunda, que la
suma de cuadrados de los pares se maximiza concentrando toda la masa `1−α` en
un solo par, con `m_p = (1−α)/2`). Entonces, **siempre**:

    N_eff  ≥  1 / (α² + (1−α)²/2)

y la cota es **alcanzada** (una autoconjugada con masa `α` y un par con
`(1−α)/2` cada uno), así que es exacta, no conservadora. De ahí:

- **α = 0  ⟹  N_eff ≥ 2**, con igualdad sólo si toda la masa está en un único
  par `{O, −O}` con 1/2 cada uno. Ésta es la forma correcta del enunciado del
  paper.
- Resolviendo `α² + (1−α)²/2 ≤ 1/2`: **α ≤ 2/3 ⟹ N_eff ≥ 2**, con igualdad en
  `α = 2/3`. El enunciado "N_eff ≥ 2 salvo órbitas autosimétricas dominantes"
  es correcto, y "dominante" tiene un valor exacto: **2/3**.
- Con `α > 2/3` la cota baja de 2, y en el extremo `α = 1` concentrado en una
  sola órbita autoconjugada da `N_eff = 1`.
- La `F(N)` del colapso con N par es **un caso particular** de esta cota, con
  igualdad: ahí `α = q0 = 2,5/N` se reparte en partes iguales entre las
  `C(N,N/2)/2` órbitas balanceadas, de modo que `Σ_{O=−O} m² =
  2q0²/C(N,N/2)` y los dos puntos fijos ±1 forman el par con `(1−q0)/2`:
  `F(N) = 1/((1−q0)²/2 + 2q0²/C(N,N/2))`, que es exactamente
  `piso_del_colapso.forma_cerrada(N, "codigo")`.

Lo que **no** dice el teorema, y por eso se mide: si `α > 2/3` ocurre de hecho
en alguna W, y si el **estimador** a 200/0/uniforme puede dar menos de 2 aunque
el exacto no. Eso es (b) y (c).

## Qué corre, entonces

- **(a) verificación de los eslabones**, no del teorema: que `f(−σ) = −f(σ)` en
  el código (exhaustivo sobre los 2^N estados para N ≤ 12, y sobre las 14 W de
  N = 20 con una muestra estratificada); que `P(a) = P(N−a)` para N = 2..21 por
  forma cerrada y contra `sample_s0` real; y que la cota de (iv) se alcanza en
  el colapso.
- **(b) contraejemplos**: todas las W simétricas de diagonal cero con entradas
  en {−1,0,+1} para N = 2..5 (3^(N(N−1)/2) W: 3, 27, 729 y 59049), con N_eff
  **exacto** por enumeración; y para N = 6..8, una muestra de 10.000 W por N con
  `seed = 0` **declarada** (es la seed de la muestra de W, no la del
  instrumento). Por N y paridad: el N_eff mínimo, la W que lo da, cuántas W dan
  N_eff < 2, y su masa autoconjugada `α`. En estas W las entradas son enteras,
  así que el `h` de float64 es exacto y el paso del código coincide con el paso
  exacto: no hay la divergencia del punto 1 (se verifica).
- **(c) sobre las 14 W del punto 1**: órbitas autoconjugadas, su masa exacta, y
  si el estimador a 200/0/uniforme da menos de 2. Se leen del resultado del
  punto 1 (`margen_exacto_14W_resultado.json`), no se recalculan.
- **(d) la línea del REG de fourforums v8n** que cita el paper.
- **(e) la paridad de n_runs contra la de N**, sobre el colapso: la distribución
  del plug-in de F para N = 4..21 con n_runs = 199, 200 y 201. **Exacta** por la
  binomial con N impar, donde `p0 = 0` y hay sólo dos órbitas. Con **N par** hay
  cola: las `n₀` muestras balanceadas se reparten entre `K = C(N,N/2)/2`
  órbitas, y **contarlas como K distintas es falso para N chico** (medido: con
  N = 4, donde K = 3, da media 13,75 contra `F(4) = 4,99`). Así que con N par va
  la **simulación con 1000 seeds declaradas (0..999)**, que reparte la cola. Dos
  controles: con N impar la simulación tiene que dar lo mismo que la exacta, y
  con N = 20 y 21 se compara contra el muestreo **real** del instrumento
  (`count_attractors` sobre `calibrate.extremo_colapso`, 100 seeds declaradas).
  El 200 es el default del instrumento; **199 y 201 los declara este driver**,
  con su razón: son el 200 ± 1 para ver la paridad de n_runs contra la de N.

## Condiciones

- `n_runs = 200`, `seed = 0`, distribución **uniforme**, leídos de
  `calibrate.N_RUNS_DEFAULT` / `SEED_DEFAULT`, para todo lo muestreado con el
  instrumento. Los otros valores (199, 201, las seeds 0..99 del control, la seed
  0 de la muestra de W) son declaraciones de este driver, cada una con su razón.
- En toda tabla, `N` y su paridad. Sólo se mide: no se nombra qué significa.

Salida: `experiments/simetria_neff_dos_resultado.json` (escritura atómica) y un
resumen por stdout.
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from math import log
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "services"))
sys.path.insert(0, str(ROOT / "experiments"))

from calibrate import N_RUNS_DEFAULT, SEED_DEFAULT            # noqa: E402
from landscape_engine import (count_attractors, relax, relax_orbit,  # noqa: E402
                              sample_s0)

import margen_exacto_14W as ME                                  # noqa: E402
import piso_del_colapso as PC                                   # noqa: E402

SALIDA = Path(__file__).resolve().parent / "simetria_neff_dos_resultado.json"


# ── (a) los eslabones ───────────────────────────────────────────────────────

def antisimetria_exhaustiva(W: np.ndarray) -> dict:
    """
    `f(−σ) = −f(σ)` sobre **todos** los 2^N estados, con el paso del código.

    Se compara el sucesor del estado conjugado contra el conjugado del sucesor,
    usando la misma tabla `nxt` que la enumeración: el conjugado de un índice es
    el XOR con la máscara de N unos.
    """
    N = W.shape[0]
    nxt, info = ME.siguiente(W, "codigo")
    mask = np.uint32((1 << N) - 1)
    idx = np.arange(1 << N, dtype=np.uint32)
    izq = nxt[idx ^ mask]            # f(−σ)
    der = nxt[idx] ^ mask            # −f(σ)
    malos = np.nonzero(izq != der)[0]
    return {"N": N, "estados": 1 << N, "discrepancias": int(malos.size),
            "cumple": bool(malos.size == 0),
            "empates_exactos_estado_nodo": info["empates_exactos_estado_nodo"]}


def antisimetria_muestreada(W: np.ndarray, por_a: int = 25,
                            seed: int = 7) -> dict:
    """
    `relax_orbit(−σ)` contra `−relax_orbit(σ)` con el código real, sobre una
    muestra estratificada por cantidad de nodos activos.

    Compara la órbita entera (como conjunto de estados) y el período, y además
    `relax(−σ) = −relax(σ)` — que es la línea del REG de fourforums v8n, y que
    exige que la **fase** devuelta por el loop de `max_iter` también se
    corresponda, no sólo la órbita.
    """
    N = W.shape[0]
    rng = np.random.default_rng(seed)
    malos_orbita, malos_relax, revisados = 0, 0, 0
    for a in range(1, N + 1):
        for _ in range(por_a):
            s = np.full(N, -1.0)
            s[rng.choice(N, a, replace=False)] = 1.0
            o1, p1, _, _ = relax_orbit(s, W)
            o2, p2, _, _ = relax_orbit(-s, W)
            conj = frozenset((-np.frombuffer(b, dtype=np.float64)).tobytes()
                             for b in o1)
            revisados += 1
            if conj != o2 or p1 != p2:
                malos_orbita += 1
            if not np.array_equal(relax(-s, W), -relax(s, W)):
                malos_relax += 1
    return {"N": N, "revisados": revisados,
            "orbita_conjugada_distinta": malos_orbita,
            "relax_menos_sigma_distinto": malos_relax,
            "cumple": bool(malos_orbita == 0 and malos_relax == 0)}


def medida_invariante(N_max: int = 21, n_muestras: int = 200000,
                      seed: int = 11) -> dict:
    """
    `P(n_act = k) = P(n_act = N − k)` para N = 2..N_max.

    Por la forma cerrada de `piso_del_colapso.p_activos_codigo` (que es la
    medida del código escrita), y contra `sample_s0` **real** para los N que el
    punto 2 usa de hecho: el redondeo de numpy y el `max(1, ·)` se ven ahí, no
    en la fórmula. Se reporta la diferencia máxima, no un veredicto.
    """
    filas = []
    for N in range(2, N_max + 1):
        pa = PC.p_activos_codigo(N)
        dif = float(np.abs(pa - pa[::-1]).max())
        filas.append({"N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
                      "max_dif_P_a_vs_P_N_menos_a": dif,
                      "suma_P": float(pa.sum())})
    # contra sample_s0 real, en los N que se usan
    empirico = []
    for N in (5, 8, 20, 21):
        rng = np.random.default_rng(seed)
        cuenta = np.zeros(N + 1)
        for _ in range(n_muestras):
            cuenta[int((sample_s0(rng, N, None) > 0).sum())] += 1
        emp = cuenta / n_muestras
        teo = PC.p_activos_codigo(N)
        empirico.append({
            "N": N, "muestras": n_muestras, "seed_de_la_muestra": seed,
            "max_dif_contra_la_forma_cerrada": float(np.abs(emp - teo).max()),
            "max_dif_simetria_empirica": float(np.abs(emp - emp[::-1]).max()),
        })
    return {"forma_cerrada": filas, "contra_sample_s0": empirico}


def cota_de_la_involucion(alpha: float) -> float:
    """
    La cota exacta de (iv): `N_eff ≥ 1/(α² + (1−α)²/2)`, con α la masa total de
    las órbitas autoconjugadas. Alcanzada por una autoconjugada de masa α más un
    par de (1−α)/2.
    """
    return 1.0 / (alpha ** 2 + (1.0 - alpha) ** 2 / 2.0)


def cota_contra_el_colapso(Ns: tuple = (4, 6, 8, 10, 12, 14, 16, 18, 20)) -> list:
    """
    La cota de (iv) contra `F(N)` del colapso, que la alcanza con `α = 2,5/N`
    repartida en partes iguales: ahí la cota con α **sola** es más laxa que
    `F(N)`, y la cota con la masa de la **mayor** autoconjugada (`μ`) la
    reproduce exacta. Las dos se reportan.
    """
    out = []
    for N in Ns:
        enum = PC.masas_por_enumeracion(N, "codigo")
        alpha = enum["masa_total_S0"]
        mu = enum["masa_de_cada_orbita_periodo_2"]
        F = PC.forma_cerrada(N, "codigo")
        exacta = 1.0 / (mu * alpha + (1.0 - alpha) ** 2 / 2.0)
        out.append({
            "N": N, "paridad_N": "par",
            "alpha_masa_autoconjugada": alpha,
            "mu_mayor_autoconjugada": mu,
            "F(N)": F,
            "cota_solo_con_alpha": cota_de_la_involucion(alpha),
            "cota_con_mu": exacta,
            "cota_con_mu_menos_F": exacta - F,
            "alpha_menor_o_igual_2_tercios": bool(alpha <= 2.0 / 3.0),
        })
    return out


# ── (b) contraejemplos ──────────────────────────────────────────────────────

def _n_eff_exacto_entero(W: np.ndarray) -> dict:
    """
    N_eff exacto de una W **entera** chica, por enumeración de los 2^N estados
    bajo la medida del código, con la masa autoconjugada.

    Con entradas enteras el `h` de float64 es exacto (los enteros chicos y sus
    sumas son exactos en IEEE754), así que el paso del código **es** el paso
    exacto: no hay la divergencia del punto 1. Se verifica en
    `_control_entero`.
    """
    N = W.shape[0]
    nxt, _ = ME.siguiente(W, "exacto")
    orb, per, per_max = ME.orbitas(nxt)
    w = ME.pesos_medida_codigo(N)
    masa = np.bincount(orb.astype(np.int64), weights=w, minlength=1 << N)
    vivos = np.nonzero(masa)[0]
    m = masa[vivos] / masa[vivos].sum()
    comp = np.arange(1 << N, dtype=np.uint32) ^ np.uint32((1 << N) - 1)
    auto = orb[comp[vivos]] == vivos
    theta = float(np.square(m).sum())
    return {"n_eff": 1.0 / theta, "n_orbitas": int(vivos.size),
            "periodo_max": per_max,
            "alpha": float(m[auto].sum()),
            "mu": float(m[auto].max()) if auto.any() else 0.0,
            "n_autoconjugadas": int(auto.sum())}


def _control_entero(W: np.ndarray) -> bool:
    """Con W entera, el paso de float64 y el exacto dan el mismo `nxt`."""
    a, _ = ME.siguiente(W, "codigo")
    b, _ = ME.siguiente(W, "exacto")
    return bool(np.array_equal(a, b))


def _arma_W(N: int, valores) -> np.ndarray:
    W = np.zeros((N, N))
    k = 0
    for i in range(N):
        for j in range(i + 1, N):
            W[i, j] = W[j, i] = valores[k]
            k += 1
    return W


def W_al_azar(N: int, seed: int) -> np.ndarray:
    """
    Una W simétrica de diagonal cero con entradas en {−1,0,+1}, con `seed`
    **declarada**: es la seed de la W, no la del instrumento. Se usa para los
    controles exhaustivos de (a) y del paso entero de (b).
    """
    rng = np.random.default_rng(seed)
    return _arma_W(N, rng.choice([-1.0, 0.0, 1.0], N * (N - 1) // 2))


def busqueda_contraejemplos(N: int, muestra: int | None = None,
                            seed: int = 0) -> dict:
    """
    N_eff exacto sobre las W simétricas de diagonal cero con entradas en
    {−1,0,+1}.

    `muestra = None` → **todas** (3^(N(N−1)/2)). Si no, `muestra` W al azar con
    `seed` declarada: es la seed de la muestra de W, no la del instrumento.

    Devuelve el mínimo de N_eff y la W que lo da, cuántas W dan N_eff < 2 (con
    su α), y cuántas tienen α > 2/3 — que es la condición exacta de (iv).
    """
    pares = N * (N - 1) // 2
    total = 3 ** pares
    if muestra is None:
        gen = itertools.product((-1.0, 0.0, 1.0), repeat=pares)
        n_rev = total
    else:
        rng = np.random.default_rng(seed)
        gen = (tuple(v) for v in rng.choice([-1.0, 0.0, 1.0],
                                           size=(muestra, pares)))
        n_rev = muestra

    peor = None
    ejemplos_menores, ejemplos_alpha = [], []
    n_menores, n_alpha_grande, con_alpha_pos = 0, 0, 0
    for valores in gen:
        W = _arma_W(N, valores)
        r = _n_eff_exacto_entero(W)
        if r["alpha"] > 0:
            con_alpha_pos += 1
        if peor is None or r["n_eff"] < peor[0]["n_eff"]:
            peor = (r, valores)
        if r["n_eff"] < 2.0 - 1e-12:
            n_menores += 1
            if len(ejemplos_menores) < 20:    # tope de ejemplos, no de conteo
                ejemplos_menores.append({"W_triangulo": list(valores), **r})
        if r["alpha"] > 2.0 / 3.0:
            n_alpha_grande += 1
            if len(ejemplos_alpha) < 20:
                ejemplos_alpha.append({"W_triangulo": list(valores), **r})
    return {
        "N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
        "W_posibles": total,
        "W_revisadas": n_rev,
        "exhaustiva": muestra is None,
        "seed_de_la_muestra_de_W": None if muestra is None else seed,
        "n_eff_minimo": peor[0]["n_eff"],
        "W_del_minimo_triangulo_superior": list(peor[1]),
        "detalle_del_minimo": peor[0],
        "cuantas_con_n_eff_menor_que_2": n_menores,
        "ejemplos_con_n_eff_menor_que_2": ejemplos_menores,
        "cuantas_con_alpha_positiva": con_alpha_pos,
        "cuantas_con_alpha_mayor_que_dos_tercios": n_alpha_grande,
        "ejemplos_con_alpha_mayor_que_dos_tercios": ejemplos_alpha,
    }


# ── (c) las 14 W ────────────────────────────────────────────────────────────

def las_14_W() -> dict:
    """
    Lo que el punto 1 ya midió sobre las 14 W, leído de su resultado: órbitas
    autoconjugadas, su masa exacta α, la cota de (iv), el N_eff exacto y el
    estimador a 200/0/uniforme. No se recalcula nada.
    """
    p = Path(__file__).resolve().parent / "margen_exacto_14W_resultado.json"
    if not p.exists():
        return {"falta": str(p)}
    d = json.load(open(p, encoding="utf-8"))
    filas = []
    for w in d["W"]:
        if "enumeracion_con_el_paso_del_codigo" not in w:
            continue
        e = w["enumeracion_con_el_paso_del_codigo"]
        alpha = e["masa_autoconjugada"]
        filas.append({
            "w_sha": w["w_sha"][:8], "intento": w["intento"],
            "N": e["N"], "paridad_N": e["paridad_N"],
            "n_orbitas_autoconjugadas": e["n_orbitas_autoconjugadas"],
            "alpha": alpha,
            "alpha_menor_o_igual_2_tercios": bool(alpha <= 2.0 / 3.0),
            "cota_de_la_involucion": cota_de_la_involucion(alpha),
            "n_eff_exacto": e["n_eff_exacto"],
            "n_eff_exacto_mayor_o_igual_2": bool(e["n_eff_exacto"] >= 2.0),
            "n_eff_muestreado_200_0": w["n_eff0_muestreado_200_0_uniforme"],
            "el_estimador_da_menos_de_2": bool(
                w["n_eff0_muestreado_200_0_uniforme"] < 2.0),
            "ic95_del_141": (w.get("ic_del_141") or {}).get("n_eff_ic95"),
        })
    return {"filas": filas,
            "cuantas_con_estimador_menor_que_2":
                sum(f["el_estimador_da_menos_de_2"] for f in filas),
            "cuantas_con_exacto_menor_que_2":
                sum(not f["n_eff_exacto_mayor_o_igual_2"] for f in filas)}


# ── (e) la paridad de n_runs contra la de N ─────────────────────────────────

def dist_plugin_colapso(N: int, n_runs: int) -> dict:
    """
    La distribución del plug-in de F sobre el colapso con `n_runs` muestras,
    **para N impar**, exacta.

    Con N impar el lema da `P(S=0) = 0`: hay exactamente dos órbitas, los dos
    puntos fijos ±1, de masa 1/2 cada una. La distribución del plug-in es
    entonces binomial y se suma sin error sobre las realizaciones `(n₊, n₋)`.

    **Para N par esta función no sirve y no se usa**: la cola de `n₀` muestras
    se reparte entre `C(N,N/2)/2` órbitas, y acá cada muestra de la cola se
    contaría como una órbita distinta. Medido: con N = 4, donde hay **3**
    órbitas balanceadas, eso daba media 13,75 contra `F(4) = 4,99`. Para N par
    va `dist_plugin_simulada`, que reparte la cola.

    Reporta media, percentiles 5/50/95, `P(plug-in ≥ F)`, `P(plug-in > F)` y
    `P(plug-in = 2)`, que con N impar es el máximo alcanzable.
    """
    ex = PC.masas_por_enumeracion(N, "codigo")
    p_mas, p_menos = ex["masa_todos_mas"], ex["masa_todos_menos"]
    p_0 = ex["masa_total_S0"]
    K = max(ex["n_orbitas_periodo_2"], 1)
    F = PC.forma_cerrada(N, "codigo")

    from math import lgamma
    vals, probs = [], []
    for n_mas in range(n_runs + 1):
        for n_menos in range(n_runs - n_mas + 1):
            n0 = n_runs - n_mas - n_menos
            if n0 and p_0 <= 0:
                continue
            logp = (lgamma(n_runs + 1) - lgamma(n_mas + 1)
                    - lgamma(n_menos + 1) - lgamma(n0 + 1))
            ok = True
            for k, p in ((n_mas, p_mas), (n_menos, p_menos), (n0, p_0)):
                if k:
                    if p <= 0:
                        ok = False
                        break
                    logp += k * log(p)
            if not ok:
                continue
            pr = float(np.exp(logp))
            if pr < 1e-18:
                continue
            theta = (n_mas ** 2 + n_menos ** 2 + n0) / n_runs ** 2
            vals.append(1.0 / theta)
            probs.append(pr)
    v = np.array(vals)
    w = np.array(probs)
    orden = np.argsort(v)
    v, w = v[orden], w[orden]
    masa_cubierta = float(w.sum())
    w = w / w.sum()
    acum = np.cumsum(w)

    def q(x):
        return float(v[np.searchsorted(acum, x)])

    media = float((v * w).sum())
    return {
        "N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
        "n_runs": n_runs,
        "paridad_n_runs": "par" if n_runs % 2 == 0 else "impar",
        "exacta": (N % 2 == 1),
        "masa_cubierta": masa_cubierta,
        "F(N)": F,
        "n_eff_exacto": ex["n_eff_exacto"],
        "media": media,
        "sesgo_media_menos_F": media - F,
        "p5": q(0.05), "p50": q(0.5), "p95": q(0.95),
        "min": float(v[0]), "max": float(v[-1]),
        "P_mayor_o_igual_F": float(w[v >= F - 1e-12].sum()),
        "P_mayor_que_F": float(w[v > F + 1e-12].sum()),
        "P_igual_a_2": float(w[np.abs(v - 2.0) < 1e-12].sum()),
        "colisiones_esperadas_en_la_cola":
            float(n_runs * (n_runs - 1) / 2 * p_0 ** 2 / K),
    }


def dist_plugin_simulada(N: int, n_runs: int, n_seeds: int = 1000) -> dict:
    """
    La distribución del plug-in de F sobre el colapso, **con la cola
    repartida**, por simulación con `n_seeds` seeds declaradas (0..n_seeds−1).

    No corre `relax_orbit`: usa la estructura de órbitas que da el lema y que
    `piso_del_colapso` ya verificó contra el código (los dos puntos fijos ±1 de
    masa `(1−q0)/2` y las `K = C(N,N/2)/2` órbitas balanceadas de masa `q0/K`).
    Por seed: `(n₊, n₋, n₀)` del multinomial, y las `n₀` muestras de la cola
    repartidas uniformemente entre las K órbitas —uniformemente porque las K
    tienen **la misma** masa—, contando las coincidencias. El plug-in es
    `n_runs² / (n₊² + n₋² + Σ_cola c²)`.

    Las seeds 0..n_seeds−1 son una declaración de este driver, con su razón: el
    default del instrumento es una sola seed (0) y acá hace falta una
    distribución. Se controla contra la forma exacta con N impar y contra el
    muestreo real del instrumento con N = 20 y 21.
    """
    ex = PC.masas_por_enumeracion(N, "codigo")
    p = [ex["masa_todos_mas"], ex["masa_todos_menos"], ex["masa_total_S0"]]
    K = max(ex["n_orbitas_periodo_2"], 1)
    F = PC.forma_cerrada(N, "codigo")
    vals = np.empty(n_seeds)
    for s in range(n_seeds):
        rng = np.random.default_rng(s)
        n_mas, n_menos, n0 = rng.multinomial(n_runs, p)
        sc = 0
        if n0:
            cuales = rng.integers(0, K, size=n0)
            _, c = np.unique(cuales, return_counts=True)
            sc = int((c.astype(np.int64) ** 2).sum())
        vals[s] = n_runs ** 2 / (n_mas ** 2 + n_menos ** 2 + sc)
    return {
        "N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
        "n_runs": n_runs,
        "paridad_n_runs": "par" if n_runs % 2 == 0 else "impar",
        "exacta": False, "seeds": f"0..{n_seeds - 1}",
        "K_orbitas_balanceadas": K,
        "F(N)": F, "n_eff_exacto": ex["n_eff_exacto"],
        "media": float(vals.mean()),
        "sesgo_media_menos_F": float(vals.mean() - F),
        "sd": float(vals.std(ddof=1)),
        "p5": float(np.percentile(vals, 5)),
        "p50": float(np.percentile(vals, 50)),
        "p95": float(np.percentile(vals, 95)),
        "min": float(vals.min()), "max": float(vals.max()),
        "P_mayor_o_igual_F": float((vals >= F - 1e-12).mean()),
        "P_mayor_que_F": float((vals > F + 1e-12).mean()),
        "P_igual_a_2": float((np.abs(vals - 2.0) < 1e-12).mean()),
    }


def control_muestreo_real(N: int, n_runs: int, n_seeds: int = 100) -> dict:
    """
    El control: `count_attractors` sobre `calibrate.extremo_colapso`, con
    `n_seeds` seeds declaradas (0..n_seeds−1), contra la distribución exacta.

    Las seeds 0..99 son una declaración de este driver, con su razón: el default
    del instrumento es una sola seed (0), y acá hace falta una distribución.
    """
    W = PC.W_colapso(N)          # extremo_colapso del repo, escala 1,0
    vals = [count_attractors(W, n_runs=n_runs, seed=s) for s in range(n_seeds)]
    v = np.array(vals, dtype=float)
    F = PC.forma_cerrada(N, "codigo")
    return {"N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
            "n_runs": n_runs, "seeds": f"0..{n_seeds - 1}",
            "media": float(v.mean()), "sd": float(v.std(ddof=1)),
            "p5": float(np.percentile(v, 5)),
            "p50": float(np.percentile(v, 50)),
            "p95": float(np.percentile(v, 95)),
            "F(N)": F,
            "frac_mayor_o_igual_F": float((v >= F - 1e-12).mean()),
            "frac_igual_a_2": float((np.abs(v - 2.0) < 1e-12).mean())}


def main() -> None:
    salida = {
        "que": "N_eff >= 2 por la simetria sigma <-> -sigma (texto 20, punto 2)",
        "la_parte_a_es_un_teorema": (
            "demostrada en el docstring: f(-s) = -f(s) para los tres casos de "
            "la regla de empate; la medida es invariante porque P(a) = P(N-a); "
            "la conjugacion de orbitas es una involucion que preserva masa, y "
            "sus puntos fijos son las orbitas autoconjugadas. Condicion "
            "exacta: N_eff >= 1/(alpha^2 + (1-alpha)^2/2), alcanzada; de ahi "
            "alpha = 0 => N_eff >= 2, y alpha <= 2/3 => N_eff >= 2."
        ),
        "defaults_del_instrumento": {"n_runs": N_RUNS_DEFAULT,
                                     "seed": SEED_DEFAULT,
                                     "sampling_mode": "uniform"},
        "declaraciones_de_este_driver": {
            "n_runs_199_y_201": "el 200 ± 1, para ver la paridad de n_runs "
                                "contra la de N (punto 2e)",
            "seeds_0_99": "el control del muestreo real necesita una "
                          "distribucion; el default es una sola seed",
            "seed_0_de_la_muestra_de_W": "la seed de la muestra de W del punto "
                                         "2b, no la del instrumento",
        },
    }

    # (a)
    print("(a) los eslabones del teorema")
    ex_anti = [{"seed_de_la_W": 3, **antisimetria_exhaustiva(W_al_azar(N, 3))}
               for N in (4, 8, 12)]
    med = medida_invariante()
    cotas = cota_contra_el_colapso()
    salida["a_antisimetria_exhaustiva_W_al_azar"] = ex_anti
    salida["a_medida_invariante"] = med
    salida["a_cota_contra_el_colapso"] = cotas
    print("    f(-s)=-f(s) exhaustivo (N=4,8,12):",
          [r["cumple"] for r in ex_anti])
    print("    max dif P(a) vs P(N-a), N=2..21:",
          max(r["max_dif_P_a_vs_P_N_menos_a"] for r in med["forma_cerrada"]))
    print("    cota con mu menos F(N):",
          max(abs(c["cota_con_mu_menos_F"]) for c in cotas))

    # (a) sobre las 14 W de N=20, con el código real
    filas14 = ME.w_de_las_curvas()
    anti14 = []
    for f in filas14:
        if f["W"] is None:
            continue
        anti14.append({"w_sha": f["w_sha"][:8],
                       **antisimetria_muestreada(f["W"])})
    salida["a_antisimetria_en_las_14_W"] = anti14
    print("    relax_orbit(-s) == -relax_orbit(s) en las 14 W:",
          all(r["cumple"] for r in anti14),
          f"({sum(r['revisados'] for r in anti14)} estados)")

    # (b)
    print("(b) contraejemplos")
    b = []
    for N in (2, 3, 4, 5):
        r = busqueda_contraejemplos(N)
        b.append(r)
        print(f"    N={N} {r['paridad_N']:>5} exhaustiva {r['W_revisadas']:>6} W"
              f" · min N_eff = {r['n_eff_minimo']:.6f}"
              f" · con N_eff<2: {r['cuantas_con_n_eff_menor_que_2']}"
              f" · con alpha>2/3: {r['cuantas_con_alpha_mayor_que_dos_tercios']}")
    for N in (6, 7, 8):
        r = busqueda_contraejemplos(N, muestra=10000, seed=0)
        b.append(r)
        print(f"    N={N} {r['paridad_N']:>5} muestra    {r['W_revisadas']:>6} W"
              f" · min N_eff = {r['n_eff_minimo']:.6f}"
              f" · con N_eff<2: {r['cuantas_con_n_eff_menor_que_2']}"
              f" · con alpha>2/3: {r['cuantas_con_alpha_mayor_que_dos_tercios']}")
    salida["b_busqueda"] = b
    salida["b_control_paso_entero"] = {
        "seed_de_las_W": 5,
        "W_entera_el_paso_de_float64_es_el_exacto":
            all(_control_entero(W_al_azar(N, 5)) for N in (4, 6, 8))}

    # (c)
    print("(c) las 14 W")
    c = las_14_W()
    salida["c_las_14_W"] = c
    print(f"    exacto < 2: {c['cuantas_con_exacto_menor_que_2']} de "
          f"{len(c['filas'])} · estimador 200/0 < 2: "
          f"{c['cuantas_con_estimador_menor_que_2']} de {len(c['filas'])}")

    # (d)
    salida["d_la_linea_del_REG"] = {
        "linea_citada": "relax(-s) = -relax(s): las orbitas vienen en pares +-",
        "vale_la_primera_mitad": all(r["relax_menos_sigma_distinto"] == 0
                                     for r in anti14),
        "estados_revisados": sum(r["revisados"] for r in anti14),
        "la_condicion": (
            "la igualdad relax(-s) = -relax(s) vale tal como esta escrita, y "
            "no necesita condicion: la fase que devuelve el loop de max_iter "
            "es la misma para s y para -s porque la cola y el periodo "
            "coinciden. Lo que necesita condicion es la segunda mitad: la "
            "conjugacion es una INVOLUCION, no un apareamiento libre, asi que "
            "las orbitas vienen en pares {O, -O} salvo las que cumplen O = -O "
            "(autoconjugadas), que son puntos fijos y no tienen pareja. Esas "
            "existen y tienen masa medida en las 14 W del punto 1."
        ),
    }

    # (e)
    print("(e) la paridad de n_runs contra la de N")
    e, e_sim = [], []
    for N in range(4, 22):
        for nr in (199, N_RUNS_DEFAULT, 201):
            if N % 2 == 1:
                e.append(dist_plugin_colapso(N, nr))     # exacta, binomial
            e_sim.append(dist_plugin_simulada(N, nr))     # con la cola repartida
    salida["e_distribucion_exacta_N_impar"] = e
    salida["e_distribucion_simulada_1000_seeds"] = e_sim
    # control: con N impar las dos tienen que coincidir
    salida["e_control_exacta_vs_simulada_N_impar"] = [
        {"N": a["N"], "n_runs": a["n_runs"],
         "dif_media": a["media"] - b["media"],
         "dif_P_mayor_o_igual_F": a["P_mayor_o_igual_F"] - b["P_mayor_o_igual_F"]}
        for a in e for b in e_sim
        if a["N"] == b["N"] and a["n_runs"] == b["n_runs"]]
    e = e_sim
    enc = ("     N  par    n_runs  par   F(N)      media      p5      p50  "
           "    p95   P(>=F)   P(=2)")
    print(enc)
    for r in e:
        if r["N"] in (4, 5, 20, 21):
            print(f"    {r['N']:>2} {r['paridad_N']:>5} {r['n_runs']:>8} "
                  f"{r['paridad_n_runs']:>5} {r['F(N)']:.4f} "
                  f"{r['media']:>9.4f} {r['p5']:>8.4f} {r['p50']:>8.4f} "
                  f"{r['p95']:>8.4f} {r['P_mayor_o_igual_F']:>8.4f} "
                  f"{r['P_igual_a_2']:>8.4f}")
    ctrl = [control_muestreo_real(N, nr)
            for N in (20, 21) for nr in (199, N_RUNS_DEFAULT, 201)]
    salida["e_control_muestreo_real"] = ctrl
    for r in ctrl:
        print(f"    control real N={r['N']} n_runs={r['n_runs']}: "
              f"media {r['media']:.4f} p50 {r['p50']:.4f} "
              f"frac>=F {r['frac_mayor_o_igual_F']:.2f} "
              f"frac=2 {r['frac_igual_a_2']:.2f}")

    tmp = SALIDA.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(salida, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    os.replace(tmp, SALIDA)
    print(f"\n-> {SALIDA}")


if __name__ == "__main__":
    main()
