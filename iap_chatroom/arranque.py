"""
arranque.py — el `state_dir` como **argumento de arranque explícito** del server

### Por qué existe

`CKMMonitor` acepta `state_dir` desde el CP2b (F3a), pero **ningún camino vivo
podía pasarlo**: `server.py` y `mcp_server.py` construían `CKMMonitor()` sin
argumentos. El vivo 03 lo resolvió con un launcher propio
(`experiments/vivo_03_server.py`) que gana la carrera del singleton. Ese
launcher **queda como traza y no se borra**; esto es el camino declarado.

delamor/Opus: **argumento explícito, no variable de entorno implícita.** Una
variable de entorno no se ve en el comando que quedó en la consola, y entonces
el log de un vivo no alcanza para saber dónde escribió.

### Por qué un módulo aparte, y no `__main__`

El singleton se construye **al importar**: `server.py` importa `mcp_server`, y
ahí dentro está el primer `CKMMonitor()`. Cuando `if __name__ == "__main__"`
corre, la instancia ya existe y su `state_dir` ya está fijado — el `__init__`
corta con `if self._initialized: return`.

Así que el argumento tiene que estar leído **antes de esa importación**. Este
módulo no importa nada de `iap_chatroom`, así que puede cargarse primero sin
arrastrar el resto.

### Sin argumento, el default de hoy

`state_dir_pedido()` devuelve `None` y `CKMMonitor` usa `iap_chatroom/_state/`,
que es lo que usaba antes de esto. **Nada cambia para quien no pasa el
argumento.**
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

# La bandera, escrita una sola vez acá para que no haya dos spellings sueltos.
FLAG = "--state-dir"

# `None` es **"nadie lo pidió"**, y no un directorio vacío: con None
# `CKMMonitor` aplica su default. No se inicializa con el default acá, porque
# entonces no se podría distinguir "me pidieron el default" de "no me pidieron
# nada", y el panel tiene que poder decir cuál de las dos fue.
_state_dir_pedido: Optional[Path] = None
_fue_pedido: bool = False


def fijar_state_dir(valor: "str | Path | None") -> Optional[Path]:
    """
    Fija el `state_dir` pedido. Tiene que llamarse **antes** de que se importe
    `mcp_server` o `server`, o la instancia ya está construida.

    Con `None` vuelve al default y `fue_pedido()` pasa a False: sirve para los
    tests, que necesitan dejar el módulo como estaba.
    """
    global _state_dir_pedido, _fue_pedido
    if valor is None:
        _state_dir_pedido = None
        _fue_pedido = False
        return None
    _state_dir_pedido = Path(valor)
    _fue_pedido = True
    return _state_dir_pedido


def state_dir_pedido() -> Optional[Path]:
    """El que se pidió, o `None` si nadie lo pidió."""
    return _state_dir_pedido


def fue_pedido() -> bool:
    """
    Si alguien lo pidió explícitamente. **Se distingue de `state_dir_pedido()
    is None`** para el caso en que alguien pida justo el default: el panel dice
    "me lo pidieron" y no "estoy en el default porque nadie dijo nada".
    """
    return _fue_pedido


def leer_de_argv(argv: Sequence[str]) -> Optional[Path]:
    """
    Lee `--state-dir <ruta>` (o `--state-dir=<ruta>`) de `argv` y lo fija.

    Devuelve lo fijado, o `None` si la bandera no estaba. **Ignora el resto de
    `argv` sin quejarse**: acá no se valida la línea de comandos del server,
    sólo se busca esta bandera. Lo que no se reconoce no es asunto de este
    módulo, y tratarlo como error rompería a quien pase flags de uvicorn.

    Si la bandera está y no viene seguida de una ruta, **levanta**: pedir el
    aislamiento y quedarse en el default sin aviso es peor que no arrancar.
    """
    args = list(argv)
    for i, a in enumerate(args):
        if a == FLAG:
            if i + 1 >= len(args) or args[i + 1].startswith("-"):
                raise ValueError(
                    f"{FLAG} sin ruta. Pedir el aislamiento y caer al default "
                    f"sin avisar es peor que no arrancar."
                )
            return fijar_state_dir(args[i + 1])
        if a.startswith(FLAG + "="):
            ruta = a.split("=", 1)[1]
            if not ruta:
                raise ValueError(f"{FLAG}= sin ruta.")
            return fijar_state_dir(ruta)
    return None


def monitor():
    """
    Construye (o devuelve) el `CKMMonitor` con el `state_dir` pedido.

    Es un singleton: la **primera** llamada fija el directorio y las siguientes
    devuelven esa misma instancia. Por eso `server.py` y `mcp_server.py` pueden
    llamar a esto los dos sin que se instancie estado nuevo.

    El import va adentro para que este módulo siga sin dependencias de
    `iap_chatroom` a nivel de módulo: tiene que poder cargarse **antes** que
    todo lo demás.
    """
    from iap_chatroom.ckm_monitor import CKMMonitor

    return CKMMonitor(state_dir=_state_dir_pedido)


def declarar() -> dict:
    """
    Lo que el server dice al arrancar y lo que va al panel de Monitor: **dónde
    está escribiendo este proceso**.

    `pedido` distingue el default elegido del default por omisión. `efectivo`
    sale de la instancia y no de esta configuración: si alguien construyó el
    monitor antes (el launcher del vivo 03, un test), el efectivo es el suyo y
    **el panel tiene que decir el real, no el que yo pedí**.
    """
    from iap_chatroom.ckm_monitor import CKMMonitor

    efectivo = (
        CKMMonitor._instance.state_dir if CKMMonitor._instance is not None else None
    )
    return {
        "state_dir": str(efectivo) if efectivo is not None else None,
        "state_dir_pedido": (
            str(_state_dir_pedido) if _state_dir_pedido is not None else None
        ),
        "fue_pedido": _fue_pedido,
        # Si lo que corre coincide con lo que se pidió. False dice que alguien
        # construyó el monitor antes, y eso es un dato y no un detalle.
        "coincide": (
            None if not _fue_pedido
            else (efectivo is not None and Path(efectivo) == _state_dir_pedido)
        ),
    }
