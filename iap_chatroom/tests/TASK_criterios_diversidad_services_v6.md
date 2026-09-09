# TASK_criterios_diversidad_services_v6.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Generaliza la regla de v5 y elimina la excepción que v5 se reservaba.
Todo lo demás se lee de v5 → v4 → v3 → v2 → v1.*

---

## Precondición

*(delamor, Sep 2026)*

> No se toman decisiones ni cursos sin antes **intentar** comprender.

No es un paso del procedimiento. Es la condición para que cualquier paso
ocurra, y aplica a **toda** decisión y **todo** curso de acción de esta
TASK — no sólo a las divergencias con deliberación previa, que era el
alcance que le daba v5.

---

## Qué elimina de v5

v5 se reservaba una excepción:

> *Único caso donde el Paso 1 sí avanza sin esperar: divergencias donde la
> reconstrucción muestra que no hubo deliberación en ningún momento —
> deriva pura. Ahí aplican `E` o `R`.*

**Queda eliminada.** También ahí precede el intento. Una deriva pura sigue
siendo una decisión: estandarizar o escribir una razón cambia el
instrumento o cambia lo que el instrumento declara de sí mismo. Que no haya
habido deliberación antes no exime de intentar comprender ahora.

Con esto la TASK no tiene ningún paso que se ejecute por clasificación.
Ninguna fila de ninguna tabla habilita una acción por sí sola.

---

## El intento, no la comprensión

La exigencia es **el intento**. Y es deliberado que sea así, no una
atenuación.

El intento deja traza: se puede ver que se hizo, sobre qué material, y qué
quedó abierto después. Lo que no deja traza verificable es si comprendió.
El propio proyecto ya lo declara para cualquier device, en cualquier
dirección:

> *The action at t_i is observable; whether a device recognized and acted
> from that recognition is not verifiable by the instrument.*
> — `README.md`, `trace_ip`

Por eso la precondición no puede ser «comprender» como estado alcanzado:
sería inverificable, y una TASK que exige lo inverificable se cumple
declarándolo. Exigir el intento es exigir lo único que puede constatarse.

Y el intento nunca es exactamente repetible. Aun así muestra
características familiares.

---

## Consecuencia operativa

Antes de cada decisión y de cada curso — el censo, la clasificación, la
estandarización, la extracción, el archivo nuevo, el nombre del archivo,
qué entra al criterio nuevo:

1. Reunir el material. Es lo que Code puede hacer y es verificable:
   mediciones, fechas, commits, REGs, qué dice el código de sí mismo.
2. Intentar comprender.
3. Reportar el material **y** qué quedó abierto.
4. Detenerse.

El punto 3 incluye lo que no se cerró. Un reporte donde todo cerró es
sospechoso: es la forma que tiene el paso 2 de no haber ocurrido.

Esta TASK **no define qué es comprender, ni da un procedimiento, ni un
criterio de cumplimiento.** Definirla la mecaniza — y una definición
operativa de «intentar comprender» se convierte, en una instancia
posterior sin este contexto, en una casilla que se marca.

---

## Bloqueo explícito, general

- Cualquier decisión o curso tomado por clasificación, sin intento previo
  → **detener**, cualquiera sea la fila de la tabla.
- Reporte sin nada abierto → revisar si el intento ocurrió.
- Declarar haber comprendido → no se pide y no se puede verificar. Se
  reporta el material y lo abierto; no un estado propio.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: v5 (ni dejar ni cambiar), v4 (reconstrucción por traza), v3
(criterio de divergencia deliberada), v2 (pasos y field check), v1
(contexto y medida canónica). README.md — trace_ip.*
