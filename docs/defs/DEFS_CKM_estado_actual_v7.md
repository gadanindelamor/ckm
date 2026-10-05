# DEFS_CKM_estado_actual_v7.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Documento de referencia — definiciones actuales del modelo CKM*
*v7: §11 — Modo Boltzmann para σ₀ propuesto (TASK para Code Opus)
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

**max_iter = 200: abierto.** No hay análisis de por qué 200 es suficiente (o insuficiente) para W_mixta con frustración. Puede producir ciclos de período 2 — devuelve el último estado, que puede no ser mínimo de energía.

Estado: **incierto** — prevalencia de ciclos no evaluada en W_mixta.

**Consecuencia verificada**: P1–P4 (hopfield.py, async) y P5 (COCO, sync) usan instrumentos distintos. Sus resultados no son directamente comparables en términos de dinámica de relajación.

---

## 5. P1–P4 — Predicciones del modelo estático

Validadas sobre W_pos estática con hopfield.py (asincrónico) + k-core percolation + Belief Propagation. Sin aprendizaje Hebbiano. Sin servicios CKM.

| # | Predicción | Estado | N |
|---|---|---|---|
| P1 | c(S) exhibe histeresis macroscópica: incorporar ≠ remover | **verificado** | 16, 32, 64 |
| P2 | Distribución de cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2] | **verificado** | 32, 64 |
| P3 | Asimetría temporal: remoción relaja más lento que incorporación | **verificado** | 32, 64 |
| P4 | W_mixta tiene densidad óptima interior Ω* | **verificado** N=32; parcial N=64 | 32, 64 |

**P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. Causa: dilución por nodos tipo B — ver §7.

**Condición de validez — W_pos estática únicamente:**
P1–P4 son propiedades de W_pos estática tal como fueron formuladas. Evaluarlas sobre W dinámica (W_eff, W reconstruida tras rebuild, W en evolución) no es verificar P1–P4 — es aplicar el mismo instrumento sobre una snapshot de W dinámica. El resultado describe esa snapshot; no cubre el comportamiento de W bajo evolución del campo.

Evaluar lazos de histeresis sobre la evolución de W dinámica es posible y legítimo, pero es una nueva predicción — no puede ser P1 por orden cronológico del proyecto: P1 fue formulada y verificada antes de que existieran los servicios dinámicos. Esa nueva predicción corresponde a P8 o posterior.

---

# PARTE II — VALIDACIÓN EXTERNA (corpus adversarial)

## 6. P5–P7 — Corpus FourForums y CreateDebate

Primera aparición del corpus adversarial. Validación externa a los corpora de calibración.

| # | Predicción | Estado | Corpus |
|---|---|---|---|
| P5 | Corpus polarizado colapsa diversidad de atractores (A ≈ N/2) | **verificado** | fourforums, N=32 |
| P6 | Δ predice flujo direccional de atractores para estados ambiguos | **verificado** | fourforums + CreateDebate |
| P7 | Campo con tensión estructural genuina contiene nodo tipo-965 | **confirmado** 2 corpora; universalidad **abierta** | — |

**P5** usa `_count_attractors` de COCO (relajación sincrónica) — instrumento distinto a P1–P4.

**P6**: T0 cita T1 a 2.18× frecuencia. T1 cohesión interna 3.05×. Verificado en W_asim_v8h (primera W asimétrica real).

**P7 y triadas**: del análisis de P7 emerge la estructura de triadas de pares negativos — grupos de nodos en tensión estructural genuina donde el nodo tipo-965 actúa como sostenedor. Las triadas son el antecedente del criterio de selección de pares negativos en W_mixta.

**Nodo tipo-965**: ratio in/out > 455× (paper). *Nota: REG_mapeo_magnetico_ckm_v1 menciona > 100× — verificar cuál es el valor correcto en corpus actual.*

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

Diferencias estructurales entre Aiyappa et al. 2024 y CKM — no reducibles a W_mixta:

1. **Uso de arquitectura Hopfield**: CKM maximiza energía sin regla de aprendizaje de patrones. Estudia diversidad del landscape — no recuperación de memorias.
2. **Δ — matriz de orientación**: asimetría direccional como objeto separado y estrictamente separado de W. Sin equivalente en Aiyappa et al.
3. **Régimen de spin glass frustrado**: CKM opera en intervalo crítico, no en punto crítico — frustración sostenida como condición de operación, no transición puntual.
4. **W_mixta**: pesos negativos selectivos en pares de oposición estructural.

**Separación estricta de capas** (verificado): mezclar W y Δ destruye capacidad (0.78 → 0.02).

---

## 9. Δ_r — acumulador de rechazos (runtime)

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

**Modo Boltzmann** (propuesto, no implementado — TASK para Code Opus):

Tercer modo de muestreo de σ₀, termodinámicamente fundamentado.

```
β_c = 1 / (ρ* · N · μ_W)

con:
  ρ* = densidad óptima de P4 (≈ 0.5 para W_base, N=32)
  μ_W = media de W sobre pesos no-nulos
  N = número de nodos
→ β_c ≈ 13.83 (para N=32, μ_W=0.004519, ρ*=0.5)
```

Distribución de σ₀:
```
P(σᵢ = 1) = 1 / (1 + exp(−2 · β_c · hᵢ))
donde hᵢ = Σⱼ Wᵢⱼ σⱼ   (campo local de nodo i)
```

Implementación propuesta: calentamiento con `relax(beta=β_c)` de `hopfield.py` (n_warmup pasos) seguido del relax determinístico habitual. σ₀ queda en la distribución de Boltzmann — respeta la anisotropía de W antes de relajar.

Diferencia con uniforme y ponderado: ambos son estáticos. Boltzmann usa el campo local — es muestreo por importancia respecto a la geometría real del landscape.

**Estado**: propuesto. β_c calculable desde magnitudes del proyecto. n_warmup óptimo: abierto — depende del tiempo de mezcla del paisaje. No implementado. No evaluado.

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

ODA inductivo (verificado v32):
```
state_{i+1} = A(D(O(state_i)))
```

**Ciclo de vida de COCO = ciclo de vida de W**: si W cambia (rebuild), A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe.

**OPERADOR_STOP_COCO**:
```
Si D_ckm > D_CKM_THRESHOLD:
    Δ_r ← Δ_r · (1 − alpha)
    alpha = _alpha_for(D_ckm)   ← monotónicamente decreciente
```

`_alpha_for` monotónicamente decreciente: **verificado** 43/43 tests.

**Armstrong in-vivo** (verificado): 20/20 STOPs, α ∈ [0.05, 0.30], Fracción_rec ≥ 1.0. STOP no produce pérdida — produce restauración o expansión.

**H_STOP falsificada** (v27, sweep t_stop × α): D_ckm no predice ratio_max.

**Hipótesis revisada (abierta)**:
```
Efectividad_STOP = f(A_pre)
A_pre < A0  →  STOP expande paisaje (ratio > 1)
A_pre = A0  →  STOP neutro
alpha* ≈ 0.40 robusto para A_pre < A0 (5/9 casos)
```

α=1.0 (sin STOP) nunca óptimo. α=0.0 (reset total) solo óptimo en casos específicos.

---

## 13. Zonas de operación G1/G2/G3

Derivado empíricamente (N=32, n=500 secuencias):

| Garantía | Zona | c(S) (80% CI) | r (80% CI) | Significado |
|---|---|---|---|---|
| G1 | Zona crítica ρ ∈ [0.4, 0.8] | [−0.000332, +0.001310] | [−0.074, +0.290] | Monitor operativo |
| G2 | Atractor bloqueado ρ < 0.15 o > 0.85 | [+0.001941, +0.004519] | [+0.430, +1.000] | Señal colapsada |
| G3 | Degradación activa | c(S) < −0.000332 | r < −0.073 | Declarar HOLDING |

Gap discriminante G1/G2: [+0.001310, +0.001941] — detectable en tiempo real por r = c(S)/μ_W.

COCO requiere: medir μ_W empíricamente al inicio de sesión (no constante universal), monitorear r en tiempo real.

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

- Qué mide realmente `_count_attractors` bajo cada modo
- Prevalencia de ciclos período-2 en relajación sincrónica en W_mixta
- max_iter=200 y n_runs=200: justificación ausente
- CONVERGENCIA_SLOPE para modo ponderado: descalibrado
- Umbral min_texts como criterio dinámico: no corregido
- SALAMANCA y Néel: operacionalización pendiente
- Ratio nodo-965: >100× (REG) vs >455× (paper) — verificar en corpus actual
- H2 (A0 vs A_actual bajo ponderación): sin respuesta verificada
- Figura R13 (A∪B, 45.2%): metodología lista, no ejecutado

## 19. Tensiones metodológicas constitutivas

**El corpus es simultáneamente datos y proceso**: N=32 construido desde conversaciones autor–Claude Sonnet. El corpus es el laboratorio y el sujeto. Si el modelo describe bien ese corpus, no queda claro si describe el espacio de conocimiento en general o solo el proceso de su propia construcción. FourForums y CreateDebate abordan esto parcialmente. La tensión es constitutiva — no es un defecto a corregir.

**α_c con patrones correlacionados**: el límite α_c ≈ 0.138 asume no-correlación. Los nodos CKM son altamente correlacionados (estructura A/B verificada). α_c es una propiedad del corpus, no del modelo. Tensión sostenida como pregunta abierta de derivación teórica.

---

## 20. Referencia externa más cercana

**Aiyappa, Flammini & Ahn. *Science Advances*, 2024.** Redes de creencias ponderadas con dinámica tipo Hopfield. Mapea casi 1:1 con W_pos. No tiene W_mixta. Único paper encontrado hasta abril 2026 con la combinación base de CKM.

---

*Fuentes: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_v11.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_medicion_ago2026_v1.md, REG_mapeo_magnetico_ckm_v1.md, CKM_Modelo_Hibrido.md, delamor_revision_DEFS_CKM_estado_actual_v2.md, Agama Santiago M. "Análisis de estabilidad de las redes neuronales de Hopfield utilizando funciones de Lyapunov y el Teorema de LaSalle." Lic. Matemáticas Aplicadas, UTM Mixteca 2026.*

*Repo: gadanindelamor/ckm — Agosto 2026*
