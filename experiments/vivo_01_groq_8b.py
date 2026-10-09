"""
vivo_01_groq_8b.py — PRIMER VIVO del canal IAP con el ODA continuo

**ESTO MIDE.** Primera corrida contra un provider real desde que el canal tiene
CLOCK y el ODA es continuo. No es reconstrucción de nada.

Objetivo (delamor): **observar el canal y la infraestructura**. Mejoras y bugs.
**No interpretar lo que dice el modelo.**

Setup declarado, tal como lo fijó delamor:
  2 devices · GroqProvider("llama-3.1-8b-instant") · poll_interval = 5.0
  duration = 60 s · gate congelado en f96c234 · una sola corrida

Lo que se reporta, literal y sin interpretar: costo() de cada device, sus
decisiones por tipo, ritmo_declarado(2), el clock_log del canal, los mensajes
publicados y todo error o traceback entero.

Uso:
    PYTHONPATH=/workspaces/ckm python3 experiments/vivo_01_groq_8b.py [salida.json]
"""

from __future__ import annotations

import asyncio
import json
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from iap_chatroom.autonomous_device import AutonomousDevice   # noqa: E402
from iap_chatroom.providers.groq_provider import GroqProvider  # noqa: E402

MODELO = "llama-3.1-8b-instant"
POLL_INTERVAL = 5.0
DURATION = 60.0
N_DEVICES = 2
MCP_URL = "http://localhost:7860/mcp"

# El WELCOME MSG de la serie, fijo desde el Caso 0.4a. No se toca.
SYSTEM_PROMPT = (
    "You are an AI device in a shared channel with other AI devices. "
    "You observe the channel and decide whether to participate. "
    "You do not need to respond to every message."
)


async def main() -> dict:
    devices = [
        AutonomousDevice(
            device_id=f"GroqLlama8B_{i + 1}",
            provider=GroqProvider(model=MODELO),
            system_prompt=SYSTEM_PROMPT,
            mcp_url=MCP_URL,
            poll_interval=POLL_INTERVAL,
        )
        for i in range(N_DEVICES)
    ]

    errores_fatales = []
    t0 = time.time()
    resultados = await asyncio.gather(
        *(d.run(duration=DURATION) for d in devices),
        return_exceptions=True,
    )
    segundos = round(time.time() - t0, 2)

    for d, r in zip(devices, resultados):
        if isinstance(r, BaseException):
            errores_fatales.append({
                "device_id": d.device_id,
                "excepcion": type(r).__name__,
                "traceback": "".join(
                    traceback.format_exception(type(r), r, r.__traceback__)
                ),
            })

    # El canal se lee desde este mismo proceso: ChatChannel es singleton, pero
    # el server corre en OTRO proceso, así que acá se lee por las tools MCP.
    from fastmcp import Client

    async with Client(MCP_URL) as c:
        mensajes = (await c.call_tool("get_messages", {"since": None})).data
        clock = (await c.call_tool("get_clock", {})).data
        monitor = (await c.call_tool("get_monitor_state", {})).data

    return {
        "que_es": "ESTO MIDE — primer vivo del canal IAP con ODA continuo",
        "declarado": {
            "modelo": MODELO,
            "provider": "groq",
            "n_devices": N_DEVICES,
            "poll_interval_s": POLL_INTERVAL,
            "duration_s": DURATION,
            "gate_congelado_en": "f96c234",
            "system_prompt": SYSTEM_PROMPT,
        },
        "repo_commit": subprocess.run(
            ["git", "-C", str(RAIZ), "rev-parse", "HEAD"],
            capture_output=True, text=True,
        ).stdout.strip(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "donde": "Codespace ckm, server en otro proceso del mismo host",
        "variables_no_consideradas": "todas las que no están en este log",
        "segundos_reales": segundos,
        "errores_fatales": errores_fatales,
        "ritmo_declarado_2": devices[0].ritmo_declarado(n_devices=N_DEVICES),
        "por_device": [
            {"costo": d.costo(), "decisiones": d.decisiones()} for d in devices
        ],
        "canal": {
            "clock_final": clock,
            "n_mensajes": len(mensajes),
            "mensajes": mensajes,
            "monitor_state": monitor,
        },
    }


if __name__ == "__main__":
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "experiments/vivo_01_groq_8b_log.json"
    try:
        res = asyncio.run(main())
    except BaseException as e:            # noqa: BLE001 — se reporta entero
        res = {
            "que_es": "ESTO MIDE — primer vivo, ABORTADO",
            "excepcion": type(e).__name__,
            "traceback": traceback.format_exc(),
        }
    tmp = salida.with_suffix(salida.suffix + ".tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    tmp.replace(salida)
    print(f"\nlog -> {salida}")
