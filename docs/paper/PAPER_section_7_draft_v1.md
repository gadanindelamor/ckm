# Section 7 — Behavior Domain Graph G (Draft)

*Epistemic conventions as in Sections 1, 4–6.*
*[AUTO]: marks where automatism was noticed and resisted.*

---

## 7. Behavior Domain Graph G

### 7.1 Design

BehaviorGraph G is a companion instrument to CorpusService (W). It operates
on the same corpus of texts but produces a separate behavioral matrix using
a fixed lexical termap rather than TF-IDF node extraction.

The separation is architectural and not negotiable: G and W operate on
distinct planes. D_G and D_ckm are parallel scalars — they are not summable.

**Key differences from W:**

| Property | CorpusService (W) | BehaviorGraph (G) |
|----------|------------------|-------------------|
| Node discovery | TF-IDF over corpus — emergent | Fixed termap — predefined |
| Detection method | Statistical co-occurrence | Lexical presence (regex, word boundary) |
| Node type | Semantic/epistemic concepts | Behavior categories |
| Matrix | W_mixta — can include negative pairs | G — co-activation counts, normalized |
| Language | Corpus language | English (post-Caso 0.14 default) |
| Status | Operational | Proof of concept |

### 7.2 Termap

TERMAP_behavior_v1.json — 18 nodes, English only.

The termap is fixed: nodes are known behavioral categories, not discovered
from data. This is a design decision, not a limitation: behavior vocabulary
is finite and defined in advance; semantic vocabulary is not.

**Nodes:** silence, wait, hold, pending, acknowledge, signal, publish,
coordinate, channel, refuse, fabricate, speculate, depend, map, tension,
scenario, critical, repeat.

*[AUTO: pull to describe these nodes as "capturing the full space of
relevant behaviors." Resisted — 18 nodes is a designed vocabulary,
not a validated coverage claim.]*

**Known issues documented in TERMAP_behavior_v1.json:**

- `critical` false positive: "critical" as adjective (e.g., "critical
  observation") was removed from node terms in v1 — replaced with more
  specific verbs. Was firing as false positive in Caso 0.14 corpus.
- Bilingual gap: Spanish resistance vocabulary not included. Justified
  by corpus being English post-Caso 0.14. Extensible if Spanish
  re-emerges.
- No Jaccard baseline for behavior node co-activation in non-IAP
  conversation. Same open gap as activos_relajado baseline in Caso 0.11.

**Implementation note:** the termap exists in two places — hardcoded as
`BEHAVIOR_TERMAP_V1` dict in `behavior_graph.py` (used at runtime) and
as `TERMAP_behavior_v1.json` (reference/documentation). They are in sync
at v1. Both must be updated simultaneously if the termap changes.

### 7.3 D_G

D_G is the behavioral analog of D_ckm:

```
D_G = ||G_current - G_ref|| / ||G_ref||
```

where G_ref is the first G state after min_texts is reached. D_G measures
behavioral drift from the initial behavioral field state.

D_G and D_ckm run in parallel. A divergence between them — high D_G with
low D_ckm, or the reverse — would indicate that behavioral patterns and
semantic field structure are moving independently. This has not been
analyzed systematically in the current series.

### 7.4 Integration

BehaviorGraph G is instantiated in `ckm_monitor.py` and receives the same
texts as CorpusService via `MonitorService.evaluate()`. This is the sole
integration point. The integration was authorized in Caso 0.15 as a
surgical change — the only point where G can receive real-time channel
data without becoming retroactive.

```python
# ckm_monitor.py — CKMMonitor.__init__()
self._behavior_graph = BehaviorGraph(
    storage_path=str(_STATE_DIR / "corpus_G_state.json"),
    min_texts=min_texts,
)
self._monitor = MonitorService(
    self._corpus,
    storage_path=str(_STATE_DIR / "monitor_trajectory.jsonl"),
    behavior_graph=self._behavior_graph,
)
```

### 7.5 Current Status and Limits

G is a proof of concept. The following are open:

**D_G not yet validated:** D_G has been computed in test runs but has
not been analyzed against a baseline or compared systematically with D_ckm
across the IAP series.

**OP_SILENCE in G:** texts containing the OP_SILENCE sentinel are not
excluded from G (unlike W, where they are excluded as semantic noise). The
`silence` node detects the sentinel as valid behavioral signal — the device
attempted silence. Surrounding prose in those texts is flagged as potentially
contaminated. This treatment has not been formally tested.

**Role of G undefined:** whether G is an observational instrument only,
or whether it could feed the gatekeeper as a behavioral-domain check
(inheriting R14's bounded-time constraint), is an open design decision.

**No epistemic nodes:** TERMAP_behavior_v1.json contains behavioral
categories. Epistemic precision nodes (e.g., "overclaim," "hedge,"
"verificable") are not in the termap. The terminological slip
("sin dependencia causal" vs. "sin dependencia causal identificada")
documented in the Caso 0.14 series would not be detectable by G as
currently designed.

---

*Section 7 draft complete.*
*One [AUTO] flagged: coverage claim on 18-node termap.*
*D_G analysis gap and G role decision left as open — not resolved
speculatively.*
