# TASK_replay_sesion_trust_v3

*Clase T — Oct 2026 — gadanin.delamor + Claude (Opus 5.5, Cowork)*
*Ejecuta: Claude Code, solo en Codespace.*
*Consolida TASK_replay_sesion_trust_v2 y la subtask paso1 v1–v4, más las decisiones tras el CP0 de Code. Reemplaza a todas. Antecedente Clase R: REG_divergent_sesion_trust_v1 (no se modifica).*

---

## 1. Qué se quiere saber

La sesión TRUST (28 sep – 3 oct 2026) fue en vivo y **no se puede reproducir**. Hay cuatro razones:

- el muestreo del modelo no es determinista;
- el harness, el contexto inyectado y la perilla de esfuerzo cambiaron durante la sesión;
- cada mensaje humano respondió a la salida anterior;
- hubo una compactación en el medio.

Por eso no se reproduce: se hace **replay**. Se reenvían los turnos humanos de un tramo y se mide si las respuestas nuevas **caen en las mismas cuencas** que las originales.

La pregunta no es si las respuestas salen iguales, porque no van a salir iguales. Es si el campo conserva la forma aunque el contenido cambie.

## 2. Insumos

| Archivo | Dónde | Qué es |
|---|---|---|
| `EXPORT_sesion_trust_parte2_v1.md` | `process/replay/_private/` | Turnos humanos y respuestas visibles de la parte 2 de la sesión (post-compactación), revisado por delamor |
| `tramos_paso1.json` | `process/replay/_private/` | Tramo(s) a usar, elegido(s) por delamor |
| esta TASK | `docs/tasks/` | — |

**Por qué la parte 2:** el transcript de la parte 1 no está disponible; el entorno donde vivía se recicló.

**Por qué `_private/`:** el export y los replays son conversación personal y el repo va a ser público. Code agrega `process/replay/` a `.gitignore` (OK dado por delamor). Al repo van solo el código, los números y el REG.

## 3. Paso 1 — un solo tramo

`categorias` (3 oct, 02:01–02:20): las categorías de verificabilidad. Es un tramo puramente conversacional, sin herramientas.

**Condición:** en la sesión original el esfuerzo estaba en **alto** (se subió a las 01:56 y se bajó a las 02:24). El replay registra con qué esfuerzo corre. Si la API no lo expone, esa comparación queda como **no verificable**.

## 4. Lo que hace Code

### A. Preparación
1. Parsear el export: turnos separados por `---`, encabezados `**delamor**` / `**Claude**` + timestamp.
2. Cortar el tramo según `tramos_paso1.json`, incluyendo la respuesta de Claude al último turno humano.
3. Guardar por separado los turnos humanos y las respuestas originales.

### B. Driver — `experiments/replay_sesion_trust.py`

**Por qué `experiments/`:** es la convención del repo (no existe `drivers/`). El precedente directo es `experiments/replay_caso09_camino_vivo.py`.

1. Reenviar los turnos humanos del tramo como conversación independiente, en orden.
2. Modelo: primero `claude-opus-5-5`, que es el configurado en la sesión original. Si la API lo rechaza, `claude-opus-5`, y se declara.
3. Registrar los parámetros: modelo, temperatura, max_tokens y esfuerzo (si la API lo expone; si no, registrar que no se controló).
4. **No usar tal cual** `iap_chatroom/providers/anthropic_provider.py`: tiene modelo por defecto sonnet, max_tokens fijo y no controla temperatura. Extenderlo dentro del driver, o usar el SDK directo. El provider del canal no se toca.
5. R = 5 replays, que se guardan en `_private/` junto con el costo en tokens de cada uno.

### C. Medición

1. **Una sola W**, construida desde las respuestas **originales** del tramo.
   - **Por qué una sola:** las cuencas de W distintas no se corresponden entre sí. Si cada replay tuviera su propia W, no habría forma de comparar.
   - **Por qué construirla una vez:** en caso09, W se reconstruía en cada mensaje y los nodos nunca se estabilizaron. Se usa `rebuild_suspendido=True` o `NodeExtractorService.accumulate` directo.
   - **W_pos, con `force_w_pos=True`:** una conversación es un corpus de coordinación, no de debate, y ahí los marcadores de oposición funcionan como conectores (paper v26 §5.1). Es un flag de desarrollo que deja `forced_w_pos` marcado en la traza, y se declara en el REG.
   - **Estado aislado:** `storage_path` va dentro de `_private/`, para no pisar `corpus_state.json`.
   - Registrar sha256(W) y `CKMlandscapeConfig`, con estos valores:
     - `sampling_mode = uniform`, coherente con la validación por enumeración exacta (§4.3).
     - θ_W es del Gatekeeper, que no participa aquí. Se pasa cualquier valor válido y se registra como **"no usado en este run"**.
     - `scale`: Code reporta qué controla. Si no interviene en ninguna cuenta, se trata igual que θ_W.
2. **Proyección:** cada respuesta, original o replay, pasa por `NodeExtractorService.evaluate(text, nodes)` para obtener σ, y se relaja con `landscape_engine.relax_orbit` sobre la W única (regla GOLES). Se registra la órbita final.
3. **Ocupación:** la fracción de respuestas que cae en cada órbita, para el original y para cada replay.
4. **Métricas:**
   - N_eff de cada ocupación (`landscape_engine.n_eff`);
   - divergencia de Jensen–Shannon original↔replay y replay↔replay. **No existe en el repo**: se escribe en el driver (Clase T), no en `services/`. Se puede calcular porque todas las ocupaciones viven en el mismo paisaje;
   - D_masa_cuencas **no** se usa para comparar replays, porque se define contra una línea base y no es una distancia entre distribuciones.

### D. Salida
REG borrador con:
- parámetros, modelo efectivo, sha256(W) y config;
- N_eff (original y cada replay), JS original↔replay y JS replay↔replay (media y rango);
- costo total;
- el lugar de verificabilidad de cada resultado: verificado / verificable / no verificable;
- §8, copiado textual.

Va a `registers/REG_replay_sesion_trust_paso1_v1.md` **solo con el OK de delamor**. Desde ese momento es Clase R.

## 5. Lo que Code NO hace

- No elige tramos.
- No commitea `_private/`.
- No interpreta: mide y registra.
- No toca `services/` ni el provider del canal.

## 6. Checkpoints — Code se detiene, reporta y espera el OK

**Vale también para las acciones espontáneas:** cualquier cosa fuera de esta TASK es un checkpoint.

**Por qué:** la precisión sobre la propia mecanicidad no se intenta desde adentro. Se construye como par. Los checkpoints son esa posición externa.

**Formato del reporte:** qué hizo · qué salió (números) · qué no pudo · qué no esperaba · costo hasta ahora.

| CP | Después de | Reporta |
|---|---|---|
| **CP0** | leer la TASK y el repo | Tensiones entre la TASK y el repo; consideraciones. *(Hecho el 3 oct; sus hallazgos ya están en esta v3.)* |
| **CP1** | A | Turnos del tramo (humanos / Claude); primero y último en una línea; confirmación de que no hay datos personales |
| **CP2** | C.1 | N, la lista de nodos, μ_W, β_c, sha256(W), config, qué controla `scale`. delamor revisa si los nodos tienen sentido |
| **CP3** | proyectar solo el original | Órbitas, ocupación y N_eff del original; **nodos activados por respuesta**. Si la mediana es ≤ 2 → posible colapso: se reporta y se espera |
| **CP4** | **1** replay | Modelo efectivo, si el esfuerzo está expuesto, costo, nodos activados, ocupación, N_eff y JS original↔replay_1. delamor decide si se corren los otros 4 |
| **CP5** | R = 5 | Métricas completas y el REG borrador fuera de `registers/` |

## 7. Tensiones de fondo, a declarar en el REG

- **El harness:** la sesión original corrió en Cowork, con system prompt, herramientas, memoria y proyecto. El replay por API no tiene nada de eso, así que **mide otro sistema**.
- **El esfuerzo:** original en alto, replay según lo que la API permita.
- **La escala:** un tramo corto tiene pocos textos y N chico. La escala condiciona la lectura, y se declara en vez de corregirse.

## 8. Lo que no se afirma

- Que los replays caigan en las mismas cuencas no muestra que la sesión se haya "reproducido".
- Que no caigan no muestra que la original fuera "falsa".
- Solo dice algo sobre la forma del campo bajo reenvío, en otro sistema y a esta escala.

## 9. Criterio de cierre

- Tests del driver: el parseo del export, el corte del tramo y el pipeline sobre un tramo sintético chico.
- REG borrador entregado. Nada de `_private/` commiteado.
- Según CONVENTIONS: ¿qué test debería haber cambiado con esto? Declarar los huecos.
