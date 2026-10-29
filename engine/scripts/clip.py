#!/usr/bin/env python3
"""Cut and stitch real footage. The timeline-free edit tool.

    python3 scripts/clip.py cut    <in.mp4> <out.mp4> <start> <end>
    python3 scripts/clip.py stitch <out.mp4> <in1.mp4> <in2.mp4> [more...]
                                   [--mute]

cut     Frame-accurate trim, re-encoded (stream-copy cuts snap to keyframes
        and land up to 2s off; the re-encode is what makes <start> mean
        <start>). Times in seconds, decimals fine.

stitch  Hard-cut concatenation, in argument order. Every clip is normalised
        to the FIRST clip's resolution and frame rate (scaled to fit, padded,
        never stretched), audio resampled to 48kHz stereo. Hard cuts only, on
        purpose: no crossfades, no dissolves — that rule predates this tool.
        --mute drops audio entirely (for clips that will get a voiceover or
        bed later); without it, every input must have an audio track, and a
        clip that has none is an error rather than a silently broken output.

Both print the MEASURED duration of the output. Needs a real ffmpeg (see
ffio.py's error message if you don't have one).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffio

ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart"]


def cut(src, dst, start, end):
    if not (0 <= start < end):
        sys.exit(f"bad range: start={start} end={end}")
    ffio.run([ffio.ffmpeg(), "-y", "-v", "error", "-i", src,
              "-ss", f"{start}", "-to", f"{end}",
              *ENC, "-c:a", "aac", "-b:a", "192k", dst])
    ffio.report(dst)


def stitch(dst, srcs, mute):
    if len(srcs) < 2:
        sys.exit("stitch needs at least two input clips")
    infos = [ffio.probe(s) for s in srcs]
    if not mute:
        for s, i in zip(srcs, infos):
            if not i["has_audio"]:
                sys.exit(
                    f"{s} has no audio track. Either give every clip audio, "
                    "or pass --mute to stitch video-only (add a voiceover or "
                    "bed at the format stage instead)."
                )
    w, h, fps = infos[0]["w"], infos[0]["h"], round(infos[0]["fps"], 3)

    parts, labels = [], []
    for n in range(len(srcs)):
        parts.append(
            f"[{n}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps}[v{n}]")
        if not mute:
            parts.append(
                f"[{n}:a]aresample=48000,"
                f"aformat=channel_layouts=stereo[a{n}]")
            labels.append(f"[v{n}][a{n}]")
        else:
            labels.append(f"[v{n}]")
    av = "" if mute else ":a=1"
    parts.append(
        f"{''.join(labels)}concat=n={len(srcs)}:v=1{av}[vo]"
        + ("" if mute else "[ao]"))

    cmd = [ffio.ffmpeg(), "-y", "-v", "error"]
    for s in srcs:
        cmd += ["-i", s]
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vo]"]
    if not mute:
        cmd += ["-map", "[ao]", "-c:a", "aac", "-b:a", "192k"]
    cmd += [*ENC, dst]
    ffio.run(cmd)
    ffio.report(dst)


def main():
    args = [a for a in sys.argv[1:] if a != "--mute"]
    mute = "--mute" in sys.argv
    if len(args) >= 2 and args[0] == "cut" and len(args) == 5:
        cut(args[1], args[2], float(args[3]), float(args[4]))
    elif len(args) >= 4 and args[0] == "stitch":
        stitch(args[1], args[2:], mute)
    else:
        sys.exit(__doc__.strip())


if __name__ == "__main__":
    main()
