// uso: node render.js <pagina.html> <saida.pdf|-> <pasta_png|-> [largura_png]
// Serve a pasta via http.server antes (fontes não carregam por file://).
const { chromium } = require('playwright');
const [, , pagina, pdf, pngDir, largura] = process.argv;
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('console', m => console.log('[pg]', m.text()));
  page.on('requestfailed', r => console.log('[falhou]', r.url()));
  await page.goto('http://127.0.0.1:8765/' + pagina, { waitUntil: 'networkidle' });
  await page.waitForSelector('body[data-pronto="1"]', { timeout: 30000 });

  // checagens: conteúdo vazando, fontes carregadas, texto pequeno demais nos balões
  const rel = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach(pg => {
      const pr = pg.getBoundingClientRect();
      const rod = pg.querySelector('.rodape');
      const limite = rod ? rod.getBoundingClientRect().top : pr.bottom - 45;
      let pior = -1e9, quem = '';
      pg.querySelectorAll('.card, .gibi, .desenho, .tres, .bloco, .fotos, .passos, .seguir, .tinta, .passos-uso, .duas, .mapa, .fileira, .folha, .grade-c, .moldura, .selos, .estrelas, .assina').forEach(el => {
        const b = el.getBoundingClientRect().bottom;
        if (b > pior) { pior = b; quem = el.className; }
      });
      const fontesFora = [...pg.querySelectorAll('*')].filter(el => {
        const f = getComputedStyle(el).fontFamily; return el.childNodes.length && !/Fredoka|Atkinson|Comic/.test(f);
      }).length;
      out.push({ pg: pg.dataset.pg, sobra_mm: +((limite - pior) / (96 / 25.4)).toFixed(1), ultimo: quem, fontesFora });
    });
    const fontes = [...document.fonts].map(f => `${f.family} ${f.weight} ${f.status}`);
    const baloes = [...document.querySelectorAll('.bal, .narra')].map(b => parseFloat(getComputedStyle(b).fontSize) * 0.75).filter(pt => pt < 8.45).length;
    return { paginas: out, fontes, baloes_pequenos: baloes };
  });
  console.log(JSON.stringify(rel, null, 1));

  if (pngDir && pngDir !== '-') {
    fs.mkdirSync(pngDir, { recursive: true });
    const w = parseInt(largura || '1240');
    const escala = w / (210 * 96 / 25.4);
    const ctx2 = await browser.newContext({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: escala });
    const p2 = await ctx2.newPage();
    await p2.goto('http://127.0.0.1:8765/' + pagina, { waitUntil: 'networkidle' });
    await p2.waitForSelector('body[data-pronto="1"]', { timeout: 30000 });
    const pgs = await p2.$$('.page');
    for (const el of pgs) {
      const nome = await el.getAttribute('data-pg');
      await el.screenshot({ path: `${pngDir}/${nome}.png` });
    }
    console.log('png:', pgs.length);
  }
  if (pdf && pdf !== '-') {
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    console.log('pdf ok');
  }
  await browser.close();
})();
