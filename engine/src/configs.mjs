/**
 * One entry per ad. THIS IS THE ONLY FILE YOU EDIT TO ADD AN AD.
 *
 * The fields drive both the composition id and the output path, so a config
 * entry and a render command cannot drift apart.
 *
 *   ads/<personaDir>/<number>-<format-lowercase>-<conceptSlug>/
 *     <PREFIX>_<number>_<Persona>_<Format>_<Concept>_<HookStyle>_<OFFER>_<Ratio>.mp4
 *
 * (<PREFIX> is BRAND.filePrefix in brand.mjs. The full convention is in
 * parts/80-naming-and-delivery.md — check it before a big build.)
 *
 * number      the creative concept. 401, 402, ... Pick a scheme and keep it.
 * persona     your audience segment, CamelCase. One word.
 * personaDir  delivery folder for that segment. Numbering them by share of
 *             your paying base keeps the biggest segment at the top of every
 *             file listing: 01-founders, 02-individuals, ...
 * format      What you will see, in plain English:
 *               Cards    your graphics in sequence, with a voiceover
 *               Aerial   drone/landscape footage, static text block, silent
 *               OneWord  one word at a time, voiceover-synced
 *             OneWord IS RSVP. The code uses the technical name, the delivery
 *             tree uses the plain one so nobody needs the jargon to file a file.
 * concept     CamelCase, no spaces. The idea, not the wording.
 * conceptSlug lowercase-hyphenated form, for the folder.
 * hookStyle   HOW THE AD OPENS, and it REPLACES a bare V1/V2 counter:
 *               Ask    opens on a question
 *               Tell   direct address, names the reader's situation as fact
 *               About  third person
 *             A counter told you two files differed but never what differed.
 *             This says the thing itself, and the whole account sorts by it.
 *
 * A DEFECT FIX IS NOT A TEST ARM. A broken cut leaves the delivery tree
 * entirely, to ads/_retired/ with a WHY-RETIRED.md. Never into the concept
 * folder, not even a subfolder: if a file is in a persona folder, it can be
 * uploaded, and that rule is only worth anything with no exceptions.
 *
 * config.voEnd is the end time of the last word. scripts/timings.py prints it.
 * DO NOT GUESS IT. Too low and the end card cuts into the read; too high and
 * the ad ends on a held word and silence.
 *
 * config.bodyEnd (paid only) is where the body stops and the offer outro
 * begins. The offer eyebrow appears there.
 *
 * A FORMAT TEST REUSES THE VOICEOVER FILE OF THE AD IT TESTS AGAINST — the same
 * file, not a re-recording of the same script. Two rolls of one script are not
 * the same take, and if the voice differs the format is no longer the only
 * variable that moved.
 *
 * THE LIST SHIPS EMPTY. Every entry needs its voiceover in public/audio/ and
 * its timings in public/words/<number>.json (from scripts/timings.py), and the
 * timings are require()d at bundle time, so an entry pointing at files that do
 * not exist yet stops the whole studio from opening. Add the files first, then
 * the entry. The commented templates below are the two shapes to copy.
 */
export const ADS = [
  // --- OneWord (RSVP) template: the zero-spend starting format -----------
  // {
  //   number: "101",
  //   persona: "YourSegment",
  //   personaDir: "01-your-segment",
  //   format: "OneWord",
  //   concept: "YourConceptName",
  //   conceptSlug: "your-concept-name",
  //   hookStyle: "Tell",
  //   config: {
  //     offer: "free",                 // never omit it
  //     vo: "audio/vo_101.wav",        // your voiceover file
  //     bed: "audio/bed_phrygian.wav", // make it first: python3 scripts/bed.py. Or omit: no music
  //     voEnd: 25.1,                   // <- from timings.py output. Do not guess.
  //   },
  // },

  // --- Cards (captions over artwork) template ----------------------------
  // Scenes hard-cut between static punch-ins of your artwork. `zoom` is chosen
  // per scene and held; nothing animates and nothing reads the frame number.
  // {
  //   number: "102",
  //   persona: "YourSegment",
  //   personaDir: "01-your-segment",
  //   format: "Cards",
  //   concept: "YourConceptName",
  //   conceptSlug: "your-concept-name",
  //   hookStyle: "Tell",
  //   config: {
  //     offer: "free",
  //     theme: "dark",                  // or "paper" — match your artwork
  //     vo: "audio/vo_102.wav",
  //     bed: "audio/bed_phrygian.wav",  // from scripts/bed.py. Or omit: no music
  //     hookEnd: 2.90,                  // when the on-screen hook hands off to scene 1
  //     hookAccent: "(word|another)",   // regex SOURCE string, escapes doubled
  //     hookAccentFlags: "i",           // never "g": .test() on a global regex is stateful
  //     hookSize: 96,
  //     hookLineHeight: 1.1,
  //     voEnd: 28.90,                   // from timings.py. Do not guess.
  //     endCard: "large",
  //     scenes: [
  //       // img paths are relative to public/. zoom 1.0 = whole artwork wide;
  //       // above 1 is a static punch-in. focusX/focusY pick the centre of
  //       // interest (0-1). If artwork text runs to an edge, focus flush to
  //       // that edge: losing an illustration reads as a crop, losing text
  //       // reads as a bug.
  //       { img: "img/your-art.jpg", zoom: 1.0, focusY: 0.50, from: 2.90, to: 5.56 },
  //       { img: "img/your-art.jpg", zoom: 1.5, focusX: 1, focusY: 0.50, from: 5.56, to: 10.88 },
  //     ],
  //   },
  // },
];
