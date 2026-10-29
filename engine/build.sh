#!/bin/bash
# Render every ad in src/configs.mjs, both ratios, named to convention.
#
#   ./build.sh          # all of them
#   ./build.sh 431      # one
#
# Paths and filenames are built from the same fields the compositions are, so a
# render can never land in a folder that disagrees with its config. The
# convention is in parts/80-naming-and-delivery.md:
#
#   ads/<personaDir>/<number>-<format-lowercase>-<conceptSlug>/
#     <PREFIX>_<number>_<Persona>_<Format>_<Concept>_<HookStyle>_<OFFER>_<Ratio>.mp4
#
# <PREFIX> is BRAND.filePrefix in src/brand.mjs.
#
# There is NO version counter. HookStyle (Ask/Tell/About) replaced it, because a
# counter told you two files differed but never what differed.
set -e
cd "$(dirname "$0")"

WANT="${1:-}"

# Read the ad list from configs.mjs rather than duplicating it here. A second
# copy of the list is a second place to forget to update. This is why that file
# is plain JavaScript: node imports it as-is, with nothing installed.
node --input-type=module -e '
import { ADS } from "./src/configs.mjs";
for (const a of ADS) {
  const offer = (a.config.offer ?? "free").toUpperCase();
  console.log([a.number, a.persona, a.personaDir, a.format, a.concept,
               a.conceptSlug, a.hookStyle, offer].join("|"));
}' > .ads.tmp

# Where finished ads land. Set BRAND.outputRoot in src/brand.mjs; it may be a
# path outside this folder, so the tool and the work can live apart.
OUTROOT=$(node --input-type=module -e '
import { BRAND } from "./src/brand.mjs";
console.log(BRAND.outputRoot ?? "ads");')
OUTROOT="${OUTROOT/#\~/$HOME}"          # expand a leading ~
mkdir -p "$OUTROOT"
echo "output: $OUTROOT"

PREFIX=$(node --input-type=module -e '
import { BRAND } from "./src/brand.mjs";
console.log(BRAND.filePrefix ?? "AD");')

while IFS='|' read -r num persona pdir format concept slug hookstyle offer; do
  [ -n "$WANT" ] && [ "$WANT" != "$num" ] && continue

  fmt_lc=$(printf '%s' "$format" | tr '[:upper:]' '[:lower:]')
  dir="${OUTROOT}/${pdir}/${num}-${fmt_lc}-${slug}"
  mkdir -p "$dir"
  base="${PREFIX}_${num}_${persona}_${format}_${concept}_${hookstyle}_${offer}"
  echo "--- $num $persona $format $hookstyle $offer ---"

  npx remotion render "${format}${num}-${hookstyle}-${offer}-9x16" \
    "${dir}/${base}_9x16.mp4" --log=error
  npx remotion render "${format}${num}-${hookstyle}-${offer}-4x5" \
    "${dir}/${base}_4x5.mp4" --log=error
done < .ads.tmp
rm -f .ads.tmp

echo
# Report REAL durations and sizes. Never report a length you did not measure.
#
# ffprobe: prefer the system one, fall back to the copy Remotion already ships
# in its compositor package. That fallback is the reason the two ready formats
# need nothing but Node — no Homebrew, no separate ffmpeg install. The bundled
# binary needs its own dylibs on the library path, hence DYLD_LIBRARY_PATH.
COMP=$(ls -d node_modules/@remotion/compositor-* 2>/dev/null | head -1)
if command -v ffprobe >/dev/null 2>&1; then
  probe() { ffprobe "$@"; }
elif [ -n "$COMP" ] && [ -x "$COMP/ffprobe" ]; then
  probe() { DYLD_LIBRARY_PATH="$COMP" "$COMP/ffprobe" "$@"; }
else
  probe() { echo ""; }
  echo "(no ffprobe found — durations not measured)"
fi
find "$OUTROOT" -name '*.mp4' | sort | while read -r f; do
  printf "%-76s %ss %s\n" "$(basename "$f")" \
    "$(probe -v error -show_entries format=duration -of csv=p=0 "$f")" \
    "$(du -h "$f" | cut -f1)"
done
