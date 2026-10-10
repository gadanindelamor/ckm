"""
server.py — IAP Chatroom entry point.

Uso:
    python server.py [--state-dir RUTA]

`--state-dir` fija dónde escribe el Monitor (`corpus_state.json`,
`corpus_G_state.json`, `monitor_trajectory.jsonl`). **Sin el argumento, el
default de siempre** (`iap_chatroom/_state/`), así que nada cambia para quien
no lo pasa.

Es un **argumento explícito y no una variable de entorno** (delamor/Opus): una
variable no queda en el comando, y entonces el log de un vivo no alcanza para
saber dónde escribió. El server lo declara al arrancar y en el panel de
Monitor.
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

# ── el `--state-dir`, ANTES de cualquier import que construya el monitor ────
# El singleton se arma al importar: `mcp_server` tiene el primer
# `CKMMonitor()`. Cuando corre `if __name__ == "__main__"` la instancia ya
# existe y su directorio ya está fijado (`__init__` corta con
# `if self._initialized: return`). Así que esto NO puede estar más abajo ni
# dentro del `__main__`: el orden de estas líneas es el fix.
from iap_chatroom import arranque

arranque.leer_de_argv(sys.argv)

from iap_chatroom.api_routes import router            # noqa: E402
from iap_chatroom.channel import ChatChannel          # noqa: E402
from iap_chatroom.device_manager import DeviceManager  # noqa: E402
from iap_chatroom.mcp_server import mcp               # noqa: E402
from iap_chatroom.ui_gradio import build_gradio_app    # noqa: E402

# Singletons
channel = ChatChannel()
device_manager = DeviceManager()
ckm_monitor = arranque.monitor()

# **Dónde escribe este proceso**, dicho al arrancar. Cada vivo deja la línea en
# su consola, al lado del comando que lo lanzó.
_decl = arranque.declarar()
print(f"[server] state_dir = {_decl['state_dir']}"
      f"{' (pedido por --state-dir)' if _decl['fue_pedido'] else ' (default)'}")
if _decl["fue_pedido"] and not _decl["coincide"]:
    print(f"[server] AVISO: se pidió {_decl['state_dir_pedido']} y corre en "
          f"{_decl['state_dir']} — alguien construyó el monitor antes")

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
