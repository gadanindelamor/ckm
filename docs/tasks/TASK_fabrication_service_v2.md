# TASK_fabrication_service_v2 — reescribir FabricationService y sus tests desde cero

*10 oct 2026 — confirmado por delamor. Redacta Opus (Cowork); ejecuta Code.*

## Por qué

El único FabricationService que existe es `experiments/fabrication_service_dev.py` (`df44aec`, 1 jun): *"Reconstrucción desde snippets … [INFERRED] reconstruido desde REG"*, con umbrales inferidos (c_S 0.003, T 0.05, A0 5) y el fi saturado sin corregir (REG_monitor_ckm_v1). No está en `services/`. Lo que sí está en uso es `MonitorService._fabrication_index` (`monitor_service.py:668`): **fracción de nodos que el texto declara activos y que la relajación rechaza**, que COCO consume (`coco.py:398`).

## Qué se hace

1. **`services/fabrication_service.py` nuevo, desde cero**, con lo que hoy se usa y nada más: el fabrication index (σ_prompt, σ_relajado) → valor, con su borde declarado (0 declarados → hoy devuelve 0.0; **delamor, 10 oct: respeta las reglas del resto de los módulos → UNKNOWN**, no un valor de la escala).
2. **Monitor delega en el servicio** y sigue dando el mismo número: test de regresión que compara, sobre trazas preservadas, el valor de antes y el de después (deben ser idénticos).
3. **Tests propios** del servicio: casos de respuesta conocida (ninguno rechazado → 0; todos → 1; mixto → fracción), el borde de 0 declarados, y entradas de forma inválida.
4. **`experiments/fabrication_service_dev.py` queda como traza**, sin tocar (no se renombra ni se borra).

## Lo que no entra ahora

Detección más allá del índice (señales de control, cuadrantes, Δ declarado vs acumulado): se analiza después, con delamor, sobre lo que el servicio reescrito muestre.

## Una pregunta para el registro

El paper (§6.3, §6.4) dice que FabricationService se disparó en el Caso 0.11. Antes de cambiar ese texto, que el REPORTE diga **qué código** corrió en 0.11 (¿el fabrication index de Monitor, el `_dev`, otro?).

## Reglas

No se toca el gate. No se renombra nada. Archivos nombrados al commitear. Un REPORTE por CP: CP1 servicio + tests propios; CP2 delegación + regresión.

## Recursos (criterio de delamor, 10 oct)

Cada test se verifica con los recursos al alcance del proyecto (local, Codespace, Groq). Lo que necesite un recurso fuera de alcance se implementa igual y queda **declarado** en el REPORTE con el recurso que falta; no se verifica hasta tenerlo.
