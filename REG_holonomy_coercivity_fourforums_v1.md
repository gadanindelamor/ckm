# REG_holonomy_coercivity_fourforums_v1

*CKM — Holonomía y Coercividad en red fourforums gun control*
*2026-05-08*

---

## Experimento 1 — Holonomía: ¿el camino importa?

**Pregunta:** iniciar con el atacante activo vs el sostenedor activo.
¿Convergen al mismo atractor dominante?

**Setup:** 8 pares de alta asimetría (|asim| > 0.85). 300 runs por condición.
Condición A: atacante activo (+1), sostenedor inactivo (-1).
Condición B: sostenedor activo (+1), atacante inactivo (-1).

### Resultados

| Par (atacante→sostenedor) | Asim  | Atractor dominante | Δ fracción activa |
|--------------------------|-------|-------------------|-------------------|
| 1034→965                 | -1.00 | MISMO             | +0.176            |
| 3452→965                 | -1.00 | MISMO             | +0.000            |
| 115→1034                 | +1.00 | MISMO             | -0.176            |
| 751→965                  | +1.00 | MISMO             | +0.176            |
| 115→555                  | +1.00 | MISMO             | +0.000            |
| 809→965                  | +0.987| MISMO             | +0.000            |
| 150→751                  | +0.960| MISMO             | -0.176            |
| 3452→809                 | -0.891| MISMO             | +0.000            |

**Pares con atractor dominante distinto:** 0/8

### Hallazgo: holonomía en amplitud, no en identidad

El atractor dominante es el mismo independientemente del camino.
Pero el Δ fracción activa es consistentemente no-nulo: **0.176** en 4/8 pares.

El camino no cambia QUÉ atractor domina.
El camino cambia CUÁNTOS nodos se activan.

Convergencia con Experimento B2 (CKM N=32):
traza_inferencia activa al inicio → +2.3 nodos en promedio.
Mismo mecanismo: el residuo holonómico es de amplitud, no de dirección.

**La holonomía del dominio gun control es de tamaño, no de identidad.**

---

## Experimento 2 — Coercividad: punto de ruptura de tríadas C3

**Pregunta:** ¿cuánto ruido necesita una tríada C3 para colapsar?
Barrido: ruido ∈ {0%, 5%, 10%, 15%, 20%, 30%, 40%, 50%}
Estado inicial: tríada en tensión (signos alternados).
Colapso = todos los nodos de la tríada en el mismo signo.

### Resultados

**Tríadas con Author 965 (ancla estructural):**

| Tríada            | Ruptura  | Curva (0%→50% ruido)                    |
|-------------------|----------|-----------------------------------------|
| (150, 965, 1034)  | >50%     | 0.00 constante hasta 50%                |
| (555, 965, 1034)  | >50%     | 0.00 constante hasta 50%                |
| (150, 555, 965)   | >50%     | 0.00→0.26 (máx 26% a 50% ruido)         |

**Tríada sin Author 965:**

| Tríada             | Ruptura  | Curva (0%→50% ruido)                    |
|--------------------|----------|-----------------------------------------|
| (150, 501, 1443)   | —        | 1.00 constante (ya colapsada a ruido=0) |

### Hallazgo: dos regímenes de resistencia

**Con 965:** colapso ≈ 0.00 hasta 50% de ruido.
La tríada no colapsa bajo ninguna perturbación probada.

**Sin 965:** colapso = 1.00 a ruido = 0.
La tríada está colapsada antes de que empiece el experimento.
No tiene tensión que sostener.

### Interpretación estructural

Author 965 no es un ancla pasiva.
Es el elemento que **mantiene la tensión de la tríada activa**.

Sin 965, la tríada resuelve inmediatamente (colapso espontáneo).
Con 965, la tríada resiste perturbación extrema (coercividad alta).

En términos ferromagnéticos:
- 965 = eje duro de magnetización
- Tríadas con 965 = material con alta coercividad
- Tríadas sin 965 = material blando (colapsa con campo mínimo)

**965 es la condición que mantiene al lobo y al cordero indemnes.**
Su función estructural es sostener la tensión, no resolverla.

---

## Síntesis: dos propiedades del manifold fourforums

| Propiedad         | Resultado                          | Mapa CKM               |
|-------------------|------------------------------------|------------------------|
| Holonomía         | En amplitud (+0.176), no identidad | B2: traza_inferencia   |
| Coercividad       | 965 = coercividad máxima           | Mr (remanencia)        |
| Resistencia tríada| Con 965: >50% ruido; sin 965: 0%   | Umbral de rotación VP  |

---

*Experimento ejecutado sobre fourforums_delta.json (36 pares C1-C5+C7+C8)*
*Sin SQL requerido. Reproducible.*
