# REG_avance_ckm_claudecode_v1.md

*Jun 2026 — Registro de avance del proyecto CKM según tres informes de Claude Code.*  
*Fuentes: CKMGIT0528 (28 mayo), ckmloc0530 (31 mayo), CKMGIT0602 (2 junio).*

---

## 1. Estructura del registro

Tres puntos de observación independientes. Claude Code lee el repo en cada instancia sin historia del anterior. Lo que aparece como cambio entre informes es cambio real en el proyecto.

| Instancia | Fecha | Versión repo | Acceso |
|---|---|---|---|
| CKMGIT0528 | 28 mayo 2026 | v25 | git clone |
| ckmloc0530 | 31 mayo 2026 | v25→v27 | local |
| CKMGIT0602 | 2 junio 2026 | v27 | git clone actualizado |

---

## 2. Eje de predicciones falsificables

| Predicción | CKMGIT0528 | ckmloc0530 | CKMGIT0602 |
|---|---|---|---|
| P1 histéresis | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P2 cascadas τ∈[1.5,2] | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P3 asimetría temporal | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P4 densidad óptima Ω* | ✓ Confirmada | ~ Parcial (N=64 diluida) | ✓ Confirmada (reencuadrada: W_mixta 13× W_pos) |
| P5 corpus polarizado | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P6 Delta ruptura simetría | ✓ Confirmada (54pp / 80pp) | ✓ Sin cambio | ✓ Confirmada (54pp / 100pp — corrección valor FF) |
| P7 nodo tipo-965 | ~ Hipótesis | ~ Hipótesis | ~ Hipótesis (confirmada en ambos corpora pero abierta como falsificable en nuevos dominios) |
| H_STOP monotonía D_ckm | — no formulada | ✗ Falsada | ✗ Falsada + reformulada como f(A_pre) |
| HOLDINGs H1/H2/H3 | Activos | **Cerrados** (estructura A/B μ_W) | Cerrados — confirmado |

**Nota P6:** CKMGIT0528 y ckmloc0530 citan fourforums como 80pp. CKMGIT0602 cita 100pp. El valor 100pp corresponde a run_v8g con clave compuesta correcta. La corrección es real — el 80pp era de una versión con el bug de post_id.

**Nota P4:** el reencuadre en CKMGIT0602 ("W_mixta produce c(S) 13× mayor que W_pos") no contradice la parcialidad reportada en ckmloc0530 — captura el mismo resultado desde el ángulo de la ventaja relativa en lugar del ρ* interior.

---

## 3. Eje de código — bugs y correcciones

### 3.1 Bug crítico: mcp_adapter epsilon

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — `task_mode_exit()` no restaura epsilon; C2 permanentemente suspendido |
| ckmloc0530 | **Resuelto** — `_saved_epsilon` captura valor antes de modificar |
| CKMGIT0602 | Resuelto — sin mención específica (ya no es issue) |

**Impacto:** el bug hacía que tras la primera operación task_mode, el criterio de cohesión C2 quedara desactivado para siempre. Resolución quirúrgica (1 atributo de instancia).

### 3.2 Escala W + Δ_r

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — W∈[0,1] vs Δ_r∈[0,∞); después de pocas evaluaciones Δ_r domina W sin señal |
| ckmloc0530 | **Resuelto** — `_combine_W_Delta()` normaliza Δ_r por `mean(W_nonzero)` |
| CKMGIT0602 | Resuelto — mencionado como fortaleza del MonitorService |

### 3.3 NaN silencioso en analytics.py

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — nodo core-invariante (traza_inferencia 84%) produce NaN en corrcoef |
| ckmloc0530 | **Resuelto** — `np.nan_to_num(corr, nan=0.0)` |
| CKMGIT0602 | Resuelto — sin mención |

### 3.4 Recálculo k-core innecesario

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — k-core recalculado 500× por llamada a cascade_distribution() |
| ckmloc0530 | **Resuelto** — `core_list` extraído fuera del loop |
| CKMGIT0602 | Resuelto — sin mención |

### 3.5 Import tardío scipy

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — `from scipy import stats` dentro del cuerpo de función |
| ckmloc0530 | **Resuelto** — movido a nivel de módulo |
| CKMGIT0602 | Resuelto — sin mención |

### 3.6 Issues persistentes (sin resolver en los tres informes)

| Issue | Estado en CKMGIT0602 | Impacto |
|---|---|---|
| `cS()` en core.py: Python O(N²) vs vectorizado en monitor_service | Persiste | Menor — rendimiento |
| `optimal_density()` triple loop ~18M ops | Persiste | Menor para N≤64 |
| `_count_attractors()` sin cacheo | Persiste | Costo por evaluación |
| `evaluate()` con active_capabilities=None: estado residual | Persiste | Edge case sin flag |
| FabricationService _dev: versión experiments/ no migrada a services/ | Persiste | Divergencia _direction_score |
| `_direction_score` discrepancia entre versiones | Persiste | Lógica sin unificar |
| `corpus_state.json` sin versionado de schema | CKMGIT0602 lo menciona | Riesgo silencioso |

---

## 4. Eje teórico — conocimiento nuevo producido por sesión

### 4.1 CKMGIT0528 → ckmloc0530 (sesión loc0530)

**Cierre de HOLDINGs H1/H2/H3** — resultado central de mayor alcance.

Los tres HOLDINGs eran preguntas abiertas desde v25:
- H1: ¿α_c sigue siendo 0.138 con patrones correlacionados?
- H2: ¿por qué P4 se diluye en N=64?
- H3: ¿por qué μ_W no generaliza entre N?

La derivación de la estructura bimodal A/B (CV=0.944, razón max/min=102×) los cierra como tres observaciones de la misma función c(S)*(N,ρ_corr):
- μ_BB ≈ mean(fi·fj), ratio 1.025 — derivable analíticamente
- μ_AA no derivable — núcleo correlacionado, frecuencias marginales infladas mutuamente
- μ_W global depende de proporción A/B, no de N

Consecuencia operativa: medir μ_W empíricamente al inicio de sesión no es workaround — es el procedimiento correcto.

**Garantías G1/G2/G3** — operacionalización del monitor.

Sistema de tres zonas derivado empíricamente (N=32, n=500 secuencias). El ratio r = c(S)/μ_W como indicador en tiempo real reemplaza el threshold fijo hardcodeado. Gap discriminante G1/G2 detectable: [+0.001310, +0.001941].

**Falsificación H_STOP** — resultado negativamente informativo.

D_ckm(t_stop) no predice efectividad del operador STOP. Casos t=10 y t=20 con D_ckm=0.200 idéntico producen ratio_max diferente (1.250 vs 1.500). La hipótesis de monotonía queda falsada. Hipótesis reformulada: Efectividad_STOP = f(A_pre). α*≈0.4 robusto (5/9 casos).

**Convergencia IAP → COCO-thermostat** — cristalización conceptual.

Distinción operativa entre COCO-registry (almacena M declarado, se vuelve stale) y COCO-thermostat (β colectivo desde interacción real, no se vuelve stale). La fuente de la diferencia: Δ_bias (declaración) vs Δ_r (rechazo del campo).

**Tipos de Inferencia** — mapa preliminar, sin formalizar.

Cuatro nombres registrados: Generalización, Hysteresis Inference, Perspective Inference, Collective Inference. Forma no forzada — preservados para cuando las condiciones sean correctas.

**Modos Operacionales** — arquitectura de admisión formalizada.

```
first_time → accumulation → operational/standard
                                   └── task_mode (implementado)
                                   └── restricted (hipótesis)
```

C3_default = f(corpus_density): sospecha crece con madurez del campo, no con tiempo absoluto. Caso irreducible documentado.

### 4.2 ckmloc0530 → CKMGIT0602 (sesión loc → git actualizado)

**Validación fourforums con pipeline v8g correcto** — resultado empírico de mayor peso.

El bug de post_id (no global, reinicia por discussion) fue el obstáculo técnico central. Fix: clave compuesta (discussion_id, post_id). Impacto: posts mapeados de 468 → 35,966. Consecuencia directa: P6 colapso = 100pp (no 80pp), P7 confirmada con autor 204 (ratio 296×, out=0).

**P7 confirmada en segundo corpus independiente.**

Autor 204 (T0, ratio=296) es el equivalente estructural de autor 965 (CreateDebate, ratio=455). Diferencia notable: en fourforums hay sostenedores puros en AMBOS polos (T0 y T1). En CreateDebate el polo sostenedor era exclusivamente del polo sos_dom. La simetría del debate gun control en fourforums es mayor.

**Estructura A/B de μ_W confirmada** — HOLDINGs cerrados visibles en el repo.

CKMGIT0602 puede leer los REGs de cierre directamente. Lo que en ckmloc0530 era resultado de sesión, en CKMGIT0602 es parte del cuerpo de conocimiento accesible.

**Señal STOP, grados de pérdida** — extensión de la falsificación anterior.

La sesión que produjo v27 introduce la hipótesis de pérdida como función de D_ckm(t_stop) y T(W), con formulación: Perdida_STOP(t) = A(t_pre) − max_alpha[A(t_post)(alpha)]. Pendiente experimental: sweep D_ckm(t_stop) × alpha.

---

## 5. Gaps abiertos — estado en CKMGIT0602

| Gap | Origen | Prioridad declarada |
|---|---|---|
| W asimétrico en fourforums (mturk labels) | Consecuencia W simétrico actual | Alta — desbloquea C6c real |
| Verificación autor 204 contenido | P7 confirmada por ratio, no por contenido | Media |
| P7 en otros dominios (abortion, climate) | Generalización P7 | Media |
| Sweep D_ckm(t_stop) × alpha | H_STOP falsada, hipótesis revisada pendiente | Alta |
| μ_AA estructura interna núcleo | No derivable sin modelo del núcleo | Proyecto separado |
| COCO-thermostat prototipo | Hipótesis central sin implementar | Central |
| μ_W inicialización automática en CorpusService | Prerequisito operativo COCO | Alta |
| term_map N=64 reconstrucción | Bloquea W_base real N=64 | Técnico |
| G1/G2/G3 calibración para N≠32 | Garantías solo válidas para N=32 | Extensión |
| CorpusService compartido multi-agente | Spec sesión compartida | Arquitectural |
| Tipos de Inferencia formalización | Registrado — no forzar antes de tiempo | Emergente |

---

## 6. Trayectoria del proyecto — síntesis

**Código:** de 1 bug crítico + 4 issues identificados (CKMGIT0528) → código del modelo matemático central libre de bugs conocidos (ckmloc0530) → sin regresiones, issues restantes son de rendimiento/organización (CKMGIT0602).

**Teoría:** de 3 HOLDINGs activos + H_STOP no formulada (CKMGIT0528) → 3 HOLDINGs cerrados + H_STOP falsada + G1/G2/G3 operacionales (ckmloc0530) → estructura A/B integrada al cuerpo de conocimiento accesible + extensión STOP grados de pérdida (CKMGIT0602).

**Validación empírica:** de P6 con bug implícito en fourforums (80pp, post_id incorrecto) → P6 100pp con datos reales, P7 confirmada en segundo corpus, invariancia de estructura direccional entre corpora independientes verificada.

**Dirección emergente:** COCO-thermostat como siguiente capa. La distinción COCO-registry vs COCO-thermostat está cristalizada conceptualmente. El prerequisito operativo (μ_W automático en CorpusService) está identificado. La arquitectura de admisión por modos operacionales está formalizada.

Lo que el proyecto sabe que no sabe: μ_AA sin forma cerrada, α_c con núcleo correlacionado como propiedad del corpus no del modelo, G1/G2/G3 requieren re-calibración por dominio. Documentado explícitamente en los tres informes — no deuda técnica, frontera epistemológica reconocida.

---

*Clase R · Jun 2026 · Basado en tres informes técnicos de Claude Code.*
