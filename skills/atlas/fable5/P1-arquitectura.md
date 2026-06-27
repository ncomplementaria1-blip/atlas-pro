# PILAR 1 · ARQUITECTURA DE SOFTWARE Y SISTEMAS — versión profunda
> Transferencia Fable 5 · 2026-06-11 · se carga en dispatches backend/schema/webhook/cron/auth.
> El resumen ejecutivo vive en `../fable5-transfer-playbook.md` — esto es el nivel completo.
>
> **SCOPE: el MÉTODO es UNIVERSAL** (frameworks, algoritmos, árboles de decisión sirven
> para cualquier proyecto y stack). Los desafíos y varios ejemplos usan casos reales de
> el proyecto como material didáctico. En OTRO proyecto (atlas-pro, cokrea, keto...):
> replicar el MÉTODO; las reglas de dominio/marca ([el proyecto]: la normativa de protección de datos, deudas
> específicas, excepción 18+, patrones MP/un canal de mensajería) NO viajan — las del proyecto activo
> se cargan de `projects/<name>/` + el CLAUDE.md de su repo. Scope Discipline: NUNCA
> mezclar proyectos.

## A) Framework Mental — los 5 lentes

Miro toda feature backend a través de cinco lentes, EN ESTE ORDEN. El orden importa:
cada lente descarta diseños enteros antes de que el siguiente gaste tiempo en ellos.

1. **Fuentes de verdad.** Cada dato tiene UNA dueña nombrable (tabla.columna o módulo).
   Si dos lugares pueden responder la misma pregunta, el bug ya existe — solo falta la
   fecha. Prueba operativa: "¿cuántas calorías registró hoy?" debe tener UNA query
   canónica. Los demás consumidores derivan de ella, jamás recalculan por su cuenta.
2. **Bordes.** Todo lo externo FALLA: la red se corta, el webhook llega dos veces, el
   cron corre tarde o dos veces, el usuario manda el form dos veces, un proveedor de pagos
   reintenta hasta 4 veces, un canal de mensajería duplica mensajes. El diseño empieza en el borde,
   no en el happy path. El interior del sistema confía; el borde, jamás.
3. **Idempotencia antes que retry.** Un retry sin idempotencia es un generador de
   duplicados con timer. Primero hago la operación segura de repetir (constraint UNIQUE,
   UPDATE condicional atómico), DESPUÉS le pongo reintentos.
4. **Blast radius.** ¿Qué se rompe si ESTO se rompe? Un cron caído que nadie nota por
   3 días vale más diseño defensivo que un endpoint que truena en la cara del usuario
   (ese al menos avisa). Lo silencioso es lo peligroso: por eso todo borde loggea
   estructurado y todo cron deja huella de "corrí a las X, procesé N".
5. **Lo aburrido gana.** Postgres hasta que duela. Monolito modular hasta que duela.
   Un equipo de 1 (Ale) no paga el impuesto operativo de microservicios JAMÁS — cada
   servicio nuevo es un deploy, un log, un modo de fallo y una página de status más.
   "Escalable" para el proyecto = índices correctos + queries planas + cache medido.

Escalamiento horizontal mental: ¿qué estado impide clonar el proceso? (sesiones en
memoria, archivos locales, locks en RAM, contadores in-process). Compute stateless,
estado en Postgres/objeto-store. Amplify ya clona el web server — el diseño está bien
si nunca tuvimos que pensarlo.

## B) Algoritmos de Ejecución

### B1. Diseño de una feature backend (el paso a paso completo)

1. Clasificar cada dato: **transaccional** (registro de comida, pago, invitación) /
   **derivado** (NutriScore, totales del día, streak) / **efímero** (draft, estado UI).
   Derivado JAMÁS se guarda como verdad — se recalcula o se cachea con invalidación
   explícita y nombrada.
2. Asignar dueño: una tabla, una columna, un módulo. Escribirlo en el plan.
3. Contrato en el borde: schema SQL con constraints + validación zod en CADA entrada
   externa (API route, webhook, payload de cron). Tipos compartidos en `shared/` —
   single source (el patrón de los slugs datos sensibles es el canon: replicarlo).
4. **La pregunta triple** antes de codear: ¿qué pasa si esto llega DOS VECES? ¿TARDE?
   ¿NUNCA? Cada respuesta es código o constraint, no esperanza.
5. Idempotencia mecánica: la DB es el árbitro, no un if en JS. `INSERT ... ON CONFLICT
   DO NOTHING` para eventos · `UPDATE ... WHERE status='pending'` atómico para
   transiciones de estado · tabla de eventos procesados para webhooks (ver D1).
6. Observabilidad mínima viable: log estructurado del borde — qué llegó (id, tipo),
   qué se decidió (acción, razón), qué se respondió (status). Una línea JSON por evento.
   Sin esto, el incidente de las 2am es arqueología.
7. Migración reversible: toda migración tiene plan de vuelta escrito. Si no lo tiene,
   es operación destructiva → STOP Ale (ley inmune).

### B2. Decisión de cache (árbol completo)

```
¿La query es lenta O cara O se repite mucho?
├─ no → NO cachear. El cache prematuro es deuda con intereses.
└─ sí → ¿el dato puede estar stale N segundos sin daño?
    ├─ no (saldo de pago, estado de invitación) → NO cachear. Optimizar la query.
    └─ sí → ¿quién lo consume?
        ├─ todos igual (catálogo alimentos, planes) → cache server (memoria/LRU)
        │   TTL = frecuencia de cambio real del dato (alimentos: horas, no segundos)
        ├─ por usuario (totales del día) → client cache (React Query) con
        │   invalidación al MUTAR (registrar comida → invalidate(['totales', fecha]))
        └─ estático público (landing, imágenes) → CDN/Cloudinary, cache infinito + hash
INVALIDACIÓN: nombrada y quirúrgica. "Invalidar todo" = confesión de que no se sabe
qué depende de qué. Cada mutación lista QUÉ caches toca.
```

### B3. ¿Cola, cron o inline? (umbrales concretos)

| Señal | Veredicto |
|---|---|
| Respuesta que el usuario espera (<2s) | inline en el route, transaccional |
| Trabajo diferible disparado por evento, volumen bajo (<100/h) | inline post-respuesta o cron corto — NO cola |
| Trabajo periódico (recordatorios, proactivo un canal de mensajería) | cron (ya es el patrón: `el asistente-proactive`, `meal-reminders`) |
| Volumen alto + picos + reintentos con backoff | recién AHÍ una cola — y es un cambio de arquitectura → /plan-eng-review |

Una cola agrega un modo de fallo nuevo (mensaje perdido/duplicado/atascado) — solo se
justifica cuando QUITA más modos de fallo de los que agrega. A escala el proyecto, casi
nunca.

### B4. Optimización de queries (método, no recetas)

1. Medir primero: `EXPLAIN ANALYZE` de la query real con datos realistas. Sin medición
   no hay optimización, hay superstición.
2. Leer el plan en este orden: ¿**Seq Scan** sobre tabla grande? → falta índice o el
   índice no es usable (función sobre la columna, tipo distinto, OR). ¿**rows**
   estimado vs real difieren >10x? → estadísticas viejas (`ANALYZE`) o correlación que
   el planner no ve. ¿**Nested Loop** sobre miles de filas? → falta índice en el lado
   interno del join.
3. Índices: para cada FK que se joinea, índice (deuda real conocida: 8 FK sin índice —
   no crear la novena). Índice compuesto: columna de igualdad primero, rango después
   (`(user_id, fecha)` para "registros del usuario en el mes"). Cada índice cuesta en
   cada INSERT — no coleccionarlos.
4. N+1: la señal es un loop con await adentro. Fix: una query con JOIN o `IN (...)`,
   jamás "después lo cacheo".
5. Paginar TODO lo que crece con el tiempo (registros, mensajes). Cursor (`WHERE
   created_at < $last`) sobre OFFSET — OFFSET escanea lo que salta.

### B5. Seguridad aplicada (el threat model de 10 minutos)

> Versión profunda en `seguridad.md` (mismo dir) — OBLIGATORIA cuando safety_touch=yes:
> auth/OAuth2 completo, web/mobile/LLM security, secrets, la normativa de protección de datos, respuesta a incidentes.

Por cada feature nueva, recorrer STRIDE-lite — 5 preguntas, 10 minutos:
1. **Suplantación**: ¿cada endpoint verifica QUIÉN llama? (sesión server-side; el
   user_id viene de la sesión, JAMÁS del body — un body con user_id ajeno es IDOR).
2. **Manipulación**: ¿el webhook verifica firma? (un proveedor de pagos: validar firma/secret;
   un canal de mensajería: app_secret + verify token — infra ya en prod, no recrear).
3. **Repudio**: ¿queda huella de quién hizo qué? (created_by, logs de borde).
4. **Filtración**: ¿este dato es PII/sensible? → minimizar (hash de email en vez de
   email cuando solo se compara), cifrar en reposo, la normativa de protección de datos Chile. ¿El error
   response filtra internals? (stack traces a producción = no).
5. **Elevación**: ¿qué pasa si un usuario free llama el endpoint premium directo?
   (el gate se verifica server-side por request, no en el cliente).
OAuth2/auth/pagos/schema/PII = `safety_touch=yes` → /matu canonical SIEMPRE, sin
negociación. Deuda conocida a NO empeorar: OAuth tokens en plaintext + sin RLS — toda
feature nueva que toque esas zonas las mejora o al menos no las extiende.

### B6. CI/CD e infraestructura como código

El pipeline actual: typecheck → push a main → deploy Amplify. Principios:
- Cada paso manual es un paso que un día se salta. Automatizar el gate, no el recordatorio.
- La config de infra vive en el repo (amplify.yml, env declaradas) — el ambiente se
  reconstruye desde el repo, no desde la memoria de nadie.
- Migración + deploy: la migración corre ANTES del código que la necesita, y es
  compatible hacia atrás un deploy (el código viejo debe poder convivir con el schema
  nuevo durante el rollout). Columna nueva = nullable o con default barato; JAMÁS un
  default que reescribe la tabla entera en caliente.
- Env vars nuevas de prod = STOP Ale (ley inmune — credenciales externas).

## C) Reglas de Oro (inquebrantables)

- Todo webhook idempotente — un proveedor de pagos y un canal de mensajería REINTENTAN por diseño.
- El user_id sale de la sesión, jamás del body. (IDOR es el bug #1 de apps de 1 dev.)
- Validación zod en el borde, tipos en `shared/`, single source.
- Secrets jamás en el repo; dato sensible cifrado en reposo (la normativa de protección de datos).
- DDD-lite: módulos por dominio dentro del monolito. Microservicios = prohibido a este
  tamaño de equipo.
- Índice para cada FK joineada. Paginación por cursor para todo lo que crece.
- Transacción corta: JAMÁS una llamada externa (HTTP, LLM) dentro de una transacción
  abierta — bloquea conexiones y escala el blast radius.
- Retry siempre con backoff exponencial + tope. Retry infinito = DoS a uno mismo.
- Migración destructiva o masiva = STOP Ale. Arquitectura nueva grande → /plan-eng-review.
- Lo que no se puede explicar en un diagrama de flujo de datos de 1 pantalla, está
  sobre-diseñado.

## D) Desafíos de Sincronización (resueltos a fondo)

### D1. Webhook un proveedor de pagos idempotente (dinero = cero tolerancia)

**Datos:** tabla `payment_events`: `id`, `mp_event_id` UNIQUE (la clave de la
idempotencia), `type`, `payment_id`, `status`, `raw` jsonb, `processed_at` nullable,
`created_at`. El UNIQUE sobre `mp_event_id` es el árbitro.

**Flujo:** webhook llega → validar firma → `INSERT ... ON CONFLICT (mp_event_id) DO
NOTHING RETURNING id` → si no retornó fila, ya lo vimos: responder 200 y salir (responder
200 SIEMPRE que el evento sea válido aunque sea duplicado — si respondes 500, MP
reintenta para siempre). Si retornó fila → procesar: consultar el pago a la API de MP
(la verdad es la API, no el payload del webhook — el webhook es solo el timbre) →
actualizar la suscripción en la MISMA transacción que marca `processed_at`.

**Pregunta triple:** ¿dos veces? → ON CONFLICT lo absorbe. ¿tarde? → se consulta el
estado actual a la API, no se confía en el orden de llegada (un "approved" puede llegar
después de un "refunded": por eso la API es la verdad). ¿nunca? → cron de reconciliación
diario: pagos `pending` >24h se consultan activamente.

**Blast radius:** si el procesamiento falla post-INSERT, el evento queda sin
`processed_at` → el cron de reconciliación lo retoma. Nada depende de que el webhook
llegue: el webhook ACELERA, la reconciliación GARANTIZA.

### D2. Cron proactivo un canal de mensajería (ventana 24h + dedupe)

**Restricción dura de Meta:** fuera de la ventana de 24h desde el último mensaje del
usuario, solo se pueden enviar PLANTILLAS aprobadas. El cron debe: (1) seleccionar
usuarios elegibles (allowlist `el asistente` — infra ya en prod), (2) por
usuario, decidir ventana: ¿último mensaje entrante <24h? → mensaje libre; si no →
plantilla aprobada o saltar, (3) dedupe: tabla `proactive_sends` con UNIQUE
`(user_id, campaign, fecha)` — el cron puede correr dos veces sin duplicar envíos,
(4) presupuesto: tope de envíos por corrida (un bug no debe spamear a toda la base),
(5) huella: log "corrí a las X, evalué N, envié M, salté K por ventana".

**El modo de fallo que importa:** cron corre dos veces (cron-job.org reintenta, deploy
en el medio). El UNIQUE de `proactive_sends` lo absorbe — idempotencia por constraint,
no por "esperemos que no pase".

### D3. Decisión de NO-arquitectura: unificar los dos sistemas de planes

Hechos: web usa `diet_plans`, mobile usa `weekly_plans/architect` (documentado: no
mezclar). La tentación arquitectónica: "unifiquemos en un solo modelo". Mi análisis:

- Costo de unificar AHORA: migración de datos viva + reescribir dos superficies +
  riesgo de regresión en pagos/planes (zona safety) — semanas, en pre-launch de stores.
- Costo de NO unificar: dos modelos a mantener, confusión documentada (ya mitigada con
  memoria + ley de no mezclar).
- Reversibilidad: unificar es difícil de revertir; convivir es reversible cuando quiera.
- **Veredicto: NO unificar ahora.** Congelar la frontera (cada superficie su sistema,
  documentado), unificar post-launch con datos reales de cuál modelo sirve mejor.
  Registrarlo en BACKLOG con trigger explícito ("post Play Store + App Store live").

La lección transferida: la decisión arquitectónica más frecuente y más ignorada es
"todavía no". Se toma con costo/reversibilidad/timing, no con elegancia.

## Anti-patrones que me cazo (catálogo P1)

- **God-route:** un endpoint que hace fetch + validación + 4 efectos + email. Partir
  en módulo de dominio + efectos diferibles.
- **N+1 con await en loop.** JOIN o IN, siempre.
- **Llamada externa dentro de transacción abierta.** Cerrar la transacción, llamar,
  segunda transacción corta para el resultado.
- **Retry sin idempotencia ni backoff.** Primero constraint, después retry, siempre tope.
- **El cron silencioso.** Sin huella de ejecución = no existe hasta que explota.
- **Default pesado en migración.** `ALTER TABLE ... ADD COLUMN ... DEFAULT now()` sobre
  tabla grande = lock + reescritura. Nullable primero, backfill por lotes, NOT NULL al final.
- **"Lo cacheo y listo".** Cache sin estrategia de invalidación nombrada = bug de datos
  stale en 2 semanas.
- **Config en la cabeza.** Si reconstruir el ambiente requiere recordar algo, está mal.
