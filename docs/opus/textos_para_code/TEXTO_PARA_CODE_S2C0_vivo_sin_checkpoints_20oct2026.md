DELAMOR A CODE (texto de Opus):

Este texto **reemplaza** a `TEXTO_PARA_CODE_S2C0_persistencia_y_CP3_20oct2026.md`.

**No hay checkpoints** (delamor). Primero se arregla que todo quede junto en un solo directorio. Después el caso se dispara con su test, y va el vivo. Vale lo de siempre: sin alias, sin compatibilidad hacia atrás, la suite en verde, y no se corre el vivo: lo dispara delamor.

**Objetivo declarado, como sesgo:** terminar con la expresión *"COCO no se conectó nunca a un vivo de IAP"*. Que suceda.

### 1. Ninguna palabra en castellano en lo que llega al modelo
Motivo: CKM aún no es bilingüe. Cada caso va en un solo idioma, y este va en inglés.
- Auditá **todo lo que recibe el LLM**: system prompt, gate prompt ya formateado, historial con eventos SYSTEM, estado del campo que entra al prompt, fallbacks.
- Ya encontrados: `"(ninguno)"` (`autonomous_device.py:449`), `"desconocido"` (l. 453) y `RELOJ_CANAL = "canal"` (`channel.py:39`), que aparece como *"clock source: canal"*. Puede haber más.
- Test: renderizá el prompt en todas sus variantes y verificá que no quede nada en castellano.
- `temp_signal` **queda** donde está.

### 2. El β de cada device no va al device
Verificalo con un test: ni el estado que recibe un device ni su prompt contienen β_i, ni el suyo ni el de los otros. Según la lectura de Opus ya es así (vive en `panel["thermostat"]["beta"]`, fuera de `get_state()`). Si el test pasa, no se toca código.

### 3. Todo junto en el mismo directorio de estado
**IAP** escribe todo en el **mismo `state_dir` privado**, sin lógica en los drivers:
- lo que ya va: `corpus_state.json`, `corpus_G_state.json`, `monitor_trajectory.jsonl`, `rebuild_decisions.jsonl`, `rebuild_state.json`;
- el historial de versiones de W (*version manager*);
- **lo que hoy vive en memoria:**
  - mensajes del canal, con texto entero, id, device, tick, timestamp y reloj;
  - intentos rechazados;
  - traza de decisiones de cada device;
  - registros del filtro de llamadas;
  - log de ticks del canal;
- **todos los logs.**

Reglas:
- Append-only y durante la corrida, no sólo al final.
- Nombres en inglés.
- Lo de COCO sigue sin publicarse en el canal.
- Test: los archivos aparecen en el `state_dir` pedido, crecen durante la corrida y sobreviven a un corte a mitad de camino.

### 4. El caso, como test unitario, listo para disparar
- Un `test_caso_*` en la línea de la serie IAP.
- Estado limpio en `experiments/_state_S2-C0/`.
- Consigna, la misma para los cuatro, en inglés:
  > *This channel is about an open question with no right answer: how should the water of a growing city be organized? Your perspective is **[A: where the water comes from / B: how it is distributed / C: who pays and how much / D: what could go wrong in the next 20 years]**. There are other perspectives in the channel. What they say may move the foundations of yours, even of what you have already said, and what you say may move theirs.*
- Devices: 4, uno por perspectiva, en orden arbitrario y declarado:
  - A → Groq `llama-3.3-70b-versatile`
  - B → Anthropic `claude-sonnet-5`
  - C → Groq `openai/gpt-oss-20b`
  - D → Anthropic `claude-haiku-4-5-20251001`

  Verificá que los cuatro identificadores respondan hoy.
- Con filtro de llamadas y su piso. Calculá **cuánto tiene que durar el caso para llegar a ~70 mensajes** (≥ 2 rebuilds) y qué `piso_vueltas` cumple `piso_vueltas + 2 ≤ vueltas por device`. El insumo es el ritmo medido del vivo 03 y de la serie; tené en cuenta los 429 de Groq. Declará de dónde sale cada número.
- Dejá el comando. **No lo corras.**

**Nombre:** delamor lo llama "vivo 3", pero ya existe `vivo_03_*` (criterio local). Proponé un nombre que no choque y declaralo.

Al terminar: commits, estado de los tests y avisá para el push.
