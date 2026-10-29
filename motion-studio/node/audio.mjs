// node audio.mjs → out/score.wav   120 BPM score + SFX. The SFX times below match examples/showreel.html; move them to match your film. render.mjs mixes out/score.wav in automatically.
import { writeFileSync, mkdirSync } from 'node:fs';
const SR = 48000, DUR = 15.5, BEAT = 0.5, buf = new Float32Array(Math.ceil(DUR * SR));
let s = 42; const noise = () => (s = (s * 1664525 + 1013904223) >>> 0) / 2147483648 - 1;
const add = (t0, len, fn) => { const a = Math.floor(t0 * SR);
  for (let i = 0; i < len * SR && a + i < buf.length; i++) if (a + i >= 0) buf[a + i] += fn(i / SR); };
const hz = (m) => 440 * Math.pow(2, (m - 69) / 12);

const kick  = (t) => add(t, 0.4, x => Math.sin(2 * Math.PI * (45 * x + 60 * (1 - Math.exp(-x * 30)) / 30)) * Math.exp(-x * 9) * 0.9);
const hat   = (t, v = 0.12) => { let p = 0; add(t, 0.06, x => { const n = noise(), o = n - p; p = n; return o * Math.exp(-x * 70) * v; }); };
const click = (t) => add(t, 0.05, x => Math.sin(2 * Math.PI * 1800 * x) * Math.exp(-x * 90) * 0.35);
const pop   = (t, f = 600) => add(t, 0.15, x => Math.sin(2 * Math.PI * (f + 900 * x) * x) * Math.exp(-x * 30) * 0.3);
const whoosh = (end, len = 0.4) => add(end - len, len, x => noise() * Math.pow(x / len, 2) * 0.25);
const thump = (t) => add(t, 0.6, x => Math.sin(2 * Math.PI * (90 - 60 * x) * x) * Math.exp(-x * 7) * 0.9);
const bass = (t, m, len) => add(t, len, x => { const f = hz(m);
  return (Math.sin(2 * Math.PI * f * x) + 0.4 * Math.sin(4 * Math.PI * f * x) + 0.15 * Math.sin(6 * Math.PI * f * x))
    * Math.min(1, x * 200) * Math.exp(-x * 5) * 0.35; });
const pluck = (t, m, v = 0.18) => add(t, 0.5, x => { const f = hz(m);
  return (Math.sin(2 * Math.PI * f * x) + 0.5 * Math.sin(2 * Math.PI * 2 * f * x)) * Math.exp(-x * 8) * v; });

// Groove: kick on every beat, hats on the offbeat, bass in eighths, one pluck figure per bar
const roots = [45, 41, 48, 43];                       // A, F, C, G
const chords = [[69, 72, 76], [65, 69, 72], [72, 76, 79], [67, 71, 74]];
for (let b = 0; b < 30; b++) {
  const t = b * BEAT, bar = Math.floor(b / 4) % 4;
  if (t < 12 || t >= 12.5) kick(t);
  hat(t + BEAT / 2);
  bass(t, roots[bar], 0.24); bass(t + BEAT / 2, roots[bar] + 12, 0.2);
  if (b % 4 === 0 || b % 4 === 3) pluck(t + (b % 4 === 3 ? 0.25 : 0), chords[bar][b % 3]);
}
// SFX locked to picture
[0, 0.06, 0.12, 0.18].forEach((t) => click(t + 0.09));          // letters land
whoosh(2.0, 0.6); [2, 4, 6, 8, 10, 12].forEach(thump);           // cuts
[2.5, 3, 3.5].forEach((t) => pop(t, 700));                       // word steps
[4.5, 5, 5.5].forEach((t) => pop(t, 500)); whoosh(5.65, 0.3);    // morphs, flood
for (let i = 0; i < 6; i++) pop(8.15 + i * 0.12, 400 + i * 120); // bars
whoosh(12, 0.7);                                                 // tunnel exit
click(12.15); whoosh(12.3, 0.2); thump(12.5);                    // dot, rule
for (let i = 0; i < 33; i++) if (i % 2 === 0) click(12.85 + i * 0.03);  // typing
chords[0].forEach((m) => pluck(12.5, m, 0.22)); chords[0].forEach((m) => pluck(13.5, m + 12, 0.12));

let peak = 0; for (const v of buf) peak = Math.max(peak, Math.abs(v));
const n = buf.length, b = Buffer.alloc(44 + n * 2);
b.write('RIFF', 0); b.writeUInt32LE(36 + n * 2, 4); b.write('WAVEfmt ', 8);
b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22);
b.writeUInt32LE(SR, 24); b.writeUInt32LE(SR * 2, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34);
b.write('data', 36); b.writeUInt32LE(n * 2, 40);
for (let i = 0; i < n; i++) b.writeInt16LE(Math.round(buf[i] / peak * 0.9 * 32767), 44 + i * 2);
mkdirSync('out', { recursive: true }); writeFileSync('out/score.wav', b);
console.log('out/score.wav');
