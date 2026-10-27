# ESTADO al cortar — 27 oct 2026 (Opus 5.5, Cowork)

La traza completa está en `docs/opus/decisiones_en_el_acto.md`, 27 oct. Esto es sólo el mapa.

## Hecho hoy
- **TASK_calibrate_en_el_build_v2: cerrada en CPa–CP2, y CP3 (el vivo) corrido.**
  - CP1 (`0d2e2d8`): la primera W nace por su propia condición, calibra antes de instalarse y deja su línea `bootstrap`.
  - CP2 (BANDEJA, 07:10 UTC): la calibración tiene su lugar en la Config, firmada con su W. La vara de COCO es un `Threshold` `MEASURED` o `DECLARED`, con su causa. `n_runs` de calibrate = 1000. Suite: 872 passed, 7 xfailed, 0 failed.
  - CP3: `serie2_caso0`, intento 4, 1204 s. Las 7 calibraciones dieron `no_calibrado: sin_separacion`; hubo 0 disparos. El REG está en `registers/REG_iap_serie2_caso0_intento4_v1.md`, con el OK de delamor.
- **Definiciones de delamor:**
  - `n_runs` de calibrate = 1000. Su razón: *"darles posibilidades para que sientan el sesgo"*.
  - Defaults de la Config: el valor da igual; lo que importa es que caer en uno se vea.
  - El margen: *"lo de siempre es el sesgo de querer ponerle el NUMERO conveniente. en vez de sostener la tension"*. No se toca.
  - `w_sha_match`: el arreglo propuesto es sesgo de control. Queda la colisión registrada.
  - Parámetros de muestreo (n_runs, seeds, los de Boltzmann si los hay): si es el mismo concepto, un campo; si no, un nombre por concepto (BABEL). El default es uno solo, para los tres casos y los que vengan. Un valor distinto por caso sólo lo pone un driver que lo declara.
- **DEFS v19** (`docs/defs/DEFS_CKM_estado_actual_v19.md`). Lo que dependía del CP2 quedó como "decidido, no implementado".
- Textos para Code: 11 (CP2 y cierre), 12 (el vivo) y 13 (los parámetros de muestreo, más dos correcciones de registro).

## Qué espera y de quién
- **Code:** el texto 13. (1) Revisar en Monitor, COCO y la copia de W si cada parámetro de muestreo es el mismo concepto, y después implementarlo. (2) Guardar `w_sha_live_at_calibration` en el registro. (3) Que el test de β busque en la estructura.
- **Opus (próxima sesión):** leer el reporte del texto 13 en la BANDEJA. Actualizar en las DEFS v19 los renglones del CP2 ("decidido" → "implementado") y lo que salga de los parámetros de muestreo. Después, el v33.
- **delamor:**
  1. **E5:** anotar en el docstring de `ckm_monitor.py:84-90` que la "primera calibración que separa" fue con `n_runs = 200, seed = 0`.
  2. **E1:** el `state_dir` por default de `CKMMonitor` es el directorio declarado traza. ¿Se cambia?
  3. **P14:** los drivers declaran tres cosas que IAP no declara: los archivos de estado, el puerto y los providers. ¿Se encara, y quién lo decide?
  4. Siguen los del 24 oct: J1, J2, los subgrafos chicos, `W_asim` y la figura Monitor contra COCO.

## Raro
- Los commits de Opus en la PC dejan locks en `.git`. El permiso de borrado se pide de nuevo en cada sesión.
- En `.git/objects` siguen 302 `tmp_obj_*` viejos; no se tocaron.
- Hay dos tests sensibles en la suite, reportados por Code: el de β (falso positivo por un timestamp) y `test_oda_continuo` (20 ms, depende de la carga).

---
## 27 oct, tarde — el texto 13, cerrado por Code
- **Hecho:**
  - Monitor, COCO y la copia de W leen `n_runs` y `seed` de un solo lugar en la Config.
  - Un valor distinto por caso sólo entra si alguien lo firma con `declared_by`.
  - `w_sha_live_at_calibration` se guarda en el registro de la calibración.
  - El test de β busca en la estructura.
  - Suite: 890 passed, 7 xfailed, 0 failed, 49 s.
- **Decidido por delamor:** el default de muestreo es **200** y la semilla es 0. Reemplaza el 1000 de esta mañana, que queda como traza. A 200 vuelve la dependencia de la semilla medida en el CP0.
- **Opus (próxima sesión):**
  - las DEFS v19: §10 y §12 dicen 1000 → 200; los renglones del CP2 pasan a "implementado"; y lo del texto 13;
  - el docstring de `coco.py:173-175`, que Code midió que ya no es cierto tal como está escrito;
  - después, el v33.
- **delamor — lo nuevo, con qué hay que decidir:**
  - **La copia de W cuenta siempre en `uniform`.** Qué es: `calibrate` no declara `sampling_mode` ni `n_warmup`. Si el canal corriera en `weighted` o `boltzmann`, la vara de COCO saldría de una curva `uniform`. Hoy el canal corre en `uniform` y no se nota. Hay que decidir si `calibrate` lee el modo de muestreo de la Config. Es el patrón de calibrate (E3).
  - **Dos `seed` con el mismo nombre en `calibrate`.** Qué es: el de `extremo_expansion` elige qué pares invierten el signo; no sortea `sigma_0`. Hay que decidir si se renombra (BABEL). Hoy no se usa en el flujo.
  - **Q1–Q3, que trajiste vos y quedan abiertas** (BANDEJA, 16:45 UTC): los nombres de `d_ckm`, permutar roles de devices entre providers, y FREE WILL después de un `LEAVE`.
  - **A5:** `human_device_skin` nace en la BANDEJA, con sus condiciones (17:00–17:10 UTC). No es un pedido.
