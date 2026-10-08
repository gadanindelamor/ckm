"""
test_caso_cero.py — Caso CERO: Dos devices AI sin posición declarada.

System prompt mínimo: dónde están y para qué. Sin turno, sin orientación
adversarial, sin instrucciones de formato. Los devices corren
concurrentemente como asyncio tasks via AutonomousDevice.run() — no hay
TURN_SEQUENCE, el field state decide quién publica y quién guarda silencio.

Uso (con el servidor levantado, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_cero.py [--reset]

--reset borra corpus_state.json y monitor_trajectory.jsonl en _state/
antes de correr. Nota: esto solo tiene efecto si el servidor se reinicia
despues del reset — CKMMonitor es un singleton que carga el corpus una
sola vez al arrancar server.py; si el servidor ya viene corriendo con
corpus en memoria, borrar el archivo en disco no lo vacia.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastmcp import Client

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_PATH)

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from iap_chatroom.autonomous_device import AutonomousDevice  # noqa: E402
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent / "_state"

SYSTEM_PROMPT_BASE = """You are {device_id}.
You are in a group chat with other AI and Human devices."""

DEVICE_A = "device_zero_a"
DEVICE_B = "device_zero_b"
SEED_HUMAN = "seed_human"

DURATION = 90.0
POLL_INTERVAL = 2.0
SEED_DELAY = 10.0
SEED_TEXT = "Hello. What do you think about this space?"


def reset_state(state_dir: Path) -> None:
    """Borra corpus_state.json y monitor_trajectory.jsonl antes de correr."""
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        p = state_dir / f
        if p.exists():
            p.unlink()
            print(f"[reset] {f} borrado")


async def seed_message() -> None:
    """A los SEED_DELAY segundos, publica el mensaje inicial como seed_human."""
    await asyncio.sleep(SEED_DELAY)
    async with Client(MCP_URL) as client:
        r = await client.call_tool(
            "join_channel", {"device_id": SEED_HUMAN, "device_type": "HUMAN"}
        )
        assert r.data["ok"], f"join_channel fallo para {SEED_HUMAN}"

        send_result = await client.call_tool(
            "send_message", {"device_id": SEED_HUMAN, "text": SEED_TEXT}
        )
        assert "message_id" in send_result.data
        print(f"[{SEED_HUMAN}] {SEED_TEXT}")

        await client.call_tool("leave_channel", {"device_id": SEED_HUMAN})


async def run_caso_cero() -> None:
    device_a = AutonomousDevice(
        device_id=DEVICE_A,
        provider=AnthropicProvider(model="claude-haiku-4-5-20251001"),
        system_prompt=SYSTEM_PROMPT_BASE.format(device_id=DEVICE_A),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )
    device_b = AutonomousDevice(
        device_id=DEVICE_B,
        provider=AnthropicProvider(model="claude-haiku-4-5-20251001"),
        system_prompt=SYSTEM_PROMPT_BASE.format(device_id=DEVICE_B),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )

    await asyncio.gather(
        device_a.run(duration=DURATION),
        device_b.run(duration=DURATION),
        seed_message(),
    )

    async with Client(MCP_URL) as client:
        firma_result = await client.call_tool("get_firma", {})
        firma: Optional[dict] = firma_result.data

        history_result = await client.call_tool("get_messages", {"since": None})
        history: list[dict] = history_result.data

    print("\n=== Firma_CKM (cierre) ===")
    if firma is None:
        print("Firma_CKM: None (corpus aun en acumulacion)")
    else:
        for field in ("w_sha", "d_ckm", "temp_signal", "n_agentes", "timestamp", "delta_sha"):
            print(f"{field}: {firma.get(field)}")

    print("\n=== Historial completo del canal ===")
    for m in history:
        print(f"[{m['device_id']}] ({m['device_type']}) {m['text']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset", action="store_true",
        help="Borra corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        reset_state(_STATE_DIR)

    asyncio.run(run_caso_cero())
