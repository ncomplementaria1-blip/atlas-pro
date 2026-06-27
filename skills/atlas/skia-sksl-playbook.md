# Skia / SkSL · RN Playbook — world-class shaders sin crash ni lag

> Lecciones DURAS de implementar el orb + totem plasma-tube en producción (NutricomAI, 2026-05-31).
> Consumir al construir/revisar CUALQUIER visual Skia en RN (rings, orb-guía, totem, celebraciones).
> Complementa `worldclass-craft.md` (estética) con el CÓMO técnico. Cada punto = una hora perdida que no se repite.

---

## A. SkSL — sintaxis y gotchas (compila o no compila)
- Tipos: `float2/float3/float4` (NO `vec2`). Entry: `half4 main(float2 fragCoord)`. Retorno premultiplicado: `half4(col*alpha, alpha)`.
- **NO hay `fwidth`/derivadas** garantizadas → AA analítico con un uniform `u_px` = ancho de 1px en uv (`1.0/SIZE`-ish). Toda banda/borde se suaviza con `smoothstep(aaB, -aaB, dist)` usando `aaB=u_px`.
- Uniforms vecN se pasan como **arrays JS**: `uniform float4 u_pc;` ← `{ u_pc: [a,b,c,d] }`. Las keys del objeto deben matchear EXACTO los uniforms declarados (sobra/falta uno → crash o basura).
- `atan(y, x)` es la versión 2-arg (atan2). Cuidá el orden.
- `RuntimeEffect.Make(...)` a nivel módulo + guard `if (!SHADER) return null` → si la compilación falla, render null en vez de crash.

## B. ⛔ Y-FLIP WebGL → Skia (el bug que Ale cazó, /matu no)
- WebGL: `gl_FragCoord.y` crece hacia ARRIBA (y-up). Skia: `fragCoord.y` crece hacia ABAJO (y-down).
- Portar un shader WebGL a Skia SIN invertir `uv.y` → **toda la geometría angular queda espejada vertical** (arcos/barridos en el lugar equivocado). Lo radial (`length(uv)`) no se afecta.
- Fix: `float2 uv=(fragCoord-0.5*u_res)/u_res.y; uv.y=-uv.y;` justo al calcular uv.
- Test obligatorio: que cada elemento angular caiga en la posición del master, no solo "que estén los colores".

## C. ⛔ WORKLET SAFETY (crash nativo abort trap 6)
- Los uniforms se arman con `useDerivedValue(() => ({...}))` → ESO ES UN WORKLET (UI runtime).
- **NUNCA llamar una función JS no-worklet dentro del worklet** (ej. `clamp01(...)`) → Hermes `throwPendingError` → `__cxa_throw` → terminate → **Abort trap 6** (crash nativo, NO redbox).
- El worklet SOLO puede capturar: valores planos (números, arrays), shared values (`clock.value`, `sv.value`), consts de módulo. Toda transformación (clamp, map, math con funciones) → **precalcular en el JS thread** (`useMemo`) y capturar el resultado plano.
- Diagnóstico: si la app se va al HOME (no redbox) al montar un componente Skia+Reanimated → es esto. Leer el crash `.ips`: backtrace con `worklets::RuntimeDecorator::call` + `HermesRuntimeImpl::throwPendingError` lo confirma.
- Patrón validado: `AlexiaOrbSkia.tsx` y `CaloriasTotemV2.tsx`.

## D. ⛔ Falsy-leak-render (crash en prod con data vacía)
- `{count && <X/>}` con `count=0`/`""` → RN intenta renderizar `0`/`""` fuera de `<Text>` → crash.
- Usar SIEMPRE `{count > 0 && ...}`, `{x != null ? ... : null}`, o ternario con `null`. Los strings dentro de `<Text>` (`${pct != null ? ... : ""}`) están OK.

## E. Performance gama baja (Adreno 610 / Snapdragon 680)
- **focus-pause:** `useIsFocused()` → cuando NO hay foco, NO leer `clock.value` (devolver `u_time` constante) → el derived value deja de cambiar → el Canvas deja de invalidar → 0 GPU fuera del tab. Crítico para batería.
- `fbm` 3-4 octavas en shaders CONTINUOS (no 5). 5 octavas solo si es one-shot o el device aguanta.
- **Grano:** `hash(uv*u_res+t)` con `uv*u_res` ~340 → el arg de `sin()` se va a ~10^5 → `mediump` pierde precisión → banding/moiré en gama baja. Sembrar con valor acotado (`uv` ±0.5) o validar en APK.
- `needs-apk-validation: SÍ` SIEMPRE en shaders full-screen continuos (el sim/iPhone miente sobre perf de gama baja).
- BlurMask es caro: en low-end, light-head sin blur o blur chico (≤5).

## F. Craft visual (cómo un shader se ve world-class)
- **AA / grosor del core:** `u_px` chico (~0.7/SIZE) = core brillante GRUESO (bandas crisp). `u_px` grande (1.15) come el core → se ve fino/lavado. Balance: crisp sin shimmer (validar animado en device).
- **Bloom/glow:** `c*exp(-max(dBand,0)*k)*intensidad`. `k` menor (17→15→13) = halo más ANCHO/suave. Intensidad en la **mitad-baja** del rango (restraint · ~0.18). Modular con la respiración, no con el valor del dato (TCA-safe).
- **Sección de tubo 3D:** `tube = 1.0-0.5*across*across` (across = pos normalizada -1..1 a través del grosor) → centro vivo, bordes caen. + `spine = smoothstep(0.18,0,abs(across))*0.12` (cresta/highlight, redondea).
- **Plasma sedoso:** `fbm` con interpolación QUÍNTICA `f*f*f*(f*(f*6-15)+10)` (no cúbica `3-2f`). Flujo: `fbm(dir*K + (t*vx, t*vy) + across*A)`.
- **Ignición one-shot escalonada:** `1.0 - pow(1.0 - clamp((ig*S - delay - idx*stagger)/dur, 0,1), 3.0)` (ease-out cúbico, stagger por índice del elemento). Respeta reduce-motion (instantáneo).
- **Inicio iluminado con propósito:** gradiente `startGrad = mix(1.0, 0.45, localT)` (el comienzo del arco brilla, el fin atenúa) → marca principio/fin, da coherencia.
- **Disco transparente:** `alpha = smoothstep(0.47, 0.445, dist)` y retornar `half4(col*alpha, alpha)` → compone sobre cualquier fondo (Canvas transparente, no negro).

## G. Supersampling residual (por qué el RN no iguala el prototipo WebGL)
- El prototipo WebGL suele renderizar con supersampling (SS=2.6: render a 2.6× → downsample) → bordes suaves + bloom "fat". Skia a device DPR (~3×) NO supersamplea igual.
- Resultado: los tubos/bordes del RN se ven un toque más finos/duros que el proto.
- Compensar BARATO con: `u_px` chico (core grueso) + bloom más ancho (`k` menor) + grosor `T` que escale con el radio. NO meter supersampling real en el shader (2-4× costo GPU, rompe gama baja).

## H. Geometría escalable
- Definí TODO en fracciones del SIZE (R, T, kcal radius, R_MACRO). Para agrandar/achicar el elemento solo cambia SIZE.
- Al escalar el radio (R) manteniendo T fijo → los tubos se ven más finos relativos → escalar T también (~mismo factor) para preservar el grosor del master.
- Cadena de radios apretada (texto < anillo interior < arco < label exterior): para dar aire al centro, subir SIZE (espacio absoluto) + empujar el ring afuera coordinadamente. Texto en px fijo ocupa más en canvas chico que en el proto de 600px → en mobile el ring suele necesitar agrandarse vs el proto.

## I. Método de trabajo (validado orb + totem)
1. **Prototipo en WebGL** (OrbLab `*.html`, fragment shader GLSL ≈ SkSL-portable) servido con `python3 -m http.server`. Render con Playwright → screenshot. Iterar el feel con Ale a 10/10.
2. **Portar a RN** Skia: traducir GLSL→SkSL (B/A arriba), reusar el shader del orb donde aplique.
3. **Visual diff** master(proto) vs impl(sim screenshot) side-by-side. Cada elemento angular en su lugar (no solo colores).
4. **Sim reconnect** (Expo dev-client): `terminate` → `openurl nutriai://expo-development-client/?url=http%3A%2F%2Flocalhost%3A<PORT>` → esperar bundle → `openurl nutriai://<ruta>`. Si "Unmatched Route" o estado raro → Metro `-c` restart (re-escanea rutas). Verificar el PUERTO real del Metro (puede caer en 8082 si 8081 está ocupado).
5. `/matu light` con reviewers visuales OPUS (UI Designer + fitness-ux motion + a11y + Mobile App Builder). Ojo: pueden razonar sobre comentarios del shader y no cazar bugs de orientación → el ojo de Ale + el visual diff son el gate real.

## J. Reusables (no reinventar)
- `apps/mobile/components/AlexiaOrbSkia.tsx` — shader del orb (vidrio/fresnel/breathing). Base del orb-guía.
- `apps/mobile/components/dashboard/CaloriasTotemV2.tsx` — patrón COMPLETO: SkSL + Reanimated uniforms (worklet-safe) + ignición + focus-pause + reduce-motion + a11y + cold-state.
- Prototipos: `~/Documents/NutricomAI_OrbLab/{orb,ring,totem}.html`.

---

## K. Técnicas avanzadas (William Candillon + shader art IQ/Kishimisu) — rings, orb-guía, glass dome

### K.1 Glass / frosted / refracción
- **Frosted card barato (sin shader):** `<BackdropBlur blur={12} clip={rect}>` + RoundedRect `rgba(255,255,255,0.08)` + borde con LinearGradient `rgba(255,255,255,0.3)→0.05`. ⚠️ BackdropBlur NO captura ScrollView ni contenido fuera del Canvas → si el fondo es scroll, `makeImageSnapshotAsync()` del fondo fijo y pasalo como textura al shader.
- **Refracción real (domo de cristal):** `RuntimeShader` como ImageFilter sobre el Group del totem. `uniform shader image` (el contenido detrás) → normal de esfera fake → `image.eval(pos + N.xy*refractStrength)`. Snippet:
```
float2 p = uv/DOME_R; float z = sqrt(max(0.0,1.0-dot(p,p))); float3 N = normalize(float3(p,z));
half4 content = image.eval(pos + N.xy*0.08*(1.0-z)*minRes);   // más refracción en bordes
float fresnel = 0.04 + 0.96*pow(1.0-z, 5.0);                  // Schlick (vidrio n=1.5)
float spec = pow(max(0.0,dot(N, normalize(float3(0.3,0.8,1.0)))), 32.0);
col = mix(content.rgb, emerald*0.6, fresnel*0.5) + spec*0.4;
```
- **Alternativa barata (overlay decorativo):** Circle + RadialGradient transparent→white en el borde + BlurMask inner + BlendMode "screen". Da "vidrio" sin refracción.

### K.2 Bloom sin postprocessing
- **BlurMask** en círculos/paths: `<BlurMask blur={30} style="outer"/>` = glow puro (outer/normal/solid/inner). El `blur` acepta SharedValue (animar con Reanimated).
- **Bloom multicapa** = mismo elemento 3× en un Group con `blendMode="screen"`: base + blur15 + blur40/op0.4. "screen" acumula luz sin saturar = bloom real. 3 draw calls, OK en gama baja.

### K.3 Trail / comet del orb-guía
- El camino = `Skia.Path` (la bezier de la sección 5 de motion-playbook). Render `<Path path={trail} start={tail} end={progress} style="stroke">` con SweepGradient color→transparent. La cola sigue: `tail.value = withDelay(80, withTiming(progress.value))`.
- Cabeza luminosa: `useDerivedValue(() => path.getPoint(progress.value))` → Circle + BlurMask outer (r8 blur18) + aura (r16 op0.3 blur30), BlendMode "plus".
- **DashPathEffect** con `phase` animado = luz corriendo por un cable (barato). `getPosTan(t)` (PathMeasure) da {x,y,angle} a lo largo del path para gradientes por segmento.

### K.4 Noise barato — usar el builtin, NO fbm custom en gama baja
- En vez de escribir fbm en SkSL (loop + texture evals = caro): pasar `<FractalNoise freqX={0.04} freqY={0.04} octaves={3}/>` o `<Turbulence/>` como **child shader** → `uniform shader noiseMap; ... noiseMap.eval(uv)` = todo el fbm precalculado por Skia en 1 eval. `<DisplacementMap channelX="g" channelY="a" scale={20}>` + Turbulence = ondulación/plasma sin SkSL custom.

### K.5 SDF 2D (rings perfectos, AA sin fwidth) · IQ
```
float sdRing(float2 p, float r, float th){ return abs(length(p)-r) - th*0.5; }   // signed dist al ring
float aa(float d){ return 1.0 - smoothstep(-u_px, u_px, d); }                     // u_px = 1.5/minRes desde JS
float smin(float a, float b, float k){ k*=4.0; float h=max(k-abs(a-b),0.0)/k; return min(a,b)-h*h*k*0.25; } // metaballs/liquid
```
Glow gaussiano barato sobre un SDF: `exp(-12.0*abs(d))` (1 sample, sin branch). Outer glow: `exp(-4.0*max(d,0.0))`.

### K.6 Liquid-fill esmeralda (rings) — advección fake, NO Navier-Stokes
- fbm animado en coords POLARES (fluye a lo largo del ring) + comet head gaussiano en el frente del fill + step por ángulo para la parte llena. Núcleo:
```
float ang = atan(uv.y,uv.x)/6.2831 + 0.5;            // 0..1
float inFill = step(ang, u_fill);
float2 polar = float2(ang*3.14159, (length(uv)-R)*20.0);
float energy = fbmAnimated(polar + float2(iTime*0.8,0.0), iTime);
float dHead = abs(atan(uv.y,uv.x)+3.14159 - u_fill*6.2831); dHead = min(dHead, 6.2831-dHead);
float comet = exp(-dHead*dHead*20.0)*inFill;
float3 col = mix(emerald*0.3, emerald, energy)*inFill + mix(emerald,float3(0.3,1.0,0.8),0.4)*comet*2.5;
```
- Flow direction = tangente al círculo (`float2(-uv.y,uv.x)`) + perturbación noise → desplazar las UVs del fbm = "empuja" como fluido.
- **Cosine palette (IQ)** para gradientes esmeralda→teal→cyan: `a + b*cos(6.2831*(c*t+d))`.

### K.7 Performance Adreno 610 (barato → caro)
- **BARATO (60fps seguro):** BlurMask en shapes simples · Gradients (linear/radial/sweep) · Path.trim + DashPathEffect · SharedValue→uniform · FractalNoise/Turbulence builtin (octaves 2-3) · DisplacementMap · SDF ring + `exp()` glow (1 eval) · BackdropBlur en región <200px estática · BlendMode screen/plus · Atlas API para partículas en batch.
- **CARO/EVITAR:** framebuffer reads (backdrop sobre canvas grande) · **dynamic branching divergente** (mover la condición a uniform) · **loops con bound variable** (SIEMPRE `for(int i=0;i<5;i++)` literal, NUNCA `i<numOctaves`) · transcendentales (sin/cos/exp/log) en cadena · `discard` (mata Early-Z → usar alpha=0) · raymarching 3D · >2 niveles de domain-warp · >4-5 texture evals/fragmento · >6 octavas fbm.
- **mediump 2× más rápido** en Adreno 610: `half`/`half4` para color+noise, `float` para coords/distancias. Evitar cast implícito float↔half (8 instrucciones de más).
- Regla: lo que en Shadertoy/WebGL requiere multi-pass o FBO NO corre bien → mantener single-pass, compositar con BlendMode en el mismo Canvas.

### K.8 Recursos
- **William Candillon** "Can it be done in RN?": canal `youtube.com/@wcandillon` · repo `github.com/wcandillon/can-it-be-done-in-react-native` · Liquid Glass `youtube.com/watch?v=qYFMOMVZoPY` · SDF of a Line `=KgJUNYS7ZnA` · Gradient along Path (trail) `=7SCzL-XnfUU` · Glassmorphism `=ao2i_sOD-z0` · liquid-glass-rn-skia `github.com/alexandrius/liquid-glass-rn-skia`.
- **Kishimisu** "Intro to Shader Art Coding" `youtube.com/watch?v=f4s1h2YETNY` + shadertoy `view/mtyGWy` · **The Art of Code** (raymarching/SDF) · **Inigo Quilez** iquilezles.org (2D SDF `/distfunctions2d`, fbm `/fbm`, domain warp `/warp`, smin, palettes).
- **Skia playground** (testear SkSL sin RN): `shaders.skia.org` · docs RuntimeShader/ImageFilter de react-native-skia · Qualcomm Adreno best-practices.

---

## L. Liquid Glass (iOS 26) — el orb/domo al estado del arte 2026

Apple "Liquid Glass" (WWDC25) = el techo del glass HOY. NO es blur+opacidad: es **lensing real**
(refracción por displacement, no ray-trace) + **specular que responde al giroscopio** + **aberración
cromática** + **sombra adaptativa al contenido** + tint que lee el fondo. Lo que lo separa del
glassmorphism 2021 (frosted plano) es el lensing y la adaptividad.

**Lensing en SkSL** (refracción de Snell simplificada · el diferencial real):
```
// dentro del shape (SDF), desplazar las UVs del fondo segun la pendiente de una lente convexa
float slope = (1.0-t)/sqrt(1.0-(1.0-t)*(1.0-t));        // t = dist normalizada al borde (0 centro,1 borde)
float bend  = slope * (1.0 - 1.0/IOR) * radius * 0.5;   // IOR 1.3-1.5 (vidrio)
float2 disp = uv - dir*bend;                            // dir = gradiente del SDF (hacia afuera)
half4 bg = image.eval(disp);                            // fondo refractado
// aberracion cromatica (prisma): 3 samples con IOR levemente distinto por canal
// + specular Schlick (pow(1-cosθ,5)) · el lightDir puede venir del giroscopio (expo-sensors DeviceMotion)
// + grain sutil: fract(sin(dot(uv,float2(12.9898,78.233)))*43758.5453)*0.06
```
Repo de referencia: `github.com/alexandrius/liquid-glass-rn-skia` (de Shadertoy 3cdXDX). iOS 26 nativo: `@callstack/liquid-glass` (solo iOS≥26; Android = View opaca).

**⛔ Reglas duras (de los errores de Apple):**
- **Glass para IDENTIDAD, sólido para DATOS.** Apple llevó glass a todo → backlash de contraste (medido 1.5:1 vs WCAG 4.5:1). letsdev.de: "evitar glass en apps de salud con datos críticos". En NutricomAI el glass vive en el orb/domo/nav/celebración; las MÉTRICAS (kcal, macros, %, scanner, formularios) van sólidas sobre `#050505`. Nunca al revés. (Refuerza dataviz-tca-safe.)
- **⛔ NO glass-on-glass:** el shader de refracción samplearía otro shader, no el contenido → artefactos + GPU doble.
- **Perf:** el backdrop/lensing lee el framebuffer = +5ms en Adreno TBDR (perf-profiling-playbook). Máx 2-3 capas glass por pantalla. En gama baja: lensing solo en el orb (1 elemento), fallback blur estático en nav. `expo-sensors` giroscopio → uniform: vale en el ORB (1 elemento) si mide bien; ⛔ NO en toda la UI (laggy gama baja).
- **Dirección NutricomAI = "Glass Esmeralda" propio**, no copia de Apple: orb/domo con lensing+specular+grain (el showcase del material), resto sólido alta-legibilidad. Esa tensión glass-lujo / datos-austeros es intencional y TCA-safe.

> ⛔ Gotcha de color (New Arch): para animar color que va a un Canvas/shader usar **`interpolateColors` de @shopify/react-native-skia**, NUNCA `interpolateColor` de Reanimated (salta a negro). Ver newarch-gotchas.

---

## §3D-FAKE PREMIUM — totem/cockpit world-class en Skia (estudio Candillon + R3F · 2026-06-07)

> Estudio de 5 videos Candillon (3D transforms `pYu3DiWYtL0` · Liquid Glass `qYFMOMVZoPY` · Activity Rings `5-95kYTJMb4` · Neumorphism · Glassmorphism) + Maxime Heckel / Three.js Journey + viabilidad R3F-RN. Pedido Ale para llevar el totem RN a 10/10. Crudos en `~/yt` (copyright · NO commitear).

**⛔ VEREDICTO ARQUITECTURA — R3F / Three.js en RN = NO (descartar):**
- `pmndrs/native` README oficial: "DO NOT USE YET. Unstable, incomplete, probably broken." expo-gl con perf issues reconocidos por los maintainers. Simulador iOS = `EXC_BAD_ACCESS` por OpenGL ES incompleto (por eso un mockup R3F nunca rinde en sim — confirmado con el mockup D de Mi día). Adreno 610 = el bridge JS→OpenGL come los 16ms. WebGPU-RN (`react-native-wgpu`) = experimental, prod 2027+.
- **El 3D real-time en RN va por SKIA** (corre en render thread, sin bridge, ~200% faster vs CPU) **o pre-render** (video/atlas). NUNCA R3F en gama baja.

**Camino A — Skia 2.5D (elevar `CaloriasTotemV2` que YA existe):**
- **3D fake:** `processTransform3d([{rotateX},{rotateY},{perspective:800}])` → `Matrix4`, en worklet (`useDerivedValue`). Pivot correcto: translate-al-centro → matrix → translate-vuelta. ⛔ Gotchas: la matrix de Skia es row-major, SkSL espera column-major → TRANSPONER antes del `uniform mat4`. + y-flip Skia (ya resuelto `5a08fe67`).
- **Profundidad fake:** Z proyectado `(matrix*vec4(pos,0,1)).z` → normalizar −R..R→0..1 → modula specular/blur (frente nítido+brillante, lateral oscuro). El blur por-Z con `BlurImageFilter` NATIVO (⛔ nunca blur manual en SkSL).
- **Material metálico (bisel/specular sin env map):** SDF del anillo `abs(length(uv-c)-R)-halfStroke` → normal por gradiente del SDF → `pow(max(dot(N,L),0),32)` con `lightDir` fijo. O(1)/píxel, 60fps Adreno 610. ⛔ NO `BoxShadow inner:true` (Candillon textual: "extremely slow on low-end").
- **Arco progreso:** `path.addCircle` + `trim(0,progress)` con `usePathValue` + `withSpring`; `SweepGradient` mismo-hue; head dot con `path.getLastPoint()` (sin trig); sombra del head = `BoxShadow` outer + clip rotado (unidireccional).
- **Los 5 ingredientes de lujo que SÍ corren en Skia** (de los 9 del 3D-web premium): (1) **fresnel rim glow** — gradiente radial, el aro brilla esmeralda en los bordes (máx impacto / costo cero); (2) **gradiente metálico direccional** pseudo-matcap — highlight frío arriba, midtone, warm abajo = acero sin HDRI; (3) **contact shadow** — elipse `MaskFilter blur`, sigma ∝ elevación; (4) **bloom en capas** — arco en capa `BlendMode.Plus` + blur leve = fake HDR emission; (5) **cámara que vive** — spring sutil `useSharedValue` → touch/giroscopio, el totem respira.
- **Olvidar (necesitan GPU 3D real):** transmission física, HDRI reflections reales, depth-of-field dinámico. Matcap + fresnel dan ~60-80% del lujo a costo cero.

**Camino B — Pre-render (máximo realismo, 0ms JS):**
Three.js headless / Blender → render del aro girando/llenándose 1 vez → MP4 H.264 (idle loop + clip fill) → RN `expo-av Video repeat` + números como `Text` nativo en overlay absoluto (nítidos, accesibles, data-driven). GPU decodifica H.264 en HW fixed-function (3-5x más eficiente que shader en gama baja · ~200-400KB · sin init WebGL ~300-500ms). Mejor para "momento hero" NO interactivo. Contra: el fill del arco deja de ser live (es video).

**Recomendación NutricomAI:** **Camino A (Skia 2.5D sobre `CaloriasTotemV2`)** — ya existe, y-flip resuelto, data-driven en vivo; las 5 técnicas lo suben a 10/10 sin nueva infra ni pelear hardware. Pre-render (B) reservar para splash / celebración hero pre-determinada. Cero R3F.

