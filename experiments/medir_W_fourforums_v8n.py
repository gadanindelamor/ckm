"""
medir_W_fourforums_v8n.py — mide con el instrumento existente las ocho W de
fourforums producidas en ckmdatasets por build_W_v8n.py (TAREA 7, delamor,
23 oct 2026).

Qué son las W: votos humanos de acuerdo/desacuerdo del IAC (fourforums, gun
control). El signo lo pusieron los anotadores. Cada archivo trae su
extracción declarada (clave "declaration", O1–O7). N = 146, nodos a000…a145.
  W_obs, W_sign, W_presence, W_null_s1..s5 (signos de aristas no nulas
  permutados; mismos 297 −, 75 +, 11 en 0).
Son un derivado del IAC: viven en process/datasets_private/ (fuera de git),
igual que el JSON de resultados que escribe este script.

Qué mide, por W y por n_runs ∈ {1000, 5000, 20000}:
  - N_eff = n_eff(basin_masses(W, n_runs, seed))
  - órbitas distintas
  - fracción de período 2: por masa (fracción de muestras que caen en
    órbitas de período 2) y por conteo (fracción de órbitas distintas)
  - masa de la órbita mayor
  - beta_c_landscape(W) (aritmética: no depende de n_runs ni de seed)

Instrumento: services/landscape_engine.py, sin tocar. basin_masses no
devuelve el período de cada órbita, así que el script repite su muestreo
con las mismas piezas que usa basin_masses en modo por defecto (uniforme,
sin weighted ni boltzmann): rng = default_rng(seed), sample_s0(rng, N, None),
relax_orbit(s0, W). Las masas así obtenidas se comparan con basin_masses
(mismo seed, mismo n_runs) y deben ser idénticas; si no, el script se
detiene.

Misma seed para las ocho W y para los tres n_runs. Consecuencia declarada:
con la misma seed las muestras de n_runs=1000 son un prefijo de las de 5000,
y éstas de las de 20000 (sample_s0 consume el rng igual en cada llamada).
La convergencia que se reporta es la de muestras anidadas.

Antes de medir verifica el sha256 de cada W contra manifest_v8n.json y se
detiene si alguno no coincide.

No interpreta. Mide y escribe.

Uso:
    python experiments/medir_W_fourforums_v8n.py
    python experiments/medir_W_fourforums_v8n.py --n_runs 1000 5000 20000 --seed 20261023
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))

from landscape_engine import (  # noqa: E402
    basin_masses, beta_c_landscape, n_eff, relax_orbit, sample_s0,
)

DIR_DEFAULT = REPO / "process" / "datasets_private" / "fourforums_W_v8n"
ORDEN = ["W_obs", "W_sign", "W_presence",
         "W_null_s1", "W_null_s2", "W_null_s3", "W_null_s4", "W_null_s5"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def medir(W: np.ndarray, n_runs: int, seed: int) -> dict:
    """Muestreo de basin_masses (modo por defecto) con el período de cada órbita."""
    N = W.shape[0]
    rng = np.random.default_rng(seed)
    cuenta: dict = {}
    periodo: dict = {}
    sin_cerrar = 0
    for _ in range(n_runs):
        s0 = sample_s0(rng, N, None)
        orbita, per, _, _ = relax_orbit(s0, W)
        cuenta[orbita] = cuenta.get(orbita, 0) + 1
        periodo[orbita] = per
        sin_cerrar += (per == 0)
    masas = np.array(sorted(cuenta.values(), reverse=True), dtype=float) / n_runs

    ref = basin_masses(W, n_runs=n_runs, seed=seed)
    if not np.array_equal(masas, ref):
        raise SystemExit(f"masas != basin_masses (n_runs={n_runs}, seed={seed}): se detiene")

    pers = np.array(list(periodo.values()))
    cnt = np.array([cuenta[o] for o in periodo])
    return {
        "n_runs": n_runs,
        "seed": seed,
        "N_eff": n_eff(ref),
        "orbitas_distintas": int(len(cuenta)),
        "masa_orbita_mayor": float(ref[0]),
        "frac_periodo2_por_masa": float(cnt[pers == 2].sum() / n_runs),
        "frac_periodo2_por_conteo": float((pers == 2).mean()),
        "periodos_presentes": sorted({int(p) for p in pers}),
        "runs_sin_cerrar_orbita": int(sin_cerrar),
        "masas_igual_basin_masses": True,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(DIR_DEFAULT))
    ap.add_argument("--n_runs", type=int, nargs="+", default=[1000, 5000, 20000])
    ap.add_argument("--seed", type=int, default=20261023)
    ap.add_argument("--out", default=None, help="default: <dir>/resultados_medir_W_fourforums_v8n.json")
    args = ap.parse_args()

    d = Path(args.dir)
    manifest = json.loads((d / "manifest_v8n.json").read_text())
    shas = {}
    for name in ORDEN:
        e = manifest["W"][name]
        h = sha256(d / e["file"])
        if h != e["sha256"]:
            raise SystemExit(f"sha256 no coincide para {name}: {h} != {e['sha256']}: se detiene")
        shas[name] = h
    print(f"sha256 verificados: {len(shas)}/{len(ORDEN)}")

    try:
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                              capture_output=True, text=True).stdout.strip()
    except OSError:
        head = None

    res = {
        "producer": "experiments/medir_W_fourforums_v8n.py",
        "script_sha256": sha256(Path(__file__)),
        "git_head": head,
        "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "muestreo": "basin_masses por defecto: uniforme, weighted=False, boltzmann=False, max_iter=200",
        "seed": args.seed,
        "n_runs": args.n_runs,
        "manifest_sha256": sha256(d / "manifest_v8n.json"),
        "W": {},
    }
    for name in ORDEN:
        obj = json.loads((d / manifest["W"][name]["file"]).read_text())
        W = np.array(obj["W"], dtype=float)
        r = {"sha256": shas[name], "N": int(W.shape[0]),
             "beta_c_landscape": beta_c_landscape(W), "por_n_runs": []}
        for n in args.n_runs:
            t0 = time.time()
            m = medir(W, n, args.seed)
            m["segundos"] = round(time.time() - t0, 2)
            r["por_n_runs"].append(m)
            print(f"{name:11s} n_runs={n:6d}  N_eff={m['N_eff']:10.3f}  orbitas={m['orbitas_distintas']:6d}  "
                  f"p2_masa={m['frac_periodo2_por_masa']:.4f}  p2_conteo={m['frac_periodo2_por_conteo']:.4f}  "
                  f"masa_max={m['masa_orbita_mayor']:.4f}  periodos={m['periodos_presentes']}  "
                  f"sin_cerrar={m['runs_sin_cerrar_orbita']}  ({m['segundos']}s)", flush=True)
        print(f"{name:11s} beta_c_landscape={r['beta_c_landscape']}")
        res["W"][name] = r

    out = Path(args.out) if args.out else d / "resultados_medir_W_fourforums_v8n.json"
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"escrito: {out}  sha256={sha256(out)}")


if __name__ == "__main__":
    main()
