# 301 Build Recipe: Video

Materials for the **AI 301 live workshop: make a video for your business with Claude**. Students paste one recipe into Claude Code. Claude clones this repo, sets up the video engine, studies a reference video if they have one, plans the edit with them, builds a draft it has already checked, saves their notes as rules, and exports the final.

Handout and recipe: https://301-build-recipe-video.vercel.app

## Use it yourself

1. Install the Claude desktop app (paid Claude plan) and Node.js 18+.
2. Clone this repo into its own folder:

   ```bash
   git clone https://github.com/how-to-ai-co/301-build-recipe-video.git ~/Documents/video-engine
   ```

3. In Claude Code, open that folder (Code tab, Local, Select folder) and say hi. `CLAUDE.md` loads on its own and takes it from there.

No API key is needed to edit your own footage, add captions, or make motion graphics. Paid AI generation (voices, footage, lip sync) is optional, and Claude prices every call before it runs.

## What's here

- **`CLAUDE.md`**: the operator guide Claude follows.
- **`engine/`**: Remotion compositions and Python scripts. These handle Whisper word timings, the Yap talking-head edit, zero-gap trims, captions, a film-grain grade, original music beds, loudness levels, delivery checks, and fal and Replicate generation with a dry run.
- **`parts/`**: thirteen deep guides, from keys and accounts to every format, plus a failure log of mistakes already paid for.
- **`recipes/`** and **`styles/`**: the Yap formula and release check, and named looks (Yap Depth, Oren Static Hooks, Editorial Tech).
- **`motion-studio/`**: motion graphics from code, in a Node version and a no-install browser version that exports MP4 from Chrome.
- **`references/`**: design rules, an animation library guide (Remotion, GSAP, Lottie, Motion Canvas and more), an AI video generation guide, and reference-video breakdowns.
- **`.claude/skills/`**: skills that load automatically:
  - **`video-edit` and `refine-video-edit`**: edits that learn from your notes.
  - **`reference-video`**: paste any video link and say "make mine like this".
  - **Yap planning, overlays, timing and covers.**
  - **Captions.**
- **`review-panel/`**: a local page for reviewing drafts with timestamped notes and a waveform trim.
- **`examples/doranalytics/`**: a finished brand book to copy the shape of.
- **`app/`, `content/`, `public/`**: the handout site. `public/build-recipe.md` is the recipe; keep `content/recipe.json` in sync with `npm run sync`.

## Handout site

`npm ci`, then `npm run dev`. Validate with `npm run check` and `npm run build`.

## Not included

The full cinematic film workflow (scripted scenes with actors) is built on licensed third-party material, so it isn't in this public repo. `parts/60-format-kling-dialogue.md` keeps the Kling setup and the record of one finished dialogue film.
