#!/usr/bin/env bash
# ATLAS Pro v1.0.0 · Script de instalacion universal
#
# Uso (modo local - desde el directorio de ATLAS):
#   bash atlas-setup.sh            # instalacion o reinstalacion completa
#   bash atlas-setup.sh --upgrade  # actualiza solo archivos del motor
#
# Uso (modo remoto - cuando se publique el repo):
#   bash <(curl -fsSL https://get.atlas-pro.dev/install.sh)
#
# --upgrade preserva projects/ y hace backup solo de los archivos del motor.
# Sin --upgrade hace backup completo del directorio de instalacion.

# Guard: requiere bash, no sh
[ -n "${BASH_VERSION:-}" ] || { echo "[ERROR] Este script requiere bash. Usar: bash atlas-setup.sh"; exit 1; }

set -euo pipefail

ATLAS_VERSION="1.0.0"
ATLAS_INSTALL_DIR="$HOME/.claude/skills/atlas"
ATLAS_PROJECTS_DIR="$ATLAS_INSTALL_DIR/projects"
CORE_FILES=("motor.md" "SKILL.md" "onboarding.md")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

UPGRADE_MODE=false
BACKUP=""

for arg in "$@"; do
  case "$arg" in
    --upgrade) UPGRADE_MODE=true ;;
    --help|-h)
      printf 'ATLAS Pro v%s\n' "$ATLAS_VERSION"
      printf 'Uso: bash atlas-setup.sh [--upgrade]\n\n'
      printf 'Sin flags:  Instalacion o reinstalacion completa.\n'
      printf '            Si ya existe instalacion, hace backup del directorio completo.\n'
      printf '\n'
      printf '  --upgrade  Actualiza solo los archivos del motor (motor.md, SKILL.md,\n'
      printf '             onboarding.md). El directorio projects/ no se toca.\n'
      printf '             Hace backup de los 3 archivos del motor antes de reemplazarlos.\n'
      printf '             Mas rapido que reinstalacion completa.\n'
      exit 0
      ;;
    *) printf '[ERROR] Argumento desconocido: %s · Usar --help para ver opciones\n' "$arg" >&2; exit 1 ;;
  esac
done

# ---------- logging ----------

log()   { printf '[ATLAS] %s\n' "$*"; }
warn()  { printf '[WARN]  %s\n' "$*" >&2; }
fail()  { printf '[ERROR] %s\n' "$*" >&2; exit 1; }

# Cleanup en fallo parcial
cleanup() {
  local code=$?
  if [ "$code" -ne 0 ]; then
    warn "Instalacion fallida (exit $code)"
    if [ -n "$BACKUP" ] && [ -e "$BACKUP" ]; then
      warn "Backup disponible: $BACKUP"
      warn "Para restaurar manualmente: mv \"$BACKUP\" \"$ATLAS_INSTALL_DIR\""
    fi
  fi
}
trap cleanup EXIT

# ---------- pre-checks ----------

log "ATLAS Pro v$ATLAS_VERSION · verificando requisitos..."

command -v python3 >/dev/null 2>&1 || fail "python3 requerido · instalar via brew (macOS) o apt (Linux)"
PYTHON_VER=$(python3 -c "import sys; print('%d.%d' % sys.version_info[:2])")
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" \
  || fail "python3 >= 3.8 requerido · version actual: $PYTHON_VER"
log "  python3 $PYTHON_VER OK"

if command -v git >/dev/null 2>&1; then
  log "  git $(git --version | awk '{print $3}') OK"
else
  warn "  git no encontrado · funciones de commit no disponibles"
fi

[ -d "$HOME/.claude" ] || fail "~/.claude no encontrado · instalar Claude Code: https://claude.ai/code"
log "  Claude Code OK"

[ -w "$HOME/.claude" ] || fail "Sin permisos de escritura en $HOME/.claude"

# Verificar archivos del motor (modo local)
for file in "${CORE_FILES[@]}"; do
  if [ ! -f "$SCRIPT_DIR/$file" ]; then
    fail "Archivo requerido no encontrado: $SCRIPT_DIR/$file · Verificar que el repo esta completo"
  fi
done

# ---------- instalacion ----------

log ""
if [ "$UPGRADE_MODE" = true ]; then
  log "Actualizando motor en $ATLAS_INSTALL_DIR (--upgrade)..."
else
  log "Instalando en $ATLAS_INSTALL_DIR..."
fi

# Backup segun modo
if [ -d "$ATLAS_INSTALL_DIR" ]; then
  BACKUP_SUFFIX="$(date +%Y%m%d-%H%M%S)-$$"
  if [ "$UPGRADE_MODE" = true ]; then
    # Backup liviano: solo los 3 archivos del motor (si existen)
    BACKED=0
    BACKUP="${ATLAS_INSTALL_DIR}.motor-bak.${BACKUP_SUFFIX}"
    mkdir -p "$BACKUP"
    for file in "${CORE_FILES[@]}"; do
      if [ -f "$ATLAS_INSTALL_DIR/$file" ]; then
        cp "$ATLAS_INSTALL_DIR/$file" "$BACKUP/"
        BACKED=$((BACKED + 1))
      fi
    done
    if [ "$BACKED" -gt 0 ]; then
      log "  Backup del motor ($BACKED archivo(s)): $(basename "$BACKUP")"
    else
      rmdir "$BACKUP" 2>/dev/null || true
      BACKUP=""
      log "  Sin archivos previos del motor · no se crea backup"
    fi
  else
    # Backup completo del directorio de instalacion
    BACKUP="${ATLAS_INSTALL_DIR}.bak.${BACKUP_SUFFIX}"
    cp -rP "$ATLAS_INSTALL_DIR" "$BACKUP"
    log "  Backup completo: $(basename "$BACKUP")"
  fi
fi

mkdir -p "$ATLAS_INSTALL_DIR" "$ATLAS_PROJECTS_DIR"

# Copiar archivos del motor (si src == dst, el archivo ya esta en su lugar)
UPDATED=0
SKIPPED=0
for file in "${CORE_FILES[@]}"; do
  src="$SCRIPT_DIR/$file"
  dst="$ATLAS_INSTALL_DIR/$file"
  if [ "$src" = "$dst" ]; then
    log "  $file (ya en destino · sin cambios)"
    SKIPPED=$((SKIPPED + 1))
  else
    cp "$src" "$dst"
    chmod 644 "$dst"
    log "  $file OK"
    UPDATED=$((UPDATED + 1))
  fi
done

PROJECT_COUNT=$(find "$ATLAS_PROJECTS_DIR" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
if [ "$PROJECT_COUNT" -gt 0 ]; then
  log "  projects/ preservado ($PROJECT_COUNT proyecto(s) intacto(s))"
else
  log "  projects/ creado (vacio · ejecutar /atlas para onboarding)"
fi

# ---------- verificacion ----------

log ""
log "Verificando instalacion..."

MISSING=0
for file in "${CORE_FILES[@]}"; do
  if [ ! -s "$ATLAS_INSTALL_DIR/$file" ]; then
    warn "  FALTA o vacio: $file"
    MISSING=$((MISSING + 1))
  fi
done

[ "$MISSING" -gt 0 ] && fail "Instalacion incompleta · $MISSING archivo(s) faltante(s)"

# Leer skill name via Python sin interpolacion de path en codigo (evita injection)
SKILL_NAME=$(python3 - "$ATLAS_INSTALL_DIR/SKILL.md" <<'PYEOF'
import re, sys
try:
    with open(sys.argv[1], encoding='utf-8') as f:
        m = re.search(r'^name:\s*(.+)$', f.read(), re.MULTILINE)
        if m:
            print(m.group(1).strip())
        else:
            print('atlas')
except Exception:
    print('atlas')
PYEOF
)
# Sanitizar: solo caracteres seguros para nombre de skill (previene terminal injection)
SKILL_NAME=$(printf '%s' "$SKILL_NAME" | tr -cd 'a-zA-Z0-9_-')
[ -z "$SKILL_NAME" ] && SKILL_NAME="atlas"

# ---------- resultado ----------

log ""
log "============================================"
log "ATLAS Pro v$ATLAS_VERSION instalado correctamente"
log "============================================"
log ""
log "  Skill:       /$SKILL_NAME"
log "  Motor:       $ATLAS_INSTALL_DIR/motor.md"
log "  Proyectos:   $ATLAS_PROJECTS_DIR/"
if [ "$UPDATED" -gt 0 ]; then
  log "  Copiados:    $UPDATED archivo(s)"
fi
if [ "$SKIPPED" -gt 0 ]; then
  log "  Sin cambio:  $SKIPPED archivo(s) (ya en destino)"
fi
[ -n "$BACKUP" ] && log "  Backup:      $(basename "$BACKUP")"
log ""
log "Proximos pasos:"
log "  1. Ir al directorio de tu proyecto:"
log "       cd /ruta/a/tu-proyecto"
log "  2. Abrir Claude Code y ejecutar:"
log "       /atlas"
log "  3. ATLAS detecta el proyecto automaticamente."
log "     Si no existe config, ejecuta el onboarding wizard."
log ""
log "Documentacion: $ATLAS_INSTALL_DIR/motor.md"
log ""
