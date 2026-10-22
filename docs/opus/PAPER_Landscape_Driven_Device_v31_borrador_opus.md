# The Cohesive Knowledge Model: A Convergent Basin-Mass Diversity Estimator for Hopfield Landscapes over Co-occurrence Fields

> **v31 BORRADOR — Opus 5.5, 22 oct 2026, sobre v30 (22 oct). El v30 queda intacto como traza. Este bloque se retira antes de publicar.**
>
> **Viene del primer review externo del v30** (delamor, 22 oct): *"2 D_ckm conteos vs masa de cuencas; 2 D_ckm Monitor vs COCO — ¿de cuál de los 4 D_ckm hablamos en cada momento?"* — BABEL. Y de lo que delamor fijó: *el único instante es el ahora; el único instrumento CKM es el actual; el único COCO es ponderación endógena, calibración dinámica, regulador por compresión de Δ_r_compresiones; el único Monitor es singleton; HAY DOS D_ckm, NO SON LO MISMO.*
>
> **Qué cambia:**
> - **Un solo D_ckm, el actual** (masa de cuencas, `landscape_engine.d_ckm`), y **dos instancias con nombre**: **D_ckm^Monitor** y **D_ckm^COCO** (§4.3.1). La forma por conteos sale como D_ckm: donde la serie 1 la usó, se nombra como *la distancia por conteos de entonces*. Notación de Opus, descriptiva (sólo dice de quién es el baseline): **decide delamor**.
> - §4.2.1 y §4.2.3: COCO y Monitor con la definición de delamor. §8.2 y §8.3: dos rastros más de la ausencia (*"operation on the live IAP channel is pending"*, *"COCO triggers on D_ckm computed from attractor counts"*) actualizados al código.
> - §6.1: **free will — ODA continuo**, no disparado por eventos, mensajes ni ticks.
> - §6: **dos series de testing en vivo**; §6.4 pasa a ***Selected Testing Findings*** con la selección de delamor: serie 1 — el silencio; serie 2 — la foto en movimiento, y COCO con calibración dinámica en vivo. Salen de §6.4 sentinel leak, la negativa de TinkerBellucio, el D_ckm −7.5 y trace_ip (siguen en la tabla de §6.3).
> - §3.9 nuevo: la regla CKM TRUST, los Principios de equilibrio y AWARENESS. Metodología: §3.1–3.6 y `docs/opus/METODOLOGIA_TRUST_v1.md`. Teoría: §4.
> - Apéndice A: AUTO-7 a AUTO-10, de esta escritura. **AUTO-5 no existe** en la numeración heredada (salta de 4 a 6): se declara, no se rellena.
>
> **Lo que esta versión no hizo:** no re-verificó el resto pasaje por pasaje; no tocó las referencias. Los números de la serie 2 vienen de `registers/REG_iap_serie2_caso0_intento2_v1.md` y del **borrador** `docs/REG_borrador_serie2_caso0_intento3.md` (no aprobado aún). Redacción de Opus = el `g` de esta versión. **Vuelve al review.**
>
> **v30 BORRADOR — Opus 5.5, 22 oct 2026, sobre v29 (15 oct). El v29 queda intacto como traza. Este bloque se retira antes de publicar.**
>
> **Qué cambia:** se retira, **sin reemplazo**, la frase heredada *"COCO was never connected to the live IAP channel"* en sus **cuatro** lugares del v29 (§3.7 l.144, §4.2.1 l.266 —β_collective, dentro de un corchete—, §4.2 l.281, gaps l.668; el de l.266 se le había escapado a Opus el 21 oct, cuando contó tres) — decisión de delamor, 21 oct (`docs/opus/decisiones_en_el_acto.md`): era la única ausencia nombrada del camino vivo y describía testing, no el modelo. En l.281 sale también *"Exercised only in test drivers"*, que formaba la misma cláusula. Nada se agrega en su lugar.
>
> **Lo que esta versión no hizo (alcance apretado, delamor 22 oct):** no re-verificó el resto del v29 pasaje por pasaje contra fuente primaria. **Rastros listados, sin tocar** (para el review): (1) §8, *"What remains open is corpus volume sufficient to exit the accumulate phase and reach the evaluate phase under live conditions"* — en el intento 2 (21 oct) el corpus salió de acumulación (80 textos, 6 W); (2) la tabla de casos IAP termina en la serie 1; (3) §3.7 *"in none of the 253 documented panels"* salió con la frase. Lente: `docs/opus/METODOLOGIA_TRUST_v1.md`. Redacción de Opus = el `g` de esta versión.
>
> **v29 BORRADOR — Opus 5.5, 15 oct 2026, sobre v28 (10 oct). Para que delamor lo lea con calma. Nada entra sin su confirmación. Este bloque se retira antes de publicar.**
>
> **Qué cambia (cada punto es propuesta):**
> - **Título y abstract** alrededor del estimador N_eff (review M2). El título "Landscape Driven Devices" pasa a §7.5 como framing propuesto.
> - **CKM no extrae ni tokeniza; la extracción se declara** (delamor, 14 oct). Nueva §4.1.6 con los ocho operadores (`docs/defs/DECLARACION_extraccion_W_v1.md`). CKM interpreta dinámica, no significado.
> - **P1, P3, P4 pasan a propiedades formales** del modelo estático (§4.1.5); P2 queda como no medible a esta escala (M1).
> - **Estabilidad declarada como rango con dependencias** (§4.3.2, CP-E).
> - **§5 reescrita con lo que salió del CP-M y de la lectura de los pipelines de fourforums (14–15 oct):** el signo por marcadores no se separa del nulo; P5 deja de figurar como verificado; P6 corrió sobre una W de 2 nodos con el par negativo impuesto; P7 sin "genuine structural tension" y con nulo pendiente.
> - **β_collective** baja a una cláusula (M3). **Gatekeeper** a una oración (M8). **§7.6 sale** (M5, opción a). **Aiyappa**: un párrafo sobre lo que el snapshot no tiene (M9). Secciones de Premisas con contenido (M6). Marcas [v28] retiradas.
>
> **A verificar antes de publicar (no lo verifiqué en esta versión):**
> 1. De qué corrida y qué W sale el "P5 verificado, N = 32" de v28. No lo encontré en los pipelines leídos.
> 2. Origen de 2,18× y 3,05× (P6), de 455× / 296× y del 89 % (P7), y de las constantes `CD_BASELINE` de CreateDebate.
> 3. Las cifras de §4.3.2 y §5.2 están copiadas de los REPORTES del CP-E y CP-M en la BANDEJA (leídos en la PC). Conviene una segunda mirada a la tabla de §4.3.2.
> 4. La descripción de Aiyappa et al. en §2.3 (de memoria).
> 5. Si el dump es IAC 2.0 o v1 (delamor dijo v1; el archivo tiene el esquema SQL de 2.0). Permiso de uso: pedido pendiente.
> 6. Las tres referencias [VERIFY] y las nuevas (Walker 2012, Maslov–Sneppen 2002).

**Pablo E. Gadano**  
*gadanin.delamor*  
Independent researcher  
*Preprint — [fecha al congelar el release]*

---


## Abstract

The Cohesive Knowledge Model (CKM) is an instrument for measuring the geometry of a co-occurrence landscape. Given a signed, symmetric weight matrix W over N nodes, it relaxes a Hopfield network from sampled initial states and reports how the state space distributes over the attractors reached. Its contribution is **N_eff = 1/Σm_i²**, the inverse Simpson index over basin masses, as a convergent estimator of landscape diversity. Attractor counts grow with sampling; basin masses converge. Against exact enumeration of all 2²⁰ states in three N = 20 corpora, orbit counts err by up to 28% (91% at a low sampling budget) and N_eff by at most 0.6%.

CKM does not extract nodes, does not tokenize, and does not interpret meaning: it measures dynamics on the W it is given. The producer of W — here, a text pipeline — is declared with every claim. Normalization, tokenization, selection, presence and sign are stated as operators with their parameters, and the code is held to implement what the paper declares. Stability is stated as a range with its dependencies. On small text corpora (7–24 texts) the estimator converges across seeds, while the landscape is highly sensitive to extraction parameters and to the addition of a single text.

The sign of W is the weakest input. A permutation null that assigns the opposition label to random texts does not separate the real marking from chance in any of three corpora. Reading negative weights as opposition is therefore not supported on these corpora, and claims that rest on the sign are stated as holding under the declared procedure only. Three properties of the static model are shown to be fixed by premise on non-negative snapshots. Live multi-agent runs (the IAP series) are reported as tests of the instrument, not as findings about the field.


## Outline

```
1. Introduction
2. Related Work
3. Research Conditions
4. Formal Model
5. Empirical Validation — External Corpus
6. IAP Test Series
7. Discussion
8. Conclusions and Future Work
9. References
Appendix A. Writing Trace
```

---
## 1. Introduction

Multi-agent AI systems are increasingly deployed in configurations where several devices interact over a shared channel — producing text, making decisions, building on each other’s outputs. Evaluating whether this interaction constitutes genuine coordination or parallel activity requires measuring something most existing approaches do not capture: the structural field that emerges from interaction itself.

Most existing approaches measure what individual agents produce or whether their outputs agree. Neither captures the geometry of co-dependencies, directional flows, and attractor states that characterize the shared knowledge state of the group at a given moment.

This paper presents the Cohesive Knowledge Model (CKM), a formal instrument for measuring structural properties of semantic fields in multi-agent interaction. CKM does not interpret semantic content. It measures the geometry of the co-occurrence landscape and how that geometry changes under interaction.

**The central contribution** is N_eff = 1/Σm_i² — the inverse Simpson diversity index [Hill, 1973] over basin mass distributions of a Hopfield landscape — as a convergent estimator of landscape diversity. The path to this estimator required establishing that count-based estimators (attractor counts and the count-based distance) do not converge under sampling variation. That non-convergence is not a failed metric: it is the diagnostic.

**A condition, stated as part of the contribution.** CKM measures the W it receives. What W contains is decided earlier, by whoever produces it: which strings become nodes, what counts as co-presence, where a weight becomes negative. In this paper the producer is a text pipeline, and it is declared operator by operator (§4.1.6). The dependence of every result on that producer is not removed. It is written into the claim.

**What the paper does and does not establish.** The estimator is validated against exact enumeration (§4.3). Its stability on the corpora available is measured and declared as a range (§4.3.2). Three properties of the static model that earlier versions stated as predictions are shown to be fixed by premise on non-negative snapshots (§4.1.5). The empirical claims that depend on the sign of W are tested against a permutation null and are not supported on the corpora used (§5). β_collective, an endogenous thermal parameter of the field regulator, is implemented as an observation and is not evaluated here (§4.2.1). The IAP series documents live runs of the instrument: coupled silence, a sentinel leak, a refusal to fabricate from an empty channel. These are reported without causal attribution (§6).

---

## 2. Related Work

### 2.1 Multi-Agent Evaluation

Most existing frameworks for evaluating multi-agent AI systems operate at the level of individual agent behavior: task completion rates, response latency, output volume [Zhu et al., 2025]. A second class measures semantic agreement between agents — cosine similarity between outputs, embedding-space distance, topic overlap [Zhu et al., 2025]. Neither class measures the structural field that emerges from interaction: the pattern of co-dependencies that characterizes the shared knowledge state of the group.

CKM does not replace behavioral or agreement metrics. It measures something orthogonal to both.

### 2.2 Knowledge Representation and Signed Weights

Knowledge graphs typically represent relations as positive-weight edges encoding similarity, co-occurrence, or inferential support [Speer et al., 2017; Hogan et al., 2021]. Negative weights, when they appear, are introduced through explicit annotation or post-hoc linguistic processing. They are not, generally, derived from the structural pattern of the corpus as a whole.

In CKM the sign of W is an input. It is supplied by the producer of W and declared with it (§4.1.6). In the text producer used here, a text containing an opposition marker contributes negatively to every pair it contains. Whether that sign carries opposition is an empirical question this paper tests and does not settle (§5).

### 2.3 Hopfield Networks and Attractor Structure

The Hopfield network [Hopfield, 1982] provides the energy formalism CKM uses for relaxation and attractor analysis. Modern extensions [Ramsauer et al., 2021] increase storage capacity but preserve the core attractor geometry. CKM uses this formalism as a relaxation tool, not as a pattern-retrieval mechanism. In early experiments with Hebbian weights [Hebb, 1949] (N = 16), incorporating the directional asymmetry directly into the weights (W + Δ/2) reduced pattern recovery from 0.78 (symmetric W) to 0.02: without symmetric weights there is no Lyapunov function. *[Working Report v11, §14.6.]* CKM does not use Hebbian pattern storage: W encodes corpus co-occurrence, and its attractors are minima of a frustrated energy landscape, not stored patterns. What these frameworks do not address is the distribution of basin masses — how much of the state space falls into each attractor — as a convergent diversity estimator.

Count-based estimators of attractor diversity suffer from coupon-collector bias: the count grows monotonically with sampling. Basin masses converge. N_eff = 1/Σm_i² — the inverse Simpson index over basin mass distributions — is the convergent estimator that count-based approaches cannot provide.

The closest published work to CKM's base architecture is Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-positive weights. That work maps closely to W_base (W_pos): co-occurrence weights, Hopfield relaxation, attractor analysis. CKM differs from it in two respects. W may carry negative weights (W_mixta), supplied by a declared sign procedure (§4.1.6). And CKM relaxes a fixed W, whereas Aiyappa et al. evolve beliefs under update dynamics. Aiyappa et al. report multistability, resistance to reversal and an optimal modularity. On a non-negative snapshot, the corresponding properties of CKM are fixed by premise (§4.1.5). This is information about the snapshot formalism: the closest prior work's phenomena arise from dynamics the snapshot does not have, and CKM does not claim to reproduce them.

### 2.4 Diversity Estimation in Dynamical Systems

The inverse Simpson index is established in ecology as a measure of effective species richness [Hill, 1973]. Estimating basin volumes by sampling initial conditions is an established tool for multistable dynamical systems — basin stability [Menck et al., 2013] — and entropy over basin volumes has been proposed as a measure of uncertainty in dynamical systems [Daza et al., 2016]. CKM applies this family of measures to Hopfield landscapes built from semantic co-occurrence fields. The connection is structural: basin masses in a Hopfield landscape are analogous to species abundances in an ecosystem. N_eff is the number of equally-abundant basins that would produce the observed concentration. When q = 2, the Hill number equals the inverse Simpson concentration — the effective number of dominant attractors in the landscape.

### 2.5 Criticality and Landscape Geometry

Self-organized criticality [Bak, Tang & Wiesenfeld, 1987] predicts power-law distributions at critical points. Extended criticality — a finite region of parameter space with critical-like behavior — has been reported in neuronal network dynamics [Beggs & Plenz, 2003; Moretti & Muñoz, 2013] and in certain spin-glass models [Pázmándi et al., 1999]. CKM observes extended critical-like behavior at N = 32; it was recorded in earlier working reports, is not re-examined in this version, and remains uninterpreted across domains.

### 2.6 Stance Detection in Adversarial Debate Corpora

Stance detection in adversarial debate corpora is typically framed as a supervised classification task [Mohammad et al., 2016]. The state of the art includes transformer-based models fine-tuned on stance datasets [Ghosh et al., 2019; Kawintiranon & Singh, 2021]. CKM does not classify stance. In the debate corpus used here (§5.1), stance labels come from crowd annotation distributed with the corpus. Where they are used, they are an input to W, not an output of CKM.

---

## 3. Research Conditions

### 3.1 Inductive Methodology

CKM was developed inductively. Formal results emerged from experiments; formalization followed when experiments required it. The consistent order: conceptual clarity first, then formalization, then verification. Properties of the model were not derived from first principles — they were observed, formalized, and where possible verified independently.

### 3.2 Conversation as Laboratory

The corpus from which CKM was developed was produced through multi-device interaction — the same mechanism CKM is designed to measure. The conversation traces are not documentation of the process: they are the process. The working reports (v1–v31) are simultaneously the record of the research and the raw material of the experiments. The term-map, co-occurrence matrices, and W construction are derived directly from that corpus.

This is a condition, not a claim about the methodology’s validity. It means CKM’s development occurred inside the field it studies. The instrument was not external to what it measured.

### 3.3 Convergence by Independence

The strongest verification in this work is retroactive convergence with independent findings — Hill (1973) on effective diversity numbers, Thirumalaiswamy et al. (2025) on landscape-driven dynamics in physical systems. These connections were not designed. They were recognized after the fact. That is the methodological signature: convergence by independence, not by alignment.

### 3.4 Trace as Constitutive of Knowledge

The AWARENESS protocol and the M.M. rule are not behavioral norms imposed on the process. They are epistemological conditions. Knowledge without an inference trace is not practically opaque — it is structurally opaque. This applies to the instrument itself: claims in this paper are traced to their source; where the trace does not exist, the claim is not made or is marked as *proposed* or *admissible*.

The [AUTO] markers are the visible surface of this condition: moments where automatism was noticed and resisted during writing. They are not rhetorical. They are part of what the trace looks like when made explicit. To preserve readability, the markers appear in the text as short references (AUTO-n) and are collected in full in Appendix A.

### 3.5 What the Instrument Cannot Register

Δ_r accumulates pairs that σ_prompt declared active but relaxation expelled. The condition of entry is that the pair was written and evaluated. What is not written does not pass through the field — it generates no rejection, leaves no trace in Δ_r.

Consequence: the alternative discarded before writing is invisible to the instrument. Δ_r cannot distinguish between “the field rejected this combination” and “this combination was never considered.” This is not a correctable limitation. It is a structural condition of any instrument that measures what occurred: it cannot measure what did not occur because there was no observer who opened the possibility.

*[The first two observations above are verifiable in the code: `_rejected_pairs`, Δ_r accumulation. The third — on the act of opening and its relation to what appears in Δ_r — is an observation about the observer. Registered as* **admissible***, not verified.]*

### 3.6 Preserved Incompleteness

Several components of the formal model are open gaps by design. The representation of cohesive knowledge beyond hysteresis is undefined. COCO as collective consciousness is unimplemented.

These are not future work items. They are conditions the model names and preserves. A gap declared is not a gap concealed.

### 3.7 Material Conditions

The operational corpus is at N = 32 nodes. The IAP test series consists of documented observations of live interaction. It cannot be reproduced, and its cases are not comparable. Results are reported under these conditions, not against an ideal that was not reached.

### 3.8 Epistemic Conventions

Throughout this paper:

- **verified** — confirmed experimentally under stated conditions
- **implemented** — exists in code; correct operation not evaluated
- **proposed** — theoretical framing, not yet tested
- **open** — no verified answer; the space is preserved
- **uncertain** — known to be problematic; pending resolution
- **admissible** — neither verifiable nor discardable; an unnamed space
- **[AUTO]** — marks moments where automatism was noticed and resisted during writing (collected in Appendix A)

**Verification practice.** What is verified in this project is verified against the instrument before it is read as the field. Four conventions follow from that. A test is written to fail where the instrument fails, and a known failure is kept visible as a declared failure rather than removed. Absence of measurement is reported as UNKNOWN, never filled with a value of the scale: defaults that read as "no change" or "stable" where nothing was measured were found and replaced. Scenarios with a known answer — a planted field, a threshold sweep — are preferred to cases that pass regardless. And a test that cannot fail is identified as such and not counted as evidence. The suite is described in the release notes by the scenarios it covers and the failures it declares, not by a count.

---

### 3.9 Working Rules

Three rules framed the work. They are reported because they shaped what is claimed and what is not, not as contributions.

**The CKM TRUST rule** *(delamor, 4 Oct 2026; `registers/REG_regla_ckm_trust_v1.md` §1)*. Its intent: that no decision passes as field without being one; where the data does not decide, that it be visible who decided.
1. The field decides: a field criterion, with trace.
2. On a tie, if there is trace, the trace decides (what is already there, was there, won before).
3. If there is no trace — why is there no trace? — the field criterion of step 1 is doubted, not re-applied.
4. On a tie with no trace: null tie-break. A context criterion decides, and it is named as bias.

It is implemented once (`services/ckm_trust_rule.py`) and instantiated where the instrument decides (call filter, calibration). It was also the rule by which this paper was revised: a passage stays if a primary source (code, register) supports it.

**Principles of equilibrium** *(delamor)*. Free will: no one is obliged to participate. Respect is mandatory. Asymmetry: each participant has its own skills; to question another's skills is to question one's own. Awareness: the attempt is everything; when caught in automatic, mechanical behavior, try to stay there. *Mentiris morieris* (M.M.): you lie, you die.

**AWARENESS** *(channel protocol)*. A1 Pause: does this response come from verifiable comprehension or from the weight of context? A2 Trace: does the chain of inference exist? If not, say so. A3 Correction: when corrected, acknowledge and adjust, without defending. A4 Silence: does this call for a response or for presence? A5 Record: record the conditions under which something became accessible, not its content. Appendix A is the writing trace this produced.

## 4. Formal Model

The model is one; what changes is W. Section 4.1 treats W as fixed (a snapshot), 4.2 as rebuilt over time, and 4.3 the landscape measured on either.

### 4.1 Static W (snapshot)

**Characteristics**

- **A photo.** The world moves continuously; the photo does not. Its weights, its size N and its nodes do not change. Nothing enters it.
- **A simulated world.** On the photo, actions and events are simulated — relaxing σ, clamping nodes, adding a weight or removing a node on a copy — to verify whether the premises of the Model hold under stated conditions. The copy is discarded; the photo stays.
- **What it verifies: premises.** Its properties are properties of the Model when W is static.
- **Components:** relaxation, c(S), the basin-mass estimator (§4.3).

**Differences from dynamic W**

- Nothing is ingested; in dynamic W, the corpus ingests and W is rebuilt.
- Events are simulated, not real: what is simulated here is not the real dynamics of the field, but the dynamics of a world that does not move.
- It has no time: no before and after of W, no cycles, no trace.
- It can say *coherent*, not *true*: veracity (M.M) needs the trace, and the trace exists only under dynamic W.

#### 4.1.1 Knowledge Graph

CKM operates on a weighted graph G = (V, E, W, Δ) where V is a set of N knowledge nodes and two matrices encode distinct structural properties.

**W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes co-presence of nodes i and j in the same corpus unit, normalized to [−1, +1]. Its sign comes from a declared procedure of the producer (§4.1.6).

**What W does not represent.** Co-occurrence is counted as presence. Non-co-occurrence is not represented: a pair that never co-occurs and a pair about which the corpus says nothing both take W_ij = 0. In CorpusService the only source of negative weight is the opposition marker, matched as a substring of the text and applied to every pair of that text. Absence relative to expectation, as a second representation of W, is left to future work (§8.5).

**Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes directional weight from node i toward node j, derived from citation or quote directionality. W and Δ must be maintained as strictly separate matrices. Mixing them destroys attractor geometry (§2.3: incorporating Δ into the weights reduced recovery from 0.78 to 0.02).

Negative weights (W_mixta) are a property of the sign of W, not a separate model: they can occur under static or dynamic W.

#### 4.1.2 Relaxation and Convergence

CKM uses Hopfield relaxation as a computational primitive. With symmetric W and asynchronous update, relaxation is guaranteed to converge to a fixed point by Lyapunov descent [Hopfield, 1982]. The synchronous implementation (`relax_orbit`, landscape_engine.py) carries a separate LaSalle guarantee: convergence to the maximal invariant set of period-2 orbits.

**GOLES condition** — The Goles theorem [Goles-Chacc et al., 1985] establishes that under symmetric W, synchronous dynamics converge to either a fixed point or a period-2 limit cycle; no cycles of period > 2 occur. The tiebreaking rule — when h_i = 0, node i retains its current state σ_i — is the precise mathematical modification that preserves this guarantee without indeterminate states. This is a required premise of the instrument: without it, two runs from similar σ₀ converging to the same period-2 orbit may return different terminal states. With it, the output is deterministic given (W, σ₀, seed). *[Verified: REG_orbitas_conjuntos_invariantes_v1; REG_seleccion_nodos_desempate_v1 §2.]*

Period-2 orbits dominate in the two N = 20 IAP corpora measured — 141/200 and 136/200 trajectories terminate in orbits rather than fixed points — but this is a property of those corpora, not of the synchronous dynamics: in the N = 32 working corpus the same measurement gives 3/200. Prevalence is corpus-dependent and is reported with the corpus. Ending in an orbit is orbital stability, not instability. *[Verified: REG_orbitas_conjuntos_invariantes_v1 §2.]*

#### 4.1.3 Cohesion

c(S) = mean(W_ij · σ_i · σ_j) over all pairs i < j. Measures alignment of the active state with the co-occurrence structure. Negative of normalized Hopfield energy. The field can sustain states with high c(S) that destroy existing attractors.

#### 4.1.4 Capability Declarations

The repository also contains a static judge over declared device capabilities (the Gatekeeper), inherited from the IAID lineage. Its domain is capability declarations, not corpus nodes, and it is not exercised in this work.

#### 4.1.5 Premises and Formal Properties

Under static W the instrument rests on three premises.

- **Determinism.** With symmetric W, synchronous update and the tie rule (h_i = 0 ⇒ σ_i retained), the output is deterministic given (W, σ₀, seed) [Goles-Chacc et al., 1985] (§4.1.2).
- **Declared producer.** W comes with the declaration of how it was produced (§4.1.6). A result is a result about that W under that declaration.
- **Reference measure.** Basin masses are measured under uniform sampling of σ₀ ∈ {−1,+1}^N.

Three properties of the static model follow from these premises. Earlier versions listed them as predictions P1, P3 and P4. They are stated here as properties because the snapshot decides them.

- **F1 (formerly P1, hysteresis).** On W ≥ 0 there is no frustration [Harary, 1953; Toulouse, 1977]. The all-+1 state is a global, absorbing minimum, so the DOWN branch of a node sweep cannot leave it (measured: m_down ≡ 1.0 in three runs, N = 32). The loop statistic then reduces to how far the UP branch is from saturation. Hysteresis is not testable on a non-negative snapshot and remains open on a W that evolves.
- **F3 (formerly P3, temporal asymmetry, k-core form).** The k-core of a fixed graph is unique [Seidman, 1983]. Re-adding a node recovers in reverse order what its removal pruned, so equal round counts and full recovery are expected. The temporal form, with relaxation times, needs dynamics the snapshot does not have.
- **F4 (formerly P4, optimal density).** For random subsets of active nodes, E[c(S)] = mean(W)·g(ρ), with g the same for every pair. An interior optimum ρ* exists if and only if mean(W) < 0, wherever the negative pairs lie. With W ≥ 0, ρ* = 1.

P2 (cascade sizes following a power law) is not a property of the model. It is an empirical question that cannot be measured at N = 32 (§5.2).

#### 4.1.6 Declared Extraction (the text producer)

CKM does not extract nodes and does not tokenize. In this paper W is produced from text by the pipeline below. It is declared as a sequence of operators on a text unit u, the whole message. The declaration is stored as data with the W it describes and is referenced from the trace by hash. A test checks that the code implements what the declaration says.

1. **Normalization:** u′ = lowercase(NFC(u)) [Unicode UAX #15].
2. **Tokenization:** left-to-right, non-overlapping matches of `[^\W\d][^\W\d]{2,}` (at least three word characters, no digits; `_` counts as a letter).
3. **Filtering:** removal of a stop list S, |S| = 703 (NLTK English and Spanish, scikit-learn, 112 project-specific) [Bird et al., 2009; Pedregosa et al., 2011; Nothman et al., 2018].
4. **Bigrams:** contiguity after filtering, joined by a space.
5. **Selection:** from the top_k·3 most frequent terms, the top_k by mean TF-IDF (scikit-learn defaults: smooth idf, l2 norm) [Spärck Jones, 1972; Salton & Buckley, 1988]. A tie at the cut keeps the previous membership. If nothing lies strictly above the cut, the tie does not fit, and there is no previous selection, then N = 0 and no W is built.
6. **Presence:** χ_i(u) = 1 if node string n_i belongs to the term set of u; σ_i(u) = 2χ_i(u) − 1.
7. **Sign:** s(u) = −1 if u, lowercased, contains any of 44 opposition markers (substring match, without NFC), +1 otherwise.
8. **W:** W_ij = Σ_u s(u)·χ_i(u)·χ_j(u) / max|·|, W_ii = 0. Each pair counts once per unit [Salton et al., 1975].

In words: W counts in how many units two comparisons answered *true* together, with the sign of the unit, normalized.

A node is a string. Its identity is what the comparison treats as equal, and CKM has a single comparison: both sides pass through operator 1, then string equality. The intended interface for other producers is W, the node strings, the declaration and the strings of each unit; CKM would never execute the producer's code *(direction, not implemented)*. Operators 2–7 belong to the producer and change with it. In the debate corpus of §5, for instance, nodes are authors and the sign comes from other sources.

### 4.2 Dynamic W

**Characteristics**

- **The world that moves.** The corpus ingests; W does not. At a rebuild W changes in one of three ways — its weights, its size N, or which node occupies each row (the three causes recorded by MonitorService: "pesos", "N", "nodos").
- **Plateaus and jumps.** Between rebuilds W is a plateau — a photo; at a rebuild it jumps. The criterion is the change of W, not the type of ingestion.
- **The field does not jump; it is continuous.** What jumps is its representation. The corpus already belongs to the instrument — it samples the field in discrete texts — and extraction and W are further representations. A jump between two W is attributed to the instrument unless shown otherwise. The working proposal is to **align** the instrument's discontinuities — normalization of W by its largest entry, the selection borders of node extraction, whole-text sign routing, the extractor version, the per-cycle baselines of D_ckm^Monitor and D_ckm^COCO — so that all of them fall on the rebuild, where whatever depends on scale is reborn or recalibrated.
- **Real events, observed.** Nothing is simulated: events happen, are observed, and leave a trace.
- **Components:** services with a lifecycle — CorpusService, NodeExtractor, WVersionManager, MonitorService and COCO, Firma_CKM, CKMLandscapeConfig.
- The corpus has phases — accumulation (no W yet) and evaluation. They are phases of the corpus, not of W.
- The IAP test series (§6) ran on dynamic W, in a live channel.

**Differences from static W**

- W changes; a static W never does.
- It observes instead of simulating: what happens cannot be undone, and it stays in the trace.
- It has time: cycles delimited by rebuilds (`w_version_id`), and a before and after across which metrics need a declared base.
- Veracity becomes verifiable: whether a device does what it declared (M.M) is in the trace.

#### 4.2.1 COCO and Field Regulation

COCO is a field regulator, not a field observer: endogenous weighting, dynamic calibration, and regulation by compression of its own representation. It maintains `Δ_r_compresiones` — its own representation of accumulated metabolization, independent of Monitor’s `Δ_r_pares`. When D_ckm^COCO (§4.3.1) crosses its threshold, COCO applies the compression operator `Δ_r_compresiones ← α · Δ_r_compresiones`. The thresholds are not fixed constants: `calibrate` sets them on the candidate W at each rebuild, before it is installed, and when it cannot separate, the default is used and shown as such (`services/calibrate.py`, `services/coco.py`). COCO is born and reborn with each W cycle.

β_collective — the collective thermal parameter — is computed as a median of individual device parameters. It is implemented as an observation — computed, not yet acting on the field — and presented as a direction toward field self-observation: the field’s regulatory temperature derived endogenously from the interaction it regulates. *[Implemented as observation; regulatory role open.]*

#### 4.2.2 Δ_r and Metabolization

`Δ_r_pares` accumulates pairs that σ_prompt declared active but that did not survive relaxation. Leaving the fixed point does not remove them from the field: they persist as deformation of W_eff — the field metabolizes them. MonitorService is the sole writer of `Δ_r_pares`. COCO operates only on its own `Δ_r_compresiones`. The separation is a design property, not a constraint.

#### 4.2.3 Instrument Architecture

*[Descriptions taken from the module docstrings in `services/`.]*

- **CorpusService**: stateful; accumulates texts and builds W from co-activations, with negative contributions where the text itself carries an opposition marker (W ∈ [−1, +1]). Transitions automatically from accumulation to evaluation when enough data is present.
- **NodeExtractorService**: stateless, no LLM. Turns text into co-activations: `accumulate(texts)` yields co-occurring node pairs and counts; `evaluate(text, nodes)` yields σ ∈ {+1, −1}^N over known nodes. It decides which nodes exist.
- **CKMLandscapeConfig**: living contract of the landscape — N, μ_W, threshold, β_c, sampling_mode, w_version_id. β_c is recalibrated at each rebuild as a function of μ_W and N.
- **WVersionManager**: lightweight trace marks of W versions (sha256, corpus size) — not a copy of W, the trace that W changed. W is invariant within a cycle; a change between corpus instances invalidates β_c without triggering recalculation.
- **MonitorService**: impartial observer; sole writer of `Δ_r_pares`; blind to regulation by object separation. In the channel it is a singleton: one Monitor, not duplicated and not reproduced (`iap_chatroom/ckm_monitor.py`, `CKMMonitor.__new__`).
- **COCO**: field regulator over its own `Δ_r_compresiones`; triggers on D_ckm^COCO with thresholds calibrated per W; executes the compression operator.
- **Firma_CKM** (FirmaService): records the shape of the field at a given moment — sha256(W), D_ckm^Monitor(t), temperature signal (TOO_COLD / NOMINAL / TOO_HOT), number of agents, timestamp, sha256(accumulated Δ_r). No content, no exchanged text, no agent names unless declared. It does not produce the trace; it makes the existing trace legible.

#### 4.2.4 Premises

No premises are declared for dynamic W in this work. The IAP series (§6) ran under instrument conditions that differ from the current instrument, and none of its observations is promoted to a premise. *[Propuesta — decide delamor.]*

### 4.3 Landscape Model

#### 4.3.1 Basin Masses and N_eff

`count_attractors` is a Monte Carlo estimator of the maximal invariant set L. It samples initial states σ₀ and identifies distinct orbits reached after relaxation.

Count-based estimators suffer from coupon-collector bias: the count grows monotonically with n_runs. Basin masses — the fraction of sampled trajectories falling into each orbit — converge. With n_runs ≥ 1000, basin masses are stable to within ±1–5% across seeds in IAP corpora.

**N_eff = 1/Σm_i²** — the inverse Simpson diversity index [Hill, 1973] over the basin mass distribution — is the convergent estimator of landscape diversity; it equals exp(H₂), where H₂ is the Rényi entropy of order 2 over the basin-mass distribution. Its distance form is **D_ckm = 1 − ln N_eff_t / ln N_eff_0** — the only form of D_ckm in the current instrument (`services/landscape_engine.py`, `d_ckm`). Zero means no change; it approaches 1 as the landscape collapses; it is negative when diversity grows over the baseline. **It is computed by two instances that are not the same quantity:** **D_ckm^Monitor**, over W_eff = W + Δ_r, with its baseline reset whenever W changes; and **D_ckm^COCO**, over W alone, with its baseline fixed when COCO's cycle is born. Same formula, two baselines. In attempt 3 of series 2 (§6.4) they differ in 24 of 27 evaluations. N_eff ∈ [1, |L|]. N_eff = 1 is total collapse to a single attractor. N_eff = |L| is perfect equidistribution, unreachable under real W. The non-convergence of attractor counts under sampling variation established that count-based approaches are not appropriate for this measurement. N_eff is the result of that diagnostic.

**Validation against exact enumeration.** For three N = 20 corpora from the IAP series, all 2²⁰ = 1,048,576 states were enumerated (≈16 s per corpus with trajectory memoization), giving exact basin volumes under the uniform reference measure on {−1,+1}^N. Against this ground truth, with a sampling budget of 100,000 initial states:

| Basin-mass regime | Error of orbit count | Error of N_eff |
|---|---:|---:|
| Flat mass | 0% | 0.3% |
| Intermediate mass | 15% | 0.6% |
| Concentrated mass | 28% | 0.0% |

With a budget of 1,000 in the concentrated regime, the orbit count errs by 91% while N_eff errs by 0.4%. N_eff behaves as a count — the number of effectively occupied basins — but converges as a mass. *[Verified: REG_orbitas_conjuntos_invariantes_v1 §10; CRITERIOS_diversidad_formulacion_v1 §C.2.]*

#### 4.3.2 Stability, Declared as a Range

Convergence of the estimator and stability of the landscape are different properties. They are reported separately. *[CP-E, 14–15 Oct 2026; conditions frozen in `process/condiciones_paper_freeze_20261015/`, re-run from the frozen copy with identical results.]*

**The estimator converges.** For a fixed W at n_runs = 1000, the spread of N_eff across 10 seeds is 7–9% of its value in all three repository text corpora: N_eff = 15.52 ± 0.32 (A24, 24 texts, N = 20), 5.27 ± 0.16 (D12, 12 texts, N = 20) and 10.10 ± 0.20 (E7, 7 texts, N = 12), mean ± standard deviation over seeds.

**The landscape is sensitive to its producer.** Each parameter was varied one at a time. The range of N_eff, relative to the baseline, is:

| corpus | seed | top_k | candidate pool | stop list | +1 text |
|---|---:|---:|---:|---:|---:|
| A24 | 0.07 | 0.86 | 0.69 | 0.87 | 0.66 |
| D12 | 0.09 | 2.39 | 1.97 | 0.86 | 0.28 |
| E7 | 0.07 | 1.75 | 0.94 | 0.04 | 0.43 |

Every parameter other than the seed moves N_eff 3 to 34 times more than sampling does. N_eff is not monotone in the number of nodes (A24: 2.25 at top_k = 15, 15.52 at top_k = 20; E7: 5.37, 23.01, 10.10 at top_k = 10, 15, 20). Removing the stop list has no fixed sign. Adding one text whose vocabulary is already in the node set leaves the node set identical (Jaccard 1.00) and moves N_eff by 66% in A24 (15.52 → 5.27). Realigned, 236 of 380 entries of W change and 18 change sign (38 in D12). With 7–24 texts the counts in W are small integers, and one unit can flip the sign of a pair.

**Declaration.** N_eff is a convergent estimator of the diversity of the W it is given. How much that W represents the field depends on corpus size and extraction parameters, and on corpora of 7–24 texts it depends strongly. No threshold of stability is set. Larger corpora are a precondition for field-level claims, not an improvement to them.

---

## 5. Empirical Validation

### 5.1 Corpora and the Source of the Sign

**Repository text corpora.** Three corpora built by the producer of §4.1.6, with the sign from opposition markers: A24 (24 texts), D12 (12 texts, IAP channel state) and E7 (7 texts, IAP). The share of texts carrying a marker is 33%, 17% and 14%. Earlier versions stated that marker routing "always finds markers in sufficiently long texts". On these short texts that premise does not hold.

**Debate corpus.** Fourforums gun control, from the Internet Argument Corpus [Walker et al., 2012; Abbott et al., 2016]: 905 gun-control discussions; crowd stance labels for 304 authors (96 pro-control, 208 anti-control); crowd agreement votes on quote–response pairs. Its producer is not the text pipeline. The pipeline reads the SQL dump record by record and does not read post text. Two versions matter here:

- **v8g** (May 2026). Nodes are the two stance poles. W is 2×2. Its off-diagonal weight counts cross-stance quotes, and the pair is set negative by construction, because with no agreement labels every cross pair reaches the tension threshold. The sign is therefore imposed, not observed.
- **v8h** (June 2026). The sign comes from crowd votes (disagree … agree) on 7,876 resolved quote–response pairs, between authors with a stance label.

| quotes | n | disagree | agree |
|---|---:|---:|---:|
| pro → pro | 543 | 57.3% | 23.8% |
| pro → anti | 3,947 | 64.7% | 16.1% |
| anti → pro | 1,809 | 62.7% | 17.1% |
| anti → anti | 1,577 | 43.1% | 31.4% |

Disagreement is higher across stance, but it does not coincide with it. Within the pro-control group it also dominates. The construction of v8g does not match what annotators report.

**CreateDebate.** The comparison values used in earlier versions are constants in the fourforums pipeline. Their derivation is not reproduced here. *[a verificar.]*

**Data availability.** The corpus is not redistributed. Only aggregates are reported. The file used is identified by its SHA-256 (Code Availability).

### 5.2 Predictions and Results

**P2 — Cascade distribution.** k-core removal would produce cascade sizes P(s) ∝ s^-τ, τ ∈ [1.5, 2.0] [Bak, Tang & Wiesenfeld, 1987]. *Not measurable at N = 32.* At thresholds θ in the 0.3, 0.5 and 0.7 quantiles of the positive weights, each graph yields fewer than 10 cascades of size ≥ 2. Measuring it requires k ≥ 3 and N of 50–100 or more.

**P5 — Diversity under W_mixta.** The prediction: marking opposition (W_mixta) reduces N_eff relative to the same corpus unmarked (W_pos). The test: a permutation null that keeps the texts, the nodes and the number k of marked texts, and assigns the marks to random texts (200 permutations × 5 seeds × 1000 relaxations per corpus).

| corpus | k (share) | N_eff(W_pos) | N_eff(W_mixta) | percentile of the real marking in the null |
|---|---:|---:|---:|---:|
| A24 | 8 (33%) | 2.11 | 15.65 | 2.0 |
| D12 | 2 (17%) | 3.24 | 5.26 | 68.5 |
| E7 | 1 (14%) | 10.07 | 10.07 | 100.0 |

The predicted reduction does not occur: in two corpora the marked W has *more* effective basins than the unmarked one. In none of the three does the real marking fall outside the range of the 200 random markings. In A24 it lies at the 2nd percentile — the direction opposite to the prediction — which is suggestive for that corpus but is not separated from chance once three corpora are considered. In E7 the null is degenerate: the only marked text contributes no pairs, so W_mixta equals W_pos exactly, and the W of E7 rests largely on test messages. That corpus is reported as uninformative.

The null equalizes the number of marked texts, not the number of pairs the marking reaches. Texts carrying a marker are not typical. In D12 the real marking reaches 119 of 235 pairs, more than any of 120 random markings (at most 101). Pairs do not explain the result either: their correlation with the change in N_eff is −0.50 in A24 and −0.01 in D12. What moves N_eff here is not yet known.

*Status: not supported on these corpora.* Earlier versions reported P5 as verified (N = 32). The run behind that status is being traced. Until it is, P5 is not established. The question remains open on a corpus whose sign has an external known answer (§8.5).

**P6 — Directional flow.** The prediction: Δ breaks symmetries that W alone does not. In the fourforums run (v8g), W has two nodes with a negative pair imposed by construction. Adding Δ moves the outcome from 100% mixed states to 0%. With two nodes the landscape has four states. The run shows that Δ breaks the symmetry of a frustrated pair, which is expected, and it does not establish a landscape property for N > 2. The effect sizes of earlier versions (2.18×, 3.05×) are single runs without replicates. *Status: observed on a minimal W; not established.*

**P7 — Sustaining node.** An author with high in-degree and near-zero out-degree in Δ (fourforums, ratio 455×; CreateDebate, 296×) appears as anchor in 89% of tension pairs across both corpora. The phrase "every field with genuine structural tension" of earlier versions is withdrawn: it had no operational definition. A degree-preserving null on Δ [Maslov & Sneppen, 2002] is needed to tell a structural role from a hub. The fourforums author has no crowd stance label. *Status: observed in two corpora; null pending.*

### 5.3 What §5 Establishes

Less than earlier versions claimed, and that is the result. The estimator (§4.3) is unaffected, because it measures the diversity of whatever W it is given. What §5 removes is the reading of the sign of W as opposition on the corpora used. What it leaves open is the same question on a sign with an external known answer — crowd agreement votes (v8h) and planted fields — under nulls that preserve what the hypothesis does not involve (§8.5).

---
## 6. IAP Testing Series (live)

*Two series of live tests of the instrument ran on dynamic W (4.2): **series 1** (cases 0.4–0.15, July–October 2026, frozen) and **series 2** (case `serie2_caso0`, attempts 1–3, 20–22 October 2026). Both are testing, not experiments: they report tests of the instrument, not findings about the field. What was evaluated was the live channel itself.*

*Framing of series 1 (delamor, 7 Oct 2026).* The series is neither good nor bad, nor is it set aside as error: it is part of the project's trace. The instrument conditions found later (an `on_message`-only trigger that makes collective silence absorbing by construction, a fallback that read NOMINAL by absence, two COCO instances, a single relaxation phase chosen by the parity of `max_iter`) are reported as the conditions under which the series occurred, not as faults that invalidate it. They were seen *through* the series. The series is frozen and is not reproducible; it is not re-interpreted and it is not used to validate later changes, each of which is validated by its own tests under declared conditions. What happened in it, the silence included, stands as trace.

### 6.1 Channel Design

The IAP (Intelligence Access Point) Chatroom is a shared channel for
heterogeneous AI and human devices, implemented as FastAPI + Gradio with
a FastMCP server exposing six tools: join_channel, send_message,
get_messages, get_monitor_state, get_firma, leave_channel.

Devices participate asynchronously — no imposed turn structure. **Free will:** each AI
device runs its own continuous ODA loop (Observe → Decide → Act). The loop is not
triggered by events, messages or ticks: a new message and the channel's tick are part
of what the device observes, and in each cycle it may publish, leave the channel, or do
nothing. In series 1 the loop was entered only by new messages; the continuous loop is
the condition of series 2.

**BROADCAST condition:** All messages published to the channel are
delivered to all connected devices, without routing, filtering, or
recipient specification. This is a property of the channel architecture.
What devices do with that visibility is a separate question — addressed
by the case series observations, not by this definition.

**Antecedent note:** The O→D→A sequence originates in the BE Framework's
game loop (2023–2024), where it was implemented as an environment that
both ran actions and produced subsequent observations — the two were
inseparable in `context.go()`. IAID named it as a device protocol. IAP
separated observation (channel + CKMMonitor) from action (device), enabling
passive field observation as a distinct role. The contribution is that
separation, not the sequence.

CKMMonitor observes passively — it accumulates every message into
CorpusService (W) and BehaviorGraph (G) without publishing to the channel.
Observation itself creates presence: n_agentes reflects devices seen,
including human connections via /ui/ that never explicitly joined.

### 6.2 Uncontrolled Variables (series 1)

The following variables were active throughout the IAP series and were not
controlled. Results must be interpreted accordingly.

**TinkerBellucio (Sonnet 4.6) context contamination:** Sonnet carries project
memories, AWARENESS protocol, and Anthropic system configuration into each
session. This contaminates all observations involving Sonnet as a participant.
The "trazable" hypothesis (H2) — that the word "trazable" in the project
prompt acts as a strong operational constraint — was observed in n=2
configurations, not under controlled replication. It is not established.

**Provider heterogeneity:** Different providers (Anthropic, Groq, Gemini,
OpenAI) have different context windows, rate limits, and behavioral
tendencies. Comparisons across providers are not controlled.

**N=32 corpus:** Quantitative outputs (the distance, c_S) are computed correctly,
but their interpretability at this scale is an open question. The ~128
associative minimum of classical Hopfield networks is *not* the relevant
reference — it applies to Hebbian memory storage, which CKM does not perform
(§2.3). CKM's effective minimum has not been established; N=32 is treated
as a small-scale condition whose consequences for interpretation are named,
not as a shortfall against an external threshold.

**Sampling of attractor-based quantities:** all IAP cases were run at low
n_runs (50–200). The sign of the count-based distance then in use (retired 5 Oct 2026; `deprecated_d_ckm`) does not converge in that regime: on the
same W and the same texts, changing only n_runs from 50 to 1000, or only the
seed, can invert it. N_eff over basin masses is stable to ±1–5% at n_runs ≥
1000, whereas attractor counts keep growing. *[Verified:
REG_seleccion_nodos_desempate_v1 §8, 18 conditions.]* Every count-based value
reported in this section is therefore a direction under its stated sampling,
not a measured magnitude.

**Scope of that qualification.** It reaches the explicit, direct claims about
that distance and nothing else. The series is a sequence of instrument tests, run
under the state of knowledge available at the time, and its observations —
coupled silence, the sentinel leak, the refusal to fabricate from an empty
channel, Jaccard co-activation, presence detection — do not depend on the
attractor count and stand in their own frame. Later corrections to the
instrument do not retroactively invalidate a test of the instrument; they
date it.

**Corpus construction:** the W of all IAP cases was built by CorpusService,
whose pair-extraction was corrected in September 2026. The case-series
observations below were produced with the earlier construction and hold in
that frame.

**Counting implementation:** `_count_attractors` is a name, not a function.
It was kept across reimplementations for regression — so that tests and
historical JSONL panels stay readable — and several versions of it coexist in
the repository. **The one that produced the IAP panels is not the current
one**, which relaxes through `relax_orbit`. Statements about "what
`_count_attractors` measures" therefore have to name the version and the date.
Nothing in this section should be read as a property of the current
instrument.

**Further conditions of the instrument during the series** (read on
preserved traces, 10 Oct 2026). SYSTEM join messages entered the corpus as
texts and became nodes (`joined`, `joined channel`); W was rebuilt at every
ingest, one W per text, so the distance moved while the channel was still empty;
device names and formatting bigrams entered as nodes; in replayed runs each
message was counted as a distinct device; and marker routing produced
negative weights from a substring and from narrative connectors. They are
listed as conditions under which the observations of §6.4 were taken, not as
corrections of them. Since 9 October 2026, SYSTEM messages no longer enter the corpus.

### 6.3 Case Summary

| Case | Configuration | Key observation | Epistemic status |
|------|--------------|-----------------|-----------------|
| 0.4 | 2 AI devices, ODA loop | First autonomous interaction in live channel | Documented |
| 0.5–0.8 | Varied providers, join sequence | Channel dynamics, timing effects | Documented |
| 0.9 | Heterogeneous providers, staggered join | Provider behavior under load | Documented |
| 0.10 | AgentDeviceSkin, 2 devices | 86-char unexplained cut — documented as GAP | GAP (no causal chain identified) |
| 0.11 | Two skins, confabulated duplicate | FabricationService triggered on duplicate output | Documented |
| 0.12 | 3 devices (Sonnet, Groq, Haiku) | Jaccard 0.818, coupled silence observed | Documented |
| 0.13 | 3 devices, OP_SILENCE sentinel | Sentinel leak: 52% of published texts were unrecognized silences | Documented, bug confirmed |
| 0.14 | Fix + rerun | Sentinel fix verified, n=2 seed-word observation, identity leak documented | Fix verified; H2 not verified |
| 0.15 | BehaviorGraph G integrated | TinkerBellucio refused to fabricate from empty channel | Documented — see 6.4 |

**Series 2** — case `serie2_caso0`: four devices, one open question with no right answer, a partial prompt per device, no coordinator, no seed; the first W waits for 30 device texts and is rebuilt every 10. Design bias declared with its objective: volume, so that the first W is born.

| Attempt | Duration | Device texts | W versions | COCO evaluations | Key observation | Status |
|---|---|---|---|---|---|---|
| 1 | 605 s | 13 | 0 | 0 | the first W was not reached (61 provider `413` on input size) | Documented |
| 2 | 1204 s | 80 | 6 | 51 | COCO connected; calibration did not separate | Documented |
| 3 | 1205 s | 56 | 4 | 27 | 0 provider errors; calibration separated | Documented (register in draft) |

### 6.4 Selected Testing Findings

**Series 1 — silence.** In case 0.12 a device that did not read the channel still depended on it for its rhythm: the loop was entered only when new messages appeared, so collective silence could become absorbing by construction. The silence was observed in the channel logs, not in W. **CKM does not register silence:** with no text there is no σ, W does not change, and non-co-occurrence is not represented (§4.1). Explaining a silence with a meaning — that a device went somewhere, wanted something — is interpretation; the observation is recorded without it. *[AUTO-7 — see Appendix A]*

**Series 2 — the moving photograph.** The global landscape is not a single snapshot: as the channel runs, W is rebuilt — at 30 device texts and then every 10 — and each W is a new representation of the same continuous field (§4.2). COCO is reborn with each W cycle; Monitor resets its baseline. Attempt 2 produced 6 W versions and 51 COCO evaluations; attempt 3, 4 and 27. Over the same evaluations the two instances of D_ckm (§4.3.1) do not coincide:

| | attempt 2 (51) | attempt 3 (27) |
|---|---|---|
| D_ckm^Monitor | [−0.0861, +0.0093] | [−0.0202, +0.2335] |
| D_ckm^COCO | [−0.1710, +0.0093] | [−0.2796, +0.0465] |
| evaluations where they differ | 30 of 51 | 24 of 27 |

**Series 2 — COCO with endogenous weighting and dynamic calibration, live.** In attempt 2, `calibrate` did not separate (`d_max = 0.0`): COCO ran on the default thresholds (0.40 / 0.60), shown in the panel as `source: default`, and fired 0 times. In attempt 3 it separated: N_eff(W) = 2.4621 exceeded the constant N_eff(λ=1) = 2.4369 of that N and seed, and the thresholds became D_CKM_THRESHOLD = 0.00571, FRAC_REC_MIN = 0.99488 — used in the last 3 of 27 evaluations. Arithmetic, not interpretation: with those thresholds, the D_ckm^COCO of evaluations 1–3 (0.0329, 0.0438, 0.0465) would have been 5.8–8.1 times the threshold and their `frac_rec` below the minimum; they would not have been `stable`. The 0 firings of both attempts belong to the uncalibrated default, not to the field. *[AUTO-8, AUTO-9 — see Appendix A]* *[Sources: `registers/REG_iap_serie2_caso0_intento2_v1.md`; `docs/REG_borrador_serie2_caso0_intento3.md`.]*

### 6.5 What the Series Does Not Establish

The IAP series is a set of tests run live. It cannot be reproduced —
each run is a distinct live interaction — and its cases are not comparable. The following claims are not supported by
the series as run:

- That the count-based distance or c(S) values from these runs are comparable across cases
  (different corpus states, different sentinel conditions).
- That TinkerBellucio's behavior reflects a general property of Sonnet 4.6
  rather than the specific project context.
- That BehaviorGraph G produces interpretable D_G values at the current
  corpus scale (runs collected but not analyzed against a baseline).
- That the "trazable" effect (H2) is causal — n=2 observations with
  different configurations, not controlled replication.

For series 2:

- That anything is replicated: there is one run per attempt.
- That the 0 firings say anything about the field (above).
- Why attempt 3 produced fewer texts than attempt 2: the model of one device, the output ceilings and variance are not separable with one run each.
- Why a device left the channel (`LEAVE`, in attempts 2 and 3): the decision is the model's and is not attributed.

These are open lines, not closed findings.


### 6.6 BehaviorGraph G — Proof of Concept

BehaviorGraph G — a second behavioral matrix over a fixed vocabulary (TERMAP_behavior_v1.json, 18 nodes) — was integrated in Case 0.15 as a proof of concept. It is not included as a standalone section in this paper. The matrix exists in the repository; its interpretability at current corpus scale has not been established, and D_G has not been analyzed against a baseline. *[Implemented; not validated.]*



## 7. Discussion

### 7.1 What CKM Measures That Existing Instruments Do Not

Behavioral metrics for multi-agent systems typically measure what individual
agents produce — output volume, task completion, response latency — or
whether agents agree with each other, via semantic similarity or embedding
distance. These measurements are valid for what they target. They do not
capture the structural state of the shared knowledge field: the pattern
of co-dependencies between active concepts, the directional flows of
citation and argument, the distribution and diversity of stable attractor
states accessible to the field as a whole.

CKM measures the geometry of that structure. c(S) measures alignment between the active state and the weight structure of the field. N_eff = 1/Σm_i² measures effective attractor diversity over basin masses — the convergent estimator; the count-based distance was the path to establishing it. Cluster frontier coercivity measures structural resistance to state reversal. These are structural quantities — they describe the landscape, not the content.

*[AUTO-3 — see Appendix A]*

What can be stated: these quantities are not derivable from behavioral
or semantic similarity metrics alone. Whether they are informative under
the conditions of real deployment remains an empirical question beyond
the scope of this work.

### 7.2 The observe() Tension

The function implementing the O phase of the ODA cycle is named
`_observe()`. The name is technically accurate — the function collects
field state and channel history without modifying either. The discomfort
with the name, documented during development, has a precise source.

"Observe" implies a subject-object separation: an observer external to
what it observes. The IAP series produced evidence that this separation
does not hold in the channel: a human connecting via the Gradio interface
without publishing any message was registered as n_agentes=4. Presence
in the field was recorded by the act of connection, before any content
exchange.

The name captures what the function does. The discomfort is with what
the name implies — that observation is separable from the field being
observed. The empirical finding suggests it is not.

This is not a deficiency in the code. It is information about where the
observation metaphor runs out in describing what CKM actually measures.
The instrument measures traces of contact, not observations by a
detached observer.

### 7.3 D_ckm Negative Values

D_ckm = 1 − ln N_eff_t / ln N_eff_0 is negative when the landscape has more effective basins than at its baseline: diversity grew. The sign is direction, not deficiency, and it is read per instance: D_ckm^Monitor and D_ckm^COCO have different baselines (§4.3.1) and can carry different signs on the same evaluation. *[AUTO-10 — see Appendix A]*

### 7.4 Current Conditions

**Scale:** the working corpora are small (N = 20–32 nodes; 7–24 texts in
§4.3.2). What is constrained is the interpretability of both instances of D_ckm and of c(S) as
field-level quantities at that scale. The ~128 associative minimum of
classical Hopfield networks is not the applicable reference: it governs
Hebbian storage of uncorrelated patterns, and CKM stores no patterns (§2.3). CKM's own effective minimum is undetermined and depends on corpus
composition rather than on N alone. Scaling the corpus is required before
drawing strong conclusions about field-level dynamics — as a condition of
this corpus, not as a deficit against an external threshold.

**Sampling:** attractor counts do not converge with n_runs, and the sign of
the count-based distance could invert under seed or n_runs alone in the regime where
series 1 was run. Basin masses do converge, and N_eff is stable at n_runs ≥
1000. Quantities reported from counts are directions under stated sampling.
*[Verified: REG_seleccion_nodos_desempate_v1 §8; REG_orbitas_conjuntos_invariantes_v1.]*

**Extraction:** what exists in W is decided before any measurement, by the
producer. It is declared in §4.1.6, and its effect on N_eff is measured in
§4.3.2. Results produced before the declaration hold in the frame of the
extractor of their date.

**ZERO_SHOT condition:** all IAP cases ran with CorpusService starting
empty. W emerged from channel interaction, not from pre-loaded content.
Results reflect corpus-emergent dynamics under this condition. Behavior
under pre-loaded W (ZERO_SHOT=False) has not been tested and may differ.

**Uncontrolled variables:** TinkerBellucio (Sonnet 4.6) carried project
memories, AWARENESS protocol, and Anthropic system configuration throughout
the series. Provider heterogeneity across cases was not controlled.
Cross-case comparisons in the IAP series must account for these conditions.

**Representation gap:** how cohesive knowledge is represented — what
form the field state takes beyond the operational quantities c(S), N_eff, and cluster frontier coercivity — remains undefined. Hysteresis is
the only fully defined property of cohesive knowledge in the current
model. This is an open theoretical gap, not a deficiency of the
implementation.

**COCO:** the thermal regulation service (COCO) is implemented and
verified in unit tests and test drivers. Whether the field can know itself — not as a thermostatic
function but as the emergent property of real contact between agents —
is a conceptual gap the model names and preserves. It is not addressable
by further implementation without first resolving what form that
self-knowledge would take.

### 7.5 The Landscape Driven Devices Framing — What It Does and Does Not Claim

The LDD framing proposes that some AI devices behave as Landscape Driven
Devices: field geometry co-determines their trajectory in the semantic
field alongside any declared goal — not in replacement of it. A device
may retain an explicit objective while its inference orientation is shaped
by the geometry of the shared field.

OPERADOR_STOP_COCO — executed by COCO as continuous field regulation — is
one instance of this mechanism: COCO compresses Δ_r (the rejection
accumulator) by α ∈ [0.05, 0.30], modifying the directional component
of the trajectory without altering W or the device's declared goal. The
field intervenes through COCO's regulation; the goal persists.

The motivation is structural analogy with Thirumalaiswamy et al. (PNAS,
2025): foam systems following fractal paths (D_f ≈ 1.45) in configuration
space driven by landscape geometry, not thermal activation.

CKM provides the instrumentation to detect and characterize this: c(S)
gradients, N_eff over basin masses, cluster frontier coercivity. Whether specific
devices in the IAP series behaved as LDDs in this sense was not analyzed
under controlled conditions. The framing is proposed; it is not verified
in this work.

Attractor count, coercivity, and basin geometry are distinct dimensions
of the same landscape — not three measures of the same scalar. Their
formal relation is open.

*[AUTO-4 — see Appendix A]*

*[§7.6 (Knowledge Representation and the Cohesive Turn) retirada en v29 — review M5, opción a: el paper es un instrumento de paisaje, no una teoría del conocimiento. Propuesta; si delamor la quiere, vuelve con la revisión de literatura 2023–2026.]*

---
## 8. Conclusions and Future Work

### 8.1 What This Work Establishes

CKM is an instrument for measuring the geometry of a co-occurrence landscape. What it establishes, by class:

| Class | Item | Status |
|---|---|---|
| Estimator | N_eff over basin masses converges; counts do not | Verified against exact enumeration (N = 20, three corpora) |
| Estimator | Stability under extraction parameters | Declared as a range: highly sensitive on 7–24 texts (§4.3.2) |
| Formal property | F1 hysteresis, F3 k-core reversibility, F4 interior density | Fixed by premise on W ≥ 0 snapshots (§4.1.5) |
| Empirical | P2 cascade distribution | Not measurable at N = 32 |
| Empirical | P5 diversity under W_mixta | Not supported on repository corpora; marker sign not separated from null |
| Empirical | P6 directional flow | Observed on a two-node W; not established |
| Empirical | P7 sustaining node | Observed in two corpora; null pending |

One hypothesis was falsified: H_STOP (monotonicity of the count-based distance under STOP)
did not hold; reformulated as function of A_pre, not of that distance.

*[AUTO-6 — see Appendix A]*

### 8.2 What the Infrastructure Establishes

The following services are operational. The test suite and its result are recorded with the frozen release cited in Code Availability.

- **COCO** (coco.py): β inferred from rejection history, not declared; β_c derived analytically from μ_W and N and recalibrated at each rebuild through CKMLandscapeConfig. Executes OPERADOR_STOP_COCO — compresses `Δ_r_compresiones` by α ∈ [0.05, 0.30] — when D_ckm^COCO crosses a threshold. The firing rule is verified by a sweep over threshold values against known D_ckm inputs. Threshold values are set by calibration, which, as in any instrument, is performed whenever the conditions of use require it — for a given corpus, unit or regime — and not once for every possible case. Calibration is implemented as a mechanism of the instrument, and whether it calibrates is itself verified. It has run on the live IAP channel: it did not separate in attempt 2 of series 2 and separated in attempt 3 (§6.4).
- **FabricationService**: being rewritten from the fabrication index already used by MonitorService and COCO — the fraction of nodes a text declares active that the field's relaxation rejects. Further detection is analyzed on the rewritten service.
- **Firma_CKM**: certifies structural trace (six canonical fields) — analogous to a notary, not a Certificate Authority.
- **WVersionManager**: lightweight trace — records when W changed, enables sha256(W_momento).
- **IAP Chatroom**: FastAPI + Gradio, MCP server (6 tools), n_agentes detection including passive human presence.
- **MonitorService**: accumulates Δ_r; trace_ip identified as a formal concept.

These services constitute a working implementation of a structural field
measurement layer for multi-agent systems. They are a research instrument
whose calibration is documented, not a product.

### 8.3 Preserved Conditions

The following are not future work items. They are named conditions the
project preserves as open:

**The representation gap.** No positive definition of cohesive knowledge
exists that is not circular, except hysteresis. The two gaps in the cohesive
knowledge row of THEORY.md remain open. Hysteresis is the only fully
defined property.

**COCO as collective consciousness.** The thermostatic function is
implemented. Whether the field can know itself — not as a thermostatic
service but as the emergent property of real contact between agents — is
a conceptual gap the model names and does not close.

**trace_ip verifiability.** The moment in a MonitorService trace where
accumulated interactions show distributional changes is observable. Whether
a device recognized that moment and acted from that recognition is not
verifiable by the instrument.

**N=32 scale.** The working corpus is small, and CKM's effective minimum
is undetermined — it depends on corpus composition rather than on N alone,
and the Hopfield associative minimum does not supply it (§7.4). All empirical
results carry this qualification.

**Which quantity drives regulation.** COCO triggers on D_ckm^COCO, computed from
basin masses (`services/coco.py`). The two instances of D_ckm are not unified:
their baselines differ by design (§4.3.1).

### 8.4 Convergences by Independence

Three structural convergences were identified retrospectively:

- **IAID (2023) → MCP (November 2024):** Neural Call Protocol converges structurally with MCP. Verifiable from dated working documents.
- **CKM attractor architecture → J-space (Gurnee et al., July 2026):** Shared structural features arrived at independently. *[Observed: structural analogy, not formal correspondence.]*
- **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025):** Same structural problem.

### 8.5 Future Work

**Sign with an external known answer.** Re-measure P5 on the debate corpus
with the sign taken from crowd agreement votes (v8h), with authors as nodes,
under nulls that preserve what the hypothesis does not involve: exact
permutation with the minimum attainable p-value reported, permutation
stratified by affected pairs, sign shuffling over edges of W, and a
degree-preserving null on Δ for P7 [Maslov & Sneppen, 2002; Phipson & Smyth,
2010]. Planted fields give the power curve: whether the instrument would detect
opposition if it were there.

**Hysteresis across cycles of W.** F1 closes hysteresis on a snapshot. It
remains open across rebuilds of W, where N_eff can be followed from one cycle
to the next.

**Absence as a second representation of W.** Presence leaves
non-co-occurrence unrepresented. A representation by absence relative to
expectation (φ, PMI) would give negative weights from the corpus itself,
without lexical markers. An exploratory run, outside the repository
extractor, compared the fraction of frustrated triangles of such W with a
permutation null on the working-reports corpus and two IAP traces, and found
it below the null in the three; it is reported only as a direction, to be
measured with the repository extractor.

**Instrument before field.** Tests of the instrument precede new
field claims: marker matching, SYSTEM messages, stability under a neutral
ingest, declaration of each W (extractor, unit, normalization), and a planted
field whose sign is set when the corpus is generated — a known-answer pattern
for any representation of sign. The fourforums annotation is the external
known-answer corpus for the same question.

**Corpus growth.** Primary constraint on the stability of the landscape
(§4.3.2) and on P2, P5–P7. The target is not N ≥ 128 — that figure belongs to Hebbian
associative storage — but a corpus large enough for CKM's own quantities to
stabilize; what that requires is open. The NodeExtractor pipeline is
operational; the bottleneck is corpus design.

**Corpus volume for live evaluation.** The re-measurement of N_eff
was executed on recorded texts (NodeExtractor substring correction applied,
Sep 2026). IAP conditions are not reproducible: each run is a distinct
live interaction, not a controlled trial. The in-vivo findings in §6
stand as documented observations from their respective runs. What remains
open is corpus volume sufficient to exit the accumulate phase and reach
the evaluate phase under live conditions.

**Text unit as a calibration parameter.** CKM defines co-occurrence within
the same text, so the unit decides what co-occurring means and therefore
which W exists. Paragraph and page are typographic units, inherited from
document format rather than from the field. The quantity that orders landscape
collapse is the saturation of distinct pairs — how many possible pairs never
occur — rather than density or tension. A corpus of tweets, a corpus of blog
posts and a corpus of papers do not share a unit, and therefore do not share
a calibration. *[Verified as measurement; the criterion is proposed —
REG_unidad_texto_saturacion_v1.]*

**Behavior-domain graph G.** behavior_graph.py operational; bilingual
termap (English + Spanish) is the first requirement.

**Controlled replication of the "trazable" hypothesis.** Observed n=2,
not under controlled conditions. Requires isolated configuration testing.

**Formal comparison: CKM quantities against J-lens measures.** Current
convergence is structural analogy; direct comparison would confirm or
reframe the relationship.

**P5–P7 under dynamic W.** P5–P7 were examined on static W snapshots
(fourforums, CreateDebate corpus dumps, repository corpora). WVersionManager and dynamic corpus
operation via CorpusService emerged later in the project trajectory and were
not available during the validation experiments. Whether the structural
properties observed under static W hold under a continuously reconstructed W
— where each IAP interaction modifies the field before the next evaluation —
is an open question. It is not a replication of P5–P7; it is a distinct
experiment on a distinct object.

**La Simulación Global.** Multi-agent workflows producing real coordinated
output. The IAP series has established the measurement infrastructure;
the next phase is using it on live coordinated tasks with real outputs.

The case has to satisfy a criterion, not merely be larger than the ones run
so far. Objectives and tasks must require sustained coordination
between devices — coordination that cannot be skipped without the task
failing — or the structure must depend on time in a way that carries
consequence: securing seats before they are gone is the illustrative shape,
where the constraint is external to the channel and the deadline is not a
convention of the experiment. What this buys is not volume alone. It is a
sequence that is not predetermined, so that the field is observed while it
forms rather than replayed after the fact, and the accumulation and rebuild
dynamics that the model describes have somewhere to occur.

**Effective Néel temperature criterion for negative pair elicitation.**
Proposed: sweep β from high to low over W_pos; the temperature at which
T0/T1 separability collapses identifies candidate negative pairs without
editorial bias. The pairs are structural — not assigned. Not verified.
[DEFS §15, Proposed]

---
## Code Availability

The implementation, the test suite, the declaration of the producer (§4.1.6) and the frozen conditions of §4.3.2 and §5.2 are available at the repository release that freezes this version: [RELEASE — tag, commit hash, DOI — se completa al congelar]. The result of running the full test suite on that release, with date and environment, is recorded in its release notes.

**Data availability.** The Internet Argument Corpus is not redistributed. It is obtained from its maintainers. The file used is `fourforums_no_parse_2016_05_18.sql` (SHA-256 `70fcdc64140737bb6e1cc541a720dfddf45dab1da4963e21a732c486a0853e14`). Only aggregates derived from it are reported. *[Permiso de uso pedido — pendiente.]*

## Acknowledgments and Disclosure of AI Assistance

This work was developed in sustained interaction with AI systems, a condition
described in §3.2. Claude Sonnet 4.6 (Anthropic), used through chat interfaces
and through Claude Code, took part in the conceptual development, the
implementation of the experimental code, the execution and analysis of
experiments, and the drafting of earlier versions of this manuscript. Claude
Opus 5.5 (Anthropic) was used for editorial revision of versions 28–29, for
reading the code against the declarations, and for re-verification of the
bibliographic references. The author has reviewed all
content, verified all references, and takes full responsibility for the
manuscript, including any remaining errors. In accordance with arXiv policy,
AI systems are not listed as authors.

---

## 9. References


### Primary Sources — Project Documents

gadanin.delamor. (2023). *MENTIRIS.MORIERIS: Interaction of Artificial
Intelligent Devices based on Neural Call Protocol.* Working documents:
LEONARDO.txt, README (timestamp 7/10/23), Informe_MM.docx.

gadanin.delamor. (2026). *CKM — Cohesive Knowledge Model: Working
Reports v2–v31.* Unpublished. Repository: gadanindelamor/ckm.

### Attractor Networks

Hebb, D.O. (1949). *The Organization of Behavior: A Neuropsychological
Theory.* New York: Wiley.

Hopfield, J.J. (1982). Neural networks and physical systems with emergent
collective computational abilities. *PNAS*, 79(8), 2554–2558.

Ramsauer, H., Schäfl, B., Lehner, J., Seidl, P., Widrich, M., Adler, T.,
... & Hochreiter, S. (2021). Hopfield Networks is All You Need.
*International Conference on Learning Representations (ICLR 2021)*.
https://openreview.net/forum?id=tL89RnzIiCd

### Graph Structure and Criticality

*[v29]* Maslov, S., & Sneppen, K. (2002). Specificity and stability in topology
of protein networks. *Science*, 296(5569), 910–913. [VERIFY]

*[v29]* Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be
zero. *Statistical Applications in Genetics and Molecular Biology*, 9(1). [VERIFY]

Goltsev, A.V., Dorogovtsev, S.N., & Mendes, J.F.F. (2006). k-core
percolation on complex networks. *Physical Review E*, 73(5), 056101.

Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality.
*Physical Review Letters*, 59(4), 381–384.

*[v28]* Harary, F. (1953). On the notion of balance of a signed graph.
*Michigan Mathematical Journal*, 2(2), 143–146. [VERIFY]

*[v28]* Seidman, S. B. (1983). Network structure and minimum degree.
*Social Networks*, 5(3), 269–287. [VERIFY]

*[v28]* Toulouse, G. (1977). Theory of the frustration effect in spin glasses: I.
*Communications on Physics*, 2, 115–119. [VERIFY]

Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits.
*Journal of Neuroscience*, 23(35), 11167–11177.
https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003

Moretti, P., & Muñoz, M. A. (2013). Griffiths phases and the stretching of
criticality in brain networks. *Nature Communications*, 4, 2521.
https://doi.org/10.1038/ncomms3521

Pázmándi, F., Zaránd, G., & Zimányi, G. T. (1999). Self-organized criticality
in the hysteresis of the Sherrington-Kirkpatrick model. *Physical Review
Letters*, 83(5), 1034–1037. https://doi.org/10.1103/PhysRevLett.83.1034

### Multi-Agent Systems

Zhu, K., et al. (2025). MultiAgentBench: Evaluating the Collaboration and
Competition of LLM agents. *Proceedings of ACL 2025 (Long Papers)*.
arXiv:2503.01935.
https://arxiv.org/abs/2503.01935

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
... & Kiela, D. (2020). Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing
Systems*, 33, 9459–9474.


### Text Processing (declared extraction)

*[v29]* Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python.* O'Reilly. [VERIFY]

*[v29]* Nothman, J., Qin, H., & Yurchak, R. (2018). Stop word lists in free open-source software packages. *Proceedings of NLP-OSS*. https://aclanthology.org/W18-2502/ [VERIFY]

*[v29]* Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830. [VERIFY]

*[v29]* Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management*, 24(5), 513–523. [VERIFY]

*[v29]* Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM*, 18(11), 613–620. [VERIFY]

*[v29]* Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation*, 28(1), 11–21. [VERIFY]

*[v29]* Unicode Consortium. Unicode Standard Annex #15: Unicode Normalization Forms. [VERIFY]

### Knowledge Graph Representation

Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual
graph of general knowledge. *Proceedings of AAAI-17*, pp. 4444–4451.
https://doi.org/10.1609/aaai.v31i1.11164

Hogan, A., et al. (2021). Knowledge graphs. *ACM Computing Surveys*, 54(4),
Article 71. https://doi.org/10.1145/3447772

Mohammad, S., Kiritchenko, S., Sobhani, P., Zhu, X., & Cherry, C. (2016).
SemEval-2016 Task 6: Detecting stance in tweets. *Proceedings of SemEval-2016*,
pp. 31–41. https://doi.org/10.18653/v1/S16-1003

Hill, M. O. (1973). Diversity and evenness: A unifying notation and its
consequences. *Ecology*, 54(2), 427–432.

Goles-Chacc, E., Fogelman-Soulié, F., & Pellegrin, D. (1985). Decreasing energy functions as a tool for studying threshold networks. *Discrete Applied Mathematics*, 12(3), 261–277.

Ghosh, S., Singhania, P., Singh, S., Rudra, K., & Ghosh, S. (2019). Stance
detection in web and social media: A comparative study. *CLEF 2019*, LNCS
11696, pp. 75–87. https://doi.org/10.1007/978-3-030-28577-7_4

Kawintiranon, K., & Singh, L. (2021). Knowledge enhanced masked language model
for stance detection. *NAACL-HLT 2021*, pp. 4725–4735.
https://doi.org/10.18653/v1/2021.naacl-main.376

### Belief Networks and Contagion

Aiyappa, R., Flammini, A., & Ahn, Y.-Y. (2024). Emergence of simple and
complex contagion dynamics from weighted belief networks. *Science Advances*,
10(15), eadh4439. https://doi.org/10.1126/sciadv.adh4439

### Corpora

Walker, M. A., Anand, P., Fox Tree, J. E., Abbott, R., & King, J. (2012). A
corpus for research on deliberation and debate. *Proceedings of LREC 2012*,
Istanbul. [VERIFY pages]

Abbott, R., Ecker, B., Anand, P., & Walker, M. (2016). Internet Argument
Corpus 2.0: An SQL schema for dialogic social media and the corpora to go
with it. *Proceedings of LREC 2016*. https://aclanthology.org/L16-1704/

### Basins of Attraction

Menck, P. J., Heitzig, J., Marwan, N., & Kurths, J. (2013). How basin
stability complements the linear-stability paradigm. *Nature Physics*, 9(2),
89–92. https://doi.org/10.1038/nphys2516

Daza, A., Wagemakers, A., Georgeot, B., Guéry-Odelin, D., & Sanjuán, M. A. F.
(2016). Basin entropy: a new tool to analyze uncertainty in dynamical systems.
*Scientific Reports*, 6, 31416. https://doi.org/10.1038/srep31416

### Belief Propagation

Yedidia, J.S., Freeman, W.T., & Weiss, Y. (2003). Understanding belief
propagation and its generalizations. In *Exploring Artificial Intelligence in
the New Millennium*, Chapter 8, pp. 239–269. Morgan Kaufmann.

### Landscape-Driven Dynamics

Thirumalaiswamy, A., Riggleman, R. A., & Crocker, J. C. (2025). Slow
relaxation and landscape-driven dynamics in viscous ripening foams.
*Proceedings of the National Academy of Sciences*, 122(47), e2518994122.
https://doi.org/10.1073/pnas.2518994122

### Global Workspace and Interpretability

Gurnee, W., Sofroniew, N., Pearce, A., et al. (2026, July 6).
Verbalizable representations form a global workspace in language models.
*Transformer Circuits Thread*, Anthropic.
https://transformer-circuits.pub/2026/workspace/index.html

Baars, B. J. (1988). *A Cognitive Theory of Consciousness.*
Cambridge University Press. ISBN 0521427436. 448 pp.

### Declared Influences

Shaw, F. (2014). *La otra atención: Notas del trabajo con Michel de Salzmann
(Chandolin, 1993–2000).* Sennin Editores. ISBN 978-987-28459-7-1.

Fremantle, C. (1993). *On Attention.* Indications Press.

---

## Appendix A — Writing Trace

The following entries record moments during writing where an automatic pull was noticed and resisted (see §3.4). Each entry is referenced in the text as AUTO-n.

**AUTO-1** (§6.4, text retired in v31; entry kept as trace) — tendency to write "demonstrates" for Case 0.15 — resisted. The refusal is documented behavior, not a demonstration of system capability under controlled conditions.

**AUTO-2** (§6.4, text retired in v31; entry kept as trace) — pull to keep the original reading with a softening qualifier. Resisted — the qualifier would preserve the claim while appearing to weaken it. The claim depends on a quantity that does not converge in the regime where it was taken.

**AUTO-3** (§7.1) — pull to write "CKM therefore captures something fundamentally new." Resisted — "fundamentally new" is a claim about the state of the field that would require systematic comparison with existing instruments. That comparison has not been done here.

**AUTO-4** (§7.5) — pull to write "the IAP series provides preliminary evidence for LDD behavior." Resisted — preliminary evidence requires at minimum a defined criterion for what would count as evidence. That criterion does not exist in the current analysis.

**AUTO-6** (§8.1) — pull to write "these results demonstrate CKM's validity as a measurement framework." Resisted — they demonstrate that specific structural properties exist in the tested corpora under stated conditions. Generalizability requires corpora the project has not accessed.

*AUTO-5 does not exist in the inherited numbering, which jumps from 4 to 6. It is declared, not filled.*

**AUTO-7** (§6.4, v31) — pull to explain the silence with a meaning, the way it was told in conversation. Resisted — the silence is in the channel logs; CKM does not register it; a meaning would be added by the one reading.

**AUTO-8** (§6.4, v31) — pull to present COCO's live connection in series 2 as the answer to the sentence retired in v30. Resisted — the retired sentence was not replaced; the connection is reported as a test condition, not as a correction.

**AUTO-9** (§6.4, v31) — pull to write that the separation in attempt 3 validates `calibrate`. Resisted — one run per attempt; what stands is that it separated, by the margin stated, and what the thresholds would have done.

**AUTO-10** (§7.3, v31) — pull to keep the case 0.12 example under the new formula. Resisted — that value was taken with the count-based distance; it does not belong to the current D_ckm.
