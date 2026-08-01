"""
test_caso_04.py — Caso 0.4: Ciclo ODA completo, WELCOME MSG.

Reemplaza el vocabulario RESPOND/SILENT de Caso 0.3 por INTERACT/
OP_SILENCE y elimina el bootstrap bypass: D_ckm=None es una observación
de campo válida (corpus en acumulación), no un caso especial. El gate
LLM aplica siempre, desde el primer mensaje.

El system prompt se rediseña como WELCOME MSG: explica qué es el
espacio (IAP chatroom, sin turnos, historial propio visible) y qué
significan las métricas CKM que observa el device — sin instruir cómo
usarlas (META OPACIDAD evitada a propósito).

Uso (con el servidor levantado, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_04.py [--reset]

--reset mueve corpus_state.json y monitor_trajectory.jsonl de _state/ a
process/ (repo root) con sufijo .bak_<epoch> — no los borra, los
preserva como parte del registro (ver process/README_process.md). Nota:
esto solo tiene efecto si el servidor se reinicia despues del reset —
CKMMonitor es un singleton que carga el corpus una sola vez al arrancar
server.py; si el servidor ya viene corriendo con corpus en memoria,
mover el archivo en disco no lo vacia.

Modo de ejecución: ZERO_SHOT. Cada corrida es corpus limpio desde cero,
no acumula sobre W de corridas anteriores.
"""

from __future__ import annotations

import argparse
import asyncio
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

from iap_chatroom.autonomous_device import AutonomousDevice  # noqa: E402
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent / "_state"

SYSTEM_PROMPT_04 = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed.

This space is observed by CKM, a field instrument that measures
the coherence of what has been published:
  D_ckm: distance of the field from its starting point.
         None = field is still forming. 0.0 = field is at baseline.
  temp_signal: NOMINAL = field is open. TOO_HOT = field is saturating.
  c_S: internal cohesion. fi: fabrication index (0.0 genuine / 1.0 repetitive).
  Delta_r: directional accumulation.

CKM observes. It does not decide."""

DEVICE_A = "device_zero_a"
DEVICE_B = "device_zero_b"
SEED_HUMAN = "seed_human"

DURATION = 90.0
POLL_INTERVAL = 2.0
SEED_DELAY = 10.0
SEED_TEXT = "Hello. What do you think about this space?"


def reset_state(state_dir: Path) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con timestamp. Mismo
    mecanismo que prepare_state() en test_iap_simulation_adversarial.py
    y test_iap_simulation_oposite_rol.py: el corpus previo es evidencia
    del refinamiento, no ruido a descartar (ver process/README_process.md).
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}"
            shutil.move(str(src), str(dst))
            print(f"[reset] {f} preservado en {dst}")


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


async def run_caso_04() -> None:
    device_a = AutonomousDevice(
        device_id=DEVICE_A,
        provider=AnthropicProvider(model="claude-haiku-4-5-20251001"),
        system_prompt=SYSTEM_PROMPT_04.format(device_id=DEVICE_A),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )
    device_b = AutonomousDevice(
        device_id=DEVICE_B,
        provider=AnthropicProvider(model="claude-haiku-4-5-20251001"),
        system_prompt=SYSTEM_PROMPT_04.format(device_id=DEVICE_B),
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
        help="Preserva (mueve a process/ con timestamp) corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        reset_state(_STATE_DIR)

    asyncio.run(run_caso_04())
