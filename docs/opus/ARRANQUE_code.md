# Arranque — Code (Codespace), sesión nueva

*Lo pega delamor al abrir la sesión de Code. Escrito el 21 oct 2026 por Opus 5.5. Completo y autocontenido.*

```
Repo: gadanindelamor/ckm (Codespace). Trabajás según docs/tasks/PROTOCOLO_code_continuidad_v1.md — leelo entero primero.

1. Git lo hacés vos (delamor, 21 oct): git pull --rebase origin main antes de trabajar y antes de cada push. Push al cerrar cada CP o parte. Commits nombrando los archivos uno por uno; nunca add -A ni commit -a. Si el rebase da conflicto: git rebase --abort, A1.PAUSA y lo reportás.

2. Chequeo de arranque (§2), escrito en docs/tasks/BANDEJA_code.md como entrada ARRANQUE: revisé / encontré / no pude revisar. Nada de "OK". Incluí las preguntas Pn sin respuesta en DECISIONES_opus.md y en docs/opus/decisiones_en_el_acto.md.

3. Estado: leé el último docs/opus/ESTADO_al_cortar_<fecha>.md y docs/opus/decisiones_en_el_acto.md (lo último). Ahí está qué TASK o texto está abierto y qué espera.

4. Ejecutá sólo el próximo paso abierto. Antes de tocar nada, evaluá el texto contra el repo y decí las tensiones. Al cerrar: commit, push, ESTADO y reporte. El reporte va en la BANDEJA además del chat. A1.PAUSA.

5. Reglas vigentes:
   - No decidas nada de §5 (E1–E6): preguntá en la BANDEJA, BLOQUEA / NO BLOQUEA.
   - docs/opus/ es de Opus: no se edita (salvo pedido explícito); la traza con fecha no se reescribe.
   - registers/ es Clase R: REG nuevos como borrador afuera, salvo orden de delamor.
   - Sin regresiones ni compatibilidad hacia atrás; lo viejo se reproduce desde su freeze en process/.
   - Cada .py modificado actualiza su docstring.
   - Rótulos nuevos en inglés. Nada en castellano en lo que llega a un modelo.
   - Lo que va en una consigna para devices es un pedido, no una orden.
   - Un vivo de IAP no se corre sin orden explícita de delamor. Al correr: en background, sin seguirlo; leer el resumen, no el log entero. Durante el vivo, ninguna intervención.
```
