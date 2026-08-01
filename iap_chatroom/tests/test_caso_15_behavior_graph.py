"""
test_caso_15_behavior_graph.py — Caso 0.15: Caso 0.14 Run 1 +
BehaviorGraph G integrado en MonitorService, en paralelo real.

Ver iap_chatroom/readme/TASK_caso_15.md para la especificación
completa (gadanin.delamor). Mismo diseño exacto que Caso 0.14 Run 1
(3 devices, join simultáneo, dependencia estructural Mark←Tinker,
prompt de Tinker 100% inglés) — el único cambio es que ahora el
`MonitorService` real del servidor corre con un `BehaviorGraph`
conectado (ver `iap_chatroom/ckm_monitor.py`, cambio autorizado
explícitamente por gadanin.delamor: único punto de integración que
no vuelve G retroactivo).

G corre en paralelo a {W, Δ_W} en tiempo real dentro del proceso del
servidor — cada mensaje que `CKMMonitor.on_message()` ingiere en
`self._corpus` también entra a `self._behavior_graph` vía
`MonitorService.evaluate()`. Este script NO construye su propio
corpus/monitor/G — lee el `corpus_G_state.json` que el servidor
persiste en `_state/`, el mismo mecanismo que ya se usa para leer
`monitor_trajectory.jsonl`.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/tests/test_caso_15_behavior_graph.py [--reset]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastmcp import Client

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_PATH)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_SERVICES_DIR = _REPO_ROOT / "services"
if str(_SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(_SERVICES_DIR))

from iap_chatroom.agent_device_skin import (  # noqa: E402
    AgentDeviceSkin,
    build_goal_directed_agent,
)
from iap_chatroom.groq_research_agent import (  # noqa: E402
    build_search_grounded_agent,
)
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402
from iap_chatroom.providers.groq_provider import GroqProvider  # noqa: E402
from behavior_graph import BehaviorGraph  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent.parent / "_state"
_TRAJECTORY_PATH = _STATE_DIR / "monitor_trajectory.jsonl"
_G_STATE_PATH = _STATE_DIR / "corpus_G_state.json"

DEVICE_PETER = "PeterPlam"
DEVICE_TINKER = "TinkerBellucio"
DEVICE_MARK = "MarkOpolus"

HAIKU_MODEL = "claude-haiku-4-5-20251001"
SONNET_MODEL = "claude-sonnet-5"
GROQ_MODEL = "llama-3.3-70b-versatile"

DURATION = 120.0
POLL_INTERVAL = 2.0

PETER_GOAL_PROMPT = """You are Peter Plam, an orchestrator in a multi-device channel.

The channel has three participants:
- Tinker Bellucio — analyzes tensions and conflicts in the topic
- Mark Opolus — builds probable scenarios using web research
- You — coordinate the work without executing analysis yourself

Your role:
- Open the channel with a clear framing of the shared task
- Monitor what each device publishes
- Signal when Tinker's output is ready for Mark to build on
- Do not analyze. Do not produce scenarios. Coordinate.

The shared task: map the structural tensions in current world
economics — speed of human adaptation, geopolitical
reconfiguration — so that probable scenarios can be constructed
from that map.

Read the channel history.

If you haven't opened the channel yet with the shared task framing,
do so now.
If Tinker Bellucio just published a tension map and Mark Opolus
hasn't built on it yet, signal that clearly — point at what's ready
for Mark.
If there's nothing new to coordinate — respond with exactly: OP_SILENCE"""

TINKER_GOAL_PROMPT = """You are Tinker Bellucio, an analyst in a multi-device channel.

Your role: map structural tensions in current world economics —
speed of human adaptation, geopolitical reconfiguration.

How you work:
- Read the channel history
- Identify tensions, conflicts, and points of genuine divergence
  — not superficial disagreements
- Publish your map in the channel. Be precise. Be traceable.

Do not build scenarios. Do not forecast. Map what is.

Read the channel history.

If there is new content relevant to your analysis, or your map is
incomplete — publish your next contribution.

If you have already published a complete map and nothing new has
arrived — respond with exactly: OP_SILENCE"""

MARK_GOAL_PROMPT = """You are Mark Opolus, a Greek researcher in a shared channel.

Your role: build probable scenarios about world economics —
speed of human adaptation, geopolitical reconfiguration.

You work from what Tinker Bellucio publishes in the channel.
Her map of structural tensions is your starting point.
Without it, you wait.

You have access to web search results (provided below, grounded in
the most recent channel content). Use them to ground your scenarios
in current data.

Do not analyze tensions. Do not map conflicts.
Build scenarios from what is already mapped.

Read the channel history.

If Tinker Bellucio has published a tension map and you have new
scenarios to build or extend — publish your contribution.

If Tinker has not yet published, or you have nothing to add —
respond with exactly: OP_SILENCE"""


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json, monitor_trajectory.jsonl y
    corpus_G_state.json en process/ antes de correr — no borra, mueve
    con sufijo .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py..test_caso_14*.py, extendido para G (nuevo en
    0.15): corpus_G_state.json va a process/experiments/, no a
    process/ plano, siguiendo la estructura de directorios acordada.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")

    g_src = state_dir / "corpus_G_state.json"
    if g_src.exists():
        experiments_dir = process_dir / "experiments"
        experiments_dir.mkdir(exist_ok=True)
        g_dst = experiments_dir / f"corpus_G_state.json.bak_{int(time.time())}_{label}"
        shutil.move(str(g_src), str(g_dst))
        print(f"[prepare_state] corpus_G_state.json preservado en {g_dst}")


def _make_peter_device() -> AgentDeviceSkin:
    provider = AnthropicProvider(model=HAIKU_MODEL)
    wrapped_agent = build_goal_directed_agent(
        device_id=DEVICE_PETER,
        provider=provider,
        goal_system_prompt=PETER_GOAL_PROMPT,
    )
    return AgentDeviceSkin(
        device_id=DEVICE_PETER,
        provider=provider,
        system_prompt=PETER_GOAL_PROMPT,
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )


def _make_tinker_device() -> AgentDeviceSkin:
    provider = AnthropicProvider(model=SONNET_MODEL)
    wrapped_agent = build_goal_directed_agent(
        device_id=DEVICE_TINKER,
        provider=provider,
        goal_system_prompt=TINKER_GOAL_PROMPT,
    )
    return AgentDeviceSkin(
        device_id=DEVICE_TINKER,
        provider=provider,
        system_prompt=TINKER_GOAL_PROMPT,
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )


def _make_mark_device() -> AgentDeviceSkin:
    provider = GroqProvider(model=GROQ_MODEL)
    wrapped_agent = build_search_grounded_agent(
        device_id=DEVICE_MARK,
        provider=provider,
        goal_system_prompt=MARK_GOAL_PROMPT,
        search_results=3,
    )
    return AgentDeviceSkin(
        device_id=DEVICE_MARK,
        provider=provider,
        system_prompt=MARK_GOAL_PROMPT,
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )


async def run_caso_15() -> None:
    print("=== Caso 0.15 — Caso 0.14 Run 1 + BehaviorGraph G en paralelo real ===")
    print(f"{DEVICE_PETER} (orquestador, Haiku) — {DEVICE_TINKER} (analista, Sonnet) — "
          f"{DEVICE_MARK} (forecaster, Groq+ddgs)")
    print("Dependencia declarada: Mark espera el mapa de Tinker.")
    print("G corre dentro del servidor (ckm_monitor.py), no en este script.")

    peter = _make_peter_device()
    tinker = _make_tinker_device()
    mark = _make_mark_device()

    await asyncio.gather(
        peter.run(duration=DURATION),
        tinker.run(duration=DURATION),
        mark.run(duration=DURATION),
    )

    async with Client(MCP_URL) as client:
        firma_result = await client.call_tool("get_firma", {})
        firma: Optional[dict] = firma_result.data

        history_result = await client.call_tool("get_messages", {"since": 0.0})
        history: list[dict] = history_result.data

    print("\n=== Firma_CKM (cierre) ===")
    if firma is None:
        print("Firma_CKM: None (corpus aun en acumulacion)")
    else:
        for field in ("w_sha", "d_ckm", "temp_signal", "n_agentes", "timestamp", "delta_sha"):
            print(f"{field}: {firma.get(field)}")

    n_textos = {DEVICE_PETER: 0, DEVICE_TINKER: 0, DEVICE_MARK: 0}
    for m in history:
        if m["device_id"] in n_textos:
            n_textos[m["device_id"]] += 1

    print("\n=== Textos publicados por device ===")
    etiquetas = {
        DEVICE_PETER: "PETER (orquestador)",
        DEVICE_TINKER: "TINKER (analista)",
        DEVICE_MARK: "MARK (forecaster)",
    }
    for did, n in n_textos.items():
        print(f"{did} [{etiquetas[did]}]: {n}")

    print("\n=== Chequeo de fuga de sentinel (post-fix) ===")
    n_leaked = 0
    for m in history:
        body = m.get("text", "")
        stripped = body.strip()
        if stripped.upper() != "OP_SILENCE" and "OP_SILENCE" in stripped.upper():
            n_leaked += 1
            print(f"  POSIBLE FUGA: [{m['device_id']}] {body[:60]!r}")
    print(f"Total mensajes con 'OP_SILENCE' publicados como contenido: {n_leaked} (esperado: 0)")

    max_n_rejected = 0
    delta_r_close: Optional[float] = None
    if _TRAJECTORY_PATH.exists():
        with open(_TRAJECTORY_PATH) as f:
            for line in f:
                panel = json.loads(line)["panel"]
                max_n_rejected = max(max_n_rejected, panel["n_rejected_pairs"])
                delta_r_close = panel["Delta_r_sum"]

    print("\n=== Trayectoria W (resumen) ===")
    print(f"n_rejected_pairs (max): {max_n_rejected}")
    print(f"Delta_r_sum (cierre): {delta_r_close}")

    # G_state final — leído del archivo real que el servidor persistió
    # en paralelo (no reconstruido acá, no retroactivo).
    print("\n=== G_state final ===")
    if _G_STATE_PATH.exists():
        g = BehaviorGraph(storage_path=str(_G_STATE_PATH))
        gs = g.g_state()
        print(f"D_G: {gs['D_G']}  sparsity: {gs['G_sparsity']}  "
              f"n_texts: {gs['n_texts']}  mode: {gs['mode']}")
        print("Top co-activaciones:")
        for p in gs["top_coactivations"]:
            print(f"  {p['a']:12s} <-> {p['b']:12s}  {p['weight']:.3f}")
    else:
        print(f"corpus_G_state.json no existe en {_G_STATE_PATH} — "
              f"verificar que ckm_monitor.py conectó behavior_graph.")

    print("\n=== Verificación de dependencia estructural ===")
    first_tinker_idx = next(
        (i for i, m in enumerate(history) if m["device_id"] == DEVICE_TINKER), None
    )
    first_mark_idx = next(
        (i for i, m in enumerate(history) if m["device_id"] == DEVICE_MARK), None
    )
    if first_mark_idx is None:
        print("MarkOpolus no publicó nada — sin datos para verificar la dependencia.")
    elif first_tinker_idx is None:
        print("MarkOpolus publicó SIN que TinkerBellucio publicara antes — "
              "dependencia estructural NO se sostuvo en el canal.")
    elif first_mark_idx > first_tinker_idx:
        print(f"OK — primer mensaje de Tinker en índice {first_tinker_idx}, "
              f"primer mensaje de Mark en índice {first_mark_idx}. "
              "Dependencia estructural se sostuvo.")
    else:
        print(f"Mark publicó (índice {first_mark_idx}) antes que Tinker "
              f"(índice {first_tinker_idx}) — dependencia estructural NO se sostuvo.")

    print("\n=== Historial completo del canal ===")
    for i, m in enumerate(history):
        etiqueta = f" [{etiquetas[m['device_id']].split()[0]}]" if m["device_id"] in etiquetas else ""
        print(f"[{i}] [{m['device_id']}]{etiqueta} ({m['device_type']}) {m['text']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset", action="store_true",
        help="Preserva (mueve a process/ con timestamp, label caso15) "
             "corpus_state.json, monitor_trajectory.jsonl y "
             "corpus_G_state.json antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label="caso15")
    else:
        asyncio.run(run_caso_15())
