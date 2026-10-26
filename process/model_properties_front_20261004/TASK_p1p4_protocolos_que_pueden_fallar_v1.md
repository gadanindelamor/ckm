# TASK_p1p4_protocolos_que_pueden_fallar_v1

*Clase T — BORRADOR — 4 oct 2026 — redacta Claude Opus 5.5 (Cowork) a pedido de delamor ("relajen, hagan lo que corresponda").*
*Para Claude Code, Codespace `ckm`. Ejecutar sólo con OK de delamor. Checkpoints en cada paso.*
*Antecedentes: `OBS_P1_run_P1_y_coercitividad_04oct_v1.md` (ckm___memories) · `docs/CKM_Modelo_Hibrido.md` · `experiments/ckm_p1p4_module.py` · `readme/EXPERIMENTS.md`.*

---

## 0. Qué se pide

Para cada propiedad P1–P4: un protocolo que **ejercite la dinámica** que el Modelo Híbrido dice que la produce, con un **nulo** que pueda dar "no", y una corrección por comparaciones declarada **antes** de correr. No interpretar: medir y registrar.

**No tocar** `ckm_p1p4_module.py` ni `hopfield.py` (son traza de abril). Driver nuevo en `experiments/`. Si algo se pule, vuelve a `services/` por CONVENTIONS con test y docstring.

## CP0 — leer y reportar tensiones (sin ejecutar)

Verificar contra el repo lo que dice la OBS: `run_P1` sin `relax`; `add_steps` fijo en 0 en `run_P3`; `run_P4` sobre subconjuntos aleatorios; `np.interp` sobre ρ decreciente en `hysteresis_loop`. Buscar si existen `exp_p1_histeresis.py` / `ckm_viz_v1.py` y qué código produjo EXPERIMENTS.md y REG_p1p4_*. Reportar.

## P1 — histéresis con relajación

- UP: σ todo −1. Incorporar nodos de a uno en un orden dado, **fijándolos** (clamped, campo externo) y **relajando el resto** con `landscape_engine.relax` (síncrono, GOLES). Medir c(S) y ρ_efectivo del estado relajado.
- DOWN: σ todo +1, retirar (fijar en −1) en el mismo orden, relajar, medir.
- Estadístico: área del lazo en ρ de control; diferencia de ρ_efectivo a igual ρ de control.
- **Nulo:** W barajada conservando grado y signo; mismo protocolo. ¿El área de W real cae fuera del nulo?
- Expectativa declarada (Opus): en W positiva el lazo aparece por física de Ising con campo — **probablemente también en el nulo**. Si es así, P1 es propiedad del modelo, no del corpus. Ese es un resultado, no un fracaso.

## P2 — cascadas

- Ajuste de ley de potencia con test de bondad (Clauset–Shalizi–Newman) y comparación por razón de verosimilitud contra exponencial y lognormal. Declarar el rango de tamaños disponible (N acota).
- θ elegido antes de correr, o todos los θ con corrección.
- Nulo: W barajada.

## P3 — asimetría temporal

- **Implementar la rama de adición** (hoy fija en 0): readición del nodo con sus aristas originales, contar rondas de expansión del k-core (o pasos de relajación Hopfield tras incorporar vs tras retirar, si se elige la versión dinámica — declarar cuál).
- Nulo: W barajada.

## P4 — densidad óptima

- Dato de partida (verificado por linealidad y simulación): con subconjuntos aleatorios, Ω* interior ⇔ media(W_mixta) < 0, en ρ≈0.5, para cualquier ubicación de los pares negativos.
- Protocolo dinámico: c(S) de **estados relajados** con densidad controlada (clamping parcial), W_mixta real vs W_mixta con los **mismos números** de pares negativos ubicados al azar (nulo de ubicación).
- Pregunta: ¿la ubicación estructural de los pares negativos importa, o sólo su suma?

## CP final — REG borrador fuera de `registers/`

Tabla por propiedad: protocolo · nulo · resultado · ¿pasa el nulo? · comparaciones totales. Salga como salga.

## Lo que Code NO hace

No modifica los módulos de abril. No toca la Clase R. No reescribe el paper. No decide si P1–P4 son "del modelo" o "del corpus": registra lo que dan los nulos.
