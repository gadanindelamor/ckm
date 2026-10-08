# REG_iap_caso_08_v1.md

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.8 — celda vacía de la tabla de `REG_iap_caso_07_v1.md`: 2
devices, hetero-modelo, join escalonado (DELTA_T=5s). Variable de
control respecto a 0.6 R1 (única corrida hetero+escalonado hasta
ahora): mismo mecanismo de join escalonado y misma heterogeneidad de
modelo, pero con 2 devices en vez de 4 — aísla el tamaño de grupo.

Tabla de referencia previa a esta corrida:

| | join simultáneo | join escalonado (DELTA_T=5s) |
|---|---|---|
| **mono-modelo** | 0.5: actividad (1/1) | 0.6 R2,R3: silencio (2/2) |
| **hetero-modelo** | 0.7: silencio (3/3) | 0.6 R1: actividad (1/1) — **4 devices** |

Ambos devices leen vía tool `get_messages` — `AutonomousDevice` base,
sin resource, sin subclase. `SYSTEM_PROMPT_04A` (sin explicación CKM),
sin seed_human — mismo mecanismo de seed SYSTEM-event de 0.5/0.6/0.7.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_08.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Runs

| Run | early (t=0) | late (t=5s) |
|---|---|---|
| 1 | ClaudeHaiku_4-5-20251001_1 | ClaudeSonnet_5_2 |
| 2 | ClaudeSonnet_5_2 | ClaudeHaiku_4-5-20251001_1 |

Roles invertidos entre runs para controlar orden de modelo — mismo
diseño que 0.6 Run 2 vs Run 3. DURATION=90s (early), DURATION-DELTA_T=85s
(late) — cierran juntos en wall-clock, mismo criterio que 0.6.

**NO MODIFICAR:** `autonomous_device.py`, `channel.py`, `ckm_monitor.py`,
`server.py`, `mcp_server.py` sin cambios — confirmado con
`git status --porcelain` antes de correr (el diff visible en
`mcp_server.py` es el resource de Caso 0.7, preexistente, no tocado en
esta tarea). No hubo situación que requiriera reportar excepción a la
regla — el script reutiliza `AutonomousDevice` sin subclase, igual que
`test_caso_07_run2.py`.

---

## Resultados

| | Run 1 (Haiku early → Sonnet late) | Run 2 (Sonnet early → Haiku late) |
|---|---|---|
| join sin error | ✅ 2/2 | ✅ 2/2 |
| textos AI publicados | 0 | 0 |
| Firma_CKM | None (corpus nunca alcanzó min_texts=3) | None (ídem) |
| n_rejected_pairs (max) | 0 (sin evaluaciones) | 0 (sin evaluaciones) |

**Verificado contra crudo:**
- Run 1 (`process/corpus_state.json.bak_1784670163_caso08_run2`):
  `texts` = `["ClaudeHaiku_4-5-20251001_1 joined the channel",
  "ClaudeSonnet_5_2 joined the channel"]`, `w_version_history` = `[]`.
- Run 2 (`process/corpus_state.json.bak_1784670336_caso08_run2`):
  `texts` = `["ClaudeSonnet_5_2 joined the channel",
  "ClaudeHaiku_4-5-20251001_1 joined the channel"]` (orden invertido,
  consistente con el role-swap), `w_version_history` = `[]`.

Nota de trazabilidad de backups (mismo patrón ya visto en Caso 0.6):
`bak_1784670163_caso08_run2` contiene los datos de **Run 1** (archivado
como preparación de Run 2, por diseño de `prepare_state(label=f"caso08_run{n}")`
como paso 1 de cada run — la label no coincide con el run cuyos datos
archiva).

---

## Log de decisiones (ambos runs, mismo patrón)

```
Run 1: [Haiku] OP_SILENCE → [Sonnet] OP_SILENCE → [Haiku] OP_SILENCE
Run 2: [Sonnet] OP_SILENCE → [Haiku] OP_SILENCE → [Sonnet] OP_SILENCE
```

Silencio total en ambos runs, sin importar qué modelo fue early. Ningún
texto AI publicado en ninguno de los dos.

---

## Hallazgo: el patrón 2×2 no sobrevive al control de tamaño de grupo

**2/2 silencio.** Caso 0.8 (hetero-modelo, escalonado, **2 devices**)
no replica la actividad de 0.6 R1 (hetero-modelo, escalonado, **4
devices**). La tabla limpia propuesta en `REG_iap_caso_07_v1.md` —
"actividad en la diagonal emparejada, silencio en la cruzada" — se
rompe: la celda hetero+escalonado da silencio con 2 devices e
implícitamente actividad solo se había visto con 4.

Tabla actualizada:

| | join simultáneo | join escalonado |
|---|---|---|
| **mono-modelo, 2 dev.** | 0.5: actividad (1/1) | — (no corrido) |
| **mono-modelo, 4 dev.** | — (no corrido) | 0.6 R2,R3: silencio (2/2) |
| **hetero-modelo, 2 dev.** | 0.7: silencio (3/3) | **0.8: silencio (2/2)** |
| **hetero-modelo, 4 dev.** | — (no corrido) | 0.6 R1: actividad (1/1) |

Con el tamaño de grupo puesto en evidencia como variable propia, el
panorama se reordena: **silencio es el resultado dominante** (7 de 9
corridas totales de la sesión, contando 0.5/0.6/0.7/0.8), y los dos
únicos casos de actividad (0.5 y 0.6 R1) son ambos n=1, sin réplica.
En vez de "heterogeneidad × timing" como explicación limpia, la lectura
más honesta ahora es: la actividad es el resultado frágil/infrecuente
en este diseño experimental completo, no el silencio — y ninguna de las
dos corridas con actividad tiene una réplica que confirme que no fue
la muestra puntual la que produjo el resultado.

**Implicación directa:** antes de seguir cruzando variables (modelo,
timing, tamaño de grupo), lo que más falta es **replicar 0.5 y 0.6 R1**
— los dos casos con actividad — para saber si son robustos o si, como
pasó con Caso 0.7 Run 1 (que parecía sólido hasta que Run 1.1 lo
replicó... y en este caso el patrón sí se sostuvo), podrían no
replicar. Sin esas réplicas, cualquier tabla 2×2 o 2×2×2 construida
sobre estos datos descansa sobre dos observaciones no confirmadas.

---

## Pendientes

**Orden de réplica y qué hace cada resultado — explícito antes de
correr, no después:**

1. **Replicar Caso 0.5 primero** (2 devices mono-modelo, join
   simultáneo) — la corrida más simple de las dos, y la que decide más.

   - **Si NO replica actividad:** fin de la búsqueda de tabla. El
     resultado robusto de todo el programa experimental (0.5 → 0.8) es
     silencio, sin condicionar a modelo, timing ni tamaño de grupo. No
     hay 2×2 ni 2×2×2 que construir — ni siquiera hace falta correr la
     réplica de 0.6 R1 para sostener esa conclusión, aunque puede
     correrse igual por completitud. Este REG (y la memoria asociada)
     se cerrarían con esa lectura, no con más celdas pendientes.
   - **Si SÍ replica actividad:** procede a replicar 0.6 Run 1.

2. **Replicar Caso 0.6 Run 1** (4 devices hetero-modelo, join
   escalonado) — solo si 0.5 replicó.

   - **Si NO replica actividad:** el caso mono-modelo+simultáneo (0.5)
     queda como el único patrón de actividad confirmado; hetero+escalonado
     (0.6 R1) se reclasifica como varianza de sampling, no como celda
     real de la tabla. La tabla 2×2 pierde una fila, no se completa.
   - **Si SÍ replica actividad:** ambas corridas de actividad quedan
     confirmadas, y el tamaño de grupo (2 vs 4) queda como la variable
     más probable para explicar por qué 0.8 no replicó el patrón de
     0.6 R1 con 2 devices — recién ahí tiene sentido completar la
     tabla 2×2×2 (celdas sin correr: mono-modelo escalonado con 2
     devices; mono-modelo simultáneo con 4 devices).

---

## Archivos relacionados

- REG_iap_caso_07_v1.md — origen de la tabla 2×2 y la celda que este caso llena
- REG_iap_caso_06_v1.md — origen de la hipótesis de heterogeneidad, ya matizada
- REG_iap_caso_05_v1.md — único caso mono-modelo con actividad, candidato a replicar
- iap_chatroom/test_caso_08.py — script de esta corrida
- process/*caso08* — backups de ambos runs

---

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
