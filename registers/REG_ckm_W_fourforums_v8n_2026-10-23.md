# REG_ckm_W_fourforums_v8n_2026-10-23

*Medición de las ocho W de fourforums (build_W_v8n, ckmdatasets) con el instrumento existente — TAREA 7, delamor, 2026-10-23*

## Partida

- Repo `ckm`, commit de partida `2fc81c3` (`git pull --rebase`). Clonado en el Codespace de `ckmdatasets` (`/workspaces/ckm`): ckm no estaba en ese Codespace; delamor eligió clonarlo y copiar las W desde `ckmdatasets/out/W/`.
- `.gitignore`: `process/datasets_private/` agregado **antes** de copiar las W (commit `e2c4b67`, junto con la predicción).
- W copiadas a `process/datasets_private/fourforums_W_v8n/`: 8 W + `manifest_v8n.json`. El mapa de ids (`nodes_map_v8n.json`) **no** se copió.
- sha256 de las 8 W verificados contra el manifest: **8/8 coinciden** (tabla abajo). El script los vuelve a verificar antes de medir.
- Predicción escrita en la BANDEJA y commiteada (`e2c4b67`) antes de correr cualquier dinámica.
- Script: `experiments/medir_W_fourforums_v8n.py`. Usa `basin_masses`, `n_eff`, `relax_orbit`, `beta_c_landscape` y `sample_s0` (la pieza de muestreo que usa `basin_masses`; precedente: `orbitas_vs_estados_convergencia.py`) de `services/landscape_engine.py`. `services/` e `iap_chatroom/` no se tocaron.
- Muestreo: el de `basin_masses` por defecto (uniforme, `weighted=False`, `boltzmann=False`, `max_iter=200`). Seed 20261023, la misma para las ocho W y para los tres n_runs.
- Período por órbita: el script repite el muestreo de `basin_masses` con `sample_s0` + `relax_orbit` y compara las masas con `basin_masses`: **idénticas en las 24 combinaciones** (W × n_runs).
- Resultados: `process/datasets_private/fourforums_W_v8n/resultados_medir_W_fourforums_v8n.json` (fuera de git), sha256 `87c220dd4f1bc8be9ee13c9b221b7979a75eaf658b7d53bf96608de626275cfe`, con el sha256 de cada W adentro.
- Tiempo: 67.2 s sumando las 24 corridas (cada una incluye su verificación contra `basin_masses`); ver la columna "segundos" de la tabla de convergencia.

## Predicción (copiada tal cual de la BANDEJA)

## PREDICCIÓN — 2026-10-23 22:06 UTC · TAREA 7: medir las W de fourforums (v8n)

*Code (Claude Opus 5.5, Codespace `ckmdatasets` con `ckm` clonado en `/workspaces/ckm`). Escrita ANTES de correr cualquier dinámica. Sólo miré: los sha256 (8/8 OK), grados y media de pesos positivos de W_obs y W_presence.*

**Lo que no es predicción sino teorema / aritmética (no se "espera", se sabe):**
- W simétrica, diagonal 0, actualización síncrona → toda órbita tiene período 1 o 2 (Goles–Olivos). Período > 2: 0 en las ocho.
- relax(−σ) = −relax(σ): las órbitas vienen en pares ±.
- `beta_c_landscape` = 1/(0.5·N·mean(W>0)) es aritmética, no depende de n_runs ni seed. W_obs: mean pos 0.2596 → β_c ≈ 0.0528. W_sign: mean pos = 1 → β_c = 1/73 ≈ 0.01370. W_presence: mean pos 0.02058 → β_c ≈ 0.666. W_null_s*: distinto en cada una (los signos se permutan, las magnitudes quedan por arista, así que cambia qué magnitudes son positivas).

**Predicción (dinámica, n_runs ∈ {1000, 5000, 20000}, muestreo uniforme por defecto de `basin_masses`):**
- **W_presence** (todo ≥ 0, ferromagnética, conexa, 36 nodos de grado 1): pocas órbitas, masa dominada por las dos de consenso (todo +1 / todo −1) y algunas mixtas. N_eff chico (del orden de 2–10) y **convergente** entre n_runs. Habrá período 2 (la actualización síncrona oscila en bordes bipartitos aun con pesos positivos), en fracción baja-moderada. Masa de la órbita mayor alta (≥ 0.2).
- **W_obs** (297 −, 75 +, 11 en 0; 168/354 triángulos frustrados; grado mediano 3, 39 hojas): paisaje vidrioso. Muchas órbitas distintas, que **crecen con n_runs** (no saturan en 20000). N_eff grande y **no convergente**: del orden de una fracción apreciable de n_runs. Masa de la órbita mayor chica (≤ 0.05). Fracción de período 2 alta (> 0.5): dominan las negativas, y en síncrono lo antiferromagnético oscila.
- **W_sign**: como W_obs en orden de magnitud. Sin magnitudes aparecen más campos locales h = 0 exactos (empates que congelan el nodo), así que espero algo distinto, sin dirección que pueda afirmar.
- **W_null_s1..s5**: mismo régimen que W_obs (vidrioso, no convergente, período 2 alto). Las cinco cerca entre sí. W_obs tiene menos triángulos frustrados que el nulo L3 (168 vs 194 ± 12.6), y si eso pesa en el instrumento esperaría para W_obs un N_eff algo menor y una masa mayor algo más alta que las nulas. **Confianza baja** en esa dirección: puede caer dentro de la dispersión de las cinco.

**Lo que no sé predecir:** si W_obs se distingue de las nulas en alguna medida con estos n_runs; el valor de la fracción de período 2 en W_presence.

## Tabla W × medidas (n_runs = 20000)

| W | β_c landscape | N_eff (20000) | órbitas distintas (20000) | frac. período 2 por masa | frac. período 2 por conteo | masa órbita mayor | períodos presentes |
|---|---|---|---|---|---|---|---|
| W_obs | 0.052764 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | [2] |
| W_sign | 0.013699 | 20000.000 | 20000 | 0.9992 | 0.9992 | 0.00005 | [1, 2] |
| W_presence | 0.665540 | 3720.930 | 15605 | 0.9710 | 0.9928 | 0.00465 | [1, 2] |
| W_null_s1 | 0.045494 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | [2] |
| W_null_s2 | 0.044583 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | [2] |
| W_null_s3 | 0.040932 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | [2] |
| W_null_s4 | 0.044889 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | [2] |
| W_null_s5 | 0.043835 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | [2] |

## Convergencia (n_runs ∈ {1000, 5000, 20000}; muestras anidadas: misma seed → las de 1000 son prefijo de las de 5000 y éstas de las de 20000)

| W | n_runs | N_eff | órbitas distintas | p2 masa | p2 conteo | masa mayor | sin cerrar | segundos |
|---|---|---|---|---|---|---|---|---|
| W_obs | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.26 |
| W_obs | 5000 | 5000.000 | 5000 | 1.0000 | 1.0000 | 0.00020 | 0 | 1.38 |
| W_obs | 20000 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | 0 | 5.14 |
| W_sign | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.32 |
| W_sign | 5000 | 5000.000 | 5000 | 0.9996 | 0.9996 | 0.00020 | 0 | 1.27 |
| W_sign | 20000 | 20000.000 | 20000 | 0.9992 | 0.9992 | 0.00005 | 0 | 5.28 |
| W_presence | 1000 | 826.446 | 934 | 0.9630 | 0.9754 | 0.00600 | 0 | 0.23 |
| W_presence | 5000 | 2243.360 | 4257 | 0.9662 | 0.9868 | 0.00580 | 0 | 1.21 |
| W_presence | 20000 | 3720.930 | 15605 | 0.9710 | 0.9928 | 0.00465 | 0 | 5.42 |
| W_null_s1 | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.25 |
| W_null_s1 | 5000 | 5000.000 | 5000 | 1.0000 | 1.0000 | 0.00020 | 0 | 1.17 |
| W_null_s1 | 20000 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | 0 | 7.69 |
| W_null_s2 | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.44 |
| W_null_s2 | 5000 | 5000.000 | 5000 | 1.0000 | 1.0000 | 0.00020 | 0 | 2.44 |
| W_null_s2 | 20000 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | 0 | 9.58 |
| W_null_s3 | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.54 |
| W_null_s3 | 5000 | 5000.000 | 5000 | 1.0000 | 1.0000 | 0.00020 | 0 | 2.34 |
| W_null_s3 | 20000 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | 0 | 7.03 |
| W_null_s4 | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.25 |
| W_null_s4 | 5000 | 5000.000 | 5000 | 1.0000 | 1.0000 | 0.00020 | 0 | 1.43 |
| W_null_s4 | 20000 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | 0 | 6.12 |
| W_null_s5 | 1000 | 1000.000 | 1000 | 1.0000 | 1.0000 | 0.00100 | 0 | 0.28 |
| W_null_s5 | 5000 | 5000.000 | 5000 | 1.0000 | 1.0000 | 0.00020 | 0 | 1.46 |
| W_null_s5 | 20000 | 20000.000 | 20000 | 1.0000 | 1.0000 | 0.00005 | 0 | 5.68 |

## sha256 verificados

| W | sha256 (verificado contra manifest_v8n.json) |
|---|---|
| W_obs | `e1659d55e1bf092f243338f960ea81456aa2ba37a302d35543230ecdae5cf038` |
| W_sign | `df596e5d3814c6bb0131ba1ddd24c517649d0111f007df6c33f62c735fc66665` |
| W_presence | `bf82cf3d0121b84199ced4204d27d51d387e8f651c48ce18999b772bd25b5249` |
| W_null_s1 | `ac9ca0ad2bc362ff56ae9e6ef71460b54dc3cd0230d331b819de86a20972818d` |
| W_null_s2 | `88717cc5065baba37ceb6896550b5eaf61c1f2d9d572289bf9335f6ca2ea53f1` |
| W_null_s3 | `9a91e749a58eceb468433c88826d924980e81cb58c420a879f7f85f8e9ca1cd7` |
| W_null_s4 | `697dcea3b40c004134e00cb3b4e5488e8a17abd58d783ba58820f3cb9f7e0019` |
| W_null_s5 | `35d0645b81f220ae476a3023dd5aa780f9beca051207ca02ca9d27c8ced1080b` |

script_sha256: `ff36b229a3be3c4b4c51d54da843314c09b0e641b82f731538874b2de853858b` · git_head al correr: `e2c4b67` · fecha UTC: 2026-10-23 22:06:13 · seed: 20261023 · muestreo: basin_masses por defecto: uniforme, weighted=False, boltzmann=False, max_iter=200 · manifest_sha256: `09de177410c4ea03f7961720429cded875fb6cc5de96989ff446375af0fc6d45`

## Lo que estos números no dicen

- En W_obs, W_sign y W_null_s1..s5, N_eff = n_runs y órbitas distintas = n_runs en los tres n_runs: ninguna órbita se alcanzó dos veces. El instrumento está en su techo: estos números no dicen cuántas órbitas hay, sólo que hay más de las que 20000 muestras revisitan. No dicen si N_eff converge.
- Por eso no dicen si W_obs se distingue de las nulas en N_eff, órbitas o masa mayor: las seis coinciden en el techo. Sólo β_c_landscape difiere, y es aritmética de las magnitudes positivas.
- W_presence: N_eff y órbitas crecen con n_runs (826 → 2243 → 3721; 934 → 4257 → 15605). No dicen dónde, ni si, satura.
- Sólo muestreo uniforme por defecto. No dicen nada del modo `weighted` ni del `boltzmann` (β_c_landscape se reporta, no se usó para muestrear).
- Sólo dinámica síncrona determinista con `max_iter=200` (ninguna corrida agotó max_iter). Que no aparezca período > 2 es el teorema (Goles–Olivos), no un hallazgo.
- Una sola seed; muestras anidadas entre n_runs. No hay estimación de varianza entre seeds.
- Las W son productos de extracción con decisiones declaradas (O1–O7 en ckmdatasets): no dicen qué pasaría con otra simetrización, otra elección de nodos u otra escala.
- No son P1–P4, ni D_ckm, ni nada sobre vivos.
- La comparación con la predicción está en el chat y en la BANDEJA, no aquí.
