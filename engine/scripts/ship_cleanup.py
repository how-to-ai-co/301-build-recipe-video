#!/usr/bin/env python3
"""Clear out the working files of videos that have shipped.

A video counts as shipped when its folder in ~/Desktop/Final Content holds a
final mp4 and a cover. Everything Claude made on the way there (revisions,
project files, proxies, audio stems, the copied source clip) lives in its
project folder under output/, and the raw clip usually still sits in
~/Downloads. Once the final is safely in Final Content, all of that can go.

    python3 engine/scripts/ship_cleanup.py                  # dry run: report only
    python3 engine/scripts/ship_cleanup.py --trash          # move it all to the Trash
    python3 engine/scripts/ship_cleanup.py --archive /Volumes/SSD/video-archive

Nothing is ever hard-deleted. --trash moves files to the macOS Trash (empty
it yourself); --archive moves them to a folder you name, keeping the layout.
Any post caption (caption*.txt / captions.md) is copied into the Final
Content folder first, so finals, covers and captions all survive.
"""

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
FINALS = Path.home() / "Desktop" / "Final Content"
DOWNLOADS = Path.home() / "Downloads"
VIDEO = {".mp4", ".mov", ".m4v"}
IMAGE = {".png", ".jpg", ".jpeg"}
CAPTION_NAMES = ("caption", "captions", "post-copy", "post")


def gb(n):
    return f"{n / 1e9:.1f} GB" if n >= 1e8 else f"{n / 1e6:.0f} MB"


def size_of(p):
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and not f.is_symlink())


def index_by_size(root, exts):
    """Map file size -> paths, for matching copies without hashing 50 GB."""
    idx = {}
    for f in root.rglob("*"):
        if f.is_file() and f.suffix.lower() in exts and f.stat().st_size > 1_000_000:
            idx.setdefault(f.stat().st_size, []).append(f)
    return idx


def shipped_items():
    """Yield (final_folder, final_mp4, cover, delivery_dict) for each shipped video."""
    for d in sorted(p for p in FINALS.iterdir() if p.is_dir()):
        vids = [f for f in d.iterdir() if f.suffix.lower() in VIDEO]
        covers = [f for f in d.iterdir() if f.suffix.lower() in IMAGE]
        delivery = {}
        if (d / "delivery.json").exists():
            try:
                delivery = json.loads((d / "delivery.json").read_text())
            except ValueError:
                pass
        yield d, (vids[0] if vids else None), (covers[0] if covers else None), delivery


def project_for(source, shipped_sources):
    """The folder under output/ that belongs to this one video.

    Usually the top-level folder. When that folder holds the working files of
    several videos (a batch, three yaps in one), step down to the child folder
    the source sits in, so a sibling that has not shipped is left alone.
    """
    rel = source.relative_to(OUTPUT)
    top = OUTPUT / rel.parts[0]
    others = [s for s in shipped_sources if s != source and top in s.parents]
    if len(rel.parts) > 2 and (others or has_unshipped_children(top, shipped_sources)):
        return top / rel.parts[1]
    return top


def has_unshipped_children(top, shipped_sources):
    kids = [k for k in top.iterdir() if k.is_dir() and not k.name.startswith(".")]
    video_kids = [k for k in kids if any(f.suffix.lower() in VIDEO for f in k.rglob("*"))]
    if len(video_kids) < 2:
        return False
    return any(not any(k in s.parents for s in shipped_sources) for k in video_kids)


def find_captions(project):
    return [f for f in project.rglob("*")
            if f.is_file() and f.suffix.lower() in {".txt", ".md"}
            and f.stem.lower().split("-")[0] in CAPTION_NAMES]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--trash", action="store_true", help="move working files to the macOS Trash")
    mode.add_argument("--archive", metavar="DIR", help="move working files to DIR (an SSD, a Drive folder)")
    ap.add_argument("--keep-raw", action="store_true", help="leave the raw clips in ~/Downloads alone")
    args = ap.parse_args()

    if not FINALS.is_dir():
        sys.exit(f"No Final Content folder at {FINALS}")

    print("Indexing output/ and Downloads (sizes only, a few seconds)...")
    out_idx = index_by_size(OUTPUT, VIDEO)
    dl_idx = {} if args.keep_raw else index_by_size(DOWNLOADS, VIDEO) if DOWNLOADS.is_dir() else {}

    # Pass 1: work out which output file each final came from.
    items = []
    for folder, final, cover, delivery in shipped_items():
        if not final or not cover:
            items.append((folder, None, "skipped: Final Content folder is missing its video or cover"))
            continue
        src = Path(delivery["source_video"]) if delivery.get("source_video") else None
        if not (src and src.exists() and OUTPUT in src.parents):
            same = [p for p in out_idx.get(final.stat().st_size, []) if p.name == final.name] \
                or out_idx.get(final.stat().st_size, [])
            src = same[0] if same else None
        if not src:
            items.append((folder, None, "no matching project in output/ (already cleaned, or made elsewhere)"))
            continue
        items.append((folder, src, delivery))
    sources = [s for _, s, _ in items if s]

    # Pass 2: what each shipped video leaves behind.
    plan, seen, total = [], set(), 0
    for folder, src, extra in items:
        if not src:
            print(f"\n  {folder.name}\n    {extra}")
            continue
        project = project_for(src, sources)
        if project in seen:
            continue
        seen.add(project)
        moves = [project]
        raws = set()
        if delivery_raw := (extra.get("original") if isinstance(extra, dict) else None):
            if Path(delivery_raw).exists():
                raws.add(Path(delivery_raw))
        # Any big video in the project that is a byte-size twin of a Downloads clip is the raw copy.
        for f in project.rglob("*"):
            if f.is_file() and f.suffix.lower() in VIDEO:
                raws.update(dl_idx.get(f.stat().st_size, []))
        # A raw clip can feed several videos (part 1, part 2). Keep it while any
        # project outside this one still holds a copy that has not shipped.
        raws = {r for r in raws if not any(
            project not in p.parents and not any(s.parent == p.parent or p.parent in s.parents for s in sources)
            for p in out_idx.get(r.stat().st_size, []))}
        if args.keep_raw:
            raws = set()
        moves += sorted(raws)
        caps = find_captions(project)
        size = sum(size_of(m) for m in moves)
        total += size
        plan.append((folder, project, moves, caps, size))

    print("\nShipped videos and what they leave behind:\n")
    for folder, project, moves, caps, size in plan:
        print(f"  {folder.name}   ->  frees {gb(size)}")
        print(f"    keeps:   Final Content/{folder.name}/ (final + cover"
              + (f" + {len(caps)} caption file{'s' if len(caps) > 1 else ''})" if caps else ")"))
        for m in moves:
            label = "project" if m == project else "raw clip"
            print(f"    {label:8} {m.relative_to(ROOT) if ROOT in m.parents else m}  ({gb(size_of(m))})")
        print()

    untouched = sorted(p.name for p in OUTPUT.iterdir() if p.is_dir()
                       and not any(p == pr or p in pr.parents for _, pr, *_ in plan))
    print(f"Not shipped (left alone): {len(untouched)} folders in output/")
    print(f"\nTotal it would free: {gb(total)}")

    if not (args.trash or args.archive):
        print("\nDry run. Nothing moved. Re-run with --trash or --archive DIR to do it.")
        return

    dest_root = Path(args.archive).expanduser() if args.archive else Path.home() / ".Trash" / f"ship-cleanup-{time.strftime('%Y%m%d-%H%M%S')}"
    for folder, project, moves, caps, _ in plan:
        for c in caps:
            target = folder / c.name
            if not target.exists():
                shutil.copy2(c, target)
        for m in moves:
            try:
                rel = m.relative_to(ROOT)
            except ValueError:
                rel = Path("Downloads") / m.name
            target = dest_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if m.exists():
                shutil.move(str(m), str(target))
    where = "the Trash (empty it to get the space back)" if args.trash else str(dest_root)
    print(f"\nMoved to {where}.")


if __name__ == "__main__":
    main()
