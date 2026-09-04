# TASK_coco_alpha_compuesto_v3.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*v3 — agrega n_runs al panel (hallazgo sweep n_runs 60→70)*

---

## Objetivo

Dos extensiones independientes al ciclo de decisión de COCO:

1. **alpha compuesto**: `_alpha_for()` incorpora eficiencia histórica de STOPs
   anteriores vía `landscape_history`.
2. **criterio de rebuild por gradiente**: `CorpusService._rebuild()` se
   dispara no solo por volumen sino por señal estructural del campo.

---

## Contexto — lo que ya existe

- `COCO.landscape_history()` — lista de dicts con `delta_A`, `delta_cS`,
  `alpha_used`, `D_ckm` por cada STOP (T5b).
- `COCO._alpha_for(D_ckm)` — mapeo lineal D_ckm → α. Retrospectivo.
  No usa landscape_history.
- `COCO._alpha_trajectory` — lista de `{t, alpha, D_ckm, delta_A}`.
- El ruido estocástico ya existe estructuralmente en `_count_attractors`
  (n_runs finito, coupon-collector). No agregar ε artificial.

---

## Extensión 1 — alpha compuesto

### Principio

Si los STOPs anteriores con α pequeño produjeron `delta_A` grande —
el campo responde bien a compresiones suaves → empujar α hacia menor.

Si los STOPs anteriores fueron ineficientes (α grande, `delta_A` pequeño
o negativo) → empujar α hacia mayor.

### Fórmula

```python
alpha_final = clip(alpha_for(D_ckm) + gamma * landscape_component, ALPHA_MIN, ALPHA_MAX)
```

Donde `landscape_component`:

```python
def _landscape_component(self) -> float:
    """
    Gradiente de eficiencia histórica de STOP.
    Positivo → STOPs anteriores fueron eficientes con α bajo → reducir α.
    Negativo → STOPs ineficientes → aumentar α.
    Retorna 0.0 si no hay historia suficiente (< 2 entradas).
    """
    h = self.landscape_history()
    if len(h) < 2:
        return 0.0
    # Eficiencia = delta_A / alpha_used (delta_A por unidad de compresión)
    efficiencies = [
        e["delta_A"] / e["alpha_used"]
        for e in h[-5:]   # ventana últimas 5 entradas
        if e.get("alpha_used") and e["alpha_used"] > 0
        and e.get("delta_A") is not None
    ]
    if not efficiencies:
        return 0.0
    return -np.mean(efficiencies) * self._gamma  # negativo: más eficiencia → α más bajo
```

### Parámetro

`gamma: float = 0.01` en `COCO.__init__` — conservador, ajustable.
No hardcodeado como constante de módulo — es variable de instancia.

```python
self._gamma = gamma
```

### Integración en `observe()`

```python
alpha_used = clip(
    self._alpha_for(D_ckm) + self._landscape_component(),
    ALPHA_MIN, ALPHA_MAX
)
```

Solo activar si `track_landscape=True` y `len(landscape_history()) >= 2`.
Si no hay historia suficiente, usar `_alpha_for(D_ckm)` solo — sin cambio.

---

## Extensión 2 — criterio de rebuild por gradiente D_ckm

### Principio

El rebuild de W hoy se dispara por volumen (`len(texts) >= min_texts`).
El campo puede no necesitar rebuild aunque el volumen crezca — o necesitarlo
antes de que el volumen lo indique.

Señal estructural: el gradiente de D_ckm.

`∇D_ckm(t) = D_ckm(t) - D_ckm(t-1)`

- Positivo sostenido (N pasos) → campo degradándose más rápido que COCO
  puede comprimir → rebuild urgente aunque volumen sea bajo.
- Negativo sostenido → campo ganando atractores → esperar, no rebuild.
- Cercano a cero sostenido → campo estabilizado en ese nivel.

### Implementación

En `CorpusService`, nuevo método:

```python
def should_rebuild(self, d_ckm_history: list[float], n: int = 3) -> bool:
    """
    Retorna True si el gradiente de D_ckm es positivo sostenido por n pasos.
    Señal estructural de rebuild — complementa el criterio de volumen.
    """
    if len(d_ckm_history) < n + 1:
        return False
    recent = d_ckm_history[-(n+1):]
    gradients = [recent[i+1] - recent[i] for i in range(n)]
    return all(g > 0 for g in gradients)
```

### Tres señales de rebuild (jerarquía)

```python
# En CKMMonitor.on_message() o equivalente:
rebuild_needed = (
    corpus.should_rebuild(d_ckm_history, n=3)   # estructural — prioridad
    or len(corpus._texts) >= corpus._min_texts * 2  # volumen — fallback
    or ciclos_sin_rebuild >= MAX_CICLOS          # tiempo — último recurso
)
```

El tiempo es fallback — no el criterio principal.

---

## Criterio de éxito

```bash
python tests/test_coco.py              # 28/28
python tests/test_monitor_services.py  # 35/35

# Extensión 1 — verificar que landscape_component modifica alpha:
coco = COCO(W=W, track_landscape=True, gamma=0.01)
# ... correr 3+ STOPs ...
h = coco.landscape_history()
assert len(h) >= 2
alpha_base = coco._alpha_for(0.45)
alpha_comp = coco._landscape_component()
print(f"alpha_base={alpha_base:.4f} landscape_component={alpha_comp:.4f}")
# No asumir signo — registrar y documentar

# Extensión 2 — verificar gradiente:
from services.corpus_service import CorpusService
cs = CorpusService.__new__(CorpusService)
# degradación sostenida → rebuild
assert cs.should_rebuild([0.3, 0.35, 0.40, 0.45], n=3) == True
# recuperación → no rebuild
assert cs.should_rebuild([0.4, 0.35, 0.30, 0.25], n=3) == False
print("OK — should_rebuild")
```

---

## NO modificar

- Lógica base de `_alpha_for()` — se preserva, el compuesto la llama
- Constantes ALPHA_MIN, ALPHA_MAX, D_CKM_THRESHOLD
- `agent_device_skin.py`, `groq_research_agent.py`, REGs históricos
- Si `track_landscape=False` o historia insuficiente: comportamiento
  idéntico al actual — sin regresión

---

## Archivos a modificar

```
services/coco.py           — _landscape_component(), gamma param,
                             integración en observe()
services/corpus_service.py — should_rebuild()
iap_chatroom/ckm_monitor.py — jerarquía de señales de rebuild
```

---

*Repo: gadanindelamor/ckm · Codespace: ckm*

---

## Panel — trazabilidad de la decisión (v2)

En `monitor_service.py`, después de construir el bloque `panel["thermostat"]`:

```python
panel["thermostat"]["landscape_component"] = (
    self._thermostat._landscape_component()
    if self._thermostat is not None and self._thermostat._track_landscape
    else None
)
panel["thermostat"]["gamma"] = (
    self._thermostat._gamma
    if self._thermostat is not None
    else None
)
```

`alpha_used` ya está — registra el alpha final aplicado.
`landscape_component` registra cuánto pesó el componente histórico.
`gamma` registra el parámetro de sensibilidad activo en ese momento.

Sin estos campos: alpha_used es observable, su composición no.
Con estos campos: trace_ip de la decisión de alpha es completa en el JSONL.

---

## Panel — n_runs (v3)

Agregar a `panel["thermostat"]` en `monitor_service.py`:

```python
panel["thermostat"]["n_runs"] = (
    self._thermostat._n_runs
    if self._thermostat is not None
    else None
)
```

Motivación: hallazgo sweep `n_runs` (Ago 2026) muestra quiebre abrupto
entre n_runs=60 (3/20 STOPs) y n_runs=70 (20/20 STOPs) en seed=123.
D_ckm_tail no converge hasta n_runs=200 — el estimador tiene sesgo
estructural dependiente de n_runs.

Sin este campo en el panel: D_ckm y alpha_used no son interpretables
sin conocer con qué n_runs se calcularon. Con este campo: cada decisión
de STOP queda trazable junto al parámetro del instrumento que la produjo.
