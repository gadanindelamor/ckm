# Texto para Code — 16 — repo ckm — los providers en IAP, e iap_chatroom/tests/ es process — 27 oct 2026 (Opus 5.5)

*Va después del texto 15. Dos decisiones de delamor (27 oct).*

```
Code: dos puntos, después del texto 15, en este orden. Por favor.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Unidad: cada punto. El punto 2 tiene una A1.PAUSA propia, marcada.

1. P14 punto 3: los providers pasan a IAP. delamor, 27 oct, sobre "IAP no
   sabe qué providers hay": "un driver de test lo sabe. hay que llevar ese
   knowhow a IAP".
   - Hoy iap_chatroom/providers/ tiene cuatro clases (anthropic, gemini,
     groq, openai) y ningún registro nombre→clase; el único mapa es
     _PROVIDERS = {"groq": …, "gemini": …} de
     iap_chatroom/tests/test_caso_serie2_caso0.py:343, que cubre 2 de 4.
   - IAP declara el registro (en iap_chatroom/providers/, nombres en inglés),
     con los cuatro. El driver del caso lo lee en vez de tener el suyo.
   - El guardia de P14 (test_caso_serie2_caso0_diseno.py) pasa a mirar esto:
     que el caso no declare su propio mapa de providers.
   - Test: el registro tiene los cuatro y cada nombre construye su clase;
     un nombre que no existe falla diciendo cuáles hay.
   - Los puntos 1 (la lista de archivos de estado) y 2 (el puerto) de P14
     son la misma forma: NO los hagas acá; delamor decide si van.

2. iap_chatroom/tests/ es process. delamor, 27 oct: "iap_chatroom/tests/ es
   process. ¿sostiene REGs?, ¿o sostiene declaraciones en DEFS, en paper?
   freezar el resto que no sostiene. y es historia... el punto es no agregar
   tests allí en esa carpeta, o bien abrir la estructura del repo para que
   sea precisa".
   2a. Clasificación, sin mover nada. Una tabla con los 34 archivos de
       iap_chatroom/tests/, uno por fila: qué es (driver de un vivo, test,
       simulación, réplica); qué sostiene, con cita: un REG en registers/
       (cuál), una declaración en las DEFS v19 (sección) o en el paper v32
       (línea), o nada; si algo vivo lo importa o lo invoca (otro .py,
       correr_caso0.sh, tests/, docs vivos como README o CLAUDE.md); y la
       propuesta: queda, o va a process/ (freezado, como historia).
       test_caso_serie2_caso0.py lo usa el próximo vivo y correr_caso0.sh:
       decí dónde tendría que vivir, pero no lo muevas.
   2b. A1.PAUSA con la tabla. Mover es estructura del repo: Opus lee la
       tabla y da el OK, o lo sube a delamor si toca dónde viven los casos.
       En el reporte, propuesta (sólo propuesta) de una estructura precisa
       para lo que queda vivo: dónde van los drivers de los vivos de ahora
       en adelante, para que ningún test nuevo caiga en esta carpeta.
   - Desde ahora: no se agregan archivos a iap_chatroom/tests/.

NO: P14 puntos 1 y 2, el state_dir, el patrón de calibrate, la medida de
referencia, el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos, suite completa en serie al cerrar el punto 1, pull
--rebase y push. A1.PAUSA.
```
