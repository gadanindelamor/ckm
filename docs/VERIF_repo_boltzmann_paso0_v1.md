# VERIF_repo_boltzmann_paso0_v1.md

*Ago 2026 — gadanin.delamor + Claude Code (Opus 5, Codespace ckm)*
*Verificación contra el repo real — para transporte al ambiente Claude.ai chat*

---

## Qué es este archivo

`TASK_boltzmann_sampling_count_attractors_v1.md` define un Paso 0 con una
condición de parada explícita:

> *Si `relax(beta=float)` no existe en hopfield.py con la firma esperada,
> detener y reportar a delamor antes de continuar.*

**La condición se disparó. No se modificó ningún archivo.**

Este documento es el reporte. Está escrito para ser leído en un ambiente
sin acceso al repo: todo lo que afirma está citado literal, con archivo y
línea. Nada acá es de memoria.

---

## Resumen en una línea

`relax(beta=float)` existe, pero en otro archivo, con otra firma, no es
importable desde `services/`, y usa el RNG global de numpy — que es
exactamente lo que `_count_attractors()` aísla.

---

## Hallazgo 1 — ubicación

La TASK indica `services/hopfield.py`. Ese archivo **no existe**.

```
$ ls services/hopfield.py
NO EXISTE

$ find . -name "hopfield.py" -not -path "./.git/*"
./hopfield.py          ← raíz del repo
```

El `grep -n "beta" services/hopfield.py` del Paso 0 no devuelve nada, y no
porque falte `beta` — porque falta el archivo.

Esto es coherente con la estructura declarada en el README: `hopfield.py`
figura en la raíz, junto a `core.py`, `analytics.py`, `kcore.py` (capa de
validación P1–P4), separada de `services/` (capa runtime IAP).

---

## Hallazgo 2 — no es importable desde services/

`hopfield.py` línea 16:

```python
from .core import CKMGraph, CKMConfig
```

Import **relativo**. Requiere que el módulo sea parte de un paquete. Los
únicos `__init__.py` del repo son:

```
./iap_chatroom/__init__.py
./iap_chatroom/providers/__init__.py
```

No hay `__init__.py` en la raíz. Verificado en ejecución:

```
$ python -c "import sys; sys.path.insert(0,'.'); import hopfield"
ImportError: attempted relative import with no known parent package
```

**Hoy, desde `services/coco.py`, esa función no se puede llamar.** No es una
cuestión de estilo de import: no hay forma de resolverlo sin tocar la
estructura de paquetes del repo, que está fuera de los "archivos a
modificar" de la TASK.

---

## Hallazgo 3 — la firma es otra

Firma real, `hopfield.py` líneas 21–26:

```python
def relax(
    graph: CKMGraph,
    sigma_init: Optional[np.ndarray] = None,
    max_iter: int = 1000,
    beta: Optional[float] = None,
    seed: Optional[int] = None,
) -> np.ndarray:
```

El primer parámetro es un objeto `CKMGraph` (definido en `core.py:66`), no
una matriz. `COCO` trabaja con `np.ndarray` crudos y **no construye
`CKMGraph` en ningún punto** — no lo importa siquiera. Usarla implicaría
instanciar un `CKMGraph` por run (o por llamada) dentro de
`_count_attractors`.

---

## Hallazgo 4 — RNG global vs. RNG aislado

`hopfield.py` líneas 37–38 y 51–52:

```python
    if seed is not None:
        np.random.seed(seed)          # <- estado GLOBAL de numpy
    ...
            p = 1.0 / (1.0 + np.exp(-2.0 * beta * h))
            sigma[i] = 1.0 if np.random.rand() < p else -1.0
```

`services/coco.py`, `_count_attractors`:

```python
        rng = np.random.default_rng(self._seed)    # <- Generator AISLADO
```

Son dos regímenes de aleatoriedad incompatibles. Llamar a `relax()` dentro
del loop de `_count_attractors` contamina y es contaminado por el estado
global del proceso.

**Por qué importa más de lo que parece:** el aislamiento de semilla de
`_count_attractors` es la propiedad sobre la que se apoya todo
`experiments/stochastic_attractor_eval.py` y los resultados de
`REG_stochastic_eval_v1.md` y `v2`. Ese módulo existe precisamente porque
`seed` y `n_runs` sólo son configurables al instanciar `COCO`; si el conteo
pasara a depender del RNG global, las corridas dejarían de ser
reproducibles por `(seed, n_runs, W)` y los `run_hash` de esos REG dejarían
de identificar lo que dicen identificar.

Esto no está en la lista de "NO modificar" de la TASK, pero es una
regresión silenciosa sobre trabajo ya registrado.

---

## Hallazgo 5 — `n_warmup` no tiene traducción directa

`hopfield.py` línea 43:

```python
    for _ in range(max_iter * N):
        i = np.random.randint(N)
```

`relax()` corre `max_iter * N` actualizaciones asíncronas (un nodo por vez)
y devuelve sólo el estado final. No acepta un número de pasos: "n_warmup =
N pasos" no es un argumento que exista. Habría que pasar `max_iter=1` (que
da exactamente N actualizaciones) o usar `relax_steps()` (`hopfield.py:57`),
cuya firma no fue verificada para este uso.

---

## Hallazgo 6 — dos β_c distintos, y la diferencia no es marginal

La TASK pide:

```python
mu_W = np.mean(W[W > 0])          # media sobre pesos no-nulos
```

`services/coco.py`, `beta_c_corpus()` (líneas 331–335) ya calcula un β_c,
pero con otra μ_W:

```python
        ii, jj = np.triu_indices(self.N, k=1)
        mu_W = float(np.mean(self.W[ii, jj]))     # incluye ceros
        if mu_W <= 0:
            return float("inf")
        return 1.0 / (BETA_RHO_STAR * self.N * mu_W)
```

Su docstring lo dice explícito: *"μ_W global (incluye ceros) — conservador,
menos sensible"*.

Medido sobre `services/W_ckm_corpus_v2.json` (N=32, densidad 0.7324):

| μ_W | valor | β_c resultante |
|---|---|---|
| incluyendo ceros (`coco.py`, actual) | 0.004519 | **13.8318** |
| sólo `W > 0` (TASK) | 0.005977 | **10.4575** |

Razón: **0.756**. El β_c de la TASK es un 24% más bajo.

`β_c = 13.83` es el valor que aparece como parámetro calibrado en el README,
como *"analytically derived"* en el PAPER §9.2, y como base del modo
Boltzmann propuesto en `DEFS_CKM_estado_actual_v7.md` §11. La TASK, tal como
está escrita, introduciría un **segundo** β_c en el mismo archivo, con otro
nombre y otro valor, sin declarar la relación entre ambos.

**Decisión pendiente de delamor:** ¿el modo Boltzmann usa su propio β_c
(μ_W sobre no-nulos, 10.46) o el ya calibrado en el proyecto (13.83)? No es
una elección de implementación — cambia la temperatura a la que se muestrea.

---

## Opciones para implementar (ninguna ejecutada)

**A — reimplementar el paso Boltzmann dentro de `coco.py`.**
Tres líneas sobre el `rng` aislado que ya existe: `p = 1/(1+exp(-2·β_c·h))`,
actualización asíncrona, `n_warmup` pasos. No importa `hopfield.py`, no toca
el RNG global, no toca la estructura del repo, respeta los "archivos a
modificar" de la TASK.
*Costo:* duplica la fórmula que ya vive en `hopfield.py:51`. Es el mismo
patrón que ya produjo `experiments/monitor_service.py` conviviendo con
`services/monitor_service.py` — dos implementaciones de lo mismo que pueden
divergir sin que nadie lo note.

**B — hacer importable `hopfield.py`** (`__init__.py` en la raíz, o carga por
ruta con `importlib`) y adaptar la llamada.
*Costo:* toca la estructura de paquetes del repo y arrastra el RNG global
adentro del conteo (Hallazgo 4). El `__init__.py` en la raíz además cambia
cómo se resuelven imports en todo el repo.

**C — portar `relax` a `services/`** con firma sobre `W` en vez de `CKMGraph`.
Es la que deja el repo mejor: una sola implementación, canónica, usable por
las dos capas.
*Costo:* la más invasiva, y toca la capa de validación P1–P4 — código sobre
el que corrieron las predicciones ya publicadas.

**Recomendación:** **A**, con un comentario que apunte a `hopfield.py:51`
como fuente de la fórmula, y la duplicación declarada explícitamente en el
docstring en vez de silenciosa. Pero es decisión de delamor: la TASK ordena
detener y reportar, y eso es lo que se hizo.

---

## Lo que este documento no dice

- **No dice que la TASK esté mal.** Dice que fue escrita desde un ambiente
  sin el repo a la vista, y que cuatro de sus supuestos (ruta del archivo,
  firma, importabilidad, μ_W) no coinciden con el código real. Es
  exactamente el desfasaje entre ambientes que la metodología del proyecto
  ya nombra como condición material (PAPER §3.x).
- **No evalúa si Boltzmann muestrea mejor.** Eso es empírico y requiere la
  implementación corrida, más un REG posterior — como la propia TASK declara
  en "Lo que este TASK no cierra".
- **No toca el punto de `n_warmup` óptimo.** Sigue abierto.

---

## Estado

- Ningún archivo modificado. Ningún commit.
- Pendiente de instrucción: opción A/B/C, y cuál β_c.

---

*Repo: gadanindelamor/ckm · Codespace ckm — bash/Linux*
