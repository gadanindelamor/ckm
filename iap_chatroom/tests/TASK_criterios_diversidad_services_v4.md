# TASK_criterios_diversidad_services_v4.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Agrega un paso que v3 salteaba. Todo lo demás se lee de v3 → v2 → v1.*

---

## Lo que v3 salteaba

*(Corrección de delamor, Sep 2026)*

v3 clasificaba cada divergencia y ofrecía dos salidas — estandarizar o
escribir la razón. Faltaba el paso del medio:

> El criterio mira hacia atrás **desde acá**, y **no invalida** las
> divergencias ya declaradas. Por lo cual hay que **comprender la
> deliberación** y **luego** proponer.

Dos cosas, y las dos importan:

**1. No es una purga.** `count_seed` y `weighted/boltzmann` quedaron
clasificadas como deliberadas en v3 y **siguen válidas**. Aplicar el
criterio hacia atrás no las pone en duda ni las reabre.

**2. Ausencia de razón escrita no es ausencia de deliberación.** Que no
esté escrita significa que no dejó rastro *en el código*. Puede haber
dejado rastro en otra parte, o puede no haber existido. Son estados
distintos y hay que distinguirlos antes de proponer cualquier cosa.

---

## El paso que va en el medio — comprender la deliberación

Para cada divergencia sin razón en el código, **antes** de proponer `E` o
`R`, reconstruir desde la traza del propio repo. No preguntando, no
suponiendo: midiendo.

**Método:**

1. `git log --reverse -S"<el valor exacto>"` sobre los archivos — cuándo
   nace el valor, en qué commit, en qué servicio.
2. Qué REG introdujo o midió ese valor, y con qué fecha.
3. **Comparar las dos fechas.** Si el valor es anterior a la deliberación
   que hoy justifica su contraparte, no hay deliberación que comprender
   del lado del valor viejo: hay un default puesto antes de que la
   pregunta existiera.
4. Si el valor es posterior a la deliberación y difiere igual, entonces sí
   hubo una decisión y hay que encontrarla antes de tocar nada.

Los dos casos se ven distintos y llevan a propuestas distintas. Sin el
paso 3 se confunden.

---

## Ejemplo trabajado — `n_runs` 50 vs 80

Reconstrucción, no supuesto:

| cuándo | qué | fuente |
|---|---|---|
| 2026-05-28 | `MonitorService` nace con `n_runs_attractors: int = 50`, sin razón. En el mismo commit `FabricationService` nace con `n_runs=100` | `6d563fd` |
| 2026-06-05 | `COCO` nace con `n_runs = 80`, ocho días después, otro servicio, otra sesión | `28ec9de` |
| Ago 2026 | aparece la deliberación sobre `n_runs`: el sweep, `REG_stochastic_eval_v1/v2`, `REG_n_runs_sweep_armstrong_v1`, `REG_count_attractors_bias_v1` | REGs |
| Ago 2026 | de esa deliberación sale la razón que hoy tiene el 80: *"no cambiar sin revisar el hallazgo del sweep n_runs 60→70"* | `coco.py:134-136` |

**Lectura:** el 50 es **anterior a la deliberación**, por tres meses. No hay
una deliberación que comprender del lado del 50 — hay un default puesto
antes de que la pregunta existiera. La deliberación sí existe, ocurrió
después, y alcanzó a **una sola de las dos copias**.

Tres estados, no dos. Y el tercero es el frecuente:

- **deliberada** — razón escrita, y dónde se ve
- **deliberación posterior no propagada** — la deliberación existe y está
  registrada, el valor viejo quedó afuera de su alcance
- **deriva** — ninguna deliberación, en ningún momento

---

## Qué propuesta sale de cada estado

**Deliberada** → nada. No se toca.

**Deliberación posterior no propagada** → la propuesta no es inventar una
razón para el valor viejo ni estandarizar por simetría. Es **traer el valor
viejo al alcance de la deliberación que ya ocurrió**. Dos formas, y la
elección es de delamor:

- adoptar el valor que la deliberación respalda, con su razón y su
  referencia al REG; o
- declarar por qué este servicio queda **exceptuado** de esa deliberación —
  lo que es una afirmación sobre qué es el servicio, no sobre el número.

**Deriva** → recién acá aplican las dos salidas de v3 (`E` estandarizar /
`R` escribir la razón), y sólo si la razón fue enunciada por delamor o
existe en un REG.

---

## Lo que Code hace en el Paso 1, actualizado

**Hace:** el censo, la reconstrucción por traza de cada divergencia sin
razón escrita, la clasificación en los **tres** estados, y la propuesta que
corresponde a cada estado. Reporta y se detiene.

**No hace:** elegir entre las formas. Ni inventar una deliberación que la
traza no muestra. Si la traza no alcanza para distinguir "deliberación
posterior no propagada" de "deriva", se reporta como
**indistinguible por la traza** y se pregunta — no se elige la lectura más
cómoda.

---

## Bloqueo explícito, adicional

- Clasificar como deriva sin haber hecho la reconstrucción por traza →
  **detener**. Es el paso que v3 salteaba, y saltearlo produce una
  propuesta sobre un estado que no es el real.
- Tratar el criterio como una purga de lo ya declarado → **detener**. No
  invalida nada hacia atrás.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: v3 (criterio de divergencia deliberada y censo), v2 (pasos y
field check), v1 (contexto y medida canónica)*
