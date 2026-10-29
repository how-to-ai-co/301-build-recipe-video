> # The working source is `engine/src/AdCaptions.tsx`, not this file
>
> This section was researched and audited before the format was ever executed.
> It has since been **built and rendered**, and the version that shipped in
> `engine/` is the one to use.
>
> **Verification chain (reference build):** the consolidated component was
> rendered and diffed against the five original per-campaign components it
> replaces, across multiple ads in both ratios and both offer arms — **zero
> pixel difference and zero audio-sample difference** on every one. That covers
> the dark theme, the paper theme, the `contain` fit path, the two-column
> ledger, the full logo wall and the artwork-crop path. Then the brand-config
> version in `engine/` was diffed against that: identical again.
>
> ### Five defects were found by executing it. All are fixed in `engine/`.
>
> 1. **The original `Root.tsx` wiring cannot run in this bundle.** It was
>    written for the original repo: a second config file, dozens of static flat
>    `words_*.json` imports, and composition ids that `build.sh` never asks for.
>    Replaced by a format registry keyed on the config's `format` field.
> 2. **A naive import line is a hard build error.** Re-declaring `FPS` and
>    `Word` alongside the RSVP import is rejected outright by Node's parser;
>    esbuild in transform mode silently binds `FPS` to the wrong import, which
>    is worse. Fixed by aliasing only `durationOf`.
> 3. **Timings paths derived from the ad number collide** when two arms of one
>    number have different voiceovers. Fixed with an optional `words` stem
>    override, and the composition id now carries the HookStyle token so the two
>    arms cannot overwrite each other.
> 4. **The music bed must loop or be built to length.** This never bit in the
>    original tree because every track happened to run slightly longer than its
>    composition. A short bed against a longer caption cut plays silence over
>    the tail, including the entire end card.
> 5. **The two formats used different sans stacks.** `Cards` shipped without
>    `'Helvetica Neue'` at the front of the stack and `OneWord` shipped with it.
>    Unifying them changes the pixels of every existing Cards cut, so both are
>    kept in `brand.mjs` and the discrepancy is documented there.
>
> **The component body itself was sound.** Everything below about the scene
> model, the caption grouping, the hook card, the regex-as-string rule, the
> ledger timing and the end-card size sets reproduces exactly. It was the wiring
> around it that was broken.

> ### Naming
>
> Take the delivery naming from `parts/80-naming-and-delivery.md`. The formats
> are `Cards`, `Aerial` and `OneWord`, and the hook-style token is
> `Ask` / `Tell` / `About`. Any older version-counter (`_V1`) naming you find in
> an existing tree is the dead scheme.

# Format 2 — captions over artwork (`Cards` in the delivery tree)

**A voiceover, a full-frame hook card, then static infographic artwork with the
transcript burned in underneath it, hard-cutting from one image to the next on
the beat of the read. Optionally a two-column free-vs-paid ledger before the
end card.**

In the reference build this one component carried an entire multi-audience wave:
dozens of delivered mp4s — every cut in 9:16 and 4:5 — came out of it, with
every difference between cuts expressed as a config field.

It shares the scaffold from Part 1 (RSVP): same `package.json`, same
`theme.ts`, same `timings.py`, same bed tooling. This part adds one component
file and one config list next to them.

---

## What the format is

```
 ┌──────────────────────────┐   0 → hookEnd
 │                          │   HOOK CARD. The whole opening line at 84-108px,
 │  Your hook line          │   full frame, no artwork. Each word is dim until
 │  goes right here.        │   it is spoken, so the line types itself in.
 │                          │   One or two words are in the accent colour.
 └──────────────────────────┘

 ┌──────────────────────────┐   hookEnd → bodyEnd
 │ ┌──────────────────────┐ │   ARTWORK, 980px wide, top-aligned at y=90.
 │ │                      │ │   Hard cut to the next image on the beat.
 │ │   the infographic    │ │   Optional static punch-in (zoom + focus).
 │ │                      │ │
 │ └──────────────────────┘ │   Scrim gradient fades the bottom of the frame
 │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  │   to solid so dense artwork never bleeds through.
 │ ┌──────────────────────┐ │
 │ │ caption phrase, the  │ │   CAPTION BAND, 940px, accent rule on top.
 │ │ spoken word accented │ │   4-7 words at a time from the timings file.
 │ └──────────────────────┘ │   The currently-spoken word is in the accent.
 └──────────────────────────┘

 ┌──────────────────────────┐   bodyEnd → voEnd   (PAID cuts only)
 │  FREE      │ PAID        │   THE LEDGER. Left column: what the free tier
 │  Row one   │ [logos]     │   gets. Right column: your tool logos filling
 │  Row two   │ + Extra…    │   in, then two "+" rows. Captions keep running.
 │  Row three │ + Extra…    │
 └──────────────────────────┘

 ┌──────────────────────────┐   voEnd → end
 │        (avatar)          │   END CARD. Avatar, brand name, subline,
 │       Your Brand         │   the CTA button, and on paid cuts an extra
 │        [ CTA ]           │   line under the button.
 │       READ IT ON         │   Held 3.2s free / 3.6s paid.
 └──────────────────────────┘
```

Everything is authored in absolute pixels for a 1080x1920 frame. The 4:5 cut is
the **same layout rendered in a 1080x1350 frame**, not a crop of the 9:16 file.
See the gotcha about what that hides.

## When to use it

- You have a voiceover and real artwork worth showing. The format is a vehicle
  for infographics; without them it is just a caption over a colour field.
- You want the same creative to work muted. Everything the voice says is on
  screen, and on paid cuts the free/paid boundary is a visual, not a claim.
- You are testing a **hook**. The hook card is a separate act with its own
  timing, so swapping the opening line changes one thing and nothing else.

**When not to use it.** It is the most expensive format in the bundle to
produce: it needs a voiceover, word timings, hand-tuned scene boundaries and a
music bed. If you only want to test a hook or a format, Part 1's RSVP format
costs nothing and reuses the audio you already have. And paid cuts run long for
cold traffic — in the reference build free cuts measured roughly 24-32s and
paid cuts roughly 38-47s, and the long paid tail was a known open item, not a
feature.

## Numbering concepts and offers

Give each **concept** one number, and let the offer live in the filename as a
token, not in the number. The reference build originally gave "the paid version
of concept N" its own number series, and those ghost numbers then survived in
config symbol names and audio filenames long after the scheme died —
**one concept, one number, two offers** is the rule that ends that. If your
reporting table shows a number that only ever existed as a paid twin, someone
is using a dead scheme.

> **Landmine class, verified in the reference build.** When a build script is
> renamed or re-keyed, check what the configs actually *read*. The reference
> repo's paid-audio builder was re-keyed to concept numbers and started writing
> `vo_paid_<concept>.wav`, while the configs still read the old
> `vo_paid_<ghost>.wav` names — both sets sat on disk as byte-identical
> duplicates, so re-running the builder did **not** refresh what the renders
> read, and no error ever appeared. If you rename an output, repoint every
> consumer in the same commit, and delete the stale set.

`hookAccent` is the regex source that puts the accent colour on the
load-bearing words in the hook card; `hookSize` is the hook type size. Both are
per-cut knobs — see the hook-card section for how to set them.

**The filename convention** carries a **Format** token and has **no spaces**:

```
ads/<NN-audience>/<number>-<format>-<hook>/
    YOURBRAND_<number>_<Audience>_<Format>_<Hook>_<OFFER>_<Ratio>.mp4
    caption-free.md  caption-paid.md
```

Spaces in filenames break globbing, break some Drive syncs, and silently broke
two renders during the reference build. Number the audience folders so they
sort by share of your paying base.

---

## The scene model: zoom + focus, and why there is no Ken Burns

**There is no Ken Burns in this format and there must not be.** The standing
creative rule is hard cuts only, no crossfades, nothing moving inside a scene.
The `zoom` field is a **static punch-in chosen per scene and held**, not an
animated push. Nothing in the component reads the frame number to move artwork.

(The only Ken Burns anywhere in the reference pipeline was a pre-Remotion
prototype that used ffmpeg `zoompan` with PNG caption cards. It was abandoned
before anything shipped. If you find `zoompan` in a build script, you are
looking at a dead path.)

A scene is one image plus a window onto it:

```
{ img: "img/artwork-2.jpg", zoom: 1.5, focusX: 1, focusY: 0.75, from: 10.88, to: 15.12 }
```

- `zoom: 1` lays the whole 980px-wide artwork in the frame. Above 1 the artwork
  is drawn larger than the 980x1240 box and the box clips it.
- `focusX` / `focusY` are the **centre of interest in the artwork's own
  coordinates**: 0 is the left/top edge, 1 is the right/bottom edge, 0.5 is the
  middle. The component tries to put that point at the centre of the frame.
- It is not allowed to overshoot. The `offset()` helper clamps so the artwork
  can never be pulled past its own edge:

```ts
/** Place a focus point at the centre of the frame, but never past the artwork's
 *  own edge — otherwise a punch-in slices the title off the top or the
 *  descriptions off the right, which is exactly what it did the first time. */
const offset = (frame: number, img: number, focus: number) =>
  img <= frame ? (frame - img) / 2
    : Math.max(frame - img, Math.min(0, frame / 2 - img * focus));
```

The load-bearing lesson underneath `focusX: 1`: in the reference build one
poster's text ran to the last pixel column of the image, so any punch-in that
was not flush right sliced words. **Losing the left of an illustration reads as
a crop; losing text reads as a bug.**

The other lesson is when *not* to punch in: if a region of the artwork
contradicts the voiceover, stay wide — the contradiction is only legible when
you punch in on it, and wide also lands the title and the full structure of the
graphic.

**Scene boundaries land on the word that opens each beat**, read out of the
timings file. They are not evenly spaced and they are not guessed. Regenerating
a voiceover invalidates every one of them.

### The aspect assumption

`ART_ASPECT` is hard-coded to the aspect ratio of your standard infographic
size (1.25 for 1280x1600 artwork). The component uses it to work out where the
focus point is vertically. **Any asset whose real aspect differs gets a wrong
vertical offset in the crop path**: a taller-than-assumed image loses its
bottom instead of being centred, and a wider-than-assumed image sits too high
with dead background under it. The arithmetic is deterministic — natural height
at the 980px layout width versus the height the component assumed — so you can
compute the error per asset before rendering.

In the reference build two off-aspect assets shipped that way. The consolidated
component adds an optional per-scene `aspect` so you can fix it, but **leaving
it unset reproduces an existing render exactly, mistakes included** — never
"fix" a live ad by accident. Measure every asset's real dimensions and either
standardise your artwork to one aspect or declare `aspect` per scene.

---

## How `words.json` drives the burned-in captions

The captions are not written by hand. They are the measured word timings of the
voiceover, grouped into phrases at render time.

**1. Transcribe.** `timings.py` (Part 1) runs Whisper `small` with
`word_timestamps=True, language="en"` and writes a flat array:

```json
[ {"w":"Your","s":0.0,"e":0.32}, {"w":"hook","s":0.32,"e":0.44}, … ]
```

Every word carries a start and an end, because the caption must never gap.
**Always read the transcript it prints.** Whisper mishears brand names, and it
splits numbers: `250,000` becomes `250` + `,000` and `100%` becomes `100` +
`%`. The split numbers are repaired at render time; a misheard word has to be
caught here.

**2. Group into phrases.** `phrases()` in the component:

- Push words onto the current group. Close the group when the word ends a
  sentence *and* the group already has 3 words, or when it hits 7 words.
- Then walk each group backwards and glue any token that is punctuation-only
  (`%`, `,`, `.`) or starts with punctuation-then-digit (`,000`) onto the word
  before it. This is what puts `250,000` and `100%` back together.
- Then merge any group shorter than 3 words into the previous one, if the result
  stays at 8 words or under, so nothing reads as a fragment.

**The glue only runs inside a group, and that is not always enough.** If the
7-word cap happens to split a number's pieces across a group boundary — `100`
at the end of one group, `%` opening the next — the glue loop never sees them
together and the cards render the number broken in half. This is a
deterministic consequence of `phrases()` plus a particular timings file, it is
cosmetic, and it is not fixed by config — a fix means gluing across group
boundaries *before* grouping, which changes `phrases()` for **every** cut. Do
not change it without re-rendering and re-checking everything live. Check any
voiceover that ends on a number.

**The 7-word cap wins over sentence boundaries, and it shows.** Cards can end
mid-sentence and the next card opens with the tail of the previous one:

```
Here is your opening question line
now? Followed by the second sentence which
runs over onto this card, and then
the closing line.
```

That is the intended behaviour. It reads fine at speed because the accent
tracks the spoken word, but if you ever want sentence-clean cards you are
changing `phrases()`, not the config.

**3. Pick the group for this frame.** The caption finds the group whose span
contains `t`. Real voiceovers have silences between sentences, so when `t`
falls in a gap the component **holds the last group that finished** rather than
rendering an empty band. Without that fallback the caption would blink out
between sentences.

**4. Accent the spoken word.** Inside the group, the word where
`s <= t <= e` is drawn in the accent colour; everything else is ink.

**5. Paid cuts get one merged file.** The paid-audio builder concatenates the
body voiceover, a 0.55s gap, and the shared offer voiceover into one wav, and
merges the word arrays by shifting every outro word by `body duration + 0.55`.
So one timings file spans body *and* offer and the captions keep running over
the ledger with no extra machinery. `voEnd` is the last merged word's end plus
about 0.22s.

Because the outro is literally the same audio in every paid ad,
`voEnd - bodyEnd` is **the same constant in every single paid cut** (13.34s in
the reference build). That is a useful invariant: if a config has a different
gap, one of its two numbers is wrong.

---

## The hook card

The hook is its own act. It gets the whole frame, no artwork, at 84-108px.

**Which words appear** is `w.e <= hookEnd + hookLead`, with `hookLead`
defaulting to 0.35s. This is a filter on the *same* timings array, not a
separate script — which means the hook card content is a function of `hookEnd`
alone. Two consequences:

- `hookEnd` does not have to land at the end of the first sentence. A
  one-breath opening question can be too fast to read on its own; deliberately
  running `hookEnd` past it lets the card carry the setup line too. Several
  reference-build cuts did exactly that, with the reason recorded in a comment
  next to the number.
- Because the filter is by end-time, regenerate the timings and the card
  content can change even though `hookEnd` did not. Re-check the card after
  any re-record.

**`hookSize` is set per cut by eye, not by a formula.** The sizes used across
the reference build, by word count on the card:

| Words on card | Sizes actually used |
|---|---|
| 7 | 96-108 |
| 8 | 92-108 |
| 10 | 84-104 |
| 11 | 84-88 |
| 14 | 96 |
| 16 | 84 |

The trend is real — more words, smaller type — but there is no rule you can
apply blind. There is no auto-fit; a hook that is too long at too large a size
wraps into the vertical middle of the frame and looks broken. Render the 4:5
and look at it.

**Each word is dim until it is spoken** (`t >= w.s`), so the line assembles in
time with the read instead of appearing all at once.

### Why `hookAccent` is a string, not a `RegExp`

```ts
/** Regex SOURCE, not a RegExp: defaultProps are JSON-serialised by Remotion
 *  and a RegExp arrives at the component as an empty object. */
hookAccent: string;
hookAccentFlags?: string;
```

Remotion serialises `defaultProps` to JSON so the studio can edit them and the
CLI can pass them across a process boundary. `JSON.stringify(/keyword/i)`
produces `{}`. A `RegExp` in a config therefore arrives at the component as an
empty object, `.test` is undefined, and the render crashes — or worse, if you
guard it, silently stops accenting anything. Pass the source and build the
RegExp inside the component.

Three consequences you have to live with:

- **Escaping is doubled.** `"(keyword|really\\?)"` in JavaScript produces the
  source `(keyword|really\?)`. Writing `"(keyword|really?)"` makes the `?` a
  quantifier and the pattern matches `reall` too — a silent wrong-word accent,
  not an error.
- **The pattern is tested against the token including its punctuation**,
  because that is how Whisper emits words: `really?`, `one.`, `don't.`. Real
  patterns end up looking like `(keyword\.|up\.)` and `one\.?$`.
- **Never put `g` in `hookAccentFlags`.** `.test()` on a global regex advances
  `lastIndex`, so across a `.map()` it would match every other occurrence. The
  component builds a fresh regex per frame, which contains the damage, but the
  flag is still wrong.

The same JSON round-trip is why the theme is passed by **name** (`"dark"` /
`"paper"`) in the consolidated component rather than as an object. The original
code embedded the theme object and then had to compare `th.bg === PAPER.bg`
instead of `th === PAPER`, with a comment explaining why:
`// compare by value: themes arrive JSON-deserialised, so identity fails`.
Naming the theme removes the whole class of bug.

---

## Theme switching

Two themes, chosen per ad by which artwork carries it:

| | dark | paper |
|---|---|---|
| background | `#12100E` | `#F7F5F1` |
| ink | `#F7F3EC` | `#16130F` |
| accent | `#E4703C` | `#D9541F` |
| muted | `#8B8378` | `#6E675E` |
| dim (unspoken hook words) | `#3A352F` | `#CFC9BF` |
| caption band | `rgba(18,16,14,0.94)` | `#F7F5F1` + drop shadow |
| scrim | fade to 0.97 at 58%→70% | fade to 1.0 at 56%→68% |
| logo chip | `#F4F1EB` | `#FFFFFF` |
| wordmark | `brand/wordmark_light.png` | `brand/wordmark.png` |

**The rule that picks the theme is about the artwork, not the audience.** Light
artwork goes on paper; anything goes on dark. Dark artwork on a paper layout
punches a hole in the page — which is what the unused `inset` scene flag exists
to solve, by framing the dark asset as a deliberate card with a border and a
shadow. No reference-build ad needed it; the rule is still real.

The paper caption band gets a drop shadow and the dark one does not, because on
paper the band is the same colour as the background and needs the lift.

**One value in that table is not applied consistently and it is deliberate.**
The `muted` colour drives the end-card subtitle and the "READ IT ON" label —
but only on the compact card. On the **large** card the original components
hard-coded the paper muted grey for "READ IT ON" on *both* themes, even though
the dark theme has its own muted value, while the subtitle above it used the
theme's muted. So on the large dark card the two lines are different greys, and
reading `th.muted` for both — which is what a naive consolidation does —
visibly lightens the label on existing renders. The `READ_ON` constant in the
component preserves the original.

---

## The two-column ledger

Only on `offer: "paid"`, between `bodyEnd` and `voEnd`. It replaces the
artwork; the captions and the scrim keep running exactly as they do over a
scene.

```
FREE            │  PAID
Free row one    │  [ tool logos, filling in 2 at a time ]
Free row two    │  + Paid row one
Free row three  │  + Paid row two
```

**The split is the point.** An earlier version listed everything together,
which left the free/paid boundary to the voiceover alone and lost it entirely
with the sound off. Most feed placements play muted, so the screen has to
carry it.

**The reveal timing is derived, not configured.** `OUTRO_SPLIT = 0.46` puts the
turn 46% of the way through the outro:

```
split      = bodyEnd + (voEnd - bodyEnd) * 0.46
logos      2 at split, +1 every 0.24s
"+ Paid row one"   at split + 2.4
"+ Paid row two"   at split + 3.4
```

Since the outro audio is identical in every paid ad, those absolute offsets are
identical in every paid ad too. In the reference build this was verified across
every paid cut: each one landed the last row the same fixed interval before
`voEnd`.

### The logo wall

The right column shows the tools or partners the paid tier includes, as real
marks, not names.

**Each sits in a light chip at uniform size.** A real logo set mixes monochrome
and full-colour marks, so dropped straight onto the dark theme half of them
vanish. Chips are how real partner walls solve this and they work unchanged on
both themes.

Expect visual weight to vary: some brands only publish a lockup (icon plus
wordmark) where others publish an icon, so one entry can read lighter than the
rest. That is their actual logo, not an error.

Sourcing rules, because this matters:

- Get each mark from the brand's own site, CDN, or a reputable icon library.
- **Screen every SVG for scripts and external references before it goes in
  `public/`.** An SVG is executable markup — never drop an unread one in.
- If you lose the logo files, set the names in the accent colour rather than
  shipping broken images. (An early reference-build pass rendered the wall as
  typography for exactly this reason; logos superseded it.)
- **Keep the wall in sync with what your landing page actually delivers.** The
  reference build shipped a wall that disagreed with the live upgrade page —
  the ad promised tools the page did not list. Treat any mismatch between the
  ad's logo wall and the offer page as the highest-priority fix before paid
  spend.

---

## The end card

Two size sets, both used in the reference build, and you have to pick
deliberately.

| | `large` | `compact` |
|---|---|---|
| avatar | 260px | 230px |
| brand name | 104px | 98px |
| subtitle | 42px | 38px |
| CTA | 58px, `30px 84px` | 54px, `26px 76px` |
| wordmark | 380px | 330px |
| hold | 3.2s | 3.6s paid / 3.2s free |

The subtitle changes with the offer, not the size: the free cut carries your
full subline, the paid cut a shorter one. Paid also adds one extra line under
the button. In `engine/` all of these strings, plus the avatar and wordmark
paths, come from `src/brand.mjs`.

**Decide what the button says based on your funnel, and keep it honest.** In
the reference build the CTA named the free action on *both* offers, because the
funnel routed everyone through the free signup first and the paywall on the
other side did the selling — the ad never sent anyone to a separate paid page.
And **no price appeared on screen, ever**: a price in the creative is a claim
you then have to keep synchronised with the offer page forever.

---

## The source

### `src/theme.ts`

The `Theme` type and the two palettes. In the original tree these lived inside
one of the per-campaign components and the others imported them from it;
pulling them into their own module is the only structural change the
consolidation makes outside the component itself. In `engine/` this file is a
thin re-export of the palette in `brand.mjs`.

```ts
/** Two themes, chosen per ad by which artwork carries it. */
export type Theme = {
  bg: string; ink: string; accent: string; muted: string;
  dim: string; captionBg: string; wordmark: string; scrimTo: string;
};

export const DARK: Theme = {
  bg: "#12100E", ink: "#F7F3EC", accent: "#E4703C", muted: "#8B8378",
  dim: "#3A352F", captionBg: "rgba(18,16,14,0.94)",
  wordmark: "brand/wordmark_light.png",
  scrimTo: "linear-gradient(to bottom, rgba(18,16,14,0) 58%, rgba(18,16,14,0.97) 70%)",
};

export const PAPER: Theme = {
  bg: "#F7F5F1", ink: "#16130F", accent: "#D9541F", muted: "#6E675E",
  dim: "#CFC9BF", captionBg: "#F7F5F1",
  wordmark: "brand/wordmark.png",
  scrimTo: "linear-gradient(to bottom, rgba(247,245,241,0) 56%, rgba(247,245,241,1) 68%)",
};
```

`AdCaptions.tsx` below re-declares the scrim strings in its own `SCRIM` record
rather than reading `th.scrimTo`. They are identical text; either source works.
`th.scrimTo` is kept in the type so `AdRsvp.tsx` keeps compiling unchanged.

### `src/AdCaptions.tsx`

One component, every cut. This replaces the five near-identical per-campaign
components of the original tree.

**Not typechecked by default.** The reference project had no `typescript`
dependency installed, so `tsc --noEmit` could not run as it stood. Remotion
bundles TSX through esbuild/rspack, which strips types without checking them.
If you want a typecheck, `npm i -D typescript` first; note that a
`tsconfig.json` with `strict: false` and no `allowJs` means the `.mjs` config
import will need a `// @ts-ignore` or a `.d.ts`.

Brand strings and asset paths appear below as placeholders; in `engine/` they
come from `src/brand.mjs`.

```tsx
import React from "react";
import {
  AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";
import { DARK, PAPER, Theme } from "./theme";

/**
 * Format 2 — captions over artwork.
 *
 * ONE component for every cut. In the original tree this was five
 * near-identical files, one per campaign. Everything they did differently is
 * a config field here.
 *
 * The shape of every cut, in order:
 *
 *   0        -> hookEnd   hook card: the whole opening line, full frame,
 *                         nothing competing with it
 *   hookEnd  -> bodyEnd   artwork + burned-in captions. HARD CUTS ONLY between
 *                         scenes: no Ken Burns, no crossfades, nothing moves
 *                         inside a scene
 *   bodyEnd  -> voEnd     PAID only: the two-column offer ledger. Captions keep
 *                         running over it
 *   voEnd    -> end       end card
 *
 * FREE cuts set offer:"free" and simply have no ledger; bodyEnd == voEnd.
 */

export const FPS = 30;

export type Word = { w: string; s: number; e: number };

/** Theme is named, not embedded. Remotion serialises defaultProps to JSON, so
 *  an embedded theme object arrives as a fresh object and identity comparisons
 *  (`th === PAPER`) silently fail. The original code worked around that by
 *  comparing `th.bg === PAPER.bg`; naming the theme removes the class of bug,
 *  and it also lets the config list live in plain .mjs. */
export type ThemeName = "dark" | "paper";
const THEMES: Record<ThemeName, Theme> = { dark: DARK, paper: PAPER };

/** Scrim under the caption band so dense infographics never bleed through.
 *  The two gradients differ in stop positions AND final alpha. */
const SCRIM: Record<ThemeName, string> = {
  dark: "linear-gradient(to bottom, rgba(18,16,14,0) 58%, rgba(18,16,14,0.97) 70%)",
  paper: "linear-gradient(to bottom, rgba(247,245,241,0) 56%, rgba(247,245,241,1) 68%)",
};

/** Logo chips are light on both themes. A real logo set mixes monochrome and
 *  full-colour marks, so dropped straight onto the dark theme half of them
 *  vanish. */
const CHIP: Record<ThemeName, string> = { dark: "#F4F1EB", paper: "#FFFFFF" };

const SERIF = "Georgia, 'Iowan Old Style', serif";
const SANS = "Helvetica, Arial, sans-serif";

const FRAME_W = 980;
const FRAME_H = 1240;
const ART_ASPECT = 1.25;   // your standard infographic aspect (1280x1600)

/**
 * The tools or partners your paid tier includes, as real logos. Replace these
 * placeholders with your own set. Source each mark from the brand's own site
 * or a reputable icon library, and SCREEN EVERY SVG for scripts and external
 * references before committing it — an SVG is executable markup.
 *
 * Each logo sits in a light chip at a uniform size. Chips are how real partner
 * walls solve the mixed-colour problem and they work unchanged on both themes.
 */
export const TOOLS = [
  { name: "Tool one", file: "logos/tool-1.svg" },
  { name: "Tool two", file: "logos/tool-2.svg" },
  { name: "Tool three", file: "logos/tool-3.svg" },
  { name: "Tool four", file: "logos/tool-4.svg" },
  { name: "Tool five", file: "logos/tool-5.svg" },
  { name: "Tool six", file: "logos/tool-6.svg" },
  { name: "Tool seven", file: "logos/tool-7.svg" },
  { name: "Tool eight", file: "logos/tool-8.svg" },
];

export type Scene = {
  img: string;
  /** 1 = the whole artwork across the frame. Above 1 is a static punch-in.
   *  Nothing animates: the zoom is chosen per scene and held. */
  zoom?: number;
  /** Horizontal centre of interest, 0 = left edge of the artwork, 1 = right.
   *  If the artwork's text runs to its last pixel column, use focusX:1 — any
   *  other alignment slices words. Losing the left of an illustration reads as
   *  a crop; losing text reads as a bug. */
  focusX?: number;
  /** Vertical centre of interest, 0 = top of the artwork, 1 = bottom. */
  focusY?: number;
  /** Dark artwork on the paper layout. Inset it as a framed card so it reads as
   *  a deliberate insert rather than a hole punched in the page. */
  inset?: boolean;
  /** "crop" (default) lays the artwork out at `zoom` and clips whatever leaves
   *  the box. "contain" scales the whole image to fit, ignoring zoom/focus. */
  fit?: "crop" | "contain";
  /** Height of the artwork box. 1240 unless a cut deliberately overrides it. */
  boxH?: number;
  /** height / width of the ARTWORK ITSELF, used only to place the focus point.
   *  Defaults to ART_ASPECT; declare it for any asset that differs, or the
   *  vertical offset in the crop path will be wrong. Leaving it unset on an
   *  existing ad reproduces that ad's shipped render exactly. */
  aspect?: number;
  from: number;
  to: number;
};

export type CaptionConfig = {
  /** "free" ends after the body and uses the free end card. "paid" appends the
   *  shared offer ledger between bodyEnd and voEnd. Default "free".
   *
   *  !! THE DEFAULT IS INVERTED FROM THE ORIGINAL PAID COMPONENT, which
   *  treated any config that OMITTED `offer` as paid (the ledger and the 3.6s
   *  card). Port such a config verbatim and it silently becomes a FREE cut:
   *  no ledger, wrong end card, 0.4s short. Every entry in
   *  configsCaptions.mjs states `offer` explicitly for this reason. Never
   *  leave it out. */
  offer?: "free" | "paid";
  theme: ThemeName;
  /** staticFile paths, relative to public/. */
  vo: string;
  bed: string;
  /** Where the hook card gives way to artwork. */
  hookEnd: number;
  /** Regex SOURCE, not a RegExp: defaultProps are JSON-serialised by Remotion
   *  and a RegExp arrives at the component as an empty object. */
  hookAccent: string;
  hookAccentFlags?: string;
  /** Hook type size. Set it by word count and by eye: 7 words takes 96-108,
   *  16 takes 84. */
  hookSize: number;
  /** 1.12 default; some cuts tune 1.1. */
  hookLineHeight?: number;
  /** How far past hookEnd a word may end and still appear on the hook card.
   *  0.35 default. */
  hookLead?: number;
  scenes: Scene[];
  /** Where the body VO stops and the shared offer outro starts. Omit on free
   *  cuts; it defaults to voEnd. */
  bodyEnd?: number;
  /** Where ALL speech stops. Derived from the timings file, never guessed.
   *  On PAID cuts it is exactly last-word-end + 0.22 and the paid-audio
   *  builder prints it. On FREE cuts, take the last word's end that
   *  timings.py prints and add 0 to ~0.24s of padding yourself. */
  voEnd: number;
  /** Two end-card size sets exist; pick one deliberately per cut.
   *  Default "compact". */
  endCard?: "large" | "compact";
  /** Override the end card hold. Default 3.6s on paid, 3.2s on free. */
  endCardSeconds?: number;
};

/** 3.6s on paid, 3.2s on free. See the inverted-default warning on `offer`
 *  above: the original paid component gave 3.6s to any config that did not
 *  say "free". */
export const durationOf = (c: CaptionConfig) =>
  c.voEnd + (c.endCardSeconds ?? (c.offer === "paid" ? 3.6 : 3.2));

/** Place a focus point at the centre of the frame, but never past the artwork's
 *  own edge — otherwise a punch-in slices the title off the top or the
 *  descriptions off the right, which is exactly what it did the first time. */
const offset = (frame: number, img: number, focus: number) =>
  img <= frame ? (frame - img) / 2
    : Math.max(frame - img, Math.min(0, frame / 2 - img * focus));

const Frame: React.FC<{ scene: Scene; accent: string }> = ({ scene, accent }) => {
  const boxH = scene.boxH ?? FRAME_H;
  const inset = scene.inset === true;
  const pad = inset ? 26 : 0;

  const box: React.CSSProperties = {
    width: FRAME_W, height: boxH, overflow: "hidden", position: "relative",
    padding: pad,
    background: inset ? "#0E0C0A" : "transparent",
    borderRadius: inset ? 18 : 0,
    border: inset ? `3px solid ${accent}` : "none",
    boxShadow: inset ? "0 18px 60px rgba(0,0,0,0.28)" : "none",
    boxSizing: "border-box",
  };

  if ((scene.fit ?? "crop") === "contain") {
    return (
      <div style={box}>
        <Img src={staticFile(scene.img)}
             style={{ width: "100%", height: "100%", objectFit: "contain" }} />
      </div>
    );
  }

  const innerW = FRAME_W - pad * 2;
  const innerH = boxH - pad * 2;
  const w = innerW * (scene.zoom ?? 1);
  const h = w * (scene.aspect ?? ART_ASPECT);
  return (
    <div style={box}>
      <Img src={staticFile(scene.img)} style={{
        position: "absolute", width: w,
        left: pad + offset(innerW, w, scene.focusX ?? 0.5),
        top: pad + offset(innerH, h, scene.focusY ?? 0.5),
      }} />
    </div>
  );
};

/**
 * The offer as a two-column ledger: what is free on the left, what the paid
 * tier adds on the right.
 *
 * The split is the point. An earlier version listed everything together, which
 * left the free/paid boundary to the voiceover alone and lost it entirely with
 * the sound off. Most feed placements play muted, so the screen has to carry
 * it. Row copy below is placeholder; in engine/ it comes from brand.mjs.
 */
const OutroCard: React.FC<{ theme: ThemeName; t: number; split: number }> = ({
  theme, t, split,
}) => {
  const th = THEMES[theme];
  const shown = Math.min(TOOLS.length, Math.max(0, Math.floor((t - split) / 0.24) + 2));
  const freeRows = ["Free row one", "Free row two", "Free row three"];

  return (
    <div style={{
      width: FRAME_W, height: FRAME_H, display: "flex", flexDirection: "column",
      justifyContent: "center", gap: 34, paddingTop: 40,
    }}>
      <div style={{ display: "flex", gap: 34 }}>
        {/* FREE */}
        <div style={{ flex: "0 0 320px" }}>
          <div style={{
            fontFamily: SANS, fontSize: 26, letterSpacing: "0.18em",
            textTransform: "uppercase", color: th.muted, marginBottom: 26,
          }}>Free</div>
          {freeRows.map((r) => (
            <div key={r} style={{
              fontFamily: SERIF, fontSize: 48, lineHeight: 1.62, color: th.ink,
            }}>{r}</div>
          ))}
        </div>

        <div style={{ width: 2, background: th.muted, opacity: 0.35 }} />

        {/* PAID */}
        <div style={{ flex: 1 }}>
          <div style={{
            fontFamily: SANS, fontSize: 26, letterSpacing: "0.18em",
            textTransform: "uppercase", color: th.accent, marginBottom: 26,
          }}>Paid</div>
          <div style={{
            display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14, marginBottom: 26,
          }}>
            {TOOLS.map((tool, i) => (
              <div key={tool.name} style={{
                background: CHIP[theme], borderRadius: 14, height: 132,
                display: "flex", alignItems: "center", justifyContent: "center",
                padding: 14, opacity: i < shown ? 1 : 0,
              }}>
                <Img src={staticFile(tool.file)}
                     style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain" }} />
              </div>
            ))}
          </div>
          {([["Paid row one", split + 2.4], ["Paid row two", split + 3.4]] as
            [string, number][]).map(([label, at]) => (
            <div key={label} style={{
              fontFamily: SERIF, fontSize: 42, lineHeight: 1.62, color: th.ink,
              opacity: t >= at ? 1 : 0,
            }}>
              <span style={{ color: th.accent, fontWeight: 700 }}>+ </span>{label}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/** Group words into readable phrases: 4-7 words, break only on sentence ends. */
export function phrases(words: Word[]): Word[][] {
  const raw: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    const sentenceEnd = /[.!?]$/.test(w.w);
    if ((sentenceEnd && cur.length >= 3) || cur.length >= 7) {
      raw.push(cur);
      cur = [];
    }
  }
  if (cur.length) raw.push(cur);

  // whisper splits numbers like 250,000 into "250" + ",000" — glue them back
  for (const g of raw) {
    for (let i = g.length - 1; i > 0; i--) {
      if (/^[,.]\d/.test(g[i].w) || /^[%.,!?;:]+$/.test(g[i].w)) {
        g[i - 1] = { w: g[i - 1].w + g[i].w, s: g[i - 1].s, e: g[i].e };
        g.splice(i, 1);
      }
    }
  }

  // merge any stub under 3 words into its neighbour so nothing reads as a fragment
  const out: Word[][] = [];
  for (const g of raw) {
    if (g.length < 3 && out.length && out[out.length - 1].length + g.length <= 8) {
      out[out.length - 1] = out[out.length - 1].concat(g);
    } else {
      out.push(g);
    }
  }
  return out;
}

const Caption: React.FC<{ theme: ThemeName; groups: Word[][]; t: number }> = ({
  theme, groups, t,
}) => {
  const th = THEMES[theme];
  // The caption must NEVER gap. If t falls between two groups, hold the last
  // group that finished rather than rendering an empty band.
  let gi = groups.findIndex((g) => t >= g[0].s && t <= g[g.length - 1].e);
  if (gi === -1) {
    for (let i = groups.length - 1; i >= 0; i--) {
      if (t > groups[i][groups[i].length - 1].e) { gi = i; break; }
    }
    if (gi === -1) gi = 0;
  }
  const g = groups[gi];

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 250 }}>
      <div style={{
        background: th.captionBg, borderTop: `6px solid ${th.accent}`, borderRadius: 10,
        padding: "34px 46px", width: 940, display: "flex", flexWrap: "wrap",
        gap: "6px 18px", justifyContent: "center",
        boxShadow: theme === "paper" ? "0 10px 40px rgba(0,0,0,0.10)" : "none",
      }}>
        {g.map((w, i) => (
          <span key={i} style={{
            fontFamily: SERIF, fontWeight: 700, fontSize: 64, lineHeight: 1.16,
            color: t >= w.s && t <= w.e ? th.accent : th.ink,
          }}>{w.w}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const HookCard: React.FC<{ c: CaptionConfig; words: Word[]; t: number }> = ({ c, words, t }) => {
  const th = THEMES[c.theme];
  const hookWords = words.filter((w) => w.e <= c.hookEnd + (c.hookLead ?? 0.35));
  // Built fresh every frame and never given the /g flag: .test() on a global
  // regex is stateful and would accent only every other match.
  const accent = new RegExp(c.hookAccent, c.hookAccentFlags);
  return (
    <AbsoluteFill style={{ justifyContent: "center", padding: "0 84px" }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px 22px" }}>
        {hookWords.map((w, i) => (
          <span key={i} style={{
            fontFamily: SERIF, fontWeight: 700, fontSize: c.hookSize,
            lineHeight: c.hookLineHeight ?? 1.12,
            // dim until the word is spoken, so the line types itself in
            color: t >= w.s ? (accent.test(w.w) ? th.accent : th.ink) : th.dim,
          }}>{w.w}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const SIZES = {
  large: {
    gap: 22, avatar: 260, avatarGap: 18, title: 104, sub: 42,
    ctaTop: 34, ctaPad: "30px 84px", cta: 58,
    readTop: 54, readGap: 14, read: 26, wordmark: 380,
  },
  compact: {
    gap: 18, avatar: 230, avatarGap: 12, title: 98, sub: 38,
    ctaTop: 26, ctaPad: "26px 76px", cta: 54,
    readTop: 34, readGap: 12, read: 24, wordmark: 330,
  },
};

/** "READ IT ON" was one hard-coded grey on BOTH themes in every original
 *  large-card component, even though the dark theme has its own muted value;
 *  only the compact-card component read th.muted. Reading th.muted here for
 *  both sizes would lighten the dark large card and silently change existing
 *  renders. Kept as a constant so those renders reproduce. */
const READ_ON: Record<"large" | "compact", (muted: string) => string> = {
  large: () => "#6E675E",
  compact: (muted) => muted,
};

/**
 * The end card. All brand strings and asset paths below are placeholders — in
 * engine/ they come from src/brand.mjs. Keep the CTA honest to your funnel and
 * keep prices off the screen.
 */
const EndCard: React.FC<{ c: CaptionConfig }> = ({ c }) => {
  const th = THEMES[c.theme];
  const paid = c.offer === "paid";
  const size = c.endCard ?? "compact";
  const z = SIZES[size];
  const readOn = READ_ON[size](th.muted);
  return (
    <AbsoluteFill style={{
      justifyContent: "center", alignItems: "center", flexDirection: "column", gap: z.gap,
    }}>
      <Img src={staticFile("brand/avatar.png")} style={{
        width: z.avatar, height: z.avatar, borderRadius: z.avatar / 2,
        border: `6px solid ${th.accent}`, objectFit: "cover", marginBottom: z.avatarGap,
      }} />
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: z.title, color: th.ink }}>
        Your Brand
      </div>
      <div style={{ fontFamily: SERIF, fontSize: z.sub, color: th.muted }}>
        {paid ? "Your short subline" : "Your full subline"}
      </div>
      <div style={{
        marginTop: z.ctaTop, background: th.accent, borderRadius: 14, padding: z.ctaPad,
        fontFamily: SERIF, fontWeight: 700, fontSize: z.cta, color: th.bg,
      }}>Your CTA</div>
      {paid && (
        <div style={{ marginTop: 16, fontFamily: SERIF, fontSize: 38, color: th.ink }}>
          Your paid follow-up line
        </div>
      )}
      <div style={{
        marginTop: z.readTop, display: "flex", flexDirection: "column",
        alignItems: "center", gap: z.readGap,
      }}>
        <div style={{
          fontFamily: SANS, fontSize: z.read, letterSpacing: "0.18em",
          textTransform: "uppercase", color: readOn,
        }}>Read it on</div>
        <Img src={staticFile(th.wordmark)} style={{ width: z.wordmark }} />
      </div>
    </AbsoluteFill>
  );
};

/** Where in the outro the logo wall stops and the extra rows begin. */
const OUTRO_SPLIT = 0.46;

export const AdCaptions: React.FC<{ words: Word[]; c: CaptionConfig }> = ({ words, c }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const th = THEMES[c.theme];
  const groups = React.useMemo(() => phrases(words), [words]);

  const bodyEnd = c.bodyEnd ?? c.voEnd;
  const inOutro = c.offer === "paid" && t >= bodyEnd && t < c.voEnd;
  const split = bodyEnd + (c.voEnd - bodyEnd) * OUTRO_SPLIT;
  const scene = c.scenes.find((s) => t >= s.from && t < s.to) ?? c.scenes[c.scenes.length - 1];

  return (
    <AbsoluteFill style={{ backgroundColor: th.bg }}>
      {/* Audio sits ABOVE the branches on purpose. In the five original
          components it was repeated inside every branch, because a frame that
          renders a branch with no <Audio> in it contributes nothing to that
          frame's audio. One tree, one copy, nothing to forget. */}
      <Audio src={staticFile(c.vo)} />
      <Audio src={staticFile(c.bed)} volume={(f) => {
        const tt = f / FPS;
        // music has to lift for the end card or it vanishes the moment the VO stops
        return tt < c.voEnd ? 0.16 : Math.min(0.55, 0.16 + ((tt - c.voEnd) / 0.6) * 0.39);
      }} />

      {t < c.hookEnd ? (
        <HookCard c={c} words={words} t={t} />
      ) : t < c.voEnd ? (
        <>
          {/* artwork sits in the upper area so it never sits under the caption */}
          <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 90 }}>
            {inOutro
              ? <OutroCard theme={c.theme} t={t} split={split} />
              : <Frame scene={scene} accent={th.accent} />}
          </AbsoluteFill>
          <AbsoluteFill style={{ background: SCRIM[c.theme] }} />
          <Caption theme={c.theme} groups={groups} t={t} />
        </>
      ) : (
        <EndCard c={c} />
      )}
    </AbsoluteFill>
  );
};
```

---

## The config, field by field

| Field | Type | Required | Default | What it does |
|---|---|---|---|---|
| `offer` | `"free"` \| `"paid"` | **always state it** | `"free"` | `"paid"` inserts the ledger between `bodyEnd` and `voEnd`, changes the end-card subtitle, adds the paid follow-up line, and lengthens the end card to 3.6s. **The default is inverted from the original paid component, which treated "not free" as paid.** A config ported from an old tree without this field silently loses its ledger. |
| `theme` | `"dark"` \| `"paper"` | **yes** | — | Picks background, ink, accent, dim, caption band, scrim, logo chip and wordmark. Chosen by the artwork, not the audience. |
| `vo` | string | **yes** | — | Voiceover path under `public/`. On paid cuts this is the merged body+outro wav from the paid-audio builder. |
| `bed` | string | **yes** | — | Music bed path under `public/`. Must be at least as long as `durationOf(c)`. |
| `hookEnd` | seconds | **yes** | — | End of the hook card. Also the `from` of the first scene. Not necessarily the end of the first sentence — a cut can deliberately hold through the setup line. |
| `hookAccent` | regex **source** string | **yes** | — | Words matching this are drawn in the accent on the hook card. Escape doubled (`"really\\?"`). Tested against the token *with* its punctuation. |
| `hookAccentFlags` | string | no | none | Usually `"i"`. **Never `"g"`.** |
| `hookSize` | px | **yes** | — | Hook type size, 84-108 across the reference build. Set by eye against the rendered card, not by a formula — see the measured word-count/size table above. No auto-fit. |
| `hookLineHeight` | number | no | `1.12` | Some cuts tune `1.1`. |
| `hookLead` | seconds | no | `0.35` | How far past `hookEnd` a word may end and still be on the card. |
| `scenes` | `Scene[]` | **yes** | — | Body artwork, in order. Must cover `hookEnd` → `bodyEnd` with no holes; a hole falls through to the last scene. |
| `bodyEnd` | seconds | paid only | `voEnd` | Where the body VO stops and the offer starts. Printed by the paid-audio builder. On a paid cut `voEnd - bodyEnd` is a constant shared by every paid ad. |
| `voEnd` | seconds | **yes** | — | Where all speech stops. PAID: exactly last-word-end + 0.22, printed by the paid-audio builder. FREE: hand-set — `timings.py` prints the *last word's end*; add 0 to ~0.24s of padding yourself. **Do not guess it.** |
| `endCard` | `"large"` \| `"compact"` | no | `"compact"` | Two end-card size sets exist; pick per cut. |
| `endCardSeconds` | seconds | no | 3.6 paid / 3.2 free | Only touch this if you are changing the format. |

### `Scene`

| Field | Type | Required | Default | What it does |
|---|---|---|---|---|
| `img` | string | **yes** | — | Path under `public/`. |
| `from` / `to` | seconds | **yes** | — | Scene window. Land these on the word that opens the beat, from the timings file. |
| `zoom` | number | no | `1` | Static punch-in. Never animated. |
| `focusX` | 0-1 | no | `0.5` | Horizontal centre of interest in the artwork. `1` = flush right. |
| `focusY` | 0-1 | no | `0.5` | Vertical centre of interest. |
| `fit` | `"crop"` \| `"contain"` | no | `"crop"` | `"contain"` fits the whole image and ignores zoom/focus. |
| `boxH` | px | no | `1240` | Override only deliberately; it moves the artwork against the scrim. |
| `aspect` | number | no | `ART_ASPECT` | Artwork height/width, used only for focus placement. Declare it for any off-standard asset. |
| `inset` | boolean | no | `false` | Frames the artwork as a dark card with an accent border. For dark artwork on the paper theme. |

---

## Worked examples

### `src/configsCaptions.mjs`

Plain JavaScript, same reason as Part 1: Remotion imports it and `build.sh`
imports it, and plain ESM is the only format both read with nothing installed.
The theme is a string, which is what makes that possible.

```js
/**
 * One entry per caption-format ad.
 *
 * `number`, `audience` and `hook` drive the output filename, per
 * parts/80-naming-and-delivery.md:
 *   YOURBRAND_[number]_[Audience]_Cards_[Hook]_[OFFER]_[Ratio].mp4
 * `hook` is CamelCase with NO SPACES: spaces break globbing and Drive sync and
 * silently broke two renders in the reference build. `dir` is the delivery
 * folder, audience-first. A defect fix moves the old file OUT OF THE TREE to
 * ads/_retired/ with a WHY-RETIRED.md; a deliberate variable arm does not.
 * (Leaving a superseded file one level down inside a concept folder is a dead
 * convention: it still turns up in a Drive sync and gets run.)
 *
 * `words` is the timings file, public/words/<stem>.json. Every hook arm has
 * its own, because a rewritten hook means a regenerated voiceover means new
 * timings for EVERY word, not just the hook.
 *
 * Scene boundaries are taken from those timings and land on the word that
 * opens each beat. Regenerating a voiceover invalidates all of them.
 */
export const CAPTION_ADS = [

  // ---------------------------------------------------------------------
  // A FREE cut on the large end card, contain-fit artwork.
  //
  // If you run an Ask arm and a Tell arm of the same concept, keep them
  // within a fraction of a second of each other in total length so the two
  // cuts stay directly comparable, and judge on cost per paid conversion.
  // ---------------------------------------------------------------------
  {
    number: "101", audience: "AudienceOne", hook: "YourHookToken",
    dir: "01-audience-one/101-cards-your-hook", v: 1,
    words: "101.json",
    config: {
      offer: "free",
      theme: "dark",
      vo: "audio/vo_101.wav",
      bed: "audio/bed.mp3",
      hookEnd: 2.60,            // end of your hook line — from the timings file
      // Put the accent on the one or two words doing the work in the hook.
      hookAccent: "(keyword|doesn't)",
      hookSize: 96,
      hookLineHeight: 1.1,
      voEnd: 28.60,             // <- from timings.py, do not guess
      endCard: "large",
      scenes: [
        // contain-fit shows each artwork whole; crop-fit (the default) uses
        // zoom/focus instead. Land every boundary on the word that opens the
        // beat, from the timings file.
        { img: "img/artwork-1.jpg", fit: "contain", from: 2.60,  to: 8.02 },
        { img: "img/artwork-2.jpg", fit: "contain", from: 8.02,  to: 11.84 },
        { img: "img/artwork-3.jpg", fit: "contain", from: 11.84, to: 19.70 },
        { img: "img/artwork-4.jpg", fit: "contain", from: 19.70, to: 28.60 },
      ],
    },
  },

  // ---------------------------------------------------------------------
  // A FREE cut using punch-ins — the crop-path example.
  //
  // The VO walks a ladder-style poster, so each beat cuts to that band of
  // the artwork instead of showing the whole poster shrunk to nothing.
  // Hard cuts only — nothing moves inside a scene.
  // ---------------------------------------------------------------------
  {
    number: "102", audience: "AudienceTwo", hook: "SecondHookToken",
    dir: "02-audience-two/102-cards-second-hook", v: 1,
    words: "102.json",
    config: {
      offer: "free",
      theme: "dark",            // pick the theme by the artwork, not the audience
      vo: "audio/vo_102.wav",
      bed: "audio/bed.mp3",
      hookEnd: 2.90,            // hook line ends 2.76; card holds a beat longer
      hookAccent: "(keyword|one\\.?$)",
      hookAccentFlags: "i",
      hookSize: 96,
      hookLineHeight: 1.1,
      voEnd: 28.90,             // last word ends 28.74, padding added by hand
      endCard: "large",
      scenes: [
        // Stay wide when a region of the poster would contradict the VO if
        // punched in — and wide also lands the title and the whole structure.
        { img: "img/poster.jpg", zoom: 1.0, focusY: 0.50, from: 2.90, to: 5.56 },
        // Punch in where poster and script agree almost word for word.
        // focusX: 1 (flush right) because this poster's text runs to its last
        // pixel column — any other alignment slices words.
        { img: "img/poster.jpg", zoom: 1.5, focusX: 1, focusY: 0.50, from: 5.56,  to: 10.88 },
        { img: "img/poster.jpg", zoom: 1.5, focusX: 1, focusY: 0.75, from: 10.88, to: 15.12 },
        { img: "img/poster.jpg",    zoom: 1.0, focusY: 0.50, from: 15.12, to: 19.72 },
        { img: "img/artwork-4.jpg", zoom: 1.0, focusY: 0.50, from: 19.72, to: 28.90 },
      ],
    },
  },

  // ---------------------------------------------------------------------
  // A PAID cut — the offer-ledger example.
  //
  // The body is the SAME artwork and the SAME timings as the FREE cut. The
  // only difference is the shared offer outro appended, so bodyEnd is where
  // the free ad used to stop and voEnd is where the offer stops. The last
  // body scene runs to bodyEnd rather than to the free ad's voEnd, so the
  // artwork holds through the beat before the offer starts.
  //
  // bodyEnd and voEnd are PRINTED BY the paid-audio builder. Re-run it and
  // paste the new numbers whenever the outro changes. Never hand-edit one
  // ad's offer.
  // ---------------------------------------------------------------------
  {
    number: "103", audience: "AudienceOne", hook: "ThirdHookToken",
    dir: "01-audience-one/103-cards-third-hook", v: 1,
    words: "paid_103.json",
    config: {
      offer: "paid",
      theme: "paper",           // light artwork only — dark posters punch holes in this layout
      vo: "audio/vo_paid_103.wav",
      bed: "audio/bed.mp3",
      hookEnd: 2.35,            // the hook question + the setup line
      hookAccent: "keyword",
      hookAccentFlags: "i",
      // hookEnd can hold through the setup line, so the card carries more
      // words than the spoken hook sentence alone — size for what is ON the
      // card, not for the first sentence.
      hookSize: 108,
      bodyEnd: 24.05,           // <- paid-audio builder
      voEnd: 37.39,             // <- paid-audio builder. Always bodyEnd + the shared outro length
      scenes: [
        { img: "img/artwork-5.jpg", from: 2.35,  to: 9.30 },
        { img: "img/artwork-2.jpg", from: 9.30,  to: 15.40 },
        { img: "img/artwork-4.jpg", from: 15.40, to: 24.05 },
      ],
    },
  },

  // ---------------------------------------------------------------------
  // A FREE cut on the compact end card.
  //
  // Its PAID twin is this config with offer:"paid", the paid vo, and the
  // last scene's `to` moved to the new bodyEnd. Nothing else changes, which
  // is what makes the pair isolate the offer and nothing else.
  // ---------------------------------------------------------------------
  {
    number: "104", audience: "AudienceThree", hook: "FourthHookToken",
    dir: "03-audience-three/104-cards-fourth-hook", v: 1,
    words: "104.json",
    config: {
      offer: "free",
      theme: "paper",
      vo: "audio/vo_104.wav",
      bed: "audio/bed.mp3",
      hookEnd: 2.95,
      hookAccent: "(keyword\\.|up\\.)",
      hookSize: 88,
      voEnd: 23.95,             // free: no outro, so bodyEnd is omitted and defaults here
      scenes: [
        { img: "img/artwork-6.jpg", from: 2.95,  to: 8.82 },
        { img: "img/artwork-7.jpg", from: 8.82,  to: 13.02 },
        { img: "img/artwork-5.jpg", from: 13.02, to: 17.80 },
        { img: "img/artwork-4.jpg", from: 17.80, to: 23.95 },
      ],
    },
  },
];
```

### Wiring it in

In `engine/` this is already done: `Root.tsx` is generated from the config
list and maps a config's `format` to a component, and the words import was
tested with the actual bundler. If you wire it by hand in another tree, two
lessons from the reference build:

**The timings files may need to be imported statically.** With
`"module": "ESNext"` in `tsconfig.json`, `require()` is not defined, and a
template-literal `require(\`../public/words/${ad.words}\`)` cannot be resolved
by every bundler. Remotion's webpack bundler *does* resolve a template-literal
require into a context module over the whole directory — that was tested in
this bundle with two ads and rendered four files — but if you ever switch
bundlers, re-test it first, and the always-safe form is one static `import` per
timings file with a lookup map:

```tsx
import { AdCaptions, durationOf as capDur, FPS, Word } from "./AdCaptions";
import { CAPTION_ADS } from "./configsCaptions.mjs";

// Static, because resolveJsonModule + ESNext modules means the bundler has to
// see every path literally. One line per timings file.
import w101 from "../public/words/101.json";
import w102 from "../public/words/102.json";
import wPaid103 from "../public/words/paid_103.json";
import w104 from "../public/words/104.json";

const WORDS: Record<string, Word[]> = {
  "101.json": w101,
  "102.json": w102,
  "paid_103.json": wPaid103,
  "104.json": w104,
};

const RATIOS = [
  { name: "9x16", width: 1080, height: 1920 },
  { name: "4x5", width: 1080, height: 1350 },
];

// …inside RemotionRoot:
{CAPTION_ADS.flatMap((ad) => {
  const offer = (ad.config.offer ?? "free").toUpperCase();
  const words = WORDS[ad.words];
  if (!words) throw new Error(`no timings imported for ${ad.words}`);
  return RATIOS.map((r) => (
    <Composition
      key={`${ad.number}-${offer}-${ad.v}-${r.name}`}
      id={`Cap${ad.number}-${offer}-V${ad.v}-${r.name}`}
      component={AdCaptions as any}
      durationInFrames={Math.round(capDur(ad.config) * FPS)}
      fps={FPS}
      width={r.width}
      height={r.height}
      defaultProps={{ words, c: ad.config }}
    />
  ));
})}
```

And the render, one line per ratio. **No spaces in the output path** — that is
the rule that broke two renders in the reference build when it was ignored:

```bash
npx remotion render "Cap101-FREE-V1-9x16" \
  "../ads/01-audience-one/101-cards-your-hook/YOURBRAND_101_AudienceOne_Cards_YourHookToken_FREE_9x16.mp4" \
  --log=error
npx remotion render "Cap101-FREE-V1-4x5" \
  "../ads/01-audience-one/101-cards-your-hook/YOURBRAND_101_AudienceOne_Cards_YourHookToken_FREE_4x5.mp4" \
  --log=error
```

**Both ratios are rendered from the composition, not cropped from each other.**
Every caption composition is declared twice, at 1080x1920 and 1080x1350,
against the same component. (The *aerial* format in the reference pipeline
derived its 4:5 with an ffmpeg crop instead — do not carry that habit across
formats.)

### Assets this format needs in `public/`

None of the artwork or audio ships in the bundle; you supply all of it.

```
img/*.jpg|png                      your infographic artwork — see below
brand/avatar.png  wordmark.png  wordmark_light.png    per src/brand.mjs
logos/*.svg                        your tool/partner logos (paid cuts only)
words/*.json                       one per cut, from scripts/timings.py
audio/vo_*.wav                     your voiceovers (ElevenLabs or your own recording)
audio/bed*.wav                     your music bed, composed by scripts/bed.py
```

- **Artwork** comes from your own assets, or generate it with
  `scripts/generate.py`. Standardise on one pixel size and aspect (the layout
  maths assume `ART_ASPECT`); measure every asset that deviates and declare
  `aspect` on its scenes.
- **Voiceover**: generate with ElevenLabs or record your own, then run
  `timings.py` and `prosody.py` (Part 1) on it.
- **Brand PNGs** go in `public/brand/` under the filenames `src/brand.mjs`
  points at.
- **Screen everything.** SVG logos: zero `<script>` elements, zero external
  references, before they are committed. Artwork lifted from social posts:
  view it at full resolution first — the reference build rejected assets that
  showed live file-share links complete with access tokens, and one that
  showed a team member's local file path. Brightness-ranking will not catch
  any of it.

---

## What was merged, and what had to be reconciled

Five per-campaign components became one. Every difference between them is now
a config field. Nothing was dropped silently; here is the complete list,
including the places where the originals genuinely disagreed and a default had
to be picked.

**Identical in all five, merged with no decision:** `phrases()`; the caption
band geometry (940px, `34px 46px` padding, 6px accent rule, 64px/1.16 type,
`6px 18px` gap, `paddingBottom: 250`); the caption's hold-the-last-group
fallback; the artwork wrapper (`paddingTop: 90`, top-aligned, centred); the
music duck curve; `staticFile` asset paths.

**Config fields that were per-file constants:**

| Was | Now |
|---|---|
| `VO_END`, `HOOK_END`, `DURATION` module constants | `voEnd`, `hookEnd`, `durationOf()` |
| a hardcoded accent regex per file | `hookAccent` + `hookAccentFlags` |
| hardcoded `DARK` / `PAPER` palette per file | `theme: "dark" \| "paper"` |
| five separate config types | one `CaptionConfig` |
| `END_CARD = 3.2` vs `3.6` | `endCardSeconds`, defaulted by `offer` |

**Six real behaviour differences, and how each was handled:**

1. **Artwork fit.** Two of the originals rendered the image with
   `objectFit: "contain"` in a fixed box; the others used a crop box with
   `zoom`/`focus`. These produce visibly different frames for any artwork that
   is not the layout aspect — the same asset can appear whole in one cut and
   bottom-cropped in its paid twin. **Both kept**, as `fit: "crop" | "contain"`
   plus `boxH`. Default is `"crop"`, so a new ad gets the majority behaviour
   and legacy cuts declare their exception. Nothing was normalised behind
   anyone's back.
2. **End card scale.** Some components used a larger end card (260px avatar,
   104px title, 380px wordmark) than others (230/98/330), and the smaller card
   also shipped on some **free** cuts — so the size does not follow the offer
   and could not be derived. **Both kept** as `endCard: "large" | "compact"`,
   default `"compact"`, with `"large"` declared where it applies.
3. **Hook line height.** 1.1 in some originals, 1.12 in others — and the paid
   twin of one ad already rendered its hook at 1.12 while the free cut
   rendered 1.1, so the tree was already inconsistent. **Both kept** as
   `hookLineHeight`, default 1.12.
4. **Hook lead window.** 0.35s everywhere except one component at 0.30s.
   Checked against the two timings files that used it: no word ended inside
   the 50ms difference, so the two values produced identical cards. **Kept**
   as `hookLead`, default 0.35.
5. **"READ IT ON" colour.** The large-card components hard-code one grey on
   both themes; the compact-card component reads `th.muted`, which is a
   different grey on dark. **Both kept**, keyed off `endCard` via the
   `READ_ON` map, because the size and the colour happen to split the same
   way. Collapsing both to `th.muted` would have lightened the label on
   existing dark large-card renders without anyone noticing.
6. **What "no offer set" means.** The original paid component treated a
   missing `offer` as PAID, and its configs relied on that by omitting the
   field. `CaptionConfig` defaults it to `"free"` instead, because the free
   components were the majority and a free cut is the safer accident. **The
   flip is deliberate and it is the one place a verbatim port silently changes
   output** — every entry in `configsCaptions.mjs` states `offer` explicitly.

**Three things deliberately changed, with the reason:**

- **The theme is passed by name.** The original embedded the palette object in
  the config, which JSON-round-trips into a new object, which is why two
  places compared `th.bg === PAPER.bg`, one of them with a comment explaining
  the trap. A string name removes the trap and lets the config list be plain
  `.mjs`. The palettes themselves move into `src/theme.ts`.
- **The audio is declared once at the top of the tree** instead of being
  repeated inside every branch. Same output; one fewer way to ship a silent
  section. The reason it has to be present on every rendered frame is
  preserved as a comment.
- **`OutroCard`'s unused `from` prop was dropped.** It was passed and never
  read.

**One thing deliberately not carried over:** an early typographic `TOOLS`
array — partner *names* as strings, a stopgap until real marks were collected.
The real-SVG logo wall superseded it and the string version was dead code. But
the fallback plan it represents is written into the logo-wall section above,
because if the SVGs go missing, names in the accent colour beat broken images.

---

## Gotchas

**The 4:5 cut hides the bottom third of the artwork.** The layout is authored
for 1080x1920 and the 4:5 composition renders the same absolute pixel layout in
a 1080x1350 frame. The scrim reaches full opacity at 70% of the frame height —
y=1344 at 9:16, but y=945 at 4:5 — while the artwork box still runs to y=1330.
So roughly the bottom 31% of every image is invisible in the 4:5 cut. **Choose
`focusY` on the 4:5 render, not the 9:16 one**, and never move `paddingTop: 90`
or `paddingBottom: 250` without checking both ratios.

**Scene windows must tile without holes.** The lookup is
`scenes.find(s => t >= s.from && t < s.to)`, falling back to the *last* scene. A
gap between two scenes silently shows the final image instead of erroring. The
first scene's `from` must equal `hookEnd`, and the last scene's `to` must equal
`bodyEnd` (paid) or `voEnd` (free).

**`voEnd` is not a design choice.** It is driven by the last word's end time in
the timings file — exactly +0.22 on paid cuts, hand-set between +0.00 and
+0.24 on the free ones. Too low and the end card cuts into the read; too high
and the ad ends on a held word and silence.

**Regenerating a voiceover invalidates every number in the config.** A hook
rewrite changes the length of the *first sentence*, which shifts every
subsequent word, which moves every scene boundary. That is why each hook arm
carries a full second set of scene times that land on the same words at
different seconds. Never copy one arm's boundaries into another.

**Read the transcript and run `prosody.py` before every render.** In one
reference-build session, six of eight generated takes had a defect that would
otherwise have shipped: phantom repeated phrases, dropped words, an inserted
contraction that reversed a line's meaning, and rising terminals on
statements. Mechanical checks caught all of them.

**The music volume curve reads a module constant, not the composition fps.**
`volume={(f) => { const tt = f / FPS; … }}` uses `FPS = 30`. If you ever render
this format at another frame rate the duck will be timed wrong. Everything in
the bundle is 30fps.

**Hook cards do not auto-fit.** `hookSize` is manual. A 16-word hook at 96px
wraps past the vertical centre and looks broken; size down for long hooks and
render the 4:5 to check.

**Never edit one ad's copy of the offer.** The outro voiceover is generated
once and appended to every paid body by the paid-audio builder. To change the
offer: edit that one script, regenerate, re-run the build, re-render
everything. That is also why `voEnd - bodyEnd` is the same constant in every
paid cut, which is a cheap way to spot a config that has drifted.

**Write your own compliance list and bake it into the format.** The reference
build carried one — rules like: verify any audience-size number before it
appears in copy, no price on screen, agreed limits on faces and personal or
employer names, and a fixed vocabulary for what the product is called. Decide
your equivalents before the first render, put them where the copy is written,
and treat any violation as a build failure, not a review note.

---

## A note on what is not here

The reference build's audit trail — line-by-line verification of the original
repo, its open questions, its delivered-file inventory and its
account-specific numbers — was client material and is not part of this kit.
Every transferable lesson it produced is folded into the sections above: the
inverted `offer` default, the regex-as-string rule, the READ-IT-ON colour
preservation, the aspect-assumption arithmetic, the number-glue limitation in
`phrases()`, the stale-filename landmine class, and the rule that measured
numbers beat comments. Two habits are the summary of all of it: **read the
real timings file instead of trusting a comment, and render the frame instead
of trusting the config.**
