---
name: visual-hooks-overlays
description: Define a coherent visual strategy and create purposeful video overlays from a script, supplied evidence and a shared design system. Use for overlay concepts, asset selection, storyboards and composition; exact cue timing belongs to overlay-timing.
---

## Read the recipe first
Before planning overlays, read `recipes/yap.md` and `CLAUDE.md` at the top of this repo, plus `.claude/skills/video-edit/references/edit-rules.md`. The recipe's Current shared formula overrides older conflicting defaults in this skill, including title bubbles/backing panels, persistent titles, no-logo guidance and sparse visual density. Check the actual composed result against that current formula.

# Overlay strategy and design

Own what appears on screen, why it helps, and how the assets look together. [yap-video-plan](../yap-video-plan/SKILL.md) owns the complete script and accepted edit. [overlay-timing](../overlay-timing/SKILL.md) owns cue alignment, individual durations and final frame ranges. Do not generate images merely because a transcript mentions a noun.

For Yap edits, overlays are images only; the persistent title is the only added text unless explicitly requested. Never substitute text cards or add labels to image cards. Preserve existing text in approved source charts and genuine screenshots.

## Start with the communication strategy

Read the whole script before proposing assets. Identify the central argument, the opening promise, the claims that benefit from visible evidence, and passages best served by the presenter alone. Choose a small set of purposeful moments; do not fill a cadence or assign an image to every row.

For each selected event specify the exact spoken point, the visual's job (evidence, explanation, demonstration, comparison or deliberate joke), exactly what the viewer sees, and the one takeaway it should make easier to understand. A label such as "AI graphic," "funny collage" or "relevant screenshot" is not an executable concept. A joke or metaphor must have a clear connection and understandable payoff; do not default to unrelated stock objects or random generated scenes.

Use the user's supplied evidence first when it fits the claim. For statistics, show the actual chart or a faithful chart made from available data. For products or processes, use a genuine relevant screen or demonstration. For an abstract relationship, an unmistakable conceptual illustration may help. Clean presenter footage is a valid recommendation when no visual adds information. Never invent measurements, intermediate data points, personal accounts, UI, claims or results. In Yap edits use no emoji or logo overlays unless the user changes that preference.

## Define one design system for this video

Before sourcing or generating a batch, state a short concrete design brief in the plan:

- Visual approach and tone, grounded in this script and supplied assets.
- A restrained palette, typography and hierarchy, background treatment, borders/corners, and consistent emphasis/callout treatment.
- The approved title's reserved area, the presenter's actual moving footprint, safe zones, and the usable overlay area.
- The limited asset families that serve this video, such as source charts with consistent callouts or genuine product crops. Use a coherent treatment across families; consistency does not require rebuilding genuine evidence or distorting assets into identical boxes.
- A simple, consistent entrance/exit treatment. Give the timing skill the asset's reading burden; do not decide durations by animation style.

Preserve the approved title, its upper-frame placement and styling defined by the Yap skill, continuously. Do not remove, move or shrink it to accommodate an overlay. Adapt the overlay around it or raise a concrete layout conflict. Preserve the original presenter framing. Do not assume a universal overlay size or reuse an empty template as a substitute for a scene-specific idea.

## Make the plan reviewable before production

In the full-script plan, give each selected overlay an event ID and a specific concept, evidence/source status, essential text or data, composition, and the takeaway. Mark intervening rows Clean. Integrate the timing skill's cues into the same overlay cell; do not replace the complete script with a visual mood board or cue list.

Before bulk asset production, make representative composed storyboard frames for materially different layouts using actual presenter frames and the persistent title. If a source asset is missing, identify it honestly as a proposed asset. Resolve illegibility, title conflicts and weak concepts in these frames before repeating the treatment. Work within existing user authorization; planning does not itself authorize rendering, paid generation or external publishing, and existing approval does not need to be requested again.

Asset creation follows the concept and design brief. Use existing real assets, faithful plotting or deterministic layout for factual graphics. Use generated imagery only for a specific justified illustrative scene within the user's authorized scope; a design request is not an automatic request for generation. Never present generated material as factual evidence. Give each generated scene an individual prompt that includes its narrative action, the shared visual style, composition and reserved title/presenter areas.

## Composition and quality review

For Instagram at 1080×1920, keep essential overlay content in x=35–980, y=220–1470 with breathing room; scale proportionally. Inspect source sharpness and aspect ratio before choosing size. Preserve units, dates, qualifications and source attribution on evidence; any callout must repeat the actual data accurately and remain clearly scoped.

Preserve original talking-head framing. If an overlay intersects the presenter, composite original video → overlay → synchronized background-removed presenter at identical scale and position. Foreground masking may cover decorative areas, never essential labels or data. If the available space cannot accommodate a readable chart with the title and presenter, simplify its framing without altering meaning, choose another composition, or explicitly flag the conflict. Do not silently remove the title or cover the face.

Review actual composed entry, middle and exit frames for every event, including head/hand movement, at phone size and with the safe-zone exclusions. Verify that the takeaway is legible, the asset supports the exact claim, the design treatment is coherent, the title remains visible, and essential evidence survives masking. Revise or omit failures. Ask the timing skill to extend a hold when reading requires it; longer duration does not fix unreadable text.

When visuals are rejected, retire them from the active edit while preserving prior versions. Return to the full-script strategy for replacements instead of generating more variations of the rejected idea. Keep accepted audio and cuts locked.

## Overlay scale and depth

For talking-head edits, image overlays should average roughly two-thirds of frame width (about 720 px at 1080 px). Start charts and substantial imagery at that scale; do not shrink them to fit above the presenter. Keep the approved title and original presenter framing, and composite the large image behind the synchronized foreground presenter. Tighten title/image spacing and allow the head to overlap the image's lower portion. Prioritize keeping the main visual takeaway and key values visible; do not solve overlap by making the whole image tiny. Review every appearance. Small logos are a separate asset class when explicitly requested.
