# REG_coco_docstrings_rewrite_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Reescritura de los docstrings de `services/coco.py` a versión orientada
a developer (`TASK_rewrite_coco_docstrings_v1.md` → v2 → v3). Documenta
tres iteraciones con errores reales encontrados y corregidos en cada
paso — el proceso es tan relevante como el resultado: v1 y v2 fueron
escritas sin verificar contra el código real, y ambas contenían
afirmaciones falsas sobre el objeto que describían.

---

## v1 — tres errores de hecho

`TASK_rewrite_coco_docstrings_v1.md` fue escrita antes de que
`track_landscape`, `landscape_history`, `gamma` (alpha compuesto) y el
rename agent→device existieran en `coco.py`. Verificado línea por línea
contra el código antes de ejecutar nada:

1. **`class COCO`** — proponía *"Does not track individual devices or
   their identities."* Falso: `register_device_eval(device_id, fi)`
   guarda por `device_id`, `beta_status()["devices"]` lo expone. (Esta
   afirmación ya existía en el docstring viejo, en español — "No sabe
   quién es cada device" — v1 la iba a traducir, no a corregir.)

2. **`observe()`** — proponía documentar `ThermostatState.temp_signal`
   como campo del return. No existe: los campos reales son `t, D_ckm,
   A_current, A0, frac_rec, stop_applied, alpha_used, zone`.
   `temp_signal` es un método de `COCO`, no un campo del state.

3. **`__init__`** — documentaba 4 parámetros (`W, n_runs=50, seed=42,
   dynamic_alpha=True`) de una firma real que tiene 10: faltaban
   `d_ckm_threshold`, `alpha_star`, `frac_rec_min`, `track_landscape`,
   `landscape_history`, `gamma`. Los 2 que sí aparecían tenían defaults
   incorrectos (`n_runs=50` vs real `80`; `seed=42` vs real `0`).

Además: criterio de éxito con ruta inexistente (`services/test_coco.py`,
real `tests/test_coco.py`) y cifra desactualizada (`43/43`, real
`28/28` — mismo error ya corregido dos veces antes en esta sesión, en
`PAPER_Landscape_Driven_Device_v10_1.md` y `CKM_Informe_Trabajo_v32.md`).
Y cobertura incompleta: `history()`, `status()`, `_classify_zone()`,
`_relax()`, `_count_attractors()` no tenían ningún docstring y v1 no
los mencionaba.

**No se ejecutó v1.** Se reportaron los tres errores y el resto de
hallazgos antes de tocar el archivo.

---

## v2 — corrige todo lo de v1, introduce un error propio

Sonnet reescribió la task incorporando cada hallazgo con precisión —
hasta el detalle de la key `"note"` en `temp_signal()` quedó igual que
como se había encontrado. Agregó criterio editorial explícito ("el
developer que abre coco.py en VSCode, un hover, diez segundos, sin
historia del proyecto, sin teoría"), un Paso 0 obligatorio ("no escribir
ningún docstring desde memoria"), la lista completa de métodos
(públicos y privados) que necesitaban docstring, y un criterio de éxito
correcto (`tests/test_coco.py # 28/28` + chequeo AST en vez de grep).

Un error nuevo: la lista de "Públicos — docstring completo obligatorio"
incluía `landscape_delta()` como si fuera un método de `COCO`. No
existe. Lo que existe es `self._last_landscape_delta` — un atributo de
instancia, expuesto indirectamente vía
`panel["thermostat"]["landscape_delta"]` en `monitor_service.py`
(`getattr(self._thermostat, "_last_landscape_delta", None)`). A
diferencia de `landscape_history()` (método real, envuelve
`self._landscape_history`), no hay accessor propio para el último dict.

**Tampoco se ejecutó v2** — se reportó el error antes de tocar el
archivo.

---

## v3 — resolución y ejecución

Escrita por Claude Code (a pedido explícito: *"armas una TASK v3 con lo
que propones, la dejás en su lugar con las otras, y después la
ejecutás como si la hubiese escrito otra instancia"* — protocolo
deliberado de desacoplar autoría de ejecución, para que la task se
revise con la misma exigencia que si viniera de otro lado).

Resolución del error de v2: documentar la forma del dict de
`landscape_delta` dentro del docstring de `landscape_history()` —donde
el mismo shape aparece repetido en cada entry de la lista, el lugar
real donde un dev lo va a encontrar— en vez de inventar un método
nuevo (violaría "NO modificar: firmas de métodos", restricción que v1
y v2 coinciden en imponer).

Guardada en `iap_chatroom/tests/TASK_rewrite_coco_docstrings_v3.md`,
junto a v1. Ejecutada siguiendo el Paso 0 (re-lectura completa de
`coco.py`, sin copiar nada de v1 ni v2 de memoria).

### Trabajo realizado

- **Corregidos** (errores de hecho de v1): `class COCO`, `__init__`,
  `observe()`.
- **Resuelto lo propio de v3**: `landscape_history()` documenta ahora
  la forma completa de cada entry — cubre lo que v2 le pedía a
  `landscape_delta()`.
- **Nuevos** (sin ningún docstring antes): `history()`, `status()`,
  `_classify_zone()`, `_relax()`, `_count_attractors()` (con nota
  sobre el sesgo de `n_runs` — ver sweep Ago 2026, 60→70), y
  `ThermostatState` (opcional según la task, bajo riesgo por no ser
  método — agregado).
- **Expandidos**: `temp_signal()` (enumera las keys del dict real,
  incluida `"note"`), `delta_state()`, `alpha_trajectory()` (aclara
  que su campo `t` es el índice dentro de la lista, no el `t` de
  `ThermostatState` — son dos cosas distintas, valía la pena dejarlo
  explícito).
- **Sin tocar, confirmados ya correctos**: `beta_c_corpus()`,
  `_alpha_for()`, `_landscape_component()`, `_mean_cS()`.

### Divergencia propia durante la ejecución

Al escribir `__init__`, el primer intento apendizó el nuevo bloque
`Args:` después del párrafo narrativo viejo en vez de reemplazarlo —
quedó duplicada la explicación de `track_landscape`/`landscape_history`/
`gamma` un momento. Detectado al releer antes de seguir con el próximo
método, corregido reemplazando el docstring completo.

### Criterio de éxito

```
tests/test_coco.py: 28/28 passed
```

Chequeo AST (`ast.get_docstring` sobre todo `FunctionDef`/
`AsyncFunctionDef` no-dunder): limpio, salvo `_test_temp_signal`
(línea 624) — función de test en la sección `# Tests TEMP_SIGNAL` al
final del archivo, no un método de `COCO`, nunca estuvo en la lista de
ninguna versión de la task. Fuera de alcance, no tocada.

---

## Estado

- Commiteado: `4c4d03a` ("docs: coco.py docstrings — developer-oriented,
  contra código real (TASK_rewrite_coco_docstrings_v3)"), pusheado.
- El mensaje de commit quedó deliberadamente corto — apunta a este REG
  y a `TASK_rewrite_coco_docstrings_v3.md` para el detalle, en vez de
  reproducir la narrativa completa. Decisión explícita: "¿el mensaje de
  commit es el mensaje que lee quién?" — alguien escaneando `git log`
  necesita qué y por qué, no la novela v1→v2→v3.

---

## Divergencia encontrada al releer este REG

`docs/DOC_coco_drift_docstrings_v1.md` — v1 decía *"Los originales están
archivados en `docs/DOC_coco_drift_docstrings_v1.md` — no se pierden."*
Ese archivo no existe en ningún lado del repo (`find` no lo encuentra).
No es que el archivo de esta sesión lo haya usado sin verificar — es que
la premisa de v1 sobre dónde vivía el respaldo era falsa desde el
origen. No se perdió nada igual: los docstrings viejos siguen enteros en
`git show de4c555:services/coco.py` (el commit inmediato anterior al
`4c4d03a` de esta reescritura) — el respaldo real fue git, no el archivo
que v1 asumía que existía.

---

## Archivos relacionados

- `iap_chatroom/tests/TASK_rewrite_coco_docstrings_v1.md` — versión
  original, no ejecutada, con los tres errores de hecho
- `iap_chatroom/tests/TASK_rewrite_coco_docstrings_v3.md` — versión
  ejecutada
- `services/coco.py` — archivo modificado
- `docs/DOC_coco_drift_docstrings_v1.md` — mencionado por v1 como
  archivo de respaldo; no existe (ver "Divergencia encontrada" arriba)
- `git show de4c555:services/coco.py` — docstrings originales, respaldo real

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
