# TASK_n_runs_panel_saturacion_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: TASK_neff_y_frontera_logica_v1; D_masa_cuencas log (`80c9c50`); condicion_W (`69a7c58`).*

---

## Medido (W corregida, extracción en una rama)

| corpus | k | N_eff con n_runs 50 → 200 → 500 → 1000 → 2000 → 5000 |
|---|---:|---|
| caso09 | 12 | 3.16 → 3.60 → 3.47 → 3.89 → 4.02 → 4.01 |
| caso09 | 21 | 1.92 → 1.97 → 2.02 → 2.02 → 2.03 → 2.02 |
| caso13 | 13 | 3.44 → 3.56 → 3.62 → 3.69 → 3.72 → 3.69 |
| caso13 | 24 | 4.50 → 4.65 → 4.76 → 4.85 → 4.78 → 4.79 |
| WARMUP_TEXTS | 20 | 50 → 177 → 396 → 655 → 978 → 1326 — **no converge** |

- Casos IAP: N_eff converge ~1000 runs (±2% del valor a 5000). Con 50, 5–20% bajo.
- WARMUP_TEXTS: N_eff ≈ n_runs — cada muestra cae en una órbita nueva. No mide el paisaje: mide el muestreo. Mismo corpus sin fin de warm-up en la selección de nodos.
- Costo: ~60 ms por cálculo con 1000 runs.

## Qué hacer (delamor: sí)

1. **n_runs = 1000** por defecto en MonitorService (`n_runs_attractors`). Declarado en `condicion_W`. Afecta también el conteo de A (D_ckm), que no satura con ningún n_runs.
2. **Señal de saturación** en el panel, junto a N_eff:
   - `N_eff_sobre_n_runs` — cerca de 1 → N_eff es del muestreo, no del paisaje.
   - `orbitas_unicas_frac` — fracción de órbitas vistas una sola vez.
   Continuas; no se declara "saturado/no saturado" en el panel.

## Verificación

- Panel lleva la señal; WARMUP da valores cerca de 1, caso09 lejos.
- **Completitud:** qué tests deberían moverse con el cambio de default — y si ninguno, declararlo.

## Qué no hace

No cambia n_runs de COCO (`n_runs=80`). No define un umbral de saturación.
