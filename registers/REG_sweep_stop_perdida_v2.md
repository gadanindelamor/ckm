# REG_sweep_stop_perdida_v2.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Experimento: sweep D_ckm(t_stop) × alpha → Pérdida_STOP*  
*Ref: REG_stop_grados_perdida_v1.md · v27 sección 41*  
*Clase R*

---

## Configuración

```
W_ckm_corpus_v2.json  — N=32, mu_W=0.004519, 0 pares negativos (W_base)
W_mixta               — W_base + 3 pares negativos (AMP=15):
                          (13,22): cohesion_fabricada ↔ M_M
                          (15,16): atractor_espurio ↔ portero
                          (18,20): sentido_comun ↔ inconmensurabilidad
N_RUNS = 150  (atractores)
SEED   = 42
T_STOPS = [10, 20, 40, 60, 80, 100, 130, 160, 200, 250]
ALPHAS  = [0.0, 0.1, ..., 1.0]  (11 valores)
```

Operador STOP: Δ → α·Δ (α=1.0 = sin STOP; α=0.0 = reset total)

---

## Resultados — W_base

A0 = 2 (sin Δ, n_runs=150)

| t_stop | D_ckm | A_pre | alpha* | A_post_max | Pérdida_STOP |
|--------|-------|-------|--------|------------|--------------|
| 10     | −0.50 | 3     | 0.7    | 3          | 0            |
| 20     |  0.00 | 2     | 0.0    | 2          | 0            |
| 40     |  0.00 | 2     | 0.0    | 2          | 0            |
| 60     | −0.50 | 3     | 0.1    | 3          | 0            |
| 80     | −0.50 | 3     | 0.3    | 4          | −1           |
| 100    |  0.00 | 2     | 0.1    | 3          | −1           |
| 130    |  0.00 | 2     | 0.2    | 4          | −2           |
| 160    | −1.00 | 4     | 0.3    | 5          | −1           |
| 200    |  0.00 | 2     | 0.2    | 6          | −4           |
| 250    | −1.50 | 5     | 1.0    | 5          | 0            |

D_ckm < 0: 5/10 · D_ckm = 0: 5/10 · D_ckm > 0: **0/10**  
Pérdida_STOP < 0 (expansión): 5/10 · = 0 (neutro): 5/10 · > 0 (pérdida real): **0/10**

---

## Resultados — W_mixta

A0 = 5 (sin Δ, n_runs=150)

| t_stop | D_ckm | A_pre | alpha* | A_post_max | Pérdida_STOP |
|--------|-------|-------|--------|------------|--------------|
| 10     |  0.00 | 5     | 0.0    | 5          | 0            |
| 20     | −0.20 | 6     | 0.4    | 8          | −2           |
| 40     | −0.40 | 7     | 0.2    | 8          | −1           |
| 60     | −0.80 | 9     | 0.8    | 9          | 0            |
| 80     | −0.40 | 7     | 0.8    | 8          | −1           |
| 100    | −0.20 | 6     | 0.2    | 7          | −1           |
| 130    | −0.20 | 6     | 0.2    | 7          | −1           |
| 160    |  0.00 | 5     | 0.0    | 5          | 0            |
| 200    |  0.00 | 5     | 0.4    | 8          | −3           |
| 250    | +0.40 | 3     | 0.1    | 6          | −3           |

D_ckm < 0: 6/10 · D_ckm = 0: 3/10 · D_ckm > 0: **1/10** (t=250)  
Pérdida_STOP < 0 (expansión): 7/10 · = 0: 3/10 · > 0: **0/10**

Caso t=250 (único D_ckm > 0):  
`A_post_per_alpha: {0.0:5, 0.1:6, 0.2:6, 0.3:5, 0.4:5, 0.5:4, 0.6:4, 0.7:5, 0.8:5, 0.9:3, 1.0:3}`  
A_pre=3 → A_post_max=6 (α=0.1). Pérdida = −3 (expansión, no pérdida).

---

## Verificación hipótesis

**Hipótesis original:** Pérdida_STOP monótona creciente en D_ckm(t_stop).

| W | Monótona | Spearman rho |
|---|----------|--------------|
| W_base  | NO | −0.382 |
| W_mixta | NO | −0.285 |

Hipótesis **no confirmada**. Pero el resultado es structuralmente más informativo que una simple falsación.

---

## Hallazgos

**H1 — Pérdida_STOP = 0 en este régimen.**  
En ninguno de los 20 casos (10 t_stops × 2 W) hay pérdida neta de atractores tras STOP. Pérdida_STOP ≤ 0 en todos. La hipótesis de "grados de pérdida" asume pérdida; en este corpus a esta escala de tensión (AMP=15, 3 pares negativos), el STOP produce expansión o es neutro — no pérdida.

**H2 — La acumulación de Δ expande el paisaje antes de colapsarlo.**  
D_ckm negativo en 11/20 casos. Con W_base A0=2, la acumulación de Δ crea atractores nuevos regularmente (A_pre llega a 5). Con W_mixta A0=5, el patrón es menos regular pero el pico llega a A_pre=9 (t=60). El colapso real (D_ckm > 0) solo ocurre en W_mixta t=250 — y aun así STOP expande.

**H3 — STOP siempre expande o es neutro respecto a A_pre.**  
En el único caso de D_ckm > 0 (W_mixta t=250, A_pre=3 < A0=5), STOP con α=0.1 produce A_post=6 > A0. El operador restaura más que el estado inicial. Consistent con f(A_pre): A_pre < A0 → STOP expande.

**H4 — alpha* no tiene valor universal.**  
Distribución W_base: {0.0:2, 0.1:2, 0.2:2, 0.3:2, 0.7:1, 1.0:1}. Distribución W_mixta: {0.2:3, 0.0:2, 0.4:2, 0.8:2, 0.1:1}. No hay concentración robusta en α*≈0.4 del experimento previo. La forma de la curva A_post(α) varía con t_stop.

---

## Reformulación de la pregunta

La pregunta "grados de pérdida" requiere régimen donde D_ckm > 0 sostenido y Pérdida_STOP > 0.

Para observar ese régimen se necesita:
- Mayor AMP (>15) o más pares negativos que produzcan colapso más profundo
- O T_STEPS más largo con misma acumulación
- O un W diferente donde A0 sea mayor y la degradación llegue antes

El experimento de sesión "Take your time" citado en el REG original (W_mixta t=200: A_pre=13 → A(α=0)=5) usaba AMP diferente o corpus distinto. **Ese régimen no se reproduce con AMP=15 y 3 pares negativos sobre W_ckm_corpus_v2.**

---

## Observación sobre W_base y G1

Observación adicional (pre-experimento): W_ckm_corpus_v2.json tiene 0 pares negativos. Con W_pos pura, todos los estados relajados convergen al mismo atractor (A0=2, c(S)=0.004519 constante, r≈1.0 siempre). El sistema está en G2 bloqueado — G1 operacional no es accesible con esta W. Para operar el monitor en G1 se requiere W_mixta o corpus con tensión real.

---

## Preguntas abiertas que genera este experimento

1. ¿A qué AMP/n_pares_negativos aparece Pérdida_STOP > 0 de forma consistente?  
2. ¿La expansión de A tras STOP (Pérdida < 0) es un invariante de baja tensión o un artefacto del régimen AMP=15?  
3. ¿El exp "Take your time" (A_pre=13) usaba AMP diferente? Revisar parámetros exactos de ese experimento.  
4. La no-monotonía de alpha* entre t_stops — ¿es propiedad del corpus o del mecanismo de acumulación?

---

## Estado

- Hipótesis de monotonía Pérdida_STOP ~ D_ckm: **no confirmada** (tampoco falsada en sentido fuerte — el régimen de pérdida no se alcanzó)  
- Hipótesis f(A_pre): **consistente** con H3 — el único caso D_ckm > 0 produce expansión como predice  
- Régimen de pérdida real: **requiere parámetros distintos** (AMP mayor o más pares negativos)  
- Próximo paso: identificar parámetros del exp "Take your time" (A_pre=13) y reproducir ese régimen

---

*sweep_stop_perdida.py · N_RUNS=150 · SEED=42 · T_STOPS=[10,20,40,60,80,100,130,160,200,250]*
