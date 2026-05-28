# REG_hint_next_instance_v1.md

*Mayo 2026 — Hint para próxima instancia. Lo que costó más encontrar.*

---

## Crítico — código

**relax usa W+Delta, no W solo:**
```python
sigma = relax(sigma.copy(), W_start + Delta)  # NO: relax(sigma, W_start)
```
Esto es lo que hace la trayectoria cohesiva funcionar. Sin Delta en la dinámica,
sigma queda frozen en su atractor inicial y nada evoluciona.

**sigma init = all -1 (no random, no all +1):**
W_base (todos positivos) tiene all-1 como punto fijo.
Inicializar con all-1 y relajar con W_base da sigma=all-1 (0 activos).
Eso produce fi=1.000 saturado en W_base — que es el comportamiento documentado,
no un error.

**D_ckm puede y debe ser negativo:**
D_ckm < 0 → A(t) > A(0) → sistema en expansión. Es información real.
El código anterior tenía `max(0.0, ...)` — incorrecto. Remover.

---

## STOP + D_ckm + full_meaning — leer primero

**REG_hipotesis_distancia_contextual_v1.md contiene todo:**
- Definición formal D_ckm: `D_ckm(t) = [A(t₀) - A(t)] / A(t₀)`
- Operador STOP: `Δ → α·Δ`
- Tres condiciones verificadas (exp_stop_operator.png):

```
D_ckm(t) > 0  →  colapso   →  STOP restaura A(t)
D_ckm(t) < 0  →  expansión →  STOP contrae A(t)
D_ckm(t) = 0  →  equilibrio →  perturbación sin dirección
```

- Criterio full_meaning: R(t) > k AND A(0) > θ_A AND T > τ
- Mapa de cuadrantes c(S) vs D_ckm

**No construir desde cero. Leer ese REG primero.**

---

## stop_signal STABLE en tests

Causa: sigma aleatoria por paso, no trayectoria real de agente.
No es limitación de la fórmula. La señal funciona con agente real.

---

## Problema central no resuelto

Δ_declarado ≠ Δ_acumulado. El monitor necesita Δ_declarado
(dependencias explícitas del dominio). Los experimentos usan Δ_acumulado
(trazas de co-ocurrencia proporcional a W). Son el mismo problema que
los métodos de población del CKM. No resuelto.

---

## Archivos que existen en el proyecto

- `ckm_monitor.py` — FabricationService (reconstruido, limitaciones en REG)
- `exp_monitor_trajectory.py` — experimento trayectoria cohesiva
- `REG_monitor_ckm_v1.md` → reemplazado por v2 (correcciones stop_signal + D_ckm)
- `CONDITIONS_experimentos.md` — condiciones requeridas M1/M2
- `W_ckm_corpus_v2.json` — corpus N=32, base para todos los experimentos

## Lo que se perdió en Take your time y no fue descargado

`ckm_monitor.py` original fue creado pero no presentado via present_files.
La reconstrucción tiene divergencias: fi_mixta llega a ~0.90, REG dice 0.69.
Causa probable: parámetros del original no completamente recuperables.

---

## Sobre deriva en conversaciones largas

Conversaciones largas acumulan resonancia. Verificar en documentos
antes de construir. "Lo definiste vos" = ir a buscar, no derivar de nuevo.
AWARENESS A1-A5 aplica al proceso de codear y documentar, no solo a teoria.
