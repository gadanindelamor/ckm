DELAMOR A CODE (texto de Opus):

Vale lo de siempre: no se toca el vivo hasta que delamor lo corra, sin alias, sin compatibilidad hacia atrás, y la suite cierra en verde.

**Objetivo de S2-C0 CP3, declarado como sesgo** (delamor): terminar con la expresión *"COCO no se conectó nunca a un vivo de IAP"*. Por límites, el objetivo es **que suceda**. Todo lo demás queda como está.

**Orden (delamor): primero CP3, luego CP2 y fixes.** Lo del CP2 ya está cubierto por tests y por la medición del 19 oct (COCO conectado y evaluando, primer W a los 30, ODA con canal en silencio, corte al fin del caso); se retoma después del vivo.

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
