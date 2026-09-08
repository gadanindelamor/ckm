# PROPUESTA — capa de análisis en `services/`, criterios de diversidad, y gatekeeper

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5, Codespace ckm)*
*Documento de propuesta. Nada ejecutado, nada modificado.*

---

## Cómo leer esto

Hay un hilo que atraviesa las cuatro partes, y aparece recién al leerlas
juntas: **lo que está declarado operativo no está siendo ejercido, y las
cantidades declaradas no están definidas sin declarar su referencia.**

Aparece en la capa de raíz (tres de cinco módulos no se pueden importar),
en FabricationService (nadie lo instancia), en el gatekeeper (no existe en
`services/`), y en la diversidad (el conteo depende del muestreo). Son
cuatro instancias de la misma forma, no cuatro problemas.

Todo lo que sigue está medido. Donde hay opinión, está marcada.

---

# Parte 1 — Estado verificado de la capa de raíz

## 1.1 Tres de cinco módulos no son importables

```
core         OK
kcore        OK
analytics    FALLA — ImportError: attempted relative import with no known parent package
hopfield     FALLA — ídem
mcp_adapter  FALLA — ídem
```

Causa: import relativo (`from .core import CKMGraph`) sin `__init__.py` en
la raíz. Es el mismo hallazgo que bloqueó la primera versión de la TASK de
Boltzmann con `hopfield.py`, ahora extendido: **`analytics.py` y
`mcp_adapter.py` están en la misma situación.**

Consecuencia práctica: `optimal_density` (P4), `copresence_matrix`,
`cluster_nodes`, `perfect_oppositions`, `attractor_stats` y toda la
relajación de `hopfield.py` **no se pueden llamar desde ningún lado del
repo hoy**.

Mover a `services/` con imports planos —el estilo del resto de `services/`,
`from coco import COCO`— **no es reorganizar: es lo que los vuelve
ejecutables.** Ese es el valor principal del movimiento, aparte del
contenido.

## 1.2 Diferencias exactas de los archivos pasados

**`d_core.py` vs `core.py` (raíz):**

| | raíz | pasado |
|---|---|---|
| clase | `CKMGraph` | `CKMGraphArrays` |
| `hebb_W` | **sí** | no |
| `hebb_delta` | **sí** | no |
| `reset`, `set_state` | **sí** | no |
| import de `NodeExtractorService` | **lazy**, dentro de `from_corpus` | top-level relativo |

**`d_analytics.py` vs `analytics.py` (raíz):** las cinco funciones son
iguales; se agrega **`cluster_frontier_density`**. El import cambia a
`from .d_core import CKMGraphArrays`.

## 1.3 Dos cosas a decidir en el movimiento

**a) Los métodos Hebbianos.** `hebb_W` y `hebb_delta` están en raíz y no en
el archivo pasado. Sacarlos es coherente con el modelo — el aprendizaje
Hebbiano fue probado y rechazado.

Pero: **`hebb_W` es el instrumento que produjo el hallazgo** "mezclar W y Δ
destruye recuperación, 0.78 → 0.02", que está en el README, en THEORY R18 y
en el PAPER §4.1 como *verificado*. Si se borra, esa verificación deja de
ser re-ejecutable.

*Propuesta:* no borrarlos del repo. Si no van en la versión de `services/`,
que queden en la de raíz o en `process/`, marcados como el instrumento de
una verificación registrada. Es el mismo criterio que aplicaste con
FabricationService y con los `ABORTADA_*`.

**b) El import de `NodeExtractorService`.** `core.py` lo hace lazy
deliberadamente, con el comentario:

> *"NodeExtractorService imported lazily inside from_corpus to avoid
> circular dependency risk and keep core independent."*

Subirlo a top-level reintroduce lo que ese comentario evita — y más aún en
`services/`, donde `node_extractor` convive con todo lo demás.

*Propuesta:* mantenerlo lazy. Es una línea y preserva la independencia
declarada.

---

# Parte 2 — Criterios de diversidad: tres niveles, no uno

Lo medido esta sesión (REG_orbitas_conjuntos_invariantes_v1) más lo que
aportan estos archivos se organiza en **tres niveles distintos**, que no
compiten: miden cosas de distinto orden.

## Nivel A — estados y órbitas *(lo de esta sesión)*

| cantidad | qué es | ¿converge con n_runs? |
|---|---|---|
| terminales | lo que devuelve `_count_attractors` hoy | **no** (×82) |
| órbitas (L/~) | subconjuntos invariantes mínimos | **no** |
| \|L\| | estados del conjunto máximo invariante | **no** |
| **masa de cuenca (top-k)** | P(σ₀ cae en esa órbita) | **sí** (3–12% sobre ×100) |

Verdad de terreno por enumeración exhaustiva de 2²⁰ en tres corpus N=20.

## Nivel B — nodos *(lo que aporta `analytics.py`)*

`attractor_stats` devuelve **`node_presence`**: con qué frecuencia participa
cada nodo en los atractores. Eso es **masa a nivel de nodo** — no cuántos
atractores hay, sino **qué nodos los habitan**. Ninguna cantidad del nivel A
lo captura.

`copresence_matrix` / `cluster_nodes` / `perfect_oppositions` miden la
**organización de los nodos a través de los atractores** — correlación de
co-presencia, clusters por co-movimiento, pares en oposición perfecta.

Cuarto nivel de información: no la cardinalidad ni la masa del paisaje, sino
su **estructura interna**.

**Advertencia sobre el tipo de dato.** En `analytics.py`, `attractors` es
`dict[frozenset, int]` donde el `frozenset` es el **conjunto de nodos
activos** de un atractor. En `_relax_orbit`, la órbita es un `frozenset` de
**estados completos**. Misma forma, contenido distinto. Al integrarlos hay
que decidir explícitamente cuál se le pasa a cada función, o se van a
mezclar en silencio.

## Nivel C — clusters *(lo que aporta `cluster_frontier_density`)*

Densidad de peso intra-cluster contra inter-cluster, y
`coercivity = min(intra_a, intra_b) / inter`. Mide cuánto resiste cada
frontera entre clusters.

---

# Parte 3 — Las dos coercividades

**Esto hay que separarlo antes de intentar unificar criterios, no después.**

| | definición | qué mide | estado |
|---|---|---|---|
| **coercividad P1** | ρ donde c(S) cruza cero en la rama UP del lazo | intervalo frustrado [0.406, 0.586] | verificado geométricamente |
| **coercividad de frontera** | `min(intra_a, intra_b) / inter` entre clusters | resistencia de una frontera | implementado, no medido |

Son dos cantidades distintas con el mismo nombre. La primera es del lazo de
histéresis y es un intervalo sobre densidad; la segunda es un ratio de pesos
entre particiones de nodos. No hay razón *a priori* para que se relacionen.

*Propuesta:* nombrarlas distinto antes de usarlas juntas —
`coercividad_histeresis` y `coercividad_frontera`, o lo que prefieras— y
declarar en el paper que son dos, no una con dos métodos.

---

# Parte 4 — El gatekeeper

## 4.1 No existe en `services/`

Búsqueda exhaustiva en `services/*.py` de `gatekeeper`, `admit`, `C1`–`C4`,
`theta_W`, `alpha_c`, `score_3d`: **cero resultados**. El único
`direction_score` en `services/` es el de FabricationService, que tiene otra
fórmula.

La admisión en `MonitorService` es **implícita y de otra naturaleza**:

```python
def _rejected_pairs(self, sigma_p, sigma_r):
    """Pares que sigma_prompt declaró activos pero relax expulsó."""
```

No admite ni rechaza nodos: **relaja, y mide qué expulsó la relajación**. Es
medición post-hoc de expulsión, a nivel de **par**, no criterio de admisión a
nivel de **nodo**.

`fabrication_index` = fracción de nodos declarados que fueron expulsados.

Mientras tanto, `CKMGraph.gatekeeper` (en raíz, sin usar) aplica C1–C4 más un
`score_3d` con umbral 0.630.

**Son dos mecanismos completamente distintos, y solo uno está en el
runtime.** El PAPER §4.3 dice *"C1–C4 above describe the gatekeeper's current
implementation"* — esa implementación está en la capa que no se ejecuta.

## 4.2 Y los umbrales no aplican a los corpus actuales

`CKMConfig` declara: *"All parameters calibrated on real corpus N=16"*.

C1 exige `max|W(nodo, activos)| ≥ theta_W = 0.10`:

| corpus | max\|W\| | nodos que pasarían C1 |
|---|---:|---|
| WARMUP (N=20) | 1.0000 | 18/20 |
| caso09 natural (N=20) | 1.0000 | 20/20 |
| **`W_ckm_corpus_v2` (N=32)** | **0.0529** | **0/32** |

**Sobre el corpus CKM, C1 rechazaría todos los nodos.** Ningún peso alcanza
el umbral.

La causa es que hay **tres normalizaciones distintas de W** conviviendo:

| origen | normalización | max\|W\| resultante |
|---|---|---|
| `CorpusService._rebuild` | `(pos−neg) / max\|pos−neg\|` | **1.0** siempre |
| `CKMGraph.from_corpus` | `cooc / n_párrafos` | depende del corpus |
| `W_ckm_corpus_v2.json` | otra | **0.053** |

`theta_W = 0.10` significa algo distinto en cada una. **No es que el umbral
esté mal calibrado: es que no está definido sin declarar la
normalización.** Misma forma que la diversidad — la cantidad no existe sin
su referencia.

C4 (`_n_patterns / N < alpha_c = 0.138`) da un tope de **2.8 patrones para
N=20** y **4.4 para N=32**. No es un problema hoy porque `_n_patterns` nunca
se incrementa en ningún lado.

## 4.3 `CKMConfig` — revisión parámetro por parámetro

```python
@dataclass
class CKMConfig:
    """CKM runtime configuration. All parameters calibrated on real corpus N=16."""
    theta_W: float = 0.10       # C1
    epsilon: float = 0.005      # C2
    alpha_c: float = 0.138      # C4
    score_threshold: float = 0.630
    alpha_score: float = 0.20   # c(S)
    beta_score:  float = 0.50   # direction_score
    gamma_score: float = 0.30   # cohesion_density
    w_neg: float = 0.10
    max_iter: int = 1000
    seed: int = 42
```

### C1 y C2 degeneran sobre el mismo corpus, en direcciones opuestas

**C2** exige `c(S)_post ≥ c(S)_actual − ε`, con ε = 0.005. Pero c(S) está
acotado por `mean(|W_ij|)`:

| corpus | máx \|c(S)\| posible | ε | ε / rango |
|---|---:|---:|---:|
| WARMUP (N=20) | 0.076316 | 0.005 | 0.1× |
| **`W_ckm_corpus_v2` (N=32)** | **0.004519** | 0.005 | **1.1×** |

**En el corpus CKM, ε es mayor que el rango completo de c(S).** C2 no puede
fallar: acepta cualquier nodo.

Junto con lo de §4.2:

| criterio | sobre `W_ckm_corpus_v2` |
|---|---|
| **C1** (`theta_W = 0.10`) | **rechaza los 32 nodos** — ninguno alcanza el umbral |
| **C2** (`epsilon = 0.005`) | **acepta todos** — la tolerancia supera el rango entero |

Dos criterios que degeneran sobre el mismo corpus, en sentidos opuestos, por
la misma causa: **umbrales absolutos aplicados a una W con otra escala.**

### C4 está atado al mecanismo que el modelo rechaza

`_n_patterns` se incrementa en **un solo lugar**: `core.py:360`, dentro de
`hebb_W`. Es decir, el contador de capacidad sube únicamente cuando se usa
aprendizaje Hebbiano — el mecanismo que el proyecto probó y descartó
(0.78 → 0.02).

Consecuencia: **C4 es inerte por construcción en el modelo actual.**
`_n_patterns` queda en 0, `0/N < 0.138` siempre. Y si se sacan los Hebbianos
de la versión de `services/` (como hace el archivo pasado), queda inerte de
forma permanente y sin contador que lo pueda mover.

Además, `α_c = 0.138` **es** la capacidad asociativa Hebbiana. DEFS §17 ya
argumenta que el mínimo N≥128 de Hopfield no aplica a CKM porque CKM no
almacena memorias. El mismo argumento aplica a α_c: si no hay
almacenamiento Hebbiano, ese no es el límite de capacidad correcto.

### `max_iter` y `seed`: cuatro valores sin reconciliar

| capa | `max_iter` | `seed` |
|---|---:|---:|
| `CKMConfig` (core.py) | **1000** | **42** |
| COCO | 200 | 0 |
| MonitorService | 200 | 0 |
| `hopfield.py` (raíz) | 1000 (× N, asíncrono) | — |

Los de `CKMConfig` **no los usa `services/`**: cada servicio tiene los
suyos. Al portar, uno de los dos juegos gana o hay que declarar por qué
conviven.

Nota con lo de esta sesión: `max_iter` 1000 y 200 son **ambos pares**, así
que para órbitas de período 2 devuelven la misma fase. La diferencia sería
visible sólo con períodos ≥ 3, que no aparecen con W simétrica.

### `w_neg = 0.10` — tercera vía de introducir negativos

| mecanismo | dónde | cómo |
|---|---|---|
| marcadores de oposición | `CorpusService._rebuild` | `(pos − neg) / max\|pos−neg\|` |
| AMP sobre pares elegidos | `calibrate_W_mixta.py` | `W[i,j] = −W_base[i,j] · AMP` |
| **`w_neg`** | `CKMGraph.from_corpus` | `W[i,j] = −0.10` fijo |

Tres formas distintas de que W tenga negativos, con tres escalas distintas.
Consistente con el hallazgo de las tres normalizaciones: es el mismo
problema visto desde el otro lado.

### Lo que sí está bien

Los pesos del score suman exactamente 1: `0.20 + 0.50 + 0.30 = 1.00`. Y
`beta_score = 0.50` le da a `direction_score` (M.M) la mitad del peso — que
es coherente con que M.M sea el criterio central del modelo, no un factor
más.

## 4.4 Lo que propongo para el gatekeeper

**No portarlo tal cual.** Sería mover al runtime un mecanismo cuyo primer
criterio rechaza el corpus del proyecto.

Tres pasos, en este orden:

1. **Declarar la normalización de W como parte del contrato**, y expresar
   `theta_W` relativo a ella —por ejemplo como fracción de `max|W|` o de
   `μ_W`— en vez de absoluto. Es la misma corrección que la medida de
   referencia en diversidad.
2. **Decidir qué es la admisión en el runtime.** Hoy hay dos objetos: el
   gatekeeper node-level de `core.py` y la expulsión pair-level de
   `MonitorService`. No es obvio que el segundo deba reemplazarse por el
   primero; puede que sean dos capas legítimas (admisión al grafo vs.
   rechazo del campo). Esa es decisión del modelo, no de implementación.
3. **Recién entonces portar**, con tests, y con la calibración rehecha sobre
   la normalización declarada.

R15 está marcado *"parcialmente formalizado"* en el PAPER y en DEFS. Esto
agrega precisión a qué parte falta: no es la especificación semántica
solamente — es que los umbrales existentes no son transferibles entre
normalizaciones.

---

# Parte 5 — Orden propuesto

| # | qué | por qué en ese orden |
|---|---|---|
| 1 | Mover `analytics.py` → `services/` con imports planos, más `cluster_frontier_density` | Es lo que la vuelve ejecutable. Sin dependencias nuevas salvo `core`. |
| 2 | Mover `core.py` → `services/` como `CKMGraphArrays`, import lazy de NodeExtractor, Hebbianos preservados en algún lado | `analytics` depende de él. |
| 3 | Medir nivel B y C sobre los corpus con verdad de terreno de N=20 | Ya hay con qué contrastar: 1136 / 573 / 170 órbitas exactas. |
| 4 | Separar las dos coercividades por nombre | Antes de que entren juntas a un criterio unificado. |
| 5 | Gatekeeper: los tres pasos de §4.3 | El más grande, y el que depende de decisiones tuyas. |

Los pasos 1–3 son mecánicos y verificables con el criterio de siempre —
impacto cero por default, replicación exacta. El 4 es de nombres. El 5 es de
modelo.

---

# Parte 6 — Lo que no propongo, y las decisiones que son tuyas

**No propongo un criterio unificado de diversidad.** Los tres niveles miden
cosas de distinto orden y todavía no hay medición cruzada entre ellos. Que
sean tres dimensiones o tres vistas de una sola es empírico, y el
experimento —medir A, coercividad y cuencas sobre el mismo barrido— no se
hizo. Lo único medido es que **A y forma de cuencas se desacoplan** (barrido
AMP, sección 8 del REG): eso ya descarta que A las resuma.

**No propongo tocar `mcp_adapter.py`**, aunque tenga el mismo problema de
import. Está fuera de lo que planteaste.

**Decisiones tuyas:**

1. ¿Los Hebbianos se preservan, y dónde?
2. ¿`CKMGraphArrays` es el nombre definitivo, y `core.py` de raíz queda o se
   va a `process/`?
3. ¿La admisión en el runtime es node-level (gatekeeper) o pair-level
   (expulsión), o las dos como capas distintas?
4. ¿`theta_W` pasa a ser relativo, y a qué — `max|W|`, `μ_W`, otra cosa?
5. ¿Los tres niveles de diversidad entran al paper como tres, o hay que
   intentar unificarlos antes?

---

*Nada ejecutado. Todas las mediciones de este documento son verificables
re-corriendo lo que está citado.*
*Sep 2026 — Codespace ckm*
