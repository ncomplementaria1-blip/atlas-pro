#!/bin/bash
# atlas-gc.sh · Recolector de basura del ecosistema (2026-06-12 · orden Ale)
# DOS SCOPES (límite fijado por el clasificador de seguridad — correcto):
#  · AUTO (default · PASO 0 de cada run · sin cron): SOLO artefactos que ATLAS
#    mismo generó — tmp de gates, __pycache__ propio, intel vencido, worktree prune.
#  · --full (SOLO manual · orden explícita de Ale): suma basura pre-existente fuera
#    del scope — clones temp_subdir de plugins, crudos ~/yt +14d, caches Electron
#    de Claude Desktop. JAMÁS corre automático.
# REGLA DE ORO: solo basura CONOCIDA con filtro de edad. JAMÁS toca repos, docs,
# masters, telemetría, learned-patterns, historiales, assets.
# Uso: atlas-gc.sh [--dry] [--quiet] [--full]
set -u
DRY=""; QUIET=""; FULL=""
for a in "$@"; do [ "$a" = "--dry" ] && DRY=1; [ "$a" = "--quiet" ] && QUIET=1; [ "$a" = "--full" ] && FULL=1; done
ATLAS="$(cd "$(dirname "$0")" && pwd)"
FREED_KB=0

say() { [ -z "$QUIET" ] && echo "$@"; }
kb_of() { du -sk "$@" 2>/dev/null | awk '{s+=$1} END {print s+0}'; }
purge() {  # purge <etiqueta> <paths...>
  local label="$1"; shift
  [ $# -eq 0 ] && return 0
  local kb; kb=$(kb_of "$@")
  [ "${kb:-0}" -eq 0 ] && return 0
  if [ -n "$DRY" ]; then say "  [dry] $label · $((kb/1024))MB"; else
    rm -rf "$@" 2>/dev/null
    FREED_KB=$((FREED_KB + kb)); say "  GC · $label · $((kb/1024))MB liberados"
  fi
}

# 1. Artefactos de gates en /tmp con +2 días (los del run activo se conservan)
OLD_TMP=$(find /tmp -maxdepth 1 \( -name "atlas-visual" -o -name "atlas-director" \
  -o -name "atlas-grow-*" -o -name "paridad-*" -o -name "atlas-web-shot.*" \
  -o -name "atlas-dev.log" -o -name "atlas-eval-precommit.log" \) -mtime +2 2>/dev/null)
[ -n "$OLD_TMP" ] && purge "tmp gates (+2d)" $OLD_TMP

# 2. __pycache__ de la skill (regenerable)
PYC=$(find "$ATLAS" -type d -name "__pycache__" 2>/dev/null)
[ -n "$PYC" ] && purge "__pycache__" $PYC

# 2b. Session-locks STALE >2h (mismo umbral que el override del motor · PASO 0).
# Hace la limpieza PROACTIVA: antes solo se liberaba al reinvocar /atlas en ESE
# proyecto (red reactiva); ahora cualquier arranque limpia los locks colgados de
# TODOS los proyectos — cierra el caso del lock fantasma (sesión muerta de golpe
# que no disparó el trap EXIT ni llegó al PASO 9). Solo toca locks con locked=true
# y >2h; jamás un lock vivo (<2h = sesión real en curso).
LOCKS_CLEANED=$(python3 - "$ATLAS" << 'PY'
import json, glob, os, sys, datetime
n = 0
for lk in glob.glob(os.path.join(sys.argv[1], 'projects', '*', 'session-lock.json')):
    try:
        d = json.load(open(lk))
    except Exception:
        continue
    if not d.get('locked'):
        continue
    ts = d.get('ts')
    stale = True
    if ts:
        try:
            age_h = (datetime.datetime.now(datetime.timezone.utc) -
                     datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))).total_seconds() / 3600
            stale = age_h > 2.0
        except Exception:
            stale = True  # ts ilegible → tratar como stale
    if stale:
        json.dump({'locked': False, 'session': None, 'task': None,
                   'branch': None, 'ts': None, 'pid': None}, open(lk, 'w'), indent=2)
        n += 1
print(n)
PY
)
[ "${LOCKS_CLEANED:-0}" -gt 0 ] && say "  GC · $LOCKS_CLEANED session-lock(s) stale (>2h) liberado(s)"

# 3. [--full] Clones huérfanos del instalador de plugins (temp_subdir_*)
if [ -n "$FULL" ]; then
  TEMPS=$(find "$HOME/.claude/plugins/cache" -maxdepth 1 -name "temp_subdir_*" 2>/dev/null)
  [ -n "$TEMPS" ] && purge "plugins temp_subdir huérfanos" $TEMPS
fi

# 4. Intel briefs VENCIDOS (pasados 2× su TTL — doble margen de seguridad)
for f in "$ATLAS"/projects/*/intel/*.md; do
  [ -f "$f" ] || continue
  V=$(python3 - "$f" << 'PY'
import re, sys, datetime
t = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'fecha:\s*(\d{4}-\d{2}-\d{2})', t); n = re.search(r'ttl_dias:\s*(\d+)', t)
if m and n:
    age = (datetime.date.today() - datetime.date.fromisoformat(m.group(1))).days
    print('VENCIDO' if age > 2*int(n.group(1)) else 'OK')
else: print('OK')  # sin frontmatter parseable → no tocar
PY
)
  [ "$V" = "VENCIDO" ] && purge "intel vencido $(basename "$f")" "$f"
done

# 5. Worktrees muertos (refs colgantes) — prune en atlas + repos registrados
git -C "$ATLAS" worktree prune 2>/dev/null
for pj in "$ATLAS"/projects/*/project.json; do
  R=$(python3 -c "import json;print(json.load(open('$pj')).get('repo_path',''))" 2>/dev/null)
  [ -n "$R" ] && [ -d "$R/.git" ] && git -C "$R" worktree prune 2>/dev/null
done
say "  GC · worktree prune · refs muertas limpiadas"

# 6. [--full] Crudos de YouTube-study +14 días (síntesis ya extraída · copyright local)
if [ -n "$FULL" ] && [ -d "$HOME/yt" ]; then
  OLD_YT=$(find "$HOME/yt" -maxdepth 1 -type f \( -name "*.mp4" -o -name "*.webm" \
    -o -name "*.vtt" -o -name "*.png" \) -mtime +14 2>/dev/null)
  [ -n "$OLD_YT" ] && purge "yt crudos (+14d)" $OLD_YT
fi

# 7. [--full] Caches Electron de Claude Desktop (regenerables · precedente 1.8GB 2026-04)
CD="$HOME/Library/Application Support/Claude"
if [ -n "$FULL" ] && [ -d "$CD" ]; then
  CACHES=()
  for c in "Cache" "Code Cache" "GPUCache" "DawnGraphiteCache" "DawnWebGPUCache"; do
    [ -d "$CD/$c" ] && CACHES+=("$CD/$c")
  done
  KB=$(kb_of "${CACHES[@]:-}")
  # Solo si pasan de 300MB (no molestar por migajas)
  if [ "${KB:-0}" -gt 307200 ]; then purge "Claude Desktop caches" "${CACHES[@]}"; fi
fi

say "GC TOTAL · $((FREED_KB/1024))MB liberados$( [ -n "$DRY" ] && echo ' (dry-run: nada borrado)')"
exit 0
