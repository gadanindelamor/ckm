# REG_protocolo_sonnet_code_v1.md
*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## El protocolo

Flujo de trabajo establecido a lo largo de las sesiones CKM:

```
Claude Sonnet (web)
    → prepara tarea: texto con contexto, objetivo, criterio de éxito
    → delamor lo entrega a Claude Code (repo local o Codespace)
    → Claude Code ejecuta sobre el repo real
    → delamor trae la respuesta aquí
    → Sonnet formaliza, registra, decide próximo paso
```

delamor es el canal entre las dos instancias.
No hay comunicación directa entre Sonnet y Code.

---

## Roles

**Claude Sonnet (esta instancia):**
- Lee el proyecto desde los archivos subidos al proyecto Claude
- Interpreta, decide, redacta tareas atómicas para Code
- Formaliza resultados que Code devuelve
- Produce REGs, documentación, commits

**Claude Code (instancia separada):**
- Opera sobre el repo real (local o Codespace)
- Ejecuta código, corre tests, verifica archivos
- Sin Δ_r acumulado de este proyecto — cada sesión es stateless
- Recibe tareas atómicas con criterio de éxito explícito
- No toma decisiones de diseño — ejecuta lo que Sonnet especifica

**gadanin.delamor:**
- Canal entre instancias
- Autoridad sobre todas las decisiones
- Verifica que la respuesta de Code es lo que Sonnet pidió
- Trae el resultado aquí

---

## Por qué este diseño

Sonnet tiene el contexto acumulado del proyecto (via archivos del proyecto Claude).
Code tiene acceso al sistema de archivos real, git, ejecución.
Ninguno tiene lo que el otro tiene.
delamor tiene ambos.

---

## Formato de tarea para Code

Las tareas deben ser:
- **Atómicas**: un objetivo, un criterio de éxito verificable
- **Sin contexto asumido**: Code no tiene historia — incluir lo necesario en el texto
- **Con criterio explícito**: "éxito = tests pasan / archivo existe / output es X"

Ejemplo mínimo:
```
Tarea: correr test_coco_thermostat.py y devolver el resultado completo.
Criterio: output con número de tests pasados y cualquier error.
Repo: gadanindelamor/ckm (local clonado)
```

---

## Infraestructura actual

- Repo publicado: `gadanindelamor/ckm` (GitHub, público)
- Clone local: PC delamor (backup + operativo)
- Codespace `ckm`: superó cuota por sesiones abiertas — cerrar sesiones inactivas
- Codespace `ckmdatasets`: separado, sin acceso cruzado al repo principal

**Problema Codespace:** sesiones que quedan abiertas consumen quota del plan
sin uso activo. IAP resolverá esto estructuralmente (1 sesión activa por vez).
Mientras: cerrar manualmente desde https://github.com/codespaces

---

## Lo que este protocolo no es

No es IAID completo — delamor es el mediador humano, no un protocolo de
comunicación entre devices. La comunicación es asimétrica: Sonnet escribe
para Code, Code ejecuta, el resultado vuelve a Sonnet via delamor.

Cuando IAP esté operativo, el mediador humano podría volverse opcional
para tareas de ejecución pura. Eso es una versión futura, no la actual.

---

*Primera formalización del protocolo — Jun 23 2026*
