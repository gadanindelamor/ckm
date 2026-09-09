# TASK_criterios_diversidad_services_v3.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Refina el Paso 1.b de `TASK_criterios_diversidad_services_v2.md`. Todo lo
demás —field check, Pasos 2/3/4, decisiones pendientes, bloqueos— se lee
de v2, que se lee sobre v1. No se repite acá.*

---

## Criterio de divergencia deliberada — endurecido

*(Definición de delamor, Sep 2026)*

Una divergencia es **deliberada** sólo si cumple **las dos** condiciones:

1. **Declara su razón.** Por qué difiere, no qué hace.
2. **Dice dónde se ve en el código.** Qué método, atributo o llamada
   manifiesta la diferencia.

Y explícitamente:

> **Un valor distinto no es una razón.** `n_runs = 100` o `300`,
> `max_iter = 100` o `200`, no es deliberado. Un número que difiere sin
> razón escrita es **deriva**, por más intencional que haya sido en su
> momento.

La intención no deja rastro. La razón escrita sí. Lo que no está escrito
no es deliberado a los efectos de esta TASK — es indistinguible de deriva,
que es exactamente la condición que produjo las 4 variantes de `_relax`.

---

## Censo aplicado — services/coco.py vs services/monitor_service.py

| divergencia | razón en el código | dónde se ve | clase |
|---|---|---|---|
| `_relax` `max_iter` 100 vs 200 | no había | — | era deriva → unificada en `5f2ec6c`, medido 0/200 estados finales distintos |
| `count_seed=0` vs `self._seed` | **sí** — docstring del constructor: "son los valores que este servicio usaba hardcodeados, de modo que el comportamiento numerico no cambia", con referencia a `TASK_monitor_service_unificar_rutinas_v1` | `_count_attractors()` | **deliberada** |
| `weighted: Optional[bool]=None` vs `bool=False` | **sí** — docstring: "weighted/boltzmann en None toman self._sampling_mode. Pasarlos explicitos permite un conteo puntual en otro modo sin cambiar la configuracion del servicio" | `self._sampling_mode` | **deliberada** |
| `_combine_W_Delta(W, Δ_r)` vs `W + Δ_r` crudo | **parcial** — `_D_ckm` dice "Se usa _combine_W_Delta para escala compatible", que explica la escala pero **no la divergencia con COCO** | `_D_ckm()`, `evaluate()` | **falta la razón** |
| `n_runs` 50 (monitor) vs 80 (COCO) | **no** — COCO sí la tiene ("no cambiar sin revisar el hallazgo del sweep n_runs 60→70"); monitor no la tiene en ningún lado del repo | — | **deriva** |

Consecuencia: v1 había puesto `n_runs` fuera de alcance por considerarla
diferencia de diseño. Con este criterio, **no lo es**. Queda dentro del
Paso 1 como deriva.

---

## Dos salidas por cada deriva — y sólo una es mía

Para cada divergencia clasificada como deriva, el Paso 1 tiene dos salidas.
**No son equivalentes y la elección no es de Code:**

**Salida E — estandarizar.** Las copias quedan con el mismo valor. Mueve
números → requiere field check completo, y si no da cero se revierte.

**Salida R — escribir la razón.** El valor no se toca; se escribe por qué
difiere y dónde se ve. La divergencia pasa de deriva a deliberada. **Impacto
numérico cero por construcción** — no hay nada que verificar salvo que el
texto sea verdadero.

`R` es más barata y no mueve el instrumento. Pero **es una afirmación sobre
el modelo**: decir por qué MonitorService cuenta con 50 reinicios y COCO con
80 es decir algo sobre qué es cada uno. Eso es de delamor, no de Code.

Precedente en esta sesión: la razón de la cuarta divergencia
(`_combine_W_Delta`) delamor la enunció como *"Monitor no domina ni regula.
COCO sí. Los servicios de CKM son un sistema dinámico"*. Esa razón existe y
**no está en el código** — está en un REG y en la conversación. `R` para esa
divergencia es transcribirla al código; no es inventarla.

---

## Lo que Code hace y lo que no, en el Paso 1

**Hace:**
- El censo completo con el criterio de arriba, sobre las copias VIVAS.
- Clasificar cada divergencia: deliberada / falta la razón / deriva.
- Reportar la tabla y **detenerse**.

**No hace:**
- Elegir entre `E` y `R` para ninguna divergencia.
- Escribir una razón que no haya sido enunciada. Si no hay razón en el
  código ni en un REG ni dicha por delamor, se reporta como
  **"sin razón conocida"** y se pregunta. Rellenar el hueco causal con algo
  verosímil es el automatismo registrado en
  `REG_condiciones_meta_access_v1-3.md`: dispara sobre *cuánto* y *cuál*, no
  sobre *por qué*, y las dos veces que rellenó, fabricó.

---

## Bloqueo explícito, adicional a los de v2

- Divergencia sin razón conocida → **reportar y preguntar**. No proponer
  una razón plausible.
- Razón que existe sólo en un REG o en la conversación → se puede
  transcribir al código citando la fuente, **no reformular**. Si la
  transcripción exige interpretar, preguntar.
- `R` aplicada a una divergencia cuya razón resulta falsa contra el código
  → eso es peor que la deriva. Verificar la razón contra el código antes de
  escribirla, igual que se verifica un número.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
*Referencias: TASK_criterios_diversidad_services_v2.md (pasos y field check),
v1 (contexto y medida canónica), TASK_monitor_service_unificar_rutinas_v1.md,
REG_condiciones_meta_access_v1-3.md*
