"""
test_caso_13_handoff_dependency.py — Caso 0.13: 3 devices, dependencia
estructural sin orquestador evaluador.

Ver iap_chatroom/TASK_caso_13.md para la especificación completa
(gadanin.delamor). Primera corrida de la serie con 3 devices y join
simultáneo (no escalonado) — toda la serie 0.4-0.12 usó 1-2 devices.

  PeterPlam       → orquestador. AgentDeviceSkin + build_goal_directed_agent
                    (agent_device_skin.py, sin modificar). AnthropicProvider,
                    claude-haiku-4-5-20251001.
  TinkerBellucio  → analista. Mismo mecanismo. AnthropicProvider,
                    claude-sonnet-5.
  MarkOpolus      → forecaster. AgentDeviceSkin + build_search_grounded_agent
                    (groq_research_agent.py, nuevo esta sesión — conversacional
                    + búsqueda real vía ddgs, a diferencia de
                    build_autonomous_groq_agent que no lee el canal).
                    GroqProvider, llama-3.3-70b-versatile.

Dependencia estructural declarada (no impuesta por el protocolo, vive
en los prompts): MarkOpolus necesita el mapa de tensiones de
TinkerBellucio antes de construir escenarios — "sin él, espera".
Ninguna dependencia equivalente obliga a TinkerBellucio a esperar a
PeterPlam (ambas conocen el topic desde su propio system prompt) — es
deliberado, parte de lo que el caso observa: si el framing de Peter
influye en el orden real pese a no ser estructuralmente necesario.

Nota de implementación: "System prompts" y "Gate prompts" del
TASK_caso_13.md se combinan en un solo `goal_system_prompt` por
device — mismo patrón ya usado en ARCHITECT_GOAL_PROMPT/
THEORIST_GOAL_PROMPT (Caso 0.11): rol + instrucción de silencio en un
solo bloque, porque build_goal_directed_agent/build_search_grounded_agent
son de una sola llamada (deciden y generan a la vez, sin gate LLM
separado).

DURATION=120s (no especificado en la tarea — más largo que el estándar
de 90s de la serie 2-device, para dar lugar a la cadena de 3 pasos:
Peter abre → Tinker mapea → Mark construye escenarios). POLL_INTERVAL=2.0s.
Join simultáneo — sin DELTA_T.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_13_handoff_dependency.py [--reset]
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

from iap_chatroom.agent_device_skin import (  # noqa: E402
    AgentDeviceSkin,
    build_goal_directed_agent,
)
from iap_chatroom.groq_research_agent import (  # noqa: E402
    build_search_grounded_agent,
)
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402
from iap_chatroom.providers.groq_provider import GroqProvider  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent.parent / "_state"
_TRAJECTORY_PATH = _STATE_DIR / "monitor_trajectory.jsonl"

DEVICE_PETER = "PeterPlam"
DEVICE_TINKER = "TinkerBellucio"
DEVICE_MARK = "MarkOpolus"

HAIKU_MODEL = "claude-haiku-4-5-20251001"
SONNET_MODEL = "claude-sonnet-5"
GROQ_MODEL = "llama-3.3-70b-versatile"

DURATION = 120.0
POLL_INTERVAL = 2.0

# System prompt + gate prompt combinados (ver nota de implementación
# en el docstring del módulo). Rol/tarea primero, instrucción de
# silencio al final — mismo orden que TASK_caso_13.md.

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
- Publish your map in the channel. Be precise. Be trazable.

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
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py..test_caso_12*.py.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


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


async def run_caso_13() -> None:
    print("=== Caso 0.13 — Handoff dependency, 3 devices, join simultáneo ===")
    print(f"{DEVICE_PETER} (orquestador, Haiku) — {DEVICE_TINKER} (analista, Sonnet) — "
          f"{DEVICE_MARK} (forecaster, Groq+ddgs)")
    print("Dependencia declarada: Mark espera el mapa de Tinker. Sin dependencia "
          "equivalente para Peter→Tinker (deliberado, ver docstring del módulo).")

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

    max_n_rejected = 0
    delta_r_close: Optional[float] = None
    if _TRAJECTORY_PATH.exists():
        with open(_TRAJECTORY_PATH) as f:
            for line in f:
                panel = json.loads(line)["panel"]
                max_n_rejected = max(max_n_rejected, panel["n_rejected_pairs"])
                delta_r_close = panel["Delta_r_sum"]

    print("\n=== Trayectoria (resumen) ===")
    print(f"n_rejected_pairs (max): {max_n_rejected}")
    print(f"Delta_r_sum (cierre): {delta_r_close}")

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
        help="Preserva (mueve a process/ con timestamp, label caso13) "
             "corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label="caso13")
    else:
        asyncio.run(run_caso_13())
