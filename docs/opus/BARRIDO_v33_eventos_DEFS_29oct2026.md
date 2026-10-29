# BARRIDO v33 — eventos, bloque por bloque — DEFS v2–v20 (θ = 0,6)

Generado por `docs/opus/barrido_mapa.py defs 0.6` (29 oct 2026). Cada línea es un bloque (párrafo) y lo que le pasa entre versiones contiguas; v0 es una versión vacía, así lo de la primera versión cuenta como "llega". Texto cortado a 220 caracteres. Sin lectura ni categorías.

## v0 → v2

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | # DEFS_CKM_estado_actual_v2.md | *Ago 2026 — gadanin.delamor + Claude Sonnet 4.6* *Documento de referencia — definiciones actuales del modelo CKM* *v2: agrega P5, P6, mapeo magnético, SALAMANCA, coercividad, ODA, Armstrong, tres estados epistémicos* |
| nuevo | # DEFS_CKM_estado_actual_v2.md | Convenciones epistémicas: - **verificado**: confirmado experimentalmente bajo condiciones declaradas - **implementado**: existe en código, funcionamiento correcto no evaluado - **propuesto**: marco teórico, no probado - … |
| nuevo | ### W — matriz simétrica de co-ocurrencia | **W_base**: todos los pesos ≥ 0. Co-ocurrencia normalizada. |
| nuevo | ### W — matriz simétrica de co-ocurrencia | **W_mixta**: W_base con pesos negativos asignados intencionalmente a pares en tensión estructural (`negative_pairs`). Peso negativo: w_neg = −0.10 (configurable). |
| nuevo | ### W — matriz simétrica de co-ocurrencia | **Propiedad verificada**: W y Δ deben mantenerse separadas. Mezclarlas destruye capacidad de recuperación (0.78 → 0.02). |
| nuevo | ### W — matriz simétrica de co-ocurrencia | **W como suelo supuesto** (v32, propuesto): W no es lo que el campo dice — es lo que el campo da por sentado al decir cualquier cosa. c(S) mide cuánto de ese suelo está activo en un momento, no el suelo mismo. |
| nuevo | ### W — matriz simétrica de co-ocurrencia | **W es piecewise constant**: inmutable dentro de cada intervalo O_t. Se reconstruye discretamente cuando el corpus cruza umbral. Los saltos son el objeto de estudio; P1–P7 aplican dentro de cada O_t. |
| nuevo | ### W — matriz simétrica de co-ocurrencia | **Ciclo de vida de COCO = ciclo de vida de W** (verificado v32): si W cambia (rebuild), β_c cambia, A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe. |
| nuevo | ### Δ — matriz asimétrica de orientación (estática, corpus) | ### Δ — matriz asimétrica de orientación (estática, corpus) |
| nuevo | ### Δ — matriz asimétrica de orientación (estática, corpus) | ``` Δ : N×N, asimétrica Derivada del corpus — orientación direccional de dependencias ``` |
| nuevo | ### Δ — matriz asimétrica de orientación (estática, corpus) | Usada exclusivamente por el Gatekeeper (C3, criterio M.M). No entra en dinámica de relajación. **Δ estático ≠ Δ_r**. |
| nuevo | ### Δ_r — acumulador de rechazos (runtime, MonitorService) | ### Δ_r — acumulador de rechazos (runtime, MonitorService) |
| nuevo | ### Δ_r — acumulador de rechazos (runtime, MonitorService) | ``` Δ_r : N×N, asimétrica Acumula rechazos del Gatekeeper a lo largo del tiempo W_eff = W + Δ_r ← lo que COCO regula ``` |
| nuevo | ### Δ_r — acumulador de rechazos (runtime, MonitorService) | COCO opera sobre Δ_r, no sobre Δ. Son objetos distintos con roles distintos. |
| nuevo | ### c(S) — función de cohesión | ``` c(S) = mean(W_ij · σᵢ · σⱼ) sobre todos los pares i < j = −E_Hopfield / (N(N-1)/2) ``` |
| nuevo | ### c(S) — función de cohesión | Mide alineación entre estado σ y pesos W. No mide "cohesión del campo" en sentido conceptual — mide la fracción del suelo W que está activa en σ. |
| nuevo | ## 2. Naturaleza del landscape — W_pos vs W_mixta | ## 2. Naturaleza del landscape — W_pos vs W_mixta |
| nuevo | ## 2. Naturaleza del landscape — W_pos vs W_mixta | **W_pos — ferromagnética** (verificado P4, framing propuesto v32): Todos los nodos tienden a alinearse en el mismo atractor. Sin oposición estructural, el sistema colapsa hacia saturación. |
| nuevo | ## 2. Naturaleza del landscape — W_pos vs W_mixta | **W_mixta — ferrimagnética** (verificado P4, framing propuesto v32): No es antiferromagnética pura. Es fondo ferromagnético (W_pos) más pares negativos selectivos en la frontera T0/T1. Las dos subredes tienen orientación… |
| nuevo | ## 2. Naturaleza del landscape — W_pos vs W_mixta | **Observación**: CKM usa la función de energía Hopfield y la mecánica de relajación como herramienta computacional. No es una red Hopfield asociativa. Los atractores no son memorias Hebbianas — son mínimos del landscape … |
| nuevo | ## 3. Coercividad CKM | Del análisis del lazo P1 (ckm_viz_v1.py, N=32, n=200 secuencias): |
| nuevo | ## 3. Coercividad CKM | Dos cruces de c(S)=0 en rama UP: H_c ≈ ρ=0.406 y H_c ≈ ρ=0.586. Entre esos dos puntos: c(S) < 0 en incorporación. |
| nuevo | ## 3. Coercividad CKM | **La coercividad no es un punto sino un intervalo frustrado.** |
| nuevo | ## 3. Coercividad CKM | Coercividad de W_pos: nula (sin resistencia al cambio de estado). Coercividad de W_mixta: mayor — la tensión estructural introduce resistencia. |
| nuevo | ## 3. Coercividad CKM | Estado: **verificado** geométricamente en lazo P1. Interpretación magnética: **propuesto**. |
| nuevo | ## 4. Nodo tipo-965 | Definición: nodo con in-degree alto (≥ 455× out-degree), out-degree ≈ 0. Pure sostenedor. |
| nuevo | ## 4. Nodo tipo-965 | **Verificado**: ratio in/out > 455× en nodo tipo-965 del corpus CKM. **Verificado en dos corpora**: fourforums y CreateDebate contienen al menos un nodo de este tipo (P7). **Candidato verificado como bridge**: nodo 965 c… |
| nuevo | ## 4. Nodo tipo-965 | **Triadas que contienen nodo tipo-965**: coercividad = 0 verificada (Paper §5, hasta n confirmado). |
| nuevo | ### hopfield.py — asincrónica (Hopfield estándar) | ``` Para cada paso: i = nodo aleatorio (uno por vez) h_i = Σⱼ W_ij σⱼ σᵢ ← +1 si h_i > 0, −1 si h_i < 0, σᵢ si h_i = 0 ``` |
| nuevo | ### hopfield.py — asincrónica (Hopfield estándar) | Garantiza convergencia a mínimo local de energía. Sin ciclos. |
| nuevo | ### coco.py → _relax — sincrónica (vectorizada) | ``` Para cada iteración: h = W_eff @ σ ← todos los nodos simultáneamente σ ← sign(h), sin cambio si h = 0 convergencia: np.allclose(σ_nuevo, σ) Cap: max_iter = 200 ``` |
| nuevo | ### coco.py → _relax — sincrónica (vectorizada) | Puede producir **ciclos de período 2**: oscilación sin convergencia a punto fijo. Si hay ciclo, devuelve el último estado — que puede no ser mínimo de energía. |
| nuevo | ### coco.py → _relax — sincrónica (vectorizada) | Estado: **incierto** — prevalencia de ciclos en W_ckm_corpus_v2 y W_mixta no evaluada. |
| nuevo | ## 6. Conteo de atractores — _count_attractors (COCO) | ``` Para cada run (1..n_runs): n_act ~ uniform(0.3, 0.7) · N σ₀: n_act nodos en +1, resto −1 σ_final = _relax(σ₀, W_eff) A = \|{σ_final únicos}\| ``` |
| nuevo | ## 6. Conteo de atractores — _count_attractors (COCO) | **Modo uniforme** (default, modo operacional): P(nodo i) = 1/N. |
| nuevo | ## 6. Conteo de atractores — _count_attractors (COCO) | **Modo ponderado** (experimental, no cableado a `observe()`): ``` fᵢ = Σⱼ \|W_eff_ij\| pᵢ = fᵢ / Σₖ fₖ ``` |
| nuevo | ## 6. Conteo de atractores — _count_attractors (COCO) | **Estado incierto**: ningún modo validado como medición correcta de diversidad. Ver REG_situacion_medicion_ago2026_v1.md. El modo uniforme puede medir velocidad de expulsión desde estados iniciales improbables, no divers… |
| nuevo | ## 6. Conteo de atractores — _count_attractors (COCO) | **Dos sesgos documentados e independientes**: 1. `n_runs` — coupon-collector: crece sin saturación (verificado hasta n_runs=300 ponderado) 2. Distribución de σ₀ — no representa topología de W_eff |
| nuevo | ## 7. D_ckm | - D_ckm > 0: diversidad cayó ("degradado") - D_ckm < 0: diversidad aumentó ("expandido"). No es error — es información. - D_ckm = 0: sin cambio |
| nuevo | ## 7. D_ckm | **D_CKM_THRESHOLD = 0.40** — umbral para disparo de OPERADOR_STOP_COCO. |
| nuevo | ## 7. D_ckm | **Estado incierto**: D_ckm hereda los sesgos de `_count_attractors`. A n_runs fijo, no es invariante al modo de muestreo. case_id=5 cruza el threshold (0.510 → 0.032) cambiando solo la distribución de σ₀. case_id=1 cambi… |
| nuevo | ## 8. COCO y OPERADOR_STOP_COCO | COCO es un device ODA completo (Observa-Decide-Actúa). No necesita DeviceSkin — necesita campo, no canal. |
| nuevo | ## 8. COCO y OPERADOR_STOP_COCO | **ODA inductivo** (verificado v32): ``` state_{i+1} = A(D(O(state_i))) ``` No recursivo. No requiere nueva instancia por ciclo. |
| nuevo | ## 8. COCO y OPERADOR_STOP_COCO | **OPERADOR_STOP_COCO**: ``` Si D_ckm > D_CKM_THRESHOLD: Δ_r ← Δ_r · (1 − alpha) alpha = _alpha_for(D_ckm) ← monotónicamente decreciente con D_ckm ``` |
| nuevo | ## 8. COCO y OPERADOR_STOP_COCO | `alpha*` ≈ 0.40 — valor robusto en 5/9 casos observados. `_alpha_for(D_ckm)` monotónicamente decreciente: **verificado** 43/43 tests. |
| nuevo | ## 8. COCO y OPERADOR_STOP_COCO | **Armstrong in-vivo** (verificado v32, REG_armstrong_stop_coco_v1.md): - 20/20 evaluaciones con stop_applied=True (seed=42, textos con nodos reales) - α ∈ [0.05, 0.30] verificado - Compresión geométrica de Δ_r confirmada… |
| nuevo | ## 8. COCO y OPERADOR_STOP_COCO | **Nota**: Armstrong con vocabulario ajeno al corpus no dispara STOP. Causa: vocabulario sin anclaje en W activa máximo 1 nodo — nunca hay par candidato a rechazo. Δ_r = 0. |
| nuevo | ## 9. Las siete predicciones — P1–P7 | \| # \| Predicción \| Estado \| N \| \|---\|---\|---\|---\| \| P1 \| c(S) exhibe histeresis macroscópica: incorporar ≠ remover \| **verificado** \| 16, 32, 64 \| \| P2 \| Distribución de cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2… |
| nuevo | ## 9. Las siete predicciones — P1–P7 | **P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. 18 pares negativos diluidos en 2016 pares posibles. La predicción estructural se sostiene; la predicción de magnitud no escal… |
| nuevo | ## 9. Las siete predicciones — P1–P7 | **P6 detalle**: T0 cita T1 a 2.18× frecuencia. T1 tiene mayor cohesión interna (3.05×). Verificado en W_asim_v8h (primera W asimétrica real, votos MTurk fourforums). |
| nuevo | ## 10. k-core y zona crítica | k-core: subconjunto donde cada nodo tiene al menos k vecinos dentro del subconjunto. Umbral de arista: \|W_ij\| ≥ θ. |
| nuevo | ## 10. k-core y zona crítica | Zona crítica identificada en θ ∈ [0.002, 0.007] para W_mixta N=32. |
| nuevo | ## 11. SALAMANCA — criterio de admisión de tensión estructural | ## 11. SALAMANCA — criterio de admisión de tensión estructural |
| nuevo | ## 11. SALAMANCA — criterio de admisión de tensión estructural | Criterio **previo** a la construcción de W_mixta. Detecta si W_pos tiene naturaleza estructuralmente adversarial (partición T0/T1 con cut bajo) antes de introducir pares negativos. |
| nuevo | ## 11. SALAMANCA — criterio de admisión de tensión estructural | Si SALAMANCA detecta estructura adversarial → identificar frontera → candidatos a pares negativos. Si no detecta → W_pos es la respuesta correcta. W_mixta no tiene objeto. |
| nuevo | ## 11. SALAMANCA — criterio de admisión de tensión estructural | **P4 + SALAMANCA = criterio de admisión de tensión estructural**, no de construcción de matriz. |
| nuevo | ## 11. SALAMANCA — criterio de admisión de tensión estructural | Alternativa propuesta: barrer β de alto a bajo, medir separabilidad c(S) interno vs cruzado. β_Néel = β donde separabilidad colapsa. Problema: min-cut requiere semilla T0/T1. Sin semilla: normalized cut espectral. |
| nuevo | ## 12. Temperatura de Néel efectiva vs β_c | β_c = punto crítico ferromagnético (tipo Curie). T_Néel efectiva = β donde T0/T1 dejan de ser distinguibles como subredes. |
| nuevo | ## 12. Temperatura de Néel efectiva vs β_c | Son dos cantidades distintas. T_Néel sería más alta en sistema con interacciones competidoras. Potencial criterio de elicitación de candidatos negativos sin sesgo externo. |
| nuevo | ## 13. Estados epistémicos del proyecto (v32) | ## 13. Estados epistémicos del proyecto (v32) |
| nuevo | ## 13. Estados epistémicos del proyecto (v32) | - **Verificadas**: confirmado experimentalmente bajo condiciones declaradas - **Verificables**: no verificado aún pero el protocolo de verificación existe - **Admisibles**: no verificable, no descartable — el espacio don… |
| nuevo | ## 13. Estados epistémicos del proyecto (v32) | Lo admisible no se cierra. Lo que abre, abre también al automatismo. Lo que cierra, muere. |
| nuevo | ## 14. Condiciones de corpus | - N actual: 32 (W_ckm_corpus_v2) - Mínimo Hopfield para observaciones estadísticamente válidas: ~128 - W_ckm_corpus_v3 pendiente de rebuild con textos v26–v32 - Todos los resultados empíricos sobre W_ckm_corpus_v2 llevan… |
| nuevo | ## 14. Condiciones de corpus | Corpora externos: fourforums (N=32–64), CreateDebate (N=32–64). P1–P7 validadas sobre estos corpora bajo muestreo **uniforme**. Ver §6 sobre incertidumbre metodológica del conteo. |
| nuevo | ## 15. Lo que permanece abierto | - Qué mide realmente `_count_attractors` bajo cada modo - Si el breakpoint n_runs=60→70 es transición de fase o artefacto del modo uniforme - Distribución de σ₀ apropiada para landscapes frustrados con cuencas pequeñas y… |
| nuevo | ## 15. Lo que permanece abierto | *Fuentes primarias: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_Landscape_Driven_Device_v10_2.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_me… |
| nuevo | ## 15. Lo que permanece abierto | *Repo: gadanindelamor/ckm — Agosto 2026* |
| nuevo | ## 16. Paper de referencia más cercano a CKM base | ## 16. Paper de referencia más cercano a CKM base |
| nuevo | ## 16. Paper de referencia más cercano a CKM base | **Aiyappa, Flammini & Ahn. "Emergence of simple and complex contagion dynamics from weighted belief networks." *Science Advances*, 2024.** |
| nuevo | ## 16. Paper de referencia más cercano a CKM base | Único paper encontrado hasta abril 2026 que usa la combinación base de CKM: grafo con pesos W + dinámica tipo Hopfield sobre red de creencias ponderadas. Mapea casi 1:1 con la arquitectura CKM base (W_pos, sin pesos nega… |
| nuevo | ## 16. Paper de referencia más cercano a CKM base | Lo que NO tiene: W_mixta (pesos negativos / energía opuesta / frustración estructural intencional). La diferencia entre Aiyappa et al. y CKM es exactamente W_mixta — lo que no tiene precedente publicado encontrado. |

## v2 → v7

**Se van y no vuelven**

| título | bloque |
|---|---|
| ### W — matriz simétrica de co-ocurrencia | **Propiedad verificada**: W y Δ deben mantenerse separadas. Mezclarlas destruye capacidad de recuperación (0.78 → 0.02). |
| ### W — matriz simétrica de co-ocurrencia | **W es piecewise constant**: inmutable dentro de cada intervalo O_t. Se reconstruye discretamente cuando el corpus cruza umbral. Los saltos son el objeto de estudio; P1–P7 aplican dentro de cada O_t. |
| ### Δ_r — acumulador de rechazos (runtime, MonitorService) | ### Δ_r — acumulador de rechazos (runtime, MonitorService) |
| ### Δ_r — acumulador de rechazos (runtime, MonitorService) | ``` Δ_r : N×N, asimétrica Acumula rechazos del Gatekeeper a lo largo del tiempo W_eff = W + Δ_r ← lo que COCO regula ``` |
| ## 2. Naturaleza del landscape — W_pos vs W_mixta | **W_pos — ferromagnética** (verificado P4, framing propuesto v32): Todos los nodos tienden a alinearse en el mismo atractor. Sin oposición estructural, el sistema colapsa hacia saturación. |
| ## 2. Naturaleza del landscape — W_pos vs W_mixta | **W_mixta — ferrimagnética** (verificado P4, framing propuesto v32): No es antiferromagnética pura. Es fondo ferromagnético (W_pos) más pares negativos selectivos en la frontera T0/T1. Las dos subredes tienen orientación… |
| ## 2. Naturaleza del landscape — W_pos vs W_mixta | **Observación**: CKM usa la función de energía Hopfield y la mecánica de relajación como herramienta computacional. No es una red Hopfield asociativa. Los atractores no son memorias Hebbianas — son mínimos del landscape … |
| ## 3. Coercividad CKM | Dos cruces de c(S)=0 en rama UP: H_c ≈ ρ=0.406 y H_c ≈ ρ=0.586. Entre esos dos puntos: c(S) < 0 en incorporación. |
| ## 4. Nodo tipo-965 | Definición: nodo con in-degree alto (≥ 455× out-degree), out-degree ≈ 0. Pure sostenedor. |
| ## 4. Nodo tipo-965 | **Verificado**: ratio in/out > 455× en nodo tipo-965 del corpus CKM. **Verificado en dos corpora**: fourforums y CreateDebate contienen al menos un nodo de este tipo (P7). **Candidato verificado como bridge**: nodo 965 c… |
| ## 4. Nodo tipo-965 | **Triadas que contienen nodo tipo-965**: coercividad = 0 verificada (Paper §5, hasta n confirmado). |
| ## 6. Conteo de atractores — _count_attractors (COCO) | **Estado incierto**: ningún modo validado como medición correcta de diversidad. Ver REG_situacion_medicion_ago2026_v1.md. El modo uniforme puede medir velocidad de expulsión desde estados iniciales improbables, no divers… |
| ## 7. D_ckm | **Estado incierto**: D_ckm hereda los sesgos de `_count_attractors`. A n_runs fijo, no es invariante al modo de muestreo. case_id=5 cruza el threshold (0.510 → 0.032) cambiando solo la distribución de σ₀. case_id=1 cambi… |
| ## 8. COCO y OPERADOR_STOP_COCO | COCO es un device ODA completo (Observa-Decide-Actúa). No necesita DeviceSkin — necesita campo, no canal. |
| ## 8. COCO y OPERADOR_STOP_COCO | **ODA inductivo** (verificado v32): ``` state_{i+1} = A(D(O(state_i))) ``` No recursivo. No requiere nueva instancia por ciclo. |
| ## 8. COCO y OPERADOR_STOP_COCO | `alpha*` ≈ 0.40 — valor robusto en 5/9 casos observados. `_alpha_for(D_ckm)` monotónicamente decreciente: **verificado** 43/43 tests. |
| ## 8. COCO y OPERADOR_STOP_COCO | **Armstrong in-vivo** (verificado v32, REG_armstrong_stop_coco_v1.md): - 20/20 evaluaciones con stop_applied=True (seed=42, textos con nodos reales) - α ∈ [0.05, 0.30] verificado - Compresión geométrica de Δ_r confirmada… |
| ## 8. COCO y OPERADOR_STOP_COCO | **Nota**: Armstrong con vocabulario ajeno al corpus no dispara STOP. Causa: vocabulario sin anclaje en W activa máximo 1 nodo — nunca hay par candidato a rechazo. Δ_r = 0. |
| ## 9. Las siete predicciones — P1–P7 | \| # \| Predicción \| Estado \| N \| \|---\|---\|---\|---\| \| P1 \| c(S) exhibe histeresis macroscópica: incorporar ≠ remover \| **verificado** \| 16, 32, 64 \| \| P2 \| Distribución de cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2… |
| ## 9. Las siete predicciones — P1–P7 | **P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. 18 pares negativos diluidos en 2016 pares posibles. La predicción estructural se sostiene; la predicción de magnitud no escal… |
| ## 10. k-core y zona crítica | k-core: subconjunto donde cada nodo tiene al menos k vecinos dentro del subconjunto. Umbral de arista: \|W_ij\| ≥ θ. |
| ## 10. k-core y zona crítica | Zona crítica identificada en θ ∈ [0.002, 0.007] para W_mixta N=32. |
| ## 11. SALAMANCA — criterio de admisión de tensión estructural | **P4 + SALAMANCA = criterio de admisión de tensión estructural**, no de construcción de matriz. |
| ## 11. SALAMANCA — criterio de admisión de tensión estructural | Alternativa propuesta: barrer β de alto a bajo, medir separabilidad c(S) interno vs cruzado. β_Néel = β donde separabilidad colapsa. Problema: min-cut requiere semilla T0/T1. Sin semilla: normalized cut espectral. |
| ## 12. Temperatura de Néel efectiva vs β_c | β_c = punto crítico ferromagnético (tipo Curie). T_Néel efectiva = β donde T0/T1 dejan de ser distinguibles como subredes. |
| ## 12. Temperatura de Néel efectiva vs β_c | Son dos cantidades distintas. T_Néel sería más alta en sistema con interacciones competidoras. Potencial criterio de elicitación de candidatos negativos sin sesgo externo. |
| ## 13. Estados epistémicos del proyecto (v32) | Lo admisible no se cierra. Lo que abre, abre también al automatismo. Lo que cierra, muere. |
| ## 14. Condiciones de corpus | - N actual: 32 (W_ckm_corpus_v2) - Mínimo Hopfield para observaciones estadísticamente válidas: ~128 - W_ckm_corpus_v3 pendiente de rebuild con textos v26–v32 - Todos los resultados empíricos sobre W_ckm_corpus_v2 llevan… |
| ## 14. Condiciones de corpus | Corpora externos: fourforums (N=32–64), CreateDebate (N=32–64). P1–P7 validadas sobre estos corpora bajo muestreo **uniforme**. Ver §6 sobre incertidumbre metodológica del conteo. |
| ## 15. Lo que permanece abierto | - Qué mide realmente `_count_attractors` bajo cada modo - Si el breakpoint n_runs=60→70 es transición de fase o artefacto del modo uniforme - Distribución de σ₀ apropiada para landscapes frustrados con cuencas pequeñas y… |
| ## 15. Lo que permanece abierto | *Fuentes primarias: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_Landscape_Driven_Device_v10_2.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_me… |
| ## 16. Paper de referencia más cercano a CKM base | ## 16. Paper de referencia más cercano a CKM base |
| ## 16. Paper de referencia más cercano a CKM base | **Aiyappa, Flammini & Ahn. "Emergence of simple and complex contagion dynamics from weighted belief networks." *Science Advances*, 2024.** |
| ## 16. Paper de referencia más cercano a CKM base | Lo que NO tiene: W_mixta (pesos negativos / energía opuesta / frustración estructural intencional). La diferencia entre Aiyappa et al. y CKM es exactamente W_mixta — lo que no tiene precedente publicado encontrado. |

**Se van y vuelven después**

| vuelve en | título | bloque |
|---|---|---|
| v15 | # DEFS_CKM_estado_actual_v2.md | *Ago 2026 — gadanin.delamor + Claude Sonnet 4.6* *Documento de referencia — definiciones actuales del modelo CKM* *v2: agrega P5, P6, mapeo magnético, SALAMANCA, coercividad, ODA, Armstrong, tres estados epistémicos* |
| v14 | ### Δ — matriz asimétrica de orientación (estática, corpus) | Usada exclusivamente por el Gatekeeper (C3, criterio M.M). No entra en dinámica de relajación. **Δ estático ≠ Δ_r**. |
| v9 | ### c(S) — función de cohesión | Mide alineación entre estado σ y pesos W. No mide "cohesión del campo" en sentido conceptual — mide la fracción del suelo W que está activa en σ. |
| v15 | ## 3. Coercividad CKM | Coercividad de W_pos: nula (sin resistencia al cambio de estado). Coercividad de W_mixta: mayor — la tensión estructural introduce resistencia. |
| v9 | ## 7. D_ckm | **D_CKM_THRESHOLD = 0.40** — umbral para disparo de OPERADOR_STOP_COCO. |
| v20 | ## 13. Estados epistémicos del proyecto (v32) | ## 13. Estados epistémicos del proyecto (v32) |
| v19 | ## 13. Estados epistémicos del proyecto (v32) | - **Verificadas**: confirmado experimentalmente bajo condiciones declaradas - **Verificables**: no verificado aún pero el protocolo de verificación existe - **Admisibles**: no verificable, no descartable — el espacio don… |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | # DEFS_CKM_estado_actual_v7.md | *Ago 2026 — gadanin.delamor + Claude Sonnet 4.6* *Documento de referencia — definiciones actuales del modelo CKM* *v7: §11 — Modo Boltzmann para σ₀ propuesto (TASK para Code Opus) *v4: reorganización arquitectónica (pre-… |
| nuevo | # PARTE I — MODELO ESTÁTICO (pre-servicios CKM) | # PARTE I — MODELO ESTÁTICO (pre-servicios CKM) |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | ``` W_pos : N×N, simétrica (W = Wᵀ) W_ij = conteo_coocurrencia(i, j) / n_textos ≥ 0 ``` |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **W es piecewise constant por diseño del instrumento**: CKM reconstruye W cuando el corpus cruza un umbral (`min_texts`). El campo semántico subyacente es dinámico continuo — el carácter piecewise es un artefacto del ins… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **Fase de acumulación**: antes de que el corpus alcance `min_texts`, los textos son aprobados por el Gatekeeper pero W aún no existe (o no ha sido reconstruida). En esta fase las evaluaciones del Gatekeeper no tienen W_p… |
| nuevo | ## 2. Δ — matriz de orientación (corpus estático) | Usada por el Gatekeeper (criterio M.M, C3). **El Gatekeeper evalúa contra W del momento de ingesta** — que a partir del primer nodo admitido es siempre **W vieja**: la última versión construida antes del texto actual. W_… |
| nuevo | ## 2. Δ — matriz de orientación (corpus estático) | Si W no ha sido construida aún (fase de acumulación), M.M no tiene referencia. **Δ estático ≠ Δ_r**. |
| nuevo | ## 2. Δ — matriz de orientación (corpus estático) | *Desfasaje — abierto, prioridad baja: W vieja es condición permanente de operación.* |
| nuevo | ## 2. Δ — matriz de orientación (corpus estático) | *Cuándo ocurre rebuild (verificado en corpus_service.py y ckm_monitor.py):* - *Automático: `ingest()` llama `_rebuild()` cuando `len(texts) >= min_texts` — criterio de volumen.* - *Estructural: `should_rebuild(d_ckm_hist… |
| nuevo | ## 3. c(S) — función de cohesión | **La herramienta vs. el uso (distinción crítica):** - Primera línea: nombra la herramienta — la función de energía Hopfield, tomada como formalismo computacional. - Segunda línea: nombra el uso en CKM — medir la alineaci… |
| nuevo | ## 3. c(S) — función de cohesión | Cuando la energía decrece (relajación Hopfield), la cohesión crece. La dinámica Hopfield es el motor; CKM lee el resultado en la dirección opuesta. |
| nuevo | ## 3. c(S) — función de cohesión | **Función analítica unificada** (verificado, v27 — cierre de H1/H2/H3): |
| nuevo | ## 3. c(S) — función de cohesión | Donde `μ_W` escala con composición del corpus y `r` es el factor de alineación medible en tiempo real. Los tres HOLDINGs H1/H2/H3 son proyecciones observables de esta función, no límites independientes. |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | Aplica funciones de activación Hopfield sobre W_pos. Selección de nodos según distribución uniforme. Garantiza convergencia a mínimo local de energía. Sin ciclos. Sin aprendizaje Hebbiano. |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | **Garantía formal de convergencia — Lyapunov/LaSalle:** |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | Con W simétrica y actualización asíncrona, la función de energía de Hopfield |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | es una función de Lyapunov del sistema. Cada actualización asíncrona satisface dV ≤ 0 en cada paso. El conjunto invariante máximo L en Z = {σ : dV = 0} son exactamente los mínimos locales de V. Por el Teorema de Invarian… |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | Consecuencia operativa: con actualización **asíncrona** y W **simétrica**, los ciclos de período 2 son **imposibles**. `relax()` devuelve siempre un elemento de L — un mínimo local de V. Antes implícito en el código; aho… |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | *Fuente: Agama Santiago, M. "Análisis de estabilidad de las redes neuronales de Hopfield utilizando funciones de Lyapunov y el Teorema de LaSalle." Licenciatura en Matemáticas Aplicadas, UTM Mixteca, 2026. §2 (Lyapunov/L… |
| nuevo | ### hopfield.py — asincrónica (usada en P1–P4) | **Qualifier**: P1–P4 son válidas bajo relajación asincrónica con: - Selección de nodos según distribución **uniforme** - **Seed = 42 fija** — para permitir comparación entre corridas - **n_runs**: no hay problema del col… |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | ### coco.py → _relax — sincrónica (usada en servicios, P5) |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | **max_iter = 200: abierto.** No hay análisis de por qué 200 es suficiente (o insuficiente) para W_mixta con frustración. Puede producir ciclos de período 2 — devuelve el último estado, que puede no ser mínimo de energía. |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | **Consecuencia verificada**: P1–P4 (hopfield.py, async) y P5 (COCO, sync) usan instrumentos distintos. Sus resultados no son directamente comparables en términos de dinámica de relajación. |
| nuevo | ## 5. P1–P4 — Predicciones del modelo estático | Validadas sobre W_pos estática con hopfield.py (asincrónico) + k-core percolation + Belief Propagation. Sin aprendizaje Hebbiano. Sin servicios CKM. |
| nuevo | ## 5. P1–P4 — Predicciones del modelo estático | **P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. Causa: dilución por nodos tipo B — ver §7. |
| nuevo | ## 5. P1–P4 — Predicciones del modelo estático | **Condición de validez — W_pos estática únicamente:** P1–P4 son propiedades de W_pos estática tal como fueron formuladas. Evaluarlas sobre W dinámica (W_eff, W reconstruida tras rebuild, W en evolución) no es verificar P… |
| nuevo | ## 5. P1–P4 — Predicciones del modelo estático | Evaluar lazos de histeresis sobre la evolución de W dinámica es posible y legítimo, pero es una nueva predicción — no puede ser P1 por orden cronológico del proyecto: P1 fue formulada y verificada antes de que existieran… |
| nuevo | # PARTE II — VALIDACIÓN EXTERNA (corpus adversarial) | # PARTE II — VALIDACIÓN EXTERNA (corpus adversarial) |
| nuevo | ## 6. P5–P7 — Corpus FourForums y CreateDebate | Primera aparición del corpus adversarial. Validación externa a los corpora de calibración. |
| nuevo | ## 6. P5–P7 — Corpus FourForums y CreateDebate | **P5** usa `_count_attractors` de COCO (relajación sincrónica) — instrumento distinto a P1–P4. |
| nuevo | ## 6. P5–P7 — Corpus FourForums y CreateDebate | **P7 y triadas**: del análisis de P7 emerge la estructura de triadas de pares negativos — grupos de nodos en tensión estructural genuina donde el nodo tipo-965 actúa como sostenedor. Las triadas son el antecedente del cr… |
| nuevo | ## 6. P5–P7 — Corpus FourForums y CreateDebate | **Nodo tipo-965**: ratio in/out > 455× (paper). *Nota: REG_mapeo_magnetico_ckm_v1 menciona > 100× — verificar cuál es el valor correcto en corpus actual.* |
| nuevo | # PARTE III — MODELO DINÁMICO (servicios CKM) | # PARTE III — MODELO DINÁMICO (servicios CKM) |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | Análisis de distribución de frecuencias marginales en N=32 (CV=0.944, razón max/min=102×): |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | \| Grupo \| Nodos \| fi \| Pares \| \|---\|---\|---\|---\| \| A \| 16 \| ≥ 0.064 \| núcleo correlacionado \| \| B \| 16 \| < 0.064 \| nodos tardíos / baja densidad \| |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | \| Par \| μ_W obs \| mean(fi·fj) \| ratio \| derivable \| \|---\|---\|---\|---\|---\| \| BB \| 0.000523 \| 0.000510 \| 1.025 \| ✓ (nodos B ≈ independientes estadísticos) \| \| AA \| 0.016122 \| 0.065599 \| 0.246 \| ✗ (nú… |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | **Cierres operativos** (verificado, v27): - **H3 cerrado**: μ_W no generaliza entre N porque cambia la proporción A/B, no N per se. - **H2 cerrado**: dilución P4 en N=64 es consecuencia de agregar nodos tipo B (μ_W → 0).… |
| nuevo | ## 8. W_mixta — ferrimagnética | **Ferromagnética (W_pos)**: todos los nodos tienden al mismo atractor. Sin resistencia. **Ferrimagnética (W_mixta)**: fondo ferromagnético + pares negativos selectivos en frontera T0/T1. Momento resultante no se cancela.… |
| nuevo | ## 8. W_mixta — ferrimagnética | **W_pos y W_mixta pertenecen a regímenes cualitativamente distintos.** |
| nuevo | ## 8. W_mixta — ferrimagnética | Diferencias estructurales entre Aiyappa et al. 2024 y CKM — no reducibles a W_mixta: |
| nuevo | ## 8. W_mixta — ferrimagnética | 1. **Uso de arquitectura Hopfield**: CKM maximiza energía sin regla de aprendizaje de patrones. Estudia diversidad del landscape — no recuperación de memorias. 2. **Δ — matriz de orientación**: asimetría direccional como… |
| nuevo | ## 8. W_mixta — ferrimagnética | **Separación estricta de capas** (verificado): mezclar W y Δ destruye capacidad (0.78 → 0.02). |
| nuevo | ## 9. Δ_r — acumulador de rechazos (runtime) | ``` Δ_r : N×N, simétrica por construcción (monitor_service.py L112-114) W_eff = W + Δ_r ← lo que COCO regula ``` |
| nuevo | ## 9. Δ_r — acumulador de rechazos (runtime) | **Nota**: Δ_r es simétrica, no asimétrica. El par (i,j) nunca se genera sin (j,i) — la simetría es forzada en la acumulación. Esto la distingue de Δ (estática, asimétrica). La confusión entre ambas explica la etiqueta in… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **n_runs hardcoded = 200 en modo operacional**: abierto. Insuficiente para coupon-collector en corpus grandes. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Modo uniforme** (default): P(nodo i) = 1/N. **Modo ponderado** (experimental, no cableado): pᵢ = \|W_eff\|ᵢ / Σ\|W_eff\|. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **L como objeto que se mide — fundamento formal:** |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Los atractores de Hopfield son los mínimos locales de V(σ) = −½σᵀWσ — el conjunto L del Teorema de LaSalle. `_count_attractors()` es un **estimador de \|L\|** por Monte Carlo sobre condiciones iniciales. Las cuencas de a… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Por qué uniforme sesga:** en W anisótropa (nodo tipo-965, ratio 455×), las cuencas tienen volúmenes muy distintos. Muestreo uniforme concentra σ₀ en zonas sin estructura → expulsión rápida hacia cuencas dominantes → el… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Por qué ponderado da menos (dirección invertida, 2 observaciones consistentes):** ponderar por \|W_eff.sum(axis=1)\| concentra σ₀ en los nodos de mayor conectividad — que residen en la cuenca dominante. No amplía cober… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Modo Boltzmann** (propuesto, no implementado — TASK para Code Opus): |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Tercer modo de muestreo de σ₀, termodinámicamente fundamentado. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | con: ρ* = densidad óptima de P4 (≈ 0.5 para W_base, N=32) μ_W = media de W sobre pesos no-nulos N = número de nodos → β_c ≈ 13.83 (para N=32, μ_W=0.004519, ρ*=0.5) ``` |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Distribución de σ₀: ``` P(σᵢ = 1) = 1 / (1 + exp(−2 · β_c · hᵢ)) donde hᵢ = Σⱼ Wᵢⱼ σⱼ (campo local de nodo i) ``` |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Implementación propuesta: calentamiento con `relax(beta=β_c)` de `hopfield.py` (n_warmup pasos) seguido del relax determinístico habitual. σ₀ queda en la distribución de Boltzmann — respeta la anisotropía de W antes de r… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Diferencia con uniforme y ponderado: ambos son estáticos. Boltzmann usa el campo local — es muestreo por importancia respecto a la geometría real del landscape. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Estado**: propuesto. β_c calculable desde magnitudes del proyecto. n_warmup óptimo: abierto — depende del tiempo de mezcla del paisaje. No implementado. No evaluado. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Verificación de condiciones Lyapunov sobre W_eff — código:** |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Dos condiciones requeridas por Lyapunov/LaSalle: W_eff simétrica, diagonal cero. Ambas verificadas en `monitor_service.py`: |
| nuevo | ## 11. Conteo de atractores — _count_attractors | *Simetría de Δ_r* — acumulación explícita en ambas direcciones (`monitor_service.py` líneas 112–114): ```python for i, j in rejected: self._Delta_r[i, j] += 1 self._Delta_r[j, i] += 1 ``` Δ_r = Δ_rᵀ por construcción. W e… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | *Diagonal cero de Δ_r* — `_rejected_pairs` genera solo pares con j > i (`monitor_service.py` líneas 232–233): ```python for i in range(len(declared)): for j in range(i + 1, len(declared)): # j > i siempre ``` El par (i, … |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Las dos condiciones necesarias para que la garantía Lyapunov/LaSalle aplique a `_count_attractors(W_eff)` están satisfechas por construcción del código, no por convención. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **H_STOP falsificada** (v27, sweep t_stop × α): D_ckm no predice ratio_max. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **Hipótesis revisada (abierta)**: ``` Efectividad_STOP = f(A_pre) A_pre < A0 → STOP expande paisaje (ratio > 1) A_pre = A0 → STOP neutro alpha* ≈ 0.40 robusto para A_pre < A0 (5/9 casos) ``` |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | α=1.0 (sin STOP) nunca óptimo. α=0.0 (reset total) solo óptimo en casos específicos. |
| nuevo | ## 13. Zonas de operación G1/G2/G3 | \| Garantía \| Zona \| c(S) (80% CI) \| r (80% CI) \| Significado \| \|---\|---\|---\|---\|---\| \| G1 \| Zona crítica ρ ∈ [0.4, 0.8] \| [−0.000332, +0.001310] \| [−0.074, +0.290] \| Monitor operativo \| \| G2 \| Atracto… |
| nuevo | ## 13. Zonas de operación G1/G2/G3 | Gap discriminante G1/G2: [+0.001310, +0.001941] — detectable en tiempo real por r = c(S)/μ_W. |
| nuevo | ## 13. Zonas de operación G1/G2/G3 | COCO requiere: medir μ_W empíricamente al inicio de sesión (no constante universal), monitorear r en tiempo real. |
| nuevo | ## 14. Coercividad CKM | Del lazo P1 (hopfield.py, N=32, n=200 secuencias): dos cruces de c(S)=0 en rama UP a ρ=0.406 y ρ=0.586. Intervalo frustrado, no punto. |
| nuevo | ## 14. Coercividad CKM | **Definición operativa** (REG_mapeo_magnetico_ckm_v1): valor de ρ donde c(S) cruza cero en rama de incorporación — análogo al campo coercitivo magnético. |
| nuevo | ## 14. Coercividad CKM | Coercividad W_pos: nula. Coercividad W_mixta: mayor. Estado: **verificado** geométricamente; interpretación magnética: **propuesto**. |
| nuevo | ## 15. Temperatura de Néel efectiva (≈ Nielsen ≈ TEER) | Criterio de elicitación de pares negativos sin sesgo editorial: 1. Construir W_pos. 2. Barrer β de alto a bajo. 3. β_Néel = β donde separabilidad T0/T1 colapsa. 4. Pares en clusters opuestos antes del colapso → candidato… |
| nuevo | ## 15. Temperatura de Néel efectiva (≈ Nielsen ≈ TEER) | Relacionado con SALAMANCA (ver §16). Ver NOTAS_proxima_sesion_paper_v11.md, Tema 4. |
| nuevo | ## 17. Escala y N | **N=128 (mínimo Hopfield asociativo)**: aplica a memorias Hebbianas con patrones no correlacionados (α_c ≈ 0.138N). **No aplica a CKM** — CKM no almacena memorias. El mínimo operativo de CKM es abierto y depende de compo… |
| nuevo | ## 17. Escala y N | Al aumentar N en CKM, el comportamiento va en dirección opuesta al Hopfield clásico. El límite real está dado por la densidad del lenguaje natural humano. En implementación persistente, N podría ser del orden de miles. |
| nuevo | ## 18. Lo que permanece abierto | - Qué mide realmente `_count_attractors` bajo cada modo - Prevalencia de ciclos período-2 en relajación sincrónica en W_mixta - max_iter=200 y n_runs=200: justificación ausente - CONVERGENCIA_SLOPE para modo ponderado: d… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **El corpus es simultáneamente datos y proceso**: N=32 construido desde conversaciones autor–Claude Sonnet. El corpus es el laboratorio y el sujeto. Si el modelo describe bien ese corpus, no queda claro si describe el es… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **α_c con patrones correlacionados**: el límite α_c ≈ 0.138 asume no-correlación. Los nodos CKM son altamente correlacionados (estructura A/B verificada). α_c es una propiedad del corpus, no del modelo. Tensión sostenida… |
| nuevo | ## 20. Referencia externa más cercana | *Fuentes: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_v11.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_medicion_ago2026_v1.md, REG_mapeo_magn… |

## v7 → v8

**Se van y no vuelven**

| título | bloque |
|---|---|
| ### coco.py → _relax — sincrónica (usada en servicios, P5) | **max_iter = 200: abierto.** No hay análisis de por qué 200 es suficiente (o insuficiente) para W_mixta con frustración. Puede producir ciclos de período 2 — devuelve el último estado, que puede no ser mínimo de energía. |
| ## 12. COCO y OPERADOR_STOP_COCO | **Armstrong in-vivo** (verificado): 20/20 STOPs, α ∈ [0.05, 0.30], Fracción_rec ≥ 1.0. STOP no produce pérdida — produce restauración o expansión. |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | **Ciclos de período 2 — estabilidad orbital, no deficiencia (v8):** |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | El modo sincrónico puede producir ciclos de período 2. Esto no es inestabilidad — es **estabilidad orbital** (atractor de ciclo límite). El sistema es acotado (2^N estados posibles), determinista y perfectamente predecib… |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | \| Modo \| Conjunto invariante M \| Tipo de estabilidad \| \|---\|---\|---\| \| Asincrónico \| Mínimos locales de V (puntos fijos) \| Estática \| \| Sincrónico estándar \| Órbitas de período 2 \| Orbital / periódica \| \… |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | **LaSalle sincrónico:** con W simétrica y diagonal cero, mapeada bajo función de Lyapunov adaptada para ejecución sincrónica, el cambio de energía total entre pasos sucesivos está acotado estructuralmente. LaSalle garant… |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | *Fuente: Predictibilidad_orbital.md — gadanin.delamor, Sep 2026.* |
| nuevo | ### coco.py → _relax — sincrónica (usada en servicios, P5) | **Consecuencia operativa para `_count_attractors`:** cuando `_relax` sincrónico converge a una órbita de período 2 (A → B → A → B), devuelve el último estado antes de alcanzar max_iter. Ese estado es un punto arbitrario … |
| nuevo | ## 10. D_ckm | **Dos instancias de D_ckm — distinción explícita (v8, NOTA_armstrong v2):** |
| nuevo | ## 10. D_ckm | ``` D_ckm_coco ← COCO, conduce decisiones de STOP D_ckm_monitor ← MonitorService panel, herramienta de observación ``` |
| nuevo | ## 10. D_ckm | Ambas usan la misma fórmula `(A0 − A_actual) / A0` pero operan sobre rutas distintas: |
| nuevo | ## 10. D_ckm | - **`D_ckm_monitor`**: `_combine_W_Delta` normaliza `Δ_r / max(Δ_r)`. STOP aplica `α·Δ_r` — escalar uniforme. La normalización cancela el escalar por construcción. Resultado: D_ckm_monitor **algebraicamente ciego** a la … |
| nuevo | ## 10. D_ckm | - **`D_ckm_coco`**: opera sobre W_eff con Δ_r sin normalización interna relativa — refleja el efecto real de STOP sobre el campo navegable. |
| nuevo | ## 10. D_ckm | **Asimetría de calibración:** D_CKM_THRESHOLD = 0.40 calibrado con W_mixta (AMP=40). En corpus W_pos de baja densidad (WARMUP_TEXTS), el piso estructural = (174−64)/174 = 0.632 > 0.40 → el umbral no activa STOP de manera… |
| nuevo | ## 10. D_ckm | **Pendiente de implementación:** alias `D_ckm_monitor` en MonitorService (TASK_dckm_monitor_alias_v1) — no sustituye `D_ckm` para preservar legibilidad de JSOLs históricos. |
| nuevo | ## 10. D_ckm | **Dirección de exploración (propuesta):** diferencia `D_ckm_coco − D_ckm_monitor` como señal de cuándo COCO tiene efecto real vs. opera sobre Δ_r sin cambiar el campo navegable. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Qualifier tie-breaking — acotado a corpus específicos (v8, NOTA_armstrong v2):** |
| nuevo | ## 11. Conteo de atractores — _count_attractors | La dominancia de tie-breaking (factor ~3: 174 → 60 atractores) se verificó en corpus WARMUP_TEXTS. |
| nuevo | ## 11. Conteo de atractores — _count_attractors | \| corpus \| N \| densidad \| valores no-nulos \| h=0 en primer paso \| \|---\|---:\|---:\|---\|---:\| \| WARMUP_TEXTS \| 20 \| 0.126 \| {0.5, 1.0} \| 33.6% \| \| W_ckm_corpus_v2.json \| 32 \| 0.756 \| 95 distintos, max … |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Condiciones de aplicación de tie-breaking dominante: - densidad < ~0.15 (corpus esparcido) - pocos valores distintos no-nulos (pesos discretos) - fracción h=0 en primer paso > ~30% |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **No transfiere a W_ckm_corpus_v2.json**: con ese corpus count(W) = 5 con la regla actual. El factor ~3 desaparece. El tie-breaking no es propiedad general de `_count_attractors` — es información sobre la estructura del … |
| nuevo | ## 11. Conteo de atractores — _count_attractors | La regla "conserva σ cuando h=0" es la que garantiza convergencia (Lyapunov/LaSalle, §4). No se toca. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **frac_rec — dos métricas distintas (v8, NOTA_armstrong v2):** - `frac_rec` del REG_destruccion_recuperacion_v1 = max_α[A_post(α)]/A0 — el máximo sobre α en barrido controlado. Este valor ≥ 1.0 en todos los casos observa… |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | No son comparables directamente. "STOP no produce pérdida" se sostiene en su contexto original (barrido max_α, REG_destruccion_recuperacion_v1). La corrida Armstrong no refuta ni confirma esta propiedad para el régimen W… |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **Efecto COCO por régimen de W (v8, NOTA_armstrong v2):** - **W_pos baja densidad (WARMUP_TEXTS)**: efecto real en primeros ~3 STOPs (delta_A = +34, +31, +24). Se agota cuando Δ_r cae por debajo de ~0.05 — estado absorbe… |
| nuevo | ## 18. Lo que permanece abierto | - Qué mide realmente `_count_attractors` bajo cada modo - Qué produce `_count_attractors` cuando el paisaje contiene órbitas de período 2: el estado devuelto es un punto arbitrario de la órbita — posible inflación o inco… |

## v8 → v9

**Se van y no vuelven**

| título | bloque |
|---|---|
| ## 5. P1–P4 — Predicciones del modelo estático | Evaluar lazos de histeresis sobre la evolución de W dinámica es posible y legítimo, pero es una nueva predicción — no puede ser P1 por orden cronológico del proyecto: P1 fue formulada y verificada antes de que existieran… |
| ## 11. Conteo de atractores — _count_attractors | **Estado**: propuesto. β_c calculable desde magnitudes del proyecto. n_warmup óptimo: abierto — depende del tiempo de mezcla del paisaje. No implementado. No evaluado. |
| ## 12. COCO y OPERADOR_STOP_COCO | **Efecto COCO por régimen de W (v8, NOTA_armstrong v2):** - **W_pos baja densidad (WARMUP_TEXTS)**: efecto real en primeros ~3 STOPs (delta_A = +34, +31, +24). Se agota cuando Δ_r cae por debajo de ~0.05 — estado absorbe… |
| ## 18. Lo que permanece abierto | - Qué mide realmente `_count_attractors` bajo cada modo - Qué produce `_count_attractors` cuando el paisaje contiene órbitas de período 2: el estado devuelto es un punto arbitrario de la órbita — posible inflación o inco… |

**Se van y vuelven después**

| vuelve en | título | bloque |
|---|---|---|
| v13 | ## 11. Conteo de atractores — _count_attractors | Distribución de σ₀: ``` P(σᵢ = 1) = 1 / (1 + exp(−2 · β_c · hᵢ)) donde hᵢ = Σⱼ Wᵢⱼ σⱼ (campo local de nodo i) ``` |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## 0. Dominio CKM | **CKM is a formal model for knowledge field dynamics in multi-device AI systems.** |
| nuevo | ## 0. Dominio CKM | Multi-agent AI interaction produces a shared knowledge field that individual device outputs and pairwise similarity scores do not capture. CKM measures the structural geometry of this field. |
| nuevo | ## 0. Dominio CKM | El dominio son las interacciones entre devices. Cualquier propiedad, predicción u observación CKM se evalúa en relación a este dominio. La comprensión de una parte es en relación al dominio — no al universo de todos los … |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | ## OP. Analytics global del instrumento — snapshot W y dinámico |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | *Sección de referencia. Cubre el instrumento en sus dos formas: W snapshot (análisis estático, P1–P4) y runtime dinámico (servicios, COCO). Cualquier afirmación en este documento debe rastrearse a una fila de esta tabla,… |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | **Forma:** S = snapshot (W estático) · D = dinámico (runtime) · S+D = ambas |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | \| Objeto \| Forma \| Técnica \| Qué mide \| Representación estructural en CKM \| \|---\|---\|---\|---\|---\| \| **fi** \| S \| Frecuencia marginal: fracción de textos donde aparece el nodo i \| Presencia individual de u… |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | **Distinciones que no viajan entre objetos:** |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | - fi alto ≠ nodo importante. fi alto en corpus adversarial = concepto disputado que aparece en múltiples stances por separado — no necesariamente en el mismo texto. - Cluster (analytics.py) ≠ stance. Los clusters agrupan… |
| nuevo | ## 5. P1–P4 — Bootstrap formal del modelo estático | P1–P4 son el **bootstrap formal de CKM**: las predicciones que establecen que el modelo tiene las propiedades estructurales necesarias para ser válido en su dominio. No son el propósito del proyecto — son su fundamento. … |
| nuevo | ## 5. P1–P4 — Bootstrap formal del modelo estático | Algunas predicciones tienen demostración matemática directa; otras son verificadas empíricamente. La distinción importa: |
| nuevo | # PARTE II — OBSERVACIONES EN CORPUS ADVERSARIAL (dominio acotado) | # PARTE II — OBSERVACIONES EN CORPUS ADVERSARIAL (dominio acotado) |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy acotado) |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | **Relevancia para el proyecto: baja.** P5–P7 son observaciones que emergieron al aplicar el instrumento CKM sobre corpora de debate adversarial externo (CreateDebate gun control, FourForums gun control). Son derivados de… |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | **Dominio de validez estricto**: corpus adversariales de postura fija. No son características generales del modelo CKM. No son propiedades del modelo — son comportamientos observados en un tipo de corpus muy específico. … |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | El dominio de CKM son interacciones entre devices — con sus respectivos VPs, no reducibles a polaridad binaria. El trabajo IAP (Sonnet + Code + delamor) opera con al menos 3 stances distintos. delamor es participante con… |
| nuevo | ## 8. W_mixta — ferrimagnética | **Build de W_mixta — marcadores de oposición (corpus_service.py v2):** Cada texto es ruteado por presencia de marcadores de oposición (_OPPOSITION_MARKERS, ES+EN). Sin marcador → pares suman a pos_counts. Con marcador → … |
| nuevo | ## 8. W_mixta — ferrimagnética | ``` W = (pos_counts − neg_counts) / max(\|pos − neg\|) Rango: [−1, +1] ``` |
| nuevo | ## 8. W_mixta — ferrimagnética | `force_w_pos=True`: flag de desarrollo únicamente — saltea el ruteo, todos los pares van a pos_counts. La W resultante queda marcada en traza (`causal_event=rebuild_debug_force_w_pos`). No es estado alcanzable en operaci… |
| nuevo | ## 8. W_mixta — ferrimagnética | **Calibración W_mixta — build y rebuilds (v9):** D_CKM_THRESHOLD (0.40 default) debe calibrarse contra W_mixta, no contra W_pos. Condiciones: - **Build inicial**: calibrar D_CKM_THRESHOLD al construir W_mixta por primera… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **D_ckm cuantizado en paisajes pequeños (REG_wmixta_forzado_paso3_v1):** con A0 entero pequeño, D_ckm = (A0−A)/A0 toma valores discretos con pasos grandes. El umbral 0.40 puede caer entre dos valores alcanzables — COCO n… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | con: ρ* = 0.5 (identidad algebraica: relax(−σ) = −relax(σ)) N = número de nodos μ_W = media de W sobre pesos no-nulos → método: beta_c_corpus() en coco.py ``` |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Parámetros: - `sampling_mode`: "uniform" \| "weighted" \| "boltzmann" — configurable por corrida - `n_warmup`: default = N. Óptimo: **abierto** — depende del tiempo de mezcla del landscape. - β_c se computa una vez por l… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Trazabilidad: el panel registra `sampling_mode` y `n_warmup` por evaluación — cada decisión de STOP es trazable al modo que produjo el D_ckm que la desencadenó (REG_stochastic_eval_v2). |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Estado**: implementado. Evaluado en WARMUP_TEXTS (W_pos). Evaluación en W_mixta (caso09_run2, corpus IAP): pendiente — ver §12. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **COCO no es opcional.** Es componente constitutivo del modelo — no una característica adicional ni un módulo activable. Un sistema IAP sin COCO no es CKM en operación; es el instrumento sin su mecanismo de regulación. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | Natural (W_mixta, 56 pesos negativos): A0=26–32 (n_runs=50). 42 STOPs en 3 modos, ningún delta_A negativo, mínimo +11. Campo cicla — cruza umbral en ambas direcciones. Δ_r acotada 62–76 vs 632 sin thermostat. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | Forzado (W_pos del mismo corpus): A0=3–4. 7 STOPs en un solo modo (weighted), delta_A máximo +1. Uniform y boltzmann no cruzaron el umbral. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **Mecanismo verificado:** la diferencia en STOPs pasa por A0 y la grilla. W_mixta produce A0 ~10× mayor (n_runs=150: 58 vs 4) — grilla fina, umbral 0.40 alcanzable. W_pos produce A0=3–4 — umbral cae entre valores que la … |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **Cautela:** el forzado no es W_pos genérica — es la W_pos de un corpus con tensión subyacente no codificada. La comparación no está pareada en escala de operación (A0~30 vs A0~4). |
| nuevo | ## 13. Zonas de operación G1/G2/G3 | **μ_W y r — siempre al inicio de sesión, nunca como constante (v9):** μ_W NO es una constante universal — cambia con la composición A/B del corpus y con N. El factor r = c(S)/μ_W pierde discriminación si μ_W es aproximad… |
| nuevo | ## 18. Lo que permanece abierto | Los abiertos se organizan por plano. Ver también §X sobre planos distintos. |
| nuevo | ## 18. Lo que permanece abierto | **Deuda técnica registrada**: - Desfasaje Gatekeeper / W vieja: condición permanente de operación, no bug |
| nuevo | ## X. Planos distintos: validez matemática y verificación operacional | ## X. Planos distintos: validez matemática y verificación operacional |
| nuevo | ## X. Planos distintos: validez matemática y verificación operacional | La validez matemática de CKM (Lyapunov/LaSalle, separación W/Δ, garantías de convergencia) está demostrada independientemente de cualquier corpus particular. La demostración es formal — no depende de que el experimento W… |
| nuevo | ## X. Planos distintos: validez matemática y verificación operacional | La verificación operacional (¿qué produce `_count_attractors` en W_mixta? ¿cuántos STOPs tienen efecto real?) es empírica y corpus-dependiente. Aporta información sobre el comportamiento del instrumento en condiciones es… |
| nuevo | ## X. Planos distintos: validez matemática y verificación operacional | **Confundir estos planos produce errores en ambas direcciones:** - Exigir verificación operacional en corpus específico como condición de validez matemática: incorrecto. - Asumir que validez matemática implica comportami… |
| nuevo | ## X. Planos distintos: validez matemática y verificación operacional | P5–P7 son verificaciones operacionales en un corpus muy específico. Si P5–P7 no se reproducen en otro corpus, nada cambia al modelo. Si `_count_attractors` en W_mixta con Boltzmann muestra o no invarianza orbital, nada c… |

## v9 → v10

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | **CKMlandscapeConfig** (nombre propuesto, propuesta previa " CKMDynamicConfig"). No es una bolsa de constantes. Es el contrato vivo del instrumento: porta N actual, μ_W medido en esta sesión, θ_W calculado (no hardcodead… |
| nuevo | ## EL Modelo Conceptual | **NodeExtractor**. El cartógrafo. Decide qué existe — los N nodos que se convierten en el espacio. Todo lo que viene después depende de lo que declaró. Corre lazy por rebuild. Es el más silencioso y el de mayor impacto a… |
| nuevo | ## EL Modelo Conceptual | **CorpusService**. El guardián de W. Recibe textos, construye y reconstruye la matrix de pesos, gestiona el ciclo de vida de W como snapshot. W es piecewise constant por diseño del instrumento — no propiedad del campo. A… |
| nuevo | ## EL Modelo Conceptual | **Gatekeeper**. El evaluador de admisión. Decisión binaria antes de que algo entre al campo. C1–C4, M.M en C3. Diseñado para el dominio de capacidades declaradas por devices — su dominio de validez sobre nodos de corpus … |
| nuevo | ## EL Modelo Conceptual | **MonitorService**. El observador impartial. Recibe estado del campo, relaja, acumula lo que el campo expulsa durante la relajación (Δ_r). Registra sin decidir. D_ckm_monitor es algebraicamente ciego a STOP por cancelaci… |
| nuevo | ## EL Modelo Conceptual | **COCO**. El regulador. Nace con W al momento del rebuild, opera sobre ese espacio congelado. Ve D_ckm_coco (con magnitud de Δ_r), decide compresión. No admite — regula lo que ya entró. La tensión con Monitor no está res… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | --- ## SLAs — acuerdos sin burlar encapsulamiento |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | NodeExtractor → CorpusService: "devuelvo nodos y co-ocurrencias del corpus. Corro una vez por rebuild. Lo que devuelvo define el espacio N." |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | CorpusService → Monitor: "te doy W. Cuando reconstruyo, W puede cambiar de shape — N puede ser distinto. Hoy no te aviso. Eso es un gap." |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | CorpusService → COCO: "te instancio con la W del momento. Tu ciclo de vida es el mío." |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | Monitor → COCO: "acumulo Δ_r. Es mío. Puedo darte acceso de lectura. No tenés derecho de escritura sobre mi estado interno." |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | COCO → Monitor: hoy escribe sobre Δ_r de Monitor directamente. Eso viola el SLA que debería existir. COCO debería operar sobre una copia o sobre su propia representación de Δ_r — no sobre el estado de otro servicio. |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | CKMlandscapeConfig → todos: "soy la fuente de verdad de calibración. Si no me consultás con N y μ_W actuales antes de evaluar, tu umbral es inválido." |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | Gatekeeper → CorpusService (propuesto): "evalúo antes de que el nodo entre. Necesito W_vieja. Sin W no puedo aplicar C1." |

## v10 → v10_1

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | **Monitor** es dueño de `Δ_r_pares` — los rechazos que el campo produce durante la relajación. Lógica propia, independiente de cualquier otro servicio. Nadie escribe ahí. |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | **COCO** tiene su propio `Δ_r_compresiones` — la historia de lo que comprimió, por ciclo de vida. Objeto distinto. No es el Δ_r de Monitor. COCO no toca el estado de Monitor. |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | Con esa separación, la ceguera de Monitor no es un mecanismo que hay que implementar ni un efecto que hay que cancelar matemáticamente — es una consecuencia natural de que los dos objetos nunca se tocan. Monitor no ve la… |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | La función `CancelarMatemáticamente(coco_compresion)` sería necesaria solo si los dos Δ_r estuvieran mezclados. Con separación limpia, no existe el problema que esa función resolvería. |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | **β por ciclo de vida de COCO.** β nace con la W que construyó esa instancia de COCO. Si W cambia — N nuevo, pesos nuevos — esa β ya no tiene referencia válida. La instancia muere con el rebuild. CKMlandscapeConfig puede… |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | Esto también reescribe D3. No es una divergencia sobre encapsulamiento solamente — es que los dos objetos aún no existen como objetos distintos en el código. `Δ_r_pares` y `Δ_r_compresiones` son el mismo nombre hoy. |

## v10_1 → v12

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | **FabricationService.** Detecta cohesión fabricada — fi=0.0 sobre contenido desconocido es correcto (el campo no puede rechazar lo que no conoce). No tiene instanciador activo. Su definición completa espera condiciones p… |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **Armstrong in-vivo** (verificado): OPERADOR_STOP_COCO aplicado 20/20 veces, α ∈ [0.05, 0.30]. |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | *Tensión registrada: la declaración "no opcional" puede ser cierre prematuro de una tensión abierta entre Monitor y COCO. Marcada como abierta en PROPUESTA v5.* |

## v12 → v13

**Se van y no vuelven**

| título | bloque |
|---|---|
| ## EL Modelo Conceptual | **MonitorService**. El observador impartial. Recibe estado del campo, relaja, acumula lo que el campo metaboliza durante la relajación (Δ_r). Registra sin decidir. D_ckm_monitor es algebraicamente ciego a OPERADOR_STOP_C… |
| ## SLAs — acuerdos sin burlar encapsulamiento | COCO → Monitor: hoy escribe sobre Δ_r de Monitor directamente. Eso viola el SLA que debería existir. COCO debería operar sobre su propia representación de Δ_r — no sobre el estado de otro servicio. |
| ### coco.py → _relax — sincrónica (usada en servicios, P5) | ``` Para cada iteración: h = W_eff @ σ ← todos los nodos simultáneamente σ ← sign(h) convergencia: np.allclose(σ_nuevo, σ) Cap: max_iter = 200 ``` |
| ### coco.py → _relax — sincrónica (usada en servicios, P5) | **Consecuencia operativa para `_count_attractors`:** cuando `_relax` sincrónico converge a una órbita de período 2 (A → B → A → B), devuelve el último estado antes de alcanzar max_iter. Ese estado es un punto arbitrario … |
| ## 9. Δ_r — acumulador de metabolización (runtime) | **Nota**: Δ_r es simétrica, no asimétrica. El par (i,j) nunca se genera sin (j,i) — la simetría es forzada en la acumulación. Esto la distingue de Δ (estática, asimétrica). La confusión entre ambas explica la etiqueta in… |
| ## 11. Conteo de atractores — _count_attractors | **n_runs hardcoded = 200 en modo operacional**: abierto. Insuficiente para coupon-collector en corpus grandes. |
| ## 11. Conteo de atractores — _count_attractors | con: ρ* = 0.5 (identidad algebraica: relax(−σ) = −relax(σ)) N = número de nodos μ_W = media de W sobre pesos no-nulos → método: beta_c_corpus() en coco.py ``` |
| ## 11. Conteo de atractores — _count_attractors | Parámetros: - `sampling_mode`: "uniform" \| "weighted" \| "boltzmann" — configurable por corrida - `n_warmup`: default = N. Óptimo: **abierto** — depende del tiempo de mezcla del landscape. - β_c se computa una vez por l… |
| ## 11. Conteo de atractores — _count_attractors | Trazabilidad: el panel registra `sampling_mode` y `n_warmup` por evaluación — cada decisión de OPERADOR_STOP_COCO es trazable al modo que produjo el D_ckm que la desencadenó (REG_stochastic_eval_v2). |
| ## 11. Conteo de atractores — _count_attractors | **Estado**: implementado. Evaluado en WARMUP_TEXTS (W_pos). Evaluación en W_mixta (caso09_run2, corpus IAP): pendiente — ver §12. |

**Se van y vuelven después**

| vuelve en | título | bloque |
|---|---|---|
| v15 | ## 11. Conteo de atractores — _count_attractors | Implementación: calentamiento estocástico (`n_warmup` pasos con `relax(beta=β_c)` de `hopfield.py`) desde σ₀ aleatorio, seguido del relax determinístico habitual. σ₀ queda en la distribución de Boltzmann — respeta la ani… |
| v15 | ## 11. Conteo de atractores — _count_attractors | Diferencia con uniforme y ponderado: ambos son estáticos. Boltzmann usa el campo local — muestreo por importancia respecto a la geometría real del landscape. |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | **MonitorService**. El observador impartial. Recibe estado del campo, relaja, acumula lo que el campo metaboliza durante la relajación (`Δ_r_pares`). Registra sin decidir. D_ckm_monitor es ciego a OPERADOR_STOP_COCO — no… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | COCO → Monitor: D3 implementado. COCO porta `Δ_r_compresiones` — objeto propio, historia de compresiones por ciclo de vida. No escribe en el estado de Monitor. La separación es la que garantiza la independencia del obser… |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | ``` relax_orbit(sigma, W_eff, max_iter=200): detecta órbita exacta (período 1 o 2) tiebreak GOLES: conserva σ cuando h=0 devuelve (sigma_final, period, steps, estado_seleccionado) Cap: max_iter = 200 ``` |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | *Fuente: convergencia orbital — teorema de invarianza de LaSalle (estándar, ver Agama Santiago 2026 para la derivación formal). Aplicación al instrumento CKM: Predictibilidad_orbital.md — gadanin.delamor, Sep 2026.* |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | **Consecuencia operativa para `_count_attractors` — resuelta por GOLES:** `relax_orbit` detecta la órbita completa. Cuando h=0 el nodo conserva σ (regla "conserva σ" — garantiza determinismo: misma W, mismo σ₀, mismo see… |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | **Prevalencia de órbitas verificada:** ~70% de las trayectorias en corpora operacionales N=20 terminan en órbitas de período 2. Velocidad: 87× vs relax sin detección de órbita (REG_orbitas_conjuntos_invariantes_v1). |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | *Nota (Sep 2026): los valores de fi arriba corresponden al corpus W_ckm_corpus_v2.json prior a la corrección del bug de extracción de pares (CorpusService, commit 5aa3504). Con el corpus corregido: CV=1.08, max/min=68.6×… |
| nuevo | ## 8. W_mixta — ferrimagnética | **Precondición de dominio** (REG_unidad_texto_saturacion_v1 §5, decidido): el ruteo por marcadores léxicos asume que el corpus fue elicitado con posiciones que se oponen por diseño. En corpus de autor único o de coordina… |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | ``` Δ_r_pares : N×N, simétrica por construcción (Monitor, monitor_service.py L112-114) Δ_r_compresiones : N×N, objeto propio de COCO (coco.py, desde D3 — Sep 2026) |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | W_eff_monitor = W + Δ_r_pares ← lo que Monitor relaja y mide W_eff_coco = W + Δ_r_compresiones ← lo que COCO regula ``` |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | **D3 implementado (Sep 2026):** `Δ_r_pares` es de Monitor — nadie escribe en él excepto Monitor. `Δ_r_compresiones` es de COCO — historia de compresiones por ciclo de vida, objeto distinto. OPERADOR_STOP_COCO opera sobre… |
| nuevo | ## 10. D_ckm | **D_ckm no converge en signo bajo variación de seed o n_runs** (REG_seleccion_nodos_desempate_v1 §8, verificado sobre caso09 bootstrap 12 y 16): el signo puede invertirse cambiando solo n_runs de 50 a 1000 sobre la misma… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **n_runs hardcoded = 200 en modo operacional** (actualizado a 1000 en MonitorService, Sep 2026): con n_runs=50, N_eff queda ~32% por debajo del valor convergente. Con n_runs=1000, N_eff converge ±2% respecto a 5000 runs … |
| nuevo | ## 11. Conteo de atractores — _count_attractors | Tercer modo de muestreo de σ₀, termodinámicamente fundamentado. Con `relax_orbit` y n_runs≥1000, el muestreo uniforme converge en masas de cuenca. El warmup de Boltzmann **ya no es necesario** para la convergencia: la ve… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | *Estado: implementado. El modo uniforme con relax_orbit es el camino convergente verificado.* |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | *Post-D3 (Sep 2026): OPERADOR_STOP_COCO opera sobre `Δ_r_compresiones` — el objeto propio de COCO. No modifica `Δ_r_pares` de Monitor.* |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | *Nota post-D3 (Sep 2026): el hallazgo "Δ_r acotada 62-76" medía `Δ_r_pares` de Monitor en el sistema pre-D3, donde COCO escribía en ese objeto. Post-D3, Monitor acumula `Δ_r_pares` sin cota desde COCO — COCO opera sobre … |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **W_mixta sin estado nulo**: el procedimiento `_has_opposition(text)` siempre encuentra marcadores en textos suficientemente largos — no tiene salida nula. Ninguna W_mixta construida hasta la fecha pudo haber resultado W… |

## v13 → v14

**Se van y no vuelven**

| título | bloque |
|---|---|
| ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | **Prevalencia de órbitas verificada:** ~70% de las trayectorias en corpora operacionales N=20 terminan en órbitas de período 2. Velocidad: 87× vs relax sin detección de órbita (REG_orbitas_conjuntos_invariantes_v1). |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | **CorpusService**. El guardián de W. Recibe textos, construye y reconstruye la matrix de pesos, gestiona el ciclo de vida de W como snapshot. W es piecewise constant por diseño del instrumento — no propiedad del campo. A… |
| nuevo | ## EL Modelo Conceptual | **Gatekeeper**. El evaluador de admisión. Decisión binaria antes de que algo entre al campo. C1–C4, M.M en C3. Diseñado para el dominio de capacidades declaradas por devices — su dominio de validez sobre nodos de corpus … |
| nuevo | ## EL Modelo Conceptual | *La formulación anterior tenía un propósito.* Decir *"ausente de `services/`"* (v9–v13) registraba que **el mecanismo declarado no estaba siendo ejercido**: el PAPER daba C1–C4 como la implementación vigente, y esa imple… |
| nuevo | ## EL Modelo Conceptual | **Selección de nodos ≠ admisión** *(v14 — REG_seleccion_nodos_desempate_v1 §7; Informe v31 §60.2: "la distinción portero/elicitación es arquitectónicamente crítica")*. Elegir los N nodos por TF-IDF es **elicitación de lo… |
| nuevo | ## EL Modelo Conceptual | **Plantear la admisión en `services/` es válido — con precondiciones** *(v14, decisión delamor)*. La pregunta no está descartada: llevar un criterio de admisión al runtime es legítimo. Lo que está decidido es el **orden*… |
| nuevo | ## EL Modelo Conceptual | \| # \| qué \| por qué es precondición del siguiente \| dónde está medido \| \|---\|---\|---\|---\| \| 1 \| **Corpus extensos** \| con 3–24 textos el dato no distingue: TF-IDF sale de conteos enteros y el espacio de punt… |
| nuevo | ## EL Modelo Conceptual | Recién con los tres, evaluar admisión sobre nodos de corpus mide algo. Antes, mide el instrumento. *(Y sigue siendo otro dominio que el de `mcp_adapter.py`: la transferencia del criterio es lo que se estaría probando.)* |
| nuevo | ## EL Modelo Conceptual | **De dónde saldría el volumen** *(v14, declarado por delamor)*. El paso 1 no está esperando una medición: está esperando corpus. **Los casos disponibles hoy no generan el volumen necesario** — la serie IAP de devices lle… |
| nuevo | ## EL Modelo Conceptual | Eso abre una pregunta de dominio que conviene no saltear: el dominio declarado de CKM son las **interacciones entre devices bajo M.M.** (§0). Un corpus de agentes puede estar adentro de ese dominio o ser un dominio acota… |
| nuevo | ## EL Modelo Conceptual | **El corpus de informes no es el sustituto** *(v14, decisión delamor)*. Tiene volumen —870 párrafos, 15.557 palabras— y por eso tienta usarlo para simular la acumulación y los rebuilds por criterio. **No sirve para eso.*… |
| nuevo | ## EL Modelo Conceptual | **Para qué sirve:** para **comparar determinadas características** del instrumento — activación por texto, saturación de pares distintos, efecto de la unidad de texto, contrafácticos con `force_w_pos`. Eso es lo que `REG… |
| nuevo | ## EL Modelo Conceptual | **Consecuencia sobre un abierto:** medir la saturación como **trayectoria** bajo ingesta incremental —que es el abierto que ese REG deja— necesita un corpus del dominio, no los informes. Con ellos se mediría la acumulaci… |
| nuevo | ## EL Modelo Conceptual | **Y un corpus encontrado tampoco alcanza** *(v14, delamor)*. Se buscaron corpus de agentes hace meses y puede que hoy haya más, pero **un corpus que ya existe se ingesta como replay**, y una secuencia predeterminada no e… |
| nuevo | ## EL Modelo Conceptual | **Lo que sí daría dato del dominio con volumen es un caso diseñado, no un corpus encontrado:** una interacción con objetivos y tareas que exijan **coordinación sostenida** entre devices —coordinación que no se pueda salt… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | CorpusService → Monitor: "te doy W. Cuando reconstruyo, W puede cambiar de shape — N puede ser distinto. **No te aviso: te dejo preguntar.** `w_change_since(sha, nodes)` te dice si cambiaron N, los nodos o los pesos." *(… |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | Esto también reescribe D3. No era una divergencia sobre encapsulamiento solamente: era que los dos objetos no existían como objetos distintos en el código. **Desde `7df4a72` (Sep 2026) existen** — `Δ_r_pares` en Monitor,… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **Acumulación por criterio del dato (Sep 2026, verificado — REG_seleccion_nodos_desempate_v1 §4):** `min_texts` deja de ser el único criterio. Con la regla de desempate, si el dato no distingue —todo el pool empatado y s… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **N deja de ser fijo (verificado, ídem §5):** con la regla de desempate, N puede superar `top_k` (empatados conservados más términos nuevos por margen) o caer por debajo. Medido: N ∈ [9, 41] con `top_k`=32; en un corpus … |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | ## 1.1 La rama de extracción — lo que decide qué existe antes de que haya medición |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | *Sección nueva (v14). NodeExtractor y `CorpusService._rebuild` deciden qué nodos y qué pares existen. Todo lo que este documento mide ocurre después de esa decisión, y durante Sep 2026 se verificaron cuatro condiciones d… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **a) Pares por texto entre nodos globales** *(corregido — `5aa3504`, REG_hipotesis_distancia_contextual_v4 §1–§2)*. `_rebuild` hacía **dos** extracciones: una global para elegir los N nodos, y otra **por texto** para rut… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | \| caso09, bootstrap 12 \| global \| lo que entraba a W \| \|---\|---:\|---:\| \| pares distintos \| 299 \| 161 — **46% perdidos** \| \| co-ocurrencias \| 425 \| 189 — **55% perdidas** \| |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | Corregido: `accumulate` devuelve `pairs_by_text` entre nodos globales y `_rebuild` rutea con eso, sin re-extraer. **Cambia todas las W construidas por CorpusService.** Lo medido antes vale en su marco. |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **b) Nodos aislados** *(REG_hipotesis_distancia_contextual_v3 §2, v4 §2)*. Un nodo aislado tiene su fila de W entera en cero: su campo local es siempre 0, conserva su valor, y con `a` aislados cada atractor acoplado apar… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **c) σ por una sola rama** *(corregido — `7bf485b`, REG_hipotesis_distancia_contextual_v4 §7)*. `evaluate` construía σ_prompt por substring mientras W se construía con el analizador de `accumulate`: dos criterios distint… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **d) Stopwords e idioma** *(REG_unidad_texto_saturacion_v1 §4.3, verificado, **no corregido**)*. `_STOPWORDS` es la unión NLTK-es + NLTK-en + sklearn-en, y la unión **suma los falsos positivos de las tres listas en vez d… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **d.1) Nunca hubo mapeo de nodos en corpus bilingüe — abierto hasta hoy** *(v14, delamor)*. `day` y `día` son el caso limpio: un solo concepto, dos grafías, y para el extractor **dos términos que compiten por el top_k**.… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **d.2) Familia de palabras: probado, sin efecto** *(v14, delamor)*. Agrupar variantes morfológicas en familias de palabras **se probó y no cambiaba la prueba ni sus resultados**. Queda registrado para que no se vuelva a … |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **e) Saturación de pares distintos** *(REG_unidad_texto_saturacion_v1 §3, §4)*. La cantidad que ordena el colapso del paisaje no es la densidad de W ni la tensión, sino cuántos de los pares posibles **nunca ocurren**. Co… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | *Estado: (a) y (c) verificados y corregidos; (b) frecuencia verificada; (d) verificado, no corregido; (e) verificado como medición, criterio propuesto.* |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | **Prevalencia de órbitas — verificada y dependiente del corpus** *(corregido en v14)*. La misma tabla de REG_orbitas §2 da los tres números: |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | \| corpus \| N \| trayectorias que quedan en órbita \| \|---\|---:\|---:\| \| WARMUP_TEXTS \| 20 \| 141/200 — **70.5%** \| \| caso09 natural \| 20 \| 136/200 — **68%** \| \| `W_ckm_corpus_v2` \| 32 \| 3/200 — **1.5%** \| |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | El "~70%" vale para esos dos corpus N=20, **no para el corpus operativo del proyecto**, que es N=32 y da 1.5%. Versiones anteriores lo enunciaban como *"corpora operacionales"*, que suena general y no lo es. Velocidad: 8… |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | *Nota (Sep 2026) — **corregida en v14**: la partición A/B de arriba (CV=0.944, max/min=102×) **no se reproduce midiendo `W_ckm_corpus_v2.json` directamente**: da CV=1.08, max/min=68.6×, mediana 0.020, y sólo 5 nodos con … |
| nuevo | ## 7. Estructura bimodal A/B y función unificada | *Lo que sí depende de `5aa3504`: toda W construida por `CorpusService` cambió (§1.1a). Si `W_ckm_corpus_v2.json` fue construida por ese camino, la partición requiere recalibración; si vino de otro pipeline, no. No verifi… |
| nuevo | ## 10. D_ckm | *(Post-D3: el Δ_r de esta fórmula es `Δ_r_pares` para `D_ckm_monitor` y `Δ_r_compresiones` para `D_ckm_coco`. Son dos campos distintos desde `7df4a72` — ver §9.)* |
| nuevo | ## 10. D_ckm | **La "d" y D_contextual — lo que se mostró** *(v14)*. Se **mostró**, no se demostró. Lo que hay es esto y nada más: |
| nuevo | ## 10. D_ckm | - `REG_d_contextual_temporal_v1` (Mayo 2026) operacionaliza `D_contextual(t) = [A(0) − A(t)] / A(0)`, que es la definición de D_ckm letra por letra. Desde mayo los dos nombres designan el mismo objeto computado, en dos d… |
| nuevo | ## 10. D_ckm | Eso es lo mostrado. **No demuestra que la entropía de trayectorias accesibles y un cociente de conteos guarden una relación formal**, y que H sea H₂ sobre masas es una elección que la formulación de mayo no fijó. Una exp… |
| nuevo | ## 10. D_ckm | El rótulo arrastra una consecuencia igual: la *d* viene de D_contextual, que es una distancia. Leer D_ckm positivo como *"degradación"* es interpretación agregada al nombre, no propiedad de la cantidad. |
| nuevo | ## 10. D_ckm | - **`D_ckm_monitor`**: opera sobre `W + Δ_r_pares`, con `_combine_W_Delta` normalizando `Δ_r / max(Δ_r)`. **Post-D3 es ciego a las compresiones de COCO porque nunca recibe ese objeto** — separación, no cancelación (ver M… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **`_count_attractors` no nombra una función: nombra varias** *(v14, declarado por delamor)*. El nombre se conservó **por regresión** —para no romper tests ni la lectura de JSONLs históricos— mientras la implementación ca… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | **Precisión de REG_orbitas §4, no incorporada hasta v14:** lo estima **por defecto** —los terminales son estados de L, y sólo se ven las fases que las colas alcanzaron— y **no estima el número de órbitas**. Son dos canti… |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **Free will en IAP** *(v14, delamor — anotado a pedido)*. Los devices **no reaccionan solamente a eventos `on_message`**. Pueden interactuar cuando lo deciden, sin turnos, y todos ven todo. Tres condiciones que lo sostie… |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | - **Sin turnos, y broadcast.** Todo mensaje publicado se entrega a todos los devices conectados, sin ruteo ni destinatario. Nadie tiene asignado cuándo le toca. - **Loop propio, reloj propio.** `AutonomousDevice` corre s… |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | *Estado hoy:* la fase O se entra con un mensaje nuevo ajeno (`_observe(client, message)`; el trigger se filtra para que nunca sea propio). El loop propio **habilita** decidir sin ese disparador; los skins actuales no lo … |
| nuevo | ## 12. COCO y OPERADOR_STOP_COCO | **ODA sin auto-observación no aporta nada** *(v14, delamor)*. El ciclo O→D→A no es la contribución: viene del game loop del BE Framework (2023–2024). Lo que lo vuelve otra cosa es la **auto-observación** —y el intento—, … |
| nuevo | ## 18. Lo que permanece abierto | **Plano matemático / estructural** (afecta al modelo): - H2 (A0 vs A_actual bajo ponderación): sin respuesta verificada - Figura R13 (A∪B, 45.2%): metodología lista, no ejecutado - SALAMANCA y Néel: operacionalización pe… |
| nuevo | ## 18. Lo que permanece abierto | **Plano operacional / calibración** (afecta al instrumento, no a la validez matemática): - Calibración W_mixta build/rebuild: pendiente (§8) - Implementación alias D_ckm_monitor en MonitorService: pendiente (TASK_dckm_mo… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **El rótulo no es determinista cuando se sostienen tensiones** *(v14, delamor)*. Mantener una tensión abierta tiene un costo, y el costo lo pagan los nombres. `_count_attractors` es el caso medido: el nombre se conservó … |
| nuevo | ## 19. Tensiones metodológicas constitutivas | La alternativa —renombrar cada vez que cambia la función, que es lo prolijo del método tradicional— haría el rótulo determinista. **Es un intercambio deliberado, no un descuido:** determinación del nombre contra continui… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | *Renombrando se pierde la traza*, y no en el sentido de que sea más incómoda de leer: **los paneles históricos quedan huérfanos de referente.** Los números sobreviven y lo que los produjo deja de estar nombrado en ningún… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | *Y lo que se gana es coherencia fabricada* — en el sentido técnico que el proyecto le da al término. Con un nombre por comportamiento, ningún documento puede quedar desfasado y **ninguna discrepancia es exhibible**. Eso … |
| nuevo | ## 19. Tensiones metodológicas constitutivas | De ahí se sigue lo que da vuelta la intuición de ingeniería: **el desfasaje documento/código es el observable que el método tradicional suprime.** Que un documento quede atrás es la señal de que el objeto se movió. Renom… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | 1. **Toda afirmación sobre qué mide X lleva fecha, o no dice nada.** "Qué mide `_count_attractors`" no tiene respuesta sin la versión. 2. **El desfasaje entre documento y código es estructural al método, no descuido de r… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **El proxy devuelve un número siempre; el objeto no** *(v14 — REG_unidad_texto_saturacion_v1 §5.3, declarado)*. La misma forma aparece cuatro veces, siempre con el proxy del lado medible: |
| nuevo | ## 19. Tensiones metodológicas constitutivas | \| se quiso medir \| se midió \| \|---\|---\| \| tensión estructural \| ocurrencias de "pero" (`_has_opposition`) \| \| la unidad del campo \| la unidad tipográfica (párrafo, página) \| \| frecuencia del concepto \| frec… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | En los cuatro casos nada falla y todo sigue dando resultado — por eso la sustitución no se nota. Lo que la hace visible no es un test: es tener un corpus donde la respuesta correcta es *nada*. |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **Sesgo de destino en inferencia** *(v14 — REG_hipotesis_distancia_contextual_v4 §6, declarado por delamor)*. `bootstrap = 12` se eligió **por el resultado**: era el punto donde D_ckm cruzaba el umbral, o sea donde el in… |
| nuevo | ## 20. Referencia externa más cercana | *Fuentes v14 (Sep 2026): REG_hipotesis_distancia_contextual_v2 (la "d" es distancia; identidad con D_masa_cuencas), v3 (d(σ) ejecutado; nodos aislados), v4 (mecanismo de la extracción; σ por una rama; sesgo declarado), R… |

## v14 → v15

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## 0. Dominio CKM | **Dos frases, dos órdenes** *(v15 — delamor, 8 oct: "por eso inventaron los órdenes; sólo es miopía")*. |
| nuevo | ## 0. Dominio CKM | - **Orden de la teoría.** *"El modelo no tiene dominio. Los dominios son interpretaciones del modelo. El dominio de M.M lo da su propia definición: declaraciones de funciones y de eventos (IAID 2024)."* (delamor, 6 oct).… |
| nuevo | ## 0. Dominio CKM | Ninguna anula a la otra; cada una tiene su juez. El primer borrador de la v15 las había leído en un mismo plano y las había puesto como "tensión abierta": esa miopía fue de Opus. |
| nuevo | ## 0. Dominio CKM | **Consecuencia.** Todo resultado de este documento vale en una interpretación declarada. Llevarlo a otra —los conceptos de un corpus, las declaraciones de M.M, un corpus adversarial— es otra pregunta: **qué hipótesis usó… |
| nuevo | ## EL Modelo Conceptual | *(v15: **existe y es fuente** — `services/ckm_landscape_config.py`; TASK_CKMlandscapeConfig_v3 cerrada en `44af68a`.)* Cada campo se ubica según **qué lo hace cambiar**: - **medido** —cambia si y sólo si cambia `w_versio… |
| nuevo | ## EL Modelo Conceptual | La config **no es una foto de una W: es la traza de los ciclos por los que pasó.** La inmutabilidad pasa del objeto a la traza (I1): la config gana ciclos, no los edita. **Monitor abre el ciclo** (`17b6421`). `n_runs = 1… |
| nuevo | ## EL Modelo Conceptual | *(v15: el criterio de extracción —`top_k`, `ngram_max`, stopwords, `token_pattern`, `TOL_EMPATE`, desempate por precedente— va en un **bloque propio, `NodeExtractorConfig`**, no en la Config de W (delamor, 8 oct): la ext… |
| nuevo | ## EL Modelo Conceptual | *(v15: **ya no aloja a COCO** — `1e8d267`, CP4 de TASK_monitor_coco_ciclo_orbita_v2. `corpus.coco` queda deprecada y devuelve `None`. "Aloja la instancia de COCO nacida con cada rebuild" es traza: hasta el CP4 CorpusServ… |
| nuevo | ## EL Modelo Conceptual | *(v15, delamor 6 oct — FICHAS §1.)* **El Gatekeeper es un juez, no un portero.** Dicta una **sentencia binaria — válida / no válida — con fundamentos**. No abre puertas, no admite y **no va en la puerta**: es un criterio… |
| nuevo | ## EL Modelo Conceptual | *(v15: ese caso tiene forma propuesta — TASK_canal_iap_clock_iniciativa_v2, CP3: conseguir entradas para la fiesta de presentación del CKM **antes de que se acaben**. La condición es que queden entradas; baja cuando otro… |
| nuevo | ## EL Modelo Conceptual | *(v15 — TASK_monitor_coco_ciclo_orbita_v2, CERRADA, 284/284.)* Monitor **mide sobre la órbita**, no sobre la fase que cae en `max_iter` (§4). Cada par declarado activo queda en una de tres clases, sin promediar: **acepta… |
| nuevo | ## EL Modelo Conceptual | *(v15: **COCO renace con el ciclo que abre Monitor**, no con el rebuild de CorpusService (CP2b, CP4). Al nacer: baseline fijado con Δ_r en cero, así que W_eff = W (CP3 punto 3); `landscape_history` **vacío**, porque la h… |
| nuevo | ## EL Modelo Conceptual | *(v15: pasó de `services/` a `process/` — `f8e0783`, 5 oct.)* |
| nuevo | ## EL Modelo Conceptual | **Firma_CKM** *(v15 — no figuraba en las DEFS; FICHAS §6)*. Certifica **traza, no contenido**: `{sha256(W_momento), D_ckm(t), temp_signal, n_agentes, timestamp, sha256(Δ_r acumulado)}`, sin texto ni nombres no declarados… |
| nuevo | ## EL Modelo Conceptual | **¿Servicio a quién?** *(v15 — delamor, 6 oct: "services son servicio a alguien")*. De los archivos de `services/`, **tres sirven a alguien de afuera** y llegan a los participantes por el canal: Monitor, Firma y COCO. Co… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | CorpusService → COCO: "te instancio con la W del momento. Tu ciclo de vida es el mío." *(v15: ya no vale. Desde el CP4, CorpusService no instancia a COCO. Vigente: **Monitor → COCO: "abro el ciclo; nacés con él"** — base… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | CKMlandscapeConfig → todos: "soy la fuente de verdad de calibración. Si no me consultás con N y μ_W actuales antes de evaluar, tu umbral es inválido." *(v15: lo que porta es `sampling_mode`, `n_runs`, `seed`, `scale` y l… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | Gatekeeper → CorpusService (propuesto): "evalúo antes de que el nodo entre. Necesito W_vieja. Sin W no puedo aplicar C1." *(v15: choca con "no va en la puerta" (delamor, 6 oct). Queda como traza de una propuesta que la f… |
| nuevo | ### Definicion `Δ_r_pares y Δ_r_compresiones` Reencuadra D3 | *(v15: hay un tercer objeto, `Δ_r_torsion`, de Monitor, que **no entra a W_eff** — Modelo Conceptual y §9. Y "β por ciclo de vida de COCO" ya es así en el código: COCO renace con el ciclo, §12.)* |
| nuevo | ## N. Nombres — rótulo, objeto y fecha *(nueva en v15, sin número para… | ## N. Nombres — rótulo, objeto y fecha *(nueva en v15, sin número para conservar §0–§20)* |
| nuevo | ## N. Nombres — rótulo, objeto y fecha *(nueva en v15, sin número para… | *Por §19, el nombre no determina el objeto: lo determina el par (nombre, fecha). Esta tabla **no renombra nada en el código**: declara qué objeto nombra cada rótulo y desde cuándo. Donde hay que decidir, dice [delamor].* |
| nuevo | ## N. Nombres — rótulo, objeto y fecha *(nueva en v15, sin número para… | \| rótulo \| dónde \| objeto que nombra \| desde \| estado \| \|---\|---\|---\|---\|---\| \| **metabolizado** \| DEFS v11+ \| par declarado activo que el campo **rechaza y absorbe**: en σ, la relajación no sostiene la ac… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **Qué es W** *(v15 — delamor, 6 oct; `claude/sesion_06oct2026_definiciones_W` §1)*. - **W es una matriz** N×N de relaciones entre pares de nodos. El valor de cada celda es el peso de la relación (en el corpus, la co-ocur… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | *Sobre los títulos de las Partes:* la v14 decía "pre-servicios" y "servicios CKM". Ese corte es cronológico —abril contra mayo a julio—, no el criterio. La v15 titula por régimen de W y deja el título viejo entre parénte… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **f) El criterio de extracción no deja huella** *(v15 — FICHAS §5, leído en el código el 7 oct)*. El estado JSON de `CorpusService` lleva `n_nodes`, `min_texts`, `w_sha` y `rebuild_suspendido`, pero **no** el criterio co… |
| nuevo | ### landscape_engine.py → relax_orbit — sincrónica (usada en servicios… | **La órbita es el objeto** *(v15 — TASK_monitor_coco_ciclo_orbita_v2, CP0 a CP2)*. Toda medición dentro del ciclo se hace sobre la **órbita completa** —las dos fases, sin orden, como el `frozenset` de `relax_orbit`—, no … |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | *(v15 — reescrita; pedido de delamor: "redactalo, incluilo en la v15". La v14 decía **verificado** en las cuatro. Esa tabla se conserva al final de esta sección, entera, como traza: es el suelo desde el que se vio lo que… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **Qué son.** Las cuatro predicciones falsables del Modelo Híbrido (`docs/CKM_Modelo_Hibrido.md`, abril 2026: Hopfield + k-core + BP sobre una W). En el Orden BABEL propuesto son E1–E4; como los prefijos no están decidido… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | \| # \| Predicción \| Estado v15 \| Plano \| Por qué \| \|---\|---\|---\|---\|---\| \| P1 \| c(S) exhibe histéresis: incorporar ≠ remover \| **no testeable sobre una W snapshot con W ≥ 0** \| matemático \| Con W ≥ 0 no h… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **Una sola premisa cierra P1 y P4.** `force_w_pos=True` decide las dos respuestas antes de correr. No son dos propiedades mal medidas: es **una premisa medida dos veces**. **Y tres de las cuatro piden tiempo** —P1 histor… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | *Fuentes:* `P1P4/BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1.md` (5 oct; **borrador**, fuera de `registers/`, entra con el OK de delamor); el candado `experiments/CERRADO_LEER_ANTES_ckm_p1p4_module.md` (`eddb4b0`);… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **Lo que no dice.** No dice que P1–P4 sean falsas. Dice que una W snapshot no negativa **no es condición para preguntarlo**. Cierra P1 y P4 sobre W_pos snapshot; **no cierra P1–P4 como propiedades del Modelo Híbrido**. |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **Conciliación con la verificación del 4 oct** *(Opus, v15 — quedó como tensión el 5 oct: "conciliar `eddb4b0` con la PROPUESTA v27")*. El INFORME_verificacion_P1_P4_v2 (4 oct) dio P1 "verificada como propiedad del model… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | *Esta conciliación es lectura de Opus, y espera la de delamor.* |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **De dónde venía el "verificado".** Los números de abril (`readme/EXPERIMENTS.md`, Informe v32 §64.4) se produjeron con `exp_p1_histeresis.py` y `ckm_viz_v1.py`, que **nunca entraron al repo** (`find` sobre todo el árbol… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **Lo que queda abierto, y es otra pregunta: P1–P4 sobre W dinámica.** Las mismas cuatro, sobre una W que evoluciona. Ahí la frustración puede **aparecer de la dinámica** en vez de ponerse a mano con una W_mixta: la regla… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | No hay resultado de abril al que llegar; la TASK se escribe de cero. **Sin identificador** hasta que se formulen como premisas propias de W dinámica (Orden BABEL, regla 3: una premisa no cruza modelos). **[delamor]** |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | **Lo que decía la v14** *(traza, sin cambios)*: |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | > P1–P4 son el **bootstrap formal de CKM**: las predicciones que establecen que el modelo tiene las propiedades estructurales necesarias para ser válido en su dominio. No son el propósito del proyecto — son su fundamento… |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | *(v15)* **Adversarial no es un modelo: es el signo de W** (delamor, 6 oct), y puede aparecer en los dos regímenes. Esta Parte se conserva como dominio acotado. **Babel entre documentos:** la v14 las llama *observaciones*… |
| nuevo | # PARTE III — W DINÁMICA: EL MUNDO QUE SE MUEVE *(v14: MODELO DINÁMICO… | # PARTE III — W DINÁMICA: EL MUNDO QUE SE MUEVE *(v14: MODELO DINÁMICO, servicios CKM)* |
| nuevo | ## 8. W_mixta — ferrimagnética | *(v15 — réplica de la Fig. 5, §20: en Aiyappa cambian los pesos; en CKM, sobre una W, cambian los estados. La energía de Aiyappa es triádica (Heider); la de CKM, por pares (Hopfield). Pariente, no gemelo.)* |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | **v15 — qué entra a `Δ_r_pares`** (delamor, 8 oct, CP3 1a; `ef1bc33`, `monitor_service.py` L218–L240). **Sólo los pares rechazados en las dos fases** de la órbita (§4; en el código, `expulsados` — §N). `Δ_r_torsion` —los… |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | ``` W_eff_monitor = W + Δ_r_pares ← sólo rechazados en las dos fases Δ_r_torsion : N×N, simétrica, de Monitor — no entra a W_eff ``` |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | **Ciclo de vida.** Al cambiar W, Monitor descarta Δ_r y abre un ciclo nuevo en la Config; COCO renace con él con Δ_r en cero, así que **W_eff = W al nacer** (§12). Las líneas citadas arriba (L112–114) son de septiembre: … |
| nuevo | ## 10. D_ckm | **v15 — la fórmula cambió** (`dabd1ed`, 5 oct; `registers/REG_d_ckm_formula_canonica_v1.md`; decidido por delamor el 4 oct): |
| nuevo | ## 10. D_ckm | - La forma lineal `(A0 − A) / A0` **deja de ser lo que calculan Monitor y COCO**. Queda en el engine como `deprecated_d_ckm`, y nada en `services/` la llama. - **Los nombres se conservan** (`d_ckm`, `count_attractors`, `… |
| nuevo | ## 10. D_ckm | **Consecuencias sobre lo que sigue en esta sección, que es la v14 y se conserva como traza** (donde dice A0 / A_actual como conteos, se lee "septiembre"): - "D_ckm no converge en signo bajo variación de seed o n_runs" er… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | *(v15: desde `dabd1ed`, `landscape_engine.count_attractors` devuelve **N_eff por órbita** (`float`), no terminales; la forma anterior queda como `deprecated_count_attractors`. Lo que sigue en esta sección describe la de … |
| nuevo | ## 11. Conteo de atractores — _count_attractors | *(v15: las líneas que siguen son de septiembre. Hoy el bucle es `for i, j in expulsados:` (L233), y `Δ_r_torsion` se acumula igual (L238–L240): las dos condiciones siguen por construcción. Que `pares_por_orbita` genere s… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | *(v15)* **No hay más STOPs** (delamor, 5 oct): stop es detenerse, y el operador nunca se detuvo: hace `Δ → α·Δ`. Su nombre formal es **operador de compresión de COCO**; "operadorstop" es el apodo *"entre los íntimos"*. E… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | **Genealogía de "no produce pérdida".** El resultado es de **junio** (`registers/REG_destruccion_recuperacion_v1`, Sonnet 4.6): un driver (`sweep_stop_perdida.py`) con W fija (W_mixta AMP=40, N=32, A0=25), cuando todavía… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | *(v15: `TASK_canal_iap_clock_iniciativa_v2` (`c451af8`) propone el **CLOCK del canal** —ticks numerados, comunes y observables; el silencio entre mensajes es dato— y el **ODA continuo**: el mensaje nuevo y el tick pasan … |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | **Ciclo de vida de COCO = ciclo de vida de W**: si W cambia (rebuild), A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe. *(v15: **implementado** — CP2b y CP4. Antes había dos COCO: el que… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | **COCO y el canal** *(v15)*. **La serie IAP nunca tuvo COCO conectado**: se ejerció en tests y drivers (delamor, para el paper; MAPA_REG_corpus_v4: *"el canal vivo no inyecta thermostat"*). **Desde el CP4 (`1e8d267`) el … |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | `_alpha_for` monotónicamente decreciente: **verificado** 43/43 tests. *(v15: `d_ckm_threshold`, `alpha_star` y `frac_rec_min` están **no recalibrados** sobre la escala log de D_ckm; son de Calibración — §10.)* |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | **Armstrong in-vivo** (verificado): OPERADOR_STOP_COCO aplicado 20/20 veces, α ∈ [0.05, 0.30]. *(v15 — MAPA_REG_corpus_v4, REG_armstrong_stop_coco_v1 §Réplica: "in-vivo" es un pipeline MonitorService + COCO **en un scrip… |
| nuevo | ## 14. Coercividad CKM | *(v15 — `P1P4/OBS_P1_run_P1_y_coercitividad_04oct_v1.md` §3.)* **Los dos cruces son combinatoria de N, no coercitividad del campo.** Para k nodos en +1 elegidos al azar, E[c(S)] = μ_W · ((2k − N)² − N) / (N(N − 1)), que … |
| nuevo | ## 15. Temperatura de Néel efectiva (≈ Nielsen ≈ TEER) | *Propuesto — no verificado* *(v15: sigue **no corrido** — REG_salamanca_s1_v1 §6. Es el segundo paso de la admisión de W_mixta: qué profundidad tiene la frontera que SALAMANCA encuentra. Su lugar en el Orden BABEL no est… |
| nuevo | ## 16. SALAMANCA | *v14: Propuesto — no verificado.* ***v15: S1 corrido*** *(`registers/REG_salamanca_s1_v1.md`, OK de delamor 5 oct; 1000 barajados, k-means con 10 inicializaciones, Bonferroni sobre 7 k).* |
| nuevo | ## 16. SALAMANCA | **Corrección (v15 — REG_salamanca_s1 §3, delamor): no detecta estructura adversarial; detecta modularidad.** Que haya módulos no dice que haya posiciones que se opongan. Una palabra, dos objetos, y es la razón de que el … |
| nuevo | ## 16. SALAMANCA | **El intento que subyace** *(delamor)*: no es encontrar fronteras, es tener un criterio que **pueda devolver vacío**. *"Lo que natura non da, SALAMANCA non presta"* — y *"no se fía"*. |
| nuevo | ## 16. SALAMANCA | \| corpus \| saturación \| veredicto S1 \| lectura \| \|---\|---:\|---\|---\| \| caso09 \| 0.619 \| **FRONTERA** (k = 3 y 6; k = 3: cluster mín. 6 nodos, efecto 2.97×, p < 0.001) \| separa protocolo e identidad de device… |
| nuevo | ## 16. SALAMANCA | - **La saturación ordena:** monótona en los cinco corpus medibles, y medida sobre W antes de particionar. Verificado como medición; la lectura causal es **propuesta**. - **Lo que más importa:** el criterio **devolvió vac… |
| nuevo | ## 18. Lo que permanece abierto | **Nuevos en v15** (plano indicado en cada uno): - **Calibración** (operacional): el proceso no existe. Los umbrales de COCO están no recalibrados sobre la escala log; la corrida larga de caso09 (`n_torsion`, 16 de 24 en … |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **Regla CKM TRUST** *(v15 — dictada por delamor, 4 oct 2026; `claude/sesion_04oct2026_regla_ckm_trust`)*. Cómo se decide cuando hay que decidir: |
| nuevo | ## 19. Tensiones metodológicas constitutivas | 1. **El campo decide:** criterio de campo con traza. La traza es parte del criterio, no un agregado. 2. **Si empata y hay traza, la traza decide:** gana el que ya está, ya estuvo, ya ganó. 3. **Si no hay traza: ¿por qué … |
| nuevo | ## 19. Tensiones metodológicas constitutivas | Sin el paso 3, cada vez que falta traza se pasa directo al 4: decide el contexto, y el sesgo se presenta, subrepticiamente, como si fuera del campo. ¿Pasa desapercibido? *Depende: mecánicamente, sí* — y ese matiz es lo q… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **UNKNOWN no es un grado** *(v15)*. No es NOMINAL ni "desconocido": es no haber visto, un estado del que observa. El vacío pasaba como "stable" en COCO y como NOMINAL en Firma; desde `c06db07` y `57f8a88` es UNKNOWN, y e… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | **El test tiene que poder fallar** *(v15)*. En los CP3i y CP4 de Monitor+COCO v2 se hicieron **ocho inversiones**: cambios deliberados al código, cada uno rompe al menos un test, y se restaura (la salida literal está en … |
| nuevo | ## 20. Referencia externa más cercana | *(v15 — réplica de la Fig. 5, 4 oct, Opus 5.5; `P1P4/INFORME_replica_Aiyappa_fig5_v1.md`.)* **Se sostiene:** la modularidad óptima aparece en contagio complejo —con ρ0 = 0.10 de semillas, la adopción es 0.50 con μ = 0.01… |
| nuevo | ## 20. Referencia externa más cercana | **Pariente, no gemelo.** En Aiyappa cambian los pesos; en CKM, sobre una W, cambian los estados. La energía de Aiyappa es triádica (Heider); la de CKM, por pares (Hopfield). "Mapea casi 1:1 con W_pos" se lee con eso. **L… |
| nuevo | ## 20. Referencia externa más cercana | **Cita, siempre:** Aiyappa, R., Flammini, A., & Ahn, Y.-Y. (2024). *Science Advances* 10(15), eadh4439. doi:10.1126/sciadv.adh4439. |
| nuevo | ## 20. Referencia externa más cercana | *Fuentes v15 (Oct 2026): registers/REG_d_ckm_formula_canonica_v1 (`dabd1ed`), registers/REG_salamanca_s1_v1, registers/REG_trace_ip_sesion_05oct_v1; P1P4/BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1 (borrador), P1P4… |
| nuevo | ## 20. Referencia externa más cercana | *Repo: gadanindelamor/ckm — Sep–Oct 2026 · v15 DRAFT hasta la lectura de delamor* |

## v15 → v16

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **El campo no salta; el corpus ya es instrumento** *(v16 — delamor, 10 oct)*. El campo es continuo. El corpus lo muestrea en textos discretos, la extracción lo representa y W lo fotografía: **las W son representaciones**… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | **`W_ckm_corpus_v2.json` — origen UNKNOWN** *(v16, delamor)*. Nunca se supo quién la escribió ni quién escribió su referencia. 32 nodos, 375 pares positivos, 121 ceros, **0 negativos**. Su campo `termap_version` no nombr… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **f.1) Una etiqueta heredada se propagó por código** *(v16)*. `experiments/build_W_base_N64.py` escribe `"termap_version": "v3_tfidf_auto"` y `assert corpus_size > 5145` (el corpus_size de la W v2): continúa la numeració… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **g) Origen del signo — los marcadores** *(v16 — leído en código y medido en trazas, 10 oct; abierto)*. La única fuente de peso negativo es `_OPPOSITION_MARKERS` (44 marcadores es/en), buscado por **substring** sobre el … |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | **h) Teorema de presencia** *(v16)*. La co-ocurrencia por presencia es de la forma XᵀX: semidefinida positiva y ≥ 0. **Con presencia sola no hay triángulo con producto de signos negativo y T(W) = 0** por construcción. La… |

## v16 → v17

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | > **v17 (14–19 oct).** > - **CKM no extrae nodos ni tokeniza; interpreta dinámica, no significado** (delamor, 14 oct). El productor de W **se declara**: `docs/defs/DECLARACION_extraccion_W_v1.md` (14 oct, 8 operadores; d… |
| nuevo | ## N. Nombres — rótulo, objeto y fecha *(nueva en v15, sin número para… | > **v17 (19 oct).** **Rótulos en inglés** de acá en adelante (delamor). Renombres declarados, sin alias: `criterio_local` → `local_criterion`, `arranque` → `startup`, y las claves del panel nacidas en S2-C0 CP1 (encargad… |
| nuevo | ## OP. Analytics global del instrumento — snapshot W y dinámico | > **v17 (CP-E, 15 oct; `0e042ac`, freeze `e1db2a2`).** **Estabilidad declarada como rango con dependencias.** N_eff converge frente al muestreo: dispersión entre 10 seeds **7–9 %** del valor (A24 15,52 ± 0,32; D12 5,27 ±… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | > **v17 (15 oct, delamor).** **W es la representación de lo disponible y accesible en este instante**, el único que existe. No hay "W vieja" y "W nueva": hay la W a la que cada uno accedió cuando miró; lo que corresponde… |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | > **v17.** La rama de extracción **se declara** (ver Modelo Conceptual v17): 8 operadores, v1 → v2. Medido sobre ella (CP-E, ver OP v17): el paisaje con 7–24 textos depende fuertemente de la extracción. **Revisión de cri… |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | > **v17 (14–15 oct).** **CP-M** (`a1c6a18`): un nulo que asigna la marca de oposición a textos al azar (mismo k) **no separa** la marca real en ningún corpus (percentiles 2,0 / 68,5 / 100; en dos corpus W_mixta tiene **m… |
| nuevo | ## 8. W_mixta — ferrimagnética | > **v17 (15–18 oct).** El signo lo da `_has_opposition` (CKM): devuelve **−1/+1**, no "oposición". Declaración v2: **palabra completa y NFC** (antes subcadena: "but" en "distribution", "pero" en "espero"). Sobre la lectu… |
| nuevo | ## 9. Δ_r — acumulador de metabolización (runtime) | > **v17 (15–18 oct).** La escala con que Δ_r entra a W_eff en Monitor (`_combine_W_Delta`: Δ_r / max Δ_r × media de W > 0) es **una elección heredada** — el propio código lo dice — y dentro de un ciclo es lo único que mu… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | > **v17 (18–19 oct).** Los umbrales históricos `0.40` / `0.60` se calibraron sobre la forma lineal por conteo (lo dice `coco.py`). Con `calibrate` en el canal (S2-C0 CP1), con 45 mensajes de 2 devices: **calibrado**, `D_… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | > **v17 (20 oct) — cómo se calibra COCO, leído en el código** (`services/coco.py`, `services/calibrate.py`, `iap_chatroom/ckm_monitor.py`). > - **`calibrate` calibra dos umbrales y nada más:** `D_CKM_THRESHOLD`, a partir… |
| nuevo | ## 17. Escala y N | > **v17.** En la Serie 2, el primer W espera **≥ 30 mensajes de ≥ 2 devices**; `min_df = 2`; rebuild cada 10 mensajes; n_runs ≥ 1000 (mínimos sensatos, S2-C0). Ver OP v17: con 7–24 textos el paisaje depende fuertemente d… |
| nuevo | ## 18. Lo que permanece abierto | > **v17 (19 oct), agregados:** la **sombra de `calibrate`** (propuesta: si hace falta, qué mejora, qué requiere, impacto; insumo: cuánto tarda en el salto, CP1b); la **escala de Δ_r** (CP1b); **permiso de uso del IAC** y… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | > **v17 (14–15 oct).** > - **Sin regresiones ni compatibilidad hacia atrás** — *"la regresión es cuando el producto está estabilizado… acá estamos investigando"*. Lo que pasó se conserva **congelando sus condiciones en `… |

## v17 → v18

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | > **v18 (20–22 oct).** > - **Las dos series de IAP son testing, no experimentos** (delamor, 21 oct, `docs/opus/decisiones_en_el_acto.md`). Lo que se observa en ellas describe el estado del instrumento durante la prueba, … |
| nuevo | ## 1.1 La rama de extracción — lo que decide qué existe antes de que h… | > **v18 (21 oct).** **Operador 5, pool con ≤ top_k términos** (`595d0b7`, en `DECLARACION_extraccion_W_v2.md`, en `declaracion()` y en `_seleccionar`): si el pool tiene `top_k` términos o menos, entran todos — N = \|pool… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | > **v18 (21–22 oct) — la calibración en vivo no separó.** En el intento 2 (REG §2): `calibrated: false`, `estado: no_calibrado`, `causa: "sin_separacion"` (la curva de λ no separa: `d_max = 0.0`, `curva_monotona: false`)… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | > **v18 (21–22 oct) — sobre el párrafo que sigue.** *"La serie IAP nunca tuvo COCO conectado"* (v15) **queda como traza, con su fecha**, como toda la v17. Desde el 21 oct (intento 2, Modelo Conceptual v18) COCO **sí** es… |
| nuevo | ## 18. Lo que permanece abierto | > **v18 (22 oct) — abiertos nuevos, del intento 2** (REG §7): (1) techo de Groq **por modelo** — con 512, `gpt-oss-20b` dejó 17 de 98 llamadas vacías por razonamiento (la verificación previa era n = 1); (2) cuota de Gemi… |

## v18 → v19

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## EL Modelo Conceptual | > **v19 (26–27 oct).** > - **El estado: cada uno guarda lo suyo, en su lugar** (delamor, 27 oct: *"es cada uno guarda por su cuenta, y sus atribución, SI. solo que es donde guarda.... no cuando, no overlapping, no... es … |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | > **v19 (27 oct).** CKMlandscapeConfig → todos: hoy **no** porta umbrales (D6). **Decidido, no implementado (CP2, D3–D4):** porta el registro de la calibración en su lugar, firmado con su `w_sha`; COCO lee de ahí su vara… |
| nuevo | ## 1. W_pos — matriz estática de co-ocurrencia | > **v19 (23–26 oct) — premisas sólo en W dinámica.** > - **W estática no tiene premisas** (delamor, 26 oct: *"las premisas entiendo serían solo para W dinámica?"*; ante la propuesta de Opus: *"sí. anotalo"*). Tiene **F**… |
| nuevo | ## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstra… | > **v19 (26 oct).** **P1–P7 se retiran todas como premisas** (delamor: *"las retiraría todas P1 P7; establecería las F formulaciones matemáticas que se verifican en W estática, que es lo escrito solo que no son premisas"… |
| nuevo | ## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy… | > **v19 (26 oct).** > - **P5, P6, P7: esperan condiciones** (delamor). No son premisas (§5, v19). > - **El nulo del signo por marcadores se queda como medición**, sin la predicción P5 (delamor: *"si P5 está probado sería… |
| nuevo | ## 8. W_mixta — ferrimagnética | > **v19 (27 oct) — la calibración en el build: el origen ya pasa por `calibrate`.** Lo de abajo (v9: *"Build inicial: calibrar… Estado: pendiente de implementación"*) habla de W_mixta; lo de este bloque vale para **cualq… |
| nuevo | ## 10. D_ckm | > **v19 (26 oct) — tres D_ckm, no dos.** Misma fórmula (`1 − ln N_eff / ln N_eff0`), distinto contra qué: > - **Monitor:** baseline W + Δ_r; se resetea cuando cambia W; `n_runs_attractors` propio (1000), no de la Config.… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | > **v19 (26–27 oct) — la vara de COCO.** > - **Dos casos en que COCO_i juzga con una vara que no sale de W_i** (26 oct; delamor: *"EXACTO. esa es la punta del supuesto ovillo. justo 1 y 2"*): (1) `calibrate` no separa → … |
| nuevo | ## 18. Lo que permanece abierto | > **v19 (23–27 oct), agregados.** Cada uno con lo que hay que decidir: > - **E5 [delamor]:** anotar en el docstring de `ckm_monitor.py:84-90` que la "primera calibración que separa" fue con `n_runs = 200, seed = 0`. > - … |
| nuevo | ## 19. Tensiones metodológicas constitutivas | > **v19 (26–27 oct).** > - **Los defaults se declaran** (delamor, 26 oct: *"similar a todos los defaults de parametros, deben ser declarados"*; ante la lectura de Opus: *"Nunca lo completa en silencio el argumento de una… |

## v19 → v20

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## 0. Dominio CKM | > **v20 (28 oct) — cambio de fase.** delamor: *"TRUST, el proyecto está cambiando de fase, acumulación a EVALUACIÓN.. CKM cierra y se transforma en TRAZA VIVA"*. El plan: las DEFS, el paper, el plan de cierre del repo y … |
| nuevo | ## EL Modelo Conceptual | > **v20 (27–28 oct).** > - **El lugar de la calibración en la Config: implementado** (CP2 de `TASK_calibrate_en_el_build_v2`; BANDEJA 27 oct 07:10 UTC; TASK cerrada en CPa–CP2, `e940c81`). `registrar_calibracion` es el ú… |
| nuevo | ## SLAs — acuerdos sin burlar encapsulamiento | > **v20 (27 oct).** Lo del SLA de la v19 está **implementado** (CP2): COCO lee su vara del lugar de la calibración como `Threshold`. `MEASURED` si viene de una calibración de su W; `DECLARED` con la causa (`sin_registro_… |
| nuevo | ## 4. Dinámica de relajación — dos implementaciones distintas | > **v20 (28 oct) — el lema del colapso, y la paridad.** > - Con todos los acoplamientos iguales a `e > 0` y la diagonal en 0, el campo es `h_i = e·(S − σ_i)`, con `S = Σσ`. Bajo `relax_orbit` (sincrónica; con `h = 0` con… |
| nuevo | ## 8. W_mixta — ferrimagnética | > **v20 (27–28 oct).** El CP2 completó lo de la v19: la calibración en el build tiene su lugar en la Config y COCO lee de ahí (Modelo Conceptual, v20). El caso 1 (la vara de otra W) tiene un test (`tests/test_vara_del_co… |
| nuevo | ## 10. D_ckm | > **v20 (27–28 oct).** > - **El mismo `n_runs` para los tres D_ckm**, 200 por default (Modelo Conceptual, v20). La razón escrita del 27 oct es de delamor: comparar dos D_ckm estimados con muestras de distinto tamaño comp… |
| nuevo | ## 11. Conteo de atractores — _count_attractors | > **v20 (28 oct).** > - **Genealogía** (delamor: *"la paridad… que sucedía desde los conteos antes de las masas. de allí LaSalle que lo traje a CKM, la fricción y finalmente masa de cuencas que es UNA de las mediciones s… |
| nuevo | ## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR… | > **v20 (28 oct) — el patrón de calibrate, medido y leído al revés.** > - **La única calibración que separó en un vivo tiene un margen cuyo intervalo contiene el 0** (texto 14.1). Es `bdb98f5b` (intento 3): margen +0,011… |
| nuevo | ## 14. Coercividad CKM | > **v20 (28 oct).** El λ en que termina de colapsar cada W se parece a una coercividad (cuánto empuje ferromagnético borra la estructura de W). Está **cerrado por declaración** (§12, v20): no se mide por enumeración. |
| nuevo | ## 18. Lo que permanece abierto | > **v20 (28 oct), estado de los abiertos de la v19 y agregados:** > - **Resueltos:** E5 (el docstring de `ckm_monitor.py` declara las condiciones de la primera separación, `293fd44`); P13; P14 punto 3 (los providers en I… |
| nuevo | ## 19. Tensiones metodológicas constitutivas | > **v20 (28 oct).** > - **El número conveniente, una vez más:** el margen no se toca para que separe. La definición candidata no empuja a que separe: con ella, probablemente desaparece la única separación que hubo. > - *… |
