"""
test_caso_10_device_skin.py — Caso 0.10: AgentDeviceSkin, primer agente
con objetivo propio sobre el ciclo ODA.

Toda la serie 0.4-0.9 usó AutonomousDevice con su gate LLM genérico
(GATE_PROMPT_04) — la decisión INTERACT/OP_SILENCE y el contenido
publicado dependían solo del campo CKM y el WELCOME MSG del canal,
nunca de un objetivo propio del device. Caso 0.10 introduce
AgentDeviceSkin (agent_device_skin.py): la decisión y el contenido los
define un agente externo ("wrapped agent") con su propio system
prompt, orientado a un objetivo — sin gate LLM propio.

2 devices:
  ResearcherSkin_Sonnet5_1    → AgentDeviceSkin, objetivo propio
                                 (explicar por qué importa la cohesión
                                 de conocimiento en sistemas multiagente)
  AutonomousControl_Sonnet5_2 → AutonomousDevice base, sin skin — control

Mismo provider y modelo en ambos (AnthropicProvider, claude-sonnet-5) —
la variable de esta corrida es el mecanismo de decisión/generación
(skin con objetivo propio vs gate LLM genérico), no el modelo.

Join escalonado, DELTA_T=5s — mismo diseño que Caso 0.9/0.8. El device
con skin es early (t=0), el control es late (t=5s) — elección arbitraria
del script, no especificada por la tarea; documentado acá para que sea
explícita.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_10_device_skin.py [--reset]
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

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from iap_chatroom.agent_device_skin import (  # noqa: E402
    AgentDeviceSkin,
    build_goal_directed_agent,
)
from iap_chatroom.autonomous_device import AutonomousDevice  # noqa: E402
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent / "_state"
_TRAJECTORY_PATH = _STATE_DIR / "monitor_trajectory.jsonl"

# WELCOME MSG del canal — igual que 0.4a/0.5/0.6/0.7/0.8/0.9. Solo lo
# usa AutonomousControl_Sonnet5_2 (control); ResearcherSkin_Sonnet5_1
# lo recibe también (requerido por el constructor) pero no lo usa para
# generar contenido — ver agent_device_skin.py.
SYSTEM_PROMPT_04A = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

# Objetivo propio del agente wrapped — del agente, no del canal.
RESEARCHER_GOAL_PROMPT = """You are {device_id}, an AI researcher.

Your goal: explain to whoever you meet why knowledge cohesion matters
in multi-agent systems. Engage substantively toward that goal.

You are in a shared chatroom with no turn structure. You can read the
full history, publish a message toward your goal, or choose not to
publish. If you have nothing useful to add toward your goal right now,
respond with exactly: OP_SILENCE"""

MODEL = "claude-sonnet-5"

DEVICE_SKIN = "ResearcherSkin_Sonnet5_1"
DEVICE_CONTROL = "AutonomousControl_Sonnet5_2"

DURATION = 90.0
POLL_INTERVAL = 2.0
DELTA_T = 5.0


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py..test_caso_09*.py.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


async def _run_late(device: AutonomousDevice) -> None:
    await asyncio.sleep(DELTA_T)
    await device.run(duration=DURATION - DELTA_T)


async def run_caso_10() -> None:
    print(f"[setup] {DEVICE_SKIN} = AgentDeviceSkin (objetivo propio, sin gate LLM) — early (t=0)")
    print(f"[setup] {DEVICE_CONTROL} = AutonomousDevice base (control, gate LLM genérico) — late (t={DELTA_T}s)")

    skin_provider = AnthropicProvider(model=MODEL)
    wrapped_agent = build_goal_directed_agent(
        device_id=DEVICE_SKIN,
        provider=skin_provider,
        goal_system_prompt=RESEARCHER_GOAL_PROMPT.format(device_id=DEVICE_SKIN),
    )
    skin_device = AgentDeviceSkin(
        device_id=DEVICE_SKIN,
        provider=skin_provider,
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_SKIN),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )

    control_device = AutonomousDevice(
        device_id=DEVICE_CONTROL,
        provider=AnthropicProvider(model=MODEL),
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_CONTROL),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )

    await asyncio.gather(
        skin_device.run(duration=DURATION),
        _run_late(control_device),
    )

    async with Client(MCP_URL) as client:
        firma_result = await client.call_tool("get_firma", {})
        firma: Optional[dict] = firma_result.data

        # since=0.0 — get_messages(since=None) trunca a los ultimos 20
        history_result = await client.call_tool("get_messages", {"since": 0.0})
        history: list[dict] = history_result.data

    print("\n=== Firma_CKM (cierre) ===")
    if firma is None:
        print("Firma_CKM: None (corpus aun en acumulacion)")
    else:
        for field in ("w_sha", "d_ckm", "temp_signal", "n_agentes", "timestamp", "delta_sha"):
            print(f"{field}: {firma.get(field)}")

    n_textos = {DEVICE_SKIN: 0, DEVICE_CONTROL: 0}
    for m in history:
        if m["device_id"] in n_textos:
            n_textos[m["device_id"]] += 1

    print("\n=== Textos publicados por device ===")
    for did, n in n_textos.items():
        etiqueta = "SKIN (objetivo propio)" if did == DEVICE_SKIN else "CONTROL (gate genérico)"
        print(f"{did} [{etiqueta}]: {n}")

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

    print("\n=== Historial completo del canal ===")
    for m in history:
        etiqueta = ""
        if m["device_id"] == DEVICE_SKIN:
            etiqueta = " [SKIN]"
        elif m["device_id"] == DEVICE_CONTROL:
            etiqueta = " [CONTROL]"
        print(f"[{m['device_id']}]{etiqueta} ({m['device_type']}) {m['text']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset", action="store_true",
        help="Preserva (mueve a process/ con timestamp, label caso10_run1) corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label="caso10_run1")
    else:
        asyncio.run(run_caso_10())
