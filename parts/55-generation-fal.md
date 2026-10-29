# PART 55: The fal layer. Voices, talking takes, lip sync, cutouts and stills from one key

**fal is the default generation account for this engine.** One key in
`engine/.env` covers generated voiceovers, talking-head takes with natural
voices, lip sync onto real footage, background removal, silent motion clips and
product stills. Replicate (`parts/50`) and Kling's MCP (`parts/60`) are still
documented and still work; reach for them when this part sends you there.

Everything in this file ran on a real fal account and produced a finished file
that shipped or was reviewed. Endpoint names and payload fields are copied from
those scripts, not from fal's marketing pages. **If you want a model that is not
in the table below, treat it as untested:** open its page on fal.ai, read the
input schema, and dry-run it before spending.

Read `parts/70-playbook-and-failures.md` before the first paid call, and
`parts/00-keys-and-accounts.md` §5.14 before you create the key.

---

## 55.1 The runner: `scripts/fal.py`

The runner is the one script Claude uses to talk to fal. It submits a job to
fal's queue, waits for it to finish, and downloads the result into the engine
folder. Every call below goes through it, so there is no per-ad fal code to
write.

```bash
cd engine

# Dry run: prints the endpoint and payload, spends nothing
python3 scripts/fal.py <endpoint> '<json payload>' <outfile>

# The same call for real
python3 scripts/fal.py <endpoint> '<json payload>' <outfile> --go

# Put a local video, audio clip or image on fal storage; prints a URL
python3 scripts/fal.py --upload public/footage/speaker.mp4

# Small images only: print a data URI to paste into an image_url field
python3 scripts/fal.py --datauri public/img/product.png
```

Four rules the runner enforces, and that anything you add must keep:

1. **The key comes from `engine/.env` and nowhere else.** The shell environment
   is never read, so a key exported for another project cannot bill through
   this engine by accident. The key is never printed.
2. **Nothing spends without `--go`.**
3. **It does not know prices.** The dry run shows the job, not the cost. Before
   `--go`, open the model's page on fal.ai, read the current price, and tell
   the operator in dollars. In the projects this part was written from, the
   per-run price was never checked and the spend was only ever "uncounted".
   Do not repeat that.
4. **Uploads before URLs.** Lip sync and video endpoints want a `video_url` or
   `audio_url`. Upload the file with `--upload` and pass the URL it prints.
   A base64 data URI worked for a small five-second clip once, but it bloats
   the request and is the first thing to fail on anything longer.

Results download as soon as the job finishes. Do not keep fal result URLs
around as the only copy of a file you paid for.

---

## 55.2 The routing table: which endpoint for which job

### Voice

| Endpoint | Use it for | Payload that worked |
|---|---|---|
| `fal-ai/minimax/speech-2.8-hd` | **The default narrator.** One continuous read, cut to the script by Whisper word timings. Produced every narrator read in a run of shipped ads | `{"text": "...", "voice_setting": {"voice_id": "English_CaptivatingStoryteller", "speed": 1.0, "emotion": "happy"}, "output_format": "url"}` |
| `fal-ai/elevenlabs/tts/eleven-v3` | ElevenLabs library voices. **These return 402 on ElevenLabs' free direct plan but work through fal**, so you need no ElevenLabs subscription for them | `{"text": "...", "voice": "Charlie", "stability": 0.45, "similarity_boost": 0.8, "speed": 1.1}` |
| `fal-ai/chatterbox/text-to-speech` | Zero-shot voice clone from a reference clip. Needs a clean 15 s clip of one speaker alone. **Only with that speaker's written consent** | `{"text": "...", "audio_url": "<uploaded ref clip>", "exaggeration": 0.6, "cfg": 0.4}` |

Every voice file then goes through the normal spine in `parts/10`:
`scripts/timings.py` for word timings, `scripts/prosody.py` for uptalk, and a
human listening to the whole thing.

### Talking takes (a person speaking, with a natural voice)

| Endpoint | Use it for | Payload that worked |
|---|---|---|
| `bytedance/seedance-2.5/text-to-video` | **A talking spot: one take per speaker, the whole line in one go, native audio.** Also a voiceover source: its voices were judged more natural than the text-to-speech reads, so generate at 480p, keep the audio, throw the picture away | `{"prompt": "...", "duration": "30", "resolution": "480p", "aspect_ratio": "9:16", "generate_audio": true}` |
| `bytedance/seedance-2.5/reference-to-video` | A voice matched to a reference clip. Put `@Audio1` (and optionally `@Image1`) in the prompt and pass the files as URLs. Used for voice only; the picture was discarded | `{"prompt": "... @Image1 ... @Audio1 ...", "image_urls": ["..."], "audio_urls": ["..."], "duration": "30", "resolution": "480p", "aspect_ratio": "9:16", "generate_audio": true, "seed": 1}` |

The prompt shape that produced clean, usable takes:

```
Static camera, locked off, close-up at eye level, front view, vertical frame,
one continuous take with no cuts. <who: age, look, wardrobe> sits at a desk in
a quiet, softly lit home office and talks to the camera. Calm, friendly and
natural, like a podcast host explaining something useful to a friend, not a
salesperson. Every word is articulated clearly at a relaxed conversational
pace, with a short natural pause between sentences. <He/She> says: "<line>"
Then <he/she> stops talking and smiles. NO MUSIC. No background noise, only
the voice in a quiet room. No texts or subtitles on screen.
```

### Lip sync (new audio onto real footage of a face)

| Endpoint | Use it for | Payload that worked |
|---|---|---|
| `fal-ai/sync-lipsync/v2/pro` | **The default lip-sync pass.** Real footage of a speaker plus a new voice track | `{"video_url": "...", "audio_url": "...", "sync_mode": "cut_off"}` |
| `fal-ai/latentsync` | The second option, and the fix pass for generated clips whose mouths drift | `{"video_url": "...", "audio_url": "..."}` (optional `"guidance_scale": 2.0, "loop_mode": "pingpong"`) |

**Consent comes first.** Putting words in a real person's mouth needs their
explicit yes, and they watch the exact file before it runs anywhere. One
founder banned any AI version of their voice or face after the ads using it
were already built. Ask before you build, not after.

### Cutouts

| Endpoint | Use it for | Payload that worked |
|---|---|---|
| `bria/video/background-removal` | Cuts a person out of a video and leaves the background transparent, like a green screen without the green. Used for a speaker cutout sitting in the corner over the rest of the ad | `{"video_url": "...", "background_color": "Transparent", "output_container_and_codec": "webm_vp9", "preserve_audio": false}` |

Crop to head and shoulders **before** the cutout. It is cheaper, and the
transparent webm then drops straight into an overlay.

### Silent motion and stills

| Endpoint | Use it for | Payload that worked |
|---|---|---|
| `fal-ai/kling-video/v2.5-turbo/pro/image-to-video` | Silent B-roll from a still: a person listening on a webcam call, small natural movement. About 90 s to render a 5 s clip | `{"prompt": "...", "image_url": "...", "duration": "5", "negative_prompt": "camera movement, zoom, text, captions, distortion, extra people"}` |
| `fal-ai/kling-video/v2.1/pro/image-to-video` | First frame plus last frame, the model fills the motion between. Used for product turntables | `{"prompt": "...", "image_url": "<start>", "tail_image_url": "<end>", "duration": "5", "cfg_scale": 0.5, "negative_prompt": "blur, distort, low quality, text, watermark, extra objects, morphing hands"}` |
| `fal-ai/nano-banana-pro/edit` | Product and scene stills built from reference images. About 90 generations in one product project | `{"prompt": "...", "image_urls": ["...", "..."], "aspect_ratio": "4:5", "resolution": "2K", "output_format": "png", "num_images": 1}` |

**Kling on fal is for silent footage.** For dialogue with native audio on Kling
3.0, use Kling's own MCP and `parts/60`. For a talking person, use Seedance
text-to-video above, which is what finally shipped after every Kling mouth was
rejected.

---

## 55.3 What went wrong, so it does not go wrong again

**1. `403 "User is locked. Reason: Exhausted balance"` means top up, not a bad
key.** It has hit mid-session more than once. Check the balance at
`https://fal.ai/dashboard/billing` before any long job, and stop and tell the
operator when it appears. Do not rotate the key over it.

**2. Keep parallel batches small.** Bursts of six parallel jobs got some 403s
that passed on a retry. Retry once, and only after confirming the balance is
not the cause.

**3. fal's Seedance image-to-video refuses photoreal start frames** ("likeness
of a real person"). Do not fight it. Describe the person in words and use
text-to-video.

**4. Seedance fills its whole clip no matter how short the line is.** Pace
comes from the edit, not the prompt: trim the silences (`silenceremove`) and
speed the voice up about 15% with `atempo=1.15`, which keeps the pitch.

**5. Delivery words change the read more than anything else.** A prompt that
asked for a calm read came back "slow and emotionless"; re-rolling with an
upbeat, energetic description fixed it. "Flat", "dry" and "unhurried" all
produced a depressing read. Describe the person you want to hear, not the
absence of energy.

**6. Spell out anything the voice can misread.** "OpenAI" came back as "open
eyes" until the script said "Open A.I."; write "one-oh-one" for 101 and spell
names the way they sound. Keep the real spelling on screen, and fix Whisper's
own mishearings in the timings file.

**7. Generated mouths drift.** Kling 3.0's native audio ran the mouth 250 to
500 ms off and never closed on p, b and m. Every talking clip made that way
needed a lip-sync pass (§55.2) before it could ship.

**8. Judge lip sync with frames, not with a model's opinion.** A video model
gave contradictory lip-sync verdicts on the same footage twice. Pull a frame
strip at the plosives (p, b, m) and line it up against Whisper's word onsets.
The sync model also damps mouth movement, so check that the mouth still moves
enough.

**9. Check the source stretch before a lip-sync spend.** LatentSync fails with
"no face" when the face leaves the frame or another person appears mid-clip.
Step the stretch at 2 fps first and pick one where the face stays put the whole
time.

**10. Reference-to-video re-stages the scene every roll.** It is good for
matching a voice and bad for picture consistency. On Replicate, Seedance 2.5
refused an image and reference audio in the same call (`ModelError E006`); on
fal the reference-to-video endpoint accepted both. Either way, when the picture
has to stay consistent, lock it with a start frame and bring the voice in
separately.

---

## 55.4 Recipes

**A generated voiceover for OneWord or Cards.** MiniMax through fal, one
continuous read, then the normal spine.

```bash
python3 scripts/fal.py fal-ai/minimax/speech-2.8-hd \
  '{"text":"<script>","voice_setting":{"voice_id":"English_CaptivatingStoryteller","speed":1.0},"output_format":"url"}' \
  public/audio/vo_101.mp3            # dry run first, then add --go
ffmpeg -y -i public/audio/vo_101.mp3 -ac 1 -ar 48000 public/audio/vo_101.wav
python3 scripts/timings.py public/audio/vo_101.wav public/words/101.json
```

MiniMax returns an mp3; the engine's convention is a 48 kHz mono wav, which is
what the conversion line makes.

**A natural-sounding voice with no face on screen.** Seedance 2.5
text-to-video at 480p with the prompt shape in §55.2, then pull the audio:

```bash
ffmpeg -y -i take.mp4 -vn -ac 1 -ar 48000 public/audio/vo_101.wav
```

Two voices (a man and a woman) in parallel give the operator a choice for the
price of two takes.

**A real speaker saying a new line, as a corner cutout** (with their consent):

1. Crop the source footage to head and shoulders with ffmpeg, on a stretch
   where the face stays in frame (step it at 2 fps).
2. `--upload` the crop and the new voice track.
3. `fal-ai/sync-lipsync/v2/pro` with `sync_mode: cut_off`.
4. `bria/video/background-removal` on the lip-synced result, transparent webm.
5. Place it with `scripts/overlay.py` or a Remotion component.

**Product stills from references.** `fal-ai/nano-banana-pro/edit` with the
approved product shots as `image_urls`, a fixed prompt block describing the
look, then the scene. Keep the fixed block in one file so every still shares
it.

Checkpoint one of anything end to end, have the operator watch and listen,
report the spend, and only then batch.
