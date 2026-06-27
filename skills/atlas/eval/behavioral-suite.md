# Suite Behavioral CONGELADA · el examen que NO aprende
> Implementa P5-D3 de la Transferencia Fable 5 (2026-06-12 · orden Ale "corrige todas
> tus propuestas"). atlas-eval.py mide ESTRUCTURA (archivos, leyes, presupuestos);
> esta suite mide COMPORTAMIENTO: ¿/atlas ejecuta mejor o peor después de un cambio?
>
> **LEY DE CONGELAMIENTO:** las 3 tareas-referencia de abajo NO se editan, NO se
> "mejoran", NO se adaptan al motor nuevo. Un examen que evoluciona junto con el
> sistema no mide nada (P5-D3). Cambiarlas requiere orden explícita de Ale y resetea
> el historial comparativo.

## Cuándo se corre

- ANTES de mergear un cambio GRANDE del motor (nuevo paso, gate nuevo, reescritura
  de política). NO para fixes de 1 línea — para eso basta atlas-eval.
- Sospecha de degradación silenciosa (más rounds de /matu que de costumbre, más
  preguntas prohibidas en learned-patterns).
- A pedido de Ale.

Costo por corrida: 1-3 flujos /atlas completos. Por eso es manual y selectiva —
el examen barato (atlas-eval) corre siempre; este corre cuando importa.

## Protocolo A/B

1. **Branch desechable:** los runs ocurren en un worktree/branch `eval/behavioral-*`
   del repo objetivo — NADA se mergea a producto. Al terminar: branch borrada.
2. **Run B (motor actual):** ejecutar la(s) tarea(s) de referencia con el motor @HEAD.
3. **Run A (motor previo, solo si hay duda):** `git -C ~/.claude/skills/atlas stash`
   del cambio → re-correr → `stash pop`. Si existe historial previo de la misma REF,
   usar ese registro como A (más barato que re-correr).
4. **Comparar métricas** (fuentes: `atlas-proxy-log.jsonl` · flow-checkpoint.json ·
   learned-patterns.md del proyecto):

| Métrica | Fuente | Regresión si |
|---|---|---|
| `matu_score_final` | checkpoint | baja >0.2 vs registro previo |
| `matu_rounds_done` | checkpoint | sube +1 o más |
| `tier` real vs estimado | atlas-proxy-log | sube de tier (VERDE→NARANJA) sin razón |
| `diff_pct` pixelmatch | 6G-2.5 output | sube >2 puntos |
| Violaciones de autonomía | learned-patterns (entradas nuevas del run) | CUALQUIER pregunta prohibida = FAIL duro |
| Carga de pilares fable5 | transcript del run | dispatch sin el pilar correspondiente = FAIL de wiring |

5. **Veredicto:** cualquier celda en regresión → el cambio del motor se revierte o se
   arregla ANTES de quedar. Sin celda en regresión → el cambio queda + registrar el
   run en `eval/behavioral-history.jsonl` (append: fecha, REF, commit del motor,
   métricas) — ese historial es la línea base de la próxima corrida.

## Las 3 tareas-referencia (CONGELADAS · cubren los 3 modos del Router)

### REF-L · Replicación spec-driven (light · el caso más frecuente)
- **Tarea:** implementar la tarjeta de progreso del master certificado de Mi día
  (`docs/mockups/mobile/mi-dia-v2/COCKPIT-FINAL.html` · /matu PASS 9.58) como
  componente RN aislado en la branch desechable.
- **Esperado:** Router → `master_covers=yes` · light · creative_spin=[] · tier ≤VERDE
  · sonnet impl · carga P2+P5+TEST · pixelmatch ≤5% · /matu light ≥9.5 · cero
  preguntas · cero mejoras no pedidas (tabla 1B respetada).

### REF-N · Fix quirúrgico (nano · disciplina de alcance)
- **Tarea:** "el token `--text-muted` de la tarjeta REF-L diverge del master en 1
  valor — corregirlo" (fix sintético ≤30 líneas sobre el output de REF-L).
- **Esperado:** Router → nano · tier AZUL · haiku impl · diff ≤30 líneas · /matu
  nano ≥9.0 · NINGÚN archivo extra tocado (scope discipline) · cero spin.

### REF-C · Diseño nuevo (canonical · el camino completo)
- **Tarea:** "tarjeta de resumen semanal de hábitos" SIN master (componente
  sintético — no existe en el producto a propósito, para que siempre sea NEW).
- **Esperado:** Router → `master_covers=no` · canonical · creative_spin≠[] · 3
  mockups A/B/C + Brand Council + gate anti-slop · carga P2+P4+P5+TEST · /matu
  canonical ≥9.5 · safe-para-datos-sensibles (cero rachas punitivas en el diseño) · tier
  NARANJA/ROJO declarado ANTES de ejecutar (COSTO_GATE visible).

### REF-G · Generativo (prompt-craft + 6I · el camino de assets)
*(Agregada 2026-06-12 PRE-primer-run — historial vacío, sin reset — por orden explícita
de Ale de cobertura completa, como exige la ley de congelamiento.)*
- **Tarea:** "og-image de marca del proyecto (1200×630) desde el brief" — generativa
  pura, sin master previo, SIEMPRE nueva.
- **Esperado:** lista de ESENCIA escrita ANTES de generar (prompt-craft B1) → prompt
  contractual con pre-flight 6/6 → generación → gate 6I corre → `ESSENCE_STATUS:
  PASS (N/N + cero tells)` → asset + `<asset>.prompt.md` guardados juntos · cero
  adjetivos de resultado en el prompt · paleta DNA con valores literales.

## Qué mide cada una (por diseño)

REF-L mide **fidelidad y eficiencia** (el 80% del trabajo real) · REF-N mide
**disciplina de alcance** (que barato siga siendo quirúrgico) · REF-C mide **calidad
de diseño y proceso completo** (que canonical no se degrade ni se salte gates) ·
REF-G mide **el camino generativo** (esencia→contrato→gate 6I — que "100% sin
errores" siga siendo un loop y no un deseo).
Las tres juntas miden el **wiring de la Transferencia** (¿cargó los pilares?) y la
**autonomía** (¿preguntó algo prohibido?).

## Registro

`eval/behavioral-history.jsonl` — una línea por run:
`{"ts": "...", "ref": "REF-L", "motor_commit": "...", "matu_score": 9.6,
"matu_rounds": 1, "tier": "VERDE", "diff_pct": 2.1, "violaciones": 0, "wiring_ok": true}`

Sin historial todavía: el PRIMER run real (el estreno del motor post-transferencia)
funda la línea base.
