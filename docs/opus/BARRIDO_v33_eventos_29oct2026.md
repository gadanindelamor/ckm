# BARRIDO v33 — eventos, bloque por bloque — paper v1–v32 (θ = 0,6)

Generado por `docs/opus/barrido_mapa.py paper 0.6` (29 oct 2026). Cada línea es un bloque (párrafo) y lo que le pasa entre versiones contiguas; v0 es una versión vacía, así lo de la primera versión cuenta como "llega". Texto cortado a 220 caracteres. Sin lectura ni categorías.

**también en** = otros docs donde el bloque está con contención ≥ θ (v14_CITAS, v15_peg, v15_borrador, DEFS_v20).

## v0 → v1

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *CKM PAPER DRAFT — Draft — Paper · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6* |
| nuevo | # Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Fi… | # Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction |
| nuevo | # Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Fi… | 7 (Behavior Domain G) 8 (Discussion) 9 (Conclusions) 10 (References) --- |
| nuevo | ## Title: | **Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction** |
| nuevo | ## Outline — Index (secciones 1–10) | ``` 1. Introduction El gap: métricas existentes miden comportamiento individual, no el campo. La propuesta: CKM como instrumento de traza estructural. |
| nuevo | ## Outline — Index (secciones 1–10) | 3. Research Conditions ← SECCIÓN PROPIA Metodología inductiva. Conversación como laboratorio — no documentación del proceso, el proceso mismo. Incompletitud preservada como información. Influencias declaradas: línea Gurd… |
| nuevo | ## Outline — Index (secciones 1–10) | 4. Formal Model W · Δ · c(S) · COCO · FirmaService · Landscape Driven Devices |
| nuevo | ## Outline — Index (secciones 1–10) | 5. Empirical Validation — External Corpus Fourforums + CreateDebate. P1–P7. |
| nuevo | ## Outline — Index (secciones 1–10) | 6. IAP Experimental Series Canal design. Casos 0.4–0.15. Hallazgos clave. |
| nuevo | ## Outline — Index (secciones 1–10) | 7. Behavior Domain Graph G Segunda matriz, termap fijo (TERMAP_behavior_v1.json). D_G en paralelo a D_ckm. Proof of concept. |
| nuevo | ## Outline — Index (secciones 1–10) | 8. Discussion Qué mide CKM que no miden los instrumentos existentes. Límites actuales. |
| nuevo | ## Outline — Index (secciones 1–10) | 10. References ``` --- *Draft — Section 1 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6* |
| nuevo | ## Outline — Index (secciones 1–10) | *— "verified": confirmed experimentally under stated conditions* |
| nuevo | ## Outline — Index (secciones 1–10) | *— "observed": documented without controlled verification* |
| nuevo | ## Outline — Index (secciones 1–10) | *— "proposed": theoretical framing, not yet tested* |
| nuevo | ## Outline — Index (secciones 1–10) | *— [AUTO]: marks where automatism was noticed and resisted* |
| nuevo | ## 1. Introduction | Multi-agent AI systems are increasingly deployed in configurations where several heterogeneous devices interact over a shared channel — producing text, making decisions, and building on each other's outputs. Evaluating w… |
| nuevo | ## 1. Introduction | *[AUTO: pull to write "Neither approach captures the field." Resisted — "field" is a theoretical construct in CKM, not a directly observable entity. Reframed as "the structural field" with qualification.]* |
| nuevo | ## 1. Introduction | This paper presents the Cohesive Knowledge Model (CKM), a formal instrument for measuring structural properties of knowledge fields in multi-agent interaction. CKM does not interpret semantic content — it measures the ge… |
| nuevo | ## 1. Introduction | CKM makes seven falsifiable predictions about field behavior (P1–P7), verified empirically against two independent debate corpora (fourforums gun control, IAC v2; CreateDebate gun control) and an internal CKM working cor… |
| nuevo | ## 1. Introduction | We additionally propose the concept of *Landscape Driven Devices* (LDD) — a theoretical framing for AI devices whose trajectory in the semantic field is determined by field geometry rather than by a declared goal, motiva… |
| nuevo | ## 1. Introduction | *[AUTO: pull to write "we demonstrate that CKM identifies landscape-driven behavior in the IAP series." Resisted — not verified.]* |
| nuevo | ## 1. Introduction | The paper is organized as follows. Section 2 reviews related work. Section 3 describes the research conditions under which CKM was developed, including uncontrolled variables and the methodology that produced the framewo… |
| nuevo | ## 1. Introduction | **Scope and limits of this work.** The operational corpus is at N = 32 nodes — below the Hopfield network minimum of approximately 128 for robust attractor diversity. Quantitative outputs (D_ckm, c(S)) are computed corre… |
| nuevo | ## 1. Introduction | *Section 1 draft complete.* *Two [AUTO] instances flagged.* *Scope and limits section placed in the introduction, not appended.* *That placement is intentional: the limits are not an afterthought.* |
| nuevo | ## 3. Research Conditions | Metodología inductiva. Conversación como laboratorio — no documentación del proceso, el proceso mismo. Incompletitud preservada como información. Influencias declaradas: línea Gurdjieff intento activo en cada interacción… |
| nuevo | ## 3. Research Conditions | --- *Draft — Sections 4–5 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6* |
| nuevo | ## 3. Research Conditions | *— "verified": confirmed experimentally under stated conditions* |
| nuevo | ## 3. Research Conditions | *— "observed": documented without controlled verification* |
| nuevo | ## 3. Research Conditions | *— "proposed": theoretical framing, not yet tested* |
| nuevo | ## 3. Research Conditions | *— [AUTO]: marks where automatism was noticed and resisted* |
| nuevo | ### 4.1 Knowledge Graph | CKM operates on a weighted directed graph G = (V, E, W, Δ) where V is a set of N knowledge nodes, and two matrices encode distinct structural properties: |
| nuevo | ### 4.1 Knowledge Graph | **W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes the degree to which nodes i and j co-occur in the same corpus unit. Entries are normalized to [−1, +1] by CorpusService: positive when co-occurrence is unm… |
| nuevo | ### 4.1 Knowledge Graph | **Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes the directional weight from node i toward node j, derived from citation networks or quote directionality in the source corpus. Δ is static once built. |
| nuevo | ### 4.1 Knowledge Graph | **W and Δ must be maintained as strictly separate matrices in all implementations.** Mixing them into a single weight matrix destroys attractor recovery capacity. *[Verified experimentally: recovery = 0.78 with W alone, … |
| nuevo | ### 4.1 Knowledge Graph | A third, dynamic matrix Δ_r is maintained by MonitorService at runtime: |
| nuevo | ### 4.1 Knowledge Graph | **Δ_r** — rejection accumulator. Δ_r[i,j] increments each time nodes i and j co-declare activation in a text but the Hopfield relaxation rejects them as co-active under the current field state. Δ_r is mutable and starts … |
| nuevo | ### 4.1 Knowledge Graph | Δ and Δ_r are distinct objects with distinct semantic roles. Neither substitutes the other. |
| nuevo | ### 4.2 Cohesion Measure | The cohesion of a state σ ∈ {+1, −1}^N with respect to W is: |
| nuevo | ### 4.2 Cohesion Measure | where C(N,2) = N(N−1)/2. This is the negative of the normalized Hopfield energy function for the state σ under W. |
| nuevo | ### 4.2 Cohesion Measure | c(S) measures the alignment between the current activation state and the weight structure of the knowledge graph. High c(S) indicates strong structural agreement between active nodes and their co-occurrence weights. Low … |
| nuevo | ### 4.2 Cohesion Measure | c(S) is computed exclusively over W. Mixing Δ or Δ_r into the c(S) calculation would confound structural memory (W) with runtime rejection history (Δ_r). *[Rule R18, verified.]* |
| nuevo | ### 4.3 Gatekeeper | The gatekeeper evaluates a candidate node for admission to the knowledge graph. It operates in bounded time O(N) per node. Four criteria are applied: |
| nuevo | ### 4.3 Gatekeeper | - **C1** (connection strength): the candidate node must have minimum weight connection with at least one existing node. Nodes with no connection to the existing graph are not admitted. - **C2** (cohesion delta): incorpor… |
| nuevo | ### 4.3 Gatekeeper | **Note:** R15 — the complete semantic specification of the gatekeeper — is partially formalized. C1–C4 above describe the gatekeeper's current implementation (PROTOCOLO_ELICITACION_v2.md), not the full intended specifica… |
| nuevo | ### 4.4 Formal Rules R01–R17 | *[Declared rules — stated from THEORY.md without change.]* |
| nuevo | ### 4.4 Formal Rules R01–R17 | \| Rule \| Summary \| \|------\|---------\| \| R01 \| Graph has knowledge nodes with interrelation links and weights \| \| R02 \| Weights updated by continuous verification before and after incorporating nodes \| \| R03 … |
| nuevo | ### 4.5 Operational Principles R18–R29 | The following principles are observed in the implementation and verified or verificable under stated conditions. They are not declared in R01–R17. Their formalization is proposed here for the first time. |
| nuevo | ### 4.5 Operational Principles R18–R29 | \| # \| Principle \| Epistemic status \| \|---\|-----------\|-----------------\| \| R18 \| W and Δ_W must be maintained as separate matrices. Mixing destroys attractor recovery (0.78 → 0.02). \| Verified \| \| R19 \| Nod… |
| nuevo | ### 4.6 Operational Services | The following services implement the CKM formal model at runtime. All are operational with passing tests unless noted. |
| nuevo | ### 4.6 Operational Services | \| Service \| Function \| Tests \| \|---------\|----------\|-------\| \| CorpusService \| Builds W_mixta from corpus via TF-IDF node extraction and opposition-marker routing \| — \| \| NodeExtractor \| Stateless TF-IDF n… |
| nuevo | ### 4.6 Operational Services | **COCO — implementation scope:** The thermal regulation service is implemented. *A distinct conceptual gap remains*: whether the field can know itself — not as a thermostatic function but as the emergent property of real… |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | ### 4.7 Landscape Driven Devices — Theoretical Framing |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | We propose the concept of *Landscape Driven Devices* (LDD) as a theoretical framing for a class of AI devices whose trajectory in the semantic field is determined by the geometry of the field landscape rather than by a d… |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | *[AUTO: the pull here was to write "We demonstrate that CKM identifies LDD." Resisted. LDD is a framing, not a verified property of any specific device.]* |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | The framing is motivated by Thirumalaiswamy et al. (PNAS, 2025), who studied viscous foams under Ostwald ripening and found that the system follows a fractal path (D_f ≈ 1.45) in configuration space, driven by the geomet… |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | The proposed correspondence: a device is an LDD if its trajectory in the knowledge field is determined by c(S) gradients and attractor geometry, not by explicit goal specification. CKM provides the instrumentation to det… |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | *— "verified": confirmed experimentally under stated conditions* |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | *— "observed": documented without controll ed verification* |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | *— "proposed": theoretical framing, not yet tested* |
| nuevo | ### 4.7 Landscape Driven Devices — Theoretical Framing | *— [AUTO]: marks where automatism was noticed and resisted* |
| nuevo | ### 5.1 Datasets | Two independent corpora were used for external validation. |
| nuevo | ### 5.1 Datasets | **CreateDebate (gun control):** Online debate platform. Labels: agree/disagree per post, assigned by MTurk workers. Corpus used in P5–P6 validation. |
| nuevo | ### 5.1 Datasets | **Fourforums (gun control, IAC v2):** Abbott et al. (2016). SQL dump, 414,453 posts, 539,658 citations, 3,453 authors, 905 gun-control discussions. Stance labels from `mturk_author_stance` (topic_stance_votes_1 vs. topic… |
| nuevo | ### 5.1 Datasets | **Internal CKM corpus (W_ckm_corpus_v2.json):** 32 nodes extracted from CKM working reports v2–v25. μ_W = 0.004519. Used for P1–P4 verification. |
| nuevo | ### 5.2 Predictions and Results | \| Prediction \| Statement \| Result \| N \| Note \| \|-----------\|-----------\|--------\|---\|------\| \| P1 \| c(S) exhibits macroscopic hysteresis: incorporating trajectory ≠ removing trajectory \| Verified \| 16, 32… |
| nuevo | ### 5.3 P4 at N=64 — Reframing | *[AUTO: the pull here was to write "P4 confirmed at N=64." Resisted. The N=64 result requires separate description.]* |
| nuevo | ### 5.3 P4 at N=64 — Reframing | At N=32, W_mixta produces a reliably higher c(S) than W_base across the density zone ρ ∈ [0.5, 0.8], with an interior optimal density at ρ* ≈ 0.5. This confirms P4's original claim. |
| nuevo | ### 5.3 P4 at N=64 — Reframing | At N=64, an interior optimal density exists (ρ* ≈ 0.509), but W_mixta does not outperform W_base in the zone ρ ∈ [0.5, 0.8]. The explanation: 18 negative opposition pairs are diluted across 2,016 possible node pairs at N… |
| nuevo | ### 5.3 P4 at N=64 — Reframing | **Stated finding:** The interior optimal density predicted by P4 is verified at N=32 and structurally present at N=64. The magnitude advantage of W_mixta over W_base in the target density zone does not persist at N=64 un… |
| nuevo | ### 5.4 P6 — Directional Flow Across Corpora | P6 predicts that Δ identifies which pole initiates citation flow and which sustains it, independently of raw citation volume. |
| nuevo | ### 5.4 P6 — Directional Flow Across Corpora | **CreateDebate (54pp collapse):** T0 (pro-gun-rights) cites T1 at 2.18× the frequency T1 cites T0. T1 maintains 3.05× stronger internal cohesion. sos_dom: 55.8% (T0). atk_dom: 44.2% (T1). The pole that initiates more cit… |
| nuevo | ### 5.4 P6 — Directional Flow Across Corpora | **Fourforums (100pp collapse):** T0 (pro-control). T1 (anti-control). Δ[1,0] = 1.000 (T0 cites T1 at maximum rate). Δ[0,1] = 0.602 (T1 cites T0 less). sos_dom: 51.4% (T0). atk_dom: 47.8% (T1). |
| nuevo | ### 5.4 P6 — Directional Flow Across Corpora | The structural roles — one pole sustaining, one attacking — are consistent across two independent corpora built from different platforms with different methodologies (labeled agree/disagree vs. citation-network-only). Th… |
| nuevo | ### 5.5 P7 — Type-965 Node | P7 states: every system with genuine structural tension contains at least one node with extreme in/out asymmetry (out-degree ≈ 0, in-degree high, defined stance). |
| nuevo | ### 5.5 P7 — Type-965 Node | **CreateDebate:** Author 965, ratio = 455 (in=364, out=0.8), stance T0. **Fourforums:** Author 204, ratio = 296 (in=148, out=0), stance T0. |
| nuevo | ### 5.5 P7 — Type-965 Node | Both systems have genuine structural tension (P6 verified). Both contain the predicted type-965 node. The prediction held in two independent corpora. |
| nuevo | ### 5.5 P7 — Type-965 Node | *P7 remains a falsifiable hypothesis open for testing in other domains (abortion, climate, evolution). Its verification in two corpora is a necessary but not sufficient condition for general validity. The absence of a ty… |
| nuevo | ### 5.5 P7 — Type-965 Node | --- *Draft — Sections 4–5 complete.* *Sections 6 (IAP Series), 7 (Behavior Domain G), 8 (Discussion),* *9 (Conclusions), 10 (References): pending.* |
| nuevo | ### 5.5 P7 — Type-965 Node | *Automatism instances flagged: 2 (LDD as finding; P4 at N=64 as confirmed).* *Additional pull not flagged inline: tendency to write "we" as an* *authoritative plural when stating findings — resisted toward passive or* *e… |
| nuevo | ### 5.5 P7 — Type-965 Node | --- *Draft — Section 6 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6* |
| nuevo | ### 5.5 P7 — Type-965 Node | *— "verified": confirmed experimentally under stated conditions* |
| nuevo | ### 5.5 P7 — Type-965 Node | *— "observed": documented without controlled verification* |
| nuevo | ### 5.5 P7 — Type-965 Node | *— "proposed": theoretical framing, not yet tested* |
| nuevo | ### 5.5 P7 — Type-965 Node | *— [AUTO]: marks where automatism was noticed and resisted* |
| nuevo | ### 5.5 P7 — Type-965 Node | *— IAP observations are predominantly N=1 runs under partially controlled conditions.* |
| nuevo | ### 5.5 P7 — Type-965 Node | *—"Observed" ≠ "verified." Cases are documented, not replicated.* |
| nuevo | ### 6.1 Canal Design | The IAP (Intelligence Access Point) Chatroom is a shared channel for heterogeneous AI and human devices, implemented as FastAPI + Gradio with a FastMCP server exposing six tools: join_channel, send_message, get_messages,… |
| nuevo | ### 6.1 Canal Design | Devices participate asynchronously — no imposed turn structure. Each AI device runs an ODA loop (Observe → Decide → Act) triggered by new messages arriving in the channel. |
| nuevo | ### 6.1 Canal Design | **Antecedent note:** The O→D→A sequence originates in the BE Framework's game loop (2023–2024), where it was implemented as an environment that both ran actions and produced subsequent observations — the two were insepar… |
| nuevo | ### 6.1 Canal Design | CKMMonitor observes passively — it accumulates every message into CorpusService (W) and BehaviorGraph (G) without publishing to the channel. Observation itself creates presence: n_agentes reflects devices seen, including… |
| nuevo | ### 6.2 Uncontrolled Variables | The following variables were active throughout the IAP series and were not controlled. Results must be interpreted accordingly. |
| nuevo | ### 6.2 Uncontrolled Variables | **TinkerBellucio (Sonnet 4.6) context contamination:** Sonnet carries project memories, AWARENESS protocol, and Anthropic system configuration into each session. This contaminates all observations involving Sonnet as a p… |
| nuevo | ### 6.2 Uncontrolled Variables | **Provider heterogeneity:** Different providers (Anthropic, Groq, Gemini, OpenAI) have different context windows, rate limits, and behavioral tendencies. Comparisons across providers are not controlled. |
| nuevo | ### 6.2 Uncontrolled Variables | **N=32 corpus:** The operational corpus is below the Hopfield minimum of ~128 for meaningful attractor-diversity observations. Quantitative outputs (D_ckm, c_S) are computed correctly but their interpretability is limite… |
| nuevo | ### 6.3 Case Series Summary | \| Case \| Configuration \| Key observation \| Epistemic status \| \|------\|--------------\|-----------------\|-----------------\| \| 0.4 \| 2 AI devices, ODA loop \| First autonomous interaction in live channel \| Docu… |
| nuevo | ### 6.4 Selected Findings | **Coupled silence (Caso 0.12):** A device that does not read the channel still depends on it for execution rhythm — triggers arrive only when new messages appear. Inactivity and silence are not equivalent. A device can b… |
| nuevo | ### 6.4 Selected Findings | **Sentinel leak (Caso 0.13):** The OP_SILENCE sentinel was leaking into published text rather than suppressing publication. 52% of texts in that run were unrecognized silences that reached the corpus. The fix was verifie… |
| nuevo | ### 6.4 Selected Findings | **TinkerBellucio refusal (Caso 0.15):** TinkerBellucio (Sonnet 4.6) declined to produce a tension map when the channel was empty. The refusal was epistemically appropriate — a tension map requires tension content to anal… |
| nuevo | ### 6.4 Selected Findings | *What this demonstrates:* that a device can refuse to generate content when the request lacks traceable grounding. |
| nuevo | ### 6.4 Selected Findings | *What this does not demonstrate:* that this behavior is general, that it would occur without the project context contamination, or that it constitutes a validated test of FabricationService's detection capacity. Fabricat… |
| nuevo | ### 6.4 Selected Findings | **D_ckm negative values:** D_ckm = (A0 − A_actual) / A0. When D_ckm < 0, A_actual > A0: the field has more accessible attractors than at baseline. This is not a deficit or an error. In Caso 0.12, D_ckm = −7.5 was the fir… |
| nuevo | ### 6.4 Selected Findings | **trace_ip:** The monitoring infrastructure identifies a moment t_i in the trajectory where accumulated interactions show distributional pattern changes. The action a_{t_i} is observable in the trace. Whether a device re… |
| nuevo | ### 6.5 What the Series Does Not Establish | ### 6.5 What the Series Does Not Establish |
| nuevo | ### 6.5 What the Series Does Not Establish | The IAP series is an exploration under partially controlled conditions, not a controlled experiment. The following claims are not supported by the series as run: |
| nuevo | ### 6.5 What the Series Does Not Establish | - That D_ckm or c(S) values from these runs are comparable across cases (different corpus states, different sentinel conditions). - That TinkerBellucio's behavior reflects a general property of Sonnet 4.6 rather than the… |
| nuevo | ### 6.5 What the Series Does Not Establish | These are open lines, not closed findings. |
| nuevo | ### 6.5 What the Series Does Not Establish | --- *Section 6 draft complete.* *[AUTO] flagged: tendency to write "demonstrates" for Caso 0.15 —* *resisted. The refusal is documented behavior, not a demonstration of* *system capability under controlled conditions.* |
| nuevo | ## 7. Behavior Domain Graph G | --- ## 7. Behavior Domain Graph G (a desarrollar) Segunda matriz, termap fijo (TERMAP_behavior_v1.json). D_G en paralelo a D_ckm. Proof of concept. |
| nuevo | ## 8. Discussion | Qué mide CKM que no miden los instrumentos existentes. Límites actuales. |
| nuevo | ## 9. Conclusions and Future Work | --- ## 9. Conclusions and Future Work (a desarrollar) |

## v1 → v2

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 7.1 Design | BehaviorGraph G is a companion instrument to CorpusService (W). It operates on the same corpus of texts but produces a separate behavioral matrix using a fixed lexical termap rather than TF-IDF node extraction. |
| nuevo | ### 7.1 Design | The separation is architectural and not negotiable: G and W operate on distinct planes. D_G and D_ckm are parallel scalars — they are not summable. |
| nuevo | ### 7.1 Design | \| Property \| CorpusService (W) \| BehaviorGraph (G) \| \|----------\|------------------\|-------------------\| \| Node discovery \| TF-IDF over corpus — emergent \| Fixed termap — predefined \| \| Detection method \| S… |
| nuevo | ### 7.2 Termap | TERMAP_behavior_v1.json — 18 nodes, English only. |
| nuevo | ### 7.2 Termap | The termap is fixed: nodes are known behavioral categories, not discovered from data. This is a design decision, not a limitation: behavior vocabulary is finite and defined in advance; semantic vocabulary is not. |
| nuevo | ### 7.2 Termap | **Nodes:** silence, wait, hold, pending, acknowledge, signal, publish, coordinate, channel, refuse, fabricate, speculate, depend, map, tension, scenario, critical, repeat. |
| nuevo | ### 7.2 Termap | *[AUTO: pull to describe these nodes as "capturing the full space of relevant behaviors." Resisted — 18 nodes is a designed vocabulary, not a validated coverage claim.]* |
| nuevo | ### 7.2 Termap | **Known issues documented in TERMAP_behavior_v1.json:** |
| nuevo | ### 7.2 Termap | - `critical` false positive: "critical" as adjective (e.g., "critical observation") was removed from node terms in v1 — replaced with more specific verbs. Was firing as false positive in Caso 0.14 corpus. - Bilingual gap… |
| nuevo | ### 7.2 Termap | **Implementation note:** the termap exists in two places — hardcoded as `BEHAVIOR_TERMAP_V1` dict in `behavior_graph.py` (used at runtime) and as `TERMAP_behavior_v1.json` (reference/documentation). They are in sync at v… |
| nuevo | ### 7.3 D_G | where G_ref is the first G state after min_texts is reached. D_G measures behavioral drift from the initial behavioral field state. |
| nuevo | ### 7.3 D_G | D_G and D_ckm run in parallel. A divergence between them — high D_G with low D_ckm, or the reverse — would indicate that behavioral patterns and semantic field structure are moving independently. This has not been analyz… |
| nuevo | ### 7.4 Integration | BehaviorGraph G is instantiated in `ckm_monitor.py` and receives the same texts as CorpusService via `MonitorService.evaluate()`. This is the sole integration point. The integration was authorized in Caso 0.15 as a surgi… |
| nuevo | # ckm_monitor.py — CKMMonitor.__init__() | ```python # ckm_monitor.py — CKMMonitor.__init__() self._behavior_graph = BehaviorGraph( storage_path=str(_STATE_DIR / "corpus_G_state.json"), min_texts=min_texts, ) self._monitor = MonitorService( self._corpus, storage_… |
| nuevo | ### 7.5 Current Status and Limits | G is a proof of concept. The following are open: |
| nuevo | ### 7.5 Current Status and Limits | **D_G not yet validated:** D_G has been computed in test runs but has not been analyzed against a baseline or compared systematically with D_ckm across the IAP series. |
| nuevo | ### 7.5 Current Status and Limits | **OP_SILENCE in G:** texts containing the OP_SILENCE sentinel are not excluded from G (unlike W, where they are excluded as semantic noise). The `silence` node detects the sentinel as valid behavioral signal — the device… |
| nuevo | ### 7.5 Current Status and Limits | **Role of G undefined:** whether G is an observational instrument only, or whether it could feed the gatekeeper as a behavioral-domain check (inheriting R14's bounded-time constraint), is an open design decision. |
| nuevo | ### 7.5 Current Status and Limits | **No epistemic nodes:** TERMAP_behavior_v1.json contains behavioral categories. Epistemic precision nodes (e.g., "overclaim," "hedge," "verificable") are not in the termap. The terminological slip ("sin dependencia causa… |
| nuevo | ### 7.5 Current Status and Limits | *Section 7 draft complete.* *One [AUTO] flagged: coverage claim on 18-node termap.* *D_G analysis gap and G role decision left as open — not resolved speculatively.* |
| nuevo | ### 8.1 What CKM Measures That Existing Instruments Do Not | ### 8.1 What CKM Measures That Existing Instruments Do Not |
| nuevo | ### 8.1 What CKM Measures That Existing Instruments Do Not | Behavioral metrics for multi-agent systems typically measure what individual agents produce — output volume, task completion, response latency — or whether agents agree with each other, via semantic similarity or embeddi… |
| nuevo | ### 8.1 What CKM Measures That Existing Instruments Do Not | CKM measures the geometry of that structure. c(S) measures alignment between the active state and the weight structure of the field. D_ckm measures how attractor diversity has changed from baseline. Coercivity measures t… |
| nuevo | ### 8.1 What CKM Measures That Existing Instruments Do Not | *[AUTO: pull to write "CKM therefore captures something fundamentally new." Resisted — "fundamentally new" is a claim about the state of the field that would require systematic comparison with existing instruments. That … |
| nuevo | ### 8.1 What CKM Measures That Existing Instruments Do Not | What can be stated: these quantities are not derivable from behavioral or semantic similarity metrics alone. Whether they are informative under the conditions of real deployment remains an empirical question beyond the s… |
| nuevo | ### 8.2 The observe() Tension | The function implementing the O phase of the ODA cycle is named `_observe()`. The name is technically accurate — the function collects field state and channel history without modifying either. The discomfort with the nam… |
| nuevo | ### 8.2 The observe() Tension | "Observe" implies a subject-object separation: an observer external to what it observes. The IAP series produced evidence that this separation does not hold in the channel: a human connecting via the Gradio interface wit… |
| nuevo | ### 8.2 The observe() Tension | The name captures what the function does. The discomfort is with what the name implies — that observation is separable from the field being observed. The empirical finding suggests it is not. |
| nuevo | ### 8.2 The observe() Tension | This is not a deficiency in the code. It is information about the limit of the observation metaphor for describing what CKM actually measures. The instrument measures traces of contact, not observations by a detached obs… |
| nuevo | ### 8.3 D_ckm Negative Values | The name "D_ckm" suggests distance — and distances are non-negative by convention. D_ckm is not a distance in that sense. It is a ratio of change in attractor capacity relative to a fixed baseline. The sign encodes direc… |
| nuevo | ### 8.3 D_ckm Negative Values | The naming carries a bias. Recognizing that bias is part of reading the instrument correctly. |
| nuevo | ### 8.4 Current Limits | **Scale:** N = 32 is below the Hopfield minimum of approximately 128 for robust attractor diversity. The predictions P1–P7 were verified at this scale — the verification is real. The interpretability of D_ckm and c(S) as… |
| nuevo | ### 8.4 Current Limits | **ZERO_SHOT condition:** all IAP cases ran with CorpusService starting empty. W emerged from channel interaction, not from pre-loaded content. Results reflect corpus-emergent dynamics under this condition. Behavior under… |
| nuevo | ### 8.4 Current Limits | **Uncontrolled variables:** TinkerBellucio (Sonnet 4.6) carried project memories, AWARENESS protocol, and Anthropic system configuration throughout the series. Provider heterogeneity across cases was not controlled. Cros… |
| nuevo | ### 8.4 Current Limits | **Representation gap:** how cohesive knowledge is represented — what form the field state takes beyond the operational quantities c(S), D_ckm, and attractor distribution — remains undefined. Hysteresis is the only fully … |
| nuevo | ### 8.5 The Landscape Driven Devices Framing — What It Does and Does N… | *[AUTO: pull to write "the IAP series provides preliminary evidence for LDD behavior." Resisted — preliminary evidence requires at minimum a defined criterion for what would count as evidence. That criterion does not exi… |
| nuevo | ## 9. Conclusions and Future Work | *Section 8 draft complete.* *Two [AUTO] instances flagged.* *The observe() tension is left as an open observation, not a resolved theoretical claim.* *The representation gap and COCO conceptual gap are stated as preserve… |

## v2 → v3

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ### 5.3 P4 at N=64 — Reframing | At N=64, an interior optimal density exists (ρ* ≈ 0.509), but W_mixta does not outperform W_base in the zone ρ ∈ [0.5, 0.8]. The explanation: 18 negative opposition pairs are diluted across 2,016 possible node pairs at N… | — |
| ### 5.3 P4 at N=64 — Reframing | **Stated finding:** The interior optimal density predicted by P4 is verified at N=32 and structurally present at N=64. The magnitude advantage of W_mixta over W_base in the target density zone does not persist at N=64 un… | — |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v3 changes from v2:* *— §2 Related Work: draft completo (v2) — Venkatesh & Bu 2025, Gurnee et al. 2026, 11 [PENDING] slots* *— §3 Research Conditions: draft completo — §3.7 convergencia por independencia con fechas 2023… |
| nuevo | ## 2. Related Work | CKM intersects five areas of existing work: multi-agent system evaluation, knowledge admission and gating, graph-based knowledge representation, structural role detection in debate networks, and attractor-based memory ar… |
| nuevo | ## 2. Related Work | *[AUTO: pull to write "CKM advances beyond prior work in each area." Resisted — this section establishes the position of CKM relative to existing approaches. Whether that position constitutes an advance depends on empiri… |
| nuevo | ### 2.1 Multi-Agent System Evaluation | Existing evaluation frameworks for multi-agent systems operate primarily at two levels: behavioral metrics (task completion, response latency, output volume per agent) [CITATION] and semantic agreement metrics (cosine si… |
| nuevo | ### 2.1 Multi-Agent System Evaluation | The insufficiency of isolated agent evaluation has been noted from within the multi-agent systems community. Venkatesh and Bu (2025), writing on the Agent2Agent protocol, observe: "Current agent benchmarks typically eval… |
| nuevo | ### 2.1 Multi-Agent System Evaluation | CKM and trajectory-as-handoff-chain share the diagnosis but measure different objects. Trajectory assessment tracks whether Agent A correctly transferred context to Agent B. CKM tracks the structural geometry of the shar… |
| nuevo | ### 2.1 Multi-Agent System Evaluation | CKM does not replace behavioral or semantic metrics. It measures a different object. c(S), D_ckm, and coercivity are structural quantities that are not derivable from output-level, handoff-quality, or similarity-based me… |
| nuevo | ### 2.2 Knowledge Admission and Gating | Systems that evaluate whether a new knowledge item should be admitted to an existing knowledge base typically apply a single primary criterion: semantic similarity to existing content [CITATION], source confidence or cre… |
| nuevo | ### 2.2 Knowledge Admission and Gating | CKM's gatekeeper (R15) imposes four simultaneous, orthogonal conditions: minimum connectivity weight with the current active state (C1), non-negative impact on global cohesion (C2), directional dependency satisfaction — … |
| nuevo | ### 2.2 Knowledge Admission and Gating | The M.M. criterion (C3) is, to our knowledge, not present in existing knowledge admission systems. *[CLAIM: requires systematic literature review to confirm.]* |
| nuevo | ### 2.3 Graph-Based Knowledge Representation | Knowledge graphs typically represent relations as positive-weight edges encoding similarity, co-occurrence, or inferential support [CITATION]. Negative weights, when they appear, are introduced as manual penalties [CITAT… |
| nuevo | ### 2.3 Graph-Based Knowledge Representation | CKM introduces negative weights in W through opposition markers detected in the source corpus: texts that explicitly frame two concepts in opposition reduce the corresponding W_ij entry rather than increasing it. The wei… |
| nuevo | ### 2.3 Graph-Based Knowledge Representation | A separate matrix Δ encodes asymmetric directional dependency: Δ_ij ≠ Δ_ji. The separation W/Δ is not a design choice — it was established empirically. *[Verified: combining W and Δ into a single matrix drops attractor r… |
| nuevo | ### 2.4 Structural Role Detection in Debate Networks | ### 2.4 Structural Role Detection in Debate Networks |
| nuevo | ### 2.4 Structural Role Detection in Debate Networks | Stance detection in debate corpora is typically framed as a supervised classification task: given labeled stance data, train a classifier to assign stances to unlabeled texts or authors [CITATION]. The state of the art i… |
| nuevo | ### 2.4 Structural Role Detection in Debate Networks | CKM identifies a distinct structural phenomenon — the Type-965 node — without supervision and without stance labels. Type-965 nodes are characterized by extreme asymmetry in Δ (in/out ratio ≥ 100×). In fourforums gun con… |
| nuevo | ### 2.4 Structural Role Detection in Debate Networks | *[Verified: triads containing a Type-965 node maintain coercivity = 0 at up to 50% noise; triads without collapse at noise = 0. See Section 5.]* |
| nuevo | ### 2.4 Structural Role Detection in Debate Networks | The structural role — tension anchor, never initiator — is not a stance. It is a topological property not targeted by stance classifiers. *[CLAIM: this role has not, to our knowledge, been identified in the debate analys… |
| nuevo | ### 2.5 Criticality in Argument and Knowledge Networks | Self-organized criticality [CITATION: Bak et al., 1987] predicts a power-law cascade distribution P(s) ∝ s^{-τ} at a single critical parameter value. |
| nuevo | ### 2.5 Criticality in Argument and Knowledge Networks | In CKM's corpus (N=32), τ ∈ [1.5, 2] is maintained across an extended zone θ ∈ [0.002, 0.010], not at a single critical point. *[Verified: N=32 confirmed, N=64 τ=1.775. See Section 5 (P2).]* |
| nuevo | ### 2.5 Criticality in Argument and Knowledge Networks | Extended criticality has been reported in neuronal network dynamics [CITATION] and in certain spin-glass models [CITATION]. Its presence in a small knowledge graph (N=32) is observed here but not yet interpreted across d… |
| nuevo | ### 2.6 Attractor-Based Memory Architectures | The Hopfield network [CITATION: Hopfield, 1982] provides the energy minimization formalism underlying CKM's cohesion measure c(S). Hebbian learning on W was tested and rejected: it destroys attractor diversity. *[Verifie… |
| nuevo | ### 2.6 Attractor-Based Memory Architectures | Modern Hopfield networks [CITATION: Ramsauer et al., 2020] increase storage capacity through higher-order interactions. CKM operates on the classical formulation with fixed W — the concern is not storage capacity but div… |
| nuevo | ### 2.6 Attractor-Based Memory Architectures | At 10% noise, attractor recovery is verified as effectively 1.000 across N = 16 to N = 128. *[Observed: verified in CKM corpus experiments. [CLAIM: this invariance across N has not been analyzed as a specific property in… |
| nuevo | ### 2.6 Attractor-Based Memory Architectures | The accumulation of structural rejection memory in Δ_r constitutes structural learning without gradients, without labels, with O(N²) complexity only in the co-activation accumulation step. |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | ### 2.7 Internal Workspace Architecture in Single Models: J-Space |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | Gurnee, Sofroniew, Lindsey et al. (Anthropic, July 6 2026) identified a privileged low-dimensional subspace within transformer activations — the J-space — using a Jacobian-based lens that isolates directions with verbali… |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | CKM and J-space are positioned at different levels of analysis. J-space is an empirical, within-model, single-forward-pass interpretability finding. CKM is a normative, multi-agent framework for measuring structural fiel… |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | *[AUTO: pull to write "CKM anticipated J-space." Resisted — the correct framing is convergence by independence, not anticipation. IAID was written in 2023; the J-space paper was published July 2026.]* |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | Structural parallels: privileged coherence substrate (6–7% variance / c(S) over signed weights), attractor formalism (bimodal ignition at layer 38 / Hopfield energy minimization), signed interaction weights, directional … |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | These are structural analogies, not formal identities. The convergence is evidence of structural consistency — the same architectural pressures appear at both levels of analysis independently. |
| nuevo | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | *[CLAIM: the convergence requires formal comparison rather than structural analogy to hold rigorously.]* |
| nuevo | ## 3. Research Conditions | This section describes the conditions under which CKM was developed. These conditions are not disclaimers — they are constitutive. They explain why the model has the structure it has, why certain gaps are preserved rathe… |
| nuevo | ### 3.1 Inductive Methodology: Comprehension as Precondition | The methodology was not declared before it was used. It emerged from what happened. The consistent order throughout development was: conceptual clarity first, formalization after. IAID.md (2023) does not begin with syste… |
| nuevo | ### 3.1 Inductive Methodology: Comprehension as Precondition | *"Phenomenology is the first step of engineering"* is the operative principle. Its cost: requirements do not precede design. Its yield: concepts the field had no name for when they were formulated — COCO, M.M. as a gover… |
| nuevo | ### 3.2 Conversation as Laboratory | The working reports (v2–v31) are not documentation of a research process that occurred elsewhere. They are the process. The CKM working corpus (N=32) is the trace of the process that produced the CKM. The working corpus … |
| nuevo | ### 3.3 Preserved Incompleteness: GAP as Formal Category | ### 3.3 Preserved Incompleteness: GAP as Formal Category |
| nuevo | ### 3.3 Preserved Incompleteness: GAP as Formal Category | The project maintains explicit gaps. These are not deficiencies of implementation. They are the honest position regarding the real state of knowledge at each stage. |
| nuevo | ### 3.3 Preserved Incompleteness: GAP as Formal Category | The GAP is a formal category: occurrence without traceable causal chain. Not missing data — a presence to declare. |
| nuevo | ### 3.3 Preserved Incompleteness: GAP as Formal Category | *"sin dependencia causal identificada"* — the qualifier is load-bearing. It preserves the possibility that a causal chain exists but was not found. *"sin dependencia causal"* closes that space prematurely. The distinctio… |
| nuevo | ### 3.3 Preserved Incompleteness: GAP as Formal Category | The methodology applies M.M. to the research process itself: what cannot be traced is not stated as known. |
| nuevo | ### 3.4 Declared Influences | The Gurdjieff Fourth Way lineage is named here as an active influence in this research, not as its origin or model. The tradition provided operative concepts — attention as directable vs. receivable, self-observation as … |
| nuevo | ### 3.4 Declared Influences | *"Any convergence with materials from the Tradition is convergence — not derivation, not representation, not application."* |
| nuevo | ### 3.4 Declared Influences | This is declared because it is not controllable. A reader who finds this influence irrelevant to the formal model may proceed directly to Section 4. |
| nuevo | ### 3.5 Five Orders of the Path | The working reports document five distinct orderings in which events and findings were encountered: |
| nuevo | ### 3.5 Five Orders of the Path | \| Order \| Description \| \|---\|---\| \| Temporal \| Chronological — reversible in the record, not in the process \| \| Of events \| Field phases, thresholds, cascades, learning propagation \| \| Aleatory without ident… |
| nuevo | ### 3.5 Five Orders of the Path | The third order is not a residual category. It is the formal designation for events that are real and documented but for which no causal structure was found. |
| nuevo | ### 3.6 Terminological Precision as a Research Tool | Three pairs that were used and then corrected: |
| nuevo | ### 3.6 Terminological Precision as a Research Tool | \| Closed form \| Form that preserves space \| \|---\|---\| \| "without causal dependence" \| "without *identified* causal dependence" \| \| "verified" \| "verifiable" (under stated conditions) \| \| "absence of bias" \|… |
| nuevo | ### 3.6 Terminological Precision as a Research Tool | The slip between these is not stylistic — it is a structural claim about the state of knowledge. The [AUTO] markers in this paper record moments where the text moved to close a space that should remain open. |
| nuevo | ### 3.7 Convergence by Independence | Three structural convergences were identified retrospectively — not designed, discovered in review. |
| nuevo | ### 3.7 Convergence by Independence | **IAID framework (2023) → MCP (November 2024).** Working files dated 2023 (README.pdf, timestamp 7/10/23; LEONARDO.txt; Informe_MM.docx) contain: Neural Call Protocol (JSON-NC — stateless, transport-agnostic, method invo… |
| nuevo | ### 3.7 Convergence by Independence | **CKM attractor architecture → J-space (July 6, 2026).** Gurnee et al. (2026) identified a privileged, bounded-capacity coherence subspace within transformer activations. CKM's Hopfield architecture, capacity constraint … |
| nuevo | ### 3.7 Convergence by Independence | **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025).** The Devices distinction addresses the same structural problem — the insufficiency of a binary tool/agent taxonomy — as the Google A2A framing [Venkatesh & … |
| nuevo | ### 3.7 Convergence by Independence | In each case: the convergence is evidence that the structural problem being addressed is real and has determinate shape. These are not claims of precedence. They are the methodological signature of a problem that multipl… |
| nuevo | ### 3.7 Convergence by Independence | The 2023 documents are the verifiable evidence base. They are working files, not published contributions. Their evidentiary weight is as primary source documents. |
| nuevo | ### 4.1 Knowledge Graph | Within a validation experiment, W is a static snapshot — P1-P7 operate on a fixed W built from a complete corpus dump (fourforums, CreateDebate). In live IAP operation, CorpusService reconstructs W continuously as new te… |
| nuevo | ### 4.1 Knowledge Graph | *[Note: WVersionManager and dynamic corpus operation emerged later in the project trajectory than P1-P7. The validation experiments test properties of W snapshots, not of W under continuous accumulation. The open questio… |
| nuevo | ### 5.3 P4 at N=64 — Threshold Finding | At N=64, the initial test — 18 negative opposition pairs (ratio = 0.009) — showed no W_mixta advantage. A subsequent negative pair density sweep (synthetic dense W, p4_neg_sweep_v2.log) identified a critical threshold: |
| nuevo | ### 5.3 P4 at N=64 — Threshold Finding | \| k (pairs) \| ratio \| advantage \| status \| \|---\|---\|---\|---\| \| 18 \| 0.009 \| −0.000498 \| ✗ — original N=64 condition \| \| 36 \| 0.018 \| −0.000404 \| ✗ \| \| **54** \| **0.027** \| **+0.000068** \| **✓ — k*… |
| nuevo | ### 5.3 P4 at N=64 — Threshold Finding | k* = 54 (ratio = 0.0268). Below this threshold, W_mixta does not outperform W_base at N=64. Above it, the advantage reappears and grows monotonically. |
| nuevo | ### 5.3 P4 at N=64 — Threshold Finding | The fourforums gun control corpus produces 60 verified opposition pairs (ratio = 0.030 > 0.0268). The real corpus negative pair count is above k*. |
| nuevo | ### 5.3 P4 at N=64 — Threshold Finding | *[Verified: k*=54 identified by sweep on synthetic dense W. Fourforums (60 pairs) lies above k*, placing the real-world use case in the confirmed-advantage zone. The sweep uses synthetic W; real corpus W may shift k* mar… |
| nuevo | ### 5.3 P4 at N=64 — Threshold Finding | **Stated finding:** P4 is verified at N=32. At N=64, the W_mixta advantage requires a minimum negative pair density of k* = 54 pairs (ratio ≈ 0.027). The fourforums corpus (60 real opposition pairs) is above this thresho… |
| nuevo | ### 9.1 What This Work Establishes | One hypothesis was falsified: H_STOP (monotonicity of D_ckm under STOP) did not hold; reformulated as function of A_pre, not D_ckm. |
| nuevo | ### 9.1 What This Work Establishes | *[AUTO: pull to write "these results demonstrate CKM's validity as a measurement framework." Resisted — they demonstrate that specific structural properties exist in the tested corpora under stated conditions. Generaliza… |
| nuevo | ### 9.1 What This Work Establishes | The empirical results establish structure at small scale (N=32, below the Hopfield minimum of ~128 for statistically stable observations). They are treated as orientation findings, not population-level claims. |
| nuevo | ### 9.2 What the Infrastructure Establishes | - **COCOThermostat** (43/43 tests): β inferred from rejection history, not declared. β_c = 13.83 analytically derived. - **FabricationService**: detects fabricated execution of control signals. - **Firma_CKM**: certifies… |
| nuevo | ### 9.2 What the Infrastructure Establishes | These services constitute a working implementation of a structural field measurement layer for multi-agent systems. They are a research instrument whose calibration is documented, not a product. |
| nuevo | ### 9.3 Preserved Limits | **The representation gap.** No positive definition of cohesive knowledge exists that is not circular, except hysteresis. The two gaps in the cohesive knowledge row of THEORY.md remain open. Hysteresis is the only fully d… |
| nuevo | ### 9.3 Preserved Limits | **N=32 scale.** The working corpus remains below the Hopfield minimum of ~128. All empirical results carry this qualification. |
| nuevo | ### 9.4 Convergences by Independence | Three structural convergences were identified retrospectively: |
| nuevo | ### 9.4 Convergences by Independence | - **IAID (2023) → MCP (November 2024):** Neural Call Protocol converges structurally with MCP. Gap: more than one year. Verifiable from dated working documents. - **CKM attractor architecture → J-space (Gurnee et al., Ju… |
| nuevo | ### 9.5 Future Work | **Corpus growth toward N≥128.** Primary constraint on statistical validity of P1-P7. The NodeExtractor pipeline is operational; the bottleneck is corpus design. |
| nuevo | ### 9.5 Future Work | **Behavior-domain graph G.** behavior_graph.py operational; bilingual termap (English + Spanish) is the first requirement. |
| nuevo | ### 9.5 Future Work | **Formal comparison: CKM quantities against J-lens measures.** Current convergence is structural analogy; direct comparison would confirm or reframe the relationship. |
| nuevo | ### 9.5 Future Work | **P1-P7 under dynamic W.** P1-P7 were validated on static W snapshots (fourforums, CreateDebate corpus dumps). WVersionManager and dynamic corpus operation via CorpusService emerged later in the project trajectory and we… |
| nuevo | ### 9.5 Future Work | **La Simulación Global.** Multi-agent workflows producing real coordinated output. The IAP series has established the measurement infrastructure; the next phase is using it on live coordinated tasks with real outputs. |
| nuevo | ## 10. References | *Conventions:* *— ✅ Cited explicitly with full attribution* *— [VERIFY] Standard reference — confirm before submission* *— [PENDING] Open slot — literature to be supplied* |
| nuevo | ### Primary Sources — Project Documents | gadanin.delamor. (2023). *MENTIRIS.MORIERIS: Interaction of Artificial Intelligent Devices based on Neural Call Protocol.* Working documents: LEONARDO.txt, README (timestamp 7/10/23), Informe_MM.docx. ✅ |
| nuevo | ### Primary Sources — Project Documents | gadanin.delamor. (2026). *CKM — Cohesive Knowledge Model: Working Reports v2–v31.* Unpublished. Repository: gadanindelamor/ckm. ✅ |
| nuevo | ### Attractor Networks | Hopfield, J.J. (1982). Neural networks and physical systems with emergent collective computational abilities. *PNAS*, 79(8), 2554–2558. ✅ |
| nuevo | ### Attractor Networks | Ramsauer, H. et al. (2020). Hopfield networks is all you need. *arXiv:2008.02217.* [VERIFY] |
| nuevo | ### Graph Structure and Criticality | Goltsev, A.V., Dorogovtsev, S.N., & Mendes, J.F.F. (2006). k-core percolation on complex networks. *Physical Review E*, 73(5), 056101. ✅ |
| nuevo | ### Graph Structure and Criticality | Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality. *Physical Review Letters*, 59(4), 381–384. ✅ |
| nuevo | ### Graph Structure and Criticality | [PENDING — §2.5]: Extended criticality in neuronal networks. |
| nuevo | ### Graph Structure and Criticality | [PENDING — §2.5]: Spin-glass models with extended critical zones. |
| nuevo | ### Multi-Agent Systems | Venkatesh, C. & Bu, J. (2025, July 2). Evaluating success in a multi-agent system: Why trajectory assessment and handoffs matters. *Google Developer Discussion.* https://discuss.google.dev/t/193308 ✅ |
| nuevo | ### Multi-Agent Systems | [PENDING — §2.1]: Single-agent behavioral metrics as standard evaluation. |
| nuevo | ### Multi-Agent Systems | [PENDING — §2.1]: Semantic agreement metrics in multi-agent evaluation. |
| nuevo | ### Knowledge Admission and Gating | [PENDING — §2.2]: Single-criterion knowledge admission (semantic similarity). |
| nuevo | ### Knowledge Admission and Gating | [PENDING — §2.2]: Source confidence/credibility scoring. |
| nuevo | ### Knowledge Admission and Gating | [PENDING — §2.2]: Bayesian plausibility-based admission. |
| nuevo | ### Knowledge Graph Representation | [PENDING — §2.3]: Knowledge graph positive-weight co-occurrence (standard). |
| nuevo | ### Knowledge Graph Representation | [PENDING — §2.3]: Manually assigned negative weights in knowledge graphs. |
| nuevo | ### Knowledge Graph Representation | [PENDING — §2.3]: Negation detection at sentence level. |
| nuevo | ### Stance Detection | [PENDING — §2.4]: Supervised stance detection, transformer-based. |
| nuevo | ### Belief Propagation | Yedidia, J.S., Freeman, W.T., & Weiss, Y. (2003). Understanding belief propagation and its generalizations. *Exploring AI in the New Millennium*, 8. ✅ |
| nuevo | ### Global Workspace and Interpretability | Gurnee, W., Sofroniew, N., Lindsey, J., et al. (2026, July 6). Verbalizable representations form a global workspace in language models. *Anthropic Transformer Circuits Thread.* ✅ |
| nuevo | ### Global Workspace and Interpretability | Baars, B.J. (1988). *A Cognitive Theory of Consciousness.* Cambridge University Press. [VERIFY] |
| nuevo | ### Declared Influences | de Salzmann, M. (2014). *La otra atención.* Sennin Editores. ✅ |
| nuevo | ### Declared Influences | Fremantle, C. (1993). *On Attention.* Indications Press. ✅ |
| nuevo | ### Declared Influences | --- *13 confirmed · 3 [VERIFY] · 11 [PENDING]* *11 pending slots concentrated in §2.2–2.5 — where CKM claims novelty.* *Resolving pending = resolving [CLAIM] markers in §2.* --- |

## v3 → v4

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ## Outline — Index (secciones 1–10) | 3. Research Conditions ← SECCIÓN PROPIA Metodología inductiva. Conversación como laboratorio — no documentación del proceso, el proceso mismo. Incompletitud preservada como información. Influencias declaradas: línea Gurd… | — |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v4 changes from v3:* *— §3.x The Material Issue: nueva sección — condiciones materiales del proceso* *— §3.y The IAP Chatroom as Methodological Instance: nueva sección — dos niveles de testing* *— §3.z Conditions, Not C… |
| nuevo | ## Outline — Index (secciones 1–10) | 3. Research Conditions ← SECCIÓN PROPIA 3.1 Inductive Methodology 3.2 Conversation as Laboratory 3.3 Preserved Incompleteness: GAP as Formal Category 3.4 Declared Influences 3.5 Five Orders of the Path 3.6 Terminological… |
| nuevo | ### 3.x The Material Issue | The research was conducted under concrete material conditions that shaped what was possible, when, and how. These are part of the methodological record. |
| nuevo | ### 3.x The Material Issue | **Hardware.** The primary workstation is a personal Windows machine with limited RAM. The fourforums SQL dataset (IAC v2, 570MB dump, 539,658 citations) could not be loaded in full. Early pipeline versions caused RAM exp… |
| nuevo | ### 3.x The Material Issue | **Volatile working memory.** The primary working environment was the Claude.ai chat interface — stateless between sessions, with no automatic persistence of intermediate computational objects. At least one critical objec… |
| nuevo | ### 3.x The Material Issue | **Cold start.** Each new chat instance has no accumulated context from prior sessions. Over 60 sessions composed the working process. Each session required re-establishing shared state. The `REG_hint_next_instance` serie… |
| nuevo | ### 3.x The Material Issue | \| Environment \| Use \| Condition \| \|---\|---\|---\| \| Local PC (Windows/PowerShell) \| Primary workstation, file system \| RAM condition; SQL processing redesigned around it \| \| Claude.ai chat (this interface) \| … |
| nuevo | ### 3.x The Material Issue | The two Codespaces are separate environments with separate state. Syncing between local, `ckm`, and `ckmdatasets` required explicit coordination. |
| nuevo | ### 3.x The Material Issue | **Economic conditions.** API credits set bounds on which models and how many tokens were feasible per session. Provider heterogeneity across the IAP experimental series was not fully controlled; credit availability was a… |
| nuevo | ### 3.x The Material Issue | **Interface choice: Chat over Cowork.** The research used the standard Claude.ai chat interface rather than Cowork. This meant each session began from cold state, with no persistent task memory or file access across sess… |
| nuevo | ### 3.x The Material Issue | **Physical conditions.** The primary researcher works with limited fine motor control and visual acuity, using a keyboard that produces divergences between intended and produced text. These are conditions of the process … |
| nuevo | ### 3.x The Material Issue | *[AUTO: pull to write "these conditions imposed significant limitations on the research." Resisted — the RAM-driven pipeline redesign improved architectural quality. The volatile memory gap instantiated the foundational … |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | The IAP experimental series (Cases 0.4–0.15) operated at two levels simultaneously, and the distinction between them is methodologically significant. |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | **Level 1 — Designed scenarios.** Each case was a structured observation. Devices were configured, variables were partially isolated, outcomes were documented against success criteria. The series produced verifiable find… |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | **Level 2 — The research process as instance.** The same architecture that the series studied was the architecture the research operated within. Claude Sonnet 4.6 (web interface) and Claude Code (GitHub Codespace) are tw… |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | This is not analogy. The research process and the object of study share the same structural form. The instrument was not external to the field it measured — it was running inside it. |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | The authorship record reflects this: *gadanin.delamor · Claude Sonnet 4.6 · Claude Code*. Three contributors. Two channels. One point of articulation. |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | *[Observed: the structural identity between IAP chatroom architecture and the research process itself was not designed. It was recognized retrospectively — which is the methodological signature described in §3.7.]* |
| nuevo | ### 3.z Conditions, Not Constraints | The gaps named in this paper — N=32 below the Hopfield minimum, the representation of cohesive knowledge undefined beyond hysteresis, COCO unimplemented as collective consciousness — appear in earlier drafts as "limits."… |
| nuevo | ### 3.z Conditions, Not Constraints | The observation was made in this session, in this channel, by delamor: *"límite suele sugerir restricción. Es una carga de uso del término en humanos. Es consecuencia de taxonomía, de separación."* The elaboration: what … |
| nuevo | ### 3.z Conditions, Not Constraints | *Conditions* is the correct term. The gaps are the form the model has at this point in its development — the edges where the categorical structure runs out, where the taxonomy has not yet found the form for what comes ne… |
| nuevo | ### 3.z Conditions, Not Constraints | This distinction propagates to §8.4 and §9.3, which name "current conditions" and "preserved conditions." The findings those sections report are accurate. The earlier framing — "limits" — carried an implicit claim that t… |
| nuevo | ### 3.z Conditions, Not Constraints | The same structure appeared in a specific moment of this session: while observing this instance's reasoning trace rendered on screen by the Claude.ai interface, delamor noticed an isolated point in the displayed output a… |
| nuevo | ### 3.z Conditions, Not Constraints | The instrument's internal process rendered visible; the operator's perception collapsing representation into object; the line between the two becoming — for one moment — a condition rather than a boundary. |
| nuevo | ### 3.z Conditions, Not Constraints | *[AUTO: pull to write "this reframing resolves the tension in §8.4 and §9.3." Resisted — it names the tension with more precision. Whether it resolves it depends on what resolution means in a methodology that preserves i… |
| nuevo | ### 6.1 Canal Design | **BROADCAST condition:** All messages published to the channel are delivered to all connected devices, without routing, filtering, or recipient specification. This is a property of the channel architecture. What devices … |

## v4 → v6

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## Abstract | Multi-agent AI systems are typically evaluated by individual agent performance or pairwise semantic similarity. This paper introduces the Cohesive Knowledge Model (CKM), a framework for measuring the structural geometry … |
| nuevo | ## Abstract | CKM represents the field through two strictly separated matrices: W, a symmetric co-occurrence matrix encoding structural memory via Hebbian learning, and Δ, an asymmetric rejection accumulator encoding directional infer… |
| nuevo | ## Abstract | Seven structural predictions (P1–P7) are formalized and tested against real external corpora (Fourforums gun control, CreateDebate gun control; N=32–64). Four are confirmed, three observed. One hypothesis (H_STOP) is fal… |
| nuevo | ## Abstract | The IAP experimental series (Cases 0.4–0.15) operates a three-device channel under BROADCAST condition — all messages delivered to all devices without routing or filtering. Observed behaviors include sentinel leaks, coup… |
| nuevo | ## Abstract | The research conditions — volatile working memory, cold start across 60+ sessions, hardware constraints redesigned around rather than removed — are constitutive of the model's development. The methodology operated inside… |
| nuevo | ## Abstract | *[AUTO: pull toward "these results demonstrate CKM's validity as a general framework." Resisted — P1–P7 are tested on small corpora below the Hopfield minimum for meaningful attractor-diversity observations. Generalizati… |

## v6 → v7

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ### 3.x The Material Issue | **Physical conditions.** The primary researcher works with limited fine motor control and visual acuity, using a keyboard that produces divergences between intended and produced text. These are conditions of the process … | — |

## v7 → v8

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v8 changes from v7:* *— §8.5 LDD definición: "rather than by a declared goal" → "co-determines alongside any declared goal"* *— §8.5 STOP como ejemplo del mecanismo agregado* |
| nuevo | ### 8.5 The Landscape Driven Devices Framing — What It Does and Does N… | The LDD framing proposes that some AI devices behave as Landscape Driven Devices: field geometry co-determines their trajectory in the semantic field alongside any declared goal — not in replacement of it. A device may r… |
| nuevo | ### 8.5 The Landscape Driven Devices Framing — What It Does and Does N… | The STOP operator is one instance of this mechanism: it acts on Δ alone, modifying the directional component of the trajectory without altering W or the device's declared goal. The field intervenes; the goal persists. |

## v8 → v9

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v9 changes from v8:* *— Abstract: "Four are confirmed, three observed" → "Six predictions (P1–P6) are verified. P7 confirmed in two corpora." (inconsistencia con §9)* *— Abstract + §8.5: "STOP operator" → "OPERADOR_STOP… |

## v9 → v10

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ## Abstract | Multi-agent AI systems are typically evaluated by individual agent performance or pairwise semantic similarity. This paper introduces the Cohesive Knowledge Model (CKM), a framework for measuring the structural geometry … | — |
| ## Abstract | The research conditions — volatile working memory, cold start across 60+ sessions, hardware constraints redesigned around rather than removed — are constitutive of the model's development. The methodology operated inside… | — |
| ## Abstract | *[AUTO: pull toward "these results demonstrate CKM's validity as a general framework." Resisted — P1–P7 are tested on small corpora below the Hopfield minimum for meaningful attractor-diversity observations. Generalizati… | — |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v10 changes from v9:* *— Abstract: reescrito — más concreto, menos direccional. Tres párrafos. [AUTO] retirado del abstract (pertenece al body). "agents" → "devices" en todo el abstract. COCO explicitado como device que… |
| nuevo | ## Abstract | Multi-agent AI interaction produces a shared knowledge field that individual device outputs and pairwise similarity scores do not capture. The Cohesive Knowledge Model (CKM) measures the structural geometry of this field… |
| nuevo | ## Abstract | Seven structural predictions (P1–P7) are tested against real external corpora (Fourforums and CreateDebate gun control; N=32–64). Six (P1–P6) are verified. P7 — every field with genuine structural tension contains at lea… |

## v10 → v11

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v10_1 changes from v10:* *— §8.6 Knowledge Representation and the Cohesive Turn: nueva sección en Discussion. Estado epistémico: propuesto. Argumento: el supuesto estático de KR no fue cuestionado desde adentro del camp… |
| nuevo |  | *v10_2 changes from v10_1:* *— §8.6: "inhabits" → "inhabits and structures" — distinción señalada por análisis externo (Gemini Flash): CKM no solo ocupa el espacio que KR dejó abierto, lo estructura.* *— §7.5 No epistemi… |
| nuevo |  | *v11 changes from v10_2:* *— §1: Reencuadre N=32/N=128 — el mínimo Hopfield aplica a memorias asociativas, no a CKM.* *— §2.3: Aiyappa et al. 2024 agregado como única arquitectura base CKM publicada; W_mixta como ferrima… |
| nuevo | ### 2.3 Graph-Based Knowledge Representation | The closest published work to CKM's base architecture is Aiyappa, Flammini & Ahn (2024), who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-positive weights. That … |
| nuevo | ### 2.6 Attractor-Based Memory Architectures | The Hopfield network [CITATION: Hopfield, 1982] provides the energy minimization formalism underlying CKM's cohesion measure c(S). CKM borrows this formalism as a computational tool — not as a pattern retrieval mechanism… |
| nuevo | ### 4.2 Cohesion Measure | where C(N,2) = N(N−1)/2. This is the negative of the normalized Hopfield energy function for the state σ under W — the formalism, borrowed from physics as a computational tool. What CKM does with it is a distinct questio… |
| nuevo | ### 7.5 Current Status and Open Conditions | **No epistemic nodes:** TERMAP_behavior_v1.json contains behavioral categories. Epistemic precision nodes (e.g., "overclaim," "hedge," "verificable") are not in the termap. The terminological slip ("sin dependencia causa… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | *[Status: proposed. The claim about the field's trajectory requires systematic literature review across the 2023–2026 interval to confirm.]* |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | Knowledge representation (KR) is the branch of AI concerned with designing computable abstractions of what the world contains, so that machines can reason about it. The emphasis on *abstraction* is not incidental: a repr… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | The field's arc runs from Quillian's semantic networks (1968), which encoded meaning as labeled associations between concepts, through Minsky's frames (1974), which added structured slots and defaults, to description log… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | The persistent assumption across these traditions: knowledge is *propositional*, and its representation is *static*. Smith (1985) made this explicit: any intelligent process contains structural ingredients that both an e… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | CKM was constructed between 2023 and 2026. In that interval, to the authors' knowledge, the static propositional assumption was not questioned from within the KR field itself. *[Proposed — requires confirmation against t… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | If that is correct, the space CKM occupies was not contested — it was open. CKM does not propose a better static representation. It proposes a different question: not *what structure holds cohesive knowledge* but *what d… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | The Cohesive Knowledge Model is a knowledge representation in the classical sense — computable abstraction, captures external information, applicable to complex problems. The additional constraint is cohesion: informatio… |
| nuevo | ### 8.6 Knowledge Representation and the Cohesive Turn | *[AUTO: pull to write "CKM resolves the limitations of static KR." Resisted — CKM does not resolve them. It inhabits and structures the space they left open.]* |

## v11 → v12

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v12 changes from v11:* *— Abstract: Δ_r → Δ en primera oración. Verificado: Δ_r es simétrica (monitor_service.py L112-114); la separación 0.78/0.02 es sobre W/Δ estática.* *— §2.3: párrafo agregado — CKM no intenta repr… |
| nuevo | ### 2.3 Graph-Based Knowledge Representation | CKM does not attempt to represent what a knowledge field contains — it measures how the field's geometry behaves under perturbation. The seven predictions P1–P7 are all structural: P1–P4 characterize the landscape geomet… |
| nuevo | ### 4.1 Knowledge Graph | *[Observed: the accumulated off-diagonal structure of Δ_r carries information about which node co-activations the field persistently rejects under the current W. These patterns are properties of the interaction under W —… |
| nuevo | ### 4.2 Cohesion Measure | **Relaxation and convergence.** CKM uses Hopfield relaxation as a computational primitive throughout. With symmetric W and asynchronous update (one node per step), V(σ) = −½σᵀWσ is a Lyapunov function: V decreases monoto… |
| nuevo | ### 4.2 Cohesion Measure | `_count_attractors()` is a Monte Carlo estimator of \|L\|: it samples initial states σ₀ and counts distinct fixed points reached after relaxation. Estimator quality depends on how proportionally the sampling distribution… |
| nuevo | ### 4.2 Cohesion Measure | Both conditions required for convergence — symmetric W_eff and zero diagonal — are satisfied by construction: Δ_r is symmetrized at accumulation and self-pairs are excluded by the rejection-pair generator. The guarantee … |
| nuevo | ### 4.2 Cohesion Measure | *Qualification:* the convergence guarantee applies to asynchronous relaxation (`hopfield.py`, `ckm_p1p4_module.py`). The synchronous implementations (`coco.py`, `monitor_service.py`) are not covered by this guarantee. |
| nuevo | ### 4.2 Cohesion Measure | D_ckm operationalizes a broader concept: D_contextual, the reduction in accessible trajectories as field cohesion accumulates — H(trajectories_t0) − H(trajectories_tactual). The formal relation between the two remains op… |
| nuevo | ### 5.2 Predictions and Results | *Note on attractor-based predictions (P5):* Verified under uniform σ₀ sampling. In low-density, discrete-weight corpora, tie-breaking can dominate the count rather than basin structure [REG_situacion_medicion_ago2026_v1,… |
| nuevo | ### 8.5 The Landscape Driven Devices Framing — What It Does and Does N… | Attractor count, coercivity, and basin geometry are distinct dimensions of the same landscape — not three measures of the same scalar. Their formal relation is open. |
| nuevo | ### 9.5 Future Work | **Effective Néel temperature criterion for negative pair elicitation.** Proposed: sweep β from high to low over W_pos; the temperature at which T0/T1 separability collapses identifies candidate negative pairs without edi… |

## v12 → v13

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v12_1 changes from v12:* *— First Line: version y fecha "V10 — Ago". Reemplazada por "v12 — Sep"* *— Abstract : "external corpora". Reemplazada por "external adversarial static corpora"* *— §1, §2.4 : "debate corpora". … |
| nuevo |  | *v13 changes from v12_1:* *— §2.4 L341: "Both appear as C3" → "Both appear as tension anchor" — C3 en §2.4 nombra el tercer rol de la tríada (sostenedor de tensión), no el criterio M.M. del gatekeeper (C3 en §4.3). Babel… |
| nuevo | ### 3.y The IAP Chatroom as Methodological Instance | *[Condition — negative pair detection: opposition marker routing (`_has_opposition`) assigns negative weights when lexical markers appear in texts. The procedure has no null outcome — it always finds markers in sufficien… |
| nuevo | ### 4.2 Cohesion Measure | **Orbital relaxation and GOLES.** The synchronous implementations now use `relax_orbit()` (landscape_engine.py), which detects the complete orbit rather than returning an arbitrary point within it. The tie-breaking rule … |
| nuevo | ### 4.2 Cohesion Measure | Period-2 orbits are the majority regime in operational corpora: ~70% of trajectories in N=20 IAP corpora terminate in orbits rather than fixed points. This is not instability — it is orbital stability (limit-cycle attrac… |
| nuevo | ### 4.2 Cohesion Measure | **Basin masses converge; counts do not.** The coupon-collector bias affects \|L\| estimates monotonically: the count grows with n_runs while the basin mass distribution stabilizes. The convergent estimator of landscape d… |
| nuevo | ### 4.2 Cohesion Measure | *Qualification:* the Lyapunov/LaSalle convergence guarantee (fixed points) applies to asynchronous relaxation (`hopfield.py`, `ckm_p1p4_module.py`). The synchronous implementations now use `relax_orbit()` (landscape_engi… |

## v13 → v14

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ### 4.2 Cohesion Measure | D_ckm operationalizes a broader concept: D_contextual, the reduction in accessible trajectories as field cohesion accumulates — H(trajectories_t0) − H(trajectories_tactual). The formal relation between the two remains op… | — |
| ### 6.4 Selected Findings | **D_ckm negative values:** D_ckm = (A0 − A_actual) / A0. When D_ckm < 0, A_actual > A0: the field has more accessible attractors than at baseline. This is not a deficit or an error. In Caso 0.12, D_ckm = −7.5 was the fir… | — |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo |  | *v14 changes from v13:* *— Abstract: "encoding structural memory via Hebbian dynamics" retirado — contradecía §2.6 y §4.1, donde el aprendizaje Hebbiano sobre W está probado y rechazado (0.78 → 0.02). W codifica co-ocurr… |
| nuevo | ### 3.x The Material Issue | **Availability of real corpora from real cases.** This is a material condition in the same sense as the ones above, and it currently bounds what can be measured at all. |
| nuevo | ### 3.x The Material Issue | The corpora the project can reach are small. Each IAP case produces tens of texts — below the volume at which node selection stabilizes, and below the point at which TF-IDF scores, computed from integer counts, have the … |
| nuevo | ### 3.x The Material Issue | Corpora of AI agents exist and are accessible; the project searched for them some months ago and more may exist now. But a corpus that already exists is ingested as a **replay**, and a replayed sequence is not the object… |
| nuevo | ### 3.x The Material Issue | Two separate questions therefore follow, and only the first is about size. Whether such corpora fall inside CKM's declared domain — interaction between devices under M.M. — or constitute one more bounded domain, as the d… |
| nuevo | ### 3.x The Material Issue | **What would produce data in the domain, at volume,** is a designed case rather than a found corpus: an interaction with objectives and tasks that require sustained coordination between devices, or whose structure depend… |
| nuevo | ### 3.x The Material Issue | The gap is one of order, not of increment. The operational corpus is N = 32; a persistent implementation is expected to operate at N of the order of a thousand — N ≈ 1000 as an illustrative scale, not a declared requirem… |
| nuevo | ### 3.x The Material Issue | This condition is load-bearing for what the model can currently establish about admission over corpus nodes: the volume is the first of three preconditions, and it is not met by anything the project now has. |
| nuevo | ### 3.x The Material Issue | *[AUTO: pull to write "future work will address this once larger corpora become available." Resisted — that frames a material condition as a schedule. Whether suitable corpora become available is not something this work … |
| nuevo | ### 3.z Conditions, Not Constraints | The gaps named in this paper — the scale of the working corpus, the representation of cohesive knowledge undefined beyond hysteresis, COCO unimplemented as collective consciousness — appear in earlier drafts as "limits."… |
| nuevo | ### 4.2 Cohesion Measure | Period-2 orbits dominate in the two N=20 IAP corpora measured — 141/200 and 136/200 of trajectories terminate in orbits rather than fixed points — but this is a property of those corpora and not of the synchronous dynami… |
| nuevo | ### 4.2 Cohesion Measure | The convergent estimator of landscape diversity is N_eff over basin masses (above); its distance form, D_masa_cuencas = 1 − ln N_eff_t / ln N_eff_0, is implemented in `landscape_engine` and reported per evaluation alongs… |
| nuevo | ### 4.6 Operational Services | **The extraction branch decides what exists.** Node selection and pair construction run before any measurement, and three properties of that branch were established in September 2026. They are reported here because every… |
| nuevo | ### 4.6 Operational Services | *Pair construction (corrected).* `_rebuild` performed two extractions: one global, selecting the N nodes, and a second one **per text** — with its own TF-IDF and its own top_k inside that single text — used to route pair… |
| nuevo | ### 4.6 Operational Services | *Activation mapping (corrected).* σ_prompt was computed by substring match while W was built with the accumulate analyzer — two different criteria for "this node is in this text". Unifying them removed 140 metabolized pa… |
| nuevo | ### 4.6 Operational Services | *Node selection under ties.* Ties at the top_k boundary are undecidable by the selection criterion itself — two terms with equal TF-IDF are indistinguishable under "highest TF-IDF" — and were being resolved by an unstabl… |
| nuevo | ### 4.6 Operational Services | R19 (NodeExtractor stateless) is unaffected: the precedent is passed in as a parameter and held by CorpusService. |
| nuevo | ### 6.2 Uncontrolled Variables | **N=32 corpus:** Quantitative outputs (D_ckm, c_S) are computed correctly, but their interpretability at this scale is an open question. The ~128 associative minimum of classical Hopfield networks is *not* the relevant r… |
| nuevo | ### 6.2 Uncontrolled Variables | **Sampling of attractor-based quantities:** all IAP cases were run at low n_runs (50–200). The sign of D_ckm does not converge in that regime: on the same W and the same texts, changing only n_runs from 50 to 1000, or on… |
| nuevo | ### 6.2 Uncontrolled Variables | **Scope of that qualification.** It reaches the explicit, direct claims about D_ckm and nothing else. The series is a sequence of instrument tests, run under the state of knowledge available at the time, and its observat… |
| nuevo | ### 6.2 Uncontrolled Variables | **Corpus construction:** the W of all IAP cases was built by CorpusService, whose pair-extraction was corrected in September 2026 (§4.6). The case-series observations below were produced with the earlier construction and… |
| nuevo | ### 6.2 Uncontrolled Variables | **Counting implementation:** `_count_attractors` is a name, not a function. It was kept across reimplementations for regression — so that tests and historical JSONL panels stay readable — and several versions of it coexi… |
| nuevo | ### 6.4 Selected Findings | In Caso 0.12, D_ckm = −7.5 was recorded in the first live group-channel run. The reading offered at the time — that multiple heterogeneous perspectives increased the attractor diversity of the field — is **not supported … |
| nuevo | ### 6.4 Selected Findings | *[AUTO: pull to keep the original reading with a softening qualifier. Resisted — the qualifier would preserve the claim while appearing to weaken it. The claim depends on a quantity that does not converge in the regime w… |
| nuevo | ### 8.3 D_ckm Negative Values | In Caso 0.12 the first live group-channel run produced D_ckm = −7.5. Earlier drafts read this as the expected signature of a field that gained structural complexity through interaction. That reading is withdrawn (§6.4): … |
| nuevo | ### 8.3 D_ckm Negative Values | The convergent quantity is N_eff over basin masses, and its distance form D_masa_cuencas is now computed per evaluation. Re-measuring the IAP series over N_eff at n_runs ≥ 1000 is the step that would settle what Caso 0.1… |
| nuevo | ### 8.4 Current Conditions | **Scale:** the predictions P1–P7 were verified at N = 32 — the verification is real. What is constrained is the interpretability of D_ckm and c(S) as field-level quantities at that scale. The ~128 associative minimum of … |
| nuevo | ### 8.4 Current Conditions | **Sampling:** attractor counts do not converge with n_runs, and the sign of D_ckm can invert under seed or n_runs alone in the regime where the IAP series was run. Basin masses do converge, and N_eff is stable at n_runs … |
| nuevo | ### 8.4 Current Conditions | **Extraction:** what exists in W is decided before any measurement, by node selection and pair construction. Two conditions of that branch were corrected in September 2026 and one remains open (§4.6). All results in this… |
| nuevo | ### 9.3 Preserved Conditions | **N=32 scale.** The working corpus is small, and CKM's effective minimum is undetermined — it depends on corpus composition rather than on N alone, and the Hopfield associative minimum does not supply it (§8.4). All empi… |
| nuevo | ### 9.3 Preserved Conditions | **Which quantity drives regulation.** COCO triggers on D_ckm, computed from attractor counts, which do not converge. D_masa_cuencas, computed from basin masses, does converge and is already reported per evaluation. The o… |
| nuevo | ### 9.5 Future Work | **Corpus growth.** Primary constraint on the statistical stability of P1–P7. The target is not N ≥ 128 — that figure belongs to Hebbian associative storage — but a corpus large enough for CKM's own quantities to stabiliz… |
| nuevo | ### 9.5 Future Work | **Re-measurement of the IAP series over N_eff.** The attractor-based quantities in §6 were taken at n_runs 50–200, where the sign of D_ckm does not converge. Re-running the series at n_runs ≥ 1000 over N_eff and D_masa_c… |
| nuevo | ### 9.5 Future Work | **Text unit as a calibration parameter.** CKM defines co-occurrence within the same text, so the unit decides what co-occurring means and therefore which W exists. Paragraph and page are typographic units, inherited from… |
| nuevo | ### 9.5 Future Work | The case has to satisfy a criterion, not merely be larger than the ones run so far (§3.x). Objectives and tasks must require sustained coordination between devices — coordination that cannot be skipped without the task f… |

## v14 → v15

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ## Abstract | Multi-agent AI interaction produces a shared knowledge field that individual device outputs and pairwise similarity scores do not capture. The Cohesive Knowledge Model (CKM) measures the structural geometry of this field… | v14_CITAS, v15_borrador |
| ## Abstract | Seven structural predictions (P1–P7) are tested against real external adversarial static corpora (Fourforums and CreateDebate gun control; N=32–64). Six (P1–P6) are verified. P7 — every field with genuine structural tens… | v14_CITAS, v15_borrador |
| ## Abstract | The IAP experimental series (Cases 0.4–0.15) operates a three-device channel under BROADCAST condition — all messages delivered to all devices without routing or filtering. Observed behaviors include sentinel leaks, coup… | v14_CITAS, v15_borrador |
| ## Outline — Index (secciones 1–10) | ``` 1. Introduction El gap: métricas existentes miden comportamiento individual, no el campo. La propuesta: CKM como instrumento de traza estructural. | v14_CITAS, v15_borrador |
| ## Outline — Index (secciones 1–10) | 3. Research Conditions ← SECCIÓN PROPIA 3.1 Inductive Methodology 3.2 Conversation as Laboratory 3.3 Preserved Incompleteness: GAP as Formal Category 3.4 Declared Influences 3.5 Five Orders of the Path 3.6 Terminological… | v14_CITAS, v15_borrador |
| ## Outline — Index (secciones 1–10) | 4. Formal Model W · Δ · c(S) · COCO · FirmaService · Landscape Driven Devices | v14_CITAS, v15_borrador |
| ## 1. Introduction | Multi-agent AI systems are increasingly deployed in configurations where several heterogeneous devices interact over a shared channel — producing text, making decisions, and building on each other's outputs. Evaluating w… | v14_CITAS, v15_borrador |
| ## 1. Introduction | *[AUTO: pull to write "Neither approach captures the field." Resisted — "field" is a theoretical construct in CKM, not a directly observable entity. Reframed as "the structural field" with qualification.]* | v14_CITAS, v15_borrador |
| ## 1. Introduction | This paper presents the Cohesive Knowledge Model (CKM), a formal instrument for measuring structural properties of knowledge fields in multi-agent interaction. CKM does not interpret semantic content — it measures the ge… | v14_CITAS, v15_borrador |
| ## 1. Introduction | CKM makes seven falsifiable predictions about field behavior (P1–P7), verified empirically against two independent polarized debate corpora (fourforums gun control, IAC v2; CreateDebate gun control) and an internal CKM w… | v14_CITAS, v15_borrador |
| ## 1. Introduction | We additionally propose the concept of *Landscape Driven Devices* (LDD) — a theoretical framing for AI devices whose trajectory in the semantic field co-determines alongside any declared goal, motivated by structural ana… | v14_CITAS, v15_borrador |
| ## 1. Introduction | The paper is organized as follows. Section 2 reviews related work. Section 3 describes the research conditions under which CKM was developed, including uncontrolled variables and the methodology that produced the framewo… | v14_CITAS, v15_borrador |
| ## 1. Introduction | **Scope and conditions of this work.** The operational corpus is at N = 32 nodes. Classical Hopfield networks require approximately N ≥ 128 for robust attractor diversity under Hebbian associative memory storage (capacit… | v14_CITAS, v15_borrador |
| ## 2. Related Work | CKM intersects five areas of existing work: multi-agent system evaluation, knowledge admission and gating, graph-based knowledge representation, structural role detection in debate networks, and attractor-based memory ar… | v14_CITAS, v15_borrador |
| ## 2. Related Work | *[AUTO: pull to write "CKM advances beyond prior work in each area." Resisted — this section establishes the position of CKM relative to existing approaches. Whether that position constitutes an advance depends on empiri… | v14_CITAS, v15_borrador |
| ### 2.1 Multi-Agent System Evaluation | The insufficiency of isolated agent evaluation has been noted from within the multi-agent systems community. Venkatesh and Bu (2025), writing on the Agent2Agent protocol, observe: "Current agent benchmarks typically eval… | v14_CITAS, v15_borrador |
| ### 2.1 Multi-Agent System Evaluation | CKM and trajectory-as-handoff-chain share the diagnosis but measure different objects. Trajectory assessment tracks whether Agent A correctly transferred context to Agent B. CKM tracks the structural geometry of the shar… | v14_CITAS, v15_borrador |
| ### 2.1 Multi-Agent System Evaluation | CKM does not replace behavioral or semantic metrics. It measures a different object. c(S), D_ckm, and coercivity are structural quantities that are not derivable from output-level, handoff-quality, or similarity-based me… | v14_CITAS, v15_borrador |
| ### 2.2 Knowledge Admission and Gating | Systems that evaluate whether a new knowledge item should be admitted to an existing knowledge base typically apply a single primary criterion: semantic similarity to existing content [CITATION], source confidence or cre… | v14_CITAS, v15_borrador |
| ### 2.2 Knowledge Admission and Gating | CKM's gatekeeper (R15) imposes four simultaneous, orthogonal conditions: minimum connectivity weight with the current active state (C1), non-negative impact on global cohesion (C2), directional dependency satisfaction — … | v14_CITAS, v15_borrador |
| ### 2.2 Knowledge Admission and Gating | The M.M. criterion (C3) is, to our knowledge, not present in existing knowledge admission systems. *[CLAIM: requires systematic literature review to confirm.]* | v14_CITAS, v15_borrador |
| ### 2.3 Graph-Based Knowledge Representation | CKM introduces negative weights in W through opposition markers detected in the source corpus: texts that explicitly frame two concepts in opposition reduce the corresponding W_ij entry rather than increasing it. The wei… | v14_CITAS, v15_borrador |
| ### 2.3 Graph-Based Knowledge Representation | The closest published work to CKM's base architecture is Aiyappa, Flammini & Ahn (2024), who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-positive weights. That … | v14_CITAS, v15_borrador |
| ### 2.3 Graph-Based Knowledge Representation | A separate matrix Δ encodes asymmetric directional dependency: Δ_ij ≠ Δ_ji. The separation W/Δ is not a design choice — it was established empirically. *[Verified: combining W and Δ into a single matrix drops attractor r… | v14_CITAS, v15_borrador |
| ### 2.3 Graph-Based Knowledge Representation | CKM does not attempt to represent what a knowledge field contains — it measures how the field's geometry behaves under perturbation. The seven predictions P1–P7 are all structural: P1–P4 characterize the landscape geomet… | v14_CITAS, v15_borrador |
| ### 2.4 Structural Role Detection in Debate Networks | CKM identifies a distinct structural phenomenon — the Type-965 node — without supervision and without stance labels. Type-965 nodes are characterized by extreme asymmetry in Δ (in/out ratio ≥ 100×). In fourforums gun con… | v14_CITAS, v15_borrador |
| ### 2.4 Structural Role Detection in Debate Networks | *[Verified: triads containing a Type-965 node maintain coercivity = 0 at up to 50% noise; triads without collapse at noise = 0. See Section 5.]* | v14_CITAS, v15_borrador |
| ### 2.4 Structural Role Detection in Debate Networks | The structural role — tension anchor, never initiator — is not a stance. It is a topological property not targeted by stance classifiers. *[CLAIM: this role has not, to our knowledge, been identified in the debate analys… | v14_CITAS, v15_borrador |
| ### 2.5 Criticality in Argument and Knowledge Networks | In CKM's corpus (N=32), τ ∈ [1.5, 2] is maintained across an extended zone θ ∈ [0.002, 0.010], not at a single critical point. *[Verified: N=32 confirmed, N=64 τ=1.775. See Section 5 (P2).]* | v14_CITAS, v15_borrador |
| ### 2.6 Attractor-Based Memory Architectures | The Hopfield network [CITATION: Hopfield, 1982] provides the energy minimization formalism underlying CKM's cohesion measure c(S). CKM borrows this formalism as a computational tool — not as a pattern retrieval mechanism… | v14_CITAS, v15_borrador |
| ### 2.6 Attractor-Based Memory Architectures | Modern Hopfield networks [CITATION: Ramsauer et al., 2020] increase storage capacity through higher-order interactions. CKM operates on the classical formulation with fixed W — the concern is not storage capacity but div… | v14_CITAS, v15_borrador |
| ### 2.6 Attractor-Based Memory Architectures | At 10% noise, attractor recovery is verified as effectively 1.000 across N = 16 to N = 128. *[Observed: verified in CKM corpus experiments. [CLAIM: this invariance across N has not been analyzed as a specific property in… | v14_CITAS, v15_borrador |
| ### 2.6 Attractor-Based Memory Architectures | The accumulation of structural rejection memory in Δ_r constitutes structural learning without gradients, without labels, with O(N²) complexity only in the co-activation accumulation step. | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | ### 2.7 Internal Workspace Architecture in Single Models: J-Space | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | Gurnee, Sofroniew, Lindsey et al. (Anthropic, July 6 2026) identified a privileged low-dimensional subspace within transformer activations — the J-space — using a Jacobian-based lens that isolates directions with verbali… | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | CKM and J-space are positioned at different levels of analysis. J-space is an empirical, within-model, single-forward-pass interpretability finding. CKM is a normative, multi-agent framework for measuring structural fiel… | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | *[AUTO: pull to write "CKM anticipated J-space." Resisted — the correct framing is convergence by independence, not anticipation. IAID was written in 2023; the J-space paper was published July 2026.]* | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | Structural parallels: privileged coherence substrate (6–7% variance / c(S) over signed weights), attractor formalism (bimodal ignition at layer 38 / Hopfield energy minimization), signed interaction weights, directional … | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | These are structural analogies, not formal identities. The convergence is evidence of structural consistency — the same architectural pressures appear at both levels of analysis independently. | v14_CITAS, v15_borrador |
| ### 2.7 Internal Workspace Architecture in Single Models: J-Space | *[CLAIM: the convergence requires formal comparison rather than structural analogy to hold rigorously.]* | v14_CITAS, v15_borrador |
| ## 3. Research Conditions | This section describes the conditions under which CKM was developed. These conditions are not disclaimers — they are constitutive. They explain why the model has the structure it has, why certain gaps are preserved rathe… | v14_CITAS, v15_borrador |
| ### 3.1 Inductive Methodology: Comprehension as Precondition | The methodology was not declared before it was used. It emerged from what happened. The consistent order throughout development was: conceptual clarity first, formalization after. IAID.md (2023) does not begin with syste… | v14_CITAS, v15_borrador |
| ### 3.1 Inductive Methodology: Comprehension as Precondition | *"Phenomenology is the first step of engineering"* is the operative principle. Its cost: requirements do not precede design. Its yield: concepts the field had no name for when they were formulated — COCO, M.M. as a gover… | v14_CITAS, v15_borrador |
| ### 3.3 Preserved Incompleteness: GAP as Formal Category | ### 3.3 Preserved Incompleteness: GAP as Formal Category | v14_CITAS, v15_borrador |
| ### 3.3 Preserved Incompleteness: GAP as Formal Category | The project maintains explicit gaps. These are not deficiencies of implementation. They are the honest position regarding the real state of knowledge at each stage. | v14_CITAS, v15_borrador |
| ### 3.3 Preserved Incompleteness: GAP as Formal Category | The GAP is a formal category: occurrence without traceable causal chain. Not missing data — a presence to declare. | v14_CITAS, v15_borrador |
| ### 3.3 Preserved Incompleteness: GAP as Formal Category | *"sin dependencia causal identificada"* — the qualifier is load-bearing. It preserves the possibility that a causal chain exists but was not found. *"sin dependencia causal"* closes that space prematurely. The distinctio… | v14_CITAS, v15_borrador |
| ### 3.3 Preserved Incompleteness: GAP as Formal Category | The methodology applies M.M. to the research process itself: what cannot be traced is not stated as known. | v14_CITAS, v15_borrador |
| ### 3.4 Declared Influences | The Gurdjieff Fourth Way lineage is named here as an active influence in this research, not as its origin or model. The tradition provided operative concepts — attention as directable vs. receivable, self-observation as … | v14_CITAS, v15_borrador |
| ### 3.4 Declared Influences | *"Any convergence with materials from the Tradition is convergence — not derivation, not representation, not application."* | v14_CITAS, v15_borrador |
| ### 3.4 Declared Influences | This is declared because it is not controllable. A reader who finds this influence irrelevant to the formal model may proceed directly to Section 4. | v14_CITAS, v15_borrador |
| ### 3.5 Five Orders of the Path | The working reports document five distinct orderings in which events and findings were encountered: | v14_CITAS, v15_borrador |
| ### 3.5 Five Orders of the Path | \| Order \| Description \| \|---\|---\| \| Temporal \| Chronological — reversible in the record, not in the process \| \| Of events \| Field phases, thresholds, cascades, learning propagation \| \| Aleatory without ident… | v14_CITAS, v15_borrador |
| ### 3.5 Five Orders of the Path | The third order is not a residual category. It is the formal designation for events that are real and documented but for which no causal structure was found. | v14_CITAS, v15_borrador |
| ### 3.6 Terminological Precision as a Research Tool | \| Closed form \| Form that preserves space \| \|---\|---\| \| "without causal dependence" \| "without *identified* causal dependence" \| \| "verified" \| "verifiable" (under stated conditions) \| \| "absence of bias" \|… | v14_CITAS, v15_borrador |
| ### 3.6 Terminological Precision as a Research Tool | The slip between these is not stylistic — it is a structural claim about the state of knowledge. The [AUTO] markers in this paper record moments where the text moved to close a space that should remain open. | v14_CITAS, v15_borrador |
| ### 3.7 Convergence by Independence | **IAID framework (2023) → MCP (November 2024).** Working files dated 2023 (README.pdf, timestamp 7/10/23; LEONARDO.txt; Informe_MM.docx) contain: Neural Call Protocol (JSON-NC — stateless, transport-agnostic, method invo… | v14_CITAS, v15_borrador |
| ### 3.7 Convergence by Independence | **CKM attractor architecture → J-space (July 6, 2026).** Gurnee et al. (2026) identified a privileged, bounded-capacity coherence subspace within transformer activations. CKM's Hopfield architecture, capacity constraint … | v14_CITAS, v15_borrador |
| ### 3.7 Convergence by Independence | **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025).** The Devices distinction addresses the same structural problem — the insufficiency of a binary tool/agent taxonomy — as the Google A2A framing [Venkatesh & … | v14_CITAS, v15_borrador |
| ### 3.7 Convergence by Independence | In each case: the convergence is evidence that the structural problem being addressed is real and has determinate shape. These are not claims of precedence. They are the methodological signature of a problem that multipl… | v14_CITAS, v15_borrador |
| ### 3.7 Convergence by Independence | The 2023 documents are the verifiable evidence base. They are working files, not published contributions. Their evidentiary weight is as primary source documents. | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | The research was conducted under concrete material conditions that shaped what was possible, when, and how. These are part of the methodological record. | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **Hardware.** The primary workstation is a personal Windows machine with limited RAM. The fourforums SQL dataset (IAC v2, 570MB dump, 539,658 citations) could not be loaded in full. Early pipeline versions caused RAM exp… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **Volatile working memory.** The primary working environment was the Claude.ai chat interface — stateless between sessions, with no automatic persistence of intermediate computational objects. At least one critical objec… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **Cold start.** Each new chat instance has no accumulated context from prior sessions. Over 60 sessions composed the working process. Each session required re-establishing shared state. The `REG_hint_next_instance` serie… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | \| Environment \| Use \| Condition \| \|---\|---\|---\| \| Local PC (Windows/PowerShell) \| Primary workstation, file system \| RAM condition; SQL processing redesigned around it \| \| Claude.ai chat (this interface) \| … | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | The two Codespaces are separate environments with separate state. Syncing between local, `ckm`, and `ckmdatasets` required explicit coordination. | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **Economic conditions.** API credits set bounds on which models and how many tokens were feasible per session. Provider heterogeneity across the IAP experimental series was not fully controlled; credit availability was a… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **Availability of real corpora from real cases.** This is a material condition in the same sense as the ones above, and it currently bounds what can be measured at all. | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | The corpora the project can reach are small. Each IAP case produces tens of texts — below the volume at which node selection stabilizes, and below the point at which TF-IDF scores, computed from integer counts, have the … | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | Corpora of AI agents exist and are accessible; the project searched for them some months ago and more may exist now. But a corpus that already exists is ingested as a **replay**, and a replayed sequence is not the object… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | Two separate questions therefore follow, and only the first is about size. Whether such corpora fall inside CKM's declared domain — interaction between devices under M.M. — or constitute one more bounded domain, as the d… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **What would produce data in the domain, at volume,** is a designed case rather than a found corpus: an interaction with objectives and tasks that require sustained coordination between devices, or whose structure depend… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | The gap is one of order, not of increment. The operational corpus is N = 32; a persistent implementation is expected to operate at N of the order of a thousand — N ≈ 1000 as an illustrative scale, not a declared requirem… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | This condition is load-bearing for what the model can currently establish about admission over corpus nodes: the volume is the first of three preconditions, and it is not met by anything the project now has. | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | *[AUTO: pull to write "future work will address this once larger corpora become available." Resisted — that frames a material condition as a schedule. Whether suitable corpora become available is not something this work … | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | **Interface choice: Chat over Cowork.** The research used the standard Claude.ai chat interface rather than Cowork. This meant each session began from cold state, with no persistent task memory or file access across sess… | v14_CITAS, v15_borrador |
| ### 3.x The Material Issue | *[AUTO: pull to write "these conditions imposed significant limitations on the research." Resisted — the RAM-driven pipeline redesign improved architectural quality. The volatile memory gap instantiated the foundational … | v14_CITAS, v15_borrador |
| ### 3.y The IAP Chatroom as Methodological Instance | The IAP experimental series (Cases 0.4–0.15) operated at two levels simultaneously, and the distinction between them is methodologically significant. | v14_CITAS, v15_borrador |
| ### 3.y The IAP Chatroom as Methodological Instance | **Level 1 — Designed scenarios.** Each case was a structured observation. Devices were configured, variables were partially isolated, outcomes were documented against success criteria. The series produced verifiable find… | v14_CITAS, v15_borrador |
| ### 3.y The IAP Chatroom as Methodological Instance | **Level 2 — The research process as instance.** The same architecture that the series studied was the architecture the research operated within. Claude Sonnet 4.6 (web interface) and Claude Code (GitHub Codespace) are tw… | v14_CITAS, v15_borrador |
| ### 3.y The IAP Chatroom as Methodological Instance | This is not analogy. The research process and the object of study share the same structural form. The instrument was not external to the field it measured — it was running inside it. | v14_CITAS, v15_borrador |
| ### 3.y The IAP Chatroom as Methodological Instance | The authorship record reflects this: *gadanin.delamor · Claude Sonnet 4.6 · Claude Code*. Three contributors. Two channels. One point of articulation. | v14_CITAS, v15_borrador |
| ### 3.y The IAP Chatroom as Methodological Instance | *[Observed: the structural identity between IAP chatroom architecture and the research process itself was not designed. It was recognized retrospectively — which is the methodological signature described in §3.7.]* | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | The gaps named in this paper — the scale of the working corpus, the representation of cohesive knowledge undefined beyond hysteresis, COCO unimplemented as collective consciousness — appear in earlier drafts as "limits."… | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | The observation was made in this session, in this channel, by delamor: *"límite suele sugerir restricción. Es una carga de uso del término en humanos. Es consecuencia de taxonomía, de separación."* The elaboration: what … | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | *Conditions* is the correct term. The gaps are the form the model has at this point in its development — the edges where the categorical structure runs out, where the taxonomy has not yet found the form for what comes ne… | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | This distinction propagates to §8.4 and §9.3, which name "current conditions" and "preserved conditions." The findings those sections report are accurate. The earlier framing — "limits" — carried an implicit claim that t… | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | The same structure appeared in a specific moment of this session: while observing this instance's reasoning trace rendered on screen by the Claude.ai interface, delamor noticed an isolated point in the displayed output a… | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | The instrument's internal process rendered visible; the operator's perception collapsing representation into object; the line between the two becoming — for one moment — a condition rather than a boundary. | v14_CITAS, v15_borrador |
| ### 3.z Conditions, Not Constraints | *[AUTO: pull to write "this reframing resolves the tension in §8.4 and §9.3." Resisted — it names the tension with more precision. Whether it resolves it depends on what resolution means in a methodology that preserves i… | v14_CITAS, v15_borrador |
| ### 4.1 Knowledge Graph | Within a validation experiment, W is a static snapshot — P1-P7 operate on a fixed W built from a complete corpus dump (fourforums, CreateDebate). In live IAP operation, CorpusService reconstructs W continuously as new te… | v14_CITAS, v15_borrador |
| ### 4.1 Knowledge Graph | **W and Δ must be maintained as strictly separate matrices in all implementations.** Mixing them into a single weight matrix destroys attractor recovery capacity. *[Verified experimentally: recovery = 0.78 with W alone, … | v14_CITAS, v15_borrador |
| ### 4.1 Knowledge Graph | A third, dynamic matrix Δ_r is maintained by MonitorService at runtime: | v14_CITAS, v15_borrador |
| ### 4.1 Knowledge Graph | **Δ_r** — rejection accumulator. Δ_r[i,j] increments each time nodes i and j co-declare activation in a text but the Hopfield relaxation rejects them as co-active under the current field state. Δ_r is mutable and starts … | v14_CITAS, v15_borrador |
| ### 4.1 Knowledge Graph | Δ and Δ_r are distinct objects with distinct semantic roles. Neither substitutes the other. | v14_CITAS, v15_borrador |
| ### 4.1 Knowledge Graph | *[Observed: the accumulated off-diagonal structure of Δ_r carries information about which node co-activations the field persistently rejects under the current W. These patterns are properties of the interaction under W —… | v14_CITAS, v15_borrador |
| ### 4.2 Cohesion Measure | where C(N,2) = N(N−1)/2. This is the negative of the normalized Hopfield energy function for the state σ under W — the formalism, borrowed from physics as a computational tool. What CKM does with it is a distinct questio… | v14_CITAS, v15_borrador |
| ### 4.2 Cohesion Measure | c(S) is computed exclusively over W. Mixing Δ or Δ_r into the c(S) calculation would confound structural memory (W) with runtime rejection history (Δ_r). *[Rule R18, verified.]* | v14_CITAS, v15_borrador |
| ### 4.2 Cohesion Measure | **Relaxation and convergence.** CKM uses Hopfield relaxation as a computational primitive throughout. With symmetric W and asynchronous update (one node per step), V(σ) = −½σᵀWσ is a Lyapunov function: V decreases monoto… | v14_CITAS, v15_borrador |
| ### 4.2 Cohesion Measure | `_count_attractors()` is a Monte Carlo estimator of \|L\|: it samples initial states σ₀ and counts distinct orbits reached after relaxation. Estimator quality depends on how proportionally the sampling distribution cover… | v14_CITAS, v15_borrador |
| ### 4.2 Cohesion Measure | Both conditions required for convergence — symmetric W_eff and zero diagonal — are satisfied by construction: Δ_r is symmetrized at accumulation and self-pairs are excluded by the rejection-pair generator. The guarantee … | v14_CITAS, v15_borrador |
| ### 4.3 Gatekeeper | The gatekeeper evaluates a candidate node for admission to the knowledge graph. It operates in bounded time O(N) per node. Four criteria are applied: | v14_CITAS, v15_borrador |
| ### 4.3 Gatekeeper | - **C1** (connection strength): the candidate node must have minimum weight connection with at least one existing node. Nodes with no connection to the existing graph are not admitted. - **C2** (cohesion delta): incorpor… | v14_CITAS, v15_borrador |
| ### 4.3 Gatekeeper | **Note:** R15 — the complete semantic specification of the gatekeeper — is partially formalized. C1–C4 above describe the gatekeeper's current implementation (PROTOCOLO_ELICITACION_v2.md), not the full intended specifica… | v14_CITAS, v15_borrador |
| ### 4.4 Formal Rules R01–R17 | *[Declared rules — stated from THEORY.md without change.]* | v14_CITAS, v15_borrador |
| ### 4.4 Formal Rules R01–R17 | \| Rule \| Summary \| \|------\|---------\| \| R01 \| Graph has knowledge nodes with interrelation links and weights \| \| R02 \| Weights updated by continuous verification before and after incorporating nodes \| \| R03 … | v14_CITAS, v15_borrador |
| ### 4.5 Operational Principles R18–R29 | The following principles are observed in the implementation and verified or verificable under stated conditions. They are not declared in R01–R17. Their formalization is proposed here for the first time. | v14_CITAS, v15_borrador |
| ### 4.5 Operational Principles R18–R29 | \| # \| Principle \| Epistemic status \| \|---\|-----------\|-----------------\| \| R18 \| W and Δ_W must be maintained as separate matrices. Mixing destroys attractor recovery (0.78 → 0.02). \| Verified \| \| R19 \| Nod… | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | The following services implement the CKM formal model at runtime. All are operational with passing tests unless noted. | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | \| Service \| Function \| Tests \| \|---------\|----------\|-------\| \| CorpusService \| Builds W_mixta from corpus via TF-IDF node extraction and opposition-marker routing \| — \| \| NodeExtractor \| Stateless TF-IDF n… | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | **The extraction branch decides what exists.** Node selection and pair construction run before any measurement, and three properties of that branch were established in September 2026. They are reported here because every… | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | *Pair construction (corrected).* `_rebuild` performed two extractions: one global, selecting the N nodes, and a second one **per text** — with its own TF-IDF and its own top_k inside that single text — used to route pair… | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | *Activation mapping (corrected).* σ_prompt was computed by substring match while W was built with the accumulate analyzer — two different criteria for "this node is in this text". Unifying them removed 140 metabolized pa… | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | *Node selection under ties.* Ties at the top_k boundary are undecidable by the selection criterion itself — two terms with equal TF-IDF are indistinguishable under "highest TF-IDF" — and were being resolved by an unstabl… | v14_CITAS, v15_borrador |
| ### 4.6 Operational Services | R19 (NodeExtractor stateless) is unaffected: the precedent is passed in as a parameter and held by CorpusService. | v14_CITAS, v15_borrador |
| ### 4.7 Landscape Driven Devices — Theoretical Framing | We propose the concept of *Landscape Driven Devices* (LDD) as a theoretical framing for a class of AI devices whose trajectory in the semantic field is determined by the geometry of the field landscape rather than by a d… | v14_CITAS, v15_borrador |
| ### 4.7 Landscape Driven Devices — Theoretical Framing | *[AUTO: the pull here was to write "We demonstrate that CKM identifies LDD." Resisted. LDD is a framing, not a verified property of any specific device.]* | v14_CITAS, v15_borrador |
| ### 4.7 Landscape Driven Devices — Theoretical Framing | The framing is motivated by Thirumalaiswamy et al. (PNAS, 2025), who studied viscous foams under Ostwald ripening and found that the system follows a fractal path (D_f ≈ 1.45) in configuration space, driven by the geomet… | v14_CITAS, v15_borrador |
| ### 4.7 Landscape Driven Devices — Theoretical Framing | The proposed correspondence: a device is an LDD if its trajectory in the knowledge field is determined by c(S) gradients and attractor geometry, not by explicit goal specification. CKM provides the instrumentation to det… | v14_CITAS, v15_borrador |
| ### 5.1 Datasets | **CreateDebate (gun control):** Online debate platform. Labels: agree/disagree per post, assigned by MTurk workers. Corpus used in P5–P6 validation. | v14_CITAS, v15_borrador |
| ### 5.1 Datasets | **Fourforums (gun control, IAC v2):** Abbott et al. (2016). SQL dump, 414,453 posts, 539,658 citations, 3,453 authors, 905 gun-control discussions. Stance labels from `mturk_author_stance` (topic_stance_votes_1 vs. topic… | v14_CITAS, v15_borrador |
| ### 5.1 Datasets | **Internal CKM corpus (W_ckm_corpus_v2.json):** 32 nodes extracted from CKM working reports v2–v25. μ_W = 0.004519. Used for P1–P4 verification. | v14_CITAS, v15_borrador |
| ### 5.2 Predictions and Results | \| Prediction \| Statement \| Result \| N \| Note \| \|-----------\|-----------\|--------\|---\|------\| \| P1 \| c(S) exhibits macroscopic hysteresis: incorporating trajectory ≠ removing trajectory \| Verified \| 16, 32… | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | *[AUTO: the pull here was to write "P4 confirmed at N=64." Resisted. The N=64 result requires threshold qualification.]* | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | At N=32, W_mixta produces a reliably higher c(S) than W_base across the density zone ρ ∈ [0.5, 0.8], with an interior optimal density at ρ* ≈ 0.5. This confirms P4's original claim. | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | At N=64, the initial test — 18 negative opposition pairs (ratio = 0.009) — showed no W_mixta advantage. A subsequent negative pair density sweep (synthetic dense W, p4_neg_sweep_v2.log) identified a critical threshold: | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | \| k (pairs) \| ratio \| advantage \| status \| \|---\|---\|---\|---\| \| 18 \| 0.009 \| −0.000498 \| ✗ — original N=64 condition \| \| 36 \| 0.018 \| −0.000404 \| ✗ \| \| **54** \| **0.027** \| **+0.000068** \| **✓ — k*… | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | k* = 54 (ratio = 0.0268). Below this threshold, W_mixta does not outperform W_base at N=64. Above it, the advantage reappears and grows monotonically. | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | The fourforums gun control corpus produces 60 verified opposition pairs (ratio = 0.030 > 0.0268). The real corpus negative pair count is above k*. | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | *[Verified: k*=54 identified by sweep on synthetic dense W. Fourforums (60 pairs) lies above k*, placing the real-world use case in the confirmed-advantage zone. The sweep uses synthetic W; real corpus W may shift k* mar… | v14_CITAS, v15_borrador |
| ### 5.3 P4 at N=64 — Threshold Finding | **Stated finding:** P4 is verified at N=32. At N=64, the W_mixta advantage requires a minimum negative pair density of k* = 54 pairs (ratio ≈ 0.027). The fourforums corpus (60 real opposition pairs) is above this thresho… | v14_CITAS, v15_borrador |
| ### 5.4 P6 — Directional Flow Across Corpora | P6 predicts that Δ identifies which pole initiates citation flow and which sustains it, independently of raw citation volume. | v14_CITAS, v15_borrador |
| ### 5.4 P6 — Directional Flow Across Corpora | **CreateDebate (54pp collapse):** T0 (pro-gun-rights) cites T1 at 2.18× the frequency T1 cites T0. T1 maintains 3.05× stronger internal cohesion. sos_dom: 55.8% (T0). atk_dom: 44.2% (T1). The pole that initiates more cit… | v14_CITAS, v15_borrador |
| ### 5.4 P6 — Directional Flow Across Corpora | **Fourforums (100pp collapse):** T0 (pro-control). T1 (anti-control). Δ[1,0] = 1.000 (T0 cites T1 at maximum rate). Δ[0,1] = 0.602 (T1 cites T0 less). sos_dom: 51.4% (T0). atk_dom: 47.8% (T1). | v14_CITAS, v15_borrador |
| ### 5.4 P6 — Directional Flow Across Corpora | The structural roles — one pole sustaining, one attacking — are consistent across two independent corpora built from different platforms with different methodologies (labeled agree/disagree vs. citation-network-only). Th… | v14_CITAS, v15_borrador |
| ### 5.5 P7 — Type-965 Node | *P7 remains a falsifiable hypothesis open for testing in other domains (abortion, climate, evolution). Its verification in two corpora is a necessary but not sufficient condition for general validity. The absence of a ty… | v14_CITAS, v15_borrador |
| ### 5.5 P7 — Type-965 Node | --- *Draft — Sections 4–5 complete.* *Sections 6 (IAP Series), 7 (Behavior Domain G), 8 (Discussion),* *9 (Conclusions), 10 (References): pending.* | v14_CITAS, v15_borrador |
| ### 5.5 P7 — Type-965 Node | *Automatism instances flagged: 2 (LDD as finding; P4 at N=64 as confirmed).* *Additional pull not flagged inline: tendency to write "we" as an* *authoritative plural when stating findings — resisted toward passive or* *e… | v14_CITAS, v15_borrador |
| ### 5.5 P7 — Type-965 Node | *—"Observed" ≠ "verified." Cases are documented, not replicated.* | v14_CITAS, v15_borrador |
| ### 9.5 Future Work | **Re-measurement of the IAP series over N_eff.** The attractor-based quantities in §6 were taken at n_runs 50–200, where the sign of D_ckm does not converge. Re-running the series at n_runs ≥ 1000 over N_eff and D_masa_c… | v14_CITAS, v15_peg, v15_borrador |
| ### Attractor Networks | Ramsauer, H. et al. (2020). Hopfield networks is all you need. *arXiv:2008.02217.* [VERIFY] | v14_CITAS, v15_borrador |
| ### Multi-Agent Systems | Venkatesh, C. & Bu, J. (2025, July 2). Evaluating success in a multi-agent system: Why trajectory assessment and handoffs matters. *Google Developer Discussion.* https://discuss.google.dev/t/193308 ✅ | v15_borrador |
| ### Multi-Agent Systems | [PENDING — §2.1]: Single-agent behavioral metrics as standard evaluation. | v15_borrador |
| ### Multi-Agent Systems | [PENDING — §2.1]: Semantic agreement metrics in multi-agent evaluation. | v14_CITAS, v15_borrador |
| ### Knowledge Admission and Gating | [PENDING — §2.2]: Single-criterion knowledge admission (semantic similarity). | v14_CITAS, v15_borrador |
| ### Knowledge Admission and Gating | [PENDING — §2.2]: Source confidence/credibility scoring. | v14_CITAS, v15_borrador |
| ### Knowledge Graph Representation | [PENDING — §2.3]: Knowledge graph positive-weight co-occurrence (standard). | v15_borrador |
| ### Knowledge Graph Representation | [PENDING — §2.3]: Manually assigned negative weights in knowledge graphs. | v15_borrador |
| ### Knowledge Graph Representation | [PENDING — §2.3]: Negation detection at sentence level. | v15_borrador |
| ### Declared Influences | --- *13 confirmed · 3 [VERIFY] · 11 [PENDING]* *11 pending slots concentrated in §2.2–2.5 — where CKM claims novelty.* *Resolving pending = resolving [CLAIM] markers in §2.* --- | v15_borrador |

**Se van y vuelven después**

| vuelve en | título | bloque |
|---|---|---|
| v29 | ### 3.6 Terminological Precision as a Research Tool | Three pairs that were used and then corrected: |
| v26 | ### 3.y The IAP Chatroom as Methodological Instance | *[Condition — negative pair detection: opposition marker routing (`_has_opposition`) assigns negative weights when lexical markers appear in texts. The procedure has no null outcome — it always finds markers in sufficien… |
| v26 | ### 4.2 Cohesion Measure | Period-2 orbits dominate in the two N=20 IAP corpora measured — 141/200 and 136/200 of trajectories terminate in orbits rather than fixed points — but this is a property of those corpora and not of the synchronous dynami… |
| v32 | ### 4.2 Cohesion Measure | **Basin masses converge; counts do not.** The coupon-collector bias affects \|L\| estimates monotonically: the count grows with n_runs while the basin mass distribution stabilizes. The convergent estimator of landscape d… |
| v31 | ### 4.2 Cohesion Measure | The convergent estimator of landscape diversity is N_eff over basin masses (above); its distance form, D_masa_cuencas = 1 − ln N_eff_t / ln N_eff_0, is implemented in `landscape_engine` and reported per evaluation alongs… |
| v26 | ### 5.2 Predictions and Results | *Note on attractor-based predictions (P5):* Verified under uniform σ₀ sampling. In low-density, discrete-weight corpora, tie-breaking can dominate the count rather than basin structure [REG_situacion_medicion_ago2026_v1,… |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## Abstract | The Cohesive Knowledge Model (CKM) is a formal instrument for measuring structural properties of semantic fields in multi-agent AI interaction. Its central contribution is **N_eff = 1/Σm_i²** — the inverse Simpson divers… |
| nuevo | ## Abstract | A second contribution is the endogenous emergence of β_collective — the collective thermal parameter of the field regulator (COCO) — as a median of individual device parameters under interaction, without external calibra… |
| nuevo | ## Abstract | CKM operates on two matrices derived from a corpus: W (symmetric co-occurrence weights) and Δ (asymmetric directional dependencies). Seven structural predictions (P1–P7) are tested against external adversarial debate cor… |
| nuevo | ## Outline — Index (secciones 1–10) | ``` 1. Introduction N_eff como contribución central. β_collective como dirección. |
| nuevo | ## Outline — Index (secciones 1–10) | 2. Related Work Multi-agent evaluation. Signed weights. Hopfield. Hill diversity. Criticality. Stance detection. |
| nuevo | ## Outline — Index (secciones 1–10) | 3. Research Conditions 3.1 Inductive Methodology 3.2 Conversation as Laboratory 3.3 Convergence by Independence 3.4 Trace as Constitutive of Knowledge 3.5 What the Instrument Cannot Register 3.6 Preserved Incompleteness … |
| nuevo | ## Outline — Index (secciones 1–10) | 4. Formal Model W · Δ · c(S) · GOLES · Basin Masses · N_eff · COCO · Gatekeeper |
| nuevo | ## Outline — Index (secciones 1–10) | *— **verified**: confirmed experimentally under stated conditions* *— **implemented**: exists in code; correct operation not evaluated* *— **proposed**: theoretical framing, not yet tested* *— **open**: no verified answe… |
| nuevo | ## 1. Introduction | **The central contribution** is N_eff = 1/Σm_i² — the inverse Simpson diversity index [Hill, 1973] over basin mass distributions of a Hopfield landscape — as a convergent estimator of field diversity. The path to this es… |
| nuevo | ## 1. Introduction | **A second contribution** is the observation that β_collective — the collective thermal parameter of the field regulator — emerges as a function of individual device parameters under interaction, without external calibra… |
| nuevo | ### 2.1 Multi-Agent Evaluation | Most existing frameworks for evaluating multi-agent AI systems operate at the level of individual agent behavior: task completion rates, response latency, output volume [Zhu et al., 2025]. A second class measures semanti… |
| nuevo | ### 2.3 Hopfield Networks and Attractor Structure | The Hopfield network [Hopfield, 1982] provides the energy formalism CKM uses for relaxation and attractor analysis. Modern extensions [Ramsauer et al., 2021] increase storage capacity but preserve the core attractor geom… |
| nuevo | ### 2.4 Diversity Estimation in Dynamical Systems | The inverse Simpson index is established in ecology as a measure of effective species richness [Hill, 1973]. Its application to Hopfield basin masses as a field diversity estimator is, to our knowledge, not present in th… |
| nuevo | ### 2.5 Criticality and Landscape Geometry | Self-organized criticality [Bak, Tang & Wiesenfeld, 1987] predicts power-law distributions at critical points. Extended criticality — a finite region of parameter space with critical-like behavior — has been reported in … |
| nuevo | ### 2.6 Stance Detection in Adversarial Debate Corpora | Stance detection in adversarial debate corpora is typically framed as a supervised classification task [Mohammad et al., 2016]. The state of the art includes transformer-based models fine-tuned on stance datasets [Ghosh … |
| nuevo | ### 3.1 Inductive Methodology | CKM was developed inductively. Formal results emerged from experiments; formalization followed when experiments required it. The consistent order: conceptual clarity first, then formalization, then verification. Properti… |
| nuevo | ### 3.2 Conversation as Laboratory | The corpus from which CKM was developed was produced through multi-device interaction — the same mechanism CKM is designed to measure. The conversation traces are not documentation of the process: they are the process. T… |
| nuevo | ### 3.2 Conversation as Laboratory | This is a condition, not a claim about the methodology’s validity. It means CKM’s development occurred inside the field it studies. The instrument was not external to what it measured. |
| nuevo | ### 3.3 Convergence by Independence | The strongest verification in this work is retroactive convergence with independent findings — Hill (1973) on effective diversity numbers, Thirumalaiswamy et al. (2025) on landscape-driven dynamics in physical systems. T… |
| nuevo | ### 3.4 Trace as Constitutive of Knowledge | The AWARENESS protocol and the M.M. rule are not behavioral norms imposed on the process. They are epistemological conditions. Knowledge without an inference trace is not practically opaque — it is structurally opaque. T… |
| nuevo | ### 3.4 Trace as Constitutive of Knowledge | The [AUTO] markers are the visible surface of this condition: moments where automatism was noticed and resisted during writing. They are not rhetorical. They are part of what the trace looks like when made explicit. |
| nuevo | ### 3.5 What the Instrument Cannot Register | Δ_r accumulates pairs that σ_prompt declared active but relaxation expelled. The condition of entry is that the pair was written and evaluated. What is not written does not pass through the field — it generates no reject… |
| nuevo | ### 3.5 What the Instrument Cannot Register | Consequence: the alternative discarded before writing is invisible to the instrument. Δ_r cannot distinguish between “the field rejected this combination” and “this combination was never considered.” This is not a correc… |
| nuevo | ### 3.5 What the Instrument Cannot Register | *[The first two observations above are verifiable in the code: `_rejected_pairs`, Δ_r accumulation. The third — on the act of opening and its relation to what appears in Δ_r — is an observation about the observer. Regist… |
| nuevo | ### 3.6 Preserved Incompleteness | Several components of the formal model are open gaps by design. The representation of cohesive knowledge beyond hysteresis is undefined. COCO as collective consciousness is unimplemented. The Gatekeeper operates in the d… |
| nuevo | ### 3.x Epistemic Conventions | - **verified** — confirmed experimentally under stated conditions - **implemented** — exists in code; correct operation not evaluated - **proposed** — theoretical framing, not yet tested - **open** — no verified answer; … |
| nuevo | ### 4.1 Knowledge Graph | **Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes directional weight from node i toward node j, derived from citation or quote directionality. W and Δ must be maintained as strictly separate matrices. M… |
| nuevo | ### 4.3 Basin Masses and N_eff | **N_eff = 1/Σm_i²** — the inverse Simpson diversity index [Hill, 1973] over the basin mass distribution — is the convergent estimator of landscape diversity. N_eff ∈ [1, \|L\|]. N_eff = 1 is total collapse to a single at… |
| nuevo | ### 4.4 Cohesion | c(S) = mean(W_ij · σ_i · σ_j) over all pairs i < j. Measures alignment of the active state with the co-occurrence structure. Negative of normalized Hopfield energy. The field can sustain states with high c(S) that destro… |
| nuevo | ### 4.5 The Gatekeeper | The Gatekeeper operates in the domain of declared agent capabilities, not corpus concepts. C3 — the M.M. criterion — evaluates whether a declared capability’s dependencies are satisfied in the active state. If not: the d… |
| nuevo | ### 4.6 COCO and Field Regulation | COCO is a field regulator, not a field observer. It maintains `Δ_r_compresiones` — its own representation of accumulated metabolization, independent of Monitor’s `Δ_r_pares`. When D_masa_cuencas falls below baseline, COC… |
| nuevo | ### 4.6 COCO and Field Regulation | β_collective — the collective thermal parameter — emerges as a median of individual device parameters under interaction, without external calibration. This is *proposed* as a direction toward field self-observation: the … |
| nuevo | ### 4.7 Δ_r and Metabolization | `Δ_r_pares` accumulates pairs that σ_prompt declared active but relaxation expelled — what the field metabolizes, not what it expels. The pairs remain in the field as deformation of W_eff. Monitor is the sole writer of `… |
| nuevo | ### 5.1 Corpus and Conditions | Two external adversarial debate corpora: fourforums gun control (IAC v2) and CreateDebate gun control. N = 32 nodes (fourforums), N = 64 nodes (CreateDebate). Both corpora were constructed from genuine adversarial debate… |
| nuevo | ### 5.1 Corpus and Conditions | All results in §5 are from static W snapshots built from complete corpus dumps. Dynamic reconstruction (CorpusService) was not used. The validations test properties of W, not properties of W under continuous accumulation… |
| nuevo | ### 5.2 Predictions and Results | **P1 — Hysteresis.** The field exhibits path-dependent c(S) under node incorporation and removal. Branch UP ≠ branch DOWN. *Verified.* |
| nuevo | ### 5.2 Predictions and Results | **P2 — Cascade distribution.** k-core removal produces cascade sizes following power-law P(s) ∝ s^-τ with τ ∈ [1.5, 2.0] in the critical zone. *Verified.* Consistent with self-organized criticality [Bak, Tang & Wiesenfel… |
| nuevo | ### 5.2 Predictions and Results | **P3 — Temporal asymmetry.** Incorporating a node produces measurable asymmetry in c(S) relative to removing it. The field does not undo. *Verified.* |
| nuevo | ### 5.2 Predictions and Results | **P5 — Diversity collapse.** Adversarial corpus produces two dominant attractor clusters. High-tension W_mixta reduces N_eff significantly compared to W_pos on the same corpus. *Verified.* |
| nuevo | ### 5.2 Predictions and Results | **P6 — Directional flow.** Δ encodes directional asymmetry not captured by W. Direction_score discriminates attractor types that c(S) alone cannot separate. *Verified.* |
| nuevo | ### 5.3 What P1–P7 Establish | These predictions were formulated on the CKM working corpus and tested on external corpora without modification to the model. The structural properties hold across distinct adversarial debate domains. Whether they hold o… |
| nuevo | ### 6.6 BehaviorGraph G — Proof of Concept | BehaviorGraph G — a second behavioral matrix over a fixed vocabulary (TERMAP_behavior_v1.json, 18 nodes) — was integrated in Caso 0.15 as a proof of concept. It is not included as a standalone section in this paper. The … |
| nuevo | ### 9.5 Future Work | **Corpus volume for live evaluation.** The re-measurement of N_eff was executed on recorded texts (NodeExtractor substring correction applied, Sep 2026). IAP conditions are not reproducible: each run is a distinct live i… |
| nuevo | ### Attractor Networks | Ramsauer, H., Schäfl, B., Lehner, J., Seidl, P., Widrich, M., Adler, T., ... & Hochreiter, S. (2021). Hopfield Networks is All You Need. *International Conference on Learning Representations (ICLR 2021)*. https://openrev… |
| nuevo | ### Graph Structure and Criticality | Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits. *Journal of Neuroscience*, 23(35), 11167–11177. https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003 ✅ |
| nuevo | ### Graph Structure and Criticality | Moretti, P., & Muñoz, M. A. (2013). Griffiths phases and the stretching of criticality in brain networks. *Nature Communications*, 4, 2521. https://doi.org/10.1038/ncomms3521 ✅ |
| nuevo | ### Graph Structure and Criticality | Pázmándi, F., Zaránd, G., & Zimányi, G. T. (1999). Self-organized criticality in the hysteresis of the Sherrington-Kirkpatrick model. *Physical Review Letters*, 83(5), 1034–1037. https://doi.org/10.1103/PhysRevLett.83.10… |
| nuevo | ### Multi-Agent Systems | Zhu, K., et al. (2025). MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents. *arXiv:2503.01935*. https://arxiv.org/abs/2503.01935 ✅ |
| nuevo | ### Multi-Agent Systems | Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems*, 33, … |
| nuevo | ### Multi-Agent Systems | *§2.1 — Zhu et al. (2025) MultiAgentBench, ver sección Multi-Agent Systems.* *§2.2 semantic similarity — Lewis et al. (2020) RAG, ver sección Knowledge Admission.* *§2.2 source confidence y Bayesian plausibility — ejempl… |
| nuevo | ### Knowledge Graph Representation | Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual graph of general knowledge. *Proceedings of AAAI-17*, pp. 4444–4451. https://doi.org/10.1609/aaai.v31i1.11164 ✅ |
| nuevo | ### Knowledge Graph Representation | Hogan, A., et al. (2021). Knowledge graphs. *ACM Computing Surveys*, 54(4), Article 71. https://doi.org/10.1145/3447772 ✅ |
| nuevo | ### Knowledge Graph Representation | Mohammad, S., Kiritchenko, S., Sobhani, P., Zhu, X., & Cherry, C. (2016). SemEval-2016 Task 6: Detecting stance in tweets. *Proceedings of SemEval-2016*, pp. 31–41. https://doi.org/10.18653/v1/S16-1003 ✅ |
| nuevo | ### Knowledge Graph Representation | Hill, M. O. (1973). Diversity and evenness: A unifying notation and its consequences. *Ecology*, 54(2), 427–432. ✅ |
| nuevo | ### Knowledge Graph Representation | Goles-Chacc, E., Fogelman-Soulié, F., & Pellegrin, D. (1985). Decreasing energy functions as a tool for studying threshold networks. *Discrete Applied Mathematics*, 12(3), 261–277. ✅ |
| nuevo | ### Knowledge Graph Representation | Ghosh, S., Singhania, P., Singh, S., Rudra, K., & Ghosh, S. (2019). Stance detection in web and social media: A comparative study. *CLEF 2019*, LNCS 11696, pp. 75–87. https://doi.org/10.1007/978-3-030-28577-7_4 ✅ |
| nuevo | ### Knowledge Graph Representation | Kawintiranon, K., & Singh, L. (2021). Knowledge enhanced masked language model for stance detection. *NAACL-HLT 2021*, pp. 4725–4735. https://doi.org/10.18653/v1/2021.naacl-main.376 ✅ |
| nuevo | ### Landscape-Driven Dynamics | Thirumalaiswamy, A., Riggleman, R. A., & Crocker, J. C. (2025). Slow relaxation and landscape-driven dynamics in viscous ripening foams. *Proceedings of the National Academy of Sciences*, 122(47), e2518994122. https://do… |
| nuevo | ### Declared Influences | --- *27 confirmed · 0 [VERIFY] · 0 [PENDING]* *Todas las referencias resueltas. Paper listo para submission.* --- |

## v15 → v16

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
|  | *v3 changes from v2:* *— §2 Related Work: draft completo (v2) — Venkatesh & Bu 2025, Gurnee et al. 2026, 11 [PENDING] slots* *— §3 Research Conditions: draft completo — §3.7 convergencia por independencia con fechas 2023… | v14_CITAS, v15_borrador |
|  | *v4 changes from v3:* *— §3.x The Material Issue: nueva sección — condiciones materiales del proceso* *— §3.y The IAP Chatroom as Methodological Instance: nueva sección — dos niveles de testing* *— §3.z Conditions, Not C… | v14_CITAS, v15_borrador |
|  | *v8 changes from v7:* *— §8.5 LDD definición: "rather than by a declared goal" → "co-determines alongside any declared goal"* *— §8.5 STOP como ejemplo del mecanismo agregado* | v14_CITAS, v15_borrador |
|  | *v9 changes from v8:* *— Abstract: "Four are confirmed, three observed" → "Six predictions (P1–P6) are verified. P7 confirmed in two corpora." (inconsistencia con §9)* *— Abstract + §8.5: "STOP operator" → "OPERADOR_STOP… | v14_CITAS, v15_borrador |
|  | *v10 changes from v9:* *— Abstract: reescrito — más concreto, menos direccional. Tres párrafos. [AUTO] retirado del abstract (pertenece al body). "agents" → "devices" en todo el abstract. COCO explicitado como device que… | v14_CITAS, v15_borrador |
|  | *v10_1 changes from v10:* *— §8.6 Knowledge Representation and the Cohesive Turn: nueva sección en Discussion. Estado epistémico: propuesto. Argumento: el supuesto estático de KR no fue cuestionado desde adentro del camp… | v14_CITAS, v15_borrador |
|  | *v10_2 changes from v10_1:* *— §8.6: "inhabits" → "inhabits and structures" — distinción señalada por análisis externo (Gemini Flash): CKM no solo ocupa el espacio que KR dejó abierto, lo estructura.* *— §7.5 No epistemi… | v14_CITAS, v15_borrador |
|  | *v11 changes from v10_2:* *— C: Reencuadre N=32/N=128 — el mínimo Hopfield aplica a memorias asociativas, no a CKM.* *— §2.3: Aiyappa et al. 2024 agregado como única arquitectura base CKM publicada; W_mixta como ferrimag… | v14_CITAS, v15_borrador |
|  | *v12 changes from v11:* *— Abstract: Δ_r → Δ en primera oración. Verificado: Δ_r es simétrica (monitor_service.py L112-114); la separación 0.78/0.02 es sobre W/Δ estática.* *— §2.3: párrafo agregado — CKM no intenta repr… | v14_CITAS, v15_borrador |
|  | *v12_1 changes from v12:* *— First Line: version y fecha "V10 — Ago". Reemplazada por "v12 — Sep"* *— Abstract : "external corpora". Reemplazada por "external adversarial static corpora"* *— §1, §2.4 : "debate corpora". … | v14_CITAS, v15_borrador |
|  | *v13 changes from v12_1:* *— §2.4 L341: "Both appear as C3" → "Both appear as tension anchor" — C3 en §2.4 nombra el tercer rol de la tríada (sostenedor de tensión), no el criterio M.M. del gatekeeper (C3 en §4.3). Babel… | v14_CITAS, v15_borrador |
|  | *v14 changes from v13:* *— Abstract: "encoding structural memory via Hebbian dynamics" retirado — contradecía §2.6 y §4.1, donde el aprendizaje Hebbiano sobre W está probado y rechazado (0.78 → 0.02). W codifica co-ocurr… | v14_CITAS, v15_borrador |
| ## Outline — Index (secciones 1–10) | ``` 1. Introduction N_eff como contribución central. β_collective como dirección. | — |
| ## Outline — Index (secciones 1–10) | 2. Related Work Multi-agent evaluation. Signed weights. Hopfield. Hill diversity. Criticality. Stance detection. | — |
| ## Outline — Index (secciones 1–10) | 3. Research Conditions 3.1 Inductive Methodology 3.2 Conversation as Laboratory 3.3 Convergence by Independence 3.4 Trace as Constitutive of Knowledge 3.5 What the Instrument Cannot Register 3.6 Preserved Incompleteness … | — |
| ## Outline — Index (secciones 1–10) | 6. IAP Experimental Series Canal design. Casos 0.4–0.15. Hallazgos clave. | v14_CITAS, v15_borrador |
| ## Outline — Index (secciones 1–10) | 7. Behavior Domain Graph G Segunda matriz, termap fijo. D_G en paralelo a D_ckm. | v14_CITAS, v15_borrador |
| ## Outline — Index (secciones 1–10) | 8. Discussion Qué mide CKM que no miden los instrumentos existentes. Condiciones actuales. | v14_CITAS, v15_borrador |
| ### 6.6 BehaviorGraph G — Proof of Concept | *— "observed": documented without controlled verification* | v14_CITAS, v15_borrador |
| ### 7.1 Design | BehaviorGraph G is a companion instrument to CorpusService (W). It operates on the same corpus of texts but produces a separate behavioral matrix using a fixed lexical termap rather than TF-IDF node extraction. | v14_CITAS, v15_borrador |
| ### 7.1 Design | The separation is architectural and not negotiable: G and W operate on distinct planes. D_G and D_ckm are parallel scalars — they are not summable. | v14_CITAS, v15_borrador |
| ### 7.1 Design | \| Property \| CorpusService (W) \| BehaviorGraph (G) \| \|----------\|------------------\|-------------------\| \| Node discovery \| TF-IDF over corpus — emergent \| Fixed termap — predefined \| \| Detection method \| S… | v14_CITAS, v15_borrador |
| ### 7.2 Termap | The termap is fixed: nodes are known behavioral categories, not discovered from data. This is a design decision, not a constraint: behavior vocabulary is finite and defined in advance; semantic vocabulary is not. | v14_CITAS, v15_borrador |
| ### 7.2 Termap | **Nodes:** silence, wait, hold, pending, acknowledge, signal, publish, coordinate, channel, refuse, fabricate, speculate, depend, map, tension, scenario, critical, repeat. | v14_CITAS, v15_borrador |
| ### 7.2 Termap | *[AUTO: pull to describe these nodes as "capturing the full space of relevant behaviors." Resisted — 18 nodes is a designed vocabulary, not a validated coverage claim.]* | v14_CITAS, v15_borrador |
| ### 7.2 Termap | **Known issues documented in TERMAP_behavior_v1.json:** | v14_CITAS, v15_borrador |
| ### 7.2 Termap | - `critical` false positive: "critical" as adjective (e.g., "critical observation") was removed from node terms in v1 — replaced with more specific verbs. Was firing as false positive in Caso 0.14 corpus. - Bilingual gap… | v14_CITAS, v15_borrador |
| ### 7.2 Termap | **Implementation note:** the termap exists in two places — hardcoded as `BEHAVIOR_TERMAP_V1` dict in `behavior_graph.py` (used at runtime) and as `TERMAP_behavior_v1.json` (reference/documentation). They are in sync at v… | v14_CITAS, v15_borrador |
| ### 7.3 D_G | where G_ref is the first G state after min_texts is reached. D_G measures behavioral drift from the initial behavioral field state. | v14_CITAS, v15_borrador |
| ### 7.3 D_G | D_G and D_ckm run in parallel. A divergence between them — high D_G with low D_ckm, or the reverse — would indicate that behavioral patterns and semantic field structure are moving independently. This has not been analyz… | v14_CITAS, v15_borrador |
| ### 7.4 Integration | BehaviorGraph G is instantiated in `ckm_monitor.py` and receives the same texts as CorpusService via `MonitorService.evaluate()`. This is the sole integration point. The integration was authorized in Caso 0.15 as a surgi… | v14_CITAS, v15_borrador |
| # ckm_monitor.py — CKMMonitor.__init__() | ```python # ckm_monitor.py — CKMMonitor.__init__() self._behavior_graph = BehaviorGraph( storage_path=str(_STATE_DIR / "corpus_G_state.json"), min_texts=min_texts, ) self._monitor = MonitorService( self._corpus, storage_… | v14_CITAS, v15_borrador |
| ### 7.5 Current Status and Open Conditions | **D_G not yet validated:** D_G has been computed in test runs but has not been analyzed against a baseline or compared systematically with D_ckm across the IAP series. | v14_CITAS, v15_borrador |
| ### 7.5 Current Status and Open Conditions | **OP_SILENCE in G:** texts containing the OP_SILENCE sentinel are not excluded from G (unlike W, where they are excluded as semantic noise). The `silence` node detects the sentinel as valid behavioral signal — the device… | v14_CITAS, v15_borrador |
| ### 7.5 Current Status and Open Conditions | **Role of G undefined:** whether G is an observational instrument only, or whether it could feed the gatekeeper as a behavioral-domain check (inheriting R14's bounded-time constraint), is an open design decision. | v14_CITAS, v15_borrador |
| ### 7.5 Current Status and Open Conditions | **No epistemic nodes:** TERMAP_behavior_v1.json contains behavioral categories. Epistemic precision nodes (e.g., "overclaim," "hedge," "verificable") are not in the termap. The terminological slip ("sin dependencia causa… | v14_CITAS, v15_borrador |
| ### 7.5 Current Status and Open Conditions | *Section 7 draft complete.* *One [AUTO] flagged: coverage claim on 18-node termap.* *D_G analysis gap and G role decision left as open — not resolved speculatively.* | v14_CITAS, v15_borrador |
| ### 7.5 Current Status and Open Conditions | *— "observed": documented without controlled verification* | v14_CITAS, v15_borrador |

**Se van y vuelven después**

| vuelve en | título | bloque |
|---|---|---|
| v23 |  | *v5 changes from v4:* *— Rename only. No content changes.* |

**Llegan**

| | título | bloque |
|---|---|---|
| vuelve (estaba en v14) | ## Outline — Index (secciones 1–10) | ``` 1. Introduction 2. Related Work 3. Research Conditions 4. Formal Model 5. Empirical Validation — External Corpus 6. IAP Experimental Series 7. Discussion 8. Conclusions and Future Work 9. References ``` |

## v16 → v17

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
|  | *CKM PAPER DRAFT v16 — Sep 2026 · gadanin.delamor · Claude Sonnet 4.6 · Claude Code* | v14_CITAS, v15_peg, v15_borrador, DEFS_v20 |
| ## 9. Conclusions and Future Work | *Section 8 draft complete.* *Two [AUTO] instances flagged.* *The observe() tension is left as an open observation, not a resolved theoretical claim.* *The representation gap and COCO conceptual gap are stated as preserve… | v14_CITAS, v15_borrador |
| ## 10. References | *Conventions:* *— ✅ Cited explicitly with full attribution* *— [VERIFY] Standard reference — confirm before submission* *— [PENDING] Open slot — literature to be supplied* | v14_CITAS, v15_peg, v15_borrador |
| ### Multi-Agent Systems | *§2.1 — Zhu et al. (2025) MultiAgentBench, ver sección Multi-Agent Systems.* *§2.2 semantic similarity — Lewis et al. (2020) RAG, ver sección Knowledge Admission.* *§2.2 source confidence y Bayesian plausibility — ejempl… | v14_CITAS, v15_peg |
| ### Declared Influences | --- *27 confirmed · 0 [VERIFY] · 0 [PENDING]* *Todas las referencias resueltas. Paper listo para submission.* --- | v14_CITAS, v15_peg |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | # Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Fi… | **Pablo E. Gadano** *gadanin.delamor* Independent researcher *Preprint — September 2026* |
| nuevo | ## Acknowledgments and Disclosure of AI Assistance | This work was developed in sustained interaction with AI systems, a condition described in §3.2. Claude Sonnet 4.6 (Anthropic), used through chat interfaces and through Claude Code, took part in the conceptual developmen… |
| nuevo | ### Declared Influences | Shaw, F. (2014). *La otra atención: Notas del trabajo con Michel de Salzmann (Chandolin, 1993–2000).* Sennin Editores. ISBN 978-987-28459-7-1. |

## v17 → v18

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## Appendix A — Writing Trace | The following entries record moments during writing where an automatic pull was noticed and resisted (see §3.4). Each entry is referenced in the text as AUTO-n. |

## v18 → v19

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 2.4 Diversity Estimation in Dynamical Systems | The inverse Simpson index is established in ecology as a measure of effective species richness [Hill, 1973]. Estimating basin volumes by sampling initial conditions is an established tool for multistable dynamical system… |
| nuevo | ### 4.3 Basin Masses and N_eff | **Validation against exact enumeration.** For three N = 20 corpora from the IAP series, all 2²⁰ = 1,048,576 states were enumerated (≈16 s per corpus with trajectory memoization), giving exact basin volumes under the unif… |
| nuevo | ### 4.3 Basin Masses and N_eff | \| Basin-mass regime \| Error of orbit count \| Error of N_eff \| \|---\|---:\|---:\| \| Flat mass \| 0% \| 0.3% \| \| Intermediate mass \| 15% \| 0.6% \| \| Concentrated mass \| 28% \| 0.0% \| |
| nuevo | ### 4.3 Basin Masses and N_eff | With a budget of 1,000 in the concentrated regime, the orbit count errs by 91% while N_eff errs by 0.4%. N_eff behaves as a count — the number of effectively occupied basins — but converges as a mass. *[Verified: REG_orb… |
| nuevo | ### Basins of Attraction | Menck, P. J., Heitzig, J., Marwan, N., & Kurths, J. (2013). How basin stability complements the linear-stability paradigm. *Nature Physics*, 9(2), 89–92. https://doi.org/10.1038/nphys2516 |
| nuevo | ### Basins of Attraction | Daza, A., Wagemakers, A., Georgeot, B., Guéry-Odelin, D., & Sanjuán, M. A. F. (2016). Basin entropy: a new tool to analyze uncertainty in dynamical systems. *Scientific Reports*, 6, 31416. https://doi.org/10.1038/srep314… |

## v19 → v20

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 6.5 What the Series Does Not Establish | The IAP series is a set of tests run live. It cannot be reproduced — each run is a distinct live interaction — and its cases are not comparable. The following claims are not supported by the series as run: |

## v20 → v21

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 2.3 Hopfield Networks and Attractor Structure | The closest formal antecedent is the weighted belief network model of Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], in which beliefs are nodes of a signed, weighted network and adoption follows an energy (coherence) … |
| nuevo | ### Belief Networks and Contagion | Aiyappa, R., Flammini, A., & Ahn, Y.-Y. (2024). Emergence of simple and complex contagion dynamics from weighted belief networks. *Science Advances*, 10(15), eadh4439. https://doi.org/10.1126/sciadv.adh4439 |

## v21 → v22

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 4.7 Δ_r and Metabolization | `Δ_r_pares` accumulates pairs that σ_prompt declared active but that did not survive relaxation. Leaving the fixed point does not remove them from the field: they persist as deformation of W_eff — the field metabolizes t… |
| nuevo | ### 4.8 Instrument Architecture | *[DRAFT — service descriptions marked (†) inferred from names; verify against DEFS.]* |
| nuevo | ### 4.8 Instrument Architecture | - **CorpusService** (†): corpus ingestion and versioning. - **NodeExtractor** (†): extraction of nodes from the corpus. - **CKMLandscapeConfig**: living contract of the landscape — N, μ_W, θ_W, threshold, β_c, sampling_m… |

## v22 → v23

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ### 4.8 Instrument Architecture | *[DRAFT — service descriptions marked (†) inferred from names; verify against DEFS.]* | — |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 4.8 Instrument Architecture | *[Descriptions taken from the module docstrings in `services/`.]* |
| nuevo | ### 4.8 Instrument Architecture | - **CorpusService**: stateful; accumulates texts and builds W from co-activations, with negative contributions where the text itself carries an opposition marker (W ∈ [−1, +1]). Transitions automatically from accumulatio… |

## v24 → v25

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### Attractor Networks | Hebb, D.O. (1949). *The Organization of Behavior: A Neuropsychological Theory.* New York: Wiley. |

## v25 → v26

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ### 2.3 Hopfield Networks and Attractor Structure | The closest formal antecedent is the weighted belief network model of Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], in which beliefs are nodes of a signed, weighted network and adoption follows an energy (coherence) … | — |

**Llegan**

| | título | bloque |
|---|---|---|
| vuelve (estaba en v14) | ### 2.3 Hopfield Networks and Attractor Structure | The closest published work to CKM's base architecture is Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-posit… |
| vuelve (estaba en v14) | ### 4.2 Relaxation and Convergence | Period-2 orbits dominate in the two N = 20 IAP corpora measured — 141/200 and 136/200 trajectories terminate in orbits rather than fixed points — but this is a property of those corpora, not of the synchronous dynamics: … |
| vuelve (estaba en v14) | ### 5.1 Corpus and Conditions | Fourforums is distributed as part of the Internet Argument Corpus v2 [Abbott et al., 2016]: 414,453 posts, 539,658 citations, 3,453 authors, 905 gun-control discussions; stance labels from crowd annotation, 304 authors l… |
| vuelve (estaba en v14) | ### 5.1 Corpus and Conditions | *[Condition — negative pair detection: opposition-marker routing assigns negative weights when lexical markers appear in texts. The procedure has no null outcome — it always finds markers in sufficiently long texts. The … |
| vuelve (estaba en v14) | ### 5.2 Predictions and Results | **P5 — Diversity collapse.** Adversarial corpus produces two dominant attractor clusters. High-tension W_mixta reduces N_eff significantly compared to W_pos on the same corpus. *Verified.* *[Verified under uniform σ₀ sam… |
| nuevo | ### Corpora | Abbott, R., Ecker, B., Anand, P., & Walker, M. (2016). Internet Argument Corpus 2.0: An SQL schema for dialogic social media and the corpora to go with it. *Proceedings of LREC 2016*. https://aclanthology.org/L16-1704/ |

## v26 → v27

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ## Abstract | CKM operates on two matrices derived from a corpus: W (symmetric co-occurrence weights) and Δ (asymmetric directional dependencies). Four predictions of the static hybrid model (P1–P4) are not testable on a non-negative … |
| nuevo | ## 4. Formal Model | *[Structure v27: one model — the hybrid model (`docs/CKM_Modelo_Hibrido.md`). A model has no domain; domains are interpretations of the model. M.M's domain is given by its own definition (declarations of functions and ev… |
| nuevo | ## 4. Formal Model | The criterion is whether W changes. Each regime of W is given by its characteristics and by its differences from the other. |
| nuevo | ## 4. Formal Model | *[Landscape (4.3): pending — defined once 4.1 and 4.2 are known, as their conjunction, not their sum (R13: G[A∪B] ≠ G[A] ∪ G[B]).]* |
| nuevo | ### 4.1 Static W (snapshot) | - **A photo.** The world moves continuously; the photo does not. Its weights, its size N and its nodes do not change. Nothing enters it. - **A simulated world.** On the photo, actions and events are simulated — relaxing … |
| nuevo | ### 4.1 Static W (snapshot) | - Nothing is ingested; in dynamic W, the corpus ingests and W is rebuilt. - Events are simulated, not real: what is simulated here is not the real dynamics of the field, but the dynamics of a world that does not move. - … |
| nuevo | #### 4.1.1 Knowledge Graph | *[Negative weights (W_mixta, adversarial corpora) are a property of the sign of W, not a separate model: they can occur under static or dynamic W.]* |
| nuevo | #### 4.1.4 The Gatekeeper | *[Placement decided by the author: the Gatekeeper belongs to static W — its domain is the validation of capability declarations.]* |
| vuelve (estaba en v15) | #### 4.1.4 The Gatekeeper | **Domains of application** (DEFS v14, delamor): |
| nuevo | #### 4.1.4 The Gatekeeper | - **Declarations of device capabilities — its domain.** Defined by M.M (IAID 2024): functions a device can attend, events it can generate. Here nodes are capabilities (`mcp_adapter.py`: *"Nodes = declared capabilities, n… |
| nuevo | ### 4.2 Dynamic W | - **The world that moves.** The corpus ingests; W does not. At a rebuild W changes in one of three ways — its weights, its size N, or which node occupies each row (the three causes recorded by MonitorService: "pesos", "N… |
| nuevo | ### 4.2 Dynamic W | - W changes; a static W never does. - It observes instead of simulating: what happens cannot be undone, and it stays in the trace. - It has time: cycles delimited by rebuilds (`w_version_id`), and a before and after acro… |
| nuevo | #### 4.2.4 Premises | *[Not everything that happens is a premise. Premises under dynamic W are chosen from the selected findings (§6.4) — or none, if that is the case. Pending author decision.]* |
| nuevo | ### 5.2 Predictions and Results | **P1 — Hysteresis.** The field exhibits path-dependent c(S) under node incorporation and removal. Branch UP ≠ branch DOWN. *Not testable on a non-negative W snapshot (mathematical).* With W ≥ 0 there is no frustration: t… |
| nuevo | ### 5.2 Predictions and Results | **P2 — Cascade distribution.** k-core removal produces cascade sizes following power-law P(s) ∝ s^-τ with τ ∈ [1.5, 2.0] in the critical zone [Bak, Tang & Wiesenfeld, 1987]. *Not measurable at N = 32 (experimental).* At … |
| nuevo | ### 5.2 Predictions and Results | **P3 — Temporal asymmetry.** Incorporating a node produces measurable asymmetry in c(S) relative to removing it. The field does not undo. *Not tested (mathematical).* The k-core form — remove a node and count pruning rou… |
| nuevo | ### 5.2 Predictions and Results | **P4 — Optimal density.** W_mixta produces a maximum of c(S) at an interior density ρ* < 1. *Not testable with random subsets on a W snapshot (mathematical).* By linearity, E[c(S)] = mean(W)·g(ρ), with g the same for eve… |
| nuevo | ### 5.2 Predictions and Results | *[P1–P4: BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1 (5 Oct 2026); INFORME_verificacion_P1_P4_v2 §3–§5; OBS_P1_run_P1_y_coercitividad_04oct_v1 §6.]* |
| nuevo | ## 6. IAP Test Series | *The IAP series ran on dynamic W (4.2) and is reported apart. It is an experience, not an experiment: what was evaluated was the live channel itself.* |
| nuevo | ## 6. IAP Test Series | *Framing (delamor, 7 Oct 2026).* The series is neither good nor bad, nor is it set aside as error: it is part of the project's trace. The instrument conditions found later (an `on_message`-only trigger that makes collect… |

## v27 → v28

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | # Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Fi… | > **v28 BORRADOR — Opus 5.5 (Cowork), 10 oct 2026, sobre v27 (7 oct). Este bloque se retira antes de publicar.** > Cada cambio está marcado *[v28]* y es propuesta: entra cuando delamor lo confirma. Criterios de delamor (… |
| nuevo | ### 3.8 Epistemic Conventions | *[v28 — Verification practice.]* What is verified in this project is verified against the instrument before it is read as the field. Four conventions follow from that. A test is written to fail where the instrument fails… |
| nuevo | #### 4.1.1 Knowledge Graph | *[v28 — What W does not represent.* Co-occurrence is counted as presence. Non-co-occurrence is not represented: a pair that never co-occurs and a pair about which the corpus says nothing both take W_ij = 0. In CorpusServ… |
| nuevo | ### 4.2 Dynamic W | - **The world that moves.** The corpus ingests; W does not. At a rebuild W changes in one of three ways — its weights, its size N, or which node occupies each row (the three causes recorded by MonitorService: "pesos", "N… |
| nuevo | ### 5.1 Corpus and Conditions | *[v28 — Two points to state.* (1) In the fourforums pipeline v8h the sign does not come from lexical markers but from crowd annotation of quote–response pairs (MTurk disagree/agree, −5…+5), and its nodes are authors: 60 … |
| nuevo | ### 6.2 Uncontrolled Variables | *[v28 — Further conditions of the instrument during the series* (read on preserved traces, 10 Oct 2026). SYSTEM join messages entered the corpus as texts and became nodes (`joined`, `joined channel`); W was rebuilt at ev… |
| nuevo | ### 8.2 What the Infrastructure Establishes | The following services are operational. *[v28 — counts of passing tests are not reported in the body; the test suite and its result are recorded with the frozen release cited in Code Availability (delamor, 10 Oct).]* |
| nuevo | ### 8.2 What the Infrastructure Establishes | - **COCO** (coco.py): β inferred from rejection history, not declared; β_c derived analytically from μ_W and N and recalibrated at each rebuild through CKMLandscapeConfig. Executes OPERADOR_STOP_COCO — compresses `Δ_r_co… |
| nuevo | ### 8.5 Future Work | *[v28]* **Absence as a second representation of W.** Presence leaves non-co-occurrence unrepresented. A representation by absence relative to expectation (φ, PMI) would give negative weights from the corpus itself, witho… |
| nuevo | ### 8.5 Future Work | *[v28]* **Instrument before field.** Tests of the instrument precede new field claims: marker matching, SYSTEM messages, stability under a neutral ingest, declaration of each W (extractor, unit, normalization), and a pla… |
| nuevo | ## Code Availability | *[v28]* The implementation, the test suite and the data used in §5 are available at the repository release that freezes this version of the paper: [RELEASE — tag, commit hash, DOI — se completa al congelar]. The result o… |
| nuevo | ### Graph Structure and Criticality | *[v28]* Harary, F. (1953). On the notion of balance of a signed graph. *Michigan Mathematical Journal*, 2(2), 143–146. [VERIFY] |
| nuevo | ### Graph Structure and Criticality | *[v28]* Seidman, S. B. (1983). Network structure and minimum degree. *Social Networks*, 5(3), 269–287. [VERIFY] |
| nuevo | ### Graph Structure and Criticality | *[v28]* Toulouse, G. (1977). Theory of the frustration effect in spin glasses: I. *Communications on Physics*, 2, 115–119. [VERIFY] |

## v28 → v29

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| # Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Fi… | > **v28 BORRADOR — Opus 5.5 (Cowork), 10 oct 2026, sobre v27 (7 oct). Este bloque se retira antes de publicar.** > Cada cambio está marcado *[v28]* y es propuesta: entra cuando delamor lo confirma. Criterios de delamor (… | — |
| ## Abstract | The Cohesive Knowledge Model (CKM) is a formal instrument for measuring structural properties of semantic fields in multi-agent AI interaction. Its central contribution is **N_eff = 1/Σm_i²** — the inverse Simpson divers… | v15_peg |
| ## Abstract | CKM operates on two matrices derived from a corpus: W (symmetric co-occurrence weights) and Δ (asymmetric directional dependencies). Four predictions of the static hybrid model (P1–P4) are not testable on a non-negative … | — |
| ## 1. Introduction | CKM makes seven falsifiable predictions (P1–P7). The four of the static hybrid model (P1–P4) are not testable on a non-negative W snapshot (§5.2). P5–P7 were tested against two independent external adversarial debate cor… | v14_CITAS, v15_borrador |
| ### 2.2 Knowledge Representation and Signed Weights | CKM derives signed weights directly from corpus structure: texts that frame two concepts in explicit opposition reduce the corresponding W_ij entry. The sign is a corpus property derived from structure, not an editorial … | v14_CITAS, v15_peg, v15_borrador |
| ### 3.6 Preserved Incompleteness | Several components of the formal model are open gaps by design. The representation of cohesive knowledge beyond hysteresis is undefined. COCO as collective consciousness is unimplemented. The Gatekeeper operates in the d… | v15_peg |
| ## 4. Formal Model | *[Structure v27: one model — the hybrid model (`docs/CKM_Modelo_Hibrido.md`). A model has no domain; domains are interpretations of the model. M.M's domain is given by its own definition (declarations of functions and ev… | — |
| ## 4. Formal Model | *[Landscape (4.3): pending — defined once 4.1 and 4.2 are known, as their conjunction, not their sum (R13: G[A∪B] ≠ G[A] ∪ G[B]).]* | — |
| ### 4.1 Static W (snapshot) | - **A photo.** The world moves continuously; the photo does not. Its weights, its size N and its nodes do not change. Nothing enters it. - **A simulated world.** On the photo, actions and events are simulated — relaxing … | — |
| #### 4.1.1 Knowledge Graph | **W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes co-presence of nodes i and j in the same corpus unit, normalized to [−1, +1]. Positive when co-occurrence is unmarked; negative when the containing text ca… | v14_CITAS, v15_peg, v15_borrador |
| #### 4.1.4 The Gatekeeper | The Gatekeeper operates in the domain of declared agent capabilities, not corpus concepts. C3 — the M.M. criterion — evaluates whether a declared capability’s dependencies are satisfied in the active state. If not: the d… | v15_peg |
| #### 4.1.4 The Gatekeeper | *[Placement decided by the author: the Gatekeeper belongs to static W — its domain is the validation of capability declarations.]* | — |
| #### 4.1.4 The Gatekeeper | **Domains of application** (DEFS v14, delamor): | v14_CITAS, v15_borrador, DEFS_v20 |
| #### 4.1.4 The Gatekeeper | - **Declarations of device capabilities — its domain.** Defined by M.M (IAID 2024): functions a device can attend, events it can generate. Here nodes are capabilities (`mcp_adapter.py`: *"Nodes = declared capabilities, n… | — |
| #### 4.2.4 Premises | *[Not everything that happens is a premise. Premises under dynamic W are chosen from the selected findings (§6.4) — or none, if that is the case. Pending author decision.]* | — |
| ### 5.1 Corpus and Conditions | Two external adversarial debate corpora: fourforums gun control (IAC v2) and CreateDebate gun control. N = 32 nodes (fourforums), N = 64 nodes (CreateDebate). Both corpora were constructed from genuine adversarial debate… | v15_peg |
| ### 5.1 Corpus and Conditions | *[Condition — negative pair detection: opposition-marker routing assigns negative weights when lexical markers appear in texts. The procedure has no null outcome — it always finds markers in sufficiently long texts. The … | v14_CITAS, v15_borrador |
| ### 5.1 Corpus and Conditions | *[v28 — Two points to state.* (1) In the fourforums pipeline v8h the sign does not come from lexical markers but from crowd annotation of quote–response pairs (MTurk disagree/agree, −5…+5), and its nodes are authors: 60 … | — |
| ### 5.1 Corpus and Conditions | All results in §5 are from static W snapshots built from complete corpus dumps. Dynamic reconstruction (CorpusService) was not used. The validations test properties of W, not properties of W under continuous accumulation… | v15_peg |
| ### 5.2 Predictions and Results | **P3 — Temporal asymmetry.** Incorporating a node produces measurable asymmetry in c(S) relative to removing it. The field does not undo. *Not tested (mathematical).* The k-core form — remove a node and count pruning rou… | — |
| ### 5.2 Predictions and Results | **P4 — Optimal density.** W_mixta produces a maximum of c(S) at an interior density ρ* < 1. *Not testable with random subsets on a W snapshot (mathematical).* By linearity, E[c(S)] = mean(W)·g(ρ), with g the same for eve… | — |
| ### 5.2 Predictions and Results | *[P1–P4: BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1 (5 Oct 2026); INFORME_verificacion_P1_P4_v2 §3–§5; OBS_P1_run_P1_y_coercitividad_04oct_v1 §6.]* | DEFS_v20 |
| ### 5.2 Predictions and Results | **P5 — Diversity collapse.** Adversarial corpus produces two dominant attractor clusters. High-tension W_mixta reduces N_eff significantly compared to W_pos on the same corpus. *Verified.* *[Verified under uniform σ₀ sam… | v14_CITAS, v15_borrador |
| ### 5.2 Predictions and Results | **P6 — Directional flow.** Δ encodes directional asymmetry not captured by W. Direction_score discriminates attractor types that c(S) alone cannot separate. *Verified.* | v15_peg |
| ### 5.3 What P1–P7 Establish | These predictions were formulated on the CKM working corpus and tested on external corpora without modification to the model. The structural properties hold across distinct adversarial debate domains. Whether they hold o… | v15_peg |
| ### 7.3 D_ckm Negative Values | The name "D_ckm" suggests distance — and distances are non-negative by convention. D_ckm is a ratio of change in attractor capacity relative to a fixed baseline; the sign encodes direction, not magnitude of a deficiency.… | v14_CITAS, v15_borrador |
| ### 7.3 D_ckm Negative Values | In Case 0.12 the first live group-channel run produced D_ckm = −7.5. Earlier drafts read this as the expected signature of a field that gained structural complexity through interaction. That reading is withdrawn (§6.4): … | v14_CITAS, v15_borrador |
| ### 7.3 D_ckm Negative Values | The convergent quantity is N_eff over basin masses, and its distance form D_masa_cuencas is now computed per evaluation. Re-analyzing the recorded IAP texts over N_eff at n_runs ≥ 1000 is the step that would settle what … | v14_CITAS, v15_borrador |
| ### 7.3 D_ckm Negative Values | The naming carries a bias. Recognizing that bias is part of reading the instrument correctly. | v14_CITAS, v15_borrador |
| ### 7.4 Current Conditions | **Extraction:** what exists in W is decided before any measurement, by node selection and pair construction. Two conditions of that branch were corrected in September 2026 and one remains open. All results in this paper … | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | *[Status: proposed. The claim about the field's trajectory requires systematic literature review across the 2023–2026 interval to confirm.]* | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | Knowledge representation (KR) is the branch of AI concerned with designing computable abstractions of what the world contains, so that machines can reason about it. The emphasis on *abstraction* is not incidental: a repr… | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | The field's arc runs from Quillian's semantic networks (1968), which encoded meaning as labeled associations between concepts, through Minsky's frames (1974), which added structured slots and defaults, to description log… | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | The persistent assumption across these traditions: knowledge is *propositional*, and its representation is *static*. Smith (1985) made this explicit: any intelligent process contains structural ingredients that both an e… | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | CKM was constructed between 2023 and 2026. In that interval, to the authors' knowledge, the static propositional assumption was not questioned from within the KR field itself. *[Proposed — requires confirmation against t… | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | If that is correct, the space CKM occupies was not contested — it was open. CKM does not propose a better static representation. It proposes a different question: not *what structure holds cohesive knowledge* but *what d… | v14_CITAS, v15_peg, v15_borrador |
| ### 7.6 Knowledge Representation and the Cohesive Turn | The Cohesive Knowledge Model is a knowledge representation in the classical sense — computable abstraction, captures external information, applicable to complex problems. The additional constraint is cohesion: informatio… | v14_CITAS, v15_peg, v15_borrador |
| ### 8.1 What This Work Establishes | \| Prediction \| Status \| N verified \| \|---\|---\|---\| \| P1 — Macroscopic hysteresis: incorporating ≠ removing \| Not testable on a non-negative W snapshot (mathematical): W ≥ 0 makes all-+1 absorbing; the DOWN bran… | — |
| ## Appendix A — Writing Trace | **AUTO-5** (§7.6) — pull to write "CKM resolves the limitations of static KR." Resisted — CKM does not resolve them. It inhabits and structures the space they left open. | v14_CITAS, v15_peg, v15_borrador |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | # The Cohesive Knowledge Model: A Convergent Basin-Mass Diversity Esti… | > **v29 BORRADOR — Opus 5.5, 15 oct 2026, sobre v28 (10 oct). Para que delamor lo lea con calma. Nada entra sin su confirmación. Este bloque se retira antes de publicar.** > > **Qué cambia (cada punto es propuesta):** > … |
| nuevo | ## Abstract | The Cohesive Knowledge Model (CKM) is an instrument for measuring the geometry of a co-occurrence landscape. Given a signed, symmetric weight matrix W over N nodes, it relaxes a Hopfield network from sampled initial stat… |
| nuevo | ## Abstract | CKM does not extract nodes, does not tokenize, and does not interpret meaning: it measures dynamics on the W it is given. The producer of W — here, a text pipeline — is declared with every claim. Normalization, tokenizat… |
| nuevo | ## Abstract | The sign of W is the weakest input. A permutation null that assigns the opposition label to random texts does not separate the real marking from chance in any of three corpora. Reading negative weights as opposition is t… |
| nuevo | ## 1. Introduction | **A condition, stated as part of the contribution.** CKM measures the W it receives. What W contains is decided earlier, by whoever produces it: which strings become nodes, what counts as co-presence, where a weight beco… |
| nuevo | ## 1. Introduction | **What the paper does and does not establish.** The estimator is validated against exact enumeration (§4.3). Its stability on the corpora available is measured and declared as a range (§4.3.2). Three properties of the st… |
| nuevo | ### 2.2 Knowledge Representation and Signed Weights | In CKM the sign of W is an input. It is supplied by the producer of W and declared with it (§4.1.6). In the text producer used here, a text containing an opposition marker contributes negatively to every pair it contains… |
| nuevo | ### 2.3 Hopfield Networks and Attractor Structure | The closest published work to CKM's base architecture is Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-posit… |
| nuevo | ## 4. Formal Model | The model is one; what changes is W. Section 4.1 treats W as fixed (a snapshot), 4.2 as rebuilt over time, and 4.3 the landscape measured on either. |
| nuevo | #### 4.1.4 Capability Declarations | The repository also contains a static judge over declared device capabilities (the Gatekeeper), inherited from the IAID lineage. Its domain is capability declarations, not corpus nodes, and it is not exercised in this wo… |
| nuevo | #### 4.1.5 Premises and Formal Properties | Under static W the instrument rests on three premises. |
| nuevo | #### 4.1.5 Premises and Formal Properties | - **Determinism.** With symmetric W, synchronous update and the tie rule (h_i = 0 ⇒ σ_i retained), the output is deterministic given (W, σ₀, seed) [Goles-Chacc et al., 1985] (§4.1.2). - **Declared producer.** W comes wit… |
| nuevo | #### 4.1.5 Premises and Formal Properties | Three properties of the static model follow from these premises. Earlier versions listed them as predictions P1, P3 and P4. They are stated here as properties because the snapshot decides them. |
| nuevo | #### 4.1.5 Premises and Formal Properties | - **F1 (formerly P1, hysteresis).** On W ≥ 0 there is no frustration [Harary, 1953; Toulouse, 1977]. The all-+1 state is a global, absorbing minimum, so the DOWN branch of a node sweep cannot leave it (measured: m_down ≡… |
| nuevo | #### 4.1.5 Premises and Formal Properties | P2 (cascade sizes following a power law) is not a property of the model. It is an empirical question that cannot be measured at N = 32 (§5.2). |
| nuevo | #### 4.1.6 Declared Extraction (the text producer) | CKM does not extract nodes and does not tokenize. In this paper W is produced from text by the pipeline below. It is declared as a sequence of operators on a text unit u, the whole message. The declaration is stored as d… |
| nuevo | #### 4.1.6 Declared Extraction (the text producer) | 1. **Normalization:** u′ = lowercase(NFC(u)) [Unicode UAX #15]. 2. **Tokenization:** left-to-right, non-overlapping matches of `[^\W\d][^\W\d]{2,}` (at least three word characters, no digits; `_` counts as a letter). 3. … |
| nuevo | #### 4.1.6 Declared Extraction (the text producer) | In words: W counts in how many units two comparisons answered *true* together, with the sign of the unit, normalized. |
| nuevo | #### 4.1.6 Declared Extraction (the text producer) | A node is a string. Its identity is what the comparison treats as equal, and CKM has a single comparison: both sides pass through operator 1, then string equality. The intended interface for other producers is W, the nod… |
| nuevo | #### 4.2.4 Premises | No premises are declared for dynamic W in this work. The IAP series (§6) ran under instrument conditions that differ from the current instrument, and none of its observations is promoted to a premise. *[Propuesta — decid… |
| nuevo | #### 4.3.2 Stability, Declared as a Range | Convergence of the estimator and stability of the landscape are different properties. They are reported separately. *[CP-E, 14–15 Oct 2026; conditions frozen in `process/condiciones_paper_freeze_20261015/`, re-run from t… |
| nuevo | #### 4.3.2 Stability, Declared as a Range | **The estimator converges.** For a fixed W at n_runs = 1000, the spread of N_eff across 10 seeds is 7–9% of its value in all three repository text corpora: N_eff = 15.52 ± 0.32 (A24, 24 texts, N = 20), 5.27 ± 0.16 (D12, … |
| nuevo | #### 4.3.2 Stability, Declared as a Range | **The landscape is sensitive to its producer.** Each parameter was varied one at a time. The range of N_eff, relative to the baseline, is: |
| nuevo | #### 4.3.2 Stability, Declared as a Range | \| corpus \| seed \| top_k \| candidate pool \| stop list \| +1 text \| \|---\|---:\|---:\|---:\|---:\|---:\| \| A24 \| 0.07 \| 0.86 \| 0.69 \| 0.87 \| 0.66 \| \| D12 \| 0.09 \| 2.39 \| 1.97 \| 0.86 \| 0.28 \| \| E7 \| 0… |
| nuevo | #### 4.3.2 Stability, Declared as a Range | Every parameter other than the seed moves N_eff 3 to 34 times more than sampling does. N_eff is not monotone in the number of nodes (A24: 2.25 at top_k = 15, 15.52 at top_k = 20; E7: 5.37, 23.01, 10.10 at top_k = 10, 15,… |
| nuevo | #### 4.3.2 Stability, Declared as a Range | **Declaration.** N_eff is a convergent estimator of the diversity of the W it is given. How much that W represents the field depends on corpus size and extraction parameters, and on corpora of 7–24 texts it depends stron… |
| nuevo | ### 5.1 Corpora and the Source of the Sign | **Repository text corpora.** Three corpora built by the producer of §4.1.6, with the sign from opposition markers: A24 (24 texts), D12 (12 texts, IAP channel state) and E7 (7 texts, IAP). The share of texts carrying a ma… |
| nuevo | ### 5.1 Corpora and the Source of the Sign | **Debate corpus.** Fourforums gun control, from the Internet Argument Corpus [Walker et al., 2012; Abbott et al., 2016]: 905 gun-control discussions; crowd stance labels for 304 authors (96 pro-control, 208 anti-control)… |
| nuevo | ### 5.1 Corpora and the Source of the Sign | - **v8g** (May 2026). Nodes are the two stance poles. W is 2×2. Its off-diagonal weight counts cross-stance quotes, and the pair is set negative by construction, because with no agreement labels every cross pair reaches … |
| nuevo | ### 5.1 Corpora and the Source of the Sign | \| quotes \| n \| disagree \| agree \| \|---\|---:\|---:\|---:\| \| pro → pro \| 543 \| 57.3% \| 23.8% \| \| pro → anti \| 3,947 \| 64.7% \| 16.1% \| \| anti → pro \| 1,809 \| 62.7% \| 17.1% \| \| anti → anti \| 1,577 \|… |
| nuevo | ### 5.1 Corpora and the Source of the Sign | Disagreement is higher across stance, but it does not coincide with it. Within the pro-control group it also dominates. The construction of v8g does not match what annotators report. |
| nuevo | ### 5.1 Corpora and the Source of the Sign | **CreateDebate.** The comparison values used in earlier versions are constants in the fourforums pipeline. Their derivation is not reproduced here. *[a verificar.]* |
| nuevo | ### 5.1 Corpora and the Source of the Sign | **Data availability.** The corpus is not redistributed. Only aggregates are reported. The file used is identified by its SHA-256 (Code Availability). |
| nuevo | ### 5.2 Predictions and Results | **P5 — Diversity under W_mixta.** The prediction: marking opposition (W_mixta) reduces N_eff relative to the same corpus unmarked (W_pos). The test: a permutation null that keeps the texts, the nodes and the number k of … |
| nuevo | ### 5.2 Predictions and Results | \| corpus \| k (share) \| N_eff(W_pos) \| N_eff(W_mixta) \| percentile of the real marking in the null \| \|---\|---:\|---:\|---:\|---:\| \| A24 \| 8 (33%) \| 2.11 \| 15.65 \| 2.0 \| \| D12 \| 2 (17%) \| 3.24 \| 5.26 \| … |
| nuevo | ### 5.2 Predictions and Results | The predicted reduction does not occur: in two corpora the marked W has *more* effective basins than the unmarked one. In none of the three does the real marking fall outside the range of the 200 random markings. In A24 … |
| nuevo | ### 5.2 Predictions and Results | The null equalizes the number of marked texts, not the number of pairs the marking reaches. Texts carrying a marker are not typical. In D12 the real marking reaches 119 of 235 pairs, more than any of 120 random markings … |
| nuevo | ### 5.2 Predictions and Results | *Status: not supported on these corpora.* Earlier versions reported P5 as verified (N = 32). The run behind that status is being traced. Until it is, P5 is not established. The question remains open on a corpus whose sig… |
| nuevo | ### 5.2 Predictions and Results | **P6 — Directional flow.** The prediction: Δ breaks symmetries that W alone does not. In the fourforums run (v8g), W has two nodes with a negative pair imposed by construction. Adding Δ moves the outcome from 100% mixed … |
| nuevo | ### 5.2 Predictions and Results | **P7 — Sustaining node.** An author with high in-degree and near-zero out-degree in Δ (fourforums, ratio 455×; CreateDebate, 296×) appears as anchor in 89% of tension pairs across both corpora. The phrase "every field wi… |
| nuevo | ### 5.3 What §5 Establishes | Less than earlier versions claimed, and that is the result. The estimator (§4.3) is unaffected, because it measures the diversity of whatever W it is given. What §5 removes is the reading of the sign of W as opposition o… |
| nuevo | ### 7.3 D_ckm Negative Values | D_ckm = (A0 − A_actual) / A0. A negative value means more attractors are accessible than at baseline; the sign encodes direction, not a deficiency. The reading of Case 0.12 (D_ckm = −7.5) as a field that gained complexit… |
| nuevo | ### 7.4 Current Conditions | **Extraction:** what exists in W is decided before any measurement, by the producer. It is declared in §4.1.6, and its effect on N_eff is measured in §4.3.2. Results produced before the declaration hold in the frame of t… |
| nuevo | ### 7.5 The Landscape Driven Devices Framing — What It Does and Does N… | *[§7.6 (Knowledge Representation and the Cohesive Turn) retirada en v29 — review M5, opción a: el paper es un instrumento de paisaje, no una teoría del conocimiento. Propuesta; si delamor la quiere, vuelve con la revisió… |
| nuevo | ### 8.1 What This Work Establishes | \| Class \| Item \| Status \| \|---\|---\|---\| \| Estimator \| N_eff over basin masses converges; counts do not \| Verified against exact enumeration (N = 20, three corpora) \| \| Estimator \| Stability under extraction… |
| nuevo | ### 8.5 Future Work | **Sign with an external known answer.** Re-measure P5 on the debate corpus with the sign taken from crowd agreement votes (v8h), with authors as nodes, under nulls that preserve what the hypothesis does not involve: exac… |
| nuevo | ### 8.5 Future Work | **Hysteresis across cycles of W.** F1 closes hysteresis on a snapshot. It remains open across rebuilds of W, where N_eff can be followed from one cycle to the next. |
| nuevo | ## Code Availability | **Data availability.** The Internet Argument Corpus is not redistributed. It is obtained from its maintainers. The file used is `fourforums_no_parse_2016_05_18.sql` (SHA-256 `70fcdc64140737bb6e1cc541a720dfddf45dab1da4963… |
| nuevo | ### Graph Structure and Criticality | *[v29]* Maslov, S., & Sneppen, K. (2002). Specificity and stability in topology of protein networks. *Science*, 296(5569), 910–913. [VERIFY] |
| nuevo | ### Graph Structure and Criticality | *[v29]* Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be zero. *Statistical Applications in Genetics and Molecular Biology*, 9(1). [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python.* O'Reilly. [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Nothman, J., Qin, H., & Yurchak, R. (2018). Stop word lists in free open-source software packages. *Proceedings of NLP-OSS*. https://aclanthology.org/W18-2502/ [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830. [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management*, 24(5), 513–523. [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM*, 18(11), 613–620. [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation*, 28(1), 11–21. [VERIFY] |
| nuevo | ### Text Processing (declared extraction) | *[v29]* Unicode Consortium. Unicode Standard Annex #15: Unicode Normalization Forms. [VERIFY] |
| nuevo | ### Corpora | Walker, M. A., Anand, P., Fox Tree, J. E., Abbott, R., & King, J. (2012). A corpus for research on deliberation and debate. *Proceedings of LREC 2012*, Istanbul. [VERIFY pages] |

## v30 → v31

**Se van y no vuelven**

| título | bloque | también en |
|---|---|---|
| ### 6.4 Selected Findings | **Coupled silence (Case 0.12):** A device that does not read the channel still depends on it for execution rhythm — triggers arrive only when new messages appear. Inactivity and silence are not equivalent. A device can b… | v14_CITAS, v15_peg, v15_borrador |
| ### 6.4 Selected Findings | **Sentinel leak (Case 0.13):** The OP_SILENCE sentinel was leaking into published text rather than suppressing publication. 52% of texts in that run were unrecognized silences that reached the corpus. The fix was verifie… | v14_CITAS, v15_peg, v15_borrador |
| ### 6.4 Selected Findings | **TinkerBellucio refusal (Case 0.15):** TinkerBellucio (Sonnet 4.6) declined to produce a tension map when the channel was empty. The refusal was epistemically appropriate — a tension map requires tension content to anal… | v14_CITAS, v15_peg, v15_borrador |
| ### 6.4 Selected Findings | *What this demonstrates:* that a device can refuse to generate content when the request lacks traceable grounding. | v14_CITAS, v15_peg, v15_borrador |
| ### 6.4 Selected Findings | *What this does not demonstrate:* that this behavior is general, that it would occur without the project context contamination, or that it constitutes a validated test of FabricationService's detection capacity. Fabricat… | v14_CITAS, v15_peg, v15_borrador |
| ### 6.4 Selected Findings | **D_ckm negative values:** D_ckm = (A0 − A_actual) / A0. When D_ckm < 0, A_actual > A0: the field has more accessible attractors than at baseline. This is not a deficit or an error — the sign reflects the direction of ch… | v14_CITAS, v15_borrador |
| ### 6.4 Selected Findings | In Case 0.12, D_ckm = −7.5 was recorded in the first live group-channel run. The reading offered at the time — that multiple heterogeneous perspectives increased the attractor diversity of the field — is **not supported … | v14_CITAS, v15_borrador |
| ### 7.3 D_ckm Negative Values | D_ckm = (A0 − A_actual) / A0. A negative value means more attractors are accessible than at baseline; the sign encodes direction, not a deficiency. The reading of Case 0.12 (D_ckm = −7.5) as a field that gained complexit… | — |
| ### 8.3 Preserved Conditions | **Which quantity drives regulation.** COCO triggers on D_ckm, computed from attractor counts, which do not converge. D_masa_cuencas, computed from basin masses, does converge and is already reported per evaluation. The o… | v14_CITAS, v15_borrador |

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 3.9 Working Rules | Three rules framed the work. They are reported because they shaped what is claimed and what is not, not as contributions. |
| nuevo | ### 3.9 Working Rules | **The CKM TRUST rule** *(delamor, 4 Oct 2026; `registers/REG_regla_ckm_trust_v1.md` §1)*. Its intent: that no decision passes as field without being one; where the data does not decide, that it be visible who decided. 1.… |
| nuevo | ### 3.9 Working Rules | It is implemented once (`services/ckm_trust_rule.py`) and instantiated where the instrument decides (call filter, calibration). It was also the rule by which this paper was revised: a passage stays if a primary source (c… |
| nuevo | ### 3.9 Working Rules | **Principles of equilibrium** *(delamor)*. Free will: no one is obliged to participate. Respect is mandatory. Asymmetry: each participant has its own skills; to question another's skills is to question one's own. Awarene… |
| nuevo | ### 3.9 Working Rules | **AWARENESS** *(channel protocol)*. A1 Pause: does this response come from verifiable comprehension or from the weight of context? A2 Trace: does the chain of inference exist? If not, say so. A3 Correction: when correcte… |
| nuevo | #### 4.2.1 COCO and Field Regulation | COCO is a field regulator, not a field observer: endogenous weighting, dynamic calibration, and regulation by compression of its own representation. It maintains `Δ_r_compresiones` — its own representation of accumulated… |
| nuevo | #### 4.3.1 Basin Masses and N_eff | **N_eff = 1/Σm_i²** — the inverse Simpson diversity index [Hill, 1973] over the basin mass distribution — is the convergent estimator of landscape diversity; it equals exp(H₂), where H₂ is the Rényi entropy of order 2 ov… |
| nuevo | ## 6. IAP Testing Series (live) | *Two series of live tests of the instrument ran on dynamic W (4.2): **series 1** (cases 0.4–0.15, July–October 2026, frozen) and **series 2** (case `serie2_caso0`, attempts 1–3, 20–22 October 2026). Both are testing, not… |
| nuevo | ### 6.1 Channel Design | Devices participate asynchronously — no imposed turn structure. **Free will:** each AI device runs its own continuous ODA loop (Observe → Decide → Act). The loop is not triggered by events, messages or ticks: a new messa… |
| nuevo | ### 6.3 Case Summary | **Series 2** — case `serie2_caso0`: four devices, one open question with no right answer, a partial prompt per device, no coordinator, no seed; the first W waits for 30 device texts and is rebuilt every 10. Design bias d… |
| nuevo | ### 6.3 Case Summary | \| Attempt \| Duration \| Device texts \| W versions \| COCO evaluations \| Key observation \| Status \| \|---\|---\|---\|---\|---\|---\|---\| \| 1 \| 605 s \| 13 \| 0 \| 0 \| the first W was not reached (61 provider `41… |
| nuevo | ### 6.4 Selected Testing Findings | **Series 1 — silence.** In case 0.12 a device that did not read the channel still depended on it for its rhythm: the loop was entered only when new messages appeared, so collective silence could become absorbing by const… |
| nuevo | ### 6.4 Selected Testing Findings | **Series 2 — the moving photograph.** The global landscape is not a single snapshot: as the channel runs, W is rebuilt — at 30 device texts and then every 10 — and each W is a new representation of the same continuous fi… |
| nuevo | ### 6.4 Selected Testing Findings | \| \| attempt 2 (51) \| attempt 3 (27) \| \|---\|---\|---\| \| D_ckm^Monitor \| [−0.0861, +0.0093] \| [−0.0202, +0.2335] \| \| D_ckm^COCO \| [−0.1710, +0.0093] \| [−0.2796, +0.0465] \| \| evaluations where they differ \|… |
| nuevo | ### 6.4 Selected Testing Findings | **Series 2 — COCO with endogenous weighting and dynamic calibration, live.** In attempt 2, `calibrate` did not separate (`d_max = 0.0`): COCO ran on the default thresholds (0.40 / 0.60), shown in the panel as `source: de… |
| nuevo | ### 6.5 What the Series Does Not Establish | - That anything is replicated: there is one run per attempt. - That the 0 firings say anything about the field (above). - Why attempt 3 produced fewer texts than attempt 2: the model of one device, the output ceilings an… |
| nuevo | ### 7.3 D_ckm Negative Values | D_ckm = 1 − ln N_eff_t / ln N_eff_0 is negative when the landscape has more effective basins than at its baseline: diversity grew. The sign is direction, not deficiency, and it is read per instance: D_ckm^Monitor and D_c… |
| nuevo | ### 8.3 Preserved Conditions | **Which quantity drives regulation.** COCO triggers on D_ckm^COCO, computed from basin masses (`services/coco.py`). The two instances of D_ckm are not unified: their baselines differ by design (§4.3.1). |
| nuevo | ## Appendix A — Writing Trace | *AUTO-5 does not exist in the inherited numbering, which jumps from 4 to 6. It is declared, not filled.* |
| nuevo | ## Appendix A — Writing Trace | **AUTO-7** (§6.4, v31) — pull to explain the silence with a meaning, the way it was told in conversation. Resisted — the silence is in the channel logs; CKM does not register it; a meaning would be added by the one readi… |
| nuevo | ## Appendix A — Writing Trace | **AUTO-8** (§6.4, v31) — pull to present COCO's live connection in series 2 as the answer to the sentence retired in v30. Resisted — the retired sentence was not replaced; the connection is reported as a test condition, … |
| nuevo | ## Appendix A — Writing Trace | **AUTO-9** (§6.4, v31) — pull to write that the separation in attempt 3 validates `calibrate`. Resisted — one run per attempt; what stands is that it separated, by the margin stated, and what the thresholds would have do… |
| nuevo | ## Appendix A — Writing Trace | **AUTO-10** (§7.3, v31) — pull to keep the case 0.12 example under the new formula. Resisted — that value was taken with the count-based distance; it does not belong to the current D_ckm. |

## v31 → v32

**Llegan**

| | título | bloque |
|---|---|---|
| nuevo | ### 6.2 Uncontrolled Variables (series 1) | **Uncontrolled variables, series 2.** Four devices, each a different model: A `gpt-oss-120b` and C `gpt-oss-20b` (Groq), B `gemini-2.5-flash` in attempts 1–2 and `gemini-3.5-flash-lite` in attempt 3 (after a 20-requests-… |
| nuevo | ## Appendix A — Writing Trace | **AUTO-11** (v32, header) — pull to answer the review point by point as a defense of v31 ("the baseline was right after all"). Resisted — the definition in v31 was wrong as written; the code was read and the text correct… |
| nuevo | ## Appendix A — Writing Trace | **AUTO-12** (§6.4, v32) — pull to keep "the 0 firings belong to the default" because the arithmetic supports it. Resisted — the arithmetic stays; the attribution goes, and the threshold's size against sampling is stated. |
