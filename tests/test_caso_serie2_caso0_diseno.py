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

    La duración se verifica contra la tasa **pesimista** del diseño
    (p = 0.15 de publicar por vuelta): si alcanza ahí, alcanza.
    """
    from iap_chatroom.ckm_monitor import MIN_TEXTS_FIRST_W, REBUILD_EVERY

    assert MIN_TEXTS_FIRST_W == 30 and REBUILD_EVERY == 10
    textos_para_dos_rebuilds = MIN_TEXTS_FIRST_W + 2 * REBUILD_EVERY
    assert textos_para_dos_rebuilds == 50
    assert caso.TEXTOS_OBJETIVO >= textos_para_dos_rebuilds

    P_PESIMISTA = 0.15
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
    assert "import run_store" not in cuerpo, (
        "el caso importa run_store: la escritura tiene que estar en IAP"
    )
    # sin el punto no alcanza: el docstring de `construir_devices` nombra
    # `run_store` para decir que la lógica está ahí y no acá.
    assert "run_store." not in cuerpo, "el caso llama a run_store"
    for archivo in run_store.ARCHIVOS:
        assert re.search(rf'open\([^)]*{re.escape(archivo)}', cuerpo) is None, (
            f"el caso abre {archivo} por su cuenta"
        )
    # `ARCHIVOS_DE_ESTADO` sí los nombra, y para **preservarlos** (moverlos a
    # `process/` con timestamp), que es lo contrario de escribirlos.
    assert "shutil.move" in cuerpo and "preservar_estado" in cuerpo


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
