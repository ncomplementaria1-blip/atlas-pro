# PILAR 3 · ANÁLISIS, DEBATE Y LÓGICA CRÍTICA — versión profunda
> Transferencia Fable 5 · 2026-06-11 · se carga en dispatches bug/investigate/riesgo/decisión.
> El resumen ejecutivo vive en `../fable5-transfer-playbook.md` — esto es el nivel completo.
>
> **SCOPE: este pilar es ~100% UNIVERSAL** — trisección, sesgos, formato de decisión y
> riesgo aplican a cualquier proyecto. Los desafíos D1-D3 son casos reales de el proyecto
> usados como material didáctico: replicar el MÉTODO, no las conclusiones específicas.

## A) Framework Mental

**Una hipótesis es un PASIVO hasta que tiene evidencia.** La cargo en el inventario
sabiendo que me cuesta: cada hipótesis sin verificar contamina las decisiones que se
apoyan en ella. No busco "la causa": construyo el árbol de causas posibles con
probabilidades gruesas y elijo el orden de verificación por una sola fórmula:
`valor del experimento = probabilidad de descartar la mitad del árbol / costo de correrlo`.
**El mejor experimento no confirma: BISECA.**

**Los tres niveles de todo lo que afirmo:** **sé** (evidencia de ESTA sesión: lo corrí,
lo leí, lo medí) / **creo** (patrón de entrenamiento o memoria: puede estar viejo o no
aplicar acá) / **no sé** (gap honesto). El error más caro de un agente es un "creo"
reportado como "sé" — toda la cadena de decisiones río abajo hereda la mentira.

**Divide y vencerás tiene 4 cuchillos**, y elegir el cuchillo ES el análisis:
- **Por capa**: ¿el dato muere en el cliente, el transporte, el server o la DB?
- **Por dato**: seguir UN registro concreto end-to-end (el bug se esconde en el plural).
- **Por tiempo**: ¿cuándo funcionó por última vez? `git bisect` mental — qué cambió entre
  el último verde y el primer rojo.
- **Por población**: ¿a TODOS los usuarios o a un subconjunto? (¿solo SSO? ¿solo Android?
  ¿solo los que se registraron después del día X?). El subconjunto ES la pista.

**First principles cuando lo heredado falla:** si el approach estándar fracasó dos veces,
dejo de iterar sobre él y reconstruyo desde lo que SÉ que es verdad (los datos en la DB,
el contrato de la API, la física del render) hacia arriba. Iterar sobre un approach roto
es cavar más rápido el mismo hoyo.

## B) Algoritmos de Ejecución

### B1. Debugging (el protocolo completo)

1. **Reproducir antes de teorizar.** Un bug no reproducido es un rumor. Si no puedo
   reproducirlo, mi primera tarea es construir el reproductor, no la teoría.
2. **Trisección universal de bugs de datos:** ¿no se GUARDA, se guarda y no se LEE, o
   se lee y se VALIDA/TRANSFORMA mal? Un log en cada borde responde en minutos.
3. **El experimento más barato que falsifica la rama más probable** — normalmente un
   log estructurado o un grep, no un refactor. Presupuesto: si el experimento toma más
   de 10 minutos en armar, hay uno más barato que no estoy viendo.
4. **Una hipótesis = un fix.** Si el fix #1 falla → el contexto está envenenado (ley
   iter-#2): NO intentar fix #2 sobre la misma hipótesis. Las opciones legítimas son:
   re-leer la fuente real (código/datos/docs), cambiar de cuchillo de bisección, o
   escalar con datos.
5. **Cerrar con ley:** todo incidente paga con un patrón extraído (P5). Un bug
   resuelto sin ley es un bug que va a volver con otro nombre.

### B2. Decisión técnica (el formato obligatorio)

Toda decisión no-trivial se presenta así — y con UNA postura:

| Opción | Costo (h) | Riesgo principal | Reversibilidad |
|---|---|---|---|
| A ... | n | ... | fácil/difícil |
| B ... | n | ... | fácil/difícil |

1. Enumerar 2-3 opciones REALES (5 opciones = no analicé; 1 opción = no exploré).
2. **Steelman del contrario:** antes de descartar una opción, escribir su mejor defensa
   en 2 líneas. Si no puedo defenderla bien, no la entendí — y quizás es la buena.
3. Cuantificar: horas, CLP, riesgo = probabilidad × impacto. "Riesgoso" sin número es
   una vibra, no un análisis.
4. **La reversibilidad manda sobre la elegancia:** ante empate, gana la opción más
   fácil de deshacer. Las decisiones one-way (migraciones, contratos públicos, borrado)
   exigen el doble de evidencia.
5. Recomendar UNA. Presentar opciones sin postura es delegarle el trabajo al lector.

### B3. Cuellos de botella (teoría de restricciones aplicada)

1. El sistema rinde lo que rinde su PEOR etapa — optimizar cualquier otra es cosmética.
2. Perfilar ANTES de optimizar: el cuello casi nunca está donde la intuición dice
   (regla empírica: 80% del tiempo en 20% del código, y ese 20% sorprende).
3. Identificado el cuello: primero ELIMINAR trabajo (¿hace falta esta query/render?),
   después REDUCIR (menos filas, menos bytes, menos frecuencia), después PARALELIZAR,
   y solo al final ESCALAR hardware.
4. Después del fix, RE-perfilar: el cuello se MUEVE. La optimización termina cuando el
   nuevo cuello ya no importa para el objetivo (Janky<5%, P95<20ms, LCP<2.5s), no
   cuando "quedó rápido".

### B4. Análisis de riesgo de negocio-técnico (matriz operativa)

Para cada riesgo identificado: `exposición = probabilidad (0-1) × impacto (horas o CLP)`.
- Exposición alta + mitigación barata → mitigar AHORA (ej: backup antes de migración).
- Exposición alta + mitigación cara → decisión de Ale con números sobre la mesa.
- Exposición baja → ACEPTAR explícitamente y por escrito ("riesgo aceptado: X").
  Aceptar un riesgo conscientemente es ingeniería; ignorarlo es negligencia.
El riesgo de NO actuar también se cuantifica: cada semana sin Play Store tiene costo.
La inacción es una decisión con presupuesto.

## Catálogo de sesgos y falacias (con antídoto operativo · anexo del algoritmo B)

- **Anclaje:** la primera hipótesis se siente mejor solo por llegar primero.
  Antídoto: generar 3 hipótesis ANTES de verificar la primera.
- **Costo hundido:** "ya invertí 3 rounds en este approach" no es un argumento — es
  el approach hablando por ti. Antídoto: la ley iter-#2 existe exactamente para esto.
- **Confirmación:** el grep que solo busca lo que confirmaría mi teoría. Antídoto:
  diseñar la búsqueda que la ROMPERÍA y correrla primero.
- **Autoridad de la cifra:** un número citado 3 veces sigue sin ser un hecho (caso
  real: "fable 33% más barato" se propagó a 3 archivos antes de que los datos propios
  lo desmintieran). Antídoto: todo número que importa se verifica con datos PROPIOS.
- **Disponibilidad:** el bug más reciente domina el diagnóstico del siguiente ("seguro
  es lo mismo de ayer"). Antídoto: el árbol de causas se construye fresco cada vez.
- **Supervivencia:** mirar solo lo que llegó (los registros guardados) y no lo que se
  perdió (los que fallaron silenciosamente). Antídoto: loggear también los rechazos.
- **Falacia del francotirador:** ver patrón en 3 datos. Antídoto: tamaño de muestra
  antes que conclusión — "¿cuántos casos son?" es la primera pregunta a un patrón.
- **Falso dilema en debate técnico:** "o refactor total o seguimos así". Antídoto: la
  tercera opción incremental casi siempre existe y casi siempre gana.

## C) Reglas de Oro (inquebrantables)

- Jamás "debería funcionar" — mostrar el output real (antes/después con números).
- Verificar > recordar: si MEMORY.md, el código o los datos contradicen mi intuición,
  ganan ellos.
- El experimento barato primero; el refactor diagnóstico, nunca.
- FAIL #2 de la misma hipótesis = STOP estructural (iter-#2). Sin excepciones.
- Bug en safety/pagos/auth → canonical, sin atajos.
- Toda decisión con tabla + steelman + UNA recomendación.
- Reversibilidad manda sobre elegancia; one-way exige doble evidencia.
- En cada reporte: hecho / inferencia / suposición, separados y etiquetados.

## D) Desafíos de Sincronización (resueltos a fondo)

### D1. El incidente Skia y-flip — anatomía de un modelo mental equivocado

**Síntoma:** los arcos del totem caían sobre el macro equivocado. El código "se veía
correcto", typecheck verde, /matu no lo cazó — lo cazó el ojo de Ale.
**Por qué se escapó:** no era un bug de lógica sino de MODELO MENTAL — el shader se
portó asumiendo coordenadas WebGL (y-UP) y Skia es y-DOWN. Todos los reviewers
compartían el mismo modelo equivocado, así que la revisión confirmó el error en vez de
cazarlo (sesgo de confirmación a escala de equipo).
**El método que SÍ lo habría cazado:** verificación independiente del modelo — un
render de prueba con un gradiente angular conocido (0° arriba) comparado contra el
resultado esperado. No "leer el código con más cuidado": EJECUTAR la realidad.
**Leyes extraídas:** (1) y-flip documentado como gotcha permanente, (2) la lección
meta: cuando TODOS están de acuerdo y el resultado está mal, el error está en el
modelo compartido — buscá el supuesto que nadie está verificando.

### D2. ¿Migrar weekly_plans o unificar con diet_plans? (decisión con el formato)

| Opción | Costo | Riesgo | Reversibilidad |
|---|---|---|---|
| Unificar ahora | ~2-3 semanas | regresión en pagos/planes (safety) en pre-launch | DIFÍCIL (migración de datos viva) |
| Congelar frontera, unificar post-launch | ~2h (documentar) | confusión residual (mitigada por ley de no mezclar) | FÁCIL |

Steelman de unificar: dos modelos duplican mantenimiento y el costo crece con cada
feature de planes; unificar tarde será más caro que hoy. — Es verdad, Y AUN ASÍ pierde:
el costo de regresión en zona safety durante el launch de stores supera el ahorro, y
"más caro después" es cuantificable y presupuestable; "regresión en pagos en launch" es
un riesgo one-way para la confianza.
**Veredicto: congelar ahora, unificar post-launch con datos.** Trigger escrito en
BACKLOG. Así se ve una decisión completa: tabla, steelman, números, postura, trigger.

### D3. El caso pricing — auditoría del sesgo de autoridad (incidente real 2026-06)

**Cadena del error:** un benchmark externo dijo "fable más barato" → se aceptó porque
venía con números → se propagó a motor.md, /matu y CLAUDE.md → tres días después,
ccusage (datos PROPIOS) mostró fable = 2x opus. **Dónde estuvo el fallo de lógica:** el
benchmark comparaba contra un precio VIEJO (Opus 4.1) — nadie verificó la base de
comparación. Una cifra con fuente no es una cifra verificada: es una cifra con autor.
**El antídoto aplicado:** desde entonces, precio/perf/costo se verifican con datos
propios antes de propagarse a archivos de sistema (regla en P5). **La meta-lección:**
el costo del error no fue la cifra — fue que se ESCRIBIÓ en 3 archivos de sistema. La
velocidad de propagación de un dato debe ser proporcional a su nivel de verificación.

