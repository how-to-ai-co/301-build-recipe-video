# Making your own creative

The rest of this bundle documents what already shipped. This part is about
using the engine for ideas nobody has had yet: your own brand, your own colours,
your own generated footage, your own formats.

Read this once before you start changing things, because two of the knobs below
will quietly destroy the format if you turn them the wrong way, and the file
says which.

---

## 1. Rebranding: one file, no code

Everything a viewer reads that is not the script, plus the entire palette, lives
in `src/brand.mjs`. **No component contains a brand string.** That is deliberate:
the moment one does, a rebrand becomes a search-and-replace across every format
and somebody misses one.

**This is tested, not aspirational.** Editing only `brand.mjs` — accent orange
to cyan, background warm-black to cool-black, name, subline, button label,
platform lockup off, anchor moved — re-rendered into a completely different
looking ad with zero changes to any `.tsx` file.

```js
// src/brand.mjs
export const BRAND = {
  name: "Signal Weekly",
  avatar: "brand/your-avatar.png",
  platformLabel: null,                    // null hides the platform lockup
  freeSubline: "12,000 operators · free every Tuesday",
  cta: "Get it free",
  ...
};
```

Then drop your PNGs in `public/brand/` and render. That is the whole procedure.

### Where the output goes

`BRAND.outputRoot` decides where finished ads land. Default `"ads"` keeps them
inside the engine folder. Point it anywhere:

```js
outputRoot: "~/Documents/your-brand/ads",
```

**This is what makes one engine serve several brands.** A brand is a
`brand.mjs` plus an output folder. Copy the file, change the name, the palette
and the output root, and you are rendering for somebody else without touching a
component or a second install.

### The two colour rules that actually matter

Pick whatever palette you like, but these formats are read at arm's length, on
a phone, often at half brightness and almost always muted:

1. **`bg` against `ink` needs real contrast.** Aim for 7:1 or better. The
   shipped pair is about 15:1.
2. **`accent` has exactly one job: mark where the eye should land.** In RSVP it
   is the recognition letter; in captions it is the word being spoken. If it
   does not pop against **both** `bg` and `ink`, the format stops working as a
   reading aid and becomes decoration. Test it on a real render before you
   commit to it.

### The two knobs that will break it

**`RSVP.anchor`.** Move it left if your copy has long words. **Never centre the
word itself.** Centring slides the fixation point with word length, which is the
exact cost RSVP exists to remove, and it is what the first build got wrong.

**`RSVP.sizes`.** Coarse buckets on purpose. Making the type resize on every
word makes the read feel unstable and seasick. If long words overflow, move the
anchor, do not add more size buckets.

---

## 2. Generating your own footage and stills

`scripts/generate.py` is the runner. **Every call is a dry run until you pass
`--go`**, and it prints the payload and what it will cost first.

```bash
python3 scripts/generate.py --list              # what is available
python3 scripts/generate.py --schema seedance   # the model's real inputs, free
python3 scripts/generate.py seedance "aerial over a coastal city at golden \
    hour, slow push in, no people" --out public/footage/city.mp4
# ^ prints the payload and stops. Add --go to actually spend.
```

### Pick a model by what it refuses, not by what looks best

| Model | Use for | Will refuse or break |
|---|---|---|
| `seedance` | Landscapes, action, the best motion available | **Any human face as input.** Not image-to-video, not reference images, not even a white-background character sheet. Text-to-video with people in the prompt is fine |
| `veo` | The only one taking a face input **with** native audio and lip sync | Weapon-over-person two-shots. Rate-limits hard. Drifts in the last ~0.5s, so trim the tail |
| `kling` | Faces and props together | No audio on this tier |
| `nano` | Stills, character sheets, edits. Cheap | Returns sizes nobody asked for, so output is normalised on download |

Two rules that cost real money to learn, both in `parts/70`:

- **Reference-consistency work does not belong here.** "Make this the same
  person from another angle" trips a likeness filter on the Gemini image models
  and fails in seconds with no error text. That work goes to Kling's own image
  models.
- **Never attach a character sheet to a shot where the face is not visible.**
  The model resolves the contradiction by rendering the face somewhere anyway:
  a duplicate second person, or a shadow figure on the wall. For from-behind
  framings, drop the sheet and let wardrobe carry identity.

### Before you batch anything

Generate **one**. Take it all the way through assembly, grade, and somebody's
actual ears and eyes. Report the spend. Decide your stop-loss in advance. A
batch of twelve broken clips costs twelve times as much to discover as one.

**`scripts/generate.py` has never been executed.** It is assembled from the
project's working runner and its documented parameters, but nobody has run it.
Start with one cheap image, look at the result, and only then trust it.

---

## 3. Inventing a new format

The engine is a spine, not a template: **a script becomes a voiceover, the
voiceover becomes word-level timings, the timings drive the visuals, and the
result renders to both ratios.** A new format only replaces the visual layer.

Concretely, to add one:

1. Write `src/AdYourFormat.tsx`. Take `AdRsvp.tsx` as the model. It receives
   `words` (the timings) and `c` (its config) and returns frames. Read your
   colours and copy from `brand.mjs`; do not hardcode them.
2. Export a `durationOf(config)` so Remotion knows the length.
3. Add your format to `src/Root.tsx`, which maps a config's `format` field to a
   component.
4. Add a `format` token in `configs.mjs`. It lands in the filename, so pick
   something short and capitalised: `Rsvp`, `Voiceover`, `Aerial`, `Yours`.

You get both ratios, the naming convention, the timing sync and the build
reporting for free. That is the point of the spine.

### Ideas the spine already supports that nobody has built

These need no new infrastructure, only a component:

- **Kinetic type on generated footage.** RSVP words over a Seedance landscape
  rather than flat black. The timings already exist.
- **Split screen.** Problem on the left, output on the right, cutting on the
  beat of the read.
- **Screen recording with burned captions.** Cheapest possible proof format,
  and the one most accounts never get around to testing.
- **Single-image formats.** Nothing forces motion. A static frame with the
  timings driving only the caption is legitimate and renders in seconds.

---

## 4. What will not save you

The engine automates the mechanical parts: sync, layout, both ratios, naming,
measured durations. It cannot tell you whether an idea is good.

Two gates stay human, always, and every failure in this project's log happened
when somebody let a green check stand in for one of them:

1. **Is the performance believable?**
2. **Does the read sound right?**

Word-for-word correctness, scripted pauses and register drops are all
measurable. Whether it sounds like a person is not.

And whatever you build, **change one variable per test.** Same voiceover file,
not a re-recording. If two things move between an ad and the thing it is being
compared against, the result tells you nothing and the spend is wasted.
