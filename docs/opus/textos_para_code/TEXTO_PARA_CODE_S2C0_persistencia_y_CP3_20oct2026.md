**NO SE PEGA — reemplazado por `TEXTO_PARA_CODE_S2C0_vivo_sin_checkpoints_20oct2026.md`.**

DELAMOR A CODE (texto de Opus):

Vale lo de siempre: no se toca el vivo hasta que delamor lo corra, sin alias, sin compatibilidad hacia atrás, y la suite cierra en verde.

**Objetivo de S2-C0 CP3, declarado como sesgo** (delamor): terminar con la expresión *"COCO no se conectó nunca a un vivo de IAP"*. Por límites, el objetivo es **que suceda**. Todo lo demás queda como está.

**Orden (delamor): primero CP3, luego CP2 y fixes.** Lo del CP2 ya está cubierto por tests y por la medición del 19 oct (COCO conectado y evaluando, primer W a los 30, ODA con canal en silencio, corte al fin del caso); se retoma después del vivo.

**(0) Antes del CP3: ninguna palabra en castellano en lo que llega al modelo** (delamor: *"las consignas y todo SÓLO EN INGLÉS… ninguna palabrita perdida en español"*). **Motivo (delamor): CKM aún no es bilingüe.** No es por la "hipótesis de la palabra-semilla" de los REG 0.13–0.14: esa lectura no se usa.
- Auditá **todo lo que recibe el LLM**: system prompt, `GATE_PROMPT_CONTINUO` ya formateado, el historial (incluidos los eventos SYSTEM), el estado del campo que entra al prompt, los fallbacks y cualquier valor que se inserte en el texto.
- Opus ya encontró tres en `autonomous_device.py`: `"(ninguno)"` (l. 449), `"desconocido"` (fallback de `reloj`, l. 453) y el valor `RELOJ_CANAL = "canal"` (`channel.py:39`), que aparece en el prompt como *"clock source: canal"*. Puede haber más.
- Pasalos a inglés, declarados y sin alias.
- **Test:** renderizá el prompt completo en sus variantes (con trigger y sin trigger, con campo y sin campo, con reloj UNKNOWN) y verificá que no tenga palabras en castellano (diacríticos españoles y un listado de palabras funcionales).
- Lo que el modelo no ve (comentarios, docstrings, logs internos) no entra en este paso.

**(0b) El β de cada device no va al device** (delamor: *"lo que NO VA AL DEVICE es β de device"*). `temp_signal` **sí** va: es del canal y queda como está, en el estado y en el prompt. *[Opus había leído mal y pedía sacarlo: se retira.]* Según lo que leyó Opus, el β_i ya no llega: vive en `panel["thermostat"]["beta"]` (`monitor_service.py:376`), y `get_state()` (`ckm_monitor.py`) publica sólo la señal de `temp_signal` y el bloque `coco`, que lleva β_c del corpus y μ_W, no β_i. **Verificalo con un test**: ni el estado que recibe un device ni su prompt contienen β_i (ni el suyo ni el de los otros). No se cambia código salvo que el test lo pida.

**(1) PRIMERO CP3 (delamor) — preparar el vivo, sin correrlo.** Con lo que hay hoy: lo de COCO ya queda en `monitor_trajectory.jsonl` del `state_dir`, y eso alcanza para el objetivo. Los mensajes y la traza de los devices hoy viven en memoria: **declaralo** en el reporte (qué se guarda y qué no con el código de hoy). No agregues lógica en el driver para guardarlos.
- Estado en `experiments/_state_S2-C0/`, limpio.
- Mínimo 2 devices, con filtro de llamadas y su piso.
- Con el ritmo medido del vivo 03, calculá **cuánto tiene que durar el caso para llegar a ~70 mensajes** (≥ 2 rebuilds) y qué `piso_vueltas` cumple `piso_vueltas + 2 ≤ vueltas por device`. Entregá los números con de dónde salen.
- **Consigna** (opción (b): un tema abierto, sin respuesta correcta) y **qué devices / modelos** van: los pone delamor. Dejá el lugar declarado.
- Dejá el comando para correr el vivo. **No lo corras**: lo corre delamor, que está presente.

**(2) Después del vivo: CP2 y fixes. El primer fix es la persistencia en IAP, no en los drivers.** Hoy hay tres cosas que viven sólo en memoria. Que IAP las escriba él mismo en el **mismo `state_dir` privado** donde ya van `corpus_state.json`, `corpus_G_state.json`, `monitor_trajectory.jsonl`, `rebuild_decisions.jsonl` y `rebuild_state.json`:
- los **mensajes del canal**: texto entero, `message_id`, device, tick, timestamp, reloj;
- los **intentos rechazados** (`rejected_attempts`);
- la **traza de decisiones de cada device** (`_decisiones`: tick de observación, tick de acción, resultado, motivo y vía del filtro, `END_OF_CASE`).

Reglas:
- Escritura **append-only, durante la corrida**, no sólo al final: si el proceso se cae, lo escrito queda.
- Nombres en inglés.
- **Sin lógica en los drivers**: el driver sólo pasa el `state_dir`.
- Lo de COCO sigue sin publicarse en el canal: queda en `monitor_trajectory.jsonl`, como hoy.
- Tests: que los tres archivos aparezcan en el `state_dir` pedido, crezcan durante la corrida y sobrevivan a un corte a mitad de camino.
- Los drivers no se revisan ahora: eso va después del vivo.

Al terminar: commits, estado de los tests y avisá para el push.
