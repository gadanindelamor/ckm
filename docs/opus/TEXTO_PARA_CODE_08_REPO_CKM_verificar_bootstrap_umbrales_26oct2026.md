# Texto para Code — 08 — repo ckm — verificar la cadena bootstrap / calibrate / umbrales — 26 oct 2026 (Opus 5.5)

*delamor lo pega en el prompt de Code (Codespace, repo `ckm`). Bloque completo y autocontenido.*

```
Code: verificación, no implementación. Nada de lo de abajo cambia el comportamiento del código.

0. ARRANQUE
- En el Codespace, el git pull --rebase y el push los hacés vos (delamor no).
- Leé primero docs/opus/decisiones_en_el_acto.md, entradas del 26 oct desde
  "Respuestas de delamor al Feedback X" hasta el final. Ahí está lo que Opus y
  delamor encontraron hoy, con file:line. Varias lecturas de Opus fueron
  PARCIALES (sólo funciones, no archivos enteros): están marcadas.
- Regla de lectura: los .py se leen completos, docstring y código; 1 vez si es
  sólo lectura, 2 veces (antes y después) si escribís. Divergencias
  docstring/código se declaran.
- Antes de empezar: evaluá este texto contra el repo y reportá tensiones.

1. LO QUE TENÉS QUE VERIFICAR (confirmar o corregir, con file:line)

V1. El nacimiento de la primera W, hoy (main con el revert 7040a02).
    Leé completos iap_chatroom/ckm_monitor.py y services/corpus_service.py.
    Describí el flujo del mensaje en que nace W: qué condiciones lo permiten
    (min_texts, min_devices_first_w, rebuild_suspendido, no_rebuild_reason),
    quién la construye (ingest), y por qué no se entra al bloque de la
    decisión ni a _calibrate. Después, lo que cambiaba a7d065f.
    Criterio de delamor para evaluarlo: "build del bootstrap" es CONSTRUIR LA
    PRIMERA W CALIBRADA, con su condición (bootstrap verdadera);
    should_rebuild y rebuild son del flujo en régimen. Si la implementación
    del bootstrap usa la maquinaria del rebuild, ¿contradice ese concepto?
    Reportá dónde sí y dónde no. Si ves un flujo donde el build del bootstrap
    va separado, DESCRIBILO; no lo implementes.

V2. Hay TRES D_ckm (misma fórmula, distintos argumentos). Confirmá o corregí:
    - Monitor: baseline W + Δ_r, se resetea cuando cambia W, n_runs propio.
    - COCO: baseline W sola, fijada al nacer el COCO del ciclo, lee el Δ_r de
      Monitor, n_runs de la Config.
    - calibrate: baseline la W candidata, deformación artificial (λ hacia el
      colapso), n_runs = 200 (Monitor la llama sin pasarle la Config).

V3. n_runs. Leé services/monitor_service.py completo. Opus vio que Monitor
    cuenta con su parámetro n_runs_attractors (:128, :875, :941) y no con la
    Config, mientras COCO toma la de la Config (:670-676). El docstring de
    ckm_landscape_config.py dice "n_runs y seed son UNO SOLO para Monitor y
    COCO". Confirmá o corregí. NO lo arregles: depende de una decisión de
    delamor (defaults de LandscapeConfig).

V4. Por qué COCO cae en 0.40 / 0.60. La cadena que encontró Opus:
    ckm_monitor.py:282 pasa coco_config={"track_landscape": True}, sin
    umbrales → COCO nace con kw = coco_config + Config → el constructor de
    COCO pone el default (coco.py:147-149) → los umbrales sólo entran por
    set_coco_thresholds y sólo si calibrate devolvió números
    (monitor_service.py:520-529). Dos casos sin aviso:
      (1) calibrate no separa → COCO hereda lo que hubiera (default, o la
          vara calibrada para OTRA W); FRAC_REC_MIN "UNKNOWN" se filtra;
      (2) primer ciclo → no hay calibrate → default.
    Confirmá o corregí. Y MEDÍ, sobre las trayectorias de los intentos 2 y 3
    (experiments/_state_S2-C0/monitor_trajectory.jsonl y el .bak del intento 2
    en process/): por cada ciclo, qué umbrales usó COCO, de qué calibración
    salieron (su w_sha) y cuál era la W viva. ¿El panel dice de qué W salió la
    vara, o sólo "calibrate" / default?

V5. La curva de λ. De las mismas trayectorias, extraé la curva completa de
    cada calibración (λ, n_eff, d_ckm, frac_rec, los 5 puntos), y poné en la
    misma tabla dónde quedan 0.40 y 0.60. Sólo la tabla y lo que se ve; sin
    nombrar qué significa.

V6. Divergencias de docstring ya encontradas. Reportá el estado de cada una:
    - _calibrate cita docs/REG_borrador_calibrate_no_corre_en_el_build.md,
      que ahora es registers/REG_calibrate_no_corre_en_el_build_v1.md;
    - set_coco_thresholds dice "después de un rebuild"; _calibrate dice que
      calibra "antes de instalarla";
    - ckm_monitor.py:82-83 y :326 ("no hace nada"), del REG del calibrate §5.
    Podés corregir SÓLO estos docstrings (sin tocar código), en un commit
    aparte que nombre cada una. Lo demás, sólo reportar.

2. LO QUE NO SE HACE
- No reaplicar a7d065f. No tocar las 13 de test_should_rebuild_conectado.py.
- No cambiar calibrate, el margen, los defaults ni la Config.
- No correr el vivo.

3. REPORTE
- En docs/tasks/BANDEJA_code.md, una entrada por V1–V6: confirmado /
  corregido (con file:line) / no pude verificar (y por qué). Sin veredicto
  global.
- Commit nombrando archivos, pull --rebase y push.

A1.PAUSA al terminar el reporte. Lo lee Opus antes que delamor.
```
