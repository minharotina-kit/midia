"""Reel do ep. 1: as cenas com movimento lento, texto animado e caixinha de música original."""
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import compose
from compose import headline, body, HAND, BODY, ACCENT, INK

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
C = S + 'zip-cenas/Bento_Ep1_Cena_0%d.png'
OUT = S + 'reel/'
os.makedirs(OUT, exist_ok=True)
RW, RH, FPS = 1080, 1920, 30
DUR = 23.0
TOP = 260                       # texto começa abaixo da área do nome
XF = 0.3                        # crossfade entre cenas

paper = Image.open(C % 6).convert('RGB').getpixel((20, 20))

# cena: (arquivo, início, fim, zoom_ini, zoom_fim, cx_ini, cx_fim, cy) em fração da imagem
SEGS = [
    (1, 0.0, 3.2, 1.00, 1.10, 0.50, 0.50, 0.55),
    (2, 3.2, 6.4, 1.04, 1.14, 0.48, 0.52, 0.52),
    (3, 6.4, 9.4, 1.06, 1.06, 0.42, 0.56, 0.50),
    (4, 9.4, 13.4, 1.00, 1.08, 0.55, 0.55, 0.50),
    (5, 13.4, 16.6, 1.10, 1.00, 0.45, 0.45, 0.52),
    ('papel', 16.6, 20.6, 1.0, 1.0, 0.5, 0.5, 0.5),
    (1, 20.6, DUR, 1.12, 1.00, 0.50, 0.50, 0.55),
]


def layer():
    return Image.new('RGBA', (RW, RH), (0, 0, 0, 0))


def txt_head(lines, y, size=92):
    im = layer()
    compose.W = RW
    headline(im, lines, y, size=size)
    return im


def txt_hand(text, y, size=78):
    im = layer()
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(HAND, size)
    for ln in compose.wrap(d, text, f, 900):
        tw = d.textlength(ln, font=f)
        d.text(((RW - tw) / 2, y), ln, font=f, fill=ACCENT, stroke_width=5,
               stroke_fill=(255, 246, 236))
        y += size + 6
    return im


def txt_body(text, y, size=46):
    im = layer()
    compose.W = RW
    body(im, text, y, size=size, max_w=900)
    return im


# textos: (início, fim, camada)
TEXTS = [
    (0.0, 3.2, txt_head(['06:50.'], TOP, 130)),
    (0.85, 3.2, txt_head(['Ainda de pijama?'], TOP + 150, 96)),
    (3.35, 6.4, txt_head(['Sem saber o que', 'vem depois...'], TOP, 92)),
    (4.3, 6.4, txt_hand('o Bento vira bolinha e sai rolando!', TOP + 230)),
    (6.55, 9.4, txt_head(['A manhã dele', 'tem 3 passos.'], TOP, 92)),
    (9.55, 13.4, txt_head(['1. Abrir a janela'], TOP, 84)),
    (10.35, 13.4, txt_head(['2. Lavar o rosto'], TOP + 96, 84)),
    (11.15, 13.4, txt_head(['3. Vestir a roupa'], TOP + 192, 84)),
    (12.0, 13.4, txt_hand('Desenrolei!', TOP + 300, 96)),
    (13.55, 16.6, txt_head(['07:09.', 'Deu tempo!'], TOP, 104)),
    (14.6, 16.6, txt_hand('Bi-bi!', TOP + 250, 104)),
    (16.75, 20.6, txt_head(['Por que funciona?'], TOP + 40, 88)),
    (17.4, 20.6, txt_body('Quando a ordem é sempre a mesma, a criança sabe o que vem depois.',
                          TOP + 180)),
    (18.2, 20.6, txt_body('Academia Americana de Pediatria', TOP + 360, 34)),
    (20.75, DUR, txt_head(['Amanhã, 06:50...'], TOP, 100)),
    (21.4, DUR, txt_hand('Salva pra assistir com ele!', TOP + 150, 82)),
]

# fundo creme no topo para o texto ler bem
fade = Image.new('RGBA', (RW, 820), paper + (0,))
g = Image.new('L', (1, 820))
for y in range(820):
    g.putpixel((0, y), int(225 * (1 - y / 820) ** 1.3))
fade.putalpha(g.resize((RW, 820)))

SRC = {i: Image.open(C % i).convert('RGB') for i in (1, 2, 3, 4, 5)}


def papel_frame():
    im = Image.new('RGB', (RW, RH), paper)
    b = Image.open(C % 6).convert('RGB').crop((120, 300, 1000, 1360))
    b = b.resize((round(b.width * 0.74), round(b.height * 0.74)), Image.LANCZOS)
    im.paste(b, ((RW - b.width) // 2 + 20, RH - 360 - b.height))
    return im


PAPEL = papel_frame()


def scene_frame(seg, t):
    key, t0, t1, z0, z1, cx0, cx1, cy = seg
    if key == 'papel':
        return PAPEL.copy()
    src = SRC[key]
    k = (t - t0) / (t1 - t0)
    k = k * k * (3 - 2 * k)                   # suave
    z = z0 + (z1 - z0) * k
    cx = (cx0 + (cx1 - cx0) * k) * src.width
    s0 = max(RW / src.width, RH / src.height)
    ww, hh = RW / (s0 * z), RH / (s0 * z)
    cyp = cy * src.height
    x0 = min(max(cx - ww / 2, 0), src.width - ww)
    y0 = min(max(cyp - hh / 2, 0), src.height - hh)
    im = src.resize((RW, RH), Image.BILINEAR, box=(x0, y0, x0 + ww, y0 + hh))
    if key == 2:                              # tremidinha da bolinha rolando
        dx = int(6 * np.sin(t * 22))
        im = im.transform(im.size, Image.AFFINE, (1, 0, dx, 0, 1, 0), Image.BILINEAR)
    return im


def frame_at(t):
    cur = [s for s in SEGS if s[1] <= t < s[2]] or [SEGS[-1]]
    seg = cur[0]
    im = scene_frame(seg, t).convert('RGBA')
    i = SEGS.index(seg)
    if i > 0 and t - seg[1] < XF:              # crossfade com a cena anterior
        prev = scene_frame(SEGS[i - 1], min(t, SEGS[i - 1][2] - 1e-3)).convert('RGBA')
        a = (t - seg[1]) / XF
        im = Image.blend(prev, im, a)
    if seg[0] != 'papel':
        im.alpha_composite(fade)
    for (a0, a1, lay) in TEXTS:
        if a0 <= t < a1:
            k = 1.0 if a0 == 0 else min(1.0, (t - a0) / 0.22)
            if k < 1:
                al = lay.getchannel('A').point(lambda v, k=k: int(v * k))
                l2 = lay.copy()
                l2.putalpha(al)
                off = int((1 - k) * 24)
                tmp = layer()
                tmp.alpha_composite(l2, (0, off))
                im.alpha_composite(tmp)
            else:
                im.alpha_composite(lay)
    return im.convert('RGB')


def musica(path):
    sr = 44100
    n = int(DUR * sr)
    out = np.zeros(n + sr * 2)
    beat = 60 / 100
    # melodia original em dó maior pentatônica (nota MIDI, início em batidas, duração)
    mel = [72, 76, 79, 76, 81, 79, 76, 74, 72, 74, 76, 79, 76, 74, 72, 67,
           72, 76, 79, 81, 84, 81, 79, 76, 74, 76, 79, 76, 74, 72, 74, 72]
    rit = [1, .5, .5, 1, 1, .5, .5, 1, 1, .5, .5, 1, .5, .5, 1, 1] * 2
    t = 0.0
    seq = []
    while t < DUR / beat:
        for m, r in zip(mel, rit):
            seq.append((m, t))
            t += r
            if t >= DUR / beat:
                break

    def tine(freq, dur, amp):
        tt = np.arange(int(dur * sr)) / sr
        env = np.exp(-tt / 0.75) * np.minimum(1, tt / 0.004)
        w = (np.sin(2 * np.pi * freq * tt) + 0.22 * np.sin(2 * np.pi * 2 * freq * tt) * np.exp(-tt / 0.25)
             + 0.08 * np.sin(2 * np.pi * 4.2 * freq * tt) * np.exp(-tt / 0.08))
        return amp * w * env

    for m, b in seq:
        f = 440 * 2 ** ((m - 69) / 12)
        i0 = int(b * beat * sr)
        x = tine(f, 2.2, 0.32)
        out[i0:i0 + len(x)] += x[:len(out) - i0]
    for bar in range(int(DUR / (4 * beat)) + 1):       # baixo suave no começo de cada compasso
        root = [48, 45, 41, 43][bar % 4]
        f = 440 * 2 ** ((root - 69) / 12)
        i0 = int(bar * 4 * beat * sr)
        tt = np.arange(int(2.4 * sr)) / sr
        x = 0.18 * np.sin(2 * np.pi * f * tt) * np.exp(-tt / 1.1) * np.minimum(1, tt / 0.01)
        out[i0:i0 + len(x)] += x[:len(out) - i0]
    rev = out.copy()
    for d, g_ in ((0.11, 0.28), (0.23, 0.18), (0.37, 0.10)):
        k = int(d * sr)
        rev[k:] += g_ * out[:-k]
    rev = rev[:n]
    fo = int(0.6 * sr)
    rev[-fo:] *= np.linspace(1, 0, fo)
    rev /= np.max(np.abs(rev)) * 1.12
    pcm = (rev * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


if __name__ == '__main__':
    wav = OUT + 'musica.wav'
    musica(wav)
    video = OUT + 'reel-ep1-sem-audio.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264',
                          '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', video],
                         stdin=subprocess.PIPE)
    nf = int(DUR * FPS)
    for fi in range(nf):
        p.stdin.write(frame_at(fi / FPS).tobytes())
    p.stdin.close()
    p.wait()
    final = OUT + 'reel-ep1.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav,
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-ar', '44100', '-shortest', '-movflags', '+faststart', final], check=True)
    for t in (0.0, 1.2, 4.8, 11.8, 15.0, 18.6, 22.0):
        frame_at(t).resize((360, 640)).save(OUT + f'quadro-{t:04.1f}.jpg', quality=80)
    print('ok', final)
