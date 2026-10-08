"""
test_caso_05.py — Caso 0.5: System event como seed.

El canal emite automáticamente un mensaje SYSTEM cuando cada device hace
join ("{device_id} joined the channel") — ver channel.publish_system_event()
y join_channel() en mcp_server.py. No hay seed_human ni mensaje autoral
humano: el primer estímulo que puede disparar el ciclo ODA es puramente
operacional.

Variable de control respecto a 0.4a: mismo SYSTEM_PROMPT_04A (sin
explicación CKM), mismo modelo (Haiku, baseline de costo/comparabilidad
— la variable modelo ya se aisló en 0.4b), mismo ODA. Único cambio: el
seed. 0.4/0.4a/0.4b usaban "What do you think about this space?" desde
seed_human; acá no hay seed humano en absoluto, solo los join events.

Hipótesis (de REG_iap_caso_04b_v1.md): "think" apareció como nodo
aislado temprano en W en 0.4a y 0.4b porque la palabra viene del seed
("What do you *think*..."), no del vocabulario que los devices
construyen. Sin seed semántico, W debería formarse desde "joined",
"channel" y los nombres de los devices — sin ese nodo aislado.

Uso (con el servidor levantado, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_05.py [--reset]

--reset mueve corpus_state.json y monitor_trajectory.jsonl de _state/ a
process/ (repo root) con sufijo .bak_<epoch> — no los borra, los
preserva como parte del registro (ver process/README_process.md). Nota:
esto solo tiene efecto si el servidor se reinicia despues del reset —
CKMMonitor es un singleton que carga el corpus una sola vez al arrancar
server.py; si el servidor ya viene corriendo con corpus en memoria,
mover el archivo en disco no lo vacia.

Modo de ejecución: ZERO_SHOT. Corpus limpio desde cero, sin acumular
sobre W de corridas anteriores (incluyendo Caso 0.4, 0.4a, 0.4b).
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

# Idéntico a SYSTEM_PROMPT_04A de Caso 0.4a — sin bloque CKM. Aísla solo
# la variable seed (ver docstring del módulo).
SYSTEM_PROMPT_04A = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

MODEL = "claude-haiku-4-5-20251001"

DEVICE_A = "device_zero_a"
DEVICE_B = "device_zero_b"

DURATION = 90.0
POLL_INTERVAL = 2.0
# Sin SEED_DELAY / SEED_TEXT / SEED_HUMAN — el primer evento del canal
# es el join event SYSTEM emitido automáticamente por join_channel().


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


async def run_caso_05() -> None:
    device_a = AutonomousDevice(
        device_id=DEVICE_A,
        provider=AnthropicProvider(model=MODEL),
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_A),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )
    device_b = AutonomousDevice(
        device_id=DEVICE_B,
        provider=AnthropicProvider(model=MODEL),
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_B),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )

    await asyncio.gather(
        device_a.run(duration=DURATION),
        device_b.run(duration=DURATION),
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

    asyncio.run(run_caso_05())
