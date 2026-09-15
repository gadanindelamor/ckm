# TASK_CKMlandscapeConfig_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet + Claude Code (Opus 5)*

*Contexto: leer DEFS_CKM_estado_actual_v11.md §0 Modelo Conceptual y PROPUESTA_ckm_landscape_dynamics_v4.md §10 antes de comenzar.*

---

## Qué hacer

Crear `CKMlandscapeConfig` como clase independiente en `services/`. No hereda de `CKMConfig`. No modifica código existente.

## Qué debe portar

- `N` — número de nodos del corpus actual.
- `mu_W_nonzero` — media de W sobre pares no nulos, medida desde la W del corpus.
- `mu_W_global` — media de W con ceros, medida desde la W del corpus.
  La config porta los dos con nombre explícito. **Cada consumidor declara cuál usa.** La config no elige: hace visible la elección.
- `theta_W` — **parámetro obligatorio, sin default**, hasta que se decida la fórmula. La fórmula queda como `NotImplementedError`, con un docstring que describe la propiedad requerida: al menos el núcleo A pasa C1.
- `w_version_id` — `sha256(W)`, vía `w_version.py` (ya existe). Identifica a W: la misma W da el mismo id.
- `config_id` + `timestamp` — identifican a la instancia de config. Distintos en cada instanciación.
- `sampling_mode`, `beta_c`.
- `scale` — escala del umbral de D_masa_cuencas: lineal o log. **Parámetro declarado, sin default**, hasta que se cierre esa decisión (abierta en PROPUESTA v4).

`w_version_id` y `config_id` son dos objetos distintos: uno identifica a W, el otro a la instancia de config.

## Qué no hace

No lee de archivo (el test carga el JSON y le pasa W). No tiene valores default heredados de CKMConfig. No asume N fijo.

## Verificación

Dado `W_ckm_corpus_v2.json`:

- `mu_W_nonzero` ≈ 0.005977 y `mu_W_global` ≈ 0.004519.
- `theta_W`: construir sin `theta_W` falla. El criterio de corrección de la fórmula —al menos el núcleo A pasa C1— se verifica cuando la fórmula exista; no en esta TASK.
- `scale`: construir sin `scale` falla.
- Serializable a JSON y recargable produciendo los mismos valores.
- `w_version_id` igual en dos instanciaciones sobre la misma W.
- `config_id` distinto en dos instanciaciones consecutivas.

## Deuda técnica que NO toca esta TASK

D6, D1, D7 vienen después. Esta TASK no conecta CKMlandscapeConfig a ningún servicio existente — solo la crea y verifica que existe y serializa.

## Abierto

- Fórmula de `theta_W`.
- `beta_c` depende de μ_W, y hoy `COCO.beta_c_corpus()` usa `mu_W_global` (β_c = 13.83). Con `mu_W_nonzero` daría ≈ 10.46. Qué μ_W usa `beta_c` en la config: a declarar.
