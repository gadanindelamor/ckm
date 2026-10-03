# TASK_representacion_atractores_adaptador_v1

*Clase T — Oct 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Desprende de TASK_salamanca_neel_coercividad_v2, CP1. Precondición del paso 1 de esa TASK.*
*Antecedentes: PROPUESTA_capa_analisis_services_v1 §Nivel B ("Advertencia sobre el tipo de dato"); REG_orbitas_conjuntos_invariantes_v1; DEFS §4.2 (GOLES/LaSalle).*

---

## 1. El problema

Dos objetos con la misma forma y contenido distinto:

- `analytics.copresence_matrix(attractors, N)` espera `dict[frozenset, int]`, donde el frozenset es el **conjunto de nodos activos** de un atractor. Lo usa así: `for i in attr: attr_matrix[idx, i] = 1`.
- `landscape_engine.relax_orbit` devuelve la órbita como `frozenset` de **estados completos**, serializados con `.tobytes()`.

La PROPUESTA ya lo había marcado, textual:

> *"Misma forma, contenido distinto. Al integrarlos hay que decidir explícitamente cuál se le pasa a cada función, o se van a mezclar en silencio."*

**La pérdida no es sólo de tipo.** Representar un atractor por su conjunto de nodos activos:

1. **borra el periodo** — una órbita de periodo 2 son dos estados y un solo conjunto;
2. **colapsa estados distintos** que tengan los mismos nodos en +1 bajo la misma clave.

Con GOLES el periodo es 1 o 2, nunca más (DEFS §4.2), así que el caso es acotado y tratable.

## 2. La tentación, declarada

*(delamor: qué tentación a 1… PULL. Y Code: la tengo yo también.)*

La opción cómoda es pasarle el conjunto de nodos activos tal cual: funciona, no hay nada que escribir, se sigue. **El costo sería silencioso** — los números saldrían bien igual, y la pérdida de periodo no aparecería en ninguna salida.

Es la misma forma que REG_unidad_texto §5.3 nombra: el proxy devuelve un número siempre, el objeto no.

## 3. Lo que hace Code

### Paso 1 — medir, no elegir

Contar la distribución de periodos en los corpus del paso 1 de la TASK madre: `caso09`, `caso13`, `caso14`, `informes_version`, `informes_pagina300` y el tramo `categorias`.

Por corpus: cuántas órbitas distintas, cuántas de periodo 1, cuántas de periodo 2, y qué fracción de la masa de cuenca está en periodo 2.

**Si sale cero periodo 2 en todos: la opción 1 es exactamente correcta y no cuesta nada.** El paso 2 se reduce a declararlo.

Referencia de contraste que ya existe: el paper §4.2 reporta 141/200 y 136/200 trayectorias en órbita para los dos corpus IAP de N=20, y 3/200 para el corpus de trabajo de N=32. **La prevalencia es del corpus**, así que hay que medirla en estos.

### Paso 2 — el adaptador

En el driver (Clase T). **No toca `services/`**: ni `analytics.py` ni `landscape_engine.py`.

Regla: **cada órbita aporta una fila por cada estado de su conjunto invariante, pesada por la masa de la cuenca.**

- periodo 1 → una fila. **Idéntico al comportamiento de hoy.**
- periodo 2 → dos filas.

No es un parche sobre `copresence_matrix`: es lo que esa función mide. Correlaciona nodos por co-presencia **entre atractores**, y una órbita de periodo 2 tiene genuinamente dos conjuntos activos. Meter los dos es describir la órbita, no repararla.

El peso entra porque `copresence_matrix` hoy trata todas las claves por igual (`unique = list(attractors.keys())`, una fila por clave, sin usar el `int` del valor). Si se agregan filas sin peso, una órbita de periodo 2 con masa chica pesaría el doble que una de periodo 1 con masa grande.

### Paso 3 — verificar que es impacto cero donde debe serlo

- En un corpus donde todas las órbitas son periodo 1, el adaptador tiene que dar **exactamente** la misma matriz de copresencia que pasarle los conjuntos activos directo. Comparación bit a bit.
- En uno con periodo 2, reportar en qué cambia la matriz y los clusters que salen de ella.

## 4. Decisiones

**Tomadas (delamor):**
1. Medir antes de elegir la representación.
2. Adaptador con una fila por estado, pesada por masa de cuenca.
3. Vive en el driver. `analytics` y `landscape_engine` no se tocan.

**Abiertas:**
4. Si el peso debe ser la masa de la cuenca de la **órbita** repartida entre sus estados, o la masa completa de la órbita en cada fila. Son dos cosas distintas y la diferencia aparece sólo con periodo 2.
5. Si dos estados distintos con el mismo conjunto activo deben contar como una fila o como dos. Hoy colapsan; con el adaptador siguen colapsando, porque la clave sigue siendo el conjunto. **Queda registrado, no resuelto.**

## 5. Lo que Code NO hace

- No modifica `analytics.py` ni `landscape_engine.py`.
- No cambia `copresence_matrix` para que acepte estados completos.
- No decide la representación antes de medir.
- Toda acción fuera de esta TASK es checkpoint.

## 6. Checkpoints

**Formato:** qué hizo · qué salió (números) · qué no pudo · qué no esperaba · costo.

| CP | Después de | Reporta |
|---|---|---|
| **CP1** | paso 1 | Distribución de periodos por corpus y fracción de masa en periodo 2 |
| **CP2** | pasos 2–3 | Que la matriz es idéntica donde el periodo es 1; y dónde cambia si no |

## 7. Criterio de cierre

- Test del adaptador: periodo 1 → matriz idéntica a la vía directa; periodo 2 → el número de filas que corresponde.
- Según CONVENTIONS: ¿qué test debería haber cambiado con esto? Declarar los huecos.
- Si el paso 1 da cero periodo 2 en todos los corpus, **eso es el resultado**: se declara y el adaptador queda escrito para cuando aparezca, no se da por verificado.

---

## Anexo — registro de CP1 de la TASK madre (paso 0, hecho)

`git mv process/initial_static_model/analytics.py services/analytics.py`.

El diff son **dos hunks, los dos del import**; las cinco funciones quedaron byte a byte iguales:

```
< from typing import Optional
> from typing import TYPE_CHECKING, Optional

< from .core import CKMGraph
> if TYPE_CHECKING:
>     from core import CKMGraph
```

Suite: 172 passed, sin cambios.

**`core.py` no se movió.** `CKMGraph` aparece una sola vez en `analytics`, como anotación de `optimal_density`, y con `from __future__ import annotations` no se evalúa. Mover `core.py` habría roto `hopfield.py` y `mcp_adapter.py` (que lo importan con `from .core`), y `mcp_adapter` es el Gatekeeper que el paper §4.5 declara verificado a 0.092 ms.

**El testigo en `process/` pierde `analytics.py`** *(decidido: delamor)*. Entra en uso **sin cambios**, así que no hay pérdida que atestiguar que el historial de git no tenga. Distinto de FabricationService, que fue a `process/` porque se reescribe.
