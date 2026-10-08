# ESTADO_monitor_coco_ciclo_orbita_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-08 01:49 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP0 — evaluar contra el repo, sin código.** Cerrado el 2026-10-08. Base: `6152c71`.
Los nueve puntos, reportados en `BANDEJA_code.md`, entrada `REPORTE CP0` de 01:46 UTC.

## Lo que el CP0 encontró, en una línea cada uno

1. **Dos usos vivos de una sola fase**, no los de la lista: `monitor_service.py:168` —el
   principal, de donde salen Δ_r, c_S y fabrication_index— y `mean_cS`, que COCO usa. El
   `relax` de `deprecated_count_attractors` está muerto. **N_eff y D_ckm ya van por órbita.**
2. **`relax(−σ) = −relax(σ)` demostrada fase a fase**, con el empate GOLES como la condición
   que la hace valer, y con las condiciones de punto flotante declaradas.
3. **Un solo usuario vivo de `corpus.coco`**: el canal, y le pide **sólo
   `landscape_history()`**. Es `ckm_monitor.py:104`, no L93.
4. **La configuración no es la misma hoy: Monitor cuenta con n_runs=1000 y COCO con 80.**
5. **β muere con la instancia** y vuelve a None, que es el borde ya bien resuelto. Nada lo
   conserva hoy.
6. El `declarado` de la Config es `sampling_mode` + `scale`. El resto de COCO → **P9**.
7. **Los 80 paneles históricos tienen `thermostat: None`**: la divergencia de los dos COCO no
   está ahí. Lo que sí está, escrito desde una fase, son `n_rejected_pairs`, `rechazados`,
   `c_S` y `fabrication_index`.
8. **Tres bordes vivos del vacío** (`_classify_zone` → "stable", `frac_rec` → 1.0, A0 fijado en
   silencio), **uno latente** (los defaults de `ThermostatState`) y **el borde de
   `landscape_engine:418` no está vivo**: es de la forma deprecada.
9. **77 de los 220 tests** tocan esto. Y los **21 `test_caso_*` del canal no son pytest**:
   recogen 0 items, así que esa cobertura no existe automáticamente.

## En curso

**CP1 — medir lo que hoy se rompe, sin tocar `services/`.** Driver en `experiments/`.
Si esta línea sigue acá en la próxima sesión, el CP1 se cortó: el driver escribe su log con
escritura atómica, así que un `.json` sin `.tmp` está completo y lo que midió sirve.

## Qué espera, y de quién

- **P9 — BLOQUEA — [delamor]:** con qué configuración nace COCO y dónde se declara.
  **Bloquea el CP2, no el CP1.** No propuse default: elegir el `n_runs` cambia lo que el
  instrumento mide (E3).

## Próximo paso

**CP1 — medir lo que hoy se rompe, sin tocar `services/`.** Driver en `experiments/` con
pre-registro en el docstring. No necesita P9.

## Nada quedó a medias

El CP0 era lectura y se cerró entero. No se escribió ni se corrió código. La suite sigue en
220/220.
