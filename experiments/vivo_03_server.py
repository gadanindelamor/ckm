"""
vivo_03_server.py — el server del VIVO 03, con el `state_dir` aislado

**Archivo nuevo. No modifica `server.py` ni `mcp_server.py`.**

### Por qué existe

La orden del vivo 03 pide `state_dir` **nuevo y aislado**. `CKMMonitor` acepta
`state_dir` desde el CP2b (F3a), pero **ningún camino vivo puede pasarlo**:
`server.py:31` y `mcp_server.py:23` construyen `CKMMonitor()` sin argumentos, y
no hay hook de entorno. F3a agregó el parámetro y dejó el camino vivo sin poder
usarlo — va reportado como hallazgo, no corregido de paso.

### Cómo se aísla sin tocar nada

`CKMMonitor` es un **singleton real** (`__new__` + `_instance`,
`ckm_monitor.py:45-51`, y `__init__` corta con `if self._initialized: return`).
Entonces quien lo construye **primero** fija la instancia para todo el proceso:
este launcher lo construye con el `state_dir` del vivo y **después** importa el
server, cuyo `CKMMonitor()` devuelve esa misma instancia.

No es un truco sobre el sistema de archivos: no se mueve ni se borra nada.
`iap_chatroom/_state/` (el de agosto) queda intacto como traza.

Uso:
    PYTHONPATH=/workspaces/ckm python3 experiments/vivo_03_server.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# El state_dir del vivo. Nombre con el vivo adentro: que se vea de quién es.
STATE_DIR = RAIZ / "experiments" / "_state_vivo_03"

from iap_chatroom.ckm_monitor import CKMMonitor  # noqa: E402

# ── acá se gana la carrera ───────────────────────────────────────────────────
# Esta construcción fija el singleton. Tiene que ir ANTES de importar el server.
_monitor = CKMMonitor(state_dir=STATE_DIR)
assert _monitor.state_dir == STATE_DIR, (
    f"el state_dir no quedó aislado: {_monitor.state_dir}"
)
print(f"[vivo 03] state_dir aislado = {_monitor.state_dir}")

import iap_chatroom.server as server  # noqa: E402

# Y se verifica que el server esté usando LA MISMA instancia, no otra. Si el
# server construyera una propia, el aislamiento sería aparente y el log diría
# una cosa mientras el corpus escribiría en otra.
assert server.ckm_monitor is _monitor, (
    "el server no está usando el monitor aislado: el singleton no alcanzó"
)
assert server.ckm_monitor.state_dir == STATE_DIR
print(f"[vivo 03] server.ckm_monitor es la misma instancia: ok")


if __name__ == "__main__":
    import uvicorn

    # Mismo arranque que `server.py`: un solo proceso, sin `workers=`, para que
    # ChatChannel y CKMMonitor sigan siendo singletons de verdad.
    uvicorn.run(server.app, host="0.0.0.0", port=7860, log_level="warning")
