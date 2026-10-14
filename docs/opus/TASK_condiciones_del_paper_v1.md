# TASK_condiciones_del_paper_v1

*14 oct 2026. Opus 5.5 (Cowork), con el marco de delamor del 14 oct. Para Code, en el Codespace. Reemplaza a `TASK_tests_instrumento_v1` (que queda como traza; su CP6 está hecho). Leído contra `fb2b87a`.*

## Por qué
El paper v29 tiene que decir, como **condición declarada**, en qué rango vale lo que afirma. Cada CP de esta TASK produce **un número o una propiedad que va al paper**. Ninguno arregla nada.

delamor (14 oct): *"una vez que esté estable, digamos: definimos sin complicarla, bueno, está estable dentro de este rango, con estas dependencias observadas, y ahí te despachás con suites con drivers matemáticos."*

## Reglas
1. **Sin regresiones, sin compatibilidad hacia atrás.** La única versión es la actual.
2. **No se arregla nada.** Lo que el código hace se mide y se reporta.
3. **No se toca el gate** (`f96c234`). Nada vivo cambia.
4. Predicción con número commiteada **antes** de correr. Archivos nombrados uno por uno. Un REPORTE por CP en la BANDEJA.
5. Corpus: **sólo los del repo**. Los de `ckmdatasets` (fourforums, CreateDebate) **sólo con orden de delamor** (CP-N).
6. Donde se duda: **A1.PAUSA**, reportar, esperar.

## Checkpoints

### CP-T — Teorema de presencia · `tests/test_teorema_presencia.py`
*(era tests_instrumento CP3)*
Con textos sin marcadores (o `force_w_pos=True`), sobre los corpus del repo: ningún Wᵢⱼ < 0; 0 triángulos con producto de signos < 0; T(W) = 0. Es una **propiedad del modelo** (va a §4/§5.2, con P1/P4), no de un corpus. Si falla, el instrumento hace otra cosa que la matemática: A1.PAUSA y reportar.

### CP-E — Rango de estabilidad · driver en `experiments/` + REPORTE
*(era tests_instrumento CP4; usa lo medido en CP6)*
Lo que ya se sabe (CP6, campo plantado, 12 oct): ‖ΔW‖ decae como 1/n con el campo quieto (de 0,34 a 0,02 en 30 pasos); N_eff fue función de la partición, no de los pesos, desde el paso 5.
Medir, sobre los corpus del repo, **cuánto se mueve N_eff** al variar, de a una por vez: `top_k`, tamaño del pool, lista de stopwords (la actual vs. sólo NLTK vs. sólo sklearn), un texto más con vocabulario ya visto. Con varias seeds de muestreo, reportando dispersión.
Salida: una tabla **"N_eff estable dentro de este rango, con estas dependencias"**, lista para el paper. **No se fija umbral.**

### CP-M — Nulo de marcadores · driver en `experiments/` + REPORTE — **opcional**
*(era tests_instrumento CP1; review v28 M4)*
Mismos textos, misma cantidad de textos marcados como oposición, pero la marca puesta en textos **al azar** (varias permutaciones). Comparar la caída de N_eff (W_pos → W_mixta) con la marca real y con las barajadas.
Opcional porque el paper afirma lo que pasa **bajo** el procedimiento de marcadores (declarado). El nulo sirve a quien quiera interpretar el signo como "oposición" — interpretación que es del lector.

### CP-N — Nulos de P5 y P7 — **sólo con orden de delamor**
*(review v28 M7)*
P5: réplicas por seed con su dispersión. P7: nulo que preserva grados en Δ. Usa fourforums/CreateDebate (`ckmdatasets`): **no se arranca sin orden de delamor.**

## Orden
CP-T → CP-E → (CP-M si delamor lo quiere) → (CP-N con orden).

## Sale de `TASK_tests_instrumento_v1`
- **CP2** (SYSTEM fuera del corpus): ya está en el código desde F3b (`ckm_monitor.py:284-312`). "SYSTEM es campo" quedó abierto por delamor, sin apuro.
- **CP5** (declaración de la W): pasa a `TASK_declaracion_extraccion_v1`.
- **CP7** (disparo de COCO): en pausa con la calibración; COCO no es núcleo del paper.
