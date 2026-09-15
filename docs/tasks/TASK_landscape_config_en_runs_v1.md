# TASK_landscape_config_en_runs_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v4.md, Paso 2 (D6). Precondición: TASK_CKMlandscapeConfig_v1 (ejecutada, `450e7ba`).*

---

## Qué hacer

Cada panel y cada línea JSONL de MonitorService lleva la `CKMlandscapeConfig` serializada que lo produjo.

## Decisiones (delamor)

1. **Monitor recibe la config ya construida.** Parámetro opcional del constructor. Quien arma el run declara los valores; Monitor no decide calibración.
2. **Rebuild no entra.** La config se construye una vez por run. Si W cambia dentro del run, `w_version_id` queda desactualizado — gap conocido de D7, registrado, no se toca acá.
3. **Verificación = recargar la config.** De cada línea del JSONL se recarga una `CKMlandscapeConfig` igual a la que produjo ese panel. Reproducir el run queda **abierto** (la config porta sha de W, no W; tampoco n_runs, count_seed ni textos).
4. **La config es la del contador de Monitor.** COCO tendrá la suya cuando se conecte; no se colapsan.
5. **Clave nueva `landscape_config`.** No se toca ninguna clave existente. Paneles históricos no la tienen.

## Comportamiento

- Sin config: `panel["landscape_config"] = None`. Los usos actuales no cambian.
- Con config: `panel["landscape_config"] = config.to_dict()`.
- `config.sampling_mode` distinto del `sampling_mode` de Monitor: falla en construcción (ValueError), mismo criterio que la validación de `scale`.

## Verificación

- Monitor sin config: panel y JSONL con `landscape_config` = None.
- Monitor con config: cada línea del JSONL recarga con `CKMlandscapeConfig.from_dict` una config igual a la pasada.
- Tests existentes de MonitorService sin regresión.

## Abierto

- Reproducir un run desde su propio JSON.
- Config de COCO.
- D7: config desactualizada tras rebuild dentro del run.
