# Verificación del PLAN_v33 (28 oct) contra el mapa del barrido y contra el v32 — 29 oct 2026 (Opus 5.5, Cowork)

Pedido de delamor: *"PLAN_v33_28oct2026.md sobre esa propuesta puedes verificar contra el mapa mientras leo?"*
Fuentes: `docs/opus/PLAN_v33_28oct2026.md`, `docs/opus/BARRIDO_v33_29oct2026.md` (y sus dos archivos de eventos), el v32 (`docs/opus/PAPER_Landscape_Driven_Device_v32_borrador_opus.md`, 1117 líneas). Sin interpretar. Lo que pide decisión va marcado **[delamor]**.

## 1. Las citas del plan contra el v32

Todas coinciden con lo que el plan dice, con dos excepciones:

- **IAC v2.** El plan cita l.398 y l.900 para *"[Permiso de uso pedido — pendiente]"*. Ese texto no está en el cuerpo del v32. Está sólo en el bloque de arriba (l.50: *"Permiso de uso: pedido pendiente"*). En el cuerpo, l.398 y l.900 ya dicen *"not redistributed… obtained from its maintainers"*. Lo que falta hacer es sacarlo del bloque de arriba.
- **Abstract.** El plan cita l.61–67. La frase *"Three properties of the static model are shown to be fixed by premise"* está en l.67. Hay una frase del mismo tipo en §8.1, l.737 (*"Fixed by premise on W ≥ 0 snapshots"*), y el plan ya la cubre en §8.1.

Coinciden: l.266/272 (P1, P3, P4 y P2), l.312, l.326, l.334 (*"what jumps is its representation"* y *"[Propuesta — decide delamor.]"*), l.342, l.344 (*"N_eff = 1 is total collapse…"* y *"approaches 1"*), l.346, l.370 (*"15.52"*), l.396 (*"[a verificar.]"*), l.404–416, l.553 (*"register in draft"*), l.567, l.724, l.752.

**El cambio "representation → measurement"** (§4.2 y §4.2.4) coincide con delamor (23 oct, decisiones l.142) y con las DEFS v20 (l.291: *"lo que salta es la medición"*).

## 2. Lo que vino después del plan y el plan no tiene

**"COCO regula el campo" nunca fue válida** (delamor, 29 oct: ningún elemento de 𝓡(H) regula H; COCO regula representaciones del campo).

El v32 todavía dice:
- l.310: *"4.2.1 COCO and Field Regulation"*;
- l.312: *"COCO is a field regulator, not a field observer"*;
- l.329: *"COCO: field regulator over its own Δ_r_compresiones"*;
- l.702: *"executed by COCO as continuous field regulation"*;
- l.706: *"the field intervenes through COCO's regulation"*.

El plan no toca ninguna de estas líneas. delamor dijo *"se retiró del paper que coco no regula"*, pero en el v32 la frase está.

La razón del retiro sigue sin encontrarse (B7 del barrido). El mapa tiene un candidato: un bloque con "COCO … regul…" que se va en v14 → v15 y no vuelve. No lo leí.

## 3. El plan contra el mapa

El plan edita el v32. Lo que se fue antes de v32, el plan sólo puede tocarlo si lo trae de vuelta.

**Lo que el plan trae de vuelta (sería un "vuelve" en el v33):**
- **β (M3)**, en §4.2.3: un párrafo con β_i, β_collective, beta_c_corpus, beta_c_landscape y beta_c_nonzero/global.
  - En el mapa, los bloques de β colectivo se van en v14 → v15 y v15 → v16.
  - En v29 β_collective bajó a una cláusula (bloque de arriba del v29, l.11, M3); en el v32 está en l.314.
- **"La masa de cuenca es una medición sobre las cuencas, no la única."** No es un bloque del mapa: es nuevo.

**Lo que se fue con razón registrada en el paper y el plan no decide:**
- **§7.6 *Knowledge Representation and the Cohesive Turn***: 7 bloques que se van en v28 → v29, más 1 de *"Knowledge Representation and Signed Weights"*.
  - La razón está en el v32, l.724: *"retirada en v29 — review M5, opción a: el paper es un instrumento de paisaje, no una teoría del conocimiento. Propuesta; si delamor la quiere, vuelve con la revisión de literatura 2023–2026"*.
  - El bloque de arriba del v29 (l.3) dice *"Nada entra sin su confirmación"*. No encontré una confirmación de delamor de esa salida (en decisiones ni en los ESTADO del 15 al 28 oct).
  - Después, el 23 oct (decisiones l.137, el esquema CKM de delamor): *"1 encuadre teórico — representación del conocimiento y medir el campo son perspectivas de lo mismo; full meaning ('si va')"*.
  - El plan lo trata sólo como *"la nota en castellano de §7.6 (l.724) no va al `_print`"*.
  - **Si §7.6 vuelve, y en qué forma: [delamor].** Es su ejemplo del barrido.
- **Gatekeeper**: 4 bloques que se van en v28 → v29. En v29 quedó en una oración (M8), y en el v32 está en l.256. El plan no lo menciona.
- **D_ckm Negative Values**: 4 bloques que se van en v28 → v29 y 1 en v30 → v31. En el v32 §7.3 sigue (l.645). El plan no lo menciona.

**Lo que se fue sin razón registrada en el paper y el plan no menciona.** El encabezado de v15 no registra el corte v14 → v15: repite el bloque de cambios de v3. No busqué la razón fuera del paper (NOTAS, work_reports). Los grupos más grandes que se van y no vuelven, por título, con la cantidad de bloques:
- v14 → v15:
  - The Material Issue (17)
  - P4 at N=64 — Threshold Finding (8)
  - Introduction (7)
  - J-Space (7)
  - Conditions, Not Constraints (7)
  - **Operational Services (7)**: la tabla de services, con CorpusService *"Builds W_mixta from corpus via TF-IDF node extraction"*
  - The IAP Chatroom as Methodological Instance (6)
  - Knowledge Graph (6)
  - Knowledge Admission and Gating (5)
  - Preserved Incompleteness: GAP as Formal Category (5)
  - Convergence by Independence (5)
  - Cohesion Measure (5)
  - Graph-Based Knowledge Representation (4)
  - Attractor-Based Memory Architectures (4)
  - Declared Influences (4)
  - Landscape Driven Devices — Theoretical Framing (4)
  - P6 — Directional Flow Across Corpora (4)
  - P7 — Type-965 Node (4)
- v15 → v16: Termap (6), Current Status and Open Conditions (6), y el índice (6).
- v30 → v31: Selected Findings (7).
- La lista completa, bloque por bloque, está en `BARRIDO_v33_eventos_29oct2026.md`.

## 4. Lo que queda para delamor
1. Si §7.6 (la representación del conocimiento) vuelve al v33, y cómo. Hay una salida en v29 sin confirmación encontrada y un "si va" del 23 oct.
2. Si el v33 corrige las cinco líneas de "COCO … field regulator" (§2). Lo que vino el 29 oct no estaba en el plan.
3. Si se busca la razón del corte v14 → v15 fuera del paper.
