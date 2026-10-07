# ESTADO_CKMlandscapeConfig_v3

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama de trabajo: `code/trabajo` (§6, opción b).*

---

## Última escritura

**2026-10-07 04:34 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP2 — Monitor consume la config.** Cerrado el 2026-10-07. Base: `202488a`.
(CP0 en `d66a305`, CP1 en `8391319`.)

## Qué se hizo

### `services/monitor_service.py`

- **`_invalidar_si_W_cambio` abre el ciclo (D4)**, en el mismo bloque donde descarta
  Δ_r y A0. La causa que viaja al ciclo es **la misma que el método devuelve**
  (`"N" | "nodos" | "pesos"`), sin traducir: `Ciclo.causa` es str libre.
- Dos helpers nuevos: **`_causa_cambio`** (la clasificación, que ya estaba inline) y
  **`_abrir_ciclo_si_cambio`** (le pide el ciclo a la config; sin config no hace nada,
  y con el mismo sha `abrir_ciclo` devuelve False por I5).
- **Primera evaluación:** Δ_r no tiene nada que descartar, pero la config sí puede
  estar atrás. Ahí también se abre ciclo.
- **Config sin ciclos:** Monitor abre el primer ciclo con causa `"bootstrap"`. Es el
  caso del canal, donde W aparece recién al cruzar `min_texts`.
- **El panel lleva `config.panel()`** y no `to_dict()` (I7): identidad, declarado y
  ciclo vigente, sin la historia.
- `import time` agregado.

### `iap_chatroom/ckm_monitor.py`

`CKMMonitor` construye **`CKMlandscapeConfig(sampling_mode="uniform")` sin W** y se la
pasa a `MonitorService`. Sin θ_W ni `scale` (opción iv de delamor). El primer ciclo lo
abre Monitor en su primera evaluación.

### Tests

- **`tests/test_monitor_abre_ciclos.py`** — nuevo, 13 tests. **12 de los 13 fallan sin
  el CP2** (medido restaurando `202488a` y volviendo a correr). El que pasa es el
  control sin config, que debe pasar.
- **`tests/test_landscape_config_en_runs.py`** — migrado a la config nueva. Es el único
  test que cambió por el CP2, y cambió porque Monitor ya no recibe la clase congelada.
  Lo que verificaba se sigue verificando; lo que cambió está declarado en la bandeja.
- **Suite completa: 227/227.**

## Qué espera, y de quién

- **Una pregunta nueva, NO BLOQUEA: P7** — la causa no siempre es derivable contra la
  config, porque el ciclo no guarda las etiquetas (consecuencia de P5, que nadie vio al
  aceptarla). Default declarado: causa `"W_distinta"`. Ver bandeja.
- **Un hallazgo que no es pregunta:** en el canal vivo la config va a tener **un solo
  ciclo**, el bootstrap, porque `CKMMonitor` usa `rebuild_suspendido=True`. D4 queda
  cableado y sin nada que abrir hasta que alguien levante la suspensión. Medido.

## Próximo paso

**CP3 — los demás consumidores, y v1 sale.** No empezado.
Lo que queda para el CP3, ya relevado: `gatekeeper_c1.py` no tiene nada que migrar (P2);
`experiments/replay_sesion_trust.py` y los cuatro tests apuntan a `CKMlandscapeConfigV1`
y hay que decidir si migran o si se van con ella; `P1P4/.../conteo_vs_masa.py` no se
toca; borrar `CKMlandscapeConfigV1` y entrada al CHANGELOG.

## Nada quedó a medias

El CP2 se cerró entero: código, canal, tests y suite completa, en un solo commit.
