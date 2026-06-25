# REG_qr_asymmetry_fourforums_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Pipeline v8h — W asimétrico fourforums gun control*
*Clase R*

---

## Fuente

Script: `fourforums_pipeline_v8h.py`
SQL: `fourforums_no_parse_2016_05_18.sql` (544MB, ~1270 líneas batch INSERT)
Explorador previo: `explore_qr_asymmetry_v1.py`
Output: `W_asim_v8h.json`

Cadena de join:
`mturk_2010_qr_task1_worker_response.(page_id, tab_number, disagree_agree)`
→ `mturk_2010_qr_entry.(page_id, tab_number)` → `(discussion_id, post_id, quote_index)`
→ `post.(discussion_id, post_id)` → `responder_author_id`
→ `quote.(discussion_id, post_id, quote_index)` → `(source_discussion_id, source_post_id)`
→ `post.(source_discussion_id, source_post_id)` → `quoter_author_id`
→ `mturk_author_stance` → stance T0/T1 (topic_id=9, gun control)

---

## Cobertura

| Métrica | Valor |
|---------|-------|
| Discusiones gun control | 905 |
| Autores con stance | 304 (T0=96, T1=208) |
| Posts gun control | 35,966 |
| Quotes gun control | 42,395 |
| Pares QR anotados | 9,975 |
| Votos task1 total | 54,005 |
| Votos resueltos | 7,876 (14.6%) |
| Pares autor N≥2 | 513 |

Nota: resolución 14.6% porque qr_entry cubre todos los topics — 80% de votos
corresponden a discusiones fuera de gun control, no a errores de join.

---

## Asimetría de stance confirmada

| Par | n | mean_da | disagree% | agree% |
|-----|---|---------|-----------|--------|
| T0 cita T1 | 3,947 | −1.613 | 64.7% | 16.1% |
| T1 cita T0 | 1,809 | −1.473 | 62.7% | 17.1% |
| T0 cita T0 | 543 | −1.035 | 57.3% | 23.8% |
| T1 cita T1 | 1,577 | −0.339 | 43.1% | 31.4% |

---

## Hallazgos estructurales

### H1 — T1 tiene cohesión interna, T0 no

T1-T1: mean_da=−0.339, múltiples pares con valores positivos:
- 679→755: +2.091
- 323→755: +1.778
- 682→2104: +1.556
- 20→415: +1.040
- 682→755: +0.396
- 148→755: +0.618

T0-T0: todos negativos sin excepción. T0 tiene tensión interna real.
T1 tiene cohesión interna real.

### H2 — T0 es el atacante estructural

T0 cita T1 a 2.18× la frecuencia de T1 cita T0 (3,947 vs 1,809).
Intensidad del ataque también mayor (−1.613 vs −1.473).
T0 inicia el contacto adversarial. T1 responde.

### H3 — Autor 148 es el equivalente estructural de autor 965

Autor 148 (T1) aparece como `responder` en 7 de los top-10 pares:
- 437(T0) → 148: n=699, mean_da=−1.817
- 37(T0) → 148: n=248, mean_da=−0.996
- 436(T0) → 148: n=208, mean_da=−1.760
- 442(T0) → 148: n=126, mean_da=−1.857
- 132(T0) → 148: n=101, mean_da=−1.970
- 127(T0) → 148: n=74, mean_da=−1.959
- 1069(T0) → 148: n=35, mean_da=−0.343

Múltiples T0 convergen sobre 148. Alta coercitividad. Haz de rectas verificado.
Convergencia con P7 y estructura de autor 965 (CreateDebate).

### H4 — Autor 437 es el atacante dominante (T0)

Autor 437 (T0): mayor out-citation hacia T1 (699 votos sobre autor 148).
Contraparte: 148 cita a 437 con n=294 — la tensión es bidireccional pero asimétrica.
437 es el equivalente estructural del atacante dominante en CreateDebate.

---

## Convergencia con resultados anteriores

| Resultado previo | Confirmación v8h |
|-----------------|-----------------|
| P7: nodo tipo-965 con haz de rectas | Autor 148 con 7 atacantes convergentes |
| P6: Delta rompe simetría | T0-T1 vs T1-T0 difieren en n y mean_da |
| Holonomía fourforums (amplitude) | T0→T1 más intenso que T1→T0 |
| T0 como atacante estructural | T0 cita T1 al doble de frecuencia |

---

## Pendientes

- Mapear author_ids a topic nodes (N×N W_asim para experimentos CKM)
- Verificar si autor 148 tiene el mismo perfil C3 que autor 965
- Documentar limitación: cross-topic quotes del quoter no capturadas
  (quote.source_discussion_id puede ser de otro topic — quoter fuera de gun_dids)

---

## Archivos relacionados

- `W_asim_v8h.json` — output completo con top_pairs
- `explore_qr_asymmetry_v1.py` — explorador previo (schema + row counts)
- `fourforums_pipeline_v8h.py` — pipeline (en Codespace ckmdatasets)
- `REG_holonomy_coercivity_fourforums_v1.md` — antecedente
- `REG_author_965_structure_v1.md` — estructura análoga en CreateDebate

---

*Clase R · Jun 2026 · Codespace ckmdatasets*
