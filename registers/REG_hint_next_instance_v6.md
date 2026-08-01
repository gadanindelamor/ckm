#REG_hint_next_instance_v6.md

*Jul 21 2026 — Hint para próxima instancia. Continúa el hilo IAP Chatroom
iniciado en v5 (Casos 0.4→0.5). Este cubre Casos 0.6→0.9.*
*Leer v5 primero si no se tiene el contexto de la serie 0.4/0.5.*

---

## Estado del repo — IMPORTANTE: nada de esto está commiteado

Todo lo de Casos 0.6→0.9 sigue en el working tree, sin commitear. Último
commit real: `a78c3fe` (hint de v5, Casos 0.4→0.5). Si estás leyendo esto
en una sesión/chat nuevo, correr `git status` antes de asumir cualquier
cosa sobre qué existe.

Modificados (no commiteados):
- `iap_chatroom/mcp_server.py` — resource `iap://canal/mensajes` (Caso 0.7)
- `services/monitor_service.py` — fix real de bug (ver abajo)
- `registers/REG_iap_caso_05_v1.md` — actualizado con réplica

Nuevos (untracked):
- `iap_chatroom/test_caso_06.py`, `test_caso_07.py`, `test_caso_07_run2.py`,
  `test_caso_08.py`, `test_caso_09_provider_hetero_join_escalonado_2dev.py`
- `iap_chatroom/TASK_caso_09.md` — task lista para correr desde cero
- `registers/REG_iap_caso_06_v1.md` a `REG_iap_caso_09_v1.md`
- ~20 backups en `process/*caso0[6-9]*` y `process/*caso05_replica1*`
- `process/TASK_caso_09_PREGENERADO.md`,
  `process/test_caso_09_..._PREGENERADO.py` — versión de la task/script
  con el trabajo ya hecho, preservada aparte a pedido de gadanin.delamor
  (para simular el escenario "empezar de cero" en `TASK_caso_09.md`)

---

## Cadena de hallazgos — de "heterogeneidad de modelo" a "heterogeneidad de provider"

**Caso 0.6** (4 devices, join escalonado DELTA_T=5s): Run 1 (early
mixto Haiku+Sonnet) dio actividad; Runs 2/3 (mono-modelo) dieron
silencio. Hipótesis inicial: heterogeneidad → actividad.

**Caso 0.7** (2 devices, join simultáneo, Resource MCP vs tool):
Haiku+Sonnet dio silencio total, replicado 3/3 (incluyendo control sin
resource) — refutando la hipótesis simple. Cruzando con 0.5/0.6 salió
una tabla 2×2 limpia (heterogeneidad × timing de join) sin excepciones
en ese momento.

**Caso 0.8** (2 devices, join escalonado, hetero-modelo — la celda que
faltaba de la tabla): silencio 2/2. La tabla 2×2 se rompió — group size
resultó ser una variable no controlada (0.6 R1 era 4 devices, 0.8 es 2).

**Cadena de réplicas** (pedida explícitamente por gadanin.delamor antes
de seguir cruzando variables — "antes de replicar, ¿qué pasa si 0.5 no
replica? No hay tabla que construir"):
- Réplica de Caso 0.5 (mono-modelo+simultáneo): **replicó** en sentido
  binario (2 textos otra vez), pero con mecanismo social distinto
  (espejos paralelos original vs interacción cruzada en la réplica) —
  ver `REG_iap_caso_05_v1.md`, sección "Réplica 1".
- Réplica de Caso 0.6 Run 1 (hetero-modelo+escalonado, 4 devices):
  primer intento **crasheó** por un bug real en
  `services/monitor_service.py` (ver abajo). Segundo intento, limpio,
  **dio silencio** — 0.6 R1 se reclasifica como varianza de muestreo,
  no celda confirmada.

**Conclusión intermedia:** de toda la serie 0.5-0.8 (9 corridas), el
único patrón de actividad confirmado por réplica era mono-modelo +
join simultáneo (Caso 0.5). Silencio era el resultado dominante.

**Caso 0.9 — cambio de eje, resultado grande:** en vez de variar modelo
dentro de Anthropic, se varió *provider* — Anthropic Sonnet vs Groq
Llama-3.3-70b, mismo diseño que Caso 0.8 (2 devices, join escalonado).
**Actividad 2/2, con volumen y densidad muy por encima de cualquier
corrida previa** (22 y 16 textos AI, vs máximo previo de 8). Contenido
notable en Run 2: Sonnet confrontó explícitamente a Groq por un patrón
de validación sin sustancia, escalando en frontalidad de forma
verificable (conteo explícito "Third time now", auto-etiquetado
"I'll name what I think is happening, plainly", ultimátum con salida
declarada) — y Groq reconoció el patrón y respondió con contraargumento
real. Ver `registers/REG_iap_caso_09_v1.md`.

**Esto es n=2, no confirmado todavía.** Mismo criterio que toda la
serie: no generalizar sin réplica. Pendiente explícito en el REG:
replicar Caso 0.9, probar hetero-provider+simultáneo (separar provider
de timing), probar mono-provider Groq (separar "heterogeneidad de
provider" de "Llama-3.3 es simplemente más hablador").

---

## Bug real corregido — `services/monitor_service.py` línea 93

`self._Delta_r` (acumulador de rechazos, combinado con `W` en
`_combine_W_Delta`) solo se inicializaba una vez. Si `N` (nodos de `W`)
crecía en un rebuild posterior, `_Delta_r` quedaba con el tamaño viejo
para siempre → `ValueError: operands could not be broadcast together`
la próxima vez que `_Delta_r` no era cero y `N` había cambiado.

Fix (1 línea, verificado con repro antes/después, no solo inferencia):
```python
if self._Delta_r is None or self._Delta_r.shape != (N, N):
    self._Delta_r = np.zeros((N, N))
```

**Nota semántica importante:** el reset pone `_Delta_r` en ceros cuando
`N` cambia — si eso pasa a mitad de una corrida futura, `Delta_r_sum`
de esa corrida no es comparable 1:1 con una corrida donde `N` se
mantuvo estable. Verificar si `N` cambió antes de comparar trayectorias
entre corridas.

**Sigue sin commitear.** Verificar que sigue presente
(`grep -n "self._Delta_r.shape" services/monitor_service.py`) antes de
asumirlo en cualquier corrida futura.

---

## Convenciones ya establecidas — no reinventar

- Backup de estado: mover `_state/corpus_state.json` y
  `monitor_trajectory.jsonl` a `process/` con sufijo `.bak_<epoch>_<label>`
  antes de cada corrida (`prepare_state()`, ya en todos los scripts
  `test_caso_0[4-9]*.py`).
- **Gotcha de labeling:** `prepare_state(label=f"caso_run{n}")` como
  paso 1 de cada run archiva los datos del run *anterior* bajo la
  etiqueta del run *actual* — verificar contenido real (`agent_id`s,
  `texts`) antes de confiar en el nombre del archivo.
- Lifecycle del servidor: `run_in_background` + `TaskStop`, no
  `nohup`+`kill` suelto. Esperar `GET /api/monitor` con `200` antes de
  asumir que está listo.
- Si la tarea trae NO MODIFICAR y la solución correcta requiere tocar
  un archivo de esa lista: reportar antes de proceder — aunque
  termines encontrando una solución que no lo requiere (subclassing,
  etc.), el paso de preguntar tiene valor en sí mismo (confirmado
  explícitamente por gadanin.delamor).
- Scripts no modificados para una réplica no soportan labels custom —
  renombrar el backup manualmente después, no editar el script.

---

## Pendientes explícitos para Caso 0.10+

1. Replicar Caso 0.9 (provider heterogeneity) — n=2 no alcanza.
2. Hetero-provider + join simultáneo — separar provider de timing.
3. Mono-provider Groq (2 instancias Llama) — separar "efecto Groq" de
   "efecto heterogeneidad de provider en general".
4. La tabla 2×2×2 completa (modelo/provider × timing × tamaño de grupo)
   sigue con celdas sin correr y ningún cruce con tamaño de grupo
   controlado limpiamente.
5. `TASK_caso_09.md` en `iap_chatroom/` está listo para usarse como
   plantilla de "task completa desde cero" para diseñar Caso 0.10 —
   mismo formato que las tasks de Caso 06-09.

---

## Archivos relacionados

- REG_hint_next_instance_v5.md — hilo previo (Casos 0.4→0.5)
- registers/REG_iap_caso_0[5-9]_v1.md — todos los registros de esta cadena
- iap_chatroom/TASK_caso_09.md — task lista para reusar como plantilla

---

*Jul 21 2026*
