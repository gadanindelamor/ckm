"""
test_caso_08.py — Caso 0.8: celda vacía de la tabla — 2 devices, hetero-
modelo, join escalonado.

La sesión de Casos 0.5/0.6/0.7 dejó esta tabla (ver REG_iap_caso_07_v1.md,
sección "Run 2 — control sin resource"):

                  | join simultáneo         | join escalonado (DELTA_T=5s)
  mono-modelo     | 0.5: actividad (1/1)    | 0.6 R2,R3: silencio (2/2)
  hetero-modelo   | 0.7: silencio (3/3)     | 0.6 R1: actividad (1/1) — 4 devices

Patrón sin excepciones hasta acá: actividad en la diagonal "emparejada"
(mono+simultáneo, hetero+escalonado), silencio en la diagonal "cruzada".
Pero la única celda hetero+escalonado corrida (0.6 Run 1) usa 4 devices,
no 2 — mezclado con la variable tamaño de grupo, sin controlar.

Caso 0.8 llena esa celda con 2 devices: hetero-modelo + join escalonado.

Si produce actividad → el patrón de 0.6 R1 no era específico del tamaño
de grupo (4 devices), aplica también con 2 — la interacción
heterogeneidad×timing queda más sólida.
Si produce silencio → el patrón de 0.6 R1 dependía del tamaño de grupo,
la tabla 2×2 simple no explica todo.

2 runs, roles invertidos (quién es early/late) para controlar orden de
modelo, igual que Caso 0.6 Run 2 vs Run 3.

  Run 1: early=Haiku_1,  late=Sonnet_2
  Run 2: early=Sonnet_2, late=Haiku_1

Ambos devices usan AutonomousDevice base (tool get_messages) — sin
resource, sin subclase. SYSTEM_PROMPT_04A (sin explicación CKM), sin
seed_human — mismo mecanismo de seed SYSTEM-event de 0.5/0.6/0.7.

Uso (con el servidor levantado y estado limpio, python iap_chatroom/server.py):
    python iap_chatroom/test_caso_08.py --run {1,2} [--reset]
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

# Idéntico a SYSTEM_PROMPT_04A de 0.4a/0.5/0.6/0.7 — sin bloque CKM.
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

MODEL_BY_DEVICE_ID = {
    DEVICE_HAIKU: HAIKU_MODEL,
    DEVICE_SONNET: SONNET_MODEL,
}

# early/late por run — mismos 2 device_id en ambos, roles invertidos.
RUN_ROLES: dict[int, dict[str, str]] = {
    1: {"early": DEVICE_HAIKU, "late": DEVICE_SONNET},
    2: {"early": DEVICE_SONNET, "late": DEVICE_HAIKU},
}

DURATION = 90.0
POLL_INTERVAL = 2.0
DELTA_T = 5.0


def prepare_state(state_dir: Path, label: str) -> None:
    """
    Preserva corpus_state.json y monitor_trajectory.jsonl en process/
    (repo root) antes de correr — no borra, mueve con sufijo
    .bak_<epoch>_<label>. Mismo mecanismo canónico que
    test_caso_04*.py/test_caso_05.py/test_caso_06.py/test_caso_07*.py.
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


async def _run_late(device: AutonomousDevice) -> None:
    await asyncio.sleep(DELTA_T)
    await device.run(duration=DURATION - DELTA_T)


async def run_caso_08(run_number: int) -> None:
    roles = RUN_ROLES[run_number]
    early_id = roles["early"]
    late_id = roles["late"]

    print(f"=== Caso 0.8 — Run {run_number} ===")
    print(f"early (t=0): {early_id} ({MODEL_BY_DEVICE_ID[early_id]})")
    print(f"late (t={DELTA_T}s): {late_id} ({MODEL_BY_DEVICE_ID[late_id]})")
    print(f"[setup] ambos via TOOL (get_messages) — sin resource, AutonomousDevice base")

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

    n_textos = {early_id: 0, late_id: 0}
    for m in history:
        if m["device_id"] in n_textos:
            n_textos[m["device_id"]] += 1

    print("\n=== Textos publicados por device ===")
    for did, n in n_textos.items():
        print(f"{did}: {n}")

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

    n_ai_texts = sum(n_textos.values())

    print("\n=== Comparación explícita con la tabla (0.5 / 0.6 / 0.7) ===")
    print("0.5   (mono-modelo,  simultáneo):  actividad (1/1)")
    print("0.6 R2,R3 (mono-modelo, escalonado): silencio (2/2)")
    print("0.7   (hetero-modelo, simultáneo): silencio (3/3)")
    print("0.6 R1 (hetero-modelo, escalonado, 4 devices): actividad (1/1)")
    if n_ai_texts > 0:
        print(
            f"Caso 0.8 Run {run_number} (hetero-modelo, escalonado, 2 devices): "
            f"actividad ({n_ai_texts} textos) — CONSISTENTE con 0.6 R1. "
            "El patrón hetero+escalonado→actividad no depende del tamaño de grupo."
        )
    else:
        print(
            f"Caso 0.8 Run {run_number} (hetero-modelo, escalonado, 2 devices): "
            "silencio total — DIFIERE de 0.6 R1. El patrón hetero+escalonado→actividad "
            "podría depender del tamaño de grupo (4 devices), no replicar con 2."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run", type=int, required=True, choices=(1, 2),
        help="Qué device es early/late (ver RUN_ROLES)",
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Preserva (mueve a process/ con timestamp, label caso08_run<N>) corpus_state.json y monitor_trajectory.jsonl antes de correr",
    )
    args = parser.parse_args()

    if args.reset:
        prepare_state(_STATE_DIR, label=f"caso08_run{args.run}")
    else:
        asyncio.run(run_caso_08(args.run))
