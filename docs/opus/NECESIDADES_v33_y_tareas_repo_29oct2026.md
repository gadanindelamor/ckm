# Necesidades del paper v33 y tareas para el repo — 29 oct 2026 (Opus 5.5, Cowork)

Sale de escribir `docs/opus/PAPER_Landscape_Driven_Device_v33_borrador_opus.md` (*Pendientes* del bloque de arriba). Es para revisar con delamor en A1.PAUSA. **Todavía no son textos para Code**: los textos se arman después de acordar esto.

Orden de prioridad de delamor (28 oct): CKM el instrumento, después IAP, después devices, después conexiones y servicios.

## 1. Lo que el paper necesita (respaldo)

| # | qué | dónde lo usa el v33 | quién | estado |
|---|---|---|---|---|
| R0 | el piso del colapso, el lema, bajo las dos medidas | §4.1.5, §6.4 | Code (14.2) | **hecho, en el cuerpo** |
| R1 | el margen de las 14 W contra el F exacto, con N_eff0 por enumeración | §6.4 (el signo del margen del intento 3 contra F), §8.1 | Code: **texto 18, punto 1** (ya escrito; espera) | pendiente |
| R2 | el *"15.52 → 5.27"* del v32 contra el CP-E (`0e042ac`) | §4.3.2 (la frase salió hasta saberlo) | Code, lectura; o Opus en la PC, si el CP-E está en el repo | pendiente |
| R3 | N_eff ≥ 2 para toda W por la simetría σ ↔ −σ: prueba corta y enumeración en algunas W (N ≤ 20) | abstract, §4.3.1, §8.1 | Code | pendiente |
| R4 | el n_runs, la seed y la medida de cada número. Falta el ±1–5 % (`REG_seleccion_nodos_desempate_v1` §8) | §4.3.1, §7.4 | Opus, lectura en la PC | pendiente |
| R5 | el baseline de Monitor: ¿hay decisión registrada? | §4.3.1 | Opus | **leído:** no está en `DECISIONES_opus.md`; el cuerpo lo dice como está en el código |
| R6 | el criterio estructural de rebuild, contra el código | §6.3 | Opus | **hecho:** `should_rebuild`, gradiente de D_ckm^Monitor en 3 evaluaciones seguidas del mismo ciclo, `n=3` en `ckm_monitor.py:572` |
| R7 | fourforums: qué son O1–O7, y si las aristas 297 / 75 / 11 son las de la W de N = 146 | §5.2 | Opus, lectura de los REGs de `ckmdatasets` y el de v8n | nuevo, pendiente |
| R8 | la revisión de literatura de KR 2023–2026 | §7.6 (vuelve el párrafo que salió) | delamor decide quién y cómo | nuevo, pendiente |
| R9 | las referencias a verificar (lista en *Pendientes*) | §9 | Opus, con búsqueda web | pendiente |

**Lo más barato que pide Code, en una sola pasada:** R1 (texto 18, punto 1) más R3, en la misma enumeración. Ya estaba así en el plan del 28 oct, y sigue igual. R2 va en la misma pasada si el CP-E está en el Codespace.

**Lo que hace Opus sin Code:** R4, R7 y R9.

## 2. Tareas para el repo que salieron de escribir el v33

Son de cierre, no de respaldo del paper. Van al plan de cierre del repo (paso 3 de delamor).

1. **`should_rebuild(self, d_ckm_history, n: int = 3)`** (`services/corpus_service.py:258`) tiene un default en el argumento. El llamador lo declara (`n=3`, `ckm_monitor.py:572`), pero choca con la regla del 26 oct: ningún default lo completa en silencio una función. *Instrumento.*
2. **El docstring de `beta_i`** contra el código: ya estaba en "Raro" del doc X. Ahora el paper lo cita en §4.2.3. *Instrumento.*
3. **Comparar docstrings con código antes del release** (delamor, 29 oct): ya está en el plan de cierre.
4. **Los textos 17 y 19** siguen esperando el plan de cierre. No son respaldo del paper.
5. **La tabla de D_ckm de §6.4 sin el intento 4:** si se agrega, sale del JSON del intento 4. Es opcional.

## 3. Después de acordar
- Opus arma **un** texto para Code con R1 + R3 (+ R2 si aplica), completo y autocontenido. Va también a la BANDEJA. Pull y push los hace Code.
- Opus hace R4, R7 y R9 en la PC.
- Con eso, el `_print` y el review frío (skill `cold-referee`).
