# ATLAS Pro — motor de calidad world-class para Claude Code

> Un motor que hace que **cualquier** proyecto de UI/producto llegue a 10/10. No es un theme ni un set de componentes: es el **criterio** — destilado de 20+ design systems tier-1 (Apple, Stripe, Linear, Vercel, Figma, Ferrari, Tesla, Coinbase, Revolut, Cohere…), research de R3F/motion/splash, y los mejores referentes de craft e ingeniería con agentes — cableado a un flujo que se ejecuta solo.

---

## Qué es

ATLAS es una **skill de Claude Code**. Cuando vas a implementar UI, una pantalla nueva, un refactor visual o un asset, ATLAS:

1. **Detecta tu proyecto** (por el directorio) y carga su configuración.
2. **Carga la vara de calidad universal** (`universal-craft-codex.md`) + el **overlay de tu marca** (`brand-context.md`).
3. Corre un **flujo de 10 pasos** con pre-flight, intel, creative spin (3 mockups A/B/C), brand council, implementación, review, smoke, visual-diff loop, gate cinematográfico para video, gate de esencia para imagen, `/matu` (certificación ≥9.0), tests, commit.
4. No te pregunta entre pasos: decide lo más razonable, ejecuta, y reporta al cierre (2 únicos STOP: operación de DB destructiva · credenciales nuevas).

**La idea central:** el criterio de calidad no vive en el modelo — vive en los archivos. ATLAS los carga en contexto en el momento justo, así el output es world-class y no "lo que el modelo recuerda de fábrica".

---

## Arquitectura: codex (base) + overlay (tu marca)

```
universal-craft-codex.md   ← BASE · project-neutral · la vara 10/10 (igual para todos)
        +
projects/<tu-proyecto>/brand-context.md   ← OVERLAY · tu DNA (color, tipo, voz, restricciones)
        =
   criterio con el que ATLAS diseña y revisa tu producto
```

El overlay **especializa** el codex, nunca lo contradice. El codex trae las leyes universales (tipografía/color/spacing/componentes/restraint, motion, 3D/cinemática, splash/onboarding, arquitectura híbrida mobile, short-form/generativo, harness/ingeniería) + un **Gate Universal 10/10**. El overlay las aterriza a tu marca.

---

## Qué hay adentro

```
skills/atlas/
├── SKILL.md                     # entrypoint · auto-detección de proyecto · modo universal
├── motor.md                     # el motor: flujo de 10 pasos
├── onboarding.md                # wizard para registrar un proyecto nuevo
├── universal-craft-codex.md     # ⭐ la vara de calidad universal (project-neutral)
├── worldclass-craft.md          # EJEMPLO de overlay (DNA de un producto real) — borrable
├── grow.md · innovate.md        # modos: crecer el cerebro · ideación
├── eval/                        # harness de evals del propio ATLAS
├── fable5/                      # pilares de criterio de código (P1–P5 + seguridad/testing/llm)
├── *-playbook.md                # craft técnico hondo:
│   ├── skia-sksl-playbook.md            (shaders Skia React Native)
│   ├── motion-playbook.md               (math + taste de motion)
│   ├── gesture-choreography-playbook.md (física del gesto)
│   ├── cinematography-playbook.md       (director de foto para VIDEO)
│   ├── prompt-craft-playbook.md         (imagen generativa: esencia→cláusulas)
│   ├── dataviz-safe-para-datos-sensibles.md · haptics · perf-profiling · rive-adoption · newarch-gotchas
│   └── youtube-study-playbook.md        (cómo "estudiar" videos de referentes)
├── atlas-log.py · atlas-monitor.py · atlas-gc.sh · atlas-setup.sh
├── hooks/pre-commit
└── projects/
    └── _TEMPLATE/               # plantilla para registrar TU proyecto
        ├── project.json
        └── brand-context.md
```

**Excluido a propósito** (privado del autor): proyectos reales, su historial de evals/aprendizaje, y el repo git. El paquete es craft puro, sin datos de nadie.

---

## Instalación

Requiere [Claude Code](https://claude.com/claude-code) instalado.

```bash
cd ~/Desktop/ATLAS-Pro
./INSTALL.sh
```

Esto copia `skills/atlas/` a `~/.claude/skills/atlas/`. (Si ya tenés una skill `atlas`, el instalador hace backup antes.)

Luego, en cualquier proyecto: invocá `/atlas` y seguí el `onboarding` para registrarlo (copia `projects/_TEMPLATE/` → `projects/tu-proyecto/`, edita `project.json` con la ruta de tu repo y `brand-context.md` con tu DNA).

**Instalá (repo público — sin login):**
```bash
git clone https://github.com/ncomplementaria1-blip/atlas-pro ~/atlas-pro
cd ~/atlas-pro && ./INSTALL.sh && ./ENABLE-AUTOUPDATE.sh
```
`INSTALL.sh` enlaza por symlink · `ENABLE-AUTOUPDATE.sh` hace que ATLAS se actualice **solo** cada vez que abrís Claude Code.

---

## Actualizaciones (automáticas)

Con `ENABLE-AUTOUPDATE.sh` activado, cada vez que abrís Claude Code ATLAS hace `git pull` solo en background → siempre tenés la última versión, sin hacer nada. **Tus proyectos (`projects/*`) nunca se tocan** (gitignored). Cambios en `skills/atlas/CHANGELOG.md`, versión en `skills/atlas/VERSION`.

¿Preferís manual? `cd ~/atlas-pro && ./UPDATE.sh`.

> **Solo el maintainer publica.** El repo es público (todos LEEN y reciben updates), pero **solo el dueño puede pushear** mejoras. Flujo del maintainer: mejorás en tu copia de trabajo (`~/.claude/skills/atlas`), subís `VERSION`, anotás en `CHANGELOG.md`, y `./PUBLISH.sh "<resumen>"` (sync limpio sin proyectos privados + commit + push). Todos lo reciben automático.

---

## Uso

- **`/atlas <componente>`** — implementa/refina un componente con el flujo completo.
- **`/atlas design <cosa>`** — **PITCH de agencia**: genera 3 conceptos impactantes divergentes (no shipea). El músculo creativo.
- **`/atlas`** (sin componente, dentro de un repo registrado) — modo proxy: lee tu backlog y propone el próximo paso.
- **`/atlas`** (fuera de todo repo) — **modo universal**: aplica el codex como filtro de calidad a un mockup/HTML/asset suelto y lo puntúa contra el Gate 10/10.
- **`/atlas innovate`** — ideación net-new de features. **`/atlas grow`** — hace crecer el propio criterio del motor.

---

## Dependencias opcionales

El motor referencia otras skills de Claude Code para algunos pasos (review, smoke, mobile, certificación). Si no las tenés, esos pasos degradan con gracia (el flujo sigue). Las principales: `/matu` (certificación), `/impeccable` (design laws anti-slop), `/implement-mobile`, `/review`, `/smoke-agent`, `/qa`. ATLAS funciona sin ellas; con ellas, redondea el 10/10.

Herramientas externas usadas por los playbooks (instalá según necesidad): `ffmpeg` + `yt-dlp` (estudio de video), `grok-cli` u otro generador (video/imagen), Playwright/simctl/adb (visual-diff). Stack de craft: `react-native-skia`, `react-native-reanimated`, `rive-react-native` (mobile) · `three` + `@react-three/fiber` + `@react-three/drei` + `@react-three/postprocessing` (web 3D).

---

## La filosofía en una línea

> Restraint = sofisticación. Si podés nombrar el efecto, está demasiado alto. Si el diseño sirve para otra empresa cambiándole los textos, es slop. World-class = decisiones tomadas en contra del diseño + realismo de material/luz/movimiento + la imperfección de una herramienta real.

Empezá por leer `skills/atlas/universal-craft-codex.md`. Ahí está todo el criterio.
