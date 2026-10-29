# Yap audio: cleanup and Instagram loudness

Start with the full-script edit plan in `yap.md` before implementing a Yap edit.

Every Yap edit gets this audio pass. Reference implementation: `output/yap-5658/audio.py` (the build calls it and muxes `master.wav`).

1. **Cleanup** — DeepFilterNet 3 (local AI speech enhancement) on the whole source take, before cutting. It lives in its own env, `.venv-df/` (torch/torchaudio 2.5.1, numpy<2, soundfile), so it cannot break the main `.venv`. The `deepFilter` CLI writes its file and then hangs on exit: stop it once the output stops growing.
2. **Polish** — highpass 80 Hz, -2 dB at 250 Hz, +2 dB at 3.5 kHz, de-esser, gentle compressor (3:1 at -22 dB).
3. **Cut** — same clips and speed as the picture, 12 ms fades at each join.
4. **Level** — -14 LUFS integrated, true peak at or below -1.5 dBTP. Gain to target plus a 4x-oversampled limiter; plain loudnorm cannot reach -14 when the raw take has clipped peaks. Measure the final file and fail the build if it is off target.

Cost: about 30 s of CPU per 2-minute take. Listen on headphones before shipping; the numbers do not tell you whether the cleanup sounds natural.

## Editorial tightening after a draft

Combine the full retained script with raw/enhanced waveform inspection. Review loud non-speech between phrases (chuckles, mic-blown breaths, mouth noises, handling bursts) as well as silence; do not equate waveform energy with meaningful speech. Locate exact source boundaries, remove unnecessary pauses/false starts while preserving the selected second take and word edges, and recheck each changed join in context. Revalidate the final encoded audio and picture mapping. Do not describe numerical/transcript validation as a listening pass; disclose any auditory limitation.
