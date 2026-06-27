# PROMPT CRAFT · esencia al 100% en TODO lo generativo
> 2026-06-12 · orden Ale: "que genere siempre buenos prompts para que grok-cli capture
> la esencia al 100% sin errores — y eso aplica para todo". Método universal para
> video, imagen, código creativo y copy generativo. Lo consume P4-B4, el 6H (video),
> el 6I (imagen estática) y cualquier invocación de grok-cli / nano-banana / mk-image.

## A) Framework Mental

**La esencia se EXTRAE antes de promptear — jamás se "tiene en la cabeza".** El error
raíz de los prompts mediocres: el que promptea cree saber qué quiere, pero nunca lo
listó → el prompt omite la mitad y el modelo rellena con su prior (= look IA genérico).

**EL MÉTODO: el prompt es un CONTRATO.** Primero la LISTA DE ESENCIA (los must-haves
numerados del brief); después el prompt, donde CADA must-have tiene su cláusula
verificable; al final el GATE, que verifica cláusula por cláusula contra el output.
Sin lista no hay contrato; sin contrato no hay 100%.

**Lenguaje FÍSICO, jamás adjetivos de resultado.** "Cinematic", "beautiful", "premium",
"high quality", "8k", "trending" = pedirle el postre sin darle la receta — el modelo
los mapea a SU promedio estadístico (= slop). Lo que sí funciona: describir la FÍSICA
que produce el resultado — luz (fuente, dirección, calidad, temperatura), lente
(focal, apertura, distancia), material (cómo responde a la luz), composición (dónde
está cada cosa y por qué), movimiento (motivado por qué).

**El espacio negativo es parte de la esencia:** lo que NO debe aparecer se declara
explícito (negativos anti-slop + vetos del proyecto). Un prompt sin prohibiciones
deja la puerta abierta al prior.

## B) Algoritmo de Ejecución

### B1. Extracción de esencia (SIEMPRE primero · 2 minutos)

Del brief/master/pedido, listar numerado:
```
ESENCIA · [pieza] · [fecha]
1. SUJETO: qué es, exactamente (objeto/escena/concepto — sin ambigüedad)
2. INTENCIÓN: qué debe SENTIR quien lo ve, en 1 frase (la emoción es un must-have)
3. SPECS FÍSICAS: luz · paleta EXACTA del DNA (hex/tokens literales) · materiales ·
   composición · encuadre/lente · movimiento (si video)
4. MARCA/DNA: qué elementos de identidad DEBEN estar (logo N, tipografía, restraint)
5. PROHIBICIONES: vetos del proyecto (orb radial, rojo en comida...) + negativos
   anti-slop del medio
6. CONTEXTO DE USO: dónde vive (splash mobile 9:16 · og-image 1200×630 · ad 4:5) —
   el aspect ratio y la legibilidad a tamaño real SON esencia
```
Test: si un tercero puede generar la pieza correcta SOLO con esta lista → está completa.

### B2. Construcción del prompt por medio

**VIDEO (grok-cli · mk-video):** estructura y rúbrica completas en
`cinematography-playbook.md` (§prompting · §12 rúbrica · §13 anti-tells). Cláusulas:
plano a plano — composición + lente/DOF + movimiento MOTIVADO + luz con fuente +
grade + continuidad. Gate: **6H**.

**IMAGEN ESTÁTICA (grok-cli image · nano-banana · mk-image):** orden de cláusulas:
1. Sujeto + acción/estado (1 frase concreta)
2. Entorno + luz física (fuente, dirección, calidad, hora)
3. Cámara: focal + apertura + ángulo + distancia (la imagen "de marca" tiene lente)
4. Material/estilo: superficie, paleta DNA con valores literales, nivel de detalle
5. Composición: qué va dónde, espacio negativo, jerarquía
6. NEGATIVOS: watermark, texto ilegible, manos deformes, simetría plástica,
   saturación uniforme, bokeh falso + los vetos del proyecto
Gate: **6I** (essence check item por item).

**CÓDIGO CREATIVO (shaders · motion):** constraints-first — presupuesto (60fps gama
baja) + plataforma (Skia y-DOWN, worklet-safe) + el FENÓMENO físico deseado ("la luz
atraviesa y refracta en el borde", no "efecto glass"). Gate: 6G + perf numbers.

**COPY GENERATIVO:** register del producto (neutro-tuteo) + prohibiciones (cero
emojis, cero em-dash si aplica impeccable) + el JOB del texto (qué debe lograr en
quien lee) + largo exacto. Gate: /matu copy.

### B3. PRE-FLIGHT (antes de gastar la generación · 30 segundos)

```
□ ¿CADA item de la ESENCIA tiene su cláusula en el prompt? (mapear 1→1, no de memoria)
□ ¿Cero adjetivos de resultado? (cinematic/beautiful/premium/8k/trending = reemplazar por física)
□ ¿Paleta/DNA con valores LITERALES (hex, nombre de fuente), no "los colores de la marca"?
□ ¿Negativos declarados (anti-slop del medio + vetos del proyecto)?
□ ¿Aspect ratio + contexto de uso especificados?
□ ¿Ambigüedades muertas? (toda palabra que admite 2 lecturas, reescrita)
```
Un check en rojo → arreglar el prompt ANTES de generar. La generación es lo caro;
el pre-flight es gratis.

### B4. Iteración post-gate (jamás regenerar a ciegas)

El gate (6H/6I/6G) devuelve QUÉ cláusula falló → se reescribe ESA cláusula (más
física, más literal, o movida antes en el prompt — lo primero pesa más) → regenerar →
re-gate. Cambiar todo el prompt por una falla puntual = perder lo que SÍ funcionaba.
Max 5 rounds → escalar con la tabla de cláusulas en rojo.

## C) Reglas de Oro

- JAMÁS generar sin lista de esencia escrita. La lista ES el contrato.
- Cada must-have → una cláusula verificable. Lo no escrito no existe para el modelo.
- Física, no adjetivos de resultado. Valores literales, no referencias vagas.
- Negativos siempre (anti-slop del medio + vetos del proyecto).
- Pre-flight antes de cada generación. Iterar la cláusula, no el prompt entero.
- Todo output generativo pasa su gate: video→6H · imagen→6I · código→6G · copy→/matu.
  Sin gate no hay "100% sin errores" — hay esperanza.
- El prompt exitoso se CACHEA junto al asset (mismo dir, `.prompt.md`) — re-generar
  una variante parte del contrato ganador, no de cero.

## D) Desafío resuelto — prompt grok-cli para el splash (caso real pendiente)

**ESENCIA (del splash-MASTER aprobado):** 1. SUJETO: la marca N liquid-glass con
núcleo emergiendo de superficie líquida oscura. 2. INTENCIÓN: calma premium con un
solo momento de asombro (el wow del flujo onboarding). 3. FÍSICA: luz key superior
fría rebotando en el glass (transmisión + refracción en bordes), fondo #0F0F10,
acento brand #059669 SOLO en el núcleo, cámara 85mm f/2 dolly-in lento MOTIVADO por
la emergencia, ACES filmic. 4. DNA: marca N exacta del logo.html — no "una N". 5.
PROHIBICIONES: cero texto en pantalla, cero partículas genéricas, cero lens-flare
chillón, cero loop con salto (§13). 6. USO: 9:16 mobile, 3-5s, legible como splash.
**PROMPT (cláusulas 1→1):** cada número de arriba se vuelve una oración física en
ese orden. **PRE-FLIGHT:** 6/6 ✓. **GATE:** 6H puntúa los 10 ejes; si "movimiento
motivado" <8 → se reescribe SOLO la cláusula de cámara (ej: "dolly-in 10% acelerando
al emerger el núcleo") → re-render → re-gate. Así "captura la esencia al 100%" deja
de ser deseo y es un loop verificable.

---

## grok-cli — mastery (el brazo generativo · pipeline tier Mithos)

Capacidades (verificado SKILL grok-cli): `image` (hasta 10 variantes · aspect libre · 1k · `--output-dir` batch) · `image-edit` (compositing hasta 3 fuentes · paths/URL/data-URI) · `video` (text+image+hasta 7 `--reference-image` · `--duration 8` max · 720p) · `video-edit` (re-estiliza · NO cambia duración/aspect) · `video-extend` (alarga · **SOLO `--video-url`, falla silencioso con `--video` local**) · `tts`/`stt` (diarización) · `search` (X/Twitter para tendencias en vivo).

**Pipeline 5 fases (nunca generar 1):**
1. **Sweep:** `grok-cli image --count 8 --aspect-ratio 1:1 --resolution 1k --output-dir ./sweep/` — el asset final es el mejor FRAME de un barrido, no "el mejor prompt".
2. **Contact-sheet** (ffmpeg montage) → elegir 1 candidato.
3. **Refinar:** `image-edit --image best.png --image referencia-real.jpg` — anclar material/luz de una referencia real (mata la alucinación de color).
4. **Animar:** `video --image refined.png --duration 8 --aspect-ratio 9:16` con prompt de FÍSICA (rotación/respiración/cámara), no apariencia.
5. **Extender** (si hace falta): subir a URL → `video-extend --video-url …`.

**Flags no obvios:** `--reference-image` (hasta 7) = paleta de materiales sin mezclar la composición · `--no-web-search` en `chat` para prompt generativo puro · `--model` es por-comando (imagen ≠ chat, no hay global). **Forma-contenedor primero** (rect/circle/panel/float = arquitectura semántica). Ancla siempre con `--image` cuando exista un referente real. Todo crudo de IA pasa el post-proceso de 3 pasos (grade ACES · temporal denoise · frame-blend) — ver codex Parte VI.
