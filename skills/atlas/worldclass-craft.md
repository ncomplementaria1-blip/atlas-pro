# World-Class Visual Craft — OVERLAY NutricomAI
> ⛔ BASE = `universal-craft-codex.md` (project-neutral · la vara 10/10 de ATLAS para CUALQUIER proyecto). **Este archivo es el OVERLAY de NutricomAI**: especializa el codex con el DNA del producto (esmeralda, TCA-safe, El Estanque, Plus Jakarta). El overlay nunca contradice el codex — lo concreta. Cargar SIEMPRE el codex primero; este archivo encima solo en sesiones NutricomAI.
> Consumido por /atlas (creative spin + 6G visual) y /matu (reviewers de diseño). Aplica a TODO output visual: mobile (Skia/RN), web (R3F/three.js), mockups, splash, onboarding, totems, orbs, rings, landing.
> Fuente completa: `~/Documents/NutricomAI_SplashOnboarding_Research_20260531/research_report_..._v2.{md,html}`.
> **Playbooks especializados (cargar el que aplique a la tarea):** `skia-sksl-playbook.md` (shaders Skia RN: gotchas, glass/Liquid-Glass, trail, liquid-fill, perf Adreno 610) · `motion-playbook.md` (math Freya + taste Emil/Rauno: durations, easing, bezier, anti-slop) · `dataviz-tca-safe.md` (rings/gauges premium + reglas TCA duras) · `rive-adoption.md` (onboarding/celebraciones) · `haptics-playbook.md` (feel físico · hook useHaptics) · `perf-profiling-playbook.md` (medir 60fps de verdad en gama baja) · `newarch-gotchas.md` (Skia/Reanimated4/Rive en Fabric · versiones + reglas anti-crash) · `gesture-choreography-playbook.md` (la física que separa "playback" de "vivo": snapPoint+velocity, follow-spring, withDecay/rubber-band, stagger, spring presets, perspective 3D · Candillon/Reactiive/Catalin/SWM) · `cinematography-playbook.md` (el DIRECTOR DE FOTO para VIDEO: composición/lente/movimiento-motivado/luz/grade/montaje/sonido + prompting cinematográfico generativo grok-cli + rúbrica 10/10 + anti-AI-slop · splash/orbe/totem/landing/ad). Todos en `~/.claude/skills/atlas/`.
> **Liquid Glass (iOS 26, el techo 2026):** glass = lensing real (refracción Snell) + specular giroscopio + grain, NO blur plano. ⛔ LEY: glass para IDENTIDAD (orb/domo/nav/celebración), SÓLIDO para DATOS (Apple tuvo backlash de contraste 1.5:1 — letsdev: "evitar glass en datos clínicos"). Detalle: skia-sksl-playbook §L.

---

## LEY 0 — La diferencia "AI básico" → "agency world-class" NO es más features
Es **realismo de material + luz real + movimiento de cámara cinematográfico + la imperfección de una lente real.** Si algo se ve "AI-generado", falló. Test: si alguien puede decir "esto lo hizo una IA" sin dudar → rehacer.

---

## 1. Stack de realismo 3D (web · three.js + react-three-fiber + drei) — las 6 palancas
1. **glTF real, no procedural** — modelos con UVs + normal maps bakeados. Compresión Draco+Meshopt+KTX2. `gltfjsx --transform`. `useGLTF.preload()`. (Excepción: una esfera + transmission + HDRI YA es foto-real para un orb — no necesita glTF.)
2. **HDRI real (Polyhaven CC0) + IBL = la palanca #1.** `<Environment files="*.hdr" environmentIntensity={1.8} background={false}>`. La luz real del entorno hace los reflejos creíbles; sin esto el cristal se ve sucio.
3. **Material:** orb de cristal → `MeshTransmissionMaterial` (drei): `transmission=1, ior=1.52, thickness, chromaticAberration=0.04, backside=true, attenuationColor`. Metal → PBR maps (`normalMap` = palanca #1 de microdetalle, ORM, `envMapIntensity=1.8`, `clearcoat` para lacado).
4. **Contact shadows** — `<ContactShadows frames={1} blur={3}>` (render-once, 0 runtime) o `<AccumulativeShadows temporal>` + `<RandomizedLight>`. Mata el "objeto flotando" (tell #1 de AI-básico).
5. **Tone mapping ACESFilmic** (default R3F) + `toneMappingExposure≈1.2`. Para esmeralda usar **AgX** si se ve fluorescente. NUNCA NoToneMapping/Linear.
6. **Color management** (R3F r139+ auto): color sRGB, datos (normal/rough) Linear.

## 2. Cinematografía (cámara 3D web acá · para VIDEO real → `cinematography-playbook.md`: el DIRECTOR de foto)
> Esta sección es la cámara/post en R3F. Para dirigir un VIDEO (splash pre-render, clip del orbe/totem in-app, hero landing, ad) — composición, lente, movimiento motivado, montaje, sonido, prompting generativo y la rúbrica 10/10 — consumir `cinematography-playbook.md`. El video se DIRIGE, no solo se genera.
- **La CÁMARA se mueve, no solo los objetos.** `<CameraControls>` (drei/yomotsu): `lerpLookAt`, `dollyTo`, `fitToSphere`. Parallax con `maath` `easing.damp3` (frame-rate-independent). Cámara a 60fps = refs mutables en `useFrame`, NUNCA React state. Secuencias: Theatre.js (timeline) o GSAP (easings custom). FOV cine 45-55°.
- **Post stack — ORDEN exacto** (`@react-three/postprocessing`): `N8AO → SelectiveBloom → DepthOfField → ToneMapping(ACES) → LUT → ChromaticAberration → Vignette → Noise(grain, ÚLTIMO)`. SelectiveBloom solo en emisivos (`toneMapped={false}`, `emissiveIntensity>1`). DOF como narrativa (foco guía el ojo).
- **"Lens character" = acumulación de imperfecciones.** chromatic (0.001-0.002) + grain (opacity 0.03-0.05) + vignette (0.55-0.7) + DOF. **Regla: si podés nombrar el efecto, está demasiado alto.**
- **Luz de 3 puntos:** ambient frío bajo + key cálido + rim cián atrás (amplifica bloom en el borde = halo de producto premium).

## 3. ⛔ LEY de viabilidad mobile (CRÍTICA — sin esto el plan es fantasía)
**El stack 3D real-time completo NO corre en React Native nativo (Adreno 610 / Snapdragon 680):**
- `@react-three/postprocessing` ROTO en native (`renderbufferStorageMultisample`): Bloom, SSAO, SSR, DOF, ChromaticAberration, grain, vignette = **web-only**.
- R3F native roto por `expo-gl@11` vs `@15` (SDK 53+). HDRI/IBL, KTX2/Draco, MeshTransmissionMaterial (glass), ContactShadows drei = rotos/costosos en native.
- Throttling térmico a los 2-3 min de GPU sostenida → nada 3D continuo en gama baja.

**Arquitectura híbrida (el wow que SÍ ships):**
| Superficie | Tech | Por qué |
|---|---|---|
| Splash (one-shot 2-3s) | **VIDEO pre-renderizado** (escena 3D completa offline → MP4 ~1MB, ffmpeg) | AAA idéntico en todo device, 0 costo runtime |
| Onboarding | Rive / Skia SkSL | 60fps real, interactivo, ~300KB |
| Totem/orb/rings in-app | **react-native-skia SkSL** (lo actual) | 60fps garantizado; vignette/grain/glow/DOF *fake* con blur de Skia |
| Landing web | **R3F real-time COMPLETO** | acá SÍ corre todo — escaparate Awwwards |

**Insight:** wow 3D en mobile = pre-render a video. wow interactivo = landing web. in-app = Skia/Rive que finge profundidad. Tres herramientas, una estética.

## 4. Skia/GPU craft mobile (orb + totem plasma-tube · prod 2026-05-31)
> Detalle técnico COMPLETO (sintaxis SkSL, worklet-safety, AA, bloom, ignición, perf, método, sim reconnect): **`skia-sksl-playbook.md`** — consumir SIEMPRE al construir/revisar un shader Skia RN.
- Todo el cluster en UNA SkSL RuntimeEffect (well + tubos plasma + anillo + viñeta/grano), no Paths emisivos: más barato + más control. Tubos = sección 3D (`1-0.5·across²`) + spine + plasma fbm quintico + inicio iluminado. Bloom = exp falloff (restraint). AA por `u_px` (sin fwidth). Disco transparente (compone sobre cualquier fondo).
- ⛔ 3 trampas que CRASHEAN/rompen: (1) el worklet de uniforms (`useDerivedValue`) NO puede llamar funciones JS no-worklet → **abort trap 6** (precalcular en `useMemo`); (2) **y-flip** WebGL→Skia (`uv.y=-uv.y`) o la geometría angular queda espejada vertical; (3) `{0 && <X/>}` crashea (usar ternario/`>0`).
- **Perf/batería:** focus-pause (`useIsFocused` → no leer el clock sin foco → el Canvas deja de invalidar). fbm 3-4 oct en continuo. `needs-apk-validation` siempre.
- Reduce-motion: cortar la invalidación del Canvas (no solo "verse fijo").
- Método: prototipo WebGL (OrbLab) → validar feel con Ale → portar a RN → visual diff master vs impl. El ojo de Ale caza lo que /matu no (ej. el y-flip).

## 5. Referentes (robar craft)
- **RN/Skia (in-app · #1):** **William Candillon — "Can it be done in React Native?"** (youtube.com/@wcandillon · co-autor de react-native-skia) — glass/refracción, trail, gestures, shaders Skia a 60fps en gama baja. → skia-sksl-playbook.
- **Motion:** **Freya Holmér** (@acegikmo · la math: bezier/splines/easing/lerp) · **Emil Kowalski** (emilkowal.ski · el taste) · **Rauno Freiberg** (rauno.me · interaction design). → motion-playbook.
- **Shader art:** **Kishimisu** ("Intro to Shader Art Coding"), **The Art of Code** (raymarching/SDF), **Inigo Quilez** (iquilezles.org / Shadertoy · 2D SDF, fbm, domain warp, palettes).
- **Health data-viz (TCA-safe):** WHOOP, Oura, **Gentler Streak**, **MacroFactor** (modelo no-shame). → dataviz-tca-safe.
- **3D/web:** Bruno Simon (threejs-journey.com), Yuri Artyukh (@akella_), Maxime Heckel, SimonDev, The Book of Shaders, Olivier Larose.
- **Estudios:** Lusion (lusion.co), Active Theory, **Basement Studio (Buenos Aires · LATAM)**, Aristide Benoist, Resn. **Rive:** Rive Masterclass (@RiveMasterclass).
- **Galerías:** Awwwards (collections/webgl + webgl-shaders-code con código), FWA, Godly (godly.website), Codrops.
- **Demo norte del orb:** Codrops "Vortex inside a glass sphere (TSL)".
- **Cómo estudiar a estos referentes en VIDEO (capacidad ADN · `youtube-study-playbook.md`):** FAZM "ve"
  videos vía `yt-dlp` (subtítulos = transcript) + `ffmpeg` (frames en contact-sheet, leídos como imagen).
  Autónomo: avisa qué videos va a estudiar y lo hace; crudos locales en `~/yt`, nunca commiteados (copyright).

## 6. Principios de gusto (taste · cross-proyecto)
- **Restraint = sofisticación.** El bloom/glow vive en la mitad-baja de su rango. Premium ≠ chillón.
- **TCA-safe siempre:** la luz es material/instrumento, no gamificación. Intensidad desacoplada del valor (no premio/castigo). Respiración = "encendido", no pulso de alarma.
- **DNA:** dark `#050505` · esmeralda `#059669/#34D399` · canales macro (carbo cyan/proteína magenta/grasa amber/fibra lima) · Plus Jakarta Sans + JetBrains Mono · cero emojis · cero gradientes genéricos.
- **Dirección in-app ESTABLECIDA (NutricomAI · binding 2026-06-07): EL ESTANQUE** — orbe/agua de cristal LÍQUIDO (cockpit-premium líquido). Caso probado: TOTEM (video Grok + react-native-skia useVideo + ColorMatrix luma→alpha · master `docs/mockups/mobile/totem-ideas/ESTANQUE-MASTER.html` · impl `EstanqueTotem.tsx` /matu PASS 9.59). Liquid Glass para IDENTIDAD, sólido para DATOS. Aplica a TODA pantalla — scope + stack + motion en `~/.claude/skills/atlas/projects/nutricomai/fullapp-estanque-brief.md`.
- **Copy producto:** español neutro tuteo (no voseo); comida chilena (papa, palta, choclo).
- **Para "wow" en gama baja: pre-renderizar.** No pelear contra el hardware en tiempo real.
