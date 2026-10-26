"""Reel "Faz hoje": 3 coisas pra deixar prontas antes de dormir.
Visual de noite: céu azul com estrelas, quadro de giz com a lista sendo escrita e marcada, polaroides do Bento.

Uso:
  python3 build_reel_noite.py                         -> rascunho mudo com tempos estimados
  python3 build_reel_noite.py narr.mp3 musica.mp3     -> versão final encaixada na voz
"""
import json
import math
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_reel_info as bi
from build_reel_info import ease, back, text_sprite, headline, chip, with_alpha, polaroid, STICKER

S, OUT, RW, RH, FPS = bi.S, bi.OUT, bi.RW, bi.RH, bi.FPS
TITLE, HAND, BODYB = bi.TITLE, bi.HAND, bi.BODYB
CREAM = (250, 244, 230)
CHALK = (238, 234, 222)
CHALK_Y = (250, 222, 140)
MOON_HL = (252, 226, 160)
for k in (5,):
    bi.SRC[k] = Image.open(bi.C1 % k).convert('RGB')

SEG = {'hook': 0.0, 'i1': 6.0, 'i2': 10.6, 'i3': 14.0, 'fonte': 18.6, 'cta': 25.4, 'fim': 29.3}
DRAFT_CUES = {'hook': [1.4], 'i1': [1.2], 'i2': [1.0], 'i3': [1.2], 'fonte': [0.4], 'cta': [1.0]}


# ---------- fundo de noite ----------
def night_bg(seed=7):
    y = np.linspace(0, 1, RH)[:, None]
    top, bot = np.array([22, 30, 66]), np.array([58, 62, 118])
    g = top + (bot - top) * (y ** 0.9)
    a = np.repeat(g[:, None, :], RW, axis=1).reshape(RH, RW, 3)
    rng = np.random.default_rng(seed)
    a = a + rng.integers(-3, 4, size=(RH, RW, 1))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    glow = Image.new('L', (RW, RH), 0)
    ImageDraw.Draw(glow).ellipse((620, -260, 1340, 420), fill=70)
    lay = Image.new('RGBA', (RW, RH), (120, 130, 200, 0))
    lay.putalpha(glow.filter(ImageFilter.GaussianBlur(120)))
    im.alpha_composite(lay)
    return im


BG = night_bg()
rnd = random.Random(3)
STARS = [(rnd.randint(20, RW - 20), rnd.randint(20, RH - 300), rnd.choice((2, 2, 3, 4)), rnd.random() * 6.28,
          0.6 + rnd.random() * 1.6) for _ in range(90)]


def sky(t):
    im = BG.copy()
    d = ImageDraw.Draw(im)
    for (x, y, r, ph, sp) in STARS:
        a = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * sp + ph))
        c = tuple(int(v * a + 40 * (1 - a)) for v in (255, 246, 214))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    # lua crescente
    m = Image.new('L', (220, 220), 0)
    dm = ImageDraw.Draw(m)
    dm.ellipse((20, 20, 200, 200), fill=255)
    dm.ellipse((70, 0, 240, 170), fill=0)
    moon = Image.new('RGBA', (220, 220), (252, 236, 190, 0))
    moon.putalpha(m.filter(ImageFilter.GaussianBlur(1)))
    im.alpha_composite(moon, (820, 40 + int(6 * math.sin(t * 0.8))))
    return im


# ---------- quadro de giz ----------
BX0, BY0, BX1, BY1 = 80, 270, 1000, 790


def board_base():
    im = Image.new('RGBA', (RW, RH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((BX0 + 8, BY0 + 16, BX1 + 8, BY1 + 16), radius=26, fill=(8, 10, 30, 110))
    im = im.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((BX0, BY0, BX1, BY1), radius=26, fill=(150, 104, 62))
    d.rounded_rectangle((BX0 + 22, BY0 + 22, BX1 - 22, BY1 - 22), radius=12, fill=(40, 58, 52))
    a = np.asarray(im).astype(np.int16)
    rng = np.random.default_rng(5)
    region = a[BY0 + 22:BY1 - 22, BX0 + 22:BX1 - 22, :3]
    noise = rng.integers(-6, 7, size=region.shape[:2] + (1,))
    region += noise
    for _ in range(18):                                   # manchas de giz apagado
        cx, cy = rng.integers(0, region.shape[1]), rng.integers(0, region.shape[0])
        rr = rng.integers(40, 120)
        yy, xx = np.ogrid[:region.shape[0], :region.shape[1]]
        mask = ((xx - cx) ** 2 + (yy - cy) ** 2) < rr ** 2
        region[mask] += 5
    a[BY0 + 22:BY1 - 22, BX0 + 22:BX1 - 22, :3] = np.clip(region, 0, 255)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


BOARD = board_base()


def chalk(text, size, color=CHALK):
    sp = text_sprite(text, HAND, size, color + (255,))
    a = np.asarray(sp).copy()
    rng = np.random.default_rng(len(text))
    grain = rng.random(a.shape[:2]) > 0.18
    a[..., 3] = (a[..., 3] * grain * 0.92).astype(np.uint8)
    return Image.fromarray(a)


def chalk_check(p, size=54):
    """Caixinha + tique de giz desenhado até a fração p."""
    im = Image.new('RGBA', (size + 20, size + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, size + 6, size + 6), radius=8, outline=CHALK + (220,), width=5)
    pts = [(14, size * 0.55), (size * 0.45, size * 0.9), (size + 14, -4)]
    if p > 0:
        seg1 = min(1, p / 0.4)
        x0, y0 = pts[0]
        x1, y1 = pts[1]
        d.line([(x0, y0), (x0 + (x1 - x0) * seg1, y0 + (y1 - y0) * seg1)], fill=CHALK_Y + (255,), width=9)
        if p > 0.4:
            seg2 = (p - 0.4) / 0.6
            x2, y2 = pts[2]
            d.line([(x1, y1), (x1 + (x2 - x1) * seg2, y1 + (y2 - y1) * seg2)], fill=CHALK_Y + (255,), width=9)
    return im


TITLE_CHALK = chalk('Antes de dormir:', 76, CHALK_Y)
ITEMS = [chalk('roupa separada (2 opções)', 70), chalk('mochila na porta', 70), chalk('quadro dos passos', 70)]
ITEM_Y = [425, 540, 655]


def write_reveal(sp, p):
    """Mostra o texto 'sendo escrito' da esquerda pra direita."""
    w = max(1, int(sp.width * ease(p)))
    out = Image.new('RGBA', sp.size, (0, 0, 0, 0))
    out.paste(sp.crop((0, 0, w, sp.height)), (0, 0))
    return out


# ---------- textos ----------
def dark_fade():
    h = 980
    g = Image.new('L', (1, h))
    for y in range(h):
        g.putpixel((0, y), int(235 * (1 - y / h) ** 1.2))
    lay = Image.new('RGBA', (RW, h), (22, 30, 66, 0))
    lay.putalpha(g.resize((RW, h)))
    return lay


FADE = dark_fade()


def strong(hl):
    """Pincel mais forte pra ler bem no fundo escuro."""
    br, tx = hl
    br = br.copy()
    br.putalpha(br.getchannel('A').point(lambda v: min(255, int(v * 1.9))))
    return br, tx


HOOK_H = strong(headline(['A manhã de amanhã', 'começa hoje à noite.'], 94, MOON_HL, 11))
HOOK_HAND = [text_sprite('3 coisas pra deixar prontas', HAND, 76, CHALK_Y + (255,), 4, (22, 30, 66, 255)),
             text_sprite('antes de dormir', HAND, 76, CHALK_Y + (255,), 4, (22, 30, 66, 255))]
FONTE_TXT = strong(headline(['Preparar na noite', 'anterior ajuda a', 'diminuir a briga', 'da manhã.'], 78, MOON_HL, 12))
FONTE_CHIP = chip('Academia Americana de Pediatria', 34)
CTA_H = strong(headline(['Salva pra fazer', 'hoje à noite.'], 104, MOON_HL, 13))
HANDLE = text_sprite('@paisdarotina', BODYB, 42, CREAM + (255,))
NUM = {}
for n in (1, 2, 3):
    NUM[n] = chalk(f'{n}.', 64, CHALK_Y)

POLA = {
    'i1': dict(key=8, box=(0.0, 0.22, 1.0, 0.86), cap='vestido sem briga', ang=-3),
    'i2': dict(key=5, box=(0.0, 0.25, 1.0, 0.95), cap='mochila na porta', ang=3),
    'i3': dict(key=3, box=(0.05, 0.12, 1.0, 0.86), cap='os 3 passos na parede', ang=-2),
}


CLIP_DIR = S + 'anim2/clip4_frames/'
CLIP_N = 189


def hook_scene(t):
    """Gancho com o Bento animado dormindo (clipe do ep. 2, 0,8x), pra o quadro 0 já ter movimento."""
    i = min(CLIP_N, max(1, int(t * FPS) + 1))
    im = Image.open(CLIP_DIR + 'f%04d.jpg' % i).convert('RGBA')
    im.alpha_composite(FADE)
    return im


def fade_ab(seg, part, t, din=0.25, dout=0.2):
    order = ['hook', 'i1', 'i2', 'i3', 'fonte', 'cta', 'fim']
    t0 = seg[part]
    t1 = seg[order[order.index(part) + 1]] if part != 'cta' else 1e9
    if t < t0 or t >= t1:
        return 0.0, 0.0
    p = 1.0 if t0 == 0 else ease((t - t0) / din)
    q = ease((t1 - t) / dout)
    return p, q


def frame(t, seg, cues):
    parts = ['hook', 'i1', 'i2', 'i3', 'fonte', 'cta']
    cur = max([p for p in parts if seg[p] <= t], key=lambda p: seg[p])
    if cur == 'hook':
        im = hook_scene(t)
    else:
        im = sky(t)
        if t - seg['i1'] < 0.35:                          # passagem da cena do gancho pro céu
            k = ease((t - seg['i1']) / 0.35)
            im = Image.blend(hook_scene(t), im, k)
    # ---- gancho
    if cur == 'hook':
        br, tx = HOOK_H
        w = ease((t + 0.15) / 0.45)
        x = (RW - br.width) // 2
        im.alpha_composite(br.crop((0, 0, max(1, int(br.width * w)), br.height)), (x, 290))
        im.alpha_composite(tx, (x, 290))
        r0 = cues['hook'][0]
        for j, sp in enumerate(HOOK_HAND):
            k = ease((t - r0 - 0.25 * j) / 0.3)
            if k > 0:
                im.alpha_composite(with_alpha(sp, k), ((RW - sp.width) // 2, int(560 + 86 * j + (1 - k) * 30)))
    # ---- quadro (i1 até fonte)
    if seg['i1'] <= t < seg['cta']:
        kb = ease((t - seg['i1']) / 0.3)
        qb = ease((seg['cta'] - t) / 0.2)
        a = kb * qb
        dy = int((1 - kb) * -40)
        im.alpha_composite(with_alpha(BOARD, a), (0, dy))
        im.alpha_composite(with_alpha(TITLE_CHALK, a), (BX0 + 60, BY0 + 40 + dy))
        for n, part in enumerate(['i1', 'i2', 'i3']):
            if t < seg[part]:
                continue
            local = t - seg[part]
            wr = local / 0.7 if part != cur or True else 1
            y = ITEM_Y[n] + dy
            im.alpha_composite(with_alpha(chalk_check(min(1, max(0, (local - cues[part][0]) / 0.45))), a),
                               (BX0 + 60, y + 6))
            im.alpha_composite(with_alpha(write_reveal(NUM[n + 1], min(1, local / 0.2)), a), (BX0 + 140, y - 4))
            im.alpha_composite(with_alpha(write_reveal(ITEMS[n], min(1, wr)), a), (BX0 + 200, y - 4))
    # ---- polaroide de cada item
    if cur in POLA:
        p, q = fade_ab(seg, cur, t)
        d = POLA[cur]
        local = t - seg[cur]
        span = (seg[{'i1': 'i2', 'i2': 'i3', 'i3': 'fonte'}[cur]] - seg[cur])
        ang = d['ang'] + 0.8 * math.sin(t * 1.4) + (1 - back(local / 0.5)) * 8
        sp = polaroid(d['key'], d['box'], 520, 440, d['cap'], 1.0 + 0.06 * local / span, ang)
        yy = 800 + (1 - ease(local / 0.4)) * 160 - (1 - q) * 30
        im.alpha_composite(with_alpha(sp, min(p, q, local / 0.2 if local < 0.2 else 1)),
                           ((RW - sp.width) // 2, int(yy)))
    # ---- fonte
    if cur == 'fonte':
        p, q = fade_ab(seg, 'fonte', t)
        local = t - seg['fonte']
        br, tx = FONTE_TXT
        x = (RW - br.width) // 2
        w = ease((local - cues['fonte'][0]) / 0.5)
        if w > 0:
            im.alpha_composite(with_alpha(br.crop((0, 0, max(1, int(br.width * w)), br.height)), q), (x, 850))
            im.alpha_composite(with_alpha(tx, min(1, w * 2) * q), (x, 850))
        k = ease((local - cues['fonte'][0] - 0.6) / 0.3) * q
        if k > 0:
            im.alpha_composite(with_alpha(FONTE_CHIP, k), ((RW - FONTE_CHIP.width) // 2, 1250 + int((1 - k) * 20)))
    # ---- fim
    if cur == 'cta':
        local = t - seg['cta']
        br, tx = CTA_H
        x = (RW - br.width) // 2
        w = ease(local / 0.4)
        im.alpha_composite(br.crop((0, 0, max(1, int(br.width * w)), br.height)), (x, 300))
        im.alpha_composite(with_alpha(tx, min(1, local / 0.2 + 0.01)), (x, 300))
        s = 0.6 + 0.4 * back(local / 0.5)
        st = STICKER.resize((int(STICKER.width * s), int(STICKER.height * s)), Image.BICUBIC)
        im.alpha_composite(with_alpha(st, min(1, local / 0.15 + 0.01)),
                           ((RW - st.width) // 2 + 20, int(620 + STICKER.height - st.height + 10 * math.sin(t * 2.2))))
        k = ease((local - cues['cta'][0]) / 0.3)
        if k > 0:
            im.alpha_composite(with_alpha(HANDLE, k), ((RW - HANDLE.width) // 2, 1480))
    return im.convert('RGB')


# ---------- encaixe na voz ----------
def fit_to_voice(narr):
    """Acha o começo de cada fala pelas pausas: gancho(2 frases), um, dois, três, fonte, pedido."""
    starts, ends, dur = bi.phrases(narr)
    return starts, ends, dur


def mix(path, dur, narr, music):
    fo = dur - 1.4
    if narr:
        fc = (f'[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=10dB,apad=pad_dur=4,atrim=0:{dur},'
              'asplit=2[voc][sc];'
              f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},asetpts=PTS-STARTPTS,'
              f'volume=-11dB,afade=t=in:d=0.4,afade=t=out:st={fo}:d=1.4[mus];'
              '[mus][sc]sidechaincompress=threshold=0.015:ratio=6:attack=30:release=450:makeup=1[duck];'
              '[voc][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
        ins = ['-i', narr, '-i', music]
    else:
        fc = f'anullsrc=r=48000:cl=stereo,atrim=0:{dur}[out]'
        ins = []
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '[out]',
                    '-ar', '48000', '-t', str(dur), path], check=True)


def render(seg, cues, name, narr=None, music=None):
    dur = seg['fim']
    wav = OUT + name + '.wav'
    mix(wav, dur, narr, music)
    video = OUT + name + '-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset',
                            'medium', '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    want = [0.0, 2.2, seg['i1'] + 1.8, seg['i2'] + 1.8, seg['i3'] + 2.5, seg['fonte'] + 2.0,
            seg['cta'] + 1.5]
    snaps = {}
    for fi in range(int(round(dur * FPS))):
        t = fi / FPS
        fr = frame(t, seg, cues)
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
    if len(sys.argv) > 2:
        print(json.dumps(fit_to_voice(sys.argv[1])))
    else:
        print(render(SEG, DRAFT_CUES, 'reel-noite-rascunho'))
