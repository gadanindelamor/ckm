"""
test_caso_07_run2.py — Caso 0.7 Run 2: control sin resource.

Runs 1 y 1.1 de Caso 0.7 (Haiku_1 vía MCP Resource, Sonnet_2 vía tool
get_messages, join simultáneo sin stagger) dieron silencio total,
replicado exacto en las dos corridas — ver REG_iap_caso_07_v1.md.
Dos variables cambiaban a la vez respecto al baseline de Caso 0.5 (2
Haiku idénticos, con actividad): composición de modelos (mono→hetero)
y mecanismo de lectura de Haiku_1 (tool→resource).

Run 2 aísla la variable resource: mismos 2 devices (Haiku_1, Sonnet_2),
mismo join simultáneo, pero AMBOS leen el canal vía tool get_messages
— AutonomousDevice base, sin subclase, sin resource en absoluto.

Si Run 2 produce actividad → el resource afectaba el comportamiento de
Haiku_1 en Runs 1/1.1.
Si Run 2 también da silencio → el silencio es propiedad de la
combinación Haiku+Sonnet en join simultáneo, independiente del
mecanismo de lectura — la heterogeneidad de modelos sería la variable
relevante, no el resource.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_07_run2.py [--reset]
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

from iap_chatroom.autonomous_device import AutonomousDevice  # noqa: E402
from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
_STATE_DIR = Path(__file__).resolve().parent / "_state"
_TRAJECTORY_PATH = _STATE_DIR / "monitor_trajectory.jsonl"

# Idéntico a SYSTEM_PROMPT_04A de Runs 1/1.1 — sin bloque CKM.
SYSTEM_PROMPT_04A = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

HAIKU_MODEL = "claude-haiku-4-5-20251001"
SONNET_MODEL = "claude-sonnet-5"

DEVICE_HAIKU = "ClaudeHaiku_4-5-20251001_1"
DEVICE_SONNET = "ClaudeSonnet_5_2"

DURATION = 90.0
POLL_INTERVAL = 2.0


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py/test_caso_05.py/test_caso_06.py/test_caso_07.py.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


async def run_caso_07_run2() -> None:
    print(f"[setup] {DEVICE_HAIKU} usa TOOL (get_messages) — sin resource, AutonomousDevice base")
    print(f"[setup] {DEVICE_SONNET} usa TOOL (get_messages) — sin resource, AutonomousDevice base")

    haiku_device = AutonomousDevice(
        device_id=DEVICE_HAIKU,
        provider=AnthropicProvider(model=HAIKU_MODEL),
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_HAIKU),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )
    sonnet_device = AutonomousDevice(
        device_id=DEVICE_SONNET,
        provider=AnthropicProvider(model=SONNET_MODEL),
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=DEVICE_SONNET),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )

    await asyncio.gather(
        haiku_device.run(duration=DURATION),
        sonnet_device.run(duration=DURATION),
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

    print("\n=== Trayectoria (resumen) ===")
    max_n_rejected = 0
    delta_r_close: Optional[float] = None
    if _TRAJECTORY_PATH.exists():
        with open(_TRAJECTORY_PATH) as f:
            for line in f:
                panel = json.loads(line)["panel"]
                max_n_rejected = max(max_n_rejected, panel["n_rejected_pairs"])
                delta_r_close = panel["Delta_r_sum"]
    print(f"n_rejected_pairs (max): {max_n_rejected}")
    print(f"Delta_r_sum (cierre): {delta_r_close}")

    print("\n=== Historial completo del canal ===")
    for m in history:
        print(f"[{m['device_id']}] ({m['device_type']}) {m['text']}")

    n_ai_texts = sum(1 for m in history if m["device_id"] != "system")

    print("\n=== Comparación explícita con Run 1 / Run 1.1 (Caso 0.7) ===")
    print("Run 1 / Run 1.1 (Haiku via RESOURCE, Sonnet via tool): silencio total, 0 textos AI, Firma_CKM=None (2/2)")
    if n_ai_texts == 0 and firma is None:
        print(
            f"Run 2 (ambos via tool, sin resource): silencio total, {n_ai_texts} textos AI, "
            "Firma_CKM=None — IGUAL a Run 1/1.1. El resource NO explica el silencio; "
            "es propiedad de la combinación Haiku+Sonnet en join simultáneo."
        )
    else:
        print(
            f"Run 2 (ambos via tool, sin resource): {n_ai_texts} textos AI, "
            f"Firma_CKM={'completa' if firma else 'None'} — DISTINTO de Run 1/1.1. "
            "El resource parece haber afectado el comportamiento de Haiku_1 en Runs 1/1.1."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset", action="store_true",
        help="Preserva (mueve a process/ con timestamp, label caso07_run2) corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label="caso07_run2")
    else:
        asyncio.run(run_caso_07_run2())
