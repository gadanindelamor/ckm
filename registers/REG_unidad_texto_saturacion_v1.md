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
distintos. A diferencia de la tensión (§4), no premia el texto largo: crece
monótona con el largo hasta 100% y ahí deja de informar, de modo que el
criterio es *mantenerse lejos de la saturación*, no maximizar nada.

*Estado: verificado como medición; el criterio es propuesto, no decidido.*

---

## 4. La tensión no es criterio fuera de corpus adversariales

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

## 5. Lo que esto le hace a la unidad de texto

Ninguna de las dos unidades tipográficas es la del campo:

- **párrafo**: la mayoría de los textos no aporta pares (mediana 0); W se
  arma con la minoría larga.
- **página**: satura los pares distintos y produce negativos por longitud;
  el paisaje que aparece es el de la frustración de esos negativos.

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

- §1, §2, §3 (medición): **verificado**
- §3 (criterio), §5: **propuesto**
- §4: alcance **decidido**; consecuencias **declaradas**

No cierra. Acota.

---

*Sep 2026 — Codespace ckm*
