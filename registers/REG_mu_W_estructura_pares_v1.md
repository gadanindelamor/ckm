# REG_mu_W_estructura_pares_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — subir al proyecto*

---

## Origen

Derivación analítica de μ_W como prerequisito para resolver H1/H2/H3.
Pregunta: ¿es posible derivar μ_W desde primeros principios?

---

## Hallazgo — estructura de pares

Distribución de frecuencias marginales (suma de fila W) para N=32:

```
CV = 0.944  —  alta heterogeneidad
Razón max/min = 102x
Skewness = +0.524  (cola derecha)
Mediana = 0.064  —  punto de corte natural
```

**Bimodalidad implícita:**
```
Grupo A (16 nodos, f >= 0.064):  nodos centrales del corpus
Grupo B (16 nodos, f <  0.064):  nodos tardíos / baja densidad
```

---

## Comparación μ_W observado vs mean(fi·fj)

| Grupo | Pares | μ_W obs | mean(fi·fj) | ratio | δ |
|-------|-------|---------|-------------|-------|---|
| AA    | 120   | 0.016122 | 0.065599   | 0.246 | −0.049 |
| AB    | 256   | 0.000952 | 0.005933   | 0.160 | −0.005 |
| BB    | 120   | 0.000523 | 0.000510   | 1.025 | +0.000013 |
| **Global** | **496** | **0.004519** | **0.019057** | **0.237** | — |

---

## Resultado central

**μ_BB ≈ mean(fi·fj)** — derivable analíticamente. Ratio 1.025 ≈ 1.

Para nodos de baja frecuencia (Grupo B), la co-ocurrencia observada
es igual a la predicha por independencia estadística.
No hay señal estructural — solo ruido de frecuencia.

**μ_AA y μ_AB no son derivables desde fi·fj.**
El modelo de independencia sobreestima 4x–6x.
Causa: los nodos centrales co-ocurren tanto entre sí que sus frecuencias
marginales están infladas mutuamente. No son independientes — son el núcleo.

---

## Cierre de HOLDINGs H1/H2/H3

### H3 — normalización empírica N=16

**Cerrado.**

μ_W no generaliza entre N porque al cambiar N cambia la proporción
de nodos A vs B, y μ_AA domina el global (ratio 0.246 vs 1.025).
Medir μ_W empíricamente al inicio de cada sesión no es workaround —
es el procedimiento correcto. μ_AA no tiene forma cerrada sin conocer
la estructura del núcleo correlacionado.

### H2 — dilución P4 en N=64

**Cerrado por arrastre.**

Si N crece agregando nodos tipo B: μ_W cae hacia régimen BB (μ_W → 0).
Si N crece agregando nodos tipo A: μ_W permanece alto.
N no determina μ_W — la composición del corpus lo determina.
La dilución observada en N=64 es consecuencia de agregar nodos periféricos.

### H1 — α_c asume no-correlación

**Cerrado por arrastre.**

α_c = 0.138 fue derivado asumiendo patrones no correlacionados (Hopfield clásico).
La estructura real tiene núcleo correlacionado (Grupo A) que modifica la capacidad.
α_c efectivo depende de la composición A/B del corpus — no es constante universal.

---

## Lo que generaliza / lo que no generaliza

| | Generaliza | Condición |
|---|---|---|
| μ_BB | Sí | Solo para corpus con nodos de baja densidad |
| Estructura A/B | Sí (forma) | Siempre hay núcleo + periferia en corpus real |
| μ_W global | No | Depende de proporción A/B — propiedad del corpus |
| α_c | No | Depende de composición del núcleo |
| Percentiles de r | Sí | Propiedad estructural del atractor |

**Lo que generaliza es la estructura** (BB se comporta como independencia,
AA requiere medición). No el valor de μ_W.

---

## Frontera — conocer la estructura del núcleo

La derivación analítica de μ_AA requiere modelar el núcleo correlacionado:
cómo se organizan los 16 nodos centrales, cuál es su estructura de co-ocurrencia,
si hay sub-núcleos.

Esto es un proyecto separado. No es necesario para operar COCO-thermostat.
La medición empírica de μ_W es suficiente y correcta.

---

## Estado

- H1, H2, H3: **cerrados**
- μ_BB derivable analíticamente: **verificado** (ratio 1.025)
- μ_AA estructura interna: **abierto — proyecto separado**
- Procedimiento operativo: medir μ_W al inicio de sesión, monitorear r en tiempo real
- No cierra la estructura del núcleo. Eso abre.
