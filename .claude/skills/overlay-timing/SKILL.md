---
name: overlay-timing
description: Time planned video overlays to spoken cues and individual reading durations using edited-audio word timestamps and frame verification. Use after the visual strategy is defined; does not choose or generate images.
---

## Read the recipe first
Before timing overlays, read `recipes/yap.md` and `CLAUDE.md` at the top of this repo, plus `.claude/skills/video-edit/references/edit-rules.md`. The recipe's Current shared formula overrides older conflicting defaults in this skill, including title bubbles/backing panels, persistent titles, no-logo guidance and sparse visual density. Check the actual composed result against that current formula.

# Overlay timing

Own the temporal decisions for each selected overlay. [yap-video-plan](../yap-video-plan/SKILL.md) owns the full-script strategy and accepted edit; [visual-hooks-overlays](../visual-hooks-overlays/SKILL.md) owns design and asset creation. Do not redesign an asset or change accepted speech cuts to fit a convenient timing slot.

## Required inputs and cue sheet

Use the locked cut map, selected speed, output frame rate, edited-audio word timestamps, and concrete visual concepts with their essential reading content. If editing is not yet locked, mark timings provisional. Do not invent exact edited times from source transcript ranges alone.

For every event record: event ID; exact trigger word/phrase; original source cue; edited word onset and final relevant word; proposed edited in/out; end-exclusive output frame range; duration; and a short reason for the reading hold. Keep source seconds, edited seconds and frame numbers distinct. Cross-check source timings through the cut map where available. Identify a cue removed by a cut rather than mapping it to unrelated retained speech.

Use Whisper or another available transcription/alignment tool on the actual edited audio. Automatic timings are estimates; inspect uncertain speech edges with waveform/context and listen where capability is available. State what was actually checked and whether a listening review was completed.

## Individual durations

Enter on the related spoken cue. An opening image may deliberately enter on frame zero before its named phrase; label that anticipation and keep it through the phrase.

Use at least **1.0 second**, usually **1.5 seconds** for a simple image. Charts and detailed evidence often need **3–5 seconds or longer**. These are starting points, not a cap, a fixed cadence or a coverage quota. Choose each hold from its actual reading burden and the spoken thought. Keep it through the final relevant word with a brief exit allowance, generally 0.15–0.30 seconds unless the next thought requires a different transition. Extend for reading when needed; identify that extension in the plan. Do not equate a transcript row with an overlay duration or hold every image through an entire paragraph.

If reading time conflicts with the next cue, resolve it visibly in the plan: simplify with the design skill, select fewer events, or revise the transition. Do not silently shorten, stack or retrigger visuals. Leave deliberate clean presenter footage between events where the content permits. No routine interval, one-second ceiling, or required percentage of visual coverage applies. (`recipes/yap.md` may set a faster pace, such as a change about every second; the recipe wins.)

Measure durations in **final playback seconds after speed changes**. Quantize to the actual output frame rate and store inclusive start/exclusive end frames. Do not divide an already edited timestamp or output hold by playback speed a second time.

## Engine and verification

Use the repo's Python environment (see `CLAUDE.md`) and inspect current `engine/scripts/yap.py` behavior. `flash(..., dur=...)` and `hold(..., dur=...)` use explicit output durations; their cue argument is source time. The engine must not clamp to 0.9 seconds or silently shorten collisions. Flag overlapping events and out-of-range holds for resolution before rendering. An explicit edited-frame compositor is also valid.

Check the final export, not just the cue sheet: first visible frame, last visible frame, first clean frame after exit, planned duration, cue alignment and clean gaps for every event. Readability and foreground occlusion belong to the design skill's entry/middle/exit composition review. If speech cuts or speed change, recompute every affected event. Preserve approved audio during visual-only revisions.
