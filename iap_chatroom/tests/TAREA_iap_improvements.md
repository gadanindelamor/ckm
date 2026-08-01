# TAREA: IAP improvements — umbral W, providers, status field, GUI test

Repo: gadanindelamor/ckm
Codespace: ckm

## LEER ANTES DE TOCAR
- iap_chatroom/ckm_monitor.py
- iap_chatroom/mcp_server.py
- iap_chatroom/channel.py
- iap_chatroom/test_iap_simulation.py

---

## ITEM 1 — Umbral rebuild(W) configurable

En CorpusService (services/corpus_service.py o donde esté min_texts):
- OLD: min_texts = 3 (hardcoded)
- NEW: min_texts configurable via constructor, default=3

En CKMMonitor o donde se instancie CorpusService:
- Exponer min_texts como parámetro. Sin cambio de comportamiento por defecto — solo lo hace configurable.

En mcp_server.py o server.py donde se instancia el monitor:
- Documentar en comentario que min_texts=3 es el default actual.

---

## ITEM 2 — get_monitor_state(): agregar campo status

En ckm_monitor.py, método get_state():

- OLD: devuelve D_ckm, temp_signal, n_agentes, corpus_size, message_count, n_nodes
- NEW: agregar campo "corpus_status":
  - "accumulating" si corpus_size < min_texts (W no existe, D_ckm=None)
  - "operational" si W existe y D_ckm es calculable

Esto permite al observador externo distinguir entre "aún acumulando" y "error/vacío".

Actualizar get_monitor_state() MCP tool en mcp_server.py para que devuelva el nuevo campo.

Actualizar test_mcp_client.py:
- OLD: assert "D_ckm" in r4.data
- NEW: assert "D_ckm" in r4.data and "corpus_status" in r4.data

---

## ITEM 3 — test_iap_simulation.py: 2 modelos mismo provider

Reemplazar FakeProvider por AnthropicProvider real con dos modelos distintos. La ANTHROPIC_API_KEY ya está en .env (real, no placeholder).

- agent_a_support → AnthropicProvider(model="claude-haiku-4-5-20251001")
- agent_b_grievance → AnthropicProvider(model="claude-sonnet-4-6")

Si AnthropicProvider no acepta model como parámetro de constructor:
- verificar providers/anthropic_provider.py — adaptar mínimamente.
- No reescribir el provider — solo agregar model como parámetro opcional con default al modelo actual.

Actualizar el docstring del script:
- Remover nota sobre FakeProvider como workaround.
- Documentar: "2 modelos Anthropic — evaluamos campo CKM, no providers."

CUSTOMER sigue siendo predefinido (HUMAN, sin provider).

---

## ITEM 4 — GUI: test funcional

Con el servidor corriendo (python iap_chatroom/server.py):

1. GET /ui/ → verificar 200 OK (ya sabemos que pasa)
2. Abrir la UI en el browser del Codespace o via curl:
   `curl -s http://localhost:7860/ui/ | head -50`
   Verificar que devuelve HTML con elementos de Gradio
3. Identificar qué campos/botones expone la UI (sin necesidad de interacción manual — solo leer el HTML)
4. Documentar en output: qué muestra la UI, si es funcional o solo un placeholder

---

## CRITERIOS DE ÉXITO
- [ ] min_texts configurable (default=3, comportamiento idéntico)
- [ ] get_monitor_state() devuelve "corpus_status" field
- [ ] test_mcp_client.py: 6/6 OK con nuevo campo
- [ ] test_iap_simulation.py corre con AnthropicProvider real (2 modelos)
- [ ] Output completo de la simulación (8 turnos + log CKM + Firma_CKM)
- [ ] GUI: descripción de qué expone /ui/

## DEVOLVER
- Output completo test_mcp_client.py (6/6)
- Output completo test_iap_simulation.py (8 turnos)
- Firma_CKM al cierre
- Descripción GUI
- Hash commit + push output
