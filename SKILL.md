---
name: atlas
description: Use for ANY project when implementing UI components, new screens, refactors, or product changes. Triggers on "implementa", "codea", "nueva pantalla", "construye el componente", or any task referencing a master mockup + component. Auto-detects project from cwd. Runs onboarding wizard on first use if no project config exists. Required before touching any component file in any tracked project.
---

# /atlas — Motor de Calidad Universal

ATLAS es el motor canónico de calidad adaptable a cualquier proyecto. Se instala una vez y sirve para todos.

Para el detalle de cada paso: ver `motor.md`. Para nuevo proyecto: ver `onboarding.md`.

**LEY ABSOLUTA: Este es el único flujo válido para cualquier cambio UI/producto en proyectos ATLAS. No hay atajos.**

---

## PASO 0 — Auto-detección de proyecto (obligatorio · antes de motor.md)

```bash
CWD=$(pwd)
PROJECT_NAME=""
ATLAS_DIR_BASE="$HOME/.claude/skills/atlas/projects"

for dir in "$ATLAS_DIR_BASE"/*/; do
  [ -f "$dir/project.json" ] || continue
  REPO=$(python3 -c "import json; print(json.load(open('$dir/project.json')).get('repo_path',''))" 2>/dev/null || echo "")
  if [ -n "$REPO" ] && echo "$CWD" | grep -qF "$REPO"; then
    PROJECT_NAME=$(basename "$dir")
    ATLAS_DIR="$dir"
    break
  fi
done

if [ -z "$PROJECT_NAME" ]; then
  echo "ATLAS · proyecto no encontrado en config"
  echo "FAZM: leer onboarding.md y ejecutar el wizard antes de continuar"
  exit 0
fi

echo "ATLAS · proyecto detectado: $PROJECT_NAME"
echo "FAZM: cargar motor.md y ejecutar con PROJECT_NAME=$PROJECT_NAME"
```

Si proyecto detectado → leer `motor.md` y ejecutar con `$PROJECT_NAME` seteado.
Si no → leer `onboarding.md` y ejecutar el wizard, luego reiniciar desde aquí.

# Detección de MODO EXPEDITO

```bash
# Detectar en el mensaje del usuario antes de cargar motor.md
USER_MSG="[mensaje del usuario]"
MODO_TOTAL="no"
if echo "$USER_MSG" | grep -qiE "hazlo todo|modo auto|ejecuta todo|sin preguntas|dale|arrancamos|sigue solo|no me preguntes|todo tu|todo tú"; then
  MODO_TOTAL="yes"
  echo "MODO EXPEDITO activado · cero interrupciones · árbol de alternativas activo"
fi
export MODO_TOTAL
```

MODO_TOTAL se pasa a motor.md como variable de entorno.

# Detección de TASK · modo proxy si no hay tarea

```bash
# Extraer el task del mensaje del usuario (quitar "/atlas" y flags conocidos)
COMPONENTE_RAW=$(echo "$USER_MSG" | sed 's|/atlas||g; s|--eco||g' | xargs)

if [ -z "$COMPONENTE_RAW" ]; then
  # /atlas sin task → PASO 10 directo (proxy mode)
  echo "ATLAS · sin task especificado · activando modo proxy"
  PROXY_MODE="yes"
else
  PROXY_MODE="no"
  COMPONENTE="$COMPONENTE_RAW"
fi
export PROXY_MODE COMPONENTE
```

**Si `PROXY_MODE=yes`:** saltar motor.md. Ir directo a PASO 10:
1. Leer `$ATLAS_DIR/project-estado.json` → mostrar progreso y última acción
2. Leer `$PROJECT_REPO/.claude/BACKLOG.md` → encontrar la primera tarea `[ ]` sin `[ALE]`
3. Reportar: `PRÓXIMO TASK: [desc] — invocar /atlas <descripción>` para arrancar el flujo completo

**Si `PROXY_MODE=no`:** cargar `motor.md` y ejecutar con `$PROJECT_NAME` y `$COMPONENTE` seteados.

---

## Flujo rápido (idéntico para todos los proyectos)

| Paso | Nombre | Bloqueante | Notas |
|------|--------|-----------|-------|
| 0 | Auto-detect + Pre-flight | Sí | Lock · typecheck · master · hook |
| 1 | Router + writing-plans | Sí | Clasifica tipo · platform · matu_mode |
| 2 | Skills de diseño | Solo si creative_spin≠[] | TIER A siempre cuando aplica |
| 3 | Creative Spin | Solo si creative_spin≠[] | 3 mockups HTML A/B/C |
| 4 | Brand Council | Solo si creative_spin≠[] | Brand Guardian + UI Designer + fitness-ux |
| 5 | Implementación + checkpoint | Sí | /implement-mobile o web directo |
| 6 | Review + Smoke + Security | Sí | /review + /smoke-agent + 6F gate |
| 7 | /matu canonical o light | Sí | Incremental desde Round 2 · max 5 rounds |
| 8 | /qa (tests) | CREATE_NEW + REWRITE_COMPLEX | Post-/matu PASS |
| 9 | Commit + Push + PR | Sí | Guard main · lock release |
| 10 | Proxy · siguiente task | — | Reporta, NO invoca el flujo |

**creative_spin=[]** (REFACTOR_SIMPLE · EXTRACT · POLISH): saltar PASO 2, 3, 4 → implementar desde master directo.

**`--eco`**: fuerza creative_spin=[] + matu_mode=light. Solo si el cambio no toca critical_paths del proyecto.

---

## Los 2 STOP reales (universales · inmunes a cualquier modo)

1. Operación DB destructiva irreversible — DROP TABLE · DELETE masivo · migración elimina datos
2. Credenciales externas nuevas — nueva API key · nuevas env vars prod

Todo lo demás es autónomo.

---

## Reglas absolutas

- NUNCA saltear PRE-FLIGHT
- NUNCA saltear /smoke-agent
- NUNCA re-correr agentes PASS en /matu Round 2+
- NUNCA push directo a main/master
- NUNCA invocar /atlas desde el proxy
- NUNCA llamar ScheduleWakeup ni CronCreate
- Si 3 STOP consecutivos en mismo componente → escalar con causa raíz
