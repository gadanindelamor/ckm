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

---
## Actualización (19→20 oct, noche) — hasta `c85ea97`, 755/7/0
- **Claves del panel CP1 en inglés** (`8b7c57a`); heredadas en castellano listadas por módulo como pendientes. Stash resuelto.
- **CP1b** (`88d31fc`, `d15ba96`): con `/max Δ_r` Monitor y COCO diferían en signo; la normalización cancelaba la acumulación. `calibrate` en el salto: ~68 ms → **sin sombra para S2-C0**.
- **Decisión de delamor: Δ_r no se normaliza, como en COCO** (`f684aee`). Misma fórmula, distintos insumos: siguen distintos el Δ (COCO comprime al STOP) y el baseline.
- **Sin interpretaciones** (delamor): se mide qué miden, no se decide. Corridas "antes/después" (`b303613`, `f684aee`; `experiments/medir_dos_d_ckm_{antes,despues}.jsonl`): después, COCO disparó 1 vez (n=48). Camino (`c85ea97`): el cambio llega a COCO por su insumo (pares expulsados → Δ_r), primera diferencia n=34. No atribuible: una corrida por lado.
- **Abierto, anotado sin cambiar nada:** `calibrate` calibra sobre W sola por interpolación; COCO cruza con W + Δ_r. Misma referencia (A0 sobre W), distinto camino. Se mira en el vivo.
- El canal **no publica** lo de COCO (información sensible, delamor). Pendiente hablar: qué puede entender un device de D_ckm.
- `w_eff.same: True` fijo en el panel (`monitor_service.py:491`) = "misma fórmula"; desde el primer STOP las matrices difieren. Menor.

## Para el diseño del vivo (Code libre hasta cerrarlo conceptualmente)
- Ensayo (CP2, sin IA, por script) y vivo (CP3) son dos; la medición de hoy cubre buena parte del CP2 (falta verificar canal en silencio y corte al final).
- **Consigna: delamor elige** (a) nada, (b) tema abierto sin respuesta correcta, (c) tarea con resultado.
- **Duración:** ≥ 50 mensajes (≥ 2 rebuilds), mejor ~70; a tiempo con el ritmo del vivo 03 → `piso_vueltas` (`piso_vueltas + 2 ≤ vueltas por device`).
