// uso: node render.js pagina.html cues.json END fps saida.mp4 [t1,t2,...]  (com tempos: só tira fotos)
const { chromium } = require('playwright');
const fs = require('fs'); const { spawn } = require('child_process'); const path = require('path');
(async () => {
  const [page, cuesPath, END, FPS, out, shots] = process.argv.slice(2);
  const cues = JSON.parse(fs.readFileSync(cuesPath, 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(([c, e]) => { window.CUES = c; window.END = e; }, [cues, parseFloat(END)]);
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.resolve(page));
  await p.evaluate(() => window.ready);
  if (errs.length) { console.error(errs); process.exit(1); }
  if (shots) {
    for (const t of shots.split(',')) { await p.evaluate(t => { window.seek(t); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, parseFloat(t)); await p.screenshot({ path: `${out}-${t}.jpg`, type: 'jpeg', quality: 80 }); }
  } else {
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', FPS, '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out]);
    const n = Math.round(parseFloat(END) * parseFloat(FPS));
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => { window.seek(t); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, i / parseFloat(FPS));
      const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  if (errs.length) console.error(errs);
  await b.close(); console.log('ok');
})();
