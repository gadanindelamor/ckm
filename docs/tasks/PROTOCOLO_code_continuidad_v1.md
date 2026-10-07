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

> **Decidido por delamor (7 oct): opción (b), rama `code/trabajo`.** Code trabaja y hace push **solo** a `code/trabajo`, nunca a `main`. Opus lee la rama con `fetch` desde el clon local. Pasar algo a `main` lo decide delamor (E2).

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
5. Rama: code/trabajo. Push solo a code/trabajo, nunca a main.
```
