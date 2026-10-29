---
name: video-edit
description: Plan, render or revise any video edit using the user's saved edit rules, so each edit starts from everything they have taught you. Use before planning or rendering any video edit (Yap talking-head videos, overlays, captions, trims, covers), and whenever a draft is ready to show.
---

# Video edit

This skill does the edit. Its partner, `refine-video-edit`, learns from the user's feedback. Together they make every round better than the last.

## Before you plan or render

1. Read the saved rules in [references/edit-rules.md](references/edit-rules.md). Read the whole file every time.
2. Read the recipe for this kind of video. For a Yap talking-head video, that is `recipes/yap.md` and `recipes/yap-release-check.md`, and the `yap-video-plan` skill. If the user named a style, also read `styles/README.md` and that style's `styles/<name>/STYLE.md`.
3. Read any notes saved for this one video (its plan or feedback file under `output/`), if they exist.

If two sources disagree, use this order. The newest dated line wins inside each file.

1. What the user says in this chat, for this video.
2. The saved rules in `references/edit-rules.md`.
3. The recipe and style files.
4. The general defaults in the other skills.

Do not invent rules the user never gave. If no rule covers a choice, make a sensible call and say so in one line.

## While you work

- Apply every rule that fits this video. Skip rules that do not fit, such as caption rules when the user did not ask for captions.
- Keep one-off instructions for this video in this video's notes, not in the rules file.
- Planning does not mean permission to render or to spend money on generation. Ask first when the recipe says to.

## Before you show a draft

Go through `references/edit-rules.md` one line at a time and answer each check yes or no for this draft. Look at real frames and real measurements, not at the plan. Fix any "no" you can fix. If a "no" is a taste call, list it for the user instead of guessing.

## After you show a draft

Show the draft, then ask for feedback in one short line, for example:

> What would you change? Timestamps, "too slow", a marked-up frame, anything works.

When the user gives feedback:

1. Hand it to the `refine-video-edit` skill. It saves the reusable parts as new rules.
2. Apply the fixes to this draft.
3. Show the new draft and ask again.

Do both in the same turn. The user should never have to tell you the same thing twice.
