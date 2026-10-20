"""
test_caso_serie2_caso0.py — **Serie 2, caso 0** ("Cimientos")

Orden: `docs/opus/textos_para_code/TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md`
(delamor, texto de Opus, 20 oct 2026). Reemplaza a `..._persistencia_y_CP3_...`.

**Objetivo declarado, como sesgo** (delamor): terminar con la expresión *"COCO
no se conectó nunca a un vivo de IAP"*. Que suceda.

El apodo "Cimientos" es para recordarlo y **no entra a ningún prompt**: no
aparece en este archivo fuera de este docstring.

----------------------------------------------------------------------------
NO SE CORRE DESDE ACÁ. LO DISPARA DELAMOR.
----------------------------------------------------------------------------

Dos procesos, en este orden:

    # 1) el server, con el state_dir del caso
    PYTHONPATH=/workspaces/ckm python3 iap_chatroom/server.py \
        --state-dir /workspaces/ckm/experiments/_state_S2-C0

    # 2) el caso
    PYTHONPATH=/workspaces/ckm python3 iap_chatroom/tests/test_caso_serie2_caso0.py

`--preflight` corre **sólo** la verificación de los cuatro modelos y sale sin
tocar el canal. `--reset` preserva el estado anterior en `process/` con
timestamp —no borra— y sale.

**Durante el vivo no hay más tareas ni intervenciones** (delamor). Una vez
disparado, nadie toca nada hasta que termine.

----------------------------------------------------------------------------
EL DISEÑO, Y DE DÓNDE SALE CADA NÚMERO
----------------------------------------------------------------------------

**Sin agentes.** `AutonomousDevice` genuino, sin `AgentDeviceSkin`. No es
`vivo_03_*`: es un caso de la Serie 2, con su nombre.

**Sin seed** (decisión de Opus, por delegación de delamor: *"no, siempre que
no obstaculice el objetivo"*). No hay `seed_human`. El corpus arranca sólo con
lo que publiquen los devices; el ODA continuo permite que un device hable
primero (`tests/test_oda_continuo.py::test_iniciativa_el_diseno_permite_hablar_primero`).

**Riesgo declarado:** si el caso no llega a 30 textos de device, no hay primer
W, COCO no nace y el objetivo no se cumple. En ese caso, **lo primero a
ajustar en el próximo intento es poner un seed.**

### Estructura de prompts, como en la serie IAP 1

`system_prompt` = el bloque común de la serie (`SYSTEM_PROMPT_04A`: qué es el
canal y qué puede hacer el device) **más la consigna parcial**. Sin
explicación de los campos de CKM, como en 0.4a (delamor, para este caso). El
gate y la generación son los del código (`GATE_PROMPT_CONTINUO`). Device ids
**neutros**: `device_a`..`device_d`, para que el id no revele la perspectiva de
nadie.

### Consigna parcial, y nadie ve la lista de las cuatro

Cada device recibe **sólo su perspectiva**. La lista de las cuatro no la ve
nadie, y **no hay coordinador**: nadie tiene más información que los otros.
`test_la_consigna_de_un_device_no_nombra_las_otras_perspectivas` lo verifica
sobre los cuatro prompts armados.

### Los cuatro devices

| | perspectiva | provider | modelo |
|---|---|---|---|
| A | where the water comes from | Groq | `openai/gpt-oss-120b` |
| B | how it is distributed | Google | `gemini-2.5-flash` |
| C | who pays and how much | Groq | `openai/gpt-oss-20b` |
| D | what could go wrong in the next 20 years | Groq | `qwen/qwen3.8-27b` |

Orden arbitrario y **declarado**, como pide el texto.

**Por qué no es el cuarteto del texto original.** El texto pedía A → Groq
`llama-3.3-70b-versatile`, B → Anthropic `claude-sonnet-5`, C → Groq
`openai/gpt-oss-20b`, D → Anthropic `claude-haiku-4-5-20251001`, y *"verificá
que los cuatro identificadores respondan hoy"*. Medido el 20 oct 2026 con las
claves de este repo:

- `llama-3.3-70b-versatile` → **404**, y `models.list()` de esa cuenta no trae
  **ningún** modelo llama: Groq lo retiró. No es un problema de clave.
- los dos de Anthropic → **401 invalid x-api-key**. `ANTHROPIC_API_KEY` no
  está en el entorno (el secret de GitHub trae `GROQ_API_KEY`, no ésta) y la
  de `.env` no es válida.
- `openai/gpt-oss-20b` → OK.

Reemplazo **confirmado por delamor** el 20 oct (*"confirmo tu propuesta A
gpt-oss-120b / B gemini-2.5-flash / C gpt-oss-20b / D qwen/qwen3.8-27b"*),
después de proponerle conservar el 2×2 de providers copiando la clave de
Anthropic. Los cuatro verificados ese día, y `--preflight` los vuelve a
verificar al disparar: un identificador muerto tiene que frenar el caso
**antes** del canal, no en la vuelta 3.

**La heterogeneidad de providers baja de 2×2 a 3+1.** Es la condición que el
Caso 0.9 confirmó como la que produce actividad, y queda **declarada como
debilitada**, no como conservada.

**Una asimetría más, declarada:** `GeminiProvider` aplana los roles en un solo
string (el device B recibe el system prompt con prefijo `system:`), mientras
Groq recibe la lista con el system aparte. Ver su docstring. No se corrigió:
cambia la estructura del prompt que un device lee.

### Duración, piso y ritmo — el insumo es lo medido

**Insumo 1, vivo 03** (`experiments/vivo_03_criterio_local_log.json`):
`poll_interval = 5.0` → **5.2 s por vuelta** observados, 11.5 vueltas/min por
device, 12 vueltas en 62.4 s, **0 rate limits** con 2 devices sobre Groq.
**Insumo 2, serie IAP 1:** `poll_interval = 2.0`, duración 90–120 s.

Se toma `poll_interval = 5.0`, el **medido**, y no el 2.0 de la serie: con 2.0
el ritmo sería 2.5 veces el único que hay medido contra un provider real, y
con tres devices sobre la misma cuenta de Groq los 429 dejan de ser
improbables.

**Cuántos mensajes hacen falta.** El primer W espera **30 textos** y
`rebuild_every = 10`, así que el rebuild por volumen cae en 40, 50, 60, 70:
**≥ 2 rebuilds a los 50 textos**. Los mensajes **SYSTEM no entran al corpus**
(`system_to_corpus: False`), así que los 4 joins no cuentan: el objetivo son
**70 textos de device**, que en el canal son 74 mensajes.

**Cuánto tiene que durar.** Con N devices, `60/poll_interval` vueltas por
minuto y `p` = probabilidad de publicar por vuelta:

    mensajes/min = N · (60/poll_interval) · p = 4 · 12 · p = 48·p

`p` **no es un teorema y es parte de lo que esto mide**. El único dato es el
vivo 03: 2 INTERACT en 9 llamadas al gate (p ≈ 0.22), en un canal sin consigna
y casi en silencio. Con consigna y cuatro perspectivas debería ser mayor, y no
se predice.

    p = 0.40  →  70 / 19.2  =  3.6 min  =  219 s
    p = 0.25  →  70 / 12.0  =  5.8 min  =  350 s
    p = 0.15  →  70 /  7.2  =  9.7 min  =  583 s

`DURATION = 600 s` cubre hasta `p ≈ 0.15`. **No se corta al llegar a 70**: si
`p` es mayor, siguen hablando y el corpus pasa de 70 — más textos y más
rebuilds, que no estorban al objetivo.

**El piso.** `piso_vueltas + 2 ≤ vueltas por device` es la condición del
texto. Vueltas por device = `DURATION / s_por_vuelta`; con 5.2 s medidos son
115, y con 7 s pesimistas (el vivo 03 era casi todo skip; acá hay llamadas de
verdad) son **85**. Con `piso_vueltas = 6` el piso dispara en la vuelta **8**
(`piso + 2`, medido en el CP2b, no deducido): **8 ≤ 85**, con margen de un
orden.

Y 6 y no 12 (el default) **por el arranque sin seed**: el canal empieza en
silencio, y el piso es lo único que impide que el silencio sea punto fijo. Con
6, cada device reintenta la iniciativa cada 7 vueltas ≈ 36 s — unas 16 veces
en 600 s, 64 entre los cuatro. Con 12 serían 8 por device. Sigue **sin
calibrar**, como todo umbral del filtro, y el panel lo dice.

**Los 429 de Groq.** `llamadas/min = N·(60/poll)·(1+p)`. Los tres devices de
Groq, con p = 0.4: `3 · 12 · 1.4 ≈ 50` llamadas/min sobre la cuenta, pero
**repartidas en tres modelos distintos** (los límites de Groq son por modelo):
≈ 17 por modelo y por minuto. El vivo 03 hizo 0 rate limits. Si igual
aparecen, quedan marcados `rate_limit: True` en la traza de la vuelta y en
`device_log.jsonl` — que es la medición de que el ritmo no entró.

### Dónde queda todo

Un solo directorio: `experiments/_state_S2-C0/`. El nombre sigue al campo
`case` del panel, que es literalmente `"S2-C0"` (`ckm_monitor.CASE`), y es el
que el texto escribe. El nombre técnico de la corrida es `serie2_caso0`.

Ahí van, por el punto 3: `corpus_state.json` (con el historial de versiones de
W adentro), `corpus_G_state.json`, `monitor_trajectory.jsonl`,
`rebuild_decisions.jsonl`, `rebuild_state.json`, `channel_messages.jsonl`,
`rejected_attempts.jsonl`, `channel_ticks.jsonl`, `device_decisions.jsonl`,
`call_filter_records.jsonl`, `device_log.jsonl`. Append-only y durante la
corrida. El JSON del final es un resumen **además** de eso, no en su lugar.

**Lo de COCO no se publica en el canal** (delamor): queda en
`monitor_trajectory.jsonl`.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import platform
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_PATH)

RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from iap_chatroom.autonomous_device import AutonomousDevice          # noqa: E402
from iap_chatroom.local_criterion import (                            # noqa: E402
    LocalCriterion,
    LocalCriterionThresholds,
)
from iap_chatroom.providers.gemini_provider import GeminiProvider     # noqa: E402
from iap_chatroom.providers.groq_provider import GroqProvider         # noqa: E402

MCP_URL = "http://localhost:7860/mcp"
STATE_DIR = RAIZ / "experiments" / "_state_S2-C0"

NOMBRE = "serie2_caso0"

# ── los números, todos declarados arriba en el docstring ────────────────────
POLL_INTERVAL = 5.0      # el medido en el vivo 03
DURATION = 600.0         # cubre p ≈ 0.15 para 70 textos de device
PISO_VUELTAS = 6         # piso + 2 = 8 ≤ 85 vueltas por device (pesimista)
TEXTOS_OBJETIVO = 70     # textos de device; ≥ 2 rebuilds a los 50

# ── los prompts ─────────────────────────────────────────────────────────────

# El bloque común de la serie, **igual que `SYSTEM_PROMPT_04A`** (Caso 0.4a):
# qué es el canal y qué puede hacer el device. Sin explicación de los campos de
# CKM, que es lo que 0.4a aisló y lo que delamor pide para este caso.
BLOQUE_COMUN = """You are {device_id}.

You are in an IAP chatroom — a shared space with no turn structure.
Other devices (AI and Human) may be present.

What you can do:
- Read the full chat history, including your own prior messages
- Publish a message — to anyone, about anything, at any time
- Do nothing — operational silence (OP_SILENCE) means not publishing. No announcement needed."""

# La consigna parcial, textual del orden de delamor. El corchete se reemplaza
# por **la perspectiva de ese device y nada más**.
CONSIGNA = """This channel is about an open question with no right answer: how should the water of a growing city be organized? Your perspective is {perspectiva}. There are other perspectives in the channel. What they say may move the foundations of yours, even of what you have already said, and what you say may move theirs."""

# Las cuatro perspectivas. **Esta lista no va a ningún prompt**: cada device
# recibe su string y nunca los otros tres.
PERSPECTIVAS = {
    "A": "where the water comes from",
    "B": "how it is distributed",
    "C": "who pays and how much",
    "D": "what could go wrong in the next 20 years",
}

# El cuarteto, en orden arbitrario y declarado. Un solo lugar: si un modelo se
# cae, acá se cambia y en ninguna otra parte.
DEVICES = (
    # (letra, device_id neutro, provider, modelo)
    ("A", "device_a", "groq", "openai/gpt-oss-120b"),
    ("B", "device_b", "gemini", "gemini-2.5-flash"),
    ("C", "device_c", "groq", "openai/gpt-oss-20b"),
    ("D", "device_d", "groq", "qwen/qwen3.8-27b"),
)

_PROVIDERS = {"groq": GroqProvider, "gemini": GeminiProvider}


def system_prompt(device_id: str, letra: str) -> str:
    """El bloque común más la consigna parcial. Sólo la perspectiva propia."""
    return (BLOQUE_COMUN.format(device_id=device_id)
            + "\n\n"
            + CONSIGNA.format(perspectiva=PERSPECTIVAS[letra]))


def _umbrales() -> LocalCriterionThresholds:
    return LocalCriterionThresholds(piso_vueltas=PISO_VUELTAS)


def construir_devices() -> list[AutonomousDevice]:
    """
    Los cuatro devices, cada uno con **su propio** filtro y el `state_dir` del
    caso.

    El filtro tiene estado (cuántas vueltas sin llamar), y ese estado es por
    device: uno compartido haría que el piso de uno reseteara el del otro.

    El `state_dir` se pasa y nada más: la lógica de qué se escribe y cuándo
    está en IAP (`run_store`), no acá. Es lo que delamor pide con *"sin lógica
    en los drivers"*.
    """
    devices = [
        AutonomousDevice(
            device_id=did,
            provider=_PROVIDERS[prov](model=modelo),
            system_prompt=system_prompt(did, letra),
            mcp_url=MCP_URL,
            poll_interval=POLL_INTERVAL,
            local_criterion=LocalCriterion(umbrales=_umbrales()),
            state_dir=STATE_DIR,
        )
        for letra, did, prov, modelo in DEVICES
    ]
    filtros = [id(d.local_criterion) for d in devices]
    assert len(set(filtros)) == len(devices), (
        "dos devices comparten el filtro: el piso de uno resetearía al otro"
    )
    return devices


# ── preflight: los cuatro identificadores, hoy ──────────────────────────────

async def preflight() -> dict:
    """
    Que los cuatro modelos respondan, **antes** de tocar el canal.

    El texto pide *"verificá que los cuatro identificadores respondan hoy"*.
    Acá queda como puerta del disparo y no como una verificación que alguien
    hizo una vez: un modelo que el provider retiró —le pasó a
    `llama-3.3-70b-versatile` entre que se escribió el orden y hoy— tiene que
    frenar el caso acá, no aparecer como un silencio en la vuelta 3 que
    después hay que atribuir.

    Una llamada por device, con el mismo camino de claves que usa el caso.
    """
    resultados = []
    for letra, did, prov, modelo in DEVICES:
        p = _PROVIDERS[prov](model=modelo)
        t0 = time.monotonic()
        try:
            r = await p.complete(
                [{"role": "user", "content": "Reply with exactly one word: OK"}]
            )
            resultados.append({
                "letra": letra, "device_id": did, "provider": prov,
                "model": modelo, "responde": True,
                "respuesta": r.strip()[:40],
                "latencia_s": round(time.monotonic() - t0, 3),
            })
        except Exception as e:                  # noqa: BLE001 — se reporta
            resultados.append({
                "letra": letra, "device_id": did, "provider": prov,
                "model": modelo, "responde": False,
                "excepcion": type(e).__name__, "mensaje": str(e)[:200],
                "latencia_s": round(time.monotonic() - t0, 3),
            })
    return {
        "todos_responden": all(r["responde"] for r in resultados),
        "devices": resultados,
    }


def imprimir_preflight(pre: dict) -> None:
    print("=== preflight: los cuatro identificadores ===")
    for r in pre["devices"]:
        if r["responde"]:
            print(f"  {r['letra']} {r['device_id']:9s} {r['provider']:7s} "
                  f"{r['model']:24s} OK   {r['latencia_s']}s")
        else:
            print(f"  {r['letra']} {r['device_id']:9s} {r['provider']:7s} "
                  f"{r['model']:24s} FALLA {r['excepcion']}: {r['mensaje']}")
    print(f"  todos responden: {pre['todos_responden']}")


# ── estado de partida y preservación ────────────────────────────────────────

ARCHIVOS_DE_ESTADO = (
    "corpus_state.json", "corpus_G_state.json", "monitor_trajectory.jsonl",
    "rebuild_decisions.jsonl", "rebuild_state.json",
    "channel_messages.jsonl", "rejected_attempts.jsonl",
    "channel_ticks.jsonl", "device_decisions.jsonl",
    "call_filter_records.jsonl", "device_log.jsonl",
)


def preservar_estado() -> list[str]:
    """
    Mueve el estado anterior a `process/` con timestamp. **No borra**: el
    mecanismo canónico de la serie (`prepare_state` en los `test_caso_*`), y
    el criterio de `process/README_process.md` — el corpus previo es evidencia
    del refinamiento, no ruido a descartar.
    """
    destino = RAIZ / "process"
    destino.mkdir(exist_ok=True)
    movidos = []
    for f in ARCHIVOS_DE_ESTADO:
        src = STATE_DIR / f
        if src.exists():
            dst = destino / f"{f}.bak_{int(time.time())}_{NOMBRE}"
            shutil.move(str(src), str(dst))
            movidos.append(str(dst))
            print(f"[preservar] {f} -> {dst}")
    if not movidos:
        print(f"[preservar] {STATE_DIR} ya estaba limpio")
    return movidos


async def estado_de_partida() -> dict:
    """Se lee ANTES de arrancar, por MCP, y se declara en el log."""
    from fastmcp import Client

    async with Client(MCP_URL) as c:
        monitor = (await c.call_tool("get_monitor_state", {})).data
        clock = (await c.call_tool("get_clock", {})).data
        mensajes = (await c.call_tool("get_messages", {"since": None})).data
    return {
        "monitor_state": monitor,
        "clock": clock,
        "mensajes_en_el_canal": len(mensajes),
    }


# ── el caso ─────────────────────────────────────────────────────────────────

async def correr() -> dict:
    pre = await preflight()
    imprimir_preflight(pre)
    if not pre["todos_responden"]:
        # **No se arranca con un device muerto.** Tres devices y un silencio
        # sin causa atribuible no es este caso.
        return {
            "que_es": f"ESTO MIDE — {NOMBRE}, ABORTADO EN EL PREFLIGHT",
            "preflight": pre,
            "motivo": "al menos un identificador no responde hoy",
        }

    partida = await estado_de_partida()
    print(f"\n=== {NOMBRE} — 4 devices, sin seed, {DURATION:.0f}s ===")
    print(f"state_dir = {STATE_DIR}")
    print(f"corpus de partida = {partida['monitor_state']['corpus_size']} textos, "
          f"{partida['mensajes_en_el_canal']} mensajes en el canal")

    devices = construir_devices()

    t0 = time.time()
    resultados = await asyncio.gather(
        *(d.run(duration=DURATION) for d in devices),
        return_exceptions=True,
    )
    segundos = round(time.time() - t0, 2)

    errores_fatales = []
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
        firma = (await c.call_tool("get_firma", {})).data

    umb = _umbrales()
    return {
        "que_es": f"ESTO MIDE — {NOMBRE}: COCO contra un vivo de IAP",
        "objetivo_declarado_como_sesgo": (
            'terminar con la expresion "COCO no se conecto nunca a un vivo '
            'de IAP". Por limites, el objetivo es QUE SUCEDA.'
        ),
        "orden": (
            "docs/opus/textos_para_code/"
            "TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md"
        ),
        "preflight": pre,
        "estado_de_partida_leido_por_MCP": partida,
        "declarado": {
            "nombre_tecnico": NOMBRE,
            "sin_seed": True,
            "sin_agentes": True,
            "sin_coordinador": True,
            "devices": [
                {"letra": l, "device_id": d, "provider": p, "model": m,
                 "perspectiva": PERSPECTIVAS[l]}
                for l, d, p, m in DEVICES
            ],
            "poll_interval_s": POLL_INTERVAL,
            "duration_s": DURATION,
            "textos_de_device_objetivo": TEXTOS_OBJETIVO,
            "umbrales": {
                "dt_minimo_s": umb.dt_minimo_s,
                "piso_vueltas": umb.piso_vueltas,
                "tasa_auditoria": umb.tasa_auditoria,
                "tasa_auditoria_pase": umb.tasa_auditoria_pase,
            },
            "umbrales_calibrados": umb.calibrado,
            "state_dir": str(STATE_DIR),
            "heterogeneidad_de_providers": (
                "3 Groq + 1 Google. DEBILITADA respecto del 2x2 del orden "
                "original: los dos identificadores de Anthropic dan 401 y el "
                "llama de Groq da 404. Reemplazo confirmado por delamor."
            ),
            "asimetria_declarada": (
                "GeminiProvider aplana los roles en un solo string; el device "
                "B recibe el system prompt con prefijo 'system:'. Groq recibe "
                "la lista con el system aparte. No se corrigio."
            ),
            "system_prompts": {
                d: system_prompt(d, l) for l, d, _, _ in DEVICES
            },
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
            "firma": firma,
        },
        "archivos_del_state_dir": sorted(
            p.name for p in STATE_DIR.iterdir()
        ) if STATE_DIR.exists() else [],
    }


def imprimir_cierre(res: dict) -> None:
    """Lo mínimo para mirar el objetivo sin abrir el JSON."""
    if "canal" not in res:
        print(f"\n{res['que_es']}")
        return
    mon = res["canal"]["monitor_state"]
    coco = mon.get("coco") or {}
    print("\n=== el objetivo ===")
    print(f"coco.connected          : {coco.get('connected')}")
    print(f"coco.generation         : {coco.get('generation')}")
    print(f"coco.n_evaluations      : {coco.get('n_evaluations_received')}")
    print(f"coco.w_version_id       : {str(coco.get('w_version_id'))[:16]}")
    print(f"coco.triggers           : {coco.get('triggers')}")
    print("\n=== el campo ===")
    print(f"corpus_size (textos)    : {mon.get('corpus_size')}")
    print(f"message_count           : {mon.get('message_count')}")
    print(f"D_ckm                   : {mon.get('D_ckm')}")
    print(f"temp_signal             : {mon.get('temp_signal')}")
    print(f"rebuild_senal / causa   : {mon.get('rebuild_senal')} / "
          f"{mon.get('rebuild_causa')}")
    print(f"n_decisiones_registradas: {mon.get('n_decisiones_registradas')}")
    print("\n=== por device ===")
    for d in res["por_device"]:
        c = d["costo"]
        print(f"  {c['device_id']:9s} {str(c['model']):24s} "
              f"vueltas={c['vueltas']:3d} llamadas={c['llamadas_llm']:3d} "
              f"429={c['errores_rate_limit']} "
              f"decisiones={c['decisiones_por_tipo']}")
    print(f"\nmensajes en el canal    : {res['canal']['n_mensajes']} "
          f"(incluye los joins SYSTEM, que NO entran al corpus)")
    print(f"archivos en el state_dir: {res['archivos_del_state_dir']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{NOMBRE} — no lo corre Code")
    parser.add_argument("--preflight", action="store_true",
                        help="sólo verifica los cuatro modelos y sale")
    parser.add_argument("--reset", action="store_true",
                        help="preserva el estado anterior en process/ y sale")
    parser.add_argument("salida", nargs="?", default=None,
                        help="JSON de salida")
    args = parser.parse_args()

    if args.reset:
        preservar_estado()
        sys.exit(0)

    if args.preflight:
        imprimir_preflight(asyncio.run(preflight()))
        sys.exit(0)

    salida = (Path(args.salida) if args.salida
              else RAIZ / f"experiments/{NOMBRE}_log.json")
    try:
        res = asyncio.run(correr())
    except BaseException as e:               # noqa: BLE001 — se reporta entero
        res = {
            "que_es": f"ESTO MIDE — {NOMBRE}, ABORTADO",
            "excepcion": type(e).__name__,
            "traceback": traceback.format_exc(),
        }
    tmp = salida.with_suffix(salida.suffix + ".tmp")
    tmp.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    tmp.replace(salida)
    imprimir_cierre(res)
    print(f"\nlog -> {salida}")
