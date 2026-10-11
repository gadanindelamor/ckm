# NOTAS_proxima_sesion_paper_v11.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Para la próxima sesión de trabajo sobre PAPER v11*

---

## Header del paper

```
CKM PAPER DRAFT v11 — Ago 2026
```

---

## Tema 1 — Distribución / sesgo estructural de W en sweeps count_attractors · P1–P7

**Qué hay que trabajar en el paper:**
El conteo de atractores usado para verificar P1–P7 fue producido con muestreo uniforme de σ₀. Ese modo puede medir velocidad de expulsión desde estados iniciales improbables, no diversidad estructural del landscape. Esto afecta la base empírica de P1–P7.

**Posición actual del paper (v11):** P1–P7 se reportan como verificadas sin caveats sobre el modo de muestreo. Hay que decidir cómo presentar esto — ¿como condición del instrumento, como limitación, como open question?

**Referencias:**
- `REG_situacion_medicion_ago2026_v1.md` — registro central de la situación. Lista REGs afectados.
- `REG_stochastic_eval_v1.md` — sweep uniforme seeds 0–9, n_runs 10–150
- `REG_stochastic_eval_v2.md` — sweep ponderado. Tabla comparativa uniform/weighted. Dos ejes de sensibilidad documentados.
- `REG_count_attractors_bias_v1.md` — documentación del sesgo de uniformidad y modo weighted
- `DEFS_CKM_estado_actual_v3.md §6` — estado incierto del conteo

**Riesgo de confusión:** No confundir "sesgo de uniformidad en σ₀" con "sesgo de n_runs (coupon-collector)". Son dos sesgos independientes documentados en REG_count_attractors_bias_v1.

---

## Tema 2 — CKM no compite con KR — estudia dinámicas de conocimiento (no estática) · P1–P7

**Qué hay que trabajar en el paper:**
§2.3 (Graph-Based Knowledge Representation) y §8 (Discussion) necesitan ser más explícitos: CKM no es un sistema de representación del conocimiento. Es un instrumento que estudia la geometría del campo bajo perturbación — dinámicas, no estados.

**Posición actual del paper (v11):** §8.6 dice "CKM inhabits and structures" el espacio que KR dejó abierto. No compite — ocupa. Pero el §2.3 puede leerse como si CKM fuera una alternativa a KR.

**Argumento central:**
KR pregunta: "¿cómo representar lo que se sabe?" (estático, propositivo)
CKM pregunta: "¿cómo cambia la geometría del campo cuando se incorpora o rechaza conocimiento?" (dinámico, estructural)
Las 7 predicciones P1–P7 son todas sobre dinámicas: histeresis, cascadas, asimetría temporal, densidad óptima, colapso, flujo direccional, rol estructural. Ninguna es sobre representación de contenido.

**Referencias:**
- `PAPER v11 §2.3` — Graph-Based KR, relación con Aiyappa et al. 2024
- `PAPER v11 §8.6` — "inhabits and structures"
- `CKM_Modelo_Hibrido.md` — análisis original de 14 familias de modelos. La distinción estático/dinámico está ahí.
- `DEFS_CKM_estado_actual_v3.md §2` — "W como suelo supuesto" — CKM no modela lo que el campo dice sino cómo cambia lo que da por sentado

**Riesgo de confusión:** No equiparar "CKM no compite con KR" con "CKM no es relevante para aplicaciones de KR". La relevancia es posible por complementariedad, no por sustitución.

---

## Tema 3 — Criterios de diversidad: conteo de atractores, coercividad, cuencas (abierto)

**Qué hay que trabajar en el paper:**
El paper usa "attractor diversity" como concepto pero no lo define formalmente. ¿Qué es diversidad en CKM? ¿Conteo de atractores únicos? ¿Tamaño de cuencas? ¿Coercividad? ¿Los tres son complementarios o redundantes?

**Estado actual:**
- Conteo de atractores (A): implementado, metodología en revisión (ver Tema 1)
- Coercividad: verificada geométricamente en lazo P1. Definición operativa: valor de ρ donde c(S) cruza cero en rama UP. Es un intervalo frustrado [0.406, 0.586], no un punto.
- Cuencas: propuesto que son pequeñas y profundas en sistema frustrado. No verificado directamente.

**La pregunta abierta:**
¿Son A (conteo), coercividad, y tamaño de cuencas tres medidas del mismo fenómeno o tres dimensiones independientes de "diversidad"? ¿Puede el paper proponer un criterio unificado?

**Referencias:**
- `REG_mapeo_magnetico_ckm_v1.md §1.7` — coercividad CKM, lazo P1, datos disponibles en hopfield.py
- `DEFS_CKM_estado_actual_v3.md §3` — coercividad como intervalo
- `PAPER v11 §5.3` — P4 / W_mixta coercividad
- `REG_stochastic_eval_v2.md` — A_observed bajo dos modos, ninguno validado
- `Thermodynae_Link.pdf` — Husain (2026) Eur. Phys. J. B: transición de fase continua en red Hopfield memristiva. Atención: aplica a Hopfield asociativo estándar, no directamente a CKM. El paper de Husain muestra ausencia de histeresis → transición continua. CKM muestra histeresis (P1) → régimen distinto.

**Riesgo de confusión:**
- No equiparar "atractor único" con "cuenca grande". En sistemas frustrados las cuencas más profundas pueden ser las más pequeñas en extensión.
- No usar Husain (2026) para argumentar sobre N mínimo de CKM — ver DEFS v3 §14.

---

## Tema 4 — Néel (≈ Nielsen ≈ TEER) · selección dinámica de pares negativos

**Qué es:**
Temperatura de Néel efectiva como criterio de elicitación de pares negativos sin sesgo externo. Louis Néel, físico. El nombre fue aproximado en sesión como "Nielsen" y "TEER" — la unión de los dos términos delimita el concepto exacto.

**El criterio** (propuesto, no verificado — DEFS_CKM_estado_actual_v3.md §12):
1. Construir W_pos sin declarar pares negativos.
2. Barrer β de alto a bajo.
3. Medir separabilidad T0 vs T1 en cada β: c(S) interno vs cruzado.
4. β_Néel = β donde la separabilidad colapsa.
5. Los pares (i,j) en clusters opuestos antes del colapso → candidatos a pares negativos.

Criterio estructural, no editorial. Los pares emergen del barrido.

**Referencias:**
- `DEFS_CKM_estado_actual_v3.md §12`
- `REG_mapeo_magnetico_ckm_v1.md §3.3`
- `PAPER v11 §2.3`

---

## Archivos de la sesión actual que entran al proyecto

- `DEFS_CKM_estado_actual_v3.md` — referencia actual de definiciones
- `PAPER_Landscape_Driven_Device_v11.md` — paper con 5 cambios quirúrgicos

---

*gadanindelamor/ckm — Agosto 2026*
