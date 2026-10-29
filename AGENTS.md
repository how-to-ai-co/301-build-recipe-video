# Instructions for coding agents

You are helping a How to AI 301 student make a video for their business. The student is not an engineer. The full recipe is `public/build-recipe.md`. The operator guide for the engine is `CLAUDE.md`; follow it.

Unlike other 301 recipes, the student works **inside this repo**: it is the engine. Clone it once to its own folder (default `~/Documents/video-engine`) and keep using it.

## What is in this repo

| Path | Use it for |
| --- | --- |
| `CLAUDE.md` | The operator guide: greeting, formats, setup stages, quality gates, compliance. Read it first. |
| `engine/` | The working project: Remotion compositions in `src/`, Python scripts in `scripts/` (timings, Yap edit, trims, captions, grade, music bed, delivery checks, paid generation with a dry run first). |
| `parts/` | Deep guides, one per layer: keys, voice and music, each format, fal and Replicate generation, the failure log, naming and delivery, Mad Libs templates. Read on demand. |
| `recipes/` | The Yap talking-head formula, its release check, flash overlays and audio. A worked example from one creator. |
| `styles/` | Named looks the student can ask for: Yap Depth, Oren Static Hooks, Editorial Tech. |
| `motion-studio/` | Motion graphics from code. `node/` renders frames with Playwright and ffmpeg; `browser/motion.html` needs only Chrome. |
| `references/` | Design rules, the animation library guide, the AI video generation guide, and `videos/` for reference-video breakdowns. |
| `review-panel/` | A local web page for reviewing drafts, pinning notes to timestamps and trimming. Optional. |
| `examples/doranalytics/` | A finished brand book to show what a filled-in brand looks like. Never copy its values. |
| `.claude/skills/` | Loaded automatically: `video-edit` and `refine-video-edit` (edits that learn from feedback), `reference-video`, `yap-video-plan`, `visual-hooks-overlays`, `overlay-timing`, `yap-cover-image`, `caption`. |
| `app/`, `content/`, `public/` | The workshop handout website. Not part of the student's build. |

If you cannot clone this repo, stop and tell the student. Never recreate these files from memory.

## Rules

- Ask the student's questions up front (recipe Step 1). After that, stop only for approvals, account screens and anything that costs money.
- Free first. Never call a paid service without stating the service, the output and the price, and getting a yes. `engine/scripts/fal.py` and `generate.py` dry-run by default; only add `--go` after approval.
- Keys live in `engine/.env`, typed by the student. Never ask for them in chat, print them or commit them.
- Never put words in a real person's mouth (voice clone, lip sync) without their written consent.
- Reference videos are for studying style. Never reuse their footage, music or logos in the student's video. Downloaded media stays out of git.
- Before showing any draft, look at real frames (a contact sheet or stills) and check them against `references/design-rules.md` and the saved edit rules. A successful render is not a quality check.
- Every note the student gives goes through `.claude/skills/refine-video-edit/SKILL.md`, so reusable notes become rules.
- Work and finished videos stay in `output/` (ignored by git). Do not set up git or push for the student unless they ask.
- Narrate in one short line at a time. Give URLs as clickable links and open finished videos for the student.
