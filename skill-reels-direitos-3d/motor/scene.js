import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { LINES, SHOTS, DUR } from './timing.js';
window.DUR = DUR;
await document.fonts.load('700 40px F'); await document.fonts.load('800 40px N');
const W = 1080, H = 1920, PI = Math.PI;
const R = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true, preserveDrawingBuffer: true });
R.setSize(W, H, false); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
R.outputColorSpace = THREE.SRGBColorSpace; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.08;
const scene = new THREE.Scene(); scene.background = new THREE.Color('#9fc4e6');
const cam = new THREE.PerspectiveCamera(42, W / H, .05, 120);

// ---------- utilidades ----------
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const win = (t, a, b) => clamp((t - a) / (b - a));
const eio = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
const eout = x => 1 - Math.pow(1 - x, 3);
const back = x => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, p) => a + (b - a) * p;
const L3 = (a, b, p) => [lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)];
const wt = (l, i) => LINES[l].words[Math.min(i, LINES[l].words.length - 1)][2];
function rng(s) { return () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const MC = {};
const mat = (c, o = {}) => { const k = c + JSON.stringify(o); return MC[k] || (MC[k] = new THREE.MeshStandardMaterial({ color: c, roughness: .72, ...o })); };
function add(geo, m, p, par, sh = true) { const me = new THREE.Mesh(geo, typeof m === 'string' ? mat(m) : m); me.castShadow = me.receiveShadow = sh; if (p) me.position.set(...p); (par || scene).add(me); return me; }
const B = (w, h, d, c, p, par, sh) => add(new THREE.BoxGeometry(w, h, d), c, p, par, sh);
const RB = (w, h, d, r, c, p, par) => add(new RoundedBoxGeometry(w, h, d, 3, r), c, p, par);
const CY = (rt, rb, h, c, p, par, seg = 18) => add(new THREE.CylinderGeometry(rt, rb, h, seg), c, p, par);
const SP = (r, c, p, par, seg = 22) => add(new THREE.SphereGeometry(r, seg, Math.round(seg * .7)), c, p, par);
const G = (p, par) => { const g = new THREE.Group(); if (p) g.position.set(...p); (par || scene).add(g); return g; };
function ctex(w, h, fn) { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); fn(g, w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData.g = g; t.userData.c = c; return t; }
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function txt(g, lines, w, h, fg = '#fff', pad = .1) {
  const tot = lines.reduce((s, l) => s + (l[1] || 1), 0), lh = h * (1 - 2 * pad) / tot; let y = h * pad;
  g.textAlign = 'center'; g.textBaseline = 'middle';
  for (const [s, k = 1, col, font = 'F'] of lines) {
    let fs = lh * k * .82; g.font = `700 ${fs}px ${font}`; const m = g.measureText(s).width, mw = w * (1 - 2 * pad);
    if (m > mw) { fs *= mw / m; g.font = `700 ${fs}px ${font}`; }
    g.fillStyle = col || fg; g.fillText(s, w / 2, y + lh * k / 2 + fs * .04); y += lh * k;
  }
}
function sign(w, h, lines, { bg = '#1351b4', fg = '#fff', ppu = 320, basic = false, r = 0, border = null, pad = .1 } = {}) {
  const t = ctex(Math.round(w * ppu), Math.round(h * ppu), (g, Wd, Ht) => {
    g.clearRect(0, 0, Wd, Ht); if (bg) { g.fillStyle = bg; rr(g, 0, 0, Wd, Ht, r * ppu); g.fill(); }
    if (border) { g.lineWidth = border[1] * ppu; g.strokeStyle = border[0]; rr(g, g.lineWidth / 2, g.lineWidth / 2, Wd - g.lineWidth, Ht - g.lineWidth, r * ppu); g.stroke(); }
    txt(g, lines, Wd, Ht, fg, pad);
  });
  const M = basic ? new THREE.MeshBasicMaterial({ map: t, transparent: true, toneMapped: false }) : new THREE.MeshStandardMaterial({ map: t, roughness: .6, transparent: !!r || !bg });
  const me = new THREE.Mesh(new THREE.PlaneGeometry(w, h), M); me.receiveShadow = true; return me;
}
const put = (me, p, par, ry = 0) => { me.position.set(...p); me.rotation.y = ry; (par || scene).add(me); return me; };

// ---------- luz ----------
scene.add(new THREE.HemisphereLight('#eaf4ff', '#8a7a68', 1.15));
const sun = new THREE.DirectionalLight('#fff3df', 2.1); sun.castShadow = true; sun.shadow.mapSize.set(1536, 1536);
Object.assign(sun.shadow.camera, { left: -7, right: 7, top: 7, bottom: -7, near: .5, far: 40 }); sun.shadow.bias = -.0006; sun.shadow.normalBias = .02;
scene.add(sun, sun.target);
const fill = new THREE.PointLight('#ffe2b8', 6, 14, 1.6); scene.add(fill);

// ---------- personagens ----------
function person(o) {
  const { skin = '#c98b62', shirt = '#e05a6b', pants = '#2e4a7a', hair = '#2b1a12', shoe = '#262626', s = 1, style = 'short', bone = false, p = [0, 0, 0] } = o;
  const P = { root: G(p) }; P.root.scale.setScalar(s); P.hipY = .92; P.seat = .5;
  const th = bone ? .45 : 1, BN = '#efe8d8';
  P.hips = G([0, .92, 0], P.root);
  if (bone) { CY(.12, .14, .1, BN, [0, 0, 0], P.hips); } else RB(.36, .2, .22, .06, pants, [0, 0, 0], P.hips);
  for (const sd of [1, -1]) {
    const L = sd > 0 ? 'L' : 'R';
    const t = G([sd * .095, -.05, 0], P.hips); CY(.075 * th, .06 * th, .42, bone ? BN : pants, [0, -.21, 0], t);
    const k = G([0, -.42, 0], t); CY(.062 * th, .05 * th, .4, bone ? BN : pants, [0, -.2, 0], k);
    RB(.12, .08, .25, .03, bone ? BN : shoe, [0, -.42, .055], k);
    P['th' + L] = t; P['kn' + L] = k;
  }
  P.tor = G([0, .06, 0], P.hips);
  if (bone) {
    CY(.025, .025, .52, BN, [0, .27, 0], P.tor);
    for (let i = 0; i < 4; i++) { const rib = add(new THREE.TorusGeometry(.15 - i * .012, .018, 6, 18, PI * 1.6), BN, [0, .5 - i * .075, 0], P.tor); rib.rotation.set(PI / 2, 0, PI * .7); }
  } else {
    RB(.4, .52, .25, .1, shirt, [0, .28, 0], P.tor);
    if (o.lanyard) { CY(.008, .008, .3, '#1351b4', [0, .42, .13], P.tor); put(sign(.12, .16, [['INSS', 1, '#1351b4']], { bg: '#fff', ppu: 600 }), [0, .24, .132], P.tor); }
  }
  CY(.05, .055, .1, bone ? BN : skin, [0, .58, 0], P.tor);
  P.head = G([0, .62, 0], P.tor);
  const hd = SP(.165, bone ? BN : skin, [0, .14, 0], P.head); hd.scale.set(1, 1.08, 1);
  if (bone) {
    for (const sd of [1, -1]) { const e = SP(.045, '#1d1d1d', [sd * .06, .16, .125], P.head); e.scale.z = .5; }
    SP(.022, '#1d1d1d', [0, .1, .155], P.head);
  } else {
    for (const sd of [1, -1]) { SP(.024, '#fff', [sd * .058, .165, .145], P.head, 12); SP(.016, '#1b1b1b', [sd * .058, .165, .162], P.head, 10); B(.06, .014, .012, hair, [sd * .058, .215, .15], P.head, false); }
    const n = SP(.026, skin, [0, .125, .165], P.head, 12); n.scale.set(1, 1, .8);
  }
  P.mouth = B(.075, .02, .02, bone ? '#d8cdb5' : '#7a2a2a', [0, .065, .152], P.head, false);
  if (bone) { for (let i = -2; i <= 2; i++) B(.016, .022, .01, '#fffdf5', [i * .018, .072, .16], P.head, false); }
  if (style !== 'bald') { const cap = SP(.178, hair, [0, .2, -.035], P.head); cap.scale.set(1.04, .88, 1.02); }
  if (style === 'pony') { SP(.085, hair, [0, .2, -.17], P.head); const pt = CY(.05, .025, .26, hair, [0, .07, -.21], P.head); pt.rotation.x = .3; }
  if (style === 'bun') { SP(.08, hair, [0, .3, -.1], P.head); }
  if (style === 'long') { RB(.3, .32, .1, .05, hair, [0, .05, -.11], P.head); }
  if (o.glasses) for (const sd of [1, -1]) { const g = add(new THREE.TorusGeometry(.04, .008, 6, 16), '#222', [sd * .058, .165, .17], P.head, false); }
  if (o.stache) B(.09, .022, .02, hair, [0, .095, .163], P.head, false);
  if (o.phones) { const band = add(new THREE.TorusGeometry(.18, .02, 6, 20, PI), '#ff5a68', [0, .16, 0], P.head); band.rotation.z = 0; for (const sd of [1, -1]) CY(.06, .06, .05, '#ff5a68', [sd * .175, .14, 0], P.head).rotation.z = PI / 2; }
  for (const sd of [1, -1]) {
    const L = sd > 0 ? 'L' : 'R';
    const sh = G([sd * .235, .48, 0], P.tor); CY(.058 * th, .05 * th, .3, bone ? BN : shirt, [0, -.15, 0], sh);
    const el = G([0, -.3, 0], sh); CY(.045 * th, .038 * th, .27, bone ? BN : skin, [0, -.135, 0], el);
    const hand = G([0, -.29, 0], el); SP(.05, bone ? BN : skin, [0, 0, 0], hand, 12);
    P['sh' + L] = sh; P['el' + L] = el; P['hand' + L] = hand;
  }
  return P;
}
function pose(P, o = {}) {
  const { walk = null, sit = 0, aL = [0, 0], aR = [0, 0], eL = .1, eR = .1, head = [0, 0, 0], lean = 0, jaw = 0, y = 0, legsOpen = 0 } = o;
  let tL = 0, tR = 0, kL = 0, kR = 0, bob = 0, sw = 0;
  if (walk !== null) { const s = Math.sin(walk); tL = -s * .55; tR = s * .55; kL = Math.max(0, Math.sin(walk - 1.4)) * .95; kR = Math.max(0, -Math.sin(walk - 1.4)) * .95; bob = Math.abs(Math.cos(walk)) * .035; sw = s * .5; }
  tL -= sit * 1.5; tR -= sit * 1.5; kL += sit * 1.55; kR += sit * 1.55;
  P.thL.rotation.set(tL, 0, legsOpen); P.thR.rotation.set(tR, 0, -legsOpen); P.knL.rotation.set(kL, 0, 0); P.knR.rotation.set(kR, 0, 0);
  P.hips.position.y = P.hipY - sit * (P.hipY - P.seat) + bob + y;
  P.tor.rotation.set(lean, 0, 0);
  P.shL.rotation.set(-aL[0] + sw, 0, .08 + aL[1]); P.shR.rotation.set(-aR[0] - sw, 0, -.08 - aR[1]);
  P.elL.rotation.set(-eL, 0, 0); P.elR.rotation.set(-eR, 0, 0);
  P.head.rotation.set(...head); P.mouth.scale.y = 1 + jaw * 5;
}

// ---------- AGÊNCIA DO INSS (x≈0) ----------
const tile = ctex(512, 512, (g) => { g.fillStyle = '#e6e2da'; g.fillRect(0, 0, 512, 512); g.fillStyle = '#d6d1c6'; g.fillRect(0, 0, 256, 256); g.fillRect(256, 256, 256, 256); g.strokeStyle = '#c3bdb1'; g.lineWidth = 4; g.strokeRect(0, 0, 512, 512); g.strokeRect(0, 0, 256, 256); });
tile.wrapS = tile.wrapT = THREE.RepeatWrapping; tile.repeat.set(16, 16);
const floor = add(new THREE.PlaneGeometry(32, 32), new THREE.MeshStandardMaterial({ map: tile, roughness: .55 }), [0, 0, 0]); floor.rotation.x = -PI / 2;
B(14.4, 3.8, .2, '#eef2f6', [0, 1.9, -4.7]); B(14.4, .9, .21, '#cfe0f5', [0, .45, -4.69]); B(14.4, .14, .22, '#1351b4', [0, 2.35, -4.68]);
B(.2, 3.8, 12, '#f2f4f7', [-7.1, 1.9, 0.6]); B(.2, 3.8, 12, '#f2f4f7', [7.1, 1.9, 0.6]); B(14.4, .2, 12, '#f7f8fa', [0, 3.85, 0.6], null, false);
for (const z of [-2.6, .4, 3.2]) for (const x of [-4, 0, 4]) { B(1.4, .04, .5, '#ffffff', [x, 3.73, z], null, false).material = new THREE.MeshBasicMaterial({ color: '#ffffff' }); }
put(sign(2.8, .95, [['INSS', 1.25], ['Agência da Previdência Social', .55]], { bg: '#1351b4', r: .12 }), [3.6, 2.95, -4.58]);
const senhaTex = ctex(640, 260, () => { }); const senhaPanel = add(new THREE.BoxGeometry(1.7, .7, .1), [mat('#111'), mat('#111'), mat('#111'), mat('#111'), new THREE.MeshBasicMaterial({ map: senhaTex, toneMapped: false }), mat('#111')], [-3.4, 2.85, -4.55]);
let senhaCur = '';
function senha(v) { if (v === senhaCur) return; senhaCur = v; const g = senhaTex.userData.g; g.fillStyle = '#120404'; g.fillRect(0, 0, 640, 260); g.fillStyle = '#ffb000'; g.font = '700 54px F'; g.textAlign = 'center'; g.fillText('SENHA', 320, 78); g.fillStyle = '#ff3b2f'; g.font = '700 150px F'; g.fillText(v, 320, 228); senhaTex.needsUpdate = true; }
senha('001');
// janelas
for (const z of [-2.2, 3.4]) { put(sign(.06, .06, [['']], { bg: '#bfe3ff' }), [0, 0, 0]); const wn = B(.05, 1.4, 1.8, '#cfeaff', [-7.0, 2.0, z], null, false); wn.material = new THREE.MeshBasicMaterial({ color: '#d7eeff' }); B(.08, 1.5, .06, '#dfe5ec', [-6.98, 2.0, z]); }
// porta JUNTA DE RECURSOS (parede esquerda)
B(.12, 2.3, 1.3, '#dfe5ec', [-7.0, 1.15, 0.2]);
const doorPiv = G([-6.94, 0, -.38]); B(.06, 2.15, 1.12, '#8a5a3b', [0, 1.075, .56], doorPiv); SP(.04, '#d9b24a', [.06, 1.05, 1.0], doorPiv, 10);
put(sign(1.9, .5, [['JUNTA DE RECURSOS', 1]], { bg: '#0f7a4a', r: .06 }), [-6.98, 2.6, 0.2], null, PI / 2);
// cartazes
put(sign(.8, 1.05, [['MEU', 1], ['INSS', 1.4], ['ou ligue', .6], ['135', 1.3]], { bg: '#fff', fg: '#1351b4', r: .05, border: ['#1351b4', .03] }), [6.98, 1.7, -1.6], null, -PI / 2);
put(sign(1.0, .6, [['SILÊNCIO', 1], ['por favor', .6]], { bg: '#fff7d6', fg: '#8a5a00', r: .05 }), [-1.0, 2.9, -4.58]);
const clock = G([1.2, 3.0, -4.58]); CY(.28, .28, .05, '#fff', [0, 0, 0], clock).rotation.x = PI / 2; add(new THREE.TorusGeometry(.28, .03, 8, 24), '#333', [0, 0, .01], clock);
B(.025, .2, .02, '#222', [0, .08, .04], clock); B(.02, .14, .02, '#222', [.05, -.03, .04], clock).rotation.z = 1.1;
// balcão com 3 guichês
B(9.4, .85, .14, '#dfe5ec', [0, .425, -2.28]); B(9.6, .06, .8, '#b98a5e', [0, .87, -2.62]); B(9.4, .8, .1, '#c5ccd5', [0, .4, -3.0]);
const glass = new THREE.MeshStandardMaterial({ color: '#cfefff', transparent: true, opacity: .25, roughness: .1 });
for (const x of [-4.6, -1.55, 1.55, 4.6]) { const gp = add(new THREE.BoxGeometry(.04, .85, .8), glass, [x, 1.32, -2.62]); gp.castShadow = false; }
const clerks = [];
for (const [i, x] of [[1, -3.1], [2, 0], [3, 3.1]]) {
  put(sign(1.1, .38, [['GUICHÊ ' + i, 1]], { bg: '#1351b4', r: .06 }), [x, 2.25, -2.62]); CY(.008, .008, 1.4, '#888', [x, 3.1, -2.62]);
  const mon = G([x + (i === 2 ? -.62 : .45), .9, -2.85]); RB(.55, .36, .05, .02, '#1f2a36', [0, .3, 0], mon); B(.06, .14, .05, '#333', [0, .08, 0], mon); B(.25, .02, .16, '#333', [0, .01, 0], mon);
  const ch = G([x, 0, -3.5]); CY(.24, .24, .07, '#2d3a4a', [0, .47, 0], ch); B(.42, .45, .06, '#2d3a4a', [0, .78, -.2], ch); CY(.03, .03, .44, '#555', [0, .22, 0], ch);
  if (i !== 2) { const c = person({ p: [x, 0, -3.32], skin: i === 1 ? '#8d5a3b' : '#e0b08a', shirt: i === 1 ? '#f2f2f2' : '#d6e6ff', hair: i === 1 ? '#111' : '#6b4a2a', style: i === 1 ? 'long' : 'short', lanyard: true }); clerks.push(c); }
}
const clerk = person({ p: [0, 0, -3.32], skin: '#d9a07a', shirt: '#ffffff', pants: '#3a3a44', hair: '#3a2a1e', glasses: true, stache: true, lanyard: true });
// papel + carimbo no balcão
const paper = put(sign(.42, .56, [['REQUERIMENTO BPC', .5, '#1351b4'], ['', .6], ['', .5], ['', .5]], { bg: '#fffef6', ppu: 500 }), [-.15, .905, -2.5]); paper.rotation.x = -PI / 2;
const negMark = put(sign(.36, .14, [['NEGADO', 1, '#e0263a']], { bg: null, border: ['#e0263a', .012], ppu: 600, r: .02, pad: .14 }), [-.15, .907, -2.46]); negMark.rotation.set(-PI / 2, 0, .18);
const stamp = G([.25, .9, -2.75]); RB(.16, .07, .1, .02, '#7a1c1c', [0, .035, 0], stamp); CY(.022, .022, .12, '#222', [0, .12, 0], stamp); SP(.045, '#222', [0, .2, 0], stamp, 12);
// cadeiras da sala de espera
const ROWS = [.8, 2.0, 3.2], SEATX = []; for (let i = 0; i < 11; i++) SEATX.push(-4.6 + i * .64);
for (const z of ROWS) { B(7.2, .05, .06, '#555', [-1.4, .38, z]); for (const x of SEATX) { RB(.5, .06, .46, .03, '#2f7dd1', [x, .45, z]); RB(.5, .48, .06, .03, '#2f7dd1', [x, .72, z + .22]).rotation.x = -.12; CY(.02, .02, .4, '#555', [x, .2, z]); } }
const sitPos = (row, i) => [SEATX[i], 0, ROWS[row] + .02];
const waiting = [];
const LOOKS = [['#e0b08a', '#7fbf6a', '#333', 'short'], ['#8d5a3b', '#f2a03d', '#111', 'long'], ['#f0c8a8', '#9a7fd1', '#b8862e', 'pony'], ['#a86b47', '#d9534f', '#222', 'short'], ['#e8c09a', '#4fb3a9', '#999', 'bun'], ['#6e4630', '#ffd24a', '#111', 'short'], ['#f2d0b5', '#5d7fd6', '#6b3e1f', 'long']];
[[0, 0], [0, 2], [0, 6], [0, 9], [1, 1], [1, 4], [1, 7], [2, 2], [2, 5], [2, 8]].forEach(([r, i], n) => { const lk = LOOKS[n % LOOKS.length]; const pp = person({ p: sitPos(r, i), skin: lk[0], shirt: lk[1], hair: lk[2], style: lk[3], pants: n % 2 ? '#34495e' : '#5b4636' }); pp.root.rotation.y = PI; waiting.push(pp); });
const skel = person({ p: sitPos(0, 4), bone: true, style: 'bald' }); skel.root.rotation.y = PI;
const ticket = put(sign(.13, .09, [['047', 1, '#c0392b']], { bg: '#fff', ppu: 800 }), [0, -.03, .05], skel.handR); ticket.rotation.set(-PI / 2, 0, 0);
const web = put(sign(.7, .7, [['']], { bg: null, ppu: 300 }), [-.18, 1.15, .1], skel.root); web.rotation.y = .3;
{ const g = web.material.map.userData.g; g.strokeStyle = 'rgba(255,255,255,.85)'; g.lineWidth = 2; for (let a = 0; a < 8; a++) { g.beginPath(); g.moveTo(105, 105); g.lineTo(105 + Math.cos(a * PI / 4) * 105, 105 + Math.sin(a * PI / 4) * 105); g.stroke(); } for (let r = 20; r < 105; r += 18) { g.beginPath(); for (let a = 0; a <= 8; a++) { const x = 105 + Math.cos(a * PI / 4) * r, y = 105 + Math.sin(a * PI / 4) * r; a ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); } web.material.map.needsUpdate = true; web.material.side = THREE.DoubleSide; web.material.depthWrite = false; }
// bebedouro e plantas
const cool = G([6.4, 0, -1.2]); RB(.4, 1.0, .4, .05, '#e8edf2', [0, .5, 0], cool); CY(.17, .17, .45, '#8fd3ff', [0, 1.22, 0], cool);
for (const p of [[6.4, 0, 1.0], [-6.4, 0, -3.8], [6.4, 0, 3.6]]) { const pl = G(p); CY(.2, .16, .4, '#c0603a', [0, .2, 0], pl); for (let i = 0; i < 6; i++) { const lf = SP(.22, '#3f9b4f', [Math.cos(i) * .12, .6 + i * .07, Math.sin(i * 2) * .12], pl, 10); lf.scale.set(.6, 1.2, .6); } }
// blocos dos níveis (S2)
const levels = [];
for (let i = 0; i < 3; i++) {
  const lv = G([3.7 + i * .78, 0, -.4]); const h = .3 + i * .3;
  const bx = RB(.7, h, .7, .04, ['#4fd0ff', '#ffd24a', '#ff8ec4'][i], [0, h / 2, 0], lv);
  const lb = put(sign(.5, .3, [['NÍVEL ' + (i + 1), 1, '#0d1b2a']], { bg: '#fff', r: .05, ppu: 500 }), [0, h - .2, .356], lv);
  const ck = put(sign(.36, .36, [['✓', 1, '#fff']], { bg: '#18b35a', r: .18, ppu: 500, pad: 0 }), [0, h + .45, 0], lv);
  levels.push({ g: lv, h, ck });
}
// mãe e filho
const mom = person({ skin: '#c98b62', shirt: '#8e44ad', pants: '#2e4a7a', hair: '#3b2416', style: 'pony' });
const kid = person({ s: .6, skin: '#d7a27c', shirt: '#ffd24a', pants: '#3a7bd5', hair: '#2b1a12', phones: true });
const momPaper = put(sign(.21, .28, [['RECURSO', .5, '#0f7a4a'], ['', 1]], { bg: '#fffef6', ppu: 700 }), [0, -.06, .06], mom.handR); momPaper.rotation.set(-1.2, 0, 0);
const phone = G([0, -.05, .07], mom.handL); RB(.09, .17, .015, .012, '#111', [0, 0, 0], phone);
const scr = put(sign(.08, .15, [['▶', 1.3, '#fff'], ['@paisda', .5], ['rotina', .5]], { bg: '#e1306c', ppu: 900, basic: true }), [0, 0, .009], phone);
const shades = G([0, 0, 0], kid.head); for (const sd of [1, -1]) { B(.11, .045, .02, '#050505', [sd * .06, .165, .175], shades, false); B(.06, .02, .021, '#050505', [sd * .06, .14, .175], shades, false); } B(.26, .025, .02, '#050505', [0, .19, .176], shades, false);
const sweat = []; for (let i = 0; i < 3; i++) { const d = SP(.022, '#9fe0ff', [0, 0, 0], clerk.head, 10); d.scale.y = 1.5; sweat.push(d); }

// ---------- SALA DA FAMÍLIA (x≈30) ----------
const HX = 30;
const wood = ctex(512, 512, g => { g.fillStyle = '#c99566'; g.fillRect(0, 0, 512, 512); for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? '#bf8a5b' : '#cf9d6f'; g.fillRect(0, i * 64, 512, 62); } });
wood.wrapS = wood.wrapT = THREE.RepeatWrapping; wood.repeat.set(3, 3);
const hf = add(new THREE.PlaneGeometry(9, 8), new THREE.MeshStandardMaterial({ map: wood, roughness: .6 }), [HX, .002, .5]); hf.rotation.x = -PI / 2;
B(9, 3.4, .2, '#f6d7b8', [HX, 1.7, -2.6]); B(.2, 3.4, 8, '#f0c9a4', [HX - 4.4, 1.7, .5]); B(.2, 3.4, 8, '#f0c9a4', [HX + 4.4, 1.7, .5]);
const win2 = B(1.6, 1.2, .05, '#bfe6ff', [HX + 2.4, 1.9, -2.48], null, false); win2.material = new THREE.MeshBasicMaterial({ color: '#bfe6ff' }); B(1.7, .08, .1, '#fff', [HX + 2.4, 1.3, -2.45]); B(.06, 1.2, .07, '#fff', [HX + 2.4, 1.9, -2.45]);
for (const [x, y, c] of [[-1.2, 2.2, '#8fc1e3'], [-.4, 2.35, '#f2b5a0'], [.5, 2.15, '#b8d99a']]) { B(.5, .6, .04, '#5a3b25', [HX + x, y, -2.48]); B(.42, .52, .045, c, [HX + x, y, -2.47], null, false); }
put(sign(1.1, .3, [['Deus é fiel', 1, '#5a3b25', 'F']], { bg: null, ppu: 400 }), [HX - .4, 2.85, -2.48]);
const sofa = G([HX, 0, -1.7]); RB(2.8, .45, .95, .08, '#4f6f9a', [0, .25, 0], sofa); RB(2.8, .7, .28, .08, '#4f6f9a', [0, .75, -.36], sofa); RB(.28, .62, .95, .08, '#47658c', [-1.42, .4, 0], sofa); RB(.28, .62, .95, .08, '#47658c', [1.42, .4, 0], sofa);
for (const x of [-.85, 0, .85]) RB(.82, .14, .8, .06, '#5d7fae', [x, .52, .05], sofa);
const rug = CY(1.7, 1.7, .01, '#e7b65c', [HX, .008, .2], null, 40); rug.scale.z = .65;
const table = G([HX, 0, .25]); RB(1.6, .07, .8, .03, '#8a5a3b', [0, .44, 0], table); for (const [x, z] of [[-.7, -.32], [.7, -.32], [-.7, .32], [.7, .32]]) CY(.03, .03, .42, '#6b4430', [x, .21, z], table);
const tv = G([HX - 3.4, 0, .5]); B(.5, .5, 1.6, '#6b4430', [0, .25, 0], tv); B(.06, .8, 1.4, '#111', [0, 1.0, 0], tv);
const lamp = G([HX + 2.0, 0, -1.9]); CY(.03, .03, 1.5, '#333', [0, .75, 0], lamp); CY(.18, .28, .3, '#fff1c9', [0, 1.6, 0], lamp);
const vo = person({ p: [HX - .85, 0, -1.55], skin: '#e0b08a', shirt: '#c06c84', pants: '#6c5b7b', hair: '#d9d9d9', style: 'bun', glasses: true });
const cane = G([HX - 1.25, 0, -1.1]); CY(.018, .018, .85, '#6b4430', [0, .43, 0], cane); add(new THREE.TorusGeometry(.06, .018, 6, 12, PI), '#6b4430', [.06, .86, 0], cane);
const momH = { x: HX + .05, z: -1.55 }, kidH = { x: HX + .85, z: -1.5 };
// moedas
const coinM = mat('#f2c14e', { metalness: .55, roughness: .35 }), voM = mat('#ff9f43', { metalness: .55, roughness: .35 });
const coins = []; for (let i = 0; i < 10; i++) { const c = CY(.13, .13, .045, i >= 5 ? voM : coinM, [0, 0, 0], null, 24); c.userData.vo = i >= 5; coins.push(c); }
const CX = HX + .2, CZ = .3, TOP = .475;
const limitBar = B(.62, .025, .025, '#ff3b30', [CX, TOP + 6.5 * .046, CZ], null, false); limitBar.material = new THREE.MeshBasicMaterial({ color: '#ff3b30', toneMapped: false });
const limTex = put(sign(.62, .2, [['LIMITE: R$ 405,25', .6], ['POR PESSOA', .4]], { bg: '#ff3b30', r: .04, ppu: 600, basic: true }), [CX - .64, TOP + 6.5 * .046, CZ]);
const limGreen = put(sign(.62, .2, [['DENTRO DO LIMITE', .6], ['✓', .4]], { bg: '#18b35a', r: .04, ppu: 600, basic: true }), [CX - .64, TOP + 6.5 * .046, CZ]);
// martelo do STF
const gavel = G([HX - .25, 3, .3]); CY(.03, .03, .7, '#7a4a2a', [.25, 0, 0], gavel).rotation.z = PI / 2; const gh = CY(.1, .1, .34, '#6b3a1f', [-.12, 0, 0], gavel); gh.rotation.x = PI / 2;
put(sign(.2, .12, [['STF', 1, '#ffd24a']], { bg: '#3a1d0c', ppu: 600 }), [-.12, 0, .171], gavel);
const block = CY(.14, .16, .06, '#6b3a1f', [HX - .55, .505, .05]);
// cartão do CadÚnico + cadeado + CRAS
const cardG = G([HX + .35, .48, .32]); const cad = put(sign(.62, .4, [['CADASTRO ÚNICO', .7, '#1351b4'], ['Atualizado em: 2023', .5, '#333', 'N'], ['Validade: 2 anos', .5, '#c0392b', 'N']], { bg: '#ffffff', r: .03, border: ['#1351b4', .015], ppu: 700 }), [0, .23, 0], cardG); cad.rotation.x = -.35;
B(.5, .03, .14, '#555', [0, .02, -.06], cardG);
const lock = G([0, 0, 0], cardG); RB(.2, .17, .07, .02, '#c0392b', [0, 0, 0], lock); const sk = add(new THREE.TorusGeometry(.065, .018, 8, 18, PI), '#9aa3ab', [0, .085, 0], lock);
const cras = G([HX - .45, .475, .3]); const crasParts = [];
crasParts.push(RB(.62, .04, .44, .01, '#9aa3ab', [0, .02, 0], cras));
crasParts.push(RB(.56, .3, .36, .02, '#fdf6e3', [0, .19, 0], cras));
const roof = add(new THREE.ConeGeometry(.44, .2, 4), '#d0563c', [0, .44, 0], cras); roof.rotation.y = PI / 4; roof.scale.set(1, 1, .75); crasParts.push(roof);
const crasSign = put(sign(.36, .11, [['CRAS', 1]], { bg: '#e67e22', r: .02, ppu: 700 }), [0, .27, .182], cras); crasParts.push(crasSign);
crasParts.push(B(.1, .15, .01, '#6b4430', [0, .115, .182], cras));
const crasBase = crasParts.map(m => m.position.y);

// ---------- confete ----------
const CONF = 160, conf = new THREE.InstancedMesh(new THREE.PlaneGeometry(.05, .025), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, toneMapped: false }), CONF);
const cr = rng(7), confD = []; const CC = ['#ffd24a', '#ff5a68', '#3dffa0', '#4fd0ff', '#ff8ec4', '#ffffff'].map(c => new THREE.Color(c));
for (let i = 0; i < CONF; i++) { confD.push([cr() * 2 - 1, cr() * 1.3 + .6, cr() * 2 - 1, cr() * 10, cr() * 10]); conf.setColorAt(i, CC[i % CC.length]); }
conf.frustumCulled = false; scene.add(conf); const dm = new THREE.Object3D();
function confetti(t, t0, o) { const a = t - t0; conf.visible = a > 0 && a < 3.2; if (!conf.visible) return; for (let i = 0; i < CONF; i++) { const d = confD[i]; dm.position.set(o[0] + d[0] * a * 1.3, o[1] + d[1] * a * 2.2 - 2.4 * a * a, o[2] + d[2] * a * 1.1); dm.rotation.set(d[3] + a * 6, d[4] + a * 5, 0); dm.updateMatrix(); conf.setMatrixAt(i, dm.matrix); } conf.instanceMatrix.needsUpdate = true; }

// ---------- overlay ----------
const $ = id => document.getElementById(id); const pills = {}; const v3 = new THREE.Vector3();
function pill(key, text, cls, pos, op, dy = 0) {
  let el = pills[key]; if (!el) { el = pills[key] = document.createElement('div'); el.className = 'pill ' + (cls || ''); el.textContent = text; $('pills').appendChild(el); }
  el.style.opacity = op; if (op <= 0) return;
  (pos.isObject3D ? pos.getWorldPosition(v3) : v3.set(...pos)); v3.project(cam);
  const x = clamp((v3.x + 1) / 2 * W, el.offsetWidth / 2 + 24, W - el.offsetWidth / 2 - 24), y = Math.max(300, Math.min(1250, (1 - v3.y) / 2 * H + dy)); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.style.transform = `translate(-50%,-50%) scale(${.6 + .4 * back(clamp(op))})`;
}
const pop = (t, a, b = 99) => clamp(Math.min((t - a) / .18, (b - t) / .15));
let capKey = '';
function captions(t) {
  let i = LINES.findIndex(L => t >= L.t0 - .05 && t < L.t1); if (i < 0) { $('cap').innerHTML = ''; capKey = ''; return; }
  const ws = LINES[i].words, n = ws.length, per = n > 11 ? Math.ceil(n / Math.ceil(n / 8)) : n;
  let last = 0; ws.forEach((w, j) => { if (t >= w[2] - .02) last = j; });
  const pg = Math.floor(last / per), from = pg * per, to = Math.min(n, from + per);
  let key = i + ':' + pg + ':' + last; if (key === capKey) return; capKey = key;
  $('cap').innerHTML = ws.slice(from, to).map((w, j) => { const on = from + j <= last, cur = from + j === last; return `<span style="opacity:${on ? 1 : 0};color:${w[1] || '#fff'};transform:scale(${cur ? 1.12 : 1})">${w[0]}</span>`; }).join(' ');
}
function setStamp(text, cls, t, a, b) { const el = $('stamp'); const p = clamp((t - a) / .22); const on = t >= a && t < b; el.style.opacity = on ? 1 : 0; if (!on) return; if (el.textContent !== text) el.textContent = text; el.className = cls || ''; el.style.transform = `translate(-50%,-50%) rotate(-6deg) scale(${lerp(1.9, 1, eout(p))})`; }
function setCard(b, i, t, a, z) { const el = $('card'); const op = clamp(Math.min((t - a) / .25, (z - t) / .2)); el.style.opacity = op; if (op > 0) { if ($('cb').textContent !== b) { $('cb').textContent = b; $('ci').textContent = i; } el.style.transform = `translateX(${(1 - eout(clamp((t - a) / .3))) * -120}px)`; } }
function setBubble(q, t, a, z) { const el = $('bubble'); const op = clamp(Math.min((t - a) / .15, (z - t) / .15)); el.style.opacity = op; if (op > 0) { if ($('bq').textContent !== q) $('bq').textContent = q; el.style.transform = `scale(${.7 + .3 * back(clamp((t - a) / .3))})`; } }
function setCounter(s, t, a, z) { const el = $('counter'); const op = clamp(Math.min((t - a) / .15, (z - t) / .15)); el.style.opacity = op; if (op > 0) { if (el.textContent !== s) el.textContent = s; el.style.transform = `translateX(-50%) scale(${.6 + .4 * back(clamp((t - a) / .25))})`; } }

// ---------- câmeras ----------
const S = k => SHOTS[k].t0, E = k => SHOTS[k].t1;
let SH = 0;
function camAt(t, segs) { let s = segs[0]; for (const g of segs) if (t >= g[0]) s = g; const nx = segs[segs.indexOf(s) + 1]; const p = eio(win(t, s[0], nx ? nx[0] : s[6] || s[0] + 3)); return { pos: L3(s[1], s[2], p), look: L3(s[3], s[4], p), fov: s[5] || 42 }; }
// [início, posA, posB, olharA, olharB, fov, fim]
const CAMS = [
  [[0, [1.35, 1.32, -.75], [.95, 1.22, -1.25], [-.05, 1.05, -2.9], [-.05, 1.05, -2.95], 44, E(0)]],
  [[S(1), [-3.0, 1.3, -1.25], [-2.35, 1.22, -1.0], [-2.1, 1.0, .8], [-2.05, 1.0, .8], 42, E(1)]],
  [[S(2), [5.0, 1.6, 3.9], [4.7, 1.45, 3.3], [4.3, .8, -.4], [4.3, .85, -.4], 42], [wt(2, 9) - .1, [3.3, .8, 2.0], [3.5, .75, 1.8], [4.4, .9, -.4], [4.4, .95, -.4], 44, E(2)]],
  [[S(3), [HX + .1, 1.45, 3.4], [HX, 1.35, 2.95], [HX, .75, -1.0], [HX, .75, -1.0], 44, E(3)]],
  [[S(4), [HX - .5, 1.05, 1.75], [HX - .3, 1.0, 1.5], [HX - .45, .8, -.6], [HX - .3, .78, -.4], 44], [wt(4, 18) - .15, [HX + 1.2, 1.2, 2.1], [HX + 1.0, 1.15, 1.85], [HX + .05, .72, .0], [HX + .1, .72, .0], 44, E(4)]],
  [[S(5), [HX + 1.1, 1.1, 1.9], [HX + .95, 1.05, 1.65], [HX - .2, .7, .1], [HX - .25, .68, .1], 44, E(5)]],
  [[S(6), [1.15, 1.5, -.45], [.9, 1.45, -.8], [-.1, 1.1, -3.2], [-.1, 1.08, -3.2], 42, E(6)]],
  [[S(7), null, null, null, null, 44, E(7)]],
  [[S(8), [HX + .55, 1.0, 2.0], [HX + .45, .95, 1.7], [HX + .3, .72, .2], [HX + .3, .72, .2], 42], [wt(9, 0) - .12, [HX + 1.3, 1.05, 1.6], [HX + 1.15, 1.0, 1.45], [HX + .2, .7, .2], [HX + .2, .68, .2], 42], [wt(9, 5) - .12, [HX - .1, 1.1, 2.0], [HX - .2, 1.0, 1.7], [HX - .2, .68, .2], [HX - .25, .66, .2], 42, E(8)]],
  [[S(9), [1.25, 1.28, -1.05], [1.0, 1.2, -1.35], [-.05, 1.05, -3.0], [-.05, .98, -3.0], 44], [wt(10, 4) - .1, [.05, .95, -2.12], [.1, .93, -2.08], [.32, .88, -1.15], [.32, .88, -1.15], 40], [wt(10, 6) - .08, [1.3, 1.3, -.7], [1.2, 1.25, -.85], [-.05, .95, -3.0], [-.05, .9, -3.0], 44, E(9)]],
  [[S(10), [-3.4, 2.45, -2.6], [-3.4, 2.55, -2.95], [-3.4, 2.85, -4.6], [-3.4, 2.85, -4.6], 40], [S(10) + 1.0, [-1.45, 1.45, -1.75], [-1.6, 1.4, -2.0], [-2.0, 1.15, .5], [-2.0, 1.2, .5], 44, E(10)]],
];

// ---------- cena por instante ----------
function stand(P, x, z, ry) { P.root.position.set(x, 0, z); P.root.rotation.y = ry; }
function update(t) {
  let k = SHOTS.findIndex(s => t >= s.t0 && t < s.t1); if (k < 0) k = SHOTS.length - 1; const lt = t - S(k);
  const home = [3, 4, 5, 8].includes(k);
  // padrão
  senha('001'); conf.visible = false; SH = 0; shades.visible = false; sweat.forEach(d => d.visible = false); lock.visible = false; phone.visible = false; momPaper.visible = false;
  levels.forEach(l => { l.g.visible = k === 2; }); web.visible = true; ticket.visible = true; negMark.visible = t > 1.55;
  doorPiv.rotation.y = 0;
  stand(skel, ...sitPos(0, 4).filter((_, i) => i !== 1), PI); pose(skel, { sit: 1, aL: [.15, .05], aR: [.55, .05], eR: .9, head: [.45, 0, .25], jaw: .3 });
  waiting.forEach((p, i) => pose(p, { sit: 1, aL: [.3, 0], aR: [.3, 0], eL: .9, eR: .9, head: [.05 * Math.sin(t * .7 + i), .25 * Math.sin(t * .4 + i * 2), 0] }));
  clerks.forEach((c, i) => pose(c, { sit: 1, aL: [.6, 0], aR: [.6, 0], eL: 1.2, eR: 1.2, head: [.1, .15 * Math.sin(t + i), 0] }));
  stand(clerk, 0, -3.32, 0); let cp = { sit: 1, aL: [.55, 0], aR: [.55, 0], eL: 1.1, eR: 1.1, head: [.08, 0, 0] };
  stamp.position.set(.25, .9, -2.75); stamp.rotation.set(0, 0, 0);
  // família na agência
  stand(mom, -.38, -1.65, PI); stand(kid, .32, -1.6, PI); let mp = { aL: [.1, .05], aR: [.1, .05], head: [0, 0, 0] }, kp = { aL: [.05, .05], aR: [.05, .05], head: [-.15, 0, 0] };
  if (home) { stand(mom, momH.x, momH.z, 0); stand(kid, kidH.x, kidH.z, 0); mp = { sit: 1, aL: [.35, 0], aR: [.35, 0], eL: .8, eR: .8, head: [.15, 0, 0] }; kp = { sit: 1, aL: [.3, 0], aR: [.3, 0], eL: .7, eR: .7, head: [.1, .2 * Math.sin(t * 2), 0] }; }
  let vp = { sit: 1, aL: [.35, 0], aR: [.35, 0], eL: .9, eR: .9, head: [.1, 0, 0] };
  // moedas: quantas e onde
  let nCoins = 0, voFly = 0, barGreen = false;
  gavel.position.set(HX - .25, 3, .3); gavel.rotation.set(0, 0, 0);
  crasParts.forEach((m, i) => { m.visible = false; m.position.y = crasBase[i]; }); cardG.visible = k === 8; block.visible = k === 5;
  // luz
  const cx = home ? HX : 0; sun.position.set(cx + 4, 9, 6); sun.target.position.set(cx, 0, -1); fill.position.set(cx + 1, 2.6, 1.5);

  let shot = null;
  if (k === 0) {
    const s0 = .75, hit = 1.55; const up = win(lt, s0, s0 + .4), dn = win(lt, hit - .12, hit);
    stamp.position.set(-.15 + (1 - up) * .4, .9 + up * .35 - dn * .35, -2.5 - (1 - up) * .25);
    cp = { sit: 1, aL: [.55, 0], aR: [.55 + up * .9 - dn * .7, .1], eR: 1.1 - up * .5, eL: 1.1, head: [.12, 0, 0], lean: .1 * up };
    if (lt > hit) SH = .025 * Math.exp(-(lt - hit) * 6);
    setBubble('"Autismo leve não dá BPC."', t, .05, E(0) - .05);
    mp.head = [-.1, 0, 0]; mp.aL = [.3, .1]; mp.eL = .5;
  }
  if (k === 1) {
    setCounter('DESCULPA 1/3', t, wt(1, 6) - .1, E(1));
    pill('esp', 'ESPERANDO A PERÍCIA 💀', 'y', [skel.root.position.x, 1.42, .8], pop(t, S(1) + .5, E(1)));
    pill('047', 'SENHA 047', 'r', skel.handR, pop(t, S(1) + 1.3, E(1)), -60);
  }
  if (k === 2) {
    levels.forEach((l, i) => { const p = back(win(lt, .1 + i * .18, .5 + i * .18)); l.g.scale.set(1, Math.max(.001, p), 1); l.ck.visible = t > wt(2, 11) + i * .15; l.ck.scale.setScalar(back(win(t, wt(2, 11) + i * .15, wt(2, 11) + i * .15 + .3))); l.ck.rotation.y = Math.sin(t * 3 + i) * .25; });
    const j = win(lt, .9, 1.4); stand(kid, lerp(3.0, 3.7, j), lerp(.15, -.4, j), 0); kp = { aL: [.4 + j * 1.5, .3], aR: [.4 + j * 1.5, .3], y: Math.sin(j * PI) * .6 / .6 + j * .3 / .6, head: [-.1, 0, 0] };
    if (t > wt(2, 11)) kp = { aL: [2.6, .4], aR: [2.6, .4], eL: .2, eR: .2, y: .5 + Math.abs(Math.sin((t - wt(2, 11)) * 7)) * .12, head: [-.15, 0, 0] };
    stand(mom, 2.75, .25, .5); mp = { aL: [.2, .1], aR: [.9, .3], eR: .6, head: [0, .3, 0] };
    setCard('LEI 12.764/2012', 'Autista é pessoa com deficiência para todos os efeitos legais.', t, wt(2, 4) - .1, E(2));
    setStamp('SEM GRAU MÍNIMO', '', t, wt(2, 12), E(2));
  }
  if (k === 3) {
    nCoins = Math.min(10, Math.floor(win(lt, .15, 1.9) * 10.99));
    setCounter('DESCULPA 2/3', t, S(3) + .05, E(3)); setBubble('"A renda passou do limite."', t, wt(3, 2) - .1, E(3));
    vp.head = [.1, -.3, 0];
  }
  if (k === 4) {
    nCoins = 10; voFly = win(t, wt(4, 18), wt(4, 18) + .9); barGreen = voFly > .8;
    pill('vo', 'APOSENTADORIA DA VÓ (ATÉ 1 SALÁRIO)', 'y', [HX - .2, 1.35, -.2], pop(t, wt(4, 9) - .1, wt(4, 18)));
    pill('irmao', 'BPC DE OUTRO FILHO', 'y', [HX + .5, 1.25, .1], pop(t, wt(4, 2) - .1, wt(4, 8)));
    vp = { sit: 1, aL: [.35 + voFly * 1.2, .2], aR: [.35 + voFly * 1.2, .2], eL: .5, eR: .5, head: [.05, .3, 0] };
    setStamp('NÃO ENTRA NA CONTA', '', t, wt(4, 19), E(4));
    setCard('Lei 8.742/93, art. 20, §14', 'BPC ou benefício de até 1 salário de outro idoso ou pessoa com deficiência da família não conta na renda.', t, wt(4, 19) + .2, E(4));
    mp.head = [.15, -.2, 0];
  }
  if (k === 5) {
    nCoins = 5; barGreen = true;
    const hit = wt(5, 3) + .05; const f = win(t, hit - .45, hit); gavel.position.set(HX - .43, lerp(2.2, .66, f * f), .05); gavel.rotation.z = lerp(-.6, 0, f);
    if (t > hit) { const b2 = Math.exp(-(t - hit) * 5) * Math.abs(Math.sin((t - hit) * 14)); gavel.position.y = .66 + b2 * .12; SH = .03 * Math.exp(-(t - hit) * 5); }
    pill('stf', 'STF', 'y', gavel, pop(t, hit, E(5)), -110);
    setStamp('NÃO É ABSOLUTO', '', t, wt(5, 7), E(5));
    setCard('STF · Tema 27', 'O limite de 1/4 do salário mínimo por pessoa não é critério absoluto.', t, hit + .25, E(5));
    mp.head = [.1, -.3, 0]; mp.aL = [.4, .3]; mp.eL = 1.0; kp.head = [.1, -.5, 0];
  }
  if (k === 6) {
    const sh = back(win(lt, .45, .9)); cp = { sit: 1, aL: [.8 * sh, .9 * sh], aR: [.8 * sh, .9 * sh], eL: 1.6 * sh + .2, eR: 1.6 * sh + .2, head: [.1, 0, .25 * sh], lean: -.1 * sh };
    setCounter('DESCULPA 3/3', t, S(6) + .05, E(6)); setBubble('"Negado, não tem o que fazer."', t, wt(6, 2) - .1, E(6));
    mp.head = [0, .15, 0];
  }
  if (k === 7) {
    const d = clamp(lt / 4.6), x0 = -.38, z0 = -1.65, x1 = -6.3, z1 = .2; const p = eio(d) * .15 + d * .85;
    const mx = lerp(x0, x1, p), mz = lerp(z0, z1, p); const ry = Math.atan2(x1 - x0, z1 - z0);
    stand(mom, mx, mz, ry); mp = { walk: lt * 7.5, aL: [.05, .05], aR: [1.0, .05], eR: .8, head: [0, 0, 0] }; momPaper.visible = true;
    stand(kid, mx + .25, mz + .62, ry); kp = { walk: lt * 9 + 1, aL: [.1, .05], aR: [.1, .05], head: [0, 0, 0] };
    if (lt > 4.6) { mp = { aL: [.05, .05], aR: [1.3, .05], eR: .3, head: [0, 0, 0] }; kp = { aL: [.1, 0], aR: [.1, 0] }; }
    doorPiv.rotation.y = -1.3 * eout(win(lt, 4.5, 5.2));
    const look = [mx - .5, 1.1, mz + .1]; shot = { pos: [Math.max(-6.55, mx - 2.6), 1.45, mz + 2.2], look, fov: 42 };
    setStamp('TEM SIM!', '', t, S(7) + .05, wt(7, 3));
    pill('30', '30 DIAS', 'g', [mx, 2.05, mz], pop(t, wt(7, 3), wt(7, 8)));
    pill('jr', 'JUNTA DE RECURSOS', 'g', [-6.9, 2.15, .2], pop(t, wt(7, 8), E(7)));
    pill('m', 'MEU INSS', 'y', [mx - .2, 1.85, mz], pop(t, wt(7, 12), E(7)));
    pill('135', 'LIGUE 135', 'y', [mx - .2, 1.55, mz], pop(t, wt(7, 15), E(7)));
    setCard('Recurso em 30 dias', 'Junta de Recursos, pelo Meu INSS ou pelo 135 (cartilha do INSS).', t, wt(7, 6), E(7));
  }
  if (k === 8) {
    nCoins = 0; cardG.visible = true;
    pill('2a', 'VALE 2 ANOS', 'y', [HX + .35, 1.05, .3], pop(t, wt(8, 9), wt(9, 0)));
    const lk = win(t, wt(9, 2) - .35, wt(9, 2)); lock.visible = t > wt(9, 2) - .35 && t < wt(9, 5) + .5; lock.position.set(0, lerp(1.2, .24, lk * lk), .06); lock.rotation.x = -.35;
    if (t > wt(9, 2)) SH = .015 * Math.exp(-(t - wt(9, 2)) * 6);
    setStamp('VENCIDO = BLOQUEIO', 'red', t, wt(9, 2), wt(9, 5));
    crasParts.forEach((m, i) => { const a = wt(9, 5) + i * .14; m.visible = t > a; m.position.y = crasBase[i] + (1 - back(win(t, a, a + .3))) * .5; });
    if (t > wt(9, 5)) { lock.position.y = .24 + (t - wt(9, 5)) * 3; }
    setStamp('ATUALIZA NO CRAS', '', t, wt(9, 7), E(8));
    setCard('CadÚnico em dia', 'O INSS pede o cadastro atualizado a cada 2 anos. Atualize no CRAS.', t, wt(8, 6), E(8));
    mp.head = [.2, .1, 0];
  }
  if (k === 9) {
    stand(kid, .32, -1.15, PI); phone.visible = true; mp = { aL: [1.55, -.1], eL: .25, aR: [.1, .05], head: [-.05, 0, 0] };
    const read = win(lt, .2, .6), slide = eio(win(t, wt(10, 6) - .05, wt(10, 6) + .4));
    cp = { sit: 1, aL: [.5, 0], aR: [.5, 0], eL: 1.1, eR: 1.1, head: [.1 + read * .15, 0, 0], lean: .15 * read - slide * .5, jaw: read > .5 ? .5 : 0, y: -slide * .75 };
    sweat.forEach((d, i) => { const a = ((lt * 1.4 + i * .33) % 1); d.visible = lt > .5 && slide < .6; d.position.set((i - 1) * .1, .28 - a * .25, .14); });
    shades.visible = t > wt(10, 5) - .25; shades.position.y = (1 - eout(win(t, wt(10, 5) - .25, wt(10, 5) + .2))) * .5;
    kp.head = [-.18, -.25, 0];
    if (t > wt(10, 6) + .12) confetti(t, wt(10, 6) + .12, [0, 1.6, -2.3]);
    $('flash').style.opacity = clamp(1 - Math.abs(t - (wt(10, 4) - .1)) / .08) * .7;
  }
  if (k === 10) {
    senha(lt > .45 ? '047' : '046');
    const up = back(win(lt, 1.2, 1.6)); web.visible = lt < 1.25; ticket.visible = true;
    pose(skel, { sit: 1 - up, aL: [2.8 * up, .5 * up], aR: [2.8 * up, .5 * up], eL: .2, eR: .2, head: [.45 * (1 - up), 0, .25 * (1 - up)], jaw: .6 + .4 * Math.abs(Math.sin(lt * 9)), y: up * Math.abs(Math.sin((lt - 1.6) * 6)) * .18 * (lt > 1.6) });
    skel.root.position.z = sitPos(0, 4)[2] - up * .35;
    if (lt > 1.6) confetti(t, S(10) + 1.6, [-1.95, 1.6, .5]);
    pill('ch', 'CHAMANDO: SENHA 047', 'r', [-3.4, 2.4, -4.5], pop(t, S(10) + .5, S(10) + 1.0));
    const cm = $('cmt'); const op = clamp((lt - 1.7) / .2); cm.style.opacity = op; cm.style.transform = `scale(${.7 + .3 * back(clamp((lt - 1.7) / .3))})`;
    const msg = 'Me disseram que autismo leve não dá BPC 🙄'; $('ct').textContent = msg.slice(0, Math.floor(clamp((lt - 2.1) / 2.2) * msg.length)); $('cur').style.opacity = Math.floor(lt * 3) % 2 ? 1 : .2;
    $('at').style.opacity = clamp((lt - 4.2) / .3);
    $('flash').style.opacity = clamp(1 - Math.abs(lt - .98) / .08) * .5;
  } else { $('cmt').style.opacity = 0; $('at').style.opacity = 0; if (k !== 9) $('flash').style.opacity = 0; }
  // limpa overlays fora do plano
  if (![2, 4, 5, 7, 8].includes(k)) setCard('', '', t, 99, 100);
  if (![0, 3, 6].includes(k)) setBubble('', t, 99, 100);
  if (![1, 3, 6].includes(k)) setCounter('', t, 99, 100);
  if (![2, 4, 5, 7, 8].includes(k)) setStamp('', '', t, 99, 100);
  for (const key in pills) if (!({ 1: ['esp', '047'], 4: ['vo', 'irmao'], 5: ['stf'], 7: ['30', 'jr', 'm', '135'], 8: ['2a'], 10: ['ch'] }[k] || []).includes(key)) pills[key].style.opacity = 0;
  // moedas
  const voIdx = [5, 6, 7, 8, 9];
  coins.forEach((c, i) => {
    c.visible = home && i < (k === 5 ? 5 : k === 4 ? 10 : nCoins) && k !== 8;
    let y = TOP + i * .046 + .023, x = CX, z = CZ;
    if (k === 3) { const a = .15 + i * .175; y += (1 - eout(win(lt, a, a + .25))) * .6; }
    if (c.userData.vo && voFly > 0) { const q = clamp(voFly * 1.3 - (i - 5) * .06); x = lerp(CX, HX - .85, q); z = lerp(CZ, -1.3, q); y = lerp(y, .75, q) + Math.sin(q * PI) * .7; c.visible = q < .98; }
    c.position.set(x, y, z);
  });
  limitBar.visible = limTex.visible = home && (k === 3 || k === 4 || k === 5); limGreen.visible = limitBar.visible && barGreen; limTex.visible = limitBar.visible && !barGreen;
  limitBar.material.color.set(barGreen ? '#18b35a' : '#ff3b30');
  // poses
  pose(clerk, cp); pose(mom, mp); pose(kid, kp); pose(vo, vp);
  // câmera
  const c = shot || camAt(t, CAMS[k]);
  const sx = SH * Math.sin(t * 90), sy = SH * Math.cos(t * 77);
  cam.position.set(c.pos[0] + sx, c.pos[1] + sy, c.pos[2]); cam.lookAt(c.look[0] + sx, c.look[1] + sy, c.look[2]); cam.fov = c.fov * 1.3; cam.updateProjectionMatrix();
  captions(t);
}
// estado inicial das peças da família em casa
stand(vo, HX - .85, -1.55, 0);
window.renderAt = t => { update(t); R.render(scene, cam); };
window.ready = true;
