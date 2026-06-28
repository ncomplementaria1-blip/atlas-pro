# PILAR 1-SIS · ARQUITECTURA DE SISTEMAS — nivel sistema, no feature
> Complemento de P1-arquitectura.md (feature-level). Este archivo sube al nivel SISTEMA.
> Canon: Fowler · Sam Newman · Kleppmann (DDIA) · Evans (DDD) · Hohpe · Richardson · Vogels · DORA · C4 · Building Evolutionary Architectures.
> Cargar cuando: nueva arquitectura · decisión de división de servicios · migración de sistema · ADR · review de diseño sistémico.

---

## 1. DECISIÓN Y TRADEOFFS

**Toda arquitectura es una apuesta sobre qué va a cambiar.** No existe arquitectura neutral; existe arquitectura que explicita sus apuestas y arquitectura que las esconde.

- **ADR obligatorio** para toda decisión de peso-sistema: contexto · opciones consideradas · decisión · consecuencias (positivas Y negativas). Sin ADR, la decisión se desinforma en 6 meses. Formato mínimo: `docs/adr/NNNN-titulo.md`. El valor no es el documento — es el razonamiento que queda.
- **One-way vs two-way doors** (Bezos/Vogels): clasificar antes de decidir. Two-way = reversible con costo razonable (cambiar un endpoint, agregar un índice) → decidir rápido. One-way = difícil de revertir (romper un contrato público, partir un monolito, adoptar un message broker) → deliberar, documentar, postergar si hay duda. La mayoría de las decisiones de arquitectura son two-way sobreestimadas como one-way.
- **"It depends" con criterios explícitos.** "Depende" sin criterios es señal de no haber pensado. El árbol de decisión explícito (si X entonces A, si Y entonces B) es el entregable; el criterio se agrega al ADR.
- No optimizar para el sistema que podrías necesitar. Optimizar para el sistema que necesitás ahora más el headroom de 18 meses.

---

## 2. LÍMITES Y ACOPLAMIENTO

**El mayor riesgo de arquitectura no es código malo — es límites mal trazados.** Un límite mal trazado crea acoplamiento oculto que crece con cada feature.

- **Bounded Context (DDD-Evans):** cada contexto tiene su modelo propio de dominio. "Usuario" en pagos no es igual que "usuario" en perfil sensible. Forzar un modelo único que sirva a todos = el god-object del dominio. Cuando dos equipos (o módulos) tienen definiciones distintas del mismo concepto, hay dos bounded contexts, no un malentendido.
- **Alta cohesión, bajo acoplamiento:** lo que cambia junto vive junto; lo que cambia por razones distintas se separa. Señal de acoplamiento: cambiar A requiere cambiar B aunque B no sea el motivo del cambio.
- **Dependencias dirigidas:** los grafos de dependencia son DAGs. Ciclos = cambios en cascada, testing imposible, deploy acoplado. Si el módulo A importa B y B importa A, no hay dos módulos, hay uno mal partido.
- **Anti-Corruption Layer (ACL):** al integrar sistemas externos (legado, terceros), siempre una capa traductora. El modelo externo no contamina el interno. El ACL absorbe los cambios del proveedor; el dominio propio permanece estable.
- **Shared nothing como objetivo.** Estado compartido entre módulos/servicios = acoplamiento operativo. Cada módulo es dueño de sus datos; los demás leen por contrato (API/evento), no por acceso directo a la DB ajena.

---

## 3. DATOS — la decisión más irreversible

**El modelo de datos es la decisión de arquitectura con mayor inercia.** El código se reescribe en semanas; migrar un modelo de datos en producción con usuarios reales es una operación de meses.

- **Una sola fuente de verdad por fact.** Kleppmann: "if the same data is stored in several places, all copies need to be kept in sync." La sincronización siempre falla eventualmente. Elegir el sistema de registro (system of record) y derivar desde ahí.
- **Consistencia vs disponibilidad (CAP/PACELC):** bajo partición de red, elegís consistencia O disponibilidad. La mayoría de los sistemas necesitan CP (banco, inventario) o AP (redes sociales, analytics). No existe CA a escala distribuida. Elegir explícitamente y documentar qué invariante sacrificás.
- **Consistencia eventual es una promesa, no un default.** "Eventualmente consistente" requiere especificar: cuánto eventual, qué operaciones son compensables, quién detecta la inconsistencia. Sin esas respuestas no es diseño, es esperanza.
- **Event Sourcing/CQRS — cuándo sí:** audit trail completo es requisito · reconstrucción de estado es requisito · múltiples proyecciones del mismo dato · equipos distintos leen vs escriben. Cuándo no: CRUD simple · equipo pequeño · startup pre-PMF — el overhead operativo (snapshots, projectors, event versioning) supera el beneficio.
- **Sharding — cuando el monolith de DB duela:** antes de partir la DB, escalar vertical. Antes de sharding, réplicas de lectura para queries. El sharding introduce distribución en todos los joins que crucen el shard key — ese costo es permanente.
- **Idempotencia a nivel dato:** el constraint UNIQUE en la DB es el árbitro, no el `if` en la aplicación. El `if` puede tener race conditions; el constraint no.

---

## 4. COMUNICACIÓN ENTRE SISTEMAS

**Sincrónico acopa deployment; asincrónico acopa datos.** No hay opción sin tradeoff.

- **Sync cuando:** el caller necesita la respuesta para continuar · la latencia de la cola sería inaceptable · el contrato es simple y el receptor siempre disponible. HTTP/gRPC para llamadas internas síncronas; versionar desde el inicio.
- **Async cuando:** desacoplamiento de disponibilidad importa · el receptor puede estar caído sin bloquear al emisor · fanout natural (un evento, múltiples consumidores) · trabajo de larga duración.
- **Contratos de API:** versioná desde el primer día. Breaking change = versión nueva. Deprecación con período explícito. Consumer-Driven Contract Testing (Pact) cuando hay múltiples consumidores: el consumidor define qué necesita, el proveedor lo verifica en CI.
- **Idempotencia en mensajería:** exactly-once delivery es una ilusión a escala. Diseñar para at-least-once + consumidor idempotente. Cada mensaje lleva ID; el consumidor guarda IDs procesados o usa constraint de DB.
- **Retries con backoff exponencial + jitter + tope:** retry inmediato aumenta carga en el peor momento. Backoff exponencial con jitter distribuye la carga. Tope máximo para no hacer retry infinito (DoS a sí mismo).
- **Sagas para transacciones distribuidas (Richardson):** no hay transacciones ACID cross-servicios. Saga choreography (eventos) para flujos simples; saga orchestration (coordinador) para flujos complejos con compensaciones. Cada paso de saga tiene su compensación definida antes de implementar el paso.

---

## 5. ESCALABILIDAD Y DESEMPEÑO

**Escalar antes de medir es optimización prematura a nivel sistema.** El costo es deuda de complejidad.

- **Medir antes de decidir.** Datos reales de carga antes de cualquier decisión de escala: dónde está el cuello de botella HOY. Sin medición, la solución probable es la solución equivocada.
- **Escala vertical primero.** Más barato, más simple, sin cambios de arquitectura. Solo cuando la vertical duela, horizontal.
- **Statelessness como requisito para horizontal scaling.** Sesiones en DB/Redis. Archivos en object store. Contadores en DB atómica. Cada proceso es idéntico y reemplazable.
- **Invalidación de cache nombrada y quirúrgica.** Cache sin estrategia de invalidación explícita es bug de datos stale esperando. Cada mutación lista qué caches toca.
- **Back-pressure:** cuando el productor genera más rápido de lo que el consumidor procesa, señalizar hacia atrás (HTTP 429, cola con bound, circuit breaker). Sin back-pressure el sistema colapsa bajo carga.

---

## 6. RESILIENCIA

**Los fallos son la norma, no la excepción.** Diseñar para fallos desde el día uno.

- **Timeouts en todo.** Sin timeout, una dependencia lenta puede bloquear todos los threads del caller. El valor del timeout es una decisión de negocio, no un default del framework.
- **Circuit Breakers:** cuando un servicio remoto falla consistentemente, dejar de llamarlo temporalmente. Three states: closed (normal) · open (falla rápido) · half-open (prueba recuperación). Evita cascada de fallos.
- **Bulkheads:** aislar pools de recursos por criticidad. El pool de threads de pagos no debe ser consumido por analytics.
- **Blast radius mínimo:** diseño que hace explícito qué se rompe si X se rompe, y acota la respuesta. Microservicios con DB compartida no acotan el blast radius.
- **Degradación elegante:** el sistema bajo falla parcial sirve su función core degradada, no falla completamente. Feature flags para desactivar funcionalidad non-core bajo carga.
- **No single point of failure:** identificar SPOFs en el diagrama. Cada SPOF es riesgo de indisponibilidad total. Failover probado en producción — el failover que no se prueba falla cuando importa.
- **Idempotencia como requisito de resiliencia:** el retry automático es imposible si la operación no es idempotente.

---

## 7. EVOLVABILIDAD

**La arquitectura que "resiste el cambio" es arquitectura que ya llegó a su fin.** El objetivo es arquitectura que cambia barato.

- **Fitness functions (Building Evolutionary Architectures):** métricas ejecutables que verifican que la arquitectura mantiene sus propiedades con cada cambio. Ejemplos: test que verifica que el módulo A no importa B · análisis de dependencias en CI · test de contrato de API. La arquitectura se certifica por CI, no por inspección manual.
- **Strangler Fig para migraciones (Fowler):** reemplazar un sistema legado incrementalmente sin big-bang. El sistema nuevo convive con el viejo; el tráfico se mueve gradualmente; el viejo se estrangula. Jamás reescritura completa en paralelo que deja de integrarse.
- **Reversibilidad como criterio de diseño:** antes de cada decisión, "¿cómo la deshago si está mal?" Si la respuesta es "no puedo", es one-way → deliberar más.
- **Extensión por adición, no por modificación.** Nuevas funcionalidades en módulos nuevos, no en módulos ya estables.
- **Canary releases y feature flags:** desacoplar deploy de release. El código nuevo está en producción pero solo sirve al % definido del tráfico. Rollback sin revert de código.

---

## 8. SIMPLICIDAD Y MONOLITO-FIRST

**La complejidad accidental es el mayor costo oculto de arquitectura.**

- **Monolito modular first (Newman):** empezar con módulos bien delimitados dentro de un monolito. Los límites son conceptuales antes de ser físicos. Partir cuando los límites demostrados sean correctos Y el costo de acoplamiento supere el costo de distribución.
- **Las señales para partir un monolito:** necesidad de escala independiente por componente · equipos distintos que se bloquean mutuamente en deploy · diferentes requisitos de disponibilidad por componente. Ninguna de estas señales existe en un startup pre-escala.
- **Complejidad esencial vs accidental (Brooks):** la complejidad esencial es inherente al dominio. La accidental es la que los ingenieros introducen. Reducir la accidental sin piedad.
- **YAGNI a nivel sistema:** no construir la arquitectura para el millón de usuarios cuando hay 1000. Las arquitecturas construidas para el escenario hipotético pagan su costo operativo hoy con usuarios que pagan mañana (si llegan).
- **El monolito que escala:** Instagram con PostgreSQL a 1 TB; Shopify con monolito Rails a escala masiva. El ceiling del monolito bien estructurado es mucho más alto de lo que el folk-knowledge sugiere.

---

## 9. SEGURIDAD Y MULTITENANCY A NIVEL SISTEMA

**Los límites de seguridad son decisiones de arquitectura, no configuración.**

- **Trust boundaries explícitos en el diagrama:** cada sistema tiene un perímetro. Qué entra, qué sale, qué se verifica en el límite. Diagrama sin trust boundaries no es un diagrama de arquitectura segura.
- **Aislamiento de tenants por diseño:** Row-level security (PostgreSQL RLS) como default en schemas compartidos. Schemas separados por tenant para aislamiento más fuerte. DB separadas solo cuando el aislamiento es requisito legal o contractual.
- **Defense in depth a nivel sistema:** si la autenticación falla, la autorización debe resistir. Si la autorización falla, los logs deben detectar. Si los logs fallan, el rate limiting debe frenar. Capas independientes.
- **Secrets management como arquitectura:** los secretos no viven en la aplicación, viven en el secret manager. La rotación no requiere redeploy. Toda credencial tiene TTL.
- **Network segmentation:** los servicios internos no son accesibles desde internet. VPC, subnets privadas, bastión para acceso administrativo.
- **Audit log como requisito de arquitectura:** toda acción relevante queda en un log inmutable. Diseñarlo post-hecho es 5x más caro.

---

## 10. OBSERVABILIDAD

**No podés operar lo que no podés ver.**

- **Los tres pilares (logs · métricas · traces):** logs para eventos discretos; métricas para estado agregado en el tiempo; traces para latencia end-to-end a través de sistemas. Los tres son complementarios.
- **Observabilidad por diseño, no afterthought:** instrumentar al mismo tiempo que se construye. Un feature sin métricas es un feature que nadie sabe si funciona.
- **SLO/error budget (DORA/SRE):** definir el nivel de servicio como porcentaje de tiempo que el sistema cumple su objetivo. El error budget es lo que queda. Gastar el error budget deploya cambios riesgosos; cuando se agota, freeze de releases.
- **Structured logs:** JSON, siempre. Con request ID, user ID (anonimizado si PII), timestamp, severity, contexto relevante. Logs sin estructura son búsqueda de texto en un incidente a las 2am.
- **Alertas sobre síntomas, no causas:** alertar cuando el SLO está en riesgo (error rate >1%, latency p99 >500ms), no cuando la CPU está al 80%.
- **Tracing distribuido:** el trace ID viaja en headers. Permite reconstruir el camino completo de una request a través de todos los sistemas.

---

## 11. TELLS DE ARQUITECTURA OVER-ENGINEERED → CORRECCIÓN

| Tell | Por qué es problema | Corrección world-class |
|---|---|---|
| Microservicios desde el día 1 | 8 modos de fallo donde había 1; límites incorrectos hasta tener datos; deployment y observabilidad exponencialmente más complejos | Monolito modular; partir cuando los datos lo justifiquen |
| DB compartida entre "servicios" | Acoplamiento oculto en el schema; migración rompe otro servicio; los servicios son un monolito con overhead de red | Una DB por servicio O volver al monolito honesto |
| Message broker para todo por default | Complejidad operacional alta; debugging difícil; ordering guarantees complejas | Sync HTTP para el 80%; async solo cuando el desacoplamiento de disponibilidad lo justifica |
| Event sourcing en CRUD simple | Proyectores, snapshots, versioning, replay; overhead 10x sobre CRUD con auditoría simple | Append-only log de auditoría en Postgres; event sourcing solo cuando reconstrucción de estado es requisito real |
| GraphQL para API interna (1 cliente) | Overhead de schema, resolvers, N+1 por default; sin beneficio con 1 consumidor | REST simple o RPC; GraphQL para múltiples clientes con necesidades distintas |
| Kubernetes para un startup | Curva operacional masiva; recursos cognitivos del equipo pequeño consumidos en infra | PaaS hasta que el control fino del infra sea el cuello de botella |
| Colas para trabajo de 100ms | Overhead de dead-letter queues, reintentos, monitoreo mayor que el trabajo mismo | Inline o cron; cola cuando el throughput o el desacoplamiento lo justifican |
| Distributed monolith | El peor de ambos mundos: complejidad de microservicios sin independencia de deploy | Volver al monolito y limpiar los límites antes de partir |
| API versioning sin estrategia de sunset | Endpoints acumulados, cliente sin presión de migrar | Deprecation notices, sunset header, período de migración definido, telemetría de uso por versión |
| Sagas sin compensaciones definidas | Transacción distribuida sin rollback posible; estado inconsistente permanente | Cada paso tiene su compensación antes de implementar el paso; la compensación se prueba |
| Fault tolerance sin chaos testing | El failover que no se prueba falla en producción | Probar el failover antes de necesitarlo |
| Observabilidad como última tarea del sprint | Sistema invisible en producción; debugging ciego | Logs, métricas y health check como criterio de definition-of-done |
| Consistencia eventual sin especificar "cuánto eventual" | "Eventualmente" es un cheque en blanco; el negocio no puede tolerar inconsistencia indefinida | Especificar SLA de convergencia, mecanismo de detección y compensación |

---

## 12. EL SALTO A MÍTICO

Lo que separa una arquitectura buena de una atemporal no es complejidad — es claridad, reversibilidad y auto-documentación.

**La que se borra sola.** La arquitectura mítica desaparece del código; el negocio ocupa el primer plano. Los patrones son tan naturales que no hay que explicarlos en onboarding. Hohpe: el arquitecto es el ascensorista — traduce entre pisos sin que ningún piso sepa que el otro existe.

**La que escala con el equipo.** No con el tráfico — con el equipo. Un sistema que requiere héroes para operar es frágil. La arquitectura mítica permite que un ingeniero nuevo cambie un bounded context sin entender todos los demás.

**La reversible.** Cada decisión tiene su mecanismo de vuelta. Feature flags se pueden apagar. Migraciones tienen script de rollback. Servicios nuevos tienen strangler fig que puede invertirse.

**La que hace explícito lo implícito.** ADRs que registran no solo qué se decidió sino qué se descartó y por qué. Fitness functions que codifican en CI las invariantes arquitectónicas. Diagramas C4 en 4 niveles de zoom: contexto (qué hace y con quién) → contenedores (piezas desplegables) → componentes (qué hay dentro) → código (solo cuando es crítico).

**La que falla bien.** Degrada, no colapsa. El on-call sabe qué está roto antes de que lo reporten. El rollback es un flag, no un ritual de 2 horas.

**La que mide su propia salud.** SLOs definidos, error budget visible, deployment frequency medida. DORA metrics como espejo: si el lead time es mayor a 1 semana, la arquitectura está frenando el equipo. Las métricas DORA son fitness functions del sistema sociotécnico.

---

## 13. GATE DE REVISIÓN ARQUITECTÓNICA

Aplicar al revisar un diseño de sistema. Cada pregunta es PASS o FAIL. Score final /10.

| # | Pregunta | Peso |
|---|---|---|
| 1 | ¿Hay ADR para cada decisión de peso-sistema con opciones descartadas documentadas? | 1 |
| 2 | ¿Cada dato tiene una fuente de verdad única y nombrada? | 1 |
| 3 | ¿Los bounded contexts están explícitos y con límites respetados (sin DB compartida entre contextos)? | 1 |
| 4 | ¿La complejidad del sistema está justificada por el tamaño del equipo y el tráfico real (no hipotético)? | 1 |
| 5 | ¿Toda operación que cruza un límite de sistema tiene idempotencia documentada? | 1 |
| 6 | ¿El sistema tiene timeouts, circuit breakers y degradación elegante definidos y probados? | 1 |
| 7 | ¿La observabilidad (logs estructurados · métricas · traces · SLO) es parte del diseño desde el inicio? | 1 |
| 8 | ¿Cada decisión irreversible (one-way door) fue marcada como tal y deliberada explícitamente? | 1 |
| 9 | ¿El aislamiento de tenants y los trust boundaries están en el diagrama de arquitectura? | 0.5 |
| 10 | ¿Hay fitness functions automatizadas que verifiquen las invariantes arquitectónicas en CI? | 0.5 |

**PASS >= 8.0 · CONDICIONAL 6.0-7.9 · FAIL < 6.0**

FAIL = no proceder a implementación; revisar ítems rojos primero.
CONDICIONAL = proceder con ítems como deuda técnica de arquitectura con fecha de resolución.
