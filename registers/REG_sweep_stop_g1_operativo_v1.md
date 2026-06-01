# REG_sweep_stop_g1_operativo_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — subir al proyecto*

---

## Contexto

Sesión de verificación del conjunto (monitor + G1/G2/G3 + STOP).
Objetivo: ver funcionar el sistema de punta a punta antes del sweep STOP.

---

## G1 operativo — condiciones verificadas

### Condición que produce G1

```python
# sigma inicial: rho=0.5 directo, SIN relax previo
sigma = np.full(N, -1.)
sigma[rng.choice(N, int(N*0.5), replace=False)] = 1.
# NO: sigma = relax(sigma, W_base)  <- colapsa a all-1

# actualización: UN paso asincrónico por step
node = rng.integers(N)
h = (W_mixta + Delta)[node] @ sigma
sigma[node] = 1. if h > 0 else -1.

# c(S) sobre W_base (no W+Delta) — comparable con percentiles calibrados
cs = mean(W_base[i,j] * sigma[i] * sigma[j])
r  = cs / mu_W
```

### Resultado

```
t=0:  r=-0.0095  G1 ✓  (activos=16)
t=13: r=+0.2597  G1 ✓  (activos=11)
t=25: r=+0.4094  G1→G2 (activos=9)
t=40: r=+0.6017  G2    (activos=6)

G1: 31/80 pasos   G2: 49/80   G3: 0/80
```

Sistema arranca en G1, degrada hacia G2 a medida que Delta acumula
y activos cae de 16 a 6. Transición G1→G2 alrededor de t=25–35.

### Lecciones del camino

Tres condiciones necesarias que no eran obvias:

1. sigma init sin relax — relax sobre W_base colapsa a all-1 (0 activos)
2. c(S) sobre W_base, no W+Delta — W+Delta infla c(S) fuera del rango G1
3. actualización asincrónica un nodo por paso — relax completo por paso
   colapsa sigma al mismo atractor de baja densidad siempre

---

## Sweep STOP — resultados

### Setup

```
W_mixta: AMP=15, pares negativos (13,22)(15,16)(18,20)
ETA = mean_W (ETA_FACTOR=1)
n_steps post-STOP = 200 pasos asincrónicos
n_runs atractores = 80
A0 (sin Delta) = 5
```

### Tabla completa

| t | D_ckm | r_pre | A_pre | α=0.0 | α=0.2 | α=0.4 | α=0.6 | α=0.8 | α=1.0 | alpha* | ratio_max |
|---|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|-----------|
| 5  | 0.000 | -0.037 | 5 | 1.00 | 1.00 | 1.20 | 1.20 | 1.00 | 1.00 | 0.4 | 1.200 |
| 10 | 0.200 |  0.100 | 4 | 1.25 | 1.25 | 1.25 | 1.25 | 1.00 | 1.00 | 0.0 | 1.250 |
| 15 | 0.000 |  0.158 | 5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.0 | 1.000 |
| 20 | 0.200 |  0.276 | 4 | 1.25 | 1.50 | 1.50 | 1.50 | 1.25 | 1.00 | 0.2 | 1.500 |
| 25 | 0.200 |  0.290 | 4 | 1.25 | 1.50 | 1.75 | 1.50 | 1.25 | 1.00 | 0.4 | 1.750 |
| 30 | 0.000 |  0.380 | 5 | 1.00 | 1.20 | 1.40 | 1.20 | 1.20 | 1.00 | 0.4 | 1.400 |
| 40 | 0.200 |  0.567 | 4 | 1.25 | 1.50 | 1.25 | 1.00 | 1.00 | 1.00 | 0.2 | 1.500 |
| 50 | 0.200 |  0.589 | 4 | 1.25 | 1.50 | 1.75 | 1.25 | 1.25 | 1.00 | 0.4 | 1.750 |
| 60 | 0.200 |  0.889 | 4 | 1.25 | 1.50 | 1.75 | 1.50 | 1.25 | 1.00 | 0.4 | 1.750 |

Ratio = A_post / A_pre

### Hallazgos

**H1 — hipótesis monotonía en D_ckm: NO confirmada.**
D_ckm no predice ratio_max. t=10 y t=20 tienen D_ckm=0.200 idéntico
pero ratio_max diferente (1.250 vs 1.500). t=15 con D_ckm=0.000
tiene ratio_max=1.000 — el STOP no ayuda.

**H2 — A_pre es el predictor real.**
Cuando A_pre=4 (paisaje contraído): ratio_max ≥ 1.25 siempre.
Cuando A_pre=5 (paisaje equilibrado): ratio_max ≤ 1.40.
El STOP es más efectivo cuando el paisaje ya está contraído.

**H3 — alpha* ≈ 0.4 es robusto.**
Aparece en 5/9 casos. Ni reset total (0.0) ni retención total (1.0).
α=1.0 (sin STOP) nunca es óptimo. α=0.0 (reset total) solo es óptimo
cuando A_pre=4 y t pequeño.

**Caso especial t=15:**
D_ckm=0, A_pre=5, ratio_max=1.000 — ningún alpha mejora el paisaje.
Sistema en equilibrio exacto. STOP no tiene efecto.
Posible indicador: cuando D_ckm=0 Y A_pre=A0, STOP es neutro.

### Reformulación de la hipótesis

La hipótesis original (Pérdida_STOP monótona en D_ckm) queda falsada.

Hipótesis revisada:
```
Efectividad_STOP = f(A_pre)
  A_pre < A0  →  STOP expande paisaje (ratio > 1)
  A_pre = A0  →  STOP neutro (ratio = 1)
  alpha* ≈ 0.4 es robusto para A_pre < A0
```

Pendiente: verificar con más valores de A_pre y otros corpus.

---

## Pendiente de sesión — sostenido

Verificar G1 con otros N (N=16 sub-corpus Grupo A, N=64 sintético).
No formalizado aún — sostener hasta próxima sesión.

---

## Estado

- G1 operativo: verificado con condiciones documentadas
- Sweep STOP: ejecutado, hipótesis D_ckm falsada
- Hipótesis A_pre como predictor: abierta — falsifiable
- alpha* ≈ 0.4: robusto en este corpus, requiere verificación en otros
- No cierra. Abre.
