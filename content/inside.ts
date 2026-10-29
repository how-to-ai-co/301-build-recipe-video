// Everything in the repo, for the "What's inside" page. Keep in step with the folders.
export const REPO = "https://github.com/how-to-ai-co/301-build-recipe-video";
export const tree = (path: string) => `${REPO}/tree/main/${path}`;
export const blob = (path: string) => `${REPO}/blob/main/${path}`;

export type Item = { name: string; path: string; what: string; cost?: "free" | "paid" | "mac" };
export type Section = { id: string; title: string; intro: string; folder?: string; items: Item[] };

export const prompt = [
  { t: "Asks you everything up front", d: "What you're making, where it goes, a video you like, your footage, the message, your website, voice and music. Then it stops asking." },
  { t: "Sets up the engine", d: "Clones this repo to Documents/video-engine and installs only what your video needs. You only open Terminal if an installer needs your Mac password." },
  { t: "Learns your brand", d: "Takes your colours, fonts and logo from your website and shows you a one-table summary to correct." },
  { t: "Studies your reference video", d: "Downloads it, measures pacing and cuts, makes a contact sheet and tells you what makes it work. It borrows the style, never the footage." },
  { t: "Plans the edit with you", d: "For a talking head: every line with its timestamp, the proposed cut and overlay. For a graphic: what is on screen, second by second. You approve before anything renders." },
  { t: "Builds a draft and checks it first", d: "Renders fast at 720p, looks at its own frames against the design rules and your saved rules, and fixes what fails before you see it." },
  { t: "Turns your notes into rules", d: "Fixes this video, and saves the notes that should apply to every video as yes/no rules for next time." },
  { t: "Exports and hands off", d: "Full quality in the right shape, a delivery check, the file opened for you, and a prompt to pick up where you left off." },
];

export const sections: Section[] = [
  {
    id: "skills", title: "Skills Claude loads on its own", folder: ".claude/skills",
    intro: "Open the folder in Claude Code and these switch on by themselves when the task fits.",
    items: [
      { name: "video-edit", path: ".claude/skills/video-edit/SKILL.md", what: "Reads your saved edit rules before every plan or render, and checks each draft against them yes or no." },
      { name: "refine-video-edit", path: ".claude/skills/refine-video-edit/SKILL.md", what: "Turns your notes on a draft into dated yes/no rules. Reusable notes become rules; one-off fixes stay with that video." },
      { name: "Your edit rules", path: ".claude/skills/video-edit/references/edit-rules.md", what: "The rules file itself, with starter rules for pacing, text, overlays, audio, captions, look and delivery. Delete any you disagree with." },
      { name: "reference-video", path: ".claude/skills/reference-video/SKILL.md", what: "Paste an Instagram, TikTok or YouTube link and say \"make mine like this.\" Claude breaks the style down and applies it to your footage." },
      { name: "yap-video-plan", path: ".claude/skills/yap-video-plan/SKILL.md", what: "Plans a talking-head edit: the full script with times, proposed cuts and overlays, title and playback speed." },
      { name: "visual-hooks-overlays", path: ".claude/skills/visual-hooks-overlays/SKILL.md", what: "Picks what goes on screen and makes the overlays in one shared look." },
      { name: "overlay-timing", path: ".claude/skills/overlay-timing/SKILL.md", what: "Times each overlay to the exact spoken word, with enough time to read it." },
      { name: "yap-cover-image", path: ".claude/skills/yap-cover-image/SKILL.md", what: "Makes a 9:16 cover image for every finished video and checks it at thumbnail size." },
      { name: "caption", path: ".claude/skills/caption/SKILL.md", what: "Writes the post caption in your voice, and learns from the ones you approve." },
    ],
  },
  {
    id: "formats", title: "Videos it can make", folder: "parts",
    intro: "Each format has a deep guide Claude reads when you pick it.",
    items: [
      { name: "Talking head (Yap)", path: "recipes/yap.md", what: "Cuts the silences and stumbles, speeds the take up a little, cleans the audio, adds a title hook and drops in overlays as you say the matching word.", cost: "free" },
      { name: "Creator clips", path: "parts/45-creator-clips.md", what: "Your footage with a hook and word-synced captions burned on, trimmed and joined. No editing software.", cost: "free" },
      { name: "Words on screen (OneWord)", path: "parts/20-format-rsvp.md", what: "One word at a time on a dark screen, timed to your voice. No footage needed.", cost: "free" },
      { name: "Captions over artwork (Cards)", path: "parts/30-format-captions.md", what: "Captions over your own graphics, with hard cuts.", cost: "free" },
      { name: "Aerial mood piece", path: "parts/40-format-aerial.md", what: "A 9-second silent landscape clip with a text block and your logo. Free with your own clip; generating the clip costs money.", cost: "free" },
      { name: "Motion graphics", path: "motion-studio/README.md", what: "Animated logos, stats that count up, charts that draw themselves, short explainers. Written in code and exported to MP4.", cost: "free" },
      { name: "Dialogue scenes with actors", path: "parts/60-format-kling-dialogue.md", what: "The Kling setup and the full record of one finished acted film. The most expensive job by far.", cost: "paid" },
    ],
  },
  {
    id: "tools", title: "Editing tools", folder: "engine/scripts",
    intro: "Python scripts Claude runs for you. You never need to type these.",
    items: [
      { name: "yap.py", path: "engine/scripts/yap.py", what: "The whole talking-head edit in one script: cut stumbles, flash a logo, hold a chart, swap the title for a call to action, render.", cost: "free" },
      { name: "yap_islands.py", path: "engine/scripts/yap_islands.py", what: "The zero-gap trim: finds every bit of sound and lists the ums, breaths and clicks so they can go.", cost: "free" },
      { name: "clip.py", path: "engine/scripts/clip.py", what: "Frame-accurate trims, and joins clips with hard cuts only.", cost: "free" },
      { name: "overlay.py", path: "engine/scripts/overlay.py", what: "Burns a hook onto a video, transcribes the speech and burns on synced captions.", cost: "free" },
      { name: "reference.py", path: "engine/scripts/reference.py", what: "Downloads a reference video and measures it: length, cuts per second, shot length, loudness, a contact sheet and a style breakdown.", cost: "free" },
      { name: "grade.py", path: "engine/scripts/grade.py", what: "The realism pass. Takes the too-clean AI shine off with lower contrast, softer colour and moving film grain.", cost: "free" },
      { name: "render_aerial.py", path: "engine/scripts/render_aerial.py", what: "Burns a text block and your logo onto a landscape clip.", cost: "free" },
      { name: "cutout and cutout-person", path: "engine/bin", what: "Removes an image background with the Mac's built-in tools. Free, no API.", cost: "mac" },
      { name: "Remotion compositions", path: "engine/src", what: "The code that draws OneWord, Cards, the app-bundling animation, a battery graphic and an explainer, in 9:16 and 4:5.", cost: "free" },
    ],
  },
  {
    id: "sound", title: "Sound", folder: "engine/scripts",
    intro: "Voice, music and loudness, mostly free.",
    items: [
      { name: "timings.py", path: "engine/scripts/timings.py", what: "Turns a voiceover into word-by-word timings with Whisper, so text lands on the word.", cost: "free" },
      { name: "prosody.py", path: "engine/scripts/prosody.py", what: "Flags uptalk, where a sentence rises like a question when it should fall.", cost: "free" },
      { name: "bed.py", path: "engine/scripts/bed.py", what: "Composes an original music bed that loops cleanly. You own it outright.", cost: "free" },
      { name: "Yap audio recipe", path: "recipes/yap-audio.md", what: "Noise cleanup and levelling to Instagram's loudness (-14 LUFS).", cost: "free" },
      { name: "Voice and music guide", path: "parts/10-voice-and-music.md", what: "Recording your own voice, generated voices and how to match a track's mood without using the track.", cost: "free" },
    ],
  },
  {
    id: "generation", title: "AI generation (optional, costs money)", folder: "engine/scripts",
    intro: "Nothing here runs without your yes. Claude names the service, what it makes and the price first.",
    items: [
      { name: "fal.py", path: "engine/scripts/fal.py", what: "Voices, talking people, lip sync, video cutouts and stills from one fal key. Dry run until you add --go.", cost: "paid" },
      { name: "generate.py", path: "engine/scripts/generate.py", what: "Footage and stills on Replicate (Seedance, Veo, Kling, Nano Banana). Shows the price before spending.", cost: "paid" },
      { name: "fal guide", path: "parts/55-generation-fal.md", what: "The first key to get, and what it covers.", cost: "paid" },
      { name: "Replicate guide", path: "parts/50-generation-replicate.md", what: "Footage, stills and character sheets, with the full record of what worked.", cost: "paid" },
      { name: "Keys and accounts", path: "parts/00-keys-and-accounts.md", what: "Signing up, where each key goes (engine/.env) and the traps, like credits that expire.", cost: "paid" },
    ],
  },
  {
    id: "rules", title: "Rulebooks and styles", folder: "recipes",
    intro: "How a good edit is judged. The Yap rules are a worked example from one creator's real feedback.",
    items: [
      { name: "Yap formula", path: "recipes/yap.md", what: "The main rulebook: titles of three words or fewer, the screen changing about every second, real headlines and charts instead of text labels, drafts at 720p and finals at 1080p." },
      { name: "Release check", path: "recipes/yap-release-check.md", what: "Two gates: approve the image picks before rendering, then a fresh-eyes check of the draft. Every past note is a yes/no line." },
      { name: "Flash overlays", path: "recipes/flash-overlays.md", what: "How overlays flash in on the spoken word." },
      { name: "Yap Depth", path: "styles/yap-depth/STYLE.md", what: "Title on screen, your original framing, big overlays behind your head." },
      { name: "Oren Static Hooks", path: "styles/oren-static-hooks/STYLE.md", what: "Large objects on either side of your head." },
      { name: "Editorial Tech", path: "styles/editorial-tech/STYLE.md", what: "Punch-in zooms, an italic hook, dark full-screen explainer animations." },
      { name: "Mad Libs templates", path: "parts/95-madlibs-templates.md", what: "Take the structure of an ad you liked and fill in your own content." },
      { name: "Make it your own", path: "parts/90-make-it-your-own.md", what: "Changing the look to your brand, and adding a new format." },
    ],
  },
  {
    id: "motion", title: "Motion studio", folder: "motion-studio",
    intro: "Claude can't film. It writes a page that can draw any moment in time, then turns every moment into a frame.",
    items: [
      { name: "No-install version", path: "motion-studio/browser/motion.html", what: "One file in Chrome with Play, Contact sheet and Export MP4. Tested: frame-exact MP4 with sound, in four shapes.", cost: "free" },
      { name: "Node version", path: "motion-studio/node", what: "Renders every frame with a headless browser and joins them with ffmpeg. One npm install. Motion blur and a generated score.", cost: "free" },
      { name: "Build guides", path: "motion-studio/README.md", what: "Which version to pick, the critique loop (contact sheet, critique, fix, export) and the house rules." },
      { name: "Example showreel", path: "motion-studio/node/examples/showreel.html", what: "A 7-shot, 15-second reel to see the quality bar." },
    ],
  },
  {
    id: "references", title: "Curated references", folder: "references",
    intro: "What Claude reads so your video doesn't look generic. Checked 29 October 2026.",
    items: [
      { name: "Design rules", path: "references/design-rules.md", what: "Type sizes, colour, timing and easing, safe zones, the looks that give away AI, animated charts, audio levels and a pre-export checklist." },
      { name: "Animation library guide", path: "references/library-guide.md", what: "Remotion, HyperFrames, Motion Canvas, GSAP, Lottie, Rive, Three.js, p5.js, WebCodecs, Whisper and more, plus ten ffmpeg recipes and an \"I want X, use Y\" table." },
      { name: "AI video generation guide", path: "references/video-generation.md", what: "fal, Replicate, Kling, Higgsfield, Veo, Seedance, Runway, Luma, ElevenLabs and image models: what each is for, how it connects and what it costs." },
      { name: "Reference videos", path: "references/videos/README.md", what: "Where breakdowns of videos you like are saved, plus channels worth studying." },
      { name: "Instagram safe zone", path: "instagram-safe-zone.md", what: "Where text gets covered by the app's buttons, with a reference image." },
    ],
  },
  {
    id: "review", title: "Review and delivery", folder: "review-panel",
    intro: "Optional, for people making videos every week.",
    items: [
      { name: "Review panel", path: "review-panel/README.md", what: "A local page that finds new drafts on its own. Pin a timestamp, leave notes, trim on a waveform, preview one scene, approve." },
      { name: "deliver.py", path: "engine/scripts/deliver.py", what: "Checks file names, leftover placeholders and missing captions before anything ships." },
      { name: "ship_cleanup.py", path: "engine/scripts/ship_cleanup.py", what: "Moves a shipped video's working files to the Trash. Never deletes permanently." },
      { name: "Naming and delivery", path: "parts/80-naming-and-delivery.md", what: "How finished files are named and filed." },
      { name: "Playbook and failure log", path: "parts/70-playbook-and-failures.md", what: "Every line is a mistake someone already paid for." },
    ],
  },
  {
    id: "brand", title: "Brand", folder: "examples/doranalytics",
    intro: "Your brand lives in one file, engine/src/brand.mjs. Claude fills it in from your website.",
    items: [
      { name: "Brand file", path: "engine/src/brand.mjs", what: "Name, colours, fonts, logo, call to action and words you never use." },
      { name: "Example brand book", path: "examples/doranalytics/BRAND-GUIDELINES.md", what: "A finished brand to show the shape: palettes, font pairings, chart styles and CSS tokens." },
      { name: "Example brand strategy", path: "examples/doranalytics/BRAND-STRATEGY.md", what: "Purpose, audiences, content pillars and the check every piece has to pass." },
    ],
  },
];

export const notIncluded = [
  "The full cinematic film workflow. It is built on a paid third-party guide, so it stays private.",
  "Other people's footage, music or logos. Reference videos are for studying style and stay out of git.",
  "API keys. Paid services use your own keys in engine/.env, which is never committed.",
];
