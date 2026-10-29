# The animation and video toolkit

Which tool to reach for, and why. Claude reads this when a video needs motion,
encoding, transcription or cleanup, and picks the smallest tool that does the job.

**Checked 29 October 2026.** Versions, licences and prices change. Anything
marked **[unverified]** could not be confirmed on the day. Re-check a licence
before you use a tool for a paying client.

## How this repo already fits together

| Folder | What it uses |
|---|---|
| `engine/` | Remotion (React) for the `OneWord` and `Cards` formats. Python scripts call ffmpeg and Whisper |
| `motion-studio/node/` | Plain HTML/canvas films, captured frame by frame with Playwright, encoded by ffmpeg |
| `motion-studio/browser/` | The same idea with no install: draws in the browser, encodes MP4 with WebCodecs and a muxer |
| `recipes/yap-audio.md` | DeepFilterNet speech cleanup, then ffmpeg EQ, compression and loudness |
| `.claude/skills/reference-video/` | yt-dlp to fetch a video you want to study |

**Default choice:** stay inside what the repo already uses. Add a new library
only when the job really needs it.

---

## Video frameworks (code in, MP4 out)

### Remotion
- **Best at:** videos written in React. Templated or data-driven videos,
  word-synced text, many variants from one config.
- **Pick it when:** the job fits `engine/` (OneWord, Cards) or needs React
  components, props per variant, or batch renders.
- **Licence and cost:** source-available, **not** open source.
  - Free for individuals, non-profits, people evaluating it, and **for-profit
    companies of up to 3 people**.
  - A company of 4 or more needs a Company License. "Creators" (people making
    videos by hand) $25 per seat per month. "Automators" (scripted or batch
    renders) $0.01 per render, $100/month minimum. Enterprise from $500/month.
  - **For students:** making videos for your employer, if it has 4+ staff, needs
    that licence. Your own personal or freelance-solo work does not.
- **In this repo:** `engine/` is a Remotion project. `npx remotion studio` to preview, `./build.sh` to render.
- **Status:** very active (v4.0.539, 26 Oct 2026).
- **Link:** https://www.remotion.dev · licence: https://www.remotion.pro/license

### HyperFrames (HeyGen)
- **Best at:** an AI agent writing plain HTML, CSS and animation that renders to
  MP4 the same way every time. Headless Chrome plus ffmpeg, built for agents.
- **Pick it when:** you want the HTML-to-video approach of `motion-studio/`
  with a maintained framework behind it, or you need a free alternative to
  Remotion at a company of 4+.
- **Licence and cost:** Apache-2.0. Free, no render fees, no commercial limits.
- **In this repo:** not installed. Same idea as `motion-studio/node/`. Agent
  skills install with `npx skills add heygen-com/hyperframes`.
- **Status:** very active (v0.8.x, releases most days). Still pre-1.0, so expect changes.
- **Link:** https://github.com/heygen-com/hyperframes

### Motion Canvas
- **Best at:** explainer and diagram animations synced to a voiceover, written in TypeScript with a live editor.
- **Pick it when:** a clean, diagram-style explainer is the whole video.
- **Licence and cost:** MIT, free.
- **In this repo:** not used.
- **Status:** slowing down. Last npm release v3.17.2 (Dec 2024); some repo activity in 2026.
- **Link:** https://motioncanvas.io

### Theatre.js
- **Best at:** editing keyframes on a visual timeline, especially for Three.js scenes.
- **Pick it when:** rarely. Only if someone wants to scrub a 3D scene by hand.
- **Licence and cost:** core Apache-2.0, Studio editor AGPL-3.0.
- **Status:** **dormant in public.** Last push Aug 2024, last release May 2024.
  The README says work moved to a private repo. Do not start new work on it.
- **Link:** https://github.com/theatre-js/theatre

---

## Animation libraries (move things on a web page)

All of these run inside `motion-studio/` or a Remotion component. In render
mode they must be driven by time, not by the clock (see "Render contract" below).

### GSAP
- **Best at:** precise timelines with fine-grained easing control. Text splitting (SplitText) and shape morphing (MorphSVG).
- **Pick it when:** a motion graphic has many parts that must line up exactly.
- **Licence and cost:** free, including every plugin, under GSAP's own
  "Standard No-Charge" licence. Owned by Webflow. **Not open source.** You may
  not use it to build a visual no-code animation tool that competes with
  Webflow. Normal videos and sites are fine, and code AI writes with it is allowed.
- **In this repo:** not installed. Use `timeline.pause()` and `timeline.seek(t)` so the render controls time.
- **Status:** active (v3.15, Apr 2026).
- **Link:** https://gsap.com · licence: https://gsap.com/standard-license

### anime.js
- **Best at:** small, general animation with a light footprint.
- **Pick it when:** GSAP is more than you need.
- **Licence and cost:** MIT, free.
- **Status:** active, v4 (v4.5, Jun 2026).
- **Link:** https://animejs.com

### CSS animations and the Web Animations API
- **Best at:** simple moves with no library at all.
- **Pick it when:** the animation is a few fades, slides or scales.
- **Licence and cost:** built into every browser, free.
- **In this repo:** fine for the browser preview. **In render mode, do not let CSS
  run on its own clock.** Use `element.getAnimations()` and set `currentTime`
  per frame, or compute styles from `t` yourself.
- **Status:** supported in all major browsers [support not re-checked today].
- **Link:** https://developer.mozilla.org/docs/Web/API/Web_Animations_API

### Lottie, dotLottie and LottieFiles
- **Best at:** dropping in vector animations a designer made in After Effects (icons, ticks, loaders, small characters).
- **Pick it when:** a finished animation already exists as a `.json` or `.lottie` file.
- **Licence and cost:** players are MIT and free (`lottie-web`,
  `@lottiefiles/dotlottie-web`). LottieFiles (the marketplace and editor):
  Individual $19.99/user/month, Team $24.99, billed yearly.
  Whether a free plan still exists is **[unverified]**. Check the licence on each
  animation you download.
- **In this repo:** not installed. Drive it by frame (`goToAndStop(frame, true)`), not by playback.
- **Status:** dotlottie-web active (Oct 2026). lottie-web slower (last release May 2025).
- **Link:** https://lottiefiles.com · https://github.com/LottieFiles/dotlottie-web

### Rive
- **Best at:** interactive animations with states (a button that reacts, a character that blinks).
- **Pick it when:** the same asset must also live in an app or site. For a flat video it is usually overkill.
- **Licence and cost:** runtimes MIT, no royalties. Editor: Free $0 (adds a
  Rive splash and limits imported assets to 10 MB), Cadet $9, Voyager $32, Enterprise $120 per seat per month.
- **Status:** active (Oct 2026).
- **Link:** https://rive.app

---

## 3D and creative coding

### Three.js and React Three Fiber
- **Best at:** 3D in the browser: product turntables, floating objects, depth.
- **Pick it when:** the idea needs real 3D. Use React Three Fiber inside a
  Remotion component (`@remotion/three`), or plain Three.js inside `motion-studio/`.
- **Licence and cost:** both MIT, free.
- **Gotcha:** 3D looks generic fast (shiny spheres, floating cubes). Give it a
  real object and a reason. See `design-rules.md`.
- **Status:** Three.js r186 (Sep 2026); React Three Fiber v9.8 (Oct 2026). Both very active.
- **Link:** https://threejs.org · https://github.com/pmndrs/react-three-fiber

### p5.js
- **Best at:** generative visuals and beginner-friendly creative coding.
- **Pick it when:** a texture, pattern or particle field is the point, and you want readable code.
- **Licence and cost:** LGPL-2.1, free.
- **In this repo:** not installed. Call `noLoop()` and `redraw()` per frame, and seed the randomness (`randomSeed`).
- **Status:** v2.x is current (v2.3.4, Sep 2026). Which version the web editor uses by default is **[unverified]**.
- **Link:** https://p5js.org

---

## Encoding and capture

### WebCodecs + a muxer (browser MP4 export)
- **Best at:** turning canvas frames into an MP4 inside the browser. No install, no server.
- **Pick it when:** the student has nothing installed, or wants a page that exports its own video.
- **Licence and cost:** WebCodecs is a browser standard. Supported in Chrome 94+,
  Firefox 130+, Safari 26+ (older Safari only partly).
- **Muxer:** `mp4-muxer` (MIT) is what `motion-studio/browser/` was written
  around. **It is now deprecated**; its author replaced it with **Mediabunny**
  (MPL-2.0, very active). Remotion already pulls Mediabunny in. New browser
  export code should use Mediabunny.
- **Link:** https://caniuse.com/webcodecs · https://mediabunny.dev · https://github.com/Vanilagy/mp4-muxer

### Playwright frame capture
- **Best at:** opening an HTML film in headless Chromium, seeking to each frame, and taking a screenshot. Also screen recordings of real websites.
- **Pick it when:** you use `motion-studio/node/` (it already does this), or you need a clean recording of a live web page.
- **Licence and cost:** Apache-2.0, free.
- **In this repo:** `motion-studio/node/render.mjs` and `stills.mjs`. `npm install` in that folder brings Playwright, Chromium and ffmpeg.
- **Status:** very active (v1.64, Oct 2026).
- **Link:** https://playwright.dev

### The render contract (applies to every code-drawn film here)
From `motion-studio/node/CLAUDE.md`:
- Every film is a pure function of time. `window.seek(t)` paints frame `t`.
- No CSS transitions on their own clock, no `setTimeout`, no `requestAnimationFrame` in render mode, no state carried between frames.
- Seeded noise only (mulberry32). Never `Math.random`.
- Encode H.264, `yuv420p`, CRF 16.

Break this and frames come out in the wrong order, jittery, or different on each render.

---

## Audio, speech and fetching

### Whisper (speech to text)
- **Best at:** word-by-word timings and transcripts for captions and cuts.
- **Licence and cost:** MIT, free, runs locally.
- **In this repo:** `openai-whisper` in `engine/requirements.txt`, used by
  `scripts/timings.py`. First run downloads a model (about 500 MB for `small`).
- **Faster options:** `whisper.cpp` (MIT, very fast on Apple Silicon) and
  `faster-whisper` (MIT, Python).
- **Gotchas:** it mishears names ("clod" for Claude, "codecs" for Codex). Spell
  captions from the script, not from Whisper. It invents words over music-only stretches.
- **Link:** https://github.com/openai/whisper · https://github.com/ggml-org/whisper.cpp · https://github.com/SYSTRAN/faster-whisper

### DeepFilterNet (noise removal)
- **Best at:** cleaning room noise and hiss from a voice recording, locally.
- **Licence and cost:** MIT or Apache-2.0, free.
- **In this repo:** step 1 of `recipes/yap-audio.md`, in its own `.venv-df/`. The CLI writes its file and then hangs; stop it once the file stops growing.
- **Status:** **effectively unmaintained** (last release Aug 2023). It still works with the pinned versions in the recipe. Do not upgrade its dependencies casually.
- **Link:** https://github.com/Rikorose/DeepFilterNet

### yt-dlp (download a reference video)
- **Best at:** fetching video or audio from YouTube, Instagram, TikTok and thousands of other sites.
- **Licence and cost:** Unlicense (public domain), free.
- **In this repo:** the reference-video skill uses it to study videos you like.
- **Gotcha:** since November 2025, YouTube downloads need a JavaScript runtime
  installed (Deno recommended; Node also works). Update often (`yt-dlp -U`); sites change weekly.
- **Rules:** download only to study. Never re-upload someone else's video or put
  its footage in yours without rights. Some sites' terms forbid downloading at all.
- **Link:** https://github.com/yt-dlp/yt-dlp

### ffmpeg (the workhorse)
- **Best at:** cutting, joining, resizing, encoding, mixing and measuring any audio or video.
- **Licence and cost:** free. LGPL by default; builds with x264 or x265 become GPL
  [licence detail from general knowledge, not re-checked today]. This does not
  limit the videos you make.
- **In this repo:** everywhere. Remotion ships its own copy; `motion-studio/node`
  installs one; Homebrew (`brew install ffmpeg`) gives the full version.
- **Status:** latest stable 9.0.2 (Sep 2026).
- **Link:** https://ffmpeg.org

---

## ffmpeg: ten recipes

Copy, change the file names, run. Each one re-encodes to H.264 so the output
plays everywhere. `-crf 18` is high quality; raise it for smaller files.

**1. Trim a clip (frame-accurate)**
```bash
ffmpeg -ss 00:00:05.0 -i in.mp4 -t 10 -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k trimmed.mp4
```
Starts at 5 s, keeps 10 s. `-t` after `-i` bounds the output (repo rule).

**2. Join clips with hard cuts**
Use the concat *filter*, not stream copy. Stream-copy joins drifted audio a few
frames per join in this repo (`parts/70`). This also makes every clip the same size and frame rate:
```bash
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -filter_complex "
[0:v]scale=1080:1920,setsar=1,fps=30[v0];
[1:v]scale=1080:1920,setsar=1,fps=30[v1];
[2:v]scale=1080:1920,setsar=1,fps=30[v2];
[v0][0:a][v1][1:a][v2][2:a]concat=n=3:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k joined.mp4
```
Every input needs an audio track. Add silence to one that has none (`-f lavfi -i anullsrc=r=48000:cl=stereo` plus `-shortest`).

**3. Make a 16:9 clip vertical (9:16)**
Crop the centre (loses the sides):
```bash
ffmpeg -i wide.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,setsar=1" -c:v libx264 -crf 18 -c:a copy vertical.mp4
```
Move the crop with `crop=ih*9/16:ih:X:0`, where X is the left edge in pixels.
Or keep the whole frame and pad top and bottom:
```bash
ffmpeg -i wide.mp4 -vf "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x111111,setsar=1" -c:v libx264 -crf 18 -c:a copy vertical-pad.mp4
```

**4. Burn in subtitles from an .srt file**
```bash
ffmpeg -i in.mp4 -vf "subtitles=captions.srt:force_style='FontName=Inter,FontSize=14,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1.2,Shadow=0,Alignment=2,MarginV=60'" -c:v libx264 -crf 18 -c:a copy captioned.mp4
```
`FontSize` and `MarginV` are measured against a 288-pixel-tall canvas, not your
video. 14 is about 93 px on 1920. MarginV 60 lifts the text about 400 px above
the bottom, clear of Instagram's caption area. Needs an ffmpeg built with
libass (`ffmpeg -filters | grep subtitles`). For word-by-word captions use
`engine/scripts/overlay.py` instead.

**5. Normalise loudness to -14 LUFS**
```bash
ffmpeg -i in.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v copy -c:a aac -b:a 192k -ar 48000 loud.mp4
```
Then measure the result:
```bash
ffmpeg -i loud.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12
```
One pass gets close. A take with clipped peaks may not reach -14 this way; the
repo's method is gain plus a limiter (`recipes/yap-audio.md`).

**6. Speed up 1.05x and keep the pitch**
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=PTS/1.05[v];[0:a]atempo=1.05[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -c:a aac -b:a 192k faster.mp4
```
`atempo` keeps the pitch. The Yap default is 1.07x; 1.05x when it feels rushed.

**7. Contact sheet (one image, many frames)**
```bash
ffmpeg -i in.mp4 -vf "fps=1,scale=216:384,tile=8x3" -frames:v 1 sheet.png
```
One frame a second, 24 frames on one sheet. Claude can open the PNG and look.
Change `fps=1` to `fps=2` for a closer look. Add `-ss` before `-i` to start later.

**8. GIF that does not look muddy**
```bash
ffmpeg -i in.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" -loop 0 out.gif
```
Keep it short (under 6 s) or the file gets huge.

**9. Add a music bed that ducks under the voice**
```bash
ffmpeg -i voice.mp4 -stream_loop -1 -i bed.wav -filter_complex "
[0:a]asplit=2[vo][key];
[1:a]volume=0.25[m];
[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];
[vo][duck]amix=inputs=2:duration=first:normalize=0[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k mixed.mp4
```
The music dips whenever the voice speaks. Then run recipe 5 on the result. Only
use music you own: `engine/scripts/bed.py` composes an original bed.

**10. Find the cuts (scene detection)**
```bash
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -fps_mode vfr -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
```
Prints the time of every hard cut. Lower `0.3` to catch softer cuts. Save the frames too:
```bash
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',scale=360:-2" -fps_mode vfr cut_%03d.jpg
```
Useful for counting a reference video's cut rate (see `references/videos/`).

Measure anything with `ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact file.mp4`.

---

## Decision table

| I want... | Use |
|---|---|
| One word at a time, synced to a voiceover | Remotion, `engine/` `OneWord` |
| Captions over my graphics with hard cuts | Remotion, `engine/` `Cards` |
| Hook text or word captions on my own footage | `engine/scripts/overlay.py` (ffmpeg) |
| Trim, join, crop to vertical, speed up | ffmpeg, recipes 1, 2, 3, 6 (or `engine/scripts/clip.py`) |
| An animated logo, stat count-up or self-drawing chart | `motion-studio/node/` (HTML + canvas, Playwright, ffmpeg) |
| The same, with nothing installed | `motion-studio/browser/` (WebCodecs + muxer) |
| Many parts on one tight timeline | GSAP, seeked by the render |
| A designer's After Effects animation | Lottie (`dotlottie-web`), driven by frame |
| A real 3D object or depth | Three.js, or React Three Fiber inside Remotion |
| Generative texture or particles | p5.js or plain canvas, seeded |
| A diagram explainer, code-first, with a live editor | Motion Canvas (or HyperFrames) |
| HTML-to-video at a company of 4+ without a Remotion licence | HyperFrames (Apache-2.0) or `motion-studio/` |
| Word timings or a transcript | Whisper (`engine/scripts/timings.py`) |
| Remove room noise from my voice | DeepFilterNet (`recipes/yap-audio.md`) |
| Instagram loudness | ffmpeg, recipe 5 (-14 LUFS, true peak -1.5 dBTP) |
| Music under the voice | `engine/scripts/bed.py`, then ffmpeg recipe 9 |
| Study a video I like | yt-dlp, then recipes 7 and 10, then `.claude/skills/reference-video/` |
| A recording of a live website | Playwright |
| A GIF for a doc or Slack | ffmpeg recipe 8 |
| Generated footage, voices or stills | not here: `video-generation.md` |

## Not verified on 29 October 2026
- Whether LottieFiles still has a free plan.
- Which p5.js version the web editor uses by default.
- ffmpeg's exact licence split and Web Animations API support (from general knowledge).
- Whether Theatre.js has private progress toward 1.0.
- The ffmpeg recipes are standard usage but were not run on this machine today. Check outputs with recipe 7 and `ffprobe`.
