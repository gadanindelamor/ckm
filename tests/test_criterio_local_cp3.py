"""
CP3 — `criterio_local` instancia el engine, y lo que cambia se mide

`TASK_ckm_trust_rule_v1`, CP3 (orden de delamor, 13 oct). El CP2 verificó el
mapeo **sobre el vivo 03**: 24 registros, un corpus. Este archivo verifica lo
que el CP2 no podía — **el espacio de entradas completo** — contra una **copia
congelada** de la cascada que había antes del CP3.

## Por qué una copia congelada y no "los tests pasan"

Regla de completitud del proyecto: *"una aserción que repite la fórmula del
código no encuentra un off-by-one"*. Comparar el engine contra mi lectura de la
cascada verificaría mi lectura. `_CASCADA_ANTES` es la cascada **tal cual
estaba** en `60e21f5` (`iap_chatroom/criterio_local.py:252-282`), copiada sin
tocar nada salvo sacarla del objeto: es el oráculo, no un resumen.

El barrido recorre el producto de:

- `tick`: `None` y un entero
- `n_nuevos`: 0, 1, 7
- `nombrado`: False, True
- `nunca_llamo`: False, True
- `vueltas_sin_llamar`: 0, 1, piso−1, piso, piso+1
- `piso_vueltas`: 1, 3, 12

La auditoría se neutraliza (`tasa_auditoria=0.0` y `tasa_auditoria_pase=0.0`):
**no es de la regla** —no resuelve un empate, la mide—, así que entra en su
propio test y no en el barrido.

## El resultado

- **`llamar` es idéntico en las 360 combinaciones.** Ninguna excepción.
- **`motivo`/`via` difieren en exactamente un caso**, el declarado en el
  docstring del módulo: **piso vencido y campo positivo a la vez**. La cascada
  evaluaba el piso antes del campo (`piso`/`VIA_PISO`); la forma hace decidir
  al campo primero y el engine ni llega a evaluar el piso
  (`mensajes_nuevos`/`nombrado`, `VIA_CRITERIO`).

Esa colisión es **0 de 24 en el vivo 03** (lo mide
`test_criterio_local_como_instancia.py`). Acá se mide cuántas son en el barrido
y se exhibe que no hay ninguna otra.
"""

import itertools
import random
from typing import Optional

import pytest

from iap_chatroom.criterio_local import (
    MOTIVO_AUDITORIA,
    MOTIVO_MENSAJES,
    MOTIVO_NOMBRADO,
    MOTIVO_PISO,
    MOTIVO_PRIMERA,
    MOTIVO_SIN_CAMBIO,
    VIA_AUDITORIA,
    VIA_CRITERIO,
    VIA_PISO,
    CriterioLocal,
    UmbralesCriterioLocal,
)


# ── El oráculo: la cascada de `60e21f5`, copiada sin tocar ──────────────────

def _CASCADA_ANTES(*, tick, n_nuevos, nombrado, nunca_llamo,
                   vueltas_sin_llamar, piso_vueltas) -> tuple:
    """
    `iap_chatroom/criterio_local.py:252-282` en `60e21f5`, con el sorteo de la
    auditoría sacado (va en su propio test) y el estado pasado por argumento.

    Devuelve `(llamar, motivo, via)`.
    """
    # (a) El clock UNKNOWN: se llama. No se puede evaluar el piso sin tick.
    if tick is None:
        return (True, "tick_UNKNOWN", VIA_CRITERIO)
    # (b) La primera vuelta: **nunca llamo** no es "llamo hace 0 vueltas".
    if nunca_llamo and vueltas_sin_llamar == 0:
        return (True, MOTIVO_PRIMERA, VIA_CRITERIO)
    # (c) El piso, deterministico. Va antes que todo lo demas.
    if vueltas_sin_llamar >= piso_vueltas:
        return (True, MOTIVO_PISO, VIA_PISO)
    # (d) El criterio propiamente: lo que cambio.
    if nombrado:
        return (True, MOTIVO_NOMBRADO, VIA_CRITERIO)
    if n_nuevos > 0:
        return (True, MOTIVO_MENSAJES, VIA_CRITERIO)
    # (e) La auditoria: fuera del barrido, tasa 0.0.
    # (f) El skip, con su motivo y sus deltas.
    return (False, MOTIVO_SIN_CAMBIO, None)


def _ahora(*, tick, n_nuevos, nombrado, nunca_llamo,
           vueltas_sin_llamar, piso_vueltas) -> tuple:
    """El `criterio_local` de hoy, con el estado interno **puesto a mano** para
    que las dos vean exactamente la misma entrada."""
    f = CriterioLocal(
        umbrales=UmbralesCriterioLocal(piso_vueltas=piso_vueltas,
                                       tasa_auditoria=0.0,
                                       tasa_auditoria_pase=0.0),
        rng=random.Random(0),
    )
    f._tick_ultima_llamada = None if nunca_llamo else 0
    f._vueltas_sin_llamar = vueltas_sin_llamar
    r = f.evaluar(tick=tick, n_nuevos=n_nuevos, nombrado=nombrado)
    return (r["llamar"], r["motivo"], r["via"])


def _barrido():
    """El producto completo. `(entrada, antes, ahora)` por combinación."""
    for piso in (1, 3, 12):
        ejes = itertools.product(
            (None, 5),                                   # tick
            (0, 1, 7),                                   # n_nuevos
            (False, True),                               # nombrado
            (False, True),                               # nunca_llamo
            sorted({0, 1, piso - 1, piso, piso + 1}),    # vueltas_sin_llamar
        )
        for tick, n, nom, nunca, v in ejes:
            if v < 0:
                continue
            e = dict(tick=tick, n_nuevos=n, nombrado=nom, nunca_llamo=nunca,
                     vueltas_sin_llamar=v, piso_vueltas=piso)
            yield e, _CASCADA_ANTES(**e), _ahora(**e)


# ── Lo que NO cambió: la decisión ───────────────────────────────────────────

def test_llamar_es_identico_en_todo_el_barrido() -> None:
    """**El resultado del CP3.** El gate `f96c234` sobre lo único que sale del
    filtro hacia el lazo: si se llama a D o no."""
    difs = [(e, a[0], b[0]) for e, a, b in _barrido() if a[0] != b[0]]
    assert not difs, f"la decisión cambió en {len(difs)} combinaciones: {difs[:5]}"


def test_el_barrido_cubre_las_dos_decisiones_y_no_es_trivial() -> None:
    """Un barrido donde todo da `llamar=True` no verificaría nada del skip."""
    filas = list(_barrido())
    assert len(filas) >= 300
    decisiones = {a[0] for _, a, _ in filas}
    assert decisiones == {True, False}
    # y los seis motivos de la cascada aparecen, salvo el de la auditoría, que
    # está neutralizada a propósito
    motivos = {a[1] for _, a, _ in filas}
    assert motivos == {"tick_UNKNOWN", MOTIVO_PRIMERA, MOTIVO_PISO,
                       MOTIVO_NOMBRADO, MOTIVO_MENSAJES, MOTIVO_SIN_CAMBIO}


# ── Lo que SÍ cambió: un rótulo, y sólo en la colisión piso-campo ───────────

def test_cuantas_difieren_en_motivo_y_en_via_y_son_las_mismas() -> None:
    """
    El conteo que pidió delamor (13 oct). **60 de 312** difieren en `motivo` y
    **las mismas 60** difieren en `via`. Ninguna otra.

    Que sean **las mismas filas** importa: si `motivo` cambiara en un conjunto y
    `via` en otro, habría dos diferencias y no una.

    El 60 es **del barrido**, no una tasa esperable: un tercio de las filas tiene
    `piso_vueltas=1`, que sobre-representa la colisión. En `vivo_03` es 0 de 24.
    """
    filas = list(_barrido())
    clave = lambda e: tuple(sorted(e.items()))
    dif_motivo = {clave(e) for e, a, b in filas if a[1] != b[1]}
    dif_via    = {clave(e) for e, a, b in filas if a[2] != b[2]}

    assert len(filas) == 312
    assert len(dif_motivo) == 60
    assert dif_motivo == dif_via, "motivo y via difieren en filas distintas"

    # y los únicos pares de rótulos que se dan vuelta son los de la colisión
    assert {(a[1], b[1]) for _, a, b in filas if a[1] != b[1]} == {
        (MOTIVO_PISO, MOTIVO_MENSAJES), (MOTIVO_PISO, MOTIVO_NOMBRADO)}
    assert {(a[2], b[2]) for _, a, b in filas if a[2] != b[2]} == {
        (VIA_PISO, VIA_CRITERIO)}


def test_la_unica_diferencia_es_el_rotulo_de_la_colision_piso_campo() -> None:
    """
    La diferencia declarada en el docstring del módulo, **medida**: cuando el
    piso venció **y** el campo da positivo, la cascada rotulaba `piso` y la
    forma rotula el campo. La decisión es la misma: se llama igual.

    Cualquier otra diferencia de rótulo haría fallar este test, que es para lo
    que está.
    """
    difs = [(e, a, b) for e, a, b in _barrido() if a != b]
    assert difs, "no hubo ninguna diferencia: la colisión debería estar en el barrido"
    for e, antes, ahora in difs:
        # la colisión, y nada más que la colisión
        assert e["tick"] is not None
        assert not (e["nunca_llamo"] and e["vueltas_sin_llamar"] == 0)
        assert e["vueltas_sin_llamar"] >= e["piso_vueltas"]
        assert e["n_nuevos"] + int(e["nombrado"]) > 0
        # antes: el piso. ahora: el campo. Y la decisión, la misma.
        assert antes == (True, MOTIVO_PISO, VIA_PISO)
        assert ahora[0] is True
        assert ahora[1] in (MOTIVO_MENSAJES, MOTIVO_NOMBRADO)
        assert ahora[2] == VIA_CRITERIO


def test_sin_colision_el_piso_sigue_rotulando_piso() -> None:
    """La contracara: con el campo en cero, el piso rotula como siempre. Si no,
    la diferencia de arriba no sería de la colisión sino del piso entero."""
    for e, antes, ahora in _barrido():
        if (e["tick"] is not None
                and not (e["nunca_llamo"] and e["vueltas_sin_llamar"] == 0)
                and e["vueltas_sin_llamar"] >= e["piso_vueltas"]
                and e["n_nuevos"] + int(e["nombrado"]) == 0):
            assert antes == ahora == (True, MOTIVO_PISO, VIA_PISO)


# ── Las piezas que el barrido deja afuera a propósito ───────────────────────

def test_la_auditoria_sigue_fuera_de_la_forma_y_sortea_igual() -> None:
    """La auditoría **no es de la regla**: mide la regla. Se neutraliza en el
    barrido y se verifica acá, con la tasa en 1.0 y el piso lejos."""
    f = CriterioLocal(
        umbrales=UmbralesCriterioLocal(piso_vueltas=99, tasa_auditoria=1.0),
        rng=random.Random(0),
    )
    f.evaluar(tick=1, n_nuevos=0)                 # gasta la primera vuelta
    r = f.evaluar(tick=2, n_nuevos=0)
    assert (r["llamar"], r["motivo"], r["via"]) == (True, MOTIVO_AUDITORIA,
                                                    VIA_AUDITORIA)
    # y la regla, debajo del overlay, decía que no
    assert _CASCADA_ANTES(tick=2, n_nuevos=0, nombrado=False, nunca_llamo=False,
                          vueltas_sin_llamar=1, piso_vueltas=99)[0] is False


def test_el_sorteo_no_se_corrio_de_lugar() -> None:
    """
    El orden de los sorteos es lo que hace determinístico un RNG con semilla.
    Dos filtros con la misma semilla y la misma entrada tienen que dar la misma
    secuencia; y la secuencia tiene que ser la de **antes** del CP3, así que se
    compara contra el número de tiradas que la cascada hacía.
    """
    def corrida(seed):
        f = CriterioLocal(
            umbrales=UmbralesCriterioLocal(piso_vueltas=5, tasa_auditoria=0.3,
                                           tasa_auditoria_pase=0.5),
            rng=random.Random(seed),
        )
        return [f.evaluar(tick=t, n_nuevos=0) for t in range(1, 21)]

    a, b = corrida(7), corrida(7)
    assert [r["motivo"] for r in a] == [r["motivo"] for r in b]

    # **Exactamente una tirada por vuelta**, y eso ya era así antes del CP3:
    # la que llama por criterio o piso tira `auditado_pase`; la que no llama
    # tiró la auditoría y perdió; la que llama por auditoría tiró la auditoría
    # y ganó, y entonces no tira `auditado_pase`. Las tres ramas, una tirada.
    # Medirlo así es más fuerte que contar por vía: si una rama tirara de más
    # o de menos, acá se ve.
    tiradas = len(a)
    testigo = random.Random(7)
    for _ in range(tiradas):
        testigo.random()
    # el RNG del filtro quedó exactamente donde el testigo
    f = CriterioLocal(
        umbrales=UmbralesCriterioLocal(piso_vueltas=5, tasa_auditoria=0.3,
                                       tasa_auditoria_pase=0.5),
        rng=random.Random(7),
    )
    for t in range(1, 21):
        f.evaluar(tick=t, n_nuevos=0)
    assert f.rng.random() == testigo.random()


def test_el_registro_no_gano_ni_perdio_claves() -> None:
    """Gate `f96c234` sobre la **forma** del registro: las mismas claves que
    antes del CP3. La `Decision` del engine se lee y no se guarda."""
    f = CriterioLocal(umbrales=UmbralesCriterioLocal(piso_vueltas=4,
                                                     tasa_auditoria_pase=1.0))
    r = f.evaluar(tick=1, n_nuevos=0)             # llama: primera vuelta
    assert set(r) == {"llamar", "motivo", "via", "tick", "deltas",
                      "umbrales_calibrados", "umbrales", "auditado_pase"}
    r2 = f.evaluar(tick=2, n_nuevos=0)            # skip
    assert set(r2) == {"llamar", "motivo", "via", "tick", "deltas",
                       "umbrales_calibrados", "umbrales"}
    assert set(r["deltas"]) == {"n_nuevos", "nombrado", "dt_desde_ajeno",
                                "dt_desde_que_hable", "estado_objetivo",
                                "presupuesto", "vueltas_sin_llamar"}
    assert set(r["umbrales"]) == {"dt_minimo_s", "piso_vueltas",
                                  "tasa_auditoria", "tasa_auditoria_pase"}


# ── El casillero que el CP2 declaró alineado y no pudo medir ────────────────

def test_tick_None_ahora_entra_por_el_piso_y_no_por_un_if_previo() -> None:
    """
    Decisión 5 del 12 oct: el piso no evaluable **sube la duda**. El CP2 lo dejó
    declarado como alineado y `vivo_03` no tenía con qué medirlo (0 de 24).

    Acá se mide: sin tick, `trace_streak=None`, el engine marca `FLOOR_UNKNOWN`
    y escala. Se llama a D, igual que antes — pero ahora sale de la regla.
    """
    from services.ckm_trust_rule import ESCALATED, FLOOR_UNKNOWN

    f = CriterioLocal(umbrales=UmbralesCriterioLocal(piso_vueltas=4))
    f.evaluar(tick=1, n_nuevos=0)                 # gasta la primera vuelta
    dec = f._regla(n_nuevos=0, nombrado=False).decide(
        ["llamar"], capacity=None, trace=frozenset(), trace_streak=None,
    )
    assert dec.origin == ESCALATED
    assert FLOOR_UNKNOWN in dec.markers
    assert dec.record["floor_missing"] == "trace_streak_unknown"
    # y el filtro, con esa misma entrada, llama
    r = f.evaluar(tick=None, n_nuevos=0)
    assert r["llamar"] and r["motivo"] == "tick_UNKNOWN"


def test_el_piso_no_se_recalcula_fuera_del_engine() -> None:
    """
    *Un solo corazón.* El rótulo `piso` sale de `record["floor_reached"]`, no de
    volver a comparar `vueltas_sin_llamar` contra `piso_vueltas`. Se verifica
    sobre el texto: la comparación no está en el archivo.
    """
    from pathlib import Path
    texto = (Path(__file__).resolve().parent.parent
             / "iap_chatroom" / "criterio_local.py").read_text()
    assert "_vueltas_sin_llamar >= " not in texto
    assert "floor_reached" in texto


def test_sin_rotulo_no_se_inventa_un_motivo() -> None:
    """El mapeo se declara total. Si deja de serlo, lo dice en vez de rellenar:
    `AssertionError` con el origen, el motivo y el registro."""
    f = CriterioLocal(umbrales=UmbralesCriterioLocal(piso_vueltas=4))
    f._tick_ultima_llamada, f._vueltas_sin_llamar = 0, 1

    class _ReglaQueEscala:
        record = {"trace_present": True}
        origin = "ESCALATED"
        reason = "inventado"
        value = None

        def decide(self, *a, **k):
            return self

    f._regla = lambda **kw: _ReglaQueEscala()
    with pytest.raises(AssertionError, match="llamar sin rotulo"):
        f.evaluar(tick=1, n_nuevos=0)


# ── El vivo 03, replayado por `criterio_local` y no por el mapeo ────────────

def test_vivo_03_las_24_decisiones_siguen_iguales(tmp_path) -> None:
    """
    **La verificación mínima que pidió delamor (13 oct).** El CP2 ya había
    comparado el vivo 03 contra la forma, pero a través del **mapeo escrito en
    el test**. Acá se replayan los 24 registros por `criterio_local` mismo, que
    es lo que el CP3 cambió.

    El replay es **secuencial y con estado**: cada device corre sus vueltas en
    orden y el filtro lleva su propio `_vueltas_sin_llamar`. Si una sola vuelta
    se corriera de lugar, las de atrás se desalinearían y el test lo vería.

    El azar **no se re-sortea**: se guioniza desde el log (`_RngDelLog`), que es
    la misma decisión que tomó el CP2 —re-sortear mediría el RNG y no el
    mapeo—. Hay **exactamente una tirada por vuelta**, y el log dice cuál fue.
    """
    import json
    from pathlib import Path

    log = json.loads(
        (Path(__file__).resolve().parent.parent
         / "experiments" / "vivo_03_criterio_local_log.json").read_text()
    )

    class _RngDelLog(random.Random):
        """Una tirada por vuelta, leída del log en vez de sorteada."""

        def __init__(self, valores):
            super().__init__(0)
            self._v, self._i = list(valores), 0

        def random(self):
            v = self._v[self._i]
            self._i += 1
            return v

    total = 0
    for dev in log["por_device"]:
        regs = dev["registros_criterio"]
        # la tirada de cada vuelta, reconstruida del log: la auditoría que
        # ganó, el `auditado_pase` que salió, o una que no gana nada
        tiradas = []
        for r in regs:
            if r["via"] == "auditoria":
                tiradas.append(0.0)                     # la auditoría disparó
            elif r["llamar"]:
                tiradas.append(0.0 if r.get("auditado_pase") else 1.0)
            else:
                tiradas.append(1.0)                     # no disparó
        piso = regs[0]["umbrales"]["piso_vueltas"]
        f = CriterioLocal(
            umbrales=UmbralesCriterioLocal(piso_vueltas=piso),
            rng=_RngDelLog(tiradas),
        )
        for r in regs:
            d = r["deltas"]
            nuevo = f.evaluar(tick=r["tick"], n_nuevos=d["n_nuevos"],
                              nombrado=d["nombrado"],
                              dt_desde_ajeno=d["dt_desde_ajeno"],
                              dt_desde_que_hable=d["dt_desde_que_hable"])
            assert nuevo["llamar"] == r["llamar"], (dev.get("device_id"), r["vuelta"])
            assert nuevo["motivo"] == r["motivo"], (dev.get("device_id"), r["vuelta"])
            assert nuevo["via"] == r["via"], (dev.get("device_id"), r["vuelta"])
            assert nuevo.get("auditado_pase") == r.get("auditado_pase")
            assert nuevo["deltas"]["vueltas_sin_llamar"] == d["vueltas_sin_llamar"]
            total += 1

    assert total == 24, "el vivo 03 tiene 24 registros: si son otros, cambió el corpus"


def test_tick_None_y_despues_un_tick_conocido_no_esta_en_el_barrido() -> None:
    """
    La pregunta de delamor (13 oct). **El barrido no la cubre**: arma un filtro
    por combinación y le pone el estado a mano, así que no tiene **secuencias**.
    Esto sí es una secuencia, y por eso va aparte.

    **Lo que sale, y es de antes del CP3:** la vuelta siguiente a un
    `tick_UNKNOWN` se rotula **`primera_vuelta`**, aunque el device ya haya
    llamado. La llamada con `tick=None` guarda `_tick_ultima_llamada = None`
    —*"no se sabe en qué tick se llamó, y eso no es el tick −1"*, el comentario
    está desde el CP2b— y `_sin_traza()` lee ese *no se sabe* como *nunca*.

    Es I2 por la puerta de atrás: una ausencia leída como un valor. **El CP3 no
    lo introduce ni lo arregla** — se verificó corriendo la misma secuencia
    contra el archivo de `60e21f5` y da lo mismo—, y arreglarlo sería un cambio
    de comportamiento que no es de este checkpoint. Queda clavado acá para que
    no se pierda, y reportado.
    """
    for piso in (3, 12):
        for n_tercera in (0, 2):
            f = CriterioLocal(
                umbrales=UmbralesCriterioLocal(piso_vueltas=piso,
                                               tasa_auditoria=0.0,
                                               tasa_auditoria_pase=0.0),
                rng=random.Random(0),
            )
            r0 = f.evaluar(tick=1, n_nuevos=0)        # primera de verdad
            r1 = f.evaluar(tick=None, n_nuevos=0)     # el clock UNKNOWN
            r2 = f.evaluar(tick=7, n_nuevos=n_tercera)

            assert (r0["motivo"], r0["via"]) == (MOTIVO_PRIMERA, VIA_CRITERIO)
            assert (r1["motivo"], r1["via"]) == ("tick_UNKNOWN", VIA_CRITERIO)
            # la que contesta la pregunta: NO es `mensajes_nuevos` ni `piso`
            assert (r2["motivo"], r2["via"]) == (MOTIVO_PRIMERA, VIA_CRITERIO)
            assert r2["llamar"] is True
            # el estado que lo explica: la llamada sin tick dejó el UNKNOWN
            assert f._tick_ultima_llamada == 7
