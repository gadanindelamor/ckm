# TASK_monitor_service_unificar_rutinas_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Origen: desajuste identificado por delamor en REG_wmixta_consolidado_v1 —
la condición `sin_thermostat` ejecuta rutinas propias de MonitorService,
con distribución uniforme hardcodeada.*

---

## Contexto — las cuatro divergencias, ya medidas

`MonitorService` y `COCO` tienen implementaciones **separadas** de `_relax`
y `_count_attractors`. Difieren en cuatro cosas:

| | MonitorService | COCO |
|---|---|---|
| `_relax` `max_iter` | 100 (`monitor_service.py:209`) | 200 (`coco.py:538`) |
| seed del conteo | **`default_rng(0)` hardcodeado** | `self._seed`, configurable |
| distribución de σ₀ | **uniforme hardcodeada**, sin parámetro | uniform / weighted / boltzmann |
| W sobre la que cuenta | `_combine_W_Delta(W, Δ_r)` | `W + Δ_r` crudo |

El cuerpo de `_relax` es, por lo demás, **idéntico byte a byte**. El cuerpo
del loop de conteo también, salvo el muestreo de σ₀.

**Consecuencia registrada:** la fila `sin_thermostat` de los REGs de wmixta
no es "el mismo instrumento sin regulación" — es otro instrumento sobre
otro paisaje.

---

## Evaluación de impacto — ya ejecutada, no repetir

Corpus: 24 textos de `caso09_run2`, régimen natural, `n_runs=50`.
Se midió, por evaluación, cuántas cambian respecto de `MonitorService` tal
como está hoy:

| variante | D_ckm | c_S | rechazos | σ_relajado | Δ_r final |
|---|---:|---:|---:|---:|---:|
| V1 — `_relax` `max_iter` 100→200 | **0** | **0** | **0** | **0** | 632 → **632** |
| V2 — V1 + conteo `seed` 0→42 | 23 | 0 | 0 | 0 | 632 → **632** |
| V3 — V2 + W cruda (sin `_combine_W_Delta`) | 23 | 18 | 16 | 20 | 632 → **212** |

Y la equivalencia exacta, misma W, `n_runs=50`:

| W_eff | `MonitorService._count_attractors` | `COCO(seed=0)._count_attractors` |
|---|---:|---:|
| W sola | 33 | **33** |
| `_combine_W_Delta(W, D)` | 24 | **24** |
| `W + D` crudo | 27 | **27** |

`_relax`: **0 de 200** estados finales distintos entre `max_iter` 100 y 200.

**Conclusión de la evaluación: el reemplazo mínimo tiene impacto CERO
exacto**, siempre que MonitorService conserve `seed=0` y modo `uniform`
como defaults. No es impacto pequeño — es ningún número que cambie.

---

## Objetivo

Unificar: que `MonitorService` use **exactamente** las rutinas de COCO,
sin duplicación, preservando su comportamiento numérico actual.

---

## Paso 0 — verificar antes de tocar

- `services/monitor_service.py` — los tres sitios de llamada reales:
  `evaluate()` (línea ~108, produce `sigma_relaxed`), `_D_ckm()` (~268-269),
  y `_count_attractors()` (~284). Las líneas 10 y 30 están **dentro del
  docstring** — no son código.
- `services/coco.py` — `_relax`, `_count_attractors`, `_sample_s0`,
  `_node_probs`, `_boltzmann_warmup`. Notar que `_sample_s0` usa `self.N`.
- `tests/test_monitor_services.py` — qué asume sobre estos métodos.
- Quién más llama a estos privados fuera de los dos servicios.

Reportar y esperar instrucción sobre la opción de diseño (abajo).

---

## Alcance — qué entra y qué NO

**Entra:**
- `_relax` de MonitorService pasa a ser el de COCO (`max_iter=200`).
- `_count_attractors` de MonitorService pasa a ser el de COCO, con
  `seed` y `sampling_mode` **configurables** y defaults que preservan el
  comportamiento actual: `seed=0`, `sampling_mode="uniform"`.
- El modo queda expuesto en el panel, igual que ya lo está el del thermostat.

**Contrato de firmas (decisión de delamor, Sep 2026):**

MonitorService **conserva `seed=0` y modo `uniform` como sus defaults**.
Todo parámetro que la rutina de COCO tenga y la de MonitorService no debe
ser **opcional o con default**, de modo que los sitios de llamada actuales
—que pasan sólo `W`— sigan funcionando sin cambio.

Verificado en el repo: las firmas de COCO **ya cumplen** esto —
`weighted=False`, `boltzmann=False`, `n_warmup=None` (`coco.py:664-670`)— y
ningún sitio de llamada del repo pasa posicionales más allá de `W`. No hay
que agregar defaults: hay que no romperlos.

Único punto a decidir explícitamente: **`max_iter`** no es un parámetro
adicional sino el mismo con otro default — 100 en MonitorService
(`:209`), 200 en COCO (`:538`). Ninguna llamada lo pasa, así que al
unificar MonitorService hereda 200. Medido: **0 de 200** estados finales
distintos. Se adopta 200.

**NO entra — explícitamente fuera de alcance:**
- **Quitar o cambiar `_combine_W_Delta`.** Es la divergencia grande (V3:
  toca `sigma_relaxed` en 20 de 24 evaluaciones, Δ_r final 632 → 212). No
  es "unificar rutinas": cambia qué rechaza el instrumento. Decisión aparte.
- Cambiar `n_runs_attractors` (50) ni el `n_runs` de COCO (80).
- `ALPHA_MIN`, `ALPHA_MAX`, `D_CKM_THRESHOLD`.
- La lógica de `OPERADOR_STOP_COCO`.
- REGs históricos, nada en `process/iap/`.

---

## Opciones de diseño — decidir antes de implementar

**A — Extraer a módulo compartido** (`services/hopfield_sampling.py` o
similar): `relax`, `sample_s0`, `node_probs`, `boltzmann_warmup`,
`count_attractors` como funciones puras sobre `(W, N, rng, ...)`. COCO y
MonitorService importan de ahí.
*A favor:* elimina la duplicación de raíz, una sola implementación
canónica, testeable por separado.
*En contra:* **modifica `coco.py`**, que varias TASKs previas marcaron como
no modificable. Requiere autorización explícita.

**B — MonitorService delega en COCO sin tocar `coco.py`**: instancia un
`COCO(W=W_eff, n_runs=self._n_runs, seed=..., sampling_mode=...)` y llama a
sus métodos. El constructor de COCO es barato (valida W, fija N, no
computa).
*A favor:* `coco.py` intacto; cero duplicación de la lógica de conteo.
*En contra:* MonitorService pasa a depender de COCO estructuralmente —
instancia un regulador para usar su contador. Conceptualmente raro, y COCO
ya no sería opcional en el sentido en que lo es hoy.

**C — Copiar el código de COCO dentro de MonitorService.**
*A favor:* trivial, sin dependencias nuevas.
*En contra:* la duplicación persiste, ahora con tres copias de la fórmula
contando `experiments/`. Es el patrón que ya produjo este desajuste.

**Recomendación: A**, con autorización explícita para tocar `coco.py`. Es
la única que cierra el problema en vez de moverlo. Si `coco.py` no se
puede tocar, **B**; **C** solo si se descartan las dos.

---

## Criterio de éxito

1. `tests/test_monitor_services.py` → 35/35 sin cambios en el archivo de tests.
2. `tests/test_coco.py` → 28/28. `python services/coco.py` → T1-T13 OK.
3. **Regresión numérica exacta**: replay de los 24 textos de `caso09_run2`
   (régimen natural, `n_runs_attractors=50`) produce paneles **idénticos**
   a los actuales — `D_ckm`, `c_S`, `n_rejected_pairs`, `activos_relajado`,
   `Delta_r_sum`, en las 24 evaluaciones. Cero diferencias, no "diferencias
   chicas".
4. `MonitorService` acepta `sampling_mode` y lo reporta en el panel.
5. Verificar que con `sampling_mode="weighted"` o `"boltzmann"` el conteo
   **sí** cambia — que el parámetro esté realmente conectado y no sea
   decorativo.

---

## REG

`registers/REG_monitor_service_unificar_rutinas_v1.md` — generar tras
verificar el criterio 3, no antes. Debe registrar:
- las cuatro divergencias originales y su medición,
- qué opción de diseño se tomó y por qué,
- la verificación de regresión exacta,
- que `_combine_W_Delta` quedó **sin tocar** y sigue siendo la divergencia
  abierta entre los dos instrumentos.

---

## Bloqueo explícito

Si preservar el comportamiento numérico actual resulta imposible sin tocar
`_combine_W_Delta`, o si algún test existente falla y la única forma de
pasarlo es modificar el test — **detener y reportar**. No encadenar cambios.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: REG_wmixta_consolidado_v1.md, REG_wmixta_natural_paso2_v1.md,
REG_wmixta_forzado_paso3_v1.md*
