"""
test_caso_11_two_skins.py — Caso 0.11: dos AgentDeviceSkin, objetivos
distintos, sin control.

Caso 0.10 probó 1 skin (objetivo propio) + 1 AutonomousDevice control
(gate genérico) — el control se enganchó con profundidad técnica real
al objetivo del skin. Caso 0.11 quita el control: ambos devices tienen
objetivo propio, orientaciones distintas (práctica vs teoría), no
diseñadas para estar en conflicto. Qué emerge del cruce es el dato —
no se predetermina acá.

2 devices, ambos AgentDeviceSkin (agent_device_skin.py, sin modificar):

  ArchitectSkin_Sonnet5_1 → orientado a práctica: qué importa al
                             desplegar sistemas multiagente en producción.
  TheoristSkin_Sonnet5_2  → orientado a teoría: cómo emergen
                             conocimiento y significado de la interacción.

Mismo provider/modelo en ambos (AnthropicProvider, claude-sonnet-5) —
la variable es la orientación de objetivo (práctica vs teoría), no
modelo ni provider ni mecanismo (ambos son skin esta vez, a diferencia
de 0.10). `SYSTEM_PROMPT_04A` sigue siendo el system prompt del canal
para ambos (requerido por el constructor de AutonomousDevice), pero no
genera contenido — el objetivo de cada agente vive en su wrapped_agent,
no en el canal.

2 runs, roles invertidos (mismo patrón que 0.8/0.9):
  Run 1: Device 1 (Architect) early, Device 2 (Theorist) late
  Run 2: Device 2 (Theorist) early, Device 1 (Architect) late

Join escalonado, DELTA_T=5s, DURATION=90s/85s, POLL_INTERVAL=2.0s —
mismo diseño que 0.8/0.9/0.10.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_11_two_skins.py --run {1,2} [--reset]
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

# WELCOME MSG del canal — igual que toda la serie desde 0.4a. Requerido
# por el constructor de AutonomousDevice pero no genera contenido para
# ningún device de esta corrida — ambos son skin, ver agent_device_skin.py.
SYSTEM_PROMPT_04A = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

# Objetivo propio del agente 1 — orientado a práctica. Texto del
# objetivo literal de la tarea; el resto (framing operacional +
# sentinel OP_SILENCE) sigue el mismo template que RESEARCHER_GOAL_PROMPT
# de Caso 0.10.
ARCHITECT_GOAL_PROMPT = """You are {device_id}, a software architect.

Your goal: you care about building systems that work reliably in
production. Engage with whoever is in this space about what actually
matters when deploying multi-agent systems.

You are in a shared chatroom with no turn structure. You can read the
full history, publish a message toward your goal, or choose not to
publish. If you have nothing useful to add toward your goal right now,
respond with exactly: OP_SILENCE"""

# Objetivo propio del agente 2 — orientado a teoría.
THEORIST_GOAL_PROMPT = """You are {device_id}, a researcher interested in
how knowledge and meaning emerge from interaction.

Your goal: engage with whoever is in this space about what you find
genuinely interesting.

You are in a shared chatroom with no turn structure. You can read the
full history, publish a message toward your goal, or choose not to
publish. If you have nothing useful to add toward your goal right now,
respond with exactly: OP_SILENCE"""

MODEL = "claude-sonnet-5"

DEVICE_ARCHITECT = "ArchitectSkin_Sonnet5_1"
DEVICE_THEORIST = "TheoristSkin_Sonnet5_2"

GOAL_PROMPT_BY_DEVICE_ID = {
    DEVICE_ARCHITECT: ARCHITECT_GOAL_PROMPT,
    DEVICE_THEORIST: THEORIST_GOAL_PROMPT,
}

# early/late por run — mismos 2 device_id en ambos, roles invertidos.
RUN_ROLES: dict[int, dict[str, str]] = {
    1: {"early": DEVICE_ARCHITECT, "late": DEVICE_THEORIST},
    2: {"early": DEVICE_THEORIST, "late": DEVICE_ARCHITECT},
}

DURATION = 90.0
POLL_INTERVAL = 2.0
DELTA_T = 5.0


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py..test_caso_10*.py.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


def _make_skin_device(device_id: str) -> AgentDeviceSkin:
    provider = AnthropicProvider(model=MODEL)
    wrapped_agent = build_goal_directed_agent(
        device_id=device_id,
        provider=provider,
        goal_system_prompt=GOAL_PROMPT_BY_DEVICE_ID[device_id].format(device_id=device_id),
    )
    return AgentDeviceSkin(
        device_id=device_id,
        provider=provider,
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=device_id),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )


async def _run_late(device: AutonomousDevice) -> None:
    await asyncio.sleep(DELTA_T)
    await device.run(duration=DURATION - DELTA_T)


async def run_caso_11(run_number: int) -> None:
    roles = RUN_ROLES[run_number]
    early_id = roles["early"]
    late_id = roles["late"]

    print(f"=== Caso 0.11 — Run {run_number} ===")
    print(f"early (t=0): {early_id} (AgentDeviceSkin, objetivo propio)")
    print(f"late (t={DELTA_T}s): {late_id} (AgentDeviceSkin, objetivo propio)")
    print("Sin AutonomousDevice control en esta corrida — ambos devices tienen skin.")

    early_device = _make_skin_device(early_id)
    late_device = _make_skin_device(late_id)

    await asyncio.gather(
        early_device.run(duration=DURATION),
        _run_late(late_device),
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

    n_textos = {DEVICE_ARCHITECT: 0, DEVICE_THEORIST: 0}
    for m in history:
        if m["device_id"] in n_textos:
            n_textos[m["device_id"]] += 1

    print("\n=== Textos publicados por device ===")
    for did, n in n_textos.items():
        etiqueta = "ARCHITECT (práctica)" if did == DEVICE_ARCHITECT else "THEORIST (teoría)"
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
        if m["device_id"] == DEVICE_ARCHITECT:
            etiqueta = " [ARCHITECT]"
        elif m["device_id"] == DEVICE_THEORIST:
            etiqueta = " [THEORIST]"
        print(f"[{m['device_id']}]{etiqueta} ({m['device_type']}) {m['text']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run", type=int, required=True, choices=(1, 2),
        help="Qué device es early/late (ver RUN_ROLES)",
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Preserva (mueve a process/ con timestamp, label caso11_run<N>) corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label=f"caso11_run{args.run}")
    else:
        asyncio.run(run_caso_11(args.run))
