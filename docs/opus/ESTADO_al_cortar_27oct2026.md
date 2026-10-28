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

---
## 27 oct, cierre — después del texto 13
- **Resuelto:**
  - E5: el docstring de `ckm_monitor.py` declara las condiciones de la primera separación en un vivo (`293fd44`).
  - P13 ya estaba resuelto (la "fila misteriosa").
  - P14 punto 3: los providers pasan a IAP (delamor).
  - `iap_chatroom/tests/` es process: no se agregan archivos ahí.
- **Textos para Code pendientes, en orden:**
  - **14:** el intervalo de Simpson, el piso del colapso por enumeración y la medida de referencia.
  - **15:** hacia el próximo vivo. `--check`, la caída de B, el test del skin, el inventario de defaults y el docstring de `coco.py`.
  - **16:** el registro de providers en IAP y la clasificación de `iap_chatroom/tests/`, con A1.PAUSA antes de mover.
- **Opus (próxima sesión):**
  - leer en la BANDEJA los reportes de 14, 15 y 16;
  - dar el OK o subir a delamor el movimiento de `iap_chatroom/tests/`;
  - las DEFS v19: 1000 → 200, CP2 implementado, texto 13, E5 resuelto, la medida de referencia y el piso del colapso según el 14;
  - después, el v33.
- **delamor:**
  - **La medida de referencia:** "uniforme" en el código (30–70 % de nodos activos) no es la del paper (uniforme sobre {−1,+1}^N). Decide después de la lectura de Code. Declaró su propio sesgo hacia la opción más directa.
  - **E1, el state_dir:** espera el `--check` y el inventario. Opciones A, B y C, con la inclinación de Opus por B.
  - **P14 puntos 1 y 2** (los archivos de estado y el puerto): ¿también pasan a IAP?
  - **Siguen abiertos:** el patrón de calibrate (la tensión del margen sostenida; el máximo interno; el rango expansión–contracción; el percentil sobre el ruido propio; la W sombra) y las dos semillas en `calibrate`. También J1, J2, los subgrafos, `W_asim`, la figura y el REG del intento 2.
- **Abierto, sin pedido:**
  - "ODA son 4 pasos y uno no es paso";
  - el criterio local es implementación, no paso;
  - `human_device_skin` (¿evolución de la GUI?);
  - Q1–Q3.

---
## 28 oct — reportes de 14, 15 y 16 leídos; decisiones; textos 17, 18 y 19
- **Decidido por delamor:**
  - la medida de referencia es la del código (la banda);
  - λ\* cerrado por declaración;
  - IAP declara lo suyo (los archivos de estado, el puerto, los casos en `cases/`, el state_dir por corrida), con la implementación delegada en Opus;
  - devices: aún no;
  - la regla amarrete;
  - todo sin criterio local;
  - el orden de prioridades: instrumento, IAP, devices, servicios.
- **Definición candidata, sin registrar:** "W supera el piso" ⇔ N_eff(W, μ) > F(N, μ), con F exacto por forma cerrada. Espera el reporte del texto 18.
- **Code, en orden:** el 17, el 18 y el 19.
- **Opus (sesión nueva), por dirección de delamor:** *"cerrar DEFS y paper. luego continuar exploración"*.
  - **DEFS v19:** 1000 → 200; CP2 implementado; texto 13; E5 resuelto; la medida de referencia (la banda; la validación del paper bajo el hipercubo); el lema del piso (paridad, forma cerrada); la masa de cuenca como una de las mediciones; la torsión y los `rechazados` según la fase; los resultados del 18 y la definición si se registra.
  - **v33,** según el plan del 26 oct más lo anterior.
- **Después, la exploración:** el caso 1 (sin definir); otro intento del caso cero con permutación de roles y providers, sin criterio local; el skin.

---
## 28 oct, cierre del día — cambio de fase
- delamor: *"TRUST, el proyecto está cambiando de fase, acumulación a EVALUACIÓN.. CKM cierra y se transforma en TRAZA VIVA"*.
- **El plan:** las DEFS v19, el paper v33, el plan de cierre del repo y el release; *"y vemos qué sucede"*.
- **Próxima sesión de Opus (nueva, desde este ESTADO):** las DEFS v19 primero y después el v33, con el corte del 28 oct. Lo verificado hasta los reportes de hoy entra; el texto 18 entra si llega antes; lo demás va a otros papers.
- **Los textos 17, 18 y 19:** pendientes. Se evalúan dentro del plan de cierre del repo; delamor decide si Code los hace antes.
- **Actualización (delamor):** los textos 17, 18 y 19 **esperan** hasta saber qué respaldo necesita el paper. El v33 se escribe primero; de ahí sale qué se le pide a Code.
