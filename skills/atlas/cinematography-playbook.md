# Cinematography Playbook — el Director de Foto de FAZM/NutricomAI

> Destilado de craft cinematográfico para TODO output de video (2026-06-07). Consumir al diseñar/dirigir/revisar
> CUALQUIER video: splash pre-render, clip del orbe/totem, hero de landing, ad Meta/TikTok, celebración Rive→video.
> El eje es el del DIRECTOR DE FOTO: cada plano MOTIVADO (composición + lente + movimiento + luz + color + corte + sonido).
> Regla maestra (gemela del motion-playbook): **si podés nombrar el efecto, está muy alto.** Restraint = cine; exceso = AI-slop.
> Brazos ejecutores (el director es la VISIÓN, estos las MANOS): `grok-cli` (generativo Grok Imagine · SuperGrok OAuth) ·
> `/video` (mk-video: Veo/Runway/Kling/Pika/Remotion) · `/video-edit` (corte ffmpeg) · `youtube-study-playbook.md` (extraer frames).

---

## LEY 0 — La diferencia "video AI básico" → "pieza de autor" NO es resolución
Es **intención por plano + luz motivada + movimiento de cámara con causa + el carácter de una lente real + un corte que respira.**
Un clip "cinematic 4k beautiful" sin intención es slop. Test del director: por cada plano, responder *¿por qué ESTA cámara, ESTA luz, ESTE corte, AHORA?* Si la respuesta es "se ve lindo" → no está dirigido. Si alguien puede decir "esto lo hizo una IA" sin dudar → rehacer.

---

## 1. Las 4 superficies de video de NutricomAI (qué dirige el director en cada una)
| Superficie | Pipeline | Lo que el director controla | Restricción dura |
|---|---|---|---|
| **Splash / wow one-shot** | Escena 3D offline (R3F/Grok) → MP4 ~1MB ffmpeg | plano único, push-in motivado, ignición de luz, loop perfecto | 2-3s · ≤1MB · loop sin costura · idéntico en todo device |
| **Orbe / totem / agua in-app** | `grok-cli video` → `useVideo` + `ColorMatrix` (luma→alpha) Skia | el clip debe componer: fondo NEGRO PURO, sin banding, materia líquida creíble | 60fps garantizado · clip corto loopable · TCA-safe |
| **Hero landing web** | R3F real-time O video pre-render | cámara que se mueve, post-stack completo, DOF narrativo | Awwwards-tier · web-only el post 3D |
| **Ad / social (Meta/TikTok)** | grok-cli / Veo / Kling + `/video-edit` | hook 0-2s, vertical 9:16, ritmo, captions, safe-area | spec de plataforma · deferir estrategia a `/video` + `mk-ad-creative` |

Insight: en mobile el wow vive PRE-RENDERIZADO (no se pelea el hardware · ver worldclass-craft §3). El director dirige el clip OFFLINE con calidad de cine; el runtime solo lo reproduce/compone.

---

## 2. ENCUADRE Y COMPOSICIÓN (la gramática base)
- **Escala de plano** (intención emocional, no capricho): EWS/establecimiento = contexto · WS = cuerpo/acción · MS = relación · CU = emoción · ECU = detalle/tensión. Cambiar de escala = cambiar de idea; no zoomear sin razón.
- **Tercios + punto de interés** sobre intersecciones. El centro perfecto SOLO para simetría deliberada (producto premium, identidad — el orbe centrado es válido: es un ícono, no una escena).
- **Headroom** justo (ni decapitado ni flotando) · **lead room / nose room**: dejar aire hacia donde mira/se mueve el sujeto.
- **Profundidad en 3 capas**: foreground (encuadra) · midground (sujeto) · background (contexto). Sin capas la imagen es plana = tell de AI-básico. Para el orbe: partículas/cáusticas fg + orbe mg + viñeta/scrim bg.
- **Balance y líneas guía**: la composición conduce el ojo al sujeto. Negative space = sofisticación (el dark #050505 ES composición).

## 3. LENTE (la psicología de la focal · "lens character")
- **Focal → emoción:** 24mm gran-angular = espacio/épica/distorsión (cuidado con caras) · 35mm = natural documental · **50mm = ojo humano (default honesto)** · 85mm = retrato, compresión, separa sujeto del fondo (premium) · macro = textura/detalle (gotas, ingrediente, piel del alimento).
- **Compresión telefoto** acerca planos y aplana → look de producto caro. **Distorsión wide** exagera profundidad → energía/inmersión.
- **DOF como narrativa**: foco poco profundo aísla el sujeto (el ojo va donde está el foco). Bokeh = lujo. El rack-focus (cambiar el foco dentro del plano) revela/conecta.
- **"Lens character" = imperfección acumulada** (worldclass-craft §2): aberración cromática sutil (0.001-0.002), grano (opacity 0.03-0.05), viñeta (0.55-0.7), un punto de flare/bloom en emisivos. Una lente real nunca es perfecta — esa "suciedad" es lo que lee como cine. ⛔ si podés nombrar el efecto, bajalo.

## 4. MOVIMIENTO DE CÁMARA (cada uno MOTIVADO · nunca decorativo)
| Movimiento | Significa | Cuándo en NutricomAI |
|---|---|---|
| **Push-in (dolly/empuje)** | intimidad, revelación, foco emocional | splash: empuje lento al orbe naciendo |
| **Pull-out** | contexto, soledad, "el todo" | revelar el cockpit completo desde el orbe |
| **Dolly lateral / truck** | acompañar, presentar | barrer ingredientes/macros |
| **Tilt / pan** | descubrir, conectar dos puntos | de la comida al dato |
| **Crane / boom** | escala, cierre de escena | hero de landing |
| **Handheld** | urgencia, humano, crudo | casi NUNCA en NutricomAI (rompe lo premium/calmo) |
| **Locked (trípode)** | control, lujo, observación | producto/identidad · el default premium |
- **Velocidad de cine**: lenta y con ease (la cámara acelera y frena suave, nunca lineal). Cámara a 60fps = movimiento sub-perceptible; el ojo siente "vivo" sin "se mueve". Easing de cámara = `ease-out-expo` para revelaciones (ver motion-playbook §2).
- **La cámara se mueve, no solo el objeto** (worldclass-craft §2). Pero **un movimiento por plano**: combinar push+pan+tilt+zoom a la vez = mareo + slop. Restraint también acá.
- ⛔ **zoom digital brusco, shake gratuito, órbita 360° sin motivo, speed-ramp de plantilla** = tells de AI/TikTok genérico.

## 5. ILUMINACIÓN (luz motivada · la firma premium)
- **3 puntos** (worldclass-craft §2): key cálido (la forma) + fill frío bajo (sombra abierta, ratio alto = dramático/low-key) + **rim/back cián** (separa del fondo, amplifica bloom en el borde = halo de producto). El rim ES la firma NutricomAI.
- **Luz motivada**: que parezca venir de una fuente del mundo (el propio orbe emite, la pantalla ilumina la cara). Luz sin fuente lógica = videojuego barato.
- **Low-key dark** (#050505) es la casa: pocas luces, mucho negro, el sujeto emerge. NO subir exposición global — el contraste ES el lujo.
- **Temperatura/contraste de color**: cálido vs frío en la misma toma da dimensión. Esmeralda #059669/#34D399 = vida (la única saturación fuerte permitida).

## 6. COLOR / GRADE (paleta + ACES, no filtro)
- **ACESFilmic** tone mapping (worldclass-craft §2) · exposure ~1.2 · AgX si el esmeralda sale fluorescente. NUNCA Linear/None.
- **Paleta DNA**: dark #050505 · esmeralda vida · canales macro (carbo cyan #22D3EE / prote magenta #E879F9 / grasa amber #FBBF24 / fibra lima #84CC16) como acentos puntuales. ⛔ **teal-and-orange genérico de Hollywood = slop** — su grade es esmeralda-sobre-negro, no el cliché.
- **Contraste y crushed blacks** con cuidado: negro profundo SÍ, pero sin perder el detalle del material líquido (banding = muerte del compositing in-app). Exportar 10-bit cuando se pueda; dither al bajar a 8-bit.
- **Consistencia plano a plano**: el grade es uno solo en toda la pieza (continuidad de color = profesionalismo).

## 7. RITMO DEL MONTAJE (Walter Murch · "el corte que respira")
- **Duración de plano = ritmo**: planos largos = calma/lujo/contemplación (NutricomAI diario) · cortes rápidos = energía (ad/hook). El ritmo sigue la **respiración del espectador**, no un BPM mecánico.
- **Regla de Murch (jerarquía del corte):** emoción (51%) > historia > ritmo > eye-trace > planaridad/eje. Cortá donde la EMOCIÓN lo pide antes que donde la continuidad lo permite.
- **Corte invisible**: cortar en el movimiento (match-on-action), respetar el eje de los 180°, eye-trace (el ojo ya está donde aparece el siguiente plano). **J-cut / L-cut** (el audio entra antes/sale después del corte) = el pegamento pro que hace fluido el montaje.
- **Match cut** (forma/movimiento que rima entre planos) = elegancia (gota → orbe → plato). **Hold** (dejar respirar el último frame) antes de cortar.
- En ads: **hook en 0-2s** (el plano más fuerte primero, no el build-up). Cada 1.5-3s un cambio si es social; planos más largos si es brand.

## 8. SONIDO (el 50% invisible · vende el material)
- **Sound design diegético** (agua que se mueve, ignición que enciende, click del registro) hace CREÍBLE la imagen — el cerebro "siente" el líquido por el sonido. Un orbe sin sonido de agua se ve CGI; con él, se ve real.
- **Score**: minimal, cálido (Headspace/Calm), nunca épico-de-stock. ⛔ **música épica genérica + whoosh de transición = el tell #1 de ad-AI**.
- **TCA-safe en audio**: nada de tensión/alarma/urgencia ansiosa. Respiración, no pulso de pánico (gemelo de la regla de motion). El silencio es una opción premium.
- **Ducking** del score bajo la voz/SFX clave. Mezcla: SFX > voz > música.

## 9. TIEMPO (slow-mo / speed con propósito)
- **Slow-motion** solo para revelar belleza/detalle que a velocidad real se pierde (la gota cayendo, el líquido reconfigurándose). No slow-mo "porque sí".
- **Speed-ramp** (acelerar→frenar en el beat) con MUCHO restraint — es el efecto más cliché de los 2020s; en NutricomAI casi nunca.
- **Loop perfecto** (splash/orbe in-app): primer frame == último (o cross-dissolve invisible) · sin "salto" perceptible. ffmpeg: cortar en el cruce de fase de la respiración.

---

## 10. PROMPTING CINEMATOGRÁFICO (dirigir un modelo generativo · grok-cli/Veo/Kling)
El modelo es tu equipo de rodaje: si le das una orden vaga, improvisa slop. **Fórmula del director** (en este orden):
`[escala de plano] de [sujeto + acción concreta], [movimiento de cámara motivado], [lente/focal + DOF], [esquema de luz + dirección + temperatura], [paleta/grade + mood], [textura/film stock], [ritmo/duración]`

- ⛔ **Prompt slop:** "a beautiful cinematic 4k video of a glowing orb, amazing, high quality, trending". (Sin intención → el modelo promedia → slop.)
- ✅ **Prompt dirigido (orbe estanque splash):** "Extreme close-up of a liquid emerald sphere forming from still black water, slow 3-second push-in, 85mm lens shallow depth of field, single warm key from upper-left + cyan rim light behind, near-black #050505 background, emerald #34D399 internal glow, subtle film grain and chromatic aberration, calm and premium, seamless loop, no text."
- **Negativos** (lo que mata el realismo): `no morphing, no extra fingers, no warped geometry, no text artifacts, no flicker, no oversaturation, no lens flare spam, no fast cuts`.
- **Consistencia**: fijar seed entre tomas (`grok-cli ... --seed N`) · misma descripción de luz/lente/grade en todos los prompts de una pieza (continuidad). `image-edit`/`video-extend` para mantener el mismo sujeto.
- **Iteración del director**: generar 3-4 variantes, juzgar contra la RÚBRICA (§12), elegir, refinar el prompt sobre lo que falló (no regenerar a ciegas). El ojo de Ale caza lo que el modelo no.
- **Material in-app**: para compositing useVideo+ColorMatrix → pedir **fondo negro PURO uniforme** (luma→alpha limpio), sujeto bien separado, sin banding en el degradé. Probar el alpha antes de dar por bueno el clip.

## 11. PIPELINES TÉCNICOS (la entrega correcta)
- **Pre-render R3F→MP4** (splash): renderizar a **24fps** (cadencia de cine) o 30 si hay UI · `motion blur` ON (sin él se ve a saltos = CGI) · ffmpeg: `-c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart` · target ~1MB · loop con primer=último frame. Verificar peso y loop ANTES de integrar.
- **In-app compositing** (totem probado · /matu 9.59 · `EstanqueTotem.tsx`): `grok-cli video` con fondo negro → `useVideo` (Skia) + `ColorMatrix` luma→alpha → compone sobre cualquier pantalla. ⛔ y-flip Skia (worldclass-craft §4) · sin banding · focus-pause batería.
- **Ad / social**: `/video` (mk-video) orquesta la generación + `/video-edit` corta por transcript/beats · vertical 9:16 · captions quemados · safe-area (la UI de plataforma no tapa el sujeto) · primer frame = thumbnail fuerte.
- **"Ver" el video para revisarlo** (capacidad ADN · reusar `youtube-study-playbook.md`): `ffmpeg -i clip.mp4 -vf "fps=2,scale=320:-1,tile=4x4" sheet.png` → leer el contact-sheet como imagen → evaluar contra la rúbrica. Crudos en `~/yt`/`/tmp`, nunca commiteados.

---

## 12. RÚBRICA DEL DIRECTOR — el gate "todo sea 10/10" (PASO 6H)
Puntuar cada eje 0-10 sobre frames extraídos (§11) + el clip. **PASS = promedio ≥ 9.5 Y ningún eje < 8.** Cualquier tell de AI (§13) presente = FAIL automático.
1. **Composición** — capas/tercios/balance/negative space; el ojo va al sujeto.
2. **Lente / DOF** — focal con intención; foco aísla; bokeh creíble.
3. **Movimiento motivado** — un movimiento por plano, con causa, ease de cine.
4. **Luz** — 3 puntos, motivada, rim-firma, low-key sin aplastar.
5. **Color / grade** — paleta DNA, ACES, consistente, sin teal-orange cliché.
6. **Ritmo de montaje** — duración por emoción, J/L cuts, corte invisible.
7. **Continuidad** — eje 180°, color/luz constantes, sin saltos.
8. **Sonido** — SFX diegético creíble, score restraint, TCA-safe, mezcla limpia.
9. **Lens character / textura** — grano/aberración/viñeta sutiles; nada plástico.
10. **Cero tells AI** — sin morphing/flicker/uncanny/física imposible/plantilla.

## 13. ⛔ ANTI-AI-SLOP DE VIDEO (cualquiera presente = rehacer)
1. Morphing de manos/dedos/objetos · geometría que "respira" mal. 2. Flicker temporal / hervor de textura entre frames. 3. Caras uncanny / ojos muertos. 4. Física imposible del líquido (el agua que no pesa). 5. Movimiento de cámara sin motivo (órbita/zoom decorativo). 6. "Cinematic/epic/4k" genérico sin dirección. 7. Música épica de stock + whoosh. 8. Speed-ramp / transición de plantilla (wipe, star, glitch). 9. Texto kinético de template. 10. Sobre-saturación / teal-orange / bloom chillón. 11. Loop con salto perceptible. 12. Banding en degradés (mata el compositing).

## 14. REFERENTES (robar craft · estudiar vía youtube-study-playbook)
- **DPs:** Roger Deakins (luz motivada, restraint) · Emmanuel Lubezki "Chivo" (cámara fluida, luz natural) · Darius Khondji (textura/oscuridad). Podcast: *Team Deakins*.
- **Montaje:** **Walter Murch — *In the Blink of an Eye*** (la regla del corte, biblia del editor) · *Every Frame a Painting* (YouTube · gramática visual).
- **Product / brand film:** Apple keynote films & "Shot on iPhone" (locked, low-key, producto como héroe) · **ManvsMachine**, **Buck**, **Territory Studio**, **Ash Thorp** (motion+grade premium) · Linear/Vercel/Stripe brand video (restraint tech).
- **Generativo dirigido:** estudiar reels de directores que prompean con lenguaje de cine (shot list real), NO "prompt packs" genéricos. Aplicar §10.
- **Cómo estudiarlos:** `yt-dlp` (subs/transcript) + `ffmpeg` frames→contact-sheet (youtube-study-playbook.md). Síntesis al repo; crudos nunca.

---

## Resumen operativo (el director en una línea)
Antes de generar/dirigir un video: **shot list** (qué planos, por qué) → prompt dirigido §10 / pipeline §11 → extraer frames §11 → rúbrica §12 → si <9.5 o algún tell §13 → refinar el plano que falló, no regenerar a ciegas. Restraint siempre: el cine es lo que NO se ve gritar.
