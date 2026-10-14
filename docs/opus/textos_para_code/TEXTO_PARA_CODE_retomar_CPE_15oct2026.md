DELAMOR A CODE (texto de Opus):

Soy delamor. Se reinició el Codespace y esta es una sesión nueva. Retomamos donde quedó.

**Antes de nada:** `git pull`. GitHub tiene todo: lo tuyo hasta `397f104` y lo de Opus en `docs/opus/` (la traza de Opus vive ahí desde el 14 oct; la escribe Opus desde la PC; vos no la editás).

**Dónde estamos** (leelo en el repo, no me lo creas):
- `TASK_declaracion_extraccion_v1`: **completa** (CP0, CP1, CP2, CP3 y anexo). Declaración canónica en `docs/defs/DECLARACION_extraccion_W_v1.md`.
- `TASK_condiciones_del_paper_v1`: **CP-T hecho** (`ece56f4`, reporte `2e89afa`). **CP-E en curso:** la predicción está commiteada (`7c6e75a`, *"orden de las dependencias, y nltk no está instalado"*); el driver no se escribió.
- Lo que queda decidido y anotado en `docs/tasks/DECISIONES_opus.md` hasta `397f104`, incluido el principio "CKM no ejecuta código ajeno".

**Paso 1 — una decisión mía para DECISIONES**, en commit propio. Precisa la entrada de `397f104` ("opciones que dé CKM"):
> 15 oct, delamor: *"1 criterio sólo funcionando"*. La comparación de CKM es **una sola, fija, de CKM, declarada una vez**: los dos lados —el nodo y las cadenas de la unidad— pasan por el operador 1 (NFC + minúsculas) y se comparan por igualdad de cadenas. **No por W ni por nodo** (*"eso requerirá un paquete adicional de 500 cajas a Nvidia"*). *"Es lo deseable, y si puede ser… primero lo primero… baby steps"*: **dirección, sin código ahora.** Sigue valiendo el principio: no se ejecuta código ajeno.

**Paso 2 — seguir con el CP-E** de `TASK_condiciones_del_paper_v1`, desde la predicción de `7c6e75a` (no la reescribas: es la que vale, y fue commiteada antes). Escribir el driver, correrlo, comparar contra la predicción, REPORTE en la BANDEJA y **A1.PAUSA**.
- Recordatorio de la TASK: medir **cuánto se mueve N_eff** al variar de a una por vez `top_k`, tamaño del pool, lista de stopwords y un texto más con vocabulario ya visto; varias seeds; reportar dispersión; **no se fija umbral**. Salida: tabla "N_eff estable dentro de este rango, con estas dependencias", lista para el paper.
- Si alguna variante necesita un recurso que no está (por ejemplo `nltk`), se declara en el REPORTE con el recurso que falta y se sigue con lo que sí se puede — o A1.PAUSA si eso cambia lo que el CP-E puede afirmar.

**Reglas de siempre:** predicción antes (ya está); archivos nombrados uno por uno al commitear, sin `git add -A`; sin regresiones ni compatibilidad hacia atrás; no se toca el gate (`f96c234`); nada vivo cambia; donde se duda, A1.PAUSA.
