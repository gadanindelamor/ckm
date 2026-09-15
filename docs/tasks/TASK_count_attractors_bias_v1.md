# TASK_count_attractors_bias_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v1 — TASK nueva. Origen: análisis diferencial sesión Ago 2026.*

---

## Convención de versiones

Cada versión es un archivo nuevo con sufijo `_vN.md`.
No sobreescribir versiones anteriores.
La versión activa para Code es siempre la de número más alto.

---

## Contexto — dos sesgos en `_count_attractors`, uno documentado y uno no

`_count_attractors(self, W_eff)` en `services/coco.py` tiene dos sesgos:

**Sesgo 1 — n_runs (ya documentado en el docstring):**
El conteo crece ~linealmente con n_runs sin saturar.
Verificado en REG_n_runs_sweep_armstrong_v1.md y REG_stochastic_eval_v1.md.

**Sesgo 2 — uniformidad sobre nodos (no documentado):**
```python
n_act = max(1, int(round(rng.uniform(0.3, 0.7) * self.N)))
s0[rng.choice(self.N, n_act, replace=False)] = 1.
```
`rng.choice(self.N, ...)` asigna probabilidad idéntica a cada nodo como
candidato al estado inicial — independientemente de su posición en W_eff,
su conectividad, o su rol estructural.

Con W sparse (μ_W = 0.004519, N=32), la mayoría de estados iniciales
generados caen en zonas de acoplamiento casi cero. El sistema los expulsa
en t=1. `_count_attractors` mide dinámica de expulsión, no diversidad
del paisaje. Es una cota inferior más baja de lo necesario.

Con W_mixta + nodo tipo-965 (asimetría 100× en Δ), el espacio de estados
es fuertemente anisotrópico. Un generador uniforme sobremuestra zonas
muertas y submuestrea las líneas de tensión donde opera COCO.

Estos dos sesgos son independientes. Esta tarea trata el segundo.

---

## Paso 0 — Verificación previa OBLIGATORIA

```bash
cat services/coco.py
```

Leer y reportar:
- Firma exacta de `_count_attractors(self, W_eff)` — parámetros actuales
- Firma exacta de `_mean_cS()` — comparte el mismo loop de muestreo,
  confirmar si usa la misma secuencia RNG
- Si hay tests que llaman `_count_attractors` directamente (no solo
  indirectamente vía `observe()`)
- Número actual de tests: verificar contra 28/28

---

## Tarea 1 — Documentar el sesgo de uniformidad

Agregar al docstring de `_count_attractors` la descripción del sesgo 2:

```
Sesgo estructural: rng.choice(self.N, ...) asigna probabilidad uniforme
a cada nodo como candidato al estado inicial. Con W sparse o anisotrópica
(p.ej. presencia de nodo tipo-965), esto sobremuestra zonas de acoplamiento
bajo. El método cuenta una cota inferior más conservadora que la diversidad
real del paisaje. Para muestreo informado por W_eff, usar weighted=True
(ver parámetro).
```

No cambiar nada más en esta tarea. Solo el docstring.

---

## Tarea 2 — Agregar modo ponderado (weighted=True)

**Cambio mínimo**: agregar parámetro `weighted: bool = False` a
`_count_attractors`. Comportamiento por defecto idéntico al actual.

Cuando `weighted=True`:
```python
# Peso de cada nodo = actividad marginal en W_eff
fi = np.abs(W_eff).sum(axis=1)          # vector N
fi_sum = fi.sum()
if fi_sum > 0:
    probs = fi / fi_sum                  # distribución sobre nodos
else:
    probs = None                         # fallback a uniforme

s0[rng.choice(self.N, n_act, replace=False, p=probs)] = 1.
```

**Por qué `|W_eff.sum(axis=1)|`**: es la frecuencia marginal de cada nodo
en el paisaje que se está evaluando. Nodos con mayor acoplamiento en W_eff
tienen mayor probabilidad de estar en la cuenca de un atractor real.
No requiere cómputo adicional de β_c — usa la estructura de W_eff directamente.

**Fallback explícito**: si fi_sum == 0 (W_eff completamente cero), caer
en distribución uniforme sin error.

---

## Tarea 3 — `_mean_cS` (si comparte el loop)

Si `_mean_cS` usa la misma secuencia RNG con la misma semilla:
- Agregar el mismo parámetro `weighted: bool = False` con la misma lógica
- Si no comparte el loop, documentarlo en el docstring de `_mean_cS`

Code decide según lo que encuentre en Paso 0.

---

## Lo que NO cambia

- Firma pública de `observe()`, `delta_state()`, ni ningún otro método
- Comportamiento con `weighted=False` (default) — idéntico al actual
- `self._seed`, `self._n_runs` — sin modificar
- Los 28 tests deben pasar sin cambios

---

## Criterio de éxito

```bash
python tests/test_coco.py
```
→ 28/28. Sin regresiones.

Prueba manual que `weighted=True` produce resultado diferente a
`weighted=False` sobre W con nodo de alta conectividad:
```python
coco = COCO(W=W, seed=0, n_runs=50)
a_uniform = coco._count_attractors(W, weighted=False)
a_weighted = coco._count_attractors(W, weighted=True)
# No necesariamente distintos — pero el path de código diferente se ejecuta
```

---

## Convenciones

- Archivo modificado: `services/coco.py` únicamente
- REG: `registers/REG_count_attractors_bias_v1.md` — generar tras
  verificar que tests pasan, no antes

---

## Bloqueo explícito

Si agregar `weighted` como parámetro de `_count_attractors` requiere
modificar la firma pública de `observe()` o cualquier método que lo
llame externamente — detener y reportar. No encadenar cambios.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
