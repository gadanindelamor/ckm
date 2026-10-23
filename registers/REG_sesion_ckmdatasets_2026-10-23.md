# REG_sesion_ckmdatasets_2026-10-23

*Evaluación del repo y destrabe de push + ejecución - 2026-10-23*

## Hallazgos (CP0, sólo lectura)

- `main` estaba 2 commits adelante de `origin/main` (GitHub en `ac6211f`, v8g 19 may), sin pushear.
- Causa: `fourforums_no_parse_2016_05_18.sql` (570 MB) versionado sin LFS; GitHub rechaza > 100 MB.
- **P1-P4 nunca se ejecutó en v8g**: `from trace.ckm_p1p4_module` choca con el módulo stdlib `trace`; el `except ImportError` lo omitía en silencio. Ningún resultado P1-P4 salió de este repo.
- networkx no instalado (requerido por `ckm_p1p4_module.py`).
- v8h: `--sql` por defecto apuntaba a `trace/…sql`, el dump está en la raíz.
- Sin `requirements.txt`.
- `CONVENTIONS_experiments.md`: inventario desactualizado (v8c, `test_ckm_p1p4.py` no existen). No corregido.

## Tareas realizadas

| Commit | Cambio |
|--------|--------|
| `4b9f495`, `20f351c` | 2 commits locales reescritos sin el `.sql` (contenido y mensajes iguales) |
| `de25321` | `.gitignore`: `*.sql` |
| `fd6c05d` | v8g: import `ckm_p1p4_module` desde la raíz + aviso con causa; v8h: ruta `--sql` a la raíz; `requirements.txt` (numpy, scipy, networkx) |

- Push sin force: `ac6211f..de25321`, luego `de25321..fd6c05d`.
- `.sql` restaurado en la raíz, SHA1 `7db7fb40269e3ff9dba9008b1c99c31bd1c699d6` (idéntico al original). Ignorado por git.
- networkx 3.7 instalado. Verificado `HAS_P1P4 = True` en v8g.
- Prueba de humo de `run_all` sobre matriz sintética 8x8: P1-P4 completos, REG escrito (fuera del repo). No es resultado experimental.

## Respaldos conservados (no borrar)

- Rama local `backup/pre-sql-removal` y `refs/original/` (historial previo con el `.sql`).
- Copia `ff_backup.sql` en el scratchpad de la sesión.

## Riesgo

- El `.sql` existe sólo en este codespace. Guardar copia externa.

## Pendiente

- Correr v8g completo con P1-P4 sobre datos reales y registrar REG (primeros P1-P4 reales de fourforums).
- Actualizar inventario de `CONVENTIONS_experiments.md`.
