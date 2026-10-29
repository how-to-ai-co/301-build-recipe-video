> ### One correction before you copy anything from here
> The shared paid outro in the original account shipped an offer line that was
> factually wrong on two counts, and it had been spoken in 46 rendered files
> before anyone caught it. The mechanism is the lesson: the outro is generated
> once and appended to every paid ad, so a wrong claim in it ships everywhere
> at once. Verify every factual claim in your offer line against reality before
> you generate the outro. CORRECTED 2026-07-30.

> ## Read this first: two codebases, one convention
>
> This section was written by reading the original production repo, which is
> where all of this actually ran and shipped. Every constant, filter graph and
> failure in it is real and was checked against that source, twice. For this
> starter kit, client names, script copy, offer wording and account identifiers
> have been scrubbed; placeholder copy is marked as such and is deliberately
> not realistic. The numbers, thresholds and failure lessons are untouched.
>
> The `engine/` folder in this bundle is a consolidated rebuild of that
> pipeline. It does the same things with a tidier layout. Where this section
> describes a path or a wiring detail, translate it:
>
> | The original repo | `engine/` in this bundle |
> |---|---|
> | `Theme`/`DARK`/`PAPER` declared inside the paid-ad component | `src/theme.ts`, imported by every component |
> | Timings flat at `public/words_*.json` | `public/words/<number>.json` |
> | `video/timings.py`, `video/prosody.py` | `scripts/timings.py`, `scripts/prosody.py` |
> | `Root.tsx` with ~40 hand-written `<Composition>` blocks and static imports | `Root.tsx` generated from `src/configs.mjs` |
> | Composition id hand-written per ad | derived: `<Format><number>-<OFFER>-<ratio>` |
> | One shell script per wave | one `build.sh` reading `configs.mjs` |
>
> **On the dynamic words import.** The audit pass flagged
> `require(`../public/words/${...}`)` in the generated `Root.tsx` as unrunnable.
> That is correct for the original repo's setup and wrong for this bundle:
> Remotion bundles with webpack, which resolves a template-literal require into
> a context module over the whole directory. It was tested here with two ads and
> rendered four files. Trust the test, not the claim, and if you ever switch
> bundlers, re-test it first.
>
> **On shipped audio.** This kit ships no audio at all: no voiceover files, no
> word-timing JSON, no music. Your bed is composed in your first session by
> `scripts/bed.py` (full source in §6.3), an original composition with zero
> rights encumbrance. Anywhere below that talks about reusing an existing
> voiceover or bed, read it as: reuse one you already made, or generate your
> first one and reuse that.
>
> Everything else below stands as written.

# 50. Voice and music

Everything that makes sound in the ad pipeline: the two voice routes, the one
consolidated generator, the QC chain that catches defects before a human wastes
attention on them, and the music bed.

Read this before you generate a single second of audio. The rules in here were
paid for one broken take at a time.

---

## 0. The one rule that outranks everything else

**No audio ships that a human has not listened to.**

Not "a human approved the transcript". Not "the checks passed". A person puts
headphones on and plays the file end to end.

Two independent pieces of evidence for why, both from the original account's
standing rules and failure log:

1. From the standing rules in the original repo's ads README:

   > **Read the transcript and run `prosody.py` before every render.** Six
   > of eight Chatterbox takes in one session had a defect that would otherwise
   > have shipped: phantom repeated phrases, dropped words, an inserted
   > contraction that reversed a line's meaning, and rising terminals on
   > statements.

2. From the failure log in the original account's video-ads handoff:

   > **NEVER ship audio no human has heard.** Every unheard version failed:
   > mismatched TTS voices, robotic delivery, homemade synth music. Metrics
   > (reverb index, centroid, HF/LF) diagnose but do not clear.

The mechanical checks in section 4 exist to make the human listen *less*, not to
replace them. They filter out the takes that are provably broken so the only
question left for ears is "is this performance believable", which is the one
question no script can answer.

Note the honest state the original tree was in when this was written:
**"Not yet judged by ear." appeared in fourteen caption files**, not three.
The backlog was the first hook wave in both offers plus the entire RSVP wave:
every one of them rendered, filed, caption-written, and not cleared through
this gate. One caption file stated the rule it was waiting on verbatim:
*"Per the standing rule in the ads README, the operator listens before this
ships."* Expect your own tree to accumulate the same backlog; track it.

---

## 1. Two routes, and which one to use

| | Chatterbox (local clone) | ElevenLabs (hosted API) |
|---|---|---|
| Cost | free, MIT, runs on a Mac | metered, key in `video/.env` |
| Voice | cloned from `video/audio/ref_british.mp3` | stock voices, or a clone of your own speaker |
| Determinism | **stochastic**, every roll differs | not measured here: the four eval calls were each run once |
| Your own speaker's voice | not practical from a short clip | possible, **blocked on the free plan** |
| Used by | every shipped voiceover in the original account | evaluation samples only |

Every voiceover in every shipped ad in the original account was Chatterbox.
ElevenLabs was evaluated on 2026-07-27, hit a hard plan wall on all four cloned
voices, and stayed dormant. It stays in the module because the day the plan is
upgraded it becomes a one-word change.

**There is a route zero, and it is cheaper than both.** The original engine doc
ranked the voice options, and the first line was: *"Reuse an existing
voiceover. Free. Always the first choice for a format test."* That is exactly
what the RSVP wave did: no generation at all, each format-test cut played the
same file its counterpart played, so the format was the only variable. This kit
ships no voiceover files, so route zero for you means: reuse a voiceover you
already made, or generate your first one and then reuse it for every format
test after. Before you reach for either engine below, check whether the test
you are running actually needs a new read. A new read is a new variable.

And the gate on either engine, from the same doc: **confirm `.env` is
gitignored, then confirm the key works with one cheap call before generating a
wave.** The original `video/.gitignore` listed `.env` (verified), along with
`node_modules/`, `vo/*.wav` and `out/`. Note the third entry: **the take files
themselves are gitignored**, so "keep every take" is a rule enforced by nothing
but discipline and the local disk.

**Route C, fal, is this engine's default for a generated voice.** One `FAL_KEY`
reaches MiniMax (the narrator voice behind a run of shipped ads), ElevenLabs
library voices (which work through fal even where the free direct plan returns
402), a hosted Chatterbox clone, and Seedance 2.5 takes, whose voices were
judged more natural than the text-to-speech reads. The endpoints, payloads and traps are in
`parts/55-generation-fal.md`. Everything below about timings, prosody and
listening applies to a fal voice exactly as written.

---

## 2. Route A: ElevenLabs

### 2.1 What is in the account

The key lives at `video/.env`, mode 600, gitignored. Use a project-scoped key,
scoped to Text-to-Speech, Music Generation and Voices-read only.

`video/.env` has exactly two lines (values redacted here):

```
ELEVENLABS_API_KEY=<redacted>
REPLICATE_API_TOKEN=<redacted>
```

> A lesson from the original account: a Replicate token from that file was
> pasted into a chat transcript once and had to be rotated. If a credential
> ever appears in a transcript or log, rotate it: delete the token, create a
> new one, and `read -s` it back into `video/.env`. Two different credentials
> sharing one file makes this easy to forget.

### 2.2 Voice IDs actually wired up

The helper carries a VOICES map. The first four below are stock ElevenLabs
voices and work on any plan. The original account also had four pre-existing
clones of its speaker's voice; replace those slots with your own chosen voice
IDs:

```python
VOICES = {
    "roger":   "CwhRBWXzGAHq8TQ4Fs17",
    "laura":   "FGY2WhTYpPnrIDTdsKH5",
    "charlie": "IKne3meq5aSn9XLyUdCD",
    "hope":    "OYTbf65OHHFELVut7v2H",
    "clone_pro":     "<your professional clone voice id>",
    "clone_instant": "<your instant clone voice id>",
}
```

### 2.3 The free-tier 403, verbatim

Verified 2026-07-27 in the original account. Two failures were still sitting in
that repo as 227- and 259-byte "mp3" files.

> **Correction to an earlier draft of this section.** It said the helper writes
> the error body to the output file. It does not. The original `tts.py` catches
> `HTTPError`, prints the first 220 characters and `return False` *before* the
> `write_bytes` call. So the two JSON files on disk were written by an older
> revision of the helper, or by hand, and no code in the tree today produces
> them. The size tell below is still worth knowing because such artifacts can
> exist and will mislead you.

Their contents (request ids elided):

`el_clone_pro.mp3`:

```json
{"detail":{"type":"authorization_error","code":"subscription_required","message":"Professional voices require a Creator tier subscription or above.","status":"only_for_creator+"}}
```

`el_clone_instant.mp3`:

```json
{"detail":{"type":"authorization_error","code":"subscription_required","message":"Instantly cloned voices are not available on your current plan. Please upgrade your subscription.","status":"ivc_not_permitted"}}
```

Two different refusals, two different codes: professional clones need
`only_for_creator+`, instant clones are `ivc_not_permitted`. The Music API is
also blocked on the free tier ("not available for free users").

**What upgrading buys.** Creator is roughly $22/mo. It unlocks your own
speaker's cloned voice, which is the single biggest quality jump available in
this pipeline. If your account cannot show a face on camera, it can still
carry a real voice. Once upgraded it is one identifier change in the SCRIPTS
table.

**The size tell.** If an ElevenLabs output is under ~1 KB it is a JSON error
body, not audio. For scale, the four eval takes that *did* work were 129-170 KB
(the turbo take 128,775 bytes / 7.99 s; the v3 take 170,153 bytes / 10.56 s).
The consolidated module in section 3.3 checks the HTTP status and refuses to
write on failure, same as the originals.

**Free-tier ceiling.** The free tier came with **10,000 credits**. That is the
budget the four eval calls came out of.

### 2.4 Settings that were actually used

The evaluation was four calls, and the per-voice tuning is real, not
decorative:

| Output | Voice | Model | stability | style | similarity_boost | Text |
|---|---|---|---|---|---|---|
| `v3_roger` | roger | `eleven_v3` | 0.3 | 0.7 | 0.75 | TAGGED |
| `v3_laura` | laura | `eleven_v3` | 0.3 | 0.8 | 0.75 | TAGGED |
| `v3_charlie` | charlie | `eleven_v3` | 0.25 | 0.75 | 0.75 | TAGGED |
| `turbo_roger` | roger | `eleven_turbo_v2_5` | 0.3 | 0.75 | 0.75 | PLAIN |

`use_speaker_boost` is `True` on every call. Output format is
`mp3_44100_128`, set as a query parameter on the URL, not in the body.

The two evaluation texts, with placeholder copy (write your own; keep the
structure):

```
PLAIN   You have the app open. That was the easy part. Your product's hook
        line goes here, and your qualifier goes here. It's free to try.

TAGGED  [excited] You have the app open. That was the easy part. Your
        product's hook line goes here... [serious] and your qualifier goes
        here. [confident] It's free to try.
```

The `[excited]` / `[serious]` / `[confident]` inline tags are an `eleven_v3`
feature. **What the original source actually shows** is only the pairing:
TAGGED text went to `eleven_v3` and PLAIN text went to `eleven_turbo_v2_5`.
There is no comment in the repo saying what happens if you cross them. Treat
"turbo will read the brackets aloud" as the working assumption behind the
pairing, not as something anyone measured.

A second script in the same tagged style existed in the original tree and also
targeted `eleven_v3`, which is consistent with the pairing.

---

## 3. Route B: Chatterbox local cloning

### 3.1 The reference clip

Everything in the original account was cloned from one file.

| | |
|---|---|
| Path | `video/audio/ref_british.mp3` |
| Duration | 4.226 s |
| Format | MP3, 44.1 kHz, mono, ~65 kbps |
| Size | 34,290 bytes |

**Every script in the original repo pointed at this same file.** All nine
`vo_*.py` scripts hardcoded `REF = ROOT / "audio" / "ref_british.mp3"`. That is
deliberate and it is load-bearing for the tests: the ads README required that a
format-test cut and the ad it tests against share *the same audio file*, not a
re-recording, so that format is the only variable. Sharing a reference clip is
the weaker version of the same principle applied across the whole account: one
voice, so persona and hook results are comparable.

The clip is 4.2 seconds. That is short for a voice reference and it is part of
why the takes vary as much as they do. **The provenance of the original clip
was not recorded anywhere in that repo.** See open questions: record where your
reference clip came from and whether the speaker consented, before you clone
anything from it.

Chatterbox writes **24 kHz mono float32 WAV**. Verified with ffprobe on three
takes (`pcm_f32le,24000,1`).

### 3.2 Running it

Chatterbox is a normal pip package; on the original machine it resolved to
`site-packages/chatterbox/`. The device line is identical in every original
script and is carried into the consolidated module:

```python
dev = "mps" if torch.backends.mps.is_available() else "cpu"
m = ChatterboxTTS.from_pretrained(device=dev)
```

**Loading the model costs roughly a minute.** One of the original scripts
existed as a single file for exactly that reason ("Loading ChatterboxTTS costs
roughly a minute, so generating these separately wastes four of them"). The
consolidated module loads once per invocation regardless of how many jobs you
ask for, which generalises that saving to every job.

### 3.3 The consolidated module

This replaces the original account's nine `vo_*.py` scripts, `tts.py` **and
`make_ad.py`**. Complete and runnable. Save as `video/voice.py`.

(`make_ad.py` was the third ElevenLabs caller in that tree and was missed by
the first pass of this section. It duplicated `tts.py`'s VOICES map and POST
helper, and it was the *only* record anywhere of how the ElevenLabs **Music
API** was called. That call is carried below as `eleven_music()` so the recipe
is not lost when the plan is upgraded. See merge note 8.)

The SCRIPTS table below ships with generic placeholder entries. The original
production table held about twenty entries: four persona bodies, three hook
variants, four sub-persona cuts, a shared paid outro, two superseded
format-test rolls, and the ElevenLabs evaluation set. The schema and the
measured tuning are what transfer; the text fields are placeholder copy on
purpose. Put your own scripts in.

```python
#!/usr/bin/env python3
"""One voice module for the whole ad account. Two engines, one SCRIPTS table.

    python3 voice.py list                       # every job, engine, tuning
    python3 voice.py why body                   # why this job is tuned this way
    python3 voice.py gen hook_v2                # 3 takes -> vo/hook_t{n}.wav
    python3 voice.py gen body body_low --takes 5
    python3 voice.py gen body body_low outro    # ONE model load for all three
    python3 voice.py publish hook_v2 --take 1   # copy the pick into public/audio/
    python3 voice.py gen v3_eval                # ElevenLabs route
    python3 voice.py music vo/ad_music.mp3      # ElevenLabs Music (BLOCKED on
                                                # the free plan; recipe kept)

ROUTE ZERO, ALWAYS CHECK IT FIRST: reuse a voiceover you already made. In the
original account the format-test wave generated nothing at all: each cut played
the same file as the ad it tested against, which is what made the format the
only variable. A new read is a new variable.

ENGINES
  chatterbox  local clone of audio/ref_british.mp3. Free, MIT, no API key,
              STOCHASTIC. Every shipped voiceover in the original account.
  elevenlabs  hosted TTS, key read from video/.env, never printed. Cloned
              voices return 403 on the free plan; stock voices work.

BEFORE EITHER ENGINE: confirm .env is gitignored, then confirm the key works
with ONE cheap call before generating a whole wave.

TAKES ARE NUMBERED, NEVER OVERWRITTEN. Chatterbox is stochastic and its
failures are uncorrelated between rolls: a take that fixes uptalk on one line
can introduce a phantom repeated phrase on another. Overwriting once cost a
good take that had already passed every check. Every roll lands as
vo/<stem>_t<n>.wav and is kept until a human has picked one BY EAR.

Before you generate a hook variant at all:
    python3 check_script.py <id>      # the body must not have drifted

After generating, vet EVERY take before it goes near a render:
    python3 timings.py vo/hook_t1.wav tmp/w.json   # READ the transcript
    python3 prosody.py vo/hook_t1.wav tmp/w.json   # 0 uptalk problems

And then listen to it. The checks filter; they do not clear.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).parent
VO = ROOT / "vo"
PUB = ROOT / "public" / "audio"
REF = ROOT / "audio" / "ref_british.mp3"

# ---------------------------------------------------------------- ElevenLabs --

# Cloned voices are 403 on the free plan. Verified 2026-07-27:
#   professional clone -> {"code":"subscription_required",
#                          "status":"only_for_creator+",
#                          "message":"Professional voices require a Creator tier
#                                     subscription or above."}
#   instant clone      -> {"code":"subscription_required",
#                          "status":"ivc_not_permitted",
#                          "message":"Instantly cloned voices are not available
#                                     on your current plan."}
# The Music API is blocked on the same plan. Creator is ~$22/mo and unlocks
# your own speaker's cloned voice, which is the biggest single quality jump
# available here, and the only way to put a real person in an ad when you
# cannot show a face on camera.
VOICES = {
    "roger":   "CwhRBWXzGAHq8TQ4Fs17",
    "laura":   "FGY2WhTYpPnrIDTdsKH5",
    "charlie": "IKne3meq5aSn9XLyUdCD",
    "hope":    "OYTbf65OHHFELVut7v2H",
    "clone_pro":     "<your professional clone voice id>",
    "clone_instant": "<your instant clone voice id>",
}


def _eleven_key() -> str:
    """Read the key from video/.env. Never print it, never log it."""
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            k = line.split("=", 1)[1].strip()
            if k:
                return k
    sys.exit("no ELEVENLABS_API_KEY in video/.env")


def eleven_say(voice: str, text: str, out: pathlib.Path, model: str = "eleven_v3",
               stability: float = 0.3, style: float = 0.7, sim: float = 0.75) -> bool:
    """One ElevenLabs TTS call. Returns True on success.

    An earlier helper wrote the response body to disk unconditionally, so a
    403 landed as a 227-byte "mp3" containing JSON. This version writes nothing
    unless the call succeeded.
    """
    vid = VOICES.get(voice, voice)
    body = json.dumps({
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": sim,
            "style": style,
            "use_speaker_boost": True,
        },
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": _eleven_key(), "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        print(f"{out.name}: FAIL {e.code} {e.read().decode()[:220]}")
        return False
    out.write_bytes(data)
    print(f"{out.name}: ok ({len(data)//1024} KB)  voice={voice} model={model} "
          f"stab={stability} style={style} sim={sim}")
    return True


# The ElevenLabs Music API call, carried over verbatim from the original
# make_ad.py. It is BLOCKED on the free plan ("not available for free users"),
# so it never produced a file there. It is kept because it was the only record
# in that tree of how music was going to be generated, and because every
# alternative today is either bed.py or an uncleared supplied track. Note the
# prompt: no vocals and no melody that competes with speech, even energy
# throughout. That is the same brief bed.py satisfies by being a sustained
# drone with no percussion and no melody.
MUSIC_PROMPT = ("Minimal modern tech underscore for a short social ad. "
                "Warm analog synth pulse, soft muted kick, light percussive ticks, "
                "confident and forward-moving but restrained. No vocals, no melody "
                "that competes with speech. Even energy throughout.")
MUSIC_MS = 24000


def eleven_music(out: pathlib.Path, prompt: str = MUSIC_PROMPT,
                 length_ms: int = MUSIC_MS) -> bool:
    """One ElevenLabs Music call. Returns True on success. 403 on the free plan."""
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/music",
        data=json.dumps({"prompt": prompt, "music_length_ms": length_ms}).encode(),
        headers={"xi-api-key": _eleven_key(), "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        print(f"{out.name}: FAIL {e.code} {e.read().decode()[:220]}")
        return False
    out.write_bytes(data)
    print(f"{out.name}: ok ({len(data)//1024} KB)  {length_ms}ms")
    return True


# ---------------------------------------------------------------- Chatterbox --

_MODEL = None


def _chatterbox():
    """Load once per process. from_pretrained costs about a minute."""
    global _MODEL
    if _MODEL is None:
        import torch
        from chatterbox.tts import ChatterboxTTS
        dev = "mps" if torch.backends.mps.is_available() else "cpu"
        t = time.time()
        _MODEL = ChatterboxTTS.from_pretrained(device=dev)
        print(f"chatterbox loaded on {dev} ({time.time()-t:.0f}s)", flush=True)
    return _MODEL


# -------------------------------------------------------------------- SCRIPTS --

# engine       "chatterbox" | "elevenlabs"
# stem         take files land as vo/<stem>_t<n>.wav
# publish      filename under public/audio/ that the Remotion configs read, or
#              None when the build scripts point at vo/<stem>_t<n>.wav directly
# exaggeration Chatterbox pitch/emphasis range. LOWER IS FLATTER and less prone
#              to rising terminals. Per job, never global — see `why`.
# cfg_weight   Chatterbox guidance. LOWER IS SLOWER and more deliberate.
# takes        default number of rolls for `gen`
# why          the reason this job is tuned the way it is. Load-bearing.
#
# EVERY text FIELD BELOW IS PLACEHOLDER COPY. Replace with your own scripts.
# The tuning values are real and measured; see section 3.4.
SCRIPTS = {

    "body": {
        "engine": "chatterbox", "stem": "body", "publish": "vo.wav",
        "exaggeration": 0.5, "cfg_weight": 0.25, "takes": 1,
        "why": (
            "The original-wave default setting. Ellipses and short sentences "
            "force Chatterbox to breathe; cfg_weight 0.25 slows delivery. This "
            "is the setting the later fixes are measured against: expect "
            "audible uptalk on statement endings at 0.50. Spell numbers out "
            "in the text, and keep sentences short."
        ),
        "text": (
            "Your opening statement, as a statement... not a question. "
            "A short second sentence. "
            "A line with a beat in the middle... and its landing. "
            "Your product's hook line. "
            "A concrete, true example of the outcome. "
            "Five minutes a week... what it covers, and what it skips. "
            "Your brand name. One plain, verified fact about it. "
            "One hundred percent free... forever."
        ),
    },

    "body_low": {
        "engine": "chatterbox", "stem": "body_low", "publish": "vo_low.wav",
        "exaggeration": 0.32, "cfg_weight": 0.40, "takes": 1,
        "why": (
            "The uptalk-fixed setting. At 0.50/0.25 two statement endings in "
            "one original take rose +20.9 Hz and +35.1 Hz, which makes a "
            "statement sound like a question. 0.32 removes the dramatic pitch "
            "swing; cfg_weight 0.40 keeps it deliberate without the drift that "
            "comes from very low guidance. Verify with prosody.py after. "
            "\n"
            "TWO PROSODY FIXES TO CARRY INTO YOUR OWN SCRIPTS. "
            "(1) Chatterbox can insert a contraction that reverses a line's "
            "meaning when a pronoun sits directly before 'already'. Rephrase "
            "so the contraction has nothing to attach to. "
            "(2) An ellipsis between two sentences makes Chatterbox treat the "
            "pair as one continuing utterance, so the terminal fall never "
            "lands. Hard stops between sentences instead. "
            "\n"
            "KEEP THE FREE AND PAID CTAS SEPARATE. In the original account, "
            "the paid versions of every body came as a SEPARATE pass (the "
            "shared outro) so the offer was a clean variable. Do not "
            "'helpfully' add the paid offer to a free body."
        ),
        "text": (
            "Your opening statement. Hard stop. "
            "A second short statement. "
            "The pain your reader recognises, stated flatly. "
            "The reframe your ad exists to deliver. "
            "Your product's hook line. "
            "Your brand name. One plain, verified fact about it. "
            "One hundred percent free. Forever."
        ),
    },

    "hook_v2": {
        "engine": "chatterbox", "stem": "hook", "publish": "vo_v2.wav",
        "exaggeration": 0.40, "cfg_weight": 0.25, "takes": 3,
        "why": (
            "A hook variant: ONLY THE HOOK CHANGES against the body it tests. "
            "Every following sentence must be byte-identical to the live "
            "body's script, so the hook is the single variable under test. "
            "Run check_script.py BEFORE generating: it diffs this against the "
            "body's word timings and fails below 0.94 similarity. "
            "\n"
            "The standing creative rule in the original account: NEVER OPEN ON "
            "A QUESTION. A question reads as low authority; an assumed pain "
            "makes the reader feel called out. Rewrite 'are you X?' as "
            "'you're X, and you already know...'. "
            "\n"
            "exaggeration 0.40, lower than the 0.50 the first wave used. "
            "Measured across the format-test rolls: 0.50 put audible uptalk "
            "on statement endings, 0.35 slowed the read to 155 wpm and "
            "started dropping words. 0.40 was the only setting that produced "
            "a take with every sentence falling. "
            "\n"
            "In the original account the shipped take was the pick of 3: "
            "transcript word for word, prosody.py 0 uptalk, terminal falls of "
            "-11.9, -10.3 and -8.4 Hz. The rejected takes: one rushed at 210 "
            "wpm and ran two sentences together, one had uptalk on two "
            "endings. Expect the same spread."
        ),
        "text": (
            "Your rewritten hook, as a statement. "
            "A short second sentence. "
            "The rest of the body, byte-identical to the body entry. "
            "Your brand name. One plain, verified fact about it. "
            "One hundred percent free... forever."
        ),
    },

    "outro": {
        "engine": "chatterbox", "stem": "outro", "publish": None,
        "exaggeration": 0.32, "cfg_weight": 0.32, "takes": 1,
        "why": (
            "GENERATED ONCE, APPENDED TO EVERY PAID AD. build_paid.py and "
            "build_rsvp_paid.py both read the same vo/ file verbatim, so the "
            "offer is stated identically everywhere. Change the offer by "
            "editing this entry, regenerating, re-running both builds and "
            "re-rendering. NEVER write a separate closing line per persona and "
            "never edit a single ad. That is why publish is None: the build "
            "scripts read the vo/ file directly. "
            "\n"
            "!! CHECK THAT THE RE-RUN ACTUALLY REACHES EVERY COMPOSITION. In "
            "the original account, the paid configs for one wave read audio "
            "filenames that NO SCRIPT WROTE (a retired numbering scheme), and "
            "byte-identical stale copies on disk masked it. Regenerating the "
            "outro would have silently left those compositions rendering the "
            "OLD offer. Grep your configs for every audio filename and confirm "
            "a builder writes each one. See section 5. "
            "\n"
            "Watch your banned words. The original account banned one common "
            "product word outright because the founder's public content "
            "attacked competitors on exactly that word; a near-synonym sat "
            "close enough to invite the same comparison. Keep your own list "
            "and check the outro against it. "
            "\n"
            "NO PRICE WAS STATED in the original outro, and the funnel was "
            "unchanged: subscribe free, then the platform's paywall presents "
            "the paid tier. The ad does not sell, it qualifies. "
            "\n"
            "Keep it tight. It is appended to every paid ad, so every second "
            "here costs a second per ad. An early draft ran 16.5s and put "
            "every ad past 43s. "
            "\n"
            "The opening line should do the differentiating plainly. A soft "
            "line that implies a speed difference between free and paid "
            "fudges the actual line, which is free versus paid. Stating 'the "
            "free thing stays free, full stop' first pre-empts the objection "
            "that kills paid-tier ads: that the free thing is a trojan horse. "
            "Then a flat admission of what is paid, not a soft-pedal. "
            "\n"
            "Prosody carries the body_low fixes: low exaggeration and hard "
            "stops between sentences rather than ellipses, which is what "
            "caused the +35 Hz uptalk in the first fixed-body take. "
            "SEE OPEN QUESTION 1: the original outro script's docstring "
            "claimed cfg_weight 0.40, the code passed 0.32. 0.32 is what "
            "produced the shipped file, so 0.32 is what is carried here."
        ),
        "text": (
            "Your free product stays free. Say so plainly. "
            "Name what the paid tier is. "
            "List its real inclusions here, each one verified. "
            "Start free. Upgrade when you're ready."
        ),
    },

    # ======================= ElevenLabs evaluation samples ====================
    #
    # The bake-off recipe. Kept so the settings are not re-derived. The
    # [excited]/[serious]/[confident] tags are an eleven_v3 feature; the
    # working assumption is that a turbo model SPEAKS THE BRACKETS, which is
    # why the turbo entry uses plain text.

    "v3_eval": {
        "engine": "elevenlabs", "voice": "roger", "model": "eleven_v3",
        "stability": 0.3, "style": 0.7, "sim": 0.75, "out": "v3_eval",
        "why": "eleven_v3 with inline emotion tags, stock male voice.",
        "text": ("[excited] You have the app open. That was the easy part. "
                 "Your product's hook line goes here... "
                 "[serious] and your qualifier goes here. "
                 "[confident] It's free to try."),
    },
    "turbo_eval": {
        "engine": "elevenlabs", "voice": "roger", "model": "eleven_turbo_v2_5",
        "stability": 0.3, "style": 0.75, "sim": 0.75, "out": "turbo_eval",
        "why": "Turbo model, PLAIN text. Turbo does not read the emotion tags.",
        "text": ("You have the app open. That was the easy part. Your "
                 "product's hook line goes here, and your qualifier goes "
                 "here. It's free to try."),
    },

    # A legacy entry pattern worth knowing: the original tree kept the VO
    # script of its very first prototype ad in the table purely so that
    # prototype's build stayed reproducible. If you keep a legacy build
    # around, keep its script here too, and check any product names in it
    # are current before re-shipping.
}


# ----------------------------------------------------------------- commands --

def next_index(stem: str) -> int:
    """First unused take number.

    len(existing) + 1, carried unchanged from the original. It assumes NO TAKE
    IS EVER DELETED, which is the standing rule anyway. The guard in gen()
    means a collision refuses rather than overwrites.
    """
    return len(sorted(VO.glob(f"{stem}_t*.wav"))) + 1


def cmd_list(_args) -> int:
    print(f"{'id':18}{'engine':12}{'stem/out':22}{'exag':>6}{'cfg':>6}  publish")
    for k, s in SCRIPTS.items():
        if s["engine"] == "chatterbox":
            print(f"{k:18}{s['engine']:12}{s['stem']:22}"
                  f"{s['exaggeration']:6.2f}{s['cfg_weight']:6.2f}  {s['publish'] or '-'}")
        else:
            print(f"{k:18}{s['engine']:12}{s['out']:22}{'':6}{'':6}  -")
    return 0


def cmd_why(args) -> int:
    for k in args.ids:
        s = SCRIPTS[k]
        print(f"\n=== {k} ===")
        for para in s["why"].split("\n"):
            print("  " + para.strip())
        print(f"\n  words: {len(s['text'].split())}")
    return 0


def cmd_gen(args) -> int:
    VO.mkdir(exist_ok=True)
    for k in args.ids:
        if k not in SCRIPTS:
            sys.exit(f"unknown id {k!r}; run `voice.py list`")
        s = SCRIPTS[k]

        if s["engine"] == "elevenlabs":
            eleven_say(s["voice"], s["text"], VO / f"{s['out']}.mp3",
                       model=s["model"], stability=s["stability"],
                       style=s["style"], sim=s["sim"])
            continue

        import torchaudio as ta
        m = _chatterbox()
        n_takes = args.takes or s["takes"]
        start = next_index(s["stem"])
        for i in range(start, start + n_takes):
            out = VO / f"{s['stem']}_t{i}.wav"
            if out.exists():                      # never overwrite a vetted take
                sys.exit(f"{out} already exists — refusing to overwrite")
            t = time.time()
            wav = m.generate(s["text"], audio_prompt_path=str(REF),
                             exaggeration=s["exaggeration"],
                             cfg_weight=s["cfg_weight"])
            ta.save(str(out), wav, m.sr)
            d = wav.shape[-1] / m.sr
            w = len(s["text"].split())
            print(f"{out.name}: {d:.1f}s  {w} words  {w/d*60:.0f} wpm  "
                  f"exag={s['exaggeration']} cfg={s['cfg_weight']}  "
                  f"({time.time()-t:.0f}s)", flush=True)
        print(f"  -> now vet each take:\n"
              f"     python3 timings.py vo/{s['stem']}_t{start}.wav tmp/w.json\n"
              f"     python3 prosody.py vo/{s['stem']}_t{start}.wav tmp/w.json\n"
              f"     then LISTEN to it.", flush=True)
    return 0


def cmd_music(args) -> int:
    """ElevenLabs Music. Blocked on the free plan; kept so the recipe exists."""
    VO.mkdir(exist_ok=True)
    return 0 if eleven_music(pathlib.Path(args.out), length_ms=args.ms) else 1


def cmd_publish(args) -> int:
    """Copy a chosen take to the filename the Remotion configs read.

    In the original tree this step was a manual `cp` that no script performed.
    Verified by checksum: every published file was byte-identical to a take in
    vo/. Making it a command is the only behaviour this module adds that the
    originals did not have.
    """
    s = SCRIPTS[args.id]
    if s["engine"] != "chatterbox":
        sys.exit("publish is for chatterbox takes only")
    if not s["publish"]:
        sys.exit(f"{args.id} has publish=None — the build scripts read "
                 f"vo/{s['stem']}_t<n>.wav directly, nothing to copy")
    src = VO / f"{s['stem']}_t{args.take}.wav"
    if not src.exists():
        sys.exit(f"no such take: {src}")
    PUB.mkdir(parents=True, exist_ok=True)
    dst = PUB / s["publish"]
    shutil.copyfile(src, dst)
    print(f"{src} -> {dst}")
    print("  now re-run timings.py against the PUBLISHED file and update voEnd "
          "in the matching config, or the end card will cut into the read.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list").set_defaults(fn=cmd_list)

    w = sub.add_parser("why")
    w.add_argument("ids", nargs="+")
    w.set_defaults(fn=cmd_why)

    g = sub.add_parser("gen")
    g.add_argument("ids", nargs="+")
    g.add_argument("--takes", type=int, default=None,
                   help="override the per-job default take count")
    g.set_defaults(fn=cmd_gen)

    b = sub.add_parser("publish")
    b.add_argument("id")
    b.add_argument("--take", type=int, required=True)
    b.set_defaults(fn=cmd_publish)

    mu = sub.add_parser("music")
    mu.add_argument("out")
    mu.add_argument("--ms", type=int, default=MUSIC_MS)
    mu.set_defaults(fn=cmd_music)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
```

### 3.4 The tuning table, and why each number is what it is

Every value below came out of a measured failure in the original account. None
of them are defaults someone liked the sound of. The job labels are
genericized; the numbers are not.

| Job family | exag | cfg | Why this setting |
|---|---|---|---|
| First-wave bodies | 0.50 | 0.25 | The original wave. Ellipses and short sentences force Chatterbox to breathe; low `cfg_weight` slows delivery. This is the setting the later work is measured *against*. |
| The uptalk-fixed body | 0.32 | 0.40 | 0.50 threw the terminals upward: one sentence-final word rose **+20.9 Hz**, another **+35.1 Hz**. 0.32 removes the pitch swing; cfg 0.25 → 0.40 keeps it deliberate without low-guidance drift. |
| Hook variants | 0.40 | 0.25 | Measured across the format-test rolls: **0.50 put audible uptalk on statement endings; 0.35 slowed the read to 155 wpm and started dropping words. 0.40 was the only setting that produced a take with every sentence falling.** |
| Sub-persona cuts | 0.32 | 0.36 | Carries every earlier fix. 0.50/0.25 produced measurable uptalk (+35 Hz); **0.40 once produced a 213 wpm read against 187 in the bodies**, so these sit lower still. |
| The shared outro | 0.32 | 0.32 | Same low-exaggeration treatment as the fixed body, hard stops between sentences. See open question 1 about the 0.32-vs-0.40 contradiction in the original. |
| First format-test roll | 0.40 | 0.25 | **0.50 put audible uptalk on the pain-callout line, the one line in the ad that must not sound uncertain.** This is the roll that produced the 0.40 the whole hook wave inherited. |
| Second format-test roll | 0.50 | 0.25 | Left at the default; only the first roll had a measured failure, so only that one moved. |

**The general law:** lower `exaggeration` = flatter = less prone to rising
terminals. Lower `cfg_weight` = slower and more deliberate, but too low and the
read drifts.

### 3.5 Punctuation is a prosody control, not typography

This is the most transferable lesson in the whole voice layer.

- **An ellipsis between two sentences makes Chatterbox treat them as one
  continuing utterance, so the terminal never lands.** That is what caused the
  +35.1 Hz uptalk on a sentence-final word in one original take. The
  documented fix is a **hard stop**.
- **An ellipsis inside a sentence, for a beat, is fine.** That is what they are
  for.
- Ellipses are **pacing marks for the model, not punctuation the viewer sees.**
  The RSVP display reads from Whisper timings, so the beat an ellipsis creates
  in the audio is what spaces the words on screen.
- **Spell numbers out.** "Fifty thousand", not "50,000". "One hundred
  percent", not "100%". Whisper splits `50,000` into `50` + `,000` and `100%`
  into `100` + `%`; the compositions glue them back, but spelling them out
  keeps the transcript clean at the source.
- **Watch for contractions the model inserts.** One original line came back
  with an inserted contraction that reversed its meaning ("you already paid
  for X" became "you're already paid", which reads as *you have been
  compensated*). The fix was removing the pronoun directly before "already" so
  the contraction had nothing to attach to.
- **Short soft words after a sentence break get eaten.** "Want to go faster?"
  came back as "want to wear faster" (whisper-small) and "120 faster"
  (whisper-medium). "move" carries more weight than "go", and an ellipsis buys
  room.
- **When two Whisper models disagree, the audio is bad, not the
  transcription.** An industry term abbreviated in one script gave two
  different mishearings from two models; the spelled-out full term survived.
  Spell out abbreviations.
- **A closing line whose brand name echoes words from the sentence before it
  can produce a phantom repeat.** In the original account, one such pairing
  produced a phantom repeated phrase in four separate takes. Expect it. Check
  the transcript every time.

### 3.6 What I merged, and the behaviour differences I had to reconcile

Nine `vo_*.py` scripts plus `tts.py` **plus `make_ad.py`**, eleven files in
all, collapse into one `voice.py`. What that cost:

**1. Take numbering is now universal.** `vo_hooks.py` numbered its takes and
never overwrote them; the other eight wrote a single fixed filename and
clobbered it. The numbered behaviour wins, on `vo_hooks.py`'s own evidence:

> Chatterbox is stochastic and its failures are uncorrelated between rolls: a
> take that fixes uptalk on one line can introduce a phantom repeated phrase on
> another. Overwriting cost a good take that had already passed every check.

*Behaviour change you must know about:* the old scripts dropped their output
straight into place under a fixed name. `voice.py gen <id>` now writes
`vo/<stem>_t1.wav`. If your build scripts name fixed paths, either run
`voice.py publish`, or copy the take to the legacy name yourself. Section 5
has the pattern.

**2. `exaggeration` and `cfg_weight` are per-entry with no default.** One
original script had `EXAGGERATION.get(k, 0.5)`, a silent fallback to the
setting that was *measured to produce uptalk*. There is no fallback here. A
missing value raises `KeyError`, which is the correct failure.

**3. One model load per invocation, for every job.** The sub-persona script
already did this for its four scripts, explicitly, because loading costs about
a minute. Now every job gets it.

**4. ElevenLabs failures no longer write files.** The original `say()` only
wrote on success but printed the error to stdout, and yet two JSON error
bodies were sitting in `vo/` as `.mp3`. Reading the original: `say()` returns
`False` before writing on `HTTPError`, so those two files predate that guard
or were written by an earlier version. Either way, `eleven_say()` here writes
nothing on failure and says so. **This is a deliberate divergence from the
artifacts on disk, not from the code.**

**5. Two scripts existed in near-duplicate pairs with real textual
differences. I kept both and did not merge them.**

| Pair | Difference | Why it matters |
|---|---|---|
| A hook script vs its format-test twin | a comma before the same clause in one, a hard stop in the other | comma vs hard stop, which is exactly the prosody control in 3.5 |
| A body script vs its format-test twin | a hard stop before the closing run in one, an ellipsis in the other | hard stop vs ellipsis, same control |

They are not the same script. Collapsing them would have silently changed a
delivery that was tuned on purpose. Both lived in the table; a `_superseded`
suffix recorded that the format-test wave shipped the reused takes instead.

**6. The format-test script was misnamed internally.** Its usage line named
the format's old working title and it wrote stems under that old name. The
format was renamed (the ads README was emphatic that the distinction between
the old name and RSVP is load-bearing), the file was renamed, but the
docstring and output stem were not. Carried with the old stem so existing
files still resolved. Lesson: when you rename a format, grep for the old name
in docstrings and output stems too.

**7. One persona script wrote a `_v2` stem, and a plain-stem file existed on
disk with no script in the repo that generates it.** See open questions.

**8. `make_ad.py` was a third ElevenLabs caller and is now folded in.** It
duplicated `tts.py`'s VOICES map (six of the eight entries) and its own POST
helper with the same write-only-on-success behaviour. Two things in it were
nearly lost:

| From `make_ad.py` | Where it went |
|---|---|
| The prototype ad's VO script (tagged, with a since-renamed product name in it) | noted in SCRIPTS. The prototype `build.sh` read that VO file, so without the script that build is not reproducible. |
| `POST /v1/music` with `music_length_ms: 24000` and the full underscore prompt | `eleven_music()` + `MUSIC_PROMPT`. The only record in the tree of the music call. |

*Behaviour differences reconciled:* `make_ad.py` passed a full filename where
`tts.py` passed a stem and appended `.mp3`; the merged `eleven_say()` takes a
`pathlib.Path`, and the `out` field in SCRIPTS is a stem, following `tts.py`.
`make_ad.py` used a 180 s timeout against `tts.py`'s 120 s; `eleven_say()`
keeps 120 s and `eleven_music()` keeps 180 s, because music generation is the
slower call. `make_ad.py` truncated error bodies at 200 characters, `tts.py`
at 220; 220 is kept.

**9. CLI shape changed, deliberately.** `vo_hooks.py` took a bare positional
take count and defaulted to one specific job with no arguments; two other
scripts defaulted to generating *everything*. `voice.py` requires explicit ids
and moves the count to `--takes`. A script that generates a whole wave when
you forget to type an argument is not a feature when each roll costs a minute
of model time and the takes are gitignored.

---

## 4. The QC chain

Four gates, in this order. Skipping any of them has already cost real work.

```
        check_script.py          BEFORE you generate anything (hook variants only)
              ↓
        voice.py gen             numbered takes, never overwritten
              ↓
        timings.py               word timings + READ THE PRINTED TRANSCRIPT
              ↓
        prosody.py               0 uptalk problems, no long gaps, no stretched words
              ↓
        a human listens          non-negotiable, outranks all of the above
```

### 4.1 `check_script.py`: did anything except the hook move?

Run this **before generating takes**, not after.

The whole value of a hook variant is that one thing moved. If any other
sentence drifts, the pair stops being a test and becomes two different ads that
happen to share a number. **Nothing in the render pipeline will catch it,
because both files look fine.**

**The incident this exists because of:** the first draft of one hook variant
scored **0.573** against its body. Three sentences of the body had been
dropped and a line invented. Three takes were generated and vetted for prosody
before anyone compared the words. All of that work was thrown away.

Threshold: a hook rewrite should score **above ~0.94**. The only opcodes should
be the hook itself and any clause that exists solely to serve the old hook. A
clause like "if the answer is no" cannot survive when the question it answered
does not.

It parses `SCRIPTS` out of the generator with `ast.literal_eval` rather than
importing it, so it never loads torch. **If you adopt `voice.py`, point
`scripts()` at `voice.py` and pull `["text"]` out of each entry.** The values
are now dicts, not bare strings. That is the one edit consolidation forces.

Complete source (adjust `V1_WORDS` and the `norm()` number replacements to
your own scripts):

```python
#!/usr/bin/env python3
"""Diff a hook-variant script against the body it is supposed to preserve.

    python3 check_script.py          # all of them
    python3 check_script.py <id>

The whole value of a hook variant is that ONE thing moved. If any other
sentence drifts, the pair stops being a test and becomes two different ads that
happen to share a number, and nothing in the render pipeline will catch it,
because both files look fine.

This is not hypothetical. The first draft of one variant scored 0.573 against
its body: three sentences had been dropped and a line invented. Three takes
were generated and vetted for prosody before anyone compared the words.

Run this BEFORE generating takes. A hook rewrite should score above ~0.94; the
only opcodes should be the hook itself and any clause that exists solely to
serve the old hook.
"""
import ast, json, re, sys, difflib, pathlib

ROOT = pathlib.Path(__file__).parent
V1_WORDS = {"401": "public/words.json",
            "402": "public/words_2.json",
            "404": "public/words_4.json"}


def norm(s: str) -> list:
    s = re.sub(r"\s+", " ", s.lower())
    # Match these replacements to the numbers your own scripts spell out.
    # Whisper tokenises "50,000" as "50 ,000" and "100%" as "100 %".
    s = s.replace("50 ,000", "fifty thousand").replace("50,000", "fifty thousand")
    s = s.replace("100 %", "one hundred percent").replace("100%", "one hundred percent")
    return re.sub(r"[^a-z0-9' ]", "", s).strip().split()


def scripts() -> dict:
    tree = ast.parse((ROOT / "voice.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SCRIPTS":
            return {k: v["text"] for k, v in ast.literal_eval(node.value).items()}
    sys.exit("no SCRIPTS in voice.py")


def main(want) -> int:
    S = scripts()
    bad = 0
    for num in want:
        a = norm(" ".join(x["w"] for x in json.load(open(ROOT / V1_WORDS[num]))))
        b = norm(S[num])
        sm = difflib.SequenceMatcher(None, a, b)
        r = sm.ratio()
        flag = "OK  " if r >= 0.94 else "DRIFT"
        print(f"[{flag}] {num}  similarity {r:.3f}")
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            print(f"    {tag:8} V1: {' '.join(a[i1:i2])[:78]!r}")
            print(f"    {'':8} V2: {' '.join(b[j1:j2])[:78]!r}")
        if r < 0.94:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or sorted(V1_WORDS)))
```

Note what it compares: the variant **script text** against the body's
**Whisper transcript**, not against the body's script. That is stricter and
correct: it catches the case where the body's audio never actually said what
the body's script claimed. The `norm()` replacements exist because the
transcript contains Whisper's split tokens while the script spells the words.

**What a clean run looks like**, from the original account's three
question-to-statement hook rewrites (run 2026-07-30):

```
[OK  ] 401  similarity 0.955
    delete   V1: 'does'
             V2: ''
    insert   V1: ''
             V2: "doesn't"
    delete   V1: 'yet'
             V2: ''
    delete   V1: 'if the answer is no'
             V2: ''
[OK  ] 402  similarity 0.964
    replace  V1: 'are you'
             V2: "you're"
    replace  V1: 'then'
             V2: 'and'
[OK  ] 404  similarity 0.970
    replace  V1: 'are you'
             V2: "you're"
    replace  V1: 'then'
             V2: 'so'
```

Exit code 0. All three above threshold, and the only opcodes are the hook plus
one clause that existed solely to serve the old question, exactly the
predicted shape. Use it as the reference.

### 4.2 `timings.py`: word timings, and the transcript you must read

Complete source:

```python
#!/usr/bin/env python3
"""Word-level timings for a VO wav -> public/words_*.json

    python3 timings.py vo/body_t1.wav public/words.json

Captions must never gap, so the composition needs a start and end for every
word. Always read the printed transcript before rendering: Whisper can mishear
a short brand line (the original account's three-word brand name came back
with one word swapped in one take), and it splits "50,000" into "50" + ",000"
and "100%" into "100" + "%". The compositions glue those back together, but a
misheard word has to be caught here.
"""
import json, pathlib, sys
import whisper

ROOT = pathlib.Path(__file__).parent


def main(src: pathlib.Path, out: pathlib.Path) -> None:
    m = whisper.load_model("small")
    r = m.transcribe(str(src), word_timestamps=True, language="en")

    words = []
    for seg in r["segments"]:
        for w in seg.get("words", []):
            words.append({
                "w": w["word"].strip(),
                "s": round(float(w["start"]), 3),
                "e": round(float(w["end"]), 3),
            })

    out.write_text(json.dumps(words, indent=1))
    print(" ".join(x["w"] for x in words))
    print(f"\n{len(words)} words · ends {words[-1]['e']}s · wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: timings.py <vo.wav> <out.json>")
    main(ROOT / sys.argv[1], ROOT / sys.argv[2])
```

Model is **whisper `small`**. The escalation path when something sounds wrong
is to re-run with `medium` and compare. That is how a phantom repeated phrase
was confirmed as a real audio defect on one roll, and how an abbreviated
industry term was confirmed as unpronounceable rather than mistranscribed.

Output shape, one object per word:

```json
[
 {"w": "You're", "s": 0.0,  "e": 0.34},
 {"w": "a",      "s": 0.34, "e": 0.46}
]
```

The last word's `e` value is what the Remotion configs call `voEnd`. **Re-cut a
voiceover and you must re-run `timings.py` and update `voEnd`, or the end card
will cut into the read.**

Both paths are resolved relative to `video/`, so call it as
`python3 timings.py vo/x.wav public/words_x.json` from inside `video/`.

### 4.3 `prosody.py`: the uptalk detector

This is the piece that turns "it sounds off but every word is right" into a
number.

It reports, per sentence-final word, whether pitch **rises** or **falls**
across that word. A statement should fall. **A rising terminal on a statement
is uptalk: it makes the line sound uncertain or like a question, and it is the
single most common way a Chatterbox take sounds "off" while every word is
still correct.**

**The threshold: anything above +6 Hz across a sentence-final word is audible
as uptalk.** `UPTALK_HZ = 6.0`.

**The documented fix, both halves together:**
1. Re-generate with **lower `exaggeration`**.
2. **Replace any ellipsis before the offending sentence with a hard stop.**

Do both. The ellipsis is what makes Chatterbox treat the pair as one continuing
utterance so the terminal never lands; the exaggeration is what gives it room
to swing upward.

Complete source:

```python
#!/usr/bin/env python3
"""Check a VO take for intonation problems you would otherwise have to hear.

    python3 prosody.py vo/body_t1.wav public/words.json

Reports, per sentence-final word, whether pitch RISES or FALLS across the word.
A statement should fall. A rising terminal on a statement is uptalk: it makes the
line sound uncertain or like a question, and it is the single most common way a
Chatterbox take sounds "off" while every word is still correct.

Also flags long gaps and words delivered much faster or slower than the take's
own average, which is how dropped or rushed phrases show up numerically.

Rule of thumb from the takes measured so far: anything above +6 Hz across a
sentence-final word is audible as uptalk. Re-generate with lower `exaggeration`
and replace any ellipsis before the offending sentence with a hard stop.
"""
import json, sys, warnings
import numpy as np
import librosa

warnings.filterwarnings("ignore")

UPTALK_HZ = 6.0
LONG_GAP_S = 0.9


def main(wav_path: str, words_path: str) -> None:
    y, sr = librosa.load(wav_path, sr=22050)
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=350, sr=sr, frame_length=1024)
    times = librosa.times_like(f0, sr=sr, hop_length=256)
    words = json.load(open(words_path))

    def contour(a: float, b: float):
        m = (times >= a) & (times < b) & voiced
        v = f0[m]
        return v[~np.isnan(v)]

    print(f"{wav_path}  ({words[-1]['e']:.2f}s, {len(words)} words)\n")
    print("SENTENCE ENDINGS  (a statement should fall)")
    problems = 0
    for w in words:
        if not w["w"].endswith((".", "?", "!")):
            continue
        # A question SHOULD rise. Flagging it was a false positive on a
        # question-opening script.
        if w["w"].endswith("?"):
            continue
        v = contour(w["s"], w["e"])
        if len(v) < 6:
            print(f"  {w['s']:6.2f}  {w['w']:<14} not enough voiced pitch to measure")
            continue
        half = len(v) // 2
        delta = v[half:].mean() - v[:half].mean()
        if delta > UPTALK_HZ:
            tag, bad = "RISES  <-- uptalk", True
        elif delta < -UPTALK_HZ:
            tag, bad = "falls", False
        else:
            tag, bad = "flat", False
        problems += bad
        print(f"  {w['s']:6.2f}  {w['w']:<14} {v.mean():5.0f} Hz  {delta:+6.1f} Hz  {tag}")

    print("\nLONG GAPS  (a stutter or a dropped phrase often hides in one)")
    for i in range(1, len(words)):
        gap = words[i]["s"] - words[i - 1]["e"]
        if gap >= LONG_GAP_S:
            print(f"  {words[i-1]['e']:6.2f}  {gap:.2f}s after {words[i-1]['w']!r}")

    durs = np.array([w["e"] - w["s"] for w in words])
    slow = [w for w, d in zip(words, durs) if d > durs.mean() + 3 * durs.std()]
    if slow:
        print("\nUNUSUALLY LONG WORDS  (whisper collapsing speech it failed to transcribe)")
        for w in slow:
            print(f"  {w['s']:6.2f}  {w['w']!r} spans {w['e']-w['s']:.2f}s")

    print(f"\n{problems} uptalk problem(s)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: prosody.py <vo.wav> <words.json>")
    main(sys.argv[1], sys.argv[2])
```

Three things it reports, and what each one means:

| Report | Detects | Threshold |
|---|---|---|
| **Sentence endings** | uptalk on statements | `delta > +6.0 Hz` = RISES |
| **Long gaps** | a stutter or a dropped phrase hiding in the silence | gap ≥ **0.9 s** |
| **Unusually long words** | Whisper collapsing speech it failed to transcribe | duration > mean + **3σ** |

Mechanics worth knowing before you trust the number: pitch is tracked with
`librosa.pyin` at 22.05 kHz, `fmin=60`, `fmax=350`. The delta is the mean of
the second half of the word's voiced pitch minus the mean of the first half.
Fewer than 6 voiced frames prints "not enough voiced pitch to measure" rather
than a number. Treat that as *unmeasured*, not *passed*.

**Questions are skipped on purpose.** A question *should* rise; flagging one
was a false positive on a question-opening script in the original account.
That is why question-opening scripts do not light this up.

Real numbers from the original account's shipped takes, so you know what
"good" looks like (words genericized):

| Take | Falling terminals reported |
|---|---|
| Hook variant A, pick of 3 | three terminals at −11.9 Hz · −10.3 · −8.4 |
| Hook variant B, pick of 3 | three terminals at −23.2 Hz · −12.8 · −10.0 |
| Hook variant C, pick of 3 | three terminals at −16.8 Hz · −13.8 · −7.4 |

And the failures it caught: the first fixed-body take had terminals at
**+20.9 Hz** and **+35.1 Hz**; one hook take had uptalk on two endings;
another had uptalk on one.

### 4.4 The gate

**Zero uptalk problems, transcript read word for word against the script, and
the operator has listened to the take. All three.**

If a take fails, you do not fix it in post. You re-roll, and you keep the
failed take. That is what the numbered filenames are for.

---

## 5. Getting a take into a render

The generator writes to `video/vo/`. Remotion reads from `video/public/audio/`.
**In the original tree nothing bridged those two directories.** It was a manual
`cp`. The mapping was verified by checksum rather than by trusting the
filenames: fourteen files in `public/audio/` were each byte-identical to a
specific take in `vo/`, plus two orphans left over from an abandoned build
that nothing referenced. Do not delete orphans without checking, but do not
assume they are live either.

`voice.py publish <id> --take <n>` performs that copy explicitly. It is the
one capability the consolidated module adds that the originals did not have.

**The paid cuts are built, not published.** `build_paid.py` and
`build_rsvp_paid.py` read the outro take from `vo/` directly and write
`public/audio/vo_paid_<n>.wav` and `public/audio/vo_rsvp_paid_<n>.wav`
themselves. That is why `outro` has `publish: None`.

**With one break in the chain, and it is the best trap in this section.** In
the original account, `build_paid.py::VARIANTS` was keyed 401-404 and wrote
`vo_paid_401.wav` … `vo_paid_404.wav`. But the paid configs read
`audio/vo_paid_411.wav` … `vo_paid_414.wav` and `bed_paid_411.mp3` …
`bed_paid_414.mp3`, and **nothing in the tree wrote the 41x files** (grepped
`*.py` and `*.sh`). Both sets were present on disk and byte-identical:

```
SAME  vo_paid_401.wav  vo_paid_411.wav     (2,067,438 bytes)
SAME  vo_paid_402.wav  vo_paid_412.wav     (1,804,398 bytes)
SAME  vo_paid_403.wav  vo_paid_413.wav     (2,072,718 bytes)
SAME  vo_paid_404.wav  vo_paid_414.wav     (1,987,758 bytes)
```

so the renders were correct *right now* and nothing looked broken. The moment
anyone regenerated the outro and re-ran `build_paid.py`, those paid
compositions would keep rendering the old offer with no error and no warning.
The 411-414 series was a retired way of encoding "the paid one"; the config
was never migrated with it. The other waves were clean: their configs read the
numbers their builders write. The general check: **grep your configs for every
audio filename and confirm a builder writes each one.** Open question 10.

Both builders use the same two constants:

```python
GAP = 0.55          # beat between the body and the offer, so the turn is audible
END_CARD = 3.6      # must match END_CARD in the paid-ad component (and the RSVP one)
```

and both merge word timings by shifting the outro by `body_duration + GAP`, so
the offer's captions land correctly without re-running Whisper on the joined
file. `voEnd` is then `merged[-1]["e"] + 0.22`.

---

## 6. Music

### 6.1 Two kinds of music in this account, and only one of them is safe

| | Originally composed | Supplied tracks |
|---|---|---|
| Files | `audio/bed_phrygian.wav` (written by `bed.py` when you run it) and a second composition made the same way | three `.m4a` tracks supplied by the operator |
| Used by | the aerial wave, and one assembly | every other wave in the original account |
| Rights | **zero encumbrance, we wrote it** | **no clearance evidence, either way** |

From the original ads README, open item 2 (track names genericized):

> **Music licensing is undocumented** on all three tracks used across the
> first wave. All supplied by the operator, none with clearance evidence. The
> aerial wave uses originally composed music and does not have this problem.

And from one caption's notes:

> Music: a supplied track, stored in `video/audio/`. **Licensing
> unconfirmed**, no clearance evidence either way. Confirm before this runs
> paid.

**That is why `bed.py` exists.** Not because the supplied tracks sound wrong,
but because a paid ad running on someone else's music is a liability nobody
wrote down. The standing instruction is: **do not substitute a track someone
found.**

### 6.2 Which track is under which ad

In the original account, the three supplied tracks were assigned per persona,
and the format-test paid cuts deliberately matched the track of the ad each
concept tested against, so a format-test cut and its counterpart sounded the
same:

| Track | Coverage |
|---|---|
| Supplied track A | two persona bodies and three of their variants |
| Supplied track B | four persona bodies/variants and six format-test cuts |
| Supplied track C | one persona body and three format-test cuts |
| `audio/bed_phrygian.wav` | the aerial wave (both offers, both hook arms) and one assembly |

**All three uncleared tracks were load-bearing across 19 of the account's paid
cuts**: the 11 entries in `build_paid.py::VARIANTS` plus the 8 in
`build_rsvp_paid.py::VARIANTS`. The FREE cuts of the same concepts used the
same three tracks, so the real exposure was larger than 19 files; 19 was just
the paid count. If clearance comes back negative on a supplied track, that is
not a one-file fix. It is a re-score of everything except the composed-bed
wave. Compose your beds.

### 6.3 `bed.py`: the originally composed bed

A cinematic drone in **C Phrygian**, matched to the reference ad's harmony. No
percussion, no melody, sustained pad over a C pedal, so it loops without a
downbeat and the wrap is inaudible under a read of any length.

The harmony was not guessed. It came from a **per-second FFT of the source
clip over 45-400 Hz**:

```
0-3s  C   (C2 C3 G3)      i
3-4s  Db  (Db3 F3 F4)     bII  <- the Neapolitan doing all the work
4-6s  Eb  (Eb2 Bb3 C4)    III
6-8s  C   (C2 C3 C4)      i
8-9s  Db  (Db2 F3 C4)     bII
```

Phrygian is the mode with a flat second degree. That `bII`, the Neapolitan, is
what gives the bed its unease without a single minor-key cliché, and the
comment in the source says so explicitly because it is the one chord you must
not "correct" if you edit this.

Complete source. Writes `audio/bed_phrygian.wav`, 10 seconds, 48 kHz stereo:

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

Two design notes in there that are worth keeping when you edit it:

- **The lowpass sweep is crossfaded across a fixed filter ladder, not
  re-designed per block.** Re-designing a Butterworth filter block by block
  clicks at every block edge, a ~23 Hz ratchet, audible as a buzz. Nine fixed
  cutoffs from 900 Hz to 3200 Hz, geometrically spaced, with triangular
  interpolation weights, gives movement with no discontinuity anywhere.
- **Output is normalised then multiplied by 0.72.** That headroom is for the
  voiceover and any clip ambience mixed on top of it. Do not "fix" the level.

**It writes to `audio/bed_phrygian.wav` with a relative path**, so you must
run it from inside `video/`:

```bash
cd video && python3 bed.py
```

To make a bed for a different reference ad, repeat the method, not the notes:
per-second FFT of the source clip over 45-400 Hz, name the chords, pick the
mode they imply, and keep the constraints (no percussion, no melody, sustained
pad over a pedal, headroom left for the voice). The original account produced
a second bed exactly this way for its captions format.

### 6.4 `make_bed.sh`: fitting a track to a cut

Used by `build_paid.py` and `build_rsvp_paid.py`. Complete source:

```bash
#!/bin/bash
# make_bed.sh <source-track> <video-duration-seconds> <output.mp3>
# Music runs edge to edge at full strength. Loops if the track is shorter than
# the video. Only a 0.4s tail fade to avoid a click. Nothing dies under the end card.
set -e
SRC="$1"; DUR="$2"; OUT="$3"; START="${4:-0}"

SRCDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
USABLE=$(echo "$SRCDUR - $START" | bc)
NEED=$(echo "$DUR + 0.5" | bc)

if (( $(echo "$USABLE < $NEED" | bc -l) )); then
  LOOPS=$(python3 -c "import math;print(int(math.ceil($NEED/$USABLE)))")
  echo "  track $USABLE s < needed $NEED s -> looping ${LOOPS}x"
  ffmpeg -y -stream_loop $((LOOPS)) -ss "$START" -i "$SRC" -t "$NEED" \
    -af "afade=t=in:st=0:d=0.8,afade=t=out:st=$(echo "$DUR-0.4"|bc):d=0.4,loudnorm=I=-19:TP=-2:LRA=9" \
    -c:a libmp3lame -b:a 192k "$OUT" -loglevel error
else
  ffmpeg -y -ss "$START" -i "$SRC" -t "$NEED" \
    -af "afade=t=in:st=0:d=0.8,afade=t=out:st=$(echo "$DUR-0.4"|bc):d=0.4,loudnorm=I=-19:TP=-2:LRA=9" \
    -c:a libmp3lame -b:a 192k "$OUT" -loglevel error
fi
echo "  bed: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s for a ${DUR}s video"
```

Fixed decisions in there: **0.8 s fade in, 0.4 s fade out** (short enough that
nothing dies under the end card, long enough to avoid a click), loudness
normalised to **I=-19 LUFS, TP=-2 dBTP, LRA=9**, MP3 at 192 kbps, and it
always renders `DUR + 0.5` seconds so the video never runs off the end of the
bed.

### 6.5 How the music sits in the mix

**The bed must lift for the end card.** Held flat under speech it disappears
the moment the voiceover stops, and this was *measured*, not felt. From the
original account's failure log:

> **Music must lift for the end card.** Held at 16% under speech it disappears
> the moment the VO stops (**measured a 12 dB drop**). It now ramps to 55% over
> 0.6s at `VO_END`. Verify with `astats` on the delivered file, not the bed file.

From the paid-ad component, the actual volume callback (note `FPS`, a module
constant, not the `fps` from `useVideoConfig`):

```ts
<Audio src={staticFile(c.bed)} volume={(f) => {
  const tt = f / FPS;
  return tt < c.voEnd ? 0.16 : Math.min(0.55, 0.16 + ((tt - c.voEnd) / 0.6) * 0.39);
}} />
```

0.16 under the read, ramping to 0.55 over 0.6 s at `voEnd`. The callback is
duplicated in both return branches of that component (hook card and body), so
if you change one, change both.

The RSVP component uses the same shape at lower levels and adds `loop`:

```ts
<Audio loop src={staticFile(c.bed)} volume={(f) => {
  const tt = f / FPS;
  return tt < c.voEnd ? 0.14 : Math.min(0.5, 0.14 + ((tt - c.voEnd) / 0.6) * 0.36);
}} />
```

The `loop` is there for a reason, and the rejected alternative is the
important half of it. From that component's comment:

> Looped because a few beds are shorter than their read plus the end card:
> one bed is 26.6s against a 28.3s read. **The alternative was borrowing a
> longer persona's track, which would add a second variable to a test whose
> whole point is that only the format moved.** These are sustained drones with
> no percussion, so the wrap is not a downbeat.

(That bed measured 26.600 s; the comment's number is accurate.) That is the
same property `bed.py` was written to have: no downbeat, so a loop point is
inaudible.

**Verify the lift on the delivered file with `astats`, not on the bed file.**
The bed file is flat by construction; the ramp only exists after the render.

Where ffmpeg does the mixing instead of Remotion, the recipes are:

**Read the label on the first one before you copy it.** The prototype
`build.sh` is *not* the main pipeline. It was the original 9:16 test ad:
stills, Ken Burns zoompan, PNG caption overlays, an ElevenLabs VO, and a
procedural placeholder bed built from two `sine` sources and pink noise. It
predates the standing rule "**Hard cuts only**. No Ken Burns, no crossfades"
and violates it. The sidechain recipe below is still the best
duck-the-bed-under-VO reference in the tree; the rest of that script is not a
model to follow.

```bash
# prototype build.sh — VO ducks the bed via sidechain compression
[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=1.0,asplit=2[vo1][vo2];
[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.55[bg];
[bg][vo1]sidechaincompress=threshold=0.04:ratio=9:attack=8:release=380[duck];
[duck][vo2]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]

# aerial build scripts — byte-identical graphs. No VO in the aerial wave; the
# bed sits over the clip's own engine ambience. Note duration=shortest here
# against duration=longest above: the aerial cuts are fixed-length, so the mix
# ends when the shorter of clip and bed ends.
[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55[amb];
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[bed];
[bed][amb]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[a]
```

### 6.6 The unresolved AI-music-provenance question

**Status in the original account: open, unanswered, and it blocked clearing
the licensing item.** It is kept here because you will hit the same question
the first time someone hands you a track.

The only record of it in that repo was one line in the failure-log doc:

> Still open from before: confirm which Suno plan generated the first wave's
> music.

and its restatement in that doc's next-actions list.

What that line implies, and what it does not:

- **It implies** two of the supplied tracks were believed to have come out of
  Suno, an AI music service.
- **It does not establish** that they did. Elsewhere the same tracks were
  recorded only as "supplied by the operator", with no source named.
- **It says nothing at all** about the third track.

Why the plan matters and not just the tool: commercial-use rights on AI music
services are generally tied to the subscription tier that was active **at the
moment of generation**, and can differ for tracks made on a free tier versus a
paid one. So "we used Suno" is not an answer. The answer has to be the
account, the plan, and the generation date for each file. None of that could
be determined from the repo.

**Until someone produces that, for any supplied track:**

- Treat it as **uncleared**.
- Composed beds are unaffected. `bed.py` output has **zero rights
  encumbrance.** That is the reason the composed bed exists.
- **New work should use `bed.py`, not a supplied track.** Adding another
  uncleared file makes the eventual re-score bigger for no benefit.

---

## 7. Open questions

Things that could not be determined from the original source. None of these
are guesses dressed up as facts, and every one of them is a class of problem
your own account can reproduce.

1. **The outro script contradicted itself on `cfg_weight`.** Its docstring
   said "exaggeration 0.32 and cfg_weight 0.40 stop the terminals drifting
   upward"; its code passed `cfg_weight=0.32`. The code is what produced the
   shipped outro, so the consolidated table carries **0.32** and flags it.
   Someone has to decide whether the docstring is stale or the code is a typo
   that changed the shipped delivery. Keep docstrings and code in agreement.

2. **Two takes were edited by hand and no script in the repo does it.**
   Measured:

   | Raw | Trimmed | Removed | Format change |
   |---|---|---|---|
   | raw take A 28.42 s | trimmed 27.32 s | 1.10 s | f32 → s16 |
   | raw take B 30.34 s | trimmed 29.09 s | 1.25 s | f32 → s16 |

   The first and last 0.5 s of each pair matched byte for byte, so the cut is
   interior. That is consistent with excising a documented phantom repeat, but
   the cut points, the command used, and whether the same edit is needed on
   future rolls were all unrecorded. **No other take had a `_raw` twin**, so
   whatever this was, it was done twice and then stopped. Record your hand
   edits.

3. **The provenance of the voice reference clip was nowhere in the repo.**
   Every voiceover in the account was cloned from one 4.2-second clip. Where
   it came from, whether the speaker consented, and whether it could keep
   being used were all unanswered. For a paid ad account this is the same
   class of exposure as the music licensing item. Record the provenance and
   consent for your reference clip before you clone anything.

4. **One take on disk had no generating script.** A persona's generator wrote
   a `_v2` stem; a plain-stem file predated it and nothing in the repo
   produced it or recorded whether it differed in script. Orphan audio is a
   liability: you cannot regenerate what you cannot trace.

5. **Which AI-music plan, account and date produced each supplied track**,
   and whether the third track came from that service at all. See 6.6.

6. **Two rendered bed files were referenced by nothing.** Grepped across
   `*.py`, `*.sh`, `*.ts`, `*.tsx` and `*.md`: only `bed_phrygian.wav` was
   ever read. Both may be stale renders; they were documented, not deleted.

7. **The output path of `bed.py` disagreed with the engine doc.** The repo
   file wrote `audio/bed_phrygian.wav` and the build scripts read exactly
   that; the doc described a version writing `public/audio/bed_phrygian.wav`.
   The repo file is the one the builds used; which is intended going forward
   was not settled.

8. **`check_script.py` covered only three of the four bodies.** One body had
   a variant that moved the *close*, not the hook, and it was not checked by
   anything. Adding it is a one-line change; whether it was left out
   deliberately was unknown. The "one variable" logic applies to any variant,
   not just hook variants.

9. **Nothing verifies that a published take matches the `voEnd` in its
   config.** `voEnd` is hand-copied from `timings.py` output into the
   configs. A re-cut voiceover with a stale `voEnd` renders an end card that
   cuts into the read, and no check catches it. A comment warns about it;
   nothing enforces it.

10. **One paid config read audio no script writes.** The 411-414 trap in
    section 5. The files were duplicated on disk and byte-identical, so this
    was latent, not broken. The fix is either repointing the config or adding
    the retired numbers back to the builder; someone has to pick one.

11. **`vo/*.wav` was gitignored.** Every take, including the shipped picks
    and the outro, existed only on one machine. The rule "never overwrite a
    take" was protecting files that no backup covered. Decide on purpose
    whether your takes are backed up.

12. **Nobody wrote down why the prototype build and its VO were still in the
    tree.** The prototype used Ken Burns, which the standing rules ban, and
    its bed was a procedural sine-and-noise placeholder. It looked like the
    first prototype, kept. It was documented rather than declared dead,
    because its rendered VO was a real asset and nothing confirmed it was
    unused.

---

## AUDIT NOTES (adversarial pass, 2026-07-30)

Every claim in this section was re-checked against the original source.
Corrections applied in place; nothing was deleted without a replacement. Doc
and file names below are genericized for this kit; the findings are not.

### Corrections made

**FABRICATION**

1. **§2.3 said the ElevenLabs helper "writes the API's error body to the
   output file rather than raising."** It does not. The original helper
   catches `HTTPError`, prints, and returns `False` *before* the
   `write_bytes`. Replaced with a correction block; the two JSON files on
   disk were real but no current code produced them. This also removed a
   self-contradiction: merge note 4 already said the opposite of §2.3.
2. **§1 claimed ElevenLabs is "deterministic enough to not re-roll."** No
   source supported it; each of the four eval calls ran exactly once. Changed
   to "not measured here."
3. **§2.4 asserted "if you feed TAGGED to a turbo model it will speak the
   brackets."** Nothing in the repo said this. The source showed only the
   pairing (TAGGED→`eleven_v3`, PLAIN→`eleven_turbo_v2_5`). Downgraded to a
   stated working assumption, with a second tagged-with-`eleven_v3` script
   cited as the corroborating instance of the pairing.

**WRONG CONSTANTS**

4. **§6.2 said "20 of the account's paid cuts."** The real count is **19**:
   11 in `build_paid.py` + 8 in `build_rsvp_paid.py`. Corrected, with a note
   that the FREE cuts widen the real exposure.
5. **§6.5 quoted the Remotion volume callback as `const tt = f / fps;`.** The
   source uses `FPS`, a module constant, not the `fps` from `useVideoConfig`.
   Corrected, and the fact that the callback is duplicated in both return
   branches is now stated.

**SILENT BEHAVIOUR LOSS**

6. **`make_ad.py` was never mentioned.** It was a third ElevenLabs caller and
   a near-duplicate of `tts.py` (own VOICES map with six of the eight
   entries, own POST helper). The consolidation claimed to replace "nine
   `vo_*.py` scripts and `tts.py`" and silently dropped it. It carried two
   things nothing else in the tree had: the **`POST /v1/music` call** (prompt
   + `music_length_ms: 24000`) and the **VO script the prototype build
   depends on**. Both are now in the module as `eleven_music()` /
   `MUSIC_PROMPT` / `MUSIC_MS` and a SCRIPTS note, with a `music` subcommand
   wired into `main()`. Merge note 8 records the reconciled differences
   (filename-vs-stem, 180 s vs 120 s timeout, 200 vs 220 char error
   truncation).
7. **CLI defaults changed without being disclosed.** One original script took
   a bare positional take count and defaulted to a specific job; two others
   defaulted to generating *everything*. Now merge note 9.

**STRIPPED LESSONS**

8. The fixed-body script's "free CTA only, the paid versions come as a
   separate pass so the offer is a clean variable" rule was missing from its
   entry. Restored; it is the reason the outro is a separate entry at all.
9. "Verify with prosody.py after" was missing from the fixed-body entry.
   Restored.
10. "No price is stated; the funnel is unchanged: subscribe free, then the
    platform's paywall presents the paid tier" was missing from the outro
    entry. Restored (genericized here).
11. "Same voice and reference clip as the main wave on purpose: this is a new
    FORMAT, not a new voice" was missing from the format-test entry.
    Restored.
12. §6.5 kept the *reason* for `loop` but dropped the **rejected
    alternative** ("borrowing a longer persona's track would add a second
    variable to a test whose whole point is that only the format moved") and
    the "sustained drones, no percussion, so the wrap is not a downbeat"
    justification. Both restored.
13. The **12 dB measurement** behind the end-card lift was missing. Restored
    as a quote.
14. "**Reuse an existing voiceover**: always the first choice for a format
    test" and the "confirm `.env` is gitignored, then confirm the key works
    with one cheap call" gate were both absent. Added as "route zero" in §1
    and in the module docstring.

**SCOPE ERRORS**

15. **§0 said "Not yet judged by ear" appears on three cuts.** It appeared in
    **fourteen** caption files: the whole format-test wave plus both offers
    of the hook wave. Corrected.
16. **§6.5 presented the prototype's filter graph without saying what the
    prototype is.** It is the legacy 9:16 build (Ken Burns zoompan,
    procedural sine+pink-noise bed) and it violates the hard-cuts-only rule.
    Labelled.

**NEW FINDING, latent, not yet broken**

17. **One paid config read audio no script writes.** The config read a
    retired numbering's filenames while the builder wrote the current
    numbering's, with byte-identical stale copies on disk masking it
    (verified by md5). **Regenerate the outro and those paid cuts silently
    keep the old offer.** This directly undercuts the "change the offer in
    one place" guarantee that §3.3 and §5 both assert. Documented in the
    `outro` entry, in §5 with the checksum evidence, and as open question 10.
    The other waves were unaffected.

18. Added open questions **11** (takes gitignored, so every take existed on
    one machine only) and **12** (prototype build status unrecorded).

### Verified correct — no change needed

Ran or measured against the original repo, not assumed:

- **`check_script.py`, `timings.py`, `prosody.py`, `bed.py`, `make_bed.sh`
  were reproduced byte-identically from that repo** (this kit's copies then
  received the genericization edits called out inline: example paths, the
  `norm()` numbers, the `scripts()` source file, and docstring examples).
  All embedded Python blocks parse under `ast.parse`. No `...`, no "rest of
  file unchanged", no truncated function anywhere.
- **`check_script.py` actually run.** Output matched the section's claimed
  "current state" exactly: similarities 0.955 / 0.964 / 0.970, same opcodes,
  exit 0.
- **Both ElevenLabs 403 bodies** read from disk (227 and 259 bytes). Verbatim
  match (request ids elided in this kit).
- **All stock voice IDs** match the original source character for character.
- **All four eval-call settings** match the source, including `sim`
  defaulting to 0.75 and `use_speaker_boost=True`.
- **The reference clip**: ffprobe gave `mp3, 44100 Hz, mono, 4.226032 s,
  64911 bit/s, 34290 bytes`. The section's "4.226 s / 44.1 kHz / mono /
  ~65 kbps / 34,290 bytes" is right.
- **All nine `vo_*.py` hardcoded the same `REF` path**, confirmed by grep, 9
  of 9.
- **Chatterbox output format** `pcm_f32le, 24000, 1`, confirmed on three
  takes.
- **Every tuning pair** in §3.4 confirmed against its source script. **The
  outro docstring-says-0.40 / code-passes-0.32 contradiction is real**; open
  question 1 is correctly stated.
- **All 14 rows of the §5 checksum mapping** re-verified with `md5 -q`. Every
  pair SAME, including the two orphans.
- **The orphans are orphans.** Grep for their names across
  `*.ts/*.tsx/*.py/*.sh/*.md` returned nothing; the RSVP config pointed at
  the reused hook takes instead, as claimed.
- **Nothing bridged `vo/` → `public/audio/`.** Grep confirmed no script
  performed that copy; §5's "it was a manual `cp`" holds.
- **Hand-edit measurements** (28.42→27.32 s and 30.34→29.09 s, f32→s16)
  exactly as stated, and no other take had a `_raw` twin.
- **The music mapping** matched both builders' VARIANTS row for row.
- **`GAP = 0.55`, `END_CARD = 3.6`, `voEnd = merged[-1]["e"] + 0.22`**: all
  correct in both builders.
- **`make_bed.sh` constants**: 0.8 s in, 0.4 s out, `I=-19:TP=-2:LRA=9`,
  192 kbps, `DUR + 0.5`. All correct.
- **`bed.py`**: `SR 48000`, `DUR 10.0`, and the output measured
  `pcm_s16le, 48000 Hz, 2 ch, 10.000000 s`. The Neapolitan/`bII` comment, the
  9-band `geomspace(900, 3200, 9)` crossfade ladder, the ~23 Hz ratchet
  warning, and the `*= 0.72` headroom are all present and match the source.
- **The looped bed measured 26.600 s**, so the component comment's "26.6s
  against a 28.3s read" is accurate.
- **The two unreferenced bed renders are unreferenced**: grep found only
  `bed_phrygian.wav` read anywhere.
- **Open question 7 is real**: the repo file wrote `audio/bed_phrygian.wav`;
  the engine doc described `public/audio/bed_phrygian.wav`.
- **`UPTALK_HZ = 6.0`, `LONG_GAP_S = 0.9`, mean + 3σ,
  `pyin(fmin=60, fmax=350)` at 22050 Hz, `len(v) < 6` unmeasured, questions
  skipped**: all correct against the source.
- **Every prosody number quoted** (the three shipped takes' falling
  terminals, the +20.9 Hz and +35.1 Hz failures, the 0.573 drift score)
  traces to a caption note or source comment in the original repo.
- **Both long quotes in §0** were verbatim from the original standing rules
  and failure log (names genericized in this kit).
- **§6.1's licensing quotes** were verbatim from the original README and one
  caption file (track names genericized in this kit).
- **ElevenLabs account facts**: project-scoped key limited to Text-to-Speech
  / Music Generation / Voices-read; Creator ~$22/mo (three independent
  places); `.env` mode `600` and gitignored (checked both); the Replicate
  token sharing that file needed rotating after a transcript paste. The
  section is right that these are two different credentials sharing one file.
- **"Free, MIT"** for Chatterbox is sourced and the installed package's
  metadata carries MIT licence text. It resolves to
  `site-packages/chatterbox`, as claimed.
- **§6.6**: the failure-log doc really contains only the two lines
  paraphrased, really says nothing about the third track, and the section's
  refusal to infer more is the right call.

### Not verified, and why

- Nothing in this section was executed against a paid API. `check_script.py`
  was the only script run; it is pure `difflib` over local JSON.
- No one listened to any take during the audit. Every prosody and transcript
  claim traces to a caption note or a source comment, not to ears, which is
  precisely the gap section 0 is about.
