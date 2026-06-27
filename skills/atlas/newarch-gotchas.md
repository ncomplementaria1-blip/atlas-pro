# New Architecture Gotchas — Skia + Reanimated 4 + Rive (Expo SDK 54 / RN 0.81 / Fabric)

> Destilado de research 2026-06-01. el proyecto YA corre en New Arch (fabric:true). Consumir ANTES de
> construir cualquier elemento Skia/Reanimated/Rive. Las trampas que crashean o lagean, con la causa.

## Versiones que DEBEN coincidir (SDK 54 + New Arch)
| Lib | Versión | Nota |
|---|---|---|
| `@shopify/react-native-skia` | **2.2.3** | New Arch obligatorio · RN ≥0.79 |
| `react-native-reanimated` | **4.1.0** | New-Arch-only (no corre en Paper) |
| `react-native-worklets` | **0.5.x** | dep SEPARADA · DEBE matchear el native bundled (mismatch JS/native = crash explícito) |
| `rive-nitro-react-native` | latest | ⛔ NO el legacy `@rive-app/react-native` (roto en SDK 54) |
| `react-native-nitro-modules` | ≥0.33.2 | peer de Rive Nitro |
| `react-native-gesture-handler` | ≥2.x | usar su Pressable si activás SYNC_UPDATE flags |

## ⛔ WORKLET CRASH (abort trap 6) — la causa profunda
Hermes corre **DOS runtimes**: RN Runtime (JS thread, React/state) y UI Runtime (worklets). El Babel
plugin serializa funciones con `'worklet'` al UI Runtime. Llamar SÍNCRONO una función NO-worklet desde
el UI Runtime → su bytecode no existe ahí → SIGABRT (abort 6, crash NATIVO, no redbox).
- **El `'worklet'` NO se hereda:** si A es worklet y llama a B, B también necesita `'worklet'`. Marcá tus propios helpers de math (clamp, ease, lerp).
- **Capturable en worklet:** primitivos, arrays/objetos planos (copia), SharedValues, otras funciones-worklet, Math.*.
- **NO capturable:** funciones de libs sin `'worklet'` (date-fns, lodash, **`interpolateColor` de Reanimated**), NativeModules, objetos con prototipos.
- Fix: precalcular en el RN Runtime (`useMemo`/`useEffect` → SharedValue) y el worklet solo toca primitivos/SharedValues. (= nuestro fix del totem.)
- API Reanimated 4: `runOnJS(fn)(a,b)` → **`scheduleOnRN(fn, a, b)`** (args directos). `runOnUI` → `scheduleOnUI`.

## ⛔ Otros gotchas que rompen
1. **`interpolateColor` (Reanimated) con props de Skia → colores saltan a negro.** Usar SIEMPRE **`interpolateColors` de `@shopify/react-native-skia`** para color que va a un Canvas/shader.
2. **NO habilitar React Compiler** (issue #6826): hoistea el callback fuera del contexto worklet → "non-worklet on UI thread" crash. No es default en SDK 54 — dejarlo así.
3. **NO duplicar el babel plugin:** `babel-preset-expo` ya incluye reanimated/worklets plugin. Agregarlo a mano → crash "Cannot read property 'create' of undefined" en FlatList.
4. **Props Registry bloat (jank que crece):** Fabric clona TODO shadow node que alguna vez usó `useAnimatedStyle` mientras esté montado. El Muro/FlatList con animaciones degrada con el tiempo. FIX (activar ahora en package.json, requiere rebuild nativo):
   ```json
   "reanimated": { "staticFeatureFlags": { "USE_COMMIT_HOOK_ONLY_FOR_REACT_COMMITS": true } }
   ```
   (on por default recién en Reanimated 4.3+; RN ≥0.80 requerido.)
5. **Skia SDK 54 bug** `Property 'SkiaViewApi' doesn't exist` (expo #39277, ordering del import): workaround = importar el módulo Skia en un archivo extra temprano.
6. **Rive:** `@rive-app/react-native` legacy = build fail Kotlin en SDK 54. Usar `rive-nitro-react-native` (Nitro = New Arch, 15-59× más rápido). Testear en **release build Android físico** desde el inicio (los errores de release son crípticos).
7. **NO animar layout props** (width/height/flex) con `useAnimatedStyle` en UI thread → recálculo de layout cada frame = jank. Animar transform/opacity.

## Lo que Fabric DA (aprovechar)
- Skia migró a immutable display list → **+50% FPS iOS, ~+200% Android** + diffing por nodo (cambiar 1 uniform = solo actualiza ese uniform en GPU, no re-renderiza el Canvas).
- Commit hook inyecta props animadas en el shadow tree SIN bridge → Skia + Reanimated a 60-120fps sin tocar JS thread.
- **El contenido interno del Canvas Skia bypasea Fabric**: pasar SharedValues como uniforms/props a lo de adentro del Canvas = 0 JS thread en el loop.
- Concurrent rendering: los gestos (alta prioridad) interrumpen animaciones de fondo → el input del usuario siempre gana.

## Patrones HACER
- Shader con tiempo: `useClock()` (Skia) + `useDerivedValue(()=>{ 'worklet'; return {iTime: clock.value/1000, ...uniforms} })` → pasar como `uniforms`. (= patrón del totem/orb, validado.)
- Física/simulación: `useFrameCallback((f)=>{ 'worklet'; ... }, true)` wrapeado en `useCallback`.
- Color animado en Canvas: `interpolateColors(progress.value, [0,1], ['#a','#b'])`.
- Celebraciones: `rive-nitro-react-native` + confirmar `react-native-nitro-modules` en el build.

Refs: Reanimated migration/feature-flags/worklets-troubleshooting docs (swmansion) · Rive Nitro README · expo #39277 · reanimated #6826/#7480/#8235.
