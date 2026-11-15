// uso: node shoot.mjs stills t1,t2,...   |   node shoot.mjs video f0 f1 saida.mp4
import { createRequire } from 'module'; const { chromium } = createRequire(import.meta.url)('playwright');
import { spawn } from 'child_process';
import fs from 'fs';
const [mode, a, b, out] = process.argv.slice(2);
const br = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const pg = await br.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
const errs = []; pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await pg.goto('http://localhost:8765/bpc/index.html');
await pg.waitForFunction(() => window.ready === true || window.__err, null, { timeout: 60000 }).catch(e => errs.push(String(e)));
if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
const shot = async t => { await pg.evaluate(t => window.renderAt(t), t); return pg.screenshot({ type: 'jpeg', quality: 92 }); };
if (mode === 'stills') {
  for (const t of a.split(',').map(Number)) { const buf = await shot(t); fs.writeFileSync(`/home/claude/curto/bpc/st/${t.toFixed(2)}.jpg`, buf); }
} else {
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', out + '.tmp.mp4']);
  for (let f = +a; f < +b; f++) { const buf = await shot(f / 30); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (f % 60 === 0) console.log(out, f); }
  ff.stdin.end(); const code = await new Promise(r => ff.on('close', r));
  if (code === 0) fs.renameSync(out + '.tmp.mp4', out);
}
if (errs.length) console.error(errs.join('\n'));
await br.close();
