# Registrar tu proyecto en ATLAS (4 pasos)

ATLAS detecta el proyecto por el directorio donde lo invocás. Para que reconozca el tuyo:

1. **Copiá esta carpeta** con el nombre de tu proyecto (kebab-case, sin espacios):
   ```bash
   cp -R ~/.claude/skills/atlas/projects/_TEMPLATE ~/.claude/skills/atlas/projects/mi-proyecto
   ```

2. **Editá `project.json`** — lo mínimo imprescindible:
   - `name` · `repo_path` (ruta ABSOLUTA a tu repo — es lo que ATLAS matchea contra tu directorio actual) · `typecheck_cmd` · `dev_server_cmd` + `dev_server_port` (para el visual-diff web) · `mockup_base_path`.
   - El resto tiene defaults razonables; ajustalos cuando los necesites.

3. **Llená `brand-context.md`** — tu OVERLAY: color de acción único, canvas con tinte, tipografía, radius, pieza signature, voz, restricciones duras. Cuanto más específico, mejores los mockups del Creative Spin y más duro el review. (El codex universal ya trae las leyes; esto las aterriza a TU marca.)

4. **Probá:** abrí Claude Code dentro de tu repo y corré `/atlas <componente>`. Si `project.json:repo_path` coincide con tu directorio, ATLAS lo detecta y arranca el flujo.

> Atajo: en vez de hacerlo a mano, invocá `/atlas` dentro de tu repo sin configurarlo — ATLAS detecta que no hay proyecto y te ofrece correr el **onboarding** (`onboarding.md`), que genera estos archivos con vos.

`_TEMPLATE/` no se toca: es la plantilla. Su `repo_path` es ficticio a propósito, así nunca matchea ningún directorio real.
