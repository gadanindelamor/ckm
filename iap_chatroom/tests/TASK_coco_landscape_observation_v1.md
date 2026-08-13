# TASK_coco_landscape_observation_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Objetivo

Dos extensiones quirúrgicas a `services/coco.py` y `services/monitor_service.py`:

1. Exponer `d_ckm_coco` en el panel (gap identificado en Armstrong).
2. Registrar qué cambió en el paisaje antes/después de la compresión con α.

La decisión de α (`_alpha_for`) queda como está — retrospectiva, pondera
degradación acumulada hasta ese momento. No se toca.

---

## Contexto conceptual (no implementar — registrar en docstrings)

Cada observación de COCO deja traza en Δ_r.
La traza modifica lo que la siguiente observación encuentra.
No hay retorno al punto de partida. Δ_r abre — no cierra.

Esto no es un bug a corregir — es la condición estructural del instrumento.
El instrumento interviene el campo al medirlo.

`trace_ip` nombra esta condición sin resolverla. Fuera del scope de esta tarea.

---

## Extensión 1 — `d_ckm_coco` en panel

### Qué hacer

En `coco.py`, método `observe()`: al calcular D_ckm, almacenarlo en
`self._last_d_ckm`.

```python
self._last_d_ckm = d_ckm  # después de calcularlo, antes de retornar
```

En `monitor_service.py`, después de llamar `thermostat.observe()`:

```python
if self._thermostat is not None:
    ts = self._thermostat.last_state()
    panel["thermostat"] = {
        ...campos existentes...,
        "d_ckm_coco": getattr(self._thermostat, "_last_d_ckm", None),
    }
```

### Criterio de éxito

```python
panel["thermostat"]["d_ckm_coco"]  # float o None — nunca KeyError
# En Armstrong t=0: debe ser 0.449 (no 0.0 como el D_ckm de Monitor)
```

---

## Extensión 2 — Paisaje antes/después de STOP

### Qué hacer

En `coco.py`, dentro de `observe()`, cuando `stop_applied=True`:

**Antes de aplicar STOP** — registrar estado del paisaje:

```python
W_eff_antes = self._W + self._Delta
A_antes = self._count_attractors(W_eff_antes)
cS_antes = self._mean_cS(W_eff_antes)
```

**Después de aplicar STOP** (Δ_r → α·Δ_r):

```python
W_eff_despues = self._W + self._Delta  # ya comprimido
A_despues = self._count_attractors(W_eff_despues)
cS_despues = self._mean_cS(W_eff_despues)
```

**Registrar en ThermostatState** (o en atributos accesibles):

```python
self._last_landscape_delta = {
    "A_antes": A_antes,
    "A_despues": A_despues,
    "delta_A": A_despues - A_antes,
    "cS_antes": cS_antes,
    "cS_despues": cS_despues,
    "delta_cS": cS_despues - cS_antes,
    "alpha_used": alpha,
    "D_ckm_at_stop": d_ckm,
}
```

**Exponer en panel** (hidden field, mismo nivel que d_ckm_coco):

```python
panel["thermostat"]["landscape_delta"] = getattr(
    self._thermostat, "_last_landscape_delta", None
)
```

### Nota de costo

`_count_attractors` con n_runs=50 es costoso. Opciones:

- `landscape_n_runs=10` como parámetro separado de COCO (default conservador)
- O flag `track_landscape=False` en COCO constructor — activar explícitamente

**Recomendación:** flag `track_landscape=False` por defecto.
En Armstrong test: instanciar con `track_landscape=True`.

```python
coco = COCO(W=corpus.get_W(), track_landscape=True)
```

### Criterio de éxito

```python
# Cuando stop_applied=True y track_landscape=True:
panel["thermostat"]["landscape_delta"]["delta_A"]  # int — atractores ganados/perdidos
panel["thermostat"]["landscape_delta"]["delta_cS"] # float — cambio en cohesión
panel["thermostat"]["landscape_delta"]["alpha_used"] # float — α que produjo ese cambio
```

---

## Extensión 3 — α trajectory log (lightweight)

Registrar la serie de (t, α, D_ckm, delta_A) en `self._alpha_trajectory`:

```python
self._alpha_trajectory.append({
    "t": len(self._alpha_trajectory),
    "alpha": alpha,
    "D_ckm": d_ckm,
    "delta_A": A_despues - A_antes if track_landscape else None,
})
```

Accesible vía:

```python
def alpha_trajectory(self) -> list:
    """Returns list of {t, alpha, D_ckm, delta_A} dicts."""
    return list(self._alpha_trajectory)
```

---

## Orden de ejecución

1. Extensión 1 (d_ckm_coco en panel) — simple, cero costo de cómputo.
2. Extensión 2 (landscape_delta) — con flag track_landscape=False por defecto.
3. Extensión 3 (alpha_trajectory) — append en cada STOP, sin costo extra.
4. Tests: `python services/test_coco.py` — 43/43.
5. Verificar con test_armstrong actualizado: `track_landscape=True`,
   confirmar que landscape_delta aparece en panel y que los valores son coherentes.

---

## NO modificar

- Lógica de `_alpha_for()` — queda retrospectiva como está.
- Constantes ALPHA_MIN, ALPHA_MAX, D_CKM_THRESHOLD.
- Firma de `observe()` — no agregar parámetros ahí.
- `agent_device_skin.py`, `groq_research_agent.py`.
- REGs históricos.

---

## Archivos a modificar

```
services/coco.py          — _last_d_ckm, _last_landscape_delta, _alpha_trajectory,
                            track_landscape flag, alpha_trajectory() método
services/monitor_service.py — panel["thermostat"]["d_ckm_coco"],
                              panel["thermostat"]["landscape_delta"]
iap_chatroom/tests/test_armstrong_stop_coco.py  — track_landscape=True en instancia
```

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
