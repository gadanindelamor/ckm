"""
api_routes.py — endpoints REST + WebSocket de la IAP Chatroom.
"""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from iap_chatroom import arranque
from iap_chatroom.channel import ChatChannel
from iap_chatroom.device_manager import DeviceManager

router = APIRouter()

channel = ChatChannel()
device_manager = DeviceManager()


# **Nadie construye `CKMMonitor` al importarse** (CP1, agregado 1 de delamor,
# 18 oct). Acá había un `ckm_monitor = CKMMonitor()` a nivel de módulo: como
# `server.py` importa este módulo **antes** de llamar a `arranque.monitor()`,
# ese pelado ganaba la carrera del singleton y el `--state-dir` quedaba en el
# default — con un aviso por consola y nada en el panel. En la Serie 2 eso
# podría escribir en el estado de otra cosa.
#
# El monitor se pide **cuando se usa**, a `arranque`, que es el único que sabe
# qué directorio se pidió. La función es una línea y no cachea: el singleton ya
# es el caché.
def _monitor():
    return arranque.monitor()



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
    if message is None:
        # El canal no publica vacíos (CP1, agregado 2). 422: la petición está
        # bien formada y el contenido es el que el canal no acepta.
        raise HTTPException(
            status_code=422,
            detail="texto vacio: el canal no publica mensajes sin contenido",
        )
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
    return _monitor().get_state()


@router.get("/monitor/firma")
async def get_monitor_firma():
    return _monitor().get_firma()
