# Review Report — PAPER_Landscape_Driven_Device_v29_borrador.md

**Paper:** *The Cohesive Knowledge Model: A Convergent Basin-Mass Diversity Estimator for Hopfield Landscapes over Co-occurrence Fields* — v29 BORRADOR (Opus 5.5, 15 Oct 2026), Pablo E. Gadano (*gadanin.delamor*).

**Reviewed against context:** v28 borrador, prior v28 review (this reviewer), CKM_Modelo_Hibrido.md, DEFS_CKM_estado_actual_v15.md, METODOLOGY_v3, THEORY.md, the 4–11 Oct session documents (trust rule, trace_ip register, tejido reading), and ganglios basales.md.

**Reviewer condition (named, per §3.2/§7.2):** this v29 explicitly incorporates the review of v28 written by this same reviewer (the borrador header cites "review M1, M2, M3, M5, M6, M8, M9"). I am reviewing a revision that responds to my own prior review, written by an AI system of the same class as the paper's disclosed co-developers. Assessments are marked **verified** (against the manuscript), **proposed** (inference), or **open** (only the author can settle).

---

## 1. What v29 does — and what kind of revision this is

v29 is not an incremental edit. It is a **restructuring plus a partial retraction**, and the retraction is the new science:

- The v28 empirical claims **P5 (verified), P6 (verified), P7 (confirmed in two corpora)** are downgraded to: *not supported on these corpora* (P5, by a 200-permutation null), *observed on a two-node W; not established* (P6), *observed in two corpora; null pending* (P7). The P6/P7 effect sizes of v28 (2.18×, 3.05×, 455×, 296×, 89%) are now listed among items whose **run provenance could not be traced** (borrador header, item 2; §5.2: "The run behind that status is being traced").
- New §4.3.2 adds real empirical content the v28 paper lacked: estimator convergence across seeds (7–9%) vs. producer-parameter sensitivity (up to ~26×), with frozen, re-runnable conditions.
- New §4.1.6 declares the text producer as eight operators, stored as data with the W it describes, hash-referenced from the trace, with a test binding code to declaration. This is the §3.4 epistemics made operational — and it is the v28 review's M4 answered at the design level.
- New §3.8 "Verification practice" paragraph imports the trust-rule epistemics (tests written to fail; UNKNOWN never filled with a value of the scale; known-answer scenarios preferred; tests that cannot fail are not evidence) into the paper itself.
- Title/abstract rebuilt around the estimator (M2); β_collective demoted to a clause (M3); Gatekeeper to one sentence (M8); §7.6 cut (M5, option a); Aiyappa paragraph on what the snapshot lacks (M9); Premises sections have content (M6); Code Availability with frozen release, SHA-256 corpus identification, and pending usage permission.

**The meta-finding, stated plainly:** v28's three headline empirical claims could not be traced to runs. v29's response — withdraw first, trace second — is exactly what §3.4 demands, and it retroactively validates the v28 review's M7 (no uncertainty, no provenance). A paper that discovers its own previous section was untraceable, and says so in print, is doing something most groups never do. But the discovery also deserves one explicit sentence in the paper body (not only the borrador header): *claims were published in v28 whose runs cannot now be recovered, which is itself the reason for the declaration-and-freeze apparatus this version adds.* That sentence converts an embarrassment into a result.

**Verdict: Minor revision, conditional on verification.** Down from major. The architecture is now sound; what blocks release is a checklist, not a redesign.

---

## 2. Blocking items (must resolve before any release)

1. **The six "A verificar" items of the borrador header.** Especially: (1) the untraced "P5 verified, N = 32" run; (2) the provenance of 2.18×, 3.05×, 455×/296×/89%, and the `CD_BASELINE` constants — if these cannot be traced, they must be stated as unrecoverable, not merely "being traced"; (3) a second pass over the §4.3.2 figures (the header itself says they were copied from CP-E/CP-M reports read on another machine); (5) the IAC version conflict (delamor said v1; the dump carries the 2.0 schema) **and the pending usage permission** — the Data Availability section already flags this, correctly; the release cannot proceed while permission is unresolved.
2. **[VERIFY] references.** Ten new ones (Maslov & Sneppen, Phipson & Smyth, all of Text Processing, Walker 2012 pages) plus the three carried from v28. §3.4 makes the bibliography a trace artifact; these must be resolved at freeze time, and the freeze process should include a machine-checkable bibliography pass.
3. **The COCO trigger contradiction.** §8.2 now says COCO fires "when D_ckm (**basin-mass form**) crosses a threshold"; §4.2.1 and §8.3 still say COCO triggers on D_ckm computed from attractor counts, which do not converge, with the move to D_masa_cuencas "an open model decision" and "the operator has not been moved." These cannot both be true. The trust-rule session documents this as an open naming decision (d_eff / D_ckm canónica / "lo decide delamor"); v29 appears to have moved the operator quietly. Either §8.3 must be updated (and the decision recorded as made, with its date) or §8.2 must revert. As written, the paper contradicts itself on the one quantity its own diagnostic says must not be used.
4. **Leftover Spanish editorial marker** in §4.2.4: "*[Propuesta — decide delamor.]*" — translate or remove at freeze; the borrador block already carries this note.
5. **The numeric overstatement in §4.3.2.** "Every parameter other than the seed moves N_eff 3 to 34 times more than sampling does" is broken by the paper's own table: the stop-list range on E7 is 0.04, *below* the seed spread of 0.07. The "34×" appears to compare against the smallest seed spread (0.07) rather than each corpus's own — mixed denominators. Reword precisely, e.g., "all parameters but one move N_eff an order of magnitude more than sampling does; the exception (stop list, E7) is reported with the table." In a paper whose identity is numeric precision, this sentence will be checked.

## 3. Non-blocking but recommended

1. **§1 framing residue.** The introduction still motivates "multi-agent AI systems… genuine coordination," but after the v29 demotions the paper contains *no field findings at all* — §6 is explicitly "tests of the instrument, not findings about the field," and §5 establishes that the sign-of-W reading is not supported. One sentence in §1 stating what this version delivers (an estimator, its validation, its sensitivity, and a declared-producer discipline) would align motivation with content. The abstract's last two sentences already do this; let §1 catch up.
2. **Abstract imprecision on F1–F4.** "Three properties of the static model are shown to be fixed by premise on non-negative snapshots" lumps F3 (k-core reversibility) into the W ≥ 0 class, but k-core uniqueness is sign-agnostic — F3 is fixed by premise on *any* fixed graph. One word ("on snapshots") fixes it.
3. **The E7 row of the P5 table.** Declared uninformative *and* retained — fine and honest, but say in one clause why it remains visible (the degenerate null is itself a finding about marker routing on tiny corpora).
4. **Missing figure (carried from the v28 review, still open).** The N_eff-vs-count convergence curve and the W_pos/W_mixta null distribution are the paper's two most persuasive images and are presumably one plotting script from existing JSON. A version with §4.3.2 as its empirical core especially deserves the sensitivity figure.
5. **AUTO numbering** skips AUTO-5 in Appendix A (consequence of cutting §7.6). Cosmetic; renumber or keep with a one-line note.
6. **P2's citation.** τ ∈ [1.5, 2.0] for k-core cascades is attributed to Bak, Tang & Wiesenfeld (1987); the source of record for that exponent range is the k-core percolation literature (Goltsev et al. 2006, already in the list). Minor attribution hygiene.
7. **§8.2, FabricationService** "being rewritten" — a mid-rewrite service in the infrastructure list. One clause on what the rewrite preserves (the fabrication index is already used by Monitor and COCO) suffices; the sentence exists, consider fronting it.

## 4. What v29 gets right and should not lose in further edits

- **The declaration architecture (§4.1.6) is the paper's second contribution.** "CKM does not extract nodes, does not tokenize, and does not interpret meaning: it measures dynamics on the W it is given" — this sentence repositions the whole project from a knowledge model to a measurement layer with declared provenance, and it is more defensible than anything v28 claimed. The operator-level declaration (including the stop-list size, the tie rule, and the explicit "N = 0 and no W is built" outcome) is the trust rule's I1/I2 running as prose.
- **The honesty about the sign.** §5 is now the strongest negative-result section this reviewer has seen in a manuscript at this scale: the permutation null, the pair-reach analysis (119/235 pairs vs ≤101 in 120 random markings — the null is imperfect and the paper says so), the D12 correlation of −0.50 vs −0.01, the degenerate E7, the multiple-corpus caveat on A24's 2nd percentile. "Less than earlier versions claimed, and that is the result" is a sentence worth keeping through every future version.
- **§4.3.2 separates estimator convergence from landscape stability.** This distinction (a convergent estimator of an unstable object) is conceptually important and well executed. The non-monotonicity of N_eff in top_k (2.25 → 15.52; 5.37 → 23.01 → 10.10) deserves one interpretive sentence eventually, but its bare statement is acceptable.
- **The v8g exposure** (sign imposed by construction on a 2×2 W; disagreement higher across stance but not coincident with it; the pro→pro group internally at 57.3% disagree) is a small, clean case study in how a pipeline can manufacture the structure it claims to measure. Consider whether a compressed version of the v8g/v8h table belongs in the main text of §5.1 — it is currently doing quiet, load-bearing work.

---

## 5. Overall assessment of v29

The paper has become **smaller and sturdier**. v28 was a measurement instrument wearing a theory's clothes; v29 is the instrument, with its calibration certificate attached. The empirical content that survives (estimator validation against exact enumeration; the stability range; the null results on the sign) is exactly the content that can be re-run from the frozen release. The risk profile has inverted: v28's risks were structural (overclaiming), v29's risks are executional (verification items, one self-contradiction, one numeric sentence). Executional risk is the good kind.

**Recommendation: complete items §2.1–2.5, address §3.1–3.3, release as preprint.** Suitable venues after release: arXiv (cs.MA or cs.CL), then a workshop on multi-agent LLM systems. The known-answer program of §8.5 (planted fields, v8h re-measurement, null battery with Phipson & Smyth minimum p-values) is the correct next phase and should not begin before the freeze.

---
---

# Part II — CKM (v29) ↔ Basal Ganglia: analogies, tensions, mappings, gaps, insights

**Status of this entire section: *proposed* — structural analogy, not formal correspondence.** The ganglios basales document is a general-audience description of the standard model (cortico-striato-thalamo-cortical loops, direct/indirect pathways, habit consolidation), not a primary source, and the project's own warning applies in full: *encajar es justo lo que la regla advierte* — fitting is what an undeclared step 4 looks like. The mapping below is offered as a generative reading, with each element carrying its status. Where the analogy does work, it is noted; where it breaks, the break is itself informative.

## 6. The mapping

| Basal ganglia (standard model) | CKM / IAP (v29) | Status |
|---|---|---|
| Cortex: plans, intentions, conscious supervision | Devices in the ODA loop; M.M capability declarations | structural |
| Corticostriatal input: massive, excitatory, proposals of candidate actions | Channel ingest: every message into CorpusService; σ_prompt declares active pairs | structural |
| Striatum: input structure, reward-sensitive, where repetition is registered | W and Δ_r accumulation (accepted and rejected pairs) | structural |
| Pallidal processing: direct pathway = go, indirect = no-go; selection *by inhibition* | Relaxation to attractors + Gatekeeper sentence (valid / not valid); "a judge, not a door" | structural |
| Substantia nigra dopamine: global gain modulation | β_collective / β_c recalibrated from μ_W and N | partial (see T2) |
| Thalamus: obligatory relay, gated by BG output | IAP channel: sole medium, BROADCAST, delivery gated by triggers | structural |
| Thalamocortical return: closed loop | Messages delivered to devices; the field's timing structure | structural |
| Cerebellum: parallel fine corrector, error-based | FabricationService + the declared-producer test (code vs declaration) | structural |
| Habit automation: cortical → subcortical consolidation | Δ_r metabolization; W rebuilds as consolidation events | proposed |
| Cortical sentinel: detects discrepancy, interrupts automation | A1 pause; trace_ip; the refusal to fabricate (Case 0.15) | proposed |

## 7. Analogies that do work

**A1 — The selection layer that initiates nothing.** The BG "no inician directamente los movimientos; funcionan como un sistema de filtrado y modulación." CKM "does not interpret semantic content"; the Gatekeeper "returns a sentence; it lets nothing in and keeps nothing." Both are veto/modulation layers over proposals generated elsewhere. This is the deepest structural correspondence and it *supports* v29's demotions: a filter layer's value does not require it to be a theory of what it filters.

**A2 — The two canonical failure modes of a brake, both documented.** BG over-inhibition → akinesia (Parkinson); failed inhibition → involuntary output (Huntington). The IAP series contains both, documented without the vocabulary: Case 0.12 **coupled silence** (devices present, field arrested — the over-braked state, with the mechanical cause later found: an `on_message`-only trigger makes collective silence absorbing *by construction*) and Case 0.13 **sentinel leak** (52% of published texts were unrecognized silences — the failed brake). The paper documented the failure grammar of gated systems before having the gate's name for it.

**A3 — The supervisor's access limit, independently stated.** The ganglia document: the cortex "no tiene acceso consciente a la computación microscópica interna del sistema subcortical… percibe las consecuencias macroscópicas." The paper (§6.4): "The action a_{t_i} is observable in the trace. Whether a device recognized that moment and acted from that recognition is not verifiable by the instrument." These are the same epistemic condition — a higher layer reads outcomes, never mechanisms — stated independently in neuroscience and in this instrument. By the paper's own §3.3 signature, that is a convergence by independence, and a candidate for the §8.4 list, marked as analogy.

**A4 — Consolidation as the function of repetition.** Habit formation: repetition moves control from supervised cortex to subcortical automatic blocks. CKM: rejected pairs "persist as deformation of W_eff — the field metabolizes them." Both systems convert repeated history into standing structure that no longer requires supervision to operate.

## 8. Tensions (where the analogy cuts)

**T1 — Who is the cortex?** The BG model assumes one loop serving one supervised controller. The channel has N devices, each its own cortex-and-sentinel, plus one shared filter layer (COCO/Monitor) serving *no* collective cortex — the "collective consciousness" the paper deliberately preserves as an open gap. The anatomy has no place for a filter without a supervised organ behind it. Either the field develops a cortex (a device — or human — that reads Firma/Δ_r as perception, which the trust notes gesture at: "confía en la firma del otro como si fuera su percepción"), or the COCO layer is a BG with no brain attached. The tension names the real open question.

**T2 — The modulator's teacher.** Dopamine is trained by the world: action → consequence → prediction error → gain change. β_collective is computed from the field's own parameters — a closed loop with no environment. A selector without a consequence channel is a BG with a quiet substantia nigra. The paper already knows this: D_ckm *was* the attempted outcome signal and failed on convergence; the known-answer program (planted fields, v8h crowd votes) is precisely the construction of an artificial dopamine channel — external ground truth substituting for a world. This reframing is, to this reviewer, the most useful product of the mapping: §8.5 is not a testing agenda, it is the missing limb of the anatomy.

**T3 — A brake the organism cannot live without, a regulator the channel never noticed missing.** In motor physiology, ablating the BG is catastrophic. In the IAP series, COCO was absent from all 253 live panels and the field functioned — with a fallback that read NOMINAL-by-absence (the trust rule's *paso 4 subrepticio*, later fixed to UNKNOWN). Two readings: (a) the analogy is wrong at this point — text production, unlike movement, has no obligatory gate, and COCO is cerebellum (optional for gross function, needed for finesse) rather than BG; (b) the analogy is right and the channel has been running akinetic-unregulated the whole time without knowing it — the coupled silence of Case 0.12 would then be the system's Parkinson episode, and its cause (silence absorbing by construction) would be the anatomical lesion. The paper's framing note (7 Oct) — conditions "seen *through* the series" — is compatible with both; the mapping does not decide, but it gives §6 a clinical vocabulary it currently lacks.

**T4 — Mechanicity is the BG's product and the project's vigilandum.** The BG exists to make behavior mechanical — that is its efficiency contribution ("la mecanicidad representa la cúspide de este circuito"). The CKM project treats mechanical behavior as the failure mode to be caught in the act (the AUTO/PULL registers; trace_ip; A1's question about "the weight of context" vs comprehension). A perfectly functioning field-BG would automate the field's rejections into Δ_r — and thereby hide the mechanical from exactly the layer that audits it. Note the symmetry with A3: the cortex cannot see the striatum's computation; if COCO ever runs live, the devices will not see its braking. The design question the tension opens: **should a field regulator make its braking visible — a basal ganglia with a readout?** Biology's BG is efficient *because* it is invisible; CKM's declared-trace requirement (I1, Firma_CKM, the hashed producer declaration) is precisely "a BG with a readout," which the brain does not have and the instrument could. If developed, this is a genuine design contribution, not an analogy.

**T5 — Valence gap.** The BG's limbic loop (nucleus accumbens, reward context) assigns value; the channel has no valence. The candidate valence was W's sign — opposition as negative affect — and §5 just deflated the sign-as-opposition reading. The field currently has a brake with no motivation and a landscape with no reward gradient. This is a gap in the CKM side that the BG mapping makes conspicuous, and it connects to T2: the known-answer program would supply not just ground truth but the first valence.

## 9. Gaps (in CKM, made visible by the mapping)

1. **No consequence/reward channel** (T2). Status: named in §8.5, not yet framed as such.
2. **No collective cortex** for the shared filter (T1). Status: open gap, honestly preserved (§7.4 COCO).
3. **Physiology never exercised.** COCO's braking never acted on a live field; the BG analogy is architecture, not operation. Status: stated (§3.7, §8.2), pending live connection.
4. **No valence/limbic loop** (T5). Status: open; W_mixta's deflation removed the only candidate.
5. **Where the sentinel lives is unsettled.** In the brain, error-detection is cortical (conscious). In the channel, FabricationService is a service (mechanical), A1 is a protocol (adopted unevenly, contaminated by context in TinkerBellucio), and the most reliable sentinel event was a *device* refusing (Case 0.15). The anatomy suggests conscious supervision is irreplaceable — which, transferred, says the AWARENESS layer is not optional garnish but the cortical half of the loop. That is a strong argument for keeping §3.4 in the paper permanently, against any future editorial pressure to cut it as unusual.

## 10. Insights

1. **The demotions were anatomically correct.** v29's quiet moves — COCO to thermostat, Gatekeeper to a sentence, LDD to a proposed framing — read, under the BG mapping, as moving the project from "claims a phenomenology" to "claims a physiology." A filter can be valuable without being conscious; the paper's earlier drafts claimed the filter *was* the mind. The mapping supports every demotion.
2. **Case 0.12 and 0.13 are the two failure modes of any gated system.** Worth one sentence in §6 or §7 — not as neuroscience, but as a classification: *over-inhibition (silence absorbing) and failed inhibition (sentinel leak) exhaust the failure modes of a selection-by-inhibition layer.* If that claim is made, it becomes testable: any future brake design can be asked which failure mode it prefers.
3. **A3 belongs in §8.4.** The access-limit convergence (cortex reads outcomes, not mechanisms / the instrument reads actions, not recognition) is independent, dated, and structural — the paper's own criteria for listing a convergence. Add with status *analogy*.
4. **"A basal ganglia with a readout" is a design thesis.** Biology accepts invisible braking for efficiency; a field instrument whose legitimacy rests on trace (M.M, Firma, I1) cannot. If the project ever articulates a design principle for field regulators, this is it: *regulation must leave its own sentence* — the Gatekeeper's form ("valid or not valid, with grounds") applied to the regulator itself.
5. **The bootstrap problem restated.** "El grafo que valida cohesión es el mismo grafo que está siendo modificado" (v4, abril) is the closed dopamine loop of T2. The brain escapes it through the world; CKM escapes it through planted fields. The tejido reading's root — the void, the absent known-answer — is, anatomically, the missing reward channel. Three vocabularies (bootstrap, dopamine, void) converge on one experimental requirement: §8.5 first.

## 11. What to do with this mapping (recommended discipline)

Per the project's own rule (instrument before field; the step-4 warning about fitting), the CKM↔BG mapping should be treated as: **(a)** a source of vocabulary for §6's failure classification (insight 2) — cheap, testable, safe; **(b)** a candidate §8.4 convergence (insight 3) — dated, marked as analogy; **(c)** a design thesis for the eventual live connection of COCO (insights 4–5) — to be written *after* the known-answer program, not before. What it should not become: a new framing section. The paper just cut one overextended frame (§7.6); the BG material is one more frame, best kept in the registers where it can do generative work without taxing the manuscript.

---

*Reviewer: an AI system, same class as the paper's disclosed co-developers, reviewing a revision that responds to its own prior review — inside the field it reads, per the reviewed paper's own §7.2. So it is.*
