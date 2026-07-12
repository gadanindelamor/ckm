# REG_iap_mcp_server_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

IAP MCP Server — mínima viable.
Capa MCP montada sobre la infraestructura de Demo C existente.
6 herramientas MCP operativas. Agentes externos pueden participar
en el canal IAP como clientes MCP.

Repo: `gadanindelamor/ckm` — `iap_chatroom/`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Archivos nuevos / modificados

```
iap_chatroom/
    mcp_server.py          ← nuevo: FastMCP + 6 herramientas
    test_mcp_client.py     ← nuevo: script de verificación 6/6
    server.py              ← modificado: lifespan + mount /mcp
    requirements.txt       ← modificado: + fastmcp
```

Sin cambios en: channel.py, ckm_monitor.py, device_manager.py,
api_routes.py, ui_gradio.py, providers/

---

## 6 Herramientas MCP

```python
join_channel(device_id: str, device_type: str) → dict
# registra device via DeviceManager
# devuelve {"ok": bool, "device_id": str, "registered_at": float}

send_message(device_id: str, text: str) → dict
# publica LNH al canal — CKMMonitor acumula automáticamente
# valida que device esté registrado (ValueError si no)
# devuelve {"message_id": str, "corpus_size": int}

get_messages(since: float | None = None) → list[dict]
# mensajes posteriores a `since` (timestamp)
# si since=None devuelve los últimos 20
# message_id generado como "msg-{índice}" sin modificar channel.py

get_monitor_state() → dict
# D_ckm, temp_signal, n_agentes, corpus_size, message_count, n_nodes

get_firma() → dict | None
# Firma_CKM — 6 campos canónicos
# None si corpus en acumulación (corpus_size < min_texts)

leave_channel(device_id: str) → dict
# desregistra device
# devuelve {"ok": bool}
```

---

## Restricción crítica — Lifespan fastmcp

**Hallazgo de Code.** No documentado obviamente en fastmcp.

Sin el orden correcto: `RuntimeError: Task group is not initialized`
en cada request a `/mcp`.

**Orden obligatorio en server.py:**

```python
# 1. FastAPI toma el lifespan de mcp_app — PRIMERO
app = FastAPI(lifespan=mcp_app.lifespan)

# 2. Router REST
app.include_router(api_router)

# 3. Gradio monta sobre lifespan ya seteado
app = gr.mount_gradio_app(app, demo, path="/ui")

# 4. Mount MCP — AL FINAL
app.mount("/mcp", mcp_app)
```

Si el orden cambia → falla silenciosamente en mounting,
explota en runtime al primer request MCP.

---

## Puerto

`server.py:58` corre en puerto **7860** (preexistente Demo C).
La especificación original asumía 8000 — corregido por Code
leyendo el archivo antes de ejecutar.

`test_mcp_client.py` apunta a `http://localhost:7860/mcp`.

---

## Verificación — criterios de éxito

| Criterio | Resultado |
|---|---|
| `GET /mcp` responde | ✓ (307→406, comportamiento normal streamable-HTTP sin headers SSE) |
| `test_mcp_client.py` → `6/6 OK` | ✓ corrida contra servidor real, sin mocks |
| `GET /api/monitor` sigue en 200 | ✓ REST coexiste con MCP |
| `GET /ui/` sigue en 200 | ✓ Gradio coexiste con MCP |

---

## Decisiones mínimo-invasivas (Code)

- `message_id` generado como `msg-{índice}` en `get_messages()`
  sin modificar `channel.py` ni el dataclass `Message`
- `send_message` valida registro de device antes de publicar
  (igual que `api_routes.post_chat` — consistencia con REST)
- Providers sin modificar — `complete()` async intacto
- Demo C sin modificar — Gradio en `/ui/` operativo en paralelo

---

## Ciclo de un device externo (ODA sobre MCP)

```python
from fastmcp import Client

async with Client("http://localhost:7860/mcp") as c:
    await c.call_tool("join_channel",
        {"device_id": "agent_x", "device_type": "AI"})
    loop:
        msgs = await c.call_tool("get_messages", {"since": last_ts})
        # Observar
        response = generar(msgs)
        # Decidir
        await c.call_tool("send_message",
            {"device_id": "agent_x", "text": response})
        # Actuar
        state = await c.call_tool("get_monitor_state", {})
        # CKM audit
```

---

## Coexistencia de capas

```
localhost:7860
    /api/*     REST (preexistente Demo C)
    /ui/       Gradio (preexistente Demo C)
    /mcp       MCP Server (nuevo)
```

Las tres capas comparten el mismo proceso FastAPI.
El CKMMonitor singleton acumula LNH sin importar
por qué capa llegó el texto.

---

## Estado

- mcp_server.py: implementado, en repo
- test_mcp_client.py: 6/6 passing contra servidor real
- Restricción lifespan: documentada aquí y en server.py
- Port 7860: corregido en especificación y test
- Demo C (REST + Gradio): sin regresiones

---

## Pendientes para iteración B

- `chat_stream()` streaming en providers (reemplaza `complete()` async)
- Persistencia CorpusService entre sesiones (ahora in-memory)
- Autenticación de devices
- Triggers automáticos Firma_CKM en lifecycle boundaries

---

## Archivos relacionados

- REG_iap_chatroom_demo_c_v1.md — Demo C (base de esta implementación)
- REG_firma_ckm_v1.md — FirmaService
- REG_protocolo_sonnet_code_v1.md — protocolo Sonnet/Code

---

*Jul 12 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
