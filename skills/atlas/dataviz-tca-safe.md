# Data-Viz Playbook — health rings/gauges premium + safe-para-datos-sensibles

> Destilado de research 2026-05-31 (Apple/WHOOP/Oura/Gentler Streak/MacroFactor + estudio sensible datos sensibles).
> Consumir al diseñar/revisar CUALQUIER visualización de datos de el proyecto: totem, rings (ayuno/agua/
> hábitos/macros), gráficos de tendencia, gauges. La psicología es parte del craft, no un agregado.

---

## 1. PATRONES PREMIUM (invariantes cross-app)
| Principio | Implementación |
|---|---|
| Restraint de color | 3 colores semánticos MAX. Más = ruido. (WHOOP: verde/amarillo/rojo y nada más.) |
| Número héroe oversized | métrica primaria 56-72sp, sin decoración (legible "a un brazo de distancia", WHOOP) |
| Leading dot / comet head | círculo con glow gaussiano en el endpoint del arco, misma saturación que el arco |
| Dark canvas funcional | `#050505`/`#000` — los datos pop, el fondo no decora |
| Semantic gradient | el arco cambia de color según posición/valor (sweep gradient en el STROKE, no fill) |
| Progressive disclosure | 3 niveles en 3 pantallas: at-a-glance → vs-baseline → raw/trends. Nunca todo a la vez. |
| Baseline PERSONAL | comparación vs vos (tu semana pasada), NUNCA vs promedio de usuarios |
| Motion con easing | trim del arco con spring/cubic-bezier, nunca linear; leading dot con bounce suave |
| Espaciado generoso | padding 16-24, gap 8 entre arcos concéntricos |

- **Dial = punto en un rango continuo**, NO barra que "llena hacia una meta". WHOOP usa escala 0-21 (rara a propósito = el dato es personal, no "% de meta"). Oura 0-100 con zonas, nunca binario pass/fail.
- **Wrap-around (>100%):** el arco da la vuelta y se superpone con alpha ~40-60% — comunica "superaste" SIN punir. Nunca rojo.
- **Tendencias:** area chart con fill 20% (transmite volumen) + línea baseline punteada `#FFFFFF30` + punto de hoy con glow. 7-day rolling avg como línea principal (suaviza el ruido). Gap (no cero) en días sin registro. Sin proyecciones futuras.
- **Consistencia histórica:** heatmap estilo GitHub (7col × N semanas) en vez de "racha X días" — ves el patrón, no la pérdida.

## 2. ⛔ safe-para-datos-sensibles — reglas duras (estudio BJPsych: 73% de usuarios de apps de calorías reportó que contribuyó a su datos sensibles)
**NUNCA:**
- Rojo o warning al superar CUALQUIER meta nutricional (rojo = "fracaso moral").
- Proyecciones de peso/composición ("si cada día fuera así, pesarías X" — daño documentado).
- Lenguaje binario "cerraste/fallaste el ring".
- Streak counter prominente que resetea a cero (sunk-cost → compulsión).
- Sugerir restricción ("te quedan X kcal, cuidado").
- Comparación con "usuarios similares".
- Progress bar que muestra "cuánto te FALTA" como déficit.

**SIEMPRE:**
- **Rango cómodo, no meta puntual**: "Tu zona hoy: 1800-2200 kcal" — el punto puede estar en cualquier lado del rango sin juicio.
- Baseline personal (vs tu semana pasada).
- Lenguaje de **abundancia**: "has nutrido tu cuerpo con X" > "te faltan X".
- Celebrar el **registro** (el acto de consciencia), no el resultado.
- Tendencia suavizada (rolling avg) para peso, no fluctuación diaria (mata el catastrofismo de "subí 2kg").
- Permitir skip/pausa sin perder estado ("hoy no registré" ≠ fracaso; Gentler Streak permite "sick/injured/break").
- **Amber** como "atención neutral", NUNCA rojo. Macros con colores de marca (cyan/magenta/amber/lima) que no traen carga moral.

**Copy table:**
| Evitar | Usar |
|---|---|
| "Te faltan X kcal" | "Has comido X kcal hoy" |
| "Superaste tu meta" (rojo) | "Hoy comiste un poco más — está bien" |
| "Racha rota" | "Volviste · eso es lo que cuenta" |
| "Meta de calorías" | "Zona cómoda" / "rango de energía" |
| "Fallaste el ayuno" | "Hoy el ayuno fue de X horas" |

> Modelo a seguir: **MacroFactor** ("¿qué pasaría si una app de nutrición no intentara hacerte sentir culpable?") + **Gentler Streak** ("si 15 min es lo que tu cuerpo puede hoy, eso es genial"). Modelo a NO seguir: Apple Rings (gestalt-closure + sunk-cost → ansiedad en población datos sensibles), MyFitnessPal (rojo/verde moral).

## 3. APLICACIÓN — rings de el proyecto
- **Ring de ayuno:** arco de 240° (gap abajo, menos "objetivo a cerrar"). 3 zonas de color en gradiente continuo (el color de acento claro→oscuro→cyan). Leading dot con glow que pulsa suave. Centro: tiempo `HH:MM` + "en zona de beneficio"/"iniciando" (nunca "te faltan X horas"). Zona objetivo = rango (14-18h) como arco de fondo más brillante; el punto aterriza en cualquier lado sin punir. Cero rojo. Completar = shimmer recorre el arco (no confetti).
- **Ring de agua:** fill por tomas, cada una con micro-bounce (spring). Cyan. Centro: "3 vasos hoy" (absoluto, no "faltan 5"). Sin meta numérica prominente. Sin notificación de "fallaste" si no se registra.
- **Ring de hábitos (Tus Gustos):** N segmentos (uno por hábito, máx 4-5), color por hábito. Gap = no completado. SIN racha visible (la racha vive en detalle, opt-in). Historial = heatmap "año en píxeles". Completar = segmento flota (translateY -4, spring).
- **Totem (ya shipeado):** mantener. Refinamientos: sweep gradient en cada arco de macro + leading dot con glow + track del arco a 15-20% del color (no gris) + wrap-around con alpha 40% (no rojo). En home compact: solo 3 valores + mini sparkline 7d.
- **Comet head (todos los rings):** 3 capas sobre el endpoint — Circle blur grande (r12, op0.4) + medio (r6, op0.6) + sólido (r3, op1.0), BlendMode plus. Posición: `x=cx+r·cos(angle), y=cy+r·sin(angle)`.

## Referentes / recursos
- WHOOP design breakdown (925studios) · Gentler Streak (Apple "Behind the Design" + 60fps.design) · Oura redesign (Instrument) · MacroFactor philosophy · estudio datos sensibles `pmc.ncbi.nlm.nih.gov/articles/PMC8485346` · Smashing "Streak System UX Psychology" 2026 · Mobbin health-fitness · lib base `react-native-progress-circle-gradient` (UI-thread sweep) + comet head custom Skia.
