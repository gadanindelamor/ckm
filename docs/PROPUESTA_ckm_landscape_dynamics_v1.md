# PROPUESTA — CKM Landscape Dynamics

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Reorganiza `PROPUESTA_capa_analisis_services_v1.md` con las consideraciones
de delamor. Aquella no se reemplaza: queda como testigo de lo que se
propuso antes de este orden.*

---

## Cómo leer esto

**Orden: entender → modelar → implementar → paper.** Concepto y modelo
primero. Revisión, validaciones y patrones después. El paper al final.

Regla de trazabilidad, la misma de DEFS §OP: toda afirmación rastrea a
`DEFS_CKM_estado_actual_v9.md` (vigente), a una decisión de delamor, o queda
marcada **propuesto** / **abierto**.

La Parte I describe **lo que está siendo modelado**, no el código. El código
aparece sólo en la Parte V, estado del repo.

---

# Parte I — CKM Landscape Dynamics

## 1. Dominio

CKM es un modelo formal de dinámica de campos de conocimiento en sistemas de
devices. El dominio son **las interacciones entre devices**; toda propiedad
se evalúa en relación a ese dominio, no al universo de corpora posibles.
*(DEFS §0)*

## 2. W snapshot de W dinámica

El instrumento tiene dos formas *(DEFS §OP)*:

- **S — snapshot:** W estática, un cuadro. Análisis estructural.
- **D — dinámica:** runtime, servicios, regulación.

El campo es continuo. En el canal se **discretiza**: cada interacción es una
muestra, y cada muestra produce una W. La traza de versiones marca dónde hay
cuadro sin guardar el cuadro. Entre dos muestras el campo siguió y la traza no
tiene nada — no es quietud, es no haber muestreado. *(delamor; medido Sep 2026)*

**P1–P4 operan sobre un cuadro mientras COCO sostiene las tensiones.**
*(delamor)* La foto no detiene al campo: se toma de él mientras corre.

## 3. Traza cronológica de las capas

| capa | qué modela | forma | estado |
|---|---|---|---|
| **W estática — P1–P4** | bootstrap formal del modelo: histéresis, cascadas, asimetría temporal, densidad óptima | S | verificado *(DEFS §5)* |
| **Corpus adversariales — P5–P7** | observaciones en corpus externo de dominio acotado | S | operacional, no condiciona validez *(DEFS §6, §X)* |
| **W dinámica — Monitor** | el campo reconstruido por interacción; Δ_r como deformación acumulada | D | implementado *(DEFS §9, §10)* |
| **Termostato** | COCO como regulación térmica: β, β_c, temp_signal, STOP | D | implementado *(DEFS §12)* |
| **COCO regulador** | COCO como componente constitutivo: sostiene las tensiones del campo | D | **abierto** — ver §4 |

COCO-registry —el ledger de capacidades declaradas de IAID, una de las dos
arquitecturas de COCO en THEORY— **es MCP**: externo, lo resolvió otro, y el
canal ya corre sobre él. El COCO de CKM es el lado térmico. *(delamor)*

## 4. COCO no es opcional

DEFS §12: *"COCO no es opcional. Es componente constitutivo del modelo. Un
sistema IAP sin COCO no es CKM en operación; es el instrumento sin su
mecanismo de regulación."*

Y: *"Ciclo de vida de COCO = ciclo de vida de W. COCO con W vieja mide
degradación respecto a un campo que ya no existe."*

**Observado (Sep 2026):** en la serie IAP 0.4–0.15 ningún panel registró
regulador — 0 de 253. Por la definición de §12, el canal operó como
instrumento sin su mecanismo de regulación. Detalle en la Parte IV.

## 5. ODA

*(DEFS §12, verificado v32)*

```
state_{i+1} = A(D(O(state_i)))
```

Tres etapas que no son todas pasos *(delamor)*. Y una condición que no es
etapa: estar, esperando que algo llegue. El device no dispara su propio
ciclo.

**Abierto:** en el diseño de origen *(IAID, doc de trabajo — puede variar)*
la D es de COCO — *"COCO is where decisions are made, devices just perform
actions"*. Hoy la D vive en el device. MAPA_REG lo tiene como transitorio.

## 6. Verificación antes y después de la admisión

R02: *"Weights updated by continuous verification **before and after**
incorporating nodes."* El gatekeeper es el antes; COCO, el después. Una red,
dos momentos. *(delamor)*

R09 no se opone al gatekeeper. Lo que no selecciona es **la perspectiva
activa** — *"The system does not select the active perspective"* (THEORY).
R15 selecciona nodos en la puerta. Objetos distintos. *(delamor)*

*(Una versión anterior de este párrafo planteaba una tensión R09/R15. Venía
del resumen de R09 en el paper, que perdió "the active perspective".)*

---

# Parte II — Criterios de diversidad

Formulación completa, conceptual y técnica:
**`docs/CRITERIOS_diversidad_formulacion_v1.md`**.

Ubicación en el modelo: son análisis del **cuadro**. No alimentan a COCO.
Plano operacional, no validez del modelo *(DEFS §X)*.

**Tres niveles, no uno:**

| nivel | qué mide |
|---|---|
| A — estados y órbitas | cardinalidad y masa del landscape |
| B — nodos | qué nodos habitan los atractores |
| C — clusters | organización interna y resistencia de fronteras |

---

# Parte III — Definiciones propuestas

*Todo lo de esta parte es* ***propuesto***.

## 7. Dinámica del modelo Landscape

A formular después de entender la Parte I. No se adelanta.

## 8. SLA — monitor · corpus · gatekeeper · COCO regulador

Service Level Agreements, declarados en `CKM_Informe_Trabajo_v29/v30` junto a
Supervised Contract Protocols.

La cadena como acuerdo entre servicios: qué garantiza cada uno al siguiente.

**Dos capas del modelo** *(decisión delamor)* — y sólo una es admisión:

- **antes — gatekeeper:** portero binario. Pasa o no pasa. Admite la
  entrada. Criterios C1–C4 (`readme/API_SPEC.md`).
- **después — COCO:** no admite. Digiere, metaboliza lo que ya entró. Lo que
  la relajación rechaza entra a Δ_r, y COCO lo regula.

*(La primera versión de este párrafo llamaba "admisión" a las dos capas. La
segunda no lo es — delamor.)*

**Ingesta** *(delamor)*: evaluación de admisión, con umbral de ciclo. W no
se reconstruye por mensaje: se reconstruye por ciclo, y el umbral decide
cuándo cierra un ciclo.

Relación con lo medido (Parte V): hoy la ingesta reconstruye por mensaje,
sin evaluación de admisión, y COCO vive una sola ingesta. El criterio de
ciclo existe escrito —gradiente de `D_ckm` sostenido— y no está conectado.

## 9. Diseño

A definir después de §7 y §8.

## 10. CKMConfig — variables, parámetros, umbrales, calibraciones

**Todos los parámetros**, no sólo `theta_W`. Primero entender qué modela
cada uno y en qué plano *(decisión delamor)*.

Lo ya visible, sin interpretar:

- se declara *"calibrated on real corpus N=16"*; el corpus operativo es N=32
- `max_iter=1000, seed=42` son los valores del plano estático
- el bloque *3D Score* (`score_threshold`, `alpha/beta/gamma_score`) no tiene
  consumidores en código; `API_SPEC` lo documenta como clasificador de
  atractores, precisión 1.000 en N=16. Tuvo función en el plano estático
- `w_neg=−0.10` es una de las tres vías de introducir negativos *(DEFS §8)*
- μ_W y r se miden al inicio de cada sesión, nunca como constante *(DEFS §13)*

## 11. Criterios de diversidad

Ver Parte II.

---

# Parte IV — Decisiones de delamor

1. **Hebbianos** — sólo en la carpeta destinada al Modelo Estático histórico.
2. **Una sola clase de grafo.** `CKMGraphArrays` si se vectoriza por
   performance; `CKMGraph` si no pesa y es viable. **`core.py` de raíz → a
   `process/`**, como modelo estático inicial. *En espera:* no se puede
   ubicar el core viejo sin saber cuál es el core actual de CKM *(delamor)*.
3. **Admisión** — primero entender MonitorService y el gatekeeper: lo que
   está siendo modelado, no el relato del código. Dos capas en CKM Landscape
   Dynamics.
4. **`theta_W` relativo** — todos los parámetros. Primero entender.
5. **Tres niveles en el paper** — cuando se trate del paper. Primero
   entender, modelar, implementar; el paper al final.

## Premisas de ejecución

*(delamor, Sep 2026 — de acuerdo con esta propuesta, bajo estas premisas)*

1. **Testeo luego de cada paso.** Leyendo docstrings y código, no sólo
   midiendo impacto: *"si uno cambia una rutina compartida mecánicamente,
   sólo leyendo impacto nunca se sabe."*
2. **No romper backwards.**
3. **Una tarea GAP, abierta.** No para imprevistos: para cambios de curso
   previstos, sabiendo que van a surgir divergencias. Ejemplo: la que marca
   las ramas de código no actualizadas — copias que quedaron atrás cuando el
   original cambió.

---

# Parte V — Revisión, validaciones, patrones

*Después del concepto. Punteros, no repetición.*

## Validaciones abiertas

- **COCO con W congelada** — `REG_coco_w_congelada_v1.md` + driver
  `experiments/coco_lifetime_analytics.py`. Clasificado **bug** por delamor.
  COCO nace con W y muere con W *(decisión declarada)*; lo que falla es la
  frecuencia: rebuild por mensaje, no por ciclo. A0 se renueva con el
  rebuild; β se conserva.
- **El canal vivo nunca conectó COCO** — 0 de 253 paneles. Relación directa
  con §4.
- **`temp_signal`** llegó a los devices como `NOMINAL` sin medición durante
  toda la serie.

## Patrones

Formas que se repitieron, sin carga:

- **La copia pierde primero la razón.** El código se copia entero; el
  comentario que dice por qué, no.
- **Una referencia fija tapa un accesor vivo.** Existe cómo pedir el actual;
  se guardó el primero.
- **Un gap enunciado con dos lecturas.** *"Sólo vive en tests"*: que no
  exista o que no actúe. La implementación satisface una; los criterios de
  éxito heredan la ambigüedad.
- **Un default plausible tapa el honesto.** `UNKNOWN` escrito e inalcanzable
  detrás de `NOMINAL`.
- **Un escalar congelado citado como constante.** El conteo de tests se movió
  tres veces en una tarde.
- **Un experimento con nombre de test.** Cero aserciones.
- **El nombre de una carpeta leído como su significado.**

---

# Parte VI — Propuesta de plan

*El estado del repo es del segundo carril: el repo va aparte y después, con
sus criterios generales. Sin cambiar todo — lo que está, por algo está.
(delamor)*

## Estado del repo

- **Capa raíz:** `analytics.py`, `hopfield.py`, `mcp_adapter.py` no importan,
  los tres por la misma línea (`from .core`). `core.py` y `kcore.py` sí.
  Nada en el repo importa la capa raíz.
- **P1–P4:** `experiments/ckm_p1p4_module.py` es función pura de
  `(W_base, W_mixta, nodes)`. No usa el dump. Le falta `networkx`: declarado
  en `pyproject.toml`, sin instalar.
- **Pipelines con SQL** → corresponden a `ckmdatasets` *(regla de delamor)*.

## Resto del plan

Primer paso: **entender** — MonitorService, gatekeeper y COCO como lo que
modelan.

**FabricationService** entra en el mismo paso *(delamor)*: el actual es una
reconstrucción desde un snippet —se declara así en su docstring— y queda en
`process/` como testigo de esa pérdida. Se reescribe con las rutinas actuales
y con la comprensión de qué se supone que hace ese servicio. Primero lo
segundo.

Lo que sigue no se planifica desde acá.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
