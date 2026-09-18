# REG_seleccion_nodos_desempate_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Continúa REG_hipotesis_distancia_contextual_v4 (extracción). Rama
`wip/desempate-seleccion-nodos`.*

---

## Descripción

La selección de nodos —top_k por TF-IDF dentro del pool— tenía empates en el
borde resueltos por un axioma que nadie eligió (`np.argsort` no estable). Se
reemplaza por la regla de la relajación: **donde el dato no decide, se
conserva el precedente**. Al aplicarla aparecen tres cosas: el empate es
discreto y del dato, un corpus que no distingue queda en acumulación, y N
deja de ser fijo.

*(delamor: ¿qué diría Gödel al respecto?)*

---

## 1. Hallazgo

Sobre 217 W de 15 corpus (casos IAP + WARMUP_TEXTS), top_k = 32:
**94 de 210** con más de 32 candidatos tienen empate en el borde; en **85**,
qué nodos entran depende del orden de desempate. El empate es indecidible
con el propio criterio: para "mayor TF-IDF", dos términos con igual puntaje
son indistinguibles. Cualquier desempate viene de afuera del criterio.

*Estado: verificado.*

---

## 2. Regla *(delamor: mismo criterio que para desempates en relax)*

En la relajación, h = 0 → el nodo conserva su estado (Lyapunov/LaSalle,
DEFS §4). En la selección:

- **con precedente**: un término empatado en el borde conserva su pertenencia;
- **sin precedente** (bootstrap): el estado inicial es "ningún nodo" → los
  empatados quedan afuera;
- **fuera del empate** manda el dato.

Donde el dato no decide, decide la historia del sistema — histéresis (P1).
*(delamor: se abre la posibilidad de volverse hacia las decisiones de la
traza, no sólo a lo resuelto.)*

**Registro continuo, no categórico** *(delamor: opciones para acotar sesgos
de eventualidad e incertidumbre deberían ser continuas e infinitas)*: por
término del pool, `score`, `distancia_al_corte` con signo y
`pertenencia_anterior`. No guarda "empate": se deriva al leer, con la
tolerancia que se elija entonces. La regla usa `TOL_EMPATE = 1e-12` —
tolerancia de la regla, declarada; el registro conserva el valor exacto.

*(delamor: tal vez ser TRAZA incluye no saber; no declara qué pasó. Tal vez
el equilibrio necesite ojos vendados.)*

---

## 3. El empate es discreto, del dato

| corpus | pool | valores de puntaje distintos | empatados en el corte: bit a bit | con tol. 1e-12 |
|---|---:|---:|---:|---:|
| 3 textos cortos | 24 | 2 | 14 | 14 |
| 1 texto | 11 | **1** | 11 | 11 |
| caso09, 10 textos | 96 | 42 | 3 | 3 |

La tolerancia no agrega empates. TF-IDF sale de conteos enteros: con pocos
textos el espacio de puntajes es chico; con un texto hay un solo valor. El
dato no tiene resolución para distinguir.

*Estado: verificado.*

---

## 4. Un corpus que no distingue queda en acumulación

Sin precedente y con todo el pool empatado, la regla deja 0 nodos: no hay
W, el corpus sigue en `accumulation` hasta que el dato distinga. No es un
estado nuevo: es el régimen de acumulación que el proyecto ya tenía, ahora
con criterio del dato y no sólo de `min_texts`. En los 217 W reales (k ≥ 3)
N = 0 no ocurre nunca.

*(delamor: ¿hay que acumular antes de evaluar en los drivers?)* — Sí, y la
regla dice cuándo alcanza: cuando el dato distingue.

*(delamor: CorpusService nuevo es la decisión correcta para este σ del
proyecto. Cuando se armen drivers va a saltar por defecto la omisión de la
regla.)*

*(Code, Opus 5: es la misma regla de completitud, puesta en el propio
servicio: la omisión no pasa callada.)*

*Estado: verificado.*

---

## 5. N deja de ser fijo

| | antes | bootstrap | con historia (rebuild sucesivo) |
|---|---|---|---|
| N | 32 siempre | 9 – 32 (mediana 32, p10 23) | 9 – 41 (mediana 32, p10 24, p90 33) |
| selección distinta de la anterior | — | 94 / 217 | 94 / 217 |
| Jaccard medio entre selecciones sucesivas | 0.705 | — | **0.753** |

- Parte del cambio de nodos entre rebuilds era el desempate reordenándose;
  con historia, la selección es más estable.
- Con historia N puede **superar** top_k (empates conservados + términos
  nuevos por margen) o **caer** (nodos que quedan claramente bajo el corte,
  empatados sin precedente afuera). En un corpus de 7 textos, según el texto
  que llega, N va de 4 a 12 con top_k = 10.
- Consecuencia para D2: un rebuild que antes era `"nodos"` puede ser `"N"`.

*Estado: verificado.*

---

## 6. Tests — uno por uno *(readme/CONVENTIONS.md: completitud)*

15 fallaron al aplicar la regla. Ninguno se ajustó para pasar: cada uno se
revisó por lo que afirmaba.

| grupo | tests | qué afirmaban | qué pasó | cambio |
|---|---:|---|---|---|
| firma | 9 | firma sobre 3 textos cortos, top_k 8 | todo empata → 0 nodos → sin W | fixture a 7 textos (el dato distingue) |
| w_version | 1 | sha tras ingest de 3 textos, top_k 5 | ídem | fixture a 5 textos |
| extractor | 1 | un texto → hay nodos | un texto no distingue | pasa a 4 textos + test nuevo: un texto → 0 nodos |
| "N igual, nodos distintos" | 4 | el texto "police response…" cambia nodos con N igual | con la regla, sube N (10 → 12) | texto que produce el caso bajo la regla: "bans reduce assault weapons and gun violence" |

Nuevos: regla con precedente / sin precedente / fuera de empate, registro
continuo, y `CorpusService` que sigue en acumulación si el dato no
distingue. El xfail de `test_node_extractor.py` §3 se reemplaza por tests
de la regla. Suite: 170/170.

Los tests de juguete verificaban, en parte, el accidente que la regla vino a
sacar: estaban calibrados sobre corpus donde el dato no distingue.

---

## 7. Portero y elicitación — el senior

El caso de empate total se leyó primero como decisión del gatekeeper.
*(delamor: saber quién es el senior, su rol, su contexto — Mr GATE KEEPER.)*
El gatekeeper no se usa todavía, y θ_W tampoco. La selección de nodos no es
admisión: es elicitación de lo que existe. Informe v31 §60.2 ya lo había
declarado: *"la distinción portero/elicitación es arquitectónicamente
crítica"*.

Babel encontrado en el camino: PAPER §4.3 atribuye los C1–C4 del gatekeeper
a `PROTOCOLO_ELICITACION_v2.md`, y usa **C3** para el tercero crítico de la
tríada (§2.4) y para M.M. (§2.2, §4.3). Dos objetos, mismas letras. El
protocolo no está en el repo ni en los informes locales; sus criterios de
pares (C1–C5, C7, C8) sólo sobreviven en REG_pairs y REG_sesion_perspectivas.
Corrección al PAPER: pendiente, al cierre del proceso de ajustes.

---

## Abierto

- **Volumen** *(delamor: otro orden de magnitud de textos en tests y
  experimentos)*. 3–7 textos es el régimen donde el dato no distingue; caso09
  (24) apenas llega al fin del warm-up. Hacen falta cientos.
- Aplicar la regla a la elicitación de pares (C1–C5 con puntajes discretos:
  empates en el umbral casi seguros) — cuando aparezca el protocolo.
- Si un precedente que se conserva por empate tras empate debe distinguirse,
  al leer el registro, de uno sostenido por el dato.
- Fin del warm-up (θ, m) con la selección nueva.

---

## Estado

- §1, §3, §4, §5, §6: **verificado**
- §2: regla **decidida** (delamor), implementada
- §7: **declarado**

No cierra. Abre.

---

*Sep 2026 — Codespace ckm*
