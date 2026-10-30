# Lo que tenés que definir vos, delamor — 30 oct 2026 (Opus 5.5)

*Sin códigos para buscar: cada ítem dice qué es, dónde está y qué hay que decidir. Antes de listar algo, Opus lo buscó en `docs/opus/decisiones_en_el_acto.md`, `docs/tasks/DECISIONES_opus.md` y la BANDEJA. Lo que ya estaba decidido va en la parte A, para que no vuelva a pedirse.*

---

## A. Lo que Code te reclama: **ya está decidido**. No tenés que hacer nada
Code lo sigue viendo abierto porque lee `DECISIONES_opus.md` y estas decisiones quedaron en `decisiones_en_el_acto.md`, el registro de Opus. El texto 22 se las pasa, pero todavía no corrió: espera al Codespace.

1. **El archivo suelto con una línea de tick** que apareció en el estado del canal. Lo resolviste el 27 oct; Code lo movió a `process/`.
2. **Qué declara IAP y qué los drivers:** el registro de providers, la lista de archivos de estado de una corrida y el puerto. Lo decidiste el 27 y el 28 oct: *"un driver de test lo sabe; hay que llevar ese knowhow a IAP"*, y para el resto, *"ídem, sigue esa lógica"*. Se implementa con el texto 19.
3. **Si el `--check` del caso 0 tiene que dejar el estado como lo encontró.** Decidido el 28 oct: no hace `--reset` y usa su propio directorio. Se implementa con el texto 19.
4. **Si los 3 tests que usan la W del último vivo se anclan a una copia fija.** Decidido el 28 oct: sí, a la copia en `process/`. Se implementa con el texto 17.
5. **El empate del código** (h = 0 calculado con decimales). Decidido hoy: las dos cosas, que el código cumpla la regla y que el paper declare cómo se calcula.

## B. Lo que Opus había listado como tuyo y **ya estaba decidido** (me corrijo, A3)
6. **El nombre "expulsados":** el 10 oct dijiste *"nada es expulsado"* y *"no se renombra nada"*. El v35 lo aplica: el código conserva `expulsados` y el paper dice "rechazado en todas las fases".
7. **Los prefijos del Orden BABEL** (E1–E4, D1–D3…): el 5 oct dijiste *"descubramos nosotros algún patrón… veremos"*. Queda en esperar el patrón.
8. **Si §7.6 (la representación del conocimiento) va en el paper:** *"sí va"* (23 oct) y *"SI ENTRA"* (29 oct). El review la critica; eso cae en el punto 15.
9. **El campo:** *"el campo es continuo; lo que salta es la medición"* (23 oct), y las W son representaciones (10 oct). Está decidido. El review encontró que el paper usa "field" también para W y para el canal. Ver el punto 14.

---

## C. Lo que sí hay que definir. Orden: instrumento, paper, IAP, infraestructura

### Instrumento
10. **Cuándo "separa" calibrate.**
    - *Hoy:* compara los dos extremos del camino (la W sin tocar y la W colapsada). Separa si el colapso da más distancia que la W sin tocar.
    - *La alternativa:* usar el máximo de la curva, que el código ya registra pero no usa.
    - *Lo que cambia:* con los extremos, separar es comparar N_eff(W) con un número fijo F(N), que no depende de W (lo señaló el review). Con el máximo, depende del interior del camino. En el intento 3, con el máximo separan los 3 rebuilds en vez de 1.
    - *El riesgo:* el máximo de puntos muestreados se infla por ruido.
    - *Qué decidir:* nada todavía. Primero Code mide la curva exacta (por enumeración) de las 16 W, y con eso decidís. Fuente: `REVISION_DEFS_v20_…_30oct2026.md` §9.
11. **Si `services/analytics.py` pesa cada atractor por su masa.**
    - *Hoy:* la co-presencia, los clusters, las oposiciones y node_presence se calculan sobre atractores únicos, todos con el mismo peso.
    - *Lo que ya decía el documento de criterios del 11 sep:* pesar es necesario; sin peso se hereda el sesgo del conteo.
    - *Qué decidir:* sí o no. Recomendación de Opus: sí. La versión con peso ya existe en el driver de Néel.
12. **Si "no se renombra nada" (10 oct) vale también para** OPERADOR_STOP_COCO en el código, Gatekeeper y los verbos de "agregar un nodo" (activar / incorporar). Hoy figuran como abiertos. *Qué decidir:* si vale para todos, se cierran.

### Paper
13. **Si SALAMANCA y Néel entran al paper.**
    - *Qué son:* SALAMANCA busca si W tiene dos regiones separadas. Néel mide si esa frontera tiene profundidad.
    - *Lo medido:* SALAMANCA está registrado y encontró módulos, no posiciones enfrentadas. Néel se corrió el 20 sep y dio profundidad cero. Los dos pueden devolver "no hay nada", y lo hicieron.
    - *Lo que les falta:* Néel tiene un solo corpus y no hay control positivo.
    - *Qué decidir:* entran, o no.
14. **"field" en el texto.** El concepto está decidido (punto 9). Lo que falta es que el texto use "field" sólo para el campo, y otro nombre para W ("the representation") y para el canal. *Qué decidir:* si Opus pasa el texto así. Toca §3 y §7, que son tu voz.
15. **§3.3 y §7.6.** El review dice que la *"verificación por convergencia independiente"* (§3.3) no es una verificación, y que *"representar conocimiento y medir el campo son dos perspectivas de lo mismo"* (§7.6) no tiene argumento en el texto. *Qué decidir:* (a) quedan como están, declarados como tuyos; (b) se fundamentan; (c) salen.
16. **Contra qué estimadores se ubica el aporte.** El review pide comparar N_eff con los estimadores de riqueza de especies (Chao1, Good–Turing), no sólo con el conteo crudo. *Qué decidir:* (a) se mide (Code); (b) se cita como trabajo futuro; (c) no se hace.
17. **Si los criterios de "W sola"** del documento del 11 sep entran al paper: el índice de frustración (el paper ya lo usa para fourforums sin nombrarlo), el espectro y la distinción topológico / métrico.
18. **La literatura de representación del conocimiento 2023–2026:** quién la revisa y cómo. De eso depende la afirmación de §7.6 sobre KR.
19. **Los Acknowledgments**, que son tu voz. Hoy dicen que verificaste todas las referencias, y la verificación todavía no está hecha. Tampoco nombran a Claude Opus 5, el modelo con el que Code corrió los experimentos. *Qué decidir:* cómo lo decís.

### IAP
20. **El OK para pasar el registro del intento 5 a `registers/`.** Va después de que Code lo corrija (texto 22).

### Infraestructura
21. **El Codespace:** esperar el próximo ciclo de facturación o subir el presupuesto (la hora de 2 núcleos cuesta USD 0,18). Hasta que vuelva, esperan: el texto 22; el empate (punto 5); la curva exacta de calibrate (punto 10); §5.2 con la extracción de hoy.

---

*Lo que Opus decide solo (las correcciones del review que no tocan lo tuyo, las DEFS v21, los textos para Code) está registrado en `decisiones_en_el_acto.md` y no te llega como pendiente.*
