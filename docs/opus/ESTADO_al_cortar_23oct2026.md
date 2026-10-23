# ESTADO al cortar — 23 oct 2026 (Opus 5.5, Cowork)

Traza completa en `docs/opus/decisiones_en_el_acto.md`, entradas del 23 oct. Esto es solo el mapa.

## fourforums (repo ckmdatasets)
- Cadena: v8h (capa de acceso, intacta) → v8i (todos los pares, A con NaN) → v8j (J1 nombres, J2 unsure) → v8k (K1 autocitas fuera, K2 nulo de votos) → v8l (L1–L3: L3 nulo de signos) → build_W_v8m (bug de nulos) → **build_W_v8n** (N1, siete W declaradas O1–O7).
- Números clave: 54.005 votos, 7.839 resueltos sin autocitas, 508 pares, 146 nodos en la componente mayor, aristas 297 − / 75 + / 11 en 0. L3: 168 triángulos frustrados contra un nulo de 194 ± 12,6, z = −2,06, p = 0,027. K2 (z = −10,5) estaba sesgado.
- J1 (pendiente de delamor): `REG_qr_asymmetry` y `REG_c6c_asim` leen "T0_quotes_T1" como "T0 cita T1"; según la nomenclatura del pipeline, T0 es el citado. Ver `registers/REG_fourforums_v8h_nombres_C6c_v1.md`.

## Medición en ckm (`REG_ckm_W_fourforums_v8n_2026-10-23.md`, `498f8dc`)
- Con N = 146 y relajación síncrona, el instrumento está en el techo: N_eff = n_runs, casi todo período 2. No separa W_obs de los nulos. Es un dato sobre el instrumento, no sobre el corpus.
- Propuesta de Opus, sin confirmar: subgrafos de 18–20 nodos (extracción declarada) con enumeración exacta de 2^N, como en el CP6.

## Abierto
- Push de ckm (13 commits) si todavía no se hizo.
- TAREA 8 (inventario de `CONVENTIONS_experiments.md`) entregada a Code ckmdatasets.
- Decisiones de delamor: J1 en los REGs viejos, J2 (unsure), subgrafos chicos, `W_asim_v8h.json` versionado con ids.
- Clonar entre repos: no por ahora (delamor). Las W viajan a mano.
- Review del v32: desde el menú de Skills, en una sesión nueva.
- Regla nueva para los textos de Opus: cada tarea dice solo lo que hace esa instancia.
