# REG_fourforums_v8h_nombres_C6c_v1

Clase R. Va a `registers/` con el OK de delamor (23 oct 2026).

*23 oct 2026. gadanin.delamor + Claude Opus 5.5 (Cowork). Solo se leyó: el clon `ckmdatasets` de la PC (`916524c`), `ckm/registers/`, `ckmdatasets_old/trace/` y el `CREATE TABLE` del dump en la PC. No se corrió nada sobre el dump real.*

---

## El intento que subyace

Una W cuyo signo no lo pongamos nosotros (delamor: *"perfecto, es lo que imaginaba"*). El signo lo ponen los anotadores humanos del IAC (`mturk_2010_qr_task1_worker_response.disagree_agree`), y v8h es la capa de acceso al dump más avanzada que hay (delamor: *"el dump es tricky… un diseño relacional poco intuitivo, que no corresponde 100 % a las indicaciones técnicas del txt"*).

## 1. Lo que ya estaba establecido (Sonnet 4.6 + delamor)

| REG | Fecha (cabecera / commit en ckm) | Qué establece |
|---|---|---|
| `REG_qr_asymmetry_fourforums_v1` | jun / `ebdfae1` 25 jun | La cadena del join, la cobertura (905 discusiones, 304 autores T0=96 T1=208, 54.005 votos, 7.876 resueltos = 14,6 %: el resto es de otros temas, no errores), la tabla por postura, H1–H4 |
| `REG_exp_delta_t_W_fourforums_v1/v2` | 1 jul / `7fa25f8` 8 jul | Δt contra W_obs: ρ = −0,0575, n.s. Hay un Δt negativo (372→148) |
| `REG_c6c_asim_fourforums_v1` | jul / `7fa25f8` 8 jul | C6c ∈ [0,38; 0,41] |
| `REG_holonomy_coercivity_fourforums_v1` | 8 may | Holonomía y coercividad (v8g) |
| `REG_author_965_structure_v1` | — | CreateDebate |

Pendiente escrito por esos REGs: *"Construir W[N×N] orientada desde top_pairs… para experimentos P1–P4 con W_asim real"*. v8i lo hace, con todos los pares.

## 2. Hallazgo: cómo se llama cada extremo de un voto

- **v8h** guarda `pair_da[qtr_aid][rsp_aid]`. `qtr_aid` es el autor del post **fuente** (`quote.source_post_id`) y `rsp_aid` el autor del post que **contiene** la cita.
- **`delta_t_wobs_v1.py`** (Sonnet, 1 jul) lo dice así: *"(did, pid) = post CITANTE (más nuevo) → autor = responder… (sd, sp) = post CITADO (más viejo) → autor = quoter en la nomenclatura del pipeline"*. Las medianas de Δt positivas son una evidencia empírica a favor, con un solo caso negativo.
- **El `CREATE TABLE quote` del dump** dice lo mismo: la fila es del post que cita, y `source_*` es el post citado. Ojo: es lo declarado por el dump, y delamor advierte que ese esquema no es 100 % confiable. Por eso el peso lo lleva la evidencia de Δt.
- **Lo que no coincide:** `REG_qr_asymmetry` (25 jun) y `REG_c6c_asim` (8 jul) leen "T0_quotes_T1" como *"T0 cita T1"*. Según el script del 1 jul, en esa clave T0 es el **citado** y T1 el que responde.

**Fechas.** La lectura "T0 cita T1" aparece el 25 jun y pasa a C6c el 8 jul. El script del 1 jul ya tenía la nomenclatura correcta, y C6c entró en el mismo commit que él. No es una lectura de antes de una versión del pipeline: es la misma v8h, leída de dos maneras en la misma ventana. *(Sobre qué instancia lo leyó así no hay traza.)*

**Qué cambia si vale J1:** las magnitudes no. Se invierte el sentido de las lecturas: H2 "T0 es el atacante estructural" pasa a ser "T1 responde a T0 2,18 veces más que T0 a T1"; H4 "437 atacante dominante" pasa a ser 437 como el más citado por 148; C6c = 0,41 se mantiene como número y cambia su dirección.

**Lectura de Opus, no verificada:** `REG_c6c_asim` tuvo que conciliar una aparente contradicción con P6 de v8g (*"T0 sos_dom 51,4 %, T0 recibe réplicas"*) diciendo *"dos caras del mismo rol"*. Con J1 no hay nada que conciliar: T0 recibe réplicas en v8g y T0 es citado en v8h. Falta verificar la definición de sos_dom en v8g.

## 3. Lo que se hizo (código, sin correr sobre el dump real)

- **`fourforums_pipeline_v8i.py`**: la capa de acceso de v8h intacta, incluidos sus nombres. Agrega todos los pares, la matriz dirigida A (NaN = sin dato, nunca 0) y los conteos. No decide la simetrización, el mínimo de votos, qué N ni el nulo.
- **`fourforums_pipeline_v8j.py`**: v8i más dos cambios declarados. **J1**: nombres `quoted_author` / `responding_author`. **J2**: lee `disagree_agree_unsure` y lo reporta, sin descartar esos votos.
- Probados contra un dump sintético: A es idéntica bit a bit entre i y j, y solo difieren los nombres y los conteos de unsure.
- Copias en `docs/opus/ckmdatasets/` y en `contexto_claude`. Van a la raíz de `ckmdatasets`, con `out/` en el `.gitignore`.

## 4. Otras correcciones de este día

- **El dump tiene copia en la PC**, en `ckmdatasets_old/trace/` (`.sql` y `.gz`), ignorada por git (`*.sql`) y sin versionar. El "existe solo en el Codespace" del REG de la tarea 1 y de Opus era incorrecto.
- **`W_asim_v8h.json` está versionado en `ckmdatasets`** con ids de autor por par. Es un derivado por fila, y según la clasificación del 15 oct quizás no corresponda. Lo decide delamor.

## 5. Pendiente

- Correr v8i y v8j en `ckmdatasets` y comparar los dos logs.
- Decidir J1 (si se adopta, revisar H2, H4 y C6c en los REGs y lo que use el paper) y J2.
- Para W: la simetrización, el mínimo de votos, qué N (2^N estados) y el nulo.
- Verificar sos_dom en v8g.

## Lo que este REG no sabe

- No se corrió nada sobre el dump real. Los números de §1 son de los REGs, no de esta sesión.
- No se leyeron `ckm___model`, `___paper` ni `___research` (no están conectados).
- La evidencia de J1 es la de Sonnet (Δt) y el esquema declarado. No hay prueba independiente.
