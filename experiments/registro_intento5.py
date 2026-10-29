"""
registro_intento5.py — los datos del REG del intento 5, de su propio estado

Texto para Code 21, punto 3 (Opus 5.5, 29 oct 2026). Junta en un solo JSON lo
que el REG borrador tiene que mostrar, leído del `state_dir` del vivo y del log
del driver. **Mide y registra. No interpreta**, y no toca `services/` ni
`iap_chatroom/`.

## De dónde sale cada cosa

- las calibraciones (el origen y cada rebuild), las evaluaciones de COCO con su
  `Threshold`, y la torsión por evaluación de Monitor: de
  `experiments/_state_S2-C0/monitor_trajectory.jsonl`;
- la línea `bootstrap` del origen: de `rebuild_decisions.jsonl`;
- por device, vueltas y errores: del log del driver
  (`experiments/serie2_caso0_intento5_log.json`); el `t` del último tick, de
  `channel_ticks.jsonl`;
- el N_eff0 **exacto** de la W calibrada: por enumeración de los 2^N estados
  bajo la medida del código, con `margen_exacto_14W` (texto 20, punto 1), que
  es el script que el texto 21 manda reusar si ya está. `F(N)` sale de
  `piso_del_colapso.forma_cerrada`.

## Lo que cuenta como "caerse en un default"

Se cuentan los lugares donde el registro dice que el valor **no** vino de una
medición: `source != "calibrate"` en el `Threshold` de COCO (y su `provenance`
`DECLARED`), y `estado != "calibrado"` en una calibración. No se cuenta un
default que además coincide con lo declarado: se cuenta **qué lugar** lo usó.

Salida: `experiments/registro_intento5_resultado.json` (escritura atómica).
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

import margen_exacto_14W as ME                                  # noqa: E402
import piso_del_colapso as PC                                   # noqa: E402

ESTADO = ROOT / "experiments/_state_S2-C0"
LOG = ROOT / "experiments/serie2_caso0_intento5_log.json"
SALIDA = ROOT / "experiments/registro_intento5_resultado.json"

CLAVES_TORSION = ("periodo_orbita", "cola_orbita", "n_aceptados",
                  "n_expulsados", "n_torsion", "Delta_r_sum",
                  "Delta_r_torsion_sum")


def main() -> None:
    traj = [json.loads(x) for x in open(ESTADO / "monitor_trajectory.jsonl",
                                        encoding="utf-8")]
    out: dict = {"que": "los datos del REG del intento 5 (texto 21, punto 3)",
                 "evaluaciones_de_monitor": len(traj)}

    # ── las calibraciones ───────────────────────────────────────────────
    vistas, cals = set(), []
    for i, d in enumerate(traj):
        c = d.get("panel", {}).get("coco", {}).get("calibration")
        if not c:
            continue
        cond = c["condiciones"]
        clave = (cond.get("w_sha"), cond.get("t"))
        if clave in vistas:
            continue
        vistas.add(clave)
        cals.append({
            "evaluacion": i,
            "estado": c["estado"], "causa": cond.get("causa"),
            "n_runs": cond.get("n_runs"), "seed": cond.get("seed"),
            "sampling_mode": cond.get("sampling_mode"),
            "parametros_declarados": c.get("parametros_declarados"),
            "declared_by": (c.get("parametros_declarados") or {})
            .get("declared_by"),
            "w_sha": c.get("w_sha"),
            "w_sha_live_at_calibration": c.get("w_sha_live_at_calibration"),
            "duration_s": c.get("duration_s"),
            "blocking": c.get("blocking"),
            "N": d["panel"]["coco"].get("N"),
            "n_eff0_muestreado": cond["curva"][0]["n_eff"],
            "n_eff_colapso_muestreado": cond["curva"][-1]["n_eff"],
            "margen_separacion": cond.get("margen_separacion"),
            "curva": cond.get("curva"),
            "valores": c.get("valores"),
        })
    for c in cals:
        N = c["N"]
        c["paridad_N"] = None if N is None else ("par" if N % 2 == 0
                                                 else "impar")
    out["calibraciones"] = cals

    # ── el N_eff exacto, de la W **calibrada** y de la final ───────────
    #
    # `corpus_state.json["W"]` es la W **final** del vivo, que no es la que se
    # calibró si hubo rebuild: acá la calibración es del origen (30 textos,
    # sha 66ea8d05) y el estado cierra con 40 textos (sha 6c16bb08). Así que
    # las W se **reconstruyen desde los prefijos del corpus y se verifican
    # contra su sha** con `simpson_en_las_curvas.w_por_sha`, que es lo mismo
    # que hizo el 14.1, y se reporta cada una por su sha. Medir la final y
    # llamarla "la calibrada" sería un error de identidad, no de número.
    import simpson_en_las_curvas as S
    from w_version import sha256_W

    st = json.load(open(ESTADO / "corpus_state.json", encoding="utf-8"))
    ws, fallidas = S.w_por_sha(ESTADO / "corpus_state.json")
    sha_final = sha256_W(np.array(st["W"], dtype=float))
    exactos = []
    for h in st.get("w_version_history", []):
        sha = h["sha256"]
        W = ws.get(sha)
        fila = {
            "w_sha": sha, "corpus_size": h["corpus_size"],
            "es_la_calibrada": bool(cals and sha == cals[0]["w_sha"]),
            "es_la_final_del_estado": sha == sha_final,
            "sha_verifica": sha in ws,
        }
        if W is None:
            fila["no_recomputable"] = True
            exactos.append(fila)
            continue
        N = W.shape[0]
        if N > 21:
            fila["N"] = N
            fila["sin_enumeracion"] = "N > 21"
            exactos.append(fila)
            continue
        cod = ME.n_eff_exacto(W, "codigo")
        art = ME.n_eff_exacto(W, "exacto")
        F = PC.forma_cerrada(N, "codigo")
        fila.update({
            "N": N, "paridad_N": "par" if N % 2 == 0 else "impar",
            "F(N)": F,
            "n_eff0_exacto_paso_del_codigo": cod["n_eff_exacto"],
            "n_eff0_exacto_aritmetica_exacta": art["n_eff_exacto"],
            "m_exacto_paso_del_codigo": ME.margen(cod["n_eff_exacto"], F),
            "m_exacto_aritmetica_exacta": ME.margen(art["n_eff_exacto"], F),
            "separa_exacto": bool(cod["n_eff_exacto"] > F),
            "n_eff0_muestreado_200_0": float(
                __import__("landscape_engine").count_attractors(
                    W, n_runs=200, seed=0)),
            "n_orbitas_con_masa": cod["n_orbitas_con_masa"],
            "periodo_max": cod["periodo_max"],
            "n_orbitas_autoconjugadas": cod["n_orbitas_autoconjugadas"],
            "masa_autoconjugada_alpha": cod["masa_autoconjugada"],
            "alpha_menor_o_igual_2_tercios":
                bool(cod["masa_autoconjugada"] <= 2.0 / 3.0),
            "verificacion_contra_relax_orbit":
                ME.verificar_contra_relax_orbit(W, "codigo"),
        })
        exactos.append(fila)
    out["n_eff_exacto_por_W"] = exactos
    out["W_no_recomputables"] = fallidas
    exacto = next((e for e in exactos if e.get("es_la_calibrada")), None)
    out["la_W_calibrada"] = exacto

    # ── COCO: el Threshold de cada evaluación ──────────────────────────
    ev = []
    for i, d in enumerate(traj):
        co = d["panel"]["coco"]
        th = co.get("thresholds") or {}
        org = th.get("origen") or {}
        ev.append({
            "evaluacion": i,
            "n_evaluations_received": co.get("n_evaluations_received"),
            "w_version_id_coco": co.get("w_version_id"),
            "w_version_id_monitor": co.get("w_version_id_monitor"),
            "w_matches": co.get("w_matches"),
            "D_CKM_THRESHOLD": th.get("D_CKM_THRESHOLD"),
            "FRAC_REC_MIN": th.get("FRAC_REC_MIN"),
            "source": th.get("source"), "calibrated": th.get("calibrated"),
            "causa": th.get("causa"),
            "provenance_d_ckm": (org.get("d_ckm_threshold") or {})
            .get("provenance"),
            "source_d_ckm": (org.get("d_ckm_threshold") or {}).get("source"),
            "provenance_frac_rec": (org.get("frac_rec_min") or {})
            .get("provenance"),
            "w_sha_del_registro": th.get("w_sha_del_registro"),
            "w_sha_match": th.get("w_sha_match"),
            "el_w_sha_del_registro_es_el_de_la_W_juzgada":
                th.get("w_sha_del_registro") == co.get("w_version_id"),
            "triggers": co.get("triggers"),
            "D_ckm": d["panel"].get("D_ckm"),
            "N_eff": d["panel"].get("N_eff"),
        })
    out["evaluaciones_de_coco"] = ev

    # ── la torsión ─────────────────────────────────────────────────────
    tor, ausentes = [], {k: 0 for k in CLAVES_TORSION}
    for i, d in enumerate(traj):
        p = d["panel"]
        fila = {"evaluacion": i, "device_id": d.get("device_id"),
                "N": p.get("condicion_W", {}).get("N")}
        fila["paridad_N"] = (None if fila["N"] is None else
                             ("par" if fila["N"] % 2 == 0 else "impar"))
        for k in CLAVES_TORSION:
            if k in p:
                fila[k] = p[k]
            else:
                fila[k] = None
                ausentes[k] += 1
        fila["pares_torsion"] = p.get("pares_torsion")
        tor.append(fila)
    out["torsion"] = {
        "claves_ausentes": ausentes,
        "con_periodo_2": sum(1 for f in tor if f["periodo_orbita"] == 2),
        "con_torsion_mayor_que_0": sum(1 for f in tor
                                       if (f["n_torsion"] or 0) > 0),
        "suma_n_aceptados": sum(f["n_aceptados"] or 0 for f in tor),
        "suma_n_expulsados": sum(f["n_expulsados"] or 0 for f in tor),
        "suma_n_torsion": sum(f["n_torsion"] or 0 for f in tor),
        "suma_Delta_r": sum(f["Delta_r_sum"] or 0 for f in tor),
        "suma_Delta_r_torsion": sum(f["Delta_r_torsion_sum"] or 0
                                    for f in tor),
        "filas": tor,
    }

    # ── el bootstrap del origen ────────────────────────────────────────
    dec = [json.loads(x) for x in open(ESTADO / "rebuild_decisions.jsonl",
                                       encoding="utf-8")]
    out["rebuild_decisions"] = {
        "lineas": len(dec),
        "bootstrap": [d for d in dec
                      if "bootstrap" in json.dumps(d, ensure_ascii=False)],
        "causas": sorted({str(d.get("causa")) for d in dec}),
        "con_rebuild_true": sum(1 for d in dec if d.get("rebuild") is True),
    }

    # ── los defaults ───────────────────────────────────────────────────
    out["defaults"] = {
        "evaluaciones_de_coco_con_source_default":
            sum(1 for e in ev if e["source"] == "default"),
        "evaluaciones_de_coco_con_provenance_DECLARED":
            sum(1 for e in ev if e["provenance_d_ckm"] == "DECLARED"),
        "calibraciones_no_calibradas":
            sum(1 for c in cals if c["estado"] != "calibrado"),
        "donde": sorted({e["source_d_ckm"] for e in ev if e["source_d_ckm"]}),
        "valores": sorted({(e["D_CKM_THRESHOLD"], e["FRAC_REC_MIN"])
                           for e in ev}),
    }

    # ── los devices ────────────────────────────────────────────────────
    log = json.load(open(LOG, encoding="utf-8"))
    ticks = [json.loads(x) for x in open(ESTADO / "channel_ticks.jsonl",
                                         encoding="utf-8")]
    ultimo_tick = {}
    for t in ticks:
        did = t.get("device_id") or t.get("device")
        if did:
            ultimo_tick[did] = t.get("t")
    out["devices"] = {"del_log_del_driver": log.get("por_device",
                                                    log.get("devices")),
                      "t_del_ultimo_tick": ultimo_tick,
                      "ticks": len(ticks)}
    out["del_log_del_driver"] = {
        k: log.get(k) for k in ("repo_commit", "declarado", "segundos_reales",
                                "objetivo_declarado_como_sesgo", "orden",
                                "modo", "preflight")}

    tmp = SALIDA.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    os.replace(tmp, SALIDA)
    print(f"-> {SALIDA}")
    print(f"calibraciones: {len(cals)} · evaluaciones de COCO: {len(ev)} · "
          f"torsión>0: {out['torsion']['con_torsion_mayor_que_0']} · "
          f"período 2: {out['torsion']['con_periodo_2']}")
    if exacto:
        print(f"la W calibrada: N_eff0 exacto {exacto['n_eff0_exacto_paso_del_codigo']:.6f} · "
              f"F({exacto['N']}) {exacto['F(N)']:.6f} · m exacto "
              f"{exacto['m_exacto_paso_del_codigo']:+.6f} · separa "
              f"{exacto['separa_exacto']} · α "
              f"{exacto['masa_autoconjugada_alpha']:.6f}")


if __name__ == "__main__":
    main()
