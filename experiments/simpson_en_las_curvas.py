"""
simpson_en_las_curvas.py — el intervalo de Simpson sobre las curvas que ya existen

Texto para Code 14, punto 1 (Opus 5.5, 27 oct 2026; delamor: *"si. CONFIRMO"*).
**Mide y registra. No elige ningún umbral, margen ni percentil**, y no toca
`services/`: lee los registros de `calibrate` de los vivos ya corridos y
recomputa los conteos por cuenca que esos registros no guardaron.

## Qué mide

Para cada punto de cada curva de `calibrate` (cada λ de la grilla):

- `n_eff_plugin`   — N_eff como lo calcula el código hoy: `1 / Σ (c_k/n)²`
                     (`landscape_engine.n_eff` sobre `basin_masses`).
- `simpson_plugin` — el Σm² de ese mismo plug-in, que es `1 / n_eff_plugin`.
- `simpson_unb`    — el estimador **insesgado** de Σm² (Simpson 1949):
                     `Σ c_k(c_k − 1) / (n(n − 1))`. Insesgado exacto bajo
                     muestreo multinomial: con c_k ~ Bin(n, m_k),
                     `E[c_k(c_k − 1)] = n(n − 1)·m_k²`. Verificado en el
                     punto `verificacion_formulas`.
- `var_delta`      — varianza aproximada del plug-in por método delta:
                     `(4/n)·(Σm³ − (Σm²)²)`, con las masas estimadas en lugar
                     de las verdaderas. Sale del gradiente `∂θ/∂p_k = 2p_k`
                     sobre la covarianza multinomial.
- el intervalo `θ ± 1,96·√var` llevado a `N_eff = 1/θ` y a
  `d_ckm = 1 − ln N_eff / ln N_eff0`.

## Condiciones

- Las curvas son las de los intentos **2, 3 y 4** de `serie2_caso0`, las tres
  en `process/`: `...bak_1792649008...`, `...bak_1793085284...` y
  `...bak_1793150043...`. El intento 4 vivía en `experiments/_state_S2-C0/`
  cuando esto se escribió, y el `--reset` del `correr_caso0.sh --check` del 28
  oct lo preservó en `process/` con su timestamp (texto 15, punto 1). La ruta
  se actualizó acá: el script apunta a donde está la evidencia hoy.
  **Son 14 curvas en dos condiciones de muestreo**: los intentos 2 y 3 con
  `n_runs = 200` y el intento 4 con `n_runs = 1000`; las dos con `seed = 0`.
- Los conteos por cuenca **no están en el registro**, y las W intermedias
  tampoco: `w_version_history` guarda shas. Así que cada W se **recomputa**
  desde el prefijo del corpus (`CorpusService._compute`, determinista) y se
  **verifica contra su sha** antes de usarla. Una W cuyo sha no verifica no se
  usa: queda declarada como no recomputable.
- La W del extremo y la grilla salen del registro de cada curva
  (`condiciones.grilla_lambda`), no de los defaults del módulo.
- `d_ckm` usa como `N_eff0` el punto λ=0 de la misma curva, que es el baseline
  reusado (`calibrate.py:283-294`). El intervalo de `d_ckm` propaga **sólo** la
  incertidumbre de `N_eff(λ)`: λ=0 entra como el mismo conjunto de muestras, no
  como una medición independiente. La correlación entre puntos (misma seed →
  mismas σ₀) **no** está en estos intervalos, y por eso la superposición que se
  reporta es la de dos intervalos marginales.

## Qué NO hace

No cambia el estimador del instrumento, el margen, la grilla, el patrón de
calibrate, el n_runs ni el muestreo. No corre ningún vivo.

Salida: `experiments/simpson_en_las_curvas_resultado.json` (escritura atómica,
`.tmp` y rename) y una tabla por stdout.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "services"))

from calibrate import extremo_colapso, interpolar          # noqa: E402
from corpus_service import CorpusService                    # noqa: E402
from landscape_engine import relax_orbit                    # noqa: E402
from w_version import sha256_W                              # noqa: E402

Z = 1.959963984540054   # 95% normal


# ── los tres intentos ───────────────────────────────────────────────────────
INTENTOS = [
    ("intento2", "process/monitor_trajectory.jsonl.bak_1792649008_serie2_caso0",
                 "process/corpus_state.json.bak_1792649008_serie2_caso0"),
    ("intento3", "process/monitor_trajectory.jsonl.bak_1793085284_serie2_caso0",
                 "process/corpus_state.json.bak_1793085284_serie2_caso0"),
    # el intento 4, preservado en process/ por el --reset del 28 oct
    ("intento4", "process/monitor_trajectory.jsonl.bak_1793150043_serie2_caso0",
                 "process/corpus_state.json.bak_1793150043_serie2_caso0"),
]


def curvas_de(traj_path: Path) -> list:
    """Las calibraciones distintas de una trayectoria, en orden de aparición."""
    vistas, out = set(), []
    with open(traj_path, encoding="utf-8") as fh:
        for linea in fh:
            d = json.loads(linea)
            cal = d.get("panel", {}).get("coco", {}).get("calibration")
            if not cal:
                continue
            cond = cal.get("condiciones", {})
            clave = (cond.get("w_sha"), cond.get("t"))
            if clave in vistas:
                continue
            vistas.add(clave)
            out.append(cal)
    return out


def w_por_sha(corpus_path: Path) -> dict:
    """
    Las W de una corrida, reconstruidas desde los prefijos del corpus y
    **verificadas contra su sha**. `{sha: W}` sólo con las que verifican.

    La cadena importa: `_compute` resuelve los empates del top_k con la
    selección anterior (`seleccion_anterior`), así que las W se recomputan en
    el mismo orden en que nacieron, arrastrando los nodos instalados.
    """
    st = json.load(open(corpus_path, encoding="utf-8"))
    textos = st["texts"]
    tmp = tempfile.mktemp(suffix=".json")
    cs = CorpusService(storage_path=tmp, min_texts=30, top_k=20, min_df=2,
                       rebuild_suspendido=True)
    nodos_prev: list = []
    out, fallidas = {}, []
    for h in st["w_version_history"]:
        cs._texts = list(textos[: h["corpus_size"]])
        cs._nodes = list(nodos_prev)
        calc = cs._compute()
        if calc is None:
            fallidas.append((h["corpus_size"], "sin_nodos"))
            continue
        nodos, W, _ = calc
        if sha256_W(W) == h["sha256"]:
            out[h["sha256"]] = W
        else:
            fallidas.append((h["corpus_size"], "sha_no_verifica"))
        nodos_prev = nodos
    if os.path.exists(tmp):
        os.unlink(tmp)
    return out, fallidas


def conteos_por_cuenca(W_eff: np.ndarray, *, n_runs: int, seed: int) -> np.ndarray:
    """
    Los conteos `c_k` por órbita — lo mismo que `basin_masses` antes de
    normalizar. Se replica acá y no se importa porque `basin_masses` devuelve
    masas y el estimador insesgado necesita los conteos enteros.

    Mismo muestreo que el instrumento: `sample_s0` por default (uniforme sobre
    nodos, 30–70% activos), misma seed → mismas σ₀.
    """
    from landscape_engine import _setup, _muestra     # mismo muestreo, sin copia
    rng, beta, probs, n_w = _setup(W_eff, seed, False, False, None)
    cuenta: dict = {}
    for _ in range(n_runs):
        s0 = _muestra(rng, W_eff, probs, beta, n_w)
        orb = relax_orbit(s0, W_eff)[0]
        cuenta[orb] = cuenta.get(orb, 0) + 1
    return np.array(sorted(cuenta.values(), reverse=True), dtype=float)


def estimadores(c: np.ndarray) -> dict:
    """
    Los tres estimadores y el intervalo, sobre los conteos `c_k`.

    `theta` es Σm². `n_eff = 1/theta`. El intervalo es normal sobre `theta`
    (±Z·√var) y se lleva a N_eff invirtiendo: el límite **inferior** de theta da
    el **superior** de N_eff.
    """
    n = float(c.sum())
    m = c / n
    theta_plugin = float(np.square(m).sum())
    theta_unb = float((c * (c - 1.0)).sum() / (n * (n - 1.0))) if n > 1 else float("nan")
    m3 = float(np.power(m, 3).sum())
    var = float((4.0 / n) * (m3 - theta_plugin ** 2))
    se = float(np.sqrt(var)) if var > 0 else 0.0
    lo, hi = theta_plugin - Z * se, theta_plugin + Z * se
    return {
        "n": n,
        "k_cuencas": int(c.size),
        "conteos": [int(x) for x in c],
        "theta_plugin": theta_plugin,
        "theta_unb": theta_unb,
        "n_eff_plugin": 1.0 / theta_plugin,
        "n_eff_unb": (1.0 / theta_unb) if theta_unb and theta_unb > 0 else None,
        "sesgo_plugin_menos_unb": theta_plugin - theta_unb,
        "var_delta": var,
        "se_theta": se,
        "theta_ic95": [lo, hi],
        # el inferior de theta es el superior de N_eff
        "n_eff_ic95": [(1.0 / hi) if hi > 0 else None,
                       (1.0 / lo) if lo > 0 else None],
    }


def d_ckm_ic(n_eff_pt: float, ic: list, n_eff0: float) -> dict:
    """
    `d_ckm = 1 − ln N_eff / ln N_eff0` con el intervalo de N_eff propagado.

    `N_eff0` entra **fijo**: es el baseline reusado de λ=0, las mismas muestras.
    `None` si `ln N_eff0` no sirve de divisor (N_eff0 ≤ 1), que es el mismo
    caso en que `d_ckm` del instrumento devuelve None.
    """
    if n_eff0 is None or n_eff0 <= 1.0:
        return {"d_ckm": None, "d_ckm_ic95": [None, None]}
    ln0 = float(np.log(n_eff0))
    d = 1.0 - float(np.log(n_eff_pt)) / ln0
    # d decrece con N_eff: el superior de N_eff da el inferior de d
    bordes = [1.0 - float(np.log(x)) / ln0 for x in ic if x and x > 0]
    return {"d_ckm": d, "d_ckm_ic95": [min(bordes), max(bordes)] if len(bordes) == 2
            else [None, None]}


def verificacion_formulas(seed: int = 12345) -> dict:
    """
    Las dos fórmulas, verificadas contra el muestreo antes de usarlas (el texto
    14 las da "a verificar").

    Con masas verdaderas conocidas se sortean R réplicas multinomiales de
    tamaño n y se compara:
      - el sesgo del plug-in contra `(θ − Σm³·0)`... medido, no supuesto: el
        promedio de `theta_plugin − θ` contra el promedio de
        `theta_unb − θ` (que debería ser ~0);
      - la varianza empírica del plug-in contra `(4/n)(Σm³ − θ²)`.
    """
    rng = np.random.default_rng(seed)
    out = []
    for masas in ([0.5, 0.3, 0.15, 0.05],
                  [0.44, 0.44, 0.12],
                  [0.9, 0.05, 0.03, 0.02],
                  list(np.full(10, 0.1))):
        p = np.asarray(masas, dtype=float)
        p = p / p.sum()
        theta = float(np.square(p).sum())
        m3 = float(np.power(p, 3).sum())
        for n in (200, 1000):
            c = rng.multinomial(n, p, size=20000).astype(float)
            tp = np.square(c / n).sum(axis=1)
            tu = (c * (c - 1.0)).sum(axis=1) / (n * (n - 1.0))
            out.append({
                "masas": [round(float(x), 4) for x in p],
                "n": n,
                "theta_verdadero": theta,
                "sesgo_plugin_medido": float(tp.mean() - theta),
                "sesgo_plugin_esperado_1_n": float((1.0 - theta) / n),
                "sesgo_unb_medido": float(tu.mean() - theta),
                "var_plugin_medida": float(tp.var(ddof=1)),
                "var_delta_formula": float((4.0 / n) * (m3 - theta ** 2)),
            })
    return {"replicas": 20000, "casos": out}


def main() -> None:
    os.chdir(ROOT)
    resultado = {
        "que": "intervalo de Simpson sobre las curvas de calibrate de los "
               "intentos 2, 3 y 4 de serie2_caso0",
        "texto": "docs/opus/TEXTO_PARA_CODE_14_REPO_CKM_simpson_y_piso_del_"
                 "colapso_27oct2026.md, punto 1",
        "conteos": "recomputados (el registro no los guarda); W reconstruida "
                   "desde el prefijo del corpus y verificada por sha",
        "verificacion_formulas": verificacion_formulas(),
        "curvas": [],
    }

    for nombre, traj, corpus in INTENTOS:
        Ws, fallidas = w_por_sha(ROOT / corpus)
        for cal in curvas_de(ROOT / traj):
            cond = cal["condiciones"]
            sha, n_runs, seed = cond["w_sha"], cond["n_runs"], cond["seed"]
            fila = {
                "intento": nombre,
                "w_sha": sha,
                "estado": cal["estado"],
                "causa": cond.get("causa"),
                "n_runs": n_runs,
                "seed": seed,
                "grilla_lambda": cond["grilla_lambda"],
                "puntos": [],
            }
            W = Ws.get(sha)
            if W is None:
                fila["recomputable"] = False
                fila["motivo"] = "W no recomputable desde el corpus"
                fila["w_no_recomputables"] = fallidas
                resultado["curvas"].append(fila)
                continue
            fila["recomputable"] = True
            fila["N"] = int(W.shape[0])

            W_col = extremo_colapso(W)
            est_por_lambda = {}
            for lam in cond["grilla_lambda"]:
                W_lam = W if lam == 0.0 else interpolar(W, W_col, lam)
                c = conteos_por_cuenca(W_lam, n_runs=n_runs, seed=seed)
                est_por_lambda[lam] = estimadores(c)

            n_eff0 = est_por_lambda[cond["grilla_lambda"][0]]["n_eff_plugin"]
            ic0 = est_por_lambda[cond["grilla_lambda"][0]]["n_eff_ic95"]

            registrada = {p["lambda"]: p for p in cond["curva"]}
            for lam in cond["grilla_lambda"]:
                e = est_por_lambda[lam]
                pt = {"lambda": lam, **e}
                pt.update(d_ckm_ic(e["n_eff_plugin"], e["n_eff_ic95"], n_eff0))
                reg = registrada.get(float(lam), {})
                pt["n_eff_registrado"] = reg.get("n_eff")
                pt["coincide_con_el_registro"] = (
                    reg.get("n_eff") is not None
                    and abs(reg["n_eff"] - e["n_eff_plugin"]) < 1e-9
                )
                # superposición con el intervalo de λ=0
                a, b = e["n_eff_ic95"]
                pt["ic_superpone_con_lambda0"] = not (b < ic0[0] or a > ic0[1])
                # N_eff insesgado con el mismo baseline insesgado
                fila["puntos"].append(pt)

            # la lectura del margen, con intervalo: d_colapso − d_sin_cambio
            d_ult = fila["puntos"][-1]
            fila["margen_registrado"] = cond.get("margen_separacion")
            fila["margen_recomputado"] = d_ult["d_ckm"]
            fila["margen_ic95"] = d_ult["d_ckm_ic95"]
            resultado["curvas"].append(fila)

    salida = ROOT / "experiments" / "simpson_en_las_curvas_resultado.json"
    tmp = salida.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(resultado, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.rename(salida)

    # ── tabla ──
    print("\n== verificación de las dos fórmulas (multinomial, 20000 réplicas) ==")
    print(f"{'masas':>26} {'n':>5} {'sesgo plugin':>13} {'(1-θ)/n':>10} "
          f"{'sesgo unb':>11} {'var medida':>12} {'var delta':>12}")
    for c in resultado["verificacion_formulas"]["casos"]:
        print(f"{str(c['masas']):>26} {c['n']:>5} {c['sesgo_plugin_medido']:>13.6f} "
              f"{c['sesgo_plugin_esperado_1_n']:>10.6f} {c['sesgo_unb_medido']:>11.6f} "
              f"{c['var_plugin_medida']:>12.6e} {c['var_delta_formula']:>12.6e}")

    print("\n== las curvas ==")
    for f in resultado["curvas"]:
        if not f.get("recomputable"):
            print(f"\n{f['intento']} {f['w_sha'][:8]} — NO recomputable: {f['motivo']}")
            continue
        print(f"\n{f['intento']} {f['w_sha'][:8]} estado={f['estado']} "
              f"causa={f['causa']} n_runs={f['n_runs']} seed={f['seed']} N={f['N']}")
        print(f"  {'λ':>5} {'k':>4} {'N_eff plug':>11} {'N_eff unb':>10} "
              f"{'IC95 N_eff':>21} {'=reg':>5} {'sup λ0':>7} {'d_ckm':>9} {'IC95 d_ckm':>21}")
        for p in f["puntos"]:
            ic = p["n_eff_ic95"]
            dic = p["d_ckm_ic95"]
            ics = f"[{ic[0]:.4f}, {ic[1]:.4f}]" if all(ic) else "—"
            dics = (f"[{dic[0]:.4f}, {dic[1]:.4f}]" if all(x is not None for x in dic)
                    else "—")
            unb = f"{p['n_eff_unb']:.4f}" if p["n_eff_unb"] else "—"
            d = f"{p['d_ckm']:.4f}" if p["d_ckm"] is not None else "—"
            print(f"  {p['lambda']:>5} {p['k_cuencas']:>4} {p['n_eff_plugin']:>11.4f} "
                  f"{unb:>10} {ics:>21} {str(p['coincide_con_el_registro']):>5} "
                  f"{str(p['ic_superpone_con_lambda0']):>7} {d:>9} {dics:>21}")
        print(f"  margen registrado {f['margen_registrado']} | recomputado "
              f"{f['margen_recomputado']} | IC95 {f['margen_ic95']}")
    print(f"\nsalida: {salida}")


if __name__ == "__main__":
    main()
