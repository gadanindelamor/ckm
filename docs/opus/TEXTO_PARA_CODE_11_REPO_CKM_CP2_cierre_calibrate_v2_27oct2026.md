# Texto para Code — 11 — repo ckm — CP2 y cierre de TASK_calibrate_en_el_build_v2 — 27 oct 2026 (Opus 5.5)

```
Code: OK de Opus a CP2 de docs/tasks/TASK_calibrate_en_el_build_v2.md, y
cierre de la TASK al terminar CP2. Por favor, en este orden.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, del 27 oct, desde
  "Reporte de CP1 (BANDEJA" hasta el final: ahí están tu CP1 leído y las
  definiciones de delamor para CP2.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Unidad: CP2 entero, de corrido. A1.PAUSA al terminar CP2, antes del cierre.

Definiciones de delamor (27 oct) que CP2 aplica:
- D6': n_runs de calibrate = 1000. Cerrado.
- Defaults de LandscapeConfig: su valor no se define ("cualquiera da lo
  mismo"); lo que importa es que caer en un default se pueda ver. No cambies
  ningún número de default.
- El margen de calibrate (extremos o máximo interno) no se toca. delamor:
  "lo de siempre es el sesgo de querer ponerle el NUMERO conveniente. en vez
  de sostener la tension". Elegir el margen, la grilla o un número para que
  separe es ese sesgo. Por favor sostené la tensión: medí y registrá lo que
  sale, separe o no.

CP2 = D3 + D4 + D6', así:
- D3: el registro de la calibración vive en un lugar de la Config (slot +
  to_dict/from_dict), no dentro del Ciclo. Un solo escritor (el punto
  _calibrar_antes_de_instalar). Contiene valores, estado, condiciones, w_sha
  de la W calibrada, duration_s y blocking. from_dict sobre un estado viejo lo
  lee UNKNOWN, no nulo_calibrado.
- D4: COCO lee su vara de ese lugar, como Threshold de services/ckm_trust_rule.py.
  Calibrado -> MEASURED, con source = calibración + w_sha. Si no -> DECLARED,
  con source = el default de coco.py y la causa (no_calibrado:<causa> o
  nulo_calibrado). Nunca los números de otra W. Si el w_sha del lugar no es el
  de la W que COCO juzga, el panel lo dice.
  Test del caso 1: una calibración que separa seguida de una que no separa NO
  deja la vara vieja.
- D6': n_runs, seed y grilla de calibrate se declaran en ese lugar del estado
  (no como default de función). n_runs = 1000. seed y grilla: los valores de
  hoy, declarados.
- Por favor medí, antes de tocar tests, qué se mueve al pasar a 1000. Un test
  que afirmaba "calibrado" a 200 no se afloja: se declara qué afirmaba, por
  qué se mueve, y se reescribe para afirmar lo que pasa ahora. Lo de los
  vivos (que con 1000 la W del vivo no separa en 10 de 10 semillas) va como
  dato medido, sin predecir el campo.
- Defaults de LandscapeConfig: el docstring dice "obligatorio" para n_runs y
  seed y el código les da default (ckm_landscape_config.py:173-175 contra
  :198-199 y :238-239). Corregí el docstring para que diga lo que hace el
  código. Y verificá, sin implementar el mecanismo general, si hoy caer en
  N_RUNS_DEFAULT / SEED_DEFAULT queda visible en la traza o el panel. Si no
  queda visible, reportalo con dónde y por qué; no lo arregles en esta TASK.
- El 17% (reusar A0 como el punto lambda=0): commit aparte, con un test que
  verifique resultado idéntico con la misma semilla. Si no sale idéntico, no
  entra, y se reporta.

NO: el patrón de calibrate (colapso, grilla, margen), el mecanismo general de
defaults (centinela, inventario), P14, el state_dir por default de CKMMonitor
(E1 de delamor), el docstring E5 de ckm_monitor.py:84-90, el vivo.

Cierre (después de la A1.PAUSA de CP2, si CP2 quedó en verde):
- En docs/tasks/ESTADO_calibrate_en_el_build_v2.md: la TASK queda cerrada en
  CPa-CP2; CP3 (el vivo) fuera, sólo con orden explícita de delamor. Lista
  de lo que la TASK deja abierto, una línea cada cosa: la tensión del
  margen de calibrate, sostenida (no se cambia para que separe), E5 (docstring de la "primera calibración que separa", con
  n_runs=200 seed=0), la divergencia w_version del origen, el mecanismo
  general de defaults, el state_dir por default (E1), P14.
- Registrá en DECISIONES_opus.md las definiciones de delamor del 27 oct de
  arriba (n_runs=1000, defaults de Config, la tensión del margen sostenida).

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos, suite completa (en serie) al cerrar, pull --rebase y push.
A1.PAUSA.
```
