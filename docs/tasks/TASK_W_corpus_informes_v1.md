# TASK_W_corpus_informes_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: REG_seleccion_nodos_desempate_v1 (regla de desempate, §8 estabilidad); rebuild suspendido (`e1980e0`). delamor: hay que usar otro orden de magnitud de volumen en tests y experimentos.*

---

## Qué hacer

Construir W desde los **informes de trabajo** (v1–v28, subidos a `docs/*.docx`) y medir el instrumento ahí: es el primer corpus del proyecto con volumen.

**Insumo ya preparado** (no medido): 27 informes extraídos a texto; párrafos de ≥ 40 caracteres, deduplicados conservando la primera aparición → **1116 párrafos, 18.099 palabras**. Contra los 24 textos de caso09, dos órdenes de magnitud en párrafos.

## Decisiones a tomar antes (delamor)

1. **Granularidad del "texto"**: párrafo (1116), sección, o informe entero (27). CKM define co-ocurrencia *en el mismo texto*: la granularidad decide qué significa co-ocurrir.
2. **Deduplicación**: v1–v24 son acumulativos; sin deduplicar, un párrafo pesa hasta 24 veces (misma forma que la saturación de traza que frenó la Clase R). Deduplicado ya, pero es decisión declarable.
3. **top_k**: 32 como el canal, o mayor — con 18k palabras, 32 nodos es una fracción ínfima del vocabulario.
4. **Legitimidad del corpus**: son los informes del propio proyecto. DEFS §19 ya declara esa tensión: *"el corpus es simultáneamente datos y proceso"*. Acá es más fuerte: el corpus describe al instrumento que lo mide.

## Qué medir (una vez decidido lo anterior)

- **Selección**: N, empates en el borde, nodos aislados, y si el warm-up de la selección termina (Jaccard ≥ θ sostenido) — en caso09 llegaba recién en k ≈ 21 de 24; acá hay 1116.
- **Paisaje**: A0, N_eff y la señal de saturación con n_runs 50 / 1000 / 5000, y seeds 0/1/2 — la misma matriz de REG_seleccion §8, ahora con volumen.
- **Comparación**: si con volumen D_ckm deja de cambiar de signo entre seeds, y si N_eff0 crece o se estabiliza.
- **Costo**: tiempo por evaluación con N grande (el relax es O(N²) por paso).

## Resultado

Corpus: 870 párrafos únicos, 15.557 palabras, 27 informes
(`experiments/corpus_informes_limpio.py`). Driver:
`experiments/driver_W_corpus_informes.py`.

| unidad | textos | palabras/texto | con marcador | densidad | neg | mu_W | N_eff@1000 | N_eff@5000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| párrafo | 870 | 17.9 | 4% | 0.766 | 1 | 0.1094 | 2.00 | 2.01 |
| página 300 | 50 | 311.1 | 50% | 0.831 | 210 | 0.0294 | 9.52 | 9.68 |

**Decisiones tomadas (delamor):** texto = párrafo como candidata; y texto =
página, con la medida definida por Code: párrafos completos hasta ~300
palabras (una carilla a espacio simple), sin cortar ninguno.

- **Por párrafo el paisaje colapsa**: N_eff = 2 — todo encendido y su
  espejo. Régimen G2 de DEFS §13 (señal colapsada).
- **Por página hay paisaje**: N_eff ≈ 9.5, estable entre 1000 y 5000 runs.
- **Los 210 pares negativos no son más tensión.** El ruteo por marcadores es
  **por texto**: un texto largo tiene más chance de contener "pero". Textos
  con marcador: 4% por párrafo, 50% por página, con casi las mismas
  ocurrencias (25 vs 19). **Tensión estructural y longitud del texto quedan
  confundidas** — abierto nuevo, es del modelo.
- **Stopwords**: la medición inicial dio 9 de 32 nodos en palabras función
  castellanas. delamor decidió embeber la unión NLTK es+en y sklearn en
  (703). Con eso entran términos del dominio (histéresis, cohesivo,
  perspectiva, escenario). `apos` era un artefacto del extractor de Code
  (`&apos;` sin decodificar), corregido.

## Qué no hace

- No conecta nada al canal. No decide bootstrap ni umbral.
- No toca el rebuild: W se construye una vez (rebuild suspendido).

## Abierto

- Si este corpus sirve como referencia del instrumento o solo como prueba de volumen, dado que se describe a sí mismo.
- **El ruteo de oposición depende del largo del texto** (4% vs 50% de textos con marcador por la misma cantidad de marcadores). Con qué unidad —o con qué otro criterio— se elicita la tensión sin que la longitud la produzca.
- Extensión propia de stopwords para `puede`, `solo`, `dos`, `hacia`: no adoptada.
