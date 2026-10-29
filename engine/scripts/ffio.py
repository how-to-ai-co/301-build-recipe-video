"""Shared ffmpeg plumbing for clip.py and overlay.py.

These tools need a REAL ffmpeg (the slim binary Remotion bundles for its own
rendering has no lavfi and almost no filters). On a Mac that means Homebrew,
and installing Homebrew needs the operator's password, so the error message
below points at the same walkthrough the preflight stage uses.
"""
import json
import shutil
import subprocess
import sys


def _find(name, env):
    import os
    p = os.environ.get(env) or shutil.which(name)
    if not p:
        sys.exit(
            f"{name} not found. Creator-clip work needs a real {name} "
            "(the one Remotion bundles is too minimal). On a Mac: install "
            "Homebrew from https://brew.sh (needs your password, so a human "
            "does this part), then `brew install ffmpeg`, then rerun."
        )
    return p


def ffmpeg():
    return _find("ffmpeg", "FFMPEG")


def ffprobe():
    return _find("ffprobe", "FFPROBE")


def run(cmd):
    subprocess.run(cmd, check=True)


def probe(path):
    """width, height, fps, duration, has_audio for one media file."""
    out = subprocess.run(
        [ffprobe(), "-v", "error", "-print_format", "json",
         "-show_streams", "-show_format", str(path)],
        check=True, capture_output=True, text=True).stdout
    info = json.loads(out)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {
        "w": int(v["width"]),
        "h": int(v["height"]),
        "fps": float(num) / float(den or 1),
        "duration": float(info["format"]["duration"]),
        "has_audio": any(s["codec_type"] == "audio" for s in info["streams"]),
    }


def report(path):
    """Print the MEASURED duration. Never report a length you did not measure."""
    p = probe(path)
    print(f"wrote {path}  {p['duration']:.2f}s  {p['w']}x{p['h']}")
