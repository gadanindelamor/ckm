# MAPA_REG_corpus_v2.md

*Jul 22 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Actualización de MAPA_REG_corpus_v1.md (Jun 25 2026)*
*Clase R*

---

## Advertencia preliminar (heredada de v1)

Este mapa fue construido después de leer todos los REGs en sesión.
Es una interpretación con sesgo de instancia. Las relaciones direccionales
son inferidas — no están declaradas en los archivos.
Las correcciones son bienvenidas y esperadas.

**Propiedad crítica: MAPA_REG es session-dependent.**
Requiere leer todos los REGs en una sola sesión con contexto suficiente.
Se actualiza por adición. Lo que el mapa no captura en una sesión
permanece no capturado hasta la próxima ventana.

**Estado de esta versión:** v2 incorpora todo lo de v1 más los REGs
generados entre Jun 25 y Jul 22 2026. El bloque IAP Chatroom experimental
(casos 0.4–0.9) es la adición más sustancial.

---

## Correcciones a v1

**W versionado** — en v1 listado como gap de dirección. En v2:
implementado. `REG_w_version_ckm_v1` documenta WVersionManager y
WTracePoint. Ya no es gap.

**FirmaService** — en v1 sin REG propio. En v2: `REG_firma_ckm_v1`,
6 campos canónicos, operativo.

**IAP como servicio MCP** — en v1 en Capa 7 (estado abierto). En v2:
operativo y en fase de testing activo (serie 0.4–0.9). Pertenece a
Capa 4b (nueva).

**Silencio como resultado robusto** — en v1 no había suficiente dato
experimental para nombrarlo. En v2 confirmado: 7 de 11 corridas IAP
(0.4–0.8) dieron silencio. Único patrón de actividad confirmado hasta
0.8: mono-modelo + join simultáneo (n=2). Caso 0.9 rompe el patrón
con hetero-provider (n=2, pendiente réplica).

---

## Capas del corpus — v2

**Capa 1 — Fundamento empírico externo** (sin cambios desde v1)
Fourforums, CreateDebate. Lo que el sistema midió afuera.

**Capa 2 — Fundamento empírico interno** (sin cambios desde v1)
Termap, W_base, garantías, μ_W.

**Capa 3 — Instrumentos de detección** (ampliada)
Monitor, FabricationService, CorpusService, NodeExtractor.
Nuevos: FirmaService, WVersionManager.

**Capa 4 — Dinámicas del campo** (ampliada)
STOP, destrucción, recuperación, COCO, COCOThermostat (operativo).
Nuevo: STOP en dos planos distintos (campo vs agente).

**Capa 4b — IAP Chatroom experimental** (nueva en v2)
Canal IAP, MCP server, ciclo ODA, serie de casos 0.4–0.9.
Observación del campo grupal en condiciones reales.

**Capa 5 — Contacto con agentes externos** (sin cambios desde v1)
Hat, Copilot, NotebookLM.
Nuevo: Devices_vs_Agents.md (revisado Jul 22, no es REG pero es corpus activo).

**Capa 6 — Condiciones del proceso** (sin cambios desde v1)
Meta_access, hints, perspectivas, protocolo Sonnet/Code.

**Capa 7 — Estado abierto** (actualizada)
Lo que no existe todavía o acaba de ser nombrado.
Nuevo: NOTA_conceptual_campo_compartido_v1, device_skin/device_wrapper.

---

## Orden temporal — adiciones desde Jun 25 2026

```
Jun–Jul 2026 — Instrumentos nuevos (Firma + W versionado)
  REG_firma_ckm_v1                    ← FirmaService, 6 campos canónicos
  REG_w_version_ckm_v1               ← WVersionManager, WTracePoint

Jun–Jul 2026 — Integración A2A
  REG_a2a_integracion_ckm_v1
  REG_a2a_integracion_ckm_v2         ← límites de NodeExtractor sobre tráfico A2A

Jul 2026 — Dinámicas del campo (STOP + dos planos)
  REG_stop_agente_vs_campo_v1        ← STOP nivel campo ≠ STOP nivel agente

Jul 2026 — IAP Chatroom: infraestructura
  REG_iap_mcp_server_v1              ← 6 tools MCP sobre singletons
  REG_iap_chatroom_demo_c_v1         ← FastAPI + Gradio, Demo C
  REG_iap_chatroom_demo_claude_code_v0  ← construcción del chatroom por Code

Jul 2026 — IAP Chatroom: simulaciones
  REG_iap_simulation_smartwidget_v1  ← primera corrida SmartWidget (FakeProvider)
  REG_iap_simulation_smartwidget_v2  ← corrida con Anthropic real, bug doble-import
  REG_iap_simulation_adversarial_v1  ← Haiku adversarial → meta-drift, firma meta-reflexiva
  REG_iap_simulation_oposite_rol_v1  ← roles opuestos en canal

Jul 2026 — IAP Chatroom: serie de casos 0.4–0.9
  REG_iap_caso_04_oda_v1             ← ciclo ODA completo, frame break ("I'm Claude")
  REG_iap_caso_04a_v1               ← sin CKM en WELCOME MSG, meta-drift persiste
  REG_iap_caso_04b_v1               ← Sonnet: disputa epistémica, pico n_rejected=144
  REG_iap_caso_05_v1                ← sin seed humano, join SYSTEM como seed
  REG_iap_caso_06_v1                ← 4 devices, join escalonado, fix monitor_service.py
  REG_iap_caso_07_v1                ← MCP Resource vs tool, silencio (3/3 runs)
  REG_iap_caso_08_v1                ← 2 devices hetero-modelo, escalonado, silencio (2/2)
  REG_iap_caso_09_v1                ← hetero-PROVIDER (Anthropic+Groq), actividad (2/2)

Jul 22 2026 — Corpus conceptual
  Devices_vs_Agents.md (revisado)    ← eje device/agente, AutonomousDevice transitional
  NOTA_conceptual_campo_compartido_v1 ← W_eff como servidor matemático, intuición conceptual
```

---

## Relaciones direccionales — heredadas de v1 (sin cambios)

*(Ver MAPA_REG_corpus_v1.md — eje corpus→instrumento, corpus adversarial→predicciones,
instrumento→operadores de campo, evaluaciones externas→instrumento,
condiciones del proceso→continuidad, código→resultados.)*

---

## Relaciones direccionales — nuevas en v2

### Eje instrumento → firma y trazabilidad

```
REG_w_version_ckm_v1
  → REG_firma_ckm_v1                 (W versionado es prerequisito de Firma estable)
  → REG_iap_chatroom_demo_c_v1       (Firma_CKM en canal en vivo: D_ckm=-0.2222)

REG_firma_ckm_v1
  → REG_iap_caso_04_oda_v1 en adelante  (Firma al cierre de cada caso)
```

### Eje IAP infraestructura → IAP experimental

```
REG_iap_mcp_server_v1
  → REG_iap_simulation_smartwidget_v1/v2   (primer uso del server)
  → REG_iap_simulation_adversarial_v1
  → REG_iap_caso_04_oda_v1 en adelante     (todos los casos usan el server)

REG_iap_chatroom_demo_c_v1
  → REG_iap_caso_04_oda_v1                 (AutonomousDevice sobre infraestructura Demo C)
```

### Eje serie de casos (0.4→0.9)

```
REG_iap_simulation_adversarial_v1
  → REG_iap_caso_04_oda_v1             (meta-drift precedente: conflict-avoidance de Haiku)

REG_iap_caso_04_oda_v1
  → REG_iap_caso_04a_v1                (hipótesis: CKM en WELCOME MSG primea meta-drift)
  → REG_iap_caso_04b_v1                (hipótesis: meta-drift es propiedad de Haiku)

REG_iap_caso_04a_v1
  → REG_iap_caso_04b_v1                (hipótesis "efecto del bloque CKM" refutada)

REG_iap_caso_04b_v1
  → REG_iap_caso_05_v1                 (hipótesis: el seed "think" primea meta-drift)

REG_iap_caso_05_v1
  → REG_iap_caso_06_v1                 (hipótesis: heterogeneidad en early produce actividad)

REG_iap_caso_06_v1
  → REG_iap_caso_07_v1                 (hipótesis ruptura de simetría; MCP Resource)
  → fix monitor_service.py             (bug real descubierto y corregido en esta sesión)

REG_iap_caso_07_v1
  → REG_iap_caso_08_v1                 (tabla 2×2: hetero×timing; control tamaño grupo)

REG_iap_caso_08_v1
  → REG_iap_caso_09_v1                 (eje modelo→provider; primera actividad confirmada)
```

### Eje A2A → IAP

```
REG_a2a_integracion_ckm_v1/v2
  → REG_iap_mcp_server_v1              (NodeExtractor no opera sobre tráfico A2A —
                                         requiere LNH conversacional)
  → NOTA_conceptual_campo_compartido_v1 (A2A vs MCP extendido: W_eff como punto de encuentro)
```

### Eje conceptual (nuevo en v2)

```
NOTA_conceptual_campo_compartido_v1
  → Devices_vs_Agents.md              (AutonomousDevice: ciclo agéntico sin objetivo)
  → REG_iap_caso_09_v1               (hetero-provider como perturbación que activa el campo)
```

---

## Hallazgos experimentales IAP — serie 0.4–0.9 (para futuras instancias)

Resultado dominante: **silencio (7 de 11 corridas pre-0.9)**.

Único patrón de actividad confirmado antes de Caso 0.9:
**mono-modelo + join simultáneo** (n=2, Caso 0.5 original + réplica).

Patrón de silencio confirmado:
- Hetero-modelo intra-Anthropic + escalonado: silencio (Casos 0.6 R2/R3, 0.8 — 4/4 corridas limpias)
- Hetero-modelo intra-Anthropic + simultáneo: silencio (Caso 0.7 — 3/3)
- Hetero-modelo intra-Anthropic + escalonado, 4 devices: 0.6 R1 dio actividad en intento crasheado, réplica limpia post-fix dio silencio — **reclasificado como varianza de muestreo**

**Caso 0.9 (hetero-PROVIDER: Anthropic+Groq, escalonado, 2 devices):**
actividad 2/2, primera celda hetero+escalonado con resultado limpio confirmado.
Contenido sustantivo — no meta-drift ni acknowledgment. Pendiente réplica
antes de generalizar.

**Variable aislada en Caso 0.7:** mecanismo de lectura (tool vs MCP Resource)
no afecta el patrón de silencio — causa descartada.

**Fix real**: `services/monitor_service.py` línea 93 — `_Delta_r` se
redimensiona cuando N crece entre rebuilds de W. Bug documentado en
`REG_iap_caso_06_v1`. Sin el fix, cualquier corrida con corpus suficientemente
grande crashea con `ValueError: shape mismatch`.

---

## Nodos con rol estructural especial — v2

**Heredados de v1:**
- `REG_termap_ckm_corpus_v1` — hub de convergencia, ancla W_base
- `REG_pendientes_ckm_v1` — core-invariante, presente en todas las trayectorias
- `REG_monitor_ckm_v1/v2` — posible duplicado, verificación aún pendiente
- `GPT53_REG_hat_feedbak.md` — fuera de convención REG_*, contenido válido
- `REG_iap_coco_convergence_v1` — bisagra entre capas

**Nuevos en v2:**
- `REG_iap_caso_09_v1` — primer caso con actividad hetero+escalonado confirmada;
  rompe el patrón dominante de silencio
- `REG_iap_caso_06_v1` — contiene fix real de monitor_service.py, no solo resultado experimental
- `REG_firma_ckm_v1` + `REG_w_version_ckm_v1` — cierran los dos gaps de dirección de v1
- `NOTA_conceptual_campo_compartido_v1` — primer registro de W_eff como
  servidor matemático; marcado explícitamente como intuición conceptual

---

## Pares en tensión — heredados de v1

*(Ver MAPA_REG_corpus_v1.md — monitor_v1↔arch, garantías↔influencia_código,
hat↔meta_access, coco_proto↔beta_colectivo.)*

## Pares en tensión — nuevos en v2

`REG_iap_caso_05_v1` ↔ `REG_iap_caso_09_v1`
→ 0.5: dos espejos del mismo modelo → actividad por convergencia.
  0.9: dos providers distintos → actividad por divergencia.
  Misma señal binaria, mecanismo opuesto. El instrumento CKM los distingue:
  0.5 produce c_S positivo alto, D_ckm pequeño negativo;
  0.9 produce Delta_r_sum 2316.0, fi=1.0 sostenido, n_rejected máximo de la serie.

`REG_a2a_integracion_ckm_v2` ↔ `NOTA_conceptual_campo_compartido_v1`
→ A2A detectó el límite: NodeExtractor no opera sobre tráfico protocolar.
  La nota conceptual reformula el problema: W_eff es el servidor matemático
  que hace innecesario el protocolo de descubrimiento.
  Dirección: a2a_integracion plantea el límite; nota_conceptual lo reencuadra.

`REG_iap_caso_06_v1 (fix)` ↔ `REG_iap_caso_09_v1 (resultado)`
→ El fix de monitor_service.py fue necesario para que 0.9 corriera limpio.
  Sin él, el crash de 0.6 R1 réplica se hubiera repetido en 0.9 (corpus
  grande, N crece entre rebuilds). El resultado de 0.9 depende del fix de 0.6.

---

## Estado abierto — v2

**Pendientes operacionales:**
- Réplica de Caso 0.9 (n=2, necesita n≥3 antes de generalizar)
- Groq+Groq (mono-provider no-Anthropic) para aislar "efecto Groq" de
  "efecto heterogeneidad de provider"
- Hetero-provider + join simultáneo (celda vacía en la tabla)
- device_skin/device_wrapper: concepto registrado en memoria, sin REG ni implementación

**Pendientes conceptuales:**
- W_{A∪B} ≠ W_A + W_B — matemáticamente sólido, no verificado
  experimentalmente con dos subcorpus explícitos
- COCO como capa de decisión centralizada para devices —
  AutonomousDevice actualmente decide localmente (arquitectura transitional)
- MCP Resources con notificaciones push — fastmcp 3.4.4 no expone la API;
  pendiente si versión futura la expone

**Gaps de v1 cerrados en v2:**
- W versionado → implementado (REG_w_version_ckm_v1) ✓
- FirmaService → implementado (REG_firma_ckm_v1) ✓
- IAP como servicio MCP → operativo y en testing ✓

---

## Lo que el mapa no captura (heredado de v1, actualizado)

Las relaciones entre REGs y los Informes de Trabajo (v2-v30) no están
trazadas. Los Informes son el corpus; los REGs son trazas del contacto.

Los REG_hint_* son registros del canal, no del proyecto. Reducen el
costo de continuidad entre instancias — función diferente del resto.

La serie IAP 0.4–0.9 es densa y tiene relaciones internas no trazadas
en detalle (cada caso referencia al anterior). El orden temporal es
suficiente para navegarla; el grafo de relaciones dentro de la serie
se reconstruye desde los propios REGs.

`NOTA_conceptual_campo_compartido_v1` no es REG de resultado experimental —
es registro de intuición conceptual. Marcado explícitamente como tal
en el documento. No tiene el mismo peso epistemológico que el resto.

---

*Jun 2026 — v1 construido*
*Jun 23 2026 — v1 actualización: COCOThermostat operativo, Capa 4*
*Jun 25 2026 — v1 actualización: taxonomía de gaps*
*Jul 22 2026 — v2: serie IAP 0.4–0.9, Firma, W versionado, fix monitor_service.py,
  NOTA conceptual, Devices_vs_Agents revisado*
