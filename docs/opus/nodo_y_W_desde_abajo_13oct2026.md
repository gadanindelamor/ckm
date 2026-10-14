# Nodo y W, desde abajo — 13 oct 2026 (noche)
*Opus 5.5 (Cowork), a pedido de delamor: "sanitizar la extracción.. podés generar la traza y documentación de esto". Conversación del 13 oct después de la pausa del CP-S. Todo lo citado con línea se leyó en la PC, sólo lectura, con el repo en `fb2b87a`. Lo que no se verificó dice que no. Las decisiones con cita están también en `docs/opus/decisiones_en_el_acto.md`.*

## 0. La pregunta
delamor: *"¿qué es un nodo dentro del modelo CKM? … técnicamente. qué representa.."* — *"porque eso contesta qué mide CKM"* — *"¿co-ocurrencia de qué cosa?"*. Se respondió **de abajo hacia arriba**, sin usar "concepto".

## 1. La cadena, de abajo hacia arriba (productor de texto, `PERFIL_ES_EN`)
```
texto ─(perfil)→ tokens ─(construcción)→ ckm_form ─(comparación)→ σᵢ ─(co-ocurrencia por unidad)→ W ─(relajación)→ cuencas, N_eff, regla TRUST
                                              └─(traductor, propuesta)→ lo que lee un humano
```
Cada flecha es un lugar donde **se elige algo**. En cada una puede ir una marca (la traza es la marca de que hubo una elección).

## 2. Tokenize — qué hace hoy (`services/node_extractor.py:347-358`)
Orden fijo: NFC (S1) → minúsculas → `re.findall(r"[^\W\d][^\W\d]{2,}")` → fuera stopwords (703) → bigramas pegando tokens con `" "`.

Corrido el mismo patrón sobre ejemplos (en el espacio de Opus, no en la PC):

| texto | tokens |
|---|---|
| `Peter Pan` / `Peter-Pan` / `Peter, Pan` | `peter`, `pan` (+ bigrama `peter pan`) |
| `peter_pan` | `peter_pan` — un token: `_` cuenta como letra |
| `co-alinear` | `alinear` — "co" tiene 2 letras y desaparece |
| `IA y AI` | nada — 2 letras no existen |
| `don't` | `don` |
| `CKM v29 W2` | `ckm` — dígitos cortan |
| `información` | `información` |
| `北京大学是好学校` | la oración entera, un token |

**Visto, no decidido (n3, de delamor):** `_` como letra; guion, apóstrofo y dígitos cortan; largo mínimo 3; idiomas sin espacios. Tokenize decide qué cadenas **pueden llegar a ser** nodo: lo que el patrón no produce no existe en W.

**El bigrama es una cadena construida, no encontrada** (`:357`, `" ".join`). `control of guns` → `control guns`: la stopword sale **antes** de armar el bigrama. Eso es S3 (espera OK). El separador `" "` no está declarado en el perfil; funciona porque ningún token contiene espacio (reversible).

**Dónde viven los tokens:** en ninguna estructura. Se guardan `texts` (crudos) y `nodes` (cadenas). Se re-tokeniza todo en cada rebuild (`:433`) y cada texto nuevo en `evaluate` (`:522`). Como se guarda el texto crudo, todo puede rehacerse bajo otro perfil.

## 3. Si cambia tokenize y el resto no
Tres casos: (1) cadenas que ya no se pueden producir → en `evaluate` quedan en −1 siempre (el código **afirma** −1; roza I2, no verificado contra la regla); (2) la misma cadena con otro origen (`peter pan` desde "peter de pan" o desde "peter pan") — silencioso, ni W ni el sha lo ven; (3) mezcla vía `seleccion_anterior` (`corpus_service.py:298`).

El perfil se guarda y se carga (`corpus_service.py:302, 396, 409`) pero **nadie lo compara**: la marca existe, nadie la lee.

**Decisión de delamor** (*"decidido. lo confirmo."*): si el perfil del estado no coincide con el del extractor, el código se detiene (A1.PAUSA mecánico) en vez de resolver. Va **antes o junto con S3**. Sin código todavía.

## 4. Qué es un nodo
- En el código: un `str` en `nodes[i]`; `i` es sólo la ubicación (decisión de delamor del mismo día: *"el nodo ES la cadena"*).
- Bajando: el `str` de Python es una **secuencia de puntos de código**; los bytes dependen de la codificación (`año`: `61 f1 6f` en puntos de código, `61 c3 b1 6f` en UTF-8). NFC y NFD de `año` se ven igual y para Python son distintos.
- La identidad la da **la operación que compara**: `n in terminos` (`:522`), igualdad de `str` sobre puntos de código, después de NFC.
- delamor: **"un nodo es una comparación"** — *"y su función de comparación o bien de generación de token etc"*. Entonces un nodo, completo, es: **la cadena** (lo que se compara) + **la función que la genera** (perfil, analizador, construcción) + **la función que la compara**. Identidad = lo que esa comparación considera igual; estado σᵢ = lo que esa comparación responde ante este texto (`σᵢ = +1 if n in terminos else -1`). *"Eso es lo que en este instante es, no lo que fue ni lo que será."*
- Hoy las dos funciones **no viajan con el nodo**: viven en el extractor, una para todos los nodos. El nodo guardado es sólo la cadena; la generación deja marca en `perfil_extraccion` (S0b).
- Todos los nodos de una W tienen que compartir la función: W cuenta respuestas sobre el mismo texto bajo la misma comparación.
- **Alcance:** esto es el productor de texto. En fourforums los nodos son autores; en `mcp_adapter`, capacidades declaradas (`DEFS_CKM_estado_actual_v16.md:69`). Ahí también son `str`, sin tokens detrás. Lo general es "un nodo es una cadena"; lo demás depende del productor. No se generaliza.

## 5. Qué co-ocurre — qué es W (productor de texto)
Leído en `node_extractor.py:449-459` y `corpus_service.py:319-337`: por cada texto, `active` = nodos presentes; cada par de `active` suma **1 por texto** (no por aparición); suma en negativo si `_has_opposition(text)`, si no en positivo; `W = (pos − neg) / max|·|`, simétrica, diagonal 0. La unidad es el texto entero (`window` reservado, sin uso, `:298`).

**Lo que co-ocurre son dos resultados `True` de la misma función de comparación, aplicada a la misma unidad de texto.** En el texto no hay co-ocurrencia: hay caracteres. Lo que co-ocurre son dos actos del instrumento.

> **W (texto) = cuántas veces, en el corpus, la misma función de comparación devolvió `True` para dos nodos sobre la misma unidad de texto; con signo según una función de oposición sobre esa unidad; normalizada.**

Sobre eso trabaja todo lo demás: relajación (`landscape_engine.py:74`), cuencas, N_eff, regla TRUST.

**Hipótesis de Opus, verificada y descartada:** dijo que podía haber dos comparaciones distintas (al construir W, el nodo debe estar además en el pool; en `evaluate`, no). Leído `_seleccionar` (`:472-512`): elige **sólo** índices de `terms`, que es el vocabulario del pool, también al conservar en el empate. Los nodos están siempre dentro del pool → dentro de un mismo extractor, las dos comparaciones coinciden. Queda el caso de perfil distinto (§3).

## 6. Propuesta abierta de delamor — el traductor
*"tal vez los nodos son cadenas de tokens, y se trabajan como tales, y sólo un proceso, único, luego veremos si singleton, es quien convierte o traduce únicamente cuando es requerido"*; *"Peter y Pan es la representación, es después de la traducción para que lo lea un humano"*.

Notas: hoy el token **es** el `str` (no hay otra representación ni traductor). Con ids, la dependencia se muda al vocabulario, pero queda en un lugar con un dueño (hoy está repartida en `:357`, `:522` y el JSON). La tupla no arregla "peter de pan" (S3). Singleton supone un perfil; ¿uno por perfil? Otros productores tendrían que declarar su unidad. Referencia, no respaldo: los tokenizadores de modelos de lenguaje trabajan con ids y decodifican a texto sólo al mostrar ("Unicode sandwich" en Python: decodificar en los bordes).

## 7. La foto
`foto_W_canal_IAP.png` (en el proyecto y en `contexto_claude`): W de `iap_chatroom/_state/corpus_state.json`, 12 textos, 32 nodos, 194 acoplamientos (108 +, 86 −). Círculo/cuadrado = convención **del dibujo** (`" " in n`), no del instrumento. Es W, no el instante: falta σ. La posición no significa nada. Script: `foto_W.py`.

## 8. Lo que no se verificó
- Cómo se arma W y σ en fourforums y `mcp_adapter`.
- Si la −1 afirmada para un nodo irreproducible choca con I2.
- Que no exista otra vía por la que entre una cadena con espacio.

## 9. El observador dentro de lo observado (canal IAP)

> **Corrección de Opus (A3, 14 oct) — leer antes que el resto de §9.** El estado leído (`iap_chatroom/_state/corpus_state.json`, commit `4ab7be8`, 10 oct) es el de **los vivos 01 y 02**, anterior al filtro **F3b (9 oct)**: desde entonces los mensajes `SYSTEM` (joins, leaves) **no entran al corpus** (`iap_chatroom/ckm_monitor.py:284-312` y su docstring, que ya decía *"8 de los 12 textos del corpus eran 'X joined the channel'"*). Así que lo de abajo **no fue un hallazgo nuevo**: es una foto de un estado viejo, ya visto y ya resuelto. Además el conteo estaba mal: son **8 joins** (no 7) + 1 prueba ("Hola desde MCP test"). Bajo el punto 4 de delamor (14 oct: *"la única versión del modelo que hay es la actual; el resto es imaginación"*), esa foto no describe al instrumento de hoy. Lo que sigue vigente de §9: (1) los devices **pueden** ver la medición vía `get_monitor_state` (no verificado si la usan); (2) delamor dejó abierto que **SYSTEM es campo** (*"no, nunca en estas condiciones"*), sin apuro.

delamor: *"si yo device delamor sospecho, o incluso confirmo que estoy siendo observado, eso podría modificar mis actos, tan sólo sospecharlo… el acto de observar puede interferir en el fenómeno observado, mientras sucede."*

Referencia, no respaldo: reactividad de la medición (efecto Hawthorne); el panóptico de Bentham, en la lectura de Foucault: alcanza con no poder saber si te miran.

Verificado (PC, `fb2b87a`, y estado del canal):
1. **Los devices pueden ver la medición.** `iap_chatroom/mcp_server.py` les ofrece `get_monitor_state` (D_ckm, temp_signal, n_nodes, corpus_size, …) y `get_firma`; `send_message` devuelve `corpus_size` en cada envío. **No verificado:** si los devices autónomos lo consultan o lo ponen en su prompt. Si lo hacen, los textos que forman W los escribe alguien que ve W.
2. **El aparato ya está dentro de lo observado.** De los 12 textos de `iap_chatroom/_state/corpus_state.json`, **7 son "X joined the channel"**: eventos del canal, no actos de devices. El acoplamiento más fuerte de la foto (`joined` / `joined channel` / `channel`) es la infraestructura registrándose. Uno más es una prueba ("Hola desde MCP test"), el grupo suelto de la foto. El texto 5 es un device diciendo "No substantive content to map" — habla de la tarea de medir.

**En este corpus, más de la mitad de lo que W mide no es interacción:** 8 de las 12 unidades de texto (7 eventos del canal + 1 prueba) no son actos de devices. *Precisión de Opus:* se contaron **unidades**, no el peso de cada una en W (cuántos pares aporta cada texto no se midió). La frase vale como "más de la mitad de las unidades sobre las que se arma W".

No es misterio: es un lazo clásico que se puede ver y cortar o declarar — qué ve un device del estado, y qué textos entran al corpus. Cae dentro de sanear la extracción: **¿un "joined the channel" es una unidad de texto de la interacción, o un evento del aparato?** Es n3, de delamor.

Opus (A1): saber que cada decisión queda registrada cambia cómo escribe — más cuidadoso, también más lento. No sabe separar del todo cuánto es comprensión y cuánto es ser observado.
