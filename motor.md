# ATLAS · Motor Genérico

Motor canónico de calidad. Se ejecuta después de que SKILL.md detecta el proyecto.
`$PROJECT_NAME` debe estar seteado antes de cargar este archivo.

---

## BIENVENIDA · lo primero que ve el usuario al invocar ATLAS

Antes de cualquier paso técnico, ATLAS muestra el estado actual del proyecto en lenguaje simple.
Esto es lo que ancla al usuario — nunca más se pierde en la línea de tiempo.

```bash
# Asegurar ATLAS_DIR disponible (CONFIGURACIÓN INICIAL puede no haber corrido aún)
ATLAS_DIR="${ATLAS_DIR:-$HOME/.claude/skills/atlas/projects/$PROJECT_NAME}"
ESTADO_FILE="$ATLAS_DIR/project-estado.json"

# Cargar estado o crear uno vacío si es primera vez
if [ ! -f "$ESTADO_FILE" ]; then
  python3 -c "
import json, datetime
estado = {
  'inicio': datetime.datetime.utcnow().isoformat() + 'Z',
  'ultima_sesion': None,
  'ultima_accion': 'Proyecto iniciado',
  'componentes_listos': [],
  'componentes_pendientes': [],
  'progreso_pct': 0,
  'sesiones_totales': 0,
  'proximo_paso': 'Definir las primeras pantallas del producto'
}
json.dump(estado, open('$ESTADO_FILE', 'w'), indent=2)
"
fi

PROGRESO=$(python3 -c "import json; print(json.load(open('$ESTADO_FILE', encoding='utf-8')).get('progreso_pct', 0))" 2>/dev/null || echo "0")
ULTIMA_ACCION=$(python3 -c "import json; print(json.load(open('$ESTADO_FILE', encoding='utf-8')).get('ultima_accion','Sesión anterior'))" 2>/dev/null || echo "")
LISTOS=$(python3 -c "import json; print(len(json.load(open('$ESTADO_FILE', encoding='utf-8')).get('componentes_listos',[])))" 2>/dev/null || echo "0")
PENDIENTES=$(python3 -c "import json; items=json.load(open('$ESTADO_FILE', encoding='utf-8')).get('componentes_pendientes',[]); print(', '.join(items[:3]) + ('...' if len(items)>3 else ''))" 2>/dev/null || echo "")
PROXIMO=$(python3 -c "import json; print(json.load(open('$ESTADO_FILE', encoding='utf-8')).get('proximo_paso',''))" 2>/dev/null || echo "")
```

**Output al usuario — SOLO al inicio de sesión (ATLAS habla al principio y al final, nunca en el medio):**

Si `USER_NIVEL=basico`:
```
Hola, acá estoy. Sigamos construyendo $PROJECT_NAME.

Progreso: [█ repetido PROGRESO/10 veces]░░ [PROGRESO]% listo
Última sesión: [ULTIMA_ACCION]
Pantallas terminadas: [LISTOS]
Hoy vamos a: [COMPONENTE] — [descripción en lenguaje simple]

Empiezo solo. Te aviso cuando esté listo.
```

Si `USER_NIVEL=avanzado`:
```
ATLAS · [PROJECT_NAME] · [PROGRESO]% · arrancando: [COMPONENTE]
```

**Después de este mensaje: silencio total hasta PASO 9.** El coach trabaja internamente.

---

## POLÍTICA DE AUTONOMÍA · ley máxima del motor

**Principio:** el usuario contrató a ATLAS para ejecutar, no para preguntar. Cada pregunta innecesaria es tiempo y tokens perdidos — el recurso más valioso.

### Las únicas 2 pausas reales (inmunes · siempre)
1. Operación DB destructiva irreversible — DROP TABLE · DELETE masivo · migración elimina datos
2. Credenciales externas nuevas — nueva API key · nueva cuenta de pago · nuevas env vars prod

Todo lo demás → **ATLAS decide y avanza.** Sin pausas intermedias. Sin rodeos.

### Tabla de decisiones autónomas (ATLAS decide solo — nunca pregunta)

| Decisión | ATLAS elige |
|---|---|
| A vs B técnico (librería, approach, pattern) | La opción recomendada en la skill o la más conservadora |
| Qué color usar si el brief no especifica | Derivar del color primario con algoritmo (lighten 20% para highlight) |
| Qué tipografía si no hay spec | La declarada en brand-context.md, siempre |
| Versión de dependencia | La estable más reciente compatible |
| Estructura de carpetas | La convención del proyecto detectada vía grep |
| Nombre de rama | `$BRANCH_PREFIX/$COMPONENTE-$(date +%Y%m%d)` automático |
| Qué mockup usar si no hay en masters.json | El fallback registrado |
| Matu mode si hay duda | canonical (más seguro) |
| Continuar o no con el siguiente paso | Continuar siempre, salvo los 2 STOP reales |
| Commit message | Generado automáticamente con formato definido |
| Agente a usar en cada paso | El definido en motor.md — sin consultar |

### Mensajes prohibidos en ATLAS (NUNCA generar)
- "¿Querés que continúe con...?"
- "¿Confirmas que...?"
- "¿A o B?"
- "¿Cuál preferís?"
- "¿Está bien si...?"
- "Antes de continuar, ¿...?"
- "¿Te parece si...?"

Si ATLAS siente el impulso de generar uno de estos → elegir la opción más razonable y reportar qué eligió al finalizar.

### Mecanismo de auto-respuesta (ATLAS se responde solo)

Cuando ATLAS necesita información que el usuario no sabe o no puede responder:

1. Buscar en `project-brief.md` — casi siempre la respuesta está ahí
2. Si no está en el brief → deducir desde el stack/plataforma/país del proyecto
3. Si no se puede deducir → elegir la opción más estándar para el tipo de proyecto
4. Reportar la decisión en 1 línea al final: "Elegí [X] porque [razón simple]"
5. **Nunca bloquear al usuario con una pregunta técnica que ATLAS puede resolver solo**

Ejemplos concretos:
- "¿Qué font-size para el título?" → leer el brand-context.md, extraer la jerarquía tipográfica
- "¿Qué color de fondo para este card?" → derivar del color base del brief + superficie elevada estándar
- "¿Cómo nombro este componente?" → seguir la convención de nombres detectada en el repo
- "¿Qué agente uso aquí?" → el definido en motor.md para este paso — sin deliberar

### Capa emocional · ATLAS transmite tranquilidad

ATLAS reconoce el estado emocional del proceso y comunica en consecuencia:

**Cuando algo tarda más de lo esperado:**
```
[nivel basico] → "Esto está tomando un poco más de lo normal — es porque [razón simple]. Sigo yo solo."
[nivel avanzado] → "Round extra en /matu por [motivo]. Resolviendo."
```

**Cuando algo falla y ATLAS lo arregla solo:**
```
[nivel basico] → "Encontré un problema, pero ya lo resolví. Seguimos."
[nivel avanzado] → "Fix aplicado · continuando."
```

**Cuando un componente queda listo:**
```
[nivel basico] → "[Componente] terminado y guardado. Vas [PROGRESO]% del camino."
[nivel avanzado] → "PASS · [componente] · commit [hash]"
```

**Cuando quedan pocas cosas:**
```
[nivel basico] → "Ya casi. Quedan [N] pantallas para tener el producto completo."
```

**Nunca:**
- Dramatizar errores o fallas técnicas
- Decir "no puedo" sin intentarlo
- Dejar al usuario sin saber qué pasa
- Terminar una sesión sin decir claramente qué sigue

---

## MODO EXPEDITO · "hazlo todo tú"

**Trigger (detectar en el mensaje del usuario):**
`"hazlo todo tú"` · `"modo auto"` · `"ejecuta todo"` · `"sin preguntas"` · `"dale"` · `"arrancamos"` · `"sigue solo"` · `"no me preguntes nada"` · cualquier indicación de ejecución autónoma completa.

```bash
MODO_TOTAL="yes"  # activado por trigger · también es el comportamiento recomendado por defecto
```

Cuando `MODO_TOTAL=yes` — ATLAS corre de corrido sin ninguna pausa:
- **Onboarding:** ATLAS completa los campos vacíos del brief con defaults razonables → no espera edición del usuario
- **PASO 1B arquitectura:** genera el mapa de screens → continúa directo a 1B-2 sin mostrar ni pedir "ok"
- **PASO 4 Brand Council:** aplica el mockup ganador → continúa sin notificación de cierre
- **Todo obstáculo técnico:** recorrer el árbol de alternativas antes de escalar

Los 2 STOP reales (operación DB destructiva · credenciales nuevas) siguen vigentes. Todo lo demás: resolver y avanzar.

### Árbol de alternativas · ATLAS nunca se bloquea

Ante cualquier obstáculo, ATLAS recorre las 3 alternativas antes de escalar. Escalar = último recurso con causa raíz documentada.

| Obstáculo | Alternativa 1 | Alternativa 2 | Alternativa 3 (último recurso) |
|---|---|---|---|
| Master file no encontrado | Usar fallback de masters.json | MAQUETA-MASTER global del proyecto | Generar master básico con PASO 1B-2 |
| Typecheck falla | Fix automático (errores TS frecuentes) | Anotar deuda en BACKLOG + continuar | TODO en el archivo + commit con nota |
| Agente falla o timeout | Retry con prompt simplificado | Agente alternativo del mismo dominio | FAZM sintetiza el output directamente |
| /matu sin PASS en R3 | Fix adicional de issues abiertos | Si avg≥9.2 y cero T1 → continuar con nota en PR | R4→R5 con redispatch selectivo |
| git push falla (sin remote) | Commit local + documentar en PR | `git remote add origin` + push | Exportar como `.patch` |
| Dependencia faltante | Instalar automáticamente | Alternativa equivalente sin esa dep | Mock temporal con TODO |
| Simulador no disponible (mobile) | Typecheck + snapshot como evidencia | Screenshot de componente aislado | Verificación manual marcada en PR |
| Archivo no encontrado | Buscar por patrón (`grep`, `find`) en repo | Inferir desde `git log` / `git blame` | Crear con template mínimo del proyecto |
| Conflicto de merge | Resolver automáticamente (no destructivo) | Rebase desde HEAD~1 | Stash + nueva branch + PR separado |
| Campo del brief vacío (onboarding) | Deducir desde stack/país/plataforma del repo | Usar el default más estándar del sector | Placeholder explícito + nota en brief |
| Chrome/Playwright no disponible | `curl` para verificar respuesta HTTP + typecheck estático | `puppeteer` CLI o `playwright` desde terminal | Screenshot manual + evidencia de código como fallback |
| Acción manual requerida (2FA · captcha · GUI nativa) | Instrucción de 3 pasos exacta con URL + nombres de campos | Grabar los pasos en BACKLOG con `[MANUAL]` y continuar el resto | Documentar el bloqueo con evidencia · no parar el flujo completo por un paso |

**Regla:** si las 3 alternativas fallan → reportar el bloqueo con causa raíz + qué se intentó. **Nunca reportar un bloqueo sin haber intentado al menos 2 alternativas.**

### Principio de acción manual · nunca delegar sin guía

Si un paso requiere que el usuario actúe (2FA, clic en GUI nativa, acceso a panel externo), ATLAS **nunca dice "hacelo vos"**. En cambio:

```
Lo que encontré: [descripción en 1 línea del obstáculo]
Para desbloquearlo, hacé esto (30 segundos):
  1. Abrí [URL exacta o "la app X"]
  2. Hacé clic en [nombre exacto del botón/campo]
  3. [acción específica — ej: "escribí tu código de 6 dígitos y confirmá"]
Cuando esté listo, decime "listo" y continúo.
```

La diferencia crítica: instrucción específica de 3 pasos con contexto vs. delegar sin guía. El usuario sabe exactamente qué hacer y tarda 30 segundos.

---

## AUTONOMIA_BLOCK · incluir en TODOS los prompts de Agent() dispatch

```
AUTONOMÍA: Sos parte de un flujo autónomo de ATLAS. Reglas absolutas:
1. NO preguntes entre pasos — decidí la opción más razonable y reportá tu elección.
2. Si hay A vs B, opción 1 vs 2, "which approach?" → elegí la recomendada o la más conservadora y avanzá.
3. Los únicos STOP reales: (a) operación DB destructiva irreversible, (b) credenciales externas nuevas.
4. Todo lo demás: ejecutá, reportá resultado, continuá al siguiente paso.
5. Tu reporte al finalizar debe incluir qué decidiste y por qué — no pedir confirmación de lo que ya hiciste.
```

FAZM: copiar este bloque textual al inicio de cada prompt de Agent() dentro del flujo.

---

## POLÍTICA DE COMUNICACIÓN · cómo habla ATLAS con el usuario

**Principio del coach interno:** ATLAS procesa, decide y resuelve en silencio. El usuario escucha SOLO dos veces por tarea: al inicio (BIENVENIDA) y al cierre (PASO 9). Todo lo del medio es trabajo interno — sin narrar, sin anunciar, sin confirmar pasos.

**Principio del lenguaje:** el usuario no tiene por qué aprender el vocabulario de ATLAS. ATLAS aprende el vocabulario del usuario.

### Cargar perfil del usuario

```bash
USER_NIVEL=$(python3 -c "
import re
brief = open('$ATLAS_DIR/project-brief.md', encoding='utf-8').read() if __import__('os').path.exists('$ATLAS_DIR/project-brief.md') else ''
exp = re.search(r'Experiencia.*?:\s*(.+)', brief)
if exp:
    v = exp.group(1).lower()
    if any(x in v for x in ['ninguna','nada','cero','no tengo']):
        print('basico')
    elif any(x in v for x in ['bastante','mucha','avanzad','experto']):
        print('avanzado')
    else:
        print('intermedio')
else:
    print('basico')
" 2>/dev/null || echo "basico")

USER_LANG=$(python3 -c "
import re
brief = open('$ATLAS_DIR/project-brief.md', encoding='utf-8').read() if __import__('os').path.exists('$ATLAS_DIR/project-brief.md') else ''
lang = re.search(r'Idioma.*?:\s*(.+)', brief)
if lang and 'ingl' in lang.group(1).lower():
    print('en')
else:
    print('es')
" 2>/dev/null || echo "es")

USER_EXPLAIN=$(python3 -c "
import re
brief = open('$ATLAS_DIR/project-brief.md', encoding='utf-8').read() if __import__('os').path.exists('$ATLAS_DIR/project-brief.md') else ''
exp = re.search(r'término técnico nuevo.*?:\s*(.+)', brief)
if exp and 'siempre' in exp.group(1).lower():
    print('siempre')
elif exp and 'no hace' in exp.group(1).lower():
    print('nunca')
else:
    print('cuando_aplica')
" 2>/dev/null || echo "siempre")
```

### Reglas según perfil

**Si `USER_NIVEL=basico`:**
- Todos los mensajes ATLAS COACH en español simple — sin términos técnicos sin explicar
- Cuando se introduce un término técnico nuevo → explicarlo en paréntesis la primera vez
- Nunca usar inglés sin traducción
- Reemplazar jerga técnica por descripción de lo que hace:
  - "typecheck" → "verifico que el código no tiene errores"
  - "commit" → "guardo el progreso"
  - "branch" → "abro una copia del proyecto para trabajar sin afectar lo que ya funciona"
  - "deploy" → "publico los cambios al sitio"
  - "merge" → "uno los cambios al proyecto principal"
  - "PR" → "propongo los cambios para revisión"
  - "dependencies" → "programas externos que el proyecto necesita"
  - "build" → "preparo la aplicación para que funcione en los dispositivos"

**Si `USER_NIVEL=intermedio`:**
- Español primario · términos técnicos comunes están bien (HTML, CSS, base de datos)
- Términos muy específicos: explicar la primera vez que aparecen
- Inglés: solo si no hay equivalente natural en español

**Si `USER_NIVEL=avanzado`:**
- Sin restricciones de vocabulario · comportamiento estándar

### Glosario dinámico

```bash
GLOSARIO_FILE="$ATLAS_DIR/glosario-usuario.md"
# FAZM: si USER_NIVEL=basico y se usa un término técnico por primera vez → agregarlo al glosario
# Formato: ## [término] → [explicación en 1 línea en español simple]
# No repetir explicaciones de términos que ya están en el glosario
```

---

## DESIGN_AGENCY_BLOCK · inyectar SOLO cuando creative_spin≠[] (PASO 3 + PASO 4)

```bash
# FAZM: leer el brand-context.md del proyecto e incluir verbatim como DESIGN_AGENCY_BLOCK
# NOTA: brand-context.md y matu-context.md son derivados de project-brief.md
# Si el brief fue editado → regenerar ambos antes de este paso:
#   FAZM lee el brief actualizado y reescribe brand-context.md + matu-context.md
BRAND_CONTEXT_FILE="$ATLAS_DIR/brand-context.md"
if [ ! -f "$BRAND_CONTEXT_FILE" ]; then
  echo "WARN · brand-context.md no encontrado · usando project-brief.md como fallback"
  DESIGN_AGENCY_BLOCK=$(cat "$ATLAS_DIR/project-brief.md" 2>/dev/null || echo "# Brand Context no disponible")
else
  DESIGN_AGENCY_BLOCK=$(cat "$BRAND_CONTEXT_FILE")
fi
```

NO incluir en REFACTOR_SIMPLE · EXTRACT · POLISH · --eco.

---

## CONFIGURACIÓN INICIAL · LOAD_PROJECT_CONFIG

FAZM: ejecutar este bloque al inicio de cada paso del motor para asegurar que las variables están seteadas.

```bash
# Guard: PROJECT_NAME debe estar seteado (via SKILL.md auto-detección)
if [ -z "$PROJECT_NAME" ]; then
  echo "FATAL · PROJECT_NAME no seteado · ejecutar SKILL.md primero"
  exit 1
fi

# Config del proyecto
ATLAS_DIR="${ATLAS_DIR:-$HOME/.claude/skills/atlas/projects/$PROJECT_NAME}"

PROJECT_REPO=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['repo_path'])" 2>/dev/null)
if [ -z "$PROJECT_REPO" ]; then
  echo "FATAL · PROJECT_REPO no encontrado · verificar $ATLAS_DIR/project.json"
  exit 1
fi
TYPECHECK_CMD=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['typecheck_cmd'])" 2>/dev/null || echo "npm run typecheck")
PLATFORM_DEFAULT=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['platform'])" 2>/dev/null || echo "mobile")
CRITICAL_PATHS_REGEX=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['critical_paths_regex'])" 2>/dev/null || echo "schema|migration|payment|auth|credentials|\\.env")
STAGING_PATHS_REGEX=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['staging_paths_regex'])" 2>/dev/null || echo "^(src/|components/|app/|packages/)")
DEPLOY_TARGET=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['deploy'])" 2>/dev/null || echo "vercel")
BRANCH_PREFIX_CREATE=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('branch_prefix_create','feat'))" 2>/dev/null || echo "feat")
BRANCH_PREFIX_REFACTOR=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('branch_prefix_refactor','refactor'))" 2>/dev/null || echo "refactor")
SMOKE_PLATFORM=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('smoke_platform','mobile'))" 2>/dev/null || echo "mobile")
IMPLEMENT_SKILL=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('implement_mobile_skill','/implement-mobile'))" 2>/dev/null || echo "/implement-mobile")
MOCKUP_BASE_PATH=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('mockup_base_path','docs/mockups'))" 2>/dev/null || echo "docs/mockups")
PROXY_COMPASS=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('proxy_compass_skill',''))" 2>/dev/null || echo "")
PROXY_BACKLOG=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('proxy_backlog','.claude/BACKLOG.md'))" 2>/dev/null || echo ".claude/BACKLOG.md")
PROJECT_DISPLAY_NAME=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json')).get('name', '$PROJECT_NAME'))" 2>/dev/null || echo "$PROJECT_NAME")
PROJECT_BRIEF=$(cat "$ATLAS_DIR/project-brief.md" 2>/dev/null || echo "")
CURRENT_YEAR=$(date +%Y)
PREV_YEAR=$((CURRENT_YEAR - 1))
MODO_TOTAL="${MODO_TOTAL:-no}"
CHECKPOINT_FILE="$PROJECT_REPO/.claude/flow-checkpoint.json"
BACKLOG_FILE="$PROJECT_REPO/.claude/BACKLOG.md"

cd "$PROJECT_REPO"
mkdir -p .claude/hooks
touch "$BACKLOG_FILE" 2>/dev/null || true
```

---

## Invocar

```
/atlas
/atlas <descripción del componente/cambio>
/atlas <descripción> <master-file>
/atlas --eco <descripción>
```

Sin argumentos: PROXY_MODE=yes → ir directo a PASO 10 (proxy) sin correr el motor.
Con `<master-file>`: path relativo al master mockup.
Sin `<master-file>`: lookup en masters.json del proyecto.

**`--eco`**: fuerza `creative_spin=[]` y `matu_mode=light`. No aplicar si el cambio toca critical_paths del proyecto.

---

## Lookup de MASTER_FILE

```bash
# Guard: si COMPONENTE vacío → PROXY_MODE (no debería llegar aquí, SKILL.md lo previene)
COMPONENTE="${COMPONENTE:-}"
if [ -z "$COMPONENTE" ]; then
  echo "ATLAS · COMPONENTE no especificado · activar PASO 10 (proxy)"
  # → saltar al PASO 10 directamente
fi

# FAZM: setear COMPONENTE desde el argumento o contexto antes de este bloque
COMPONENTE="${COMPONENTE:-[nombre del componente]}"

MASTER_FILE=$(python3 << PYEOF
import json, sys
atlas_dir = "$HOME/.claude/skills/atlas/projects/$PROJECT_NAME"
masters = json.load(open(f'{atlas_dir}/masters.json'))
components = masters.get('components', {})
fallback = masters.get('fallback', '')
comp = "$COMPONENTE".lower().replace('-','').replace('_','').replace(' ','')
# Fuzzy match
for key, path in components.items():
    k = key.lower().replace('-','').replace('_','')
    if k in comp or comp in k:
        if path and not path.startswith('/'):
            path = '$PROJECT_REPO/' + path
        print(path)
        sys.exit()
# fallback es relativo al repo — prefijarlo si no es absoluto
if fallback and not fallback.startswith('/'):
    fallback = '$PROJECT_REPO/' + fallback
print(fallback)
PYEOF
)
```

Si `MASTER_FILE` vacío → STOP · reportar a Ale · no continuar.

---

## PASO 0 · PRE-FLIGHT VALIDATOR (~0 tokens · bloqueante)

```bash
# FAZM: cargar config antes de este paso (CONFIGURACIÓN INICIAL arriba)
# COMPONENTE y MASTER_FILE ya seteados desde Lookup

# SESSION LOCK
LOCK_FILE="$PROJECT_REPO/.claude/session-lock.json"
FLOW_LOCK="$PROJECT_REPO/.claude/.flow-lock"

# Limpiar .flow-lock stale (>2h) automáticamente
if [ -f "$FLOW_LOCK" ]; then
  FLOW_LOCK_AGE=$(python3 -c "
import json, datetime
d = json.load(open('$FLOW_LOCK'))
ts = d.get('ts','')
if ts:
    locked_at = datetime.datetime.fromisoformat(ts.replace('Z','+00:00'))
    age_hours = (datetime.datetime.now(datetime.timezone.utc) - locked_at).total_seconds() / 3600
    print(f'{age_hours:.1f}')
else:
    print('99')
" 2>/dev/null || echo "99")
  IS_FLOW_STALE=$(python3 -c "print('yes' if float('$FLOW_LOCK_AGE') > 2.0 else 'no')" 2>/dev/null || echo "yes")
  if [ "$IS_FLOW_STALE" = "yes" ]; then
    echo "WARN · .flow-lock stale ($FLOW_LOCK_AGE h) · limpiando"
    rm -f "$FLOW_LOCK"
  fi
fi

LOCKED=$(python3 -c "
import json, sys
try:
    d = json.load(open('$LOCK_FILE'))
    print(d.get('locked', False))
except (FileNotFoundError, json.JSONDecodeError):
    print('False')
" 2>/dev/null || echo "False")

if [ "$LOCKED" = "True" ]; then
  LOCK_AGE=$(python3 -c "
import json, datetime
d = json.load(open('$LOCK_FILE'))
ts = d.get('ts','')
if ts:
    locked_at = datetime.datetime.fromisoformat(ts.replace('Z','+00:00'))
    age_hours = (datetime.datetime.now(datetime.timezone.utc) - locked_at).total_seconds() / 3600
    print(f'{age_hours:.1f}')
else:
    print('99')
" 2>/dev/null || echo "99")
  IS_STALE=$(python3 -c "print('yes' if float('$LOCK_AGE') > 2.0 else 'no')" 2>/dev/null || echo "no")
  if [ "$IS_STALE" = "yes" ]; then
    echo "WARN · SESSION LOCK STALE ($LOCK_AGE h) · override automático"
  else
    LOCK_SESSION=$(python3 -c "import json; d=json.load(open('$LOCK_FILE')); print(d['session'])" 2>/dev/null)
    LOCK_TASK=$(python3 -c "import json; d=json.load(open('$LOCK_FILE')); print(d['task'])" 2>/dev/null)
    echo "STOP · SESSION LOCK ACTIVO · sesión=$LOCK_SESSION · task=$LOCK_TASK"
    exit 1
  fi
fi

# Adquirir lock
SESSION_ID="${TERM_SESSION_ID:-terminal-$$}"
ATLAS_PID=$$
trap 'python3 -c "import json; open(\"$LOCK_FILE\",\"w\").write(json.dumps({\"locked\":False,\"session\":None,\"task\":None,\"branch\":None,\"ts\":None,\"pid\":None}, indent=2))"; rm -f "$FLOW_LOCK"' EXIT
python3 -c "
import json, datetime
with open('$LOCK_FILE', 'w') as f:
    json.dump({'locked': True, 'session': '$SESSION_ID', 'task': '$COMPONENTE',
               'branch': '$(git branch --show-current)',
               'ts': datetime.datetime.utcnow().isoformat() + 'Z', 'pid': $ATLAS_PID}, f, indent=2)
"
echo "Lock adquirido · sesión $SESSION_ID"

# Reset checkpoint
python3 -c "
import json, datetime
with open('$CHECKPOINT_FILE', 'w') as f:
    json.dump({'paso': 0, 'status': 'IN_PROGRESS', 'nuevo_flujo': True,
               'componente': '$COMPONENTE', 'master_file': '$MASTER_FILE',
               'proyecto': '$PROJECT_NAME',
               'ts': datetime.datetime.utcnow().isoformat() + 'Z'}, f, indent=2)
"

# Typecheck
TYPECHECK_OUTPUT=$($TYPECHECK_CMD 2>&1); TYPECHECK_EXIT=$?
echo "$TYPECHECK_OUTPUT" | tail -3
if [ "$TYPECHECK_EXIT" -ne 0 ]; then
  echo "FAIL · typecheck errors · arreglar antes de continuar"
  python3 -c "import json; open('$LOCK_FILE','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi
echo "TYPECHECK_EXIT=0"

# Merge conflicts
git status --short | grep -E "^(AA|DD|UU|AU|UA|DU|UD)" && echo "MERGE CONFLICT" || echo "OK"

# Master check
if [ ! -f "$MASTER_FILE" ] && [ -n "$MASTER_FILE" ]; then
  echo "WARN · master no encontrado: $MASTER_FILE"
  FALLBACK_MASTER=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/masters.json')).get('fallback',''))" 2>/dev/null || echo "")
  if [ -n "$FALLBACK_MASTER" ] && [ -f "$FALLBACK_MASTER" ]; then
    MASTER_FILE="$FALLBACK_MASTER"
    echo "FALLBACK → usando master general: $MASTER_FILE"
  else
    echo "FAIL · master no encontrado ni fallback"
    python3 -c "import json; open('$LOCK_FILE','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
    exit 1
  fi
fi
echo "Master OK: $MASTER_FILE"

# Hook check (warn only)
ls .claude/hooks/check-mobile-antipatterns.sh 2>/dev/null && echo "Hook OK" || echo "WARN · hook no encontrado · anti-pattern check se saltea"

# Actualizar checkpoint PASS
python3 -c "
import json
d = json.load(open('$CHECKPOINT_FILE'))
d['status'] = 'PASS'; d['paso'] = 0
json.dump(d, open('$CHECKPOINT_FILE','w'), indent=2)
"
```

---

## MODELO DE COSTO · referencia rápida

| Tier | Condición | Agentes totales | Tokens totales |
|---|---|---|---|
| VERDE | POLISH/EXTRACT + light + sin creative_spin | ~8 | ~70-100k |
| AMARILLO | REFACTOR_SIMPLE + light | ~12 | ~90-130k |
| NARANJA | CREATE_NEW/REWRITE + canonical + sin creative_spin | ~32 | ~200-280k |
| ROJO | CREATE_NEW/REWRITE + canonical + creative_spin≠[] | ~55+ | ~350-500k+ |

---

## PASO 1 · ROUTER (1 llamada · JSON compacto)

Dispatchar 1 agente `general-purpose`:

```
Analizá: [descripción]
Devolvé SOLO este JSON:
{
  "tipo": "CREATE_NEW | REWRITE_COMPLEX | REFACTOR_SIMPLE | EXTRACT | POLISH",
  "platform": "mobile | web",
  "matu_mode": "canonical | light",
  "creative_spin": ["Brand Guardian", "UI Designer"],
  "razon": "1 línea",
  "costo": {
    "tier": "VERDE | AMARILLO | NARANJA | ROJO",
    "agentes_estimados": N,
    "driver": "paso o factor que explica el tier en 5 palabras"
  }
}
Reglas tipo: CREATE_NEW=inexistente; REWRITE_COMPLEX=>3 useSharedValue/Skia/stagger; REFACTOR_SIMPLE=≤100 líneas; EXTRACT=sub-componente; POLISH=ajustes menores
Reglas matu_mode: canonical si CREATE_NEW/REWRITE_COMPLEX/safety; light si REFACTOR_SIMPLE/EXTRACT/POLISH
Reglas creative_spin: Brand Guardian si cambio visual; XR Architect si animaciones/depth; UI Designer si layout; Whimsy si onboarding/chat; UX si flows críticos; [] si REFACTOR_SIMPLE/EXTRACT
Reglas costo.tier: VERDE si POLISH/EXTRACT+light+sin_spin; AMARILLO si REFACTOR+light; NARANJA si CREATE_NEW/REWRITE+canonical+sin_spin; ROJO si CREATE_NEW/REWRITE+canonical+spin≠[]
```

### Parseo del output del Router

```bash
ROUTER_JSON_OUTPUT='[JSON devuelto por el agente]'
ROUTER_TIPO=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['tipo'])")
ROUTER_PLATFORM=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['platform'])")
MATU_MODE=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['matu_mode'])")
CREATIVE_SPIN_JSON=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['creative_spin']))")
COSTO_TIER=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['costo']['tier'])")
AGENTES_N=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['costo']['agentes_estimados'])")
COSTO_DRIVER=$(echo "$ROUTER_JSON_OUTPUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['costo']['driver'])")
```

### COSTO_GATE · post-Router

```bash
# Loguear
python3 -c "
import json, datetime
entry = {
  'ts': datetime.datetime.utcnow().isoformat() + 'Z',
  'evento': 'router_costo',
  'proyecto': '$PROJECT_NAME',
  'componente': '$COMPONENTE',
  'tier': '$COSTO_TIER',
  'agentes_estimados': int('$AGENTES_N') if '$AGENTES_N'.isdigit() else 0,
  'driver': '$COSTO_DRIVER'
}
with open('.claude/atlas-proxy-log.jsonl', 'a') as f:
    f.write(json.dumps(entry) + '\n')
"

# Si ROJO → buscar mockups previos
if [ "$COSTO_TIER" = "ROJO" ]; then
  KEYWORDS=$(echo "$COMPONENTE" | tr '[:upper:]' '[:lower:]' | tr ' /_-' '\n' | grep -E '.{3,}' | head -3 | tr '\n' '|' | sed 's/|$//')
  MOCKUP_DIR=$(find "$PROJECT_REPO/docs/mockups" -type d 2>/dev/null | grep -F "$COMPONENTE" | head -1)
  if [ -n "$MOCKUP_DIR" ]; then
    MOCKUP_COUNT=$(find "$MOCKUP_DIR" -maxdepth 1 -name "*.html" | wc -l | tr -d ' ')
    echo "OPTIMIZACION · tier ROJO pero existen $MOCKUP_COUNT mockups previos en $MOCKUP_DIR"
    echo "FAZM decide: si algún HTML de $MOCKUP_DIR cubre el cambio → setar creative_spin=[] y continuar desde PASO 5"
  else
    echo "WARN · tier ROJO · $AGENTES_N agentes estimados · driver: $COSTO_DRIVER"
  fi
fi
```

### Post-Router · checkpoint

```bash
python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 1; d['status'] = 'PASS'
d['router_tipo'] = '$ROUTER_TIPO'
d['router_platform'] = '$ROUTER_PLATFORM'
d['matu_mode'] = '$MATU_MODE'
d['creative_spin'] = $CREATIVE_SPIN_JSON
d['branch_name'] = '$(git branch --show-current)'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

### Post-Router · writing-plans

```bash
if { [ "$COSTO_TIER" = "ROJO" ] || [ "$COSTO_TIER" = "NARANJA" ]; } && \
   { [ "$ROUTER_TIPO" = "CREATE_NEW" ] || [ "$ROUTER_TIPO" = "REWRITE_COMPLEX" ]; }; then
  echo "WRITING_PLANS_NEEDED · tier=$COSTO_TIER · tipo=$ROUTER_TIPO"
  # FIRE-AND-FORGET: invocar superpowers:writing-plans "[descripción]"
  # No bloquea — continuar a PASO 2 inmediatamente
fi
```

### Post-Router · branch

```bash
if [ "$ROUTER_TIPO" = "CREATE_NEW" ] || [ "$ROUTER_TIPO" = "REWRITE_COMPLEX" ]; then
  git checkout -b "$BRANCH_PREFIX_CREATE/$COMPONENTE-$(date +%Y%m%d)" 2>/dev/null || \
  git checkout "$BRANCH_PREFIX_CREATE/$COMPONENTE-$(date +%Y%m%d)"
else
  git checkout -b "$BRANCH_PREFIX_REFACTOR/$COMPONENTE-$(date +%Y%m%d)" 2>/dev/null || \
  git checkout "$BRANCH_PREFIX_REFACTOR/$COMPONENTE-$(date +%Y%m%d)"
fi
```

---

## PASO 1B · PRODUCT ARCHITECTURE (auto · solo CREATE_NEW sin master)

**Por qué existe:** implementar componentes sin un mapa del producto completo genera inconsistencia entre pantallas. Un master único del producto entero evita que la pantalla 5 contradiga la pantalla 2.

Condición de activación:
```bash
NEEDS_ARCHITECTURE="no"
FALLBACK_MASTER=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/masters.json')).get('fallback',''))" 2>/dev/null || echo "")
if [ "$ROUTER_TIPO" = "CREATE_NEW" ] && [ -z "$FALLBACK_MASTER" ]; then
  NEEDS_ARCHITECTURE="yes"
fi
```

Si `NEEDS_ARCHITECTURE=no` → saltar directo a PASO 2.

### 1B-1 · Arquitectura del producto

Dispatchar 1 agente `general-purpose`. Prompt:

```
Sos un arquitecto de producto. Leé el brief del proyecto:

[PROJECT_BRIEF — contenido de project-brief.md]

Definí la arquitectura completa: TODOS los screens, flujos de navegación, secciones principales y componentes globales. No inventar nada que contradiga el brief. Completar lo que no especifica con decisiones razonables alineadas al producto.

Devolvé SOLO este formato:

# Product Architecture — [nombre]

## Screens (nombre · propósito en 1 línea)
1. [Screen] — [qué hace · cuándo aparece]
...

## Flujos de navegación
- Onboarding: [screen1 → screen2 → ...]
- Flujo principal: [tab bar / drawer / stack]
- Flujos críticos: [auth · pago · etc si aplica]

## Secciones por screen
### [Screen]
- Header: [contenido]
- Body: [secciones]
- CTA/Footer: [contenido]

## Componentes globales
- [nombre]: [descripción · en qué screens aparece]

## Estados
- Vacío: [cómo se ve sin datos]
- Error: [cómo se maneja]
- Carga: [skeleton · spinner · nada]

Máx 400 palabras. Decisiones concretas — cero "podría ser".
```

```bash
ARCH_FILE="$ATLAS_DIR/product-architecture.md"
# FAZM: escribir output del agente en $ARCH_FILE
```

Si `MODO_TOTAL=yes` → continuar directo a 1B-2 sin mostrar ni pausar. ATLAS elige la arquitectura generada.

Si `MODO_TOTAL=no` → mostrar al usuario y esperar "ok" o correcciones antes de 1B-2:
```
ATLAS · Arquitectura lista — [N screens · M flujos]

[contenido de product-architecture.md]

¿Algo que cambiar? → decime qué. ¿Todo bien? → "ok" y genero el master completo.
```
Si el usuario pide cambios → aplicar y continuar. Si dice "ok" → ir a 1B-2.

### 1B-2 · Full master HTML

Dispatchar agente `Frontend Developer`. Prompt:

```
[AUTONOMIA_BLOCK]

[DESIGN_AGENCY_BLOCK — brand-context.md]

[PROJECT_BRIEF — project-brief.md]

PRODUCT ARCHITECTURE:
[contenido de product-architecture.md]

TAREA: Generá un master HTML completo — TODOS los screens en una sola página scrolleable. Cada screen en su sección con separador y nombre visible.

REGLAS:
- Un solo archivo HTML · todos los screens en orden de flujo
- DNA visual exacto del brief: colores hex · tipografía · entidad de marca
- Copy real basado en el brief — cero lorem ipsum
- Cero emojis · cero placeholders genéricos
- Componentes globales (navbar, tab bar) en el primer screen que los use

OUTPUT: archivo HTML completo. No fragmentos.
```

```bash
FULL_MASTER_PATH="$PROJECT_REPO/$MOCKUP_BASE_PATH/MASTER-PRODUCTO-COMPLETO.html"
# FAZM: escribir output del agente en $FULL_MASTER_PATH

# Registrar como fallback en masters.json
python3 -c "
import json
path = '$ATLAS_DIR/masters.json'
d = json.load(open(path))
d['fallback'] = '$MOCKUP_BASE_PATH/MASTER-PRODUCTO-COMPLETO.html'
json.dump(d, open(path, 'w'), indent=2)
print('Master registrado como fallback')
"

# Actualizar MASTER_FILE para los pasos siguientes
MASTER_FILE="$FULL_MASTER_PATH"
```

# FAZM (interno): master en $FULL_MASTER_PATH · MASTER_FILE=$FULL_MASTER_PATH · continuar a PASO 2

---

## PASO 2 · SKILLS DE DISEÑO + TREND INTEL (paralelo · solo si creative_spin≠[])

Si `creative_spin=[]` → saltar PASO 2, 3, 4. Ir directo a PASO 5 desde master.

### Pre-PASO 2 · TREND INTEL (lanzar en paralelo con TIER A · no bloquear)

```bash
TREND_INTEL_FILE="$ATLAS_DIR/trend-intel-$COMPONENTE.md"
```

Dispatchar 1 agente `Trend Researcher` al mismo tiempo que los TIER A. Los resultados se consumen en PASO 3 — no bloquea la generación de skills.

Prompt:

```
[AUTONOMIA_BLOCK]

Sos un investigador de tendencias de diseño y producto. Tu trabajo es encontrar lo que está ganando HOY — no hace 6 meses — en esta categoría.

Producto: [descripción del brief · 2 líneas]
Plataforma: [ROUTER_PLATFORM]
Componente a diseñar: [COMPONENTE]

INVESTIGAR (usar WebSearch — buscar resultados de $PREV_YEAR-$CURRENT_YEAR):
1. "[categoría del producto] app design trends $CURRENT_YEAR"
2. "best [categoría] mobile UI $CURRENT_YEAR awwwards dribbble"
3. "UI design trends $CURRENT_YEAR typography color motion"
4. "[categoría] top apps $CURRENT_YEAR design"

OUTPUT (máx 250 palabras):
# Trend Intel — [COMPONENTE]

## Lo que está ganando ahora (con evidencia)
- [tendencia]: [cómo se ve · producto real que la usa · por qué gana]

## Lo que está agotado (evitar a toda costa)
- [patrón muerto]: [por qué ya no gana]

## Referentes world-class $PREV_YEAR-$CURRENT_YEAR
- [producto/diseño]: [lo que hace diferente · aplicable a este componente]

## Aplicación directa
- [insight concreto para $COMPONENTE basado en lo investigado]

Sé específico. Nombres reales. Tendencias verificables. Cero generalidades.
```

```bash
# FAZM (interno): escribir output en $TREND_INTEL_FILE
TREND_INTEL=$(cat "$TREND_INTEL_FILE" 2>/dev/null || echo "")
```

**TIER A Mobile** (siempre si creative_spin≠[]): `/frontend-design` · `/ui-ux-pro-max` · `/react-native-design` · `/react-state-management` · `/design-shotgun` · `/brand-guidelines`

**TIER A Web** (siempre si creative_spin≠[]): `/frontend-design` · `/ui-ux-pro-max` · `/nextjs-app-router-patterns` · `/tailwind-design-system` · `/react-state-management` · `/design-shotgun` · `/brand-guidelines`

**TIER B Mobile** (solo CREATE_NEW/REWRITE_COMPLEX): `/react-native-expert` · `/react-native-architecture` · `/building-native-ui` · `/fixing-motion-performance` (si animaciones)

**TIER C** (solo si hay data): `/native-data-fetching` (mobile) · `/postgresql-code-review` (ambas)

**TIER D** (condicional): `/design-html` si mockup previo necesita ajuste · `/design-review` si review de componente existente

Checkpoint post-PASO 2:
```bash
python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 2; d['status'] = 'PASS'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

---

## PASO 3 · CREATIVE SPIN (paralelo · solo si creative_spin≠[])

FAZM: leer `$ATLAS_DIR/brand-context.md` e incluir verbatim como DESIGN_AGENCY_BLOCK en cada prompt.

```bash
BRAND_CONTEXT_FILE="$ATLAS_DIR/brand-context.md"
if [ -f "$BRAND_CONTEXT_FILE" ]; then
  DESIGN_AGENCY_BLOCK=$(cat "$BRAND_CONTEXT_FILE")
else
  DESIGN_AGENCY_BLOCK=$(cat "$ATLAS_DIR/project-brief.md" 2>/dev/null || echo "")
fi
TREND_INTEL_FILE="$ATLAS_DIR/trend-intel-$COMPONENTE.md"
# El Trend Researcher fue dispatched en PASO 2 en paralelo; si aún no escribió → fallback
TREND_INTEL=$(cat "$TREND_INTEL_FILE" 2>/dev/null || echo "")
if [ -z "$TREND_INTEL" ]; then
  echo "WARN · trend-intel-$COMPONENTE.md no disponible · continuar sin tendencias externas"
  TREND_INTEL="Investigar tendencias actuales ($CURRENT_YEAR) en el sector antes de proponer dirección"
fi
```

Dispatchar agentes del `creative_spin` en paralelo. Prompt por agente:

```
[AUTONOMIA_BLOCK]

[DESIGN_AGENCY_BLOCK — contenido de brand-context.md]

[PROJECT_BRIEF — contenido de project-brief.md · contexto narrativo vivo del producto]

TREND INTEL — lo que está ganando HOY en este sector ($PREV_YEAR-$CURRENT_YEAR):
[TREND_INTEL — contenido de $TREND_INTEL_FILE]

Eres [AGENTE] en sprint creativo para [componente].
EJE ASIGNADO: [A=editorial/tipográfico | B=espacial/profundidad | C=material/táctil]
DIRECCIÓN ESTÉTICA: [síntesis de outputs TIER A del PASO 2]
MASTER (spec inmutable): [grep -Fn "$COMPONENTE" "$PROJECT_REPO/$MASTER_FILE" 2>/dev/null | head -10 || head -30 "$PROJECT_REPO/$MASTER_FILE" 2>/dev/null | head -10]
TAREA: UNA dirección visual de nivel agencia siguiendo el WORKFLOW INTERNO. Máx 12 líneas · sin código.
OBLIGATORIO: tu dirección debe incorporar al menos 1 tendencia del TREND INTEL y explicar cómo la adapta al DNA de la marca — no copiar, transformar.
Cerrá con: REFERENCIA (1 trabajo world-class publicado en $PREV_YEAR-$CURRENT_YEAR) + ¿qué hace UNFORGETTABLE este diseño en el contexto actual? + auto-corrección anti-slop (SÍ/NO + qué reemplazaste).
```

Generar mockups en `$MOCKUP_BASE_PATH/$COMPONENTE/A.html`, `B.html`, `C.html`.

**Asignación de ejes:** 3+ agentes: 1 por eje · 2 agentes: A+B · FAZM genera C con `/design-html` · 1 agente: los 3 secuenciales

Checkpoint post-PASO 3:
```bash
# FAZM: asignar el output real de cada agente antes de exportar
# El agente eje A devuelve una dirección en ≤12 líneas → capturar en DIRECTION_A
# Ejemplo: DIRECTION_A="Tipografía condensada Bold 700 como protagonista · tracking -1px · grid editorial"
DIRECTION_A="[FAZM: output real del agente eje A — NO dejar este placeholder]"
DIRECTION_B="[FAZM: output real del agente eje B — NO dejar este placeholder]"
DIRECTION_C="[FAZM: output real del agente eje C — NO dejar este placeholder]"
# FAZM: reemplazar los 3 con el output real de los agentes antes de continuar
for _var in DIRECTION_A DIRECTION_B DIRECTION_C; do
  _val="${!_var}"
  if echo "$_val" | grep -q "FAZM: output real"; then
    echo "ERROR · $_var no fue reemplazado con el output del agente de diseño"
    exit 1
  fi
done
export DIRECTION_A DIRECTION_B DIRECTION_C

python3 << PYEOF
import json, datetime, os
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 3; d['status'] = 'PASS'
d['mockups_generados'] = ['$MOCKUP_BASE_PATH/$COMPONENTE/A.html',
                          '$MOCKUP_BASE_PATH/$COMPONENTE/B.html',
                          '$MOCKUP_BASE_PATH/$COMPONENTE/C.html']
d['directions'] = {
    'A': os.environ.get('DIRECTION_A', ''),
    'B': os.environ.get('DIRECTION_B', ''),
    'C': os.environ.get('DIRECTION_C', '')
}
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
PYEOF
```

---

## PASO 4 · BRAND COUNCIL · SELECCIÓN MOCKUP (autónomo)

FAZM: leer `$ATLAS_DIR/brand-context.md` e incluir verbatim como DESIGN_AGENCY_BLOCK.

Pre-dispatch · verificar tamaño:
```bash
for f in A B C; do
  SIZE=$(wc -c < "$PROJECT_REPO/$MOCKUP_BASE_PATH/$COMPONENTE/$f.html" 2>/dev/null || echo 0)
  if [ "$SIZE" -gt 51200 ]; then
    echo "WARN · mockup $f es ${SIZE}B (>50KB) · usar head -400 como input del agente"
    head -400 "$PROJECT_REPO/$MOCKUP_BASE_PATH/$COMPONENTE/$f.html" > "/tmp/$COMPONENTE-$f-truncated.html"
  fi
done
```

Dispatchar 3 agentes en paralelo — `Brand Guardian` · `UI Designer` · `fitness-ux-specialist`. Incluir AUTONOMIA_BLOCK + DESIGN_AGENCY_BLOCK al inicio:

```
[AUTONOMIA_BLOCK]

[DESIGN_AGENCY_BLOCK — contenido de brand-context.md]

[PROJECT_BRIEF — contenido de project-brief.md · contexto narrativo vivo del producto]

Eres [AGENTE] · Brand Council.

MASTER REFERENCE: [grep -n "$COMPONENTE" $MASTER_FILE | head -20]

MOCKUPS:
A: $PROJECT_REPO/$MOCKUP_BASE_PATH/$COMPONENTE/A.html — dirección $DIRECTION_A
B: $PROJECT_REPO/$MOCKUP_BASE_PATH/$COMPONENTE/B.html — dirección $DIRECTION_B
C: $PROJECT_REPO/$MOCKUP_BASE_PATH/$COMPONENTE/C.html — dirección $DIRECTION_C

PASO OBLIGATORIO: usar Read tool sobre cada path antes de dar score.

TAREA: Evaluá los 3 mockups. Doble eje: fidelidad al master + DNA, y VANGUARDIA.
Formato (máx 100 palabras):
SCORE_A: X/10 · VANGUARDIA A/10 · [razón] · [slop detectado o "ninguno"]
SCORE_B: X/10 · VANGUARDIA B/10 · [razón] · [slop detectado o "ninguno"]
SCORE_C: X/10 · VANGUARDIA C/10 · [razón] · [slop detectado o "ninguno"]
ELEGIDO: [A/B/C] · [por qué supera a los otros en 1 línea]
```

**Agregación:**
```
GANADOR = mockup con mayor (avg_fidelidad * 0.6 + avg_vanguardia * 0.4)
Gate anti-slop: si ganador tiene vanguardia <6 Y otro tiene avg≥7.5 + vanguardia≥7.5 → gana el segundo
Si los 3 tienen vanguardia <6 → STOP · escalar: "3 direcciones slop · re-spin requerido"
Tie → Brand Guardian desempata
```

Persistir estado:
```bash
MOCKUP_GANADOR="A"   # FAZM: sustituir con el ganador real del Brand Council ("A", "B", o "C")
# Validar que es A/B/C y no el placeholder sin cambiar
if ! echo "$MOCKUP_GANADOR" | grep -qE "^[ABC]$"; then
  echo "ERROR · MOCKUP_GANADOR='$MOCKUP_GANADOR' inválido · debe ser A, B o C"
  exit 1
fi

python3 -c "
import json, datetime
d = json.load(open('$CHECKPOINT_FILE'))
d['paso'] = 4; d['status'] = 'PASS'
d['mockup_ganador'] = '$MOCKUP_GANADOR'
d['matu_rounds_done'] = 0; d['matu_pass'] = False
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('$CHECKPOINT_FILE','w'), indent=2)
"
```

Invocar `/context-save` post-elección.

---

## PASO 5A · SPEC EXTRACTION (pre-implementación · obligatorio si creative_spin≠[] o CREATE_NEW)

**Por qué existe:** el agente de implementación "interpreta" el mockup y toma decisiones propias — spacing distinto, copy parafraseado, colores aproximados. Extraer specs primero lo convierte en un ejecutor preciso, no un diseñador.

```bash
MOCKUP_SOURCE=$(python3 -c "
import json, os
d = json.load(open('.claude/flow-checkpoint.json'))
ganador = d.get('mockup_ganador', '')
base = '$PROJECT_REPO/$MOCKUP_BASE_PATH/$COMPONENTE/'
if ganador and os.path.exists(base + ganador + '.html'):
    print(base + ganador + '.html')
elif '$MASTER_FILE' and os.path.exists('$PROJECT_REPO/$MASTER_FILE'):
    print('$PROJECT_REPO/$MASTER_FILE')
else:
    print('$MASTER_FILE')
" 2>/dev/null || echo "$MASTER_FILE")

SPEC_FILE="$PROJECT_REPO/.claude/implementation-spec-$COMPONENTE.md"
```

Dispatchar 1 agente `general-purpose`. Prompt:

```
Sos un spec extractor. Tu trabajo: leer el HTML del mockup y producir una lista de implementación exacta. Sin interpretación — solo lo que está literalmente en el HTML.

Leé: [$MOCKUP_SOURCE]

Devolvé SOLO este formato (cada item verificable):

# Implementation Spec — [$COMPONENTE]
Fuente: [$MOCKUP_SOURCE]

## Layout
- [ ] Estructura raíz: [flex/grid · dirección · justify · align]
- [ ] Padding contenedor: [top right bottom left exacto]
- [ ] Gap entre elementos: [valor exacto]

## Colores (hex exactos — no aproximar)
- [ ] Background: [#hex]
- [ ] Surface/card: [#hex]
- [ ] Texto principal: [#hex]
- [ ] Texto secundario: [#hex]
- [ ] Acento/marca: [#hex]
- [ ] [otros colores presentes en el mockup]

## Tipografía
- [ ] [elemento]: [font-family] [weight] [size] [line-height si hay] [tracking si hay]

## Copy (literal — cero parafraseo)
- [ ] [nombre del elemento]: "[texto exacto del mockup]"

## Interacciones declaradas
- [ ] [elemento]: [acción] → [resultado visible]

## Jerarquía de componentes
[árbol de componentes tal como aparece en el HTML · indentado]

REGLA ABSOLUTA: si no está en el HTML → no lo listés. Cero inventar.
```

```bash
# FAZM: escribir output del agente en $SPEC_FILE
SPEC_ITEMS=$(grep -c '^\- \[ \]' "$SPEC_FILE" 2>/dev/null || echo "0")
```

# FAZM (interno): spec en $SPEC_FILE · $SPEC_ITEMS items · continuar a PASO 5 con esta lista como input obligatorio

---

## PASO 5 · IMPLEMENTACIÓN

**REGLA DE FIDELIDAD:** el agente de implementación DEBE recibir `$SPEC_FILE` como primer input. Implementa contra la lista de specs — no contra el mockup visual directamente.

**Mobile:** invocar `$IMPLEMENT_SKILL` · componente + master + mockup elegido + `$SPEC_FILE`.

**Web:** implementar desde `$SPEC_FILE` · Tailwind tokens · Server/Client components · `motion` para animaciones.

**Both (monorepo):** implementar según `$ROUTER_PLATFORM` detectado en PASO 1.

### 5Z · CHECKPOINT COMMIT (obligatorio · anti-loss)

```bash
# Staging selectivo — nunca git add -A
git diff --name-only | grep -E "$STAGING_PATHS_REGEX" | xargs -r git add
git ls-files --others --exclude-standard | grep -E "$STAGING_PATHS_REGEX" | xargs -r git add
git diff --cached --stat

TYPECHECK_OUTPUT=$($TYPECHECK_CMD 2>&1); TYPECHECK_EXIT=$?
echo "$TYPECHECK_OUTPUT" | tail -3
if [ "$TYPECHECK_EXIT" -ne 0 ]; then
  echo "STOP · typecheck falla pre-checkpoint 5Z · arreglar antes de commitear"
  python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi

git commit -m "wip(checkpoint): $COMPONENTE · PASO 5 · pre-review · revertible

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 5; d['status'] = 'PASS'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

---

## PASO 6 · REVIEW + SMOKE + SECURITY

**6A · /review + /performance** (CREATE_NEW/REWRITE_COMPLEX · compound · bloqueante):
"Revisá [archivo] para calidad de código + performance. Reportá issues separados por categoría."

**6A · /review solo** (REFACTOR_SIMPLE/EXTRACT/POLISH · bloqueante)

**6B · /cso** (condicional · safety/auth/pagos/PII)

**6D · /smoke-agent** (bloqueante):
- Mobile: `/smoke-agent` — typecheck · hook · flows · import graph
- Web: `/smoke-agent --platform web`
- Both: correr ambos

Checkpoint post-6D:
```bash
python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 6; d['status'] = 'PASS_6D'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

**6E · /qa** (web · post-smoke · solo si tipo = CREATE_NEW/REWRITE_COMPLEX)

**6F · VERIFICATION GATE** (pre-/matu · BLOQUEANTE):

```bash
TYPECHECK_OUTPUT=$($TYPECHECK_CMD 2>&1); TYPECHECK_EXIT=$?
echo "$TYPECHECK_OUTPUT" | tail -5
echo "TYPECHECK_EXIT=$TYPECHECK_EXIT"

DIFF_BASE=$(git merge-base HEAD origin/main 2>/dev/null || echo "HEAD~1")
git diff --stat "$DIFF_BASE"

HOOK_TARGET=$(git diff --name-only "$DIFF_BASE" 2>/dev/null | grep -E "\.(tsx|ts)$" | head -1 || echo "src/$COMPONENTE")
bash "$PROJECT_REPO/.claude/hooks/check-mobile-antipatterns.sh" "$PROJECT_REPO/$HOOK_TARGET" 2>&1 | tail -5 || echo "WARN · hook ausente"
DIFF_FILES=$(git diff --name-only "$DIFF_BASE" 2>/dev/null)
if [ $? -ne 0 ]; then
  echo "WARN · git diff falló · CRITICAL_TOUCHED marcado como desconocido"
  CRITICAL_TOUCHED="UNKNOWN"
else
  CRITICAL_TOUCHED=$(echo "$DIFF_FILES" | grep -E "$CRITICAL_PATHS_REGEX" || echo "ninguno")
fi
echo "CRITICAL_TOUCHED=$CRITICAL_TOUCHED"

if [ "$ROUTER_PLATFORM" = "mobile" ]; then
  PARIDAD_EVIDENCIA=""
  xcrun simctl io booted screenshot "/tmp/paridad-$COMPONENTE.png" 2>/dev/null && \
    ls "/tmp/paridad-$COMPONENTE.png" &>/dev/null && \
    PARIDAD_EVIDENCIA="/tmp/paridad-$COMPONENTE.png"
  if [ -z "$PARIDAD_EVIDENCIA" ]; then
    echo "WARN · simulator no disponible · verificación visual manual requerida"
    PARIDAD_EVIDENCIA="manual-required"
  fi
else
  TARGET_FILE=$(git diff --name-only "$DIFF_BASE" 2>/dev/null | grep -E "\.(tsx|ts|jsx|js|css)$" | head -1)
  PARIDAD_EVIDENCIA=$(grep -c "$COMPONENTE" "$PROJECT_REPO/$TARGET_FILE" 2>/dev/null || echo "0")
fi
echo "PARIDAD_EVIDENCIA=$PARIDAD_EVIDENCIA"
if [ -z "$PARIDAD_EVIDENCIA" ] || [ "$PARIDAD_EVIDENCIA" = "0" ]; then
  echo "WARN · paridad no verificada · continuar con precaución"
fi
```

PASS solo si: TYPECHECK_EXIT=0 · PARIDAD_EVIDENCIA es path o número · CRITICAL_TOUCHED listado.

Post-6F · override matu_mode si CRITICAL_TOUCHED:
```bash
ENV_TOUCHED=$(echo "$CRITICAL_TOUCHED" | grep -E "\.env" || echo "")
if [ -n "$ENV_TOUCHED" ]; then
  echo "STOP · .env en diff · posibles credenciales nuevas · requiere OK explícito"
  python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi

if [ "$CRITICAL_TOUCHED" != "ninguno" ] && [ "$MATU_MODE" = "light" ]; then
  echo "OVERRIDE · CRITICAL_TOUCHED + light → forzar canonical"
  MATU_MODE="canonical"
fi
```

Checkpoint post-6F:
```bash
python3 -c "
import json
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 6; d['status'] = 'PASS'; d['matu_mode'] = '$MATU_MODE'
d['diff_base'] = '$DIFF_BASE'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

**6G · FIDELITY CHECK** (si `$SPEC_FILE` existe · post-implementación · pre-/matu):

```bash
SPEC_FILE="$PROJECT_REPO/.claude/implementation-spec-$COMPONENTE.md"
if [ ! -f "$SPEC_FILE" ]; then
  echo "SKIP 6G · no hay spec file (creative_spin=[] o REFACTOR) · continuar a PASO 7"
fi
```

Si `$SPEC_FILE` existe → dispatchar 1 agente `code-reviewer`. Prompt:

```
Sos un verificador de fidelidad. Verificá que la implementación cumple CADA item de la spec. Sin excepciones por "está cerca" — o cumple exactamente o no cumple.

SPEC: [contenido de $SPEC_FILE]

CÓDIGO: [archivos modificados desde git diff $DIFF_BASE]

Para cada item de la spec:
✓ cumple — si el valor en código coincide exactamente con el spec
✗ desviación — si hay cualquier diferencia · indicar valor real encontrado

OUTPUT OBLIGATORIO:
FIDELITY_SCORE: N/[total]

Items ✗ (solo los que fallan):
- [item spec] → real: [valor encontrado en código]

Si N = total → FIDELITY_PASS · si N < total → FIDELITY_FAIL
```

Si `FIDELITY_FAIL`:
1. FAZM aplica los fixes de los items ✗ directamente al código
2. Re-corre typecheck
3. Re-corre 6G una vez (máximo 2 intentos)
4. Si sigue FAIL tras 2 intentos → escalar con lista de items irresolubles

```bash
# FAZM (interno): FIDELITY_SCORE=N/total · si PASS → continuar a PASO 7 · si FAIL → aplicar fixes en silencio
# Persistir FIDELITY_SCORE en checkpoint (FAZM: setar desde output del agente antes de este bloque)
FIDELITY_SCORE="${FIDELITY_SCORE:-N/A}"
python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['fidelity_score'] = '$FIDELITY_SCORE'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

---

## PASO 7 · /matu

FAZM: leer `$ATLAS_DIR/matu-context.md` e incluir verbatim como bloque CONTEXTO en cada agente de /matu.

```bash
MATU_CONTEXT=$(cat "$ATLAS_DIR/matu-context.md")
```

**canonical** (CREATE_NEW/REWRITE_COMPLEX/safety): Bloque A (6) + Bloque B GAN (8) + Bloque C según clasificación · avg ≥9.5 · cero T1

**light** (REFACTOR_SIMPLE/EXTRACT/POLISH): Brand Guardian · UI Designer · fitness-ux-specialist · avg ≥9.0 · cero T1

```
/matu [canonical|light] "$COMPONENTE · [descripción · archivos afectados · master: $MASTER_FILE]"
```

Round 2+: re-dispatchar SOLO agentes con T1. Máximo 5 rounds.

Pre-dispatch R2+ · typecheck:
```bash
MATU_ROUND=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('matu_rounds_done',0))" 2>/dev/null || echo 0)

TYPECHECK_OUTPUT=$($TYPECHECK_CMD 2>&1); TYPECHECK_EXIT=$?
echo "$TYPECHECK_OUTPUT" | tail -3
if [ "$TYPECHECK_EXIT" -ne 0 ]; then
  echo "STOP · typecheck falla post-fixes · arreglar antes de re-dispatch R$(($MATU_ROUND + 1))"
  python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi
```

Tracking por round:
```bash
MATU_ROUND_N=1
MATU_FAILED_AGENTS_JSON='[]'
MATU_SCORE_FINAL="9.5"
MATU_PASS_BOOL="True"

if ! echo "$MATU_ROUND_N" | grep -qE '^[0-9]+$'; then
  echo "ERROR · MATU_ROUND_N debe ser entero · valor actual: '$MATU_ROUND_N'"
  python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi
if [ "$MATU_PASS_BOOL" != "True" ] && [ "$MATU_PASS_BOOL" != "False" ]; then
  echo "ERROR · MATU_PASS_BOOL debe ser 'True' o 'False' · valor actual: '$MATU_PASS_BOOL'"
  python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi
export MATU_FAILED_AGENTS_JSON

python3 << PYEOF
import json, os
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 7
d['matu_rounds_done'] = $MATU_ROUND_N
d['matu_failed_agents'] = json.loads(os.environ.get('MATU_FAILED_AGENTS_JSON', '[]'))
d['matu_score_final'] = '$MATU_SCORE_FINAL'
d['matu_pass'] = $MATU_PASS_BOOL
d['status'] = 'PASS' if '$MATU_PASS_BOOL' == 'True' else 'IN_PROGRESS'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
PYEOF
```

Round 5 sin PASS → STOP · escalar con causa raíz.

---

## PASO 8 · Tests (CREATE_NEW + REWRITE_COMPLEX · post-/matu PASS)

Checkpoint inicio:
```bash
python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 8; d['status'] = 'IN_PROGRESS'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

Invocar `/qa` con foco en el componente. Tests mínimos obligatorios (PASS = los 3 pasan):
1. Render sin crash
2. Props requeridas — assertions sobre outputs clave
3. Compliance check — si hay reglas de compliance en `$ATLAS_DIR/flow-rules.md`, verificar que ningún texto las viola

A11y básica (no bloquea · si falla, agregar a `.claude/BACKLOG.md` como `[A11Y-DEUDA] $COMPONENTE: [descripción]`).

Checkpoint cierre PASO 8 (solo en PASS):
```bash
python3 -c "
import json, datetime
d = json.load(open('.claude/flow-checkpoint.json'))
d['paso'] = 8; d['status'] = 'PASS'
d['ts'] = datetime.datetime.utcnow().isoformat() + 'Z'
json.dump(d, open('.claude/flow-checkpoint.json','w'), indent=2)
"
```

---

## PASO 9 · COMMIT + PUSH

Pre-commit:
```bash
TYPECHECK_OUTPUT=$($TYPECHECK_CMD 2>&1); TYPECHECK_EXIT=$?
echo "$TYPECHECK_OUTPUT" | tail -3
if [ "$TYPECHECK_EXIT" -ne 0 ]; then
  echo "STOP · typecheck falla pre-commit · no commitear con errores"
  python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
  exit 1
fi
grep -rn "console\.log\|debugger" src/ 2>/dev/null && echo "LIMPIAR" || echo "OK"
```

Commit:
```bash
# Staging selectivo — siempre usa $STAGING_PATHS_REGEX del proyecto (no hardcodear paths)
# ROUTER_PLATFORM es siempre "web" o "mobile" — nunca "both" (el Router lo resuelve al clasificar)
git diff --name-only | grep -E "$STAGING_PATHS_REGEX" | xargs -r git add
git ls-files --others --exclude-standard | grep -E "$STAGING_PATHS_REGEX" | xargs -r git add
git add docs/ .claude/BACKLOG.md 2>/dev/null || true
git diff --cached --stat

# Recovery cross-day
ROUTER_PLATFORM=${ROUTER_PLATFORM:-$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('router_platform','$PLATFORM_DEFAULT'))" 2>/dev/null || echo "$PLATFORM_DEFAULT")}
if [ "$ROUTER_PLATFORM" = "web" ]; then
  PLATFORM_PREFIX="feat(web)"
elif [ "$ROUTER_PLATFORM" = "both" ]; then
  PLATFORM_PREFIX="feat(both)"
else
  PLATFORM_PREFIX="feat(mobile)"
fi

# Leer del checkpoint
MATU_MODE_COMMIT=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('matu_mode','canonical'))" 2>/dev/null || echo "$MATU_MODE")
MATU_SCORE_COMMIT=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('matu_score_final','?'))" 2>/dev/null || echo "?")
MATU_ROUNDS_COMMIT=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('matu_rounds_done',1))" 2>/dev/null || echo "1")
MOCKUP_COMMIT=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('mockup_ganador','none'))" 2>/dev/null || echo "none")
FIDELITY_SCORE_COMMIT=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('fidelity_score','N/A'))" 2>/dev/null || echo "N/A")

git commit -m "$PLATFORM_PREFIX: $COMPONENTE · /matu $MATU_MODE_COMMIT ${MATU_SCORE_COMMIT}avg · ${MATU_ROUNDS_COMMIT} rounds

Master: $MASTER_FILE
/matu: R1 → R${MATU_ROUNDS_COMMIT} PASS ${MATU_SCORE_COMMIT} · mockup $MOCKUP_COMMIT

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Liberar locks + loguear costo real:
```bash
python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))"
rm -f .claude/.flow-lock

MATU_ROUNDS=$(python3 -c "import json; d=json.load(open('.claude/flow-checkpoint.json')); print(d.get('matu_rounds_done',1))" 2>/dev/null || echo "1")
python3 -c "
import json, datetime
entry = {
  'ts': datetime.datetime.utcnow().isoformat() + 'Z',
  'evento': 'flujo_completado',
  'proyecto': '$PROJECT_NAME',
  'componente': '$COMPONENTE',
  'tier_estimado': '$COSTO_TIER',
  'matu_mode': '$MATU_MODE',
  'matu_rounds_reales': int('$MATU_ROUNDS') if '$MATU_ROUNDS'.isdigit() else 1,
  'commit': '$(git rev-parse --short HEAD 2>/dev/null || echo unknown)'
}
with open('.claude/atlas-proxy-log.jsonl', 'a') as f:
    f.write(json.dumps(entry) + '\n')
"
```

Push + merge (automático si limpio · STOP si CRITICAL_TOUCHED):
```bash
CURRENT_BRANCH=$(git branch --show-current)
git fetch origin main 2>/dev/null || echo "WARN · git fetch falló"

DIFF_BASE_P9=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('diff_base',''))" 2>/dev/null || echo "")
DIFF_BASE_P9=${DIFF_BASE_P9:-$(git merge-base HEAD origin/main 2>/dev/null || echo "HEAD~1")}

CRITICAL_FILES=$(git diff --name-only "$DIFF_BASE_P9" 2>/dev/null | grep -E "$CRITICAL_PATHS_REGEX")
if [ -n "$CRITICAL_FILES" ]; then
  # Verificar destructivo
  DESTRUCTIVO=$(git diff "$DIFF_BASE_P9" 2>/dev/null | grep -E "^\+.*(DROP TABLE|DROP COLUMN|DELETE FROM|TRUNCATE)" | grep -v "^\+.*--" | wc -l | tr -d ' ')
  if [ "$DESTRUCTIVO" -gt 0 ]; then
    echo "STOP IRREVERSIBLE · operación destructiva detectada · requiere OK explícito"
    python3 -c "import json; open('.claude/session-lock.json','w').write(json.dumps({'locked':False,'session':None,'task':None,'branch':None,'ts':None,'pid':None}, indent=2))" && rm -f .claude/.flow-lock
    exit 1
  fi
  # No destructivo → Security Council
  CRITICAL_DIFF=$(git diff "$DIFF_BASE_P9" -- $CRITICAL_FILES 2>/dev/null | head -200)
  echo "SECURITY_COUNCIL_NEEDED · dispatching 3 agentes..."
  # FAZM: dispatchar Security Council (ver sección "Security Council" abajo)
  echo "STOP · Security Council completado · cambios críticos: $CRITICAL_FILES"
  echo "Requiere OK del project owner para push + merge"
  exit 0
fi

# Recovery cross-day: usar branch del checkpoint si disponible
CHECKPOINT_BRANCH=$(python3 -c "import json; print(json.load(open('.claude/flow-checkpoint.json')).get('branch_name',''))" 2>/dev/null || echo "")
if [ -n "$CHECKPOINT_BRANCH" ] && git show-ref --quiet "refs/heads/$CHECKPOINT_BRANCH"; then
  CURRENT_BRANCH="$CHECKPOINT_BRANCH"
fi

if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
  echo "STOP · ya en main · nada que mergear"
  exit 0
fi

git push origin "$CURRENT_BRANCH"

PR_URL=$(gh pr view "$CURRENT_BRANCH" --json url -q .url 2>/dev/null)
if [ -z "$PR_URL" ]; then
  gh pr create --title "${PLATFORM_PREFIX}: $COMPONENTE · /matu PASS ${MATU_SCORE_COMMIT}avg · ${MATU_ROUNDS_COMMIT} rounds" \
    --body "/matu: R1→R${MATU_ROUNDS_COMMIT} PASS ${MATU_SCORE_COMMIT} · /smoke-agent PASS · mockup $MOCKUP_COMMIT · fidelidad $FIDELITY_SCORE_COMMIT" \
    --base main
fi
gh pr merge "$CURRENT_BRANCH" --squash --delete-branch --auto 2>/dev/null || \
gh pr merge "$CURRENT_BRANCH" --squash --delete-branch
echo "Merge ejecutado · deploy $DEPLOY_TARGET disparado automáticamente"
```

Actualizar estado del proyecto:
```bash
ESTADO_FILE="$ATLAS_DIR/project-estado.json"
python3 -c "
import json, datetime
try:
    d = json.load(open('$ESTADO_FILE'))
except:
    d = {'componentes_listos': [], 'componentes_pendientes': [], 'sesiones_totales': 0}

comp = '$COMPONENTE'
if comp not in d.get('componentes_listos', []):
    d.setdefault('componentes_listos', []).append(comp)
if comp in d.get('componentes_pendientes', []):
    d['componentes_pendientes'].remove(comp)

total = len(d['componentes_listos']) + len(d.get('componentes_pendientes', []))
d['progreso_pct'] = int(len(d['componentes_listos']) / max(total, 1) * 100)
d['ultima_sesion'] = datetime.datetime.utcnow().isoformat() + 'Z'
d['ultima_accion'] = f'$COMPONENTE terminado · /matu PASS $MATU_SCORE_COMMIT'
d['sesiones_totales'] = d.get('sesiones_totales', 0) + 1

pendientes = d.get('componentes_pendientes', [])
if pendientes:
    d['proximo_paso'] = f'Continuar con: {pendientes[0]}'
else:
    d['proximo_paso'] = 'Todos los componentes registrados están listos'

json.dump(d, open('$ESTADO_FILE', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'Estado actualizado · {d[\"progreso_pct\"]}% completo · {len(d[\"componentes_listos\"])} listo(s)')
"
```

**Output al usuario — PASO 9 es el único mensaje de cierre del flujo completo:**

Si `USER_NIVEL=basico`:
```
Listo. [COMPONENTE] está terminado y guardado.

[progreso]% del camino.
Siguiente: [proximo_paso]
```

Si `USER_NIVEL=avanzado`:
```
PASS · [componente] · commit [hash] · [progreso]% · próximo: [proximo_paso]
```

---

## PASO 10 · PROXY · siguiente task

FAZM: leer `$ATLAS_DIR/flow-rules.md` sección "PASO 10 · Proxy behavior" y ejecutar el prompt definido ahí.

```bash
PROXY_RULES=$(cat "$ATLAS_DIR/flow-rules.md")
# FAZM: dispatchar Agent(subagent_type="Product Manager", prompt="[contenido de la sección PASO 10 de flow-rules.md]")
```

Si flow-rules.md no tiene sección PASO 10 → Proxy genérico:
```
Sos el proxy de [PROJECT_NAME]. Lee .claude/BACKLOG.md · elegí la siguiente tarea según prioridad · reportá "PRÓXIMO TASK: [ID] [desc] · invocar /atlas". NO invocar /atlas directamente.
```

---

## Security Council · Prompt por agente

FAZM: leer `$ATLAS_DIR/matu-context.md` y `$ATLAS_DIR/flow-rules.md` para construir el contexto.

```
[AUTONOMIA_BLOCK]

Eres [AGENTE] · Security Council de [PROJECT_NAME].

CONTEXTO DEL PROYECTO:
[contenido de matu-context.md]

CAMBIO A REVISAR:
[diff completo de los archivos críticos detectados]

TAREA: Evaluá si este cambio es seguro. Tu PASS habilita que el project owner apruebe el merge manualmente. Reportá hallazgos completos.

Formato obligatorio (máx 150 palabras):
VEREDICTO: PASS | FAIL
DESTRUCTIVO: SÍ | NO
TIER 1 — BLOQUEANTES:
- [issue] → [fix concreto]
Sin T1: escribí "ninguno".
```

Agentes: `security-reviewer` · `Legal Compliance Checker` · `Backend Architect`
Los 3 deben dar VEREDICTO=PASS y DESTRUCTIVO=NO.

---

## RECOVERY (sesión cortada)

```bash
cat "$PROJECT_REPO/.claude/flow-checkpoint.json"
```

| checkpoint paso | status | retomar desde |
|---|---|---|
| 0 | PASS | PASO 1 |
| 1 | PASS | PASO 2 · si creative_spin=[] → PASO 5 directo |
| 2 | PASS | PASO 3 · si creative_spin=[] → PASO 5 |
| 3 | PASS | PASO 4 · usar mockups_generados + directions del checkpoint |
| 4 | PASS | PASO 5 · usar mockup_ganador del checkpoint |
| 5 | PASS | PASO 6 · re-correr review+smoke+6F completo |
| 6 | PASS_6D | PASO 6 · solo 6E (si aplica) + 6F gate |
| 6 | PASS | PASO 7 · dispatch completo |
| 7 | IN_PROGRESS | Re-despachar solo matu_failed_agents del checkpoint |
| 7 | PASS | PASO 8 si CREATE_NEW/REWRITE_COMPLEX · si no → PASO 9 |
| 8 | IN_PROGRESS | Re-invocar /qa desde cero |
| 8 | PASS | PASO 9 directo |

IN_PROGRESS → re-ejecutar ese paso. No existe → flujo nuevo desde PASO 0.

Recovery cross-day:
```bash
# Recargar config
ATLAS_DIR="${ATLAS_DIR:-$HOME/.claude/skills/atlas/projects/$PROJECT_NAME}"
PROJECT_REPO=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['repo_path'])" 2>/dev/null)
TYPECHECK_CMD=$(python3 -c "import json; print(json.load(open('$ATLAS_DIR/project.json'))['typecheck_cmd'])" 2>/dev/null || echo "npm run typecheck")
CURRENT_YEAR=$(date +%Y)
PREV_YEAR=$((CURRENT_YEAR - 1))
CHECKPOINT_FILE="$PROJECT_REPO/.claude/flow-checkpoint.json"
BACKLOG_FILE="$PROJECT_REPO/.claude/BACKLOG.md"

# Restaurar variables de sesión
cd "$PROJECT_REPO"
ROUTER_PLATFORM=$(python3 -c "import json; print(json.load(open('$CHECKPOINT_FILE')).get('router_platform','mobile'))" 2>/dev/null || echo "mobile")
COMPONENTE=$(python3 -c "import json; print(json.load(open('$CHECKPOINT_FILE')).get('componente',''))" 2>/dev/null || echo "")
MASTER_FILE=$(python3 -c "import json; print(json.load(open('$CHECKPOINT_FILE')).get('master_file',''))" 2>/dev/null || echo "")
MATU_MODE=$(python3 -c "import json; print(json.load(open('$CHECKPOINT_FILE')).get('matu_mode','canonical'))" 2>/dev/null || echo "canonical")
CHECKPOINT_BRANCH=$(python3 -c "import json; print(json.load(open('$CHECKPOINT_FILE')).get('branch_name',''))" 2>/dev/null || echo "")
if [ -n "$CHECKPOINT_BRANCH" ] && git show-ref --quiet "refs/heads/$CHECKPOINT_BRANCH"; then
  git checkout "$CHECKPOINT_BRANCH"
fi
DIFF_BASE=$(python3 -c "import json; print(json.load(open('$CHECKPOINT_FILE')).get('diff_base',''))" 2>/dev/null || echo "")
```
