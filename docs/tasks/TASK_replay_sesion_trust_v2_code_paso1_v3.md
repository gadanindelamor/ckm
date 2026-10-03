# TASK_replay_sesion_trust_v2_code_paso1_v3

*Clase T — subtask para Claude Code (Codespace) — Oct 2026*
*Parte de: TASK_replay_sesion_trust_v2. Leerla antes de empezar.*

---

## Verificación previa contra el repo local (Opus, Cowork — 3 oct 2026)

Lo que sigue se verificó leyendo el repo local, sin ejecutar código. Corrige la v2 de esta subtask.

1. **Ubicación del driver:** el repo no tiene `drivers/`. La convención es `experiments/`. Usar `experiments/replay_sesion_trust.py`.
2. **Precedente directo:** `experiments/replay_caso09_camino_vivo.py`. Ahí se midió que, con el camino del canal, W se reconstruye en cada mensaje y el conjunto de nodos no se estabiliza nunca. Por eso este replay construye W **una sola vez**: con `rebuild_suspendido=True`, o con `NodeExtractorService.accumulate` directo sobre las respuestas originales.
3. **Aislar el estado:** CorpusService persiste en `storage_path` (por defecto `corpus_state.json`). Hay que pasar una ruta dentro de `process/replay/_private/` para no pisar ningún estado existente.
4. **W_pos:** se obtiene con `force_w_pos=True`. Es un **flag de desarrollo**, el contrafáctico exacto ("mismo corpus, sin codificar su tensión"), y la W queda marcada en la traza (`forced_w_pos`). Se declara en el REG.
5. **Funciones que ya existen:** `landscape_engine.relax_orbit`, `basin_masses`, `n_eff`. La config está en `services/ckm_landscape_config.py` (clase `CKMlandscapeConfig`, con `l` minúscula). La divergencia de Jensen–Shannon **no existe**: va en el driver, que es Clase T, no en `services/`.
6. **Riesgo de degeneración:** `evaluate` asigna σ_i = +1 solo si el término aparece en el texto. Con respuestas cortas, la mayoría de los σ_i es −1 y muchas respuestas pueden caer en la misma órbita. **CP3 debe reportarlo** antes de seguir.
7. **Proveedor:** `iap_chatroom/providers/anthropic_provider.py` existe, pero su modelo por defecto es `claude-sonnet-5`, max_tokens está fijo en 4096 y no controla temperatura ni esfuerzo. Hay que extenderlo en el driver (sin tocar el provider del canal) o usar el SDK directo.
8. **Tensión de fondo — el harness:** la sesión original corrió dentro de Cowork, con system prompt, herramientas, memoria y proyecto. Un replay por API no tiene nada de eso. **El replay mide otro sistema**, y el REG tiene que decirlo. El modelo original de la sesión es `claude-opus-5-5`.

## Cambio de alcance respecto de v2

El paso 1 **no** usa la parte previa a la compactación: ese transcript no está disponible. Usa la **parte 2**, ya exportada y revisada por delamor:

`EXPORT_sesion_trust_parte2_v1.md`

## Lo que NO hace Code

- **No elige los tramos.** Los límites (turnos de inicio y fin) los entrega delamor en `tramos_paso1.json`.
- **No commitea el export ni los transcripts de replay a una rama pública.** Contienen conversación personal. Van en un directorio ignorado por git (por ejemplo `process/replay/_private/`, que se agrega a `.gitignore`). Al repo van solo el código, los resultados numéricos y el REG.
- **No interpreta.** Mide y registra. La lectura la hace delamor.

## Lo que hace Code

### A. Preparación
1. Parsear el export: los turnos están separados por `---` y encabezados `**delamor**` / `**Claude**` con timestamp.
2. Cortar los tramos según `tramos_paso1.json`. Formato:
   `[{"id": "museo", "desde": "<timestamp>", "hasta": "<timestamp>"}, ...]`
3. Por cada tramo, guardar los turnos humanos y las respuestas originales por separado.

### B. Driver — `experiments/replay_sesion_trust.py`
1. Reenviar los turnos humanos de cada tramo como conversación independiente, en orden.
2. Parámetros fijos y registrados en el output: modelo, temperatura, max_tokens. "Esfuerzo" solo si la API lo expone; si no, registrar que no se controló.
3. R = 5 replays por tramo.
4. Guardar cada replay en `_private/`.
5. Registrar costo en tokens por replay.

### C. Medición
1. **W única por tramo**, construida con CorpusService y NodeExtractorService desde las respuestas **originales** del tramo. Modo W_pos: sin marcadores de oposición, porque es un corpus de coordinación (paper v26 §5.1). Registrar sha256(W) vía WVersionManager y la CKMLandscapeConfig completa.
2. **Proyección:** cada respuesta, original o replay → `NodeExtractorService.evaluate(text, nodes)` → σ → relajar sobre la W única con `relax_orbit` (regla GOLES) → registrar la órbita final.
3. **Ocupación:** distribución de respuestas por órbita, para el original y para cada replay.
4. **Métricas:**
   - N_eff de cada ocupación;
   - divergencia de Jensen–Shannon original↔replay y replay↔replay;
   - dispersión replay↔replay como referencia del ruido del modelo.

### D. Salida
`registers/REG_replay_sesion_trust_paso1_v1.md` con:
- parámetros, sha256(W), config;
- tabla por tramo: N_eff (original, cada replay), JS original↔replay (media y rango), JS replay↔replay (media y rango);
- costo total;
- por cada resultado, su lugar: verificado / verificable / no verificable;
- §"Lo que no se afirma", copiado de TASK v2 §6.

## Checkpoints — Code se detiene y reporta

**Esto vale también para las acciones espontáneas.** Toda acción de Code que no esté en esta subtask (crear un archivo no previsto, cambiar un servicio, correr algo extra, abrir otra task) es un checkpoint: se detiene, reporta y espera el OK.

**CP0 — Code evalúa la task contra el repo.** Antes de escribir código:
- Leer esta subtask, TASK_replay_sesion_trust_v2 y los archivos citados arriba.
- Reportar tensiones entre la task y el repo: lo que no existe, lo que existe distinto, lo que contradice un REG.
- Sugerir consideraciones.
- No empezar A sin el OK.

En cada checkpoint, Code **se detiene**, entrega un reporte parcial breve y **espera el OK de delamor** antes de seguir. No se encadenan checkpoints. Si algo no coincide con lo esperado, se reporta: no se corrige en silencio.

Formato del reporte: qué hizo · qué salió (números) · qué no pudo · qué no esperaba · costo hasta ahora.

**CP1 — Parseo y corte.** Después de A.
- Cantidad de turnos del tramo `categorias` (humanos / Claude).
- Primer y último turno, citados en una línea.
- Confirmación de que el tramo no contiene datos personales.

**CP2 — Paisaje.** Después de C.1.
- N y la lista de nodos extraídos.
- μ_W, β_c, sha256(W) y la CKMLandscapeConfig.
- delamor revisa si los nodos tienen sentido para el tramo.

**CP3 — Original sobre su paisaje.** Proyectar solo las respuestas originales.
- Órbitas alcanzadas, ocupación y N_eff del original.
- Cuántas respuestas caen en cada órbita.

**CP4 — Un replay.** Correr **1** replay, no 5.
- Parámetros usados. Si "esfuerzo" está expuesto por la API, sí o no.
- Costo del replay.
- Ocupación, N_eff y JS original↔replay_1.
- Con esto delamor decide si se corren los otros 4.

**CP5 — R = 5 y borrador del REG.**
- Métricas completas (D).
- El REG se entrega como **borrador** fuera de `registers/`. Va a `registers/` solo con el OK de delamor, y desde ese momento es Clase R.

## Criterio de cierre
- Tests del driver: el parseo del export, el corte de tramos y que el pipeline corra sobre un tramo sintético chico.
- REG escrito. Sin commits de `_private/`.
- Siguiendo CONVENTIONS: ¿qué test debería haber cambiado con esto? Declarar los huecos.
