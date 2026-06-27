# ATLAS — Gaps de vanguardia 2026 (qué falta para 10/10)

> Estudio YouTube 2026-06-04 (método youtube-study-playbook). 5 referentes:
> Cole Medin "5 Techniques Separating Top Agentic Engineers" + "Agent Teams" · Chase AI "Top 10
> Skills/Plugins/CLIs April 2026" · "Skill Creator: Evals & Benchmarking" · Zen van Riel "Agentic
> Engineer Workflow 2026". Crudos locales en ~/yt (no commitear). Gap analysis vs lo que /atlas ya tiene.

## EL GAP #1 (convergente en 3 fuentes): /atlas no se mide a sí mismo
Tiene gates por tarea (typecheck · pixelmatch · /matu >=9.5 · smoke) pero NO un eval-harness del propio
flujo: nada que mida objetivamente si /atlas mejora o degrada entre versiones. Evidencia viva: la
compresión del motor (−23%, 2026-06-04) se hizo "a fe", sin probar que la calidad se mantuvo.

**Pieza estrella a agregar = `atlas-eval`** (skill + script): set fijo de tareas-referencia que se corren
con y sin un cambio, midiendo pass-rate /matu + tokens + regresión visual (pixelmatch). Cada cambio al
motor pasa de "creo" a "subió/bajó X%". Es lo que cierra el loop de calidad → 10/10.

## Ranking de gaps para 10/10 (filtrado a founder solista · anti-over-tooling)

| # | Gap | Qué agregar | Impacto / esfuerzo |
|---|---|---|---|
| 1 | No se auto-mide | `atlas-eval`: tareas-referencia + A/B (atlas on/off) + regresión | Cierra el loop de calidad · medio |
| 2 | Contexto PLAN<->EXEC mezclado | context-reset gate: plan.md -> contexto fresco -> ejecutar solo del plan | -15% alucinación (Cole) · bajo |
| 3 | Self-learning manual | loop System-Evolution: agente opus post-FAIL propone fix al SISTEMA (skill/rules), no a la línea · conecta con learned-patterns | auto-mejora compuesta · medio |
| 4 | Review 1 solo modelo (sesgo Anthropic) | Codex como 2do reviewer CONDICIONAL (safety/arquitectura) | ojos externos selectivos · bajo |
| 5 | Paralelo "ciego" | contract-first scheduling (DB->API->FE secuencial, resto paralelo) | evita contrato roto multi-capa · medio |

## Descartado (over-tooling · contra la ley anti-over-tooling de Ale)
- Obsidian -> ya tiene memoria Karpathy ([[tooling_karpathy_kb]]).
- LightRAG / GraphRAG -> no escala para corpus personal.
- Firecrawl / GWS CLI -> sin uso hoy.
- Auto-research (loop ML sin freno) -> explosión de costo.
- Multi-agent teams full (T-Mux / P2P / swarms) -> infra enterprise; el "contract-first" liviano captura el 80% sin la infra.

## Recomendación
Construir `atlas-eval` primero (gap #1). Todo lo demás (#2 context-reset, #3 self-evolution) son
refinamientos sobre eso. Nada de swarms ni RAG.

## Estado de implementación (2026-06-04)
- **#1 atlas-eval → HECHO** (commit 970ab7f · `eval/`). El harness se auto-mide.
- **#2 context-reset PLAN→EXEC → HECHO** (motor.md PASO 5 · regla atómica).
- **#3 self-evolution loop → HECHO** (motor.md PASO 7 · post-FAIL propone fix al sistema → learned-patterns).
- **#4 reviewer adversarial → HECHO** (versión Anthropic gratis · motor.md PASO 7): 2º par de ojos (opus REFUTADOR) en safety/arquitectura, sin credencial ni costo. Codex cross-vendor (pago) = upgrade OPCIONAL [ALE] si algún día querés el ángulo OpenAI.
- **#5 contract-first scheduling → DESCARTADO** para founder solista (es para teams multi-capa · over-tooling). Re-evaluar si el proyecto suma equipo.

**Resultado:** /atlas = 10/10 para el perfil solista. #1-#4 HECHO y verificado con atlas-eval (PASS limpio). #5 descartado a propósito (teams). Codex (pago, cross-vendor) queda como único opcional, no necesario.
