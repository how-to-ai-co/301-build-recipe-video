#!/usr/bin/env python3
"""The delivery gate. Run after every build, before anything leaves the tree.

    python3 scripts/deliver.py           # check the whole delivery tree
    python3 scripts/deliver.py --open    # ...and open it in Finder to drag from

Walks BRAND.outputRoot and checks every finished edit against the convention
in parts/80-naming-and-delivery.md. Two severities:

HARD FAILURES — block delivery for any video, post or ad:
  - a filename that does not match
    <PREFIX>_<number>_<Segment>_<Format>_<Concept>_<HookStyle>_<OFFER>_<Ratio>.mp4
    (spaces, leftover [BRACKETS], wrong tokens)
  - the number token not matching the folder
  - a missing post-copy file for an offer the folder holds
    (caption-free.md / caption-paid.md — the post caption or the Ads Manager
    fields, depending on the lane)
  - an empty folder

AD-LANE WARNINGS — reported so nothing ships unnoticed, never blocking
(an organic post is one ratio and any length on purpose):
  - a cut missing its second ratio
  - a FREE cut over 35s (long for cold ad traffic), anything over 60s

`_retired/` and `_batches/` are skipped, as parts/80 defines.

Then it prints what is READY TO DELIVER and prompts the human step this kit
will not automate: dragging the passing folders into your DAM — Drive,
Dropbox, Frame.io, whatever `BRAND.dam` in src/brand.mjs names. Uploading is
deliberately a human act: the gate proves the files are right, a person
decides they ship.

Exit code is non-zero only on hard failures, so Claude cannot call the tree
clean without this saying so.
"""
import re
import subprocess
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
SKIP = {"_retired", "_batches"}


def brand():
    out = subprocess.run(
        ["node", "--input-type=module", "-e",
         'import { BRAND } from "./src/brand.mjs";'
         'console.log(JSON.stringify({p: BRAND.filePrefix ?? "AD",'
         'o: BRAND.outputRoot ?? "ads", d: BRAND.dam ?? ""}))'],
        cwd=ENGINE, check=True, capture_output=True, text=True).stdout
    import json
    return json.loads(out)


def find_ffprobe():
    import shutil
    p = shutil.which("ffprobe")
    if p:
        return [p]
    for comp in sorted((ENGINE / "node_modules").glob("@remotion/compositor-*")):
        if (comp / "ffprobe").exists():
            import os
            os.environ["DYLD_LIBRARY_PATH"] = str(comp)
            return [str(comp / "ffprobe")]
    return None


def duration(probe, path):
    if not probe:
        return None
    out = subprocess.run(
        [*probe, "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out) if out else None


def main():
    b = brand()
    root = (ENGINE / b["o"]).resolve() if not b["o"].startswith(("/", "~")) \
        else Path(b["o"]).expanduser()
    if not root.is_dir():
        sys.exit(f"no delivery tree at {root} — nothing built yet?")

    probe = find_ffprobe()
    if not probe:
        print("(no ffprobe found — durations not measured this run)")

    name_re = re.compile(
        rf"^{re.escape(b['p'])}_(\d+)_[A-Z][A-Za-z0-9]*_[A-Z][A-Za-z0-9]*_"
        rf"[A-Z][A-Za-z0-9]*_(Ask|Tell|About)_(FREE|PAID)_(9x16|4x5)\.mp4$")

    ready, failed = [], []
    folders = [d for d in sorted(root.glob("*/*"))
               if d.is_dir() and not ({*d.parts} & SKIP)]
    if not folders:
        sys.exit(f"{root} has no concept folders yet")

    for folder in folders:
        issues = []
        warns = []
        mp4s = sorted(folder.glob("*.mp4"))
        cuts = {}
        for f in mp4s:
            m = name_re.match(f.name)
            if not m:
                why = ("has a space" if " " in f.name else
                       "leftover [placeholder]" if "[" in f.name else
                       "does not match the convention")
                issues.append(f"{f.name}: {why} (parts/80)")
                continue
            num, hook, offer, ratio = m.groups()
            cuts.setdefault((num, hook, offer), set()).add(ratio)
            if not str(folder.name).startswith(num + "-"):
                issues.append(f"{f.name}: number {num} does not match "
                              f"folder {folder.name}")
            d = duration(probe, f)
            if d and d > 60:
                warns.append(f"{f.name}: {d:.1f}s — over 60s. Fine for a "
                             "post, long for an ad")
            elif d and offer == "FREE" and d > 35:
                warns.append(f"{f.name}: {d:.1f}s — long for cold ad "
                             "traffic. Fine for an organic post")
        for (num, hook, offer), ratios in cuts.items():
            missing = {"9x16", "4x5"} - ratios
            for r in sorted(missing):
                warns.append(f"{num} {hook} {offer}: no {r} ratio — needed "
                             "if this ships as an ad")
        offers = {o for (_, _, o) in cuts}
        for o in sorted(offers):
            cap = folder / f"caption-{o.lower()}.md"
            if not cap.exists():
                issues.append(f"missing {cap.name} — the post copy, or the "
                              "Ads Manager fields for an ad (parts/80)")
        if not mp4s:
            issues.append("no mp4 files")

        rel = folder.relative_to(root)
        if issues:
            failed.append(rel)
            print(f"\nFAIL  {rel}")
            for i in issues:
                print(f"      - {i}")
        else:
            ready.append(rel)
            print(f"ok    {rel}  ({len(mp4s)} files)")
        for w in warns:
            print(f"      ~ ad-lane warning: {w}")

    print()
    if failed:
        print(f"{len(failed)} folder(s) failed, {len(ready)} clean. "
              "Fix the failures before anything is delivered — a wrong file "
              "in the tree WILL get uploaded eventually.")
        sys.exit(1)

    print(f"READY TO DELIVER — {len(ready)} folder(s), all checks passed.")
    dam = b["d"]
    if dam and "[" not in dam:
        print(f"Drag them from {root} into: {dam}")
    else:
        print(f"Drag them from {root} into your DAM (Drive, Dropbox, "
              "Frame.io, ...). Set BRAND.dam in src/brand.mjs to name the "
              "exact destination here.")
    print("Uploading stays a human act on purpose: this gate proves the "
          "files are right, you decide they ship.")
    if "--open" in sys.argv and sys.platform == "darwin":
        subprocess.run(["open", str(root)])


if __name__ == "__main__":
    main()
