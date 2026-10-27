# Texto para Code — 13 — repo ckm — un solo n_runs (decisión de delamor) + dos correcciones de registro — 27 oct 2026 (Opus 5.5)

```
Code: tres puntos, en este orden. Por favor.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, del 27 oct, desde
  "CP2, CP3 y el REG del intento 4: leídos por Opus" hasta el final.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Unidad: cada punto. De corrido dentro de cada uno; A1.PAUSA al terminar el
  punto 1 sólo si encontrás una tensión; si no, seguí.

1. UN SOLO n_runs — decisión de delamor (E3 que subiste en el CP2).
   delamor, 27 oct: "si se trata del mismo concepto, n_runs, que se usa como
   variaciones de sigma estados iniciales, y se analiza donde tiende o
   converge. La respuesta es si. Confirmo todos leen el mismo concepto".
   Y su pregunta de origen: "si cambio el n_runs para barridos en la config,
   cambia el de Monitor, y el de COCO?". Después de este punto, la respuesta
   tiene que ser sí, y también para calibrate.
   - Monitor, COCO y calibrate leen n_runs de CKMlandscapeConfig. Ninguno lo
     tiene propio: sale calibrate_n_runs (Config y CALIBRATE_N_RUNS en
     ckm_monitor.py); Monitor deja de contar con n_runs_attractors propio
     (monitor_service.py:91, :140) y lee el de la Config.
   - No cambia ningún número: hoy los tres valen 1000.
   - Alcance de la decisión: n_runs. seed y grilla no están en esta decisión:
     seed de Monitor (count_seed), seed de calibrate y seed de COCO quedan como
     están; reportá cómo quedan, sin unificarlos.
   - Test: cambiar Config.n_runs mueve a los tres (Monitor, COCO y calibrate).
   - Si un camino construye Monitor o calibrate sin Config (tests, drivers,
     calibrate offline), no lo arregles con un default nuevo: reportá cuáles
     son y qué n_runs usan hoy.
   - Docstrings a revisar, con el grep: el de la Config (ahora sí "uno solo
     para Monitor, COCO y calibrate"), el de coco.py:173-175 ("sesgado hacia
     arriba con n_runs… no cambiar sin revisar el hallazgo del sweep 60→70")
     — no lo cambies, decí si sigue siendo cierto tal como está escrito —,
     y el de CALIBRATE_N_RUNS con la razón de delamor (la razón se conserva,
     en el docstring de la Config o donde quede el valor).
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

NO: el margen, la grilla, el patrón de calibrate, w_sha_match, el mecanismo
general de defaults, P14, E1, E5, el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos (uno por punto), suite completa en serie al cerrar,
pull --rebase y push. A1.PAUSA.
```
