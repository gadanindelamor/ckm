# CERRADO — LEER ANTES DE TOCAR `ckm_p1p4_module.py`

**CANDADO.** *5 oct 2026 — gadanin.delamor + Claude Opus 5.*

---

## `ckm_p1p4_module.py` NO MIDIÓ P1–P4. Es reconstrucción.

Es un intento posterior de volver a un resultado ya dado por probado. El código que produjo los
números de `readme/EXPERIMENTS.md` y de `docs/work_reports/CKM_Informe_Trabajo_v32.md` §64.4
—`exp_p1_histeresis.py`, `ckm_viz_v1.py`— **nunca entró al repo**. Verificado con `find` sobre
todo el árbol y `git log --all --diff-filter=A` sobre todas las ramas, el 5 oct 2026.

## P1 y P4 sobre W snapshot con W ≥ 0 NO SON TESTEABLES

Una sola premisa —`force_w_pos=True`— decide las dos respuestas antes de correr:

- **P1:** con W ≥ 0 no hay frustración; todo +1 es mínimo global y absorbente. La rama DOWN no
  puede salir de ahí. `md ≡ 1.0` exacto (medido, 3 corridas, N=32).
- **P4:** E[c(S)] = media(W)·g(ρ) por linealidad. Con media(W) > 0, ρ* = 1.0 siempre.

Y de las cuatro, **tres piden tiempo**: P1 historia, P2 propagación, P3 flecha temporal. Un
snapshot de W no tiene ninguna. Lo único que un snapshot contesta es de forma P4, y eso es
aritmética de media(W).

## Los tests de este módulo no pueden fallar en la dirección que importa

- `test_homo_W_no_hysteresis`: W homogénea → UP = DOWN exacto → Wilcoxon lanza excepción →
  `except: pass` → INSUFICIENTE → pasa.
- `run_P3`: `add_steps.append(0)` fijo. La rama de adición no se mide.
- `run_P2`: "CONFIRMADA si **algún** θ cae en [1.5, 2]". Sin bondad de ajuste.
- `run_P1`: ramas UP/DOWN intercambiables → diferencia esperada exactamente 0 para cualquier W.

## Qué cierra esto, y qué no

**Cierra:** P1 y P4 sobre W_pos snapshot. **No cierra:** P1–P4 como propiedades del Modelo
Híbrido. No toca N_eff contra enumeración exacta, SALAMANCA, D3, ni la D_ckm canónica.

## El candado

`REG_p1p4_ckm_v25_corpus.json` dice CONFIRMADA. **Esa traza quedó cerrada.** Por la regla del
proyecto: *no se reabre algo cerrado sin leer el REG que lo cerró.*

El REG que lo cierra:
`P1P4/BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1.md` — borrador, fuera de `registers/`,
pendiente del OK de delamor para entrar.

## Hacia dónde va el frente

A las premisas nuevas, **sobre el modelo dinámico**, con nombre propio: **no** son P1, ni 2, ni 3,
ni 7, ni 8. Serie nueva, para que nadie las confunda con esta traza.

Orientación completa: `P1P4/ORIENTACION_p1p4_modelo_dinamico_v1.md`.

**No ejecutar este módulo para sostener nada.** Es traza de abril.
