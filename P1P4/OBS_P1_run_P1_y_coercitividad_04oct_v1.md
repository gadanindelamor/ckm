# OBS_P1_run_P1_y_coercitividad_04oct_v1

**BORRADOR — observación, aparte.** *4 oct 2026 — gadanin.delamor + Claude Opus 5.5 (Cowork).*
*Contexto declarado (delamor): P1 se corrió en abril–mayo 2026, antes de que existieran los REG y la metodología. Se lee en ese marco.*
*Mirado en: GitHub `gadanindelamor/ckm` @ `2097ca4`. Simulaciones propias en contenedor Cowork (no código del proyecto corriendo).*

## 1. Qué hace `run_P1` (`experiments/ckm_p1p4_module.py`)

1. 200 secuencias; cada una, una permutación aleatoria `order` de los N nodos.
2. UP: σ todo −1, prende nodos uno a uno en `order`; anota c(S) en cada ρ.
3. DOWN: σ todo +1, apaga nodos uno a uno **en el mismo `order`**; anota c(S) en cada ρ.
4. Por cada ρ en [0.35, 0.70]: Wilcoxon pareado UP vs DOWN.
5. `CONFIRMADA` si el **mínimo** de los p < 0.05.

**No relaja** (0 llamadas a `relax` en la función). c(S) se calcula sobre el estado puesto a mano.
**Ramas intercambiables:** en un ρ dado, UP tiene en +1 los primeros k de la permutación y DOWN los últimos k; invertir la permutación cambia una por la otra → diferencia esperada **exactamente 0 para cualquier W**.
**Mínimo de ~11 p sin corrección.** Simulación (lógica copiada, W simétricas aleatorias, N=16): CONFIRMADA en 17/200 (8%).
**Auto-test** `test_homo_W_no_hysteresis`: con W homogénea UP=DOWN exacto → Wilcoxon lanza excepción → `except: pass` → INSUFICIENTE → pasa. No puede fallar. No existe test que pida CONFIRMADA en W_mixta.
Traza registrada: `REG_p1p4_ckm_v25_corpus.json` → CONFIRMADA, max_Δc(S)=0.000079, min_p=0.0459. META_REG v5: W_base p=0.040, W_mixta p=0.405.

## 2. `hysteresis_loop` (`process/initial_static_model/hopfield.py`)

Tampoco relaja. Órdenes UP/DOWN independientes. La rama DOWN se interpola con `np.interp` sobre ρ **decreciente**; numpy no lo admite y no avisa (verificado: xp decreciente → [9,1,1,1,1] en vez de [1,3,5,7,9]). La rama UP (ρ creciente) está bien.
EXPERIMENTS.md reporta P1 N=32/64 con p≈0 y áreas de lazo; los scripts citados (`exp_p1_histeresis.py`) no están en el repo. No pude verificar cuál código los produjo.

## 3. Coercitividad [0.406, 0.586] — depende de N, no de W

Informe v32 §64.4: cruces de c(S)=0 en la rama UP del lazo P1 (ckm_viz_v1.py, N=32).
Para k nodos en +1 elegidos al azar:

    E[c(S)] = μ_W · ((2k − N)² − N) / (N(N − 1))

cero en **ρ = 0.5 ± 1/(2√N)** → N=32: **0.412 y 0.588**. Independiente de W (salvo μ_W ≠ 0).
Aplicado el operador: W_ckm_corpus_v2 cruza entre 0.375–0.406 y 0.562–0.594; W positiva aleatoria entre 0.406–0.438 y 0.562–0.594.
El número está bien medido; es combinatoria de N, no coercitividad del campo.

## 4. Lo que esto NO dice

- No dice que P1 sea falsa. La histéresis tiene apoyo matemático (Modelo Híbrido, abril 2026; Goltsev–Dorogovtsev–Mendes; Aiyappa et al. 2024). Lo que no la testea es este protocolo.
- No toca P2 ni P4 (no revisados a fondo).
- No toca N_eff vs enumeración exacta, SALAMANCA, D3.

## 5. Un test de P1 que pueda fallar (propuesta, no ejecutada)

UP: incorporar nodo → **relajar** (dinámica) → medir c(S) del estado relajado. DOWN: retirar → relajar → medir. Mismo ρ de control, comparar estados alcanzados. Nulo: W barajada conservando grado. Corrección por comparaciones. Corre en Codespace, como TASK.

## Aparte

- "La charla de Newton" — delamor pidió anotar esto junto a ella. No tengo esa traza en este chat ni en los archivos que leí. Pendiente: ubicarla.

---

## 6. P2, P3, P4 en el mismo módulo (leído después, misma noche)

- **P3 (`run_P3`):** `add_steps.append(0)` fijo — la rama de adición no se mide ("aproximación conservadora"). Mann-Whitney rem > 0 contra ceros: confirma siempre que alguna remoción pode al menos una ronda. **No puede fallar en la dirección que importa.**
- **P4 (`run_P4`):** estados aleatorios, sin relajación, media de c(S) por ρ. Por linealidad: E[c(S)] = media(W) · g(ρ), con g igual para todo par. La curva media depende **sólo de la media de W**, no de qué pares son negativos. Ω* interior ⇔ media(W_mixta) < 0, y cae en ρ≈0.5.
  Aplicado el operador (W_ckm_corpus_v2 + pares −0.10 **al azar**): 20 pares → media +0.00035 → ρ*=1.0; 30 pares → media −0.00180 → ρ*=0.509; 60 pares → −0.00742 → ρ*=0.541. El N=64 reportado (ρ*=0.509) es consistente con esto.
- **P2 (`run_P2`):** τ por MLE sobre tamaños de cascada acotados por N (≤32), 6 θ, "CONFIRMADA si **algún** θ cae en [1.5, 2]". Sin test de bondad de ajuste ni comparación con otras distribuciones; con N=32 no hay décadas para sostener una ley de potencia. Puede fallar, pero pasar no muestra ley de potencia.

**Lectura:** los cuatro tests del módulo de abril no ejercitan la dinámica que la matemática del Modelo Híbrido exige. Eso no refuta P1–P4 como propiedades del modelo; dice que **no están testeadas empíricamente** por este código.

## 7. Siguiente — TASK

`TASK_p1p4_protocolos_que_pueden_fallar_v1.md` (borrador, para Code, Codespace).
