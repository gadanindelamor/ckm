# Traza externa — extracción de nodos (13 oct 2026)
*Opus (Cowork), a pedido de delamor: "acá estamos sobre un plano diferente, donde sí puede existir traza: las investigaciones y desarrollos sobre extracción de nodos. Papers, teoremas". Para S2 y S3 del CP-S de `TASK_node_extractor_regla_v1`. **Referencia, no respaldo** (criterio de delamor para el paper). Lectura corta: lo que se leyó está dicho; lo que no, también.*

## Qué se leyó y con qué alcance
| fuente | qué se leyó | alcance |
|---|---|---|
| Nothman, Qin, Yurchak (2018), *Stop Word Lists in Free Open-source Software Packages*, NLP-OSS — https://aclanthology.org/W18-2502/ | **sólo el abstract** | no el paper completo |
| Frantzi, Ananiadou, Mima (2000), C-value/NC-value — https://link.springer.com/article/10.1007/s007999900023 | la fórmula, vía Maynard & Ananiadou (2000), *Identifying Terms by their Family and Friends* (COLING, C00-1077), cuya extracción de texto salió **incompleta** | fórmula reconstruida, ver abajo |
| Rose et al. (2010), RAKE, *Automatic Keyword Extraction from Individual Documents* — descripción en la documentación del paquete `slowraker` | la regla de candidatos y el puntaje | no el capítulo original |
| Unicode UAX #15 (formas de normalización) | conocimiento general, **no releído hoy** | — |

## S2 — términos anidados ("gun" dentro de "gun control")
**C-value** (forma estándar; la extracción del PDF salió incompleta, el término restado se reconstruye de memoria — verificar contra Frantzi et al. 2000 antes de citar):
- si `a` no está anidado: `C(a) = log2|a| · f(a)`
- si está anidado: `C(a) = log2|a| · ( f(a) − (1/P(T_a)) · Σ_{b∈T_a} f(b) )`, con `T_a` = candidatos más largos que contienen a `a`, `P(T_a)` = cuántos son.

**Dónde coincide con lo decidido:** el principio. Una aparición de "gun" **dentro** de "gun control" no es evidencia independiente de "gun". C-value la descuenta; nuestro S2 descuenta el **par** (gun, gun control) de W.

**Dónde no coincide — y es lo que esta lectura agrega:** C-value actúa sobre la **selección** (el puntaje de cada término). Nuestro S2 actúa sólo sobre los **pares** (W). Con S2 tal como está escrito, el unigrama "gun" **sigue sumando TF-IDF** por sus apariciones dentro del bigrama, y eso puede meterlo en el top_k. El anidamiento infla **dos** cosas: W (lo que S2 arregla) y la selección (lo que S2 no toca). Descontar en la selección cambia `f` de `_seleccionar` → es decisión de **delamor**, no mecánica.

## S3 — bigramas y adyacencia
**RAKE:** un candidato es *"cualquier conjunto de palabras contiguas que no contiene un delimitador de frase ni una stopword"*; los delimitadores son la **puntuación** (punto, coma). Razón de los autores: los términos *"rara vez contienen puntuación o stopwords"*.

**Dónde coincide:** la decisión de Opus del 13 oct — adyacencia sobre todas las palabras del texto, una stopword en medio rompe el bigrama.

**Dónde no coincide — lo que falta en S3:** la **puntuación**. Hoy el tokenizador descarta la puntuación, así que "…el control. Las armas…" o "control, guns" producen el bigrama `control guns` aunque haya un punto o una coma en medio. Por la misma razón que la stopword, **la puntuación debería romper la adyacencia**. Es mecánico (no cambia qué es un nodo). → agregar a S3.

## Stopwords
**Nothman et al. (abstract):** las listas de stopwords tienen *"omisiones e inclusiones sorprendentes"* (ej.: incluir una palabra de contenido como "computer") y pueden ser **incompatibles con el tokenizador** con el que se usan. El estudio fue motivado por problemas de la lista de **scikit-learn**, que es parte de nuestra lista de 703.

**Coincide con lo medido:** CP0 (d) — 45 stopwords con apóstrofo que el tokenizador nunca produce; y las de contenido ("system", "fire", "estado", "sentido").

**Lo que esta lectura agrega:** con S3, **la lista de stopwords pasa a cortar frases**, no sólo a sacar palabras. Una stopword de contenido ("system") ya no sólo desaparece: además **rompe** el bigrama donde estaba ("knowledge system"). S3 hace que la lista pese más. La lista es de delamor (n3, "qué es un nodo").

## Unicode
NFC es la forma de normalización estándar de Unicode (UAX #15). No es una elección del proyecto. S1 sigue.

## Lo que queda para delamor
1. **Anidamiento en la selección** (C-value): ¿se descuentan las apariciones anidadas también en el puntaje de `_seleccionar`, o sólo en los pares de W (S2)?
2. **La lista de stopwords** pasa a cortar frases con S3. Revisarla (lo marcado: "system", "fire", "estado", "sentido"…) gana peso.

## Lo que decide Opus (instrumento)
- **S3 incluye la puntuación como delimitador** (como RAKE). Mecánico.
- S2 queda como está (pares), con la limitación declarada: no toca la selección.

## Agregado posterior (13 oct, conversación con delamor)
- Sobre C-value, delamor: *"gun control es algo / gun rights es otra cosa"*, *"gun es otra cosa de nuevo"*, *"no se suman"*, *"eso es sintaxis del lenguaje"*. Ninguna de las formas de contar resuelve qué es una unidad; eso es n3. S2b queda en ver cómo funciona, en tests.
- C-value multiplica por log2 del largo: para un unigrama da 0. Está pensado para términos de varias palabras (a verificar contra el paper).
