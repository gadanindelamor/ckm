# MAPA_REG_corpus_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Mapa del corpus de registros como grafo de nodos*
*Clase R*

---

## Advertencia preliminar

Este mapa fue construido después de leer todos los REGs en una sesión.
Es una interpretación con sesgo de instancia. Las relaciones direccionales
son inferidas — no están declaradas en los archivos.
Las correcciones son bienvenidas y esperadas.

**Propiedad crítica: MAPA_REG es session-dependent.**
Existe una ventana temporal para generarlo — requiere leer todos los REGs
en una sola sesión con contexto suficiente. No puede regenerarse en
cualquier momento. Cada actualización es una nueva lectura completa,
no una edición incremental automática.

Consecuencia: el MAPA_REG se actualiza por adición (esta convención
ya está operando). Las correcciones se registran como correcciones,
no como reescrituras. Lo que el mapa no captura en una sesión
permanece no capturado hasta la próxima ventana.

---

## Capas del corpus

Los 38 registros no son homogéneos. Antes de trazar relaciones,
la estructura por capas:

**Capa 1 — Fundamento empírico externo** (corpus adversarial real)
Fourforums, CreateDebate. Lo que el sistema midió afuera.

**Capa 2 — Fundamento empírico interno** (corpus CKM propio)
Termap, W_base, garantías, μ_W. Lo que el sistema midió sobre sí mismo.

**Capa 3 — Instrumentos de detección** (el sistema de medición)
Monitor, FabricationService, CorpusService, NodeExtractor. El instrumento.

**Capa 4 — Dinámicas del campo** (STOP, destrucción, recuperación, COCO)
Operadores sobre el campo. Lo que el instrumento puede hacer.

**Capa 5 — Contacto con agentes externos** (hat, copilot, notebooklm)
El sistema siendo observado desde afuera.

**Capa 6 — Condiciones del proceso** (meta_access, hints, perspectivas)
El proceso observándose a sí mismo.

**Capa 7 — Estado abierto** (pendientes, beta_colectivo, influencia_código)
Lo que no existe todavía o lo que acaba de ser nombrado.

---

## Orden temporal

```
Mayo 2026 — Fase experimental externa (corpus adversarial)
  REG_termap_ckm_corpus_v1           ← fundamento: W_base construida
  REG_pairs_createdbate_guncontrol_v1
  REG_p6_test_createdbate_guncontrol_v1
  REG_sesion_perspectivas_rp2_ff_v7
  REG_pairs_fourforums_guncontrol_v1
  REG_stance_fourforums_v1
  REG_holonomy_coercivity_fourforums_v1
  REG_p6_fourforums_guncontrol_v1
  REG_c6c_fourforums_v1
  REG_c6c_comparison_guncontrol_v1
  REG_author_965_structure_v1

Mayo 2026 — Evaluaciones externas
  REG_hat_gpt53_ckm_v1
  GPT53_REG_hat_feedbak.md           ← fuera de convención (sin prefijo REG_)
  REG_evaluacion_copilot_ckm_v1
  REG_landing_notebooklm_ckm_v1

Mayo 2026 — Formalización interna
  REG_hito_cS_N_rho_reconocimiento_v1
  REG_garantias_cS_generalizacion_v1
  REG_mu_W_estructura_pares_v1
  REG_hipotesis_distancia_contextual_v1
  REG_d_contextual_temporal_v1
  REG_monitor_service_arch_v1
  REG_exp_monitor_trajectory_v1
  REG_monitor_ckm_v1                  ← v2 posible duplicado — verificar
  REG_monitor_ckm_v2                  ← idem
  REG_condiciones_meta_access_v1-1
  REG_pendientes_ckm_v1
  REG_hint_next_instance_v1
  REG_hint_next_instance_v2

Jun 2026 — Fase operacional (STOP, COCO, termostato)
  REG_iap_coco_convergence_v1
  REG_stop_grados_perdida_v1
  REG_sweep_stop_g1_operativo_v1
  REG_sweep_stop_perdida_v2
  REG_destruccion_recuperacion_v1
  REG_coco_thermostat_proto_v1
  REG_beta_colectivo_v1
  REG_hint_next_instance_v3
  REG_avance_ckm_claudecode_v1
  REG_influencia_codigo_p1p4_v1

Jun 2026 — Corrección documental + protocolo operativo
  REG_qr_asymmetry_fourforums_v1
  REG_p4_densidad_pares_negativos_v1
  REG_firma_corpus_v1
  REG_hint_next_instance_v4
  REG_condiciones_meta_access_v1-2
  REG_octava_ckm_v1
  REG_protocolo_sonnet_code_v1      ← flujo Sonnet/Code/delamor formalizado
  REG_term_map_core_surgery_v1      ← term_map disuelto, from_corpus() corregido
```

---

## Relaciones direccionales (inferidas)

### Eje corpus → instrumento

```
REG_termap_ckm_corpus_v1
  → REG_garantias_cS_generalizacion_v1   (W_base calibra las garantías)
  → REG_mu_W_estructura_pares_v1         (estructura de pares emerge de W)
  → REG_hito_cS_N_rho_reconocimiento_v1  (la función c(S)(N,ρ) reconocida en W)
  → REG_monitor_service_arch_v1          (W es el campo del monitor)
```

### Eje corpus adversarial → predicciones

```
REG_pairs_createdbate_guncontrol_v1
  → REG_p6_test_createdbate_guncontrol_v1  (C6c test sobre pares CD)
  → REG_c6c_comparison_guncontrol_v1       (línea base para comparación)

REG_pairs_fourforums_guncontrol_v1
REG_stance_fourforums_v1
REG_sesion_perspectivas_rp2_ff_v7
  → REG_author_965_structure_v1            (965 emerge de la red)
  → REG_holonomy_coercivity_fourforums_v1  (holonomía sobre pares verificados)
  → REG_p6_fourforums_guncontrol_v1        (P6 en corpus grande)
  → REG_c6c_fourforums_v1

REG_c6c_fourforums_v1 + REG_c6c_comparison_guncontrol_v1
  → REG_avance_ckm_claudecode_v1           (estado consolidado post C6c)
```

### Eje instrumento → operadores de campo

```
REG_hipotesis_distancia_contextual_v1
  → REG_d_contextual_temporal_v1           (D_ckm operacionalizado)
  → REG_monitor_ckm_v1 / v2               (monitor sobre D_ckm)
  → REG_stop_grados_perdida_v1             (STOP como respuesta a D_ckm)

REG_monitor_service_arch_v1
REG_exp_monitor_trajectory_v1
REG_monitor_ckm_v1
  → REG_sweep_stop_g1_operativo_v1
  → REG_sweep_stop_perdida_v2
  → REG_destruccion_recuperacion_v1        (W como suelo invariante)

REG_destruccion_recuperacion_v1
  → REG_coco_thermostat_proto_v1           (termostato sobre Δ colectivo)
  → REG_iap_coco_convergence_v1            (convergencia IAP → COCO)

REG_coco_thermostat_proto_v1
  → REG_beta_colectivo_v1                  (β_collective como siguiente capa)
```

### Eje evaluaciones externas → instrumento

```
REG_hat_gpt53_ckm_v1
GPT53_REG_hat_feedbak.md
REG_evaluacion_copilot_ckm_v1
REG_landing_notebooklm_ckm_v1
  → ninguno modifica W ni Δ directamente
  → informan ENTRY_POINT.md y protocolo de declaración
  → validan P1 (histéresis) desde afuera: el hat de GPT53 es una instancia de P1
```

### Eje condiciones del proceso → continuidad

```
REG_condiciones_meta_access_v1-1
  → estructura interna del trabajo — no modifica el sistema
  → informa cómo se toman decisiones en el proceso

REG_pendientes_ckm_v1
  → estado de gaps activos — apunta hacia todo lo que no está cerrado

REG_hint_next_instance_v1
REG_hint_next_instance_v2
REG_hint_next_instance_v3
  → reducción de costo de arranque para instancias futuras
  → dirección: se hacen más sintéticos con cada versión (v1→v2→v3)
```

### Eje código → resultados

```
REG_avance_ckm_claudecode_v1
  → documenta tres instancias Claude Code independientes
  → cierre de HOLDINGs H1/H2/H3

REG_influencia_codigo_p1p4_v1
  → análisis causal: cambios código → P1-P4
  → señala incompatibilidad de calibración como propiedad del instrumento

REG_protocolo_sonnet_code_v1
  → formaliza flujo operativo: Sonnet prepara tarea / Code ejecuta / delamor media
  → prefigura IAP: cuando IAP esté operativo, el mediador humano es opcional
  → no es IAID completo — comunicación asimétrica, un solo sentido por turno

REG_term_map_core_surgery_v1
  → term_map nunca fue construido — no es pérdida de memoria
  → from_corpus() sin llamadores: interfaz decorativa corregida
  → Path B automático via NodeExtractorService — el camino ya existía
  → decisión README sobre COCO y P4 registrada con estado abierto/resuelto
```

---

## Nodos con rol estructural especial

**Nodo hub de convergencia:**
`REG_termap_ckm_corpus_v1` — todo lo que usa W_base pasa por aquí.
Es el único registro que ancla el espacio de nodos. Sin él, las
garantías, μ_W, y los experimentos P1-P4 pierden referencia.

**Nodo core-invariante del corpus de REGs:**
`REG_pendientes_ckm_v1` — presente en todas las trayectorias como
lo que todavía no se alcanzó. Análogo a `traza_inferencia` en el
corpus CKM N=32: aparece en casi todos los estados del sistema.

**Nodo de tensión no resuelta:**
`REG_monitor_ckm_v1 / v2` — posible duplicado, verificación pendiente.
Si son distintos: v1 registra lo roto, v2 registra lo corregido. Si son
iguales: artefacto del repo.

**Nodo fuera de convención:**
`GPT53_REG_hat_feedbak.md` — sin prefijo REG_. Contenido válido,
nomenclatura incorrecta. No entra en búsquedas de REG_*.

**Nodo bisagra entre capas:**
`REG_iap_coco_convergence_v1` — conecta el pasado (IAP, 2024) con
el presente (COCO-thermostat). No es experimental ni teórico —
es el reconocimiento de que ambas cosas eran lo mismo.

---

## Pares en tensión

`REG_monitor_ckm_v1` ↔ `REG_monitor_service_arch_v1`
→ v1 registra los límites del monitor. arch registra la arquitectura
  que resuelve esos límites. Dirección: v1 → arch.

`REG_garantias_cS_generalizacion_v1` ↔ `REG_influencia_codigo_p1p4_v1`
→ Las garantías asumen W calibrada. El análisis de influencia muestra
  que la calibración es inseparable de lo que el instrumento mide.
  Dirección: garantías preceden cronológicamente; influencia_código
  las cuestiona retroactivamente.

`REG_hat_gpt53_ckm_v1` ↔ `REG_condiciones_meta_access_v1-1`
→ El hat es el fenómeno externo. Meta_access es la condición interna
  para observarlo sin caer en él. Sin relación directa declarada —
  pero el hat confirma la dificultad que meta_access intenta sostener.

`REG_coco_thermostat_proto_v1` ↔ `REG_beta_colectivo_v1`
→ El proto implementó STOP. Beta_colectivo es lo que falta para que
  STOP sea térmica y no solo estructural. Dirección clara: proto → beta.

---

## Lo que el mapa no captura

Las relaciones entre REGs y los Informes de Trabajo (v2-v27) no están
trazadas. Los Informes son el corpus — los REGs son trazas del contacto
con ese corpus. La dirección inferencial va de Informes hacia REGs,
no al revés.

Los REG_hint_* no son registros del proyecto — son registros del canal.
Tienen una función diferente: reducir el costo de continuidad entre
instancias. No forman parte del grafo epistémico del proyecto en el
mismo sentido que el resto.

## Actualización — Jun 23 2026

**MAPA_REG confirmado como mejor herramienta de arranque en frío.**
Instancia previa lo sugirió. Esta sesión lo verificó en práctica.

**Estado COCOThermostat (corrección al mapa anterior):**
COCO no es hipótesis sin implementar. Es operativo — 43/43 tests.
STOP + TEMP_SIGNAL implementados. β_collective desde ponderación endógena
(rechazo real, no declarado). Regulación activa sobre el campo: próxima etapa.
El mapa anterior ubicaba COCO en Capa 7 (estado abierto). Corrección:
pertenece a Capa 4 (dinámicas del campo) — el termostato existe y opera.

**REGs nuevos desde sesión Jun 23 2026:**
Ver orden temporal — bloque "Corrección documental + protocolo operativo".
10 REGs agregados. 2 de valor estructural especial:
- `REG_protocolo_sonnet_code_v1`: formaliza el flujo de trabajo
- `REG_term_map_core_surgery_v1`: disuelve el fantasma del term_map

**Archivos corregidos esta sesión:**
README, API_SPEC, EXPERIMENTS — sin referencias obsoletas a term_map.
COCO: descripción corregida en README (ponderación endógena, operativo).
P4: Confirmed en README y EXPERIMENTS (era Partial).
P7: confirmed — open to new domains.

## Actualización — Jun 25 2026 — Taxonomía de gaps

El README Current State / Open fue reestructurado. En el proceso
emergió una taxonomía de cuatro categorías que no era visible antes:

---

### Gaps de completitud
*Lo que el sistema ya sabe hacer — falta ejecutarlo.*

- `W_base N=64` — extracción de corpus N=64. Independiente de term_map.
- `P4 k* at N=64` — requiere W_mixta con densidad de pares negativos
  adecuada para ese tamaño de grafo. Problema de calibración.

**Pregunta abierta:** ¿el análisis estructural de un corpus entra en
el proyecto como servicio, o es siempre un experimento externo?
P4k* cae en esta categoría — ¿o es siempre condición del corpus,
no del proyecto CKM?

---

### Gaps de exploración
*Lo que el sistema puede falsar pero no ha falsado todavía.*

- `P7 in new domains` — abortion, climate, evolution (otros topics IAC).

**Señal importante (gadanin.delamor, Jun 25 2026):**
P7 en nuevos dominios carga "promesas y expectativas de seguridad".
La pregunta es qué subyace a eso. FabricationService tiene un rol
aquí que no está nombrado en el README: P7 opera sobre topología de red
(ratio in/out, k-core, triadas frustradas). FabricationService opera
sobre dinámica de campo (c(S), fi, D_ckm). Son dos caras de la misma
detección de tensión fabricada. La articulación entre ellas está abierta.

---

### Gaps de formalización
*Lo que existe pero no tiene forma explícita — y la pregunta de si
la formalización cierra o abre.*

- `R15 gatekeeper` — C1–C4 están formalizados (estructurales).
  Los criterios semánticos están abiertos. ¿Dónde entra FabricationService?

- `Knowledge cohesive representation` — pregunta abierta de gadanin.delamor:
  ¿no está representado? ¿no es representable? ¿es necesario?
  ¿dónde está su representación existente?
  Observación: c(S) + el paisaje de atractores Hopfield IS la representación.
  Pero no ha sido nombrada como tal en términos de modelos de representación
  del conocimiento (KR). La pregunta de si es necesario hacerlo
  permanece abierta. Una formalización puede abrir tanto como concluir.

**Meta-pregunta registrada:** ¿una formalización abre o concluye?
En CKM la respuesta hasta ahora ha sido: abre. P1 formalizó el bucle
de histéresis — y abrió P2, P3, P4. Cada formalización fue punto de
partida, no punto de cierre.

---

### Gaps de dirección
*Lo que está pendiente de decisión arquitectural, no de ejecución.*

- `Versioned W` — dependencia compartida de Firma del Corpus e IAP.
  Sin W versionado, ninguno de los dos puede operar. Es el umbral
  que separa los conceptos establecidos de sus implementaciones.

---

*Jun 2026 — actualizado Jun 25 2026*
