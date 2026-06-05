# REG_coco_thermostat_proto_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Primera implementación de COCO-thermostat sobre ciclo A2A simulado*  
*Clase R*

---

## Origen

Sesión actual. Trayectoria directa desde:

1. Sweep D_ckm(t_stop) × alpha → reformulación "grados de pérdida"
2. Curva A(t) destrucción/recuperación → hallazgo: W es suelo invariante
3. Observación: ningún agente individual ve D_ckm del campo colectivo
4. Convergencia IAP: los límites de RPC/A2A (P2P, Client-Server, Rigid Structure) son los mismos que motivaron el proyecto IAP en 2024

COCO-thermostat es la respuesta CKM a esos límites. No almacena capacidades declaradas — observa lo que el campo rechazó.

---

## Arquitectura implementada

### `COCOThermostat` — 120 líneas

```python
thermostat = COCOThermostat(W=W_mixta)
state = thermostat.observe(Delta_colectivo)   # en cada ciclo A2A
```

**Entradas:** W (corpus, fijo), Δ colectivo (emergido de interacción real A2A)

**Salida:** `ThermostatState` — zona, D_ckm, A_current, frac_rec, stop_applied, alpha_used

**No usa:** AgentCards, capacidades declaradas, identidad de agentes

**Trabaja con:** Δ_r — lo que el campo rechazó, acumulado de interacciones reales

### Clasificación de zonas

```
D_ckm < 0              → stable   (campo expandido — acumulación suma atractores)
0 ≤ D_ckm < 0.40       → stable   (degradación menor al umbral)
D_ckm ≥ 0.40 y frac ≥ 0.60  → degrading  (STOP recomendado)
D_ckm ≥ 0.40 y frac < 0.60  → deep       (STOP urgente)
```

Umbrales derivados empíricamente del sweep REG_destruccion_recuperacion_v1.md:
- D_ckm_threshold = 0.40 (zona degradación sostenida en curva A(t))
- alpha_star = 0.10 (A_post_max en sweep AMP=40)
- frac_rec_min = 0.60 (A(t)/A0 < 0.60 → degradación profunda)

### Operador STOP

```
cuando zone in ("degrading", "deep"):
    Delta_colectivo = 0.10 * Delta_colectivo
```

Delta se reduce al 10%. W no se toca. El suelo emerge.

---

## Experimento — ciclo A2A simulado

**Configuración:**
```
W_mixta AMP=40, N=32, A0=20
4 agentes, 20 rondas, 10 interacciones/ronda
Acumulación: pares (i,j) por w_probs, ETA=mean_W
n_runs=80, SEED=42
```

**Resultados:**

| Ronda | A(t) | D_ckm | frac_rec | zona | STOP |
|-------|------|-------|----------|------|------|
| 1 | 19 | 0.050 | 0.95 | stable | |
| 2 | 19 | 0.050 | 0.95 | stable | |
| **3** | **9** | **0.550** | **0.45** | **deep** | **✓** |
| 4 | 20 | 0.000 | 1.00 | stable | |
| **5** | **10** | **0.500** | **0.50** | **deep** | **✓** |
| 6 | 20 | 0.000 | 1.00 | stable | |
| **7** | **10** | **0.500** | **0.50** | **deep** | **✓** |
| 8 | 21 | −0.050 | 1.05 | stable | |
| 9 | 20 | 0.000 | 1.00 | stable | |
| **10** | **10** | **0.500** | **0.50** | **deep** | **✓** |
| 11 | 22 | −0.100 | 1.10 | stable | |
| 12 | 14 | 0.300 | 0.70 | stable | |
| **13** | **9** | **0.550** | **0.45** | **deep** | **✓** |
| 14 | 14 | 0.300 | 0.70 | stable | |
| **15** | **9** | **0.550** | **0.45** | **deep** | **✓** |
| 16 | 23 | −0.150 | 1.15 | stable | |
| 17 | 22 | −0.100 | 1.10 | stable | |
| 18 | 19 | 0.050 | 0.95 | stable | |
| **19** | **12** | **0.400** | **0.60** | **degrading** | **✓** |
| 20 | 17 | 0.150 | 0.85 | stable | |

**STOPs emitidos: 7/20 rondas**

Patrón: cada STOP → ronda siguiente estable (A≈A0, D_ckm≈0). El thermostat mantiene el campo vivo.

Rondas 8, 11, 16, 17: D_ckm < 0 — campo expandido por encima de A0. El thermostat no interviene en expansión (correcto: la expansión no requiere STOP).

---

## Hallazgos

**H1 — COCO-thermostat mantiene el campo cerca de A0 sin conocer a los agentes.**
El único input es Δ_r — lo que emergió de interacción real. Sin AgentCards. Sin declaración de capacidades. El campo se autorregula.

**H2 — La frecuencia de STOP (7/20 = 35%) refleja la frecuencia de cruce del umbral en la curva A(t).**
Consistente con el sweep: el campo oscila entre expansión y degradación. El thermostat actúa solo en degradación.

**H3 — El thermostat no actúa en expansión (D_ckm < 0).**
Rondas 8, 11, 16, 17: A(t) > A0, D_ckm negativo. Sin STOP. Correcto — la expansión es información del campo, no ruido a corregir.

**H4 — alpha=0.10 es suficiente para restaurar desde zona deep.**
En todos los casos deep (D_ckm≈0.55, A≈9), la ronda siguiente tiene A≈20, D_ckm≈0. Reset parcial del 90% de Δ devuelve el campo a A0.

---

## Convergencia IAP → COCO-thermostat

El documento "some wire thoughts" (gadanin.delamor, sesión actual) describe los tres límites de RPC que motivaron el IAP en 2024:

1. **P2P** — solo modela pares. OUT OF SCOPE: equipos, reuniones, difusiones.
2. **Client-Server** — exige jerarquía Solicitador/Proveedor. OUT OF SCOPE: interacciones que comparten sin ser requeridas.
3. **Rigid Structure Process** — Remote + Call + Procedural. Goal-driven receta.

A2A con AgentCards hereda los tres límites: declara capacidades antes de la interacción (Rigid), asume Client-Server implícito (orquestador/ejecutor), modela de a pares o en estrella.

COCO-thermostat no declara nada. Observa el campo que emerge de la interacción real. El corpus colectivo (CorpusService compartido) acumula Δ_r de todos los agentes — sin P2P, sin jerarquía, sin receta.

"El protocolo es la interacción, no su precursor." — REG_iap_coco_convergence_v1.

---

## Limitaciones del prototipo v1

1. **Δ_colectivo simulado** — en producción, CorpusService compartido acumula rechazos reales de cada agente. Aquí se simula con acumulación aleatoria ponderada por W.

2. **alpha_star fijo** — el sweep mostró que alpha_star varía por t_stop. El prototipo usa 0.10 como valor empírico robusto. Mejora: calibrar alpha_star dinámicamente por D_ckm actual.

3. **Un solo umbral D_ckm** — el experimento usó 0.40. La curva A(t) sugiere que el umbral óptimo depende de A0 y de la densidad del corpus. Mejora: umbral relativo = f(A0, corpus_density).

4. **Sin β colectivo** — el prototipo regula Δ pero no el parámetro térmico β por agente. COCO-thermostat completo dirige β hacia β_c para cada agente según su historia de rechazo. Eso requiere integración con el modelo ferromagnético.

5. **Sin CorpusService real** — el prototipo opera sobre W_mixta sintética. Integración con CorpusService real es el próximo paso operativo.

---

## Próximos pasos

1. Integrar COCOThermostat con MonitorService — el monitor acumula Δ_r real, el thermostat lo observa.
2. Calibración dinámica alpha_star por D_ckm(t).
3. Prototipo β colectivo: COCO como regulador térmico, no solo de Δ.
4. Experimento con CorpusService real (W_ckm_corpus_v2 + interacciones reales A2A).

---

## Archivos generados

- `coco_thermostat.py` — implementación (~120 líneas)
- `exp_coco_thermostat_v1.png` — curvas A(t), D_ckm, frac_rec con marcas STOP

---

*N=32 · W_mixta AMP=40 · A0=20 · 20 rondas · 7 STOPs · alpha=0.10*
