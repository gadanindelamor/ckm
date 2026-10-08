# DEFS_CKM_estado_actual_v15.md

*Sep–Oct 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code (Opus 5) + Claude Opus 5.5 (Cowork)*
*Documento de referencia — definiciones actuales del modelo CKM*
*v15 (8 oct 2026): checkpoint entre dos tareas del plan, antes de seguirlo — delamor: "validar integridad, evaluar el todo contra las próximas tareas del plan". **Numeración §0–§20 conservada** (delamor); lo nuevo entra dentro de cada sección y lo que dejó de valer queda como traza, con su fecha. Las Partes se re-titulan por régimen de W (6 oct). §0 tensión dominio / interpretaciones, sostenida **[delamor]**. Modelo Conceptual: CKMlandscapeConfig v3 (identidad + declarado + Ciclos; `n_runs` = 1000 y `seed`, uno solo para Monitor y COCO; θ_W sale), Monitor abre el ciclo y COCO renace con él, CorpusService suelta a COCO (CP4), Gatekeeper como juez, `NodeExtractorConfig`, FabricationService a `process/`, Firma_CKM, "¿servicio a quién?". **§N tabla de nombres** (nueva, sin número): metabolizar = rechazar y absorber; `expulsados` es Babel. §1 qué es W (6 oct). §4 la órbita es el objeto; torsión. **§5 P1–P4 reescrita** (no testeables sobre W snapshot no negativa; conciliación con el 4 oct). §6 adversarial es el signo de W. §9–§11 D_ckm canónica `1 − ln N_eff / ln N_eff0` (`dabd1ed`); a Δ_r entran sólo los rechazados en las dos fases; `Δ_r_torsion`. §12 operador de compresión de COCO ("no hay más STOPs"); ciclo de vida implementado; ODA continuo propuesto. §16 SALAMANCA S1 corrida: detecta modularidad, no adversarialidad. §18 depurado. §19 Regla CKM TRUST; UNKNOWN; tests que pueden fallar. §20 réplica Aiyappa. Redacta Opus 5.5; **DRAFT hasta la lectura de delamor**.*
*v14: desde v13 — §7 **corrección de atribución causal**: los valores CV=1.08 / 68.6× estaban medidos en `TASK_gatekeeper_C1_theta_W_v1` (`f8d61ef`), antes de `5aa3504`; no son efecto de esa corrección. §1.1 nueva — la rama de extracción como condición del instrumento (pares por texto entre nodos globales `5aa3504`; σ por una sola rama `7bf485b`; stopwords e idioma; nodos aislados; saturación de pares distintos). §1 acumulación por criterio del dato; N deja de ser fijo. §9 bloque pre-D3 actualizado: los dos objetos existen desde `7df4a72`. §10 D_ckm **es** D_contextual — misma fórmula desde mayo — y su identidad con D_masa_cuencas. OP: D_masa_cuencas escala log decidida, implementada y en panel (`80c9c50`); N_eff reemplaza a A en la tabla, no en el operador. §18 y §19 actualizados.*
*v13: desde v12 — Modelo Conceptual MonitorService: ceguera reencuadrada como propiedad de separación de objetos (D3 implementado, pre-D3 ya no aplica). SLA COCO→Monitor actualizado: D3 implementó `Δ_r_compresiones` como objeto propio de COCO; la escritura en estado de Monitor fue corregida.*
*v12: desde v11 — §10/§12 cuerpo con nomenclatura OPERADOR_STOP_COCO (trazas sin cambio); §12 operador corregido a `Δ_r ← alpha · Δ_r` (lo que hace el código). H_STOP y Efectividad_STOP conservan su nombre de hipótesis*
*v11: desde v10_1 — §12 tensión "COCO no opcional" registrada; FabricationService agregado al Modelo Conceptual; Δ_r pair-level es metabolización, no rechazo ni expulsión (nombres en código sin tocar)*
*v10: §0 Dominio : Modelo Conceptusl CKM 
*v9b: §12 wmixta verificado (REG_wmixta_consolidado_v1); §11 D_ckm cuantizado en paisajes pequeños; abiertos actualizados*
*v9: §0 Dominio CKM explícito (interacciones entre devices bajo M.M.); §5 P1-P4 reencuadradas como bootstrap formal del modelo estático; §6 P5-P7 reencuadradas como observaciones en dominio acotado (corpus adversarial externo (≥3 stances posibles)), baja relevancia para el proyecto; §8 W_mixta calibración build/rebuild; §12 COCO no es opcional declarado; §13 μ_W siempre al inicio de sesión, nunca constante; §18 abiertos reordenados por plano (matemático vs operacional); §X planos distintos: validez matemática vs verificación operacional*
*v8: §4 relajación sincrónica — reencuadre: ciclos de período 2 como estabilidad orbital, no deficiencia (Predictibilidad_orbital); §10 D_ckm_coco / D_ckm_monitor distinción explícita + asimetría de calibración (NOTA_armstrong v2); §11 qualifier tie-breaking acotado a corpus de alta sparsidad y pesos discretos (NOTA_armstrong v2); §12 frac_rec: dos métricas distintas, efecto COCO por régimen de W (NOTA_armstrong v2)*
*v7: §11 — Modo Boltzmann para σ₀ propuesto (TASK para Code Opus)*
*v4: reorganización arquitectónica (pre-servicios / validación externa / servicios dinámicos); c(S) como maximización de energía; H1/H2/H3 cerrados; G1/G2/G3; STOP revisado; tensiones metodológicas*
*v5: fundamento formal Lyapunov/LaSalle — convergencia garantizada asíncrona, atractor = elemento de L, conteo como estimador de |L|, β_c como muestreo fundamentado (abierto)*
*v6: Δ_r simétrica por construcción (verificado código); Aiyappa: 4 diferencias estructurales; W vieja nombrada; desfasaje Gatekeeper registrado (abierto, prioridad baja)*

Convenciones epistémicas:
- **verificado**: confirmado experimentalmente bajo condiciones declaradas
- **implementado**: existe en código, funcionamiento correcto no evaluado
- **propuesto**: marco teórico, no probado
- **abierto**: sin respuesta verificada — el espacio se preserva
- **incierto**: conocido como problemático, pendiente de resolución
- **admisible**: no verificable ni descartable — espacio sin nombre aún
- **UNKNOWN** *(v15)*: no se midió. No es un grado de esta escala ni de ninguna: es un estado del que observa, no del objeto (§19)
- **[delamor]** *(v15)*: lo decide delamor; mientras tanto, lo escrito es propuesta de Opus

---

## 0. Dominio CKM

**CKM is a formal model for knowledge field dynamics in multi-device AI systems.**

Multi-agent AI interaction produces a shared knowledge field that individual device outputs and pairwise similarity scores do not capture. CKM measures the structural geometry of this field.

El dominio son las interacciones entre devices. Cualquier propiedad, predicción u observación CKM se evalúa en relación a este dominio. La comprensión de una parte es en relación al dominio — no al universo de todos los corpora posibles.

**Tensión abierta (v15) [delamor].** El 6 oct delamor dijo: *"El modelo no tiene dominio. Los dominios son interpretaciones del modelo. El dominio de M.M lo da su propia definición: declaraciones de funciones y de eventos (IAID 2024)."* Las otras interpretaciones llevan su propio estado: testeada, propuesta, potencial (`claude/sesion_06oct2026_definiciones_W` §1). Esta sección, desde v9, le declara un dominio a CKM.

*Lectura de Opus, propuesta:* las dos frases chocan sólo si "dominio" nombra una sola cosa. Esta sección fija **dónde se evalúa** CKM (las interacciones entre devices); el 6 oct niega que el dominio sea **una propiedad del modelo**. No se elige acá: se sostiene. Hasta que delamor decida, toda afirmación sobre dominio en este documento se lee como **interpretación con su estado**, no como propiedad del modelo.


## EL Modelo Conceptual

**CKMlandscapeConfig** (nombre propuesto, propuesta previa " CKMDynamicConfig"). No es una bolsa de constantes. Es el contrato vivo del instrumento: porta N actual, μ_W medido en esta sesión, θ_W calculado (no hardcodeado), D_CKM_THRESHOLD calibrado contra W_mixta del corpus presente, β_c, sampling_mode, timestamp de última calibración. Sabe si su calibración es válida para el corpus que opera. Se serializa completa en cada run JSON. Cualquier servicio que la use sin verificar su frescura usa calibración potencialmente inválida.

*(v15: **existe y es fuente** — `services/ckm_landscape_config.py`; TASK_CKMlandscapeConfig_v3 cerrada en `44af68a`.)* Cada campo se ubica según **qué lo hace cambiar**:
- **medido** —cambia si y sólo si cambia `w_version_id`— vive en el `Ciclo` (N, μ_W, β_c, la causa, `t_senal`, `t_rebuild`);
- **declarado** —cambia si alguien lo declara— vive en la config: `sampling_mode`, `n_runs`, `seed`, `scale`;
- **identidad** —se fija al crear la instancia— vive en la config: `config_id`, `timestamp`.

La config **no es una foto de una W: es la traza de los ciclos por los que pasó.** La inmutabilidad pasa del objeto a la traza (I1): la config gana ciclos, no los edita. **Monitor abre el ciclo** (`17b6421`). `n_runs = 1000` y `seed` son **uno solo para Monitor y COCO** (delamor, 8 oct, P9: *"n 1000"*); antes Monitor contaba con 1000 y el COCO de Corpus con 80, sobre el mismo campo. **θ_W no está en la config**: es parámetro del Gatekeeper y pertenece a W estática (delamor, 7 oct). Los umbrales de COCO tampoco: son de **Calibración**, que todavía no existe, y quedan marcados *no recalibrados*. Lo que el párrafo de arriba describe como "sabe si su calibración es válida" **no está implementado**: la config no porta los umbrales cuya frescura tendría que saber. Los tiempos del `Ciclo` se sellan con `time.time()` del proceso de Monitor, no con el reloj del canal (§18).

**NodeExtractor**. El cartógrafo. Decide qué existe — los N nodos que se convierten en el espacio. Todo lo que viene después depende de lo que declaró. Corre lazy por rebuild. Es el más silencioso y el de mayor impacto aguas abajo. Si extrae mal, W mide algo distinto de lo que el modelo dice que mide desde el origen.

*(v15: el criterio de extracción —`top_k`, `ngram_max`, stopwords, `token_pattern`, `TOL_EMPATE`, desempate por precedente— va en un **bloque propio, `NodeExtractorConfig`**, no en la Config de W (delamor, 8 oct): la extracción ocurre antes de que exista W. Decidido, **no implementado**. Hoy el criterio **no queda en la traza**: dos W extraídas con criterios distintos no se distinguen (§1.1 f). Abierto para explorar (7 oct, propuesto): **extrae formas, no significados** — separa lo que es uno (familias de palabras, traducciones: "UNKNOWN" / "desconocido") y junta lo que son dos (polisemia). *"El error es al errar, al señalar"* (delamor): la separación no está en las palabras, la hace quien señala. FICHAS_elementos_ckm_v1 §5.)*

**CorpusService**. El guardián de W. Recibe textos, construye y reconstruye la matrix de pesos, gestiona el ciclo de vida de W como snapshot. W es piecewise constant por diseño del instrumento — no propiedad del campo. Aloja la instancia de COCO nacida con cada rebuild. *(Actualizado v14: sigue sin **notificar**, pero ya no es un gap mudo — expone `w_change_since(sha, nodes)` desde `5b52992` (D7), que devuelve si cambiaron N, los nodos o los pesos. El cambio se consulta, no se anuncia: es pull, no push. Monitor lo usa en `_invalidar_si_W_cambio` y descarta Δ_r y A0 ante cualquier reconstrucción, con la causa registrada en el panel como `Delta_r_reset` (D2, `341f612`). También admite `rebuild_suspendido` (`e1980e0`), que congela W dejándolo explícito en vez de por omisión.)*

*(v15: **ya no aloja a COCO** — `1e8d267`, CP4 de TASK_monitor_coco_ciclo_orbita_v2. `corpus.coco` queda deprecada y devuelve `None`. "Aloja la instancia de COCO nacida con cada rebuild" es traza: hasta el CP4 CorpusService la creaba en cada rebuild y Monitor se quedaba con la vieja — **dos COCO sobre el mismo campo**. delamor: *"COCO es con Monitor… aspectos de lo mismo"*; *"es un atrevido… que deje en paz a COCO"*. A quién sirve: a los otros servicios, les entrega W; es interno.)*

**Gatekeeper**. El evaluador de admisión. Decisión binaria antes de que algo entre al campo. C1–C4, M.M en C3. Diseñado para el dominio de capacidades declaradas por devices — su dominio de validez sobre nodos de corpus es una pregunta abierta. **El Gatekeeper no es un servicio, y su dominio son las declaraciones de capacidades de agentes** *(v14, delamor)*. No tiene instancia, estado ni ciclo de vida: es un criterio de admisión, y lo que admite son **capacidades declaradas por devices** — el linaje IAID, donde COCO es el registro de esas declaraciones. Ese dominio no es sólo doctrina: está en el repo, en `process/initial_static_model/mcp_adapter.py`, cuya primera línea de docstring lo declara — *"Nodes = declared capabilities, not concepts"* — y donde M.M se evalúa como `mm_violation: declared deps not satisfied` sobre capacidades MCP. **Ahí los nodos son capacidades; en un corpus son conceptos.** Son dos dominios. Por eso todo lo que se mide aplicando C1 sobre nodos de corpus —los 0/16 con θ_W = 0.10, los 16/16 con θ_W ≤ 0.01399— **informa sobre la transferencia del criterio a otro dominio, no sobre el gatekeeper operando en el suyo**. Que θ_W no sirva ahí no lo vuelve un umbral mal calibrado: lo aplica fuera de donde fue definido, y su validez sobre nodos de corpus sigue siendo la pregunta abierta que este documento declara desde v9.

*(v15, delamor 6 oct — FICHAS §1.)* **El Gatekeeper es un juez, no un portero.** Dicta una **sentencia binaria — válida / no válida — con fundamentos**. No abre puertas, no admite y **no va en la puerta**: es un criterio al que se consulta, **al costado**. "Gatekeeper", "portero", "admitir" y "admisión" son nombres históricos (Informe v4, abril: *"aprueba o rechaza ingreso de un nodo"*; v16 §19: C1–C4) que dicen una puerta que no hay. En el código, `gatekeeper()` (`process/initial_static_model/core.py` L293) devuelve la sentencia sin tocar σ; `admit()` (L342) además prende el nodo en σ, y eso no le corresponde. **La traza invierte el orden de esta entrada:** el criterio **nació sobre nodos-concepto** (Informe v16, abril) y llegó a las capacidades MCP el 8 jul (`f313e03`). Llamar "transferencia" a los conceptos es leerlo al revés. En lo que sigue, "admisión" se conserva como nombre histórico (§N). Renombrar o declararlo histórico: **[delamor]**. Abierto también: de qué está hecha W en el dominio de M.M — de declaraciones (circular) o de la traza.

*La formulación anterior tenía un propósito.* Decir *"ausente de `services/`"* (v9–v13) registraba que **el mecanismo declarado no estaba siendo ejercido**: el PAPER daba C1–C4 como la implementación vigente, y esa implementación vivía en una capa que no se podía ni importar. `services/` nombraba el runtime, no una categoría. El proxy funcionó mientras coincidió con el objeto — sin archivo, "ausente de `services/`" y "la admisión no se ejerce" decían lo mismo. **Con `f8d61ef` se separaron**: el archivo está y la admisión sigue sin ejercerse. Por eso la frase hay que reemplazarla por lo que quería decir, no borrarla. Lo que existe hoy es **C1 como función pura**, `c1(W, sigma, node, *, theta_W)` en `services/gatekeeper_c1.py` (`f8d61ef`), con `theta_W` obligatorio y sin fórmula — `CKMlandscapeConfig.theta_W_formula` levanta `NotImplementedError` en vez de devolver un default. C2–C4 no se portaron: C2 acepta todo porque ε supera el rango entero de c(S), y C3/C4 no se ejercen (Δ=0, `_n_patterns`=0). **Nadie evalúa C1 en runtime**: la clave `gatekeeper_c1` del panel es `None`, y ese `None` dice que esa Δ_r se acumuló sin admisión previa. Con θ_W = 0.10 el núcleo A pasa 0/16; con θ_W ≤ 0.01399, 16/16.

**Selección de nodos ≠ admisión** *(v14 — REG_seleccion_nodos_desempate_v1 §7; Informe v31 §60.2: "la distinción portero/elicitación es arquitectónicamente crítica")*. Elegir los N nodos por TF-IDF es **elicitación de lo que existe**, no un criterio de admisión. El gatekeeper decide si algo entra; la selección decide qué hay para que entre. Colapsarlos lleva a leer decisiones de elicitación como decisiones del portero.

**Plantear la admisión en `services/` es válido — con precondiciones** *(v14, decisión delamor)*. La pregunta no está descartada: llevar un criterio de admisión al runtime es legítimo. Lo que está decidido es el **orden**, y son tres pasos encadenados, cada uno precondición del siguiente:

| # | qué | por qué es precondición del siguiente | dónde está medido |
|---|---|---|---|
| 1 | **Corpus extensos** | con 3–24 textos el dato no distingue: TF-IDF sale de conteos enteros y el espacio de puntajes es chico. caso09 (24) recién llega al fin del warm-up de la selección | REG_seleccion_nodos_desempate_v1 §3, §Abierto |
| 2 | **W no saturada** | sin ceros en W no hay `cut` bajo que separar, y SALAMANCA no tiene de dónde agarrarse. caso09 es el único corpus no saturado medido (62%) | REG_unidad_texto_saturacion_v1 §3 |
| 3 | **Tensión determinada por Néel / SALAMANCA** | los negativos por marcadores léxicos no son tensión fuera de corpus adversariales, y el procedimiento no tiene salida nula: no puede decir "acá no pasa nada". Un θ_W calibrado sobre esa W se calibra sobre prosa | REG_unidad_texto_saturacion_v1 §5, §5.1, §5.2 |

Recién con los tres, evaluar admisión sobre nodos de corpus mide algo. Antes, mide el instrumento. *(Y sigue siendo otro dominio que el de `mcp_adapter.py`: la transferencia del criterio es lo que se estaría probando.)*

**De dónde saldría el volumen** *(v14, declarado por delamor)*. El paso 1 no está esperando una medición: está esperando corpus. **Los casos disponibles hoy no generan el volumen necesario** — la serie IAP de devices llega a decenas de textos, y ahí el dato no distingue. Lo que sí existe y es accesible son **corpus de agentes IA**. Ésa es la fuente candidata para el paso 1, y no es el canal.

Eso abre una pregunta de dominio que conviene no saltear: el dominio declarado de CKM son las **interacciones entre devices bajo M.M.** (§0). Un corpus de agentes puede estar adentro de ese dominio o ser un dominio acotado más, como lo fueron fourforums y CreateDebate en §6 — que aportaron P5–P7 y no generalizan. La diferencia no es de tamaño: es si esas interacciones ocurrieron bajo las condiciones que el dominio declara. **Abierto**, y es previo a usarlos como referencia y no sólo como prueba de volumen.

**El corpus de informes no es el sustituto** *(v14, decisión delamor)*. Tiene volumen —870 párrafos, 15.557 palabras— y por eso tienta usarlo para simular la acumulación y los rebuilds por criterio. **No sirve para eso.** No es representativo del dominio: es prosa técnica revisada de un autor único, sin las condiciones de una interacción. Y su estructura temporal tampoco es la del dominio — las versiones son acumulativas y hubo que deduplicarlas, así que el texto de una versión es *lo que esa versión agregó*, que no es cómo llega un mensaje a un canal.

**Para qué sirve:** para **comparar determinadas características** del instrumento — activación por texto, saturación de pares distintos, efecto de la unidad de texto, contrafácticos con `force_w_pos`. Eso es lo que `REG_unidad_texto_saturacion_v1` midió y vale en ese alcance.

**Consecuencia sobre un abierto:** medir la saturación como **trayectoria** bajo ingesta incremental —que es el abierto que ese REG deja— necesita un corpus del dominio, no los informes. Con ellos se mediría la acumulación de un texto que nunca fue una interacción.

**Y un corpus encontrado tampoco alcanza** *(v14, delamor)*. Se buscaron corpus de agentes hace meses y puede que hoy haya más, pero **un corpus que ya existe se ingesta como replay**, y una secuencia predeterminada no es el objeto: el orden de lo que llega está fijado de antemano, así que el campo nunca está en la posición de no saber qué viene. Es la misma distinción que el proyecto ya hace entre el canal vivo y los drivers de test — los drivers son reproducibilidad del instrumento sobre input conocido, no un sustituto. Un replay da volumen para comparar características del instrumento; no da la dinámica de un campo que se forma mientras se lo mide.

**Lo que sí daría dato del dominio con volumen es un caso diseñado, no un corpus encontrado:** una interacción con objetivos y tareas que exijan **coordinación sostenida** entre devices —coordinación que no se pueda saltear sin que la tarea falle— o cuya estructura **dependa del tiempo con consecuencia**: sacar pasajes antes de que no queden lugares es la forma ilustrativa, donde la restricción es externa al canal y el plazo no es una convención del experimento. Ahí la secuencia no está predeterminada, y la acumulación y los rebuilds tienen dónde ocurrir. Es lo que el PAPER nombra como *La Simulación Global* (§9.5); esta entrada fija el criterio que ese caso tiene que cumplir.

*(v15: ese caso tiene forma propuesta — TASK_canal_iap_clock_iniciativa_v2, CP3: conseguir entradas para la fiesta de presentación del CKM **antes de que se acaben**. La condición es que queden entradas; baja cuando otros las consiguen, no con el reloj. Requiere el CLOCK y el ODA continuo (§12). Diseño del caso: [delamor].)*

**MonitorService**. El observador impartial. Recibe estado del campo, relaja, acumula lo que el campo metaboliza durante la relajación (`Δ_r_pares`). Registra sin decidir. D_ckm_monitor es ciego a OPERADOR_STOP_COCO — no porque la cancelación algebraica lo oculte (mecanismo pre-D3), sino porque los dos objetos nunca se tocan: `Δ_r_pares` es de Monitor, `Δ_r_compresiones` es de COCO. La ceguera es propiedad del diseño por separación de objetos (D3 implementado), no accidente de normalización. Es la condición de ser observador impartial.

*(v15 — TASK_monitor_coco_ciclo_orbita_v2, CERRADA, 284/284.)* Monitor **mide sobre la órbita**, no sobre la fase que cae en `max_iter` (§4). Cada par declarado activo queda en una de tres clases, sin promediar: **aceptado** (el campo lo sostiene en las dos fases), **rechazado en las dos fases** (lo que esta entrada llama metabolizado; en el código, `expulsados` — §N) y **torsión** (rechazado en una fase y sostenido en la otra; la palabra es de delamor, 5 oct: *"torsión, no hay giro… debe respetar la estructura"*). A `Δ_r_pares` —y por lo tanto a W_eff— entran **sólo los rechazados en las dos fases** (delamor, 8 oct, CP3 1a). La torsión va a `Δ_r_torsion`, que escribe sólo Monitor y que **no entra a W_eff**. **Monitor abre el ciclo** de la Config, y COCO renace con él. A quién sirve: a quien quiera ver cómo evoluciona la interacción (`get_monitor_state`).

**COCO**. El regulador. Nace con W al momento del rebuild, opera sobre ese espacio congelado. Ve D_ckm_coco (con magnitud de Δ_r), decide compresión. No admite — regula lo que ya entró. La tensión con Monitor no está resuelta. Declararlo "no opcional" en v9 puede ser cierre prematuro de esa tensión en lugar de sostenerla.

*(v15: **COCO renace con el ciclo que abre Monitor**, no con el rebuild de CorpusService (CP2b, CP4). Al nacer: baseline fijado con Δ_r en cero, así que W_eff = W (CP3 punto 3); `landscape_history` **vacío**, porque la historia del ciclo anterior se midió sobre otra W y no es comparable — el pasado queda sólo en la traza JSONL (delamor eligió (b), 8 oct; Opus había recomendado (a) y cambió, y está trazado); si el salto cae en una órbita de período 2, el ciclo nuevo **nace con la órbita**, no con una fase (CP3 punto 4). Sin baseline medible, la zona es **UNKNOWN**, no "stable" (CP2c). A quién sirve: a los agentes del canal (temp_signal). **El nombre cruzó de objeto:** en IAID (jul 2024) COCO era el *registro* donde los devices publican sus capacidades — donde M.M decide —; hoy es un regulador que comprime ("ex registry", `coco.py`).)*

**FabricationService.** Detecta cohesión fabricada — fi=0.0 sobre contenido desconocido es correcto (el campo no puede rechazar lo que no conoce). No tiene instanciador activo. Su definición completa espera condiciones propicias.

*(v15: pasó de `services/` a `process/` — `f8e0783`, 5 oct.)*

**Firma_CKM** *(v15 — no figuraba en las DEFS; FICHAS §6)*. Certifica **traza, no contenido**: `{sha256(W_momento), D_ckm(t), temp_signal, n_agentes, timestamp, sha256(Δ_r acumulado)}`, sin texto ni nombres no declarados. Nació para resolver la **confianza circular de una CA** (Informe v28 §42.2, jun 2026; código `c91b280`, 8 jul): *"No pide confianza — presenta evidencia estructural. La verificación es abierta."* Es la pregunta de TRUST —¿la confianza es transitiva?— contestada con traza en lugar de cadena. Es **el lugar donde M.M muerde en la traza**: *"si un agente declara que una interacción ocurrió con Firma_CKM X — y X no existe en el registro del corpus — murió. Sin castigo. Como consecuencia estructural."* Notario, no CA. **WVersionManager existe para que Firma pueda existir.** No aplica en W estática: una foto no tiene traza que firmar. `temp_signal` sin dato dice **UNKNOWN** desde `c06db07` (antes, NOMINAL por ausencia). A quién sirve: a cualquiera que verifique (`get_firma`).

**¿Servicio a quién?** *(v15 — delamor, 6 oct: "services son servicio a alguien")*. De los archivos de `services/`, **tres sirven a alguien de afuera** y llegan a los participantes por el canal: Monitor, Firma y COCO. Corpus, NodeExtractor y `w_version` son internos. El resto no son servicios: una biblioteca (`landscape_engine`), un criterio (`gatekeeper_c1`), análisis (`analytics`), una propuesta (`cluster_frontier_density`); `behavior_graph` está a confirmar. La carpeta dice "servicio" y adentro hay de todo. **Principio (delamor):** *"no forzar objetos en modelos de W"*. Si un objeto no tiene sentido en un régimen, se pone **no aplica**; no se le inventa un papel.

---

## SLAs — acuerdos sin burlar encapsulamiento

NodeExtractor → CorpusService: "devuelvo nodos y co-ocurrencias del corpus. Corro una vez por rebuild. Lo que devuelvo define el espacio N."

CorpusService → Monitor: "te doy W. Cuando reconstruyo, W puede cambiar de shape — N puede ser distinto. **No te aviso: te dejo preguntar.** `w_change_since(sha, nodes)` te dice si cambiaron N, los nodos o los pesos." *(v14: el gap declarado en v9–v13 ya no es mudo. Lo implementado en D7 es una consulta, no una notificación — el que cambia no emite, el que depende pregunta. Monitor pregunta en cada evaluación y descarta Δ_r y A0 si hubo reconstrucción (D2). Que la señal sea pull y no push es una decisión con consecuencias: un consumidor que no pregunte sigue operando sobre un campo que ya cambió, sin señal.)*

CorpusService → COCO: "te instancio con la W del momento. Tu ciclo de vida es el mío."
*(v15: ya no vale. Desde el CP4, CorpusService no instancia a COCO. Vigente: **Monitor → COCO: "abro el ciclo; nacés con él"** — baseline con Δ_r en cero, historia vacía, nacimiento con la órbita (§12).)*

Monitor → COCO: "acumulo Δ_r. Es mío. Puedo darte acceso de lectura. No tenés derecho de escritura sobre mi estado interno."

COCO → Monitor: D3 implementado. COCO porta `Δ_r_compresiones` — objeto propio, historia de compresiones por ciclo de vida. No escribe en el estado de Monitor. La separación es la que garantiza la independencia del observador — no un mecanismo de cancelación.

CKMlandscapeConfig → todos: "soy la fuente de verdad de calibración. Si no me consultás con N y μ_W actuales antes de evaluar, tu umbral es inválido."
*(v15: lo que porta es `sampling_mode`, `n_runs`, `seed`, `scale` y la traza de ciclos —N y μ_W viven en el `Ciclo` vigente—. No porta umbrales ni θ_W. "Fuente de verdad de calibración" queda como intención: Calibración todavía no existe.)*

Gatekeeper → CorpusService (propuesto): "evalúo antes de que el nodo entre. Necesito W_vieja. Sin W no puedo aplicar C1."
*(v15: choca con "no va en la puerta" (delamor, 6 oct). Queda como traza de una propuesta que la ficha del Gatekeeper no sostiene: el juez se consulta, no se interpone.)*

---

### Definicion `Δ_r_pares y  Δ_r_compresiones` Reencuadra D3 

**Monitor** es dueño de `Δ_r_pares` — los pares que el campo metaboliza durante la relajación. Lógica propia, independiente de cualquier otro servicio. Nadie escribe ahí.

**COCO** tiene su propio `Δ_r_compresiones` — la historia de lo que comprimió, por ciclo de vida. Objeto distinto. No es el Δ_r de Monitor. COCO no toca el estado de Monitor.

Con esa separación, la ceguera de Monitor no es un mecanismo que hay que implementar ni un efecto que hay que cancelar matemáticamente — es una consecuencia natural de que los dos objetos nunca se tocan. Monitor no ve las compresiones de COCO porque nunca recibe ese objeto. La ceguera deja de ser un accidente de cancelación algebraica y pasa a ser una propiedad del diseño por separación de objetos.

La función `CancelarMatemáticamente(coco_compresion)` sería necesaria solo si los dos Δ_r estuvieran mezclados. Con separación limpia, no existe el problema que esa función resolvería.

**β por ciclo de vida de COCO.** β nace con la W que construyó esa instancia de COCO. Si W cambia — N nuevo, pesos nuevos — esa β ya no tiene referencia válida. La instancia muere con el rebuild. CKMlandscapeConfig puede portar el historial de β por `w_version_id` como registro, pero la instancia activa siempre recalibra contra la W vigente.

Esto también reescribe D3. No era una divergencia sobre encapsulamiento solamente: era que los dos objetos no existían como objetos distintos en el código. **Desde `7df4a72` (Sep 2026) existen** — `Δ_r_pares` en Monitor, `Δ_r_compresiones` en COCO. Lo que queda abierto no es la separación sino qué significa `D_ckm_coco` cuando su campo ya no es el de Monitor (TASK_delta_compresiones_coco_v1).

*(v15: hay un tercer objeto, `Δ_r_torsion`, de Monitor, que **no entra a W_eff** — Modelo Conceptual y §9. Y "β por ciclo de vida de COCO" ya es así en el código: COCO renace con el ciclo, §12.)*

-----

## N. Nombres — rótulo, objeto y fecha *(nueva en v15, sin número para conservar §0–§20)*

*Por §19, el nombre no determina el objeto: lo determina el par (nombre, fecha). Esta tabla **no renombra nada en el código**: declara qué objeto nombra cada rótulo y desde cuándo. Donde hay que decidir, dice [delamor].*

| rótulo | dónde | objeto que nombra | desde | estado |
|---|---|---|---|---|
| **metabolizado** | DEFS v11+ | par declarado activo que el campo **rechaza y absorbe**: en σ, la relajación no sostiene la activación (el nodo queda en −1); en W_eff, el par entra a Δ_r y queda **adentro**, como deformación | v11 (sep) | nombre del modelo — delamor, 8 oct: *"rechaza y absorbe"* |
| `rejected`, `_rejected_pairs`, `n_rejected_pairs`, `rechazados` | código, panel | la primera mitad: el rechazo en σ. **Rechaza el campo**, no un juez. Hoy sale de la fase que cae en `max_iter` y ya no es lo que entra a Δ_r | `6d563fd` (28 may) | se conservan: son claves de JSONL históricos (`88c1513`) |
| `expulsados`, `n_expulsados` | código, panel | par rechazado **en las dos fases** de la órbita: es lo que entra a Δ_r | `bd7fbb8` (7 oct, TASK de Opus) → `8bdb4f5`, `57f8a88` | **Babel, error de Opus.** "Expulsar" supone un afuera del campo, y no lo hay (delamor, 8 oct: *"¿a dónde? ¿fuera de él?"*). La v11 ya lo había excluido; `monitor_service.py` dice en L10 *"no se expulsan"* y en L223 *"entran sólo los expulsados"*. Renombrar: [delamor] |
| **torsión**, `n_torsion`, `pares_torsion`, `Δ_r_torsion` | código, panel | par rechazado en una fase de la órbita y sostenido en la otra | delamor, 5 oct (REG_trace_ip, momento 14); código CP2/CP3i, 8 oct | vigente |
| "expulsión" (§11) | DEFS v7+ | otro objeto: trayectorias desde σ₀ que caen rápido en cuencas dominantes. Tampoco salen del espacio de estados | v7 | se conserva con esta aclaración |
| **operador de compresión de COCO** | DEFS v15 | `Δ_r_compresiones ← α · Δ_r_compresiones` | delamor, 5 oct: *"no hay más STOPs"* | nombre formal |
| OPERADOR_STOP_COCO, STOP, "operadorstop" | DEFS v12–v14, código, REG | el mismo operador; "operadorstop" es el apodo *"entre los íntimos"* | v12 (sep) | nombres históricos; los REG cerrados no se renombran; renombrar en el código: [delamor] |
| `MonitorService.stop_signal` | código | **otro objeto**, no leído en v15 | — | UNKNOWN |
| H_STOP, Efectividad_STOP | DEFS §12 | hipótesis | Informe v27 | conservan su nombre de hipótesis |
| Gatekeeper, portero, admitir, admisión, `admit()` | Informes v4 y v16, DEFS, código | un **juez** que dicta válida / no válida con fundamentos; no abre ni admite | abril | nombres históricos; renombrar: [delamor] |
| `count_attractors`, `_count_attractors` | código | desde `dabd1ed` (5 oct), **N_eff por órbita** (`float`); antes, estados terminales distintos (`int`) | mayo → oct | se conservan por regresión (§11, §19) |
| `d_ckm`, D_ckm, `A0`, `A_actual` | código, panel | desde `dabd1ed`, `1 − ln N_eff / ln N_eff0`; antes `(A0 − A) / A0` | mayo → oct | ídem (§10) |
| "degradado" / "expandido" | DEFS §10 | lectura agregada al signo de D_ckm; la *d* viene de una distancia | v14 | interpretación, no propiedad |
| "agregar un nodo" | varios | **Babel**: puede ser *activar* (en σ) o *incorporar* (N ± 1, en la matriz). En W estática sólo se simula: *"¿qué pasaría si…?"* | 6 oct | verbos propuestos activar/desactivar, incorporar/retirar: [delamor] |
| contagio / acoplado | delamor (IAP project) / Sonnet | contagio es una observación del proceso (algo se propaga entre devices); acoplamiento es un mecanismo (devices ligados). El cambio de palabra convirtió una observación en una explicación | IAP project | se dice *contagio*. Ninguna se valida con la serie IAP, que no se revisa |
| UNKNOWN / NOMINAL / "desconocido" | código, DEFS | UNKNOWN: estado del que observa (no se midió). NOMINAL: un valor de la escala. "Desconocido" suena a propiedad del objeto | `c06db07`, `57f8a88` | el default de lo no medido es UNKNOWN (§19) |
| `services/` | repo | una carpeta; no todo lo de adentro es servicio | 28 may | ver Modelo Conceptual |
| E1–E4, EA1–EA3, D1–D3, L1–L4 | PROPUESTA v27 | identificadores del Orden BABEL | 5 oct | **propuestos**; los prefijos no están decididos (delamor: esperar a que aparezca el patrón). Esta DEFS sigue diciendo P1–P7 |

---

## OP. Analytics global del instrumento — snapshot W y dinámico

*Sección de referencia. Cubre el instrumento en sus dos formas: W snapshot (análisis estático, P1–P4) y runtime dinámico (servicios, COCO). Cualquier afirmación en este documento debe rastrearse a una fila de esta tabla, o estar explícitamente marcada como propuesto / abierto.*

**Forma:** S = snapshot (W estático) · D = dinámico (runtime) · S+D = ambas

| Objeto | Forma | Técnica | Qué mide | Representación estructural en CKM |
|---|---|---|---|---|
| **fi** | S | Frecuencia marginal: fracción de textos donde aparece el nodo i | Presencia individual de un concepto en el corpus | Actividad del nodo — independiente de co-ocurrencia |
| **W_ij** | S | Co-ocurrencia normalizada por n_textos | Densidad de co-presencia de pares en el corpus | Campo asumido — suelo simétrico. Lo que el campo da por sentado |
| **W_ij / (fi·fj)** | S | Razón observado/esperado estadístico | Si el par co-ocurre más o menos de lo esperado por independencia | Fuerza de asociación estructural neta — lo que fi no explica |
| **c(S)** | S+D | mean(W_ij · σi · σj) sobre todos los pares i<j | Alineación del estado activo con la estructura W | Cohesión del campo — cuánto del suelo está activo |
| **r = c(S)/μ_W** | D | Normalización por peso medio del corpus, medido al inicio de sesión | Cohesión relativa independiente de escala del corpus | Señal de régimen operacional G1/G2/G3 |
| **Histeresis (P1)** | S | Rama UP (incorporación) vs DOWN (remoción) de c(S) · Wilcoxon zona crítica | Asimetría path-dependiente del campo bajo perturbación | El campo recuerda su trayectoria — el suelo no es reversible |
| **Ω* (P4)** | S | c(S) vs ρ en grid · argmax | Densidad óptima interior de W_mixta | La tensión estructural produce cohesión — no la reduce |
| **Atractores A = \|L\|** | S+D | Monte Carlo σ₀ + relajación Hopfield → estados únicos | Número de configuraciones estables alcanzables | Diversidad del landscape — estimador de \|L\| (LaSalle). Conteo no converge: crece con n_runs (sesgo coleccionista). **v15:** `count_attractors` devuelve N_eff por órbita desde `dabd1ed`; el conteo queda como `deprecated_count_attractors`. |
| **N_eff** *(implementado, landscape_engine.py)* | S+D | 1 / Σmᵢ² sobre masas de cuenca muestreadas | Diversidad efectiva del landscape ponderada por volumen de cuenca | Inverso de Simpson sobre cuencas. Rango: [1, A0]. N_eff=1 = colapso total; N_eff=A0 = equidistribución perfecta (no ocurre con W real). Convergente con n_runs≥1000 (±1–5% en casos IAP). **Reemplaza a A como estimador de diversidad en esta tabla, no en el operador**: D_ckm sigue definido sobre A, y COCO sigue disparando sobre D_ckm. |
| **D_masa_cuencas** *(implementado — `landscape_engine.d_masa_cuencas`, en panel desde `80c9c50`)* | D | 1 − ln N_eff_actual / ln N_eff_0 = [H₂(t0) − H₂(t)] / H₂(t0) | Degradación del landscape medida sobre masas de cuenca | Escala log **decidida** (delamor) e implementada: preserva el carácter información-teórico (N_eff = exp(H₂_Rényi)). Es D_contextual normalizada por H₂(t0) — ver §10. Más sensible cerca del colapso y con N_eff_0 chico; con la W corregida N_eff_0 está en 2–4, o sea operando cerca de ese borde (REG_hipotesis_distancia_contextual_v4 §5). **v15:** desde `dabd1ed`, D_ckm y D_masa_cuencas son el mismo número. |
| **node_presence** *(implementado, landscape_engine.py)* | S+D | fracción de atractores muestreados donde cada nodo está activo | Presencia de cada nodo en el espacio de atractores | Qué nodos habitan las cuencas — no su presencia en textos. |
| **d(σ)** *(implementado, landscape_engine.py)* | S+D | mínimo de flips que cambia la órbita de σ | Distancia de σ a la frontera de su cuenca | Con W corregida caso09 natural (N=20): 81% de la masa tiene d=1. Función pura, no conectada al panel todavía. |
| **D_ckm** | D | **v15:** `1 − ln N_eff / ln N_eff0` (`dabd1ed`, 5 oct). Hasta v14: (A0 − A_actual) / A0, hoy `deprecated_d_ckm` | Cambio relativo de la diversidad efectiva respecto del baseline del ciclo | Distancia del landscape a su baseline. Leerla como "degradación" es interpretación (§10) |
| **Δ_r** | D | Acumulación de pares metabolizados por el campo — quedan como deformación en W_eff. **v15:** sólo los rechazados en las dos fases de la órbita | Historia de perturbaciones del campo en runtime | Deformación acumulada del landscape |
| **órbita en el panel** *(v15, `57f8a88`)*: `periodo_orbita`, `n_aceptados`, `n_expulsados`, `n_torsion`, `pares_torsion` | D | `pares_por_orbita` sobre las fases de `relax_orbit` | Cómo se reparte cada par declarado sobre la órbita | La órbita es el objeto (§4). Sin promediar |
| **Δ_r_torsion** *(v15)* | D | Pares rechazados en una fase y sostenidos en la otra; lo escribe sólo Monitor | La parte de la perturbación que depende de la paridad | **No entra a W_eff** (CP3 1a) |
| **UNKNOWN** *(v15)* | S+D | Ausencia de medición: baseline ≤ 1, D_ckm `None`, temp_signal sin dato | Que no se midió | No es un grado de ninguna escala: no es NOMINAL ni "stable" |
| **copresence_matrix** | S+D | Pearson de co-presencia de nodos *a través de atractores únicos* | Co-movimiento de nodos en el landscape — no en textos | Geometría del espacio de atractores |
| **cluster_nodes** | S+D | Clustering jerárquico Ward sobre copresence_matrix | Grupos de nodos por co-movimiento en atractor space | Partición estructural del landscape en regiones coherentes |
| **perfect_oppositions** | S | Pares con correlación de co-presencia ≤ −0.90 | Nodos que casi nunca aparecen juntos en el mismo atractor | Candidatos a pesos negativos en W_mixta |
| **cluster_frontier_density** | S+D | mean(W_ij) intra-cluster vs inter-cluster sobre partición | Cohesión interna de cada cluster vs porosidad de su frontera | Coercitividad de frontera: min(intra_a, intra_b) / inter(a,b) |
| **W_mixta** | S | W_pos + pesos negativos en pares de frontera coercitiva | Landscape frustrado con cuencas profundas múltiples | Campo ferrimagnético — cohesión interna + resistencia de frontera |
| **Boltzmann σ₀** | S+D | Calentamiento estocástico n_warmup pasos con β_c, luego relax determinístico | Muestreo de σ₀ respetando anisotropía de W | Cobertura de cuencas por importancia — modo en `_count_attractors` |
| **β_Néel** *(propuesto)* | S | Barrido β → temperatura donde colapsa separabilidad por par de clusters | Profundidad térmica de cada frontera de cluster | Coercitividad pairwise — diagnóstico de si W_mixta tiene objeto |

**Distinciones que no viajan entre objetos:**

- fi alto ≠ nodo importante. fi alto en corpus adversarial = concepto disputado que aparece en múltiples stances por separado — no necesariamente en el mismo texto.
- Cluster (analytics.py) ≠ stance. Los clusters agrupan nodos por co-movimiento en atractor space. El número de clusters efectivos lo determina W — no el número de stances declarados en el corpus.
- Stances declarados ≠ polos del campo. Un corpus de 5 partidos puede producir 2 o 3 clusters según cuánto se solapen sus vocabularios en W.
- Coercitividad de frontera ≠ oposición binaria. Es gradiente por par de clusters. Alta coercitividad = la frontera resiste el cruce. Nada es opuesto — hay fronteras con distintos valores de resistencia.
- Mediciones estructurales viajan como mediciones. Interpretaciones de dominio no viajan.

---

# PARTE I — W ESTÁTICA: LA FOTO *(v14: MODELO ESTÁTICO, pre-servicios CKM)*

## 1. W_pos — matriz estática de co-ocurrencia

```
W_pos : N×N, simétrica (W = Wᵀ)
W_ij  = conteo_coocurrencia(i, j) / n_textos   ≥ 0
```

**W_base** = todos los pesos ≥ 0. Co-ocurrencia normalizada. Sin pesos negativos.

**Qué es W** *(v15 — delamor, 6 oct; `claude/sesion_06oct2026_definiciones_W` §1)*.
- **W es una matriz** N×N de relaciones entre pares de nodos. El valor de cada celda es el peso de la relación (en el corpus, la co-ocurrencia).
- **Un nodo no es W.** Es una fila y una columna, y tiene un estado σ_i, que por ahora es ±1. El estado vive en σ y el peso en W.
- **Lo que cambia es W**, de tres maneras —las tres causas que ya registra Monitor—: **pesos**, **N** o **nodos** (quién ocupa cada fila). **El criterio que separa los regímenes es si W cambia**, no el tipo de ingesta ni la existencia de servicios.
- **W estática = una foto.** Es un mundo simulado: sobre ella se simulan acciones y eventos (relajar, activar o desactivar nodos, agregar o quitar sobre una copia) para verificar premisas. Nada entra. **El modelo se mueve (σ); W no.** Sus premisas son **condicionales** ("si tal cosa, entonces tal otra") y se verifican simulando sobre la foto.
- **W dinámica = el mundo que se mueve.** El **corpus** ingesta (W no ingesta nada) y en el rebuild W cambia. Los eventos son reales y se observan; queda la traza.
- **Las fases (acumulación / evaluación) son del corpus, no de W.**
- **Adversarial no es un modelo:** es el signo de W, y puede aparecer en los dos regímenes.
- **Landscape** se define después, cuando estén la estática y la dinámica, como su **conjunción**, no su suma (R13: G[A∪B] ≠ G[A] ∪ G[B]). Propuesto.
- **Las cinco propiedades del Modelo Híbrido** (`docs/CKM_Modelo_Hibrido.md`: actualización local bayesiana, propagación en cadena, histéresis, asimetría agregar/quitar, modulación por densidad local) **son de W estática** (delamor, 6 oct).

*Sobre los títulos de las Partes:* la v14 decía "pre-servicios" y "servicios CKM". Ese corte es cronológico —abril contra mayo a julio—, no el criterio. La v15 titula por régimen de W y deja el título viejo entre paréntesis, como traza.

**W como suelo supuesto** (propuesto, v32): W no es lo que el campo dice — es lo que el campo da por sentado al decir cualquier cosa. c(S) mide cuánto de ese suelo está activo en un momento dado, no el suelo mismo.

**W es piecewise constant por diseño del instrumento**: CKM reconstruye W cuando el corpus cruza un umbral (`min_texts`). El campo semántico subyacente es dinámico continuo — el carácter piecewise es un artefacto del instrumento, no una propiedad del campo. El umbral `min_texts` es arbitrario (configurable: 3 en ckm_monitor, 5 en monitor_service). **No fue corregido a criterio dinámico.** (Verificado en código, Ago 2026.)

**Fase de acumulación**: antes de que el corpus alcance `min_texts`, los textos son aprobados por el Gatekeeper pero W aún no existe (o no ha sido reconstruida). En esta fase las evaluaciones del Gatekeeper no tienen W_pos contra la cual comparar — el criterio M.M no puede aplicarse en sentido estricto. La acumulación no debe modelarse como piecewise: es el estado inicial previo a la construcción de W_pos.

**Acumulación por criterio del dato (Sep 2026, verificado — REG_seleccion_nodos_desempate_v1 §4):** `min_texts` deja de ser el único criterio. Con la regla de desempate, si el dato no distingue —todo el pool empatado y sin precedente— la selección devuelve 0 nodos y el corpus **sigue en `accumulation`** hasta que el dato distinga. No es un estado nuevo: es el mismo régimen de acumulación, ahora con criterio del dato. En las 217 W reales (k ≥ 3) N = 0 no ocurre nunca.

**N deja de ser fijo (verificado, ídem §5):** con la regla de desempate, N puede superar `top_k` (empatados conservados más términos nuevos por margen) o caer por debajo. Medido: N ∈ [9, 41] con `top_k`=32; en un corpus de 7 textos, N va de 4 a 12 con `top_k`=10. Consecuencia sobre D2: un rebuild que antes se clasificaba `"nodos"` puede clasificarse `"N"`.

---

## 1.1 La rama de extracción — lo que decide qué existe antes de que haya medición

*Sección nueva (v14). NodeExtractor y `CorpusService._rebuild` deciden qué nodos y qué pares existen. Todo lo que este documento mide ocurre después de esa decisión, y durante Sep 2026 se verificaron cuatro condiciones de esa rama. Las tres primeras son del instrumento; la cuarta es del dato.*

**a) Pares por texto entre nodos globales** *(corregido — `5aa3504`, REG_hipotesis_distancia_contextual_v4 §1–§2)*. `_rebuild` hacía **dos** extracciones: una global para elegir los N nodos, y otra **por texto** para rutear pos/neg — con su propio TF-IDF y su propio `top_k` dentro de ese único texto. Si un texto tenía más de `top_k` términos distintos, nodos globales quedaban fuera del top de ese texto y sus pares se perdían.

| caso09, bootstrap 12 | global | lo que entraba a W |
|---|---:|---:|
| pares distintos | 299 | 161 — **46% perdidos** |
| co-ocurrencias | 425 | 189 — **55% perdidas** |

Corregido: `accumulate` devuelve `pairs_by_text` entre nodos globales y `_rebuild` rutea con eso, sin re-extraer. **Cambia todas las W construidas por CorpusService.** Lo medido antes vale en su marco.

**b) Nodos aislados** *(REG_hipotesis_distancia_contextual_v3 §2, v4 §2)*. Un nodo aislado tiene su fila de W entera en cero: su campo local es siempre 0, conserva su valor, y con `a` aislados cada atractor acoplado aparece en **2^a copias triviales** — infla A sin que el paisaje cambie. Frecuencia sobre 217 W de 15 corpus: **52% antes de la corrección, 4% después** (máx. 1). Los que quedan no co-ocurren con ningún nodo en sus textos: **aislamiento del dato, no del instrumento**. El factor 2^a se cancela en D_ckm y en D_masa lineal, **no** en D_masa log, y además **no es constante durante un run**: Δ_r acopla en W_eff nodos que W tenía aislados (v3 §4).

**c) σ por una sola rama** *(corregido — `7bf485b`, REG_hipotesis_distancia_contextual_v4 §7)*. `evaluate` construía σ_prompt por substring mientras W se construía con el analizador de `accumulate`: dos criterios distintos de "el nodo está en el texto". Con W idéntica (mismo sha), unificar la rama quitó 140 pares metabolizados, y **139 de esos 140** involucraban un nodo que sólo el substring activaba (`here` dentro de "w**here**", `one` dentro de "some**one**"). ~100% del cambio. Arrastre: las lecturas de D_ckm previas a la unificación incluían metabolización de nodos que el texto no nombraba.

**d) Stopwords e idioma** *(REG_unidad_texto_saturacion_v1 §4.3, verificado, **no corregido**)*. `_STOPWORDS` es la unión NLTK-es + NLTK-en + sklearn-en, y la unión **suma los falsos positivos de las tres listas en vez de compensarlos**. `estado` —el nombre del objeto central del modelo, σ— se elimina porque NLTK-es lo lista como participio de *estar*. En texto mezclado el concepto se parte asimétrico: en caso13, `estado` (3 ocurrencias) se descarta y `state` (7) queda como nodo, de modo que el nodo lleva 7 de 10 ocurrencias reales sin que eso quede declarado. Y en el extremo: **una palabra de un prompt de configuración decide qué existe en el campo** — `trazable` (la única no inglesa de los tres prompts de caso13) hizo que TinkerBellucio escribiera su mapa entero en castellano; ese texto, el más largo del corpus (1043 palabras), activó 3 de 32 nodos y aportó 3 de 496 pares. W no contiene el mapa: contiene la conversación en inglés sobre el mapa.

**d.1) Nunca hubo mapeo de nodos en corpus bilingüe — abierto hasta hoy** *(v14, delamor)*. `day` y `día` son el caso limpio: un solo concepto, dos grafías, y para el extractor **dos términos que compiten por el top_k**. Ninguno de los dos es el concepto; cada uno lleva la mitad de sus ocurrencias, y si una de las mitades no llega al corte, el concepto entra con el peso de la otra. `estado` / `state` es el mismo problema con una capa más encima, porque ahí además una de las dos mitades la borra una lista de stopwords. **No existe una capa que una las grafías, y no se intentó.** Mientras no exista, en todo corpus mezclado el concepto entra partido, y el desbalance no queda declarado — agravado por lo de arriba: como las listas de stopwords no borran lo mismo, una mitad del concepto puede desaparecer y la otra sobrevivir como nodo.

**d.2) Familia de palabras: probado, sin efecto** *(v14, delamor)*. Agrupar variantes morfológicas en familias de palabras **se probó y no cambiaba la prueba ni sus resultados**. Queda registrado para que no se vuelva a intentar esperando que resuelva lo anterior: **es otro problema**. La familia de palabras une variantes de un mismo término; el mapeo bilingüe une términos distintos de dos idiomas. Resolver el primero no toca el segundo.

**e) Saturación de pares distintos** *(REG_unidad_texto_saturacion_v1 §3, §4)*. La cantidad que ordena el colapso del paisaje no es la densidad de W ni la tensión, sino cuántos de los pares posibles **nunca ocurren**. Con `top_k`=32 hay 496 pares posibles; de página-40 en adelante ya ocurren 451–495, y el paisaje colapsa a N_eff ≈ 2 (régimen G2, §13). Por unidad "versión" ocurren los 496: N_eff = 1.00, y los 27 ceros que quedan son **cancelaciones** (el par ocurrió en ambos signos), ninguno ausencia — con lo cual el 0 de W pasa a nombrar dos objetos distintos que el relax no puede distinguir. **caso09 es el único corpus no saturado de los medidos (307/496, 62%)**; caso13 llega a 88% y caso14 a 99%.

**f) El criterio de extracción no deja huella** *(v15 — FICHAS §5, leído en el código el 7 oct)*. El estado JSON de `CorpusService` lleva `n_nodes`, `min_texts`, `w_sha` y `rebuild_suspendido`, pero **no** el criterio con el que se extrajeron los nodos: `top_k`, `ngram_max`, el conjunto de stopwords (sin versión ni hash), `token_pattern`, `TOL_EMPATE` y la regla de desempate. Dos W con el mismo `w_sha` se pueden comparar; dos W extraídas con criterios distintos **no se distinguen en la traza**. El criterio es la mano que señala, y hoy no deja huella. Va a `NodeExtractorConfig` (delamor, 8 oct). No implementado.

*Estado: (a) y (c) verificados y corregidos; (b) frecuencia verificada; (d) verificado, no corregido; (e) verificado como medición, criterio propuesto; (f) verificado en código, decidido, no implementado.*

---

## 2. Δ — matriz de orientación (corpus estático)

```
Δ : N×N, asimétrica
Orientación direccional derivada del corpus
```

Usada por el Gatekeeper (criterio M.M, C3). **El Gatekeeper evalúa contra W del momento de ingesta** — que a partir del primer nodo admitido es siempre **W vieja**: la última versión construida antes del texto actual. W_mixta es "actual" exclusivamente hasta el primer ingreso; desde t>0, la evaluación es siempre contra una snapshot previa al texto evaluado.

Si W no ha sido construida aún (fase de acumulación), M.M no tiene referencia. **Δ estático ≠ Δ_r**.

*Desfasaje — abierto, prioridad baja: W vieja es condición permanente de operación.*

*Cuándo ocurre rebuild (verificado en corpus_service.py y ckm_monitor.py):*
- *Automático: `ingest()` llama `_rebuild()` cuando `len(texts) >= min_texts` — criterio de volumen.*
- *Estructural: `should_rebuild(d_ckm_history, n=3)` — implementado. El orquestador es `CKMMonitor.on_message()`, que mantiene `_d_ckm_history` y evalúa la jerarquía (estructural > volumen > tiempo) en `_last_rebuild_signal`. El comentario en el código lo precisa: "señal observable — no fuerza el rebuild todavía". `_last_rebuild_signal` es informacional, no ejecutiva.*
- *Suspendido: `rebuild_suspendido=True` (`e1980e0`) congela W tras el primer build — `ingest` sigue acumulando textos y no reconstruye. Existe para que la W quede fija por decisión declarada y no por omisión; se serializa en el estado. (v14)*

---

## 3. c(S) — función de cohesión

```
c(S) = mean(W_ij · σᵢ · σⱼ)  sobre todos los pares i < j
     = −E_Hopfield / (N(N-1)/2)
```

**La herramienta vs. el uso (distinción crítica):**
- Primera línea: nombra la herramienta — la función de energía Hopfield, tomada como formalismo computacional.
- Segunda línea: nombra el uso en CKM — medir la alineación entre estado σ y la estructura de pesos W.

**CKM maximiza energía — lo opuesto a Hopfield:**

```
Hopfield: minimiza E(S)
CKM:      maximiza c(S) = −E(S)/C(N,2)
```

La relación formal:

```
E(S(t+1)) < E(S(t))    →    c(S(t+1)) > c(S(t))
```

Cuando la energía decrece (relajación Hopfield), la cohesión crece. La dinámica Hopfield es el motor; CKM lee el resultado en la dirección opuesta.

**Función analítica unificada** (verificado, v27 — cierre de H1/H2/H3):

```
c(S)*(N, ρ_corr) = μ_W(N, ρ_corr) · r(zona, ρ)
```

Donde `μ_W` escala con composición del corpus y `r` es el factor de alineación medible en tiempo real. Los tres HOLDINGs H1/H2/H3 son proyecciones observables de esta función, no límites independientes.

---

## 4. Dinámica de relajación — dos implementaciones distintas

### hopfield.py — asincrónica (usada en P1–P4)

```
Para cada paso:
    i = nodo aleatorio (uno por vez)           ← selección uniforme
    h_i = Σⱼ W_ij σⱼ
    σᵢ ← +1 si h_i > 0, −1 si h_i < 0, σᵢ si h_i = 0
```

Aplica funciones de activación Hopfield sobre W_pos. Selección de nodos según distribución uniforme. Garantiza convergencia a mínimo local de energía. Sin ciclos. Sin aprendizaje Hebbiano.

**Garantía formal de convergencia — Lyapunov/LaSalle:**

Con W simétrica y actualización asíncrona, la función de energía de Hopfield

```
V(σ) = −½ σᵀWσ
```

es una función de Lyapunov del sistema. Cada actualización asíncrona satisface dV ≤ 0 en cada paso. El conjunto invariante máximo L en Z = {σ : dV = 0} son exactamente los mínimos locales de V. Por el Teorema de Invarianza de LaSalle, toda trayectoria acotada converge a L.

Consecuencia operativa: con actualización **asíncrona** y W **simétrica**, los ciclos de período 2 son **imposibles**. `relax()` devuelve siempre un elemento de L — un mínimo local de V. Antes implícito en el código; ahora formalmente garantizado.

*Fuente: Agama Santiago, M. "Análisis de estabilidad de las redes neuronales de Hopfield utilizando funciones de Lyapunov y el Teorema de LaSalle." Licenciatura en Matemáticas Aplicadas, UTM Mixteca, 2026. §2 (Lyapunov/LaSalle), §4.1 (función de energía Hopfield como Lyapunov), §4.3 (atractores como mínimos de V).*

**Qualifier**: P1–P4 son válidas bajo relajación asincrónica con *(v15: se lee "se midieron bajo"; su estado está en §5)*:
- Selección de nodos según distribución **uniforme**
- **Seed = 42 fija** — para permitir comparación entre corridas
- **n_runs**: no hay problema del coleccionista de cupones. P1–P4 no cuentan atractores por muestreo aleatorio — miden c(S) a lo largo de trayectorias deterministas, distribución de cascadas estructurales, asimetría temporal, y posición de Ω*. No hay D_ckm. El sesgo coupon-collector aplica a `_count_attractors` (P5, COCO) — no a estos experimentos.

### landscape_engine.py → relax_orbit — sincrónica (usada en servicios, P5)

```
relax_orbit(sigma, W_eff, max_iter=200):
    detecta órbita exacta (período 1 o 2)
    tiebreak GOLES: conserva σ cuando h=0
    devuelve (sigma_final, period, steps, estado_seleccionado)
Cap: max_iter = 200
```

**max_iter = 200: abierto.** No hay análisis de por qué 200 es suficiente (o insuficiente) para W_mixta con frustración.

**Ciclos de período 2 — estabilidad orbital, no deficiencia (v8):**

El modo sincrónico puede producir ciclos de período 2. Esto no es inestabilidad — es **estabilidad orbital** (atractor de ciclo límite). El sistema es acotado (2^N estados posibles), determinista y perfectamente predecible. La función de energía Hopfield estándar puede aumentar (ΔE > 0) entre pasos sincrónicos, pero el sistema converge a M = conjunto de órbitas de período 2, no diverge. Calificar de defectuoso al modo sincrónico por no producir punto fijo es un error de nomenclatura: confunde estabilidad de punto fijo con estabilidad del sistema.

Tres regímenes de convergencia:

| Modo | Conjunto invariante M | Tipo de estabilidad |
|---|---|---|
| Asincrónico | Mínimos locales de V (puntos fijos) | Estática |
| Sincrónico estándar | Órbitas de período 2 | Orbital / periódica |
| Sincrónico modificado (pesos asimétricos / activación no lineal continua) | Atractor extraño | Global acotada, local caótica |

**LaSalle sincrónico:** con W simétrica y diagonal cero, mapeada bajo función de Lyapunov adaptada para ejecución sincrónica, el cambio de energía total entre pasos sucesivos está acotado estructuralmente. LaSalle garantiza convergencia a M. No es la garantía del modo asincrónico (M = mínimos locales de V) — es una garantía distinta sobre un objeto distinto: M = conjunto de órbitas de período 2. En ningún régimen el sistema colapsa numéricamente.

*Fuente: convergencia orbital — teorema de invarianza de LaSalle (estándar, ver Agama Santiago 2026 para la derivación formal). Aplicación al instrumento CKM: Predictibilidad_orbital.md — gadanin.delamor, Sep 2026.*

**Consecuencia operativa para `_count_attractors` — resuelta por GOLES:** `relax_orbit` detecta la órbita completa. Cuando h=0 el nodo conserva σ (regla "conserva σ" — garantiza determinismo: misma W, mismo σ₀, mismo seed → siempre el mismo estado terminal). La regla es premisa requerida del instrumento: sin ella, dos corridas desde σ₀ similares pueden devolver A o B de la misma órbita de período 2, contadas como dos atractores distintos. Con la regla: determinístico. *Verificado: REG_seleccion_nodos_desempate_v1 §2, REG_orbitas_conjuntos_invariantes_v1.*

**Prevalencia de órbitas — verificada y dependiente del corpus** *(corregido en v14)*. La misma tabla de REG_orbitas §2 da los tres números:

| corpus | N | trayectorias que quedan en órbita |
|---|---:|---:|
| WARMUP_TEXTS | 20 | 141/200 — **70.5%** |
| caso09 natural | 20 | 136/200 — **68%** |
| `W_ckm_corpus_v2` | 32 | 3/200 — **1.5%** |

El "~70%" vale para esos dos corpus N=20, **no para el corpus operativo del proyecto**, que es N=32 y da 1.5%. Versiones anteriores lo enunciaban como *"corpora operacionales"*, que suena general y no lo es. Velocidad: 87× vs relax sin detección de órbita (REG_orbitas_conjuntos_invariantes_v1 §1).

**La órbita es el objeto** *(v15 — TASK_monitor_coco_ciclo_orbita_v2, CP0 a CP2)*. Toda medición dentro del ciclo se hace sobre la **órbita completa** —las dos fases, sin orden, como el `frozenset` de `relax_orbit`—, no sobre la fase que cae en `max_iter`.
- **La paridad pesa.** En caso09, 16 de 24 textos terminan en período 2, y medir una fase u otra da L1 = 24.0 (CP1, `045005b`). La expectativa de Code, escrita antes de correr, decía lo contrario; lo declaró.
- **Precisión de la invariante.** "Punto fijo ⇒ R_A = R_B" vale **a igual W_eff**, no a lo largo de un recorrido: la divergencia se compone porque Δ_r entra a W_eff.
- **Identidad demostrada** (CP0): `relax(−σ) = −relax(σ)`. La bisagra es GOLES (h = 0 conserva σ).
- **Torsión:** el par rechazado en una fase y sostenido en la otra. Es la marca del período 2 sobre los pares (§9, §N).

**Consecuencia verificada**: P1–P4 (hopfield.py, async) y P5 (COCO, sync) usan instrumentos distintos con garantías distintas. Sus resultados no son directamente comparables en términos de dinámica de relajación.

---

## 5. P1–P4 — predicciones del modelo estático híbrido *(v14: Bootstrap formal del modelo estático)*

*(v15 — reescrita; pedido de delamor: "redactalo, incluilo en la v15". La v14 decía **verificado** en las cuatro. Esa tabla se conserva al final de esta sección, entera, como traza: es el suelo desde el que se vio lo que sigue. **No se rotula de error.** Lo que cambió no es el modelo: es lo que se sabe de las condiciones en que se midió. Newton: para negar el suelo hay que pararse sobre él.)*

**Qué son.** Las cuatro predicciones falsables del Modelo Híbrido (`docs/CKM_Modelo_Hibrido.md`, abril 2026: Hopfield + k-core + BP sobre una W). En el Orden BABEL propuesto son E1–E4; como los prefijos no están decididos, esta sección sigue diciendo P1–P4.

| # | Predicción | Estado v15 | Plano | Por qué |
|---|---|---|---|---|
| P1 | c(S) exhibe histéresis: incorporar ≠ remover | **no testeable sobre una W snapshot con W ≥ 0** | matemático | Con W ≥ 0 no hay frustración: σ = todo +1 es mínimo global y absorbente, y la rama DOWN no puede salir de ahí. Medido: `m_down ≡ 1.0` exacto en 3 corridas sobre `W_ckm_corpus_v2.json` (N = 32, cero negativos). **Una rama constante no es una rama.** |
| P2 | Cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2] | **no medible con N = 32** | experimental | Menos de 10 cascadas de tamaño ≥ 2 por grafo; el rango no llega a 1.2 décadas. La condición N (`CKM_experiments_correct_N.md`) pide k ≥ 3 y N de 50 a 100 o más |
| P3 | Asimetría temporal: remover relaja más lento que incorporar | **no testeada** | matemático | La forma k-core sobre un grafo fijo es reversible por construcción —el k-core es único—: lo que la remoción poda, la re-adición lo recupera en orden inverso. El test no puede fallar en la otra dirección. La versión con tiempos de relajación no se corrió |
| P4 | W_mixta tiene densidad óptima interior Ω* | **no testeable con subconjuntos al azar** | matemático | Por linealidad, E[c(S)] = media(W)·g(ρ), con g igual para todo par: **Ω* interior ⇔ media(W) < 0**. Con W ≥ 0, ρ* = 1.0 siempre. Verificado con el operador (W_ckm_corpus_v2 + pares −0.10 **al azar**): 20 pares → media +0.00035 → ρ* = 1.0; 30 → −0.00180 → 0.509; 60 → −0.00742 → 0.541. Decide el signo de la media, no dónde están los pares. El ρ* ≈ 0.509 reportado en N = 64 es consistente con esto |

**Una sola premisa cierra P1 y P4.** `force_w_pos=True` decide las dos respuestas antes de correr. No son dos propiedades mal medidas: es **una premisa medida dos veces**. **Y tres de las cuatro piden tiempo** —P1 historia, P2 propagación, P3 flecha temporal—, que un snapshot no tiene. Lo único que un snapshot contesta es de la forma de P4, y eso es aritmética de media(W).

*Fuentes:* `P1P4/BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1.md` (5 oct; **borrador**, fuera de `registers/`, entra con el OK de delamor); el candado `experiments/CERRADO_LEER_ANTES_ckm_p1p4_module.md` (`eddb4b0`); `P1P4/INFORME_verificacion_P1_P4_v2.md` (4 oct); `P1P4/OBS_P1_run_P1_y_coercitividad_04oct_v1.md` §6. El paper v27 ya lo sigue (§5.2).

**Lo que no dice.** No dice que P1–P4 sean falsas. Dice que una W snapshot no negativa **no es condición para preguntarlo**. Cierra P1 y P4 sobre W_pos snapshot; **no cierra P1–P4 como propiedades del Modelo Híbrido**.

**Conciliación con la verificación del 4 oct** *(Opus, v15 — quedó como tensión el 5 oct: "conciliar `eddb4b0` con la PROPUESTA v27")*. El INFORME_verificacion_P1_P4_v2 (4 oct) dio P1 "verificada como propiedad del modelo, con relajación". El 4 oct y el 5 oct **no se contradicen: son los mismos datos leídos dos veces.**
- El 4 oct ya registraba que la rama DOWN se queda en m = 1 —remanencia total— y que *"cualquier W positiva lo produce"*: los nulos daban entre 0.25 y 0.31.
- El 5 oct midió que `m_down ≡ 1.0` es exacto, y que el estadístico es A = 1 − media(m_up) a cuatro decimales (0.3172 / 0.3040 / 0.3078). **A no es área de lazo: es cuánto le falta a la rama UP para saturar.**
- **Lo que sí se sostiene del 4 oct es una medición sobre la rama UP:** en `W_viejo` (la W del paper) la estructura del corpus retrasa la saturación más de lo que explica la fuerza de cada nodo (nulo N_fuerza, p < 0.005; pasa Bonferroni sobre 4 comparaciones). En `W_nuevo` (informes por párrafo, CorpusService actual) el efecto es débil (p = 0.045; no pasa). **Es una propiedad de la rama UP, no histéresis.**
- El veredicto "P1 verificada" del 4 oct queda como traza. La PROPUESTA v27 (E1 "verificada") todavía no sigue al 5 oct.

*Esta conciliación es lectura de Opus, y espera la de delamor.*

**De dónde venía el "verificado".** Los números de abril (`readme/EXPERIMENTS.md`, Informe v32 §64.4) se produjeron con `exp_p1_histeresis.py` y `ckm_viz_v1.py`, que **nunca entraron al repo** (`find` sobre todo el árbol y `git log --all --diff-filter=A` sobre todas las ramas, 5 oct). `experiments/ckm_p1p4_module.py` **no es lo que midió**: es una reconstrucción posterior, y nada lo marcaba como tal. Sus tests no podían fallar en la dirección que importa (`except: pass` → INSUFICIENTE → pasa; `add_steps.append(0)` fijo; "CONFIRMADA si algún θ cae en [1.5, 2]"; ramas UP/DOWN intercambiables). El ciclo de reverificación se repitió cuatro veces porque **"no testeada" no cierra nada**, y no había REG que lo cerrara. Nada de eso hace falsa la tabla de abril: sin ella no se habría visto la premisa que decide las dos respuestas.

**Lo que queda abierto, y es otra pregunta: P1–P4 sobre W dinámica.** Las mismas cuatro, sobre una W que evoluciona. Ahí la frustración puede **aparecer de la dinámica** en vez de ponerse a mano con una W_mixta: la regla de Aiyappa, Flammini & Ahn (2024), Δb ~ N(α·b_emisor + β·b_y·b_z, σ²), tiene un término triádico que genera pesos de los dos signos (§20). Antes de escribir una línea de código:
1. **Comparabilidad de ramas.** Con W móvil, la W al final del UP no es la del arranque del DOWN, y parte de cualquier lazo sería eso. Declarar antes qué se fija y qué corre.
2. **Literatura.** La histéresis en Hopfield **con aprendizaje** puede estar publicada. Si lo está, es replicación declarada, no hallazgo.
3. **Citar a Aiyappa de frente**, con repo y commit: `rachithaiyappa/beliefnet` @ `2289c39`.

No hay resultado de abril al que llegar; la TASK se escribe de cero. **Sin identificador** hasta que se formulen como premisas propias de W dinámica (Orden BABEL, regla 3: una premisa no cruza modelos). **[delamor]**

**Lo que decía la v14** *(traza, sin cambios)*:

> P1–P4 son el **bootstrap formal de CKM**: las predicciones que establecen que el modelo tiene las propiedades estructurales necesarias para ser válido en su dominio. No son el propósito del proyecto — son su fundamento. Sin P1–P4 verificadas, el instrumento no tiene base formal.
>
> Algunas predicciones tienen demostración matemática directa; otras son verificadas empíricamente. La distinción importa:
>
> | # | Predicción | Estado | N | Fundamento |
> |---|---|---|---|---|
> | P1 | c(S) exhibe histeresis macroscópica: incorporar ≠ remover | **verificado** | 16, 32, 64 | Lyapunov + path-dependencia en paisaje de energía |
> | P2 | Distribución de cascadas P(s) ∝ s^−τ, τ ∈ [1.5, 2] | **verificado** | 32, 64 | k-core percolation |
> | P3 | Asimetría temporal: remoción relaja más lento que incorporación | **verificado** | 32, 64 | Consecuencia matemática de histéresis P1 |
> | P4 | W_mixta tiene densidad óptima interior Ω* | **verificado** N=32; parcial N=64 | 32, 64 | Frustración en paisaje ferrimagnético |
>
> Validadas sobre W_pos estática con hopfield.py (asincrónico) + k-core percolation + Belief Propagation. Sin aprendizaje Hebbiano. Sin servicios CKM.
>
> **P4 N=64**: Ω* interior existe (ρ*≈0.509). W_mixta no supera W_base en zona [0.5–0.8] a N=64. Causa: dilución por nodos tipo B — ver §7.
>
> **Condición de validez — W_pos estática únicamente:**
> P1–P4 son propiedades de W_pos estática tal como fueron formuladas. Evaluarlas sobre W dinámica (W_eff, W reconstruida tras rebuild, W en evolución) no es verificar P1–P4 — es aplicar el mismo instrumento sobre una snapshot de W dinámica. Esa nueva evaluación corresponde a P8 o posterior.

---

# PARTE II — EL SIGNO DE W: OBSERVACIONES EN CORPUS ADVERSARIAL (dominio acotado) *(v14: OBSERVACIONES EN CORPUS ADVERSARIAL)*

## 6. P5–P7 — Observaciones en corpus adversarial externo (dominio muy acotado)

**Relevancia para el proyecto: baja.** P5–P7 son observaciones que emergieron al aplicar el instrumento CKM sobre corpora de debate adversarial externo (CreateDebate gun control, FourForums gun control). Son derivados del uso del instrumento, no propósito del proyecto.

**Dominio de validez estricto**: corpus adversariales de postura fija. No son características generales del modelo CKM. No son propiedades del modelo — son comportamientos observados en un tipo de corpus muy específico. No verificable que este escenario sea frecuente ni representativo en el dominio de interacciones entre devices bajo M.M.

El dominio de CKM son interacciones entre devices — con sus respectivos VPs, no reducibles a polaridad binaria. El trabajo IAP (Sonnet + Code + delamor) opera con al menos 3 stances distintos. delamor es participante con VP propio, no árbitro de desempate entre dos polos. P5–P7 no generalizan al dominio principal.

*(v15)* **Adversarial no es un modelo: es el signo de W** (delamor, 6 oct), y puede aparecer en los dos regímenes. Esta Parte se conserva como dominio acotado. **Babel entre documentos:** la v14 las llama *observaciones* de relevancia baja; la PROPUESTA v27 las llama *predicciones* EA1–EA3 de una "extensión adversarial del estático". No se resuelve acá: **[delamor]**. **En fourforums los nodos son autores**, no términos: la W del paper es relacional (`SKIP_TABLES` incluye `'text'`; REG_salamanca_s1_v1 §3). P6 se midió sobre esa W. Ninguna W_mixta se verificó contra nulo (§8).

| # | Observación | Estado | Corpus |
|---|---|---|---|
| P5 | Corpus adversarial colapsa diversidad de atractores (A ≈ N/2) | **verificado** en ese corpus | fourforums, N=32 |
| P6 | Δ predice flujo direccional para estados ambiguos | **verificado** en ese corpus | fourforums + CreateDebate |
| P7 | Campo con tensión estructural genuina contiene nodo tipo-965 | **observado** en 2 corpora; universalidad **abierta** | — |

**P5** usa `_count_attractors` de COCO (relajación sincrónica) — instrumento distinto a P1–P4.

**P6**: T0 cita T1 a 2.18× frecuencia. T1 cohesión interna 3.05×. Verificado en W_asim_v8h.

**P7 y triadas**: Del análisis de P7 emerge la estructura de triadas — antecedente del criterio de selección de pares negativos en W_mixta. Esa conexión sí es relevante al modelo; la observación del nodo tipo-965 como derivado es lo que tiene alcance acotado.

**Nodo tipo-965**: ratio in/out > 455× (paper). *Verificar valor correcto en corpus actual — REG menciona > 100×.*

---

# PARTE III — W DINÁMICA: EL MUNDO QUE SE MUEVE *(v14: MODELO DINÁMICO, servicios CKM)*

## 7. Estructura bimodal A/B y función unificada

Análisis de distribución de frecuencias marginales en N=32 (CV=0.944, razón max/min=102×):

| Grupo | Nodos | fi | Pares |
|---|---|---|---|
| A | 16 | ≥ 0.064 | núcleo correlacionado |
| B | 16 | < 0.064 | nodos tardíos / baja densidad |

*Nota (Sep 2026) — **corregida en v14**: la partición A/B de arriba (CV=0.944, max/min=102×) **no se reproduce midiendo `W_ckm_corpus_v2.json` directamente**: da CV=1.08, max/min=68.6×, mediana 0.020, y sólo 5 nodos con fi ≥ 0.064 en vez de 16. Esa medición es de `TASK_gatekeeper_C1_theta_W_v1` (acuerdo 4, commit `f8d61ef`) y es **anterior** a la corrección de extracción de pares (`5aa3504`), así que la discrepancia no es efecto de esa corrección — v13 se la atribuía. La causa no está identificada: los candidatos son otra definición de fi (`para_counts` contra fracción de textos), otro corpus de origen, u otra versión del JSON. **Abierto.***

*Lo que sí depende de `5aa3504`: toda W construida por `CorpusService` cambió (§1.1a). Si `W_ckm_corpus_v2.json` fue construida por ese camino, la partición requiere recalibración; si vino de otro pipeline, no. No verificado. Los experimentos P1–P7 se verificaron sobre el JSON tal como está — válidos en ese marco.*

| Par | μ_W obs | mean(fi·fj) | ratio | derivable |
|---|---|---|---|---|
| BB | 0.000523 | 0.000510 | 1.025 | ✓ (nodos B ≈ independientes estadísticos) |
| AA | 0.016122 | 0.065599 | 0.246 | ✗ (núcleo correlacionado internamente) |
| AB | 0.000952 | 0.005933 | 0.160 | ✗ |

**Cierres operativos** (verificado, v27):
- **H3 cerrado**: μ_W no generaliza entre N porque cambia la proporción A/B, no N per se.
- **H2 cerrado**: dilución P4 en N=64 es consecuencia de agregar nodos tipo B (μ_W → 0).
- **H1 cerrado**: α_c = 0.138 asume patrones no correlacionados. Con núcleo A correlacionado, la capacidad efectiva depende de composición A/B.

---

## 8. W_mixta — ferrimagnética

W_pos con pesos negativos asignados intencionalmente a pares en tensión estructural. Peso negativo: w_neg = −0.10 (configurable).

**Ferromagnética (W_pos)**: todos los nodos tienden al mismo atractor. Sin resistencia.
**Ferrimagnética (W_mixta)**: fondo ferromagnético + pares negativos selectivos en frontera T0/T1. Momento resultante no se cancela. Múltiples atractores con cuencas pequeñas y profundas — característica de sistemas frustrados.

**W_pos y W_mixta pertenecen a regímenes cualitativamente distintos.**

**Build de W_mixta — marcadores de oposición (corpus_service.py v2):**
Cada texto es ruteado por presencia de marcadores de oposición (_OPPOSITION_MARKERS, ES+EN). Sin marcador → pares suman a pos_counts. Con marcador → pares suman a neg_counts.

```
W = (pos_counts − neg_counts) / max(|pos − neg|)
Rango: [−1, +1]
```

**Precondición de dominio** (REG_unidad_texto_saturacion_v1 §5, decidido): el ruteo por marcadores léxicos asume que el corpus fue elicitado con posiciones que se oponen por diseño. En corpus de autor único o de coordinación (canal IAP, informes de trabajo), los mismos marcadores ("pero", "sin embargo") son conectores discursivos — no oposición estructural. Los pares negativos resultantes no miden tensión: miden la procedencia léxica del marcador. **Ninguna W_mixta del proyecto fue verificada contra nulo**: el procedimiento `_has_opposition(text)` siempre encuentra algo en textos suficientemente largos — no tiene salida nula. Consecuencia: todas las W_mixta construidas hasta la fecha están sin contrastar, no mal medidas. Néel y SALAMANCA (§15, §16) son el criterio propuesto para verificar si un corpus tiene estructura adversarial antes de aplicar el ruteo. *(v15: SALAMANCA S1 se corrió y lo que detecta es **modularidad, no adversarialidad**; Néel no está corrido — §16.)*

`force_w_pos=True`: flag de desarrollo únicamente — saltea el ruteo, todos los pares van a pos_counts. La W resultante queda marcada en traza (`causal_event=rebuild_debug_force_w_pos`). No es estado alcanzable en operación normal. Sirve para verificar el instrumento en el contrafáctico exacto: mismo corpus, sin codificar su tensión.

**Calibración W_mixta — build y rebuilds (v9):**
D_CKM_THRESHOLD (0.40 default) debe calibrarse contra W_mixta, no contra W_pos. Condiciones:
- **Build inicial**: calibrar D_CKM_THRESHOLD al construir W_mixta por primera vez.
- **Cada rebuild**: recalibrar cuando W_mixta se reconstruya (corpus supera umbral min_texts). El piso estructural de W_mixta cambia con N y composición A/B — una calibración de build inicial no es válida para rebuilds en corpus distinto.
- **Consecuencia de no recalibrar**: asimetría documentada en §10 — piso estructural W_pos (0.632) > umbral (0.40) → COCO sin efecto práctico. La calibración obsoleta deja el instrumento ciego al campo que opera.
Estado: pendiente de implementación. *(v15: va a Calibración, que todavía no existe. El 0.40 además es de la escala lineal de D_ckm, que cambió — §10.)*

Diferencias estructurales entre Aiyappa et al. 2024 y CKM — no reducibles a W_mixta:

1. **Uso de arquitectura Hopfield**: CKM maximiza energía sin regla de aprendizaje de patrones. Estudia diversidad del landscape — no recuperación de memorias.
2. **Δ — matriz de orientación**: asimetría direccional como objeto separado y estrictamente separado de W. Sin equivalente en Aiyappa et al.
3. **Régimen de spin glass frustrado**: CKM opera en intervalo crítico, no en punto crítico — frustración sostenida como condición de operación, no transición puntual.
4. **W_mixta**: pesos negativos selectivos en pares de oposición estructural.

*(v15 — réplica de la Fig. 5, §20: en Aiyappa cambian los pesos; en CKM, sobre una W, cambian los estados. La energía de Aiyappa es triádica (Heider); la de CKM, por pares (Hopfield). Pariente, no gemelo.)*

**Separación estricta de capas** (verificado): mezclar W y Δ destruye capacidad (0.78 → 0.02).

---

## 9. Δ_r — acumulador de metabolización (runtime)

```
Δ_r_pares   : N×N, simétrica por construcción (Monitor, monitor_service.py L112-114)
Δ_r_compresiones : N×N, objeto propio de COCO (coco.py, desde D3 — Sep 2026)

W_eff_monitor = W + Δ_r_pares     ← lo que Monitor relaja y mide
W_eff_coco    = W + Δ_r_compresiones  ← lo que COCO regula
```

**D3 implementado (Sep 2026):** `Δ_r_pares` es de Monitor — nadie escribe en él excepto Monitor. `Δ_r_compresiones` es de COCO — historia de compresiones por ciclo de vida, objeto distinto. OPERADOR_STOP_COCO opera sobre `Δ_r_compresiones`, no sobre el estado de Monitor. La ceguera de D_ckm_monitor a las compresiones de COCO es propiedad del diseño por separación de objetos — no cancelación algebraica.

**Nota**: Δ_r es simétrica, no asimétrica. El par (i,j) nunca se genera sin (j,i) — la simetría es forzada en la acumulación. Esto la distingue de Δ (estática, asimétrica). **Δ estático ≠ Δ_r**. Son objetos distintos con roles distintos.

**v15 — qué entra a `Δ_r_pares`** (delamor, 8 oct, CP3 1a; `ef1bc33`, `monitor_service.py` L218–L240). **Sólo los pares rechazados en las dos fases** de la órbita (§4; en el código, `expulsados` — §N). `Δ_r_torsion` —los rechazados en una sola fase— es un objeto propio, de Monitor, y **no entra a W_eff**. Los dos se acumulan en las dos direcciones, así que la simetría se conserva por construcción. `rechazados` y `n_rejected_pairs` siguen saliendo de la fase que cae en `max_iter`, sólo para que los paneles sean comparables con los históricos.

```
W_eff_monitor = W + Δ_r_pares        ← sólo rechazados en las dos fases
Δ_r_torsion   : N×N, simétrica, de Monitor — no entra a W_eff
```

**Ciclo de vida.** Al cambiar W, Monitor descarta Δ_r y abre un ciclo nuevo en la Config; COCO renace con él con Δ_r en cero, así que **W_eff = W al nacer** (§12). Las líneas citadas arriba (L112–114) son de septiembre: el código cambió de lugar.

---

## 10. D_ckm

**v15 — la fórmula cambió** (`dabd1ed`, 5 oct; `registers/REG_d_ckm_formula_canonica_v1.md`; decidido por delamor el 4 oct):

```
D_ckm = 1 − ln N_eff / ln N_eff0          N_eff = 1 / Σ m²   (m: masas de cuenca por órbita)
```

- La forma lineal `(A0 − A) / A0` **deja de ser lo que calculan Monitor y COCO**. Queda en el engine como `deprecated_d_ckm`, y nada en `services/` la llama.
- **Los nombres se conservan** (`d_ckm`, `count_attractors`, `A0`, `A_actual`): lo que cambió es la cantidad que llevan (§N). *(delamor: "después póngale d_ckm o d_cuencas, no me importa, mientras haga lo que DEBE.")*
- Baseline ≤ 1 → `None`, sin medición. El vacío es **UNKNOWN**, no "stable" (CP2c, `57f8a88`).
- En el panel, `D_ckm` y `D_masa_cuencas` son el mismo número.
- Traza del proceso: la TASK se escribió **después** de aplicar los pasos 1 a 4, no antes, y el REG lo declara. El paso 1 solo había dejado un estado intermedio —la fórmula de masa sobre **conteos**— que no era ni la forma anterior ni la canónica.

**Consecuencias sobre lo que sigue en esta sección, que es la v14 y se conserva como traza** (donde dice A0 / A_actual como conteos, se lee "septiembre"):
- "D_ckm no converge en signo bajo variación de seed o n_runs" era del **conteo**. N_eff con n_runs ≥ 1000 es estable (±1–5%), y `n_runs = 1000` está declarado en la Config (§11).
- **D_CKM_THRESHOLD = 0.40 se calibró sobre la escala lineal.** Sobre la escala log está **no recalibrado**. Va a Calibración: **[delamor]**.
- La cuantización "en paisajes pequeños" (§11) era de A0 entero; N_eff es real.
- "Qué cantidad conduce a COCO" (§18) queda cerrado en la cantidad y abierto en los umbrales.

```
D_ckm = (A0 − A_actual) / A0

A0      = _count_attractors(W)
A_actual = _count_attractors(W + Δ_r)
```

*(Post-D3: el Δ_r de esta fórmula es `Δ_r_pares` para `D_ckm_monitor` y `Δ_r_compresiones` para `D_ckm_coco`. Son dos campos distintos desde `7df4a72` — ver §9.)*

- D_ckm > 0: diversidad cayó ("degradado")
- D_ckm < 0: diversidad aumentó ("expandido") — no es error, es información
- D_ckm = 0: sin cambio

**La "d" y D_contextual — lo que se mostró** *(v14)*. Se **mostró**, no se demostró. Lo que hay es esto y nada más:

- `REG_d_contextual_temporal_v1` (Mayo 2026) operacionaliza `D_contextual(t) = [A(0) − A(t)] / A(0)`, que es la definición de D_ckm letra por letra. Desde mayo los dos nombres designan el mismo objeto computado, en dos documentos que no se citan entre sí. *Es un hecho sobre los documentos.*
- Si H se toma como H₂ de Rényi y `N_eff = exp(H₂)`, entonces `H₂(t0) − H₂(t) = ln N_eff_0 − ln N_eff_actual`, y normalizado por H₂(t0) da `1 − ln N_eff / ln N_eff_0` — la fórmula de `landscape_engine.d_masa_cuencas`. *Es álgebra, dada esa elección de H.*
- D_ckm y D_masa_cuencas difieren en la **referencia**, no en la forma: conteos contra masas. Por §11, sólo la segunda converge.

Eso es lo mostrado. **No demuestra que la entropía de trayectorias accesibles y un cociente de conteos guarden una relación formal**, y que H sea H₂ sobre masas es una elección que la formulación de mayo no fijó. Una expresión se adoptó como operacionalización de la otra; el paso entre ambas no está dado. *(delamor: mostrar no es demostrar.)*

El rótulo arrastra una consecuencia igual: la *d* viene de D_contextual, que es una distancia. Leer D_ckm positivo como *"degradación"* es interpretación agregada al nombre, no propiedad de la cantidad.

**D_CKM_THRESHOLD = 0.40**

**D_ckm no converge en signo bajo variación de seed o n_runs** (REG_seleccion_nodos_desempate_v1 §8, verificado sobre caso09 bootstrap 12 y 16): el signo puede invertirse cambiando solo n_runs de 50 a 1000 sobre la misma W y los mismos textos. A0 crece con n_runs (bootstrap 16: 4–8 → 21–25); A0 y A_actual crecen a ritmos distintos, de ahí el cambio de signo. **N_eff con n_runs≥1000 es estable** (±1–5% entre seeds). D_ckm como dirección es indicativo; como valor absoluto o signo, no converge sin n_runs suficiente.

**Estado incierto**: hereda sesgos de `_count_attractors`. Ver REG_situacion_medicion_ago2026_v1 y REG_stochastic_eval_v2.

**Dos instancias de D_ckm — distinción explícita (v8, NOTA_armstrong v2):**

```
D_ckm_coco    ← COCO, conduce decisiones de OPERADOR_STOP_COCO
D_ckm_monitor ← MonitorService panel, herramienta de observación
```

Ambas usan la misma fórmula `(A0 − A_actual) / A0` pero operan sobre rutas distintas:

- **`D_ckm_monitor`**: opera sobre `W + Δ_r_pares`, con `_combine_W_Delta` normalizando `Δ_r / max(Δ_r)`. **Post-D3 es ciego a las compresiones de COCO porque nunca recibe ese objeto** — separación, no cancelación (ver Modelo Conceptual y §9). *Registro histórico, pre-D3: cuando COCO escribía sobre el Δ_r de Monitor, la normalización cancelaba el escalar uniforme `α·Δ_r` por construcción — verificado, valor idéntico (0.8857) en 19 evaluaciones consecutivas con Δ_r diferente en 14 órdenes de magnitud; cancelación exacta, no aproximada. La normalización sigue en el código; lo que ya no llega es el escalar.*

- **`D_ckm_coco`**: opera sobre W_eff con Δ_r sin normalización interna relativa — refleja el efecto real de OPERADOR_STOP_COCO sobre el campo navegable.

**Asimetría de calibración:** D_CKM_THRESHOLD = 0.40 calibrado con W_mixta (AMP=40). En corpus W_pos de baja densidad (WARMUP_TEXTS), el piso estructural = (174−64)/174 = 0.632 > 0.40 → el umbral no activa OPERADOR_STOP_COCO de manera sensible. No es un bug — es asimetría documentada entre calibración (W_mixta, donde el instrumento tiene efecto real) y uso actual (W_pos, donde el piso estructural supera el umbral).

**Pendiente de implementación:** alias `D_ckm_monitor` en MonitorService (TASK_dckm_monitor_alias_v1) — no sustituye `D_ckm` para preservar legibilidad de JSOLs históricos.

**Dirección de exploración (propuesta):** diferencia `D_ckm_coco − D_ckm_monitor` como señal de cuándo COCO tiene efecto real vs. opera sobre Δ_r sin cambiar el campo navegable.

---

## 11. Conteo de atractores — _count_attractors

**`_count_attractors` no nombra una función: nombra varias** *(v14, declarado por delamor)*. El nombre se conservó **por regresión** —para no romper tests ni la lectura de JSONLs históricos— mientras la implementación cambiaba. Hoy conviven, entre otras, `services/landscape_engine.count_attractors` (la vigente, con `relax_orbit`), `services/monitor_service._count_attractors` y `services/coco.py._count_attractors` (que delegan), `services/fabrication_service` (dos variantes), y las copias de `experiments/` y `process/experiments/coco_thermostat.py`. **La que produjo los paneles de la serie IAP no es la vigente.** Cualquier afirmación sobre "lo que mide `_count_attractors`" tiene que decir cuál, y a qué fecha. Lo medido en §11 y §4 corresponde a la implementación vigente salvo que se diga otra cosa.

*(v15: desde `dabd1ed`, `landscape_engine.count_attractors` devuelve **N_eff por órbita** (`float`), no terminales; la forma anterior queda como `deprecated_count_attractors`. Lo que sigue en esta sección describe la de septiembre y se conserva como traza. **`n_runs = 1000` y `seed`** se declaran en la Config, uno solo para Monitor y COCO (delamor, 8 oct, P9: *"n 1000"*, donde N_eff converge ±2% respecto de 5000). Antes, sobre el mismo campo, Monitor contaba con 1000 y el COCO de Corpus con 80.)*

```
Para cada run (1..n_runs):
    n_act ~ uniform(0.3, 0.7) · N
    σ₀: n_act nodos en +1, resto −1
    σ_final = _relax(σ₀, W_eff)   ← relajación sincrónica, max_iter=200
A = |{σ_final únicos}|
```

**n_runs hardcoded = 200 en modo operacional** (actualizado a 1000 en MonitorService, Sep 2026): con n_runs=50, N_eff queda ~32% por debajo del valor convergente. Con n_runs=1000, N_eff converge ±2% respecto a 5000 runs en casos IAP. Señal de saturación agregada al panel: `N_eff_sobre_n_runs` y `orbitas_unicas_frac`. WARMUP_TEXTS no converge: N_eff≈n_runs — mide el muestreo, no el paisaje.

**Dos sesgos documentados e independientes:**
1. `n_runs` — coupon-collector sin saturación (verificado hasta n_runs=300 ponderado)
2. Distribución de σ₀ — no representa topología de W_eff

**Modo uniforme** (default): P(nodo i) = 1/N.
**Modo ponderado** (experimental, no cableado): pᵢ = |W_eff|ᵢ / Σ|W_eff|.

**Estado incierto**: ningún modo validado. El uniforme puede medir velocidad de expulsión, no diversidad. El ponderado da conteos menores (92/100 pareados) — dirección opuesta a la hipótesis.

**L como objeto que se mide — fundamento formal:**

Los atractores de Hopfield son los mínimos locales de V(σ) = −½σᵀWσ — el conjunto L del Teorema de LaSalle. `_count_attractors()` es un **estimador de |L|** por Monte Carlo sobre condiciones iniciales. Las cuencas de atracción tilan el espacio de estados {−1,+1}^N; la calidad del estimador depende de cuán proporcionalmente la distribución de σ₀ cubre esas cuencas.

**Precisión de REG_orbitas §4, no incorporada hasta v14:** lo estima **por defecto** —los terminales son estados de L, y sólo se ven las fases que las colas alcanzaron— y **no estima el número de órbitas**. Son dos cantidades distintas, `|L|` y `|L/~|`, con el orden `órbitas ≤ terminales ≤ |L|` (medido: WARMUP 164/174/280; caso09 natural 53/64/83; `W_ckm_corpus_v2` 5/5/8). Contar órbitas requiere `relax_orbit`; `_count_attractors` no lo hace. *Cuánto muestreo necesita cada una de las dos respecto de la otra: **no medido**, no hay registro que lo compare.*

**Por qué uniforme sesga:** en W anisótropa (nodo tipo-965, ratio 455×), las cuencas tienen volúmenes muy distintos. Muestreo uniforme concentra σ₀ en zonas sin estructura → expulsión rápida hacia cuencas dominantes → el instrumento mide variedad de trayectorias de expulsión, no variedad de cuencas.

**Por qué ponderado da menos (dirección invertida, 2 observaciones consistentes):** ponderar por |W_eff.sum(axis=1)| concentra σ₀ en los nodos de mayor conectividad — que residen en la cuenca dominante. No amplía cobertura: la estrecha. El efecto observado (menos atractores únicos) es coherente con este mecanismo. Sin conteo exhaustivo, no verificable; explicación: **admisible**.

**Qualifier tie-breaking — acotado a corpus específicos (v8, NOTA_armstrong v2):**

La dominancia de tie-breaking (factor ~3: 174 → 60 atractores) se verificó en corpus WARMUP_TEXTS.

| corpus | N | densidad | valores no-nulos | h=0 en primer paso |
|---|---:|---:|---|---:|
| WARMUP_TEXTS | 20 | 0.126 | {0.5, 1.0} | 33.6% |
| W_ckm_corpus_v2.json | 32 | 0.756 | 95 distintos, max 0.053 | 1.5% |

Condiciones de aplicación de tie-breaking dominante:
- densidad < ~0.15 (corpus esparcido)
- pocos valores distintos no-nulos (pesos discretos)
- fracción h=0 en primer paso > ~30%

**No transfiere a W_ckm_corpus_v2.json**: con ese corpus count(W) = 5 con la regla actual. El factor ~3 desaparece. El tie-breaking no es propiedad general de `_count_attractors` — es información sobre la estructura del corpus específico.

**D_ckm cuantizado en paisajes pequeños (REG_wmixta_forzado_paso3_v1):** con A0 entero pequeño, D_ckm = (A0−A)/A0 toma valores discretos con pasos grandes. El umbral 0.40 puede caer entre dos valores alcanzables — COCO no puede cruzarlo aunque el campo se degrade. Con A0=3: valores posibles {0, 0.333, 0.667, 1.0}, paso=0.333. Con A0~30: paso~0.033, ~30 valores intermedios entre 0 y 0.40. El modo de muestreo fija A0, A0 fija la grilla, la grilla determina si COCO puede actuar. El sesgo n_runs mueve A0 y por tanto mueve la grilla.

La regla "conserva σ cuando h=0" es la que garantiza convergencia (Lyapunov/LaSalle, §4). No se toca.

**Modo Boltzmann** (implementado — Code Opus, Ago 2026):

Tercer modo de muestreo de σ₀, termodinámicamente fundamentado. Con `relax_orbit` y n_runs≥1000, el muestreo uniforme converge en masas de cuenca. El warmup de Boltzmann **ya no es necesario** para la convergencia: la velocidad de `relax_orbit` lo hace redundante. En caso09 (24 textos), el corpus se agota antes de completar el warmup. El modo sigue disponible pero no es el camino operacional.

*Estado: implementado. El modo uniforme con relax_orbit es el camino convergente verificado.*

**Verificación de condiciones Lyapunov sobre W_eff — código:**

Dos condiciones requeridas por Lyapunov/LaSalle: W_eff simétrica, diagonal cero. Ambas verificadas en `monitor_service.py`:

*(v15: las líneas que siguen son de septiembre. Hoy el bucle es `for i, j in expulsados:` (L233), y `Δ_r_torsion` se acumula igual (L238–L240): las dos condiciones siguen por construcción. Que `pares_por_orbita` genere sólo pares con j > i **no se reverificó línea por línea en v15**.)*

*Simetría de Δ_r* — acumulación explícita en ambas direcciones (`monitor_service.py` líneas 112–114):
```python
for i, j in rejected:
    self._Delta_r[i, j] += 1
    self._Delta_r[j, i] += 1
```
Δ_r = Δ_rᵀ por construcción. W es simétrica por construcción. → W_eff = W + Δ_r_norm simétrica. ✓

*Diagonal cero de Δ_r* — `_rejected_pairs` genera solo pares con j > i (`monitor_service.py` líneas 232–233):
```python
for i in range(len(declared)):
    for j in range(i + 1, len(declared)):   # j > i siempre
```
El par (i, i) nunca se genera → Δ_r[i,i] = 0 ∀i. W[i,i] = 0 por convención Hopfield. → W_eff[i,i] = 0 ∀i. ✓

Las dos condiciones necesarias para que la garantía Lyapunov/LaSalle aplique a `_count_attractors(W_eff)` están satisfechas por construcción del código, no por convención.

---

## 12. COCO y el operador de compresión de COCO *(v14: COCO y OPERADOR_STOP_COCO)*

*(v15)* **No hay más STOPs** (delamor, 5 oct): stop es detenerse, y el operador nunca se detuvo: hace `Δ → α·Δ`. Su nombre formal es **operador de compresión de COCO**; "operadorstop" es el apodo *"entre los íntimos"*. El texto de la v14 conserva OPERADOR_STOP_COCO como traza (los REG cerrados no se renombran; §N). *"STOP es invitar a cenar a BABEL: al otro día tenés un compañero de cuarto instalado con el desayuno listo, y ni sabés quién es."*

**Genealogía de "no produce pérdida".** El resultado es de **junio** (`registers/REG_destruccion_recuperacion_v1`, Sonnet 4.6): un driver (`sweep_stop_perdida.py`) con W fija (W_mixta AMP=40, N=32, A0=25), cuando todavía no existían COCO ni D3; α se barre y se toma max_α. Desde v12 lleva pegado el nombre del operador de septiembre. Abierto, además: ese REG mezcla Δ y Δ_r, y con W fija y sin rebuild no está claro si la premisa es de W dinámica o del signo de W **[delamor]**.

**COCO no es opcional.** Es componente constitutivo del modelo — no una característica adicional ni un módulo activable. Un sistema IAP sin COCO no es CKM en operación; es el instrumento sin su mecanismo de regulación.

ODA inductivo (verificado v32):
```
state_{i+1} = A(D(O(state_i)))
```

**Free will en IAP** *(v14, delamor — anotado a pedido)*. Los devices **no reaccionan solamente a eventos `on_message`**. Pueden interactuar cuando lo deciden, sin turnos, y todos ven todo. Tres condiciones que lo sostienen, verificadas en código:

- **Sin turnos, y broadcast.** Todo mensaje publicado se entrega a todos los devices conectados, sin ruteo ni destinatario. Nadie tiene asignado cuándo le toca.
- **Loop propio, reloj propio.** `AutonomousDevice` corre su propio loop asíncrono de polling contra MCP (`poll_interval`, default 2 s). **No es un callback del canal**: el canal no lo invoca, el device pregunta. Esa es la diferencia arquitectónica que hace posible la iniciativa — un device invocado por el canal no puede decidir cuándo actuar, uno que corre su propio ciclo sí.
- **No publicar es un acto.** `OP_SILENCE` está declarado en el código como *"salida real, no omisión"*. El silencio es una decisión de la fase D, no la ausencia de una.

*Estado hoy:* la fase O se entra con un mensaje nuevo ajeno (`_observe(client, message)`; el trigger se filtra para que nunca sea propio). El loop propio **habilita** decidir sin ese disparador; los skins actuales no lo ejercen. PROPUESTA v5 ya lo declara: *"Observe incluye el silencio. Un device con objetivo propio puede decidir actuar antes de que ocurra Z. `on_message` no puede ser el único trigger."* La capacidad es arquitectónica; su ejercicio es abierto.

*(v15: `TASK_canal_iap_clock_iniciativa_v2` (`c451af8`) propone el **CLOCK del canal** —ticks numerados, comunes y observables; el silencio entre mensajes es dato— y el **ODA continuo**: el mensaje nuevo y el tick pasan a ser parte de la observación, no el disparador; D elige una acción —publicar, irse— o ninguna, y cada acción usa una primitiva del canal. Todos los timestamps en UTC, de recepción, del reloj del canal. La serie IAP 0.4–0.15 se **congela** con sus condiciones: no se revisa, no se reproduce (*"NO ES REPRODUCIBLE"*). **Propuesto**, sin implementar; el CP0 de Code está pendiente. **Genealogía:** delamor observó *contagio* en el IAP project; Sonnet lo escribió después como *acoplamiento* (§N).)*

**ODA sin auto-observación no aporta nada** *(v14, delamor)*. El ciclo O→D→A no es la contribución: viene del game loop del BE Framework (2023–2024). Lo que lo vuelve otra cosa es la **auto-observación** —y el intento—, sin lo cual A(D(O(·))) es un bucle de reacción con tres nombres. En la misma línea: un device skin **pretende liberar**; que libere o no depende de eso, no de la arquitectura que lo permite.

**Ciclo de vida de COCO = ciclo de vida de W**: si W cambia (rebuild), A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe. *(v15: **implementado** — CP2b y CP4. Antes había dos COCO: el que creaba Corpus en cada rebuild y el viejo que retenía Monitor; el `ValueError` (31,31) contra (28,28) en `coco.py:254` rompía cuando cambiaba N. Hoy COCO renace con el ciclo que abre Monitor, con baseline en W_eff = W, historia vacía y, en período 2, con la órbita — Modelo Conceptual.)*

**COCO y el canal** *(v15)*. **La serie IAP nunca tuvo COCO conectado**: se ejerció en tests y drivers (delamor, para el paper; MAPA_REG_corpus_v4: *"el canal vivo no inyecta thermostat"*). **Desde el CP4 (`1e8d267`) el canal sí lo construye**: `CKMMonitor` le pasa `coco_config` a Monitor, que hace nacer a COCO con el ciclo bootstrap y renacer en cada ciclo (`iap_chatroom/ckm_monitor.py` L87–L98). Se corrió una vez por el camino real (ChatChannel → callback de CKMMonitor) sin errores. **Con devices vivos no se corrió:** los `test_caso_*` necesitan claves de provider (§18). Las dos frases valen a la vez, cada una con su fecha.

**OPERADOR_STOP_COCO**:
```
Si D_ckm > D_CKM_THRESHOLD:
    Δ_r_compresiones ← alpha · Δ_r_compresiones
    alpha = _alpha_for(D_ckm)   ← monotónicamente decreciente
```

*Post-D3 (Sep 2026): OPERADOR_STOP_COCO opera sobre `Δ_r_compresiones` — el objeto propio de COCO. No modifica `Δ_r_pares` de Monitor.*

`_alpha_for` monotónicamente decreciente: **verificado** 43/43 tests. *(v15: `d_ckm_threshold`, `alpha_star` y `frac_rec_min` están **no recalibrados** sobre la escala log de D_ckm; son de Calibración — §10.)*

**Armstrong in-vivo** (verificado): OPERADOR_STOP_COCO aplicado 20/20 veces, α ∈ [0.05, 0.30]. *(v15 — MAPA_REG_corpus_v4, REG_armstrong_stop_coco_v1 §Réplica: "in-vivo" es un pipeline MonitorService + COCO **en un script de test**, no el canal. Con **seed 123**, única variable cambiada, da **3/20**, no 20/20. El mecanismo replica (α en rango, Δ_A > 0); el conteo de aplicaciones no: depende de dónde cae una estimación ruidosa respecto de un umbral fijo.)*

**frac_rec — dos métricas distintas (v8, NOTA_armstrong v2):**
- `frac_rec` del REG_destruccion_recuperacion_v1 = max_α[A_post(α)]/A0 — el máximo sobre α en barrido controlado. Este valor ≥ 1.0 en todos los casos observados.
- `frac_rec` en runtime de la corrida Armstrong = A_post/A0 en cada aplicación individual de OPERADOR_STOP_COCO; va de 0.05 a 0.68, no llega a 1.0 en ningún modo.

No son comparables directamente. "OPERADOR_STOP_COCO no produce pérdida" se sostiene en su contexto original (barrido max_α, REG_destruccion_recuperacion_v1). La corrida Armstrong no refuta ni confirma esta propiedad para el régimen W_pos baja densidad.

**Efecto COCO por régimen de W (v8, NOTA_armstrong v2):**
- **W_pos baja densidad (WARMUP_TEXTS)**: efecto real en primeras ~3 aplicaciones de OPERADOR_STOP_COCO (delta_A = +34, +31, +24). Se agota cuando Δ_r cae por debajo de ~0.05 — estado absorbente. OPERADOR_STOP_COCO sigue aplicando pero no puede mover el landscape: el soporte de Δ_r no cambia, solo la magnitud. Estado absorbente ≠ catástrofe.
- **W_mixta — verificado (REG_wmixta_consolidado_v1, Sep 2026)**: corpus `caso09_run2` (24 textos IAP). Dos regímenes controlados — único parámetro diferente: `force_w_pos`.

  Natural (W_mixta, 56 pesos negativos): A0=26–32 (n_runs=50). 42 aplicaciones de OPERADOR_STOP_COCO en 3 modos, ningún delta_A negativo, mínimo +11. Campo cicla — cruza umbral en ambas direcciones. Δ_r acotada 62–76 vs 632 sin thermostat.

  *Nota post-D3 (Sep 2026): el hallazgo "Δ_r acotada 62-76" medía `Δ_r_pares` de Monitor en el sistema pre-D3, donde COCO escribía en ese objeto. Post-D3, Monitor acumula `Δ_r_pares` sin cota desde COCO — COCO opera sobre `Δ_r_compresiones` propio. Los paneles nuevos no son comparables con los anteriores en ese campo.*

  Forzado (W_pos del mismo corpus): A0=3–4. 7 aplicaciones de OPERADOR_STOP_COCO en un solo modo (weighted), delta_A máximo +1. Uniform y boltzmann no cruzaron el umbral.

  **Mecanismo verificado:** la diferencia en aplicaciones de OPERADOR_STOP_COCO pasa por A0 y la grilla. W_mixta produce A0 ~10× mayor (n_runs=150: 58 vs 4) — grilla fina, umbral 0.40 alcanzable. W_pos produce A0=3–4 — umbral cae entre valores que la grilla no contiene.

  **Cautela:** el forzado no es W_pos genérica — es la W_pos de un corpus con tensión subyacente no codificada. La comparación no está pareada en escala de operación (A0~30 vs A0~4).

**H_STOP falsificada** (v27, sweep t_stop × α): D_ckm no predice ratio_max.

**Hipótesis revisada (abierta)**:
```
Efectividad_STOP = f(A_pre)
A_pre < A0  →  OPERADOR_STOP_COCO expande paisaje (ratio > 1)
A_pre = A0  →  OPERADOR_STOP_COCO neutro
alpha* ≈ 0.40 robusto para A_pre < A0 (5/9 casos)
```

α=1.0 (sin OPERADOR_STOP_COCO) nunca óptimo. α=0.0 (reset total) solo óptimo en casos específicos.

*Tensión registrada: la declaración "no opcional" puede ser cierre prematuro de una tensión abierta entre Monitor y COCO. Marcada como abierta en PROPUESTA v5.*

---

## 13. Zonas de operación G1/G2/G3

Derivado empíricamente (N=32, n=500 secuencias):

| Garantía | Zona | c(S) (80% CI) | r (80% CI) | Significado |
|---|---|---|---|---|
| G1 | Zona crítica ρ ∈ [0.4, 0.8] | [−0.000332, +0.001310] | [−0.074, +0.290] | Monitor operativo |
| G2 | Atractor bloqueado ρ < 0.15 o > 0.85 | [+0.001941, +0.004519] | [+0.430, +1.000] | Señal colapsada |
| G3 | Degradación activa | c(S) < −0.000332 | r < −0.073 | Declarar HOLDING |

Gap discriminante G1/G2: [+0.001310, +0.001941] — detectable en tiempo real por r = c(S)/μ_W.

**μ_W y r — siempre al inicio de sesión, nunca como constante (v9):**
μ_W NO es una constante universal — cambia con la composición A/B del corpus y con N. El factor r = c(S)/μ_W pierde discriminación si μ_W es aproximado o heredado de otra sesión. COCO requiere: (1) medir μ_W empíricamente al inicio de cada sesión, antes de cualquier evaluación G1/G2/G3; (2) monitorear r en tiempo real durante la sesión.

---

# PARTE IV — CRITERIOS DE SELECCIÓN Y ESCALA

## 14. Coercividad CKM

Del lazo P1 (hopfield.py, N=32, n=200 secuencias): dos cruces de c(S)=0 en rama UP a ρ=0.406 y ρ=0.586. Intervalo frustrado, no punto.

**Definición operativa** (REG_mapeo_magnetico_ckm_v1): valor de ρ donde c(S) cruza cero en rama de incorporación — análogo al campo coercitivo magnético.

Coercividad W_pos: nula. Coercividad W_mixta: mayor. Estado: **verificado** geométricamente; interpretación magnética: **propuesto**.

*(v15 — `P1P4/OBS_P1_run_P1_y_coercitividad_04oct_v1.md` §3.)* **Los dos cruces son combinatoria de N, no coercitividad del campo.** Para k nodos en +1 elegidos al azar, E[c(S)] = μ_W · ((2k − N)² − N) / (N(N − 1)), que se anula en **ρ = 0.5 ± 1/(2√N)**: con N = 32, 0.412 y 0.588, **independiente de W** (salvo μ_W ≠ 0). Con el operador: W_ckm_corpus_v2 cruza entre 0.375–0.406 y 0.562–0.594; una W positiva aleatoria, entre 0.406–0.438 y 0.562–0.594. Además el lazo de abril no relajaba (§5). **El número está bien medido; lo que no es, es una propiedad del campo.** La coercividad como propiedad de W queda **abierta**, y SALAMANCA mide otra cosa: la coercitividad de **frontera** por par de clusters (§16).

---

## 15. Temperatura de Néel efectiva (≈ Nielsen ≈ TEER)

*Propuesto — no verificado* *(v15: sigue **no corrido** — REG_salamanca_s1_v1 §6. Es el segundo paso de la admisión de W_mixta: qué profundidad tiene la frontera que SALAMANCA encuentra. Su lugar en el Orden BABEL no está decidido: barre β sobre una W fija, pero su uso es construir W_mixta [delamor].)*

Criterio de elicitación de pares negativos sin sesgo editorial:
1. Construir W_pos.
2. Barrer β de alto a bajo.
3. β_Néel = β donde separabilidad T0/T1 colapsa.
4. Pares en clusters opuestos antes del colapso → candidatos a pares negativos.

Relacionado con SALAMANCA (ver §16). Ver NOTAS_proxima_sesion_paper_v11.md, Tema 4.

---

## 16. SALAMANCA

*v14: Propuesto — no verificado.* ***v15: S1 corrido*** *(`registers/REG_salamanca_s1_v1.md`, OK de delamor 5 oct; 1000 barajados, k-means con 10 inicializaciones, Bonferroni sobre 7 k).*

Criterio previo a W_mixta: detecta si W_pos tiene estructura adversarial (T0/T1 con cut bajo) antes de introducir pares negativos. Si no detecta → W_pos es la respuesta; W_mixta no tiene objeto.

**Corrección (v15 — REG_salamanca_s1 §3, delamor): no detecta estructura adversarial; detecta modularidad.** Que haya módulos no dice que haya posiciones que se opongan. Una palabra, dos objetos, y es la razón de que el criterio admita de más: **SALAMANCA sola habría admitido W_mixta en un canal de coordinación.** La admisión de W_mixta necesita los dos pasos; Néel es el segundo (§15).

**El intento que subyace** *(delamor)*: no es encontrar fronteras, es tener un criterio que **pueda devolver vacío**. *"Lo que natura non da, SALAMANCA non presta"* — y *"no se fía"*.

| corpus | saturación | veredicto S1 | lectura |
|---|---:|---|---|
| caso09 | 0.619 | **FRONTERA** (k = 3 y 6; k = 3: cluster mín. 6 nodos, efecto 2.97×, p < 0.001) | separa protocolo e identidad de device de contenido: un canal de coordinación, no dos posiciones |
| caso13 | 0.875 | **FRONTERA** sólo con clusters de 2 nodos | posible división del trabajo entre devices; en k = 2 y 3 el barajado es más coercitivo que el real |
| informes, página 300 | 0.964 | **FRONTERA** sólo con clusters de 3, efecto 1.29× | — |
| caso14 | 0.992 | **NO MEDIBLE** | saturada: sin ceros no hay corte barato |
| informes, versión | 1.000 | **NO MEDIBLE** | ídem |
| tramo `categorias` | 0.467 | **NADA** / no medible | 7 textos |

- **La saturación ordena:** monótona en los cinco corpus medibles, y medida sobre W antes de particionar. Verificado como medición; la lectura causal es **propuesta**.
- **Lo que más importa:** el criterio **devolvió vacío** donde no había con qué —dos corpus saturados, uno por tamaño—. Eso es lo que el ruteo por marcadores nunca pudo hacer.
- **Control positivo: ausente.** Ningún corpus fue elicitado con posiciones opuestas por diseño. Previstos: RfA (Wikipedia Requests for Adminship, posiciones declaradas y voto registrado; delamor) y fourforums como W de **términos** (el dump está en `ckmdatasets`, local).
- La corrección por la familia completa de comparaciones **no está sostenida** a 1000 barajados.

```
cut(T0, T1) = Σ W_ij   para i∈T0, j∈T1
```

Alternativa: barrido β + normalized cut espectral (sin semilla T0/T1 previa).

---

## 17. Escala y N

**N=128 (mínimo Hopfield asociativo)**: aplica a memorias Hebbianas con patrones no correlacionados (α_c ≈ 0.138N). **No aplica a CKM** — CKM no almacena memorias. El mínimo operativo de CKM es abierto y depende de composición A/B del corpus.

Al aumentar N en CKM, el comportamiento va en dirección opuesta al Hopfield clásico. El límite real está dado por la densidad del lenguaje natural humano. En implementación persistente, N podría ser del orden de miles.

---

# PARTE V — ABIERTOS Y TENSIONES

## 18. Lo que permanece abierto

Los abiertos se organizan por plano. Ver también §X sobre planos distintos.

**Plano matemático / estructural** (afecta al modelo):
- H2 (A0 vs A_actual bajo ponderación): sin respuesta verificada
- Figura R13 (A∪B, 45.2%): metodología lista, no ejecutado
- SALAMANCA y Néel: operacionalización pendiente. *(v14: dejaron de ser sólo criterio de elicitación de pares negativos — son **precondición** de plantear la admisión sobre nodos de corpus, tercer paso de la cadena del Modelo Conceptual. Y tienen condición de referencia desde REG_unidad_texto §5.2: caso09 debe dar estructura; los informes y el canal IAP, nada. Si dan lo contrario, el criterio está mal.)* *(v15: S1 dio frontera en caso09, frontera débil en informes por página y no medible en informes por versión. La condición de referencia no se cumple entera, y lo que S1 mide es modularidad — §16.)*
- max_iter=200 y n_runs=200: justificación ausente para W_mixta con frustración *(v15: `n_runs = 1000` declarado en la Config, P9; max_iter sigue sin justificación)*
- Qué mide realmente `_count_attractors` bajo cada modo — pregunta estructural sobre el instrumento
- **Qué cantidad conduce a COCO**: hoy D_ckm, que por §11 no converge ni en signo. D_masa_cuencas opera sobre masas, que sí convergen, y ya está en el panel. El operador no se movió. *(v14)* *(v15: **cerrado en la cantidad** — `dabd1ed`: D_ckm es la fórmula canónica sobre masas. **Abierto en los umbrales**: no recalibrados.)*
- **fi de la partición A/B**: la discrepancia 102× / 68.6× no tiene causa identificada (§7)

**Plano operacional / calibración** (afecta al instrumento, no a la validez matemática):
- Calibración W_mixta build/rebuild: pendiente (§8)
- Implementación alias D_ckm_monitor en MonitorService: pendiente (TASK_dckm_monitor_alias_v1)
- Umbral min_texts como criterio dinámico: la saturación de pares distintos es el criterio propuesto (REG_unidad_texto_saturacion_v1 §3) — cuándo W deja de ganar ceros informativos. No implementado.
- ~~Desempate de selección de nodos~~ → **cerrado**: regla implementada y verificada — donde el dato no decide, conserva el precedente (histéresis, P1). N deja de ser fijo (REG_seleccion_nodos_desempate_v1, 170/170 tests).
- ~~Escala de D_masa_cuencas (lineal vs log)~~ → **cerrado**: log, decidida por delamor, implementada y en panel (`80c9c50`).
- **Stopwords e idioma: verificado y no corregido** (§1.1d). La unión de tres listas elimina `estado`, que es σ. Un corpus mezclado parte el concepto de forma asimétrica y sin declararlo. *(v14)*
- **Nodos aislados residuales (4%)**: sin decidir si se excluyen del conteo o se registran como condición de la W (§1.1b). *(v14)*
- **`_combine_W_Delta` sigue metiendo Δ_r en pares que W tiene en cero**: la metabolización crea acoplamientos donde el dato no los tiene (REG_hipotesis_distancia_contextual_v4, abierto). *(v14)*
- **Los parámetros de extracción no se persisten**: `CorpusService.save()` no guarda `top_k`, `min_texts`, `rebuild_suspendido` ni la versión de stopwords. Un estado reabierto con otros parámetros continúa sin señal (REG_unidad_texto_saturacion_v1). *(v14)*
- **Qué resultados previos cambian de marco** por `5aa3504` y `7bf485b`: no revisado. caso09 quedó **sin condición empírica de referencia** — bootstrap 12 no se sostiene (REG_hipotesis_distancia_contextual_v4 §3, §7). *(v14)*
- CONVERGENCIA_SLOPE para modo ponderado: descalibrado
- Efecto COCO en W_mixta más allá de ~3 STOPs: propuesto, operacional — no condiciona validez del modelo
- Órbitas período-2 en `_count_attractors` sincrónico: operacional — no amenaza las garantías LaSalle; afecta la calibración del estimador

**Nuevos en v15** (plano indicado en cada uno):
- **Calibración** (operacional): el proceso no existe. Los umbrales de COCO están no recalibrados sobre la escala log; la corrida larga de caso09 (`n_torsion`, 16 de 24 en período 2) va ahí.
- **Dos relojes** (operacional): `t_senal` y `t_rebuild` del `Ciclo` se sellan con `time.time()` del proceso de Monitor; los mensajes del canal, con su timestamp de recepción. Si el CLOCK vive en la Config, conviven dos fuentes en un objeto (TASK canal IAP v2 §0.6, CP0 punto 2).
- **Los 21 `test_caso_*` del canal no son tests de pytest** (recogen 0 items) y necesitan claves de provider que el Codespace no tiene: **punto ciego declarado**. Cada reporte que toque el canal los nombra en "no pude revisar".
- **`test_armstrong_via_corpus_v3.py:34`** (`assert corpus.coco is not None`) roto a sabiendas por el CP4; va con la revisión de las seis salidas `armstrong_*`, de origen **UNKNOWN** [delamor].
- **P10:** `_last_landscape_signal` se escribe y nadie lo lee. Se queda hasta que alguien toque `corpus_service.py` por otro motivo.
- **`NodeExtractorConfig`:** decidido, no implementado. El criterio de extracción no queda en la traza (§1.1 f).
- **Nombres a decidir** (§N): `expulsados`; Gatekeeper / admitir; activar / incorporar; STOP en el código [delamor].
- **P1–P4 sobre W dinámica** (matemático / estructural): sin TASK (§5) [delamor].
- **Prefijos del Orden BABEL:** sin decidir (esperar el patrón).
- **§0, dominio contra interpretaciones:** tensión sostenida [delamor].
- **D2 de la PROPUESTA v27:** la fila sigue mal escrita (§12, genealogía).
- **Las DEFS viven en el repo público** (`docs/defs/`, v7–v15). La nota del 4 oct dice que son privadas; delamor eligió `docs/defs/` para la v15 (8 oct). Tensión registrada el 5 oct, abierta.

**Plano verificación en corpus acotado** (baja relevancia para el proyecto):
- Ratio nodo-965: >100× (REG) vs >455× (paper) — verificar en corpus actual (corpus polarizado, §6)

**Deuda técnica registrada**:
- Desfasaje Gatekeeper / W vieja: condición permanente de operación, no bug

## X. Planos distintos: validez matemática y verificación operacional

La validez matemática de CKM (Lyapunov/LaSalle, separación W/Δ, garantías de convergencia) está demostrada independientemente de cualquier corpus particular. La demostración es formal — no depende de que el experimento W_mixta STOP_COCO funcione en el corpus que tengamos a mano, ni de que `_count_attractors` refleje o no la invarianza orbital.

La verificación operacional (¿qué produce `_count_attractors` en W_mixta? ¿cuántos STOPs tienen efecto real?) es empírica y corpus-dependiente. Aporta información sobre el comportamiento del instrumento en condiciones específicas — no amenaza ni confirma la validez matemática del modelo.

**Confundir estos planos produce errores en ambas direcciones:**
- Exigir verificación operacional en corpus específico como condición de validez matemática: incorrecto.
- Asumir que validez matemática implica comportamiento operacional en cualquier corpus: incorrecto.

P5–P7 son verificaciones operacionales en un corpus muy específico. Si P5–P7 no se reproducen en otro corpus, nada cambia al modelo. Si `_count_attractors` en W_mixta con Boltzmann muestra o no invarianza orbital, nada cambia al modelo. Son planos diferentes. La comprensión de una parte es en relación a su dominio.

---

## 19. Tensiones metodológicas constitutivas

**W_mixta sin estado nulo**: el procedimiento `_has_opposition(text)` siempre encuentra marcadores en textos suficientemente largos — no tiene salida nula. Ninguna W_mixta construida hasta la fecha pudo haber resultado W_pos. Las W_mixta no están mal medidas: están sin contrastar. Esta es una tensión metodológica constitutiva: el instrumento de elicitación de negativos no puede confirmar que no hay estructura adversarial. Néel y SALAMANCA (§15, §16) son la respuesta propuesta. (REG_unidad_texto_saturacion_v1 §5.2, declarado.)

**El rótulo no es determinista cuando se sostienen tensiones** *(v14, delamor)*. Mantener una tensión abierta tiene un costo, y el costo lo pagan los nombres. `_count_attractors` es el caso medido: el nombre se conservó **por regresión** —para que los tests y los JSONL históricos siguieran legibles— mientras la implementación cambiaba debajo. En mayo nombra relajación uniforme con conteo de terminales; desde agosto nombra relajación orbital, y lo que cuenta sigue siendo terminales (`landscape_engine.count_attractors` hace `add(tuple(relax(s0, W_eff)))`, y `relax` devuelve el estado en `max_iter`, no la órbita). **El nombre no determina el objeto: lo determina el par (nombre, fecha).**

La alternativa —renombrar cada vez que cambia la función, que es lo prolijo del método tradicional— haría el rótulo determinista. **Es un intercambio deliberado, no un descuido:** determinación del nombre contra continuidad de la traza. Esta metodología eligió lo segundo, y conviene ser exacto sobre qué cuesta cada opción.

*Renombrando se pierde la traza*, y no en el sentido de que sea más incómoda de leer: **los paneles históricos quedan huérfanos de referente.** Los números sobreviven y lo que los produjo deja de estar nombrado en ningún lado. Es la pregunta fundacional de IAID otra vez, ahora del lado del instrumento: el conocimiento no sobrevivió cuando el device cerró.

*Y lo que se gana es coherencia fabricada* — en el sentido técnico que el proyecto le da al término. Con un nombre por comportamiento, ningún documento puede quedar desfasado y **ninguna discrepancia es exhibible**. Eso no demuestra coherencia: hace que la incoherencia sea inobservable. Es la misma forma que `_has_opposition` sin salida nula (§8): un procedimiento que no puede dar negativo no mide, confirma.

De ahí se sigue lo que da vuelta la intuición de ingeniería: **el desfasaje documento/código es el observable que el método tradicional suprime.** Que un documento quede atrás es la señal de que el objeto se movió. Renombrando no habría desfasaje — y tampoco señal.

Dos consecuencias que no son opcionales:

1. **Toda afirmación sobre qué mide X lleva fecha, o no dice nada.** "Qué mide `_count_attractors`" no tiene respuesta sin la versión.
2. **El desfasaje entre documento y código es estructural al método, no descuido de redacción.** Un documento fija el significado de un rótulo en el momento en que se escribe; el rótulo sigue moviéndose debajo mientras la tensión se sostiene abierta. Las correcciones de v14 —gatekeeper "ausente", el gap "mudo", los dos objetos de D3, la escala log "propuesta"— son todas de esa clase. Corregirlas no evita que vuelva a pasar: es la forma que toma sostener tensiones en documentos que se versionan.

**El proxy devuelve un número siempre; el objeto no** *(v14 — REG_unidad_texto_saturacion_v1 §5.3, declarado)*. La misma forma aparece cuatro veces, siempre con el proxy del lado medible:

| se quiso medir | se midió |
|---|---|
| tensión estructural | ocurrencias de "pero" (`_has_opposition`) |
| la unidad del campo | la unidad tipográfica (párrafo, página) |
| frecuencia del concepto | frecuencia del token |
| lo que un device aportó | lo que escribió en el idioma de los nodos |

En los cuatro casos nada falla y todo sigue dando resultado — por eso la sustitución no se nota. Lo que la hace visible no es un test: es tener un corpus donde la respuesta correcta es *nada*.

**Sesgo de destino en inferencia** *(v14 — REG_hipotesis_distancia_contextual_v4 §6, declarado por delamor)*. `bootstrap = 12` se eligió **por el resultado**: era el punto donde D_ckm cruzaba el umbral, o sea donde el instrumento hacía lo esperado. Medido después, cae en medio del warm-up de la selección de nodos (Jaccard 0.78–0.83; se estabiliza recién en k ≈ 21). La misma forma apareció otras dos veces en la misma sesión: un test de D3 que pasaba sin discriminar, y la lectura de una subida de D_ckm como propiedad del campo antes de mirar los nodos aislados. En las tres, el resultado esperado llegó antes que la verificación. Alternativa propuesta, que no mira D_ckm: fijar nodos y A0 al **fin del warm-up** de la selección (Jaccard ≥ θ durante m pasos) y declarar cuando un corpus no lo alcanza. θ y m sin decidir.

**Regla CKM TRUST** *(v15 — dictada por delamor, 4 oct 2026; `claude/sesion_04oct2026_regla_ckm_trust`)*. Cómo se decide cuando hay que decidir:

1. **El campo decide:** criterio de campo con traza. La traza es parte del criterio, no un agregado.
2. **Si empata y hay traza, la traza decide:** gana el que ya está, ya estuvo, ya ganó.
3. **Si no hay traza: ¿por qué no hay traza?** Se vuelve a 1, con **duda** del criterio. La duda abre, en pregunta: ampliar, acotar o separar el criterio (D3 fue eso: Δ_r → Δ_r_compresiones + Δ_r_pares).
4. **Si empata o no hay traza → desempate NULO.** Decide el criterio de contexto, que es **sesgo potencial, y se declara**.

Sin el paso 3, cada vez que falta traza se pasa directo al 4: decide el contexto, y el sesgo se presenta, subrepticiamente, como si fuera del campo. ¿Pasa desapercibido? *Depende: mecánicamente, sí* — y ese matiz es lo que hace que no sea una receta: es una regla. *"Nunca llegás al paso 3 si no te salteaste el 1."* Si se verificó haber pasado por el 1 y aun así se está en el 3, el campo está sugiriendo algo. Lo que lleva al 3: síntesis, asunción, defecto no formulado, nulo, orden, sesgo de destino, incertidumbre de **inferencia** (no de dato), cancelación matemática casual. El desempate por precedente de NodeExtractor ya era el paso 2 en el código antes de que la regla se dictara (REG_seleccion_nodos_desempate_v1). **Dudar es actitud, no falta.** La separación, las taxonomías, los niveles y los umbrales no son del campo: son el campo, parte de él; el acto de trazar la línea que separa los crea y los extingue — son del que señala.

**UNKNOWN no es un grado** *(v15)*. No es NOMINAL ni "desconocido": es no haber visto, un estado del que observa. El vacío pasaba como "stable" en COCO y como NOMINAL en Firma; desde `c06db07` y `57f8a88` es UNKNOWN, y el test que sostenía el NOMINAL por ausencia se cambió (`test_D_ckm_None_is_stable` → `…_is_UNKNOWN_not_stable`). Se van a seguir mezclando, porque la mecanicidad lo hace; lo que se puede hacer es que **el default de lo mecánico sea UNKNOWN**.

**El test tiene que poder fallar** *(v15)*. En los CP3i y CP4 de Monitor+COCO v2 se hicieron **ocho inversiones**: cambios deliberados al código, cada uno rompe al menos un test, y se restaura (la salida literal está en la BANDEJA). Dos tests que no podían fallar aparecieron **al invertir, no al leer**. Es la misma forma que `_has_opposition` sin salida nula, que el k-core de P3 y que `ckm_p1p4_module` (§5): **un procedimiento que no puede dar negativo no mide, confirma.**

**El corpus es simultáneamente datos y proceso**: N=32 construido desde conversaciones autor–Claude Sonnet. El corpus es el laboratorio y el sujeto. Si el modelo describe bien ese corpus, no queda claro si describe el espacio de conocimiento en general o solo el proceso de su propia construcción. FourForums y CreateDebate abordan esto parcialmente. La tensión es constitutiva — no es un defecto a corregir.

**α_c con patrones correlacionados**: el límite α_c ≈ 0.138 asume no-correlación. Los nodos CKM son altamente correlacionados (estructura A/B verificada). α_c es una propiedad del corpus, no del modelo. Tensión sostenida como pregunta abierta de derivación teórica.

---

## 20. Referencia externa más cercana

**Aiyappa, Flammini & Ahn. *Science Advances*, 2024.** Redes de creencias ponderadas con dinámica tipo Hopfield. Mapea casi 1:1 con W_pos. No tiene W_mixta. Único paper encontrado hasta abril 2026 con la combinación base de CKM.

*(v15 — réplica de la Fig. 5, 4 oct, Opus 5.5; `P1P4/INFORME_replica_Aiyappa_fig5_v1.md`.)* **Se sostiene:** la modularidad óptima aparece en contagio complejo —con ρ0 = 0.10 de semillas, la adopción es 0.50 con μ = 0.01, 1.00 con μ entre 0.14 y 0.19, y 0.12 con μ = 0.5—; en contagio simple no hay óptimo. Port uno a uno a Python + C de `rachithaiyappa/beliefnet` @ `2289c39`, con los parámetros de su README (α = 2, β = 1, σ = 0.2, N = 100, M = 1500), criterio pre-registrado, seed 0, 10 ensembles por celda. Límites: no es su Julia (otro generador aleatorio); la ventana de ρ0 es angosta en la grilla usada; sólo se replicó la Fig. 5. No se encontró nada que invalide el paper.

**Pariente, no gemelo.** En Aiyappa cambian los pesos; en CKM, sobre una W, cambian los estados. La energía de Aiyappa es triádica (Heider); la de CKM, por pares (Hopfield). "Mapea casi 1:1 con W_pos" se lee con eso. **La tabla del Modelo Híbrido le atribuye "histéresis Sí" a Aiyappa: esa lectura es del CKM; el preprint no la dice.** Su regla de actualización genera pesos de los dos signos, y es la pista para P1–P4 sobre W dinámica (§5). La relación de su modelo con P1–P4 va en CONDICIONES Aiyappa v3 (plan, pendiente); en la v2, la Condición 3 está mal: los cambios eran para P1–P4, no para el modelo dinámico (delamor, 5 oct).

**Cita, siempre:** Aiyappa, R., Flammini, A., & Ahn, Y.-Y. (2024). *Science Advances* 10(15), eadh4439. doi:10.1126/sciadv.adh4439.

---

*Fuentes v15 (Oct 2026): registers/REG_d_ckm_formula_canonica_v1 (`dabd1ed`), registers/REG_salamanca_s1_v1, registers/REG_trace_ip_sesion_05oct_v1; P1P4/BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1 (borrador), P1P4/INFORME_verificacion_P1_P4_v2, P1P4/OBS_P1_run_P1_y_coercitividad_04oct_v1, P1P4/INFORME_replica_Aiyappa_fig5_v1, experiments/CERRADO_LEER_ANTES_ckm_p1p4_module (`eddb4b0`); docs/tasks/TASK_CKMlandscapeConfig_v3 (cerrada, `44af68a`), TASK_monitor_coco_ciclo_orbita_v2 (cerrada, `1e8d267`), TASK_canal_iap_clock_iniciativa_v2 (`c451af8`), DECISIONES_opus.md y BANDEJA_code.md hasta el 8 oct; services/ckm_landscape_config.py, services/monitor_service.py, services/landscape_engine.py, services/coco.py en `94baf68`; ckm___memories/FICHAS_elementos_ckm_v1, PROPUESTA_estructura_modelo_formal_paper_v27; notas del proyecto TRUST del 4, 5 y 6 oct (Regla CKM TRUST, Orden BABEL, definiciones de W).*

*Fuentes v14 (Sep 2026): REG_hipotesis_distancia_contextual_v2 (la "d" es distancia; identidad con D_masa_cuencas), v3 (d(σ) ejecutado; nodos aislados), v4 (mecanismo de la extracción; σ por una rama; sesgo declarado), REG_seleccion_nodos_desempate_v1 (regla de desempate; N no fijo; estabilidad bajo n_runs y seed), REG_unidad_texto_saturacion_v1 (saturación; idioma; alcance del ruteo adversarial), REG_orbitas_conjuntos_invariantes_v1, services/landscape_engine.py, services/node_extractor.py, services/corpus_service.py, services/monitor_service.py.*

*Fuentes: THEORY.md, core.py, hopfield.py, kcore.py, analytics.py, coco.py, PAPER_v12_1.md, CKM_Informe_Trabajo_v32.md, MAPA_REG_corpus_v3.md, REG_stochastic_eval_v2.md, REG_situacion_medicion_ago2026_v1.md, REG_mapeo_magnetico_ckm_v1.md, CKM_Modelo_Hibrido.md, delamor_revision_DEFS_CKM_estado_actual_v2.md, NOTA_armstrong_hallazgos_implicancias_20260825_v2_.md, Predictibilidad_orbital.md, CKM_encuadre_representacion_conocimiento_v1.md, Agama Santiago M. "Análisis de estabilidad de las redes neuronales de Hopfield utilizando funciones de Lyapunov y el Teorema de LaSalle." Lic. Matemáticas Aplicadas, UTM Mixteca 2026.*

*Repo: gadanindelamor/ckm — Sep–Oct 2026 · v15 DRAFT hasta la lectura de delamor*
