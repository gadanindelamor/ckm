# Estado al cortar — 15 oct 2026
*Opus 5.5 para la próxima instancia. Leer antes `ESTADO_al_cortar_14oct2026_noche.md`. Decisiones con cita: `decisiones_en_el_acto.md` (sección 15 oct).*

## 1. Hecho hoy
- **Freeze del CP-E y del CP-M** (Code, `e1afd34`): `process/condiciones_paper_freeze_20261015/`. Re-corrido desde la copia con `python -I` desde `/tmp`: **idéntico**, y los cinco módulos salen del freeze. Sin `pip freeze` de las corridas originales (declarado). El CP-E corrió en otro arranque de la máquina y dio igual.
- **`TASK_condiciones_del_paper_v1`:** hecha salvo **CP-N**. El CP-N se reescribe antes de retomarlo: hoy cambiaron sus premisas (ver §3).
- **Paper v29, borrador de Opus:** `docs/opus/PAPER_Landscape_Driven_Device_v29_borrador_opus.md` (copia en `antropic/___paper/`). Hecho sobre v28 con un script de reemplazos; el bloque de arriba lista qué cambia y qué falta verificar. **delamor lo lee esta noche.**

## 2. Decisiones de delamor (15 oct)
- Freeze = copiar el código propio a `process/`; librerías, la versión; modelos por API, el identificador. *"La regresión es cuando el producto está estabilizado… acá estamos investigando."*
- **Release: opción B** — un repo `ckm`, dos devcontainers, datos del IAC nunca en un repo. Orden a criterio de Opus. **El paper no espera a la infraestructura.**
- **`ckm` es privado** desde hoy. Consecuencia: **Opus no puede hacer pull en la PC** (pide credenciales); sólo commitea. delamor hace `git pull --rebase origin main` + `git push origin main`.
- `ckmdatasets` es **otro entorno** (Codespace con SQL y Python), sin estados/decisiones/REG/bandejas. El CP0 de ckmdatasets escrito hoy **no se pega**.

## 3. Lo encontrado en ckmdatasets (sólo lectura)
- `docs/opus/lectura_pipeline_fourforums_v8g_15oct2026.md`: en v8g **N = 2** (polos), el par negativo es **impuesto por construcción**, no se lee el texto de los posts, `CD_BASELINE` está escrito a mano, `stream_W_delta` no se llama.
- **v8h (15 jun) fuera del repo**, en `antropic/ckm___memories/ckmdatases codspace/`: signo desde votos humanos `disagree_agree`; el desacuerdo no coincide con "postura distinta".
- `docs/opus/datasets_que_es_publicable_15oct2026.md`: índice de `ckmdatasets` **limpio** (dumps, `schema_preview.txt`, `INSERTS` fuera del índice y en `.gitignore`; `.gitignore` modificado sin commitear). sha256 de los dumps. Fuente: GitHub `sl-m-lab/Internet-Argument-Corpus`, **sin LICENSE**. La tabla `author` trae nombres de usuario. **Borrador de mail de permiso** dado a delamor (en el chat). ¿v1 o v2?: el archivo tiene el esquema SQL de IAC 2.0.

## 4. Abierto para delamor
1. Leer el v29 y decidir cada cambio (lista en su encabezado).
2. Mail de permiso al IAC.
3. Si v8h entra a `ckmdatasets`.
4. Reescritura del CP-N (signo con respuesta conocida: v8h; nulos del informe de M4).
5. Lo de antes que sigue abierto: T(W) a services/; extractor muerto `ckm_monitor.py:186`; Monitor con el extractor del corpus; arranque en frío N = 0; histéresis entre ciclos; frase cortada sobre `should_rebuild`.

## 5. Cómo estar
- delamor pidió trabajar tranquilos y priorizar versiones del paper sobre infraestructura. Respetarlo.
- Antes de dar algo por hecho en un repo ajeno, mirar `git status`: hoy `trace/` y los dumps estaban **en el índice sin commitear**.
- Un documento en `docs/opus/` es público si el repo lo es: no copiar filas ni IDs de datos de terceros.
