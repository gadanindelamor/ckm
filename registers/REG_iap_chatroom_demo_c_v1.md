# REG_iap_chatroom_demo_c_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

IAP Chatroom mínima viable — Demo C.
Servidor FastAPI + Gradio con CKM Monitor observador.
3 devices (2 AI + 1 Human) sobre CorpusService compartido.
W emerge de la interacción LNH — campo vacío al inicio.

Repo: `gadanindelamor/ckm` — `iap_chatroom/`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Arquitectura implementada

```
ChatChannel (LNH)
    ├── device_a   (AI — claude-sonnet-4-6)
    ├── device_b   (AI — claude-haiku-4-5)
    └── test_human (HUMAN)

CKM Monitor (observador — no participa)
    ├── NodeExtractorService(top_k=32)
    ├── CorpusService()          ← vacío al inicio
    ├── MonitorService(corpus)
    └── FirmaService(corpus, monitor, n_agentes)
```

**Ciclo device** — no hay turnos. Cada device publica cuando tiene algo.
Todo el LNH del canal va al CorpusService sin filtro de origen.

---

## Estructura de archivos

```
iap_chatroom/
    server.py           FastAPI app + uvicorn entry point
    channel.py          ChatChannel (mensajes, broadcast WS, callbacks)
    device_manager.py   DeviceManager (registro, sin ciclo agéntico)
    ckm_monitor.py      CKMMonitor (observador, acumula en cada mensaje)
    api_routes.py       REST + WebSocket endpoints
    ui_gradio.py        Gradio UI montada sobre FastAPI en /ui/
    requirements.txt
    .env.example
    providers/
        base.py         Provider(ABC) con complete() async
        anthropic_provider.py
        openai_provider.py
        gemini_provider.py
        groq_provider.py
        __init__.py
```

---

## API

```
POST  /api/devices/register      registrar device
POST  /api/devices/{id}/unregister
GET   /api/devices               listar activos

POST  /api/chat                  publicar mensaje (broadcast + CKM Monitor)
WS    /api/chat/stream           recibir broadcasts en tiempo real

GET   /api/monitor               estado CKM
GET   /api/monitor/firma         Firma_CKM del momento

GET   /ui/                       Gradio UI (chat + monitor)
```

---

## Adaptaciones respecto a la especificación

**API de servicios CKM (leída de los archivos reales por Claude Code):**

| Especificación | API real | Estado |
|---|---|---|
| `corpus.accumulate(texts)` | `corpus.ingest(texts)` | corregido |
| `monitor.evaluate()` | `monitor.evaluate(text: str)` | corregido |
| `firma.firmar()` stateful | `firma.firmar(corpus, monitor, n_agentes)` stateless | corregido |

**Providers:** Claude Code escribió interface `Provider.complete()` async.
La interface IAP (`BaseProvider.chat_stream()` streaming) queda como target para opción B.
Para Demo C la interface async es suficiente — los devices AI no necesitan streaming en el canal.

**Bug encontrado y corregido:** `uvicorn.run("server:app", ...)` como string
reimportaba `server.py` como segundo módulo, duplicando el callback
`channel.add_callback(ckm_monitor.on_message)` — cada mensaje se ingería 2 veces.
Fix: `uvicorn.run(app, ...)` pasando el objeto directamente.

---

## Verificación — criterios de éxito

| Criterio | Resultado |
|---|---|
| Servidor arranca sin errores | ✓ |
| GET /api/devices → [] | ✓ |
| POST /api/devices/register | ✓ |
| POST /api/chat → Message | ✓ |
| GET /api/monitor con corpus_size y message_count | ✓ |
| GET /ui/ → 200 OK, HTML Gradio | ✓ |
| WS /api/chat/stream (broadcast) | ✓ |

---

## Estado CKM al cierre de la demo

5 mensajes publicados por 3 devices:

```json
{
  "corpus_size":   5,
  "n_nodes":       32,
  "message_count": 5,
  "D_ckm":        -0.2222,
  "temp_signal":  "NOMINAL",
  "n_agentes":    3
}
```

**Firma_CKM — 6 campos canónicos:**

```json
{
  "w_sha":       "667753df6a75913cbe5d36c4aa7dfedf6ca847d9ccdd3ec15bc2d8fb51446666",
  "d_ckm":       -0.2222,
  "temp_signal": "NOMINAL",
  "n_agentes":   3,
  "timestamp":   1783712258.3627133,
  "delta_sha":   "df089d7345fbd79974f68083efc2398a5fa231f3aacb8e90878675d4a3b9dbf5"
}
```

---

## Observación — primer comportamiento del campo grupal

**D_ckm = -0.2222** con 5 mensajes de 3 devices.

D_ckm negativo indica que el campo grupal tiene más atractores accesibles
que al inicio (t=0). El LNH de los 3 devices expandió el paisaje de atractores
en lugar de contraerlo. Primera observación empírica del campo grupal emergente
desde interacción real — no precargado, no sintético.

---

## Notas de diseño — decisiones confirmadas

- **W vacía al inicio** — el campo emerge de la interacción, no de corpus precargado.
  W precargada (W_ckm_corpus_v2.json) queda como experimento futuro (campo precargado vs emergente).
- **Todo el LNH acumula** — sin filtro por tipo de device (AI o HUMAN).
- **CKM Monitor es observador** — no participa en el canal.
- **Ciclo device, no agéntico** — sin turnos, publicación libre.
- **Text file upload** — pendiente diseño. Opción B: device con skill file_reader
  extrae texto y publica como LNH. El canal solo ve LNH.

---

## Pendientes para opción B (MCP server)

- Reemplazar `Provider.complete()` async → `BaseProvider.chat_stream()` streaming (IAP interface)
- Implementar mcp_adapter como capa de aislamiento A2A/MCP
- Triggers automáticos para Firma_CKM en lifecycle boundaries de sesión
- Persistencia de CorpusService entre sesiones (ahora es in-memory)
- Autenticación de devices

---

## Archivos relacionados

- `iap_chatroom/` — implementación completa
- REG_iap_coco_convergence_v1.md — convergencia IAP → COCO-thermostat
- REG_firma_ckm_v1.md — FirmaService implementado
- API_SPEC.md — especificación de servicios CKM

---

*Jul 10 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
