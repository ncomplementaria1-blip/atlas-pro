# Haptics Playbook — el feel físico (el 50% del wow que no se ve)

> Destilado de research 2026-06-01. Consumir al agregar feedback táctil. `expo-haptics` (SDK 54).
> Regla de oro: **si lo dudás, no pongas haptic. 3 bien diseñados > 20 mediocres.** Haptic acompaña
> SIEMPRE un cambio visual, nunca solo. Frecuencia inversa a importancia.

## Vocabulario
- **iOS impact** (respuesta a gesto): `light` (chips/tap), `medium` (cards/FAB · default), `heavy` (destructivo confirmado), `soft` (elástico/toggle), `rigid` (snap/lock/encaje).
- **iOS notification** (outcome, NO input): `success` (guardado/scan OK), `warning` (validación falla), `error` (rechazo real).
- **iOS selection**: cambio de selección discreta (picker, segmented · NO scroll libre).
- **Core Haptics** (patterns custom): transient (impulso, intensity+sharpness) / continuous (sostenido +duration). sharpness 0=rumble orgánico, 1=click mecánico.

## ⛔ Realidad Android gama baja (Snapdragon 680)
- Mayoría = actuador **ERM** (no LRA) → `light`/`medium`/`heavy` se sienten IGUAL (mismo motor). NO diseñar capas de intensidad asumiendo diferenciación.
- **Usar `performAndroidHapticsAsync(AndroidHaptics.*)`** (SDK 54, sin permiso VIBRATE, más suave, semántico: `Keyboard_Press`, `Virtual_Key`, `Toggle_On/Off`, `Gesture_End`, `Confirm`, `Reject`) — mejor que `notificationAsync` en Android.
- ⛔ NO custom patterns en Android (ERM hace buzz largo desagradable). Si el haptic SUENA (ruido mecánico) → está muy fuerte.

## Timing (≤20ms de desfase es imperceptible; >30ms se nota)
- Press = haptic en **`onPressIn`** (coincide con el scale-down), NO en `onPress`.
- Outcome (registro/scan) = haptic DESPUÉS del `await` de la acción real (en el éxito, no en el press).
- ⛔ `expo-haptics` corre en JS thread; `runOnJS`/`scheduleOnRN` desde worklet es async → puede llegar 1-2 frames tarde. Para el aterrizaje del orb-guía usar `useAnimatedReaction` con threshold (no `onEnd`):
  ```
  useAnimatedReaction(() => Math.abs(orbX.value-targetX)<8 && Math.abs(orbY.value-targetY)<8,
    (near, was) => { if (near && !was) runOnRN(nutri.orbLand); });
  ```

## Hook reutilizable (el proyecto · directo a `src/hooks/useHaptics.ts`)
```ts
import * as Haptics from 'expo-haptics'; import { Platform } from 'react-native';
const isAndroid = Platform.OS === 'android', isWeb = Platform.OS === 'web';
const safe = (fn: () => Promise<void>) => { if (isWeb) return; fn().catch(() => {}); }; // nunca throw/bloquea
export const nutri = {
  pressCard: () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Keyboard_Press) : Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)),
  pressFAB:  () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Virtual_Key)   : Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)),
  toggleOn:  () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Toggle_On)     : Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft)),
  toggleOff: () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Toggle_Off)    : Haptics.selectionAsync()),
  orbLand:   () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Gesture_End)   : Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft)),
  success:   () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Confirm)       : Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)),
  warning:   () => safe(() => isAndroid ? Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Reject)        : Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning)),
  celebrate: () => { if (isWeb) return; if (isAndroid) safe(()=>Haptics.performAndroidHapticsAsync(Haptics.AndroidHaptics.Confirm));
    else { safe(()=>Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)); setTimeout(()=>safe(()=>Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)),100);} },
};
```

## Vocabulario el proyecto (momento → haptic)
| Momento | iOS | Android | Cuándo |
|---|---|---|---|
| Press card | Light | Keyboard_Press | onPressIn (solo si hay acción) |
| Press FAB (registro) | Medium | Virtual_Key | onPressIn |
| Toggle on/off | Soft / selection | Toggle_On/Off | onValueChange |
| Orb-guía aterriza | Soft | Gesture_End | threshold nearTarget |
| Registro/scan OK | success | Confirm | tras el await del backend |
| Scan falla / validación | **warning** (NO error) | Reject | en el frame del error |
| Primer logro / celebración | Light→100ms→Medium (≤2 pulsos, ≤200ms) | Confirm | en el peak visual |

## ⛔ safe-para-datos-sensibles
- Celebración háptica = doble-tap **cálido y discreto** (Light→Medium), NUNCA secuencia dramática/fanfarria.
- NUNCA `.error` para "excediste calorías" → usar `warning` o nada. El haptic no debe "castigar".
- Cuándo NO: scroll libre · animaciones decorativas sin input · loops/timers · cada letra de texto · acciones sin cambio de estado.

Refs: Apple HIG "Playing Haptics" · `docs.expo.dev/versions/latest/sdk/haptics` · `performAndroidHapticsAsync` (expo PR #34077).
