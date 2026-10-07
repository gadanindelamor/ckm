# DECISIONES_opus

*Decisiones que Opus toma por debajo del umbral (`PROTOCOLO_code_continuidad_v1.md` §5). delamor puede revertir cualquiera.*
*Formato: fecha · qué · por qué · cómo revertir.*

---

- **2026-10-07** · La Config v3 mantiene una clase `CKMlandscapeConfigV1` renombrada hasta el CP3, en lugar de borrarla en el CP1 · así los consumidores no se rompen mientras se migra · revertir: borrarla en el CP1.
- **2026-10-07** · El laboratorio de W quedó en `docs/lab/laboratorio_w.html` · era una carpeta nueva y no había convención · revertir: mover el archivo antes del commit.

### Sobre el ARRANQUE y el REPORTE CP0 de Code (BANDEJA, 2026-10-07 03:54 UTC)

- **2026-10-07** · **CP0 de Config v3: aceptado.** Los cuatro puntos están completos y las correcciones que hizo en el camino quedaron declaradas · revertir: pedir que se rehaga el punto que se quiera.
- **2026-10-07** · **Concurrencia: va un lock y no se escala.** Hay un lector en un hilo (`gr.Timer` → `get_state`) y un escritor en el event loop, en el mismo proceso. Es la primera rama de la TASK §2. El lock cubre el reemplazo de `ciclo_vigente` y la lectura que arma el panel · revertir: sacar el lock (no se recomienda).
- **2026-10-07** · **P1 (`theta_W_formula`): se acepta el default.** Pasa a la clase nueva sin cambios. Es una función pura que no define nada nuevo · revertir: borrarla y ajustar los dos asserts.
- **2026-10-07** · **P2 (`gatekeeper_c1.py`): se acepta el default.** En el CP3 no se toca, salvo el docstring si `theta_W_formula` se mueve · revertir: trivial.
- **2026-10-07** · **P4 (lectura de los registros planos de v1): se acepta el default.** Es una función de lectura plano → (identidad, declarado, ciclo único `bootstrap`, `t_señal=None`, `t_rebuild=timestamp`) y no reescribe nada histórico · revertir: borrar la función.
- **2026-10-07** · **§2.5 del protocolo (tests en el arranque): de ahora en más se corren.** Correr tests no cambia código, así que entra en el chequeo aunque el CP sea de lectura. Esta vez no se corrieron y quedó declarado en "no pude revisar", que era lo correcto · revertir: volver a solo leerlos.
- **2026-10-07** · **CP1: puede arrancar.** P3 bloquea el CP2, no el CP1 · revertir: frenar el CP1 hasta que se responda P3.
- **P3: escalada a delamor** (E3/E4: qué instrumenta el canal vivo y con qué θ_W). Pendiente.
