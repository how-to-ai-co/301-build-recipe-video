---
name: yap-video-plan
description: Plan Yap (also called Yack) talking-head video edits with a complete segmented script, source times, proposed edits and overlays, and a specific playback-speed recommendation. Use when planning or revising a Yap video before rendering.
---

## Read the recipe first
Before any Yap plan, read `recipes/yap.md` and `CLAUDE.md` at the top of this repo. The recipe's Current shared formula overrides older conflicting defaults in this skill, including title bubbles/backing panels, persistent titles, no-logo guidance and sparse visual density. Check the actual composed result against that current formula.

# Yap video plan

This is the coordinating skill for Yap edits. It owns the full-script plan, content decisions, title, speed and accepted audio/cut baseline. Use [visual-hooks-overlays](../visual-hooks-overlays/SKILL.md) for on-screen strategy, a coherent design system, asset creation and composition review. Use [overlay-timing](../overlay-timing/SKILL.md) for spoken cues, individual reading holds and frame verification. These are three complementary skills; do not maintain competing timing policies here. The audio implementation remains `recipes/yap-audio.md`.

Use image overlays only. The persistent title is the only added text unless the user explicitly asks for other text. Do not add word cards, photo labels, or text rasterized into an image. Existing text within approved source charts and genuine screenshots may remain. Use clean footage when no image adds value.

Always make the full script visible in the plan. A summary, highlight list, or cue sheet alone is insufficient.

Preserve the speaker's content, opening and sequence by default. Cleanup covers dead air and clear delivery mistakes; it does not authorize shortening the argument, deleting examples, replacing the hook or imposing a runtime target. Mark substantive cuts as optional discussion items unless the user requests them. Do not treat repeated emphasis as an error automatically. If the user-stated duration differs materially from the measured source duration, report both and resolve the source/version mismatch before presenting a definitive timeline; never cut content merely to force the stated duration.

## Required planning output

Title text uses **Title Case** (capitalize the first letter of every word; preserve acronyms such as AI), a larger bold size, and a slightly lower screen position. At 1080×1920, start around 104 px type with the title centered near y=410 (scale proportionally), then fit to the wording and actual head movement. Keep the full title inside the Instagram safe rectangle and clear of the face; do not move or shrink the presenter. These are starting measurements, not permission to overlap a face. Titles use the fewest words that clearly name the subject. Remove unnecessary possessives, introductions and filler: recommend "AI Video Workflow," never "My AI Video Workflow." Do not pad a clear title to a minimum word count. Keep the recommendation at the top alongside speed. Style the background like an Instagram text bubble: measure the rendered glyph bounds and fit a rounded bubble to the text with compact, even padding (start with 16–24 px per side at 1080 px width). Never stretch the bubble to a fixed frame-wide width or leave large empty wings beside the words. Size the bubble from the actual text, including when the font or wording changes. Place it slightly lower in the upper portion of the frame (the y≈410 center above is a starting point), with safe-zone and head-movement checks. Preserve an existing title's wording and case during padding/position-only revisions. (Where `recipes/yap.md` sets a different title look, such as no backing panel, the recipe wins.)

Start with the shortest clear recommended title at the very top, clearly labeled as proposed and open for discussion, followed by one recommended constant playback speed between **1.03× and 1.07×**, inclusive, and explain why it suits this specific take. Separate speed changes from silence removal. Consider delivery within sentences, density, emphasis, and pauses; raw whole-file words per minute can be misleading. Label estimates and unverified listening judgments honestly. Do not merely list the allowed range or silently let an engine default override the recommendation.

Provide a complete source-order chart with exactly THREE columns. Display the chart inline in the chat, not in a separate file. Chunk the entire script moment by moment into approximately **1–2-second source chunks**, using natural caption-style phrase boundaries (often 3–7 words), not whole sentences or paragraphs. Timing determines chunk size; do not force a word count. These are script-row durations, not overlay hold durations. Include the source in–out time inside each script cell. Keep edit and overlay cells compact, expanding only for a meaningful issue:

| Script · source time | Proposed edit | Proposed overlay |
|---|---|---|

- Account for **every spoken word**, including removed sections, repetitions, false starts, and the ending. Include start/end dead air and between-segment pause treatment separately. Use readable source timecodes. Never abbreviate script cells with ellipses, topic labels, or sentence fragments standing in for omitted words.
- Keep source text separate from proposed text. For each chunk, state Keep, Trim, Cut, or Move with a short note only when useful. Keep means the complete script cell is retained unchanged; Cut means it is omitted. For partial changes show the exact retained wording, or split the row so retained and deleted words are separate. CUT means no resulting speech. For moves, identify the exact destination in playback order.
- Use actual recorded wording for executable edits. Label any suggested new wording as a pickup/re-record rather than implying it exists in the footage. Flag uncertain transcription without silently altering the source.
- Use the design skill to define a short visual strategy and concrete design brief before the script chart: what the video should demonstrate, which moments need evidence, the shared visual treatment, and reserved title/presenter areas. Every selected overlay cell must identify the event, exact visible concept, purpose/takeaway, source status, essential content, and composition. Incorporate the timing skill's edited in/out and cue; mark intervening rows **Clean**. Do not substitute image-generation prompts, vague topic labels or a cue sheet for the complete script. No emoji or logo overlays for Yap unless the user changes that preference. Develop representative composed storyboard frames before bulk asset production; preserve current authorization boundaries.
- The three-column chart is the primary deliverable. Do not automatically duplicate it with a second full-script section. Supply a retained-only reading script separately if requested. Preserve complete source coverage in the chart.
- If offering an alternative, clearly label it and provide exact replacement wording/source ranges. Keep one primary recommendation unambiguous. Do not silently delete the speaker's position or rewrite their claims as verified facts.
- Recommend title text at the top alongside the selected speed, before the chart. A new title is proposed for discussion; preserve a title the user has already approved. If asked only to plan, finish the reviewable plan without rendering.

## Video-engine context

The video engine is this code repository, not a visual application. Do not invent an engine dashboard, GUI or product screenshot. Show actual user interactions in Claude/chat when relevant, or a genuine repository/code view only when specifically useful or requested. For personal workflow steps, identify user screenshots or screen recordings needed. Public product screenshots may illustrate a generic interface but cannot establish the user's own actions.

Read `CLAUDE.md` and the current `recipes/yap-audio.md`, `recipes/flash-overlays.md`, and relevant `engine/scripts/yap.py` behavior. Treat older project examples and supplied guides as references, not new user requests. Use the repo's Python environment (see the setup steps in `CLAUDE.md`) before shell commands. Keep originals untouched. Supporting analysis may be saved under `output/`, but the requested plan belongs inline in the chat.

Inspect metadata, obtain/reuse word timings, and inspect representative frames. State whether audio was actually listened to. Source times from automatic transcription remain provisional until checked; do not invent frame accuracy or edited timestamps. Provide edited cue times/frame numbers only when a concrete cut list supports them. Estimate runtime from retained material, intended pause treatment, and chosen speed, and distinguish estimates from measured renders.

## Approved trimming baseline

Use the script and waveform **together** for every trimming pass. The script identifies intended speech and phrase boundaries; the waveform locates the actual speech edges and non-speech events. A loud laugh, breath blown into the microphone, mouth noise, or handling burst can occupy a removable gap even when it never crosses a silence threshold. Review those between-phrase events explicitly; do not mistake acoustic energy for useful speech. Remove unwanted non-speech gaps with explicit editorial cuts, protect the last and next phonemes, and review the join. Preserve intentional laughter or emphasis when it serves the delivery; follow the user's specific feedback. Silence detection and automatic word timestamps are aids, never the complete trimming decision. Automatic transcription can collapse repeated phrases into one: when the user flags a stumble, compare the waveform and transcribe each delivery separately before selecting the complete take.

Use audio-based trimming as the starting point for Yap cleanup. Do not rely on transcript word gaps alone: automatic timestamps often stretch across real pauses inside phrases. Detect quiet intervals in both the raw audio and the full-take DeepFilterNet output, initially at **−40 dB for at least 220 ms**. For automatic silence cuts, trim only their overlapping quiet region, leaving **50 ms on each side** (about 100 ms total per internal join). Remove leading/trailing dead air with the same speech-edge protection. Apply the same cut map to picture and audio, with 12 ms audio fades at joins and pitch-preserving tempo at the selected speed.

Thresholds are a starting point, not a mandate to cut quiet speech. Inspect uncertain boundaries and re-transcribe the edited audio to catch missing words; transcription is not a substitute for listening. Preserve the content, emphasis, breaths needed for natural delivery, and the approved speed. Save each video's accepted cut list (for example `output/<project>/approved-cuts.json`) so it can be reused. Once trims/audio are accepted, lock them during visual revisions.

## Rejected visual directions

When the user rejects a set of visuals, remove them from the active edit and do not carry them into the next plan. Preserve prior version files for recovery. Develop a fresh full-script plan before adding replacement visuals. Do not assume permission to generate replacements. A rejection can be narrow: for example, the user may reject every metaphor image in a video while keeping its trims, speed and audio. Keep what was approved.

## Composition and audio

- Keep the approved title continuously visible from the first frame through the last frame of every Yap edit, unless the user explicitly requests different timing. The title is independent of flash-overlay cadence and remains during clean presenter footage. Verify opening, middle, ending, and timeline coverage; never apply a short opening-only title by default. (`recipes/yap.md` may now say otherwise; the recipe wins.)
- When the user asks for a tighter cut, review false starts, repeated setup, filler asides, and hesitation inside sentences—not only long silences. Preserve the argument and examples while choosing the cleanest delivery. A speed increase alone is not a trimming pass.

- Preserve original talking-head framing: never shift, shrink, pad, or crop the presenter to create overlay space unless expressly requested. If an overlay overlaps the presenter, composite original video → overlay → synchronized background-removed presenter at identical scale and position. The presenter may partly occlude the overlay. Preserve approved cuts, speed, and audio during visual-only revisions.

- Select the visual medium for its purpose: recognizable photographic cutouts, meaningful illustrations, humorous composites, or real demos. Use screenshots only when their visible content proves or clarifies the point immediately. Do not invent personal materials, UI, claims or results. Concepts may be proposed before sourcing; never present them as acquired evidence.
- Delegate all overlay cue and duration decisions to [overlay-timing](../overlay-timing/SKILL.md). Visual complexity determines the necessary reading time; the timing skill does not choose images. Apply the design skill's composition review to every event. Preserve the approved persistent title's location and styling during overlay revisions; adapt overlays around it.
- For Instagram at 1080×1920, contain text and reference overlays inside x=35–980 and y=220–1470 with breathing room and face clearance; scale for other resolutions. Include actual composed-frame verification with safe-zone exclusions in the build plan. Apply the user's separate green-screen presenter rules only to green-screen edits.
- Plan the current Yap speech-cleanup chain and final -14 LUFS integrated / true peak ≤ -1.5 dBTP. Preserve natural breaths and word boundaries; silence detection can misclassify quiet speech. Listening remains distinct from measured loudness.
- Do not assume music, full captions, generated imagery, or paid services are wanted. Plan only requested or clearly proposed additions.

Show the entire three-column plan inline in the conversation. Do not deliver it as a separate file or substitute a file link. Split long charts into consecutive inline parts if needed, without omitting any script. Validate that no source segment is missing and the edited script matches the selected cuts before presenting it.

## Overlay scale and depth

For talking-head edits, image overlays should average roughly two-thirds of frame width (about 720 px at 1080 px). Start charts and substantial imagery at that scale; do not shrink them to fit above the presenter. Keep the approved title and original presenter framing, and composite the large image behind the synchronized foreground presenter. Tighten title/image spacing and allow the head to overlap the image's lower portion. Prioritize keeping the main visual takeaway and key values visible; do not solve overlap by making the whole image tiny. Review every appearance. Small logos are a separate asset class when explicitly requested.

## Finished-video cover

Use [yap-cover-image](../yap-cover-image/SKILL.md) before final delivery. Every finished video includes a separately exported 9:16 cover displayed inline beside the playable video, unless the user opts out. Select a strong actual frame and reuse or adapt approved artwork; the cover skill owns frame selection, thumbnail composition, crop review and delivery. Cover-only requests do not require repeating the full-script edit plan.

## Learning from feedback

Before planning, also read `.claude/skills/video-edit/references/edit-rules.md` and apply its rules. When the user gives feedback on a plan or draft, use the `refine-video-edit` skill to save the reusable parts.
