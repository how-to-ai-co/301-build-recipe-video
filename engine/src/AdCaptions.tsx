import React from "react";
import {
  AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";
import { Theme } from "./theme";
import { BRAND, DARK, PAPER } from "./brand.mjs";

/**
 * Format 2 — captions over artwork.
 *
 * ONE component for every cut in the 401-404, 411-414 and 421-424 waves. In the
 * original tree this was five near-identical files (Ad.tsx, AdFounder.tsx,
 * AdIndividual.tsx, AdBoss.tsx, AdPaid.tsx). Everything they did differently is
 * a config field here.
 *
 * The shape of every cut, in order:
 *
 *   0        -> hookEnd   hook card: the whole opening line, full frame,
 *                         nothing competing with it
 *   hookEnd  -> bodyEnd   artwork + burned-in captions. HARD CUTS ONLY between
 *                         scenes: no Ken Burns, no crossfades, nothing moves
 *                         inside a scene
 *   bodyEnd  -> voEnd     PAID only: the two-column offer ledger. Captions keep
 *                         running over it
 *   voEnd    -> end       end card
 *
 * FREE cuts set offer:"free" and simply have no ledger; bodyEnd == voEnd.
 */

export const FPS = 30;

export type Word = { w: string; s: number; e: number };

/** Theme is named, not embedded. Remotion serialises defaultProps to JSON, so
 *  an embedded theme object arrives as a fresh object and identity comparisons
 *  (`th === PAPER`) silently fail. The original code worked around that by
 *  comparing `th.bg === PAPER.bg`; naming the theme removes the class of bug,
 *  and it also lets the config list live in plain .mjs. */
export type ThemeName = "dark" | "paper";
const THEMES: Record<ThemeName, Theme> = { dark: DARK, paper: PAPER };

/** Scrim under the caption band so dense infographics never bleed through.
 *  The two gradients differ in stop positions AND final alpha; both are
 *  byte-identical to what shipped. */
const SCRIM: Record<ThemeName, string> = {
  dark: "linear-gradient(to bottom, rgba(18,16,14,0) 58%, rgba(18,16,14,0.97) 70%)",
  paper: "linear-gradient(to bottom, rgba(247,245,241,0) 56%, rgba(247,245,241,1) 68%)",
};

/** Logo chips are light on both themes. The set mixes monochrome and full
 *  colour marks and Google is multicolour, so dropped straight onto the dark
 *  theme half of them vanish. */
const CHIP: Record<ThemeName, string> = { dark: "#F4F1EB", paper: "#FFFFFF" };

const SERIF = BRAND.serif;
const SANS = BRAND.sansCards;   // see the note in brand.mjs

const FRAME_W = 980;
const FRAME_H = 1240;
const ART_ASPECT = 1.25;   // the infographics are all 1280x1600

/**
 * Logos shown on the PAID offer scene, revealed one by one. Ships empty; an
 * empty list renders nothing. Add SVGs to public/logos/ and list them here.
 *
 * Each logo sits in a light chip at a uniform size. Chips are how real partner
 * walls solve the mixed-colour problem and they work unchanged on both themes.
 *
 * Two rules that came from expensive mistakes:
 *   - Screen every SVG for scripts and external references BEFORE committing.
 *   - Only list what your live offer page actually includes, checked against
 *     that page, not against an older ad. A partner with no logo asset should
 *     render as a name, never silently vanish: a true name beats a false logo.
 */
export const TOOLS: { name: string; file: string }[] = [];

export type Scene = {
  img: string;
  /** 1 = the whole artwork across the frame. Above 1 is a static punch-in.
   *  Nothing animates: the zoom is chosen per scene and held. */
  zoom?: number;
  /** Horizontal centre of interest, 0 = left edge of the artwork, 1 = right.
   *  If your artwork's text runs to an edge, focus flush to that edge — any
   *  other alignment slices words. Losing the side of an illustration reads as
   *  a crop; losing text reads as a bug. */
  focusX?: number;
  /** Vertical centre of interest, 0 = top of the artwork, 1 = bottom. */
  focusY?: number;
  /** Dark artwork on the paper layout. Inset it as a framed card so it reads as
   *  a deliberate insert rather than a hole punched in the page. No shipped ad
   *  uses this; the rule behind it is still real. */
  inset?: boolean;
  /** "crop" (default) lays the artwork out at `zoom` and clips whatever leaves
   *  the box. "contain" scales the whole image to fit, ignoring zoom/focus —
   *  that is what 401 and 402 shipped with. */
  fit?: "crop" | "contain";
  /** Height of the artwork box. 1240 everywhere except 401, which shipped with
   *  1280 and therefore sits about 20px lower than every other ad. */
  boxH?: number;
  /** height / width of the ARTWORK ITSELF, used only to place the focus point.
   *  Every shipped ad assumes 1.25, which is right for the 1280x1600
   *  infographics and wrong for ikea.png (978x1348) and nelly.png (2000x1969).
   *  Leaving it unset reproduces the shipped renders, mistakes included. */
  aspect?: number;
  from: number;
  to: number;
};

export type CaptionConfig = {
  /** "free" ends after the body and uses the free end card. "paid" appends the
   *  shared offer ledger between bodyEnd and voEnd. Default "free".
   *
   *  !! THE DEFAULT IS INVERTED FROM THE ORIGINAL. AdPaid tested
   *  `c.offer !== "free"` (AdPaid.tsx:270) and `c.offer === "free" ? 3.2 : 3.6`
   *  (AdPaid.tsx:89), so a config that OMITTED `offer` got the paid ledger and
   *  the 3.6s card. P411-P414 in paidConfigs.ts omit it exactly like that. Port
   *  one of those verbatim and it silently becomes a FREE cut: no ledger, wrong
   *  end card, 0.4s short. Every entry in configs.mjs states `offer`
   *  explicitly for this reason. Never leave it out. */
  offer?: "free" | "paid";
  theme: ThemeName;
  /** staticFile paths, relative to public/. */
  vo: string;
  /** Make one with scripts/bed.py. Omit to render with no music. */
  bed?: string;
  /** Where the hook card gives way to artwork. */
  hookEnd: number;
  /** Regex SOURCE, not a RegExp: defaultProps are JSON-serialised by Remotion
   *  and a RegExp arrives at the component as an empty object. */
  hookAccent: string;
  hookAccentFlags?: string;
  /** Hook type size. Set it by eye against the rendered card; there is no
   *  formula and no auto-fit. 84-108 across the account. */
  hookSize: number;
  /** 1.12 default. 401, 402 and 403 FREE shipped at 1.1. */
  hookLineHeight?: number;
  /** How far past hookEnd a word may end and still appear on the hook card.
   *  0.35 default; 402 FREE shipped 0.30 (no visible difference — no word in
   *  either founder timing file ends inside that 50ms window). */
  hookLead?: number;
  scenes: Scene[];
  /** Where the body VO stops and the shared offer outro starts. Omit on free
   *  cuts; it defaults to voEnd. */
  bodyEnd?: number;
  /** Where ALL speech stops. Derived from the timings file, never guessed.
   *  On PAID cuts it is exactly last-word-end + 0.22 and build_paid.py prints
   *  it. On FREE cuts it was set by hand and is NOT uniform: 401 V1/V2 and
   *  402 V1/V2 set it exactly equal to the last word's end; 403, 404 and
   *  421-424 add 0.16-0.24. timings.py prints the last word's end, not voEnd —
   *  read that number and add the padding yourself. */
  voEnd: number;
  /** "large" is the 401-404 FREE end card, "compact" is everything built
   *  through AdPaid (411-414 and all of 421-424). Default "compact". */
  endCard?: "large" | "compact";
  /** Override the end card hold. Default 3.6s on paid, 3.2s on free. */
  endCardSeconds?: number;
};

/** 3.6s on paid, 3.2s on free — the two END_CARD constants from the original
 *  files (AdPaid.tsx:18 vs Ad/AdFounder/AdIndividual/AdBoss :5-8). See the
 *  inverted-default warning on `offer` above: the original AdPaid gave 3.6s to
 *  any config that did not say "free". */
export const durationOf = (c: CaptionConfig) =>
  c.voEnd + (c.endCardSeconds ?? (c.offer === "paid" ? 3.6 : 3.2));

/** Place a focus point at the centre of the frame, but never past the artwork's
 *  own edge — otherwise a punch-in slices the title off the top or the
 *  descriptions off the right, which is exactly what it did the first time. */
const offset = (frame: number, img: number, focus: number) =>
  img <= frame ? (frame - img) / 2
    : Math.max(frame - img, Math.min(0, frame / 2 - img * focus));

const Frame: React.FC<{ scene: Scene; accent: string }> = ({ scene, accent }) => {
  const boxH = scene.boxH ?? FRAME_H;
  const inset = scene.inset === true;
  const pad = inset ? 26 : 0;

  const box: React.CSSProperties = {
    width: FRAME_W, height: boxH, overflow: "hidden", position: "relative",
    padding: pad,
    background: inset ? "#0E0C0A" : "transparent",
    borderRadius: inset ? 18 : 0,
    border: inset ? `3px solid ${accent}` : "none",
    boxShadow: inset ? "0 18px 60px rgba(0,0,0,0.28)" : "none",
    boxSizing: "border-box",
  };

  if ((scene.fit ?? "crop") === "contain") {
    return (
      <div style={box}>
        <Img src={staticFile(scene.img)}
             style={{ width: "100%", height: "100%", objectFit: "contain" }} />
      </div>
    );
  }

  const innerW = FRAME_W - pad * 2;
  const innerH = boxH - pad * 2;
  const w = innerW * (scene.zoom ?? 1);
  const h = w * (scene.aspect ?? ART_ASPECT);
  return (
    <div style={box}>
      <Img src={staticFile(scene.img)} style={{
        position: "absolute", width: w,
        left: pad + offset(innerW, w, scene.focusX ?? 0.5),
        top: pad + offset(innerH, h, scene.focusY ?? 0.5),
      }} />
    </div>
  );
};

/**
 * The offer as a two-column ledger: what is free on the left, what the paid
 * community adds on the right.
 *
 * The split is the point. An earlier version listed everything together, which
 * left the free/paid boundary to the voiceover alone and lost it entirely with
 * the sound off. Most of Meta plays muted, so the screen has to carry it.
 */
const OutroCard: React.FC<{ theme: ThemeName; t: number; split: number }> = ({
  theme, t, split,
}) => {
  const th = THEMES[theme];
  const shown = Math.min(TOOLS.length, Math.max(0, Math.floor((t - split) / 0.24) + 2));
  const freeRows = ["Every article", "Every week", "Forever"];

  return (
    <div style={{
      width: FRAME_W, height: FRAME_H, display: "flex", flexDirection: "column",
      justifyContent: "center", gap: 34, paddingTop: 40,
    }}>
      <div style={{ display: "flex", gap: 34 }}>
        {/* FREE */}
        <div style={{ flex: "0 0 320px" }}>
          <div style={{
            fontFamily: SANS, fontSize: 26, letterSpacing: "0.18em",
            textTransform: "uppercase", color: th.muted, marginBottom: 26,
          }}>Free</div>
          {freeRows.map((r) => (
            <div key={r} style={{
              fontFamily: SERIF, fontSize: 48, lineHeight: 1.62, color: th.ink,
            }}>{r}</div>
          ))}
        </div>

        <div style={{ width: 2, background: th.muted, opacity: 0.35 }} />

        {/* COMMUNITY */}
        <div style={{ flex: 1 }}>
          <div style={{
            fontFamily: SANS, fontSize: 26, letterSpacing: "0.18em",
            textTransform: "uppercase", color: th.accent, marginBottom: 26,
          }}>Community · paid</div>
          <div style={{
            display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14, marginBottom: 26,
          }}>
            {TOOLS.map((tool, i) => (
              <div key={tool.name} style={{
                background: CHIP[theme], borderRadius: 14, height: 132,
                display: "flex", alignItems: "center", justifyContent: "center",
                padding: 14, opacity: i < shown ? 1 : 0,
              }}>
                <Img src={staticFile(tool.file)}
                     style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain" }} />
              </div>
            ))}
          </div>
          {([["Live workshops", split + 2.4], ["The people doing this work", split + 3.4]] as
            [string, number][]).map(([label, at]) => (
            <div key={label} style={{
              fontFamily: SERIF, fontSize: 42, lineHeight: 1.62, color: th.ink,
              opacity: t >= at ? 1 : 0,
            }}>
              <span style={{ color: th.accent, fontWeight: 700 }}>+ </span>{label}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/** Group words into readable phrases: 4-7 words, break only on sentence ends. */
export function phrases(words: Word[]): Word[][] {
  const raw: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    const sentenceEnd = /[.!?]$/.test(w.w);
    if ((sentenceEnd && cur.length >= 3) || cur.length >= 7) {
      raw.push(cur);
      cur = [];
    }
  }
  if (cur.length) raw.push(cur);

  // whisper splits numbers like 500,000 into "500" + ",000" — glue them back
  for (const g of raw) {
    for (let i = g.length - 1; i > 0; i--) {
      if (/^[,.]\d/.test(g[i].w) || /^[%.,!?;:]+$/.test(g[i].w)) {
        g[i - 1] = { w: g[i - 1].w + g[i].w, s: g[i - 1].s, e: g[i].e };
        g.splice(i, 1);
      }
    }
  }

  // merge any stub under 3 words into its neighbour so nothing reads as a fragment
  const out: Word[][] = [];
  for (const g of raw) {
    if (g.length < 3 && out.length && out[out.length - 1].length + g.length <= 8) {
      out[out.length - 1] = out[out.length - 1].concat(g);
    } else {
      out.push(g);
    }
  }
  return out;
}

const Caption: React.FC<{ theme: ThemeName; groups: Word[][]; t: number }> = ({
  theme, groups, t,
}) => {
  const th = THEMES[theme];
  // The caption must NEVER gap. If t falls between two groups, hold the last
  // group that finished rather than rendering an empty band.
  let gi = groups.findIndex((g) => t >= g[0].s && t <= g[g.length - 1].e);
  if (gi === -1) {
    for (let i = groups.length - 1; i >= 0; i--) {
      if (t > groups[i][groups[i].length - 1].e) { gi = i; break; }
    }
    if (gi === -1) gi = 0;
  }
  const g = groups[gi];

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 250 }}>
      <div style={{
        background: th.captionBg, borderTop: `6px solid ${th.accent}`, borderRadius: 10,
        padding: "34px 46px", width: 940, display: "flex", flexWrap: "wrap",
        gap: "6px 18px", justifyContent: "center",
        boxShadow: theme === "paper" ? "0 10px 40px rgba(0,0,0,0.10)" : "none",
      }}>
        {g.map((w, i) => (
          <span key={i} style={{
            fontFamily: SERIF, fontWeight: 700, fontSize: 64, lineHeight: 1.16,
            color: t >= w.s && t <= w.e ? th.accent : th.ink,
          }}>{w.w}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const HookCard: React.FC<{ c: CaptionConfig; words: Word[]; t: number }> = ({ c, words, t }) => {
  const th = THEMES[c.theme];
  const hookWords = words.filter((w) => w.e <= c.hookEnd + (c.hookLead ?? 0.35));
  // Built fresh every frame and never given the /g flag: .test() on a global
  // regex is stateful and would accent only every other match.
  const accent = new RegExp(c.hookAccent, c.hookAccentFlags);
  return (
    <AbsoluteFill style={{ justifyContent: "center", padding: "0 84px" }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px 22px" }}>
        {hookWords.map((w, i) => (
          <span key={i} style={{
            fontFamily: SERIF, fontWeight: 700, fontSize: c.hookSize,
            lineHeight: c.hookLineHeight ?? 1.12,
            // dim until the word is spoken, so the line types itself in
            color: t >= w.s ? (accent.test(w.w) ? th.accent : th.ink) : th.dim,
          }}>{w.w}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const SIZES = {
  large: {
    gap: 22, avatar: 260, avatarGap: 18, title: 104, sub: 42,
    ctaTop: 34, ctaPad: "30px 84px", cta: 58,
    readTop: 54, readGap: 14, read: 26, wordmark: 380,
  },
  compact: {
    gap: 18, avatar: 230, avatarGap: 12, title: 98, sub: 38,
    ctaTop: 26, ctaPad: "26px 76px", cta: 54,
    readTop: 34, readGap: 12, read: 24, wordmark: 330,
  },
};

/** "READ IT ON" is #6E675E on BOTH themes in every original file — Ad.tsx:261
 *  and AdIndividual.tsx:230 hard-code it on the DARK theme even though DARK.muted
 *  is #8B8378, and AdFounder/AdBoss reach the same value through the paper MUTED.
 *  Reading th.muted here instead would lighten the dark end card and silently
 *  change 401 FREE and 403 FREE. Kept as a constant so the shipped renders
 *  reproduce. AdPaid.tsx:317 is the one exception: the compact card DOES use
 *  th.muted, so the compact dark cuts really are #8B8378. */
const READ_ON: Record<"large" | "compact", (muted: string) => string> = {
  large: () => "#6E675E",
  compact: (muted) => muted,
};

/**
 * The funnel is unchanged on both offers: the click performs the same free
 * action, and the paid cut names the upgrade as what comes next. The button
 * stays honest. Whether price ever appears on screen belongs on your
 * compliance list in brand.mjs.
 */
const EndCard: React.FC<{ c: CaptionConfig }> = ({ c }) => {
  const th = THEMES[c.theme];
  const paid = c.offer === "paid";
  const size = c.endCard ?? "compact";
  const z = SIZES[size];
  const readOn = READ_ON[size](th.muted);
  return (
    <AbsoluteFill style={{
      justifyContent: "center", alignItems: "center", flexDirection: "column", gap: z.gap,
    }}>
      {BRAND.avatar && (
        <Img src={staticFile(BRAND.avatar)} style={{
          width: z.avatar, height: z.avatar, borderRadius: z.avatar / 2,
          border: `6px solid ${th.accent}`, objectFit: "cover", marginBottom: z.avatarGap,
        }} />
      )}
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: z.title, color: th.ink }}>
        {BRAND.name}
      </div>
      <div style={{ fontFamily: SERIF, fontSize: z.sub, color: th.muted }}>
        {paid ? BRAND.paidSubline : BRAND.freeSubline}
      </div>
      <div style={{
        marginTop: z.ctaTop, background: th.accent, borderRadius: 14, padding: z.ctaPad,
        fontFamily: SERIF, fontWeight: 700, fontSize: z.cta, color: th.bg,
      }}>{BRAND.cta}</div>
      {paid && BRAND.paidFollowOn && (
        <div style={{ marginTop: 16, fontFamily: SERIF, fontSize: 38, color: th.ink }}>
          {BRAND.paidFollowOn}
        </div>
      )}
      {BRAND.platformLabel && th.wordmark && (
        <div style={{
          marginTop: z.readTop, display: "flex", flexDirection: "column",
          alignItems: "center", gap: z.readGap,
        }}>
          <div style={{
            fontFamily: SANS, fontSize: z.read, letterSpacing: "0.18em",
            textTransform: "uppercase", color: readOn,
          }}>{BRAND.platformLabel}</div>
          <Img src={staticFile(th.wordmark)} style={{ width: z.wordmark }} />
        </div>
      )}
    </AbsoluteFill>
  );
};

/** Where in the outro the logo wall stops and the extra rows begin. */
const OUTRO_SPLIT = 0.46;

export const AdCaptions: React.FC<{ words: Word[]; c: CaptionConfig }> = ({ words, c }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const th = THEMES[c.theme];
  const groups = React.useMemo(() => phrases(words), [words]);

  const bodyEnd = c.bodyEnd ?? c.voEnd;
  const inOutro = c.offer === "paid" && t >= bodyEnd && t < c.voEnd;
  const split = bodyEnd + (c.voEnd - bodyEnd) * OUTRO_SPLIT;
  const scene = c.scenes.find((s) => t >= s.from && t < s.to) ?? c.scenes[c.scenes.length - 1];

  return (
    <AbsoluteFill style={{ backgroundColor: th.bg }}>
      {/* Audio sits ABOVE the branches on purpose. In the five original
          components it was repeated inside every branch, because a frame that
          renders a branch with no <Audio> in it contributes nothing to that
          frame's audio. One tree, one copy, nothing to forget. */}
      <Audio src={staticFile(c.vo)} />
      {/* DEFECT FIX 3, measured: the documented component had a bare <Audio> for
          the bed. The licensed mp3 beds all happen to run ~0.5s longer than
          their composition, so it never bit in the original tree — but this
          bundle's own bed, scripts/bed.py's bed_phrygian.wav, is 10.0s, and a
          32.1s cut on it would play 22s of silence including the whole end
          card, which is exactly what the duck curve below exists to prevent.
          AdRsvp already loops for this reason. Sustained pads, no percussion,
          so the wrap is inaudible; verified bit-identical output on a bed that
          is longer than the composition, so this is free where it is not
          needed. */}
      {c.bed && <Audio loop src={staticFile(c.bed)} volume={(f) => {
        const tt = f / FPS;
        // music has to lift for the end card or it vanishes the moment the VO stops
        return tt < c.voEnd ? 0.16 : Math.min(0.55, 0.16 + ((tt - c.voEnd) / 0.6) * 0.39);
      }} />}

      {t < c.hookEnd ? (
        <HookCard c={c} words={words} t={t} />
      ) : t < c.voEnd ? (
        <>
          {/* artwork sits in the upper area so it never sits under the caption */}
          <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 90 }}>
            {inOutro
              ? <OutroCard theme={c.theme} t={t} split={split} />
              : <Frame scene={scene} accent={th.accent} />}
          </AbsoluteFill>
          <AbsoluteFill style={{ background: SCRIM[c.theme] }} />
          <Caption theme={c.theme} groups={groups} t={t} />
        </>
      ) : (
        <EndCard c={c} />
      )}
    </AbsoluteFill>
  );
};
