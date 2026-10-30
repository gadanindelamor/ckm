# Review frío — PAPER_Landscape_Driven_Device_v34_print_opus.md — 30 oct 2026

*Hecho por una instancia nueva (general-purpose, el mismo modelo) que recibió sólo la ruta del `_print` y el prompt de la skill `cold-referee`. Desvío de la skill, declarado: el primer intento se cortó porque los filtros de seguridad marcaron el pedido (`reasoning_extraction`). El segundo intento cambió la traza de la revisión por "marcá los ítems que salieron sólo porque se esperaba una lista" y llevó algunas preguntas abiertas menos. El informe sigue tal como volvió; sólo se pasaron a caracteres los `&gt;`, `&lt;` y `&amp;` que llegaron escapados.*

---

The paper's strongest result holds up: the convergence claim and the margin arithmetic check out when recomputed. But the formal claim that the bound reproduces F(N) is wrong as stated. §4.3.2 and §5.2 give incompatible numbers for the same corpora. Several summaries were not updated after attempt 5. The central terms (field, CKM, α, declared, calibrate) each name more than one thing.

**A1, the basis of this review.** I read only the document and opened no other file. Two kinds of item are mine: arithmetic I recomputed (marked "checked"), and points about outside literature that come from my background knowledge (marked "background"). Anything that depends on the cited registers or code I could not see is marked "unverified".

## 1. One name for more than one thing (Babel)

1. **"field", throughout. Major.** It names three things:
   - something outside the instrument: "the field is continuous; what jumps is its measurement" (§4.2, §4.2.4);
   - W or W_eff, the instrument's own object: "the field's relaxation rejects" (§8.2); Δ_r "persists as deformation of W_eff — the field metabolizes them" (§4.2.2); "the field decides" (TRUST rule, §3.9);
   - the channel of live interaction (§6).

   §4.2.1 says COCO "regulates its own representation of the field, not the field". §4.2.2 then calls a change to W_eff the field metabolizing. The paper's one declared premise (§4.2.4) depends on keeping these apart, and the text does not.

2. **"CKM" / "the instrument". Moderate.** §4.1.6 says "CKM does not extract nodes and does not tokenize". Yet §4.2 and §4.2.3 list CorpusService and NodeExtractorService ("It decides which nodes exist") as components of the instrument. §7.6 then calls CKM "a knowledge representation in the classical sense". The paper's stated condition, that the producer is separate from the instrument, needs this boundary drawn in one place.

3. **"α". Moderate.** It means the compression factor, α ∈ [0.05, 0.30] (§4.2.1, §7.5, §8.2), and also the mass of self-conjugate orbits (§4.3.1). In §6.4, attempt 5, "α = 0.199" stands next to the COCO thresholds and falls inside the compression range, so a reader cannot tell which is meant.

4. **"declared" / "declaration". Moderate.** It covers:
   - the author's statement of a procedure (§4.1.6);
   - nodes a text has as present ("declared pair", "σ_prompt declared active", §4.2.2);
   - the threshold provenance label `DECLARED` (§4.2.1);
   - a device's declared goal (§7.5) and declared capabilities (§4.1.4);
   - "declared defaults" (§7.4).

   "Declared active" also reads presence of a token as an act by the text.

5. **"COCO". Moderate.** It names an implemented service (§4.2.1), "two COCO instances" in series 1 (§6), and an unimplemented concept, "COCO as collective consciousness" (§3.6, §8.3). §7.4 places both under one heading.

6. **"D_ckm", how many instances. Moderate.** §4.3.1 and §8.2 say three (calibrate, Monitor, COCO). §7.4 says "both instances of D_ckm"; §8.3 says "the two instances of D_ckm are not unified". §6.2 also uses "the distance" for the retired count-based quantity.

7. **"calibrate" / "separate". Moderate.**
   - §6.4 shows that separating is equivalent to N_eff(W) > F(N), where F(N) is a constant for each N (≈2.61 at N = 20). Each threshold is half the margin (checked: 0.011418/2 = 0.00571; 0.506/2 = 0.253).
   - "Calibration" therefore compares N_eff_0 with a constant that does not depend on W, not with an external standard.
   - The paper also says "what the thresholds separate is not established" (§6.4) and lists "a definition of separation, if one is registered" as future work (§8.5).
   - Even so, §8.1 reports separation counts as a measurement, and §8.2 says "whether it calibrates is itself verified".

8. **"converges". Moderate.** It is used for two different things:
   - shrinkage of the error as n_runs grows (§4.3.1);
   - spread across seeds at one fixed n_runs ("the estimator converges", §4.3.2 and the abstract, from an 8–12% seed range at n_runs = 1000). That is precision at one budget, not convergence.

9. **"N_eff_0". Minor.** It is the Monitor baseline, the COCO baseline, N_eff at λ = 0 for calibrate (§6.4, "exact N_eff_0"), and the value in case 09 (§4.3.1).

10. **"Δ_r". Minor.** §3.5 uses it as one quantity. §4.2.2 splits it into `Δ_r_pares`, `Δ_r_compresiones` and `Δ_r_torsion`. Firma's "sha256(accumulated Δ_r)" (§4.2.3) and "Σ Δ_r = 0" (§6.4) do not say which one.

11. **W_eff and W_Monitor. Minor.** Both are defined as W + `Δ_r_pares` (§4.2.2, §4.3.1), so one object has two names.

12. **M.M. and "Free will". Minor.** Both are used in two senses, but §3.9 says so. I list them only for completeness.

## 2. Claims without support, or beyond what the source can say

13. **§4.3.1: "The collapsed landscape is the equality case… and the bound reproduces F(N) to 10⁻¹⁵". Major (checked).**
    - The equality case of the bound needs one self-conjugate orbit of mass α.
    - The F(N) formula in §6.4 spreads α over C(N, N/2)/2 orbits, so the term is 2α²/C, not α².
    - At N = 20, α = 0.125, the bound gives 2.5098 while F(20) = 2.6122.
    - The bound itself (Σm² ≤ α² + (1 − α)²/2, so N_eff ≥ 2 for α ≤ 2/3) checks out. The sentence linking it to F(N) does not.
    - Either the sentence refers to a different, refined bound that is not written down, or it is wrong. §8.1 lists this row as "Proved; bound tight".

14. **The conjugation-invariance step in §4.3.1. Minor (unsure).** "P(a) = P(N − a) because the band [0.3, 0.7] is symmetric" holds only if turning the drawn fraction into an integer count of active nodes is symmetric too. That rounding rule is not stated; floor rounding would break the symmetry.

15. **§4.1.2: the tie rule versus float64. Moderate (unsure).** The paper says the code flips instead of retaining in 13–22% of states. It does not say whether Goles's guarantee (no cycles of period > 2) still holds for the step that actually runs, where rounding acts like a state-dependent threshold. The evidence offered is 500 states per W against `relax_orbit`. Every "exact" value in §6.4 is exact for the float map, not for the declared map.

16. **§4.1.1 / §2.3: "Mixing them destroys attractor geometry". Moderate.** The only evidence is one Hebbian pattern-recovery experiment (N = 16, Working Report v11). §2.3 itself says CKM does not use Hebbian storage, so the result is carried into a regime the paper says it does not apply to.

17. **§2.5: "CKM observes extended critical-like behavior at N = 32". Moderate.** The paper states it as an observation and gives no data, saying it is "not re-examined in this version". By §3.4's own rule, a claim without a trace in the text is not made, so it should be withdrawn or marked.

18. **§3.3: "The strongest verification in this work is retroactive convergence with independent findings" (Hill 1973; Thirumalaiswamy 2025). Moderate.** Hill supplies the definition the paper adopts, and §7.5 calls Thirumalaiswamy a "structural analogy". Neither is verification. This also contradicts §4.3.1, where the verification is exact enumeration.

19. **"Cluster frontier coercivity" (§7.1, §7.4, §7.5). Moderate.** It is presented as one of the quantities CKM measures, but it is never defined, computed or reported anywhere in §4–§6. The same goes for "c(S) gradients" (§7.5).

20. **Hysteresis (§7.4, §8.3, §4.1.5, §8.1, §8.5). Moderate.**
    - §7.4 calls it "the only fully defined property of cohesive knowledge", but the paper never gives the definition; the loop statistic is mentioned, not defined.
    - §4.1.5 says F1 makes hysteresis "not testable on a non-negative snapshot".
    - §8.5 says "F1 closes hysteresis on a snapshot".
    - §8.1 marks F1 "Verified".
    - What was measured (m_down ≡ 1.0 in three runs) is a degeneracy, not a property of the landscape.

21. **F3 (§4.1.5). Minor to moderate.** "Re-adding a node recovers in reverse order… equal round counts" does not follow from k-core uniqueness; uniqueness gives the final set, not the order or the number of rounds. No measurement is reported, yet the abstract and §8.1 count F3 among the "verified" formulations.

22. **F4 (§4.1.5). Minor (checked algebraically).** For W ≥ 0, ρ = 0 gives the same E[c(S)] as ρ = 1, so "ρ* = 1" omits ρ = 0. For mean(W) < 0 the optimum is always ρ = 1/2, so the "optimal density" depends only on the sign of mean(W). That is worth stating as a limit on what F4 says.

23. **§4.1.3: "The field can sustain states with high c(S) that destroy existing attractors." Minor.** No support is given, and "destroy" is not defined for a fixed W.

24. **§4.3.1: "N_eff = |L| is perfect equidistribution, unreachable under real W." Minor.** §4.3.1's own parity paragraph shows that for odd N the collapsed landscape has two basins of mass 1/2, so N_eff = |L| = 2. That is a counterexample unless the collapsed W is excluded from "real W", which the text does not say.

25. **§2.3: the mapping to Aiyappa et al. Moderate.** "the corresponding properties of CKM are decided by the snapshot (§4.1.5)" pairs multistability, resistance to reversal and optimal modularity with F1, F3 and F4 without saying which corresponds to which. F4 is about density, not modularity. I cannot check from memory whether Aiyappa et al.'s networks are "all-positive"; that characterization should be checked against the source.

26. **§2.5: Beggs & Plenz (2003) cited for "extended criticality". Minor (background).** As I recall, that paper reports critical avalanches, not an extended critical region; Moretti & Muñoz fits the claim. I am fairly confident, not certain.

27. **§7.6: "The persistent assumption across these traditions: knowledge is propositional, and its representation is static. Smith [1985] made this explicit." Moderate (background).**
    - Belief revision (AGM, 1985) and truth-maintenance systems are KR traditions built around representations that change.
    - Smith's knowledge representation hypothesis is about propositional ingredients with a causal role; it does not assert that representation is static.
    - AUTO-14 says a related claim was withheld until the literature is reviewed, yet this broader one stays in.

28. **§7.6: "Representing knowledge and measuring the field are, in this work, two perspectives on the same thing." Moderate.** No argument is given, and it conflicts with the abstract's "does not interpret meaning".

29. **§7.2 and §6.1: "Observation itself creates presence… The instrument measures traces of contact, not observations by a detached observer." Moderate.** The evidence is that a connection counter counted a connection (n_agentes = 4), which is how the counter was designed. The text concedes "one observation of a counter does not settle that" and then draws the conclusion anyway.

30. **§8.4: convergences by independence. Moderate.**
    - "Agents Are Not Tools" (2025) is cited but missing from the references.
    - MCP has no reference.
    - "IAID → MCP… verifiable from dated working documents" points to documents the reader does not have.
    - "J-space" does not appear in the title of the Gurnee et al. reference and is never defined.

31. **§8.3: "an open loop of area 0.000862… with time as an axis is a helix". Minor.** This is an interpretive figure that rests on a register the reader does not have.

32. **§8.5, text unit: "The quantity that orders landscape collapse is the saturation of distinct pairs… rather than density or tension". Minor.** It is marked "verified as measurement", but no measurement appears in the paper, and "tension" is undefined (also "tension threshold" in §5.1).

33. **Internal registers as the only support. Moderate.** Many "[Verified: REG_…]" tags point to files outside the paper, and none appears in the references. Code Availability names a release "that freezes this version" but gives no tag, commit or DOI, so the reader cannot locate what the claims rest on.

## 3. Absences

34. **No baseline beyond the raw count. Major (background).** The case for N_eff is that raw orbit counts grow with sampling. Estimating richness from samples with unseen classes is a known problem with known bias-corrected estimators (Chao1, Good–Turing coverage). The paper compares against the uncorrected count only, which is the weakest baseline. Separately, consistency of a plug-in Simpson estimator for a finite distribution is standard, so the contribution needs to be placed against that literature (Daza 2016 is cited; species-richness estimators are not).

35. **Convergence depends on the basin count, and the abstract does not say so. Moderate.** The plug-in converges only when n_runs is large relative to the number of basins that carry mass. §5.2 shows the failure (N = 146, no orbit reached twice), but the abstract and §8.1 state convergence without the condition.

36. **The headline enumeration uses the uniform measure; the instrument uses the reference measure. Moderate.**
    - §4.3.1 says the exact enumeration was under the uniform measure, not the instrument's reference measure, and §4.1.5 shows the two differ by 11.4%.
    - The abstract does not mention this.
    - The paper does not say which measure the 100,000 comparison samples were drawn from. If it was the reference measure, the comparison is not like for like.

37. **The validation table is one run per regime. Moderate.** There are three corpora, one per regime, and no seeds or repetitions are stated. The abstract's "at most 0.6%" generalizes from those three runs. The three IAP corpora are also not identified (no W hash, no case).

38. **§4.3.2 and §5.2 give different numbers for the same corpus names. Major (checked).**
    - §4.3.2 (current extraction): A24 4.88, D12 3.06, E7 4.79.
    - §5.2: A24 W_mixta 15.65, D12 5.26, E7 10.07.
    - §5.2 says D12's real marking "reaches 119 of 235 pairs", but D12 has N = 19 in §4.3.2, which allows at most 171 pairs.
    - So §5.2 used a different extraction, N or measure, and states none of them. The null result on the sign, which the abstract leads with, therefore lacks its declared producer.

39. **Permutation null size. Moderate (checked).** With k = 2 marked texts out of 12 (D12) there are only 66 distinct markings; with k = 1 out of 7 (E7), only 7. The text says "200 permutations" in one place and "120 random markings" in another. The smallest attainable p-values (1/66, 1/7) and the test's power are not reported, although §8.5 lists exact permutation as future work. "Not supported" stands as wording, but a reader should be told the test could barely have detected an effect.

40. **§5.2: "Pairs do not explain the result either: correlation −0.50 in A24". Minor to moderate.** A correlation of −0.50 is not nothing. "Do not explain" interprets a moderate correlation from one corpus.

41. **The fourforums W producer (v8i–v8n) is not given in the paper. Moderate.**
    - Missing: how votes become signs, the thresholds, how 304 labelled authors became N = 146, the symmetrization, and the number of permutations behind p = 0.027.
    - The normal one-tailed p for z = −2.06 is about 0.020, so the 0.027 presumably comes from permutations.
    - §1 says the producer "is declared with every claim"; here it is only pointed at a register.

42. **The sign producer's inputs. Moderate.** The 44 opposition markers and the 112 project-specific stop words are not listed, and the sign is the input the paper calls weakest. The source texts of A24 are not described (D12 and E7 get one phrase each).

43. **The Δ_r_pares update rule. Moderate.** The size and sign of the increment per expelled pair are not given, yet D_ckm^Monitor and W_eff depend on it.

44. **"Jump" in calibrate. Moderate.** §6.4 sets thresholds "at the midpoint of the jump" and reports "d_max", but separation is decided from the two ends. In attempt 3 the curve's interior maxima (0.176, 0.231) are far larger than the margin (0.011). How "jump" relates to "margin" is not defined.

45. **Coordination. Moderate.** §1 motivates CKM as telling "genuine coordination" from "parallel activity". No section connects any CKM quantity to that distinction or tests it, and no named absence points to it.

46. **F2. Minor.** Formulations are numbered F1, F3, F4. F2 is never mentioned or accounted for.

47. **The F1–F4 results cover non-negative W only. Minor to moderate.** The measured corpora carry negative weights (A24 has 33% marked texts). The paper does not say what, if anything, F1–F4 imply for those W.

48. **Selective repetition of stability figures. Minor.** §6.2 and §7.4 repeat the most favourable figure (±1–5%, three seeds, one corpus), while §4.3.2's 10-seed range of 8–12% is not repeated there.

49. **One named absence among similar ones. Minor.** §6.4 names one missing check: "Whether the two instances share sampling seeds is not established". Two of the same kind go unnamed:
    - With no compression, W_COCO = W_Monitor. The 24 of 27 differences in attempt 3 then come from the baseline and possibly the seed, not the landscape.
    - In attempt 5, D_ckm^Monitor = 0 throughout follows by construction once Σ Δ_r = 0 and the same seed is used. It is not a measurement.

## 4. Interpretation where only observation is warranted

50. **§7.5: "OPERADOR_STOP_COCO… is one instance of this mechanism" (LDD). Moderate.** LDD is about a device's trajectory being shaped by field geometry. COCO compresses its own representation, and §4.2.3 says β "do[es] not act on any quantity". Nothing in the text links the compression to any device's behaviour, so it is not an instance of the device mechanism as defined.

51. **§6.2: "They are genuine devices"; §4.2.3: Monitor is an "impartial observer"; §8.2: Firma "certifies". Minor.** These are evaluative labels. "Certifies" also conflicts with §4.2.3, which says Firma "does not produce the trace; it makes the existing trace legible".

52. **§6.2: series 1 observations "stand in their own frame". Minor to moderate.** Jaccard co-activation and presence detection depend on corpus construction that §6.2 itself lists as flawed (SYSTEM messages as nodes, W rebuilt per text). The claim that they are unaffected is asserted, not argued.

53. **§8.1: H_STOP "was reformulated in terms of the attractor count". Moderate.** The paper rejects counts as non-convergent (§4.3.1) and then reformulates its one falsified hypothesis in terms of a count. H_STOP and STOP are not introduced anywhere else.

## 5. Contradictions and dangling references

54. **Attempt 5 is only partly integrated. Moderate.**
    - §6's header says series 2 is "attempts 1–4, 20–27 October".
    - The §6.3 table has no attempt 5 and no date for it.
    - §6.5 ("For series 2…") does not cover it.
    - §8.2 says calibrate ran "in attempts 2–4… the one separation registered (attempt 3) lies within the noise", while §6.4 and §8.1 report an exact separation in attempt 5 (+0.4915).
    - §4.2.2's "four live runs of series 2… 154 Monitor evaluations": 154 equals 51 + 27 + 65 + 11, the COCO evaluation counts of attempts 2–5 (checked). So it is unclear which four runs are meant and whether these are Monitor or COCO evaluations.

55. **Attempt 2: "6 W versions" (§6.3) but "four rebuilds" calibrated (§6.4). Minor (unsure).** Six versions is the first W plus five rebuilds; the total of 14 calibrated W adds up only with four. One version is unaccounted for.

56. **AUTO-9 is stale. Minor.** It says "what stands is that it separated, by the margin stated". §6.4 now gives an exact margin of −0.0649 for that W, meaning it did not separate.

57. **§3.4 versus §3.9. Moderate.** §3.4 says "claims in this paper are traced to their source; where the trace does not exist, the claim is not made". §3.9 says "the rest of the paper has not been re-verified passage by passage". Items 17, 19, 30 and 31 are such untraced claims.

58. **Statements fixed at N = 32. Minor.** §3.7 ("operational corpus is at N = 32") and §8.3 ("N=32 scale… All empirical results carry this qualification") predate the results at N = 7, 19, 20 and 146. §7.4 gives "N = 20–32".

59. **Dangling cross-references and antecedents. Minor.**
    - §6.4 "(§4.2.4)" for the photograph; §4.2.4 is Premises.
    - §8.3 "(§7.6)" for hysteresis; it is in §7.4.
    - §8.5 "The first of these nulls" has no antecedent.
    - §8.5 "The re-measurement of N_eff" has no antecedent.
    - §1 "Their findings…" now attaches to the KR sentence.
    - "case 09" (§4.3.1) does not match the table's "0.9".
    - "[DEFS §15]" and "T0/T1" are undefined and not referenced.
    - Working reports are "v1–v31" in §3.2 and "v2–v31" in the references.

60. **Uncited references. Minor.** Goltsev 2006, Lewis 2020, Yedidia 2003, Baars 1988, Shaw 2014 and Fremantle 1993 are listed but never cited in the text. "Declared Influences" may be intended, but that is not said.

61. **Appendix A depends on version history the reader does not have. Minor.** "Retired in v30", "the review point", "v32, header" all refer to it. AUTO-11 to AUTO-15 are not referenced from the body, and AUTO-5 is out of order.

62. **Other small inconsistencies. Minor.**
    - FabricationService is "being rewritten" (§8.2) under a heading that says the services "are operational".
    - §4.1.6 says the debate corpus has "nodes are authors", but v8g's nodes are the two stance poles.
    - §5.1's "disagree" and "agree" do not add to 100% and the remainder is not explained.
    - §5.1 says disagreement dominates within the pro group, but it also dominates within the anti group (43.1% against 31.4%).
    - §3.8's labels do not include "Proved", "Documented", "GAP" or "Measurement", which §6.3 and §8.1 use.

## Items produced mainly because a list was expected

- **Item 12** (M.M. and Free will): the paper already discloses both, and I added it for completeness. Marked.
- **Items 60 and 62:** real, but small. I listed them because I was being thorough, not because they affect what the paper establishes. Partly marked.
- **Item 26** (Beggs & Plenz) depends on my memory more than on the text. It is not a list filler, but it carries less weight than it looks.

None of the others was produced to fill the list. Items 13, 34, 36 and 38 are the ones the text itself most clearly required, along with the attempt-5 inconsistency in item 54. The arithmetic behind items 13, 39, 54 and the margins was recomputed, not taken from the paper.
