# NO ES REPRODUCIBLE. Intento de congelar las condiciones del CP-E y del CP-M.

*2026-10-15 — Claude Opus 5 (Code). Texto de delamor:
`docs/opus/textos_para_code/TEXTO_PARA_CODE_freeze_CPE_CPM_15oct2026.md`. Decisión en
`docs/tasks/DECISIONES_opus.md` (`9622fd4`). Predicción commiteada antes de crear esta carpeta
(`a1c717f`). Molde: `process/iap_series_freeze_20261008/`.*

**Los originales no se tocaron.** Esto es una copia: `cp -p`, verificada con `diff` archivo por
archivo. Lo congelado sigue estando donde estaba.

---

## Qué se congela y por qué ahora

El paper (v29) cita el **CP-E** —rango de estabilidad de N_eff— y el **CP-M** —el nulo de
marcadores— de `docs/tasks/TASK_condiciones_del_paper_v1.md`. Los dos drivers **importan los
servicios vivos**, y uno de los tres corpus, **D12**, *es* estado vivo del canal
(`iap_chatroom/_state/corpus_state.json`). Si el canal corre, o si cambia un servicio, lo que el
paper declara deja de poder rearmarse.

delamor, 15 oct: *"cuando freezamos algo… se mueve a carpeta de process los archivos necesarios
para reproducir, lo necesario… sino no se va a reproducir"*; *"por eso dije basta de regresión…
la regresión es cuando el producto está estabilizado… pero acá estamos investigando, ¿no?"*.

**Lo que pasó no se conserva con regresiones en el código vivo: se conserva acá.**

## Qué hay

| carpeta | qué | de dónde |
|---|---|---|
| `experiments/` | `driver_cpe_rango_neff.py`, `driver_cpm_nulo_marcadores.py` | `experiments/` |
| `services/` | `node_extractor.py`, `corpus_service.py`, `landscape_engine.py`, `w_version.py` | `services/` |
| `process/experiments/wmixta_paso2_natural/` | `corpus_natural_uniform.json` (**A24**) | misma ruta |
| `iap_chatroom/_state/` | `corpus_state.json` (**D12**, estado vivo, tal como está hoy) | misma ruta |
| `process/iap/` | `corpus_state.json` (**E7**) | misma ruta |
| `resultados/` | la salida de cada driver, **stdout tal cual** (`*_stderr.txt` quedaron **vacíos**, y quedan como constancia), y la salida de la verificación de imports | corrida desde esta copia |
| `entorno/` | `pip_freeze.txt`, `python.txt`, `commit.txt`, `nltk.txt`, la declaración de extracción y su sha, `sha256_de_lo_copiado.txt` y `verificacion_imports.py` | medido al congelar |

**El árbol relativo es el del repo**, así que los drivers corren **sin editarlos**:
`RAIZ = Path(__file__).resolve().parent.parent` resuelve a esta carpeta.

```
cd /tmp && python -I <esta carpeta>/experiments/driver_cpe_rango_neff.py
cd /tmp && python -I <esta carpeta>/experiments/driver_cpm_nulo_marcadores.py
```

Se corrió así —**desde afuera del repo y en modo aislado** (`-I`, que implica `-E`, `-s` y `-P`)—
a pedido de delamor, para que ni `PYTHONPATH`, ni el site del usuario, ni el directorio del script
puedan traer nada del repo vivo. Verificado además módulo por módulo con `entorno/verificacion_imports.py`
(salida en `resultados/verificacion_imports_stdout.txt`): los cinco
(`services.node_extractor`, `services.corpus_service`, `services.landscape_engine`,
`node_extractor`, `w_version`) resuelven **dentro de esta carpeta**.

**Los números dieron idénticos** a los de los REPORTES del CP-E y del CP-M, hasta el último
decimal impreso. Tiempos desde la copia: CP-E **56 s**, CP-M **3 min 16 s**.

## El mínimo de `services/`, y es una decisión declarada

El texto dice *"decidí vos el mínimo; si dudás, la carpeta entera"*. **Son cuatro archivos**, y
no es una estimación: los drivers importan `node_extractor`, `corpus_service` y
`landscape_engine`; `corpus_service` importa `w_version`; `landscape_engine` no importa nada del
repo. **No hay imports lazy** fuera de `tempfile`, `os`, `itertools` y `math`. **No hay
`services/__init__.py`** (es paquete de espacio de nombres) y **ningún módulo abre un archivo del
repo**: `DECLARACION_REF` es una cadena, no una lectura.

Una rareza que estaba en el repo y viaja igual: `corpus_service` importa `node_extractor` **a
secas** y los drivers importan `services.node_extractor`, así que hay **dos objetos módulo** para
el mismo archivo (`is` → `False`). No rompe nada —no hay `isinstance` en el medio— y acá los dos
salen del freeze.

## Lo que no se pudo congelar, y se declara

1. **Las librerías de terceros no se copian: se guarda la versión** (`entorno/pip_freeze.txt`;
   las que mueven los números son `numpy==2.4.6`, `scikit-learn==1.9.0`, `scipy==1.17.1`).
   **Esas versiones valen mientras se puedan reinstalar.** Si una se retira del índice, queda
   sólo el identificador, igual que con los modelos por API en el freeze de la serie IAP.
2. **No quedó registrado el `pip freeze` de las corridas originales** del CP-E (`0e042ac`,
   03:42 UTC) y del CP-M (`a1c6a18`, 04:31 UTC): no existía el archivo. Lo más cercano que hay en
   el repo es el `pip_freeze.txt` del freeze del 8 oct, y contra el de hoy **difiere en una sola
   línea** (`networkx==3.7`, que estos drivers no importan). O sea: **"entorno idéntico" vale
   *dado* este entorno, no está verificado contra el de aquel momento.** La máquina arrancó a las
   **04:13 UTC**, o sea **después** de la corrida del CP-E y **antes** de la del CP-M: el CP-E
   corrió en otro arranque del Codespace.
3. **`nltk` no está instalado** (`entorno/nltk.txt`) y la lista de 703 stopwords está embebida en
   `node_extractor.py`. Por eso el CP-E usa **0 stopwords** como tercer nivel, que es el extremo:
   *"sólo NLTK"* no se puede construir ni separar de la unión. Ya estaba declarado en el REPORTE
   del CP-E y **no cambia lo que el CP-E afirma**; lo que no se puede decir es cuánto aporta cada
   lista.
4. **La máquina.** `entorno/python.txt` dice el intérprete y la plataforma; el hardware, el
   contenedor y el kernel no se congelan. **No hay `.devcontainer/`** en el repo (era el límite 2
   del freeze del 8 oct y sigue igual).
5. **D12 es estado vivo.** Acá queda **tal como estaba el 15 oct**
   (sha256 `c3bd376bb53721daed1fb563e8bc7fe81cfb31bdb2791f498e16a347f65b4e4d`, mtime 2026-10-09).
   El canal lo puede cambiar en cualquier momento; esta copia no.
6. **Lo que no se sabe.** *"No conocemos el todo. Las interpretaciones siempre son falsas"*
   (delamor). Esto congela condiciones, no el fenómeno.

## Lo que esta carpeta no decide

El CP-E y el CP-M **no fijan umbral**, y acá tampoco. Los resultados en `resultados/` son la
salida de los drivers, sin interpretar. La lectura está en los REPORTES de la BANDEJA
(CP-E 03:42 UTC, CP-M 04:31 UTC) y en `docs/tasks/DECISIONES_opus.md`.
