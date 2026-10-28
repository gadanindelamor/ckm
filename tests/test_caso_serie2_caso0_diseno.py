"""
test_caso_serie2_caso0_diseno.py — **el diseño del caso, verificado sin red**

Punto 4 de `TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md`. El caso
vive en `iap_chatroom/tests/test_caso_serie2_caso0.py`, que es un script de la
serie IAP y **no lo colecta pytest** (`testpaths = ["tests"]`): correrlo es
disparar el vivo, y eso lo hace delamor.

Este archivo sí lo colecta la suite, y verifica lo del diseño que **se puede
medir sin tocar el canal ni un provider**: la consigna parcial, que nadie vea
la lista de las cuatro perspectivas, los ids neutros, la ausencia de seed y de
coordinador, y la aritmética del piso y de la duración.

Lo que **no** puede verificar: que los cuatro modelos respondan. Eso es una
llamada a la red y vive en `--preflight` del caso, que corre al disparar.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

CASO_PATH = RAIZ / "iap_chatroom" / "tests" / "test_caso_serie2_caso0.py"


@pytest.fixture(scope="module")
def caso():
    """
    El módulo del caso, importado por ruta.

    Por ruta y no con `import` normal porque `iap_chatroom/tests/` no es un
    paquete y su nombre empieza con `test_`: importarlo por nombre lo pondría
    a competir con los tests de la suite.

    **Importarlo no dispara nada.** Los providers se construyen dentro de
    `construir_devices()` y `preflight()`, no al importar; a nivel de módulo
    sólo hay constantes y un `load_dotenv`.
    """
    spec = importlib.util.spec_from_file_location("caso_serie2_caso0", CASO_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def canal_limpio(monkeypatch):
    """Un `ChatChannel` nuevo: es singleton, así que se resetea la instancia."""
    from iap_chatroom.channel import ChatChannel

    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


# ── la consigna parcial ──────────────────────────────────────────────────────

def test_hay_cuatro_devices_uno_por_perspectiva(caso):
    assert len(caso.DEVICES) == 4
    assert len(caso.PERSPECTIVAS) == 4
    letras = [l for l, _, _, _ in caso.DEVICES]
    assert sorted(letras) == ["A", "B", "C", "D"]
    assert set(letras) == set(caso.PERSPECTIVAS)


def test_las_cuatro_perspectivas_son_las_del_orden(caso):
    """Textuales del orden de delamor. Si cambian, cambia el caso."""
    assert caso.PERSPECTIVAS == {
        "A": "where the water comes from",
        "B": "how it is distributed",
        "C": "who pays and how much",
        "D": "what could go wrong in the next 20 years",
    }


def test_la_consigna_de_un_device_no_nombra_las_otras_perspectivas(caso):
    """
    *"Cada device recibe sólo su perspectiva: la lista de las cuatro no la ve
    nadie."* **Sin coordinador:** nadie tiene más información que los otros.

    Se verifica en los cuatro prompts armados, contra las tres perspectivas
    ajenas de cada uno.
    """
    for letra, did, _, _ in caso.DEVICES:
        prompt = caso.system_prompt(did, letra)
        assert caso.PERSPECTIVAS[letra] in prompt, (
            f"{did} no recibió su propia perspectiva"
        )
        for otra_letra, otra in caso.PERSPECTIVAS.items():
            if otra_letra == letra:
                continue
            assert otra not in prompt, (
                f"el prompt de {did} nombra la perspectiva de {otra_letra}"
            )


def test_ningun_prompt_tiene_mas_informacion_que_los_otros(caso):
    """
    Sin coordinador: los cuatro prompts son **el mismo texto** salvo el
    `device_id` y la perspectiva. Si uno tuviera un párrafo más, sería el
    coordinador que el orden prohíbe.
    """
    plantillas = set()
    for letra, did, _, _ in caso.DEVICES:
        p = caso.system_prompt(did, letra)
        p = p.replace(did, "{device_id}")
        p = p.replace(caso.PERSPECTIVAS[letra], "{perspectiva}")
        plantillas.add(p)
    assert len(plantillas) == 1, (
        f"los prompts no son la misma plantilla: {len(plantillas)} distintas"
    )


def test_el_system_prompt_es_el_bloque_de_la_serie_mas_la_consigna(caso):
    """
    *"system prompt = el bloque común de la serie (como en
    `SYSTEM_PROMPT_04A`), más la consigna parcial"*.

    El bloque se compara contra el **congelado** de la serie 1
    (`process/iap_series_freeze_20261008/tests/test_caso_04a.py`), que es la
    fuente: copiarlo a mano y que después diverja es el riesgo.
    """
    congelado = (RAIZ / "process" / "iap_series_freeze_20261008" / "tests"
                 / "test_caso_04a.py").read_text()
    m = re.search(r'SYSTEM_PROMPT_04A = """(.*?)"""', congelado, re.S)
    assert m, "no se encontró SYSTEM_PROMPT_04A en el congelado de la serie 1"
    assert caso.BLOQUE_COMUN == m.group(1), (
        "el bloque común divergió del SYSTEM_PROMPT_04A de la serie 1"
    )
    prompt = caso.system_prompt("device_a", "A")
    assert prompt.startswith(caso.BLOQUE_COMUN.format(device_id="device_a"))
    assert prompt.endswith(
        caso.CONSIGNA.format(perspectiva=caso.PERSPECTIVAS["A"])
    )


def test_sin_explicacion_de_los_campos_de_CKM_en_el_system_prompt(caso):
    """
    *"Sin explicación de los campos de CKM en el system prompt, como en
    0.4a"* (delamor, para este caso). El device **sí** recibe las métricas en
    el gate; lo que no hay es marco previo para interpretarlas.
    """
    for letra, did, _, _ in caso.DEVICES:
        prompt = caso.system_prompt(did, letra)
        for campo in ("D_ckm", "temp_signal", "c_S", "Delta_r", "CKM",
                      "fabrication", "beta", "corpus", "W "):
            assert campo not in prompt, f"{campo} explicado en el prompt de {did}"


def test_el_apodo_no_entra_a_ningun_prompt(caso):
    """
    *"El apodo nunca entra a ningún prompt."* Ni el apodo ni el nombre técnico.
    """
    for letra, did, _, _ in caso.DEVICES:
        prompt = caso.system_prompt(did, letra)
        for palabra in ("Cimientos", "cimientos", "serie2_caso0", "S2-C0",
                        "S2", "Serie 2"):
            assert palabra not in prompt, f"{palabra!r} en el prompt de {did}"


def test_todo_lo_que_llega_al_modelo_esta_en_ingles(caso):
    """
    El punto 1 aplicado a los prompts **de este caso**: el system prompt es lo
    único que el caso escribe, y el resto lo audita
    `tests/test_prompt_solo_ingles.py`. Mismo detector, para que el criterio
    sea uno.
    """
    from test_prompt_solo_ingles import castellano

    for letra, did, _, _ in caso.DEVICES:
        hallados = castellano(caso.system_prompt(did, letra))
        assert hallados == [], f"castellano en el prompt de {did}: {hallados}"
    assert castellano(caso.BLOQUE_COMUN) == []
    assert castellano(caso.CONSIGNA) == []


# ── los ids ──────────────────────────────────────────────────────────────────

def test_los_device_ids_son_neutros_y_en_ingles(caso):
    """
    *"Device ids neutros, en inglés."*

    Neutros **y además** sin la perspectiva adentro: el id viaja en el
    historial que todos leen (`[device_id]: texto`), así que un
    `device_cost` le diría a los otros tres cuál es la perspectiva de C — que
    es justo lo que la consigna parcial no quiere.
    """
    ids = [d for _, d, _, _ in caso.DEVICES]
    assert ids == ["device_a", "device_b", "device_c", "device_d"]
    assert len(set(ids)) == 4
    for letra, did, _, _ in caso.DEVICES:
        for palabra in caso.PERSPECTIVAS[letra].split():
            if len(palabra) > 3:
                assert palabra not in did, f"{did} revela su perspectiva"


# ── sin seed, sin agentes ────────────────────────────────────────────────────

def test_no_hay_seed(caso):
    """
    *"Sin seed: no hay `seed_human`; el corpus arranca sólo con lo que
    publiquen los devices."*

    Se mira el fuente y no una bandera: la ausencia de un mecanismo no se
    puede verificar con un atributo que diga que no está.
    """
    fuente = CASO_PATH.read_text()
    cuerpo = fuente.split('"""', 2)[2]          # sin el docstring del módulo
    for marca in ("seed_human", "SEED_TEXT", "SEED_DELAY", "seed_message"):
        assert marca not in cuerpo, f"{marca} en el caso: hay seed"
    assert "HUMAN" not in cuerpo, "un device HUMAN sería el seed con otro nombre"


def test_sin_agentes_devices_genuinos(caso):
    """
    *"Sin agentes: devices genuinos (`AutonomousDevice`), sin `AgentDeviceSkin`."*

    Se mira **el cuerpo** y no el archivo entero: el docstring del caso nombra
    `AgentDeviceSkin` justo para declarar que no está, y buscarlo en todo el
    fuente hace fallar al test por la declaración de su propia ausencia. Me
    pasó al escribirlo.
    """
    cuerpo = CASO_PATH.read_text().split('"""', 2)[2]
    assert "AgentDeviceSkin" not in cuerpo
    assert "build_goal_directed_agent" not in cuerpo
    assert "groq_research_agent" not in cuerpo
    assert caso.AutonomousDevice.__name__ == "AutonomousDevice"


def test_el_ODA_continuo_permite_hablar_primero():
    """
    El riesgo del arranque sin seed descansa en esto, y está medido en otro
    lado: `tests/test_oda_continuo.py::test_iniciativa_el_diseno_permite_hablar_primero`.
    Acá se verifica que ese test exista — si se borrara, el caso se quedaría
    sin la premisa que lo sostiene.
    """
    fuente = (RAIZ / "tests" / "test_oda_continuo.py").read_text()
    assert "def test_iniciativa_el_diseno_permite_hablar_primero" in fuente


# ── la aritmética ────────────────────────────────────────────────────────────

def test_el_piso_cae_dentro_de_las_vueltas_del_caso(caso):
    """
    La condición del orden: `piso_vueltas + 2 ≤ vueltas por device`.

    Las vueltas se calculan con el **peor** segundo por vuelta considerado en
    el diseño (7 s: los 5.2 medidos en el vivo 03 más margen por las llamadas
    de verdad), no con el mejor. Un piso que entra sólo en el caso optimista
    es, en la práctica, un piso que puede no entrar.
    """
    S_POR_VUELTA_PESIMISTA = 7.0
    vueltas = caso.DURATION / S_POR_VUELTA_PESIMISTA
    assert caso.PISO_VUELTAS + 2 <= vueltas, (
        f"piso {caso.PISO_VUELTAS} + 2 > {vueltas:.0f} vueltas por device"
    )
    # y el piso dispara en piso+2, que es lo medido en el CP2b y lo que el
    # panel del device declara
    from iap_chatroom.local_criterion import LocalCriterionThresholds
    umb = LocalCriterionThresholds(piso_vueltas=caso.PISO_VUELTAS)
    assert umb.piso_vueltas + 2 == 8


def test_la_duracion_alcanza_para_dos_rebuilds(caso):
    """
    ≥ 2 rebuilds pide **50 textos de device**: el primer W espera
    `MIN_TEXTS_FIRST_W = 30` y el criterio de volumen dispara cada
    `REBUILD_EVERY = 10`. El objetivo declarado son 70.

    La duración se verifica contra la tasa **pesimista declarada**: desde el
    intento 2 es **p = 0.075**, la mitad de la del intento 1 (0.15), porque
    `DURATION` subió a 1200 s con ese objetivo. Si alcanza ahí, alcanza.

    **Esto es lo que cubre el cambio de `DURATION`:** con los 600 s del
    intento 1 este test falla contra p = 0.075 (hacen falta 1167 s).
    """
    from iap_chatroom.ckm_monitor import MIN_TEXTS_FIRST_W, REBUILD_EVERY

    assert MIN_TEXTS_FIRST_W == 30 and REBUILD_EVERY == 10
    textos_para_dos_rebuilds = MIN_TEXTS_FIRST_W + 2 * REBUILD_EVERY
    assert textos_para_dos_rebuilds == 50
    assert caso.TEXTOS_OBJETIVO >= textos_para_dos_rebuilds

    P_PESIMISTA = 0.075
    n_devices = len(caso.DEVICES)
    mensajes_por_min = n_devices * (60.0 / caso.POLL_INTERVAL) * P_PESIMISTA
    minutos = caso.TEXTOS_OBJETIVO / mensajes_por_min
    assert minutos * 60 <= caso.DURATION, (
        f"con p={P_PESIMISTA} hacen falta {minutos * 60:.0f}s y hay "
        f"{caso.DURATION:.0f}s"
    )


def test_el_poll_interval_es_el_medido_en_el_vivo_03(caso):
    """
    El insumo del ritmo es **lo medido**, no un número nuevo: el vivo 03 corrió
    con `poll_interval = 5.0` y dio 5.2 s por vuelta y 0 rate limits.
    """
    assert caso.POLL_INTERVAL == 5.0
    log = RAIZ / "experiments" / "vivo_03_criterio_local_log.json"
    if not log.exists():
        pytest.skip("el log del vivo 03 no está en este checkout")
    import json
    d = json.loads(log.read_text())
    assert d["declarado"]["poll_interval_s"] == caso.POLL_INTERVAL
    for p in d["por_device"]:
        assert p["costo"]["errores_rate_limit"] == 0


def test_los_mensajes_SYSTEM_no_cuentan_para_el_objetivo():
    """
    Los 4 joins son SYSTEM y **no entran al corpus**, así que el objetivo de
    70 es de textos de device y en el canal son 74. Si esto cambiara, la
    aritmética del caso cambiaría sin que nada lo dijera.
    """
    from iap_chatroom.ckm_monitor import CKMMonitor
    from iap_chatroom.channel import ChatChannel
    import tempfile

    anterior_m, anterior_c = CKMMonitor._instance, ChatChannel._instance
    CKMMonitor._instance = None
    ChatChannel._instance = None
    try:
        with tempfile.TemporaryDirectory() as d:
            m = CKMMonitor(state_dir=d, min_texts=3)
            assert m.get_state()["parameters"]["system_to_corpus"] is False
    finally:
        CKMMonitor._instance, ChatChannel._instance = anterior_m, anterior_c


# ── el modo de ejecución ─────────────────────────────────────────────────────

def test_el_modo_de_ejecucion_esta_declarado_y_el_default_es_zero_shot(caso):
    """
    La convención de la serie 1 (*"Modo de ejecución: ZERO_SHOT por run"*).
    **El modo es la decisión de limpiar o no el `state_dir`**, y el default no
    puede ser acumular: el plan es volver a ejecutar el caso hasta que COCO se
    conecte, y un arrastre silencioso haría que W abarcara dos intentos sin
    que el log lo dijera.
    """
    assert caso.MODO_ZERO_SHOT == "ZERO_SHOT"
    assert caso.MODO_CONTINUA == "CONTINUA"
    assert caso.MODO_POR_DEFAULT == caso.MODO_ZERO_SHOT


def test_zero_shot_aborta_si_el_corpus_no_esta_en_cero(caso):
    """
    **La exigencia, no la bandera.** Un `--reset` que alguien se olvida de
    pasar deja el intento 2 corriendo sobre el corpus del 1; esto lo frena.
    """
    partida = {"monitor_state": {"corpus_size": 18}}
    aborto = caso._verificar_modo(caso.MODO_ZERO_SHOT, partida)
    assert aborto is not None, "ZERO_SHOT con corpus 18 tiene que abortar"
    assert "ABORTADO" in aborto["que_es"]
    assert aborto["corpus_de_partida"] == 18
    assert aborto["modo_de_ejecucion"] == caso.MODO_ZERO_SHOT


def test_zero_shot_con_corpus_en_cero_sigue(caso):
    assert caso._verificar_modo(
        caso.MODO_ZERO_SHOT, {"monitor_state": {"corpus_size": 0}}
    ) is None


def test_continua_no_aborta_nunca_y_declara_de_cuanto_arranco(caso):
    """
    `CONTINUA` es una **decisión declarada**, no "lo mismo sin reset". No
    aborta; lo que tiene que pasar es que el corpus de partida quede en el log.
    """
    assert caso._verificar_modo(
        caso.MODO_CONTINUA, {"monitor_state": {"corpus_size": 18}}
    ) is None
    cuerpo = CASO_PATH.read_text().split('"""', 2)[2]
    assert '"modo_de_ejecucion": modo' in cuerpo
    assert '"corpus_de_partida": partida["monitor_state"]["corpus_size"]' in cuerpo


def test_el_aborto_dice_que_hay_que_reiniciar_el_server(caso):
    """
    Lo que hace que esto no sea una formalidad: **`--reset` no vacía el corpus
    en memoria**, que `CorpusService` cargó al arrancar `server.py`. Un reset
    sin reinicio se lee como hecho y no lo está. El aborto tiene que decirlo,
    porque es el paso que se olvida.
    """
    aborto = caso._verificar_modo(
        caso.MODO_ZERO_SHOT, {"monitor_state": {"corpus_size": 5}}
    )
    pasos = " ".join(aborto["como_se_arregla"]).upper()
    assert "REINICIAR EL SERVER" in pasos
    assert "--RESET" in pasos
    assert caso.MODO_CONTINUA in pasos


def test_el_modo_se_verifica_sin_tocar_el_canal(caso):
    """
    La verificación es sobre el `estado_de_partida` **ya leído por MCP**: una
    función pura sobre ese dict. No publica, no se une al canal y no llama a
    ningún provider — un aborto por modo no puede dejar rastro en el corpus.
    """
    import inspect

    fuente = inspect.getsource(caso._verificar_modo)
    for prohibido in ("publish", "send_message", "join_channel", "await",
                      "Client", "complete("):
        assert prohibido not in fuente, f"_verificar_modo hace {prohibido}"


# ── el state_dir y el comando ────────────────────────────────────────────────

def test_el_caso_pasa_el_state_dir_y_nada_mas(caso):
    """
    *"Sin lógica en los drivers."* El caso construye los devices con
    `state_dir=` y no escribe él mismo ninguno de los archivos de la corrida.
    """
    from iap_chatroom import run_store

    cuerpo = CASO_PATH.read_text().split('"""', 2)[2]

    # lo único que hace con el directorio: pasarlo
    assert "state_dir=STATE_DIR" in cuerpo

    # **y no escribe ninguno de los archivos de la corrida.** Acá tenía una
    # condición con un `or` que la volvía siempre verdadera —`archivo in
    # str(run_store.ARCHIVOS)` es cierto para todos—, así que el test pasaba
    # sin mirar. Lo que hay que verificar es que el caso no llame a `append`
    # ni abra esos archivos para escribir.
    # **Escribir, no leer** (22 oct 2026, ítem 2). La regla de delamor es
    # *"quien **escribe** es IAP"*: el driver pasa el `state_dir` y no decide
    # qué se guarda. Hasta acá el guardia lo exigía prohibiendo **nombrar**
    # `run_store`, que es más de lo que la regla pide, y dejaba sin cubierta la
    # distinción que la regla hace.
    #
    # El caso **lee** `channel_messages.jsonl` con el lector de `run_store`
    # para poner en su log el total del canal y no la ventana de 20
    # (`mensajes_del_canal`, hueco del intento 2). Leer el registro del canal
    # para reportarlo es lo que un driver hace; lo que no puede es escribirlo.
    #
    # **Queda como pregunta NO BLOQUEA en la BANDEJA**, con este default
    # declarado y reversible en una línea: si delamor prefiere el guardia
    # absoluto, el caso lee el archivo con la stdlib y vuelve a no nombrar
    # `run_store` — a costa de repetir el nombre del archivo, que hoy es de
    # `run_store` y de nadie más.
    escrituras = ("run_store.append", "run_store.set_state_dir",
                  "run_store.reset_failures")
    for llamada in escrituras:
        assert llamada not in cuerpo, f"el caso llama a {llamada}"
    lecturas = [l for l in cuerpo.splitlines() if "run_store." in l]
    permitidas = ("run_store.read", "run_store.CHANNEL_MESSAGES",
                  "run_store.ARCHIVOS")
    for linea in lecturas:
        assert any(p in linea for p in permitidas), (
            f"el caso usa run_store para algo que no es leer: {linea.strip()}"
        )
    for archivo in run_store.ARCHIVOS:
        assert re.search(rf'open\([^)]*{re.escape(archivo)}', cuerpo) is None, (
            f"el caso abre {archivo} por su cuenta"
        )
    # `ARCHIVOS_DE_ESTADO` sí los nombra, y para **preservarlos** (moverlos a
    # `process/` con timestamp), que es lo contrario de escribirlos.
    assert "shutil.move" in cuerpo and "preservar_estado" in cuerpo


def test_el_caso_no_declara_su_propio_mapa_de_providers(caso):
    """
    **P14 punto 3** (delamor, 27 oct 2026: *"un driver de test lo sabe. hay que
    llevar ese knowhow a IAP"*; texto para Code 16, punto 1).

    El guardia de *"sin lógica en los drivers"* mira acá lo mismo que mira con
    el `state_dir`: el caso **pide**, IAP **declara**. Hasta el 28 oct el caso
    tenía su propio `_PROVIDERS` con **dos** de los cuatro providers, y era el
    único mapa nombre → clase del repo.

    Lo que se exige: que el caso no vuelva a declarar un mapa, que no importe
    clases de provider para elegir con ellas, y que **cada nombre que usa esté
    en el registro de IAP** — que es la parte que un `assert` sobre el texto no
    puede dar.
    """
    from iap_chatroom.providers import provider_names

    cuerpo = CASO_PATH.read_text().split('"""', 2)[2]

    assert "_PROVIDERS" not in cuerpo, "el caso volvió a declarar su mapa"
    assert "build_provider" in cuerpo, "el caso no pide el provider por nombre"
    for clase in ("GroqProvider", "GeminiProvider", "AnthropicProvider",
                  "OpenAIProvider"):
        assert f"import {clase}" not in cuerpo, (
            f"el caso importa {clase}: elegir la clase es del registro"
        )

    registrados = provider_names()
    for letra, did, prov, modelo in caso.DEVICES:
        assert prov in registrados, (
            f"{did} pide el provider {prov!r}, que no está en el registro de "
            f"IAP ({', '.join(registrados)})"
        )


def test_el_state_dir_es_el_del_orden(caso):
    """
    `experiments/_state_S2-C0/`, como lo escribe el orden. El nombre sigue al
    campo `case` del panel, que es literalmente `"S2-C0"`; el nombre técnico
    de la corrida es `serie2_caso0` y va en el archivo y en el log.
    """
    from iap_chatroom.ckm_monitor import CASE

    assert caso.STATE_DIR == RAIZ / "experiments" / "_state_S2-C0"
    assert CASE == "S2-C0"
    assert caso.NOMBRE == "serie2_caso0"


def test_el_comando_esta_escrito_en_el_caso():
    """
    *"Dejá el comando."* Y que diga el `--state-dir`: un vivo sin esa bandera
    escribe en el `_state` de agosto, que es traza y no se toca.
    """
    doc = CASO_PATH.read_text().split('"""')[1]
    assert "--state-dir" in doc
    assert "iap_chatroom/server.py" in doc
    assert "experiments/_state_S2-C0" in doc
    assert "NO SE CORRE DESDE ACÁ" in doc


def test_el_caso_no_lo_colecta_pytest():
    """
    Correr el caso es disparar el vivo. `testpaths = ["tests"]` lo deja
    afuera, y este test lo fija: si alguien agregara
    `iap_chatroom/tests` a `testpaths`, la suite dispararía el vivo.
    """
    import tomllib

    cfg = tomllib.loads((RAIZ / "pyproject.toml").read_text())
    testpaths = cfg["tool"]["pytest"]["ini_options"]["testpaths"]
    assert testpaths == ["tests"], testpaths
    assert CASO_PATH.parent.name == "tests"
    assert CASO_PATH.parent.parent.name == "iap_chatroom"


# ── el sesgo del intento 2, declarado con su objetivo ────────────────────────
#
# Los cuatro números que cambian entre el intento 1 y el 2 (delamor y Opus, 21
# oct 2026), con el objetivo declarado: **volumen, para que nazca el primer
# W**. El sesgo va en lo que entra —canal y consigna—; la declaración de CKM
# (el 30, `min_df`, `top_k`) **no se toca**.
#
# `DURATION` ya lo cubre `test_la_duracion_alcanza_para_dos_rebuilds`, contra
# el p pesimista nuevo.

# Lo medido el 22 oct 2026 con los prompts del vivo (5 llamadas por modelo,
# por fase y por condición; techo de la medición alto a propósito): el
# **máximo** de `completion_tokens` que cada modelo gastó cuando no lo
# cortaron. Dos tablas, porque la bandera de razonamiento **no es portable**.
MAXIMO_SIN_BANDERA = {
    "openai/gpt-oss-120b": 213,
    "openai/gpt-oss-20b": 999,      # 988 de razonamiento, para UNA palabra
    "qwen/qwen3.8-27b": 102,
}
MAXIMO_CON_BANDERA_LOW = {
    "openai/gpt-oss-120b": 125,
    "openai/gpt-oss-20b": 128,
    "qwen/qwen3.8-27b": 849,        # la bandera lo EMPEORA: 283-755 de razonamiento
}
# El OTPM que se conoce **medido**, no por los headers: `qwen` da
# `429 OTPM Limit 1000`.
OTPM_MEDIDO_QWEN = 1000


def test_cada_modelo_de_groq_tiene_su_techo_y_cubre_lo_medido():
    """
    **El techo por modelo cubre el máximo que ese modelo gastó bajo la
    condición en la que va a correr** — con la bandera de razonamiento si la
    recibe, sin ella si no.

    El que lo pedía es `gpt-oss-20b`: **sin** bandera gastó **999** tokens en
    el gate —988 de razonamiento, para contestar una palabra— en 1 de 5
    llamadas, y con el techo en 512 esa llamada volvía **vacía** (los 17 vacíos
    del intento 2). **Con** `reasoning_effort="low"` su máximo es **128**, así
    que 512 lo cubre 4×.

    **Si este test falla, el techo quedó por debajo de la cola de su propia
    condición.**
    """
    from iap_chatroom.providers.groq_provider import (
        MAX_TOKENS_POR_MODELO, esfuerzo_de_razonamiento, techo_de_salida,
    )

    for modelo in MAXIMO_SIN_BANDERA:
        assert modelo in MAX_TOKENS_POR_MODELO, f"{modelo} sin techo propio"
        techo = techo_de_salida(modelo)
        con_bandera = esfuerzo_de_razonamiento(modelo) is not None
        maximo = (MAXIMO_CON_BANDERA_LOW if con_bandera
                  else MAXIMO_SIN_BANDERA)[modelo]
        assert techo > maximo, (
            f"{modelo}: techo {techo} no cubre el máximo medido {maximo} "
            f"(bandera={esfuerzo_de_razonamiento(modelo)}) — una llamada así "
            f"vuelve vacía"
        )


def test_la_bandera_de_razonamiento_va_solo_donde_baja_el_gasto():
    """
    **La bandera no es portable, y la tabla lo dice.** En los dos `gpt-oss`
    `reasoning_effort="low"` baja el gasto (213 → 125 y 999 → 128). En
    `qwen3.8` lo **sube**: 102 → 849, con 283–755 de razonamiento donde antes
    no informaba nada, y 2 de 10 llamadas murieron con `429 OTPM`.

    Así que un modelo **no** recibe la bandera por default: la recibe si está
    medido que le baja el gasto. Este test fija las dos direcciones.
    """
    from iap_chatroom.providers.groq_provider import esfuerzo_de_razonamiento

    for modelo, maximo in MAXIMO_SIN_BANDERA.items():
        con = MAXIMO_CON_BANDERA_LOW[modelo]
        baja = con < maximo
        recibe = esfuerzo_de_razonamiento(modelo) is not None
        assert recibe == baja, (
            f"{modelo}: la bandera {'baja' if baja else 'SUBE'} el gasto "
            f"({maximo} -> {con}) y recibe={recibe}"
        )
    # y el que no está en la tabla no la recibe
    assert esfuerzo_de_razonamiento("un/modelo-que-nadie-midio") is None
    assert esfuerzo_de_razonamiento(None) is None


def test_el_techo_de_qwen_entra_en_su_OTPM_medido():
    """
    `qwen` es el único con OTPM medido (`Limit 1000`, intento 1). Su techo
    tiene que entrar ahí **por sí solo** —si no, una llamada sola no cabe en el
    presupuesto de salida del minuto— y además **cuanto más bajo, más llamadas
    caben**: con 256 entran **3** por minuto, con 512 entraba 1.

    **La cuenta, corregida por este test** (22 oct 2026): escribí "con 256
    entran 4" y `1000 // 256 = 3`. El test lo encontró en el primer intento, y
    lo que se corrige es **la afirmación**, no el techo: 256 sigue siendo 2,5×
    el máximo medido de ese modelo sin bandera (102).
    """
    from iap_chatroom.providers.groq_provider import techo_de_salida

    techo = techo_de_salida("qwen/qwen3.8-27b")
    assert techo < OTPM_MEDIDO_QWEN, techo
    assert OTPM_MEDIDO_QWEN // techo >= 3, (
        f"con techo {techo} entran {OTPM_MEDIDO_QWEN // techo} llamadas por "
        f"minuto en el OTPM de qwen"
    )


def test_un_modelo_sin_medir_cae_al_default_declarado():
    """
    Un modelo que nadie midió **no hereda el techo de otro**: cae al default
    declarado, que es el valor del intento 2 —el único vivo entero— y no un
    promedio. Medirlo es la condición para nombrarlo en un caso.
    """
    from iap_chatroom.providers.groq_provider import (
        MAX_TOKENS_POR_DEFAULT, techo_de_salida,
    )

    assert techo_de_salida("un/modelo-que-nadie-midio") == MAX_TOKENS_POR_DEFAULT
    assert techo_de_salida(None) == MAX_TOKENS_POR_DEFAULT


def test_el_techo_deja_margen_sobre_el_pedido_de_la_consigna():
    """
    La cota de abajo, que sigue valiendo: la consigna pide ≈ 80 palabras ≈ 110
    tokens, y el techo tiene que dejar margen o el fix de los `max_tokens`
    —que cerró el truncamiento silencioso— se reabre por el otro lado.
    """
    from iap_chatroom.providers.groq_provider import techo_de_salida

    TOKENS_DEL_PEDIDO = 110
    for modelo in MAXIMO_SIN_BANDERA:
        assert techo_de_salida(modelo) >= 2 * TOKENS_DEL_PEDIDO, modelo


def test_los_otros_dos_providers_no_bajan_su_techo():
    """
    **El sesgo es de Groq y de nadie más.** Gemini queda en 4096 (T3): sus seis
    errores del intento 1 fueron cuota del plan y un 503, ninguno de techo de
    salida, y `gemini-2.5-flash` cuenta los tokens de *thinking* adentro de
    `max_output_tokens` — bajarlo devuelve texto vacío, que el device
    registraría como `generacion_vacia`. Anthropic no corre en este caso.
    """
    from iap_chatroom.providers.gemini_provider import MAX_OUTPUT_TOKENS

    assert MAX_OUTPUT_TOKENS == 4096
    fuente = (RAIZ / "iap_chatroom" / "providers" / "anthropic_provider.py").read_text()
    assert '"max_tokens": 4096' in fuente


def test_las_dos_ventanas_de_historial_son_dos_numeros_distintos():
    """
    **Dos preguntas, dos ventanas** (Opus, 21 oct): el gate decide *si* hablar
    y le alcanza con lo último; el generate *escribe* y necesita ver más del
    canal. Y la del generate **tiene que existir**: hasta el 21 oct
    `_to_chat_messages` usaba `self._history` entero.
    """
    from iap_chatroom.autonomous_device import VENTANA_GATE, VENTANA_GENERATE

    assert VENTANA_GATE == 4
    assert VENTANA_GENERATE == 10
    assert VENTANA_GATE < VENTANA_GENERATE


def test_el_generate_no_manda_mas_que_su_ventana():
    """
    La ventana del generate **medida sobre la salida**, no sobre la constante:
    con 25 mensajes en el historial, el prompt lleva los últimos
    `VENTANA_GENERATE` y no los 25.

    El conteo es de **mensajes del historial**, así que la comparación se hace
    antes del `_coalesce` (que fusiona consecutivos del mismo rol): se cuenta
    cuántos textos del historial aparecen en el prompt.
    """
    from iap_chatroom.autonomous_device import AutonomousDevice, VENTANA_GENERATE
    from iap_chatroom.providers.base import Provider

    class ProviderQueNoLlama(Provider):
        name = "stub"

        async def complete(self, messages):        # pragma: no cover
            raise AssertionError("este test no llama al provider")

    dev = AutonomousDevice(
        device_id="device_x",
        provider=ProviderQueNoLlama(),
        system_prompt="S",
    )
    dev._history = [
        {"device_id": "device_y", "text": f"texto_{i:02d}"} for i in range(25)
    ]
    enviado = "\n".join(m["content"] for m in dev._to_chat_messages())

    assert "texto_24" in enviado, "el último mensaje del canal tiene que estar"
    assert "texto_00" not in enviado, "el primero de 25 no puede seguir viajando"
    presentes = [i for i in range(25) if f"texto_{i:02d}" in enviado]
    assert len(presentes) == VENTANA_GENERATE, presentes
    assert presentes == list(range(25 - VENTANA_GENERATE, 25))


def test_el_gate_no_manda_mas_que_su_ventana():
    """
    La del gate, también sobre la salida: `_decide` arma el prompt con los
    últimos `VENTANA_GATE` mensajes. El provider stub **captura** lo que
    recibe y contesta `OP_SILENCE`, así que no hay red y la decisión no actúa.

    Los 68 errores del provider del intento 1 fueron **todos** de esta fase
    (`fase: "decide"`), así que ésta es la ventana que la medición señala.
    """
    import asyncio

    from iap_chatroom.autonomous_device import AutonomousDevice, VENTANA_GATE
    from iap_chatroom.providers.base import Provider

    capturado = {}

    class ProviderQueCaptura(Provider):
        name = "stub"

        async def complete(self, messages):
            capturado["messages"] = messages
            return "OP_SILENCE"

    dev = AutonomousDevice(
        device_id="device_x",
        provider=ProviderQueCaptura(),
        system_prompt="S",
    )
    observacion = {
        "field": {},
        "history": [
            {"device_id": "device_y", "text": f"texto_{i:02d}", "timestamp": i}
            for i in range(25)
        ],
        "clock": {},
        "tick_anterior": None,
        "trigger": None,
        "own_recent": [],
    }
    assert asyncio.run(dev._decide(observacion)) == "OP_SILENCE"

    enviado = "\n".join(m["content"] for m in capturado["messages"])
    presentes = [i for i in range(25) if f"texto_{i:02d}" in enviado]
    assert len(presentes) == VENTANA_GATE, presentes
    assert presentes == list(range(25 - VENTANA_GATE, 25))


def test_la_consigna_pide_mensajes_cortos_y_es_un_pedido(caso):
    """
    *"Un pedido, no una orden con forma de condición… son LLMs, no se trata de
    presionar"* (delamor, 21 oct). Lo que el test puede fijar: que el pedido
    esté, que esté **en la consigna** —que es lo único que el caso escribe
    además del bloque común—, que siga **sólo en inglés**, y que no venga con
    una condición ni con una amenaza de recorte.

    Lo que **no** fija: que los modelos lo respeten. Eso es del modelo, y es
    el riesgo declarado de la ventana por cantidad.
    """
    from test_prompt_solo_ingles import castellano

    pedido = "Please keep your messages short if you can"
    assert pedido in caso.CONSIGNA
    assert "80 words or fewer" in caso.CONSIGNA
    assert castellano(caso.CONSIGNA) == []
    # el pedido va al final, después de lo que ya decía la consigna
    assert caso.CONSIGNA.index(pedido) > caso.CONSIGNA.index("may move theirs")
    # y es un pedido: sin condición ni recorte anunciado
    for forma in ("must ", "do not exceed", "will be truncated", "only if",
                  "required", "limit of"):
        assert forma not in caso.CONSIGNA.lower(), forma
    # y llega a los cuatro devices, por el system prompt
    for letra, did, _, _ in caso.DEVICES:
        assert pedido in caso.system_prompt(did, letra)


# ── el canal entero en el log, y no la ventana de 20 (hueco del intento 2) ───

def test_el_log_registra_el_canal_entero_desde_el_registro_del_canal(
    caso, tmp_path, monkeypatch
) -> None:
    """
    **Hueco medido en el intento 2** (REG §6.1): el log guardaba en
    `canal.n_mensajes` la lectura de `get_messages`, que tiene **tope 20**, y
    dijo 20 cuando por el canal habían pasado 84.

    `mensajes_del_canal()` lee `channel_messages.jsonl` —el registro que
    escribió el canal— así que el número es el total. Con 25 líneas tiene que
    dar 25: por encima del tope, que es donde el hueco se veía.
    """
    import json

    d = tmp_path / "_state"
    d.mkdir()
    (d / "channel_messages.jsonl").write_text("\n".join(
        json.dumps({"device_id": f"device_{i % 3}", "device_type": "AI",
                    "text": f"texto {i}", "message_id": f"msg-{i}"})
        for i in range(25)
    ) + "\n")
    monkeypatch.setattr(caso, "STATE_DIR", d)

    leidos = caso.mensajes_del_canal()
    assert len(leidos) == 25, len(leidos)
    assert leidos[0]["text"] == "texto 0" and leidos[-1]["text"] == "texto 24"


def test_sin_registro_del_canal_devuelve_vacio_y_el_log_lo_declara(
    caso, tmp_path, monkeypatch
) -> None:
    """
    Un driver sin `state_dir` no tiene registro del canal. Entonces
    `mensajes_del_canal()` devuelve `[]`, y el log **cae a la lectura por MCP
    diciéndolo** (`n_mensajes_segun`): un número con tope y un total no se
    pueden confundir si el registro declara de dónde salió.
    """
    monkeypatch.setattr(caso, "STATE_DIR", tmp_path / "no_existe")
    assert caso.mensajes_del_canal() == []


def test_la_lectura_por_MCP_tiene_tope_20_medido_contra_la_corrida(
    canal_limpio, tmp_path, monkeypatch
) -> None:
    """
    **La inversión, atada a la corrida y no a la fórmula.** Si esto fallara, el
    helper de arriba sobraría. Se publica 25 veces en un canal de verdad y se
    llama a la tool: devuelve **20**, los últimos.

    `run_store.set_state_dir(tmp_path)` va **después** de importar
    `mcp_server`, porque ese import construye el `CKMMonitor` por default y
    apunta el `state_dir` del proceso a la traza de agosto (lo dice el guardia
    de `conftest.py`).
    """
    import asyncio

    from iap_chatroom import mcp_server, run_store

    run_store.set_state_dir(tmp_path / "state")
    monkeypatch.setattr(mcp_server, "channel", canal_limpio)
    for i in range(25):
        asyncio.run(canal_limpio.publish("d0", "AI", f"texto {i}"))

    todos = asyncio.run(mcp_server.get_messages(None))
    assert len(todos) == 20, f"el tope cambió: {len(todos)}"
    assert todos[0]["text"] == "texto 5", todos[0]["text"]
    assert todos[-1]["text"] == "texto 24"
    # y el canal tiene los 25: el tope es de la lectura, no del canal
    assert len(canal_limpio.get_history()) == 25
