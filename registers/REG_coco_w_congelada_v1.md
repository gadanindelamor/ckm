# REG_coco_w_congelada_v1.md

*Sep 2026 — gadanin.delamor + Claude Opus 5 (Code)*
*Clase R*

---

## Descripción

`COCO.self.W` queda congelada en el momento de la construcción de la
instancia, y `MonitorService` nunca adopta la instancia nueva que
`CorpusService._rebuild()` crea en cada ingesta. El defecto tiene dos
desenlaces según el corpus, y **hoy no es alcanzable en producción** porque
el canal vivo no inyecta thermostat.

Todas las mediciones de este REG se regeneran con
`experiments/coco_lifetime_analytics.py` (secciones A–F). Salidas en
`process/experiments/coco_lifetime/`.

---

## Origen

Hallado leyendo código en conversación, siguiendo una pregunta de delamor
sobre la vida de las instancias de COCO. No salió de un test que fallara:
ningún test falla.

---

## El mecanismo

```python
# corpus_service.py:255-257 — ultimas lineas de _rebuild()
from coco import COCO
history = self._load_landscape_history(self._monitor_jsonl_path)
self._coco = COCO(W=self._W, track_landscape=True, landscape_history=history)

# corpus_service.py:107-110 — el accesor vivo existe
@property
def coco(self):
    return getattr(self, '_coco', None)

# monitor_service.py:71 — asignado una vez, nunca reasignado
self._thermostat = thermostat
```

`_rebuild()` corre **en cada ingesta** (verificado: 6 textos → 6 rebuilds).
El accesor `corpus.coco` devuelve siempre el actual. `MonitorService` guarda
una referencia inyectada en el constructor que **tapa** el accesor:
`corpus.coco` no aparece ni una vez en `monitor_service.py`.

Y `observe()` recibe **sólo Δ_r**. COCO nunca recibe una W nueva: usa
`self.W` para `A0`, para `β_c` y para `W_eff = self.W + self._Delta`.

**La regla está declarada.** README:

> *When W changes, a new COCO instance must be created — COCO's β_c is
> derived from the W it was initialized with.*

La instancia se crea. La adopción no ocurre. Es la misma forma que R02
(*verification network before and after*): declarada entera, implementada a
la mitad.

---

## Sección A — identidad de instancias

| corpus | ingestas | `corpus.coco` cambió de objeto | `monitor._thermostat` cambió | coincidieron |
|---|---:|---:|---:|---:|
| caso09_run2 | 21 | **21** | 1 (nunca) | **0** |
| sintéticos | 9 | **9** | 1 (nunca) | **0** |

Cero coincidencias en 30 ingestas medidas.

---

## Sección B — W congelada vs W actual

**caso09_run2 — N crece:**

```
N de COCO: 19        N actual: 20        shapes calzan: NO
mu_W    0.28654971  →  0.01052632
beta_c  0.367347    →  9.5                (factor 25.9)
```

**sintéticos — N saturado en top_k:**

```
N de COCO: 20        N actual: 20        shapes calzan: SI
mu_W    0.32105263  →  0.14210526
beta_c  0.311475    →  0.703704           (factor 2.26)
max_abs_dif observados: {1.0, 2.0}
```

`max_abs_dif = 2.0` sobre W ∈ [−1,+1] significa que un peso **cambió de
signo** entre la W de COCO y la actual. No es deriva numérica.

`β_c = 1/(ρ*·N·μ_W)` — congelada W, congelados μ_W, N y β_c. `β_c` es contra
lo que `temp_signal()` compara.

---

## Los dos desenlaces — dependen del corpus, no del código

**N crece después de construir COCO → excepción dura.** caso09, primera
evaluación, `n_textos=4`:

```
ValueError: operands could not be broadcast together with shapes (19,19) (20,20)
   coco.py:212   W_eff = self.W + self._Delta
```

**N ya saturó en `top_k` → silencio.** Los shapes calzan siempre, no hay
excepción, y sólo difieren los valores. Sección D, sintéticos, 9
evaluaciones:

| | valores distintos |
|---|---:|
| `D_ckm_monitor` | **7** |
| `D_ckm_coco` | **1** (plano en 0.0) |
| coinciden | 2 de 9 |
| STOPs | 0 |

Compuesto con DEFS §10, que ya documenta que `D_ckm_monitor` es
**algebraicamente ciego** a la compresión de STOP (cancelación exacta,
verificada en 19 evaluaciones con Δ_r variando 14 órdenes de magnitud):

```
D_ckm_monitor  →  W actual,  ciego a STOP
D_ckm_coco     →  sensible a STOP,  W del momento de construcción
```

Hoy ninguno de los dos es W actual **y** sensible a STOP a la vez.

---

## Sección C — β

Con N saturado, el regulador **acumula** β precisamente **porque es el
objeto viejo**: 9 evaluaciones acumuladas contra 0 en `corpus.coco`, que
tiene la W actual y nunca observa.

```
evals acumuladas en el regulador : 9
evals acumuladas en corpus.coco  : 0
```

Adoptar el fresco daría W actual y **β reiniciado**. El defecto está
protegiendo la acumulación de β por accidente.

Con N creciendo no llega a acumular nada: revienta en la primera evaluación.

---

## Sección F — alcance real

```
construcciones de MonitorService en el repo : 19
    con thermostat                          : 11
    en produccion (fuera de tests/experiments/__main__) : 1
    en produccion CON thermostat            : 0
```

La única construcción de producción es `iap_chatroom/ckm_monitor.py:74`, y
sus keywords son `storage_path` y `behavior_graph`. **No pasa thermostat.**

Consecuencia: en el canal vivo COCO **nunca regula**. `panel["thermostat"]`
es `None` siempre. `corpus.coco` se construye en cada mensaje y nadie le
llama `observe()`; su único uso es `landscape_history()` en
`ckm_monitor.py:90`.

**El defecto está latente. Se vuelve excepción el día que alguien conecte
COCO al canal** — con un corpus real, en la primera evaluación posterior a
que se agregue un nodo.

---

## Lo que NO queda afectado

Los drivers y tests que sí inyectan thermostat **ingestan todo en un bloque
antes de construir COCO** y no vuelven a ingestar:

```python
corpus.ingest(orig.WARMUP_TEXTS)      # test_armstrong_boltzmann_comparison.py:72
th = COCO(...)                        # :78
monitor = MonitorService(..., thermostat=th)   # :86
# luego N evaluate(), ningun ingest mas
```

Una W por condición, sin rebuild posterior: la W congelada **es** la W
correcta. Las mediciones de `REG_armstrong_*`, `REG_stochastic_eval_*`,
`REG_n_runs_sweep_*` y `REG_wmixta_*` se sostienen sin cambio.

Eso también define su cuadro: esos STOPs se midieron sobre **campo estático
con Δ_r creciendo**. Lo que el canal haría —COCO regulando mientras el piso
se reconstruye— no está medido.

---

## Rebuild por mensaje vs por ciclo

El período con que W cambia es lo que vuelve inanición a una regla correcta.

```python
# corpus_service.py:95 — incondicional
if len(self._texts) >= self.min_texts:
    self._rebuild()

# corpus_service.py:123 — el criterio de ciclo, escrito y nunca llamado
def should_rebuild(self, d_ckm_history, n=3) -> bool:
    """gradiente de D_ckm positivo sostenido por n pasos."""
```

`CorpusService` no llama `should_rebuild()` nunca. Su único llamador,
`ckm_monitor.py:114`, guarda el resultado en `_last_rebuild_signal`, que
**no se lee en ningún lado del repo**. Y su disyunción satura: el término
`len(_texts) >= min_texts*2` es monótono, así que la señal es `True` desde
el sexto texto pase lo que pase con el gradiente.

Con rebuild por ciclo, COCO viviría un ciclo y β acumularía sin necesidad de
trasplantar nada.

---

## Clasificación y decisiones (delamor, Sep 2026)

- **Es bug, no GAP.** No hay nada escrito que preserve la instancia vieja a
  propósito; la deliberación existe (README) y dice lo contrario.
- **`A0` debe cambiar con los rebuilds.** La instancia nueva ya lo hace:
  nace con `_A0 = None` y lo recalcula sobre la W del momento. No se
  trasplanta — se deja morir.
- **β se conserva.** `_rejections_per_device` es historia real de rechazos;
  no debe reiniciarse con el rebuild.

Precedente de trasplante en las mismas tres líneas: `landscape_history` ya
se rescata desde el jsonl. Se rescata **una** de seis cosas que acumula.

---

## Sección E — censo de rutinas duplicadas

Por AST, con docstrings quitados: ni comentarios ni formato influyen.

```
_relax              3 variantes /  7 archivos
_relax_orbit        1 variante  /  2 archivos    coco.py y monitor_service.py IDENTICOS
relax_orbit         1 variante  /  1 archivo     experiments/orbit_analytics.py
_count_attractors   5 variantes /  7 archivos
_cS                 2 variantes /  5 archivos
```

**Corrige una medición previa de esta misma sesión.** Se reportaron 4
variantes de `_relax`; son **3**. El extractor usado entonces cortaba en
firmas multilínea, y `ast.dump` sin quitar docstring marcaba como distintas
funciones que sólo difieren en su docstring. Dos instrumentos descartados
antes de llegar al que sirvió — los dos de Code.

La unificación de `TASK_monitor_service_unificar_rutinas_v1` **se sostiene y
es más fuerte de lo registrado**: no sólo `_relax`; la primitiva
`_relax_orbit` entera es idéntica entre COCO y MonitorService.

---

## Lo que queda abierto

- Magnitud del efecto en un corpus operativo real y estabilizado: no medido.
- Si `should_rebuild()` debe gobernar el rebuild, y con qué criterio de
  ciclo. Es decisión de modelo.
- El orden del arreglo: conectar COCO al canal expone la excepción. Arreglar
  la adopción sin arreglar el crecimiento de N cambia silencio por caída.

---

## Archivos

```
experiments/coco_lifetime_analytics.py       driver — regenera todo esto
process/experiments/coco_lifetime/*.json     salidas, no se pisan
```

Referencias: DEFS_CKM_estado_actual_v9 §9 §10 §11 §18, README (regla de
instancia nueva, R02, R09), REG_monitor_service_unificar_rutinas_v1,
REG_armstrong_boltzmann_comparison_v1.

*Sep 2026 · Codespace ckm*
