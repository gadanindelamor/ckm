
# Premisa de Experimentos CKM

## CONDICION N

Un experimento puede servir como evidencia o contraejemplo para una afirmación sobre los tres modelos matemáticos que constituyen  CKM Si  se cumple:

	- **N≥30** si un argumento depende de observar histéresis, cascadas o atractores espurios 
	- **N≥100** si un argumento necesita rigor cuantitativo (exponentes críticos, validez de α_c)

Por simetría algebraica o por tratabilidad pedagógica— CONDICION N es donde los 3 modelos **demuestran su teoría exacta**, no donde la cuestionan.


# N=4 es insuficiente: por qué tres modelos canónicos colapsan a la trivialidad

**N=4 no exhibe ningún fenómeno no-trivial en los tres modelos consultados.** En las redes de Hopfield, en k-core percolation sobre N=4, y en Belief Propagation sobre el ciclo de cuatro nodos, la teoría establecida demuestra que el sistema cae en regímenes trivialmente analizables —enumerables a mano, monótonos, o con punto fijo único— donde precisamente desaparecen los fenómenos emergentes (atractores espurios, transiciones híbridas, multiplicidad de fixed points) que estos modelos fueron creados para estudiar. Las tres teorías coinciden: son **resultados del límite termodinámico** o exigen estructuras (multiplicidad de loops, jerarquía núcleo-corona, mezclas de ≥3 patrones) que un grafo de cuatro nodos sencillamente no puede contener. La pregunta derivada admite una respuesta numérica defendible: **N≈30 sigue siendo el umbral histórico** (es el menor tamaño que el propio Hopfield consideró aceptable en 1982), aunque para un experimento sintético analíticamente manejable basta con **N≈8–16** dependiendo del fenómeno objetivo.

## Hopfield en N=4: capacidad fraccionaria y estados enumerables

**La fórmula α_c ≈ 0.138·N es asintótica y no aplica en N=4.** El resultado de Amit, Gutfreund y Sompolinsky (Phys. Rev. Lett. 55, 1530, 1985; Annals of Physics 173, 30, 1987) se obtiene mediante el método de réplicas en el límite N→∞ y exige que el ruido del crosstalk satisfaga el teorema central del límite. Para N=4 esto da capacidad ≈0.55 patrones —una cantidad matemáticamente vacua—. McEliece, Posner, Rodemich y Venkatesh (IEEE Trans. Inf. Theory 33:461, 1987) derivan rigurosamente C ≈ N/(2 log N), que para N=4 arroja ~1.44 patrones; en la práctica, **un único patrón con su antípoda**.

Con sólo 2⁴=16 estados (8 pares antípodas por simetría Z₂) y 6 pesos sinápticos w_ij, el sistema es **enumerable por fuerza bruta** y carece de "fenómeno emergente". Los atractores espurios canónicos —mezclas simétricas sgn(±ξ¹±ξ²±ξ³)— exigen al menos P=3 patrones almacenados, lo que en N=4 corresponde a α=0.75, ya en la fase de spin-glass donde no hay retrieval. El "blackout catastrophe" descrito por Nadal, Toulouse, Changeux y Dehaene (EPL 1:535, 1986) es un fenómeno estadístico-mecánico que requiere α≥α_c distinguible del ruido finito; estudios modernos de Folli et al. (Frontiers Comput. Neurosci., 2017) sólo lo simulan a N≥50.

Decisivo: **el propio Hopfield (1982, PNAS 79:2554) usó N=30 y N=100** y calificó N=30 de *"slightly small"*. Hertz, Krogh y Palmer (*Introduction to the Theory of Neural Computation*, 1991) usan N=100 como ilustración estándar. El paper de Aiyappa, Flammini y Ahn (*Science Advances* 10(15):eadh4439, 2024) trata sobre **redes de creencias ponderadas para contagio social**, no sobre Hopfield clásico en escala pequeña; **la referencia parece estar mal atribuida** si se esperaba evidencia para Hopfield N pequeño.

## N=4 bajo k-core con k=2: la trivialidad analítica P(survive)=p⁴

**El 2-core de N=4 sobrevive si y sólo si los cuatro nodos sobreviven al sampling.** Por enumeración exhaustiva de las 16 configuraciones de presencia/ausencia (cada nodo retenido con probabilidad p), si se elimina aunque sea un nodo, los dos vértices vecinos quedan con grado 1 y son podados, propagando el colapso al grafo entero. El resultado exacto es:

**P(2-core no vacío) = p⁴**, una función analítica e infinitamente diferenciable en [0,1] **sin umbral crítico, sin discontinuidad, sin divergencia de longitud de correlación**. En el límite N→∞ del ciclo C_N, p^N concentra la "transición" trivialmente en p=1.

El paper de Goltsev, Dorogovtsev y Mendes (Phys. Rev. E 73, 056101, 2006; arXiv:cond-mat/0602611) declara explícitamente que sus resultados aplican a redes con estructura **localmente tree-like** en el límite N→∞ usando generating functions del configuration model; la transición híbrida (salto discontinuo + singularidad β=1/2) que descubren ocurre **únicamente para k≥3** —para k=2 la transición es continua tipo percolación ordinaria con β=1—. Dorogovtsev, Goltsev y Mendes (PRL 96, 040601, 2006) refuerzan que el fenómeno híbrido es de **campo medio**; Rizzo (arXiv:1807.08066, 2018) demuestra mediante M-layer expansion que en dimensión física finita la transición híbrida ni siquiera sobrevive como punto crítico genuino sino como crossover suavizado.

N=4 viola tres hipótesis simultáneamente: **no es tree-like** (es un loop global), **N=4 está infinitamente lejos del límite termodinámico**, y **carece de jerarquía núcleo-corona** porque toda la red es corona (todo vértice tiene grado exactamente k=2). Los estudios de finite-size scaling de Shang et al. (arXiv:1710.02959, 2017) usan N=10³–10⁶ para extraer exponentes; el ancho del régimen crítico Δp_c~N^(-1/3) en ER da Δp_c≈0.63 para N=4, **mayor que el intervalo [0,1] mismo**. En bootstrap percolation 2D, Holroyd (Probab. Theory Relat. Fields 125:195, 2003) deriva p_c(L)~π²/(18 log L) válido sólo asintóticamente; simulaciones útiles requieren L≥20.

## Belief Propagation en N=4: el caso teóricamente más simple con loop

**N=4 cae bajo el teorema de Weiss (Neural Computation 12:1, 2000) para single-loop graphs**, que es precisamente el escenario donde la teoría de loopy BP está completamente resuelta. Weiss demuestra que para cualquier grafo con un único ciclo y potenciales no-determinísticos: (a) BP converge a un único punto fijo independientemente de la inicialización, (b) la diferencia entre creencias loopy y marginales correctas se expresa cerradamente vía los autovalores λ₁≥λ₂≥... de la matriz cíclica de compatibilidad C, con tasa de convergencia |λ₂/λ₁|, y (c) en nodos binarios, **thresholding las creencias loopy recupera el MAP correcto** aunque la magnitud sea inexacta.

Este resultado se confirma desde múltiples ángulos: Mooij y Kappen (IEEE Trans. Inf. Theory, 2007; arXiv:cs/0504030) muestran que su condición espectral suficiente es **sharp en single loops**; Heskes (Neural Computation 16:2379, 2004) demuestra que la **energía libre de Bethe es convexa** sobre el conjunto de constraints en single loops, garantizando un único minimizador; Watanabe y Fukumizu (arXiv:1002.3307, 2009) reconfirman vía graph zeta function. Yedidia, Freeman y Weiss (MERL TR-2001-22, 2001/2003) no discuten C4 porque es teóricamente trivial —la motivación de su análisis Bethe-Kikuchi son grafos con ciclos cortos entrelazados donde Bethe falla—.

Para que aparezcan **multiplicidad de fixed points, oscilaciones, simetry-breaking ferromagnético** o sensibilidad a inicialización se necesitan múltiples ciclos enlazados. Knoll y Pernkopf (UAI 2017) usan **K4 (grafo completo de 4 nodos)** como ejemplo mínimo no-trivial: contiene varios triángulos y un C4 superpuestos, y exhibe transiciones críticas J_C+ donde aparecen fixed points adicionales. El benchmark estándar son **grids 3×3 (N=9)** y **4×4 (N=16)**; en QMR-DT (Murphy, Weiss, Jordan, UAI 1999) las oscilaciones de período 2 emergieron con ~600 nodos pero por priors extremos, no por tamaño.

## Sí, N=4 puede ser interesante: pero no para estos tres modelos

Hay un matiz importante. **C4 sí es útil pedagógicamente** para BP porque la fórmula de Weiss da una expresión analítica cerrada de la diferencia loopy-vs-exacto, y porque ilustra que la aproximación de Bethe es exactamente convexa. El problema no es que C4 sea inútil, sino que **es el caso teóricamente trivial** donde no aparecen los fenómenos patológicos que motivan el estudio empírico de loopy BP. Análogamente, Hopfield con N=4 sirve como ejercicio de pizarra para visualizar la regla de Hebb y la dinámica determinística, pero no exhibe atractores espurios genuinos. Para k-core ni siquiera hay valor pedagógico: P=p⁴ es una ley de potencia trivial.

## Pregunta derivada: el N mínimo defendible para experimentos sintéticos

La síntesis de las tres literaturas converge en una jerarquía. Para fenómenos colectivos no-triviales pero analíticamente manejables, los umbrales documentados son:

| Modelo | N=4 | N mínimo didáctico | N mínimo "Hopfield-1982" | N para análisis cuantitativo |
|---|---|---|---|---|
| Hopfield (atractores espurios, mezclas) | trivial | **N≈8–10** (P=2–3 patrones, 2⁸=256 estados) | **N=30** (Hopfield 1982) | N≈100 para validar α_c=0.138 |
| k-core / bootstrap percolation | P=p⁴ trivial | **N≈50–100** con k≥3 | N≈10³–10⁴ FSS | N≈10⁵ para exponentes |
| Loopy Belief Propagation | trivial (Weiss 2000) | **K4** (N=4 con todos los enlaces) o **grid 3×3 (N=9)** | grid 4×4 (N=16) | grid 10×10 (N=100) |

**La recomendación numérica más defendible** para un experimento sintético que (a) exhiba histéresis, cascadas y atractores espurios de forma no-trivial pero (b) siga siendo analíticamente manejable, es **N entre 16 y 32**. Este rango captura:

- En Hopfield, espacio de 2¹⁶=65 536 a 2³²≈4×10⁹ estados —enumerable computacionalmente pero suficiente para almacenar P=3–4 patrones con mezclas espurias visibles—.
- En k-core, se requiere acompañar el aumento de N con grado medio ⟨z⟩≥2k y k≥3 (no k=2), porque el tamaño solo no salva la trivialidad estructural; N=16 en una red ER con ⟨z⟩=4 ya admite cascadas observables.
- En BP, grids 4×4=16 o 5×5=25 muestran multiplicidad de fixed points y dependencia espectral del damping (Knoll-Pernkopf 2017).

Si el objetivo es **un único N que sirva a los tres modelos simultáneamente con margen de seguridad**, la respuesta histórica y estadísticamente defendible es **N≈30**, siguiendo a Hopfield (1982) explícitamente. Es el menor tamaño donde los tres fenómenos —atractores espurios robustos, cascadas tipo k-core, multiplicidad de fixed points en BP— han sido **documentados empíricamente con confianza** en la literatura primaria, sin abandonar el régimen donde la enumeración computacional sigue siendo factible (2³⁰≈10⁹ estados, manejable con muestreo Monte Carlo).

## Conclusiones 

Los tres modelos comparten una propiedad subyacente: **son construcciones del límite termodinámico que codifican fenómenos emergentes ausentes en sus restricciones a sistemas finitos pequeños**. El α_c de Hopfield, la transición híbrida de Goltsev-Dorogovtsev-Mendes, y las patologías de loopy BP son todos resultados de campo medio o de configuration models con N→∞. Restringirlos a N=4 no produce versiones "miniatura" de los fenómenos, sino regímenes cualitativamente distintos donde la teoría se reduce a álgebra elemental (16 estados enumerables, p⁴ analítica, fixed point único garantizado).

La implicación metodológica es clara: **un experimento sintético en N=4 no puede servir como evidencia ni como contraejemplo para ninguna afirmación sobre estos tres modelos**. Si un argumento depende de observar histéresis, cascadas o atractores espurios, debe usar N≥30 como mínimo; si necesita rigor cuantitativo (exponentes críticos, validez de α_c), N≥100 es el piso defendible. Y si la motivación es C4 específicamente —por simetría algebraica o por tractabilidad pedagógica— conviene reformular el problema: C4 es donde estos modelos **demuestran su teoría exacta**, no donde la cuestionan.