# Rive Adoption Playbook — onboarding + celebraciones (NutricomAI RN/Expo)

> Destilado de research 2026-05-31. Consumir cuando se implemente onboarding o los 7 micro-momentos/
> celebraciones. Rive = lógica interactiva de estados sobre vectores. NO reemplaza Skia para GPU/glass.

## 1. División clara: Skia vs Rive
| Elemento | Tool | Razón |
|---|---|---|
| Orb de cristal, totem, rings, glass | **Skia (SkSL)** | refracción/transmisión/shaders custom — Rive no tiene shaders ni materiales |
| Splash hero | Skia o **video pre-render** | máxima calidad one-shot |
| Onboarding (7 pasos) | **Rive** | states interactivos, responde a swipe/tap, lógica embebida |
| Celebraciones / "primer logro" / "plato se materializa" / "insight se revela" | **Rive** | one-shot trigger + auto-return, 60fps, archivo ~2-5KB |
| Micro-feedback de botones | Rive o Reanimated | |
> Conviven sin conflicto (renderers nativos independientes). ⛔ NO montar múltiples `RiveView` a la vez en Snapdragon 680 (cada uno = un thread de render). Una animación Rive activa por pantalla; las demás unmounted (no solo invisible).

## 2. ⛔ Runtime correcto (2026)
- **USAR `@rive-app/react-native`** (Nitro Modules, nuevo). Hooks: `useRiveFile`, `useRive`, `useViewModelInstance`, `useRiveNumber`, `useRiveTrigger`, `useRiveEvent`. Requiere RN 0.78+ / Expo SDK 53+ (SDK 54 = RN 0.81, OK). Componente `<RiveView/>`.
- ⛔ **NO usar `rive-react-native`** (legacy): ROTO en RN 0.80+ (Expo SDK 54 no compila, errores Kotlin). Sin mantenimiento.
- Setup Expo: `npx expo install @rive-app/react-native react-native-nitro-modules` + `expo-build-properties` (compileSdk 36, iOS 15.1) + `expo prebuild --clean` + development build (no Expo Go). NutricomAI ya usa `eas build` → encaja.
- Por qué Rive > Lottie: formato binario `.riv` 10-15× más chico (240KB Lottie → 16KB Rive); renderer propio multi-thread (NO Skia: lo sacaron en android v10) → 60fps vs 17fps de Lottie en gama baja (benchmark Callstack/Sony Xperia Z3). Costo: ~30MB más GPU memory.

## 3. State machines (el modelo mental)
- **ViewModels/data-binding** (nuevo, recomendado) en vez de Inputs legacy: el `.riv` expone propiedades (number/string/bool/color/trigger). El animador cambia la state machine interna SIN tocar código mientras el contrato de nombres no cambie.
- Estados: Animation / Blend-1D (mezcla por número, ej. intensidad de celebración) / Blend-2D / Any-State (interrupciones) / Exit.
- Triggers one-shot desde JS; Events de la animación → callback JS (ej. "terminé → navegá").

## 4. State machine ejemplo: "Primer logro" (<60s, TCA-safe)
```
[Idle] --triggerAchievement--> [Appear] (0.3s ease-out scale+opacity)
  --> [Bloom] (orb vectorial se expande + anillo de luz, 0.8s · Blend-1D por achievementType: esmeralda→amber)
  --> [Hold] (loop suave 2s, lee el mensaje)
  --> [Dismiss] (fade 0.4s) --onComplete event--> [Idle]
```
TCA-safe: el plato/orb aparece COMPLETO (no un contador que "se llena"); la celebración es sobre el reconocimiento/registro, NO sobre el valor calórico. Sin fanfarria de déficit.

## 5. Bugs conocidos / mitigaciones
- Scroll jank en Android release (rive-android 9.13+): pinear `rive-android:9.12.2` en build.gradle.
- Data-binding trigger en iOS dispara solo 1 vez: resetear el trigger a false desde JS antes de re-disparar.
- Data-binding a veces no arranca la state machine hasta el primer tap (issue #348): forzar un tick inicial o usar trigger directo.
- Nuevo runtime = early release: arrancar con un micro-momento simple sin riesgo + smoke en device gama baja ANTES de meterlo en onboarding crítico.

## 6. Plan de adopción (3 semanas)
1. PoC: botón 3 estados (idle→pressed→success), compila con `eas build --profile preview`, smoke FPS en device gama baja.
2. Celebración: confetti + ring de luz vectorial (sin mesh deform), state machine Idle→Bloom→Hold→Dismiss, disparar al 1er registro del día, verificar `onComplete`→JS.
3. Onboarding: 7 artboards en un `.riv`, boolean `isActive` por paso, controlado por el stepper existente.

## Recursos
- Docs: `rive.app/docs/runtimes/react-native` + `/adding-rive-to-expo` · GitHub `rive-app/rive-nitro-react-native`.
- YouTube: Rive Masterclass (@RiveMasterclass) · state-machine tutorial `youtube.com/watch?v=acbUvtjUZSY` · rive101.com.
- Community .riv (remixar): `rive.app/community/files/` (success-confetti, interactive-badge, like-heartbeat).
- Benchmark: Callstack "Lottie vs Rive".
