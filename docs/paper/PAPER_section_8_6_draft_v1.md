# §8.6 — Field and Reading Apparatus: Scope of Measurement

*Adición a PAPER_section_8_draft_v1.md · §8.6*
*Fuente: Claude Code, evaluación pre-IAP · THEORY.md R10-R13 · Ago 2026*
*Insertar después de §8.5, antes del cierre de sección.*

---

### 8.6 Field and Reading Apparatus: Scope of Measurement

A distinction noted during development is precise enough to state
explicitly. Claude Code, in a pre-IAP evaluation of the codebase, wrote:

> "Los cambios de servicios (fabrication_index, word boundary, RNG) son
> correctos pero transparentes a P1-P4 por diseño: los experimentos miden
> el campo, no el aparato de lectura."
> ("Service changes [...] are correct but transparent to P1-P4 by design:
> the experiments measure the field, not the reading apparatus.")

**The field** is W — the symmetric co-occurrence weight matrix, built once
from a corpus. P1-P4 operate on W directly as a mathematical object:
hysteresis (P1), cascade distributions (P2), temporal asymmetry (P3),
optimal negative pair density (P4). These are structural properties of W.
The field is static once built.

**The reading apparatus** is the inference-time machinery: NodeExtractor
(TF-IDF extraction, word boundary detection), FabricationService
(fabrication_index), CorpusService (opposition marker routing, sampling).
These services process incoming text and map it onto W. They are how the
field is read, not what the field is.

"Transparent to P1-P4" means: P1-P4 receive W as input and never invoke
the reading apparatus. Changes to word boundary detection, the fabrication
index, or the random number generator do not modify W, and therefore do
not modify P1-P4 results. The reading apparatus could be completely
replaced without affecting any empirical validation finding.

**The scope implication:** P1-P7 are claims about field geometry — about
the attractor landscape, coercivity structure, and cascade behavior of W.
They are not claims about how any particular implementation reads text into
that field. This separation is architecturally enforced: W is built from
the corpus once; the reading apparatus evaluates new inputs against the
pre-existing W.

This separation carries an epistemological consequence. The validation
results establish that the structural field has specific measurable
properties. They do not establish that any particular text processing
pipeline will reliably activate the relevant nodes from arbitrary input.
That is a separate question — the accuracy of the reading apparatus as an
instrument for mapping from natural language to field-space — and it is
not addressed by P1-P7.

**Connection to R10–R11:** THEORY.md rules R10 and R11 address a related
structural point. R10 states that divergence between perspectives is
information, not noise. R11 states that divergence between perspectives is
recorded as a node in the graph. Both rules presuppose the field/apparatus
distinction: what gets recorded as a node is not raw text or model output
but a structural divergence identified by the reading apparatus and
materialized in the field.

The reading apparatus does not create divergence — it detects it. The
divergence is a property of the field configuration; the apparatus makes
it accessible. R11's "recorded as a node" is a field operation, not an
apparatus operation. The same divergence might or might not be detected
depending on the apparatus; if detected, what is added to the graph is
the structural divergence, not the particular text that revealed it.

*[AUTO: pull to write "this separation guarantees the validity of P1-P7
independently of any implementation." Resisted — it guarantees scope
independence, not validity in general. Whether W correctly captures the
structural field of the corpus depends on how W was built, which depends
on the apparatus that built it (CorpusService, NodeExtractor). The
separation is clean at runtime; at construction time, W is apparatus-
dependent.]*

---

*§8.6 complete.*
*One [AUTO] flagged: scope independence ≠ validity independence.*
*R11 connection: divergence is a field property made accessible by the*
*apparatus — the node recorded is the structural divergence, not its*
*textual trace.*
*Source attribution: Claude Code pre-IAP evaluation (exact session not*
*recoverable — formulation used as primary, not attributed as finding).*
