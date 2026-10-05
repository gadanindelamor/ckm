# BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1

**Clase R — BORRADOR. Fuera de `registers/`.** Entra a `registers/` sólo con el OK de delamor.
*5 oct 2026 — gadanin.delamor + Claude Opus 5, Codespace `ckm` @ `f8e0783`.*

**Qué cierra:** P1 y P4 sobre una W snapshot no negativa. **No** cierra P1–P4 como propiedades
del Modelo Híbrido.

---

## 1. Lo que se cierra

**P1 (histéresis) y P4 (densidad óptima) no son testeables sobre una W snapshot con W ≥ 0.**
No es que los tests de abril fallaran. Es que la premisa `force_w_pos=True` decide las dos
respuestas antes de correr cualquier cosa.

- **P1.** Con W ≥ 0 no hay frustración: σ = todo +1 es mínimo global y absorbente. La rama DOWN
  del protocolo del 4 oct no puede salir de ahí. **Medido acá**, 3 corridas sobre
  `process/experiments/W_ckm_corpus_v2.json` (N=32, min(W)=0.0, cero negativos):
  `md ≡ 1.0` exacto en todas, y `A = 1 − mean(m_up)` a cuatro decimales (0.3172 / 0.3040 / 0.3078).
  Una rama constante no es una rama. El estadístico A no es área de lazo: es cuánto le falta a la
  rama UP para saturar.
- **P4.** Por linealidad, E[c(S)] = media(W)·g(ρ), con g igual para todo par. Ω* interior ⇔
  media(W) < 0. Con W ≥ 0, ρ* = 1.0 siempre. Verificado por el operador en la
  `OBS_P1_run_P1_y_coercitividad_04oct_v1` §6 (20 pares → ρ*=1.0; 30 → 0.509; 60 → 0.541,
  según el signo de la media, no según dónde estén los pares negativos).

**Una sola premisa cierra las dos.** No son dos propiedades mal medidas: es una premisa medida
dos veces.

## 2. Lo que se cierra por falta de substrato

De las cuatro, tres piden tiempo: **P1** historia, **P2** propagación, **P3** flecha temporal.
Un snapshot de W no tiene ninguna de las tres. Lo único que un snapshot puede contestar es de
forma P4 —promedios estáticos— y eso es aritmética de media(W).

Por eso el ciclo de cuatro pasadas no se cerraba: cada instancia buscaba un test mejor, y lo que
faltaba no era un test.

## 3. Desde dónde se miró

- `find` sobre todo el árbol incluido `process/` y lo no trackeado, y
  `git log --all --diff-filter=A` sobre todas las ramas: `exp_p1_histeresis.py` y `ckm_viz_v1.py`
  **nunca entraron al repo**. Los números de `readme/EXPERIMENTS.md` y
  `docs/work_reports/CKM_Informe_Trabajo_v32.md` §64.4 no tienen código recuperable.
- `experiments/ckm_p1p4_module.py` **no es lo que midió**: es reconstrucción posterior. Nada en
  el repo lo marcaba como tal.
- `P1P4/verificacion_p1_p3.py` (4 oct, contenedor Cowork) **sí está**, recuperado el 5 oct con su
  log. Su pre-registro está en el docstring, escrito antes de correr. Leído completo.
- Las tres corridas de §1 son propias, en este Codespace, hoy.

## 4. Lo que este REG NO dice

- No dice que P1–P4 sean falsas. Dice que W_pos snapshot no es condición para preguntarlo.
- No dice que el driver del 4 oct no pueda fallar: puede, y W_nuevo no pasó.
- No toca N_eff contra enumeración exacta, SALAMANCA, D3, ni la D_ckm canónica (`dabd1ed`).
- No toca P2 ni P3 más allá del substrato: su medición sobre snapshot quedó NO MEDIBLE en el
  `INFORME_verificacion_P1_P4_v2.md` §5 y §4, por N=32 y por reversibilidad matemática del k-core.

## 5. Lo que queda abierto, y es otra pregunta

**P1–P4 sobre el modelo dinámico.** Las mismas cuatro, sobre W que evoluciona. La regla de
Aiyappa, Flammini & Ahn (2024) —Δb ~ N(α·b_emisor + β·b_y·b_z, σ²)— tiene término triádico, que
genera pesos de los dos signos: la frustración **aparece de la dinámica**, no se pone a mano con
una `W_mixta`.

No hay resultado de abril al que llegar. Por eso esta pregunta sale del ciclo.

A revisar antes de escribir una línea de código:
1. **Comparabilidad de ramas.** Con W móvil, la W al final del UP no es la del arranque del DOWN.
   Parte de cualquier lazo sería eso. Declarar antes qué se fija y qué corre.
2. **Literatura.** Histéresis en Hopfield **con aprendizaje** puede estar publicada. Si lo está,
   es replicación declarada, no hallazgo.
3. **Citar a Aiyappa de frente**, con repo y commit (`rachithaiyappa/beliefnet` @ `2289c39`).

La TASK se escribe de cero. No se copia y pega del driver del 4 oct.

## 6. La condición que hacía el ciclo

1. Un test que no puede fallar en la dirección que importa.
2. Queda registrado como CONFIRMADA (`REG_p1p4_ckm_v25_corpus.json`, META_REG v5).
3. La verificación llega después y desde afuera. Nunca desde donde se corrió.
4. **No había REG que lo cerrara.** "No testeada" no cierra nada, así que se reabría.

Este borrador es el 4.
