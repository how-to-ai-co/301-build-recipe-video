# Build: motion graphics studio with Node

Build the user a motion graphic for their business, made entirely in code. A headless browser draws every frame and ffmpeg joins them into an MP4, so you can render and look at your own frames without the user's help.

The kit is in `motion-studio/node/` of this repo (https://github.com/how-to-ai-co/301-build-recipe-video). Work in that folder. Everything below is relative to it.

Talk to the user plainly and briefly. Assume they have never done this before.

## Step 0: Check and install

Run `node -v`. If Node is missing or older than 18, stop. Tell the user to use `motion-studio/build-motion-no-install.md` instead. Do not install Node.

If this repo isn't on their computer yet, clone it: `git clone https://github.com/how-to-ai-co/301-build-recipe-video`. If they have no git, have them download the ZIP from that page and unzip it.

Otherwise, start this in the background and go straight to the interview:

```
cd motion-studio/node && npm install
```

That one command brings Playwright, Chromium and ffmpeg (`ffmpeg-static`). Nothing else to install. The scripts use the user's own ffmpeg if it can write H.264, otherwise the bundled one.

## Step 1: Interview the user

Ask these one at a time. Offer the examples, accept short answers, use the default if they are unsure. Ask nothing else.

1. What is your business, and what is its website?
2. What do you want to make? For example: an animated logo intro, a social post that moves (a stat, a quote, a before and after), a chart that draws itself, a short "how it works", a looping banner, or a short ad.
3. Where will it go? Story or TikTok: 9:16 (1080x1920). Feed post: 4:5 (1080x1350). Website or YouTube: 16:9 (1920x1080). Default: 9:16.
4. What should it say? The one message, number or few words that matter. Default: suggest one from their website.
5. Is there a look you like? A screenshot of anything, or a named style. Default: their own brand.

Then repeat it back in three lines (what, where, what it says) and start building.

## Step 2: Gather their brand

Open their website with Playwright. Save a screenshot, the logo and any product images into `assets/`. Note the main colors (hex) and fonts. Tell the user in one line what you found.

Never invent their product, their screens or their numbers. Crop and animate the real thing. If a number is needed and the site does not have one, ask.

## Step 3: Read the house rules

`CLAUDE.md` in this folder holds the rules: the render contract, banned looks, sound and the critique loop. Follow them. Also: nothing important smaller than 48px at 1080 wide, and the first second is already moving.

## Step 4: Build

- Copy `starter.html` to `index.html` and replace the scenes. Keep `window.seek(t)`, the `spring` function and the seeded `rng`. A value with several targets is the sum of one spring per change (see `track` in `examples/showreel.html`).
- Set the canvas `width`/`height` and `W`/`H` to the chosen size, and `DUR` to the length. Default 10 seconds.
- Do not rewrite `render.mjs`, `stills.mjs` or `ffmpeg.mjs`. Pass flags instead: `--dur 10`, and `--w 1920 --h 1080` (or `--w 1080 --h 1350`) for other sizes.
- `examples/showreel.html` is a finished 15-second reel. Read it for technique, not for its look.

## Step 5: Critique your own work

Run `node stills.mjs --dur <length>` and open `out/sheet.png` yourself. Be a harsh motion director, not a proud author.

Score 1 to 10: hook in the first second, readability on a phone, motion quality, variety, composition, brand accuracy. Show the user the scores in one line and the 3 biggest problems with their times. Fix them, run stills.mjs again, and repeat until every score is 8 or more or the user says it is good enough.

## Step 6: Render

Draft first: `node render.mjs --dur <length> --fps 30 --sub 1` (seconds). Tell the user where `out/final.mp4` is and open it for them.

If they want the polished version: `node render.mjs --dur <length>` (60fps with motion blur, a few minutes). For sound, edit the hit times in `audio.mjs` to match the film, run `node audio.mjs`, then render again; render.mjs mixes `out/score.wav` in.

Then tell them, in two lines, that to make another they just say what they want next in this folder, and that sound and motion blur are the upgrades if they haven't used them.
