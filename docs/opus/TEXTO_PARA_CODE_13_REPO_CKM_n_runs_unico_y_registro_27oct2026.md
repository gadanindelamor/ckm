# Texto para Code — 13 (reemplaza la versión anterior entera) — repo ckm — n_runs y seeds: revisar el concepto e implementar (dirección de delamor) + dos correcciones de registro — 27 oct 2026 (Opus 5.5)

```
Code: tres puntos, en este orden. Por favor.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, del 27 oct, desde
  "CP2, CP3 y el REG del intento 4: leídos por Opus" hasta el final.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Unidad: cada punto. De corrido dentro de cada uno; A1.PAUSA al terminar el
  punto 1 sólo si encontrás una tensión; si no, seguí.

1. n_runs y seeds: revisar si son el mismo concepto, y después implementar —
   dirección de delamor (E3 que subiste en el CP2). delamor, 27 oct: "La
   direccion, es revise. y que implemente lo solicitado coco, monitor, y copia
   de W, usan el mismo n runs (si son el mismo conceptualmente claro) idem
   seeds, etc... Ahora si NO lo son conceptualmente, porque coco tal y cual,
   y en cambio Monitor tal cosa, etc etc. CONCEPTUALMENTE se separan, BABEL".
   Antes había dicho: "si se trata del mismo concepto, n_runs, que se usa como
   variaciones de sigma estados iniciales, y se analiza donde tiende o
   converge... todos leen el mismo concepto". "Copia de W" es su nombre para
   el D_ckm de calibrate.
   1a. Revisión, sin código. Para cada parámetro de muestreo (n_runs, seed y
       lo que encuentres del mismo tipo, por ejemplo la grilla o
       sampling_mode) y para cada uno de los tres (Monitor, COCO, copia de
       W), escribí en la BANDEJA una tabla con lo que el código hace, no con
       lo que significa: qué se muestrea, sobre qué W o copia, qué se calcula
       con eso, y contra qué se compara ese resultado después. Con línea de
       código. Al final de cada parámetro: "mismo concepto" o "se separa", y
       la razón, en una línea, tomada de la tabla.
   1b. Implementación, según 1a, sin esperar:
       - mismo concepto en los tres -> un solo campo en CKMlandscapeConfig,
         que leen los tres. Sale el propio de cada uno (calibrate_n_runs y
         CALIBRATE_N_RUNS; n_runs_attractors y count_seed de Monitor, si es
         el caso).
       - no es el mismo concepto -> un campo por concepto en la Config, con
         nombre propio (orden BABEL: un nombre por concepto, en inglés), y
         cada uno declarado. Dos que hoy se llaman igual y son distintos
         dejan de llamarse igual.
       - Si para algún parámetro la tabla no alcanza para decidir, ése no
         se implementa: A1.PAUSA sólo para ése y seguí con lo demás.
   - No cambia ningún número: los valores de hoy pasan tal cual al campo
     que les toque.
   - Test: cambiar un campo de la Config mueve exactamente a los que lo leen,
     y a ningún otro.
   - Si un camino construye Monitor o calibrate sin Config (tests, drivers,
     calibrate offline), no lo arregles con un default nuevo: reportá cuáles
     son y qué valores usan hoy.
   - Docstrings, con el grep: el de la Config, el de coco.py:173-175
     ("sesgado hacia arriba con n_runs… no cambiar sin revisar el hallazgo
     del sweep 60→70") — no lo cambies, decí si sigue siendo cierto tal como
     está escrito —, y la razón de delamor para el 1000 de calibrate ("darles
     posibilidades para que sientan el sesgo. luego lo que suceda solo
     sucederá"), que se conserva donde quede el valor.
   - El n_runs = 80 de la firma de COCO es un default de función: no lo toques
     (TASK de defaults); decí si en algún camino todavía se usa.

2. w_sha_live_at_calibration se persiste en el registro de la calibración
   (decisión de Opus): junto a duration_s y blocking, en el lugar de la
   calibración de la Config. Es registrar un campo que ya se mide y se
   descarta. Test: el registro lo trae, None en el origen. Sin tocar
   w_sha_match: la colisión queda registrada como está (delamor la marcó
   como sesgo de control).

3. test_beta_no_va_al_device busca sobre la estructura, no sobre el texto
   (decisión de Opus): recorrer el estado y afirmar que ningún valor es el β
   del device en un lugar que lo publique, en vez de buscar repr(v) como
   subcadena del JSON. Declará en su docstring qué afirmaba, por qué daba
   falso positivo (los dígitos de β dentro de un timestamp) y qué afirma
   ahora. No se afloja: tiene que seguir fallando si el β viaja.

NO: el margen, los valores de la grilla (puede cambiar de lugar, no de
valor), el patrón de calibrate, w_sha_match, el mecanismo general de
defaults, P14, E1, E5, el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos (uno por punto), suite completa en serie al cerrar,
pull --rebase y push. A1.PAUSA.
```
