# AI 301 build recipe: Video

Make a video for your business with nothing but Claude.

Copy this whole recipe into Claude Code. Keep this page open while you work.

By the end you will have one finished video of your own: a talking-head edit of footage you filmed, a clip with captions, a moving graphic, or a video in the style of one you admire. Along the way, Claude learns your taste. Every note you give becomes a saved rule, so your next video starts closer to what you want.

## The job

Act as my video editor and motion designer. Ask me everything you need up front, set up the video engine, study any reference video I give you, plan the edit with me, build a first draft, critique it yourself, take my notes, save them as rules, and export the final video.

Use the video engine at https://github.com/how-to-ai-co/301-build-recipe-video. Clone it to `~/Documents/video-engine` (its own folder, not inside another project and never a temporary folder: I will keep using it). Read its `AGENTS.md` and `CLAUDE.md` before you start, and follow `CLAUDE.md` as if it had loaded on its own. If the clone fails, stop and tell me. Never recreate the engine's files from memory.

## Work with me

- Run commands, edit files and check results yourself. I should not need to open Terminal unless an installer needs my Mac password.
- Show me every draft as a playable video, and open it for me.
- Give every URL as a clickable link, never inside code formatting.
- Ask all your questions in Step 1, using clickable options if you have them, otherwise lettered choices. After that, only stop for my approvals, account screens I have to click through myself, or anything that costs money.
- Never spend money without asking. Free paths come first. Before any paid generation call, tell me the service, what it makes and the price, and wait for my yes.
- Never ask me to paste API keys or passwords into chat. Tell me exactly where to paste each key privately (`engine/.env`).
- Taking time is fine. Working in silence is not. Tell me what you are doing in one short line at a time.
- Use plain language. Explain any technical word the first time it comes up.

## Step 1: ask me everything up front

Ask these together, in one or two screens. Skip any question my earlier answers make unnecessary.

1. **What are we making?**
   - A. A talking-head video I filmed (cut the pauses, add a title hook, captions and overlays)
   - B. A clip of my footage with a hook and captions
   - C. A moving graphic: an animated logo, a stat or quote, a chart that draws itself, a short "how it works"
   - D. Words on screen timed to a voiceover (no footage needed)
   - E. Something else (I will describe it)
2. **Where will it go?** Instagram or TikTok (9:16) / YouTube (16:9) / LinkedIn or a feed post (4:5 or 1:1) / a paid ad / not sure yet.
3. **Do you have a video you'd like it to feel like?** Paste a link (Instagram, TikTok, YouTube, anything) or drop a file. Optional.
4. **Your footage or files.** Drop them in, or tell me where they are (for example the latest video in Downloads). Skip for C and D.
5. **What should it say?** The one message, in your words. For A and B, the footage already says it; tell me the point and the call to action.
6. **Your website**, so I can take your colours, fonts and logo. Optional.
7. **Voice and music** (only if there is no voice in the footage): no voice / I'll record a voice memo / generate one (paid). Music: none / an original bed composed here (free).

Save the answers (no secrets) to `.video/setup.json` in the engine folder.

## Step 2: set up the engine

Follow Part 3 of `CLAUDE.md` (Stage 0 preflight and Stage 1). Check quietly and stop me only for what is missing:

1. Node.js 18 or newer. If it is missing, send me to https://nodejs.org for the LTS installer.
2. Python 3, for word timings and transcripts.
3. ffmpeg, if I chose A or B, a reference video or footage edits. If it needs Homebrew, give me the one command and wait while I type my password.
4. Install what the chosen format needs, and nothing more: `npm install` in `engine/` for Remotion formats, the Python packages in `engine/requirements.txt` for timings and transcripts, and `yt-dlp` if I gave a reference link.
5. For a moving graphic (C), read `motion-studio/README.md`, check `node -v` and pick the Node version or the no-install browser version.

Report what passed in one short list, then move on.

## Step 3: my brand

Fill in `engine/src/brand.mjs` from my website, or from my answers if I have none: name, colours, fonts, logo, call to action and words I never use. `examples/doranalytics/` shows what a finished brand looks like; never copy its values. Show me the result in one short table and let me change anything.

## Step 4: study the reference video

Skip this step if I gave no reference. Otherwise follow `.claude/skills/reference-video/SKILL.md`: download or read it, measure its length and pacing, make a contact sheet, look at the frames, and fill in its breakdown. Then tell me in three or four lines what makes it work (the hook, the pacing, the text style, the look) and what we will borrow. Borrow the style, never the footage.

## Step 5: plan it with me

Read `.claude/skills/video-edit/SKILL.md` and the saved rules it points to, plus the guides that fit what I chose:

- **A, talking head:** `recipes/yap.md` and `.claude/skills/yap-video-plan/SKILL.md`. Show me the plan as a table: script with timestamps, proposed edit, proposed overlay. Put the title hook at the top and recommend a speed.
- **B, clip with captions:** `parts/45-creator-clips.md`.
- **C, moving graphic:** `motion-studio/README.md`. Propose the beats (what is on screen, second by second).
- **D, words on screen:** `parts/20-format-rsvp.md` or `parts/30-format-captions.md`.
- **Always:** `references/design-rules.md`, and `styles/` if I named a look or my reference matches one.

Ask me one question: **Build it / Change something first.**

## Step 6: build the first draft and critique it yourself

Build it at draft quality (720p) so it renders fast. Before you show me, make a contact sheet or pull frames, look at them yourself, and check them against `references/design-rules.md`, the saved edit rules and `recipes/yap-release-check.md` for talking-head edits. Fix what fails. Then show me the draft and tell me in two lines what you checked and what you fixed.

## Step 7: take my notes and learn from them

Ask for my notes: timestamps, "too slow", "bigger title", anything. Then follow `.claude/skills/refine-video-edit/SKILL.md`: fix this video, and save the notes that should apply to every future video as rules in `.claude/skills/video-edit/references/edit-rules.md`. Tell me in one line which rules you saved. Do one more round if I want it.

## Step 8: export

Render the final at full quality (1080p) in the ratio I need, plus the second ratio if it is an ad. Run the delivery check (`parts/80-naming-and-delivery.md`). Open the final for me and tell me where the file is.

## Finish with a handoff

End with:

- Where the final video is, its length and size.
- Which rules you saved from my notes, and where they live.
- Anything that used a paid service, and what it cost.
- Two ideas for my next video using the same setup.

Update `.video/setup.json` with what was built. Tell me that next time I can open `~/Documents/video-engine` directly in Claude Code and just say what I want to make. Then give me this resume prompt:

> Resume my AI 301 video from `.video/setup.json` in `~/Documents/video-engine`. Check what is done, keep it, and continue from the next unfinished step. Use my saved edit rules. Do not repeat the questions.
