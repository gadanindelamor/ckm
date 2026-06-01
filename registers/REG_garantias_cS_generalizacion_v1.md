# REG_garantias_cS_generalizacion_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Función `c(S)*(N, ρ_corr)` — derivación y verificación empírica

### Forma analítica

```
c(S)*(N, ρ_corr) = μ_W(N, ρ_corr) · r(zona, ρ)

μ_W(N, ρ_corr) ≈ C · ρ_corr / N     [escala con corpus]
r = c(S) / μ_W                        [factor de alineación — medible en tiempo real]
```

**Nota derivación:** La forma clásica Hopfield `c(S)* = 1/N + α·ρ_corr²` (Hebb rule,
patrones binarios no correlacionados) **no aplica** a W de co-ocurrencia CKM.
Verificado empíricamente: predice valores 10–20× mayores que los observados.
La forma correcta para co-ocurrencia es la basada en μ_W.

### Datos empíricos base (N=32, corpus CKM W_ckm_corpus_v2.json)

```
μ_W = 0.004519
W range: [0.0, 0.0529]
ρ_corr (correlación pairwise de filas W): 0.527 ± 0.266
```

---

## Tres garantías formales (n=500 secuencias, N=32)

### G1 — Zona crítica activa (ρ ∈ [0.4, 0.8])

```
c(S) ∈ [-0.000332, +0.001310]   (80% CI)
r    ∈ [-0.074,    +0.290]
Mediana: c(S) ≈ 0,  r ≈ 0.006
```

Señal real, pequeña, oscilante alrededor de cero.
Zona donde P1–P4 se verifican. El monitor opera aquí.

### G2 — Atractor bloqueado (ρ < 0.15 o ρ > 0.85)

```
c(S) ∈ [+0.001941, +0.004519]   (80% CI)
r    ∈ [+0.430,    +1.000]
```

Sistema colapsado fuera de zona crítica.
La señal de tensión ya no es informativa.

### G3 — Degradación activa

```
c(S) < -0.000332   (r < -0.073, bajo P10 de zona crítica)
```

Campo con cohesión negativa. Δ_r o W_mixta están distorsionando
el campo más allá de la varianza normal de la zona crítica.

### Gap discriminante G1/G2

```
[+0.001310, +0.001941]
```

Separa zona crítica de atractor bloqueado. Detectable en tiempo real por r.

---

## Distribución completa de r (percentiles, zona crítica)

| Percentil | r      | c(S)       |
|-----------|--------|------------|
| P5        | -0.085 | -0.000385  |
| P10       | -0.074 | -0.000332  |
| P25       | -0.046 | -0.000208  |
| P50       |  0.006 | +0.000028  |
| P75       |  0.121 | +0.000547  |
| P90       |  0.290 | +0.001310  |
| P95       |  0.386 | +0.001745  |

---

## Propiedad del factor r

| Zona | r generaliza | Condición |
|---|---|---|
| W_base, rho extremo | Sí — estable 0.93–0.96 | Todos positivos, densidad extrema |
| W_base, zona crítica | Sí — percentiles estables | Si ρ_corr similar al corpus |
| W_mixta / Δ_r acumulado | r es **variable** | r cambia con estructura negativa |
| N diferente | Percentiles a verificar | μ_W debe medirse empíricamente |

**r no es constante a lo largo de la sesión.**
r monitoreado en tiempo real es indicador de salud estructural del campo.

---

## Declaración para COCO-thermostat

```
COCO-thermostat opera con garantía G1 cuando:

  1. N declarado con μ_W medido empíricamente para ese corpus
  2. r monitoreado en tiempo real (r = c(S) / μ_W)
  3. Sistema en zona crítica: r < 0.290  (bajo P90 G1)
  4. No degradado: r > -0.073  (sobre P10 G1)

Fuera de estas condiciones:
  r > 0.430  → G2 activa (atractor bloqueado — señal colapsada)
  r < -0.073 → G3 activa (degradación — declarar HOLDING)

Las garantías son válidas para N=32 con ρ_corr ≈ 0.527.
Generalización a N diferente requiere re-medición de μ_W.
Generalización a ρ_corr diferente requiere re-calibración de percentiles.
```

---

## HOLDINGs activos post-derivación

| HOLDING | Estado | Nota |
|---|---|---|
| H1: α_c ≈ 0.138 | Activo | No aplica a W co-ocurrencia — requiere reformulación |
| H2: dilución P4 en N=64 | Activo | Explicado: μ_W ∝ 1/N → señal se reduce a la mitad |
| H3: normalización empírica N=16 | Activo | Confirmado: μ_W varía con N — no generaliza directamente |

Los tres HOLDINGs son proyecciones de la misma función `c(S)*(N, ρ_corr)`.
Resolver H3 analíticamente (derivar μ_W desde primeros principios) arrastraría H1 y H2.

---

## Principio de generalización — operacionalizado

> El conocimiento cohesivo puede generalizarse dentro de ciertos límites
> que surgen explícitamente desde la función/proceso de generalización.
> — gadanin.delamor, Abril 2028

**Lo que generaliza:** percentiles de r (propiedad estructural del atractor).
**Lo que no generaliza:** μ_W (propiedad del corpus — debe medirse).
**La garantía:** es un intervalo [G1_low, G1_high] que declara la zona de operación.

---

## Conexión IAP / COCO-thermostat

El CorpusService compartido entre agentes (COCO-thermostat) debe:
- Medir μ_W del corpus colectivo al inicio de cada sesión
- Monitorear r en tiempo real sobre el corpus acumulado
- Declarar G1/G2/G3 como estado de operación visible para todos los agentes

La garantía no es binaria. Es un gradiente con percentiles de confianza
que emergen del proceso de generalización mismo.
