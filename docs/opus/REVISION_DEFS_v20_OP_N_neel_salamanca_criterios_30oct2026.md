# Revisión — DEFS v20 (§N y §OP), Néel / SALAMANCA, full_meaning, trace_ip y CRITERIOS_diversidad — 30 oct 2026 (Opus 5.5, Cowork)

*Pedido de delamor (30 oct): revisar las DEFS actuales, la grilla de OP y de N, y Néel / SALAMANCA (*"creo que hay tests que se hicieron"*), full_meaning e IP trace, y `docs/CRITERIOS_diversidad_formulacion_v1.md`. *"Luego una sola respuesta con todo en doc."* Lectura en la PC. No se tocó ningún archivo, salvo éste.*

## 0. Lo más importante, primero
1. **P19 ya estaba encontrado el 11 sep**, en `CRITERIOS_diversidad_formulacion_v1.md` §4, con su regla y tres arreglos posibles. Eso decide la forma de A: va en §6.
2. **Néel se corrió el 20 sep**, y la DEFS v20 y el paper v34 dicen que no.
3. **SALAMANCA está registrado** (Clase R) y el paper no lo menciona.
4. **Error mío en el v34 (A3):** escribí *"expelled"* en §4.2.2. La tabla N lo marca como Babel desde el 8 oct.

## 1. DEFS v20 — la última (no hay v21)

### §N, los nombres: 19 rótulos
metabolizado · `rejected` / `rechazados` · `expulsados` · torsión / `n_torsion` / `Δ_r_torsion` · "expulsión" (§11) · operador de compresión de COCO · OPERADOR_STOP_COCO / "operadorstop" · `MonitorService.stop_signal` (UNKNOWN) · H_STOP · Gatekeeper / portero / `admit()` · `count_attractors` · `d_ckm`, `A0`, `A_actual` · "degradado / expandido" · "agregar un nodo" · contagio / acoplado · UNKNOWN / NOMINAL · `services/` · E1–E4, EA1–EA3, D1–D3, L1–L4 (Orden BABEL, propuestos).

Lo que está abierto ahí y espera a delamor desde octubre:
- el renombre de `expulsados` (*"¿a dónde? ¿fuera de él?"*, 8 oct);
- OPERADOR_STOP_COCO en el código;
- Gatekeeper;
- los verbos de "agregar un nodo" (activar / desactivar, incorporar / retirar);
- los prefijos del Orden BABEL.

### §OP, los objetos del instrumento: 26
S = W estática, D = dinámica, S+D = las dos.
- **Del corpus (S):** fi, W_ij, W_ij/(fi·fj), T(W), perfect_oppositions, W_mixta.
- **Del estado:** c(S) (S+D) y r = c(S)/μ_W (D).
- **De las formulaciones (S):** Histéresis (P1) y Ω* (P4). En el paper son F1 y F4.
- **Del landscape (S+D):** Atractores A = |L|, N_eff, node_presence, d(σ), copresence_matrix, cluster_nodes, cluster_frontier_density, Boltzmann σ₀ y β_Néel (propuesto).
- **De la dinámica (D):** D_masa_cuencas, D_ckm, Δ_r, la órbita en el panel, Δ_r_torsion y UNKNOWN.

### Desactualizado en §OP
- **La nota v17:** los números del CP-E de `0e042ac` (15,52 / 5,27 / 10,10, el −66 %). Con el extractor de hoy no se reproducen (texto 20, punto 3).
- **La fila N_eff:**
  - dice "±1–5 % en casos IAP": es N_eff0 de un solo corpus (caso09), con 3 seeds (R4);
  - dice "D_ckm sigue definido sobre A", cuando desde v15 D_ckm se calcula con N_eff;
  - dice "Rango [1, A0]", y ahora hay una cota inferior: §5.

### Falta en §OP (medido o decidido después de la v20)
- F(N), el piso del colapso, y el margen y la separación (N_eff(W) > F(N));
- α, la masa autoconjugada, con la cota y la condición α ≤ 2/3;
- W_Monitor, W_COCO y W_calibrate, y los tres D_ckm;
- Δ_r_pares y Δ_r_compresiones: están en las SLAs, no en la tabla;
- el Threshold MEASURED / DECLARED y frac_rec;
- los criterios D.1–D.5 de CRITERIOS (§5).

### Otras dos cosas
- **"paridad" en la fila Δ_r_torsion:** ahí es la paridad de la **fase** de la órbita de período 2, no la de N. Code midió las dos en el texto 20 (2e y 4d).
- **El ítem 19 del review** ("cluster frontier coercivity" no está definida): en §OP sí está, como `cluster_frontier_density`, min(intra_a, intra_b) / inter(a, b), y también en CRITERIOS Parte III. Lo que falta es que el paper la traiga.

## 2. Néel y SALAMANCA

- **SALAMANCA S1.**
  - Fuente: `registers/REG_salamanca_s1_v1.md` (Clase R, OK de delamor el 5 oct), con 1000 barajados, k-means con 10 inicializaciones y Bonferroni sobre 7 k.
  - Lo medido: **detecta modularidad, no adversarialidad**. La saturación ordena (monótona en los cinco corpus medibles), y el criterio **devolvió vacío** en los dos corpus saturados y en el de 7 textos.
  - Control positivo: ausente. La corrección por la familia completa no se sostiene a 1000 barajados.
  - La DEFS v20 §16 lo trae completo. **El paper v34 no lo menciona.**
- **Néel.**
  - Fuente: `docs/tasks/TASK_neel_separabilidad_v1.md`, sección *"Resultado — primera corrida"*. Es una TASK, no un REG. Driver: `experiments/driver_neel_salamanca.py`, commit `abc14b3` del 20 sep.
  - El pre-registro estaba mal asignado: caso09 es el canal IAP 0.9, no el debate (lo declaró Code).
  - SALAMANCA dio ncut 0,633 contra el nulo 0,873 (20 barajados, p < 0,001). La partición separa protocolo e identidad de los devices del contenido.
  - Néel dio una frontera de profundidad cero: de los 20 pares menos correlacionados, a β = 0,244 / 0,122 / 0,068, persisten en 3 semillas 1 / 0 / 0, contra 0,03 por azar. *"Módulos sin frontera."*
  - Pendiente desde entonces: el control positivo con fourforums.
- **La contradicción:** la DEFS v20 §15 dice *"sigue no corrido"* (citando el REG de SALAMANCA, §6), y el paper v34 §8.5 trae a Néel como *"Proposed… Not verified"*.
- **Los tests:** `tests/test_coco.py:140` y `tests/test_vacio_y_orbita_en_el_panel.py:8` afirman que *"SALAMANCA: no medible" no es "nada"*. No hay un test del criterio.

## 3. full_meaning
Sólo existe en la DEFS v20, fila T(W) de §OP: con presencia sola, T = 0 por teorema (§1.1 h), así que `full_meaning` (T > τ) no se alcanza sin marcadores. No hay código (grep en `services/`, `iap_chatroom/` y `experiments/`: nada), y el v34 no lo trae.

## 4. trace_ip
- **En el paper v34**, §8.2 (MonitorService, *trajectory inflection point*) y §8.3: el momento es observable; si un device lo reconoció, no es verificable.
- **Su instancia:** `registers/REG_trace_ip_sesion_05oct_v1.md` (Clase R, 5 oct). Sus momentos son el origen de varias cosas de hoy:
  - período 2 como Möbius o cilindro (10–11);
  - *"NODE EXTRACTOR, REBUILD, Néel, SALAMANCA"* como los cuatro lugares donde una magnitud se vuelve existencia o relación (12);
  - los rebuilds que no respetaban el período 2 (13);
  - el nacimiento de la torsión, *"debe respetar la estructura"* (14);
  - los dos COCO (15).

## 5. `docs/CRITERIOS_diversidad_formulacion_v1.md` (11 sep, `550dd64`)
Es un documento autocontenido, con formulación y especificación. Lo que trae, contra lo de hoy:

- **§4, la condición de exactitud: es P19.**
  - El documento dice: *"`sign(h)` es discontinua en h = 0… Regla: los empates son exactos si y sólo si los pesos lo son."* Con pesos no diádicos, el **46 %** de los pasos cambia de sucesor según cómo se escriba el producto; con pesos diádicos, el 0 %. Normalizar por 3 en vez de por 4 dio el mismo número de órbitas (33), pero 18 de ellas distintas.
  - Los tres arreglos, en orden de costo: (1) no normalizar, trabajar con los conteos enteros; (2) **normalizar por la potencia de dos siguiente**; (3) suma exacta compensada.
  - El asincrónico reduce el efecto, pero no lo elimina.
  - Code midió lo mismo el 29 oct, del otro lado: W con denominador 12, y entre el 13 y el 22 % de los estados con otro sucesor que el exacto. **Lo encontrado el 11 sep no llegó al paper, ni a las DEFS, ni al código.**
- **D.5, diagnósticos de exactitud:** `valores_distintos`, `diádico`, `frac_empates` y `frágil`. El documento dice: *"`frágil > 0`… Es diagnóstico obligatorio antes de reportar cualquier número."* No se implementó.
- **§2.3, la medida de referencia:** CRITERIOS llama **canónica** a la uniforme sobre el hipercubo (así la masa es volumen de cuenca, una propiedad de W sola), y dice que la banda 30–70 % es *"una tercera referencia"*. El 28 oct delamor eligió la banda del código. No es una contradicción, porque las dos se declaran, pero la DEFS v21 tiene que decir que la canónica de CRITERIOS fue reemplazada, y cuándo.
- **C.2:** es la fuente de la tabla de validación de §4.3.1 del paper (masa plana / intermedia / concentrada). Fue bajo la uniforme, y el paper ya lo dice. Responde en parte el ítem 36 del review.
- **D.1–D.4, criterios de W sola, sin muestrear:**
  - D.1, índice de frustración: topológico, por triángulos, invariante a la escala. Es el que usa §5.2 del paper para fourforums;
  - D.2, `frac_neg` = Σ|W<0| / Σ|W|: **es la misma fórmula que T(W) de §OP**. Dos nombres para un objeto (Babel);
  - D.3, el espectro (λ_min, λ_max);
  - D.4, el CV de las frecuencias marginales.
  En §OP sólo está T(W).
- **Eje 1 / Eje 2:** separa las cantidades de W sola de las de la sonda, y las topológicas de las métricas. Medido: con los negativos amplificados ×16, la frustración queda fija (0,0258) mientras frac_neg va de 0,031 a 0,338. El paper no usa esta distinción.
- **Parte III, lo abierto:**
  - qué tendría que contar un índice de degradación (decisión del modelo, no del teorema);
  - la medición cruzada entre los criterios de W y los de la sonda;
  - la profundidad de cuenca: la cola es plana, y el candidato son las barreras de energía, sin probar;
  - la coercividad de frontera *"de W sola"*, derivando la partición por corte espectral. **Es lo que después hizo SALAMANCA**;
  - con N > 22 no hay verdad de terreno.
- **Para el review:** el ítem 34 (Chao1, Good–Turing) tampoco tiene respuesta acá. CRITERIOS argumenta contra el conteo crudo, igual que el paper.

## 6. Lo que decide Opus (bajo el umbral; se registra en `decisiones_en_el_acto.md`)
1. **La forma de P19 A sale de CRITERIOS §4.** Primera opción: normalizar W por la potencia de dos siguiente. Escalar W por una constante positiva no cambia sign(h), así que la dinámica queda igual a la exacta; sólo cambian de escala las cantidades métricas absolutas. Code mide si eso alcanza y qué arrastra en lo métrico: c(S), μ_W, los umbrales absolutos. Si W no viene de conteos enteros, la opción es la suma exacta (3). Se implementa también D.5 (`frágil`) como diagnóstico, antes y después. Va en un texto para Code de la próxima sesión, con el recálculo de §4.3.1 y §6.4. §4.1.2 del paper (B) cita CRITERIOS §4 como el hallazgo del 11 sep.
2. **DEFS v21:** se corrigen §15 (Néel se corrió), la nota v17 de §OP, la fila N_eff y la de Δ_r_torsion. Se agrega lo que falta (§1), D.1–D.5 de CRITERIOS y el reemplazo de la medida canónica (28 oct). T(W) y frac_neg quedan declarados como el mismo objeto.
3. **Paper:** "expelled" sale de §4.2.2 hasta que delamor elija el rótulo. Mientras tanto, la frase se escribe por su definición: *"rejected in every phase of the orbit"*.

## 7. Lo que decide delamor
1. **¿SALAMANCA y Néel entran al paper?** Lo que aportan: un criterio que puede devolver vacío, y lo devolvió (en el canal y en los corpus saturados). Lo que no tienen: un solo corpus para Néel (mal asignado en el pre-registro), sin control positivo, con 20 nulos y 3 semillas.
2. **El rótulo de `expulsados`.** Está abierto desde el 8 oct. Hoy el código dice `expulsados` y el paper *"expelled"*.
3. **¿Entran al paper los criterios de W sola (D.1–D.4) y la distinción topológico / métrico?** §5.2 ya usa D.1 sin nombrarlo como criterio.

## 8. Lo que no hizo esta revisión
- No leyó las DEFS v20 enteras: §N, §OP, §15, §16 y §17, y las filas que se nombran.
- No leyó CRITERIOS §C.1, C.3–C.5 en detalle, ni las TASK de SALAMANCA y Néel v1–v5, ni la SUPERTASK.
- No corrió nada.
