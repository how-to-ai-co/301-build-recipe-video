# Motion studio rules

## Setup
- `npm install` once in this folder. It brings Playwright, Chromium and ffmpeg.
- New film: copy starter.html to index.html and replace the scenes.
- examples/showreel.html is a finished 15-second reel to learn from.

## Render contract
- Every film is a pure function of time: `window.seek(t)` paints frame t on `<canvas id="c">`.
- No CSS transitions, no setTimeout, no requestAnimationFrame in render mode,
  no state carried between frames. Seeded noise only (mulberry32), never Math.random.
- Contact sheet: `node stills.mjs` → out/sheet.png. Use `--dur` to match the film.
- Draft: `node render.mjs --fps 30 --sub 1`. Final: `node render.mjs` (60fps, motion blur).
  Both write out/final.mp4, H.264 yuv420p, CRF 16. Other sizes: `--w 1920 --h 1080`.

## Look
- Banned defaults: centered title on gradient, everything fading in,
  corner labels and frame borders, glow on UI chrome, generic particle bursts.
- One display face, one UI face. One accent color unless the brief says otherwise.
- Every 2 to 4 seconds something new must happen on screen.
- Real assets only. Never invent the user's product, screens or numbers.
- Nothing important smaller than 48px at 1080 wide.

## Sound
- Score and SFX are synthesized in code (`node audio.mjs` → out/score.wav) unless a track is supplied.
- Put hits on the beat grid (BEAT in index.html) and on the cuts. render.mjs mixes out/score.wav in.

## Loop before you show me anything
1. Run stills.mjs and LOOK at out/sheet.png.
2. Score it 1-10 on: hook in first 2s, readability at phone size,
   motion quality, variety, brand accuracy, sound sync.
3. Fix the 3 worst problems. Repeat until every score is 8+.
4. Only then do the full render.
