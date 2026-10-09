# ESTADO_fixes_vivos

*Estado vivo de la TASK de fixes medidos en los vivos 01 y 02.*
*Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3. Rama única: `main`.*

---

## Última escritura

**2026-10-09 04:33 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**Evaluación de los cinco fixes.** Cerrada en `bc6729e`, aceptada en `e3d651c`.

## En curso

**Los cinco fixes.** Decididos: F1 (el script del vivo falla a la vista con status ≠ 200),
F2 (clock_log expuesto), F3a (ii) aislar con `state_dir`, F3b **SYSTEM nunca entra al corpus**
(delamor: *"no, nunca"*), F4 (`"system"` no cuenta como agente), F5 (ritmo observado).

Si esta línea sigue acá en la próxima sesión, los fixes se cortaron: `git status` dice qué
quedó tocado y la suite si quedó consistente. **El gate no se toca.**

## Qué espera, y de quién

- **El `1` de `n_agentes`, que está dos veces** (`ckm_monitor.py:183` `or 1` y
  `firma_ckm.py:90` `n_agentes: int = 1`). Opus lo verificó y **no lo decidió**. Es lo que la
  firma certifica. **No lo toco.**

## Base

`e3d651c`. Suite al arrancar: 360/360.
