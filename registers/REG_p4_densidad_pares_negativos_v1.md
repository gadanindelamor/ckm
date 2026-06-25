# REG_p4_densidad_pares_negativos_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*p4_neg_sweep.py — N=64, W_base sintética mode='dense'*
*Clase R*

---

## Pregunta

¿Por qué P4 se debilita en N=64 con los 18 pares negativos del corpus CKM?
¿Es dilución por densidad de pares, o estructura k-core?

---

## Resultado

**k* = 54 (ratio = 0.0268)**

| k | ratio | ventaja W_mixta | estado |
|---|-------|-----------------|--------|
| 18 | 0.0089 | −0.000498 | ✗ ← situación N=64 original |
| 36 | 0.0179 | −0.000404 | ✗ |
| 54 | 0.0268 | +0.000068 | **✓ ← k*** |
| 60 | 0.0298 | +0.000282 | **✓ ← fourforums real** |
| 72 | 0.0357 | +0.000502 | ✓ |
| 108 | 0.0536 | +0.001239 | ✓ |
| 144 | 0.0714 | +0.002829 | ✓ |
| 180 | 0.0893 | +0.003136 | ✓ |

---

## Hallazgo principal

**P4 se debilita en N=64 por dilución de densidad de pares negativos.**

Con N=64 y 18 pares negativos reales (ratio=0.009), el umbral k*=54
no se alcanza. La ventaja de W_mixta no aparece.

Con 60 pares negativos reales de fourforums (ratio=0.030), k*=54 se supera
y P4 confirma. El mecanismo es densidad, no k-core.

---

## Convergencia con REG_mu_W_estructura_pares_v1.md

H2 (dilución P4 en N=64) fue cerrado independientemente por composición μ_W:
- N=64 agrega nodos periféricos (Grupo B) que reducen μ_W global
- Aquí: la misma conclusión desde densidad de pares negativos
- Dos caminos independientes, misma causa estructural

---

## Respaldo empírico de P4

Los 60 pares negativos de `neg_pairs_config_fourforums_v8h.json`
(extraídos de mturk_2010_qr_task1_worker_response, gun control, N=304 autores)
son suficientes para confirmar P4 en N=64.

P4 no está refutada — está condicionada a densidad mínima de tensión estructural:
**ratio_neg ≥ 0.027** (k* / total_pairs en N=64).

---

## Script

`experiments/p4_neg_sweep.py` — K_VALUES = [18, 36, 54, 60, 72, 108, 144, 180]
W_base: sintética mode='dense' (4 clusters, within=0.10–0.25, between=0.01–0.05)
N=64, N_LEVELS=20, N_SUBSETS=80, SEED=42

---

## Pendiente

- Verificar k* con W_base real de fourforums (cuando disponible)
- G1 con N ≠ 32 requiere verificación análoga (ver REG_hint_next_instance_v4)

*Clase R · Jun 2026*
EOF
