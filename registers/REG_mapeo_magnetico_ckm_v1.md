# REG_mapeo_magnetico_ckm_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Ago 2026. Exploración de analogías entre física magnética
(histéresis, ferromagnetismo, antiferromagnetismo, ferrimagnetismo,
temperatura de Néel, coercitividad) y el modelo CKM. Emergieron
propuestas de elicitación estructural de pares negativos y criterio
de admisión de W_mixta.

---

## 1. Mapeo CKM — Física Magnética (verificado / propuesto)

### 1.1 W_pos — ferromagnética

W_pos es ferromagnética: todos los nodos tienden a alinearse en el
mismo atractor bajo campo uniforme. Sin oposición estructural, el
sistema colapsa hacia saturación.

### 1.2 W_mixta — sistema con interacciones competidoras

W_mixta no es antiferromagnética pura. Es fondo ferromagnético (W_pos)
más pares negativos selectivos entre T0 y T1. Más cerca del
**ferrimagnetismo** que del antiferromagnetismo puro: las dos subredes
tienen orientación opuesta pero el momento resultante no se cancela.
T0 o T1 dominan según condiciones — no hay cancelación simétrica.

Los pares negativos codifican la interacción antiferromagnética en la
frontera entre subredes. El fondo ferromagnético preserva la cohesión
interna de cada subred.

### 1.3 T0 / T1 — subredes con acoplamiento competidor

T0 / T1 son las dos subredes con acoplamiento interno ferromagnético
e interacción intersubred competidora. Son los dominios magnéticos del
sistema. En las fronteras entre dominios existe energía potencial.

### 1.4 Nodo 965 — nodo bridge en la frontera

El nodo 965 (ratio in/out > 100×, out-degree ≈ 0) es candidato
estructural al rol de nodo bridge en la frontera T0↔T1.
**Propuesto — requiere verificación topológica contra la red real.**

### 1.5 P4 — resistencia al colapso por frustración

P4 verificado (N=32): W_mixta mantiene más atractores accesibles que
W_pos bajo igual acumulación. La frustración entre interacciones
competidoras genera más cuencas de atracción — resiste el colapso en
saturación por ese mecanismo, no por antiferromagnetismo puro.

### 1.6 β_c vs temperatura de Néel

β_c en CKM es el punto crítico ferromagnético (tipo Curie) —
temperatura donde el orden global se destruye.

La temperatura de Néel es el punto donde T0/T1 dejan de ser
distinguibles como subredes — cantidad distinta, potencialmente
más alta que β_c en un sistema con interacciones competidoras.

**Propuesto — no equivalente a β_c. No verificado.**

### 1.7 Lazo de histéresis — coercitividad CKM

El lazo P1 traza c(S) vs ρ en rama UP (incorporación) y DOWN
(remoción). La coercitividad CKM es legible del mismo lazo: valor
de Δ_r acumulado donde el sistema pierde su atractor actual —
análogo al campo coercitivo magnético (valor donde la magnetización
cruza cero en el lazo).

Datos disponibles en `hopfield.py` (`hysteresis_loop()`). Análisis
gráfico sobre datos existentes, sin experimento nuevo.

| N | Área lazo | Max Δc(S) en ρ | p-valor |
|---|---|---|---|
| 16 | 0.0156 | — | confirmado |
| 32 | 0.000862 | 0.001308 en ρ=0.469 | p≈0 |
| 64 | 0.000367 | en ρ=0.547 | p≈0 |

---

## 2. P4 N=64 — reencuadre

P4 no es problema de escala — es problema de densidad de tensión.

Sweep k* sobre W sintética densa identificó el umbral donde la ventaja
de W_mixta sobre W_base reaparece en N=64:

| k (pares neg) | ratio | ventaja |
|---|---|---|
| 18 | 0.009 | −0.000498 ✗ |
| 36 | 0.018 | −0.000404 ✗ |
| **54** | **0.027** | **+0.000068 ✓** |
| 60 | 0.030 | +0.000282 ✓ |
| 72 | 0.036 | +0.000502 ✓ |

fourforums: 60 pares verificados → ratio=0.030 > k*=54. El corpus
real está por encima del umbral.

**Apertura:** k*=54 fue hallado en W sintética con estructura
uniforme. En corpus real con bimodal A/B, pares negativos entre nodos
Grupo A (fi alto) tienen impacto desproporcionado — k* efectivo
podría ser menor. No verificado contra fourforums.

---

## 3. Propuestas emergentes

### 3.1 SALAMANCA — criterio de admisión de tensión estructural

*Estado: propuesto.*

Criterio previo a la construcción de W_mixta. Detecta si W_pos tiene
naturaleza estructural adversarial — si hay partición T0/T1 con cut
bajo en W_pos, o no.

La pregunta es binaria: ¿hay estructura adversarial suficiente para
justificar pares negativos?

- Si sí → identificar frontera → construir W_mixta.
- Si no → W_pos es la respuesta correcta. W_mixta no tiene objeto.

**P4 + SALAMANCA = criterio de admisión de tensión estructural,
no de construcción de matriz.**

Operar sobre W acumulada (no en cada ingestión — la partición no
es estable hasta que W converge).

### 3.2 Graph cut como métrica de separabilidad

*Estado: propuesto.*

`cut(T0, T1) = Σ W_ij para i∈T0, j∈T1`

Mide el peso total de aristas que cruzan la frontera entre subredes.
Cut bajo = subredes separadas = estructura adversarial presente.

Procedimiento SALAMANCA con graph cut:

1. W_pos construida, clusters T0/T1 no declarados.
2. Barrer umbral de peso θ: W_θ = W con aristas < θ zeroed.
3. En cada θ: detectar componentes conexas o particionar por mínimo cut.
4. θ_crítico = θ donde el mínimo cut colapsa (T0/T1 se funden).
5. La partición justo antes del colapso identifica T0/T1 sin
   conocimiento editorial previo.
6. Los pares con W_ij > 0 que cruzan esa partición son candidatos
   a pares negativos.

Implementación: `nx.minimum_cut(G, s, t, capacity='weight')` requiere
semilla s∈T0, t∈T1. Sin semilla: normalized cut espectral.

**Problema huevo/gallina:** min-cut requiere s,t de subredes distintas.
Si T0/T1 no están declarados, la semilla no existe. Alternativa
espectral no lo requiere.

### 3.3 Temperatura de Néel como criterio de elicitación

*Estado: propuesto.*

Procedimiento alternativo a graph cut para identificar pares negativos
sin conocimiento previo:

1. Construir W_pos desde el corpus — sin pares negativos.
2. Barrer β de alto a bajo (frío → caliente).
3. En cada β: correr `find_attractors`, medir separabilidad
   c(S) interno T0 vs c(S) cruzado T0×T1.
4. β_Néel efectivo = β donde la separabilidad colapsa.
5. Los pares (i,j) en clusters opuestos que pierden su oposición
   en β_Néel son candidatos a pares negativos.

Depende de que los clusters T0/T1 emerjan del propio barrido.
Si no emergen, el criterio no tiene objeto.

---

## 4. Aperturas registradas

- Coercitividad CKM: análisis gráfico del lazo P1 pendiente.
- k* real vs k* sintético: verificar si bimodal A/B reduce el
  umbral efectivo en fourforums.
- SALAMANCA: operacionalización como servicio o paso de análisis.
- Temperatura de Néel efectiva: relación con β_c — dos cantidades
  distintas en sistema con interacciones competidoras.
- 965 como nodo bridge: verificación topológica pendiente.

---

*Verificado contra datos: P1 (EXPERIMENTS.md), P4 sweep (p4_neg_sweep.py),*
*fourforums 60 pares (REG_p4_fourforums_guncontrol_v1).*
*Propuestas: SALAMANCA, graph cut, Néel elicitación — no verificadas.*
