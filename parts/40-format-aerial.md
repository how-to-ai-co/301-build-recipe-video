> # This format now RUNS. Use `engine/scripts/render_aerial.py`
>
> When this section was written the format was documentation. It has since been
> installed and rendered:
>
> ```bash
> python3 scripts/render_aerial.py public/footage/your_clip.mp4 \
>     example ads/test.mp4
> ```
>
> The SHIPPED script's COPY dict uses placeholder keys `example` and
> `example_paid`, and its lockup is text-only until you set the LOCKUP
> constants (and optionally MARK) at the top of the file. The full listing
> later in this document is the original production version, kept for
> reference: it shows the segment-a..d key scheme and the mark-PNG lockup
> this doc's tables describe.
>
> No footage ships — bring your own clip, use stock you have rights to, or
> generate one (`parts/50`). It needs Pillow (`pip install -r requirements.txt`)
> and ffmpeg, which makes it the one format that is not pure Node.
>
> **It needs FOOTAGE**, and that is inherent, not a gap: the format is a text
> block burned over a clip, so there has to be a clip. Their own video works
> exactly as well as a generated one, so this format does not require any
> spend.
>
> Everything below still holds for the filter graphs, the crop geometry and the
> reasoning. Only the filenames are stale; see `parts/80`.

> ### Filenames in this section are stale
>
> It was written before the delivery convention changed. Any `_V1.mp4` you see
> below, and the format tokens `Voiceover` and `Rsvp`, are gone: the version
> counter was replaced by a **HookStyle** token (`Ask` / `Tell` / `About`), and
> the formats are now `Cards`, `Aerial` and `OneWord`.
>
> **The paths and filenames here are wrong. The code, constants and reasoning
> are not.** Take the naming from `parts/80-naming-and-delivery.md`, and take
> `ads/README.md` in the main repo over both.

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

> **Extra note for this section:** it was written while another session was
> reorganising `ads/` underneath it. The delivery paths were corrected to the
> new persona-first tree. See `parts/80-naming-and-delivery.md`, which is the
> current convention, and re-check `ads/README.md` in the main repo if this
> is more than a few days old.

# The aerial format — ads 405-408

A picturesque AI-generated landscape clip, one static text block burned over it,
an original music bed mixed under the clip's own ambience, 9 seconds, no
voiceover. Four concepts, two offers, two hook arms, two ratios.

Everything in this section was read out of the working pipeline and, where a
number is quoted, measured on this machine. Numbers marked **measured** were run;
numbers marked **inferred** were not.

One caveat for the whole section: this starter kit is scrubbed of the original
client's copy, names and brand assets. Every copy string below is a placeholder,
and every layout number (line counts, block heights, bbox tuples, MD5s) was
measured on the original production copy and lockup — treat those numbers as
worked examples of the method, and re-run the measurements against your own copy
before trusting any specific pixel value. The same applies to the §12 and §15
verification claims (string-identical copy, pixel-identical overlays,
bit-identical MD5s): they were made against the original copy before this scrub
and will not reproduce against the placeholder strings.

---

## 1. What ships

| | |
|---|---|
| Concepts | 405 Segment A · 406 **Segment B** (renamed after shipping; the pixels still carry the old label, see below) · 407 Segment C · 408 Segment D |
| Offers | `FREE` (the free destination) and `PAID` (the paid destination) |
| Hook arms | `V1` third person, `V2` second person. **V2 is FREE-only, and only 405 was rendered.** |
| Ratios | 9x16 native 1080x1920 · 4x5 centre crop 1080x1350 |
| Source duration | 9.055782 s for seven clips, 9.101995 s for `gen/paid_d.mp4` — **measured** |
| Output duration | 9.056 s, except 408 PAID at 9.102 s — **measured** on all 18 |
| Video | H.264, CRF 18, preset medium, yuv420p |
| Voiceover | none |
| Audio | AAC 48 kHz stereo, **192–197 kbps measured** across all 18 shipped files |
| File sizes | 6.7 MB to 30.8 MB — **measured** on the 18 shipped 405-408 files |

Full matrix the build **can** produce: 4 personas × (FREE V1, FREE V2, PAID V1) ×
2 ratios = **24 files**. Not 32 — there is no PAID V2, see §7.

**What is actually on disk is 18 files, not 24.** FREE V2 was only ever built for
405 Segment A (`./build_ads_v2.sh segment-a`, 2026-07-29 20:43). 406, 407 and 408 have
FREE V1 and PAID V1 only. `ads/MANIFEST.md` agrees: three rows for 405, two each
for 406/407/408. Do not report the V2 arm as a four-persona test — it is one
persona.

Naming, per `ads/README.md` **as rewritten 2026-07-30**:

```
ads/<NN-persona>/<number>-<format>-<hook>/BRAND_<number>_<Persona>_<Format>_<Hook>_<OFFER>_<Ratio>_V<n>.mp4
                                          caption-free.md  /  caption-paid.md
```

Worked example (tokens genericised for this kit):
`ads/01-segment-a/405-aerial-example-hook-a/BRAND_405_SegmentA_Aerial_ExampleHookA_FREE_9x16_V1.mp4`.

**No spaces in filenames.** That is a rule now, and it is load-bearing: per
`ads/README.md`, 62 of 94 files used to carry spaces, they break globbing, break
some Drive syncs, and "silently broke two renders during the build". The hook
token is CamelCase with the spaces stripped (`ExampleHookA`), and a
`Format` token (`Voiceover` · `Aerial` · `Rsvp`) sits between Persona and Hook.

Two consequences specific to this wave:

- **The four aerial concepts live under persona-first folders**:
  405 → `01-segment-a`, 406 → `03-segment-b`, 407 → `04-segment-c`,
  408 → `02-segment-d`.
- **406's Persona token was renamed after shipping.** The README retired 406's
  original audience label, but the *on-screen copy of the shipped 406 mp4 still
  opens with the old label* and the caption is still titled with it too. The
  video was renamed, not re-rendered. If that mismatch matters to you, it is a
  re-render, not a rename.

Everything below that quotes an old flat path such as
`ads/405-segment-a-example-hook-a/…` predates that rename.

---

## 2. Inputs you must have before anything runs

### 2a. Footage — eight generated landscape clips

| Persona | FREE clip | PAID clip |
|---|---|---|
| Segment A (405) | `gen/seedance2_v1.mp4` | `gen/paid_a.mp4` |
| Segment B (406) | `gen/lands_b.mp4` | `gen/paid_b.mp4` |
| Segment C (407) | `gen/lands_c.mp4` | `gen/paid_c.mp4` |
| Segment D (408) | `gen/lands_d.mp4` | `gen/paid_d.mp4` |

All eight are **measured** at H.264 1080x1920, AAC 44.1 kHz stereo, 9.055782 s
(`paid_d` 9.101995 s). Generated on **Seedance 2.0** via Replicate.
They carry their own native ambience — engine hum, wind, city — and that
ambience is load-bearing: it is half the final mix.

The two 405 looks, per the shipped captions: FREE is "Andean plateau city, warm
late afternoon", PAID is "High desert city at dusk, street lights coming on".

Nothing in the pipeline resizes or reframes the footage. **Generate at 1080x1920
or the geometry in §5 is wrong.**

### 2b. Music bed — `audio/bed_phrygian.wav`

Originally composed, synthesised in Python. Not licensed, not stock, no rights
question. 48 kHz stereo PCM, 10.000 s, peak-normalised to 0.72. Full generator
in §11.

### 2c. Fonts and the brand mark

| Asset | Path | Note |
|---|---|---|
| SF Pro (variable) | `/System/Library/Fonts/SFNS.ttf` | **macOS only.** This is the whole look. |
| Lockup font | first `.ttf`/`.otf` in `public/brand/` | auto-detected by the shipped script; SIL-OFL serifs like Lora are a free download. System font until you add one |
| Brand mark | `public/brand/brand_mark.png` | supply your own square RGBA png (the original was 1000x1000) |

No fonts and no brand mark ship with this kit — drop your own into
`public/brand/` during setup. In the consolidated `engine/`, the end-card brand
assets are wired through `src/brand.mjs`, so a rebrand is one file.

**Variation names are exact strings and a typo fails silently.** SF Pro exposes
`Heavy` and `Semibold` (lowercase b). Lora exposes `SemiBold` (capital B). The
`font()` helper swallows the exception from `set_variation_by_name`, so a wrong
name does not error — it renders Regular and you find out by eye. That
inconsistent capitalisation between the two fonts is real; do not "fix" it.

### 2d. Tooling

`ffmpeg` + `ffprobe` (built against ffmpeg 8.1 here), `python3` with `Pillow`
(12.1.1 here), `numpy`, `scipy` (the last two only for the bed).

---

## 3. The pipeline, three ffmpeg passes

```
gen/<clip>.mp4  ──┐
                  ├─► [1] score   ─► tmp/_<key>.mp4    (video stream-copied, new AAC)
audio/bed.wav  ──┘

tmp/_<key>.mp4 ──► [2] overlay ─► ..._9x16_V1.mp4      (H.264 CRF 18, audio copied)
                                     │
                                     └─► [3] crop ─► ..._4x5_V1.mp4  (H.264 CRF 18, audio copied)
```

Video is encoded by us **twice** for the 4:5 deliverable: once burning the
overlay at 9x16, once cropping that result. That is deliberate — cropping the
already-burned 9x16 guarantees the two ratios carry pixel-identical type. The
alternative (crop first, render a second overlay at 1350) risks two different
layouts. At CRF 18 the second generation is not visible.

---

## 4. Pass 1 — the audio mix

Byte-identical in both original build scripts. This is the whole thing:

```
ffmpeg -y -v error -i "$src" -i "$BED" -filter_complex "\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55[amb];\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[bed];\
[bed][amb]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k "tmp/_${key}.mp4"
```

Line by line:

- **`[0:a]` is the clip's own ambience**, resampled 44.1 → 48 kHz and pulled
  down to **0.55**. **`[1:a]` is the music bed at 1.0.** The music is the louder
  element and the generated ambience sits under it. If you invert that you get a
  drone-footage stock reel, not an ad.
- **`aformat` on both legs is not optional.** Source is 44.1 kHz, bed is 48 kHz.
  `amix` will resample for you, but pinning both to 48 kHz stereo first is what
  keeps the two legs phase-sane and the output a single predictable format.
- **The "amix weights" live in the `volume` filters, not in `amix`.** `amix` has
  a `weights=` option; this graph does not use it. Two separate `volume` stages
  are easier to read and to change one at a time.
- **`normalize=0` is the important flag.** `amix` defaults to `normalize=1`,
  which divides every input by the input count — that would halve both legs and
  quietly undo the 0.55 / 1.0 balance you just set. With `normalize=0` the legs
  sum as written.
- **`duration=shortest`** bounds the mix at 9.056 s (the clip), not 10.0 s (the
  bed). The bed is deliberately a little long so it never runs out.
- **`alimiter=limit=0.95` is insurance plus makeup gain.** **Measured** on
  `gen/lands_b.mp4`: the raw sum peaks at **-1.892 dBFS**, i.e. it never
  actually hits the 0.95 ceiling, so the limiter does no gain reduction on this
  material. What it *does* do is apply `alimiter`'s `level` option, which
  **defaults to true** — a flat makeup gain of 1/limit. Output peak **measured**
  at **-1.446897 dBFS**, a lift of +0.4455 dB = 20·log10(1/0.95). So on this
  footage the limiter is a fixed +0.45 dB lift with a safety net for any clip
  whose ambience comes back hotter. If you ever want a true -0.45 dBFS ceiling
  instead, add `:level=disabled`.
  (Re-measured on this machine with `astats`, ffmpeg 8.1: raw sum peak
  -1.892424 dBFS, limited peak -1.446897 dBFS. `ffmpeg -h filter=alimiter`
  confirms `level <boolean> auto level (default true)`. For contrast, the same
  graph with `amix`'s default `normalize=1` peaks at -7.9 dBFS — that is the
  6 dB the flag is protecting you from.)
- **`-c:v copy`** — the video is untouched at this stage, so do not re-encode it.
- Output AAC 192k. The final files carry **192–197 kbps** — **measured** across
  all 18 (192151 on 405 PAID up to 196951 on 408 PAID).

There is no `loudnorm` anywhere in this format. (`make_bed.sh`, used by the
*other* waves, does `loudnorm=I=-19:TP=-2:LRA=9`; the aerial wave does not touch
it, because there is no voiceover to duck around.)

---

## 5. Pass 2 — the overlay

### 5a. Typography

Plain system font, everything on screen at once, no sequential reveal, no design
flourish. It is the **Instagram Stories text-tool look**, on purpose — a pattern
interrupt against a feed of designed infographics. Only the lockup is branded.

| Element | Value |
|---|---|
| Body face | SF Pro variable, weight `Heavy` |
| Body size | 62 px start, shrink loop steps down by 2 to a floor of **34** |
| Line height | `int(size × 1.16)` = 71 px at 62 |
| Paragraph gap | `int(size × 0.55)` = 34 px at 62 |
| Block width | 88% of frame = 950 px wrap width |
| Fill | pure white |
| Outline | **4 px hard black stroke, not a soft shadow** |
| Alignment | every line centred individually |
| Wordmark | Lora `SemiBold` 76 px, your brand wordmark |
| Brand mark | square png resized to 78x78 LANCZOS |
| Tagline | SF Pro `Semibold` 34 px, 3 px stroke |

SF Pro is genuinely what Instagram Stories "Classic" renders in on iOS (Roboto
on Android), so this is the native-app look and not an approximation.
Drop a geometric sans (Montserrat is a free download) into `public/brand/` if
the CapCut-style look is ever wanted as a further arm.

### 5b. Layout math

```
W, H                = 1080, 1920
SAFE_TOP            = int(H * 0.14)   = 268    # Meta Reels chrome, top ~14%
SAFE_BOTTOM         = int(H * 0.795)  = 1526   # ← DEAD CODE, see below
lock_y              = int(H * 0.735)  = 1411
avail               = (lock_y - 70) - SAFE_TOP = 1073
max_w               = int(W * 0.88)   = 950
y_top of block      = SAFE_TOP + (avail - total) // 2
```

The text block is centred inside `avail`, **not inside the whole safe band**.
That 70 px is the gutter above the lockup. Without it a tall four-paragraph PAID
block collides with the wordmark.

`SAFE_BOTTOM` is computed and never referenced. It is dead. Keep the number
written down anyway — it records where the bottom Reels chrome starts — but do
not believe the code enforces it. It does not: the PAID tagline's last row of ink
is **y=1548**, which is **22 px** past 1526. (Pillow's `getbbox()` returns 1549
for that layer; the lower bound is exclusive, so the last painted row is 1548.
Every bbox number in this section is a raw `getbbox()` tuple — read the fourth
value as one-past-the-last row.) That has shipped and nobody flagged it, but know
it is happening before you lengthen that tagline.

**The shrink loop currently never fires.** Every one of the twelve copy
permutations lays out at the full 62 px — **measured** by running the real layout
code:

| key | size | lines/para | block height | y range |
|---|---|---|---|---|
| segment-a V1 / V2 | 62 | 3,2,1 / 3,2,1 | 494 | 557–1051 |
| segment-b V1 / V2 | 62 | 4,2,1 / 4,2,1 | 565 | 522–1087 |
| segment-c V1 / V2 | 62 | 3,2,1 / 4,2,1 | 494 / 565 | 557–1051 / 522–1087 |
| segment-d V1 / V2 | 62 | 2,3,1 / 3,3,1 | 494 / 565 | 557–1051 / 522–1087 |
| segment-a PAID | 62 | 3,3,3,1 | 812 | 398–1210 |
| segment-b PAID | 62 | 4,3,3,1 | 883 | 363–1246 |
| segment-c PAID | 62 | 3,3,3,1 | 812 | 398–1210 |
| segment-d PAID | 62 | 2,4,3,1 | 812 | 398–1210 |

The tallest block is 883 against 1073 of room. **This corrects a claim in
`ads/01-segment-a/405-aerial-example-hook-a/caption-paid.md` line 71**
(the same line is in all four PAID captions), which says "Block auto-shrinks to clear the
lockup, so this four-paragraph copy sits slightly smaller than the FREE cut's
three." It does not. The PAID block is *taller* but rendered at the same 62 px.
Fix the caption, not the code.

Sharp edge to know about: if the loop reaches its smallest size and the block
still does not fit, it exits with the last (smallest) values and the block
silently overflows into the lockup. There is no guard. Copy long enough to
trigger that is copy too long for a 9-second ad, but that is a judgement, not an
assertion the code makes.

That smallest size is **34 px, not 35**. The loop is `range(BODY, 33, -2)` =
`[62, 60, … , 36, 34]`; Python's `range` stops *before* the 33, so the last value
tried is 34.

### 5c. Lockup geometry — **measured**

Raw Pillow `getbbox()` tuples `(left, upper, right, lower)`, right/lower
exclusive, re-measured on this machine:

```
mark   78x78 at (310, 1419)          # lx = 310.0 exactly, wordmark advance 362.0 px
wordmark  Lora SemiBold 76                        (408, 1429, 770, 1493)
tagline FREE  (original free tagline)             (355, 1512, 727, 1543)
tagline PAID  (original paid tagline)             (288, 1512, 795, 1549)
```

The mark and wordmark are centred as one unit: `lx = (W - (78 + 20 + text_w)) / 2`,
20 px of air between mark and word, mark nudged 8 px down so its optical centre
matches the cap height.

The PAID tagline uses U+00B7 MIDDLE DOT, not a hyphen or a bullet.

### 5d. The fade and the ffmpeg call

```
ffmpeg -y -v error -i src -loop 1 -i overlay.png \
  -filter_complex \
  "[1]format=rgba,fade=in:st=0.35:d=0.55:alpha=1[ov];[0][ov]overlay=0:0:format=auto" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy -shortest out.mp4
```

The block holds a 0.35 s beat of clean landscape, then fades up over 0.55 s and
stays for the rest of the 9 seconds. Nothing else moves. See §9 for why `-loop 1`
and `-shortest` are both mandatory.

The overlay PNG is written next to the output as `<name>.overlay.png` and deleted
after a successful run. If a build dies mid-way you will find orphan PNGs in the
ad folders; they are safe to delete.

---

## 6. Pass 3 — the 4:5 crop, and why the offset is 285

```
ffmpeg -y -v error -i "..._9x16_V1.mp4" \
  -vf "crop=1080:1350:0:285" -c:v libx264 -crf 18 -preset medium \
  -pix_fmt yuv420p -c:a copy "..._4x5_V1.mp4"
```

`crop=w:h:x:y`. Width is unchanged (1080, x=0). Height 1350 is 1080 × 5/4.

**The 285 is not a taste decision, it is arithmetic: (1920 − 1350) / 2 = 285.**
It is a dead-centre crop, 285 px shaved off the top and 285 off the bottom. The
kept window is y ∈ [285, 1635].

That works only because the layout in §5b puts everything inside that window with
room to spare — **measured**:

Two different numbers get confused here, so keep them apart. The table in §5b is
the **layout box** — the y the code writes text at, and box + block height. The
actual **ink** starts lower than the box top (the glyph origin sits below the
em-box top) and ends higher than box + height (the last line's descender space
and the trailing line-height are empty). Both, for the worst case:

| | value | source |
|---|---|---|
| segment-b PAID layout box | y 363, box bottom 363+883 = 1246 | §5b, computed |
| segment-b PAID **whole overlay** ink bbox | `(73, 371, 1006, 1549)` | **measured**, `overlay('segment-b_paid').getbbox()` |
| crop window kept rows | 285 … 1634 inclusive | `crop=1080:1350:0:285` |

Margins on the tallest permutation, **measured, not derived**: topmost ink 371 −
285 = **86 px** at the top; bottommost painted row 1548, 1634 − 1548 = **86 px**
at the bottom. Symmetrical, and thinner than it looks — a single extra line of
62 px Heavy body copy is 71 px of it. If you raise `BODY`, lower `SAFE_TOP`, or
add a fifth paragraph, re-run the layout numbers before you trust the crop.

(An earlier draft of this section reported 78 px at the top. That was the layout
box top, 363, not the ink. 78 is a conservative number so nothing shipped wrong,
but it is not what the pixels say.)

The audio is stream-copied here (`-c:a copy`), so both ratios carry the identical
mix and there is no second AAC generation.

---

## 7. How PAID differs from FREE

This is the part people get wrong. **PAID is not a V-variant of FREE.** Five
things move at once, which is exactly why the OFFER token exists — a V number
would falsely claim a single variable changed.

| | FREE | PAID |
|---|---|---|
| Footage | its own landscape | **a different landscape**, generated net new |
| Paragraph 1 (hook) | the V1 hook | **byte-identical to the V1 hook** |
| Paragraph 2 | the body line | the paid lead-in + the same body line |
| Paragraph 3 | the free CTA | the shared offer line (below) |
| Paragraph 4 | — | the paid CTA |
| Lockup tagline | the free tagline | the paid tagline |
| Ads Manager CTA | Subscribe | Learn More |
| Headline | the free headline | the paid headline |

The shared offer paragraph, one string for all four personas because the offer is
one offer:

> [One placeholder sentence describing what the paid tier includes.]

**PAID has its own footage and that is unique to this wave.** In 401-404 the PAID
cut reuses its FREE twin's artwork and only appends an offer outro. Here the
landscape is different on purpose, so the two do not read as the same ad twice in
one feed. Same persona, same hook, same format, different footage and different
copy — still one concept with two offers, still one number.

**Judge on cost per paid subscriber at 30 days, not CTR.** Naming a paid
tier filters people at the click, so PAID should be expected to lose CTR by
design and can still win the metric that matters.

One claim in the original PAID copy was flagged unverified in the shipped
caption and never cleared: **that a recurring benefit really recurred at the
stated cadence**. It was a claim in a paid ad and it needed sign-off before
spend. The lesson stands for any brand: cadence and quantity claims in paid
ads get verified before money goes behind them.

A second, separate caption note explains why nothing countable is on screen: at
build time the project's own pages and docs disagreed on both the count of items
included in the paid offer and its dollar value. **No count and no dollar value
goes on screen** until the sources agree. No price on screen ever — that is a
standing rule in `ads/README.md`, not a per-ad choice.

(These are two different things. The cadence claim is *in the copy* and
unverified. The count is *deliberately absent from the copy* because the
underlying numbers disagree. Do not collapse them into one item.)

---

## 8. V1 vs V2 — the hook arms

Both run. Neither replaces the other. Per `ads/README.md` the V token covers
"one variable inside the same concept and offer moves", which is exactly this, so
V1 stays live and does **not** move to `_superseded/`.

The brand's hook rule, set in a creative sync: never open on a question, and do
not address a category — name the reader's pain as fact and let them feel
called out. The canonical rewrite was "Are you an X?" → "You're an X and you
already know". Strong hooks almost always open on "you", "stop" or "instead".

405-408 never used question hooks, so **what moves in this wave's V2 is the other
half of that rule**: third person → second person. That is a *different* change
from the 401/402 V2s, which fixed the question. Do not read the three V2 results
as one experiment.

Only paragraph 1 changes. Paragraphs 2 and 3 are byte-identical to V1, as are the
footage, music, crop and offer.

**The V2 copy exists in code for all four personas. Only 405 Segment A was ever
rendered.** `render_ad.py` carries `segment-b_v2`, `segment-c_v2` and `segment-d_v2`, and
the layout table above covers all four, but the only V2 mp4s on disk are the two
405 files (2026-07-29 20:43). `ads/MANIFEST.md` lists one V2 row, and only 405's
`caption-free.md` carries the required variants block. The other three rows in the
table below are *unshipped copy*, not a live arm. Render them before you quote
them in a plan.

| Persona | V1 (third person) | V2 (second person) |
|---|---|---|
| Segment A | Placeholder third-person hook for segment A: names the audience category. | Placeholder second-person hook for segment A: states the reader's pain as fact. |
| Segment B | Placeholder third-person hook for segment B — carries “curly quotes” on purpose. | Placeholder second-person hook for segment B: states the reader's pain as fact. |
| Segment C | Placeholder third-person hook for segment C: names the audience category. | Placeholder second-person hook for segment C: states the reader's pain as fact. |
| Segment D | Placeholder third-person hook for segment D: names the audience category. | Placeholder second-person hook for segment D: states the reader's pain as fact. |

The original segment-B V1 line contained **curly quotes**, U+201C and U+201D,
not ASCII, and the placeholder keeps a pair to preserve the lesson: SF Pro
renders them correctly and straight quotes look wrong at 62 px Heavy.

**There is no PAID V2**, and that is a data fact, not an omission to fill in: no
second paid landscape was ever generated, and the PAID copy deliberately holds
paragraph 1 identical to V1 so the offer is the only variable in the FREE/PAID
pair. The consolidated build below refuses `--offer PAID --arm V2` with an error
rather than quietly emitting a V1-hook file labelled V2.

---

## 9. The ffmpeg traps

Four, three of them expensive. Two have been reproduced on this machine.

### Trap 1 — `-loop 1` on a still overlay, or the fade never happens

A single-frame image input gives `fade=` no timeline to act on. Alpha stays at
its t=0 value, which is 0, and `overlay` then repeats that fully transparent
frame for the whole clip. **You get a clean landscape with no text and no error
message.** `-loop 1` on the image input is what makes the still a stream with a
running clock.

### Trap 2 — `-shortest` is mandatory once you have used `-loop 1`

`-loop 1` makes the image input infinite. `overlay` with its default framesync
settings does not terminate on the main input's EOF, so the encode runs forever.

**Reproduced twice.** First run: the §5d command with `-shortest` removed, on
`gen/lands_b.mp4` (a 9.056 s source), at `-crf 28 -preset ultrafast`, killed
after 2 minutes of wall clock having written **1613.8 s** of video and **119 MB**,
still going. Re-run during the audit with the same command and the same source
but a flat placeholder overlay: **23.3 MB written in 30 s and still running** when
killed — the same ~0.8 MB/s runaway, extrapolating to ~93 MB at 2 minutes.

Treat the exact byte and second figures as illustrative, not as constants: they
move with the overlay's content (a mostly-transparent real overlay compresses
differently from a flat one), the preset and the machine. **The behaviour is the
fact: it does not stop.**

Corollary from the wider pipeline: **cap segments with an output-side `-t`**,
i.e. `-t` placed after the filter graph and before the output filename, where it
bounds the *output*. An input-side `-t` bounds the decode instead and interacts
badly with loops and filters.

### Trap 3 — do not stream-copy a hybrid

A `-c copy` mux of streams that do not agree (different sample rates, different
timebases, a looped input) does not fail loudly, it produces a runaway or a file
that plays wrong in one player and fine in another. **Re-encode any pass where
the streams changed shape.** In this pipeline the rule shows up three times, and
each `-c:*:copy` is only there because that specific stream is provably
untouched:

| Pass | video | audio | why copy is safe |
|---|---|---|---|
| 1 score | `-c:v copy` | re-encoded to AAC | video never enters the filter graph |
| 2 overlay | re-encoded, CRF 18 | `-c:a copy` | audio was finalised in pass 1 |
| 3 crop | re-encoded, CRF 18 | `-c:a copy` | same |

### Trap 4, minor — `format=rgba` before `fade`

`fade=…:alpha=1` needs a pixel format that has an alpha channel. `[1]format=rgba`
is not decoration; drop it and the alpha fade is a no-op.

---

## 10. The consolidated source

Two files replace three near-identical originals (`render_ad.py`,
`build_ads.sh`, `build_ads_v2.sh`). What was merged and what had to be
reconciled is in §12.

Put them at the root of the pipeline directory, alongside `gen/`, `audio/`,
`public/brand/` and `tmp/`. `chmod +x build_aerial.sh`.

### 10a. `render_aerial.py`

```python
#!/usr/bin/env python3
"""Burn a static persona text block + your brand lockup onto a clip.

Text is plain system font, all on screen at once, no sequential reveal and no
design flourish — the Instagram text-tool look. Only the lockup is branded:
Lora for the wordmark and your own brand mark from public/brand, not a redraw.
(In the consolidated engine/, the lockup assets are wired via src/brand.mjs.)

Usage:
  python3 render_aerial.py <in.mp4> <persona> <OFFER> <ARM> <out.mp4>

  persona   segment-a | segment-b | segment-c | segment-d
  OFFER     FREE | PAID    destination: free offer vs paid offer
  ARM       V1 | V2        hook arm. V2 exists for FREE only, see paragraphs().

This module replaces the three-way (V1 / V2 / paid) key-suffix scheme of the
original render_ad.py with an explicit (persona, offer, arm) triple. The copy
that comes out is byte-identical to the shipped 405-408 cuts.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BRAND = Path(__file__).parent / "public" / "brand"
SF = "/System/Library/Fonts/SFNS.ttf"
LORA = str(BRAND / "Lora-var.ttf")

# Meta Reels chrome covers roughly the top 14% and bottom 20%.
# NOTE: SAFE_BOTTOM is recorded for reference and is NOT enforced anywhere.
# The PAID tagline's last painted row is y=1548, 22px past it. Known, shipped.
SAFE_TOP, SAFE_BOTTOM = int(H * 0.14), int(H * 0.795)

# SF Pro is genuinely what Instagram Stories "Classic" renders in on iOS
# (Roboto on Android), so this is the native-app look rather than an
# approximation. Montserrat-var.ttf is in public/brand if the CapCut-style
# geometric look is ever wanted as a further arm.
BODY = 62
LINE = 1.16
GAP = 0.55         # paragraph gap, keeps it reading as one block
WIDTH = 0.88       # share of frame the text block fills
STROKE = 4         # hard black outline, not a soft shadow

# ---------------------------------------------------------------------------
# Copy. One entry per persona; the arms and offers are assembled from it in
# paragraphs() so that no line of shared copy is ever written down twice.
#
# hook_v1 — third person. Names a category.
# hook_v2 — second person. The brand's hook rule from a creative sync: never
#   open on a question, and do not address a category — name the reader's pain
#   as fact and let them feel called out. The canonical rewrite was "Are you
#   an X?" -> "You're an X and you already know." Strong hooks almost always
#   open on "you", "stop" or "instead".
#
#   405-408 never used questions, so what V2 fixes here is the OTHER half of
#   that rule: third person -> second person. This is a DIFFERENT change from
#   401/402 V2. Do not read the three V2 results as one experiment.
#
# ONLY the hook changes between arms. body and the CTA are byte-identical, so
# the hook is the single variable under test.
#
# The segment-b hook_v1 carries curly quotes (U+201C / U+201D) on purpose. Straight
# quotes look wrong at 62px Heavy. Do not "normalise" them.
# ---------------------------------------------------------------------------
COPY = {
    "segment-a": {
        "hook_v1": "Placeholder third-person hook for segment A: names the "
                   "audience and the problem.",
        "hook_v2": "Placeholder second-person hook for segment A: states the "
                   "reader's pain as fact.",
        "body": "Placeholder body line for segment A.",
    },
    "segment-b": {
        "hook_v1": "Placeholder third-person hook for segment B, quoting "
                   "“someone else's words” in curly quotes.",
        "hook_v2": "Placeholder second-person hook for segment B: states the "
                   "reader's pain as fact.",
        "body": "Placeholder body line for segment B.",
    },
    "segment-c": {
        "hook_v1": "Placeholder third-person hook for segment C: names the "
                   "audience and the problem.",
        "hook_v2": "Placeholder second-person hook for segment C: states the "
                   "reader's pain as fact.",
        "body": "Placeholder body line for segment C.",
    },
    "segment-d": {
        "hook_v1": "Placeholder third-person hook for segment D: names the "
                   "audience and the problem.",
        "hook_v2": "Placeholder second-person hook for segment D: states the "
                   "reader's pain as fact.",
        "body": "Placeholder body line for segment D, deliberately a little "
                "longer than the others.",
    },
}

FREE_CTA = "Placeholder free CTA."
PAID_CTA = "Placeholder paid CTA."

# The paid cut routes to the paid destination instead of the free one.
# Paragraph 1 is byte-identical to V1 so the OFFER is the only variable under
# test in the FREE/PAID pair. The offer paragraph is shared across personas
# because the offer is. Change it here and it changes in all four ads.
PAID_BODY_PREFIX = "Placeholder paid lead-in. "
OFFER = ("Placeholder shared offer paragraph: one sentence on what "
         "the paid tier includes.")

# The lockup must not send people to the free thing the PAID cut is trying to
# upsell past. (The original carried this comment saying "V2"; that dates from
# the abandoned scheme where PAID was encoded as "405-408 V2". It is the OFFER
# that drives this, not the arm.)
LOCKUP_TAG = {
    "FREE": "Placeholder free tagline",
    "PAID": "Placeholder · paid tagline",   # U+00B7 middle dot
}

PERSONAS = tuple(COPY)
OFFERS = ("FREE", "PAID")
ARMS = ("V1", "V2")


def paragraphs(persona, offer, arm):
    """The text block, as a list of paragraphs, for one (persona, offer, arm).

    There is no PAID V2 and that is deliberate, not a gap to fill: no second
    paid landscape was ever generated, and the PAID copy holds its hook
    identical to V1 precisely so the offer is the only variable. Emitting a
    V1-hook file labelled V2 would be a lie in the filename, so this raises.
    """
    c = COPY[persona]
    if offer == "FREE":
        return [c["hook_v1"] if arm == "V1" else c["hook_v2"],
                c["body"],
                FREE_CTA]
    if arm != "V1":
        raise SystemExit("there is no PAID V2 — see paragraphs() in this file")
    return [c["hook_v1"],
            PAID_BODY_PREFIX + c["body"],
            OFFER,
            PAID_CTA]


def font(path, size, weight):
    """Variable-font instance by name.

    set_variation_by_name is NAME-EXACT and this swallows its exception, so a
    typo does not raise — it silently renders Regular. SF Pro spells it
    'Heavy' / 'Semibold'; Lora spells it 'SemiBold'. That inconsistency is in
    the fonts, not in this code.
    """
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def overlay(paras, offer):
    """One RGBA layer: static text block + branded lockup."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    max_w = int(W * WIDTH)

    # The block lives above the lockup, not in the whole safe band, or a tall
    # PAID block would collide with it. Shrink the type until it fits that
    # space. With the current copy this loop always breaks on the first pass at
    # 62px — the shrink is headroom, not an active behaviour. range(BODY, 33, -2)
    # stops BEFORE 33, so the smallest size actually tried is 34, not 35. If it
    # runs all the way to 34 and still does not fit, the block overflows silently.
    lock_y = int(H * 0.735)
    avail = (lock_y - 70) - SAFE_TOP

    for size in range(BODY, 33, -2):
        body = font(SF, size, "Heavy")
        lh, gap = int(size * LINE), int(size * GAP)
        rows = [wrap(d, p, body, max_w) for p in paras]
        total = sum(len(r) * lh for r in rows) + gap * (len(rows) - 1)
        if total <= avail:
            break

    y = SAFE_TOP + (avail - total) // 2

    yy = y
    for r in rows:
        for ln in r:
            x = (W - d.textlength(ln, font=body)) / 2
            d.text((x, yy), ln, font=body, fill=(255, 255, 255, 255),
                   stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
            yy += lh
        yy += gap

    # --- lockup: [brand mark] wordmark  /  tagline ---
    mark = Image.open(BRAND / "brand_mark.png").convert("RGBA")
    ms = 78
    mark = mark.resize((ms, ms), Image.LANCZOS)

    lora = font(LORA, 76, "SemiBold")
    word = "Your Brand"
    tw = d.textlength(word, font=lora)
    lx = (W - (ms + 20 + tw)) / 2
    ly = lock_y

    img.alpha_composite(mark, (int(lx), int(ly + 8)))
    d = ImageDraw.Draw(img)     # re-bind after the in-place composite
    d.text((lx + ms + 20, ly), word, font=lora, fill=(255, 255, 255, 255),
           stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))

    sub = font(SF, 34, "Semibold")
    tag = LOCKUP_TAG[offer]
    d.text(((W - d.textlength(tag, font=sub)) / 2, ly + 96), tag, font=sub,
           fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
    return img


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__.strip())
    src, persona, offer, arm, dst = sys.argv[1:6]

    if persona not in PERSONAS:
        sys.exit(f"persona must be one of {PERSONAS}, got {persona!r}")
    if offer not in OFFERS:
        sys.exit(f"OFFER must be one of {OFFERS}, got {offer!r}")
    if arm not in ARMS:
        sys.exit(f"ARM must be one of {ARMS}, got {arm!r}")

    png = Path(dst).with_suffix(".overlay.png")
    overlay(paragraphs(persona, offer, arm), offer).save(png)

    subprocess.run([
        # -loop 1 is required: a single-frame image gives fade= no timeline to
        # act on, so alpha stays at its t=0 value (0) and overlay repeats that
        # transparent frame for the whole clip.
        #
        # -shortest is required BECAUSE of -loop 1: the image input is now
        # infinite and overlay does not stop on the main input's EOF. Measured
        # without it: a 9s source produced 1613s / 119MB before being killed.
        "ffmpeg", "-y", "-v", "error", "-i", src, "-loop", "1", "-i", str(png),
        "-filter_complex",
        # format=rgba is not decoration — fade:alpha=1 needs an alpha channel.
        "[1]format=rgba,fade=in:st=0.35:d=0.55:alpha=1[ov];"
        "[0][ov]overlay=0:0:format=auto",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        # -c:a copy is safe here and only here: the audio was finalised by the
        # scoring pass in build_aerial.sh and does not enter the filter graph.
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", dst,
    ], check=True)
    png.unlink()
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
```

### 10b. `build_aerial.sh`

```bash
#!/bin/bash
# Aerial wave (405-408). Scores each generated landscape with the original bed,
# burns the static text block, and emits 9x16 + 4x5 into ../ads/.
#
#   ./build_aerial.sh                       everything (24 files)
#   ./build_aerial.sh --persona segment-a      one concept
#   ./build_aerial.sh --offer FREE           one destination
#   ./build_aerial.sh --arm V2               one hook arm
#   ./build_aerial.sh --persona segment-b --offer PAID --arm V1
#
# This one script replaces the former build_ads.sh (FREE V1 + PAID V1) and
# build_ads_v2.sh (FREE V2). The three arms only ever differed in which copy
# key they passed and which V token they wrote; everything else was duplicated
# text. See the handoff section "What was merged" for the reconciliations.
#
# Naming follows ads/README.md (rewritten 2026-07-30):
#   <NN-persona>/<number>-<format>-<hook>/
#     BRAND_<number>_<Persona>_<Format>_<Hook>_<OFFER>_<Ratio>_V<n>.mp4
# number = creative concept, Format = Aerial here, OFFER = destination,
# V = defect fix OR one moved variable. The FREE and PAID cuts of one number
# share a folder and a hook; they differ in footage, copy, offer and CTA, which
# is what OFFER is for.
#
# NO SPACES IN FILENAMES. Not cosmetic: 62 of 94 files used to carry them, they
# break globbing, break some Drive syncs, and silently broke two renders during
# a build. The hook is CamelCased by stripping spaces, not by lowercasing.
set -e
cd "$(dirname "$0")"

BED=audio/bed_phrygian.wav
ADS=../ads

# copy key | number | Persona token | Hook | delivery folder | FREE clip | PAID clip
#
# The delivery folder is DATA, not derived. It used to be built from the hook
# with tr; that stopped working on 2026-07-30 when ads/ went persona-first,
# because the persona folder is not derivable from anything else in the row.
#
# 406 is the trap. Its Persona token was renamed after shipping, but the
# on-screen copy of the shipped mp4 still opens with the old audience label.
# The file was renamed, the video was not re-rendered. Copy key, filename
# token and pixels are three separate things — do not change one of them
# without changing the other two on purpose.
#
# PAID has its OWN footage in this wave — unlike 401-404, where the paid cut
# reuses the free cut's artwork and only appends an outro. Deliberate: the two
# must not read as the same ad twice in one feed.
ROWS=(
  "segment-a|405|SegmentA|Example Hook A|01-segment-a/405-aerial-example-hook-a|gen/seedance2_v1.mp4|gen/paid_a.mp4"
  "segment-b|406|SegmentB|Example Hook B|03-segment-b/406-aerial-example-hook-b|gen/lands_b.mp4|gen/paid_b.mp4"
  "segment-c|407|SegmentC|Example Hook C|04-segment-c/407-aerial-example-hook-c|gen/lands_c.mp4|gen/paid_c.mp4"
  "segment-d|408|SegmentD|Example Hook D|02-segment-d/408-aerial-example-hook-d|gen/lands_d.mp4|gen/paid_d.mp4"
)

# offer:arm — the complete matrix this format ships.
# There is NO "PAID:V2": no second paid landscape was ever generated, and the
# PAID copy holds paragraph 1 identical to V1 so the offer is the only variable
# in the FREE/PAID pair. render_aerial.py refuses that combination outright.
JOBS=("FREE:V1" "FREE:V2" "PAID:V1")

WANT_PERSONA=""
WANT_OFFER=""
WANT_ARM=""
while [ $# -gt 0 ]; do
  case "$1" in
    --persona) WANT_PERSONA="$2"; shift 2 ;;
    --offer)   WANT_OFFER="$2";   shift 2 ;;
    --arm)     WANT_ARM="$2";     shift 2 ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ "$WANT_OFFER" = "PAID" ] && [ "$WANT_ARM" = "V2" ]; then
  echo "there is no PAID V2 — see JOBS above" >&2
  exit 2
fi

[ -f "$BED" ] || { echo "missing $BED — run bed.py first" >&2; exit 1; }

mkdir -p tmp
BUILT=()

for row in "${ROWS[@]}"; do
  IFS='|' read -r key num label hook folder free_clip paid_clip <<< "$row"
  [ -n "$WANT_PERSONA" ] && [ "$WANT_PERSONA" != "$key" ] && continue

  dir="${ADS}/${folder}"
  mkdir -p "$dir"

  # "Example Hook A" -> "ExampleHookA". Strip spaces, keep
  # capitalisation. Do NOT lowercase and hyphenate: that was the old flat-tree
  # folder slug and it is not the filename token.
  hooktok=$(echo "$hook" | tr -d ' ')

  for job in "${JOBS[@]}"; do
    IFS=':' read -r offer arm <<< "$job"
    [ -n "$WANT_OFFER" ] && [ "$WANT_OFFER" != "$offer" ] && continue
    [ -n "$WANT_ARM" ]   && [ "$WANT_ARM"   != "$arm"   ] && continue

    if [ "$offer" = "FREE" ]; then src="$free_clip"; else src="$paid_clip"; fi
    [ -f "$src" ] || { echo "!!! missing $src, skipping $num $offer $arm" >&2; continue; }

    base="BRAND_${num}_${label}_Aerial_${hooktok}_${offer}"
    tmp="tmp/_${key}_${offer}_${arm}.mp4"
    echo "--- $num $label $offer $arm ---"

    # 1. music bed under the clip's own engine/wind ambience.
    #    aformat on BOTH legs: source is 44.1k, bed is 48k.
    #    normalize=0 is load-bearing — amix defaults to normalize=1, which
    #    divides by the input count and would silently undo the 0.55/1.0
    #    balance. duration=shortest bounds to the 9.06s clip, not the 10s bed.
    #    alimiter=limit=0.95 catches any hot ambience; its `level` option
    #    defaults to true, so it also applies a flat +0.45dB (1/0.95) makeup.
    ffmpeg -y -v error -i "$src" -i "$BED" -filter_complex "\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55[amb];\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[bed];\
[bed][amb]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[a]" \
      -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k "$tmp"

    # 2. burn the text block (this is the only pass that touches the picture)
    python3 render_aerial.py "$tmp" "$key" "$offer" "$arm" \
      "${dir}/${base}_9x16_${arm}.mp4"

    # 3. 4:5 is a dead-centre crop: (1920-1350)/2 = 285. Text sits mid-frame
    #    so it survives — measured ink clearance is 86px top and 86px bottom on
    #    the tallest block (segment-b PAID). Re-check those if you change the type size.
    #    Cropping the ALREADY-BURNED 9x16 is what guarantees both ratios carry
    #    pixel-identical type.
    ffmpeg -y -v error -i "${dir}/${base}_9x16_${arm}.mp4" \
      -vf "crop=1080:1350:0:285" -c:v libx264 -crf 18 -preset medium \
      -pix_fmt yuv420p -c:a copy "${dir}/${base}_4x5_${arm}.mp4"

    rm -f "$tmp"
    BUILT+=("${dir}/${base}_9x16_${arm}.mp4" "${dir}/${base}_4x5_${arm}.mp4")
  done
done

echo
for f in "${BUILT[@]}"; do
  [ -e "$f" ] || continue
  printf "%-78s %ss %s\n" "$(basename "$f")" \
    "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")" \
    "$(du -h "$f" | cut -f1)"
done
```

---

## 11. `bed.py` — the music, complete

Included in full because there is no other way to produce `bed_phrygian.wav`,
and because "original music, zero rights encumbrance" is one of the things that
makes this wave shippable when 401-404 are blocked on undocumented licensing.
Requires `numpy` and `scipy`. Run it from the pipeline directory; it writes
`audio/bed_phrygian.wav` and that directory must already exist.

```python
#!/usr/bin/env python3
"""Cinematic drone bed in C Phrygian, matched to the reference ad's harmony.

Reference analysis (per-second FFT of the source clip, 45-400 Hz):
    0-3s  C   (C2 C3 G3)      i
    3-4s  Db  (Db3 F3 F4)     bII  <- the Neapolitan doing all the work
    4-6s  Eb  (Eb2 Bb3 C4)    III
    6-8s  C   (C2 C3 C4)      i
    8-9s  Db  (Db2 F3 C4)     bII

No percussion, no melody. Sustained pad over a C pedal.
Output: audio/bed_phrygian.wav
"""
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig

SR = 48000
DUR = 10.0
N = int(SR * DUR)
t = np.arange(N) / SR


def hz(name):
    names = {"C": 0, "C#": 1, "Db": 1, "D": 2, "Eb": 3, "D#": 3, "E": 4, "F": 5,
             "F#": 6, "Gb": 6, "G": 7, "Ab": 8, "G#": 8, "A": 9, "Bb": 10, "B": 11}
    p, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** (((o + 1) * 12 + names[p] - 69) / 12.0)


# (start, end, [notes]) — overlapping so chords crossfade into each other
CHORDS = [
    (0.0, 3.4, ["C2", "C3", "G3", "C4"]),
    (2.8, 4.4, ["Db2", "Db3", "F3", "F4"]),
    (3.9, 6.4, ["Eb2", "Bb3", "C4", "G4"]),
    (5.9, 8.4, ["C2", "C3", "G3", "C4"]),
    (7.9, 10.0, ["Db2", "Db3", "F3", "C4"]),
]

# harmonic weights — mild sawtooth, warm not buzzy
HARMONICS = [(1, 1.0), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.07), (6, 0.04)]
DETUNE = [-6.0, 0.0, 6.0]  # cents, three-voice unison for width


def env(start, end, attack=0.9, release=1.1):
    """Smooth raised-cosine envelope over [start, end]."""
    e = np.zeros(N)
    i0, i1 = int(start * SR), min(int(end * SR), N)
    if i1 <= i0:
        return e
    e[i0:i1] = 1.0
    a = int(attack * SR)
    if a > 0:
        k = min(a, i1 - i0)
        e[i0:i0 + k] *= 0.5 * (1 - np.cos(np.linspace(0, np.pi, k)))
    r = int(release * SR)
    if r > 0:
        k = min(r, i1 - i0)
        e[i1 - k:i1] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, k)))
    return e


left = np.zeros(N)
right = np.zeros(N)

for start, end, notes in CHORDS:
    e = env(start, end)
    for ni, name in enumerate(notes):
        f0 = hz(name)
        # roll off the upper voices so the low end stays the anchor
        voice_gain = 1.0 if ni == 0 else 0.55 / (1 + 0.35 * ni)
        for di, cents in enumerate(DETUNE):
            f = f0 * 2 ** (cents / 1200.0)
            # slow drift so it never sounds static
            drift = 1 + 0.0007 * np.sin(2 * np.pi * (0.07 + 0.013 * ni) * t + ni)
            phase = 2 * np.pi * f * t * drift + (ni * 1.7 + di * 0.9)
            v = np.zeros(N)
            for h, amp in HARMONICS:
                if f * h > 9000:
                    break
                v += amp * np.sin(phase * h)
            v *= e * voice_gain
            # spread the detuned voices across the stereo field
            pan = 0.5 + 0.32 * (di - 1)
            left += v * (1 - pan)
            right += v * pan

# air layer: filtered noise, very low, gives the pad some breath
rng = np.random.default_rng(3)
noise = rng.standard_normal(N)
b, a = sig.butter(2, [180 / (SR / 2), 2400 / (SR / 2)], btype="band")
noise = sig.lfilter(b, a, noise)
noise *= 0.06 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t))
left += noise
right += sig.lfilter(b, a, rng.standard_normal(N)) * 0.06

# slow lowpass sweep, opens toward the Eb then closes — movement without a melody.
# Filtering block-by-block with a re-designed filter clicks at every block edge
# (a ~23 Hz ratchet). Instead: filter the whole signal at a few fixed cutoffs and
# crossfade between them. Each layer is continuous, the weights are smooth, so
# the result has no discontinuities anywhere.
stereo = np.stack([left, right])
cut_lo, cut_hi = 900.0, 3200.0
sweep = cut_lo + (cut_hi - cut_lo) * (0.5 - 0.5 * np.cos(2 * np.pi * t / DUR))

BANDS = np.geomspace(cut_lo, cut_hi, 9)
layers = []
for fc in BANDS:
    bb, aa = sig.butter(2, fc / (SR / 2), btype="low")
    layers.append(sig.lfilter(bb, aa, stereo, axis=1))

# triangular interpolation weights across the band ladder
out = np.zeros_like(stereo)
idx = np.interp(sweep, BANDS, np.arange(len(BANDS)))
lo = np.clip(np.floor(idx).astype(int), 0, len(BANDS) - 2)
frac = idx - lo
for k in range(len(BANDS) - 1):
    m = lo == k
    if not m.any():
        continue
    w = np.zeros(N)
    w[m] = 1 - frac[m]
    out += layers[k] * w
    w = np.zeros(N)
    w[m] = frac[m]
    out += layers[k + 1] * w

# master fades and normalise to leave headroom for VO and chatter
master = env(0.0, DUR, attack=1.4, release=1.6)
out *= master
out /= np.abs(out).max()
out *= 0.72

wav.write("audio/bed_phrygian.wav", SR, (out.T * 32767).astype(np.int16))
print("wrote audio/bed_phrygian.wav")
```

The bed is 10.0 s against a 9.06 s clip on purpose. `duration=shortest` in the
mix trims it, and the extra second means the bed's release tail is never what
you hear at the cut. Do not shorten it to match.

---

## 12. What was merged, and what had to be reconciled

Three files became two. `build_ads.sh` and `build_ads_v2.sh` were 95% identical
text; `render_ad.py` encoded the arm and the offer as string suffixes on a copy
key (`segment-a`, `segment-a_v2`, `segment-a_paid`) with the dictionary assembled by
two `COPY.update({...})` comprehensions.

**Merged:**

| Was | Now |
|---|---|
| `build_ads.sh` — FREE V1 + PAID V1, all four personas, no arguments | `build_aerial.sh` with no arguments — but its default `JOBS` is `("FREE:V1" "FREE:V2" "PAID:V1")`, i.e. **all three**, 24 files. To reproduce the old `build_ads.sh` exactly, run `--arm V1` |
| `build_ads_v2.sh` — FREE V2 only, optional single-persona argument | same script, `--arm V2` |
| flat `../ads/405-segment-a-example-hook-a/`, spaces in filenames | persona-first folder + `Aerial` format token + spaces stripped, both carried as a `folder` column in `ROWS` |
| `render_ad.py` `COPY` dict of 12 assembled keys | `COPY` of 4 persona entries + `paragraphs(persona, offer, arm)` |
| copy key `"${key}_v2"` / `"${key}_paid"` | explicit `<persona> <OFFER> <ARM>` arguments |
| hard-coded `_V1` / `_V2` in the output filename | `${arm}` |

**Behaviour differences I had to reconcile, all resolved toward the safer arm:**

1. **`mkdir -p "$dir"`.** `build_ads.sh` had it, `build_ads_v2.sh` did not — V2
   silently assumed V1 had already created the ad folders. On a fresh checkout
   the V2 script would have failed. **Kept**, unconditionally.
2. **Single-item filter.** Only `build_ads_v2.sh` had one, and it was
   positional (`./build_ads_v2.sh segment-a`). **Kept and generalised** to named
   `--persona` / `--offer` / `--arm` flags, because with three axes a bare
   positional is ambiguous.
3. **`[ -e "$f" ] || continue` in the summary loop.** Only V2 had it. V1's
   summary would print a literal unexpanded glob if nothing matched. **Kept**,
   and the summary now iterates an array of files this run actually produced
   rather than re-globbing the ads tree, so a partial build reports only what it
   built instead of re-listing every V from every previous run.
4. **Temp filename.** V1 used `tmp/_${key}.mp4`, V2 used `tmp/_${key}_v2.mp4`.
   Merged to `tmp/_${key}_${offer}_${arm}.mp4`, which is now collision-free
   across all three arms — the originals would have collided if the FREE and
   PAID arms had ever run concurrently.
5. **The stale `_paid` comment.** `render_ad.py` carried
   `# V2 must not send people to the free thing it is trying to upsell past`
   above a condition that actually tests `key.endswith("_paid")`. The comment
   dates from the abandoned scheme where PAID was encoded as "405-408 V2" (see
   `ads/README.md`). **Comment kept, corrected, and the correction noted inline**
   so nobody re-derives the wrong rule.
6. **The missing PAID V2.** Neither original built one; in `render_ad.py` the
   combination would have thrown a bare `KeyError`. **Now an explicit error with
   a reason**, both in the shell (before any encoding starts) and in Python. This
   is the one place I chose a louder failure than the original had. Nothing is
   dropped: the behaviour is still "no PAID V2 is produced".
7. **The 2026-07-30 tree rename.** Both originals were edited *the same day this
   handoff was written* to target the new persona-first folders, the `Aerial`
   format token, space-free filenames and the renamed 406 Persona token, and their
   summary glob widened from `../ads/40[5-8]-*/*.mp4` to `../ads/*/40[5-8]-*/*.mp4`.
   The consolidated script above matches the **new** scheme. **Kept as data**: the
   folder is a `ROWS` column rather than the hardcoded `case "$num" in` block the
   updated originals use, because a `case` that has to be edited in two scripts is
   exactly what this consolidation exists to remove. Same output paths, one place
   to change them.
8. **Argument validation in `render_aerial.py`.** The original `main()` read
   `sys.argv[1:4]` with no checks; a bad copy key produced a `KeyError` traceback
   and a bad argument count an `IndexError`. Now each of persona / OFFER / ARM is
   checked against its tuple and the usage string is the module docstring. Guards
   only — no valid invocation behaves differently.

**Added, not present in either original:** a check that `audio/bed_phrygian.wav`
exists before the loop starts, and a per-row check that the source clip exists.
The originals would fail mid-encode with an ffmpeg error and, under `set -e`,
abandon a half-built ad folder plus a stray tmp file. These are guards only —
they change no output.

**Verification of the consolidation — run, not assumed.** The two files in §10
were extracted from this document and executed against the live assets:

- All 12 `(persona, offer, arm)` copy permutations compared string-by-string
  against the original `render_ad.py` `COPY` dict: **identical**.
- All 12 rendered overlay PNGs compared to the originals with
  `ImageChops.difference(...).getbbox()`: **pixel-identical, zero differences**.
- `--offer PAID --arm V2` refused with exit 2 before any encoding.
- A full end-to-end build of 408 Segment D PAID V1 (both ratios, 9.4 s wall
  clock) produced files whose MD5s **match the shipped 2026-07-27 files
  bit-for-bit**: `28b7856a0a08d3805936bc9e0fbfb40a` (9x16) and
  `3f55dc5156bcd0b5430d3372bcdcdb80` (4x5).

**Re-verified independently during the audit**, same machine, ffmpeg 8.1,
Pillow 12.1.1:

- The `render_aerial.py` block was extracted from this file verbatim and run
  side by side with the untouched `video/render_ad.py`. All 12 permutations:
  copy lists compare equal, and `ImageChops.difference(old, new).getbbox()` is
  `None` for every one. **Zero pixel difference.**
- `paragraphs("segment-a", "PAID", "V2")` raises `SystemExit`; the shell guard
  exits 2 with `there is no PAID V2 — see JOBS above`. `bash -n` is clean and the
  script parses under macOS `/bin/bash` 3.2.57.
- The three-pass build of 408 PAID V1 was re-run into a scratch directory:
  **8.95 s wall clock**, and both MD5s reproduce the shipped files exactly. The
  bit-identical claim is real, and it means ffmpeg 8.1 + libx264 on this machine
  is byte-deterministic for these settings. It will **not** reproduce on a
  different ffmpeg build — do not treat MD5 as an acceptance test elsewhere.

**Deliberately NOT changed:**

- `set -e` (not `set -euo pipefail`). The `[ -n "$X" ] && [ ... ] && continue`
  idiom the originals use is `set -e`-safe because only the *final* command in
  an `&&` list triggers the exit, and that command is `continue`. It has been
  run in anger; I did not want to tighten the shell options and re-derive that.
- The double video encode for 4:5. See §3.
- The 62 px start size, 0.14 / 0.735 fractions, 70 px lockup gutter, 4 px stroke,
  0.35 s / 0.55 s fade, CRF 18, preset medium, AAC 192k. All shipped values.

---

## 13. Delivery

Finished `.mp4`s go to Drive, not into git — `ads/**/*.mp4` is gitignored in the
source repo. Git holds source, configs and captions.

Each ad folder carries `caption-free.md` and `caption-paid.md` with the exact
Ads Manager fields: primary text, headline, description, CTA, the ad name, plus
how to judge the test and the known caveats. **A folder holding more than one V
must open its caption with a variants block** naming each V, what differs, and
whether both are still spending. Without it a reviewer sees `_V1.mp4` beside
`_V2.mp4` and cannot tell whether V1 is dead or live.

Two rules that apply at trafficking time, from `ads/README.md`:

- **The link target must be the tracked landing page with UTM**, never the
  raw destination platform, or attribution is lost. (This one is in each caption's Notes block,
  not in README — it is a caption rule.)
- **406 and 404 target substantially the same people**, and their paid cuts
  collide the same way. Running both means bidding against yourself. Since the
  2026-07-30 rename they sit in the **same folder tree** (`ads/03-segment-b/`), which
  makes the collision visible instead of something you have to remember.

Two more from the same README, both relevant to this wave:

- **Scheduling never goes in the path.** Upload weeks split FREE/PAID pairs across
  folders and mean nothing a month later. Batching belongs in `ads/MANIFEST.md`
  or a `_batches/` view of hardlinks. Moving files is how files get lost.
- `ads/MANIFEST.md` is generated by `video/make_manifest.py` and is the index of
  record: every file, persona, format, hook, offer, version and length. Regenerate
  it after a build; do not hand-edit it.

---

## 14. Open questions

Things I could not determine from the source and did not invent.

1. **The Seedance prompts are not recorded anywhere in the repo.** I grepped the
   whole tree. The eight landscape clips exist as `.mp4` files in a gitignored
   directory; the text that generated them is gone. What survives is a one-line
   **Look:** description in each caption — and, correcting an earlier draft of
   this section, **all four concepts have one, not just 405**:

   | | FREE look | PAID look |
   |---|---|---|
   | 405 Segment A | Andean plateau city, warm late afternoon | High desert city at dusk, street lights coming on |
   | 406 Segment B | Coastal megacity at golden hour | — |
   | 407 Segment C | Farmland grid and braided river, late afternoon | — |
   | 408 Segment D | Empty snow range at dawn | — |

   The three PAID looks other than 405's are not written down anywhere. A one-line
   look is a mood note, not a prompt, so **the wave is still not reproducible from
   text** — anyone re-generating footage is writing new prompts. If the clips are
   still on the original machine, get them to shared storage before that disk
   is reset; the repo has no remote and `ads/**/*.mp4` is gitignored
   (`.gitignore` line 16).
2. **Fonts and the brand mark are binaries** and cannot travel in this
   document. Neither ships with this kit: Lora is freely available (SIL OFL)
   if you want the editorial-serif lockup, and the brand mark is your own
   square RGBA png. The shipped script falls back to the system font until a
   font file appears in `public/brand/`.
3. **macOS-only.** `/System/Library/Fonts/SFNS.ttf` does not exist on Linux and
   there is no fallback path in the code. I do not know whether anyone has tried
   this on another OS. A Linux build would need a licensed SF Pro or an accepted
   substitute, and the layout table in §5b would need re-measuring because the
   line counts would change.
4. **Why 0.55 for the ambience.** No comment records how that number was chosen
   or whether alternatives were auditioned. It reads as a by-ear decision.
   Likewise the 0.35 s / 0.55 s fade timings.
5. **`SAFE_BOTTOM` and the 22 px overhang.** I could not find any record of
   whether the PAID tagline crossing the nominal bottom-chrome line was noticed
   and accepted, or simply never checked. It is in the shipped files.
6. **Whether `-shortest` is strictly required or merely prudent** was an open
   question until I tested it; it is now answered (required, §9 trap 2). But I
   tested one ffmpeg version (8.1) on one clip. I did not test whether older
   ffmpeg builds terminate on main-input EOF.
7. **The V1/V2 test has no result yet** that I could find in the repo. The V2
   arm was built 2026-07-29 **for 405 Segment A only** (see §1 and §8). Nothing
   records spend or outcome for either arm, so there is no basis in these files
   for retiring one — and with a single persona rendered there is no basis for a
   wave-level read either. Whether the other three V2s were skipped deliberately
   or simply never got run, I could not determine.
7b. **406 says the new label in its filename and the old label in its pixels.**
   The 2026-07-30 rename retired 406's original persona label, but the shipped
   mp4 still opens with the old label and its caption is still headed by it. I
   could not find a decision recording whether the copy is meant to follow, so
   it is either a pending re-render or an accepted mismatch. Ask before
   re-rendering — the file is bit-identical to what has been reviewed.
8. **The cadence claim in the original PAID copy was unverified** and flagged
   as such in the shipped caption. It was a claim in a paid ad. Such claims
   need sign-off before spend, and I have no evidence either way.
9. **The `gen/seedance2_v1_scored.mp4` file** sits beside `seedance2_v1.mp4` and
   is not referenced by any script I read. It appears to be an earlier one-off
   score of the segment-a clip, superseded by the build script's scoring pass. I
   did not verify that by comparing the audio. (Audit confirmed the "unreferenced"
   half: a repo-wide grep for `seedance2_v1_scored` outside the binary itself
   returns nothing.)

---

## 15. AUDIT NOTES — 2026-07-30

Adversarial pass over this section against `video/`, `ads/` and `docs/`.
Everything below was run on this machine (ffmpeg 8.1, Pillow 12.1.1,
`/bin/bash` 3.2.57). No paid API was called.

### Corrected

| # | Where | Was | Is | Source |
|---|---|---|---|---|
| 1 | §1 file count | "twelve shipped 405/406/407/408 files" | **18** | `find ads -name 'BRAND_40[5-8]_*Aerial*.mp4' \| wc -l` → 18; `ads/MANIFEST.md:35-37,49-50,65-66,80-81` |
| 2 | §1 file sizes | "9 to 31 MB" | **6.7 MB to 30.8 MB** | `stat -f %z`: min 6690033 (406 PAID 4x5), max 30786149 (405 FREE 9x16 V2) |
| 3 | §1 matrix | "Full matrix **actually built** … 24 files" | 24 is what the build *can* emit; **18 exist**, FREE V2 was run for 405 only | only `ads/01-segment-a/405-…` holds `_V2` files (mtime 2026-07-29 20:43); `ads/MANIFEST.md` has one V2 row |
| 4 | §1 naming | flat `ads/[number]-[persona]-[hook]/…` with spaces in the filename, "the files on disk carry spaces" | persona-first `ads/<NN-persona>/<number>-<format>-<hook>/BRAND_…_<Format>_…`, **no spaces**, `Format=Aerial` | `ads/README.md:1-44` (rewritten 2026-07-30); `ads/MANIFEST.md` |
| 5 | §1, §7, §8, §10b | 406's original persona label | the filename/folder token was renamed (now under `03-segment-b/`); the mp4's on-screen copy still opens with the old label | `video/build_ads.sh:18,22,34`; `ads/README.md:29,37-41,77` |
| 6 | §4 | AAC "~192-195 kbps" | **192–197 kbps** | ffprobe across all 18: 192151 … 196951 |
| 7 | §4 | limiter lift "+0.4456 dB" | **+0.4455 dB** (20·log10(1/0.95) = 0.44553); measured delta 0.445527 | `astats`: raw −1.892424 dBFS, limited −1.446897 dBFS |
| 8 | §5a, §5b, §10a | shrink-loop floor "35" | **34** | `range(BODY, 33, -2)` → `[62,…,36,34]`; `video/render_ad.py:146` |
| 9 | §5b, §10a, §14.5 | PAID tagline "reaches y=1549, 23 px past 1526" | last **painted** row is **1548**, **22 px** past; 1549 is Pillow's exclusive bbox lower bound | measured `getbbox()` |
| 10 | §5c | wordmark bbox x "404–774"; FREE tagline x "353–…"; PAID tagline x "285–…" | **408–770**, **355–727**, **288–795** | measured `getbbox()` on isolated layers |
| 11 | §6 | "topmost ink 363 / bottommost ink 1246"; "78 px of clearance at the top" | those are **layout-box** values, not ink; measured overlay bbox for `segment-b_paid` is `(73, 371, 1006, 1549)`, so clearance is **86 px top and 86 px bottom** | `overlay('segment-b_paid').getbbox()` |
| 12 | §7 | "Two claims in the PAID copy are flagged unverified" | **one** (the cadence claim). The item-count/price note is a separate caption item about what is *kept off* screen | `ads/01-segment-a/405-…/caption-paid.md:75-80` |
| 13 | §9 heading | "all three" traps, then lists four | four | — |
| 14 | §9 trap 2 | single runaway measurement stated as a constant | reproduced independently (23.3 MB in 30 s, still running); byte/second figures flagged as illustrative, the non-termination as the fact | re-run of the §5d command minus `-shortest` |
| 15 | §10b | `dir`/`base` derived by `tr` from the hook → old flat path + spaced filename | `folder` is now a `ROWS` column; `base` uses the `Aerial` token and `tr -d ' '` | matches `video/build_ads.sh:32-39` |
| 16 | §12 table | "`build_aerial.sh` with `JOBS=("FREE:V1" "PAID:V1")` selected by default" | contradicted its own script — default `JOBS` is all three (24 files); `--arm V1` is the old `build_ads.sh` equivalent | §10b line `JOBS=(…)` |
| 17 | §12 | reconciliation list stopped at 6 | added #7 (the 2026-07-30 rename) and #8 (argument validation, which was added silently) | — |
| 18 | §13 | the old 406/404 label wording plus two rules | updated to the current README wording, plus the scheduling-not-in-the-path rule and `ads/MANIFEST.md` / `video/make_manifest.py` | `ads/README.md:21-24,43-44,150-153` |
| 19 | §14.1 | "[look descriptions] and none at all for 406-408" | **false** — all four FREE captions carry a `**Look:**` line; added the table | 406 "Coastal megacity at golden hour", 407 "Farmland grid and braided river, late afternoon", 408 "Empty snow range at dawn" |
| 20 | §14.7 | "The V2 arm was built 2026-07-29" | true for 405 only; added 7b for the label/copy mismatch | as #3, #5 |

### Verified correct — no change needed

- **The whole `bed.py` listing in §11 is byte-for-byte the real `video/bed.py`**,
  including the block-filtering / ~23 Hz ratchet comment. Diffed line by line.
  Measured output: 48 kHz stereo, 10.000 s, peak 0.71999. §2b is right.
- **All 12 copy strings** in §10a's `COPY` / `paragraphs()` compare equal to
  `video/render_ad.py`'s assembled `COPY` dict, curly quotes (U+201C/U+201D) and
  the U+00B7 middle dot included.
- **All 12 overlays render pixel-identical** to the originals:
  `ImageChops.difference(old, new).getbbox()` is `None` for every permutation.
- **The §5b layout table is exactly right** — every size, line count, block height
  and y range reproduces by running the real layout code. The shrink loop does
  never fire; the caption's "block auto-shrinks" line really is wrong.
- **The 285 crop offset**, `SAFE_TOP` 268, `SAFE_BOTTOM` 1526, `lock_y` 1411,
  `avail` 1073, `max_w` 950, line height 71, gap 34, mark at (310, 1419): all
  reproduce.
- **The audio graph is byte-identical in both original scripts** and quoted
  correctly, `normalize=0` included. With `normalize=1` the same mix peaks at
  −7.9 dBFS instead of −1.9: the flag is worth what the section says it is.
- **`alimiter`'s `level` really does default to true** — `ffmpeg -h filter=alimiter`
  prints `level <boolean> auto level (default true)`.
- **Font variation names**: SF Pro exposes `Heavy` and `Semibold`; Lora exposes
  `SemiBold`. The inconsistent capitalisation is real, and `font()` really does
  swallow the exception.
- **The bit-identical rebuild claim in §12 is true.** Re-ran the three passes for
  408 PAID V1 in a scratch tree, 8.95 s wall clock, and both MD5s match the
  shipped files. Then re-ran it **through the corrected §10b script**: it wrote
  `ads/02-segment-d/408-aerial-example-hook-d/BRAND_408_SegmentD_Aerial_ExampleHookD_PAID_9x16_V1.mp4`
  and `…_4x5_V1.mp4` with MD5s `28b7856a0a08d3805936bc9e0fbfb40a` and
  `3f55dc5156bcd0b5430d3372bcdcdb80` — correct path, correct name, correct bytes.
- **No elision anywhere.** Both listings compile (`python3 -m py_compile`,
  `bash -n`) and contain no `...` or "unchanged" placeholders. The only literal
  ellipses in the file are in prose and in ASCII diagrams.
- **No stripped lessons found.** Every load-bearing comment in `render_ad.py`
  (`-loop 1` / fade timeline, the Instagram-Stories font note, the brand hook
  rule, "ONLY paragraph 1 changes", the offer-shared-across-personas note) is
  present. One was *changed* deliberately and correctly: the original's
  "Montserrat … if the CapCut-style geometric look is ever wanted as a **V2**"
  now reads "as a further arm", because V2 means the hook arm in the new scheme.
  The stale `# V2 must not send people to the free thing…` comment above the
  `key.endswith("_paid")` test is quoted accurately and its correction is flagged.
- **No fabrication found.** Every model name (Seedance 2.0), filter, flag,
  constant and price-free claim traces to a real line. `gen/seedance2_v1_scored.mp4`
  is genuinely unreferenced.

### Standing risk

**The repo changed under this section while it was being audited.** At 17:38–17:40
on 2026-07-30 a concurrent process rewrote `ads/README.md`, moved every ad folder
into persona-first directories, renamed every mp4 to the space-free
`…_<Format>_<Hook>_…` form, generated `ads/MANIFEST.md` and `video/make_manifest.py`,
and edited `video/build_ads.sh` and `video/build_ads_v2.sh` to match.
`video/render_ad.py` and `video/bed.py` were **not** touched (mtime 2026-07-29
22:51), which is why every §5/§10a/§11 claim survived unchanged and only the
path/naming claims needed correcting. Corrections 4, 5, 15 and 18 above are all
that rename. **If you are reading this more than a day after it was written,
re-check `ads/README.md` before trusting any path in §1, §10b or §13.**

Not corrected, flagged instead: `video/build_ads.sh` and `build_ads_v2.sh` now
hardcode the four delivery folders in a `case "$num"` block **in both files**. The
consolidated script carries them once, as data. That is a deliberate divergence
from the current originals, not an oversight — output paths are identical, proven
above.
