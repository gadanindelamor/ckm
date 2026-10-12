OBS_PAPER__v13

LEER TODO ANTES. si no leo no me doy cuenta,  TODO el material que hay y el que no hay tambi. Preguntas y subo lo que me pidas.
No leíste n el chat actual parece ni los 2 abteriores. No tense acceso ?


no varece que hays leído doc que es cribisate DEFS actuales, v13

leelo falta de todo, Aplica lo que indica defs al papar.



la función canonica NO es A0 - A actual etc, CKM converge orbitas bada d beads, edge eso eta en el paper...
y no es ni devirsida ni degadacion. es conteo con colweccionista de coneos cupones  y que estima las fases delas orbitas que son atracores. las orbitas son ciclo 3. tc tannpoco converge contar orbitas, pero acerea hasta 80 veces el relacc. Usamos relax orbital que es la verdad de lo que sucede, Entiendo que aun te esistas a la vedad matemática pero la teoría de sistemas dinámicos existe y esta demotrada, NADA tiene que ver con Ly punov, 
La función que mapea  La Salelle es ta implementada converge y funciona. esta escrito , lo escribite vo srecien.

Puede faltar talvez  los últimos 5 regs.  rgs. quizás ni lo ceo, pero digamos ques los lees. y actualizas.



ESTO LO GENERASTE EN ESTA SSION
lo leeiste?

*Forma:** S = snapshot (W estático) · D = dinámico (runtime) · S+D = ambas

| Objeto | Forma | Técnica | Qué mide | Representación estructural en CKM |
|---|---|---|---|---|
| **fi** | S | Frecuencia marginal: fracción de textos donde aparece el nodo i | Presencia individual de un concepto en el corpus | Actividad del nodo — independiente de co-ocurrencia |
| **W_ij** | S | Co-ocurrencia normalizada por n_textos | Densidad de co-presencia de pares en el corpus | Campo asumido — suelo simétrico. Lo que el campo da por sentado |
| **W_ij / (fi·fj)** | S | Razón observado/esperado estadístico | Si el par co-ocurre más o menos de lo esperado por independencia | Fuerza de asociación estructural neta — lo que fi no explica |
| **c(S)** | S+D | mean(W_ij · σi · σj) sobre todos los pares i<j | Alineación del estado activo con la estructura W | Cohesión del campo — cuánto del suelo está activo |
| **r = c(S)/μ_W** | D | Normalización por peso medio del corpus, medido al inicio de sesión | Cohesión relativa independiente de escala del corpus | Señal de régimen operacional G1/G2/G3 |
| **Histeresis (P1)** | S | Rama UP (incorporación) vs DOWN (remoción) de c(S) · Wilcoxon zona crítica | Asimetría path-dependiente del campo bajo perturbación | El campo recuerda su trayectoria — el suelo no es reversible |
| **Ω* (P4)** | S | c(S) vs ρ en grid · argmax | Densidad óptima interior de W_mixta | La tensión estructural produce cohesión — no la reduce |
| **Atractores A = \|L\|** | S+D | Monte Carlo σ₀ + relajación Hopfield → estados únicos | Número de configuraciones estables alcanzables | Diversidad del landscape — estimador de \|L\| (LaSalle). Conteo no converge: crece con n_runs (sesgo coleccionista). |
| **N_eff** *(implementado, landscape_engine.py)* | S+D | 1 / Σmᵢ² sobre masas de cuenca muestreadas | Diversidad efectiva del landscape ponderada por volumen de cuenca | Inverso de Simpson sobre cuencas. Rango: [1, A0]. N_eff=1 = colapso total; N_eff=A0 = equidistribución perfecta (no ocurre con W real). Convergente con n_runs≥1000 (±1–5% en casos IAP). Reemplaza A como estimador de diversidad. |
| **D_masa_cuencas** *(propuesto)* | D | 1 − log(N_eff_actual) / log(N_eff_0) | Degradación del landscape medida sobre masas de cuenca | Escala log preserva carácter información-teórico (N_eff = exp(H₂_Rényi)). Abierto: escala lineal vs log no decidida. |
| **node_presence** *(implementado, landscape_engine.py)* | S+D | fracción de atractores muestreados donde cada nodo está activo | Presencia de cada nodo en el espacio de atractores | Qué nodos habitan las cuencas — no su presencia en textos. |
| **d(σ)** *(implementado, landscape_engine.py)* | S+D | mínimo de flips que cambia la órbita de σ | Distancia de σ a la frontera de su cuenca | Con W corregida caso09 natural (N=20): 81% de la masa tiene d=1. Función pura, no conectada al panel todavía. |
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
…………………………..……………………………….
 falta cuencas Eff simpson,, goedl bueno , todo o que hace conveyer a CKM, la demostración matematecas. relax sincronico CONVERGE la funciones ta definida la demostración es de \lasalle. \no requiere \Lapynuor.  
 bueno fala. TODO desde el punto de inflexion
 --------------------------------------
 
 lee los regs, si falta algo lo pedis o preguntas,

**Scope and conditions of this work.** The operational corpus is at N = 32 nodes. Classical Hopfield networks require approximately N ≥ 128 for robust attractor diversity under Hebbian associative memory storage (capacity α_c ≈ 0.138N). CKM does not store associative memories and does not use Hebbian learning on W — the scale condition is therefore not the Hopfield associative minimum.

>>> _clamor_
y condición de nodos no  correlacionados


The working reports (v2–v31) are not documentation of a research process


>>> _clamor_ v32 9 
versions

reject metabolize 


