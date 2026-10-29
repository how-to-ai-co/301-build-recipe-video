// Finds an ffmpeg that can write H.264. Uses the one on your computer if it has one,
// otherwise the copy that `npm install` brought along (ffmpeg-static).
import { spawnSync } from 'node:child_process';

let cached;
export async function ffmpegPath() {
  if (cached) return cached;
  const sys = spawnSync('ffmpeg', ['-hide_banner', '-encoders'], { encoding: 'utf8' });
  if (sys.status === 0 && sys.stdout.includes('libx264') && !process.env.MOTION_BUNDLED_FFMPEG) return (cached = 'ffmpeg');
  try {
    const { default: p } = await import('ffmpeg-static');
    if (p) return (cached = p);
  } catch {}
  console.error('No ffmpeg found. Run `npm install` in this folder first.');
  process.exit(1);
}
