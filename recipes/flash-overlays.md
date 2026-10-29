# Spoken-cue overlays: engine integration

Creative strategy and asset creation live in `.claude/skills/visual-hooks-overlays/SKILL.md`. Cue alignment, individual reading holds and final-frame verification live in `.claude/skills/overlay-timing/SKILL.md`. For Yap, integrate both into the complete script plan required by `.claude/skills/yap-video-plan/SKILL.md`.

## Engine API

Activate the workspace with `source ./activate.sh` before shell commands. In `engine/scripts/yap.py`:

- `Yap.flash(image, source_cue, dur=1.5)` accepts an explicit positive finite duration with **no 0.9-second clamp**.
- `Yap.hold(image, source_cue, dur=4.5)` also uses final playback seconds. Alternatively, `until=source_end` maps a source endpoint through the cut list. If neither is given, the legacy fallback is 2 seconds; prefer an explicit planned duration.
- Cue arguments and `until` are source times. `dur` is output time and must not be divided by speed again. To work directly in edited frames, use an explicit compositor with a verified cut map.
- Resolved intervals use inclusive start/exclusive end frames. The engine reports an error for overlapping events or a hold beyond the video end instead of silently shortening them. Resolve those conflicts in the plan.
- The API does not choose a suitable visual or reading time. Follow the timing skill and verify the actual export.

## Integration constraints

Preserve the approved persistent title and original presenter framing. Engine safe-area checks alone do not establish face clearance or essential-text readability. Where masking is required, use original video → overlay → synchronized foreground presenter; inspect every composed event as specified in the design skill. Do not treat the engine's basic static overlay compositor as automatic foreground segmentation.

For Instagram, nominal safe-zone containment is only the outer boundary. Start bordered cards/screenshots/tweets and title blocks with an additional approximately 100 px horizontal inset (x=135–880 at 1080×1920, scaled proportionally), then judge visible left/right breathing room in the actual composition. Include the full border/shadow in the fit. Reduce and reposition edge-hugging cards, preserve readable evidence, and inspect at phone size with 1.05× and 1.10× crop/zoom stress checks, especially left-edge clearance. This is a conservative layout buffer, not an official Instagram crop measurement. Existing vertical exclusions, full-bleed backgrounds and approved bottom-anchored presenter exceptions remain applicable. See the Instagram spacing refinement in AGENTS.md.

Never use emoji. For Yap, the main skill's no-logo preference applies; other recipes may use genuine official logos when requested. Never fabricate UI, data or personal account evidence. Source and inspect assets before rendering, preserve chart scope and attribution, and size by content rather than a universal percentage.

Keep accepted cuts, speed and audio locked during visual revisions. Preserve originals, write versioned exports under `output/`, copy completed exports to Downloads, and show playable results inline with absolute paths. Use `recipes/yap-audio.md` for audio; this overlay change does not alter that workflow.

## Purpose and positioning check

Default to original presenter framing. For each replacement background, name its exact spoken purpose or evidence-reading benefit. Remove generic stock creator/consumer portraits and repeating desk/office filler; use original footage with the relevant overlay instead. Avoid stacking an unrelated stock scene behind an interface and presenter. Repeated backgrounds require an intentional narrative callback. Place each asset relative to the moving head/hands, with deliberate proximity, legibility and comfortable border spacing; inspect entry/middle/exit and enlarged phone crops. Product identity must match the cue: Instinct is an iMessage-based assistant, and a supplied sign-in screenshot is identification material, not a chat screenshot.
