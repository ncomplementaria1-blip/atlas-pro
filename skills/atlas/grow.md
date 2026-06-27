# ATLAS_MODE=grow · EL CICLO DE CRECIMIENTO DEL CEREBRO
> Cargado ON-DEMAND vía `/atlas grow` (2026-06-12 · orden Ale: "que atlas vaya
> creciendo su cerebro"). Cierra el loop que faltaba: el sistema ya CAPTURA
> experiencia (learned-patterns · telemetría · propuestas post-FAIL · post-mortems);
> este ciclo la DIGIERE y la consolida en el cerebro permanente.
>
> **El modelo mental:** el cerebro de /atlas son sus archivos (motor = leyes ·
> fable5/ = criterio · playbooks = técnica · projects/ = dominio). Crecer = que la
> experiencia vivida se convierta en archivo, con disciplina: cada lección al lugar
> correcto, deduplicada, aprobada por Ale, verificada por los exámenes. Sin este
> ciclo, las lecciones mueren como log; con él, cada incidente hace al sistema
> permanentemente mejor.
>
> **El techo, dicho honesto (P5):** los archivos elevan el CRITERIO hacia nivel
> Fable 5 — las preguntas correctas, el orden, las trampas. El horsepower de
> razonamiento lo pone el modelo ejecutor. PERO: en el dominio propio (tus
> proyectos, tus incidentes, tus leyes) el cerebro acumulado SUPERA al Fable
> genérico — conoce lo que ningún modelo trae de fábrica. Esa es la meta real:
> no imitar a Fable — superarlo EN TU CANCHA. ("No me cites — superame.")

## Cuándo corre

- **Manual:** `/atlas grow` — Ale lo pide.
- **Auto-propuesto (no auto-ejecutado):** el proxy (PASO 10) propone "/atlas grow"
  como candidato prioritario cuando un proyecto acumula **≥8 entradas sin
  `[CONSOLIDADO]`** en learned-patterns.md, o pasaron **≥30 días** del último ciclo
  (grow-history). El sistema PIDE digerir cuando está lleno — jamás se auto-modifica
  sin pasar por G2 (aprobación de Ale). Cero cron, cero wakeups (ley).

## El ciclo G0-G4

### G0 · COSECHA (inventario crudo · sin juicio todavía)

```bash
GROW_DIR="/tmp/atlas-grow-$(date +%s)"; mkdir -p "$GROW_DIR"
# Fuentes (todas las que existan):
# 1. learned-patterns.md de CADA proyecto (entradas sin [CONSOLIDADO])
# 2. eval/behavioral-history.jsonl (regresiones y sus causas)
# 3. git log de la skill desde el último grow (qué cambió y por qué — los mensajes
#    de commit son lecciones fechadas)
# 4. atlas-proxy-log.jsonl: tier estimado vs real (sobre-costos repetidos = lección)
# 5. intel briefs con REUTILIZABLE=sí ($ATLAS_DIR/intel/*.md de cada proyecto):
#    hallazgos del mundo (web/YouTube/TikTok) que el INTEL GATE marcó como patrón
#    permanente — el destilador decide su destino (playbook/criterio).
# PRIORIDAD (lección del ciclo grow-1): las fuentes VIVAS (telemetría de sesiones
# de atlas-log · proxy-log · behavioral-history · intel briefs) rinden más que
# re-cosechar learned-patterns ya consolidado — ese archivo es el feeder histórico
# del motor y sus lecciones ya fueron absorbidas al construirlo.
for pdir in "$HOME/.claude/skills/atlas/projects"/*/; do
  LP="$pdir/learned-patterns.md"
  [ -f "$LP" ] && grep -B1 -A6 '^---' "$LP" | grep -v 'CONSOLIDADO' >> "$GROW_DIR/cosecha.md"
done
LAST_GROW=$(tail -1 "$HOME/.claude/skills/atlas/eval/grow-history.jsonl" 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('motor_commit','HEAD~30'))" 2>/dev/null || echo "HEAD~30")
git -C "$HOME/.claude/skills/atlas" log --oneline "$LAST_GROW"..HEAD >> "$GROW_DIR/cosecha.md" 2>/dev/null
echo "COSECHA · $(grep -c '^---' "$GROW_DIR/cosecha.md" 2>/dev/null || echo 0) lecciones crudas"
```

### G1 · DESTILACIÓN (dispatch 1 agente **opus** · el paso de juicio)

Prompt del destilador (incluir AUTONOMIA_BLOCK + P5 completo como contexto):

```
Sos el destilador del cerebro de ATLAS. Recibís lecciones crudas (violaciones
capturadas, fallas de proceso, regresiones, sobre-costos). Tu trabajo: clasificar
CADA una en su destino correcto — o descartarla con razón.

DESTINOS (en orden de exigencia):
- LEY (motor.md inline): patrón de comportamiento que DEBE bloquearse siempre.
  Test: ¿prevenir esto justifica cargarlo en CADA invocación? Solo las always-on.
- CRITERIO (fable5/P*.md o transversal): juicio universal de método — cómo decidir,
  qué preguntar, qué trampa evitar. Universal = sirve en cualquier proyecto.
- TÉCNICA (playbook existente): conocimiento de herramienta/plataforma específica.
- DOMINIO (projects/<name>/flow-rules.md): regla que SOLO aplica a ese proyecto.
- RUIDO: incidente puntual sin patrón (typo, falla externa irrepetible) → descartar.

REGLAS DEL DESTILADOR:
1. Test de las 2 líneas (P5): si la ley no cabe en 2 líneas accionables, no
   entendiste el patrón — seguí destilando o descartá.
2. DEDUPE obligatorio: grep contra el cerebro existente ANTES de proponer. Si ya
   existe una ley/criterio que lo cubre → la lección confirma, no agrega: marcar
   [YA-CUBIERTO por <ley>]. El cerebro crece por calidad, no por volumen.
3. Anti-bloat: motor tiene presupuesto (eval cap +10%). Preferir SIEMPRE el destino
   más barato que funcione: DOMINIO < TÉCNICA < CRITERIO < LEY.
4. Cada propuesta con su diff EXACTO (archivo, sección, texto a insertar).

OUTPUT:
| # | Lección (resumen 1 línea) | Destino | Diff propuesto | Por qué ahí |
RESUMEN: N crudas → L leyes · C criterios · T técnicas · D dominio · R ruido · Y ya-cubiertas
```

### G2 · PROPUESTA A ALE (gate humano · inmune)

Presentar la tabla del destilador a Ale — completa, sin editorial, con los diffs.
**Nada se aplica sin su OK.** Esto NO es burocracia: un sistema que se auto-modifica
sin gate humano puede consolidar un error como ley (y el eval estructural no
detecta leyes equivocadas, solo leyes rotas). Ale puede aprobar todo, parte, o nada.

### G3 · CONSOLIDACIÓN (post-OK · con la red completa)

1. Aplicar SOLO los diffs aprobados, uno por destino.
2. `python3 eval/atlas-eval.py` → PASS obligatorio (presupuesto + gates intactos).
3. Si algún diff tocó motor.md de forma estructural (paso/gate/política) →
   correr la suite behavioral (eval/behavioral-suite.md) antes de dar por bueno.
4. Commit con mensaje `grow(atlas): ciclo N — X lecciones consolidadas` +
   detalle por destino.

### G4 · PODA + REGISTRO (cerrar el ciclo)

1. En cada learned-patterns.md: marcar las entradas consumidas con
   `[CONSOLIDADO grow-N → <destino>]` (NUNCA borrarlas — son el historial clínico).
   Las [YA-CUBIERTO] se marcan igual (confirman leyes existentes).
2. Append a `eval/grow-history.jsonl`:
   `{"ts": "2026-06-12T00:00:00Z", "ciclo": 1, "motor_commit": "abc1234",
   "crudas": 12, "leyes": 1, "criterios": 2, "tecnicas": 1, "dominio": 3,
   "ruido": 4, "ya_cubiertas": 1}`
3. Reportar a Ale: crecimiento del cerebro en números (líneas de criterio antes/
   después · ratio de digestión · edad de la lección más vieja pendiente).

## Métricas del cerebro (la salud del crecimiento)

- **Ratio de digestión** = consolidadas / capturadas. Sano: >70% tras cada ciclo.
  Un ratio bajo crónico = el sistema vive incidentes que no entiende (alerta P5).
- **Edad de la lección más vieja sin consolidar.** Sano: <45 días.
- **Densidad, no volumen:** si dos ciclos seguidos solo producen RUIDO/YA-CUBIERTO →
  el cerebro está maduro para su superficie actual — el crecimiento real vendrá de
  superficie nueva (features, proyectos), no de re-digerir lo mismo.

## Lo que este ciclo NO hace (límites por diseño)

- No se auto-aplica nada al motor sin Ale (G2 inmune).
- No corre solo en background (ley: cero cron/wakeups — el proxy lo PROPONE).
- No edita la suite behavioral ni las REF (el examen no aprende — P5-D3).
- No borra historial (poda = marcar, jamás eliminar).
