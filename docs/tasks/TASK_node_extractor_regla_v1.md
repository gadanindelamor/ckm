# TASK_node_extractor_regla_v1

*Opus (Cowork), 13 oct 2026. delamor: «esa es la dirección… instanciar la regla»;
«identificar órdenes, condiciones, variables calibrables, etc». Para Code, en el
Codespace.*

## Por qué

**Sanear `NodeExtractor` = definirlo conceptualmente, ver su correctitud, y
escribirlo como instancia de `CkmTrustRule`.** Mismo camino que `criterio_local`
(`TASK_ckm_trust_rule_v1`, CP0 → CP3).

## Traza de la que se parte (no se re-mide)

- **BANDEJA, CP0 de `TASK_ckm_trust_rule_v1`:** §4 (`_seleccionar` en la forma),
  **F1** (P vacío, sin reloj), **F2** (sin ↑k: I5 contra el paso 4; el código eligió
  *"empatados afuera"* sin nombrar el `g`), **"no se ubica"** (¿dos `f` en k2?), y el
  **índice alfabético** que mueve `w_sha` y `N_eff`.
- **`REG_unidad_texto_saturacion_v1`:** unidad de texto, saturación, stopwords
  (*"estado"*, §4.3), marcadores sin salida nula (§5), y los parámetros de
  extracción que `save()` **no persiste**.

## Fuera de este TASK

- **Elegir** la unidad de texto o el valor de `top_k`: es **calibración** (delamor,
  13 oct).
- Stemming / lematización, y las stopwords con contenido: **qué es un nodo** lo
  decide delamor.
- Los marcadores: son el **CP1b** de `TASK_ckm_trust_rule_v1`.

## Reglas del TASK

1. **Gate `f96c234`:** `services/node_extractor.py` **no cambia** sin orden de
   delamor.
2. **I2:** la ausencia no tiene valor por defecto.
3. **Docstrings en el mismo commit.**
4. **Archivos nombrados uno por uno** al commitear.
5. **ALTO por CP.**

## Checkpoints

### CP0a — Sin código. Órdenes, condiciones, variables calibrables

1. **Órdenes.** Cada decisión de `NodeExtractor` —el **pool**, `_seleccionar`,
   `evaluate`— en qué orden vive, con el criterio *"un orden es lo que queda fijo
   mientras el de abajo varía"*; su **contigüidad**; y cuál es su **↑k**, si existe.
   Retomar el *"no se ubica"* del CP0 **sin forzarlo**: si sigue sin poder decirse,
   se dice.
2. **Condiciones.** Lo que tiene que valer para que la salida **signifique** algo:
   unidad de texto, idioma/s, tamaño y saturación del corpus, encoding. Para cada
   una: si hoy **se declara**, **se registra** o **se persiste**.
3. **Variables calibrables.** Tabla con **todo parámetro que decide algo**,
   explícito o implícito: `top_k`, el factor **3** del pool, `ngram_max`, el largo
   mínimo y el alfabeto del `token_pattern`, la lista de stopwords **y su versión**,
   `TOL_EMPATE`, los defaults de `TfidfVectorizer` (`lowercase`, `norm="l2"`,
   `smooth_idf`), y la unidad de texto.
   **Columnas:** valor · **origen** (declarado / medido / default de librería / no se
   sabe) · qué **orden** lo produce · si **`calibrate`** lo calibra hoy · si
   **`save()`** lo persiste · **tolerancia** (o `None` declarado).
   **Y separar tres especies:** calibrable · **definición de qué es un nodo** (de
   delamor) · **numérica** (no es de la regla).
4. **Dónde no se pudo decir.**

**Reporta:** las cuatro listas.

### CP0 — Sin tocar `node_extractor.py`. Correctitud de **C**

Qué llega como **candidato**. Confirmar o refutar **cada punto con un test chico**;
**lo que hoy está mal queda como `xfail(strict=True)`, sin arreglo**:

| | qué |
|---|---|
| **a** | **bigramas anidados:** si `"x y"` y `"x"` son nodos, co-ocurren en **todo** texto donde está el bigrama → W positiva **por construcción**, no por campo |
| **b** | **bigramas que atraviesan stopwords:** `"control of guns"` → `"control guns"` |
| **c** | **Unicode:** NFD (`"información"` con tilde combinada) y letras fuera de la clase del `token_pattern` (`ç`, `ã`, `õ`, `à`, `ï`) |
| **d** | **stopwords que el `token_pattern` nunca produce** (las que llevan apóstrofo) |
| **e** | **`accumulate` con corpus vacío:** faltan `pairs_by_text` y `registro_borde` |
| **f** | **el pool** (`max_features = top_k·3`): ¿el corte por frecuencia es **estable ante empates en el borde**? Es una **segunda decisión, sin R** |

**Reporta:** cada punto confirmado/refutado **con evidencia**, y **el pool escrito en
la forma** `⟨C, f, R, κ, ε, T, P, g, ↑k⟩`, con sus **casilleros vacíos**.

### CP1 — Sin tocar `node_extractor.py`. `_seleccionar` como instancia, **en un test**

Expresar `_seleccionar` —y el **pool**, si entra— como instancia de `CkmTrustRule`
**en un test**. **Antes de correr, escribir la predicción en la BANDEJA.** Comparar
contra el código de hoy:

- sobre los **corpus registrados** que elijas (**declaralos**);
- con un **barrido** contra una **copia congelada** de `_seleccionar` del commit
  actual.

**Casilleros conocidos de antemano, a declarar, no a resolver:**

- **ε = `None` declarado** (`TOL_EMPATE` es **numérica**, no de la regla);
- **P = `None` declarado** (no hay reloj: **F1**);
- **↑k = `None` → `ESCALATED`**; el que llama decide, y hoy decide *"afuera"*: ese
  **`g` se nombra en el test** (**F2**).

**Reporta:** igual, o **la lista de diferencias**, y **"Lo que la forma no nombra"**
—decisiones **vs** rótulos, como en el CP3 de `TASK_ckm_trust_rule_v1`—. **Si la
forma no entra, se reporta, no se fuerza.**

### CP2 — Sólo con orden de delamor

Que `node_extractor.py` instancie el módulo.
