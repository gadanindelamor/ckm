# ESTADO_canal_iap_clock_iniciativa_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-09 00:07 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP2a — el ODA continuo, sin criterio local.** Cerrado el 2026-10-09. Suite **321/321**,
ocho inversiones. `trigger_mode="continuo"` como único modo, una decisión por vuelta, el
silencio no absorbente, LEAVE como decisión, y el `since` del reloj del canal leído antes de
`get_messages`. **La inversión 19 no rompía porque `_observe` pedía el clock y el loop lo
sobreescribía**: código redundante que ningún test podía distinguir. Arreglado en el código.
**Tocó sólo `iap_chatroom/`.**

Antes: **CP1 — el CLOCK del canal.** Cerrado el 2026-10-08. Suite **304/304**, cinco inversiones.
El canal genera los ticks con su reloj de pared UTC, la Config los registra, y cada tiempo
declara su procedencia. **La inversión 10 no rompía**: nada protegía que el reloj del canal
fuera el que sella los mensajes. Cerrado con dos tests nuevos.

Antes: **CP0b — freeze de la serie IAP.** Cerrado el 2026-10-08.
Copia en `process/iap_series_freeze_20261008/` (67 archivos, 620 KB), verificada por `diff`.
**Los originales no se tocaron**: `git status` sobre `iap_chatroom/` y `registers/` da vacío.

Antes: **CP0 — evaluar contra el repo, sin código.** Cerrado el 2026-10-08, commit `8151298`,
aceptado en `2ad873e`.


## Qué espera, y de quién

- **Nada bloqueante.** El CLOCK quedó decidido (E3, `f07a9dc`) e implementado en el CP1.
- Sin implementar hasta el OK de delamor: **el criterio local sin LLM** y **WAIT** (TASK §1).

## Próximo paso

**CP2b — el criterio local encima** (OK de delamor, `e737e78`): `skip` registrado con su motivo,
auditoría **al azar sobre las dos caras**, umbrales declarados "no calibrados", y el test que
pide delamor: en silencio y con objetivo, el filtro **igual** deja pasar a D alguna vez — que el
filtro no vuelva absorbente el silencio.

Los tres requisitos del CP2 quedaron cumplidos en el CP2a: el `since` del canal, el clock
observado en silencio, y `get_messages` probado con el `since` real del device.

**Después:** el CP3 (el caso Z, de delamor) y la corrida viva, que espera las claves. El costo
estimado está reportado y lo decide delamor.

## Base

`eb32605`. Suite al arrancar 284/284, al cerrar el CP1 **304/304**.

## Nada quedó a medias

El CP1 se cerró entero. `grep -c INVERSION` sobre `channel.py`, `ckm_landscape_config.py`,
`monitor_service.py` y `ckm_monitor.py` → 0, 0, 0, 0.
Y la diferencia 64/67 del CP0b quedó resuelta con nombre: eran **6** `.pyc` de
`providers/__pycache__/`, borrados; la carpeta quedó en 62 y 62.
