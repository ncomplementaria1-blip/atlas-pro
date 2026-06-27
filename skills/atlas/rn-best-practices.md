# RN Best Practices · ecosistema (Callstack + Expo + gigs-slc 130+) · 2026-05-31

> Reglas RN oficiales/autoritativas que COMPLEMENTAN nuestro tooling interno (#0j/#0k/#0m).
> Las consumen los **reviewers RN de `/matu`** (criterio de review) + **`/implementar`** (regla de implementación).
> NO duplican lo nuestro (layout determinístico, anti-patterns fontFamily+fontWeight/Pressable-array, tokens master-driven, pixelmatch).
> NO chocan con master-driven (el diseño viene del master aprobado · estas son reglas de PERFORMANCE/CORRECTNESS de código, no de diseño).

## React Compiler (perf · -4.3% TTI medido)
1. **Instalar `babel-plugin-react-compiler`** (Expo 54+ · `npx expo install`). Reemplaza memo/useCallback/useMemo automático. Gotcha: si hay violaciones del eslint-plugin, el componente se salta SIN error → verificar badge "Memo ✨" en DevTools. → REVIEW: flagear memo/useCallback manual si Compiler activo.
2. **Reanimated con Compiler: `.get()`/`.set()` en shared values, NUNCA `.value`** fuera de worklets — `.value` excluye el componente de la optimización sin warning. → REVIEW: flag `.value` fuera de worklet.
3. **Destructurar funciones al inicio del render** (`const { push } = router`), no `router.push()` inline en callbacks — el Compiler no memoiza referencias en cadena de objetos. → REVIEW: flag `router.X()`/`navigation.X()` inline.

## State (perf)
4. **Estado global frecuente: Jotai/Zustand con selectores, NO React Context.** Context re-renderiza TODOS los consumidores en cada cambio. → REVIEW: flag `useContext` con objeto mutable de alta frecuencia. IMPL: migrar plan/perfil/sesión.
5. **State = verdad semántica (`pressed`/`isOpen`/`progress`), nunca valores visuales** (`scale`/`opacity`/`translateY` se DERIVAN via `interpolate`). Aplica a useState y useSharedValue. → REVIEW: flag estado con nombres de props CSS.
6. **Scroll position NUNCA en useState** (dispara decenas de veces/seg) → `useSharedValue` + `useAnimatedScrollHandler` (UI thread, cero re-renders) o `useRef`. → REVIEW: flag `useState` con `scrollY`/`scrollOffset`.

## Animación (perf · 60fps)
7. **Press animations: `GestureDetector` + `Gesture.Tap()` + worklets, NO `Pressable.onPressIn/Out`** (corre en UI thread sin roundtrip al JS thread). → REVIEW: flag lógica de animación en onPressIn/Out.
8. **Animar SOLO `transform` y `opacity`, NUNCA layout** (`width`/`height`/`top`/`left`/`margin` recalculan layout cada frame). Expansión/colapso = `scaleY`/`translateY`, no `height`/`top`. → REVIEW: flag `useAnimatedStyle` que retorna height/width/top/left animados.
9. **`useDerivedValue` para derivar de shared values; `useAnimatedReaction` SOLO para side effects** (haptics/runOnJS/log), no para derivar. → REVIEW: flag useAnimatedReaction que retorna/asigna shared values.

## Listas (perf · memoria)
10. **FlashList/LegendList, NUNCA ScrollView + `.map()`** (ScrollView monta todo upfront). Listas heterogéneas (ej. Registro Muro): `getItemType` con discriminated unions. → REVIEW: flag ScrollView+.map >5 items o lista heterogénea sin getItemType.
11. **List items: pasar SOLO primitivos como props** (`id`/`name`/`price`) — props de objeto = referencia nueva siempre → `memo()` nunca skippea. Derivar adentro del hijo. Callbacks: 1 `useCallback` en el padre con id como arg. → REVIEW: flag props objeto en componente con memo().
12. **`expo-image`, NO el `Image` nativo de RN** (blurhash, `cachePolicy:"memory-disk"`, `priority`, `contentFit`). Crítico en fotos de comida/avatares. → REVIEW: flag `import { Image } from 'react-native'`.
13. **Imágenes en listas: pedir 2× el tamaño de display, no full-res** — Cloudinary ya soporta (`w_200,c_fill`). → REVIEW: flag URL Cloudinary sin resize en contexto de lista (Registro Muro).

## Native UI (Expo · iOS feel)
14. **Fuentes: `expo-font` config plugin en app.json (build-time), NO `useFonts`/`Font.loadAsync`** (evita FOUT + estado de loading en cada arranque). Nosotros usamos Plus Jakarta Sans con useFonts → migrar. → REVIEW: flag `useFonts()`.
15. **Navegación: `native-stack` (default expo-router) + `NativeTabs`/`react-native-bottom-tabs`, NO los JS-based** (`@react-navigation/stack`, `@react-navigation/bottom-tabs`). → REVIEW: flag imports JS-based.
16. **Modales: `<Modal presentationStyle="formSheet">` o RN-Navigation `presentation:'formSheet'`, NO bottom-sheets JS** (swipe-dismiss + keyboard avoidance + a11y nativos gratis). → REVIEW: flag bottom-sheet de terceros / modal custom.
17. **`collapsable={false}` en wrappers de componentes nativos con conteo exacto de hijos** (TabBar, etc.) — Fabric flattening elimina layout-only views agresivo → bug silencioso. → REVIEW: flag wrapper de native component sin collapsable={false}.

## Bundle / Build (TTI)
18. **Prohibido barrel exports** (`import {A} from './components'` bundlea TODO) → import directo (`./components/A`; `date-fns/format` no `date-fns`). ESLint `no-barrel-files`. → IMPL + REVIEW: flag import desde index sin path.
19. **Android Hermes mmap: `noCompress += ["bundle"]` en build.gradle** (RN<0.79 · -16% TTI · requiere `expo prebuild`). → IMPL one-time (verificar versión RN).

## Rendering safety (CRASH prevention · ley)
20. **`{count && <X/>}` con falsy (0, "") → CRASH en prod** (RN intenta renderizar `0` fuera de `<Text>`). Usar `{count > 0 && ...}`, `{!!count && ...}`, o ternario con null. ESLint `react/jsx-no-leaked-render`. → REVIEW obligatorio + CLAUDE.md ley global. Causa crashes silenciosos con data vacía del backend (contadores macros, listas vacías).

### Bonus (monorepo)
- **Deps nativas SIEMPRE en el package.json del APP**, no solo en paquete compartido (autolinking solo escanea node_modules del app · si no, falla runtime silencioso).

---
Fuentes: [Callstack agent-skills](https://github.com/callstackincubator/agent-skills) · [gigs-slc react-native-skills (130+)](https://github.com/gigs-slc/react-native-skills) · [Callstack blog](https://www.callstack.com/blog/announcing-react-native-best-practices-for-ai-agents) · [Expo Skills](https://docs.expo.dev/skills/)
