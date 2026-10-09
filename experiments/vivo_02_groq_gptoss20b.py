"""
vivo_02_groq_gptoss20b.py — VIVO 02 del canal IAP con el ODA continuo

**ESTO MIDE.** Primera corrida contra un provider real desde que el canal tiene
CLOCK y el ODA es continuo. No es reconstrucción de nada.

Objetivo (delamor): **observar el canal y la infraestructura**. Mejoras y bugs.
**No interpretar lo que dice el modelo.**

Setup declarado, tal como lo fijó delamor:
  2 devices · GroqProvider("openai/gpt-oss-20b") · poll_interval = 5.0
  duration = 60 s · gate congelado en f96c234 · una sola corrida

**Por qué este modelo, declarado.** El vivo 01 falló con 404: el modelo que se
había elegido no existe en la cuenta. Los 11 modelos que la cuenta expone son:

  allam-2-7b · canopylabs/orpheus-arabic-saudi · canopylabs/orpheus-v1-english
  meta-llama/llama-prompt-guard-2-22m · meta-llama/llama-prompt-guard-2-86m
  openai/gpt-oss-120b · openai/gpt-oss-20b · openai/gpt-oss-safeguard-20b
  qwen/qwen3.8-27b · whisper-large-v3 · whisper-large-v3-turbo

`llama-3.3-70b-versatile` **no está**. Los únicos con "llama" son los
`prompt-guard`, que son **clasificadores, no modelos de chat**: no contestan un
gate con una palabra. La regla decía "el primero con llama o gpt-oss", y la
lectura literal daría un prompt-guard (no sirve) o `gpt-oss-120b`
(alfabéticamente primero, más caro). **Elegí `openai/gpt-oss-20b`**: es de chat,
está en la lista, y es el más chico — el criterio económico del plan. Declarado
y reversible.

**El listado se obtuvo con el SDK de Groq, no con `urllib`:** el `GET` crudo a
`/openai/v1/models` devuelve **403 con `error code: 1010`**, que es un bloqueo
de **Cloudflare** por firma del cliente, no un problema de la clave.

**Estado de partida, declarado y sin limpiar** (leído por MCP antes de arrancar):
`corpus_size = 10` (8 textos de agosto más los 2 joins del vivo 01, que quedaron
en `_state/`), `message_count = 0`, canal vacío, `n_agentes = 0`,
`D_ckm = None`, `temp_signal = None`, `corpus_status = operational`,
`clock tick = 15`.

Lo que se reporta, literal y sin interpretar: costo() de cada device, sus
decisiones por tipo, ritmo_declarado(2), el clock_log del canal, los mensajes
publicados y todo error o traceback entero.

Uso:
    PYTHONPATH=/workspaces/ckm python3 experiments/vivo_02_groq_gptoss20b.py [salida.json]
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

MODELO = "openai/gpt-oss-20b"
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
            device_id=f"GroqGptOss20B_{i + 1}",
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
        "que_es": "ESTO MIDE — vivo 02 del canal IAP con ODA continuo",
        "estado_de_partida_declarado": {
            "corpus_size": 10, "message_count": 0, "n_nodes": 32,
            "n_agentes": 0, "D_ckm": None, "temp_signal": None,
            "corpus_status": "operational", "mensajes_en_el_canal": 0,
            "clock_tick": 15,
            "nota": "sin limpiar: 8 textos de agosto + 2 joins del vivo 01",
        },
        "modelos_de_la_cuenta": [
            "allam-2-7b", "canopylabs/orpheus-arabic-saudi",
            "canopylabs/orpheus-v1-english",
            "meta-llama/llama-prompt-guard-2-22m",
            "meta-llama/llama-prompt-guard-2-86m",
            "openai/gpt-oss-120b", "openai/gpt-oss-20b",
            "openai/gpt-oss-safeguard-20b", "qwen/qwen3.8-27b",
            "whisper-large-v3", "whisper-large-v3-turbo",
        ],
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
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "experiments/vivo_02_groq_gptoss20b_log.json"
    try:
        res = asyncio.run(main())
    except BaseException as e:            # noqa: BLE001 — se reporta entero
        res = {
            "que_es": "ESTO MIDE — vivo 02, ABORTADO",
            "excepcion": type(e).__name__,
            "traceback": traceback.format_exc(),
        }
    tmp = salida.with_suffix(salida.suffix + ".tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    tmp.replace(salida)
    print(f"\nlog -> {salida}")
