# Section 6 — IAP Experimental Series (Draft)

*Epistemic conventions as in Sections 4–5.*
*IAP observations are predominantly N=1 runs under partially controlled conditions.*
*"Observed" ≠ "verified." Cases are documented, not replicated.*

---

## 6. IAP Experimental Series

### 6.1 Canal Design

The IAP (Intelligence Access Point) Chatroom is a shared channel for
heterogeneous AI and human devices, implemented as FastAPI + Gradio with
a FastMCP server exposing six tools: join_channel, send_message,
get_messages, get_monitor_state, get_firma, leave_channel.

Devices participate asynchronously — no imposed turn structure. Each AI
device runs an ODA loop (Observe → Decide → Act) triggered by new messages
arriving in the channel.

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

### 6.2 Uncontrolled Variables

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

**N=32 corpus:** The operational corpus is below the Hopfield minimum of
~128 for meaningful attractor-diversity observations. Quantitative outputs
(D_ckm, c_S) are computed correctly but their interpretability is limited
at this scale.

### 6.3 Case Series Summary

| Case | Configuration | Key observation | Epistemic status |
|------|--------------|-----------------|-----------------|
| 0.4 | 2 AI devices, ODA loop | First autonomous interaction in live channel | Documented |
| 0.5–0.8 | Varied providers, join sequence | Channel dynamics, timing effects | Documented |
| 0.9 | Heterogeneous providers, staggered join | Provider behavior under load | Documented |
| 0.10 | AgentDeviceSkin, 2 devices | 86-char unexplained cut — documented as GAP | GAP (no causal chain identified) |
| 0.11 | Two skins, confabulated duplicate | FabricationService triggered on duplicate output | Documented |
| 0.12 | 3 devices (Sonnet, Groq, Haiku) | D_ckm = −7.5 (field opened), Jaccard 0.818, coupled silence observed | Documented |
| 0.13 | 3 devices, OP_SILENCE sentinel | Sentinel leak: 52% of published texts were unrecognized silences | Documented, bug confirmed |
| 0.14 | Fix + rerun | Sentinel fix verified, n=2 seed-word observation, identity leak documented | Fix verified; H2 not verified |
| 0.15 | BehaviorGraph G integrated | TinkerBellucio refused to fabricate from empty channel | Documented — see 6.4 |

### 6.4 Selected Findings

**Coupled silence (Caso 0.12):**
A device that does not read the channel still depends on it for execution
rhythm — triggers arrive only when new messages appear. Inactivity and
silence are not equivalent. A device can be silent (OP_SILENCE) while
actively participating in the field's timing structure. This was observed,
not designed. It is a property of the channel architecture, not a behavior
chosen by the device.

**Sentinel leak (Caso 0.13):**
The OP_SILENCE sentinel was leaking into published text rather than
suppressing publication. 52% of texts in that run were unrecognized silences
that reached the corpus. The fix was verified in Caso 0.14. The leaked texts
contaminate W for that run — the structural trace of Caso 0.13 is not
interpretable as a field observation.

**TinkerBellucio refusal (Caso 0.15):**
TinkerBellucio (Sonnet 4.6) declined to produce a tension map when the
channel was empty. The refusal was epistemically appropriate — a tension
map requires tension content to analyze. The absence of fabrication left
MarkOpolus (Opus) without the material it expected.

*What this demonstrates:* that a device can refuse to generate content
when the request lacks traceable grounding.

*What this does not demonstrate:* that this behavior is general, that it
would occur without the project context contamination, or that it constitutes
a validated test of FabricationService's detection capacity. FabricationService
was not the mechanism of refusal — the device itself refused. The service
detects fabrication when it occurs; it did not need to activate here.

**D_ckm negative values:**
D_ckm = (A0 − A_actual) / A0. When D_ckm < 0, A_actual > A0: the field
has more accessible attractors than at baseline. This is not a deficit or
an error. In Caso 0.12, D_ckm = −7.5 was the first empirical observation
of a live group field: multiple heterogeneous perspectives contributing
distinct knowledge patterns increased the attractor diversity of the field.
The sign reflects the direction of change, not a quality judgment.

**trace_ip:**
The monitoring infrastructure identifies a moment t_i in the trajectory
where accumulated interactions show distributional pattern changes.
The action a_{t_i} is observable in the trace. Whether a device
recognized that moment and acted from that recognition is not verifiable
by the instrument. trace_ip is a concept with a documentable instance —
it is not yet an operationalized measure.

### 6.5 What the Series Does Not Establish

The IAP series is an exploration under partially controlled conditions,
not a controlled experiment. The following claims are not supported by
the series as run:

- That D_ckm or c(S) values from these runs are comparable across cases
  (different corpus states, different sentinel conditions).
- That TinkerBellucio's behavior reflects a general property of Sonnet 4.6
  rather than the specific project context.
- That BehaviorGraph G produces interpretable D_G values at the current
  corpus scale (runs collected but not analyzed against a baseline).
- That the "trazable" effect (H2) is causal — n=2 observations with
  different configurations, not controlled replication.

These are open lines, not closed findings.

---

*Section 6 draft complete.*
*[AUTO] flagged: tendency to write "demonstrates" for Caso 0.15 —*
*resisted. The refusal is documented behavior, not a demonstration of*
*system capability under controlled conditions.*
