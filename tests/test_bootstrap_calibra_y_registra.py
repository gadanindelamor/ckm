"""
test_bootstrap_calibra_y_registra.py — CP1 de `TASK_calibrate_en_el_build_v2`

**D1 + D2 + D5, 27 oct 2026.** El nacimiento de W tiene su condición propia,
pasa por el punto único de calibración *antes de instalar*, y deja su línea.

### Qué cerró esto, medido antes

El V1 del texto 08 (BANDEJA, 26 oct) encontró un **candado doble**: la primera W
la construía `ingest`, y además el cambio de sha ponía en cero los tres
contadores en la misma vuelta, así que **ningún criterio podía votar en el
mensaje en que W nacía**. Consecuencia, medida en las dos corridas vivas: el
COCO del primer ciclo arrancaba con los defaults **por construcción** y su
`calibration.estado` era `None` —ni siquiera `nulo_calibrado`—, en 11 de 51
evaluaciones del intento 2 y 4 de 27 del 3
(`registers/REG_calibrate_no_corre_en_el_build_v1.md`).

Y el nacimiento era **el único cambio de W de una corrida sin línea** en
`rebuild_decisions.jsonl` (hallazgo B).

### Lo que estos tests afirman, y lo que no

Afirman el **mecanismo**: que el origen pasa por calibrate, que su registro
existe y que la vara del primer COCO sale de su propia W. **No afirman que la
calibración separe**: si separa o no es del campo, y con este corpus de test
puede dar cualquiera de los dos. Lo que no puede volver a pasar es que no haya
registro.

El `n_runs` de `calibrate` **no se toca acá**: es de delamor (D6').
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom.ckm_monitor import (                            # noqa: E402
    CAUSA_BOOTSTRAP,
    CRITERIOS_POR_DEFAULT,
    CKMMonitor,
)

TEXTOS = [
    "gun control reduces violence",
    "gun control does not reduce violence",
    "the data on firearms is contested",
    "statistics on weapons are disputed",
    "rights and weapons are in tension",
]


class _Msg:
    def __init__(self, text: str, device_id: str = "d1", device_type: str = "AI"):
        self.text, self.device_id, self.device_type = text, device_id, device_type


@pytest.fixture
def monitor(tmp_path, monkeypatch):
    """`CKMMonitor` con `state_dir` aislado. Es singleton: sin resetear
    `_instance`, un test se quedaría con el corpus del anterior."""
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    cm = CKMMonitor(min_texts=3, rebuild_every=6, min_devices_first_w=1,
                    state_dir=tmp_path / "_state")
    yield cm
    monkeypatch.setattr(CKMMonitor, "_instance", None)


# ── D2: la primera W pasa por calibrate, y antes de instalarse ──────────────

def test_la_primera_W_pasa_por_calibrate(monitor) -> None:
    """
    Con W recién nacida, `punto_calibrate` **existe y tiene estado**.

    `state is None` era el síntoma que el REG midió: no es `nulo_calibrado`
    —"no se ejecutó"—, es que no había registro de ninguna clase.
    """
    cm = monitor
    assert cm._punto_calibrate is None, "el test necesita arrancar sin registro"
    for t in TEXTOS[:3]:                       # el 3º cruza min_texts
        cm.on_message(_Msg(t))

    assert cm._corpus.w_sha() is not None, "W no nació"
    punto = cm._punto_calibrate
    assert punto is not None, "la primera W no pasó por el punto de calibración"
    assert punto["state"] in ("calibrado", "no_calibrado", "nulo_calibrado"), (
        f"estado fuera de los tres de calibrate.py: {punto['state']!r}"
    )


def test_la_primera_W_se_calibro_ANTES_de_instalarse(monitor) -> None:
    """
    **El orden, visible desde afuera y sin mirar el código.** El registro lleva
    dos shas: el de la **candidata** (`w_sha`) y el de la que estaba **viva al
    calibrar** (`w_sha_live_at_calibration`).

    En el origen, la que estaba viva es **ninguna**: `None`. Si la calibración
    hubiera corrido después de instalar, ese campo traería el sha de la W nueva
    — que es exactamente lo que este test invierte.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))

    punto = cm._punto_calibrate
    assert punto["w_sha_live_at_calibration"] is None, (
        "había una W viva al calibrar el origen: se calibró después de instalar"
    )
    assert punto["w_sha"] == cm._corpus.w_sha(), (
        "la W calibrada no es la que quedó instalada"
    )
    assert punto["moment"] == "antes del rebuild, sobre la W candidata"


def test_el_primer_COCO_ya_no_nace_sin_registro_de_calibracion(monitor) -> None:
    """
    **Lo que el REG midió, invertido.** El bloque `coco.calibration` del panel
    era `None` en todas las evaluaciones del primer ciclo. Ahora trae el
    registro, con el `w_sha` de la W que COCO juzga.

    No se afirma que haya separado: se afirma que **hay registro** y que es de
    **su propia** W.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))

    coco = cm._last_panel["coco"]
    assert coco["connected"] is True
    cal = coco["calibration"]
    assert cal is not None, "el primer ciclo sigue sin registro de calibración"
    assert cal["estado"] in ("calibrado", "no_calibrado")
    assert cal["condiciones"]["w_sha"] == coco["w_version_id"], (
        "el registro no es de la W que COCO juzga"
    )
    # Y la vara declara de dónde sale, sea calibrada o default.
    assert coco["thresholds"]["source"] in ("calibrate", "default")


# ── D5: el origen deja su línea ─────────────────────────────────────────────

def test_el_origen_deja_su_linea_con_causa_bootstrap(monitor) -> None:
    """
    Era el único cambio de W de una corrida sin registro (hallazgo B).

    El par `w_sha_antes` / `w_sha_despues` es lo que lo hace legible: antes del
    origen **no había** W, así que `w_sha_antes` es `None`.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))

    d = cm.decisiones_de_rebuild()
    assert len(d) == 1, f"líneas registradas: {[x['causa'] for x in d]}"
    linea = d[0]
    assert linea["causa"] == CAUSA_BOOTSTRAP == "bootstrap"
    assert linea["ocurrio"] is True
    assert linea["motivo_no_rebuild"] is None
    assert linea["w_sha_antes"] is None, "había W antes del origen"
    assert linea["w_sha_despues"] == cm._corpus.w_sha()
    assert linea["w_cambio"] is True
    # La identificación de la serie viaja también en la línea del origen.
    assert linea["series"] == "S2" and linea["case"] == "S2-C0"


def test_el_origen_no_es_un_criterio_de_la_jerarquia(monitor) -> None:
    """
    **D1: no es un criterio, y la jerarquía no cambia.** `bootstrap` no entra en
    la votación, así que en el mensaje del nacimiento **ningún criterio votó**.

    Es la diferencia con `a7d065f`, que lo hizo una cuarta causa de la jerarquía
    y la suite lo tumbó con 30 failed: con `min_texts < rebuild_every` el
    nacimiento pasaba a depender de que votara el volumen.
    """
    cm = monitor
    assert CAUSA_BOOTSTRAP not in CRITERIOS_POR_DEFAULT, (
        "bootstrap entró en la votación: es el error que a7d065f midió"
    )
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))

    assert cm._corpus.w_sha() is not None, "W no nació"
    assert cm._last_rebuild_causa is None, (
        f"votó un criterio en el mensaje del origen: {cm._last_rebuild_causa}"
    )
    assert cm._last_rebuild_signal is False
    estado = cm.get_state()
    assert estado["criterios_rebuild"] == list(CRITERIOS_POR_DEFAULT)
    assert estado["criterios_por_default"] is True


def test_el_causal_event_del_origen_sigue_siendo_rebuild_DIVERGENCIA(
    monitor,
) -> None:
    """
    **Divergencia declarada, no corregida** (decisión de Opus, 27 oct).

    El origen se instala con `_rebuild()`, así que `w_version` lo marca
    `"rebuild"` — igual que un rebuild por ingesta. Lo que lo distingue es su
    línea en `rebuild_decisions.jsonl`, no su marca en `w_version`.

    **El test existe para que la divergencia sea visible**: si alguien la
    corrige, esto falla y la corrección queda a la vista en vez de pasar sola.
    """
    cm = monitor
    for t in TEXTOS[:3]:
        cm.on_message(_Msg(t))

    eventos = [p.causal_event for p in cm._corpus._w_versions.history()]
    assert eventos, "no se registró ninguna versión de W"
    assert eventos[0] == "rebuild", (
        f"el origen cambió de marca en w_version: {eventos[0]!r}. Si fue a "
        "propósito, es la divergencia declarada del CP1 y hay que actualizar "
        "este test y la nota de `build_first_W`."
    )
    assert "rebuild_por_decision" not in eventos[0], (
        "el origen tomó el camino de la decisión del régimen"
    )
