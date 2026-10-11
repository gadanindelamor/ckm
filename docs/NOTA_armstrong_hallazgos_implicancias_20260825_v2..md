# NOTA_armstrong_hallazgos_implicancias_20260825_1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Post-experimento Armstrong boltzmann comparison v1*
*Correcciones incorporadas desde feedback Code Opus*
*Nota de trabajo — no REG*

---

## 1. COCO como componente siempre presente — implicancia de naming

### Lo que muestra el experimento

Con W_pos pura (baja densidad, pesos binarios, 33.6% de h exactamente 0 —
corpus WARMUP_TEXTS, N=20): **COCO tiene efecto real en los primeros ~3
STOPs** (delta_A = +34, +31, +24), y se agota cuando Δ_r cae por debajo
de ~0.05. Por debajo de ese umbral, Δ_r solo rompe empates y el conteo no
se mueve. ALPHA_MIN–ALPHA_MAX = [0.05, 0.30] cae justo en esa frontera.

Con W_mixta: tensión estructural real, pesos negativos que crean cuencas
profundas distintas. Δ_r puede alterar qué atractores son alcanzables.
COCO tendría efecto real más allá de esos primeros STOPs. **Propuesto —
no fue medido en este experimento. Toda la corrida fue W_pos (0 pesos
negativos, verificado).**

La pregunta operativa no es "¿hay COCO?" sino "¿el corpus tiene tensión
estructural suficiente para que la regulación de Δ_r importe, y por cuántos
STOPs?". Con W_pos: regulación real pero que se agota. Con W_mixta:
propuesto como sostenida — pendiente de corrida específica.

**Pregunta abierta:** los STOPs sobre Δ_r que ya no mueven el landscape
semántico — ¿dicen algo sobre el proceso de escritura independientemente
del landscape? No establecido. Dirección de observación posible.

### Naming — consecuencia directa

Si COCO es componente siempre presente:

```
panel["D_ckm"]                  ← MonitorService — herramienta de observación
panel["thermostat"]["D_ckm"]    ← COCO — conduce decisiones de STOP
```

Dos objetos distintos con el mismo nombre corto. Para mantener legibilidad
de los JOSONLs históricos existentes: **agregar `D_ckm_monitor` como alias,
no sustituir `D_ckm`**. Los trazos anteriores siguen siendo legibles.

### D_ckm del panel como herramienta de exploración

**Verificado en REG_armstrong_boltzmann_comparison_v1:**
`_combine_W_Delta` normaliza `Δ_r / max(Δ_r)`. STOP aplica `α·Δ_r` —
escalar uniforme. La normalización cancela el escalar por construcción.
D_ckm del panel fue 0.8857 idéntico en tres modos en las 19 evaluaciones
i=1 a i=19 (en i=0 el panel dio 0.0 con A0 aún diferido),
con Δ_r diferente en 14 órdenes de magnitud. Cancelación exacta, no
aproximada.

La diferencia D_ckm_coco − D_ckm_monitor podría ser señal de cuándo COCO
está teniendo efecto real vs. operando sobre Δ_r sin cambiar el campo
navegable. **Propuesto como dirección de exploración — no evaluado.**

---

## 2. A0 dominado por tie-breaking en corpus de baja densidad y pesos discretos

### Corpus del experimento — no W_ckm_corpus_v2.json

**El corpus del experimento es WARMUP_TEXTS (N=20), no W_ckm_corpus_v2.json.**
Son dos corpus distintos:

| corpus | N | densidad | valores no-nulos | h=0 en primer paso |
|---|---:|---:|---|---:|
| WARMUP_TEXTS | 20 | 0.126 | {0.5, 1.0} | 33.6% |
| W_ckm_corpus_v2.json | 32 | 0.756 | 95 distintos, max 0.053 | 1.5% |

### El hallazgo y su alcance

En WARMUP_TEXTS: `_relax` conserva σ_i cuando h_i = 0. El 33.6% de nodos
empatados quedan congelados en su valor de σ₀. count(W) = 174 con la regla
actual; 61 resolviendo a +1; 60 a -1. **Factor ~3 — A0 está dominado por
tie-breaking.**

**El hallazgo NO transfiere a W_ckm_corpus_v2.json.** Con ese corpus
(1.5% empates): count(W) = 5 con la regla actual, 5 resolviendo a +1.
El factor ~3 desaparece.

El qualifier para DEFS §11 debe especificar cuándo aplica: corpus con
alta sparsidad y pocos valores distintos no-nulos. No como propiedad
general de `_count_attractors`.

### Por qué la regla actual es correcta

La regla "conserva σ cuando h=0" es la que garantiza convergencia
(Lyapunov/LaSalle, DEFS §4). Cambiarla no es local — rompería la garantía.
**No se toca.** El tie-breaking es información sobre la estructura del
corpus, no ruido a corregir.

### Matiz sobre el título

"A0 mide diversidad de tie-breaking, no de cuencas de energía" es más fuerte
que los datos. Con empates resueltos el conteo da ~60, no ~1. El
tie-breaking **domina la diferencia** (174 → 60) pero no explica todo lo
que se cuenta. El cuerpo ("dominado por") es el que se sostiene.

---

## 3. Estado absorbente de STOP — no es catástrofe

### Lo que ocurre

Δ_r cae a ~1e-14. STOP multiplica por α pero no puede cambiar el soporte
(patrón de no-ceros). En ese régimen el conteo depende del soporte, no de
la magnitud. D_ckm_coco queda estructuralmente por encima de 0.40.
Piso: (174-64)/174 = 0.632.

COCO sigue aplicando STOP en las 20 evaluaciones sobre una Δ_r que ya
no puede mover el landscape.

### Sobre delta_A — en contexto correcto

delta_A fue negativo en 4/20 STOPs (uniform) y 6/20 (boltzmann) — registrado
en REG. Todos los negativos caen en el régimen inerte (i≥5, Δ_r≤1e-3) y son
del orden de la oscilación propia del estimador (±2-3, medida en REG:
62/65/64 para magnitudes 0.05/1e-6/1e-14 sobre el mismo soporte). Los STOPs
que movieron el campo real dieron +34, +31, +24 — ninguno negativo.

Los negativos existen y están registrados. No son pérdidas estructurales.
La afirmación histórica "STOP nunca produce pérdida" no queda refutada por
estos negativos.

**Aclaración sobre frac_rec:** el frac_rec del REG_destruccion_recuperacion_v1
es max_α[A_post(α)]/A0 — el máximo sobre α, no el valor runtime. El frac_rec
en runtime de esta corrida va de 0.05 a 0.68 y nunca llega a 1.0 en ningún
modo. Son dos métricas distintas que no deben compararse directamente.

"OPERADOR_STOP_COCO nunca produce pérdida" se sostiene en su contexto
original. Esta corrida no lo refuta — pero tampoco lo confirma para el
régimen W_pos de baja densidad.

### Sobre el umbral 0.40 — pregunta respondida en el repo

`REG_destruccion_recuperacion_v1.md:39` — calibrado con W_mixta AMP=40.
No es pregunta abierta: es asimetría documentada entre calibración (W_mixta,
donde el instrumento tiene efecto real) y uso actual (W_pos, donde el piso
estructural queda por encima del umbral).

---

## Pendientes derivados de esta nota

- **Agregar alias `D_ckm_monitor`** en MonitorService (no sustituir D_ckm)
- **DEFS §11**: qualifier sobre tie-breaking acotado a corpus de alta
  sparsidad y pesos discretos — con especificación de cuándo aplica
- **DEFS §10**: distinguir D_ckm_coco vs D_ckm del panel explícitamente,
  con la asimetría de calibración documentada
- **Corrida con W_mixta**: verificar si COCO tiene efecto real en ese régimen
  (§1 lo propone, no lo mide)
- **Exploración futura**: diferencia D_ckm_monitor − D_ckm_coco como señal
  de efectividad de la regulación

---

*Fuente: REG_armstrong_boltzmann_comparison_v1.md (Code Opus, Ago 2026)*
*Feedback Code Opus incorporado: 5 correcciones sobre versión anterior*
*No commit hasta instrucción de delamor*
