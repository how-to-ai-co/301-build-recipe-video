#!/usr/bin/env python3
"""Text overlays on real footage — creator clips, UGC, screen recordings.

    python3 scripts/overlay.py hook       <in.mp4> <out.mp4> "Your hook text"
                                          [--from 0] [--until END]
    python3 scripts/overlay.py transcribe <in.mp4> <words.json>
    python3 scripts/overlay.py captions   <in.mp4> <words.json> <out.mp4>

hook        Burns a static text block near the top of the frame, the
            Instagram text-tool look (same recipe as the aerial format:
            system font, heavy weight, hard black stroke, fade-in).
            --from/--until bound when it is on screen; omit --until to hold
            it for the whole clip.

transcribe  Extracts the clip's own audio and runs it through
            scripts/timings.py (Whisper), writing the word timings that
            captions needs. READ THE PRINTED TRANSCRIPT — a misheard word
            burned into the video is the whole failure mode. Needs the
            Python env from requirements.txt.

captions    Burns word-group captions synced to the speech, lower third,
            inside the feed-chrome safe area. Groups split on pauses over
            0.9s and cap at 5 words, stray punctuation is glued to the word
            before it — the same reading rules the Cards format uses.

Text sizes are set relative to a 1080-wide frame and scale with the input.
macOS only (uses the system SF font, same as the aerial format). Needs a real
ffmpeg. Screen the result at full resolution before it ships, and keep every
caption inside the safe areas: feed chrome covers roughly the top 14% and
bottom 20% of a 9:16 frame.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffio

SF = "/System/Library/Fonts/SFNS.ttf"
SAFE_TOP = 0.14          # feed chrome, share of frame height
SAFE_BOTTOM = 0.795
HOOK_SIZE = 62           # px at 1080 wide, same as the aerial text block
CAP_SIZE = 54
STROKE = 4               # hard black outline, not a soft shadow
LINE = 1.16
WIDTH = 0.88             # share of frame width the text may fill
CAP_Y = 0.70             # caption baseline band, above the bottom chrome
MAX_WORDS = 5            # per caption group
GAP_SPLIT = 0.9          # a pause this long starts a new group

ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart",
       "-c:a", "copy"]


def font(size, weight="Heavy"):
    f = ImageFont.truetype(SF, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_layer(w, h, text, size_1080, y_center):
    """Full-frame RGBA with a centred, wrapped, stroked text block."""
    scale = w / 1080
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fnt = font(int(size_1080 * scale))
    lh = int(size_1080 * scale * LINE)
    lines = wrap(d, text, fnt, int(w * WIDTH))
    total = len(lines) * lh
    yy = int(y_center * h - total / 2)
    for ln in lines:
        x = (w - d.textlength(ln, font=fnt)) / 2
        d.text((x, yy), ln, font=fnt, fill=(255, 255, 255, 255),
               stroke_width=int(STROKE * scale) or STROKE,
               stroke_fill=(0, 0, 0, 255))
        yy += lh
    return img


def hook(src, dst, text, t_from, t_until):
    info = ffio.probe(src)
    t_until = info["duration"] if t_until is None else t_until
    # The block sits in the upper third, under the top chrome.
    png = Path(dst).with_suffix(".overlay.png")
    text_layer(info["w"], info["h"], text, HOOK_SIZE, SAFE_TOP + 0.14).save(png)
    ffio.run([
        # -loop 1: a single-frame image gives fade= no timeline to act on
        # otherwise (same trap render_aerial.py documents).
        ffio.ffmpeg(), "-y", "-v", "error", "-i", src,
        "-loop", "1", "-i", str(png),
        "-filter_complex",
        f"[1]format=rgba,fade=in:st={t_from + 0.35}:d=0.55:alpha=1[ov];"
        f"[0][ov]overlay=0:0:format=auto:enable='between(t,{t_from},{t_until})'",
        # -shortest is load-bearing: the -loop 1 image input is infinite, and
        # without it ffmpeg encodes forever.
        "-shortest", *ENC, dst,
    ])
    png.unlink()
    ffio.report(dst)


def glue(words):
    """",000" and lone punctuation join the word before them — a stray ",000"
    burned as its own caption is the ugliest thing this tool can do."""
    out = []
    for w in words:
        joinable = (w["w"][:1] in ",." and w["w"][1:2].isdigit()) or \
            all(c in "%.,!?;:" for c in w["w"])
        if joinable and out:
            p = out[-1]
            out[-1] = {"w": p["w"] + w["w"], "s": p["s"], "e": w["e"]}
        else:
            out.append(dict(w))
    return out


def group(words):
    groups, cur = [], []
    for w in words:
        if cur and (w["s"] - cur[-1]["e"] > GAP_SPLIT or len(cur) >= MAX_WORDS):
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    # merge a trailing stub so nothing reads as a fragment
    if len(groups) > 1 and len(groups[-1]) < 3 and \
            len(groups[-2]) + len(groups[-1]) <= MAX_WORDS + 2:
        groups[-2] += groups.pop()
    return groups


def captions(src, words_path, dst):
    info = ffio.probe(src)
    words = glue(json.loads(Path(words_path).read_text()))
    groups = group(words)
    if not groups:
        sys.exit(f"{words_path} holds no words")

    tmp = Path(tempfile.mkdtemp(prefix="captions_"))
    parts, prev = [], "[0]"
    cmd = [ffio.ffmpeg(), "-y", "-v", "error", "-i", src]
    for n, g in enumerate(groups):
        png = tmp / f"g{n}.png"
        text_layer(info["w"], info["h"],
                   " ".join(w["w"] for w in g), CAP_SIZE, CAP_Y).save(png)
        cmd += ["-i", str(png)]
        # Hold each caption to the start of the next group so speech pauses
        # never blank the lower third mid-read.
        end = groups[n + 1][0]["s"] if n + 1 < len(groups) else g[-1]["e"] + 0.3
        out = f"[v{n}]" if n + 1 < len(groups) else "[vo]"
        parts.append(
            f"{prev}[{n + 1}]overlay=0:0:format=auto:"
            f"enable='between(t,{g[0]['s']},{end})'{out}")
        prev = f"[v{n}]"
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vo]",
            "-map", "0:a?", *ENC, dst]
    ffio.run(cmd)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    print(f"{len(groups)} caption groups")
    ffio.report(dst)


def transcribe(src, words_path):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
        wav = t.name
    ffio.run([ffio.ffmpeg(), "-y", "-v", "error", "-i", src,
              "-vn", "-ac", "1", "-ar", "16000", wav])
    r = subprocess.run([sys.executable,
                        str(Path(__file__).resolve().parent / "timings.py"),
                        wav, words_path])
    Path(wav).unlink()
    if r.returncode:
        sys.exit(r.returncode)


def main():
    a = sys.argv[1:]
    opts = {}
    while "--from" in a:
        i = a.index("--from"); opts["from"] = float(a[i + 1]); del a[i:i + 2]
    while "--until" in a:
        i = a.index("--until"); opts["until"] = float(a[i + 1]); del a[i:i + 2]
    if len(a) == 4 and a[0] == "hook":
        hook(a[1], a[2], a[3], opts.get("from", 0.0), opts.get("until"))
    elif len(a) == 3 and a[0] == "transcribe":
        transcribe(a[1], a[2])
    elif len(a) == 4 and a[0] == "captions":
        captions(a[1], a[2], a[3])
    else:
        sys.exit(__doc__.strip())


if __name__ == "__main__":
    main()
