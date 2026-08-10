# REG_armstrong_stop_coco_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Primera observación in-vivo de OPERADOR_STOP_COCO en el pipeline real
`MonitorService.evaluate() → COCO.observe(Δ_r) → compresión → MonitorService
adopta Δ_r comprimido`. Verificado hasta ahora solo en tests unitarios
(coco.py T1-T13) y en experimentos standalone (sweep_stop_perdida) —
nunca con `MonitorService` construyendo Δ_r orgánicamente desde texto real
y un `COCO` real reaccionando a eso en el mismo proceso.

Especificación: `iap_chatroom/tests/TASK_armstrong_stop_coco_v1.md`.
Script: `iap_chatroom/tests/test_armstrong_stop_coco.py`.

Precondición: R1+R2 de `TASK_refactoring_coco_device_v1.md` ya aplicados
(`COCO`, `evaluate(device_id=...)`) — el script usa la API post-refactoring
directamente.

---

## Intento 1 — resultado nulo, causa raíz identificada (no fue bug)

El diseño original de la tarea usaba 20 textos de vocabulario técnico
totalmente ajeno al corpus CKM (redes neuronales, blockchain, política
monetaria, fotosíntesis...) bajo la hipótesis: *"vocabulario ajeno →
alta fi → muchos rechazos → Δ_r crece rápido"*.

**Resultado: STOP no disparó ni una sola vez en 20/20 evaluaciones.**
`D_ckm` se mantuvo en `0.0000` durante todo el run. `Δ_r` nunca superó 0.

**Causa raíz, verificada contra el código, no asumida:**

`fabrication_index` (`_fabrication_index()`, `monitor_service.py`) mide
la fracción de **nodos** declarados activos que la relajación rechazó —
`declared==0 → fi=0.0` por guarda explícita; con exactamente 1 nodo
activo, ese único nodo puede saturar a `fi=1.0` de forma vacía.

`Δ_r` (`_rejected_pairs()`) solo acumula **pares** de nodos co-activos
que la relajación separó — requiere ≥2 nodos activos simultáneos para
que exista siquiera un par candidato a rechazo.

Verificado contra el crudo (`activos_prompt` de cada evaluación,
`process/experiments/armstrong_corpus_state.json.bak_*_null_result_v1`):
**máximo 1 nodo activo por texto en las 20 evaluaciones.** Vocabulario
completamente ajeno al corpus de precarga (N=20 nodos, extraídos de 20
oraciones cortas sobre CKM) activa como mucho un token aislado — nunca
dos simultáneos. `fi` osciló (promedio 0.25, picos en 1.0), pero `Δ_r`
se mantuvo exactamente en 0 en las 20 evaluaciones porque nunca existió
un par que rechazar.

**Esto reproduce, con datos nuevos, el "problema del chocolate" ya
documentado en `REG_monitor_ckm_v2.md`:** *"El campo no puede rechazar
lo que no conoce. Es una propiedad del sistema, no una falla."* Textos
sin ningún anclaje al vocabulario del corpus no se detectan como
fabricados — pasan invisibles, no rechazados.

**Consecuencia para el fallback del propio task** ("si STOP no dispara,
agregar 10 textos más, misma estrategia de vocabulario ajeno"): esa
estrategia no puede funcionar — agregar más texto igualmente ajeno
solo repite el mismo resultado nulo, porque el mecanismo que falla
(0-1 nodos activos, nunca un par) es estructural al diseño de los
textos, no una cuestión de volumen. Reportado a gadanin.delamor antes
de seguir; decisión explícita: rediseñar los textos en vez de seguir
el fallback literal.

---

## Intento 2 — textos rediseñados, condición Armstrong confirmada

**Estrategia corregida:** en vez de vocabulario ajeno, reusar los 20
nodos reales extraídos del corpus de precarga (`CorpusService.get_nodes()`,
verificado antes de escribir los textos): `d_ckm`, `attractor`, `all`,
`delta_r`, `matrix`, `over`, `measures`, `about dependencies`, `applies`,
`delta`, `matrix encoding`, `encoding`, `device`, `coco`, `operates`,
`structural`, `sha`, `times`, `summable`, `cases` — combinados en
oraciones nuevas que cruzan nodos de oraciones de precarga distintas y
no relacionadas (p. ej. `coco` viene de la oración sobre COCO-ODA, `sha`
de la oración sobre FirmaService, `attractor` de la de Hopfield — nunca
co-ocurrieron en los 20 textos originales). W es W_pos pura (sin pares
negativos — ninguno de los 20 textos de precarga tiene marcadores de
oposición), así que cualquier par nuevo entre nodos reales sin soporte
previo en W es candidato genuino a rechazo en la relajación.

**Resultado — condición Armstrong confirmada, 20/20:**

| Criterio (TASK_armstrong_stop_coco_v1.md) | Resultado |
|---|---|
| `stop_applied = True` al menos una vez | ✅ — 20/20 evaluaciones |
| `Δ_r_after < Δ_r_before` (compresión confirmada) | ✅ — desde t=2 en adelante, geométrico puro por α (ver tabla) |
| `alpha_used ∈ [0.05, 0.30]` | ✅ — todos los valores dentro del rango declarado (`ALPHA_MIN=0.05`, `ALPHA_MAX=0.30`) |

**Primer ARMSTRONG (t=0):**
```json
{
  "t": 0,
  "text_preview": "Coco applies sha over all structural cases, summable times a",
  "D_ckm": 0.0,
  "fi": 0.0769,
  "zone": "deep",
  "temp_signal": {"signal": "TOO_COLD", "beta_collective": 13.0,
                   "beta_c_corpus": 1.3103, "ratio": 9.9211},
  "alpha_used": 0.2795918367346939,
  "Delta_r_before": 0.0,
  "Delta_r_after": 6.710204081632654
}
```

**Trayectoria completa de Δ_r** (`process/experiments/armstrong_delta_r_history.json`):

| t | Δ_r antes | Δ_r después | mecanismo |
|---|---|---|---|
| 0 | 0.0000 | 6.7102 | acumulación neta (nuevos rechazos > compresión) |
| 1 | 6.7102 | 13.0592 | acumulación neta |
| 2 | 13.0592 | 2.3187 | **compresión neta** — primera vez que α domina |
| 3 | 2.3187 | 0.6680 | compresión neta |
| 4 | 0.6680 | 0.1924 | compresión neta |
| 5–19 | — | — | decaimiento geométrico puro por α=0.2881/paso (sin nuevos rechazos) |

De t=4 en adelante, `Δ_r_after / Δ_r_before = 0.28809...` en cada paso,
exactamente `alpha_used` — confirma que, agotados los pares nuevos
rechazables, `COCO` sigue comprimiendo lo que ya había puramente por
`Δ → α·Δ`, sin más entrada.

---

## Nota — `compression_ratio` del script ≠ `Fracción_rec` de `REG_destruccion_recuperacion_v1`

El script de la tarea (sección "TEXTO COMPLETO... modo debug" e
impresión final) llama `compression_ratio = Δ_r_after / Δ_r_before` y
la etiqueta como *"Fracción_rec (debería ser ≥ 1.0 por
REG_destruccion_recuperacion_v1)"*. **Esto no es la misma magnitud.**

`REG_destruccion_recuperacion_v1.md` define `Fracción_rec(t) =
max_α[A_post(α)] / A0` — un cociente de **conteo de atractores** bajo
barrido de múltiples α, tomando el mejor. El script de este experimento
mide `Δ_r_after / Δ_r_before` bajo un único α dinámico — un cociente de
**magnitud del acumulador de rechazos**, no de atractores. Por
construcción (`α < 1` casi siempre que hay compresión), este segundo
cociente tiende a ser `< 1.0`, no `≥ 1.0` — lo opuesto de lo que el
criterio original esperaba si se tratara de la misma cantidad.

No se afirma "Fracción_rec ≥ 1.0 confirmado" en este REG porque no es
lo que se midió. Lo que sí está confirmado, con datos reales: `Δ_r`
comprime geométricamente por el `α` que `COCO` calculó dinámicamente,
consistente con `_alpha_for()` y con el hallazgo de
`REG_sesion_coco_endogeno_v2.md` (ponderación endógena — `α` no es fijo,
depende de `D_ckm`, que depende del estado estructural real del campo).

---

## Hallazgo secundario — TOO_COLD sostenido

`temp_signal` reporta `TOO_COLD` (β_collective ≫ β_c_corpus) desde el
primer trigger en adelante — `beta_collective` sube a 13.0 tras la
primera evaluación (un solo `device_id` distinto por texto, cada uno
con una sola medición de `fi`; con `fi` bajo, `β_i = 1/fi` se dispara
alto). Consistente con el diseño del experimento (20 `device_id`
distintos, uno por texto, cada uno visto una sola vez) — no es un
hallazgo sobre el campo real, es artefacto de que este experimento no
repite evaluaciones por el mismo device. No investigado más — fuera
del objetivo de esta tarea (aislar OPERADOR_STOP_COCO, no calibrar
TEMP_SIGNAL bajo carga real).

---

## Estado

- Condición Armstrong: **confirmada** — `stop_applied=True`, compresión
  real verificada (t=2 a t=19), `alpha_used` dentro de rango en las 20
  evaluaciones.
- Circuito completo `MonitorService.evaluate() → COCO.observe() →
  compresión → MonitorService adopta Δ_r` — observado en vivo por
  primera vez, no solo en tests unitarios ni en sweeps standalone.
- n=1 diseño — no confirmar como patrón robusto sin réplica.
- El diseño original del task (vocabulario ajeno) queda documentado
  como enfoque que no puede funcionar por el mecanismo fi≠Δ_r — no se
  reintentó tal cual, se corrigió antes de re-correr.
- `compression_ratio` del script y `Fracción_rec` de
  `REG_destruccion_recuperacion_v1` son magnitudes distintas — no
  equivalentes, aclarado arriba.

---

## Archivos relacionados

- `iap_chatroom/tests/TASK_armstrong_stop_coco_v1.md` — especificación
- `iap_chatroom/tests/test_armstrong_stop_coco.py` — script (TEXTS
  rediseñados respecto al original del task, ver Intento 1/2 arriba)
- `process/experiments/armstrong_stop_coco_v1.jsonl` — trayectoria completa (intento 2)
- `process/experiments/armstrong_delta_r_history.json` — historial Δ_r (intento 2)
- `process/experiments/armstrong_*.bak_*_null_result_v1` — intento 1 preservado, no descartado
- `registers/REG_monitor_ckm_v2.md` — origen del "problema del chocolate"
- `registers/REG_sesion_coco_endogeno_v2.md` — ponderación endógena de α, origen de esta tarea
- `registers/REG_destruccion_recuperacion_v1.md` — definición real de Fracción_rec

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
