# atlas-eval — el harness que mide al harness

Gap #1 del roadmap 2026 (ver `../roadmap-2026-gaps.md`): /atlas tenía gates por tarea pero no se
medía a sí mismo. Esto cierra el loop — detecta regresión cada vez que se edita el motor.

## Uso rápido

```bash
python3 eval/atlas-eval.py             # corre los evals vs baseline -> PASS/FAIL (exit 0/1)
python3 eval/atlas-eval.py --snapshot  # re-graba baseline.json (tras un cambio aprobado)
python3 eval/atlas-eval.py /tmp/otro-motor.md   # evaluar un motor alternativo (testing)
```

## Cuándo correrlo (LEY)
- **Antes y después de tocar `motor.md`** (compresión, extracción, refactor). Si el eval pasa de PASS a
  FAIL -> la edición rompió algo: revertir o arreglar antes de commitear.
- Tras un cambio aprobado que sube el baseline a propósito (ej. nuevo gate) -> `--snapshot` para fijar el nuevo piso.

## Qué chequea (determinista · cero tokens de modelo)
- **CRIT** — los 10 gates/leyes presentes (typecheck, 6G, pixelmatch, /matu, smoke, FALSE PASS, 2 pausas
  reales, silencio operacional, tabla de decisiones, SELF-AUDIT) · flujo >=10 pasos · no perder gates/pasos vs baseline.
- **HIGH** — progressive disclosure sano (innovate.md + autonomy-examples.md existen y referenciados) ·
  sin refs rotas a archivos clave · budget anti-bloat (motor <= baseline +10%).
- **MED** — sintaxis de los scripts (.py via py_compile, .sh via bash -n).
- **LOW** — no perder playbooks.

FAIL en cualquier CRIT -> exit 1 (regresión que bloquea commit). HIGH/MED/LOW -> warnings.

## baseline.json
Foto de referencia (líneas, tokens, # gates, # pasos, # playbooks). Versionado en git para detectar
drift entre sesiones. Se actualiza solo con `--snapshot` (cambio deliberado), nunca automático.

## Modo A/B PROFUNDO (manual · usa modelo · no automatizado acá)
El script cubre el A/B ESTRUCTURAL barato. Para el A/B de COMPORTAMIENTO (¿el output sigue siendo
world-class?), procedimiento manual cuando un cambio al motor es grande:
1. Elegir 3-5 tareas-referencia ya certificadas (pantallas con /matu PASS conocido + master).
2. Correr cada una con el motor NUEVO y con el motor ANTERIOR (git stash / branch).
3. Comparar: /matu score · tokens consumidos · pixelmatch vs master.
4. Si el nuevo no puntúa igual o mejor en /matu y 6G -> no mergear el cambio.

Esto es lo que faltó al comprimir el motor (2026-06-04): el A/B estructural ya lo cubre el script;
el A/B de comportamiento queda para cambios de alto riesgo.
