"""
test_caso_06.py — Caso 0.6: join escalonado, 4 devices, early/late.

Variable de control respecto a 0.5: mismo SYSTEM_PROMPT_04A (sin
explicación CKM), mismo ciclo ODA, mismo mecanismo de seed (join event
SYSTEM, sin seed_human). Lo que cambia es la dinámica de join: 4
devices en vez de 2, repartidos en un grupo "early" (join en t=0) y un
grupo "late" (join en t=DELTA_T), en vez de los 2 devices simultáneos
de 0.4/0.4a/0.4b/0.5.

Tres runs, mismos 4 device_id en los tres (naming fijo — ver
MODEL_BY_DEVICE_ID), pero la asignación early/late cambia:

  Run 1: early=[Haiku_1, Sonnet_2]   late=[Haiku_3, Sonnet_4]   (grupos mixtos)
  Run 2: early=[Haiku_1, Haiku_3]    late=[Sonnet_2, Sonnet_4]  (Haiku primero)
  Run 3: early=[Sonnet_2, Sonnet_4]  late=[Haiku_1, Haiku_3]    (Sonnet primero)

Duración: DURATION=90s es la ventana total del experimento (wall-clock
desde el join del grupo early), no 90s por device. El grupo early corre
`AutonomousDevice.run(duration=DURATION)` desde t=0; el grupo late corre
`run(duration=DURATION - DELTA_T)` desde t=DELTA_T — así los 4 devices
cierran en el mismo instante de pared (t=90s), dando un corte
comparable entre grupos en vez de que "late" quede corriendo 5s de más.

Uso (con el servidor levantado y con estado ya limpio para este run,
python iap_chatroom/server.py):
    python iap_chatroom/test_caso_06.py --run {1,2,3}

    python iap_chatroom/test_caso_06.py --run N --reset
        Solo preserva (mueve a process/ con label caso06_runN) el estado
        actual de _state/ y termina — no corre el experimento. Pensado
        para usarse ANTES de reiniciar el servidor, no junto con la
        corrida real (el reinicio del servidor es responsabilidad del
        orquestador — CKMMonitor es singleton, un --reset con el server
        ya corriendo no vacía su corpus en memoria).

Modo de ejecución: ZERO_SHOT por run. autonomous_device.py, channel.py,
mcp_server.py y server.py no se modifican para este caso — ya exponen
todo lo necesario (device_type SYSTEM, filtro ODA ampliado, ciclo ODA
sin bootstrap bypass) desde Caso 0.5.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import sys
import time
from collections import Counter
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

# Idéntico a SYSTEM_PROMPT_04A de 0.4a/0.5 — sin bloque CKM. Mantiene
# esa variable constante; lo único que cambia en Caso 0.6 es el join.
SYSTEM_PROMPT_04A = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

HAIKU_MODEL = "claude-haiku-4-5-20251001"
SONNET_MODEL = "claude-sonnet-5"

DEVICE_1 = "ClaudeHaiku_4-5-20251001_1"
DEVICE_2 = "ClaudeSonnet_5_2"
DEVICE_3 = "ClaudeHaiku_4-5-20251001_3"
DEVICE_4 = "ClaudeSonnet_5_4"

MODEL_BY_DEVICE_ID = {
    DEVICE_1: HAIKU_MODEL,
    DEVICE_2: SONNET_MODEL,
    DEVICE_3: HAIKU_MODEL,
    DEVICE_4: SONNET_MODEL,
}

# early/late por run — mismos 4 device_id en los tres, cambia el grupo.
RUN_GROUPS: dict[int, dict[str, list[str]]] = {
    1: {"early": [DEVICE_1, DEVICE_2], "late": [DEVICE_3, DEVICE_4]},
    2: {"early": [DEVICE_1, DEVICE_3], "late": [DEVICE_2, DEVICE_4]},
    3: {"early": [DEVICE_2, DEVICE_4], "late": [DEVICE_1, DEVICE_3]},
}

DURATION = 90.0
POLL_INTERVAL = 2.0
DELTA_T = 5.0
MIN_TEXTS = 3  # documental — el umbral real vive en CKMMonitor/CorpusService, no se toca acá


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py/test_caso_05.py (a su vez heredado de
    prepare_state() en test_iap_simulation_adversarial.py).
    """
    process_dir = _REPO_ROOT / "process"
    process_dir.mkdir(exist_ok=True)
    for f in ["corpus_state.json", "monitor_trajectory.jsonl"]:
        src = state_dir / f
        if src.exists():
            dst = process_dir / f"{f}.bak_{int(time.time())}_{label}"
            shutil.move(str(src), str(dst))
            print(f"[prepare_state] {f} preservado en {dst}")


def _make_device(device_id: str) -> AutonomousDevice:
    return AutonomousDevice(
        device_id=device_id,
        provider=AnthropicProvider(model=MODEL_BY_DEVICE_ID[device_id]),
        system_prompt=SYSTEM_PROMPT_04A.format(device_id=device_id),
        mcp_url=MCP_URL,
        poll_interval=POLL_INTERVAL,
    )


async def _run_late_group(devices: list[AutonomousDevice]) -> None:
    await asyncio.sleep(DELTA_T)
    await asyncio.gather(*[d.run(duration=DURATION - DELTA_T) for d in devices])


async def run_caso_06(run_number: int) -> None:
    groups = RUN_GROUPS[run_number]
    early_devices = [_make_device(did) for did in groups["early"]]
    late_devices = [_make_device(did) for did in groups["late"]]

    print(f"=== Caso 0.6 — Run {run_number} ===")
    print(f"early (t=0): {groups['early']}")
    print(f"late (t={DELTA_T}s): {groups['late']}")

    await asyncio.gather(
        *[d.run(duration=DURATION) for d in early_devices],
        _run_late_group(late_devices),
    )

    async with Client(MCP_URL) as client:
        firma_result = await client.call_tool("get_firma", {})
        firma: Optional[dict] = firma_result.data

        # since=0.0 (no None) — get_messages(since=None) trunca a los
        # últimos 20; con 4 devices activos el corpus puede superar eso.
        history_result = await client.call_tool("get_messages", {"since": 0.0})
        history: list[dict] = history_result.data

    print("\n=== Firma_CKM (cierre) ===")
    if firma is None:
        print("Firma_CKM: None (corpus aun en acumulacion)")
    else:
        for field in ("w_sha", "d_ckm", "temp_signal", "n_agentes", "timestamp", "delta_sha"):
            print(f"{field}: {firma.get(field)}")

    texts_by_device = Counter(
        m["device_id"] for m in history if m["device_id"] != "system"
    )
    print("\n=== Textos publicados por device ===")
    for device_id in groups["early"] + groups["late"]:
        print(f"{device_id}: {texts_by_device.get(device_id, 0)}")

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
        print(f"[{m['device_id']}] ({m['device_type']}) {m['text']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run", type=int, required=True, choices=(1, 2, 3),
        help="Configuración early/late a correr (ver RUN_GROUPS)",
    )
    parser.add_argument(
        "--reset", action="store_true",
        help=(
            "Solo preserva _state/ actual en process/ (label caso06_run<N>) "
            "y termina. Correr antes de reiniciar el servidor, no junto "
            "con la corrida real."
        ),
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label=f"caso06_run{args.run}")
    else:
        asyncio.run(run_caso_06(args.run))
