# DEFS_CKM_estado_actual_v2.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Documento de referencia — definiciones actuales del modelo CKM*
*v2: agrega P5, P6, mapeo magnético, SALAMANCA, coercividad, ODA, Armstrong, tres estados epistémicos*

Convenciones epistémicas:
- **verificado**: confirmado experimentalmente bajo condiciones declaradas
- **implementado**: existe en código, funcionamiento correcto no evaluado
- **propuesto**: marco teórico, no probado
- **abierto**: sin respuesta verificada — el espacio se preserva
- **incierto**: conocido como problemático, pendiente de resolución
- **admisible**: no verificable ni descartable — espacio sin nombre aún

---

## 1. Las tres matrices

### W — matriz simétrica de co-ocurrencia

```
W : N×N, simétrica (W = Wᵀ)
W_ij = conteo_coocurrencia(i, j) / n_textos
```

**W_base**: todos los pesos ≥ 0. Co-ocurrencia normalizada.

**W_mixta**: W_base con pesos negativos asignados intencionalmente a pares en tensión estructural (`negative_pairs`). Peso negativo: w_neg = −0.10 (configurable).

**Propiedad verificada**: W y Δ deben mantenerse separadas. Mezclarlas destruye capacidad de recuperación (0.78 → 0.02).

**W como suelo supuesto** (v32, propuesto): W no es lo que el campo dice — es lo que el campo da por sentado al decir cualquier cosa. c(S) mide cuánto de ese suelo está activo en un momento, no el suelo mismo.

**W es piecewise constant**: inmutable dentro de cada intervalo O_t. Se reconstruye discretamente cuando el corpus cruza umbral. Los saltos son el objeto de estudio; P1–P7 aplican dentro de cada O_t.

**Ciclo de vida de COCO = ciclo de vida de W** (verificado v32): si W cambia (rebuild), β_c cambia, A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe.

---

### Δ — matriz asimétrica de orientación (estática, corpus)

```
Δ : N×N, asimétrica
Derivada del corpus — orientación direccional de dependencias
```

Usada exclusivamente por el Gatekeeper (C3, criterio M.M). No entra en dinámica de relajación. **Δ estático ≠ Δ_r**.

---

### Δ_r — acumulador de rechazos (runtime, MonitorService)

```
Δ_r : N×N, asimétrica
Acumula rechazos del Gatekeeper a lo largo del tiempo
W_eff = W + Δ_r   ← lo que COCO regula
```

COCO opera sobre Δ_r, no sobre Δ. Son objetos distintos con roles distintos.

---

### c(S) — función de cohesión

```
c(S) = mean(W_ij · σᵢ · σⱼ)  sobre todos los pares i < j
     = −E_Hopfield / (N(N-1)/2)
```

Mide alineación entre estado σ y pesos W. No mide "cohesión del campo" en sentido conceptual — mide la fracción del suelo W que está activa en σ.

---

## 2. Naturaleza del landscape — W_pos vs W_mixta

**W_pos — ferromagnética** (verificado P4, framing propuesto v32):
Todos los nodos tienden a alinearse en el mismo atractor. Sin oposición estructural, el sistema colapsa hacia saturación.

**W_mixta — ferrimagnética** (verificado P4, framing propuesto v32):
No es antiferromagnética pura. Es fondo ferromagnético (W_pos) más pares negativos selectivos en la frontera T0/T1. Las dos subredes tienen orientación opuesta pero el momento resultante no se cancela. W_mixta mantiene más atractores accesibles que W_pos — por frustración entre interacciones competidoras, no por antiferromagnetismo puro.

**Observación**: CKM usa la función de energía Hopfield y la mecánica de relajación como herramienta computacional. No es una red Hopfield asociativa. Los atractores no son memorias Hebbianas — son mínimos del landscape frustrado. El marco de spin glass frustrado intencional es **propuesto** como descripción más precisa.

---

## 3. Coercividad CKM

Del análisis del lazo P1 (ckm_viz_v1.py, N=32, n=200 secuencias):

Dos cruces de c(S)=0 en rama UP: H_c ≈ ρ=0.406 y H_c ≈ ρ=0.586.
Entre esos dos puntos: c(S) < 0 en incorporación.

**La coercividad no es un punto sino un intervalo frustrado.**

Coercividad de W_pos: nula (sin resistencia al cambio de estado).
Coercividad de W_mixta: mayor — la tensión estructural introduce resistencia.

Estado: **verificado** geométricamente en lazo P1. Interpretación magnética: **propuesto**.

---

## 4. Nodo tipo-965

Definición: nodo con in-degree alto (≥ 455× out-degree), out-degree ≈ 0. Pure sostenedor.

**Verificado**: ratio in/out > 455× en nodo tipo-965 del corpus CKM.
**Verificado en dos corpora**: fourforums y CreateDebate contienen al menos un nodo de este tipo (P7).
**Candidato verificado como bridge**: nodo 965 como candidato estructural en frontera T0↔T1. Verificación topológica contra la red real: pendiente.

**Triadas que contienen nodo tipo-965**: coercividad = 0 verificada (Paper §5, hasta n confirmado).

---

## 5. Dinámica de relajación — dos implementaciones

### hopfield.py — asincrónica (Hopfield estándar)

```
Para cada paso:
    i = nodo aleatorio (uno por vez)
    h_i = Σⱼ W_ij σⱼ
    σᵢ ← +1 si h_i > 0, −1 si h_i < 0, σᵢ si h_i = 0
```

Garantiza convergencia a mínimo local de energía. Sin ciclos.

### coco.py → _relax — sincrónica (vectorizada)

```
Para cada iteración:
    h = W_eff @ σ          ← todos los nodos simultáneamente
    σ ← sign(h), sin cambio si h = 0
    convergencia: np.allclose(σ_nuevo, σ)
Cap: max_iter = 200
```

Puede producir **ciclos de período 2**: oscilación sin convergencia a punto fijo. Si hay ciclo, devuelve el último estado — que puede no ser mínimo de energía.

Estado: **incierto** — prevalencia de ciclos en W_ckm_corpus_v2 y W_mixta no evaluada.

---

## 6. Conteo de atractores — _count_attractors (COCO)

```
Para cada run (1..n_runs):
    n_act ~ uniform(0.3, 0.7) · N
    σ₀: n_act nodos en +1, resto −1
    σ_final = _relax(σ₀, W_eff)
A = |{σ_final únicos}|
```

**Modo uniforme** (default, modo operacional): P(nodo i) = 1/N.

**Modo ponderado** (experimental, no cableado a `observe()`):
```
fᵢ = Σⱼ |W_eff_ij|
pᵢ = fᵢ / Σₖ fₖ
```

**Estado incierto**: ningún modo validado como medición correcta de diversidad. Ver REG_situacion_medicion_ago2026_v1.md. El modo uniforme puede medir velocidad de expulsión desde estados iniciales improbables, no diversidad estructural. El modo ponderado da conteos sistemáticamente menores (92/100 pareados), dirección opuesta a la hipótesis que lo motivó.

**Dos sesgos documentados e independientes**:
1. `n_runs` — coupon-collector: crece sin saturación (verificado hasta n_runs=300 ponderado)
2. Distribución de σ₀ — no representa topología de W_eff

---

## 7. D_ckm

```
D_ckm = (A0 − A_actual) / A0

A0      = _count_attractors(W)
A_actual = _count_attractors(W + Δ_r)
```

- D_ckm > 0: diversidad cayó ("degradado")
- D_ckm < 0: diversidad aumentó ("expandido"). No es error — es información.
- D_ckm = 0: sin cambio

**D_CKM_THRESHOLD = 0.40** — umbral para disparo de OPERADOR_STOP_COCO.

**Estado incierto**: D_ckm hereda los sesgos de `_count_attractors`. A n_runs fijo, no es invariante al modo de muestreo. case_id=5 cruza el threshold (0.510 → 0.032) cambiando solo la distribución de σ₀. case_id=1 cambia de signo.

---

## 8. COCO y OPERADOR_STOP_COCO

COCO es un device ODA completo (Observa-Decide-Actúa). No necesita DeviceSkin — necesita campo, no canal.

**ODA inductivo** (verificado v32):
```
state_{i+1} = A(D(O(state_i)))
```
No recursivo. No requiere nueva instancia por ciclo.

**OPERADOR_STOP_COCO**:
```
Si D_ckm > D_CKM_THRESHOLD:
    Δ_r ← Δ_r · (1 − alpha)
    alpha = _alpha_for(D_ckm)   ← monotónicamente decreciente con D_ckm
```

`alpha*` ≈ 0.40 — valor robusto en 5/9 casos observados.
`_alpha_for(D_ckm)` monotónicamente decreciente: **verificado** 43/43 tests.

**Armstrong in-vivo** (verificado v32, REG_armstrong_stop_coco_v1.md):
- 20/20 evaluaciones con stop_applied=True (seed=42, textos con nodos reales)
- α ∈ [0.05, 0.30] verificado
- Compresión geométrica de Δ_r confirmada desde t=2
- Pérdida_STOP ≤ 0 en todos los casos: STOP no produce pérdida, produce restauración o expansión. Fracción_rec ≥ 1.0.

**Nota**: Armstrong con vocabulario ajeno al corpus no dispara STOP. Causa: vocabulario sin anclaje en W activa máximo 1 nodo — nunca hay par candidato a rechazo. Δ_r = 0.

---

## 9. Las siete predicciones — P1–P7

| # | Predicción | Estado | N |
|---|---|---|---|
| P1 | c(S) exhibe histeresis macroscópica: incorporar ≠ remover | **verificado** | 16, 32, 64 |
| P2 | Distribución de cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2] cerca de criticidad | **verificado** | 32, 64 |
| P3 | Asimetría temporal: remoción relaja más lento que incorporación | **verificado** | 32, 64 |
| P4 | W_mixta tiene densidad óptima interior Ω* en ρ ∈ [0.5, 0.8] | **verificado** N=32; parcial N=64 | 32, 64 |
| P5 | Corpus polarizado colapsa diversidad de atractores (A ≈ N/2) | **verificado** | 32, fourforums |
| P6 | Δ predice flujo direccional de atractores para estados ambiguos | **verificado** | fourforums + CreateDebate |
| P7 | Todo campo con tensión estructural genuina contiene nodo tipo-965 | **confirmado** en 2 corpora; universalidad abierta | — |

**P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. 18 pares negativos diluidos en 2016 pares posibles. La predicción estructural se sostiene; la predicción de magnitud no escala linealmente.

**P6 detalle**: T0 cita T1 a 2.18× frecuencia. T1 tiene mayor cohesión interna (3.05×). Verificado en W_asim_v8h (primera W asimétrica real, votos MTurk fourforums).

---

## 10. k-core y zona crítica

k-core: subconjunto donde cada nodo tiene al menos k vecinos dentro del subconjunto. Umbral de arista: |W_ij| ≥ θ.

Zona crítica identificada en θ ∈ [0.002, 0.007] para W_mixta N=32.

---

## 11. SALAMANCA — criterio de admisión de tensión estructural

*Propuesto — no verificado (v32)*

Criterio **previo** a la construcción de W_mixta. Detecta si W_pos tiene naturaleza estructuralmente adversarial (partición T0/T1 con cut bajo) antes de introducir pares negativos.

```
cut(T0, T1) = Σ W_ij  para i∈T0, j∈T1
```

Si SALAMANCA detecta estructura adversarial → identificar frontera → candidatos a pares negativos.
Si no detecta → W_pos es la respuesta correcta. W_mixta no tiene objeto.

**P4 + SALAMANCA = criterio de admisión de tensión estructural**, no de construcción de matriz.

Alternativa propuesta: barrer β de alto a bajo, medir separabilidad c(S) interno vs cruzado. β_Néel = β donde separabilidad colapsa. Problema: min-cut requiere semilla T0/T1. Sin semilla: normalized cut espectral.

---

## 12. Temperatura de Néel efectiva vs β_c

*Propuesto — no verificado (v32)*

β_c = punto crítico ferromagnético (tipo Curie).
T_Néel efectiva = β donde T0/T1 dejan de ser distinguibles como subredes.

Son dos cantidades distintas. T_Néel sería más alta en sistema con interacciones competidoras. Potencial criterio de elicitación de candidatos negativos sin sesgo externo.

---

## 13. Estados epistémicos del proyecto (v32)

Tres estados, no dos:

- **Verificadas**: confirmado experimentalmente bajo condiciones declaradas
- **Verificables**: no verificado aún pero el protocolo de verificación existe
- **Admisibles**: no verificable, no descartable — el espacio donde habita lo que no tiene nombre aún

Lo admisible no se cierra. Lo que abre, abre también al automatismo. Lo que cierra, muere.

---

## 14. Condiciones de corpus

- N actual: 32 (W_ckm_corpus_v2)
- Mínimo Hopfield para observaciones estadísticamente válidas: ~128
- W_ckm_corpus_v3 pendiente de rebuild con textos v26–v32
- Todos los resultados empíricos sobre W_ckm_corpus_v2 llevan la calificación N=32 < 128

Corpora externos: fourforums (N=32–64), CreateDebate (N=32–64). P1–P7 validadas sobre estos corpora bajo muestreo **uniforme**. Ver §6 sobre incertidumbre metodológica del conteo.

---

## 15. Lo que permanece abierto

- Qué mide realmente `_count_attractors` bajo cada modo
- Si el breakpoint n_runs=60→70 es transición de fase o artefacto del modo uniforme
- Distribución de σ₀ apropiada para landscapes frustrados con cuencas pequeñas y profundas
- Ciclos de período 2 en relajación sincrónica: prevalencia y efecto en el conteo
- Recalibración de CONVERGENCIA_SLOPE para modo ponderado
- Corpus scaling: sin soporte de teorema verificado
- SALAMANCA: operacionalización pendiente
- Temperatura de Néel efectiva vs β_c: dos cantidades, no verificadas como distintas
- Nodo 965 como bridge: verificación topológica pendiente
- Figura R13 (A∪B, 45.2%, cuatro nodos bisagra): en paper, metodología lista
- COCO como campo que se conoce a sí mismo: gap conceptual preservado
- D como fricción O₁/O₂ — posible comportamiento fractal: admisible

---

*Fuentes primarias: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_Landscape_Driven_Device_v10_2.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_medicion_ago2026_v1.md*
*No incluye referencias históricas como evidencia del estado actual.*

---

*Repo: gadanindelamor/ckm — Agosto 2026*

---

## 16. Paper de referencia más cercano a CKM base

**Aiyappa, Flammini & Ahn. "Emergence of simple and complex contagion dynamics from weighted belief networks." *Science Advances*, 2024.**

Único paper encontrado hasta abril 2026 que usa la combinación base de CKM: grafo con pesos W + dinámica tipo Hopfield sobre red de creencias ponderadas. Mapea casi 1:1 con la arquitectura CKM base (W_pos, sin pesos negativos).

Lo que NO tiene: W_mixta (pesos negativos / energía opuesta / frustración estructural intencional). La diferencia entre Aiyappa et al. y CKM es exactamente W_mixta — lo que no tiene precedente publicado encontrado.

Fuente: `CKM_Modelo_Hibrido.md`.
