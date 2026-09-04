# CKM en el paisaje de la representación del conocimiento

*Cohesive Knowledge Model — Encuadre teórico comparativo*  
*gadanin.delamor · Mayo 2026 · v1*

---

## Introducción

El Cohesive Knowledge Model (CKM) es un modelo formal para la dinámica de grafos
de conocimiento en sistemas multi-agente. Su pregunta central no es nueva en
la representación del conocimiento — pero su respuesta sí lo es:

> ¿Cómo verificar que el conocimiento nuevo es genuinamente interdependiente
> con el cuerpo existente — no solo semánticamente próximo, no solo de fuente confiable?

Este documento ubica CKM dentro de los marcos establecidos de la representación
del conocimiento, identifica correspondencias precisas, y nombra lo que CKM agrega
al paisaje sin precedente conocido.

---

## 1. Posición en el espacio IA simbólica / subsimbólica

### 1.1 La distinción clásica

La IA simbólica representa el conocimiento mediante estructuras discretas y reglas
explícitas (lógica, redes semánticas, marcos, ontologías). La IA subsimbólica codifica
el conocimiento implícitamente en pesos de conexión (redes neuronales, algoritmos
genéticos). La tensión entre ambos paradigmas es constitutiva del campo desde 1956.

### 1.2 CKM como híbrido estructurado

CKM ocupa un espacio intermedio que los marcos clásicos no definen:

| Componente | Tipo | Función |
|-----------|------|---------|
| Nodos del grafo | Simbólico | Conceptos explícitos con identidad |
| W — matriz de co-ocurrencia | Simbólico | Memoria estructural declarada |
| Criterios C1–C4 (Gatekeeper) | Simbólico | Reglas de admisión binarias |
| Δ — asimetría direccional | Frontera | Orienta la inferencia, no la declara |
| c(S) = mean(W_ij·σ_i·σ_j) | Subsimbólico | Medida emergente de cohesión |
| Atractores Hopfield | Subsimbólico | Estados estables no declarados a priori |
| β (temperatura thermal) | Subsimbólico | Sensibilidad al ruido — parámetro de campo |

La combinación no es decorativa: la capa subsimbólica detecta propiedades
(histéresis, densidad óptima interior, coercividad) que la representación
simbólica pura no puede producir. La capa simbólica hace verificable y
falsificable lo que la capa subsimbólica produce.

**Ningún framework clásico nombra este híbrido.** CKM lo ocupa.

---

## 2. Encuadres clásicos — correspondencias

### 2.1 Conocimiento declarativo vs. procedimental → W vs. Δ

La distinción clásica (Luger & Stubblefield, 1998) separa el conocimiento
que responde "¿qué?" del que responde "¿cómo?".

| Categoría clásica | Definición | Equivalente en CKM |
|------------------|-----------|-------------------|
| Declarativo | Hechos, estructuras, qué es cierto | W — co-ocurrencia simétrica. Qué co-ocurre. |
| Procedimental | Acciones, orientación, cómo llegar | Δ — asimetría direccional. Cómo orientó el chispazo. |

**Observación crítica**: la separación W/Δ en CKM no es solo organizacional —
mezclar ambas matrices destruye la capacidad de recuperación de atractores
(de 0.78 a 0.02, verificado). Esto confirma empíricamente que el conocimiento
declarativo y procedimental tienen dinámicas incompatibles si se almacenan
en la misma estructura.

Δ acumula **orientación** del evento inferencial, no frecuencia.
Esta distinción no existe en el marco clásico.

### 2.2 Restricciones de integridad → M.M y Gatekeeper R15

El marco clásico define las restricciones de integridad como "condiciones que
todas las instancias deben satisfacer para ser válidas" (Davis, Shrobe & Szolovits, 1993).

CKM extiende esto en dos direcciones:

**Restricción sobre el contenido** (Gatekeeper R15):
- C1: peso mínimo de conexión (θ_W = 0.10)
- C2: delta de cohesión ≥ −ε (no degradar el grafo)
- C3: dirección inferencial positiva
- C4: capacidad < α_c · N (límite de Hopfield: α_c ≈ 0.138)

**Restricción sobre el agente** (M.M — Mentiriis Morieris):
Un dispositivo no puede declarar capacidades que no puede ejercer.
Esta no es una restricción sobre el conocimiento que ingresa —
es una restricción sobre quien declara. Es la restricción de integridad
más fuerte del sistema porque opera sobre la fuente, no el contenido.

El framework clásico no tiene equivalente a M.M.
Las restricciones de integridad se aplican a los datos, no a los productores de datos.

### 2.3 Sentido común como problema → inversión CKM

El problema del sentido común (Minsky, 1975; Russell & Norvig, 2010) es una
de las principales dificultades de la representación clásica: el conocimiento
implícito es difícil de capturar, codificar, y no colapsar bajo excepciones.

CKM no resuelve este problema — lo reencuadra estructuralmente.

En el corpus N=32, `sentido_común` es un nodo del grafo. Pertenece al
**cluster C4 "suelo"** (junto con `beta_termal`, `DOM_I`, `filtro_previo`,
`cohesion_fabricada`). Está en **oposición perfecta** con `inconmensurabilidad`.

El sentido común no es aquí lo que el sistema debe adquirir y codificar.
Es un atractor de **baja tensión** — estado estable de baja diferenciación —
opuesto estructuralmente al polo de máxima divergencia.

**El problema del sentido común se convierte en información estructural.**

### 2.4 Conocimiento incierto → β como parámetro thermal

El framework clásico trata la incertidumbre mediante lógica difusa, probabilidades
bayesianas, o factores de confianza asignados manualmente.

CKM formaliza la incertidumbre de modo diferente: β (parámetro de temperatura
inversa) controla la susceptibilidad del sistema al ruido. En β_c el sistema
cruza el umbral crítico — máxima sensibilidad, mínima estabilidad.

La distinción es profunda:
- **Incertidumbre clásica**: propiedad del dato (¿qué tan confiable es esta afirmación?)
- **Incertidumbre CKM**: propiedad del estado del sistema (¿qué tan receptivo está el dispositivo a ser deformado por este input?)

β no mide la confiabilidad del conocimiento que entra.
Mide el estado del sistema que lo recibe.

---

## 3. Encuadres avanzados — correspondencias

### 3.1 Revisión de creencias (AGM) → P3 y histéresis

La teoría AGM (Alchourrón, Gärdenfors, Makinson, 1985) establece postulados
formales para la revisión de creencias. El resultado central: la **contracción**
(eliminar una creencia) es más costosa y compleja que la **expansión** (agregar una).

CKM confirma esto empíricamente y lo precisa:

**P3 (verificado, p < 0.0001)**: la relajación tras eliminar nodos es más lenta
que tras añadirlos a densidad idéntica.

**P1 (verificado, p ≈ 0)**: la histéresis en c(S) — la rama descendente (remoción)
difiere de la ascendente (incorporación) a densidades idénticas. El sistema
**recuerda su trayectoria**.

AGM es un marco normativo (cómo *debería* comportarse un sistema racional).
CKM es empírico: mide *cómo se comporta* un grafo de conocimiento real
bajo perturbaciones controladas. La confirmación de AGM en CKM es validación
cruzada por independencia de método.

> **Extensión CKM sobre AGM**: la histéresis no es solo asimetría de costo —
> es una propiedad geométrica del espacio de estados. La trayectoria de llegada
> modifica el atractor alcanzable. Esto AGM no predice.

### 3.2 Teoría de argumentación (Dung, 1995) → triadas C3 y oposición estructural

Los marcos de argumentación abstracta de Dung (1995) definen relaciones
de ataque entre argumentos y calculan extensiones (conjuntos admisibles).
La noción central: la aceptabilidad de un argumento depende de su posición
en la red de ataques, no de su contenido.

CKM conecta con este marco en la estructura de triadas:

**C3 (criterio de elicitación)**: una tríada válida requiere un tercer nodo
que añada tensión al par base — sin él, el par es declarativo, no argumentativo.

**Author 965 (fourforums)**: polo sostenedor estructural puro. Ratio in/out = 455×.
Coercividad = 0.00 hasta 50% de ruido (resistencia absoluta). Presencia de 965
en la tríada → colapso del par a tensión 0 (la tensión se mantiene activa).
Ausencia de 965 → colapso inmediato.

En términos de Dung: 965 es el argumento cuya presencia hace inadmisible
el conjunto de extensiones colapsadas. No ataca — estructura el campo
de ataques posibles.

**Extensión CKM sobre Dung**: los marcos de argumentación son estáticos —
calculan extensiones sobre una red fija. CKM mide la **dinámica temporal**
de cómo la tensión se mantiene o colapsa bajo ruido acumulado.
La coercividad (resistencia a la perturbación) no tiene equivalente en AGM ni en Dung.

### 3.3 Espacios conceptuales (Gärdenfors, 2000) → perspectivas y vanishing points

La teoría de espacios conceptuales de Gärdenfors representa los conceptos
como regiones en un espacio geométrico métrico. La similitud es distancia.
Las categorías son regiones convexas. El aprendizaje es deformación del espacio.

CKM introduce una estructura geométrica compatible pero distinta:

**Puntos de fuga (vanishing points — VP)**: cada perspectiva tiene un VP —
origen de su proyección direccional en el campo. La divergencia entre perspectivas
es función de la geometría entre VPs.

| Geometría | Implicación |
|-----------|-------------|
| VPs paralelos | Divergencia solo a distancia |
| VPs opuestos | Divergencia máxima desde el origen |
| VP compartido | Paralaje, no divergencia |

**R13 (verificado experimentalmente)**: el contacto entre perspectivas
inconmensurables **deforma el campo local sin desplazar los VPs**.
Lo que emerge pertenece al campo, no al grafo — irreversible, bilateral, asimétrico.

En Gärdenfors, el aprendizaje mueve los conceptos en el espacio.
En CKM R13, el contacto deforma el campo sin mover los VPs —
hay dos umbrales: el de inversión de M (menor) y el de desplazamiento del VP (mayor).
Debajo del segundo umbral: deformación sin cambio de perspectiva. Encima: evento cualitativamente distinto.

**Gota de tinta sobre tiza**: ninguno retorna a su estado previo.
Ambos son constituyentes del mismo campo después del contacto.

### 3.4 Física estadística / ferromagnetismo → β_c, M, H_self

El isomorfismo con la física ferromagnética es el más formalizado en CKM:

| Física ferromagnética | CKM |
|----------------------|-----|
| Temperatura T (inversa: β) | β — parámetro thermal del dispositivo |
| Temperatura crítica T_c (β_c) | Umbral de receptividad máxima |
| Magnetización M | Estado de atención del dispositivo (Mi atención) |
| Campo externo H | Demanda que la situación ejerce sobre el dispositivo |
| Campo propio H_self | Campo auto-generado — historia acumulada (Mr) |
| Remanencia Mr | Traza — el sistema recuerda su historia sin campo externo |
| Coercividad Hc | Resistencia a la inversión de M |
| Histéresis | Path-dependencia: la trayectoria de llegada modifica el estado actual |

**Resultado formal CKM (verificado)**:
- W_mixta produce c(S) 13× mayor que W_pos (P4)
- "La geometría de la tensión lo fuerza" — grafos con tensión real tienen
  mayor cohesión que grafos sin tensión. Confirmado N=32.

**Interpretación**: el ferromagnetismo no es una metáfora en CKM.
Es el modelo formal del que se derivan predicciones falsificables
que fueron confirmadas experimentalmente.

### 3.5 Inferencia activa / predictive coding (Friston) → ODA loop

La inferencia activa (Friston, 2010) modela el comportamiento de sistemas
biológicos como minimización de energía libre — la diferencia entre el
modelo generativo del sistema y los inputs sensoriales. El ciclo:
percepción → actualización de creencias → acción → nueva percepción.

El ODA loop de IAID (Observación → Decisión → Acción) es estructuralmente
isomorfo:

| Inferencia activa | IAID/CKM |
|------------------|---------|
| Energía libre F | c(S) — medida de desalineación W/estado |
| Prior | Estado actual del grafo + Δ acumulado |
| Likelihood | Input del nuevo nodo |
| Posterior | Estado tras relajación Hopfield |
| Acción | Decisión del Gatekeeper (admitir/rechazar) |
| Precision (β en Friston) | β thermal en CKM |

**Diferencia clave**: en inferencia activa, el sistema minimiza energía libre
de modo continuo y pasivo. En CKM, el Gatekeeper es una decisión binaria
discreta — admisión o rechazo. La red de verificación continua opera
después de la admisión.

El β thermal en CKM corresponde a la precisión en Friston — pero con una
distinción: en CKM β es propiedad del dispositivo receptor (su estado de
atención), no del prior. Esto habilita H_self como campo autogenerado.

### 3.6 Topología algebraica (Sciamarella / Templex) → R12 y orientabilidad

La tesis de Sciamarella (UBA, 2001) desarrolla el método BraMAH y el concepto
de Templex para caracterizar atractores dinámicos mediante invariantes topológicos:
H₀ (componentes conexas), H₁ (ciclos), H₂ (cavidades 3D), y cadenas de orientabilidad.

La distinción cilindro/Möbius en topología corresponde a la distinción
R12 en CKM entre divergencia **resoluble** e **inconmensurabilidad estructural**:

| Topología | CKM |
|-----------|-----|
| Cilindro (torsión nula) | Divergencia resoluble — las perspectivas pueden cerrarse |
| Banda de Möbius (torsión) | Inconmensurabilidad estructural — el cierre destruye la tensión |
| H₀, H₁, H₂ | Invariantes computables sobre el grafo CKM |
| Invariantes iguales | Perspectivas estructuralmente equivalentes |
| Difieren en torsión | Incommensurabilidad confirmada |

**Estado**: Sciamarella/Templex sobre CKM es dirección abierta — no verificada.
El operador formal para R12 (¿cuándo es resoluble vs estructural la divergencia?)
no está implementado. Esta conexión es hipótesis con alta plausibilidad formal.

---

## 4. Lo que CKM agrega al paisaje — sin nombre previo

Los encuadres anteriores cubren correspondencias. Lo siguiente no tiene
nombre en ningún framework establecido:

### 4.1 Tensión como condición de cohesión

Ningún esquema de representación clásico tiene aristas negativas con función
**generativa**. En CKM, los pesos negativos de W_mixta sobre pares opuestos
no representan conflicto a resolver — son la condición que produce el Ω*
interior (densidad óptima) donde c(S) es máxima.

> Un grafo con tensión real y bien articulada tiene mayor cohesión
> que un grafo sin tensión.

Esto invierte la intuición estándar. En representación de conocimiento,
el conflicto es ruido o excepción. En CKM, la oposición es el motor.

### 4.2 Holonomía — residuo de amplitud, no de dirección

Los experimentos de holonomía (8 pares de alta asimetría) muestran:
- El atractor dominante es el mismo en A→B que en B→A (mismo en 8/8 pares)
- Pero la **fracción de nodos activos** difiere en +0.176 en 4/8 pares

La trayectoria no cambia a qué atractor converge — cambia cuánto del grafo
activa el atractor al que converge. Esto es **holonomía como residuo de amplitud**.

No existe equivalente en revisión de creencias, redes semánticas, ni inferencia activa.

### 4.3 Cohesión path-dependent (P1 + holonomía)

El sistema no tiene un estado único para cada densidad ρ — tiene dos estados
distintos según venga de incorporación o de remoción. La histéresis más
la holonomía producen un espacio de estados donde la trayectoria
es información irreducible. El sistema no puede ser caracterizado
solo por su estado presente — necesita su historia.

Ningún esquema de representación clásico incorpora esto.

### 4.4 Traza como constituyente del conocimiento

La traza de inferencia (Δ acumulado) no es metadata del proceso.
Es parte constitutiva del conocimiento mismo.

En el corpus N=32: traza_inferencia activa al inicio → +2.3 nodos promedio
en el atractor resultante. La orientación de la llegada modifica el estado alcanzable.

Esto es fenomenológicamente equivalente a "gota de tinta sobre tiza":
el proceso de formación del conocimiento transforma el medio en que opera.
La traza no puede separarse del resultado sin pérdida de información estructural.

---

## 5. Tabla de posicionamiento

| Framework | Origen | Conexión con CKM | Extensión CKM |
|-----------|--------|-----------------|---------------|
| IA simbólica/subsimbólica | Minsky, 1975+ | CKM es híbrido estructurado | Define el espacio intermedio sin nombre |
| Decl./procedimental | Luger & Stubblefield, 1998 | W ↔ declarativo, Δ ↔ procedimental | Separación verificada empíricamente |
| Restricciones de integridad | Davis et al., 1993 | Gatekeeper C1–C4 | M.M: restricción sobre el agente, no el dato |
| Revisión de creencias (AGM) | AGM, 1985 | P3 confirma asimetría contracción/expansión | Histéresis — path-dependencia no predicha por AGM |
| Argumentación abstracta | Dung, 1995 | Triadas C3, coercividad | Dinámica temporal de tensión bajo ruido |
| Espacios conceptuales | Gärdenfors, 2000 | VPs como geometría de perspectivas | R13: deformación sin desplazamiento de VP |
| Ferromagnetismo | Ising/Hopfield | Isomorfismo formal completo | P4: tensión produce cohesión (contra-intuitivo) |
| Inferencia activa | Friston, 2010 | ODA ↔ ciclo percepción-acción | β como propiedad del receptor, no del prior |
| Topología algebraica | Sciamarella, 2001 | H₀/H₁/H₂ sobre grafo CKM | R12: operador para inconmensurabilidad (abierto) |

---

## 6. Criterio definitorio

El criterio que distingue CKM de todos los frameworks anteriores no es técnico:

> La cohesión no se declara. Se mide como propiedad emergente
> de la estructura bajo perturbación.

Un sistema puede tener restricciones de integridad correctas, relaciones
bien tipadas, y ontología formalmente válida — y aun así tener cohesión fabricada.
La cohesión fabricada colapsa bajo ruido. La cohesión real resiste.

**Esta distinción es el núcleo empírico de CKM.**
No tiene nombre en ningún framework previo de representación del conocimiento.

---

*CKM · v25 · Mayo 2026 · gadanin.delamor*  
*Status: investigación activa. Predicciones P1–P6 verificadas. P7–P8 hipótesis pendientes.*  
*Subir al proyecto via "Agregar al proyecto". No copy-paste (Unicode).*
