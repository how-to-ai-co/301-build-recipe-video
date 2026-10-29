// Everything in the repo, packaged for the "What's inside" page. Keep in step with the folders.
export const REPO = "https://github.com/how-to-ai-co/301-build-recipe-video";
export const tree = (path: string) => `${REPO}/tree/main/${path}`;
export const blob = (path: string) => `${REPO}/blob/main/${path}`;
export const repoLink = (path: string) => (/\.[a-z]+$/.test(path) ? blob(path) : tree(path));

export type Icon =
  | "Brain" | "Clapperboard" | "Scissors" | "AudioWaveform" | "Shapes" | "Palette" | "Library"
  | "ListChecks" | "Paintbrush" | "Sparkles" | "Repeat" | "ScanEye" | "Mic" | "Smartphone";
export type Cost = "free" | "paid" | "mac";
export type Feature = { title: string; what: string; path: string; cost?: Cost };
export type Pack = { id: string; name: string; tagline: string; icon: Icon; tone: string; folder: string; features: Feature[] };
export type Headliner = { title: string; pitch: string; icon: Icon; tone: string; viz: "learn" | "study" | "cut" | "motion"; path: string };

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

export const headliners: Headliner[] = [
  {
    title: "An editor that learns your taste", icon: "Repeat", tone: "orange", path: ".claude/skills/refine-video-edit/SKILL.md",
    pitch: "Say \"bigger title\" once. Every note you give becomes a saved rule, so the next video starts where the last one finished.",
    viz: "learn",
  },
  {
    title: "Make mine like this", icon: "ScanEye", tone: "violet", path: ".claude/skills/reference-video/SKILL.md",
    pitch: "Paste any Reel, TikTok or YouTube link. Claude measures the pacing, cuts and text, then gives your footage the same feel.",
    viz: "study",
  },
  {
    title: "Talking-head editor", icon: "Mic", tone: "teal", path: "recipes/yap.md",
    pitch: "Drop in a raw take from your phone. Out comes a tight, captioned, Instagram-ready video with a title hook and overlays.",
    viz: "cut",
  },
  {
    title: "Motion graphics studio", icon: "Shapes", tone: "blue", path: "motion-studio/README.md",
    pitch: "Animated logos, stats that count up, charts that draw themselves. Claude designs them in code and exports a real MP4.",
    viz: "motion",
  },
];

export const packs: Pack[] = [
  {
    id: "skills", name: "Smart Skills", icon: "Brain", tone: "orange", folder: ".claude/skills",
    tagline: "Nine skills that switch on by themselves when you open the folder.",
    features: [
      { title: "Edits that remember", what: "Reads your saved rules before every plan and checks each draft against them.", path: ".claude/skills/video-edit/SKILL.md" },
      { title: "Notes into rules", what: "Turns your feedback into dated rules. One-off fixes stay with that video.", path: ".claude/skills/refine-video-edit/SKILL.md" },
      { title: "Your personal rulebook", what: "Starter rules for pacing, text, audio and look. Keep, change or delete any.", path: ".claude/skills/video-edit/references/edit-rules.md" },
      { title: "Style decoder", what: "Breaks down any video you love and applies it to yours.", path: ".claude/skills/reference-video/SKILL.md" },
      { title: "Edit planner", what: "Every line with its timestamp, the proposed cut, the overlay, the title and speed.", path: ".claude/skills/yap-video-plan/SKILL.md" },
      { title: "Overlay designer", what: "Picks what goes on screen and makes it all in one look.", path: ".claude/skills/visual-hooks-overlays/SKILL.md" },
      { title: "Word-perfect timing", what: "Lands each overlay on the exact spoken word, held long enough to read.", path: ".claude/skills/overlay-timing/SKILL.md" },
      { title: "Cover maker", what: "A 9:16 cover for every video, checked at thumbnail size.", path: ".claude/skills/yap-cover-image/SKILL.md" },
      { title: "Caption writer", what: "Writes the post caption in your voice and learns from the ones you approve.", path: ".claude/skills/caption/SKILL.md" },
    ],
  },
  {
    id: "formats", name: "Format Library", icon: "Clapperboard", tone: "teal", folder: "parts",
    tagline: "Seven ready-made video formats, each with its own playbook.",
    features: [
      { title: "Talking head", what: "Tight cuts, a title hook and overlays on the word.", path: "recipes/yap.md", cost: "free" },
      { title: "Creator clips", what: "Your footage with a hook and synced captions. No editing app.", path: "parts/45-creator-clips.md", cost: "free" },
      { title: "One word at a time", what: "Kinetic text timed to your voice. No footage needed.", path: "parts/20-format-rsvp.md", cost: "free" },
      { title: "Captions over artwork", what: "Your graphics with captions and hard cuts.", path: "parts/30-format-captions.md", cost: "free" },
      { title: "Aerial mood piece", what: "A 9-second landscape with your words and logo. Works with the sound off.", path: "parts/40-format-aerial.md", cost: "free" },
      { title: "Motion graphics", what: "Logos, stats, charts and explainers, exported to MP4.", path: "motion-studio/README.md", cost: "free" },
      { title: "Scenes with actors", what: "The Kling setup and the record of one finished acted film.", path: "parts/60-format-kling-dialogue.md", cost: "paid" },
    ],
  },
  {
    id: "editing", name: "Editing Suite", icon: "Scissors", tone: "violet", folder: "engine/scripts",
    tagline: "The edit bay, run for you. You never type a command.",
    features: [
      { title: "One-script talking-head edit", what: "Cut stumbles, flash a logo, hold a chart, swap in a call to action, render.", path: "engine/scripts/yap.py", cost: "free" },
      { title: "Zero-gap trim", what: "Finds every um, breath and click so the take is just words.", path: "engine/scripts/yap_islands.py", cost: "free" },
      { title: "Frame-perfect cuts", what: "Trims to the frame and joins clips with clean hard cuts.", path: "engine/scripts/clip.py", cost: "free" },
      { title: "Hooks and captions", what: "Burns on a hook and word-synced captions from your speech.", path: "engine/scripts/overlay.py", cost: "free" },
      { title: "Film-look grade", what: "Takes the too-clean AI shine off with grain and softer colour.", path: "engine/scripts/grade.py", cost: "free" },
      { title: "Reference analyser", what: "Measures any video: cuts, shot length, loudness, contact sheet.", path: "engine/scripts/reference.py", cost: "free" },
      { title: "One-click cutouts", what: "Removes a background with the Mac's built-in tools. No API.", path: "engine/bin", cost: "mac" },
      { title: "Animation components", what: "App logos flying into a chat box, a battery graphic, an explainer.", path: "engine/src", cost: "free" },
    ],
  },
  {
    id: "sound", name: "Sound Studio", icon: "AudioWaveform", tone: "blue", folder: "engine/scripts",
    tagline: "Voice, music and levels, without a licence in sight.",
    features: [
      { title: "Original music beds", what: "Composed on your machine, loops cleanly, yours outright.", path: "engine/scripts/bed.py", cost: "free" },
      { title: "Word-by-word timing", what: "Whisper times every word so text lands on the beat.", path: "engine/scripts/timings.py", cost: "free" },
      { title: "Delivery coach", what: "Flags sentences that rise like a question when they should land.", path: "engine/scripts/prosody.py", cost: "free" },
      { title: "Instagram-ready audio", what: "Noise cleanup and levelling to -14 LUFS.", path: "recipes/yap-audio.md", cost: "free" },
      { title: "Voice and music guide", what: "Record yourself, generate a voice, or match a track's mood.", path: "parts/10-voice-and-music.md", cost: "free" },
    ],
  },
  {
    id: "motion", name: "Motion Studio", icon: "Shapes", tone: "orange", folder: "motion-studio",
    tagline: "Claude can't film, so it draws every frame in code.",
    features: [
      { title: "No-install studio", what: "One file in Chrome: Play, Contact sheet, Export MP4.", path: "motion-studio/browser/motion.html", cost: "free" },
      { title: "Pro renderer", what: "Every frame rendered with motion blur and a generated score.", path: "motion-studio/node", cost: "free" },
      { title: "Critique loop", what: "Claude reviews a contact sheet of its own frames before you see it.", path: "motion-studio/README.md" },
      { title: "15-second showreel", what: "A 7-shot example to see the quality bar.", path: "motion-studio/node/examples/showreel.html" },
    ],
  },
  {
    id: "styles", name: "Style Vault", icon: "Palette", tone: "teal", folder: "styles",
    tagline: "Proven looks and rulebooks, built from real edits.",
    features: [
      { title: "The Yap formula", what: "The rulebook behind dozens of real edits: short titles, constant motion, real proof.", path: "recipes/yap.md" },
      { title: "Two-gate release check", what: "Approve the images before render, then a fresh-eyes check of the draft.", path: "recipes/yap-release-check.md" },
      { title: "Yap Depth", what: "Big overlays behind your head, title on screen.", path: "styles/yap-depth/STYLE.md" },
      { title: "Static Hooks", what: "Bold objects either side of your head.", path: "styles/oren-static-hooks/STYLE.md" },
      { title: "Editorial Tech", what: "Punch-in zooms, an italic hook, dark explainer cutaways.", path: "styles/editorial-tech/STYLE.md" },
      { title: "Mad Libs templates", what: "Take an ad that worked and fill in yours.", path: "parts/95-madlibs-templates.md" },
    ],
  },
  {
    id: "library", name: "Designer's Library", icon: "Library", tone: "violet", folder: "references",
    tagline: "What Claude reads so your video never looks generic. Checked October 2026.",
    features: [
      { title: "Design rules", what: "Type, colour, timing, safe zones, and the looks that give away AI.", path: "references/design-rules.md" },
      { title: "Animation toolkit guide", what: "Remotion, GSAP, Lottie, Rive, Three.js and more, plus ten ffmpeg recipes.", path: "references/library-guide.md" },
      { title: "AI video buyer's guide", what: "fal, Replicate, Kling, Veo, Runway, Luma: what each does and costs.", path: "references/video-generation.md" },
      { title: "Reference board", what: "Your saved breakdowns plus channels worth studying.", path: "references/videos/README.md" },
      { title: "Instagram safe zone", what: "Where the app's buttons cover your text, with a template.", path: "instagram-safe-zone.md" },
    ],
  },
  {
    id: "review", name: "Review Room", icon: "ListChecks", tone: "blue", folder: "review-panel",
    tagline: "For when you're making videos every week.",
    features: [
      { title: "Review panel", what: "Pin notes to timestamps, trim on a waveform, approve.", path: "review-panel/README.md" },
      { title: "Delivery gate", what: "Catches bad file names, placeholders and missing captions.", path: "engine/scripts/deliver.py" },
      { title: "Auto-tidy", what: "Moves a shipped video's working files to the Trash. Never deletes.", path: "engine/scripts/ship_cleanup.py" },
      { title: "Failure log", what: "Every line is a mistake someone already paid for.", path: "parts/70-playbook-and-failures.md" },
      { title: "Naming and filing", what: "How finished files are named and handed off.", path: "parts/80-naming-and-delivery.md" },
    ],
  },
  {
    id: "brand", name: "Brand Kit", icon: "Paintbrush", tone: "orange", folder: "examples/doranalytics",
    tagline: "Your look in one file, filled in from your website.",
    features: [
      { title: "One brand file", what: "Name, colours, fonts, logo, call to action, banned words.", path: "engine/src/brand.mjs" },
      { title: "Example brand book", what: "A finished one to copy the shape of: palettes, fonts, chart styles.", path: "examples/doranalytics/BRAND-GUIDELINES.md" },
      { title: "Example brand strategy", what: "Purpose, audiences, pillars and a check every piece must pass.", path: "examples/doranalytics/BRAND-STRATEGY.md" },
    ],
  },
  {
    id: "generation", name: "AI Generation Add-on", icon: "Sparkles", tone: "violet", folder: "engine/scripts",
    tagline: "Optional. Pay as you go, and nothing runs without your yes.",
    features: [
      { title: "AI voices and lip sync", what: "Voices, talking people and cutouts from one fal key.", path: "engine/scripts/fal.py", cost: "paid" },
      { title: "AI footage and stills", what: "Seedance, Veo, Kling and more on Replicate, priced first.", path: "engine/scripts/generate.py", cost: "paid" },
      { title: "Generation playbooks", what: "What worked, what didn't, and what it cost.", path: "parts/55-generation-fal.md", cost: "paid" },
      { title: "Keys without the traps", what: "Sign-up, where each key goes, credits that expire.", path: "parts/00-keys-and-accounts.md", cost: "paid" },
    ],
  },
];

export const totalFeatures = packs.reduce((n, p) => n + p.features.length, 0);

export const notIncluded = [
  "The full cinematic film workflow. It is built on a paid third-party guide, so it stays private.",
  "Other people's footage, music or logos. Reference videos are for studying style and stay out of git.",
  "API keys. Paid services use your own keys in engine/.env, which is never committed.",
];
