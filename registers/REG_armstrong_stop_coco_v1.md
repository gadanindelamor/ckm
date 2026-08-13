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
  "D_ckm_monitor": 0.0,
  "D_ckm_coco": 0.449,
  "fi": 0.0769,
  "zone": "deep",
  "temp_signal": {"signal": "TOO_COLD", "beta_collective": 13.0,
                   "beta_c_corpus": 1.3103, "ratio": 9.9211},
  "alpha_used": 0.2795918367346939,
  "Delta_r_before": 0.0,
  "Delta_r_after": 6.710204081632654
}
```

**Corrección — dos D_ckm distintos, no uno (observación de gadanin.delamor,
verificada contra el código):** el campo `D_ckm` de nivel superior del
panel (`panel["D_ckm"]`, calculado por `MonitorService._D_ckm()`) y
`panel["thermostat"]["D_ckm"]` (calculado internamente por
`COCO.observe()`) **no son la misma cantidad** — el primer intento de
este REG citaba el de `MonitorService` (0.0) como si fuera el que
disparó `zone="deep"`/`stop_applied=True`, lo cual es incorrecto: la
zona y el STOP dependen exclusivamente del `D_ckm` interno de `COCO`
(0.449, ya sobre el umbral 0.40).

Verificado línea por línea:

- `MonitorService._D_ckm()` (`monitor_service.py`): `self._A0` se fija
  la primera vez que se llama, usando `A(W + Δ_r)` **de esa misma
  llamada** — y `_D_ckm()` se invoca después de que los rechazos de esa
  misma evaluación ya se sumaron a `Δ_r`. Consecuencia estructural, no
  casual: en la primera evaluación, `A0 = A_actual` por construcción →
  `D_ckm = (A0-A_actual)/A0 = 0.0` siempre, sin importar el contenido
  del texto. Desde t=1 en adelante, `A0` queda fijo en ese primer
  snapshot y `D_ckm` sí se mueve (0.7037 estable desde t=1).
- `COCO.observe()` (`coco.py`): `self._A0` se fija la primera vez que
  se llama `observe()`, usando `A(self.W)` — **W puro, sin Δ, para
  siempre**. Como `COCO.observe()` recibe el `Δ_r` ya acumulado por la
  evaluación de `MonitorService` que lo llamó, su primer `D_ckm`
  compara ese `Δ_r` no-cero contra un piso sin Δ — de ahí que a t=0 ya
  sea 0.449, no 0.

Comparación completa de ambos D_ckm en las 20 evaluaciones:

| t | D_ckm (MonitorService) | D_ckm (COCO) | zone |
|---|---|---|---|
| 0 | 0.0000 | 0.4490 | deep |
| 1 | 0.7037 | 0.7959 | deep |
| 2 | 0.7037 | 0.6939 | deep |
| 3–19 | 0.7037 (fijo) | 0.4286 (fijo desde t=3) | deep |

Ambos convergen a valores estables distintos, ninguno vuelve a 0 pese a
que `Δ_r` decae geométricamente hacia ~0 hacia t=19 — consistente con
que cada `D_ckm` usa su propio `A0` congelado en su propio primer
llamado, no un piso compartido. **No afecta el resultado de este REG**
(el STOP lo dispara `COCO.observe()`, con su propio `D_ckm` correcto y
por encima de umbral en las 20 evaluaciones) — pero cualquier lectura
futura de la trayectoria (paper, próximo REG) debe citar
`panel["thermostat"]["D_ckm"]` como el `D_ckm` que gobierna
`zone`/`stop_applied`, no `panel["D_ckm"]`.

**Relación con R22** (`REG_reglas_no_declaradas_R18plus_v1.md`,
"δ_collective es divergencia fértil — no sincronizar"): R22 ya
documentaba que `monitor._Delta_r` y `thermostat._Delta` pueden
divergir como arrays. Esta observación es un nivel más: las métricas
**derivadas** de esos dos Δ (los dos D_ckm) también divergen, y no por
la misma razón — divergen porque cada una define su propio A0 desde un
punto de referencia distinto (uno con Δ incluido en el snapshot inicial,
el otro sin Δ para siempre), no solo porque los arrays Δ mismos difieran.

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
- `panel["D_ckm"]` (MonitorService) y `panel["thermostat"]["D_ckm"]`
  (COCO) son magnitudes distintas, con A0 definidos desde puntos de
  referencia distintos — corregido tras observación de gadanin.delamor
  (ver sección dedicada arriba). El D_ckm que gobierna `zone`/
  `stop_applied` es siempre el de COCO.

---

## Addendum — `landscape_delta` (TASK_coco_landscape_observation_v1, Extensiones 2 y 3)

Re-corrida idéntica del Intento 2 (mismo corpus, mismos textos, mismos
seeds — `Δ_r`/`D_ckm` reproducen exacto los valores ya reportados
arriba, confirmando determinismo) con `COCO(..., track_landscape=True)`
recién implementado. Mide `A`/`c(S)` del paisaje antes y después de
cada compresión — no solo la magnitud de `Δ_r`.

| t | A_antes | A_después | Δ_A | c(S)_antes | c(S)_después | Δ_c(S) | D_ckm_at_stop |
|---|---|---|---|---|---|---|---|
| 0 | 27 | 42 | **+15** | 0.1039 | 0.0662 | −0.0376 | 0.449 |
| 1 | 10 | 15 | **+5**  | 0.3037 | 0.0919 | −0.2118 | 0.7959 |
| 2 | 15 | 28 | **+13** | 0.0919 | 0.0622 | −0.0296 | 0.6939 |

**Δ_A positivo en los tres primeros triggers — atractores ganados, no
perdidos, verificado ahora a nivel de paisaje, no solo inferido de que
`Δ_r` decrece en magnitud.** Confirma cuantitativamente, con un
instrumento nuevo, lo mismo que `REG_destruccion_recuperacion_v1.md`
encontró por otro camino: OPERADOR_STOP_COCO restaura/expande, no
destruye. `D_ckm_at_stop` coincide exacto con los valores de COCO ya
reportados en este REG (0.449, 0.7959, 0.6939) — mismo cálculo, ahora
también expuesto junto al paisaje que lo produjo.

`c(S)` acá se computa sobre `W_eff` (`W+Δ`), no sobre `W` solo — mismo
plano que ya usa `_count_attractors()` internamente en `COCO`, distinto
del `c(S)` de `MonitorService` (que sí es W-exclusivo, R18). No es una
violación de R18: `self.W` nunca se muta, `W_eff` es una combinación
efímera local a la observación, igual que `A_current`.

Implementación: `services/coco.py` (`_mean_cS()`, `track_landscape` flag,
`_last_landscape_delta`, `alpha_trajectory()` con `delta_A` real) y
`services/monitor_service.py` (`panel["thermostat"]["landscape_delta"]`).
Extensión 1 del mismo task no se implementó — `panel["thermostat"]["D_ckm"]`
ya era el D_ckm de COCO (ver arriba), un campo `d_ckm_coco` nuevo habría
sido redundante.

---

## Réplica — seed=123, única variable cambiada

Pedida explícitamente por gadanin.delamor tras la Extensión 2, antes de
dar el "20/20" del Intento 2 por robusto. El pipeline completo (corpus,
`WARMUP_TEXTS`, `TEXTS`, `n_runs=50`, `track_landscape=True`) es
determinístico dado un seed — no hay forma de "correr de nuevo" y
obtener variación real sin cambiar algo. Única variable cambiada:
`seed` de `COCO` (42 → 123). Todo lo demás, idéntico al Intento 2.
Script: `armstrong_replica_seed123.py` (scratchpad), output:
`process/experiments/armstrong_replica_seed123*`.

### Resultado: 3/20 STOPs, no 20/20

| t | D_ckm (COCO) | zone | stop | alpha_used |
|---|---|---|---|---|
| 0 | 0.4898 | deep | True | 0.2626 |
| 1 | 0.8163 | deep | True | 0.1265 |
| 2 | 0.6735 | deep | True | 0.1861 |
| 3–19 | 0.3673 (fijo) | stable | False | — |

Comparación directa con el Intento 2 (`seed=42`):

| | seed=42 (Intento 2) | seed=123 (réplica) |
|---|---|---|
| STOPs | 20/20 | **3/20** |
| D_ckm de convergencia (t≥3) | 0.4286 (**arriba** de 0.40) | 0.3673 (**abajo** de 0.40) |
| alpha_used, t=0–2 | 0.2796, 0.1350, 0.1776 | 0.2626, 0.1265, 0.1861 — mismo rango |
| Δ_A, t=0–2 | +15, +5, +13 | +18, +7, +15 — mismo signo |

### Lectura — qué replica, qué no, y por qué cada uno es el resultado correcto

**Replica (mecanismo robusto):** en las tres primeras evaluaciones de
ambas semillas, `alpha_used` cae dentro de `[0.05, 0.30]` y `Δ_A` es
positivo — STOP, cuando dispara, comprime dentro del rango declarado y
gana atractores, no los pierde. Esto no depende del seed. Es el
hallazgo central de la Extensión 2, confirmado independientemente.

**No replica (y no debería):** el conteo "20/20" del Intento 2 no es
una propiedad robusta del mecanismo — es dónde cayó, para ese seed
específico, el `D_ckm` de convergencia respecto al umbral fijo 0.40.
`D_ckm` es una **estimación** sobre `n_runs=50` muestras estocásticas
de `_count_attractors()`, no un valor analítico exacto. Con `seed=42`
esa estimación convergió a 0.4286 (arriba del umbral → sigue
disparando indefinidamente). Con `seed=123` convergió a 0.3673 (abajo
→ se estabiliza y para en t=3). Ambos valores están a menos de 0.033
del umbral — el sistema converge cerca del borde en las dos semillas,
y el ruido de muestreo decide de qué lado cae.

**Por qué esto es información estructural, no un defecto:** un umbral
fijo (0.40) comparado contra una estimación ruidosa produce
exactamente este comportamiento — sensibilidad binaria (sigue/para)
ante una cantidad continua con varianza. El 20/20 original no estaba
mal — era el resultado correcto para `seed=42`. El 3/20 tampoco está
mal — es el resultado correcto para `seed=123`. Lo que no se sostiene
es la generalización "COCO regula indefinidamente sobre este corpus" —
eso era artefacto de una semilla particular, no propiedad del
mecanismo. `n_runs=50` puede ser insuficiente para una estimación
estable cerca del umbral — línea abierta, no resuelta acá.

---

## Archivos relacionados

- `iap_chatroom/tests/TASK_armstrong_stop_coco_v1.md` — especificación
- `iap_chatroom/tests/TASK_coco_landscape_observation_v1.md` — especificación del addendum (Ext. 2/3)
- `iap_chatroom/tests/test_armstrong_stop_coco.py` — script (TEXTS
  rediseñados respecto al original del task, ver Intento 1/2 arriba;
  `track_landscape=True` desde el addendum)
- `process/experiments/armstrong_stop_coco_v1.jsonl` — trayectoria completa, incluye `landscape_delta` (seed=42)
- `process/experiments/armstrong_replica_seed123.jsonl` — trayectoria completa de la réplica (seed=123)
- `process/experiments/armstrong_replica_seed123_summary.json` — resumen de los 3 STOPs de la réplica
- `process/experiments/armstrong_delta_r_history.json` — historial Δ_r (seed=42)
- `process/experiments/armstrong_*.bak_*_null_result_v1` — intento 1 preservado, no descartado
- `process/experiments/armstrong_*.bak_*_pre_ext2` — estado previo al addendum de Ext. 2, preservado
- `registers/REG_monitor_ckm_v2.md` — origen del "problema del chocolate"
- `registers/REG_sesion_coco_endogeno_v2.md` — ponderación endógena de α, origen de esta tarea
- `registers/REG_destruccion_recuperacion_v1.md` — definición real de Fracción_rec

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
