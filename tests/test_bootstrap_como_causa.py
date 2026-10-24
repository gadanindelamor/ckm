"""
test_bootstrap_como_causa.py — CP1 de `TASK_calibrate_en_el_build_v1`

**Qué cierra.** `ingest()` construía la primera W, y esa W **no pasaba por el
punto de calibración** —que vive en el bloque de la decisión—, así que el COCO
del primer ciclo arrancaba siempre con los defaults
(`D_CKM_THRESHOLD = 0.40`, `FRAC_REC_MIN = 0.60`), **por construcción y no por
el corpus**: su `calibration.estado` era `None`, ni siquiera `nulo_calibrado`.
11 de 51 evaluaciones del intento 2 y 4 de 27 del 3
(`docs/REG_borrador_calibrate_no_corre_en_el_build.md`).

**El cambio:** `ingest(..., allow_first_W=False)` y una cuarta causa,
`CAUSA_BOOTSTRAP = "bootstrap"` —el nombre que **ya existe** en
`ckm_landscape_config:52`, con el que Monitor ya abre el primer ciclo— puesto
primero en la jerarquía y votando **sólo mientras no hay W**. **No hay
nomenclatura nueva:** llamarlo `"first_w"`, que fue la primera versión, habría
sido un segundo nombre para algo que ya tiene uno (lo señaló delamor con una
palabra: *"LandscapeConfig"*).

### Por qué hay un test con los parámetros POR DEFAULT, y es el que importa

El primer intento de este cambio **no agregó la causa**: le sacó el permiso a
`ingest` y dejó que votara el volumen. La suite lo tumbó con **30 failed**,
porque el volumen pide `_textos_desde_rebuild >= rebuild_every` y donde
`min_texts < rebuild_every` W nacía tarde o no nacía.

**Y el test que yo había escrito pasó**, porque elegí `min_texts=6` con
`rebuild_every=3` — parámetros que **garantizaban** la hipótesis. Un test que
confirmaba en vez de uno que arriesgaba. Así que
`test_la_W_nace_al_cruzar_min_texts_con_rebuild_every_por_default` usa el
`rebuild_every` **de default (10)** contra un `min_texts` chico: es la
configuración que rompió, y **con el cambio anterior este test falla**.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

TEXTOS = [
    "gun control reduces violence and saves lives in urban areas",
    "the second amendment protects the right to bear arms",
    "background checks do not stop criminals from getting weapons",
    "assault weapons bans reduce mass shootings and gun violence",
    "mental health is the real cause of gun violence not firearms",
    "red flag laws remove guns from people in crisis situations",
    "concealed carry permits deter crime in public spaces",
    "gun buyback programs reduce the number of weapons in circulation",
]


class _Msg:
    def __init__(self, device_id, text, device_type="AI"):
        self.device_id = device_id
        self.text = text
        self.device_type = device_type


def _monitor(tmp_path, monkeypatch, **kw):
    import iap_chatroom.ckm_monitor as mod

    monkeypatch.setattr(mod, "_STATE_DIR", tmp_path)
    monkeypatch.setattr(mod.CKMMonitor, "_instance", None)
    return mod, mod.CKMMonitor(**kw)


def _publicar(cm, n, devices=("d1", "d2")):
    for i in range(n):
        cm.on_message(_Msg(devices[i % len(devices)], TEXTOS[i % len(TEXTOS)]))


# ── el test que el intento anterior no habría pasado ────────────────────────

def test_la_W_nace_al_cruzar_min_texts_con_rebuild_every_por_default(
    tmp_path, monkeypatch
) -> None:
    """
    **`min_texts = 6` y `rebuild_every` por default (10).** Es la configuración
    en la que el primer intento fallaba: el volumen no podía votar todavía.

    W tiene que nacer **en el mensaje donde el corpus cruza `min_texts`** con
    ≥ 2 devices, no diez mensajes después.
    """
    mod, cm = _monitor(tmp_path, monkeypatch, min_texts=6)
    assert cm._rebuild_every == 10, (
        "este test mide contra el rebuild_every de default; si cambió, el "
        "número de arriba hay que volver a mirarlo"
    )

    nacio = None
    for i in range(10):
        cm.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % len(TEXTOS)]))
        if cm._corpus.w_sha() is not None:
            nacio = len(cm._corpus._texts)
            break

    assert nacio == 6, (
        f"W nació con {nacio} textos y `min_texts` es 6: el nacimiento quedó "
        f"acoplado al ritmo del rebuild"
    )


def test_la_causa_registrada_es_bootstrap_y_no_volumen(tmp_path, monkeypatch) -> None:
    """
    La línea de la decisión tiene que decir **`bootstrap`**, el mismo string
    con el que la Config abre el ciclo: un nombre, un concepto. El atajo descartado
    —un `or` en el criterio de volumen— habría escrito `causa: "volumen"` para
    algo que no es volumen: el registro mintiendo sobre su propia razón.
    """
    mod, cm = _monitor(tmp_path, monkeypatch, min_texts=6)
    _publicar(cm, 8)

    dec = cm.decisiones_de_rebuild()
    assert dec, "no se registró ninguna decisión"
    nacimiento = [d for d in dec if d.get("ocurrio") and d.get("w_sha_antes") is None]
    assert len(nacimiento) == 1, nacimiento
    assert nacimiento[0]["causa"] == mod.CAUSA_BOOTSTRAP == "bootstrap"


def test_el_primer_W_deja_registro_de_calibracion(tmp_path, monkeypatch) -> None:
    """
    **El punto del cambio.** Antes la primera W dejaba `punto_calibrate: None`
    porque nunca se la intentó calibrar. Ahora pasa por el mismo punto que los
    rebuilds y deja su registro **separe o no**: `calibrado`, `no_calibrado` y
    `nulo_calibrado` son tres cosas distintas, y `None` no es ninguna.

    Y el `moment` conserva **un solo valor**: la asimetría que la TASK
    discutía se eliminó en vez de declararse.
    """
    mod, cm = _monitor(tmp_path, monkeypatch, min_texts=6)
    _publicar(cm, 8)

    assert cm._corpus.w_sha() is not None, "no nació W"
    pc = cm.get_state()["punto_calibrate"]
    assert pc is not None, "la primera W volvió a nacer sin pasar por calibrate"
    assert pc["state"] in ("calibrado", "no_calibrado", "nulo_calibrado"), pc
    assert pc["moment"] == "antes del rebuild, sobre la W candidata"


def test_la_condicion_de_dos_devices_sigue_gobernando(tmp_path, monkeypatch) -> None:
    """
    *"≥ min_texts mensajes de ≥ 2 devices"* salió del argumento de `ingest` y
    **sigue viva** en `no_rebuild_reason(allow_first_w)`, que es donde decide.
    """
    mod, cm = _monitor(tmp_path, monkeypatch, min_texts=6)
    _publicar(cm, 10, devices=("d1",))
    assert len(cm._corpus._texts) >= 6
    assert cm._corpus.w_sha() is None, "W nació con un solo device"
    assert cm._corpus.no_rebuild_reason(False) == "primer_W_no_habilitado"

    cm.on_message(_Msg("d2", TEXTOS[0]))
    assert cm._corpus.w_sha() is not None, "con el segundo device tenía que nacer"


def test_ingest_por_si_solo_ya_no_construye_W(tmp_path, monkeypatch) -> None:
    """`ingest` acumula y no construye W: la segunda puerta se cerró."""
    mod, cm = _monitor(tmp_path, monkeypatch, min_texts=6)
    c = cm._corpus
    c.ingest(TEXTOS[:8], allow_first_W=False)
    assert len(c._texts) >= 6 and c.w_sha() is None


# ── el borde declarado ──────────────────────────────────────────────────────

def test_sin_la_causa_bootstrap_el_nacimiento_vuelve_a_depender_del_volumen(
    tmp_path, monkeypatch
) -> None:
    """
    **El precio, fijado y medido.** Saliendo `bootstrap` de la votación, W vuelve
    a nacer cuando **el volumen** lo permite —acoplada a `rebuild_every`— y no
    cuando el corpus cruza su umbral.

    Con `min_texts = 6` y `rebuild_every = 10`, el volumen recién puede votar
    en el mensaje 10, así que W nace con **10** textos en vez de 6: cuatro
    mensajes de atraso, y el campo midiéndose sobre una W que llegó tarde.

    Queda acá para que el día que alguien toque `criterios_rebuild` se entere
    en la suite y no en un vivo.
    """
    import iap_chatroom.ckm_monitor as m

    mod, cm = _monitor(
        tmp_path, monkeypatch, min_texts=6,
        criterios_rebuild=(m.CAUSA_ESTRUCTURAL, m.CAUSA_VOLUMEN, m.CAUSA_TIEMPO),
    )
    nacio = None
    for i in range(12):
        cm.on_message(_Msg("d1" if i % 2 else "d2", TEXTOS[i % len(TEXTOS)]))
        if cm._corpus.w_sha() is not None:
            nacio = len(cm._corpus._texts)
            break

    assert nacio == 10, (
        f"sin `bootstrap`, W nació con {nacio} textos; se esperaba 10 — el "
        f"mensaje en que el volumen puede votar (rebuild_every)"
    )
    assert nacio != 6, "el borde declarado no existe: nació igual al cruzar min_texts"
