"""
test_serie2_caso0_cp1.py — CP1 de `TASK_iap_serie2_caso0_v1`

**Un test por punto del CP1, y cada uno falla si el punto falta.** Ésa es la
consigna de la TASK: *"implementar, con tests que fallen si falta algo"*.

Qué cubre, en el orden del CP1:

- **(a)** el bloque `coco` en el panel de Monitor y en el del canal: conectado,
  id de instancia, `w_version_id`, β_c y μ_W, ‖Δ_r_compresiones‖, hora de la
  última evaluación, disparos, **una sola instancia**;
- **(b)** D_ckm es la forma por masas y **el conteo no está** en el panel;
- **(c)** la tabla de parámetros, y que en el camino vivo quede **un solo
  extractor**;
- **(d)** la identificación `S2` / `S2-C0`, en el panel y en cada registro;
- **(e)** la declaración v2: `min_df`, NFC y palabra completa en el signo;
- **(f)** el reloj en el panel y el ODA que no lo usa como disparador;
- **(g)** el mundo no espera y la participación es finita;
- **(h)** `calibrate` en el punto de rebuild;
- **agregados de delamor (18 oct)**: nadie construye `CKMMonitor` al importar,
  el canal no publica vacíos, y las dos W_eff quedan declaradas.

Los stubs del canal y del provider salen de `test_oda_continuo`, que es donde
viven desde el CP2a: duplicarlos acá los dejaría divergir en silencio.
"""

from __future__ import annotations

import asyncio
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from iap_chatroom.channel import ChatChannel                      # noqa: E402
from iap_chatroom.autonomous_device import (                      # noqa: E402
    DECISION_FIN_DEL_CASO,
)
from iap_chatroom import ckm_monitor as mod_monitor               # noqa: E402
from iap_chatroom.ckm_monitor import CKMMonitor                   # noqa: E402
from services.corpus_service import CorpusService                 # noqa: E402
from services.node_extractor import MIN_DF, NodeExtractorService  # noqa: E402
from services.monitor_service import MonitorService               # noqa: E402
from services.ckm_landscape_config import CKMlandscapeConfig      # noqa: E402

from test_oda_continuo import (                                   # noqa: E402
    ClientStub, ProviderStub, _correr, _device, _publicar_sync,
)


# ── armado común ────────────────────────────────────────────────────────────

TEXTOS = [
    "gun control reduces violence and saves lives in urban areas",
    "the second amendment protects the right to bear arms",
    "background checks do not stop criminals from getting weapons",
    "assault weapons bans reduce mass shootings and gun violence",
    "gun rights are constitutional rights and should not be restricted",
    "mental health is the real cause of gun violence not access to arms",
    "urban areas report more gun violence than rural areas",
    "constitutional rights include the right to bear arms in the home",
]


@pytest.fixture
def canal(monkeypatch):
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return ChatChannel()


@pytest.fixture
def monitor_con_coco(tmp_path):
    """Un MonitorService con COCO, como lo arma el canal: `coco_config`."""
    corpus = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3)
    corpus.ingest(TEXTOS)
    assert corpus.get_W() is not None, "el fixture necesita W"
    m = MonitorService(
        corpus,
        storage_path=str(tmp_path / "t.jsonl"),
        landscape_config=CKMlandscapeConfig(sampling_mode="uniform", n_runs=50),
        coco_config={"track_landscape": True},
    )
    return m


@pytest.fixture
def canal_monitor(tmp_path, monkeypatch):
    """Un `CKMMonitor` nuevo en su propio `state_dir` (el singleton se resetea)."""
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    monkeypatch.setattr(ChatChannel, "_instance", None)
    return CKMMonitor(state_dir=tmp_path / "estado")


class _Msg:
    def __init__(self, device_id, text, device_type="AI"):
        self.device_id = device_id
        self.text = text
        self.device_type = device_type


# ───────────────────────────────────────────────────────────────────────────
# (a) el bloque `coco`: conectado y COMPROBABLE
# ───────────────────────────────────────────────────────────────────────────

def test_a_el_panel_lleva_el_bloque_coco_con_todo_lo_que_pide_la_condicion_2(
    monitor_con_coco,
):
    """
    delamor: *"delamor debe poder ver y comprobar la conexión durante el caso,
    en el panel y en la traza"*. Antes de esto, de COCO salía **un string**.
    """
    panel = monitor_con_coco.evaluate("gun violence in urban areas", device_id="d1")
    coco = panel["coco"]
    assert coco["conectado"] is True
    for clave in ("instancia_id", "generacion", "w_version_id",
                  "w_version_id_monitor", "w_coincide", "mu_W", "beta_c",
                  "Delta_r_compresiones_norma", "ultima_evaluacion_utc",
                  "n_evaluaciones_recibidas", "disparos", "umbrales", "w_eff"):
        assert clave in coco, f"falta {clave} en el bloque coco"
    assert coco["w_coincide"] is True
    assert coco["n_evaluaciones_recibidas"] == 1
    assert coco["ultima_evaluacion_utc"] is not None
    # 0 disparos es un valor: la Serie 2 no le exige disparar.
    assert isinstance(coco["disparos"], int)


def test_a_sin_coco_el_bloque_lo_dice_y_no_inventa_una_conexion(tmp_path):
    corpus = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3)
    corpus.ingest(TEXTOS)
    m = MonitorService(corpus, storage_path=str(tmp_path / "t.jsonl"))
    panel = m.evaluate("gun violence", device_id="d1")
    assert panel["coco"]["conectado"] is False
    assert "motivo" in panel["coco"]


def test_a_una_sola_instancia_de_coco_y_es_la_que_el_panel_dice(monitor_con_coco):
    """
    `instancia_id` tiene que ser **el COCO que Monitor tiene**, no una copia.
    Si alguien construyera un segundo COCO, el id del panel dejaría de ser el
    de `monitor.thermostat`.
    """
    panel = monitor_con_coco.evaluate("gun violence", device_id="d1")
    assert panel["coco"]["instancia_id"] == id(monitor_con_coco.thermostat)
    assert panel["coco"]["instancias"] == 1


def test_a_beta_c_infinito_se_muestra_y_no_se_oculta(monitor_con_coco):
    """
    μ_W ≤ 0 ⇒ β_c = ∞, y **el ∞ es el dato** (revisión de criterios, punto 7).
    Se fuerza una W con media negativa sobre el COCO vivo.
    """
    # COCO nace con el ciclo, que se abre en la primera evaluación: antes de
    # eso `thermostat` es None y no hay a quién mirarle la W.
    monitor_con_coco.evaluate("gun violence", device_id="d1")
    coco = monitor_con_coco.thermostat
    coco.W = -np.abs(coco.W)
    np.fill_diagonal(coco.W, 0.0)
    panel = monitor_con_coco.evaluate("gun violence", device_id="d1")
    assert panel["coco"]["beta_c"] == "inf"
    assert panel["coco"]["beta_c_infinito"] is True
    assert panel["coco"]["mu_W"] < 0


def test_agregado3_las_dos_W_eff_quedan_declaradas(monitor_con_coco):
    """
    Agregado 3 de delamor: COCO mide sobre `W + Δ_r` **crudo** y Monitor sobre
    `W + Δ_r` **escalado**. No se unifican; se declaran.
    """
    panel = monitor_con_coco.evaluate("gun violence", device_id="d1")
    w_eff = panel["coco"]["w_eff"]
    assert w_eff["misma"] is False
    assert "crudo" in w_eff["coco"]
    assert "media(W>0)" in w_eff["monitor"]
    assert w_eff["baseline_coco"] != w_eff["baseline_monitor"]


def test_agregado3_la_diferencia_declarada_es_real_y_no_solo_un_texto(
    monitor_con_coco,
):
    """
    Que el panel lo diga no alcanza: con Δ_r no nulo, las dos W_eff tienen que
    **diferir de verdad**. Si alguien unificara las escalas sin tocar el texto,
    este test se cae.
    """
    m = monitor_con_coco
    W = m.corpus.get_W()
    m._Delta_r = np.zeros_like(W)
    m._Delta_r[0, 1] = m._Delta_r[1, 0] = 3.0
    w_eff_monitor = m._combine_W_Delta(W, m._Delta_r)
    w_eff_coco = W + m._Delta_r
    assert not np.allclose(w_eff_monitor, w_eff_coco)


# ───────────────────────────────────────────────────────────────────────────
# (b) D_ckm por masas, y el conteo afuera
# ───────────────────────────────────────────────────────────────────────────

def test_b_el_panel_del_canal_declara_la_forma_de_D_ckm_y_no_lleva_conteo(
    canal_monitor,
):
    estado = canal_monitor.get_state()
    from services.landscape_engine import D_CKM_FORMA
    assert estado["D_ckm_forma"] == D_CKM_FORMA == "masa_log"
    # El conteo de atractores no se reporta como medida del campo en la S2.
    for clave in estado:
        assert "conteo" not in clave, f"{clave} reporta conteo en el panel S2"
        assert clave != "A_actual" and clave != "A0"


# ───────────────────────────────────────────────────────────────────────────
# (c) la tabla de parámetros, y un solo extractor
# ───────────────────────────────────────────────────────────────────────────

def test_c_el_panel_lleva_la_tabla_de_parametros(canal_monitor):
    p = canal_monitor.get_state()["parametros"]
    assert p["top_k"] == 20
    assert p["pool"] == 60
    assert p["min_df"] == 2
    assert p["n_stopwords"] == 703
    assert p["min_textos_primer_W"] == 30
    assert p["min_devices_primer_W"] == 2
    assert p["rebuild_cada"] == 10
    assert p["n_runs"] >= 1000
    assert p["system_al_corpus"] is False
    assert p["declaracion"].endswith("DECLARACION_extraccion_W_v2.md")


def test_c_un_solo_extractor_en_el_camino_vivo(canal_monitor):
    """
    El extractor muerto de `ckm_monitor.py` (top_k=32, construido y nunca
    usado) **se fue**. El que queda es el de `CorpusService`.
    """
    assert not hasattr(canal_monitor, "_extractor")
    extractores = [
        v for v in vars(canal_monitor).values()
        if isinstance(v, NodeExtractorService)
    ]
    assert extractores == []


def test_c_monitor_evalua_con_el_extractor_del_corpus_no_con_uno_propio(
    tmp_path,
):
    """
    *"Un solo extractor en el camino vivo: el mismo para construir W y evaluar
    σ."* Falla si Monitor vuelve a armarse el suyo: con uno propio, coinciden
    **por default** y basta cambiar un parámetro del corpus para que W salga de
    una tokenización y σ de otra.
    """
    corpus = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3,
                           top_k=7, min_df=1)
    corpus.ingest(TEXTOS)
    m = MonitorService(corpus, storage_path=str(tmp_path / "t.jsonl"))
    assert m._extractor is corpus.extractor
    assert m._extractor.top_k == 7 and m._extractor.min_df == 1


def test_c_el_canal_construye_el_corpus_con_los_parametros_declarados(
    canal_monitor,
):
    ext = canal_monitor._corpus._extractor
    assert ext.top_k == 20, "el canal usaba top_k=32, que no es el declarado"
    assert ext.min_df == 2


def test_c_el_primer_W_espera_30_mensajes(canal_monitor):
    for i in range(29):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    assert canal_monitor._corpus.get_W() is None
    canal_monitor.on_message(_Msg("d1", TEXTOS[0]))
    assert canal_monitor._corpus.get_W() is not None


def test_c_el_primer_W_espera_2_devices(canal_monitor):
    """Con 40 mensajes de **un solo** device no hay W: no es interacción."""
    for i in range(40):
        canal_monitor.on_message(_Msg("solo_uno", TEXTOS[i % 8]))
    assert canal_monitor._corpus.get_W() is None
    assert canal_monitor.get_state()["corpus_status"] == "accumulating"
    canal_monitor.on_message(_Msg("otro", TEXTOS[1]))
    assert canal_monitor._corpus.get_W() is not None


def test_c_el_rebuild_es_cada_10_y_no_dos_veces_min_texts(canal_monitor):
    assert canal_monitor._rebuild_cada == 10
    assert canal_monitor._rebuild_cada != canal_monitor._corpus.min_texts * 2


# ───────────────────────────────────────────────────────────────────────────
# (d) identificación
# ───────────────────────────────────────────────────────────────────────────

def test_d_el_panel_dice_de_que_serie_y_de_que_caso_es(canal_monitor):
    estado = canal_monitor.get_state()
    assert estado["serie"] == "S2"
    assert estado["caso"] == "S2-C0"


def test_d_cada_decision_registrada_lleva_la_identificacion(canal_monitor):
    for i in range(45):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    decisiones = canal_monitor.decisiones_de_rebuild()
    assert decisiones, "el fixture no produjo ninguna decisión de rebuild"
    assert all(d["serie"] == "S2" and d["caso"] == "S2-C0" for d in decisiones)


# ───────────────────────────────────────────────────────────────────────────
# (e) la declaración v2
# ───────────────────────────────────────────────────────────────────────────

def test_e_min_df_es_2_y_viaja_en_la_declaracion(tmp_path):
    corpus = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3)
    d = corpus.declaracion_extraccion()
    assert MIN_DF == 2
    assert d["parametros_del_servicio"]["min_df"] == 2
    assert d["operadores"]["5_seleccion"]["parametros"]["min_df"] == 2
    assert d["referencia"].endswith("DECLARACION_extraccion_W_v2.md")


def test_e_un_termino_de_una_sola_unidad_ya_no_es_nodo():
    """
    `min_df = 2`: lo que aparece en **un** mensaje no co-ocurre con nada fuera
    de él. `unicornio` está en un solo texto; `violence` en varios.
    """
    svc = NodeExtractorService(top_k=20)
    r = svc.accumulate([
        "gun violence in urban areas",
        "gun violence and mental health",
        "urban areas and gun laws",
        "the unicornio appears exactly once here",
    ])
    assert "unicornio" not in r["nodes"]
    assert "violence" in r["nodes"]


def test_e_con_min_df_1_el_mismo_termino_si_entra():
    """El control: lo que lo saca es `min_df`, no otra cosa del corpus."""
    svc = NodeExtractorService(top_k=20, min_df=1)
    r = svc.accumulate([
        "gun violence in urban areas",
        "gun violence and mental health",
        "urban areas and gun laws",
        "the unicornio appears exactly once here",
    ])
    assert "unicornio" in r["nodes"]


def test_e_menos_unidades_que_min_df_no_es_un_error_es_una_salida_vacia():
    svc = NodeExtractorService(top_k=20)
    r = svc.accumulate(["un solo texto con palabras suficientes para tokenizar"])
    assert r["nodes"] == []
    assert r["pairs"] == {}
    assert "perfil" in r


def test_e_el_signo_es_por_palabra_completa():
    """`but` adentro de `distribution` **ya no** marca oposición (v2)."""
    assert CorpusService._has_opposition("the distribution is fair") is False
    assert CorpusService._has_opposition("the data is fair but incomplete") is True
    assert CorpusService._has_opposition("esperó un rato") is False
    assert CorpusService._has_opposition("pero eso no es así") is True


def test_e_el_signo_normaliza_a_NFC_igual_que_el_operador_1():
    """
    Las dos formas de la misma palabra tienen que dar lo mismo. Con los 44
    marcadores ASCII de hoy esto **no cambia ningún resultado** y por eso el
    test usa un marcador inyectado: lo que fija es el mecanismo, no un efecto.
    """
    from services import corpus_service as cs
    nfd = unicodedata.normalize("NFD", "año")
    nfc = unicodedata.normalize("NFC", "año")
    assert nfd != nfc
    original_re = cs._OPPOSITION_RE
    try:
        import re as _re
        cs._OPPOSITION_RE = _re.compile(r"(?<!\w)" + _re.escape(nfc) + r"(?!\w)")
        assert CorpusService._has_opposition(f"hace un {nfd} de esto") is True
    finally:
        cs._OPPOSITION_RE = original_re


def test_e_la_declaracion_v2_existe_y_dice_que_cambio():
    doc = (RAIZ / "docs/defs/DECLARACION_extraccion_W_v2.md").read_text()
    assert "min_df" in doc
    assert "palabra completa" in doc
    assert "Criterios de normalización" in doc


# ───────────────────────────────────────────────────────────────────────────
# (f) el reloj y el ODA continuo
# ───────────────────────────────────────────────────────────────────────────

def test_f_el_tick_del_canal_esta_en_el_panel(canal_monitor):
    estado = canal_monitor.get_state()
    assert isinstance(estado["tick"], int)


def test_f_mirar_el_panel_no_registra_un_tick(canal_monitor):
    """
    El log de ticks es de los devices que observan. Si el panel registrara,
    el silencio del canal dejaría de ser dato.
    """
    canal = ChatChannel()
    antes = len(canal.clock_log())
    canal_monitor.get_state()
    assert len(canal.clock_log()) == antes


def test_f_el_device_decide_sin_que_haya_un_mensaje_nuevo(canal):
    """Falla si un device sólo se activa con mensajes nuevos."""
    dev = _device(ProviderStub(["OP_SILENCE"] * 5))
    _correr(dev, ClientStub(canal), duration=0.05)
    assert len(dev.decisiones()) >= 2
    assert all(d["n_nuevos"] == 0 for d in dev.decisiones())


def test_f_un_tick_no_dispara_una_vuelta(canal):
    """
    Falla si las vueltas siguen a los ticks. El reloj se **observa**: con el
    período del canal en 60 s, un run corto no cambia de tick y sin embargo
    hay varias vueltas.
    """
    dev = _device(ProviderStub(["OP_SILENCE"] * 20))
    _correr(dev, ClientStub(canal), duration=0.05)
    ticks = {d["tick"] for d in dev.decisiones()}
    assert len(dev.decisiones()) > len(ticks)


# ───────────────────────────────────────────────────────────────────────────
# (g) el mundo no espera, y la participación es finita
# ───────────────────────────────────────────────────────────────────────────

class ProviderQueNuncaResponde(ProviderStub):
    """Un provider que no contesta. No es una falla: es que tarda."""

    def __init__(self):
        super().__init__([])

    async def complete(self, messages):
        self.llamadas.append(messages)
        await asyncio.sleep(3600)


def test_g_al_vencer_duration_el_device_no_sigue_vivo(canal):
    """
    Falla si un device que está decidiendo cuando vence el caso queda vivo
    después del fin. **No es un timeout de la decisión**: el corte es el fin
    del caso.
    """
    dev = _device(ProviderQueNuncaResponde())
    t0 = asyncio.get_event_loop_policy().new_event_loop().time()
    del t0
    import time as _t
    inicio = _t.monotonic()
    _correr(dev, ClientStub(canal), duration=0.2)
    transcurrido = _t.monotonic() - inicio
    assert transcurrido < 5, "el device siguió vivo después del fin del caso"
    assert dev._cortado_por_fin_del_caso is True


def test_g_la_vuelta_que_el_fin_del_caso_corto_queda_registrada(canal):
    dev = _device(ProviderQueNuncaResponde())
    _correr(dev, ClientStub(canal), duration=0.2)
    ultima = dev.decisiones()[-1]
    assert ultima["decision"] == DECISION_FIN_DEL_CASO
    assert ultima["resultado_accion"].startswith("no_ocurrio")


def test_g_el_mundo_no_se_bloquea_mientras_un_device_decide(canal):
    """
    Falla si el canal, su reloj u otro device quedan esperando a un device que
    no termina de decidir. El otro device publica y el canal lo sella mientras
    el primero sigue adentro de su llamada.
    """
    lento = _device(ProviderQueNuncaResponde(), device_id="lento")
    rapido = _device(ProviderStub(["INTERACT", "hola desde el rapido"] * 5),
                     device_id="rapido")

    async def correr():
        import iap_chatroom.autonomous_device as mod
        orig = mod.Client
        mod.Client = lambda url: ClientStub(canal)
        try:
            await asyncio.gather(
                lento.run(duration=0.3),
                rapido.run(duration=0.3),
            )
        finally:
            mod.Client = orig

    asyncio.run(correr())
    assert rapido.decisiones(), "el device rápido no llegó a decidir"
    assert canal.tick() is not None
    assert lento._cortado_por_fin_del_caso is True


def test_g_la_traza_lleva_tick_de_observacion_tick_de_accion_y_resultado(canal):
    dev = _device(ProviderStub(["INTERACT", "un mensaje publicado"]))
    _correr(dev, ClientStub(canal), duration=0.05)
    publicadas = [d for d in dev.decisiones() if d["decision"] == "INTERACT"]
    assert publicadas, "el stub no llegó a publicar"
    d = publicadas[0]
    assert d["tick_observacion"] is not None
    assert d["tick_accion"] is not None
    assert d["resultado_accion"] == "publicado"


def test_g_una_accion_que_el_canal_no_acepta_se_registra_como_no_ocurrida(canal):
    """
    *"Si actúa y la circunstancia ya no está, la acción no ocurre y eso se
    registra, no se esconde."* Acá la circunstancia es el canal rechazando.
    """
    class ClientQueRechaza(ClientStub):
        async def call_tool(self, nombre, args=None):
            if nombre == "send_message":
                return type("_R", (), {"data": {"ok": False,
                                                "motivo": "texto_vacio"}})()
            return await super().call_tool(nombre, args)

    dev = _device(ProviderStub(["INTERACT", "algo"]))
    _correr(dev, ClientQueRechaza(canal), duration=0.05)
    rechazadas = [d for d in dev.decisiones()
                  if (d.get("resultado_accion") or "").startswith("no_ocurrio")]
    assert rechazadas


# ───────────────────────────────────────────────────────────────────────────
# (h) `calibrate` en el punto de rebuild
# ───────────────────────────────────────────────────────────────────────────

def test_h_el_panel_muestra_el_resultado_de_calibrate_despues_de_un_rebuild(
    canal_monitor,
):
    for i in range(45):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    punto = canal_monitor.get_state()["punto_calibrate"]
    assert punto is not None, "no hubo rebuild: el fixture no prueba nada"
    assert punto["implementado"] is True
    assert punto["estado"] in ("calibrado", "no_calibrado", "nulo_calibrado")
    assert punto["w_sha"] is not None
    assert "valores" in punto


def test_h_coco_no_sigue_con_el_0_40_del_modulo_despues_de_calibrar(
    canal_monitor,
):
    """
    Falla si COCO sigue con `D_CKM_THRESHOLD = 0.40` después de un rebuild
    **que calibró**. Si no calibró, lo que se exige es que **se vea** que no
    calibró — no que el 0.40 se presente como medido.
    """
    for i in range(60):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    estado = canal_monitor.get_state()
    punto = estado["punto_calibrate"]
    assert punto is not None and punto["implementado"] is True
    coco = estado["coco"]
    assert coco["conectado"] is True
    if punto["estado"] == "calibrado" and isinstance(
        punto["valores"].get("D_CKM_THRESHOLD"), float
    ):
        assert coco["umbrales"]["origen"] == "calibrate"
        assert coco["umbrales"]["calibrado"] is True
        assert coco["umbrales"]["D_CKM_THRESHOLD"] != 0.40
    else:
        assert coco["umbrales"]["calibrado"] is False
        assert coco["calibracion"]["estado"] == punto["estado"]


def test_h_calibrate_corre_ANTES_de_instalar_la_W(canal_monitor):
    """
    **El orden** (delamor, 19 oct): decidido el rebuild, `calibrate` corre
    sobre la **W candidata**, todavía dentro del ciclo i; recién después se
    instala W.

    Falla si `calibrate` corre después de instalar: ahí la W viva en el momento
    de calibrar **sería** la nueva, y los dos shas del panel coincidirían. El
    test exige las dos cosas: que al calibrar estuviera viva la **vieja**, y
    que la candidata sea la que **quedó** instalada.
    """
    for i in range(45):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    punto = canal_monitor.get_state()["punto_calibrate"]
    assert punto is not None and punto["estado"] != "nulo_calibrado"
    assert punto["momento"] == "antes del rebuild, sobre la W candidata"
    # la que se calibró es la que quedó instalada
    assert punto["w_sha"] == canal_monitor._corpus.w_sha()
    # y al calibrar estaba viva otra: si fueran iguales, habría corrido después
    assert punto["w_sha_vigente_al_calibrar"] != punto["w_sha"]


def test_h_sin_salto_no_se_calibra_y_se_ve_por_que(canal_monitor):
    """
    Con señal de rebuild pero sin salto posible —un solo device, el primer W
    sin permiso— **no se calibra**, y el panel dice `nulo_calibrado` con el
    motivo. No es "corrió y no separó".
    """
    for i in range(40):
        canal_monitor.on_message(_Msg("solo_uno", TEXTOS[i % 8]))
    punto = canal_monitor.get_state()["punto_calibrate"]
    assert punto is not None
    assert punto["estado"] == "nulo_calibrado"
    assert punto["motivo"] == "primer_W_no_habilitado"
    assert punto["valores"] == {}


def test_h_el_panel_declara_cuanto_tardo_calibrate_y_que_bloquea(canal_monitor):
    """
    En el salto `calibrate` corre **en el hilo del mensaje**: mientras calibra,
    el canal no atiende. Eso se declara, con el tiempo medido — es el insumo de
    la propuesta de la sombra.
    """
    for i in range(45):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    punto = canal_monitor.get_state()["punto_calibrate"]
    assert punto["bloqueante"] is True
    assert punto["duracion_s"] > 0


def test_h_la_W_candidata_es_la_que_el_rebuild_instala(tmp_path):
    """
    `W_candidata()` no instala nada y acierta: lo que devuelve es,
    byte a byte, lo que el rebuild deja vivo.
    """
    # `rebuild_suspendido=True` como el canal vivo: la ingesta no reconstruye,
    # así que entre el primer W y el salto hay textos nuevos sin instalar.
    corpus = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3,
                           rebuild_suspendido=True)
    corpus.ingest(TEXTOS[:4])
    sha_antes = corpus.w_sha()
    corpus.ingest(TEXTOS[4:])
    candidata = corpus.W_candidata()
    assert corpus.w_sha() == sha_antes, "W_candidata() movió la W viva"
    corpus.rebuild_por_decision("volumen")
    assert np.array_equal(candidata, corpus.get_W())


def test_h_calibrate_no_toca_la_W_viva(canal_monitor):
    for i in range(45):
        canal_monitor.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % 8]))
    W = canal_monitor._corpus.get_W()
    antes = W.copy()
    canal_monitor._calibrar()
    assert np.array_equal(canal_monitor._corpus.get_W(), antes)


# ───────────────────────────────────────────────────────────────────────────
# agregado 1 — nadie construye CKMMonitor al importarse
# ───────────────────────────────────────────────────────────────────────────

def test_agregado1_ningun_modulo_construye_el_monitor_al_importarse():
    """
    Falla si vuelve a aparecer un `CKMMonitor()` a nivel de módulo. En
    `server.py` el primer import es `api_routes`, así que ese pelado ganaba la
    carrera del singleton y el `--state-dir` quedaba en el default.
    """
    for nombre in ("api_routes.py", "ui_gradio.py"):
        fuente = (RAIZ / "iap_chatroom" / nombre).read_text()
        lineas = [
            l for l in fuente.splitlines()
            if "CKMMonitor()" in l and not l.lstrip().startswith("#")
        ]
        assert lineas == [], f"{nombre} construye el monitor al importarse: {lineas}"


def test_agregado1_el_state_dir_pedido_es_el_que_queda(tmp_path, monkeypatch):
    """
    Falla si el singleton nace con el directorio por default habiendo uno
    pedido. Es la grieta que el CP0 encontró, medida de punta a punta.
    """
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    from iap_chatroom import arranque
    pedido = tmp_path / "s2_c0"
    arranque.fijar_state_dir(pedido)
    try:
        import iap_chatroom.api_routes as api_routes
        import importlib
        importlib.reload(api_routes)
        m = arranque.monitor()
        assert m.state_dir == pedido
        assert arranque.declarar()["coincide"] is True
    finally:
        arranque.fijar_state_dir(None)


# ───────────────────────────────────────────────────────────────────────────
# agregado 2 — el canal no publica vacíos
# ───────────────────────────────────────────────────────────────────────────

def test_agregado2_el_canal_no_publica_un_texto_vacio(canal):
    m = asyncio.run(canal.publish("d1", "AI", ""))
    assert m is None
    assert canal.messages == []


def test_agregado2_tampoco_uno_de_solo_espacios(canal):
    assert asyncio.run(canal.publish("d1", "AI", "   \n\t ")) is None
    assert canal.messages == []


def test_agregado2_el_intento_rechazado_queda_con_quien_y_cuando(canal):
    asyncio.run(canal.publish("d1", "AI", "  "))
    intentos = canal.intentos_rechazados()
    assert len(intentos) == 1
    i = intentos[0]
    assert i["device_id"] == "d1"
    assert i["motivo"] == "texto_vacio"
    assert i["tick"] is not None and i["timestamp"] is not None
    # el repr distingue un vacío con espacios de uno sin ellos
    assert i["recibido"] == repr("  ")


def test_agregado2_un_texto_con_contenido_sigue_pasando(canal):
    m = asyncio.run(canal.publish("d1", "AI", "hola"))
    assert m is not None
    assert canal.intentos_rechazados() == []


def test_agregado2_el_vacio_no_llega_al_corpus(canal_monitor, canal):
    """La guarda es del canal, así que vale para cualquiera que publique."""
    canal.add_callback(canal_monitor.on_message)
    asyncio.run(canal.publish("d1", "AI", ""))
    assert canal_monitor.get_state()["corpus_size"] == 0
