# Motion Playbook — math + taste (Freya Holmér · Emil Kowalski · Rauno)

> Destilado de research 2026-05-31. Consumir al diseñar/revisar CUALQUIER animación (Reanimated/Skia).
> Dos ejes: la MATEMÁTICA (Freya — que se sienta vivo) + el TASTE (Emil/Rauno — cuándo y cuánto).
> Regla maestra: **animar poco, que se sienta necesario. Si podés nombrar el efecto, está muy alto.**

---

## 1. DURACIONES REALES (la mayoría de las UI animations son demasiado largas)
- Micro-interacción (press, toggle, hover, badge): **100-150ms**
- UI estándar (tooltip, dropdown chico, chip): **150-250ms**
- Modal / sheet / drawer / transición de pantalla: **200-300ms**
- **Techo de TODA UI: 300ms.** (Excepción: hero one-shot — splash, orb-guía, ignición — hasta ~500ms.)
- **Exits 20% más rápidos que enters** (el usuario ya decidió salir).
- Stagger entre ítems de lista: **30-60ms** (>100ms = slideshow). Máximo 5-6 ítems staggered.

## 2. EASING — la decisión más importante (Emil)
| Caso | Easing | Por qué |
|---|---|---|
| Entra a pantalla | **ease-out** | rápido→decelera = respuesta inmediata |
| Sale de pantalla | ease-in | acelera hacia afuera |
| Se mueve A→B en pantalla | ease-in-out | objeto físico |
| Color/hover/no-posicional | ease default | |
| Loop constante (spinner) | linear | sin inicio/fin |
| **Default si dudás** | **ease-out** | siempre se siente responsivo |
- **ease-out-expo premium (Linear/Vercel/iOS):** `Easing.bezier(0.16, 1, 0.3, 1)`. La desaceleración asintótica nunca se siente como "freno". USAR para orb-guía, ignición, entradas hero.
- Otros: cards entrando `Easing.bezier(0.25,1,0.5,1)` · dismiss `Easing.bezier(0.4,0,1,1)` (ease-in).
- ⛔ NUNCA bounce/elastic en UI seria (el cerebro lo lee como juguete o bug). En NutricomAI = ansioso, anti-TCA.

## 3. SPRING vs DURATION
- **Spring** = todo lo que el usuario TOCA directo (press, drag, swipe). Preserva velocidad al interrumpir (crítico).
- **Duration+easing** = transiciones de estado NO gesture-driven (appear/disappear, color, skeleton→content).
- Spring se siente vivo; timing fijo se siente software.
- Apple WWDC23: **bounce=0** default (smooth). bounce 0.15 = "brisk/playful". bounce 0.30 = post-gesto físico. **>0.4 evitar.**
- Press premium: `withSpring(0.96, {damping:20, stiffness:300})` + haptic `ImpactFeedbackStyle.Light` en `onPressIn` (NO onPress, llega tarde). Cards: scale 0.96-0.97 (no 0.9, no 0.99). FAB chico: 0.93.

## 4. INTERRUPTIBILIDAD (ley no negociable · Rauno)
Toda animación touch-driven DEBE poder interrumpirse (el usuario cambia de opinión a mitad del swipe). Springs son interrumpibles y preservan velocidad; `withTiming` reinicia desde cero. Si una interacción no se puede interrumpir → se siente no-responsiva.

## 5. MATH DE FREYA (que se sienta vivo, no programado)
- **lerp / ilerp / remap** (el cuchillo suizo): `lerp(a,b,t)=a+(b-a)*t` · `ilerp(a,b,v)=(v-a)/(b-a)` · `remap` = componer ambos. Trabajar SIEMPRE en `t∈[0,1]`; la duración en ms es capa de presentación.
- **smootherstep (quintic, C2):** `t*t*t*(t*(t*6-15)+10)` — más cremoso que smoothstep cúbico. (Es el mismo quintic del fbm del totem.)
- **Bézier cuadrática (la curva del orb-guía):** `Q(t)=(1-t)²P0 + 2(1-t)t·P1 + t²P2`. El control point P1 = "la intención del movimiento". Para arco grácil: P1 = midpoint + perpendicular·(dist·0.3). En NutricomAI el arco SIEMPRE curva hacia el centro de pantalla (el orb "siente" la gravedad del contenido).
- **Splines Catmull-Rom (C1, pasa por los puntos)** para paths multi-waypoint. Para velocidad uniforme: arc-length param (samplear 100 puntos, distancias acumuladas, `interpolate()` progreso→t).
- **Squash-and-stretch al aterrizar (volumen conservado):** scaleX `1+s*0.18`, scaleY `1-s*0.15` (Y menor → "absorbido", no "aplastado"), `s=sin(local*π)`.
- **Respiración VIVA = frecuencias irracionales.** Un loop de 3.0s se ve programado. Sumar 2ª armónica de 7.0s (ratio 3/7) → el patrón tarda ~21s en repetir → el ojo lo lee orgánico. `sin(t*2π/3)*2.5 + sin(t*2π/7)*1.0`. Escala respiración ±1.5% (casi imperceptible, registrado inconsciente).
- **Exponential decay framerate-independent** (no `lerp(v,target,0.1)` que es frame-dependiente): `v = target+(v-target)*exp(-decay*dt)`, decay 3=flotante pesado, 8=snappy.

## 6. CUÁNDO ANIMAR (4 criterios · TODOS deben ser sí)
1. Responde a una acción del usuario (nunca autoplay).
2. Clarifica algo (orientación espacial, estado, causa-efecto).
3. Reduce carga cognitiva (no la añade).
4. Se ve ~1 vez por sesión / poco.
⛔ **NO animar lo de alta frecuencia** (registrar comida, marcar agua, teclado, navegar tabs, lista al cargar): una animación de 300ms en algo que se hace 100×/día = castigo acumulado. "Se sintió lenta después de días" (Rauno).

## 7. ANTI-AI-SLOP (señales de over-animación)
1. Duración >400ms fuera de un hero. 2. Bounce sin gesto de drag/throw. 3. Stagger >6 elementos. 4. >3 elementos animando simultáneo en una pantalla. 5. Animar acciones repetitivas. 6. Scale desde 0 (usar 0.85-0.90). 7. Animación que el usuario no disparó.

## 8. REDUCE-MOTION (no opcional · 35% de usuarios afectados por vestibular)
No eliminar la animación: reducir desplazamiento/escala (opacity fade en vez de slide). Cada animación con su ruta `prefers-reduced-motion`. `AccessibilityInfo.isReduceMotionEnabled()` / `useReducedMotion()`.

## 9. PRESETS NUTRICOMAI (Reanimated)
| Caso | Config | Duración |
|---|---|---|
| Orb-guía vuelo | `Easing.bezier(0.16,1,0.3,1)` (o spring `{stiffness:80,damping:18,mass:1.2}`) | 420-500ms |
| Ignición totem (stagger) | `Easing.bezier(0.16,1,0.3,1)`, stagger 60ms | 280-340ms |
| Cards entran | `Easing.bezier(0.25,1,0.5,1)` | 360ms |
| Press card | `withSpring(0.96,{damping:20,stiffness:300})` + haptic Light | spring |
| FAB aparición | spring `{duration:0.3,bounce:0.15}` | 300ms |
| Tab indicator | `withSpring({stiffness:400,damping:35})` | spring |
| Sheet (TCA-safe, sin bounce) | `withSpring({duration:0.4,bounce:0})` | 400ms |
| Dismiss | `Easing.in(Easing.quad)` | 280ms |
| Respiración orb | `useClock` + sin() irracional | continuo |

## 10. QUÉ ANIMAR vs NO en NutricomAI
SÍ: orb-guía (1ª vez + navegación), completar objetivo del día (suave, TCA-safe), registro confirmado→ítem aparece (spring 200ms), escanear→resultado (shared element), tab indicator, sheet de detalle.
NO: lista de alimentos al cargar (directo), texto de macros al actualizar, registro de agua (instantáneo), teclado numérico, todo el flujo de log de comida (alta frecuencia).

## Referentes
- **Freya Holmér** (@acegikmo): "Beauty of Bézier Curves" `youtube.com/watch?v=aVwxzDHniEw` · "Continuity of Splines" `=jvPPXbo87ds` · "Lerp Smoothing is Broken" `=LSNQuFEDOyQ` · Math for Game Devs playlist · Mathfs `github.com/FreyaHolmer/Mathfs`.
- **Emil Kowalski** (emilkowal.ski): "Great Animations" + "Good vs Great Animations" · curso animations.dev.
- **Rauno Freiberg** (rauno.me): "Invisible Details of Interaction Design" `rauno.me/craft/interaction-design` · UI Playbook uiplaybook.dev.
- Apple WWDC23 "Animate with Springs" · Vercel motionguide.vercel.app.
