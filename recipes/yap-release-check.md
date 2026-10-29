# Yap release check

> **Worked example.** These rules came from one creator's real feedback (Brian Doran, How to AI) over many Yap edits, so you will see "he" and past video names. Use them as a strong starting point. Your own notes are saved separately by `.claude/skills/refine-video-edit/SKILL.md` into `.claude/skills/video-edit/references/edit-rules.md`, and where your rules disagree with these, yours win.

Two gates around the edit. The first moves image choices to before the render, where a wrong pick costs seconds. The second checks the finished draft against the formula so the person reviewing sees only what failed.

Run both in a fresh session that did not make the plan or the edit. The maker grading its own work is how a written rule gets skipped. The checker gets the files and this list, and nothing about why choices were made.

## Gate 1: image picks, before any render

Input: the three-column plan (Script · source time | Proposed edit | Proposed overlay).

For every row that is not Clean:

1. Write one line stating what the speaker is claiming or doing in that row, and the feeling of the line (threatened, impressed, skeptical, amused, neutral). The image is chosen for the claim and the feeling, not for the noun.
2. Gather at least four candidates. Record for each: source link, pixel size, what it shows, and for a person, their expression.
3. Reject any candidate that fails a hard test:
   - Not the right person, product or screen.
   - A related logo or screen instead of the product's own.
   - Shorter side under 1000 px, visibly compressed, or watermarked.
   - A landing page or static number where the row needs the part that moves.
   - A person whose expression contradicts the feeling of the line.
4. Rank what is left by fit to the claim, then the feeling, then sharpness. Pick the top one and keep the runner-up.
5. If nothing survives, say so on that row. Do not fill it with the best of a bad set.

Output one contact sheet per video: each row's script line, the pick, the runner-up, and the one-line reason. This is approved or corrected in a single look before the ten-minute render starts. A swap here is "use the runner-up on row 6", not a re-edit.

## Gate 2: the finished draft, before it is shown

Input: the 720p draft, the plan, the approved contact sheet, the accepted opening reference frame if one exists.

Pull frames: 0.0 s, 1.0 s, 3.0 s, then the entry, middle and exit of every overlay row. Measure audio with a loudness pass. Then answer every line below yes or no, with the frame or measurement as evidence. No line is answered from the plan or from the fact that the render succeeded.

### Opening
- Is a substantial visual, more than a logo, on screen at frame zero?
- Is the presenter at original full-frame position and scale? If not, is there a recorded authorization for this exact scene?
- Is the title Orbitron Bold, white, with glow and dark lettering shadow, and no panel, bubble or rectangle behind it?
- Is the title directly above the moving head, clear of the face, at all three opening frames?
- Is the title at most three words, at most seven letters per word, or the user's exact wording for this video?
- Does the title leave after the hook? Does it return only where the speaker says the title phrase and the plan calls for it?
- If an accepted reference frame exists, does the opening match it? If none exists, say "no reference" and do not claim a match.

### Every overlay
- Does it show the claim or action in that line, not only something named in it?
- Is it the approved pick from the contact sheet?
- Is it on screen from the spoken cue through the last relevant word?
- Is the essential content inside x 35 to 980, y 220 to 1470?
- While the title is up, do cards sit in the band above it? After it leaves, does each behind-head image run the full width with equal side borders (60 px at 1080) from the top safe line (y≈230) down behind the head?
- Does the presenter cover only decorative parts of it, never the action, text or values?
- Is it sharp and readable at phone size, and still intact at 1.05× and 1.10× crop?
- Is it genuine? No invented interface, evidence or footage.
- Is it different from every other image in this video?

### People
- Right person?
- Does the expression fit the feeling of the line?
- Background fully removed, with clean edges around hair?
- Placed where the plan says, not covering the presenter's face?

### Logos and lists
- Is each logo the product's own official mark, in its brand color, with no white box or app tile?
- Does each logo appear when its name is spoken, once?
- For a spoken list, does each chip appear as it is said, in spoken order, in the band above the head?
- Is every text chip a genuine bullet list (roles, a tool stack)? Is any chip standing in for a concept, person or product that has real reference material?

### Pace
- Does the picture change about every 2 to 3 seconds, without a fixed rhythm?
- Is every Clean row Clean on purpose? Does any Clean row contain a named tool, list, statistic or reference to the work?

### Sound and trim
- Dialogue at the plan's speed (1.07× unless the user set another for this video) with pitch preserved?
- Integrated loudness at −14 LUFS, true peak at or under −1.5 dBTP? Report the measured numbers.
- Any laughter, breath, mouth noise or handling noise left between phrases?
- Any clipped first or last sound at a join?

### Cover
- Is there a 9:16 cover, and does it survive the thumbnail crops?

## What happens to failures

- **Mechanical** (position, size, safe zone, timing to the cue, logo background, loudness): fix, render once more, recheck only the lines that failed.
- **Taste** (which image, whether the hook lands, whether a cut feels right): do not fix. List them.

Report in this shape, failures only:

| Row or time | Check that failed | Frame | Fixed, or needs a decision |
|---|---|---|---|

End with one line: how many checks ran, how many failed, how many are left for a decision. If nothing is left, say so in one line and show the opening frame and the cover.

## Keeping it current

When a draft is rejected for a reason not on this list, add that reason here as a new yes or no line, with the date and the video it came from. New rules go into this check first. Add them to the making instructions only if the same line fails three times.

## Lines added from rejected drafts

Each line came from a real rejection. Date and video in brackets.

### Images
- Does a supplied or captured video overlay show the part that moves and impresses (charts forming, a scroll), not a static number or landing frame? [Oct 10, Analysts are Finally Cooked]
- Does a video overlay keep moving until it leaves, with no freeze at the end? [Oct 11, Slop Leadership]
- Was the supplied clip watched in full before choosing? If it does not contain what the user described, was that said and the real thing captured? [Oct 10, Analysts]
- Does every named tool, list, statistic and reference to the work have a visual? [Oct 10, Analysts]
- Is each image only the real image: no page chrome, player buttons, white borders or screenshot edges? [Oct 11, Slop Leadership]
- Where the point is "everyone is doing this", are there many real examples (about 30 covers, 6 thumbnails, 12 headlines), not one? [Oct 11, Slop Leadership]
- Does the image look like the thing named, at a glance? (A hive mind must read as a hive mind, not as bees.) [Oct 11, Slop Leadership]
- On a line that mocks or criticizes, does the image avoid making one identifiable stranger, or one race or other group, the face of the negative? Use a silhouette or a non-identifying image. [Oct 11, Slop Leadership]
- Is there a visible gap between anything drawn in front (title, logos, labels) and the head? [Oct 11, Slop Leadership]
- Is each logo the exact product named (Claude Code is not the Claude app)? [Oct 10, Analysts]

### Footage and trim
- Does any text in the footage (hat, sign, screen) read backwards? If so, is the footage flipped? [Oct 11, Slop Leadership]
- Is every repeated take, false start and stumble gone, with the best take kept? [Oct 10, Analysts; Oct 11, Slop Leadership]
- Are pauses as tight as the user asked for this video, with no small gaps left between phrases? [Oct 11, Slop Leadership, asked twice]
- Is the opening sentence intact? (A trim bug once deleted it.) [Oct 11, Slop Leadership]

### Effects
- Is any added effect (drip, glow, slide) subtle in colour and area, and behind the head unless the plan says otherwise? [Oct 11, Slop Leadership]
- If the plan says every frame has an overlay, is any frame empty, including between an exit and the next entry? [Oct 11, Slop Leadership]

### Added Oct 11, Slop Leadership draft 3 feedback
- Is the opening visual hook the most prominent thing on screen: large, animated where asked, behind the head and behind the title? [Oct 11, Slop Leadership]
- When a chart is the point, is it the chart alone, with no article or page around it? [Oct 11, Slop Leadership]
- Are any two back-to-back overlays the same kind of thing (two Wikipedia pages, two headlines)? [Oct 11, Slop Leadership]
- Does a colour the user named after a real thing (Nickelodeon slime) match a reference photo of that thing? [Oct 11, Slop Leadership]
- In a stacked title, are the lines the same font size unless the user asked otherwise? [Oct 11, Slop Leadership]
- Is a full-screen background a high-resolution, literal photo of the thing named (a real hive for "hive mind")? [Oct 11, Slop Leadership]
- When the speaker names a phone or app state (DND), does its real-looking notification appear on top of the current overlay? [Oct 11, Slop Leadership]
- If the user asked for a known image to be recreated or animated, does the result look exactly like that image? If it cannot, is the original image used instead, and was that said before rendering? [Oct 11, Slop Leadership draft 4]

### Added Oct 11, OAI vs ANT first-pass feedback
- Is there 0 ms left between phrases? Zero gap is the baseline for every video unless the user asks for air. [Oct 11, OAI vs ANT]
- Is every "um", "uh", breath or blow into the microphone, and every repeated or restarted word, cut? Silence detection alone misses all of these; check each sound between words. [Oct 11, OAI vs ANT]
- Is every chip, list and card inside x 135 to 880 (at 1080), with the same margin left and right? [Oct 11, OAI vs ANT]
- Is the cover frame flattering: eyes open, relaxed face, mouth not caught mid-word, not distorted by being close to the lens? It need not be a smile. [Oct 11, OAI vs ANT]
- Were four numbered cover options shown, and did the user pick the cover? [Oct 11, OAI vs ANT]

### Added Oct 13, Ephemeral Software draft 1 feedback
- Does the pace feel natural at the chosen speed and gap? Zero gap at 1.07x can feel rushed; offer 1.05x with a 20 ms gap. [Oct 13, Ephemeral Software]
- Is there a visual on every stretch, with no clean run longer than about 3 seconds unless the user asked for a light edit? [Oct 13, Ephemeral Software]
- Where the speaker describes a proportion or a progression (90% unused, global to personal to instance), is it an animated graphic that builds as he says it, with its text on screen, not a static chart or a text list? [Oct 13, Ephemeral Software]


### Added Oct 13, Claude vs. Chat
- In a versus list, is each product's column on the side he actually points to in the footage? [Oct 13, Claude vs. Chat]
- Where captions were asked for, are they clear of the chin and face, and as low as the safe area allows (lettering just above y 1470 at 1080×1920)? [Oct 13, Claude vs. Chat]
- Are caption words spelled as in the script, not as Whisper heard them? [Oct 13, Claude vs. Chat]
- When he asked to save to the Desktop, did the 1080p video and the cover both go into the Final Content folder? [Oct 13, Claude vs. Chat]

### Added Oct 13, Ephemeral Software draft 2 feedback
- Is every overlay that fits above the head centred vertically between the safe line and the top of the hair (or slightly above centre), not parked at the top? [Oct 13, Ephemeral Software]
- Does each overlay use the available space, with no small chips or logos in a large empty band? [Oct 13, Ephemeral Software]
- Is every chart or graphic we drew ourselves animated? [Oct 13, Ephemeral Software]
- Are chips used only for spoken lists of three or more? Does a two-item contrast have a drawn visual instead? [Oct 13, Ephemeral Software]

- In a versus list, are the chips and logos big (about 46 px text, 54 px logo at 1080 wide) and the title at least 104 px, even if the chips cover the forehead? [Oct 13, Claude vs. Chat]
- Is there a visible gap (about 50 px) between the bottom of the title and the first row of chips? [Oct 13, Claude vs. Chat]
- Is the cover a separately designed image (best face frame, title low and close to the head, big logos with glow and shadow above their names), with no chips, captions or other video text on it? [Oct 13, Claude vs. Chat]
- Do the cover's title and logos survive the 4:5 and 1:1 crops? [Oct 13, Claude vs. Chat]

### Added Oct 13, Ephemeral Software draft 3 feedback
- Is there a visible buffer between every pair of elements (logos, card, title, face)? Does anything touch? [Oct 13, Ephemeral Software]
- Does the cover show the complete idea (full chart, all logos), not a mid-animation frame? [Oct 13, Ephemeral Software]
- If sound effects were requested, are they clearly quieter than the voice, with loudness and peak still on target? [Oct 13, Ephemeral Software]

### Added Oct 13, Ephemeral Software draft 4 feedback
- Are the gaps the same everywhere, with no extra margin around the card or title? [Oct 13, Ephemeral Software]
- For any requested sound effect: does the mixed track measurably differ from the voice-only track at those moments? Report the level. [Oct 13, Ephemeral Software]
- Was any one-video design choice written into the recipe as a general rule? It belongs under "Looks used once". [Oct 13, Ephemeral Software]

### Added Oct 13, AI Certified batch feedback
- Is there an overlay on screen for every frame, with no stretch of plain footage, unless he asked for a light edit? [Oct 13, AI Certified]
- After any retake was cut, were the captions compared word by word with a fresh transcript of the finished file? [Oct 13, AI Certified]
- When one long take holds several videos, was each finished file re-transcribed to catch a repeated line the first transcript merged into one? [Oct 13, AI Certified]
- Is every image free of nudity and gore (including museum pieces and art), piracy brands, and other platforms' watermarks? [Oct 13, Ephemeral Software, zero views]

### Added Oct 16, Promote Thyself feedback
- Is every drawn animation and chart high-fidelity (the craft and motion quality of the launch-day dashboard, in whatever look suits the video), with nothing that looks like flat placeholder shapes? [Oct 16, Promote Thyself]
- Is every photo or screenshot a full card running partly behind the head, unless a strip was needed to keep critical content visible? Is every overlay and hook centred at full width (never shrunk, never pushed to one side), with its text big enough to read, even where the head covers part of it? [Oct 16, Promote Thyself v2]
- Is every animated overlay already moving on its first frame, with no blank or empty card waiting for a cue? [Oct 16, Promote Thyself]
- Does every photo show the claim, not just a generic picture of the noun? [Oct 16, Promote Thyself]
- Are overlays free of the plain white card unless it genuinely helps? [Oct 16, Promote Thyself]
- Does the main motion of every animation start on frame 0, not just an idle pulse? [Oct 16, Promote Thyself v2]
- Does the frame-zero visual hook say what the video is about without the audio, rather than an abstract animation? [Oct 16, Promote Thyself v2]
- After the final and cover are in Final Content, was ship_cleanup.py run as a dry run, shown to the user, and then run with --trash on their OK? [Oct 16, cleanup]
- Is the title centred on the frame (x 540 at 1080 wide), not on the safe area, with its lettering still inside x 35-980? [Oct 17, Promote Yourself v2]

### Added Oct 20, Latency Wins / Not So Chill / AI Watches You feedback
- Does the plan name each beat's kind (overlay on the face, backdrop behind the head, B-roll without him, green screen with him bottom left), chosen for that beat, not a card by default? [Oct 20]
- Do sourced B-roll images flash quickly (under about 1 second)? [Oct 20]
- Was the visual hook composed around the head and the title, with the title placed first? [Oct 20]
- Where the title overlaps a card, is it fully inside (centred between the card top and the hair, equal room above and below) or fully outside with a gap, never on the card's edge? [Oct 20]
- Is every must-read visual (prompt, headline, form, UI text, number) fully visible against the presenter mask? Is the visual hook free of must-read content? [Oct 20]
- Does every green-screen beat put his cutout in the bottom left at about 60%, flush with the bottom? [Oct 20]
- Was the framing checked first, and for close-up footage, were overlays kept to the ones that help the point, without forcing a visual hook? [Oct 20]
- Is the cover the most impressive frame of the opening visual hook (an animation at its peak), not frame 0 or a separately designed image? [Oct 20]
- Do the animations match the launch-day reference's craft, not flat placeholder shapes? [Oct 20]
- Is every drawn visual something that has no real image? Where a real image exists (an email, an app, a document), was the real one sourced instead? [Oct 20, AI;DR]
- Is every green-screen background a rich, full-frame visual, never a near-empty field around one small card? Is single-card content shown as an overlay on his real background instead? [Oct 20, AI;DR]
- Was every generated animation viewed at full size next to a launch-day reference frame and judged high quality, not only correctly placed? [Oct 20, AI;DR]
- Is every sourced image free of an attribution requirement (no CC BY, CC BY-SA or photographer-credit terms)? [Oct 20, user rule]
2026-10-25: No green-screen animations unless explicitly asked (user rule). Animations go in overlays; green screen is sourced only.
2026-10-25: Does the screen change about every second? No still image/card over ~1 s (headlines: just long enough to read), no animation over ~3 s, no clean stretch over ~3 s. (user rule)
2026-10-25: Read every text card at full size before sending (not thumbnails). Each card is a complete headline or short line (about 12 words / 3 lines max), readable in its hold; never a paragraph excerpt, never cut mid-word, mid-line or mid-sentence; chart crops keep their title; no unrelated page content. [Oct 25, cut-off 'AI Adoption in 2024: 74% of' card]
