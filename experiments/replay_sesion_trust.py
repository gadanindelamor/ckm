"""
replay_sesion_trust.py — replay de un tramo de la sesión TRUST

TASK_replay_sesion_trust_v3. La sesión fue en vivo y no se puede reproducir
(muestreo no determinista, harness cambiante, cada turno humano respondió a
la salida anterior, compactación en el medio). Entonces no se reproduce: se
reenvían los turnos humanos de un tramo y se mide si las respuestas nuevas
caen en las MISMAS CUENCAS que las originales.

    La pregunta no es si las respuestas salen iguales — no van a salir
    iguales. Es si el campo conserva la forma aunque el contenido cambie.

Insumos (en `process/replay/_private/`, ignorado por git: es conversación
personal y el repo va a ser público):
    EXPORT_sesion_trust_parte2_v1.md   turnos humanos y respuestas visibles
    tramos_paso1.json                  el tramo, elegido por delamor

Estado de implementación: **A** (parsear y cortar) y **C.1** (la W única).
B (replay por API) y C.2–C.4 se escriben después del OK de CP2 — los
checkpoints de la TASK §6 no se encadenan.

Uso:
    python experiments/replay_sesion_trust.py --paso A
    python experiments/replay_sesion_trust.py --paso C1 [--top-k 32]
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services"))
PRIV = REPO / "process/replay/_private"
EXPORT = PRIV / "EXPORT_sesion_trust_parte2_v1.md"
TRAMOS = PRIV / "tramos_paso1.json"

ENCABEZADO = re.compile(r"^\*\*(delamor|Claude)\*\*\s*—\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})\s*$")


@dataclass
class Turno:
    i     : int
    rol   : str      # "delamor" | "Claude"
    ts    : str      # ISO a minuto, como viene en el export
    texto : str


def parse_export(path: Path = EXPORT) -> list:
    """Turnos separados por `---`, con encabezado `**rol** — <timestamp>`.

    Un bloque sin encabezado reconocible (el preámbulo del export) se
    descarta. El texto del turno es todo lo que sigue al encabezado, sin
    normalizar: el extractor es quien decide después qué es un término.
    """
    bloques = re.split(r"(?m)^---\s*$", path.read_text(encoding="utf8"))
    turnos, i = [], 0
    for b in bloques:
        lineas = [l for l in b.strip().splitlines()]
        if not lineas:
            continue
        m = ENCABEZADO.match(lineas[0].strip())
        if not m:
            continue
        texto = "\n".join(lineas[1:]).strip()
        if not texto:
            continue
        turnos.append(Turno(i=i, rol=m.group(1), ts=m.group(2), texto=texto))
        i += 1
    return turnos


def cortar(turnos: list, desde: str, hasta: str) -> dict:
    """Turnos humanos dentro de [desde, hasta] + la respuesta de Claude al
    último humano (TASK §4.A.2). El timestamp del export llega al minuto, así
    que la comparación es de cadenas ISO y los bordes son inclusive."""
    humanos = [t for t in turnos if t.rol == "delamor" and desde <= t.ts <= hasta]
    if not humanos:
        return {"humanos": [], "originales": []}
    # respuestas de Claude dentro del tramo, más la del último turno humano
    ultimo = humanos[-1].i
    siguiente = next((t for t in turnos if t.i > ultimo and t.rol == "Claude"), None)
    originales = [t for t in turnos
                  if t.rol == "Claude" and humanos[0].i < t.i <= ultimo]
    if siguiente is not None:
        originales.append(siguiente)
    return {"humanos": humanos, "originales": originales}


def paso_A(tramo_id: str = None) -> dict:
    tramos = json.loads(TRAMOS.read_text(encoding="utf8"))
    out = {}
    for spec in tramos:
        if tramo_id and spec["id"] != tramo_id:
            continue
        turnos = parse_export()
        corte = cortar(turnos, spec["desde"], spec["hasta"])
        for clave in ("humanos", "originales"):
            destino = PRIV / f"tramo_{spec['id']}_{clave}.json"
            destino.write_text(json.dumps([asdict(t) for t in corte[clave]],
                                          ensure_ascii=False, indent=1), encoding="utf8")
        out[spec["id"]] = {"spec": spec, "turnos_export": len(turnos),
                           "humanos": len(corte["humanos"]),
                           "originales": len(corte["originales"]),
                           "corte": corte}
    return out


# ── C.1 — la W única ────────────────────────────────────────────────────────
# Una sola W, desde las respuestas ORIGINALES del tramo: las cuencas de W
# distintas no se corresponden entre sí, así que si cada replay tuviera su
# propia W no habría nada que comparar. Construida UNA vez
# (rebuild_suspendido): en caso09 W se reconstruía por mensaje y los nodos
# nunca se estabilizaron. W_pos (force_w_pos) porque una conversación es un
# corpus de coordinación, no de debate, y ahí los marcadores de oposición
# funcionan como conectores — paper v26 §5.1, REG_unidad_texto §5.

THETA_W_NO_USADO = 0.0      # el Gatekeeper no participa en este run
SCALE_NO_USADO   = "log"    # declarativo: nadie lo lee (verificado en el repo)


def construir_W(originales: list, top_k: int, tramo_id: str):
    from corpus_service import CorpusService
    from ckm_landscape_config import CKMlandscapeConfigV1

    textos = [t["texto"] if isinstance(t, dict) else t.texto for t in originales]
    estado = PRIV / f"corpus_state_{tramo_id}_k{top_k}.json"
    if estado.exists():
        estado.unlink()
    c = CorpusService(storage_path=str(estado), min_texts=len(textos),
                      top_k=top_k, rebuild_suspendido=True, force_w_pos=True)
    c.ingest(textos)
    c.save()
    W, nodos = c.get_W(), c.get_nodes()
    cfg = None
    if W is not None:
        cfg = CKMlandscapeConfigV1.from_W(W, theta_W=THETA_W_NO_USADO,
                                        sampling_mode="uniform",
                                        scale=SCALE_NO_USADO)
    return W, nodos, cfg, c


def paso_C1(tramo_id: str, top_k: int):
    originales = json.loads((PRIV / f"tramo_{tramo_id}_originales.json")
                            .read_text(encoding="utf8"))
    W, nodos, cfg, c = construir_W(originales, top_k, tramo_id)
    print(f"tramo {tramo_id} · top_k {top_k} · textos {len(originales)}")
    print(f"  modo del corpus: {c.status()['mode']} · N = {len(nodos)}")
    if W is None:
        print("  W = None — el corpus sigue en acumulación: el dato no distingue")
        return
    import numpy as np
    ii, jj = np.triu_indices(len(W), 1)
    u = W[ii, jj]
    print(f"  nodos: {nodos}")
    print(f"  densidad {float((u != 0).mean()):.3f} · negativos {int((u < 0).sum())} "
          f"· pares distintos {int((u != 0).sum())} de {len(u)}")
    print(f"  mu_W_nonzero {cfg.mu_W_nonzero:.4f} · mu_W_global {cfg.mu_W_global:.4f}")
    print(f"  beta_c_nonzero {cfg.beta_c_nonzero:.4f} · beta_c_global {cfg.beta_c_global:.4f}")
    print(f"  sha256(W) = {cfg.w_version_id}")
    print(f"  config_id = {cfg.config_id}")
    print(f"  theta_W {cfg.theta_W} (NO USADO) · sampling_mode {cfg.sampling_mode} "
          f"· scale {cfg.scale} (NO USADO)")
    reg = getattr(c, "_registro_borde", [])
    if reg:
        emp = [d for d in reg if abs(d["distancia_al_corte"]) <= 1e-12]
        print(f"  registro_borde: {len(reg)} términos del pool · "
              f"empatados en el corte: {len(emp)}")


# ── C.2 / C.3 — proyección y ocupación ──────────────────────────────────────
# Cada respuesta pasa por evaluate(texto, nodos) -> sigma, y se relaja con
# relax_orbit sobre la W única (regla GOLES: h_i = 0 conserva el estado, lo
# que hace la salida determinista dado (W, sigma_0)). La órbita final es el
# lugar donde cae esa respuesta. La ocupación es la fracción de respuestas
# por órbita, y N_eff = 1/Σm² sobre esa ocupación.

def proyectar(textos: list, W, nodos: list) -> list:
    from node_extractor import NodeExtractorService
    from landscape_engine import relax_orbit
    ex = NodeExtractorService()
    out = []
    for i, t in enumerate(textos):
        sigma = ex.evaluate(t, nodos)
        orbita, periodo, cola, _ = relax_orbit(sigma, W)
        out.append({"i": i, "palabras": len(t.split()),
                    "activados": int((sigma > 0).sum()),
                    "nodos_activos": [nodos[k] for k, s in enumerate(sigma) if s > 0],
                    "orbita": orbita, "periodo": periodo, "cola": cola})
    return out


def ocupacion(proy: list) -> dict:
    """fracción de respuestas por órbita, con la órbita como clave."""
    cuenta = {}
    for p in proy:
        cuenta[p["orbita"]] = cuenta.get(p["orbita"], 0) + 1
    n = len(proy)
    return {o: c / n for o, c in cuenta.items()}


def paso_C3(tramo_id: str, top_k: int):
    import numpy as np
    from landscape_engine import n_eff
    originales = json.loads((PRIV / f"tramo_{tramo_id}_originales.json")
                            .read_text(encoding="utf8"))
    textos = [t["texto"] for t in originales]
    W, nodos, cfg, _ = construir_W(originales, top_k, tramo_id)
    proy = proyectar(textos, W, nodos)
    occ = ocupacion(proy)
    act = [p["activados"] for p in proy]

    print(f"tramo {tramo_id} · N {len(nodos)} · sha256(W) {cfg.w_version_id[:16]}…")
    print(f"\nnodos activados por respuesta (de {len(nodos)}):")
    for p in proy:
        print(f"  resp {p['i']} · {p['palabras']:4d} palabras · {p['activados']:2d} activos "
              f"· periodo {p['periodo']} · cola {p['cola']:2d} · {p['nodos_activos']}")
    print(f"\n  mediana de activados: {float(np.median(act))}  (min {min(act)}, máx {max(act)})")

    claves = {o: f"orb{k}" for k, o in enumerate(sorted(occ, key=lambda o: -occ[o]))}
    print(f"\nocupación — {len(occ)} órbita(s) distintas para {len(proy)} respuestas:")
    for o, f in sorted(occ.items(), key=lambda kv: -kv[1]):
        quienes = [p["i"] for p in proy if p["orbita"] is o or p["orbita"] == o]
        print(f"  {claves[o]}: masa {f:.3f} ({len(quienes)}/{len(proy)}) "
              f"periodo {len(o)} · respuestas {quienes}")
    masas = np.array(sorted(occ.values(), reverse=True))
    print(f"\n  N_eff del original = {n_eff(masas):.3f}")
    return proy, occ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paso", default="A", choices=["A", "C1", "C3"])
    ap.add_argument("--tramo", default="categorias")
    ap.add_argument("--top-k", type=int, default=32)
    a = ap.parse_args()
    if a.paso == "C1":
        paso_C1(a.tramo, a.top_k)
        return
    if a.paso == "C3":
        paso_C3(a.tramo, a.top_k)
        return
    for tid, r in paso_A(a.tramo).items():
        h, o = r["corte"]["humanos"], r["corte"]["originales"]
        print(f"tramo {tid}: export {r['turnos_export']} turnos | "
              f"humanos {r['humanos']} | originales de Claude {r['originales']}")
        if h:
            print(f"  primer humano  [{h[0].ts}] {h[0].texto[:90]}")
            print(f"  último humano  [{h[-1].ts}] {h[-1].texto[:90]}")
        if o:
            print(f"  palabras en originales: "
                  f"{[len(t.texto.split()) for t in o]}")


if __name__ == "__main__":
    main()
