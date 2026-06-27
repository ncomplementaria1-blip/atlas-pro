#!/usr/bin/env python3
"""
atlas-log — telemetría VIVA del flujo /atlas (fix auditoría 2026-06-07).

Por qué existe: la auditoría encontró que estado/checkpoint/learned-patterns estaban CONGELADOS
(learned-patterns 0 entradas en junio · checkpoint en paso 0 del 2026-05-24 · sesiones_totales=0
tras decenas de runs). Causa raíz: los writes de telemetría eran pasos NO-bloqueantes → se salteaban.
Solución: un solo punto de escritura, invocado como paso BLOQUEANTE en PASO 0 (open) / 7 (learn) / 9-10 (close).
Sin log, el run NO está completo.

Determinista (cero tokens de modelo). Read-modify-write: preserva todas las claves que no toca.

Uso:
  atlas-log.py <project> open       --componente X [--paso 0]
  atlas-log.py <project> checkpoint --paso 6H --status PASS [--componente X]
  atlas-log.py <project> close      --status PASS [--accion "qué se hizo"]
  atlas-log.py <project> learn      --slug y_flip_matu_miss --falla "..." --propuesta "..."
  atlas-log.py <project> propose    --componente X [--accion "contexto de la propuesta"]
  atlas-log.py <project> get-propuesta   # imprime la propuesta pendiente (o NONE)

`propose` persiste la tarea que ATLAS propuso al cierre ("¿arranco X?") en flow-checkpoint.json
→ si Ale responde "dale/arranca" en OTRA sesión (contexto compactado), el modo filler la recupera
de acá en vez de caer a proxy. `open`/`close` la consumen (incidente 2026-06-08 "perdiste el contexto").
Exit: 0 OK · 2 proyecto no encontrado.
"""
import argparse, json, os, sys, datetime

ATLAS_DIR = os.path.dirname(os.path.abspath(__file__))


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return dict(default)


def save_json(path, data):
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def main():
    p = argparse.ArgumentParser(prog="atlas-log")
    p.add_argument("project")
    p.add_argument("event", choices=["open", "checkpoint", "close", "learn", "propose", "get-propuesta"])
    p.add_argument("--paso", default=None)
    p.add_argument("--status", default=None)
    p.add_argument("--componente", default=None)
    p.add_argument("--accion", default=None)
    p.add_argument("--slug", default=None)
    p.add_argument("--falla", default=None)
    p.add_argument("--propuesta", default=None)
    a = p.parse_args()

    pdir = os.path.join(ATLAS_DIR, "projects", a.project)
    if not os.path.isdir(pdir):
        print(f"atlas-log · ERROR · proyecto no encontrado: {pdir}")
        sys.exit(2)

    estado_path = os.path.join(pdir, "project-estado.json")
    ckpt_path = os.path.join(pdir, "flow-checkpoint.json")
    learn_path = os.path.join(pdir, "learned-patterns.md")
    ts = now_iso()

    if a.event == "learn":
        slug = a.slug or "system_evolution"
        block = (
            f"\n---\n{ts[:10]} · system_evolution · {slug}\n"
            f"Falla: {a.falla or '(sin descripción)'}\n"
            f"Propuesta (NO aplicada · espera OK Ale): {a.propuesta or '(sin propuesta)'}\n"
            f"Origen: PASO 7 self-evolution (atlas-log)\n---\n"
        )
        with open(learn_path, "a", encoding="utf-8") as f:
            f.write(block)
        print(f"atlas-log · learn · append a learned-patterns.md · {slug}")
        return

    # eventos que tocan estado + checkpoint
    estado = load_json(estado_path, {"sesiones_totales": 0})
    ckpt = load_json(ckpt_path, {})

    if a.event == "get-propuesta":
        prop = ckpt.get("propuesta_pendiente")
        print(f"{prop} · propuesta_ts={ckpt.get('propuesta_ts','?')}" if prop else "NONE")
        return

    if a.event == "propose":
        ckpt.update({"propuesta_pendiente": a.componente or "?", "propuesta_ts": ts,
                     "proyecto": a.project})
        if a.accion:
            ckpt["propuesta_contexto"] = a.accion
        save_json(ckpt_path, ckpt)
        print(f"atlas-log · propose · {a.project} · propuesta_pendiente={a.componente} · {ts}")
        return

    if a.event == "open":
        estado["ultima_sesion"] = ts
        ckpt.update({"paso": a.paso or "0", "status": "IN_PROGRESS",
                     "componente": a.componente or ckpt.get("componente", "?"),
                     "proyecto": a.project, "ts": ts})
        # arrancó un run → la propuesta pendiente se consumió
        for k in ("propuesta_pendiente", "propuesta_ts", "propuesta_contexto"):
            ckpt.pop(k, None)
    elif a.event == "checkpoint":
        ckpt.update({"ts": ts, "proyecto": a.project})
        if a.paso is not None:
            ckpt["paso"] = a.paso
        if a.status is not None:
            ckpt["status"] = a.status
        if a.componente is not None:
            ckpt["componente"] = a.componente
    elif a.event == "close":
        estado["sesiones_totales"] = int(estado.get("sesiones_totales", 0) or 0) + 1
        estado["ultima_sesion"] = ts
        if a.accion:
            estado["ultima_accion"] = a.accion
        ckpt.update({"status": a.status or "PASS", "ts": ts, "proyecto": a.project})
        for k in ("propuesta_pendiente", "propuesta_ts", "propuesta_contexto"):
            ckpt.pop(k, None)

    save_json(estado_path, estado)
    save_json(ckpt_path, ckpt)
    print(f"atlas-log · {a.event} · {a.project} · sesiones={estado.get('sesiones_totales','?')} · "
          f"paso={ckpt.get('paso','?')} · status={ckpt.get('status','?')} · {ts}")


if __name__ == "__main__":
    main()
