# TASK_criterios_diversidad_services_v2.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Reemplaza el orden de ejecución de `TASK_criterios_diversidad_services_v1.md`.
El contexto medido, la medida canónica y el alcance de v1 siguen vigentes —
no se repiten acá, se leen de v1.*

---

## Qué cambia respecto de v1

v1 planteaba tres opciones de diseño (importar / extraer / copiar) y pedía
elegir una. **Propuesta de delamor, adoptada:** no se elige, se ordena.
Baby steps, con una compuerta de verificación entre cada uno, igual que en
`TASK_monitor_service_unificar_rutinas_v1`.

Duplicar deliberadamente **es un paso**, no un estado a evitar. Razón: si
se extrae y se usa en un solo movimiento, cuando un número cambia no hay
forma de saber si vino de la extracción o de lo nuevo. Un paso por vez, cada
uno con su propio cero exacto.

El orden de los dos primeros pasos no es arbitrario. Estandarizar primero
y extraer después hace que la extracción sea demostrablemente un no-op. Al
revés, la extracción tendría que decidir cuál variante gana, y esa decisión
quedaría enterrada dentro del movimiento.

---

## Field check — definición operativa de la compuerta

Después de **cada** paso, y antes de empezar el siguiente:

1. **Replay de corpus fijo**, panel completo idéntico: `D_ckm`, `c_S`,
   `n_rejected_pairs`, `activos_relajado`, `Delta_r_sum`, en **todas** las
   evaluaciones. Cero diferencias, no diferencias chicas.
   Corpus de referencia: los 24 textos de `caso09_run2`, régimen natural,
   `n_runs_attractors=50` — el mismo de
   `TASK_monitor_service_unificar_rutinas_v1`, para que las dos series sean
   comparables.
2. **Tests, sin modificar ningún archivo de tests:**
   `tests/test_coco.py` 28/28 · `tests/test_monitor_services.py` 35/35 ·
   `python services/coco.py` T1-T13 OK ·
   `python services/monitor_service.py` T1-T6 OK ·
   `python services/corpus_service.py` OK.
3. **Reportar y detenerse.** No encadenar pasos sin que delamor vea el
   resultado del field check.

Si un field check no da cero, el paso se revierte — no se ajusta el
criterio.

---

## Paso 1 — censo y estandarización en el lugar

**1.a Censo, antes de tocar nada.** Medido en esta sesión:

| rutina | definiciones | variantes distintas |
|---|---:|---:|
| `_relax` | 7 archivos | 4 |
| `_count_attractors` | 7 archivos | 5 |
| `_cS` | 5 archivos | 2 |

Agrupación de `_relax` por hash del cuerpo normalizado (sin comentarios ni
docstrings):

```
8117251e  services/coco.py (9)  ·  services/monitor_service.py (17)     ← unificados en 5f2ec6c
d3785eb4  experiments/monitor_service_dev.py (8) · experiments/monitor_service.py (8)
eb291655  services/fabrication_service.py (10) · experiments/fabrication_service_dev.py (10)
8957b4b4  process/experiments/coco_thermostat.py (8)
```

**1.b Clasificar cada copia antes de estandarizar.** Tres clases, y sólo
una es candidata:

- **VIVA** — en uso por el runtime. Candidata a estandarizar.
- **TESTIGO** — congelada a propósito, es traza de un estado.
  `process/` entero es testigo: **no se toca**. `services/fabrication_service.py`
  está pendiente de mover a `process/` por decisión de delamor — no se
  estandariza, se mueve cuando esa TASK ocurra.
- **DERIVA vs DIFERENCIA DELIBERADA** — hay que separarlas. Verificado:
  las dos variantes de `_count_attractors` en `services/` **difieren a
  propósito** y está documentado en el docstring de monitor:

  ```python
  # coco.py:717              weighted : bool = False
  # monitor_service.py:382   weighted : Optional[bool] = None  → toma self._sampling_mode
  ```

  Esa diferencia **se preserva**. Estandarizar sólo lo que divergió sin
  intención.

**1.c Estandarizar** las copias VIVAS que difieren por deriva, dejando
cada una idéntica en el cuerpo. Sin mover nada de archivo todavía.

**1.d Marcar el duplicado como paso, no como estado.** Cada copia que
queda deliberadamente duplicada lleva un comentario con: que es un paso de
esta TASK, en qué paso se colapsa, y la fecha. Precedente en el repo:
`force_w_pos` marca la W que produce con
`causal_event="rebuild_debug_force_w_pos"` para que no sea indistinguible
de una natural. Sin marca, en tres meses es una copia más.

**→ FIELD CHECK**

---

## Paso 2 — extraer las rutinas a un archivo aparte

Recién ahora, y sólo si el field check del Paso 1 dio cero.

Un módulo con las primitivas como **funciones puras** sobre
`(W, N, rng, ...)`: `relax`, `relax_orbit`, `sample_s0`, `node_probs`,
`boltzmann_warmup`, `count_attractors`. Los servicios importan de ahí.

Como las copias VIVAS ya son idénticas después del Paso 1, la extracción no
elige nada: es mecánica. Las diferencias deliberadas del Paso 1.b quedan en
el **llamador**, no en la primitiva — es donde corresponden.

Nombre del archivo: decisión de delamor. Sugerencia:
`services/hopfield_sampling.py`.

**→ FIELD CHECK**

---

## Paso 3 — los criterios nuevos, misma forma

Sólo después del field check del Paso 2.

Si un criterio nuevo usa código existente: **duplicar primero, marcado**
(igual que 1.d), field check, y colapsar después. No reusar y extender en
el mismo movimiento.

Alcance y contenido de los criterios: los de v1, sin cambios — muestreo
canónico `sigma0_nivel(rng, N, rho)` con ρ explícito, barrido sobre ρ,
masas `m_o(ρ)`, `N_eff(ρ)`, `T_k(ρ)`, y las cantidades de W sola
(frustración, `frac_neg`, espectro, CV, diagnósticos de exactitud).

**→ FIELD CHECK**

---

## Paso 4 — continuar

Se define cuando los tres anteriores hayan pasado su compuerta. No se
planifica desde acá.

---

## Decisiones pendientes de delamor

Las tres de v1, sin cambio. Ninguna bloquea los Pasos 1 y 2.

- **D2** — `node_presence` ponderada por masa / sin ponderar / las dos.
  *Recomendada: ponderada* (deriva 0.03 contra 0.19 sobre presupuesto ×100).
- **D3** — alcance: sólo Nivel A + D / A + B sin `core` / A + B + C después
  de la Parte 1 de la PROPUESTA. *Recomendada: A + D.*
- **D4** — nombres de las dos coercividades. *Puede quedar para cuando
  vayan juntas al paper.*

Nueva, y sí bloquea el Paso 2:

- **D5** — nombre del archivo de primitivas.

---

## Bloqueo explícito

- Field check que no da cero → revertir el paso y reportar. No ajustar el
  criterio.
- Si estandarizar una copia exige tocar `process/` o un testigo →
  **detener y reportar**.
- Si algún test existente falla y la única forma de pasarlo es modificar el
  test → **detener y reportar**.
- Si una diferencia parece deriva pero podría ser deliberada y no hay
  docstring que lo diga → **detener y preguntar**. No decidir por default.
- No encadenar pasos. Un paso, un field check, un reporte.

---

## REG

Uno por paso, o uno con una sección por paso — decisión de delamor. Debe
registrar, para cada paso: el censo antes, la clasificación de cada copia
(viva / testigo / deliberada), qué se estandarizó, el resultado del field
check, y qué quedó marcado como duplicado deliberado con su fecha de
colapso prevista.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: TASK_criterios_diversidad_services_v1.md (contexto, medida
canónica, alcance), TASK_monitor_service_unificar_rutinas_v1.md (precedente
de field check exacto), REG_orbitas_conjuntos_invariantes_v1.md,
CRITERIOS_diversidad_formulacion_v1.md*
