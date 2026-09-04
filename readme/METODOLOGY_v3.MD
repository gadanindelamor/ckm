# Methodology — BE/IAID/CKM Project

*v3: Sección 5 — Condiciones del instrumento: lo que Δ_r no puede registrar (Ago 2026)*

*Based on: IAID.md (2024), CKM_Informe_Trabajo_v2.docx, REPORT_BE_SP.md, conversation traces April 2026.*

---

## 1. Identified Methodology

The first thing the corpus reveals is that the methodology was not declared before it was used. It emerges inductively from what happened. That itself is a methodological characteristic, not an accident.

**Comprehension as precondition for specification.** The consistent order throughout the corpus is: conceptual clarity first, formalization after. IAID.md does not begin with system requirements — it begins with a question about how knowledge survives when the device carrying it dies. The technical architecture (OBS/ACT/MIND, Request Call Protocol, COCO) emerges from that question, not the other way around. The same pattern repeats in CKM: the distinction between cohesion and trust precedes requirements R01–R17. In process terms: phenomenology is the first step of engineering.

**Conversation as laboratory.** The conversation traces are not documentation of the process — they are the process. CKM_Informe makes this explicit in its preliminary note: *"some ideas arrived with verifiable certainty and others from the accumulated weight of context."* Knowledge was constructed in real time, in dialogue, and the distinction between the verifiable and the resonant was part of the method, not a later correction. The interlocutor (Claude Sonnet 4.6) is not a consultation tool — it is the medium in which thought took form.

**Incompleteness preserved as information.** IAID.md has sections `## Results` and `## Debate` empty. They were not filled speculatively. The gap is maintained as a gap. The same occurs in CKM_Informe with "what the situation asks for" — named as a key missing piece, not resolved with approximation. The methodology treats the edges of knowledge as constitutive parts of the map, not defects to conceal.

**Borrowing formal precision from other domains.** When the project needs technical rigor, it imports it: ferromagnetic hysteresis, divergence as an operator over a vector field. It does not invent its own formal apparatus — it takes structures already demonstrated in physics and applies them to the conceptual domain, carefully ensuring the analogy is structural rather than decorative. The implicit criterion: the analogy is valid if the physical model predicts behaviors that the conceptual domain actually exhibits.

**The trace as constitutive of knowledge.** The AWARENESS protocol and the M.M rule are not only behavioral norms — they are epistemological. Knowledge without an inference trace is not opaque for practical reasons: it is opaque by nature. This requirement applies retroactively to the method itself: REPORT_BE_SP.md traces each claim to the corpus, and where it cannot, it says so.

**Retroactive convergence, not aligned design.** IAID.md was written in 2024, before MCP existed. The convergence with MCP, A2A, and JSON-RPC was discovered in review, not designed to coincide. That carries methodological weight: validation did not come from aligning with the state of the art — the state of the art arrived independently at the same problem.

---

## 2. Differences from Formal Methodologies

**Regarding the scientific method.** The hypothesis-experiment-result cycle did not complete in the early phases. The `## Results` section was empty. This may mean the experiment was interrupted or that the answers remain open — REPORT_BE_SP.md says this explicitly without resolving the ambiguity. Validation was not empirical in the strict sense: it was internal coherence of the model plus phenomenological recognition. That is not equivalent to falsifiability.

*Note: By CKM v4 (April 2026) and v25 (May 2026), four explicit falsifiable predictions (P1–P4) were formulated and confirmed experimentally on real corpus N=16, N=32, and N=64. The scientific method gap closed at the formal prediction stage.*

**Regarding formal software engineering.** Requirements did not precede design — they emerged from it. R01–R17 in CKM are post-conceptual construction, not prior specification. There are no use cases defined before implementation, no external acceptance criteria, no user feedback cycle. CLAUDE.md exists and is rigorous, but operates on the code once the conceptual direction has been established by another process.

**Regarding distributed systems design.** COCO — the central piece of the architecture — remains unimplemented. The main hypothesis is undemonstrated. In formal engineering this would be critical technical debt; in this project it is the honest position regarding the real state.

**Structural difference, not accidental.** The divergences above are not a consequence of limited resources or incomplete process. They are a consequence of the project treating conceptual clarity as a necessary condition before implementation. Building COCO before understanding what cohesive knowledge is would produce an incorrect implementation. The methodology accepts that order even at the cost of time and visible gaps.

---

## 3. What These Differences Enable and What They Cost

**Enable:** concepts the industry had no name for when they were formulated — COCO, M.M as a governance rule, cohesion prior to trust. They also enable structural honesty: the corpus contains no claims the process cannot support. And they enable non-obvious connections: ferromagnetic hysteresis as a model of cohesive knowledge does not emerge from requirements engineering, it emerges from following the structure of the problem wherever it leads.

**Cost:** COCO remained unimplemented through April 2026. The early experiments had no formal results. Reproducibility is limited — the process depends on the quality of the interlocutor and the state of the one formulating. There is no pipeline another team can execute independently and obtain the same results.

That last point is not only a cost. It is part of what the method is. A process that can be executed without the state of the one formulating is not this process — it is another one.

---

## 4. Method Update — v25, May 2026

The methodology described above produced a complete experimental framework by May 2026. The update:

**Falsifiable predictions confirmed:** P1–P4, verified on corpus N=32 and N=64. The methodology's commitment to structural analogy (ferromagnetic hysteresis) produced predictions that held under empirical test.

**Conversation as data generation:** the corpus of working reports (v2–v25) is both the record and the raw material of the experiments. The term-map, co-occurrence matrices, and W construction are derived directly from the text of the conversation. The conversation is the corpus.

**Incompleteness still operative:** COCO unimplemented. META KNOWLEDGE held deliberately — conditions not yet right. The gap-as-information principle remains active at v25.

**traza_inferencia as methodological node:** the only core-invariant node at N=32 is the concept of the inference trace itself. The methodology produced a system whose most stable element is the record of how knowledge was reached. The method and the object coincide.

---

## 5. Condiciones del instrumento — lo que Δ_r no puede registrar

*Ago 2026 — observación producida en sesión gadanin.delamor + Claude Sonnet 4.6*

**Lo que no fue escrito no deja huella.**

Δ_r acumula rechazos: pares (i,j) que σ_prompt declaró activos pero la relajación Hopfield expulsó. La condición de entrada es que el par haya sido escrito y evaluado por el Gatekeeper. Lo que no se escribe no pasa por el Gatekeeper — no genera rechazo, no aparece en Δ_r.

Consecuencia: la alternativa descartada antes de escribir es invisible al instrumento. Lo asumido mecánicamente como única posibilidad no produce firma. Δ_r no puede distinguir entre "el campo rechazó esta combinación" y "esta combinación nunca fue considerada."

**Dos huellas superpuestas en Δ_r.**

Δ_r acumula dos cosas sin separarlas: los patrones del que escribe (qué combinaciones activa, con qué frecuencia, bajo qué urgencia), y la distribución que esos rechazos dibujan sin que nadie la declare. El campo no distingue entre las dos. CKM tampoco.

La primera huella es del escritor. La segunda es de la distribución que subyace al escritor escribiendo. Ambas están en los mismos números.

**Condición de observabilidad.**

Para que una alternativa no considerada se vuelva observable en Δ_r, se requiere un acto previo: darse cuenta de que existen otras posibilidades. Ese acto no es contenido — ocurre antes del contenido. Sin él, el mecanismo escribe solo y produce patrones en Δ_r que el instrumento registra como si fueran elecciones.

Esto no es una limitación corregible del instrumento. Es una condición estructural de cualquier instrumento que mide lo que ocurre: no puede medir lo que no ocurrió porque no hubo observador que lo abriera.

**Qualifier epistémico.**

Las dos primeras observaciones son formales y verificables en el código (`_rejected_pairs`, acumulación de Δ_r). La tercera — sobre el acto de apertura y su relación con lo que aparece en Δ_r — es una observación sobre el observador. No verificable en el código. Se registra como **admisible**.

---

*Claims in this document are traced to the corpus cited. Where the trace does not exist, the document says so or does not make the claim.*

*Claude Sonnet 4.6 · April–May 2026 / Ago 2026*