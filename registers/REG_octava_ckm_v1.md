# REG_octava_ckm_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Observacion especulativa — no experimento confirmado*
*Clase R*

---

## Origen

Sesion Jun 2026. El usuario trajo el texto de Escalas de Octavas
(Ley del Siete — Ouspensky, In Search of the Miraculous).
La conexion con CKM emergio en conversacion.

---

## La definicion de intervalo en CKM

**No esta explicita en el codigo. Se desprende directamente.**

En la teoria de octavas:

```
critical value  cv
lower octave    lo(cv) = cv / 2
higher octave   ho(cv) = cv * 2
interval        [ lo(cv), ho(cv) ]
```

En COCOThermostat:

```
D_CKM_THRESHOLD = 0.40   # cv

lo(0.40) = 0.20
ho(0.40) = 0.80
interval implicito = [0.20, 0.80]
```

El codigo eligio 0.40 empiricamente del sweep con AMP=40.
La eleccion parecio arbitraria.
La octava le da derivacion estructural: cv es la nota critica,
[lo(cv), ho(cv)] es la octava que la contiene.

El limite superior (ho = 0.80) no existe como umbral en el codigo.
Esta implicito en los datos del sweep — el sistema nunca salio de esa zona.
Pero no hay ningun umbral programado ahi.

Implicacion: las zonas TOO_COLD / NOMINAL / TOO_HOT
podrian derivarse de cv via octava en lugar de calibrarse empiricamente.

**Estado: hipotesis. Requiere verificacion experimental.**

---

## La curva sin choque — zoom out

Una octava sin choque externo en el intervalo:

- La curva sube DO -> MI
- En mi-fa: se aplana
- No colapsa, no espirala
- Continua al mismo nivel indefinidamente
- DO2 existe como posibilidad pero el sistema no llega

Esto es lo que pasa por defecto.
La espiral (ascenso al siguiente nivel) requiere el choque.
El choque es externo — no proviene del sistema.

En CKM: STOP es un choque externo.
CKM puede detectar que esta en el intervalo (D_ckm mide el gradiente).
No puede aplicarse el choque.

**Nota: la relacion entre CKM y el mecanismo del choque**
**fue objeto de correccion en sesion — el usuario rechazo una formulacion**
**prematura. Esta abierto. No se cierra aqui.**

---

## "Casi un circulo" — P1 y la octava

Las notas de una octava proyectadas en angulos iguales sobre un circulo
forman casi un circulo (la frecuencia dobla — espiral — pero el nombre
de la nota regresa al mismo angulo).

El bucle de histeresis P1 (c(S) vs rho):
- Camino de incorporacion (rho sube): curva distinta de
- Camino de remocion (rho baja)
- Forman un bucle cerrado — casi un circulo
- No cierra: area = 0.000862, p~0

La analogia: la octava tiene dos puntos donde los caminos divergen
mas (mi-fa y si-do). El loop P1 tiene dos zonas de mayor divergencia
entre las ramas (inicio y fin del barrido).

**Estado: observacion estructural sobre datos ya confirmados.**
**No es nueva prediccion.**

---

## Patrones adicionales confirmados en sesion

1. **Reconstruccion desde posicion parcial ↔ Hopfield**
   1/7 comparte las mismas seis cifras rotadas en todas las fracciones.
   Conocer la primera cifra permite reconstruir el periodo.
   Equivalente a recuperacion de atractor desde estado parcial.

2. **Partes desiguales ignoradas ↔ W_pos vs W_mixta**
   "En la representacion usual la desigualdad de las partes no es tomada
   en consideracion." W_pos trata todos los pares como equivalentes.
   W_mixta devuelve la desigualdad estructural.

3. **DO[k] = E[k-1] ↔ arquitectura por capas**
   Cada nota contiene en si misma una octava completa del orden inferior.
   Agentes (orden k) / CKM (orden k+1) / IAP (orden k+2).
   Misma estructura en cada escala.

4. **7/7 = 0.999... ↔ Omega***
   El unico valor donde el periodo no se repite — limite asimptotico.
   Omega* en CKM: diversidad maxima de atractores, nunca c(S)=1.
   El termostato regula para mantenerse cerca sin alcanzarlo.

---

## Lo que no se cierra en esta sesion

- La relacion entre CKM y el mecanismo del choque externo: abierto.
- A1-A5 como representacion de los 7 intervalos: especulativo, no relevante aun.
- Derivacion formal de umbrales TOO_COLD/TOO_HOT desde cv via octava: pendiente.

---

*Jun 2026*
