#!/usr/bin/env bash
# ATLAS Pro — PUBLICAR mejoras (solo Ale/maintainer).
# Sincroniza tu skill de trabajo → este repo de distribución (sin tus proyectos privados),
# bumpea versión, y commitea+pushea para que todos los que tienen la skill puedan UPDATE.
#
# Uso:  ./PUBLISH.sh "<resumen del cambio>"   (la versión sale de skills/atlas/VERSION)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HOME/.claude/skills/atlas"          # tu copia de trabajo (con proyectos privados)
PKG="$HERE/skills/atlas"                   # copia limpia distribuible
MSG="${1:-update ATLAS}"

[ -d "$SRC" ] || { echo "ERROR: no encuentro tu skill en $SRC"; exit 1; }

echo "· Sincronizando contenido limpio (sin proyectos privados ni datos de aprendizaje)…"
rsync -a --delete \
  --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
  --exclude='*.flow-lock' --exclude='projects/' --exclude='eval/grow-history.jsonl' \
  "$SRC/" "$PKG/"
# Re-crear la plantilla de proyecto (se excluye projects/ pero _TEMPLATE debe viajar)
mkdir -p "$PKG/projects"
[ -d "$PKG/projects/_TEMPLATE" ] || echo "  (recordá mantener projects/_TEMPLATE en el repo)"

# NEUTRALIZACIÓN (repo público): borra todo término de marca/proyecto antes de publicar.
echo "· Neutralizando contenido (scrub público)…"
bash "$HERE/scrub-public.sh" "$PKG" >/dev/null

# GATE DURO: 0 hits de términos sensibles o se ABORTA el publish (jamás filtrar a público).
HITS="$(grep -rioE 'nutricom|esmeralda|estanque|mercadopago|whatsapp|19\.?628|\bTCA\b|alexia|fazm|cl[ií]nic' "$PKG" --include='*.md' 2>/dev/null || true)"
if [ -n "$HITS" ]; then
  echo "✗ ABORTADO: quedan términos sensibles tras el scrub. NO se publica."
  echo "$HITS" | head -20
  echo "→ Ampliá el mapa en scrub-public.sh y reintentá."
  exit 1
fi
echo "  ✓ scrub limpio (0 términos sensibles)."

VER="$(cat "$PKG/VERSION" 2>/dev/null || echo '?')"
echo "· Versión a publicar: $VER"

if [ ! -d "$HERE/.git" ]; then
  echo "Este paquete todavía no es repo git. Inicializalo y conectá el remoto privado:"
  echo "  cd \"$HERE\" && git init && git add -A && git commit -m 'ATLAS v$VER'"
  echo "  gh repo create atlas-pro --private --source=. --push   # (o tu remoto)"
  exit 0
fi

git -C "$HERE" add -A
git -C "$HERE" commit -m "ATLAS v$VER · $MSG" || { echo "(sin cambios para commitear)"; exit 0; }
echo "· Pusheando…"
git -C "$HERE" push
echo "✓ Publicado v$VER. Los usuarios reciben con: ./UPDATE.sh"
