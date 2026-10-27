# TASK_calibrate_en_el_build_v2 — el bootstrap y la calibración como servicio del estado

*27 oct 2026. La escribe Opus 5.5 (Cowork) para Code. Reemplaza a la v1 (opciones A y B). Fuente: `docs/opus/decisiones_en_el_acto.md`, 26 y 27 oct; reporte de Code al texto 08 (BANDEJA, 26 oct 23:05 UTC).*

**Dirección decidida por delamor** (27 oct): *"el diseño que decido es el congruente a la dirección de tu interpretación precisa y orientada a la Visión"*. La E3 (quién calibra) queda resuelta en esa dirección. Los puntos que esta TASK marca como **[abierto]** se reportan en CP0 y no se resuelven solos.

---

## 0. La visión, en tres líneas (delamor, 27 oct)

- Cada uno guarda lo suyo, con su atribución, en **su lugar** dentro del estado. Un lugar tiene un solo escritor y muchos lectores. *"Es DONDE. Ese es el candado."*
- El dueño de los lugares es el estado. Hoy es `CKMlandscapeConfig`, que no es estática: es la traza de los ciclos.
- Los servicios *"se prestan mutuamente"*. Cachés y optimización vienen en una etapa posterior.

## 1. Lo que hay hoy (verificado por Code, texto 08)

- La primera W la construye `ingest` → `_rebuild(causa=None)`. El cambio de sha pone en cero los tres contadores en esa misma vuelta, así que ningún criterio vota y `_calibrate` no se llama. Es un **candado doble**.
- El punto de calibración está atado al bloque de la decisión del régimen, y **el origen no es una decisión del régimen**.
- Los umbrales viajan por `_coco_config` y no hay ningún campo que los ate a su W. Caso 1: tras una calibración exitosa, una que no separa deja los números viejos con el `w_sha` de la W que falló.
- En las 7 curvas medidas, el extremo de colapso es la misma matriz para toda W (N_eff = 2,4369). **El patrón no se toca en esta TASK.**

## 2. El diseño

**D1. El nacimiento tiene su propia condición.** Bootstrap verdadero = no hay W y `no_rebuild_reason(allow_first_W)` devuelve `None`. **No** es un criterio de la jerarquía, y la jerarquía estructural > volumen > tiempo no cambia.

**D2. La calibración cuelga de "antes de instalar una W", no de la decisión.** El orden vale para el origen y para cada rebuild del régimen:
1. W candidata;
2. `calibrate(candidata)`;
3. el registro se escribe en su lugar del estado;
4. se instala la W;
5. COCO nace y lee su vara de ese lugar.

**D3. El lugar de la calibración en el estado.** Un solo escritor, el servicio de calibración. Contiene `{valores, estado, condiciones, w_sha}`, y `w_sha` es la W calibrada.
- COCO lee de ahí. Si el `w_sha` del lugar no es el de la W que COCO juzga, eso queda declarado en el panel.
- Esto revisa **D6** (*"los umbrales no entran a la Config"*): la calibración sigue siendo un proceso aparte, pero su resultado vive en su lugar del estado, firmado.

**D4. Sin vara de otra W.** Si la calibración de la W viva no separa, COCO usa los defaults **declarados como tales**: `source: "default"`, con la causa (`no_calibrado:<causa>`). Nunca los números calibrados para otra W. **[abierto: confirmar en CP0 que no choca con nada del repo]**

**D5. El nacimiento queda registrado.** El origen deja su línea en `rebuild_decisions.jsonl`, con causa `bootstrap` (el nombre ya existe, `ckm_landscape_config.py:52`), igual que cualquier otro cambio de W (hallazgo B).

**D6'. Los parámetros de `calibrate`** (`n_runs` 200, `seed`, grilla) se declaran en su lugar del estado, no como default de función. El **valor** (200 o el de la Config) **[abierto]**: subirlo multiplica el costo en el hilo del mensaje.

## 3. Lo que NO toca

- El patrón de `calibrate` (el colapso, la grilla, el margen en los extremos).
- El mecanismo general de "los defaults resuelven contra el estado" (el centinela, el inventario completo). Es la TASK siguiente, después del inventario.
- Los procesos: el estado vive en el proceso del server y los devices siguen entrando solo por MCP.
- El vivo.

## 4. Checkpoints (P16: de corrido dentro de cada CP, A1.PAUSA entre CPs)

**CPa — lo mecánico (no necesita OK).**
- Registrar en `DECISIONES_opus.md` P12, P15 y P16, con las respuestas de delamor (decisiones del 26 y 27 oct).
- Corregir `n_puntos_d_ckm`: se lee antes del reset (hallazgo A). Es una corrección declarada de registro.
- **Regla nueva de `.py`** (reemplaza la del 24 oct): al acceder, A1.PAUSA. Después de modificar, revisar el docstring propio y hacer `grep` de los nombres tocados en los docstrings y comentarios del resto del repo.

**CP0 — evaluar el diseño contra el repo (no necesita OK).** Tensiones, lo que rompe, qué tests se mueven (la hipótesis es que las 13 de `test_should_rebuild_conectado.py` **no** se mueven; verificarlo), y los **[abierto]**. Sin código.

**CP1 — D1 + D2 + D5 (OK de Opus).** El nacimiento por su condición propia y la calibración antes de instalar. Tests nuevos: la primera W pasa por calibrate; el origen tiene su línea con `bootstrap`; la jerarquía no cambia.

**CP2 — D3 + D4 + D6' (OK de Opus; los [abierto] que sean E3 suben a delamor).** El lugar de la calibración en el estado, COCO leyendo de ahí, y el test del caso 1: una calibración exitosa seguida de una que no separa **no** deja la vara vieja.

**CP3 — el vivo:** solo con orden explícita de delamor.

## 5. Cómo se revierte

Cada CP es un commit que nombra sus archivos y se revierte con `git revert`. Sin compatibilidad hacia atrás: la única versión del modelo es la actual.
