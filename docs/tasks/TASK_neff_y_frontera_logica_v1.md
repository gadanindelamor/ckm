# TASK_neff_y_frontera_logica_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v5.md — "Función canónica" (N_eff) y criterios de diversidad nivel C. Condición empírica: caso09_run2, bootstrap = 12, W congelada (`c32d22a`). Rebuilds fuera por ahora.*

---

## Qué hacer

La lógica antes que los datos. Dos piezas que no dependen de cómo se reduce una órbita a nodos activos:

1. **N_eff** a `services/landscape_engine.py`, y al panel de Monitor.
2. **Lógica de `cluster_frontier_density`** verificada sola, con particiones armadas a mano.

## 1. N_eff

- `basin_masses(W_eff, n_runs, seed, …)`: fracción de las n_runs muestras de σ₀ que cae en cada **órbita** (`relax_orbit`), mismo muestreo que `count_attractors`. Ordenadas de mayor a menor.
- `n_eff(masas) = 1 / Σ m²` — inverso de Simpson. Hoy sólo existe en `experiments/orbit_analytics.py:187`.
- Panel de Monitor: `N_eff` (sobre W_eff de esta evaluación) y `N_eff0` (baseline, se fija como A0 y se resetea con él en cualquier cambio de W — D2).
- **D_masa_cuencas no se calcula**: la escala (lineal o log) sigue abierta. El panel porta los dos N_eff; la fórmula se aplica cuando se decida.

Nota: `count_attractors` cuenta **estados terminales** (`relax`), `basin_masses` cuenta **órbitas**. Son objetos distintos, sobre las mismas muestras.

## 2. cluster_frontier_density — lógica

Se queda en `services/cluster_frontier_density.py`. Acuerdos (delamor):

- **inter < 0 → `"oposicion"`.** Oposición estructural activa entre clusters; la fórmula `min(intra)/inter` no aplica. Distinto de `inf`.
- **inter = 0 → `inf`.** Sin aristas entre clusters.
- **inter > 0 → `min(intra_a, intra_b) / inter`.**
- Cluster de 1 nodo: intra = 0 → coercividad 0 (se lee como porosa — anotado, no se cambia).
- Salida serializable a JSON: claves `"Ca|Cb"`.

Verificación con particiones y W sintéticas, casos: frontera positiva, frontera nula, frontera negativa, cluster de un nodo, intra negativo.

## Verificación

- `n_eff`: masas uniformes de k órbitas → k; una sola órbita → 1.
- `basin_masses` suma 1 y su número de órbitas ≤ n_runs; con la misma seed, mismo resultado.
- Monitor: `N_eff` y `N_eff0` en el panel; `N_eff0` se resetea con A0.
- caso09, bootstrap 12, W congelada: N_eff por mensaje volcado al JSONL, **revisado antes de mostrarlo en ninguna UI**.
- Tests existentes sin regresión.

## Condición de esta etapa (delamor)

Sin rebuild, todo se evalúa contra la W, el A0 y el N_eff0 del bootstrap. Lo que sale verifica **lógica**, no mide el campo: hasta que el rebuild se habilite, los valores no son medición. Fijar A0 / N_eff0 no es relevante ahora.

Resultado de la corrida (caso09, bootstrap 12, 13 paneles): N_eff se mueve en sentido opuesto a D_ckm (Spearman −0.97) y resuelve donde D_ckm hace meseta. Con n_runs=50 queda ~32% bajo el valor al que converge (≈26 desde 1000 runs, W sola): la dirección es legible, el valor absoluto no.

## Qué no hace

- No porta `cluster_nodes` / `copresence_matrix`, ni calcula coercividad ni `node_presence` sobre caso09: dependen de cómo se reduce una órbita de período > 1 a nodos activos — **a estudiar** *(delamor: no es la unión trivial)*.
- No conecta nada al canal vivo. No toca rebuilds.
- No define D_masa_cuencas.

## Abierto

- Reducción órbita → nodos activos.
- Escala de D_masa_cuencas.
- `node_presence` (de `attractor_stats`, capa estática) — la distribución de activación por nodo que corresponde; no `node_probs`, que es del muestreo de σ₀.
