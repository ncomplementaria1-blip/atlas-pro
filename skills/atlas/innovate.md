# ATLAS · CICLO DE INNOVACIÓN (innovate mode)

> Cargado ON-DEMAND solo cuando ATLAS_MODE=innovate (`/atlas innovate`).
> Extraído de motor.md para no pesar en cada invocación de implementación
> (progressive disclosure · ver skill-design-playbook.md principio #1).

---

## ATLAS_MODE=innovate · CICLO DE INNOVACIÓN

**Trigger:** `/atlas innovate` | `/atlas innovate <área>`

ATLAS entra en modo innovación. No corre el flujo de implementación (PASO 0-10). Ejecuta discovery → síntesis → brand filter → output al BACKLOG.

```bash
INNOVATION_BACKLOG="$ATLAS_DIR/innovation-backlog.json"
INNOVATION_CONTEXT=$(python3 << PYEOF
import json, os
lines = []
try:
    estado = json.load(open("$ATLAS_DIR/project-estado.json", encoding="utf-8"))
    listos = estado.get("componentes_listos", [])
    pendientes = estado.get("componentes_pendientes", [])
    lines.append(f"Componentes listos ({len(listos)}): {', '.join(listos)}")
    lines.append(f"Componentes pendientes ({len(pendientes)}): {', '.join(pendientes)}")
    lines.append(f"Progreso: {estado.get('progreso_pct', 0)}%")
except Exception:
    lines.append("Estado: no disponible")
try:
    masters = json.load(open("$ATLAS_DIR/masters.json", encoding="utf-8"))
    comps = list(masters.get("components", {}).keys())
    lines.append(f"Secciones con master: {', '.join(comps)}")
except Exception:
    pass
try:
    prev = json.load(open("$INNOVATION_BACKLOG", encoding="utf-8"))
    prev_ideas = [i.get("titulo","") for i in prev.get("ideas",[]) if i.get("estado") not in ["implementada"]]
    if prev_ideas:
        lines.append(f"Ideas previas pendientes: {', '.join(prev_ideas[:5])}")
except Exception:
    pass
print("\n".join(lines))
PYEOF
)
BACKLOG_PREVIEW=$(head -40 "$BACKLOG_FILE" 2>/dev/null || echo "BACKLOG no accesible")
```

### PASO I0 · CONTEXT SCAN

```bash
echo "ATLAS · INNOVATE MODE"
echo "Proyecto: $PROJECT_DISPLAY_NAME · Sector: $PROJECT_SECTOR · Área: ${INNOVATE_AREA:-todo el producto}"
echo "$INNOVATION_CONTEXT"
```

### PASO I1 · DISCOVERY (4 agentes en paralelo)

Dispatchar en paralelo: `Trend Researcher` · `Product Manager` · `UX Researcher` · `Behavioral Nudge Engine`.

**Trend Researcher:**
```
[AUTONOMIA_BLOCK]

Sos un Trend Researcher especializado en innovación de producto digital.

PROYECTO: $PROJECT_DISPLAY_NAME
SECTOR: $PROJECT_SECTOR
ÁREA DE FOCO: ${INNOVATE_AREA:-todo el producto}
CONTEXTO DEL PRODUCTO: $PROJECT_BRIEF
ESTADO ACTUAL: $INNOVATION_CONTEXT

TAREA:
1. Identificá 4-5 tendencias concretas en apps de $PROJECT_SECTOR en $PREV_YEAR-$CURRENT_YEAR.
   Para cada tendencia: app que la implementa mejor · por qué funciona · cómo aplica en $PROJECT_DISPLAY_NAME.

2. Generá 5 ideas específicas (NO genéricas — deben ser únicamente aplicables a $PROJECT_DISPLAY_NAME):

Para cada idea usar este formato exacto:
IDEA: [título conciso]
TIPO: [sección | widget | feature | flujo | nueva_area | mejora_ux]
ESFUERZO: [S=<4h | M=1-3días | L=1-2sem]
IMPACTO: [alto | medio | bajo]
DESCRIPCIÓN: [2 líneas — qué es y cómo funciona]
REFERENCIA: [app que lo hace bien hoy]
```

**Product Manager:**
```
[AUTONOMIA_BLOCK]

Sos un Product Manager senior especializado en apps de $PROJECT_SECTOR.

PROYECTO: $PROJECT_DISPLAY_NAME
SECTOR: $PROJECT_SECTOR
ÁREA DE FOCO: ${INNOVATE_AREA:-todo el producto}
CONTEXTO DEL PRODUCTO: $PROJECT_BRIEF
ESTADO ACTUAL: $INNOVATION_CONTEXT
BACKLOG ACTUAL: $BACKLOG_PREVIEW

TAREA:
1. Identificá los 3 gaps más importantes del producto vs best-in-class en $PROJECT_SECTOR.

2. Generá 5 ideas priorizadas por impacto en retención/conversión/engagement:

Para cada idea:
IDEA: [título conciso]
TIPO: [sección | widget | feature | flujo | nueva_area | mejora_ux]
ESFUERZO: [S=<4h | M=1-3días | L=1-2sem]
IMPACTO: [alto | medio | bajo]
DESCRIPCIÓN: [2 líneas — qué es y qué problema resuelve]
MÉTRICA: [retención | conversión | engagement | NPS | revenue]
```

**UX Researcher:**
```
[AUTONOMIA_BLOCK]

Sos un UX Researcher experto en apps de $PROJECT_SECTOR con enfoque en behavioral design.

PROYECTO: $PROJECT_DISPLAY_NAME
SECTOR: $PROJECT_SECTOR
ÁREA DE FOCO: ${INNOVATE_AREA:-todo el producto}
CONTEXTO DEL PRODUCTO: $PROJECT_BRIEF
ESTADO ACTUAL: $INNOVATION_CONTEXT

TAREA:
Identificá oportunidades de mejora de experiencia en $PROJECT_DISPLAY_NAME.
Enfocate en: friction points del sector · progressive disclosure · empty states como momentos de engagement · micro-interactions que generan hábito · flujos rotos o costosos cognitivamente.

Generá 5 ideas específicas:

Para cada idea:
IDEA: [título conciso]
TIPO: [widget | flujo | micro-interaction | onboarding | empty-state | mejora_ux]
ESFUERZO: [S=<4h | M=1-3días | L=1-2sem]
IMPACTO: [alto | medio | bajo]
DESCRIPCIÓN: [2 líneas — qué cambia en la experiencia]
FRICTION: [qué fricción elimina o qué hábito crea]
```

**Behavioral Nudge Engine:**
```
[AUTONOMIA_BLOCK]

Sos un Behavioral Design specialist con expertise en motivación y engagement en apps de $PROJECT_SECTOR.

PROYECTO: $PROJECT_DISPLAY_NAME
SECTOR: $PROJECT_SECTOR
ÁREA DE FOCO: ${INNOVATE_AREA:-todo el producto}
CONTEXTO DEL PRODUCTO: $PROJECT_BRIEF

TAREA:
Diseñá mejoras basadas en psicología del comportamiento para $PROJECT_DISPLAY_NAME.
Frameworks: BJ Fogg Behavior Model · Self-Determination Theory · Variable Reward Loops · Social Proof · Implementation Intentions.

Generá 5 ideas específicas:

Para cada idea:
IDEA: [título conciso]
TIPO: [widget | feature | flujo | gamification | social | habit_loop | nudge]
ESFUERZO: [S=<4h | M=1-3días | L=1-2sem]
IMPACTO: [alto | medio | bajo]
DESCRIPCIÓN: [2 líneas — el mecanismo psicológico + cómo se implementa]
FRAMEWORK: [principio que lo sustenta]
```

### PASO I2 · SÍNTESIS

```bash
# ATLAS: capturar output real de los 4 agentes
IDEAS_TREND="[ATLAS: output real del Trend Researcher]"
IDEAS_PM="[ATLAS: output real del Product Manager]"
IDEAS_UX="[ATLAS: output real del UX Researcher]"
IDEAS_BEHAV="[ATLAS: output real del Behavioral Nudge Engine]"

for _var in IDEAS_TREND IDEAS_PM IDEAS_UX IDEAS_BEHAV; do
  _val="${!_var}"
  if echo "$_val" | grep -q "ATLAS: output real"; then
    echo "ERROR · $_var no fue reemplazado con el output del agente"
    exit 1
  fi
done
```

ATLAS consolida: desduplicar por título · rankear por score = impacto×esfuerzo (alto×S=9 · alto×M=6 · alto×L=3 · medio×S=6 · medio×M=4 · etc) · mantener top 15 ideas únicas ordenadas de mayor a menor score.

### PASO I3 · BRAND FILTER

Dispatchar 2 agentes en paralelo — `Brand Guardian` · `UI Designer`. Incluir DESIGN_AGENCY_BLOCK:

```
[AUTONOMIA_BLOCK]

[DESIGN_AGENCY_BLOCK]

Sos [AGENTE] · Innovation Brand Filter de $PROJECT_DISPLAY_NAME.

IDEAS A EVALUAR:
[lista consolidada del PASO I2 — top 15 ideas con su tipo/esfuerzo/impacto/descripción]

TAREA: Evaluá cada idea contra el DNA y posicionamiento de $PROJECT_DISPLAY_NAME.

Para cada idea usar este formato:
IDEA-N: PASS | FILTER | ADAPT
Razón: [1 línea]
Si ADAPT: [qué ajustar para que encaje]

CRITERIOS:
FILTER → rompe la identidad de marca, contradice el posicionamiento estratégico, introduce inconsistencia grave de producto
ADAPT → buena idea, mal framing o implementación — se puede ajustar y queda mejor
PASS → encaja con el DNA y suma al posicionamiento

NO filtrar ideas solo por ser ambiciosas o técnicamente complejas.
```

Agregación:
- PASS de ambos → PASS
- FILTER de alguno → revisar razón · si es objetiva → FILTER · si es subjetiva → PASS
- ADAPT de alguno → incorporar el ajuste → PASS_ADAPTED

### PASO I4 · OUTPUT

```bash
python3 << PYEOF
import json, datetime

atlas_dir = "$ATLAS_DIR"
backlog_file = "$BACKLOG_FILE"
innovation_file = f"{atlas_dir}/innovation-backlog.json"

# Cargar existente o crear
try:
    existing = json.load(open(innovation_file, encoding="utf-8"))
    ideas_existentes = existing.get("ideas", [])
    max_id = max((int(i.get("id","INV-000").split("-")[1]) for i in ideas_existentes if i.get("id","").startswith("INV-")), default=0)
except Exception:
    ideas_existentes = []
    max_id = 0

# ATLAS: reemplazar con lista real de ideas PASS/PASS_ADAPTED del PASO I3
# Formato de cada idea: {"titulo":..., "tipo":..., "esfuerzo":"S|M|L", "impacto":"alto|medio|bajo",
#   "descripcion":..., "fuente":"Trend Researcher|Product Manager|UX Researcher|Behavioral Nudge Engine",
#   "brand_filter":"PASS|PASS_ADAPTED", "estado":"propuesta", "area":"$INNOVATE_AREA"}
nuevas_ideas = []  # ATLAS: poblar con ideas reales

ts = datetime.datetime.utcnow().isoformat() + "Z"
for i, idea in enumerate(nuevas_ideas, start=max_id + 1):
    idea["id"] = f"INV-{i:03d}"
    idea["ts"] = ts
    idea["estado"] = "propuesta"

todas = ideas_existentes + nuevas_ideas
output = {
    "project": "$PROJECT_NAME",
    "sector": "$PROJECT_SECTOR",
    "generated_at": ts,
    "ideas": todas
}
json.dump(output, open(innovation_file, "w"), indent=2, ensure_ascii=False)

# Inyectar ideas S/M en BACKLOG.md
ideas_backlog = [i for i in nuevas_ideas if i.get("esfuerzo") in ("S", "M")]
if ideas_backlog:
    try:
        nuevas_tasks = f"\n## IDEAS INNOVACION · {ts[:10]}\n"
        for idea in ideas_backlog:
            desc = idea.get("descripcion","")[:80]
            nuevas_tasks += f"- [ ] [{idea['id']}] [{idea['tipo'].upper()}] {idea['titulo']} — {desc}\n"
        with open(backlog_file, "a", encoding="utf-8") as f:
            f.write(nuevas_tasks)
        print(f"  {len(ideas_backlog)} ideas S/M inyectadas en BACKLOG")
    except Exception as e:
        print(f"  WARN · BACKLOG no accesible: {e}")

n_l = [i for i in nuevas_ideas if i.get("esfuerzo") == "L"]
print(f"  Total ideas: {len(todas)} · Nuevas: {len(nuevas_ideas)} · En BACKLOG: {len(ideas_backlog)} · Sprint futuro (L): {len(n_l)}")
print(f"  → {innovation_file}")
PYEOF
```

**Output al usuario post-innovate:**

Si `USER_NIVEL=avanzado`:
```
ATLAS · INNOVATE · $PROJECT_DISPLAY_NAME
$N ideas generadas · $N_SM en BACKLOG (S/M) · $N_L para sprint futuro

Top ideas inmediatas (S/M, por score):
[lista top 5 con ID · tipo · título · esfuerzo · impacto]

Ideas de sprint (L):
[lista top 3 con ID · tipo · título]

→ innovation-backlog.json actualizado
→ /atlas <INV-ID> para implementar cualquiera
```

Si `USER_NIVEL=basico`:
```
Listo. Encontré $N ideas nuevas para $PROJECT_DISPLAY_NAME.

Las más rápidas de hacer ($N_SM ideas, menos de 3 días cada una):
[lista con nombre simple · para qué sirve · cuánto tarda]

Ideas más grandes para después ($N_L):
[lista con nombre simple · beneficio en 1 línea]

Próximo: `/atlas <ID>` para implementar la primera idea.
```

---

