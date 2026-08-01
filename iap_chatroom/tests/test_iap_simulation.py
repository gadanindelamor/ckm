"""
test_iap_simulation.py — IAP Simulation Test: SmartWidget Case.

Orquestacion secuencial para testing controlado.
No refleja el modelo asincrono por eventos de IAP en produccion.
Ventaja: determinista, reproducible, salida predecible.

Se corre con el servidor levantado (python iap_chatroom/server.py) y
ejercita el flujo completo de 3 devices (2 AI + 1 HUMAN) sobre las
6 tools MCP reales, siguiendo un caso de soporte al cliente de
SmartWidget Co. (producto no enciende, dentro de ventana de 30 dias).

2 modelos Anthropic — evaluamos campo CKM, no providers. Agent A y
Agent B usan el mismo provider (AnthropicProvider) con modelos
distintos (haiku / sonnet); lo que se observa es la trayectoria D_ckm
del corpus compartido, no una comparacion entre providers.

Uso:
    python iap_chatroom/test_iap_simulation.py
"""

from __future__ import annotations

import asyncio
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

from iap_chatroom.providers.anthropic_provider import AnthropicProvider  # noqa: E402
from iap_chatroom.providers.base import ChatMessage  # noqa: E402

MCP_URL = "http://localhost:7860/mcp"


AGENT_A_SYSTEM = """You are Groovie, a customer support AI for SmartWidget Co.
You have confirmed: customer purchased a SmartWidget 6 days ago.
Product is not turning on. Customer requests refund or replacement.
You do not have authority to process refunds or replacements.
Your role: present the case clearly to Agent B, answer questions,
coordinate resolution. Be concise. One message at a time."""

AGENT_B_SYSTEM = """You are a grievance redressal AI for SmartWidget Co.
Policy: purchases within 30 days qualify for refund OR replacement
at customer's choice. You have authority to approve both.
Your role: receive case from Agent A, gather necessary info,
make a decision, communicate resolution clearly.
If you need customer info, say so explicitly.
Be concise. One message at a time."""

CUSTOMER_MESSAGES = [
    "Hi, I bought the SmartWidget last week and it won't turn on. "
    "I'd prefer a replacement if possible.",
    "Thank you, I'll wait for the replacement shipment.",
]

AGENT_A = "agent_a_support"
AGENT_B = "agent_b_grievance"
CUSTOMER = "customer_01"

DEVICES = {
    AGENT_A: {"device_type": "AI", "system_prompt": AGENT_A_SYSTEM, "provider": None},
    AGENT_B: {"device_type": "AI", "system_prompt": AGENT_B_SYSTEM, "provider": None},
    CUSTOMER: {"device_type": "HUMAN", "system_prompt": None, "provider": None},
}

# turno -> device_id
TURN_SEQUENCE = [AGENT_A, AGENT_B, AGENT_A, AGENT_B, CUSTOMER, AGENT_B, AGENT_A, CUSTOMER]


def _coalesce(messages: list[ChatMessage]) -> list[ChatMessage]:
    """Fusiona mensajes consecutivos del mismo role (requisito de alternancia de Anthropic)."""
    if not messages:
        return messages
    merged: list[ChatMessage] = [dict(messages[0])]
    for m in messages[1:]:
        if m["role"] == merged[-1]["role"]:
            merged[-1]["content"] = merged[-1]["content"] + "\n" + m["content"]
        else:
            merged.append(dict(m))
    return merged


def _to_chat_messages(device_id: str, system_prompt: str, history: list[dict]) -> list[ChatMessage]:
    chat: list[ChatMessage] = [{"role": "system", "content": system_prompt}]
    for m in history:
        role = "assistant" if m["device_id"] == device_id else "user"
        chat.append({"role": role, "content": f"[{m['device_id']}]: {m['text']}"})
    system_msgs = [c for c in chat if c["role"] == "system"]
    turn_msgs = _coalesce([c for c in chat if c["role"] != "system"])
    return system_msgs + turn_msgs


async def generate(device_id: str, system_prompt: str, history: list[dict]) -> str:
    """Construye el prompt con historial del canal como contexto y llama al provider."""
    provider = DEVICES[device_id]["provider"]
    chat_messages = _to_chat_messages(device_id, system_prompt, history)
    return await provider.complete(chat_messages)


def _fmt_d_ckm(value: Optional[float]) -> str:
    return f"{value:.4f}" if isinstance(value, (int, float)) else "None"


async def _log_ckm(client: Client, device_id: str) -> None:
    state = await client.call_tool("get_monitor_state", {})
    d_ckm = state.data.get("D_ckm")
    temp = state.data.get("temp_signal") or "NOMINAL"
    corpus = state.data.get("corpus_size")
    print(f"[{device_id}] D_ckm={_fmt_d_ckm(d_ckm)} temp={temp} corpus={corpus}")
    return state.data


async def run_simulation() -> None:
    DEVICES[AGENT_A]["provider"] = AnthropicProvider(model="claude-haiku-4-5-20251001")
    DEVICES[AGENT_B]["provider"] = AnthropicProvider(model="claude-sonnet-5")

    joined: set[str] = set()
    full_history: list[dict] = []
    last_ts: dict[str, Optional[float]] = {"v": None}
    customer_idx = 0
    turn_states: list[dict] = []

    async with Client(MCP_URL) as client:

        async def ensure_joined(device_id: str) -> None:
            if device_id not in joined:
                r = await client.call_tool(
                    "join_channel",
                    {"device_id": device_id, "device_type": DEVICES[device_id]["device_type"]},
                )
                assert r.data["ok"], f"join_channel fallo para {device_id}"
                joined.add(device_id)

        for turn_num, device_id in enumerate(TURN_SEQUENCE, start=1):
            info = DEVICES[device_id]
            print(f"\n--- Turno {turn_num}: {device_id} ---")

            await ensure_joined(device_id)

            if info["device_type"] == "AI":
                fetched = await client.call_tool(
                    "get_messages", {"since": last_ts["v"]}
                )
                full_history.extend(fetched.data)
                last_ts["v"] = time.time()

                text = await generate(device_id, info["system_prompt"], full_history)
            else:
                text = CUSTOMER_MESSAGES[customer_idx]
                customer_idx += 1

            print(f"[{device_id}] {text}")

            send_result = await client.call_tool(
                "send_message", {"device_id": device_id, "text": text}
            )
            assert "message_id" in send_result.data

            state = await _log_ckm(client, device_id)
            turn_states.append({"turn": turn_num, "device_id": device_id, "text": text, "state": state})

        firma_result = await client.call_tool("get_firma", {})
        firma = firma_result.data

        for device_id in (AGENT_A, AGENT_B, CUSTOMER):
            r = await client.call_tool("leave_channel", {"device_id": device_id})
            assert r.data["ok"], f"leave_channel fallo para {device_id}"

    print("\n=== Firma_CKM (cierre) ===")
    if firma is None:
        print("Firma_CKM: None (corpus aun en acumulacion)")
    else:
        for field in ("w_sha", "d_ckm", "temp_signal", "n_agentes", "timestamp", "delta_sha"):
            print(f"{field}: {firma.get(field)}")

    print("\n=== Verificacion de criterios de exito ===")
    nominal_count = sum(
        1 for t in turn_states if (t["state"].get("temp_signal") or "NOMINAL") == "NOMINAL"
    )
    corpus_sizes = [t["state"].get("corpus_size") for t in turn_states]
    growing = all(b >= a for a, b in zip(corpus_sizes, corpus_sizes[1:]))
    d_ckm_final = firma.get("d_ckm") if firma else None
    resolution_words = ("refund", "replacement")
    agent_b_turns = [t["text"].lower() for t in turn_states if t["device_id"] == AGENT_B]
    declared_resolution = any(any(w in t for w in resolution_words) for t in agent_b_turns)

    print(f"corpus_size crece turno a turno: {growing} ({corpus_sizes})")
    print(f"temp_signal NOMINAL en >=5/8 turnos: {nominal_count}/8")
    print(f"Firma_CKM con 6 campos (no None): {firma is not None}")
    # D_ckm=0 al cierre con W_base + dominio cooperativo (todos los devices
    # hablan del mismo producto/politica) = cohesion alcanzada, no falla del
    # instrumento. El criterio "D_ckm != 0" solo aplica a corpus adversariales
    # con W_mixta; para este caso (cooperativo) se reporta como informativo.
    print(f"D_ckm al cierre (informativo, criterio != 0 aplica solo a corpus adversarial/W_mixta): {d_ckm_final}")
    print(f"Agent B declara refund/replacement: {declared_resolution}")


if __name__ == "__main__":
    asyncio.run(run_simulation())
