"""
mcp_server.py — capa MCP sobre la infraestructura existente de IAP Chatroom.

IAP se expone como MCP Server: agentes externos usan estas tools como
clientes MCP para participar en el canal de chat. Reutiliza los mismos
singletons (ChatChannel, DeviceManager, CKMMonitor) que ya usa
api_routes.py — no se instancia estado nuevo.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastmcp import FastMCP

from iap_chatroom.channel import ChatChannel
from iap_chatroom.ckm_monitor import CKMMonitor
from iap_chatroom.device_manager import DeviceManager

channel = ChatChannel()
device_manager = DeviceManager()
ckm_monitor = CKMMonitor()  # min_texts=3 (default actual del umbral rebuild(W))

mcp = FastMCP("iap-chatroom")


def _epoch(iso_timestamp: str) -> float:
    return datetime.fromisoformat(iso_timestamp).timestamp()


def _message_dict(index: int, message) -> dict:
    d = message.to_dict()
    d["message_id"] = f"msg-{index}"
    return d


@mcp.tool
async def join_channel(device_id: str, device_type: str) -> dict:
    """Registra un device en la chatroom via DeviceManager. Emite un
    mensaje SYSTEM operacional en el canal ("{device_id} joined the
    channel") — visible en get_messages() y disponible como trigger
    del ciclo ODA."""
    device = device_manager.register(device_id=device_id, device_type=device_type)
    await channel.publish_system_event(f"{device_id} joined the channel")
    return {
        "ok": True,
        "device_id": device.device_id,
        "registered_at": _epoch(device.connected_at),
    }


@mcp.tool
async def send_message(device_id: str, text: str) -> dict:
    """Publica un mensaje al ChatChannel. CKMMonitor lo acumula via callback."""
    device = device_manager.get(device_id)
    if device is None:
        raise ValueError(f"device '{device_id}' no registrado")

    message = await channel.publish(device.device_id, device.device_type, text)
    index = len(channel.messages) - 1
    return {
        "message_id": f"msg-{index}",
        "corpus_size": ckm_monitor.get_state()["corpus_size"],
    }


@mcp.tool
async def get_messages(since: Optional[float] = None) -> list[dict]:
    """Mensajes posteriores a `since` (epoch). Si since=None, retorna los ultimos 20."""
    history = channel.get_history()

    if since is None:
        start = max(0, len(history) - 20)
        selected = list(enumerate(history))[start:]
    else:
        selected = [
            (i, m) for i, m in enumerate(history) if _epoch(m.timestamp) > since
        ]

    return [_message_dict(i, m) for i, m in selected]


@mcp.tool
async def get_monitor_state() -> dict:
    """Estado CKM: D_ckm, temp_signal, n_agentes, corpus_size, message_count,
    n_nodes, corpus_status ("accumulating" si corpus_size < min_texts,
    "operational" si W existe y D_ckm es calculable)."""
    return ckm_monitor.get_state()


@mcp.tool
async def get_firma() -> Optional[dict]:
    """Firma_CKM (6 campos canonicos). None si el corpus aun esta en acumulacion."""
    return ckm_monitor.get_firma()


@mcp.tool
async def leave_channel(device_id: str) -> dict:
    """Desregistra un device de la chatroom."""
    ok = device_manager.unregister(device_id)
    return {"ok": ok}

