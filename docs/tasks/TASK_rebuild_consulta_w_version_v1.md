# TASK_rebuild_consulta_w_version_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v4.md, Paso 4 (D7). Precondiciones: TASK_CKMlandscapeConfig_v1 (`450e7ba`), TASK_landscape_config_en_runs_v1 (`6606b7c`), TASK_gatekeeper_C1_theta_W_v1 (`f8d61ef`).*

---

## Qué hacer

Que un servicio pueda saber, por consulta explícita, si W cambió desde la versión con la que opera — y cómo cambió. **Notifica, no resuelve la invalidación**: qué hacer con Δ_r, A0 o la config tras el cambio queda para D2.

## Hallazgo previo (medido)

"Cambio de N" no alcanza como señal. Cada rebuild re-extrae los nodos desde todos los textos; N queda fijo en `top_k` pero los nodos que ocupan esas posiciones cambian. Con `top_k=10`, cuatro rebuilds consecutivos:

```
10 -> 10  mismo conjunto False  mismo orden False   (×4)
```

N no cambió nunca; el conjunto de nodos cambió siempre. `Δ_r[i, j]` pasa a referir a otro par sin señal.

## Acuerdos (delamor)

1. **Dispara cualquier cambio de W**, no solo N. La señal es `w_version_id` (sha256 de W): cambia con cualquier rebuild que cambie W, independientemente de N.
2. **Consulta, no suscripción ni registro de eventos (opción c).** Se formaliza lo que ya existe —`corpus.w_sha()`, `corpus.w_changed_since(sha)`— y se agrega solo lo que falta: que la respuesta incluya `w_version_id` viejo y nuevo, N viejo y nuevo, y `nodes_changed`.
3. **Estado actual registrado para D2.** `MonitorService.evaluate` ya pone Δ_r en ceros cuando cambia el shape (`monitor_service.py:101`, fix del Caso 0.6). No reinicia `_A0`; no actúa si cambian los nodos con N igual. Es una respuesta de hecho, parcial, que nadie decidió como modelo. Esta TASK no la toca.

## Decisión de implementación (Code — a revisar)

`WVersionManager` guarda sha y corpus_size por versión, no nodos. Para calcular `nodes_changed` sin cambiar lo persistido, **quien consulta pasa los nodos con los que opera** junto con su sha:

```python
corpus.w_change_since(sha, nodes) -> {
    "changed"         : bool,
    "w_version_id_old": sha,
    "w_version_id_new": corpus.w_sha(),
    "N_old"           : len(nodes),
    "N_new"           : len(corpus.get_nodes()),
    "nodes_changed"   : nodes != corpus.get_nodes(),   # conjunto u orden
}
```

`w_sha()` y `w_changed_since()` quedan como están.

## Verificación

- Sin rebuild entre consulta y estado: `changed=False`, `nodes_changed=False`, ids iguales.
- Rebuild con N igual y nodos distintos: `changed=True`, `N_old == N_new`, `nodes_changed=True`.
- Rebuild con N distinto: `changed=True`, `N_old != N_new`.
- `w_version_id_new` coincide con `CKMlandscapeConfig.from_W(corpus.get_W(), ...).w_version_id`.
- Tests existentes sin regresión.

## Qué no hace

No invalida ni redimensiona Δ_r. No reinicia A0. No reconstruye CKMlandscapeConfig. No conecta la consulta a Monitor ni a COCO. No toca el reset de L101.

## Abierto (D2)

- Qué hacer con Δ_r cuando cambia W: invalidar, redimensionar, re-mapear por nombre de nodo.
- A0 de Monitor tras cambio de W.
- Config desactualizada tras rebuild dentro del run.
- Si el reset de L101 se mantiene, se amplía a cambio de nodos, o se reemplaza.
