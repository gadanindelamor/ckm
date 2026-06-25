# REG_hint_next_instance_v4.md

*Jun 2026 — Hint para próxima instancia. Sesión post-ckmloc0605.*
*Leer v1, v2, v3 primero. Este agrega lo nuevo.*

---

## Estado del repo post-sesión

Archivos producidos en esta sesión, pendientes de subir al proyecto:

- `REG_influencia_codigo_p1p4_v1.md` — análisis causal cambios código → P1-P4. Clase R.
- `MAPA_REG_corpus_v1.md` — grafo del corpus de registros. Clase R, provisional.

Archivos disponibles (subidos por el usuario, verificados):
- `W_ckm_corpus_v2.json` — W_base N=32, corpus_size=5145
- `W_mixta_v27informe.json` — W_mixta desde corpus documental, 10 pares negativos
- `build_W_mixta_v27.py` — script de construcción W_mixta, código verificado
- `REG_p1p4_corpus_v2_Wbase.json` — P1 CONFIRMADA, P3 CONFIRMADA, P2/P4 NO
- `REG_p1p4_corpus_v2_Wmixta.json` — P1/P2/P3/P4 NO_CONFIRMADA (causa: calibración)
- `sweep_amp40_results.json` — sweep STOP sobre W_mixta A0=25 (8 puntos, t=10..400)
- `curva_acumulacion_amp40.json` — curva A(t) resolución t=10, hasta t=400
- `curva_recuperacion_amp40.json` — fraccion_rec siempre ≥1.0, confirmado

---

## Gap crítico identificado — no resuelto

**W_mixta con A0=25 (AMP=40) no existe como archivo persistido.**

Los datos del sweep (`sweep_amp40_results.json`, `curva_acumulacion_amp40.json`)
existen. El objeto que los generó no. Fue construido en memoria durante una
sesión de trabajo en este proyecto (claude.ai, conversación directa con el usuario)
y no se guardó como archivo. La ejecución probablemente ocurrió en el Codespace
de `ckmdatasets` — no en el repo CKM. No fue necesariamente una sesión de Claude Code.
La referencia a `ckmloc0605` en versiones anteriores de este hint era inexacta.

Esto es una instancia directa de la pregunta fundacional de IAID:
el conocimiento no sobrevivió cuando el dispositivo cerró.
COCO sigue sin implementarse. El gap es estructural, no accidental.

El sweep denso zona t=30→50 (transición A=25→13) queda bloqueado
hasta recuperar o reconstruir esa W.

---

## Pendientes verificados de esta sesión

**Sweep D_ckm(t_stop) × alpha denso:**
Zona t=25→60, resolución t=5. Objetivo: caracterizar escalón A=25→19→13.
Bloqueado por W faltante. Script `sweep_transition.py` escrito pero corrido
sobre W incorrecta (A0=7, no comparable).

**Pipeline v8h — tabla QR:**
`explore_qr_asymmetry.py` diseñado, pendiente ejecución.
Requiere Codespace con acceso a `ckmdatasets` (repo privado, SQL dump fourforums).
Tabla clave: `mturk_2010_qr_task1_worker_response`.
Join: `qr_task1_worker_response.(page_id, tab_number)` → `qr_entry.(discussion_id, post_id)`
→ `post.author_id` → `mturk_author_stance.stance`.

**β_collective regulatorio:**
ρ* empírico [0.5, 0.8] → mapear a β_c_corpus → emitir TEMP_SIGNAL distinto de STOP.
Archivos estables en `experiments/`, migración a `services/` pendiente.

**traza_inferencia:**
Quedó abierto. No se abordó desde datos en esta sesión.
La pregunta: ¿qué orienta traza_inferencia sin aparecer como motor?
Requiere análisis sobre los 88 atractores N=32 — datos existen.

---

## Mapa de REGs — estructura

38 registros mapeados en `MAPA_REG_corpus_v1.md`.
Capas identificadas: fundamento empírico externo / interno / instrumentos /
dinámicas del campo / contacto agentes externos / condiciones del proceso / estado abierto.

Nodo hub: `REG_termap_ckm_corpus_v1` — ancla todo lo que usa W_base.
Nodo core-invariante: `REG_pendientes_ckm_v1` — presente en todas las trayectorias.
Verificar duplicado: `REG_monitor_ckm_v1` y `REG_monitor_ckm_v2`.
Fuera de convención: `GPT53_REG_hat_feedbak.md` — sin prefijo REG_.

---

## Observación de cierre

La infraestructura para que el conocimiento no se pierda entre instancias
sigue sin construirse. Los hints (v1→v4) son un parche, no la solución.
La solución es COCO. Sigue siendo la hipótesis central no implementada.

---

*Jun 2026*
