# TASK_criterios_diversidad_services_v5.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Corrige la resolución de v4. Todo lo demás se lee de v4 → v3 → v2 → v1.*

---

## La regla

*(delamor, Sep 2026)*

> El criterio aplica **desde aquí en adelante**. Si hay una deliberación
> previa, **no se deja ni se cambia**. Primero comprender.

Las dos acciones disponibles quedan **suspendidas**, no una de las dos.

---

## Qué corrige de v4

v4 daba una tabla de resoluciones:

```
Deliberada                              → nada. No se toca.
Deliberación posterior no propagada     → traerla al alcance
Deriva                                  → E o R
```

Las dos primeras filas están mal por el mismo motivo: **ya proponen una
acción**. «No se toca» es *dejarla*. «Traerla al alcance» es *cambiarla*.
Ambas ejecutan sobre algo que todavía no se comprendió.

La tabla correcta, donde hay deliberación previa, tiene una sola fila:

```
hay deliberación previa  →  ni dejar ni cambiar. Comprender. Reportar. Detenerse.
```

---

## Por qué «dejarla» no es la opción segura

Es la que parece segura y es la que produjo el estado actual.

`n_runs = 80` en COCO **tiene su razón escrita**, con referencia al sweep
60→70. Por eso se ve resuelto. Y precisamente porque se veía resuelto,
nadie trajo el `50` de MonitorService al alcance de esa deliberación
durante tres meses. La razón escrita no fue comprendida — fue archivada.

Dejar quieto lo que tiene razón escrita es el mecanismo por el cual una
deliberación se congela y, con el tiempo, se vuelve indistinguible de una
deriva. Es la misma forma que las 7 copias de `_relax` y que el `43/43` del
README: cada copia correcta en su momento, ninguna sabiendo de las otras.

---

## La reconstrucción por traza no es la comprensión

Corrección de Code sobre v4, para que no se lea mal.

El método de v4 —`git log -S` sobre el valor, qué REG lo introdujo,
comparar fechas— produce **material**: cuándo, dónde, en qué commit, en qué
orden. Eso es verificable, es lo que Code puede hacer, y es necesario.

**No es la comprensión.** v4 lo presentó como si cerrara el asunto: daba la
reconstrucción y de ahí saltaba a una propuesta. El salto es el error. La
reconstrucción es lo que le da algo sobre lo que trabajar a la comprensión;
no la sustituye ni la produce.

Consecuencia operativa: cuando Code termina la reconstrucción, **no sigue**.
Reporta el material y se detiene. No hay en esta TASK ningún paso donde
Code proponga una acción sobre una divergencia con deliberación previa.

Esta TASK no define qué es comprender ni da un procedimiento para
comprender. Definirla la mecaniza.

---

## Lo que Code hace en el Paso 1, final

1. Censo de copias vivas (v2 §1.a, 1.b).
2. Clasificación por el criterio de v3 — razón escrita **y** dónde se ve.
3. Reconstrucción por traza de cada divergencia, con o sin razón escrita
   (v4). Fechas, commits, REGs, orden.
4. **Reportar el material y detenerse.**

Lo que sigue no lo decide Code, y no es una elección entre opciones que
Code pueda enumerar de antemano.

Único caso donde el Paso 1 **sí** avanza sin esperar: divergencias donde la
reconstrucción muestra que **no hubo deliberación en ningún momento** —
deriva pura. Ahí aplican `E` o `R` de v3, y `R` sólo si la razón fue
enunciada o existe en un REG. Si la traza no alcanza para afirmar que no
hubo deliberación, no es deriva pura: se reporta y se espera.

---

## Bloqueo explícito, final

- Proponer «dejar como está» sobre una divergencia con deliberación previa
  → **es una acción**, y está bloqueada igual que cambiarla.
- Presentar la reconstrucción por traza como si fuera la comprensión →
  **detener**. Es el error que v4 cometió y que esta versión corrige.
- Avanzar después de reportar el material, sin instrucción → **detener**.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: v4 (reconstrucción por traza, ejemplo n_runs), v3 (criterio),
v2 (pasos y field check), v1 (contexto y medida canónica)*
