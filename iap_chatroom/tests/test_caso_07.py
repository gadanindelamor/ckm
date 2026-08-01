"""
test_caso_07.py — Caso 0.7: MCP Resource vs tool para leer el canal.

2 devices, mismo SYSTEM_PROMPT_04A que 0.4a/0.5/0.6 (sin explicación
CKM), mismo mecanismo de seed (join event SYSTEM, sin seed_human).
Variable de control: cómo cada device lee el historial del canal en la
fase _observe() del ciclo ODA.

  ClaudeHaiku_4-5-20251001_1 → lee vía MCP Resource (iap://canal/mensajes)
  ClaudeSonnet_5_2           → lee vía tool get_messages (control, sin cambios)

fastmcp instalado: 3.4.4 (pip show fastmcp). Verificado antes de escribir
este script: `Client` no expone subscribe/subscribe_resource, y `FastMCP`
(servidor) no expone un helper público para notificaciones
resource_updated — ver docstring de canal_mensajes() en mcp_server.py.
Sin push disponible en esta versión: Haiku_1 hace polling sobre el
resource (client.read_resource()) en cada ciclo ODA, igual cadencia que
el polling normal de mensajes nuevos (POLL_INTERVAL).

NO se modifica autonomous_device.py. `ResourceReadingDevice` es una
subclase que sobreescribe únicamente `_observe()` — el resto del ciclo
ODA (_decide, _interact), el polling de mensajes nuevos y join/leave en
run() quedan heredados sin cambios.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_07.py [--reset]
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

CANAL_RESOURCE_URI = "iap://canal/mensajes"

# Idéntico a SYSTEM_PROMPT_04A de 0.4a/0.5/0.6 — sin bloque CKM.
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


class ResourceReadingDevice(AutonomousDevice):
    """
    Variante de AutonomousDevice para Caso 0.7: en _observe(), lee el
    historial del canal vía MCP Resource (iap://canal/mensajes) en vez
    de la tool get_messages. get_monitor_state y el polling de mensajes
    nuevos en run() (heredado, sin override) no cambian.
    """

    async def _observe(self, client: Client, message: dict) -> dict:
        print(f"[{self.device_id}] _observe via RESOURCE ({CANAL_RESOURCE_URI})")

        field_result = await client.call_tool("get_monitor_state", {})
        field_state = field_result.data

        resource_result = await client.read_resource(CANAL_RESOURCE_URI)
        history = json.loads(resource_result[0].text)

        return {
            "field": field_state,
            "history": history,
            "trigger": message,
            "own_recent": [
                m for m in history[-20:] if m.get("device_id") == self.device_id
            ],
        }


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py/test_caso_05.py/test_caso_06.py.
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


async def run_caso_07() -> None:
    print(f"[setup] {DEVICE_HAIKU} usa RESOURCE ({CANAL_RESOURCE_URI}) para leer el canal")
    print(f"[setup] {DEVICE_SONNET} usa TOOL (get_messages) para leer el canal — control")

    haiku_device = ResourceReadingDevice(
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset", action="store_true",
        help="Preserva (mueve a process/ con timestamp, label caso07) corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label="caso07")
    else:
        asyncio.run(run_caso_07())
