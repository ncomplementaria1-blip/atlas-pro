# Gesture Choreography Playbook · la física que separa "playback" de "vivo"

> La última pieza world-class (binding · 2026-06-01). El diferenciador real entre "se ve lindo" (anima
> 0→1 al apretar) y "se siente VIVO" (responde al dedo: interrumpible, spring, momentum, rubber-band).
> Estudiado de: Candillon (gesture+cards), Reactiive (Gesture Handler 2 / chat-heads), Catalin Miron
> (pan+snap-back), Software Mansion (Reanimated 4). Stack: react-native-gesture-handler 2.x + reanimated 4.

---

## Principio (LEY)
- **Playback = muerto.** `onPress → withTiming(1)` reproduce una animación. El dedo no participa.
- **Vivo = la animación ES el gesto.** El valor lo maneja el dedo en tiempo real; al soltar, la FÍSICA
  (velocidad + spring/decay) decide dónde y cómo aterriza. Interrumpible en cualquier momento.
- safe-para-datos-sensibles: la física es para NAVEGACIÓN/feel, no gamificación. Nada de "premio" por gesto.

## Modelo de threads (no romperlo · ver newarch-gotchas)
- Todo el gesto + animación corre en **UI thread** (worklets) → 60fps sin tocar JS.
- Side-effects (analytics, "reproducí confetti", navegar) → **`runOnJS(fn)(args)`** desde el worklet.
- Nunca llamar una función no-worklet dentro del gesto sin `runOnJS` (crash / jank).

---

## Los 9 patrones (código real · los que hay que manejar 10/10)

### 1. Pan interrumpible (la base · cancela la animación en curso y continúa desde ahí)
```ts
const x = useSharedValue(0); const start = useSharedValue(0);
const pan = Gesture.Pan()
  .onBegin(() => { cancelAnimation(x); start.value = x.value; })   // <- interrumpe: agarra el valor actual
  .onUpdate(e => { x.value = start.value + e.translationX; })
  .onEnd(e => { /* física al soltar → patrones 3/4 */ });
```
Sin `cancelAnimation` + `start = x.value`, el gesto "pelea" con la animación previa = se siente roto.

### 2. Follow-with-spring (el elemento te sigue con LAG · "chat heads", trail orgánico)
```ts
const followX = useDerivedValue(() => withSpring(x.value, { damping: 14 }));
// followX persigue a x con resorte → no rígido. Base de chat-heads, cursores, orbs-guía que siguen.
```

### 3. snapPoint + withSpring(velocity) (soltás y aterriza al punto correcto, con el envión)
```ts
function snapPoint(value, velocity, points) { 'worklet';
  const projected = value + 0.2 * velocity;                 // proyección por velocidad (físico)
  const deltas = points.map(p => Math.abs(projected - p));
  const min = Math.min(...deltas);
  return points[deltas.indexOf(min)];
}
// en onEnd:
const dest = snapPoint(x.value, e.velocityX, SNAP_POINTS);
x.value = withSpring(dest, { velocity: e.velocityX, damping: 18, stiffness: 200 });
```
**Pasar `velocity` al spring** = el movimiento CONTINÚA tu throw (clave del feel premium). Sin eso, frena seco.

### 4. withDecay + clamp + rubber-band (momentum/fling con límites elásticos)
```ts
x.value = withDecay({ velocity: e.velocityX, clamp: [MIN, MAX], rubberBandEffect: true, rubberBandFactor: 0.6 });
// fling con desaceleración natural; al pegar el borde, rebota elástico (no corta seco).
```
Rubber-band manual (resistencia al arrastrar más allá del borde, en onUpdate):
```ts
function rubber(v, lo, hi, c = 0.55) { 'worklet';
  if (v < lo) return lo - (lo - v) * c;     // resistencia: cuanto más lejos, más "pesado"
  if (v > hi) return hi + (v - hi) * c;
  return v;
}
```

### 5. Stagger (cascada · cada item entra con delay por índice · vida orgánica)
```ts
items.forEach((_, i) => { v[i].value = withDelay(i * 45, withSpring(target, SPRING.snappy)); });
// 45-70ms por item. Lo que hace que una lista "aparezca con alma" y no de golpe.
```

### 6. Spring presets (EL feel · damping/stiffness, no inventar números sueltos)
```ts
const SPRING = {
  snappy:  { damping: 20, stiffness: 250 },   // crítico, sin overshoot · UI/navegación
  bouncy:  { damping: 10, stiffness: 160 },   // overshoot juguetón · celebraciones (datos sensibles: con cuidado)
  gentle:  { damping: 18, stiffness: 90  },    // suave, lento · entradas
  stiff:   { damping: 26, stiffness: 380 },    // casi instantáneo · micro-feedback
};
```
Regla: navegación/datos = `snappy`/`gentle` (sin overshoot). Overshoot solo en identidad/celebración.

### 7. Perspective 3D (profundidad real en cards/elementos · Candillon)
```ts
transform: [{ perspective: 800 }, { rotateX: `${rx}deg` }, { rotateY: `${ry}deg` }, { translateX: x.value }]
// SIN perspective, una rotación 3D se ve plana/rara. perspective ~600-1000 = proyección creíble.
```

### 8. Composability Gesture Handler 2.0 (combinar gestos sin conflicto)
```ts
Gesture.Simultaneous(pan, pinch);   // ambos a la vez (zoom + drag)
Gesture.Race(tap, pan);             // el primero que gana, cancela al otro
Gesture.Exclusive(doubleTap, tap);  // doble tap tiene prioridad sobre single
```

### 9. Reanimated 4 · API tipo CSS (alternativa declarativa · estado → transición)
```ts
// transiciones basadas en estado React, sintaxis familiar de web (Reanimated 4)
<Animated.View style={{ transitionProperty: 'transform', transitionDuration: 300, transform:[{scale}] }} />
```
Útil para estados simples (hover/press/toggle). Para gesto físico real → patrones 1-4 (imperativo).

---

## Checklist "se siente vivo" (aplicar a CADA interacción)
- [ ] ¿Es interrumpible? (cancelAnimation onBegin + start=value)
- [ ] ¿La velocidad del gesto entra al spring/decay? (continúa el envión)
- [ ] ¿Snap por velocidad (snapPoint), no por posición sola?
- [ ] ¿Rubber-band en los bordes (no corte seco)?
- [ ] ¿Spring preset correcto (snappy nav · sin overshoot en datos)?
- [ ] ¿Stagger si son varios elementos?
- [ ] ¿Side-effects vía runOnJS, resto en UI thread?
- [ ] ¿Medido en device gama baja? (el emulador miente · perf-profiling-playbook)

## Librerías emergentes a vigilar (2026)
- **react-native-ease** (App & Flow · nueva · foco performance). Aún emergente · evaluar, no adoptar a ciegas.
- **Moti** (Catalin Miron lo usa para state-driven + SVG) · capa declarativa sobre Reanimated.

## Referentes
- William Candillon (gesture+reanimated fundamentals · snapPoint · perspective 3D · gesture-driven transitions).
- Reactiive (@reactiive · serie "what about gestures" · chat-heads · follow-spring).
- Catalin Miron (pan+snap-back curvo · stagger · runOnJS · Moti).
- Software Mansion (Reanimated 4 · gesture-handler 2 · la fuente).
- Rauno Freiberg (rauno.me · el TASTE de la interacción física · web pero el principio aplica).
