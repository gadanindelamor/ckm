# TASK_invalidacion_delta_r_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v4.md, D2. Precondición: TASK_rebuild_consulta_w_version_v1 (`5b52992`).*

---

## Qué hacer

MonitorService invalida Δ_r y A0 cuando W se reconstruye, usando la consulta de D7.

## Las tres condiciones que D2 cubre

1. **N cambia** — shape de Δ_r incompatible. Hoy manejado parcialmente (`monitor_service.py:101`).
2. **N igual, conjunto de nodos cambia** — shape correcto, los índices apuntan a otros pares. No manejado.
3. **N igual, conjunto igual, orden cambia** — mismo problema que 2, más silencioso.

## Acuerdos (delamor)

1. **Reset en cualquier reconstrucción de W.** No solo en las tres condiciones: los índices pueden ser los mismos, pero los pesos que produjeron esa Δ_r ya no son los vigentes. La señal es `w_version_id`.
2. **A0 se resetea junto con Δ_r.** Comparar D_ckm contra un baseline de otro campo es lo que D2 corrige. Van juntos.
3. **COCO fuera de alcance.** `COCO.observe` suma la W de su construcción con la Δ_r de Monitor; si N cambió, los shapes no coinciden. Es real y preexistente. D2 no lo toca.
4. **Traza en el panel.** Clave nueva `Delta_r_reset`: `None` si no hubo reset; la causa si la hubo (`"N"`, `"nodos"`, `"pesos"`).

## Verificación

- Sin rebuild entre evaluaciones: Δ_r acumula, A0 se conserva, `Delta_r_reset` = None.
- Rebuild con N distinto: Δ_r en ceros con el shape nuevo, A0 recalculado, causa `"N"`.
- Rebuild con N igual y nodos distintos: reset, causa `"nodos"`.
- Rebuild con mismos nodos y pesos distintos: reset, causa `"pesos"`.
- Tests existentes sin regresión.

## Abierto

- **Δ_r no acumula si los nodos cambian en cada rebuild.** En la medición de D7 (corpus chico: 7–9 textos cortos, `top_k=10`) los nodos cambiaron en 4 de 4 rebuilds. Si eso ocurre en operación, Δ_r se resetea casi en cada mensaje, D_ckm queda cerca de 0 y COCO no llega a comprimir. No medido en corpus grande.
- **`min_texts` como criterio de rebuild** *(contexto, no decisión)*: con `min_texts` suficientemente alto, el top_k de nodos se estabiliza antes del primer rebuild. Con nodos estables, los rebuilds siguientes cambian pesos pero no índices — y Δ_r puede acumular. Es la condición que faltaba para que D_ckm tenga campo donde operar. Ahora es formulable porque existe la señal de cambio de W.
- COCO: shape mismatch con W vieja (acuerdo 3).
- Config desactualizada tras rebuild dentro del run.
