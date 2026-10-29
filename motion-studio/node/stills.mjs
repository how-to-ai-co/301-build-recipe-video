// node stills.mjs                     → out/sheet.png, one frame every 0.5s (one per beat at 120 BPM)
// node stills.mjs --step 1 --dur 10 --file examples/showreel.html
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { mkdirSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { ffmpegPath } from './ffmpeg.mjs';

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const STEP = Number(arg('step', 0.5)), DUR = Number(arg('dur', 15)), FILE = arg('file', 'index.html');
const W = Number(arg('w', 1080)), H = Number(arg('h', 1920));
const FFMPEG = await ffmpegPath();
rmSync('out/stills', { recursive: true, force: true });
mkdirSync('out/stills', { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H } });
await page.goto(pathToFileURL(resolve(FILE)).href);
await page.evaluate(() => document.fonts.ready);
let n = 0;
for (let t = STEP / 2; t < DUR; t += STEP) {
  await page.evaluate((t) => window.seek(t), t);
  await page.locator('#c').screenshot({ path: `out/stills/${String(n++).padStart(3, '0')}.png` });
}
await browser.close();
const cols = Math.min(10, n), rows = Math.ceil(n / cols);
spawnSync(FFMPEG, ['-v', 'error', '-y', '-i', 'out/stills/%03d.png', '-vf', `scale=216:-1,tile=${cols}x${rows}:padding=6:color=white`,
  '-frames:v', '1', 'out/sheet.png'], { stdio: 'inherit' });
console.log(`${n} stills → out/sheet.png (frame k is at ${STEP / 2}s + k × ${STEP}s)`);
