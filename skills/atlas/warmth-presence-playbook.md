# Warmth & Presence Playbook · calidez humana + el asistente como presencia viva

> 9º playbook del ADN world-class (2026-06-02). Disparador: tras validar el "punto justo" (totem vivo
> legible + el asistente orb-presencia + dato-héroe cálido), Ale pidió que TODO sea world-class. Gaps que faltaban:
> (1) el craft de la CALIDEZ/humanidad, (2) el asistente como presencia con alma. Estudiado: Headspace/Calm/Stoic
> (calidez), AI voice orb UI (orb vivo), Finch (apego sin infantilismo). Crudos ~/yt/refs2 (no commiteados).
> Vara única: ¿se siente NUTRICIÓN cálida (comida, cuidado, humano) o TECNOLOGÍA (frío, vidrio)? Si lo 2º → bajar.

---

## A. Craft de la CALIDEZ (Headspace / Calm / Stoic)

La calidez NO es decoración — es reducción de fricción cognitiva + voz humana + consistencia.

1. **Decidir por el usuario.** Headspace propone el plan del día (cero parálisis de elección). → el asistente propone
   "hoy registra esto", no espera que el usuario busque.
2. **Entrada por el ÁNIMO, no por el dato.** Calm abre con "¿cómo te sientes?" y filtra todo según eso. → El
   primer toque diario de el asistente es relacional ("¿cómo vas hoy?"), no "tus calorías son X" (eso es sensible).
3. **La UI desaparece cuando importa el contenido.** Headspace Sleep: el texto se va, queda lo mínimo. → cuando
   el dato-héroe es protagonista (totem, ring completo), la UI retrocede, no compite.
4. **Bienvenida que aterriza.** Calm abre con "respira hondo" antes de mostrar nada. → la apertura ancla, no informa.
5. **Microcopy alentador, chico y ubicuo, NUNCA neutral.** Stoic cierra con "good job". → cada mensaje de el asistente
   post-registro es corto, cálido, humano (no "registro guardado").
6. **Consistencia visual = calma activa.** El reviewer critica a Calm por "too visually stimulating" (mezcla
   tipografías/ilustración/foto) y elogia la consistencia de Headspace. → UN lenguaje visual (orb + línea fina +
   el color de acento), nunca mezclar estilos. La inconsistencia ROMPE la calma.
7. **Paleta de baja estimulación en momentos de calma.** Headspace Sleep = azules/morados dark de bajo contraste.
   → los momentos de el asistente hablando / resumen nocturno piden paleta serena, no el el color de acento brillante del dashboard activo.
8. **Progreso visible y vivo** (Stoic: barra en cada tarea) → avance hacia la meta como barra viva, no solo número.

---

## B. ORB VIVO · cómo darle alma a el asistente (portable a react-native-skia)

1. **⛔ INSIGHT CLAVE — más lento = más presencia.** "When the AI speaks we slow the orb down." El cerebro lee
   lentitud = peso emocional = "está contigo". Un orb acelerado se siente técnico/ansioso; uno que respira
   despacio se siente que te acompaña. La velocidad es la emoción.
2. **Mismo objeto, distinto RITMO (no distinto diseño).** Los estados cambian `rotationSpeed` y `breathAmplitude`,
   no la forma. Un solo orb, 5 ritmos.
3. **sin/cos con frecuencias NO-enteras** (`sin(t*0.8)`, `cos(t*0.5)`) → movimiento orgánico, sin periodicidad
   de loop obvia. (Reusar useClock + useDerivedValue del el asistente ya existente.)
4. **Intensidad, no color.** Cuando algo importa (celebración), INTENSIFICAR el el color de acento (+saturación/opacidad),
   nunca cambiar de hue. Coherencia DNA.
5. **El orb siempre en el layer más cercano** (z-index) — nunca detrás de las cards de datos.

**Los 5 estados de el asistente (Skia):**
- `idle` — respira lento (scale 0.98↔1.02 · 3.2s · sine · halo blur ~12 op 0.3).
- `listening` — micro-partículas entrando al centro · escala +0.05 · halo más brillante.
- `thinking` — rotación interna lenta + partículas circulando.
- `speaking` — MÁS lento que idle + halo pulsa al ritmo del texto · el color de acento +20%.
- `celebrating` — bloom 350ms (halo 0.3→0.8→0.3) + 6 micro-partículas que salen y vuelven al orb · sin texto.

---

## C. PRESENCIA con alma SIN ser infantil (Finch → robar la lógica, descartar lo cute)

1. **Apego por inversión temprana.** Finch te hace nombrar/elegir rasgos del compañero ANTES de mostrar valor →
   "es mío". → el onboarding hace que el asistente te conozca (nombre, objetivo, momento del día) por CONVERSACIÓN,
   no configuración, antes del dashboard.
2. **El compañero reacciona a vos.** El estado de el asistente responde al uso ("el asistente está satisfecha" tras buen
   registro · una línea, no notificación invasiva).
3. **Loop INDIRECTO (safe-para-datos-sensibles clave).** En Finch no registrás para perder peso — le das energía a la mascota. →
   no "contar calorías" sino "contarle a el asistente lo que comiste para que te acompañe mejor". Saca la presión del número.
4. **Celebración inmediata pero LIVIANA.** 300-400ms, gesto > palabras (el ring se completa + 2-3 partículas + el
   orb micro-bloom), SIN texto de "¡Excelente!" ni trofeos. La sobre-celebración es presión.
5. **Anticipación, no streak.** Finch manda al pájaro de aventura → volvés por curiosidad. → el asistente cierra el día
   con "vi algo en tu semana, mañana te cuento" (curiosidad, no obligación/racha que castiga). Re-engagement sin culpa.
6. **⛔ Descartar:** el pájaro, los rainbows, el XP, las evoluciones Pokémon. Robamos la RELACIÓN (nombrar,
   invertir, reaccionar, celebrar chico, anticipar), con el lenguaje el color de acento-adulto-premium del proyecto.

---

## D. Síntesis · 5 movimientos concretos para el asistente + el proyecto

1. **Bienvenida relacional** (no un número): "Buenos días, [nombre]. ¿Cómo vas hoy?" + 3 estados → el orb ajusta
   intensidad y el tono del día según la respuesta.
2. **Orb de 2 velocidades** (5 estados, velocidad inversa a presencia) en Skia — reusar el asistente, agregar `state`.
3. **Framing indirecto del registro**: "contarle a el asistente lo que comiste" (no "registrar comida") + el orb hace un
   micro-asentimiento (scale 1→1.04→1, 200ms) al recibir.
4. **Celebración micro-orgánica**: bloom 350ms + 6 partículas que vuelven al orb, sin texto. El gesto dice todo.
5. **Anticipación del mañana**: el asistente cierra con curiosidad (insight de la semana), no con resumen de calorías ni racha.

> Regla de oro transversal: el wow del proyecto no es un efecto — es que el asistente se sienta una presencia cálida
> que te acompaña sin culpa. La tecnología desaparece; queda el cuidado.

Relacionado: `worldclass-craft.md` (ADN) · `motion-playbook.md` · `dataviz-safe-para-datos-sensibles.md` ·
`feedback_craft_al_servicio_nutricion` · `feedback_todo_world_class` · referentes en
`docs/research/worldclass/2026-06-02-referentes-apps-world-class-feel.md`.
