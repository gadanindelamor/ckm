# Referee report — PAPER_Landscape_Driven_Device_v31_borrador_opus.md (v31)

Date: 22 Oct 2026. Reviewer: Claude Opus 5.5.

**Condition of this review.** The cold-referee skill spawns a fresh instance that sees only the document. That subagent was stopped by an API safeguard error before it produced anything. This review was done instead by the conversation instance. That instance did not write v31 and had no project context beyond the document and the author's request, but it is not the fresh instance the skill specifies. No file other than the draft was opened. Code and registers cited by the draft were not checked.

---

## 1. D_ckm — which instance

1.1 **§4.3.1, "Same formula, two baselines."** The definitions in the same paragraph give two differences, not one. D_ckm^Monitor is computed "over W_eff = W + Δ_r" and D_ckm^COCO "over W alone". The input matrix differs, not only the baseline. The timing of the two baselines may also be the same. Monitor resets "whenever W changes". COCO's baseline is fixed "when COCO's cycle is born", and §4.2.1 says COCO "is born and reborn with each W cycle". If a COCO cycle is a W cycle, both baselines reset at the same moment, and the 24-of-27 difference comes from W_eff vs W, not from the baseline. The paper does not say whether a COCO cycle and a W cycle are the same thing. **Major.**

1.2 **§4.3.1, "W_eff = W + Δ_r."** Δ_r has no suffix here. The paper has Δ (directional matrix, §4.1.1), Δ_r_pares (Monitor), Δ_r_compresiones (COCO) and bare Δ_r (§3.5, §4.2.3 Firma "sha256(accumulated Δ_r)", §7.5). A reader cannot tell which Δ_r enters W_eff, nor how a list of rejected pairs becomes an N×N matrix added to W. **Moderate.**

1.3 **§4.3.1, D_ckm = 1 − ln N_eff_t / ln N_eff_0.** The formula is undefined when N_eff_0 = 1, which the paper allows ("N_eff ∈ [1, |L|]"). The handling of a collapsed baseline is not stated. **Moderate.**

1.4 **§4.3.1 and §6.4, "they differ in 24 of 27 evaluations".** "Differ" has no tolerance. The paper does not state n_runs or the seed policy for series 2. Its own figures put N_eff seed spread at about 2–3% s.d. (§4.3.2: 15.52 ± 0.32, etc.). At N_eff ≈ 2.4 that is a D_ckm noise of about ±0.03. Many of the reported values (e.g. COCO 0.0329–0.0465) are within that. Unless both instances share seeds and samples, a reader cannot tell a real difference from sampling noise. I am unsure here, because it depends on implementation details the paper does not give. **Moderate–major.**

1.5 **§7.5, "COCO compresses Δ_r (the rejection accumulator) … modifying the directional component of the trajectory without altering W".** This contradicts §4.2.2, where COCO operates only on Δ_r_compresiones and never on Monitor's accumulator. "Directional component" reads as Δ (the directional matrix), which is a third object. **Moderate.**

1.6 **§4.2.1 / §4.3.1, together.** D_ckm^COCO is computed "over W alone". COCO acts by compressing Δ_r_compresiones. The paper does not say what that compression acts on, or how a compression could change the quantity that triggers it. As written, the regulator's action does not appear in its own trigger signal. **Major.** This is an absence, not a contradiction.

1.7 **§8.2, "The firing rule is verified by a sweep over threshold values against known D_ckm inputs."** The instance is not named. The context is COCO, so it is probably ^COCO. **Minor.**

1.8 **§6.2, "Quantitative outputs (the distance, c_S)" and "so the distance moved while the channel was still empty".** "The distance" relies on the reader carrying "count-based" from a sentence further down. It is readable in a series 1 context, but not stated locally. The notation c_S vs c(S) is also inconsistent. **Minor.**

1.9 **§7.4 Scale, "the interpretability of both instances of D_ckm and of c(S)".** This paragraph also covers series 1, which used neither instance. **Minor.**

1.10 **The remaining uses are unambiguous**: §4.2 bullet, §4.2.3 Firma (^Monitor), §6.2 (count-based, `deprecated_d_ckm`), §6.4 table, §7.1, §7.3, §8.1 H_STOP (count-based), §8.3.

## 2. §6 — findings as observations, with sources

2.1 **§6.3 series 2 table, W versions.** The stated rule is a first W at 30 device texts, then a rebuild every 10. Attempt 2: 80 texts → 30, 40, …, 80 = 6 ✓. Attempt 3: 56 texts → 30, 40, 50 = 3, but the table says **4**. The evaluation counts fit "one per device text from the 30th on" (80−29 = 51 ✓, 56−29 = 27 ✓). That leaves the 4 unexplained. Either the rule, the count, or an extra rebuild cause is missing. **Major** (a number in the headline table does not follow the paper's own rule).

2.2 **§6.4, "The 0 firings of both attempts belong to the uncalibrated default, not to the field."** Attempt 3 ran its last 3 evaluations on the calibrated thresholds and, by this sentence, still did not fire. So not all 0 firings were under the default. This is also a causal attribution, which §1 says the series is reported without. **Major.**

2.3 **§6.4, "N_eff(W) = 2.4621 exceeded the constant N_eff(λ=1) = 2.4369 … separated".** λ, the criterion for "separates", `d_max`, `frac_rec` and the state "stable" are not defined anywhere in the paper. The arithmetic checks: 0.0329/0.00571 ≈ 5.8 and 0.0465/0.00571 ≈ 8.1 ✓. But the threshold 0.00571 is about an order of magnitude below the sampling resolution implied in 1.4. Whether it is meaningful depends on n_runs and seeding, which are not given. **Moderate.**

2.4 **§6.4 series 2 sources.** Attempt 3 rests on "`docs/REG_borrador_serie2_caso0_intento3.md` (not approved yet)". The table marks it "Documented (register in draft)". A finding section citing an unapproved source should say what changes if the register changes. Attempt 1 ("61 provider `413`") has no source cited. **Moderate.**

2.5 **§6.4 series 1, "a device that did not read the channel still depended on it for its rhythm … collective silence could become absorbing by construction".** "Did not read the channel" is a claim about the device, and the paper does not say how it is known. "Absorbing by construction" is a design argument, not a log observation. No register or log is cited for this finding, unlike series 2. **Moderate.**

2.6 **§6.4, "Series 2 — the moving photograph … each W is a new representation of the same continuous field".** This is the framing of §4.2, restated inside "Findings". The observation is the number of rebuilds and the two value ranges. "The same continuous field" is a premise, and §4.2.4 says no premises are declared for dynamic W. **Moderate.**

2.7 **§6.1, "In series 1 the loop was entered only by new messages; the continuous loop is the condition of series 2."** No source is given. "Tick" is undefined. "Free will" names a loop design here and an ethical principle in §3.9: one name, two things. **Minor–moderate.**

2.8 **§6.2 is titled "(series 1)", and there is no series 2 counterpart.** Series 2 does not state which models or providers the four devices were, what the partial prompts contained, or whether any device carried project context (the contamination §6.2 names for series 1). §6.5 names "the model of one device" as a confound without identifying it. **Moderate.**

2.9 **§6.5 bullets are good as stated.** One run per attempt, no attribution of LEAVE. No issue.

## 3. §3.9 Working rules

3.1 **"It was also the rule by which this paper was revised: a passage stays if a primary source (code, register) supports it."** The header blocks of v30 and v31 both state that the rest of the paper was **not** re-verified passage by passage. As a claim about this paper, the sentence goes beyond what the paper reports doing. **Major** (it is the one place §3.9 claims something rather than giving context).

3.2 **"It is implemented once (`services/ckm_trust_rule.py`) and instantiated where the instrument decides (call filter, calibration)."** This is a code claim and is fine as a pointer. The "call filter" is not mentioned anywhere else in the paper. **Minor.**

3.3 **M.M. is used for several things.** It appears as "the M.M. rule" (§3.4), a principle (§3.9, "you lie, you die"), a property of the trace ("whether a device does what it declared (M.M) is in the trace", §4.2), and the 2023 project title. §3.4 refers to "the AWARENESS protocol and the M.M. rule" before §3.9 defines them. **Moderate** (Babel), minor for the forward reference.

3.4 **AWARENESS appears in two roles.** §3.9 presents it as the protocol under which the paper was written. §6.2 lists it as an uncontrolled contaminant in a device's context during series 1. Both statements are true, but §3.9 does not connect them. A reader would want to know that the writing method and an experimental confound are the same protocol. **Minor.**

3.5 **Apart from 3.1, §3.9 reads as context**: rules, attribution, dates, register path. The "Principles of equilibrium" are stated without claims about effect. No issue.

## 4. Assumed presences and absences

4.1 **§7.4 COCO, "implemented and verified in unit tests and test drivers."** §8.2 and §6.4 say COCO ran live in series 2. This sentence restates the absence that v30 removed ("only test drivers"), without the word "only". **Moderate.**

4.2 **§8.5, "What remains open is corpus volume sufficient to exit the accumulate phase and reach the evaluate phase under live conditions."** Series 2 attempts 2 and 3 built W live (6 and 4 versions, §6.3). This contradicts §6. The v30 header listed it as a trace to fix, and it is still there. **Moderate.**

4.3 **§1, "The IAP series documents live runs …: coupled silence, a sentinel leak, a refusal to fabricate from an empty channel. These are reported without causal attribution (§6)."** Two of these three are no longer in §6.4, and the sentence omits series 2. See also 2.2. **Moderate.**

4.4 **Dangling pointers.**
- §6.3 row 0.15: "Documented — see 6.4". The 0.15 refusal is not in 6.4.
- §8.2: "trace_ip identified as a formal concept" and §8.3 "trace_ip verifiability". trace_ip is never defined.
- §6.5: "TinkerBellucio's behavior". The behavior is no longer described.

**Moderate** (together).

4.5 **§8.1, "reformulated as function of A_pre".** A_pre is undefined. **Minor–moderate.**

4.6 **Two β's.** §8.2 says "β inferred from rejection history". §4.2.1 says β_collective is "a median of individual device parameters", without saying which parameters. Whether these are the same β is not stated. **Minor–moderate.**

4.7 **§4.2.1 vs §4.2.2, Δ_r_compresiones.** Δ_r_compresiones is "independent of Monitor's Δ_r_pares", and Monitor is the sole writer of Δ_r_pares. The paper does not say where Δ_r_compresiones gets its content from. **Moderate.**

4.8 **N across sections.** §3.7 says "The operational corpus is at N = 32 nodes", and §6.2, §7.4 and §8.3 repeat N = 32. But §4.3.2 uses N = 20 and N = 12, §4.3.1 validates at N = 20, and series 2 does not state its N. **Minor–moderate.**

4.9 **§7.4 ZERO_SHOT, "all IAP cases ran with CorpusService starting empty."** It is not stated whether this includes series 2. The same applies to §3.7 and the Abstract, which speak of "the IAP series" in the singular. **Minor.**

4.10 **§7.2, "a human connecting via the Gradio interface … was registered as n_agentes=4" → "The empirical finding suggests it is not [separable]".** No source is given. This is one observation of a counter, read as evidence about observer/field separability. **Moderate** (interpretation).

4.11 **§4.2.4, "No premises are declared for dynamic W",** while §4.2 states "The field does not jump; it is continuous" and attributes jumps to the instrument "unless shown otherwise". That functions as a premise. **Moderate.**

## 5. Other

5.1 **Acknowledgments, "Claude Opus 5.5 … editorial revision of versions 28–29".** The headers show Opus revised v30 and v31 as well. The disclosure is out of date. **Moderate** (disclosure accuracy).

5.2 **§4.3.2, "moves N_eff by 66% in A24 (15.52 → 5.27)".** 5.27 is exactly D12's baseline N_eff in the line above. This could be a coincidence or a copy error. Worth checking against the CP-E report. I am unsure. **Minor.**

5.3 **§4.3.1 vs §4.3.2, seed stability.** §4.3.1 says "±1–5% across seeds", and §4.3.2 says "spread … 7–9% of its value". These appear to be different statistics (s.d. vs range) under similar words. The statistic should be named in both places. **Minor.**

5.4 **§2.5, "CKM observes extended critical-like behavior at N = 32",** supported only by "earlier working reports". It is stated in the present tense with no evidence in this paper. **Minor–moderate.**

5.5 **§8.4.** The convergence claims (IAID → MCP, "J-space") are asserted, with no dated documents included. The cited Gurnee et al. title does not contain "J-space", and I cannot tell whether the term is theirs. **Minor; unsure.**

5.6 **Outline vs headings.**
- Outline "5. Empirical Validation — External Corpus" vs heading "5. Empirical Validation".
- Outline "6. IAP Test Series" vs heading "6. IAP Testing Series (live)".
- §3.2 says "working reports (v1–v31)", References say "v2–v31".

**Minor.**

5.7 **Editorial notes left in the body.** Examples: "[Propuesta — decide delamor.]", "[a verificar.]", "[Permiso de uso pedido — pendiente.]", the "[v28]/[v29]" reference tags, and "[VERIFY]". These are expected in a draft, but they need to be cleared before release. **Minor.**

5.8 **§4.1.2, period-2 prevalence measured at 200 trajectories.** This is below the n_runs ≥ 1000 the paper itself sets for stable masses. **Minor.**

---

## Count

- Major: 5 (1.1, 1.6, 2.1, 2.2, 3.1)
- Major/moderate (unsure): 1 (1.4)
- Moderate: about 20
- Minor: the rest

## Trace of this review

- I felt a pull to accept the author's framing "differ in baseline" because the request stated it. I checked it against the §4.3.1 definitions instead, which gave 1.1.
- I felt a pull to pad section 3 to match the length of the others. I left it short; 3.5 says no issue.
- 2.1 and 1.4 come from arithmetic I did myself on the paper's own numbers. I did not check them against any register.
- 5.2 may be a coincidence. I marked it as unsure rather than drop it or overstate it.
