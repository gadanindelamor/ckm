# Texto para Code — 17 — repo ckm — freeze de los duplicados, P18, docstrings y ConnectTimeout — 28 oct 2026 (Opus 5.5)

```
Code: OK de Opus al 16.2b en lo que es suyo, y tres puntos más (el cuarto, cerrado). Por favor,
en este orden.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, 28 oct, entero.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Orden de prioridad de delamor (28 oct): CKM el instrumento, luego IAP,
  luego devices, luego conexiones y servicios. Los puntos van en ese orden.
- Unidad: cada punto, de corrido. A1.PAUSA sólo si un punto encuentra una
  tensión; seguí con los demás.

1. Docstrings del instrumento, sin cambiar código:
   - services/calibrate.py, extremo_colapso: "N_eff → 1" no es alcanzable.
     Que diga el lema que mediste (S ≠ 0 → todos +1 o todos −1 en un paso;
     S = 0, N par → órbita de período 2 {σ, −σ}), que el piso es ≥ 2, de qué
     depende (N, paridad, regla de empate, medida de σ₀; no de la escala ni
     de W) y la referencia a experiments/piso_del_colapso.py.
   - services/coco.py:333 y :403: la misma redacción vieja ("ver sweep n_runs
     60→70", "cuenta atractores"); que digan lo que el código hace, como el
     punto 5 del texto 15.

2. P18: el caso "vivo" de tests/test_calibrate_reusa_A0_en_lambda_cero.py se
   ancla a la copia preservada del intento 4
   (process/*.bak_1793150043_serie2_caso0, el corpus_state.json), con la
   ruta y la fecha en el docstring, como ya hace
   experiments/simpson_en_las_curvas.py. Si el archivo no está, el caso se
   salta diciendo por qué (no degrada en silencio). Sigue afirmando lo mismo
   (el reuso de A0 sobre una W real); cambia cuál W, y se declara.

3. iap_chatroom/tests/ — lo que es de Opus (OK):
   - Los 21 duplicados byte a byte del freeze: git rm de la copia viva.
     Antes, volvé a verificar con cmp los 21. Dejá en iap_chatroom/tests/ un
     MOVED_TO_FREEZE.md que liste los 21 y diga dónde está cada copia
     (process/iap_series_freeze_20261008/tests/) y la fecha. Grep de las 21
     rutas en todo lo vivo (código, README, CLAUDE.md, docs/defs, registers/
     — en particular REG_iap_caso_04b_v1): lo que es traza no se reescribe;
     si algo vivo apunta a la ruta vieja, decilo y actualizalo.
   - Los 3 iap_simulation*: al freeze (git mv a
     process/iap_series_freeze_20261008/tests/ o a una carpeta del freeze con
     fecha, la que corresponda), actualizando en el mismo commit el
     docstring de autonomous_device.py:5.
   - test_mcp_client.py, los 6 armstrong_* y los 2 wmixta_*: quedan.
   - test_caso_serie2_caso0.py: queda; dónde viven los casos lo decide
     delamor.

4. ConnectTimeout: NO se hace (decisión de delamor, 28 oct, devices:
   "no es producto, similar a presupuestos… no veo por ahora que aporte
   valor… veo que lo va a aportar pronto. aún no"). Queda tu lectura del
   15.2 como registro.

NO: la medida de referencia, el state_dir (E1) y P17, la estructura de los
casos (cases/, nombres sin test_), P14 puntos 1 y 2, los armstrong_*, el
patrón de calibrate, el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos (uno por punto), suite completa en serie al cerrar,
pull --rebase y push. A1.PAUSA.
```
