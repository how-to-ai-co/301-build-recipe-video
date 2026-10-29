# Build: motion graphics studio, no installs

Build the user a motion graphic for their business, made entirely in code. The user has Claude Code and Chrome. Do not install anything: no Node, no Python, no ffmpeg, no packages.

The result is one HTML file that draws the graphic and exports it as an MP4 in Chrome. Start from the tested template `motion-studio/browser/motion.html` in this repo (https://github.com/how-to-ai-co/301-build-recipe-video). If the repo isn't on their computer, fetch just the template: `curl -L -o motion.html https://raw.githubusercontent.com/how-to-ai-co/301-build-recipe-video/main/motion-studio/browser/motion.html`.

Talk to the user plainly and briefly. Assume they have never done this before.

## Step 1: Interview the user

Ask these one at a time. Offer the examples, accept short answers, use the default if they are unsure. Ask nothing else.

1. What is your business, and what is its website?
2. What do you want to make? For example: an animated logo intro, a social post that moves (a stat, a quote, a before and after), a chart that draws itself, a short "how it works", a looping banner, or a short ad.
3. Where will it go? Story or TikTok: 9:16 (1080x1920). Feed post: 4:5 (1080x1350). Website or YouTube: 16:9 (1920x1080). Default: 9:16.
4. What should it say? The one message, number or few words that matter. Default: suggest one from their website.
5. Is there a look you like? A screenshot of anything, or a named style. Default: their own brand.

Then repeat it back in three lines (what, where, what it says) and start building.

## Step 2: Gather their brand

Fetch their website. Find the logo, the main colors (hex) and the fonts. Download the logo into `motion-studio/browser/assets/` with curl. Tell the user in one line what you found.

Never invent their product, their screens or their numbers. If a number is needed and the site does not have one, ask.

**Images must go into the file as data: URLs, never file paths.** Chrome blocks saving a canvas that drew an image from disk, so a file path breaks the export. Embed with `base64 -i assets/logo.png` (Mac) or PowerShell `[Convert]::ToBase64String([IO.File]::ReadAllBytes('assets\logo.png'))` (Windows), and put the result in `IMAGES` as `'data:image/png;base64,...'`. For an SVG logo use `'data:image/svg+xml,' + encodeURIComponent(svgText)`. Keep images small (under about 1 MB).

## Step 3: Build

Copy `motion-studio/browser/motion.html` to `motion-studio/browser/<short-name>.html` (for example `bakery.html`) and work in the copy.

Replace only the part between `SCENE` and `END SCENE`. Leave the toolkit and the player/exporter code alone; they are tested. In the SCENE section set:

- `DUR` (default 10 seconds), `FPS` (30), `SIZE` (the chosen size), `SHEET_FRAMES` (12).
- Colors, fonts, `IMAGES`.
- `draw(t)`: paints the exact frame for time t and nothing else. Use `W`, `H` and `u` (1 at 1080 on the short side) so the layout works in every size from the size menu. Images loaded from `IMAGES` are in `img.<name>`.
- `sound(s)`: hits on the same times as the picture, or an empty body for silence.

Render contract:
- No CSS transitions, no setTimeout, no state carried between frames.
- Motion uses `spring(t, k, d)`, which is closed-form. A value with several targets uses `track(t, [[time, value], ...])`.
- Randomness uses `rng(seed)` (mulberry32). Never Math.random.

Look:
- Banned: centered title on a gradient, everything fading in, corner labels, frame borders, glows, generic particle bursts.
- Their brand colors with one accent. At most two fonts. Prefer system fonts. If you use a web font, check the contact sheet actually shows it.
- Something new happens every 2 to 3 seconds. The first second is already moving.
- Readable on a phone: nothing important smaller than 48px at 1080 wide.

The template already has the three buttons:
- **Play** loops the preview with sound. The slider scrubs.
- **Contact sheet** saves `contact-sheet.png`: 12 frames with their times.
- **Export MP4** steps through every frame with seek(t), encodes with WebCodecs and saves `motion.mp4`, sound included. It needs internet once to load mp4-muxer from the CDN. In a browser without WebCodecs it records one real-time playthrough instead and says so.

Then tell the user: "Open <short-name>.html in Chrome (double-click it or drag it onto Chrome). Press Play. Then press Contact sheet and drag the image back here."

## Step 4: Critique your own work

When the user drags in the contact sheet, look at it properly. Be a harsh motion director, not a proud author.

Score 1 to 10: hook in the first second, readability on a phone, motion quality, variety, composition, brand accuracy. Show the scores in one line. Name the 3 biggest problems with their times. Fix them. Tell the user to refresh Chrome, press Play, and send a new contact sheet.

Repeat until every score is 8 or more, or the user says it is good enough.

## Step 5: Export

Tell the user to press Export MP4 and wait a few seconds for the download (`motion.mp4` in their Downloads folder). If the page shows a red message, ask them to paste it to you. Then tell them, in two lines, that to make another they just say what they want next, and that the same rules apply.
