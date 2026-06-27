# Perf Profiling Playbook — medir 60fps de verdad en gama baja

> Destilado de research 2026-06-01. Consumir cuando un cambio toca shaders/animaciones continuas y
> dice `needs-apk-validation`. Convierte "creo que corre" en DATO. Target: Snapdragon 680 / Adreno 610.

## ⛔ Ley 0: el EMULADOR MIENTE para GPU
El emulador usa la GPU del Mac (Metal) — NO replica Adreno (TBDR, GMEM, UBWC). Un shader a 60fps en
emulador puede caer a 20fps en Snapdragon 680 real. Emulador OK para JS/layout; para GPU/shaders =
SIEMPRE device físico. Medir DESPUÉS de 2-3 min de calentamiento (no en cold start → oculta throttling).

## Criterios de aceptación (NutricomAI / Snapdragon 680)
- **Janky frames < 5%** (en prueba de 30s con la animación activa)
- **P95 frame time < 20ms** (P99 < 50ms)
- **JS FPS > 55** sostenido · **UI FPS > 57**
- **GPU% < 85%** sostenido (deja headroom para thermal)
- **Sin rojo** en Debug GPU Overdraw sobre la zona del shader
- Tras **5 min sostenidos**: score no cae >20% (si cae → thermal throttling → pre-render o degradar)

## Workflow escalado (rápido → serio)
1. **[30s] Visual sanity:** device → Dev Options → "Profile HWUI Rendering > On screen as bars". Línea verde = 16.6ms. Barras que la cruzan = jank. Barra "Swap Buffers" alta = GPU-bound.
2. **[5min] `dumpsys gfxinfo`:**
   ```
   adb shell dumpsys gfxinfo cl.nutricomai.app reset
   # interactuar 30s con el shader activo
   adb shell dumpsys gfxinfo cl.nutricomai.app framestats
   ```
   Leer: Janky frames %, P50/P90/P95/P99. Janky <3% + P95 <20ms = verde.
3. **[10min] Flashlight** (`flashlight.dev` · `curl https://get.flashlight.dev | bash`): FPS + CPU por thread. Si `mqt_js` CPU alto → JS-bound; si UI FPS cae con mqt_js limpio → GPU/Skia-bound.
   ```
   flashlight measure   # abrir la pantalla, 30-60s, Ctrl+C → reporte HTML
   ```
4. **[20min · si hay problema] Perfetto** (`adb shell perfetto ... -o trace.pftrace` → `ui.perfetto.dev`): identificar el thread cuello de botella (RenderThread cruza 16ms = GPU; mqt_js continuo = JS).
5. **[30min · GPU serio] AGI** (Android GPU Inspector, gpuinspector.dev · soporta Adreno A6XX) o **Snapdragon Profiler**: counters `% Shader ALU Capacity Utilized`, `GPU % Utilization`, `Texture Memory Read BW`. ALU>80% = shader pesado; GPU 100% con ALU<50% = texture/memory-bound. Frame Profiler aísla el draw call del shader (ALU instruction count, objetivo <200 para continuo).
   - Requiere APK profileable: `<profileable android:shell="true"/>` en `<application>` del AndroidManifest.

## Hardware Adreno 610 (lo que hay que entender)
- 128 ALUs, 950MHz (→ ~650MHz throttled tras 3 min), LPDDR4X ~25-28GB/s efectivo. **FP16 (mediump) = 2× throughput** vs FP32 → `precision mediump float` + `half`/`half4`.
- **TBDR** (tiles 32×32 en GMEM ~2MB): HSR elimina overdraw OPACO gratis. PERO:
  - ⛔ **framebuffer read / backdrop-blur = +5-8ms GARANTIZADO** (flush GMEM → read LPDDR4X → re-bind). El costo más caro posible. Por eso glass se dosifica, no se stackea.
  - blending/alpha NO se elimina (cada capa transparente se shadea).
  - >GMEM (capas múltiples grandes) → spill a RAM (latencia 10-20×).
- Branching divergente (por-pixel) fragmenta el warp → usar `step()`/`smoothstep()` en vez de `if`.

## Presupuesto de frame (estimar ANTES de buildear)
16.6ms ≈ JS 4ms + layout 2ms + Skia CPU 2ms + **GPU 6ms** + headroom 2.6ms. Esos 6ms son el techo de shaders.
- Costo ≈ `pixels × instrucciones_por_fragment / (128·950M·0.5)`. Un orb 300×300 a 200 instr ≈ 0.3ms. 3 shaders + blending ≈ 1-2ms. + backdrop = +5ms.
- Cada `sin/cos/pow/exp` ≈ 4-8 instr ALU; cada `texture()` ≈ 10-20. fbm custom = caro → FractalNoise builtin.
- **×1.5** el estimado para release throttled.
- Redflags sin medir: backdrop sobre canvas grande · >3 Canvas con shaders simultáneos · shader que cubre >50% pantalla · uniforms que cambian cada frame (GPU 100% → throttle <5min).

## Aislar un shader: A/B con `dumpsys gfxinfo` (con shader vs canvas sólido) → diff en Janky%/P95 = su costo.
