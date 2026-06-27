# Skill Design Playbook — cómo hacer skills/harnesses world-class

> Síntesis de estudio YouTube (2026-06-04 · método youtube-study-playbook.md). 5 referentes:
> Anthropic "Claude Code best practices" (489k) · Barry Zhang & Mahesh Murag / Anthropic
> "Don't Build Agents, Build Skills Instead" (1.4M) · Anthropic "Agent Skills Explained" ·
> Cole Medin "Building Agent Harnesses masterclass" · Burke Holland "Complete guide to Agent Skills".
> Crudos locales en ~/yt (no commitear). Acá va solo la síntesis transformativa.

## Los 6 principios (convergentes en 3+ fuentes)

1. **PROGRESSIVE DISCLOSURE** (las 5 fuentes). Solo `name`+`description` viajan en el system prompt (~30-50 tok/skill). El cuerpo se carga cuando la description matchea el prompt. Archivos de apoyo (scripts/templates/sub-docs) se cargan SOLO cuando el flujo los necesita. Resultado: instalás N skills sin reventar el contexto. *El que carga siempre tiene que ser chico.*

2. **LEAN CORE + LAYERED** (Anthropic, Cole, Burke). El archivo que carga siempre debe ser corto — Cole: *"100-300 líneas, no miles"*. Detalles → archivos linkeados o scoped por path (reglas de `api/` solo se cargan al entrar a `api/`). El core = router + scope; el resto se descubre.

3. **REGLAS ATÓMICAS > EJEMPLOS VERBOSOS** (Anthropic best practices, explícito). *"Claude 4 sigue instrucciones mucho mejor; auditá y podá lo innecesario post-upgrade."* Anthropic puso 37 líneas de "no dejes comentarios" y el modelo viejo igual fallaba — la fix NO es más líneas. 5-10 reglas atómicas + 1-2 ejemplos POSITIVOS ("hacé Y") pesan menos y rinden más que 30 prohibiciones ("nunca X"). Los casos reales de violación → log que crece solo (learned-patterns), no hardcodear 40 en el core.

4. **SCRIPTS > PROSA** (Barry, Burke). Código auto-documentado, verificable, modificable, cargable on-demand. Parsear output explícito (JSON), no confiar en que el modelo "entienda" texto libre. Cada script = unidad verificable independiente. Lógica compleja en prosa = ambigüedad; en script = determinismo.

5. **DIVIDIR POR DOMINIO** (Barry, Burke, anthropic-skills). Una skill = un dominio enfocado. Señal de mal diseño (Barry Zhang): *"crece a monolito, tarda semanas en mantener, responsabilidades difusas, coupling implícito"*. Si mezcla N dominios no relacionados → N skills que se componen en runtime.

6. **SELF-IMPROVING + SUBAGENTES** (Cole, Anthropic). Stop-hooks que reflexionan post-sesión y proponen updates a las reglas (anti-stale). Exploración cara (100k tok) → subagentes con context propio; el main loop recibe solo el resumen. `description` precisa = activación automática correcta.

## Aplicación a /atlas (los referentes CONFIRMAN el diagnóstico de bloat)

| Principio | Estado /atlas hoy | Fix |
|---|---|---|
| #1 Progressive disclosure | motor.md (~37k tok) se carga ENTERO siempre | partir en sub-docs cargados on-demand por modo/paso |
| #2 Lean core | motor.md = 3088 líneas (Cole: "no miles") | core <=300 líneas; resto layered |
| #3 Reglas atómicas | 830 líneas (27%) de comportamiento: 30 "prohibido", 66 frases-ejemplo | 5-10 reglas + ejemplos positivos; casos reales -> learned-patterns |
| #4 Scripts > prosa | mucha lógica bash inline en el .md | mover a `scripts/` verificables (patrón ya iniciado con graph-hints.sh) |
| #5 Dividir por dominio | motor mezcla flow + autonomía + comunicación + innovate + reporte | innovate (304L) y report (421L) -> archivos propios on-demand |
| #6 Self-improving | learned-patterns ya existe | sumar auto-poda + más exploración a subagentes |

## Anti-patterns (lo que NO hacer)
- Cargar todo el motor en cada invocación (viola #1 — es el costo recurrente #1).
- Acumular ejemplos de "frases prohibidas" en el core (viola #3 — el modelo nuevo ya obedece; los casos reales van al log).
- Lógica que el modelo "interpreta" en prosa larga (viola #4 — pasala a script).
- Un solo archivo monolito que hace todo (viola #2 y #5).
