# Format 1 — RSVP typography (`OneWord` in the delivery tree)

**One word at a time on near-black, held at a fixed anchor, recognition letter
in the accent colour, synced to a voiceover.**

This is also the **shared scaffold** for every other format. Build it first even
if you ultimately want a different format: everything else adds a component
next to `AdRsvp.tsx` and reuses the same timings, bed, grade and build
machinery.

## Why this format first

Zero generation spend. No API key. No footage. If you reuse the voiceover of an
existing ad, no new audio either, which makes it the cheapest honest format test
you can run: same voice, same script, same music, only the presentation moved.

It is also the cheapest thing to be wrong about. Twenty minutes and nothing but
electricity.

## What RSVP actually is

RSVP is rapid serial visual presentation, the Spritz technique. **It is not
Bionic Reading, and the distinction is load-bearing.** Bionic Reading bolds word
openings in *running text* to guide your eye along a line. With a single word on
screen there is no line to travel, so that mechanism does nothing.

**The whole trick is the fixed anchor.** The recognition letter sits at the same
x on every single word and the word is laid out around it, so the eye never
moves and never re-hunts. An early build centred each word instead, which slid
the anchor left and right with word length and reintroduced exactly the cost
RSVP exists to remove.

If you touch `AdRsvp.tsx`, keep the anchor fixed.

## Verified

This is the code that is actually in `engine/`, not a transcription of it. In
the reference build this format was rendered end to end: frames were checked by
eye in both ratios, and a full rebrand through `brand.mjs` alone was rendered
and checked too.

Once you supply a voiceover and add a config entry, one command produces both
ratios, named to the delivery convention (see `parts/80-naming-and-delivery.md`):

```
ads/01-audience/NNN-oneword-yourhook/
  YOURBRAND_NNN_Audience_OneWord_YourHook_Tell_FREE_9x16.mp4
  YOURBRAND_NNN_Audience_OneWord_YourHook_Tell_FREE_4x5.mp4
```

## Build it

```bash
npm install
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python3 scripts/bed.py
```

Then per ad:

```bash
python3 scripts/timings.py public/audio/vo_NNN.wav public/words/NNN.json
python3 scripts/prosody.py public/audio/vo_NNN.wav public/words/NNN.json
# add one entry to src/configs.mjs, using the voEnd that timings.py printed
./build.sh NNN
```

`voEnd` is the end time of the last word. **Do not guess it.** Too low and the
end card cuts into the read; too high and the ad ends on a held word and
silence.

## Assets

The fonts (Lora and the Montserrat variable font) and the music beds ship in
the bundle. The rest is yours to supply:

- **Voiceover.** There is no sample voiceover in the bundle. Generate your
  first one with ElevenLabs or record it yourself, save it as
  `public/audio/vo_NNN.wav`, then run `timings.py` and `prosody.py` on it as
  above. The timings file it produces (`public/words/NNN.json`) is what drives
  the format.
- **Brand PNGs** (avatar, wordmark) go in `public/brand/`, under the filenames
  `src/brand.mjs` points at.

The music bed can also be regenerated with `python3 scripts/bed.py`. It is
originally composed, so unlike a track someone found it carries no licensing
exposure.

## Making it yours

Nothing in `AdRsvp.tsx` is brand-specific. Name, subline, button, avatar,
palette, anchor and type sizes all live in `src/brand.mjs`. See
`parts/90-make-it-your-own.md`, including the two knobs that will silently
destroy the format if you turn them the wrong way.

---

## The source

**The code is not reproduced here, on purpose.** It lives in `engine/`, which is
the thing that actually runs. A second copy in this document would drift from it
the first time somebody edits one and not the other, and that has already
happened twice.

Read the real files:

| File | What it is |
|---|---|
| `engine/src/brand.mjs` | **Start here.** Name, end-card copy, palette, and the format's visual knobs. No component holds a brand string, so this is the only file a rebrand touches. |
| `engine/src/AdRsvp.tsx` | The format. The long comments are load-bearing: they record why the anchor is fixed and why an earlier centred build was wrong. |
| `engine/src/configs.mjs` | One entry per ad. The only file you edit to add one. |
| `engine/src/Root.tsx` | Compositions, generated from `configs.mjs`. Maps a config's `format` to a component. |
| `engine/src/theme.ts` | A thin re-export. The palette itself is in `brand.mjs`. |
| `engine/scripts/timings.py` | Voiceover to word timings. Prints `voEnd`. **Read the transcript it prints.** |
| `engine/scripts/prosody.py` | Catches uptalk you would otherwise have to hear. Does not replace listening. |
| `engine/scripts/bed.py` | The music bed. Originally composed, so no licensing exposure. |
| `engine/scripts/grade.py` | The realism pass. Generated footage only. |
| `engine/scripts/generate.py` | Replicate, for your own footage and stills. Dry run until `--go`. |
| `engine/build.sh` | Renders every ad in `configs.mjs`, both ratios, named to convention, with measured durations. |

Everything is commented in place. If you want to know why a number is what it
is, the answer is next to the number.
