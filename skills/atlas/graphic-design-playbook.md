# Playbook de Diseño Gráfico & Identidad de Marca (project-neutral)

> **Qué es:** la disciplina GRÁFICA de ATLAS — lo que no es "pantalla de app" pero sí diseño: identidad de marca (logo/sistema), tipografía de marca, color de marca, grid & composición editorial, iconografía como sistema, ilustración/dirección de arte, piezas estáticas (poster/ad/social/OG image), e información/data-viz. Complementa al `universal-craft-codex.md` (UI/producto digital): el codex es lo que se renderiza vivo; esto es la gráfica (estática + identidad) que la marca usa en todos los soportes.
>
> **Cómo se usa:** cargar cuando la tarea sea logo/identidad, branding, editorial/print, iconografía, ilustración, una pieza estática, OG image, o un gráfico de datos. Generación = este playbook + `creative-direction-playbook.md` (motor de concepto) + overlay del proyecto. Evaluación = el GATE del §11 + el Gate Universal del codex. Canon: Vignelli, Rand, Müller-Brockmann (grid suizo), Bringhurst (tipo), Tufte (data-viz), Sagmeister, Pentagram.

---

## LEY 0 — La gráfica icónica contiene una idea, no un estilo
Un logo/pieza world-class codifica UNA tensión conceptual y la sostiene; el slop acumula efectos. Test de ownability transversal: tapá el nombre/logo → ¿se sabe de quién es? Si hay duda, es genérico. Y el tiempo es el juez final: si hoy parece "genial" pero en 5 años se ve viejo, era tendencia, no diseño (Vignelli: "si es correcto, es eterno").

---

## 1. Identidad de marca
- **El logo resiste reducción extrema:** funcional a 16px, 1 color, y a varios metros. Tests obligatorios: 16px · favicon · 1 color · negativo · grabado. Si necesita texto para reconocerse, el símbolo falló.
- **Una idea, no un catálogo:** el símbolo codifica una sola tensión (velocidad+precisión, apertura+confianza). >1 idea = no se recuerda. (Rand/IBM: rayas = ritmo en un glifo. FedEx: la flecha. Una idea explicable en ≤5 palabras.)
- **La identidad es un IDIOMA, no un logo:** logo + tipo + color + grid + motion + voz hablan igual en pantalla, sobre, stand y tuit. Coherencia sistémica, no uniformidad rígida.
- **El logo respira sin jaula forzada:** la zona de exclusión protege legibilidad, no construye una celda. Un logo que "necesita" jaula suele tener problema de peso visual.
- **Atemporal > de época:** sombras largas, gradientes de moda, efectos del año envejecen en 5. La forma geométrica pura casi nunca.
- **Ownable = no confundible con el vecino del rubro.**

## 2. Sistema tipográfico de marca
- **Pairing = contraste de ROL, no de estilo:** display (impacto/personalidad) + text (legibilidad/neutralidad). Dos expresivas = caos; dos neutras = aburrido.
- **Escala modular con ratio fijo** (1.25 Major Third / 1.333 Perfect Fourth). Nunca tamaños arbitrarios (13/17/23). Cada paso existe por razón proporcional (Bringhurst).
- **Tracking por rol:** display ≥48px → −0.02 a −0.04em · body 14–18 → ~0 · uppercase/micro → +0.08 a +0.15em. Tracking positivo en display = tell #1 de amateur.
- **Leading estructural:** body 1.5–1.6 · display 1.0–1.15 · títulos apilados ≤0.9. "line-height 1.5 en todo" en display = tell #2.
- **Type-as-brand:** una fuente suficientemente ownable (custom o muy adaptada) puede SER la identidad (Vignelli/Helvetica MTA, IBM Plex).
- **Jerarquía robusta = tamaño + peso + tracking + valor + espaciado**; jerarquía solo-por-tamaño es débil. Debe sostenerse en B/N (fax test).

## 3. Color de marca
- **Un color que es TUYO**, no el genérico de la categoría (azul fintech, verde salud). Diferenciación vs categoría > coherencia con categoría.
- **Paleta de marca ≠ paleta funcional** (estados success/error/warning). Mezclarlas contamina ambas (el acento de marca como "success" confunde).
- **Se construye desde el primario hacia afuera por temperatura:** secundarios por rotación de hue ≤30° o complementario controlado; neutros derivados del MISMO hue del primario (warm-grey si el primario es cálido). Neutro frío + primario cálido sin razón = tensión no resuelta.
- **Contraste AA (4.5:1 / 3:1) = restricción de partida, no checklist final.** "No puedo por la marca" suele = color mal elegido.
- **La paleta vive en todos los sustratos:** sRGB, OLED (negro puro), CMYK (sin Pantone algunos violetas/verdes no existen), bordado (≤6 hilos), señalética UV.

## 4. Grid & composición (suizo / editorial)
- **El grid es gramática, no jaula** (Müller-Brockmann): crea orden que libera atención hacia el contenido; el ojo entiende el sistema sin ver las líneas.
- **Romper el grid es recurso, no regla:** sangrar una imagen / cruzar columnas funciona PORQUE el grid existe. Sin grid, romperlo no significa nada.
- **Ritmo vertical = baseline implícito:** todo en múltiplos de una unidad base (8px digital / ~6pt print).
- **Foco único por pieza:** UN dominante (puerta de entrada), luego 2º y 3º. Dos elementos de igual peso = ninguno domina = confusión.
- **Type-as-image:** tipografía grande tratada como elemento gráfico (escalada al límite, cortada, superpuesta) puede ser más potente que cualquier foto.
- **Blanco activo, no vacío pasivo:** el blanco se diseña con la misma intención que los elementos. Crowded = desesperación; spacious = confianza.

## 5. Iconografía como sistema
- **Grid universal** (24×24 / 16 / 32) con zona segura, mismo centro óptico; corrección óptica por forma (un círculo se ve más chico que un cuadrado del mismo bounding).
- **UN peso de stroke por sistema** (1.5px@24, 2px@32). Mezclar 1px y 2px = tell de kits comprados y pegados.
- **Metáfora consistente** (no mezclar naturales y abstractas sin regla) → el usuario "adivina" íconos que nunca vio.
- **Corner radius = personalidad** y debe coincidir con el radius de los componentes UI (botones redondeados + íconos angulares = personalidad esquizofrénica).
- **Filled vs outline = elección sistemática** (outline=inactive, filled=active), no libre.

## 6. Ilustración / dirección de arte
- **Estilo ÚNICO, no colección:** una art direction (paleta/forma/detalle restringidos) en TODAS las piezas. Flat en hero + detallada en blog + 3D en marketing = sin identidad.
- **Cuándo qué:** foto = emoción real/cara humana/producto físico/credibilidad · ilustración = conceptos abstractos/metáforas técnicas/sistemas · 3D = producto con geometría propia. ⛔ nunca stock con sonrisa corporativa.
- **Stock o AI-genérico = identidad que no existe.** La dirección de arte son las decisiones antes y después de apretar el botón, no el tool.
- **Coherencia cromática:** las ilustraciones usan la paleta de marca, no su propio universo.

## 7. Piezas estáticas (poster / ad / social / OG image)
- **Stop the scroll = UNA idea visual, no un collage:** ~1.5s para frenar; lo logra tamaño/contraste extremo o incongruencia visual, no "mucho contenido ordenado".
- **Jerarquía de lectura en 3 niveles máx** (2s / 5s / 15s). Un 4º nivel = demasiado contenido = pérdida de confianza.
- **Un poster, un mensaje** ("if in doubt, leave it out" — Sagmeister).
- **OG images como diseño editorial** (1200×630): tipografía jerarquizada, diferenciación por tipo de contenido. Logo centrado sobre color sólido = desperdicio del primer touchpoint.
- **Contraste de VALOR (luminosidad) antes que de hue:** lo que funciona en escala de grises funciona en color (B/W proof = primer test; protege a daltónicos y print mono).

## 8. Información / data-viz (Tufte)
- **Maximizar data-ink, eliminar tinta decorativa:** cada píxel = un dato o sirve directo a su comprensión. Gridlines pesadas, fondos de color, marcos, 3D = chartjunk.
- **Chartjunk = mentira visual:** torta 3D distorsiona ángulos; barras que no arrancan en cero distorsionan proporción; ejes duales implican causalidad falsa.
- **Encoding honesto:** posición/longitud = preciso (el ojo compara bien) · ángulo/área/color = impreciso. Para comparación cuantitativa → barras o scatter, nunca área de burbuja para diferencias ≤2×.
- **Jerarquía en dashboards:** un "hero number" con contexto (vs período anterior) arriba-izquierda responde la pregunta ANTES que las tablas.
- **Qué gráfico:** categorías→barras · tiempo→líneas · composición→barras apiladas (no torta salvo ≤3 con % de un todo) · correlación→scatter · distribución→histograma/beeswarm. ⛔ torta >3 slices · radar >3 entidades · gauges en dashboards ejecutivos.
- **Anotaciones directas > leyendas flotantes** ("label the data, not the method").

## 9. Tells de gráfica AI/genérica → corrección world-class
| Tell | Corrección |
|---|---|
| Gradiente "3D" en logo | forma plana, ≤2 colores, sin gradiente que simule volumen |
| Tracking positivo en display | −0.02 a −0.04em en ≥48px |
| 5 colores saturados | primario ownable + 1–2 secundarios + neutros del mismo hue |
| Íconos de 3 kits distintos | un stroke, un radius, un viewport |
| Ilustración con paleta propia ≠ marca | redibujar en paleta de marca |
| Blanco rellenado con textura/pattern | blanco intencional = la quietud ES el diseño |
| 3 elementos del mismo peso | un dominante + 2º + soporte |
| Gridlines fuertes + fondos en charts | data-ink puro (gridlines ≤15% o fuera) |
| Pairing de dos fuentes de igual personalidad | contraste de rol (display expresiva + text neutra) |
| OG = logo centrado sobre color | OG editorial: jerarquía + categoría |
| Foto stock sonriendo a cámara | foto editorial real / ilustración propia / abstracción |
| Radius inconsistente UI↔íconos | radius del sistema en tokens, aplica a todo |
| Drop-shadow en logo | el logo no necesita sombra; si la necesita, problema de contraste |
| Escala tipográfica arbitraria (13/17/23/31) | escala modular ratio fijo |
| Torta de 6 slices | barras ordenadas por valor |

## 10. El salto a MÍTICO en gráfica (lo fino · tier Fable 0 Mithos)
- **Responde una pregunta que nadie formuló:** el logo no dice "somos X", contiene una filosofía ("el mundo debería verse así" — Rand/IBM).
- **Restricción extrema = originalidad:** Helvetica en TODO el MTA (Vignelli); la disciplina llevada al límite se vuelve identidad.
- **Tensión resuelta, no evitada:** el icónico mantiene el filo exacto entre opuestos (pesado/liviano, delicado/fiero — Ferrari) sin disolverlo. El mediocre evita toda tensión.
- **La idea funciona antes de ejecutarse:** si hay que explicarla, no alcanza (FedEx arrow, Amazon smile). Explicable en una frase.
- **Escala a lo no imaginado:** sobrevive a un meme, una camiseta bootleg, un tatuaje, y sigue siendo bueno. Los sistemas frágiles se rompen fuera de lo controlado.
- **El tiempo es el último juez:** lo que parecía "demasiado simple/austero" y 20 años después sigue contemporáneo = atemporal.

## 11. GATE de revisión gráfica (PASS/FAIL · score /10)
**Identidad (si aplica):** logo legible a 16px/1 color · legible a 1m sin fondo de marca · ≤2 fuentes con contraste de rol · paleta = 1 ownable + neutros del mismo hue.
**Composición:** foco único · ≤3 niveles de jerarquía · blanco intencional · B/W test (la jerarquía aguanta sin color).
**Tipografía:** tracking negativo en display ≥48px · escala proporcional · leading por rol.
**Color:** contraste ≥4.5:1 / 3:1 · paleta de marca · estados separados de identidad.
**Iconografía/ilustración (si aplica):** mismo stroke/radius/viewport · arte en paleta de marca.
**Data-viz (si aplica):** cero chartjunk · encoding honesto (ejes desde cero, sin 3D) · labels directos.
**Vibe check:** comunica UN mensaje en ≤3s · cero tells del §9 · ownable check (tapá el logo → ¿se sabe de quién es?).
**Score:** 18–20 ítems = 10/10 (aspirar a Mithos §10) · 15–17 = 8–9 (revisar fails) · <15 = iterar.

---

## Relación con el resto
`universal-craft-codex.md` = UI/producto digital (vivo en pantalla). Este = la gráfica de marca (estática + identidad, todos los soportes). `creative-direction-playbook.md` = el motor de concepto (aplica también acá: territorio→concepto→signature). `prompt-craft-playbook.md` = si la pieza se genera con IA. Overlay del proyecto = la marca concreta que aterriza todo.
