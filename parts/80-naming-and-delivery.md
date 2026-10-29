# Naming, filing, and delivery

> ## The `README.md` you keep next to your delivery tree is canonical. This file is not.
>
> On the project this engine came from, the convention changed **three times in
> a single day**. Folder layout went audience-first, a Format token was added,
> then the version counter was removed and replaced by a HookStyle token, and
> two format names were renamed into plain English.
>
> So: keep a short `README.md` at the root of your own `ads/` tree, and **read
> it before any build that matters.** If it ever disagrees with anything below,
> it wins and this file is out of date. What follows is the shape plus the
> reasoning, which moves much more slowly than the tokens do.
>
> `engine/build.sh` produces the paths and filenames. If you change the
> convention, change it there too, in `configs.mjs` and `build.sh`, and
> re-render one ad to check.

## The shape

```
ads/<NN-segment>/<number>-<format>-<concept>/
    BRAND_<number>_<Segment>_<Format>_<Concept>_<HookStyle>_<OFFER>_<Ratio>.mp4
    caption-free.md
    caption-paid.md
```

| Token | Changes when | Values |
|---|---|---|
| **BRAND** | never within one brand | a short all-caps brand code you pick once, e.g. `ACME` |
| **number** | the creative concept changes | 101, 102, … |
| **Segment** | never. It matches the folder | your audience segments, one capitalised word each |
| **Format** | the presentation changes | `Cards` · `Aerial` · `OneWord` |
| **HookStyle** | the opening line changes | `Ask` · `Tell` · `About` |
| **OFFER** | the destination changes | `FREE` · `PAID` |

Ratio is `9x16` or `4x5`. **No spaces anywhere.** On the source project, 62 of
94 filenames used to carry them; they break globbing, break some Drive syncs,
and silently broke two renders during a build.

### Format names say what you will see

| Token | What it is | In the code |
|---|---|---|
| `Cards` | Your graphics in sequence, with a voiceover | the captions-over-artwork component |
| `Aerial` | Footage, static text block, silent | the aerial format |
| `OneWord` | One word at a time, voiceover-synced | **RSVP**, the Spritz technique |

`OneWord` is RSVP. Code and docs use the technical name; the delivery tree uses
the plain one, so nobody needs the jargon to file a file.

### There is no version counter

`V1`/`V2` told you two files differed but never **what** differed. One concept
on the source project made the case: its live cut was V2, its retired one V1,
its new arm V3, and only a person who was there could decode that.

`HookStyle` says the thing itself. It also doubles as a record of brand rules.
On the source project the brand owner banned one hook pattern outright, and
because the pattern was a filename token, every offending file and its rewrite
could be sorted apart at a glance. Keep your own brand compliance list, and
when a rule maps to a token, the tree enforces it for you.

## The two rules that will not change

**1. A defect fix is not a test arm.**

**2. Broken cuts leave the delivery tree entirely.** They go to `ads/_retired/`
with a `WHY-RETIRED.md` naming the defect. Never into the concept folder, not
even a subfolder. The rule that makes this tree usable is:

> If a file is in a segment folder, it can be uploaded.

That is only worth anything with no exceptions. A defect sitting one level down
inside a concept folder still turns up in a search, a Drive sync and a bulk
select, and then somebody runs it.

| Situation | Where the old file goes |
|---|---|
| Defect fixed | `ads/_retired/`, out of the tree, with a note naming the defect |
| One variable moved on purpose | stays put, still spending, and the caption explains how to judge the pair |

## Why the audience segment is the top level

An ad set is an audience, so segment is the only axis that maps to how ads
actually get built, and the only one that never changes. A creative's segment
is fixed the moment it is written. Its format, offer and hook style are not.

Number the folders by each segment's share of your paying base, biggest first:
`01-`, `02-`, and so on, with niche test segments starting at `21-` so the two
groups sort apart.

**Scheduling is not in the tree.** Upload weeks change, they split FREE and PAID
pairs across folders, and they mean nothing a month later. A file can be in two
batches; a folder cannot. Batching belongs in `MANIFEST.md` or a `_batches/`
view of hardlinks, never in a path, **because moving files is how files get
lost.**

## Segments come from research, and lookalikes do not merge

Define your segments from actual audience research, then freeze the names.
When a name is retired, purge it: on the source project two dead segment names
kept resurfacing from stale documents for weeks. If you see a segment name that
is not on your current list, the source is stale.

One anonymized example of why lookalike segments stay separate: the source
project had two "manages people at a company" segments that read as one. The
research showed the companies differed in size by more than tenfold, and the
two groups wanted opposite things: one wanted their **team** using the
product's subject, the other wanted to be **the person who has it figured
out**. Merging them would have pointed one message in two directions. If two
of your segments differ that much under the surface, do not merge them.

## MANIFEST.md

Generated by `make_manifest.py`. Every file, segment, format, hook, offer and
length in one table. Regenerate after any build. Never hand-edit it.

## Keep a wave ledger, and never reuse a number

Concept numbers are permanent. Keep a table like this in your delivery README
so nobody reuses one:

| Numbers | Format | Segments |
|---|---|---|
| 101-104 | `Cards` | your four core segments |
| 105-108 | `Aerial` | the same four |
| 121-124 | `Cards` | four niche test segments |
| 131-138 | `OneWord` | all eight |

### Pairing waves: same voiceover file, not a re-recording

When a new wave tests a format against an existing wave, every new concept
**shares the exact voiceover file** of the ad it tests against. Not a
re-recording of the same script. The same file. That is what makes the format
the only variable in the pair. Record the pairing in the ledger:

| New | tests against |
|---|---|
| 131 | 102 `Tell` |
| 132 | 101 `Tell` |
| … | … |

One nuance from the source project worth copying: a hook rewrite is only
needed where the hook pattern was the problem. Some concepts already opened on
statements on purpose. For a niche segment, a direct "are you X?" question is
a strange thing to ask, so the targeting rides on the pain instead.

### One concept, two offers, one number

A PAID cut that reuses the FREE twin's artwork and appends an offer outro is
clearly the same concept. But even a PAID cut with **its own footage and its
own copy** stays on the same number if the segment, concept and format match.
Same concept with two offers is one number.

## Known-overlap trap, do not repeat it

On the source project, two concepts in the same segment folder targeted
substantially the same people, and their paid cuts collided the same way.
Running both means bidding against yourself. When you file a new concept, check
what already sits in that segment folder before it spends.

## Where files go

Finished `.mp4` files go to **cloud storage (Drive or similar), not git.** Git
holds source, configs, and captions. A repo full of video is a repo nobody can
clone.

## The delivery gate is a command

`python3 scripts/deliver.py`, run from `engine/`, checks everything above
mechanically, at two severities. Hard failures block any video, post or ad:
a filename off the convention, a number that does not match its folder, a
missing caption file (the post copy, or the Ads Manager fields for an ad),
an empty folder. Ad-lane warnings are printed but never block, because an
organic post is one ratio and any length on purpose: a cut missing its
second ratio, a FREE cut over 35s, anything over 60s. `_retired/` and
`_batches/` are skipped. It exits non-zero only on hard failures, prints
READY TO DELIVER when the tree is clean, and prompts the drag into the DAM
`BRAND.dam` names (`--open` opens the tree in Finder). Run it after every
build; a wrong file that sits in the tree will get uploaded eventually.

If you change the convention, deliver.py's filename pattern changes with
`configs.mjs` and `build.sh` — all three, then re-render one ad to check.

## The caption file

What the media buyer actually reads.

```markdown
# NNN · FREE · Segment · "Concept" · Tell

**Segment:** who, and what share of payers they are
**Format:** Cards | Aerial | OneWord
**Hook style:** Ask | Tell | About, and the opening line verbatim
**Offer:** which destination this cut sells
**Creatives:** BRAND_NNN_Segment_Format_Concept_Hook_FREE_9x16.mp4, _4x5.mp4
**Length:** NN.Ns

---

## What this tests
What the variable is, and what it is being tested against.

## VO script
The exact words, verbatim.

## Headline
## Description
## CTA

## How to judge this
Against what, on which metric. Your golden metric, essentially always:
cost per paying customer, not cost per click or lead.

## Notes
Voice used, licensing status of the music, anything unverified, and whether a
human has listened to it yet.
```

## Keep an open-issues list on the account

The source project kept a dated list like this next to the tree, and every item
on it was a real bill or a real risk. The categories generalize; audit your own
account against them:

1. **Do the ads and the landing page make the same promise?** The most
   expensive issue found on the source account: paid ads showed a specific
   set of partner-product logos while the live page listed a different set,
   with only a partial overlap. Logos make a promise specific, so a mismatch
   there outranks everything else on the list.
2. **Is every music track's licensing documented?** Anything built with
   `bed.py` is originally composed and clean. Anything found is a liability
   until its clearance evidence is filed.
3. **Whose voice is it?** If the voiceover is a cloned or stock voice rather
   than the brand's public face, write that down where the media buyer can see
   it, along with what upgrading to the real voice would cost.
4. **How long are the paid cuts?** On the source account the PAID cuts ran
   over 40 seconds, long for cold traffic. The fix is to trim one body beat in
   the paid cut, never the offer.
