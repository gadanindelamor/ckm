"""
run_store.py — **todo lo de una corrida, en el mismo `state_dir`**

Punto 3 de `TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md` (delamor):
*"IAP escribe todo en el mismo `state_dir` privado, sin lógica en los
drivers"*.

### Qué problema cierra

Hasta acá el `state_dir` tenía **el estado del modelo** y nada más:
`corpus_state.json`, `corpus_G_state.json`, `monitor_trajectory.jsonl`,
`rebuild_decisions.jsonl`, `rebuild_state.json` — todos escritos por
`CKMMonitor` y por los servicios. Lo del **canal** y lo de los **devices**
vivía en memoria: `ChatChannel.messages`, `_rejected_attempts`, `_clock_log`,
`AutonomousDevice._decisiones`, `_registros_criterio`, y los `print` del
`_log`. Sobrevivían sólo si el driver llegaba al final y los volcaba.

Eso tiene dos consecuencias medidas en los vivos anteriores: un corte a mitad
de camino **se lleva la corrida entera**, y el log de un vivo queda repartido
entre el `state_dir` y el JSON que escribió el driver, con el driver decidiendo
qué guardar. Lo segundo es lo que delamor nombra como *"sin lógica en los
drivers"*: si el driver elige, cada vivo guarda algo distinto.

### Las reglas, y dónde se cumple cada una

- **Append-only y durante la corrida.** Cada registro es una línea de JSONL y
  se escribe **cuando ocurre**, con `flush()` antes de volver. No hay buffer
  propio ni volcado al final: lo escrito queda aunque el proceso muera en la
  línea siguiente.
- **Nombres en inglés.** Los de los archivos y los de las claves que nacen
  acá. Las claves que vienen de otro módulo **viajan como ese módulo las
  nombró** (`motivo`, `via`, `vuelta`, `reloj`): traducirlas acá sería
  renombrar el registro de otro módulo desde afuera, y además haría que el
  archivo no dijera lo mismo que el objeto en memoria.
- **Sin lógica en los drivers.** El driver pasa el `state_dir` y nada más.
  Quien escribe es IAP: el canal lo suyo, el device lo suyo.
- **Lo de COCO sigue sin publicarse en el canal.** Este módulo no toca el
  canal: escribe en disco. `monitor_trajectory.jsonl` sigue siendo el lugar
  de COCO, como hoy.

### Dos procesos, un directorio

Un vivo de IAP corre en **dos procesos**: el server (canal + Monitor) y el
driver (los devices, por MCP). Los dos tienen que escribir en el mismo
directorio, y ninguno puede leerle la variable al otro.

- en el **server**, el directorio lo fija `CKMMonitor.__init__`, que es donde
  la corrida ya declaraba dónde escribe; el canal lo lee de acá al momento de
  escribir, no al importarse — por eso no importa que `ChatChannel()` se
  construya antes que el monitor (`mcp_server.py` lo hace);
- en el **driver**, cada `AutonomousDevice` recibe su `state_dir` y escribe con
  él. No hereda nada: en ese proceso no hay monitor.

### `None` es "nadie lo pidió", y entonces no se escribe

Igual que en `startup.py`. Sin directorio fijado, `append()` **no escribe y no
levanta**: devuelve False. Un `ChatChannel` de un test unitario no deja
archivos por ahí, y un vivo siempre tiene monitor, así que siempre escribe.

### Una falla de escritura no mata una corrida, y no se traga

`append()` no propaga la excepción: un disco lleno no puede matar un vivo de
70 mensajes. Pero **tampoco se pierde**: queda en `failures()` con su archivo,
su excepción y su momento, y el panel del device la publica. Un registro que
no se pudo escribir y un registro que no ocurrió son dos cosas distintas.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── los archivos de la corrida. Nombres en inglés, uno por concepto ──────────

# Los mensajes del canal, con el texto entero. Lo que antes vivía sólo en
# `ChatChannel.messages`.
CHANNEL_MESSAGES = "channel_messages.jsonl"

# Los intentos de publicar que el canal rechazó (`_rejected_attempts`). Un
# rechazo que no deja rastro es indistinguible de un mensaje que nunca se
# intentó.
REJECTED_ATTEMPTS = "rejected_attempts.jsonl"

# El log de ticks observados del canal, con y sin mensajes (`_clock_log`): el
# silencio entre mensajes es dato medible.
CHANNEL_TICKS = "channel_ticks.jsonl"

# La traza de decisiones de cada device (`_decisiones`), una línea por vuelta.
DEVICE_DECISIONS = "device_decisions.jsonl"

# Los registros del filtro de llamadas (`_registros_criterio`), con el motivo
# y la vía de cada skip.
CALL_FILTER_RECORDS = "call_filter_records.jsonl"

# Todos los logs: lo que el device imprimía con `print` y nada más, más los
# errores del provider y las respuestas ilegibles — que hasta acá sobrevivían
# sólo si el driver llegaba a volcar `costo()`.
#
# Desde el 21 oct 2026, dos eventos más: `op_silence_in_generate` —el generate
# devolvió, exacto, una palabra del protocolo, así que no se publicó y el
# device queda como que eligió callar— y `run_exception_inside_client`: la
# excepción de **adentro** del `async with Client(...)`, con su traceback,
# escrita cuando pasa. Sin eso se pierde — el cierre del cliente la reemplaza y
# `exceptiongroup` suprime el contexto (`autonomous_device.run`).
DEVICE_LOG = "device_log.jsonl"

# Todos los que este módulo escribe. Está acá para que un test pueda barrerlos
# sin repetir la lista (y para que agregar uno no se olvide de los tests).
ARCHIVOS = (
    CHANNEL_MESSAGES,
    REJECTED_ATTEMPTS,
    CHANNEL_TICKS,
    DEVICE_DECISIONS,
    CALL_FILTER_RECORDS,
    DEVICE_LOG,
)

# ── el directorio del proceso ────────────────────────────────────────────────

_state_dir: Optional[Path] = None

# Las escrituras vienen del loop del canal y de los loops de los devices. En un
# proceso con asyncio son del mismo hilo, pero `ChatChannel` también lo usa
# `server.py` bajo uvicorn, que sí tiene más de uno. Un lock por línea es
# barato y evita una línea partida por la mitad, que es un JSONL ilegible.
_lock = threading.Lock()

_failures: list[dict] = []


def set_state_dir(valor: "str | Path | None") -> Optional[Path]:
    """
    Fija el directorio de la corrida para **este proceso**.

    Lo llama `CKMMonitor.__init__` con el mismo valor que ya usa para el
    corpus: el directorio de la corrida es uno, y que lo declare dos veces
    sería poder declararlos distintos.

    Con `None` vuelve a "nadie lo pidió" y `append()` deja de escribir. Los
    tests lo usan para dejar el módulo como estaba.
    """
    global _state_dir
    _state_dir = Path(valor) if valor is not None else None
    return _state_dir


def state_dir() -> Optional[Path]:
    """El directorio de la corrida, o `None` si nadie lo fijó."""
    return _state_dir


def failures() -> list[dict]:
    """Las escrituras que no se pudieron hacer. Copia: no se edita."""
    return list(_failures)


def reset_failures() -> None:
    """Para los tests. No borra archivos: sólo el registro de fallas."""
    _failures.clear()


def ahora_utc() -> str:
    """El sello de cuándo se escribió la línea. ISO8601 UTC."""
    return datetime.now(timezone.utc).isoformat()


def append(archivo: str, registro: dict,
           state_dir_propio: "str | Path | None" = None) -> bool:
    """
    Escribe una línea y la baja al sistema operativo. **True si se escribió.**

    `state_dir_propio` es para quien tiene el suyo y no el del proceso: los
    devices, que corren en el proceso del driver. Sin él se usa el del módulo.

    **El `flush()` es la regla, no una optimización al revés.** Sin él, las
    líneas quedan en el buffer de Python y un `kill -9` se las lleva: el
    archivo existiría, crecería al cerrar, y "crece durante la corrida" sería
    falso justo en el caso que importa. No se hace `fsync`: eso protege de que
    se apague la máquina, y lo que el punto 3 pide es sobrevivir a un corte
    **del proceso**, que el flush ya cubre.

    `default=str` para que un valor que no sabe serializarse —un numpy, un
    Path— **no tire la línea entera**. Perder un registro por un tipo es peor
    que guardarlo como texto.
    """
    base = Path(state_dir_propio) if state_dir_propio is not None else _state_dir
    if base is None:
        return False
    linea = dict(registro)
    linea.setdefault("written_at_utc", ahora_utc())
    try:
        with _lock:
            base.mkdir(parents=True, exist_ok=True)
            with open(base / archivo, "a") as f:
                f.write(json.dumps(linea, ensure_ascii=False, default=str) + "\n")
                f.flush()
        return True
    except Exception as e:                      # noqa: BLE001 — se registra
        # No se propaga y no se pierde. Ver el docstring del módulo.
        _failures.append({
            "file": archivo,
            "state_dir": str(base),
            "exception": type(e).__name__,
            "message": str(e)[:300],
            "t_utc": ahora_utc(),
        })
        return False


def read(archivo: str, state_dir_propio: "str | Path | None" = None) -> list[dict]:
    """
    Las líneas de un archivo de la corrida, parseadas. `[]` si no existe.

    **Una línea ilegible no se saltea en silencio**: entra como
    `{"_unparsed": "<la línea>"}`. Un JSONL cortado por la mitad —que es
    exactamente lo que deja un corte— tiene que poder verse como lo que es.
    """
    base = Path(state_dir_propio) if state_dir_propio is not None else _state_dir
    if base is None:
        return []
    ruta = base / archivo
    if not ruta.exists():
        return []
    salida: list[dict] = []
    for linea in ruta.read_text().splitlines():
        if not linea.strip():
            continue
        try:
            salida.append(json.loads(linea))
        except json.JSONDecodeError:
            salida.append({"_unparsed": linea})
    return salida
