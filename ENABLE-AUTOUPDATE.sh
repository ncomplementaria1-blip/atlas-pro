#!/usr/bin/env bash
# ATLAS — activar AUTO-UPDATE (opcional).
# Registra un hook SessionStart en ~/.claude/settings.json para que ATLAS se actualice
# solo, en background, cada vez que abrís Claude Code. Requiere haber instalado por SYMLINK
# (./INSTALL.sh desde un clon git). Hace backup de settings.json y es idempotente.
set -euo pipefail

SETTINGS="$HOME/.claude/settings.json"
HOOK_CMD="bash $HOME/.claude/skills/atlas/hooks/atlas-auto-update.sh"

mkdir -p "$HOME/.claude"
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
cp "$SETTINGS" "$SETTINGS.bak.$(date +%Y%m%d-%H%M%S)"

python3 - "$SETTINGS" "$HOOK_CMD" <<'PY'
import json, sys
path, cmd = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(path))
except Exception:
    d = {}
hooks = d.setdefault("hooks", {})
ss = hooks.setdefault("SessionStart", [])
# ¿ya está? (idempotente)
exists = any(
    any(h.get("command") == cmd for h in entry.get("hooks", []))
    for entry in ss if isinstance(entry, dict)
)
if not exists:
    ss.append({"hooks": [{"type": "command", "command": cmd}]})
    json.dump(d, open(path, "w"), indent=2)
    print("ok-added")
else:
    print("ok-already")
PY

echo "✓ Auto-update activado. ATLAS se actualizará solo al abrir Claude Code."
echo "  (Backup de settings.json guardado. Para desactivar: editá ~/.claude/settings.json y quitá el hook atlas-auto-update.)"
