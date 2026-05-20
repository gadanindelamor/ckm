# REG — Sesión: Perspectivas, RP² y Fourforums v7
*CKM v4 — Mayo 2026*

---

## 1. Operaciones sobre perspectivas en CKM — estado actual

### Definidas y verificadas experimentalmente

| Operación | Descripción | Estado |
|---|---|---|
| **Unión** G[A∪B] | Ambas perspectivas activas simultáneamente. Produce atractor propio con c(S) > perspectivas puras. G[A∪B] ≠ G[A] + G[B] | Verificado (Escenario 3, v11) |
| **Intersección** A∩B | Nodos bisagra: fundamentan_a>0 y dependen_de>0. Pertenecen a ambas perspectivas | Implementado |
| **Contacto R13** | Deformación del campo local sin mover VP. Bilateral, asimétrico, irreversible. Sin operación inversa | Definido |
| **Divergencia** R10/R11 | Derivada del campo vectorial. Tiene signo y magnitud local | Definido |
| **Dos umbrales R13** | Hc: deformación de M sin rotar VP. Umbral de rotación: VP se mueve — evento cualitativamente distinto | Definido |

### No definidas formalmente
- Composición secuencial de perspectivas
- Métrica entre VPs
- Operación inversa del contacto

---

## 2. Marco proyectivo RP² — dirección de formalización

### Fundamento
El concepto VP (vanishing point) en CKM fue tomado explícitamente de la geometría proyectiva.
Una perspectiva P tiene VP = punto p en RP².

### Operaciones proyectivas candidatas

**Join**: dados dos VPs, p_A ∨ p_B = la línea l_AB que los une.
→ Candidato formal para G[A∪B]: ambos VPs activos generan l_AB.
Lo que emerge en el cruce pertenece a l_AB, no a p_A ni a p_B.
Esto espeja R13: "lo que emerge pertenece al campo, no al grafo."

**Meet**: dadas dos líneas (ejes de tensión), l_AB ∧ l_CD = punto q.
→ Candidato para VP emergente del cruce de dos tensiones. Pendiente verificación.

**Haz de rectas (pencil of lines)**: múltiples líneas de tensión convergiendo en un mismo punto p.
→ Observado empíricamente en fourforums v7 (ver sección 3).

### Estado de la formalización
- Join como G[A∪B]: **dirección, no correspondencia probada**.
  CKM opera sobre grafos discretos; RP² sobre espacio continuo.
  La correspondencia requiere mapa formal explícito — pendiente.
- Haz de rectas: **observado en datos, interpretación proyectiva sugerida**.

---

## 3. Fourforums v7 — hallazgos

### Pipeline establecido
```
C1-C5 (protocolo elicitación, red raw) → primario
C7 (MTurk agree < 0.35) + C8 (in-degree ≥ 2) → secundario
```

**Nota de nomenclatura**: en el mensaje original de diseño del pipeline,
C1="desacuerdos explícitos" y C2="centralidad propia" eran shorthand local —
son C7 y C8 en el protocolo extendido.

### Resultados

| Filtro | Pares |
|---|---|
| C1+C2 (desacuerdo + centralidad) | 169 |
| C4+C5 (asimetría + persistencia) | 137 |
| C3 (tríada crítica) | 137 |
| **C1-C5 total** | **137** |
| + C7 (MTurk explícito) | 36 |
| + C8 (in-degree global) | **36** |

N=36 pares, 9,757 interacciones totales. Todos con C3=✓.

### Hallazgo estructural principal: Author 965

Author 965 emerge como **polo sostenedor estructural puro**:
- Asimetría -1.0 contra 1034 (0 emitidos / 111 recibidos)
- Asimetría -1.0 contra 3452 (0 / 103)
- Asimetría +0.987 de 809→965 (154 vs 1)
- Aparece como C3 (tercero crítico) en la mayoría de los pares

**En términos proyectivos**: múltiples ejes de tensión l_AB convergen en o cerca de p_965.
Estructura de haz de rectas (pencil of lines) con centro en p_965.
El haz es verificable desde los datos — no es interpretación.

### Top iniciadores (polo atacante)
Author 555: 5 pares como iniciador. In-degree 2776.

### Pendiente
Cruce author_ids top (965, 555, 150, 751, 1034...) con `mturk_author_stance`
para determinar si el polo atacante (555) es pro_control o anti_control.
Esto responde directamente la pregunta C6c.

---

## 4. Extensiones del protocolo de elicitación

| Criterio | Definición | Contexto |
|---|---|---|
| **C7** | Par tiene ≥1 interacción con agree < 0.35 (MTurk) — desacuerdo declarado por annotadores externos | Corpus social anotado |
| **C8** | Ambos autores tienen in-degree > umbral en red gun control global — existen más allá de este par | Corpus social |

C6: pendiente definición.
C7 y C8 son adicionales a C1-C5, no reemplazos.

---

## 5. Scripts producidos

| Script | Función |
|---|---|
| fourforums_delta_v5.py | Quote table directo, sin MTurk, N=1488 |
| fourforums_delta_v7.py | Pipeline C1-C5 + C7+C8, N=36 pares verificados |
| REG_c6c_fourforums_v1.md | Documentación de extracción v1-v5 |

---

## 6. Zoom out de la sesión

La sesión arrancó con sesgo de ejecución (corriente automática) sobre
el obstáculo técnico del dump SQL. El giro ocurrió al nombrar el eje
real de tensión: ¿es la arquitectura T1-ataca/T7-resiste una propiedad
del dominio o un artefacto del corpus?

Esa pregunta produjo el pivot al pipeline mínimo (stance directo →
quote table → C1-C5+C7+C8), que eventualmente dio datos estructurales
verificables.

La pregunta de la formalización proyectiva quedó abierta como dirección
de trabajo — no como marco establecido.
