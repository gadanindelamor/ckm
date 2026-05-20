# Informe de Lectura — Tesis Sciamarella (2001)
## Aplicabilidad al CKM — BE Framework

**Referencia:** Sciamarella, Denisse. *Estructura topológica de flujos caóticos*. Tesis Doctoral. FCEyN, UBA. Director: Dr. Gabriel B. Mindlin. 7 de mayo de 2001. 164 páginas.

**Contexto de consulta:** Experimento 64 / Sesión 17 N64. CKM_Informe_Trabajo_v4. Arquitectura BP/PC + Hopfield + k-core/bootstrap percolation. Gap abierto: representación de nodos como vectores. Pregunta abierta: función de perspectivas deformes (múltiples VPs) en el grafo cohesivo.

---

## 1. RESUMEN DE LA TESIS

### 1.1 Problema central

Dado un sistema dinámico que opera en régimen caótico, se tiene una serie temporal de observaciones escalares. La pregunta es: ¿cómo extraer invariantes topológicos que determinen los mecanismos de plegado y estirado responsables de generar esos datos, para un sistema de dimensionalidad arbitraria?

Las técnicas previas (linking numbers, rates de rotación relativas, nudos) fallaban ante:
- dimensionalidad > 3 del espacio de fases,
- series temporales cortas o ruidosas.

### 1.2 Solución propuesta

La tesis construye una técnica de análisis topológico basada en **grupos de homología** que supera ambas restricciones.

El método tiene tres pasos:

**Paso 1 — Construcción de parches:** Los datos caóticos se cubren localmente con parches (patches) bidimensionales mediante triangulación de Delaunay. Cada parche es una aproximación local de la variedad invariante visitada por la trayectoria.

**Paso 2 — Ensamble del complejo celular:** Los parches se pegan entre sí mediante reglas algorítmicas explícitas, formando un complejo de celdas orientado. Este complejo es el "esqueleto" de la variedad invariante — su caricatura algebraica.

**Paso 3 — Cálculo de invariantes:** Sobre el complejo se calculan:
- **Grupos de homología** H₀, H₁, H₂... Hₙ — invariantes escalados por dimensión
- **Cadenas de orientabilidad** — detectan torsiones en las ramas

Los grupos de homología codifican:
- **H₀** → número de componentes conexas
- **H₁** → número de "agujeros" o lazos independientes (bucles no contractibles)
- **H₂** → número de cavidades cerradas

Las cadenas de orientabilidad distinguen estructuras que los grupos de homología solos no discriminan (e.g., cilindro vs. cinta de Möbius tienen los mismos grupos H pero diferente torsión).

### 1.3 Propiedades clave del método

- **Invarianza topológica:** los grupos son independientes de la descomposición en celdas utilizada.
- **Robustez ante perturbaciones:** los invariantes no cambian ante variaciones de parámetros de control.
- **Extensión a cualquier dimensión:** no hay restricción dimensional.
- **Aplicabilidad a series cortas y ruidosas:** la técnica no requiere órbitas periódicas reconstruidas.

### 1.4 Aplicaciones realizadas

| # | Sistema | Dimensión | Hallazgo |
|---|---------|-----------|----------|
| 1 | Sistema 3D integrado numéricamente | 3D | Variedad con 3 ciclos no triviales, dos asas sobre un disco. Reproduce resultados conocidos. |
| 2 | Sistema 4D integrado numéricamente | 4D | Rama que se bifurca con torsión media. Primer análisis topológico de flujo 4D. |
| 3 | Serie experimental — vocal 'a' de "casa" | empírica | Estructura compatible con foco-ensilladura + reinyección rápida. Potencial para huella digital topológica de locutor. |
| 4 | Suspensión del mapa cúspide (4D) | 4D | Ramas sin torsión (sin cadenas de orientabilidad). Definición de invariante homológico para este tipo de flujo. |

### 1.5 Aporte original definido en la tesis

> *El elemento matemático que permite calcular las eventuales torsiones de las ramas de una variedad ha sido definido por primera vez en este trabajo.*

Las **cadenas de orientabilidad** son un nuevo objeto matemático introducido en esta tesis como extensión de los grupos de homología.

---

## 2. ANÁLISIS DE APLICABILIDAD AL CKM

### AWARENESS — Pausa antes de las conexiones

Las conexiones que siguen son **analogías estructurales**, no identidades. El CKM trabaja con conocimiento semántico; la tesis trabaja con flujos caóticos en espacios de fases físicos. Las conexiones tienen valor heurístico y generativo — no son transferencias directas de resultados. Se indica explícitamente el nivel de confianza en cada caso.

---

### 2.1 Invariantes topológicos del grafo CKM [confianza: ALTA]

Los grupos de homología son computable directamente sobre el grafo de conocimiento del CKM, sin necesidad de adaptación especial.

Para el grafo CKM G = (N, E):

- **H₀(G):** número de componentes conexas. Indica si el grafo cohesivo es unitario o fragmentado. Un CKM con H₀ > 1 tiene islas de conocimiento no conectadas.
- **H₁(G):** número de ciclos independientes (lazos no contractibles). En el CKM, cada ciclo H₁ es un conjunto de nodos que se sostienen mutuamente en un bucle cerrado. Son los "núcleos de cohesión" — pueden coincidir conceptualmente con los k-cores.
- **H₂(G):** cavidades cerradas. Estructuras donde hay un "interior vacío" en el grafo. Posiblemente relevante para detectar zonas del CKM donde falta conocimiento intermedio.

**Relevancia para el Experimento 64:** Antes de correr el experimento Hopfield-kcore, calcular H₀, H₁, H₂ del corpus CKM provee un perfil topológico de referencia. Si el experimento modifica el grafo, los invariantes pre/post son métricas de cambio estructural verificables.

**Costo de implementación:** muy bajo. Networkx en Python tiene funciones directas para computar homología simplicial sobre grafos.

---

### 2.2 La variedad enramada como análogo del k-core [confianza: MEDIA]

En la tesis, el **templado** (variedad enramada) es el esqueleto mínimo que contiene toda la dinámica del sistema. Las ramas del templado son los generadores homológicos H₁.

En el CKM, el **k-core** es el subgrafo mínimo donde cada nodo tiene al menos k vecinos cohesivos. Es el equivalente funcional: el "esqueleto" que sostiene la cohesión.

**Analogía específica:**
- Ramas del templado = componentes del k-core
- Reconexión de ramas al disco central = la forma en que los sub-k-cores se conectan al núcleo principal
- Torsión de una rama = un nodo o arista que "tuerce" la orientabilidad del subgrafo (posiblemente: una perspectiva que invierte relaciones)

**Caveat (A2):** Esta analogía es heurística. Los k-cores son conjuntos de vértices; las ramas del templado son variedades continuas. La traducción formal requiere trabajo adicional.

---

### 2.3 Cadenas de orientabilidad → perspectivas deformes [confianza: MEDIA-ALTA]

Esta es la conexión más directa con la pregunta abierta del CKM sobre **perspectivas deformes (múltiples VPs)**.

En la tesis: las **cadenas de orientabilidad** detectan torsiones que los grupos de homología solos no ven. Un cilindro y una cinta de Möbius tienen los mismos H₀, H₁, H₂ — se distinguen solo por la torsión. La torsión indica que la variedad "se tuerce" al cerrar el bucle.

En el CKM: si una perspectiva VP es el Máximo Subgrafo Inducido por los nodos disponibles (propuesta R09), entonces una **perspectiva deformada** podría ser aquella donde al recorrer el subgrafo se llega al mismo nodo pero con una orientación invertida — es decir, donde la perspectiva contiene una inversión semántica interna.

**Propuesta concreta:** Las cadenas de orientabilidad podrían ser el operador buscado para R12 — el que distingue divergencia resoluble de inconmensurabilidad estructural. Una diferencia entre dos perspectivas que tiene torsión nula (cilindro) es resoluble; una diferencia con torsión (Möbius) es estructuralmente incommensurable.

**Esto formaliza la pregunta abierta:**
> ¿Cuándo dos perspectivas son equivalentes y cuándo son inequivalentes?

Respuesta posible: son equivalentes si sus invariantes homológicos son iguales (mismos H₀, H₁, H₂ y mismas cadenas de orientabilidad). Son inequivalentes si difieren en algún invariante. Dentro de la inequivalencia: la diferencia es **resoluble** si difieren solo en H₀ o H₁ (topología de conexiones), y es **incommensurable** si difieren en torsión (orientabilidad estructural).

---

### 2.4 Descomposición en parches → vectorización de nodos [confianza: MEDIA]

En la tesis, el paso más delicado es construir los parches locales que cubren los datos antes de ensamblar el complejo. Los parches son aproximaciones locales de la variedad usando triangulación de Delaunay sobre los puntos de datos.

En el CKM, el gap abierto es: **cómo representar los nodos como vectores**.

La tesis sugiere una estrategia:
1. No es necesario representar toda la variedad a priori — basta con cubrir localmente los datos con parches.
2. La triangulación de Delaunay provee cobertura local óptima con mínimas asunciones globales.

**Traducción al CKM:** en lugar de embedder todos los nodos del corpus en un espacio vectorial de una vez, se podrían definir "parches conceptuales" — subconjuntos locales de nodos con alta cohesión mutua — y trabajar localmente. El ensamble global emerge del pegado de parches, no de una representación global a priori.

Esto podría resolver el bootstrap problem parcialmente: no se necesita la representación global para empezar; se trabaja localmente y se ensambla.

---

### 2.5 Equivalencia de atractores → equivalencia de estados de conocimiento [confianza: MEDIA]

La pregunta central de la tesis (¿son equivalentes dos atractores extraños?) tiene un análogo directo en CKM:

> ¿Cuándo dos estados del grafo CKM son "el mismo conocimiento" y cuándo son estructuralmente distintos?

Si se computan los invariantes homológicos de dos versiones del CKM (e.g., antes y después de un experimento, o dos instancias de CKM en agentes distintos), se puede decidir si son topológicamente equivalentes sin necesidad de comparar nodo a nodo.

Esto tiene aplicación directa para los escenarios MCP multi-agente (cierre de la sesión anterior): dos agentes CKM con grafos diferentes pueden tener la misma estructura topológica (mismos invariantes) aunque sus nodos sean distintos — son equivalentes en términos de coherencia global.

---

### 2.6 Series temporales cortas y ruidosas → corpus CKM pequeño [confianza: ALTA]

La tesis fue explícitamente diseñada para trabajar con datos limitados. El corpus CKM es pequeño. Esto no es un obstáculo para la técnica homológica — es exactamente el escenario para el que fue construida.

**Relevancia directa:** el método de la tesis no requiere muchos nodos para ser aplicable. Funciona con el conjunto disponible.

---

## 3. TABLA DE CONEXIONES CKM ↔ TESIS

| Concepto en Tesis | Análogo en CKM | Nivel de formalización |
|---|---|---|
| Grupos de homología H₀, H₁, H₂ | Invariantes topológicos del grafo CKM | Directamente computable |
| Templado / variedad enramada | k-core del grafo cohesivo | Analogía funcional robusta |
| Cadenas de orientabilidad (torsión) | Operador para perspectivas deformes | Propuesta formal — requiere definición |
| Equivalencia de atractores | Equivalencia de estados de conocimiento entre agentes | Aplicable en MCP multi-agente |
| Descomposición en parches | Vectorización local de nodos (alternativa al embedding global) | Estrategia viable para Exp. 64 |
| Series cortas y ruidosas | Corpus CKM pequeño | Validación de viabilidad |
| Cadenas de torsión distinguiendo Möbius de cilindro | R12: divergencia resoluble vs. incommensurabilidad | Candidato a operador formal para R12 |

---

## 4. RECOMENDACIONES PARA EL EXPERIMENTO 64

### 4.1 Acción inmediata viable (sin vectorización previa)

Calcular los grupos de homología H₀, H₁, H₂ del grafo CKM actual usando el corpus como grafo discreto. Esto no requiere vectorizar nodos — opera sobre la estructura de aristas directamente.

```python
import networkx as nx
# CKM corpus como grafo G = (nodos, aristas_de_cohesión)
# Calcular componentes conexas (H₀)
# Calcular ciclos independientes (H₁ via cycle_basis)
# Registro de invariantes antes del experimento Hopfield
```

Esto da un **baseline topológico verificable** antes de correr la red Hopfield.

### 4.2 Orientabilidad como operador para R12

Definir formalmente: dadas dos perspectivas VP_1 y VP_2 (como subgrafos inducidos del CKM), computar si la diferencia entre ellas tiene torsión o no.

- Sin torsión → divergencia resoluble (H₁ diferente, misma orientabilidad)
- Con torsión → incommensurabilidad estructural (diferente orientabilidad)

Este operador cierra R12 de manera computacionalmente concreta.

### 4.3 Estrategia de parches para vectorización

En lugar de embedder todo el corpus en un espacio vectorial de golpe, construir "parches conceptuales": vecindarios locales de 3-5 nodos con alta interdependencia, vectorizarlos localmente, y ensamblar. La triangulación de Delaunay en espacio semántico puede ser el mecanismo de pegado.

---

## 5. EVALUACIÓN GENERAL

La tesis de Sciamarella es relevante para el CKM en tres niveles distintos:

**Nivel 1 — Herramientas directamente aplicables:** los grupos de homología sobre el grafo CKM son computable ahora, sin inversión técnica mayor. Proveen métricas objetivas del estado topológico del conocimiento.

**Nivel 2 — Marco conceptual para preguntas abiertas:** las cadenas de orientabilidad ofrecen una formalización precisa para la pregunta sobre perspectivas deformes y el operador R12. Es el candidato más sólido encontrado hasta ahora para ese gap.

**Nivel 3 — Estrategia de vectorización:** la descomposición en parches es una alternativa viable al embedding global, que puede desbloquear el Experimento 64 sin resolver primero el problema de representación completo.

**Lo que la tesis no resuelve para el CKM:** la semántica. Los invariantes homológicos capturan estructura, no significado. El puente entre la topología del grafo y la cohesión semántica sigue siendo una decisión conceptual del CKM, no una consecuencia de la técnica.

---

*Informe generado en contexto de sesión Experimento 64 / CKM_Informe_Trabajo_v4. Fecha: Mayo 2026.*
