#!/usr/bin/env python3
"""
ATLAS Monitor v1.1
Audita el estado de /atlas en un proyecto y reporta plan vs realidad.
Uso: python3 atlas-monitor.py [project_name]
     python3 atlas-monitor.py nutricomai
"""

import json
import os
import sys
import datetime
from pathlib import Path

# --- config ---
ATLAS_DIR = Path.home() / ".claude/skills/atlas"
PROJECT_NAME = sys.argv[1] if len(sys.argv) > 1 else "nutricomai"
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

# 4. Log de ejecucion (en el repo, no en atlas dir)
header("4. Log de ejecucion ATLAS (atlas-proxy-log.jsonl)")
repo_path = project_json.get("repo_path", "") if project_json else ""
log_path = Path(repo_path) / ".claude/atlas-proxy-log.jsonl" if repo_path else None
entries = load_jsonl(log_path) if log_path else []
if not log_path:
    warn("repo_path no definido — no se puede leer el log")
elif not entries:
    warn(f"Sin logs · {log_path}")
    info("El log se crea en PASO 1 (router_costo) y PASO 9 (flujo_completado) del motor")
else:
    print(f"\n  {len(entries)} entradas · ultimas 5:\n")
    for e in entries[-5:]:
        ts  = e.get("ts", "?")[:19]
        ev  = e.get("evento", e.get("event", "?"))
        comp = e.get("componente", e.get("skill", ""))
        tier = e.get("tier_estimado", "")
        mode = e.get("matu_mode", "")
        rds  = e.get("matu_rounds_reales", "")
        extra = " · ".join(filter(None, [tier, mode, f"R{rds}" if rds else ""]))
        print(f"  {ts}  {ev:20s}  {comp:20s}  {extra}")

# 4B. Checkpoint del ultimo flujo
header("4B. Ultimo flujo (flow-checkpoint.json)")
ckpt_path = Path(repo_path) / ".claude/flow-checkpoint.json" if repo_path else None
ckpt = load_json(ckpt_path) if ckpt_path else None
if not ckpt:
    warn(f"Sin checkpoint · {ckpt_path or 'repo_path no definido'}")
    info("El checkpoint se crea en PASO 0 y se actualiza en cada paso del motor")
else:
    paso    = ckpt.get("paso", "?")
    status  = ckpt.get("status", "?")
    comp    = ckpt.get("componente", "?")
    tipo    = ckpt.get("router_tipo", "?")
    mmode   = ckpt.get("matu_mode", "?")
    score   = ckpt.get("matu_score_final", "?")
    mpass   = ckpt.get("matu_pass", "?")
    branch  = ckpt.get("branch_name", "?")
    fid     = ckpt.get("fidelity_score", "N/A")
    ts      = ckpt.get("ts", "?")[:19]
    print()
    if status == "PASS" and paso == 9:
        ok(f"  Flujo completo · PASO {paso} {status}")
    elif status == "PASS":
        warn(f"  Flujo interrumpido · ultimo PASO {paso} {status} · retomar desde PASO {paso + 1}")
    else:
        fail(f"  PASO {paso} {status} · posible sesion cortada")
    print(f"  Componente:  {comp}")
    print(f"  Tipo:        {tipo}  |  Branch: {branch}")
    print(f"  /matu:       {mmode}  |  score {score}  |  pass={mpass}  |  fidelidad {fid}")
    print(f"  Timestamp:   {ts}")

# 4C. Session lock
header("4C. Session lock (session-lock.json)")
lock_path = Path(repo_path) / ".claude/session-lock.json" if repo_path else None
lock = load_json(lock_path) if lock_path else None
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
        "ADR-002 TCA-safe":       "ADR-002" in content,
        "Ley 19.628 (salud)":     "19.628" in content,
        "Ley 21.719":             "21.719" in content,
        "SERNAC compliance":      "SERNAC" in content,
        "MercadoPago":            "mercadopago" in content.lower(),
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

print(f"\n{BOLD}{'='*56}{RESET}\n")
