TAREA AUTÓNOMA — BARRIDO DE DEFS Y PAPER, con la metodología de TRUST como lente declarada (delamor, 22 oct). Si la tarea REPO de hoy no terminó, ésta va después: no la interrumpas.

Leé primero, enteros: docs/opus/METODOLOGIA_TRUST_v1.md (la lente) y readme/METODOLOGY_v3.MD (la de Sonnet sobre CKM, de donde sale la forma). Registrado en docs/opus/decisiones_en_el_acto.md (22 oct).

La unidad es el documento. Output 1 de cada CP = la versión siguiente del documento. Otros outputs son posibles y no bloquean.

CP1 — DEFS: docs/defs/DEFS_CKM_estado_actual_v17.md → v18.
CP2 — PAPER: docs/opus/PAPER_Landscape_Driven_Device_v29_borrador_opus.md → v30 (borrador, en docs/opus/), usando la DEFS v18.
El v17 y el v29 no se tocan: la traza con fecha no se reescribe.

Cómo, en los dos CP (la regla CKM TRUST aplicada al documento):
- C: cada pasaje. f (uno solo): ¿lo sostiene una fuente primaria — código o REG — con archivo y línea? No META REG, no resúmenes: la confianza no es transitiva.
- Si f decide (hay fuente, o es claro que no la hay), decide f. Si es empate de verdad (fuente ambigua), conserva el pasaje como estaba (T) y queda declarado. El riesgo a vigilar: llamar empate a lo que no se midió.
- Si no encontrás la fuente, no inventes corte: la duda sube. ↑k = Opus: PREGUNTA NO BLOQUEA en la BANDEJA, conservás el pasaje como default declarado y seguís.
- Tu redacción es el g del documento: va nombrada, no escondida.
- Ya decidido por delamor (21 oct): la frase "COCO was never connected to the live IAP channel" sale, sin reemplazo — en el v29 está en las líneas 144, 281 y 668; buscá también sus equivalentes en la DEFS v17. COCO se conectó en el intento 2 (registers/REG_iap_serie2_caso0_intento2_v1.md); eso no entra como reemplazo de la frase.

Nulos: un grep da presencias; la ausencia sale de comparar. Output secundario (no bloquea): por cada documento, el mapa entre versiones contiguas de lo que aparece, desaparece o se repite sin que ninguna decisión registrada lo explique — empezando por el hilo de la frase de COCO a través de las versiones del paper (en cuáles está, cuántas veces, cómo cambia). Con archivo y línea, sin interpretar.

Dos cuidados que la metodología misma declara:
- Anacronismo: la lente es del 4–22 oct; las versiones viejas se leen con ella, no se juzgan por ella.
- Circularidad: la lente ya trae el hallazgo de COCO. Lo valioso es lo que NO anticipa: anotalo aparte, para una METODOLOGIA v2.

Reglas: git pull --rebase antes y antes de cada push; push al cerrar cada CP; commits nombrando archivos. Entrada en la BANDEJA por CP (revisé / encontré / no pude revisar). Trabajá de corrido: A1.PAUSA sólo al terminar los dos CP o si algo bloquea todo. Nada de código del modelo se toca; nada de vivos.

Después de esto (no es tuyo): review externo del v30 y la versión final para delamor, que no lleva preguntas ni cosas a verificar.
