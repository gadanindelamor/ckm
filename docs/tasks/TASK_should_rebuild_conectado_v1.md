# TASK_should_rebuild_conectado_v1 — should_rebuild conectado y operativo

*10 oct 2026 — pedido de delamor: "dejar should_rebuild conectado y operativo en el código". Redacta Opus (Cowork); ejecuta Code.*

## Estado leído hoy (`ckm_monitor.py`, `corpus_service.py`)

- `CorpusService.ingest` reconstruye W en cada ingesta cuando `len(texts) ≥ min_texts`, salvo `rebuild_suspendido=True` con W ya construida (`corpus_service.py:94-110`). En el canal vivo, `CKMMonitor` arranca con `rebuild_suspendido=True` (L82): W se construye una vez y no se reconstruye más.
- `CKMMonitor` calcula `_last_rebuild_signal` (L190-194) con la jerarquía **estructural > volumen > tiempo** — "señal observable, no fuerza el rebuild todavía":
  - estructural: `CorpusService.should_rebuild(d_ckm_history, n=3)` (gradiente de D_ckm positivo n pasos);
  - volumen: `len(self._corpus._texts) >= min_texts * 2`;
  - tiempo: `_ciclos_sin_rebuild >= MAX_CICLOS` (10, provisional).
- `_ciclos_sin_rebuild` se resetea cuando cambia el sha de W (L172-177).

## Lo que se hace

1. **La decisión manda el rebuild.** En el camino del canal vivo, cuando `_last_rebuild_signal` es True, `CKMMonitor` llama a un rebuild explícito de `CorpusService` (método público nuevo, o el que ya exista, sin renombrar nada). `rebuild_suspendido=True` sigue impidiendo el rebuild **automático por ingesta**; el rebuild **por decisión** no queda bloqueado por ese flag. La primera W (fin de la acumulación) se construye como hoy.
2. **Causa declarada.** Cada rebuild por decisión registra cuál criterio disparó (`estructural` / `volumen` / `tiempo`) como `causal_event` en `w_version` y en el panel.
3. **Volumen = textos desde el último rebuild** (decisión de Opus, dentro del umbral, declarada): hoy cuenta el total del corpus, y después de `2·min_texts` queda en True para siempre — eso volvería al rebuild continuo que delamor descartó ("la ingesta no debe implicar rebuilds continuos").
4. **La historia de D_ckm es por ciclo:** se reinicia en cada rebuild, para que el gradiente no cruce de una meseta a otra (D_ckm se mide contra el baseline de su ciclo).
5. **Lugar para calibrar en el salto:** después del rebuild por decisión queda el punto donde va `calibrate` (`TASK_calibrate_mecanismo_v1`, confirmado; no implementado en este TASK). Hoy el punto existe y no hace nada; se declara así.

## No cambia

Los tests y drivers que usan `rebuild_suspendido=False` (rebuild por ingesta) siguen igual. No se toca el gate. No se renombra nada. Los umbrales (`n=3`, `2·min_texts`, `MAX_CICLOS=10`) quedan como están: **su valor es calibración**, no parte de este TASK.

## Tests (un CP cada uno, con REPORTE)

- CP1: con el canal vivo, ingesta sin señal → W no cambia (sha igual).
- CP2: cada criterio, con entrada conocida, dispara un rebuild y queda su `causal_event`.
- CP3: volumen cuenta desde el último rebuild (no dispara en el mensaje siguiente al rebuild).
- CP4: la historia de D_ckm se reinicia en el rebuild; Monitor invalida Δ_r como ya hace (D2).
- CP5: regresión — con `rebuild_suspendido=False` el comportamiento por ingesta es idéntico al de hoy.

## Para leer en el REPORTE

Medición previa (memoria 28 sep): en vivo, volumen y tiempo no se apagaban y el estructural no emitía con D_ckm cuantizado. Con el volumen por ciclo, decir con qué frecuencia dispara cada criterio en un smoke con Groq (opcional, al final).

## Recursos (criterio de delamor, 10 oct)

Cada test se verifica con los recursos al alcance del proyecto (local, Codespace, Groq). Lo que necesite un recurso fuera de alcance se implementa igual y queda **declarado** en el REPORTE con el recurso que falta; no se verifica hasta tenerlo.
