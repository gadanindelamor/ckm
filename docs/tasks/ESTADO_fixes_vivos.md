# ESTADO_fixes_vivos

*Estado vivo de la TASK de fixes medidos en los vivos 01 y 02.*
*Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3. Rama única: `main`.*

---

## Última escritura

**2026-10-09 04:51 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**Los cinco fixes, más la firma.** Aceptados en DECISIONES `7175468`.
**`n_agentes` obligatorio en `firmar()`** (Opus): implementado y reportado.
Suite: **379 passed**.
La evaluación previa quedó cerrada en `bc6729e`, aceptada en `e3d651c`.

## En curso

**Nada.** Los seis cambios están en el árbol y en la suite:

| | Estado |
|---|---|
| F1 | Era mi error de reporte, no un bug del canal (`/api/monitor`, no `/api/monitor/state`). Quedan los tests del endpoint y del router. |
| F2 | `clock_log_desde()` aditivo; `clock_log()` sin cambiar. Tool y dos rutas. |
| F3a | `state_dir` parametrizable, default `_STATE_DIR`. |
| F3b | SYSTEM **no entra al corpus**. |
| F4 | `"system"` no cuenta como agente. |
| F5 | `ritmo_observado()` junto al declarado en `costo()`. |
| firma | Los dos `1` afuera: `n_agentes` es el conteo real. |
| firma (2) | **Sin default**: `firmar()` sin `n_agentes` → `TypeError`. Nueve llamadores corregidos — Opus nombró cuatro. |

Las tres inversiones de la firma rompen por donde tenían que romper (A, B, C en la
BANDEJA). **El gate sigue congelado en `f96c234`**, verificado por diff.

## Qué espera, y de quién

- **El OK al REPORTE n_agentes obligatorio** (BANDEJA, 2026-10-09 04:51 UTC). **ALTO.**
- **CP2b**, si se habilita: el criterio local. Umbrales declarados *no calibrados*, y el
  test de que el filtro no vuelva absorbente al silencio.

## Base

`4feb88b`. Suite al arrancar: 360/360. Al cerrar: **379/379**.
