# TASK_monitor_coco_ciclo_orbita_v2

*5 oct 2026. Pedido de delamor; redacta Claude Opus 5.5 (Cowork); ejecuta Claude Code en el Codespace `ckm`. Verificada contra el clon local en `eddb4b0`.*
*Reemplaza a dos borradores de esta misma tarde que separaban en partes lo que es uno solo: `TASK_delta_r_orbita_torsion_v1` y `TASK_ciclo_vida_monitor_coco_v1`.*

**delamor (textual):**
- *"Monitor y COCO son aspectos de lo mismo. Si los hacen existir sin respetar el ciclo período, no hay métricas."*
- *"Que deje en paz a COCO. COCO es con Monitor."*
- *"Debe respetar la estructura."*
- *"Torsión. No hay giro."*
- *"No hay partes que sumar."*

**Reglas de trabajo.**
- Primero CP0, sin código.
- Checkpoints con feedback parcial, también para las acciones espontáneas.
- El código corre solo en el Codespace.
- Lo que se puede demostrar no se corre.
- Lo que es de delamor está marcado **[delamor]**.

---

**v2 (8 oct 2026, Opus):** se ajusta a `TASK_CKMlandscapeConfig_v3`, que ya está cerrada (CP3 `44af68a`). La v1 queda como traza. Se trabaja con `PROTOCOLO_code_continuidad_v1.md` (incluida la §8, la tríada). **Las preguntas siguen la numeración global: la próxima es P9.**

## 0b. Lo que cambió desde la v1

- **Números de línea:** se tomaron sobre `eddb4b0`. Con la Config v3, algunos archivos cambiaron (`monitor_service.py`, `ckm_monitor.py`). Ubicar por nombre de función, y reportar si alguna referencia ya no coincide. Verificado el 8 oct: `coco.py` L268 (`frac_rec`) y L570 (`_classify_zone`) siguen ahí; `ckm_monitor.py` pasó de L93 a L104.
- **Los reportes van a la bandeja,** no a delamor directamente (en la v1 decía "Reportar a delamor").

- **Ya hay un reloj de ciclo.** `MonitorService._invalidar_si_W_cambio` llama a `config.abrir_ciclo(...)` en el mismo bloque donde resetea Δ_r (Config v3 CP2, D4). El ciclo vigente se lee de `config.ciclo_vigente`, que se lee entero y bajo lock. Con el mismo sha no se abre ningún ciclo (I5).
- **El canal vivo construye la Config** sin θ_W ni scale (opción iv). Como `CKMMonitor` usa `rebuild_suspendido=True`, **en el canal hay un solo ciclo** (bootstrap). COCO va a nacer una sola vez ahí, hasta que alguien levante la suspensión.
- **Causa del ciclo:** `"N" | "nodos" | "pesos" | "bootstrap" | "W_distinta"` (P7).
- **θ_W ya no está en la Config.** Es del Gatekeeper, y COCO no lo usa.

## 0. Lo que pasa hoy (leído en el código)

Monitor y COCO son dos aspectos de una misma cosa: Monitor nota y COCO regula. Hoy esa cosa existe partida en dos puntos, y en los dos el corte no respeta ni el ciclo ni el período.

**En el ciclo de W.** CorpusService crea a COCO en cada `_rebuild()` (`corpus_service.py` ~L293–295: `self._coco = COCO(W=self._W, ...)`). Monitor, en cambio, se queda con el COCO que recibió como `thermostat` al construirse. Cuando W cambia, `_invalidar_si_W_cambio` (`monitor_service.py` L258) resetea Δ_r, A0 y N_eff0, pero *"COCO queda fuera de alcance"*. Resultado:

- quedan dos COCO vivos, `corpus.coco` (nuevo) y `monitor._thermostat` (con la W congelada);
- se miden 56 incrementos negativos en `Δ_r_compresiones` (`TASK_delta_compresiones_coco_v1` §Abierto);
- el docstring de COCO lo resume como *"una sola cantidad, dos baselines"*;
- el canal vivo (`iap_chatroom/ckm_monitor.py` L104 (era L93)) lee el COCO de Corpus, no el de Monitor;
- Corpus lo crea con la configuración por defecto (seed 0, n_runs 80), mientras que los tests usan seed 123;
- todo esto ya está registrado en `REG_coco_w_congelada_v1` y se reproduce con `experiments/coco_lifetime_analytics.py`.

**En el período de la órbita.** `MonitorService._relax` → `relax()` → `relax_orbit(...)[3]` devuelve un solo estado: el que cae en `max_iter = 200`, con la fase elegida por la paridad de ese número. Con ese estado se calculan `_rejected_pairs` → `Δ_r_pares`, `c(S)` y `fabrication_index`. Δ_r entra a W_eff, que es lo que COCO lee. El docstring de `_relax` lo reconoce: *"el test que separa los casos es 100 contra 101"*. En caso09_run2 natural, 136 de 200 runs terminan en período 2.

**Demostrado, no hace falta correrlo:**
1. En una órbita de período 2, las dos fases difieren en al menos un nodo. Si alguno de esos nodos está entre los declarados activos, el conjunto de pares expulsados cambia con la paridad.
2. Si el rebuild cae mientras se procesa un texto que relaja a período 2, la traza que hereda el nuevo ciclo se escribió desde una sola cara.

**Por qué no hay métricas.** D_ckm compara contra un baseline. Hoy hay dos baselines, nacidos en suelos distintos, y escritos desde una sola fase. Comparar a través de eso es comparar parado en dos suelos y mirando una sola cara de la cinta.

## 1. La estructura que hay que respetar

**Una sola existencia.** Monitor y COCO nacen, viven y mueren juntos. El reloj es uno: **el ciclo vigente de la Config**. Monitor lo abre (`abrir_ciclo`), y COCO renace **si y solo si se abrió un ciclo nuevo**, en el mismo bloque y con la misma causa. COCO es con Monitor: vive dentro de él. Monitor puede seguir existiendo sin COCO (`thermostat=None`), como hoy.

**Sus contenidos no se funden** (D3, acuerdos de `TASK_delta_compresiones_coco_v1`):
- Δ_r es de Monitor y solo Monitor escribe en él;
- COCO tiene su `Δ_r_compresiones`;
- la divergencia entre los dos (`delta_collective`) se preserva.

Se alinea el existir, no lo que cada uno registra.

**La órbita es el objeto.** Toda medición dentro del ciclo se hace sobre la órbita completa (las dos fases, sin orden, como el `frozenset` de `relax_orbit`), no sobre la fase que cae en `max_iter`. Para cada par (i, j) de nodos declarados activos, con R_A y R_B los pares expulsados en cada fase:

| clase | condición |
|---|---|
| **aceptado** | ∉ R_A y ∉ R_B |
| **expulsado** | ∈ R_A y ∈ R_B |
| **torsión** | en exactamente una de las dos |

- La torsión es la marca del período 2. Se registra aparte y **no se promedia**: el coseno la convierte en 0 y la aplana.
- En un punto fijo, R_A = R_B y no hay torsión. En ese caso todo es idéntico a hoy, y esa es la invariante de compatibilidad.

**El nacimiento respeta el período.** Cuando cambia W, el nuevo ciclo hereda la órbita, no una fase.

**CorpusService deja en paz a COCO.** Construye W y la versiona. No crea, no guarda y no expone a COCO.

## 2. Checkpoints

### CP0. Evaluar contra el repo (sin código)

Reportar al menos lo siguiente.

1. **Usos de `relax` de una sola fase:**
   - `landscape_engine` L258 y L284 usan `relax`; L314 y L362/376 usan `relax_orbit`. ¿Qué función es cada una? ¿Alguna alimenta algo vivo?
   - `coco.py` L593/597 tiene las dos variantes.
2. **Identidad `relax(−σ) = −relax(σ)`** (ρ* = 0.5, en `coco.py` L104/412 y `landscape_engine` L32). Confirmar que vale fase a fase, demostrándolo por simetría, sin correr.
3. **Usuarios de `corpus.coco`:**
   - `ckm_monitor.py` L104 (era L93 en `eddb4b0`);
   - `test_armstrong_n_runs_sweep.py` L73;
   - `test_armstrong_via_corpus_v3.py`;
   - `coco_lifetime_analytics.py`.

   Los tests Armstrong son traza registrada y **no se modifican**; quedan como históricos.
4. **Configuración de COCO al renacer** (seed, n_runs, sampling_mode, track_landscape): tiene que ser la misma, y estar declarada, no implícita.
5. **β:** qué acumula y qué se reinicia (`coco_lifetime_analytics` §C). Lo registrado dice: *"β no puede persistir si cambia W; muere con el rebuild; el historial por w_version_id puede ir como registro"*.
6. **Encaje con la Config v3.** COCO toma su `sampling_mode` de lo **declarado** en la Config, y no de un default propio. Lo demás de COCO que haga falta declarar (seed, n_runs, track_landscape): ¿va a la Config como declarado o queda en la configuración de COCO? Reportarlo, sin decidir (pregunta Pn). COCO lee el ciclo con `ciclo_vigente` (get consistente), nunca campo por campo.
7. **Comparabilidad.** Los JSONL y los paneles históricos (`n_rejected_pairs`, `panel["rechazados"]`) se escribieron con una sola fase y con dos COCO. Declararlo.
8. **El vacío al dividir.** Al renacer, la existencia arranca vacía: Δ_r en ceros, A0 y N_eff0 en None. La primera división se hace contra ese vacío. Hoy el vacío se disfraza de medición:
   - `d_ckm`/`d_masa_cuencas` devuelve None cuando N_eff0 ≤ 1, porque ln N_eff0 = 0. Eso está bien.
   - Pero `coco._classify_zone` (L575) traduce `D_ckm None` a **"stable"**. Y `coco.observe` (L268) define `frac_rec = A_current/self._A0 if self._A0 > 0 else 1.0`, o sea que la ausencia de baseline se lee como **recuperación total**.

   Es el mismo patrón que ya se corrigió en `temp_signal` (`c06db07`: *"el fallback de temp_signal es UNKNOWN, no NOMINAL"*), y el mismo criterio que SALAMANCA: "no medible" no es "nada". Sin baseline no hay métrica, y eso se declara: zona **UNKNOWN** y `frac_rec` None. No se lee como estable.
   - Revisar todos los bordes `if A0 > 0 else …`, `None → valor` y `max(0, …)` en Monitor, COCO y `landscape_engine` (por ejemplo, L418 `… if A0 > 0 else 0.0` en la forma deprecada).
9. **Tests afectados:** `tests/test_monitor_services.py`, `test_invalidacion_delta_r.py`, `test_delta_compresiones_coco.py` y los `iap_chatroom/tests/test_caso_*.py`.

**Alto. REPORTE en la bandeja (PROTOCOLO §6). Opus decide o escala (§5).**

### CP1. Medir lo que hoy se rompe (sin tocar `services/`)

Driver en `experiments/` con pre-registro en el docstring, escrito antes de correr. Sobre caso09_run2 natural y WARMUP_TEXTS:

- **Paridad.** El loop de Monitor con `max_iter = 200` contra `201`. Por texto: período, |R_A|, |R_B| y |R_A △ R_B|. Al final: la diferencia entre los dos `Δ_r_pares` y la diferencia de `c(S)`.
- **Dos existencias.** Identidad de instancia de COCO contra los resets de Monitor, y los incrementos negativos en `Δ_r_compresiones`. Se puede reusar `coco_lifetime_analytics` A/F.
- **Puede fallar.** Si la paridad no pesa por debajo del umbral declarado, se registra así.

Commit, versiones y seed van en el log.

**Alto. REPORTE en la bandeja (PROTOCOLO §6). Opus decide o escala (§5).**

### CP2. Una existencia, medida sobre la órbita

- `landscape_engine`: una función pura `pares_por_orbita(sigma_prompt, fases) -> (aceptados, expulsados, torsion)`. Las fases ordenadas se recuperan de `seq[prev:]` en `relax_orbit`.
- `MonitorService` recibe una **configuración** de COCO (o una fábrica), no una instancia. Crea su COCO cuando se abre el primer ciclo (bootstrap), y lo recrea **cada vez que `abrir_ciclo` devuelve True**, en el mismo bloque y con la misma causa que el ciclo (`coco_renace` en el panel, junto a `Delta_r_reset` y el `ciclo_vigente`).
- `thermostat=COCO(...)` externo queda aceptado solo en transición, con un warning declarado: *"instancia externa, no renace"*.
- El panel registra las tres clases (`n_torsion`, `pares_torsion`). **Qué entra a `Δ_r_pares` no cambia todavía:** eso es el CP3.
- **Tests:**
  - invariante de punto fijo: con torsión vacía, todo idéntico a hoy;
  - un caso de período 2 construido a mano, con torsión conocida;
  - intercambiar A y B no cambia nada;
  - COCO renace en el mismo paso que el reset de Δ_r;
  - **cero incrementos negativos** en la secuencia que hoy da 56;
  - **vacío**: en el paso del renacimiento y en cualquier evaluación con N_eff0 ≤ 1 o A0 None, la zona es UNKNOWN y `frac_rec` es None. Nunca "stable" ni 1.0. Además, OPERADOR de compresión no se aplica sin medición, y eso queda registrado como no aplicado por vacío, no como estabilidad;
  - con `thermostat=None` el panel queda igual que hoy;
  - la configuración de COCO es la misma antes y después de renacer.
  - **COCO renace si y solo si se abre un ciclo:** con el mismo sha, ni ciclo nuevo ni COCO nuevo;
  - **en el canal** (`rebuild_suspendido=True`), COCO nace una vez con el bootstrap y no vuelve a renacer. Con la suspensión levantada a mano en el test, renace con el ciclo siguiente.

**Alto. REPORTE en la bandeja (PROTOCOLO §6). Opus decide o escala (§5).**

### CP3. Lo que es de delamor (después de ver CP1 y CP2)

1. **Qué entra a `Δ_r_pares` y a W_eff.**
   - (a) Solo **expulsado**, y la torsión en un objeto propio (`Δ_r_torsion`, que escribe solo Monitor) que no entra a W_eff.
   - (b) La torsión también entra, con un peso declarado.
   - (c) Nada cambia y la torsión queda solo como observación.
2. **`landscape_history` a través del salto:** si cruza como registro (solo lectura) o no cruza.
3. **Baseline de COCO:** sobre W sola o sobre W + Δ_r. Esto define qué es D_ckm_coco, que está abierto.
4. **Con qué nace el nuevo ciclo** si el salto cae en un período 2: con la órbita (lo que propone §1) o con otra cosa.

### CP4. CorpusService suelta a COCO (después del CP3)

- Sacar `self._coco` de `_rebuild` y deprecar la property `coco`, declarándolo en el CHANGELOG.
- `ckm_monitor.py` pasa a leer desde Monitor.
- Correr los tests de `tests/` y los que no son Armstrong.

## 3. Lo que esta TASK NO hace

- No cambia `relax` ni `relax_orbit`, ni el criterio ni el momento del rebuild.
- No toca la fórmula de compresión ni los umbrales.
- No une Δ_r con `Δ_r_compresiones`.
- No promedia con coseno ni pasa a ángulos.
- No reinterpreta resultados viejos ni modifica REG o tests Armstrong.

## 4. Literatura (leer antes del CP2)

- Goles-Chacc et al. (1985): con W simétrica y dinámica síncrona, se llega a un punto fijo o a período 2. La prueba usa un desdoblamiento bipartito, que es un recubrimiento doble.
- Grafos con signo y frustración como invariante de gauge: Harary; Zaslavsky; Toulouse (1977); Mattis (1976). Es el marco de la torsión; se cita, no se reclama.
