# Creator clips: overlays, cut, stitch

Read this when the operator brings REAL footage — a talking-head clip, UGC, a
screen recording — and wants text on it, or wants pieces trimmed and joined.
This is the working-with-what-exists layer; the other formats build from
nothing.

Two tools, both in `scripts/`, both plain commands run from `engine/`:

| Tool | Does |
|---|---|
| `clip.py` | `cut` (frame-accurate trim) and `stitch` (hard-cut concatenation) |
| `overlay.py` | `hook` (static text block), `transcribe` (speech → word timings), `captions` (word-synced captions burned on) |

Run either with no arguments to print its usage. Both print the MEASURED
duration of every file they write.

## Requirements

- **A real ffmpeg.** The slim binary Remotion bundles has almost no filters.
  `brew install ffmpeg` on a Mac — and Homebrew wants the operator's
  password, so they run that one line themselves (the preflight stage in
  CLAUDE.md has the wording).
- **The Python env from `requirements.txt`** for `transcribe` (Whisper) and
  the Pillow text rendering. Same env the other scripts use.
- **macOS** for the text overlays: they use the system SF font, the same
  native-app look the aerial format uses.

## The workflows

### Captions on a creator clip

```bash
python3 scripts/overlay.py transcribe creator.mp4 public/words/creator.json
# READ THE PRINTED TRANSCRIPT before going on. A misheard word gets BURNED
# INTO THE VIDEO. Fix mishears by editing the json by hand.
python3 scripts/overlay.py captions creator.mp4 public/words/creator.json out.mp4
```

Captions group on the same reading rules the Cards format uses: split on
pauses over 0.9s, cap at five words, glue stray punctuation to the word
before it, hold each group until the next one starts so a pause never blanks
the lower third. They sit at 70% of frame height, inside the feed-chrome safe
area (chrome covers roughly the top 14% and bottom 20% of a 9:16 frame).

### A hook line on top

```bash
python3 scripts/overlay.py hook in.mp4 out.mp4 "The hook, as a statement" --until 3.0
```

Upper third, heavy weight, hard black stroke, fade-in. Omit `--until` to hold
it for the whole clip. The hook rules from the other formats apply unchanged:
a declarative line that names the viewer's situation, never a question.

### Cut and stitch

```bash
python3 scripts/clip.py cut long.mp4 bite.mp4 12.5 21.0
python3 scripts/clip.py stitch out.mp4 bite.mp4 reaction.mp4 closer.mp4
```

`cut` re-encodes so the cut lands on the frame you asked for (stream-copy
cutting snaps to keyframes and lands up to two seconds off — that is not a
corner to cut). `stitch` normalises every clip to the first clip's resolution
and frame rate, scaled to fit and padded, never stretched. Hard cuts only, on
purpose: no crossfades, no dissolves. `--mute` stitches video-only, for a
sequence that gets a voiceover or bed at the format stage; without it every
clip must carry audio, and one that does not is an error, not a silent
defect.

## Order of operations

Cut first, then stitch, then captions, then hook. Every re-encode costs a
little quality, so do the text passes last and only once. If the final piece
needs both hook and captions, run captions first and hook on its output —
they occupy different bands and do not collide.

## Rules that carry over from the rest of the kit

- **The operator watches and listens to the finished file.** Burned text
  cannot be turned off by the viewer; a typo here is a re-render, and a
  misheard word that shipped is a retired cut.
- **Rights first.** Only work with footage the operator has the right to
  use. A creator's clip needs the creator's yes, on the record, before it
  goes near an ad account.
- **Both ratios, if it ships as an ad.** A 9:16 master centre-crops to 4:5 at
  `crop=1080:1350:0:285` (the aerial format's rule) — anything near the top
  or bottom of frame gets cut, so check the 4:5 with your own eyes.
- **One variable per test**, same as everywhere else: same clip with two
  different hooks is a test; a different clip AND a different hook is noise.
- **Screen the output at full resolution** before it ships.

## Giving Claude eyes on the footage

Claude cannot play a video, but it can check one, two ways:

**Zero install, always available.** Extract frames and read them as images —
Claude Code reads PNGs natively. This is how every overlay in this kit was
verified before handover:

```bash
ffmpeg -y -v error -ss 3.2 -i out.mp4 -frames:v 1 check.png
```

Pull a frame from inside the hook window, one from a caption group, one near
the end, and look at each. Check the text is inside the safe areas, the
stroke is clean, and nothing placeholder survived. Delete the PNGs after.

**The claude-video-vision plugin, optional.** A third-party Claude Code
plugin that lets Claude watch a video properly — frames at an adaptive rate
plus audio transcription with timestamps. Worth installing when the work is
heavy on creator footage (picking cut points, QC-ing pacing). Inside Claude
Code, one at a time:

```
/plugin marketplace add https://github.com/jordanrendric/claude-video-vision
/plugin install claude-video-vision
```

Then `/setup-video-vision` runs its wizard. Audio understanding works fully
local via Whisper (already in this kit's requirements) or via a Gemini or
OpenAI key — the wizard covers the choice, and the local option means no new
account. It is not part of this kit and nothing here depends on it; the
frame-extraction method above covers verification without it.

## What this deliberately is not

There is no timeline, no transitions library, no color grading, no
multi-track audio. Those are editor jobs, and this kit is not an editor. If
a piece needs them, hand it to a human with an NLE and lose nothing: these
tools cover the eighty percent — trim, join, hook, captions — that a feed ad
actually uses.
