# Metodología — proyecto TRUST

*v1 · 22 oct 2026 · gadanin.delamor + Claude Opus 5.5 (Cowork)*
*Forma tomada de `readme/METODOLOGY_v3.MD` (Claude Sonnet 4.6, sobre CKM). Caminos: imitar esa forma, buscar ejes, buscar nulos (delamor, 22 oct).*

*Cada afirmación lleva su fuente. Donde no hay fuente en un archivo, se dice. Lo que este documento no leyó está en §5.*

---

## 1. Ejes de la metodología

Como en CKM, la metodología no se declaró antes de usarse: se fue escribiendo mientras se usaba. La regla misma *"se precisó mientras se usaba"* (`registers/REG_regla_ckm_trust_v1.md:6`), y delamor lo nombra así: *"el protocolo es la interacción sucediendo"* *(dicho en conversación; no está en un archivo del repo)*.

**Eje 1 — La regla es el método.** La regla CKM TRUST es la forma de cada decisión del proyecto, no un componente del modelo:

```
1 el campo decide: criterio de campo con traza
2 si empata y hay traza, la traza decide
3 si no hay traza . porque no hay traza_? evaluar criterio de campo en 1
4 si empata o no hay traza -> desempate NULO.
  decide criterio de contexto (sesgo)
```
(`REG_regla_ckm_trust_v1.md:20-26`, textual de delamor). El intento que la sostiene: *"Que ninguna decisión pase por campo sin serlo. Donde el dato no decide, que se vea quién decidió"* (`:13`). Opera en el código (`services/ckm_trust_rule.py`, un solo corazón; `iap_chatroom/local_criterion.py` es su primera instancia en producción) y en el trabajo: a qué texto se le cree, qué se conserva de una versión a otra, quién decide.

**Eje 2 — Dudar es la actitud, no la falta.** *"Dudar como actitud de TRUST, no como falta. En pregunta, abriendo"* (`REG_regla:40`). El paso 3 es *"DUDA del criterio"*: volver a 1 no es re-aplicar, es dudar (`:33`). De ahí la pausa: **A1.PAUSA** reemplaza a "ALTO" desde el 13 oct — *"detenerse en pregunta, abierto… es exactamente lo que está siendo modelado. El INTENTO es habitarlo"* (`docs/opus/decisiones_en_el_acto_13a15oct2026.md`, 13 oct). Y el chequeo sin veredicto: *"El OK tapa el NO LO SÉ"* (`docs/tasks/PROTOCOLO_code_continuidad_v1.md:20`) → revisé / encontré / no pude revisar.

**Eje 3 — Declarar en vez de corregir u ocultar.** Lo que no se puede sacar sin decidir algo nuevo, se nombra con su impacto: *"un criterio casual que queda, queda dicho"* (`docs/defs/DECLARACION_extraccion_W_v2.md:64`). Un diseño que empuja a un resultado se declara como sesgo con su objetivo (consigna de `serie2_caso0`, `decisiones_en_el_acto.md`, 20 oct). Un default que nadie decidió *"no es una decisión"* y se arrastra visible (`PROTOCOLO:126`).

**Eje 4 — La traza con fecha no se reescribe.** Lo nuevo va en una entrada nueva; la traza vieja dice lo que dijo ese día (`decisiones_en_el_acto.md`, 21 oct: reversión de `9322256`). Las correcciones se registran como tales, incluidos los errores de cada instancia (lista de errores de Opus, `decisiones_en_el_acto_13a15oct2026.md`).

**Eje 5 — La confianza no es transitiva.** *"Este proyecto abordó que la confianza no verifica, al menos en principio, el carácter transitivo"* (delamor, 22 oct, `decisiones_en_el_acto.md`). Consecuencia de método: fuente primaria, no resúmenes de resúmenes; *"abarcar menos y apretar más"*. La delegación en árbol reparte tareas y **concentra la responsabilidad en device delamor** (misma entrada).

**Eje 6 — Un solo device delamor.** Las decisiones le llegan de a una, en serie; Opus decide por debajo de un umbral y escala por encima (E1–E6, `PROTOCOLO:54-59`); toda decisión se marca **en el acto** (`decisiones_en_el_acto.md`, encabezado). Las instancias (Opus, Code, Sonnet antes) no se ven entre sí: las une el repo y lo que delamor pega.

**Eje 7 — Medir sin interpretar.** *"Veamos qué miden, en vez de decidir qué miden"* (delamor, 19–20 oct). CKM interpreta modelos matemáticos y sus dinámicas, no significado (`decisiones_en_el_acto_13a15oct2026.md`, 14 oct). Un resultado se reporta con lo que **no** dice (p. ej. `registers/REG_iap_serie2_caso0_intento2_v1.md`: 0 disparos con umbrales sin calibrar no se leen).

**Eje 8 — El instrumento no está separado de lo medido.** *"Incluso el instrumento parece no estar tan definidamente separado de lo que es medido"* (delamor, 14 oct). Las separaciones *"no son de la cosa, son del que señala"* (`REG_regla:42`).

---

## 2. Nulos — qué hace la metodología con la ausencia

La palabra está en la regla: el paso 4 es el **desempate NULO** (`REG_regla:24`). La metodología trata la ausencia de cuatro maneras, y cada una tiene su fuente.

**2.1 El nulo como ausencia declarada.** Lo que no está entra como `None` **declarado ausente**, no como `0` ni `False`: *"la ausencia es el estado del observador, no un valor de la escala"* (`iap_chatroom/local_criterion.py:45-52`). `None` y `UNKNOWN` no se mapean entre sí (delamor, `docs/tasks/DECISIONES_opus.md:233`). Un candidato que el campo no pudo medir (NaN) no se cae "sin marca": queda nombrado y la duda sube (`services/ckm_trust_rule.py`, sección NaN).

**2.2 El nulo del desempate.** Cuando ni el campo ni la traza deciden, decide el contexto, y el contexto **es sesgo potencial**: sin paso 3, *"cada falta de traza va directo al 4 y el sesgo se presenta, subrepticiamente, como campo"* (`REG_regla:38`). El método no evita el sesgo: lo **nombra** (casillero `g`, `ckm_trust_rule.py`).

**2.3 El nulo como control.** Un procedimiento sin resultado nulo posible no verifica nada: el review de v28 lo señaló sobre el signo de W (`DECLARACION_v2:67`), y el CP-M lo midió: la marca de oposición no se distingue del azar en los corpus del repo, y se cerró **como declaración** (`decisiones_en_el_acto_13a15oct2026.md`, 14 oct noche).

**2.4 El nulo de la traza — lo que la traza no sabe.** Dos casos de este mes:
- **La única ausencia nombrada.** El paper decía *"COCO was never connected to the live IAP channel"* en tres lugares (v29, líneas 144, 281, 668) y no decía nada de otras ausencias del camino vivo (`firma_ckm` sólo a pedido; `gatekeeper_c1` sin importar). La frase era verdadera; el sesgo estaba en que era la única. Ninguna lectura lo vio, porque cada lectura verificaba lo escrito y ninguna lo no escrito (`decisiones_en_el_acto.md`, 21 oct).
- **El informe que dejó de escribirse.** El Informe de Trabajo llega a v32 (14 ago 2026); el paper siguió de v10_1 a v29 y las DEFs de v10 a v17 sin que el Informe lo registre (`docs/opus/INVENTARIO_versiones_paper_22oct2026.md`).

Sonnet lo había escrito para Δ_r: *"lo que no fue escrito no deja huella"* (`METODOLOGY_v3.MD`, §5). Vale para la traza del proyecto: **un grep encuentra presencias; la ausencia sólo aparece comparando** (delamor, 22 oct).

---

## 3. Diferencias con metodologías formales

**Con el método científico.** Las series de IAP son **testing, no experimentos** (delamor, 21 oct). Una corrida no es replicación (REG intento 2). Lo que tiene prueba matemática en la ciencia establecida va como referencia, nunca como corroboración propia; si no hay aporte, no se publica.

**Con la ingeniería de software.** Sin tests de regresión ni compatibilidad hacia atrás *"como si fuese un producto"*: *"la única versión del modelo que hay es la actual. el resto es imaginación"* (delamor, 14 oct). Lo viejo se reproduce desde su freeze en `process/`. Lo que sí se exige: **completitud** — un cambio que no mueve ningún test ni docstring no está cubierto (`readme/CONVENTIONS.md:83-97`).

**Con la gestión de proyectos.** No hay plan previo que se ejecute: hay checkpoints, cada uno con su pausa, y la tarea se evalúa contra el repo antes de ejecutarse (protocolo). La interrupción se da por supuesta: *"el trabajo se diseña para que cortar en cualquier punto no deje daño"* (`PROTOCOLO:6`).

**Con el trabajo con agentes.** El interlocutor no es herramienta: Opus *"no tiene que hacer lo que pide"* delamor — *"en medio de mi pedido y tu hacer, está tu decisión"* (dicho en conversación). Las consignas a los LLM son **pedidos, no órdenes con forma de condición** (21 oct).

---

## 4. Qué habilita y qué cuesta

**Habilita:** ver el sesgo donde se esconde mejor — en lo que encaja (*"lo sutil horada y se enquista"*, `REG_regla:44`). Que una decisión cortada por un reinicio no se pierda. Que COCO se conectara en un vivo (21 oct) por el camino declarado: el sesgo se puso en la entrada (canal, consigna), no en el instrumento.

**Cuesta:** volumen de traza (DECISIONES_opus, BANDEJA de >12.000 líneas, decisiones en el acto); el costo se trasladó a leerla, y por eso se parte (lo último sin lo anterior). Depende de la atención de delamor en puntos precisos. Y, como en CKM: no hay pipeline que otro equipo ejecute sin el estado del que formula. *"Si yo device delamor no intento, la mecanicidad resuelve"* (13 oct).

---

## 5. Lo que este documento no sabe

- **No leí** los documentos del proyecto claude.ai (`claude/…`, 28 sep–15 oct), que son la traza de TRUST anterior al 13 oct; ni el META REG, el MAPA REG, ni los Informes de Trabajo; ni el proyecto CKM. La metodología de antes del 4 oct (origen de la regla) queda sin barrer.
- Dos afirmaciones de §1 y §3 vienen de la conversación y no de un archivo; están marcadas.
- La redacción es mía: es el casillero `g` de este documento, nombrado.

---

*Las afirmaciones van trazadas a su fuente. Donde no hay traza, el documento lo dice o no afirma.*
