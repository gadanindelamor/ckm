# REG_unidad_texto_saturacion_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Continúa TASK_W_corpus_informes_v1 (W del corpus de informes) y
REG_seleccion_nodos_desempate_v1 §Abierto (volumen).*

---

## Descripción

Qué es *un texto* no es una decisión editorial: CKM define la co-ocurrencia
**en el mismo texto**, así que la unidad decide qué significa co-ocurrir y,
por esa vía, qué W existe. Párrafo y página son unidades **tipográficas** —
vienen del formato del documento, no del campo.

*(delamor: la unidad de texto es dependiente de W. Son condiciones, no
límites. Textos científicos, blogs o tweets es diferente.)*

Este REG mide la dependencia, y encuentra que la cantidad que explica el
colapso del paisaje no es la densidad ni la tensión: es la **saturación de
pares distintos**.

Se miden tres unidades: **párrafo**, **página** (de 40 a 500 palabras) y
**versión** (un informe = un texto). Las dos primeras son tipográficas; la
tercera no.

Instrumento: `experiments/driver_unidad_texto.py`
(`--activacion`, `--coocurrencia`). Corpus de informes: 870 párrafos únicos,
15.557 palabras (`experiments/corpus_informes_limpio.py`). top_k = 32
(496 pares posibles), stopwords 703, rebuild suspendido.

---

## 1. Activación por texto

| corpus | textos | palabras p10/med/p90 | nodos activos (med) | textos con 0 nodos | densidad W | pares neg |
|---|---:|---|---:|---:|---:|---:|
| párrafo | 870 | 7 / 14 / 37 | 1 | 34% | 0.766 | 1 |
| página 40 | 300 | 41 / 49 / 66 | 4 | 6% | 0.849 | 12 |
| página 60 | 217 | 61 / 68 / 86 | 5 | 2% | 0.877 | 31 |
| página 100 | 139 | 101 / 108 / 129 | 7 | 1% | 0.905 | 32 |
| página 150 | 95 | 152 / 160 / 182 | 9 | 0% | 0.885 | 78 |
| página 200 | 74 | 201 / 210 / 227 | 12 | 0% | 0.899 | 81 |
| página 300 | 50 | 301 / 310 / 325 | 14 | 0% | 0.831 | 210 |
| página 500 | 31 | 503 / 511 / 530 | 18 | 0% | 0.909 | 420 |
| **versión** | 27 | 232 / 368 / 1027 | 15 | 0% | 0.946 | 461 |
| IAP caso09 | 24 | 18 / 76 / 147 | 7 | 0% | **0.514** | 100 |
| IAP caso13 | 26 | 10 / 73 / 178 | 12 | 0% | 0.780 | 47 |
| IAP caso14 | 18 | 4 / 224 / 512 | 20 | 0% | 0.976 | 481 |

- **Los mensajes del canal no son tweets.** Mediana 73–224 palabras: están
  más cerca de un párrafo de paper que de un mensaje corto. La intuición de
  "mensajes breves" no se sostiene contra la medición.
- Por **activación**, caso09 (7 nodos/texto) coincide con páginas de 100
  palabras, aunque la mediana de palabras sea distinta (76 vs 108). La
  palabra no es la unidad; el nodo activo sí.

*Estado: verificado.*

---

## 2. Distribución de co-ocurrencias por tamaño de texto

| corpus | textos | pares tot. | p10 | med | p90 | máx | textos 0 pares | pares distintos | / 496 | pares/100 pal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| párrafo | 870 | 1440 | 0 | **0** | 6 | 45 | **61%** | 386 | 78% | 9.3 |
| página 40 | 300 | 2348 | 0 | 6 | 21 | 45 | 15% | 451 | 91% | 15.1 |
| página 60 | 217 | 2767 | 1 | 10 | 28 | 55 | 7% | 463 | 93% | 17.8 |
| página 100 | 139 | 3769 | 3 | 21 | 55 | 136 | 3% | 487 | 98% | 24.2 |
| página 150 | 95 | 4247 | 6 | 36 | 91 | 136 | 0% | 491 | 99% | 27.3 |
| página 200 | 74 | 4532 | 12 | 60 | 105 | 153 | 0% | 491 | 99% | 29.1 |
| página 300 | 50 | 4624 | 28 | 91 | 155 | 210 | 0% | 478 | 96% | 29.7 |
| página 500 | 31 | 4598 | 28 | 153 | 231 | 253 | 0% | 495 | 100% | 29.6 |
| **versión** | 27 | 4023 | 58 | 105 | 240 | 435 | 0% | **496** | **100%** | 25.9 |
| IAP caso09 | 24 | 636 | 6 | 21 | 45 | 91 | 0% | **307** | **62%** | 30.9 |
| IAP caso13 | 26 | 1834 | 6 | 66 | 136 | 171 | 0% | 434 | 88% | 58.2 |
| IAP caso14 | 18 | 3205 | 1 | 200 | 283 | 351 | 6% | 492 | 99% | 64.9 |

- **La mediana del párrafo es 0 pares**: el 61% de los párrafos no aporta
  ninguna co-ocurrencia. Con un solo nodo activo no hay par posible. El
  corpus por párrafo es, en su mayoría, textos que no participan de W.
- **Los pares totales saturan** entre 300 y 500 palabras (4624 vs 4598:
  agrandar el texto deja de agregar).
- **Pares/100 palabras crece y se estanca** (9.3 → 29.7 → 29.6). No es una
  medida de densidad conceptual: es el efecto combinatorio de tener más
  nodos activos en el mismo texto.

*Estado: verificado, una corrida por celda.*

---

## 3. La saturación de pares distintos es la cantidad que explica

De `página 40` en adelante, los pares **distintos** ya son 451–495 de 496.
**W se queda sin ceros.** Un W casi completo no tiene estructura que
distinguir: por eso el paisaje colapsa a N_eff = 2 (todo encendido y su
espejo, régimen G2 de DEFS §13) y no porque el texto sea "denso".

La densidad de W (§1) no ordena el fenómeno —0.831 en página 300 con
paisaje, 0.849 en página 40 sin él— y los pares distintos sí:
lo que importa no es cuánto pesa cada par, sino **cuántos pares nunca
ocurren**.

**caso09 es el menos saturado de todos los corpus medidos: 307/496 (62%).**
Es el único donde W conserva ceros en cantidad. Los casos posteriores del
canal se saturan (caso13 88%, caso14 99%) — el canal fue perdiendo la
estructura que caso09 todavía tenía.

**Candidato a criterio de unidad de texto**: la saturación de pares
distintos. A diferencia de la tensión (§5), no premia el texto largo: crece
monótona con el largo hasta 100% y ahí deja de informar, de modo que el
criterio es *mantenerse lejos de la saturación*, no maximizar nada.

*Estado: verificado como medición; el criterio es propuesto, no decidido.*

---

## 4. La versión satura del todo — y el cero de W cambia de significado

*(delamor: faltó probar por versión como unidad de texto.)*

Un informe = un texto: 27 textos, la única unidad medida que **no** es
tipográfica. Viene del ritmo del trabajo, no del formato del documento. Con
los informes deduplicados (v1–v24 son acumulativos), el texto de una versión
es **lo que esa versión agregó**, no lo que contiene — y no hay alternativa:
sin deduplicar un párrafo pesaría hasta 24 veces.

| | versión |
|---|---:|
| textos | 27 |
| palabras p10 / med / p90 | 232 / 368 / 1027 |
| pares distintos | **496 / 496 (100%)** |
| pares negativos | 461 |
| ceros de W | 27 |
| A@1000 / N_eff@1000 | 3 / **1.00** |
| `force_w_pos`: A / N_eff | 7 / 2.02 |

**Es el corpus más saturado de todos: ocurren los 496 pares posibles.** No
queda un solo par que no haya co-ocurrido alguna vez. Y el paisaje es el
peor de la serie: N_eff = 1.00 — ni siquiera los dos estados espejo del
régimen G2, sino uno solo que se lleva toda la masa.

**El hallazgo del cero.** W tiene 27 ceros fuera de la diagonal. Verificado
par por par: **los 27 son cancelaciones** (el mismo par ocurrió en los dos
signos y se anularon); **ninguno es ausencia**. Con saturación total, el
cero de W deja de significar "estos dos nunca co-ocurrieron" y pasa a
significar "co-ocurrieron por igual en los dos sentidos". Dos objetos bajo
un mismo número, y el paisaje no puede distinguirlos: para el relax, la
ausencia y el empate perfecto son el mismo 0.

*(delamor, sobre la ceguera de Fabricación: lo que la garantiza es la
función matemática `cancelar(...)`.)* Acá la misma operación produce, en el
otro extremo, una ceguera que no se buscó.

**Para la ingesta incremental**: la versión es la unidad más cercana a un
incremento real, y aun así cada texto llega saturado. Ingerir por versión
significa que la primera ingesta ya trae casi todos los pares; la
trayectoria de saturación en el tiempo empieza arriba, no abajo.

*Estado: verificado (ceros por cancelación, 27/27; ausencia 0/496).*

### 4.1 Control — no es el formato incremental, es el tamaño

*(delamor: es por el formato de versión incremental, imagino.)* Se probó.
Control: **mismos tamaños, párrafos repartidos al azar** — rompe la
coherencia de versión y conserva el formato de tamaños.

| corpus | txt | pal med | distintos | neg | ceros | N_eff |
|---|---:|---:|---:|---:|---:|---:|
| versión (real) | 27 | 368 | 496/496 | 461 | **27** | 1.00 |
| versión barajada seed 0 | 27 | 390 | 496/496 | 496 | 0 | 1.00 |
| versión barajada seed 1 | 27 | 374 | 496/496 | 494 | 2 | 1.01 |
| versión barajada seed 2 | 27 | 371 | 496/496 | 496 | 0 | 1.00 |
| página 576 (secuencial) | 27 | 584 | 478/496 | 449 | 34 | 1.00 |

Destruir la coherencia de versión **no baja la saturación**. Si el formato
incremental fuera la causa, barajar tendría que moverla.

Lo que la produce es el tamaño, y sobre todo su **heterogeneidad**: los
tamaños de versión son muy desparejos (p10 232, p90 1027). Acumulando por
tamaño, **un solo texto** (1659 palabras, 11% del corpus) aporta **406 de
496** pares distintos; tres aportan 441; cinco, 492. Un informe largo barre
el campo él solo. Por eso `página 576` —textos parejos y más grandes en
mediana— satura *menos* (478): no tiene ese texto que barre.

**Dónde sí aparece la versión**: en los ceros. Los 27 por cancelación son
del corpus real; barajado quedan 0–2 y los 496 pares pasan a ser todos
negativos. La coherencia de versión es lo único que sostiene que algunos
pares aparezcan en los dos sentidos en cantidades iguales.

*(Code, Opus 5: tenía "versión" y "tamaño" como un solo objeto; son dos.)*

*Estado: verificado, 3 seeds de barajado.*

### 4.2 Alcance del corpus

*(delamor: no es un corpus representativo del dominio, de Devices.)*

Los informes son prosa técnica de un autor, revisada. El dominio del
proyecto es otro: **intercambio entre devices**. Lo medido acá vale como
prueba de volumen y como medición del instrumento, no como caracterización
del dominio.

Los **chats** serían el corpus del dominio, y no están disponibles todavía.
Condiciones previas que fija delamor, antes de cualquier ingesta:

1. **Revisión por temas personales.** Precede a todo lo técnico.
2. **Escritura errática** — las unidades tipográficas son todavía menos
   aplicables ahí que en los informes.
3. **Inglés y español mezclados** — medido, ver §4.3.

*Estado: **declarado**, no medido (salvo §4.3).*

### 4.3 El idioma mezclado — medido

*(delamor: el idioma es un tema. Mezclado, digo.)* Dentro del mismo texto,
no dos corpus distintos. Lo que sigue ya está ocurriendo, no es prospectivo.

**a. La lista unión se lleva términos del dominio, en los dos sentidos.**
`_STOPWORDS` es la unión NLTK-es + NLTK-en + sklearn-en. Cada lista aporta
sus propios falsos positivos:

| término | por qué se quita | qué es en CKM | ocurrencias |
|---|---|---|---:|
| `estado` | NLTK-es lo lista (participio de *estar*) | σ, el estado del campo | 84 en informes, 3 en caso13 |
| `estados` | ídem | ídem | 16 en informes |
| `system` | está en sklearn ENGLISH_STOP_WORDS | término de dominio | 0 en caso13 |
| `sentido` | NLTK-es | dirección / significado | 18 en informes |

`estado` es el caso claro: es el nombre del objeto central del modelo y el
extractor no lo ve. Ninguna de las dos listas fue hecha para prosa técnica,
y la unión suma los dos errores en vez de compensarlos.

**b. En texto mezclado el concepto se parte — y se parte asimétrico.**
caso13 es el único corpus mezclado de los medidos (172 de 2390 tokens, 7.2%,
se quitan por razón castellana):

| concepto | castellano | inglés | total real | lo que ve W |
|---|---|---|---:|---|
| estado / state | `estado` 3 — **quitado como stopword** | `state` 7 — **nodo** | 10 | 7, y sólo del lado inglés |
| señal / signal | `señal` 0 | `signal` 5 | 5 | 5 |
| sistema / system | `sistema` 2 | `system` 0 — sería stopword | 2 | 2 |
| error | 2 | 2 | 4 | 4 sumados (misma grafía) |

No es sólo que TF-IDF trate dos idiomas como dos términos que compiten por
el top_k. Es que **las dos listas no borran lo mismo**, así que una mitad
del concepto se elimina y la otra sobrevive: el nodo `state` de caso13 lleva
7 de 10 ocurrencias reales del concepto, y el desbalance no queda declarado
en ningún lado. `error` muestra el otro extremo: la grafía compartida los
fusiona sin que nadie lo decida.

**Consecuencia**: en un corpus mezclado, la frecuencia sobre la que se
selecciona el top_k no es la frecuencia del concepto. Es otra cosa más de la
rama de extracción que decide qué existe antes de que haya medición.

**c. Una palabra en un prompt decide qué existe en el campo.**
*(delamor: el argumento es que hay una palabra en los prompts de
configuración de los devices que resulta que está en español. Una. Y difiere
del inglés en una letra — corregido por él mismo: difiere en más.)* Es
`trazable`, en
`TINKER_GOAL_PROMPT` de caso13 — la única palabra no inglesa de los tres
prompts:

> `- Publish your map in the channel. Be precise. Be trazable.`

Sólo estaba en el prompt de TinkerBellucio. La cadena, verificada de punta a
punta:

```
una palabra: "trazable" vs "traceable" — 8 y 9 letras, distancia de
edición 2 (z→c, más una e insertada)
  → TinkerBellucio escribe su mapa entero en castellano (texto 20, 1043
    palabras: el texto MÁS LARGO del corpus)
  → activa 3 de 32 nodos (markopolus, peterplam, real — dos nombres de
    device y un cognado que se escribe igual en los dos idiomas)
  → aporta 3 pares de 496
  → W no contiene el mapa: contiene la conversación EN INGLÉS sobre el mapa
    (texto 24, 457 palabras, 11 nodos, 55 pares)
```

Caso14 aisló la variable: `trazable` → `traceable`, único cambio de texto, y
desapareció todo el castellano (n = 2).

Esto invierte §4.1. Ahí el texto más largo barría el campo él solo (406 de
496 pares); acá el más largo aporta 3. La diferencia entera es el idioma —
no el tamaño, no el formato, no el contenido. El device que puso la
sustancia se cayó del campo, y los que comentaron lo construyeron.

*Estado: **verificado** (a, b y c); no corregido.*

*(Code, Opus 5: hay dos hallazgos acá y no son el mismo. Que una palabra
cambie el idioma de salida ya estaba registrado en caso14. Lo nuevo es la
segunda mitad: que ese cambio de idioma determina qué entra a W. Un
parámetro de configuración de un device decide qué existe en el campo, sin
pasar por ninguna decisión del modelo.)*

---

## 5. La tensión no es criterio fuera de corpus adversariales

*(delamor: [el ruteo por marcadores aplica] sólo a corpus polarizados o
adversariales. Y: ¿qué hasta tensión? Ese no es un criterio aplicable.)*

TASK_W_corpus_informes dejó cerrado el mecanismo: sin negativos,
`force_w_pos` da N_eff = 2.00 exacto, y los negativos aparecen porque un
texto largo tiene más chance de contener un marcador de oposición:

```
largo del texto → chance de contener un marcador → pares negativos →
frustración → N_eff
```

Con el alcance que fija delamor, la lectura se completa: el ruteo por
marcadores traduce **postura adversarial**, y eso sólo existe en un corpus
polarizado. En los informes —y en el canal IAP, que no es un debate— el
mismo marcador ("pero", "sin embargo") es un **conector de discurso**, no
una oposición de postura. Los negativos medidos ahí no son tensión: son
prosa.

Consecuencias que quedan registradas, no resueltas:

1. **El canal IAP viene operando con W_mixta sin justificación de dominio**
   (caso09: 100 pares negativos; caso14: 481). No es un error de código: es
   un supuesto heredado del dominio adversarial donde el ruteo se diseñó.
2. **D_CKM_THRESHOLD = 0.40 fue calibrado sobre W_mixta adversarial**
   (AMP = 40). Aplicado a un W cuyos negativos son conectores, el umbral no
   tiene el referente con el que se fijó.
3. Néel (DEFS §15) y SALAMANCA (§16) pasan a ser el hilo: elicitar pares
   negativos sin que el largo del texto los produzca, y —antes— detectar si
   en un corpus dado existe estructura adversarial.

*Estado: alcance **decidido** (delamor); consecuencias 1 y 2 **declaradas**,
no verificadas.*

---

## 6. Lo que esto le hace a la unidad de texto

Ninguna de las tres unidades probadas es la del campo:

- **párrafo**: la mayoría de los textos no aporta pares (mediana 0); W se
  arma con la minoría larga.
- **página**: satura los pares distintos y produce negativos por longitud;
  el paisaje que aparece es el de la frustración de esos negativos.
- **versión**: satura del todo (496/496); los únicos ceros que quedan son
  cancelaciones. No ser tipográfica no alcanza: la unidad natural del
  trabajo no es la unidad natural de W.

La unidad tendría que definirse por cantidades de W —activación por texto,
saturación de pares distintos— y no por el formato del documento. Es
condición, no límite: un corpus de tweets, uno de blogs y uno de papers no
comparten unidad, y por eso tampoco comparten calibración.

---

## Abierto

- Qué valor de saturación es "lejos" — y si el criterio se fija sobre pares
  distintos, sobre ceros de W, o sobre N_eff directamente.
- **Ingesta incremental**: todo lo medido acá es una sola ingesta con
  rebuild suspendido. Con ingesta incremental la saturación es una
  trayectoria en el tiempo, no un número; falta medirla así.
- **Los parámetros de extracción no se persisten.** El JSON de
  `CorpusService.save()` guarda `texts`, `nodes`, `W`,
  `w_version_history`, `forced_w_pos` y `registro_borde`; **no** guarda
  `top_k`, `min_texts`, `rebuild_suspendido` ni la versión de stopwords.
  Un estado reabierto con otros parámetros continúa sin señal. Con ingesta
  incremental esto deja de ser inocuo.
- Si el canal debe seguir ruteando marcadores a negativos mientras no haya
  criterio de estructura adversarial.
- Los informes se describen a sí mismos (DEFS §19): sigue abierto si valen
  como referencia del instrumento o sólo como prueba de volumen.

---

## Estado

- §1, §2, §3 (medición), §4, §4.1: **verificado**
- §4.2: **declarado**
- §3 (criterio), §6: **propuesto**
- §5: alcance **decidido**; consecuencias **declaradas**

No cierra. Acota.

---

*Sep 2026 — Codespace ckm*
