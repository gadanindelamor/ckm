"""
torsion_lo_que_queda_afuera.py — qué deja afuera el rechazo completo de período 2

Texto para Code 20, punto 4 (Opus 5.5, 29 oct 2026; decisión de delamor del 8
oct, CP3 1a: a `Δ_r_pares` entran **sólo** los pares rechazados en las dos fases
de la órbita, y la torsión va a `Δ_r_torsion` y **no** entra a `W_eff`,
`services/monitor_service.py:328-350`). Opus decidió medir cuánto deja afuera
esa decisión. **Mide y registra. No decide nada sobre qué entra a Δ_r**, y no
toca `services/` ni `iap_chatroom/`.

## Qué mide

**(a) Los intentos 2, 3 y 4, de sus estados preservados.** Por evaluación de
Monitor: `periodo_orbita`, `cola_orbita`, `n_aceptados`, `n_expulsados`,
`n_torsion`, `Delta_r_sum`, `Delta_r_torsion_sum`, `N` y su paridad. Una tabla
por intento y un resumen: cuántas evaluaciones de período 2 y cuántas con
torsión > 0.

**(d) El mecanismo, contra el código.** Lectura de Opus de `pares_por_orbita`
(`landscape_engine.py:93-146`) que este script verifica: un par está expulsado
en una fase si **alguno** de sus dos nodos está en −1; en una órbita `{σ, −σ}`
los caídos de una fase son los activos de la otra; entonces un par con un nodo
caído y el otro no queda expulsado en las dos fases, y un par con los dos nodos
del mismo lado queda en **torsión**. Si es así, el rechazo completo deja afuera
justo esos pares en las órbitas autoconjugadas. Se cuenta sobre:

1. el **colapso** con N par (4..20), con un `sigma_prompt` de la banda;
2. las W de la búsqueda del punto 2b que tienen masa autoconjugada;
3. las órbitas autoconjugadas de las **14 W** del punto 1;
4. y, **separadas**, las órbitas de período 2 que **no** son autoconjugadas
   (`{a, b}` con `b ≠ −a`).

Sólo se cuenta: no se decide nada sobre qué entra a `Δ_r`.

## Condiciones

- `n_runs = 200`, `seed = 0`, distribución **uniforme**, leídos de
  `calibrate.N_RUNS_DEFAULT` / `SEED_DEFAULT`. Los estados preservados traen sus
  propias condiciones (el intento 4 corrió a 1000) y se reportan como vienen:
  son un registro, no una medición nueva.
- **Qué se usa de `sigma_prompt`, declarado.** En el Monitor, `sigma_prompt` son
  los nodos que el texto declaró activos, y la órbita es la relajación de ese
  estado. Acá no hay textos: se usa **el propio σ₀ muestreado** como
  `sigma_prompt`, que es la elección de este experimento y no del instrumento.
  Con eso el conjunto declarado es exactamente el de los activos de σ₀, que es
  el caso en el que la lectura de Opus es más nítida.
- En el colapso con N par, `sigma_prompt` es un estado **balanceado** de la
  banda (`a = N/2`, que está en [0,3N; 0,7N] para todo N ≥ 2): es el que cae en
  la órbita de período 2, que es la autoconjugada del colapso. Sale de
  `sample_s0` con `seed = 0`, tomando el primer sorteo con `a = N/2`; la seed es
  la del instrumento y el filtro se declara.

Salida: `experiments/torsion_lo_que_queda_afuera_resultado.json` (escritura
atómica) y las tablas por stdout.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "services"))
sys.path.insert(0, str(ROOT / "experiments"))

from calibrate import N_RUNS_DEFAULT, SEED_DEFAULT              # noqa: E402
from landscape_engine import (_muestra, _setup, fases_de_orbita,  # noqa: E402
                              pares_por_orbita, relax_orbit, sample_s0)

import margen_exacto_14W as ME                                  # noqa: E402
import piso_del_colapso as PC                                   # noqa: E402
import simetria_neff_dos as SY                                  # noqa: E402

SALIDA = (Path(__file__).resolve().parent
          / "torsion_lo_que_queda_afuera_resultado.json")

# los estados preservados por el --reset, con su timestamp (texto 15, punto 1)
INTENTOS = {
    "intento2": "process/monitor_trajectory.jsonl.bak_1792649008_serie2_caso0",
    "intento3": "process/monitor_trajectory.jsonl.bak_1793085284_serie2_caso0",
    "intento4": "process/monitor_trajectory.jsonl.bak_1793150043_serie2_caso0",
}

CLAVES = ("periodo_orbita", "cola_orbita", "n_aceptados", "n_expulsados",
          "n_torsion", "Delta_r_sum", "Delta_r_torsion_sum")


# ── (a) los intentos ────────────────────────────────────────────────────────

def evaluaciones_de(path: Path) -> dict:
    """
    Las evaluaciones de Monitor de un estado preservado, con las claves que
    pide el punto 4a. Si una clave **no está**, queda como `None` y se cuenta
    en `claves_ausentes`: no se inventa.
    """
    filas, ausentes = [], {k: 0 for k in CLAVES}
    with open(path, encoding="utf-8") as fh:
        for i, linea in enumerate(fh):
            d = json.loads(linea)
            p = d.get("panel", {})
            N = p.get("condicion_W", {}).get("N")
            fila = {"i": i, "t": d.get("t"), "device_id": d.get("device_id"),
                    "N": N,
                    "paridad_N": None if N is None else
                    ("par" if N % 2 == 0 else "impar"),
                    "n_runs": p.get("condicion_W", {}).get("n_runs"),
                    "w_sha": (p.get("condicion_W", {}).get("w_sha") or "")[:8]}
            for k in CLAVES:
                if k in p:
                    fila[k] = p[k]
                else:
                    fila[k] = None
                    ausentes[k] += 1
            fila["pares_torsion"] = p.get("pares_torsion")
            filas.append(fila)
    per2 = [f for f in filas if f["periodo_orbita"] == 2]
    tor = [f for f in filas if (f["n_torsion"] or 0) > 0]
    dtor = [f for f in filas if (f["Delta_r_torsion_sum"] or 0) > 0]
    return {
        "archivo": str(path.relative_to(ROOT)),
        "evaluaciones": len(filas),
        "claves_ausentes": ausentes,
        "con_periodo_2": len(per2),
        "con_torsion_mayor_que_0": len(tor),
        "con_Delta_r_torsion_mayor_que_0": len(dtor),
        "periodos_vistos": sorted({f["periodo_orbita"] for f in filas
                                   if f["periodo_orbita"] is not None}),
        "N_vistos": sorted({f["N"] for f in filas if f["N"] is not None}),
        "n_runs_vistos": sorted({f["n_runs"] for f in filas
                                 if f["n_runs"] is not None}),
        "suma_n_aceptados": sum(f["n_aceptados"] or 0 for f in filas),
        "suma_n_expulsados": sum(f["n_expulsados"] or 0 for f in filas),
        "suma_n_torsion": sum(f["n_torsion"] or 0 for f in filas),
        "suma_Delta_r": sum(f["Delta_r_sum"] or 0 for f in filas),
        "suma_Delta_r_torsion": sum(f["Delta_r_torsion_sum"] or 0
                                    for f in filas),
        "filas": filas,
    }


# ── (d) el mecanismo ────────────────────────────────────────────────────────

def _clase_de_orbita(orbita: frozenset, N: int) -> str:
    """
    `punto_fijo`, `periodo_2_autoconjugada` (O = −O) o
    `periodo_2_no_autoconjugada` ({a, b} con b ≠ −a), o `periodo_mayor_que_2`.
    """
    fases = fases_de_orbita(orbita, N)
    if len(fases) == 1:
        return "punto_fijo"
    if len(fases) > 2:
        return "periodo_mayor_que_2"
    conj = frozenset((-f).tobytes() for f in fases)
    return ("periodo_2_autoconjugada" if conj == orbita
            else "periodo_2_no_autoconjugada")


def clasificar_pares(W: np.ndarray, sigma_prompt: np.ndarray) -> dict:
    """
    `pares_por_orbita` sobre la órbita de `sigma_prompt`, con la clase de la
    órbita y el detalle que la lectura de Opus predice: cuántos pares tienen
    los dos nodos del **mismo** lado en una fase y cuántos tienen uno de cada.
    """
    N = W.shape[0]
    orbita, periodo, cola, _ = relax_orbit(sigma_prompt, W)
    fases = fases_de_orbita(orbita, N)
    acep, exp, tor = pares_por_orbita(sigma_prompt, fases)
    declarados = np.where(sigma_prompt > 0)[0]
    n_pares = len(declarados) * (len(declarados) - 1) // 2
    # el detalle, en la primera fase (el orden no importa: ver el docstring de
    # pares_por_orbita)
    s = fases[0]
    mismo_lado = sum(1 for a in range(len(declarados))
                     for b in range(a + 1, len(declarados))
                     if (s[declarados[a]] > 0) == (s[declarados[b]] > 0))
    return {"N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
            "clase": _clase_de_orbita(orbita, N),
            "periodo": periodo, "cola": cola,
            "nodos_declarados": int(len(declarados)),
            "pares_declarados": n_pares,
            "aceptados": len(acep), "expulsados": len(exp), "torsion": len(tor),
            "pares_con_los_dos_nodos_del_mismo_lado_en_una_fase": mismo_lado,
            "pares_con_uno_de_cada_lado": n_pares - mismo_lado}


def sigma_balanceado_de_la_banda(N: int, seed: int = SEED_DEFAULT,
                                 max_sorteos: int = 10000) -> np.ndarray | None:
    """
    El primer σ₀ de `sample_s0` (seed del instrumento) con exactamente `N/2`
    activos — el que cae en la órbita de período 2 del colapso. `a = N/2` está
    en la banda [0,3N; 0,7N] para todo N ≥ 2; el filtro se declara.
    """
    if N % 2:
        return None
    rng = np.random.default_rng(seed)
    for _ in range(max_sorteos):
        s = sample_s0(rng, N, None)
        if int((s > 0).sum()) == N // 2:
            return s
    return None


def colapso_por_N(Ns=tuple(range(4, 21, 2))) -> list:
    """(d.1) El colapso con N par, con un sigma_prompt balanceado de la banda."""
    out = []
    for N in Ns:
        s = sigma_balanceado_de_la_banda(N)
        if s is None:
            out.append({"N": N, "sin_sigma_balanceado": True})
            continue
        out.append(clasificar_pares(PC.W_colapso(N), s))
    return out


def sobre_W_con_autoconjugada(Ns=(4, 5, 6, 7, 8)) -> list:
    """
    (d.2) Las W de la búsqueda del punto 2b que tienen masa autoconjugada: se
    toma, por N, la W del **mínimo** de N_eff que esa búsqueda ya encontró (es
    una W con α alto, que es donde la lectura de Opus se juega), y se clasifica
    cada órbita que el muestreo del instrumento alcanza.
    """
    p = Path(__file__).resolve().parent / "simetria_neff_dos_resultado.json"
    if not p.exists():
        return [{"falta": str(p)}]
    d = json.load(open(p, encoding="utf-8"))
    out = []
    for r in d["b_busqueda"]:
        if r["N"] not in Ns:
            continue
        W = SY._arma_W(r["N"], r["W_del_minimo_triangulo_superior"])
        out.append({"N": r["N"],
                    "alpha_de_esta_W": r["detalle_del_minimo"]["alpha"],
                    "W_triangulo_superior": r["W_del_minimo_triangulo_superior"],
                    **por_clase(W)})
    return out


def por_clase(W: np.ndarray, n_runs: int = N_RUNS_DEFAULT,
              seed: int = SEED_DEFAULT) -> dict:
    """
    El muestreo del instrumento sobre W, agrupando por **clase de órbita** y
    sumando aceptados, expulsados y torsión.

    Usa `_setup`/`_muestra` de `landscape_engine` —el mismo muestreo, misma
    seed, misma secuencia— y cada σ₀ hace de `sigma_prompt`, que es la elección
    declarada de este experimento.
    """
    rng, beta, probs, n_w = _setup(W, seed, False, False, None)
    acc: dict = {}
    for _ in range(n_runs):
        s0 = _muestra(rng, W, probs, beta, n_w)
        r = clasificar_pares(W, s0)
        a = acc.setdefault(r["clase"], {
            "muestras": 0, "pares_declarados": 0, "aceptados": 0,
            "expulsados": 0, "torsion": 0, "mismo_lado": 0, "uno_de_cada": 0})
        a["muestras"] += 1
        a["pares_declarados"] += r["pares_declarados"]
        a["aceptados"] += r["aceptados"]
        a["expulsados"] += r["expulsados"]
        a["torsion"] += r["torsion"]
        a["mismo_lado"] += r["pares_con_los_dos_nodos_del_mismo_lado_en_una_fase"]
        a["uno_de_cada"] += r["pares_con_uno_de_cada_lado"]
    for a in acc.values():
        tot = a["pares_declarados"] or 1
        a["frac_torsion"] = a["torsion"] / tot
        a["frac_expulsados"] = a["expulsados"] / tot
        a["frac_aceptados"] = a["aceptados"] / tot
    return {"n_runs": n_runs, "seed": seed, "por_clase": acc}


def sobre_las_14_W() -> list:
    """(d.3 y d.4) Las 14 W del punto 1, por clase de órbita."""
    out = []
    for f in ME.w_de_las_curvas():
        if f["W"] is None:
            continue
        out.append({"w_sha": f["w_sha"][:8], "intento": f["intento"],
                    **por_clase(f["W"])})
    return out


def main() -> None:
    salida = {
        "que": "que deja afuera el rechazo completo de periodo 2 (texto 20, "
               "punto 4)",
        "la_decision": "a Delta_r_pares entran solo los pares rechazados en "
                       "las dos fases; la torsion va a Delta_r_torsion y no "
                       "entra a W_eff (monitor_service.py:328-350, delamor "
                       "8 oct, CP3 1a)",
        "defaults_del_instrumento": {"n_runs": N_RUNS_DEFAULT,
                                     "seed": SEED_DEFAULT,
                                     "sampling_mode": "uniform"},
        "sigma_prompt_de_este_experimento": (
            "el propio sigma_0 muestreado hace de sigma_prompt: es una "
            "eleccion del experimento, no del instrumento"),
    }

    # (a)
    print("(a) los intentos 2, 3 y 4, de sus estados preservados\n")
    a = {}
    for nombre, rel in INTENTOS.items():
        p = ROOT / rel
        if not p.exists():
            a[nombre] = {"no_esta": rel}
            print(f"  {nombre}: NO ESTÁ ({rel})")
            continue
        a[nombre] = evaluaciones_de(p)
        r = a[nombre]
        print(f"  {nombre}: {r['evaluaciones']} evaluaciones · "
              f"períodos {r['periodos_vistos']} · N {r['N_vistos']} · "
              f"n_runs {r['n_runs_vistos']}")
        print(f"      período 2: {r['con_periodo_2']} · torsión>0: "
              f"{r['con_torsion_mayor_que_0']} · Δ_r_torsion>0: "
              f"{r['con_Delta_r_torsion_mayor_que_0']}")
        print(f"      sumas: aceptados {r['suma_n_aceptados']} · expulsados "
              f"{r['suma_n_expulsados']} · torsión {r['suma_n_torsion']} · "
              f"Δ_r {r['suma_Delta_r']} · Δ_r_torsion "
              f"{r['suma_Delta_r_torsion']}")
        faltan = {k: v for k, v in r["claves_ausentes"].items() if v}
        print(f"      claves ausentes: {faltan if faltan else 'ninguna'}")
    salida["a_los_intentos"] = a

    hay_torsion = any(isinstance(r, dict) and r.get("suma_n_torsion", 0) > 0
                      for r in a.values())
    salida["b_contrafactica"] = {
        "corresponde": hay_torsion,
        "por_que": ("hay torsión > 0 en algún intento" if hay_torsion else
                    "no hay torsión > 0 en ninguna evaluación de ningún "
                    "intento: el punto 4c dice reportar la tabla de (a) y no "
                    "armar la contrafáctica"),
    }
    print(f"\n(b/c) contrafáctica: "
          f"{'CORRESPONDE' if hay_torsion else 'no corresponde'} — "
          f"{salida['b_contrafactica']['por_que']}")

    # (d)
    print("\n(d.1) el colapso con N par, sigma_prompt balanceado de la banda")
    col = colapso_por_N()
    salida["d1_colapso"] = col
    print(f"{'N':>4}{'par':>6}{'clase':>28}{'declarados':>12}{'pares':>7}"
          f"{'acep':>6}{'exp':>6}{'tors':>6}{'mismo lado':>12}{'1 de cada':>11}")
    for r in col:
        if r.get("sin_sigma_balanceado"):
            print(f"{r['N']:>4}  sin sigma balanceado de la banda")
            continue
        print(f"{r['N']:>4}{r['paridad_N']:>6}{r['clase']:>28}"
              f"{r['nodos_declarados']:>12}{r['pares_declarados']:>7}"
              f"{r['aceptados']:>6}{r['expulsados']:>6}{r['torsion']:>6}"
              f"{r['pares_con_los_dos_nodos_del_mismo_lado_en_una_fase']:>12}"
              f"{r['pares_con_uno_de_cada_lado']:>11}")

    print("\n(d.2) las W del punto 2b con masa autoconjugada, por clase")
    w2b = sobre_W_con_autoconjugada()
    salida["d2_W_del_punto_2b"] = w2b
    for r in w2b:
        if "falta" in r:
            print(f"    falta {r['falta']}")
            continue
        print(f"  N={r['N']} α={r['alpha_de_esta_W']:.4f}")
        for clase, v in sorted(r["por_clase"].items()):
            print(f"      {clase:<28} muestras {v['muestras']:>4} · "
                  f"pares {v['pares_declarados']:>6} · acep "
                  f"{v['frac_aceptados']:.3f} · exp {v['frac_expulsados']:.3f}"
                  f" · tors {v['frac_torsion']:.3f}")

    print("\n(d.3/d.4) las 14 W del punto 1, por clase de órbita")
    w14 = sobre_las_14_W()
    salida["d3_d4_las_14_W"] = w14
    agr: dict = {}
    for r in w14:
        for clase, v in r["por_clase"].items():
            g = agr.setdefault(clase, {"muestras": 0, "pares": 0, "acep": 0,
                                       "exp": 0, "tors": 0, "mismo": 0,
                                       "cada": 0, "W": 0})
            g["W"] += 1
            g["muestras"] += v["muestras"]
            g["pares"] += v["pares_declarados"]
            g["acep"] += v["aceptados"]
            g["exp"] += v["expulsados"]
            g["tors"] += v["torsion"]
            g["mismo"] += v["mismo_lado"]
            g["cada"] += v["uno_de_cada"]
    salida["d3_d4_agregado"] = agr
    print(f"{'clase':>28}{'W':>4}{'muestras':>10}{'pares':>8}{'acep':>8}"
          f"{'exp':>8}{'tors':>8}{'mismo lado':>12}{'1 de cada':>11}")
    for clase, g in sorted(agr.items()):
        print(f"{clase:>28}{g['W']:>4}{g['muestras']:>10}{g['pares']:>8}"
              f"{g['acep']:>8}{g['exp']:>8}{g['tors']:>8}{g['mismo']:>12}"
              f"{g['cada']:>11}")

    tmp = SALIDA.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(salida, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    os.replace(tmp, SALIDA)
    print(f"\n-> {SALIDA}")


if __name__ == "__main__":
    main()
