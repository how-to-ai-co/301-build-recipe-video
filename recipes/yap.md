# Canonical Yap Formula

> **Worked example.** These rules came from one creator's real feedback (Brian Doran, How to AI) over many Yap edits, so you will see "he" and past video names. Use them as a strong starting point. Your own notes are saved separately by `.claude/skills/refine-video-edit/SKILL.md` into `.claude/skills/video-edit/references/edit-rules.md`, and where your rules disagree with these, yours win.

Use these complementary skills:

- `.claude/skills/yap-video-plan/SKILL.md`: complete script-led plan, title, speed, content decisions and accepted edit baseline.
- `.claude/skills/visual-hooks-overlays/SKILL.md`: on-screen strategy, shared design system, concrete concepts, assets and composed-frame readability.
- `.claude/skills/overlay-timing/SKILL.md`: exact spoken cues, individual reading holds, source/output mapping and frame verification.

The plan starts with title and speed, then a concrete visual strategy/design brief, followed by the complete source script inline in exactly three columns: Script · source time | Proposed edit | Proposed overlay. Every selected overlay must say what appears, why it helps, what evidence it uses, and how it fits the title/presenter composition. Integrate timing into that same plan. Mark other rows Clean. Create representative composed storyboards before producing a batch of assets. Do not start with disconnected image prompts.

Keep the detailed creative and timing rules in their owning skills. Use `flash-overlays.md` only for engine integration and `yap-audio.md` for the unchanged audio workflow. Planning does not authorize rendering or paid generation; honor existing user authorization.

## Release check and how rules get added — October 11, 2026

`yap-release-check.md` (next to this file) is part of the formula. Run it on every video:

1. **Before any render:** Gate 1. For each overlay gather at least four candidates, reject the bad ones, and show one contact sheet (pick, runner-up, one-line reason per row). Render only after it is approved or corrected.
2. **After the draft render, before showing it:** Gate 2, in a fresh session or sub-agent that did not make the edit. Fix mechanical failures; list taste calls.
3. **Every time the user gives edits on a draft:** turn each new reason into a dated yes-or-no line in `yap-release-check.md`, and put any lasting rule in this file. Do this in the same turn as the fix, and say which lines were added.

## Current shared formula — October 9, 2026

This section supersedes conflicting historical defaults in skills and earlier AGENTS.md notes. Read this file before every Yap plan, first trim, visual edit and release review. Read AGENTS.md for additional shared feedback and the selected video's plan/feedback for project-specific exceptions. Shared style does not mean identical overlay concepts.

### Text hook
- Orbitron Bold, normally 104 px at 1080×1920, scaled proportionally. White lettering with a visible glow and strong dark lettering shadow for separation. No solid black rectangle, rounded black bubble or backing panel. Glow is a lettering effect, not a panel. Exact glow/shadow parameters must be matched to an accepted composed reference; do not claim an arbitrary preset is the approved match.
- Place the title directly above the actual moving head, close enough to form one composition, with face clearance and Instagram-safe placement. Do not squeeze a screenshot into a strip between the title and the head. Fix title position, size and layout while visible; remove permanently after the opening hook or when it interferes with evidence. Never bring it back.
- Default Title Case; preserve explicitly approved exceptions. At most three words, at most seven letters per word, aiming for 12–14 letters total. “Browsers are out.” remains that video's explicitly approved wording.

### Hooks, overlays and backgrounds
- Every opening combines recorded verbal hook, short text hook and substantial meaningful visual hook visible at frame zero. Logos alone do not explain the argument.
- Each visual illustrates the exact spoken claim/action, not just a mentioned noun. Use genuine sharp UI, product artwork, whole social evidence with source context, photographic cutouts and actual charts. Never invent factual evidence, UI or user footage. Only AI Data Story has extra user app footage available in this batch.
- Use meaningful changing visuals through the video, about every second (Oct 25 rule below: stills ~1 s, animations ≤ ~3 s), driven by thought and reading time. Do not use a fixed periodic grid, tiny UI strips, random stock portraits/offices, or duplicate imagery as filler. Deliberate clean footage is allowed when it communicates better.
- Plan each beat as original footage + overlay, deliberate replacement background, or full-screen evidence. State why replacement is useful for that spoken cue. Never use blank keyed backgrounds. A shared look must still give each video and scene its own concept.
- Preserve original presenter framing by default. Large substantial imagery starts around two-thirds frame width when useful; compose behind a synchronized foreground presenter at original position/scale. Presenter overlap may hide decorative regions, never the essential action, text or values. Do not shrink, move to a corner, or replace the opening environment unless the user explicitly authorized that treatment for this exact video and scene. Old Amazon/green-screen exceptions do not transfer to new projects. A proposed edit or generic permission to edit is not approval to reframe the presenter.
- Keep essential content within x=35–980, y=220–1470 at 1080×1920; bounded screenshots/cards start within x=135–880. Maintain comfortable visual margins. Full-bleed backgrounds and approved bottom-anchored presenter exceptions remain valid.
- Added text is the text hook only, unless explicitly authorized; no emoji, word-card or fabricated-text substitutes. Genuine logos/source text are permitted.
- Time each visual to its actual spoken thought through the final relevant word plus exit allowance; charts need individual reading holds. Review actual composed entry/middle/exit, moving hands/hair, phone-size readability, source context, sharpness, contrast, safe-zone overlays and 1.05×/1.10× crop stress. Render success is not aesthetic approval.

### Trim, sound and delivery
- Every video: 1.07× dialogue, pitch preserved, local speech cleanup, −14 LUFS integrated and true peak ≤−1.5 dBTP.
- First-pass target: 200 ms total retained inter-phrase pause. Combine complete script with raw/enhanced waveform and inspect noisy non-speech, laughter, handling noise and breaths. Protect phonemes and emphasis; review every changed join. Automatic quiet-gap detection alone is not the editorial pass.
- Preserve originals, editable projects, accepted takes and explicitly approved substantive cuts. Other content deletions need an explicit decision.
- Full timestamped script and beat-specific overlay/treatment strategy accompany review. Follow existing authorization for baseline/visual work; finished-video approval remains separate.
- Every finished edit includes a deliberately selected/designed 9:16 cover, reviewed at full size and thumbnail crops. Only explicit finished-video approval saves video + cover to Desktop / Final Content.

### Required check before delivery
Record the recipe revision used and check the actual composition against this formula, including font/glow/shadow/no-panel, above-head placement, frame-zero visual hook, distinct cue-specific imagery, readable depth, trim/sync/audio and cover. If an exact accepted style reference is missing, state that limitation rather than declaring a matching style. A written recipe is required context, not an automatic rendering guarantee.

Yap trimming must combine the full script with waveform inspection. Explicitly inspect between-phrase laughter, mic-blown breaths, mouth noises, and other loud non-speech gaps: silence detection alone misses them. Make targeted editorial cuts while protecting neighboring phonemes and reviewing the join.

## Cover at completion

Use `.claude/skills/yap-cover-image/SKILL.md` to select a strong frame, create a full 9:16 cover, review thumbnail crops, and attach the image inline with every finished video. Preserve the finished video when authoring its cover.

## Selectable visual style

Read `../styles/README.md` when a named style or reference is requested. Apply the chosen profile to the complete script-led plan while retaining the approved cut/audio baseline and final-cover requirement. Profiles are creative guides read by Claude, not automatic engine flags.

## Style consistency correction — October 10, 2026
The Microsoft corner-presenter opening is rejected as the default Yap look. Original full-frame talking-head framing is mandatory for new opening hooks unless this exact scene has explicit user authorization otherwise. Keep the title directly above the original moving head, not above a shrunken corner cutout. Readable image overlays may sit behind a synchronized foreground copy at identical source scale/position. Avoid oversized blurry marketing backgrounds that convey no clear action.

Batch consistency requires a single reusable title implementation and an accepted composed opening reference, not eight independent interpretations of font/placement/glow. Until that component/reference is actually implemented and validated, do not describe the recipe as enforcing consistent output. Before a batch full export, check each video's composed opening and representative body treatment against the accepted reference. Record explicit scene-specific reframing authorization; absent it, preserve the original.

## Lists, logos and video overlays — October 10, 2026 (Analysts are Finally Cooked feedback)

- **Clean logos.** Use the product's own official mark, never a related one (Claude Code is the pixel mascot, not the Claude app burst). Vector source where one exists, brand colour unchanged, background fully removed: no white box, no app tile, no screenshot crop. One logo per spoken name, shown when the name is said. A product with no mark of its own gets its name in the list font, not a borrowed logo.
- **Reference material first, text chips last (October 11).** When the speaker names a concept, person, product or claim, show the real thing: the Wikipedia chart, an article headline, the YouTube or Instagram title card, the pricing page, a real photo. Text chips (white rounded labels) are only for genuine bullet lists where the words themselves are the content, such as a list of roles or a tool stack; each item appears as it is said. Never label a concept with a chip when reference material exists.
- **Curate five, pick one (October 11).** For every image slot, gather about five real candidates, look at them side by side, and choose the one that reads fastest at phone size and best matches the exact words spoken. Do not ship the first result found.
- **Title may return on its own name (October 11, Slop Leadership).** When the speaker says the title phrase later in the video, the title text may come back for that line. Otherwise it still never returns.
- **Video overlays.** A supplied or captured screen recording is an overlay like any other: behind the head as a rounded card, or full screen when the speaker is talking about the visual itself. Show the part that moves and impresses (charts forming, transitions), never a static number or a landing page. Watch the whole clip before choosing; if the clip does not contain what the user describes, say so and capture the real thing from the live page.
- **Quick infographics.** A spoken statistic can flash in as a tiny label-free graphic (2 of 100 people), background removed, held for the sentence.
- **Density.** Look for a visual at every named tool, list, statistic and reference to the work itself before calling a row Clean.
- **Drafts are 720p and one per video.** Each new draft replaces the previous one; intermediates are deleted after the render. 1080p is rendered once, on approval.

## Overlay size, cleanliness and motion — October 11, 2026 (Slop Leadership feedback)

- **Big once the title is gone.** After the title leaves, an image runs the full safe width with equal side borders (60 px each side at 1080), starts at the top safe line (y≈230) and continues down behind the head, "halfway behind" the presenter. Do not crop an image small just to keep it above the head.
- **Breathing room in front.** Anything drawn in front of the presenter (title, logos, labels) keeps a visible gap above the head; never line it up flush against the hat or hair.
- **Only the real image.** Strip page chrome, player buttons, white borders and screenshot edges. A video cover is just the cover; an app graphic is cropped inside its own card.
- **More is better for crowds.** When the point is "everyone is doing this" (podcasts, Mac minis, headlines), show many real examples: 30 covers, 6 thumbnails, 12 headlines.
- **Video overlays last the whole beat.** A scroll or clip must keep moving until the overlay leaves; never let it finish and freeze while the speaker continues.
- **Motion is allowed when asked.** Slide-ins from different sides and the dripping title were requested for Slop Leadership; default remains hard cuts.
- **Density is per video.** Slop Leadership has an overlay on every frame at the user's request; other videos keep deliberate clean stretches unless he says otherwise.
- **Speed is per video.** Default 1.07×; Slop Leadership uses 1.05× with ~120 ms pauses.

## Trim method and covers — October 11, 2026 (OAI vs ANT, approved by the user as "a great trim")

### Zero-gap trim (the baseline for every video)
- **0 ms between phrases.** Every silence of 50 ms or more is removed completely. Do not leave 200, 120 or 70 ms of air; those earlier settings are retired.
- **Cut on the cleaned track.** Find silences on the speech-cleaned audio only. Requiring the raw audio to be quiet too leaves every breath and blow into the microphone in the cut.
- **Work in sound islands.** Split the cleaned track into islands of sound (anything above −40 dB peak, split at each 50 ms silence). Transcribe every island under one second on its own. Drop the ones that are not words: "um", "uh", breaths, clicks, laughs.
- **Protect word edges.** A small island with no transcript that sits within 120 ms of a word is that word's first or last consonant (the "s" of "stalls", the "-ing" of "overlapping"). Keep it. Islands as short as 15 ms can be a whole word ("because"); keep them.
- **Cut on the script, not only on silence.** Remove repeated takes, restarts ("on the, on the"), self-corrections ("one model or, sorry, one product"), filler lead-ins and sentences that repeat the one before. Where two takes exist, keep the last complete one.
- **Check the result against the script.** Re-transcribe the finished audio and compare it word for word with the intended script; a missing word means a cut landed wrong. Leave a stumble in if there is no safe place to cut, and say so.
- **Reference implementation:** `output/oai-vs-ant/build_trim.py` (islands in `islands.json`, every cut listed with its reason in `cut-map.json`).
- **Limit:** none of this is listening. Flag the tightest joins for the user to hear.

### Lists and cards
- Every chip, list and card sits inside x 135 to 880 at 1080 wide, with the same margin on both sides.

### Covers
- **Always offer four cover options** and let the user approve one. Never pick the cover alone.
- Options are real frames from the take with the title added, chosen for how he looks, not for a smile: relaxed face, eyes open, a natural or thinking expression, looking off-camera is fine. He chose a mid-thought, eyes-up-and-away frame for OAI vs ANT over a neutral straight-to-lens one.
- Show the four side by side, numbered, before rendering the final.

## Pace and animated infographics — October 13, 2026 (Ephemeral Software)
- **Pace is per video.** Zero gap at 1.07x is the tight default; when it feels rushed use 1.05x with a 20 ms gap. Ask if unsure.
- **Animate proportions and progressions.** "90% you don't need" is 100 squares switching off to 10; "global to personal to instance" is a funnel whose tiers grow in as each is named, with the words on the tiers. Prefer this over a static chart or a text list.
- **Fill the gaps.** Unless the edit is meant to be light, every stretch gets a visual; simple drawn animations (pieces locking together, a double-click, an icon dropped in a bin, a rising curve) are fine where no real reference exists.
- **Write cues in source time** and map them through the cut map, so changing speed or gap never needs retiming (see `output/ephemeral-software/compose.py`).


## Versus lists, captions and short-video delivery — October 13, 2026 (Claude vs. Chat, saved to Final Content by the user)

Reference implementation: `output/claude-vs-chat/build_trim.py` and `compose.py`.

### Versus list (two products compared item by item)
- **Watch which side he points to.** Pull a frame at each spoken product name and put each product's column on the side he points at. Do not assume the order of the title. (Here: Claude on screen left, OpenAI on screen right.)
- **One chip per spoken item:** the logo plus the use case ("Writing", "Computer use"), appearing at the start of the spoken product name, stacking down its column in spoken order.
- **Parent-company logo for sub-products when he asks for it.** Dot, Codex and Chat all took the OpenAI mark on this video at his request. This is an exception to "the product's own mark" and applies only when requested.
- **Chips are see-through and big:** white at about 74% opacity, dark Space Grotesk Bold 46 px text, 54 px logo in its brand colour, 72 px tall, soft shadow. The first version (34 px text, 36 px logo, inside x 135 to 880) was rejected as far too small. Columns use the full safe width: left starts at x 60, right ends at x 960. Pick the largest size at which the two longest chips on one row still fit with a gap.
- **The title stays up for the whole video** when it is the heading of the two columns. Keep it big: "Claude vs. Chat" ran at 112 px on one line (92 px was rejected as too small), lettering at about y 320 to 425.
- **Leave a buffer between the title and the first row of chips** (about 50 px). Do not butt the chips up against the title.
- Size beats face clearance on these lists: he would rather the chips cover his forehead than be small. Keep the eyes and mouth clear.

### Captions (only when he asks)
- **Orbitron Bold, smaller than the title (66 px at 1080), one line, one word at a time**, same white lettering with dark outline and shadow as the title. No panel.
- **As low as the safe area allows:** lettering sits just above y 1470, under the chin and over the hands. Never on the chin or face. (Layer top y 1370 in `compose.py`.)
- Each word appears at its spoken start and holds until the next word; every word gets at least 3 frames.
- **Spell from the script, not from Whisper** (it hears "clod" for Claude and "codecs" for Codex). Check that the word count matches the timings. Drop commas and full stops; keep a question mark.

### Trim and speed are per video
- He can set both on any video. This one ran at 1.00x with 70 ms retained pauses (35 ms each side of every sound island on the cleaned track). Zero gap and 1.07x remain the defaults when he does not say.
- A repeated take is still cut with the last complete one kept, without asking.

### Delivery
- **"Final drafts", "final content" and "save it to my desktop" all mean `~/Desktop/Final Content/<Title>-final/`.** When he asks to save there, render the 1080p and save the video and the cover together in one go. Do not save the cover alone and wait for a separate approval.
- A short video with a precise brief (title, layout, trim settings all given) can go straight to a 720p draft without the plan table.
- **He dictates, and "Yap" often arrives as "app"** ("app style format", "app recipe"). Both mean this recipe.

## Placement, animation and visual-first rules — October 13, 2026 (Ephemeral Software draft 2)
- **Centre overlays in the band.** Anything that fits above the head sits vertically centred between the top safe line (y≈226) and the top of the hair, or a touch above centre. Never park it against the safe line. Measure the head top for each take. Applies to logos, cards, lists and tweets alike. (`centred()` in `output/ephemeral-software/compose.py`.)
- **Fill the space.** When the head is low in frame, overlays get bigger to use the band; small chips floating in a large empty area fail.
- **Any chart or graphic we draw ourselves is animated.** It builds as he speaks (squares switching off, funnel tiers growing, a line drawing itself, a cursor double-clicking, an icon dropped in a bin). A real chart from a source is animated too where possible, by revealing it left to right.
- **Visualization first, chips last.** Use text chips only for a spoken list of three or more items, and make them large. Two items, a contrast or a progression gets a drawn visual instead (today/tomorrow became two different editor windows).
- **Animated hook.** The visual hook may be an animation in the first three seconds (Adobe's chart drawing itself while the cloned Adobe app icons blink out). The cover is a chosen moment of that animation.


## Covers are designed, not picked — October 13, 2026 (Claude vs. Chat; supersedes "options are real frames with the title added")

- **A cover is its own composition and never appears in the video.** Pick the best frame of his face, then place the title and artwork for the cover alone. Do not reuse the video's overlay layout, and do not carry chips, captions or any other on-screen text onto it: the title is the only text.
- **Title lower and closer to the head** than in the video, with a small gap above the hair (lettering ended about 40 px above the hairline here).
- **One big logo per side for a versus video, each directly above its own name** in the title ("Claude" under the Claude mark, "Chat" under the OpenAI mark). About 230 px at 1080 wide: big and recognizable at grid size.
- **Logos are not flat.** Background removed, then a coloured glow, a drop shadow, a thin light rim and a top highlight so they stand off the painting. Shade the background above the head a little so the title and logos read.
- Keep title and logos inside the 4:5 grid crop (y 285 to 1635) and check the 1:1 crop too.
- Still offer face-frame options when the choice is open; once he picks a frame, build the designed cover on it.
- Reference implementation: `output/claude-vs-chat/cover.py`.

## Logo-field hook, sound effects and composed covers — October 13, 2026 (Ephemeral Software draft 3)
- **Buffers between elements.** Logos, cards and the title never touch each other; keep at least ~20 px between any two, and around the face.
- **Sound effects only on request.** Default is still none. When asked, keep them far below the voice (each drop about 30 dB down) and re-check loudness and peak.
- **The cover can be composed.** It need not be a frame of the video. Build the ideal still: his face, the complete chart, every logo, the title. Still offer four face options.

## Sound effects must be measured — October 13, 2026
- **Prove a sound effect is in the file.** I cannot hear, so measure it: compare the mixed track with the voice-only track and report the effect's level. A sound effect that measures as silence is a failed render. Use a pitch a phone speaker can play (above ~400 Hz).

## Per-video design choices are not rules — October 13, 2026
A creative direction given for one video stays with that video. Record it under "Looks used once" below, not as a rule, unless the user says it applies to every video. Do not make every intro look like the last one.

### Looks used once (reference only; do not apply by default)
- **Ephemeral Software hook:** dozens of app logos scattered at random (mixed sizes, slight tilts, one even 16 px gap), filling the frame right up to his head from behind the cutout, poofing away with soft drop sounds while a stock chart draws itself. Code: `output/ephemeral-software/compose.py`.
- **Slop Leadership:** big two-line title with Nickelodeon-slime drips; paywall cards sliding in from different sides; an overlay on every frame.

## Captions and the safe zone — October 13, 2026 (Ephemeral Software, approved)
- **Safe zone, confirmed by the user's Reels guide:** 1080×1920; top 220 px and bottom 450 px reserved; 35 px each side; an extra 100 px strip on the right beside the buttons in the lower part. Safe area is x 35–980 (lower right) and y 220–1470.
- **Captions only when asked.** Small (Space Grotesk Bold, about 46 px at 1080), white with a dark outline, a few words at a time, timed to the speech. Place them flush on the bottom safe line (text ending about y 1465), which is below his chin. Correct the automatic transcript's names before rendering. No captions on the cover.


## Constant overlays and batch cuts — October 13, 2026 (AI Certified, 13 videos from one take)
- **No blank sections.** An overlay is on screen for every frame of the video: each one holds until the next cue, from frame zero to the last frame. The first draft of this batch had three or four overlays per video with clean footage between them and was sent back for it. (Slop Leadership got the same request; my reading is that this is now the default unless he asks for a light edit.)
- **Fill with real screenshots first, then small drawn animations** (a toggle switching on, a progress bar reaching a tick, a multiple-choice card being clicked, a calendar day lighting up). No added words in them.
- **When his head is high in frame, use short cards.** A 960×200 card on the top safe line stays fully readable above the hair; tall screenshots go behind the head and lose their middle.
- **Captions after a retake cut:** Whisper can time a repeated line on the take that was cut. Re-transcribe each finished file and compare it word by word with the captions before showing it.
- Reference implementation: `output/ai-certified/build.py` (one script, video number as the argument), `anims.py`, `prep_assets.py`.

## Content that can kill distribution — October 13, 2026 (Ephemeral Software got zero views as a trial reel)
Not confirmed by Instagram; these are the likely causes found in a full audit, removed in v2.
- **No nudity or gore of any kind,** including museum dioramas, classical art and cartoons. The caveman diorama (nude figures, raw bloody hide) was the strongest suspect.
- **No piracy brands** (The Pirate Bay, torrent sites) and nothing that looks like promoting copyright infringement.
- **Never re-upload an identical file after deleting a post.** Instagram treats it as a duplicate. Make a real change first.
- App and brand logos used as illustration are fine; avoid another video platform's watermark sitting on top of the footage.

## Overlay fidelity, size and starts — October 16, 2026 (Promote Thyself feedback, "as a new rule")
- **High fidelity only.** Every drawn animation, chart and overlay is high-fidelity: rich, detailed, smoothly animated and finished-looking, never simple flat placeholder shapes. The reference is the *quality* of the AI Certified launch-day dashboard (https://ai-certified-launch-day.vercel.app/): its craft, detail and motion, not its branding. Its colours, gradients, glows and particle style were arbitrary; choose the look that fits each video. Keep the storytelling (the right visual for the spoken claim); add the craft. The same bar applies to full-screen B-roll.
- **Full overlay by default.** A photo or screenshot is a full card (about 960 px wide, from the top safe line down) running partly behind the head, like the "large corporation" cubicles in Promote Thyself. Crop it into a strip above the head only when something critical would otherwise be hidden behind the head, which is rare. Never shrink an overlay that carries text, and never shift an overlay to one side: visual hooks and overlays are centred at full width, and it is fine for the head to cover part of them. Text on them must be big enough to read.
- **Charts and animations may be cropped** to a band above the head when that reads better; that is a creative call, and a square/full card is fine when the idea needs it.
- **Animations start immediately.** An animated overlay is already moving on its first frame. Never put up an overlay that sits blank or empty while it waits for a spoken cue. The main action starts on frame 0 (the orb climbing, not just pulsing in place); an idle throb is not a start.
- **No boring photos.** A generic stock photo that only names the noun is not enough; it must show the claim (Promote Thyself: the data center needs the "trapped employees" in it). The exception is a fast flash of several images in succession, where the sequence itself is the interest.
- **Not everything on a white card.** White rounded cards are not the house style. Use the dark launch-day panel look, or no background at all when the elements stand on their own (logos, objects with shadow and glow).
- **A visual hook names the topic at a glance.** An abstract animation is not a hook. The frame-zero visual must make the subject obvious before a word is heard (Promote Thyself: the particle org chart read as 'chart', not 'promotion').

## Cleanup after shipping — October 16, 2026
Once a video's 1080p final and cover are saved in `~/Desktop/Final Content/<Title>-final/`, clear its working files:
1. Run `python3 engine/scripts/ship_cleanup.py` (dry run) and show the user what it would move.
2. On their OK, run it with `--trash` (or `--archive <folder>`). It never hard-deletes; captions are copied into the Final Content folder first.
Only shipped videos are touched; anything not yet in Final Content keeps all of its files.

## Fit the format to the footage — October 20, 2026 (Latency Wins / Not So Chill / AI Watches You feedback)
This section supersedes, where they conflict: "Full overlay by default" (Oct 16), "No blank sections" (Oct 13 AI Certified), "Preserve original presenter framing" for the layouts named below, and the four designed cover options.

- **The four kinds of added visual (use these words in plans and notes).** Older sections say "overlay" for any added visual; from here on:
  - **Overlay:** a non-full-screen image, animation or card *on top of* his face (in front of him).
  - **Backdrop:** a non-full-screen image, animation or card *behind* his head, with his cutout in front. Backdrops are where the behind-the-head rules apply (only decorative parts may be hidden; never must-read content).
  - **B-roll:** full screen *without* his face. Sourced images usually flash quickly (under about 1 second); rendered animations can run longer.
  - **Green screen:** full screen *with* his face on screen, his cutout in the bottom left at about 60% (below).
- **Pick the right kind for the job, not a card by default.** For each beat choose the kind (overlay, backdrop, B-roll, green screen) and the content (a sourced image, a background-removed cutout, a rendered animation or card). Not every video has to look the same.
- **The title leads the composition.** Title placement comes first and outranks every other layout rule. The visual hook is built around his head and where the title sits, not the other way round.
- **Title and card never straddle.** When the title sits over a card, it is either fully inside the card, centred in the space between the card's top edge and his hair with equal room above and below (as in AI Watches You), or fully outside the card with a clear gap. It never sits on the card's top edge (the Latency Wins and Not So Chill openings).
- **Must-read content.** Mark every visual that carries something to read (a prompt, a headline, a login form, UI text, a number). Must-read content is fully visible: never in a backdrop where his head can cover it, checked against the presenter mask. Avoid must-read content in the visual hook altogether.
- **Green screen for full-screen graphics.** When a beat's visual (especially a visual hook) is a graphic or a rendered animation, it can run full screen with his background-removed cutout moved to the bottom left at about 60%, flush with the bottom edge. This layout is pre-approved; it does not need per-video permission.
- **Close-up footage.** Before planning, check how close he is. When his head fills the top half of the frame, don't force the usual format: use fewer overlays, and the hook can be title + face + verbal hook with no visual. Add a visual only where it helps make the point, as an overlay on top of the face, green screen, or B-roll.
- **Cover = the best frame of the visual hook.** Not frame 0 and not a separately designed composition: take the most impressive frame from the opening seconds of the visual hook. If the hook is an animation, capture it at its peak, when it is most interesting.
- **Animation quality.** Background and hook animations meet the craft bar of https://ai-certified-launch-day.vercel.app/ (see Oct 16). Simple circles, rings and progress bars on a dark panel (Latency Wins) fall short.
- **Real image over a drawn one (Oct 20, AI;DR).** Don't draw a graphical representation of a thing when a real image of it can be sourced: show a real email screenshot, not bars standing in for an email. Drawn animations are for ideas that have no real image (a process, a count, a transformation), and they must still meet the launch-day bar.
- **No plain green-screen background (Oct 20, AI;DR).** A green-screen background is always a rich, full-frame visual, like the AI;DR slop-wall hook. Never a near-empty field with one small card on it. If the visual is a single card (an email, a screenshot), don't use green screen: keep his real background with him at original framing, put the card over his face as an overlay, and put any text (a prompt, a headline) up top.
- **Check what you made, at full size, before sending (Oct 20, AI;DR).** After every render, look at each generated animation and drawn frame at full size, next to a launch-day reference frame, and ask whether it is high quality, not just placed correctly. Flat placeholder shapes (bars for text lines, empty panels, sparse fields) fail; redo them or swap in a real image. Placement checks alone are not this check.
- **No images that need a credit (Oct 20, user rule).** Never use a sourced image whose licence requires attribution (CC BY, CC BY-SA, or any "credit the photographer" terms). Use public-domain or CC0 images, the product's own official screenshots and press assets, or real screenshots captured live. Sourcing briefs must reject credit-required images outright, not rank them.

## No green-screen animation — October 25, 2026 (user rule, 12-clip batch)
- **Never use a rendered animation as a green-screen background** unless he explicitly asks for it. A green screen is a full-screen background, so it needs high-resolution footage or imagery; our animations aren't that quality. Animations are fine as overlays (and backdrops). Sourced images and video are fine as green screen.

## Change the screen every second — October 25, 2026 (user rule, 12-clip batch)
- **The screen changes about every second.** A static image, screenshot or card holds about 1 second (a must-read headline gets just enough to read, then moves on). An animation may run up to about 3 seconds. Nothing holds longer than ~3 seconds, including clean footage. Long holds (13 s, 9 s, even 3 s on a still) were the biggest problem in the Oct 25 drafts.
- This supersedes "normally around each 2–3 seconds" in the Current shared formula. A spoken beat that lasts 8 seconds gets a run of different visuals (several sourced images of the same idea, the animation split into short moments), not one held card.
