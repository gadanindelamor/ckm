"""
driver_cp1b_escala_delta_r.py — CP1b de `TASK_iap_serie2_caso0_v1`

**Qué mide:** cuánto mueve a D_ckm, **dentro de un ciclo**, la escala con la que
Δ_r entra a W_eff. Dentro de un ciclo W no cambia, así que la escala es lo
único que mueve el número.

**Las cuatro combinaciones** (las dos que el código usa hoy, más las dos
alternativas que lista la TASK):

    A  W + (Δ_r / max Δ_r) · media(W > 0)     ← Monitor, `_combine_W_Delta`
    B  W + Δ_r   (crudo)                      ← COCO, `observe`
    C  W + (Δ_r / max Δ_r) · media(|W| ≠ 0)   ← alternativa
    D  W + (Δ_r / max Δ_r)                    ← alternativa, sin factor de W

**No elige escala.** Mide, reporta y la elige delamor.

**No toca `services/`:** importa `landscape_engine` y `corpus_service` para
usarlos, y reimplementa **sólo las cuatro escalas** acá, que es lo que se está
comparando. La A es copia literal de `monitor_service._combine_W_Delta`.

**El conjunto de mensajes es el del CP1**, declarado y con su sha: los 8 textos
de `tests/test_serie2_caso0_cp1.py`, en ciclo hasta 45 mensajes, alternando dos
devices — la misma secuencia con la que el CP1 midió N = 18.

Correr:
    PYTHONPATH=/workspaces/ckm python3 experiments/driver_cp1b_escala_delta_r.py [salida.json]
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

from corpus_service import CorpusService          # noqa: E402
from landscape_engine import basin_masses, n_eff   # noqa: E402
from node_extractor import MIN_DF                  # noqa: E402
from calibrate import calibrate                    # noqa: E402

# ── el conjunto de mensajes del CP1, declarado ──────────────────────────────
TEXTOS = [
    "gun control reduces violence and saves lives in urban areas",
    "the second amendment protects the right to bear arms",
    "background checks do not stop criminals from getting weapons",
    "assault weapons bans reduce mass shootings and gun violence",
    "gun rights are constitutional rights and should not be restricted",
    "mental health is the real cause of gun violence not access to arms",
    "urban areas report more gun violence than rural areas",
    "constitutional rights include the right to bear arms in the home",
]
N_MENSAJES = 45
TOP_K = 20              # los parámetros declarados de la Serie 2
N_RUNS = 1000           # donde N_eff converge (§4.3.1)
SEED_CONTEO = 0
SEED_RECHAZOS = 7
N_RECHAZOS = 10
N_CORRIDAS_CALIBRATE = 7


def secuencia_de_mensajes() -> list[tuple[str, str]]:
    """(device_id, texto) × 45, igual que el CP1: dos devices alternados."""
    return [("d1" if i % 2 else "d2", TEXTOS[i % len(TEXTOS)])
            for i in range(N_MENSAJES)]


def sha_de_la_secuencia(seq) -> str:
    crudo = json.dumps(seq, ensure_ascii=False, sort_keys=False)
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()


# ── las cuatro escalas ──────────────────────────────────────────────────────

def escala_A(W, D):
    """Monitor, hoy. Copia literal de `_combine_W_Delta`."""
    dmax = D.max()
    if dmax == 0:
        return W
    pos = W[W > 0]
    factor = pos.mean() if len(pos) else 1.0
    return W + (D / dmax) * factor


def escala_B(W, D):
    """COCO, hoy. `W + Δ` sin normalizar nada."""
    return W + D


def escala_C(W, D):
    """Alternativa: el factor es la media de |W| sobre los no nulos."""
    dmax = D.max()
    if dmax == 0:
        return W
    nz = np.abs(W[W != 0])
    factor = nz.mean() if len(nz) else 1.0
    return W + (D / dmax) * factor


def escala_D(W, D):
    """Alternativa: normalizado al máximo y sin factor de W."""
    dmax = D.max()
    if dmax == 0:
        return W
    return W + D / dmax


ESCALAS = {
    "A_monitor_media_W_pos": escala_A,
    "B_coco_crudo": escala_B,
    "C_media_abs_W_no_nula": escala_C,
    "D_sin_factor_de_W": escala_D,
}


def n_eff_de(W_eff) -> float:
    masas = basin_masses(W_eff, n_runs=N_RUNS, seed=SEED_CONTEO)
    return float(n_eff(masas))


def d_ckm(n_t: float, n_0: float):
    """La forma canónica. None si el baseline no sirve (≤ 1)."""
    if n_0 is None or n_0 <= 1 or n_t <= 0:
        return None
    return 1.0 - (np.log(n_t) / np.log(n_0))


def pares_de_rechazo(W, k: int, seed: int):
    """
    La secuencia fija de rechazos: `k` pares, **mitad sobre pares ya acoplados
    y mitad sobre pares nulos**, en orden alternado.

    Es la decisión del punto 7 de la predicción: si todos los rechazos cayeran
    sobre pares ya acoplados, la secuencia podría no mover N_eff y lo que se
    mediría sería la secuencia, no la escala.
    """
    rng = np.random.default_rng(seed)
    N = W.shape[0]
    iu = np.triu_indices(N, k=1)
    no_nulos = [(int(i), int(j)) for i, j in zip(*iu) if W[i, j] != 0]
    nulos = [(int(i), int(j)) for i, j in zip(*iu) if W[i, j] == 0]
    rng.shuffle(no_nulos)
    rng.shuffle(nulos)
    salida = []
    for t in range(k):
        fuente = no_nulos if t % 2 == 0 else nulos
        if not fuente:
            fuente = no_nulos or nulos
        salida.append(fuente.pop())
    return salida


def main() -> None:
    salida_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        RAIZ / "experiments/driver_cp1b_escala_delta_r_resultado.json")

    seq = secuencia_de_mensajes()
    sha_seq = sha_de_la_secuencia(seq)

    # La W del canal, con los parámetros declarados de la Serie 2. El corpus
    # va a un temporal: nada del estado vivo se toca.
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    corpus = CorpusService(storage_path=str(tmp / "corpus.json"),
                           min_texts=len(seq), top_k=TOP_K)
    corpus.ingest([t for _, t in seq])
    W = corpus.get_W()
    assert W is not None, "sin W no hay nada que medir"
    N = W.shape[0]

    distintos = pares_de_rechazo(W, N_RECHAZOS, SEED_RECHAZOS)
    # **Dos secuencias, y la segunda es la que importa para separar B de D.**
    # Con un rechazo por par, `max Δ_r = 1` **siempre**, así que D —que divide
    # por el máximo— queda idéntica a B. Δ_r de verdad **acumula sobre los
    # mismos pares** (`Delta_r[i,j] += 1` por evaluación), así que la segunda
    # secuencia repite 3 pares hasta que el máximo llega a 4.
    secuencias = {
        "sin_repeticion": distintos,
        "con_repeticion": [distintos[i % 3] for i in range(N_RECHAZOS)],
    }

    base, curvas = {}, {}
    for etiqueta, rechazos in secuencias.items():
        D = np.zeros((N, N))
        base[etiqueta] = {nombre: n_eff_de(f(W, D))
                          for nombre, f in ESCALAS.items()}
        curvas[etiqueta] = {nombre: [] for nombre in ESCALAS}
        for paso, (i, j) in enumerate(rechazos, start=1):
            D[i, j] += 1
            D[j, i] += 1
            for nombre, f in ESCALAS.items():
                W_eff = f(W, D)
                ne = n_eff_de(W_eff)
                curvas[etiqueta][nombre].append({
                    "paso": paso,
                    "par": [i, j],
                    "W_ij": float(W[i, j]),
                    "Delta_max": float(D.max()),
                    "N_eff": round(ne, 4),
                    "D_ckm": (lambda d: round(d, 6) if d is not None else None)(
                        d_ckm(ne, base[etiqueta][nombre])),
                    "max_abs_W_eff": round(float(np.abs(W_eff).max()), 6),
                })
    rechazos = secuencias

    # ── cuánto tarda `calibrate` en el salto ───────────────────────────────
    # Dos cosas, porque el `duration_s` del panel cubre las dos: la extracción
    # de la candidata y la calibración.
    t_candidata, t_calibrate = [], []
    for _ in range(N_CORRIDAS_CALIBRATE):
        t0 = time.monotonic()
        Wc = corpus.candidate_W()
        t1 = time.monotonic()
        reg = calibrate(Wc, w_sha="cp1b")
        t2 = time.monotonic()
        t_candidata.append(t1 - t0)
        t_calibrate.append(t2 - t1)

    def resumen(xs):
        xs = sorted(xs)
        return {"mediana": round(xs[len(xs) // 2], 4),
                "min": round(xs[0], 4), "max": round(xs[-1], 4),
                "n": len(xs)}

    resultado = {
        "task": "TASK_iap_serie2_caso0_v1 / CP1b",
        "serie": "S2", "caso": "S2-C0",
        "condiciones": {
            "mensajes": {"n": len(seq), "sha256": sha_seq,
                         "fuente": "TEXTOS de tests/test_serie2_caso0_cp1.py, "
                                   "en ciclo, dos devices alternados"},
            "extraccion": {"top_k": TOP_K, "min_df": MIN_DF, "ngram_max": 2},
            "W": {"N": N, "sha256_W": hashlib.sha256(W.tobytes()).hexdigest(),
                  "media_W_pos": round(float(W[W > 0].mean()), 6),
                  "media_abs_W_no_nula": round(
                      float(np.abs(W[W != 0]).mean()), 6),
                  "max_abs_W": round(float(np.abs(W).max()), 6),
                  "frac_negativos": round(
                      float((W < 0).sum() / (W.size - N)), 4)},
            "conteo": {"n_runs": N_RUNS, "seed": SEED_CONTEO,
                       "forma_D_ckm": "1 - ln N_eff / ln N_eff_0"},
            "rechazos": {"n_pasos": N_RECHAZOS, "seed": SEED_RECHAZOS,
                         "secuencias": rechazos,
                         "criterio": ("sin_repeticion: alternados no nulo / "
                                      "nulo, un rechazo por par (max Delta = 1 "
                                      "siempre). con_repeticion: 3 pares "
                                      "repetidos, max Delta llega a 4 -- es lo "
                                      "que Delta_r hace de verdad")},
        },
        "baselines_N_eff": {e: {k: round(v, 4) for k, v in b.items()}
                            for e, b in base.items()},
        "curvas": curvas,
        "calibrate_en_el_salto": {
            "extraccion_candidata_s": resumen(t_candidata),
            "calibrate_s": resumen(t_calibrate),
            "total_bloqueante_s": resumen(
                [a + b for a, b in zip(t_candidata, t_calibrate)]),
            "condiciones": reg["condiciones"],
            "estado_ultima": reg["estado"],
            "valores_ultima": reg.get("valores"),
        },
    }

    salida_path.write_text(json.dumps(resultado, indent=2, ensure_ascii=False))
    print(f"[cp1b] escrito en {salida_path}")
    print(f"[cp1b] N={N}  sha_mensajes={sha_seq[:12]}  "
          f"media(W>0)={resultado['condiciones']['W']['media_W_pos']}  "
          f"media(|W|≠0)={resultado['condiciones']['W']['media_abs_W_no_nula']}")
    for etiqueta in curvas:
        print(f"[cp1b] --- {etiqueta} ---")
        for nombre in ESCALAS:
            ds = [p["D_ckm"] for p in curvas[etiqueta][nombre]]
            print(f"[cp1b] {nombre:24s} base N_eff="
                  f"{base[etiqueta][nombre]:7.3f}  D_ckm: "
                  + " ".join(f"{d:+.4f}" if d is not None else "None" for d in ds))
    print(f"[cp1b] calibrate: {resultado['calibrate_en_el_salto']}")


if __name__ == "__main__":
    main()
