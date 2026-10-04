# MAPA_REG_corpus_v4.md

*3 oct 2026 — gadanin.delamor + Claude Opus 5.5 (Cowork)*
*Actualización de MAPA_REG_corpus_v3.md (Jul 29 2026)*
*Clase R — aprobado por delamor, 3 oct 2026*

---

## Advertencia preliminar (heredada, con una diferencia de método)

Es una interpretación con sesgo de instancia. Las relaciones direccionales son inferidas. Las correcciones son bienvenidas y esperadas.

**Propiedad crítica, heredada:** MAPA_REG depende de la sesión.

**Cómo se leyó esta vez.** No todo se leyó igual, y se declara:

- **Lectura completa:** REG_iap_caso_15_v1, REG_armstrong_stop_coco_v1, REG_p4_n64_conclusion_final_v1 (§Conclusión y trazabilidad), REG_unidad_texto_saturacion_v1 (§1, §3, §5, §6, Abierto, Estado), REG_orbitas_conjuntos_invariantes_v1 (§5, §11, "no establece"), MAPA v3.
- **Lectura estructurada** (encabezados + Descripción + Estado/Resultado/Hallazgo): los demás REG agregados entre el 1 de agosto y el 20 de septiembre de 2026.
- **No releídos:** REG_hint_next_instance_v6–v8 y REG_iap_caso_06–08. Ya estaban cubiertos por v2/v3, y los hint son registro del canal, no del proyecto.
- **No hubo delegación:** toda la lectura la hizo esta instancia (por TRUST: la no transitividad).

Fuente de fechas: `git log --diff-filter=A` sobre `registers/` en el repo local de delamor (HEAD `f938a2f`).

---

## Correcciones a v3

**Gap de archivos cerrado.** v3 listaba como "404 en GitHub / no commiteados" REG_iap_caso_09, 10, 13, 14 (y 11, 12 sin verificar). **Están en `registers/` desde el 1 ago 2026**, junto con REG_iap_caso_15_v1 y REG_hint_next_instance_v6–v8.

**COCO conectado al canal.** v3 lo dejaba implícito. REG_coco_w_congelada_v1 (sep) lo dice explícito: el defecto de W congelada *"hoy no es alcanzable en producción porque el canal vivo no inyecta thermostat"*. Es coherente con lo que delamor declaró para el paper: **COCO nunca se conectó al canal IAP**; se ejerció en tests y drivers. Ojo: REG_armstrong_stop_coco_v1 dice "pipeline real", pero es `MonitorService + COCO` en un script de test, no el canal.

**"Nodos aislados por top_k".** El mecanismo propuesto en REG_hipotesis_distancia_contextual_v3 §2 **no era**. El real estaba en CorpusService y se corrigió en `5aa3504` (v4 §1–§2).

---

## Capas del corpus — v4

*(Definiciones heredadas. Dos capas nuevas: 3b y 3c.)*

**Capa 1 — Fundamento empírico externo** (fourforums, CreateDebate)
- Nuevo: **REG_p4_n64_conclusion_final_v1** — P4 confirmado en N=64. La reapertura de REG_mapeo_magnetico se apoyaba en una preocupación ya refutada: los 60 pares negativos reales son 100% T0↔T1.
- Aclaración (3 oct): la W de fourforums de los pipelines v8g/v8h es **relacional** (nodos = autores, desde quote/response y stance; v8g saltea `text`). No es una W de términos.

**Capa 2 — Fundamento empírico interno** — sin cambios de fondo.

**Capa 3 — Instrumentos**
- `_relax_orbit` (commit `1e14274`) en coco.py y monitor_service.py: cuenta órbitas, no estados terminales (REG_orbitas).
- **MonitorService unificado** con las rutinas de COCO: max_iter 200, `count_seed`, `sampling_mode`. La W sobre la que cuenta cada uno se preserva distinta a propósito (REG_monitor_service_unificar_rutinas).
- **Selección de nodos con regla de desempate:** donde el dato no decide, se conserva el precedente. N deja de ser fijo (REG_seleccion_nodos_desempate).
- `services/ckm_landscape_config.py` (clase `CKMlandscapeConfig`, con "l" minúscula).
- (3 oct) `analytics.py` movido a `services/` sin cambios salvo el import (`0ca5494`).

**Capa 3b — Sesgos del instrumento (nueva).** Es la capa que más creció entre agosto y septiembre:
- **Coupon-collector:** el conteo de atractores crece ~1:1 con n_runs y no satura (REG_stochastic_eval_v1, 10 seeds).
- **Modo de muestreo de σ₀:** uniforme, ponderado y boltzmann dan conteos distintos; el ponderado baja en 92/100 pares (stochastic_eval_v2, count_attractors_bias, boltzmann_sampling).
- **La regla de empate infla A0 ~×3:** 174 contra ~60 con empates resueltos, porque las coordenadas congeladas propagan diversidad de σ₀ (REG_armstrong_boltzmann_comparison).
- **β_c depende de la escala de W**, no solo de su geometría (boltzmann_sampling).
- **D_ckm cuantizado:** la grilla la fija A0, y el umbral 0.40 puede caer en un hueco (REG_wmixta_forzado_paso3).
- **Dos D_ckm:** el de MonitorService y el de COCO tienen A0 distintos. El que gobierna zone/STOP es el de COCO (armstrong_stop_coco).
- **Las masas convergen, los conteos no.** Verdad de terreno por enumeración de 2²⁰ en tres corpus N=20 (REG_orbitas §9–§10) → criterio operativo propuesto (§11) → **N_eff** en el paper (v19+).

**Capa 3c — Extracción y unidad de texto (nueva)**
- REG_hipotesis_distancia_contextual v2 → v3 → v4: nodos aislados en la mitad de las W, mecanismo real en CorpusService, bootstrap 12 de caso09 deja de sostenerse.
- REG_unidad_texto_saturacion_v1: la unidad de texto decide qué W existe; lo que explica el colapso es la **saturación de pares distintos**; **ninguna W_mixta del proyecto fue verificada contra nulo** (§5.2); Néel es quien puede decir "acá no pasa nada".

**Capa 4 — Dinámicas del campo**
- **Ponderación endógena de α:** α es función de D_ckm (REG_sesion_coco_endogeno_v2).
- **OPERADOR_STOP_COCO en un pipeline MonitorService + COCO** (script de test): Δ_A > 0 en los STOP observados, porque comprime sin destruir. **seed 42 da 20/20 STOP, seed 123 da 3/20.** El "20/20" dependía de la semilla (armstrong_stop_coco, réplica).
- **n_runs como variable implícita:** quiebre abrupto en n_runs = 70 (REG_n_runs_sweep_armstrong). H2 sobre A0 contra A_actual: respuesta parcial (REG_h2_a0_vs_aactual).
- **COCO en uniforme puede quedar en un estado absorbente:** el soporte de Δ_r no cambia al multiplicar por α (armstrong_boltzmann_comparison).
- **W_mixta natural contra forzado** sobre caso09_run2: el modo decide la grilla, y la grilla decide si COCO puede actuar (wmixta_natural_paso2, forzado_paso3, consolidado).
- **COCO.self.W congelada:** MonitorService nunca adopta la instancia nueva (REG_coco_w_congelada).

**Capa 4b — IAP Chatroom experimental**
- **Caso 0.15:** G conectado al MonitorService del servidor, en paralelo real. Tinker se niega a mapear sin contenido ("rechazo epistémico correcto"). Mark no publica. n=1 (REG_iap_caso_15).
- **G no ve el rechazo epistémico:** el termap v1 no tiene nodos para overclaim, hedge o rechazo por ausencia (REG_behavior_graph_epistemic_gap).
- (3 oct, TRUST) Serie IAP declarada en el paper como **serie de tests en vivo, irreproducible, casos no comparables**.

**Capa 5 — Contacto con agentes externos** — sin REG nuevos.

**Capa 6 — Condiciones del proceso**
- **REG_reglas_no_declaradas_R18plus_v1:** R18–R29, con tres estados (verificado / verificable / abierto). R18 es la separación W/Δ (0.78 → 0.02).
- **REG_coco_docstrings_rewrite_v1:** v1 y v2 de los docstrings se escribieron sin verificar contra el código y contenían afirmaciones falsas.
- **REG_divergencias_sonnet_sesion_20260829_v1_1:** dos instancias en que Sonnet declaró haber leído un documento sin haberlo leído. Registrado como divergencia de instrumento.
- **REG_minimos_locales_atractor_forzado_v1 + textos verbatim:** la conversación como laboratorio.
- **REG_condiciones_meta_access_v1-3:** condiciones de acceso de un device como Code.

**Capa 7 — Estado abierto:** ver más abajo.

---

## Orden temporal — adiciones desde Jul 29 2026

```
Ago 1   ingreso al repo de la serie IAP 06–15 + hint v6–v8 (cierra el gap de v3)
Ago 2   REG_reglas_no_declaradas_R18plus_v1
Ago 10  REG_armstrong_stop_coco_v1          ← STOP en pipeline de test; seed 42 vs 123
Ago 11  REG_sesion_coco_endogeno_v2          ← α endógeno
Ago 14  REG_mapeo_magnetico_ckm_v1           ← propone SALAMANCA y Néel; reabre P4 N=64
        REG_n_runs_sweep_armstrong_v1        ← quiebre en n_runs=70
        REG_behavior_graph_epistemic_gap_v1, REG_coco_docstrings_rewrite_v1
Ago 16  REG_stochastic_eval_v1, REG_h2_a0_vs_aactual_v1
        REG_p4_n64_conclusion_final_v1       ← cierra la reapertura de P4
        REG_minimos_locales_atractor_forzado_v1 + 2 textos verbatim
Ago 29–Sep 4  (ingreso Sep 4)
        REG_count_attractors_bias_v1, REG_stochastic_eval_v2, REG_boltzmann_sampling_v1
        REG_armstrong_boltzmann_comparison_v1 ← empate infla A0 ×3
        REG_wmixta_natural_paso2_v1, REG_wmixta_forzado_paso3_v1, REG_wmixta_consolidado_v1
        REG_divergencias_sonnet_sesion_20260829_v1_1
Sep 6   REG_monitor_service_unificar_rutinas_v1
Sep 8   REG_orbitas_conjuntos_invariantes_v1  ← enumeración 2²⁰; masas convergen
Sep 9   REG_condiciones_meta_access_v1-3
Sep 10  REG_coco_w_congelada_v1
Sep 17–18 REG_hipotesis_distancia_contextual_v2, v3, v4
        REG_seleccion_nodos_desempate_v1
Sep 20  REG_unidad_texto_saturacion_v1         ← saturación; sin nulo para W_mixta; Néel
Oct 3   (fuera de registers/) REG_borrador_salamanca_s1_v1 en docs/ — SALAMANCA implementado
        (fuera del repo) REG_divergent_sesion_trust_v1 en ckm___memories — replay no reproducible
```

---

## Relaciones direccionales — nuevas en v4

### Eje del conteo → N_eff
```
REG_stochastic_eval_v1 (coupon-collector, 10 seeds)
  → REG_count_attractors_bias_v1 → REG_stochastic_eval_v2 (ponderado baja el conteo)
  → REG_boltzmann_sampling_v1 (β_c depende de la escala)
  → REG_armstrong_boltzmann_comparison_v1 (el empate infla A0 ×3)
  → REG_orbitas_conjuntos_invariantes_v1 (órbitas; masas convergen; enumeración 2²⁰)
  → CRITERIOS_diversidad_formulacion_v1 / paper §4.3 (N_eff, validación exacta)
```

### Eje COCO / Armstrong
```
REG_sesion_coco_endogeno_v2 (α endógeno, 43/43 tests)
  → REG_armstrong_stop_coco_v1 (STOP en pipeline de test; Δ_A>0; seed 42: 20/20, seed 123: 3/20)
  → REG_n_runs_sweep_armstrong_v1 (n_runs implícito, quiebre en 70)
  → REG_h2_a0_vs_aactual_v1
  → REG_armstrong_boltzmann_comparison_v1 (estado absorbente en uniforme)
  → REG_wmixta_* (la grilla de D_ckm decide si COCO actúa)
  → REG_monitor_service_unificar_rutinas_v1
  → REG_coco_w_congelada_v1 (W congelada; no alcanzable en producción)
```

### Eje extracción → unidad de texto → SALAMANCA
```
REG_hipotesis_distancia_contextual_v2 → v3 (aislados) → v4 (bug en CorpusService, 5aa3504)
  → REG_seleccion_nodos_desempate_v1 (precedente donde el dato no decide)
  → REG_unidad_texto_saturacion_v1 (saturación; sin nulo; Néel)
  → (Oct 3) TASK_salamanca_neel_coercividad_v1…v5 + REG_borrador_salamanca_s1_v1
```

### Eje W_mixta: verificación
```
REG_mapeo_magnetico_ckm_v1 (propone SALAMANCA y Néel; reabre P4 N=64)
  → REG_p4_n64_conclusion_final_v1 (P4 N=64 confirmado; la reapertura no se sostiene)
  → REG_unidad_texto_saturacion_v1 §5.2 (ninguna W_mixta verificada contra nulo)
  → REG_borrador_salamanca_s1_v1 (caso09: modularidad, no tensión; falta control positivo)
```

### Eje honestidad del instrumento
```
REG_reglas_no_declaradas_R18plus_v1 (estados verificado/verificable/abierto)
  → REG_coco_docstrings_rewrite_v1 (docstrings escritos sin verificar)
  → REG_divergencias_sonnet_sesion_20260829_v1_1 (declaró leer sin leer)
  → REG_condiciones_meta_access_v1-3
  → (Oct 3, TRUST) "lo leí" de Opus era un resumen de WebFetch; "no existe" de Code era un token acotado;
     REG_borrador_salamanca §4: ocho errores de método, ninguno encontrado por quien los cometió
```

---

## Pares en tensión — nuevos en v4

`REG_p4_n64_conclusion_final_v1 (P4 confirmado)` ↔ `REG_unidad_texto_saturacion_v1 §5.2 (ninguna W_mixta verificada contra nulo)`
→ No se contradicen. P4 está confirmado **bajo la construcción de W_mixta**, y esa construcción no tiene estado nulo. El paper v26 dice "*Verified*" sin esa calificación. Pendiente.

`REG_armstrong_stop_coco_v1 ("MonitorService adopta Δ_r comprimido")` ↔ `delamor / DEFS v14 / paper v22+ (COCO opera solo sobre su propio Δ_r_compresiones)`
→ **Resuelta en el código** (Code, 3 oct, `e8fc177`, TASK salamanca §4.1): `MonitorService._Delta_r` se escribe en tres lugares (init, incremento, reset) y en ninguno desde COCO. COCO lo lee y comprime solo su `_Delta`. El REG Armstrong describe el código **anterior a D3**. No hay contradicción: hay una fecha.

`armstrong seed 42 (20/20)` ↔ `armstrong seed 123 (3/20)`
→ El mecanismo replica (α en rango, Δ_A > 0). El conteo de STOP no: depende de dónde cae una estimación ruidosa respecto de un umbral fijo.

`D_ckm de MonitorService` ↔ `D_ckm de COCO`
→ Son dos magnitudes con A0 distintos. El paper usa una sola sigla.

`REG_orbitas §5 ("el frozenset no pierde información")` ↔ `TASK_representacion_atractores_adaptador_v1 (Oct 3: "colapsa estados distintos")`
→ REG_orbitas ya lo había resuelto en septiembre: el mapa es determinista. En {−1,+1}^N el conjunto activo determina el estado. La TASK de octubre lo reabrió sin leer el REG. Es el patrón de REG_p4_n64: reabrir sin leer lo que cerró. **Cerrado** en el adaptador §4.5 (Code, 3 oct, `e8fc177`).

`REG_mapeo_magnetico §3.1 ("SALAMANCA detecta estructura adversarial")` ↔ `REG_borrador_salamanca_s1 §3 ("lo que detecta es modularidad")`
→ Corrección a aplicar en DEFS §16 si delamor la aprueba.

`W_pos ferromagnética (mapeo_magnetico §1.1)` ↔ `Oct 3: 99.9% de la masa en todo-prendido/todo-apagado; tramo categorias: vacío`
→ Consistentes: un paisaje sin frustración es un imán de dos polos.

---

## Estado abierto — v4

**Del instrumento:**
- Qué debe contar D_ckm: L, L/~ o masas. Es decisión del modelo (REG_orbitas, "no establece").
- Los dos D_ckm: cuál se reporta y cuál gobierna.
- n_runs y la grilla de D_ckm frente al umbral fijo 0.40.
- COCO.self.W congelada (REG_coco_w_congelada).
- Los parámetros de extracción no se persisten en `CorpusService.save()` (unidad_texto, Abierto).
- El criterio de unidad de texto: qué saturación es "lejos".

**De SALAMANCA / Néel (Oct 3):**
- Control positivo: **RfA** (SNAP, verificado), o el texto de fourforums con extensión del parser v8g.
- Néel, paso 2: no corrido.
- La frontera gruesa de caso13 **depende de la clasificación** del vocabulario de coordinación.
- k-means con varias inicializaciones: aplicado al control (10 inits).

**De la serie IAP:** heredados de v3, todavía abiertos:
- fuga de identidad (`_strip_own_prefix`);
- corte de 86 caracteres;
- auto-señalización no instruida;
- G sin nodos epistémicos (nuevo, de 0.15);
- réplica de 0.15 con un Peter que aporte contenido.

**Del paper** (lista en SUPERTASK §5): nodos de fourforums = autores; P4/P5 sin nulo; `threshold`; IAID 2023/2024 (resuelto como linaje M.M. 2023 → IAID 2024, BE previo); evidencia en .docx; README/THEORY.

---

## Lo que el mapa no captura — v4

- La relación entre REG e Informes de Trabajo sigue sin trazar.
- **Dos registros del 3 oct no están en `registers/`:** REG_borrador_salamanca_s1_v1 (en `docs/`, pasa con el OK de delamor) y REG_divergent_sesion_trust_v1 (en ckm___memories, fuera del repo).
- Los REG leídos de forma estructurada pueden tener relaciones internas que esta lectura no ve.
- El trabajo del Codespace posterior a `f938a2f` no está en este mapa.

---

*Jul 22 2026 — v2 construido*
*Jul 29 2026 — v3*
*Oct 3 2026 — v4: ingreso de la serie IAP al repo, capa de sesgos del instrumento, capa de extracción y unidad de texto, ejes conteo→N_eff, COCO/Armstrong, extracción→SALAMANCA, verificación de W_mixta y honestidad del instrumento.*
