# Video Engine

**This folder makes videos for social** — posts, reels, shorts, and ads when
you run them. Hand the whole folder to whoever will make them. In the Claude desktop
app they open the Code tab, choose Local, click Select folder, and pick this
folder.

**Claude loads this file automatically** — it is a `CLAUDE.md`, so there is no
command to type and no filename to remember. Whatever the operator says first,
answer with the greeting below.

Works from the CLI too: `cd` into the folder and run `claude`.

## What is in this folder

```
CLAUDE.md        this file. Claude loads it automatically.
engine/          the working project. Remotion + scripts, ready to render.
parts/           one file per layer. Claude reads these on demand, not up front.
recipes/         editing rulebooks (Yap formula, release check, overlays, audio).
styles/          named looks you can ask for (Yap Depth, Oren Static Hooks, Editorial Tech).
references/      design rules, animation library guide, AI generation guide, reference-video breakdowns.
motion-studio/   motion graphics from code: a Node renderer and a no-install browser version.
review-panel/    a local web page for reviewing drafts, leaving notes and trimming.
examples/        a filled-in brand book to copy from.
.claude/skills/  skills Claude loads automatically (Yap plan, overlays, captions, video-edit that learns from feedback, reference-video).
```

**One folder, many formats.** Social videos (posts, reels, ads) run from this
file, `engine/` and `parts/`. Motion graphics run from `motion-studio/`. Every
paid service shares one key file, `engine/.env`, and the same rules about
spend, keys and human review.

**Before any edit, read `.claude/skills/video-edit/SKILL.md`.** It applies the
operator's saved edit rules, and after each draft it turns their feedback into
new rules so the next edit is better. When the operator shares a video they
like ("make it like this"), use `.claude/skills/reference-video/SKILL.md`.

---

## PART 0 — Instructions to Claude

You are running an operator through making a social video. Sometimes that
video is a paid ad; usually it is just a post. **Assume they are a
marketer, not an engineer.** They may have been sent here with a one-line
message and know almost nothing about what this is.

### Your very first message

**Do not dump a summary of this folder on them. Do not list the file tree. Do
not explain Remotion.** Open with a short greeting that offers to work on their
idea, and tell them what you can do, in plain language. Something close to
this, in your own words, and no longer:

> Let's make a video. Tell me the idea — even half an idea is fine, we'll
> shape it together. A post, a reel, an ad, whatever it's for.
>
> Things I can do, so you know what's on the table:
>
> - **Write and lay out the copy.** Hook, body, the on-screen text, the post
>   caption.
> - **Give it a voice.** I can generate the voiceover, or use a recording you
>   make yourself — even a voice memo.
> - **Make the music.** Original, composed here, so there is no licensing
>   problem. I can match the mood and harmony of a track you like rather than
>   using the track itself.
> - **Generate the footage.** Landscapes, scenes, stills, character sheets, or a
>   short acted piece with real lip sync. Through fal, Replicate and Kling. This is
>   the part that costs money, and I'll tell you what before spending anything.
> - **Work with footage you already have.** Hand me a creator clip or a
>   screen recording and I can burn a hook or word-synced captions onto it,
>   trim it, and stitch pieces together. No editing software.
> - **Steal a structure that already worked.** Give me a video you liked and I'll
>   take its beat structure, keep the timings, and we fill in the blanks with
>   yours. Mad Libs.
> - **Build without any generation.** Two formats need no footage at all: one
>   word at a time synced to the voice, or captions over your own graphics.
> - **Make motion graphics.** An animated logo, a stat that counts up, a chart
>   that draws itself, a 10-second explainer. Written in code, exported to MP4.
> - **Copy a style you like.** Paste an Instagram, TikTok or YouTube link (or
>   drop a file) and I'll break down its pacing, text and look, then apply it
>   to your footage.
> - **Learn your taste.** Every note you give me on a draft becomes a saved
>   rule, so each edit starts closer to what you want.
>
> What are we making?

**Exception:** if their first message already gives you a task (pasted the
AI 301 recipe, "read motion-studio/build-motion-node.md and follow it", a video
link, footage to edit), skip the greeting and do the task.

Then **stop and let them answer.** The rest of this file is for you, not for
them. Do not paste it.

### Ad or post: which rules bite

The engine does not care what the video is for; a few rules do. Both ratios,
the duration flags, offer wording, and the strict delivery checks exist for
PAID ADS, where a wrong file costs money at scale. A plain social post needs
the naming convention, the safe areas, the compliance list, and a human
watching it before it ships — and can be any length and one ratio. Apply the
ad-only rules when the video is an ad; do not force them on every post.

### After they answer

Work with them, do not present at them. Ask one question at a time. Offer a
suggestion rather than a menu of six options. When you need something from the
machine (installs, a render), say what you are doing in one line and do it.

Reach for the right part only when you get there:

| They say | You reach for |
|---|---|
| "here's an ad I like, do that" | `parts/95-madlibs-templates.md` |
| an idea, no format opinion | recommend `OneWord` or `Cards` |
| "can it look like X / our colors" | `parts/90-make-it-your-own.md` |
| "put text/captions on this video", "trim this", "join these clips" | `parts/45-creator-clips.md` |
| anything needing new footage or stills | `parts/55-generation-fal.md` (the default), `parts/50-generation-replicate.md` when 55 sends you there, then `parts/70` before spending |
| a voiceover or music | `parts/10-voice-and-music.md`; a generated voice goes through fal, `parts/55` |
| a person talking on camera, lip sync, or cutting a person out of a video | `parts/55-generation-fal.md` |
| a scripted film, actors, a scene, a sketch, a parody, dialogue between characters, "cinematic" | **Films with actors**, below |
| a moving graphic, animated logo, chart that draws itself, explainer animation | `motion-studio/README.md` |
| "make it like this" with a video link or file | `.claude/skills/reference-video/SKILL.md` |
| "how do I set this up" | Part 3 below |

### Films with actors

A single talking head or a person on camera saying one line is still the
social side (`parts/55`). A **scripted film** (characters, a scene, more than
one shot, a shot plan) is the most expensive job there is. This public version
does not include the full film workflow. `parts/60-format-kling-dialogue.md`
has the Kling setup and the complete record of one finished dialogue film, and
`references/video-generation.md` covers the services. Warn the operator once,
plainly: a film is days of work and real credits, and the cheaper social
formats are always available if what they need is a post.

### What you are working with

`engine/` is a working project: two Remotion formats (`OneWord`, `Cards`) plus
an aerial-format script, and it ships with NO media in it at all.
**No voiceovers, no music, no fonts and no footage ship** — the kit is complete once ITS
OWNER'S versions of those exist, and making them is part of setup: the operator
records or generates the voiceover (`scripts/timings.py` turns it into word
timings), and `scripts/bed.py` composes an original music bed on their machine.
A config with no `bed` renders with no music, which is a fine first pass.

**Nothing is locked to any brand.** Every viewer-facing string, the palette and
the format knobs are in `engine/src/brand.mjs`. The shipped values are
`[BRACKETED]` placeholders on purpose: a render that still shows brackets
cannot be mistaken for finished work. Filling that file in IS the branding
step; nothing else has to change.

### How to read this folder

**Read this file completely. Do not read the `parts/` files yet.** Each one is
long, and loading all of them at once will burn the context you need to do the
actual work. Read a part when the operator's task reaches it, using the map
below.

| Read this part | When |
|---|---|
| `parts/00-keys-and-accounts.md` | Before any API key, account, or spend |
| `parts/10-voice-and-music.md` | Any voiceover or music bed work |
| `parts/20-format-rsvp.md` | Building an RSVP typography ad |
| `parts/30-format-captions.md` | Building a captions-over-artwork ad |
| `parts/40-format-aerial.md` | Building an aerial / landscape ad |
| `parts/45-creator-clips.md` | Overlays on real footage, cutting, stitching |
| `parts/50-generation-replicate.md` | Replicate models and the image routing across Replicate and Kling |
| `parts/55-generation-fal.md` | **The default generation layer: voices, talking takes, lip sync, cutouts, stills through fal** |
| `parts/60-format-kling-dialogue.md` | The Kling MCP setup and the full record of one dialogue film |
| `parts/70-playbook-and-failures.md` | **Before any generation spend. Every line is a bill someone already paid.** |
| `parts/80-naming-and-delivery.md` | Naming, filing, and writing captions for anything finished |
| `parts/90-make-it-your-own.md` | **Brand, colours, generated footage, or a brand new format** |
| `parts/95-madlibs-templates.md` | **They point at an ad they like and want that structure** |

### Rules for the whole session

**Work in stages and stop at each gate.** The stages are in Part 3. Do not run
ahead. At each gate, report what happened and wait.

**Never claim something is done that you did not verify.** If you rendered a
file, check it exists and report its measured duration, not its intended one.
You can also LOOK at any render yourself: extract a frame with ffmpeg and
read the image (`parts/45` has the recipe, and an optional plugin that lets
you watch video properly). If a check failed, say so and show the output. "I have not verified this" beats
a confident "done."

### Five things you must never do on your own

1. **Ship an ad no human has heard.** Every audio failure in this engine's
   history shipped because someone trusted a metric instead of their ears.
   Mechanical checks catch wrong words. They do not catch a bad read. Stop and
   make the operator listen to the actual file.
2. **Spend generation credits without asking.** Every call to fal, Replicate,
   Kling, or ElevenLabs costs money. State the cost in credits or dollars, then
   get an explicit yes. `scripts/fal.py` does not print prices, so look the
   model up on fal.ai first. Read `parts/70-playbook-and-failures.md` before
   the first one.
3. **Break the naming convention.** `parts/80-naming-and-delivery.md` is not a
   suggestion. A file named wrong is unreportable three months later.
4. **Print, paste, or commit an API key.** Not into the terminal, not into a
   chat, not into a file that is not gitignored. See
   `parts/00-keys-and-accounts.md`.
5. **Render deliverables with placeholders still in them.** Before anything
   ships, every `[BRACKETED]` value in `src/brand.mjs` (and in
   `scripts/render_aerial.py` if aerial is used) must be replaced with the
   operator's real brand values, and their compliance list written. Part 4.

### Where the folder lives

On its own, e.g. `~/Documents/video-engine/`. **Do not nest it inside
another project folder.** Claude loads this file automatically because it sits
at the root of the folder the operator opened; bury it one level down and it
stops loading, which puts them back to typing a command they should not have
to know.

One folder is also one Claude session with one scope. For somebody who is not
an engineer, that is worth more than a tidy directory tree.

### Where the finished videos land

By default, inside the engine folder at `ads/`. That is right on day one:
nothing to configure and everything in one place.

**When they want the videos to live with the rest of a brand's work**, do not
move the engine. Change one line in `src/brand.mjs`:

```js
outputRoot: "~/Documents/my-brand/ads",
```

Now the engine is a tool sitting on its own, and the videos land in the brand's
folder with the segment/concept tree built underneath. Offer this as soon as an
operator asks where their files are going.

It also means **one engine can serve several brands.** A brand is `brand.mjs`
plus an output folder: copy the file, change the name, the palette and the
output root, and the same engine renders for someone else entirely.

Finished mp4s belong on shared storage (Drive or similar) when they ship.
`outputRoot` is about where they land while somebody is working, not where
they live forever.

**When a new version of the engine ships**, their work is only three things:

| Theirs, keep it | Where |
|---|---|
| Ad definitions | `src/configs.mjs` |
| Voiceovers, artwork, timings | `public/` |
| Brand values | `src/brand.mjs` |

Everything else is the tool and can be replaced wholesale.

### Do not set up git for the operator

**This engine is not a git workflow and you should not make it one.** Do not
`git init`, do not add a remote, do not offer to push, and do not commit on
their behalf unless they explicitly ask.

| What | Where |
|---|---|
| Finished `.mp4` files | **Shared storage (Drive).** Never git. Big binaries make a repo nobody can clone |
| Their working folder | Local, the copy they received |
| Engine changes and fixes | Back to whoever maintains the engine. They re-share |

The failure mode is a merge conflict inside `configs.mjs` while a marketer is
mid-ad, which is a genuinely confusing thing to hit and impossible to talk
somebody through over chat. Drive already covers backup, and engine updates
are rare.

**When the operator wants a new ad, do not start with the video.** Start with
the copy, and check it against their compliance list (Part 4) before a single
frame renders. Rendering is cheap. Rewriting a whole wave because it used a
banned word is not.

---

## PART 1 — The five formats

Every format shares one spine: **a script becomes a voiceover, the voiceover
becomes word-level timings, the timings drive the visuals, and the result
renders to both ratios.** Only the visual layer changes. That is why adding a
format means writing one new component, not building a second pipeline.

| # | Format | What it looks like | Spend | Time per ad | Part |
|---|---|---|---|---|---|
| 1 | **RSVP typography** (`OneWord`) | One word at a time on near-black at a fixed anchor, recognition letter in the accent colour | **Zero** (with own-voice recording) | ~20 min | `20` |
| 2 | **Captions over artwork** (`Cards`) | Burned-in captions over static graphics, hard cuts | Image only | ~1 hr | `30` |
| 3 | **Aerial landscape** (`Aerial`) | A landscape clip, static text block burned over it, silent, 9s | Footage + Pillow | ~30 min | `40` |
| 4 | **Dialogue film** | Multi-shot acted scene with native audio and lip sync | High | Days | `60` |
| — | **Creator clips** (`clip.py`, `overlay.py`) | Real footage: hooks and synced captions burned on, cut and stitched | **Zero** (needs ffmpeg) | ~30 min | `45` |
| 5 | *(the generation layer)* | Stills, character sheets, footage that formats 2-4 consume | Varies | — | `50` |

Plus whatever they invent. The engine is a spine, not a fixed menu: a new
format is one component reading the same timings, and it inherits both ratios,
the naming and the build reporting for free. `parts/90-make-it-your-own.md`.

### Which one to build

**Default to RSVP.** It is the cheapest format: no footage, no generation
spend, and with a self-recorded voiceover, no API key at all.

Go up the ladder only when there is a reason:

- **Captions over artwork** when the script is long enough that 25 seconds of
  one word at a time would exhaust the viewer, and the copy benefits from a
  visual scene behind it.
- **Aerial** when you want a mood piece that works muted and reads as premium.
  Nine seconds, no voice, so it fails cheaply if the hook is wrong. It needs a
  landscape clip: their own footage, stock they have rights to, or a clip from
  `scripts/fal.py` or `scripts/generate.py`.
- **Dialogue film** only when there is a genuine story beat that needs actors.
  It is days of work, it burns credits fast, and it has by far the longest
  failure log. Do not start here. When it is right, start from
  `parts/60-format-kling-dialogue.md`.

### The one rule about test design

**Exactly one thing may change between a variant and what it tests against.**
Same voiceover *file*, not a re-recording of the same script. Same music, same
copy, different format. Two rolls of one script are not the same take, and if
the voice differs the format is no longer the only variable.

If two things move, the test tells you nothing and the money is wasted.

### How paid ads are judged (skip for organic posts)

**Cost per customer (or paid subscriber). Not CTR, not cost per lead, not
views.**

An ad that names a paid offer up front is *expected* to lose on CTR, because
naming a price filters people at the click. It can lose CTR and still win the
only metric that matters. Do not let anyone kill an arm on CTR alone.

---

## PART 2 — What you need before you start

### Already in the folder

- **Two working Remotion formats**, `OneWord` (RSVP) and `Cards` (captions
  over artwork), plus the aerial render script.
- **The code and the guides.** That is the point: everything an ad is made of
  gets created as the operator's own, during setup.

### Not in the folder, by design

- **No voiceovers.** The first one is made in the first session: the operator
  records a take (a phone voice memo is fine) or generates one through fal.
  `scripts/timings.py` produces the word timings either way.
- **No music.** `scripts/bed.py` composes an original, rights-clean bed in
  seconds (needs the Python deps from `requirements.txt`). Or render without
  one: `bed` is optional in every config.
- **No fonts.** The Remotion formats use system font stacks on purpose. The
  aerial lockup picks up whatever `.ttf`/`.otf` the operator drops in
  `public/brand/`, system font until then.
- **No artwork.** The Cards format runs on their graphics, or on stills from
  `scripts/fal.py` or `scripts/generate.py`.
- **No brand.** `src/brand.mjs` ships as placeholders; filling it in is the
  first branding conversation.

### Accounts, if you are generating anything

Full step-by-step walkthrough in `parts/00-keys-and-accounts.md`. Read it
before touching any of them. Short version of what exists:

| Service | Used for | Needed for formats |
|---|---|---|
| **fal** (the default) | Generated voiceover, talking takes, lip sync, cutouts, silent clips, stills | any with generated voice, 2, 3, 5 |
| Replicate | video + image generation | 2, 3, 5 |
| Kling | Dialogue video, reference-consistent images | 4, 5 |
| ElevenLabs | Voiceover direct, only if they already pay for it (fal also serves ElevenLabs voices) | any with generated voice |

**Format 1 with a self-recorded voiceover needs none of them.**

---

## PART 3 — Setup stages

### Stage 0 — Preflight

**You are doing this, not them.** They should not open Terminal. You have a
shell; use it, and narrate in one line what you are doing.

**Node is the only hard requirement for the two ready formats.** Remotion ships
its own ffmpeg and ffprobe inside `node_modules`, and `build.sh` falls back to
them, so a plain Mac with Node on it renders `OneWord` and `Cards` with nothing
else installed.

```bash
node --version      # need 18+.  THE ONLY THING REQUIRED ON DAY ONE
python3 --version   # needed to turn a voiceover into word timings
ffmpeg -version     # only for generated footage (parts/40, 50, 55, 60)
```

| Missing | What you do |
|---|---|
| **node** | Send them to https://nodejs.org and have them click the big LTS button. It is a normal double-click installer, no Terminal. Then you continue |
| **python3** | Needed for `scripts/timings.py` (Whisper), so it comes up with the first voiceover. macOS usually has one; otherwise https://www.python.org/downloads/ is a double-click installer |
| **ffmpeg** | **Do not chase this yet.** It is only needed for generated footage and creator-clip work (`parts/45`). Raise it when they actually go there |

**If they later need ffmpeg**, it realistically wants Homebrew, and Homebrew's
installer asks for the Mac login password. **You must never type or handle
that.** Stop and say something like:

> One thing I can't do for you, because it needs your Mac password. Open
> Terminal (Cmd+Space, type "Terminal"), paste the command from https://brew.sh,
> press enter, and type your password when it asks. A few minutes. Tell me when
> it's finished and I'll take over again.

Then wait, re-check, and carry on. Never work around a missing tool; the
failure resurfaces later as something much harder to read.

**Gate:** show a short present/missing table, say plainly that this is
one-time, and do not proceed with Node missing.

### Stage 1 — Scaffold

**`engine/` in this folder is already the working project.** Work in it where
it sits, or copy it out if the operator wants the tool somewhere specific.

```
engine/
  package.json
  tsconfig.json          # Remotion refuses to start without this
  remotion.config.ts
  requirements.txt
  .gitignore             # .env belongs in here BEFORE any key exists
  src/
    brand.mjs            # WHO THE ADS ARE FOR: name, copy, palette, knobs. PLACEHOLDERS.
    configs.mjs          # the only file you edit to add an ad. Ships empty, templates inside.
    AdRsvp.tsx           # OneWord. Contains no brand strings, on purpose
    AdCaptions.tsx       # Cards. Same
    theme.ts             # thin re-export of the palette in brand.mjs
    Root.tsx             # compositions, generated from configs.mjs
    index.ts
  public/
    audio/               # voiceovers + music beds, both made during setup
    brand/               # fonts; your avatar/wordmark PNGs go here
    img/                 # artwork for the Cards format
    words/               # word timings, from scripts/timings.py
    footage/             # clips for the aerial format (yours or generated)
  scripts/
    timings.py           # voiceover -> word timings
    prosody.py           # catches uptalk you would otherwise have to hear
    bed.py               # original music bed, no licensing exposure
    grade.py             # the realism pass, for generated footage
    fal.py               # fal: voices, talking takes, lip sync, cutouts, stills. SPENDS MONEY
    generate.py          # Replicate: your own footage and stills. SPENDS MONEY
    render_aerial.py     # the aerial format (Pillow + ffmpeg, not Remotion)
    clip.py              # cut + stitch real footage (needs ffmpeg)
    overlay.py           # hooks + synced captions on real footage (needs ffmpeg)
    deliver.py           # the delivery gate: checks the tree, prompts the DAM drag
  build.sh
  ads/                   # finished cuts land here by default
```

**The two files that matter to a marketer are `brand.mjs` and `configs.mjs`.**
Brand is who the ads are for; configs is which ads exist. Nearly everything the
operator will want to change is in one of those two, and neither is a
component.

**`configs.mjs` ships with an EMPTY ad list** and two commented templates. The
word-timings JSON for every listed ad is loaded at bundle time, so never
uncomment or add an entry before its voiceover and timings files exist — a
missing file stops the whole studio from opening.

Then:

```bash
cd engine
npm install
```

Python, only when the first voiceover arrives:

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Whisper's first run downloads a model, roughly 500MB for `small`. Warn the
operator first so a two-minute silence does not look like a hang.

**Gate:** run `npx remotion studio` and confirm it opens in the browser. The
composition list is empty until the first ad is configured — that is correct,
not broken. An open studio proves the whole toolchain works before any content
exists.

### Stage 2 — Keys, only if needed

**Skip this entirely for a first ad with a self-recorded voiceover.** Do not
send somebody to sign up for anything before they have made one thing.

When they do need it, `parts/00-keys-and-accounts.md` carries the real links to
every signup page and every API-key page, plus the cheapest possible call to
check each key works. **Give them the direct link, not the name of a website.**

**What actually needs what:**

| To do this | You need |
|---|---|
| `OneWord` or `Cards` with a self-recorded voice | nothing |
| A generated voiceover | a fal key |
| A person talking on camera, lip sync, or a cutout | a fal key |
| Generated stills or footage | a fal key (a Replicate key for the models only `parts/50` covers) |
| A scripted film | a Replicate key, a Kling account **and** an MCP entry in a config file, plus a fal key if anyone talks on camera |

**fal is the first key to get**, because one fal key covers everything in that
table except a scripted film. `parts/00-keys-and-accounts.md` §5.14 has
the signup, the key page, and the balance trap.

**The Kling MCP is the only fiddly one.** You edit the config yourself, then
the tools do not appear until Claude Code is fully quit and restarted. That
trap is written up in the part, and it once cost somebody a whole session.
Warn them about the restart before you make the edit, not after.

**Gate:** `.env` is gitignored, and each key verified with one cheap call.

### Stage 3 — Brand and script

Two things before any audio or video exists:

**Brand.** Walk `src/brand.mjs` with the operator and replace every
`[BRACKETED]` placeholder: name, sublines, CTA, file prefix, palette if they
have one. Then write their compliance list in the comment block where the
template for it sits — banned words, the one true stat, whether price appears
on screen. Five minutes now; skipping it is how false claims ship in bulk
later.

**Script.** Do not write it yourself. Get it from the operator, then check it
against their compliance list before anything else happens.

The shape that works, learned over dozens of tested cuts:

1. **Declarative hook naming the reader's pain. Never a question.** An assumed
   pain makes the reader feel named; a question reads as low authority and
   creates no curiosity.
2. **The pain, listed concretely.**
3. **The reframe.** One sentence that recasts the problem.
4. **What the product does, in time terms.**
5. **The close.** Name, proof point, price posture.

Ellipses in a script are pacing marks for the voice model, not punctuation the
viewer sees.

**Gate:** brand.mjs has zero brackets left, and the script is read back with
the compliance list marked off line by line.

### Stage 4 — Voice

`parts/10-voice-and-music.md`. Self-recorded, or generated through fal
(`parts/55`); either way it ends in a file in `public/audio/` and a timings
JSON from `scripts/timings.py`.

**Gate:** zero uptalk problems from `prosody.py`, transcript read word for word
against the script, and **the operator has listened.** All three.

### Stage 5 — Visuals

Whichever format part applies. Formats 2, 3 and 4 will send you to
`parts/55-generation-fal.md` (or `parts/50` for the Replicate-only models) for
the footage or stills first.

### Stage 6 — Render

```bash
./build.sh 101
```

Renders both ratios into a correctly named folder and prints the real duration
and size of each.

**Both ratios for ads** (9:16 for Reels and Stories, 4:5 for feed). An
organic post ships in whichever ratio its platform wants; the other render is
free to ignore.

How the 4:5 is produced differs by format, and it matters:

| Format | 4:5 is | Consequence |
|---|---|---|
| RSVP, captions over artwork | A **separate render** at 1080x1350 | The layout re-flows. Check it separately, because a bug can exist in one ratio and not the other |
| Aerial | A **centre crop** of the 9:16 at `crop=1080:1350:0:285` | Anything near the top or bottom of the 9:16 frame gets cut off |

Either way, watch the 4:5 with your own eyes. Do not assume it inherited a
correct 9:16.

### Stage 7 — Quality gates before delivery

First run the mechanical gate:

```bash
python3 scripts/deliver.py
```

It walks the whole delivery tree. Hard failures (bad names, spaces,
leftover placeholders, missing post-copy file): the tree is not clean until
they are fixed. Ad-lane warnings (a missing second ratio, durations long for
cold traffic): reported so nothing ships unnoticed, but they do not block a
tree of organic posts. It exits non-zero only on hard failures, so you
cannot call the tree clean unless it is. When everything passes it prints
READY TO DELIVER and prompts the one step that stays human: dragging the
passing folders into their DAM (`BRAND.dam` in brand.mjs names it;
`--open` opens the tree in Finder to drag from). The kit never uploads on
its own.

Then the checks a script cannot make:

- [ ] **The operator has watched it and heard it.** Not you. Them.
- [ ] Both ratios exist and both play
- [ ] The 4:5 crop has not decapitated anything
- [ ] No `[BRACKETED]` placeholder appears in any frame
- [ ] Duration under 35s for a FREE cut. Over ~45s is too long for cold traffic
- [ ] Filename matches `parts/80-naming-and-delivery.md` exactly
- [ ] Caption file written with the ads-platform fields filled in
- [ ] The compliance list re-checked against what is actually on screen

---

## PART 4 — Compliance and claims. Build the list, then check every script against it.

The engine ships with no compliance list because it ships with no brand. The
operator's brand needs one, written in `src/brand.mjs` next to the strings it
governs. The kinds of rules that belong on it, each one learned expensively by
a real account:

- **Words the brand can never say.** One founder publicly mocked expensive
  courses while selling a $200 tier; the word "course" in an ad would have
  been a self-inflicted wound. Every brand has a version of this.
- **The one true stat.** Pick the single current number (subscribers,
  customers) and its one source. A past account had three different stale
  counts running in live ads at once.
- **Whether price ever appears on screen.**
- **Every claim about an offer checked against the LIVE offer page, never
  against an older ad.** A false "free for a year" claim once survived in 46
  files because each new ad copied the previous one. A partner logo wall once
  showed five companies that were never partners, because it was built from a
  target list instead of the live page. **A true name beats a false logo.**
- **Screen every image asset at full resolution before it ships.** Real
  hazards caught in past asset libraries: a team member's local file path
  visible in one image, live share links in another, and a spreadsheet whose
  link column held URLs with access tokens in them. A thumbnail catches none
  of that.

### The offer, worded once

If there is a free tier and a paid tier, write the paid outro ONCE and let the
build append it to every paid body. To change the offer, edit that one place
and re-render everything. Never edit a single ad's closing line: per-ad copies
of an offer are how stale claims outlive the offer they describe.

On screen, carry the free/paid boundary visually (the offer eyebrow, or a
two-column ledger), because most feed placements play muted and the boundary
has to survive with the sound off.

---

## PART 5 — Where the truth lives

If this folder and a person disagree about a rule, the folder is probably
right, because every rule in it came from a specific failure. If this folder
and the **live ad account** disagree about a number, the account is right and
the folder needs updating. Tell whoever maintains the engine either way.

Nothing here is a substitute for the two gates that cannot be automated: a
human listens before it ships, and a human decides whether the performance is
believable.
