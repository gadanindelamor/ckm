"""
vivo_03_criterio_local.py — VIVO 03 del canal IAP, con el criterio local puesto

**ESTO MIDE.** Primera corrida con el filtro del CP2b encendido contra un
provider real. Se compara con la línea de base del vivo 02 (23 llamadas).

Orden de delamor (E1, DECISIONES `4115efa`): opción (a), vivo de 60 s con
`piso_vueltas` dentro de la ventana. **No interpretar lo que dice el modelo.**

Setup, igual al vivo 02 salvo lo marcado:
  2 devices · GroqProvider("openai/gpt-oss-20b") · poll_interval = 5.0
  duration = 60 s · gate congelado en f96c234 · una sola corrida
  **criterio local ENCENDIDO** · umbrales por default (NO calibrados)
  salvo `piso_vueltas = 6` · **state_dir nuevo y aislado**

### El teorema, escrito antes de correr (ver BANDEJA, ARRANQUE 23:32 UTC)

Con `piso_vueltas = 6` y **silencio puro**, el filtro llama en la vuelta 1
(`primera_vuelta`) y la 8 (`piso`): 2 llamadas y 10 skips en 12 vueltas. La
vuelta 14 sería la siguiente del piso y no entra en la ventana. Más las
auditorías de la cara del skip, ~Binomial(10, 0.1).

**Predicción: 2 a 4 llamadas por device**, contra 11-12 del vivo 02.

Lo que NO es teorema y es lo que esto mide: (1) los **joins SYSTEM cuentan en
`n_nuevos`** —salen del corpus por F3b pero siguen en la observación—, así que
van a disparar `mensajes_nuevos` y rompen el silencio puro; (2) qué decide el
modelo cuando se lo llama; (3) cuántas vueltas sale cada device; (4) los sorteos
de la auditoría, que en vivo van sin semilla.

### Una diferencia con el vivo 02 que hay que declarar

El vivo 02 arrancó con `corpus_size = 10` (8 textos de agosto más 2 joins del
vivo 01, sin limpiar). **Este arranca en 0**, porque el `state_dir` está
aislado, que es lo que la orden pide. Entonces la comparación con el vivo 02 es
sobre **llamadas al LLM**, no sobre el corpus: el corpus difiere por
construcción, y decirlo acá es parte de la medición.

### Cada device con SU propio filtro

El criterio local **tiene estado** (cuándo llamó por última vez), y ese estado
es por device. Un filtro compartido haría que el piso de uno reseteara el del
otro: los dos leerían el mismo contador y el panel diría cualquier cosa. Por eso
se construye uno por device y no se pasa el mismo dos veces.

Uso (el server tiene que estar corriendo con `experiments/vivo_03_server.py`):
    PYTHONPATH=/workspaces/ckm python3 experiments/vivo_03_criterio_local.py [salida.json]
"""

from __future__ import annotations

import asyncio
import json
import platform
import subprocess
import sys
import time
import traceback
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from iap_chatroom.autonomous_device import AutonomousDevice        # noqa: E402
from iap_chatroom.criterio_local import (                          # noqa: E402
    CriterioLocal,
    UmbralesCriterioLocal,
)
from iap_chatroom.providers.groq_provider import GroqProvider      # noqa: E402

MODELO = "openai/gpt-oss-20b"
POLL_INTERVAL = 5.0
DURATION = 60.0
N_DEVICES = 2
MCP_URL = "http://localhost:7860/mcp"

# El único umbral que NO va por default, y por qué: con el default de 12 el piso
# dispararía en la vuelta 14, y las vueltas por device son 11-12 — no dispararía
# nunca, y el vivo mediría el filtro sin su pieza principal. Con 6 dispara en la
# 8. El valor lo fijó Opus al dar el OK; **sigue sin calibrar**, como el resto.
PISO_VUELTAS = 6

# El WELCOME MSG de la serie, fijo desde el Caso 0.4a. No se toca.
SYSTEM_PROMPT = (
    "You are an AI device in a shared channel with other AI devices. "
    "You observe the channel and decide whether to participate. "
    "You do not need to respond to every message."
)


def _umbrales() -> UmbralesCriterioLocal:
    return UmbralesCriterioLocal(piso_vueltas=PISO_VUELTAS)


async def _estado_de_partida(url: str) -> dict:
    """Se lee ANTES de arrancar, por MCP, y se declara en el log."""
    from fastmcp import Client

    async with Client(url) as c:
        monitor = (await c.call_tool("get_monitor_state", {})).data
        clock = (await c.call_tool("get_clock", {})).data
        mensajes = (await c.call_tool("get_messages", {"since": None})).data
    return {
        "monitor_state": monitor,
        "clock": clock,
        "mensajes_en_el_canal": len(mensajes),
    }


async def main() -> dict:
    partida = await _estado_de_partida(MCP_URL)

    devices = [
        AutonomousDevice(
            device_id=f"GroqGptOss20B_{i + 1}",
            provider=GroqProvider(model=MODELO),
            system_prompt=SYSTEM_PROMPT,
            mcp_url=MCP_URL,
            poll_interval=POLL_INTERVAL,
            # uno por device: el estado del filtro es de cada uno
            criterio_local=CriterioLocal(umbrales=_umbrales()),
        )
        for i in range(N_DEVICES)
    ]
    assert devices[0].criterio_local is not devices[1].criterio_local, \
        "los dos devices comparten el filtro: el piso de uno resetearía al otro"

    errores_fatales = []
    t0 = time.time()
    resultados = await asyncio.gather(
        *(d.run(duration=DURATION) for d in devices),
        return_exceptions=True,
    )
    segundos = round(time.time() - t0, 2)

    for d, r in zip(devices, resultados):
        if isinstance(r, BaseException):
            errores_fatales.append({
                "device_id": d.device_id,
                "excepcion": type(r).__name__,
                "traceback": "".join(
                    traceback.format_exception(type(r), r, r.__traceback__)
                ),
            })

    from fastmcp import Client

    async with Client(MCP_URL) as c:
        mensajes = (await c.call_tool("get_messages", {"since": None})).data
        clock = (await c.call_tool("get_clock", {})).data
        monitor = (await c.call_tool("get_monitor_state", {})).data

    umb = _umbrales()
    llamadas_totales = sum(d._llamadas_llm for d in devices)

    return {
        "que_es": "ESTO MIDE — vivo 03: el criterio local del CP2b, en vivo",
        "orden": "delamor, E1 (DECISIONES 4115efa): opcion (a), 60 s con piso en la ventana",
        "prediccion_escrita_antes_de_correr": {
            "donde": "BANDEJA_code.md, ARRANQUE VIVO 03, 2026-10-09 23:32 UTC",
            "deterministico_con_silencio_puro": {
                "llama_en_las_vueltas": [1, 8],
                "motivos": ["primera_vuelta", "piso"],
                "skips_en_12_vueltas": 10,
                "nota": "la vuelta 14 seria el siguiente piso y no entra",
            },
            "auditorias_cara_skip": "~Binomial(10, 0.1), esperanza 1",
            "llamadas_por_device_esperadas": "2 a 4",
            "no_es_teorema": [
                "los joins SYSTEM cuentan en n_nuevos y rompen el silencio puro",
                "que decide el modelo cuando se lo llama",
                "cuantas vueltas sale cada device (latencia de Groq)",
                "los sorteos de la auditoria, sin semilla en vivo",
            ],
        },
        "estado_de_partida_leido_por_MCP": partida,
        "diferencia_declarada_con_el_vivo_02": (
            "el vivo 02 arranco con corpus_size=10 (sin limpiar); este arranca "
            "aislado. La comparacion es sobre LLAMADAS, no sobre el corpus."
        ),
        "declarado": {
            "modelo": MODELO,
            "provider": "groq",
            "n_devices": N_DEVICES,
            "poll_interval_s": POLL_INTERVAL,
            "duration_s": DURATION,
            "gate_congelado_en": "f96c234",
            "system_prompt": SYSTEM_PROMPT,
            "criterio_local": "ENCENDIDO",
            "umbrales": {
                "dt_minimo_s": umb.dt_minimo_s,
                "piso_vueltas": umb.piso_vueltas,
                "tasa_auditoria": umb.tasa_auditoria,
                "tasa_auditoria_pase": umb.tasa_auditoria_pase,
            },
            "umbrales_calibrados": umb.calibrado,
            "state_dir": str(RAIZ / "experiments" / "_state_vivo_03"),
        },
        "repo_commit": subprocess.run(
            ["git", "-C", str(RAIZ), "rev-parse", "HEAD"],
            capture_output=True, text=True,
        ).stdout.strip(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "donde": "Codespace ckm, server en otro proceso del mismo host",
        "variables_no_consideradas": "todas las que no estan en este log",
        "segundos_reales": segundos,
        "errores_fatales": errores_fatales,
        "ritmo_declarado_2": devices[0].ritmo_declarado(n_devices=N_DEVICES),
        "linea_de_base_vivo_02": {
            "llamadas_totales": 23,
            "vueltas_por_device": [11, 12],
            "decisiones_por_tipo": {"OP_SILENCE": 23},
            "errores": 0,
        },
        "llamadas_totales_vivo_03": llamadas_totales,
        "por_device": [
            {
                "costo": d.costo(),
                "panel_criterio": d.panel_criterio(),
                "registros_criterio": d.registros_criterio(),
                "decisiones": d.decisiones(),
            }
            for d in devices
        ],
        "canal": {
            "clock_final": clock,
            "n_mensajes": len(mensajes),
            "mensajes": mensajes,
            "monitor_state": monitor,
        },
    }


if __name__ == "__main__":
    salida = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else RAIZ / "experiments/vivo_03_criterio_local_log.json"
    )
    try:
        res = asyncio.run(main())
    except BaseException as e:            # noqa: BLE001 — se reporta entero
        res = {
            "que_es": "ESTO MIDE — vivo 03, ABORTADO",
            "excepcion": type(e).__name__,
            "traceback": traceback.format_exc(),
        }
    tmp = salida.with_suffix(salida.suffix + ".tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    tmp.replace(salida)
    print(f"\nlog -> {salida}")
