# TASK_boltzmann_sampling_count_attractors_v3.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Para: Code Opus*

---

## Objetivo

Agregar un tercer modo de muestreo de σ₀ en `_count_attractors()` de `coco.py`: muestreo termodinámicamente fundamentado desde la distribución de Boltzmann del landscape.

Los modos uniforme y ponderado tienen sesgos documentados (REG_situacion_medicion_ago2026_v1, REG_stochastic_eval_v2).

---

## Paso 0 — leer antes de cualquier modificación

Leer en el repo:
- `hopfield.py` — lógica de relajación estocástica disponible
- `coco.py` — `_count_attractors`, `_sample_s0`, `_relax` actuales
- `kcore.py` — para no interferir

---

## Qué implementar

### Concepto

Antes del relax determinístico habitual, correr un calentamiento estocástico desde σ₀ aleatorio. El calentamiento usa temperatura β_c, llevando el estado hacia la distribución de Boltzmann del landscape. El estado resultante es el σ₀ para el relax determinístico.

`hopfield.py` ya tiene relajación estocástica. Code lee esa implementación y la integra en `coco.py` según el estado del repo.

### β_c

```
β_c = 1 / (ρ* · N · μ_W)

  ρ*  = 0.5  — identidad algebraica: relax(-σ) = -relax(σ)
  N   = número de nodos
  μ_W = media de W sobre pesos no-nulos
```

β_c se computa una vez por llamada, no por run.

### n_warmup

Parámetro configurable. Valor inicial: N. Óptimo: abierto.

---

## Criterio de éxito

Tests existentes de `test_coco.py` pasan sin cambio.

Modo boltzmann corre sin error con `W_ckm_corpus_v2.json` y produce conteo de estados terminales. No asumir dirección — registrar y documentar en REG.

Panel de thermostat registra modo activo (`sampling_mode`) para trazabilidad de cada decisión de STOP.

---

## NO modificar

- Comportamiento actual de modos uniforme y ponderado — sin regresión
- `test_coco.py`, `test_monitor_services.py` — sin cambio
- REGs históricos
- ALPHA_MIN, ALPHA_MAX, D_CKM_THRESHOLD
- Lógica de OPERADOR_STOP_COCO

---

## Archivos a modificar

- `coco.py`
- `monitor_service.py` (si corresponde)

---

## Lo que este TASK no cierra

- n_warmup óptimo: abierto
- Si boltzmann da mejor cobertura de cuencas: empírico, requiere REG posterior

---

*Repo: gadanindelamor/ckm · Para Code Opus*
