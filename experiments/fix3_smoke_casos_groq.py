"""
fix3_smoke_casos_groq.py — fix 3: smoke de los siete `test_caso_*` que usan Groq

**ESTO ES UN SMOKE DEL CAMINO DEL CÓDIGO, NO UNA RÉPLICA DE LOS CASOS.**

Los casos originales corrieron con los providers y los modelos que dice cada
uno. Acá **todos los providers se reemplazan por `GroqProvider("openai/
gpt-oss-20b")`**, porque `ANTHROPIC_API_KEY` no está en el entorno. Lo que
mide es **si el camino del código sigue andando con el ODA continuo**, no qué
pasó en el caso. Los números que salgan **no son comparables** con los REG de
los casos 09 a 15, y nada de lo que digan los modelos se interpreta.

Orden de delamor, opción (a) (DECISIONES `0e63e50`).

### Por qué no se puede "correr los que usan sólo Groq"

Medido: **ninguno de los 21 usa sólo Groq.** Los siete que lo usan instancian
también `AnthropicProvider`. Y los 21 **no son tests de pytest**: no tienen
ninguna función `def test_` y `pytest --collect-only` recoge **0 items**. Son
scripts con `if __name__ == "__main__"`.

### Cómo corre cada caso sin modificar su archivo

1. `runpy.run_path(..., run_name="__main__")` — ejecuta el archivo como script.
   Importarlo no alcanza: el trabajo está dentro del `if __name__`.
2. Los providers se parchan **en su módulo de origen, antes de que el caso lo
   importe**: el `from ... import X` del caso queda ligado al objeto parchado.
3. `AutonomousDevice.__init__` se envuelve para **registrar cada instancia**, y
   así se puede sacar su `costo()` después — los devices se crean adentro del
   caso y de otro modo no habría manera de verlos.
4. Un **subprocess por caso**: los singletons (`ChatChannel`, `CKMMonitor`) y el
   loop de asyncio no se pueden limpiar entre casos de forma confiable. Dos
   casos en el mismo proceso se contaminarían y el smoke mediría eso.
5. **Un server por caso**, con su `--state-dir` aislado (fix 2).

### El tope de duración

`--tope N` limita lo que cada device corre, envolviendo `AutonomousDevice.run`.
Es **decisión de Code y va declarada**: el smoke mide si el camino rompe, y eso
rompe en las primeras vueltas. Sin tope, los siete son 750 s y **888 a 1776
llamadas**; con `--tope 20` bajan a unas 190 en el piso.

**Con tope, un caso que no rompe no dice que el caso ande**: dice que no rompió
en las vueltas que corrió. Eso va en el reporte.

Uso:
    # el plan y el costo, sin gastar nada
    PYTHONPATH=/workspaces/ckm python3 experiments/fix3_smoke_casos_groq.py --estimar

    # correr (pide --confirmar: gasta llamadas)
    PYTHONPATH=/workspaces/ckm python3 experiments/fix3_smoke_casos_groq.py \
        --confirmar --tope 20 [--solo 13_handoff_dependency]

    # modo interno, lo usa el driver por caso
    ... --run-caso <nombre> --salida <json> [--tope N]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

CASOS = [
    "09_provider_hetero_join_escalonado_2dev",
    "09_provider_hetero_join_escalonado_2dev_PREGENERADO",
    "12_groq_research_skin",
    "13_handoff_dependency",
    "14_handoff_english",
    "14_run2_opus_tinker",
    "15_behavior_graph",
]

MODELO = "openai/gpt-oss-20b"
PUERTO = 7860
MCP_SALUD = f"http://localhost:{PUERTO}/api/monitor"
STATE_BASE = RAIZ / "experiments" / "_state_fix3"

# Medido en los vivos: con poll 5.0 salieron 5.2 s por vuelta, así que la
# latencia del provider es ~0.2 s. Con poll 2.0, ~2.2 s por vuelta.
S_POR_VUELTA = 2.2


def _ruta(caso: str) -> Path:
    return RAIZ / "iap_chatroom" / "tests" / f"test_caso_{caso}.py"


# ── estimación, sin gastar nada ─────────────────────────────────────────────

def estimar(tope: "float | None") -> dict:
    import re

    filas, piso, techo, segundos = [], 0, 0, 0.0
    for c in CASOS:
        src = _ruta(c).read_text()
        m = re.search(r"^DURATION\s*=\s*([0-9.]+)", src, re.M)
        dur = float(m.group(1)) if m else 0.0
        efectiva = min(dur, tope) if tope else dur
        dev = len(re.findall(r"\.run\(duration", src))
        vueltas = int(efectiva / S_POR_VUELTA)
        filas.append({
            "caso": c, "duration_del_caso_s": dur, "duration_efectiva_s": efectiva,
            "devices": dev, "vueltas_por_device": vueltas,
            "llamadas_piso": dev * vueltas, "llamadas_techo": dev * vueltas * 2,
        })
        piso += dev * vueltas
        techo += dev * vueltas * 2
        segundos += efectiva
    return {
        "por_caso": filas,
        "llamadas_piso": piso,
        "llamadas_techo": techo,
        "segundos_de_corrida": segundos,
        "nota": (
            "piso = 1 llamada al gate por vuelta; techo = 2, si actúa siempre. "
            "No incluye los arranques de server ni las búsquedas de ddgs del "
            "caso 12 (que no son llamadas al LLM)."
        ),
    }


# ── el runner de UN caso, dentro de su propio proceso ──────────────────────

def correr_un_caso(caso: str, tope: "float | None") -> dict:
    import runpy

    from iap_chatroom import arranque
    from iap_chatroom.autonomous_device import AutonomousDevice
    from iap_chatroom.providers.groq_provider import GroqProvider

    state_dir = STATE_BASE / caso
    arranque.fijar_state_dir(state_dir)

    # (1) todos los providers pasan a ser el mismo Groq. Se parcha en el módulo
    #     de origen, así el `from ... import` del caso toma esto.
    sustituciones = []

    def _groq(*a, **kw):
        sustituciones.append({"args": [str(x) for x in a], "kwargs": {k: str(v) for k, v in kw.items()}})
        return GroqProvider(model=MODELO)

    import iap_chatroom.providers.groq_provider as mod_groq
    mod_groq.GroqProvider = _groq
    try:
        import iap_chatroom.providers.anthropic_provider as mod_anth
        mod_anth.AnthropicProvider = _groq
    except ImportError:
        pass   # si no existe, no hay nada que sustituir; queda declarado

    # (2) registrar los devices que el caso cree, para poder leer su costo()
    devices = []
    _init = AutonomousDevice.__init__

    def init_registrando(self, *a, **kw):
        _init(self, *a, **kw)
        devices.append(self)

    AutonomousDevice.__init__ = init_registrando

    # (3) el tope, envolviendo run(). Declarado: cambia lo que el caso pidió.
    if tope:
        _run = AutonomousDevice.run

        async def run_con_tope(self, duration: float = 60.0):
            return await _run(self, duration=min(duration, tope))

        AutonomousDevice.run = run_con_tope

    res = {
        "caso": caso,
        "state_dir": str(state_dir),
        "modelo_sustituto": MODELO,
        "tope_s": tope,
        "es_smoke_no_replica": True,
    }
    argv_previo = sys.argv[:]
    t0 = time.time()
    try:
        sys.argv = [str(_ruta(caso))]
        runpy.run_path(str(_ruta(caso)), run_name="__main__")
        res["resultado"] = "CORRIO"
    except BaseException as e:          # noqa: BLE001 — el traceback entero es el dato
        res["resultado"] = "ROMPIO"
        res["excepcion"] = type(e).__name__
        res["traceback"] = traceback.format_exc()
    finally:
        sys.argv = argv_previo
        res["segundos"] = round(time.time() - t0, 2)
        res["providers_sustituidos"] = sustituciones
        res["n_providers_sustituidos"] = len(sustituciones)
        res["por_device"] = []
        for d in devices:
            try:
                res["por_device"].append({"costo": d.costo()})
            except BaseException as e:   # noqa: BLE001
                res["por_device"].append({
                    "costo": None,
                    "fallo_al_leer_costo": f"{type(e).__name__}: {e}",
                })
    return res


# ── el driver: un server y un subprocess por caso ──────────────────────────

def _server_arriba(timeout: float = 45.0) -> bool:
    import urllib.error
    import urllib.request

    fin = time.time() + timeout
    while time.time() < fin:
        try:
            with urllib.request.urlopen(MCP_SALUD, timeout=2):
                return True
        except (urllib.error.URLError, OSError):
            time.sleep(1.0)
    return False


def correr_todos(tope: "float | None", solo: "list[str] | None") -> dict:
    casos = [c for c in CASOS if not solo or c in solo]
    salidas = []
    for c in casos:
        state_dir = STATE_BASE / c
        state_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== {c} · state_dir={state_dir} ===", flush=True)

        server = subprocess.Popen(
            [sys.executable, str(RAIZ / "iap_chatroom" / "server.py"),
             "--state-dir", str(state_dir)],
            cwd=str(RAIZ), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env={**os.environ, "PYTHONPATH": str(RAIZ)},
        )
        try:
            if not _server_arriba():
                salidas.append({
                    "caso": c, "resultado": "SERVER_NO_ARRANCO",
                    "es_smoke_no_replica": True,
                })
                continue

            json_salida = state_dir / "resultado.json"
            r = subprocess.run(
                [sys.executable, str(Path(__file__)),
                 "--run-caso", c, "--salida", str(json_salida)]
                + (["--tope", str(tope)] if tope else []),
                cwd=str(RAIZ), capture_output=True, text=True, timeout=600,
                env={**os.environ, "PYTHONPATH": str(RAIZ)},
            )
            if json_salida.exists():
                d = json.loads(json_salida.read_text())
            else:
                d = {"caso": c, "resultado": "EL_RUNNER_NO_DEJO_JSON",
                     "stdout_runner": r.stdout[-3000:], "stderr_runner": r.stderr[-3000:]}
            d["returncode_runner"] = r.returncode
            d["stdout_cola"] = r.stdout[-2000:]
            salidas.append(d)
        finally:
            server.terminate()
            try:
                server.wait(timeout=15)
            except subprocess.TimeoutExpired:
                server.kill()
            out = server.stdout.read().decode(errors="replace") if server.stdout else ""
            salidas[-1]["server_stdout_cola"] = out[-1500:]

    return {
        "que_es": "SMOKE DEL CAMINO DEL CODIGO — fix 3. NO es replica de los casos.",
        "declarado": {
            "todos_los_providers_sustituidos_por": MODELO,
            "por_que": "ANTHROPIC_API_KEY ausente en el entorno",
            "tope_s": tope,
            "si_hay_tope": (
                "un caso que no rompe NO dice que el caso ande: dice que no "
                "rompio en las vueltas que corrio"
            ),
            "no_se_interpreta": "nada de lo que digan los modelos",
            "no_se_arregla": "lo que rompa queda reportado, no corregido",
        },
        "estimacion_previa": estimar(tope),
        "repo_commit": subprocess.run(
            ["git", "-C", str(RAIZ), "rev-parse", "HEAD"],
            capture_output=True, text=True).stdout.strip(),
        "por_caso": salidas,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--estimar", action="store_true", help="solo el costo, sin gastar")
    p.add_argument("--confirmar", action="store_true", help="hace falta para correr")
    p.add_argument("--tope", type=float, default=None)
    p.add_argument("--solo", nargs="*", default=None)
    p.add_argument("--run-caso", default=None, help="modo interno")
    p.add_argument("--salida", default=None)
    a = p.parse_args()

    if a.run_caso:
        res = correr_un_caso(a.run_caso, a.tope)
        destino = Path(a.salida) if a.salida else (STATE_BASE / a.run_caso / "resultado.json")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
        print(f"[{a.run_caso}] {res['resultado']} -> {destino}")
        return 0

    if a.estimar or not a.confirmar:
        est = estimar(a.tope)
        print(json.dumps(est, indent=1, ensure_ascii=False))
        if not a.estimar:
            print("\nNo se corrio nada: falta --confirmar. Gasta llamadas reales.",
                  file=sys.stderr)
        return 0

    res = correr_todos(a.tope, a.solo)
    destino = RAIZ / "experiments" / "fix3_smoke_casos_groq_log.json"
    tmp = destino.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    tmp.replace(destino)
    print(f"\nlog -> {destino}")
    for d in res["por_caso"]:
        print(f"  {d['caso']:<52} {d['resultado']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
