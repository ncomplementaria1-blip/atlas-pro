# ATLAS · Onboarding de Proyecto Nuevo

Se ejecuta cuando ATLAS no encuentra config para el proyecto activo en cwd.
ATLAS ejecuta este protocolo completo antes de iniciar motor.md.

---

## Fase 1 · Auto-detección desde el repo

```bash
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PACKAGE_JSON="$GIT_ROOT/package.json"

# Monorepo fallback: si no hay package.json en la raíz, buscar en apps/* o packages/*
if [ ! -f "$PACKAGE_JSON" ]; then
  PACKAGE_JSON=$(find "$GIT_ROOT/apps" -maxdepth 2 -name "package.json" 2>/dev/null | head -1 || \
                 find "$GIT_ROOT/packages" -maxdepth 2 -name "package.json" 2>/dev/null | head -1 || \
                 echo "")
fi

PROJECT_NAME_GUESS=$(basename "$GIT_ROOT")

if [ -f "$PACKAGE_JSON" ]; then
  HAS_EXPO=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); print('yes' if 'expo' in str(d.get('dependencies',{})) or 'expo' in str(d.get('devDependencies',{})) else 'no')" 2>/dev/null || echo "no")
  HAS_NEXTJS=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); print('yes' if 'next' in str(d.get('dependencies',{})) else 'no')" 2>/dev/null || echo "no")
  TYPECHECK_GUESS=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); s=d.get('scripts',{}); print('npm run typecheck' if 'typecheck' in s else ('npx tsc --noEmit' if 'typescript' in str(d.get('devDependencies',{})) else 'echo OK'))" 2>/dev/null || echo "npm run typecheck")
  HAS_SUPABASE=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); print('yes' if 'supabase' in str(d) or '@supabase' in str(d) else 'no')" 2>/dev/null || echo "no")
  HAS_un proveedor de pagos=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); print('yes' if 'un proveedor de pagos' in str(d).lower() else 'no')" 2>/dev/null || echo "no")
  AUTH_GUESS=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); s=str(d); print('clerk' if 'clerk' in s else ('next-auth' if 'next-auth' in s else ('supabase-auth' if 'supabase' in s else 'por definir')))" 2>/dev/null || echo "por definir")
  DB_GUESS=$(python3 -c "import json; d=json.load(open('$PACKAGE_JSON')); s=str(d); print('supabase' if '@supabase' in s else ('prisma' if 'prisma' in s else ('drizzle' if 'drizzle' in s else 'por definir')))" 2>/dev/null || echo "por definir")
fi

if [ "$HAS_EXPO" = "yes" ] && [ "$HAS_NEXTJS" = "yes" ]; then
  PLATFORM_GUESS="ambos (mobile + web)"
elif [ "$HAS_EXPO" = "yes" ]; then
  PLATFORM_GUESS="mobile"
else
  PLATFORM_GUESS="web"
fi
```

---

## Fase 2 · Project Brief

ATLAS genera y muestra el siguiente brief pre-llenado con los valores auto-detectados.
Presentarlo completo al cliente en UN mensaje y pedir que lo complete o corrija en UNA respuesta.

```
ATLAS detectó tu proyecto. Completá o corregí este brief — una sola respuesta, sin formato especial.
Todo lo que no toques queda como está.

---

# Project Brief — $PROJECT_NAME_GUESS

## El producto
Qué es: [describí en 1-2 oraciones qué hace el producto]
Tagline: [1 línea que captura la promesa del producto]
Qué NO es: [anti-definición — qué categoría vecina NO es este producto]

## Audiencia
Para quién: [quién lo usa · edad · contexto · primera vez con este tipo de producto?]
Momento de uso: [cuándo lo usan · qué estado emocional tienen en ese momento]

## Mercado
País / región: [CL / MX / AR / US / otro]
Moneda: [CLP / MXN / ARS / USD / otro]
Compliance especial: [ninguno / datos de salud / pagos regulados / sector legal / describir]

## Identidad visual
Modo: [dark first / light first]
Color primario: [hex o "por definir"]
Color highlight: [hex o "auto-calcular desde primario"]
Tipografía: [nombre de la fuente o "system default"]
Entidad central: [nombre del personaje/mascota o "ninguno"]
Cómo se ve/comporta: [descripción breve o "N/A"]

## Tono de voz
Adjetivos: [3 palabras que describen el tono — ej: cálido · directo · experto]
Sí diría: "[ejemplo de frase que SÍ encaja con la marca]"
Nunca diría: "[ejemplo de frase que NUNCA diría la marca]"

## Stack (auto-detectado — confirmar o corregir)
Framework: $PROJECT_NAME_GUESS (detectado desde package.json)
Plataforma: $PLATFORM_GUESS
Typecheck: $TYPECHECK_GUESS
Auth: $AUTH_GUESS
DB: $DB_GUESS
Deploy target: [vercel / amplify / railway / otro]

## Tu perfil (para que ATLAS te hable como vos necesitás)
Experiencia construyendo productos digitales: [ninguna / algo / bastante]
Cómo preferís que te explique las cosas: [en simple, sin tecnicismos / con términos técnicos está bien]
Idioma: [español / inglés / español con inglés está bien]
Cuando ATLAS use un término técnico nuevo: [explicámelo siempre / solo si es muy específico / no hace falta]
Cómo escribís normalmente: [formal / casual / con humor / directo y breve]
Qué te frustra más cuando algo no funciona: [no entender qué pasó / no ver avance / no saber cuánto falta]

---

Completá lo que falta y corregí lo que esté mal. El resto lo genero yo.
```

---

## Fase 3 · Extracción y generación de archivos

Cuando el cliente devuelve el brief completado, ATLAS:

1. Lee el brief completo como texto
2. Extrae los valores de cada campo (como AI — no regex; interpretar lenguaje natural)
3. Genera los archivos de config

```bash
mkdir -p "$HOME/.claude/skills/atlas/projects/$PROJECT_NAME"
```

### project-brief.md

Guardar el brief completado tal cual lo escribió el cliente, con encabezado:

```markdown
# Project Brief — [PROJECT_NAME]
<!-- Generado en onboarding ATLAS · editable en cualquier momento -->
<!-- Este archivo es contexto vivo — los agentes lo leen en cada run -->

[brief completo tal como lo devolvió el cliente]
```

### project.json

Extraer del brief y generar:

```json
{
  "name": "[nombre del proyecto]",
  "tagline": "[tagline extraído del brief]",
  "repo_path": "[GIT_ROOT]",
  "typecheck_cmd": "[TYPECHECK_GUESS]",
  "platform": "[mobile | web | both — desde plataforma del brief]",
  "deploy": "[deploy target del brief]",
  "country": "[código país 2 letras — CL / MX / AR / US]",
  "critical_paths_regex": "schema|migration|payment|auth|credentials|\\.env",
  "staging_paths_regex": "^(src/|components/|app/|packages/)",
  "matu_mode_default": "canonical",
  "creative_spin_enabled": true,
  "branch_prefix_create": "feat",
  "branch_prefix_refactor": "refactor",
  "smoke_platform": "[mismo que platform]",
  "mockup_base_path": "docs/mockups",
  "implement_mobile_skill": "/implement-mobile",
  "proxy_compass_skill": "",
  "proxy_backlog": ".claude/BACKLOG.md"
}
```

Ajustes automáticos post-extracción:
- Si `platform = "ambos"` → `"platform": "both"` en JSON
- Si `HAS_un proveedor de pagos = "yes"` → agregar `"un proveedor de pagos"` al `critical_paths_regex`
- Si compliance menciona "pagos" → agregar `"payment"` si no está ya
- Si compliance menciona "salud" o "médico" → agregar `"health|medical"` al regex

### brand-context.md

ATLAS genera el DESIGN_AGENCY_BLOCK adaptado usando los campos del brief:
- Color primario + highlight → gradiente de marca
- Tipografía → instrucción de uso en display/body
- Entidad central → descripción de comportamiento visual
- Tono de voz → restricciones de copy
- Qué NO es → sección ANTI-SLOP específica del proyecto
- Audiencia + momento de uso → briefing de diseño emocional

Formato: seguir la estructura del bloque DESIGN_AGENCY_BLOCK — estándar de agencia, DNA visual, workflow interno, divergencia obligatoria, anti-slop, subordinación al master.

### matu-context.md

ATLAS genera el contexto para agentes /matu usando:
- Producto + tagline + audiencia + momento de uso
- Stack detectado
- País + compliance + moneda
- Entidad de marca y tono
- Estado inicial del producto: "en desarrollo · onboarding completado"

Formato: producto + stack + audiencia + país + compliance + DNA visual + estado actual del producto en secciones claras.

### masters.json

```json
{
  "components": {},
  "fallback": "",
  "note": "Vacío al inicio. Ale agrega entries cuando genera y aprueba masters. ATLAS puede sugerir paths si detecta HTML en docs/mockups/."
}
```

### flow-rules.md

ATLAS genera las reglas específicas del proyecto:
- Compliance activo y restricciones de tono (de la sección Compliance + Tono del brief)
- Proxy behavior: referencia al BACKLOG del repo (`<BACKLOG_PATH>`)
- Contexto de Security Council: producto + stack + país + compliance en 4 líneas
- Anti-patterns derivados del "Nunca diría" y "Qué NO es" del brief

### project-estado.json

```bash
python3 -c "
import json, datetime
estado = {
  'inicio': datetime.datetime.utcnow().isoformat() + 'Z',
  'ultima_sesion': None,
  'ultima_accion': 'Proyecto iniciado · onboarding completado',
  'componentes_listos': [],
  'componentes_pendientes': [],
  'progreso_pct': 0,
  'sesiones_totales': 0,
  'proximo_paso': 'Definir las primeras pantallas del producto',
  'hitos': {}
}
json.dump(estado, open('$HOME/.claude/skills/atlas/projects/$PROJECT_NAME/project-estado.json', 'w'), indent=2)
"
```

---

## Fase 4 · Confirmación y arranque

```
ATLAS ONBOARDING COMPLETO

Proyecto: [PROJECT_NAME]
Config: ~/.claude/skills/atlas/projects/[PROJECT_NAME]/

Archivos generados:
  project-brief.md   — brief vivo del producto
  project.json       — config del motor
  brand-context.md   — DNA visual para agentes de diseño
  matu-context.md    — contexto para agentes de calidad
  masters.json       — tabla de masters (vacía · agregar cuando haya mockups aprobados)
  flow-rules.md      — reglas y compliance del proyecto
  project-estado.json — estado y progreso del proyecto (inicia en 0%)

Releer SKILL.md y ejecutar motor.md con PROJECT_NAME=[PROJECT_NAME]
```

Procede con motor.md desde PASO 0 — el loop de auto-detección ahora encontrará el proyecto.

---

## Agregar master file (post-onboarding)

Cuando se genera y aprueba un master mockup para una pantalla:

```bash
python3 -c "
import json
path = '$HOME/.claude/skills/atlas/projects/$PROJECT_NAME/masters.json'
d = json.load(open(path))
d['components']['[componente]'] = '[path/relativo/al/master.html]'
json.dump(d, open(path,'w'), indent=2)
print('Master agregado: [componente] → [path]')
"
```

---

## Editar el brief después del onboarding

El brief es un documento vivo. Si el producto evoluciona:

```bash
# Editar directamente
$EDITOR "$HOME/.claude/skills/atlas/projects/$PROJECT_NAME/project-brief.md"

# Si cambió el DNA visual o tono → regenerar brand-context.md y matu-context.md
# ATLAS: leer el brief actualizado y reescribir los archivos afectados
```
