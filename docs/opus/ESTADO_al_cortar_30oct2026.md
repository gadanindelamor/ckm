# ESTADO al cortar — 30 oct 2026 (Opus 5.5, Cowork)

La traza está en `docs/opus/decisiones_en_el_acto.md`, 30 oct. Lo anterior sigue en `ESTADO_al_cortar_29oct2026_noche.md`.

## Hecho
- Los textos 20 y 21, corridos por Code y revisados por Opus en lote (BANDEJA, 29 oct 22:33 a 23:42 UTC).
- **Texto 22**, escrito y no pegado todavía: corrige el REG del intento 5 (la segunda calibración, de 6c16bb08, `calibrado`) y pasa P13, P14, P17 y P18 a `DECISIONES_opus.md`.
- delamor (30 oct): *"lo que sigue es en dirección que necesitaba el paper. si hay evidencia o material, que completes el paper, amplíes o refuerces. luego con la V33 revisada va al review"*. Uso al 77 %: el v34 se escribe en una sesión nueva.

## Próxima sesión — una tarea: el v34 `_borrador`, sobre el v33
Fuentes: el BANDEJA del 29 oct (textos 20 y 21), el REG borrador del intento 5 (después del texto 22, si ya corrió; si no, el log del driver) y `decisiones_en_el_acto.md` del 29 y el 30 oct.
1. **§6.4 (R1):** el margen exacto de las 14 W: ninguna separa. bdb98f5b da +0,011 muestreado y −0,065 exacto, y F(20) cae dentro del IC. Agregar el intento 5: el origen 66ea8d05 da −0,300 muestreado y −0,332 exacto; 6c16bb08, `calibrado`, da +0,506 muestreado y +0,4915 exacto, y su COCO no nació. AUTO-9 sigue resistido.
2. **Abstract, §4.3.1 y §8.1 (R3):** el teorema con su condición: α ≤ 2/3 ⇒ N_eff ≥ 2, y la cota N_eff ≥ 1/(α² + (1−α)²/2), alcanzada. F(N) es el caso de igualdad. Lo medido: los 769 contraejemplos, todos con α > 2/3; α de las W del caso, entre 0,004 y 0,008 (0,199 en 6c16bb08); el estimador a 200 cae debajo de 2 en 3 de 14. Corregir AUTO-13: lo que estaba "no establecido" ahora está probado, con su condición. La línea de fourforums: los pares ± **salvo las autoconjugadas**.
3. **§4.1.5 o §6.4 (paridad):** con N impar, el plug-in del colapso no pasa de 2, y llega a 2 sólo con n_runs par (P = 0,066 a 200; 0 a 199 y 201). Con N par, la paridad de n_runs no cambia nada.
4. **§4.3.2 (R2):** los números de HEAD (A24 base 4,876 ± 0,179; "+1 texto" 8,997; D12 3,063, N = 19; E7 4,788, N = 7; 38 de 42 celdas cambian; el efecto de "+1 texto" en A24 cambia de signo). Los de `0e042ac` van al bloque de arriba como traza. Fuente: `experiments/driver_cpe_rango_neff_salida_HEAD.txt`.
5. **§4.1 / §6 (torsión):** la regla de qué entra a Δ_r (rechazo completo) y lo medido: 0 torsión en 154 evaluaciones de 4 vivos; en las órbitas autoconjugadas, la torsión son los pares de un mismo lado (el 100 % en el colapso, el 78 % en las W de las curvas).
6. **l.400 y l.722 (R4):** el ±1–5 % es el N_eff0 de caso09, con 3 seeds y n_runs = 1000 (REG desempate §8). No son "basin masses… IAP corpora".
7. **§4.1.2 (P19):** hasta que delamor decida, el cuerpo dice lo que el código hace: el empate se evalúa en float64, y en el 13–22 % de los estados de estas W, h = 0 exacto da ±1e−17. Ningún signo del margen cambia. P19 va a *Pendientes*.
8. Después: R7 (fourforums) y R9 (las referencias). Si no entran en la sesión, van a *Pendientes*. Después, el `_print` y el review frío (`cold-referee`).

## Espera
- **delamor:** P19, A (el código cumple la regla) o B (el paper declara el float). Recomendación de Opus: A.
- **delamor:** pegarle a Code el texto 22 cuando quiera. Es independiente del v34.
- R8 (la literatura de KR) y el plan de cierre (textos 17 y 19), como estaban.
