"""Reel informativo: '3 motivos, com fonte'. Papel, número grande, texto entrando e polaroides do Bento.

Uso: python3 build_reel_info.py [narracao.mp3]
Sem narração gera o rascunho com tempos estimados; com narração acha as pausas e encaixa.
"""
import json
import math
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
F = S + 'fonts/ttf/'
TITLE, BODYB, BODY, HAND = F + 'Fredoka-Bold.ttf', F + 'Nunito-ExtraBold.ttf', F + 'Nunito-SemiBold.ttf', F + 'Caveat-Bold.ttf'
C1 = S + 'zip-cenas/Bento_Ep1_Cena_0%d.png'
C2 = '/home/claude/midia/cenas/ep2/cena-%02d.jpg'
U = '/root/.claude/uploads/5d8bda1a-7926-5607-9e1a-eeb000255e05/'
MUSIC = U + 'dfda338d-marlowemusic-bedtime-613384.mp3'
OUT = S + 'reel/'
RW, RH, FPS = 1080, 1920, 30

INK = (74, 44, 26)
ACCENT = (178, 74, 38)
HL = {'pessego': (247, 201, 168), 'amarelo': (252, 226, 160), 'verde': (214, 230, 200), 'azul': (205, 223, 240)}
cena6 = Image.open(C1 % 6).convert('RGB')
PAPER = cena6.getpixel((20, 20))

# tempos estimados (s); trocados pelos da narração quando ela chega
SEG = {'hook': 0.0, 'p1': 3.6, 'p2': 12.0, 'p3': 19.0, 'cta': 27.6, 'fim': 31.5}


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def back(x):
    x = min(max(x, 0.0), 1.0)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------- fundo ----------
def paper_bg(blobs, seed):
    im = Image.new('RGB', (RW, RH), PAPER)
    d = ImageDraw.Draw(im)
    dot = tuple(max(0, c - 14) for c in PAPER)
    for y in range(40, RH, 56):
        for x in range(40, RW, 56):
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=dot)
    im = im.convert('RGBA')
    for (cx, cy, r, col) in blobs:          # cor chapada + máscara borrada (sem borda escura)
        m = Image.new('L', (RW, RH), 0)
        ImageDraw.Draw(m).ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=150)
        lay = Image.new('RGBA', (RW, RH), col + (0,))
        lay.putalpha(m.filter(ImageFilter.GaussianBlur(90)))
        im.alpha_composite(lay)
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB')).astype(np.int16)
    a += rng.integers(-5, 6, size=(RH, RW, 1), dtype=np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')


BG = {
    'hook': paper_bg([(160, 420, 420, HL['pessego']), (950, 1500, 460, HL['amarelo'])], 1),
    'p1': paper_bg([(900, 380, 420, HL['azul']), (120, 1450, 440, HL['pessego'])], 2),
    'p2': paper_bg([(150, 380, 420, HL['amarelo']), (960, 1480, 460, HL['verde'])], 3),
    'p3': paper_bg([(920, 380, 420, HL['azul']), (140, 1500, 460, HL['amarelo'])], 4),
    'cta': paper_bg([(540, 1200, 560, HL['pessego'])], 5),
}


# ---------- peças ----------
def text_sprite(text, font, size, fill, stroke=0, sfill=None, pad=14):
    f = ImageFont.truetype(font, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=f, stroke_width=stroke)
    im = Image.new('RGBA', (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=fill, stroke_width=stroke,
                            stroke_fill=sfill)
    return im


def headline(lines, size, color, seed=0):
    """Devolve (pincel, texto) do mesmo tamanho, linhas centralizadas."""
    f = ImageFont.truetype(TITLE, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    widths = [tmp.textlength(ln, font=f) for ln in lines]
    w = int(max(widths)) + 90
    lh = int(size * 1.14)
    h = lh * len(lines) + 30
    br = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    tx = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    db, dt = ImageDraw.Draw(br), ImageDraw.Draw(tx)
    rnd = random.Random(seed)
    for i, (ln, lw) in enumerate(zip(lines, widths)):
        x = (w - lw) / 2
        y = 6 + i * lh
        for k in range(7):
            jx, jy = rnd.randint(-8, 8), rnd.randint(-5, 5)
            db.rounded_rectangle((x - 26 + jx, y + size * 0.22 + jy + k, x + lw + 26 + jx,
                                  y + size * 1.08 + jy - k), radius=26, fill=color + (125,))
        dt.text((x, y), ln, font=f, fill=INK)
    br = br.filter(ImageFilter.GaussianBlur(3))
    return br, tx


def badge(n, d=112):
    im = Image.new('RGBA', (d + 16, d + 16), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.ellipse((10, 12, d + 10, d + 12), fill=(120, 50, 26, 90))
    dr.ellipse((6, 6, d + 6, d + 6), fill=ACCENT)
    f = ImageFont.truetype(TITLE, int(d * 0.66))
    t = str(n)
    l, tp, r, b = dr.textbbox((0, 0), t, font=f)
    dr.text((6 + (d - (r - l)) / 2 - l, 6 + (d - (b - tp)) / 2 - tp), t, font=f, fill=(255, 250, 242))
    return im


def chip(text, size=32):
    f = ImageFont.truetype(BODYB, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw = int(tmp.textlength(text, font=f))
    im = Image.new('RGBA', (tw + 48, size + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw + 47, size + 29), radius=(size + 30) // 2, fill=(255, 250, 242),
                        outline=(226, 184, 146), width=3)
    d.text((24, 11), text, font=f, fill=ACCENT)
    return im


def check_item(text, size=46):
    f = ImageFont.truetype(BODYB, size)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    tw = int(tmp.textlength(text, font=f))
    c = 54
    im = Image.new('RGBA', (c + 18 + tw + 10, max(c, size + 16) + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cy = im.height // 2
    d.ellipse((0, cy - c // 2, c, cy + c // 2), fill=ACCENT)
    d.line([(14, cy + 1), (24, cy + 11), (41, cy - 10)], fill=(255, 250, 242), width=7, joint='curve')
    d.text((c + 18, cy - size * 0.62), text, font=f, fill=INK)
    return im


def hand(text, size=76):
    return text_sprite(text, HAND, size, ACCENT, stroke=5, sfill=PAPER + (255,))


def body(text, size=44, color=INK):
    return text_sprite(text, BODYB, size, color)


# ---------- polaroide ----------
SRC = {k: Image.open(C1 % k).convert('RGB') for k in (3, 7, 8)}
SRC[12] = Image.open(C2 % 12).convert('RGB')


def polaroid(key, box, pw, ph, caption, zoom, angle):
    src = SRC[key]
    x0, y0, x1, y1 = [v * s for v, s in zip(box, (src.width, src.height, src.width, src.height))]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bw, bh = (x1 - x0) / zoom, (y1 - y0) / zoom
    photo = src.resize((pw, ph), Image.BILINEAR, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
    m, mb = 24, 92
    fw, fh = pw + 2 * m, ph + m + mb
    pad = 40
    im = Image.new('RGBA', (fw + 2 * pad, fh + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((pad + 6, pad + 14, pad + fw + 6, pad + fh + 14), fill=(90, 50, 20, 70))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    d.rectangle((pad, pad, pad + fw, pad + fh), fill=(255, 253, 248))
    im.paste(photo, (pad + m, pad + m))
    f = ImageFont.truetype(HAND, 52)
    tw = d.textlength(caption, font=f)
    d.text((pad + (fw - tw) / 2, pad + m + ph + 14), caption, font=f, fill=INK)
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)


# ---------- Bento recortado (cena 6 tem fundo creme) ----------
def bento_sticker(scale):
    b = cena6.crop((100, 260, 1010, 1400))
    a = np.asarray(b).astype(np.int16)
    dist = np.abs(a - np.array(PAPER, dtype=np.int16)).sum(axis=2)
    al = np.clip((dist - 18) * 9, 0, 255).astype(np.uint8)
    mask = Image.fromarray(al).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    st = b.convert('RGBA')
    st.putalpha(mask)
    return st.resize((round(st.width * scale), round(st.height * scale)), Image.LANCZOS)


STICKER = bento_sticker(0.74)


# ---------- linha do tempo ----------
def build(seg, cues):
    """Elementos: (nome, t0, t1, tipo, dados). Tempos de cada parte vêm de cues (relativos ao início)."""
    E = []
    end = {k: seg[n] for k, n in (('hook', 'p1'), ('p1', 'p2'), ('p2', 'p3'), ('p3', 'cta'), ('cta', 'fim'))}
    end['cta'] = 999

    def add(part, rel, kind, data, y, x=None, grp=None):
        E.append(dict(t0=seg[part] + rel, t1=end[part], kind=kind, data=data, y=y, x=x, part=part, grp=grp))

    # gancho
    add('hook', 0.0, 'wipe', headline(['Rotina não é'], 104, HL['amarelo'], 1), 300)
    add('hook', 0.0, 'wipe', headline(['frescura.'], 156, HL['pessego'], 2), 420)
    add('hook', cues['hook'][0], 'rise', hand('3 motivos, com fonte', 88), 640)
    add('hook', 0.0, 'polaroid', dict(key=7, box=(0.0, 0.33, 1.0, 1.0), pw=620, ph=560,
                                      cap='a manhã sem rotina', ang=-4), 770)

    def point(part, n, fonte, lines, hl, seed):
        add(part, 0.0, 'pop', badge(n), 262, 'badge')
        add(part, 0.06, 'rise', chip(fonte), 296, 'chip')
        add(part, 0.08, 'wipe', headline(lines, 100, hl, seed), 410)

    point('p1', 1, 'Academia Americana de Pediatria', ['Ela sabe o que', 'vem depois.'], HL['azul'], 3)
    add('p1', cues['p1'][0], 'rise', body('Rotina regular, previsível e constante.', 46), 680)
    add('p1', 0.12, 'polaroid', dict(key=3, box=(0.05, 0.12, 1.0, 0.86), pw=560, ph=520,
                                     cap='os 3 passos na parede', ang=3), 790)

    point('p2', 2, 'Academia Americana de Pediatria', ['Menos briga', 'de manhã.'], HL['verde'], 4)
    add('p2', cues['p2'][0], 'rise', check_item('Tudo pronto na noite anterior', 44), 670, grp='g2')
    add('p2', cues['p2'][1], 'rise', check_item('Escolhas simples', 44), 750, grp='g2')
    add('p2', cues['p2'][2], 'rise', hand('"essa camiseta ou aquela?"', 64), 822)
    add('p2', 0.12, 'polaroid', dict(key=8, box=(0.0, 0.3, 1.0, 1.0), pw=520, ph=420,
                                     cap='a manhã com rotina', ang=-3), 920)

    point('p3', 3, 'Mindell e colegas · revista Sleep, 2015', ['Dorme melhor.'], HL['amarelo'], 5)
    add('p3', cues['p3'][0], 'counter', None, 540)
    add('p3', cues['p3'][0] + 0.5, 'rise', body('de 0 a 5 anos, com rotina de dormir toda noite:', 34), 650)
    add('p3', cues['p3'][1], 'rise', check_item('pegam no sono mais rápido', 42), 712, grp='g3')
    add('p3', cues['p3'][2], 'rise', check_item('acordam menos', 42), 784, grp='g3')
    add('p3', cues['p3'][3], 'rise', check_item('dormem mais', 42), 856, grp='g3')
    add('p3', 0.12, 'polaroid', dict(key=12, box=(0.0, 0.25, 1.0, 0.95), pw=500, ph=380,
                                     cap='rotina de dormir, toda noite', ang=3), 950)

    add('cta', 0.1, 'wipe', headline(['Manda pra uma mãe', 'que vive a correria.'], 90, HL['pessego'], 6), 300)
    add('cta', 0.0, 'sticker', STICKER, 640)
    add('cta', cues['cta'][0], 'rise', body('@minharotina.kit', 40, ACCENT), 1500)
    left = {}
    for e in E:
        if e['grp']:
            left[e['grp']] = max(left.get(e['grp'], 0), e['data'].width)
    for e in E:
        if e['grp']:
            e['x'] = (RW - left[e['grp']]) // 2
    return E


COUNTER_F = ImageFont.truetype(TITLE, 96)
COUNTER_F2 = ImageFont.truetype(TITLE, 60)


def counter_sprite(v):
    n = f'{int(v):,}'.replace(',', '.')
    a = text_sprite(n, TITLE, 100, ACCENT)
    b = text_sprite('crianças', TITLE, 62, INK)
    im = Image.new('RGBA', (a.width + b.width - 4, a.height), (0, 0, 0, 0))
    im.alpha_composite(a, (0, 0))
    im.alpha_composite(b, (a.width - 4, a.height - b.height - 10))
    return im


def with_alpha(sp, a):
    if a >= 0.999:
        return sp
    s = sp.copy()
    s.putalpha(sp.getchannel('A').point(lambda v: int(v * a)))
    return s


def place_row(E, frame_elems):
    """Centraliza badge + chip lado a lado."""
    pass


def frame(t, E, seg):
    parts = ['hook', 'p1', 'p2', 'p3', 'cta']
    cur = max([p for p in parts if seg[p] <= t], key=lambda p: seg[p])
    im = BG[cur].copy()
    i = parts.index(cur)
    if i > 0 and t - seg[cur] < 0.35:
        im = Image.blend(BG[parts[i - 1]], im, ease((t - seg[cur]) / 0.35))
    # largura da linha badge + chip da parte atual, pra centralizar
    row = {}
    for e in E:
        if e['part'] == cur and e['x'] in ('badge', 'chip'):
            row[e['x']] = e['data'].width
    total = row.get('badge', 0) + 6 + row.get('chip', 0)
    for e in E:
        if not (e['t0'] <= t < e['t1'] + 0.001):
            continue
        local = t - e['t0']
        p = 1.0 if e['t0'] == 0 else ease(local / 0.22)
        q = ease((e['t1'] - t) / 0.18)
        a = p * q
        dy = (1 - p) * 40 - (1 - q) * 30
        k = e['kind']
        if k == 'wipe':
            br, tx = e['data']
            w = ease(local / 0.35) if e['t0'] > 0 else ease((local + 0.15) / 0.45)
            x = (RW - br.width) // 2
            y = int(e['y'] + dy)
            cw = max(1, int(br.width * w))
            im.alpha_composite(with_alpha(br.crop((0, 0, cw, br.height)), q), (x, y))
            im.alpha_composite(with_alpha(tx, a), (x, y))
        elif k == 'pop':
            s = 0.4 + 0.6 * back(local / 0.4) if e['t0'] > 0 else 1.0
            sp = e['data']
            sp2 = sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))), Image.BICUBIC)
            cx = (RW - total) // 2 + sp.width // 2
            im.alpha_composite(with_alpha(sp2, q * min(1, local / 0.12 + 0.01)),
                               (cx - sp2.width // 2, e['y'] + sp.height // 2 - sp2.height // 2))
        elif k == 'counter':
            v = 10085 * ease(local / 1.3)
            sp = counter_sprite(v)
            im.alpha_composite(with_alpha(sp, a), ((RW - sp.width) // 2, int(e['y'] + dy)))
        elif k == 'polaroid':
            d = e['data']
            span = max(1.0, e['t1'] - e['t0'])
            zoom = 1.0 + 0.07 * (local / span)
            ang = d['ang'] + 0.8 * math.sin(t * 1.4) + (1 - back(local / 0.55)) * 8 * (e['t0'] > 0)
            sp = polaroid(d['key'], d['box'], d['pw'], d['ph'], d['cap'], zoom, ang)
            yy = e['y'] - 40 + (0 if e['t0'] == 0 else (1 - ease(local / 0.4)) * 160) - (1 - q) * 30
            im.alpha_composite(with_alpha(sp, q * (1 if e['t0'] == 0 else min(1, local / 0.2))),
                               ((RW - sp.width) // 2, int(yy)))
        elif k == 'sticker':
            sp = e['data']
            s = 0.6 + 0.4 * back(local / 0.5)
            bob = 10 * math.sin(t * 2.2)
            sp2 = sp.resize((int(sp.width * s), int(sp.height * s)), Image.BICUBIC)
            im.alpha_composite(with_alpha(sp2, min(1, local / 0.15 + 0.01)),
                               ((RW - sp2.width) // 2 + 20, int(e['y'] + sp.height - sp2.height + bob)))
        else:  # rise
            sp = e['data']
            if e['x'] == 'chip':
                x = (RW - total) // 2 + row.get('badge', 0) + 6
            elif isinstance(e['x'], int):
                x = e['x']
            else:
                x = (RW - sp.width) // 2
            im.alpha_composite(with_alpha(sp, a), (x, int(e['y'] + dy)))
    return im.convert('RGB')


# ---------- áudio ----------
def phrases(narr):
    """Começo de cada fala (pausas acima de 0,28 s)."""
    r = subprocess.run(['ffmpeg', '-i', narr, '-af', 'silencedetect=noise=-38dB:d=0.28', '-f', 'null', '-'],
                       capture_output=True, text=True)
    starts, ends = [0.0], []
    for ln in r.stderr.splitlines():
        if 'silence_start' in ln:
            ends.append(float(ln.split('silence_start: ')[1]))
        if 'silence_end' in ln:
            starts.append(float(ln.split('silence_end: ')[1].split()[0]))
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                narr], capture_output=True, text=True).stdout)
    return starts, ends, dur


def mix(path, dur, narr=None):
    fade_out = dur - 1.4
    if narr:
        fc = (f'[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=10dB,apad=pad_dur=4,atrim=0:{dur},'
              'asplit=2[voc][sc];'
              f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},asetpts=PTS-STARTPTS,'
              f'volume=-11dB,afade=t=in:d=0.4,afade=t=out:st={fade_out}:d=1.4[mus];'
              '[mus][sc]sidechaincompress=threshold=0.015:ratio=6:attack=30:release=450:makeup=1[duck];'
              '[voc][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
        ins = ['-i', narr, '-i', MUSIC]
    else:
        fc = (f'[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},asetpts=PTS-STARTPTS,'
              f'afade=t=in:d=0.4,afade=t=out:st={fade_out}:d=1.4,loudnorm=I=-18:TP=-1.5:LRA=11[out]')
        ins = ['-i', MUSIC]
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '[out]',
                    '-ar', '48000', '-t', str(dur), path], check=True)


DRAFT_CUES = {'hook': [1.3], 'p1': [2.4], 'p2': [0.9, 2.9, 3.9], 'p3': [0.6, 4.4, 5.9, 7.0], 'cta': [1.2]}


def render(seg, cues, name, narr=None):
    E = build(seg, cues)
    dur = seg['fim']
    wav = OUT + name + '.wav'
    mix(wav, dur, narr)
    video = OUT + name + '-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset',
                            'medium', '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    snaps = {}
    want = [0.0, 1.6, seg['p1'] + 1.0, seg['p1'] + 3.2, seg['p2'] + 4.5, seg['p3'] + 1.0,
            seg['p3'] + 7.6, seg['cta'] + 1.6]
    for fi in range(int(round(dur * FPS))):
        t = fi / FPS
        fr = frame(t, E, seg)
        enc.stdin.write(fr.tobytes())
        for w in want:
            if abs(t - w) < 0.5 / FPS:
                snaps[w] = fr
    enc.stdin.close()
    enc.wait()
    final = OUT + name + '.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '192k', '-shortest', '-movflags', '+faststart', final], check=True)
    ims = [snaps[k].resize((270, 480)) for k in sorted(snaps)]
    sheet = Image.new('RGB', (280 * len(ims) + 10, 500), 'white')
    for i, x in enumerate(ims):
        sheet.paste(x, (10 + i * 280, 10))
    sheet.save(S + name + '-contato.jpg', quality=85)
    return final


if __name__ == '__main__':
    if len(sys.argv) > 1:
        narr = sys.argv[1]
        starts, ends, d = phrases(narr)
        print(json.dumps({'starts': starts, 'ends': ends, 'dur': d}))
    else:
        print(render(SEG, DRAFT_CUES, 'reel-info-rascunho'))
