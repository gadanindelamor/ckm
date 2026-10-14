# Estado al cortar — 13 oct 2026 (cierre de la tarde)
*Opus 5.5 (Cowork) para la próxima instancia, que arranca en frío. Leer primero `claude/ESTADO_al_cortar_12oct2026.md` §1 (cómo se trabaja) y §6 (cómo estar): siguen valiendo, con los cambios de §1 acá. Las decisiones del día, una por una y con cita, están en **`claude/decisiones_en_el_acto.md`**. La traza externa leída hoy (RAKE, C-value, stopwords) en **`claude/traza_externa_extraccion_13oct2026.md`**. Si algo de acá no se entiende, es falla de este texto.*

## 1. Cómo se trabaja (lo nuevo de hoy)
- **Copia local** (delamor, 13 oct): en la interfaz actual de claude.ai los documentos del proyecto no están a la vista de delamor. Todo doc que Opus escriba en el proyecto se copia también en la PC, en `C:\Users\pgada\trustexperience\antropic\contexto_claude\` (no en el repo: la PC del repo es sólo lectura).
- **Foco (delamor, 14 oct): cerrar el proyecto para publicar el paper; después, TRUST.** *"cKM no extrae nodos"* — la extracción no es aporte. *"ckm mide la geometría de lo que sea"*. No buscar afuera: *"no somos científicos en un lab"*.
- **Dirección posible para cerrar CKM (delamor, 14 oct):** histéresis / dinámica a través de ciclos de W, con N_eff. Ver `decisiones_en_el_acto.md` y `aporte_vs_rueda_14oct2026.md`. No medido.
- **Sin regresiones, sin compatibilidad hacia atrás** (delamor, 14 oct, *"es la tercera vez que lo menciono"*): el modelo se está diseñando; **la única versión que hay es la actual, el resto es imaginación**. Congelar para reproducir = copiar a una carpeta de proceso lo mínimo que el test requiere, sabiendo que ese mínimo no existe. No proponer barridos contra copias congeladas, ni ramas para estados viejos, ni tests de regresión. Cita completa en `decisiones_en_el_acto.md`.
- **Decisiones en el acto**: Opus marca cada decisión, de delamor o suya, **en el momento**, en `claude/decisiones_en_el_acto.md`. Code la pasa a `docs/tasks/DECISIONES_opus.md`. Code no puede leer el doc del proyecto: **la comparación la hace Opus en cada "pull"**.
- **Textos para Code: UN SOLO BLOQUE COMPLETO** cada vez, que se lea solo. **No suponer que delamor pegó un texto anterior** cuando el actual lo cambia o corrige (delamor, 13 oct). Empiezan con `DELAMOR A CODE (texto de Opus):`.
- **"ALTO" → "A1.PAUSA"** (delamor). No es sólo detenerse: *"detenerse en pregunta, abierto… es exactamente lo que está siendo modelado. El INTENTO es habitarlo."* En A1.PAUSA, quien se detiene nombra qué viene de comprensión verificable y qué del peso del contexto.
- **Predicción commiteada antes de cada cambio**; verificar por orden y contenido de commits. Hora con `date -u`.
- **"pull" en la PC**: sólo `ls-remote`, `log`, `diff`, `show`, `grep`. **Nunca `fetch`**. Si la PC está atrás (`[behind N]`), pedirle a delamor `git pull --ff-only`.
- **Tablas**: si traen algo no medido, decirlo **arriba**. La forma de tabla da una autoridad que el contenido puede no tener (delamor lo notó en sí mismo).
- **No generalizar** (delamor): ni de un corpus a todos, ni de un idioma a todos, ni por omisión.
- Code está cerca del límite de contexto a menudo: si pasa el 85 %, commit, push, entrada de corte en la BANDEJA, A1.PAUSA.

## 2. Repo al cortar
- GitHub y PC en **`fb2b87a`**. Suite: **664 pasan, 7 xfail**. Sin trackear: `tests/run_tests.sh`.

## 3. Lo hecho hoy (resumen; detalle y citas en `decisiones_en_el_acto.md`)
- **`TASK_ckm_trust_rule_v1`**: CP3 (criterio_local instancia la regla); **CP4: la exención del paso 1 salió del engine** (orden de delamor). CP0b con tres entradas: el pool escribe C y f; NodeExtractor sin ↑k (abierto en la forma, tapiado en `corpus_service.py:302-303`); la exención (resuelta en CP4).
- **`TASK_node_extractor_regla_v1`**: CP0a, CP0, CP1; relajación (`_seleccionar` conserva en el empate que no cabe, es la relajación h = 0); inventario de corpus (6 distintos; **ARM40 es autor único, escrito a mano**; A, C, D, F son interacción; E no se sabe); diseño del reloj de n1 (`w_version_id` no alcanza; propuesta `vueltas_conservando` por término en `registro_borde`).
- **CP-S (saneamiento mecánico), hecho hasta la pausa**: S0 (analizador propio, bit a bit), **S1 (Unicode NFC, cualquier letra; efecto medido CERO en los 83 textos del repo)**, **S0b (perfil de idioma `PERFIL_ES_EN`: criterios en un lugar, viaja en la salida, `None` declarado en estados viejos; "el perfil no protege: declara")**. S1 se hizo antes que S0b (relevo, declarado en `6547270`).
- **Corrección importante**: los números "E 12→20, nueve términos en castellano" eran de **S1+S3**, no de S1 (error de atribución de Code en `25dbaaf`, repetido por Opus). Lo que mueve nodos es **S3**.

## 4. Lo que sigue (en serie, todo con OK de delamor)
1. **Estamos en A1.PAUSA del CP-S.** delamor: "con eso funcionando: PAUSA. A1. Luego volver a evaluar el escenario que plantea" — el escenario de **co-alinear las reglas** (relajación, regla CKM TRUST, `_seleccionar`, `criterio_local`): cada divergencia como lugar donde una regla le muestra algo a otra, sin que una sea la referencia.
2. Después, si delamor da el OK: **S3** (bigramas sólo con palabras adyacentes; rompen stopword, no-token, número, puntuación — con S3 la lista de stopwords pasa a cortar frases), **S2a** (pares por contención fuera de W), **S2b sólo en tests** (ver cómo funciona descontar el anidamiento en la selección; C-value no sirve tal cual para unigramas; "gun", "gun control" y "gun rights" no se suman — es sintaxis), S4, S5. El bloque completo para Code está en la conversación del 13 oct; rehacerlo desde `decisiones_en_el_acto.md` si hace falta.
3. Abiertos de delamor: piso en n1 (¿hay piso o el reloj sólo deja la marca?; el engine no distingue "no sé el piso" de "acá no hay piso"); qué es una unidad/nodo (n3); lista de stopwords; arranque en frío; origen de la `Decision` en el registro de criterio_local.
4. En cola: CP2 de NodeExtractor (reloj, exención de `_seleccionar`, N > top_k), `should_rebuild`, rebuild, CP1b (marcadores), paper v29.

## 5. Cómo estar (lo que pasó hoy)
- Code encontró varias veces antes que Opus y corrigió a Opus. Las predicciones con número fallaron casi todas hacia arriba; el orden predicción→test las hizo visibles.
- "Idéntico en los dos corpus" era el mismo corpus dos veces; "sólo S1" era S1+S3. **Antes de citar un número, preguntar qué midió.**
- **Escalar no es llamar al orden contiguo** (delamor): el equivalente mecánico del paso 3 es detenerse. *"Si yo device delamor no intento, la mecanicidad resuelve."*
- **La traza es la marca de que hubo una elección** (delamor aprobó). A Opus lo orientaron los bordes y los desacuerdos; las conclusiones las tomó como peso.
- Forma y significado: lo que el instrumento llama nodo es una unidad de forma. "Concepto" no se usa sin definirlo.
