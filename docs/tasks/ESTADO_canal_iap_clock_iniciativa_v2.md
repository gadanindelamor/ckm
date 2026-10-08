# ESTADO_canal_iap_clock_iniciativa_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-08 23:06 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP1 — el CLOCK del canal.** Cerrado el 2026-10-08. Suite **304/304**, cinco inversiones.
El canal genera los ticks con su reloj de pared UTC, la Config los registra, y cada tiempo
declara su procedencia. **La inversión 10 no rompía**: nada protegía que el reloj del canal
fuera el que sella los mensajes. Cerrado con dos tests nuevos.

Antes: **CP0b — freeze de la serie IAP.** Cerrado el 2026-10-08.
Copia en `process/iap_series_freeze_20261008/` (67 archivos, 620 KB), verificada por `diff`.
**Los originales no se tocaron**: `git status` sobre `iap_chatroom/` y `registers/` da vacío.

Antes: **CP0 — evaluar contra el repo, sin código.** Cerrado el 2026-10-08, commit `8151298`,
aceptado en `2ad873e`.


## En curso

**CP2a — el ODA continuo, sin criterio local.** Tensiones T1–T6 evaluadas y contestadas
(`982b641`). Si esta línea sigue acá en la próxima sesión, el CP2a se cortó: `git status` dice
qué quedó tocado y la suite si quedó consistente. **No toca Monitor, Config ni COCO.**

## Qué espera, y de quién

- **Nada bloqueante.** El CLOCK quedó decidido (E3, `f07a9dc`) e implementado en el CP1.
- Sin implementar hasta el OK de delamor: **el criterio local sin LLM** y **WAIT** (TASK §1).

## Próximo paso

**CP2 — el ODA continuo.** Lo que trae, y está registrado:
- el ciclo deja de dispararse por mensaje (`trigger_mode` sale del canal vivo);
- **requisito registrado por Opus:** el `since` sale de timestamps del canal, **nunca** de
  `time.time()` del device, con un test que pueda fallar. Hoy sigue saliendo del device;
- el costo se decide ahí: con N=2 y T=60 s, el continuo da 60 a 120 llamadas contra 2 a 20.

## Base

`eb32605`. Suite al arrancar 284/284, al cerrar el CP1 **304/304**.

## Nada quedó a medias

El CP1 se cerró entero. `grep -c INVERSION` sobre `channel.py`, `ckm_landscape_config.py`,
`monitor_service.py` y `ckm_monitor.py` → 0, 0, 0, 0.
Y la diferencia 64/67 del CP0b quedó resuelta con nombre: eran **6** `.pyc` de
`providers/__pycache__/`, borrados; la carpeta quedó en 62 y 62.
