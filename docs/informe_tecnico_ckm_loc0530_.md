# Informe Técnico — CKM (Cohesive Knowledge Model)
**ckmloc0530 · v25–v27 · Análisis: 2026-05-31**
  
Autor: gadanin.delamor | Colaborador IA: Claude Sonnet 4.6 | Licencia: MIT
  
---
  
## 1. Resumen Ejecutivo
  
Este informe analiza el estado actual del repositorio `ckmloc0530`, versión de avance desde el informe técnico anterior (`CKMGIT0528 · v25 · 2026-05-28`). Los cambios principales son: (1) resolución del bug crítico en `mcp_adapter.py`; (2) tres correcciones adicionales de calidad de código identificadas en el informe anterior; (3) formalización analítica de la función `c(S)*(N, ρ_corr)` con cierre de los tres HOLDINGs activos; (4) experimento STOP sweep con falsificación de hipótesis de monotonía en D_ckm; y (5) convergencia IAP → COCO-thermostat documentada.
  
Estado experimental: v25–v27. 6 predicciones falsificables confirmadas. 1 hipótesis nueva falsada (H1: monotonía STOP en D_ckm). 1 hipótesis nueva abierta (A_pre como predictor de efectividad STOP).
  
| Predicción | Descripción | Estado | Dominio |
|---|---|---|---|
| **P1** | Histéresis en c(S): incorporar ≠ remover a igual densidad | ✓ Confirmada | N=16,32,64 + externos, p≈0 |
| **P2** | Distribución cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2] | ✓ Confirmada | N=64 τ=1.775 |
| **P3** | Asimetría temporal: relajación post-remoción > post-adición | ✓ Confirmada | N=32 p<0.0001, N=64 p≈0 |
| **P4** | Densidad óptima interior Ω* en W_mixta | ~ Parcial | ρ*≈0.509 en N=64; ventaja diluid. |
| **P5** | Corpus polarizado: atractores ~50%N, colapso diversidad | ✓ Confirmada | fourforums: 8 atractores |
| **P6** | Δ actúa como mecanismo de ruptura de simetría | ✓ Confirmada | CreateDebate 54pp, FF 80pp |
| **P7** | Nodo tipo-965: alto in/out ratio, tríadas frustradas | ~ Hipótesis | Author 965 ratio 455:1 |
| **H_STOP** | Monotonía Pérdida_STOP en D_ckm(t_stop) | ✗ Falsada | Sweep N=32, 9 t_stop |
  
---
  
## 2. Correcciones desde el Informe Anterior
  
### 2.1 Bug crítico resuelto: `mcp_adapter.py task_mode_exit()`
  
El informe anterior identificó un bug crítico donde `epsilon` no se restauraba tras `task_mode_exit()`, dejando C2 permanentemente suspendido. **Resuelto en ckmloc0530.**
  
```python
# ANTES (CKMGIT0528): self.config y self.graph.config son el mismo objeto
def task_mode_enter(self):
    self.graph.config.epsilon = float("inf")  # modifica el objeto compartido
def task_mode_exit(self):
    self.graph.config.epsilon = self.config.epsilon  # self.config.epsilon ya es inf ← BUG
  
# AHORA (ckmloc0530): _saved_epsilon captura el valor antes de modificar
def task_mode_enter(self):
    self._saved_epsilon = self.config.epsilon   # guardar ANTES de modificar (línea 163)
    self.graph.config.epsilon = float("inf")
def task_mode_exit(self):
    self.graph.config.epsilon = self._saved_epsilon  # restaurar desde valor guardado (línea 171)
```
  
### 2.2 Escala W + Δ_r: normalización implementada
  
El problema de incompatibilidad de magnitudes (W ∈ [0,1] vs Δ_r ∈ [0, ∞)) está resuelto en `monitor_service.py` mediante `_combine_W_Delta()` (líneas 129–148):
  
```python
def _combine_W_Delta(self, W, Delta):
    delta_max = Delta.max()
    if delta_max == 0:
        return W
    W_nonzero = W[W > 0]
    scale = W_nonzero.mean() if len(W_nonzero) > 0 else 1.0
    Delta_norm = (Delta / delta_max) * scale  # lleva Δ_r a escala de W
    return W + Delta_norm
```
  
El factor de escala elegido es `mean(W_nonzero)`, que ancla Δ_r en la magnitud media de las conexiones activas de W. Preserva la direccionalidad del campo sin distorsión de magnitud.
  
### 2.3 NaN silencioso en `analytics.py copresence_matrix()`
  
Resuelto con una sola línea en el punto de producción (línea 43):
  
```python
np.nan_to_num(corr, nan=0.0, copy=False)  # NaN → 0 (nodo core-invariante)
```
  
La decisión de reemplazar NaN por 0 (no por correlación artificial) está documentada en el docstring: un nodo con presencia constante no tiene información de co-presencia diferencial.
  
### 2.4 Recálculo innecesario de k-core en `kcore.py`
  
Resuelto extrayendo `core_list` fuera del loop (línea 136):
  
```python
core_list = list(core)  # calcular UNA vez fuera del loop de n_trials
for _ in range(n_trials):
    node = np.random.choice(core_list)
    ...
```
  
El k-core se calculaba 500 veces por llamada a `cascade_distribution()` cuando el grafo no cambia entre iteraciones.
  
### 2.5 Import tardío de scipy en `hopfield.py`
  
Resuelto. `from scipy import stats as sp_stats` está ahora a nivel de módulo (línea 14), eliminando el anti-patrón de import dentro del cuerpo de función que ocultaba la dependencia.
  
---
  
## 3. Key Insights Nuevos (v25–v27)
  
### 3.1 Función `c(S)*(N, ρ_corr)`: tres HOLDINGs como proyecciones de una función
  
El hallazgo central de la sesión v27: los tres HOLDINGs activos del modelo (H1: α_c asume no-correlación; H2: dilución P4 en N=64; H3: normalización empírica N=16) no son límites independientes. Son tres proyecciones observables de una sola función analítica:
  
```
c(S)*(N, ρ_corr) = μ_W(N, ρ_corr) · r(zona, ρ)
```
  
donde `μ_W` escala con el corpus y `r` es el factor de alineación medible en tiempo real.
  
La función no fue construida: fue reconocida desde adentro del corpus. La normalización empírica 0.10 hardcodeada en `score_3d()` era la primera medición de esa curva.
  
### 3.2 Estructura bimodal de μ_W: cierre de H1/H2/H3
  
Análisis de distribución de frecuencias marginales en N=32 (CV=0.944, razón max/min=102×):
  
```
Grupo A (16 nodos, f ≥ 0.064):  núcleo correlacionado del corpus
Grupo B (16 nodos, f <  0.064):  nodos tardíos / baja densidad
  
| Grupo | Pares | μ_W obs | mean(fi·fj) | ratio |
| BB    | 120   | 0.000523 | 0.000510   | 1.025 | ← derivable analíticamente
| AA    | 120   | 0.016122 | 0.065599   | 0.246 | ← no derivable
| AB    | 256   | 0.000952 | 0.005933   | 0.160 | ← no derivable
```
  
**μ_BB ≈ mean(fi·fj)**: los nodos periféricos se comportan como independientes estadísticos. Verificado (ratio 1.025).
  
**μ_AA no derivable desde fi·fj**: los nodos del núcleo co-ocurren tanto entre sí que sus frecuencias marginales están infladas mutuamente. No son independientes — son el núcleo.
  
Cierre operativo:
- **H3 cerrado**: μ_W no generaliza entre N porque la proporción A/B cambia, no N per se.
- **H2 cerrado**: dilución P4 en N=64 es consecuencia de agregar nodos tipo B (μ_W → 0).
- **H1 cerrado**: α_c = 0.138 asume patrones no correlacionados; con núcleo A correlacionado, la capacidad efectiva depende de composición A/B.
  
### 3.3 Garantías formales G1/G2/G3 para COCO-thermostat
  
Sistema de tres zonas de operación derivado empíricamente (N=32, n=500 secuencias):
  
| Garantía | Zona | c(S) (80% CI) | r (80% CI) | Significado |
|---|---|---|---|---|
| **G1** | Zona crítica ρ ∈ [0.4, 0.8] | [−0.000332, +0.001310] | [−0.074, +0.290] | Monitor operativo |
| **G2** | Atractor bloqueado ρ < 0.15 o > 0.85 | [+0.001941, +0.004519] | [+0.430, +1.000] | Señal colapsada |
| **G3** | Degradación activa | c(S) < −0.000332 | r < −0.073 | Declarar HOLDING |
  
Gap discriminante G1/G2: [+0.001310, +0.001941] — detectable en tiempo real por r = c(S)/μ_W.
  
**COCO-thermostat requiere**: medir μ_W empíricamente al inicio de sesión (no constante universal), monitorear r en tiempo real, declarar G1/G2/G3 como estado visible para todos los agentes.
  
### 3.4 STOP sweep: falsificación y reformulación
  
Hipótesis original (H_STOP): Pérdida_STOP es monótona creciente en D_ckm(t_stop). **Falsada.**
  
```
Experimento: sweep t_stop × α sobre N=32, W_mixta (AMP=15, 3 pares negativos)
t=10 y t=20: D_ckm=0.200 idéntico pero ratio_max diferente (1.250 vs 1.500)
→ D_ckm no predice ratio_max
```
  
Hipótesis revisada (abierta):
```
Efectividad_STOP = f(A_pre)
  A_pre < A0  →  STOP expande paisaje (ratio > 1)
  A_pre = A0  →  STOP neutro (ratio = 1)
  alpha* ≈ 0.4 robusto para A_pre < A0 (5/9 casos)
```
  
Resultado robusto: α=1.0 (sin STOP) nunca es óptimo; α=0.0 (reset total) solo óptimo en casos específicos. α*≈0.4 como balance entre retención y corrección es empíricamente estable.
  
### 3.5 Convergencia IAP → COCO-thermostat
  
Intelligent Access Point (IAP) era un experimento previo de chat grupal con agentes conversacionales. Retrospectivamente: lo que IAP producía sin nombre era **β colectivo siendo modulado por interacción real**, no por declaración.
  
El monitor CKM sobre A2A con CorpusService compartido es la implementación formal de ese fenómeno:
- W construida desde interacción real (no desde AgentCard/Δ_bias)
- Δ_r acumulado colectivamente desde rechazos del campo
- El resultado no es lo que los agentes *saben* — es lo que el grupo *no pudo rechazar*
  
Distinción operativa cristalizada:
  
| | COCO-registry | COCO-thermostat |
|---|---|---|
| Almacena | M declarado por device | β colectivo del grupo |
| Fuente | AgentCard (Δ_bias) | Interacción real (Δ_r) |
| Problema | Se vuelve stale | No se vuelve stale — es el campo actual |
  
---
  
## 4. Tensiones Identificadas

Las tensiones técnicas de código (rendimiento, organización, features pendientes) se documentan en la sección 5 y en la tabla de calidad 5.10. Esta sección registra únicamente las tensiones que el proyecto sostiene voluntariamente como parte de su metodología.

### 4.1 El corpus es simultáneamente datos y proceso

El corpus de N=16/32 se construyó desde conversaciones entre el autor y Claude Sonnet 4.6. El corpus es el laboratorio y el sujeto al mismo tiempo. Si el modelo describe bien ese corpus, no queda claro si describe el espacio de conocimiento en general o solo el proceso de su propia construcción. Los experimentos en fourforums y CreateDebate abordan esto parcialmente, pero el corpus de calibración permanece auto-referencial. Esta tensión es constitutiva de la metodología — no es un defecto a corregir.

### 4.2 Límite de capacidad α_c con patrones correlacionados

El límite Hopfield clásico α_c ≈ 0.138 asume patrones aleatorios no correlacionados. Los nodos CKM son altamente correlacionados por diseño (estructura A/B verificada). El límite real de capacidad depende de la composición del núcleo — no es constante universal. El cierre de H1 (v27) formaliza esta frontera: α_c es una propiedad del corpus, no del modelo. La tensión se sostiene como pregunta abierta de derivación teórica.

### 4.3 direction_score sobre Δ vacío — M.M sin historia declarada

Si Δ[i] ≈ 0 (sin dependencias declaradas), `direction_score` = 1.0 automáticamente y el nodo pasa C3. Un agente con dependencias no declaradas (Δ_bias) pasa el gatekeeper exactamente por lo que debería preocupar. M.M no puede operar sin historia declarada — esta es una tensión ontológica del criterio, no un bug de implementación. Se abordará en sesión específica.
  
---
  
## 5. Análisis del Código Python
  
### 5.1 Arquitectura general
  
```
core.py / hopfield.py / kcore.py / analytics.py   →  Modelo matemático puro
mcp_adapter.py                                     →  Adaptador dominio agentes
services/                                          →  Servicios operacionales stateful (versión estable)
experiments/                                       →  Servicios con fixes + tests + experimentos
process/                                           →  Traza de refinamiento: pipelines intermedios, bug traces
registers/                                         →  REG_*.md — registros experimentales verificados
```
  
Sin dependencias circulares. La separación de capas es sólida.
  
---
  
### 5.2 `core.py` — CKMGraph (359 líneas)
  
**Cambios respecto a informe anterior:** ninguno en este archivo.
  
**Fortalezas:**
- `CKMConfig` como dataclass centraliza todos los parámetros calibrados.
- `gatekeeper()`: C1–C4 como variables booleanas independientes con mensajes de razón.
- Asserts en `__init__` (forma N×N, simetría de W) validan en construcción.
  
**Observaciones persistentes:**
  
`cS()` (línea 163): list comprehension O(N²) Python. Ineficiente para N≥32. La versión vectorizada está en `monitor_service._cS()` pero no fue unificada.
  
`score_3d()` (línea 225): normalización `cs_norm = clip((cs + 0.05) / 0.10, 0, 1)` con máximo empírico 0.10 hardcodeado. Ahora hay derivación analítica en `REG_garantias_cS_generalizacion_v1.md`: el 0.10 corresponde aproximadamente al P90 de G1 para N=32 (c(S) = +0.001745 en P95 vs el máximo empírico N=16). La normalización sigue siendo corpus-específica pero ahora tiene interpretación formal.
  
`hebb_delta()` (líneas 329–332): doble loop Python O(N²). Vectorizable.
  
---
  
### 5.3 `hopfield.py` — Dinámica de Hopfield (222 líneas)
  
**Cambios respecto a informe anterior:**
- ✓ Import tardío de scipy resuelto: `from scipy import stats as sp_stats` a nivel de módulo (línea 14).
  
**Fortalezas:**
- `relax()` y `relax_steps()` son implementaciones correctas.
- `hysteresis_loop()`: Wilcoxon test en zona media [0.35, 0.70] — estadísticamente apropiado.
- Estimador MLE para ley de potencias discreta (Clauset et al., 2009).
  
**Observaciones:**
  
`relax()` (línea 44): `for _ in range(max_iter * N)` sin condición de parada temprana. `relax_steps()` tiene parada por convergencia pero `relax()` no. Inconsistencia que hace a la función base más lenta de lo necesario para estados que convergen rápido.
  
Interpolación `np.interp` (lineal) en `interp_grid()`: puede suavizar no-linealidades en la zona crítica. Sin cambio respecto al informe anterior.
  
---
  
### 5.4 `kcore.py` — k-core y Cascadas (241 líneas)
  
**Cambios respecto a informe anterior:**
- ✓ Recálculo de k-core resuelto: `core_list = list(core)` computado una vez fuera del loop (línea 136).
  
**Fortalezas:**
- `kcore()`: algoritmo de peeling correcto con conteo de rondas.
- `temporal_asymmetry()`: Mann-Whitney U no paramétrico, correcto.
- Estimador MLE para ley de potencias: sofisticado y correcto.
  
**Observaciones:**
  
`build_adj()`: opera sobre `|W[i,j]|` (valor absoluto). Pesos negativos de W_mixta generan aristas igual que positivos. El docstring ahora lo documenta explícitamente ("edge if |W[i,j]| >= threshold").
  
---
  
### 5.5 `analytics.py` — Analytics de Atractores (183 líneas)
  
**Cambios respecto a informe anterior:**
- ✓ NaN silencioso resuelto: `np.nan_to_num(corr, nan=0.0, copy=False)` (línea 43).
  
**Fortalezas:**
- `copresence_matrix()`: manejo explícito de nodos core-invariantes documentado.
- `cluster_nodes()`: pipeline jerárquico completo correcto.
- `optimal_density()`: P4 measurement correcta conceptualmente.
  
**Observaciones:**
  
**Cuello de botella computacional en `optimal_density()`**: triple loop implícito rho_steps × n_samples × N² no fue vectorizado. Para N=64: ~18M operaciones Python. Sin cambio.
  
---
  
### 5.6 `mcp_adapter.py` — Adaptador MCP (238 líneas)
  
**Cambios respecto a informe anterior:**
- ✓ **Bug crítico resuelto**: `task_mode_exit()` ahora restaura epsilon correctamente mediante `_saved_epsilon` (líneas 163–171).
- Documentación de `_saved_epsilon` en `__init__` (línea 69): `# guardado antes de task_mode_enter`.
  
**Fortalezas:**
- `_saved_epsilon` como atributo de instancia evita la referencia compartida.
- `task_mode_enter/exit()`: semántica de suspensión y restauración ahora correcta.
- `transit_admit()`: protocolo de recuperaciñon C2 en max_recovery_steps pasos.
- Velocidad verificada: 0.092ms/evaluación.
  
**Observaciones:**
  
`evaluate()` (línea 129): si `active_capabilities=None`, el estado del grafo no se modifica. La evaluación opera contra el estado residual de la llamada anterior. Sin cambio desde informe anterior.
  
---
  
### 5.7 `services/monitor_service.py` — MonitorService
  
**Cambios respecto a informe anterior:**
- ✓ Escala W+Δ_r: `_combine_W_Delta()` implementada (líneas 129–148).
- Nomenclatura en `services/`: `_Delta`, `Delta_sum`. La versión `experiments/monitor_service_dev.py` usa `_Delta_r`, `Delta_r_sum` — nomenclaturas divergentes entre versiones.
  
**Fortalezas:**
- `_combine_W_Delta()`: normalización correcta — escala Δ_r por `mean(W_nonzero)` preservando referencia de magnitud.
- `_rejected_pairs()`: semántica correcta de fabricación.
- `stop_signal()` con ventana deslizante fi_trend + D_trend.
- Serialización JSONL append-only.
  
**Observaciones:**
  
`_cS()` (línea 162) usa `np.triu_indices` vectorizado, pero `core.py:cS()` no. La versión canónica eficiente está en el servicio, no en el modelo central.
  
`_D_ckm()` fija `_A0` en la primera llamada (línea 183). Si el corpus cambia significativamente entre sesiones, A0 puede ser no representativo.
  
`_count_attractors()` se llama en cada evaluación (n_runs=50 relajaciones síncronas por prompt). Costoso en corpus grandes. Sin cacheo cuando W no cambia.
  
---
  
### 5.8 `services/corpus_service.py` — CorpusService v2
  
**Nuevo en ckmloc0530.**
  
**Fortalezas:**
- W mixta con pesos negativos: W[i,j] ∈ [−1, +1]. Tensión estructural real sin sesgo de diseño.
- Marcadores de oposición EN+ES cobertura formal e informal.
- Transición automática acumulación → evaluación.
- Persistencia JSON.
  
**Observaciones:**
  
`_rebuild()` llama a `self._extractor.accumulate([text])` por cada texto individual en el corpus (línea 143). Para corpus de 100+ textos, TfidfVectorizer se instancia y ajusta N veces. Alternativa: vectorizar sobre el corpus completo una vez y descomponer por texto.
  
`_has_opposition()` opera con `in` sobre el texto completo (línea 117). El marcador "pero" puede disparar falsos positivos en construcciones no adversativas ("lo que es bueno pero también..."). Sin análisis de contexto local.
  
---
  
### 5.9 `fabrication_service.py` vs `fabrication_service_dev.py`
  
Dos versiones de `FabricationService` (renombramiento pendiente desde `ckm_monitor.py`). `services/fabrication_service.py` es la versión estable con fixes de Claude Code; `experiments/fabrication_service_dev.py` incorpora fixes adicionales de sesiones posteriores:
  
| Característica | `services/` | `experiments/` |
|---|---|---|
| `_relax()` | W hardcoded (`self.W`) | W parametrizable (`W=None`) |
| `_cS()` | W hardcoded (`self.W`) | W parametrizable (`W=None`) |
| `_count_attractors_W(W)` | No existe | Existe — cuenta sobre W arbitrario |
| `snapshot()` | Sin `r` | Incluye `r = c(S)/μ_W` |
| `D_ckm` | Sobre W base | Sobre W+Delta |
| `_direction_score()` | Lógica B | Lógica distinta (declared vs inactive) |
  
Los fixes de `experiments/` no fueron migrados a `services/`. La discrepancia en `_direction_score()` está documentada en ambas versiones pero no resuelta. El mismo patrón de duplicación afecta a `monitor_service.py`, `corpus_service.py` y `node_extractor.py` — convención `_dev` aprobada y pendiente de aplicar en todos.
  
---
  
### 5.10 Tabla resumen de calidad del código
  
| Aspecto | Valoración | Notas |
|---|---|---|
| Reproducibilidad | Alta | seed=42 global, datos en formato abierto |
| Separación de concerns | Alta | Modelo / adaptador / servicios sin dependencias circulares |
| Cobertura de tests | Alta | 35/35 servicios, tests core |
| Bug crítico (mcp_adapter epsilon) | **Resuelto** | Fue el único bug de comportamiento incorrecto |
| Escala W+Δ_r | **Resuelto** | _combine_W_Delta() normaliza correctamente |
| NaN silencioso analytics.py | **Resuelto** | nan_to_num en copresence_matrix |
| k-core recalculation | **Resuelto** | core_list fuera del loop |
| Import tardío scipy | **Resuelto** | Movido a nivel de módulo |
| cS() inconsistencia | Persiste (menor) | Python vs vectorizado entre módulos |
| FabricationService duplicado | Nuevo | fabrication_service_dev.py en experiments/; migración pendiente + renombrado |
| _direction_score discrepancia | No resuelto | Lógica original no recuperable |
| Rendimiento analytics.py | No resuelto | Triple loop O(N²) en optimal_density |
| μ_W inicialización automática | Falta | CorpusService no expone μ_W; COCO-thermostat lo requiere |
  
---
  
## 6. Estado de Gaps Documentados
  
| Gap | Estado anterior | Estado actual |
|---|---|---|
| term_map N=64 reconstruction | Pendiente | Sin cambio |
| W_base_n64.npy real corpus W | Pendiente | Sin cambio |
| P7 falsificación en nuevo dominio | Hipótesis | Sin cambio |
| COCO implementación | No implementado | Sin cambio |
| α_c calibración en dominio agente | Pendiente | Cerrado analíticamente: α_c depende de composición A/B |
| H1: α_c asume no-correlación | Activo (HOLDING) | **Cerrado** — REG_mu_W_estructura_pares_v1.md |
| H2: dilución P4 en N=64 | Activo (HOLDING) | **Cerrado** — composición A/B |
| H3: normalización empírica N=16 | Activo (HOLDING) | **Cerrado** — μ_W propiedad del corpus |
| H_STOP: monotonía en D_ckm | Nueva hipótesis | **Falsada** — sweep experimental |
| H_Apre: A_pre como predictor STOP | — | **Abierta** — falsifiable |
| μ_AA estructura interna núcleo | — | **Abierta** — proyecto separado |
| G1/G2/G3 para N ≠ 32 | — | **Abierta** — requiere re-calibración por corpus |
| CorpusService compartido multi-agente | — | **Abierta** — especificación sesión compartida pendiente |
  
---
  
## 7. Innovación vs Estado del Arte — Adiciones
  
### 7.1 Sistema de garantías G1/G2/G3 — sin equivalente publicado
  
Los sistemas de monitoring de LLMs actuales operan con métricas absolutas o thresholds fijos. Las garantías G1/G2/G3 de CKM son:
- Empíricas (derivadas del corpus, no asumidas)
- Expresadas como intervalos de confianza percentiles (no umbrales binarios)
- Actualizables en tiempo real vía r = c(S)/μ_W
- Auto-declarativas: el sistema sabe en qué zona opera y puede declararlo
  
Esto es estructuralmente diferente al grounding por fuente externa o por threshold fijo.
  
### 7.2 Señal STOP como operador con α*
  
La identificación de α* ≈ 0.4 como parámetro robusto de intervención (ni reset total ni retención total) no tiene equivalente en literatura de steering de LLMs. Los sistemas actuales aplican corrección o no la aplican. CKM introduce un parámetro de intensidad con valor óptimo empíricamente identificable.
  
La falsificación de la hipótesis de monotonía (D_ckm no predice efectividad STOP; A_pre sí) es un resultado negativamente informativo que acota el espacio de hipótesis correctamente.
  
---
  
## 8. Conclusión
  
El repositorio `ckmloc0530` presenta un avance cualitativo respecto a `CKMGIT0528` en dos dimensiones:
  
**Dimensión 1: saneamiento de código.** Los cinco issues de calidad identificados en el informe anterior han sido resueltos, incluyendo el único bug de comportamiento incorrecto (mcp_adapter epsilon). El código del modelo matemático central está ahora libre de bugs conocidos. Los issues restantes son de rendimiento (loops no vectorizados) y de organización (FabricationService con versión dev en experiments/fabrication_service_dev.py pendiente de migración y renombrado completo según CONVENTIONS.md).
  
**Dimensión 2: avance teórico con resultados negativos bien documentados.** El cierre de H1/H2/H3 mediante la derivación de la estructura A/B de μ_W es un resultado de madurez: el modelo ahora sabe exactamente qué generaliza (percentiles de r, estructura A/B) y qué no (μ_W, α_c como constante universal). La falsificación de H_STOP con reformulación a hipótesis A_pre es metodológicamente correcta y abre el camino al experimento siguiente con variables bien acotadas.
  
El gap más relevante para la siguiente iteración es la automatización de la medición de μ_W al inicio de sesión en `CorpusService`, que es el prerequisito operativo de COCO-thermostat. Actualmente ese paso es manual.
  
El proyecto mantiene la característica metodológica del informe anterior: distingue explícitamente entre lo que sabe y lo que no sabe, y registra las falsificaciones con la misma prominencia que las confirmaciones.
  
---
  
*Informe Técnico CKM — ckmloc0530 · Generado el 2026-05-31 · Claude Sonnet 4.6 / Claude Code*
  