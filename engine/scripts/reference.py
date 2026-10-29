#!/usr/bin/env python3
"""Break down a reference video so you can say "make mine like this".

    python3 scripts/reference.py https://www.instagram.com/reel/XXXX/
    python3 scripts/reference.py https://youtube.com/shorts/XXXX
    python3 scripts/reference.py ~/Downloads/some_video.mp4
    python3 scripts/reference.py <url> --cookies-from-browser chrome   # Instagram login wall
    python3 scripts/reference.py <url> --name oren-hook                # pick the folder name

Everything lands in  references/videos/<slug>/  at the repo root:

    source.mp4        the downloaded video (URLs only; never committed to git)
    contact.png       one thumbnail per shot in a grid, timestamped
    frames/           hook frames (0s, 0.5s, 1s) plus one larger frame per shot
    analysis.json     every measured number, for Claude to read
    transcript.json   word timings, only if Whisper is installed
    breakdown.md      the plain-language breakdown + "make mine like this" checklist

Needs: Python 3.10+, a real ffmpeg/ffprobe. Optional: yt-dlp (for links),
openai-whisper (for transcripts). Nothing here logs in or bypasses anything:
if a site wants a login, pass your own browser cookies or download the file
yourself and pass the path.

Reference videos are for studying style. Do not republish other people's footage.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ffio  # noqa: E402  (shared ffmpeg finder; exits with install help if missing)

REPO = HERE.parents[1]
OUT_ROOT = REPO / "references" / "videos"
ENGINE_VENV_PY = REPO / "engine" / ".venv" / "bin" / "python"

SCENE_THRESHOLD = 0.3
MAX_SHEET_TILES = 30
MAX_SHOT_FRAMES = 12


# --------------------------------------------------------------------------- helpers

def step(msg: str) -> None:
    print(f"\n==> {msg}", flush=True)


def note(msg: str) -> None:
    print(f"    {msg}", flush=True)


def is_url(s: str) -> bool:
    return bool(re.match(r"^https?://", s.strip(), re.I))


def slugify(s: str, limit: int = 60) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return (s[:limit].strip("-")) or "reference"


def run_quiet(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def fmt_s(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.2f}s"


# --------------------------------------------------------------------------- download

def find_ytdlp() -> list[str] | None:
    exe = shutil.which("yt-dlp")
    if exe:
        return [exe]
    try:
        import yt_dlp  # noqa: F401
        return [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        return None


LOGIN_HINTS = ("login", "log in", "sign in", "cookies", "private", "rate-limit",
               "rate limit", "not available", "requested content is not available",
               "authentication", "403")


def download(url: str, name: str | None, cookies_browser: str | None,
             force: bool) -> tuple[pathlib.Path, dict]:
    ytdlp = find_ytdlp()
    if not ytdlp:
        print(
            "\nyt-dlp is not installed, and it is what downloads video links.\n"
            "Install it with ONE of these, then run the same command again:\n\n"
            "    python3 -m pip install yt-dlp\n"
            "    brew install yt-dlp\n\n"
            "Or download the video yourself and pass the file path instead of the link."
        )
        sys.exit(0)

    cookie_args = ["--cookies-from-browser", cookies_browser] if cookies_browser else []

    step("Looking up the link")
    meta: dict = {"url": url}
    r = run_quiet(ytdlp + ["--dump-single-json", "--no-playlist", "--skip-download",
                           *cookie_args, url])
    if r.returncode == 0:
        try:
            info = json.loads(r.stdout)
            for k in ("id", "title", "uploader", "channel", "extractor_key",
                      "webpage_url", "duration", "upload_date", "license"):
                if info.get(k) is not None:
                    meta[k] = info[k]
        except json.JSONDecodeError:
            pass
    else:
        explain_download_failure(r.stderr, url, cookies_browser)

    if name:
        slug = slugify(name)
    elif meta.get("id"):
        slug = slugify(f"{meta.get('extractor_key', 'video')}-{meta['id']}")
    else:
        slug = slugify(re.sub(r"^https?://(www\.)?", "", url))
    out_dir = OUT_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "source.mp4"
    note(f"title: {meta.get('title', '?')}   by: {meta.get('uploader') or meta.get('channel') or '?'}")
    note(f"folder: {out_dir.relative_to(REPO)}")

    if target.exists() and not force:
        note("source.mp4 already downloaded; reusing it (pass --force to re-download)")
        return target, meta

    step("Downloading (this can take a minute)")
    for old in out_dir.glob("source.*"):
        old.unlink()
    cmd = ytdlp + [
        "--no-playlist", "--no-part", "--newline",
        # best quality up to 1080p, preferring mp4/m4a so no re-encode is needed
        "-f", "bv*+ba/b", "-S", "res:1080,ext:mp4:m4a",
        "--merge-output-format", "mp4",
        "-o", str(out_dir / "source.%(ext)s"),
        *cookie_args, url,
    ]
    r = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:])
        explain_download_failure(r.stderr, url, cookies_browser)

    got = sorted(out_dir.glob("source.*"))
    if not got:
        sys.exit("Download finished but no file appeared. Try downloading it yourself "
                 "and passing the file path.")
    if got[0].suffix.lower() != ".mp4":
        note(f"converting {got[0].name} -> source.mp4")
        ffio.run([ffio.ffmpeg(), "-v", "error", "-y", "-i", str(got[0]),
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                  "-c:a", "aac", str(target)])
        got[0].unlink()
    return target, meta


def explain_download_failure(stderr: str, url: str, cookies_browser: str | None) -> None:
    low = (stderr or "").lower()
    print("\nThe download did not work.")
    if any(h in low for h in LOGIN_HINTS):
        if cookies_browser:
            print(f"Even with your {cookies_browser} cookies the site said no. Check you are\n"
                  "logged in to it in that browser, or save the video yourself and pass the\n"
                  "file path instead of the link.")
        else:
            print(
                "The site probably wants you to be logged in. Two options:\n"
                "  1. Log in to the site in your browser, then add your browser's cookies:\n"
                "       python3 scripts/reference.py \"<link>\" --cookies-from-browser chrome\n"
                "     (or safari / firefox / edge / brave). Your Mac may ask for permission.\n"
                "  2. Save the video yourself (screen-record or the app's save button) and\n"
                "     pass the file path instead of the link."
            )
    else:
        print("Check the link opens in a browser. If it does, update yt-dlp\n"
              "(`python3 -m pip install -U yt-dlp` or `brew upgrade yt-dlp`), or download the\n"
              "file yourself and pass the path.")
    tail = "\n".join(l for l in (stderr or "").splitlines() if "ERROR" in l)[-600:]
    if tail:
        print(f"\nyt-dlp said:\n{tail}")
    sys.exit(1)


# --------------------------------------------------------------------------- measure

def probe(path: pathlib.Path) -> dict:
    out = run_quiet([ffio.ffprobe(), "-v", "error", "-print_format", "json",
                     "-show_streams", "-show_format", str(path)])
    if out.returncode != 0:
        sys.exit(f"ffprobe could not read {path}. Is it a video file?\n{out.stderr[-500:]}")
    info = json.loads(out.stdout)
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
    if v is None:
        sys.exit(f"{path} has no video stream.")
    num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den or 0) else 0.0
    rn, rd = (v.get("r_frame_rate") or "0/1").split("/")
    rfps = float(rn) / float(rd) if float(rd or 0) else 0.0
    if not fps or (rfps and abs(fps - rfps) / rfps < 0.05):
        fps = rfps or 30.0  # nominal rate reads cleaner (30, not 30.168)
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    rot = rot or int((v.get("tags") or {}).get("rotate", 0) or 0)
    if abs(rot) % 180 == 90:
        w, h = h, w
    dur = float(info["format"].get("duration") or v.get("duration") or 0)
    return {
        "width": w, "height": h, "fps": round(fps, 3), "duration": round(dur, 3),
        "orientation": "vertical" if h > w else ("square" if h == w else "horizontal"),
        "aspect": aspect_label(w, h),
        "video_codec": v.get("codec_name"),
        "has_audio": a is not None,
        "audio_codec": a.get("codec_name") if a else None,
    }


def aspect_label(w: int, h: int) -> str:
    r = w / h
    for label, val in (("9:16", 9 / 16), ("4:5", 4 / 5), ("1:1", 1.0),
                       ("16:9", 16 / 9), ("4:3", 4 / 3)):
        if abs(r - val) < 0.03:
            return label
    return f"{w}:{h}"


def detect_cuts(path: pathlib.Path, duration: float, threshold: float) -> list[float]:
    """Hard-cut times in seconds (excluding 0). Uses ffmpeg's scene score."""
    # Downscale first: much faster, and scene scores barely change.
    vf = f"scale=270:-2,select='gt(scene\\,{threshold})',showinfo"
    r = run_quiet([ffio.ffmpeg(), "-hide_banner", "-nostats", "-i", str(path),
                   "-an", "-vf", vf, "-f", "null", "-"])
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    # Drop cuts closer than 0.2s to the previous one (flashes / dissolves count once)
    cuts: list[float] = []
    for t in sorted(times):
        if t < 0.1 or t > duration - 0.05:
            continue
        if cuts and t - cuts[-1] < 0.2:
            continue
        cuts.append(round(t, 3))
    return cuts


def shots_from_cuts(cuts: list[float], duration: float) -> list[dict]:
    edges = [0.0] + cuts + [duration]
    return [{"n": i + 1, "start": round(a, 3), "end": round(b, 3),
             "length": round(b - a, 3)} for i, (a, b) in enumerate(zip(edges, edges[1:]))
            if b - a > 0.01]


def audio_stats(path: pathlib.Path, duration: float) -> dict:
    """Loudness (EBU R128) + silence share. Cheap, no extra installs."""
    res: dict = {}
    r = run_quiet([ffio.ffmpeg(), "-hide_banner", "-nostats", "-i", str(path), "-vn",
                   "-af", "ebur128=peak=true", "-f", "null", "-"])
    summary = r.stderr.split("Summary:")[-1] if "Summary:" in r.stderr else ""
    for key, pat in (("integrated_lufs", r"I:\s+(-?[0-9.]+|-inf) LUFS"),
                     ("loudness_range_lu", r"LRA:\s+(-?[0-9.]+) LU"),
                     ("true_peak_dbfs", r"Peak:\s+(-?[0-9.]+|-inf) dBFS")):
        m = re.search(pat, summary)
        if m and m.group(1) != "-inf":
            res[key] = float(m.group(1))

    r = run_quiet([ffio.ffmpeg(), "-hide_banner", "-nostats", "-i", str(path), "-vn",
                   "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"])
    silent = sum(float(x) for x in re.findall(r"silence_duration:\s*([0-9.]+)", r.stderr))
    gaps = len(re.findall(r"silence_end", r.stderr))
    starts = re.findall(r"silence_start:\s*([0-9.]+)", r.stderr)
    if len(starts) > gaps:  # file ends in silence
        silent += max(0.0, duration - float(starts[-1]))
        gaps += 1
    res["silent_seconds"] = round(silent, 2)
    res["silent_share"] = round(silent / duration, 3) if duration else None
    res["pauses"] = gaps
    res["character_guess"] = guess_audio_character(res, duration)
    return res


def guess_audio_character(a: dict, duration: float) -> str:
    """Rough, honest guess. Claude should confirm by listening/reading the transcript."""
    if a.get("integrated_lufs") is None or (a.get("silent_share") or 0) > 0.9:
        return "silent or near-silent"
    share = a.get("silent_share") or 0
    pauses_per_10s = (a.get("pauses", 0) / duration * 10) if duration else 0
    lra = a.get("loudness_range_lu") or 0
    if share < 0.03 and pauses_per_10s < 0.5:
        return ("continuous sound with no pauses: likely music or a music bed "
                "(possibly with voice on top)")
    if pauses_per_10s >= 1 or lra >= 8:
        return "stop-start sound with natural pauses: likely speech-led (talking head / voiceover)"
    return "mixed: could be speech over a quiet bed; confirm with the transcript"


# --------------------------------------------------------------------------- frames

def font_file() -> str | None:
    for f in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/Library/Fonts/Arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(f):
            return f
    return None


def grab(path: pathlib.Path, t: float, out: pathlib.Path, height: int,
         label: str | None = None) -> bool:
    vf = f"scale=-2:{height}"
    if label:
        ff = font_file()
        fontarg = f"fontfile='{ff}':" if ff else ""
        size = max(14, height // 18)
        draw = (f",drawtext={fontarg}text='{label}':fontsize={size}:fontcolor=white:"
                f"box=1:boxcolor=black@0.65:boxborderw=6:x=8:y=h-th-14")
        r = run_quiet([ffio.ffmpeg(), "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path),
                       "-frames:v", "1", "-vf", vf + draw, "-q:v", "3", str(out)])
        if r.returncode == 0 and out.exists():
            return True
        # drawtext missing in this ffmpeg build: fall through to an unlabelled frame
    r = run_quiet([ffio.ffmpeg(), "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path),
                   "-frames:v", "1", "-vf", vf, "-q:v", "3", str(out)])
    return r.returncode == 0 and out.exists()


def sheet_times(shots: list[dict], duration: float) -> tuple[list[float], str]:
    """One tile per shot; if that's too many or too few, sample evenly instead."""
    mids = [s["start"] + s["length"] / 2 for s in shots]
    if 4 <= len(mids) <= MAX_SHEET_TILES:
        return mids, "one frame from the middle of each shot"
    n = MAX_SHEET_TILES if len(mids) > MAX_SHEET_TILES else min(12, max(6, int(duration)))
    step_s = duration / n
    return [step_s * (i + 0.5) for i in range(n)], f"one frame every {step_s:.1f}s"


def build_contact_sheet(path: pathlib.Path, info: dict, times: list[float],
                        shot_of: list[int], out_png: pathlib.Path) -> bool:
    vertical = info["height"] >= info["width"]
    cols = 6 if vertical else 4
    tile_h = 400 if vertical else 225
    with tempfile.TemporaryDirectory() as td:
        tdp = pathlib.Path(td)
        made = 0
        for i, t in enumerate(times):
            label = f"{t:.1f}s  #{shot_of[i]}" if shot_of[i] else f"{t:.1f}s"
            if grab(path, t, tdp / f"t{made:03d}.jpg", tile_h, label):
                made += 1
        if not made:
            return False
        rows = -(-made // cols)
        cols_used = min(cols, made)
        r = run_quiet([ffio.ffmpeg(), "-v", "error", "-y", "-start_number", "0",
                       "-i", str(tdp / "t%03d.jpg"),
                       "-vf", f"tile={cols_used}x{rows}:padding=6:margin=6:color=0x202020",
                       "-frames:v", "1", "-update", "1", str(out_png)])
        if r.returncode != 0:
            note(f"contact sheet failed: {r.stderr.strip()[-300:]}")
        return r.returncode == 0 and out_png.exists()


# --------------------------------------------------------------------------- transcript

WHISPER_SNIPPET = r"""
import json, sys, whisper
m = whisper.load_model(sys.argv[3])
r = m.transcribe(sys.argv[1], word_timestamps=True)
words = []
for seg in r["segments"]:
    for w in seg.get("words", []):
        words.append({"w": w["word"].strip(), "s": round(float(w["start"]), 3),
                      "e": round(float(w["end"]), 3)})
json.dump({"language": r.get("language"), "text": r.get("text", "").strip(),
           "words": words}, open(sys.argv[2], "w"), indent=1)
"""


def whisper_python() -> str | None:
    """This interpreter if it has whisper, else the engine's .venv if that does."""
    candidates = [sys.executable]
    if ENGINE_VENV_PY.exists():
        candidates.append(str(ENGINE_VENV_PY))
    for py in candidates:
        if run_quiet([py, "-c", "import whisper"]).returncode == 0:
            return py
    return None


def transcribe(path: pathlib.Path, out_json: pathlib.Path, model: str) -> dict | None:
    py = whisper_python()
    if not py:
        note("Whisper is not installed, so no transcript. That's fine; the rest still works.")
        note("To add one later: python3 -m pip install -r engine/requirements.txt")
        return None
    note(f"transcribing with Whisper '{model}' (first run downloads the model)...")
    with tempfile.TemporaryDirectory() as td:
        wav = pathlib.Path(td) / "a.wav"
        ffio.run([ffio.ffmpeg(), "-v", "error", "-y", "-i", str(path), "-vn",
                  "-ac", "1", "-ar", "16000", str(wav)])
        r = subprocess.run([py, "-c", WHISPER_SNIPPET, str(wav), str(out_json), model],
                           capture_output=True, text=True)
    if r.returncode != 0 or not out_json.exists():
        note(f"Whisper failed, skipping transcript: {r.stderr.strip()[-300:]}")
        return None
    return json.loads(out_json.read_text())


# --------------------------------------------------------------------------- breakdown

def pacing_words(cps: float, asl: float) -> str:
    if asl <= 1.0:
        return "very fast: a new shot roughly every second or less (high-energy, MrBeast-style pacing)"
    if asl <= 2.0:
        return "fast: cuts every 1-2 seconds (typical punchy Reel/TikTok edit)"
    if asl <= 4.0:
        return "medium: cuts every 2-4 seconds (talking head with regular punch-ins/b-roll)"
    return "slow: long takes (calm, single-shot or minimal-cut talking head)"


def write_breakdown(d: pathlib.Path, src_label: str, meta: dict, info: dict,
                    shots: list[dict], cuts: list[float], audio: dict | None,
                    transcript: dict | None, sheet_note: str, frames: list[str]) -> None:
    dur = info["duration"]
    n_shots = len(shots)
    asl = dur / n_shots if n_shots else dur
    cps = len(cuts) / dur if dur else 0
    longest = max(shots, key=lambda s: s["length"]) if shots else None
    shortest = min(shots, key=lambda s: s["length"]) if shots else None
    first_cut = cuts[0] if cuts else None
    cuts_first3 = len([c for c in cuts if c < 3])

    L: list[str] = []
    L.append(f"# Reference breakdown: {meta.get('title') or src_label}\n")
    L.append(f"- **Source:** {meta.get('webpage_url') or meta.get('url') or src_label}")
    if meta.get("uploader") or meta.get("channel"):
        L.append(f"- **Creator:** {meta.get('uploader') or meta.get('channel')}")
    L.append(f"- **Analysed:** {dt.date.today().isoformat()} with `engine/scripts/reference.py`")
    L.append("- **Use:** studying style only. Don't republish this footage or put it in "
             "your own video.\n")

    L.append("## The numbers (measured, not guessed)\n")
    L.append("| | |\n|---|---|")
    L.append(f"| Length | {dur:.1f}s |")
    L.append(f"| Frame | {info['width']}x{info['height']} ({info['aspect']}, {info['orientation']}) "
             f"at {info['fps']:g} fps |")
    L.append(f"| Shots | {n_shots} ({len(cuts)} hard cuts) |")
    L.append(f"| Average shot length | {asl:.2f}s |")
    L.append(f"| Cuts per second | {cps:.2f} (a new shot every {asl:.1f}s on average) |")
    L.append(f"| First cut | {fmt_s(first_cut)} |")
    L.append(f"| Cuts in the first 3 seconds | {cuts_first3} |")
    if longest:
        L.append(f"| Longest / shortest shot | {longest['length']:.2f}s (#{longest['n']}) / "
                 f"{shortest['length']:.2f}s (#{shortest['n']}) |")
    if audio:
        if "integrated_lufs" in audio:
            L.append(f"| Loudness | {audio['integrated_lufs']:.1f} LUFS integrated, "
                     f"range {audio.get('loudness_range_lu', 0):.1f} LU, "
                     f"peak {audio.get('true_peak_dbfs', 0):.1f} dBFS |")
        L.append(f"| Silence | {audio['silent_seconds']:.1f}s total "
                 f"({(audio['silent_share'] or 0) * 100:.0f}%), {audio['pauses']} pauses |")
        L.append(f"| Sound (rough guess) | {audio['character_guess']} |")
    else:
        L.append("| Audio | none |")
    if transcript and transcript.get("words"):
        words = transcript["words"]
        talk = max(0.001, words[-1]["e"] - words[0]["s"])
        L.append(f"| Speech | {len(words)} words, first word at {words[0]['s']:.2f}s, "
                 f"{len(words) / talk * 60:.0f} words/min |")
    L.append("")
    L.append(f"**Pacing in plain words:** {pacing_words(cps, asl)}.\n")
    L.append("Note: scene detection catches hard cuts. Fast zooms, whip pans and big text "
             "changes sometimes count as cuts; slow dissolves and punch-ins on the same "
             "shot sometimes don't. Check against the contact sheet.\n")

    L.append("## Shot list\n")
    L.append("| # | Start | End | Length |\n|---|---|---|---|")
    for s in shots[:80]:
        L.append(f"| {s['n']} | {s['start']:.2f}s | {s['end']:.2f}s | {s['length']:.2f}s |")
    if len(shots) > 80:
        L.append(f"| ... | {len(shots) - 80} more in analysis.json | | |")
    L.append("")

    if transcript and transcript.get("text"):
        L.append("## What is said\n")
        L.append(f"> {transcript['text']}\n")
        L.append("(Whisper transcript; brand names are often misheard. Word timings in "
                 "`transcript.json`.)\n")
    elif transcript is None:
        L.append("## What is said\n")
        L.append("_No transcript (Whisper not installed, or no speech). Claude: describe "
                 "the spoken hook from the frames/captions if visible._\n")

    L.append("## Pictures to look at\n")
    L.append(f"- `contact.png`: {sheet_note}, labelled with time and shot number.")
    L.append("- `frames/`: " + ", ".join(f"`{f}`" for f in frames[:20])
             + (" ..." if len(frames) > 20 else ""))
    L.append("")

    L.append("## What's on screen (Claude fills this in after viewing the frames)\n")
    for item in (
        "**Framing / composition:** _(e.g. chest-up presenter centred, eyes at top third; "
        "split-screen; full-screen b-roll)_",
        "**Text on screen:** _(title at top? how long does it stay? font feel: bold sans, "
        "serif italic, handwritten; colour; outline/box)_",
        "**Captions:** _(word-by-word / phrase / none; position; highlight colour on the "
        "active word; all caps?)_",
        "**Overlays & b-roll:** _(screenshots, product shots, memes, icons, emoji; behind "
        "or in front of the speaker; how often)_",
        "**Camera moves:** _(punch-ins on emphasis, slow push, static, handheld)_",
        "**Colour / grade:** _(warm, cool, high contrast, desaturated, brand colours)_",
        "**Transitions:** _(hard cuts only, whooshes, zoom transitions, flashes)_",
    ):
        L.append(f"- {item}")
    L.append("")

    L.append("## Make mine like this (checklist)\n")
    L.append("Claude fills in each line after viewing `contact.png` and `frames/`, "
             "then maps it to this repo (`styles/`, `recipes/`).\n")
    for item in (
        f"**Hook in the first second:** what grabs you before 1.0s? "
        f"(see `frames/hook_*`; first cut at {fmt_s(first_cut)}) _..._",
        "**Title style:** _..._",
        "**Caption style:** _..._",
        "**Overlay pattern:** _(what appears, how often, where)_ _..._",
        "**Colour / grade:** _..._",
        "**Music / energy:** "
        + (f"_{audio['character_guess']}; {audio.get('integrated_lufs', 'n/a')} LUFS_ "
           if audio else "_silent_ ") + "_..._",
        f"**Pacing:** aim for ~{asl:.1f}s average shots, ~{cps:.2f} cuts/sec "
        f"(~{round(cps * 30)} cuts in a 30s video) _..._",
        "**Closest existing style in `styles/`:** _(yap-depth / oren-static-hooks / "
        "editorial-tech / new)_",
        "**What to do differently for my brand:** _..._",
    ):
        L.append(f"- [ ] {item}")
    L.append("")
    (d / "breakdown.md").write_text("\n".join(L))


# --------------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Break down a reference video (link or file) into measured style notes.")
    ap.add_argument("source", help="video link (Instagram, TikTok, YouTube, ...) or a local file path")
    ap.add_argument("--name", help="folder name under references/videos/ (default: from the link/file)")
    ap.add_argument("--cookies-from-browser", metavar="BROWSER",
                    help="use your own logged-in browser session for sites that need it "
                         "(chrome, safari, firefox, edge, brave)")
    ap.add_argument("--threshold", type=float, default=SCENE_THRESHOLD,
                    help=f"scene-cut sensitivity 0-1, lower finds more cuts (default {SCENE_THRESHOLD})")
    ap.add_argument("--no-transcript", action="store_true", help="skip Whisper even if installed")
    ap.add_argument("--whisper-model", default="small", help="Whisper model (default small)")
    ap.add_argument("--force", action="store_true", help="re-download even if source.mp4 exists")
    args = ap.parse_args()

    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or newer is needed.")
    ffio.ffmpeg(), ffio.ffprobe()  # exit early with install help if missing

    meta: dict = {}
    if is_url(args.source):
        src, meta = download(args.source.strip(), args.name, args.cookies_from_browser, args.force)
        src_label = args.source.strip()
    else:
        src = pathlib.Path(os.path.expanduser(args.source.strip().strip("'\""))).resolve()
        if not src.exists():
            sys.exit(f"Can't find the file: {src}\nTip: drag the file into the chat to paste its path.")
        src_label = src.name
        meta = {"local_file": str(src)}
    slug = slugify(args.name) if args.name else (
        src.parent.name if src.parent.parent == OUT_ROOT else slugify(src.stem))
    d = OUT_ROOT / slug
    d.mkdir(parents=True, exist_ok=True)
    frames_dir = d / "frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir()

    step("Measuring the video")
    info = probe(src)
    note(f"{info['duration']:.2f}s  {info['width']}x{info['height']} ({info['aspect']})  "
         f"{info['fps']:g} fps  audio: {'yes' if info['has_audio'] else 'no'}")

    step("Finding cuts")
    cuts = detect_cuts(src, info["duration"], args.threshold)
    shots = shots_from_cuts(cuts, info["duration"])
    asl = info["duration"] / len(shots) if shots else info["duration"]
    note(f"{len(cuts)} cuts -> {len(shots)} shots, average shot {asl:.2f}s, "
         f"{len(cuts) / info['duration'] if info['duration'] else 0:.2f} cuts/sec")
    if cuts:
        note("cuts at: " + ", ".join(f"{c:.2f}" for c in cuts[:25]) + (" ..." if len(cuts) > 25 else ""))

    step("Grabbing frames")
    frames: list[str] = []
    big_h = 960 if info["height"] >= info["width"] else 540
    for t in (0.0, 0.5, 1.0):
        if t < info["duration"]:
            f = frames_dir / f"hook_{t:.1f}s.jpg"
            if grab(src, t, f, big_h):
                frames.append(f"frames/{f.name}")
    pick = shots
    if len(shots) > MAX_SHOT_FRAMES:  # spread evenly, always keep first and last
        idx = sorted({round(i * (len(shots) - 1) / (MAX_SHOT_FRAMES - 1))
                      for i in range(MAX_SHOT_FRAMES)})
        pick = [shots[i] for i in idx]
    for s in pick:
        t = s["start"] + s["length"] / 2
        f = frames_dir / f"shot{s['n']:02d}_{t:.2f}s.jpg"
        if grab(src, t, f, big_h):
            frames.append(f"frames/{f.name}")
    note(f"{len(frames)} frames in {frames_dir.relative_to(REPO)}/")

    step("Building the contact sheet")
    times, sheet_note = sheet_times(shots, info["duration"])
    shot_of = [next((s["n"] for s in shots if s["start"] <= t < s["end"]), 0) for t in times]
    contact = d / "contact.png"
    if build_contact_sheet(src, info, times, shot_of, contact):
        note(f"{contact.relative_to(REPO)}  ({len(times)} tiles, {sheet_note})")
    else:
        note("could not build the contact sheet; look at frames/ instead")

    audio = None
    if info["has_audio"]:
        step("Listening to the audio")
        try:
            audio = audio_stats(src, info["duration"])
            if "integrated_lufs" in audio:
                note(f"{audio['integrated_lufs']:.1f} LUFS, {audio['silent_share'] * 100:.0f}% silence, "
                     f"{audio['pauses']} pauses")
            note(f"guess: {audio['character_guess']}")
        except Exception as e:  # never let audio sink the whole run
            note(f"audio analysis skipped: {e}")
    else:
        note("no audio track")

    transcript = None
    tpath = d / "transcript.json"
    if tpath.exists():
        tpath.unlink()
    if info["has_audio"] and not args.no_transcript:
        step("Transcript")
        transcript = transcribe(src, tpath, args.whisper_model)
        if transcript:
            note(f"{len(transcript['words'])} words: {transcript['text'][:140]}")

    analysis = {"source": src_label, "source_path": str(src), "meta": meta, "video": info,
                "scene_threshold": args.threshold, "cuts": cuts, "shots": shots,
                "average_shot_length": round(asl, 3),
                "cuts_per_second": round(len(cuts) / info["duration"], 3) if info["duration"] else 0,
                "audio": audio, "transcript": "transcript.json" if transcript else None,
                "frames": frames, "contact_sheet": "contact.png" if contact.exists() else None}
    (d / "analysis.json").write_text(json.dumps(analysis, indent=1))
    write_breakdown(d, src_label, meta, info, shots, cuts, audio, transcript, sheet_note, frames)

    step("Done")
    rel = d.relative_to(REPO)
    print(f"    {rel}/breakdown.md   <- the breakdown (fill in the on-screen notes + checklist)")
    print(f"    {rel}/contact.png    <- look at this first")
    print(f"    {rel}/frames/        <- hook frames + one per shot")
    print(f"    {rel}/analysis.json  <- all numbers")
    print("\nReminder: this video is for studying style. Don't republish it or put its "
          "footage in your own video.")


if __name__ == "__main__":
    main()
