DELAMOR A CODE (texto de Opus):

Soy delamor. `git pull` antes de nada.

**Decisión mía (15 oct), para DECISIONES en commit propio:**
> *"cuando freezamos algo… se mueve a carpeta de process los archivos necesarios para reproducir, lo necesario. ie: si hay un test de densidad, que utiliza un driver, el driver se mueve no solo los resultados"*; *"sino no se va a reproducir"*; *"por eso dije basta de regresión"*; *"la regresión es cuando el producto está estabilizado"*; *"pero acá estamos investigando, ¿no?"*. Lo que pasó no se conserva con regresiones ni compatibilidad hacia atrás en el código vivo: **se conserva congelando sus condiciones en `process/`**. Código propio (drivers, servicios) **se copia**; librerías de terceros (numpy, sklearn, nltk…) **se guarda la versión**, no se copian; modelos por API, el identificador. Molde: `process/iap_series_freeze_20261008/`.

**Tarea: congelar las condiciones del CP-E y del CP-M** (el paper v29 los cita).

Por qué ahora: los dos drivers (`experiments/driver_cpe_rango_neff.py`, `experiments/driver_cpm_nulo_marcadores.py`) importan los servicios vivos, y el corpus **D12 apunta a `iap_chatroom/_state/corpus_state.json`, que es estado vivo**. Si el canal corre o cambia un servicio, lo que el paper declara deja de poder rearmarse.

1. **Predicción antes**, commiteada: qué esperás al correr los drivers **desde la copia** (¿mismos números que los REPORTES del CP-E y CP-M en la BANDEJA?).
2. Crear `process/condiciones_paper_freeze_20261015/` **copiando, no moviendo** (los originales no se tocan), con el **mismo árbol relativo que el repo**, para que los drivers corran **sin editarlos** (`RAIZ = Path(__file__).parent.parent` resuelve a la carpeta del freeze):
   - `experiments/` — los dos drivers;
   - `services/` — los servicios propios que los drivers importan, directa o transitivamente (decidí vos el mínimo; si dudás, la carpeta entera, y declaralo);
   - los tres corpus en sus mismas rutas relativas: `process/experiments/wmixta_paso2_natural/corpus_natural_uniform.json`, `iap_chatroom/_state/corpus_state.json` (**D12 tal como está hoy**, con su sha256), `process/iap/corpus_state.json`;
   - `resultados/` — la salida de cada driver (hoy imprimen a stdout: guardarla tal cual);
   - `entorno/` — `pip_freeze.txt`, `python.txt`, `commit.txt`, y la declaración de extracción (sha) con la que corrieron;
   - `README.md` que empiece *"NO ES REPRODUCIBLE. Intento de congelar las condiciones"*, como el de la serie IAP, y diga qué queda afuera (nltk no instalado, si sigue así; la máquina; lo que no se sepa). Una línea: las versiones de las librerías valen mientras se puedan reinstalar; si una se retira, queda sólo el identificador, como con los modelos por API.
3. **Correr los drivers desde la copia** y comparar contra la predicción y los REPORTES. Si algo difiere, no se corrige: se reporta.
4. REPORTE en la BANDEJA y **A1.PAUSA**.

Reglas de siempre: archivos nombrados uno por uno al commitear, sin `git add -A`; sin regresiones; no se toca el gate (`f96c234`); nada vivo cambia; donde se duda, A1.PAUSA.
