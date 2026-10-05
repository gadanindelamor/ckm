"""
conteo_vs_masa.py — Opus 5.5 (Cowork), 4 oct 2026. Driver fuera del repo.

Pregunta: sobre la MISMA W (ningún cambio de campo), ¿qué dicen el conteo de
atractores (D_ckm) y la masa de cuencas (d_masa_cuencas / N_eff) cuando sólo
cambian n_runs, seed y sampling_mode?  Verdad de terreno: el campo no cambió,
así que toda distancia distinta de 0 es del instrumento, no del campo.

PRE-REGISTRO (escrito antes de correr):
  - count_attractors crece con n_runs; D_ckm toma signo según n_runs vs el
    n_runs de A0 (negativo si n_runs > n_runs_A0).
  - N_eff converge; d_masa_cuencas queda cerca de 0 a n_runs >= 1000.
  - Si d_masa_cuencas no queda cerca de 0, eso es resultado y se reporta.
Código: services/ del repo en el commit que se registra en el log, sin tocar.
"""
import json, os, platform, subprocess, sys, time
import numpy as np

REPO = sys.argv[1]
OUT  = sys.argv[2]
sys.path.insert(0, os.path.join(REPO, "services"))
from ckm_landscape_config import CKMlandscapeConfig
import landscape_engine as E

src = os.path.join(REPO, "process/experiments/W_ckm_corpus_v2.json")
d = json.load(open(src)); W = np.array(d["W"], dtype=float)
sha = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

MODES   = {"uniform": {}, "weighted": {"weighted": True}, "boltzmann": {"boltzmann": True}}
N_RUNS  = [100, 300, 1000, 3000]
SEEDS   = [0, 1, 2, 3, 4]
A0_POLICY = {"n_runs": 1000, "seed": 0}   # DECLARADO por Opus para este experimento; la config todavía no tiene campo A0

aislados = int(np.sum(np.all(W == 0, axis=1)))
log = open(OUT, "w")
def w(rec): log.write(json.dumps(rec, allow_nan=True) + "\n"); log.flush()

w({"tipo": "cabecera",
   "repo_commit": sha, "W_fuente": "process/experiments/W_ckm_corpus_v2.json",
   "W_source_field": d.get("source"), "termap_version": d.get("termap_version"),
   "corpus_size": d.get("corpus_size"), "N": int(W.shape[0]),
   "W_min": float(W.min()), "W_max": float(W.max()), "aislados_W": aislados,
   "A0_policy": A0_POLICY,
   "python": sys.version.split()[0], "numpy": np.__version__,
   "platform": platform.platform(), "machine": platform.machine(),
   "donde": "contenedor cloud de Cowork (no el Codespace, no la PC de delamor)",
   "inicio": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
   "variables_no_consideradas": "todas las que no están en este log — declarado, no enumerable (delamor)"})

for mode, kw in MODES.items():
    cfg = CKMlandscapeConfig.from_W(W, theta_W=float("nan"), sampling_mode=mode, scale="log")
    w({"tipo": "config", "mode": mode, **cfg.to_dict(),
       "nota_theta_W": "NaN = no decidido (theta_W_formula abierta); este experimento no lo usa"})
    A0  = E.count_attractors(W, n_runs=A0_POLICY["n_runs"], seed=A0_POLICY["seed"], **kw)
    ne0 = E.n_eff(E.basin_masses(W, n_runs=A0_POLICY["n_runs"], seed=A0_POLICY["seed"], **kw))
    w({"tipo": "baseline", "mode": mode, "A0": A0, "N_eff0": ne0})
    for nr in N_RUNS:
        for s in SEEDS:
            t = time.time()
            A  = E.count_attractors(W, n_runs=nr, seed=s, **kw)
            m  = E.basin_masses(W, n_runs=nr, seed=s, **kw)
            ne = E.n_eff(m)
            w({"tipo": "medicion", "mode": mode, "n_runs": nr, "seed": s,
               "A": A, "D_ckm": E.d_ckm(A, A0),
               "n_orbitas": int(len(m)), "masa_top2": float(m[:2].sum()),
               "N_eff": ne, "d_masa_cuencas": E.d_masa_cuencas(ne, ne0),
               "seg": round(time.time() - t, 2)})
w({"tipo": "fin", "fin": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
