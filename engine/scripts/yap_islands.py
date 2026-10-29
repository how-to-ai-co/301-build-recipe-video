#!/usr/bin/env python3
"""Zero-gap trim prep for a Yap video (recipes/yap.md, "Trim method").

    python engine/scripts/yap_islands.py output/<project>     # needs raw_DeepFilterNet3.wav and whisper.json there

Writes peak_enh.npy, islands.json (sound islands split at every >=50 ms silence on the CLEANED track) and
short-islands.json (each island under 1 s transcribed on its own, with the words whisper placed around it),
then prints the short islands so non-words (um, breath, click) and stumbles can be chosen for DROP.
"""
import json, sys, pathlib
import numpy as np, soundfile as sf, whisper

P = pathlib.Path(sys.argv[1]); H = 0.005
x, sr = sf.read(P / 'raw_DeepFilterNet3.wav'); hop = int(sr * H)
pk = 20 * np.log10(np.abs(x[:len(x) // hop * hop]).reshape(-1, hop).max(1) + 1e-9); np.save(P / 'peak_enh.npy', pk)
q = pk < -40; sil = []; i = 0
while i < len(q):
    if q[i]:
        j = i
        while j < len(q) and q[j]: j += 1
        if (j - i) * H >= 0.05: sil.append((i * H, j * H))
        i = j
    else: i += 1
isl = []; t = 0.0
for a, b in sil:
    if a - t > 0.02: isl.append((round(t, 3), round(a, 3)))
    t = b
isl.append((round(t, 3), round(len(pk) * H, 3)))
json.dump({'sil': sil, 'isl': isl}, open(P / 'islands.json', 'w'))
print(len(isl), 'islands; sound', round(sum(b - a for a, b in isl), 1), 's; silence', round(sum(b - a for a, b in sil), 1), 's')
m = whisper.load_model('small'); ws = [w for s in json.load(open(P / 'whisper.json'))['segments'] for w in s['words']]; out = []
for k, (a, b) in enumerate(isl):
    gp = a - isl[k - 1][1] if k else 9; gn = isl[k + 1][0] - b if k + 1 < len(isl) else 9
    if b - a <= 1.0:
        seg = x[max(0, int((a - 0.05) * sr)):int((b + 0.05) * sr)]; sf.write(P / '_tmp.wav', np.concatenate([np.zeros(sr // 4), seg, np.zeros(sr // 4)]), sr)
        r = m.transcribe(str(P / '_tmp.wav'), language='en', condition_on_previous_text=False, initial_prompt='Um, uh, hmm.')
        txt = r['text'].strip(); nsp = max([s['no_speech_prob'] for s in r['segments']] or [1])
        near = ' '.join(w['word'].strip() for w in ws if w['start'] < b + 0.15 and w['end'] > a - 0.15)
        out.append((a, b, txt, round(nsp, 2), near, round(gp, 2), round(gn, 2)))
        print(f'{a:7.2f}-{b:7.2f} ({b - a:.2f}) gaps {gp:.2f}/{gn:.2f} [{txt}] nsp={nsp:.2f} | {near}')
(P / '_tmp.wav').unlink(missing_ok=True); json.dump(out, open(P / 'short-islands.json', 'w'))
