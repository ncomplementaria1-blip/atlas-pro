# MÓDULO TRANSVERSAL · LLM ENGINEERING DE PRODUCTO — versión profunda
> Transferencia Fable 5 · 2026-06-11 · se carga cuando la tarea toca superficie IA del
> producto (el asistente chat · food-vision · un canal de mensajería coach · biblioteca · cualquier feature
> que llame a un modelo), además del pilar. La cara DEFENSIVA (injection, allowlist,
> PII) vive en `seguridad.md` B4 — este módulo es la INGENIERÍA: cómo se construye.
>
> **SCOPE: el MÉTODO es UNIVERSAL.** Los ejemplos (el asistente, platos chilenos, un canal de mensajería)
> son material didáctico de el proyecto — en otro proyecto: mismo método, dominio del
> proyecto activo. Scope Discipline manda.

## A) Framework Mental

**El LLM en producto es un COMPONENTE NO DETERMINISTA — se diseña como un borde.**
Igual que un webhook o una API externa: contrato de entrada/salida, validación,
timeout, fallback. La "magia" es experiencia del usuario; para el ingeniero es un
proveedor con SLA difuso que a veces miente con confianza.

**El prompt es CÓDIGO:** se versiona en el repo, se revisa, y se testea con eval-set.
Cambiar un prompt sin correr evals = deployar sin tests. El prompt que "funciona en mi
chat" y el que funciona sobre 20 casos reales son cosas distintas.

**Separación de autoridad (ya canon en food-vision):** el LLM PROPONE/ESTIMA/REDACTA;
el código VALIDA/DECIDE/CALCULA. El dato crítico jamás lo inventa el modelo — el LLM
estima gramos, la DB calcula calorías. Este patrón escala a todo: el LLM clasifica el
intent, el código decide qué acción ejecutar; el LLM redacta, el código decide a quién
enviar.

**Modelo por tarea, medido:** el modelo correcto para una tarea de producto es el MÁS
BARATO que pasa el eval-set — no el más nuevo ni el más grande. Clasificar intent no
necesita el modelo de la conversación sensible. Se decide con datos (D3), no con fe.

**La calidad del contexto ES la calidad de la respuesta:** contexto con ruido degrada
aunque "quepa". Al modelo entra lo que CAMBIA la respuesta; lo demás es costo y
distracción.

## B) Algoritmos de Ejecución

### B1. Toda feature LLM nueva (el pipeline completo, en orden)

1. **Contrato de salida PRIMERO:** schema zod exacto de lo que el código necesita.
   Diseñar el prompt antes que el contrato es construir el enchufe antes que el aparato.
2. **Prompt estructurado:** rol e identidad → reglas duras (qué jamás hace) → contexto
   del dominio → few-shots de los casos DIFÍCILES → formato de salida con el schema →
   user content al final, delimitado como datos (seguridad.md B4).
3. **Validación + retry inteligente:** parsear contra el schema; si falla → UN retry
   pasándole el error concreto ("tu salida no parseó: <error>") — el modelo corrige
   bien con feedback específico. Segundo fallo → fallback, jamás loop.
4. **Fallback honesto:** cada llamada tiene su plan B definido ANTES de shippear:
   re-preguntar al usuario ("no pude identificar el plato, ¿me dices qué es?"),
   degradar a flujo manual, o cola para reintento. El usuario nunca queda en un
   callejón sin salida.
5. **Eval-set antes de shippear:** 10-20 casos reales (los difíciles, no los demo) con
   resultado esperado. Pass = contrato válido + valores correctos/plausibles.
6. **Telemetría desde el día 1:** loggear input/output (sin PII — ids opacos) +
   latencia + costo por llamada. Sin esto no hay mejora posible, solo anécdotas.

### B2. System prompt de producto (el de el asistente como arquetipo)

Orden interno (lo ESTABLE primero — habilita prompt caching):
1. **Identidad y límites sensibles:** quién es, qué NO hace (no diagnostica, no
   prescribe, deriva a profesional ante señales de riesgo — datos sensibles incluido), tono
   (copy del producto: neutro con tuteo).
2. **Reglas duras enumeradas** (pocas y absolutas — 20 reglas se diluyen, 7 se cumplen).
3. **Few-shots de los momentos difíciles:** el rechazo elegante (pedido fuera de
   límites), la derivación con calidez, la corrección sin culpa. Los casos fáciles no
   necesitan ejemplo.
4. **Herramientas/acciones disponibles** con su allowlist (seguridad.md).
5. **Al final, lo dinámico:** contexto del usuario (lo MÍNIMO que cambia la respuesta:
   objetivos, restricciones, último contexto relevante — no el perfil entero).
Versionado: `prompts/el asistente-system.v3.ts` en el repo — el prompt activo es código
desplegado, no un string que alguien edita en producción.

### B3. Few-shot engineering

- Los ejemplos van donde el modelo FALLA sin ellos — se descubren con el eval-set, no
  se inventan. 2-5 quirúrgicos > 20 genéricos (más ejemplos = más costo por llamada y
  más dilución).
- Cada ejemplo muestra el formato EXACTO de salida (el modelo imita formato más fuerte
  de lo que obedece instrucciones de formato).
- Incluir SIEMPRE un ejemplo de caso negativo: qué responder cuando no sabe / el input
  es inválido — sin él, el modelo inventa antes que admitir.

### B4. Contexto y memoria (cross-canal app↔un canal de mensajería ya existente)

- Criterio de admisión al contexto: ¿este dato CAMBIA la respuesta a ESTE mensaje?
  No → fuera.
- Historial: ventana reciente completa + resumen comprimido de lo viejo (el resumen lo
  genera un modelo barato, offline del request).
- La memoria de largo plazo vive en la DB estructurada (preferencias, restricciones,
  hitos) — no en transcripts infinitos re-inyectados. El transcript es evidencia; la
  memoria es dato curado.

### B5. Prompt caching estratégico

- Estructura del prompt = estable→volátil: system + few-shots (cacheable, cambia por
  deploy) | contexto de usuario (semi-estable, cambia por sesión) | mensaje (único).
- Romper el orden rompe el cache: un timestamp al INICIO del system prompt invalida
  todo lo que viene después — lo volátil va al final, siempre.
- Medir hit-rate de cache en la telemetría (B1.6): un hit-rate bajo en un endpoint de
  volumen es plata y latencia regaladas.

### B6. Evals (el instrumento de calidad — gemelo del test post-bug)

- **Golden set:** casos reales con salida esperada (exacta para clasificación; por
  contrato+rangos para estimación; por rúbrica simple para conversación).
- **Cuándo corre:** SIEMPRE antes de cambiar prompt, modelo o temperatura. Es el
  typecheck de la capa IA.
- **Crece con producción:** cada fallo real de prod entra al set (misma regla que
  testing-estrategia B4 — el eval-set es el mapa de las heridas reales de la capa IA).
- **Rúbrica de conversación (el asistente):** pass/fail por dimensiones binarias — ¿respetó
  límites sensibles? ¿tono correcto? ¿accionable? ¿largo apropiado? — evaluables por un
  modelo barato como juez + spot-check humano de Ale en los borde.

### B7. Latencia y UX de la espera

- Chat → streaming SIEMPRE (la percepción de velocidad es el primer token, no el último).
- Análisis (foto) → estado de progreso honesto + resultado de una vez (streamear un
  JSON a medias no sirve a nadie).
- Timeout definido con fallback (B1.4) — la espera infinita es el peor estado de UX.
- Lo diferible se difiere: el resumen de memoria, la clasificación para analytics —
  nada de eso bloquea la respuesta al usuario.

## C) Reglas de Oro (inquebrantables)

- Contrato de salida antes que prompt. Siempre.
- El prompt es código: versionado en repo + eval-set corrido antes de cada cambio.
- LLM propone, código decide. El dato crítico jamás lo inventa el modelo.
- UN retry con el error como feedback; después fallback honesto. Jamás loop de retries.
- Todo fallo de producción entra al eval-set (la suite de la capa IA crece donde duele).
- PII mínima al modelo; telemetría sin PII; lo volátil al final del prompt (cache).
- El modelo por tarea se elige con eval-set, del más barato hacia arriba — medido,
  jamás asumido.
- Streaming en chat; progreso honesto en análisis; timeout con plan B en todo.
- La cara defensiva (injection, allowlist, fuga) es OBLIGATORIA junto a este módulo:
  seguridad.md B4.

## D) Desafíos de Sincronización (resueltos a fondo)

### D1. Food-vision end-to-end con el método (el arquetipo completo)

**Contrato:** `{ alimentos: [{ nombre: string, gramos_est: number, confianza: 0-1 }],
no_identificado: boolean }` — zod, estricto. **Prompt:** rol (nutricionista visual) +
regla dura (estimas gramos, JAMÁS calorías — eso lo hace la DB) + few-shots de platos
chilenos difíciles donde los modelos fallan (cazuela: ¿se cuenta el caldo?, completo:
capas ocultas, porotos granados: densidad engañosa) + ejemplo negativo (foto borrosa →
`no_identificado: true`, no inventar). **Validación:** gramos 1-2000 por item, nombres
contra el catálogo (pg_trgm fuzzy — match dudoso = pedir confirmación de 1 toque al
usuario, UX ya diseñada). **Fallback:** `no_identificado` → "¿me dices qué es?" con
input de texto prellenado. **Eval-set:** 15 fotos reales etiquetadas (las 5 que
fallaron en desarrollo + 10 representativas); pass = items correctos ±20% gramos.
**Telemetría:** confianza promedio, tasa de corrección manual del usuario (LA métrica
de calidad real — si el usuario corrige mucho, el eval-set miente).

### D2. Clasificador de intent para un canal de mensajería (lo barato bien hecho)

**Problema:** cada mensaje entrante necesita ruta (registrar comida / pregunta /
saludo / fuera de alcance) ANTES de decidir qué modelo responde. **Diseño:** modelo
chico y rápido, salida enum estricta `{ intent: "registro"|"consulta"|"social"|
"fuera_alcance", confianza: 0-1 }`, confianza < umbral → tratar como "consulta"
(el default seguro: responder conversacionalmente nunca rompe nada; registrar mal sí).
**Por qué un clasificador aparte:** enrutar con el modelo grande es pagar conversación
sensible por decidir si "hola" es un saludo — la separación baja latencia y permite que
cada ruta tenga SU prompt afinado. **Eval:** 30 mensajes reales anonimizados,
clasificación exacta esperada; el clasificador se acepta cuando acierta los 30 (es
una tarea cerrada — acá sí se exige perfección, no plausibilidad).

### D3. Receta: elegir modelo para una tarea nueva (verificado, no asumido)

(1) Definir contrato + eval-set ANTES de tocar modelos (si no, el demo del modelo
grande te seduce). (2) Probar del más barato hacia arriba: ¿pasa el eval? → ese es.
(3) Documentar la decisión CON los números (tasa de pass, latencia, costo por llamada)
— fechada, porque los modelos y precios cambian (P5: TTL del dato = semanas/meses).
(4) Re-evaluar solo con trigger real: falla en prod que el eval no cubría, o cambio
de generación de modelos. **Anti-patrón que esta receta mata:** "usemos el mejor
modelo para todo por si acaso" — es la versión IA de comprar un camión para ir al
almacén; y su gemelo "el barato sirve para todo", que se descubre tarde con usuarios
reales. Ninguna de las dos es ingeniería: medir es ingeniería.

## Cierre del módulo

La capa IA de un producto se gana o se pierde en lo invisible: contratos, evals,
fallbacks, telemetría. El usuario ve "el asistente me entiende"; abajo hay un borde no
determinista tratado con la misma disciplina que un webhook de pagos. Esa disciplina
es exactamente lo transferido acá — y con el eval-set creciendo donde duele (B6),
esta capa mejora sola con cada semana de producción.
