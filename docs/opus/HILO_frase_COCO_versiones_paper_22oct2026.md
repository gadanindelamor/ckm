# Hilo: la frase de COCO a través de las versiones del paper — 22 oct 2026
*Opus 5.5. Output secundario de la tarea PAPER (no bloquea el v30). Sólo presencias, por grep sobre cada versión; la ausencia sale de comparar versiones contiguas. Sin interpretar.*

Patrón buscado: `never (been )?connected | not connected to the live | nunca se conect | no se conect`. Versiones de `docs/paper/` y el v29 de `docs/opus/` (sin copias, CITAS, peg ni `_antes_`).

| versión | apariciones | líneas |
|---|---|---|
| v1 – v14 (incl. v10_x, v12_1) | 0 | — |
| v15 | **1** | 255 (§3.7: *"COCO was never connected to the live IAP channel — in none of the 253 documented panels"*) |
| v15_borrador | 0 | — |
| v16 – v19 | 1 | 136, 129, 130, 130 |
| **v20** | **4** | 130, 194, 530, 652 |
| v21 | 4 | 132, 196, 532, 654 |
| **v22 – v26** | **5** | v22–v25: 132, 196, 211, 545, 667 · v26: 132, 196, 211, 549, 671 |
| v27 | 5 | 132, 231, 246, 616, 738 |
| v28_borrador | 4 | 138, 242, 257, 639 |
| v29_borrador_opus | 4 | 144, 266, 281, 668 |
| **v30_borrador_opus** | **0** | retirada (delamor, 21 oct) |

**Lo que muestra la comparación (presencias, no causas):**
- Nace en **v15** (Sep 2026, cabecera: Sonnet 4.6 + Code), en §3.7, una vez.
- **v19 → v20: de 1 a 4.** Aparece en β_collective, en los gaps y en la descripción de COCO (*"Verified in unit tests and test drivers; never connected to the live IAP channel"*).
- **v21 → v22: de 4 a 5.** **v27 → v28_borrador: de 5 a 4.**
- Ninguna de estas variaciones tiene, en lo leído hoy, una decisión registrada que la explique. **No se buscó** en `docs/tasks/DECISIONES_opus.md`, los REG ni el META REG: queda como ausencia declarada de este hilo, no como hallazgo.
- El 21 oct Opus contó **tres** lugares en el v29; eran **cuatro** (el de l.266, dentro de un corchete). El grep de hoy lo encontró; la lectura de ayer no.
