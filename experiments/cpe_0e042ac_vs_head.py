"""
cpe_0e042ac_vs_head.py — el CP-E en 0e042ac contra HEAD, celda por celda

Texto para Code 20, punto 3 (Opus 5.5, 29 oct 2026; respalda el Pendiente R2 del
paper v33: el "15.52 → 5.27" de §4.3.2). **Mide y registra**, y no toca
`services/` ni `iap_chatroom/`.

## Qué hace

Lee las **dos salidas completas** de `experiments/driver_cpe_rango_neff.py`,
corrido **sin ningún cambio** en los dos commits, y las compara celda por
celda:

- `driver_cpe_rango_neff_salida_0e042ac.txt` — corrido en un `git worktree`
  separado, fuera del repo, sobre `0e042ac` (14 oct 2026), el commit del CP-E.
- `driver_cpe_rango_neff_salida_HEAD.txt` — corrido en el repo, en HEAD.

El driver es **el mismo archivo** en los dos commits (`git diff 0e042ac HEAD --
experiments/driver_cpe_rango_neff.py` es vacío), y **corre en HEAD sin
adaptaciones**: la copia `_head.py` que el texto 20 preveía "si el driver no
corre igual por cambios de API" no hizo falta y no se escribió.

## Condiciones

- El driver declara lo suyo y se respeta: `n_runs = 1000` y las **seeds 0–9**.
  Es una **reproducción**, no una medición nueva, y por eso no se le ponen los
  defaults de hoy (200 / 0): el 1000 y las diez seeds son parte de lo que se
  reproduce. Así lo declara también cada fila de la salida.
- Los **tres corpus no cambiaron** entre los dos commits: verificado con
  `git diff --stat 0e042ac HEAD --` sobre los tres archivos, vacío. Lo que
  cambió es `services/node_extractor.py` (+93 líneas) y
  `services/corpus_service.py` (+223).
- Lo que se compara es texto parseado de las dos salidas, no una corrida nueva:
  las salidas quedan en `experiments/` como la evidencia.

Salida: `experiments/cpe_0e042ac_vs_head_resultado.json` (escritura atómica) y
la tabla por stdout.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "cpe_0e042ac_vs_head_resultado.json"
FUENTES = {
    "0e042ac": AQUI / "driver_cpe_rango_neff_salida_0e042ac.txt",
    "HEAD": AQUI / "driver_cpe_rango_neff_salida_HEAD.txt",
}

RE_CORPUS = re.compile(r"^## (\w+) — (\d+) textos")
RE_MED = re.compile(
    r"N=\s*(\d+)\s+N_eff=\s*([\d.]+)\s+sd=\s*([\d.]+)\s+\[([\d.]+), ([\d.]+)\]")
RE_SIN_W = re.compile(r"sin W")
RE_TABLA = re.compile(
    r"^(\w+)\s+([\d.]+|nan)\s+([\d.]+|nan)\s+([\d.]+|nan)\s+"
    r"([\d.]+|nan)\s+([\d.]+|nan)\s*$")


def _celda(linea: str) -> dict | None:
    m = RE_MED.search(linea)
    if m:
        return {"N": int(m.group(1)), "n_eff": float(m.group(2)),
                "sd": float(m.group(3)),
                "min": float(m.group(4)), "max": float(m.group(5))}
    if RE_SIN_W.search(linea):
        return {"N": 0, "n_eff": None, "sd": None, "min": None, "max": None}
    return None


def parsear(path: Path) -> dict:
    """
    Las celdas de una salida del driver, por corpus y por perilla.

    Se apoya en el formato que imprime `driver_cpe_rango_neff.main()`: una
    sección `## <corpus>` por corpus, la línea `base`, los bloques `top_k:`,
    `pool`, `stopwords:` y la línea `un texto más`, más la tabla final de
    rangos relativos. Si el formato cambia, esto **no adivina**: la celda queda
    en None y se ve en el JSON.
    """
    out: dict = {"corpus": {}, "tabla_de_rangos": {}}
    corpus = None
    seccion = None
    for linea in path.read_text(encoding="utf-8").splitlines():
        m = RE_CORPUS.match(linea)
        if m:
            corpus = m.group(1)
            out["corpus"][corpus] = {"n_textos": int(m.group(2)),
                                     "base": None, "top_k": {}, "pool": {},
                                     "sw": {}, "extra": None,
                                     "texto_extra": None}
            seccion = None
            continue
        if corpus is None:
            continue
        d = out["corpus"][corpus]
        if "base (top_k=" in linea:
            d["base"] = _celda(linea)
        elif linea.strip() == "top_k:":
            seccion = "top_k"
        elif re.search(r"pool x(\d+)", linea):
            # antes del encabezado "pool (multiplicador...)": las dos líneas
            # empiezan con "pool" y el encabezado se comía las celdas
            d["pool"][int(re.search(r"pool x(\d+)", linea).group(1))] = \
                _celda(linea)
        elif linea.strip().startswith("pool"):
            seccion = "pool"
        elif linea.strip() == "stopwords:":
            seccion = "sw"
        elif "un texto más" in linea:
            d["extra"] = _celda(linea)
            seccion = None
        elif "el texto:" in linea:
            d["texto_extra"] = linea.split("el texto:", 1)[1].strip()
        elif seccion == "top_k" and "top_k=" in linea:
            k = int(re.search(r"top_k=\s*(\d+)", linea).group(1))
            d["top_k"][k] = _celda(linea)
        elif seccion == "pool" and re.search(r"pool x(\d+)", linea):
            m2 = re.search(r"pool x(\d+)", linea)
            d["pool"][int(m2.group(1))] = _celda(linea)
        elif seccion == "sw" and "|S|=" in linea:
            n = int(re.search(r"\|S\|=\s*(\d+)", linea).group(1))
            d["sw"][n] = _celda(linea)
        else:
            m3 = RE_TABLA.match(linea.strip())
            if m3 and m3.group(1) in out["corpus"]:
                out["tabla_de_rangos"][m3.group(1)] = {
                    "seed": float(m3.group(2)), "top_k": float(m3.group(3)),
                    "pool": float(m3.group(4)), "stopwords": float(m3.group(5)),
                    "mas_un_texto": float(m3.group(6))}
    return out


def _dif(a: dict | None, b: dict | None) -> dict:
    """La celda de 0e042ac contra la de HEAD, con la diferencia relativa."""
    if a is None or b is None:
        return {"falta_una_de_las_dos": True}
    fila = {"N_0e042ac": a["N"], "N_HEAD": b["N"],
            "n_eff_0e042ac": a["n_eff"], "n_eff_HEAD": b["n_eff"],
            "sd_0e042ac": a["sd"], "sd_HEAD": b["sd"]}
    if a["n_eff"] and b["n_eff"] is not None:
        fila["dif_relativa"] = (b["n_eff"] - a["n_eff"]) / a["n_eff"]
        fila["cambia_N"] = a["N"] != b["N"]
        # ¿se superponen los rangos de las 10 seeds?
        fila["rangos_se_superponen"] = not (a["max"] < b["min"]
                                            or b["max"] < a["min"])
    return fila


def main() -> None:
    faltan = [k for k, p in FUENTES.items() if not p.exists()]
    if faltan:
        raise SystemExit(f"faltan las salidas: {faltan}")
    viejo, nuevo = parsear(FUENTES["0e042ac"]), parsear(FUENTES["HEAD"])

    salida = {
        "que": "el CP-E en 0e042ac contra HEAD, celda por celda (texto 20, "
               "punto 3)",
        "declarado_por_el_driver": {"n_runs": 1000, "seeds": "0..9",
                                    "razon": "es una reproduccion del CP-E, "
                                             "no una medicion nueva"},
        "el_driver_es_el_mismo_archivo_en_los_dos_commits": True,
        "corrio_en_HEAD_sin_adaptaciones": True,
        "los_tres_corpus_no_cambiaron": True,
        "0e042ac": viejo, "HEAD": nuevo, "celda_por_celda": {},
    }

    print("CP-E: 0e042ac (14 oct) contra HEAD — n_runs=1000, seeds 0..9\n")
    print(f"{'corpus':<6}{'celda':<16}{'N vie':>6}{'N new':>6}"
          f"{'N_eff 0e042ac':>15}{'N_eff HEAD':>12}{'dif rel':>10}"
          f"{'solapan':>9}")
    for corpus in viejo["corpus"]:
        a, b = viejo["corpus"][corpus], nuevo["corpus"].get(corpus, {})
        celdas = {"base": (a["base"], b.get("base")),
                  "extra_+1_texto": (a["extra"], b.get("extra"))}
        for k in sorted(a["top_k"]):
            celdas[f"top_k={k}"] = (a["top_k"][k], b.get("top_k", {}).get(k))
        for m in sorted(a["pool"]):
            celdas[f"pool_x{m}"] = (a["pool"][m], b.get("pool", {}).get(m))
        for n in sorted(a["sw"]):
            celdas[f"sw_{n}"] = (a["sw"][n], b.get("sw", {}).get(n))
        salida["celda_por_celda"][corpus] = {
            nombre: _dif(x, y) for nombre, (x, y) in celdas.items()}
        salida["celda_por_celda"][corpus]["texto_extra_igual"] = (
            a["texto_extra"] == b.get("texto_extra"))
        for nombre, (x, y) in celdas.items():
            f = salida["celda_por_celda"][corpus][nombre]
            if "dif_relativa" not in f:
                print(f"{corpus:<6}{nombre:<16}{'—':>6}{'—':>6}"
                      f"{'(sin W en alguna)':>15}")
                continue
            print(f"{corpus:<6}{nombre:<16}{f['N_0e042ac']:>6}"
                  f"{f['N_HEAD']:>6}{f['n_eff_0e042ac']:>15.3f}"
                  f"{f['n_eff_HEAD']:>12.3f}{f['dif_relativa']:>+10.3f}"
                  f"{'si' if f['rangos_se_superponen'] else 'NO':>9}")

    # los tres números que cita el paper (§4.3.2)
    salida["los_numeros_del_paper"] = {
        "A24_base_15.52": {
            "0e042ac": viejo["corpus"]["A24"]["base"],
            "HEAD": nuevo["corpus"]["A24"]["base"]},
        "A24_mas_un_texto_5.27": {
            "0e042ac": viejo["corpus"]["A24"]["extra"],
            "HEAD": nuevo["corpus"]["A24"]["extra"]},
        "D12_base_5.27": {
            "0e042ac": viejo["corpus"]["D12"]["base"],
            "HEAD": nuevo["corpus"]["D12"]["base"]},
        "E7_base_10.10": {
            "0e042ac": viejo["corpus"]["E7"]["base"],
            "HEAD": nuevo["corpus"]["E7"]["base"]},
    }
    salida["tabla_de_perillas"] = {"0e042ac": viejo["tabla_de_rangos"],
                                   "HEAD": nuevo["tabla_de_rangos"]}

    print("\nla tabla de perillas (rango de N_eff / N_eff de la base)")
    print(f"{'corpus':<7}{'commit':<9}{'seed':>8}{'top_k':>8}{'pool':>8}"
          f"{'stopw':>8}{'+1 texto':>10}")
    for corpus in viejo["tabla_de_rangos"]:
        for commit, d in (("0e042ac", viejo), ("HEAD", nuevo)):
            r = d["tabla_de_rangos"].get(corpus)
            if not r:
                continue
            print(f"{corpus:<7}{commit:<9}{r['seed']:>8.3f}{r['top_k']:>8.3f}"
                  f"{r['pool']:>8.3f}{r['stopwords']:>8.3f}"
                  f"{r['mas_un_texto']:>10.3f}")

    tmp = SALIDA.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(salida, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    os.replace(tmp, SALIDA)
    print(f"\n-> {SALIDA}")


if __name__ == "__main__":
    main()
