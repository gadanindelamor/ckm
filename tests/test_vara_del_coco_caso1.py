"""
test_vara_del_coco_caso1.py — D4 de `TASK_calibrate_en_el_build_v2`

**La vara de COCO sale del lugar de la calibración en el estado, y nunca de otra
W.** CP2, 27 oct 2026.

### El caso 1, medido antes de cerrarlo

El V4 del texto 08 (BANDEJA, 26 oct) encontró la forma exacta: después de una
calibración que **separa**, otra que **no separa** reemplazaba el registro y
**no limpiaba los números**. El panel decía `source: "calibrate"`,
`calibrated: true`, con **los números de la W vieja** y el `w_sha` de **la W que
falló**. O sea: nombraba la W equivocada, y **ningún campo ataba los números a
su W**.

En los datos de los dos vivos **no se produjo** —75 de 78 evaluaciones usaron
los defaults y la única calibración exitosa fue la última—, así que estaba en el
código y no en la traza. Estos tests lo producen a mano y verifican que ahora no
pasa.

### Cómo se produce sin un corpus que separe

La calibración vive en el estado (`CKMlandscapeConfig.calibracion`), y el estado
se puede escribir. Así que el registro se pone a mano, con el `w_sha` que cada
caso necesita, y lo que se mide es **de dónde deriva COCO su vara** — que es el
mecanismo, no el campo. Si `calibrate` separa o no sobre un corpus real es otra
pregunta, y es del campo.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "services"))
from ckm_landscape_config import CKMlandscapeConfig            # noqa: E402
from coco import D_CKM_THRESHOLD, FRAC_REC_MIN                 # noqa: E402
from corpus_service import CorpusService                       # noqa: E402
from monitor_service import MonitorService                     # noqa: E402

# **Los textos tienen que compartir vocabulario.** Con `min_df = 2` un nodo
# tiene que aparecer en al menos dos textos; con tres textos sin palabras en
# común la extracción no da nodos, W queda en `None` y el corpus no sale de
# acumulación. La primera versión de este archivo usaba tres textos disjuntos y
# los cinco tests caían con `KeyError: 'coco'` — `evaluate` devuelve el panel de
# acumulación, que no tiene ese bloque. Es un defecto del test, encontrado al
# correr la suite; `_armar` ahora declara la precondición.
TEXTOS = [
    "gun control reduces violence and saves lives",
    "gun control does not reduce violence",
    "the data on gun violence is contested",
    "statistics on gun control are disputed",
    "gun rights and gun control are in tension",
]
NUEVOS = [
    "mental health is the real cause of gun violence",
    "armed citizens deter gun crime in their communities",
    "red flag laws remove guns from dangerous people",
]
PROMPT = "gun control laws reduce violence"
# `n_runs` chico en los dos contadores: estos tests miden de dónde sale la vara,
# no el paisaje.
COCO_CONFIG = {"track_landscape": True, "n_runs": 10}


def _armar(tmp_path):
    corpus = CorpusService(storage_path=str(tmp_path / "c.json"),
                           min_texts=3, top_k=8)
    corpus.ingest(TEXTOS)
    assert corpus.mode == "evaluation", (
        "el corpus quedó en acumulación: la extracción no dio nodos y estos "
        "tests miden el panel de COCO, que sólo existe con W"
    )
    cfg = CKMlandscapeConfig(sampling_mode="uniform")
    monitor = MonitorService(corpus, storage_path=str(tmp_path / "m.jsonl"),
                             n_runs_attractors=10, landscape_config=cfg,
                             coco_config=COCO_CONFIG)
    return corpus, cfg, monitor


def _registro(estado, w_sha, valores=None, causa=None):
    """Un registro de `calibrate` con la forma que escribe el canal."""
    return {
        "valores": valores or {},
        "estado": estado,
        "condiciones": {"w_sha": w_sha, "causa": causa},
        "w_sha": w_sha,
        "duration_s": 0.0,
        "blocking": True,
    }


# ── sin registro: el default, DECLARADO ─────────────────────────────────────

def test_sin_registro_la_vara_es_el_default_y_lo_dice(tmp_path) -> None:
    """
    El caso 2 del REG, visto desde la vara: sin calibración, COCO usa 0,40 /
    0,60 — **y ahora el panel dice que son el default y por qué**.
    """
    corpus, cfg, monitor = _armar(tmp_path)
    th = monitor.evaluate(PROMPT)["coco"]["thresholds"]

    assert th["D_CKM_THRESHOLD"] == D_CKM_THRESHOLD
    assert th["FRAC_REC_MIN"] == FRAC_REC_MIN
    assert th["source"] == "default"
    assert th["calibrated"] is False
    assert th["causa"] == "sin_registro_de_calibracion"
    origen = th["origen"]["d_ckm_threshold"]
    assert origen["provenance"] == "DECLARED"
    assert origen["value"] == D_CKM_THRESHOLD
    assert "default de coco.py" in origen["source"]


# ── registro de ESTA W: medido ──────────────────────────────────────────────

def test_con_registro_de_esta_W_la_vara_es_medida(tmp_path) -> None:
    """Lo que la TASK vino a habilitar: la vara sale de la W que COCO juzga."""
    corpus, cfg, monitor = _armar(tmp_path)
    sha = corpus.w_sha()
    cfg.registrar_calibracion(_registro(
        "calibrado", sha,
        valores={"D_CKM_THRESHOLD": 0.0057, "FRAC_REC_MIN": 0.9949},
    ))

    th = monitor.evaluate(PROMPT)["coco"]["thresholds"]
    assert th["D_CKM_THRESHOLD"] == 0.0057
    assert th["FRAC_REC_MIN"] == 0.9949
    assert th["source"] == "calibrate"
    assert th["calibrated"] is True
    assert th["w_sha_match"] is True
    assert th["origen"]["d_ckm_threshold"]["provenance"] == "MEASURED"
    assert sha[:12] in th["origen"]["d_ckm_threshold"]["source"]


def test_un_solo_umbral_medido_se_declara_mixed(tmp_path) -> None:
    """
    **Los dos umbrales se deciden por separado.** `calibrate` puede separar en
    `D_ckm` y no en `frac_rec`, y entonces devuelve `FRAC_REC_MIN = "UNKNOWN"`.

    Antes era todo o nada y un mixto se publicaba como calibrado entero.
    """
    corpus, cfg, monitor = _armar(tmp_path)
    cfg.registrar_calibracion(_registro(
        "calibrado", corpus.w_sha(),
        valores={"D_CKM_THRESHOLD": 0.0057, "FRAC_REC_MIN": "UNKNOWN"},
    ))

    th = monitor.evaluate(PROMPT)["coco"]["thresholds"]
    assert th["source"] == "mixed"
    assert th["calibrated"] is False, "un mixto no es calibrado entero"
    assert th["D_CKM_THRESHOLD"] == 0.0057
    assert th["FRAC_REC_MIN"] == FRAC_REC_MIN, "frac_rec cayó al default"
    assert th["origen"]["d_ckm_threshold"]["provenance"] == "MEASURED"
    assert th["origen"]["frac_rec_min"]["provenance"] == "DECLARED"
    assert "UNKNOWN" in th["origen"]["frac_rec_min"]["source"]


# ── el caso 1 ───────────────────────────────────────────────────────────────

def test_caso1_una_calibracion_que_no_separa_NO_deja_la_vara_vieja(
    tmp_path,
) -> None:
    """
    **El caso 1, cerrado.** Calibración que separa sobre W1 → COCO1 con vara
    medida. Después W cambia y la calibración de W2 **no separa**: COCO2 **no**
    hereda los números de W1.

    Antes de D4: el panel habría dicho `calibrate` / `calibrated: true` con
    `0.0057` —el número de W1— y el `w_sha` de W2 en el registro.
    """
    corpus, cfg, monitor = _armar(tmp_path)
    sha1 = corpus.w_sha()
    cfg.registrar_calibracion(_registro(
        "calibrado", sha1,
        valores={"D_CKM_THRESHOLD": 0.0057, "FRAC_REC_MIN": 0.9949},
    ))
    th1 = monitor.evaluate(PROMPT)["coco"]["thresholds"]
    assert th1["D_CKM_THRESHOLD"] == 0.0057, "el test necesita la vara medida"

    # W cambia, y la calibración de la W nueva no separa.
    corpus.ingest(NUEVOS)
    sha2 = corpus.w_sha()
    assert sha2 != sha1, "el test necesita que W se mueva"
    cfg.registrar_calibracion(_registro(
        "no_calibrado", sha2, causa="sin_separacion"))

    th2 = monitor.evaluate(PROMPT)["coco"]["thresholds"]
    assert th2["D_CKM_THRESHOLD"] != 0.0057, (
        "COCO heredó la vara de la W anterior: es el caso 1"
    )
    assert th2["D_CKM_THRESHOLD"] == D_CKM_THRESHOLD
    assert th2["source"] == "default"
    assert th2["calibrated"] is False
    assert th2["causa"] == "no_calibrado:sin_separacion"
    assert th2["origen"]["d_ckm_threshold"]["provenance"] == "DECLARED"


def test_un_registro_de_OTRA_W_no_se_usa_y_el_panel_lo_dice(tmp_path) -> None:
    """
    **Nunca los números de otra W** (D4). Si el registro del lugar no es de la W
    que COCO juzga, no se usa — y el panel **dice de qué W era**, que es el
    campo que faltaba: nada ataba los números a su W.
    """
    corpus, cfg, monitor = _armar(tmp_path)
    ajena = "f" * 64
    cfg.registrar_calibracion(_registro(
        "calibrado", ajena,
        valores={"D_CKM_THRESHOLD": 0.0057, "FRAC_REC_MIN": 0.9949},
    ))

    th = monitor.evaluate(PROMPT)["coco"]["thresholds"]
    assert th["D_CKM_THRESHOLD"] == D_CKM_THRESHOLD, "usó la vara de otra W"
    assert th["source"] == "default"
    assert th["w_sha_match"] is False
    assert th["causa"] == f"calibracion_de_otra_W:{ajena[:12]}"
    assert th["w_sha_del_registro"] == ajena
