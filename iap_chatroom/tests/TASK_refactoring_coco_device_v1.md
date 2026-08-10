# TASK_refactoring_coco_device_v1.md
*Ago 2026 — gadanin.delamor*

---

## Dos refactorings independientes. Ejecutar en orden.

---

## R1 — coco_thermostat → coco

### Scope

| Qué | Antes | Después |
|---|---|---|
| archivo | `services/coco_thermostat.py` | `services/coco.py` |
| clase principal | `class COCOThermostat:` | `class COCO:` |
| clase estado | `class ThermostatState:` | sin cambio — queda `ThermostatState` |
| imports en otros archivos | `from coco_thermostat import COCOThermostat` | `from coco import COCO` |
| tests | `tests/test_coco_thermostat.py` | `tests/test_coco.py` |
| referencias en .md | `COCOThermostat` | `COCO` |

### Archivos a modificar

```
services/coco_thermostat.py          → renombrar a services/coco.py
                                       cambiar class COCOThermostat → class COCO
services/monitor_service.py          → actualizar import y referencia
services/test_coco_thermostat.py     → renombrar a services/test_coco.py
                                       actualizar import interno
iap_chatroom/ckm_monitor.py          → actualizar import si referencia COCOThermostat
iap_chatroom/autonomous_device.py    → ídem
iap_chatroom/server.py               → ídem
cualquier otro .py que importe COCOThermostat
```

### Reglas

- `ThermostatState` NO se cambia — el nombre es correcto y no incluye Δ.
- `COCO` como nombre de clase refleja su función real: regulador del campo, no termostato.
- Si el archivo ya se llama `coco.py` y la clase ya es `COCO`: verificar y confirmar, no tocar.

### Criterio de éxito

```bash
grep -r "COCOThermostat\|coco_thermostat" services/ iap_chatroom/ tests/ --include="*.py"
# output: vacío o solo en comentarios históricos
python services/test_coco.py  # 43/43
```

---

## R2 — agent → device (en todo el código y docs)

### Regla general

`agent` → `device` en código Python (.py), docstrings, y archivos .md.

### Excepción explícita

NO cambiar cuando `agent` es parte de un nombre compuesto correcto:

```
AgentDeviceSkin         → NO cambiar (es el nombre propio de la clase)
agent_device_skin.py    → NO cambiar (nombre de archivo)
groq_research_agent.py  → NO cambiar (nombre de archivo existente)
AutonomousDevice        → ya está correcto
```

### Patrones a reemplazar (ejemplos, no exhaustivos)

```python
# ANTES
def evaluate(self, text, agent_id=None)
panel["agent_id"]
"register_agent_eval"
self._thermostat.register_agent_eval(agent_id, fi)
beta_status()["agents"]
panel["thermostat"]["beta"]["agents"]

# DESPUÉS
def evaluate(self, text, device_id=None)
panel["device_id"]
"register_device_eval"
self._thermostat.register_device_eval(device_id, fi)
beta_status()["devices"]
panel["thermostat"]["beta"]["devices"]
```

### Archivos a revisar

```
services/monitor_service.py
services/coco.py (post R1)
services/fabrication_service.py
services/corpus_service.py (si aplica)
iap_chatroom/*.py
readme/*.md
registers/REG_*.md  — solo docstrings y texto nuevo, NO modificar REGs históricos
```

### Criterio de éxito

```bash
grep -rn "\bagent\b" services/ iap_chatroom/ --include="*.py" \
  | grep -v "agent_device_skin\|groq_research_agent\|AgentDeviceSkin\|#"
# output: vacío o residual aceptable con comentario explicando por qué quedó
python services/test_coco.py   # 43/43
python iap_chatroom/tests/test_caso_15_behavior_graph.py  # sin errores de import
```

---

## Orden de ejecución

1. R1 primero (rename archivo + clase)
2. R2 segundo (agent → device en todo)
3. Tests después de cada uno
4. Un commit por refactoring, mensaje claro

---

## NO modificar

- `agent_device_skin.py` — nombre de archivo y clase son correctos
- `groq_research_agent.py` — nombre de archivo correcto
- REGs históricos — son registros, no código
- `ThermostatState` — nombre correcto, no cambiar

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
