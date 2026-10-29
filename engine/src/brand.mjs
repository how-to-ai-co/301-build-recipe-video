/**
 * WHO THE ADS ARE FOR. Change this file, not the components.
 *
 * Everything the viewer reads that is not the script itself lives here: the
 * name, the end-card lines, the button, the palette, the logos. A component
 * should never contain a brand string, because the moment one does, a rebrand
 * becomes a search-and-replace across every format and somebody misses one.
 *
 * The shipped values are PLACEHOLDERS. Replace every [BRACKETED] value with
 * your brand's real one, and drop your PNGs in public/brand/. Nothing else
 * has to change.
 */

/**
 * Palette.
 *
 * The shipped colors are a neutral warm-paper starting point. When you swap
 * in your own, the two rules that actually matter are:
 *
 *   1. `bg` and `ink` need real contrast. These formats are read at arm's
 *      length on a phone, often at half brightness, frequently muted. Aim for
 *      at least 7:1. #12100E on #F7F3EC is about 15:1.
 *   2. `accent` has ONE job: mark the thing the eye should land on. In RSVP it
 *      is the recognition letter; in captions it is the word being spoken. If
 *      it does not pop against BOTH bg and ink, the format stops working. Test
 *      it before you fall in love with it.
 *
 * `dim` is for guides and inactive text, `muted` for secondary lines.
 *
 * `wordmark` is an optional PNG in public/ shown beside `platformLabel` on the
 * end card (e.g. the logo of the platform your content lives on). null hides
 * it. Provide a light-on-dark version for DARK and a dark-on-light for PAPER.
 */
export const DARK = {
  bg: "#12100E",
  ink: "#F7F3EC",
  accent: "#E4703C",
  muted: "#8B8378",
  dim: "#3A352F",
  captionBg: "rgba(18,16,14,0.94)",
  wordmark: null,
  scrimTo:
    "linear-gradient(to bottom, rgba(18,16,14,0) 58%, rgba(18,16,14,0.97) 70%)",
};

export const PAPER = {
  bg: "#F7F5F1",
  ink: "#16130F",
  accent: "#D9541F",
  muted: "#6E675E",
  dim: "#CFC9BF",
  captionBg: "#F7F5F1",
  wordmark: null,
  scrimTo:
    "linear-gradient(to bottom, rgba(247,245,241,0) 56%, rgba(247,245,241,1) 68%)",
};

/**
 * The end card, and every other fixed string a viewer sees.
 *
 * `freeSubline` and `paidSubline` differ on purpose: naming a paid offer and
 * claiming "100% free, forever" in the same frame reads as a bait and switch,
 * so a paid cut drops the free claim rather than qualifying it.
 *
 * COMPLIANCE. Write your brand's version of this list and keep it HERE, next
 * to the strings it governs. These rules are enforced nowhere in code, so they
 * are your job. The kinds of rules that belong on it, from brands that learned
 * each one the expensive way:
 *   - words the founder publicly attacks and therefore can never appear in an
 *     ad ("course" for a brand whose founder mocks course-sellers)
 *   - THE one true stat (a subscriber count, a customer count) so stale copies
 *     of it stop circulating
 *   - whether price ever appears on screen
 *   - every claim about an offer checked against the LIVE offer page before
 *     recording, never against an older ad
 */
export const BRAND = {
  name: "[YOUR BRAND NAME]",

  /**
   * Prefix on every delivered filename. Short, uppercase, yours:
   * ACME_431_..., not AD_431_... A filename that says whose ad it is survives
   * being emailed, Slacked and re-uploaded with its context stripped.
   */
  filePrefix: "AD",

  /**
   * WHERE FINISHED ADS LAND.
   *
   * Default `"ads"` keeps them inside the engine folder, which is right on day
   * one: nothing to configure and everything in one place.
   *
   * When you want the videos to live with the rest of a brand's work, point
   * this OUTSIDE the tool instead:
   *
   *   outputRoot: "~/Documents/my-brand/ads",
   *
   * That split matters: when a new version of the engine ships you delete the
   * tool folder and unzip the new one, and the videos are untouched because
   * they were never inside it. It is also how ONE engine serves several
   * brands: copy brand.mjs per brand, point each at its own folder.
   *
   * Relative paths resolve from engine/. The persona/concept tree builds
   * underneath either way, so the naming convention does not change.
   */
  outputRoot: "ads",

  /**
   * WHERE DELIVERED ADS LIVE — your DAM: a Drive folder, Dropbox, Frame.io
   * project, whatever the team pulls from. scripts/deliver.py names it in
   * the drag-and-drop prompt after the delivery checks pass. The kit never
   * uploads on its own; delivery is a human act.
   */
  dam: "[YOUR DAM — e.g. Google Drive > Ads > YourBrand]",

  /** Round avatar on the end card (a face or a mark). Put the file in
   *  public/brand/ and set e.g. "brand/avatar.png". null hides it. */
  avatar: null,

  /** Small label above the platform wordmark, e.g. "Read it on". Set to null
   *  to hide the label and the wordmark together. */
  platformLabel: null,

  /** Under the name on a FREE cut. */
  freeSubline: "[YOUR SUBLINE — e.g. reader count · 100% free]",

  /** Under the name on a PAID cut. */
  paidSubline: "[YOUR SUBLINE, minus any free-forever claim]",

  /** The button. Keep it the action the click actually performs. */
  cta: "Subscribe free",

  /** Second line under the button, PAID cuts only. null hides it. */
  paidFollowOn: null,

  /**
   * The standing eyebrow that marks where the body ends and the offer starts,
   * on PAID cuts. Most feeds play muted, so the free/paid boundary has to
   * survive with the sound off. A logo wall would wreck a format built on one
   * word at a time, so RSVP carries the boundary with this instead.
   */
  offerEyebrow: "[YOUR PAID OFFER NAME]",

  /** Typefaces. System stacks on purpose: no font loading, no licence, no FOUT. */
  serif: "Georgia, 'Iowan Old Style', serif",
  sans: "'Helvetica Neue', Helvetica, Arial, sans-serif",

  /**
   * The Cards format shipped with a SHORTER sans stack than OneWord did — no
   * 'Helvetica Neue' at the front. Almost certainly unintended drift between
   * two hand-written components, but collapsing the two changes the pixels of
   * previously rendered cuts (measured: PSNR drops from identical to ~41dB).
   *
   * Kept separate so re-rendering an existing Cards cut reproduces the file
   * that actually ran. A NEW format should use `sans`. If you decide to unify
   * them, do it deliberately and re-render the whole wave, not by accident.
   */
  sansCards: "Helvetica, Arial, sans-serif",
};

/**
 * Per-format visual knobs, exposed so a new creative idea does not need a
 * component edit. Change these and re-render; nothing else breaks.
 */
export const RSVP = {
  /**
   * Where the fixed anchor sits horizontally, as a fraction of frame width.
   *
   * Left of centre ON PURPOSE. The recognition letter lands early in a word, so
   * the tail is almost always longer than the head; anchoring at the midpoint
   * pushes long words off the right edge. 0.40 clears 1080px for words up to
   * about 11 characters at the 145px size.
   *
   * If your copy has longer words, move this LEFT, do not shrink the type.
   * And never centre the word itself, which is the exact cost RSVP exists to
   * remove.
   */
  anchor: 0.4,

  /**
   * Type size by word length. Coarse buckets on purpose: resizing on every
   * word makes the read feel unstable. [maxChars, px], first match wins.
   */
  sizes: [
    [5, 240],
    [8, 196],
    [11, 145],
    [Infinity, 108],
  ],

  /**
   * How many letters after the anchor also get the accent.
   *
   * Two coloured letters was the original ask, but on a three-letter word two
   * is most of the word and the accent stops reading as a fixation point at
   * all. Words at or under `shortWordMax` letters get none. "you" and "one"
   * are a large share of ad copy, so this is not an edge case.
   */
  shortWordMax: 4,
  accentRun: 1,

  /** Near-black behind the words. Slightly off the theme bg, which reads flat. */
  bg: "#0A0908",

  /** How long the end card holds, in seconds. */
  freeEndCard: 3.2,
  paidEndCard: 3.6,

  /** Music bed level under the read, and under the end card. */
  bedUnderVoice: 0.14,
  bedUnderCard: 0.5,
};
