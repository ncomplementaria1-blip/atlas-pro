#!/usr/bin/env bash
# ATLAS Pro — instalador.
# Modo recomendado: SYMLINK (si este paquete es un repo git clonado) → updates con `git pull`/UPDATE.sh
# en vivo, sin reinstalar. Fallback: COPIA (con backup si ya existe).
#   ./INSTALL.sh            → auto (symlink si es repo git, si no copia)
#   ./INSTALL.sh --copy     → fuerza copia
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/skills/atlas"
DEST_DIR="$HOME/.claude/skills"
DEST="$DEST_DIR/atlas"
MODE="${1:-auto}"

if [ ! -d "$SRC" ]; then
  echo "ERROR: no encuentro $SRC — ¿corrés esto desde la carpeta ATLAS-Pro?"
  exit 1
fi

mkdir -p "$DEST_DIR"

if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  BAK="$DEST_DIR/atlas.bak.$TS"
  echo "· Ya existe 'atlas' → backup en: $BAK"
  mv "$DEST" "$BAK"
fi

if { [ "$MODE" = "auto" ] && [ -d "$HERE/.git" ]; } || [ "$MODE" = "--symlink" ]; then
  ln -s "$SRC" "$DEST"
  echo "✓ ATLAS enlazado (symlink) → $DEST"
  echo "  Updates en vivo: corré  ./UPDATE.sh  (hace git pull) y listo."
else
  cp -R "$SRC" "$DEST"
  echo "✓ ATLAS instalado (copia) → $DEST"
  echo "  Updates: corré  ./UPDATE.sh  (re-aplica preservando tus projects/)."
fi

echo ""
echo "Versión instalada: $(cat "$SRC/VERSION" 2>/dev/null || echo '?')"
echo "Siguiente paso:"
echo "  1) Abrí Claude Code en tu proyecto."
echo "  2) Invocá  /atlas  y seguí el onboarding para registrar tu repo."
echo "     (copia projects/_TEMPLATE → projects/<tu-proyecto>, edita project.json + brand-context.md)"
echo "  3) Leé skills/atlas/universal-craft-codex.md (vara) + creative-direction-playbook.md (motor)."
