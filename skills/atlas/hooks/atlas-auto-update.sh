#!/usr/bin/env bash
# ATLAS auto-update — corre en SessionStart. Trae la última versión en background, silencioso.
# Solo actúa si la skill se instaló por SYMLINK a un repo git clonado. Nunca toca projects/ (gitignored).
DEST="$HOME/.claude/skills/atlas"
[ -L "$DEST" ] || exit 0   # instalada por copia → no auto-update (usar ./UPDATE.sh manual)

TARGET="$(python3 -c "import os,sys;print(os.path.realpath(sys.argv[1]))" "$DEST" 2>/dev/null)" || exit 0
REPO="$(cd "$TARGET/../.." 2>/dev/null && pwd)" || exit 0
[ -d "$REPO/.git" ] || exit 0

# pull rápido, no bloquear el arranque si no hay red; ff-only para nunca romper
( git -C "$REPO" pull --ff-only -q 2>/dev/null ) &
exit 0
