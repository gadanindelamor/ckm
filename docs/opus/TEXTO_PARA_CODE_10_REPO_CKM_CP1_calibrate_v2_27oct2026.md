# Texto para Code — 10 — repo ckm — CP1 de TASK_calibrate_en_el_build_v2 — 27 oct 2026 (Opus 5.5)

```
Code: OK de Opus a CP1 de docs/tasks/TASK_calibrate_en_el_build_v2.md.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, del 27 oct, desde
  "Respuestas de delamor a Code, en el chat de Code" hasta el final. Ahí
  están las decisiones de Opus sobre las tensiones de tu CP0.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- De corrido dentro de CP1; A1.PAUSA al terminar.

CP1 = D1 + D2 + D5, así:
- D1: la primera W nace por su condición propia (_W is None y
  no_rebuild_reason(allow_first_W) is None). No es un criterio de la jerarquía,
  y la jerarquía no cambia.
- D2: calibra el canal (CKMMonitor), desde UNA sola función "antes de
  instalar" que llaman los dos caminos (el origen y el régimen). No desde
  _rebuild: corpus_service es productor y calibrate es instrumento.
- D5: el origen se instala con _rebuild() (causal_event sin cambios) y deja su
  línea en rebuild_decisions.jsonl con causa "bootstrap", escrita aparte, no
  por rebuild_por_decision. Los 3 tests que cuentan decisiones se reescriben
  para afirmar exactamente una línea, causa == "bootstrap", y que sea la única.
  El de cp5 (INERTE) cambia lo que afirma: escribí en su docstring qué afirma
  ahora y por qué (delamor: "cambia el contenido de lo que afirma").
- Divergencia a declarar, sin corregir: w_version sigue marcando el origen
  como "rebuild".
- Tests nuevos: la primera W pasa por calibrate (con su registro), el origen
  tiene su línea con bootstrap, la jerarquía no cambia (las 13 de la PoC en
  verde).
- El n_runs de calibrate NO se cambia en CP1: es de delamor (D6').

NO: CP2 (el lugar de la calibración en la Config, Threshold, duration_s, el
17%), el patrón, el vivo, ni el docstring E5 de ckm_monitor.py:84-90.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commit nombrando
archivos, suite completa al cerrar, pull --rebase y push. A1.PAUSA.
```
