"""
test_caso_12_groq_research_skin.py — Caso 0.12: mismo diseño de Caso
0.11 (dos AgentDeviceSkin, sin control, join escalonado, roles
invertidos), pero uno de los dos skins deja de ser un wrapped_agent
conversacional sobre Anthropic y pasa a ser el AutonomousResearchAgent
(Groq + planificación + búsqueda DuckDuckGo,
iap_chatroom/groq_research_agent.py) implementado esta sesión.

Ver iap_chatroom/TASK_caso_12.md para el detalle completo de la tarea,
el confound explícito de esta corrida (provider + mecanismo + posible
disponibilidad de búsqueda cambian juntos respecto a 0.11) y la
verificación pendiente de duckduckgo-search antes de correr.

Se reemplaza ArchitectSkin (orientación práctica) — se mantiene
TheoristSkin (orientación teórica) sin cambios respecto a 0.11.

  GroqResearchSkin_Llama_1 → AgentDeviceSkin + build_autonomous_groq_agent
                             (nuevo). Objetivo de investigación fijo,
                             NO lee el contenido del canal para decidir
                             qué publicar (ver docstring de
                             build_autonomous_groq_agent, "Nota de diseño").
  TheoristSkin_Sonnet5_2   → AgentDeviceSkin + build_goal_directed_agent
                             (sin cambios vs 0.11). Sí lee el canal y
                             responde conversacionalmente.

2 runs, roles invertidos (mismo patrón que 0.8/0.9/0.10/0.11):
  Run 1: GroqResearchSkin_Llama_1 early, TheoristSkin_Sonnet5_2 late
  Run 2: TheoristSkin_Sonnet5_2 early, GroqResearchSkin_Llama_1 late

Join escalonado, DELTA_T=5s, DURATION=90s/85s, POLL_INTERVAL=2.0s —
idéntico a 0.11.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_12_groq_research_skin.py --run {1,2} [--reset]
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
from iap_chatroom.groq_research_agent import (  # noqa: E402
    build_autonomous_groq_agent,
)
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402
from iap_chatroom.providers.groq_provider import GroqProvider  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent / "_state"
_TRAJECTORY_PATH = _STATE_DIR / "monitor_trajectory.jsonl"

# WELCOME MSG del canal — igual que toda la serie desde 0.4a. Requerido
# por el constructor de AutonomousDevice pero no genera contenido para
# ningún device de esta corrida — ambos son skin.
SYSTEM_PROMPT_04A = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

# Objetivo del research agent — mismo tema que ArchitectSkin en 0.11
# (práctica de despliegue de sistemas multiagente), reformulado como
# objetivo de investigación en vez de prompt conversacional, para
# mantener la comparación con 0.11 lo más controlada posible dado que
# el mecanismo cambia (ver TASK_caso_12.md, "Confound explícito").
GROQ_RESEARCH_OBJECTIVE = (
    "Investigar qué importa al desplegar sistemas multiagente en "
    "producción: fallos, coordinación entre agentes, observabilidad."
)

# Objetivo propio de TheoristSkin — idéntico a 0.11, sin cambios.
THEORIST_GOAL_PROMPT = """You are {device_id}, a researcher interested in
how knowledge and meaning emerge from interaction.

Your goal: engage with whoever is in this space about what you find
genuinely interesting.

You are in a shared chatroom with no turn structure. You can read the
full history, publish a message toward your goal, or choose not to
publish. If you have nothing useful to add toward your goal right now,
respond with exactly: OP_SILENCE"""

SONNET_MODEL = "claude-sonnet-5"
GROQ_MODEL = "llama-3.3-70b-versatile"

DEVICE_GROQ_RESEARCH = "GroqResearchSkin_Llama_1"
DEVICE_THEORIST = "TheoristSkin_Sonnet5_2"

# early/late por run — mismos 2 device_id en ambos, roles invertidos.
RUN_ROLES: dict[int, dict[str, str]] = {
    1: {"early": DEVICE_GROQ_RESEARCH, "late": DEVICE_THEORIST},
    2: {"early": DEVICE_THEORIST, "late": DEVICE_GROQ_RESEARCH},
}

DURATION = 90.0
POLL_INTERVAL = 2.0
DELTA_T = 5.0


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py..test_caso_11*.py.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


def _make_theorist_device() -> AgentDeviceSkin:
    provider = AnthropicProvider(model=SONNET_MODEL)
    wrapped_agent = build_goal_directed_agent(
        device_id=DEVICE_THEORIST,
        provider=provider,
        goal_system_prompt=THEORIST_GOAL_PROMPT.format(device_id=DEVICE_THEORIST),
    )
    return AgentDeviceSkin(
        device_id=DEVICE_THEORIST,
        provider=provider,
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_THEORIST),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )


def _make_groq_research_device() -> AgentDeviceSkin:
    provider = GroqProvider(model=GROQ_MODEL)
    wrapped_agent = build_autonomous_groq_agent(
        device_id=DEVICE_GROQ_RESEARCH,
        objetivo=GROQ_RESEARCH_OBJECTIVE,
        provider=provider,
    )
    return AgentDeviceSkin(
        device_id=DEVICE_GROQ_RESEARCH,
        provider=provider,
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_GROQ_RESEARCH),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
        wrapped_agent=wrapped_agent,
    )


def _make_device(device_id: str) -> AgentDeviceSkin:
    if device_id == DEVICE_GROQ_RESEARCH:
        return _make_groq_research_device()
    return _make_theorist_device()


async def _run_late(device: AutonomousDevice) -> None:
    await asyncio.sleep(DELTA_T)
    await device.run(duration=DURATION - DELTA_T)


async def run_caso_12(run_number: int) -> None:
    roles = RUN_ROLES[run_number]
    early_id = roles["early"]
    late_id = roles["late"]

    print(f"=== Caso 0.12 — Run {run_number} ===")
    print(f"early (t=0): {early_id}")
    print(f"late (t={DELTA_T}s): {late_id}")
    print(
        "Sin AutonomousDevice control — ambos devices tienen skin, "
        "mecanismos distintos (research agent no lee el canal; "
        "theorist sí)."
    )

    early_device = _make_device(early_id)
    late_device = _make_device(late_id)

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

    n_textos = {DEVICE_GROQ_RESEARCH: 0, DEVICE_THEORIST: 0}
    for m in history:
        if m["device_id"] in n_textos:
            n_textos[m["device_id"]] += 1

    print("\n=== Textos publicados por device ===")
    for did, n in n_textos.items():
        etiqueta = (
            "GROQ-RESEARCH (no lee canal)"
            if did == DEVICE_GROQ_RESEARCH
            else "THEORIST (conversacional)"
        )
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
        if m["device_id"] == DEVICE_GROQ_RESEARCH:
            etiqueta = " [GROQ-RESEARCH]"
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
        help=(
            "Preserva (mueve a process/ con timestamp, label "
            "caso12_run<N>) corpus_state.json y monitor_trajectory.jsonl "
            "antes de correr"
        ),
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label=f"caso12_run{args.run}")
    else:
        asyncio.run(run_caso_12(args.run))
