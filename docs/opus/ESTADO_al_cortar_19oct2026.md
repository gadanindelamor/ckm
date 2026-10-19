# Estado al cortar — 19 oct 2026
*Opus 5.5 para la próxima instancia. Reemplaza a `ESTADO_al_cortar_15oct2026.md`. Decisiones con cita: `decisiones_en_el_acto.md` (15 y 19 oct). Marco: `docs/defs/DEFS_CKM_estado_actual_v17.md`.*

## 1. En GitHub (hasta `496c525`, 755 pasan, 7 xfailed, 0 fallan)
- **DEFS v17** en `docs/defs/` (`e8f6c0e`, `68166fd`). delamor revisa atribuciones y *Admisible* de los bloques v17 con el documento entero.
- Code (19 oct):
  - `1f7c8a3` — **`calibrate` antes del rebuild, sobre la W candidata** (`W_candidata()` no instala). Sin salto posible no calibra y el panel dice por qué. Panel: los dos shas (candidata y viva al calibrar), `bloqueante: True`, `duracion_s` medido. 4 tests nuevos; uno falla si calibra después de instalar.
  - `e724b4d` — `criterio_local` → `local_criterion`, sin alias. Los datos del vivo 03 no se tocaron.
  - `f49adb2` — `arranque` → `startup` **con su API** (ej. `fijar_state_dir`): **decisión de Code, declarada; delamor confirma o pide sólo el `git mv`.**

## 2. A medias
- **Claves del panel del CP1 a inglés: en `git stash@{0}` del Codespace, NO en el repo.** Si el Codespace se borra, se pierde. 7 rojos, todos del mismo tipo: el barrido tradujo también claves que no nacieron en el CP1 y que otros leen en castellano (`calibrate` → `estado`/`valores`/`condiciones`; Monitor → `condicion_W`; criterio local → `umbrales_calibrados`). Arreglo propuesto por Code: publicar en inglés y **leer** esas claves como están. **No verificado que cierre en verde.**
- Pregunta abierta para delamor: ¿esas claves heredadas también pasan a inglés (otro paso, con su propio barrido) o se dejan hasta su módulo?

## 3. No arrancado
- **CP1b** (escalas de Δ_r, dos combinaciones, tiempo de `calibrate` en el salto): sin predicción escrita.
- Después: CP2 (ensayo local) y CP3 (vivo S2-C0). Consigna y duración del caso, abiertas.

## 4. Abierto (sin cambio)
Sombra de `calibrate` (propuesta), coordinar REG/BANDEJA/decisiones, mail IAC, CP-N, paper v29 (**espera**; se revisará con las DEFS v17 como guía).

## 5. Lateral
Investigación sobre *"Neural Networks Are Already Clean"* (Cammarata, Goodfire, 15 oct): informe en el chat. Ensayo original no leído directo. Sin acción sobre CKM.
