# REG_iap_chatroom_demo_claude_code_v0.md

*Jul 2026 — gadanin.delamor + Claude Code (Sonnet 5)*
*Clase R*

---

## Origen

Sesión Jul 2026. Encargo: construir `iap_chatroom/` — chatroom mínima
viable (FastAPI + Gradio) con CKM Monitor observando la interacción
en tiempo real, usando los servicios ya existentes en `services/`
(`NodeExtractorService`, `CorpusService`, `MonitorService`,
`FirmaService`) sin modificarlos.

Demo C: 3 devices (2 AI + 1 Human) publicando mensajes a un
`CorpusService` compartido, W emergiendo de la interacción — el
campo empieza vacío, sin precarga.

---

## Desviaciones respecto al spec original

**`iap/providers/` no existía** — ni en el repo ni en el filesystem.
El spec pedía copiar exacto desde ahí. Se preguntó al usuario; decisión:
escribir `providers/` desde cero (`base.py` + wrappers async delgados
para Anthropic/OpenAI/Gemini/Groq), ya que no había nada que copiar.

**API real de `services/` distinta a la asumida en el spec** — se leyó
`corpus_service.py` y `monitor_service.py` antes de escribir
`ckm_monitor.py` (paso explícito pedido) y se ajustó:

| Spec asumía | API real |
|---|---|
| `corpus.accumulate([text])` | `CorpusService.ingest(texts)` |
| `monitor.evaluate()` sin argumentos | `MonitorService.evaluate(text, agent_id=None)` |
| `firma.firmar()` sin argumentos | `FirmaService.firmar(corpus, monitor, n_agentes)` (stateless) |

Import de `services/` vía `sys.path.insert` + nombres de módulo
"bare" (`from corpus_service import ...`), igual que los módulos de
`services/` se importan entre sí — evita que la misma clase quede
duplicada bajo dos identidades de módulo distintas
(`services.corpus_service.CorpusService` vs `corpus_service.CorpusService`).

---

## Bug encontrado y corregido durante verificación

`server.py` usaba `uvicorn.run("server:app", ...)`. Con `reload=False`
esa forma no es necesaria, y causaba que uvicorn reimportara
`server.py` como un segundo módulo (`server`, distinto de `__main__`),
duplicando la ejecución de todo el código top-level — incluido
`channel.add_callback(ckm_monitor.on_message)`. Resultado: cada mensaje
se ingería 2 veces en el corpus (`ChatChannel`/`DeviceManager`/
`CKMMonitor` son singletons vía `__new__`, así que la instancia era
la misma, pero el callback quedaba registrado dos veces sobre ella).

Confirmado empíricamente: con 4 mensajes publicados, `corpus_size`
llegaba a 8 y cada texto aparecía duplicado en `corpus_state.json`.

**Fix:** `uvicorn.run(app, host="0.0.0.0", port=7860, reload=False)`
— pasar el objeto `app` directo en vez del string. Verificado después:
mensajes publicados == `message_count` == entradas únicas en el corpus.

---

## Estructura creada

```
iap_chatroom/
    __init__.py
    server.py            — entry point, singletons, mount Gradio
    channel.py            — ChatChannel (singleton), Message
    device_manager.py     — DeviceManager (singleton), Device
    ckm_monitor.py         — CKMMonitor (singleton), adaptado a API real
    api_routes.py          — REST + WebSocket
    ui_gradio.py            — chat + panel CKM Monitor (polling 3s)
    requirements.txt
    .env.example
    providers/              — escrito desde cero (no existía fuente)
        __init__.py, base.py,
        anthropic_provider.py, openai_provider.py,
        gemini_provider.py, groq_provider.py
```

`CKMMonitor.get_state()` expone: `corpus_size`, `n_nodes`,
`message_count`, `D_ckm`, `temp_signal`, `n_agentes`.
`CKMMonitor.get_firma()` expone los 6 campos canónicos de
`Firma_CKM` (`w_sha`, `d_ckm`, `temp_signal`, `n_agentes`,
`timestamp`, `delta_sha`) o `None` mientras el corpus está en
modo acumulación (`min_texts=3`).

---

## Demo C — verificación end-to-end

Registrados: `device_a` (AI, claude-sonnet-4-6, Anthropic),
`device_b` (AI, claude-haiku-4-5, Anthropic), `test_human` (HUMAN).

5 mensajes publicados en total (gun control / debate — mismo dominio
que los corpora de prueba ya usados en `services/`), sin llamar a
ninguna API de Anthropic — solo `POST /api/chat`.

```json
GET /api/monitor
{"corpus_size":5,"n_nodes":32,"message_count":5,
 "D_ckm":-0.2222,"temp_signal":"NOMINAL","n_agentes":3}

GET /api/monitor/firma
{"w_sha":"667753df...","d_ckm":-0.2222,"temp_signal":"NOMINAL",
 "n_agentes":3,"timestamp":1783712258.36,"delta_sha":"df089d73..."}
```

`GET /ui` → 307 (redirect Starlette a `/ui/`, comportamiento estándar
de `gr.mount_gradio_app`) → `/ui/` → 200, HTML de Gradio confirmado
(`og:title=Gradio`, metadata Twitter card, theming Gradio).

Sin excepciones en el log del servidor en ninguna corrida.

---

## Estado

- `iap_chatroom/`: implementado, criterios de éxito verificados,
  commit `feat: IAP Chatroom minima viable — Demo C` en `main`.
- `.gitignore`: se agregó `iap_chatroom/_state/` (corpus/trayectoria
  generados en runtime — regenerable, mismo criterio que `tmp_*.json`).
- Bug de doble-import por `uvicorn.run("server:app")` corregido antes
  del commit.
- Pendiente (no implementado, fuera de alcance de "mínima viable"):
  UI Gradio no dispara respuestas AI automáticas — `providers/` está
  disponible pero no está cableado a ningún device AI real; los
  mensajes "AI" en la demo se publican manualmente vía `POST /api/chat`,
  no generados por Anthropic/OpenAI/Gemini/Groq.

---

*Jul 2026*
