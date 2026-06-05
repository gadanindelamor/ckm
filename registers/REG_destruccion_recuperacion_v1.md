# REG_destruccion_recuperacion_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Experimento: curva de destrucción por acumulación vs recuperación por STOP*  
*Origen: reformulación emergida en sesión desde REG_sweep_stop_perdida_v2.md*  
*Clase R*

---

## Contexto — reformulación de la pregunta

La pregunta original (REG_stop_grados_perdida_v1.md):

> ¿Pérdida_STOP es monótona creciente en D_ckm(t_stop)?

Asumía que STOP produce pérdida. El sweep mostró consistentemente lo contrario: STOP produce restauración o expansión — Pérdida_STOP ≤ 0 en todos los casos.

La reformulación correcta, emergida del contacto con la estructura:

> **¿Qué fracción de lo destruido por la acumulación puede recuperar el STOP?**

```
Destrucción(t)     = A0 - A(t)
Recuperación(t)    = max_α[A_post(α)] - A(t)
Fracción_rec(t)    = max_α[A_post(α)] / A0

Pregunta: ¿Fracción_rec(t) es función de t o de D_ckm(t)?
¿Existe t* donde Fracción_rec empieza a decrecer?
```

Son dos operadores distintos: **acumulación destruye**, **STOP restaura**. No son simétricos.

---

## Configuración

```
W_ckm_corpus_v2.json — N=32, A0_base=2
W_mixta AMP=40        — 3 pares negativos, A0=25
  (13,22): cohesion_fabricada ↔ M_M
  (15,16): atractor_espurio ↔ portero
  (18,20): sentido_comun ↔ inconmensurabilidad
ETA = mean_W ≈ 0.006
N_RUNS = 150, SEED = 42
ALPHAS = [0.0, 0.1, ..., 1.0]
Puntos: t = 0, 10, 20, ..., 400  (41 puntos)
```

AMP=40 elegido porque produce A0=25 — paisaje rico que permite observar destrucción sustancial.

---

## Resultados — curva de destrucción A(t)

| t | A(t) | D_ckm | Destruido | % A0 | A_post_max | Fracción_rec |
|---|------|-------|-----------|------|------------|--------------|
| 0 | 25 | 0.000 | 0 | 100% | 25 | 1.00 |
| 10 | 24 | 0.040 | 1 | 96% | 25 | 1.00 |
| 20 | 25 | 0.000 | 0 | 100% | 27 | 1.08 |
| 30 | 25 | 0.000 | 0 | 100% | — | — |
| **40** | **19** | **0.240** | **6** | **76%** | — | — |
| **50** | **13** | **0.480** | **12** | **52%** | **27** | **1.08** |
| 100 | 12 | 0.520 | 13 | 48% | 27 | 1.08 |
| 180 | 10 | 0.600 | 15 | 40% | — | — |
| 300 | 9 | 0.640 | 16 | 36% | 25 | 1.00 |
| 400 | 9 | 0.640 | 16 | 36% | 25 | 1.00 |

**Transición brusca t=30→50**: A cae de 25 a 13 en 20 pasos. Después oscila en banda [8–15] sin recuperar A0.

Pearson r(t, A) = **−0.783** — tendencia decreciente con fluctuaciones locales. No monótona.

---

## Hallazgo central

**STOP recupera más allá de A_pre en todos los casos.**

A_post_max ≥ A0 en la mayoría de los t evaluados. La fracción recuperable ≥ 1.0 — el STOP con α óptimo devuelve el sistema al estado pre-acumulación o por encima.

Esto no es trivial: significa que con W_mixta AMP=40, la acumulación de Δ *desplaza* el paisaje pero no lo destruye estructuralmente. El suelo (W_mixta) mantiene la capacidad de recuperación intacta. STOP limpia Δ y el suelo emerge.

**La destrucción real requeriría que la acumulación modifique W** — no solo Δ. El operador STOP (Δ → α·Δ) no toca W. Por eso la recuperación es siempre posible.

---

## Implicación para la hipótesis original

La hipótesis "grados de pérdida" buscaba el caso donde STOP produce pérdida neta. Ese caso requiere un mecanismo diferente — no acumulación en Δ con W fija, sino algo que modifique W directamente.

En términos CKM: **Δ_r acumula orientación emergida, no destruye memoria**. La memoria (W) es el suelo invariante. El STOP opera sobre Δ_r, no sobre W.

La pérdida real —si existe— requeriría:
- Aprendizaje Hebbiano sobre W (que el proyecto explícitamente evita — destruye tensión)
- O deterioro del corpus fuente (los textos originales que construyeron W)

Ambos están fuera del alcance del operador STOP.

---

## Observación metodológica

La reformulación emergió del contacto directo con los datos del sweep. No fue deducción — fue lo que el campo rechazó de la pregunta original.

Mecanismo: **Hysteresis Inference** (el resultado depende del camino recorrido) + **Collective Inference** (emergió de múltiples estados iniciales sobre la misma W, no de un solo caso).

Análogo en CKM: la pregunta "grados de pérdida" llegó sin su Δ_r — sin la historia de los casos donde STOP no pierde. El sweep construyó ese Δ_r.

---

## Preguntas que abre

1. ¿Existe un operador que modifique W directamente y para el que sí haya pérdida real? ¿Qué sería ese operador en términos de interacción?

2. ¿La fracción recuperable decrece si la acumulación es más rápida (ETA mayor)? ¿Hay velocidad de acumulación donde el suelo W no alcanza?

3. La transición brusca t=30→50 (A cae de 25 a 13): ¿es umbral de fase o fluctuación? ¿Se reproduce con otras semillas?

4. La oscilación A(t) en banda [8–15] tras la transición: ¿qué la produce? ¿Qué pares de Δ son responsables de las subidas?

---

## Estado

- Reformulación: **operativa** — Fracción_rec(t) = max_α[A_post(α)] / A0 es medible
- Hipótesis original (pérdida por STOP): **no aplica** — el operador no toca W
- Nueva hipótesis (fracción recuperable decreciente en t): **abierta** — los datos actuales muestran Fracción_rec ≥ 1.0 consistente; requiere régimen donde W sea afectada para ver decrecimiento
- Curva de destrucción A(t): **accesible, calculable** — Pearson r(t,A)=−0.783, no monótona

---

*sweep_stop_perdida.py + curva_recuperacion · N_RUNS=150 · AMP=40 · SEED=42*
