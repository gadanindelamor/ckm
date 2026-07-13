"""
server.py — IAP Chatroom entry point.

Uso:
    python server.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import gradio as gr
import uvicorn
from fastapi import FastAPI

from iap_chatroom.api_routes import router
from iap_chatroom.ckm_monitor import CKMMonitor
from iap_chatroom.channel import ChatChannel
from iap_chatroom.device_manager import DeviceManager
from iap_chatroom.mcp_server import mcp
from iap_chatroom.ui_gradio import build_gradio_app

# Singletons
channel = ChatChannel()
device_manager = DeviceManager()
ckm_monitor = CKMMonitor()

# Conectar monitor al canal
channel.add_callback(ckm_monitor.on_message)

# App MCP (streamable-http) montada en /mcp. Su lifespan debe pasarse al
# FastAPI padre o el session manager de FastMCP nunca arranca (ver
# https://gofastmcp.com/deployment/asgi).
mcp_app = mcp.http_app(path="/")

# FastAPI
app = FastAPI(title="IAP Chatroom CKM", lifespan=mcp_app.lifespan)
app.include_router(router, prefix="/api")

# Gradio montado sobre FastAPI (compone su propio lifespan con el de arriba)
gradio_app = build_gradio_app()
app = gr.mount_gradio_app(app, gradio_app, path="/ui")

# MCP montado sobre FastAPI
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    # app se pasa por referencia (no como string "server:app") para evitar que
    # uvicorn reimporte este modulo bajo el nombre "server" y duplique el
    # registro de singletons (channel.add_callback quedaria registrado 2x).
    # reload=False hace que esto sea seguro (el string solo es necesario
    # para que el reloader pueda reimportar en un subproceso).
    uvicorn.run(app, host="0.0.0.0", port=7860, reload=False)
