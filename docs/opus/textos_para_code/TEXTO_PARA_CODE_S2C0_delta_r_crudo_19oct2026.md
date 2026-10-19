DELAMOR A CODE (texto de Opus):

Decisión de delamor tras el CP1b (`d15ba96`): **Δ_r no se normaliza, como en COCO.** En Monitor, W_eff = W + Δ_r crudo, sin `/max Δ_r` y sin factor de W. Su lectura: dividir por el máximo re-escala, y lo único que cancela es la acumulación. Registro: `docs/opus/decisiones_en_el_acto.md`, sección 19 oct (noche).

Se hace en dos pasos, y el primero no toca código. Vale lo de siempre: no se toca el vivo, sin alias, sin compatibilidad hacia atrás, y la suite cierra en verde.

**(1) Lectura, sin código.** En `coco.py` y en `services/calibrate.py`:
- ¿Cuándo dispara COCO? ¿Con D_ckm por encima de `D_CKM_THRESHOLD`, por debajo, o con su valor absoluto?
- ¿Qué hace con **D_ckm < 0** (campo expandido)? En el CP1b, con rechazos repetidos, el D_ckm de COCO llegó a −1,63.
- ¿Sobre qué cantidad calibra `calibrate` los umbrales: la W sola, o W + Δ_r?

Respondé con archivo y línea. Si de esto sale que con Δ_r crudo COCO nunca dispara bajo rechazos repetidos, **pará ahí y reportá**: eso lo decide delamor antes del paso 2.

**(2) El cambio, sólo si el (1) no lo frena.**
- `_combine_W_Delta` (`monitor_service.py`) pasa a W + Δ_r crudo.
- Cambiá el comentario del código y la línea de las DEFS v17 que dice "dos cantidades": ahora, con la misma W y los mismos rechazos, es **una** W_eff.
- Re-corré el driver del CP1b para mostrar que la columna de Monitor da igual a la de COCO.
- Los tests que fijaban la escala vieja se reescriben, sin conservar la vieja.
- Declaralo en el commit.

Al terminar: commits, estado de los tests y avisá para el push.
