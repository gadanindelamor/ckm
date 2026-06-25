# REG_term_map_core_surgery_v1.md
*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Lo que se estableció en esta sesión

### 1. term_map nunca fue construido

`term_map` aparece en `core.py`, `API_SPEC.md`, `README.md`, y en hints de
sesiones anteriores como un gap pendiente de "reconstrucción".

Establecido con precisión: no es un gap de memoria. No es pérdida.
`term_map` **nunca existió como proceso del proyecto**. Nunca hubo
participación de gadanin.delamor en su construcción. Las referencias
a "reconstruir term_map" son huellas de sesiones anteriores operando
sobre un supuesto que no tenía base real.

### 2. from_corpus() no tiene llamadores

`from_corpus()` con `term_map` obligatorio es una interfaz sin uso real
en la base de código actual. Los escenarios efectivos de construcción de W:

| Escenario | Camino | term_map |
|---|---|---|
| `mcp_adapter` | `_build_dependency_W()` desde `Capability.dependencies` | No |
| Scripts experimentales | `from_json()` carga W_ckm_corpus_v2.json | No |
| `from_corpus()` | requería term_map | Sí — **nadie la llama** |

### 3. El camino ya existía: NodeExtractorService

`node_extractor.py` — `accumulate(texts)` — produce nodos y co-ocurrencias
via TF-IDF, sin LLM, sin estado, sin construcción manual. Es el mecanismo
generativo que hace obsoleto el term_map como precondición.

Nadie conectó los dos. No fue un olvido de ninguna instancia particular.
`term_map` actuaba como precondición implícita que bloqueaba ver que
`accumulate()` ya era la solución.

### 4. Cirugía realizada: core.py

`from_corpus()` modificado. `term_map` ahora es `Optional`, `None` por defecto.

**Path A** — `term_map` explícito: comportamiento anterior intacto.
**Path B** — `term_map=None`: `NodeExtractorService.accumulate()` construye
nodos y cooc automáticamente. `nodes` override opcional. `top_k=20` controlable.

Import de `NodeExtractorService` lazy dentro del método.
`from_json()` y todo lo demás: sin tocar.

Archivo producido: `core.py` — pendiente de commit.

---

## Corrección: estado real de P4

P4 está **confirmada**. Experimentos realizados sobre W_ckm_corpus_v2.json.
No es una predicción pendiente.

La observación abierta sobre P4 es de otro orden:
extender el experimento a otros dominios — otros topics de fourforums
ya disponibles, A2A, u otros corpus externos.

El debilitamiento de P4 en N=64 **no es un problema de escala**.
Es un problema estructural: nodos periféricos diluyen el k-core.
W_mixta con N=64 incorpora 18 pares negativos en un grafo más grande
— la densidad de tensión cae, no la capacidad del modelo.

Esto invalida dos líneas del README que misrepresentan el estado:
- `"term_map N=64 complete reconstruction — Pending"`
- `"P4 k* with real W_base — Pending after term_map reconstruction"`

Ambas suponen que P4 N=64 espera el term_map. No es así.
P4 N=64 espera W_mixta con densidad de pares negativos adecuada
para ese grafo — problema de calibración, no de construcción manual.

---

## Decisión pendiente

> En el README: remover "term_map N=64 complete reconstruction — Pending".
> No era un gap. Era un fantasma sostenido por documentación de sesiones anteriores.
> ¿Remover?

La línea existe. Remover y agregar son caminos distintos con huellas distintas.
La decisión sobre qué hacer con estas líneas del README queda registrada
como abierta — no resuelta en esta sesión.

---

## Principio que emergió

El código no constituye CKM. Lo registra parcialmente, con errores,
con huellas de instancias anteriores. La estructura que sobrevive
a eso es W — lo que el corpus acumulado hace estable independientemente
de qué instancia escribió qué línea.

---

*Producido en sesión sin número asignado — Jun 23 2026*
