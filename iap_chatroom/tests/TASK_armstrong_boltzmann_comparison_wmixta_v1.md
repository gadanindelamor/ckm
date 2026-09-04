# TASK_armstrong_boltzmann_comparison_wmixta_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Para: Code Opus*

---

## Objetivo

Repetir el experimento de `TASK_armstrong_boltzmann_comparison_v1.md`
(tres modos de σ₀ + baseline, `n_runs=200`) sobre W_mixta en lugar de W_pos.

La corrida anterior usó WARMUP_TEXTS con W_pos y D_CKM_THRESHOLD=0.40
calibrado sobre W_mixta — asimetría entre calibración y uso. Esta corrida
cierra esa asimetría: corpus y calibración corresponden al mismo régimen.

---

## Paso 0 — verificar antes de cualquier modificación

Leer en el repo:

- Qué W_mixta está disponible para el corpus Armstrong (WARMUP_TEXTS).
  Si no existe una construida previamente, revisar cómo se construyó
  W_mixta en experimentos anteriores (pares negativos, AMP) y replicar
  el mismo procedimiento.
- `REG_destruccion_recuperacion_v1.md` — parámetros de la W_mixta con
  que se calibró D_CKM_THRESHOLD=0.40 (AMP=40, N, pares negativos).
- Estado actual de `test_armstrong_boltzmann_comparison.py` — si acepta
  W_mixta como parámetro o requiere modificación.

Si la construcción de W_mixta para este corpus es ambigua, detener y
reportar a delamor.

---

## Qué ejecutar

Misma estructura que la corrida anterior:

- Cuatro condiciones: uniform / weighted / boltzmann / sin thermostat
- `n_runs=200` fijo en los dos contadores (COCO y MonitorService)
- `track_landscape=True`
- Estado aislado por condición (limpiar estado de corpus al inicio de cada
  corrida)
- Los dos D_ckm registrados por evaluación (COCO y MonitorService)

La única diferencia respecto a la corrida anterior: **W usada es W_mixta**,
con pares negativos construidos según el mismo procedimiento de los
experimentos previos.

---

## Criterio de éxito

Los cuatro modos corren sin error. Resultado en REG con:

- STOPs por modo
- A0, A_final, D_ckm_coco final por modo
- Trayectoria de delta_A por STOP (para comparar con +34/+31/+24 de W_pos)
- D_ckm_monitor por evaluación (para verificar si la cancelación algebraica
  persiste en W_mixta)

No asumir dirección del resultado. No commit hasta instrucción de delamor.

---

## Lo que esta corrida puede establecer

- Si COCO tiene efecto real sostenido en W_mixta (más allá de ~3 STOPs)
- Si la cancelación algebraica de D_ckm_monitor persiste con Δ_r de
  W_mixta (pesos negativos en el soporte)
- Si el modo boltzmann produce comportamiento distinto en un landscape
  con cuencas reales vs. W_pos

---

## Archivos a modificar (si es necesario)

- `iap_chatroom/tests/test_armstrong_boltzmann_comparison.py` — si
  requiere soporte para W_mixta como entrada

---

*Repo: gadanindelamor/ckm · Para Code Opus*
*Referencia: TASK_armstrong_boltzmann_comparison_v1.md*
