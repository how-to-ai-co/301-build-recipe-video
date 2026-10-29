# AI generation services

What each service is for, how it connects to Claude, roughly what it costs, and
what goes wrong. Generation is the only part of this repo that spends money.
Most videos don't need it.

**Checked 29 October 2026.** This market changes monthly: models are renamed,
previews are shut down, prices move. Items marked **[unverified]** came from
third-party sites or sources that disagree. Before any paid call, open the
model's own page and read today's price.

Built on the instructor's summary (`motion-301/video-engine-summary.md`) and
the repo's guides: `parts/00-keys-and-accounts.md` (accounts and keys),
`parts/55-generation-fal.md` (fal, the default), `parts/50-generation-replicate.md`,
`parts/60-format-kling-dialogue.md`, `parts/10-voice-and-music.md`, and the
failure log `parts/70-playbook-and-failures.md`.

---

## What you need for each mode

| Mode | What it makes | You need | Typical spend |
|---|---|---|---|
| **Your own footage** (Yap, creator clips, Cards, OneWord) | Edits, captions, overlays, cuts on video you shot | **Nothing.** ffmpeg and Node. Your phone's voice memo for a voiceover | $0 |
| **Motion graphics** (`motion-studio/`) | Animated logos, charts, explainers in code | Nothing | $0 |
| **Aerial** | A 9-second silent landscape with text | Your own clip and ffmpeg. To generate the clip: a fal key (or Replicate) | About $0.50–$2 a clip |
| **Generated voice** | A voiceover from text | A fal key | Cents per ad |
| **Generated scenes, stills, B-roll** | Footage and images that don't exist yet | A fal key; Replicate or Kling for specific models | A few dollars to tens of dollars a video |
| **Talking people, lip sync** | A person saying a line | A fal key, **plus written consent** if it looks or sounds like a real person | Dollars per take; expect re-rolls |
| **Scripted film with actors** | Multi-shot dialogue scenes | Replicate, fal and Kling | Can reach the low hundreds of dollars per session |

Rough spends are estimates from the per-second prices below [general], not measured totals.

## Start free

Make your first three videos without a single key:

1. **Own footage.** Record a talking-head on your phone. Claude trims the
   silences, cleans the audio, adds a hook title and overlays (`recipes/yap.md`).
2. **OneWord.** Record a voice memo of your script. Whisper turns it into
   word timings, Remotion shows one word at a time. $0.
3. **Motion graphic.** Ask for an animated stat or chart in `motion-studio/`. $0.
4. **Music:** `engine/scripts/bed.py` composes an original bed on your machine. $0, and no licensing risk.
5. **Images:** use your own screenshots, product shots and public-domain images first.

When you want generation, get **one fal key** first. It covers voice, talking
takes, lip sync, cutouts, silent clips and stills. Put $10–$20 on it and set a
stop-loss before your first call.

**Free credits:** ElevenLabs has a free tier (10k credits a month, no
commercial use). Google's Gemini app and Flow include some video with Google AI
plans. No free API credits were confirmed for fal, Replicate, Kling or Runway
**[unverified]**.

---

## Safety rules (read before any paid call)

1. **Never put words in a real person's mouth without their written consent.**
   That covers lip sync, voice cloning, and generated video of someone who
   looks like a real person. They watch the exact file before it runs anywhere.
   One founder banned any AI version of their face or voice after the ads were
   already built. Ask before you build. (`parts/55`)
2. **No keys in chat.** Never paste an API key into Claude, a terminal command,
   or any file except `engine/.env` (which is gitignored). Claude will give you
   the `read -s` pattern in `parts/00` §5.3 so the key goes straight into the file
   without being shown. If a key was ever seen, rotate it.
3. **Dry run before you spend.** Both runners spend nothing without `--go`:
   - `engine/scripts/generate.py` (Replicate) prints the exact payload **and the price**, then stops.
   - `engine/scripts/fal.py` prints the endpoint and payload, then stops. **It does not know prices.**
     Claude must open the model's page on fal.ai and tell you the cost in dollars before adding `--go`.
4. **Claude asks before every spend.** It states the cost, then waits for a clear yes. (`CLAUDE.md`)
5. **One shot end to end before a batch.** Generate one, take it through the
   edit, watch and listen. Then batch. (`parts/70`)
6. **Decide the stop-loss first.** Write down the dollar amount at which you stop. (`parts/70`)
7. **Never resubmit because a job "looks stuck."** Status pages lag by up to 14 minutes. (`parts/70`)
8. **Download results right away.** Result links expire (Kling and others: 24 hours).
9. **Label it.** Platforms ask you to mark realistic AI-generated content. Google adds an invisible SynthID watermark to everything its models make.

---

## How things connect to Claude

| Route | How | Who |
|---|---|---|
| **API key in `engine/.env`** | Create a key on the service's site, store it with `read -s`. Claude's scripts read it from the file only | fal (`FAL_KEY`), Replicate (`REPLICATE_API_TOKEN`), ElevenLabs |
| **MCP (sign in once)** | Add a connector, fully quit and restart Claude, sign in through the browser. No key in any file | Kling (`https://kling.ai/mcp`), Higgsfield (`https://mcp.higgsfield.ai/mcp`), fal (`https://mcp.fal.ai`), ElevenLabs |
| **Web only** | You generate on the site, download, and drop the file in the project | Google Flow, Runway web, Luma, Pika, Dreamina/CapCut |

The **restart trap:** MCP tools only appear in a Claude session started after
the connector was added. Quit fully and relaunch. This once cost a whole session. (`parts/60`)

---

## The services

### fal — the default (get this key first)
- **For:** voices, talking takes, lip sync, video background removal, silent clips, stills. Hosts Kling, Seedance, MiniMax, Flux, Nano Banana and more under one key.
- **Connects:** API key `FAL_KEY` in `engine/.env`, used by `engine/scripts/fal.py`. There is also an official hosted MCP at `mcp.fal.ai` (free; you pay normal model prices), not used by this repo.
- **Pricing:** prepaid balance, priced per model, mostly per second of video. Examples: Kling v3 Pro about $0.14/s, Kling 2.5 Turbo about $0.07/s, MiniMax H3 Max about $0.05/s. No charge for queue time or server errors.
- **Proven endpoints in this repo** (`parts/55`): `fal-ai/minimax/speech-2.8-hd` (default narrator), `fal-ai/elevenlabs/tts/eleven-v3` (ElevenLabs voices without an ElevenLabs plan), `bytedance/seedance-2.5/text-to-video` (talking spot with native audio), `fal-ai/sync-lipsync/v2/pro` (lip sync), `bria/video/background-removal` (cutouts), `fal-ai/kling-video/v2.5-turbo/pro/image-to-video` (silent B-roll), `fal-ai/nano-banana-pro/edit` (stills).
- **Gotchas:**
  - `403 "User is locked. Exhausted balance"` means top up, not a bad key.
  - Six parallel jobs got random 403s. Keep batches small.
  - Seedance on fal refuses photoreal start frames ("likeness of a real person"). Describe the person in words instead.
  - Seedance fills its whole clip however short the line. Fix pace in the edit (`atempo=1.15`).
  - Spell out what voices misread: "Open A.I.", "one-oh-one".
- **Link:** https://fal.ai/pricing

### Replicate
- **For:** specific video and image models not proven on fal in this repo: `bytedance/seedance-2.0` (landscapes, no human face input), `google/veo-3.1` (face input plus native audio), `google/nano-banana-pro`.
- **Connects:** API key `REPLICATE_API_TOKEN` in `engine/.env`, used by `engine/scripts/generate.py` (prints the price on a dry run).
- **Pricing:** pay as you go against a prepaid balance. Most models bill per second of GPU time; some per output. **Check auto-reload**: with it on, there is no ceiling.
- **Ownership:** Cloudflare announced it would buy Replicate (Nov 2025). Brand and API unchanged. Whether the deal closed: **[unverified]**.
- **Gotchas:** Seedance refuses any human face as input. Veo rate-limits hard (submit one at a time, 45 s apart) and drifts in its last half-second: trim tails. Image models return wrong sizes: always normalise. Whether `google/veo-3.1` still runs on Replicate after Google retired the Veo 3.1 *preview* IDs on its own API (22 Oct 2026): **[unverified]**, check the model page.
- **Link:** https://replicate.com/pricing

### Kling (Kuaishou)
- **For:** dialogue scenes with native audio and lip sync, multi-shot takes, cheap reference-consistent images.
- **Models:** Kling 4.0 (announced 15 Oct 2026, preview, up to 30 s). Kling 3.0 / Omni is what this repo's film used. Kling 2.5 Turbo for silent clips via fal.
- **Connects:** Kling's own MCP, `https://kling.ai/mcp`, registered in `~/.claude.json` (type `http`). Sign in through the browser; no key. Then restart Claude. (`parts/60` §a, `parts/00` §5.7). A web-search check found no public listing for this MCP, only third-party ones, but the repo's entry is the one that worked. Kling also sells API access separately.
- **Pricing:** monthly web plan with credits that **expire on a fixed date** (read the date; unspent credits are lost). Measured: **12 credits per second** of video on every v3.0 tier (15 s = 180 credits). Images: `kling-image-v3_0_omni` 4 credits for two 2K images vs `gpt-image-2` 70 credits: a **17x** spread. Standard plan about $10/month for 660 credits **[unverified]**. Kling 4.0 API price **[unverified]**.
- **Gotchas:**
  - `enable_audio` defaults to off on Omni. A silent 15 s take is 180 wasted credits.
  - `resolution` defaults to 4K. Set 1080p.
  - Cap each generation at about 3 shots; 5 shots garbles dialogue.
  - Native audio drifts 250–500 ms off the mouth. Every talking clip needed a lip-sync pass.
  - Watch for the multiple-login trap: you can end up with two Kling accounts (`parts/00` §5.6.1).
  - Status reports lag badly. Poll every 5+ minutes.
- **Link:** https://klingai.com

### Higgsfield
- **For:** one sign-in to 30+ models (Kling, Veo, Seedance and others) from inside Claude, plus Higgsfield's own camera-move presets.
- **Connects:** official MCP at `https://mcp.higgsfield.ai/mcp`. Add it as a custom connector (or `claude mcp add`), sign in with your Higgsfield account. No API key. Needs a paid plan.
- **Pricing:** subscription credits. "Unlimited" plan perks **do not apply** to MCP use; generations through Claude spend credits (about 14 credits for an 8 s 720p Kling 3 clip). Plans roughly $19 / $47 / $99 a month billed yearly **[unverified]**.
- **Gotchas:** not used by this repo's scripts, so there is no dry-run price print. Claude must check the credit cost in Higgsfield before each call.
- **Link:** https://higgsfield.ai

### Google Veo, Gemini Omni and Flow
- **For:** high-quality clips with native sound.
- **Models:** **Gemini Omni Flash** (`gemini-omni-1.1-flash`, May 2026) is now Google's recommended video model on the Gemini API: up to 10 s, native audio, edit by chatting. Veo 3.1 preview IDs on the Gemini API were **shut down 22 Oct 2026**. Generally available Veo still runs on Google Cloud (Vertex) **[unverified pricing]**.
- **Connects:** Gemini API key (not wired into this repo's scripts), Replicate (`google/veo-3.1`), or web only through Flow / the Gemini app.
- **Pricing:** Omni Flash about $0.10/s at 720p, no free tier on the API. Via Runway's API: Veo 3.1 $0.40/s with audio, Veo 3.1 Fast $0.15/s. Flow credits come with Google AI Plus / Pro / Ultra plans **[credit amounts unverified]**.
- **Gotchas:** SynthID watermark on everything. Preview models get retired fast. Veo drifts at the end of clips.
- **Link:** https://ai.google.dev/gemini-api/docs/pricing

### Seedance (ByteDance)
- **For:** landscapes, aerials, action, wides; natural talking takes with native audio.
- **Models:** Seedance 2.5 (Jul 2026, up to 30 s). Seedance 2.0 still widely hosted.
- **Connects:** through fal (`bytedance/seedance-2.5/...`, proven in `parts/55`) or Replicate (`bytedance/seedance-2.0`). Consumer route: Dreamina / CapCut. Direct BytePlus API **[unverified]**.
- **Pricing:** via Runway's API, 2.5 at 720p about $0.30/s, 1080p about $0.68/s. fal prices per model page.
- **Gotchas:** refuses photoreal human faces as input images. Fills the full duration however short the script. Lots of conflicting reseller marketing.

### Runway
- **For:** Gen-4.5 video ($0.12/s), Aleph 2 for editing existing video ($0.28/s), Act-Two performance capture ($0.05/s). Its API also resells Kling, Veo, Seedance, Wan, Hailuo and others with clear per-second prices: a one-key alternative to fal.
- **Connects:** API key (not wired into this repo's scripts) or web.
- **Pricing:** API credits are prepaid at $0.01 each and are **separate from web-plan credits**. Web plans roughly $35 and $95 a month **[unverified]**.
- **Link:** https://docs.dev.runwayml.com/guides/pricing/

### Luma
- **For:** Ray3.2 video (including HDR), Uni-1.1 images.
- **Connects:** API key or web (now "Luma Agents"). Not wired into this repo.
- **Pricing (API):** a 5 s clip $0.15 at 540p, $0.30 at 720p, $1.20 at 1080p; 10 s clips 3x those. HDR costs 2–4x more. Web plans $30 / $90 / $300 a month **[unverified]**.
- **Link:** https://lumalabs.ai/api/pricing

### Pika and others worth knowing
- **Pika:** cheap, playful effects. Web plans from about $8 a month; a $10/month "API Club" with access to 70+ models and reportedly an MCP. **All [unverified].**
- **MiniMax Hailuo:** H3 (up to 2K, native audio) is current. Cheap: about $0.05/s for H3 Max on fal. MiniMax's speech model (`speech-2.8-hd` on fal) is this repo's default narrator.
- **Wan (Alibaba):** Wan 3.0 (Aug 2026) is **closed, API only**. The newest **open** version is Wan 2.2 (Apache 2.0), which you can run yourself.
- **OpenAI Sora:** **discontinued.** The app closed in April 2026 and the API models were removed on 24 Sep 2026. Ignore old guides that recommend it.
- **AI Producer by OpusClip:** an AI video-editing connector in Claude's directory **[not tested]**.

### ElevenLabs (voice and music)
- **For:** voiceover, voice cloning (with consent), sound effects, Eleven Music.
- **Models:** Eleven v4 is the newest voice model; v3 still offered.
- **Connects:** API key in `engine/.env`, or an official MCP (hosted: `https://api.elevenlabs.io/v1/mcp/mcp`; or local `uvx elevenlabs-mcp` with your key). **This repo's advice: skip a direct subscription.** fal serves ElevenLabs voices (`fal-ai/elevenlabs/tts/eleven-v3`) on your fal key.
- **Pricing:** Free $0 (10k credits/month, **no commercial licence**), Starter $6, Creator $22, Pro $99 a month and up. Speech costs about 1 credit per character; music about 900 credits a minute.
- **Gotchas:** library voices return 402 on the free direct plan. Cloned voices and the Music API need a paid plan. Generated music still isn't needed here: `bed.py` composes one for free.
- **Link:** https://elevenlabs.io/pricing

### Image models

| Model | Best for | Connects | Price per image |
|---|---|---|---|
| **Nano Banana** (Google Gemini image) | Edits from reference images, product and scene stills. Repo used Nano Banana Pro for ~90 product stills | fal (`fal-ai/nano-banana-pro/edit`), Replicate, Kling, Gemini API | Nano Banana 2.1 (newest) about $0.034 at 1K to $0.11 at 4K; Nano Banana Pro about $0.13–$0.24. Original Nano Banana shuts down 15 Mar 2027 |
| **GPT Image** (OpenAI) | Exact instruction-following, film-grade look, precise edits of a reference frame | Kling (`gpt-image-2`), OpenAI API | `gpt-image-2.5` about $0.006 (low) / $0.05 (medium) / $0.21 (high) at 1024² [estimate]. `gpt-image-1` was shut down 23 Oct 2026 |
| **Flux** (Black Forest Labs) | Fast, cheap stills; open-weight options | fal, Replicate, BFL API | FLUX.2 from $0.014 (klein) to $0.07 (max). FLUX 3 prices **[unverified]** |
| **Kling image** (`v3_0_omni`, `o1`) | Keeping a face consistent; surgical single edits | Kling MCP | 4 credits for two 2K images; about 2 credits for one edit. Default for identity work |

**Image gotchas from this repo:** Nano Banana 2 rejects likeness prompts (fails in about 5 s with no error). Image models return the wrong size: always resize. When the face is visible, **edit** the reference frame, don't recreate it. For a from-behind shot, don't pass a face sheet, or the model paints the face somewhere else. (`parts/00` §5.12, `parts/50`)

---

## Lessons already paid for

From the instructor's summary and `parts/70`:

- Seedance refuses any input image with a human face.
- For talking people, Seedance on fal worked after every Kling mouth was rejected.
- Kling's own image model is about 17 times cheaper than GPT Image 2.
- Change one thing per round. Moving several at once wasted a whole batch.
- Pasted text-to-speech sounds dubbed. Native audio, a little room reverb and a high-shelf cut close most of the gap.
- AI footage is too clean. Grade it in code (`engine/scripts/grade.py`): lower contrast, lift blacks, 3–8% grain.
- Join generated clips with the concat filter, not stream copy, or lip sync drifts.
- **A human listens before it ships.** Every unheard version failed.
- Get written consent before putting words in a real person's mouth.

## Not verified on 29 October 2026
- Kling 4.0 API pricing and Kling web plan prices.
- Higgsfield, Runway web, Luma web and Pika plan prices.
- Seedance direct API through BytePlus.
- Vertex AI (Google Cloud) Veo pricing, and whether Replicate's `google/veo-3.1` still runs.
- Free API credits on fal, Replicate, Kling or Runway.
- Whether Cloudflare's purchase of Replicate has closed.
- FLUX 3 image prices.
- Content and likeness policies for each service were not individually re-checked. Every one restricts real people and public figures in some way.
