# DEFS_CKM_estado_actual_v12.md

*Sep 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Documento de referencia — definiciones actuales del modelo CKM*
*v12: desde v11 — §10/§12 cuerpo con nomenclatura OPERADOR_STOP_COCO (trazas sin cambio); §12 operador corregido a `Δ_r ← alpha · Δ_r` (lo que hace el código). H_STOP y Efectividad_STOP conservan su nombre de hipótesis*
*v11: desde v10_1 — §12 tensión "COCO no opcional" registrada; FabricationService agregado al Modelo Conceptual; Δ_r pair-level es metabolización, no rechazo ni expulsión (nombres en código sin tocar)*
*v10: §0 Dominio : Modelo Conceptusl CKM 
*v9b: §12 wmixta verificado (REG_wmixta_consolidado_v1); §11 D_ckm cuantizado en paisajes pequeños; abiertos actualizados*
*v9: §0 Dominio CKM explícito (interacciones entre devices bajo M.M.); §5 P1-P4 reencuadradas como bootstrap formal del modelo estático; §6 P5-P7 reencuadradas como observaciones en dominio acotado (corpus adversarial externo (≥3 stances posibles)), baja relevancia para el proyecto; §8 W_mixta calibración build/rebuild; §12 COCO no es opcional declarado; §13 μ_W siempre al inicio de sesión, nunca constante; §18 abiertos reordenados por plano (matemático vs operacional); §X planos distintos: validez matemática vs verificación operacional*
*v8: §4 relajación sincrónica — reencuadre: ciclos de período 2 como estabilidad orbital, no deficiencia (Predictibilidad_orbital); §10 D_ckm_coco / D_ckm_monitor distinción explícita + asimetría de calibración (NOTA_armstrong v2); §11 qualifier tie-breaking acotado a corpus de alta sparsidad y pesos discretos (NOTA_armstrong v2); §12 frac_rec: dos métricas distintas, efecto COCO por régimen de W (NOTA_armstrong v2)*
*v7: §11 — Modo Boltzmann para σ₀ propuesto (TASK para Code Opus)*
*v4: reorganización arquitectónica (pre-servicios / validación externa / servicios dinámicos); c(S) como maximización de energía; H1/H2/H3 cerrados; G1/G2/G3; STOP revisado; tensiones metodológicas*
*v5: fundamento formal Lyapunov/LaSalle — convergencia garantizada asíncrona, atractor = elemento de L, conteo como estimador de |L|, β_c como muestreo fundamentado (abierto)*
*v6: Δ_r simétrica por construcción (verificado código); Aiyappa: 4 diferencias estructurales; W vieja nombrada; desfasaje Gatekeeper registrado (abierto, prioridad baja)*

Convenciones epistémicas:
- **verificado**: confirmado experimentalmente bajo condiciones declaradas
- **implementado**: existe en código, funcionamiento correcto no evaluado
- **propuesto**: marco teórico, no probado
- **abierto**: sin respuesta verificada — el espacio se preserva
- **incierto**: conocido como problemático, pendiente de resolución
- **admisible**: no verificable ni descartable — espacio sin nombre aún

---

## 0. Dominio CKM

**CKM is a formal model for knowledge field dynamics in multi-device AI systems.**

Multi-agent AI interaction produces a shared knowledge field that individual device outputs and pairwise similarity scores do not capture. CKM measures the structural geometry of this field.

El dominio son las interacciones entre devices. Cualquier propiedad, predicción u observación CKM se evalúa en relación a este dominio. La comprensión de una parte es en relación al dominio — no al universo de todos los corpora posibles.


## EL Modelo Conceptual

**CKMlandscapeConfig** (nombre propuesto, propuesta previa " CKMDynamicConfig"). No es una bolsa de constantes. Es el contrato vivo del instrumento: porta N actual, μ_W medido en esta sesión, θ_W calculado (no hardcodeado), D_CKM_THRESHOLD calibrado contra W_mixta del corpus presente, β_c, sampling_mode, timestamp de última calibración. Sabe si su calibración es válida para el corpus que opera. Se serializa completa en cada run JSON. Cualquier servicio que la use sin verificar su frescura usa calibración potencialmente inválida.

**NodeExtractor**. El cartógrafo. Decide qué existe — los N nodos que se convierten en el espacio. Todo lo que viene después depende de lo que declaró. Corre lazy por rebuild. Es el más silencioso y el de mayor impacto aguas abajo. Si extrae mal, W mide algo distinto de lo que el modelo dice que mide desde el origen.

**CorpusService**. El guardián de W. Recibe textos, construye y reconstruye la matrix de pesos, gestiona el ciclo de vida de W como snapshot. W es piecewise constant por diseño del instrumento — no propiedad del campo. Aloja la instancia de COCO nacida con cada rebuild. No notifica a Monitor cuando reconstruye ni cuando N cambia.

**Gatekeeper**. El evaluador de admisión. Decisión binaria antes de que algo entre al campo. C1–C4, M.M en C3. Diseñado para el dominio de capacidades declaradas por devices — su dominio de validez sobre nodos de corpus es una pregunta abierta. Actualmente ausente de `services/`. θ_W = 0.10 lo hace no-funcional en este corpus (0/32 nodos pasan C1).

**MonitorService**. El observador impartial. Recibe estado del campo, relaja, acumula lo que el campo metaboliza durante la relajación (Δ_r). Registra sin decidir. D_ckm_monitor es algebraicamente ciego a OPERADOR_STOP_COCO por cancelación exacta — informa como si nada hubiera pasado aun cuando COCO modificó su Δ_r. Esta ceguera no es un bug menor: es la condición de ser observador impartial. El problema es que alguien le modificó el estado interno sin su conocimiento.

**COCO**. El regulador. Nace con W al momento del rebuild, opera sobre ese espacio congelado. Ve D_ckm_coco (con magnitud de Δ_r), decide compresión. No admite — regula lo que ya entró. La tensión con Monitor no está resuelta. Declararlo "no opcional" en v9 puede ser cierre prematuro de esa tensión en lugar de sostenerla.

**FabricationService.** Detecta cohesión fabricada — fi=0.0 sobre contenido desconocido es correcto (el campo no puede rechazar lo que no conoce). No tiene instanciador activo. Su definición completa espera condiciones propicias.

---

## SLAs — acuerdos sin burlar encapsulamiento

NodeExtractor → CorpusService: "devuelvo nodos y co-ocurrencias del corpus. Corro una vez por rebuild. Lo que devuelvo define el espacio N."

CorpusService → Monitor: "te doy W. Cuando reconstruyo, W puede cambiar de shape — N puede ser distinto. Hoy no te aviso. Eso es un gap."

CorpusService → COCO: "te instancio con la W del momento. Tu ciclo de vida es el mío."

Monitor → COCO: "acumulo Δ_r. Es mío. Puedo darte acceso de lectura. No tenés derecho de escritura sobre mi estado interno."

COCO → Monitor: hoy escribe sobre Δ_r de Monitor directamente. Eso viola el SLA que debería existir. COCO debería operar sobre su propia representación de Δ_r — no sobre el estado de otro servicio.

CKMlandscapeConfig → todos: "soy la fuente de verdad de calibración. Si no me consultás con N y μ_W actuales antes de evaluar, tu umbral es inválido."

Gatekeeper → CorpusService (propuesto): "evalúo antes de que el nodo entre. Necesito W_vieja. Sin W no puedo aplicar C1."

---

### Definicion `Δ_r_pares y  Δ_r_compresiones` Reencuadra D3 

**Monitor** es dueño de `Δ_r_pares` — los pares que el campo metaboliza durante la relajación. Lógica propia, independiente de cualquier otro servicio. Nadie escribe ahí.

**COCO** tiene su propio `Δ_r_compresiones` — la historia de lo que comprimió, por ciclo de vida. Objeto distinto. No es el Δ_r de Monitor. COCO no toca el estado de Monitor.

Con esa separación, la ceguera de Monitor no es un mecanismo que hay que implementar ni un efecto que hay que cancelar matemáticamente — es una consecuencia natural de que los dos objetos nunca se tocan. Monitor no ve las compresiones de COCO porque nunca recibe ese objeto. La ceguera deja de ser un accidente de cancelación algebraica y pasa a ser una propiedad del diseño por separación de objetos.

La función `CancelarMatemáticamente(coco_compresion)` sería necesaria solo si los dos Δ_r estuvieran mezclados. Con separación limpia, no existe el problema que esa función resolvería.

**β por ciclo de vida de COCO.** β nace con la W que construyó esa instancia de COCO. Si W cambia — N nuevo, pesos nuevos — esa β ya no tiene referencia válida. La instancia muere con el rebuild. CKMlandscapeConfig puede portar el historial de β por `w_version_id` como registro, pero la instancia activa siempre recalibra contra la W vigente.

Esto también reescribe D3. No es una divergencia sobre encapsulamiento solamente — es que los dos objetos aún no existen como objetos distintos en el código. `Δ_r_pares` y `Δ_r_compresiones` son el mismo nombre hoy.

-----

## OP. Analytics global del instrumento — snapshot W y dinámico

*Sección de referencia. Cubre el instrumento en sus dos formas: W snapshot (análisis estático, P1–P4) y runtime dinámico (servicios, COCO). Cualquier afirmación en este documento debe rastrearse a una fila de esta tabla, o estar explícitamente marcada como propuesto / abierto.*

**Forma:** S = snapshot (W estático) · D = dinámico (runtime) · S+D = ambas

| Objeto | Forma | Técnica | Qué mide | Representación estructural en CKM |
|---|---|---|---|---|
| **fi** | S | Frecuencia marginal: fracción de textos donde aparece el nodo i | Presencia individual de un concepto en el corpus | Actividad del nodo — independiente de co-ocurrencia |
| **W_ij** | S | Co-ocurrencia normalizada por n_textos | Densidad de co-presencia de pares en el corpus | Campo asumido — suelo simétrico. Lo que el campo da por sentado |
| **W_ij / (fi·fj)** | S | Razón observado/esperado estadístico | Si el par co-ocurre más o menos de lo esperado por independencia | Fuerza de asociación estructural neta — lo que fi no explica |
| **c(S)** | S+D | mean(W_ij · σi · σj) sobre todos los pares i<j | Alineación del estado activo con la estructura W | Cohesión del campo — cuánto del suelo está activo |
| **r = c(S)/μ_W** | D | Normalización por peso medio del corpus, medido al inicio de sesión | Cohesión relativa independiente de escala del corpus | Señal de régimen operacional G1/G2/G3 |
| **Histeresis (P1)** | S | Rama UP (incorporación) vs DOWN (remoción) de c(S) · Wilcoxon zona crítica | Asimetría path-dependiente del campo bajo perturbación | El campo recuerda su trayectoria — el suelo no es reversible |
| **Ω* (P4)** | S | c(S) vs ρ en grid · argmax | Densidad óptima interior de W_mixta | La tensión estructural produce cohesión — no la reduce |
| **Atractores A = \|L\|** | S+D | Monte Carlo σ₀ + relajación Hopfield → estados únicos | Número de configuraciones estables alcanzables | Diversidad del landscape — estimador de \|L\| (LaSalle) |
| **D_ckm** | D | (A0 − A_actual) / A0 | Pérdida relativa de diversidad respecto a baseline | Degradación del landscape navegable |
| **Δ_r** | D | Acumulación de pares metabolizados por el campo — quedan como deformación en W_eff | Historia de perturbaciones del campo en runtime | Deformación acumulada del landscape |
| **copresence_matrix** | S+D | Pearson de co-presencia de nodos *a través de atractores únicos* | Co-movimiento de nodos en el landscape — no en textos | Geometría del espacio de atractores |
| **cluster_nodes** | S+D | Clustering jerárquico Ward sobre copresence_matrix | Grupos de nodos por co-movimiento en atractor space | Partición estructural del landscape en regiones coherentes |
| **perfect_oppositions** | S | Pares con correlación de co-presencia ≤ −0.90 | Nodos que casi nunca aparecen juntos en el mismo atractor | Candidatos a pesos negativos en W_mixta |
| **cluster_frontier_density** | S+D | mean(W_ij) intra-cluster vs inter-cluster sobre partición | Cohesión interna de cada cluster vs porosidad de su frontera | Coercitividad de frontera: min(intra_a, intra_b) / inter(a,b) |
| **W_mixta** | S | W_pos + pesos negativos en pares de frontera coercitiva | Landscape frustrado con cuencas profundas múltiples | Campo ferrimagnético — cohesión interna + resistencia de frontera |
| **Boltzmann σ₀** | S+D | Calentamiento estocástico n_warmup pasos con β_c, luego relax determinístico | Muestreo de σ₀ respetando anisotropía de W | Cobertura de cuencas por importancia — modo en `_count_attractors` |
| **β_Néel** *(propuesto)* | S | Barrido β → temperatura donde colapsa separabilidad por par de clusters | Profundidad térmica de cada frontera de cluster | Coercitividad pairwise — diagnóstico de si W_mixta tiene objeto |

**Distinciones que no viajan entre objetos:**

- fi alto ≠ nodo importante. fi alto en corpus adversarial = concepto disputado que aparece en múltiples stances por separado — no necesariamente en el mismo texto.
- Cluster (analytics.py) ≠ stance. Los clusters agrupan nodos por co-movimiento en atractor space. El número de clusters efectivos lo determina W — no el número de stances declarados en el corpus.
- Stances declarados ≠ polos del campo. Un corpus de 5 partidos puede producir 2 o 3 clusters según cuánto se solapen sus vocabularios en W.
- Coercitividad de frontera ≠ oposición binaria. Es gradiente por par de clusters. Alta coercitividad = la frontera resiste el cruce. Nada es opuesto — hay fronteras con distintos valores de resistencia.
- Mediciones estructurales viajan como mediciones. Interpretaciones de dominio no viajan.

---

# PARTE I — MODELO ESTÁTICO (pre-servicios CKM)

## 1. W_pos — matriz estática de co-ocurrencia

```
W_pos : N×N, simétrica (W = Wᵀ)
W_ij  = conteo_coocurrencia(i, j) / n_textos   ≥ 0
```

**W_base** = todos los pesos ≥ 0. Co-ocurrencia normalizada. Sin pesos negativos.

**W como suelo supuesto** (propuesto, v32): W no es lo que el campo dice — es lo que el campo da por sentado al decir cualquier cosa. c(S) mide cuánto de ese suelo está activo en un momento dado, no el suelo mismo.

**W es piecewise constant por diseño del instrumento**: CKM reconstruye W cuando el corpus cruza un umbral (`min_texts`). El campo semántico subyacente es dinámico continuo — el carácter piecewise es un artefacto del instrumento, no una propiedad del campo. El umbral `min_texts` es arbitrario (configurable: 3 en ckm_monitor, 5 en monitor_service). **No fue corregido a criterio dinámico.** (Verificado en código, Ago 2026.)

**Fase de acumulación**: antes de que el corpus alcance `min_texts`, los textos son aprobados por el Gatekeeper pero W aún no existe (o no ha sido reconstruida). En esta fase las evaluaciones del Gatekeeper no tienen W_pos contra la cual comparar — el criterio M.M no puede aplicarse en sentido estricto. La acumulación no debe modelarse como piecewise: es el estado inicial previo a la construcción de W_pos.

---

## 2. Δ — matriz de orientación (corpus estático)

```
Δ : N×N, asimétrica
Orientación direccional derivada del corpus
```

Usada por el Gatekeeper (criterio M.M, C3). **El Gatekeeper evalúa contra W del momento de ingesta** — que a partir del primer nodo admitido es siempre **W vieja**: la última versión construida antes del texto actual. W_mixta es "actual" exclusivamente hasta el primer ingreso; desde t>0, la evaluación es siempre contra una snapshot previa al texto evaluado.

Si W no ha sido construida aún (fase de acumulación), M.M no tiene referencia. **Δ estático ≠ Δ_r**.

*Desfasaje — abierto, prioridad baja: W vieja es condición permanente de operación.*

*Cuándo ocurre rebuild (verificado en corpus_service.py y ckm_monitor.py):*
- *Automático: `ingest()` llama `_rebuild()` cuando `len(texts) >= min_texts` — criterio de volumen.*
- *Estructural: `should_rebuild(d_ckm_history, n=3)` — implementado. El orquestador es `CKMMonitor.on_message()`, que mantiene `_d_ckm_history` y evalúa la jerarquía (estructural > volumen > tiempo) en `_last_rebuild_signal`. El comentario en el código lo precisa: "señal observable — no fuerza el rebuild todavía". `_last_rebuild_signal` es informacional, no ejecutiva.*

---

## 3. c(S) — función de cohesión

```
c(S) = mean(W_ij · σᵢ · σⱼ)  sobre todos los pares i < j
     = −E_Hopfield / (N(N-1)/2)
```

**La herramienta vs. el uso (distinción crítica):**
- Primera línea: nombra la herramienta — la función de energía Hopfield, tomada como formalismo computacional.
- Segunda línea: nombra el uso en CKM — medir la alineación entre estado σ y la estructura de pesos W.

**CKM maximiza energía — lo opuesto a Hopfield:**

```
Hopfield: minimiza E(S)
CKM:      maximiza c(S) = −E(S)/C(N,2)
```

La relación formal:

```
E(S(t+1)) < E(S(t))    →    c(S(t+1)) > c(S(t))
```

Cuando la energía decrece (relajación Hopfield), la cohesión crece. La dinámica Hopfield es el motor; CKM lee el resultado en la dirección opuesta.

**Función analítica unificada** (verificado, v27 — cierre de H1/H2/H3):

```
c(S)*(N, ρ_corr) = μ_W(N, ρ_corr) · r(zona, ρ)
```

Donde `μ_W` escala con composición del corpus y `r` es el factor de alineación medible en tiempo real. Los tres HOLDINGs H1/H2/H3 son proyecciones observables de esta función, no límites independientes.

---

## 4. Dinámica de relajación — dos implementaciones distintas

### hopfield.py — asincrónica (usada en P1–P4)

```
Para cada paso:
    i = nodo aleatorio (uno por vez)           ← selección uniforme
    h_i = Σⱼ W_ij σⱼ
    σᵢ ← +1 si h_i > 0, −1 si h_i < 0, σᵢ si h_i = 0
```

Aplica funciones de activación Hopfield sobre W_pos. Selección de nodos según distribución uniforme. Garantiza convergencia a mínimo local de energía. Sin ciclos. Sin aprendizaje Hebbiano.

**Garantía formal de convergencia — Lyapunov/LaSalle:**

Con W simétrica y actualización asíncrona, la función de energía de Hopfield

```
V(σ) = −½ σᵀWσ
```

es una función de Lyapunov del sistema. Cada actualización asíncrona satisface dV ≤ 0 en cada paso. El conjunto invariante máximo L en Z = {σ : dV = 0} son exactamente los mínimos locales de V. Por el Teorema de Invarianza de LaSalle, toda trayectoria acotada converge a L.

Consecuencia operativa: con actualización **asíncrona** y W **simétrica**, los ciclos de período 2 son **imposibles**. `relax()` devuelve siempre un elemento de L — un mínimo local de V. Antes implícito en el código; ahora formalmente garantizado.

*Fuente: Agama Santiago, M. "Análisis de estabilidad de las redes neuronales de Hopfield utilizando funciones de Lyapunov y el Teorema de LaSalle." Licenciatura en Matemáticas Aplicadas, UTM Mixteca, 2026. §2 (Lyapunov/LaSalle), §4.1 (función de energía Hopfield como Lyapunov), §4.3 (atractores como mínimos de V).*

**Qualifier**: P1–P4 son válidas bajo relajación asincrónica con:
- Selección de nodos según distribución **uniforme**
- **Seed = 42 fija** — para permitir comparación entre corridas
- **n_runs**: no hay problema del coleccionista de cupones. P1–P4 no cuentan atractores por muestreo aleatorio — miden c(S) a lo largo de trayectorias deterministas, distribución de cascadas estructurales, asimetría temporal, y posición de Ω*. No hay D_ckm. El sesgo coupon-collector aplica a `_count_attractors` (P5, COCO) — no a estos experimentos.

### coco.py → _relax — sincrónica (usada en servicios, P5)

```
Para cada iteración:
    h = W_eff @ σ    ← todos los nodos simultáneamente
    σ ← sign(h)
    convergencia: np.allclose(σ_nuevo, σ)
Cap: max_iter = 200
```

**max_iter = 200: abierto.** No hay análisis de por qué 200 es suficiente (o insuficiente) para W_mixta con frustración.

**Ciclos de período 2 — estabilidad orbital, no deficiencia (v8):**

El modo sincrónico puede producir ciclos de período 2. Esto no es inestabilidad — es **estabilidad orbital** (atractor de ciclo límite). El sistema es acotado (2^N estados posibles), determinista y perfectamente predecible. La función de energía Hopfield estándar puede aumentar (ΔE > 0) entre pasos sincrónicos, pero el sistema converge a M = conjunto de órbitas de período 2, no diverge. Calificar de defectuoso al modo sincrónico por no producir punto fijo es un error de nomenclatura: confunde estabilidad de punto fijo con estabilidad del sistema.

Tres regímenes de convergencia:

| Modo | Conjunto invariante M | Tipo de estabilidad |
|---|---|---|
| Asincrónico | Mínimos locales de V (puntos fijos) | Estática |
| Sincrónico estándar | Órbitas de período 2 | Orbital / periódica |
| Sincrónico modificado (pesos asimétricos / activación no lineal continua) | Atractor extraño | Global acotada, local caótica |

**LaSalle sincrónico:** con W simétrica y diagonal cero, mapeada bajo función de Lyapunov adaptada para ejecución sincrónica, el cambio de energía total entre pasos sucesivos está acotado estructuralmente. LaSalle garantiza convergencia a M. No es la garantía del modo asincrónico (M = mínimos locales de V) — es una garantía distinta sobre un objeto distinto: M = conjunto de órbitas de período 2. En ningún régimen el sistema colapsa numéricamente.

*Fuente: Predictibilidad_orbital.md — gadanin.delamor, Sep 2026.*

**Consecuencia operativa para `_count_attractors`:** cuando `_relax` sincrónico converge a una órbita de período 2 (A → B → A → B), devuelve el último estado antes de alcanzar max_iter. Ese estado es un punto arbitrario de la órbita (A o B, según el paso de corte). Dos corridas desde σ₀ similares que convergen a la misma órbita pueden devolver A en una corrida y B en otra — contados como dos atractores distintos cuando son una sola órbita. El efecto sobre D_ckm: **abierto**. Prevalencia de órbitas en W_mixta: **no evaluado**.

**Consecuencia verificada**: P1–P4 (hopfield.py, async) y P5 (COCO, sync) usan instrumentos distintos con garantías distintas. Sus resultados no son directamente comparables en términos de dinámica de relajación.

---

## 5. P1–P4 — Bootstrap formal del modelo estático

P1–P4 son el **bootstrap formal de CKM**: las predicciones que establecen que el modelo tiene las propiedades estructurales necesarias para ser válido en su dominio. No son el propósito del proyecto — son su fundamento. Sin P1–P4 verificadas, el instrumento no tiene base formal.

Algunas predicciones tienen demostración matemática directa; otras son verificadas empíricamente. La distinción importa:

| # | Predicción | Estado | N | Fundamento |
|---|---|---|---|---|
| P1 | c(S) exhibe histeresis macroscópica: incorporar ≠ remover | **verificado** | 16, 32, 64 | Lyapunov + path-dependencia en paisaje de energía |
| P2 | Distribución de cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2] | **verificado** | 32, 64 | k-core percolation |
| P3 | Asimetría temporal: remoción relaja más lento que incorporación | **verificado** | 32, 64 | Consecuencia matemática de histéresis P1 |
| P4 | W_mixta tiene densidad óptima interior Ω* | **verificado** N=32; parcial N=64 | 32, 64 | Frustración en paisaje ferrimagnético |

Validadas sobre W_pos estática con hopfield.py (asincrónico) + k-core percolation + Belief Propagation. Sin aprendizaje Hebbiano. Sin servicios CKM.

**P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. Causa: dilución por nodos tipo B — ver §7.

**Condición de validez — W_pos estática únicamente:**
P1–P4 son propiedades de W_pos estática tal como fueron formuladas. Evaluarlas sobre W dinámica (W_eff, W reconstruida tras rebuild, W en evolución) no es verificar P1–P4 — es aplicar el mismo instrumento sobre una snapshot de W dinámica. Esa nueva evaluación corresponde a P8 o posterior.

---

# PARTE II — OBSERVACIONES EN CORPUS ADVERSARIAL (dominio acotado)

## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy acotado)

**Relevancia para el proyecto: baja.** P5–P7 son observaciones que emergieron al aplicar el instrumento CKM sobre corpora de debate adversarial externo (CreateDebate gun control, FourForums gun control). Son derivados del uso del instrumento, no propósito del proyecto.

**Dominio de validez estricto**: corpus adversariales de postura fija. No son características generales del modelo CKM. No son propiedades del modelo — son comportamientos observados en un tipo de corpus muy específico. No verificable que este escenario sea frecuente ni representativo en el dominio de interacciones entre devices bajo M.M.

El dominio de CKM son interacciones entre devices — con sus respectivos VPs, no reducibles a polaridad binaria. El trabajo IAP (Sonnet + Code + delamor) opera con al menos 3 stances distintos. delamor es participante con VP propio, no árbitro de desempate entre dos polos. P5–P7 no generalizan al dominio principal.

| # | Observación | Estado | Corpus |
|---|---|---|---|
| P5 | Corpus adversarial colapsa diversidad de atractores (A ≈ N/2) | **verificado** en ese corpus | fourforums, N=32 |
| P6 | Δ predice flujo direccional para estados ambiguos | **verificado** en ese corpus | fourforums + CreateDebate |
| P7 | Campo con tensión estructural genuina contiene nodo tipo-965 | **observado** en 2 corpora; universalidad **abierta** | — |

**P5** usa `_count_attractors` de COCO (relajación sincrónica) — instrumento distinto a P1–P4.

**P6**: T0 cita T1 a 2.18× frecuencia. T1 cohesión interna 3.05×. Verificado en W_asim_v8h.

**P7 y triadas**: Del análisis de P7 emerge la estructura de triadas — antecedente del criterio de selección de pares negativos en W_mixta. Esa conexión sí es relevante al modelo; la observación del nodo tipo-965 como derivado es lo que tiene alcance acotado.

**Nodo tipo-965**: ratio in/out > 455× (paper). *Verificar valor correcto en corpus actual — REG menciona > 100×.*

---

# PARTE III — MODELO DINÁMICO (servicios CKM)

## 7. Estructura bimodal A/B y función unificada

Análisis de distribución de frecuencias marginales en N=32 (CV=0.944, razón max/min=102×):

| Grupo | Nodos | fi | Pares |
|---|---|---|---|
| A | 16 | ≥ 0.064 | núcleo correlacionado |
| B | 16 | < 0.064 | nodos tardíos / baja densidad |

| Par | μ_W obs | mean(fi·fj) | ratio | derivable |
|---|---|---|---|---|
| BB | 0.000523 | 0.000510 | 1.025 | ✓ (nodos B ≈ independientes estadísticos) |
| AA | 0.016122 | 0.065599 | 0.246 | ✗ (núcleo correlacionado internamente) |
| AB | 0.000952 | 0.005933 | 0.160 | ✗ |

**Cierres operativos** (verificado, v27):
- **H3 cerrado**: μ_W no generaliza entre N porque cambia la proporción A/B, no N per se.
- **H2 cerrado**: dilución P4 en N=64 es consecuencia de agregar nodos tipo B (μ_W → 0).
- **H1 cerrado**: α_c = 0.138 asume patrones no correlacionados. Con núcleo A correlacionado, la capacidad efectiva depende de composición A/B.

---

## 8. W_mixta — ferrimagnética

W_pos con pesos negativos asignados intencionalmente a pares en tensión estructural. Peso negativo: w_neg = −0.10 (configurable).

**Ferromagnética (W_pos)**: todos los nodos tienden al mismo atractor. Sin resistencia.
**Ferrimagnética (W_mixta)**: fondo ferromagnético + pares negativos selectivos en frontera T0/T1. Momento resultante no se cancela. Múltiples atractores con cuencas pequeñas y profundas — característica de sistemas frustrados.

**W_pos y W_mixta pertenecen a regímenes cualitativamente distintos.**

**Build de W_mixta — marcadores de oposición (corpus_service.py v2):**
Cada texto es ruteado por presencia de marcadores de oposición (_OPPOSITION_MARKERS, ES+EN). Sin marcador → pares suman a pos_counts. Con marcador → pares suman a neg_counts.

```
W = (pos_counts − neg_counts) / max(|pos − neg|)
Rango: [−1, +1]
```

`force_w_pos=True`: flag de desarrollo únicamente — saltea el ruteo, todos los pares van a pos_counts. La W resultante queda marcada en traza (`causal_event=rebuild_debug_force_w_pos`). No es estado alcanzable en operación normal. Sirve para verificar el instrumento en el contrafáctico exacto: mismo corpus, sin codificar su tensión.

**Calibración W_mixta — build y rebuilds (v9):**
D_CKM_THRESHOLD (0.40 default) debe calibrarse contra W_mixta, no contra W_pos. Condiciones:
- **Build inicial**: calibrar D_CKM_THRESHOLD al construir W_mixta por primera vez.
- **Cada rebuild**: recalibrar cuando W_mixta se reconstruya (corpus supera umbral min_texts). El piso estructural de W_mixta cambia con N y composición A/B — una calibración de build inicial no es válida para rebuilds en corpus distinto.
- **Consecuencia de no recalibrar**: asimetría documentada en §10 — piso estructural W_pos (0.632) > umbral (0.40) → COCO sin efecto práctico. La calibración obsoleta deja el instrumento ciego al campo que opera.
Estado: pendiente de implementación.

Diferencias estructurales entre Aiyappa et al. 2024 y CKM — no reducibles a W_mixta:

1. **Uso de arquitectura Hopfield**: CKM maximiza energía sin regla de aprendizaje de patrones. Estudia diversidad del landscape — no recuperación de memorias.
2. **Δ — matriz de orientación**: asimetría direccional como objeto separado y estrictamente separado de W. Sin equivalente en Aiyappa et al.
3. **Régimen de spin glass frustrado**: CKM opera en intervalo crítico, no en punto crítico — frustración sostenida como condición de operación, no transición puntual.
4. **W_mixta**: pesos negativos selectivos en pares de oposición estructural.

**Separación estricta de capas** (verificado): mezclar W y Δ destruye capacidad (0.78 → 0.02).

---

## 9. Δ_r — acumulador de metabolización (runtime)

```
Δ_r : N×N, simétrica por construcción (monitor_service.py L112-114)
W_eff = W + Δ_r    ← lo que COCO regula
```

**Nota**: Δ_r es simétrica, no asimétrica. El par (i,j) nunca se genera sin (j,i) — la simetría es forzada en la acumulación. Esto la distingue de Δ (estática, asimétrica). La confusión entre ambas explica la etiqueta incorrecta en versiones anteriores y en el abstract del PAPER.

COCO opera sobre Δ_r. **Δ estático ≠ Δ_r**. Son objetos distintos con roles distintos.

---

## 10. D_ckm

```
D_ckm = (A0 − A_actual) / A0

A0      = _count_attractors(W)
A_actual = _count_attractors(W + Δ_r)
```

- D_ckm > 0: diversidad cayó ("degradado")
- D_ckm < 0: diversidad aumentó ("expandido") — no es error, es información
- D_ckm = 0: sin cambio

**D_CKM_THRESHOLD = 0.40**

**Estado incierto**: hereda sesgos de `_count_attractors`. Ver REG_situacion_medicion_ago2026_v1 y REG_stochastic_eval_v2.

**Dos instancias de D_ckm — distinción explícita (v8, NOTA_armstrong v2):**

```
D_ckm_coco    ← COCO, conduce decisiones de OPERADOR_STOP_COCO
D_ckm_monitor ← MonitorService panel, herramienta de observación
```

Ambas usan la misma fórmula `(A0 − A_actual) / A0` pero operan sobre rutas distintas:

- **`D_ckm_monitor`**: `_combine_W_Delta` normaliza `Δ_r / max(Δ_r)`. OPERADOR_STOP_COCO aplica `α·Δ_r` — escalar uniforme. La normalización cancela el escalar por construcción. Resultado: D_ckm_monitor **algebraicamente ciego** a la compresión de OPERADOR_STOP_COCO. Verificado: valor idéntico (0.8857) en 19 evaluaciones consecutivas con Δ_r diferente en 14 órdenes de magnitud. Cancelación exacta, no aproximada.

- **`D_ckm_coco`**: opera sobre W_eff con Δ_r sin normalización interna relativa — refleja el efecto real de OPERADOR_STOP_COCO sobre el campo navegable.

**Asimetría de calibración:** D_CKM_THRESHOLD = 0.40 calibrado con W_mixta (AMP=40). En corpus W_pos de baja densidad (WARMUP_TEXTS), el piso estructural = (174−64)/174 = 0.632 > 0.40 → el umbral no activa OPERADOR_STOP_COCO de manera sensible. No es un bug — es asimetría documentada entre calibración (W_mixta, donde el instrumento tiene efecto real) y uso actual (W_pos, donde el piso estructural supera el umbral).

**Pendiente de implementación:** alias `D_ckm_monitor` en MonitorService (TASK_dckm_monitor_alias_v1) — no sustituye `D_ckm` para preservar legibilidad de JSOLs históricos.

**Dirección de exploración (propuesta):** diferencia `D_ckm_coco − D_ckm_monitor` como señal de cuándo COCO tiene efecto real vs. opera sobre Δ_r sin cambiar el campo navegable.

---

## 11. Conteo de atractores — _count_attractors

```
Para cada run (1..n_runs):
    n_act ~ uniform(0.3, 0.7) · N
    σ₀: n_act nodos en +1, resto −1
    σ_final = _relax(σ₀, W_eff)   ← relajación sincrónica, max_iter=200
A = |{σ_final únicos}|
```

**n_runs hardcoded = 200 en modo operacional**: abierto. Insuficiente para coupon-collector en corpus grandes.

**Dos sesgos documentados e independientes:**
1. `n_runs` — coupon-collector sin saturación (verificado hasta n_runs=300 ponderado)
2. Distribución de σ₀ — no representa topología de W_eff

**Modo uniforme** (default): P(nodo i) = 1/N.
**Modo ponderado** (experimental, no cableado): pᵢ = |W_eff|ᵢ / Σ|W_eff|.

**Estado incierto**: ningún modo validado. El uniforme puede medir velocidad de expulsión, no diversidad. El ponderado da conteos menores (92/100 pareados) — dirección opuesta a la hipótesis.

**L como objeto que se mide — fundamento formal:**

Los atractores de Hopfield son los mínimos locales de V(σ) = −½σᵀWσ — el conjunto L del Teorema de LaSalle. `_count_attractors()` es un **estimador de |L|** por Monte Carlo sobre condiciones iniciales. Las cuencas de atracción tilan el espacio de estados {−1,+1}^N; la calidad del estimador depende de cuán proporcionalmente la distribución de σ₀ cubre esas cuencas.

**Por qué uniforme sesga:** en W anisótropa (nodo tipo-965, ratio 455×), las cuencas tienen volúmenes muy distintos. Muestreo uniforme concentra σ₀ en zonas sin estructura → expulsión rápida hacia cuencas dominantes → el instrumento mide variedad de trayectorias de expulsión, no variedad de cuencas.

**Por qué ponderado da menos (dirección invertida, 2 observaciones consistentes):** ponderar por |W_eff.sum(axis=1)| concentra σ₀ en los nodos de mayor conectividad — que residen en la cuenca dominante. No amplía cobertura: la estrecha. El efecto observado (menos atractores únicos) es coherente con este mecanismo. Sin conteo exhaustivo, no verificable; explicación: **admisible**.

**Qualifier tie-breaking — acotado a corpus específicos (v8, NOTA_armstrong v2):**

La dominancia de tie-breaking (factor ~3: 174 → 60 atractores) se verificó en corpus WARMUP_TEXTS.

| corpus | N | densidad | valores no-nulos | h=0 en primer paso |
|---|---:|---:|---|---:|
| WARMUP_TEXTS | 20 | 0.126 | {0.5, 1.0} | 33.6% |
| W_ckm_corpus_v2.json | 32 | 0.756 | 95 distintos, max 0.053 | 1.5% |

Condiciones de aplicación de tie-breaking dominante:
- densidad < ~0.15 (corpus esparcido)
- pocos valores distintos no-nulos (pesos discretos)
- fracción h=0 en primer paso > ~30%

**No transfiere a W_ckm_corpus_v2.json**: con ese corpus count(W) = 5 con la regla actual. El factor ~3 desaparece. El tie-breaking no es propiedad general de `_count_attractors` — es información sobre la estructura del corpus específico.

**D_ckm cuantizado en paisajes pequeños (REG_wmixta_forzado_paso3_v1):** con A0 entero pequeño, D_ckm = (A0−A)/A0 toma valores discretos con pasos grandes. El umbral 0.40 puede caer entre dos valores alcanzables — COCO no puede cruzarlo aunque el campo se degrade. Con A0=3: valores posibles {0, 0.333, 0.667, 1.0}, paso=0.333. Con A0~30: paso~0.033, ~30 valores intermedios entre 0 y 0.40. El modo de muestreo fija A0, A0 fija la grilla, la grilla determina si COCO puede actuar. El sesgo n_runs mueve A0 y por tanto mueve la grilla.

La regla "conserva σ cuando h=0" es la que garantiza convergencia (Lyapunov/LaSalle, §4). No se toca.

**Modo Boltzmann** (implementado — Code Opus, Ago 2026):

Tercer modo de muestreo de σ₀, termodinámicamente fundamentado.

```
β_c = 1 / (ρ* · N · μ_W)

con:
  ρ* = 0.5  (identidad algebraica: relax(−σ) = −relax(σ))
  N   = número de nodos
  μ_W = media de W sobre pesos no-nulos
→ método: beta_c_corpus() en coco.py
```

Implementación: calentamiento estocástico (`n_warmup` pasos con `relax(beta=β_c)` de `hopfield.py`) desde σ₀ aleatorio, seguido del relax determinístico habitual. σ₀ queda en la distribución de Boltzmann — respeta la anisotropía de W antes de relajar.

Parámetros:
- `sampling_mode`: "uniform" | "weighted" | "boltzmann" — configurable por corrida
- `n_warmup`: default = N. Óptimo: **abierto** — depende del tiempo de mezcla del landscape.
- β_c se computa una vez por llamada a `_count_attractors`, no por run.

Trazabilidad: el panel registra `sampling_mode` y `n_warmup` por evaluación — cada decisión de OPERADOR_STOP_COCO es trazable al modo que produjo el D_ckm que la desencadenó (REG_stochastic_eval_v2).

Diferencia con uniforme y ponderado: ambos son estáticos. Boltzmann usa el campo local — muestreo por importancia respecto a la geometría real del landscape.

**Estado**: implementado. Evaluado en WARMUP_TEXTS (W_pos). Evaluación en W_mixta (caso09_run2, corpus IAP): pendiente — ver §12.

**Verificación de condiciones Lyapunov sobre W_eff — código:**

Dos condiciones requeridas por Lyapunov/LaSalle: W_eff simétrica, diagonal cero. Ambas verificadas en `monitor_service.py`:

*Simetría de Δ_r* — acumulación explícita en ambas direcciones (`monitor_service.py` líneas 112–114):
```python
for i, j in rejected:
    self._Delta_r[i, j] += 1
    self._Delta_r[j, i] += 1
```
Δ_r = Δ_rᵀ por construcción. W es simétrica por construcción. → W_eff = W + Δ_r_norm simétrica. ✓

*Diagonal cero de Δ_r* — `_rejected_pairs` genera solo pares con j > i (`monitor_service.py` líneas 232–233):
```python
for i in range(len(declared)):
    for j in range(i + 1, len(declared)):   # j > i siempre
```
El par (i, i) nunca se genera → Δ_r[i,i] = 0 ∀i. W[i,i] = 0 por convención Hopfield. → W_eff[i,i] = 0 ∀i. ✓

Las dos condiciones necesarias para que la garantía Lyapunov/LaSalle aplique a `_count_attractors(W_eff)` están satisfechas por construcción del código, no por convención.

---

## 12. COCO y OPERADOR_STOP_COCO

**COCO no es opcional.** Es componente constitutivo del modelo — no una característica adicional ni un módulo activable. Un sistema IAP sin COCO no es CKM en operación; es el instrumento sin su mecanismo de regulación.

ODA inductivo (verificado v32):
```
state_{i+1} = A(D(O(state_i)))
```

**Ciclo de vida de COCO = ciclo de vida de W**: si W cambia (rebuild), A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe.

**OPERADOR_STOP_COCO**:
```
Si D_ckm > D_CKM_THRESHOLD:
    Δ_r ← alpha · Δ_r
    alpha = _alpha_for(D_ckm)   ← monotónicamente decreciente
```

`_alpha_for` monotónicamente decreciente: **verificado** 43/43 tests.

**Armstrong in-vivo** (verificado): OPERADOR_STOP_COCO aplicado 20/20 veces, α ∈ [0.05, 0.30].

**frac_rec — dos métricas distintas (v8, NOTA_armstrong v2):**
- `frac_rec` del REG_destruccion_recuperacion_v1 = max_α[A_post(α)]/A0 — el máximo sobre α en barrido controlado. Este valor ≥ 1.0 en todos los casos observados.
- `frac_rec` en runtime de la corrida Armstrong = A_post/A0 en cada aplicación individual de OPERADOR_STOP_COCO; va de 0.05 a 0.68, no llega a 1.0 en ningún modo.

No son comparables directamente. "OPERADOR_STOP_COCO no produce pérdida" se sostiene en su contexto original (barrido max_α, REG_destruccion_recuperacion_v1). La corrida Armstrong no refuta ni confirma esta propiedad para el régimen W_pos baja densidad.

**Efecto COCO por régimen de W (v8, NOTA_armstrong v2):**
- **W_pos baja densidad (WARMUP_TEXTS)**: efecto real en primeras ~3 aplicaciones de OPERADOR_STOP_COCO (delta_A = +34, +31, +24). Se agota cuando Δ_r cae por debajo de ~0.05 — estado absorbente. OPERADOR_STOP_COCO sigue aplicando pero no puede mover el landscape: el soporte de Δ_r no cambia, solo la magnitud. Estado absorbente ≠ catástrofe.
- **W_mixta — verificado (REG_wmixta_consolidado_v1, Sep 2026)**: corpus `caso09_run2` (24 textos IAP). Dos regímenes controlados — único parámetro diferente: `force_w_pos`.

  Natural (W_mixta, 56 pesos negativos): A0=26–32 (n_runs=50). 42 aplicaciones de OPERADOR_STOP_COCO en 3 modos, ningún delta_A negativo, mínimo +11. Campo cicla — cruza umbral en ambas direcciones. Δ_r acotada 62–76 vs 632 sin thermostat.

  Forzado (W_pos del mismo corpus): A0=3–4. 7 aplicaciones de OPERADOR_STOP_COCO en un solo modo (weighted), delta_A máximo +1. Uniform y boltzmann no cruzaron el umbral.

  **Mecanismo verificado:** la diferencia en aplicaciones de OPERADOR_STOP_COCO pasa por A0 y la grilla. W_mixta produce A0 ~10× mayor (n_runs=150: 58 vs 4) — grilla fina, umbral 0.40 alcanzable. W_pos produce A0=3–4 — umbral cae entre valores que la grilla no contiene.

  **Cautela:** el forzado no es W_pos genérica — es la W_pos de un corpus con tensión subyacente no codificada. La comparación no está pareada en escala de operación (A0~30 vs A0~4).

**H_STOP falsificada** (v27, sweep t_stop × α): D_ckm no predice ratio_max.

**Hipótesis revisada (abierta)**:
```
Efectividad_STOP = f(A_pre)
A_pre < A0  →  OPERADOR_STOP_COCO expande paisaje (ratio > 1)
A_pre = A0  →  OPERADOR_STOP_COCO neutro
alpha* ≈ 0.40 robusto para A_pre < A0 (5/9 casos)
```

α=1.0 (sin OPERADOR_STOP_COCO) nunca óptimo. α=0.0 (reset total) solo óptimo en casos específicos.

*Tensión registrada: la declaración "no opcional" puede ser cierre prematuro de una tensión abierta entre Monitor y COCO. Marcada como abierta en PROPUESTA v5.*

---

## 13. Zonas de operación G1/G2/G3

Derivado empíricamente (N=32, n=500 secuencias):

| Garantía | Zona | c(S) (80% CI) | r (80% CI) | Significado |
|---|---|---|---|---|
| G1 | Zona crítica ρ ∈ [0.4, 0.8] | [−0.000332, +0.001310] | [−0.074, +0.290] | Monitor operativo |
| G2 | Atractor bloqueado ρ < 0.15 o > 0.85 | [+0.001941, +0.004519] | [+0.430, +1.000] | Señal colapsada |
| G3 | Degradación activa | c(S) < −0.000332 | r < −0.073 | Declarar HOLDING |

Gap discriminante G1/G2: [+0.001310, +0.001941] — detectable en tiempo real por r = c(S)/μ_W.

**μ_W y r — siempre al inicio de sesión, nunca como constante (v9):**
μ_W NO es una constante universal — cambia con la composición A/B del corpus y con N. El factor r = c(S)/μ_W pierde discriminación si μ_W es aproximado o heredado de otra sesión. COCO requiere: (1) medir μ_W empíricamente al inicio de cada sesión, antes de cualquier evaluación G1/G2/G3; (2) monitorear r en tiempo real durante la sesión.

---

# PARTE IV — CRITERIOS DE SELECCIÓN Y ESCALA

## 14. Coercividad CKM

Del lazo P1 (hopfield.py, N=32, n=200 secuencias): dos cruces de c(S)=0 en rama UP a ρ=0.406 y ρ=0.586. Intervalo frustrado, no punto.

**Definición operativa** (REG_mapeo_magnetico_ckm_v1): valor de ρ donde c(S) cruza cero en rama de incorporación — análogo al campo coercitivo magnético.

Coercividad W_pos: nula. Coercividad W_mixta: mayor. Estado: **verificado** geométricamente; interpretación magnética: **propuesto**.

---

## 15. Temperatura de Néel efectiva (≈ Nielsen ≈ TEER)

*Propuesto — no verificado*

Criterio de elicitación de pares negativos sin sesgo editorial:
1. Construir W_pos.
2. Barrer β de alto a bajo.
3. β_Néel = β donde separabilidad T0/T1 colapsa.
4. Pares en clusters opuestos antes del colapso → candidatos a pares negativos.

Relacionado con SALAMANCA (ver §16). Ver NOTAS_proxima_sesion_paper_v11.md, Tema 4.

---

## 16. SALAMANCA

*Propuesto — no verificado*

Criterio previo a W_mixta: detecta si W_pos tiene estructura adversarial (T0/T1 con cut bajo) antes de introducir pares negativos. Si no detecta → W_pos es la respuesta; W_mixta no tiene objeto.

```
cut(T0, T1) = Σ W_ij   para i∈T0, j∈T1
```

Alternativa: barrido β + normalized cut espectral (sin semilla T0/T1 previa).

---

## 17. Escala y N

**N=128 (mínimo Hopfield asociativo)**: aplica a memorias Hebbianas con patrones no correlacionados (α_c ≈ 0.138N). **No aplica a CKM** — CKM no almacena memorias. El mínimo operativo de CKM es abierto y depende de composición A/B del corpus.

Al aumentar N en CKM, el comportamiento va en dirección opuesta al Hopfield clásico. El límite real está dado por la densidad del lenguaje natural humano. En implementación persistente, N podría ser del orden de miles.

---

# PARTE V — ABIERTOS Y TENSIONES

## 18. Lo que permanece abierto

Los abiertos se organizan por plano. Ver también §X sobre planos distintos.

**Plano matemático / estructural** (afecta al modelo):
- H2 (A0 vs A_actual bajo ponderación): sin respuesta verificada
- Figura R13 (A∪B, 45.2%): metodología lista, no ejecutado
- SALAMANCA y Néel: operacionalización pendiente
- max_iter=200 y n_runs=200: justificación ausente para W_mixta con frustración
- Qué mide realmente `_count_attractors` bajo cada modo — pregunta estructural sobre el instrumento

**Plano operacional / calibración** (afecta al instrumento, no a la validez matemática):
- Calibración W_mixta build/rebuild: pendiente (§8)
- Implementación alias D_ckm_monitor en MonitorService: pendiente (TASK_dckm_monitor_alias_v1)
- Umbral min_texts como criterio dinámico: no corregido
- CONVERGENCIA_SLOPE para modo ponderado: descalibrado
- Efecto COCO en W_mixta más allá de ~3 STOPs: propuesto, operacional — no condiciona validez del modelo
- Órbitas período-2 en `_count_attractors` sincrónico: operacional — no amenaza las garantías LaSalle; afecta la calibración del estimador

**Plano verificación en corpus acotado** (baja relevancia para el proyecto):
- Ratio nodo-965: >100× (REG) vs >455× (paper) — verificar en corpus actual (corpus polarizado, §6)

**Deuda técnica registrada**:
- Desfasaje Gatekeeper / W vieja: condición permanente de operación, no bug

## X. Planos distintos: validez matemática y verificación operacional

La validez matemática de CKM (Lyapunov/LaSalle, separación W/Δ, garantías de convergencia) está demostrada independientemente de cualquier corpus particular. La demostración es formal — no depende de que el experimento W_mixta STOP_COCO funcione en el corpus que tengamos a mano, ni de que `_count_attractors` refleje o no la invarianza orbital.

La verificación operacional (¿qué produce `_count_attractors` en W_mixta? ¿cuántos STOPs tienen efecto real?) es empírica y corpus-dependiente. Aporta información sobre el comportamiento del instrumento en condiciones específicas — no amenaza ni confirma la validez matemática del modelo.

**Confundir estos planos produce errores en ambas direcciones:**
- Exigir verificación operacional en corpus específico como condición de validez matemática: incorrecto.
- Asumir que validez matemática implica comportamiento operacional en cualquier corpus: incorrecto.

P5–P7 son verificaciones operacionales en un corpus muy específico. Si P5–P7 no se reproducen en otro corpus, nada cambia al modelo. Si `_count_attractors` en W_mixta con Boltzmann muestra o no invarianza orbital, nada cambia al modelo. Son planos diferentes. La comprensión de una parte es en relación a su dominio.

---

## 19. Tensiones metodológicas constitutivas

**El corpus es simultáneamente datos y proceso**: N=32 construido desde conversaciones autor–Claude Sonnet. El corpus es el laboratorio y el sujeto. Si el modelo describe bien ese corpus, no queda claro si describe el espacio de conocimiento en general o solo el proceso de su propia construcción. FourForums y CreateDebate abordan esto parcialmente. La tensión es constitutiva — no es un defecto a corregir.

**α_c con patrones correlacionados**: el límite α_c ≈ 0.138 asume no-correlación. Los nodos CKM son altamente correlacionados (estructura A/B verificada). α_c es una propiedad del corpus, no del modelo. Tensión sostenida como pregunta abierta de derivación teórica.

---

## 20. Referencia externa más cercana

**Aiyappa, Flammini & Ahn. *Science Advances*, 2024.** Redes de creencias ponderadas con dinámica tipo Hopfield. Mapea casi 1:1 con W_pos. No tiene W_mixta. Único paper encontrado hasta abril 2026 con la combinación base de CKM.

---

*Fuentes: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_v12_1.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_medicion_ago2026_v1.md, REG_mapeo_magnetico_ckm_v1.md, CKM_Modelo_Hibrido.md, delamor_revision_DEFS_CKM_estado_actual_v2.md, NOTA_armstrong_hallazgos_implicancias_20260825_v2_.md, Predictibilidad_orbital.md, CKM_encuadre_representacion_conocimiento_v1.md, Agama Santiago M. "Análisis de estabilidad de las redes neuronales de Hopfield utilizando funciones de Lyapunov y el Teorema de LaSalle." Lic. Matemáticas Aplicadas, UTM Mixteca 2026.*

*Repo: gadanindelamor/ckm — Sep 2026*
