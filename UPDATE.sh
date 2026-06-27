#!/usr/bin/env bash
# ATLAS Pro — actualizador para quien TIENE la skill.
# Trae las últimas mejoras del repo de distribución. Tus proyectos (projects/*) NO se tocan: están gitignored.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$HERE/.git" ]; then
  echo "Este paquete no es un repo git (se instaló por copia)."
  echo "Para recibir updates con un comando, pedí a quien te lo pasó el enlace del repo y cloná:"
  echo "  git clone <URL-del-repo-ATLAS> ~/atlas-pro && cd ~/atlas-pro && ./INSTALL.sh"
  exit 1
fi

echo "· Versión actual: $(cat "$HERE/skills/atlas/VERSION" 2>/dev/null || echo '?')"
echo "· Trayendo últimas mejoras…"
git -C "$HERE" pull --ff-only

echo ""
echo "✓ Actualizado a versión: $(cat "$HERE/skills/atlas/VERSION" 2>/dev/null || echo '?')"
echo "  Cambios: ver CHANGELOG → $HERE/skills/atlas/CHANGELOG.md"
echo ""
# Si la skill se instaló por COPIA (no symlink), re-copiar para aplicar el update
DEST="$HOME/.claude/skills/atlas"
if [ -L "$DEST" ]; then
  echo "  Instalada por symlink → el update ya está activo."
else
  echo "  Instalada por copia → re-aplicando a ~/.claude/skills/atlas (tus projects/ se preservan)…"
  rsync -a --delete \
    --exclude='projects/' --exclude='__pycache__' --exclude='*.pyc' \
    --exclude='*.flow-lock' --exclude='eval/grow-history.jsonl' \
    "$HERE/skills/atlas/" "$DEST/"
  echo "  ✓ aplicado."
fi
