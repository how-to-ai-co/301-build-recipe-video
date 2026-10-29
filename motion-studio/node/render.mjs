// node render.mjs                     → out/final.mp4 from index.html, 60fps, 15s, motion blur
// node render.mjs --sub 1 --fps 30    → fast draft, no motion blur
// node render.mjs --file examples/showreel.html --dur 15
// If out/score.wav exists (from `node audio.mjs`), it is mixed in.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { ffmpegPath } from './ffmpeg.mjs';

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const FPS = Number(arg('fps', 60)), DUR = Number(arg('dur', 15)), SUB = Math.max(1, Number(arg('sub', 4)));
const FILE = arg('file', 'index.html'), W = Number(arg('w', 1080)), H = Number(arg('h', 1920));
const FFMPEG = await ffmpegPath();
mkdirSync('out', { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(resolve(FILE)).href);
await page.evaluate(() => document.fonts.ready);       // canvas text needs loaded fonts

// tmix averages SUB consecutive subframes (motion blur); select keeps the last of each group
const vf = SUB > 1 ? `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB` : 'null';
const audio = existsSync('out/score.wav');
const ff = spawn(FFMPEG, ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS * SUB), '-i', '-',
  ...(audio ? ['-i', 'out/score.wav'] : []),
  '-vf', vf, '-r', String(FPS), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p',
  ...(audio ? ['-c:a', 'aac', '-b:a', '192k', '-shortest'] : []),
  '-movflags', '+faststart', 'out/final.mp4'],
  { stdio: ['pipe', 'inherit', 'inherit'] });

const total = Math.round(DUR * FPS * SUB);
for (let i = 0; i < total; i++) {
  await page.evaluate((t) => window.seek(t), i / (FPS * SUB));
  const png = await page.locator('#c').screenshot({ type: 'png' });
  if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
  if (i % (FPS * SUB) === 0) console.log(`rendered ${i / (FPS * SUB)}s / ${DUR}s`);
}
ff.stdin.end();
const code = await new Promise((r) => ff.on('close', r));
await browser.close();
if (code !== 0) { console.error('ffmpeg failed'); process.exit(1); }
console.log(`out/final.mp4${audio ? ' (with out/score.wav)' : ''}`);
