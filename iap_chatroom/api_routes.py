"""
api_routes.py — endpoints REST + WebSocket de la IAP Chatroom.
"""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from iap_chatroom.channel import ChatChannel
from iap_chatroom.ckm_monitor import CKMMonitor
from iap_chatroom.device_manager import DeviceManager

router = APIRouter()

channel = ChatChannel()
device_manager = DeviceManager()
ckm_monitor = CKMMonitor()


class RegisterDeviceRequest(BaseModel):
    device_id: str
    device_type: Literal["AI", "HUMAN"]
    model: Optional[str] = None
    provider: Optional[str] = None


class ChatRequest(BaseModel):
    device_id: str
    text: str


@router.post("/devices/register")
async def register_device(body: RegisterDeviceRequest):
    device = device_manager.register(
        device_id=body.device_id,
        device_type=body.device_type,
        model=body.model,
        provider=body.provider,
    )
    return device.to_dict()


@router.post("/devices/{device_id}/unregister")
async def unregister_device(device_id: str):
    ok = device_manager.unregister(device_id)
    return {"unregistered": ok}


@router.get("/devices")
async def list_devices():
    return [d.to_dict() for d in device_manager.list_active()]


@router.post("/chat")
async def post_chat(body: ChatRequest):
    device = device_manager.get(body.device_id)
    if device is None:
        raise HTTPException(status_code=404, detail=f"device '{body.device_id}' no registrado")
    message = await channel.publish(device.device_id, device.device_type, body.text)
    return message.to_dict()


@router.websocket("/chat/stream")
async def chat_stream(ws: WebSocket):
    await ws.accept()
    channel.subscribe(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        channel.unsubscribe(ws)


@router.get("/clock")
async def get_clock():
    """El tick vigente del canal, con su período y su reloj."""
    return channel.get_clock()


@router.get("/clock/log")
async def get_clock_log(desde_tick: Optional[int] = None):
    """El log de ticks observados, con y sin mensajes (fix F2)."""
    return channel.clock_log_desde(desde_tick=desde_tick)


@router.get("/monitor")
async def get_monitor_state():
    return ckm_monitor.get_state()


@router.get("/monitor/firma")
async def get_monitor_firma():
    return ckm_monitor.get_firma()
