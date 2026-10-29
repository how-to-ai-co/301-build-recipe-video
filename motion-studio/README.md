# Motion studio

Moving graphics made in code: an animated logo, a stat that counts up, a chart that draws itself, a short explainer, a looping banner, a small ad.

Claude can't make video. It writes a web page with one function, `window.seek(t)`, that draws any moment of the film. Something else then steps through every frame and turns them into an MP4. Same `t` in, same picture out, every time.

Based on Movez's thread "How to build motion design studio with Opus 5.5".

## Pick a version

Ask Claude: **"Do I have Node installed?"** (it runs `node -v`).

| | Node version (`node/`) | Claude-only version (`browser/`) |
|---|---|---|
| Who | You have Node 18 or newer | Everyone else |
| Needs | Node. One `npm install` brings Playwright, Chromium and ffmpeg | Claude Code and Chrome (or Edge) |
| How it renders | `render.mjs`: a hidden browser screenshots every frame, ffmpeg joins them | `motion.html`: buttons in Chrome export the contact sheet and the MP4 |
| Critique loop | Claude makes and reads the contact sheet itself | You export the contact sheet and drag it back to Claude |
| Extras | Motion blur, synthesized sound (`audio.mjs`) | Synthesized sound (Web Audio), mixed into the MP4 |

Don't install Node during class. If you don't have it, use the Claude-only version.

## Start

Open this repo in Claude Code and paste one line:

- Node: `Read motion-studio/build-motion-node.md and follow it`
- Claude-only: `Read motion-studio/build-motion-no-install.md and follow it`

Claude asks you five questions (your business, what to make, where it goes, what it says, a look you like), gathers your brand from your website, builds it, runs a critique round and exports.

## The critique loop

1. **Contact sheet.** One image with a frame from every beat of the film.
   Node: Claude runs `node stills.mjs` and looks at `out/sheet.png` itself.
   Claude-only: press **Contact sheet** in Chrome and drag `contact-sheet.png` into Claude Code.
2. **Critique.** Claude scores it 1 to 10: hook in the first second, readability on a phone, motion, variety, composition, brand accuracy. It names the 3 worst problems and the times they happen.
3. **Fix.** Claude edits the file. Refresh Chrome (Claude-only) and send a new sheet.
4. **Export** once every score is 8 or more, or you're happy.
   Node: `node render.mjs` writes `out/final.mp4`.
   Claude-only: press **Export MP4**. It steps through every frame and saves `motion.mp4`. It is frame-exact, not a screen recording, and takes a few seconds.

## House rules (short version)

- Every frame is a pure function of time. No timers, no CSS animation, no state kept between frames, no `Math.random` (seeded noise only).
- Motion uses springs written as formulas, so any frame can be drawn on its own.
- Banned looks: centered title on a gradient, everything fading in, corner labels, frame borders, glows, generic particle bursts.
- Your brand colors and one accent. At most two fonts.
- Something new every 2 to 3 seconds. The first second is already moving.
- Nothing important smaller than 48px at 1080 wide.
- Real assets only. Never invent your product, screens or numbers.

The full rules are in `node/CLAUDE.md` and in each build guide.

## What's in here

```
build-motion-node.md        build guide, Node version
build-motion-no-install.md  build guide, Claude-only version
node/
  CLAUDE.md                 house rules Claude follows in this folder
  package.json              npm install → Playwright + Chromium + ffmpeg
  starter.html              template: copy to index.html
  examples/showreel.html    a finished 15-second, 7-shot reel to learn from
  stills.mjs                contact sheet → out/sheet.png
  render.mjs                MP4 → out/final.mp4
  audio.mjs                 synthesized score → out/score.wav (render.mjs mixes it in)
  ffmpeg.mjs                finds ffmpeg (yours, or the one npm installed)
browser/
  motion.html               template: Play, Contact sheet, Export MP4. Claude replaces the SCENE section
```

## Node commands

```
npm install                                             # once, about 30 seconds plus a Chromium download
node stills.mjs                                         # contact sheet of index.html
node render.mjs --fps 30 --sub 1                        # quick draft MP4
node render.mjs                                         # final: 60fps with motion blur (minutes)
node render.mjs --file examples/showreel.html --fps 30 --sub 1   # render the example
```

Flags: `--file`, `--dur` (seconds), `--fps`, `--sub` (motion blur samples, 1 = off), `--w`/`--h` (size). On this repo's test Mac, the 15-second showreel took 28 seconds at `--fps 30 --sub 1` and about 4 minutes at the default 60fps with motion blur.

## Claude-only notes

- Opened straight from disk (double-click `motion.html`). No server needed.
- Export MP4 needs an internet connection once, to load the small MP4 library (`mp4-muxer`) from a CDN.
- Best in Chrome or Edge. In a browser without WebCodecs it falls back to recording one real-time playthrough, which can drop frames.
- Images must be embedded in the file as `data:` URLs. A logo loaded from a file path blocks export when the page is opened from disk; the page says so if it happens.
- The size menu switches between 9:16, 4:5, 1:1 and 16:9. The **Sound** box turns the synthesized sound on or off for Play and Export.
