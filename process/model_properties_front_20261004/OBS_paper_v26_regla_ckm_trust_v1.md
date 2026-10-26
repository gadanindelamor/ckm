# OBS_paper_v26_regla_ckm_trust_v1

**BORRADOR — observaciones, no cambios.** El paper es DRAFT hasta la revisión de delamor; nada de esto se aplica sin su OK.

*4 oct 2026 — gadanin.delamor + Claude Opus 5.5 (Cowork)*
*Sobre: `PAPER_Landscape_Driven_Device_v26.md` (955 líneas). Lente: REG_borrador_regla_ckm_trust_v1.*
*Cómo se miró: grep y lectura de las secciones citadas, contra `services/coco.py`, `iap_chatroom/ckm_monitor.py`, DEFS v14, Informe v30 §48 y REG_borrador_salamanca_s1_v1. Sin ejecutar nada.*

---

## O1 — La regla ya está en el paper, a medias (§4.2)

**Dice:** "The tiebreaking rule — when h_i = 0, node i retains its current state σ_i — … is a required premise of the instrument."

**Con la regla:** es el paso 2 en la dinámica. El mismo paso en la **selección de nodos** (REG_seleccion_nodos_desempate_v1 §2: "donde el dato no decide, se conserva el precedente") aparece sólo como cita de verificación en §7.4. `preceden` y `conserv` dan 0 en el paper. §4.8 dice de NodeExtractorService "It decides which nodes exist", sin decir cómo decide los empates.

**Propuesta:** nombrar la regla una vez, como premisa general de toda decisión del instrumento (pares, nodos, estados, órdenes), con GOLES como su caso dinámico. Lugar a decidir: §4.2, o §3.8 *Epistemic Conventions*, que ya tiene `[AUTO]`.

## O2 — "observe" dice cuatro cosas, y el paper se contradice consigo mismo

Cuenta: 56 apariciones de `observ*`. Sentidos: (1) Monitor que acumula, (2) la O de ODA, (3) resultado documentado sin causa, (4) observación sobre el observador.

| dice | dónde |
|---|---|
| "MonitorService: **impartial observer**" | §4.8 |
| "COCO is a field regulator, **not a field observer**" | §4.6 |
| "The instrument measures **traces of contact**, not observations by a detached observer" | §7.2 |

En el código `COCO.observe()` hace el ciclo completo: lee el Δ_r de Monitor (O), clasifica la zona y elige α (D), comprime `self._Delta` (A). Y el docstring de `coco.py` empieza: *"Observa D_ckm(t)"*.

**Con la regla:** el rótulo es un criterio de contexto que pasa por descripción del objeto (§7.3 ya lo dice: *"The naming carries a bias"*).

**Propuesta:** que §7.2 alcance a §4.6 y §4.8 — o que "impartial observer" y "not a field observer" se reformulen como roles de escritura (quién escribe qué objeto), que es lo que el código sostiene.

## O3 — La contribución reclamada es una separación (§6.1, §4.7)

**Dice:** §6.1 "IAP separated observation … from action … **The contribution is that separation**, not the sequence." §4.7 "The separation is a **design property**, not a constraint."

**Con META opacidad** (Informe v30 §48.2: *"W y Δ no son dos componentes… La distinción es operacional"*) y con lo precisado el 4 oct (*la separación existe mientras se traza la línea; es del que señala*): la separación es real como **trazabilidad** —quién escribió qué— y no como desacople del campo. Cuando COCO se conecte el lazo se cierra: COCO lee Δ_r de Monitor → emite `temp_signal` → Monitor lo expone en `get_state()` → los devices actúan → el canal → Δ_r de Monitor.

**Propuesta:** formular la contribución como separación de **escritores** que hace verificable el contacto, no como separación del observador respecto del campo. No la anula: la acota (salida "acotar" del paso 3).

## O4 — META opacidad no está nombrada

`opac`: 0 apariciones. §7.2 y §7.3 son META opacidad aplicada a un rótulo (`_observe`, la *d* de D_ckm). **Propuesta:** citarla (Informe v30 §48) en §7, como el nombre de lo que esas dos secciones ya hacen.

## O5 — La ceguera de Monitor tuvo una historia que el paper no cuenta (§4.8)

**Dice:** "MonitorService: … blind to regulation **by object separation**."

**Falta:** antes de D3 la ceguera era por **cancelación**: `Δ_r / max(Δ_r)` cancelaba el escalar α·Δ_r. 0.8857 idéntico en 19 evaluaciones con Δ_r variando 14 órdenes (DEFS v14 §512). `cancel` y `0.8857`: 0 en el paper.

**Con la regla:** es el caso de la regla donde el paso 1 parece cumplido con traza y no lo está — cancelación matemática casual. El valor estable era lo que la ocultaba. D3 fue la salida "separar".

**Propuesta:** una línea en §4.7 o §4.8, o una entrada en el Apéndice A. Es la evidencia de por qué la separación de objetos importa.

## O6 — NOMINAL por ausencia (§4.8)

**Dice:** Firma_CKM registra "temperature signal (TOO_COLD / NOMINAL / TOO_HOT)". `UNKNOWN`: 0.

**Código:** `ckm_monitor.py:131` → `thermostat["temp_signal"] if thermostat else "NOMINAL"`. COCO nunca se conectó al canal, así que las firmas IAP dicen NOMINAL por ausencia.

**Con la regla:** paso 4 subrepticio — una ausencia resuelta con un valor por defecto que se lee como campo. Pendiente ya registrado (`temp_signal` debe admitir UNKNOWN, c06db07).

**Propuesta:** declarar en §4.8 y en §6 que el NOMINAL de las firmas IAP no lo produjo COCO.

> **Corrección (4 oct, más tarde):** esto lo leí en la copia local `ckm___repo`, que está atrasada. En GitHub HEAD (`2097ca4`) ya está corregido por `c06db07`: el fallback de `temp_signal` es `UNKNOWN`. Lo que queda vigente es el paper: las firmas IAP históricas dicen NOMINAL por ausencia, y §4.8 no lo declara.

## O7 — "Verified" en P4/P5 (§5.2, §8.1)

**Dice:** P4 y P5 *Verified* (líneas 237, 239, 652, 653).

**Pendiente ya registrado:** ninguna W_mixta se verificó contra nulo (SUPERTASK §5). Y REG_borrador_salamanca_s1_v1: *"modularidad no es adversarialidad"*; sin control positivo.

**Con la regla:** "Verified" sin nulo es un rótulo de §3.8 aplicado sin el criterio de campo que §3.8 define ("confirmed experimentally under stated conditions"). La condición no declarada es el nulo.

**Propuesta:** P4/P5 → *verified as measurement; null not run* (o la etiqueta que delamor elija de §3.8).

## O8 — El ruteo sin nulo y SALAMANCA (§5.1)

**Dice** (línea 225): "The procedure has no null outcome — it always finds markers in sufficiently long texts."

**Falta:** SALAMANCA es el criterio que sí puede devolver vacío, y ya devolvió "no medible" en dos corpus por saturación y uno por tamaño. `salamanca` y `modular`: 0 en el paper.

**Propuesta:** decidir si S1 entra al paper ahora (como criterio con nulo, sin control positivo) o queda para cuando corra RfA. Si entra: con su recuento de comparaciones (~112) y su "no cierra".

## O9 — ¿Qué dispara COCO? Tres nombres (§4.6, §8.3)

Paper: "When **D_ckm** crosses its threshold" · §8.3: mover a **D_masa_cuencas** es decisión abierta · nota de delamor: "d?eff es FORMULA CANONICA / COCO DISPARA SOBRE **d_eFF**".

**Con la regla:** paso 3. No lo resuelvo. ¿d_eff es D_masa_cuencas, N_eff, u otra fórmula? Lo decide delamor; si cambia, tocan §4.3, §4.6, §4.8 y §8.3.

## O10 — Lo que se registra tiene costo (§3.4, §4.8)

§3.4 *Trace as Constitutive of Knowledge* y §4.8 WVersionManager ("not a copy of W, the trace that W changed") ya distinguen traza de copia. Lo del 4 oct agrega: **la traza no cuesta; su representación sí, y elegir qué se representa es un criterio** — la regla se aplica a sí misma. Y: *el conocimiento se accede, no se tiene ni se almacena.*

**Propuesta:** una frase en §3.4, si delamor la quiere ahí. Es la más prescindible de estas observaciones.

---

## Orden sugerido (Opus — sólo sugerencia)

Primero las que corrigen afirmaciones: **O7, O6, O2**. Después las que acotan: **O3, O5**. Después las que nombran: **O1, O4**. Las que esperan una decisión del modelo: **O8, O9**. **O10** al final o nunca.
