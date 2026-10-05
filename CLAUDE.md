# CKM / TRUST

Las instrucciones del proyecto y el protocolo, cargados en cada sesión:

@TRUST_INSTRUCTIONS.md

@readme/AWARENESS.md

---

## Dónde está lo demás

- `docs/BRIEF_TRUST_para_Code_v1.md` — qué es TRUST, cómo se trabaja, quién puede qué, y el estado de los frentes.
- `readme/CONVENTIONS.md` — convenciones de código. Incluye la regla de completitud: un cambio de comportamiento que no mueve ningún test ni docstring no está cubierto.
- `docs/tasks/` — las TASK. Se ejecutan con checkpoints: al terminar cada paso, detenerse, reportar y esperar el OK. **Vale también para las acciones espontáneas.**
- `registers/` — Clase R. No se toca. Los REG nuevos se entregan como borrador fuera de `registers/`.
- `P1P4/DESPERTAR_leer_primero.md` — frente de las propiedades del modelo. Leer **antes** de abrir cualquier otro archivo de ese frente: lo que quedó cerrado, los nombres que no se usan, y la regla del teorema.

## Lo que no se hace

- No se commitea `process/replay/_private/` ni los dumps de datasets.
- No se interpreta: se mide y se registra. La lectura es de delamor.
- No se reabre algo cerrado sin leer el REG que lo cerró.
- No se afirma "no existe" sin decir desde dónde se miró.
- No se corrige en silencio.
- No se corre lo que se demuestra. Antes de una corrida, preguntar si el resultado es un teorema; si lo es, se demuestra en una línea. Correr lo demostrable gasta a delamor, que es el recurso escaso.
- No se le arma a delamor un menú de opciones para que elija. Se decide lo que es del modelo y se le dice qué se decidió.
