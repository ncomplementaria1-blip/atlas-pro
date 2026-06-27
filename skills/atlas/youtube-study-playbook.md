# YouTube Study Playbook · cómo "ver" videos sin poder reproducirlos

> Capacidad permanente del ADN (binding · 2026-06-01 · pedido de Ale). ATLAS no puede reproducir video
> en vivo, pero SÍ puede estudiar un video a fondo: transcript (lo que dice) + frames (lo que muestra).
> Validado estudiando los videos de William Candillon (RN Transitions / Liquid Glass) — funcionó.

---

## Regla de ADN (autonomía + aviso)

- ATLAS **estudia videos de forma autónoma** cuando una tarea de research/diseño/técnica lo amerita
  (vanguardia, técnicas, referentes, "aprendé de los que saben"). NO pide permiso.
- **Solo AVISA** antes: "voy a estudiar estos N videos con el método" + la lista. Luego lo hace y reporta.
- Crudos (subtítulos + video) quedan **locales** en `~/yt/` (o `/tmp`). **NUNCA se commitean** (copyright).
  Al repo va solo la **SÍNTESIS** (transformativa · resumen de técnicas, sustancialmente más corto y distinto).
- Cero credencial nueva, cero DB → no toca los 2 STOP reales. Es autónomo.

---

## Pre-requisitos (ya instalados en la máquina de Ale)
- `yt-dlp` (`/opt/homebrew/bin/yt-dlp`) — baja subtítulos y video.
- `ffmpeg` (8.x) — extrae frames / contact-sheets.
- `python3` — limpieza del VTT.
- Playwright MCP — para descubrir videos (search) y extraer descripciones/chapters.

---

## Flujo (4 pasos)

### 1. DESCUBRIR (qué videos estudiar)
Playwright → YouTube search → extraer títulos/canales/IDs:
```js
// browser_navigate a https://www.youtube.com/results?search_query=TERMINOS+CON+ESPACIOS+como+plus
// luego browser_evaluate:
() => { const o=[]; document.querySelectorAll('ytd-video-renderer').forEach(v=>{
  const t=v.querySelector('#video-title'), ch=v.querySelector('ytd-channel-name a,#channel-name a'), m=v.querySelector('#metadata-line');
  if(t&&t.textContent.trim()) o.push({title:t.textContent.trim().slice(0,100),channel:ch?ch.textContent.trim():'',meta:m?m.textContent.replace(/\s+/g,' ').trim().slice(0,36):'',href:(t.href||'').replace('https://www.youtube.com','').split('&pp')[0]});
});
return o.slice(0,12); }
```
Descripción + chapters (revelan técnica + repos): browser_navigate al watch, luego
`() => { const r=window.ytInitialPlayerResponse||{}; return {title:r?.videoDetails?.title, views:r?.videoDetails?.viewCount, descr:(r?.videoDetails?.shortDescription||'').slice(0,900)}; }`

### 2. TRANSCRIPT (lo que dice)
```bash
mkdir -p ~/yt && cd ~/yt
yt-dlp --write-auto-subs --sub-langs "en.*" --skip-download --convert-subs vtt -o "%(id)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```
Limpiar el VTT (los auto-subs vienen con timestamps + líneas rolling duplicadas):
```python
import re
raw=open('VIDEO_ID.en-orig.vtt',encoding='utf-8',errors='ignore').read()  # o .en.vtt
lines=[]
for ln in raw.splitlines():
    if '-->' in ln or not ln.strip() or ln.startswith(('WEBVTT','Kind:','Language:')): continue
    ln=re.sub(r'<[^>]+>','',ln); ln=re.sub(r'\s+',' ',ln).strip()
    if ln: lines.append(ln)
out=[]
for ln in lines:                      # dedupe consecutivo
    if not out or out[-1]!=ln: out.append(ln)
print(' '.join(out))
```
NOTA: subtítulos `kind:asr` = auto-generados → errores fonéticos ("skia"->"skier", "SDF" ok, nombres mal).
Leer con criterio. Si el video tiene subs humanos (sin `-orig`), preferirlos.

### 3. FRAMES (lo que muestra)
```bash
cd ~/yt
yt-dlp -f "bv*[height<=540]/b[height<=540]" -o "vid.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
V=$(ls vid.* | head -1)
# contact-sheet: 1 frame cada N seg en una ventana [ss, ss+t], grilla AxB, leíble como UNA imagen
ffmpeg -y -ss 8 -t 120 -i "$V" -vf "fps=1/8,scale=320:-1,tile=4x4,scale=1200:-1" -frames:v 1 ~/yt/sheet.png
```
Luego `Read ~/yt/sheet.png`. Targetear la VENTANA del demo/chapters (no el intro hablado).
Para detalle: menos frames más grandes (`tile=3x3`, `scale=380:-1`) o un frame full a un timestamp puntual:
`ffmpeg -y -ss 35.5 -i "$V" -frames:v 1 ~/yt/f.png`.

### 4. SINTETIZAR
Cruzar transcript + frames → técnicas concretas (arquitectura, primitivas, librerías, gotchas).
Guardar SOLO la síntesis en `docs/research/worldclass/` (+ playbook si es reutilizable). Borrar/dejar
local los crudos. Reportar a Ale qué se aprendió, no el dump.

---

## Gotchas
- API `timedtext` directa (fetch del baseUrl de captionTracks) suele volver VACÍA (trae `ip=0.0.0.0`,
  IP-bound). NO usarla. Usar `yt-dlp --write-auto-subs` (esquiva el bloqueo).
- yt-dlp puede warnear "impersonation no disponible" — igual funciona; si falla, `brew install yt-dlp`
  trae deps de impersonation.
- Algunos videos no tienen subtítulos (ni auto) → solo quedan frames + descripción.
- Contact-sheet: el `tile` toma los primeros AxB frames de la ventana; ajustar `fps`/`ss`/`t` para encuadrar.
- Tamaño: bajar a `height<=540` para frames es suficiente y rápido (~20-30MB). No bajar 1080 sin razón.
- Privacidad/legal: estudio personal, no redistribución. No commitear crudos. No reproducir transcript
  verbatim extenso en outputs (citar ideas, no copiar bloques largos).

---

## Cuándo usarlo
- "estudiá la vanguardia / aprendé de los que saben / mirá este video / sacá las técnicas de YouTube".
- Research de técnicas (motion, shaders, RN, diseño) donde los referentes publican en video.
- Antes de improvisar un approach nuevo: ver cómo lo hace el referente real primero.
