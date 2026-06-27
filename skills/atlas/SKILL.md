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

# WORKTREE-AWARE (2026-06-12 · ley multisesión): si CWD es un worktree del repo,
# el path no matchea repo_path — resolver el repo PRINCIPAL vía git-common-dir.
if [ -z "$PROJECT_NAME" ]; then
  WT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null || echo "")
  if [ -n "$WT_COMMON" ] && [ "$WT_COMMON" != ".git" ]; then
    MAIN_REPO=$(dirname "$WT_COMMON")
    for dir in "$ATLAS_DIR_BASE"/*/; do
      [ -f "$dir/project.json" ] || continue
      REPO=$(python3 -c "import json; print(json.load(open('$dir/project.json')).get('repo_path',''))" 2>/dev/null || echo "")
      if [ -n "$REPO" ] && [ "$MAIN_REPO" = "$REPO" ]; then
        PROJECT_NAME=$(basename "$dir"); ATLAS_DIR="$dir"
        echo "ATLAS · worktree detectado · proyecto $PROJECT_NAME · operando en $CWD"
        break
      fi
    done
  fi
fi

if [ -z "$PROJECT_NAME" ]; then
  echo "ATLAS · proyecto no encontrado en config (CWD fuera de todo repo trackeado)"
  echo "FAZM: ATLAS sigue siendo el filtro de calidad UNIVERSAL aunque no haya proyecto."
  echo "FAZM: cargar SIEMPRE universal-craft-codex.md como vara 10/10. Luego rutear:"
  echo "  · onboarding (registrar este repo como proyecto ATLAS) → leer onboarding.md + wizard"
  echo "  · revisión/diseño suelto (mockup/HTML/asset sin repo) → MODO UNIVERSAL: aplicar el"
  echo "    codex + el playbook que aplique (cinematography/prompt-craft/motion…) directo,"
  echo "    sin pre-flight de repo. Reportar score contra el Gate Universal 10/10 del codex."
  ATLAS_DIR_BASE="$HOME/.claude/skills/atlas"
  UNIVERSAL_CODEX="$ATLAS_DIR_BASE/universal-craft-codex.md"
  exit 0
fi

echo "ATLAS · proyecto detectado: $PROJECT_NAME"
echo "FAZM: cargar motor.md y ejecutar con PROJECT_NAME=$PROJECT_NAME"
```

⛔ **LEY UNIVERSAL (binding · 2026-06-26):** `universal-craft-codex.md` es la vara de calidad BASE de ATLAS y se carga **siempre, en todo proyecto y aun sin proyecto**. El criterio de un proyecto = **codex (base) + su overlay** (`brand-context.md`; para NutricomAI también `worldclass-craft.md`). El overlay especializa el codex, nunca lo contradice.

Ruteo PASO 0:
- **Proyecto detectado** → leer `motor.md` (que carga el codex + overlay) y ejecutar con `$PROJECT_NAME`.
- **Sin proyecto, querés registrarlo** → leer `onboarding.md`, correr wizard, reiniciar desde aquí.
- **Sin proyecto, revisión/diseño suelto** (mockup, HTML, asset, video, ad — sin repo) → **MODO UNIVERSAL**: cargar el codex + el playbook que aplique y filtrar/puntuar contra el Gate Universal 10/10. No requiere pre-flight de repo.

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

# Palabras-comando/continuación: NO son componentes (significan "dale con lo último propuesto")
FILLER='^(dale+|arranc[aá]|arrancamos|segu[íi]|sigue|continu[aá]|vamos|listo|hazlo|hacelo|empez[aá]|vale|oka?y?|ok|s[íi]|ya|go|yes|eso|esa|ese)$'

if [ -z "$COMPONENTE_RAW" ]; then
  TASK_KIND="empty"
elif echo "$COMPONENTE_RAW" | grep -qiE "$FILLER"; then
  TASK_KIND="filler"      # "arranca", "dale", "seguí", "sí"... → continuación, no componente
else
  TASK_KIND="component"; COMPONENTE="$COMPONENTE_RAW"
fi
export TASK_KIND COMPONENTE
```

**Ruteo según `TASK_KIND` (FAZM decide · ⛔ NUNCA correr el flujo sobre una palabra-comando):**
- **`component`** → componente real → `PROXY_MODE=no` · cargar `motor.md` con `$COMPONENTE`.
- **`filler`** (`arranca`/`dale`/`seguí`/`sí`...) → es CONTINUACIÓN, no componente. Resolver el target en este orden:
  1. **Turno anterior** de esta conversación: si propuse una tarea/componente concreto ("¿arranco el splash?") → ESE es el target.
  2. **Checkpoint durable** (sobrevive compactación · incidente 2026-06-08): `python3 "$ATLAS_DIR/../../atlas-log.py" "$PROJECT_NAME" get-propuesta` → si ≠ NONE y `propuesta_ts` <48h → ese es el target.
  3. Ninguno → tratar como `empty`.
  Con target: `COMPONENTE`=el propuesto · `PROXY_MODE=no` · cargar `motor.md`. NO ir a proxy.
- **`empty`** → ni componente ni propuesta → `PROXY_MODE=yes` (PASO 10) y **pedir componente explícito**.

**LEY `propose` (cierra el loop de continuación):** cada vez que FAZM propone un siguiente task concreto al cierre de un run/reporte ("¿arranco X?") → registrarlo ANTES de cerrar: `python3 "$ATLAS_DIR/../../atlas-log.py" "$PROJECT_NAME" propose --componente "X"`. Sin registro, un "dale" futuro no tiene a qué volver.

**Si `PROXY_MODE=yes`:** saltar motor.md. Ir directo a PASO 10:
1. Estado del proyecto: `python3 "$ATLAS_DIR/../../atlas-monitor.py" "$PROJECT_NAME"` (config · progreso · componentes · checkpoint en un solo comando — el monitor lee los JSONs). **IGUAL reconciliar contra git real** (`git -C $PROJECT_REPO log --oneline -5` + `branch --show-current`): si el estado es más viejo que el último commit → marcarlo `[STALE]` y reportar lo que dice git, no el JSON.
2. Leer `$PROJECT_REPO/.claude/BACKLOG.md` → encontrar la primera tarea `[ ]` sin `[ALE]`
3. **REALITY-CHECK antes de proponer** (incidente 2026-06-08 "el splash ya está listo"): verificar que el deliverable del task NO exista ya (glob en `mockup_base_path` + `git log` reciente). Si existe → proponer el SIGUIENTE paso real (implementar/integrar), nunca recrear lo hecho.
4. Reportar: `PRÓXIMO TASK: [desc] — invocar /atlas <descripción>` + **aclarar** que se entró a proxy porque no diste componente (o usaste una palabra-comando), y que ese backlog es del hilo activo — nombrá uno para arrancar.

**Si `PROXY_MODE=no`:** cargar `motor.md` y ejecutar con `$PROJECT_NAME` y `$COMPONENTE` seteados.

---

## Flujo rápido (idéntico para todos los proyectos)

| Paso | Nombre | Bloqueante | Notas |
|------|--------|-----------|-------|
| 0 | Auto-detect + Pre-flight | Sí | Lock · typecheck · master · hook |
| 1 | Router + writing-plans | Sí | Clasifica tipo · platform · matu_mode |
| 1C | **Intel Gate** (universal) | Evalúa siempre | Investiga el mundo cuando hay trigger (deps/safety/API/técnica nueva) · cache TTL |
| 2 | Skills de diseño | Solo si creative_spin≠[] | TIER A siempre cuando aplica |
| 3 | Creative Spin | Solo si creative_spin≠[] | 3 mockups HTML A/B/C |
| 4 | Brand Council | Solo si creative_spin≠[] | Brand Guardian + UI Designer + fitness-ux |
| 5 | Implementación + checkpoint | Sí | /implement-mobile o web directo |
| 6 | Review + Smoke + Security + 6F + **6G Visual Diff** + **6H Director (video)** + **6I Essence (imagen)** | Sí | /review + /smoke-agent + 6F gate + **6G screenshots mobile+web** + **6H rúbrica cinematográfica si VIDEO_APPLIES** + **6I essence-check si IMAGE_APPLIES** |
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
- NUNCA saltear PASO 6G Visual Diff Loop si VISUAL_LOOP_APPLIES=yes (mobile o web)
- NUNCA saltear PASO 6H Director Review si VIDEO_APPLIES=yes (splash · orbe/totem · landing · ad) — el video no se shipea hasta 10/10
- NUNCA saltear PASO 6I Essence Gate si la tarea GENERÓ imagen (grok-cli · nano-banana) — sin lista de esencia + N/N PASS, el asset no se integra
- Modos: `/atlas design <cosa>` (PITCH de agencia · genera 3 conceptos impactantes divergentes · NO shipea · D0-D3) · `/atlas innovate` (ideación de features I0-I4) · `/atlas grow` (crecimiento del cerebro G0-G4) — todos on-demand. ⛔ ATLAS no es solo filtro: en `design` PROPONE diseño world-class aplicando `creative-direction-playbook.md` (motor) + `universal-craft-codex.md` (vara). NL "dame conceptos/diseños/opciones para X" → design mode.
- NUNCA re-correr agentes PASS en /matu Round 2+
- NUNCA push directo a main/master
- NUNCA invocar /atlas desde el proxy
- NUNCA llamar ScheduleWakeup ni CronCreate
- Si 3 STOP consecutivos en mismo componente → escalar con causa raíz

---

## PASO 6G · Visual Diff Loop (resumen · detalle en motor.md)

Universal mobile+web. Renderiza master HTML + impl real (simctl/adb mobile · Playwright web), compara con dos gates encadenados:

1. **6G-2.5 · Pre-gate pixelmatch (determinista · barato · rápido)** — `scripts/visual-diff-loop.mjs --compare` mide `diff_pct` con pixelmatch. Si `diff_pct ≤ 0.05` (5%) → `VISUAL_STATUS=PASS` automático, salta a PASO 7. Sin llamada a agente multimodal. **Sin tier1 bugs visibles en el diff PNG** (chequeo manual rápido del diff_png en zonas rojas concentradas).
2. **6G-3 · Multimodal loop (semántico · sólo si pre-gate FAIL)** — agente con vision compara IMÁGENES, 3 fases (INVENTARIO → MATRIZ → FIX PLAN), itera hasta `VISUAL_SCORE ≥ 9.5/10` o max 5 rounds.

Helper: `scripts/visual-diff-loop.mjs --platform=mobile|web --component=X --master=path --round=N --compare`. Output JSON con `master_png`, `impl_png`, `diff_png`, `diff_pct`, `status` (`PASS|FAIL`).

Web requiere dev server vivo (puerto configurable en `project.json:dev_server_port`). Mobile requiere emulator booted. Sin screenshot → `VISUAL_STATUS=BLOCKED` · push prohibido.

---

## PASO 6H · Director Review (video · resumen · detalle en motor.md + `cinematography-playbook.md`)

El director de foto para que **todo video sea 10/10**. Aplica cuando `VIDEO_APPLIES=yes` (splash pre-render · clip orbe/totem in-app · hero landing · ad/social · celebración Rive→video). Independiente del 6G.

1. **6H-1 · Detectar** — la tarea toca/produce un asset `.mp4/.mov/.webm` o una superficie de video conocida (`COMPONENTE` matchea video/splash/orbe/totem/landing/ad/...).
2. **6H-2 · Extraer frames** — `ffmpeg ... fps=2,tile=4x4` → contact-sheet PNG (misma técnica del youtube-study-playbook) + loop-check primer≈último frame.
3. **6H-3 · Review loop (fable · fallback opus)** — agente con vision puntúa los **10 ejes de la rúbrica** (`cinematography-playbook.md` §12: composición · lente/DOF · movimiento motivado · luz · grade · montaje · continuidad · sonido · lens-character · cero tells AI). PASS = promedio ≥9.5 Y ningún eje <8 Y cero tells AI (§13). Loop hasta 5 rounds refinando el plano que falló (no regenerar a ciegas).

El director es la VISIÓN; los brazos ejecutores son `grok-cli` (generativo), `/video` (mk-video), `/video-edit` (corte ffmpeg). Sin clip → `DIRECTOR_STATUS=BLOCKED` · push prohibido.
