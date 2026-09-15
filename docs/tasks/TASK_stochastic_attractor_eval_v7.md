# TASK_stochastic_attractor_eval_v7.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

*v7 changes from v6:*
*— Corrige run_hash: incluir `weighted` en el input del hash.*
*— Re-ejecuta run_pair (H2) con weighted=True.*
*— Evalúa bug de idempotencia en __main__ y reporta sin tocar.*

---

## Paso 0 — obligatorio

Leer literalmente:
- `experiments/stochastic_attractor_eval.py` — estado actual post-v6.
- `registers/REG_stochastic_eval_v2.md` — estado registrado.

Reportar qué cambió v6 respecto al archivo subido como referencia.
No asumir nada del estado del repo.

---

## Objetivos

### 1 — `run_hash` incluye `weighted`

En `run_one` y `run_pair`, el campo `weighted` debe entrar en el input
del hash. Objetivo: dos corridas con los mismos (seed, n_runs, W) pero
distinto `weighted` producen hashes distintos.

### 2 — `run_pair` re-ejecutado con weighted=True

H2 quedó en uniforme. Correr con weighted=True, mismos parámetros que
la corrida H2 anterior. Output en `process/experiments/stochastic_eval/`
con timestamp nuevo.

### 3 — Bug __main__

Evaluar el bug de idempotencia (_smoke_corpus_state.json persistente).
Reportar causa y opciones. No tocar sin instrucción.

---

## Criterio de éxito

```bash
python tests/test_coco.py    # 28/28 sin regresión
```

Índice sin colisiones entre corridas uniform/weighted para mismos
(seed, n_runs, W_sha).

---

## REG

Actualizar `registers/REG_stochastic_eval_v2.md` con sección nueva.
No crear archivo nuevo.

---

## NO commit

No hacer commit de ningún cambio. Reportar qué se hizo y esperar
instrucción de delamor antes de cualquier acción sobre git.

---

## NO modificar

- `services/coco.py`
- `tests/test_coco.py`
- REGs históricos
- Ningún archivo en `process/` existente

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
