# TASK_ckm_trust_rule_v1

*11 oct 2026. Escrito por Opus (Cowork), por pedido de delamor: "el código de criterio_local no sería más que instanciar la regla CKM TRUST, escrita en código; respetemos nombres de rótulos en inglés". Para Code, en el Codespace.*

## Por qué

La regla CKM TRUST está escrita (`REG_regla_ckm_trust_v1`, 4 oct) y tiene una forma (doc "La regla CKM TRUST", 11 oct). En el código no existe como objeto: aparece repartida, entera en un sitio y a medias en otros.

- **`criterio_local.py` (CP2b)** es donde está más entera. Tiene campo con registro, conservación, piso, auditoría con tasa nombrada, `SKIP` y `None` declarado.
- **`should_rebuild`** es la misma decisión de estado pero con la regla a medias: criterios en cascada, origen en `causa`, valores sin origen.
- **`calibrate`** es la regla aplicada a los parámetros de otra regla.
- **`NodeExtractor._seleccionar`** tiene corte, `TOL_EMPATE` y selección anterior.

Lo que dijo delamor (11 oct):

- **La regla es sobre órdenes**, con dependencias entre órdenes contiguos y recursión: condiciones_i → calibrar → condiciones_{i+1}.
- **El criterio local decide si escalar al orden siguiente** (el LLM, la decisión).


**delamor, 11 oct (admisible, no verificado):** *"si fuese admisible, al menos: este engine de la regla puede ser algo que emerge en el modelo, desde el modelo, como su propia metodología de proyecto, que lo está formando como instrumento. ERGO: se trata de identificar los órdenes de escala y, al instanciarla, el engine de la regla sabe qué hacer."* Calibrar, decidir en ODA y revisar el alineamiento (PoC) serían instancias. El protocolo de trabajo (Code → ALTO → Opus → delamor) también. Escalar a una instancia del **mismo** orden no es escalar: ↑k tiene que ser otro orden.

**ε, delamor (11 oct):** *"épsilon en la regla, el definido en su formulación. El nombre deja el que tenga ahora, tolerancia. Me refiero a que NO olvidemos a épsilon."*

- ε es la **tolerancia de la regla** (I3, sin cambios), y **no se omite en ninguna instancia**.
- Hoy falta en `criterio_local` y en `should_rebuild`. Si no se conoce, va **`None` declarado**, nunca 0. Un empate sin ε declarado es un empate que nadie ve.
- delamor: *"sin épsilon el engine no va a funcionar"*. Para el código, eso quiere decir que `tolerance` es un **argumento obligatorio, sin default**, igual que `causa` en `rebuild_por_decision` y que `piso_vueltas <= 0 → ValueError`. Si es `None` declarado, toda decisión cerca del corte lo lleva en su registro (`tolerance_unknown`): no se decide como si fuera 0.
- delamor: *"si no se conoce, tal cual: se declara, y LA REGLA lo descubre al instanciarse en el proceso de calibración. Y allí el bucle elipse que escala al orden espiral, y así, y así."*
  - ε = `None` en el orden k es un candidato del orden ↑k. Calibrar es Regla_{k+1} aplicada a los parámetros de Regla_k, así que lo descubre y lo devuelve en condiciones_{i+1}.
  - La **elipse** es el bucle cerrado dentro de un orden; la **espiral**, la escalada de un orden al siguiente.
- **Precisión de la regla** (delamor): está hecha de la precisión del intervalo que define ε, la identificación de los órdenes, las condiciones y las trazas. **Lo importante es no olvidar ε.**
- **No confundir con `TOL_EMPATE = 1e-12`** de NodeExtractor, que es tolerancia numérica.
- *(Se deja como traza: delamor también dijo "o yo le llamaría de confianza, quizás". Queda **abierto** si su valor puede salir de la incertidumbre de la medición.)*

## Forma a implementar (propuesta de Opus; la valida delamor)

```
Regla_k = ⟨ C_k, f_k, R_k, κ_k, ε_k, T_k, P_k, g_k, ↑k ⟩

1. |f_k(c) − κ_k| > ε_k             → decide f_k              origin = FIELD
2. empate y existe T_k               → decide T_k (conserva)   origin = TRACE
   · si 2 se repite P_k veces sin campo → 3
3. no hay T_k (o se cumplió el piso) → NO_TRACE:
   · ¿se aplicó f_k? no → 1
   · sí → escala la duda a ↑k                                origin = ESCALATED
4. no hay ↑k, o ↑k no decide         → g_k nombrado            origin = CONTEXT
```

**Recursión:** los parámetros de Regla_k (κ_k, ε_k, P_k) son candidatos de Regla_{k+1}, es decir, calibrar. **Caso base:** el orden sin ↑k decide con g declarado. Es el arranque en frío.

## Nombres de código (identificadores `.py` en inglés, como los servicios)

- **Módulo:** `services/ckm_trust_rule.py`.
- **Tipos:**
  - `Origin`, con los valores `FIELD`, `TRACE`, `ESCALATED`, `CONTEXT`;
  - `RuleParams`, con `cut`, `tolerance`, `floor`, `calibrated`;
  - `Decision`, con `value`, `origin`, `record`, `reason`;
  - el estado del paso 3 se llama `NO_TRACE` (en la forma escrita, *SIN_TRAZA*);
  - `CkmTrustRule`, con `field_criterion`, `trace`, `context`, `escalate_to`.
- **No se renombra nada de lo que existe.** `criterio_local.py`, sus constantes (`VIA_*`, `MOTIVO_*`, `DECISION_SKIP`) y `UmbralesCriterioLocal` quedan como están. El mapeo de una cosa a la otra se declara, no se reescribe.

## Desalineamientos ya encontrados (entrada del CP0)

delamor: *"el campo continuo no salta; salta la medición; el instrumento NO salta"*. Cada desalineamiento es un lugar donde una instancia de la regla tiene un casillero roto: la medición discretiza o normaliza y el contexto entra como campo. La columna **casillero** dice qué elemento de la forma rompe.

| de dónde | qué | casillero | fuente |
|---|---|---|---|
| **discretizar** | presencia por texto entero; W ≥ 0, sin canal para la ausencia → T = 0 por construcción | f (sin signo) | TASK_tests_instrumento CP3, 10 oct |
| discretizar | marcadores de oposición por substring ("distri**but**ion") aplicados al texto entero | g sin nombre, presentado como f | TASK_tests_instrumento CP1 |
| discretizar | `top_k`, pool `top_k·3`, idf, `TOL_EMPATE`; orden alfabético en el empate | κ, ε; g (I4) | `node_extractor._seleccionar`, REG regla §4 |
| discretizar | dinámica síncrona con N par → órbitas de período 2; el "colapso" de calibrate no colapsa (N_eff ≥ 2 por Z₂) | el patrón de calibrate depende de la paridad de N | juguete de Opus, 10–11 oct (doc tejido) |
| **normalizar** | `W / max_abs` en CorpusService | escala de la medición | `corpus_service.py:332-335` |
| normalizar | `Δ / max(Δ)` dentro de la meseta | escala que salta dentro de la meseta | DECISIONES 10 oct (4): se fija al nacer el ciclo |
| normalizar | **las medias, tres convenciones**: sobre `W>0`, sobre `≠0`, sobre todos | regla desalineada entre sitios | BANDEJA `7abc160` |
| normalizar | `coco._beta_c` → `inf` y `beta_c_landscape` → `None` para el mismo caso | I2 (ausencia como valor) | BANDEJA `7abc160` |
| **el signo** | Δ se **suma** a W (`_combine_W_Delta`, `coco.observe`): el rechazo del campo entra como co-ocurrencia | origen del negativo | DECISIONES `20247ee` |
| **valores sin origen** | `min_texts=3` (era 10), factor 2, `n=3`, `MAX_CICLOS=10` "provisional", `piso_vueltas=12`, `dt_minimo_s=5.0` | κ, P puestos por alguien: g | DECISIONES `c2a0f1b`, BANDEJA `f3f8cc7` |
| valores sin origen | `min_texts=0` leído como valor → `2·0 = 0` → volumen siempre verdadero | I2: el nulo escrito como 0 | DECISIONES 11 oct |
| **cascada** | estructural > volumen > tiempo en `elif`: el criterio con valor sin origen tapa a los otros | orden de los pasos no es de la regla | `ckm_monitor.py:314-321` |

**Traza previa (delamor, 11 oct):** la revisión ya había empezado. `REG_regla_ckm_trust_v1` §4 (4 oct) es una tabla de los sitios donde la regla ya opera, verificada leyendo. Ahí están `_seleccionar`, el bootstrap, el `NOMINAL` por defecto (paso 4 subrepticio), la cancelación de α, el bootstrap = 12 (sesgo de destino) y los casos de Salamanca. Su §7 dejó para Code un CP1, el inventario de sitios de decisión en `services/` e `iap_chatroom/`, que **nunca se ejecutó** (no aparece en la BANDEJA). El CP0 de este TASK parte de esa tabla y retoma ese inventario: es paso 2, decide la traza. El REG está en la carpeta de delamor (`antropic/trust___project/structure_topology/`), no en el repo. Subirlo es decisión de delamor.

**La PoC del volumen** (la orden de delamor del 11 oct) todavía no está en `origin/main`. Cuando Code la suba, sus hallazgos entran a esta tabla.

## Reglas del TASK

1. **Gate `f96c234`.** Ningún comportamiento vivo cambia. El módulo nuevo es puro y nadie lo llama hasta el CP3.
2. **I2:** la ausencia no tiene valor por defecto. `tolerance` y `floor` faltantes son `None` declarado: nunca 0, nunca un default.
3. **I5:** el paso 3 no resuelve, escala. Sin `escalate_to`, devuelve `ESCALATED` con `escalate_to=None` y quien llama decide. No cae al paso 4 solo.
4. **Docstrings en el mismo commit** (regla del 10 oct). Si el código y el docstring difieren, se declara.
5. **Archivos nombrados uno por uno** al commitear, sin `git add -A`.

## Checkpoints

| CP | qué | reporta |
|---|---|---|
| **CP0a** | Sin código. **Identificar los órdenes de escala** y su contigüidad. Criterio propuesto (Opus): un orden es lo que queda fijo mientras el de abajo varía. Por ejemplo σ por mensaje sobre W fija, W por meseta, condiciones por ciclo de calibración. | Lista de órdenes, qué queda fijo en cada uno, cuál es el ↑ de cada uno, y dónde no se pudo decir. |
| **CP0** | Sin código. Escribir cada instancia en la forma: `criterio_local`, `should_rebuild`, `calibrate`, `NodeExtractor._seleccionar`. Tabla con un casillero por elemento, citando archivo y línea. | Los casilleros vacíos, usando como entrada la tabla de desalineamientos (Opus vio: ε falta en criterio_local y en should_rebuild; P falta en calibrate; el volumen es un g sin nombre) y las instancias que **no entran en la forma**. Si una no entra, se reporta, no se fuerza: puede fallar la forma o la instancia. |
| **CP1** | `services/ckm_trust_rule.py`, puro, con tests de la forma: los cuatro orígenes, el empate con ε, **`tolerance` obligatoria (sin default; `None` sólo declarado y registrado)**, el piso que lleva de 2 a 3, `None` declarado, el paso 3 sin `escalate_to`. | Verde, xfail o lo que no se pudo testear. |
| **CP2** | Expresar `CriterioLocal` como instancia de `CkmTrustRule` **en un test**, sin tocar `criterio_local.py`. Mismas entradas, mismas decisiones, mismos motivos que hoy, sobre `experiments/vivo_03_criterio_local_log.json`. | Bit a bit igual, o la lista de diferencias. Cada diferencia es una diferencia entre la forma y la instancia, y se reporta sin elegir. |
| **CP3** | **Sólo con orden de delamor:** que `criterio_local.py` instancie el módulo. | — |

## Fuera de este TASK

- `should_rebuild` y `calibrate` como instancias en código: se ven en el CP0, pero no se implementan.
- Elegir ε, P o cualquier valor sin origen: es calibración.
- El signo de Δ, las medias.
