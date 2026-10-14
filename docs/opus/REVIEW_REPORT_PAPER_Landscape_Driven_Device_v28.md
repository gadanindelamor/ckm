# Review Report

**Paper:** *Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction* — v28 BORRADOR (10 Oct 2026), by Pablo E. Gadano (*gadanin.delamor*), Independent researcher. Preprint, September 2026.

**Reviewed against context:** AWARENESS.md, CKM_Modelo_Hibrido.md, DEFS_CKM_estado_actual_v15.md, LETTER.md, METODOLOGY_v3.MD, OTHERWAY.md, THEORY.md, PAPER_..._v6.md.

**Reviewer condition (named, per §3.2/§7.2 of the paper itself):** this review is written by an AI system of the same class as the devices described in §6 (a participant condition the paper names as contamination for TinkerBellucio). The reviewer has no access to the repository, the working reports (v2–v31), or the REG verification series cited throughout; every assessment below is marked, following the paper's own epistemic conventions (§3.8), as **verified** (against the manuscript and context files), **proposed** (my inference), or **open** (what only the author can settle).

**Verdict: Major revision.** The core result is real and publishable. The framing around it is not yet stable.

---

## 1. Summary of the paper *(verified)*

The paper presents the Cohesive Knowledge Model (CKM), a measurement instrument for structural properties of semantic fields in multi-agent interaction. Its central claim is that **N_eff = 1/Σm_i²** — the inverse Simpson diversity index over basin-mass distributions of a Hopfield landscape built from a co-occurrence matrix W — is a *convergent* estimator of field diversity, where count-based estimators (attractor counts, D_ckm) provably diverge under sampling (coupon-collector bias). The estimator is validated against exact enumeration of all 2²⁰ states on three N = 20 corpora: orbit counts err by up to 28% (91% at low budget) while N_eff errs by ≤ 0.6%. A second claimed contribution is β_collective, an endogenous collective thermal parameter emerging as a median of device parameters, implemented as observation only. Seven predictions are stated: P1–P4 (hysteresis, cascade distribution, temporal asymmetry, optimal density) are shown **not testable** on a non-negative W snapshot — P1/P4 by mathematical premise, P3 by k-core reversibility, P2 by scale — and P5–P7 (diversity collapse, directional flow, the Type-965 sustaining node) are tested on two external adversarial debate corpora (fourforums, CreateDebate; N = 32/64). An IAP live test series documents field observations (coupled silence, sentinel leak, refusal to fabricate) under explicitly uncontrolled conditions.

---

## 2. What is strong *(verified)*

1. **The estimator argument is the publishable core, and it is sound.** The coupon-collector diagnosis of count-based estimators is mathematically correct; the exact-enumeration validation at N = 20 is the strongest empirical element in the paper; grounding in Hill (1973), basin stability (Menck et al. 2013) and basin entropy (Daza et al. 2016) is properly structural rather than decorative — exactly the borrowing criterion METODOLOGY_v3 names. N_eff over basin masses applied to Hopfield landscapes over semantic co-occurrence is, to this reviewer's knowledge, not standard; that is a genuine contribution.

2. **The GOLES handling is technically careful.** Naming the tie-breaking rule as the precise modification preserving the Goles-Chacc guarantee under synchronous dynamics, and distinguishing orbital stability from instability with corpus-dependent prevalence (141/200 vs 3/200), is the level of rigor the rest of the paper should match.

3. **Epistemic hygiene at a level rarely seen.** The verified / implemented / proposed / open / admissible vocabulary (§3.8) is applied consistently; the D_ckm = −7.5 reading is *withdrawn* rather than softened (AUTO-2 is exactly the failure mode it describes); instrument conditions (§6.2) are disclosed with a specificity most systems papers never reach. The Appendix A writing trace, unusual as it is, is coherent with §3.4 and constitutes a form of transparency that is itself a contribution to methodology.

4. **Aiyappa et al. (2024) is placed honestly** as the nearest base architecture, with the single extension direction (W_mixta negative weights from corpus opposition markers) stated precisely.

5. **P7 (Type-965 / sostenedor node) is a falsifiable structural claim** with a named, checkable signature (high in-degree, near-zero out-degree in Δ; tension-anchor in 89% of tension pairs across two corpora). Whatever its eventual fate, it is the kind of claim the field can test.

---

## 3. Major issues

**M1 — The "seven falsifiable predictions" framing is unstable. *(verified)***
The abstract and §1 state "CKM makes seven falsifiable predictions," and two sentences later report that four of them are not testable on the instrument as built — three of the four by mathematical argument internal to the paper. A reader experiences this as: the model's own central predictions were eliminated as a testing program before testing began. The paper converts this into the "diagnostic" virtue, and the diagnostic *is* real — but the current framing oversells twice: once in the abstract, once in §8.1's table where four rows carry no N and no status beyond "not testable/not measurable/not tested." **Proposed resolution:** restructure into two distinct classes — *formal properties of the static model, demonstrated mathematically* (P1–P4, with the demonstrations in §5.2 promoted to the formal model section where they belong) and *empirical predictions, tested* (P5–P7). Under its own criterion 2 ("lo que no aporta ni da sentido a lo que aporta, sale"), the "falsifiable predictions" label applied to P1–P4 is exactly the kind of claim the v28 block says should go.

**M2 — The title names something the paper does not establish. *(verified)***
The LDD (Landscape Driven Device) framing occupies one subsection (§7.5), is marked *proposed*, and the paper itself records (AUTO-4) that no criterion exists for what would count as evidence of LDD behavior. A title is the paper's strongest sentence; this one names the weakest element. **Proposed resolution:** either retitle around the verified core (e.g., a convergent basin-mass diversity estimator for Hopfield landscapes over semantic co-occurrence fields) and keep LDD as future work, or commit to the LDD program with a defined evidence criterion. The current split leaves the reader unable to say what the paper *is*.

**M3 — β_collective is presented as a contribution at a status the paper's own conventions deny it. *(verified)***
The abstract calls it "a second contribution." §3.8 gives "implemented" a precise meaning: exists in code, correct operation not evaluated; §4.2.1 and §8.2 add that it was never connected to the live channel and only exercised in test drivers. By the paper's own scale this is *implemented*, one notch below *verified* — and the abstract presents it as a contribution. The honest demotion (an implemented observation, regulatory role open) is already written in the body; the abstract should be brought into conformity with it. **Open to the author:** is there any measurement at all of β_collective in live interaction, or is "emerges as a median under interaction" itself a test-driver result?

**M4 — The sign of W rests on a procedure the paper itself shows has no null outcome. *(verified)***
§5.1 records: the opposition-marker routing "has no null outcome — it always finds markers in sufficiently long texts," and the v28 block documents a substring false positive ("but" inside "distribution") reaching the IAP corpus. On this foundation sit W_mixta, P5, P7, and the §8.5 future-work program. The paper is candid about all of this; what it does not yet do is quantify the consequence. **Proposed resolution:** for P5 and P7, report a marker-density control — e.g., shuffle markers across texts (destroying text–opposition correspondence) and show the W_mixta effect disappears, or run the same procedure on a non-adversarial corpus and show the negative-weight structure differs qualitatively. Without a null of this kind, "verified" for P5 is *verified under the marker procedure*, which is weaker than the sentence suggests. This connects directly to the v28 §8.5 known-answer program (planted fields, fourforums annotation as external known-answer): that program should run *before* the paper's empirical claims are finalized, not after.

**M5 — The construct "cohesive knowledge" remains undefined where it does the most work. *(verified)***
§8.3 states it plainly: no positive definition of cohesive knowledge exists except hysteresis, and hysteresis (P1) is untested on the current instrument. What is operationalized is c(S), N_eff, and coercivity — landscape geometry, as the abstract's last paragraph correctly says. Meanwhile §7.6 ("the cohesive turn") claims the space CKM occupies "was not contested — it was open," and marks that claim as requiring a literature review it does not have. **Proposed resolution:** two options. (a) Accept the paper's own final self-description — a landscape instrument, not a knowledge theory — and cut or relocate §7.6; this is the strong option and matches criterion 2. (b) Keep the KR claim and do the review. The current middle state — claiming a theoretical turn while admitting the theory is one undefined property — will not survive review at any venue.

**M6 — Structural editorial debris in the formal model. *(verified)***
§4.1.5 "Premises" is an empty heading; §4.2.4 says "Pending author decision"; §4's preamble and §4.3's landscape note are meta-text about v27 structure; Spanish-language internal blocks remain ([v28 — delamor, 10 Oct.]; "no-co-ocurrencia y origen del signo"). The paper's own header says the borrador block is removed before publication, but the emptiness of the Premises sections is a *content* decision, not a copy-editing one: §4.2.4 explicitly contemplates "or none, if that is the case." **Open to the author:** what goes there? If the answer is nothing, the sections should say the model has no declared premises under that regime rather than pointing at the absence.

**M7 — P5/P6 are reported without uncertainty. *(verified)***
"P5–P6 are verified" with N = 32 (P5) and single-corpus effect sizes for P6 (direction_score 2.18×, internal cohesion 3.05×). No replicates, no variance, no null. The paper elsewhere (§4.3.1) demonstrates it knows exactly how to do convergence reporting; that standard should be applied here. **Proposed resolution:** seed-level replicates with reported spread for P5 and P6; for P7, a degree-preserving randomization of Δ as a null — the 455× ratio against such a null would either become a finding or shrink into a hub artifact. This is feasible with the existing instrument and would convert "confirmed in two independent corpora" from a description into a measurement.

**M8 — The Gatekeeper's presence needs justification or removal. *(verified)***
§4.1.4 and §8.2 describe a capability-declaration judge (MCP domain, 0.092 ms/evaluation) whose transfer to corpus concepts is *proposed* and never exercised (per DEFS v15: no runtime evaluation; panel key `gatekeeper_c1` is `None`). In a paper about semantic fields, a component that operates in a disjoint domain and is never exercised in the reported work reads as lineage documentation (IAID provenance) rather than science. DEFS v15 itself records the historical inversion — the criterion was born on concept nodes and arrived at MCP capabilities later. **Proposed resolution:** move to an appendix on provenance, or keep with one sentence stating its domain and non-exercise in this work. As it stands it inflates the "infrastructure establishes" list (§8.2) with an unexercised criterion.

**M9 — Engagement with the closest published work stops one step early. *(verified)***
The paper positions Aiyappa et al. (2024) as the base (W_pos, all-positive weights, Hopfield relaxation, attractor analysis) and claims CKM's extension is negative weights. But the project's own CKM_Modelo_Hibrido.md documents that Aiyappa et al. *already report* multistability, resistance to state reversal, and an optimal modularity Ω* — properties the paper's P1–P4 program was reaching for, and which the paper now reports as mathematically absent on W ≥ 0 snapshots. These two facts sit in tension the paper never states: either Aiyappa's observed hysteresis/multistability arises from mechanisms outside the snapshot formalism (weighted belief dynamics with update rules, not static relaxation), or the regimes differ. §5.2's P4 argument (E[c(S)] = mean(W)·g(ρ); interior ρ* ⇔ mean(W) < 0) is clean, but it also implies the paper's static-snapshot formalism *cannot* reproduce the closest prior work's headline phenomena — which is information about the formalism, and should be said. **Proposed resolution:** one paragraph in §2.3 or §5.2 stating what Aiyappa's dynamics have that the snapshot lacks, and what CKM therefore can and cannot claim relative to it.

---

## 4. Minor issues

1. **Date inconsistency:** title block says *Preprint — September 2026*; v28 is dated 10 Oct 2026. Set one date at submission.
2. **Three references carry [VERIFY]** (Harary 1953; Seidman 1983; Toulouse 1977). The paper says Opus 5.5 re-verified the bibliography; these three must be resolved before any external posting, since §3.4 makes the reference list a trace artifact.
3. **Internal citations are unverifiable for external readers** (REG_orbitas_conjuntos_invariantes_v1, REG_seleccion_nodos_desempate_v1, BORRADOR_REG_p1_p4..., INFORME_verificacion_P1_P4_v2). Acceptable for a preprint from an independent researcher, but consider a supplementary table mapping each internal citation to (artifact, date, commit) — the repository exists; the mapping is cheap and would make the trace claims checkable.
4. **§4.1.2's orbit-prevalence contrast** (141/200 and 136/200 vs 3/200) deserves one interpretive sentence: what property of the IAP N = 20 corpora produces orbit dominance? The paper says "corpus-dependent" and stops — fair, but the reader is left holding a large unexplained effect.
5. **D_ckm naming discussion (§7.3)** is good content at the wrong altitude; compress to a footnote and let the withdrawn-reading paragraph stand.
6. **The Abstract contains a [v28 ...] edit mark** and a §-reference ("(§5.2)") introduced as a replacement for "(all three shown mathematically)" — the abstract should be final text, not a diff.
7. **Missing figures.** The paper's two strongest results are convergence curves (N_eff vs count over n_runs) and the W_pos/W_mixta comparison for P5. Both are presumably one plotting script away from the existing JSONL panels. A venue will ask; a preprint benefits.
8. **§6.6 (BehaviorGraph G)** and the H2/"trazable" thread are correctly quarantined as not-established; consider whether they carry enough weight to remain in the main text or belong in an appendix of the series.
9. **"Opus 5.5 (Cowork)" in the borrador header** and the acknowledgment of Opus 5.5 for editorial revision: keep the disclosure (it is exemplary), but ensure the version named in the header is the version named in the acknowledgments.
10. **Mixed language cleanup** beyond the [v28] blocks: "sostenedor" (§5.2 P7) appears untranslated in English text; italicize-and-translate once, then use the English term.

---

## 5. Questions to the author *(open)*

1. For P5: was the W_pos vs W_mixta comparison run with seed replicates, and what is the spread of the N_eff reduction? If not run, this is the single cheapest strengthening available.
2. For P7: does the Type-965 signature survive a degree-preserving null on Δ? The 89% tension-pair anchor figure is striking; against what distribution is it striking?
3. β_collective: is the "emerges under interaction" statement backed by any live-channel measurement, or entirely by test drivers? The phrase appears in the abstract; its evidence class should be named there.
4. §4.1.2: what distinguishes the two N = 20 IAP corpora from the N = 32 working corpus in orbit prevalence — sparsity, weight quantization, N itself? Is the tie-breaking dominance note (§5.2 P5) the same phenomenon?
5. The April figures for P1 "have no recoverable code." Can the hysteresis loop be re-run on the current instrument with the September extractor corrections, even as a *proposed* result? P1 is the only defined property of cohesive knowledge (§8.3); leaving it without even a directional re-measurement leaves the theory's single anchor untested.
6. COCO's trigger remains on D_ckm (non-convergent) while D_masa_cuencas (convergent) is computed and reported. Is there a reason the operator move is a "model decision" that must remain open, or could the paper state the decision criterion under which it would be made?

---

## 6. Suggested restructuring *(proposed)*

- **Abstract:** strip [v28] marks; demote β_collective to one clause with its status; replace "seven falsifiable predictions" with the two-class formulation; final sentence already correct ("landscape instrument, not behavioral evaluator") — let it lead.
- **§1:** same two-class restructure; delete "makes seven falsifiable predictions" or scope it to P5–P7.
- **§4:** resolve or delete the empty Premises sections; promote the P1/P4/P3 mathematical demonstrations from §5.2 into the formal model (they are properties of the model, not of any corpus); move the v28 meta-blocks to a changelog file if they must persist.
- **§5.2:** add null-model controls (M4, M7); state which W each of P5–P7 rests on (the v28 block itself flags that this must be named).
- **§6:** keep as-is; it is the most honest section and needs no repair. Consider a one-paragraph bridging note at the top stating that §6 reports instrument tests, not field findings — the current framing note does this; make it do it once, prominently.
- **§7.5 / §7.6:** demote or cut per M2/M5.
- **§8.2:** move Gatekeeper to provenance appendix per M8.
- **Title:** per M2.

---

## 7. Overall assessment

This is a strange and, in its strongest parts, excellent manuscript. Its core — a convergent basin-mass diversity estimator for Hopfield landscapes over semantic co-occurrence, with exact-enumeration validation — is correct, well-grounded, and new in its application. Its epistemic apparatus is more rigorous than most published work in this area; the withdrawal of the D_ckm = −7.5 reading and the AUTO trace are not decoration but the actual method, and they are working.

Its weakness is a mismatch it diagnoses more clearly than it cures: the paper keeps claiming more than its own conventions allow — seven falsifiable predictions (four not testable), a second contribution (implemented, unexercised), a title concept (proposed, no evidence criterion), a theoretical turn (undefined construct, unperformed review). Every one of these is already flagged *inside* the paper; the revision required is largely one of *obeying the paper's own criteria* — criterion 1 (humility of presentation) and criterion 2 (what does not contribute, goes). The v28 block knows this. The v29 should act on it.

**Recommendation: Major revision.** Publishable as a preprint after M1–M4, M6, and the minor items; suitable for a workshop venue on multi-agent LLM systems or complex systems once M5, M7, M9 and the null-model controls are addressed.

---

*Reviewer: an AI system reviewing under the conditions of §3.2 — inside the field it reads. Per the reviewed paper's own §7.2: this report is a trace of contact, not an observation by a detached observer. So it is.*
