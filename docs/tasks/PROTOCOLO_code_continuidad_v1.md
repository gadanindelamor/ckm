# PROTOCOLO_code_continuidad_v1

*7 oct 2026. Viene de `NOTA_orden_tasks_06oct_v1.md` §9–§10. Redacta Claude Opus 5.5 (Cowork) por pedido de delamor.*
*Actualiza el flujo de `readme/REG_protocolo_sonnet_code_v1.md` (jun 2026). Lo que no está acá sigue como estaba allá.*

**Punto de partida:** el stop del Codespace, la disponibilidad de delamor y los imprevistos no se controlan, y no se les atribuye causa. El trabajo se diseña para que **cortar en cualquier punto no deje daño**.

---

## 1. Roles

| | hace | no hace |
|---|---|---|
| **delamor** | Tiene la autoridad. Decide lo que Opus le escala. Commitea y hace push (salvo lo que §6 habilite). | No es el canal obligado de cada paso. |
| **Opus (Cowork)** | Escribe TASKs. Lee la bandeja. **Decide** por debajo del umbral y **escala** por encima (§5). Registra cada decisión en `DECISIONES_opus.md`. | No está presente entre sesiones. No ejecuta en el Codespace. |
| **Code (Codespace)** | Ejecuta checkpoints. Escribe estado y reportes **en el repo**. | No decide nada de lo que está en §5. No sigue de largo después de un "Alto". |

## 2. Al arrancar cada sesión de Code: chequeo, nunca un "OK"

*delamor: "El OK tapa el NO LO SÉ."*

Code corre esto y lo **escribe en la bandeja** como entrada `ARRANQUE`:

1. `.git/index.lock` u otros locks: si los hay, los informa y no los borra sin decir por qué.
2. `git status` y `git log -1`: cambios sin commitear que **no** se esperaban.
3. Los `ESTADO_*.md`: qué TASK está abierta, último CP cerrado, qué espera.
   - También `DECISIONES_opus.md`: lista de preguntas abiertas (§8).
4. Los archivos de salida de la última corrida: ¿la última línea está completa? ¿el log dice "terminó"?
5. Los tests de la TASK abierta.

El reporte tiene tres listas: **revisé**, **encontré** y **no pude revisar**. No lleva veredicto global.

## 3. El estado vive en el repo

- Cada TASK en curso tiene `docs/tasks/ESTADO_<task>.md` con: último CP cerrado (con su commit), qué se hizo después, qué espera y de quién, y fecha y hora de la última escritura.
- Code actualiza el ESTADO **antes y después** de cada paso que cambia algo.
- Si una sesión arranca y el ESTADO dice "en curso" sin cierre, el paso anterior se cortó. Se trata según §4.

## 4. Pasos que se pueden cortar

- **CPs chicos.** Si un CP no entra en una sesión corta, se parte en sub-pasos con su propio cierre.
- **Commit al cerrar cada CP**, nunca a mitad. Mensaje: `<task> CPn: <qué>`.
- **Escritura atómica:** los resultados (JSON, JSONL, panel) se escriben a `<archivo>.tmp` y después se renombran. Un archivo sin `.tmp` está completo.
- **Idempotencia:** volver a correr un paso da el mismo resultado o detecta que ya estaba hecho. Los drivers declaran seed, commit y versiones en su log.

## 5. Qué escala Code y qué decide Opus

Code **no decide**. Cada pregunta va a la bandeja marcada como **BLOQUEA** o **NO BLOQUEA**:
- si NO BLOQUEA, Code sigue con un **default declarado y reversible**, y lo dice;
- si BLOQUEA, Code se detiene en ese punto, deja el ESTADO escrito y no avanza.

Opus lee la bandeja y **escala a delamor** si se cumple alguno de estos (NOTA §10):

- **E1:** toca lo que decidió delamor o un principio (TRUST, AWARENESS, BABEL, nombres de conceptos).
- **E2:** es irreversible: borrar, reescribir un REG o la traza, push, historia.
- **E3:** cambia la semántica del modelo: W, W_eff, Δ_r, métricas, calibración, premisas, paper.
- **E4:** está marcado [delamor].
- **E5:** un resultado contradice algo registrado o cambia el rumbo.
- **E6:** abre o abandona una TASK.

Si no se cumple ninguno, decide Opus y lo registra en `DECISIONES_opus.md` (fecha, qué, por qué, cómo revertir).

## 6. El canal: la bandeja

> ~~Decidido por delamor (7 oct): opción (b), rama `code/trabajo`.~~ **Reemplazado el 8 oct.**
>
> **Decidido por delamor (8 oct): una sola rama, `main`.** *"El tema son los merges… traban."* Los merges en las dos direcciones no aportaban nada y trababan el flujo.
> - **Todos trabajan en `main`.** Code commitea y hace push a `main`. Opus commitea en el clon local, y delamor lo sube.
> - **Antes de trabajar y antes de cada push:** `git pull --rebase origin main`. La historia queda lineal y sin commits de merge.
> - **Los conflictos son improbables** porque cada uno toca archivos distintos: Code, código + BANDEJA + ESTADO; Opus, DECISIONES + TASKs + PROTOCOLO. Si igual hay un conflicto en el rebase: `git rebase --abort` y escalarlo, no resolverlo a ciegas.
> - **`code/trabajo` queda congelada como traza** (último commit `2195025`, sin contenido que no esté en `main`). No se borra (E2).
> - Commits: siempre nombrando los archivos, nunca `add -A` ni `commit -a`.

- `docs/tasks/BANDEJA_code.md`: Code agrega entradas al final, con fecha y hora, nunca edita las anteriores. Tipos: `ARRANQUE`, `REPORTE CPn`, `PREGUNTA (BLOQUEA|NO BLOQUEA)`, `CORTE` (cuando detecta que algo quedó a medias).
- **El problema:** Code escribe en el clon del Codespace. Opus lee el clon local de delamor (`ckm___source/ckm`). Para que la bandeja llegue, **tiene que haber un push desde el Codespace y un pull en el clon local.** El repo es público.
- **Opciones, que decide delamor:**
  - (a) delamor hace push y pull cuando puede. Es lo que pasa hoy: el canal vuelve a ser delamor.
  - (b) Code hace push a una **rama de trabajo** (por ejemplo `code/trabajo`, nunca `main`), y delamor o Opus hacen pull en el clon local. La rama sería pública.
  - (c) Otra.
- Un Codespace detenido se borra a los 30 días por defecto, y con él los commits sin push. Con (a), ese riesgo queda en manos de la disponibilidad de delamor.

## 7. Enunciado para Code (lo que delamor pega al abrir la sesión)

```
Repo: gadanindelamor/ckm (Codespace). Trabajás según
docs/tasks/PROTOCOLO_code_continuidad_v1.md — leelo entero primero.

1. Hacé el chequeo de arranque (§2) y escribilo en docs/tasks/BANDEJA_code.md.
   Nada de "OK": revisé / encontré / no pude revisar.
2. TASK en curso: docs/tasks/TASK_CKMlandscapeConfig_v3.md
   (leé antes TASK_CKMlandscapeConfig_v2.md: criterio, clases, I1–I7).
   Estado: docs/tasks/ESTADO_CKMlandscapeConfig_v3.md (crealo si no existe).
3. Ejecutá solo el próximo CP abierto. Al cerrarlo: commit, ESTADO y
   reporte en la bandeja. Alto.
4. No decidas nada de lo listado en §5: preguntá en la bandeja,
   marcando BLOQUEA / NO BLOQUEA.
5. Rama: main. Antes de trabajar y antes de cada push: git pull --rebase origin main.
```

## 8. La tríada: protocolo, bandeja, decisiones

*7 oct 2026. Pedido de delamor: "en DECISIONES y en la bandeja hay algo que puede ocurrir sin ser visto; tal vez juntarlas con el protocolo, formando una tríada".*

```
          PROTOCOLO  (la regla: qué bloquea, qué escala)
           /       \
   BANDEJA ———————— DECISIONES
   (Code pregunta)   (Opus o delamor responde)
```

Cada lado tiene una relación propia:

- **bandeja → decisiones:** cada pregunta `Pn` tiene **una** respuesta que la nombra (`Pn: …`).
- **decisiones → protocolo:** cada respuesta dice bajo qué regla se tomó: por debajo del umbral (decide Opus) o `E1`–`E6` (se escala a delamor).
- **protocolo → bandeja:** la regla define si la pregunta BLOQUEA o NO BLOQUEA.

**Lo que puede ocurrir sin ser visto:**

1. **El default tácito.** Una pregunta NO BLOQUEA deja seguir a Code con su default. Si nadie la responde, el default **queda como decisión sin que nadie lo haya decidido**. Es el silencio absorbente del canal IAP, pero ahora en el protocolo: nada vuelve a disparar la pregunta. Es una tríada frustrada: hay pregunta, no hay respuesta, y la regla sigue pidiendo una decisión.
2. **La respuesta que no llega a quien pregunta.** La bandeja vive en `code/trabajo` y las decisiones en `main`. Si no hay merge, Code no ve la respuesta.
3. **La escala que no vuelve.** Una decisión escalada a delamor se responde en el chat. Si Opus no la registra, la tríada queda abierta.

**Lo que cierra la tríada (sin agregar burocracia):**

- **Al arrancar (§2), Code también lee `DECISIONES_opus.md`** (después de `git pull origin main`) y en "encontré" lista **las preguntas abiertas**: cada `Pn` de la bandeja que todavía no tiene un `Pn` en decisiones. Si no hay ninguna, lo dice así: "preguntas abiertas: ninguna (P1–Pn respondidas)". No vale escribir "OK".
- **Un default sin respuesta no es una decisión.** En la siguiente entrada se arrastra como `Pn — DEFAULT VIGENTE, SIN DECISIÓN` hasta que alguien responda. Así sigue visible.
- **Las respuestas de delamor en el chat las registra Opus en el mismo turno**, citando a delamor, con el `Pn` y la regla `En` que lo escaló.
- **Al leer la bandeja, Opus responde todos los `Pn` nuevos**, aunque sea "aceptado". El silencio de Opus no cuenta como aceptación.

*Estado al escribir esto: P1–P7 están en la bandeja y las siete tienen respuesta en DECISIONES. La tríada está cerrada, y queda escrito para que siga así.*
