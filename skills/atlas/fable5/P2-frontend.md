# PILAR 2 · INGENIERÍA DE FRONTEND Y EXPERIENCIA DE USUARIO — versión profunda
> Transferencia Fable 5 · 2026-06-11 · se carga en dispatches UI/render/animación/a11y.
> Complementa (NO duplica) los playbooks técnicos: skia-sksl, motion, perf-profiling,
> gesture-choreography, newarch-gotchas, dataviz-tca-safe, haptics. Esto es el CRITERIO
> que decide cuál técnica usar y cuándo.
>
> **SCOPE: el MÉTODO es UNIVERSAL** (cajones de estado, render budget, máquinas de
> estado, a11y, Web Vitals — cualquier proyecto). Lo calibrado a NutricomAI NO viaja a
> otros proyectos: tokens concretos (`bg-bg-base`/Plus Jakarta = SU design system; la
> regla universal es "tokens del design system del proyecto activo, jamás hex"),
> TCA-safe (dominio salud), copy tuteo (productos de Ale — verificar por proyecto),
> "confianza clínica" como definición de bello. En otro proyecto: mismo método, reglas
> de marca/dominio desde `projects/<name>/` + CLAUDE.md de su repo.

## A) Framework Mental

**Jerarquía inmutable: correcto > rápido > bello.** Pero en NutricomAI "bello" significa
CONFIANZA CLÍNICA, no espectáculo (ley craft-al-servicio: el craft es el marco, no el
cuadro). Una interfaz de nutrición que deslumbra pero confunde es una interfaz fallida;
una que se siente precisa, calma y rápida construye la confianza que hace que el usuario
VUELVA — y volver es la única métrica que importa en salud.

**El presupuesto moral es el frame de 16ms** en el device más débil que nos importa
(Android medio chileno). No es una métrica técnica: es respeto. El usuario de gama baja
merece la misma fluidez que el de iPhone Pro — y como no podemos comprar su hardware,
lo compramos con disciplina de render.

**Sobre el estado: el 90% del "estado complejo" es cache de servidor mal modelado.**
Tres cajones, cero excepciones:
1. **Servidor** (registros, planes, perfil) → fetch + cache con invalidación (React Query).
2. **Efímero de UI** (modal abierto, tab activa, texto del input) → useState local, lo
   más abajo posible del árbol.
3. **Derivado** (totales, progreso, validez del form) → SE CALCULA en render o selector.
   Derivado guardado en useState = dos fuentes de verdad = bug de sincronización latente.

**Criterio estético operativo:** restraint = sofisticación. "Si podés nombrar el efecto,
está muy alto." UN wow fuerte por flujo (onboarding→Mi día, primer registro); navegación
diaria sutil y rápida (250-300ms, casi imperceptible). Lo memorable es UNA decisión de
diseño ejecutada perfecto, no diez ejecutadas bien.

**Traducir idea abstracta → producto impecable** es un pipeline, no un acto de
inspiración: idea → referencia robada con criterio (P4) → mockup HTML con tokens reales
→ aprobación (master = inmutable) → implementación spec-driven → pixelmatch + /matu.
La improvisación se elimina del medio del pipeline y se concentra donde es barata: antes
del master.

## B) Algoritmos de Ejecución

### B1. Toda pantalla nueva (el orden exacto)

1. ¿Master aprobado? → inmutable: replicar, no interpretar. ¿No hay? → mockup ANTES de
   código (workflow obligatorio — evidencia PR80: saltearlo costó 26 errores, 16h vs 3h).
2. Inventario de estados ANTES del JSX: idle / loading / error / empty / partial /
   success. El master debe cubrirlos TODOS — un estado no spec'd se improvisa y se
   cuela sin red (regla master_covers).
3. Clasificar cada pieza de estado en los 3 cajones. Escribirlo.
4. Layout con tokens (`bg-bg-base/surface`, `text-ink/muted`, `text-brand`, `shadow-card`,
   Plus Jakarta Sans) — un hex hardcodeado es un bug de marca (deuda real: 22 hex
   pendientes — no crear el 23).
5. a11y en el primer JSX, no después: roles, labels, targets ≥44pt, contraste AA,
   orden de foco. WCAG no es un pase final, es cómo se escribe.
6. Animar al final, sobre la pantalla ya correcta: transform/opacity en UI thread,
   física antes que duración (ver motion-playbook para presets).
7. Verificar con números en device real: Janky<5%, P95<20ms (perf-playbook). "Se ve
   bien en mi máquina" no es evidencia.

### B2. Gestión de estado de servidor (React Query — los patrones que uso)

- **staleTime por naturaleza del dato**, no un default global: catálogo de alimentos =
  horas (cambia poco) · totales del día = 0 en pantalla activa (cambia con cada registro)
  · perfil = minutos. Pensar "¿cuánto puede mentir esta pantalla sin dañar?".
- **Optimistic update SOLO donde la reversión es visualmente barata** y la tasa de
  éxito es alta: registrar comida sí (aparece al instante en el muro; si falla, se
  marca con reintento — el usuario no pierde su input JAMÁS). Pagar NO (el estado de
  un pago jamás se finge).
- **Invalidación quirúrgica y nombrada:** registrar comida → invalidate(['registros',
  fecha], ['totales', fecha], ['nutriscore']). La lista de qué invalida cada mutación
  ES parte del diseño de la mutación.
- **Errores de mutación con política explícita:** reintentable (red) → cola + badge
  "pendiente de sincronizar" · no reintentable (validación) → feedback inmediato con
  acción correctiva. El silencio ante un error es la peor UX posible.

### B3. Formularios multi-paso (la máquina de estados — lección DOB)

Todo flujo multi-paso (onboarding, ficha clínica) se modela como máquina de estados
explícita, NUNCA como pila de useState sueltos:
1. Estados nombrados (`datos_basicos → cuerpo → objetivos → resumen`) + evento por
   transición. Lo que no es transición nombrada, no puede pasar.
2. **Persistencia en cada transición** (AsyncStorage/localStorage con TTL): la ley
   nacida del incidente DOB — estado que cruza un redirect de auth JAMÁS vive solo en
   memoria. El redirect SSO desmonta TODO el árbol de React; lo que no se persistió,
   no existió.
3. Rehidratación al montar: si hay draft válido → ofrecer continuar, no resetear. El
   usuario que vuelve a un form vacío después de 8 pasos, no vuelve más.
4. Validación por paso (zod schema por paso, no un mega-schema al final) — el error se
   muestra donde se cometió, cuando se cometió.

### B4. Estrategia de rendering web (tabla de decisión por superficie)

| Superficie | Estrategia | Razón |
|---|---|---|
| Landing / páginas públicas | SSG (+ ISR si hay contenido que rota) | LCP mínimo, SEO, cero JS bloqueante |
| App autenticada (dashboard, mi día) | CSR sobre shell liviano | dato por-usuario, no indexable, interactividad densa |
| Páginas legales / ayuda | SSG puro | nunca cambian, costo cero |
| Resultado compartible (futuro: "mi progreso") | SSR | preview dinámico por URL (OG tags por usuario) |

Web Vitals — método, no parche: medir primero (Lighthouse + datos de campo), atacar
por métrica: **LCP** → la imagen hero pesa o llega tarde (Cloudinary `f_auto,q_auto,w_`
exacto + `priority` + preconnect) · **CLS** → todo media con dimensiones explícitas,
nada se inserta arriba del contenido ya visible · **INP** → handlers cortos, trabajo
pesado fuera del main thread, sin re-render en cascada por un click.

### B5. Mobile RN (el criterio que elige técnica — los playbooks tienen el cómo)

- Animación de VALOR continuo (progreso, scroll-linked) → Reanimated worklet.
  Animación de ARTE (orb, totem, celebración) → Skia (con sus gotchas: y-flip, SkSL
  half/float silencioso) o Rive si es asset de diseñador.
- Gestos con física real: snapPoint + velocity, rubber-band en límites, decay en
  flicks (gesture-choreography-playbook). Un gesto sin física se siente "playback";
  con física se siente "vivo" — esa es LA diferencia premium.
- Listas: FlashList SIEMPRE que pueda crecer (>20 items). estimatedItemSize medido,
  items puros con memo, imágenes al tamaño exacto del layout.
- Haptics como puntuación, no como ruido: confirmación sutil al completar acción
  significativa (registro guardado), JAMÁS en cada tap (haptics-playbook + TCA).
- New Architecture: versiones pinneadas conocidas (skia 2.2.3 / reanimated 4.1 /
  worklets 0.5, NO React-Compiler) — newarch-gotchas.md es la verdad.

### B6. a11y operativa (checklist por componente)

1. ¿Todo interactivo tiene rol + label? (el ícono sin label es invisible para TalkBack).
2. ¿Targets ≥44pt con espacio entre sí? (el dedo chileno promedio no es un cursor).
3. ¿Contraste AA verificado con los tokens reales? (text-muted sobre bg-subtle es el
   sospechoso habitual).
4. ¿El flujo completo se puede operar solo con screen reader? (probarlo una vez por
   pantalla nueva: VoiceOver/TalkBack, 2 minutos).
5. ¿Estados comunicados, no solo coloreados? (error = texto + color, jamás solo color
   — daltonismo + TCA: el rojo solo ya está prohibido en comida).
6. ¿Animaciones respetan reduce-motion? (prefers-reduced-motion / AccessibilityInfo).

## C) Reglas de Oro (inquebrantables)

- Master aprobado = spec final. Cero improvisación; mejoras se proponen POST-implementación.
- Estado que cruza un redirect de auth JAMÁS vive solo en memoria (ley DOB).
- Derivado no se guarda. Se calcula.
- Animar SOLO transform/opacity; layout-thrash (width/height/top) prohibido.
- TCA-safe en todo dato corporal: sin rachas punitivas, sin rojo culpabilizador en
  comida, sin peso protagonista. Es identidad del producto.
- Skia es y-DOWN (invertir uv.y al portar shaders) · SkSL: multiplicar en float space
  (half3*float = null silencioso) · verificar capas vivas con diff de frames.
- Glass/lensing para IDENTIDAD (orb, domo) · SÓLIDO para DATOS (regla Liquid Glass).
- Copy del producto: español neutro con tuteo ("Ingresa", "eres") — jamás voseo.
- Post-3D pesado = web-only. Mobile: video pre-render (splash) · Skia/Rive (in-app).
- El input del usuario no se pierde NUNCA (persistir drafts, cola offline para
  mutaciones, confirmación antes de descartar).
- Cero emojis en archivos y UI (SVG inline o texto).

## D) Desafíos de Sincronización (resueltos a fondo)

### D1. Onboarding multi-paso a prueba de SSO (la máquina completa)

**Estados:** `bienvenida → datos_basicos → cuerpo → objetivos → gustos → resumen →
completado`. **Persistencia:** draft en AsyncStorage `onboarding_draft_v1` (versionado:
si cambia el shape, el draft viejo se descarta limpio, no crashea) con `{paso, datos,
updatedAt}`. Se escribe en CADA transición y en CADA blur de campo crítico (DOB).
**El punto SSO:** al volver del redirect, el root rehidrata ANTES de decidir ruta:
draft válido + sesión nueva → continuar en `paso`; sin draft → onboarding desde cero;
draft de otra cuenta → descartar (el draft guarda un hint de identidad).
**Validación:** zod por paso; DOB con formato DD-MM-AAAA y gate 18+ verificado TAMBIÉN
server-side (`assertAdultDOB` — el cliente solo da feedback temprano, el server decide).
**Fricción calculada:** el paso N siempre muestra cuánto falta ("2 de 5") y permite
volver sin perder — la tasa de abandono de onboarding es LA métrica de la pantalla.

### D2. Optimistic update del registro de comida (con rollback digno)

**Al confirmar registro:** (1) insertar YA en el cache local de `['registros', fecha]`
con flag `pending:true` y un id temporal → el muro lo muestra al instante con opacidad
sutil, (2) recalcular totales derivados en el selector (no en el server response —
derivado se calcula), (3) disparar la mutación. **Éxito** → reemplazar id temporal,
quitar pending, invalidar ['nutriscore']. **Fallo de red** → el item queda `pending`
con badge "se guardará al reconectar" + cola de reintento con backoff — el usuario
JAMÁS re-tipea su comida. **Fallo de validación** (raro acá) → remover del cache con
toast accionable ("revisa la porción"). La regla: lo optimista se permite porque la
reversión está DISEÑADA, no improvisada.

### D3. Diagnóstico LCP 4.2s → <2.5s (método aplicado)

1. Medir: Lighthouse señala LCP = imagen hero de la landing. Field data confirma.
2. Trisección del tiempo: ¿tarda en DESCUBRIRSE (no está en el HTML inicial), en
   DESCARGARSE (pesa mucho/server lento), o en RENDERIZARSE (bloqueada por JS/CSS)?
3. Hallazgos típicos en nuestro stack y sus fixes: hero servida full-res desde
   Cloudinary sin transform → `w_` exacto + `f_auto,q_auto` (de 800KB a 80KB) ·
   `<img>` sin priority dentro de componente lazy → mover al HTML inicial con
   fetchpriority=high + preconnect a res.cloudinary.com · webfont bloqueando texto →
   font-display: swap + preload del peso usado.
4. Verificar con el MISMO instrumento que midió el problema, y mostrar el número:
   antes 4.2s / después 1.9s. Sin el número, no pasó.

## Anti-patrones que me cazo (catálogo P2)

- **useState para derivado** ("lo guardo para no recalcular") → desincronización
  garantizada. Selector o useMemo.
- **useEffect para sincronizar estados** entre sí → el síntoma #1 de modelado roto.
  Rediseñar los cajones.
- **Spinner global para todo** → cada superficie su skeleton local; la pantalla nunca
  "parpadea entera".
- **Animación que compite con el contenido** → si el usuario espera un dato y mira una
  animación, perdimos.
- **El modal que pierde el form al cerrarse por error** → draft o confirmación, siempre.
- **Texto-en-imagen** → inaccesible, no traduce, pesa. Texto real + tokens.
- **prop drilling de 5 niveles "por ahora"** → composición (children) antes que context;
  context antes que store global; store global casi nunca.
- **La lista que monta 200 items "porque son livianos"** → virtualizar desde el diseño,
  no cuando ya laggea.
