# TASK_tests_instrumento_v1

*10 oct 2026 — Opus (Cowork), con el acuerdo de delamor ("vamos a realizar esos tests"). Para Code, en el Codespace.*

## Por qué

Hoy se vio, con casos medidos, que lo que el instrumento informa no se puede leer todavía como campo:

- **el corpus ya es instrumento** (delamor);
- **los saltos son del instrumento**: el campo no salta, es continuo; las W son representaciones (delamor);
- con presencia sola W ≥ 0, **T = 0 por teorema** (T de `REG_hipotesis_distancia_contextual_v1`, mayo);
- la única tensión que entra hoy la ponen los **marcadores**, y en las corridas leídas fueron falsos positivos.

Estos tests son **del instrumento, no del campo**. Antes de medir el campo, el instrumento tiene que decir qué hace.

## Reglas

1. **No se arregla nada en este TASK.** Un test que hoy falla porque el código hace otra cosa se escribe con `@pytest.mark.xfail(strict=True, reason="<bug>, caso real: <archivo>")`. Rojo declarado: cuando alguien lo arregle, el xfail estricto obliga a mirarlo.
2. **No se toca el gate** (`f96c234`). **No se renombra nada.**
3. **Cada test lleva su caso real** (el texto o el archivo donde se vio) en el docstring. Varios archivos citados (`ckm_viz_corpus_state .json`, `corpus_natural_uniform.json`, el `corpus_state.json` con G) están en la PC de delamor, **no en el repo**: el fragmento de texto citado acá alcanza para el test; no se suben sin que delamor lo diga.
4. **Un CP por test**, cada uno con un REPORTE: verde / xfail / qué no se pudo testear y por qué.
5. Archivos nuevos en `tests/`, nombrados uno por uno al commitear (sin `git add -A`).

## Tests

### CP1 — Marcador por substring · `tests/test_marcadores_substring.py`

`CorpusService._has_opposition` busca con `m in t`.
- "power distribution, supply chains" **no** debe contar como oposición (`but` ⊂ "distri**but**ion"). Caso real: texto 3 (PeterPlam, CHANNEL OPEN) de `ckm_viz_corpus_state .json` y del caso con G (`corpus_state.json` del 0.15).
- "espero que llegue" **no** debe contar (`pero` ⊂ "es**pero**").
- "I disagree with that" **sí**.
- Esperado hoy: los dos primeros, xfail.

Registrar aparte (no testear como bug, es semántica): los usos narrativos de `but` en `corpus_natural_uniform.json` (cuento de Ava) y "a claim against observable reality" / "a disagreement" en el texto de TinkerBellucio que dice que todavía no hay tensión. El marcador por texto entero los manda a negativo.

### CP2 — SYSTEM fuera del corpus · `tests/test_system_fuera_del_corpus.py`

- Un mensaje SYSTEM ("X joined the channel") no entra a `corpus._texts`, no genera nodos (`joined`, `joined channel`) y no se evalúa en el panel.
- Verificar contra el código **actual** (el Monitor ya filtra SYSTEM desde el CP1 del canal). Si pasa, es regresión cubierta; si no, xfail.
- Caso real: `corpus_state.json` del 0.15 y `corpus_natural_uniform.json` (los joins como textos y como nodos).

### CP3 — Teorema de presencia · `tests/test_teorema_presencia.py`

Con `force_w_pos=True` (o con textos sin marcadores), sobre cualquier corpus:
- ningún W_ij < 0;
- 0 triángulos con producto de signos < 0;
- T(W) = 0.

Si algo de esto falla, el bug está en el instrumento (el teorema no puede fallar). Caso real: `_smoke_corpus_state.json` (20 textos, 0 negativos).

### CP4 — Estabilidad del instrumento · `tests/test_estabilidad_instrumento.py`

Sobre un corpus base de N textos, ingerir **un** texto neutro (sin marcadores, vocabulario ya presente) y medir:
- reescalado de W por `max_abs` (`corpus_service.py:267-270`): ‖W₁ − W₀‖ / ‖W₀‖;
- cambio de nodos o de N (top_k, pool `top_k·3`, idf);
- cambio de escala de Δ_r en `_combine_W_Delta` (Δ_r / max(Δ_r) × mean(W>0)).

**No se fija umbral** (no está decidido): el test **registra** las magnitudes y falla sólo si cambia N con un texto de vocabulario ya visto. Las magnitudes van al REPORTE: son el panorama de las discontinuidades para alinearlas en el salto (DECISIONES, 10 oct).

### CP5 — Declaración de la W · `tests/test_declaracion_w.py`

Cada W versionada (`w_version`) declara: método de extracción, versión del extractor (sha o identificador), unidad de co-ocurrencia, normalización. **Ningún campo heredado sin origen** (p. ej. `termap_version` en una W de CKM).
- Esperado hoy: xfail (la W declara sha de la matriz, `corpus_size` y `causal_event`; no declara extractor ni normalización).
- Caso real: `W_ckm_corpus_v2.json` (origen UNKNOWN, `termap_version` heredado) y `experiments/build_W_base_N64.py` (escribe `termap_version: v3_tfidf_auto`).

### CP6 — Campo plantado · `experiments/sintetico_campo_plantado.py` + REPORTE

No es unitario: es el **patrón de respuesta conocida**.
- Generador con campo conocido: dos o tres grupos de términos; dentro de cada grupo co-ocurren, entre grupos se evitan (signo verdadero conocido por construcción). Seed fija.
- Ingerir de a poco (por ejemplo, de a 10 textos) y, en cada paso:
  - W del repo (`CorpusService._rebuild`): negativos, T, triángulos frustrados;
  - W de ausencia, **φ y PMI**, calculadas en el script (no en `services/`): fracción de pares con el signo verdadero recuperado;
  - ‖ΔW‖ entre pasos (el campo está fijo: **todo salto es del instrumento**, por construcción).
- Esperado: la W del repo no recupera los negativos (no tiene canal para la ausencia); φ/PMI sí, a partir de algún tamaño de corpus. El REPORTE dice desde qué tamaño, con qué varianza (nulo por permutación, como el juguete del 10 oct).

**Decisiones abiertas de delamor que este CP no toma:** φ o PMI y contra qué nulo; W separadas o combinadas; sobre cuál juzga el Gatekeeper.

## Fuera de este TASK

Arreglar marcadores, normalizaciones o extracción; conectar `should_rebuild`; calibrar. Todo eso viene después, con delamor, sobre lo que estos tests muestren.
