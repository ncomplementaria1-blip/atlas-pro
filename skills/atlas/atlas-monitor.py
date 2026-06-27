#!/usr/bin/env python3
"""
ATLAS Monitor v1.1
Audita el estado de /atlas en un proyecto y reporta plan vs realidad.
Uso: python3 atlas-monitor.py [project_name]
     python3 atlas-monitor.py el proyecto
"""

import json
import os
import sys
import datetime
from pathlib import Path

# --- config ---
ATLAS_DIR = Path.home() / ".claude/skills/atlas"
PROJECT_NAME = sys.argv[1] if len(sys.argv) > 1 else "el proyecto"
PROJECT_DIR = ATLAS_DIR / "projects" / PROJECT_NAME

# colores ANSI
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg):    print(f"  {GREEN}OK{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}WARN{RESET} {msg}")
def fail(msg):  print(f"  {RED}FAIL{RESET} {msg}")
def info(msg):  print(f"  {CYAN}INFO{RESET} {msg}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")

# --- helpers ---
def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None

def load_jsonl(path):
    lines = []
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    lines.append(json.loads(line))
                except Exception:
                    pass
    except Exception:
        pass
    return lines

def try_read_backlog(repo_path):
    backlog_path = Path(repo_path) / ".claude/BACKLOG.md"
    try:
        content = backlog_path.read_text(encoding="utf-8")
        total = content.count("- [ ]") + content.count("- [x]") + content.count("- [~]") + content.count("- [ALE]")
        done  = content.count("- [x]")
        wip   = content.count("- [~]")
        open_ = content.count("- [ ]")
        ale   = content.count("- [ALE]")
        return {"total": total, "done": done, "wip": wip, "open": open_, "ale": ale, "accessible": True}
    except Exception:
        return {"accessible": False}

# --- main ---
print(f"\n{BOLD}{'='*56}{RESET}")
print(f"{BOLD}  ATLAS Monitor · {PROJECT_NAME.upper()}{RESET}")
print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"{BOLD}{'='*56}{RESET}")

# 1. Verificar config de proyecto
header("1. Configuracion del proyecto")
project_json = load_json(PROJECT_DIR / "project.json")
if not project_json:
    fail("project.json no encontrado — ejecutar onboarding")
    sys.exit(1)

ok(f"Proyecto: {project_json.get('name', PROJECT_NAME)}")
ok(f"Tagline:  {project_json.get('tagline', '?')}")
info(f"Repo:     {project_json.get('repo_path', '?')}")
info(f"Stack:    Expo + Next.js · {project_json.get('deploy','?')} · {project_json.get('country','?')}")

# 2. Estado del proyecto
header("2. Estado del proyecto (project-estado.json)")
estado = load_json(PROJECT_DIR / "project-estado.json")
if not estado:
    fail("project-estado.json no encontrado")
else:
    progreso = estado.get("progreso_pct", 0)
    bar_filled = int(progreso / 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)
    print(f"\n  Progreso: [{bar}] {progreso}%")
    print(f"  Ultima accion: {estado.get('ultima_accion','?')}")
    print()

    listos = estado.get("componentes_listos", [])
    pendientes = estado.get("componentes_pendientes", [])

    print(f"  {GREEN}Componentes listos ({len(listos)}):{RESET}")
    for c in listos:
        print(f"    + {c}")

    print(f"\n  {YELLOW}Componentes pendientes ({len(pendientes)}):{RESET}")
    for c in pendientes:
        print(f"    - {c}")

    hitos = estado.get("hitos", {})
    print(f"\n  Hitos:")
    for k, v in hitos.items():
        if v is True:
            ok(f"  {k}")
        elif v is False:
            fail(f"  {k}")
        else:
            warn(f"  {k}: {v}")

# 3. Masters registrados
header("3. Masters registrados (masters.json)")
masters = load_json(PROJECT_DIR / "masters.json")
if not masters:
    fail("masters.json no encontrado")
else:
    components = masters.get("components", {})
    fallback = masters.get("fallback", "")
    print(f"\n  {len(components)} componentes registrados · fallback: {'si' if fallback else 'NO'}\n")
    repo_path = project_json.get("repo_path", "") if project_json else ""
    for comp, path in components.items():
        full = Path(repo_path) / path if repo_path else None
        if full and full.exists():
            ok(f"  {comp:20s} → {path}")
        elif full and not full.exists():
            warn(f"  {comp:20s} → {path}  [archivo no accesible o no existe]")
        else:
            info(f"  {comp:20s} → {path}")

# 4. Log de ejecucion (en atlas dir — motor escribe ahi desde v1.1)
header("4. Log de ejecucion ATLAS (atlas-proxy-log.jsonl)")
log_path = PROJECT_DIR / "atlas-proxy-log.jsonl"
entries = load_jsonl(log_path)
if not entries:
    warn(f"Sin logs · {log_path}")
    info("El log se crea en PASO 1 (router_costo) y PASO 9 (flujo_completado) del motor")
else:
    print(f"\n  {len(entries)} entradas · ultimas 5:\n")
    for e in entries[-5:]:
        ts   = e.get("ts", "?")[:19]
        ev   = e.get("evento", e.get("event", "?"))
        comp = e.get("componente", e.get("skill", ""))
        tier = e.get("tier_estimado", "")
        mode = e.get("matu_mode", "")
        rds  = e.get("matu_rounds_reales", "")
        extra = " · ".join(filter(None, [tier, mode, f"R{rds}" if rds else ""]))
        print(f"  {ts}  {ev:20s}  {comp:20s}  {extra}")

# 4B. Checkpoint del ultimo flujo (en atlas dir)
header("4B. Ultimo flujo (flow-checkpoint.json)")
ckpt_path = PROJECT_DIR / "flow-checkpoint.json"
ckpt = load_json(ckpt_path)
if not ckpt:
    warn(f"Sin checkpoint · {ckpt_path}")
    info("El checkpoint se crea en PASO 0 y se actualiza en cada paso del motor")
else:
    paso   = ckpt.get("paso", "?")
    status = ckpt.get("status", "?")
    comp   = ckpt.get("componente", "?")
    tipo   = ckpt.get("router_tipo", "?")
    mmode  = ckpt.get("matu_mode", "?")
    score  = ckpt.get("matu_score_final", "?")
    mpass  = ckpt.get("matu_pass", "?")
    branch = ckpt.get("branch_name", "?")
    fid        = ckpt.get("fidelity_score", "N/A")
    fid_status = ckpt.get("fidelity_status", "N/A")
    fid_miss   = ckpt.get("fidelity_mismatches", "N/A")
    ts         = ckpt.get("ts", "?")[:19]

    # Parse fidelity_score → bar display
    if fid != "N/A" and "/" in str(fid):
        try:
            fn, ft = map(int, str(fid).split("/"))
            fpct = int(fn / ft * 100) if ft else 0
            fbar = "█" * int(fpct / 10) + "░" * (10 - int(fpct / 10))
            fid_display = f"{fid} [{fbar}] {fpct}%"
        except Exception:
            fid_display = fid
    else:
        fid_display = fid

    print()
    if status == "PASS" and paso == 9:
        ok(f"  Flujo completo · PASO {paso} {status}")
    elif status == "PASS":
        warn(f"  Interrumpido · ultimo PASO {paso} {status} · retomar desde PASO {paso + 1}")
    else:
        fail(f"  PASO {paso} {status} · posible sesion cortada")
    print(f"  Componente:  {comp}")
    print(f"  Tipo:        {tipo}  |  Branch: {branch}")
    print(f"  /matu:       {mmode}  |  score {score}  |  pass={mpass}")
    if fid_status == "PASS":
        print(f"  Fidelidad 6G: {GREEN}{fid_display}{RESET}  |  status={fid_status}  |  mismatches={fid_miss}")
    elif fid_status == "FAIL":
        print(f"  Fidelidad 6G: {RED}{fid_display}{RESET}  |  status={fid_status}  |  mismatches={fid_miss}")
    else:
        print(f"  Fidelidad 6G: {fid_display}  |  status={fid_status}")
    print(f"  Timestamp:   {ts}")

# 4C. Session lock (en atlas dir)
header("4C. Session lock (session-lock.json)")
lock_path = PROJECT_DIR / "session-lock.json"
lock = load_json(lock_path)
if not lock:
    info("Sin session-lock.json (normal si nunca se ejecuto el motor)")
else:
    locked  = lock.get("locked", False)
    session = lock.get("session", "?")
    task    = lock.get("task", "?")
    ts_lock = lock.get("ts", "?")
    if locked:
        warn(f"  LOCK ACTIVO · sesion={session} · task={task} · desde {ts_lock[:19]}")
        info("  Si la sesion murio, el lock se limpia automaticamente despues de 2h")
    else:
        ok("  Lock libre — no hay sesion ATLAS activa")

# 5. BACKLOG del repo
header("5. BACKLOG del repo (.claude/BACKLOG.md)")
repo_path = project_json.get("repo_path", "") if project_json else ""
if repo_path:
    bl = try_read_backlog(repo_path)
    if bl.get("accessible"):
        total = bl["total"]
        done  = bl["done"]
        open_ = bl["open"]
        wip   = bl["wip"]
        ale   = bl["ale"]
        pct   = int(done / total * 100) if total else 0
        print(f"\n  Total tasks: {total}  |  Done: {done}  |  WIP: {wip}  |  Open: {open_}  |  [ALE]: {ale}")
        bar_f = int(pct / 10)
        bar = "█" * bar_f + "░" * (10 - bar_f)
        print(f"  Completado:  [{bar}] {pct}%")
        if ale > 0:
            warn(f"  {ale} task(s) esperando decision de Ale [ALE]")
    else:
        warn("BACKLOG.md no accesible desde este proceso (Documents/ bloqueado por sandbox)")
        info("Ejecutar desde terminal con acceso completo para ver BACKLOG")
else:
    warn("repo_path no definido en project.json")

# 6. Compliance checks
header("6. Compliance activo (flow-rules.md)")
flow_path = PROJECT_DIR / "flow-rules.md"
if flow_path.exists():
    content = flow_path.read_text(encoding="utf-8")
    checks = {
        "ADR-002 safe-para-datos-sensibles":       "ADR-002" in content,
        "la normativa de protección de datos (salud)":     "la normativa de protección de datos" in content,
        "Ley 21.719":             "21.719" in content,
        "SERNAC compliance":      "SERNAC" in content,
        "un proveedor de pagos":            "un proveedor de pagos" in content.lower(),
        "Anti-patterns hook":     "check-mobile-antipatterns" in content,
    }
    print()
    for rule, present in checks.items():
        if present:
            ok(f"  {rule}")
        else:
            fail(f"  {rule} — no encontrado en flow-rules.md")
else:
    fail("flow-rules.md no encontrado")

# 7. Resumen
header("7. Resumen ejecutivo")
print()
if estado:
    progreso = estado.get("progreso_pct", 0)
    pendientes = estado.get("componentes_pendientes", [])
    proximo = estado.get("proximo_paso", "?")
    if progreso >= 80:
        print(f"  {GREEN}Estado BUENO — {progreso}% completado{RESET}")
    elif progreso >= 50:
        print(f"  {YELLOW}Estado MEDIO — {progreso}% completado · {len(pendientes)} items pendientes{RESET}")
    else:
        print(f"  {RED}Estado BAJO — {progreso}% completado · {len(pendientes)} items pendientes{RESET}")
    print(f"\n  Proximo paso: {proximo}")

if not entries:
    print(f"\n  {YELLOW}ATENCION: sin logs de ejecucion ATLAS{RESET}")
    print(f"  Verificar que el proxy-agent esta logueando en atlas-proxy-log.jsonl")

# 8. Innovation Pipeline
header("8. Innovation Pipeline (innovation-backlog.json)")
innov_path = PROJECT_DIR / "innovation-backlog.json"
innov = load_json(innov_path)
if not innov:
    info(f"Sin innovation-backlog · ejecutar /atlas innovate para generar ideas")
else:
    ideas = innov.get("ideas", [])
    sector = innov.get("sector", "?")
    generated = innov.get("generated_at", "?")[:10]
    total_i = len(ideas)
    propuestas   = [i for i in ideas if i.get("estado") == "propuesta"]
    en_backlog   = [i for i in ideas if i.get("estado") == "en_backlog"]
    implementadas = [i for i in ideas if i.get("estado") == "implementada"]
    print(f"\n  Sector: {sector}  |  Generado: {generated}  |  Total ideas: {total_i}")
    print(f"  Propuestas: {len(propuestas)}  |  En BACKLOG: {len(en_backlog)}  |  Implementadas: {len(implementadas)}")

    # Breakdown por esfuerzo (propuestas)
    s_ideas = [i for i in propuestas if i.get("esfuerzo") == "S"]
    m_ideas = [i for i in propuestas if i.get("esfuerzo") == "M"]
    l_ideas = [i for i in propuestas if i.get("esfuerzo") == "L"]
    print(f"  Pendientes: S(< 4h)={len(s_ideas)}  M(1-3d)={len(m_ideas)}  L(sprint)={len(l_ideas)}")

    # Top 5 por impacto
    IMPACTO_ORDER = {"alto": 0, "medio": 1, "bajo": 2}
    top = sorted(propuestas, key=lambda x: IMPACTO_ORDER.get(x.get("impacto","bajo"), 9))[:5]
    if top:
        print(f"\n  {GREEN}Top ideas pendientes:{RESET}")
        for idea in top:
            iid     = idea.get("id", "?")
            titulo  = idea.get("titulo", "?")[:40]
            tipo    = idea.get("tipo", "?")
            esfuerzo= idea.get("esfuerzo", "?")
            impacto = idea.get("impacto", "?")
            fuente  = idea.get("fuente", "?")[:20]
            print(f"    {iid}  [{tipo}] {titulo:<40} {esfuerzo} · {impacto} · {fuente}")
    if implementadas:
        ok(f"  {len(implementadas)} idea(s) ya implementadas")

# 9. PASO 6G — Fidelity Check Audit
header("9. PASO 6G — Fidelity Check Audit")
ckpt_6g = load_json(ckpt_path)
if not ckpt_6g:
    warn("Sin checkpoint — no se puede auditar 6G")
else:
    fid_s  = ckpt_6g.get("fidelity_score", "N/A")
    fid_st = ckpt_6g.get("fidelity_status", "N/A")
    fid_m  = ckpt_6g.get("fidelity_mismatches", "N/A")
    print()
    if fid_st == "PASS":
        ok(f"  6G PASS · score {fid_s} · {fid_m} mismatches")
    elif fid_st == "FAIL":
        fail(f"  6G FAIL · score {fid_s} · {fid_m} mismatches")
    else:
        warn("  6G no ejecutado en este flujo (fidelity_status=N/A)")
    if fid_s != "N/A" and "/" in str(fid_s):
        try:
            fn6, ft6 = map(int, str(fid_s).split("/"))
            fpct6 = int(fn6 / ft6 * 100) if ft6 else 0
            fbar6 = "█" * int(fpct6 / 10) + "░" * (10 - int(fpct6 / 10))
            col6 = GREEN if fpct6 == 100 else (YELLOW if fpct6 >= 80 else RED)
            print(f"  Score: {col6}{fid_s} [{fbar6}] {fpct6}%{RESET}")
        except Exception:
            print(f"  Score: {fid_s}")

# 9B. Spec file analysis
    comp_6g   = ckpt_6g.get("componente", "")
    spec_path6 = Path(repo_path) / f".claude/implementation-spec-{comp_6g}.md" if repo_path and comp_6g else None
    print()
    if spec_path6 and spec_path6.exists():
        try:
            sc = spec_path6.read_text(encoding="utf-8")
            checked_items   = sc.count("[x]") + sc.count("[x o FAIL]")
            unchecked_items = sc.count("[ ]")
            mismatch_lines  = len([l for l in sc.splitlines() if any(kw in l.upper() for kw in ("MISMATCH", "DIVERGE", "FAIL"))])
            has_juramento   = "JURAMENTO" in sc.upper() or "JURO" in sc.upper()
            has_second_ver  = "SEGUNDO VERIFICADOR" in sc.upper() or "second_verifier" in sc.lower()
            print(f"  Spec: {spec_path6.name}")
            print(f"  Items: checked={checked_items}  unchecked={unchecked_items}  flag-lines={mismatch_lines}")
            if has_juramento:
                ok("  JURAMENTO presente en spec")
            else:
                warn("  JURAMENTO ausente — spec puede ser incompleta")
            if has_second_ver:
                ok("  Segundo verificador registrado")
            else:
                warn("  Segundo verificador no registrado en spec")
        except Exception as e:
            warn(f"  Error leyendo spec: {e}")
    elif comp_6g:
        warn(f"  Spec no encontrada: .claude/implementation-spec-{comp_6g}.md")
    else:
        info("  Sin componente en checkpoint — no se puede localizar spec")

# 9C. Historial de fidelidad del log
    print()
    fid_evts = [e for e in entries if any(kw in str(e).lower() for kw in ("fidelity", "6g_pass", "6g_fail", "fidelity_pass", "fidelity_fail"))]
    if fid_evts:
        print(f"  Historial 6G ({len(fid_evts)} entradas):")
        for e in fid_evts[-3:]:
            ts_e = e.get("ts", "?")[:19]
            ev_e = e.get("evento", "?")
            sc_e = e.get("fidelity_score", "")
            print(f"    {ts_e}  {ev_e}  {sc_e}")
    else:
        info("  Sin eventos 6G en atlas-proxy-log.jsonl")

# 9D. Learned patterns
    lp_path6 = PROJECT_DIR / "learned-patterns.md"
    print()
    if lp_path6.exists():
        try:
            lp = lp_path6.read_text(encoding="utf-8")
            pattern_count = lp.count("\n---\n") // 2
            recent = [l for l in lp.splitlines() if l and len(l) > 4 and l[:4].isdigit()]
            ok(f"  Learned patterns: {pattern_count} patrones registrados (self-learning ACTIVO)")
            if recent:
                print(f"  Ultimo: {recent[-1]}")
        except Exception as e:
            warn(f"  Error leyendo learned-patterns.md: {e}")
    else:
        fail("  learned-patterns.md no encontrado — self-learning NO activo")

print(f"\n{BOLD}{'='*56}{RESET}\n")
