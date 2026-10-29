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

> **Extra note for this section:** the audit removed an entire model
> (`flux-1.1-pro`) that had been written up with a full config block but
> never existed in this project, and replaced an invented prompt with the
> real one. If you find a model named here that you cannot locate in a real
> script, treat it as suspect and check before spending.

# PART 30 — The generation layer: Replicate, Seedance, Nano Banana Pro, and the still/sheet workflow

This is the part of the engine that makes pixels that did not exist before: the
video clips, the character sheets, the scene stills, the surgical edits. It sits
*before* the edit. Nothing here touches Remotion, ffmpeg assembly, voice or
music — those are other parts. When this part is finished you have a folder of
mp4s and jpgs; everything downstream treats them as footage.

Two platforms are involved and they are not interchangeable:

- **Replicate** — a plain HTTPS API, billed in USD, used for **Seedance**
  (video), **Veo** (video with faces), **Nano Banana Pro** (images/edits) and
  **Kling 2.5** (video with faces + props). Exactly four model slugs appear
  anywhere in this project's Replicate code; there is no fifth. This is the
  part you can drive from a script, and the script is in this file.
- **Kling** — driven through its own MCP tool surface, billed in **credits**,
  used for the dialogue video and for the whole character-sheet/still workflow
  (`gpt-image-2`, `kling-image-v3_0_omni`, `kling-image-o1`). It has no
  scriptable HTTP client in this repo. It is documented here because the image
  **routing decision** spans both platforms and you cannot make it correctly by
  looking at only one.

Read Part 6's playbook first if you have not. This part goes deeper on the
specific models and gives you the runner.

> **fal is now the default generation account** (`parts/55-generation-fal.md`).
> Start there for voices, talking takes, lip sync, cutouts, silent Kling clips
> and Nano Banana Pro stills. Use this part for the Replicate models in the
> tables below (Veo 3.1 and Seedance 2.0 have no fal equivalent proven in this
> engine) and for the image routing across Kling's own models, which applies
> whichever account you generate on.

---

## 30.1 — The routing decision, in one table

The single most expensive mistake in this project was sending a job to the wrong
model and then trying to fix the result with prompt wording. Route first.

### Video

| Model | Where | Use it for | It refuses / breaks |
|---|---|---|---|
| `bytedance/seedance-2.0` | Replicate | Landscapes, aerials, action, the door break, wides, any shot with **no supplied human face**. Native audio is good. First-frame + last-frame interpolation is good. | **Any human face as an input, in any slot.** See 30.4. |
| `google/veo-3.1` | Replicate | The only model that takes a face input **and** produces native audio with lip sync. 9:16, 4/6/8s, 1080p. | Weapon-over-person two-shots. Rate-limits hard (429 — submit sequentially with 45s backoff). Drifts in the last ~0.5s: props vanish, faces bruise. Trim early, always check tails. |
| `kwaivgi/kling-v2.5-turbo-pro` | Replicate | Faces plus props/weapons. No audio at all. Inputs are `start_image` / `duration` / `aspect_ratio` / `negative_prompt`. | Silent only, so every line needs dubbing, which is the failure this project spent the most money on. Confirmed silent: `gen/char_kling.mp4` (1080x1920, 5.04s) has a video stream and no audio stream. |
| `kling-video-v3_0` / `_omni` | Kling MCP | Dialogue with native audio, multi-shot, up to 7 reference images. This is where the 409 dialogue went. | See Part 6's Kling rules. `kwaivgi/kling-v3` **does not exist on Replicate** (probed, 404) — Kling 3.0 is the reason this project has a second platform at all. |

### Images

Prices below are **Kling credits for 2 images at 2k**, measured 2026-07-29. They
are not USD and they are not comparable to Replicate's bill.

| Model | Platform | Credits | Use it for |
|---|---|---|---|
| `gpt-image-2` (t2i) / `gpt-image2` (i2i) | Kling | **70** | Part A portraits, the **Part C A24 triptych compile**, base images, and any shot where instruction-following must be exact (from-behind framings, precise blocking). Best analog/film grade fidelity of the three. |
| `gemini-3.1-flash-image` (Nano Banana 2) | Kling | **30** | General image work with no identity matching. **Rejects likeness prompts** — see 30.6. |
| `kling-image-v3_0_omni` | Kling | **4** | Reference-consistency and identity matching: Part B profiles, new camera angles off an approved base image, location sheets, no-face detail shots. The default for everything except the A24 compile. |
| `kling-image-o1` | Kling | ~2 | Surgical single-change edits on an already-approved frame. Removing debris, replacing a background behind an untouched subject. High feature consistency. |
| `google/nano-banana-pro` | Replicate | USD, see 30.8 | Text-to-image sheets and stills, and multi-reference edits, when you are already in the Replicate script and do not need Kling's identity lock. It made every Replicate-side image in this project including the sky/atoll first-frames. **Returns wrong sizes — always normalise.** |

**The spread is 17x** (70 credits vs 4). That is the whole reason routing
matters. Two rules fall straight out of it:

> **Any reference-consistency work goes to Kling's own image models.**
> **Any graded hero compile goes to the GPT-image class.**
> Everything else, the cheapest thing that can do it.

---

## 30.2 — `scripts/gen.py` — the runner

This consolidates `video/rep.py` and the **32** near-identical throwaway scripts
that were written into `/tmp` during the 405-409 sessions. Counted, not
estimated: `grep -l api.replicate.com /tmp/*.py` returns 32 files, and here they
all are, so nothing is quietly left behind —

`animate.py`, `batch409.py`, `batch409b.py`, `char_still.py`, `char_t2v.py`,
`char_vid.py`, `edit_creature.py`, `edit_first.py`, `edit_last2.py`,
`fix_c.py`, `fix_man.py`, `kling2.py`, `kling_test.py`, `ref_test.py`,
`regen_B.py`, `regen_vids.py`, `retry_s6.py`, `run_c3.py`, `run_c4.py`,
`run_creature.py`, `run_sky.py`, `run_sky2.py`, `run_sky3.py`, `scenes.py`,
`sheet.py`, `sheet_test.py`, `sheets2.py`, `sky_edits.py`, `stage1.py`,
`stills409.py`, `veo.py`, `veo_shot.py`.

Every one of them re-declared the same six-line `call()` helper, the same poll
loop, and the same base64 data-URI helper. They differed only in the payload and
in which of the post-processing steps they happened to include. **They live in
`/tmp` and `/tmp` gets cleared** — if you want the originals, copy them
somewhere real before you reboot that Mac.

**What was merged, and the behaviour differences that had to be reconciled:**

1. **Poll interval.** `rep.py` and the image scripts polled every **3s**; the
   Seedance scripts every **5s**; the Veo and Kling-2.5 scripts every **8s**
   (`veo.py`, `veo_shot.py`, `kling2.py`) and the Veo *batch* runners every
   **10s** (`batch409.py`, `batch409b.py`, `retry_s6.py`). Now per-model in the
   registry (`poll`): 3 for images, 5 for Seedance, 10 for Veo, 8 for Kling 2.5.
   The one behaviour change is that a single Veo job is now polled at the batch
   runner's 10s rather than 8s — deliberate, Veo is the model that rate-limits.
2. **Size normalisation.** Present in the frame scripts (`fix_c.py`,
   `regen_B.py`, `edit_first.py`, `edit_last2.py`, `sky_edits.py`,
   `char_still.py`, `stills409.py`, `scenes.py`), absent from `rep.py` and
   absent from the **sheet** scripts (`sheet.py`, `sheets2.py`, `stage1.py`,
   `fix_man.py`). That was not an oversight: a 16:9 character sheet
   centre-cropped to 9:16 loses its outer panels. Preserved as an explicit
   `--role` flag — `frame` normalises, `sheet` never does. **Do not "fix" a
   sheet by normalising it.**
3. **The crop guard.** Early scripts did `t=(h-1920)//2` (`edit_first.py:25`,
   `edit_last2.py:30`, `sky_edits.py:32`); later ones added
   `t=max(0,(h-1920)//2)` and `min(h,t+1920)` (`char_still.py:26`,
   `fix_c.py:27`, `regen_B.py:29`, `stills409.py:46`, `scenes.py:47`).
   **Both are wrong, in different directions, and neither one crashes.**
   Verified against PIL: a 2752x1536 Nano Banana output scaled to width 1080
   becomes 1080x**603**. Unguarded, `crop((0,-659,1080,1261))` does not raise —
   PIL happily returns 1080x1920 with black bands top and bottom, so a
   letterboxed frame is fed to the next model with no error anywhere. Guarded,
   it returns a short **1080x603** that then breaks ffmpeg downstream.
   **Changed behaviour, declared:** the runner now cover-fits — scale so both
   axes meet or exceed the target, then centre-crop. It always returns exactly
   1080x1920.
4. **QA previews.** Two different sizes were used ad hoc: half-size
   (`sheet.py:23`, `fix_man.py:26`) and 360x640 (`fix_c.py:29`,
   `regen_B.py:31`). Collapsed to one `--preview` flag that fits the longest
   side to 720px and preserves aspect, so it works for sheets and frames alike.
5. **The 402 retry loop.** Only `edit_creature.py` had it (15 attempts, 60s
   apart, waiting for the Replicate account to be topped up). Promoted to a
   general `--wait-credit MINUTES` flag, default 0 so it fails fast unless you
   ask for it.
6. **`metrics.predict_time` formatting.** `rep.py` does
   `f"time {m.get('predict_time'):.1f}s"`, which raises `TypeError` when the
   key is absent but `metrics` is not. Fixed.
7. **Token lookup.** `rep.py` read only `video/.env`. The runner now checks
   `$REPLICATE_API_TOKEN`, then `.env` in the cwd, then next to the script, then
   one directory up — a superset, so the old invocation still works.
8. **Error handling.** The scripts all did
   `sys.exit("FAILED: " + str(pred.get("error")))` indiscriminately, spending a
   fresh generation on every rerun. The runner now distinguishes a transient
   failure (retried) from a content refusal (never retried). See 30.7.
9. **The 429 loop.** `batch409.py` fired ten Veo jobs at once through a
   `ThreadPoolExecutor(max_workers=10)` and got rate-limited; `batch409b.py`
   was the rewrite — sequential, `for attempt in range(8)` with `time.sleep(45)`
   on 429, and an `os.path.exists` skip so a rerun does not regenerate what is
   already on disk. The runner's `batch` subcommand is sequential for the same
   reason. **Do not reintroduce the thread pool.**

`rep.py`'s behaviour is preserved as the `raw` subcommand, so anything in old
notes that says `python3 rep.py <slug> '<json>' <outfile>` still runs as
`python3 scripts/gen.py raw <slug> '<json>' <outfile>`. One deliberate
difference: `rep.py` polled forever, `raw` gives up after 1800s and tells you
the prediction id so you can find it on replicate.com.

```python
#!/usr/bin/env python3
"""Replicate generation runner for the video ad engine.

Submit a prediction, poll it, download the result, normalise the size.

Consolidates the old video/rep.py plus the 32 throwaway /tmp scripts that all
re-declared the same call/poll/base64 helpers and differed only in payload.

Subcommands
  video        one video generation (Seedance / Veo / Kling-on-Replicate)
  image        one image generation or multi-reference edit
  batch        a JSON list of either, run sequentially
  raw          rep.py's original behaviour: a slug and a literal JSON payload
  normalize    cover-fit an existing file to 1080x1920 (no API call)
  tone         PIL contrast/saturation drift table (the Part B acceptance test)
  match-sat    ffmpeg saturation sweep to hit a target saturation (no API call)
  schema       dump a model's Input properties from the Replicate API (free)

Requires: python3, pillow, ffmpeg (only for match-sat).
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

API = "https://api.replicate.com/v1"
HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Model registry.
#
# These four slugs, and ONLY these four, appear in this project's Replicate
# code. Every one of them has a successfully generated file on disk behind it,
# so the slug and the parameter names below are proven by use, not guessed:
#   bytedance/seedance-2.0          -> gen/lands_b.mp4, gen/creature_v4.mp4
#   google/veo-3.1                  -> gen/v409_s4.mp4, gen/veo_test.mp4
#   google/nano-banana-pro          -> gen/c409_man.jpg, gen/creature_last.jpg
#   kwaivgi/kling-v2.5-turbo-pro    -> gen/char_kling.mp4
# Do not guess new ones. The session record says the plausible variants
# (bytedance/seedance-2, -2-pro, -2-lite, -2-fast, and kwaivgi/kling-v3) were
# probed and 404'd, but that probe is NOT reproducible from anything in the
# repo - see the open questions. What IS solid: Kling 3.0 has no Replicate
# slug in use here, which is why this project also drives Kling's MCP.
#
# `keys` maps the runner's generic option names onto each model's real input
# parameter names, because they all disagree (image vs image_input,
# last_frame_image vs last_frame, and so on). None means "this model has no
# such parameter" and the runner will refuse the option rather than send junk.
# --------------------------------------------------------------------------
MODELS = {
    "seedance": dict(
        slug="bytedance/seedance-2.0",
        kind="video",
        poll=5,
        schema_verified=True,
        # HARD RULE: Seedance refuses human face inputs of ANY kind - i2v via
        # `image`, `reference_images`, even a white-background character sheet.
        # It fails with E005 "input or output was flagged as sensitive".
        # Text-to-video WITH people in the prompt is fine, and native audio is
        # fine. Route faces to Veo or to Kling.
        accepts_face_input=False,
        defaults={
            "aspect_ratio": "9:16",
            "resolution": "1080p",
            "duration": 9,
            "generate_audio": True,
        },
        keys={
            "first": "image",
            "last": "last_frame_image",
            "refs": "reference_images",
            "audio": "generate_audio",
            "seed": "seed",
            "ar": "aspect_ratio",
            "res": "resolution",
            "duration": "duration",
            "negative": None,
            "fmt": None,
        },
        # OBSERVED values only - this is not a dumped schema. Every Seedance
        # job in the source used 9:16 and 720p (iteration) or 1080p (finals),
        # confirmed by ffprobe on gen/creature_v4.mp4 (720x1280) and
        # gen/lands_b.mp4 (1080x1920). Anything outside this list gets a
        # WARNING, not a hard exit, because the real enum was never dumped.
        enums={
            "resolution": ["720p", "1080p"],
            "aspect_ratio": ["9:16"],
        },
    ),
    "veo": dict(
        slug="google/veo-3.1",
        kind="video",
        poll=10,
        schema_verified=True,
        # The ONLY model that takes a face input and still produces native
        # audio with lip sync. Rate-limits hard: submit sequentially, back off
        # 45s on 429. Drifts in the last ~0.5s (vanishing props, face
        # bruising) - trim early and always watch the tail.
        accepts_face_input=True,
        defaults={
            "aspect_ratio": "9:16",
            "resolution": "1080p",
            "duration": 8,
            "generate_audio": True,
        },
        keys={
            "first": "image",
            "last": "last_frame",
            "refs": "reference_images",
            "audio": "generate_audio",
            "seed": "seed",
            "ar": "aspect_ratio",
            "res": "resolution",
            "duration": "duration",
            "negative": "negative_prompt",
            "fmt": None,
        },
        # duration 4/6/8 and 9:16/1080p are from the handoff doc's model notes
        # and are confirmed by ffprobe: gen/v409_s4.mp4 is 4.0s 1080x1920 and
        # gen/v409_s8.mp4 is 6.0s 1080x1920. NOTE gen/veo_test.mp4 came back
        # 1280x720 because that job sent no aspect_ratio at all - Veo's own
        # default is landscape, so ALWAYS send 9:16 explicitly.
        enums={
            "resolution": ["720p", "1080p"],
            "aspect_ratio": ["16:9", "9:16"],
            "duration": [4, 6, 8],
        },
    ),
    "kling25": dict(
        slug="kwaivgi/kling-v2.5-turbo-pro",
        kind="video",
        poll=8,
        # The full Input schema was never written down, but the parameter names
        # below are proven: they are exactly what the two working scripts sent
        # (kling2.py, kling_test.py) and that call produced gen/char_kling.mp4
        # at 1080x1920, 5.04s, with NO audio stream. Note the first-frame slot
        # is `start_image`, not `image`. Run
        #   python3 scripts/gen.py schema kling25
        # if you need parameters beyond these five.
        schema_verified=True,
        accepts_face_input=True,
        defaults={
            "aspect_ratio": "9:16",
            "duration": 5,
        },
        keys={
            "first": "start_image",
            "last": None,
            "refs": None,
            "audio": None,           # this model has no audio, at all
            "seed": None,
            "ar": "aspect_ratio",
            "res": None,
            "duration": "duration",
            "negative": "negative_prompt",
            "fmt": None,
        },
        enums={},
    ),
    "nano-banana-pro": dict(
        slug="google/nano-banana-pro",
        kind="image",
        poll=3,
        schema_verified=True,
        accepts_face_input=True,
        # HARD RULE: this model returns WRONG SIZES. Measured off the files it
        # actually wrote, all at resolution "2K":
        #   16:9 -> 2752x1536  (gen/c409_man.jpg, gen/char_sheet.jpg)
        #   9:16 -> 1536x2752  (gen/c409_plate.jpg)
        #   1:1  -> 2048x2048  (gen/c409_locsheet.jpg)
        #   and 768x1344 turned up too (gen/still_a.png, gen/still_b.png)
        # Never assume the size you asked for. Anything that will seed a video
        # generation or land in a 9:16 cut must go through --role frame
        # (normalise to 1080x1920).
        #
        # aspect_ratio defaults to match_input_image because most jobs here are
        # EDITS. On a pure text-to-image call there is no input image to match,
        # so build_payload refuses that combination - pass --ar explicitly.
        # Every t2i job in the source did (sheet.py, stage1.py, char_still.py).
        defaults={
            "aspect_ratio": "match_input_image",
            "resolution": "2K",
            "output_format": "jpg",
        },
        keys={
            "first": None,
            "last": None,
            "refs": "image_input",   # array of data: URIs, up to several
            "audio": None,
            "seed": None,            # never used in any job here; unverified
            "ar": "aspect_ratio",
            "res": "resolution",
            "duration": None,
            "negative": None,
            "fmt": "output_format",
        },
        enums={},
    ),
}


# --------------------------------------------------------------------------
# auth + http
# --------------------------------------------------------------------------
def token() -> str:
    """Find REPLICATE_API_TOKEN: environment, then .env in cwd, beside this
    script, or one level up. The old rep.py only looked in video/.env."""
    tok = os.environ.get("REPLICATE_API_TOKEN")
    if tok:
        return tok.strip()
    for cand in (
        os.path.join(os.getcwd(), ".env"),
        os.path.join(HERE, ".env"),
        os.path.join(os.path.dirname(HERE), ".env"),
    ):
        if os.path.exists(cand):
            with open(cand) as f:
                for line in f:
                    if line.startswith("REPLICATE_API_TOKEN="):
                        return line.split("=", 1)[1].strip()
    sys.exit("REPLICATE_API_TOKEN not in the environment or any .env")


def call(url: str, tok: str, data=None):
    req = urllib.request.Request(url, method="POST" if data else "GET")
    req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("Content-Type", "application/json")
    body = json.dumps(data).encode() if data else None
    with urllib.request.urlopen(req, body) as r:
        return json.load(r)


def data_uri(path: str) -> str:
    """Replicate accepts inline data: URIs for file inputs, which avoids
    needing any upload step or public bucket. Images here are a few hundred
    KB, well inside the request limit."""
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    blob = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    return f"data:{mime};base64,{blob}"


# --------------------------------------------------------------------------
# submit / poll / download
# --------------------------------------------------------------------------
def submit(slug: str, payload: dict, tok: str, wait_credit_min: int = 0,
           rate_limit_attempts: int = 8, rate_limit_wait: int = 45):
    """POST the prediction, handling the only two HTTP codes that are worth
    surviving.

    402 = the Replicate account is out of credit; optionally sit and wait for a
    top-up instead of dying (--wait-credit).

    429 = rate limited. Veo does this hard and it is NOT fatal. The original
    batch runner (batch409.py) fired ten Veo jobs at once through a
    ThreadPoolExecutor and got throttled; the rewrite (batch409b.py) went
    sequential with 8 attempts, 45s apart, and that is what actually worked.
    Same numbers here. Do NOT parallelise Veo to get around this."""
    deadline = time.time() + wait_credit_min * 60
    rl = 0
    while True:
        try:
            return call(f"{API}/models/{slug}/predictions", tok, {"input": payload})
        except urllib.error.HTTPError as e:
            if e.code == 402 and time.time() < deadline:
                print("  402 out of credit, waiting 60s ...", file=sys.stderr)
                time.sleep(60)
                continue
            if e.code == 429 and rl < rate_limit_attempts:
                rl += 1
                print(f"  429 rate limited, wait {rate_limit_wait}s "
                      f"(attempt {rl}/{rate_limit_attempts})", file=sys.stderr)
                time.sleep(rate_limit_wait)
                continue
            detail = ""
            try:
                detail = e.read().decode()[:400]
            except Exception:
                pass
            sys.exit(f"HTTP {e.code} submitting {slug}: {detail}")


def poll(pred: dict, tok: str, every: int, timeout: int):
    """Replicate's status IS accurate - poll it normally and trust it.

    This is the opposite of Kling's task API, which is badly stale (a finished
    job reported QUEUING for eight minutes, a 58-second job reported RUNNING
    for fourteen). The 'never resubmit because it looks stuck' rule belongs to
    Kling, not here."""
    pid = pred["id"]
    print(f"prediction {pid} ...", file=sys.stderr)
    started = time.time()
    while pred["status"] not in ("succeeded", "failed", "canceled"):
        if time.time() - started > timeout:
            sys.exit(f"timed out after {timeout}s, prediction {pid} still "
                     f"{pred['status']} - check it on replicate.com")
        time.sleep(every)
        pred = call(f"{API}/predictions/{pid}", tok)
        print(f"  {pred['status']}", file=sys.stderr)
    return pred


def run(model_key: str, payload: dict, tok: str, timeout: int,
        wait_credit_min: int = 0, transient_retries: int = 2):
    """One generation, with the only retry policy that is actually correct.

    E004 'Service is temporarily unavailable' is transient - retry it.
    E005 'The input or output was flagged as sensitive' is a content refusal -
    NEVER retry it. Retrying E005 is how you burn money confirming a policy you
    already hit. If you get E005 from Seedance with an image input, the fix is
    routing (30.4), not another roll.

    The literal E004/E005 tokens come from the session narrative, not from any
    file in the repo, so match on the prose too - the codes may be renamed but
    the sentences are the model's own."""
    m = MODELS[model_key]
    attempt = 0
    while True:
        pred = submit(m["slug"], payload, tok, wait_credit_min)
        pred = poll(pred, tok, m["poll"], timeout)
        if pred["status"] == "succeeded":
            return pred
        err = str(pred.get("error") or "")
        low = err.lower()
        if "E005" in err or "flagged as sensitive" in low:
            sys.exit(
                "REFUSED (E005, content filter): " + err + "\n"
                "  Not transient. Do not retry. If this is Seedance with any "
                "human face as input, that is expected - see 30.4."
            )
        if ("E004" in err or "temporarily unavailable" in low) \
                and attempt < transient_retries:
            attempt += 1
            print(f"  E004 transient, retry {attempt}/{transient_retries} "
                  f"in 30s", file=sys.stderr)
            time.sleep(30)
            continue
        sys.exit(f"FAILED: {err or pred['status']}")


def outputs(pred: dict):
    o = pred.get("output")
    if o is None:
        return []
    return [o] if isinstance(o, str) else list(o)


def fetch(url: str, out: str):
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    # Download inside the same process that generated it. Replicate output
    # URLs are temporary; a URL pasted into a note is worth nothing later.
    urllib.request.urlretrieve(url, out)
    return out


def report(pred: dict):
    m = pred.get("metrics") or {}
    t = m.get("predict_time")
    if isinstance(t, (int, float)):
        print(f"time {t:.1f}s", file=sys.stderr)


# --------------------------------------------------------------------------
# post-processing
# --------------------------------------------------------------------------
def normalize_frame(path: str, w: int = 1080, h: int = 1920,
                    quality: int = 95) -> tuple:
    """Cover-fit to exactly w x h and overwrite in place.

    Every image model in this pipeline lies about output size, Nano Banana Pro
    worst of all (2752x1536 when asked for 2K 16:9). Anything that seeds a
    video generation or lands in a 9:16 cut must be an exact 1080x1920 or
    ffmpeg and the video models will each interpret the mismatch differently.

    The original scripts scaled to WIDTH and centre-cropped the height, which
    fails silently in two different ways on a 16:9 source. Unguarded
    (edit_first.py, edit_last2.py, sky_edits.py) PIL crop accepts the negative
    box and returns 1080x1920 LETTERBOXED with black bands - no exception, no
    warning, and the black goes into the next generation. Guarded with
    max()/min() (char_still.py, fix_c.py, regen_B.py, stills409.py, scenes.py)
    it returns a SHORT image - 2752x1536 becomes 1080x603 - which then breaks
    ffmpeg downstream. Cover-fit instead: scale so both axes meet or exceed the
    target, then crop. The result is always exactly w x h."""
    from PIL import Image

    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = max(w, round(sw * scale)), max(h, round(sh * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    im = im.crop((left, top, left + w, top + h))
    if path.lower().endswith(".png"):
        im.save(path)
    else:
        im.save(path, quality=quality)
    return (sw, sh), (w, h)


def write_preview(path: str, out: str, longest: int = 720):
    """One preview size for everything. Replaces the two ad-hoc sizes that were
    used interchangeably in the old scripts (half-size, and 360x640)."""
    from PIL import Image

    im = Image.open(path).convert("RGB")
    s = longest / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    im.save(out, quality=88)
    return out


def stats(path: str):
    """Contrast and saturation, the two numbers the Part B acceptance test
    turns on. Contrast is the mean of the per-channel standard deviations;
    saturation is the mean S of the HSV conversion. Measure, do not eyeball -
    a 22-point saturation drift is invisible side by side and obvious once the
    two references are cut together in a film."""
    from PIL import Image, ImageStat

    im = Image.open(path).convert("RGB")
    s = ImageStat.Stat(im)
    hsv = ImageStat.Stat(im.convert("HSV"))
    return {
        "size": im.size,
        "mean_rgb": [round(v, 1) for v in s.mean],
        "contrast": round(sum(s.stddev) / 3, 1),
        "saturation": round(hsv.mean[1], 1),
    }


def measure_sat(path: str) -> float:
    from PIL import Image, ImageStat
    return ImageStat.Stat(Image.open(path).convert("RGB").convert("HSV")).mean[1]


def match_saturation(src: str, out: str, target: float,
                     lo: float = 0.80, hi: float = 1.40, step: float = 0.01,
                     tol: float = 1.0, verbose: bool = False):
    """Find the ffmpeg eq=saturation multiplier that lands closest to a target
    saturation, then write it. This is the fix that resolved the Part B tone
    drift (30.9).

    ONE DENSE SWEEP, NOT A COARSE-THEN-REFINE SEARCH. This matters and it was
    got wrong once. Measured mean-saturation is NOT a monotonic function of the
    eq multiplier on these images - on gen/v2_sheets/herp_1.png the sequence
    runs 1.12 -> 105.1, 1.13 -> 103.3, 1.14 -> 101.3, 1.15 -> 112.0. It goes
    down, then jumps ten points. The images are dark (mean RGB around 47/44/28)
    and HSV S is (max-min)/max, so near-neutral dark pixels tip across rounding
    boundaries in clumps. Any hill-climbing or narrow-refine search locks onto
    that noise: a two-pass version of this function returned 1.183 (sat 107.0)
    on the exact job where 1.13 (sat 103.3) was correct, and reported success.
    Sweep the whole range at the resolution you intend to quote, take the global
    minimum, and say so out loud when the residual is bad.

    Probing goes through a rawvideo pipe rather than temp PNGs - identical
    pixels, about 7x faster, so a 61-point sweep costs ~11s instead of ~77s."""
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not on PATH")
    from PIL import Image, ImageStat

    w, h = Image.open(src).size

    def probe(v: float) -> float:
        p = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", src, "-vf",
             f"eq=saturation={v:.4f}", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-"],
            capture_output=True,
        )
        if p.returncode != 0:
            sys.exit("ffmpeg failed: " + p.stderr.decode()[:300])
        im = Image.frombytes("RGB", (w, h), p.stdout)
        return ImageStat.Stat(im.convert("HSV")).mean[1]

    n = int(round((hi - lo) / step)) + 1
    best = None
    for i in range(n):
        v = lo + i * step
        got = probe(v)
        d = abs(got - target)
        if verbose:
            print(f"  sat={v:.3f} -> {got:.1f} (target {target:.1f})",
                  file=sys.stderr)
        if best is None or d < best[2]:
            best = (v, got, d)
    v = best[0]
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", src, "-vf",
         f"eq=saturation={v:.4f}", "-y", out],
        check=True,
    )
    print(f"wrote {out}  eq=saturation={v:.3f}  sat={best[1]:.1f} "
          f"(target {target:.1f}, off by {best[2]:.1f})", file=sys.stderr)
    if best[2] > tol:
        print(f"  WARNING: closest match is {best[2]:.1f} off the target. "
              f"Widen --lo/--hi, or the candidate is too far out to rescue "
              f"and you should re-roll it instead.", file=sys.stderr)
    return v


# --------------------------------------------------------------------------
# payload construction
# --------------------------------------------------------------------------
def build_payload(model_key: str, prompt: str, opts: dict) -> dict:
    m = MODELS[model_key]
    if not m.get("schema_verified", True) and not m["keys"]:
        sys.exit(f"{model_key}: input schema unverified. Run "
                 f"`gen.py schema {model_key}` and fill in MODELS[...]['keys'].")
    keys, enums = m["keys"], m.get("enums", {})
    p = dict(m["defaults"])
    p["prompt"] = prompt

    def put(opt_name, value, as_uri=False, as_list=False):
        if value in (None, [], ()):
            return
        real = keys.get(opt_name)
        if real is None:
            sys.exit(f"{model_key} has no parameter for --{opt_name}")
        if as_list:
            p[real] = [data_uri(v) if as_uri else v for v in value]
        else:
            p[real] = data_uri(value) if as_uri else value

    put("first", opts.get("first"), as_uri=True)
    put("last", opts.get("last"), as_uri=True)
    put("refs", opts.get("refs"), as_uri=True, as_list=True)
    put("negative", opts.get("negative"))
    if opts.get("seed") is not None:
        put("seed", opts["seed"])
    if opts.get("ar"):
        put("ar", opts["ar"])
    if opts.get("res"):
        put("res", opts["res"])
    if opts.get("duration"):
        put("duration", opts["duration"])
    if opts.get("fmt"):
        put("fmt", opts["fmt"])
    if opts.get("no_audio") and keys.get("audio"):
        p[keys["audio"]] = False

    # Guard the one refusal that is a property of the model, not the prompt.
    if not m["accepts_face_input"] and (
        opts.get("first") or opts.get("last") or opts.get("refs")
    ):
        print("WARNING: " + m["slug"] + " refuses human faces in image inputs "
              "(E005). Plates, skies and landscapes are fine; a person is not.",
              file=sys.stderr)

    # match_input_image is meaningless with no input image, and that is the
    # easy way to burn a generation on a text-to-image call.
    if p.get(keys.get("ar")) == "match_input_image" and not opts.get("refs"):
        sys.exit(f"{model_key}: aspect_ratio=match_input_image but no --edit / "
                 f"refs image was given. Pass --ar 9:16 (or 16:9, or 1:1).")

    # WARN, do not exit. These enum lists are what the source was OBSERVED to
    # send, not a schema dump, so a legal-but-unlisted value must not be
    # blocked. Run `gen.py schema <model>` if you want the real list.
    for k, allowed in enums.items():
        if k in p and allowed and p[k] not in allowed:
            print(f"WARNING: {model_key}: {k}={p[k]!r} is outside the values "
                  f"this project has used ({allowed}). Sending anyway.",
                  file=sys.stderr)
    return p


def read_prompt(args) -> str:
    if getattr(args, "prompt_file", None):
        return pathlib.Path(args.prompt_file).read_text().strip()
    if getattr(args, "prompt", None):
        return args.prompt
    sys.exit("give --prompt or --prompt-file")


# --------------------------------------------------------------------------
# jobs
# --------------------------------------------------------------------------
def do_job(job: dict, tok: str) -> str:
    """One entry from a batch file, or one CLI invocation. Keys:
      model, prompt / prompt_file, out, role, preview,
      first, last, refs, seed, ar, res, duration, fmt, negative, no_audio
    """
    model_key = job["model"]
    if model_key not in MODELS:
        sys.exit(f"unknown model {model_key!r}; known: {sorted(MODELS)}")
    m = MODELS[model_key]
    prompt = job.get("prompt")
    if not prompt and job.get("prompt_file"):
        prompt = pathlib.Path(job["prompt_file"]).read_text().strip()
    if not prompt:
        sys.exit("job has no prompt")
    out = job["out"]
    payload = build_payload(model_key, prompt, job)
    timeout = int(job.get("timeout") or (1800 if m["kind"] == "video" else 600))
    pred = run(model_key, payload, tok, timeout,
               wait_credit_min=int(job.get("wait_credit") or 0))
    urls = outputs(pred)
    if not urls:
        sys.exit("succeeded but returned no output")
    for u in urls[1:]:
        print(u)                       # extra variants, if imageCount > 1
    fetch(urls[0], out)
    print(f"saved {out}", file=sys.stderr)

    role = job.get("role", "frame" if m["kind"] == "image" else None)
    if m["kind"] == "image":
        if role == "frame":
            src, dst = normalize_frame(
                out, int(job.get("w", 1080)), int(job.get("h", 1920)))
            print(f"  normalised {src} -> {dst}", file=sys.stderr)
        elif role == "sheet":
            # Deliberate. A character sheet or location sheet is a REFERENCE,
            # not a frame. Cropping a 16:9 triptych to 9:16 amputates the outer
            # panels, which is the whole document.
            print(f"  role=sheet, size left native "
                  f"{stats(out)['size']}", file=sys.stderr)
        else:
            print(f"  role={role}, no resize", file=sys.stderr)
    if job.get("preview"):
        pv = job["preview"] if isinstance(job["preview"], str) else \
            os.path.join(os.path.dirname(out) or ".", "qa",
                         os.path.splitext(os.path.basename(out))[0] + ".png")
        write_preview(out, pv)
        print(f"  preview {pv}", file=sys.stderr)
    report(pred)
    return out


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def add_common(sp):
    sp.add_argument("--model", required=True, choices=sorted(MODELS))
    sp.add_argument("--prompt")
    sp.add_argument("--prompt-file")
    sp.add_argument("--out", required=True)
    sp.add_argument("--seed", type=int)
    sp.add_argument("--ar", help="aspect ratio, e.g. 9:16")
    sp.add_argument("--res", help="resolution, e.g. 1080p or 2K")
    sp.add_argument("--wait-credit", type=int, default=0,
                    help="minutes to sit on HTTP 402 waiting for a top-up")
    sp.add_argument("--timeout", type=int)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("video", help="one video generation")
    add_common(v)
    v.add_argument("--first", help="first-frame image (local path)")
    v.add_argument("--last", help="last-frame image (local path)")
    v.add_argument("--ref", action="append", default=[],
                   help="reference image, repeatable")
    v.add_argument("--duration", type=int)
    v.add_argument("--negative")
    v.add_argument("--no-audio", action="store_true")

    i = sub.add_parser("image", help="one image generation or edit")
    add_common(i)
    i.add_argument("--edit", action="append", default=[],
                   help="reference/source image, repeatable (multi-reference)")
    i.add_argument("--fmt", default="jpg")
    i.add_argument("--role", choices=["frame", "sheet", "none"], default="frame",
                   help="frame = normalise to 1080x1920; sheet = leave native")
    i.add_argument("--preview", nargs="?", const=True, default=False)
    i.add_argument("--w", type=int, default=1080)
    i.add_argument("--h", type=int, default=1920)

    b = sub.add_parser("batch", help="run a JSON list of jobs sequentially")
    b.add_argument("jobs_json")
    b.add_argument("--redo-existing", action="store_true",
                   help="regenerate jobs whose out file already exists "
                        "(default: skip them, so a rerun is free)")

    r = sub.add_parser("raw", help="rep.py behaviour: slug + literal JSON")
    r.add_argument("slug")
    r.add_argument("payload")
    r.add_argument("outfile", nargs="?")

    n = sub.add_parser("normalize", help="cover-fit a file, no API call")
    n.add_argument("path")
    n.add_argument("--w", type=int, default=1080)
    n.add_argument("--h", type=int, default=1920)

    t = sub.add_parser("tone", help="contrast/saturation drift table")
    t.add_argument("reference")
    t.add_argument("candidates", nargs="+")

    ms = sub.add_parser("match-sat", help="ffmpeg saturation sweep to a target")
    ms.add_argument("src")
    ms.add_argument("out")
    ms.add_argument("--target-sat", type=float, required=True)
    ms.add_argument("--lo", type=float, default=0.80)
    ms.add_argument("--hi", type=float, default=1.40)
    ms.add_argument("--step", type=float, default=0.01)
    ms.add_argument("--verbose", action="store_true")

    sc = sub.add_parser("schema", help="dump a model's Input properties")
    sc.add_argument("model")

    a = ap.parse_args()

    if a.cmd == "normalize":
        print(normalize_frame(a.path, a.w, a.h))
        return

    if a.cmd == "tone":
        ref = stats(a.reference)
        print(f"TARGET {os.path.basename(a.reference)}: "
              f"contrast {ref['contrast']}  sat {ref['saturation']}  "
              f"{ref['size']}")
        best = None
        for c in a.candidates:
            s = stats(c)
            drift = (abs(s["contrast"] - ref["contrast"]) / max(ref["contrast"], 1e-6)
                     + abs(s["saturation"] - ref["saturation"]) / max(ref["saturation"], 1e-6))
            print(f"{os.path.basename(c):28s} contrast {s['contrast']:6.1f} "
                  f"({s['contrast']-ref['contrast']:+6.1f})  "
                  f"sat {s['saturation']:6.1f} "
                  f"({s['saturation']-ref['saturation']:+6.1f})  "
                  f"drift {drift:.3f}  {s['size']}")
            if best is None or drift < best[1]:
                best = (c, drift)
        print("CLOSEST:", best[0])
        return

    if a.cmd == "match-sat":
        match_saturation(a.src, a.out, a.target_sat, lo=a.lo, hi=a.hi,
                         step=a.step, verbose=a.verbose)
        return

    tok = token()

    if a.cmd == "schema":
        slug = MODELS[a.model]["slug"] if a.model in MODELS else a.model
        d = call(f"{API}/models/{slug}", tok)
        c = (d.get("latest_version", {}).get("openapi_schema", {})
             .get("components", {}).get("schemas", {}))
        props = c.get("Input", {}).get("properties", {})
        print("DESC:", (d.get("description") or "")[:200])
        for k, val in props.items():
            print(f"  {k}: {val.get('type')} default={val.get('default')} "
                  f"{(val.get('description') or '')[:70]}")
        for name in ("resolution", "aspect_ratio", "duration", "output_format"):
            if c.get(name, {}).get("enum"):
                print(f"{name} enum: {c[name]['enum']}")
        return

    if a.cmd == "raw":
        # rep.py, unchanged: no registry, no normalisation, no retry policy.
        payload = json.loads(a.payload)
        pred = submit(a.slug, payload, tok)
        pred = poll(pred, tok, 3, 1800)
        if pred["status"] != "succeeded":
            sys.exit(f"FAILED: {pred.get('error')}")
        urls = outputs(pred)
        for u in urls:
            print(u)
        if a.outfile:
            fetch(urls[0], a.outfile)
            print(f"saved {a.outfile}", file=sys.stderr)
        report(pred)
        return

    if a.cmd == "batch":
        # Two behaviours inherited from the originals, both of which cost money
        # to relearn. batch409b.py skipped any job whose output already existed,
        # so an interrupted batch could be rerun for free. stills409.py caught a
        # per-shot failure and CONTINUED, because aborting the whole batch on
        # one refused shot throws away the four that worked.
        jobs = json.loads(pathlib.Path(a.jobs_json).read_text())
        failed = []
        for n_, job in enumerate(jobs, 1):
            out = job.get("out")
            print(f"=== [{n_}/{len(jobs)}] {out}", file=sys.stderr)
            if out and os.path.exists(out) and not a.redo_existing:
                print("  exists, skip (pass --redo-existing to force)",
                      file=sys.stderr)
                continue
            try:
                do_job(job, tok)
            except SystemExit as e:
                print(f"  FAILED {out}: {e}", file=sys.stderr)
                failed.append((out, str(e)))
        if failed:
            print(f"\n{len(failed)}/{len(jobs)} failed:", file=sys.stderr)
            for out, msg in failed:
                print(f"  {out}: {msg}", file=sys.stderr)
            sys.exit(1)
        return

    job = dict(
        model=a.model, prompt=a.prompt, prompt_file=a.prompt_file, out=a.out,
        seed=a.seed, ar=a.ar, res=a.res, wait_credit=a.wait_credit,
        timeout=a.timeout,
    )
    if a.cmd == "video":
        job.update(first=a.first, last=a.last, refs=a.ref,
                   duration=a.duration, negative=a.negative,
                   no_audio=a.no_audio, role=None)
    else:
        job.update(refs=a.edit, fmt=a.fmt,
                   role=(None if a.role == "none" else a.role),
                   preview=a.preview, w=a.w, h=a.h)
    do_job(job, tok)


if __name__ == "__main__":
    main()
```

**Dependency note.** There is no `requirements.txt` anywhere in the source repo
— the environment is stood up by the explicit `pip install` line in Part 5,
which already pins `pillow==12.1.1`. This runner needs `pillow` (all
post-processing) and `ffmpeg` on PATH (only for `match-sat`). Nothing to add;
just do not assume a requirements file exists, because it does not.

---

## 30.3 — Recipes

All paths relative to the pipeline root. Output goes to `gen/`, which is
gitignored (it is hundreds of megabytes of generated media, and it is the only
copy — see the backup note in Part 0).

**A 9-second aerial, text to video, native audio.** The whole 405-408 wave was
this one call with a different prompt and seed each time.

```bash
python3 scripts/gen.py video --model seedance \
  --prompt-file prompts/aerial-b.txt \
  --ar 9:16 --res 1080p --duration 9 --seed 21 \
  --out gen/lands_b.mp4
```

The prompt text for the four shipped 405-408 aerials is **not in the repo** —
those scripts were not kept (see open questions). What is on disk, complete and
verbatim, is the sibling text-to-video job that produced `gen/sky_giant2.mp4`.
Copy its *shape*, not its subject: the movement is described as a constraint,
the camera artefacts are demanded explicitly, and the last line is an `AUDIO:`
block, which Seedance honours.

```
Shaky handheld phone video shot through a scratched airliner window in bad
weather, vertical, filmed by a frightened passenger. Heavy overcast storm
light. EVERYTHING IS ONE FLAT DESATURATED BLUE-GREY WASH — sky, cloud and
subject all the same narrow range of tone, almost monochrome, low contrast, low
dynamic range, washed out. Thick turbulent cloud fills the frame and streams
past the window fast. Far out in the murk stands something impossibly enormous,
mountain-scale, only a BACKLIT SILHOUETTE against the brighter cloud behind it
— no surface, no material, no detail, no face, just a dark shape. Torn cloud
constantly drifts ACROSS AND IN FRONT of it, cutting it into fragments, so it
is never fully visible at once and its edges are always broken by weather. The
lower part of it is far more lost in haze than the upper part. It does not move
at all. Only the cloud and the aircraft move. PHONE CAMERA ARTEFACTS ARE
ESSENTIAL: heavy compression blocking, blown-out highlights where cloud catches
light, motion blur, autofocus hunting, grain, a smear of glare and condensation
on the window glass. It should look like genuinely bad amateur footage, not a
clean render. No cuts, one continuous shot, no zoom, no cinematic camera move.
AUDIO: loud muffled cabin roar and turbulence rumble. A frightened passenger
close to the microphone says quietly: wait, do you see that?
```

That job ran at `"aspect_ratio":"9:16","resolution":"720p","duration":9,
"generate_audio":true,"seed":31337`. The shipped aerials are the same call at
`1080p` — `ffprobe` reports `gen/lands_b.mp4` as 1080x1920, 24fps, 9.04s.

**First-frame to last-frame interpolation.** This is how you get a specific
piece of motion rather than whatever the model feels like: generate the two end
states as images, then let Seedance interpolate. Both stills must be normalised
to the same size first, or the model gets a 1080x1920 first frame and a
1536x2752 last frame and the result drifts.

```bash
python3 scripts/gen.py image --model nano-banana-pro \
  --prompt-file prompts/atoll-plate.txt --ar 9:16 --res 2K \
  --role frame --out gen/creature_first.jpg

python3 scripts/gen.py image --model nano-banana-pro \
  --prompt-file prompts/atoll-whale.txt --edit gen/creature_first.jpg \
  --ar match_input_image --role frame --out gen/creature_last.jpg

python3 scripts/gen.py video --model seedance \
  --prompt-file prompts/atoll-motion.txt \
  --first gen/creature_first.jpg --last gen/creature_last.jpg \
  --ar 9:16 --res 720p --duration 9 --seed 404 \
  --out gen/creature_v4.mp4
```

**A surgical edit** — change exactly one thing and freeze everything else. The
prompt does the work; the model does what you literally ask, so ask literally.
This is the complete, verbatim prompt that produced `gen/creature_last.jpg`:

```
Keep this photograph exactly as it is — identical aircraft engine, window
frame, atoll, reef, clouds, colour and lighting. Change one thing only: in the
open deep blue water in the middle of the frame, add an enormous marine
creature swimming just beneath the surface. It reads as a colossal whale-like
animal: a long dark body, two clear pectoral flippers, and a wide tail fluke,
outline softened and blued by the water above it. It must be unmistakably an
animal and not a reef or a seagrass patch, but it stays under the surface and
does not breach. Photorealistic, matching the existing water colour and light.
```

Note the shape: **freeze list first** (name every element that must not move),
then `Change one thing only:`, then the change, then a negative stated as a
positive ("it must be unmistakably an animal and not a reef"), then the
grade-matching clause. Every surgical edit in this project follows it.

**A character sheet** (`--role sheet`, never normalised):

```bash
python3 scripts/gen.py image --model nano-banana-pro \
  --prompt-file prompts/sheet-boss.txt --ar 16:9 --res 2K \
  --role sheet --preview --out gen/sheet_boss.jpg
```

**A batch.** This replaces writing another throwaway script:

Prompts below are the real ones from the five-shot stage-3 run, complete:

```json
[
  {"model":"nano-banana-pro","out":"gen/c409_A.jpg","role":"frame","ar":"9:16","res":"2K",
   "refs":["gen/c409_plate.jpg","gen/c409_woman.jpg"],
   "prompt":"Use the provided kitchen photo as the exact location — same table, window, curtains, laptop, mug, sandwich plate, notebook, chair, doorway to the hallway, kettle, plant, tea towel. Keep its lighting and palette. The woman from the reference sheet sits at the table in profile, typing on the laptop, headphones round her neck, mid-bite of the sandwich in her left hand. Calm ordinary afternoon. Wide shot, eye level, whole room visible, she is small in frame. Modern A24 indie drama look: 35mm film, natural window light from camera-left, warm but desaturated, muted tones, lifted blacks, low contrast, visible grain, slight halation, real skin texture, unglamorous domestic realism, completely photorealistic."},
  {"model":"nano-banana-pro","out":"gen/c409_D.jpg","role":"frame","ar":"9:16","res":"2K",
   "refs":["gen/c409_plate.jpg","gen/c409_woman.jpg"],
   "prompt":"Use the provided kitchen photo as the exact location — same table, window, curtains, laptop, mug, sandwich plate, notebook, chair, doorway to the hallway, kettle, plant, tea towel. Keep its lighting and palette. Close medium shot of the woman from the reference sheet pressed back against the window side of the table, both hands half-raised, caught mid-plea, frightened, talking fast, eyes on someone off-frame right. The laptop and mug in the foreground. Modern A24 indie drama look: 35mm film, natural window light from camera-left, warm but desaturated, muted tones, lifted blacks, low contrast, visible grain, slight halation, real skin texture, unglamorous domestic realism, completely photorealistic."}
]
```

The location-anchor paragraph and the tone paragraph are byte-identical across
every shot in the batch. That is deliberate: they were single constants in the
original script and any drift between shots shows up as a continuity error.

```bash
python3 scripts/gen.py batch jobs/stage3.json
```

---

## 30.4 — Seedance refuses human face inputs. All of them.

This is the single hardest constraint in the video layer and it is not
documented anywhere on the model page.

Three separate jobs were submitted with a human face reaching Seedance by three
different routes. All three failed identically:

```
FAILED: Prediction failed: Async prediction failed: ModelError:
The input or output was flagged as sensitive. Please try again with different
inputs. (E005)
```

- `image` (image-to-video from a portrait still) — refused. `char_vid.py`,
  output path `gen/char_test.mp4`.
- `reference_images` (the documented character-consistency slot) — refused.
  `ref_test.py`, output path `gen/char_ref.mp4`.
- A white-background **character sheet**, which is nothing but face panels —
  refused. `sheet_test.py`, output path `gen/char_sheet_vid.mp4`. (Its success
  message says "saved gen/char_ref.mp4" — a copy-paste bug in the original
  script, not a second attempt at the same file.)

The identical prompt with **no image input at all** succeeded on the first roll
and is on disk as `gen/char_t2v.mp4` (720x1280, 9.04s, with audio). **None of
`gen/char_test.mp4`, `gen/char_ref.mp4` or `gen/char_sheet_vid.mp4` exists** —
that absence is the evidence, three for three.

So: **Seedance can generate people. It cannot be shown one.** Text-to-video with
a person described in words is fine and looks good. The moment you need *that*
person, you are on Veo (face plus native audio plus lip sync) or on Kling
(faces plus props, and on Kling 3.0, native audio).

E005 is not a transient. Do not retry it, do not reword around it, do not spend
another roll confirming it. The runner exits hard on E005 for this reason.

Landscape, sky, water and architecture inputs pass fine — the whole 405-408
aerial wave and the creature/sky sequences fed Seedance first-frame and
last-frame images with no trouble. It is faces specifically.

---

## 30.5 — Nano Banana Pro returns the wrong size. Always normalise.

Measured sizes, read off the files this model actually wrote, all from jobs that
asked for `"resolution": "2K"`:

| Requested aspect | Returned | Evidence on disk |
|---|---|---|
| `16:9` | **2752 x 1536** | `gen/c409_man.jpg`, `gen/c409_woman.jpg`, `gen/char_sheet.jpg`, `gen/sheet_man.jpg`, `gen/sheet_woman.jpg` |
| `9:16` | **1536 x 2752** | `gen/c409_plate.jpg` |
| `1:1` | **2048 x 2048** | `gen/c409_locsheet.jpg` |
| (an early job, request params not recorded) | **768 x 1344** | `gen/still_a.png`, `gen/still_b.png` |

None of those is 1080x1920. One session produced a first frame at 1080x1920 and
a last frame at 1536x2752 and fed both to a video model, which is exactly the
kind of quiet mismatch that produces "it looks a bit off" and no error anywhere.

**Rule: every generated still that will seed a video generation, or be
composited into a 9:16 cut, goes through the normalise step to exactly
1080x1920.** `--role frame` does it automatically. The runner prints the before
and after so it is visible in the log.

**Exception, and it is deliberate: sheets are not frames.** A 16:9 triptych
character sheet or a 1:1 ABCD location sheet must keep its native size and
ratio. Centre-cropping a triptych to 9:16 removes the outer two panels, which
is the entire document. Use `--role sheet`.

The Kling-side image models have their own fixed sizes, and they are different
again. Measured across `video/gen/v2_sheets/` (the two families are trivially
separable: OpenAI's outputs carry a C2PA `caBX` PNG chunk, Kling's carry a
`tEXt` `AIGC` chunk):

| Model | 16:9 | 9:16 | 1:1 |
|---|---|---|---|
| `gpt-image-2` / `gpt-image2` | 2048 x 1152 | 1152 x 2048 | 2048 x 2048 |
| `kling-image-v3_0_omni` | 2720 x 1536 | 1536 x 2720 | 2048 x 2048 |

Same rule applies to anything you pull down from there. Note that the two
models agree at 1:1 and nowhere else — do not use a 1:1 sample to decide which
model produced a file.

---

## 30.6 — Gemini image models reject identity-matching prompts

Part B of the character-sheet process is "take this approved portrait and give
me the same person in true side profile". On `gemini-3.1-flash-image`
(Nano Banana 2) that job **failed in about five seconds with no error text at
all**. Not a timeout, not a malformed input, not a quota message — a silent
policy rejection, almost certainly a likeness filter tripped by the prompt
language the task requires: *"the SAME man, identical person, same bone
structure, same jawline"* applied to a supplied photograph.

`kling-image-v3_0_omni` ran the identical intent, with the same strong
consistency language, without complaint.

The failed job appears to have been refunded — the credit balance did not move.
That is a small mercy and not a reason to keep trying.

> **Rule: any reference-consistency or identity-matching work goes to Kling's
> own image models.** Gemini/Nano Banana is for work where nobody has to be the
> same person as before.

Note the model-name trap on the Kling side: the text-to-image model is
`gpt-image-2` and the image-to-image model is `gpt-image2`, without the second
hyphen. They are different endpoints with different canonical names. Both are
correct in their own context; using the t2i name on an i2i call will fail.

---

## 30.7 — Error codes and what to do about each

| Symptom | Meaning | Action |
|---|---|---|
| `ModelError ... flagged as sensitive (E005)` | Content refusal. Face into Seedance, or genuinely disallowed content. | **Never retry.** Re-route (30.4) or change the shot. |
| `Service is temporarily unavailable (E004)` | Transient. Hit once in a batch of seven otherwise-identical still jobs. | Retry after 30s. The runner does this twice automatically. |
| HTTP `402` on submit | Replicate account out of credit. | Top up. `--wait-credit N` will sit and poll for N minutes if a top-up is already in flight. |
| HTTP `429` (Veo especially) | Rate limit. | Submit sequentially, 45s backoff. Do not parallelise Veo. |
| A Gemini image job that dies in ~5s with no error text | Likeness policy. | Re-route to a Kling image model (30.6). |
| A job that "looks stuck" on **Replicate** | Almost certainly is stuck, or is just slow. | Replicate's status is accurate. Poll normally. |
| A job that "looks stuck" on **Kling** | Its task API is badly stale: a finished job reported QUEUING for 8 minutes, a 58-second job reported RUNNING for 14, and `finishTime` is set early and means nothing until status is COMPLETED. Credit balances are cached too. | Poll on 5-minute-plus intervals. **Never switch models or resubmit because a job looks stuck.** A model swap was nearly wasted on a phantom hang. |

**Download output immediately, in the same process that generated it.** Kling's
result URLs expire 24 hours after finish. Replicate's are also temporary. The
runner always fetches before it exits; do not adopt a habit of pasting URLs into
notes for later.

---

## 30.8 — Money

- **Replicate** (`<the team's Replicate account>`): auto-reload is on, on the team card, and
  about **$25** of credit was left at the last count. One heavy generation day
  measured about **$111**. There is no per-model price recorded in the source
  for `nano-banana-pro`, `seedance-2.0`, `veo-3.1` or `kling-v2.5-turbo-pro` —
  see open questions. Video resolution is the biggest lever, and the split is
  visible in the files: every iteration clip is 720p (`gen/creature_v4.mp4`,
  `gen/sky_giant3.mp4`, `gen/char_t2v.mp4` are all 720x1280) and every shipped
  aerial is 1080p (`gen/lands_b.mp4` is 1080x1920).
- **Kling**: 8000 membership credits granted, expiring one month later.
  **12 credits per second of output** on every v3_0 tier — 15s = 180, 9s = 108,
  8s = 96. Duration is the only lever that moved the price in testing, so
  splitting a long generation into shorter ones costs nothing and produces
  better dialogue. Images: 70 / 30 / 4 credits per 2-image 2k job for
  gpt-image / gemini-flash / kling-omni respectively.
- The API token for Replicate lives in `.env` next to the pipeline. **Rotate it
  if it has ever appeared in a chat transcript**; read it in with `read -s`
  rather than echoing it.

---

## 30.9 — The character-sheet process: Part A, Part B, Part C

This is the stage that decides whether the finished film reads as a film or as
AI. The first attempt at ad 409 skipped it — references were assembled ad hoc
and then synthetic-looking faces were fought with prompt wording — and the whole
run was thrown away. Do not skip it.

The three parts build one reference per character. Every downstream still and
every video generation of that character points at it.

### Part A — the front portrait

**Model: `gpt-image-2`. 16:9, 2k, quality high. Generate 2-3 variants and pick.**

Widescreen because film and TV training data is widescreen, so a portrait
generated at 16:9 reads as a production still rather than a headshot. GPT Image 2
because it is the model that actually holds an analog grade — the alternatives
apply their own colour interpretation and drift off the muted palette, and
whatever tone this image has, everything downstream inherits.

Light it for the **actual scene**, not on a white studio background. The
abandoned first run used flat white studio light with burned-in text labels, and
that is a large part of why the video read as synthetic.

The prompt skeleton that produced the approved portrait:

```
PHOTOGRAPH, not an illustration, not a render, not CGI. A real photographic
film still of a real man.

Visual tone: Modern A24 indie drama. Shot on 35mm film, single warm practical
light source from camera-left, deep unlit shadow on the shadow side of the
face, warm highlights, lifted blacks, low contrast, muted desaturated palette
of greens and ochres, visible film grain, slight halation around the light
source, naturalistic and unglamorous.

Subject: a white American man in his mid-40s, photographed front-facing, head
and shoulders, looking just past the camera. [wardrobe, hair, skin, sweat,
stubble - be specific, this is casting]
```

`PHOTOGRAPH, not an illustration` is load-bearing: the image models will return
drawings for male subjects otherwise. It was needed on Replicate's
`nano-banana-pro` too, where a first sheet came back as illustration and had to
be re-rolled with an explicit *"looks like a casting agency headshot sheet,
completely photorealistic"*.

**Then measure it and write the numbers down.** The approved BOSS portrait was
contrast **37.1**, saturation **70.9**. Those two numbers are the contract for
everything that follows.

```bash
python3 scripts/gen.py tone gen/v2_sheets/boss_portraitA.png
```

### Part B — the true side profile

**Model: `kling-image-v3_0_omni`, from the approved Part A image. Not Gemini
(30.6). Generate 3 variants.**

The prompt has to demand identity hard — *"Take the man in 图片1 and photograph
him from a TRUE SIDE PROFILE, a full 90-degree side view of his head, facing
frame-left. Same face, bone structure, nose, jawline, age, hair, stubble and
wardrobe as 图片1."* On Kling, reference images are addressed in the prompt as
`图片1`..`图片7`, matching the input names `image_1`..`image_7`. Use those tokens
literally; "the first reference image" in English is not the documented handle.

**The acceptance test is not "does it look good". It is "does the tone match
Part A".** If grain, contrast or saturation drift between the front and side
views, the Part C triptych is internally inconsistent, and every video
generation built on that sheet inherits the inconsistency.

### The saturation-matching failure, in full

This is the part that cost the most time, so here is exactly what happened.

Two Part B candidates came back. **Both held the face perfectly.** Neither
matched the portrait's tone:

| Image | Contrast | Saturation |
|---|---|---|
| `boss_portraitA.png` (Part A, target) | 37.1 | **70.9** |
| `boss_profileA.png` | — | **48.9** (drained, -22) |
| `boss_profileB.png` | — | **101.5** (oversaturated, +31) |

(Contrast 37.1 / saturation 70.9 re-measured against the file itself, and they
are also written down in `video/gen/v2_sheets/README.md`. The two profile
candidates are recorded there too but are no longer on disk — only the
corrected final survives.)

Side by side they looked fine. The numbers say one is a third less saturated
than the target and the other is 43% more. Cut together in a film, that reads as
two different grades.

A re-roll with the colour explicitly pinned — a prompt built around
*"COLOUR MUST MATCH 图片1 EXACTLY. Same colour intensity, same muted desaturated
palette. The red flush on the cheek must be the SAME strength as in 图片1, do
not intensify it, do not make the skin redder, and equally do not drain the
colour out"* — produced more candidates. The closest still missed. (The exact
wording of that re-roll prompt is not in the repo; it is paraphrased from the
session narrative. The *outcome* is on disk — see below.)

**Prompt-level colour pinning does not work.** The fix was to stop asking and
correct it numerically: pick the candidate with the smallest combined drift,
then sweep ffmpeg's `eq=saturation` until the measured saturation lands on the
target.

```bash
# 1. which candidate is closest?
python3 scripts/gen.py tone gen/v2_sheets/HER_PORTRAIT_FINAL.png \
   gen/v2_sheets/herp_1.png

# 2. correct it
python3 scripts/gen.py match-sat gen/v2_sheets/herp_1.png \
   gen/v2_sheets/HER_PROFILE_FINAL.png --target-sat 103.5
```

The drift metric the runner prints is
`|Δcontrast|/contrast_ref + |Δsaturation|/saturation_ref`, which weights both
axes proportionally rather than letting the larger absolute number dominate.

**This is not a reconstruction — the SOLO/HER correction is reproducible from
the files right now, and the runner above reproduces it.** Running that exact
`match-sat` command against `herp_1.png` sweeps 0.80–1.40, lands on
`eq=saturation=1.130`, and writes a file byte-identical to the shipped
`HER_PROFILE_FINAL.png` (md5 `f70fdd533baf9855f5d03aec27ab4f5f`, both 5,465,228
bytes) in about 11 seconds. The numbers: `herp_1.png` measured saturation
**80.7**, target (`HER_PORTRAIT_FINAL.png`) **103.5**, result **103.3**.
A multiplier of **1.13**.

Read `match_saturation`'s docstring before you touch it. The objective is not
monotonic and a smarter-looking search finds a worse answer.

BOSS went through the same correction — `boss_profile_FINAL.png` carries the
ffmpeg re-encode signature and measures saturation **71.7** against the
portrait's 70.9 target — but its source candidate is no longer on disk, so the
exact multiplier for BOSS cannot be recovered. Do not quote one.

The correction is small either way. That is the point — the drift is small
enough to be invisible by eye and large enough to matter.

**A second-order lesson from the same episode:** the two characters do not sit
in the same range. Measured: BOSS's approved portrait is saturation 70.9,
SOLO/HER's is 103.5, a 33-point gap between the two leads' own targets, and
SOLO's raw Part B candidate came in at 80.7. The two characters share every
frame of the film, so **decide the relationship between the two characters'
grades deliberately** rather than letting each one drift to its own Part A in
isolation. Set the second character's target with the first one's numbers in
view.

### Part C — the triptych compile

**Model: `gpt-image-2` / `gpt-image2`. 1:1, T-cut layout. This one is not
negotiable.**

Compile the approved front portrait and the tone-matched side profile into one
sheet. Nano Banana produces a technically clean compile and then applies its own
colour interpretation, shifting the tone off the muted A24 palette — and since
this sheet is the reference for every base image and every video generation of
the character, that shift propagates into the entire film. The compile is
precisely where the grade must survive, which is why it gets the expensive
model.

The prompt carries an explicit instruction **not** to relight or clean up. This
is the skeleton reconstructed from the two compiles that were run — the opening
line and the layout are verbatim, the panel bodies are paraphrased, and the last
two lines are the guide's instruction as recorded:

```
Compile 3 images into one image. Triptych, T-cut layout, on a clean pure white
studio backdrop.

Top left panel  - white studio backdrop - front face close up of the [subject]
                  from the FIRST provided image.
Top right panel - white studio backdrop - side profile from the SECOND provided
                  image.
Bottom panel    - full body, [wardrobe described in words].

Do not change the face lighting. Do not remove the graininess.
```

Do not skip that last line. Preserving the lighting and grain is the entire
reason the two source images were built to a measured tone match.

### What the sheets are then used for

- Every stage-3 still that shows the character's face passes the sheet as a
  reference image.
- **Nothing else does.** See 30.10.

---

## 30.10 — Face sheet ONLY when the face is visible

Learned at a cost of 18 credits and three failed rolls, and it generalises to
every model.

The shot was setup D: over-the-hip, from **behind** the character, in a dark
hallway. The character sheet was passed as a reference, because that is what you
do. The sheet is almost entirely face panels. The prompt demanded a framing
where the face is invisible.

The model resolves that contradiction by **rendering the face somewhere anyway**:

- Two rolls produced **a duplicate second man** — him in the foreground from
  behind, and him again mid-room with the bat.
- One roll produced **a literal shadow-figure on the wall** with his face on it.

Three Kling image rolls failed this way. (The source logs it as "three Kling
rolls" without naming the model; `kling-image-v3_0_omni` was the default for
stills at the time, so that is the likely one, but it is an inference.)
Re-prompting did not fix it, because the contradiction was in the inputs, not
the wording.

**The fix that worked first try:** drop the character sheet entirely for
from-behind framings. Identity is carried by wardrobe description alone —
*"broad heavy build, navy suit jacket, short dark disordered hair on the back of
his head, face completely invisible. THERE IS ONLY THIS ONE MAN IN THE IMAGE —
no other figure, no shadow man."* — and switch to `gpt-image2` for precision
instruction-following.

> **Rule: pass the face sheet when the face is visible in the shot. Otherwise
> do not pass it at all.**

The same logic applies to the no-face detail shot (setup E, the laptop): no
faces in frame, so no sheets, and the cheap Kling model is fine.

**The neighbouring rule, learned the same way:** do not overload a generation
with references. A Kling Omni video take that was handed the ABCD location sheet
along with everything else rendered the **location sheet as a shot** — the final
0.9 seconds became a top-down drone view of a woman lifting a chair over her
head. Wrong character, wrong angle, wrong scene. For single-character work, use
the non-omni `kling-video-v3_0` with the scene still as `first_image`. That
fixed the artefact at the root **and rendered in half the time** — 6 minutes
against 13. Omni is artefact-prone specifically when it is overloaded with
references; it is not a general upgrade.

---

## 30.11 — How sheets and stills feed a shoot

The script for ad 409 (`script409.md`) is the worked example. Its structure is
the point:

**Twelve shots, five camera setups.** A (low angle on BOSS, bat overhead) is
used in shots 4, 6 and 8. B (tight close-up on SOLO) in 5, 7 and 9. C (locked
wide) in 3, 10 and 12. D (over-the-hip from behind) in 1 and 2. E (laptop
detail) in 11. Reusing A and B three times each **is** the technique — the
dynamism comes from alternation, not from novelty. Five stills, twelve shots.

So the stage-3 deliverable is not twelve images. It is:

1. **One base image** — the foundational peopled still, generated with both
   character sheets as references, on `gpt-image2`. It doubles as setup C.
2. **One wide**, derived from the base image, pulled far enough back to expose
   the whole room. Cheap model, it is spatial reference not a hero frame.
3. **One ABCD location sheet**, generated **from the peopled wide** — never
   from scratch, because models render empty rooms unconvincingly. This is where
   you settle the questions that would otherwise contradict across twelve shots:
   which side the door is on, which way it is hinged, where the window is.
4. **One start frame per setup**, each generated from the base image (for look)
   plus the location sheet (for geometry) plus the character sheet **only if the
   face is visible**.

Then the model routing per shot, straight off the script:

- **Shots 1, 2, 3, 10 → Seedance.** The approach, the door break, the reveal
  wide, the stop. Action and wides. No supplied faces in 1 and 2 (from behind),
  which is also what makes them legal for Seedance.
- **Shots 4-9, 12 → Kling.** Faces, dialogue, emotion.
- **Shot 11 → an image, animated lightly.**

Version 1 put the door break on Kling. That was the wrong tool for the only real
action beat in the film.

Three more things this stage taught, all cheap to remember and expensive to
rediscover:

- **Study the reference frame by frame before building any sequence still.**
  A 0.1-second-step ffmpeg extraction settles in minutes what prose arguments
  cannot. Three physics errors were caught this way: a bat swung at a door that
  a shoulder actually breaks, a "sequence" of stills with no forward
  progression, and a raised bat carried while walking.
- **Some concepts cannot be negatively prompted away.** "Broken white door
  debris" rendered as shattered china or glass on five separate attempts no
  matter how it was negative-prompted. The fix was to remove the concept from
  the prompt and delete the shards afterwards with `kling-image-o1` — a
  surgical, ~2-credit edit that worked first try. Reach for the edit model
  sooner.
- **Never trust model-rendered UI text.** The laptop screen in setup E is
  generated deliberately bright and illegible — *"a clean white webpage layout
  softly out of focus, NO legible text"* — and the real product screenshot is
  corner-pinned onto it in post. That guarantees the payoff word renders
  perfectly instead of coming back as a plausible-looking misspelling.
- **A contact sheet of alternatives reads as a storyboard to a client.** Stamp
  options as OPTIONS and sequences as CLIP N START. Never mix the two in one
  strip.

---

## OPEN QUESTIONS

Things I could not determine from the source and did not invent:

1. **Replicate USD pricing per generation.** The only figure in the record is
   roughly $111 for one heavy day across Seedance, Veo, Nano Banana Pro and
   Kling 2.5 combined. There is no per-model, per-second or per-image rate
   anywhere in the repo or the session log. The Kling credit prices (12/sec
   video, 70/30/4 for images) are measured and reliable; the Replicate ones are
   not known.

2. **`kwaivgi/kling-v2.5-turbo-pro`'s remaining input schema.** Five parameters
   are proven by a working call (`prompt`, `start_image`, `duration`,
   `aspect_ratio`, `negative_prompt` → `gen/char_kling.mp4`). Whether it also
   takes an end frame, a seed, or a resolution argument was never recorded.
   Run `gen.py schema kling25` if you need more than the five.

3. **`nano-banana-pro`'s `resolution` enum.** `"2K"` is the only value used in
   any job in the source. `1K` and `4K` are plausible but unverified, and no
   schema dump for this model survives in the repo.

4. **`nano-banana-pro`'s `safety_filter_level` and `allow_fallback_model`.**
   The section record says both exist with defaults `block_only_high` and
   `False`; neither appears in any job payload in the source and no schema dump
   survives, so both the existence and the defaults are unverified here.

4b. **The 404 slug probes and the literal `E004` / `E005` error codes.** Both
   are load-bearing (they justify the registry comment and the retry policy)
   and neither appears in any file in the repo — no log, no script, no doc
   contains the strings `E004`, `E005`, `flagged as sensitive`, or a record of
   probing `bytedance/seedance-2-pro` or `kwaivgi/kling-v3`. The *behaviour*
   they describe is corroborated (the three refused Seedance jobs left no
   output files; the handoff doc states the refusal rule), so the policy is
   right even if the codes are misremembered. The runner therefore matches on
   the prose as well as the code.

4c. **Which prompt produced the four shipped 405-408 aerials.** The mp4s exist
   (`gen/lands_b.mp4` and siblings, 1080x1920, 9.04s, with audio) but the
   scripts that generated them were not kept, and the prompt text appears
   nowhere in the repo. The closest surviving artefact is the ad caption
   `ads/03-segment-b/406-aerial-example-hook-b/caption-free.md`, which
   only says "Coastal megacity at golden hour." Do not reconstruct one and
   present it as the original.

4d. **The `gpt-image-2` vs `gpt-image2` naming split.** The claim that Kling's
   text-to-image model is `gpt-image-2` and its image-to-image model is
   `gpt-image2` is operationally important and appears only in the session
   narrative — the repo docs only ever write `gpt-image-2`. Confirm against the
   MCP's own model list before relying on it.

5. **How long Replicate output URLs stay alive.** The 24-hour figure in the
   handoff is specifically about **Kling** result URLs. Replicate's are
   temporary but no measured retention window exists in the source. The runner
   downloads in-process, so it has never mattered.

6. **Which Gemini model on Replicate corresponds to which on Kling.** Replicate
   exposes `google/nano-banana-pro` (and `google/nano-banana-2`); Kling exposes
   `gemini-3-pro-image` (Nano Banana Pro) and `gemini-3.1-flash-image` (Nano
   Banana 2). The likeness rejection in 30.6 was measured on **Kling's**
   `gemini-3.1-flash-image`. Whether Replicate's `nano-banana-pro` carries the
   same likeness filter was **never tested** — identity work on Replicate always
   used multi-reference stills rather than "make this the same person", which
   may be why it never tripped.

7. **`video/gen/` contents.** The directory is gitignored and local-only. File
   *names* are listed in this handoff where relevant (`c409_*`, `sheet_*`,
   `shot_s*`, `v409_s*`, `v2_sheets/*`), but the media itself exists on exactly
   one disk and has no remote. Nothing in this part can be reproduced from the
   repo alone — the prompts can, the outputs cannot.

8. **The zero.shoots production guide** is cited repeatedly as "the guide"
   (Part A/B/C, the base-image formula, the camera table, the requirement that
   the A24 compile use the GPT-image class). It is a purchased ebook, not in the
   repo. Everything of it that survives is summarised in this document and in
   `script409.md`.

---

## AUDIT NOTES (adversarial pass)

This part was audited against the actual sources: `video/rep.py`, the 36
surviving throwaway scripts in `/tmp`, `video/script409.md`,
`video/gen/v2_sheets/README.md`, the original video-ads handoff doc,
and the generated media itself (PIL/ffprobe measurements). Corrections below,
with the evidence.

### Fabrications removed

1. **`black-forest-labs/flux-1.1-pro` did not exist in this project.** It had a
   full registry entry (`safety_tolerance: 2`, `schema_verified=True`), a row in
   the 30.1 routing table crediting it with "the sky/atoll first-frames", a
   mention in 30.8 and one in the open questions. `grep -ho "models/<owner>/<name>"`
   across every Replicate script in the source returns exactly four slugs and
   their counts: `bytedance/seedance-2.0` (10), `google/nano-banana-pro` (13),
   `google/veo-3.1` (6), `kwaivgi/kling-v2.5-turbo-pro` (4). No Flux, anywhere,
   in any script, doc, or git commit touching `video/`. The sky and atoll
   first-frames were nano-banana-pro (`/tmp/sky_edits.py:25`,
   `/tmp/edit_first.py:17`). Entry and all four references deleted.

2. **The `lands_b.mp4` prompt was not the real prompt** and contained a
   literal `...` mid-quote. The string ("high-bypass turbofan", "nacelle",
   "coastal megacity") appears nowhere in the repo or `/tmp`; the only
   surviving trace of that ad's content is
   `ads/03-segment-b/406-aerial-example-hook-b/caption-free.md:5`,
   "Coastal megacity at golden hour." Replaced with the complete, verbatim
   Seedance text-to-video prompt from `/tmp/run_sky2.py:9-25` plus its real
   arguments, and the missing 405-408 prompts are now open question 4c.

3. **QA preview size `324x576` does not exist.** Only two preview sizes were
   ever used: half-size (`/tmp/sheet.py:23`, `/tmp/fix_man.py:26`) and 360x640
   (`/tmp/fix_c.py:29`, `/tmp/regen_B.py:31`). Corrected in 30.2 item 4 and in
   `write_preview`'s docstring.

4. **`eq=saturation=1.03` for BOSS "(p3 → 70.9)" was not verifiable and the
   endpoint was wrong.** There is no `p1/p2/p3.png` in `video/gen/v2_sheets/`,
   and `boss_profile_FINAL.png` measures saturation **71.7**, not 70.9. The
   BOSS Part B candidates are no longer on disk, so the BOSS multiplier cannot
   be recovered — the text now says so instead of quoting a number. The
   `match-sat` worked example was rewritten to use the pair that *is* on disk.

### Fabrication checked and CONFIRMED REAL

5. **`eq=saturation=1.13` for SOLO is exactly right**, and it is now proven
   rather than asserted: `ffmpeg -i herp_1.png -vf eq=saturation=1.13` produces
   a file byte-identical to the shipped `HER_PROFILE_FINAL.png`
   (md5 `f70fdd533baf9855f5d03aec27ab4f5f`, 5,465,228 bytes both). Measured
   `herp_1.png` sat 80.7 → 103.3 against a 103.5 target. Kept and strengthened.

6. **Contrast 37.1 / saturation 70.9 / 48.9 / 101.5** all re-measured and
   correct (`video/gen/v2_sheets/README.md:9-16`, and PIL agrees with the files).

7. **`kling-image-v3_0_omni` at 1:1 returns 2048x2048** — challenged, then
   confirmed. `loc_A.png` / `loc_B.png` are 2048x2048 and carry Kling's `tEXt
   AIGC` PNG chunk, not OpenAI's C2PA `caBX` chunk. Kept, and the size table was
   expanded into a proper two-model grid with the chunk test written down.

### Silent behaviour loss found and restored

8. **`kling25` was crippled.** The section claimed its input schema "was never
   dumped in the session record" and shipped `keys={}` with
   `schema_verified=False`, which makes `build_payload` hard-exit on any attempt
   to use it. But `/tmp/kling2.py:12-13` and `/tmp/kling_test.py:16` show the
   real parameter names in a call that **succeeded** — `gen/char_kling.mp4`
   exists, and ffprobe reports 1080x1920, 5.04s, video stream only, no audio.
   Registry entry filled in with `start_image` / `duration` / `aspect_ratio` /
   `negative_prompt` and the "no audio" fact is now evidence-backed.

9. **The 429 rate-limit backoff was dropped entirely.** `submit()` handled 402
   and let 429 fall through to `sys.exit`, while 30.7 simultaneously instructed
   the reader to "submit sequentially, 45s backoff". Three source scripts
   implement it (`/tmp/batch409b.py:28-37`, `/tmp/regen_vids.py`,
   `/tmp/retry_s6.py:14-18`), all with 45s waits. Restored with the originals'
   numbers (8 attempts, 45s), plus the load-bearing note that `batch409.py`'s
   `ThreadPoolExecutor(max_workers=10)` is what caused the throttling.

10. **`batch` regenerated work that already existed.** `/tmp/batch409b.py:25`
    skips any job whose output file is already on disk, which is what makes an
    interrupted batch free to resume. Restored as the default, with
    `--redo-existing` to override.

11. **`batch` aborted the whole run on one failure.** `/tmp/stills409.py:41-42`
    prints the failure and `continue`s, so one refused shot does not throw away
    the four that worked. Restored, with a failure summary and a non-zero exit.

### Wrong constants / wrong story

12. **"Early scripts crashed on short images" is false, and `1080x607` is the
    wrong number.** Verified against PIL: a 2752x1536 Nano Banana output scaled
    to width 1080 becomes 1080x**603**; the unguarded
    `crop((0,-659,1080,1261))` raises nothing at all — PIL returns 1080x1920
    with black bands, so the real failure is a silently letterboxed frame going
    into the next generation. The guarded version is the one that returns the
    short 1080x603. Both failure modes are now described in 30.2 item 3 and in
    `normalize_frame`'s docstring, with the file:line lists for which scripts
    did which.

13. **Poll intervals were wrong for two of four models.** "the video scripts
    polled every 5s" is true only of Seedance. Veo and Kling-2.5 single-shot
    scripts polled at 8s (`/tmp/veo.py:18`, `/tmp/veo_shot.py:18`,
    `/tmp/kling2.py:20`) and the Veo batch runners at 10s
    (`/tmp/batch409.py:50`, `/tmp/batch409b.py:40`, `/tmp/retry_s6.py:19`).
    Registry now carries 3 / 5 / 10 / 8 and the "no behaviour lost" claim is
    replaced by a declared change.

14. **The nano-banana-pro size table had a misattributed row.** "(elsewhere)
    2048x1152" is the **gpt-image-2** 16:9 size (`boss_portraitA.png`), not a
    Nano Banana output — no NBP file on disk is 2048x1152. Replaced with the
    measured table, every row backed by a named file, including the real 1:1
    result (2048x2048, `gen/c409_locsheet.jpg`).

15. **Only two of the three refused Seedance jobs were named.** The third wrote
    to `gen/char_sheet_vid.mp4` (`/tmp/sheet_test.py:27`) — and that script's
    own success message misreports its filename as `char_ref.mp4`, which is a
    trap for anyone checking. All three absences confirmed by directory listing.

16. **`requirements.txt` does not exist** anywhere in the repo (`find` across
    the tree, excluding `node_modules`). The instruction to "add pillow to the
    list" pointed at nothing; Part 5 already pins `pillow==12.1.1` in its pip
    line. Paragraph rewritten.

17. **Three "Kling rolls", model not named.** The source
    (the original video-ads handoff doc, line 263) says "Three Kling
    rolls"; naming `kling-image-v3_0_omni` was an inference. Now marked as one.

### Correctness bugs in the emitted runner

18. **`match_saturation` returned the wrong multiplier and reported success.**
    Run as originally written against the one job we can check, it returned
    `1.183` (sat 107.0) where `1.13` (sat 103.3) is correct. Cause: measured
    mean saturation is **not monotonic** in the eq multiplier on these dark
    images — 1.12→105.1, 1.13→103.3, 1.14→101.3, 1.15→112.0 — so a coarse sweep
    followed by a narrow refine locks onto noise. Replaced with a single dense
    sweep (0.80–1.40 at 0.01), a global minimum, a residual warning, and
    rawvideo-pipe probing instead of temp PNGs (identical pixels, ~7x faster).
    **Verified: it now reproduces `HER_PROFILE_FINAL.png` byte-for-byte in
    11.5s.** The non-monotonicity is written into the docstring so nobody
    "improves" it back.

19. **Hard-exiting on unverified enums was asymmetric risk.** The Seedance
    `resolution` / `aspect_ratio` enum lists were not from any schema dump in
    the repo (the source only ever sends 9:16 and 720p/1080p), so a legal value
    outside the invented list would have been blocked. Lists trimmed to what is
    observed and the check downgraded to a WARNING.

20. **`nano-banana-pro`'s `match_input_image` default breaks text-to-image.**
    With no `--edit` reference there is no input image to match. Every t2i job
    in the source passes an explicit aspect ratio (`/tmp/sheet.py:15`,
    `/tmp/stage1.py:10`, `/tmp/char_still.py:18`). Added a guard that fails
    before spending a generation. Verified: it now errors with a usable message.

21. **The `E004`/`E005` literals are not in the repo** — no file contains those
    strings, or "flagged as sensitive". The behaviour they describe *is*
    corroborated (three refused Seedance jobs left no output; the handoff doc
    states the rule), so the retry policy is right, but the matcher now also
    keys on the prose and open question 4b records the uncertainty.

### Verified as written, no change needed

- Kling pricing: 12 credits/sec, 15s=180 / 9s=108 / 8s=96; images 70/30/4;
  `kling-image-o1` ~2 credits; 8000-credit grant expiring one month out
  (handoff doc lines 247-257, 65, 98-99).
- 18 credits burned on the from-behind/face-sheet contradiction (line 259).
- The stale-`query_tasks` numbers: QUEUING 8 min on a 106s job, RUNNING 14 min
  on a 58s job, cached credit balance (lines 277-286).
- 24h expiry on Kling result URLs (line 340).
- Veo 4/6/8s — cross-checked with ffprobe: `gen/v409_s4.mp4` is 4.00s,
  `gen/v409_s8.mp4` is 6.00s, both 1080x1920.
- The five-setup / twelve-shot table and the per-shot model routing in 30.11
  match `video/script409.md:64-70` and `:145-152` exactly, including which
  shots reuse A, B and C.
- The ABCD-location-sheet-rendered-as-a-shot story, including the 0.9s top-down
  drone view of a woman lifting a chair (lines 225-232). Added the detail that
  the non-omni model also rendered in half the time (6 min vs 13), which the
  section had dropped.
- Part A "gpt-image-2, 16:9, 2k, high" (`video/gen/v2_sheets/README.md:9`).
- The 402 wait loop: 15 attempts, 60s apart (`/tmp/edit_creature.py:22-36`).
- `rep.py`'s 3s poll, `video/.env`-only token read, and the
  `f"...{m.get('predict_time'):.1f}s"` TypeError (`video/rep.py:42, 19-24, 62`).

### Verification actually performed

The emitted runner was extracted from this file and executed. `py_compile`
passes; `--help` renders; `tone`, `normalize`, `match-sat` and `batch`'s
skip-existing path were all run against real project files and produced the
results quoted above. Nothing else in this section was "verified" beyond
reading the source.

**One disclosure:** while exercising the CLI I ran a `video` subcommand that
went past argument validation and submitted a real Seedance prediction
(`5fn45ny0khrmr0czppkt8bba50`). I cancelled it within seconds; it returned
`status: canceled` with no `predict_time` in its metrics, so billed compute
should be negligible, but I cannot prove it was zero. That was my error, not a
property of the runner. Note the lesson it accidentally demonstrates: **there
is no `--dry-run` on this tool.** Anything that reaches `do_job` spends money.
Adding a `--dry-run` that prints the payload and exits is the obvious next
change and is deliberately left undone here rather than shipped untested.
