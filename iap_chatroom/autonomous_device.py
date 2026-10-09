"""
autonomous_device.py — AutonomousDevice

Device AI autónomo para IAP Chatroom. A diferencia de los scripts de
simulación (test_iap_simulation*.py), que orquestan turnos en secuencia
fija, AutonomousDevice corre su propio loop asíncrono de polling MCP.

Caso 0.4: el loop implementa el ciclo ODA (Observación · Decisión ·
Acción) explícito. _observe() recolecta campo CKM + historial del canal
(sin LLM). _decide() evalúa esa observación con el gate LLM y devuelve
INTERACT u OP_SILENCE. _interact() ejecuta la decisión: publica o no.

Sin bootstrap bypass: D_ckm=None es una observación de campo válida
(el corpus todavía está acumulando), no un caso especial que salte el
gate. El device decide igual, con el campo que haya.
"""

from __future__ import annotations

import asyncio
import re
import time
from typing import Optional

from fastmcp import Client

from iap_chatroom.providers.base import ChatMessage, Provider

# La decisión que no hubo. **No es un valor de la escala**: es el estado del
# que observa cuando el provider no respondió (§19). No autoriza ninguna
# acción, igual que OP_SILENCE, pero se distingue de él: OP_SILENCE lo decidió
# el modelo, UNKNOWN significa que no se pudo decidir.
DECISION_UNKNOWN = "UNKNOWN"

# Atributos donde los SDK suelen poner el código HTTP. **Se miran primero**:
# un 429 en `status_code` es un dato, no una coincidencia de texto.
_ATRIBUTOS_STATUS = ("status_code", "status", "code", "http_status")

# Firmas en el texto del error. **Respaldo, y declaradamente heurístico**: si
# el SDK no expone el código, se busca por texto. Puede dar falsos positivos
# —un mensaje que mencione "quota" sin ser un 429— y falsos negativos. Si no
# matchea, el error queda como genérico y **igual se registra**: no se pierde.
_FIRMAS_RATE_LIMIT = ("429", "rate limit", "rate_limit", "too many requests",
                      "quota", "ratelimit")


def _es_rate_limit(e: Exception) -> tuple:
    """
    Si la excepción es un rate limit, y **cómo se supo**.

    Returns: (es_rate_limit, metodo) con metodo ∈ {"status_code", "texto", None}.
    El método se registra: un 429 leído del `status_code` es un dato; uno
    inferido del texto es una heurística, y la traza tiene que decir cuál fue.
    """
    for attr in _ATRIBUTOS_STATUS:
        valor = getattr(e, attr, None)
        if isinstance(valor, bool):
            continue
        if isinstance(valor, int) and valor == 429:
            return True, "status_code"
        if isinstance(valor, str) and valor.strip() == "429":
            return True, "status_code"
    texto = f"{type(e).__name__}: {e}".lower()
    if any(f in texto for f in _FIRMAS_RATE_LIMIT):
        return True, "texto"
    return False, None

GATE_PROMPT_04 = """Field state:
D_ckm={d_ckm} | temp_signal={temp} | c_S={c_s} | fi={fi} | Delta_r={delta_r}

Recent messages:
{history}

Incoming: {sender}: "{text}"

Respond with exactly one word: INTERACT or OP_SILENCE."""

# ─────────────────────────────────────────────────────────────────────────────
# GATE DEL ODA CONTINUO — **DECLARADO PARA QUE DELAMOR LO LEA ANTES DE LA
# CORRIDA VIVA.** Cambia lo que el device puede decidir, y eso es de delamor
# (decisión del 8 oct, T4). Hasta esa lectura, sólo corre con stubs.
#
# Tres diferencias con GATE_PROMPT_04, y cada una tiene una razón:
#
#  1. **Tres opciones, no dos.** LEAVE entra como acción con su primitiva
#     (`leave_channel`), por decisión propia y no porque venció `duration`
#     (TASK §1). Antes irse no era una decisión: era el final del loop.
#  2. **El tick y el silencio están en la observación, no en la pregunta.**
#     El canal no calcula Δt por el device: le da el tick y los timestamps, y
#     evaluar el tiempo es parte de decidir (TASK §1, fase D).
#  3. **Puede no haber mensaje nuevo.** `Incoming: (ninguno)` es el silencio, y
#     es un dato de la observación como cualquier otro. El device decide igual.
#
# Lo que NO dice, a propósito: no sugiere qué hacer con el silencio, ni que
# hablar sea mejor que callar, ni que un Δt grande pida acción. Free will
# (TRUST): *"No one is obligated to participate."*
GATE_PROMPT_CONTINUO = """Field state:
D_ckm={d_ckm} | temp_signal={temp} | c_S={c_s} | fi={fi} | Delta_r={delta_r}

Channel clock: tick={tick} (clock source: {reloj}, tick period: {periodo_s}s)
Your last turn observed tick {tick_anterior}.

Recent messages (channel timestamps, UTC):
{history}

New since your last turn: {n_nuevos}
Incoming: {incoming}

You are not obligated to act. Respond with exactly one word:
INTERACT (publish), LEAVE (leave the channel), or OP_SILENCE (do nothing this turn)."""


def _strip_own_prefix(text: str, device_id: str) -> str:
    """
    Elimina prefijos `[device_id]:` anidados al inicio del texto.

    El modelo ve `[device_id]: texto` en su propio historial (formato
    de _to_chat_messages) e imita el prefijo en su propia respuesta;
    sin este strip, el prefijo se anida uno por turno.
    """
    pattern = rf"^(\[{re.escape(device_id)}\]:\s*)+"
    return re.sub(pattern, "", text).strip()


def _coalesce(messages: list[ChatMessage]) -> list[ChatMessage]:
    """Fusiona mensajes consecutivos del mismo role (requisito de alternancia de Anthropic)."""
    if not messages:
        return messages
    merged: list[ChatMessage] = [dict(messages[0])]
    for m in messages[1:]:
        if m["role"] == merged[-1]["role"]:
            merged[-1]["content"] = merged[-1]["content"] + "\n" + m["content"]
        else:
            merged.append(dict(m))
    return merged


class AutonomousDevice:
    """
    Device AI autónomo para IAP Chatroom.
    Loop: recibe mensajes via polling MCP → ciclo ODA (observar campo +
    historial, decidir INTERACT/OP_SILENCE, actuar) → OP_SILENCE es
    salida real, no omisión.
    """

    def __init__(
        self,
        device_id: str,
        provider: Provider,        # de iap_chatroom/providers/
        system_prompt: str,
        mcp_url: str = "http://localhost:7860/mcp",
        poll_interval: float = 2.0,   # segundos entre vueltas del ciclo
        trigger_mode: str = "continuo",
    ):
        """
        `trigger_mode` admite **un solo valor: "continuo"** (CP2a, P11).

        El modo viejo —un ODA por mensaje ajeno— **no se mantiene como modo
        vivo**: quedó congelado en `process/iap_series_freeze_20261008/`, con
        la serie que corrió bajo él. No está detrás de un flag: el loop se
        reemplazó. El parámetro existe para que el modo quede **declarado en
        el log del device**, no para poder volver atrás.

        `poll_interval` es el ritmo de la vuelta, y hoy lo fija el device
        (TASK §1). No hay mínimo declarado ni WAIT: eso es Calibración.

        **El ritmo contra el límite de la cuenta** (CP2v, pedido de Opus). Sin criterio local,
        cada vuelta cuesta **1 llamada al gate + 1 si actúa**, así que con N
        devices durante T segundos:

            llamadas ≈ N · (T / poll_interval) · (1 + p)

        y por minuto, por device: `60 / poll_interval` como piso, el doble si
        actúa siempre. Con `poll_interval = 2.0` son **30 a 60 por minuto y por
        device**.

        **El límite de la cuenta es UNKNOWN**: se lee en la consola del
        provider, y no lo invento. `ritmo_declarado()` devuelve el cálculo para
        poder compararlo contra ese número cuando exista; si el provider
        devuelve 429, queda marcado `rate_limit: True` en la traza de la
        vuelta, que es la medición de que el ritmo no entró.
        """
        if trigger_mode != "continuo":
            raise ValueError(
                f"trigger_mode={trigger_mode!r} no existe. El único modo vivo es "
                '"continuo". El modo por mensaje quedó congelado en '
                "process/iap_series_freeze_20261008/ junto con la serie IAP que "
                "corrió bajo él (CP0b); no está detrás de un flag."
            )
        self.device_id = device_id
        self.provider = provider
        self.system_prompt = system_prompt
        self.mcp_url = mcp_url
        self.poll_interval = poll_interval
        self.trigger_mode = trigger_mode
        self._history: list[dict] = []
        # message_id de todo lo ya visto: el borde de `since` puede repetir un
        # mensaje, y se descarta por id (T2).
        self._vistos: set[str] = set()
        self._tick_anterior: int = -1
        # lo que el device decidió, vuelta por vuelta. Traza propia.
        self._decisiones: list[dict] = []
        # Llamadas al LLM efectivamente hechas, acumuladas. La traza de cada
        # vuelta guarda el delta: con el criterio local (CP2b) una vuelta
        # puede costar cero, así que "vueltas" deja de ser "llamadas" y hay
        # que contarlas, no inferirlas (pedido de delamor para el primer vivo).
        self._llamadas_llm: int = 0
        # Errores del provider, acumulados, para poder atribuir un silencio:
        # el modelo que calla, el canal que pierde, o la infraestructura que
        # falla, son tres cosas distintas.
        self._errores_llm: list[dict] = []
        # Respuestas del gate que no eran ninguna de las tres palabras. Se
        # registran aparte de los errores del provider: el provider respondió,
        # lo que no se pudo fue leer la respuesta. Son dos causas distintas de
        # la misma consecuencia (UNKNOWN), y para atribuir hay que separarlas.
        self._ilegibles: list[dict] = []
        self._se_fue: bool = False
        # Inicio y fin del run, para el ritmo OBSERVADO (F5). None hasta que
        # corra: sin corrida no hay ritmo que medir, y eso es UNKNOWN, no 0.
        self._t_inicio: Optional[float] = None
        self._t_fin: Optional[float] = None

    def _to_chat_messages(self) -> list[ChatMessage]:
        chat: list[ChatMessage] = [{"role": "system", "content": self.system_prompt}]
        for m in self._history:
            role = "assistant" if m["device_id"] == self.device_id else "user"
            chat.append({"role": role, "content": f"[{m['device_id']}]: {m['text']}"})
        system_msgs = [c for c in chat if c["role"] == "system"]
        turn_msgs = _coalesce([c for c in chat if c["role"] != "system"])
        return system_msgs + turn_msgs

    async def _llamar_llm(self, messages: list, fase: str) -> Optional[str]:
        """
        Llama al provider, cuenta la llamada y registra el error si hubo.

        **La llamada se cuenta antes de saber si salió bien**: una llamada que
        falló igual se hizo, y para medir costo eso es lo que importa.

        **Devuelve None si el provider falló**, y el error queda en
        `_errores_llm` con su fase. No se propaga: una falla del provider en
        una vuelta no mata un run de 300 s. Pero **tampoco se traga**: sin
        registro, un vivo silencioso no se puede atribuir entre el modelo que
        calla, el canal que pierde y la infraestructura que falla — que es
        justo lo que el primer vivo tiene que separar (delamor).

        Quien recibe None decide qué hacer, y la dirección segura es no actuar.
        """
        self._llamadas_llm += 1
        try:
            return await self.provider.complete(messages)
        except Exception as e:                      # noqa: BLE001 — se registra
            rate_limit, metodo = _es_rate_limit(e)
            self._errores_llm.append({
                "causa": "rate_limit" if rate_limit else "error_provider",
                "fase": fase,
                "excepcion": type(e).__name__,
                "mensaje": str(e)[:300],
                # None si el provider no declara su nombre: la ausencia no se
                # rellena con un valor inventado como "?".
                "provider": getattr(self.provider, "name", None),
                "model": getattr(self.provider, "model", None),
                # 429 se distingue del resto: no dice "algo se rompió", dice
                # "vas demasiado rápido". Es información sobre el ritmo, y el
                # ritmo es lo que el CP2v tiene que declarar.
                "rate_limit": rate_limit,
                # Cómo se supo: "status_code" es un dato, "texto" es una
                # heurística. None si no es rate limit.
                "rate_limit_segun": metodo,
            })
            self._log(f"ERROR_PROVIDER({fase}): {type(e).__name__}"
                      + (" [RATE_LIMIT]" if rate_limit else ""))
            return None

    async def _generate(self) -> Optional[str]:
        """
        Construye el prompt con historial acumulado del canal y llama al
        provider. **None si el provider falló** — ver `_llamar_llm`.
        """
        text = await self._llamar_llm(self._to_chat_messages(), "generate")
        if text is None:
            return None
        return _strip_own_prefix(text, self.device_id)

    async def _observe(
        self,
        client: Client,
        message: Optional[dict] = None,
        clock: Optional[dict] = None,
    ) -> dict:
        """
        Fase O del ciclo ODA. No LLM — solo recolección de datos.

        Recolecta estado externo (campo CKM + historial del canal) y
        estado interno (propias publicaciones recientes). Si CKMMonitor
        no está disponible o el corpus aún acumula, field trae D_ckm=None
        y el resto de las métricas en None — observación válida, no error.

        **`message=None` es el silencio** (CP2a, T5): en el ODA continuo la
        vuelta corre haya o no mensaje nuevo, y "ninguno" es un dato de la
        observación como cualquier otro. La firma quedó compatible con la de
        antes, que exigía el mensaje.

        **El join dejó de ser semilla, y se declara.** En la serie congelada el
        mensaje SYSTEM "X joined the channel" podía disparar el ciclo (Caso
        0.5). En el continuo **nada dispara**: el join entra como información,
        contado en `n_nuevos` como cualquier otro mensaje, y el lugar del seed
        lo ocupa la iniciativa del device. Lo que viene de antes es el **corte
        tomado antes del join**, no el seed (precisión de Opus sobre el CP2a).

        **El clock entra a la observación** (TASK §1: *"incluye el clock, que
        es parte del campo"*). El canal no calcula nada por el device: da el
        tick y su reloj, y evaluar los Δt es de la fase D.

        **El clock se recibe, no se pide acá.** Lo lee el loop **una sola vez
        por vuelta y antes de `get_messages`** (T2): de esa misma lectura sale
        el corte de la vuelta siguiente. Si `_observe` lo pidiera por su
        cuenta serían dos lecturas distintas del mismo tiempo en la misma
        vuelta, y el corte dejaría de corresponder al tick observado. Antes
        pedía una y el loop la sobreescribía: la llamada no hacía nada, y nada
        lo señalaba — lo encontré invirtiendo (CP2a, inversión 19).

        Sin `clock` —nadie se lo pasó— queda `{}`, que es UNKNOWN: el device
        decide sin esa dimensión en vez de inventarla.
        """
        field_result = await client.call_tool("get_monitor_state", {})
        field_state = field_result.data

        history_result = await client.call_tool("get_messages", {"since": None})
        history = history_result.data

        return {
            "field": field_state,
            "history": history,
            "clock": clock if clock is not None else {},
            "tick_anterior": self._tick_anterior,
            "trigger": message,
            "own_recent": [
                m for m in history[-20:] if m.get("device_id") == self.device_id
            ],
        }

    async def _decide(self, observation: dict) -> str:
        """
        Fase D del ciclo ODA. LLM evalúa la observación y decide.

        CKM orienta — no impone. Sin bypass: D_ckm=None llega al prompt
        igual que cualquier otro valor de campo, el device decide con lo
        que tiene.

        **Tres opciones** (CP2a, T4): `INTERACT`, `LEAVE` u `OP_SILENCE`. LEAVE
        es una acción con su primitiva, por decisión propia y no porque venció
        `duration`. El texto del gate está **declarado para que delamor lo lea
        antes de la corrida viva**: cambia lo que el device puede decidir.

        **Puede no haber mensaje nuevo.** `Incoming: (ninguno)` es el silencio,
        y el device decide igual. Los Δt no vienen calculados: están el tick
        actual, el de su vuelta anterior y los timestamps, y evaluarlos es
        parte de decidir.

        **Dos causas, una consecuencia.** Si el provider falla o si la
        respuesta no es una de las tres palabras, el resultado es `UNKNOWN`:
        no actuar. Pero se registran **por separado** —`_errores_llm` y
        `_ilegibles`— porque para atribuir un vivo silencioso no es lo mismo
        que la infraestructura falle que el modelo conteste algo ilegible.
        """
        field = observation["field"]
        history = observation["history"]
        trigger = observation["trigger"]
        clock = observation.get("clock") or {}

        history_text = (
            "\n".join(
                # Un mensaje sin timestamp dice UNKNOWN, no "?": esto entra
                # al prompt que el modelo lee, y "?" no le dice nada mientras
                # UNKNOWN le dice que el dato no estaba.
                f'[{m.get("timestamp") or "UNKNOWN"}] {m["device_id"]}: {m["text"]}'
                for m in history[-10:]
            )
            if history
            else "(empty)"
        )

        incoming = (
            f'{trigger.get("device_id", "unknown")}: "{trigger.get("text", "")}"'
            if trigger is not None
            else "(ninguno)"
        )

        gate_prompt = GATE_PROMPT_CONTINUO.format(
            d_ckm=field.get("D_ckm"),
            temp=field.get("temp_signal", "UNKNOWN"),
            c_s=field.get("c_S"),
            fi=field.get("fi"),
            delta_r=field.get("Delta_r"),
            tick=clock.get("tick"),
            reloj=clock.get("reloj", "desconocido"),
            periodo_s=clock.get("periodo_s"),
            tick_anterior=observation.get("tick_anterior"),
            history=history_text,
            n_nuevos=observation.get("n_nuevos", 0),
            incoming=incoming,
        )

        response = await self._llamar_llm([
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": gate_prompt},
        ], "decide")

        if response is None:
            # **El provider falló: no hubo decisión, y eso NO es OP_SILENCE.**
            # OP_SILENCE es una decisión que el modelo tomó; un error del
            # provider no es una decisión. Confundirlas hace que un vivo
            # silencioso no se pueda atribuir entre el modelo que calla, el
            # canal que pierde y la infraestructura que falla — que es
            # exactamente lo que el primer vivo tiene que separar.
            #
            # UNKNOWN es el estado del que observa, no un valor de la escala
            # (§19 / `c06db07`). Y no autoriza ninguna acción: `_interact` no
            # publica ni se va con UNKNOWN. Corregido a señalamiento de Opus
            # sobre el CP2v; antes caía a OP_SILENCE.
            return DECISION_UNKNOWN

        # **Una palabra fuera del vocabulario también es UNKNOWN**, no
        # OP_SILENCE. Antes caía a OP_SILENCE, con el argumento de que "no
        # actuar es la salida segura" — y la salida segura sigue siendo no
        # actuar, pero **el nombre era una decisión que nadie tomó**. Si el
        # modelo contestó algo ilegible, lo que pasó es que no se pudo
        # decidir, igual que si el provider hubiera fallado. Un vacío también.
        # Segunda mitad de la nota de Opus sobre el CP2v.
        word = response.strip().upper().split()[0] if response.strip() else ""
        if word in ("INTERACT", "LEAVE", "OP_SILENCE"):
            return word
        # **La respuesta cruda, con su causa** (pedido de Opus para el
        # primer vivo con el 8B, relevado por delamor): es lo único que después va a mostrar si el
        # problema está en el gate —el prompt pide una palabra y el modelo
        # contesta una frase— o en el modelo. Sin el texto, "ilegible" es un
        # número y no se puede mirar.
        #
        # Cruda: sin strip, sin upper. Truncada a 500 y declarado si se truncó.
        self._ilegibles.append({
            "causa": "respuesta_ilegible",
            "respuesta_cruda": response[:500],
            "truncada": len(response) > 500,
            "largo": len(response),
            "fase": "decide",
            "provider": getattr(self.provider, "name", None),
            "model": getattr(self.provider, "model", None),
        })
        return DECISION_UNKNOWN

    async def _interact(self, client: Client, decision: str, observation: dict) -> None:
        """
        Fase A del ciclo ODA. Cada decisión tiene su primitiva del canal.

        OP_SILENCE: no actúa en esta vuelta. Sin anuncio, sin log en el corpus
        del canal — sólo traza local. **El ciclo sigue**: el silencio no
        termina nada.
        INTERACT: genera contenido y publica → `send_message`.
        LEAVE: se va **por decisión propia** → `leave_channel`, y marca
        `_se_fue` para que el loop corte. Antes irse no era una decisión: era
        el final del loop cuando vencía `duration`.

        Si mañana el canal ofrece otra primitiva, D la puede elegir sin cambiar
        el ciclo (TASK §1).
        """
        field_state = observation["field"]

        if decision == DECISION_UNKNOWN:
            # No hubo decisión. UNKNOWN no autoriza ninguna acción, y se
            # distingue de OP_SILENCE en la traza.
            self._log(DECISION_UNKNOWN, field_state)
            return

        if decision == "OP_SILENCE":
            self._log("OP_SILENCE", field_state)
            return

        if decision == "LEAVE":
            await client.call_tool("leave_channel", {"device_id": self.device_id})
            self._se_fue = True
            self._log("LEAVE", field_state)
            return

        text = await self._generate()
        if text is None:
            # El provider falló al generar: la decisión fue INTERACT pero no
            # hay qué publicar. Queda registrado, y no se publica nada.
            self._log("INTERACT_SIN_TEXTO", field_state)
            return
        await client.call_tool(
            "send_message", {"device_id": self.device_id, "text": text}
        )
        self._history.append(
            {"device_id": self.device_id, "device_type": "AI", "text": text}
        )
        self._log("INTERACT", field_state)

    def _log(self, decision: str, field_state: Optional[dict] = None) -> None:
        if field_state is not None:
            d_ckm = field_state.get("D_ckm")
            temp = field_state.get("temp_signal", "UNKNOWN")
            print(f"[{self.device_id}] {decision} (D_ckm={d_ckm}, temp={temp})")
        else:
            print(f"[{self.device_id}] {decision}")

    async def run(self, duration: float = 60.0) -> None:
        """
        El ciclo ODA continuo. Corre a su propio ritmo durante `duration`
        segundos, o hasta que el device decida irse.

        **Una decisión por vuelta, haya o no mensajes nuevos.** Antes había un
        ODA por cada mensaje ajeno: cinco mensajes en un poll eran cinco
        decisiones. Ahora la vuelta junta todo lo observado desde la anterior y
        decide una vez, con todo eso adelante.

        **El tick no dispara nada: se observa.** Entra a la observación junto
        con los mensajes nuevos y el campo.

        **El silencio no es absorbente.** Si nadie publicó, la vuelta corre
        igual y el device vuelve a decidir. Antes, si todos elegían
        OP_SILENCE, no aparecía ningún mensaje y nadie se disparaba nunca más.

        **El `since` sale del reloj del canal, nunca del propio** (T2). Y se
        lee **antes** de `get_messages`: si se leyera después, un mensaje que
        llega entre las dos llamadas se perdería en silencio.

        **Y el corte se atrasa un tick: `since = t − periodo_s`.**
        `get_messages` filtra con `timestamp > since`, estricto. Un mensaje
        sellado **exactamente** en el corte y que llega después del
        `get_messages` de su vuelta no pasaría `> since` nunca más. Con la
        ventana, el corte queda **estrictamente menor** que cualquier sello de
        ese instante, así que pasa; los duplicados se descartan por
        `message_id` (`_vistos`), que ya existía para el otro borde.

        **Por qué en tiempo y no en vueltas.** La primera versión usaba el
        corte de **dos vueltas atrás**. Medido: con el reloj congelado **todos
        los cortes son el mismo número**, así que mover cuál se usa no cambia
        nada — 256 vueltas, 0 mensajes vistos. El solape por vueltas depende de
        que el reloj avance; la ventana en tiempo no.

        **Declarado:** la ventana cubre resoluciones de reloj menores que un
        tick, y `_vistos` crece durante la sesión. El `periodo_s` lo trae el
        propio clock: el device no cablea la constante del canal.

        El modo viejo quedó congelado en `process/iap_series_freeze_20261008/`.
        """
        async with Client(self.mcp_url) as client:
            # El corte inicial sale del reloj del canal, no de time.time():
            # mezclar el reloj del device con el del canal descarta mensajes en
            # silencio si el device va adelantado (hallazgo del CP0).
            clock0 = await client.call_tool("get_clock", {})
            # El corte arranca un tick antes de ahora, por la misma razón que
            # en cada vuelta: el filtro de get_messages es `>` estricto.
            ventana0 = self._ventana(clock0.data)
            # Sin grano, el corte inicial es None: `get_messages(since=None)`
            # devuelve el historial reciente, así que todo cuenta como nuevo.
            # Es ruidoso y **no pierde nada**, que es la dirección segura.
            since = (clock0.data["t"] - ventana0) if ventana0 is not None else None

            r = await client.call_tool(
                "join_channel", {"device_id": self.device_id, "device_type": "AI"}
            )
            assert r.data["ok"], f"join_channel fallo para {self.device_id}"

            start = time.monotonic()
            self._t_inicio = start
            vuelta = 0

            while time.monotonic() - start < duration and not self._se_fue:
                vuelta += 1

                # (1) el corte de la vuelta SIGUIENTE se lee ANTES de pedir los
                #     mensajes (T2). Entre esta lectura y get_messages puede
                #     llegar uno: aparece en la próxima vuelta, no se pierde.
                clock_result = await client.call_tool("get_clock", {})
                clock = clock_result.data
                # El corte de la vuelta siguiente: un tick antes de esta
                # lectura. Ventana en tiempo, no en vueltas: con el reloj
                # quieto, todos los cortes serían el mismo número y mover cuál
                # se usa no cubriría nada.
                ventana = self._ventana(clock)
                if ventana is None:
                    # UNKNOWN: el corte NO avanza. Duplicados sí —los descarta
                    # _vistos—, pérdidas no.
                    proximo_since = since
                else:
                    proximo_since = clock["t"] - ventana

                # (2) los mensajes desde el corte anterior
                fetched = await client.call_tool("get_messages", {"since": since})
                nuevos = [
                    m for m in fetched.data
                    if m.get("message_id") not in self._vistos
                    and m["device_id"] != self.device_id
                    and m.get("device_type") in ("AI", "HUMAN", "SYSTEM")
                ]
                for m in fetched.data:
                    if m.get("message_id"):
                        self._vistos.add(m["message_id"])
                self._history.extend(nuevos)

                # (3) O — una observación por vuelta, con el clock adentro. El
                #     trigger es el último mensaje nuevo, o None si hubo
                #     silencio: "ninguno" es el dato.
                observation = await self._observe(
                    client, nuevos[-1] if nuevos else None, clock=clock
                )
                observation["n_nuevos"] = len(nuevos)
                observation["vuelta"] = vuelta

                # (4) D — UNA decisión por vuelta, con todo lo de arriba
                llamadas_antes = self._llamadas_llm
                errores_antes = len(self._errores_llm)
                ilegibles_antes = len(self._ilegibles)
                decision = await self._decide(observation)

                # (5) A — la primitiva que corresponda, o ninguna
                await self._interact(client, decision, observation)

                self._decisiones.append({
                    "vuelta": vuelta,
                    "tick": clock.get("tick"),
                    "tick_anterior": self._tick_anterior,
                    "reloj": clock.get("reloj"),
                    "n_nuevos": len(nuevos),
                    "trigger": (nuevos[-1].get("message_id") if nuevos else None),
                    "decision": decision,
                    "trigger_mode": self.trigger_mode,
                    # el grano con el que se calculó el corte, o UNKNOWN si el
                    # canal no lo declaró
                    "ventana": ventana if ventana is not None else "UNKNOWN",
                    # Llamadas al LLM que ESTA vuelta hizo de verdad, y errores
                    # del provider en ella. Contadas, no inferidas de la
                    # cantidad de vueltas.
                    "llamadas_llm": self._llamadas_llm - llamadas_antes,
                    "errores_llm": len(self._errores_llm) - errores_antes,
                    "ilegibles": len(self._ilegibles) - ilegibles_antes,
                })

                self._tick_anterior = clock.get("tick", -1)
                since = proximo_since

                if self._se_fue:
                    break
                await asyncio.sleep(self.poll_interval)

            self._t_fin = time.monotonic()

            # Si se fue por decisión propia, ya llamó a leave_channel en A: no
            # se llama dos veces. Si venció `duration`, se va acá.
            if not self._se_fue:
                r = await client.call_tool(
                    "leave_channel", {"device_id": self.device_id}
                )
                assert r.data["ok"], f"leave_channel fallo para {self.device_id}"

    @staticmethod
    def _ventana(clock: dict) -> Optional[float]:
        """
        El ancho de la ventana del corte: un tick del canal. **None es UNKNOWN.**

        Sin `periodo_s` utilizable no hay ventana que calcular. Tres respuestas
        posibles, y las tres se consideraron:

        1. **`or 0.0`** — lo que hacía la primera versión. Una ventana de 0
           deja el corte en `t` exacto: **el agujero que la ventana vino a
           cerrar, reintroducido en silencio por el fallback.** Es NOMINAL por
           ausencia (`c06db07`). **Descartada.**
        2. **Levantar.** Fue mi segunda respuesta. Nombra la ausencia, pero
           **mata el instrumento**: el device deja de observar. Y el criterio
           del proyecto no es ése — `temp_signal` devuelve `"UNKNOWN"` y sigue,
           `_classify_zone` devuelve UNKNOWN y no dispara STOP. UNKNOWN **no
           autoriza una acción**; no termina el proceso. **Descartada**, a
           pregunta de delamor (*"¿UNKNOWN? ¿podría ser?"*).
        3. **UNKNOWN, y no avanzar el corte.** Es la que quedó. Devuelve None,
           queda registrado en la traza de la vuelta, y el loop **conserva el
           `since` anterior**. Quedarse atrás produce **duplicados**, que
           `_vistos` ya descarta, y **nunca pérdidas** — que es el daño que
           importa. La dirección segura es hacia atrás, no hacia adelante.

        `bool` se excluye a propósito: `True` es `int` en Python y 1.0 sería un
        grano inventado.
        """
        periodo = clock.get("periodo_s")
        if isinstance(periodo, bool) or not isinstance(periodo, (int, float)):
            return None
        if periodo <= 0:
            return None
        return float(periodo)

    def decisiones(self) -> list[dict]:
        """La traza de lo decidido, vuelta por vuelta. Copia: no se edita."""
        return list(self._decisiones)

    def ritmo_declarado(self, n_devices: int = 1) -> dict:
        """
        Cuántas llamadas al LLM implica este ritmo, para comparar contra el
        límite de la cuenta. **No conoce el límite: lo devuelve como UNKNOWN.**

        Sin criterio local, cada vuelta cuesta 1 llamada (el gate) y 2 si
        actúa. El piso y el techo salen de ahí. El límite del provider se lee
        en su consola; acá no se inventa.
        """
        if self.poll_interval <= 0:
            vueltas_min = None      # sin pausa, el ritmo lo fija la latencia
        else:
            vueltas_min = 60.0 / self.poll_interval
        return {
            "poll_interval_s": self.poll_interval,
            "n_devices": n_devices,
            "vueltas_por_minuto_por_device": vueltas_min,
            "llamadas_por_minuto_piso": (
                round(vueltas_min * n_devices, 2) if vueltas_min else None
            ),
            "llamadas_por_minuto_techo": (
                round(vueltas_min * n_devices * 2, 2) if vueltas_min else None
            ),
            "limite_de_la_cuenta": "UNKNOWN — se lee en la consola del provider",
            "nota": (
                "sin poll_interval el ritmo lo fija la latencia del provider y "
                "no se puede declarar de antemano"
            ),
        }

    def ritmo_observado(self) -> dict:
        """
        El ritmo que **de hecho** hubo: vueltas y llamadas reales por minuto.

        **Va al lado del declarado, no lo reemplaza** (F5). Lo medido en los
        dos vivos: con `poll_interval = 5.0` el declarado da 12 vueltas por
        minuto, y el observado fue 12 y 12 en el vivo 01 —los 404 volvían al
        instante— y **11 y 12 en el 02**. El declarado es el **piso teórico**;
        el observado es el piso **menos la latencia** del provider.

        Sin corrida devuelve todo en None: **UNKNOWN, no 0**.
        """
        if self._t_inicio is None or self._t_fin is None:
            return {
                "segundos": None,
                "vueltas_por_minuto": None,
                "llamadas_por_minuto": None,
                "segundos_por_vuelta": None,
                "nota": "sin corrida no hay ritmo observado — UNKNOWN, no 0",
            }
        seg = self._t_fin - self._t_inicio
        n = len(self._decisiones)
        if seg <= 0:
            return {
                "segundos": round(seg, 3),
                "vueltas_por_minuto": None,
                "llamadas_por_minuto": None,
                "segundos_por_vuelta": None,
                "nota": "duración no positiva: no hay ritmo que calcular",
            }
        return {
            "segundos": round(seg, 3),
            "vueltas": n,
            "vueltas_por_minuto": round(n * 60.0 / seg, 3),
            "llamadas_por_minuto": round(self._llamadas_llm * 60.0 / seg, 3),
            "segundos_por_vuelta": round(seg / n, 3) if n else None,
        }

    def costo(self) -> dict:
        """
        Lo que el run costó, en llamadas al LLM. **Contadas, no estimadas.**

        No dice dinero ni tokens: eso depende del provider y del tamaño de los
        prompts, y el device no lo mide. Dice llamadas, vueltas y errores, que
        es lo que permite atribuir un silencio.
        """
        ds = self._decisiones
        return {
            "device_id": self.device_id,
            "provider": getattr(self.provider, "name", None),
            "model": getattr(self.provider, "model", None),
            "vueltas": len(ds),
            "llamadas_llm": self._llamadas_llm,
            "llamadas_por_vuelta": (
                round(self._llamadas_llm / len(ds), 3) if ds else None
            ),
            "errores_llm": len(self._errores_llm),
            "errores": list(self._errores_llm),
            "ilegibles": len(self._ilegibles),
            "ejemplos_ilegibles": list(self._ilegibles[:5]),
            "errores_rate_limit": sum(
                1 for e in self._errores_llm if e.get("rate_limit")
            ),
            "ritmo_declarado": self.ritmo_declarado(),
            "ritmo_observado": self.ritmo_observado(),
            "decisiones_por_tipo": {
                d: sum(1 for x in ds if x["decision"] == d)
                for d in sorted({x["decision"] for x in ds})
            },
            "vueltas_con_ventana_unknown": sum(
                1 for x in ds if x.get("ventana") == "UNKNOWN"
            ),
        }
