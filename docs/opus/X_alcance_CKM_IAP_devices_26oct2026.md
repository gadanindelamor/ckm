# X — Hasta dónde llega CKM: instrumento, canal y devices — Opus 5.5, 26 oct 2026

Pedido de delamor: *"el punto X es para que corrijas las definiciones y des tus propuestas… viene de darme cuenta que quizás estábamos implementando IAP devices, y hasta dónde llega CKM instrumento"*.
Base: lo que el repo tiene hoy (`git ls-files`, imports y docstrings, leídos el 26 oct). Lo que no está en el código va marcado como propuesta.

---

## 1. Lo que el repo tiene hoy: son cuatro cosas, no una

| capa | archivos | qué es |
|---|---|---|
| **Productor de W** | `services/corpus_service.py`, `services/node_extractor.py` | La extracción: texto → nodos → W. El paper (§4.1.6) ya dice que *"operators 2–7 belong to the producer"*. |
| **Instrumento CKM** | `services/landscape_engine.py`, `monitor_service.py`, `coco.py`, `calibrate.py`, `ckm_landscape_config.py`, `w_version.py`, `firma_ckm.py`, `ckm_trust_rule.py`, `cluster_frontier_density.py`, `analytics.py` (y `behavior_graph.py`, PoC) | Relajación, masas de cuenca, N_eff, D_ckm, Δ_r, COCO, calibración, Config, traza. |
| **Canal IAP** | `iap_chatroom/channel.py`, `server.py`, `api_routes.py`, `mcp_server.py`, `ui_gradio.py`, `run_store.py`, `startup.py`, `device_manager.py` | El canal BROADCAST, con MCP como interfaz. |
| **El puente** | `iap_chatroom/ckm_monitor.py` | El **único** archivo de `iap_chatroom/` que importa el instrumento (`CorpusService`, `MonitorService`, `CKMlandscapeConfig`, `landscape_engine`). Es CKM con contexto de canal. |
| **IAP devices** | `iap_chatroom/autonomous_device.py`, `local_criterion.py`, `agent_device_skin.py`, `groq_research_agent.py`, `providers/` | Los devices, los skins y el acceso a los LLM. |

**Fuera de CKM, aunque esté en `services/`:** `gatekeeper_c1.py`. Juzga capacidades declaradas de devices (linaje IAID), no el paisaje. El paper (§4.1.4) ya lo dice: *"not exercised in this work"*.

**El límite ya existe en el código:** los devices **no importan nada de `services/`**. Ven a CKM solo por MCP (`get_monitor_state`, `get_firma`). Lo único que el device le pasa al instrumento es el texto que publica.

**Así que sí: estábamos implementando IAP devices.** El repo `ckm` aloja instrumento, productor, canal y devices. Las series 1 y 2 probaron los cuatro juntos.

---

## 2. Correcciones a tus definiciones

**AGENTE** = *"arnés con ciclo AGÉNTICO + MULTITURNO + declared capabilities + config + LLM + agentic trained"*.
- *Propuesta:* "agentic trained" es una propiedad del LLM, no del arnés: `agent_harness(LLM_agentic)`.
- *Propuesta:* lo que separa al agente del device no es el multiturno (el device también tiene una ventana de historia), sino **quién cierra el lazo**. El ciclo agéntico termina cuando se cumple el objetivo. El ODA no termina por objetivo: es continuo, y en cada vuelta puede publicar, irse o no hacer nada.

**IAP DEVICE** = *"arnés con ciclo ODA + FREE WILL + declared capabilities + config + LLM"*.
- **Corrección, por el código:** al device le falta el **criterio local**. `local_criterion.py` lo importa `autonomous_device.py`, y su docstring dice que está *"entre O y D… decide si esta vuelta paga una llamada"*. Es parte del device.
- *Propuesta:* agregar que **observa el canal y el campo solo por MCP**, y que su única entrada al instrumento es el texto que publica.

**IAP** = *"canal BROADCAST + CKM instrumento con contexto de canal + config() (sin transferencia latente requerida, sin memorias externas)"*.
- De acuerdo, y coincide con el código (el puente es `ckm_monitor.py`).
- *Propuesta:* agregar `run_store` (la traza de la corrida) y el MCP como **única interfaz**.
- *Propuesta:* "sin transferencia latente, sin memorias externas" es una **condición que el canal no exige** a los devices. Mejor escribirla así que como una propiedad del canal: un device con memoria propia puede entrar igual, solo que IAP no se la da.

**IAP_DEVICE_SKIN** = `iap_device_skin(AI AGENT)` = `ODA(AGENTIC_LOOP(LLM))`.
- Coincide con el código: `AgentDeviceSkin` es una subclase de `AutonomousDevice` que delega `_decide()` y `_generate()` en el agente envuelto. O y A son del arnés ODA; D y el contenido son del agente.
- **Corrección de nombre:** el archivo es `agent_device_skin.py`, no `device_skins.py`.

---

## 3. Tus preguntas, con mi propuesta

- **¿El criterio local es IAP o device?** Device, por el código (ver §2).
- **¿Los IAP devices son CKM?** No. No importan el instrumento: son lo que el instrumento mide, a través de su texto, y pueden leer lo que mide.
- **¿Son Landscape Driven Devices?** No por definición. LDD es un encuadre propuesto (§7.5 del paper): un device cuya trayectoria está codeterminada por la geometría del campo. Un IAP device que lee `get_monitor_state` en su O es **candidato**. Que lo sea no está verificado.
- **¿Diseñar un device es CKM?** No. Es trabajo de IAP / IAID.

**Corrección a "outputs: métricas, intervenciones en campo":** hoy CKM **no interviene en el campo**. COCO comprime su propia copia (`Δ_r_compresiones`), y el docstring de `coco.py` dice *"la regulación no llega a Δ_r"*. Lo que sale de CKM son métricas (el panel, Firma) y una regulación sobre su propia representación. Que la intervención llegue al campo es la dirección del §7.5 (LDD), propuesta, no implementada.

---

## 4. Propuesta: dónde termina el instrumento

- **Entra:** W, con su declaración de extracción, y los σ de cada texto al evaluar. Y la Config: lo declarado.
- **Adentro:** relajación, masas de cuenca, N_eff, D_ckm (dos instancias), Δ_r, COCO, `calibrate`, Config, `w_version`, Firma, la regla TRUST.
- **Sale:** métricas y traza, más la regulación sobre su propia representación.
- **Afuera:** el productor (se declara), el canal IAP, los devices y skins, el gatekeeper.

**Qué hacer con esto (propuesta, decide delamor):**
1. **Declararlo, sin mover código.** Un párrafo en el README y en el paper (§1 o §4.2.3): el repo aloja cuatro capas, el instrumento es una, y la serie IAP prueba el instrumento a través del canal y los devices.
2. **Si algún día se separa**, el corte natural es el que el código ya tiene: `services/` sin `corpus_service`, `node_extractor` ni `gatekeeper` es el instrumento, y `ckm_monitor.py` es el puente. Sería un refactor declarado y, como no hay versiones de producto, sin compatibilidad hacia atrás. No ahora.
3. **Para el v33:** una frase en el §6.1 que diga que los devices no son parte del instrumento y que lo ven solo por MCP. Coincide con *"The contribution is that separation, not the sequence"* (§6.1, nota de antecedente).

## 5. Abierto, de delamor
- Si las definiciones con estas correcciones quedan como texto del proyecto (README, DEFS) o solo como nota.
- Si `behavior_graph.py` (G) es instrumento o es otro productor de W.
