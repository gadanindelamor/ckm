# ORIENTACION_p1p4_modelo_dinamico_v1

**BORRADOR — orientación, no resultado. Fuera de `registers/`.**
*5 oct 2026 — gadanin.delamor + Claude Opus 5, Codespace `ckm` @ `f8e0783`.*

**Marca de este archivo: esto NO midió nada.** Registra desde dónde se miró, qué no estaba,
y hacia dónde apunta el frente. Ningún número de acá sale de una corrida propia.

---

## 1. Qué se perdió, y desde dónde se miró

**De abril 2026 — `exp_p1_histeresis.py`, `ckm_viz_v1.py`.** Producen los P1 de
`readme/EXPERIMENTS.md` (N=32/64, p≈0, áreas de lazo) y la coercitividad del
`CKM_Informe_Trabajo_v32.md` §64.4.

Mirado desde:
- `find` sobre todo el árbol, incluido `process/`, `experiments/` y lo no trackeado → cero.
- `git log --all --diff-filter=A` sobre toda la historia, todas las ramas → **nunca fueron
  agregados**. No se borraron: no entraron.
- Único rastro: cuatro archivos los nombran (v32, EXPERIMENTS.md, `OBS_P1_...04oct`, `TASK_p1p4_...`).

**Del 4 oct 2026 — `verificacion_p1_p3.py`. RECUPERADO el 5 oct 2026.** Lo tenía delamor en su
máquina y lo subió; estaba en la raíz del repo y se movió a `P1P4/`. 181 líneas, con su log
(`verificacion_p1_p3_log.json`: `repo_commit` 2097ca4, seed 0, 200 nulos, 60 órdenes, versiones,
plataforma, `donde: contenedor Cowork`). **No se perdió nada.** Lo que sigue queda como traza de
desde dónde se miró antes de que apareciera.

Es el "Driver principal" según la tabla §0 del
`INFORME_verificacion_P1_P4_v2.md`: arma W_viejo y W_nuevo, aplica los nulos N_perm y N_grado,
corre P1, P2 y P3. Produce la tabla §3 (A real, p de cada nulo).

Mirado desde: `find` por nombre en todo el árbol → cero. Su log tampoco está. La carpeta
`verificacion_p1_p4_04oct/` que cita el `CONDICIONES_...` no existe.

Corrió en el contenedor de Cowork. **El contenedor no es el repo.**

Lo que sí llegó: `nulo_fuerza.py`, `p1_nulo_fuerza.py`, `p1_relajado.py`, `replica_fig5.py`,
`conteo_vs_masa.py`, `dyn.c`, y dos logs (`p1_nulo_fuerza_log.json`, `replica_fig5_log.json`).

## 2. Qué es lo que quedó en el repo

`experiments/ckm_p1p4_module.py` **no es lo que midió.** Es reconstrucción: un intento
posterior de volver a un resultado ya dado por probado. Nada en el repo lo marca como tal.

Eso explica la forma de sus tests, que es una sola forma repetida cuatro veces:
`except: pass` en `test_homo_W_no_hysteresis` · `add_steps.append(0)` fijo en `run_P3` ·
"CONFIRMADA si **algún** θ cae en [1.5, 2]" en `run_P2` · ramas UP/DOWN intercambiables en
`run_P1`, con diferencia esperada exactamente 0 para cualquier W.

No es descuido. Es la forma de un test escrito sabiendo a qué número hay que llegar.

## 3. Las condiciones del ciclo (cuatro pasadas)

1. Un test que no puede fallar en la dirección que importa.
2. Queda registrado como CONFIRMADA (`REG_p1p4_ckm_v25_corpus.json`, META_REG v5).
3. La verificación llega después y desde afuera — otro marco, otro contenedor. Nunca desde
   donde se corrió.
4. El resultado no refuta: deja "no testeada". Y "no testeada" no cierra nada, así que se reabre.

**Lo que rompe el ciclo no es un test mejor. Es la marca:** que cada archivo diga *esto midió*
o *esto intenta reproducir*. Sin esa marca, la quinta instancia vuelve a empezar.

## 4. La orientación

**P1–P4 sobre el modelo dinámico.** No una capa nueva con predicciones nuevas: las mismas
P1–P4, corridas sobre la dinámica que el Modelo Híbrido exige y que W fija nunca pudo dar.
Aiyappa, Flammini & Ahn (2024) aportan esa dinámica (`rachithaiyappa/beliefnet` @ `2289c39`).

Por qué esto sale del ciclo: **no hay resultado de abril al que llegar.** Nadie midió las dos
capas juntas — W que evoluciona por su regla y σ que relaja sobre W. Ellos mueven pesos y no
miden histéresis; el CKM mide histéresis con W fija.

## 5. A revisar antes de escribir código

- **Comparabilidad de ramas.** Con W fija, UP y DOWN comparten W y la diferencia es dependencia
  del camino. Con W móvil, la W al final del UP no es la del arranque del DOWN: parte del lazo
  sería eso, no histéresis. Declarar antes qué se fija y qué corre.
- **Literatura.** Histéresis en Hopfield **con aprendizaje** puede estar publicada. Si lo está,
  es replicación declarada, no hallazgo. Mirarlo antes evita volver a tener la respuesta a la
  entrada, ahora desde otra fuente.
- **Citar a Aiyappa de frente** en el paper (Condición 1 del `CONDICIONES_...`).

## 6. Borde expuesto, aparte del frente

`readme/EXPERIMENTS.md` y `CKM_Informe_Trabajo_v32.md` citan dos scripts que no están en el
repo ni en su historia. Un lector externo que los busque no concluye "se perdió en abril".

## 7. Lo que este archivo NO dice

- No dice que P1–P4 sean falsas. Dice que no están testeadas por el código que hay.
- No toca N_eff contra enumeración exacta, SALAMANCA, D3 — siguen en pie.
- No toca la Clase R. No modifica los módulos de abril.
- Un número sobrevivió a la pérdida de abril por **re-derivarse**, no por reproducirse:
  ρ = 0.5 ± 1/(2√N) → 0.412 y 0.588 para N=32, consistente con el [0.406, 0.586] reportado.
  Es combinatoria de N, no coercitividad del campo.

## 8. Recuperado — 5 oct 2026

`verificacion_p1_p3.py` + `verificacion_p1_p3_log.json` están en `P1P4/`. La pérdida de 2026
fue de abril solamente; la del 4 oct no ocurrió.

**Divergencia a revisar en el log, sin interpretar:** `bonferroni_alpha` dice **0.003125**
(= 0.05/16, la familia de 16 comparaciones de la v1), mientras el `INFORME_..._v2.md` §6 declara
**α = 0.0125** (= 0.05/4, la familia de 4 que la v2 redefine). El log es de la corrida con la
familia vieja. El veredicto de la v2 no depende de eso —W_viejo/N_fuerza da p < 0.005, que pasa
los dos umbrales; W_nuevo/N_fuerza da p = 0.045, que no pasa ninguno— pero el número del log y
el del informe no son el mismo, y queda anotado.

El log tiene además `P2` y `P3` por W, y un bloque `P4`, que este archivo no leyó en detalle.
