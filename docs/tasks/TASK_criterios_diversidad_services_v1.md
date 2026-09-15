# TASK_criterios_diversidad_services_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Origen: `docs/PROPUESTA_capa_analisis_services_v1.md` Parte 2 (tres niveles),
`docs/CRITERIOS_diversidad_formulacion_v1.md` (formulación conceptual y
especificación técnica), `registers/REG_orbitas_conjuntos_invariantes_v1.md`
(verdad de terreno por enumeración 2^20).*

---

## Contexto — lo ya medido, no repetir

Todo lo que sigue está verificado y no es parte de esta TASK:

- Contar **estados terminales** no estima el número de órbitas. `|L/~| ≤
  terminales ≤ |L|`. Detener en un tope fijo devuelve una **fase** de la
  órbita; dos trayectorias que llegan a la misma órbita por colas de
  distinta paridad se cuentan como dos.
- Los **conteos no convergen** con el presupuesto de muestreo; las **masas
  sí**. Contra enumeración exhaustiva de 2^20: con 100.000 muestras el
  conteo de órbitas erra hasta 28% mientras la masa agregada del top-10
  erra 0.0%.
- `N_eff = 1/Σ m_o²` se comporta como un conteo y converge como una masa.
  Errores contra verdad exacta: 0.3% / 0.6% / 0.0% en tres corpus.
- Cambiar **sólo** la distribución de σ₀ mueve el número de órbitas
  halladas por un factor de **8×** — mismo campo, mismo presupuesto.
- El índice de frustración es **invariante** a amplificar los pesos
  negativos ×16 (0.0258 en todo el rango) mientras `frac_neg` va de 0.031
  a 0.338 y `λ_min` de −0.069 a −0.422. Topológico vs métrico son
  dimensiones independientes.
- Exactitud: los empates (`h=0`) son exactos si y sólo si los pesos lo son.
  Con `max|raw|` no potencia de dos, hasta 46% de los pasos cambian de
  sucesor según cómo se escriba el producto (`W @ s` vs `s @ W`).

Verdad de terreno disponible para contrastar: **1136 / 573 / 170** órbitas
exactas en tres corpus de N=20 (`experiments/orbit_analytics.py`,
sección D).

---

## Definición ya tomada por delamor — medida de referencia canónica

**La canónica es la primera en el orden cronológico del proyecto.**
Verificado: `analytics.py`, commit `c864f53`, 2026-05-11 — anterior a
`services/` (`6d563fd`, 2026-05-28).

```python
def cs_at_rho(W, rho):
    n_active = max(1, int(rho * N))
    active   = np.random.choice(N, n_active, replace=False)
    sigma    = np.full(N, -1.0);  sigma[active] = 1.0
```

Uniforme sobre **cuáles** nodos están activos, con **ρ fijo como
parámetro**. No es una medida: es una **familia indexada por ρ** —
uniforme sobre el conjunto de nivel `{σ : #(σ_i=+1) = ⌈ρN⌉}`.

Consecuencias de diseño, no negociables:

1. `rho` es **parámetro explícito** de la rutina de muestreo. No se sortea.
2. Las salidas son **curvas sobre ρ**, `m_o(ρ)`, no escalares.
3. Las otras dos medidas conocidas son **pesos sobre ρ** de esta misma
   familia, no samplers distintos:

   | medida | en términos de la canónica |
   |---|---|
   | canónica | uniforme en el nivel ρ, con ρ declarado |
   | banda de `services/` (`_count_attractors` actual) | mezcla sobre ρ ~ U(0.3, 0.7) |
   | uniforme en el hipercubo | mezcla sobre ρ ~ Binomial(N, ½)/2^N |

   Se implementan como ponderaciones, no como código nuevo de muestreo.

4. ρ es la misma coordenada donde ya viven P1/P4 y el lazo de histéresis —
   la coercividad P1 es un intervalo sobre ρ ([0.406, 0.586]). Los
   criterios de diversidad quedan en esa coordenada, no en una paralela.

---

## Objetivo

Una capa de análisis en `services/` que calcule los criterios de
diversidad sobre una W dada, **aditiva y con impacto cero por default**.

---

## Paso 0 — verificar antes de tocar, y reportar

- `services/coco.py:538` `_relax_orbit`, `:700` `_sample_s0`, `:602`
  `_node_probs`, `:660` `_boltzmann_warmup`, `:717` `_count_attractors`.
- `services/monitor_service.py:213` `_relax_orbit`, `:382`
  `_count_attractors` — copias unificadas con COCO (`5f2ec6c`), mismo hash
  normalizado.
- `experiments/orbit_analytics.py:139` `relax_orbit`, `:159` `sigma0`,
  `:173` `muestrear`, `:187` `n_eff`, `:193` `enumerar_exhaustivo`.
- `analytics.py` de raíz: `copresence_matrix`, `cluster_nodes`,
  `attractor_stats` — **no importable hoy** (imports relativos sin
  `__init__.py`), depende de `core.py`.

**Reportar antes de escribir código:** cuántas copias de la primitiva de
órbita hay ya en el repo, y cuál sería la cuenta después de esta TASK
según la opción de diseño que se elija. Es el punto exacto del patrón que
esta sesión midió (7 definiciones de `_relax`, 4 variantes).

---

## Alcance

**Entra:**
- Muestreo canónico `sigma0_nivel(rng, N, rho)` — uniforme sobre cuáles
  nodos activos, ρ explícito.
- Barrido sobre ρ que devuelve, por cada ρ: órbitas halladas, masas
  ordenadas `m_o(ρ)`, `N_eff(ρ)`, `T_k(ρ)`.
- `N_eff` y masa agregada top-k. **Agregado, no máximo individual** — el
  máximo estimado tiene sesgo hacia arriba (26.5% de error contra 16.0%
  del top-10, mismo muestreo).
- Cantidades de W sola, sin muestrear: índice de frustración, `frac_neg`,
  espectro, CV de frecuencias marginales.
- Diagnósticos de exactitud: valores distintos, diádico sí/no, fracción de
  empates, fracción frágil al reescribir el producto.
- Las dos ponderaciones derivadas (banda y hipercubo) como reponderación
  del barrido, no como samplers nuevos.

**NO entra — explícitamente fuera de alcance:**
- **Tocar `_count_attractors`** de COCO o de MonitorService, ni sus
  defaults, ni el panel. Nada del runtime cambia de valor.
- **El gatekeeper y `CKMConfig`.** C1/C2 degeneran sobre
  `W_ckm_corpus_v2` en direcciones opuestas — es decisión de modelo.
- Mover `analytics.py` o `core.py` a `services/`. Depende de decisiones
  abiertas de la Parte 1 de la PROPUESTA (Hebbianos, nombre
  `CKMGraphArrays`, destino de `core.py` de raíz).
- La enumeración exhaustiva 2^N como servicio operativo. Es instrumento de
  verificación; se queda en `experiments/`.
- Unificar los tres niveles en un índice único. La PROPUESTA Parte 6 no lo
  propone y la medición cruzada no se hizo.

---

## Decisiones pendientes de delamor — bloquean la implementación

**D2 — `node_presence` (Nivel B).**
- (a) Ponderada por masa: `p_i = Σ_o m_o · frac_activo(o,i)`. Deriva 0.03
  contra 0.19 sin ponderar, sobre presupuesto ×100. **Recomendada.**
- (b) Sin ponderar, como `analytics.py` hoy — hereda el sesgo de conteo.
- (c) Las dos, campos distintos; la divergencia queda medible por corrida.

**D3 — Alcance de esta implementación.**
- (a) Solo Nivel A (órbitas, masas, `N_eff`, top-k) más Nivel D (W sola).
  Cero dependencias nuevas, cero decisiones abiertas. **Recomendada.**
- (b) A + B reimplementando co-presencia sin `core` — deja una copia más
  de esas rutinas en el repo.
- (c) A + B + C después de definir la Parte 1 de la PROPUESTA.

**D4 — Nombres de las dos coercividades** (§Parte 3 de la PROPUESTA: hoy
son dos cantidades distintas con el mismo nombre).
- (a) `coercividad_histeresis` / `coercividad_frontera`
- (b) `coercividad_P1` / `coercividad_cluster`
- (c) Sin tocar en esta TASK — entra cuando vayan juntas al paper.

---

## Opciones de diseño — dónde vive la primitiva de órbita

La primitiva ya existe **tres veces**: `coco.py`, `monitor_service.py`,
`orbit_analytics.py`. Escribirla de nuevo la haría cuarta.

**A — El módulo nuevo importa de `coco`.** `from coco import COCO` y usa
`_relax_orbit` vía una instancia, o se expone la función a nivel de módulo
sin tocar la clase.
*A favor:* cero copias nuevas, `coco.py` intacto en su lógica.
*En contra:* la capa de análisis pasa a depender del regulador.

**B — Extraer a `services/hopfield_sampling.py`** como funciones puras
sobre `(W, N, rng, ...)`; COCO, MonitorService y la capa nueva importan de
ahí. Baja de tres copias a una.
*A favor:* cierra el problema en vez de moverlo.
*En contra:* **modifica `coco.py` y `monitor_service.py`**. Requiere
autorización explícita y una regresión numérica exacta como la de
`TASK_monitor_service_unificar_rutinas_v1`.

**C — Copiar.** Cuarta copia. Es el patrón medido.

**Recomendación: A** para esta TASK, y **B** como TASK propia y posterior,
con su propio criterio de regresión exacta. No mezclar las dos.

---

## Criterio de éxito

1. Los tres corpus de N=20 de `orbit_analytics.py` reproducen su verdad de
   terreno: **1136 / 573 / 170** órbitas exactas por enumeración, y el
   barrido canónico las recupera con el error esperado por presupuesto.
2. `N_eff` converge donde el conteo no: repetir con presupuesto ×100 y
   verificar que `N_eff` deriva menos de 1% mientras el conteo de órbitas
   crece.
3. **Impacto cero exacto en runtime**: `tests/test_coco.py` 28/28,
   `tests/test_monitor_services.py` 35/35, `python services/coco.py`
   T1-T13 OK, `python services/monitor_service.py` T1-T6 OK, sin
   modificar ningún archivo de tests.
4. Las tres medidas coinciden por construcción: reponderar el barrido
   canónico con pesos de banda debe dar, dentro del error de muestreo, lo
   mismo que muestrear con `rho = rng.uniform(0.3, 0.7)`. Si no coinciden,
   la implementación de la familia está mal.
5. El diagnóstico de exactitud reporta `frágil > 0` en los corpus donde
   `max|raw|` no es potencia de dos, y `0` donde sí. Verificado ya: 33
   órbitas en los dos casos, **18 de 33 distintas**.
6. La orientación queda declarada: `N_eff` sube con la diversidad, `T_k`
   baja. Ningún índice mezcla los dos signos sin decirlo.

---

## REG

`registers/REG_criterios_diversidad_services_v1.md` — generar tras
verificar los criterios 1 a 4, no antes. Debe registrar la medida canónica
adoptada y su origen cronológico, qué opción de diseño se tomó y cuántas
copias de la primitiva quedaron, y qué quedó fuera de alcance con su
motivo.

---

## Bloqueo explícito

- Si cumplir el criterio 3 exige tocar `_count_attractors`, sus defaults o
  el panel — **detener y reportar**.
- Si algún test existente falla y la única forma de pasarlo es modificar
  el test — **detener y reportar**.
- Si las decisiones D2/D3/D4 no están tomadas — implementar sólo lo que no
  dependa de ellas y reportar qué quedó sin hacer. No elegir por default.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: PROPUESTA_capa_analisis_services_v1.md (Partes 2, 3, 5, 6),
CRITERIOS_diversidad_formulacion_v1.md, REG_orbitas_conjuntos_invariantes_v1.md*
