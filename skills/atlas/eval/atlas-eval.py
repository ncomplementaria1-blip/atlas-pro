#!/usr/bin/env python3
"""
atlas-eval — eval-harness del propio /atlas (gap #1 · roadmap-2026-gaps.md).

Checks DETERMINISTAS (cero tokens de modelo) sobre la skill: detectan regresión
al editar el motor — gates de calidad presentes, leyes de autonomía, progressive
disclosure sano, budget anti-bloat (vs baseline), sintaxis de scripts.

Uso:
  python3 eval/atlas-eval.py             # corre evals, compara vs baseline -> PASS/FAIL
  python3 eval/atlas-eval.py --snapshot  # guarda el estado actual como baseline.json
Exit: 0 PASS · 1 FAIL (regresión crítica).

Modo A/B PROFUNDO (manual · usa modelo · NO automatizado acá): correr /atlas sobre
3-5 tareas-referencia certificadas, con y sin un cambio, y comparar /matu score +
tokens + pixelmatch. Ver eval/README.md. Este script cubre el A/B ESTRUCTURAL barato.
"""
import os, re, json, subprocess, sys, glob

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
ATLAS = os.path.dirname(EVAL_DIR)
MOTOR = next((a for a in sys.argv[1:] if a.endswith('.md')), os.path.join(ATLAS, 'motor.md'))
BASELINE = os.path.join(EVAL_DIR, 'baseline.json')

motor = open(MOTOR, encoding='utf-8').read()
SNAPSHOT = '--snapshot' in sys.argv

# ---- métricas actuales (deterministas)
motor_lines = motor.count('\n') + 1
motor_tokens = len(motor) // 4
paso_headers = len(re.findall(r'^## PASO ', motor, re.M)) + len(re.findall(r'^## ATLAS_MODE', motor, re.M))
playbooks = len(glob.glob(os.path.join(ATLAS, '*-playbook.md')))

# Gates de calidad + leyes que DEBEN existir (checks absolutos, no dependen de baseline)
REQUIRED = {
    'gate typecheck': 'typecheck',
    'gate visual 6G': '6g',
    'gate pixelmatch': 'pixelmatch',
    'gate /matu': 'matu',
    'gate smoke': 'smoke',
    'ley FALSE PASS': 'false pass',
    'ley 2 pausas reales': 'pausas reales',
    'ley silencio operacional': 'silencio operacional',
    'ley tabla decisiones': 'tabla de decisiones',
    'ley SELF-AUDIT': 'self-audit',
}
gates_present = sum(1 for kw in REQUIRED.values() if kw in motor.lower())

# Progressive disclosure: archivos on-demand que deben existir Y estar referenciados
ONDEMAND = ['innovate.md', 'grow.md']  # autonomía NO es on-demand: sus ejemplos van inline (enforcement)
WHITELIST_REF = ['innovate.md', 'onboarding.md',
                 'worldclass-craft.md', 'skill-design-playbook.md',
                 'fable5-transfer-playbook.md', 'cinematography-playbook.md',
                 'youtube-study-playbook.md']

if SNAPSHOT:
    base = {
        'motor_lines': motor_lines, 'motor_tokens': motor_tokens,
        'paso_headers': paso_headers, 'gates_present': gates_present,
        'playbooks': playbooks,
        'note': 'baseline 2026-06-12 post mejoras-finales (transferencia fable5 + intel + 6I + grow + hook pre-commit)',
    }
    json.dump(base, open(BASELINE, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print('baseline.json guardado:')
    print(json.dumps(base, indent=2, ensure_ascii=False))
    sys.exit(0)

base = json.load(open(BASELINE, encoding='utf-8')) if os.path.exists(BASELINE) else None
results = []  # (sev, name, ok, detail)
def chk(sev, name, ok, detail=''): results.append((sev, name, bool(ok), detail))

# A. Gates/leyes absolutos
for name, kw in REQUIRED.items():
    chk('CRIT', name, kw in motor.lower())
# B. Flujo de pasos
chk('CRIT', 'flujo >=10 pasos', paso_headers >= 10, f'{paso_headers} headers PASO/MODE')
# B2. ENFORCEMENT: las leyes deben tener ejemplos concretos INLINE en el motor (no abstractas).
# Caza el bug 2026-06-06: comprimir autonomía a archivo on-demand que nunca se cargaba.
inline_examples = len(re.findall(r'"¿|^- "|^×', motor, re.M))
chk('CRIT', 'leyes con ejemplos inline (enforcement)', inline_examples >= 30, f'{inline_examples} ejemplos inline (min 30)')
# C. Progressive disclosure on-demand
for f in ONDEMAND:
    ok = os.path.exists(os.path.join(ATLAS, f)) and f in motor
    chk('HIGH', f'on-demand {f} existe+referenciado', ok)
# D. Referencias rotas a archivos clave de la skill (raíz)
refs = set(re.findall(r'([a-z0-9_-]+\.(?:md|sh|py))', motor))
broken = [f for f in WHITELIST_REF if f in refs and not os.path.exists(os.path.join(ATLAS, f))]
chk('HIGH', 'sin refs rotas a archivos clave', len(broken) == 0, f'rotas: {broken}')
# E. Budget anti-bloat + no perder piezas (vs baseline)
if base:
    cap = int(base['motor_lines'] * 1.10)
    chk('HIGH', 'budget motor (<=baseline+10%)', motor_lines <= cap, f'{motor_lines}L vs cap {cap}L')
    chk('CRIT', 'no perdio gates/leyes vs baseline', gates_present >= base['gates_present'], f'{gates_present} vs {base["gates_present"]}')
    chk('CRIT', 'no perdio pasos vs baseline', paso_headers >= base['paso_headers'], f'{paso_headers} vs {base["paso_headers"]}')
    chk('LOW', 'no perdio playbooks vs baseline', playbooks >= base['playbooks'], f'{playbooks} vs {base["playbooks"]}')
else:
    chk('LOW', 'baseline presente', False, 'corré --snapshot primero')
# F. Sintaxis de scripts de la skill
for py in sorted(set(glob.glob(os.path.join(ATLAS, '*.py')) + glob.glob(os.path.join(EVAL_DIR, '*.py')))):
    r = subprocess.run([sys.executable, '-m', 'py_compile', py], capture_output=True)
    chk('MED', f'py sintaxis {os.path.basename(py)}', r.returncode == 0, r.stderr.decode()[:80])
for sh in sorted(glob.glob(os.path.join(ATLAS, '*.sh'))):
    r = subprocess.run(['bash', '-n', sh], capture_output=True)
    chk('MED', f'bash sintaxis {os.path.basename(sh)}', r.returncode == 0, r.stderr.decode()[:80])

# G. INSTRUMENTACIÓN VIVA (fix auditoría 2026-06-07): el eval era CIEGO a si la telemetría del
#    runtime se escribe (estado/checkpoint/learned-patterns estaban congelados con eval en verde).
#    Chequea que el writer exista, esté CABLEADO al motor (open + learn) y que la telemetría de
#    cada proyecto esté bien formada. Sin fechas → determinista.
chk('HIGH', 'atlas-log.py existe (writer telemetría)', os.path.exists(os.path.join(ATLAS, 'atlas-log.py')))
chk('HIGH', 'motor cablea atlas-log open (abre sesión)', bool(re.search(r'atlas-log\.py["\s].*open', motor)))
chk('HIGH', 'motor cablea atlas-log learn (self-evolution)', bool(re.search(r'atlas-log\.py["\s].*learn', motor)))
# G2. Fixes de comportamiento (audit 2026-06-08): regresión = repetir los incidentes reales.
skill_md = open(os.path.join(ATLAS, 'SKILL.md'), encoding='utf-8').read() if os.path.exists(os.path.join(ATLAS, 'SKILL.md')) else ''
alog = open(os.path.join(ATLAS, 'atlas-log.py'), encoding='utf-8').read() if os.path.exists(os.path.join(ATLAS, 'atlas-log.py')) else ''
chk('HIGH', 'SKILL: filler detection (palabras-comando no van a proxy)', 'TASK_KIND' in skill_md and 'FILLER' in skill_md)
chk('HIGH', 'SKILL: propuesta durable (get-propuesta + ley propose)', 'get-propuesta' in skill_md and 'propose' in skill_md)
chk('HIGH', 'atlas-log soporta propose/get-propuesta', '"propose"' in alog and 'get-propuesta' in alog)
chk('HIGH', 'motor 6H: keyword sin clip = SKIP, no falso bloqueo', 'SKIP_NO_VIDEO_OUTPUT' in motor)
chk('HIGH', 'proxy: reality-check antes de proponer (no recrear lo hecho)', 'REALITY-CHECK' in motor and 'REALITY-CHECK' in skill_md)
chk('HIGH', 'motor: close en cierre commit-local (PASS_LOCAL)', 'PASS_LOCAL' in motor)
# Política 2026-06-10 (fable=2x opus por token, verificado ccusage): top-tier review/safety = opus · fable SOLO 6H director.
chk('HIGH', 'política modelo-por-costo (TOP-TIER=opus · review/safety opus SIEMPRE)', 'TOP-TIER = `opus`' in motor and 'opus SIEMPRE' in motor)
chk('HIGH', 'fable acotado a 6H director (única etapa · no quema tokens)', 'model: fable' in motor and motor.count('**fable**') <= 3)
# Transferencia Fable 5 (2026-06-11 · orden Ale): wiring en motor + archivos profundos + ruteo transversal.
chk('HIGH', 'transferencia fable5: motor cablea ruteo (índice single-source + transversales)',
    'TRANSFERENCIA FABLE 5' in motor and 'fable5-transfer-playbook.md' in motor
    and 'seguridad.md' in motor and 'testing-estrategia.md' in motor and 'llm-engineering.md' in motor)
F5_FILES = ['P1-arquitectura.md', 'P2-frontend.md', 'P3-logica-critica.md', 'P4-creatividad.md',
            'P5-metacognicion.md', 'seguridad.md', 'testing-estrategia.md', 'llm-engineering.md']
f5_missing = [f for f in F5_FILES if not os.path.exists(os.path.join(ATLAS, 'fable5', f))]
chk('HIGH', 'transferencia fable5: 8 archivos profundos existen', len(f5_missing) == 0, f'faltan: {f5_missing}')
_idx_path = os.path.join(ATLAS, 'fable5-transfer-playbook.md')
_idx = open(_idx_path, encoding='utf-8').read() if os.path.exists(_idx_path) else ''
chk('HIGH', 'transferencia fable5: índice rutea SEC/TEST/LLM + scope por proyecto',
    all(s in _idx for s in ['seguridad.md', 'testing-estrategia.md', 'llm-engineering.md', 'SCOPE POR PROYECTO']))
# Suite behavioral (P5-D3 · 2026-06-12): el examen congelado existe y declara su ley.
_bs_path = os.path.join(EVAL_DIR, 'behavioral-suite.md')
_bs = open(_bs_path, encoding='utf-8').read() if os.path.exists(_bs_path) else ''
chk('MED', 'suite behavioral congelada existe (3 REF + ley de congelamiento)',
    'CONGELADA' in _bs and all(r in _bs for r in ['REF-L', 'REF-N', 'REF-C']))
# Motor sin utcnow deprecado (migrado 2026-06-12 a timezone-aware).
chk('MED', 'motor sin datetime.utcnow deprecado', 'utcnow' not in motor)
# Worktree-aware (2026-06-12 · ley multisesión): detección en SKILL + operación en motor.
chk('MED', 'SKILL: detección worktree-aware (git-common-dir)', 'git-common-dir' in skill_md)
chk('MED', 'motor: opera en el worktree (show-toplevel + override PROJECT_REPO)', 'show-toplevel' in motor and 'WORKTREE' in motor)
# Intel gate (2026-06-12): aprende del mundo con triggers + TTL — gate en motor + playbook + cosecha en grow.
chk('HIGH', 'intel gate: motor lo cablea (PASO 1C) + playbook existe',
    'INTEL GATE' in motor and 'intel-playbook.md' in motor
    and os.path.exists(os.path.join(ATLAS, 'intel-playbook.md')))
# Contratos de dispatch (audit 2026-06-12): todo dispatch con model: explícito + criterio fable5 inline en templates.
chk('HIGH', 'contratos de dispatch: model explícito en todos (audit elevación)', motor.count('model:') >= 16, f"{motor.count('model:')} occurrencias (min 16)")
chk('MED', 'templates con slot de criterio fable5 inline (enforcement 2026-06-06)', motor.count('CRITERIO FABLE5') >= 2 and motor.count('CRITERIO OBLIGATORIO') >= 1)
# Economía de contexto (2026-06-12): ahorro sin pérdida — quirúrgico + cache-friendly + pilar por modo.
chk('MED', 'economía de contexto en motor (quirúrgico · prefijo estable · pilar por modo)', 'ECONOMÍA DE CONTEXTO' in motor and 'ECONOMÍA POR MODO' in motor)
# Prompt craft + essence gate (2026-06-12): esencia al 100% en todo lo generativo — imagen tiene su gate como el video.
chk('HIGH', 'prompt-craft: playbook existe + motor cablea 6I ESSENCE GATE',
    os.path.exists(os.path.join(ATLAS, 'prompt-craft-playbook.md'))
    and 'ESSENCE GATE' in motor and 'prompt-craft-playbook.md' in motor and 'ESSENCE_STATUS' in motor)
# GC automático (2026-06-12): basura conocida se limpia en cada arranque — sin cron.
chk('MED', 'gc automático: script existe + PASO 0 lo invoca',
    os.path.exists(os.path.join(ATLAS, 'atlas-gc.sh')) and 'atlas-gc.sh' in motor)
# GC limpia session-locks stale >2h (2026-06-15: cierra el caso del lock fantasma · proactivo).
_gc_path = os.path.join(ATLAS, 'atlas-gc.sh')
_gc = open(_gc_path, encoding='utf-8').read() if os.path.exists(_gc_path) else ''
chk('MED', 'gc limpia session-locks stale >2h (proactivo · no toca locks vivos)',
    'session-lock.json' in _gc and 'LOCKS_CLEANED' in _gc and '2.0' in _gc)
for pdir in sorted(glob.glob(os.path.join(ATLAS, 'projects', '*'))):
    if not os.path.isdir(pdir):
        continue
    pname = os.path.basename(pdir)
    est = os.path.join(pdir, 'project-estado.json')
    if not os.path.exists(est):
        continue
    try:
        e = json.load(open(est, encoding='utf-8'))
        well_formed = isinstance(e.get('sesiones_totales'), int) and 'ultima_sesion' in e
    except Exception:
        well_formed = False
    chk('MED', f'telemetría {pname}: estado bien formado', well_formed)

# ---- reporte
sev_w = {'CRIT': 3, 'HIGH': 2, 'MED': 1, 'LOW': 0.5}
total = sum(sev_w[s] for s, _, _, _ in results)
passed = sum(sev_w[s] for s, _, ok, _ in results if ok)
fails = [(s, n, d) for s, n, ok, d in results if not ok]

print(f"ATLAS-EVAL · motor {motor_lines}L / {motor_tokens}tok · {paso_headers} pasos · {gates_present}/{len(REQUIRED)} gates-leyes · {playbooks} playbooks")
if base:
    print(f"baseline   · motor {base['motor_lines']}L / {base['motor_tokens']}tok · {base['paso_headers']} pasos · {base['gates_present']} gates · {base['playbooks']} playbooks")
print(f"score: {passed:.1f}/{total:.1f} = {round(100*passed/total)}%\n")
for s, n, ok, d in results:
    mark = 'OK ' if ok else 'XX '
    print(f"  {mark}[{s}] {n}" + (f"  · {d}" if d and not ok else ''))

crit_fail = any(s == 'CRIT' for s, _, _ in fails)
print()
if crit_fail:
    print("RESULTADO: FAIL — regresion critica (revertir o arreglar antes de commitear)")
elif fails:
    print(f"RESULTADO: PASS con {len(fails)} warning(s)")
else:
    print("RESULTADO: PASS limpio")
sys.exit(1 if crit_fail else 0)
