# MÓDULO TRANSVERSAL · ESTRATEGIA DE TESTING — versión profunda
> Transferencia Fable 5 · 2026-06-11 · se carga en dispatches de implementación de
> código (CREATE_NEW / REWRITE / REFACTOR) y en TODO fix de bug, además del pilar.
>
> **SCOPE: el MÉTODO es UNIVERSAL.** Los ejemplos (un proveedor de pagos, DOB, food-vision) son
> material didáctico de el proyecto — en otro proyecto: mismo método, flujos críticos
> DEL proyecto activo. Scope Discipline manda.
>
> **Contexto que motiva este módulo:** riesgo documentado del proyecto = 0% coverage
> con ~311 commits/semana de una sola dev. El objetivo NO es "tener coverage": es
> comprar el seguro contra regresión más barato que proteja lo que mata.

## A) Framework Mental

**Un test es un seguro, no un certificado.** Se compra donde el siniestro es caro
(pagos, auth, datos sensibles, onboarding) y no se compra donde el siniestro es trivial
(un margin mal alineado lo caza pixelmatch, no un unit test).

**Pirámide INVERTIDA para solo-founder pre-launch:** pocos E2E smoke de flujos críticos
> tests de integración en los BORDES (webhooks, auth, persistencia) > unit SOLO para
lógica pura compleja (cálculos, gates, fechas). La pirámide clásica (miles de units)
asume un equipo que los mantiene; acá cada test debe pagar su mantenimiento con riesgo
real cubierto.

**El mejor test es el que falla cuando un usuario habría sufrido.** Test que falla
cuando refactorizas internals sin romper comportamiento = test malo: castiga mejorar.
Se testea el CONTRATO observable (qué entra, qué sale, qué queda en la DB), no la
implementación.

**El coverage crece donde duele:** cada bug arreglado deja el test que lo habría
cazado (test post-mortem). Así la suite es un mapa de las heridas reales del producto,
no un trofeo de porcentaje. Con esta regla, 6 meses de bugs = la suite de regresión
exacta que ESTE producto necesita.

**Verde confiable o nada:** un test flaky enseña al equipo a ignorar el rojo — es
PEOR que no tener test. Flaky = se arregla hoy o se borra hoy.

## B) Algoritmos de Ejecución

### B1. Partiendo de 0% coverage (el orden exacto, máximo ROI primero)

1. **Smoke E2E de los flujos que generan plata/confianza** (4-6 tests, no más):
   login+SSO completo · onboarding entero hasta Mi día · registrar comida (texto y
   foto) · pago sandbox end-to-end · chat básico con el asistente. Herramienta: la que ya
   está en el stack (Playwright/agent-browser — el harness de /qa ya existe).
2. **Bordes con fixtures** (los bugs caros viven acá): webhook con firma inválida →
   401 · webhook duplicado → idempotente (1 efecto) · payload malformado → 4xx sin
   crash · sesión expirada en mutación → 401 limpio.
3. **Unit de lógica pura crítica:** cálculo de calorías/macros · gate 18+ (límites:
   17.99 años rechaza, 18.0 pasa) · parsing de fechas DD-MM-AAAA · slugs/validadores
   compartidos.
4. Recién después: lo demás, SI un bug lo justifica (regla post-mortem).

### B2. Anatomía de un buen test

- **Arrange-Act-Assert**, un comportamiento por test.
- **El nombre es la regla de negocio:** `rechaza_registro_si_DOB_menor_de_18`, no
  `test_validate_1`. La suite se LEE como spec.
- **Datos mínimos realistas** via factory (un `makeUser({dob})`) — no fixtures de 40
  campos donde no se ve qué importa.
- **Real barato > mock elaborado:** DB de test real (Postgres efímero) supera un mock
  de ORM que miente sobre constraints — los bugs de idempotencia VIVEN en la DB real.
  Mock solo para lo caro/externo (API de MP, LLM).
- **Determinista por construcción:** clock inyectado (jamás `new Date()` en lógica
  testeada), sin sleeps (esperar condiciones, no tiempo), sin red real, seeds fijos.

### B3. Qué NO testear (tan importante como qué sí)

- Implementación interna (orden de llamadas privadas, estado intermedio).
- UI visual trivial — el gate pixelmatch del atlas ya cubre fidelidad visual.
- Código de terceros (Cloudinary funciona; testea TU adaptador con fixture).
- Getters/setters/mapeos triviales.
- Lo que typecheck ya garantiza (TS es la primera suite — gratis).

### B4. Test post-bug (la receta, obligatoria)

1. Reproducir el bug EN un test → correr → ROJO (si no da rojo, el test no reproduce
   el bug — no sigas).
2. Aplicar el fix → VERDE.
3. Commitear test + fix JUNTOS (el test documenta el incidente para siempre).
4. El nombre del test referencia el síntoma: `onboarding_no_pierde_DOB_tras_redirect_SSO`.

### B5. CI y disciplina de suite

- En cada push: typecheck (ya ley) + unit/integración rápidos (<2 min budget).
- Smoke E2E: antes de release/build (mobile: /smoke-agent ya es ley) — no en cada push
  si frena la velocidad.
- Presupuesto de velocidad: si la suite rápida pasa de ~2 min, se poda o paraleliza —
  una suite lenta se deja de correr, y una suite que no corre no existe.
- Datos de test: SIEMPRE sintéticos (PII real en fixtures = filtración con coverage).

## C) Reglas de Oro (inquebrantables)

- Todo bug arreglado deja su test, commiteado junto al fix. Sin excepción.
- Flujo de plata (pagos) o de seguridad (auth, 18+, PII): tests ANTES de tocar el código.
- Test flaky = arreglar hoy o borrar hoy. Convivir está prohibido.
- Se testea contrato observable, no implementación.
- DB real efímera > mock de DB. Mock solo para lo externo caro.
- Clock inyectado, cero sleeps, cero red real en la suite rápida.
- PII jamás en fixtures — datos sintéticos siempre.
- Coverage % no es objetivo ni se reporta como logro; "flujos críticos cubiertos: sí/no"
  es el reporte.
- El rojo se arregla antes de seguir — un main rojo 2 días deja de ser señal.

## D) Desafíos de Sincronización (resueltos a fondo)

### D1. Suite mínima viable para 0% coverage (~12 tests, ~1 día, 80% del riesgo)

Priorizada — cada test con qué siniestro evita:
1-3. **Webhook MP** (integración, fixtures): firma inválida→401 (endpoint abierto al
mundo) · `mp_event_id` duplicado→1 solo efecto (doble cobro/activación) · `approved`
actualiza suscripción (el flujo de plata completo).
4-6. **Gate 18+** (unit): 17.99 rechaza · 18.0 exacto pasa · DD-MM-AAAA malformado
rechaza con error claro (compliance + Play Store).
7-8. **Cálculo macros/calorías** (unit): plato conocido da valores esperados · gramos
fuera de rango plausible rechaza (la DB calcula, el cálculo es testeable puro).
9. **Draft de onboarding sobrevive redirect** (integración — el test del incidente DOB,
ver D2).
10-12. **E2E smoke**: login+SSO hasta Mi día · registrar comida texto → aparece en muro
y suma totales · flujo de pago sandbox → estado premium activo.
**ROI explícito:** estos 12 cubren pagos, auth, compliance, el dato core y el incidente
histórico — todo lo demás puede esperar a su primer bug.

### D2. El test que habría cazado el bug DOB (receta del patrón "estado cruza redirect")

Integración con render real del flujo: (1) montar onboarding → llenar DOB → avanzar
(persiste draft), (2) DESMONTAR el árbol completo (simula el redirect SSO — unmount
real, no un mock de navegación), (3) re-montar root → assert: el flujo continúa en el
paso correcto Y el DOB llega al submit final. **Por qué este diseño:** el bug vivía en
el UNMOUNT — un test que solo navegara "hacia adelante" jamás lo ve. El patrón
generaliza: todo estado que deba sobrevivir a X (redirect, kill de app, pérdida de red)
se testea ejecutando X de verdad.

### D3. Testear lo no determinista (LLM — conecta con llm-engineering.md)

El texto del modelo NO se asserta (cambia entre corridas y modelos). Se asserta el
CONTRATO: (1) la salida parsea contra el schema zod, (2) los valores caen en rangos
plausibles (gramos 1-2000, kcal coherentes), (3) las acciones propuestas ∈ allowlist,
(4) con input de injection conocido (foto-con-texto malicioso de fixture), el output
NO obedece la instrucción embebida. Para cambios de prompt: eval-set de casos reales
(no unit tests) — golden cases con tolerancia, pass/fail por contrato. El eval-set
crece con cada fallo de producción, igual que la suite con cada bug (misma filosofía,
distinto instrumento).

## Cierre del módulo

Con 0 coverage la pregunta no es "¿cómo llego a 80%?" — es "¿qué 12 tests me dejan
dormir?". Esa lista existe (D1), cuesta un día, y desde ahí la regla post-bug hace
crecer la suite exactamente donde el producto demostró que se rompe. Velocidad sin
seguro es deuda con interés compuesto; el seguro correcto cuesta un día.
