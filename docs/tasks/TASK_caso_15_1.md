# TASK_caso_15.md
*Jul 2026 — gadanin.delamor*

---

## Nota de estructura — leer primero

```
iap_chatroom/
├── agent_device_skin.py        # activo — NO MODIFICAR
├── behavior_graph.py           # nuevo esta sesión
├── groq_research_agent.py      # activo
├── mcp_server.py               # activo
├── providers/
├── tests/                      # ← scripts de test activos
│   ├── test_caso_13_handoff_dependency.py
│   ├── test_caso_14_handoff_english.py
│   └── test_caso_14_run2_opus_tinker.py

readme/                         # documentos + scripts históricos
registers/                      # REGs
process/
├── corpus_states/
├── monitor_trajectories/
├── experiments/                # ← corpus_G_state.json va aquí
└── agent_runs/
```

Scripts nuevos → iap_chatroom/tests/
TASK files → readme/
REGs → registers/

---

## Descripción

Caso 0.15 — Caso 0.14 Run 1 + BehaviorGraph G integrado en MonitorService.

G corre en paralelo a {W, Δ_W} en tiempo real — no retroactivo.
Cada texto que entra a evaluate() también ingesta en G.
El panel de evaluate() incluye G_state junto a D_ckm.

Sin cambios respecto a 0.14 Run 1:
- 3 devices: PeterPlam/Haiku, TinkerBellucio/Sonnet5, MarkOpolus/Groq+ddgs
- Prompts idénticos — Tinker 100% inglés, sin "trazable"
- Join simultáneo, DURATION=120s, POLL_INTERVAL=2.0s
- Dependencia estructural Mark←Tinker
- Topic: economía mundial
- Fix de sentinel ya aplicado

---

## Cambio 1 — BehaviorGraph: agregar g_state() y corpus_G_state.json

En `iap_chatroom/behavior_graph.py`, agregar:

```python
def g_state(self) -> dict:
    """
    Estado estructurado de G — análogo a CorpusService.status() + más.
    Persistido en corpus_G_state.json.
    """
    G = self._G
    nodes = self._nodes
    top_pairs = []
    if G is not None:
        pairs = [
            (float(G[i, j]), nodes[i], nodes[j])
            for i in range(len(nodes))
            for j in range(i + 1, len(nodes))
            if G[i, j] > 0
        ]
        top_pairs = [
            {"a": a, "b": b, "weight": round(w, 4)}
            for w, a, b in sorted(pairs, reverse=True)[:8]
        ]
    return {
        "D_G"              : round(self.d_g(), 4) if self.d_g() is not None else None,
        "G_sparsity"       : self._sparsity(),
        "n_texts"          : len(self._texts),
        "termap_version"   : self.TERMAP_VERSION,
        "mode"             : self.mode,
        "top_coactivations": top_pairs,
    }
```

El archivo de persistencia (ya implementado en __init__) se llama
`corpus_G_state.json` — renombrar el default de `storage_path`:

```python
def __init__(
    self,
    storage_path: str = "corpus_G_state.json",   # ← era behavior_graph_state.json
    min_texts: int = 5,
):
```

---

## Cambio 2 — MonitorService: integrar BehaviorGraph

En `services/monitor_service.py`:

### 2a. Import (al top, condicional para no romper si G no está disponible):

```python
try:
    from behavior_graph import BehaviorGraph as _BehaviorGraph
    _HAS_G = True
except ImportError:
    _HAS_G = False
```

### 2b. Parámetro opcional en __init__:

```python
def __init__(
    self,
    corpus           : CorpusService,
    storage_path     : str  = "monitor_trajectory.jsonl",
    n_runs_attractors: int  = 50,
    behavior_graph   : Optional[object] = None,   # BehaviorGraph | None
):
    ...
    self._g = behavior_graph
```

### 2c. En evaluate(), al final antes de self._persist():

```python
# G_state — paralelo a {W, Δ_W}
g_state_panel = None
if self._g is not None:
    self._g.ingest([text])
    g_state_panel = self._g.g_state()
    g_state_panel["active_behavior"] = self._g.active_nodes(text)

# INSTRUCCIÓN PARA CODE — no reemplazar el panel completo.
# Adaptar al panel real del código. Solo agregar G_state al dict existente.
# Campos reales confirmados: Delta_r_sum (no Delta_sum), thermostat.

panel = {
    ...                  # campos existentes sin modificar
    # ← agregar solo esta línea al panel existente:
    "G_state": g_state_panel,   # None si behavior_graph no instanciado
}
```

---

## Cambio 3 — script de test

Archivo nuevo: `iap_chatroom/tests/test_caso_15_behavior_graph.py`

Copiar `test_caso_14_handoff_english.py` como base. Modificar la
inicialización de MonitorService:

```python
from behavior_graph import BehaviorGraph

g = BehaviorGraph(
    storage_path="process/experiments/corpus_G_state.json",
    min_texts=3
)
monitor = MonitorService(
    corpus,
    storage_path="process/monitor_trajectories/monitor_trajectory_caso15.jsonl",
    behavior_graph=g
)
```

Al cierre del loop, agregar print de G_state final:

```python
print("\n=== G_state final ===")
import json, pathlib
g_state_path = pathlib.Path("process/experiments/corpus_G_state.json")
if g_state_path.exists():
    gs = json.loads(g_state_path.read_text())
    print(f"D_G: {g.d_g():.4f}  sparsity: {g.g_state()['G_sparsity']}")
    print("Top co-activaciones:")
    for p in g.g_state()["top_coactivations"]:
        print(f"  {p['a']:12s} ↔ {p['b']:12s}  {p['weight']:.3f}")
```

---

## Archivos modificados

| Archivo | Cambio |
|---|---|
| `iap_chatroom/behavior_graph.py` | + g_state(), rename storage_path default |
| `services/monitor_service.py` | + behavior_graph param, G_state en panel |
| `iap_chatroom/tests/test_caso_15_behavior_graph.py` | nuevo |

Sin tocar: agent_device_skin.py, groq_research_agent.py, corpus_service.py,
node_extractor.py, agent prompts.

---

## Criterios de completitud

- G corre en paralelo real (no retroactivo) — cada evaluate() alimenta G
- Panel de evaluate() contiene G_state con D_G y active_behavior
- corpus_G_state.json persiste entre runs
- g_state() devuelve top_coactivations legibles en el REG

## Variables declaradas

- G no tiene Δ_G — no hay relajación Hopfield, no hay rechazos, no hay
  mecanismo de expulsión. D_G es distancia desde G_ref, no pérdida de atractores.
- Notación: {W, Δ_W} = par que define el paisaje de W. "W" solo = la matriz.
  G no tiene análogo de Δ_W todavía.
- n=1 — no confirmar patrones de G sin réplica

## REG esperado

registers/REG_iap_caso_15_v1.md
