# References

Guides Claude reads while making a video. You don't need to read them first;
Claude opens the right one when the job reaches it. They are plain Markdown, so
you can read or edit any of them.

| File | What it's for | Claude reads it when |
|---|---|---|
| [library-guide.md](library-guide.md) | The animation and video toolkit: Remotion, HyperFrames, GSAP, Lottie, Three.js, ffmpeg (with 10 copy-paste recipes), Whisper, yt-dlp and more. Licences, costs, and an "I want X, use Y" table | Choosing how to build motion, encode, transcribe or clean audio |
| [design-rules.md](design-rules.md) | Rules that stop videos looking AI-made: type sizes, safe zones, colour, timing in frames, composition, banned looks, animated charts, audio levels, and a pre-export checklist | Planning, designing and checking any video |
| [video-generation.md](video-generation.md) | AI generation services (fal, Replicate, Kling, Higgsfield, Veo, Seedance, Runway, Luma, ElevenLabs, image models): what each is for, how it connects, rough prices, gotchas, safety rules, and a "start free" path. Checked 29 October 2026 | Anything that needs generated footage, voices or images, before any spend |
| [videos/](videos/) | Breakdowns of reference videos: pacing, text and look of videos you want to copy the style of | You share a video and say "make it like this" |
| [instagram-safe-zone.png](instagram-safe-zone.png) | The 1080 x 1920 Instagram safe-zone guide. Keep text and faces inside x 35–980, y 220–1470. Notes in `../instagram-safe-zone.md` | Placing any text, face or must-read content |

**Your own rules win.** Notes you give on drafts are saved as rules in
`.claude/skills/video-edit/references/edit-rules.md`. Where they disagree with
these guides, yours apply.

**Facts go stale.** Prices, models and licences in `library-guide.md` and
`video-generation.md` were checked on 29 October 2026. Ask Claude to re-check
before you spend money or use a tool for a client.
