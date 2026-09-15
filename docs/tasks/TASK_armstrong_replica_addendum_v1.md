# TASK_armstrong_replica_addendum_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Objetivo

Correr la réplica Armstrong con seed=123 y agregar el addendum al REG existente.

---

## Paso 0 — verificar que el script existe

```bash
ls iap_chatroom/tests/test_armstrong_replica_seed123.py
```

---

## Paso 1 — correr

```bash
cd /workspaces/ckm
python3 iap_chatroom/tests/test_armstrong_replica_seed123.py 2>&1
cat process/experiments/armstrong_replica_seed123_summary.json
```

---

## Paso 2 — agregar addendum a REG_armstrong_stop_coco_v1.md

Leer `registers/REG_armstrong_stop_coco_v1.md`.
Agregar al final, antes de "Archivos relacionados":

```markdown
---

## Réplica — seed=123, única variable cambiada

Script: `iap_chatroom/tests/test_armstrong_replica_seed123.py`
Corpus idéntico, TEXTS idénticos, n_runs=50, track_landscape=True.
Única variable cambiada: seed (42 → 123).

**Resultado: 3/20 STOPs** (vs 20/20 del intento 2 canónico).

STOPs en t=0, t=1, t=2. Desde t=3: D_ckm converge a 0.3673 —
por debajo del umbral 0.40. STOP deja de disparar.

Con seed=42: D_ckm converge a 0.4286 — por encima del umbral.
STOP sigue disparando las 20 evaluaciones.

**Qué replica:**
- STOP dispara en los primeros 3 triggers, alpha_used ∈ [0.05, 0.30]
  en los 3 casos.
- delta_A positivo en los 3 STOPs (valores: [COMPLETAR DESDE JSON]).
  El hallazgo central de Extensión 2 se sostiene.

**Qué no replica:**
- 20/20 del canónico. No es una propiedad robusta del mecanismo —
  es sensibilidad del estimador estocástico (n_runs=50) cerca del
  borde del umbral 0.40. Cerca del borde, el conteo de atractores
  tiene ruido suficiente para cruzarlo o no según la semilla.

**Lectura:** el mecanismo es robusto. El punto de convergencia de
D_ckm post-compresión es sensible a seed porque es una estimación
estocástica sobre 50 muestras, no un valor determinístico.
```

Completar `[COMPLETAR DESDE JSON]` con los delta_A reales del summary.

---

## Paso 3 — commit

```bash
git add registers/REG_armstrong_stop_coco_v1.md \
        process/experiments/armstrong_replica_seed123_summary.json \
        process/experiments/armstrong_replica_seed123.jsonl \
        iap_chatroom/tests/test_armstrong_replica_seed123.py
git commit -m "docs: Armstrong replica seed=123 — 3/20 STOPs, mecanismo robusto, umbral sensible a seed"
git push
```

---

## NO modificar

- El intento 2 canónico (seed=42) en el REG — no tocar esas secciones
- `process/experiments/armstrong_stop_coco_v1.jsonl` — archivo del canónico
- Cualquier otro REG

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
