# REG_termap_ckm_corpus_v1.md
*CKM — Termap y W matrix desde corpus real — Mayo 2026*

---

## Fuente

- Corpus: CKM_Informe_Trabajo_v2.docx — v25.docx (24 versiones)
- Párrafos totales: 5,145
- Nodos: 32 (N=32 completo)
- Termap: v2 (sin solapamientos entre nodos)
- Archivo W: W_ckm_corpus_v2.json

---

## Frecuencias de detección por nodo

| Nodo | Párrafos | Nota |
|------|----------|------|
| c_S | 892 | núcleo métrico central |
| hopfield | 514 | — |
| k_core | 490 | — |
| portero | 446 | — |
| red_verificacion | 382 | — |
| full_meaning | 315 | — |
| histeresis | 306 | — |
| conocimiento_cohesivo | 224 | — |
| COCO | 222 | — |
| cohesion_fabricada | 210 | — |
| AWARENESS | 207 | — |
| atractor_espurio | 195 | — |
| filtro_previo | 191 | — |
| sentido_comun | 139 | — |
| W_mixta | 93 | — |
| inconmensurabilidad | 97 | — |
| perspectiva_device | 106 | — |
| atractor_patron | 101 | — |
| perspectiva_deforme | 65 | — |
| BP | 61 | — |
| chispazo | 55 | — |
| traza_inferencia | 53 | — |
| M_M | 55 | — |
| DOM_I | 46 | — |
| DOM_II | 46 | — |
| campo_local | 36 | — |
| tension_estructural | 32 | — |
| divergencia | 24 | BAJO — concepto tardío |
| ATR_733 | 25 | BAJO — concepto tardío |
| beta_termal | 15 | BAJO — concepto tardío |
| vanishing_point | 18 | BAJO — concepto tardío |
| W_enriquecida | 13 | BAJO — concepto tardío |

---

## Top co-ocurrencias (pares de mayor W)

| Par | Co-ocurrencias |
|-----|---------------|
| c_S ↔ hopfield | 272 |
| k_core ↔ hopfield | 222 |
| c_S ↔ k_core | 204 |
| full_meaning ↔ c_S | 203 |
| full_meaning ↔ hopfield | 184 |
| full_meaning ↔ k_core | 179 |
| c_S ↔ portero | 178 |
| k_core ↔ histeresis | 166 |
| c_S ↔ atractor_espurio | 162 |
| c_S ↔ cohesion_fabricada | 158 |

---

## Estado

- W_ckm_corpus_v2.json: construida, guardada
- Pares negativos (W_mixta): NO definidos aún — pairs_neg.json fue perdido en sesión anterior
- P1-P4: pendientes de ejecución
- Nodos bajos (5): mantener por ahora — son información real sobre densidad del corpus

---

## Próximo paso

1. Definir pares negativos explícitamente (no reconstruir desde memoria — derivar desde estructura)
2. Construir W_mixta
3. Correr P1-P4
4. Guardar cada resultado como REG inmediatamente
