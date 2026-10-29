// Posiciona balões e desenha os rabinhos depois que as fontes carregam.
// .pn[data-ox][data-oy]  -> object-position do recorte (0..1)
// .bal[data-tx][data-ty] -> ponta do rabinho em px da imagem limpa
// .bal[data-x | data-xr] -> borda esquerda | direita, fração da largura do quadro
// .bal[data-y]           -> topo, fração da altura; ou data-sob="1" = logo abaixo da narração (+ data-dy em mm)
const MM = 96 / 25.4;

function mapear(img, ix, iy, ox, oy) {
  const bw = img.clientWidth, bh = img.clientHeight;
  const nw = img.naturalWidth, nh = img.naturalHeight;
  const s = Math.max(bw / nw, bh / nh);
  const offx = (bw - nw * s) * ox, offy = (bh - nh * s) * oy;
  return [offx + ix * s, offy + iy * s];
}

function rabo(b, alvo, borda, forcado) {
  // b: {l,t,r,bt} do balão no quadro; alvo: [x,y]
  const [tx, ty] = alvo;
  const raio = 3.4 * MM, base = 3.4 * MM, dentro = borda * 2.2;
  const cx = (b.l + b.r) / 2, cy = (b.t + b.bt) / 2;
  let p1, p2;
  // quanto a ponta está fora da caixa em cada eixo: o rabinho sai do lado em que ela está mais longe
  const foraX = tx < b.l ? b.l - tx : tx > b.r ? tx - b.r : 0;
  const foraY = ty < b.t ? b.t - ty : ty > b.bt ? ty - b.bt : 0;
  const vert = ty > b.bt ? 'baixo' : 'cima', horiz = tx < b.l ? 'esq' : 'dir';
  const lado = forcado || (foraY === 0 ? horiz : foraX > foraY * 1.6 ? horiz : vert);
  if (lado === 'baixo' || lado === 'cima') {
    const min = b.l + raio + base / 2, max = b.r - raio - base / 2;
    let x = cx + (tx - cx) * 0.55;
    x = Math.min(Math.max(x, min), Math.max(min, max));
    const y = lado === 'baixo' ? b.bt - dentro : b.t + dentro;
    p1 = [x - base / 2, y]; p2 = [x + base / 2, y];
  } else {
    const min = b.t + Math.min(raio, (b.bt - b.t) / 2 - base / 2), max = b.bt - Math.min(raio, (b.bt - b.t) / 2 - base / 2);
    let y = cy + (ty - cy) * 0.55;
    y = Math.min(Math.max(y, min), Math.max(min, max));
    const x = lado === 'esq' ? b.l + dentro : b.r - dentro;
    p1 = [x, y - base / 2]; p2 = [x, y + base / 2];
  }
  // curvinha leve: ponto de controle desviado pra dentro
  const mx = (p1[0] + p2[0]) / 2, my = (p1[1] + p2[1]) / 2;
  const c1 = [(p1[0] + tx) / 2 + (mx - p1[0]) * 0.35, (p1[1] + ty) / 2 + (my - p1[1]) * 0.35];
  const c2 = [(p2[0] + tx) / 2 + (mx - p2[0]) * 0.35, (p2[1] + ty) / 2 + (my - p2[1]) * 0.35];
  const f = v => v.toFixed(2);
  return `M${f(p1[0])},${f(p1[1])} Q${f(c1[0])},${f(c1[1])} ${f(tx)},${f(ty)} Q${f(c2[0])},${f(c2[1])} ${f(p2[0])},${f(p2[1])} Z`;
}

function montar() {
  const NS = 'http://www.w3.org/2000/svg';
  document.querySelectorAll('.pn').forEach(pn => {
    const img = pn.querySelector('.art img');
    const ox = parseFloat(pn.dataset.ox ?? 0.5), oy = parseFloat(pn.dataset.oy ?? 0.5);
    img.style.objectPosition = `${ox * 100}% ${oy * 100}%`;
    const W = pn.clientWidth, H = pn.clientHeight;
    const narra = pn.querySelector('.narra');
    const nb = narra ? narra.offsetTop + narra.offsetHeight : 0;
    const borda = parseFloat(getComputedStyle(pn.querySelector('.bal') || pn).borderTopWidth) || 1.7;
    const tr = document.createElementNS(NS, 'svg'); tr.setAttribute('class', 'rabo traco');
    const fu = document.createElementNS(NS, 'svg'); fu.setAttribute('class', 'rabo fundo');
    pn.querySelectorAll('.bal').forEach(bal => {
      const d = bal.dataset;
      if (d.w) bal.style.maxWidth = (parseFloat(d.w) * W) + 'px';
      let top;
      if (d.sob) top = nb + (parseFloat(d.dy || 1.8)) * MM;
      else top = parseFloat(d.y) * H;
      bal.style.top = top + 'px';
      if (d.xr !== undefined) bal.style.left = (parseFloat(d.xr) * W - bal.offsetWidth) + 'px';
      else if (d.xc !== undefined) bal.style.left = (parseFloat(d.xc) * W - bal.offsetWidth / 2) + 'px';
      else bal.style.left = (parseFloat(d.x) * W) + 'px';
      if (d.tx === undefined) return;
      // .art tem borda: a imagem começa dentro dela
      const ab = parseFloat(getComputedStyle(pn.querySelector('.art')).borderTopWidth);
      let [ax, ay] = mapear(img, parseFloat(d.tx), parseFloat(d.ty), ox, oy);
      ax += ab; ay += ab;
      const b = { l: bal.offsetLeft, t: bal.offsetTop, r: bal.offsetLeft + bal.offsetWidth, bt: bal.offsetTop + bal.offsetHeight };
      const path = rabo(b, [ax, ay], borda, d.lado);
      const p1 = document.createElementNS(NS, 'path');
      p1.setAttribute('d', path); p1.setAttribute('fill', '#fff'); p1.setAttribute('stroke', '#1d1d22');
      p1.setAttribute('stroke-width', borda * 2); p1.setAttribute('stroke-linejoin', 'round');
      tr.appendChild(p1);
      const p2 = document.createElementNS(NS, 'path');
      p2.setAttribute('d', path); p2.setAttribute('fill', '#fff');
      fu.appendChild(p2);
    });
    pn.appendChild(tr); pn.appendChild(fu);
  });
  document.body.dataset.pronto = '1';
}

document.fonts.ready.then(() => {
  const imgs = [...document.images].filter(i => !i.complete);
  Promise.all(imgs.map(i => new Promise(r => { i.onload = i.onerror = r; }))).then(montar);
});
