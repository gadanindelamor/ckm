# REG_perspectivas_v1

Clase R. **Borrador.** Pasa a `registers/` con el OK de delamor.

*23 oct 2026. gadanin.delamor + Claude Opus 5.5 (Cowork).*
*Fuentes: la conversación del 23 oct; Informe de Trabajo v1 y v4 (`antropic/ckm___memories/informes_md_draft/`); `docs/Informe_Sciamarella_CKM.md` §2.3; `docs/CKM_Modelo_Hibrido.md`; `services/monitor_service.py`. Hilo completo: `docs/opus/HILO_perspectivas_subgrafo_inducido_23oct2026.md`.*

---

## El intento que subyace

Que las perspectivas no queden como metadato pegado al grafo: que pesen desde adentro. Y ubicar **cuándo** pesan.

---

## 1. Textual *(delamor, 23 oct)*

```
hay algo con la unión A ∪ B, que no es igual a G de A ∪ G de B
es como si dentro de yo, device delamor, está A y una B
y esa unión hace algo en relación al conocimiento

unión de subgrafos inducidos extienden el todo
contra el cual la comprensión relaciona

las perspectivas calibran desde adentro los pesos
¿cuándo ocurre ese ajuste de pesos con sus grafos? ¿en qué instancia?

puede ser el rebuild, sí. y es algo más también, o lo era
fue formulado con W estática, aun sin saber que era estática
```

Palabras clave *(delamor)*: **subgrafo inducido · perspectiva · ajuste de pesos · desde adentro.** Al despojarlo, quedan afuera las inconmensurables y las R.

## 2. Antecedentes escritos *(abril 2026, Informe v1; numeración del v1)*

- **Perspectiva de device:** "estado de creencia parcial de un device sobre el mundo. Múltiples perspectivas coexisten en un mismo device. La divergencia entre ellas es información."
- **R08** "Cada device tiene perspectivas múltiples sobre el grafo." **R09** "Las perspectivas afectan los pesos de las relaciones desde adentro — no como metadato externo." **R10** "El mecanismo que orienta la perspectiva activa hacia lo que la situación pide debe ser implementado." **R11** "La divergencia entre perspectivas es información, no ruido."
- **Pendiente declarado:** "modelo formal de perspectiva como subgrafo".
- **El cuándo**, en la incógnita central: "lo que la situación pide… orienta la perspectiva activa del device hacia la acción relevante **en el instante**… opera en el META KNOWLEDGE: **disponible mientras sucede, no antes ni después.** No se puede diseñar sin haberlo observado. Se puede registrar cuando ocurre."
- **Los dos momentos** del CKM: antes de incorporar se verifica el nodo nuevo contra el grafo; después, hay un proceso continuo que ajusta los pesos (la red de verificación continua).
- **Informe v4:** la numeración se corre (R08 = desde adentro, R09 = lo que la situación pide). R13: "lo que emerge en el cruce no pertenece a ninguna — es nodo del campo, no del grafo". "R09 permanece sin modelo — es la pieza faltante más crítica del diseño."
- **Sciamarella §2.3:** "una perspectiva VP es el Máximo Subgrafo Inducido por los nodos disponibles (propuesta R09)".

## 2b. REG anterior — `registers/REG_sesion_perspectivas_rp2_ff_v7.md` (mayo 2026)

**Corrección de Opus (A3):** este borrador se escribió sin haber leído ese REG. Lo que dice ahí:
- **Unión G[A∪B]:** "Ambas perspectivas activas simultáneamente. Produce atractor propio con c(S) > perspectivas puras. **G[A∪B] ≠ G[A] + G[B]**", marcada como **verificada (Escenario 3, v11)**.
- **Intersección A∩B:** los nodos bisagra, implementada. **Contacto R13:** definido. **Divergencia R10/R11:** definida. **Dos umbrales R13:** definidos.
- Marcadas como no definidas: la composición secuencial, la métrica entre VPs y la operación inversa del contacto.
- La dirección RP² (VP como punto; join p_A ∨ p_B como candidato para G[A∪B]) aparece como "dirección, no correspondencia probada".
- Ese REG **no dice cuándo** se ajustan los pesos desde adentro.

Pendiente: leer el Escenario 3 (v11) en la fuente y saber con qué código se verificó.

## 3. Forma *(matemática estándar)*

Perspectiva A ⊆ V. Su grafo es el **subgrafo inducido** G[A]: los nodos de A con todas las W_ij entre ellos.

```
G[A ∪ B] = G[A] ∪ G[B] ∪ E(A, B)
E(A, B) = { (i, j) : i ∈ A∖B, j ∈ B∖A, W_ij ≠ 0 }      el corte
```

La unión de los grafos no es el grafo de la unión: le falta el corte. En CKM, el corte son las W_ij con un extremo de cada lado, y sobre ellas también actúa la relajación.

## 4. Estado en el código *(verificado el 23 oct)*

| Lo formulado | En el código |
|---|---|
| Perspectiva como subgrafo inducido | No está en `services/`. El REG de mayo marca la unión como verificada en el Escenario 3 (v11), con un código que todavía no ubiqué. |
| Lo que la situación pide (la perspectiva activa) | No existe |
| Red de verificación continua | No existe |
| Ajuste desde adentro, dentro de una W | Lo más cercano es `Δ_r_pares`: W_eff = W + Δ_r, con lo que la relajación rechaza. No tiene perspectiva y **se pone en cero cuando cambia W**. |
| Ajuste de todos los pesos | El rebuild (Hebb): entra un texto y se recuentan las co-ocurrencias. Es un ajuste desde afuera. |

## 5. Abierto

- **El cuándo.** El Informe lo ubica en el instante; delamor dice que "puede ser el rebuild, y algo más, o lo era". Con W estática, el instante era el único lugar posible. Con rebuild hay dos, bajo un mismo nombre. *(Lectura de Opus, no verificada.)*
- **Qué hace la unión.** Que el corte E(A, B) sea donde "la unión hace algo en relación al conocimiento" es una tensión de delamor, sostenida.
- **La explicación de Sonnet** (abril de 2026, "de un nivel más arriba", "gracias, gracias, gracias Sonnet") no se encontró. La búsqueda desde TRUST no llega a esos chats. Si aparece, se compara con este REG y se registra qué coincide, qué no y qué falta.

---

*Se registran las condiciones, no el contenido. Lo que pasó en el "ahhh claroo" no está acá: está la traza de que ocurrió.*
