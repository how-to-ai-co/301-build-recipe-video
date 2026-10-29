#!/usr/bin/env python3
"""Yap kit: talking-head edit for Instagram in one config script.

    from yap import Yap
    y = Yap('~/Downloads/IMG_1234.MOV', 'output/yap-1234', 'My-Video', ['One-line title?'])
    y.stumble(70.85, 72.75)                           # cut a false start (source seconds)
    y.flash(y.logo('assets/claude.png'), 4.1)        # simple reference, 1.5 output seconds by default
    y.hold(y.picture('assets/chart.png'), 7.1, 4.5)  # readable reference, held
    y.cta(81.3, ['Comment "AI 101"'])                # title swaps for the call to action
    y.render(1)

Pipeline (recipes/flash-overlays.md, recipes/yap-audio.md):
  cuts     measured silences shortened to 2*KEEP, plus explicit stumbles
  speed    one constant per video: 225 / the take's average wpm, clamped 1.03-1.07
  audio    DeepFilterNet -> voice polish -> per-clip trim/tempo -> -14 LUFS, TP <= -1.5
  picture  1080x1920, title card, overlays inside the Instagram safe area
  outputs  <dir>/<Name>-Yap-vN.mp4, copy in ~/Downloads, 540p preview for inline chat
"""
import json, math, os, re, shutil, subprocess, sys, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SF = '/System/Library/Fonts/SFNS.ttf'
W, H, FPS = 1080, 1920, 30
SAFE_X, SAFE_Y = (35, 980), (220, 1470)       # user's Instagram guide at 1080x1920
TOP = 440                                      # first free row under the title card
TARGET_I, TARGET_TP = -14.0, -1.5
POLISH = ('highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,deesser=i=0.35,'
          'acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=4')


def resolve_overlay_intervals(overlays, source_to_output, total):
    """Resolve explicit holds without silently shortening overlaps or the final event.

    Cue/end arguments are source times. A duration is already in output seconds.
    Final intervals use inclusive start and exclusive end frames at FPS.
    """
    if not math.isfinite(total) or total <= 0:
        raise ValueError('Video duration must be positive and finite')
    resolved = []
    for o in overlays:
        start = source_to_output(o['src0'])
        _, dur = o['kind']
        if o['src1'] is not None:
            end = source_to_output(o['src1'])
        else:
            duration = 2.0 if dur is None else dur
            if not math.isfinite(duration) or duration <= 0:
                raise ValueError('Overlay duration must be positive and finite')
            end = start + duration
        if not all(math.isfinite(t) for t in (start, end)) or start < 0 or end <= start:
            raise ValueError(f'Invalid overlay interval: {start}–{end}')
        if end > total + 1e-6:
            raise ValueError(f'Overlay {start:.3f}–{end:.3f}s exceeds video end {total:.3f}s; revise its planned hold')
        first, last = round(start * FPS), round(end * FPS)
        if last <= first:
            raise ValueError('Overlay is shorter than one output frame')
        resolved.append({**o, 'start': first / FPS, 'end': last / FPS,
                         'start_frame': first, 'end_frame': last})
    resolved.sort(key=lambda o: o['start_frame'])
    for left, right in zip(resolved, resolved[1:]):
        if left['end_frame'] > right['start_frame']:
            raise ValueError(f"Overlapping overlays at {right['start']:.3f}s; resolve the cue sheet instead of shortening a hold")
    return resolved


def ff(*a): subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', *a], check=True)


def font(size, weight):
    f = ImageFont.truetype(SF, size); f.set_variation_by_name(weight); return f


def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(path), '-af', f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA=7:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True, check=True).stderr
    return json.JSONDecoder().raw_decode(r[r.rfind('{'):])[0]


class Yap:
    def __init__(self, source, out_dir, name, title, keep=0.04, min_silence=0.15, noise_db=-35, target_wpm=225, speed_range=(1.03, 1.07)):
        self.src = str(Path(source).expanduser()); self.dir = ROOT / out_dir; self.name = name
        self.assets = self.dir / 'assets'; self.review = self.dir / 'review'
        for d in (self.assets, self.review, self.dir / 'audio'): d.mkdir(parents=True, exist_ok=True)
        self.title, self.keep, self.min_silence, self.noise_db, self.target, self.srange = title, keep, min_silence, noise_db, target_wpm, speed_range
        self.stumbles, self.overlays, self.cta_at, self.cta_lines = [], [], None, None
        self.words = json.loads((self.dir / 'words.json').read_text())
        self.duration = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', self.src],
                                             capture_output=True, text=True).stdout)
        self.clips = None

    # ---------- edit decisions ----------
    def stumble(self, start, end): self.stumbles.append((start, end)); self.clips = None

    def plan(self):
        """Clips from measured silence + stumbles, each with a words-per-minute speed."""
        if self.clips is not None: return self.clips
        log = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(self.clean()), '-af', f'silencedetect=noise={self.noise_db}dB:d={self.min_silence}', '-f', 'null', '-'],
                             capture_output=True, text=True).stderr
        m = [float(x) for x in re.findall(r'silence_(?:start|end): ([\d.]+)', log)]
        if len(m) % 2: m.append(self.duration)
        first, last = self.words[0]['s'], self.words[-1]['e']
        cuts = [(0, max(0, first - 0.15)), (last + 0.25, self.duration)]
        cuts += [(s + self.keep if s > 0 else 0, e - self.keep if e < self.duration - 0.1 else self.duration) for s, e in zip(m[::2], m[1::2])]
        cuts = sorted(c for c in cuts + self.stumbles if c[1] - c[0] > 0.03)
        clips, t = [], 0.0
        for s, e in cuts:
            if s > t: clips.append([t, s])
            t = max(t, e)
        if t < self.duration: clips.append([t, self.duration])
        clips = [[round(s * FPS) / FPS, round(e * FPS) / FPS] for s, e in clips if e - s > 0.1]
        # ONE speed for the whole video: target wpm over this take's average speaking rate, clamped.
        talk = sum(e - s for s, e in clips); wpm = len(self.words) / talk * 60
        self.wpm = wpm; speed = min(self.srange[1], max(self.srange[0], self.target / wpm))
        speeds = [speed] * len(clips)
        self.clips = [(s, e, round(v, 3)) for (s, e), v in zip(clips, speeds)]
        return self.clips

    def out(self, t):
        return sum(max(0, min(t, e) - s) / v for s, e, v in self.plan())

    # ---------- assets ----------
    def asset(self, stem):
        """assets/<stem>.* (whatever extension the download had)."""
        hits = sorted(x for x in self.assets.glob(stem + '.*') if not x.stem.endswith('-cut'))
        if not hits: raise FileNotFoundError(f'{self.assets}/{stem}.*')
        return hits[0]

    def _img(self, path):
        p = Path(path); p = p if p.is_absolute() else self.dir / p
        im = Image.open(p).convert('RGBA'); return im.crop(im.getbbox() or (0, 0, *im.size))

    def cutout(self, path, person=True):
        """Background removed with macOS Vision: person segmentation for people, generic foreground for objects."""
        p = Path(path); p = p if p.is_absolute() else self.dir / p
        dst = p.with_name(p.stem + ('-cut.png' if person else '-objcut.png'))
        if not dst.exists(): subprocess.run([str(ROOT / ('engine/bin/cutout-person' if person else 'engine/bin/cutout')), str(p), str(dst)], check=True)
        return self._img(dst)

    def fit(self, im, w, h):
        im = im.copy(); s = min(w / im.width, h / im.height)
        if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.Resampling.LANCZOS)
        return im  # never upscale: a soft asset stays small

    def logo(self, path, size=190): return self.fit(self._img(path), size, size)
    def person(self, path, height=420, cut=True): return self.fit(self.cutout(path) if cut else self._img(path), 820, height)
    def picture(self, path, width=860, height=900, radius=28, bg=None):
        im = self.fit(self._img(path), width, height)
        if bg:  # transparent drawings need a card to read over footage
            pad = 30; card = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), bg); card.alpha_composite(im, (pad, pad)); im = card
        mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *im.size), radius=radius, fill=255)
        im.putalpha(Image.composite(im.getchannel('A'), mask, mask)); return im

    def stack(self, *ims, gap=24):
        im = Image.new('RGBA', (max(i.width for i in ims), sum(i.height for i in ims) + gap * (len(ims) - 1))); y = 0
        for i in ims: im.alpha_composite(i, ((im.width - i.width) // 2, y)); y += i.height + gap
        return im

    def pair(self, left, right=None, sep='vs'):
        f = font(110 if sep == '=' else 64, 'Heavy'); gap = 130
        w = left.width + gap + (right.width if right else 0); h = max(left.height, right.height if right else 0)
        im = Image.new('RGBA', (w, h)); im.alpha_composite(left, (0, (h - left.height) // 2))
        if right:
            ImageDraw.Draw(im).text((left.width + gap // 2, h // 2), sep, font=f, fill='white', anchor='mm', stroke_width=5, stroke_fill='black')
            im.alpha_composite(right, (left.width + gap, (h - right.height) // 2))
        return im

    # ---------- placement ----------
    def _place(self, im, y=TOP, x=None):
        x = (W - im.width) // 2 if x is None else x
        assert SAFE_X[0] <= x and x + im.width <= SAFE_X[1] and SAFE_Y[0] <= y and y + im.height <= SAFE_Y[1], f'overlay outside safe area: {x},{y} {im.size}'
        c = Image.new('RGBA', (W, H)); c.alpha_composite(im, (x, y)); return c

    def _add(self, im, t0, t1, kind, y, x):
        k = len(self.overlays); path = self.assets / f'ov-{k:02d}.png'; self._place(im, y, x).save(path)
        self.overlays.append({'png': str(path), 'src0': t0, 'src1': t1, 'kind': kind})

    def flash(self, im, t, dur=1.5, y=TOP, x=None):
        """Reference at a source cue, held for explicit output seconds; no duration cap."""
        if not math.isfinite(dur) or dur <= 0:
            raise ValueError('Overlay duration must be positive and finite')
        self._add(im, t, None, ('flash', dur), y, x)

    def hold(self, im, t, dur=None, until=None, y=TOP, x=None):
        """Readable references (charts, definitions, screenshots): held in output seconds or until a source time."""
        self._add(im, t, until, ('hold', dur), y, x)

    def cta(self, t, lines): self.cta_at, self.cta_lines = t, lines

    def bundle(self, mode, logos, move, t0, t1):
        """Remotion Bundle animation. logos: [(path, source_time_it_appears)]; move: source time the apps
        fly into (bundle) or burst out of (unbundle) the chat box; shown from t0 to t1 (source seconds)."""
        self.overlays.append({'anim': 'Bundle', 'mode': mode, 'logos': logos, 'move': move, 'src0': t0, 'src1': t1, 'kind': ('anim', None)})

    def _render_anim(self, o, k):
        start, end = self.out(o['src0']), self.out(o['src1']); fr = lambda t: max(0, round((self.out(t) - start) * FPS))
        pub = ROOT / 'engine/public/yap'; pub.mkdir(parents=True, exist_ok=True); logos = []
        for path, _ in o['logos']:
            src = Path(path); src = src if src.is_absolute() else self.dir / src
            dst = pub / f'{self.dir.name}-{src.name}'; shutil.copy2(src, dst); logos.append(f'yap/{dst.name}')
        props = {'mode': o['mode'], 'logos': logos, 'appear': [fr(t) for _, t in o['logos']], 'moveAt': fr(o['move']), 'duration': round((end - start) * FPS)}
        mov = self.assets / f"anim-{k:02d}-{o['mode']}.mov"
        subprocess.run(['npx', 'remotion', 'render', 'src/yap/index.ts', o['anim'], str(mov), '--codec=prores', '--prores-profile=4444',
                        '--pixel-format=yuva444p10le', '--image-format=png', '--log=error', f'--props={json.dumps(props)}'], cwd=ROOT / 'engine', check=True)
        return str(mov), props

    def title_png(self, lines, path):
        b, r = font(68, 'Bold'), font(50, 'Regular'); d = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        w = max(d.textlength(lines[0], font=b), d.textlength(lines[1], font=r) if len(lines) > 1 else 0)
        im = Image.new('RGBA', (W, H)); dr = ImageDraw.Draw(im); bottom = 235 + (162 if len(lines) > 1 else 95)
        dr.rounded_rectangle((540 - w / 2 - 28, 235, 540 + w / 2 + 28, bottom), radius=24, fill='black')
        dr.text((540, 284), lines[0], font=b, fill='white', anchor='mm')
        if len(lines) > 1: dr.text((540, 354), lines[1], font=r, fill='white', anchor='mm')
        im.save(path); return path

    # ---------- audio ----------
    def clean(self):
        """DeepFilterNet-cleaned source audio (cached). Silence is measured on this, not the noisy original."""
        a = self.dir / 'audio'; raw, clean = a / 'source-48k.wav', a / 'source-48k_DeepFilterNet3.wav'
        if not clean.exists():
            ff('-i', self.src, '-vn', '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', '-y', str(raw))
            proc = subprocess.Popen([str(ROOT / '.venv-df/bin/deepFilter'), '-o', str(a), str(raw)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            size = -1
            for _ in range(600):  # deepFilter writes the file then hangs on exit
                time.sleep(2)
                if proc.poll() is not None: break
                if clean.exists() and clean.stat().st_size == size > 0: proc.kill(); break
                size = clean.stat().st_size if clean.exists() else -1
            if not clean.exists(): sys.exit('DeepFilterNet produced no output')
        return clean

    def audio(self):
        clean, a = self.clean(), self.dir / "audio"
        clips = self.plan(); n = len(clips)
        parts = ';'.join(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={e - s - 0.012:.3f}:d=0.012,atempo={v}[a{i}]"
                         for i, (s, e, v) in enumerate(clips))
        (a / 'filter.txt').write_text(f"{parts};{''.join(f'[a{i}]' for i in range(n))}concat=n={n}:v=0:a=1,{POLISH}[o]")
        cut, master = a / 'cut.wav', self.dir / 'master.wav'
        ff('-i', str(clean), '-/filter_complex', str(a / 'filter.txt'), '-map', '[o]', '-ar', '48000', '-c:a', 'pcm_f32le', '-y', str(cut))
        before = loudness(cut); gain = TARGET_I - float(before['input_i'])
        for _ in range(8):  # gain + 4x-oversampled limiter, nudged until on target
            ff('-i', str(cut), '-af', f'volume={gain:.2f}dB,aresample=192000,alimiter=limit={10 ** ((TARGET_TP - 0.7) / 20):.4f}:attack=1:release=50:level=disabled,aresample=48000',
               '-c:a', 'pcm_s24le', '-y', str(master))
            got = float(loudness(master)['input_i'])
            if abs(got - TARGET_I) <= 0.2: break
            gain += 1.3 * (TARGET_I - got)
        after = loudness(master)
        (self.dir / 'master-measure.json').write_text(json.dumps({'before': before, 'after': after}, indent=1))
        print(f"audio: {before['input_i']} LUFS / {before['input_tp']} dBTP -> {after['input_i']} LUFS / {after['input_tp']} dBTP")
        assert abs(float(after['input_i']) - TARGET_I) <= 0.5 and float(after['input_tp']) <= TARGET_TP + 0.1, 'loudness off target'
        return master

    # ---------- render ----------
    def render(self, version):
        clips = self.plan(); total = self.out(1e9)
        ovs = resolve_overlay_intervals(self.overlays, self.out, total)
        for k, o in enumerate(ovs):
            if 'anim' in o:
                o['png'] = None
                o['mov'], o['props'] = self._render_anim(o, k)
        titles = [(self.title_png(self.title, self.assets / 'title.png'), 0, self.out(self.cta_at) if self.cta_at else total)]
        if self.cta_at: titles.append((self.title_png(self.cta_lines, self.assets / 'title-cta.png'), self.out(self.cta_at), total))
        speeds = [v for *_, v in clips]
        (self.dir / 'edit.json').write_text(json.dumps({'source': self.src, 'title': self.title, 'cta': [self.cta_at, self.cta_lines], 'stumbles': self.stumbles,
            'speed': {'target_wpm': self.target, 'min': min(speeds), 'max': max(speeds), 'mean': sum(speeds) / len(speeds)},
            'clips': clips, 'duration': total, 'overlays': ovs}, indent=1, default=str))
        master = self.audio()
        fc = [f"[0:v]trim={s}:{e},setpts=(PTS-STARTPTS)/{v}[v{i}]" for i, (s, e, v) in enumerate(clips)]
        fc.append(''.join(f'[v{i}]' for i in range(len(clips))) + f'concat=n={len(clips)}:v=1:a=0,scale={W}:{H},setsar=1,fps={FPS}[b0]')
        inputs, k = ['-i', self.src], 0
        for png, s, e in titles:
            inputs += ['-i', str(png)]; fc.append(f"[b{k}][{k + 1}:v]overlay=0:0:enable='between(t,{s:.3f},{e - 0.001:.3f})'[b{k + 1}]"); k += 1
        for o in ovs:
            if o.get('mov'):  # alpha animation, shifted to its start time
                inputs += ['-i', o['mov']]; fc.append(f"[{k + 1}:v]setpts=PTS-STARTPTS+{o['start']}/TB[m{k}];[b{k}][m{k}]overlay=0:0:eof_action=pass:enable='gte(n,{o['start_frame']})*lt(n,{o['end_frame']})'[b{k + 1}]")
            else:
                inputs += ['-i', o['png']]; fc.append(f"[b{k}][{k + 1}:v]overlay=0:0:enable='gte(n,{o['start_frame']})*lt(n,{o['end_frame']})'[b{k + 1}]")
            k += 1
        inputs += ['-i', str(master)]
        (self.dir / 'filter.txt').write_text(';\n'.join(fc))
        dst = self.dir / f'{self.name}-Yap-v{version}.mp4'
        ff(*inputs, '-/filter_complex', str(self.dir / 'filter.txt'), '-map', f'[b{k}]', '-map', f'{k + 1}:a',
           '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-y', str(dst))
        shutil.copy2(dst, Path.home() / 'Downloads' / dst.name)
        prev_dir = Path(os.environ.get('YAP_PREVIEW_DIR', '/tmp/yap-previews')); prev_dir.mkdir(parents=True, exist_ok=True)
        prev = prev_dir / f'{self.name}-v{version}.mp4'  # no spaces in this path, or the chat won't play it inline
        ff('-i', str(dst), '-vf', 'scale=540:960', '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'fast', '-crf', '30', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-y', str(prev))
        real = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(dst)], capture_output=True, text=True).stdout)
        print(f'{dst.name}: {real:.2f}s (source {self.duration:.1f}s), {len(clips)} clips, speed {min(speeds):.3f}-{max(speeds):.3f}x, '
              f'{len(ovs)} overlays\npreview: {prev}')
        return dst, prev

    def frames(self, version, times, name='check'):
        """Contact sheet of output frames at the given output times, for visual review."""
        dst = self.dir / f'{self.name}-Yap-v{version}.mp4'; sheet = Image.new('RGB', (360 * len(times), 640))
        for i, t in enumerate(times):
            f = self.review / f'_f{i}.png'; ff('-ss', str(t), '-i', str(dst), '-frames:v', '1', '-vf', 'scale=360:640', '-y', str(f))
            sheet.paste(Image.open(f), (360 * i, 0))
        path = self.review / f'{name}.jpg'; sheet.save(path, quality=88); return path
