> ## Cleaned for redistribution
>
> This copy replaces the original production film's dialogue, captions, checker
> line sets, brand strings and account identifiers with generic placeholders.
> All technical content — models, parameters, costs, code, thresholds, command
> lines and failure lessons — is unchanged. Where the audit notes at the bottom
> claim word-for-word or byte-identical matches against source files, those
> matches were verified against the original production strings, not the
> placeholder text shown here.

> ## Read this first: two codebases, one convention
>
> This section was written by reading the **original production repo**, which is
> where all of this actually ran and shipped. Every constant, filter graph and
> failure in it is real and was checked against that source, twice.
>
> The `engine/` folder in this bundle is a **consolidated rebuild** of that
> pipeline. It does the same things with a tidier layout. Where this section
> describes a path or a wiring detail, translate it:
>
> | The original repo | `engine/` in this bundle |
> |---|---|
> | `Theme`/`DARK`/`PAPER` declared inside `AdPaid.tsx` | `src/theme.ts`, imported by every component |
> | Timings flat at `public/words_*.json` | `public/words/<number>.json` |
> | `video/timings.py`, `video/prosody.py` | `scripts/timings.py`, `scripts/prosody.py` |
> | `Root.tsx` with ~40 hand-written `<Composition>` blocks and static imports | `Root.tsx` generated from `src/configs.mjs` |
> | Composition id hand-written per ad | derived: `<Format><number>-<OFFER>-<ratio>` |
> | One shell script per wave | one `build.sh` reading `configs.mjs` |
>
> **On the dynamic words import.** The audit pass flagged
> `require(`../public/words/${...}`)` in the generated `Root.tsx` as unrunnable.
> That is correct for the original repo's setup and **wrong for this bundle**:
> Remotion bundles with webpack, which resolves a template-literal require into
> a context module over the whole directory. It was tested here with two ads and
> rendered four files. Trust the test, not the claim, and if you ever switch
> bundlers, re-test it first.
>
> Everything else below stands as written.

> **Extra note for this section:** this is the most expensive format and the
> one with the longest failure log. Read `parts/70-playbook-and-failures.md`
> before spending a single credit here, and do not start with this format.

# 40 · The Kling 3.0 dialogue-film pipeline (ad 409), end to end

Ad 409 is the only dialogue film in the original project. Everything else in `video/` is
voiceover over footage or typography. This section is the whole route for a
Kling 3.0 talking-face ad: connect the MCP, get reference images into Kling,
submit a generation, judge the takes, and cut them into two delivery ratios.

Two things to fix in your head before reading further, because the repo contains
both and they are not the same thing:

- **`video/kling_kit/KIT.md`** is the *run sheet*: the global setup box, the
  three-batch structure, the cherry-pick checklist, the delivery convention. The
  procedure is live. Its *shot content* (daylight kitchen, bat resting on a
  shoulder, the "…whose / …plan?" beat) belongs to a run that was abandoned on
  7/29 and should not be shot again.
- **`video/script409.md` v2** is the current plan of record for what 409 says and
  looks like: night interior, 12 shots in 21.3s, five reusable camera setups, the
  "…whose / …plan?" beat deleted.

The code in the repo (`assemble409.py`, `check_take.py`) was written against the
v1 line set, before the v2 rebuild. Commit order proves it: `1d40064` (the
checker and the grade pass) lands before `c9ecf19` (409 script v2). So the tables
inside those files are v1 data sitting in v2-era tooling. Both consolidated
programs below therefore take their tables as **data you supply**, and ship the
v1 tables verbatim as the known-good example plus a v2 table derived from
`script409.md`.

Status at handoff: stage 1 (script) and stage 3 (all five camera setups as
stills) are done and approved. Stage 2 (character sheets) is done but **not
fully signed off**: `video/gen/v2_sheets/README.md` records BOSS Part A approved
(`boss_portraitA.png`, contrast 37.1 / saturation 70.9 — "these are the numbers
every later reference must match") and Part B still unresolved, because
`boss_profileA.png` measures 48.9 saturation and `boss_profileB.png` 101.5, so
neither matches the portrait. Stage 5 (video generation) is next. No 409 cut has
ever been judged shippable. `video/out409_9x16.mp4` is the v5 prototype; human
review rejected it — the words were wrong, and the whole thing read as obviously
AI-generated.

One naming trap. `assemble409.py`'s own first line reads "Assemble 409 v2 — J-cut
edition". That "v2" is the *edit* version, not `script409.md` v2. The cut map in
it is the v5 prototype's. Do not read the file's docstring as evidence that the
current script is already implemented.

---

## (a) MCP setup

### 1. Register the server

The Kling MCP is a remote HTTP server. The verified registration, read out of
`~/.claude.json`, is exactly this and nothing more:

```json
{
  "mcpServers": {
    "kling": {
      "type": "http",
      "url": "https://kling.ai/mcp"
    }
  }
}
```

No API key, no token, no env block. Authorization is an in-app OAuth handshake
against whichever Kling account you sign in as, which is why the account check
below is not optional.

The documented CLI equivalent is `claude mcp add --transport http kling
https://kling.ai/mcp`. **Not verified in this session** — the JSON entry above is
the artifact that is known to work; if the CLI form differs on your version, edit
`~/.claude.json` directly.

### 2. Restart. This is the step that ate a whole session.

**Tools load only in a session started AFTER the `~/.claude.json` entry exists.**
A session that was already running when you added the entry will never see the
tools no matter what you do inside it. The previous session burned itself out on
this. Quit, relaunch, then confirm.

### 3. Confirmation, in this order

```
ToolSearch "+kling"          -> should list 8 tools:
                                who_am_i, query_membership_and_credits,
                                query_tasks, file_upload,
                                text_to_image, image_to_image,
                                text_to_video, image_to_video
```

Then, in order:

1. **`who_am_i`** — the server's own instructions say to call this first. It
   returns the signed-in identity plus, for every generation tool, its available
   models and for each model the full argument spec: required flags, defaults,
   allowed values. Defaults vary by membership tier, so this is the authoritative
   source for section (c), not this document.
2. **`query_membership_and_credits`** — the account guard. **Before spending a
   single credit, verify which account your OAuth session is bound to by
   checking the credit balance.** OAuth binds to whichever account happened to
   be signed in, and it is easy to land on the wrong one. In the original run
   two logins existed: a funded team account carrying an 8000-credit membership
   grant, and an unfunded personal account reading 66 credits. If the balance
   is not the funded balance you expect, you are on the wrong login. Do not
   generate on it. Membership grants also expire on a schedule (the original
   grant lasted one month from issue), so read the expiry too. One calibration
   note: the MCP reported 8000 where the web Credit Details page reported 8091;
   it appears to exclude bonus credits. A small gap like that is expected, not
   evidence of a wrong account.

Measured and settled: **the MCP spends the membership credits, not a separate
API balance.** `query_membership_and_credits` read 8000 before a job and 7820
after a 180-credit job on the same funded account. There is no second meter.

### 4. Browser fallback (only if the MCP breaks)

The web app has a Custom Multi-Shot UI, mapped 7/28: Omni → Video Generation →
toggle **Multi-Shot**, then **Custom Multi-shot**. That gives per-shot
description boxes with duration steppers, a `+ Shot` button, one shared reference
tray, and a Native Audio toggle in the control bar. It is the only route with a
real per-shot duration control.

Driving it from Claude has two traps, both verified:

- Create the tab **inside the MCP tab group and front it**. Tabs created outside
  the group render 0x0 and every screenshot comes back blank.
- Use `kling.ai/app/...` URLs. **Never `app.klingai.com/global/...`** — it
  redirects and drops the session.
- Multiple Chrome browsers can be paired to the extension, and **every paired
  one can still be the wrong (personal) account** — in the original setup both
  paired browsers were the personal session, and the correct profile was a
  third one that was not yet connected. Verify the signed-in identity in the
  tab before doing anything. If the tools land on the wrong account, run
  `switch_browser` and have whoever owns the funded account click Connect in
  the right profile's window.

Browsers are computer-use tier "read", so you cannot drag files into the page.
That was the original upload blocker. It is dead: `file_upload` takes a local
path. Use the MCP.

---

## (b) Upload recipe: two steps, free

Uploading costs no credits. It is a ticket call plus a POST you make yourself.

**Step 1 — get a ticket.** Call `mcp__kling__file_upload`:

| Argument | Type | Notes |
|---|---|---|
| `filename` | string | e.g. `01_character_sheet_HIM.jpg` |
| `contentType` | string | MIME type, e.g. `image/jpeg`, `image/png`, `video/mp4` |
| `size` | integer | file size in **bytes**, exact |
| `taskTraceId` | string | optional UUID v7 grouping chained steps of one intent |

It returns a single-use `ticket`, an `uploadUrl`, and an `expire_at`.

**Step 2 — POST the bytes.** The MCP does not move the file for you. The endpoint
below is the one this repo recorded as working; the **`uploadUrl` that step 1
hands back is the authoritative target**, so if the two ever disagree, POST to
the returned one.

```bash
TICKET='<ticket string from step 1>'
curl -X POST https://kling.ai/api/mcp/files \
  -F "ticket=$TICKET" \
  -F "file=@video/kling_kit/01_character_sheet_HIM.jpg;type=image/jpeg"
```

The response carries `data.url`. **That URL is the reference URL** you pass into
`inputs[].url` on a generation call.

Rules that cost something to learn:

- **Tickets are single-use and expire in about 10 minutes** (`expire_at` is
  authoritative). Upload immediately before the generation that consumes them,
  not at the top of a session. A batch of ten uploads followed by twenty minutes
  of prompt writing means ten dead tickets.
- **Reuse the returned URL** for an unchanged local file instead of
  re-uploading. URLs produced by prior Kling tasks can be fed straight back in
  with no download and no re-validation.
- **Input spec, enforced:** PNG or JPG only, below 4K resolution, at most 30MB,
  aspect ratio no wider than 1:2. All ten `kling_kit` jpgs pass.
- Publicly reachable external URLs work too, in place of an upload.

---

## (c) Generation parameters

### The call shape

`image_to_video` and `text_to_video` share one shape:

| Parameter | Required | Shape |
|---|---|---|
| `model` | **yes, no default** | one of the models `who_am_i` lists for that tool |
| `arguments` | yes | `[{"name": "...", "value": "..."}]` — **every value is a string**, including numbers and booleans |
| `inputs` | for image routes | `[{"name": "image_1", "inputType": "URL", "url": "https://..."}]` |
| `rationale` | yes in practice | plain-English purpose of this specific job |
| `taskTraceId` | optional | UUID v7 tying chained calls together |

The call returns a `generation_id` immediately. Poll `query_tasks` with it. Read
the stale-API warning in the failure log before you interpret anything it says.

### Models

| Model | Use for | Why |
|---|---|---|
| `kling-video-v3_0_omni` | multi-reference work | up to 7 reference images, 9:16, native audio, multi-shot |
| `kling-video-v3_0` (non-Omni) | **single-character dialogue — the default for 409** | takes a scene still as `first_image`, renders in about half the time (6 min vs 13), and does not hallucinate a reference sheet into a shot |
| `kling-image-v3_0_omni` | stills, reference-consistency, identity holds | 4 credits per 2 images at 2k. Default for everything except the A24 compile |
| `kling-image-o1` | surgical edits to an existing still | 2 credits, removed the debris artifact first try |
| `gpt-image-2` (not Kling) | the A24 Part C compile, and any from-behind framing | 70 credits per 2 images at 2k, best grade fidelity and instruction following |

### Arguments

Measured 7/28 on `kling-video-v3_0_omni`. Defaults are only listed where they
were actually observed; the rest are marked and must be read from `who_am_i`.

| Argument | Value used for 409 | Default | Notes |
|---|---|---|---|
| `prompt` | the whole film in one string | none | see section (d1) |
| `duration` | `"8"` to `"15"` | not recorded | integer seconds, range 3-15, **15 is the hard ceiling** |
| `aspect_ratio` | `"9:16"` | not recorded | |
| `resolution` | `"1080p"` | **`4k`** | 1080p is the finishing res and costs less |
| `imageCount` | `"1"` | not recorded | |
| `prefer_multi_shots` | `"true"` | not recorded | Omni route only |
| `enable_audio` | `"true"` | **`false`** | see below |
| `first_image` | the scene still | n/a | non-Omni `kling-video-v3_0` route |

> **`enable_audio` defaults to FALSE.** Silent takes are the single easiest way
> to waste credits on this pipeline. A 15s silent take is 180 credits of nothing,
> because the whole point of routing dialogue to Kling 3.0 is its native audio.
> Set it explicitly on every dialogue generation. Check it twice.

### Reference image addressing

Reference images are addressed **inside the prompt text** as `图片1` … `图片7`,
which map positionally to the input names `image_1` … `image_7`. Use those tokens
literally. Plain English ("the first reference image", "@01") is not the
documented handle and there is no evidence it binds.

### Price, measured

**12 credits per second of output, flat, across all v3_0 tiers.**

| Output | Credits |
|---|---|
| 15s | 180 |
| 9s | 108 |
| 8s | 96 |

Duration was the only lever that moved the price in testing. Resolution did not
appear to. **There is no volume discount for one long generation**, which is why
the 3-shot cap in the failure log costs nothing to obey.

Budget arithmetic, as a worked example: an 8000-credit grant is about 666
seconds of output, roughly 44 takes at 15s. Grants expire — read the expiry off
`query_membership_and_credits` before planning a schedule around one.

Costing a full KIT pass, from the KIT's own shot durations and the 3-shot cap.
The KIT is 12 shots in three batches; splitting each batch at 3 shots gives
**five generations**, not one per batch:

| Chunk | Shots | Seconds | Credits |
|---|---|---|---|
| Batch 1 A | 1-3 | 3+2+3 = 8 | 96 |
| Batch 1 B | 4-5 | 4+3 (shot 5 trimmed to fit) = 7 | 84 |
| Batch 2 A | 1-3 | 3+3+3 (the 2.5s shot rounds to 3) = 9 | 108 |
| Batch 2 B | 4 | 3 | 36 |
| Batch 3 | 1-3 | 3+3+4 = 10 | 120 |
| **One take of everything** | 12 | **37** | **444** |

At the KIT's "3 takes of every batch" rule that is 15 jobs and **1332 credits for
one full pass**, about 17% of the grant. Re-rolls of individual chunks are the
same 12 credits per second, so the real budget question is how many chunks need a
fourth take, not how many passes you can afford.

---

## (d) Prompt construction on the MCP route

### d1. There is no global box and no per-shot stepper

The web UI has a separate setup box and a duration stepper per shot. **The MCP
has neither.** One prompt string carries everything. So:

1. Fold the GLOBAL SETUP BOX into the head of the prompt.
2. Write `Shot N (about Xs):` blocks.
3. **Repeat a compressed pin inside every shot block** — voice, "no music", "no
   subtitles", off-lens eyeline. State carried only at the head decays.
4. Kling allocates shot boundaries itself. Post trims to the beat map, so treat
   the durations as intent, not contract.
5. Durations are integers. Max total is 15s. The KIT's Batch 1 is specced at 16s
   (3+2+3+4+4), so Shot 5 went to 3s to fit. Batch 2 (11.5s) and Batch 3 (10s)
   fit as written; Batch 2's 2.5s shot becomes 3s.

### d2. The global setup box (paste verbatim, from KIT.md)

> Handheld camera throughout. No music, only SFX and natural ambience.
> No texts or subtitles on screen.
> The man in @01 is BOSS: mid-40s, navy suit, loosened dark tie, corporate
> lanyard, sweating, hoarse deep American baritone, corporate flat vowels.
> The woman in @02 is SOLO: early 30s, grey hoodie, messy bun, headphones round
> neck, mid-range slightly raspy American voice, fast talker, cracks under stress.
> Location per @09 location sheet and the scene stills. Small home kitchen,
> table under the window (Side A), doorway to hallway on Side B, counter and
> oven on Side C. Flat overcast daylight from the window.
> Characters never look into the lens — eyelines go to the other person,
> just off-camera.

Two corrections apply to that text on the current plan of record:

- Replace `@01`/`@02`/`@09` with `图片1`/`图片2`/… on the MCP route.
- **Do not include `@09`, the ABCD location sheet, as a reference at all** (see
  failure log item 4). Use a **peopled** scene still as the room anchor instead.
  "Flat overcast daylight" is v1; `script409.md` v2 is a night interior with one
  warm practical.

### d3. The three batches (KIT.md, verbatim structure)

**One generation = one voice.** This is the number-one fix for the v1-v5 voice
drift: all of his lines come out of one generation, all of hers out of another.

**BATCH 1 — all of HIS lines.** Uploads 01, 05, 06, 09. Start frame **06** (his
close-up).

- Shot 1 (3s): Medium-close, BOSS mid-room, bat resting on his shoulder, leaning
  toward SOLO off-frame left. Furious, bellowing, voice cracking: "YOU HAVE NO
  CREW. HOW DID YOU PAINT THE HOUSE?!" The subject stops talking, silence in the room.
- Shot 2 (2s): Close-up, BOSS roars, punching each word: "SHOW ME THE HANDBOOK."
  The subject stops talking, silence in the room.
- Shot 3 (3s): Medium, BOSS jabs a finger toward her off-frame, shouting:
  "A HUNDRED FENCE PANELS LAST WEEK. YOU HAVE NO CARPENTER!" The subject stops
  talking, silence in the room.
- Shot 4 (4s): Close-up, closest yet, veins out, screaming in bursts: "TEN
  MINUTE TURNAROUNDS. NO HELPERS. SHOW ME THE HANDBOOK!" The subject stops
  talking, silence in the room.
- Shot 5 (4s): Close-up. He freezes mid-rage, breath ragged, anger draining to
  confusion. A long pause. Then quietly, hoarse: "...whose." Another pause.
  Almost to himself: "...plan?" The bat lowers slowly out of frame. The subject
  stops talking, silence in the room.

**BATCH 2 — all of HER lines.** Uploads 02, 04, 07, 09. Start frame **07**.

- Shot 1 (3s): Medium-close, SOLO pressed back against the table, hands
  half-raised, frightened, talking fast to him off-frame right: "it— it's all
  written down— step by step—" The subject stops talking, silence in the room.
- Shot 2 (3s): Same setup, faster, voice breaking: "i just follow the pages—
  anyone could—" The subject stops talking, silence in the room.
- Shot 3 (2.5s): She squeezes her eyes shut and shouts as loud as she can:
  "IT'S IN A HANDBOOK!" Then opens her eyes, panting. The subject stops
  talking, silence in the room.
- Shot 4 (3s): Calmer, catching her breath, she says simply: "it's public." Then
  she turns the laptop around to face him off-frame. The subject stops talking,
  silence in the room.

**BATCH 3 — the three silent shots, one generation.** Uploads 01, 02, 04, 05,
08, 09.

- Shot 1 (3s): Wide per @04: SOLO alone at the table, typing, eating her
  sandwich. Ordinary afternoon. Ambient kitchen sound only.
- Shot 2 (3s): Wide per @05: BOSS storms in through the Side B doorway, bat
  waving overhead like a furious little-league coach; SOLO spins in her chair,
  startled. No dialogue.
- Shot 3 (4s): Wide per @08: BOSS now SITS at the table reading the laptop,
  scrolling once; SOLO stands behind him eating the sandwich; the bat lies flat
  on the table. Calm after the storm. Ambient only.

Note "The subject stops talking, silence in the room" after every line. That
sentence is load-bearing. See failure log item 5.

### d4. Worked prompt, assembled from the documented rules

The exact prompt strings sent on 7/28-29 were never written to the repo. This is
a reconstruction from KIT.md plus the MCP consequences above, not a transcript.
It is Batch 1 split into a 3-shot chunk, on the non-Omni route:

```
model: kling-video-v3_0
arguments:
  prompt: |
    Handheld camera throughout. No music, only SFX and natural ambience. No
    texts or subtitles on screen. The man in 图片1 is BOSS: mid-40s, navy suit,
    loosened dark tie, corporate lanyard, sweating, hoarse deep American
    baritone, corporate flat vowels. Small home kitchen matching 图片2, night,
    one warm practical. He never looks into the lens; his eyeline goes to the
    woman just off-camera to frame left.

    Shot 1 (about 3s): Medium-close, BOSS mid-room, leaning toward her off-frame
    left. Furious, bellowing, voice cracking: "YOU HAVE NO CREW. HOW DID YOU
    PAINT THE HOUSE?!" The subject stops talking, silence in the room. No music,
    no subtitles, eyeline off-lens.

    Shot 2 (about 2s): Close-up, BOSS roars, punching each word: "SHOW ME THE
    HANDBOOK." The subject stops talking, silence in the room. No music, no
    subtitles, eyeline off-lens.

    Shot 3 (about 3s): Medium, BOSS jabs a finger toward her off-frame,
    shouting: "A HUNDRED FENCE PANELS LAST WEEK. YOU HAVE NO CAR-PEN-TER!" The
    subject stops talking, silence in the room. No music, no subtitles, eyeline
    off-lens.
  duration: "8"
  aspect_ratio: "9:16"
  resolution: "1080p"
  imageCount: "1"
  enable_audio: "true"
inputs:
  - {name: image_1, inputType: URL, url: <boss close-up scene still>}
  - {name: image_2, inputType: URL, url: <peopled room anchor still>}
rationale: Batch 1 chunk A of ad 409, his first three lines, 3-shot cap.
```

`CAR-PEN-TER` is deliberate. See failure log item 6.

---

## (e) The cherry-pick checklist

**A human reviews and cherry-picks every take by eye and ear. Non-negotiable.** The rule
exists because every version shipped on metrics alone failed: mismatched TTS
voices, robotic delivery, homemade synth music. Metrics diagnose. They do not
clear.

Generate **3 takes of every batch**. Pick the best. Generate more only if all
three fail.

Reject a take if ANY of these fails:

1. **Face matches the character sheet** — the same person in every shot.
2. **Line delivered word-for-word** — no stretching ("shooow me the proooompts"
   is a reject), no invented words.
3. **The prop behaves** — the bat never vanishes mid-shot, never floats.
4. **Eyeline goes off-lens** toward the other character, never into camera.
5. **The room matches the stills** — same window, table, wallpaper.
6. **The last second is clean** — no morphing, no invented props.
7. **No burned-in text, no music in the audio.**

Run `check_takes.py` (section f) **before** a human looks at anything. It
mechanically covers 2, 6 and 7, plus two things the list does not name: scripted
pauses that got merged away, and a quiet beat that inherited the shouting
register. Items 1, 3, 4 and 5 still need eyes.

One more check that is not on the KIT list and should be: after a batch passes,
build a **room-consistency contact sheet** across the passing takes and confirm
the same window, curtains, table, splashback, plant, laptop, mug, sandwich and
doorway appear in all of them. Room drift was the failure mode two rounds before
the peopled-still anchor fixed it.

**Delivery of picks.** Download into `video/kling_picks/` named `b1_s1.mp4`,
`b1_s2.mp4`, `b2_s1.mp4`, `b3_s1.mp4` and so on. That directory does not exist in
the repo yet; create it. Nothing renames picks into the assembler's expected
filenames automatically, so either copy them into the clip pattern
(`gen/v409_<name>.mp4`) or point the assembler at the picks folder by overriding
`paths.clip` to `"kling_picks/{name}.mp4"`.

**Result URLs expire 24 hours after the job finishes. Download immediately.**

---

## (f) `check_takes.py` — the mechanical checker, generalised

Consolidates `video/check_take.py`. **What changed and why:** the original had a
hardcoded `EXPECTED` dict of ad-409 lines, a hardcoded `FILLER` set, a hardcoded
`HOMOPHONE` map and five magic numbers inline. All of it is now data in a JSON
file the operator writes. **No behaviour was dropped:**

| Original behaviour | Where it went |
|---|---|
| `EXPECTED` dict | `takes` object in the JSON, same key names (`lines`, `pause_after`, `quiet_after`) |
| `FILLER` set | `filler` array, defaulted to the original eleven words |
| `HOMOPHONE` map | `homophones` object, defaulted to the original `who's`/`whos` -> `whose` |
| register drop 4.0 dB, music gap 0.6s, music floor -28 dB, tail 0.15s, ±2.0/2.5/0.3s windows | `thresholds` object, defaults identical |
| `whisper.load_model("small.en")` | `whisper_model` key, default `small.en` |
| trailing bare take id (`check_take.py f.mp4 1C`) | preserved exactly, plus an explicit `--take-id` flag |
| filename inference on `_<id>_` | preserved as the first pass; a loose substring match was **added** as a second pass, and only fires when exactly one id matches, printing a notice |
| exit code = number of failures | unchanged |
| `spec["lines"]` (KeyError if absent) | `spec.get("lines", [])` | **an addition, not a merge.** A take entry with no `lines` no longer crashes; it now reports every spoken word as "not in the script", which is the right answer for an empty expectation |

Verified: the shipped `takes-409.json` below loads into semantics identical to
the original hardcoded `EXPECTED`, checked field by field.

```python
#!/usr/bin/env python3
"""Mechanically check a generated take before a human spends attention on it.

    python3 check_takes.py --expect takes.json kling_takes/v3_1C_carpenter.mp4 1C
    python3 check_takes.py --expect takes.json kling_takes/*.mp4   # ids auto-matched

Every failure this catches was found by ear in the 7/28 session, one take at a
time. The point is that none of them needed ears. Whisper knows whether the line
was said word-for-word; the audio envelope knows whether a scripted pause exists;
ffmpeg knows whether the register actually dropped. Only "is the performance
believable" needs a human, so only that should reach one.

Checks, mapped to the cherry-pick list:
  2. word-for-word     transcript vs the expected line, word by word
  -  scripted pauses   a gap the script demands must be measurably there
  -  register          a beat marked quiet must be quieter than the beat before
  7. no music          sustained tonal content under dialogue
  6. clean tail        no audio or motion cliff in the final 0.4s

Exit code is the number of failures, so it drops into a shell loop.

------------------------------------------------------------------------------
THE EXPECTATION FILE (this is the part you fill in)

Everything film-specific lives in a JSON file. Nothing about one ad is compiled
into this script. Minimum viable file:

    {
      "takes": {
        "1C": {
          "lines": ["a hundred fence panels last week you have no carpenter"],
          "pause_after": [["week", 0.25]]
        }
      }
    }

Keys inside "takes":
  lines        list of strings. What the SCRIPT says, lowercase, no punctuation.
               Derive these from the screenplay, never from what a take happened
               to produce - otherwise the checker ratifies the defect.
  pause_after  list of [word, seconds]. The beat map needs a real gap after that
               word and a merged delivery is a defect.
  quiet_after  a single word. Everything after it must measurably drop in level.

Optional top-level keys, all defaulted, override only if you must:
  whisper_model  default "small.en"
  filler         words too common to prove anything either way
  homophones     spelling collapses applied before comparison
  thresholds     the five numbers the checks compare against

Run with --write-template to drop a commented starter file next to your takes.
------------------------------------------------------------------------------
"""
import argparse
import json
import pathlib
import subprocess
import sys

DEFAULT_EXPECT = "takes.json"

# Words too common to prove anything either way. A missing "the" is not a defect
# and an extra "a" is not an invention, so neither should fail a take.
DEFAULT_FILLER = ["a", "the", "and", "it", "is", "i", "to", "of", "in", "you", "no"]

# Whisper picks spelling from context, so a homophone tells you nothing about
# what was actually said. "whose" vs "who's" is identical audio; the gap between
# it and the next word is the real discriminator, and that is checked separately.
# Only put genuine homophones here - anything that sounds different must fail.
DEFAULT_HOMOPHONE = {"who's": "whose", "whos": "whose"}

DEFAULT_THRESHOLDS = {
    # a beat marked quiet must drop at least this much against the beat before
    "register_drop_db": 4.0,
    # window used either side of the anchor word for that comparison
    "register_before_s": 2.0,
    "register_after_s": 2.5,
    "register_offset_s": 0.3,
    # only inter-word gaps longer than this are sampled for a music bed
    "music_gap_min_s": 0.6,
    # room tone sits below this; anything louder in a gap is probably music
    "music_floor_db": -28.0,
    # the last word must end at least this far from the cut or there is no
    # room to trim and the edit will clip it
    "tail_room_s": 0.15,
}

TEMPLATE = {
    "whisper_model": "small.en",
    "thresholds": DEFAULT_THRESHOLDS,
    "filler": DEFAULT_FILLER,
    "homophones": DEFAULT_HOMOPHONE,
    "takes": {
        "EXAMPLE_ID": {
            "lines": ["first line exactly as scripted",
                      "second line exactly as scripted"],
            "pause_after": [["scripted", 0.8]],
            "quiet_after": "scripted",
        }
    },
}


def load_spec(path: str) -> dict:
    """Read the expectation file and fill in every default."""
    with open(path) as fh:
        doc = json.load(fh)
    # Tolerate a bare mapping of take-id -> spec, which is what people write
    # first. A doc with no "takes" key and no known top-level key is one.
    if "takes" not in doc:
        doc = {"takes": doc}
    cfg = {
        "whisper_model": doc.get("whisper_model", "small.en"),
        "filler": {w.lower() for w in doc.get("filler", DEFAULT_FILLER)},
        "homophones": dict(doc.get("homophones", DEFAULT_HOMOPHONE)),
        "thresholds": {**DEFAULT_THRESHOLDS, **doc.get("thresholds", {})},
        "takes": doc["takes"],
    }
    return cfg


def sh(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def norm(w: str, homophones: dict) -> str:
    w = "".join(c for c in w.lower() if c.isalnum() or c == "'")
    return homophones.get(w, w)


def words_of(path: str, cfg: dict) -> list[dict]:
    import whisper
    m = whisper.load_model(cfg["whisper_model"])
    r = m.transcribe(path, language="en", word_timestamps=True, fp16=False)
    hp = cfg["homophones"]
    return [{"w": norm(w["word"], hp), "start": w["start"], "end": w["end"]}
            for s in r["segments"] for w in s["words"] if norm(w["word"], hp)]


def mean_db(path: str, start: float, dur: float) -> float:
    out = sh(["ffmpeg", "-hide_banner", "-ss", str(start), "-t", str(dur),
              "-i", path, "-af", "volumedetect", "-f", "null", "/dev/null"])
    for line in out.splitlines():
        if "mean_volume" in line:
            return float(line.split(":")[1].strip().split()[0])
    return -99.0


def check(path: str, take_id: str, cfg: dict) -> list[str]:
    spec = cfg["takes"].get(take_id)
    if not spec:
        return [f"no expectation defined for take id {take_id!r}"]

    th = cfg["thresholds"]
    hp = cfg["homophones"]
    filler = cfg["filler"]

    fails: list[str] = []
    words = words_of(path, cfg)
    said = [w["w"] for w in words]
    print(f"  transcript: {' '.join(said)}")

    # --- check 2: word-for-word -------------------------------------------
    want = [norm(w, hp) for line in spec.get("lines", []) for w in line.split()]
    missing = [w for w in want if w not in said and w not in filler]
    if missing:
        fails.append(f"words missing or mispronounced: {', '.join(missing)}")
    # a word the model invented that no line contains
    extra = [w for w in said if w not in want and w not in filler]
    if extra:
        fails.append(f"words not in the script: {', '.join(sorted(set(extra)))}")

    # --- scripted pauses ---------------------------------------------------
    for after, need in spec.get("pause_after", []):
        idx = next((i for i, w in enumerate(words) if w["w"] == norm(after, hp)), None)
        if idx is None or idx + 1 >= len(words):
            continue
        gap = words[idx + 1]["start"] - words[idx]["end"]
        if gap < need:
            fails.append(
                f"pause after {after!r} is {gap:.2f}s, script needs >={need:.2f}s "
                f"(delivered as one continuous phrase)")
        else:
            print(f"  pause after {after!r}: {gap:.2f}s  ok")

    # --- register: the quiet beat must actually be quieter ------------------
    anchor = spec.get("quiet_after")
    if anchor:
        idx = next((i for i, w in enumerate(words) if w["w"] == norm(anchor, hp)), None)
        if idx is not None:
            t = words[idx]["end"]
            before = mean_db(path, max(0, t - th["register_before_s"]),
                             th["register_before_s"])
            after = mean_db(path, t + th["register_offset_s"], th["register_after_s"])
            drop = before - after
            if drop < th["register_drop_db"]:
                fails.append(
                    f"no register change after {anchor!r}: {before:.1f} -> "
                    f"{after:.1f} dB ({drop:.1f} dB). Quiet beat inherited the shout.")
            else:
                print(f"  register drop after {anchor!r}: {drop:.1f} dB  ok")

    # --- check 7: no music -------------------------------------------------
    # Kling bakes music in unremovably when it does it at all. Music shows as a
    # loud floor during the gaps between words; room tone does not.
    gaps = [(words[i]["end"], words[i + 1]["start"] - words[i]["end"])
            for i in range(len(words) - 1)
            if words[i + 1]["start"] - words[i]["end"] > th["music_gap_min_s"]]
    if gaps:
        floors = [mean_db(path, s + 0.1, min(d - 0.2, 1.0)) for s, d in gaps]
        worst = max(floors)
        if worst > th["music_floor_db"]:
            fails.append(f"possible music bed: loudest inter-word gap is "
                         f"{worst:.1f} dB, expected room tone below "
                         f"{th['music_floor_db']:.0f} dB")
        else:
            print(f"  quietest-gap floor: {worst:.1f} dB  ok (no music bed)")

    # --- check 6: clean tail -----------------------------------------------
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True).stdout.strip())
    if words and dur - words[-1]["end"] < th["tail_room_s"]:
        fails.append(f"last word ends {dur - words[-1]['end']:.2f}s before the "
                     f"cut - no room to trim, will clip in the edit")

    return fails


def infer_id(path: str, takes: dict) -> str | None:
    """Take id from filename. `_<id>_` first because it cannot collide; a loose
    substring match second, and only when exactly one id matches."""
    name = pathlib.Path(path).name
    exact = [k for k in takes if f"_{k}_" in name]
    if len(exact) == 1:
        return exact[0]
    loose = [k for k in takes if k in name]
    if len(loose) == 1:
        print(f"  (id {loose[0]!r} inferred by loose match on the filename)")
        return loose[0]
    return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="take files, optionally followed by a take id")
    ap.add_argument("--expect", default=DEFAULT_EXPECT,
                    help=f"expectation JSON (default {DEFAULT_EXPECT})")
    ap.add_argument("--take-id", default=None,
                    help="force one take id for every path given")
    ap.add_argument("--write-template", metavar="PATH",
                    help="write a starter expectation file and exit")
    a = ap.parse_args(argv[1:])

    if a.write_template:
        with open(a.write_template, "w") as fh:
            json.dump(TEMPLATE, fh, indent=2)
        print(f"wrote {a.write_template} - fill in 'takes' from your script")
        return 0

    if not a.paths:
        print(__doc__)
        return 0

    cfg = load_spec(a.expect)
    paths = list(a.paths)
    take_id = a.take_id
    # trailing bare take id, as in: check_takes.py take.mp4 1C
    if take_id is None and paths[-1] in cfg["takes"]:
        take_id = paths.pop()

    total = 0
    for p in paths:
        tid = take_id or infer_id(p, cfg["takes"])
        print(f"\n{pathlib.Path(p).name}  [{tid or 'unknown'}]")
        if tid is None:
            print("  SKIP: cannot infer take id from filename")
            continue
        fails = check(p, tid, cfg)
        for f in fails:
            print(f"  FAIL  {f}")
        if not fails:
            print("  PASS  all mechanical checks")
        total += len(fails)
    print(f"\n{total} mechanical failure(s). Believability still needs a human.")
    return total


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

### `takes-409.json` — the shipped example (the v1 line set)

These are the lines the repo's takes were actually judged against. They match
`KIT.md` batches 1 and 2, not `script409.md` v2. Take ids `1A`/`1B`/`1C` are the
split chunks of Batch 1; `2A`/`2B` are the split chunks of Batch 2.

```json
{
  "whisper_model": "small.en",
  "takes": {
    "1A": {
      "lines": [
        "you have no crew how did you paint the house",
        "show me the handbook"
      ]
    },
    "1C": {
      "lines": ["a hundred fence panels last week you have no carpenter"],
      "pause_after": [["week", 0.25]]
    },
    "1B": {
      "_note": "The turn of the whole film: two broken fragments, not the question 'whose plan?'. A merged delivery reads as a different line entirely.",
      "lines": [
        "ten minute turnarounds",
        "no helpers",
        "show me the handbook",
        "whose",
        "plan"
      ],
      "pause_after": [["handbook", 0.8], ["whose", 0.8]],
      "quiet_after": "handbook"
    },
    "2A": {
      "lines": [
        "it's all written down step by step",
        "i just follow the pages anyone could"
      ]
    },
    "2B": {
      "lines": ["it's in a handbook", "it's public"],
      "quiet_after": "handbook"
    }
  }
}
```

For the v2 script, the equivalent table is:

```json
{
  "takes": {
    "s04": { "lines": ["who is doing all this work you don't have a team"] },
    "s05": { "lines": ["it's not just the tools you need the right method"] },
    "s06": { "lines": ["what method"] },
    "s07": { "lines": ["it plans the day checks the work fixes the mistakes"] },
    "s08": { "lines": ["show me the method"] },
    "s09": { "lines": ["it's all in a handbook"] },
    "s12": { "lines": ["you're not getting the handbook"] }
  }
}
```

No `pause_after` and no `quiet_after` entries: `script409.md` v2 deleted the
two-fragment beat that needed them, and specifies no other measurable pause.
Shot 9 is marked "flat, almost bored" against shot 8's full scream, so a
`quiet_after` on the shot-8 anchor would be defensible, but the script does not
state a threshold, so none is asserted here.

**Where the checker ran, historically.** The v3 batch cleared four of five:
1A (both his opening lines), 1C (full line restored, the hyphenated word clean,
1.14s scripted pause), 1B (the two quiet fragments 1.16s apart instead of
merged), 2A (both her lines end to end). 2B never cleared: the film's key
compound noun came back mis-transcribed a different way on each of four
attempts. Spend was stopped there because nobody could separate a real
articulation fault from whisper mishearing a shouted compound noun, and the ad
carries a hard caption on that line either way.

---

## (g) `assemble.py` — cut, treat, caption, insert, card, grade

Consolidates `video/assemble409.py` **and** `video/grade.py` into one file.
**What was merged and what had to be reconciled:**

| Original | In the consolidated file | Note |
|---|---|---|
| `grade.py` module, imported by `assemble409.py` as `from grade import chain` | inlined: `BASE_EQ`, `BASE_NOISE`, `SKIN_PULL`, `chain()`, plus `grade_run()`/`grade_compare()` | the import is gone; one file now, no dependency |
| `grade.py in.mp4 out.mp4 [--strong]` | `assemble.py grade in.mp4 out.mp4 [--strong]` | CLI preserved as a subcommand, not dropped |
| `grade.py --compare in.mp4 [--at T]` | `assemble.py grade in.mp4 --compare [--at T]` | same |
| `assemble409.py` run with no args | `assemble.py build [--config f.json]` | same default behaviour |
| module-level `CUT` list of 6-tuples | `CONFIG["cuts"]`, list of dicts with named keys | values byte-identical, verified programmatically |
| `MUSIC_STOP_IDX = 9` | `CONFIG["music"]["stop_index"]` | same index |
| `W, H, SR = 1080, 1920, 48000`, `-r 24`, crf 18/17 | `CONFIG["video"]` | same values |
| hardcoded `gen/v409_{name}.mp4` and `gen/{name}.jpg` | `CONFIG["paths"]["clip"]` / `["still"]` format strings | lets you point at `kling_picks/` |
| `if name == "s2": crop=756:1344:324:110` | per-cut optional `"crop"` key on that cut | the punch-in comment is preserved on the data |
| `if name.startswith("img:") or name == "s2k"` in the audio loop | `CONFIG["audio"]["skip_clips"] = ["s2k"]` | **`s2k` appears nowhere in `CUT`**; the guard was inert in the shipped file. Kept as data rather than deleted, because `gen/v409_s2k.mp4` exists and the intent was clearly "use this picture, never this audio" |
| `"img:c409_insert"` prefix convention | `{"still": "c409_insert"}` | same still, `gen/c409_insert.jpg` |
| card 2.4s hardcoded in two places | `CONFIG["card"]["duration"]`, used in both | see reconciliation below |
| 4:5 `crop=1080:1350:0:285` hardcoded | `CONFIG["outputs"]["ratios"]` | still cropped from the graded master so both ratios share one grade |
| music block ran unconditionally | wrapped in `if mu.get("bed") and mu.get("stop_index") is not None` | **an addition, not a merge.** The original would crash with no bed file; the v2 config ships with music off and needs the guard. Nothing is lost when a bed is present |

**Behaviour differences I had to reconcile, stated rather than buried:**

1. **The card is 2.4s in the code and 2.0s in `script409.md`.** The code value
   won, because it is what rendered. The v2 config below sets 2.0 to match the
   script; that config has never been run.
2. **The `s2k` guard was dead code.** Preserved as data. See table above.
3. **Caption text keeps its em dashes** (`IT'S ALL WRITTEN DOWN—`). Those
   characters are rendered pixels in the deliverable, not prose, so they are
   reproduced exactly. Do not "clean" them.
4. **The shipped cut map is the v1 line set.** 14 segments, 35.0s body, 37.4s
   total. `script409.md` v2 is 12 shots, 21.3s body. Both tables are given.
5. `room()` and `roomtone()` use fixed RNG seeds (4 and 9). Those are kept
   because the impulse response and the air bed must be identical across runs,
   or a re-render changes the sound of the film.

Verified before writing this section: the file compiles, `chain()` returns the
identical filter string, the built-in cut table matches the original tuple list
element for element, and `room()`/`roomtone()` run on synthetic input.

### Dependencies

`ffmpeg` and `ffprobe` on PATH, plus Python 3.10+ with `numpy`, `scipy`,
`Pillow`. `check_takes.py` additionally needs `openai-whisper`. Confirmed present
on the original build machine (macOS): ffmpeg and ffprobe under `/opt/homebrew/bin`, numpy 1.26.4,
scipy 1.17.1, pillow 12.1.1, whisper importable.

Asset files the script opens, which are not generated by it:

- `/System/Library/Fonts/SFNS.ttf` — macOS only. San Francisco carries the
  Condensed Heavy variation used for captions. On Linux, substitute a condensed
  grotesk and expect caption line breaks to move.
- a serif in `public/brand/` (e.g. Lora, SIL OFL, free download) — the card wordmark face. Does not ship with this kit.
- `public/brand/brand_mark.png` — the card mark (swap in your own).
- `audio/bed_phrygian.wav` — the music bed, the same one approved for the 405-408
  aerials.

```python
#!/usr/bin/env python3
"""Assemble a Kling dialogue film - J-cut edition, plus the grade/grain pass.

    python3 assemble.py build                      # the built-in 409 v5 config
    python3 assemble.py build --config 409v2.json  # any other cut
    python3 assemble.py grade in.mp4 out.mp4       # default look, standalone
    python3 assemble.py grade in.mp4 out.mp4 --strong   # for shiny close-ups
    python3 assemble.py grade in.mp4 --compare     # before/after stills pair

Video: concat of trimmed, captioned segments.
Audio: ONE timeline. Each clip's room-treated audio is placed at its segment's
start, but interrupters lead early (J-cut) and every clip keeps a breath tail
(L-cut). A continuous kitchen room-tone bed glues the cuts.

Everything film-specific is in CONFIG below, and every key can be overridden by
a JSON file passed to --config. The built-in values are the ones that actually
rendered out409_9x16.mp4 / out409_4x5.mp4.
"""
import argparse
import copy
import json
import os
import subprocess
import sys

import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
from PIL import Image, ImageDraw, ImageFont

# =========================================================================
# GRADE AND GRAIN - the realism step, done in code rather than prompts.
#
# Why this exists: AI video is mathematically clean, and clean is the tell. Real
# sensors add grain and real lenses do not deliver sculpted contrast. Knocking
# the contrast and saturation down and laying grain back on is the single
# biggest realism win available in post, and it costs one ffmpeg pass.
#
# A note on the skin fix. Premiere's HSL Secondary lets you eyedropper the shiny
# forehead and pull only that. ffmpeg has no eyedropper, so `--strong` uses
# selectivecolor on reds and yellows, which is where skin highlights live. It is
# blunter than the Premiere move and it is applied to the whole frame, so it is
# worth using only on tight faces where the shine actually reads.
#
# Values are a starting point, tuned by eye against the 405-408 aerials. Grain of
# 6/255 is about 2.4%, at the low end of the 3-8% the teardown calls for, because
# Kling output already carries some texture and stacking reads as noise.
# =========================================================================

# Contrast and saturation come DOWN: AI renders both too punchy, which is what
# makes skin look sculpted. gamma_r nudged up warms the midtones a touch, which
# suits the A24 look 409 is written for (warm but desaturated).
BASE_EQ = "eq=contrast=0.94:saturation=0.92:gamma_r=1.01"

# alls = strength, allf=t+u = temporal + uniform, so the grain moves between
# frames like real grain instead of sitting on the image like a static overlay.
BASE_NOISE = "noise=alls=6:allf=t+u"

# Blunt stand-in for an HSL-secondary skin pull: take saturation out of the reds
# and yellows where skin highlights live. Whole-frame, so tight faces only.
SKIN_PULL = "selectivecolor=reds=0 0 0 -0.12:yellows=0 0 0 -0.10"


def chain(strong: bool = False) -> str:
    """Return the -vf filter chain string."""
    parts = [BASE_EQ]
    if strong:
        parts.append(SKIN_PULL)
    parts.append(BASE_NOISE)
    return ",".join(parts)


def grade_run(src: str, dst: str, strong: bool = False, crf: int = 17) -> None:
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src,
           "-vf", chain(strong),
           "-c:v", "libx264", "-crf", str(crf), "-preset", "medium",
           "-pix_fmt", "yuv420p", "-c:a", "copy", dst]
    subprocess.run(cmd, check=True)
    print(f"graded {src} -> {dst}  ({'strong' if strong else 'base'})")


def grade_compare(src: str, at: float = 1.0) -> None:
    """Write before/after stills so the numbers can be judged by eye."""
    stem = src.rsplit(".", 1)[0]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(at), "-i", src,
                    "-frames:v", "1", "-q:v", "2", f"{stem}_before.jpg"], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(at), "-i", src,
                    "-frames:v", "1", "-vf", chain(), "-q:v", "2",
                    f"{stem}_after.jpg"], check=True)
    print(f"wrote {stem}_before.jpg and {stem}_after.jpg")


# =========================================================================
# CONFIG - the built-in 409 v5 cut. Override any key with --config file.json.
#
# A cut entry is one segment of the film:
#   clip   basename resolved through paths.clip  (a generated take)
#   still  basename resolved through paths.still (a frozen image insert)
#   in     seek into the source, seconds
#   dur    length on the timeline, seconds
#   lead   start this clip's AUDIO this much EARLY (J-cut, interrupters)
#   tail   keep the audio breathing this much PAST the cut (L-cut)
#   crop   optional ffmpeg crop applied before the scale, for a punch-in
#   caps   [[TEXT, in, out], ...] burned-in captions, times relative to the cut
# =========================================================================
CONFIG = {
    "video": {
        "width": 1080, "height": 1920, "fps": 24, "sample_rate": 48000,
        "crf_segment": 18, "crf_master": 17, "preset": "medium",
    },
    "paths": {
        "work": "tmp/409",
        "clip": "gen/v409_{name}.mp4",
        "still": "gen/{name}.jpg",
        # macOS system font. San Francisco carries a Condensed Heavy variation,
        # which is the caption weight. On Linux substitute a condensed grotesk.
        "caption_font": "/System/Library/Fonts/SFNS.ttf",
        "card_font": "public/brand/Lora-var.ttf",
        "card_mark": "public/brand/brand_mark.png",
    },
    "captions": {
        "size": 78, "min_size": 40, "max_width_frac": 0.92,
        "y_frac": 0.72, "stroke": 6, "weight": "Condensed Heavy",
    },
    "audio": {
        # fade the head and tail of every placed clip so overlaps blend
        # instead of clicking
        "fade_s": 0.12,
        "roomtone_gain": 0.14,
        "roomtone_seed": 9,
        "room_seed": 4,
        "peak_ceiling": 0.97,
        # clips whose picture is used but whose audio must never be placed.
        # s2k is the Kling alternate of the same beat; it was a hardcoded name
        # in the original assembler and is kept here as data.
        "skip_clips": ["s2k"],
    },
    "music": {
        # the approved aerial bed, low, looped, dead stop at "...WHOSE."
        "bed": "audio/bed_phrygian.wav",
        "stop_index": 9,
        "gain": 0.22,
        "fade_s": 0.25,
    },
    "card": {
        "duration": 2.4,
        "bg": [11, 11, 13],
        "title": "Example Brand",
        "title_size": 110,
        # Lora's variation is spelled SemiBold; the SF tagline weight below is
        # spelled Semibold. Font-specific, both verified against the shipped
        # files, do not "tidy" them into one spelling.
        "title_variation": "SemiBold",
        "mark_px": 96, "gap_px": 24, "y_frac": 0.44,
        "tag": "YOUR TAGLINE.",
        "tag_size": 46, "tag_weight": "Semibold",
        "tag_color": [210, 210, 215], "tag_offset_px": 170,
    },
    "outputs": {
        "master": "out409_9x16.mp4",
        "ratios": [
            # 4:5 is cropped from the graded master so both ratios share one grade
            {"file": "out409_4x5.mp4", "crop": "crop=1080:1350:0:285", "crf": 18},
        ],
    },
    "grade": {"strong": False},
    "cuts": [
        {"clip": "s1",  "in": 0.0, "dur": 1.8, "lead": 0.0,  "tail": 0.3, "caps": []},
        {"clip": "s2",  "in": 0.0, "dur": 3.0, "lead": 0.2,  "tail": 0.4,
         # single: punch in on him, empty chair leaves frame
         "crop": "crop=756:1344:324:110",
         "caps": [["YOU HAVE NO CREW.", 0.3, 1.6],
                  ["HOW DID YOU PAINT THE HOUSE?", 1.6, 3.0]]},
        {"clip": "s3",  "in": 0.0, "dur": 3.2, "lead": 0.0,  "tail": 0.5,
         "caps": [["IT'S ALL WRITTEN DOWN—", 0.3, 1.8],
                  ["STEP BY STEP—", 1.8, 3.2]]},
        {"clip": "s4",  "in": 0.0, "dur": 2.4, "lead": 0.35, "tail": 0.4,
         "caps": [["SHOW ME THE HANDBOOK.", 0.2, 2.4]]},
        {"clip": "s5b", "in": 0.0, "dur": 3.6, "lead": 0.0,  "tail": 0.4,
         "caps": [["A HUNDRED FENCE PANELS LAST WEEK.", 0.2, 1.9],
                  ["YOU HAVE NO CARPENTER!", 1.9, 3.6]]},
        {"clip": "s6",  "in": 0.0, "dur": 2.6, "lead": 0.0,  "tail": 0.5,
         "caps": [["I JUST FOLLOW THE PAGES—", 0.2, 1.5],
                  ["ANYONE COULD—", 1.5, 2.6]]},
        {"clip": "s8",  "in": 0.0, "dur": 2.8, "lead": 0.35, "tail": 0.0,
         "caps": [["TEN MINUTE TURNAROUNDS.", 0.2, 1.5],
                  ["NO HELPERS.", 1.5, 2.8]]},
        {"clip": "s4",  "in": 0.0, "dur": 2.2, "lead": 0.0,  "tail": 0.3,
         "caps": [["SHOW ME THE HANDBOOK!", 0.15, 2.2]]},   # clean repeat
        {"clip": "s9",  "in": 0.0, "dur": 2.4, "lead": 0.3,  "tail": 0.4,
         "caps": [["IT'S IN A HANDBOOK!", 0.2, 2.2]]},
        {"clip": "s10", "in": 0.0, "dur": 2.2, "lead": 0.0,  "tail": 0.3,
         "caps": [["...WHOSE.", 0.4, 2.0]]},
        {"clip": "s11", "in": 0.0, "dur": 2.0, "lead": 0.0,  "tail": 0.4,
         "caps": [["IT'S PUBLIC.", 0.3, 1.8]]},
        {"still": "c409_insert", "dur": 1.5, "caps": []},   # the end-screen insert
        {"clip": "s10", "in": 3.7, "dur": 1.9, "lead": 0.0, "tail": 0.3,
         "caps": [["...PLAN?", 0.6, 1.9]]},
        {"clip": "s12", "in": 0.0, "dur": 3.4, "lead": 0.0, "tail": 0.0, "caps": []},
    ],
}


def merge(base: dict, over: dict) -> dict:
    """Recursive dict merge. Lists replace wholesale - a partial cut list is
    never what anyone means."""
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(path: str | None) -> dict:
    if not path:
        return copy.deepcopy(CONFIG)
    with open(path) as fh:
        return merge(CONFIG, json.load(fh))


def font(path: str, size: int, weight: str):
    f = ImageFont.truetype(path, size)
    for w_ in (weight, "Heavy"):
        try:
            f.set_variation_by_name(w_)
            break
        except Exception:
            continue
    return f


def cap_png(cfg: dict, text: str, path: str) -> str:
    v, c = cfg["video"], cfg["captions"]
    W, H = v["width"], v["height"]
    size = c["size"]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fnt = font(cfg["paths"]["caption_font"], size, c["weight"])
    while d.textlength(text, font=fnt) > W * c["max_width_frac"] and size > c["min_size"]:
        size -= 3
        fnt = font(cfg["paths"]["caption_font"], size, c["weight"])
    x = (W - d.textlength(text, font=fnt)) / 2
    d.text((x, int(H * c["y_frac"])), text, font=fnt, fill=(255, 255, 255, 255),
           stroke_width=c["stroke"], stroke_fill=(0, 0, 0, 240))
    img.save(path)
    return path


def room(x, SR: int, seed: int):
    """Small-kitchen convolution + tilt EQ on a float32 mono signal.

    Pasted or dry audio reads as dubbed. Measured against the reference:
    reverb index 0.93 (reference) vs 0.56 (ours, dry), spectral centroid
    597Hz vs 860Hz. RT60 around 350ms plus a high-shelf cut above 3.8kHz
    closes most of that gap.
    """
    rng = np.random.default_rng(seed)
    ir = np.zeros(int(0.45 * SR), dtype=np.float32)
    ir[0] = 1.0
    for dl, g in [(0.009, 0.5), (0.013, 0.42), (0.021, 0.36), (0.029, 0.3),
                  (0.041, 0.24), (0.055, 0.18), (0.07, 0.13)]:
        ir[int(dl * SR)] += g
    tail = rng.standard_normal(len(ir)).astype(np.float32)
    t = np.arange(len(ir)) / SR
    tail *= np.exp(-t / 0.085)
    b, a = sig.butter(2, 3600 / (SR / 2), btype="low")
    tail = sig.lfilter(b, a, tail).astype(np.float32)
    ir += 0.45 * tail
    ir /= np.abs(ir).max()
    wet = sig.fftconvolve(x, ir)[:len(x)].astype(np.float32)
    mix = 0.55 * x + 0.45 * wet
    b, a = sig.butter(2, 3800 / (SR / 2), btype="high")
    mix = mix - 0.5 * sig.lfilter(b, a, mix)
    return mix


def roomtone(n: int, SR: int, seed: int, gain: float):
    """One continuous bed of kitchen air. This is what turns a row of clips
    into a scene instead of a slideshow."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n).astype(np.float32)
    b, a = sig.butter(2, [30 / (SR / 2), 260 / (SR / 2)], btype="band")
    low = sig.lfilter(b, a, z) * 0.09
    b, a = sig.butter(2, [900 / (SR / 2), 5200 / (SR / 2)], btype="band")
    air = sig.lfilter(b, a, rng.standard_normal(n).astype(np.float32)) * 0.012
    t = (low + air)
    t /= np.abs(t).max()
    return t * gain


def build(cfg: dict) -> None:
    v = cfg["video"]
    W, H, SR, FPS = v["width"], v["height"], v["sample_rate"], v["fps"]
    work = cfg["paths"]["work"]
    os.makedirs(work, exist_ok=True)

    parts, starts, cursor = [], [], 0.0

    # ---- picture: one captioned segment per cut --------------------------
    for idx, cut in enumerate(cfg["cuts"]):
        seg = f"{work}/seg_{idx:02d}.mp4"
        dur = cut["dur"]
        if "still" in cut:
            still = cfg["paths"]["still"].format(name=cut["still"])
            # -loop 1 is mandatory on still overlays: without a timeline the
            # enable/fade expressions see nothing and the overlay is invisible.
            inputs = ["-loop", "1", "-t", str(dur), "-i", still]
        else:
            src = cfg["paths"]["clip"].format(name=cut["clip"])
            inputs = ["-ss", str(cut.get("in", 0.0)), "-t", str(dur), "-i", src]

        pre = f"{cut['crop']}," if cut.get("crop") else ""
        filt = [f"[0:v]{pre}scale={W}:{H},setsar=1[base]"]
        prev = "base"
        for i, (txt, s, e) in enumerate(cut.get("caps", [])):
            p = cap_png(cfg, txt, f"{work}/c{idx:02d}_{i}.png")
            inputs += ["-loop", "1", "-i", p]
            filt.append(f"[{prev}][{i+1}:v]overlay=0:0:enable='between(t,{s},{e})'[o{i}]")
            prev = f"o{i}"

        subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs +
                       ["-filter_complex", ";".join(filt), "-map", f"[{prev}]", "-an",
                        # output-side -t caps the segment; without it a looped
                        # still runs forever
                        "-t", str(dur), "-c:v", "libx264", "-crf", str(v["crf_segment"]),
                        "-preset", v["preset"], "-pix_fmt", "yuv420p",
                        "-r", str(FPS), seg], check=True)
        parts.append(seg)
        starts.append(cursor)
        cursor += dur
        print("seg", idx, cut.get("clip") or cut.get("still"), flush=True)

    body_dur = cursor

    # ---- end card ---------------------------------------------------------
    cd = cfg["card"]
    card = Image.new("RGB", (W, H), tuple(cd["bg"]))
    d = ImageDraw.Draw(card)
    lf = ImageFont.truetype(cfg["paths"]["card_font"], cd["title_size"])
    try:
        lf.set_variation_by_name(cd["title_variation"])
    except Exception:
        pass
    mark = Image.open(cfg["paths"]["card_mark"]).convert("RGBA").resize(
        (cd["mark_px"], cd["mark_px"]), Image.LANCZOS)
    tw = d.textlength(cd["title"], font=lf)
    lx = (W - (cd["mark_px"] + cd["gap_px"] + tw)) / 2
    ly = int(H * cd["y_frac"])
    card.paste(mark, (int(lx), int(ly + 10)), mark)
    d.text((lx + cd["mark_px"] + cd["gap_px"], ly), cd["title"], font=lf,
           fill=(255, 255, 255))
    sf2 = font(cfg["paths"]["caption_font"], cd["tag_size"], cd["tag_weight"])
    tag = cd["tag"]
    d.text(((W - d.textlength(tag, font=sf2)) / 2, ly + cd["tag_offset_px"]), tag,
           font=sf2, fill=tuple(cd["tag_color"]))
    card.save(f"{work}/card.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1",
                    "-i", f"{work}/card.png", "-t", str(cd["duration"]),
                    "-r", str(FPS), "-c:v", "libx264", "-crf", str(v["crf_segment"]),
                    "-preset", v["preset"], "-pix_fmt", "yuv420p",
                    f"{work}/seg_card.mp4"], check=True)
    parts.append(f"{work}/seg_card.mp4")

    with open(f"{work}/list.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.basename(p)}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", f"{work}/list.txt", "-c:v", "libx264",
                    "-crf", str(v["crf_segment"]), "-preset", v["preset"],
                    "-pix_fmt", "yuv420p", "-r", str(FPS),
                    f"{work}/video.mp4"], check=True)

    # ---- single audio timeline -------------------------------------------
    au = cfg["audio"]
    total = body_dur + cd["duration"]
    N = int(total * SR)
    bus = roomtone(N, SR, au["roomtone_seed"], au["roomtone_gain"])

    for cut, t0 in zip(cfg["cuts"], starts):
        name = cut.get("clip")
        if name is None or name in au["skip_clips"]:
            continue
        inp = cut.get("in", 0.0)
        dur = cut["dur"]
        lead = cut.get("lead", 0.0)
        tailx = cut.get("tail", 0.0)
        raw = f"{work}/a_{name}_{t0:.1f}.wav"
        a_in = max(0.0, inp - lead)
        a_dur = (inp - a_in) + dur + tailx
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(a_in),
                            "-t", str(a_dur), "-i", cfg["paths"]["clip"].format(name=name),
                            "-vn", "-ac", "1", "-ar", str(SR), raw])
        if r.returncode != 0:
            continue      # a silent take has no audio stream; that is allowed
        sr_, x = wav.read(raw)
        x = x.astype(np.float32) / 32768.0
        if x.ndim > 1:
            x = x.mean(1)
        x = room(x, SR, au["room_seed"])
        # fade edges so overlaps blend instead of clicking
        f_n = int(au["fade_s"] * SR)
        env = np.ones(len(x), dtype=np.float32)
        env[:f_n] = np.linspace(0, 1, f_n)
        env[-f_n:] = np.linspace(1, 0, f_n)
        x *= env
        p0 = int((t0 - (inp - a_in)) * SR)
        p0 = max(0, p0)
        p1 = min(N, p0 + len(x))
        bus[p0:p1] += x[:p1 - p0]
        print("audio", name, f"@{t0 - (inp - a_in):.2f}s", flush=True)

    # ---- music: low, looped, dead stop on the deflation beat --------------
    mu = cfg["music"]
    if mu.get("bed") and mu.get("stop_index") is not None:
        stop = starts[mu["stop_index"]]
        mn = int(stop * SR)
        msr, m = wav.read(mu["bed"])
        m = m.astype(np.float32) / 32768.0
        if m.ndim > 1:
            m = m.mean(1)
        if msr != SR:
            import scipy.signal as _sg
            m = _sg.resample(m, int(len(m) * SR / msr)).astype(np.float32)
        reps = int(np.ceil(mn / len(m)))
        m = np.tile(m, reps)[:mn]
        fade = int(mu["fade_s"] * SR)
        m[-fade:] *= np.linspace(1, 0, fade)
        bus[:mn] += mu["gain"] * m

    peak = np.abs(bus).max()
    if peak > au["peak_ceiling"]:
        bus *= au["peak_ceiling"] / peak
    wav.write(f"{work}/bus.wav", SR, (bus * 32767).astype(np.int16))

    # Mux the audio bus onto the cut, and grade in the same pass. The grade is
    # the realism step (contrast/saturation down, grain back on). It has to
    # re-encode video, so it cannot be a stream copy like it was.
    master = cfg["outputs"]["master"]
    vf = chain(cfg["grade"]["strong"])
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{work}/video.mp4",
                    "-i", f"{work}/bus.wav", "-map", "0:v", "-map", "1:a",
                    "-vf", vf,
                    "-c:v", "libx264", "-crf", str(v["crf_master"]),
                    "-preset", v["preset"], "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest",
                    master], check=True)

    for r in cfg["outputs"]["ratios"]:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", master,
                        "-vf", r["crop"], "-c:v", "libx264", "-crf", str(r["crf"]),
                        "-preset", v["preset"], "-pix_fmt", "yuv420p",
                        "-c:a", "copy", r["file"]], check=True)

    print(f"ASSEMBLED body={body_dur:.1f}s total={total:.1f}s graded={vf}", flush=True)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="cut, treat, caption, card, grade, both ratios")
    b.add_argument("--config", help="JSON overriding any key of CONFIG")

    g = sub.add_parser("grade", help="the grade/grain pass on its own")
    g.add_argument("src")
    g.add_argument("dst", nargs="?")
    g.add_argument("--strong", action="store_true",
                   help="add the blunt skin-highlight pull, for tight faces")
    g.add_argument("--compare", action="store_true",
                   help="write before/after stills instead of a video")
    g.add_argument("--at", type=float, default=1.0, help="timestamp for --compare")

    a = ap.parse_args(argv[1:])

    if a.cmd == "build":
        build(load_config(a.config))
        return 0

    if a.compare:
        grade_compare(a.src, a.at)
        return 0
    if not a.dst:
        ap.error("dst required unless --compare")
    grade_run(a.src, a.dst, a.strong)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

### The v2 beat map as a config

Derived from `script409.md` v2 shot durations. **Never run.** Body 21.3s, card
2.0s, total 23.3s, verified by loading it through `load_config`. Two things in it
are assumptions, marked here rather than hidden: caption in/out times (the script
names the caption text for shots 2, 3, 9 and 12 but no timings, so each runs the
full shot), and the J-cut lead/tail values (all zero; the script specifies none).

```json
{
  "paths": {
    "work": "tmp/409v2",
    "clip": "gen/409v2_{name}.mp4",
    "still": "gen/{name}.jpg"
  },
  "music": { "bed": null, "stop_index": null },
  "card": { "duration": 2.0 },
  "outputs": {
    "master": "out409v2_9x16.mp4",
    "ratios": [
      { "file": "out409v2_4x5.mp4", "crop": "crop=1080:1350:0:285", "crf": 18 }
    ]
  },
  "cuts": [
    { "clip": "s01_approach",   "in": 0.0, "dur": 1.4, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "clip": "s02_break",      "in": 0.0, "dur": 0.6, "lead": 0.0, "tail": 0.0,
      "caps": [["WHO", 0.0, 0.6]] },
    { "clip": "s03_reveal",     "in": 0.0, "dur": 1.2, "lead": 0.0, "tail": 0.0,
      "caps": [["IS DOING ALL THIS WORK", 0.0, 1.2]] },
    { "clip": "s04_accusation", "in": 0.0, "dur": 3.4, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "clip": "s05_answer1",    "in": 0.0, "dur": 2.9, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "clip": "s06_press",      "in": 0.0, "dur": 1.9, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "clip": "s07_answer2",    "in": 0.0, "dur": 2.8, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "clip": "s08_demand",     "in": 0.0, "dur": 1.0, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "clip": "s09_name",       "in": 0.0, "dur": 0.9, "lead": 0.0, "tail": 0.0,
      "caps": [["IT'S ALL IN A HANDBOOK", 0.0, 0.9]] },
    { "clip": "s10_stop",       "in": 0.0, "dur": 2.3, "lead": 0.0, "tail": 0.0, "caps": [] },
    { "still": "c409v2_asset",  "dur": 0.5, "caps": [] },
    { "clip": "s12_reversal",   "in": 0.0, "dur": 2.4, "lead": 0.0, "tail": 0.0,
      "caps": [["YOU'RE NOT GETTING THE HANDBOOK", 0.0, 2.4]] }
  ]
}
```

Model routing for that map, from the script: **Seedance 2.0** takes shots 1, 2, 3
and 10 (the approach, the door break, the wides). **Kling 3.0** takes shots 4-9
and 12 (faces, dialogue, emotion). Shot 11 is a still with minimal motion,
generated as an image and animated lightly. v1 put the door break on Kling, which
was the wrong tool for the only real action beat in the film.

### What the audio timeline is doing, in words

- Every clip's audio is extracted mono at 48kHz, run through `room()`, faded
  0.12s at each end, and summed into one bus that already contains a continuous
  `roomtone()` bed.
- `lead` places a clip's audio **early**, so an interrupter is heard before you
  see him. That is the J-cut. `tail` lets the previous clip's breath run past the
  picture cut. That is the L-cut. Together with the continuous bed they are what
  makes a row of separate generations read as one room instead of a slideshow.
- `room()` is a synthetic impulse: a direct hit, seven early reflections between
  9ms and 70ms, and a noise tail with an 85ms decay constant low-passed at
  3.6kHz, mixed 55% dry / 45% wet, then a tilt EQ that subtracts half of
  everything above 3.8kHz. That is the "small kitchen, RT60 about 350ms" recipe.
- The music bed starts at zero, loops, and **stops dead** at the deflation beat
  rather than fading through it.
- Peak ceiling 0.97, then int16.

---

## (h) The failure log. Read this before spending a credit.

**1. Cap a generation at about 3 shots.** Not a style preference, a defect
threshold.

**2. Five shots in 15s garbles dialogue.** Both 15s/5-shot takes came back with
soft lip sync, and take 1 inserted an extra consonant into the middle of a
three-syllable word. Shot 3 of that
take had 11 shouted syllables in 3.0 seconds. Splitting the batch fixes it, and
splitting is also **cheaper**, not just better, because pricing is flat per
second.

**3. Kling ignores the shot plan under load.** Same two takes: take 1 gave shot 4
five seconds and starved shot 5 to 0.9 seconds. Take 2 never cut to shot 5 at all
and ran 7.1 seconds continuous. You cannot fix this with wording. Split the
batch, and keep the same `first_image` across the halves so the face and the
voice stay matched.

**4. The location sheet rendered as a shot.** Take 1 of Batch 1 turned its final
0.9s into a **top-down drone view of a woman lifting a chair over her head**:
wrong character, wrong angle, wrong scene. Root cause: the ABCD location sheet
was passed to Omni as a reference image, and Omni is artifact-prone when
overloaded with references, exactly as the reference teardown material warns.
**Do not feed the ABCD location sheet to Omni.** For single-character dialogue
use non-Omni `kling-video-v3_0` with the scene still as `first_image`. It also
renders in half the time (6 min vs 13). The replacement that worked was a
**peopled** scene still as the room anchor: the contact sheet across takes 1A,
1C, 1B and 2A confirmed the same window, curtains, table, splashback, plant,
laptop, mug, sandwich and doorway. Removing the sheet with nothing in its place
was itself a failure two rounds earlier.

**5. Write the silence as an instruction, and pin the register.** A quiet beat
that follows a shouting beat **inherits the shouting** unless you say so
explicitly. Working phrasings, all in the prompts: "he never raises his voice in
this shot", "he does not speak for a long moment", "a second long silence", and
KIT.md's per-line tag "The subject stops talking, silence in the room."

**6. Hyphenate any word the model garbles.** Writing the word into the prompt
with syllable hyphens (`CAR-PEN-TER` in the worked prompt above) forces syllable
separation, and it fixed the first garbled word on the next take. The film's key
compound noun resisted four attempts anyway and drifted a different way each
time, converging toward the right word but still one consonant off. Spend was
stopped there. The ad carries a hard burned-in caption on that line, so the word
is insured visually either way. That is also why `script409.md` says the
captions exist partly to insure that word.

**7. Pricing is 12 credits per second of output**, flat across all v3_0 tiers.
15s = 180, 9s = 108, 8s = 96. Duration was the only lever that moved price in
testing. **There is no discount for one long generation**, so the shot-splitting
rule costs nothing and saves money.

**8. Result URLs expire 24 hours after the job finishes. Download immediately.**
There is no second chance and the credits are already spent. Batch 1 take 1
(180 credits, 8000 -> 7820) is the on-record example.

**9. `query_tasks` is badly stale. Do not diagnose a hang from it.** Measured
three times on 7/29:

- A finished image job reported `QUEUING` for about 8 minutes after completing in
  106 seconds.
- A 58-second job reported `RUNNING` for about 14 minutes.
- `finishTime` is set early and is meaningless while status is not `COMPLETED`.
  A FAILED job showed a `finishTime` 5 seconds after its `createTime`.
- The credits endpoint also appears cached: the balance did not move across a
  70-credit charge.

Practical rule: poll on 5-minute-plus intervals, expect long lag, and **never
switch models or resubmit because a job "looks stuck."** A model swap was nearly
wasted on a phantom hang.

### Adjacent failures from the same run, same cost

**10. From-behind shots must not get a face sheet.** 18 credits wasted. Passing a
character sheet, which is mostly face panels, while demanding a shot where the
face is invisible makes the model resolve the contradiction by rendering the face
somewhere else: a duplicate second man, or a literal shadow-figure on the wall.
Three Kling rolls failed this way. The fix that worked first try: drop the
character sheet entirely for from-behind framings, let wardrobe description carry
identity, and use GPT Image 2 for precision instruction following. **Rule: face
sheet only when the face is visible in the shot.**

**11. Gemini image models reject identity-matching prompts.** Part B (a side
profile from an approved portrait) failed on `gemini-3.1-flash-image` in 5
seconds with no error text. That is a policy rejection, almost certainly a
likeness filter tripped by prompt language demanding "the SAME man, identical
person, same bone structure" from a supplied photo. `kling-image-v3_0_omni` ran
the identical intent fine. **Rule: any reference-consistency work goes to Kling's
own image models.** Failed jobs appear to be refunded; the balance did not move.

**12. Kling renders "broken white door debris" as shattered china or glass** no
matter how it is negative-prompted. Five failures. Remove the debris concept from
the prompt, or edit it out afterwards with `kling-image-o1`, which is 2 credits,
surgical, and worked first try.

**13. Contact sheets of alternatives read as storyboards to a reviewer.** Stamp
options as options, sequences as `CLIP N START`, and never mix the two in one
strip.

**14. Study the reference frame by frame before building any sequence still.**
Human review caught three physics errors (bat versus door, no forward
progression, raised bat while walking) that a 0.1s-step ffmpeg extraction
settles in minutes. Build the extraction sheet first and keep it next to the
reference.

**15. Never ship audio no human has heard.** Every unheard version failed:
mismatched TTS voices, robotic delivery, homemade synth music. Metrics (reverb
index, spectral centroid, HF/LF balance) diagnose but do not clear. Related:
whisper hallucinates, notably "I don't care" loops, on music-only spans. Probe
specific regions; do not trust a full-pass timestamp list.

**16. ffmpeg traps that bit this pipeline.** `-loop 1` is mandatory on still
overlays, otherwise the fade sees no timeline and the overlay is invisible.
Re-encode hybrids: a stream-copy mux with mismatched streams produces a runaway
render. Cap segments with an output-side `-t`.

**17. EDIT the reference's actual frame. Never recreate it.** This is the newest
rule in the sources (7/30) and it is labelled there as the method that finally
worked. Recreation re-imagines the pose and re-rolls the physics every time: six
drifting attempts. The chain that landed the door-burst still was a **gpt-image-2
EDIT of the reference frame** — pose kept at pixel level, face, wardrobe and room
swapped — then a **`kling-image-o1` surgical background fix, 2 credits**. Locked
as `SETUP_D_BURST_FINAL.png` (his exact physics, our man, dark corridor behind so
it reads as breaking IN) plus `SETUP_D_APPROACH_WIDE.png` (bonus wide with
door-seam glow). Corollary that qualifies item 10: **face visible means the face
sheet IS allowed in the edit call.** The ban is on face sheets for from-behind
framings, not on face sheets generally.

**18. One line per shot.** Putting two lines in one shot block makes Kling
swallow the whole sentence. This was one of the three fixes that turned the v3
batch from failing into four-of-five passing.

**19. Cap the foreground shoulder at a quarter of the frame.** In an
over-the-shoulder, an uncapped foreground shoulder ate the speaker entirely in
the previous version. Same v3 fix set.

**20. Build dialogue films from SINGLES.** One readable face per frame,
performance played to just-off-lens. Two-shots only when the faces are small
(wides, the reversal). The sources call this the reference's core engineering,
not a style preference, and it is why the KIT is built as "all of his lines in
one generation, all of hers in another."

**21. Generate the location sheet FROM a peopled still.** Models render empty
rooms unrealistically. Same reason the peopled scene still beat the ABCD sheet as
a room anchor in item 4. For character sheets: front / three-quarter / profile on
white, and demand **"PHOTOGRAPH, not illustration"** — nano-banana sometimes
returns drawings for male subjects.

**22. Checkpoint one shot end to end before batching. Report spend at the
checkpoint. Decide the stop-loss in advance.** This is what actually happened
with 409: Batch 1 take 1 went out, then everything stopped for a human eye and
ear before Batches 2-3. The instruction in the sources is literal — **do not
batch ahead.**

**23. Compliance, standing.** The ad-platform rejection risk this film carries
(the bat and the implied violence) was weighed and explicitly accepted by the
decision-maker in advance. Record decisions like that; once made, do not re-open
them or quietly soften the creative to avoid the risk.

---

## (i) File map for this section

| Path | What it is |
|---|---|
| `video/kling_kit/KIT.md` | the run sheet: setup box, 3 batches, cherry-pick list, delivery |
| `video/kling_kit/01_character_sheet_HIM.jpg` | BOSS character sheet |
| `video/kling_kit/02_character_sheet_HER.jpg` | SOLO character sheet |
| `video/kling_kit/03_scene_still_empty_kitchen.jpg` | kitchen plate |
| `video/kling_kit/04_scene_still_her_at_table.jpg` | wide, her at the table |
| `video/kling_kit/05_scene_still_entrance_both.jpg` | wide, his entrance |
| `video/kling_kit/06_scene_still_him_closeup.jpg` | his close-up, Batch 1 start frame |
| `video/kling_kit/07_scene_still_her_closeup.jpg` | her close-up, Batch 2 start frame |
| `video/kling_kit/08_scene_still_reversal.jpg` | wide, the reversal |
| `video/kling_kit/09_location_sheet_ABCD.jpg` | the ABCD location sheet. **Do not feed to Omni** |
| `video/kling_kit/10_end_screen_insert.jpg` | the end-screen product insert |
| `video/script409.md` | plan of record: shots, setups, model routing, captions, audio, post |
| `video/check_take.py` | original checker, hardcoded to 409 |
| `video/assemble409.py` | original assembler, hardcoded to the v5 cut |
| `video/grade.py` | original grade pass, imported by the assembler |
| `video/gen/v409_*.mp4` | the v5-era clips the shipped cut map references |
| `video/gen/c409_insert.jpg` | the end-screen still used by the cut map |
| `video/gen/v2_sheets/` | stage 2-3 approved stills, gitignored, local only |
| `video/kling_takes/` | raw Kling takes plus per-take contact sheets |
| `video/audio/bed_phrygian.wav` | the music bed |
| `video/public/brand/` | Lora-var.ttf, brand_mark.png |
| `video/out409_9x16.mp4`, `out409_4x5.mp4` | the v5 prototype, not shippable |
| `video/kling_picks/` | **does not exist yet.** Create it for cherry-picked takes |

Approved stills in `video/gen/v2_sheets/`, checked against the directory as it
actually stands (the `_FINAL` suffix is the marker for a locked asset):

- **Character sheets:** `BOSS_SHEET_FINAL`, `HER_SHEET_FINAL`,
  `HER_PORTRAIT_FINAL`, `HER_PROFILE_FINAL`, `boss_portraitA` (Part A, approved),
  `boss_profile_FINAL`.
- **Room:** `BASE_IMAGE_FINAL`, `LOCATION_SHEET_FINAL` (ABCD, door on Side B
  hinged far side, swings into the room).
- **Setups:** `SETUP_A_FINAL` (low angle, bat overhead), `SETUP_B_FINAL` (her
  close-up, eyeline to his shoulder), `SETUP_E_FINAL` (laptop detail).
- **The door beat:** `SETUP_D_BURST_FINAL` is the **locked** burst still, from
  the edit-not-recreate chain in failure-log item 17. `SETUP_D_APPROACH_WIDE` is
  the bonus wide. `SETUP_D_BURST_START` and `SETUP_D_CLIP1_START` /
  `SETUP_D_CLIP2_START` are the earlier recreation-era stills and are superseded
  by `SETUP_D_BURST_FINAL` — do not pick one of those by name-matching.
- Also kept: `shoulder_1`, a glow-door cold open the reviewer liked as an
  optional pre-beat.

The directory holds roughly 95 files; everything without `_FINAL` is a candidate,
a comparison strip, or a dead roll. `v2_sheets/README.md` is the index and it
carries the acceptance test that matters: Part B is not judged on "does it look
good", it is judged on **does the tone match Part A**, measured with PIL
`ImageStat` rather than eyeballed, because drift between front and side is
inherited by every video generation downstream.

`SETUP_E_FINAL` carries a rule: the laptop screen gets the **real product
screenshot corner-pinned in post**. Never trust model-rendered UI text.

---

## OPEN QUESTIONS

1. **The exact prompt strings sent to Kling on 7/28-29 were never saved to the
   repo.** Only their effects are recorded. Section (d4) is a reconstruction from
   KIT.md plus the documented MCP consequences, not a transcript. If the strings
   exist anywhere it would be in a chat transcript, not on disk.
2. **`who_am_i` was not called in this session** (deliberately: no paid calls,
   and the account may need re-authorization). So the argument defaults for
   `duration`, `aspect_ratio`, `imageCount` and `prefer_multi_shots` are unknown.
   Only `resolution` (default `4k`) and `enable_audio` (default `false`) are
   recorded anywhere. Run `who_am_i` and fill in the table in section (c). Note
   that the tool's own description states defaults may vary between membership
   tiers, so the table has to be re-read on whatever account you sign in as — it
   is not a constant you can copy from here.
3. **Who pays for the Kling plan, and on what card, was never verified in the
   original project.** Treat billing ownership and the credit expiry date as
   facts to confirm with whoever owns the account before planning any spend.
4. **The 409 clip inventory does not include `v409_s7`.** The cut map skips from
   `s6` to `s8`, so this looks intentional, but nothing in the sources says what
   `s7` was or why it was dropped. `video/gen/` also holds four clips the cut map
   never references — `v409_s2b`, `v409_s5`, `v409_s2_treated`, `v409_s2k` — and
   only `s2k` is explained anywhere (as the picture-only alternate).
5. **The v2 caption in/out times are assumed, not specified.** `script409.md`
   names caption text for shots 2, 3, 9 and 12 and says captions are centred
   around 2/3 frame height, but gives no in/out times. The v2 config runs each
   caption for the full shot. Somebody has to make that call on screen.
6. **The v2 J-cut lead/tail values do not exist.** The v5 map has them per clip,
   tuned by ear. The v2 map has all zeros, so a first v2 assembly will cut
   flat and will need a pass of ear-tuning.
7. **No music-stop point is defined for the v2 map.** The v5 bed dies at
   "...WHOSE.", a line v2 deleted. The obvious equivalent is shot 10, THE STOP,
   but the script does not say so and `script409.md` says the score happens at
   the edit, so the v2 config ships with music off.
8. **Whether the key compound noun is genuinely mis-articulated or whisper mishears a
   shouted compound noun was never resolved.** Four attempts, three different
   manglings. It needs a human's ears before any more spend.
9. **No 409 cut has been graded and re-judged since `grade.py` was wired in.**
   The only measurement on record is a contrast standard deviation of 80.5
   dropping to 75.5 on one v2 take. The "looks obviously AI" rejection predates
   the grade pass being applied to anything the reviewer watched.
10. **The repo has no git remote.** Everything in `video/gen/`, `video/kling_takes/`
    and `video/gen/v2_sheets/` is gitignored and existed only on the original
    build machine. None of the source stills or takes referenced above are
    recoverable if that disk goes.
11. **BOSS Part B is still unresolved and nothing says which way it went.**
    `v2_sheets/README.md` records profileA at 48.9 saturation and profileB at
    101.5 against the approved portrait's 70.9, with the choice ("re-roll with
    saturation pinned, or take profileA and correct in the grade") left open.
    `boss_profile_FINAL.png` exists on disk, so a call was probably made, but no
    source records which candidate it came from or how it was corrected.

---

## AUDIT NOTES

Adversarial audit of this section against the sources. Every number, filter
string, filename and threshold below was re-derived from the files, not from the
section's own claims.

**Corrections made**

1. **Budget arithmetic was wrong** (section c, "Budget arithmetic"). The section
   said a full KIT pass was "9 generations x 3 takes x 96 credits = 2592
   credits". Nothing supports 9 generations: `video/kling_kit/KIT.md:28-79` is 12
   shots in three batches, which at the 3-shot cap splits into **5** chunks.
   Replaced with a per-chunk table costed from the KIT's own durations at the
   verified 12 credits/second: **444 credits per take of everything, 1332 for a
   3-take pass.**
2. **Chrome profile count was wrong** (section a4). The production video-ads
   handoff doc says **two** browsers were paired and **both** were the wrong
   login, with the correct one a *third* profile. The section said three were
   paired, two wrong — which reads as though the right profile is already
   connected. Corrected.
3. **Stage status overstated** (intro). The section claimed stages 1-3 "done and
   approved (script, character sheets, ...)". `video/gen/v2_sheets/README.md:10-16`
   records BOSS Part B as explicitly **unresolved** on saturation. Corrected, with
   the three measured numbers, and added as OPEN QUESTION 11.
4. **Stage-3 stills list was stale** (section i). It named `SETUP_D_BURST_START`
   as the door-burst asset. Commit `947cb6b` and the production handoff doc lock
   **`SETUP_D_BURST_FINAL`** instead, and the list omitted `BOSS_SHEET_FINAL`,
   `HER_SHEET_FINAL`, `HER_PORTRAIT_FINAL`, `HER_PROFILE_FINAL`,
   `boss_profile_FINAL`, `SETUP_D_APPROACH_WIDE` and `SETUP_D_CLIP1_START`, all of
   which are on disk. Rewritten against the actual directory (95 files) with the
   `_FINAL` convention explained, plus the README's PIL `ImageStat` acceptance
   test.
5. **Six load-bearing lessons were dropped.** Added as failure-log items 17-23:
   - **17, edit-not-recreate** — the newest and most valuable rule in the sources
     (the production handoff doc, commit `947cb6b`): editing the reference
     frame beat six recreation attempts that each re-rolled the physics. Its
     corollary ("face visible ⇒ face sheet allowed in the edit call") also
     qualifies existing item 10, which as written reads like a blanket ban.
   - **18, one line per shot** and **19, quarter-frame shoulder cap** — two of the
     three fixes credited in commit `734e33d` for turning the v3 batch from
     failing into four-of-five passing. Neither appeared anywhere in the section.
   - **20, build dialogue films from SINGLES** (the handoff doc), described in the
     source as the reference's core engineering — and the actual reason the KIT is
     structured one-character-per-generation.
   - **21, location sheet from a peopled still / "PHOTOGRAPH, not illustration"**
     (the handoff doc).
   - **22, checkpoint before batching, stop-loss decided in advance, "do not batch
     ahead"** (the handoff doc) — the spend-discipline rule, entirely absent.
   - **23, the platform-rejection risk on the bat was already accepted by the
     decision-maker** (the handoff doc) — material for anyone about to ship this ad.
6. **Two consolidation additions were undocumented.** Added rows to both merge
   tables: the music block is now wrapped in a `bed`/`stop_index` None-guard the
   original did not have (required by the v2 config, which ships with music off,
   and the original would crash), and `spec["lines"]` became `spec.get("lines", [])`.
   Both are additions, not losses, but an undocumented change is how silent drift
   starts.
7. **Upload endpoint caveat added** (section b). The section hardcodes
   `https://kling.ai/api/mcp/files`. The `file_upload` tool's own contract makes
   the returned `uploadUrl` authoritative; noted which wins.
8. **Naming trap flagged** (intro). `video/assemble409.py:2` opens with "Assemble
   409 v2", where "v2" is the *edit* version, not `script409.md` v2. Left
   unflagged, a reader concludes the current script is already implemented.
9. Minor factual enrichment: OPEN QUESTION 4 now lists the four other unreferenced
   `v409_*` clips on disk; OPEN QUESTION 2 now records that `who_am_i`'s own
   contract says defaults vary by membership tier, so the argument table cannot be
   copied between accounts.

**Verified clean — checked and found correct**

- **No elision anywhere.** Both Python programs are complete and runnable. Every
  `...` in the file is either a URL, a schema placeholder, or the literal caption
  text `"...WHOSE."` / `"...PLAN?"`.
- **The consolidation is faithful, proven by execution, not by reading.** Both
  blocks were extracted to files and run against the originals:
  - both compile;
  - `chain()` and `chain(True)` return strings **byte-identical** to
    `video/grade.py:46-52`;
  - the 14-entry `CONFIG["cuts"]` table matches `video/assemble409.py:26-46`
    **element for element**, including `crop=756:1344:324:110` on `s2`,
    the `s4` repeat, the `in: 3.7` re-use of `s10`, and every caption string and
    in/out time;
  - `room()` and `roomtone()` produce output **bit-identical** to the originals
    (max abs difference 0.0) on a synthetic signal, confirming the seed-4 and
    seed-9 extraction did not change the sound;
  - `MUSIC_STOP_IDX 9` preserved; body 35.0s, card 2.4s, total 37.4s;
  - `load_spec()` on the shipped `takes-409.json` reproduces `check_take.py`'s
    `EXPECTED`, `FILLER` and `HOMOPHONE` exactly, and all seven threshold defaults
    match `check_take.py:131-161`;
  - `infer_id()` returns the same id as the original on every real filename in
    `video/kling_takes/`, and the documented loose-match second pass fires only
    where the original returned `None`.
- **The v5 cut map is real.** `ffprobe` on `video/out409_9x16.mp4` reads
  **37.400000s at 1080x1920/24fps** and `out409_4x5.mp4` **1080x1350**, matching
  the section's 35.0 + 2.4 arithmetic and the `crop=1080:1350:0:285` output.
- **The v2 config loads and totals as claimed:** 12 cuts, body **21.3s**, card
  2.0s, total 23.3s through `load_config()`. The 21.3s also matches summing
  `script409.md:78-138` shot by shot.
- **MCP registration is exact.** `~/.claude.json` contains precisely
  `{"type": "http", "url": "https://kling.ai/mcp"}` under `mcpServers.kling` —
  no key, no env block, as stated.
- **Every MCP parameter claim checks out against the live tool contracts**
  (schemas read, no paid call made): `file_upload` takes exactly `filename`,
  `contentType`, `size`, `taskTraceId`; tickets single-use with `expire_at`;
  "reuse result URL instead of re-upload"; image spec "PNG/JPG only, below 4K,
  ≤30MB, aspect ratio no wider than 1:2"; `model` required with no default;
  `arguments` as name/value pairs with **all values strings**; `inputs` as
  `{name, inputType, url}`; `rationale`; `generation_id` returned immediately;
  result **URLs expire in 24 hours**. All as documented.
- **Credits, prices and dates match the sources:** 12 credits/second flat;
  15s=180, 9s=108, 8s=96; the 8000-credit grant and its one-month expiry;
  8000 MCP vs 8091 web (91 bonus); 8000 → 7820 across a 180-credit job on the
  funded account; the 66-credit wrong account; image models at 70 / 30 / 4 / 2
  credits.
- **The historical checker results are real, not reconstructed.** `1.14s` and
  `1.16s` come verbatim from commit `734e33d`; the four-attempt mis-transcription
  progression of the key compound noun from commit `01c5d0b`; the contrast
  stddev `80.5 → 75.5` in OPEN QUESTION 9 from commit `1d40064`.
- **Commit ordering claim holds:** `1d40064` (checker + grade) precedes `c9ecf19`
  (script v2), so the tooling really does predate the v2 rebuild.
- **Both KIT quotations are verbatim.** The global setup box matches
  `KIT.md:12-22` word for word, and all three batch shot lists match
  `KIT.md:32-79`, including the per-line "The subject stops talking, silence in
  the room."
- **Every `grade.py` comment survived the inlining** — the "clean is the tell"
  rationale, the Premiere HSL-Secondary note, and the 6/255 ≈ 2.4% grain
  justification are all present and unedited.
- **The `SemiBold` / `Semibold` comment is true, and I checked it rather than
  trusting it.** `Lora-var.ttf` exposes a named instance `SemiBold`;
  `/System/Library/Fonts/SFNS.ttf` exposes `Semibold` **and** `Condensed Heavy`.
  The warning not to "tidy" them into one spelling is correct.
- **Dependency claims are accurate on this machine:** numpy 1.26.4, scipy 1.17.1,
  pillow 12.1.1, whisper importable (20250625), `ffmpeg`/`ffprobe` at
  `/opt/homebrew/bin`. Python here is 3.11.4, satisfying the stated 3.10+.
- **File-map paths all resolve**, including `gen/c409_insert.jpg`,
  `audio/bed_phrygian.wav`, `public/brand/Lora-var.ttf`, the card mark PNG, the
  ten `kling_kit` jpgs, and `shoulder_1.png`. `video/kling_picks/` genuinely does
  not exist, and `v409_s7` genuinely is absent, as claimed. `v409_s2k.mp4` does
  exist, which is what makes keeping the inert `skip_clips` guard the right call.
- **The v2 checker table is correctly derived** from `script409.md:98-137` — all
  seven lines lowercased and depunctuated exactly, and the absence of
  `pause_after`/`quiet_after` is correctly justified by v2 deleting the
  two-fragment beat.

**Not changed, but worth knowing**

- The `check_takes.py` usage example names the v3 take of chunk 1C where the
  original checker's docstring named the v2 take of the same chunk. Both exist
  in the original take library; `v3` is the batch that actually passed, so the
  change is an improvement rather than an error.
- The section's `room()` docstring adds measured numbers (reverb index 0.93 vs
  0.56, centroid 597Hz vs 860Hz, RT60 ~350ms, 3.8kHz shelf) that are **not** in
  `assemble409.py:76`. They are not invented: they come from the
  production handoff doc and `script409.md:164-166`. Correctly sourced, just
  relocated.
