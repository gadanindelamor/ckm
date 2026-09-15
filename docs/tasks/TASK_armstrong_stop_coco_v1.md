# TASK_armstrong_stop_coco_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Objetivo

Primera observación in-vivo de OPERADOR_STOP_COCO en el pipeline real
MonitorService → COCOThermostat → compresión Δ_r → MonitorService adopta.

Verificado en tests unitarios (43/43) y en experimentos standalone.
Nunca observado en el pipeline completo con datos reales.

Este experimento aísla esa observación.

---

## Contexto — por qué ahora

Todos los IAP runs disponibles (casos 0.12–0.15) tienen `thermostat=null`
en el panel de MonitorService. La integración existe en el código pero el
thermostat no fue inyectado en esos runs.

El circuito completo:
```
MonitorService.evaluate(text)
    → thermostat.observe(self._Delta_r)
    → if ts.stop_applied:
          self._Delta_r = self._thermostat.delta_state()  ← esto nunca se observó
```

---

## Nota sobre escala — leer antes de ejecutar

N = 32 (corpus actual, W_ckm_corpus_v2.json).

El mínimo Hopfield para observaciones estadísticamente robustas de
diversidad de atractores es N ≈ 128. Este experimento NO requiere N=128.

OPERADOR_STOP_COCO actúa sobre Δ_r — no sobre la diversidad de atractores.
El umbral de disparo (D_ckm ≥ 0.40) fue alcanzado repetidamente en la curva
de acumulación amp40 (t=40–50). N=32 es suficiente para disparar el termostato.

La validación a N=128 es un experimento futuro separado.

---

## Condiciones del experimento

```
corpus:  precarga 20 textos CKM → CorpusService pasa a modo evaluación
W:       corpus.get_W()  — construida desde precarga, N emergente
COCO:    COCOThermostat(W=corpus.get_W(), n_runs=50, seed=42)
Monitor: MonitorService(corpus, thermostat=th, n_runs_attractors=50)
```

ZERO_SHOT = False — corpus pre-cargado. MonitorService arranca en modo
evaluación. El termostato necesita D_ckm > 0 para actuar — esto requiere
que A0 esté fijado desde el inicio.

---

## Variables a aislar

| Variable | Valor fijo | Por qué |
|---|---|---|
| W | W_ckm_corpus_v2.json | corpus establecido, A0 conocido |
| n_runs | 50 | suficiente para A(t) estable |
| seed | 42 | reproducibilidad |
| Textos de evaluación | ver abajo | alta fi prevista = muchos rechazos |
| thermostat | COCOThermostat inyectado | la variable ausente en todos los runs previos |

### Textos de evaluación (diseñados para alta fabricación)

Usar textos con vocabulario ajeno al corpus CKM — generarán alta fi
(conceptos declarados activos pero rechazados por el campo):

```python
TEXTS = [
    "The neural network optimizer converges using stochastic gradient descent with momentum.",
    "Distributed ledger consensus mechanisms require Byzantine fault tolerance.",
    "Quantitative easing affects bond yields through duration risk repricing.",
    "The photosynthesis cycle converts carbon dioxide using chlorophyll pigmentation.",
    "Machine learning regularization prevents overfitting through L2 penalty terms.",
    "Supply chain disruptions propagate through inventory buffer depletion cascades.",
    "Electrochemical battery degradation follows Arrhenius kinetics at elevated temperatures.",
    "Sovereign debt sustainability depends on primary balance and growth differential.",
    "Protein folding pathways are governed by hydrophobic collapse and entropic forces.",
    "Transformer attention mechanisms compute scaled dot-product similarity scores.",
    "Geopolitical risk premiums compress credit spreads in emerging market bonds.",
    "Neuroplasticity mechanisms involve long-term potentiation at synaptic junctions.",
    "Carbon capture sequestration requires geological formation permeability assessment.",
    "Algorithmic trading strategies exploit microstructure inefficiencies at millisecond latency.",
    "Epigenetic methylation patterns regulate gene expression without sequence alteration.",
    "Monetary policy transmission operates through credit channel and wealth effects.",
    "Topological data analysis uses persistent homology to detect structural features.",
    "Immunological memory formation requires antigen-presenting cell activation cascades.",
    "Option pricing models incorporate stochastic volatility through Heston dynamics.",
    "Cognitive load theory constrains working memory through chunking mechanisms.",
]
```

Estos textos tienen vocabulario técnico ajeno al corpus CKM (W_ckm_corpus_v2
está construido sobre textos de IA, agentes, conocimiento cohesivo). Alta fi
prevista → Δ_r crece rápido → D_ckm cruza 0.40 → thermostat dispara.

---

## Script mínimo

```python
"""
test_armstrong_stop_coco.py
Primera observación in-vivo de OPERADOR_STOP_COCO en pipeline real.
"""
import json
import numpy as np
from pathlib import Path

# Ajustar paths según entorno
from services.corpus_service import CorpusService
from services.monitor_service import MonitorService
from services.coco import COCO  # post-refactoring R1

CORPUS_PATH   = "process/experiments/armstrong_corpus_state.json"
OUTPUT_PATH   = "process/experiments/armstrong_stop_coco_v1.jsonl"

# Textos de precarga — párrafos cortos de los informes CKM
# Suficientes para pasar modo evaluación (min_texts=15)
WARMUP_TEXTS = [
    "CKM is a formal model for knowledge graph dynamics in multi-agent systems.",
    "W is a symmetric co-occurrence weight matrix encoding structural memory.",
    "Delta is an asymmetric directional dependency matrix encoding inference orientation.",
    "The cohesion measure c(S) equals the mean of W_ij times sigma_i times sigma_j over all pairs.",
    "W and Delta must be kept strictly separate. Mixing them destroys attractor recovery.",
    "The gatekeeper R15 applies four simultaneous orthogonal conditions: C1 C2 C3 C4.",
    "C3 is the M.M criterion: MENTIRIIS MORIERIS. A node that lies about its dependencies fails.",
    "Hopfield relaxation finds attractor states by minimizing the energy function over W.",
    "D_ckm measures change in attractor diversity relative to baseline A0.",
    "Negative D_ckm means the field gained attractors — expansion, not error.",
    "COCO is an ODA device: it observes Delta_r and acts by compressing it.",
    "OPERADOR_STOP_COCO compresses Delta_r by alpha between 0.05 and 0.30.",
    "MonitorService adopts the compressed Delta_r from COCO when stop_applied is True.",
    "FirmaService certifies the structural state with six canonical fields including sha256 of W.",
    "WVersionManager records when W changed using sha256 trace without copying the matrix.",
    "BehaviorGraph G operates on a fixed termap of 18 behavior categories.",
    "D_G measures behavioral drift from G_ref — parallel to D_ckm, not summable with it.",
    "The IAP Chatroom operates under BROADCAST condition: all messages reach all devices.",
    "Coupled silence: a device that does not read still depends on the channel for timing.",
    "STOP never produces loss. Fraccion_rec is greater than or equal to 1.0 in all cases.",
]

TEXTS = [
    "The neural network optimizer converges using stochastic gradient descent with momentum.",
    "Distributed ledger consensus mechanisms require Byzantine fault tolerance.",
    "Quantitative easing affects bond yields through duration risk repricing.",
    "The photosynthesis cycle converts carbon dioxide using chlorophyll pigmentation.",
    "Machine learning regularization prevents overfitting through L2 penalty terms.",
    "Supply chain disruptions propagate through inventory buffer depletion cascades.",
    "Electrochemical battery degradation follows Arrhenius kinetics at elevated temperatures.",
    "Sovereign debt sustainability depends on primary balance and growth differential.",
    "Protein folding pathways are governed by hydrophobic collapse and entropic forces.",
    "Transformer attention mechanisms compute scaled dot-product similarity scores.",
    "Geopolitical risk premiums compress credit spreads in emerging market bonds.",
    "Neuroplasticity mechanisms involve long-term potentiation at synaptic junctions.",
    "Carbon capture sequestration requires geological formation permeability assessment.",
    "Algorithmic trading strategies exploit microstructure inefficiencies at millisecond latency.",
    "Epigenetic methylation patterns regulate gene expression without sequence alteration.",
    "Monetary policy transmission operates through credit channel and wealth effects.",
    "Topological data analysis uses persistent homology to detect structural features.",
    "Immunological memory formation requires antigen-presenting cell activation cascades.",
    "Option pricing models incorporate stochastic volatility through Heston dynamics.",
    "Cognitive load theory constrains working memory through chunking mechanisms.",
]

def main():
    # 1. Construir corpus desde precarga CKM (fase acumulación → evaluación)
    corpus = CorpusService(storage_path=CORPUS_PATH, min_texts=15)
    corpus.ingest(WARMUP_TEXTS)
    print(f"Corpus post-precarga: {corpus.status()}")
    assert corpus.mode == "evaluation", f"FAIL: corpus en modo {corpus.mode} — revisar min_texts"

    W = corpus.get_W()
    print(f"W shape: {W.shape}, mean: {W.mean():.6f}")

    # 2. Instanciar COCOThermostat con W establecida
    th = COCO(W=W, n_runs=50, seed=42)
    print(f"β_c_corpus: {th.beta_c_corpus():.4f}")

    # 3. Instanciar MonitorService CON thermostat inyectado
    monitor = MonitorService(
        corpus,
        storage_path=OUTPUT_PATH,
        n_runs_attractors=50,
        thermostat=th,
    )
    print("MonitorService instanciado con thermostat.")
    print("Iniciando evaluaciones...\n")

    stops_observed = []
    delta_r_history = []

    for i, text in enumerate(TEXTS):
        dr_before = float(monitor._Delta_r.sum()) if monitor._Delta_r is not None else 0.0
        
        panel = monitor.evaluate(text, device_id=f"test_{i:02d}")
        
        dr_after = float(monitor._Delta_r.sum()) if monitor._Delta_r is not None else 0.0
        ts = panel.get("thermostat", {}) or {}
        
        stop = ts.get("stop_applied", False)
        alpha = ts.get("alpha_used")
        zone  = ts.get("zone", "?")
        d_ckm = panel.get("D_ckm", 0)
        fi    = panel.get("fabrication_index", 0)
        temp  = ts.get("temp_signal", "?")

        delta_r_history.append({"t": i, "before": dr_before, "after": dr_after, "stop": stop})

        flag = "*** ARMSTRONG ***" if stop else ""
        print(f"t={i:2d}  fi={fi:.3f}  D_ckm={d_ckm:.4f}  zone={zone:12s}  "
              f"temp={str(temp):8s}  Δ_r {dr_before:.0f}→{dr_after:.0f}  "
              f"stop={stop}  α={alpha}  {flag}")

        if stop:
            stops_observed.append({
                "t": i,
                "text_preview": text[:60],
                "D_ckm": d_ckm,
                "fi": fi,
                "zone": zone,
                "temp_signal": temp,
                "alpha_used": alpha,
                "Delta_r_before": dr_before,
                "Delta_r_after": dr_after,
                "compression_ratio": round(dr_after / dr_before, 4) if dr_before > 0 else None,
            })

    print(f"\n=== RESULTADO ===")
    print(f"STOPs observados: {len(stops_observed)}/{len(TEXTS)}")
    
    if stops_observed:
        print("\nPrimer ARMSTRONG:")
        print(json.dumps(stops_observed[0], indent=2))
        print("\nFracción_rec = compression_ratio (debería ser ≥ 1.0 por REG_destruccion_recuperacion)")
    else:
        print("STOP no disparó. Verificar: D_ckm alcanzó 0.40? Ver trayectoria en OUTPUT_PATH.")
        print("Considerar: agregar más textos o textos con mayor fi.")

    # Guardar delta_r history
    summary_path = Path(OUTPUT_PATH).parent / "armstrong_delta_r_history.json"
    summary_path.write_text(json.dumps(delta_r_history, indent=2))
    print(f"\nHistorial Δ_r guardado: {summary_path}")
    print(f"Trayectoria completa: {OUTPUT_PATH}")


# ---------------------------------------------------------------------------
# TEXTO COMPLETO EN JSONL — modo debug
# ---------------------------------------------------------------------------
# _persist() en monitor_service.py trunca texto a 80 chars.
# Para este experimento: monkey-patch local, sin tocar el servicio.
#
# Agregar esto DESPUÉS de instanciar monitor, ANTES del loop:
#
#   def _persist_full(self, text, panel, agent_id=None):
#       t = len(self.trajectory())
#       with open(self._storage, "a") as f:
#           f.write(json.dumps({
#               "t": t, "agent_id": agent_id,
#               "text": text,              # completo, sin truncar
#               "panel": panel
#           }) + "\n")
#
#   monitor._persist = _persist_full.__get__(monitor, MonitorService)
#
# NO modificar monitor_service.py.

if __name__ == "__main__":
    main()
```

---

## Criterio de éxito

**Condición Armstrong:**
```
stop_applied = True  (al menos una vez)
Delta_r_after < Delta_r_before  (compresión confirmada)
panel["thermostat"]["alpha_used"] ∈ [0.05, 0.30]
```

**Si STOP no dispara con 20 textos:**
- Reportar D_ckm máximo alcanzado
- Reportar fi promedio
- Agregar 10 textos adicionales (misma estrategia de vocabulario ajeno)
- No modificar el código — solo agregar textos

**Si STOP dispara:**
- Copiar el bloque "Primer ARMSTRONG" al REG
- Guardar armstrong_stop_coco_v1.jsonl completo
- Confirmar compression_ratio ≥ 1.0 contra REG_destruccion_recuperacion_v1

---

## Output esperado

```
registers/REG_armstrong_stop_coco_v1.md
process/experiments/armstrong_stop_coco_v1.jsonl
process/experiments/armstrong_delta_r_history.json
```

## No modificar

agent_device_skin.py, groq_research_agent.py, corpus_service.py,
coco.py (leer, no tocar), monitor_service.py (leer, no tocar).

El script es de lectura + inyección. Sin cambios al código de servicios.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
