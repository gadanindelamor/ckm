# INFORME_replica_Aiyappa_fig5_v1

*4 oct 2026, Claude Opus 5.5 (Cowork), a pedido de delamor.*

**Qué se replica.** La "modularidad óptima" en contagio complejo de Aiyappa, Flammini & Ahn, *Sci. Adv.* 10(15) eadh4439 (2024), Fig. 5.

**Fuente del código.** Repo [rachithaiyappa/beliefnet](https://github.com/rachithaiyappa/beliefnet) en el commit `2289c39`, archivos `scripts/optimalmodularity.jl` y `src/beliefnet/function.jl`. Lo porté a Python + C uno a uno. No corrí su Julia.

## Veredicto

**SE SOSTIENE.** La replicación independiente reproduce el fenómeno central: en contagio complejo existe una modularidad intermedia que maximiza la adopción. En contagio simple no existe.

## Pre-registro (escrito en el driver antes de correr)

- **Parámetros del README del repo:** α = 2.0, β = 1.0, σ = 0.2; N = 100, M = 1500, T = 2·M·N.
- **Grilla:** 20 valores de μ, de 0.01 a 0.5, como en el Julia. ρ0 (fracción de semillas) ∈ {0.05, 0.10, …, 0.30}. 10 ensembles por celda. Seed 0.
- **Criterio "se sostiene" (contagio complejo):** que para al menos un ρ0 el μ óptimo sea interior y supere a los dos extremos de la grilla por más de 2 errores estándar.
- **Control (contagio simple):** sin óptimo interior.

## Resultado

**Contagio complejo** (`dual_stable`: población estable distinta de las semillas):

| ρ0 | μ óptimo | adopción en el óptimo | en μ = 0.01 | en μ = 0.5 | criterio |
|---|---:|---:|---:|---:|---|
| 0.05 | 0.01 | 0.28 | 0.28 | 0.05 | no (óptimo en el borde) |
| **0.10** | **0.14** | **1.00** | **0.50** | **0.12** | **sí** |
| 0.15–0.30 | 0.14 | 1.00 | 0.49–0.50 | 1.00 | no: la red aleatoria también llega a 1 |

Curva para ρ0 = 0.10 (μ de 0.01 a 0.5):
0.50, 0.48, 0.48, 0.45, 0.57, **1.0, 1.0, 1.0**, 0.82, 0.48, 0.20, 0.39, 0.31, 0.30, 0.12, 0.12, 0.21, 0.20, 0.12, 0.12

- **Con μ chico:** las comunidades están aisladas y la adopción queda en la comunidad de las semillas (≈ 0.5).
- **Con μ intermedio:** la adopción es total.
- **Con μ grande:** la red es aleatoria y el contagio complejo no despega.

Es el patrón que describe el paper, en una ventana de tamaños de semilla.

**Contagio simple** (`unstable`): la adopción es 1.0 en todo μ y todo ρ0. No hay óptimo interior, como esperaba el control.

## Límites

- **No es su código corriendo.** Es un port. El generador de números aleatorios es distinto, así que los números exactos no coinciden; lo que se compara es el fenómeno.
- **La ventana de ρ0 donde aparece el óptimo es angosta en esta grilla.** Con ρ0 ≥ 0.15 la red aleatoria también llega a 1. El paper muestra el plano μ–ρ0 completo, y no lo comparé celda por celda.
- **Solo la Fig. 5.** Las Fig. 2 y 4 no se replicaron.
- **Sobre el CKM:** este resultado no es evidencia ni a favor ni en contra del CKM. Es otro modelo (ver la comparación del chat: pesos que cambian contra estados que cambian, energía triádica contra energía por pares).

## Reproducir

`gcc -O2 -shared -fPIC -o libdyn.so dyn.c && python3 replica_fig5.py salida.json` (numpy). Tarda unos 35 s.
