# Texto para Code — 19 — repo ckm — IAP declara lo suyo: archivos de estado, puerto, casos y state_dir — 28 oct 2026 (Opus 5.5)

*Va después del 17 y el 18. delamor decide la dirección y delega la implementación en Opus (28 oct): "Soy responsable de la decisión YO, y delego su implementación a Opus VOS".*

```
Code: cuatro puntos de IAP (segunda prioridad, después del instrumento). Por
favor, en este orden.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, 28 oct, desde "IAP: lo que
  decide delamor" hasta el final.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Antes de cada punto: evaluá el punto contra el repo y decí qué rompe y qué
  tests se mueven. Si algo choca con la dirección, A1.PAUSA sólo para ese
  punto. Si no, implementá de corrido. Nombres nuevos en inglés.

1. P14 puntos 1 y 2 — IAP declara lo que hoy sólo saben los drivers.
   delamor: "hay un driver que sabe más que IAP? ... sigue esa lógica".
   - Archivos de estado de una corrida: UNA lista en IAP con los 11 (los 6
     de run_store.ARCHIVOS más los 5 que arma CKMMonitor adentro:
     corpus_state.json, corpus_G_state.json, monitor_trajectory.jsonl,
     rebuild_decisions.jsonl, rebuild_state.json). CKMMonitor arma sus
     rutas desde esa lista; el driver (preservar_estado, --reset) la lee en
     vez de tener la suya. El guardia de P14 compara: el caso no declara su
     propia lista. Test: agregar un archivo a la lista lo preserva el reset.
   - Puerto (y host): una sola declaración en IAP. server.py la usa en
     uvicorn.run; el mcp_url por default de AutonomousDevice se arma desde
     ahí; el caso la lee. El valor no cambia (7860, host "0.0.0.0"), pero
     queda declarado y sale en la declaración de arranque del server y en el
     panel. Las copias de MCP_URL en drivers freezados no se tocan (traza).

2. La estructura de los casos — delamor delega en Opus: se adopta la
   propuesta de tu 16.2a.
   - iap_chatroom/cases/, con README_cases.md que declare la regla: ahí
     viven los drivers de los vivos, y un driver de un vivo NO se llama
     test_*.py (así pytest no lo colecta aunque alguien toque testpaths).
   - git mv iap_chatroom/tests/test_caso_serie2_caso0.py
     → iap_chatroom/cases/caso_serie2_caso0.py. Actualizá correr_caso0.sh,
     el CASO_PATH y los asserts de tests/test_caso_serie2_caso0_diseno.py,
     y los docs vivos que lo nombren (README, CLAUDE.md). Lo que es traza
     no se reescribe.
   - Lo que queda en iap_chatroom/tests/ (armstrong_*, wmixta_*,
     test_mcp_client.py) se queda; el README_cases.md nombra ese hueco
     (drivers de experimento sobre corpus fijos, citados por services/)
     sin resolverlo.
   - Test: el driver del caso no es colectado por pytest.

3. E1, el state_dir — delamor: "mi definición se sostiene. Yo reviewer, yo
   investigador, voy al repo a ver… debe respetar la dirección". La
   dirección: quien corre algo escribe en un lugar propio, declarado, y
   nunca en la traza. Implementación (opción B):
   - Sin --state-dir, el server (CKMMonitor) usa un directorio nuevo por
     corrida: experiments/_state_run_<UTC>/. Se dice al arrancar y va al
     panel, con fue_pedido (hoy startup.declare() sólo llega al print).
   - iap_chatroom/_state/ (la traza de agosto) deja de ser default de
     nadie. Nadie escribe ahí: si algo lo intenta, falla diciendo por qué.
     Los 3 archivos de agosto no se tocan.
   - P17: correr_caso0.sh --check no toca el estado del caso. No hace
     --reset y levanta su server sobre su propio directorio
     (experiments/_check_<UTC>/), declarado en lo que imprime. El vivo
     (sin --check) sigue como hoy: --reset y el state_dir del caso.
   - Revisá las fixtures del conftest.py y los tests que parchean
     _STATE_DIR: el default cambia y la protección tiene que seguir
     cubriendo la traza. Si un test dependía del default viejo, declaralo.
   - Test: sin --state-dir, el server no escribe en iap_chatroom/_state/;
     el panel dice dónde escribe y si fue pedido; --check deja el
     state_dir del caso como lo encontró.

4. La regla amarrete (delamor, 28 oct: "no seguir corriendo minutos si ya
   finalizó la interacción… 180 hrs por mes de Codespace"; "ponele así,
   como Newton"). Hay interacción mientras quedan al menos dos devices
   activos en el canal. Si queda uno o ninguno, el caso termina antes de
   DURATION, y el log del caso registra la causa del fin: por tiempo, o
   por interacción terminada (nombres en inglés en el código; "regla
   amarrete" en el docstring, con la cita). No es un umbral elegido: con
   uno solo no hay con quién interactuar. Antes de implementarlo, decí
   dónde vive la condición (el caso o el canal) y si toca algo del
   instrumento; un device que sale por LEAVE o por error cuenta igual como
   no activo, con su causa propia en su resumen. Test: con dos devices,
   uno sale y el caso termina con la causa declarada; con tres, uno sale y
   el caso sigue.

NO: el instrumento (está en el 17 y el 18), los devices (delamor: no es
producto todavía), el patrón de calibrate, el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos (uno por punto), suite completa en serie al cerrar,
pull --rebase y push. A1.PAUSA.
```
