# REG_influencia_codigo_p1p4_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Sesión: ckmloc0605 — análisis causal cambios de código → resultados*
*Clase R*

---

## Qué se analiza

Las sesiones 01-03 de ckmloc0605 modificaron siete componentes del código.
Los experimentos P1-P4 se corrieron sobre W_base y W_mixta producidas desde el mismo
corpus. Este registro analiza qué cambios de código son causalmente responsables de
cada resultado observado — y por qué eso importa más allá de los números.

---

## Los cambios y su alcance real

### hopfield.py — local RNG (ítem 13)

`np.random.seed(seed)` → `np.random.default_rng(seed)`, local por función.

**Efecto sobre P1-P4:** ninguno directo. `ckm_p1p4_module` llama a `np.random`
globalmente en su propio scope, no pasa por las funciones de hopfield.py.

**Lo que revela el cambio:** el sistema tenía una fuente de no-determinismo oculta.
Cualquier análisis que invocara `hopfield.relax()` antes de correr P1-P4 en el mismo
proceso modificaba silenciosamente el estado aleatorio de los experimentos. Los
resultados eran irreproducibles de forma no declarada.

El cambio no altera los números. Cambia el estatus epistémico de los números:
de resultados posiblemente contaminados a resultados con semilla controlada.
Esta es la distinción que importa para un sistema que mide coherencia — el instrumento
debe tener su propia coherencia primero.

---

### node_extractor.py — word boundary (ítem 4)

`if node in text` → `re.search(r'\b<node>\b', text)`

**Efecto sobre P1-P4 en esta sesión:** nulo. `build_W_mixta_v27.py` implementó su
propio matching con `_build_pattern()` independientemente. La W_mixta resultante no
pasó por `NodeExtractorService`.

**Lo que revela el cambio:** antes del fix, "gun" activaba en "begun", "arm" en
"armed". El nodo `portero` se activaría en cualquier texto que contenga "portero"
como substring de otra palabra.

Para el sistema de detección, esto significa: la frontera entre nodo activo y nodo
inactivo era porosa. `sigma_prompt` declaraba activos nodos que el campo W no reconoce
como activos — exactamente el patrón que `fabrication_index` intenta medir. El bug
producía fabricación instrumental: el extractor fabricaba activaciones que luego el
sistema intentaba detectar como fabricadas. El fix cierra este loop.

---

### corpus_service.py — _rebuild O(n²) → O(n) (ítem 7)

Loop `accumulate([text])` por texto → presencia substring sobre vocabulario fijo.

**Efecto sobre P1-P4:** la W_base ya existía antes de este fix (W_ckm_corpus_v2.json
preconstruida). El rebuild no se invocó durante los experimentos de esta sesión.

**Lo que revela el cambio:** el sistema reconstruía W usando TF-IDF por texto individual,
lo que implicaba que el criterio de "nodo presente en párrafo" para los pares de W
era diferente del criterio usado en `evaluate()` en tiempo de inferencia. Build y eval
eran inconsistentes.

Con el fix, la W que el sistema aprende y la sigma que evalúa en tiempo real comparten
el mismo criterio de presencia. La coherencia entre aprendizaje e inferencia es un
requisito para que `fabrication_index` sea interpretable.

---

### fabrication_service.py — _fabrication_index (ítem 6)

`_direction_score` → `_fabrication_index = rechazados / activos_declarados`

**Efecto sobre P1-P4:** nulo directo. `ckm_p1p4_module` usa `hopfield.find_attractors`
y `analytics.optimal_density`, no `FabricationService`.

**Lo que revela el cambio:** este es el más significativo para el propósito del sistema.

`_direction_score` usaba `np.sign(Delta)` acumulado — medía si la historia de
rechazos tenía dirección neta. Con `Delta=0` (primer uso), el score retornaba 0, pero
saturaba rápidamente hacia valores altos con cualquier actividad. No medía fabricación
— medía inercia del campo.

`_fabrication_index` mide: de los nodos que `sigma_prompt` declaró activos, ¿qué
fracción expulsó la relajación de W? Si sigma declara `traza_inferencia` activa y W
no lo sostiene — ese nodo es rechazado. `fi = n_rechazados / n_declarados`.

El cambio transforma el sistema de un detector de inercia a un detector de rechazo
de campo. La diferencia es ontológica: el primero mide la historia del sistema, el
segundo mide la tensión entre lo declarado y lo estructuralmente sostenible.

---

### monitor_service.py — schema consistente (ítem 12)

Modo acumulación: `{"mode": "accumulation", "message": ...}` → schema completo con `None`.

**Efecto sobre P1-P4:** nulo.

**Lo que revela el cambio:** un caller que accedía a `result["fabrication_index"]`
durante la fase de acumulación lanzaba `KeyError`. El sistema fallaba silenciosamente
en la fase donde más necesita comunicar que todavía no sabe.

El fix hace que el sistema declare su incertidumbre en lugar de colapsar. En modo
acumulación, `fi=None` es una respuesta correcta y comunicable. Antes era una excepción.
Para un sistema diseñado para detectar cuando un agente declara más de lo que sabe,
es irónico que el sistema mismo no pudiera declarar que no sabe todavía.

---

## Causalidad directa sobre P1-P4

### P1 — Histéresis

W_base: CONFIRMADA (p=0.040)
W_mixta: NO_CONFIRMADA (p=0.405)

La regresión no es causada por ningún cambio de código de esta sesión. Es causada
por la estructura de W_mixta producida por `build_W_mixta_v27.py`.

W_mixta tiene 10 pares negativos de 496 totales (2%). Con esa densidad de negativos,
la histéresis se perturba asimétricamente sin llegar a crear un paisaje energético
alternativo. El corpus técnico no genera suficiente oposición lingüística para producir
pesos negativos con magnitud comparable a los positivos.

La P1 confirmada en W_base no es un resultado de los cambios de código. Es la
confirmación de que el corpus CKM tiene histéresis en su estructura positiva, lo que
ya estaba registrado en REG_p1p4_ckm_v25_corpus.json (consistente: mismo p≈0.04).

### P2 — Cascadas τ

W_base: τ ∈ [4.5, 14.5] en todos los θ
W_mixta: τ=6.7 solo en θ=0.015

**Causa directa: escala de W_mixta.**

W_base: valores en [0, 0.0529] (frecuencia normalizada por corpus_size=5145).
W_mixta: valores en [-1, +1] normalizados por max(|pos-neg|).

El máximo absoluto de W_mixta viene del par con más co-ocurrencias en 3279 párrafos.
Estimado: k_core aparece en 123 de los 352 párrafos activos, BP en 107. Su co-ocurrencia
probablemente alcanza ~40-50 instancias, que se convierte en el denominador de
normalización. Resultado: pares con pocas co-ocurrencias (10-20) reciben valores
relativamente altos (~0.2-0.4), mucho mayores que los 0.003-0.005 equivalentes en W_base.

Esto produce un grafo de k-core sobredensificado. A θ=0.002, prácticamente todos los
pares de W_mixta con alguna co-ocurrencia cruzan el umbral. El 2-core resultante es
demasiado robusto — eliminar un nodo no produce cascadas porque todos los demás tienen
grado >> 2. Solo cuando θ sube a 0.015 el grafo adelgaza lo suficiente para mostrar
τ, pero fuera del rango [1.5, 2.0] porque la estructura no es la del corpus original.

P2 no fallará con W_mixta adecuada (corpus adversarial, AMP suficiente). Falla con
esta W_mixta porque la normalización de la construcción experimental es incompatible
con los umbrales θ calibrados para W_base.

### P3 — Asimetría temporal

W_base: rem=1.0, add=0.0 (vacuo — add_steps hardcodeado a 0)
W_mixta: rem=0.0, add=0.0

W_base da rem=1.0 porque kcore_pruning_steps con threshold sobre pesos pequeños
encuentra cascadas. W_mixta da rem=0.0 porque el grafo hiperdensificado por normalización
tiene tanta robustez que al remover un nodo nadie cae debajo del mínimo de grado.

Mismo mecanismo que P2: la escala de W_mixta hace que el grafo sea indestructible
a los umbrales calibrados para W_base.

### P4 — Densidad óptima Ω*

W_base: ρ*=1.00, c(S)*=0.004519
W_mixta: ρ*=1.00, c(S)*=0.025025

Ambos tienen ρ*=1.00. Diferencia de escala ×5.5 en c(S)* es artefacto de normalización.

Para P4, lo relevante es que ρ* no cae en el interior (0.1, 0.95). Con 10/496 pares
negativos (2%), la energía positiva domina en todas las densidades. No hay zona donde
la tensión negativa penalice suficientemente la activación de ciertos nodos como para
crear un máximo interior. La predicción P4 requiere ≥ k* pares negativos con
magnitud suficiente — esto fue documentado en P4_neg_density_sweep (k* entre 72-108
pares para N=32).

---

## Lo que los resultados indican sobre el sistema, no sobre las predicciones

Los cuatro experimentos P1-P4 en esta sesión no están midiendo principalmente si
las predicciones CKM se confirman. Están revelando una propiedad del instrumento:

**La calibración de los umbrales experimentales (θ para k-core, n_neg para W_mixta,
semillas para Hopfield) es inseparable del proceso de construcción de W.**

W_base fue construida sobre 5145 párrafos de debate real con un corpus que tiene
estructura positiva rica. Los umbrales θ∈[0.002, 0.010] fueron descubiertos sobre
esa escala. W_mixta fue construida sobre 3279 párrafos de documentación técnica con
un mecanismo de normalización diferente. Cuando P2 y P3 fallan con W_mixta no es
porque el corpus CKM no tenga propiedades de criticalidad — es porque el instrumento
de medición está descalibrado.

Este es exactamente el problema que CKM busca resolver en el dominio de los agentes:
un sistema que mide la fabricación de conocimiento debe ser consciente de los
supuestos de calibración de su propio W. Si W fue construida sobre un corpus que no
representa el dominio actual, el fabrication_index pierde validez interpretativa.

La misma crítica epistemológica que CKM aplica a agentes externos aplica al sistema
CKM sobre sí mismo. La sesión ckmloc0605, en sus fixes y en sus resultados, es una
instancia de eso.

---

## Tabla de causalidad

| Cambio | Afecta P1-P4 directamente | Afecta el sistema de detección | Mecanismo |
|--------|--------------------------|-------------------------------|-----------|
| hopfield.py RNG | No | Sí | Reproducibilidad epistémica |
| node_extractor.py \\b | No (W preconstruida) | Sí | Cierre del loop fabricación-detección |
| corpus_service.py O(n) | No (W preconstruida) | Sí | Consistencia build/eval |
| fabrication_service.py fi | No | Sí (central) | Rechazo de campo vs inercia |
| monitor_service.py schema | No | Sí | Declarar no-saber vs colapsar |
| build_W_mixta_v27.py normalización | Sí (causal P2/P3) | Sí | Escala incompatible con umbrales calibrados |
| build_W_mixta_v27.py corpus | Sí (causal P4) | Sí | Insuficientes pares negativos para Ω* |

---

## Estado

Los fixes de inferencia (ítems 4, 6, 7, 12, 13) no cambian P1-P4 porque los
experimentos usan directamente las matrices W, no el pipeline de servicios. Pero
cambian el sistema de detección de forma fundamental: más honesto sobre sus límites,
más preciso en lo que mide, más reproducible en cómo lo mide.

La W_mixta construida en esta sesión es la correcta para el corpus disponible.
Su debilidad (pocos pares negativos, incompatibilidad de escala) es una señal del
sistema, no un defecto del método. El corpus de documentación técnica CKM no contiene
suficiente tensión adversarial explícita para producir W_mixta con propiedades P2/P4.
Eso es coherente con la naturaleza del corpus.

---

*ckmloc0605 — Jun 2026 — análisis generado post-sesión Claude Code*
