# TASK_armstrong_boltzmann_comparison_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Para: Code Opus*

---

## Objetivo

Correr el experimento Armstrong con los tres modos de muestreo de σ₀
disponibles en COCO, aislando n_runs=200 como variable controlada.

Propósito: observar comportamiento de D_ckm, A, y STOPs bajo cada modo
sobre corpus real con acumulación de Δ_r. No comparar cuál es mejor —
registrar qué produce cada uno.

---

## Paso 0 — verificar antes de cualquier modificación

Leer en el repo:
- Estado actual de `_count_attractors` en `coco.py` — modos disponibles
- Cómo se instancia COCO en el script Armstrong existente
- Si MonitorService en el Armstrong actual usa COCO o corre solo

Si el script Armstrong existente no acepta configuración de modo de
muestreo sin modificación, detener y reportar a delamor.

---

## Qué ejecutar

### Condición controlada

`n_runs = 200` fijo en todas las corridas. Eliminar n_runs como variable
de confusión.

### Tres corridas secuenciales sobre el mismo corpus

1. **Uniforme** — modo default, comportamiento histórico
2. **Ponderado** — weighted=True
3. **Boltzmann** — boltzmann=True, n_warmup=N

Cada corrida: misma secuencia de prompts Armstrong, mismo corpus inicial,
mismo seed. Lo que varía: solo el modo de σ₀.

### MonitorService sin COCO

Si el script Armstrong tiene una variante donde MonitorService corre sin
thermostat, correrla también con n_runs=200 para referencia. MonitorService
solo tiene modo uniforme — es el baseline.

---

## Corrección previa — REG_boltzmann_sampling_v1

Antes de ejecutar, corregir en `REG_boltzmann_sampling_v1.md` los dos
párrafos invertidos documentados en la sesión Ago 2026:

1. "β_c depende de la escala numérica" → el producto β_c·h es invariante
   de escala. El párrafo dice lo contrario.
2. W_hub: el calentamiento era casi **determinista** (β_c·|h| ≈ 10),
   no casi aleatorio. Corpus real: casi **aleatorio** (β_c·|h| ≈ 0.065).
   Estaba invertido.

---

## Criterio de éxito

Tres REGs o un REG con tres secciones, cada una documentando:
- n_STOPs ocurridos
- D_ckm trayectoria
- A_actual por evaluación
- sampling_mode registrado en panel

No asumir dirección — registrar. No commit hasta instrucción de delamor.

---

## NO modificar

- Comportamiento default de COCO (sampling_mode="uniform") — sin regresión
- Tests existentes
- REGs históricos (solo corregir el párrafo invertido en boltzmann_v1)

---

*Repo: gadanindelamor/ckm · Para Code Opus*
