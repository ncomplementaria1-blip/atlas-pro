# Codex Universal de Craft — la vara de calidad de ATLAS (project-neutral)

> **Qué es:** la capa BASE de criterio world-class de ATLAS. Project-neutral: ninguna marca, ningún color, ningún producto. Destilado de 20+ design systems tier-1 (Apple, Stripe, Linear, Vercel, Figma, Ferrari, Tesla, Coinbase, Revolut, Cohere, ElevenLabs, x.ai, Raycast, Superhuman, Notion…), reportes deep-research (R3F cinemática · motion RN · splash/onboarding), transcripts de referentes (Candillon, Freya, Emil, Rauno, Cole Medin, Anthropic AppliedAI), y estudio de short-form/generativo. Fecha de corte: 2026-06.
>
> **Cómo se usa:** ATLAS lo carga como la vara de 10/10 para CUALQUIER proyecto (configurado o no). El criterio de un proyecto = **este codex (base) + su overlay** (`brand-context.md` del proyecto = DNA, paleta, voz, restricciones). El overlay NUNCA contradice el codex; lo especializa. El overlay del proyecto (ejemplo) es `worldclass-craft.md` + `projects/<tu-proyecto>/brand-context.md`.
>
> **Vara vs motor:** este codex es la VARA (qué se ve 10/10 · evaluación/filtro). Para GENERAR diseño impactante (cómo inventar un concepto de agencia world-class) su complemento es `creative-direction-playbook.md` — el MOTOR generativo. ATLAS no es solo filtro: en modo `design` y en el Creative Spin usa los dos juntos (codex = piso de calidad · playbook = alcance creativo).
>
> **Relación con los playbooks especializados** (cargar el que aplique a la tarea, todos en `~/.claude/skills/atlas/`): `skia-sksl-playbook.md` (shaders Skia RN) · `motion-playbook.md` (math+taste de motion) · `gesture-choreography-playbook.md` (física del gesto) · `dataviz-safe-para-datos-sensibles.md` (gauges/rings) · `rive-adoption.md` · `haptics-playbook.md` · `perf-profiling-playbook.md` · `newarch-gotchas.md` · `cinematography-playbook.md` (director de foto para VIDEO) · `prompt-craft-playbook.md` (esencia→cláusulas para imagen generativa) · `creative-direction-playbook.md` (MOTOR generativo de concepto) · `graphic-design-playbook.md` (DISCIPLINA GRÁFICA: identidad de marca/logo, editorial/print, iconografía, ilustración, piezas estáticas, data-viz) · `youtube-study-playbook.md` (cómo "ver" videos de referentes). Este codex cubre el producto DIGITAL (lo que se renderiza vivo en pantalla); para la gráfica de marca (estática + identidad, todos los soportes) la disciplina es `graphic-design-playbook.md`. Este codex es el QUÉ/por-qué transversal; los playbooks son el CÓMO técnico hondo.

---

## LEY 0 — La línea entre "AI básico" y "world-class" no son más features

Es **decisiones tomadas en contra del diseño** (restraint) + **realismo de material/luz/movimiento** + **la imperfección de una herramienta real** (lente, mano, física). Test único: si alguien puede decir "esto lo hizo/diseñó una IA" o "esto es un template" sin dudar → rehacer. El slop no es feo; es **intercambiable**. Si podés cambiarle colores y textos a un UI y sirve para otra empresa del mismo rubro → es slop. La firma de identidad hace al producto reconocible en una captura parcial.

**Calibración maestra (vale para visual, motion, 3D, video):** *si podés nombrar el efecto, está demasiado alto.* "Tiene un glow azul", "tiene gradiente arcoíris", "se ve el glassmorphism", "se ve la sombra". El efecto world-class está tan integrado que no tiene nombre propio — se percibe, no se analiza.

---

## PARTE I · CRAFT VISUAL & PRODUCTO (UI)

### Tipografía & jerarquía
- **Una familia basta; dos máximo, con rol semántico claro** (display ≠ body). El par funciona por división de trabajo, no por decoración. (Cohere, Mistral, Cal, BMW.)
- **El peso del display va al límite INFERIOR de lo legible (300–500), no al máximo.** Delgado a escala grande = sofisticación; negrita a escala grande = grito. Premium usa 400–500 en hero; genérico usa 700–900 en todo. (Stripe 300, Runway 400, Coinbase 400, Tesla ≤500.)
- **Letter-spacing negativo proporcional al tamaño: −(fontSize × 0.015 … 0.025).** Tracking positivo/cero en display ≥32px = señal de básico. (Linear −3px@80, Vercel −2.4px@64, Revolut −2.72px@136.)
- **Line-height: display ≤1.15 · body ≥1.50.** Sin excepción. El slop mezcla (display aireado + body apretado).
- **Eyebrow/label de sección = UPPERCASE + mono o serif diferenciado**, nunca sans regular. Si es sans, al menos `font-feature-settings` + tracking ≥+0.5px. (Vercel Geist Mono, Cal JetBrains Mono, Raycast ss03.)
- **`font-feature-settings` activos = el diferenciador invisible.** El mismo Inter "suena" distinto con `cv01`/`ss03`/`dlig`. Inter pelado = Inter genérico. (Raycast ss03 site-wide, Stripe ss01.)
- **≤3 pesos tipográficos en todo el sistema.** 300/400/500/600/700/800 simultáneos = no hay sistema. (Vercel 400/500/600, Tesla 400/500.)

### Color & contraste
- **Un solo color cromático de acción; todo lo demás neutro o fotografía.** El slop mete 4–8 acentos. (Linear, Vercel monocromo, Apple, Ferrari, Coinbase, Spotify, Tesla — un acento cada uno.)
- **El canvas nunca es blanco/negro puro — tiene tinte.** El tinte es la huella del sistema; #fff/#000 son el default del browser. (Linear `#010102`, Vercel `#fafafa`, Runway `#fdfcfc`.)
- **Escala de superficies: 3–5 pasos nombrados, delta de luminosidad consistente.** Saltar pasos o duplicar valores = jerarquía rota.
- **Hairlines con hex específico, NUNCA opacidades redondas** (`rgba(0,0,0,0.1)`). La opacidad round (.1/.2/.5) grita "token de draft". (Linear hairline `#23252a` vs hairline-strong `#34343a`.)
- **Color semántico (success/error/warning) SOLO en estados funcionales, nunca en marketing/hero.** Verde en hero "porque transmite éxito" contamina la paleta.
- **En dark, la profundidad viene de delta de luminosidad, NO de sombras.** `box-shadow` en dark suele ser doble señal que se cancela. (Linear 5 niveles, cero shadow en UI.)
- **Polarity flip (tier "featured" en dark sobre canvas light, o viceversa) es la única excepción al monocromo.** El featured NUNCA suma un color — invierte el polo. (Stripe navy, Superhuman, Coinbase.)

### Espaciado · grid · ritmo
- **Base 4px u 8px. Cero valores off-grid (5/7/11/13px).** Spacing = multiplicadores exactos.
- **Section rhythm ≥80px entre bloques major; lujo 96–128px.** Gap 32–48px = "template gratuito". (Vercel/Coinbase/Figma/Linear 96px.)
- **Padding interior de card = 24–32px, nunca 16px** en cards de contenido (16px = `<div>` sin diseño).
- **El white space ES contenido.** "Llenar el vacío" rompe la respiración; el espacio entre secciones señaliza que la sección terminó.

### Layout & composición
- **Una sola afirmación por banda de contenido; el scroll es el ritmo.** "Densidad de marketing" (logo+headline+3 bullets+CTA+imagen+badge) = anti-patrón universal. (Tesla: headline+sub+2 botones por viewport.)
- **Lujo = fotografía edge-to-edge como FONDO/ambiente, no como `<img>` flotante con radius+sombra.** La foto ES el layout; el texto flota con el mínimo chrome. (Ferrari, Lambo, Tesla, Apple, Runway.)
- **Una "pieza signature" por marca** — el elemento visual irreplicable sin ese brand. Sin él, no hay identidad. Repetida pierde impacto: úsala una vez por página. (Mistral sunset-stripe, Raycast 3 rayas, Linear cards flotando.)
- **Máx 2–3 cambios de polaridad de superficie (light→dark→light) por página.** Más = página sin estructura de lectura.

### Componentes
- **El radius del botón define el carácter** (decisión, no default): pill 9999px = consumer/amigable · rect 0–4px = premium/automotive · medium 6–12px = herramienta. Radius mezclado sin lógica = sistema no resuelto.
- **El primario tiene UN estilo; el secundario es la negación cromática** del primario (no un tercer color). (Vercel negro→blanco, Apple azul→blanco.)
- **CTA nunca genérico.** "Get Started"/"Learn More"/"Click Here"/"Comenzar" = slop. El label responde *"¿qué pasa cuando hago clic?"* e incluye el nombre del producto cuando aplica. ("Start building", "Get Superhuman".)
- **Botones ≥44px height; font-size del botón ≠ font-size del body.**
- **La card featured se distingue con UNA señal, no tres** (borde de color + badge "Popular" + gradiente + shadow = ruido). Preferir polarity flip o surface-elevated.
- **Card radius ≥12px en sistemas modernos** (Linear 12, Vercel 16, Figma 24); excepción intencional automotive 0px. Radius consistente entre componentes del mismo tipo — siempre.
- **Nav ≤5 ítems primarios, altura ≤52px, background casi invisible.** Nav con gradiente o ≥80px consume atención que es del contenido.
- **Inputs: 1px hairline → focus = 1px en color de acción + ring sutil (2px rgba).** El `box-shadow 0 0 0 3px` opaco confunde.
- **Números en tablas de precios/specs en monospace.**
- **El estado empty/loading/error tiene el mismo craft que el default.** Skeleton que replica el layout real; empty con copy útil. "No hay datos disponibles" en gris = craft abandonado.

### Microcopy / voz
- **Eyebrows = sustantivos o verbos imperativos, no frases de marketing.** ("DEPLOY · PREVIEW · SHIP".)
- **Números en hero sin hedging: exactos o nada.** "2.5 sec", "340 km/h" — sin "más de"/"aproximadamente". El número hedged = inseguridad.
- **Las marcas premium no explican lo obvio.** Muestran el feature (benchmark, screenshot, command palette), no lo describen. Copy que repite lo que el screenshot ya muestra = ruido.

### Restraint (la ley transversal)
- **Restraint = decisiones EN CONTRA.** Cada elemento que NO está es tan decisivo como el que está. (Vercel rechazó todo color ≠ `#171717`; Tesla rechazó shadow, radius>4, bold.)
- Glassmorphism visible, mesh-gradient de template, bevel/emboss, sombra que "se ve como sombra" = exceso. Depth percibida, no analizada.

### Tells visuales AI-básico → corrección world-class
| Tell | Corrección |
|---|---|
| Tracking ≥0 en display ≥32px | −(fontSize × 0.02) mínimo |
| `font-weight:700` en hero | 400–500 en display; 600 solo en subheads |
| 3+ acentos en un screen | 1 color de acción; resto neutro |
| `box-shadow:0 4px 6px rgba(0,0,0,.1)` (Tailwind default) | delta de luminosidad de superficie, o shadow ultra-específica |
| section gap 32–48px | ≥80px (premium 96–128) |
| placeholder "Ingresa tu correo aquí" | copy funcional ("Search for apps and commands…") |
| card featured con 3 señales | 1 señal (polarity flip) |
| radius inconsistente primario/secundario | sistema monotético de radius |
| Inter sin feature-settings | `cv01`/`ss03`/`dlig` activos |
| nav 8–12 ítems | ≤5, altura ≤52px, bg invisible |
| `transition: all .3s ease` | propiedades explícitas (`background-color 150ms…, transform 200ms…`) |
| white space "lleno" | gap mínimo de sección 80px; resistir el llenado |
| imágenes stock en hero | arte propio / producto real / placeholder tipográfico art-directed |
| spacing 5/7/11/13px | base 4/8px, cero off-grid |
| CTA "Aprende más"/"Comenzar" | responde "qué pasa al click" + nombre de producto |

---

## PARTE II · MOTION & INTERACCIÓN

### Principios en jerarquía de impacto (UI, no todos valen igual)
- **Nivel 1 (imprescindibles):** *Easing* no-lineal (lineal = robot; cubic/spring = física) · *Anticipation* (micro-setup + háptico antes del gesto principal) · *Squash&stretch* en interacciones físicas (da masa).
- **Nivel 2 (eleva a "vivo"):** *Follow-through/overshoot* (no para en seco — rebota leve antes de descansar; spring damping bajo = vivo, alto = correcto pero muerto) · *Secondary motion* (las partes que acompañan: sombra que sigue al card, texto que se reacomoda) · *Timing = peso* (duración proporcional a la masa; el error #1 es mismo duration para todo).
- **Nivel 3 (polish):** *Exaggeration* (checkmark 110% por 80ms antes de 100%) · *Arc* (los objetos siguen arcos, no rectas) · *Solid drawing* (pensar volumen aunque sea flat).

### Reglas duras de motion
- **Velocidad por tipo de interacción, propiedades explícitas:** micro 150–300ms · entrada de pantalla 300–600ms · ambiente continuo 1000ms+. NUNCA `transition: all`. NUNCA `ease:'linear'` en algo visible.
- **Sistema de DOS velocidades** (referente Headspace/Calm): UI interactiva <150–200ms + ambiente lento 2–8s. El CONTRASTE entre las dos crea profundidad/presencia.
- **Springs (Reanimated 4) con `duration + dampingRatio`, no `stiffness + mass`:** tap `{200, 0.9}` · transición `{500, 0.75}` · entrada con overshoot `stiffness 120/damping 14/mass 0.8` · tab-pill `300/20`.
- **Press premium = scale + shadow + háptico, NO opacity.** `scale 0.96` onPressIn → `1.0` onPressOut; shadow 4px→1px sincronizada; `ImpactFeedbackStyle.Light` en pressIn. Opacity dice "apagado"; scale dice "presionado físicamente".
- **Stagger reveal 60–80ms por ítem, siempre `.springify()`.** `FadeInDown.delay(i*80).springify().damping(14)`. Stagger total ≤200ms. No aumenta la duración percibida — la hace fluida. Contenedor → hijos → detalles.
- **Hover = cambio de luminosidad de superficie, no de color de texto** (cambiar color de body confunde con link).
- **Háptico triaxial como confirmación de estado, no decoración:** light al iniciar drag → medium al cruzar el threshold de no-retorno → success notification al completar. El háptico en el threshold exacto es la señal subconsciente más recordada.
- **Shared Element Transition = la técnica de mayor impacto per-esfuerzo en mobile.** Card que "crece" hacia el detalle → el usuario lee la app como nativa de verdad. (Reanimated 4.2+ `sharedTransitionTag` bajo flag, o `react-native-shared-element`.)
- **Frecuencia manda:** acción 5+ veces/día → reducir/eliminar animación (600ms × 5/día = 3s de espera/día). Lista frecuente <5 ítems → mantené el reveal.
- **Design tokens de springs, no inline:** `fast {400,22}` · `default {200,18}` · `gentle {120,14}`. Inconsistencia entre pantallas = app "rota" aunque cada una funcione aislada.
- **Animación data-driven, no scripted:** estado cambia → valor derivado → alimenta la animación declarativamente (Rive input / Reanimated shared value / CSS custom property). Anti-patrón: `onPress → startAnimation`. Correcto: `onPress → setState → estado alimenta animación`.
- **Rive como reemplazo de lógica de estado de animación:** el state-machine acepta inputs booleanos/numéricos; la app solo actualiza variables, cero interpolación en JS. Separa diseño-de-animación (Rive) de lógica-de-datos (TS). Siempre crear `rivRef` para poder actualizar en runtime.
- **Skia: `dropShadow` y `BoxShadow` (en `RoundedRect`) = rápidos; `innerShadow` = lento en gama baja** → máx 1–2 elementos hero con inner shadow, resto drop. Círculo con sombra = `path.addCircle` + BoxShadow, nunca inner.

### Movimiento ambiental vs reactivo (no confundir)
- *Ambiental*: el fondo respira independiente del usuario (idle, latido, niebla que pasa). *Reactivo*: responde al input. Slop = todo reactivo (flashy/ansioso) o todo ambiental (bonito/muerto). Proporción óptima: **80% ambiental / 20% reactivo en idle; invertir a ~30/70 durante interacción activa.**

### Señal de craft vivo vs muerto
| Señal | Muerto | Vivo |
|---|---|---|
| Easing | lineal | cubic/spring con masa |
| Inicio de gesto | inmediato | anticipation 2–4 frames |
| Fin de movimiento | para en seco | overshoot + follow-through |
| Partes del objeto | mueven juntas | offset (secondary motion) |
| Peso | mismo timing para todo | timing ∝ masa |
| Táctil | press muda color | scale+shadow+haptic coordinados |
| Loop | corte brusco | ease-out al final, ease-in al reinicio |
| Cold state | pantalla vacía / spinner | demo/skeleton + "esperando" animado |

---

## PARTE III · REALISMO 3D & CINEMÁTICA (R3F / three.js · web)

> Para DIRIGIR un video (splash pre-render, clip in-app, hero landing, ad) — composición, lente, montaje, sonido, prompting generativo, rúbrica 10/10 — el documento es `cinematography-playbook.md`. Esto es el stack técnico R3F.

### Realismo (las palancas, con valores)
1. **HDRI = palanca #1.** Equirectangular 32-bit (Polyhaven CC0) por `PMREMGenerator`; `environmentIntensity 1.5–2.0`. Dev 1k / prod 2k. Sin HDRI el cristal/metal se ve "sucio".
2. **glTF/GLB real > procedural.** El ojo detecta topología procedural. Pipeline: `npx gltfjsx Model.glb --transform -T --types --resolution 1024 --format webp` (Draco + KTX2/Basis → −70–90% peso + TSX tipado). `useGLTF.preload()` = no-negociable en splash. *(Excepción: esfera + transmission + HDRI ya es foto-real para un orb.)*
3. **Cristal = `MeshTransmissionMaterial` (drei), NO `MeshPhysical.transmission`** (el de drei hace un pase extra de refracción): `transmission=1, thickness=1.5, roughness=0.015, chromaticAberration=0.04, backside=true, ior=1.52, samples=6, attenuationDistance=1.2`. La aberración en bordes es la firma óptica vs "plástico".
4. **Normal map = palanca #1 de microdetalle** (arañazos/grano = normal, no geometría). + `roughnessMap`+`metalnessMap`+`aoMap` (ORM) + `envMapIntensity=1.8`. Lacado premium: `clearcoat=1.0, clearcoatRoughness=0.05`. CC0: ambientCG, polyhaven.
5. **Contact shadow = la diferencia entre flotar y existir** (tell #1 de AI-básico). `<ContactShadows frames={1} blur={3} opacity={0.25}/>` (render-once, 0 runtime) o `AccumulativeShadows temporal frames={80}` + `RandomizedLight`.
6. **Tone mapping: AgX > ACESFilmic para saturados (verde/cián)** — ACES los vuelve fluorescentes. ACES para punch/contraste dramático, exposure ~1.2. ⛔ `renderer.toneMapping = NoToneMapping` cuando el `ToneMapping` vive en el composer (no aplicar dos veces).
7. **Color management** (R3F r139+ auto): color sRGB, datos (normal/rough) Linear.

### Post-stack — el ORDEN es física, no sugerencia
`N8AO → SelectiveBloom → DepthOfField → ToneMapping(ACES/AgX) → LUT → ChromaticAberration → Vignette → Noise(grain, ÚLTIMO)`. Setup: `<Canvas gl={{toneMapping:NoToneMapping}}>` + `<EffectComposer enableNormalPass frameBufferType={HalfFloatType}>`.
- **N8AO > SSAO** (mejor ruido, sin flicker al mover cámara): `aoRadius=2.5, intensity=5, aoSamples=16, denoiseSamples=8`. Es `N8AOPostPass` (no el `Effect` estándar); incompatible con MSAA hardware → SMAA aparte.
- **SelectiveBloom > Bloom general** cuando es puntual: solo meshes en `selection[]`; el material emisivo necesita `toneMapped={false}` + `emissiveIntensity>1`. `intensity 2–2.5, luminanceThreshold 0.9, mipmapBlur, kernelSize VERY_LARGE`. Fallback sin composer: `fake-glow-material-r3f`.
- **DOF narrativo, no decorativo:** `bokehScale 3–6` (cine); >8 = videojuego. Reveal: `8` (solo hero en foco) → `2` al pullback. `AutoFocusDOF` por raycasting.
- **LUT = máximo color-grading al menor costo GPU.** `.cube` 3D (teal&orange, cold-desat, warm-analog). Fuentes: Iwltbap, VSCO, DaVinci.
- **Lens character = suma de imperfecciones:** chromatic `0.001–0.002` (`radialModulation=true` → se intensifica en bordes, físicamente correcto) · grain `opacity 0.02–0.08` `blendFunction SOFT_LIGHT` (blue-noise 65% + white 35% con jitter evita patrón estático) · vignette `offset 0.25–0.35, darkness 0.5–0.7`. Calibración: desactivá uno por uno; cada quitada hace la escena más "digital".

### Cámara / cinematografía
- **La cámara SE MUEVE — primero ella, después el objeto.** Cámara estática + objetos animados = presentación; cámara que respira/dolly/orbita = cine. **Un movimiento por plano** (combinar push+pan+tilt+zoom = mareo/slop).
- **`camera-controls` (yomotsu, vía drei)** = estándar de facto: `dollyTo`, `setLookAt`, `lerpLookAt` (interpola entre dos poses completas — clave para intros), `fitToSphere`. `smoothTime 0.4`. `cc.enabled=false` durante secuencias.
- **`maath easing.damp3/dampE` = frame-rate-independent** (lerp fijo depende del fps). Parallax mouse: pitch `pointer.y*0.15`, yaw `pointer.x*0.2`, smoothTime 0.25. ⛔ valores que cambian a 60fps (pos/rot de cámara) NUNCA en React state → refs mutables en `useFrame`.
- **Theatre.js para secuencias time-based (intro splash); GSAP para multi-shot con easings custom** (`CustomEase`). Ambos: refs mutables, nunca tocan React state.
- **FOV cine:** 20–30° (compresión/aislamiento) · 45–55° (neutral, default) · 65–75° (ambiente) · 85–100° (expresivo). Dolly-zoom: mover cámara + abrir FOV + `updateProjectionMatrix()`.
- **Luz de 3 puntos con identidad material:** KEY 60–70% (direccional 45° cálido 6500K, castShadow) · FILL 20–30% (hemisphere/ambient frío bajo) · RIM 40–50% (point detrás-lateral cián → separa del fondo + amplifica SelectiveBloom en el borde = halo de producto; incluir en `SelectiveBloom.lights[]`).
- **Temperatura como narrativa:** sombras frías / altas cálidas (teal&orange) empuja materiales saturados a leer "de lujo" en vez de "plástico". Vignette en SOFT_LIGHT preserva saturación.

---

## PARTE IV · SPLASH & ONBOARDING WORLD-CLASS

- **Splash 1.2–2.5s máximo. Cero texto explicativo, cero loading indicator.** No explica el producto — crea el TONO emocional.
- **Arco de splash en 4 beats:** (1) *Silencio* 0–15% — cámara lejos, hero apagado escala 0.6, grain+vignette ya presentes. (2) *Encendido* 15–50% — push-in, el material revela, bloom crece con la emisión. (3) *Respiración* 50–75% — micro-órbita/parallax, chromatic en bordes, DOF solo-hero-en-foco. (4) *Reveal* 75–100% — pullback leve, wordmark fade-up, DOF abre, vignette suaviza, fade a la app.
- **Primer micro-logro funcional en <60s del onboarding** — una victoria concreta ("tu primer registro fue exitoso"), no informativa ("aquí puedes registrar"). Es la diferencia entre onboarding recordado y olvidado.
- **Permisos POST-valor, nunca al inicio.** Pedir cámara/notif/micro recién después de mostrar el valor que habilitan.
- **Continuidad visual entre pasos = onboarding memorable.** El elemento hero del splash (orb/símbolo/mascota) sobrevive como hilo conductor de todo el onboarding (shared element / variaciones del mismo actor). Si cada paso tiene su propia identidad → es un formulario, no un mundo.
- **Mecánicas de retención probadas (apps de hábito/mascota):** streak desde día-1 (no día-0 — el usuario llega al día 2 con algo que perder) · "adventure timer" (reason-to-return sin push) · customization = monetización (skins/outfits) · capa de emoción secundaria (el actor reacciona a las acciones recientes). Anti-patrón: copiar el screen "¿dónde nos conociste?" sin datos que lo justifiquen.

---

## PARTE V · ARQUITECTURA HÍBRIDA — qué corre dónde (leyes de ingeniería)

| Superficie | Stack | Por qué |
|---|---|---|
| Landing web marketing | R3F real-time COMPLETO (HDRI+transmission+post-stack+parallax) | Desktop GPU aguanta; escaparate Awwwards; sin throttling térmico |
| Splash mobile (one-shot 2–3s) | **VIDEO pre-renderizado** MP4/WebM ~1MB (escena 3D offline → ffmpeg) | Calidad AAA idéntica en gama baja, 0 overhead runtime |
| Onboarding interactivo mobile | **Rive** (state-machines, ~300KB) | 60fps en Android viejo, vectorial, integra gestos |
| Elementos in-app persistentes | **react-native-skia SkSL** | 60fps garantizado en gama baja (2–5ms/frame); vignette/grain/DOF *fake* con capas Skia |
| Celebraciones/momentos hero efímeros | **Pre-render** 4K → sprite/video corto | Imposible real-time, trivial pre-renderizado |

**Reglas de viabilidad (RN nativo, gama baja Snapdragon 680 / Adreno 610 · estado 2026-06):**
- ⛔ `@react-three/postprocessing` **roto en RN nativo** (`renderbufferStorageMultisample` no impl.): Bloom, SSAO, SSR, DOF, ChromaticAberration, Vignette, Grain = **web-only**. No buscar workaround → pre-render o Skia.
- ⛔ R3F native roto por mismatch `expo-gl@11` (R3F) vs `@15` (SDK 53+). HDRI/IBL (`RGBELoader`) roto en Hermes (sin web-workers); KTX2/Draco `Cannot create URL for blob`. Web sí, native no.
- ⛔ `MeshTransmissionMaterial`/glass en mobile: NO (framebuffer copy no impl.; cae a 25–30fps aun en gama alta) → simular con SkSL (fresnel/distorsión/rim fake).
- **Lo que SÍ se finge en Skia sin postprocessing:** vignette (overlay radial) · grain (SkSL 2D) · bloom/glow (capas `blur()`) · DOF (blur gaussiano en capas traseras) · refracción (SkSL distorsionando lo de atrás con normal de esfera).
- **Giroscopio = faux-3D sin 3D:** `expo-sensors` + Reanimated → al inclinar, las capas se desplazan ∝ profundidad. Costo GPU cero, percepción de profundidad real. El mayor diferencial in-app al menor costo.
- **Insight maestro:** wow 3D mobile = pre-render. wow interactivo = landing web. in-app = Skia/Rive que finge profundidad. Tres herramientas, **una estética**. No pelear el hardware en tiempo real.

---

## PARTE VI · SHORT-FORM SOCIAL & VIDEO GENERATIVO

### Short-form vertical (9:16)
- **El primer frame es el contrato:** resuelve "¿para quién es esto?" en <300ms con TENSIÓN visual (objeto en movimiento, texto incompleto, contraste extremo), no con logo/title-card.
- **Una pantalla, una pregunta; cada corte genera la siguiente.** 4 beats (estado→problema→solución→call), no 10.
- **Texto en pantalla = subtítulo funcional** (85% ve sin audio): ≤12 palabras/frame, alineado izquierda + bold + contraste extremo, en el cuadrante de espacio muerto. Sin outline, sin sombra difusa, nunca centrado si hay hero.
- **El loop se diseña primero:** el último frame rima compositivamente con el primero (mismo valor tonal / posición del hero / misma palabra).
- **Velocidad de corte = urgencia, no energía:** primeros 2s lentos (anclan) → medio rápido (pico) → últimos 1.5s desaceleran (permiso para procesar antes del CTA → baja el abandono pre-CTA).
- **El producto como personaje:** la pantalla del producto *actúa* (se mueve, reacciona, tiene peso), no screenshots estáticos con zoom. Es la diferencia entre "parece ad" y "parece contenido orgánico".

### Video generativo (grok-cli / Sora / Runway)
- **El prompt especifica FÍSICA, no apariencia.** Slop: "mystical orb glowing blue". World-class: "ring rotating 15°/frame, contact shadow hardening as it descends, haze rolls L→R at 0.3× ring speed, rack-focus ring→background on frame 48". La apariencia es consecuencia de la física; si solo describís apariencia, el modelo inventa física y se nota.
- **Movimiento de cámara = primera decisión.** Sin trayectoria propia de cámara = parece render/GIF. Mínimo: push-in 2–3% de FOV en todo el clip.
- **Atmosféricos (niebla/haze) dan gratis lo que la geometría cobra caro:** ocultan discontinuidades de geometría AI, crean profundidad sin HDR, dan escala. El modelo los produce bien (ruido suave, no geometría precisa).
- **Loop de 3–8s, no clip largo.** Pasados ~8s aparece *temporal drift* (pérdida de consistencia del objeto). Generar 8s, cortar al momento de máxima consistencia, loopear.
- **Identidad = ancla geométrica fija:** texto/logo en el generativo se DEFORMA en motion → generar SIN texto y compositar el texto en post (AE/Fusion). El logo nunca vive en el clip generativo.
- **Post-proceso obligatorio (mínimo 3 pasos)** sobre cualquier crudo de IA (siempre trae subexposición en shadows, chroma-noise en transiciones, jitter temporal en bordes): (1) grade ACES tonemap · (2) temporal denoise (`hqdn3d` / Magic Mask) · (3) frame-blending ×2 si hay jitter.

### Tells de social/generativo → corrección
| Tell | Corrección |
|---|---|
| Objeto flota sin shadow | compositar shadow sintético en post |
| Logo/texto se deforma en motion | generar sin texto, compositar en post |
| Movimiento lineal sin easing | ease in/out en post (frame-blend / motion-blur) |
| Fondo idéntico cada frame | atmospheric independiente (haze/dust/bokeh drift) |
| Saturación máxima en todo | desaturar todo salvo el hero en grade |
| Jitter temporal en bordes | temporal denoise + edge-aware smoothing |
| Cámara 100% fija | camera-movement keyword o parallax en post |
| Clip >15s pierde identidad | segmentos de 8s + crossfade |
| Texto centrado con sombra | izquierda, sin sombra, contraste extremo |

---

## PARTE VII · CRAFT DE INGENIERÍA & HARNESS (el 360 técnico)

> ATLAS no es solo el filtro VISUAL — es el filtro de calidad del 360. Estas leyes valen para cómo se construye, no solo cómo se ve. (Detalle de criterio de código: pilares `fable5/P1–P5` + `seguridad.md` + `testing-estrategia.md` + `llm-engineering.md`, ruteo en `fable5-transfer-playbook.md`.)

- **El harness importa tanto como el modelo.** Con buen harness un modelo mediano supera a uno superior; sin él, el de mayor benchmark entrega mediocre. El AI layer = rules + skills + hooks + MCP + LSP + subagents (en ese orden de impacto marginal).
- **Context window = el recurso más escaso** (no el dinero ni el tiempo). Todo el diseño optimiza la ventana.
- **Rules lean (<200 líneas el global).** Rules files de miles de líneas DEGRADAN la performance — el modelo se satura. Layering > monolito (rules por subdirectorio, progressive disclosure). Separar *rules* (qué no hacer) de *skills/workflows* (cómo hacer X).
- **Reset entre planning y execution:** terminar el planning con un output a `.md` → contexto limpio → execution solo con ese archivo de input. **Estado en DISCO, no en chat:** retomar una tarea larga = leer el archivo de estado, no scrollear el chat. **Compactar temprano** (al primer warning, antes de que el modelo derive).
- **Spec-first (PRD antes de código):** documento markdown de scope/out-of-scope/arquitectura/tareas = north-star de toda la implementación. Sin PRD, las iteraciones no se conectan.
- **Skill = `SKILL.md` (metadata + índice) + `scripts/` + `templates/` + `data/`.** Progressive disclosure: solo `name+description` en cada prompt; el cuerpo se lee on-demand → cientos de skills sin saturar contexto. Path-scoping: skill activa solo en su subdirectorio. **Skills con evals:** A/B (3 agentes con skill vs 3 sin) sobre los mismos prompts con PASS/FAIL concreto; iterar hasta que el benchmark deja de mejorar.
- **Subagents (exploración aislada → resumen, barato) vs Agent-teams (implementación, peer-to-peer, 2–4× tokens).** Regla: subagents para research → plan → team para implementar. **Contract-first spawning:** fijar contratos upfront (schema DB → backend → frontend); los dependientes esperan el contrato, no el finish.
- **Hooks no son solo guardianes — son el meta-loop de mejora:** start-hook carga contexto dinámico; stop-hook corre una sesión headless que revisa los cambios y propone updates al rules-file. El sistema se mejora a sí mismo.
- **Ley de oro — fix el SISTEMA, no solo el bug:** ante un error recurrente, identificar qué parte del AI layer lo permitió (rule/workflow/doc/command) y arreglarla. Hacerlo inmediatamente tras validar la feature, con el contexto fresco.
- **MCP vs CLI vs bash:** plataforma conocida con CLI documentado (GitHub/Jira) → CLI (el modelo ya lo sabe, más rápido/confiable) · servicio interno/desconocido → MCP · operación de un comando → bash directo. MCPs que pagan: Context7 (docs actualizadas), LSP/Serena (search por símbolo).
- **LSP > grep en codebases >50K líneas:** `whereIs(symbol)`/`findReferences` reducen 10–20 greps a 1–2 queries → más tokens para razonar.
- **Multi-agente: la capacidad MENTAL es el límite, no el modelo** (~4 flujos paralelos por humano; worktrees para no pisar el index). Ganancia real de AI-coding reportada en producción: **30–60%, no "5×"** — sube la velocidad de coding; review/arquitectura/entendimiento del problema no. El trabajo se redistribuye, no desaparece.

### Anti-patterns que gritan "template AI" (código + motion)
`ease:'linear'` visible · partículas flotantes sin propósito · bounce excesivo en todo (bounce es énfasis, no estilo) · Lottie para micro-interacciones (pesado, no reactivo, idéntico en todas las apps) · fade-in/out como única transición · post-stack a intensidad máxima ("over-processed") · duración larga en acciones frecuentes.

---

## PARTE VIII · TIER FABLE 0 MITHOS — el salto de 10/10 a ICÓNICO

> 10/10 world-class = sin defectos, nivel agencia. **Mithos** = el 1% que define la categoría: la referencia que otros copian, el Grand-Prix. No es "más calidad" — es un puñado de decisiones de **física real, material que vive, y datos que mueven la interfaz** que casi nadie implementa. La escalera completa: `genérico → esperado → fresco → audaz → 10/10 world-class → MITHOS`.

### A · Física gestual real (Apple "Designing Fluid Interfaces" WWDC) — el delta "responsivo→vivo"
- **Springs por `dampingRatio` + `frequency response (Hz)`, NO por ms.** Duración = consecuencia, nunca input. tap → `dampingRatio 1.0` (sin rebote). gesto → `~0.8` (momentum). Liviano (toast/notif) → freq ~150Hz. Pesado (sheet/nav) → freq ~30Hz. La **masa conceptual** se codifica acá: cada objeto con su masa → el usuario *siente* la jerarquía sin leerla.
- **Función de proyección de velocidad:** al soltar un gesto con velocidad, animar al endpoint proyectado, no al destino fijo. `endpoint = position + velocity / (1 - decelerationRate)` (`decelerationRate ≈ 0.998`). El elemento va a donde el usuario *iba*. Este es EL delta que separa iOS de casi toda app de terceros.
- **Tracking 1:1 es ley** durante el drag (pixel a pixel); la interpolación entra solo al soltar. Cualquier desvío se lee como lag.
- **Rubber-band exacto:** `(1 - (1 / (x * 0.55 / dimension + 1))) * dimension`. No inventar la curva.
- **Hysteresis de 10pt** en todo umbral de scroll (evita oscilación en el boundary). **Detección por spike de aceleración**, no timer; reconocimiento de gestos en paralelo + cancelación, nunca secuencial. **Redirección mid-flight** sin cortar velocidad (multi-eje activo hasta que la dirección domina).
- **Motion stretch + blur en transición elemento→pantalla:** el elemento se estira elásticamente en el eje del movimiento ANTES de expandir, con blur en ese eje. Solo-scale = 10/10; stretch+blur = mithos.

### B · Skia/GPU tier mithos (Candillon et al.)
- **Runtime shader como `imageFilter` sobre el ÁRBOL DE UI VIVO** (no sobre una textura plana): el vidrio refracta contenido en movimiento debajo. Ni SwiftUI nativo lo hace.
- **Liquid shapes = SDF + smooth-minimum** `smin(d1,d2,k)`: `k=0` unión dura · `k=0.3–0.5` líquido. Imposible con path-ops.
- **Refracción óptica = displacement map** derivado del SDF de la forma sobre el background (ref ShaderToy "Optically Correct Liquid Glass", Metro Wind).
- **Variable blur por profundidad:** `depth_n = saturate((depth-near)/(far-near))` → `blur = depth_n * maxBlur` (20–40px). `saturate()` obligatorio.
- **Gotchas que rompen en silencio:** matriz 3D row-major(JS)→column-major antes de `uniform mat4` o la geometría se deforma · `half3*float` → Make null (multiplicar en float, castear al final) · `usePathValue`+`useDerivedValue` para animar paths en worklet (no rerender JS) · ring head: samplear el sweep-gradient en `headPos` (no color plano) · anillo = `outerCircle.op(inner,"difference")` (no clipPath anidado) · multi-revolución: `rotation = progress>1 ? floor(progress)*360 : 0`.

### C · Los 12 principios de animación, COMPLETOS (Rive/mascot · orb)
10/10 = anticipation + ease. Mithos = la cadena entera en cada interacción del actor: **anticipation** (3–5 frames en dirección opuesta) → **squash** (x110/y90, volumen constante x·y) → **acción primaria con arco** (nunca recta; rotación sutil del body) → **secondary motion offset 3–5 frames** (manos/cejas/cola siguen con delay) → **overshoot + elastic settle** → **exaggeration SELECTIVA en el focal point** (ej. eyeball y-scale 300% por 2 frames, resto normal) → **solid drawing** (draw-order para volumen 2D). Easing: in-out (S) orgánico · out-only explosivo · in-only gravedad.

### D · Animación data-driven a nivel sistema (la firma que "vive el contexto")
- **dato → state-machine (Rive) → animación**, JAMÁS dato → CSS/JS interpolado. Inputs tipados: Boolean para estado, Number para posición continua. El código solo `setInput`, Rive maneja blends.
- **Mithos = TODOS los sistemas de datos del usuario alimentan la animación ambiental a la vez** (hora, clima, estado, voz…) → la UI respira el contexto en tiempo real. (Android: shared-element + morph con `skipToLookAheadSize/Position` + `MorphOverlayClip.getClipPath→morph.toPath(fraction)`, compatible con Predictive Back.)

### E · El salto a mítico en lo GENERATIVO/visual (OrbLab + totems + grok)
- **El material EMANA desde adentro, no glow encima.** Glow plano = "se nota IA". Mithos = luz que rompe el cristal desde dentro + **contact-shadow elíptico aplastado** (sin él, "flota/composición IA") + menisco de transmisión en el borde.
- **Jerarquía 7×, no 2.4×:** el elemento REY mide ~7× el secundario (ej. número 132px vs 19px = "cockpit Mercedes"; 64 vs 27 = "tímido"). Medible, no subjetivo.
- **3 planos Z explícitos** (atrás ambiente / medio instrumento excavado / adelante dato con su propia shadow). 2 planos = se lee plano.
- **Secuencia de ENCENDIDO** (no loop): negro → barrido de luz → elementos se trazan en cascada → dato corona con count-up. El objeto se "activa" como instrumento real.
- **Shader orgánico fbm** (5 octavas) sobre canvas para iridiscencia de materia real — imposible en CSS. Sin fbm: círculo de color; con fbm: organismo.
- **Breathing 0.72→0.92 opacity** (nunca 0→1) = vida sin parpadeo (WCAG 2.3.1 safe). **Grain** `feTurbulence baseFrequency 0.74 / 4 octavas`, opacity ~.045, blend overlay = textura anti-IA. **Scrim radial** (no card) para legibilidad sin romper el plasma.
- **Generación = SWEEP, no 1:** generar 4–8 variantes → contact-sheet → elegir el mejor frame. El asset final es el mejor frame de un barrido, no "el mejor prompt". Elegir la **forma-contenedor primero** (rect/circle/panel/float = arquitectura semántica, no decoración). **Anclar materiales con `--image` de referencia real** (evita alucinación de color/material). Detalle de pipeline grok-cli → `prompt-craft-playbook.md` + `creative-direction-playbook.md`.

---

## EL GATE UNIVERSAL 10/10 (checklist consolidado · aplicar antes de declarar terminado)

**Visual (1 pt c/u):** display ≥28px con tracking negativo y lh ≤1.15 · ≤3 pesos y ≤2 familias con rol · 1 color de acción por surface · canvas con tinte + hairlines con hex específico · spacing múltiplo de 4/8 + section gap ≥80px · botones del mismo tipo con radius idéntico y primario = negación del secundario · card featured con 1 señal · ≤1 elemento "signature" por screen · sombras = 0 o 1 nivel específico (dark = delta de superficie) · cero CTA "Aprende más"/"Comenzar" (responde "qué pasa al click").

**Motion:** cero `ease:linear` y cero `transition:all` · press = scale+shadow+haptic · springs por token (fast/default/gentle) · stagger 60–80ms springify · háptico triaxial en gestos con threshold · dos velocidades (UI<200ms / ambiente 1000ms+) · 80/20 ambiental/reactivo en idle · animación data-driven.

**3D/cinemática (si aplica):** HDRI presente · contact shadow (nada flota) · post-stack en orden · tone mapping correcto (AgX para saturados) · lens-character por debajo del umbral nombrable · la cámara se mueve (un movimiento por plano) · refs mutables en useFrame (no React state).

**Splash/onboarding (si aplica):** ≤2.5s sin texto/loader · arco de 4 beats · micro-logro <60s · permisos post-valor · hero como hilo conductor.

**Video/social (si aplica):** primer frame = contrato <300ms · loop diseñado · texto = subtítulo funcional · prompt generativo = física no apariencia · clip 3–8s · post mínimo 3 pasos · logo compositado en post.

**Arquitectura (si aplica):** superficie ↔ stack correcto (web-only no se intenta en RN nativo) · pre-render para wow mobile · estado en disco · spec-first.

**Ingeniería:** rules lean · fix el sistema no el bug · modelo-por-rol en dispatches · subagents para research / teams para impl.

**Score:** MITHOS (icónico · PARTE VIII: física real + material que vive + data-driven) · 10/10 world-class · 8–9 detalles menores · 6–7 foundation con slop visible · <6 redesign. El umbral de ship de ATLAS = el que defina el `matu_mode` del proyecto (normalmente ≥9.0); aspirar a MITHOS en superficies hero/signature.

---

## Referentes (robar craft)
- **RN/Skia in-app:** William Candillon (@wcandillon, co-autor react-native-skia) · **Motion:** Freya Holmér (la math) · Emil Kowalski (el taste) · Rauno Freiberg (interaction) · **Shaders:** Kishimisu, The Art of Code, Inigo Quilez · **3D/web:** Bruno Simon, Yuri Artyukh, Maxime Heckel, SimonDev · **Estudios:** Lusion, Active Theory, Basement (LATAM), Resn · **Rive:** Rive Masterclass · **Data-viz humano:** WHOOP, Oura, Gentler Streak, MacroFactor · **Harness/AI-eng:** Cole Medin, Anthropic AppliedAI (Cal), Barry+Mahes (skills). **Galerías:** Awwwards (webgl-shaders-code), FWA, Godly, Codrops. Cómo "ver" sus videos → `youtube-study-playbook.md`.
