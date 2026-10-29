# Reference videos

Found a video whose style you love? Paste the link (Instagram Reel, TikTok, YouTube Short, anything) or drop the file into the chat and say **"make mine like this."** Claude runs `engine/scripts/reference.py`, which downloads it here into its own folder, measures the length, cuts per second and average shot length, pulls a contact sheet and keyframes, checks the loudness, and transcribes the words if Whisper is installed. Claude then looks at the frames, fills in `breakdown.md` (hook, titles, captions, overlays, colour, energy, pacing) and proposes how to get the same feel with your own footage and brand. References are for studying style only: nothing from them goes into your video, and everything except each `breakdown.md` stays out of git.

```bash
cd engine
python3 scripts/reference.py "https://www.instagram.com/reel/..."     # needs yt-dlp
python3 scripts/reference.py ~/Downloads/video.mp4                   # a file works too
python3 scripts/reference.py "<link>" --cookies-from-browser chrome  # if the site wants you logged in
```

**Already documented:** [`styles/`](../../styles/README.md) has three named styles built from references (Yap Depth, Oren Static Hooks, Editorial Tech). Ask for one by name, or ask Claude to save a new reference as a fourth.

## Places to find good references

Channels, not single videos, so the links stay alive. Most post Shorts/Reels alongside long-form; open the Shorts tab.

**Talking-head edits** (fast cuts, punch-ins, bold captions)
- Alex Hormozi: https://www.youtube.com/@AlexHormozi (the word-by-word bold caption look)
- Ali Abdaal: https://www.youtube.com/@aliabdaal (clean, bright, b-roll-heavy talking head)
- GaryVee: https://www.youtube.com/@garyvee (raw clips, big hooks, captions)
- Colin and Samir: https://www.youtube.com/@ColinandSamir (creator interviews, tidy editorial cuts)

**Kinetic typography** (text that moves with the words)
- Art of the Title: https://www.artofthetitle.com/ (film and TV title sequences; the classic type-in-motion library)
- Ben Marriott: https://www.youtube.com/@BenMarriott (motion design tutorials, lots of animated type)
- Remotion showcase: https://www.remotion.dev/showcase (videos made in code with Remotion, the same tool as `engine/`)

**Product explainers**
- Apple: https://www.youtube.com/@Apple (product films, minimal type, hero shots)
- Marques Brownlee: https://www.youtube.com/@mkbhd (crisp tech reviews and Shorts)
- Notion: https://www.youtube.com/@Notion and Figma: https://www.youtube.com/@figma (software demos with screen recordings)

**Motion graphics**
- Kurzgesagt: https://www.youtube.com/@kurzgesagt (flat illustrated explainers)
- Vox: https://www.youtube.com/@Vox (explainers with charts, maps and archival collage)
- School of Motion: https://www.youtube.com/@SchoolofMotion (the craft of motion design)
