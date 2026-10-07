# ESTADO_CKMlandscapeConfig_v3

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama de trabajo: `code/trabajo` (§6, opción b).*

---

## Última escritura

**2026-10-07 04:09 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP1 — la clase nueva.** Cerrado el 2026-10-07. Base: `21ba45c`.
(CP0 cerrado antes, en `d66a305`.)

## Qué se hizo

### Código

`services/ckm_landscape_config.py` — 480 líneas. Tres cosas nuevas y una congelada:

- **`medido(W)`** — función de W sola (I5). `nodes` **queda afuera**: las etiquetas
  no son función de W y meterlas rompería I5. Declarado en el docstring y en la bandeja.
- **`Ciclo`** — `dataclass(frozen=True)` con `w_version_id`, lo medido, `causa`,
  `t_senal`, `t_rebuild`, y `deriva` como property (nula, no cero, sin señal).
  Valida `t_senal <= t_rebuild` en `__post_init__` (I6).
- **`CKMlandscapeConfig`** — identidad + declarado + tupla de ciclos, con
  `threading.RLock`. `ciclo_vigente`, `panel()` y `abrir_ciclo` leen y reemplazan
  **bajo el mismo lock** (D3). `abrir_ciclo` es síncrono (D2) y el reemplazo es un
  solo cambio de referencia de la tupla (I1). **Sin `theta_W`** (delamor, 7 oct).
  `scale` opcional, `sampling_mode` obligatorio (I4 revisada).
- **`ciclo_desde_registro_plano_v1`** — el mapeo de lectura de P4. No reescribe nada.
- **`CKMlandscapeConfigV1`** — la clase vieja, renombrada y sin tocar. Conserva
  `theta_W` y `theta_W_formula` porque es traza de los runs corridos. Sale en el CP3.

### Tests

`tests/test_ckm_landscape_config_ciclos.py` — 355 líneas, **31 tests, 31 en verde**:
I1 (×3), I2 (×3), I3, I4 (×5, incluido que `theta_W` ya no es campo), I5 (×3),
I6 (×4), I7 (×2), D2, **D3 (×2, con hilos, pueden fallar)**, valores medidos (×3),
serialización con historia (×2), lectura de la traza vieja (×2, uno sobre el JSONL real).

**Suite completa: 214/214 en verde.**

## Lo que cambié fuera de la clase, y por qué

El rename hizo que `CKMlandscapeConfig` apunte a la clase nueva, que no tiene `from_W`.
Rompió 15 tests. **Redirigí a `CKMlandscapeConfigV1`** los cuatro archivos de test y
`experiments/replay_sesion_trust.py` — una línea de import y los usos, nada de lógica.
**Sin shim de compatibilidad** en la clase nueva (chau regresión).

`services/monitor_service.py` **no se tocó y no se rompió**: usa sólo `.sampling_mode`
y `.to_dict()`, que la clase nueva tiene. Verificado corriendo
`test_monitor_services.py` (36/36).

## Qué espera, y de quién

- **P3 ya está contestada** por delamor (θ_W sale de la config; el canal construye la
  Config con medido + ciclos + `sampling_mode`). El CP2 **ya no está bloqueado**.
- **Dos preguntas nuevas, las dos NO BLOQUEA**, con default declarado y reversible:
  **P5** (`nodes` afuera de lo medido) y **P6** (`t_senal` sin tilde). Ver bandeja.
- **Un aviso, no pregunta:** `P1P4/run_conteo_vs_masa_04oct/conteo_vs_masa.py` usa
  `from_W` y **se rompería si se volviera a correr**. No se tocó, como manda la TASK.

## Próximo paso

**CP2 — Monitor consume la config.** No empezado. Habilitado.

## Nada quedó a medias

El CP1 se cerró entero: clase, tests y suite completa en verde, en un solo commit.
