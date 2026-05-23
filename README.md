# ATLAS Pro

Motor de calidad universal para Claude Code. Se instala una vez y funciona en cualquier proyecto.

ATLAS orquesta el flujo completo de implementacion UI: mockup → design council → codigo → calidad → commit. Sin atajos, sin improvisar.

---

## Instalacion

```bash
git clone https://github.com/ncomplementaria1-blip/atlas-pro.git /tmp/atlas-pro
bash /tmp/atlas-pro/atlas-setup.sh
```

O si ya lo tenes clonado:

```bash
bash atlas-setup.sh           # instalacion completa
bash atlas-setup.sh --upgrade # actualiza solo el motor (preserva projects/)
```

## Uso

```
cd /ruta/a/tu-proyecto
# Abrir Claude Code y ejecutar:
/atlas
```

ATLAS detecta el proyecto automaticamente. Si no existe config, ejecuta el wizard de onboarding.

---

## Que instala

- `~/.claude/skills/atlas/motor.md` — motor canónico de calidad
- `~/.claude/skills/atlas/SKILL.md` — skill definition para Claude Code
- `~/.claude/skills/atlas/onboarding.md` — wizard de proyecto nuevo
- `~/.claude/skills/atlas/projects/` — configs por proyecto (se genera en onboarding)

## Requisitos

- [Claude Code](https://claude.ai/code)
- bash (no sh)
- python3 >= 3.8
- git (opcional, para funciones de commit)

---

## Como funciona

1. `/atlas` detecta el proyecto desde `cwd`
2. Si no existe config → ejecuta onboarding (brief del producto, DNA visual, stack)
3. Si existe → carga motor.md con el contexto del proyecto
4. El motor orquesta: pre-flight → design → implementacion → review → matu → commit

Cada proyecto tiene su propio directorio en `~/.claude/skills/atlas/projects/<nombre>/` con brief, brand-context, matu-context, masters y flow-rules.

---

## Upgrade

```bash
bash atlas-setup.sh --upgrade
```

Actualiza `motor.md`, `SKILL.md` y `onboarding.md`. El directorio `projects/` no se toca.
