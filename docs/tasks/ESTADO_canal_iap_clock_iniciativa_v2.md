# ESTADO_canal_iap_clock_iniciativa_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-08 23:06 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP0b — freeze de la serie IAP.** Cerrado el 2026-10-08.
Copia en `process/iap_series_freeze_20261008/` (67 archivos, 620 KB), verificada por `diff`.
**Los originales no se tocaron**: `git status` sobre `iap_chatroom/` y `registers/` da vacío.

Antes: **CP0 — evaluar contra el repo, sin código.** Cerrado el 2026-10-08, commit `8151298`,
aceptado en `2ad873e`.


## Qué espera, y de quién

- **El CLOCK — E3, [delamor]:** dónde vive y de qué reloj se sella cada tiempo. **El CP1 no
  arranca sin esa respuesta.**

## Próximo paso

**CP1 — el CLOCK del canal, sin cambiar a los devices.** Bloqueado por el E3.

`trigger_mode="on_message"` sigue siendo el modo del canal vivo: el freeze lo congeló, pero
sacarlo es el CP1/CP2 y no se tocó.

## Base

`b30dddd`. Suite al arrancar: 284/284.
