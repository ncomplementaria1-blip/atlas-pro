#!/usr/bin/env bash
# scrub-public — neutraliza términos de marca/proyecto en un árbol de ATLAS para release público.
# Uso: scrub-public.sh <dir-skills-atlas>
# Determinista. Acompañar SIEMPRE con el gate de 0-hits antes de publicar.
set -euo pipefail
ROOT="${1:?uso: scrub-public.sh <dir-skills-atlas>}"

find "$ROOT" -type f -name "*.md" -print0 | while IFS= read -r -d '' f; do
  perl -CSD -Mutf8 -0pi -e '
    s/OVERLAY\s+NutricomAI/OVERLAY de ejemplo (project-neutral)/gi;
    s/NutricomAI|Nutricom\s*AI/el proyecto/gi;
    s/\bNutricom\b/el proyecto/gi;
    s/\bFAZM\b/ATLAS/g;
    s/\bNEXUS\b/ATLAS/g;
    s/Alexia\w*/el asistente/gi;
    s/El\s+Estanque\w*|Estanque\w*/la dirección visual del proyecto/gi;
    s/\besmeralda\b/el color de acento/gi;
    s/Mercado\s*Pago/un proveedor de pagos/gi;
    s/\bWhatsApp\b/un canal de mensajería/gi;
    s/Ley\s*19\.?628|\b19\.?628\b/la normativa de protección de datos/gi;
    s/TCA-safe/safe-para-datos-sensibles/gi;
    s/\bTCA\b/datos sensibles/g;
    s/cl[ií]nic[ao]s/sensibles/gi;
    s/cl[ií]nic\w*/sensible/gi;
  ' "$f"
done
echo "scrub aplicado en $ROOT"
