# TASK_representacion_atractores_adaptador_v1

*Clase T — Oct 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Desprende de TASK_salamanca_neel_coercividad_v2, CP1.*
*CERRADA. F1 y F2 ejecutados. El resultado cambió su propio motivo: la partición de SALAMANCA sale de W, no de los atractores (v3 §12), así que el adaptador no se usa ahí. Queda escrito y verificado para W_mixta.*
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

- periodo 1 → una fila.
- periodo 2 → dos filas.

**CORRECCIÓN (Code, 4 oct, tras SUPERTASK v3 §4.1.2).** Esta TASK decía que con periodo 1 el resultado era *"idéntico al comportamiento de hoy"*. **Es falso:** las órbitas de periodo 1 también tienen masas distintas entre sí, así que pesarlas cambia la matriz aunque no haya ningún periodo 2. El impacto cero vale sólo para el camino **sin** peso.

Y está medido en el propio F2: caso09, cuya masa es casi toda de periodo 1, pasó de correlación media **+0.680 sin peso a +0.999 con peso**. El número estaba en la tabla de §8 y la conclusión escrita acá lo contradecía.

Precisión sobre §4.1.2 del SUPERTASK: el peso **sí** se puede aplicar desde afuera —`copresencia_pesada`, en el driver, verificada a 1e-16 contra `analytics.copresence_matrix` con pesos uniformes—. Lo que no se puede es aplicarlo **y** seguir siendo impacto cero. Esa es la parte que decide, y ahí §4.1.2 tiene razón: la opción (b) requiere un cambio declarado a `copresence_matrix` por la regla §4.4, con test, y volver a medir todo el pre-registro.

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


---

## 8. Resultado

### F1 — distribución de periodos (W_pos, top_k 32, n_runs 1000, seeds 0/1/2)

`p > 2` es **cero** en los seis corpus: GOLES se cumple (DEFS §4.2), control pasado.

| corpus | masa en periodo 2 |
|---|---:|
| caso09 | 0.001 – 0.009 |
| caso13 | 0.001 – 0.002 |
| caso14 | 0.004 – 0.006 |
| informes versión | 0.004 – 0.005 |
| informes página 300 | 0.000 – 0.004 |
| tramo `categorias` | **0.36** |

Así que **no** salió cero periodo 2, y el paso 2 no se reducía a declararlo. Pero la masa es ínfima en cinco de seis. `categorias` es el único donde el periodo no es despreciable.

Composición de las dominantes (seed 0): en caso09, informes versión e informes página 300, el **99.9% de la masa está en dos órbitas — las 32 en +1 y las 32 en −1**. Las de periodo 2 tienen 10–16 nodos prendidos.

### F2 — el adaptador, con el control de impacto cero

**Elección tomada: (b) con peso, masa de la órbita repartida entre sus estados.**

El motivo medido no fue el periodo: `copresence_matrix` **descarta el `int` que recibe** (`unique = list(attractors.keys())`, una fila por clave). Hoy ya trata una órbita del 0.1% igual que una del 50%.

**Control:** con pesos uniformes, `copresencia_pesada` contra `analytics.copresence_matrix` da **`max|dif| = 1e-16`** en los cinco corpus. Es la misma función.

| corpus | claves | corr. media sin peso | con peso |
|---|---:|---:|---:|
| caso09 | 4 | +0.680 | +0.999 |
| caso13 | 6 | +0.336 | +0.998 |
| caso14 | 10 | +0.176 | +0.996 |
| informes versión | 12 | +0.140 | +0.995 |
| informes página 300 | 2 | +1.000 | +1.000 |

### Lo que el resultado hizo con la TASK

Con peso, la matriz de co-presencia es casi todo unos: lo que el campo ocupa en W_pos son los dos extremos, y ahí todos los nodos se mueven juntos. **No hay co-movimiento diferencial que agrupar.**

Eso no invalida la elección — la confirma, y muestra que el objeto no servía para lo que esta TASK venía a habilitar. La partición de SALAMANCA sale de W. El razonamiento está en TASK_salamanca_neel_coercividad_v3 §12.

El adaptador y `analytics.py` quedan escritos y verificados **para W_mixta**, cuando la frustración exista y los atractores tengan algo que mostrar.

### Abiertas que siguen abiertas

- §4.4 — reparto de masa entre estados vs masa completa en cada fila: **decidida por el reparto**, pero su efecto sólo aparece con cuencas que no sean los extremos. Sin verificar ahí.
- **La elección (a) sin peso vs (b) con peso vuelve a estar abierta y es de D1** (SUPERTASK v3 §4.1.2). Code había elegido (b); (b) no es impacto cero y arrastra un cambio a `services/`.
- §4.5 — **CERRADA, era vacía.** Un estado σ ∈ {−1,+1}^N está determinado por qué índices están en +1: la correspondencia estado ↔ conjunto activo es biyectiva, así que "dos estados distintos con el mismo conjunto activo" no existe. Y REG_orbitas_conjuntos_invariantes_v1 §5 ya había demostrado la otra mitad en septiembre —dos órbitas no comparten estados, porque el mapa es determinista—, así que el conjunto identifica unívocamente a la órbita. Code la abrió sin leer lo que la cerraba *(lo señaló Opus 5.5)*. La única pérdida real era el **periodo**, que es la que el adaptador trata.

Instrumento: `experiments/driver_neel_salamanca.py --periodos` y `--adaptador`.
