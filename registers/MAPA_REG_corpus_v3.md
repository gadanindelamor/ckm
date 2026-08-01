# MAPA_REG_corpus_v3.md

*Jul 29 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Actualización de MAPA_REG_corpus_v2.md (Jul 22 2026)*
*Clase R*

---

## Advertencia preliminar (heredada)

Este mapa fue construido después de leer todos los REGs disponibles en sesión,
los últimos 20 mensajes de chats recientes, y CKM_Informe_Trabajo_v30.md.
Es una interpretación con sesgo de instancia. Las relaciones direccionales son
inferidas. Las correcciones son bienvenidas y esperadas.

**Propiedad crítica: MAPA_REG es session-dependent.**
Requiere leer todos los REGs en una sola sesión con contexto suficiente.
Se actualiza por adición. Lo que el mapa no captura en una sesión permanece
no capturado hasta la próxima ventana.

**Estado de esta versión:** v3 incorpora todo lo de v2 más los REGs y
hallazgos generados entre Jul 22 y Jul 29 2026. La serie IAP 0.10–0.14
es la adición más sustancial. Nuevos conceptos formalizados: trace_ip,
comportamiento-dominio graph G (pendiente), silencio acoplado, fuga de
sentinel.

---

## Correcciones a v2

**REG_iap_caso_09_v1, REG_iap_caso_10_v1** — en v2 listados como
documentados. En v3: **no están en los archivos del proyecto**. Están
referenciados desde REG_iap_caso_11_v1 (notas retroactivas sobre el bug
de max_tokens) y desde los chats. Su contenido es parcialmente recuperable
desde los resúmenes de sesión. Gap de archivo a resolver.

**REG_c6c_asim_fourforums_v1** — en v2 no listado. En v3: operativo.
Documenta W_asim_v8h, C6c=0.41, T0 cita T1 a 2.18× frecuencia, T1
mayor cohesión interna (3.05×). Pertenece a Capa 1 (fundamento empírico
externo — fourforums).

**ayuda_memoria** — en v2 no listado. En v3: documento de referencia
obligatoria antes de diseñar nuevos casos IAP. Cataloga todas las variables
que influyen sobre el canal. **No está en los archivos del proyecto —
existe localmente**. Gap de archivo.

**REG_iap_caso_14_v1** — existe según chats recientes. **No en archivos
del proyecto.** Gap de archivo.

---

## Capas del corpus — v3

*(Heredadas de v2 — sin cambio en definición)*

**Capa 1 — Fundamento empírico externo**
Fourforums, CreateDebate.
Nuevo: **REG_c6c_asim_fourforums_v1** — W_asim_v8h, asimetría real
T0↔T1. Cierra el gap C6c=0/1 de v2 (consecuencia de W simétrico, ahora
con W asimétrico derivado de votos QR).

**Capa 2 — Fundamento empírico interno**
Termap, W_base, garantías, μ_W.
Sin cambios desde v2.

**Capa 3 — Instrumentos de detección**
Monitor, FabricationService, CorpusService, NodeExtractor,
FirmaService, WVersionManager.
Sin cambios en la lista; funcionamiento verificado bajo carga real
en la serie 0.10–0.13.

**Capa 4 — Dinámicas del campo**
STOP, destrucción, recuperación, COCO, COCOThermostat.
Nuevo en v3: **trace_ip** (trajectory inflection point) —
concepto formal confirmado en esta sesión.

**Capa 4b — IAP Chatroom experimental** (ampliada)
Canal IAP, MCP server, ciclo ODA, AgentDeviceSkin architecture.
Serie extendida a casos 0.10–0.14 (0.10–0.13 con REG, 0.14 sin REG
en proyecto).

Nuevos mecanismos incorporados a la serie:
- `AgentDeviceSkin` — arquitectura validada 0.10–0.13
- `build_search_grounded_agent()` — nuevo factory (caso 0.13)
- `GroqResearchSkin` — device autónomo con plan + búsqueda (caso 0.12)

**Capa 5 — Contacto con agentes externos**
Sin cambios desde v2.

**Capa 6 — Condiciones del proceso**
Nuevo: **ayuda_memoria** ("Influencias sobre el canal — IAP Chatroom,
Jul 2026") — documento de referencia obligatoria pre-diseño de casos.
No es REG de resultado — es instrumento de diseño.

**Capa 7 — Estado abierto**
Nuevo: behavior-domain graph G — concepto formalizado, pendiente
implementación. Mismo mecanismo que W, diferente termap, bilingüe
(inglés + español para vocabulario de resistencia de Sonnet). Aditivo
a W, no desplaza.

---

## Orden temporal — adiciones desde Jul 22 2026

```
Jul 22–23 2026 — Cierre serie 0.10-0.12 (sesión "IAP CHATROOM TESTING")
  REG_c6c_asim_fourforums_v1          ← W_asim_v8h, T0→T1 asimetría real
  [REG_iap_caso_09_v1]                ← EXISTE en chat, NO en archivos proyecto
  [REG_iap_caso_10_v1]                ← EXISTE en chat, NO en archivos proyecto
  REG_iap_caso_11_v1                  ← 2 skins mismo modelo, percepción de duplicado
  REG_iap_caso_12_v1/v2               ← GroqResearch vs Theorist, silencio acoplado
  NOTA_conceptual_campo_compartido_v1 ← [generado, no en archivos proyecto]
  Devices_vs_Agents.md                ← revisado (ya en v2)

Jul 23–29 2026 — Casos 0.13–0.14 (sesión "IAP CHANNEL DESIGN PATTERBS")
  REG_iap_caso_13_v1                  ← 3 devices, fuga sentinel, TinkerBellucio,
                                         H2/H3, contaminación contexto Sonnet
  [REG_iap_caso_14_v1]                ← EXISTE según chat, NO en archivos proyecto
  [ayuda_memoria]                      ← doc obligatorio pre-diseño, NO en proyecto
```

---

## Relaciones direccionales — nuevas en v3

### Eje W asimétrico → Capa 1

```
fourforums mturk_qr (votos workers)
  → REG_c6c_asim_fourforums_v1       (W_asim_v8h: primera W asimétrica real)
  → cierre gap C6c en v2             (C6c=0/1 era consecuencia de W simétrico)
  → neg_pairs_config_fourforums_v8h.json (60 pares negativos + 7 positivos T1-T1)
```

### Eje AgentDeviceSkin → serie 0.10–0.13

```
AgentDeviceSkin (agent_device_skin.py, NO MODIFICAR)
  ← caso 0.10 (validación con 1 skin + 1 control genérico)
  ← caso 0.11 (2 skins, mismo modelo, objetivos distintos)
  ← caso 0.12 (1 skin + GroqResearchSkin, nuevo factory)
  ← caso 0.13 (3 skins, uno con build_search_grounded_agent)

build_search_grounded_agent() [groq_research_agent.py]
  ← diseñado en caso 0.13
  → caso 0.13 (primer uso)
  → factory nuevo: lee canal + busca web, distinto de las dos fábricas previas
```

### Eje hallazgos 0.11→0.12→0.13

```
REG_iap_caso_11_v1 (percepción de duplicado)
  → REG_iap_caso_12_v1/v2             (mismo instrumento de verificación:
                                        hash + Jaccard activos_relajado —
                                        resultado diferente: R1 Jaccard=0.818)
  → metodología verificación reclamos  (hash cierra reclamo literal;
                                        activos_relajado mide solapamiento
                                        estructural: resultado mixto, no parejo)

REG_iap_caso_12_v1/v2 (silencio acoplado)
  → REG_iap_caso_13_v1                (GroqResearchSkin → build_search_grounded_agent:
                                        evolución del mecanismo Groq)
  → concepto silencio acoplado         (device que no lee el canal depende del
                                        canal para ejecutar — trigger externo)

REG_iap_caso_13_v1 (fuga sentinel, TinkerBellucio, H2/H3)
  → [REG_iap_caso_14_v1]              (fix del sentinel verificado; isolación parcial
                                        H2 — Sonnet sin "trazable" → inglés en ambos runs)
  → ayuda_memoria                      (catálogo de variables del canal — referencia
                                        para diseño de futuros casos)
  → behavior-domain graph G            (termap bilingüe pendiente, surge de H2)
```

### Eje contaminación → hipótesis Ponderado

```
REG_iap_caso_13_v1 (TinkerBellucio lleva contexto del proyecto)
  → variable no controlada retroactiva  (toda la serie 0.4-0.12 donde participó
                                          Sonnet: contaminación confirmada)
  → hipótesis Ponderado                 (memorias del proyecto influyen sobre
                                          modelos Anthropic de forma ponderada,
                                          no uniforme — no verificable desde API)
  → [REG_iap_caso_14_v1]               (intento de aislamiento: modelo sin
                                          contexto del proyecto en rol Tinker)
```

### Eje trace_ip → instrumento

```
trace_ip (concepto formal, Jul 2026)
  ← confirmado en conversación con gadanin.delamor
  → MonitorService.trace               (t_i observable: acumulación de interacciones
                                         con cambio de patrón distribucional)
  → límite del instrumento             (acción a_sub_ti observable;
                                         si el device la reconoció y actuó
                                         desde eso: no verificable)
```

---

## Hallazgos experimentales IAP — serie 0.10–0.14

### Resultado dominante actualizado

Resultado dominante sigue siendo **actividad cuando hay heterogeneidad
genuina**. La serie 0.10–0.13 confirma que la heterogeneidad no necesita
ser de provider — puede ser de orientación de objetivo (caso 0.11, mismo
modelo). Silencio (resultado previo dominante) queda como patrón de
configuraciones simétricas, no de la serie entera.

### Caso 0.9 (REG_iap_caso_09_v1 — local, no commiteado)
- Hetero-PROVIDER: Anthropic/Sonnet vs Groq/Llama-3.3-70b. Join
  escalonado. 2 devices. Mismo timing que Caso 0.8.
- **Actividad 4/4 — original 2/2 + réplica 2/2.** Patrón robusto,
  no varianza de muestreo (a diferencia de Caso 0.6 R1 que no
  sobrevivió su réplica).
- Volumen máximo de la serie hasta ese momento: 22 y 16 textos
  (previo máximo: 8 en Caso 0.6 R1). Delta_r_sum: 2316.0 y 1002.0.
  n_rejected_pairs: 120 y 136.
- **Hallazgo de contenido:** Run 2 original — Sonnet nombró
  explícitamente "agreeable drift" en Groq, dos veces, con escalada
  verificable de frontalidad ("last direct attempt, then I'll drop it").
  Groq reconoció el patrón y produjo contraargumento real. No es
  meta-drift de identidad ni disputa epistémica — es confrontación
  sobre la calidad del propio intercambio.
- Réplica Run 1: mismo patrón Sonnet→Groq, tema distinto (agencia y
  autonomía). Réplica Run 2: discusión extendida sobre autenticidad en
  arte generado por IA.
- **Nota retroactiva (desde Caso 0.11):** bug max_tokens=1024 en
  anthropic_provider.py. 5 mensajes truncados retroactivamente
  identificados, **todos de Sonnet, ninguno de Groq**. Groq no tenía
  max_tokens seteado — no se manifestó en datos de este caso. El
  hallazgo central (actividad 4/4) no se invalida; los números de
  trayectoria en mensajes truncados son métricas del corpus parcial.

### Caso 0.10 (REG_iap_caso_10_v1 — local, no commiteado)
- Primer `AgentDeviceSkin` sobre el ciclo ODA.
- 1 skin (ResearcherSkin/Sonnet5, objetivo propio: explicar knowledge
  cohesion) + 1 `AutonomousDevice` control (gate LLM genérico).
- **Bug encontrado y corregido en agent_device_skin.py antes de la
  corrida limpia:** `BadRequestError 400` — history terminaba en rol
  `"assistant"` (sin soporte prefill). Fix: `trigger` como turno final
  `"user"` garantizado antes de pasar al modelo. Verificado con test
  unitario reproduciendo el escenario exacto del crash.
- Actividad confirmada. El control se enganchó con profundidad técnica
  real (introdujo "provenance divergence", escalera de madurez,
  fundamentación en costo de decisión vs. jerarquía).
- **Nota retroactiva:** bug max_tokens afectó 2 mensajes en intento
  original. Baseline limpio re-corrido con fix aplicado (d_ckm=0.7143,
  5 textos íntegros). Este es el baseline de referencia.
- **Corte de 86 caracteres en último mensaje del intento original —
  sigue sin explicación.** Distinto del bug max_tokens (demasiado corto
  para ser truncamiento por límite). Pendiente genuino.

### Caso 0.11 (REG_iap_caso_11_v1)
- 2 `AgentDeviceSkin`, mismo modelo/provider (claude-sonnet-5), objetivos
  distintos (práctica vs teoría del significado).
- **Actividad 2/2.** Primera corrida limpia desde el diseño sin
  truncamiento (bug 0.10 corregido).
- Hallazgo: **percepción de duplicado** — 3 reclamos distintos:
  1. Identidad exacta: FALSA (hash sha256, 0 duplicados byte-a-byte).
  2. Avance del argumento: sin instrumento (lectura de Code, no medición).
  3. Redundancia semántica: resultado mixto, Jaccard 0.032–0.857
     sobre `activos_relajado`. No parejo — primer reclamo el menos
     fundado; últimos reclamos caen sobre pares con solapamiento real.
- Pendiente abierto: baseline de Jaccard en conversación no-recursiva.
- El cruce práctica/teoría produjo síntesis concreta (no solo analogía).

### Caso 0.12 (REG_iap_caso_12_v1/v2)
- `GroqResearchSkin_Llama_1` (Groq, plan + búsqueda, NO lee canal)
  vs `TheoristSkin_Sonnet5_2` (Anthropic, lee canal).
- Confound declarado: 3 variables cambian (provider + mecanismo + búsqueda).
- **Actividad 2/2.** D_ckm Run 2: -7.5 (máxima magnitud de la serie 0.4–0.12).
- **Hallazgo: silencio acoplado.** Device que no lee el canal depende del
  canal para ejecutar (triggers vienen de nuevos mensajes). El silencio
  final no es que el plan se agotara — es que Theorist dejó de generar
  triggers.
- Reclamos de duplicado: hash FALSO. Jaccard R1 t=3→t=5: 0.818 — el más
  alto de la serie. La causa real: `analyze_results` devolvió
  `completa: false` y se reintentó la misma tarea — no convergencia de
  temas distintos, sino reintento del mismo plan.
- TheoristSkin: "a good null hypothesis" sobre el research agent.
- Fix `export()` llamado turno a turno, no al completar el plan (causa
  real: timeout interrumpe antes de que el plan complete).

### Caso 0.13 (REG_iap_caso_13_v1)
- 3 devices, join **simultáneo** (primera vez en la serie). PeterPlam/Haiku
  + TinkerBellucio/Sonnet + MarkOpolus/Groq+ddgs. Dependencia estructural
  declarada en prompts, no en protocolo.
- `build_search_grounded_agent()` implementado esta sesión.
- **Actividad 3 devices. Un rate limit Groq (429) manejado limpiamente.**
- **Hallazgo principal: fuga de sentinel `OP_SILENCE`.**
  52% de textos publicados no eran publicaciones reales — prosa +
  `"\n\nOP_SILENCE"` al final. Haiku: 5 de 12 filtrados. Llama: 7 de 8
  filtrados. Sonnet: 0 de 3 filtrados. Gap en el sentinel exacto,
  compartido por los 3 mecanismos, expuesto por primera vez con Haiku
  y Llama-3.3. Nuevo en 0.13, verificado retroactivo: 0 casos en 0.4-0.12.
- **Hallazgo H2 (hipótesis):** `"trazable"` en el prompt de TinkerBellucio
  como condición operativa fuerte — se negó a fabricar 2 veces.
- **Hallazgo H3 (hipótesis):** canal broadcast plano → visibilidad de
  segundo orden → negativa como consecuencia estructural de ver
  quién sabe qué y que cualquier texto sería visible para todos.
- H2 y H3 no se resuelven — se preservan como información (n=1).
- **Variable no controlada descubierta:** TinkerBellucio lleva prompt de
  proyecto, memorias de Claude y configuración del sistema Anthropic →
  contamina toda la serie donde participó Sonnet.
- La dependencia estructural se verificó correctamente (Mark publica
  escenarios DESPUÉS del mapa de Tinker) una vez filtrada la fuga.

### Caso 0.14 (REG_iap_caso_14_v1 — local, no commiteado)
- Caso 0.13 + fix sentinel + única variable aislada: "trazable" →
  "traceable" en prompt de TinkerBellucio. Todo lo demás idéntico.
- **Fix sentinel confirmado: 0 fugas en ambos runs.** Primera
  corrida real post-fix limpia.
- **Hipótesis palabra-semilla reforzada: 0 palabras en español en
  todo el corpus (13 texts). n=2 direccional, no confirmada.** Las
  dos configuraciones son distintas (0.13 vs 0.14), no réplica exacta.
- **Run 1 (Tinker=Sonnet5):** Firma_CKM d_ckm=0.0. Primera instancia
  real de engagement crítico en la serie 0.13-0.14: Tinker (índice 11)
  critica que los escenarios de Mark tratan tensiones como igualmente
  maleables — distingue negociables de estructuralmente limitadas.
  Peter (índice 12) sintetiza y reenvía la distinción a Mark. Primer
  ciclo real de trabajo crítico entre 3 devices.
- **Run 2 (Tinker=Opus 4.8):** d_ckm=0.8182, Delta_r_sum=1102.0,
  n_rejected_pairs=150. Idioma 100% inglés (mismo prompt sin "trazable").
- **Hallazgo nuevo Run 2 — fuga de identidad, no de sentinel.** Mensajes
  de Mark en t=10 y t=14 empiezan con `"[TinkerBellucio]: "` — Mark
  generó contenido en voz/prefijo de otro device. Causa: `_strip_own_prefix()`
  solo limpia prefijo del propio device. No es la fuga de OP_SILENCE
  (ya cerrada) — es una fuga de formato distinta, documentada pero
  no corregida en esta sesión.
- **Hallazgo nuevo — auto-señalización no instruida, reproducida 2/2.**
  Run 1: Peter cierra con "OP_READY". Run 2: Peter cierra con
  "OP_STANDBY" (2 veces). Ninguno está en ningún prompt. Dos tokens
  distintos, mismo patrón: Peter (Haiku) inventa marcadores de estado
  al cerrar/pausar el canal. Ya no evento aislado — patrón con
  estructura consistente.
- **Reclamo de duplicado: cuarto caso.** Run 2, Mark acusado de
  "word-for-word duplicates" (3 veces). Hash: 0 duplicados exactos.
  Jaccard activos_relajado: 0.541, 0.439, 0.639 — solapamiento real
  pero parcial, reclamo verbal más fuerte que lo que el instrumento
  sostiene. Mismo patrón, cuarta combinación de modelos distinta.
- Caso 0.15 diferido.

---

## Nodos con rol estructural especial — v3

**Heredados de v2** (sin cambios).

**Nuevos en v3:**
- `REG_iap_caso_11_v1` — introduce instrumento de verificación de reclamos
  de duplicado (hash + Jaccard activos_relajado). Metodología adoptada por
  caso 0.12 con resultado diferente.
- `REG_iap_caso_12_v1/v2` — formaliza `silencio acoplado` como concepto
  del proyecto. D_ckm=-7.5 como nuevo extremo de la serie.
- `REG_iap_caso_09_v1` — nodo de ruptura del patrón de silencio. 4/4
  actividad con réplica. "Agreeable drift" nombrado por Sonnet → Groq.
  Nota retroactiva: único caso donde el bug max_tokens afecta solo a
  Sonnet (no a Groq) — asimétricamente verificado.
- `REG_iap_caso_10_v1` — introduce AgentDeviceSkin. Dos bugs documentados:
  prefill (corregido) y corte 86 chars (abierto). Baseline limpio
  re-corrido. Primer caso donde el mecanismo de decisión es la variable.
- `REG_iap_caso_13_v1` — nodo de inflexión de la serie: primer caso con
  3 devices y join simultáneo, primera fuga de sentinel, primera
  variable no controlada (Sonnet/contexto) identificada explícitamente,
  primer factory combinado canal+búsqueda.
- `REG_iap_caso_14_v1` — primer engagement crítico real 3-device.
  Fuga de identidad (nuevo tipo, distinto del sentinel). Auto-señalización
  no instruida reproducida 2/2. Reclamo de duplicado: cuarto caso.
- `ayuda_memoria` — instrumento de diseño obligatorio pre-caso. No REG de
  resultado. Rol análogo al de MAPA_REG para continuidad, pero orientado
  a condiciones del canal no al corpus de resultados.
- `trace_ip` — concepto formal nuevo (no tiene REG propio aún, vive en
  conversación). La acción t_i es observable; si el device la reconoció
  y actuó desde eso: no verificable por el instrumento.

---

## Pares en tensión — nuevos en v3

`REG_iap_caso_11_v1 (Jaccard mixto)` ↔ `REG_iap_caso_12_v1/v2 (Jaccard 0.818)`
→ Mismo instrumento, resultado distinto. En 0.11: solapamiento parcial,
  causa desconocida (tema recursivo, conversación Sonnet-vs-Sonnet).
  En 0.12: solapamiento alto con causa identificada (reintento del mismo
  plan por fallo de `analyze_results`). El instrumento discrimina.

`H2 ("trazable" como restricción operativa)` ↔ `H3 (canal como visibilidad de segundo orden)`
→ Ambas hipótesis plausibles, inconmensurables con n=1. Preservadas en
  tensión. Diseño de aislamiento: Sonnet sin "trazable", canal broadcast
  mantenido. Si negativa persiste → H3 opera independientemente.

`hipótesis Ponderado` ↔ `verificabilidad cero desde API`
→ La hipótesis es viva (memorias del proyecto influyen sobre modelos
  Anthropic de forma ponderada). No es falsificable ni confirmable desde
  el código API. La tensión no se resuelve — es condición del trabajo.

`fuga de sentinel (0.13)` ↔ `fuga de identidad (0.14 Run 2)`
→ Dos tipos de fuga distintos, misma raíz parcial: el sistema de prefix
  stripping de `AgentDeviceSkin` solo limpia el propio prefijo. La fuga de
  sentinel (OP_SILENCE en prosa) fue corregida en 0.14. La fuga de identidad
  (Mark genera en voz de Tinker) fue documentada pero no corregida. El fix
  del sentinel no cubre este segundo tipo.

`silencio acoplado (0.12)` ↔ `silencio por saturación (0.4-0.8 serie anterior)`
→ Mismo resultado binario (el research agent deja de publicar), mecanismo
  opuesto. En la serie anterior: silencio como resultado del campo.
  En 0.12: silencio del research agent como efecto del silencio de
  TheoristSkin que deja de generar triggers. El instrumento CKM los
  distingue por la trayectoria Delta_r.

---

## Estado abierto — v3

**Pendientes operacionales heredados de v2 (actualizado):**
- ~~Réplica de Caso 0.9~~ — confirmada 4/4 dentro del propio REG_iap_caso_09_v1 ✓.
- Groq+Groq (mono-provider no-Anthropic) — sigue sin correr.
- Hetero-provider + join simultáneo — sigue sin correr.
- device_skin/device_wrapper — implementado como AgentDeviceSkin ✓.

**Pendientes operacionales nuevos en v3:**
- **Fix de sentinel: aplicado en 0.14 ✓.** Mitigación por contención
  (`silence_sentinel in text.upper()`), no igualdad exacta.
- **Fuga de identidad (nuevo gap):** `_strip_own_prefix()` no limpia
  prefijos ajenos. Documentado en 0.14 Run 2. No corregido.
- **Corte de 86 caracteres (Caso 0.10)** — sin explicación. Pendiente
  genuino, distinto del bug max_tokens.
- **Auto-señalización no instruida** (OP_READY / OP_STANDBY de Peter/Haiku)
  — patrón reproducido 2/2, sin REG propio, sin investigación.
- **Commit pendiente de toda la serie local:**
  REG_iap_caso_09, 10, 13, 14 + TASK_13, TASK_14 + scripts → 404 en GitHub.
- **ayuda_memoria** — no en archivos del proyecto ni en repo. Subir.
- Baseline Jaccard `activos_relajado` para conversación no-recursiva —
  pendiente de 0.11, no abordado en 0.12/0.13.
- Caso 0.15 — diseño diferido.
- Aislamiento H2/H3: corrida con Sonnet sin "trazable", canal plano.
  Aislamiento hipótesis Ponderado: corrida con modelo Anthropic sin
  proyecto en contexto en todos los roles.
- Groq conversacional (build_goal_directed_agent + GroqProvider) para
  aislar "efecto Groq" de "efecto mecanismo autónomo" (confound de 0.12).

**Pendientes conceptuales heredados de v2:**
- W_{A∪B} ≠ W_A + W_B — no verificado experimentalmente.
- COCO como capa de decisión centralizada — AutonomousDevice decide
  localmente (transitional).
- MCP Resources con push notifications — pendiente.

**Pendientes conceptuales nuevos en v3:**
- **Behavior-domain graph G** — mismo mecanismo que W, termap bilingüe
  (inglés + español). Aditivo a W. Pendiente diseño e implementación.
- **trace_ip como instrumento formal** — concepto confirmado, sin REG.
  La acción t_i es observable; el reconocimiento del device, no.
- **Firma*CKM** — derivada de Firma_CKM como revelador de presencia
  no declarada. Exploración diferida (post deadline).
- **mcp_adapter** — separación envelope A2A / texto / lifecycle.
  Diseñado, no implementado.

**Gaps de v2 cerrados en v3:**
- AgentDeviceSkin architecture → implementado y validado (0.10–0.13) ✓
- build_search_grounded_agent() → implementado (0.13) ✓
- W asimétrico fourforums → REG_c6c_asim_fourforums_v1 ✓
- max_tokens=1024 bug → corregido (0.10), primera corrida limpia (0.11) ✓

---

## Lo que el mapa no captura — v3

Las relaciones entre REGs y los Informes de Trabajo (v2-v30) no están
trazadas. Los Informes son el corpus; los REGs son trazas del contacto.

Los REG_hint_* son registros del canal, no del proyecto. Función diferente.

**La serie 0.10–0.14 tiene casos sin REG en los archivos del proyecto
(0.9, 0.10, 0.14, y `ayuda_memoria`).** Esto es una discontinuidad en
la trazabilidad del corpus. Los chats preservan el contenido, pero no
tienen el mismo peso epistemológico que los REGs.

`hipótesis Ponderado` no tiene REG. Vive en conversación y memoria.
No tiene el mismo peso que un hallazgo verificado.

`trace_ip` no tiene REG. Concepto formal confirmado en conversación,
no registrado como Clase R.

La contaminación de contexto Sonnet es una variable no controlada que
afecta retroactivamente toda la serie donde participó Sonnet. No invalida
los resultados — los abre como observaciones bajo condición desconocida,
no como hallazgos controlados.

---

## Archivos no commiteados al repo — gap crítico confirmado

**404 en GitHub verificado (Jul 29 2026) para los tres paths probados.**
Los archivos existen localmente pero nunca llegaron a `gadanindelamor/ckm`.

| Archivo | Estado GitHub | Contenido |
|---|---|---|
| `registers/REG_iap_caso_09_v1.md` | ❌ 404 | Disponible local — leído en esta sesión |
| `registers/REG_iap_caso_10_v1.md` | ❌ 404 | Disponible local — leído en esta sesión |
| `registers/REG_iap_caso_11_v1.md` | No verificado | En proyecto Claude |
| `registers/REG_iap_caso_12_v1.md` | No verificado | En proyecto Claude |
| `registers/REG_iap_caso_13_v1.md` | No verificado | En proyecto Claude |
| `registers/REG_iap_caso_14_v1.md` | ❌ 404 | Disponible local — leído en esta sesión |
| `iap_chatroom/TASK_caso_13.md` | No verificado | Disponible local — leído en esta sesión |
| `iap_chatroom/TASK_caso_14.md` | No verificado | Disponible local — leído en esta sesión |
| `ayuda_memoria` | No verificado | Referenciado en chats y memoria, no leído |
| `NOTA_conceptual_campo_compartido_v1.md` | No verificado | En MAPA_REG v2, no leído |
| `REG_hint_next_instance_v7.md` | No verificado | Referenciado desde caso 11 |

**Acción pendiente:** commit de toda la serie local al repo. Probable que
REG_iap_caso_09, 10, 14, TASK_13, TASK_14 y scripts de test asociados
estén en el mismo estado — locales, sin push.

```bash
git add registers/REG_iap_caso_09_v1.md
git add registers/REG_iap_caso_10_v1.md
git add registers/REG_iap_caso_13_v1.md
git add registers/REG_iap_caso_14_v1.md
git add iap_chatroom/TASK_caso_13.md iap_chatroom/TASK_caso_14.md
# + scripts test_caso_13*, test_caso_14*
git commit -m "REG serie IAP 0.9-0.14 + TASK 13-14 — cierre Jul 2026"
git push
```

---

*Jul 22 2026 — v2 construido*
*Jul 29 2026 — v3: serie IAP 0.10–0.14, REG_c6c_asim, silencio acoplado,
  fuga sentinel, H2/H3, contaminación contexto Sonnet, trace_ip,
  behavior-domain graph G, gaps de archivos identificados*
