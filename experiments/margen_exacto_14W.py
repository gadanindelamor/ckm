"""
margen_exacto_14W.py — el margen exacto de las 14 W de las curvas, por enumeración

Texto para Code 20, punto 1 (Opus 5.5, 29 oct 2026; respalda el Pendiente R1 del
paper v33). **Mide y registra. No elige ningún umbral, margen ni percentil**, y
no toca `services/` ni `iap_chatroom/`.

## Qué mide

Las 14 W de las curvas de `calibrate` de los intentos 2, 3 y 4 de `serie2_caso0`
son todas de **N = 20** (medido acá, no supuesto). Para cada una:

- `n_eff0_exacto` — N_eff de la W, **exacto**, enumerando los 2^20 estados y
  pesando cada uno por su probabilidad bajo `sample_s0` (la medida del código:
  fracción activa uniforme en [0,3; 0,7] y después los nodos; un estado con `a`
  activos pesa `P(a)/C(N,a)`, con `P(a)` de `piso_del_colapso.p_activos_codigo`).
  Las órbitas se agrupan como las agrupa `basin_masses`: por **órbita**
  (`relax_orbit`), no por estado terminal.
- `F(N)` — el N_eff del extremo de colapso bajo la misma medida, por la forma
  cerrada del lema (`piso_del_colapso.forma_cerrada`) y, **una vez por N**,
  por enumeración del colapso (`piso_del_colapso.masas_por_enumeracion`) como
  control.
- `m_exacto` = `1 − ln F / ln n_eff0_exacto` y su signo. Es la definición
  candidata del texto 20 (no registrada): "separa" ⇔ `N_eff(W) > F(N, μ)`.
  Coincide con el `margen_separacion` de `calibrate` —`d_colapso − d_sin_cambio`
  con `d_sin_cambio = 0`, `calibrate.py:337`— cuando los dos N_eff se toman
  exactos en lugar de muestreados.
- al lado, lo que **registró** `calibrate`: `n_eff` de λ=0 y de λ=1, el
  `margen_separacion`, el `estado`, la `causa` y su `n_runs`; y el IC del 14.1
  (`simpson_en_las_curvas_resultado.json`, punto λ=0 de la misma curva).
- `n_eff0_muestreado_200_0` — N_eff0 muestreado al default de hoy, 200 / 0 /
  uniforme, leído de `calibrate.N_RUNS_DEFAULT` y `SEED_DEFAULT`, no escrito a
  mano. El intento 4 calibró a `n_runs = 1000`: la columna lo dice.
- `N` y su **paridad** (delamor, 29 oct: "N paridad").

Además, lo que la enumeración deja ver y el punto 2c del texto 20 pide sobre
estas mismas W: cuántas órbitas hay, el histograma de períodos, cuántas órbitas
son **autoconjugadas** (O = −O) y cuánta masa exacta tienen. Esas funciones se
exportan para que `simetria_neff_dos.py` las reutilice en vez de reescribirlas.

## Condiciones

- Las W se reconstruyen desde los prefijos del corpus y se **verifican contra su
  sha** antes de usarlas, con la cadena de `seleccion_anterior`: es
  `simpson_en_las_curvas.w_por_sha`, que se **importa**, no se copia.
- **Dos dinámicas, las dos reportadas, y difieren.** El paso síncrono de
  `relax_orbit` es `h = W @ s` en float64 con la regla de empate "h = 0
  conserva σ_i" (`landscape_engine.py:73-74`). Las entradas de estas W son
  racionales de denominador chico (medido: q = 12), así que el h **exacto** es
  un entero sobre q y se calcula sin error en int64. El h de float64 difiere
  del exacto sólo donde el exacto es **0**: ahí el float da ±1e-17 y el nodo se
  **voltea** en lugar de conservarse. **No es un detalle numérico:** medido
  sobre estas 14 W, entre 140.250 y 225.510 de los 1.048.576 estados (13 % a
  22 %) caen en un sucesor distinto, y el N_eff se mueve hasta 0,057. Por eso
  se enumera con las dos:
  - `enumeracion_con_el_paso_del_codigo` — la dinámica del instrumento, la que
    es comparable con lo que registró `calibrate`. Es la columna de la tabla.
  - `enumeracion_con_aritmetica_exacta` — el objeto matemático que la regla de
    empate describe.
  La enumeración del paso del código se verifica contra `relax_orbit` real
  (500/500 por W, abajo); la diferencia entre las dos columnas **no cambia
  ninguno de los signos** de este punto, y se declara en lugar de elegir una.
- La enumeración vectorizada se **verifica contra `relax_orbit` real** sobre una
  muestra estratificada por cantidad de nodos activos (misma forma que
  `piso_del_colapso.verificar_muestra_estratificada`): se compara la órbita
  devuelta, no sólo su tamaño.
- `n_runs = 200`, `seed = 0`, distribución **uniforme** (`sampling_mode
  "uniform"`: la banda de `sample_s0` con elección uniforme de nodos) para todo
  lo muestreado acá. El 1000 del intento 4 es del registro, no de este script.

## Qué declara

Nada se interpreta. No se nombra qué significa la paridad de N, no se elige
ningún número para que algo separe, y la definición candidata del margen **no**
se registra: eso lo hace Opus con el reporte.

Salida: `experiments/margen_exacto_14W_resultado.json` (escritura atómica:
`.tmp` y rename) y una tabla por stdout.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from math import comb, gcd, log
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "services"))
sys.path.insert(0, str(ROOT / "experiments"))

from calibrate import N_RUNS_DEFAULT, SEED_DEFAULT          # noqa: E402
from landscape_engine import count_attractors, relax_orbit  # noqa: E402

import piso_del_colapso as PC                               # noqa: E402
import simpson_en_las_curvas as S                            # noqa: E402

SALIDA = Path(__file__).resolve().parent / "margen_exacto_14W_resultado.json"


# ── las W ───────────────────────────────────────────────────────────────────

def w_de_las_curvas() -> list:
    """
    Las 14 W de las curvas, en el orden en que aparecen, con su registro.

    Cada entrada: intento, sha, W (verificada por sha), y las condiciones y el
    estado que registró `calibrate`. Si una W no verifica su sha, queda con
    `W = None` y se declara: no se usa.
    """
    filas = []
    for nombre, traj, corpus in S.INTENTOS:
        ws, fallidas = S.w_por_sha(ROOT / corpus)
        for cal in S.curvas_de(ROOT / traj):
            cond = cal["condiciones"]
            sha = cond["w_sha"]
            filas.append({
                "intento": nombre,
                "w_sha": sha,
                "W": ws.get(sha),
                "sha_verifica": sha in ws,
                "estado": cal["estado"],
                "causa": cond.get("causa"),
                "n_runs_registrado": cond.get("n_runs"),
                "seed_registrado": cond.get("seed"),
                "n_eff0_registrado": cond["curva"][0]["n_eff"],
                "n_eff_colapso_registrado": cond["curva"][-1]["n_eff"],
                "margen_registrado": cond.get("margen_separacion"),
                "w_no_recomputables_en_la_corrida": len(fallidas),
            })
    return filas


def ic_del_141() -> dict:
    """El IC del punto λ=0 de cada curva, del resultado del 14.1, por sha."""
    p = Path(__file__).resolve().parent / "simpson_en_las_curvas_resultado.json"
    if not p.exists():
        return {}
    d = json.load(open(p, encoding="utf-8"))
    out = {}
    for c in d["curvas"]:
        p0 = c["puntos"][0]
        out[c["w_sha"]] = {
            "n_eff_plugin": p0["n_eff_plugin"],
            "n_eff_unb": p0["n_eff_unb"],
            "n_eff_ic95": p0["n_eff_ic95"],
            "n_runs": c["n_runs"],
        }
    return out


# ── el paso síncrono sobre todos los estados ────────────────────────────────

def denominador_comun(W: np.ndarray, tol: float = 1e-12) -> int | None:
    """
    El menor `q` tal que `q·W` es entero, o None si no lo hay con q ≤ 10^6.

    Se busca con `Fraction.limit_denominator` entrada por entrada y se
    **verifica**: si alguna entrada no es `p/q` dentro de `tol`, devuelve None y
    la enumeración exacta no se hace (sólo la de float64, declarada).
    """
    q = 1
    for x in np.asarray(W, dtype=float).ravel():
        f = Fraction(float(x)).limit_denominator(10 ** 6)
        if abs(float(f) - float(x)) > tol:
            return None
        q = q * f.denominator // gcd(q, f.denominator)
        if q > 10 ** 6:
            return None
    Wq = np.asarray(W, dtype=float) * q
    if np.abs(Wq - np.round(Wq)).max() > 1e-6:
        return None
    return int(q)


def _bits(idx: np.ndarray, N: int) -> np.ndarray:
    """Los N bits de cada índice, como uint8 (bit i = nodo i activo)."""
    return ((idx[:, None] >> np.arange(N, dtype=np.uint32)) & 1).astype(np.uint8)


def siguiente(W: np.ndarray, modo: str, bloque: int = 1 << 16) -> tuple:
    """
    `nxt[s]` = el estado que sigue a `s` en el paso síncrono, para los 2^N
    estados, con la regla de empate del código ("h = 0 conserva σ_i").

    `modo = "exacto"` → `h` en int64 sobre `q·W` con `q` entero. Sin error y
    **sin depender del orden de suma**, así que los empates son los verdaderos.

    `modo = "codigo"` → lo que hace `relax_orbit`: `h = W @ s` en float64. La
    diferencia no es cosmética y se midió acá: el producto por bloques
    (`sigma @ W.T`, BLAS matriz–matriz) suma en otro orden que el `W @ s`
    (matriz–vector) del código, y donde el `h` exacto es **0** el float da
    ±1e-17 y el nodo se **voltea** en vez de conservarse. Como |h| exacto es
    ≥ 1/q cuando no es 0, el signo del float sólo puede diferir del exacto en
    esos empates: así que este modo parte del exacto y **recomputa con el
    propio `W @ s` del código, estado por estado, sólo los estados que tienen
    algún empate exacto**. Verificado contra `relax_orbit`.

    Devuelve `(nxt, info)`, con `info`: empates exactos (pares estado–nodo),
    estados con algún empate, y en `"codigo"` cuántos estados terminan en un
    sucesor distinto del exacto.
    """
    N = W.shape[0]
    total = 1 << N
    q = denominador_comun(W)
    if q is None:
        raise ValueError("W sin denominador común: la enumeración exacta no "
                         "aplica a esta W")
    Mq = np.round(np.asarray(W, dtype=float) * q).astype(np.int64)
    Wf = np.asarray(W, dtype=np.float64)

    nxt = np.empty(total, dtype=np.uint32)
    pot = (np.uint32(1) << np.arange(N, dtype=np.uint32))
    n_empates, con_empate = 0, []
    for ini in range(0, total, bloque):
        idx = np.arange(ini, min(ini + bloque, total), dtype=np.uint32)
        b = _bits(idx, N)
        h = (2 * b.astype(np.int64) - 1) @ Mq.T
        empate = h == 0
        n_empates += int(np.count_nonzero(empate))
        nuevo = np.where(h > 0, 1, np.where(h < 0, 0, b)).astype(np.uint32)
        nxt[idx] = (nuevo * pot).sum(axis=1, dtype=np.uint32)
        if modo == "codigo":
            con_empate.append(idx[empate.any(axis=1)])

    info = {"empates_exactos_estado_nodo": n_empates,
            "denominador_comun_q": q}
    if modo != "codigo":
        info["estados_con_algun_empate"] = None
        return nxt, info

    sospechosos = np.concatenate(con_empate) if con_empate else np.empty(0, np.uint32)
    distintos = 0
    for i in sospechosos:
        b = _bits(np.array([i], dtype=np.uint32), N)[0]
        s = 2.0 * b.astype(np.float64) - 1.0
        hf = Wf @ s                      # el paso del código, tal cual
        nuevo = np.where(hf > 0, 1, np.where(hf < 0, 0, b)).astype(np.uint32)
        j = np.uint32((nuevo * pot).sum(dtype=np.uint32))
        if j != nxt[i]:
            distintos += 1
            nxt[i] = j
    info["estados_con_algun_empate"] = int(sospechosos.size)
    info["estados_con_sucesor_distinto_del_exacto"] = distintos
    return nxt, info


def orbitas(nxt: np.ndarray, max_periodo: int = 256) -> tuple:
    """
    Agrupa los 2^N estados por órbita sobre el grafo funcional `nxt`.

    Devuelve `(orbita_de, periodo_de_la_orbita, periodo_max)`:
    `orbita_de[s]` es el **menor índice de estado del ciclo** al que cae `s`
    —identificador canónico de la órbita, que no depende de ninguna fase— y
    `periodo_de_la_orbita[s]` el tamaño de ese ciclo.

    Cómo: se aplica `nxt` 2^k veces por duplicación de punteros hasta que todo
    estado está sobre su ciclo (k = N basta: la cola es < 2^N), y después se
    recorre el ciclo acumulando el mínimo. Es exacto, no heurístico: el espacio
    es finito y el mapa determinista, igual que en `relax_orbit`.
    """
    n = nxt.size
    f = nxt.copy()
    k = max(1, int(np.ceil(np.log2(n))))
    for _ in range(k):
        f = f[f]                      # f = nxt^(2^k): cae sobre el ciclo
    mn = f.copy()
    per = np.zeros(n, dtype=np.int32)
    cur = nxt[f]
    cerrado = cur == f
    per[cerrado] = 1
    t = 1
    while not cerrado.all() and t < max_periodo:
        mn = np.minimum(mn, cur)
        cur = nxt[cur]
        t += 1
        nuevo = (cur == f) & ~cerrado
        per[nuevo] = t
        cerrado |= nuevo
    if not cerrado.all():
        raise RuntimeError(f"ciclos de período > {max_periodo}: no cerrados "
                           f"{int((~cerrado).sum())}")
    return mn, per, int(per.max())


def pesos_medida_codigo(N: int) -> np.ndarray:
    """
    El peso de cada uno de los 2^N estados bajo `sample_s0`: un estado con `a`
    nodos activos pesa `P(a)/C(N,a)`, con `P(a)` de `piso_del_colapso`.
    """
    pa = PC.p_activos_codigo(N)
    por_a = np.array([pa[a] / comb(N, a) for a in range(N + 1)])
    pop = np.bitwise_count(np.arange(1 << N, dtype=np.uint32))
    return por_a[pop]


def n_eff_exacto(W: np.ndarray, modo: str = "exacto") -> dict:
    """
    N_eff exacto de W bajo la medida del código, por enumeración de los 2^N
    estados, agrupando por órbita como `basin_masses`.

    Reporta además lo que la enumeración deja ver sin costo extra: cuántas
    órbitas tienen masa > 0, el histograma de períodos (pesado por masa), y las
    órbitas **autoconjugadas** (O = −O), con su masa exacta. La conjugación
    σ → −σ es el XOR con la máscara de N unos.
    """
    N = W.shape[0]
    nxt, info = siguiente(W, modo)
    orb, per, per_max = orbitas(nxt)
    w = pesos_medida_codigo(N)

    masa = np.bincount(orb.astype(np.int64), weights=w, minlength=1 << N)
    vivos = np.nonzero(masa)[0]
    masas = masa[vivos]
    masas = masas / masas.sum()
    theta = float(np.square(masas).sum())

    # período por órbita (todas las fases de un ciclo comparten per)
    per_orb = per[vivos]
    hist = {}
    for p in np.unique(per_orb):
        sel = per_orb == p
        hist[int(p)] = {"orbitas": int(sel.sum()),
                        "masa": float(masas[sel].sum())}

    comp = np.arange(1 << N, dtype=np.uint32) ^ np.uint32((1 << N) - 1)
    auto = orb[comp[vivos]] == vivos          # la órbita de −σ es la misma
    return {
        "N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
        "modo_del_paso": modo,
        "estados_enumerados": 1 << N,
        "empates": info,
        "pesos_suman": float(w.sum()),
        "n_orbitas_con_masa": int(vivos.size),
        "periodo_max": per_max,
        "periodos": hist,
        "simpson": theta,
        "n_eff_exacto": 1.0 / theta,
        "n_orbitas_autoconjugadas": int(auto.sum()),
        "masa_autoconjugada": float(masas[auto].sum()),
        "masa_maxima": float(masas.max()),
        # control de la simetría: la masa de O y de −O tiene que coincidir
        "max_dif_masa_O_vs_menosO": float(
            np.abs(masas - masa[orb[comp[vivos]]] / masa[vivos].sum()).max()
        ),
    }


def verificar_contra_relax_orbit(W: np.ndarray, modo: str,
                                 por_a: int = 25, seed: int = 7) -> dict:
    """
    La enumeración vectorizada contra `relax_orbit` real, sobre una muestra
    estratificada por cantidad de nodos activos.

    Se compara la **órbita** (el conjunto de estados), no su tamaño: la órbita
    de `relax_orbit` se lleva a índices y se le toma el mínimo, que es el mismo
    identificador canónico que usa `orbitas`.
    """
    N = W.shape[0]
    nxt, _info = siguiente(W, modo)
    orb, per, _ = orbitas(nxt)
    rng = np.random.default_rng(seed)
    pot = (1 << np.arange(N)).astype(np.int64)
    malos, revisados = [], 0
    for a in range(1, N + 1):
        for _ in range(por_a):
            s = np.full(N, -1.0)
            s[rng.choice(N, a, replace=False)] = 1.0
            i = int(((s > 0).astype(np.int64) * pot).sum())
            orbita, periodo, _, _ = relax_orbit(s, W)
            idxs = [int(((np.frombuffer(b, dtype=np.float64) > 0)
                         .astype(np.int64) * pot).sum()) for b in orbita]
            revisados += 1
            if min(idxs) != int(orb[i]) or periodo != int(per[i]):
                malos.append({"estado": i, "a": a,
                              "relax_orbit": [min(idxs), periodo],
                              "enumeracion": [int(orb[i]), int(per[i])]})
    return {"revisados": revisados, "discrepancias": malos,
            "coincide": not malos}


# ── el margen ───────────────────────────────────────────────────────────────

def margen(n_eff0: float, F: float) -> float | None:
    """
    `m = 1 − ln F / ln N_eff0` — la definición candidata del texto 20, que es el
    `margen_separacion` de `calibrate` con los dos N_eff exactos.

    None si `N_eff0 ≤ 1`: ahí `d_ckm` tampoco es medible (`landscape_engine
    .d_ckm` devuelve None) y no hay margen que escribir.
    """
    if n_eff0 <= 1.0:
        return None
    return 1.0 - log(F) / log(n_eff0)


def main() -> None:
    filas = w_de_las_curvas()
    ics = ic_del_141()

    # la W que separó, primera (texto 20, punto 1)
    filas.sort(key=lambda f: (f["estado"] != "calibrado", f["intento"]))

    Ns = sorted({f["W"].shape[0] for f in filas if f["W"] is not None})
    piso = {}
    for N in Ns:
        cerrada = PC.forma_cerrada(N, "codigo")
        enum = PC.masas_por_enumeracion(N, "codigo")
        piso[N] = {
            "F_forma_cerrada": cerrada,
            "F_por_enumeracion": enum["n_eff_exacto"],
            "dif": cerrada - enum["n_eff_exacto"],
            "pesos_suman_1": enum["pesos_suman_1"],
            "n_orbitas_periodo_2_del_colapso": enum["n_orbitas_periodo_2"],
        }
        print(f"F({N}) forma cerrada = {cerrada:.6f} · por enumeración = "
              f"{enum['n_eff_exacto']:.6f} · dif = {cerrada - enum['n_eff_exacto']:.2e}")

    salida = {
        "que": "el margen exacto de las 14 W de las curvas (texto 20, punto 1)",
        "defaults_del_instrumento": {"n_runs": N_RUNS_DEFAULT,
                                     "seed": SEED_DEFAULT,
                                     "sampling_mode": "uniform"},
        "piso_F_por_N": piso,
        "W": [],
    }

    enc = ("sha      int  N par  n_eff0_exacto      F     m_exacto  signo  "
           "n_eff0_reg  margen_reg  estado        n_eff0_200_0")
    print("\n" + enc)
    print("-" * len(enc))

    for f in filas:
        W = f["W"]
        fila = {k: v for k, v in f.items() if k != "W"}
        if W is None:
            fila["no_usada"] = "sha no verifica"
            salida["W"].append(fila)
            continue
        N = W.shape[0]
        cod = n_eff_exacto(W, "codigo")     # la dinámica del instrumento
        art = n_eff_exacto(W, "exacto")     # la aritmética exacta
        ver = verificar_contra_relax_orbit(W, "codigo")
        F = piso[N]["F_forma_cerrada"]
        m_cod = margen(cod["n_eff_exacto"], F)
        m_art = margen(art["n_eff_exacto"], F)
        n200 = count_attractors(W, n_runs=N_RUNS_DEFAULT, seed=SEED_DEFAULT)

        fila.update({
            "N": N, "paridad_N": cod["paridad_N"],
            # el número que es comparable con calibrate: misma dinámica
            "enumeracion_con_el_paso_del_codigo": cod,
            "enumeracion_con_aritmetica_exacta": art,
            "difiere_el_paso": {
                "n_eff_codigo_menos_exacto":
                    cod["n_eff_exacto"] - art["n_eff_exacto"],
                "n_orbitas_codigo_menos_exacto":
                    cod["n_orbitas_con_masa"] - art["n_orbitas_con_masa"],
                "estados_con_sucesor_distinto":
                    cod["empates"].get("estados_con_sucesor_distinto_del_exacto"),
                "estados_con_algun_empate_exacto":
                    cod["empates"].get("estados_con_algun_empate"),
            },
            "verificacion_contra_relax_orbit": ver,
            "F": F,
            "m_exacto_paso_del_codigo": m_cod,
            "m_exacto_aritmetica_exacta": m_art,
            "separa_paso_del_codigo": (cod["n_eff_exacto"] > F),
            "separa_aritmetica_exacta": (art["n_eff_exacto"] > F),
            "n_eff0_muestreado_200_0_uniforme": float(n200),
            "ic_del_141": ics.get(f["w_sha"]),
        })
        salida["W"].append(fila)

        print(f"{f['w_sha'][:8]} {f['intento'][-1]}   {N} {cod['paridad_N'][:3]} "
              f"{cod['n_eff_exacto']:>14.6f} {F:>8.6f} "
              f"{(m_cod if m_cod is not None else float('nan')):>+10.6f} "
              f"{'separa' if cod['n_eff_exacto'] > F else '  no  '}  "
              f"{f['n_eff0_registrado']:>10.6f}  "
              f"{(f['margen_registrado'] if f['margen_registrado'] is not None else float('nan')):>+10.6f}  "
              f"{f['estado']:<13} {n200:>10.6f}")

    tmp = SALIDA.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, SALIDA)
    print(f"\n-> {SALIDA}")


if __name__ == "__main__":
    main()
