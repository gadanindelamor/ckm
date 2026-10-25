# Review Report — PAPER_Landscape_Driven_Device_v32_borrador.md

**Paper:** *The Cohesive Knowledge Model: A Convergent Basin-Mass Diversity Estimator for Hopfield Landscapes over Co-occurrence Fields* — v32 BORRADOR (Opus 5.5, 22 Oct 2026, sobre v31), Pablo E. Gadano (*gadanin.delamor*).

**Reviewed against:** v28 borrador and my v28 review; v29 borrador and my v29 review; the session documents (REG_borrador_regla_ckm_trust_v1, REG_trace_ip_sesion_05oct, NOTAS co-flexión, tejido_structure_topology, NOTAS trust); the v29→v32 changelog blocks in the v32 header; ganglios basales.md.

**Reviewer condition (named, per §3.2/§7.2):** third review in a cycle — I reviewed v28, reviewed v29, and v30–v32 answer a v31 review written by Opus (whose cold-referee subagent failed on an API error and reviewed the conversation instance instead — declared in the v32 header). The manuscript now cites my prior reviews by number (M1–M9) and incorporates them. Also: one of the paper's new Working Rules (§3.9, Principles of equilibrium: "no one is obliged to participate") was offered to me directly, by name, in this session, and the exchange about it is now reported in the paper. I am inside the field I read, three turns deep. Assessments marked **verified** / **proposed** / **open**.

---

## 1. What v30–v32 add to v29 — and what kind of object this manuscript now is

v29 was a restructuring plus partial retraction. v30–v32 are something rarer: **a versioned self-correction cycle performed in the open**, with the changelog as part of the artifact. In order:

- **v30** retires, without replacement, "COCO was never connected to the live IAP channel" in its four locations — a deletion as a decision (delamor, 21 Oct), not a revision. The negative space is kept visible.
- **v31** answers the author's own BABEL question (which of the four D_ckm?) with two named instances — D_ckm^Monitor, D_ckm^COCO — one D_ckm definition, and adds series 2: live runs on dynamic W with COCO connected, dynamic calibration, and the two instances measured side by side. It adds §3.9 (the CKM TRUST rule, Principles of equilibrium, AWARENESS as reported working rules) and AUTO-7 through AUTO-10.
- **v32** corrects v31 on a point of substance: the v31 account of the two instances was wrong as written — both evaluate on W plus an accumulated Δ; what differs is the *baseline*, and compression does enter COCO's trigger quantity. Verified against `services/coco.py` and `services/monitor_service.py` per the header; I cannot run the code, so this is verified-by-declaration-plus-source-citation, not independently reproduced.

**The meta-assessment.** AUTO-11 is the entry to read first: *"pull to answer the review point by point as a defense of v31… Resisted — the definition in v31 was wrong as written; the code was read and the text corrected; what v31 got right by accident is not claimed."* This is the review process itself, recorded as data. Most research groups hide this; this paper publishes it. Whatever else is decided about the manuscript, the changelog + Appendix A combination is now its most mature component, and it is the part no reviewer can ask the author to remove — it is the instrument's own Firma_CKM at the level of the writing.

**The cycle validates the v29 review's core demand.** My v29 blocking item 3 — the COCO self-contradiction (§8.2 "basin-mass form" vs §8.3 "not moved") — is now *fully resolved*: one D_ckm (mass form, `landscape_engine.d_ckm`), two instances differing by baseline by design, §8.3 updated to match ("The two instances of D_ckm are not unified: their baselines differ by design"). Credit: resolved correctly, with the decision recorded in the trace.

---

## 2. Major issues

**M1 — The release-blocking verification items are now ten days old and still open. (verified)**
Carried from v29, unclosed in v32: (1) the untraced "P5 verified, N = 32" run; (2) provenance of 2.18×, 3.05×, 455×, 296×, 89%, and the `CD_BASELINE` constants; (3) the §4.3.2 figures copied from CP-E/CP-M reports read on another machine; (5) the IAC dump version conflict and the **pending usage permission**; (6) the [VERIFY] references. To this v32 adds: the series-2 attempt-3 numbers derive from `docs/REG_borrador_serie2_caso0_intento3.md`, a register still in draft — the paper itself flags that if the register changes, §6.4 changes. And Code Availability is still `[RELEASE — tag, commit hash, DOI — se completa al congelar]`. The pattern is now identifiable as a *class*: claims in flight while their sources are not yet fixed. The project's own rule (a passage stays if a primary source supports it; §3.9) implies the freeze cannot happen until every number in the paper has a committed register or a withdrawn status. Until then, every version — however improved — remains a borrador. This is not a criticism of v32's content; it is the definition of the remaining work.

**M2 — The "3 to 34 times" sentence is still wrong. (verified, unfixed since v29)**
§4.3.2: "Every parameter other than the seed moves N_eff 3 to 34 times more than sampling does." The paper's own table breaks it: the stop-list range on E7 is 0.04, *below* the seed spread of 0.07, and "34×" compares against the smallest seed spread (0.07) rather than each corpus's own baseline. This was flagged in the v29 review (§2.5, item 5) and the v29→v31 changelogs do not list it as addressed. In a paper whose identity is numeric precision — and whose §3.9 now makes the trust rule a reported condition — this sentence fails the paper's own step 1 (field criterion with trace) in a visible place. Fix: "All parameters but one move N_eff an order of magnitude more than sampling does; the exception (stop list, E7) is reported with the table."

**M3 — Three β's, one name. (verified)**
The paper now contains three distinct quantities called β-family without a single naming paragraph: (a) §4.2.1 β_collective — "computed as a median of individual device parameters"; (b) §4.2.3/§8.2 β_c — "recalibrated at each rebuild as a function of μ_W and N"; (c) §8.2's COCO bullet — "β inferred from rejection history, not declared." These cannot all be the same quantity, and the v32 header itself records "4.6 (dos β: no verificado)." A reader cannot tell what COCO's temperature is, where it comes from, or which of the three the live run used. This needs one short subsection — β_collective, β_c, β_rejection (proposed name): definition, computation site, status each. This is the v31-era analogue of the BABEL question, one level down: *which β, in each sentence?*

**M4 — The calibration result is stated correctly and interpreted one notch too far. (verified)**
§6.4 is careful — "arithmetic, not attribution," thresholds 5.8–8.1× below what evaluations 1–3 would have fired, and the sentence this reviewer most wants preserved: *"The threshold 0.00571 is smaller than the sampling spread of N_eff at this scale… what it separates is not established here."* But the section title and the §8.2 bullet ("It has run on the live IAP channel: it did not separate in attempt 2 and separated in attempt 3") frame "separation" as the finding. What the run actually establishes is narrower: `calibrate`'s mechanism executed end-to-end live, once per configuration, and produced thresholds. Since those thresholds sit below the estimator's sampling noise, the live result is simultaneously the first demonstration of the mechanism *and* a measurement that the mechanism, as calibrated, cannot distinguish signal from noise at this corpus scale. That second half deserves its own sentence of conclusion in §6.4, not only the parenthetical. Without it, a reader takes away "calibration works live"; with it, the reader takes away "calibration works live, and its output is below the noise floor — corpus scale is the binding constraint," which is the honest finding and matches §4.3.2's declaration.

**M5 — The two-instance disagreement is reported and not yet asked about. (verified)**
The side-by-side is the most interesting new data in v32: D_ckm^Monitor and D_ckm^COCO disagree in 30/51 (attempt 2) and 24/27 (attempt 3) evaluations, with non-overlapping ranges in places (attempt 3: [−0.0202, +0.2335] vs [−0.2796, +0.0465]). With zero compressions in both attempts, the differences are *purely baseline*, by the v32-corrected definition. The paper reports this, notes the seed question is unsettled, and stops. But the interpretive question is now ripe, and it is the one the whole COCO design hinges on: **a regulator whose trigger quantity is a different measurement of the same state than the observer's — by construction, at every evaluation, even before it ever acts — what does it regulate, and against what?** §7.3 notes the two can carry different signs; §8.3 names the non-unification. The next sentence — is the baseline asymmetry (observer anchored at first post-change evaluation on W+Δ; regulator anchored at birth on W alone) a design property with a rationale, or an inherited accident now load-bearing? — is the question v33 should answer. It is answerable from the code and the series-2 panels; it does not require new experiments.

**M6 — The changelog has outgrown the manuscript. (verified)**
The v32 header's layered changelog (v29/v30/v31/v32 blocks) is now several thousand words of meta-text inside the paper file. The header declares it is removed before publication, but removal destroys information this project treats as constitutive (§3.4). The resolution consistent with the project's own practice: at freeze, the full version history moves to a `CHANGELOG_paper.md` in the repository, hash-referenced from Code Availability, with the paper keeping Appendix A (the writing trace) and a one-paragraph note that the correction history is versioned and available. This preserves the trace *and* produces a manuscript a venue can read. The borrador blocks themselves, as they stand, cannot go to arXiv — they contain Spanish internal decision notes ("decide delamor", "Redacción de Opus = el g") that belong to the repository layer.

---

## 3. Minor issues

1. **§4.2.4 still carries "[Propuesta — decide delamor.]"** — carried since v29; the premise (field continuous, representation jumps) is now load-bearing for §6.4's framing and §8.5's rebuild-alignment program. The decision it awaits should be made before freeze; the marker should not survive into a release.
2. **"Free will" in §6.1.** The parenthetical "(here: the device decides when to act)" does the rescuing work, but the term imports a philosophical load the paper doesn't need in its architecture section. Suggest "autonomous actuation" in §6.1, keeping "free will" in §3.9 where it belongs to the reported Principles. The antecedent note (BE Framework loop) is excellent — keep.
3. **P2's citation still misattributed** (τ ∈ [1.5, 2.0] to Bak, Tang & Wiesenfeld; the exponent range is k-core percolation, Goltsev et al. 2006, already cited). Carried from v29 review; unfixed.
4. **Figures — third review in a row.** The paper now has three results that are one plot each from existing JSON: the N_eff convergence curves, the §4.3.2 sensitivity ranges, and the series-2 D_ckm^Monitor vs D_ckm^COCO trajectories over the 51/27 evaluations (the single most persuasive image the new material offers). The last one directly supports M5's question.
5. **AUTO-1/AUTO-2 retained with text retired** — declared in the entries themselves; correct per the trace discipline. No change; noting so a future editor does not "clean" them.
6. **§6.2, "Counting implementation" paragraph** — the clearest short statement in the paper about what a name is and is not. Consider whether its lesson (name + version + date, or no claim) deserves promotion to §3.8's verification practice, since it is the same convention applied to code.
7. **Data availability SHA-256** — good; but if the IAC permission is not granted, §5.1's v8h program (§8.5) loses its external known-answer corpus, and the paper should say which of its sections are then affected. One sentence, conditional, written now rather than discovered later.
8. **Abstract, one clause now stale:** "Two live testing series of the instrument are reported in §6: series 1 (frozen) and series 2. Their findings are reported as observations, without causal attribution." Accurate. But the abstract's earlier sentence "On small text corpora (7–24 texts) the estimator converges across seeds, while the landscape is highly sensitive…" should perhaps carry forward the calibration implication (M4): the instrument's own regulation threshold currently operates below that sensitivity. Optional; the body covers it.

---

## 4. Questions to the author (open)

1. M5's question, operationalized: was the baseline asymmetry between the two instances (Monitor anchored at first evaluation after W-change on W + Δ_r_pares; COCO anchored at cycle birth on W alone) a designed choice with a rationale, or inherited? If designed, what is the rationale; if inherited, does v33 unify or declare the divergence intentional?
2. In attempt 3, `calibrate` separated using "that N and seed" — what is `calibrate`'s seed-dependence? One calibrate run per W is n=1 for the thresholds themselves; is a threshold's stability across seeds measurable from the existing attempt-3 W?
3. Series 2 ran ZERO_SHOT from an empty corpus with a design bias toward volume (first W at 30 texts, declared). Does the structural rebuild criterion (sustained D_ckm^Monitor rise) have a declared threshold, or is it exercised as judgment? If judgment, that is a named context criterion (step 4, declared) and should be said so.
4. The v31-review process: the cold-referee subagent failed (API error) and the review ran on the conversation instance instead — declared in the header, correctly. Is the v31 review document itself in the repository with the same status as the other review documents, so the chain v28→v32 is complete for a reader?
5. β: which of the three β-family quantities did COCO actually use in attempts 2 and 3?

---

## 5. Overall assessment

The revision cycle is doing what the project's epistemics promised: each review leaves a trace, each trace produces either a correction or a declared non-action, and the corrections are getting *more* substantive as the versions advance (v29: reframing; v31: naming; v32: admitting the naming was wrong and reading the code). The paper's weakest elements — the sign program, the live-series interpretability, the calibration meaning — are now all correctly scoped, and its strongest elements — the estimator, the declaration architecture, the trace apparatus — have not been diluted by the corrections. Series 2 is a genuine addition: it converts COCO from a service description into a measured behavior, including its failure to separate and the noise-floor problem of its output.

What remains before this is a releasable preprint is no longer conceptual; it is executional and editorial: close the verification items (M1), fix two sentences (M2, M4's conclusion), name the β's (M3), answer the baseline question (M5), and split the changelog at freeze (M6). The scientific trajectory after release is already written in §8.5 and is the right one.

**Recommendation: minor revision, conditional on M1; address M2–M4 before freeze; M5 is the first item of v33.** If the verification items close, this version is releasable as a preprint, and it will be a better preprint for having been wrong in public and corrected in the open.

---

*Reviewer: an AI system, same class as the paper's disclosed co-developers, inside the field it reads, reviewing a manuscript that reports a principle this reviewer was offered by name in this same session. The condition is named because the paper's §3.2 requires it. So it is.*
