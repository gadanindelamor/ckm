"""
groq_research_agent.py — AutonomousResearchAgent

Agente conversacional autonomo, orientado a objetivo fijo, integrable
como wrapped_agent dentro de AgentDeviceSkin
(iap_chatroom/agent_device_skin.py, sin modificar). Ejecuta UN paso del
ciclo agentico (un plan generado una vez, luego un paso de
buscar+analizar por invocacion) por cada trigger del ciclo ODA del
canal -- no corre un loop bloqueante propio. El loop lo sigue siendo
AutonomousDevice.run() / el poll_interval del canal; este modulo solo
decide que hacer en cada paso.

Decisiones ya debatidas y acordadas (ver conversacion):
1. La busqueda web queda como dependencia OPCIONAL, documentada acá y
   en el docstring de ddg_search() -- NO se agrego a pyproject.toml.
   Instalar manualmente si se quiere busqueda real:
       pip install ddgs
   (no duckduckgo-search -- deprecado, renombrado por el mismo
   mantenedor; verificado en esta sesion que duckduckgo-search==8.1.1
   devuelve [] silenciosamente en este entorno, ddgs==9.14.4 trae
   resultados reales con la misma query -- ver comentario junto al
   import). Sin el paquete instalado, ddg_search() no crashea --
   devuelve una lista con un registro de error, y el ciclo sigue.
2. La finalizacion de cada tarea la decide una respuesta JSON
   estructurada de Groq ({"completa": bool, "resumen": str, "razon":
   str}), no pattern-matching sobre texto libre.
3. Lo que se publica al canal es el resumen en lenguaje natural
   (mas fuentes citadas cuando hay), no el JSON crudo de busqueda --
   mantiene el corpus CKM legible, comparable al resto de la serie
   0.4-0.11. El JSON completo (plan + cada iteracion + resultados
   crudos) se exporta aparte para auditoria.
4. Objetivo fijo al construir el agente (mismo patron que
   RESEARCHER_GOAL_PROMPT en Caso 0.10 / ARCHITECT_GOAL_PROMPT en
   0.11) -- no se deriva del contenido del canal.
5. Limite de iteraciones vía config (max_iterations) + manejo de
   errores explicito en cada punto de fallo posible (red DDG, parseo
   JSON de Groq, y como red de seguridad final, la propia llamada a
   wrapped_agent) -- el criterio duro es que el ciclo ODA del canal
   nunca debe crashear por esto, sin importar que falle.

NO modifica ningun archivo existente del proyecto CKM/iap_chatroom.
Reusa GroqProvider (iap_chatroom/providers/groq_provider.py) tal cual
esta, con el fix de max_tokens/warning ya aplicado en sesion previa.

Nota: "temperature" no esta en la config -- GroqProvider.complete() no
acepta ese parametro (su firma es complete(messages) -> str). Queda
pendiente para una proxima iteracion, a incorporar junto con el cambio
correspondiente en groq_provider.py (fuera de alcance de este modulo).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Awaitable, Callable, Optional

from iap_chatroom.autonomous_device import _coalesce, _strip_own_prefix
from iap_chatroom.providers.base import Provider

try:
    # duckduckgo-search (paquete "duckduckgo_search") esta deprecado --
    # renombrado a "ddgs" por el mismo mantenedor. Verificado en esta
    # sesion: duckduckgo-search==8.1.1 emite RuntimeWarning y devuelve
    # [] silenciosamente en este entorno (sin lanzar, sin resultados,
    # incluso con queries genericas tipo "python programming
    # language"); ddgs==9.14.4 con la misma query trae resultados
    # reales. Se usa ddgs por eso, no por preferencia arbitraria.
    from ddgs import DDGS
    _DDGS_AVAILABLE = True
except ImportError:
    _DDGS_AVAILABLE = False

# Mismo tipo que WrappedAgent en agent_device_skin.py (no importado
# directamente para no crear una dependencia circular de conveniencia;
# la forma es identica: observation dict -> texto a publicar o None).
WrappedAgent = Callable[[dict], Awaitable[Optional[str]]]

_CONFIG_PATH = Path(__file__).resolve().parent / "groq_agent_config.json"
_RESULTS_DIR = (
    Path(__file__).resolve().parent.parent / "process" / "agent_runs"
)

DEFAULT_CONFIG = {
    "groq_model": "llama-3.3-70b-versatile",
    "max_iterations": 8,
    "search_results": 3,
}


def load_config(path: Optional[Path] = None) -> dict:
    """Carga config JSON; si no existe, usa el default embebido."""
    p = path or _CONFIG_PATH
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return dict(DEFAULT_CONFIG)


def ddg_search(query: str, max_results: int) -> list[dict]:
    """
    Busqueda real en DuckDuckGo via ddgs (dependencia OPCIONAL, no
    instalada por defecto -- ver docstring del modulo. No es
    duckduckgo-search -- ese paquete esta deprecado).

    Nunca lanza. Sin el paquete instalado, o ante cualquier error de
    red/parsing, devuelve una lista con un solo dict {"error": ...} en
    vez de propagar la excepcion -- el ciclo ODA no debe crashear por
    una busqueda fallida.
    """
    if not _DDGS_AVAILABLE:
        return [{
            "error": "ddgs no instalado (dependencia opcional) -- "
                     "pip install ddgs"
        }]
    try:
        with DDGS() as ddgs:
            return [
                {
                    "titulo": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", ""),
                }
                for r in ddgs.text(query, max_results=max_results)
            ]
    except Exception as e:
        return [{"error": str(e)}]


async def _safe_complete(
    provider: Provider,
    messages: list[dict],
    fallback: str = "",
) -> str:
    """
    Wrapper de Provider.complete() que nunca lanza -- captura cualquier
    error del lado del proveedor (red, rate limit, auth, etc.) y
    devuelve `fallback` en vez de propagar. GroqProvider.complete() en
    si no atrapa estos errores (confirmado leyendo el archivo), asi que
    esta es la capa de seguridad para el criterio "no debe crashear".
    """
    try:
        return await provider.complete(messages)  # type: ignore[arg-type]
    except Exception as e:
        print(f"[groq_research_agent WARNING] provider.complete() fallo: {e}")
        return fallback


def _parse_json_loose(raw: str) -> Optional[object]:
    """
    Groq a veces envuelve JSON en ```json ... ``` pese a que el prompt
    pide explicitamente que no lo haga -- despoja los fences antes de
    json.loads(). Devuelve None si no parsea (nunca lanza).
    """
    text = raw.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


PLAN_PROMPT_TEMPLATE = """\
Genera un plan de tareas en JSON para cumplir este objetivo:
"{objetivo}"

Devolve SOLO un array JSON (sin texto alrededor, sin markdown fences),
cada elemento con exactamente estas claves: "id" (int), "descripcion"
(str -- una consulta de busqueda concreta y buscable, no una frase
abstracta), "prioridad" ("alta"/"media"/"baja"), "estado" (siempre
"pendiente" al generar el plan). Entre 3 y 6 tareas."""


def _normalize_task(t: object, fallback_id: int) -> Optional[dict]:
    """Valida/normaliza un item de plan devuelto por Groq. None si el
    item no tiene la forma minima usable (falta descripcion)."""
    if not isinstance(t, dict) or not t.get("descripcion"):
        return None
    return {
        "id": t.get("id", fallback_id),
        "descripcion": str(t["descripcion"]),
        "prioridad": t.get("prioridad", "media"),
        "estado": "pendiente",
    }


async def plan_tasks(objetivo: str, provider: Provider) -> list[dict]:
    """Pide a Groq un plan de tareas en JSON. Ante cualquier fallo
    (provider caido, JSON no parseable, plan vacio), cae a un plan de
    una sola tarea igual al objetivo -- nunca deja el plan vacio ni
    lanza."""
    messages = [
        {
            "role": "system",
            "content": "Sos un planificador de tareas. Respondes solo JSON valido.",
        },
        {
            "role": "user",
            "content": PLAN_PROMPT_TEMPLATE.format(objetivo=objetivo),
        },
    ]
    raw = await _safe_complete(provider, messages)
    parsed = _parse_json_loose(raw)
    if isinstance(parsed, list):
        tareas = [
            t for t in (
                _normalize_task(x, i + 1) for i, x in enumerate(parsed)
            ) if t
        ]
        if tareas:
            return tareas
    return [
        {"id": 1, "descripcion": objetivo, "prioridad": "alta", "estado": "pendiente"}
    ]


ANALYSIS_PROMPT_TEMPLATE = """\
Tarea: "{tarea}"

Resultados de busqueda:
{resultados}

Respondé SOLO JSON (sin texto alrededor, sin markdown fences) con estas
claves: "completa" (bool -- true si los resultados alcanzan para dar
por cumplida la tarea), "resumen" (str, 2-4 oraciones en lenguaje
natural; cita la fuente por titulo cuando el resultado lo permita,
ej: "segun [titulo]..."; si los resultados vienen vacios o con error,
decilo en el resumen en vez de inventar contenido), "razon" (str,
por que esta o no completa)."""


async def analyze_results(
    tarea: str,
    resultados: list[dict],
    provider: Provider,
) -> dict:
    """Pide a Groq que analice los resultados de busqueda de una tarea
    y devuelva veredicto+resumen en JSON. Ante fallo del provider o
    JSON no parseable, cae a un dict con completa=False y el texto
    crudo (recortado) como resumen -- nunca lanza."""
    messages = [
        {
            "role": "system",
            "content": "Analizas resultados de busqueda y respondes solo JSON valido.",
        },
        {
            "role": "user",
            "content": ANALYSIS_PROMPT_TEMPLATE.format(
                tarea=tarea,
                resultados=json.dumps(resultados, ensure_ascii=False),
            ),
        },
    ]
    raw = await _safe_complete(provider, messages)
    parsed = _parse_json_loose(raw)
    if isinstance(parsed, dict) and "resumen" in parsed:
        return {
            "completa": bool(parsed.get("completa", False)),
            "resumen": str(parsed.get("resumen", "")),
            "razon": str(parsed.get("razon", "")),
        }
    return {
        "completa": False,
        "resumen": raw.strip()[:500] if raw else "(sin respuesta del modelo)",
        "razon": "respuesta no parseable como JSON",
    }


class AutonomousResearchAgent:
    """
    Estado de un agente de investigacion con objetivo fijo. Un
    step() == un paso: si no hay plan todavia, lo genera (una vez);
    si hay una tarea pendiente, la ejecuta (buscar + analizar +
    marcar estado); devuelve el texto a publicar o None.

    No corre un loop propio -- quien itera es quien llama a step()
    repetidamente (en este proyecto, el ciclo ODA del canal via
    build_autonomous_groq_agent() mas abajo).
    """

    def __init__(
        self,
        device_id: str,
        objetivo: str,
        provider: Provider,
        config: Optional[dict] = None,
    ):
        self.device_id = device_id
        self.objetivo = objetivo
        self.provider = provider
        self.config = config or load_config()
        self.plan: Optional[list[dict]] = None
        self.iteracion = 0
        self.resultados_globales: dict = {
            "device_id": device_id,
            "objetivo": objetivo,
            "config": self.config,
            "plan": None,
            "iteraciones": [],
        }
        # Path fijado en __init__, no recalculado en cada export -- asi
        # export() sobrescribe el mismo archivo en vez de crear uno
        # nuevo por turno.
        self._export_path: Optional[Path] = None

    def _next_pending(self) -> Optional[dict]:
        if not self.plan:
            return None
        return next(
            (t for t in self.plan if t.get("estado") == "pendiente"), None
        )

    async def step(self) -> Optional[str]:
        if self.plan is None:
            self.plan = await plan_tasks(self.objetivo, self.provider)
            self.resultados_globales["plan"] = self.plan

        max_iter = self.config.get(
            "max_iterations", DEFAULT_CONFIG["max_iterations"]
        )
        if self.iteracion >= max_iter:
            return None  # OP_SILENCE -- limite de iteraciones alcanzado

        tarea = self._next_pending()
        if tarea is None:
            return None  # OP_SILENCE -- plan completo, nada pendiente

        self.iteracion += 1
        n_results = self.config.get(
            "search_results", DEFAULT_CONFIG["search_results"]
        )
        resultados = ddg_search(tarea["descripcion"], n_results)
        analisis = await analyze_results(
            tarea["descripcion"], resultados, self.provider
        )

        if analisis.get("completa"):
            tarea["estado"] = "completada"

        self.resultados_globales["iteraciones"].append({
            "iteracion": self.iteracion,
            "tarea_id": tarea.get("id"),
            "tarea": tarea["descripcion"],
            "resultados_busqueda": resultados,
            "analisis": analisis,
        })

        fuentes = ", ".join(
            r["titulo"] for r in resultados if r.get("titulo")
        )
        texto = analisis.get("resumen", "").strip()
        if fuentes:
            texto = f"{texto}\n\n(fuentes: {fuentes})"
        return texto or None

    def export(self) -> None:
        """
        Exporta (sobrescribe) resultados_globales a JSON. Se llama
        despues de CADA step(), sin condicionar al valor que devolvio
        -- ver build_autonomous_groq_agent() mas abajo. No hay hook de
        "el canal esta por cortar el loop" disponible desde afuera
        (AutonomousDevice.run() no lo expone, y no se modifica ese
        archivo) -- exportar en cada turno es la unica forma de
        garantizar que quede un registro del ultimo estado disponible
        sin importar por que wrapped_agent deja de ser invocado
        (timeout del canal, plan completo, max_iterations, o cualquier
        otra causa). El path se fija una sola vez (self._export_path,
        en __init__) para que esto sobrescriba el mismo archivo en vez
        de acumular uno por turno.
        """
        try:
            _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
            if self._export_path is None:
                fname = f"resultados_agente_{self.device_id}_{int(time.time())}.json"
                self._export_path = _RESULTS_DIR / fname
            with open(self._export_path, "w", encoding="utf-8") as f:
                json.dump(
                    self.resultados_globales, f, indent=2, ensure_ascii=False
                )
        except OSError as e:
            print(
                f"[groq_research_agent WARNING] no se pudo exportar resultados: {e}"
            )


def build_autonomous_groq_agent(
    device_id: str,
    objetivo: str,
    provider: Provider,
    config: Optional[dict] = None,
) -> WrappedAgent:
    """
    Factory: devuelve un wrapped_agent compatible con
    AgentDeviceSkin(wrapped_agent=...) (agent_device_skin.py, sin
    modificar -- el tipo WrappedAgent de este modulo tiene la misma
    forma exacta). Objetivo FIJO al construir (decision ya acordada),
    no derivado del canal.

    Cada invocacion (un trigger del ciclo ODA) ejecuta un paso del
    agente: genera el plan la primera vez, despues un paso de
    buscar+analizar por turno. Publica el resumen en lenguaje natural
    de esa tarea (con fuentes si las hay). Devuelve None (OP_SILENCE)
    una vez que el plan se completa o se alcanza max_iterations.

    Nota de diseño: a diferencia de build_goal_directed_agent()
    (agent_device_skin.py), este wrapped_agent NO lee
    observation["history"]/["trigger"] para decidir que publicar -- el
    agente persigue su propio plan de investigacion, no responde al
    contenido conversacional del canal turno a turno. Recibe el mismo
    `observation` dict (por compatibilidad de firma con WrappedAgent),
    pero esta primera version no lo usa.

    Nunca lanza: cualquier error no anticipado dentro de step() se
    captura acá como ultima red de seguridad y se traduce en
    OP_SILENCE para ese turno, en vez de propagar hacia
    AutonomousDevice.run() y arriesgar el ciclo ODA del canal.

    Exporta (sobrescribe) el estado despues de CADA invocacion, sin
    condicionar al valor devuelto por step() ni a si hubo excepcion
    -- ver AutonomousResearchAgent.export(). AutonomousDevice.run()
    puede dejar de llamar a wrapped_agent en cualquier momento (timeout
    de duration, el caso real observado en Caso 0.12 -- ver
    registers/REG_iap_caso_12_v1.md) sin avisar; exportar en cada turno
    es lo unico que garantiza que el ultimo estado quede en disco.
    """
    agent_state = AutonomousResearchAgent(device_id, objetivo, provider, config)

    async def wrapped_agent(observation: dict) -> Optional[str]:
        try:
            return await agent_state.step()
        except Exception as e:
            print(
                f"[groq_research_agent WARNING] step() fallo inesperadamente: {e}"
            )
            return None
        finally:
            agent_state.export()

    return wrapped_agent


def build_search_grounded_agent(
    device_id: str,
    provider: Provider,
    goal_system_prompt: str,
    silence_sentinel: str = "OP_SILENCE",
    search_results: int = 3,
) -> WrappedAgent:
    """
    Factory para Caso 0.13 (registers/TASK_caso_13.md) -- ninguno de
    los dos wrapped_agent existentes cubre este mecanismo: es
    conversacional (lee observation["history"]/["trigger"] y espera
    contenido real del canal, como build_goal_directed_agent en
    agent_device_skin.py -- no toca ese archivo, reimplementa el mismo
    patron de coalescing acá) pero ademas busca en la web antes de
    generar (como AutonomousResearchAgent, reusando ddg_search de este
    modulo), en vez de perseguir un plan propio fijo que ignora el
    canal.

    Uso previsto (Caso 0.13, MarkOpolus): un device que depende
    estructuralmente de lo que otro device publica (no de un plan
    propio) pero necesita grounding real de busqueda para su
    contenido -- un handoff genuino, no una investigacion autonoma.

    La query de busqueda se deriva del `trigger` (el mensaje nuevo que
    disparo este turno) -- lo mas reciente publicado en el canal, no
    el `goal_system_prompt` fijo -- para que la busqueda este grounded
    en lo que efectivamente se dijo, no en el objetivo abstracto.
    Si no hay texto de trigger util, cae al `goal_system_prompt` como
    query (nunca busca con string vacio).

    Nunca lanza: `ddg_search` ya es crash-safe (ver docstring del
    modulo); la llamada al provider pasa por un try/except propio acá
    -- mismo criterio "no debe crashear" que el resto de este archivo.
    """

    async def wrapped_agent(observation: dict) -> Optional[str]:
        history = observation["history"]
        trigger = observation["trigger"]

        trigger_text = trigger.get("text", "")
        query = (trigger_text or goal_system_prompt)[:200]
        resultados = ddg_search(query, search_results)
        fuentes_text = "\n".join(
            f"- {r['titulo']}: {r.get('snippet', '')}"
            for r in resultados
            if r.get("titulo")
        )
        if not fuentes_text:
            fuentes_text = "(sin resultados de busqueda disponibles para esta consulta)"

        grounding_block = (
            f"\n\nWeb search results for grounding "
            f"(query: {query!r}), use if relevant:\n{fuentes_text}"
        )

        messages = [
            {"role": "system", "content": goal_system_prompt + grounding_block}
        ]
        for m in history[-10:]:
            role = "assistant" if m["device_id"] == device_id else "user"
            messages.append(
                {"role": role, "content": f"[{m['device_id']}]: {m['text']}"}
            )
        trigger_sender = trigger.get("device_id", "unknown")
        messages.append({
            "role": "user",
            "content": f"[{trigger_sender}]: {trigger_text}",
        })
        system_msgs = [c for c in messages if c["role"] == "system"]
        turn_msgs = _coalesce([c for c in messages if c["role"] != "system"])
        messages = system_msgs + turn_msgs

        try:
            raw = await provider.complete(messages)
        except Exception as e:
            print(
                f"[groq_research_agent WARNING] build_search_grounded_agent: "
                f"provider.complete() fallo: {e}"
            )
            return None

        text = _strip_own_prefix(raw, device_id).strip()
        if not text or silence_sentinel in text.upper():
            # Fix quirurgico (Jul 2026, ver conversacion / REG_iap_caso_13_v1.md):
            # contencion en vez de igualdad exacta. El sentinel exacto
            # ("== silence_sentinel") dejaba pasar como contenido real
            # cualquier texto que antepusiera prosa antes de "OP_SILENCE"
            # (12/23 textos no-join de Caso 0.13, verificado). No es la
            # solucion definitiva -- hay una propuesta mas completa en
            # curso, para mas adelante. Riesgo conocido y no resuelto:
            # si algun dia un device menciona "OP_SILENCE" como parte de
            # contenido real (discutiendo el propio mecanismo), tambien
            # se suprimiria -- no ocurrio en los datos vistos hasta ahora.
            return None
        return text

    return wrapped_agent
