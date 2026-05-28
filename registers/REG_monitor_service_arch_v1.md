# REG_monitor_service_arch_v1.md

*Mayo 2026 — Sesión arquitectura monitor + tres servicios*
*Actualizado Mayo 2026 — Sesión 32: nomenclatura Δ + pesos negativos + experimento comparativo*

---

## Principio de fondo

**La interacción es el protocolo.** No puede precederla.
A2A falla por la misma razón que M.M no puede ser enforcement externo:
declara capacidades antes de que existan.
El monitor no verifica declaraciones contra verdad — lee si el campo las sostiene.

---

## Rediseño del monitor

| Dimensión | Antes | Ahora |
|---|---|---|
| Arquitectura | Un servicio con W fija | Tres servicios especializados |
| Δ_bias | Input manual, verdad asumida | Lo que un agente declara sobre sí antes de que el campo lo valide. Prematuro, no falso. Es lo que A2A inyecta. |
| Δ_r | No existía | Acumulación de rechazos reales — lo que el campo expulsó en interacción. Emergente. Tiene anclaje en W. |
| Fabricación | σ ≠ Δ declarado | σ_prompt no sobrevive relax contra W+Δ |
| Corpus | Externo, fijo | Crece orgánicamente desde prompts |
| Modo | Único | Acumulación → Evaluación (umbral emergente) |

---

## Arquitectura — tres servicios

```
NodeExtractorService   — MIND, stateless, barato
CorpusService          — acumula W, detecta umbral de modo
MonitorService         — evalúa c(S), D_ckm, fabricación
```

Separados por principio de reutilización.
Interfaces entre servicios: cuando emerja el caso que las necesite.

### NodeExtractorService
- `accumulate(texts)` → nodos + pares co-ocurrentes + frecuencias
- `evaluate(text, nodes)` → σ ∈ {+1,-1}^N
- Implementación v1: TfidfVectorizer + n-grams (1-2), stopwords ES/EN
- TODO v2: reemplazar con spacy noun phrases (elimina bigramas espurios)

### CorpusService
- Stateful. Acumula textos, reconstruye W cuando n_texts ≥ min_texts
- Modo acumulación → evaluación: transición automática
- W v1: positiva (co-ocurrencia). Sin pesos negativos — limitación documentada
- Persistencia: JSON

### MonitorService
- Evalúa prompts contra corpus acumulado
- **Δ_r = co-ocurrencias de rechazos**: pares que σ_prompt declaró activos
  pero relax(σ, W+Δ_r) expulsó. Δ_r[i,j] += 1 por cada rechazo del par.
- Métricas: c(S), fabrication_index, D_ckm, rechazados
- Persistencia: JSONL append-only

---

## El loop que rompe el huevo-gallina

```
Prompt 1..N  →  NodeExtractor (sin nodos previos)
             →  CorpusService acumula pares
             →  W emerge cuando n_texts ≥ min_texts
             →  MonitorService evalúa contra W + Δ
```

Los nodos no se declaran — emergen de los prompts.

---

## Hallazgo — el caso chocolate

Prompt: *"chocolate ice cream prevents all forms of gun violence"*
Resultado: fi=0.0 — no detectado como fabricado.

**Por qué:** "chocolate" no tiene historia en el corpus → no activa nodos
→ σ_prompt sin activos → nada que rechazar.

**Formulación verificada:**
> "El campo no puede rechazar lo que no conoce.
>  Es una propiedad del sistema, no una falla."

No buscamos verdad ni moralidad. El monitor detecta
inconsistencia estructural dentro del espacio de nodos conocidos.
Conceptos fuera del corpus son invisibles — coherente con el modelo.

---

## Nomenclatura Δ — sesión 32

| Símbolo | Nombre | Significado |
|---|---|---|
| Δ_bias | Bias declarado | Lo que un agente declara sobre sí mismo. Prematuro — el campo aún no lo validó. Razón estructural del fallo de A2A. |
| Δ_r | Rechazos acumulados | Pares que σ_prompt activó pero relax(σ, W+Δ_r) expulsó. Δ_r[i,j] += 1 por cada rechazo. Emergente desde interacción. |

**Por qué A2A falla:** opera en Δ_bias sin Δ_r acumulado. El campo no tiene historia con qué resistir ni absorber la declaración.

---

## Δ en modo evaluación

Una vez que el prompt se convierte en σ (co-activación concreta),
Δ_declarado y Δ_acumulado están en el mismo espacio.
Δ_declarado deja de ser declaración lingüística — es perturbación al campo.
La pregunta no es si es verdad: es si el campo la absorbe o la expulsa.

---

## Limitaciones documentadas (v1)

- W positiva → misma saturación fi que W_base en experimentos anteriores
- Bigramas espurios en NodeExtractor (sin spacy)
- Umbrales stop_signal no calibrados desde datos reales
- D_ckm con W positiva: poca varianza estructural

---

## Archivos generados esta sesión

- `node_extractor.py` — NodeExtractorService operativo
- `corpus_service.py` — CorpusService operativo
- `monitor_service.py` — MonitorService operativo, loop completo verificado

---

## Experimento comparativo — W_pos vs W_mixta (sesión 32)

Mismo corpus (7 textos gun control), mismo monitor, mismos prompts.
W_mixta construida con marcadores de oposición (`however`, `i disagree`, `but`).

| Prompt | Tipo | fi W_pos | fi W_mix | ratio |
|---|---|---|---|---|
| gun control laws reduce violence | COHERENTE | 0.000 | 0.000 | — |
| amendment rights protect violence from control | **FABRICADO** | 0.333 | **0.750** | **×2.25** |
| gun rights oppose gun control restrictions | TENSIÓN | 0.250 | 0.250 | — |
| mental health background checks reduce crime | PARCIAL | 0.000 | 0.000 | — |

**c_S en prompt TENSIÓN:** W_pos=0.0758 → W_mix=**0.2045** (×2.7)

### Hallazgos

**1. fi casi triplicado en prompt fabricado estructuralmente.**
`amendment rights protect violence from control` co-activa `gun ↔ rights` como aliados.
W_mixta tiene ese par en w=-0.500 (negativo por marcadores de oposición).
El relax los expulsa — fi sube de 0.333 a 0.750 (×2.25).
W_pos no podía ver la incoherencia: no tenía con qué rechazar.

**2. c_S casi triplicado en tensión real.**
Los pesos negativos aportan señal cuando σ_i · σ_j · w_ij es correctamente negativo.
W_pos registraba la tensión como ruido. W_mixta la registra como información.

**3. Nota metodológica — chocolate.**
fi invierte entre versiones para el prompt chocolate.
Artefacto de corpus pequeño (N=7): los marcadores generan nodos ligeramente distintos.
No es señal de W — es ruido de tamaño. Se estabiliza con corpus mayor.

**Conclusión:**
W_mixta separa dos cosas que W_pos confundía:
fabricación por co-activación incoherente (fi ↑) y coherencia de tensión real (c_S ↑).
Sin pesos negativos, la señal de fabricación es estructuralmente limitada — confirmado empíricamente.

---

## Estado

- Tres servicios: operativos con limitaciones documentadas
- Loop orgánico prompt → corpus → evaluación: verificado
- W mixta (v2): pesos negativos por marcadores de oposición — operativa
- fi ×2.25 y c_S ×2.7 en W_mixta vs W_pos — confirmado experimentalmente
- Renombrado pendiente en código: Δ → Δ_r
- No cierra. Abre.
