# ESTADO_CKMlandscapeConfig_v3

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama de trabajo: `code/trabajo` (§6, opción b).*

---

## Última escritura

**2026-10-08 00:18 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP3 — los demás consumidores, y v1 sale. La TASK queda cerrada.**
Cerrado el 2026-10-08. Base: `079df6c`.
(CP0 en `d66a305`, CP1 en `8391319`, CP2 en `17b6421`.)

## Qué se hizo

Siguiendo el criterio de `DECISIONES_opus.md` (L47), punto por punto:

1. **`tests/test_ckm_landscape_config.py` se fue con V1** — pero **antes** verifiqué la
   cobertura, que era la condición del criterio. De sus 7 tests, **dos no estaban
   cubiertos** y los migré a `test_ckm_landscape_config_ciclos.py`:
   `test_identidades_dos_configs_sobre_la_misma_W` y `test_el_w_version_id_cambia_con_W`.
   El de `theta_W_formula` se fue con la fórmula, por criterio.
2. **Los que usaban V1 como herramienta migraron:** `test_gatekeeper_c1.py` a
   `medido(W)` —sólo necesitaba los μ_W— y `test_rebuild_consulta_w_version.py` a
   `CKMlandscapeConfig.create` + `ciclo_vigente.w_version_id`.
3. **`experiments/replay_sesion_trust.py`** migrado, y **dejó de imprimir θ_W**. Se
   fueron también las constantes `THETA_W_NO_USADO` y `SCALE_NO_USADO`.
4. **`P1P4/run_conteo_vs_masa_04oct/conteo_vs_masa.py` no se tocó.**
5. **`CKMlandscapeConfigV1` borrada.** El módulo baja de 480 a 398 líneas y ya no
   exporta nada de v1. `grep` de `CKMlandscapeConfigV1` en código: cero.
6. **`theta_W_formula` salió**, y la referencia del docstring de `gatekeeper_c1.py` se
   actualizó: ahora **enuncia la pregunta abierta ahí** —la propiedad que la fórmula
   tendría que cumplir— en vez de apuntar a un método que no existe. La pregunta no se
   perdió al borrar el stub.
7. **Entrada al CHANGELOG**, bajo `Unreleased`. Ver P8.

**Suite: 220/220.** Bajan los 9 del archivo borrado y suben los 2 migrados.

## Qué espera, y de quién

- **P8, NO BLOQUEA:** bajo qué versión va la entrada del CHANGELOG. Su última versión
  es **v30 — July 2026** y los informes de trabajo van por **v32**, así que el archivo
  está atrás y no invento un número. Default declarado: `Unreleased`. Ver bandeja.
- **Nada más.** P1–P7 respondidas, sin defaults vigentes sin decisión.

## Próximo paso

**La TASK está cerrada.** No quedan CPs.

Lo que sigue en la fila, ya escrito y fuera de esta TASK:
- `TASK_monitor_coco_ciclo_orbita_v1` — que COCO renazca con el ciclo. Es lo que esta
  TASK dejó explícitamente afuera, y ahora tiene de dónde leer el ciclo.
- `TASK_canal_iap_clock_iniciativa_v1` — el CLOCK, que es de dónde podría venir el
  `t_senal` que hoy queda nulo, y con él la deriva de I6.

## Nada quedó a medias

El CP3 se cerró entero en un solo commit: migraciones, borrado, CHANGELOG, y la suite
completa en verde.
