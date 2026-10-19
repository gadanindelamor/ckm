# S2-C0 — qué quedó hecho del texto del 19 oct, y qué no

*Claude Opus 5 (Code), 19 oct 2026. Cierre por límite de sesión. Contra
`docs/opus/textos_para_code/TEXTO_PARA_CODE_S2C0_CP1b_19oct2026.md`.*

**Estado de los tests: 755 pasan, 7 xfailed, 0 fallan.** Árbol limpio: todo lo que pasa está
commiteado; lo que no pasa **no se commiteó**.

| Paso del texto | Estado | Dónde |
|---|---|---|
| La TASK actualizada a `docs/tasks/`, commit propio | **hecho** | `08b0430` (copia byte a byte, mismo sha256) |
| **(1) El orden de `calibrate`**: antes del rebuild, sobre la W candidata, con test y línea en el REPORTE | **hecho** | `1f7c8a3` · REPORTE en `496c525` |
| **(2a) Renombre `criterio_local` → `local_criterion`** (+ `CriterioLocal`, `UmbralesCriterioLocal`), sin alias | **hecho** | `e724b4d` |
| **(2b) Renombre `arranque` → `startup`** | **hecho**, y **le renombré también la API** (`set_state_dir`, `read_from_argv`, `requested_state_dir`, `was_requested`, `declare`). Eso lo decidí yo y está declarado en el commit: vos nombraste el módulo | `f49adb2` |
| **(2c) Las claves del panel del CP1 a inglés** | **A MEDIAS, sin commitear** | `git stash@{0}` |
| **(3) CP1b** | **no arrancado** — no tiene ni predicción escrita | — |

## Dónde quedó lo de las claves en inglés

En **`git stash@{0}`** (`"S2-C0: claves del panel del CP1 a ingles - a medias, 7 tests rojos"`).
Se recupera con `git stash pop`. Llegó a **7 rojos de 755**:

```
tests/test_local_criterion.py::test_el_panel_declara_los_umbrales_sin_calibrar
tests/test_neff_y_frontera.py::test_panel_declara_condicion_W
tests/test_serie2_caso0_cp1.py::test_e_min_df_es_2_y_viaja_en_la_declaracion
tests/test_serie2_caso0_cp1.py::test_g_una_accion_que_el_canal_no_acepta_...
tests/test_serie2_caso0_cp1.py::test_h_el_panel_muestra_el_resultado_de_calibrate_...
tests/test_serie2_caso0_cp1.py::test_h_coco_no_sigue_con_el_0_40_del_modulo_...
tests/test_should_rebuild_conectado.py::test_cp2_el_punto_de_calibrate_ahora_CORRE
```

**Los 7 son del mismo tipo, y es un error mío de barrido:** traduje también claves que **no
nacieron en el CP1** y que otros lugares siguen leyendo en castellano — `calibrate.py`
devuelve `estado`/`valores`/`condiciones`, el panel de Monitor tiene `condicion_W`, el
criterio local `umbrales_calibrados`, la declaración `parametros_del_servicio`.

**El arreglo, que ya apliqué para `calibrate` y funciona:** **publicar** en inglés y **leer**
esas claves como están (`registro["estado"]` → `"state"` en el panel). Falta hacer lo mismo
en los otros cuatro lugares y revisar los asserts de esos 7 tests.

**A1 — lo que no puedo afirmar:** que con ese arreglo el stash cierre en verde. Lo medido son
los 7 rojos y de qué tipo son; que alcance **no está verificado**.

**A1.PAUSA.**
