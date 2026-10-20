"""
conftest.py — **la suite no escribe en el `state_dir` del repo**

### Por qué existe

El punto 3 de `serie2_caso0` hizo que `ChatChannel` y `AutonomousDevice`
escriban lo suyo en el `state_dir` de la corrida, y que ese directorio lo
declare `CKMMonitor.__init__` para todo el proceso (`run_store.set_state_dir`).

En la suite eso tiene una consecuencia que **medí al pasar**: un test que
construye `CKMMonitor()` sin `state_dir` deja el del default —
`iap_chatroom/_state/`, el corpus de agosto, que es traza y no se toca— como
directorio del proceso. Los tests siguientes que publican en un canal
escribían ahí: aparecieron `channel_messages.jsonl` y `channel_ticks.jsonl` en
el `_state` del repo, con tres líneas de dos tests distintos. No rompió nada y
no es inofensivo: es el estado acumulándose entre corridas sin que nadie lo
declare, que es exactamente lo que F3a vino a cerrar.

### Qué hace

Antes de cada test, `run_store` vuelve a *"nadie lo pidió"*. Un test que
quiera escritura fija su directorio —construyendo su `CKMMonitor` con
`tmp_path`, o llamando a `run_store.set_state_dir`—; el que no, no escribe en
ninguna parte. Y después de cada test se vuelve a limpiar, para que el
directorio de un test no sobreviva al `tmp_path` que ya no existe.

**No se desactiva la escritura**: se desactiva el *default heredado*. Los tests
del punto 3 fijan su directorio y verifican los archivos; si esto apagara el
mecanismo, esos tests pasarían sin medir nada.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from iap_chatroom import run_store  # noqa: E402


# El `_state` del repo: el corpus de agosto. **Traza, y no se toca** — 8 de sus
# 12 textos son joins, que es la condición en la que corrió la serie congelada.
_STATE_DEL_REPO = RAIZ / "iap_chatroom" / "_state"


@pytest.fixture(autouse=True)
def _run_store_aislado():
    """`run_store` arranca y termina cada test sin directorio fijado."""
    run_store.set_state_dir(None)
    run_store.reset_failures()
    yield
    run_store.set_state_dir(None)
    run_store.reset_failures()


@pytest.fixture(autouse=True)
def _el_state_del_repo_no_se_toca():
    """
    **Ningún test agrega archivos al `_state` del repo.**

    No es una precaución teórica: pasó dos veces mientras escribía el punto 3.
    La segunda fue por un test que importa `iap_chatroom.mcp_server`, y ese
    import construye el `CKMMonitor` por default, que fija el `state_dir` del
    proceso en `iap_chatroom/_state/`. El `_run_store_aislado` resetea **antes**
    del test, y el import ocurre **dentro**: cinco archivos nuevos en el corpus
    de agosto, y los encontré mirando `git status` por otra razón.

    Así que el guardia va acá y no en mi memoria. Compara el directorio antes y
    después de cada test y **falla nombrando los archivos**, con el nombre del
    test que los dejó. Un test que necesite escribir fija su directorio
    (`tmp_path`); el que no lo haga, se entera.

    **Compara nombre Y tamaño, no sólo nombre.** La primera versión miraba el
    listado, y eso deja pasar lo que importa: una vez que el archivo existe —lo
    dejó una corrida anterior, o la misma suite corriendo dos veces—, el
    nombre ya está en `antes` y **el crecimiento no se ve**. Fue lo que pasó:
    el archivo volvió a aparecer con 828 verdes y ningún test rojo, porque la
    corrida que lo creó fue otra. Con el tamaño adentro, un append también
    falla.

    **No se borra nada**: fallar es el punto. Borrar en silencio dejaría el
    mecanismo intacto y la próxima vez aparecerían nombres distintos.
    """
    def _foto() -> dict:
        if not _STATE_DEL_REPO.exists():
            return {}
        return {p.name: p.stat().st_size for p in _STATE_DEL_REPO.iterdir()}

    antes = _foto()
    yield
    despues = _foto()
    nuevos = sorted(n for n in despues if n not in antes)
    crecieron = sorted(n for n, t in despues.items()
                       if n in antes and t != antes[n])
    assert not nuevos and not crecieron, (
        f"este test escribió en el _state del repo — nuevos: {nuevos}, "
        f"modificados: {crecieron}. Ese directorio es la traza de agosto. "
        f"Fijá el state_dir del test (tmp_path) antes de que algo lo escriba "
        f"— importar iap_chatroom.mcp_server ya lo apunta al default."
    )
