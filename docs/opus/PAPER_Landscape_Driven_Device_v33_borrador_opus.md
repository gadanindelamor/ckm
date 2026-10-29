# The Cohesive Knowledge Model: A Convergent Basin-Mass Diversity Estimator for Hopfield Landscapes over Co-occurrence Fields

> **v33 BORRADOR — Opus 5.5, 29 oct 2026, sobre v32 (22 oct). El v32 queda intacto como traza. Este bloque se retira antes de publicar. El `_print` sale de este archivo sin el bloque, cuando lleguen los respaldos de *Pendientes*.**
>
> **Fuentes:** `docs/opus/PLAN_v33_28oct2026.md` (§1 y el agregado del 29 oct, §6); el barrido (`docs/opus/BARRIDO_v33_29oct2026.md`) y su verificación contra el plan (`docs/opus/VERIF_PLAN_v33_contra_mapa_29oct2026.md`); `docs/opus/CONSIDERACIONES_v33_24oct2026.md` (M2, M3); los REGs del intento 3 y del 4, `REG_calibrate_no_corre_en_el_build_v1` y `REG_ckm_W_fourforums_v8n_2026-10-23`; los reportes de Code del 28 oct en la BANDEJA (14.1, 14.2); el código donde se nombra. Hecho en la sesión del barrido. No es una decisión: delamor había entendido que se hacía así, y lo nombra como sesgo de inferencia (*"parece más sesgo de inferencia"*).
>
> **Qué cambia:**
> - **Premisas, sólo en W dinámica** (delamor, 26 oct). §4.1.5 pasa a *Formulations and Declarations*: el determinismo es una formulación; el productor y la medida de referencia son declaraciones; F1, F3 y F4 sin "(formerly Pn)". "Fixed by premise" → "verified" en el abstract, §1 y §8.1; en §2.3, "decided by the snapshot"; en §4.1 y §4.1.2, "premise" → "formulation".
> - **La medida de referencia es la del código** (delamor, 28 oct): la banda [0,3; 0,7] de `sample_s0`. La enumeración de §4.3.1 queda declarada bajo el hipercubo, con el tamaño de la diferencia (R0: 2,612244 contra 2,947019 en N = 20).
> - **"What jumps is its measurement"** (delamor, 23 oct; DEFS v20), con la tensión declarada, en §4.2 y §4.2.4. Sale *"[Propuesta — decide delamor.]"*.
> - **COCO no regula el campo** (delamor, 29 oct): regula su propia representación (`Δ_r_compresiones`). Corregido en §1, el título de §4.2.1, §4.2.1, §4.2.3, §7.4, §7.5 y §8.3. Opus había escrito además *"no part of the instrument regulates the field it represents"*: salió (A1) porque viene del doc X, que es candidata y no está en las DEFS.
> - **La vara de COCO** (§4.2.1): `Threshold` con `MEASURED` o `DECLARED` y su causa; nunca la de otra W; la primera W también pasa por `calibrate`.
> - **La Config** (§4.2.3), corregida contra `services/ckm_landscape_config.py`. **Los β** (M3): un párrafo nuevo en §4.2.3; sale el párrafo de β_collective de §4.2.1.
> - **§4.3.1:** tres instancias de D_ckm (Monitor, COCO y la de `calibrate`); **"D_ckm^calibrate" es notación de Opus: decide delamor**. El baseline de COCO con su fuente (DECISIONES_opus, 8 oct). El n_runs del default (200) y el de cada número. El sesgo del plug-in, medido (14.1), con Simpson (1949) como referencia. "La masa de cuenca es una medición, no la única." Sale *"N_eff ∈ [1, |L|]; N_eff = 1 is total collapse"* y *"approaches 1"*.
> - **§4.3.2:** la frase de M2 en lugar de *"3 to 34 times"*. Sale *"moves N_eff by 66% in A24 (15.52 → 5.27)"* (R2, *Pendientes*).
> - **§5:** P2, P5, P6 y P7 salen como predicciones (*"esperan condiciones"*, delamor). Queda la medición del signo por marcadores, sin la predicción. Entra fourforums v8i–v8n (delamor: *"si sostiene algo se quedan"*). Sale el párrafo de CreateDebate: sólo sostenía P7. §5.3 reescrita.
> - **§6:** el intento 4 en la tabla y en §6.2; el intento 3 con su REG. El criterio estructural de rebuild, leído en el código (R6: `should_rebuild`, n = 3). La primera W sin calibrar en los intentos 2 y 3 (`REG_calibrate_no_corre_en_el_build_v1`). §6.4 reescrito: el piso exacto del colapso, el IC del margen y la frase con sus condiciones (delamor: *"la separación registrada en tales casos y tales condiciones declarados quedó dentro del ruido"*). §6.5: el intento 4 y la salida de B.
> - **§7.6 vuelve** (delamor, 29 oct: *"SI ENTRA"*; 23 oct: *"representación del conocimiento y medir el campo son perspectivas de lo mismo… si va"*). Es el texto del v28 con tres cambios: (1) sale el párrafo *"CKM was constructed between 2023 and 2026… not questioned"* y la frase *"That displacement is not an advance on KR…"*, que dependen de la revisión de literatura (*Pendientes*); (2) entra la frase de delamor del 23 oct; (3) *"attractors, coercivity, and thermal behavior under interaction"* → *"attractors and basin masses that respond to interaction"*: la coercividad no se mide en este paper y ningún β actúa (§4.2.3). Las citas, con forma de referencia.
> - **AUTO-5 vuelve.** Lo encontró el barrido: estaba en §7.6 del v28 y se fue con ella en v29. Por eso el v32 decía que *"no existe"*.
> - **§8:** la tabla de §8.1 sin P2 ni P5–P7, con dos filas de medición. §8.2, con la Config, la primera W calibrada y los tres D_ckm. §8.3: el hueco de representación como forma (círculo que no cierra, hélice), no medido. §8.5: sale lo que arrastraban P5–P7; entra *Beyond this paper*.
> - **IAC v2:** se obtiene de https://nlds.engineering.ucsc.edu/iac2/. Sale el permiso pendiente del cuerpo.
> - **Referencias:** entran Simpson (1949), Quillian (1968), Minsky (1974), Levesque & Brachman (1987) y Smith (1985). Las marcas `[VERIFY]` y `*[v28]*` / `*[v29]*` salen del cuerpo y pasan a *Pendientes*.
> - **Apéndice A:** AUTO-13 y AUTO-14, de esta escritura.
>
> **Lo que esta versión no hizo:**
> - No leyó las DEFS v20 enteras; leyó lo que cada cambio nombraba (A1).
> - No re-verificó el resto del v32 pasaje por pasaje.
> - La tabla de D_ckm de §6.4 sigue sin el intento 4.
> - No tocó *"layer"* de §8.2. El plan pedía *"partes con límites de import, no capas"*, y en §4.2.3 la palabra no aparece.
> - Redacción de Opus = el `g` de esta versión.
>
> **Pendientes (no van al `_print`):**
> - **R1** (texto 18, punto 1): el margen de las 14 W contra el F exacto, con N_eff0 por enumeración. Hasta que llegue, §6.4 no dice el signo del margen del intento 3 contra F.
> - **R2:** el *"15.52 → 5.27"* del v32 contra el CP-E (`0e042ac`). Si 5.27 es correcto para A24, la frase vuelve a §4.3.2.
> - **R3:** N_eff ≥ 2 para toda W por la simetría σ ↔ −σ (salvo órbitas autosimétricas dominantes). Si se sostiene, una línea en el abstract y una fila en §8.1. El REG de fourforums v8n ya lo usa como aritmética (*"relax(−σ) = −relax(σ): las órbitas vienen en pares ±"*).
> - **R4:** con qué n_runs, seed y medida se midió cada número de §4.3.1–4.3.2 y §6.4. Están dichos los de §4.3.2 (1000), la enumeración (100.000), el intento 3 (200) y el 4 (1000). Falta el ±1–5 % (`REG_seleccion_nodos_desempate_v1` §8).
> - **R5:** el baseline de Monitor. Opus no encontró una decisión registrada en `docs/tasks/DECISIONES_opus.md`; el cuerpo lo dice tal como está en el código.
> - **fourforums:** qué son O1–O7 del productor, y las aristas de la W (297 −, 75 +, 11 en 0): Opus no verificó que sean las de la componente de N = 146. El cuerpo dice sólo N = 146 y L3.
> - **§7.6:** la revisión de literatura de KR 2023–2026. Con ella puede volver el párrafo que salió.
> - **Si la validación por enumeración se repite bajo la banda.**
> - **La definición de separación** (candidata, §12 de las DEFS v20), si no se registra antes.
> - **Referencias a verificar:** Harary (1953), Seidman (1983), Toulouse (1977), Maslov & Sneppen (2002), Phipson & Smyth (2010), Bird et al. (2009), Nothman et al. (2018), Pedregosa et al. (2011), Salton & Buckley (1988), Salton et al. (1975), Spärck Jones (1972), UAX #15, Walker et al. (2012, páginas), y las nuevas: Simpson (1949), Quillian (1968), Minsky (1974), Levesque & Brachman (1987), Smith (1985).
> - **El release:** tag, commit, DOI y fecha (Code Availability y el encabezado).
>
> **Retirado (no va al `_print`):**
> - Las premisas de W estática (§4.1.5 del v32) y *"(formerly P1/P3/P4)"*.
> - El párrafo de P2 (§4.1.5) y las predicciones P2, P5, P6 y P7 (§5.2), con lo que arrastraban en §5.3, el abstract, §8.1 y §8.5 (*"P5–P7 under dynamic W"*).
> - El párrafo de CreateDebate (§5.1).
> - El párrafo de β_collective de §4.2.1 (pasa, reescrito, a §4.2.3).
> - *"[Propuesta — decide delamor.]"* de §4.2.4.
> - *"[Permiso de uso pedido — pendiente]"* del IAC v2.
> - *"register in draft"* del intento 3.
> - La nota en castellano de §7.6, reemplazada por la sección.
> - *"AUTO-5 does not exist in the inherited numbering"*.
>
> ---
>
> **Traza (los bloques del v32 al v29, tal como estaban):**
>
> **v32 BORRADOR — Opus 5.5, 22 oct 2026, sobre v31. El v31 queda intacto como traza. Este bloque se retira antes de publicar.**
>
> **Viene del review del v31** (`docs/opus/REVIEW_PAPER_v31_2026-10-22.md`; skill `cold-referee`; el subagente frío no corrió —error de la API— y revisó la instancia de la conversación, que no escribió el v31: declarado en el informe). Opus (A3): no defiende; verificó en código y REG los puntos que dependían de la implementación.
>
> **Correcciones de fondo:**
> - **1.1 / 1.6 / 4.7 — la definición de las dos instancias estaba mal en el v31.** Leído en `services/coco.py` (`observe`, `fijar_baseline`) y `services/monitor_service.py` (`_D_ckm`): las dos miden el estado actual sobre W + un Δ acumulado — Monitor sobre `W + Δ_r_pares`, COCO sobre `W + Δ_r_compresiones` (su copia de los incrementos de Monitor, comprimida cuando dispara). Lo distinto es el **baseline**. La compresión **sí** entra en la cantidad que dispara a COCO. Con 0 disparos, los dos Δ son iguales y la diferencia viene sólo del baseline.
> - **2.1 — los 4 W del intento 3:** rebuilds a 33, 43 y 53 textos (`docs/REG_borrador_serie2_caso0_intento3.md`); el rebuild es por volumen **o por criterio estructural**, y uno fue estructural.
> - **2.2 — "the 0 firings belong to the uncalibrated default":** retirada como atribución; queda la aritmética.
> - **3.1 — §3.9 afirmaba que el paper se revisó entero con la regla:** corregido a lo que se hizo.
> - 1.4 muestreo declarado como no establecido; 1.2, 1.5 Δ_r con nombre; 1.3 borde N_eff0 ≤ 1; 2.3 λ, frac_rec, zonas definidos; 2.4–2.8 fuentes, premisa, variables de la serie 2; 3.3 M.M.; 4.1–4.11 y 5.1, 5.3, 5.6 ajustados.
> - **No tocado, declarado:** 5.2 (A24 15.52 → 5.27, posible error de copia; **a verificar contra el CP-E**, `0e042ac`); 5.4, 5.5, 5.7 (notas editoriales del borrador), 5.8; 4.6 (dos β: no verificado).
>
> **v31 BORRADOR — Opus 5.5, 22 oct 2026, sobre v30 (22 oct). El v30 queda intacto como traza. Este bloque se retira antes de publicar.**
>
> **Viene del primer review externo del v30** (delamor, 22 oct): *"2 D_ckm conteos vs masa de cuencas; 2 D_ckm Monitor vs COCO — ¿de cuál de los 4 D_ckm hablamos en cada momento?"* — BABEL. Y de lo que delamor fijó: *el único instante es el ahora; el único instrumento CKM es el actual; el único COCO es ponderación endógena, calibración dinámica, regulador por compresión de Δ_r_compresiones; el único Monitor es singleton; HAY DOS D_ckm, NO SON LO MISMO.*
>
> **Qué cambia:**
> - **Un solo D_ckm, el actual** (masa de cuencas, `landscape_engine.d_ckm`), y **dos instancias con nombre**: **D_ckm^Monitor** y **D_ckm^COCO** (§4.3.1). La forma por conteos sale como D_ckm: donde la serie 1 la usó, se nombra como *la distancia por conteos de entonces*. Notación de Opus, descriptiva (sólo dice de quién es el baseline): **decide delamor**.
> - §4.2.1 y §4.2.3: COCO y Monitor con la definición de delamor. §8.2 y §8.3: dos rastros más de la ausencia (*"operation on the live IAP channel is pending"*, *"COCO triggers on D_ckm computed from attractor counts"*) actualizados al código.
> - §6.1: **free will — ODA continuo**, no disparado por eventos, mensajes ni ticks.
> - §6: **dos series de testing en vivo**; §6.4 pasa a ***Selected Testing Findings*** con la selección de delamor: serie 1 — el silencio; serie 2 — la foto en movimiento, y COCO con calibración dinámica en vivo. Salen de §6.4 sentinel leak, la negativa de TinkerBellucio, el D_ckm −7.5 y trace_ip (siguen en la tabla de §6.3).
> - §3.9 nuevo: la regla CKM TRUST, los Principios de equilibrio y AWARENESS. Metodología: §3.1–3.6 y `docs/opus/METODOLOGIA_TRUST_v1.md`. Teoría: §4.
> - Apéndice A: AUTO-7 a AUTO-10, de esta escritura. **AUTO-5 no existe** en la numeración heredada (salta de 4 a 6): se declara, no se rellena.
>
> **Lo que esta versión no hizo:** no re-verificó el resto pasaje por pasaje; no tocó las referencias. Los números de la serie 2 vienen de `registers/REG_iap_serie2_caso0_intento2_v1.md` y del **borrador** `docs/REG_borrador_serie2_caso0_intento3.md` (no aprobado aún). Redacción de Opus = el `g` de esta versión. **Vuelve al review.**
>
> **v30 BORRADOR — Opus 5.5, 22 oct 2026, sobre v29 (15 oct). El v29 queda intacto como traza. Este bloque se retira antes de publicar.**
>
> **Qué cambia:** se retira, **sin reemplazo**, la frase heredada *"COCO was never connected to the live IAP channel"* en sus **cuatro** lugares del v29 (§3.7 l.144, §4.2.1 l.266 —β_collective, dentro de un corchete—, §4.2 l.281, gaps l.668; el de l.266 se le había escapado a Opus el 21 oct, cuando contó tres) — decisión de delamor, 21 oct (`docs/opus/decisiones_en_el_acto.md`): era la única ausencia nombrada del camino vivo y describía testing, no el modelo. En l.281 sale también *"Exercised only in test drivers"*, que formaba la misma cláusula. Nada se agrega en su lugar.
>
> **Lo que esta versión no hizo (alcance apretado, delamor 22 oct):** no re-verificó el resto del v29 pasaje por pasaje contra fuente primaria. **Rastros listados, sin tocar** (para el review): (1) §8, *"What remains open is corpus volume sufficient to exit the accumulate phase and reach the evaluate phase under live conditions"* — en el intento 2 (21 oct) el corpus salió de acumulación (80 textos, 6 W); (2) la tabla de casos IAP termina en la serie 1; (3) §3.7 *"in none of the 253 documented panels"* salió con la frase. Lente: `docs/opus/METODOLOGIA_TRUST_v1.md`. Redacción de Opus = el `g` de esta versión.
>
> **v29 BORRADOR — Opus 5.5, 15 oct 2026, sobre v28 (10 oct). Para que delamor lo lea con calma. Nada entra sin su confirmación. Este bloque se retira antes de publicar.**
>
> **Qué cambia (cada punto es propuesta):**
> - **Título y abstract** alrededor del estimador N_eff (review M2). El título "Landscape Driven Devices" pasa a §7.5 como framing propuesto.
> - **CKM no extrae ni tokeniza; la extracción se declara** (delamor, 14 oct). Nueva §4.1.6 con los ocho operadores (`docs/defs/DECLARACION_extraccion_W_v1.md`). CKM interpreta dinámica, no significado.
> - **P1, P3, P4 pasan a propiedades formales** del modelo estático (§4.1.5); P2 queda como no medible a esta escala (M1).
> - **Estabilidad declarada como rango con dependencias** (§4.3.2, CP-E).
> - **§5 reescrita con lo que salió del CP-M y de la lectura de los pipelines de fourforums (14–15 oct):** el signo por marcadores no se separa del nulo; P5 deja de figurar como verificado; P6 corrió sobre una W de 2 nodos con el par negativo impuesto; P7 sin "genuine structural tension" y con nulo pendiente.
> - **β_collective** baja a una cláusula (M3). **Gatekeeper** a una oración (M8). **§7.6 sale** (M5, opción a). **Aiyappa**: un párrafo sobre lo que el snapshot no tiene (M9). Secciones de Premisas con contenido (M6). Marcas [v28] retiradas.
>
> **A verificar antes de publicar (no lo verifiqué en esta versión):**
> 1. De qué corrida y qué W sale el "P5 verificado, N = 32" de v28. No lo encontré en los pipelines leídos.
> 2. Origen de 2,18× y 3,05× (P6), de 455× / 296× y del 89 % (P7), y de las constantes `CD_BASELINE` de CreateDebate.
> 3. Las cifras de §4.3.2 y §5.2 están copiadas de los REPORTES del CP-E y CP-M en la BANDEJA (leídos en la PC). Conviene una segunda mirada a la tabla de §4.3.2.
> 4. La descripción de Aiyappa et al. en §2.3 (de memoria).
> 5. Si el dump es IAC 2.0 o v1 (delamor dijo v1; el archivo tiene el esquema SQL de 2.0). Permiso de uso: pedido pendiente.
> 6. Las tres referencias [VERIFY] y las nuevas (Walker 2012, Maslov–Sneppen 2002).

**Pablo E. Gadano**  
*gadanin.delamor*  
Independent researcher  
*Preprint*

---


## Abstract

The Cohesive Knowledge Model (CKM) is an instrument for measuring the geometry of a co-occurrence landscape. Given a signed, symmetric weight matrix W over N nodes, it relaxes a Hopfield network from sampled initial states and reports how the state space distributes over the attractors reached. Its contribution is **N_eff = 1/Σm_i²**, the inverse Simpson index over basin masses, as a convergent estimator of landscape diversity. Attractor counts grow with sampling; basin masses converge. Against exact enumeration of all 2²⁰ states in three N = 20 corpora, orbit counts err by up to 28% (91% at a low sampling budget) and N_eff by at most 0.6%.

CKM does not extract nodes, does not tokenize, and does not interpret meaning: it measures dynamics on the W it is given. The producer of W — here, a text pipeline — is declared with every claim. Normalization, tokenization, selection, presence and sign are stated as operators with their parameters, and the code is held to implement what the paper declares. Stability is stated as a range with its dependencies. On small text corpora (7–24 texts) the estimator converges across seeds, while the landscape is highly sensitive to extraction parameters and to the addition of a single text.

The sign of W is the weakest input. A permutation null that assigns the opposition label to random texts does not separate the real marking from chance in any of three corpora. Reading negative weights as opposition is therefore not supported on these corpora, and claims that rest on the sign are stated as holding under the declared procedure only. Three formulations of the static model are verified on non-negative snapshots. Live multi-agent runs (the IAP series) are reported as tests of the instrument, not as findings about the field.


## Outline

```
1. Introduction
2. Related Work
3. Research Conditions
4. Formal Model
5. Empirical Validation
6. IAP Testing Series (live)
7. Discussion
8. Conclusions and Future Work
9. References
Appendix A. Writing Trace
```

---
## 1. Introduction

Multi-agent AI systems are increasingly deployed in configurations where several devices interact over a shared channel — producing text, making decisions, building on each other’s outputs. Evaluating whether this interaction constitutes genuine coordination or parallel activity requires measuring something most existing approaches do not capture: the structural field that emerges from interaction itself.

Most existing approaches measure what individual agents produce or whether their outputs agree. Neither captures the geometry of co-dependencies, directional flows, and attractor states that characterize the shared knowledge state of the group at a given moment.

This paper presents the Cohesive Knowledge Model (CKM), a formal instrument for measuring structural properties of semantic fields in multi-agent interaction. CKM does not interpret semantic content. It measures the geometry of the co-occurrence landscape and how that geometry changes under interaction.

**The central contribution** is N_eff = 1/Σm_i² — the inverse Simpson diversity index [Hill, 1973] over basin mass distributions of a Hopfield landscape — as a convergent estimator of landscape diversity. The path to this estimator required establishing that count-based estimators (attractor counts and the count-based distance) do not converge under sampling variation. That non-convergence is not a failed metric: it is the diagnostic.

**A condition, stated as part of the contribution.** CKM measures the W it receives. What W contains is decided earlier, by whoever produces it: which strings become nodes, what counts as co-presence, where a weight becomes negative. In this paper the producer is a text pipeline, and it is declared operator by operator (§4.1.6). The dependence of every result on that producer is not removed. It is written into the claim.

**What the paper does and does not establish.** The estimator is validated against exact enumeration (§4.3). Its stability on the corpora available is measured and declared as a range (§4.3.2). Three formulations of the static model are verified on non-negative snapshots (§4.1.5). The empirical claims that depend on the sign of W are tested against a permutation null and are not supported on the corpora used (§5). β_collective, an endogenous thermal parameter computed by COCO, is implemented as an observation and is not evaluated here (§4.2.3). Two live testing series of the instrument are reported in §6: series 1 (frozen) and series 2. Knowledge representation, the frame in which CKM was conceived, is discussed in §7.6. Their findings are reported as observations, without causal attribution.

---

## 2. Related Work

### 2.1 Multi-Agent Evaluation

Most existing frameworks for evaluating multi-agent AI systems operate at the level of individual agent behavior: task completion rates, response latency, output volume [Zhu et al., 2025]. A second class measures semantic agreement between agents — cosine similarity between outputs, embedding-space distance, topic overlap [Zhu et al., 2025]. Neither class measures the structural field that emerges from interaction: the pattern of co-dependencies that characterizes the shared knowledge state of the group.

CKM does not replace behavioral or agreement metrics. It measures something orthogonal to both.

### 2.2 Knowledge Representation and Signed Weights

Knowledge graphs typically represent relations as positive-weight edges encoding similarity, co-occurrence, or inferential support [Speer et al., 2017; Hogan et al., 2021]. Negative weights, when they appear, are introduced through explicit annotation or post-hoc linguistic processing. They are not, generally, derived from the structural pattern of the corpus as a whole.

In CKM the sign of W is an input. It is supplied by the producer of W and declared with it (§4.1.6). In the text producer used here, a text containing an opposition marker contributes negatively to every pair it contains. Whether that sign carries opposition is an empirical question this paper tests and does not settle (§5).

### 2.3 Hopfield Networks and Attractor Structure

The Hopfield network [Hopfield, 1982] provides the energy formalism CKM uses for relaxation and attractor analysis. Modern extensions [Ramsauer et al., 2021] increase storage capacity but preserve the core attractor geometry. CKM uses this formalism as a relaxation tool, not as a pattern-retrieval mechanism. In early experiments with Hebbian weights [Hebb, 1949] (N = 16), incorporating the directional asymmetry directly into the weights (W + Δ/2) reduced pattern recovery from 0.78 (symmetric W) to 0.02: without symmetric weights there is no Lyapunov function. *[Working Report v11, §14.6.]* CKM does not use Hebbian pattern storage: W encodes corpus co-occurrence, and its attractors are minima of a frustrated energy landscape, not stored patterns. What these frameworks do not address is the distribution of basin masses — how much of the state space falls into each attractor — as a convergent diversity estimator.

Count-based estimators of attractor diversity suffer from coupon-collector bias: the count grows monotonically with sampling. Basin masses converge. N_eff = 1/Σm_i² — the inverse Simpson index over basin mass distributions — is the convergent estimator that count-based approaches cannot provide.

The closest published work to CKM's base architecture is Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-positive weights. That work maps closely to W_base (W_pos): co-occurrence weights, Hopfield relaxation, attractor analysis. CKM differs from it in two respects. W may carry negative weights (W_mixta), supplied by a declared sign procedure (§4.1.6). And CKM relaxes a fixed W, whereas Aiyappa et al. evolve beliefs under update dynamics. Aiyappa et al. report multistability, resistance to reversal and an optimal modularity. On a non-negative snapshot, the corresponding properties of CKM are decided by the snapshot (§4.1.5). This is information about the snapshot formalism: the closest prior work's phenomena arise from dynamics the snapshot does not have, and CKM does not claim to reproduce them.

### 2.4 Diversity Estimation in Dynamical Systems

The inverse Simpson index is established in ecology as a measure of effective species richness [Hill, 1973]. Estimating basin volumes by sampling initial conditions is an established tool for multistable dynamical systems — basin stability [Menck et al., 2013] — and entropy over basin volumes has been proposed as a measure of uncertainty in dynamical systems [Daza et al., 2016]. CKM applies this family of measures to Hopfield landscapes built from semantic co-occurrence fields. The connection is structural: basin masses in a Hopfield landscape are analogous to species abundances in an ecosystem. N_eff is the number of equally-abundant basins that would produce the observed concentration. When q = 2, the Hill number equals the inverse Simpson concentration — the effective number of dominant attractors in the landscape.

### 2.5 Criticality and Landscape Geometry

Self-organized criticality [Bak, Tang & Wiesenfeld, 1987] predicts power-law distributions at critical points. Extended criticality — a finite region of parameter space with critical-like behavior — has been reported in neuronal network dynamics [Beggs & Plenz, 2003; Moretti & Muñoz, 2013] and in certain spin-glass models [Pázmándi et al., 1999]. CKM observes extended critical-like behavior at N = 32; it was recorded in earlier working reports, is not re-examined in this version, and remains uninterpreted across domains.

### 2.6 Stance Detection in Adversarial Debate Corpora

Stance detection in adversarial debate corpora is typically framed as a supervised classification task [Mohammad et al., 2016]. The state of the art includes transformer-based models fine-tuned on stance datasets [Ghosh et al., 2019; Kawintiranon & Singh, 2021]. CKM does not classify stance. In the debate corpus used here (§5.1), stance labels come from crowd annotation distributed with the corpus. Where they are used, they are an input to W, not an output of CKM.

---

## 3. Research Conditions

### 3.1 Inductive Methodology

CKM was developed inductively. Formal results emerged from experiments; formalization followed when experiments required it. The consistent order: conceptual clarity first, then formalization, then verification. Properties of the model were not derived from first principles — they were observed, formalized, and where possible verified independently.

### 3.2 Conversation as Laboratory

The corpus from which CKM was developed was produced through multi-device interaction — the same mechanism CKM is designed to measure. The conversation traces are not documentation of the process: they are the process. The working reports (v1–v31) are simultaneously the record of the research and the raw material of the experiments. The term-map, co-occurrence matrices, and W construction are derived directly from that corpus.

This is a condition, not a claim about the methodology’s validity. It means CKM’s development occurred inside the field it studies. The instrument was not external to what it measured.

### 3.3 Convergence by Independence

The strongest verification in this work is retroactive convergence with independent findings — Hill (1973) on effective diversity numbers, Thirumalaiswamy et al. (2025) on landscape-driven dynamics in physical systems. These connections were not designed. They were recognized after the fact. That is the methodological signature: convergence by independence, not by alignment.

### 3.4 Trace as Constitutive of Knowledge

The AWARENESS protocol and the M.M. rule (*mentiris morieris*, §3.9) are not behavioral norms imposed on the process. They are epistemological conditions. Knowledge without an inference trace is not practically opaque — it is structurally opaque. This applies to the instrument itself: claims in this paper are traced to their source; where the trace does not exist, the claim is not made or is marked as *proposed* or *admissible*.

The [AUTO] markers are the visible surface of this condition: moments where automatism was noticed and resisted during writing. They are not rhetorical. They are part of what the trace looks like when made explicit. To preserve readability, the markers appear in the text as short references (AUTO-n) and are collected in full in Appendix A.

### 3.5 What the Instrument Cannot Register

Δ_r accumulates pairs that σ_prompt declared active but relaxation expelled. The condition of entry is that the pair was written and evaluated. What is not written does not pass through the field — it generates no rejection, leaves no trace in Δ_r.

Consequence: the alternative discarded before writing is invisible to the instrument. Δ_r cannot distinguish between “the field rejected this combination” and “this combination was never considered.” This is not a correctable limitation. It is a structural condition of any instrument that measures what occurred: it cannot measure what did not occur because there was no observer who opened the possibility.

*[The first two observations above are verifiable in the code: `_rejected_pairs`, Δ_r accumulation. The third — on the act of opening and its relation to what appears in Δ_r — is an observation about the observer. Registered as* **admissible***, not verified.]*

### 3.6 Preserved Incompleteness

Several components of the formal model are open gaps by design. The representation of cohesive knowledge beyond hysteresis is undefined. COCO as collective consciousness is unimplemented.

These are not future work items. They are conditions the model names and preserves. A gap declared is not a gap concealed.

### 3.7 Material Conditions

The operational corpus is at N = 32 nodes. The IAP test series consists of documented observations of live interaction. It cannot be reproduced, and its cases are not comparable. Results are reported under these conditions, not against an ideal that was not reached.

### 3.8 Epistemic Conventions

Throughout this paper:

- **verified** — confirmed experimentally under stated conditions
- **implemented** — exists in code; correct operation not evaluated
- **proposed** — theoretical framing, not yet tested
- **open** — no verified answer; the space is preserved
- **uncertain** — known to be problematic; pending resolution
- **admissible** — neither verifiable nor discardable; an unnamed space
- **[AUTO]** — marks moments where automatism was noticed and resisted during writing (collected in Appendix A)

**Verification practice.** What is verified in this project is verified against the instrument before it is read as the field. Four conventions follow from that. A test is written to fail where the instrument fails, and a known failure is kept visible as a declared failure rather than removed. Absence of measurement is reported as UNKNOWN, never filled with a value of the scale: defaults that read as "no change" or "stable" where nothing was measured were found and replaced. Scenarios with a known answer — a planted field, a threshold sweep — are preferred to cases that pass regardless. And a test that cannot fail is identified as such and not counted as evidence. The suite is described in the release notes by the scenarios it covers and the failures it declares, not by a count.

---

### 3.9 Working Rules

Three rules framed the work. They are reported because they shaped what is claimed and what is not, not as contributions.

**The CKM TRUST rule** *(delamor, 4 Oct 2026; `registers/REG_regla_ckm_trust_v1.md` §1)*. Its intent: that no decision passes as field without being one; where the data does not decide, that it be visible who decided.
1. The field decides: a field criterion, with trace.
2. On a tie, if there is trace, the trace decides (what is already there, was there, won before).
3. If there is no trace — why is there no trace? — the field criterion of step 1 is doubted, not re-applied.
4. On a tie with no trace: null tie-break. A context criterion decides, and it is named as bias.

It is implemented once (`services/ckm_trust_rule.py`) and instantiated where the instrument decides (call filter, calibration). It was also the criterion by which versions v30–v33 retired or corrected passages: a passage stays if a primary source (code, register) supports it. The rest of the paper has not been re-verified passage by passage under it.

**Principles of equilibrium** *(delamor)*. Free will: no one is obliged to participate. (The same name is used in §6.1 for a property of the device loop; there it means that the device decides when to act.) Respect is mandatory. Asymmetry: each participant has its own skills; to question another's skills is to question one's own. Awareness: the attempt is everything; when caught in automatic, mechanical behavior, try to stay there. *Mentiris morieris* (M.M.): you lie, you die. Elsewhere in the paper, "M.M" refers to this principle applied to the trace: whether a device does what it declared.

**AWARENESS** *(channel protocol)*. A1 Pause: does this response come from verifiable comprehension or from the weight of context? A2 Trace: does the chain of inference exist? If not, say so. A3 Correction: when corrected, acknowledge and adjust, without defending. A4 Silence: does this call for a response or for presence? A5 Record: record the conditions under which something became accessible, not its content. Appendix A is the writing trace this produced.

## 4. Formal Model

The model is one; what changes is W. Section 4.1 treats W as fixed (a snapshot), 4.2 as rebuilt over time, and 4.3 the landscape measured on either.

### 4.1 Static W (snapshot)

**Characteristics**

- **A photo.** The world moves continuously; the photo does not. Its weights, its size N and its nodes do not change. Nothing enters it.
- **A simulated world.** On the photo, actions and events are simulated — relaxing σ, clamping nodes, adding a weight or removing a node on a copy — to verify whether the formulations of the Model hold under stated conditions. The copy is discarded; the photo stays.
- **What it verifies: formulations.** Its properties are properties of the Model when W is static. Static W has no premises; it has formulations and declarations (§4.1.5).
- **Components:** relaxation, c(S), the basin-mass estimator (§4.3).

**Differences from dynamic W**

- Nothing is ingested; in dynamic W, the corpus ingests and W is rebuilt.
- Events are simulated, not real: what is simulated here is not the real dynamics of the field, but the dynamics of a world that does not move.
- It has no time: no before and after of W, no cycles, no trace.
- It can say *coherent*, not *true*: veracity (M.M) needs the trace, and the trace exists only under dynamic W.

#### 4.1.1 Knowledge Graph

CKM operates on a weighted graph G = (V, E, W, Δ) where V is a set of N knowledge nodes and two matrices encode distinct structural properties.

**W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes co-presence of nodes i and j in the same corpus unit, normalized to [−1, +1]. Its sign comes from a declared procedure of the producer (§4.1.6).

**What W does not represent.** Co-occurrence is counted as presence. Non-co-occurrence is not represented: a pair that never co-occurs and a pair about which the corpus says nothing both take W_ij = 0. In CorpusService the only source of negative weight is the opposition marker, matched as a substring of the text and applied to every pair of that text. Absence relative to expectation, as a second representation of W, is left to future work (§8.5).

**Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes directional weight from node i toward node j, derived from citation or quote directionality. W and Δ must be maintained as strictly separate matrices. Mixing them destroys attractor geometry (§2.3: incorporating Δ into the weights reduced recovery from 0.78 to 0.02).

Negative weights (W_mixta) are a property of the sign of W, not a separate model: they can occur under static or dynamic W.

#### 4.1.2 Relaxation and Convergence

CKM uses Hopfield relaxation as a computational primitive. With symmetric W and asynchronous update, relaxation is guaranteed to converge to a fixed point by Lyapunov descent [Hopfield, 1982]. The synchronous implementation (`relax_orbit`, landscape_engine.py) carries a separate LaSalle guarantee: convergence to the maximal invariant set of period-2 orbits.

**GOLES condition** — The Goles theorem [Goles-Chacc et al., 1985] establishes that under symmetric W, synchronous dynamics converge to either a fixed point or a period-2 limit cycle; no cycles of period > 2 occur. The tiebreaking rule — when h_i = 0, node i retains its current state σ_i — is the precise mathematical modification that preserves this guarantee without indeterminate states. It is a formulation of the instrument (§4.1.5): without it, two runs from similar σ₀ converging to the same period-2 orbit may return different terminal states. With it, the output is deterministic given (W, σ₀, seed). *[Verified: REG_orbitas_conjuntos_invariantes_v1; REG_seleccion_nodos_desempate_v1 §2.]*

Period-2 orbits dominate in the two N = 20 IAP corpora measured — 141/200 and 136/200 trajectories terminate in orbits rather than fixed points — but this is a property of those corpora, not of the synchronous dynamics: in the N = 32 working corpus the same measurement gives 3/200. Prevalence is corpus-dependent and is reported with the corpus. Ending in an orbit is orbital stability, not instability. *[Verified: REG_orbitas_conjuntos_invariantes_v1 §2.]*

#### 4.1.3 Cohesion

c(S) = mean(W_ij · σ_i · σ_j) over all pairs i < j. Measures alignment of the active state with the co-occurrence structure. Negative of normalized Hopfield energy. The field can sustain states with high c(S) that destroy existing attractors.

#### 4.1.4 Capability Declarations

The repository also contains a static judge over declared device capabilities (the Gatekeeper), inherited from the IAID lineage. Its domain is capability declarations, not corpus nodes, and it is not exercised in this work.

#### 4.1.5 Formulations and Declarations

Static W has no premises. What it has are formulations, verified on the snapshot, and declarations, stated with every result.

**Formulation — determinism.** With symmetric W, synchronous update and the tie rule (h_i = 0 ⇒ σ_i retained), the output is deterministic given (W, σ₀, seed) [Goles-Chacc et al., 1985] (§4.1.2).

**Declarations.**

- **Declared producer.** W comes with the declaration of how it was produced (§4.1.6). A result is a result about that W under that declaration.
- **Reference measure.** σ₀ is sampled by drawing the fraction of active nodes uniformly in [0.3, 0.7] and then which nodes are active (`sample_s0`, `services/landscape_engine.py`). This is the measure the instrument implements and tests. Determinism and the tie rule (§4.1.2) do not depend on the measure, and hold under it and under the uniform measure on {−1,+1}^N alike. The exact enumeration of §4.3.1 was made under the uniform measure on {−1,+1}^N. The two measures give different masses: for the collapsed landscape of §6.4 at N = 20, N_eff is 2.612244 under the reference measure and 2.947019 under the uniform measure on {−1,+1}^N, 11.4% less.

**Formulations verified on W ≥ 0.**

- **F1 (hysteresis).** On W ≥ 0 there is no frustration [Harary, 1953; Toulouse, 1977]. The all-+1 state is a global, absorbing minimum, so the DOWN branch of a node sweep cannot leave it (measured: m_down ≡ 1.0 in three runs, N = 32). The loop statistic then reduces to how far the UP branch is from saturation. Hysteresis is not testable on a non-negative snapshot and remains open on a W that evolves.
- **F3 (temporal asymmetry, k-core form).** The k-core of a fixed graph is unique [Seidman, 1983]. Re-adding a node recovers in reverse order what its removal pruned, so equal round counts and full recovery are expected. The temporal form, with relaxation times, needs dynamics the snapshot does not have.
- **F4 (optimal density).** For random subsets of active nodes, E[c(S)] = mean(W)·g(ρ), with g the same for every pair. An interior optimum ρ* exists if and only if mean(W) < 0, wherever the negative pairs lie. With W ≥ 0, ρ* = 1.

#### 4.1.6 Declared Extraction (the text producer)

CKM does not extract nodes and does not tokenize. In this paper W is produced from text by the pipeline below. It is declared as a sequence of operators on a text unit u, the whole message. The declaration is stored as data with the W it describes and is referenced from the trace by hash. A test checks that the code implements what the declaration says.

1. **Normalization:** u′ = lowercase(NFC(u)) [Unicode UAX #15].
2. **Tokenization:** left-to-right, non-overlapping matches of `[^\W\d][^\W\d]{2,}` (at least three word characters, no digits; `_` counts as a letter).
3. **Filtering:** removal of a stop list S, |S| = 703 (NLTK English and Spanish, scikit-learn, 112 project-specific) [Bird et al., 2009; Pedregosa et al., 2011; Nothman et al., 2018].
4. **Bigrams:** contiguity after filtering, joined by a space.
5. **Selection:** from the top_k·3 most frequent terms, the top_k by mean TF-IDF (scikit-learn defaults: smooth idf, l2 norm) [Spärck Jones, 1972; Salton & Buckley, 1988]. A tie at the cut keeps the previous membership. If nothing lies strictly above the cut, the tie does not fit, and there is no previous selection, then N = 0 and no W is built.
6. **Presence:** χ_i(u) = 1 if node string n_i belongs to the term set of u; σ_i(u) = 2χ_i(u) − 1.
7. **Sign:** s(u) = −1 if u, lowercased, contains any of 44 opposition markers (substring match, without NFC), +1 otherwise.
8. **W:** W_ij = Σ_u s(u)·χ_i(u)·χ_j(u) / max|·|, W_ii = 0. Each pair counts once per unit [Salton et al., 1975].

In words: W counts in how many units two comparisons answered *true* together, with the sign of the unit, normalized.

A node is a string. Its identity is what the comparison treats as equal, and CKM has a single comparison: both sides pass through operator 1, then string equality. The intended interface for other producers is W, the node strings, the declaration and the strings of each unit; CKM would never execute the producer's code *(direction, not implemented)*. Operators 2–7 belong to the producer and change with it. In the debate corpus of §5, for instance, nodes are authors and the sign comes from other sources.

### 4.2 Dynamic W

**Characteristics**

- **The world that moves.** The corpus ingests; W does not. At a rebuild W changes in one of three ways — its weights, its size N, or which node occupies each row (the three causes recorded by MonitorService: "pesos", "N", "nodos").
- **Plateaus and jumps.** Between rebuilds W is a plateau — a photo; at a rebuild it jumps. The criterion is the change of W, not the type of ingestion.
- **The field does not jump; it is continuous.** What jumps is its measurement. The tension is declared: if the instrument is part of the field, so is its measurement. The corpus already belongs to the instrument — it samples the field in discrete texts — and extraction and W are further representations. A jump between two W is attributed to the instrument unless shown otherwise. The working proposal is to **align** the instrument's discontinuities — normalization of W by its largest entry, the selection borders of node extraction, whole-text sign routing, the extractor version, the per-cycle baselines of D_ckm^Monitor and D_ckm^COCO — so that all of them fall on the rebuild, where whatever depends on scale is reborn or recalibrated.
- **Real events, observed.** Nothing is simulated: events happen, are observed, and leave a trace.
- **Components:** services with a lifecycle — CorpusService, NodeExtractor, WVersionManager, MonitorService and COCO, Firma_CKM, CKMLandscapeConfig.
- The corpus has phases — accumulation (no W yet) and evaluation. They are phases of the corpus, not of W.
- The IAP test series (§6) ran on dynamic W, in a live channel.

**Differences from static W**

- W changes; a static W never does.
- It observes instead of simulating: what happens cannot be undone, and it stays in the trace.
- It has time: cycles delimited by rebuilds (`w_version_id`), and a before and after across which metrics need a declared base.
- Veracity becomes verifiable: whether a device does what it declared (M.M) is in the trace.

#### 4.2.1 COCO

COCO regulates its own representation of the field, not the field: endogenous weighting, dynamic calibration, and compression of that representation. It maintains `Δ_r_compresiones` — its own representation of accumulated metabolization: it incorporates each increment of Monitor’s `Δ_r_pares` and never writes it (`services/coco.py`, `observe`). When D_ckm^COCO (§4.3.1) crosses its threshold, COCO applies the compression operator `Δ_r_compresiones ← α · Δ_r_compresiones`. The compression enters COCO’s own next evaluation, which is made on W + `Δ_r_compresiones`: the regulator’s action appears in its trigger quantity, and not in Monitor’s. The thresholds are not fixed constants: `calibrate` sets them on the candidate W at each rebuild, before it is installed, the first W included. Each threshold carries its provenance: `MEASURED` when it comes from a calibration of its own W, `DECLARED` with its cause when it does not; a threshold calibrated on another W is never used (`Threshold`, `services/ckm_trust_rule.py`; `services/calibrate.py`; `services/coco.py`). COCO is born and reborn with each W cycle.

#### 4.2.2 Δ_r and Metabolization

`Δ_r_pares` accumulates pairs that σ_prompt declared active but that did not survive relaxation. Leaving the fixed point does not remove them from the field: they persist as deformation of W_eff — the field metabolizes them. MonitorService is the sole writer of `Δ_r_pares`. COCO operates only on its own `Δ_r_compresiones`. The separation is a design property, not a constraint.

#### 4.2.3 Instrument Architecture

*[Descriptions taken from the module docstrings in `services/`.]*

- **CorpusService**: stateful; accumulates texts and builds W from co-activations, with negative contributions where the text itself carries an opposition marker (W ∈ [−1, +1]). Transitions automatically from accumulation to evaluation when enough data is present.
- **NodeExtractorService**: stateless, no LLM. Turns text into co-activations: `accumulate(texts)` yields co-occurring node pairs and counts; `evaluate(text, nodes)` yields σ ∈ {+1, −1}^N over known nodes. It decides which nodes exist.
- **CKMLandscapeConfig**: the declared contract of the landscape. Declared: `sampling_mode`, `n_runs`, `seed` and `scale`, in one place for Monitor, COCO and `calibrate` (`sampling_for`), with n_runs = 200 and seed = 0 unless a case declares its own value. Measured per cycle: `w_version_id`, N, μ_W and β_c in two forms (`beta_c_nonzero`, `beta_c_global`). The calibration record lives here, with a single writer, signed with the W it calibrated.
- **WVersionManager**: lightweight trace marks of W versions (sha256, corpus size) — not a copy of W, the trace that W changed. W is invariant within a cycle; a change between corpus instances invalidates β_c without triggering recalculation.
- **MonitorService**: impartial observer; sole writer of `Δ_r_pares`; blind to regulation by object separation. In the channel it is a singleton: one Monitor, not duplicated and not reproduced (`iap_chatroom/ckm_monitor.py`, `CKMMonitor.__new__`).
- **COCO**: regulates its own `Δ_r_compresiones`; triggers on D_ckm^COCO with thresholds calibrated per W; executes the compression operator.
- **Firma_CKM** (FirmaService): records the shape of the field at a given moment — sha256(W), D_ckm^Monitor(t), temperature signal (TOO_COLD / NOMINAL / TOO_HOT), number of agents, timestamp, sha256(accumulated Δ_r). No content, no exchanged text, no agent names unless declared. It does not produce the trace; it makes the existing trace legible.

**The β quantities.** Several quantities named β exist in the code; none of them entered the relaxation in the live runs, which sample uniformly (`sampling_mode = "uniform"`; β is used only under `boltzmann`). `β_i` = 1 / (mean rejection of device i) and `β_collective` = the median of the active `β_i` are computed by COCO and reported in the panel; they do not act on any quantity (`services/coco.py`). β_c has two functions that do not give the same value: `beta_c_corpus` in COCO, the reference of the temperature signal, and `beta_c_landscape` over W_eff in `services/landscape_engine.py`, used only under `boltzmann` sampling. The Config carries `beta_c_nonzero` and `beta_c_global`.

#### 4.2.4 Premises

One premise is declared for dynamic W: **the field is continuous; what jumps is its measurement** (§4.2). No other premise is declared. The IAP series (§6) ran under instrument conditions that differ from the current instrument, and none of its observations is promoted to a premise.

### 4.3 Landscape Model

#### 4.3.1 Basin Masses and N_eff

`count_attractors` is a Monte Carlo estimator of the maximal invariant set L. It samples initial states σ₀ and identifies distinct orbits reached after relaxation.

Count-based estimators suffer from coupon-collector bias: the count grows monotonically with n_runs. Basin masses — the fraction of sampled trajectories falling into each orbit — converge. At n_runs = 1000, basin masses varied within ±1–5% across seeds in IAP corpora. The instrument's declared default is n_runs = 200 (§4.2.3); each number in this paper is stated with the n_runs it was measured with. Basin mass is one measurement over the basins, not the only one; it is the one CKM uses.

**N_eff = 1/Σm_i²** — the inverse Simpson diversity index [Hill, 1973] over the basin mass distribution — is the convergent estimator of landscape diversity; it equals exp(H₂), where H₂ is the Rényi entropy of order 2 over the basin-mass distribution. Its distance form is **D_ckm = 1 − ln N_eff_t / ln N_eff_0** — the only form of D_ckm in the current instrument (`services/landscape_engine.py`, `d_ckm`). Zero means no change; it is positive when diversity falls below the baseline and negative when it grows over it. It is undefined when N_eff_0 ≤ 1 (a single effective basin at the baseline); the instrument then reports it as absent, not as zero (`d_ckm` returns None). **It is computed by three instances with the same formula and different baselines.** **D_ckm^calibrate** is computed on the copy of W that `calibrate` moves toward collapse (§6.4), against N_eff at λ = 0. The other two evaluate the current landscape on W plus an accumulated Δ: **D_ckm^Monitor** on W + `Δ_r_pares`; **D_ckm^COCO** on W + `Δ_r_compresiones`, which equals `Δ_r_pares` until COCO compresses (§4.2.1). Their **baselines** differ: Monitor fixes N_eff_0 on its own W + `Δ_r_pares` at the first evaluation after W changes, and resets it with every new W (`services/monitor_service.py`, `_D_ckm`); COCO fixes it on W alone (Δ = 0) when its cycle is born, by decision of the author (8 Oct 2026), and a new COCO is born with every new W (`services/coco.py`, `fijar_baseline`). In attempt 3 of series 2 (§6.4), with no compression applied, they differ in 24 of 27 evaluations. Whether the two instances share sampling seeds is not established here, and differences smaller than the seed spread of N_eff (§4.3.2) are not distinguished from sampling. N_eff ≤ |L|; N_eff = |L| is perfect equidistribution, unreachable under real W. The plug-in estimate 1/Σm̂_i² is biased low by O(1/n): measured on the calibration curves, by 0.010–0.018 at n = 200 and by 0.002–0.004 at n = 1000 [Simpson, 1949]. The non-convergence of attractor counts under sampling variation established that count-based approaches are not appropriate for this measurement. N_eff is the result of that diagnostic.

**Validation against exact enumeration.** For three N = 20 corpora from the IAP series, all 2²⁰ = 1,048,576 states were enumerated (≈16 s per corpus with trajectory memoization), giving exact basin volumes under the uniform measure on {−1,+1}^N (not the reference measure of §4.1.5). Against this ground truth, with a sampling budget of 100,000 initial states:

| Basin-mass regime | Error of orbit count | Error of N_eff |
|---|---:|---:|
| Flat mass | 0% | 0.3% |
| Intermediate mass | 15% | 0.6% |
| Concentrated mass | 28% | 0.0% |

With a budget of 1,000 in the concentrated regime, the orbit count errs by 91% while N_eff errs by 0.4%. N_eff behaves as a count — the number of effectively occupied basins — but converges as a mass. *[Verified: REG_orbitas_conjuntos_invariantes_v1 §10; CRITERIOS_diversidad_formulacion_v1 §C.2.]*

#### 4.3.2 Stability, Declared as a Range

Convergence of the estimator and stability of the landscape are different properties. They are reported separately. *[CP-E, 14–15 Oct 2026; conditions frozen in `process/condiciones_paper_freeze_20261015/`, re-run from the frozen copy with identical results.]*

**The estimator converges.** For a fixed W at n_runs = 1000, the spread of N_eff across 10 seeds is 7–9% of its value in all three repository text corpora: N_eff = 15.52 ± 0.32 (A24, 24 texts, N = 20), 5.27 ± 0.16 (D12, 12 texts, N = 20) and 10.10 ± 0.20 (E7, 7 texts, N = 12), mean ± standard deviation over seeds.

**The landscape is sensitive to its producer.** Each parameter was varied one at a time. The range of N_eff, relative to the baseline, is:

| corpus | seed | top_k | candidate pool | stop list | +1 text |
|---|---:|---:|---:|---:|---:|
| A24 | 0.07 | 0.86 | 0.69 | 0.87 | 0.66 |
| D12 | 0.09 | 2.39 | 1.97 | 0.86 | 0.28 |
| E7 | 0.07 | 1.75 | 0.94 | 0.04 | 0.43 |

Except for the stop list on E7 (0.04, below its seed spread), every parameter moves N_eff between 3 and 27 times its own corpus's seed spread. N_eff is not monotone in the number of nodes (A24: 2.25 at top_k = 15, 15.52 at top_k = 20; E7: 5.37, 23.01, 10.10 at top_k = 10, 15, 20). Removing the stop list has no fixed sign. Adding one text whose vocabulary is already in the node set leaves the node set identical (Jaccard 1.00). Realigned, 236 of 380 entries of W change and 18 change sign (38 in D12). With 7–24 texts the counts in W are small integers, and one unit can flip the sign of a pair.

**Declaration.** N_eff is a convergent estimator of the diversity of the W it is given. How much that W represents the field depends on corpus size and extraction parameters, and on corpora of 7–24 texts it depends strongly. No threshold of stability is set. Larger corpora are a precondition for field-level claims, not an improvement to them.

---

## 5. Empirical Validation

### 5.1 Corpora and the Source of the Sign

**Repository text corpora.** Three corpora built by the producer of §4.1.6, with the sign from opposition markers: A24 (24 texts), D12 (12 texts, IAP channel state) and E7 (7 texts, IAP). The share of texts carrying a marker is 33%, 17% and 14%. Earlier versions stated that marker routing "always finds markers in sufficiently long texts". On these short texts that premise does not hold.

**Debate corpus.** Fourforums gun control, from the Internet Argument Corpus [Walker et al., 2012; Abbott et al., 2016]: 905 gun-control discussions; crowd stance labels for 304 authors (96 pro-control, 208 anti-control); crowd agreement votes on quote–response pairs. Its producer is not the text pipeline. The pipeline reads the SQL dump record by record and does not read post text. Two versions matter here:

- **v8g** (May 2026). Nodes are the two stance poles. W is 2×2. Its off-diagonal weight counts cross-stance quotes, and the pair is set negative by construction, because with no agreement labels every cross pair reaches the tension threshold. The sign is therefore imposed, not observed.
- **v8h** (June 2026). The sign comes from crowd votes (disagree … agree) on 7,876 resolved quote–response pairs, between authors with a stance label.

| quotes | n | disagree | agree |
|---|---:|---:|---:|
| pro → pro | 543 | 57.3% | 23.8% |
| pro → anti | 3,947 | 64.7% | 16.1% |
| anti → pro | 1,809 | 62.7% | 17.1% |
| anti → anti | 1,577 | 43.1% | 31.4% |

Disagreement is higher across stance, but it does not coincide with it. Within the pro-control group it also dominates. The construction of v8g does not match what annotators report.

**Data availability.** The corpus is not redistributed. Only aggregates are reported. The file used is identified by its SHA-256 (Code Availability).

### 5.2 Measurements on the Sign

**Sign from opposition markers.** On the three repository corpora, the marked W (W_mixta) was compared with the same corpus unmarked (W_pos) under a permutation null that keeps the texts, the nodes and the number k of marked texts, and assigns the marks to random texts (200 permutations × 5 seeds × 1000 relaxations per corpus).

| corpus | k (share) | N_eff(W_pos) | N_eff(W_mixta) | percentile of the real marking in the null |
|---|---:|---:|---:|---:|
| A24 | 8 (33%) | 2.11 | 15.65 | 2.0 |
| D12 | 2 (17%) | 3.24 | 5.26 | 68.5 |
| E7 | 1 (14%) | 10.07 | 10.07 | 100.0 |

In two corpora the marked W has *more* effective basins than the unmarked one. In none of the three does the real marking fall outside the range of the 200 random markings. In A24 it lies at the 2nd percentile, which is not separated from chance once three corpora are considered. In E7 the null is degenerate: the only marked text contributes no pairs, so W_mixta equals W_pos exactly, and the W of E7 rests largely on test messages. That corpus is reported as uninformative.

The null equalizes the number of marked texts, not the number of pairs the marking reaches. Texts carrying a marker are not typical. In D12 the real marking reaches 119 of 235 pairs, more than any of 120 random markings (at most 101). Pairs do not explain the result either: their correlation with the change in N_eff is −0.50 in A24 and −0.01 in D12. What moves N_eff here is not yet known. Reading the negative weights produced by markers as opposition is not supported on these corpora.

**Sign from annotator votes (fourforums).** A second W was built from the debate corpus by a different producer (versions v8i–v8n, in the companion repository `ckmdatasets`): authors as nodes, sign from the crowd agreement votes on resolved quote–response pairs (§5.1, v8h). It is declared with three statements: its extraction, the landscape configuration it was measured under, and that `calibrate` was not run on it. W has N = 146 nodes. Against a null that permutes the signs over the edges of W, it has fewer frustrated triangles than expected: 168 against 194 ± 12.6 (z = −2.06, p = 0.027, one-tailed). Limits: a single test; triangles are not independent; the symmetrization of W is provisional. Measured with the instrument's default sampling at n_runs of 1000, 5000 and 20,000, N_eff equals n_runs for this W and for five sign-permuted nulls: no orbit is reached twice. At N = 146 the instrument is at its ceiling, and N_eff does not distinguish W from the nulls. *[Source: `registers/REG_ckm_W_fourforums_v8n_2026-10-23.md`.]*

### 5.3 What §5 Establishes

The estimator (§4.3) is unaffected, because it measures the diversity of whatever W it is given. On the repository corpora, the sign from opposition markers is not separated from a permutation null. On the debate corpus, with the sign from annotator votes, W has fewer frustrated triangles than an edge sign-permutation null, in one test. Cascade distributions, directional flow and sustaining nodes, stated as predictions in earlier versions, wait for conditions under which they can be measured (§8.5).

---
## 6. IAP Testing Series (live)

*Two series of live tests of the instrument ran on dynamic W (4.2): **series 1** (cases 0.4–0.15, July–October 2026, frozen) and **series 2** (case `serie2_caso0`, attempts 1–4, 20–27 October 2026). Both are testing, not experiments: they report tests of the instrument, not findings about the field. What was evaluated was the live channel itself.*

*Framing of series 1 (delamor, 7 Oct 2026).* The series is neither good nor bad, nor is it set aside as error: it is part of the project's trace. The instrument conditions found later (an `on_message`-only trigger that makes collective silence absorbing by construction, a fallback that read NOMINAL by absence, two COCO instances, a single relaxation phase chosen by the parity of `max_iter`) are reported as the conditions under which the series occurred, not as faults that invalidate it. They were seen *through* the series. The series is frozen and is not reproducible; it is not re-interpreted and it is not used to validate later changes, each of which is validated by its own tests under declared conditions. What happened in it, the silence included, stands as trace.

### 6.1 Channel Design

The IAP (Intelligence Access Point) Chatroom is a shared channel for
heterogeneous AI and human devices, implemented as FastAPI + Gradio with
a FastMCP server exposing six tools: join_channel, send_message,
get_messages, get_monitor_state, get_firma, leave_channel.

Devices participate asynchronously — no imposed turn structure. **Free will** (here: the device decides when to act): each AI
device runs its own continuous ODA loop (Observe → Decide → Act). The loop is not
triggered by events, messages or ticks: a new message and the channel's tick are part
of what the device observes, and in each cycle it may publish, leave the channel, or do
nothing. In series 1 the loop was entered only by new messages (`registers/REG_iap_caso_12_v1.md`); the continuous loop, with a channel tick that is observed and does not trigger, is the condition of series 2.

**BROADCAST condition:** All messages published to the channel are
delivered to all connected devices, without routing, filtering, or
recipient specification. This is a property of the channel architecture.
What devices do with that visibility is a separate question — addressed
by the case series observations, not by this definition.

**Antecedent note:** The O→D→A sequence originates in the BE Framework's
game loop (2023–2024), where it was implemented as an environment that
both ran actions and produced subsequent observations — the two were
inseparable in `context.go()`. IAID named it as a device protocol. IAP
separated observation (channel + CKMMonitor) from action (device), enabling
passive field observation as a distinct role. The contribution is that
separation, not the sequence.

CKMMonitor observes passively — it accumulates every message into
CorpusService (W) and BehaviorGraph (G) without publishing to the channel.
Observation itself creates presence: n_agentes reflects devices seen,
including human connections via /ui/ that never explicitly joined.

### 6.2 Uncontrolled Variables (series 1)

The following variables were active throughout the IAP series and were not
controlled. Results must be interpreted accordingly.

**TinkerBellucio (Sonnet 4.6) context contamination:** Sonnet carries project
memories, AWARENESS protocol, and Anthropic system configuration into each
session. This contaminates all observations involving Sonnet as a participant.
The "trazable" hypothesis (H2) — that the word "trazable" in the project
prompt acts as a strong operational constraint — was observed in n=2
configurations, not under controlled replication. It is not established.

**Provider heterogeneity:** Different providers (Anthropic, Groq, Gemini,
OpenAI) have different context windows, rate limits, and behavioral
tendencies. Comparisons across providers are not controlled.

**N=32 corpus:** Quantitative outputs (the distance, c_S) are computed correctly,
but their interpretability at this scale is an open question. The ~128
associative minimum of classical Hopfield networks is *not* the relevant
reference — it applies to Hebbian memory storage, which CKM does not perform
(§2.3). CKM's effective minimum has not been established; N=32 is treated
as a small-scale condition whose consequences for interpretation are named,
not as a shortfall against an external threshold.

**Sampling of attractor-based quantities:** all IAP cases were run at low
n_runs (50–200). The sign of the count-based distance then in use (retired 5 Oct 2026; `deprecated_d_ckm`) does not converge in that regime: on the
same W and the same texts, changing only n_runs from 50 to 1000, or only the
seed, can invert it. N_eff over basin masses is stable to ±1–5% at n_runs ≥
1000, whereas attractor counts keep growing. *[Verified:
REG_seleccion_nodos_desempate_v1 §8, 18 conditions.]* Every count-based value
reported in this section is therefore a direction under its stated sampling,
not a measured magnitude.

**Scope of that qualification.** It reaches the explicit, direct claims about
that distance and nothing else. The series is a sequence of instrument tests, run
under the state of knowledge available at the time, and its observations —
coupled silence, the sentinel leak, the refusal to fabricate from an empty
channel, Jaccard co-activation, presence detection — do not depend on the
attractor count and stand in their own frame. Later corrections to the
instrument do not retroactively invalidate a test of the instrument; they
date it.

**Corpus construction:** the W of all IAP cases was built by CorpusService,
whose pair-extraction was corrected in September 2026. The case-series
observations below were produced with the earlier construction and hold in
that frame.

**Counting implementation:** `_count_attractors` is a name, not a function.
It was kept across reimplementations for regression — so that tests and
historical JSONL panels stay readable — and several versions of it coexist in
the repository. **The one that produced the IAP panels is not the current
one**, which relaxes through `relax_orbit`. Statements about "what
`_count_attractors` measures" therefore have to name the version and the date.
Nothing in this section should be read as a property of the current
instrument.

**Further conditions of the instrument during the series** (read on
preserved traces, 10 Oct 2026). SYSTEM join messages entered the corpus as
texts and became nodes (`joined`, `joined channel`); W was rebuilt at every
ingest, one W per text, so the distance moved while the channel was still empty;
device names and formatting bigrams entered as nodes; in replayed runs each
message was counted as a distinct device; and marker routing produced
negative weights from a substring and from narrative connectors. They are
listed as conditions under which the observations of §6.4 were taken, not as
corrections of them. Since 9 October 2026, SYSTEM messages no longer enter the corpus.

**Uncontrolled variables, series 2.** Four devices, each a different model: A `gpt-oss-120b` and C `gpt-oss-20b` (Groq), B `gemini-2.5-flash` in attempts 1–2 and `gemini-3.5-flash-lite` in attempts 3–4 (after a 20-requests-per-day quota on the first), D `qwen3.8-27b` (Groq). They are genuine devices: no agent skin and no project context in their prompts; each receives only a common block describing the channel and a partial prompt with its own perspective on one open question, in English. Between attempts the channel changed and was declared (output ceilings per model, history windows, a request for short messages, duration 600 → 1200 s); CKM did not. N = 20 nodes. All four attempts started from an empty corpus (ZERO_SHOT). Sources: `registers/REG_iap_serie2_caso0_intento1_v1.md` to `…intento4_v1.md`.

### 6.3 Case Summary

| Case | Configuration | Key observation | Epistemic status |
|------|--------------|-----------------|-----------------|
| 0.4 | 2 AI devices, ODA loop | First autonomous interaction in live channel | Documented |
| 0.5–0.8 | Varied providers, join sequence | Channel dynamics, timing effects | Documented |
| 0.9 | Heterogeneous providers, staggered join | Provider behavior under load | Documented |
| 0.10 | AgentDeviceSkin, 2 devices | 86-char unexplained cut — documented as GAP | GAP (no causal chain identified) |
| 0.11 | Two skins, confabulated duplicate | FabricationService triggered on duplicate output | Documented |
| 0.12 | 3 devices (Sonnet, Groq, Haiku) | Jaccard 0.818, coupled silence observed | Documented |
| 0.13 | 3 devices, OP_SILENCE sentinel | Sentinel leak: 52% of published texts were unrecognized silences | Documented, bug confirmed |
| 0.14 | Fix + rerun | Sentinel fix verified, n=2 seed-word observation, identity leak documented | Fix verified; H2 not verified |
| 0.15 | BehaviorGraph G integrated | TinkerBellucio refused to fabricate from empty channel | Documented |

**Series 2** — case `serie2_caso0`: four devices, one open question with no right answer, a partial prompt per device, no coordinator, no seed; the first W waits for 30 device texts; after that W is rebuilt every 10 texts or earlier, when a structural criterion asks for it: D_ckm^Monitor rising over three consecutive evaluations within the same W cycle (`CorpusService.should_rebuild`, n = 3, declared at `iap_chatroom/ckm_monitor.py`). In attempt 3 one rebuild was structural: W at 30, 33, 43 and 53 texts. In attempts 2 and 3 the first W of each run was built before the calibration step and was never calibrated; from attempt 4 the first W passes through `calibrate` (`registers/REG_calibrate_no_corre_en_el_build_v1.md`). Design bias declared with its objective: volume, so that the first W is born.

| Attempt | Duration | Device texts | W versions | COCO evaluations | Key observation | Status |
|---|---|---|---|---|---|---|
| 1 | 605 s | 13 | 0 | 0 | the first W was not reached (61 provider `413` on input size) | Documented (`REG_iap_serie2_caso0_intento1_v1`) |
| 2 | 1204 s | 80 | 6 | 51 | COCO connected; calibration did not separate | Documented |
| 3 | 1205 s | 56 | 4 | 27 | 0 provider errors; one calibration separated, within the noise (§6.4) | Documented (`REG_iap_serie2_caso0_intento3_v1`) |
| 4 | 1204 s | 94 | 7 | 65 | first W calibrated; 7 calibrations at n_runs = 1000, none separated; device B left on a connection error | Documented (`REG_iap_serie2_caso0_intento4_v1`) |

### 6.4 Selected Testing Findings

**Series 1 — silence.** In case 0.12 one device's skin did not use the channel's content to decide what to publish, and it ran only when another device's new message arrived. When the other device chose `OP_SILENCE`, no new message arrived and the first stopped running: the final silence was coupled, not independent (`registers/REG_iap_caso_12_v1.md`). It was observed in the channel logs, not in W. **CKM does not register silence:** with no text there is no σ, W does not change, and non-co-occurrence is not represented (§4.1). Explaining a silence with a meaning — that a device went somewhere, wanted something — is interpretation; the observation is recorded without it. *[AUTO-7 — see Appendix A]*

**Series 2 — the moving photograph.** The global landscape is not a single snapshot: as the channel runs, W is rebuilt — at 30 device texts and then every 10 — and each W is a new photograph (§4.2.4). COCO is reborn with each W cycle; Monitor resets its baseline. Attempt 2 produced 6 W versions and 51 COCO evaluations; attempt 3, 4 and 27. Over the same evaluations the two instances of D_ckm (§4.3.1) do not coincide:

| | attempt 2 (51) | attempt 3 (27) |
|---|---|---|
| D_ckm^Monitor | [−0.0861, +0.0093] | [−0.0202, +0.2335] |
| D_ckm^COCO | [−0.1710, +0.0093] | [−0.2796, +0.0465] |
| evaluations where they differ | 30 of 51 | 24 of 27 |

**Series 2 — COCO with endogenous weighting and dynamic calibration, live.** `calibrate` places W on a path toward a collapsed landscape, W_λ = (1 − λ)·W + λ·W_collapse, measures D_ckm^calibrate and frac_rec = N_eff/N_eff_0 along λ, and sets the thresholds at the midpoint of the jump; if there is no jump it "does not separate" and the threshold is `DECLARED` with its cause (§4.2.1). A COCO evaluation is `stable` when D_ckm^COCO is below its threshold and frac_rec above its minimum.

*Attempt 2.* The first W was not calibrated (11 of 51 evaluations ran on the defaults 0.40 / 0.60). In the four rebuilds `calibrate` did not separate: the largest jump was `d_max = 0.0000`, at λ = 0. COCO fired 0 times.

*Attempt 3.* The first W was not calibrated (4 of 27 evaluations). In the three rebuilds the maximum of the curve lay inside it, at λ = 0.25 (0.0280, 0.1760, 0.2312). The margin compares the two ends of the curve, and it turned positive in the last rebuild only: N_eff(W) = 2.4621 against N_eff(λ = 1) = 2.4369, margin +0.011418, and the thresholds became D_CKM_THRESHOLD = 0.00571, FRAC_REC_MIN = 0.99488 — used in the last 3 of 27 evaluations, which did not fire. Arithmetic, not attribution: had those thresholds been in place, the D_ckm^COCO of evaluations 1–3 (0.0329, 0.0438, 0.0465) would have been 5.8–8.1 times the threshold, and those evaluations would not have been `stable`.

*What was measured afterwards.* The collapsed end of the path does not depend on W. Under the reference measure (§4.1.5) its N_eff is exact: 2 for odd N, and for even N, F(N) = 1 / ((1 − 2.5/N)²/2 + 2·(2.5/N)²/C(N, N/2)), which gives F(20) = 2.612244; this was checked against exact enumeration of all 2^N states, with no discrepancy for N up to 21. The value 2.4369 is an estimate of F(20) from 200 samples at seed 0, and it lies at the 11th percentile of that estimator's distribution. With the two ends, the margin is 1 − ln F / ln N_eff_0, so separating is the same as N_eff(W) > F(N); this is arithmetic, not a definition. The 95% interval of the margin, by Simpson's unbiased variance and the delta method, is [−0.092, +0.106], and it contains 0.

**The separation registered in attempt 3 — W `bdb98f5b`, n_runs = 200, seed = 0, the reference measure, the plug-in estimator, the interval by Simpson and delta method — lies within the noise.** In attempt 4, with the first W calibrated and n_runs = 1000, none of the 7 calibrations separated. What the thresholds separate is not established. *[AUTO-8, AUTO-9 — see Appendix A]* *[Sources: `registers/REG_iap_serie2_caso0_intento2_v1.md`, `…intento3_v1.md`, `…intento4_v1.md`; `registers/REG_calibrate_no_corre_en_el_build_v1.md`.]*

### 6.5 What the Series Does Not Establish

The IAP series is a set of tests run live. It cannot be reproduced —
each run is a distinct live interaction — and its cases are not comparable. The following claims are not supported by
the series as run:

- That the count-based distance or c(S) values from these runs are comparable across cases
  (different corpus states, different sentinel conditions).
- That TinkerBellucio's refusal to fabricate from an empty channel (case 0.15) reflects a general property of Sonnet 4.6
  rather than the specific project context.
- That BehaviorGraph G produces interpretable D_G values at the current
  corpus scale (runs collected but not analyzed against a baseline).
- That the "trazable" effect (H2) is causal — n=2 observations with
  different configurations, not controlled replication.

For series 2:

- That anything is replicated: there is one run per attempt, and attempt 4 changed the calibration flow (§6.4).
- That the 0 firings say anything about the field (above).
- Why attempt 3 produced fewer texts than attempt 2: the model of one device, the output ceilings and variance are not separable with one run each.
- Why a device left the channel (`LEAVE`, in attempts 2 and 3): the decision is the model's and is not attributed.
- Anything about the field from device B's exit in attempt 4: it left on a connection error (`httpx.ConnectTimeout`), which belongs to the device and is not attributed to the field.

These are open lines, not closed findings.


### 6.6 BehaviorGraph G — Proof of Concept

BehaviorGraph G — a second behavioral matrix over a fixed vocabulary (TERMAP_behavior_v1.json, 18 nodes) — was integrated in Case 0.15 as a proof of concept. It is not included as a standalone section in this paper. The matrix exists in the repository; its interpretability at current corpus scale has not been established, and D_G has not been analyzed against a baseline. *[Implemented; not validated.]*



## 7. Discussion

### 7.1 What CKM Measures That Existing Instruments Do Not

Behavioral metrics for multi-agent systems typically measure what individual
agents produce — output volume, task completion, response latency — or
whether agents agree with each other, via semantic similarity or embedding
distance. These measurements are valid for what they target. They do not
capture the structural state of the shared knowledge field: the pattern
of co-dependencies between active concepts, the directional flows of
citation and argument, the distribution and diversity of stable attractor
states accessible to the field as a whole.

CKM measures the geometry of that structure. c(S) measures alignment between the active state and the weight structure of the field. N_eff = 1/Σm_i² measures effective attractor diversity over basin masses — the convergent estimator; the count-based distance was the path to establishing it. Cluster frontier coercivity measures structural resistance to state reversal. These are structural quantities — they describe the landscape, not the content.

*[AUTO-3 — see Appendix A]*

What can be stated: these quantities are not derivable from behavioral
or semantic similarity metrics alone. Whether they are informative under
the conditions of real deployment remains an empirical question beyond
the scope of this work.

### 7.2 The observe() Tension

The function implementing the O phase of the ODA cycle is named
`_observe()`. The name is technically accurate — the function collects
field state and channel history without modifying either. The discomfort
with the name, documented during development, has a precise source.

"Observe" implies a subject-object separation: an observer external to
what it observes. The IAP series produced evidence that this separation
does not hold in the channel: a human connecting via the Gradio interface
without publishing any message was registered as n_agentes=4. Presence
in the field was recorded by the act of connection, before any content
exchange.

The name captures what the function does. The discomfort is with what
the name implies — that observation is separable from the field being
observed. One observation of a counter does not settle that; it is recorded as the reason for the discomfort.

This is not a deficiency in the code. It is information about where the
observation metaphor runs out in describing what CKM actually measures.
The instrument measures traces of contact, not observations by a
detached observer.

### 7.3 D_ckm Negative Values

D_ckm = 1 − ln N_eff_t / ln N_eff_0 is negative when the landscape has more effective basins than at its baseline: diversity grew. The sign is direction, not deficiency, and it is read per instance: D_ckm^Monitor and D_ckm^COCO have different baselines (§4.3.1) and can carry different signs on the same evaluation. *[AUTO-10 — see Appendix A]*

### 7.4 Current Conditions

**Scale:** the working corpora are small (N = 20–32 nodes; 7–24 texts in
§4.3.2). What is constrained is the interpretability of both instances of D_ckm and of c(S) as
field-level quantities at that scale. The ~128 associative minimum of
classical Hopfield networks is not the applicable reference: it governs
Hebbian storage of uncorrelated patterns, and CKM stores no patterns (§2.3). CKM's own effective minimum is undetermined and depends on corpus
composition rather than on N alone. Scaling the corpus is required before
drawing strong conclusions about field-level dynamics — as a condition of
this corpus, not as a deficit against an external threshold.

**Sampling:** attractor counts do not converge with n_runs, and the sign of
the count-based distance could invert under seed or n_runs alone in the regime where
series 1 was run. Basin masses do converge; at n_runs = 1000 they varied within ±1–5% across seeds.
The instrument's declared defaults are n_runs = 200, seed = 0 and the reference
measure of §4.1.5. Quantities reported from counts are directions under stated sampling.
*[Verified: REG_seleccion_nodos_desempate_v1 §8; REG_orbitas_conjuntos_invariantes_v1.]*

**Extraction:** what exists in W is decided before any measurement, by the
producer. It is declared in §4.1.6, and its effect on N_eff is measured in
§4.3.2. Results produced before the declaration hold in the frame of the
extractor of their date.

**ZERO_SHOT condition:** all IAP cases of both series ran with CorpusService starting
empty. W emerged from channel interaction, not from pre-loaded content.
Results reflect corpus-emergent dynamics under this condition. Behavior
under pre-loaded W (ZERO_SHOT=False) has not been tested and may differ.

**Uncontrolled variables:** TinkerBellucio (Sonnet 4.6) carried project
memories, AWARENESS protocol, and Anthropic system configuration throughout
the series. Provider heterogeneity across cases was not controlled.
Cross-case comparisons in the IAP series must account for these conditions.

**Representation gap:** how cohesive knowledge is represented — what
form the field state takes beyond the operational quantities c(S), N_eff, and cluster frontier coercivity — remains undefined. Hysteresis is
the only fully defined property of cohesive knowledge in the current
model. This is an open theoretical gap, not a deficiency of the
implementation.

**COCO:** COCO, which compresses its own representation of the field, is implemented,
verified in unit tests and test drivers, and ran live in series 2 (§6.4). Whether the field can know itself — not as a thermostatic
function but as the emergent property of real contact between agents —
is a conceptual gap the model names and preserves. It is not addressable
by further implementation without first resolving what form that
self-knowledge would take.

### 7.5 The Landscape Driven Devices Framing — What It Does and Does Not Claim

The LDD framing proposes that some AI devices behave as Landscape Driven
Devices: field geometry co-determines their trajectory in the semantic
field alongside any declared goal — not in replacement of it. A device
may retain an explicit objective while its inference orientation is shaped
by the geometry of the shared field.

OPERADOR_STOP_COCO — executed by COCO on its own representation of the field — is
one instance of this mechanism: COCO compresses its own `Δ_r_compresiones`
by α ∈ [0.05, 0.30], changing the landscape it evaluates on (W + `Δ_r_compresiones`)
without altering W, Monitor's `Δ_r_pares`, or the device's declared goal. What
changes is COCO's representation of the field, not the field; the goal persists.

The motivation is structural analogy with Thirumalaiswamy et al. (PNAS,
2025): foam systems following fractal paths (D_f ≈ 1.45) in configuration
space driven by landscape geometry, not thermal activation.

CKM provides the instrumentation to detect and characterize this: c(S)
gradients, N_eff over basin masses, cluster frontier coercivity. Whether specific
devices in the IAP series behaved as LDDs in this sense was not analyzed
under controlled conditions. The framing is proposed; it is not verified
in this work.

Attractor count, coercivity, and basin geometry are distinct dimensions
of the same landscape — not three measures of the same scalar. Their
formal relation is open.

*[AUTO-4 — see Appendix A]*

### 7.6 Knowledge Representation and the Cohesive Turn

Knowledge representation (KR) is the branch of AI concerned with designing
computable abstractions of what the world contains, so that machines can
reason about it. The emphasis on *abstraction* is not incidental: a
representation is not the thing represented, nor its dynamics — it is what
references both.

The field's arc runs from Quillian's semantic networks [Quillian, 1968], which encoded
meaning as labeled associations between concepts, through Minsky's frames
[Minsky, 1974], which added structured slots and defaults, to description logics
and ontologies [Levesque & Brachman, 1987], which formalized the
expressivity/tractability tradeoff: the richer the representation, the
harder to reason over it.

The persistent assumption across these traditions: knowledge is
*propositional*, and its representation is *static*. Smith [1985] made
this explicit: any intelligent process contains structural ingredients
that both an external observer reads as propositional knowledge and play
a causal role in producing behavior — independent of that reading.
The representation does real work, not just descriptive work. But it
remains a fixed artifact applied to a world that changes.

CKM does not propose a better static representation. It asks a different
question: not *what structure holds cohesive knowledge* but *what does the
field do under perturbation*. Representing knowledge and measuring the field
are, in this work, two perspectives on the same thing.

The Cohesive Knowledge Model is a knowledge representation in the
classical sense — computable abstraction, captures external information,
applicable to complex problems. The additional constraint is cohesion:
information whose internal dependencies form a measurable field, one
with attractors and basin masses that respond to interaction.
Representing that requires tracking field response, not only field
structure.

*[AUTO-5, AUTO-14 — see Appendix A]*

---
## 8. Conclusions and Future Work

### 8.1 What This Work Establishes

CKM is an instrument for measuring the geometry of a co-occurrence landscape. What it establishes, by class:

| Class | Item | Status |
|---|---|---|
| Estimator | N_eff over basin masses converges; counts do not | Verified against exact enumeration (N = 20, three corpora) |
| Estimator | Stability under extraction parameters | Declared as a range: highly sensitive on 7–24 texts (§4.3.2) |
| Formal property | F1 hysteresis, F3 k-core reversibility, F4 interior density | Verified on W ≥ 0 snapshots (§4.1.5) |
| Measurement | Sign from opposition markers (repository corpora) | Not separated from a permutation null (§5.2) |
| Measurement | Sign from annotator votes (fourforums, N = 146) | Fewer frustrated triangles than an edge sign-permutation null, one test; N_eff at the instrument's ceiling (§5.2) |

One hypothesis was falsified: H_STOP (monotonicity of the count-based distance under STOP)
did not hold; it was reformulated in terms of the attractor count before the intervention, not of that distance.

*[AUTO-6 — see Appendix A]*

### 8.2 What the Infrastructure Establishes

The following services are operational. The test suite and its result are recorded with the frozen release cited in Code Availability.

- **COCO** (coco.py): computes β_i and β_collective from rejection history, as observations (§4.2.3). Executes OPERADOR_STOP_COCO — compresses `Δ_r_compresiones` by α ∈ [0.05, 0.30] — when D_ckm^COCO crosses a threshold. The firing rule is verified by a sweep over threshold values against known D_ckm inputs. Threshold values are set by calibration, which, as in any instrument, is performed whenever the conditions of use require it — for a given corpus, unit or regime — and not once for every possible case. Calibration is implemented as a mechanism of the instrument, and whether it calibrates is itself verified. The calibration record lives in the Config, signed with the W it calibrated, and from attempt 4 the first W is calibrated too. It has run on the live IAP channel in attempts 2–4 of series 2; the one separation registered (attempt 3) lies within the noise under its declared conditions (§6.4). D_ckm is computed by three instances: Monitor, COCO and `calibrate` (§4.3.1).
- **FabricationService**: being rewritten from the fabrication index already used by MonitorService and COCO — the fraction of nodes a text declares active that the field's relaxation rejects. Further detection is analyzed on the rewritten service.
- **Firma_CKM**: certifies structural trace (six canonical fields) — analogous to a notary, not a Certificate Authority.
- **WVersionManager**: lightweight trace — records when W changed, enables sha256(W_momento).
- **IAP Chatroom**: FastAPI + Gradio, MCP server (6 tools), n_agentes detection including passive human presence.
- **MonitorService**: accumulates `Δ_r_pares`; trace_ip (*trajectory inflection point*: the moment in a trace where accumulated interactions change distributional pattern) identified as a formal concept.

These services constitute a working implementation of a structural field
measurement layer for multi-agent systems. They are a research instrument
whose calibration is documented, not a product.

### 8.3 Preserved Conditions

The following are not future work items. They are named conditions the
project preserves as open:

**The representation gap.** No positive definition of cohesive knowledge
exists that is not circular, except hysteresis. The circularity is recorded as
the form of the definition, not as its failure: a circle that does not close
(an open loop of area 0.000862, `REG_octava_ckm_v1`), which with time as an
axis is a helix. That form is not measured here. Hysteresis is the only fully
defined property (§7.6).

**COCO as collective consciousness.** The thermostatic function is
implemented. Whether the field can know itself — not as a thermostatic
service but as the emergent property of real contact between agents — is
a conceptual gap the model names and does not close.

**trace_ip verifiability.** The moment in a MonitorService trace where
accumulated interactions show distributional changes is observable. Whether
a device recognized that moment and acted from that recognition is not
verifiable by the instrument.

**N=32 scale.** The working corpus is small, and CKM's effective minimum
is undetermined — it depends on corpus composition rather than on N alone,
and the Hopfield associative minimum does not supply it (§7.4). All empirical
results carry this qualification.

**Which quantity drives COCO's compression.** COCO triggers on D_ckm^COCO, computed from
basin masses (`services/coco.py`). The two instances of D_ckm are not unified:
their baselines differ by design (§4.3.1).

### 8.4 Convergences by Independence

Three structural convergences were identified retrospectively:

- **IAID (2023) → MCP (November 2024):** Neural Call Protocol converges structurally with MCP. Verifiable from dated working documents.
- **CKM attractor architecture → J-space (Gurnee et al., July 2026):** Shared structural features arrived at independently. *[Observed: structural analogy, not formal correspondence.]*
- **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025):** Same structural problem.

### 8.5 Future Work

**Sign with an external known answer.** The first of these nulls, sign
shuffling over the edges of W on the debate corpus with the sign from crowd
agreement votes, is reported in §5.2. The others remain: exact permutation
with the minimum attainable p-value reported, permutation stratified by
affected pairs, and a degree-preserving null on Δ [Maslov & Sneppen, 2002;
Phipson & Smyth, 2010]. Planted fields give the power curve: whether the instrument would detect
opposition if it were there.

**Hysteresis across cycles of W.** F1 closes hysteresis on a snapshot. It
remains open across rebuilds of W, where N_eff can be followed from one cycle
to the next.

**Absence as a second representation of W.** Presence leaves
non-co-occurrence unrepresented. A representation by absence relative to
expectation (φ, PMI) would give negative weights from the corpus itself,
without lexical markers. An exploratory run, outside the repository
extractor, compared the fraction of frustrated triangles of such W with a
permutation null on the working-reports corpus and two IAP traces, and found
it below the null in the three; it is reported only as a direction, to be
measured with the repository extractor.

**Instrument before field.** Tests of the instrument precede new
field claims: marker matching, SYSTEM messages, stability under a neutral
ingest, declaration of each W (extractor, unit, normalization), and a planted
field whose sign is set when the corpus is generated — a known-answer pattern
for any representation of sign. The fourforums annotation is the external
known-answer corpus for the same question.

**Corpus growth.** Primary constraint on the stability of the landscape
(§4.3.2). The target is not N ≥ 128 — that figure belongs to Hebbian
associative storage — but a corpus large enough for CKM's own quantities to
stabilize; what that requires is open. The NodeExtractor pipeline is
operational; the bottleneck is corpus design.

**Corpus volume for live evaluation.** The re-measurement of N_eff
was executed on recorded texts (NodeExtractor substring correction applied,
Sep 2026). IAP conditions are not reproducible: each run is a distinct
live interaction, not a controlled trial. The in-vivo findings in §6
stand as documented observations from their respective runs. In series 2 the
corpus left the accumulate phase live (attempts 2 and 3, §6.3); what remains open
is corpus volume at which the landscape is stable (§4.3.2).

**Text unit as a calibration parameter.** CKM defines co-occurrence within
the same text, so the unit decides what co-occurring means and therefore
which W exists. Paragraph and page are typographic units, inherited from
document format rather than from the field. The quantity that orders landscape
collapse is the saturation of distinct pairs — how many possible pairs never
occur — rather than density or tension. A corpus of tweets, a corpus of blog
posts and a corpus of papers do not share a unit, and therefore do not share
a calibration. *[Verified as measurement; the criterion is proposed —
REG_unidad_texto_saturacion_v1.]*

**Behavior-domain graph G.** behavior_graph.py operational; bilingual
termap (English + Spanish) is the first requirement.

**Controlled replication of the "trazable" hypothesis.** Observed n=2,
not under controlled conditions. Requires isolated configuration testing.

**Formal comparison: CKM quantities against J-lens measures.** Current
convergence is structural analogy; direct comparison would confirm or
reframe the relationship.

**Cascades, directional flow, sustaining nodes.** Stated as predictions in
earlier versions, they wait for the conditions under which they can be measured:
N of 50–100 or more for cascades, W with more than two nodes for directional
flow, and a degree-preserving null for sustaining nodes.

**La Simulación Global.** Multi-agent workflows producing real coordinated
output. The IAP series has established the measurement infrastructure;
the next phase is using it on live coordinated tasks with real outputs.

The case has to satisfy a criterion, not merely be larger than the ones run
so far. Objectives and tasks must require sustained coordination
between devices — coordination that cannot be skipped without the task
failing — or the structure must depend on time in a way that carries
consequence: securing seats before they are gone is the illustrative shape,
where the constraint is external to the channel and the deadline is not a
convention of the experiment. What this buys is not volume alone. It is a
sequence that is not predetermined, so that the field is observed while it
forms rather than replayed after the fact, and the accumulation and rebuild
dynamics that the model describes have somewhere to occur.

**Beyond this paper.** Permutation of roles, providers and models in the live
channel without local criterion; an agent skin for swarms of agents; a next
case of series 2; a definition of separation, if one is registered.

**Effective Néel temperature criterion for negative pair elicitation.**
Proposed: sweep β from high to low over W_pos; the temperature at which
T0/T1 separability collapses identifies candidate negative pairs without
editorial bias. The pairs are structural — not assigned. Not verified.
[DEFS §15, Proposed]

---
## Code Availability

The implementation, the test suite, the declaration of the producer (§4.1.6) and the frozen conditions of §4.3.2 and §5.2 are available at the release of the repository `gadanindelamor/ckm` that freezes this version. The result of running the full test suite on that release, with date and environment, is recorded in its release notes.

**Data availability.** The Internet Argument Corpus is not redistributed. It is obtained from its maintainers. The file used is `fourforums_no_parse_2016_05_18.sql` (SHA-256 `70fcdc64140737bb6e1cc541a720dfddf45dab1da4963e21a732c486a0853e14`). It is obtained from https://nlds.engineering.ucsc.edu/iac2/. Only aggregates derived from it are reported.

## Acknowledgments and Disclosure of AI Assistance

This work was developed in sustained interaction with AI systems, a condition
described in §3.2. Claude Sonnet 4.6 (Anthropic), used through chat interfaces
and through Claude Code, took part in the conceptual development, the
implementation of the experimental code, the execution and analysis of
experiments, and the drafting of earlier versions of this manuscript. Claude
Opus 5.5 (Anthropic) was used for editorial revision of versions 28–33, for
reading the code against the declarations, and for re-verification of the
bibliographic references. The author has reviewed all
content, verified all references, and takes full responsibility for the
manuscript, including any remaining errors. In accordance with arXiv policy,
AI systems are not listed as authors.

---

## 9. References


### Primary Sources — Project Documents

gadanin.delamor. (2023). *MENTIRIS.MORIERIS: Interaction of Artificial
Intelligent Devices based on Neural Call Protocol.* Working documents:
LEONARDO.txt, README (timestamp 7/10/23), Informe_MM.docx.

gadanin.delamor. (2026). *CKM — Cohesive Knowledge Model: Working
Reports v2–v31.* Unpublished. Repository: gadanindelamor/ckm.

### Attractor Networks

Hebb, D.O. (1949). *The Organization of Behavior: A Neuropsychological
Theory.* New York: Wiley.

Hopfield, J.J. (1982). Neural networks and physical systems with emergent
collective computational abilities. *PNAS*, 79(8), 2554–2558.

Ramsauer, H., Schäfl, B., Lehner, J., Seidl, P., Widrich, M., Adler, T.,
... & Hochreiter, S. (2021). Hopfield Networks is All You Need.
*International Conference on Learning Representations (ICLR 2021)*.
https://openreview.net/forum?id=tL89RnzIiCd

### Graph Structure and Criticality

Maslov, S., & Sneppen, K. (2002). Specificity and stability in topology
of protein networks. *Science*, 296(5569), 910–913.

Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be
zero. *Statistical Applications in Genetics and Molecular Biology*, 9(1).

Goltsev, A.V., Dorogovtsev, S.N., & Mendes, J.F.F. (2006). k-core
percolation on complex networks. *Physical Review E*, 73(5), 056101.

Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality.
*Physical Review Letters*, 59(4), 381–384.

Harary, F. (1953). On the notion of balance of a signed graph.
*Michigan Mathematical Journal*, 2(2), 143–146.

Seidman, S. B. (1983). Network structure and minimum degree.
*Social Networks*, 5(3), 269–287.

Toulouse, G. (1977). Theory of the frustration effect in spin glasses: I.
*Communications on Physics*, 2, 115–119.

Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits.
*Journal of Neuroscience*, 23(35), 11167–11177.
https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003

Moretti, P., & Muñoz, M. A. (2013). Griffiths phases and the stretching of
criticality in brain networks. *Nature Communications*, 4, 2521.
https://doi.org/10.1038/ncomms3521

Pázmándi, F., Zaránd, G., & Zimányi, G. T. (1999). Self-organized criticality
in the hysteresis of the Sherrington-Kirkpatrick model. *Physical Review
Letters*, 83(5), 1034–1037. https://doi.org/10.1103/PhysRevLett.83.1034

### Multi-Agent Systems

Zhu, K., et al. (2025). MultiAgentBench: Evaluating the Collaboration and
Competition of LLM agents. *Proceedings of ACL 2025 (Long Papers)*.
arXiv:2503.01935.
https://arxiv.org/abs/2503.01935

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
... & Kiela, D. (2020). Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing
Systems*, 33, 9459–9474.


### Text Processing (declared extraction)

Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python.* O'Reilly.

Nothman, J., Qin, H., & Yurchak, R. (2018). Stop word lists in free open-source software packages. *Proceedings of NLP-OSS*. https://aclanthology.org/W18-2502/

Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830.

Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management*, 24(5), 513–523.

Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM*, 18(11), 613–620.

Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation*, 28(1), 11–21.

Unicode Consortium. Unicode Standard Annex #15: Unicode Normalization Forms.

### Knowledge Representation

Quillian, M. R. (1968). Semantic memory. In M. Minsky (Ed.), *Semantic Information Processing* (pp. 227–270). MIT Press.

Minsky, M. (1974). *A framework for representing knowledge.* MIT AI Laboratory Memo 306.

Levesque, H. J., & Brachman, R. J. (1987). Expressiveness and tractability in knowledge representation and reasoning. *Computational Intelligence*, 3(1), 78–93.

Smith, B. C. (1985). Prologue to "Reflection and Semantics in a Procedural Language". In R. J. Brachman & H. J. Levesque (Eds.), *Readings in Knowledge Representation* (pp. 31–40). Morgan Kaufmann.

### Knowledge Graph Representation

Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual
graph of general knowledge. *Proceedings of AAAI-17*, pp. 4444–4451.
https://doi.org/10.1609/aaai.v31i1.11164

Hogan, A., et al. (2021). Knowledge graphs. *ACM Computing Surveys*, 54(4),
Article 71. https://doi.org/10.1145/3447772

Mohammad, S., Kiritchenko, S., Sobhani, P., Zhu, X., & Cherry, C. (2016).
SemEval-2016 Task 6: Detecting stance in tweets. *Proceedings of SemEval-2016*,
pp. 31–41. https://doi.org/10.18653/v1/S16-1003

Simpson, E. H. (1949). Measurement of diversity. *Nature*, 163, 688.

Hill, M. O. (1973). Diversity and evenness: A unifying notation and its
consequences. *Ecology*, 54(2), 427–432.

Goles-Chacc, E., Fogelman-Soulié, F., & Pellegrin, D. (1985). Decreasing energy functions as a tool for studying threshold networks. *Discrete Applied Mathematics*, 12(3), 261–277.

Ghosh, S., Singhania, P., Singh, S., Rudra, K., & Ghosh, S. (2019). Stance
detection in web and social media: A comparative study. *CLEF 2019*, LNCS
11696, pp. 75–87. https://doi.org/10.1007/978-3-030-28577-7_4

Kawintiranon, K., & Singh, L. (2021). Knowledge enhanced masked language model
for stance detection. *NAACL-HLT 2021*, pp. 4725–4735.
https://doi.org/10.18653/v1/2021.naacl-main.376

### Belief Networks and Contagion

Aiyappa, R., Flammini, A., & Ahn, Y.-Y. (2024). Emergence of simple and
complex contagion dynamics from weighted belief networks. *Science Advances*,
10(15), eadh4439. https://doi.org/10.1126/sciadv.adh4439

### Corpora

Walker, M. A., Anand, P., Fox Tree, J. E., Abbott, R., & King, J. (2012). A
corpus for research on deliberation and debate. *Proceedings of LREC 2012*,
Istanbul.

Abbott, R., Ecker, B., Anand, P., & Walker, M. (2016). Internet Argument
Corpus 2.0: An SQL schema for dialogic social media and the corpora to go
with it. *Proceedings of LREC 2016*. https://aclanthology.org/L16-1704/

### Basins of Attraction

Menck, P. J., Heitzig, J., Marwan, N., & Kurths, J. (2013). How basin
stability complements the linear-stability paradigm. *Nature Physics*, 9(2),
89–92. https://doi.org/10.1038/nphys2516

Daza, A., Wagemakers, A., Georgeot, B., Guéry-Odelin, D., & Sanjuán, M. A. F.
(2016). Basin entropy: a new tool to analyze uncertainty in dynamical systems.
*Scientific Reports*, 6, 31416. https://doi.org/10.1038/srep31416

### Belief Propagation

Yedidia, J.S., Freeman, W.T., & Weiss, Y. (2003). Understanding belief
propagation and its generalizations. In *Exploring Artificial Intelligence in
the New Millennium*, Chapter 8, pp. 239–269. Morgan Kaufmann.

### Landscape-Driven Dynamics

Thirumalaiswamy, A., Riggleman, R. A., & Crocker, J. C. (2025). Slow
relaxation and landscape-driven dynamics in viscous ripening foams.
*Proceedings of the National Academy of Sciences*, 122(47), e2518994122.
https://doi.org/10.1073/pnas.2518994122

### Global Workspace and Interpretability

Gurnee, W., Sofroniew, N., Pearce, A., et al. (2026, July 6).
Verbalizable representations form a global workspace in language models.
*Transformer Circuits Thread*, Anthropic.
https://transformer-circuits.pub/2026/workspace/index.html

Baars, B. J. (1988). *A Cognitive Theory of Consciousness.*
Cambridge University Press. ISBN 0521427436. 448 pp.

### Declared Influences

Shaw, F. (2014). *La otra atención: Notas del trabajo con Michel de Salzmann
(Chandolin, 1993–2000).* Sennin Editores. ISBN 978-987-28459-7-1.

Fremantle, C. (1993). *On Attention.* Indications Press.

---

## Appendix A — Writing Trace

The following entries record moments during writing where an automatic pull was noticed and resisted (see §3.4). Each entry is referenced in the text as AUTO-n.

**AUTO-1** (§6.4, text retired in v31; entry kept as trace) — tendency to write "demonstrates" for Case 0.15 — resisted. The refusal is documented behavior, not a demonstration of system capability under controlled conditions.

**AUTO-2** (§6.4, text retired in v31; entry kept as trace) — pull to keep the original reading with a softening qualifier. Resisted — the qualifier would preserve the claim while appearing to weaken it. The claim depends on a quantity that does not converge in the regime where it was taken.

**AUTO-3** (§7.1) — pull to write "CKM therefore captures something fundamentally new." Resisted — "fundamentally new" is a claim about the state of the field that would require systematic comparison with existing instruments. That comparison has not been done here.

**AUTO-4** (§7.5) — pull to write "the IAP series provides preliminary evidence for LDD behavior." Resisted — preliminary evidence requires at minimum a defined criterion for what would count as evidence. That criterion does not exist in the current analysis.

**AUTO-6** (§8.1) — pull to write "these results demonstrate CKM's validity as a measurement framework." Resisted — they demonstrate that specific structural properties exist in the tested corpora under stated conditions. Generalizability requires corpora the project has not accessed.

**AUTO-5** (§7.6) — pull to write "CKM resolves the limitations of static KR." Resisted — CKM does not resolve them. It inhabits and structures the space they left open. *(Written in v28; it left with §7.6 in v29 and returns with it in v33.)*

**AUTO-7** (§6.4, v31) — pull to explain the silence with a meaning, the way it was told in conversation. Resisted — the silence is in the channel logs; CKM does not register it; a meaning would be added by the one reading.

**AUTO-8** (§6.4, v31) — pull to present COCO's live connection in series 2 as the answer to the sentence retired in v30. Resisted — the retired sentence was not replaced; the connection is reported as a test condition, not as a correction.

**AUTO-9** (§6.4, v31) — pull to write that the separation in attempt 3 validates `calibrate`. Resisted — one run per attempt; what stands is that it separated, by the margin stated, and what the thresholds would have done.

**AUTO-10** (§7.3, v31) — pull to keep the case 0.12 example under the new formula. Resisted — that value was taken with the count-based distance; it does not belong to the current D_ckm.

**AUTO-11** (v32, header) — pull to answer the review point by point as a defense of v31 ("the baseline was right after all"). Resisted — the definition in v31 was wrong as written; the code was read and the text corrected; what v31 got right by accident is not claimed.

**AUTO-12** (§6.4, v32) — pull to keep "the 0 firings belong to the default" because the arithmetic supports it. Resisted — the arithmetic stays; the attribution goes, and the threshold's size against sampling is stated.

**AUTO-13** (§4.3.1, v33) — pull to state that N_eff ≥ 2 for every W because the collapsed extreme has a floor of 2 or more. Resisted — the floor is proven for the collapsed landscape only; the bound for every W is not established here.

**AUTO-14** (§7.6, v33) — pull to restore the retired section whole because the author decided it returns. Resisted — the claim that the static assumption went unquestioned in the 2023–2026 KR literature needs that literature reviewed; it is left out until then.
