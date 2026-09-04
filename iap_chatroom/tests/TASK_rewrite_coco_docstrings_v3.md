# TASK_rewrite_coco_docstrings_v3.md
*Ago 2026 — gadanin.delamor + Claude Code*
*v3 — corrige un error de v2: `landscape_delta()` no existe como método.*

---

## Por qué v3

v2 corrigió todos los errores de hecho de v1 (class COCO "no trackea
devices", `observe()` con campo `.temp_signal` inexistente, `__init__`
con firma de 4 parámetros en vez de 10) y quedó bien especificada en casi
todo. Pero en la lista de "Públicos — docstring completo obligatorio"
incluyó `landscape_delta()` como si fuera un método de `COCO`.

No existe. Lo que existe es `self._last_landscape_delta` — un **atributo**
de instancia, no un método público. Se expone indirectamente vía
`panel["thermostat"]["landscape_delta"]` en `monitor_service.py`
(`getattr(self._thermostat, "_last_landscape_delta", None)`). A diferencia
de `landscape_history()`, que sí es un método real y envuelve
`self._landscape_history`, no hay accessor propio para el último dict.

No hay que inventar un método nuevo para darle docstring — violaría
"NO modificar: firmas de métodos" (v2 y v1 coinciden en esa restricción).
La resolución: documentar la forma de ese dict dentro del docstring de
`landscape_history()`, que es donde el mismo shape aparece repetido en
cada entry de la lista — el lugar real donde un dev lo va a encontrar.

Todo lo demás de v2 queda igual.

---

## Criterio editorial — quién lee esto

El developer que abre `coco.py` en VSCode. Un hover. Diez segundos.
Sabe qué hace, qué recibe, qué devuelve. Sigue trabajando.

Sin historia del proyecto. Sin teoría. Sin justificaciones.

---

## Paso 0 — obligatorio antes de escribir

```bash
cat services/coco.py
```

Leer completo. Verificar:
- Firma real de `__init__` (todos los parámetros y defaults)
- Campos reales de `ThermostatState`
- Qué devuelve cada método público
- Qué hacen `history()`, `status()`, `_classify_zone()`, `_relax()`, `_count_attractors()`
- Forma real del dict en `self._last_landscape_delta` (para documentarlo
  dentro de `landscape_history()`, no en un método aparte)

No escribir ningún docstring desde memoria, desde v1, ni desde v2.

---

## Métodos que necesitan docstring (completo)

### Públicos — docstring completo obligatorio

```
__init__            — todos los parámetros con tipo y default real
observe()           — inputs, returns, side effects
beta_c_corpus()      — qué calcula, qué devuelve
temp_signal()        — keys del dict real (incluye "note" si existe)
delta_state()        — cuándo llamarlo, qué devuelve
landscape_history()  — qué contiene la lista, cuándo está vacía, Y la
                        forma de cada entry (A_antes, A_despues, delta_A,
                        cS_antes, cS_despues, delta_cS, alpha_used,
                        D_ckm_at_stop) — cubre lo que v2 le pedía a
                        landscape_delta(), que no existe como método
alpha_trajectory()   — qué contiene cada entry del dict
history()            — qué es esto (leer código antes de escribir)
status()             — qué devuelve (leer código antes de escribir)
```

### Privados — docstring mínimo (una línea + inputs/outputs si no son obvios)

```
_alpha_for()            — ya tiene buen docstring en v1, verificar que sigue vigente
_landscape_component()  — ya tiene docstring completo (agregado en TASK_coco_alpha_compuesto_v3) — verificar que sigue vigente, no reescribir si ya cumple el criterio editorial
_classify_zone()        — criterios de zona (leer código)
_relax()                — qué hace (Hopfield step, leer código)
_count_attractors()     — qué cuenta, nota sobre sesgo n_runs
```

---

## Lo que se sabe que está bien en v1/v2 (verificar antes de copiar)

- `beta_c_corpus()` — coincide con código real
- `_alpha_for()` — coincide con código real
- `temp_signal()` — casi correcto, verificar si existe key "note" en el dict real
- `_landscape_component()` y `_mean_cS()` ya tienen docstrings completos
  agregados en tasks posteriores a v1 — probablemente no necesitan reescritura,
  solo confirmación de que cumplen el criterio editorial

## Lo que se sabe que está MAL (no copiar)

De v1:
- `class COCO` — COCO sí trackea devices vía `register_device_eval`
- `observe()` — `ThermostatState` no tiene campo `.temp_signal`
- `__init__` — firma incompleta y defaults incorrectos

De v2:
- `landscape_delta()` no existe como método — ver sección "Por qué v3"

---

## Criterio de éxito

```bash
python tests/test_coco.py   # 28/28

# Verificar que todos los métodos tienen docstring:
python3 -c "
import ast, sys
with open('services/coco.py') as f:
    tree = ast.parse(f.read())
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if not node.name.startswith('__') or node.name == '__init__':
            if not (ast.get_docstring(node)):
                print(f'SIN DOCSTRING: {node.name} (línea {node.lineno})')
"
# output esperado: vacío — todos los métodos de la lista de arriba
# quedan cubiertos, no debería sobrar nada
```

---

## NO modificar

- Lógica de ningún método
- Firmas de métodos — los parámetros son los que son
- Constantes del módulo
- `ThermostatState` — si no tiene docstring, agregar solo si el código
  lo permite sin riesgo
- `agent_device_skin.py`, `groq_research_agent.py`
- REGs históricos
- No inventar métodos nuevos (p. ej. `landscape_delta()`) para poder
  darles docstring

---

## Archivos a modificar

```
services/coco.py   — solo docstrings
```

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
