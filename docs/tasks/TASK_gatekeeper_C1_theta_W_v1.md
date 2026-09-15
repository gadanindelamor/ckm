# TASK_gatekeeper_C1_theta_W_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v4.md, Paso 3 (D1). Precondiciones: TASK_CKMlandscapeConfig_v1 (`450e7ba`), TASK_landscape_config_en_runs_v1 (`6606b7c`).*

---

## Qué hacer

Llevar **solo C1** del gatekeeper a `services/`, como función que recibe `theta_W` declarado. C1 evaluable por primera vez sobre `W_ckm_corpus_v2.json`.

C1 (`process/initial_static_model/core.py`, semántica sin cambios):

```
max|W(nodo, activos)| ≥ theta_W
```

## Acuerdos (delamor)

1. **θ_W sin fórmula.** Parámetro obligatorio, igual que en CKMlandscapeConfig. `theta_W_formula` sigue en `NotImplementedError`. La segunda propiedad que definiría la fórmula no está decidida — y depende de una partición A/B que en este corpus no está resuelta (ver 4).
2. **N sale de la fórmula.** μ_W se mide sobre la W de ese N; N ya está implícito. Hasta que alguien derive un rol separado.
3. **Solo C1 (opción b).** C2–C4 no se portan: C2 acepta todo (ε supera el rango de c(S)), C3 y C4 no se ejercen (Δ=0, `_n_patterns`=0). "Gatekeeper evaluable" = C1 evaluable.
4. **Núcleo A = los 16 nodos de mayor frecuencia** (`para_counts`), declarado así en el test. La fi de DEFS §7 / REG_mu_W_estructura_pares_v1 (fi ≥ 0.064, CV 0.944, 102×) no se reproduce con este JSON (CV 1.08, 68.6×, mediana 0.020, 5 nodos ≥ 0.064). No se simula que está resuelta.
5. **σ es parámetro del test.** Qué estado activo usar para C1 no está resuelto; no se asume uno. Se evalúa con activos=A y activos=todos, declarados.
6. **W_pos.** `W_ckm_corpus_v2.json` tiene 0 pesos negativos. Todo lo medido es condición W_pos.

## Verificación

Sobre `W_ckm_corpus_v2.json`, para cada σ declarado:

- Con `theta_W = 0.10`: A pasa 0/16 — reproduce el hallazgo previo.
- Con `theta_W` ≤ 0.01399 (mínima conexión de A): A pasa 16/16.
- Semántica idéntica a C1 de `core.py` sobre los mismos nodos y σ.
- Tabla de medición (valores declarados, no fórmula): μ_W_global, 0.1·max|W|, μ_W_nonzero, 2·μ_W_nonzero → cuántos de A y de B pasan.

## Qué no hace

No decide θ_W. No porta C2–C4. No conecta C1 a CorpusService ni a Monitor. No toca `core.py`.

## Abierto

- Segunda propiedad que define θ_W.
- Definición de fi / partición A/B en este corpus.
- σ con el que se evalúa C1 en operación.
- Medición en W_mixta.
