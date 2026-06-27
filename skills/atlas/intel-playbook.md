# INTEL PLAYBOOK · /atlas aprende del mundo (web · YouTube · TikTok · docs)
> Protocolo del PASO 1C · INTEL GATE (2026-06-12 · orden Ale: "que atlas aprenda
> viendo youtube, tiktok o cualquier web cuando va a implementar/diseñar/backend/
> seguridad/código"). El gate EVALÚA siempre; INVESTIGA cuando paga.
>
> **Filosofía (P5 · TTL del conocimiento):** el criterio interno (fable5 + playbooks)
> cubre lo ESTABLE (principios = años). Lo que cambia rápido exige señal fresca del
> mundo: librerías (meses), advisories de seguridad (días), APIs externas (semanas),
> tendencias visuales (semanas). Investigar lo estable = desperdicio; no investigar
> lo volátil = implementar con datos vencidos. El gate separa ambos en segundos.

## La tabla de triggers (la corre el motor en PASO 1C · todas las rutas)

| Trigger (Router/diff/plan) | Qué investigar | TTL cache |
|---|---|---|
| `creative_spin≠[]` (diseño nuevo) | tendencias del sector (TREND INTEL · ya cableado en PASO 2) | 14 días |
| Dependencia NUEVA o major-version bump en el plan | docs oficiales · breaking changes · gotchas reales (issues) | 30 días |
| `safety_touch=yes` | advisories del stack tocado (CVE · OWASP · cambios de la lib de auth/pagos) | 7 días |
| API externa tocada (MercadoPago · WhatsApp · Cloudinary · stores) | changelog/docs oficiales de ESA API | 14 días |
| Técnica que NINGÚN playbook cubre (señal: grep sin match en la skill) | estudio dirigido: artículos + video study (YouTube/TikTok) | permanente → grow |
| REFACTOR/EXTRACT/POLISH/replicación sin nada de lo anterior | **NO investigar** — el criterio interno basta | — |

Regla de oro: si ningún trigger aplica → seguir SIN dispatch (el gate costó 5 segundos,
no 5 minutos). Si aplican varios → UN solo dispatch con todos los focos.

## Técnicas por fuente (el CÓMO)

### Web (docs · advisories · changelogs · artículos)
- `WebSearch` con año actual en la query (resultados frescos) → `WebFetch` de las
  fuentes primarias (docs oficiales > blog del autor > artículo de terceros).
- Páginas JS-pesadas que WebFetch no lee → skill `/scrape`.
- Pregunta GRANDE de arquitectura/mercado → skill `/deep-research` (fan-out + verificación).
- SIEMPRE capturar fecha de publicación de cada fuente — un hallazgo sin fecha
  no entra al brief (P5: dato sin fecha miente tarde o temprano).

### YouTube (capacidad YA validada — youtube-study-playbook.md)
- `yt-dlp --write-auto-subs` → transcript (esquiva timedtext IP-bloqueado) +
  `ffmpeg` frames → contact-sheet leído como imagen (FAZM "ve" el video).
- Crudos SIEMPRE locales en `~/yt` — JAMÁS commiteados (copyright · ley vigente).
  Al repo/cerebro solo va la SÍNTESIS.
- Cuándo video > texto: técnica visual/motion (un Candillon mostrando el gesto),
  walkthroughs de herramienta, talks de conferencia sin transcript publicado.

### TikTok / Reels / Shorts (extensión del mismo pipeline)
- `yt-dlp` baja TikTok/IG-Reels/Shorts con la MISMA invocación (soporta esas URLs).
- Diferencia práctica: subtítulos frecuentemente AUSENTES → el transcript falla →
  ir directo a frames (clip corto: `fps=2,tile=3x3` basta) + lectura visual del
  contact-sheet; el texto en pantalla (captions quemados) se lee de los frames.
- Valor real de TikTok: micro-técnicas de UI/motion y tendencias tempranas (lo que
  va a estar en dribbble en 3 meses está en TikTok hoy). Ruido alto → exigir que el
  hallazgo se VERIFIQUE en una segunda fuente antes de entrar al brief.

## El dispatch (cuando ≥1 trigger aplica)

1 agente `general-purpose` **(model: sonnet · research con juicio — no necesita opus)**,
prompt con AUTONOMIA_BLOCK + los triggers activos + el componente/plan:

```
Sos el investigador INTEL de ATLAS. Triggers activos: [lista]. Tarea: [COMPONENTE/plan].
Investigá SOLO los focos de los triggers (no exploración libre). Por cada hallazgo:
fuente + FECHA de publicación + por qué importa para ESTA tarea.

OUTPUT (máx 250 palabras · formato exacto):
# INTEL · [componente] · [fecha hoy]
## HALLAZGOS (cada uno: qué · fuente · fecha fuente)
## APLICACIÓN DIRECTA (qué cambia en la implementación por esto)
## RIESGOS DE CADUCIDAD (qué de esto vence pronto y cuándo re-verificar)
## REUTILIZABLE: sí/no — ¿es un patrón que sirve más allá de esta tarea?
Cero hallazgos genéricos ("usar buenas prácticas"). Si un foco no arroja nada
nuevo vs el criterio interno → decirlo explícito ("sin novedad vs P1-B4").
```

## Cache con TTL (no re-investigar lo fresco)

- Brief se guarda en `$ATLAS_DIR/intel/<tema-slug>.md` con frontmatter:
  `tema · fecha: 2026-06-12 · ttl_dias: 30 · trigger: dependencia-nueva`.
- ANTES de dispatchar: si existe brief del mismo tema con `hoy - fecha < ttl_dias`
  → REUSAR (cero dispatch, cero costo). Vencido → re-investigar y sobreescribir.
- El brief (fresco o cacheado) se INYECTA al prompt del implementador/diseñador
  junto al pilar fable5 que corresponda — la señal fresca y el criterio estable
  viajan juntos.

## Conexión al cerebro (intel → grow)

- Brief con `REUTILIZABLE: sí` → es candidato a conocimiento PERMANENTE: el ciclo
  `/atlas grow` lo cosecha (G0 fuente 5) y el destilador decide su destino
  (playbook/criterio) con las reglas de siempre (dedupe · anti-bloat · OK Ale).
- Así el loop completo queda: el mundo cambia → intel lo detecta al implementar →
  lo volátil se cachea con TTL → lo permanente se consolida al cerebro → el
  criterio crece. /atlas aprende del mundo SIN depender de que nadie se lo cuente.

## Reglas absolutas

- El gate corre SIEMPRE; el dispatch solo con trigger. Jamás >1 dispatch de intel
  por tarea.
- Investigación falló o sin red → continuar con criterio interno + marcar
  `INTEL: NO_DISPONIBLE` en el reporte (nunca bloquear el flujo por intel).
- Toda fuente con fecha. Hallazgo de TikTok/foro → verificar en 2ª fuente.
- Crudos de video locales, jamás al repo (copyright).
- El brief NO es spec: el master y las leyes mandan — intel INFORMA decisiones,
  no las toma (un hallazgo no autoriza a desviarse del master · #0h).
