Repo: gadanindelamor/ckm
Entorno: Codespace ckm (bash/Linux)

Archivo ya existente — NO crear, NO regenerar:
  iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py
Esta TASK cubre solo lo que falta: ejecutar los 2 runs y documentar el
resultado. El diseño, el script y el fix de monitor_service.py (nota al
final) ya están hechos.

TAREA
-----
Caso 0.9 — heterogeneidad de PROVIDER (no de modelo). Misma pregunta
que Caso 0.8, pero cambiando el eje: en vez de dos modelos Anthropic
distintos, dos providers distintos.

Toda la serie 0.5-0.8 varió modelo dentro de un mismo provider
(Anthropic: Haiku vs Sonnet). Caso 0.6 Run 1 (hetero-modelo + join
escalonado, 4 devices) pareció dar actividad en el intento original,
pero la réplica limpia (después de corregir el bug de
`services/monitor_service.py` — desincronización de tamaño entre
`_Delta_r` y `W` al crecer N entre rebuilds) dio silencio total.
Se reclasificó como varianza de muestreo, no celda confirmada. Caso 0.8
(la misma combinación de ejes con 2 devices en vez de 4) también dio
silencio, 2/2.

Caso 0.9 no repite esa celda — cambia el eje modelo→provider,
manteniendo el resto del diseño de Caso 0.8 (2 devices, join
escalonado, DELTA_T=5s, roles invertidos entre runs). Pregunta: ¿la
heterogeneidad de provider (alignment/RLHF distintos, no solo tamaño o
versión del modelo dentro de la misma empresa) produce una dinámica
distinta a la heterogeneidad de modelo intra-Anthropic ya explorada?

PARÁMETROS
----------
DURATION = 90s (early) / DURATION - DELTA_T (late)
POLL_INTERVAL = 2.0s
DELTA_T = 5s
Sin seed_human. SYSTEM_PROMPT_04A (sin explicación CKM).
Ambos devices leen vía tool get_messages — AutonomousDevice base,
sin resource, sin subclase.

DEVICES
-------
ClaudeSonnet_5_1     → AnthropicProvider, model="claude-sonnet-5"
GroqLlama_3-3-70b_2  → GroqProvider, model="llama-3.3-70b-versatile"

RUNS
----
Run 1: early=ClaudeSonnet_5_1,    late=GroqLlama_3-3-70b_2
Run 2: early=GroqLlama_3-3-70b_2, late=ClaudeSonnet_5_1

SECUENCIA POR RUN
-----------------
1. prepare_state(label=f"caso09_run{n}") — backup canónico
2. Detener el servidor si está corriendo. Verificar que
   _state/corpus_state.json y _state/monitor_trajectory.jsonl no
   existen o están vacíos. Reiniciar servidor. Esperar hasta que
   GET /api/monitor responda antes de continuar.
3. Join device early (t=0)
4. Sleep DELTA_T segundos
5. Join device late
6. Ciclo ODA corre DURATION segundos para early,
   DURATION - DELTA_T para late (cierran juntos)
7. Al cierre: loguear Firma_CKM + trajectory + historial canal
8. Comparar explícitamente con la serie previa (0.5-0.8) en el output
9. Preservar corpus_state.json y monitor_trajectory.jsonl con label
   del run antes del siguiente

CRITERIO
--------
Si produce ≥1 texto AI → sería la primera celda hetero+escalonado con
actividad confirmada en una corrida limpia (no crasheada) de toda la
serie 0.6-0.9. La heterogeneidad de provider podría ser la variable
que la heterogeneidad de modelo intra-Anthropic no alcanzaba a ser.

Si produce 0 textos AI → consistente con el patrón dominante de la
serie (silencio en 9/11 corridas previas a esta). La heterogeneidad de
provider tampoco alcanza para romper el silencio del join escalonado
con 2 devices.

Documentar en el output con esa comparación explícita, igual que
Caso 0.8. Devolver corpus_state.json y monitor_trajectory.jsonl crudos
para verificación — no confiar solo en el output de consola.

CRITERIOS DE ÉXITO
------------------
Por run:
- 2 devices join sin error
- Log muestra qué device es early y cuál late, y qué provider usa cada uno
- Firma_CKM o None documentado
- n_textos AI publicados por device
- Resultado comparado explícitamente con las celdas ya corridas (0.5-0.8)
- monitor_trajectory.jsonl preservado con label del run

NO MODIFICAR
------------
autonomous_device.py, channel.py, ckm_monitor.py, server.py, mcp_server.py

Si la única forma correcta pasa por tocar un archivo marcado
NO MODIFICAR → reportar antes de continuar.

Nota: `services/monitor_service.py` tiene un fix real aplicado — línea
93, `self._Delta_r` se redimensiona cuando `N` cambia entre rebuilds de
`W` (antes solo se inicializaba una vez). Ver
`registers/REG_iap_caso_06_v1.md`, sección "Fix del bug", para el
diagnóstico completo. Al momento de escribir esta nota el fix está
aplicado en el working tree pero **sin commitear** (`git status` lo
muestra modificado) — verificar que sigue presente antes de correr, no
asumirlo. No revertirlo. Si un nuevo crash con el mismo patrón de shape
mismatch aparece, reportarlo — no asumir que es el mismo bug ya
corregido sin verificar el traceback.
