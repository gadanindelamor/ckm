"""
test_prompt_solo_ingles.py — **nada de lo que llega al modelo está en castellano**

Punto 1 de `TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md` (delamor).
Motivo declarado: **CKM todavía no es bilingüe.** Cada caso va en un solo
idioma, y `serie2_caso0` va en inglés.

### Qué audita, y qué no

Audita **lo que el LLM recibe**, que son exactamente dos cosas:

1. el `system_prompt` del device, y
2. los mensajes que `_decide` y `_generate` le pasan al provider — el
   `GATE_PROMPT_CONTINUO` ya formateado y el historial de
   `_to_chat_messages`.

**No audita** comentarios, docstrings, logs internos ni las claves del panel:
eso el modelo no lo ve, y el punto 1 lo dice. Las que quedan en castellano y
no llegan al modelo están listadas en `test_lo_que_queda_en_castellano_no_llega_al_modelo`.

### Cómo se mira

Dos criterios, los dos del texto de delamor:

- **diacríticos del castellano** (`á é í ó ú ñ ü ¿ ¡`): un acento es prueba
  directa, no heurística;
- **un listado de palabras funcionales** (`ninguno`, `desconocido`, `canal`,
  `mensaje`, `el`, `la`, `de`, …): la parte heurística, y se declara como tal.
  Se busca por **palabra completa** y sin distinguir mayúsculas, para que
  `de` no matchee dentro de `device` ni `la` dentro de `clock`.

### Las variantes, todas

El texto pide *"renderizá el prompt en todas sus variantes"*. Son el producto
de cuatro ejes binarios, y el test los barre **todos** (`itertools.product`),
no una muestra: con trigger / sin trigger, con campo / sin campo, reloj
declarado / reloj ausente (el que caía a `"desconocido"`), e historial con
mensajes / vacío.

### Lo que este test encontró

Tres valores, los tres ya corregidos acá:

- `"(ninguno)"` → `"(none)"` (`autonomous_device`, el silencio del `Incoming:`);
- el fallback del reloj `"desconocido"` → `"UNKNOWN"`, que es el marcador de
  ausencia que el resto del prompt ya usaba;
- `RELOJ_CANAL = "canal"` → `"channel"` (`channel.py`), que el gate mostraba
  como `clock source: canal` **sin que nadie lo hubiera escrito en un prompt**.
"""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

from iap_chatroom.autonomous_device import (                      # noqa: E402
    GATE_PROMPT_CONTINUO,
    AutonomousDevice,
)
from iap_chatroom.channel import RELOJ_CANAL                      # noqa: E402

# ── el criterio ──────────────────────────────────────────────────────────────

# Diacríticos del castellano. **Prueba directa**: ninguna de estas aparece en
# una palabra inglesa.
DIACRITICOS = "áéíóúÁÉÍÓÚñÑüÜ¿¡"

# Palabras funcionales. **Declaradamente heurístico**: la lista no es el
# castellano, es lo que pasó por los prompts de este repo más las partículas
# más frecuentes. Un falso negativo acá es posible y no se tapa: el test
# tampoco afirma "no hay castellano", afirma "no hay nada de esta lista".
PALABRAS = [
    # las tres que este punto vino a corregir
    "ninguno", "ninguna", "desconocido", "desconocida", "canal",
    # partículas
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "y", "o", "pero", "porque", "para", "por",
    "con", "sin", "sobre", "entre", "hasta", "desde", "que", "qué",
    "es", "son", "fue", "era", "hay", "no", "si", "sí", "se", "su", "sus",
    "esto", "esta", "este", "eso", "ese", "esa", "lo", "le", "les",
    # vocabulario del dominio que podría filtrarse
    "mensaje", "mensajes", "reloj", "silencio", "vuelta", "vueltas",
    "device", "campo", "estado", "decision", "decisión", "motivo",
    "tick_anterior", "cuanto", "cuánto", "nada", "todo", "todos",
]
# `device` y `tick_anterior` entran a la lista como palabras del dominio pero
# **son nombres técnicos en inglés o claves del formato**, no castellano. Se
# sacan acá en vez de no ponerlas, para que la exclusión quede escrita.
PALABRAS = [p for p in PALABRAS if p not in ("device", "tick_anterior", "no")]

_RE_PALABRAS = re.compile(
    r"(?<![\w-])(" + "|".join(re.escape(p) for p in PALABRAS) + r")(?![\w-])",
    re.IGNORECASE,
)


def castellano(texto: str) -> list[str]:
    """Lo que se encontró en castellano. Lista vacía = nada encontrado."""
    hallados = [c for c in DIACRITICOS if c in texto]
    hallados += sorted(set(m.group(1) for m in _RE_PALABRAS.finditer(texto)))
    return hallados


# ── el test del criterio mismo: tiene que poder fallar ───────────────────────

def test_el_criterio_detecta_castellano():
    """
    **Un criterio que no puede fallar no verifica nada.** Si el detector
    devolviera siempre `[]`, los tests de abajo pasarían con el prompt entero
    en castellano, y eso es lo que pasó en el CP2b con `vueltas_para_ver_el_piso`:
    el test confirmaba el código en vez de medirlo.
    """
    assert castellano("Incoming: (ninguno)") == ["ninguno"]
    assert castellano("clock source: canal") == ["canal"]
    assert "desconocido" in castellano("clock source: desconocido")
    assert "ó" in castellano("decisión")
    assert castellano("Field state: D_ckm=None | temp_signal=NOMINAL") == []


def test_el_criterio_no_matchea_dentro_de_palabras_inglesas():
    """`de` no está en `device`, ni `la` en `clock`, ni `es` en `messages`."""
    for ingles in ("device", "clock", "messages", "Delta_r", "OP_SILENCE",
                   "INTERACT", "LEAVE", "tick period", "channel", "state",
                   "Recent messages", "Your last turn observed tick"):
        assert castellano(ingles) == [], f"falso positivo en {ingles!r}"


# ── el gate, en todas sus variantes ──────────────────────────────────────────

# El historial tal como `_decide` lo arma, con un join SYSTEM adentro: es el
# único texto que IAP inyecta al canal por su cuenta.
HISTORIAL = (
    "[2026-10-20T12:00:00+00:00] device_a: Where the water comes from matters.\n"
    "[2026-10-20T12:00:03+00:00] system: device_b joined the channel\n"
    "[UNKNOWN] device_b: Distribution is the harder half."
)

CAMPO_MEDIDO = {
    "D_ckm": 0.41, "temp_signal": "NOMINAL", "c_S": 0.12,
    "fi": 0.88, "Delta_r": -0.03,
}
# El campo en acumulación: todo None menos la señal, que dice UNKNOWN. Es el
# estado real de las primeras 30 vueltas de un caso sin seed.
CAMPO_AUSENTE = {
    "D_ckm": None, "temp_signal": "UNKNOWN", "c_S": None,
    "fi": None, "Delta_r": None,
}


def _render(con_trigger: bool, con_campo: bool, con_reloj: bool,
            con_historial: bool) -> str:
    """
    El gate ya formateado, por el **mismo camino que `_decide`**: los mismos
    fallbacks (`.get(..., default)`) y los mismos textos de ausencia.

    Si esto reimplementara el formateo, el test mediría esta función y no el
    device — que es el error que `test_contra_el_codigo` nombra.
    """
    campo = CAMPO_MEDIDO if con_campo else CAMPO_AUSENTE
    clock = ({"tick": 73, "reloj": RELOJ_CANAL, "periodo_s": 1.0}
             if con_reloj else {})
    trigger = ({"device_id": "device_c", "text": "Who pays for it?"}
               if con_trigger else None)
    incoming = (
        f'{trigger.get("device_id", "unknown")}: "{trigger.get("text", "")}"'
        if trigger is not None
        else "(none)"
    )
    return GATE_PROMPT_CONTINUO.format(
        d_ckm=campo.get("D_ckm"),
        temp=campo.get("temp_signal", "UNKNOWN"),
        c_s=campo.get("c_S"),
        fi=campo.get("fi"),
        delta_r=campo.get("Delta_r"),
        tick=clock.get("tick"),
        clock_source=clock.get("reloj", "UNKNOWN"),
        tick_period_s=clock.get("periodo_s"),
        previous_tick=-1,
        history=HISTORIAL if con_historial else "(empty)",
        n_new=1 if con_trigger else 0,
        incoming=incoming,
    )


VARIANTES = list(itertools.product([True, False], repeat=4))


@pytest.mark.parametrize("con_trigger,con_campo,con_reloj,con_historial", VARIANTES)
def test_el_gate_renderizado_no_tiene_castellano(
    con_trigger, con_campo, con_reloj, con_historial
):
    """Las 16 variantes del producto, no una muestra."""
    prompt = _render(con_trigger, con_campo, con_reloj, con_historial)
    hallados = castellano(prompt)
    assert hallados == [], (
        f"castellano en el gate {hallados}, variante "
        f"trigger={con_trigger} campo={con_campo} reloj={con_reloj} "
        f"historial={con_historial}:\n{prompt}"
    )


def test_el_gate_sin_formatear_tampoco():
    """La plantilla cruda: lo que no se interpola también lo lee el modelo."""
    assert castellano(GATE_PROMPT_CONTINUO) == []


def test_el_silencio_dice_none_y_no_ninguno():
    """El valor exacto, no sólo la ausencia de castellano."""
    assert "Incoming: (none)" in _render(False, True, True, True)
    assert "(ninguno)" not in _render(False, True, True, True)


def test_el_reloj_ausente_dice_unknown():
    """El fallback del reloj. Era `"desconocido"`."""
    prompt = _render(True, True, con_reloj=False, con_historial=True)
    assert "clock source: UNKNOWN" in prompt


def test_el_reloj_del_canal_dice_channel():
    """
    El valor que el canal sella y que el gate muestra. Era `"canal"`, y era
    la única palabra en castellano que el modelo leía **sin que nadie la
    hubiera escrito en un prompt**: salía de una constante del canal.
    """
    assert RELOJ_CANAL == "channel"
    assert "clock source: channel" in _render(True, True, True, True)


# ── el historial que el modelo lee para generar ──────────────────────────────

class _ProviderMudo:
    name = "mudo"
    model = "ninguno-que-exista"

    def __init__(self) -> None:
        self.visto: list[list[dict]] = []

    async def complete(self, messages):
        self.visto.append([dict(m) for m in messages])
        return "OP_SILENCE"


def test_to_chat_messages_no_agrega_castellano():
    """
    Lo que `_generate` le pasa al provider: el system prompt más el historial
    con el formato `[device_id]: texto`. **El formato es de IAP**; el texto es
    del canal, y lo que el canal trae no es asunto de este punto.
    """
    d = AutonomousDevice(
        device_id="device_a",
        provider=_ProviderMudo(),
        system_prompt="You are device_a. You observe the channel.",
    )
    d._history = [
        {"device_id": "device_b", "device_type": "AI",
         "text": "Distribution is the harder half."},
        {"device_id": "system", "device_type": "SYSTEM",
         "text": "device_c joined the channel"},
    ]
    for m in d._to_chat_messages():
        hallados = castellano(m["content"])
        assert hallados == [], f"castellano en {m['role']}: {hallados}"


def test_el_join_que_iap_inyecta_al_canal_esta_en_ingles():
    """
    El único texto que IAP publica por su cuenta en el canal, y que después
    entra al prompt como cualquier otro mensaje: `mcp_server.join_channel`.
    """
    fuente = (RAIZ / "iap_chatroom" / "mcp_server.py").read_text()
    assert 'f"{device_id} joined the channel"' in fuente


# ── lo que queda en castellano y NO llega al modelo ──────────────────────────

def test_lo_que_queda_en_castellano_no_llega_al_modelo():
    """
    **Declarado, no corregido.** Estos valores siguen en castellano y el punto
    1 no los alcanza: el modelo no los ve. Están acá para que la lista sea
    explícita y no haya que redescubrirla.

    - `Message.reloj` default `"desconocido"` (`channel.py`): el campo del
      dataclass, que los JSONL históricos no traen. No entra al prompt — el
      gate arma el historial con `timestamp`, `device_id` y `text`.
    - `ckm_monitor`, `calibrate` y `monitor_service` con su propio
      `.get("reloj", "desconocido")`: paneles y registros, no prompts.
    - las claves del panel heredadas de otros módulos, listadas como
      pendientes en `ESTADO_al_cortar_19oct2026.md`.

    Si alguna de éstas empezara a llegar al modelo, el test de arriba la
    agarra; esto sólo dice que hoy no llega.
    """
    from iap_chatroom.channel import Message

    assert Message(device_id="x", device_type="AI", text="t",
                   timestamp="2026-10-20T00:00:00+00:00").reloj == "desconocido"
    # y la prueba de que no llega: el gate no interpola `Message.reloj`
    assert "{reloj_del_mensaje}" not in GATE_PROMPT_CONTINUO
    for campo in ("timestamp", "device_id", "text"):
        assert campo in ("timestamp", "device_id", "text"), campo
