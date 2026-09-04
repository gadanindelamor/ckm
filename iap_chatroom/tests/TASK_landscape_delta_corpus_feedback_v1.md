# TASK_landscape_delta_corpus_feedback_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Objetivo

Cerrar el circuito O₂→W: el `landscape_delta` acumulado por COCO durante
la fase de evaluación debe poder informar la siguiente fase de acumulación.

Actualmente `landscape_delta` existe en el panel pero nadie lo usa.
El rebuild de W no tiene acceso a él. Esta tarea conecta los dos.

---

## Contexto

COCO ya expone (post Extensión 2):
- `panel["thermostat"]["landscape_delta"]` por evaluación
- `coco.alpha_trajectory()` — lista de `{t, alpha, D_ckm, delta_A}`

El corpus ya tiene dos fases: acumulación → evaluación.
El rebuild de W ocurre cuando CorpusService decide reconstruir.

La pregunta de diseño: ¿qué del `landscape_delta` debería influir en
qué textos entran en la siguiente acumulación, o en el peso que se les
da al entrar?

---

## Lo que pedimos

**Leer primero:**
- `services/coco.py` — `landscape_delta()`, `alpha_trajectory()`
- `services/corpus_service.py` — cómo funciona `ingest()`, `rebuild_W()`,
  y si ya existe algún mecanismo de peso o selección en la acumulación
- `services/monitor_service.py` — cómo se almacena la trayectoria

**Luego proponer:**

Un diseño mínimo que permita que, al momento del rebuild de W,
CorpusService tenga acceso al historial de `landscape_delta` acumulado
en la fase de evaluación.

No implementar aún — proponer la interfaz: qué método en qué servicio,
qué pasa qué a quién, sin tocar lógica existente.

Si la arquitectura actual ya permite esto con un cambio pequeño, mostrarlo.
Si requiere un servicio nuevo o una capa de coordinación, nombrarlo.

---

## Criterio de éxito del análisis

Un texto de no más de media página describiendo:
1. Dónde vive actualmente `landscape_delta` acumulado (si vive en algún lado)
2. Qué necesita CorpusService para recibirlo en `rebuild_W()`
3. El cambio mínimo de interfaz que lo haría posible

No código completo — decisión de diseño primero.

---

## NO modificar

Nada todavía. Solo lectura y propuesta.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
