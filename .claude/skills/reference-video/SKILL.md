---
name: reference-video
description: Break down a reference video the user likes (Instagram Reel, TikTok, YouTube Short, any link, or a local file) and turn its style into a plan for their own video. Use whenever the user shares a video link or file as inspiration, says "make mine like this", "copy this style", "edit it like this one", or asks what makes a video work.
---

# Reference video: "make mine like this"

The user shows you a video they like. You measure it, look at it, write down what makes it work, then show how to get the same feel with **their** footage and brand. You copy the style, never the footage.

## 1. Run the breakdown

From the `engine/` folder (use the engine's `.venv` Python if it exists, so Whisper is available):

```bash
python3 scripts/reference.py "<link or file path>"
```

- Quote the link. A dragged-in file path works too (strip any quotes around it).
- Add `--name short-name` if the user gave the video a name ("the oren one"), so the folder is easy to find.
- **No `yt-dlp`?** The script prints the install line and stops. Run `python3 -m pip install yt-dlp` (or `brew install yt-dlp` if they have Homebrew), say so in one line, and rerun.
- **Instagram/TikTok login wall?** Never try to get around it. Offer the two honest options: rerun with `--cookies-from-browser chrome` (or safari/firefox) after they log in to the site in that browser, or they save the video themselves and drop the file in. Never ask for their password.
- **No Whisper?** Fine, the transcript is skipped. Mention it once; don't install a 500MB model unless they want the words.

Output lands in `references/videos/<slug>/`: `contact.png`, `frames/`, `analysis.json`, `breakdown.md`, and `transcript.json` when Whisper ran.

## 2. Look before you write

1. Read `contact.png` (one tile per shot, labelled with time and shot number).
2. Read every `frames/hook_*.jpg` (0s, 0.5s, 1s): this is the hook, the most important second.
3. Read a handful of `frames/shot*.jpg` at full size to check fonts, caption style and colour.
4. Read `breakdown.md` and `transcript.json` if present.

Sanity-check the numbers against what you see. Scene detection can count a fast zoom, flash or big text change as a cut, and miss a slow dissolve or a punch-in on the same shot. Timelapses and flickery footage inflate the count. If the numbers look wrong, say so and rerun with `--threshold 0.4` (fewer cuts) or `0.2` (more).

## 3. Fill in the breakdown

Edit `references/videos/<slug>/breakdown.md` in place:

- Replace every `_(...)_` placeholder in **What's on screen** with what you actually saw. Mark guesses as guesses ("looks like a bold condensed sans, maybe Anton").
- Tick through **Make mine like this**: hook in the first second, title style, caption style, overlay pattern, colour/grade, music/energy, pacing, closest existing style, what to change for their brand. Keep it plain language; the user is a marketer, not an editor.
- Only describe what is visible or measured. Never guess a font name, song or tool as fact.

## 4. Propose how to apply it

Then tell the user, briefly:

1. **What makes it work** in 3-5 bullets, using the measured numbers ("a new shot every 1.4s", "title on screen for the first 2s").
2. **Closest match in this repo.** Read `styles/README.md` and compare with Yap Depth, Oren Static Hooks and Editorial Tech. Say which is closest and what differs. If none fits and the user wants to reuse this look, offer to save a new `styles/<name>/STYLE.md` as `styles/README.md` describes (source URL, evidence, observed techniques, parameters, asset needs, review checklist).
3. **A plan for their video**: which recipe applies (`recipes/yap.md` for talking heads, `recipes/flash-overlays.md` for overlays), what pacing to aim for, title/caption/overlay choices, and what footage or assets they need. Respect the safe zones in `instagram-safe-zone.md` even if the reference ignores them.
4. Ask **one** question to move forward (usually: "Want me to plan your edit this way?").

Before actually editing, hand over to the `video-edit` skill, which applies the user's saved rules. The user's own rules beat the reference when they conflict; say so in one line.

## Rights

- Reference videos are for studying style: pacing, layout, type, energy. That is how editors have always learned.
- **Never put the reference's footage, audio, music or graphics in the user's video**, and never republish it.
- Downloaded media stays out of git. Everything in `references/videos/<slug>/` except `breakdown.md` is gitignored (video, frames, contact sheet, transcript, analysis.json); only `breakdown.md` (your words and numbers) is worth keeping.
- Credit the creator in the breakdown (the script records the link and uploader). If the user wants music "like this", offer an original bed with `scripts/bed.py` instead.
