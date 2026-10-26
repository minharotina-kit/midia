"""Família Tatu, parte 1: A Aposta. Junta os 4 clipes do Grok com título, horas, legendas e cartão da parte 2."""
import subprocess
import sys

from PIL import Image, ImageDraw, ImageEnhance

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_reel_info as bi
from build_reel_info import ease, back, text_sprite, headline, with_alpha

S = bi.S
G = S + 'grok/'
OUT = S + 'reel/'
RW, RH, FPS = 1080, 1920, 30
TITLE, HAND, BODYB = bi.TITLE, bi.HAND, bi.BODYB
NAVY, CORAL, WHITE = (36, 44, 86), (214, 96, 80), (255, 252, 246)

# (arquivo, início no clipe, fim no clipe)
CLIPS = [('g4.mp4', 0.0, 6.0), ('g3.mp4', 0.0, 6.4), ('g1.mp4', 0.0, 4.6), ('g2.mp4', 0.0, 4.3)]
END = 2.8                                   # cartão final congelado
starts = []
t = 0.0
for c in CLIPS:
    starts.append(t)
    t += c[2] - c[1]
CARD0 = t
DUR = CARD0 + END


def strong(hl, k=1.9):
    br, tx = hl
    br = br.copy()
    br.putalpha(br.getchannel('A').point(lambda v: min(255, int(v * k))))
    return br, tx


def pill(text, bg, size=54):
    sp = text_sprite(text, BODYB, size, WHITE + (255,))
    im = Image.new('RGBA', (sp.width + 40, sp.height + 16), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=im.height // 2,
                                         fill=bg + (235,))
    im.alpha_composite(sp, (20, 8))
    return im


TITLE_H = strong(headline(['Família Tatu'], 104, (252, 226, 160), 21))
SUBT = text_sprite('Parte 1 · A Aposta', HAND, 80, WHITE + (255,), 5, (40, 30, 30, 255))


def clock(text):
    return text_sprite(text, HAND, 96, WHITE + (255,), 6, (30, 30, 50, 255))


# legendas: (início, fim, sprite, quem) em tempo do episódio
c0, c1, c2, c3 = starts
CAPS = [
    (c0 + 1.0, c0 + 3.0, pill('Hoje eu faço o Bento dormir.', NAVY)),
    (c0 + 3.35, c0 + 4.6, pill('Cinco minutos.', NAVY)),
    (c0 + 4.6, c0 + 6.0, pill('Aposta?', CORAL)),
    (c1 + 0.85, c1 + 2.9, pill('Bento, deita, por favor.', NAVY)),
    (c1 + 4.0, c1 + 6.4, pill('Bento… por favor…', NAVY)),
    (c3 + 2.0, c3 + 4.3, pill('Agora é comigo.', CORAL, 60)),
]
TOPS = [
    (c1 + 0.0, c1 + 6.4, clock('20h10'), 270),
    (c2 + 0.0, c2 + 4.6, clock('21h10'), 270),
    (c2 + 0.5, c2 + 4.6, text_sprite('(cinco minutos, ele disse)', HAND, 70, WHITE + (255,), 5, (30, 30, 50, 255)), 380),
]
CARD_H = strong(headline(['Parte 2:', 'o segredo da', 'Mamãe Tatu'], 96, (247, 201, 168), 22))
CARD_T = text_sprite('amanhã, 20h30', HAND, 92, WHITE + (255,), 6, (30, 30, 50, 255))
CARD_F = text_sprite('Segue pra não perder · @minharotina.kit', BODYB, 38, WHITE + (255,), 4, (30, 30, 50, 255))


def frames(path, t0, t1):
    vf = (f'fps={FPS},scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}')
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', path,
                          '-map', '0:v:0', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    n = RW * RH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombytes('RGB', (RW, RH), b)
    p.wait()


def overlay(im, t):
    im = im.convert('RGBA')
    if t < 2.8:                                              # título já no quadro 0
        q = ease((2.8 - t) / 0.25)
        br, tx = TITLE_H
        x = (RW - br.width) // 2
        w = ease((t + 0.15) / 0.45)
        im.alpha_composite(with_alpha(br.crop((0, 0, max(1, int(br.width * w)), br.height)), q), (x, 270))
        im.alpha_composite(with_alpha(tx, q), (x, 270))
        k = min(1.0, ease((t - 0.35) / 0.3)) * q
        if k > 0:
            im.alpha_composite(with_alpha(SUBT, k), ((RW - SUBT.width) // 2, 410))
    for a0, a1, sp, y in TOPS:
        if a0 <= t < a1:
            k = min(ease((t - a0) / 0.25), ease((a1 - t) / 0.2))
            im.alpha_composite(with_alpha(sp, k), ((RW - sp.width) // 2, int(y + (1 - k) * 20)))
    for a0, a1, sp in CAPS:
        if a0 <= t < a1:
            k = min(ease((t - a0) / 0.12), ease((a1 - t) / 0.12))
            im.alpha_composite(with_alpha(sp, k), ((RW - sp.width) // 2, 1330))
    return im


def card(last, t):
    local = t - CARD0
    z = 1.0 + 0.06 * (local / END)
    w, h = RW / z, RH / z
    im = last.resize((RW, RH), Image.BICUBIC, box=((RW - w) / 2, (RH - h) * 0.35, (RW + w) / 2, (RH - h) * 0.35 + h))
    im = ImageEnhance.Brightness(im).enhance(1 - 0.45 * ease(local / 0.4)).convert('RGBA')
    br, tx = CARD_H
    x = (RW - br.width) // 2
    wv = ease((local - 0.1) / 0.45)
    if wv > 0:
        im.alpha_composite(br.crop((0, 0, max(1, int(br.width * wv)), br.height)), (x, 330))
        im.alpha_composite(with_alpha(tx, min(1, wv * 2)), (x, 330))
    k = ease((local - 0.6) / 0.3)
    if k > 0:
        im.alpha_composite(with_alpha(CARD_T, k), ((RW - CARD_T.width) // 2, int(700 + (1 - k) * 20)))
    k2 = ease((local - 1.0) / 0.3)
    if k2 > 0:
        im.alpha_composite(with_alpha(CARD_F, k2), ((RW - CARD_F.width) // 2, 1420))
    return im


def audio(path):
    parts, labels = [], []
    for i, (f, t0, t1) in enumerate(CLIPS):
        parts += ['-i', G + f]
    parts += ['-i', G + 'g2.mp4']
    fc = ''
    for i, (f, t0, t1) in enumerate(CLIPS):
        fc += (f'[{i}:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,aresample=48000,'
               f'aformat=channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st={t1 - t0 - 0.06}:d=0.06[a{i}];')
        labels.append(f'[a{i}]')
    fc += (f'[4:a]atrim=6.0:{6.0 + END},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,'
           f'volume=6dB,afade=t=in:d=0.1,afade=t=out:st={END - 0.8}:d=0.8[a4];')
    labels.append('[a4]')
    fc += ''.join(labels) + f'concat=n={len(labels)}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11[out]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *parts, '-filter_complex', fc, '-map', '[out]',
                    '-ar', '48000', path], check=True)


if __name__ == '__main__':
    name = 'reel-tatu-ep1'
    wav = OUT + name + '.wav'
    audio(wav)
    video = OUT + name + '-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    snaps, last = {}, None
    want = [0.0, 1.5, starts[1] + 1.5, starts[2] + 1.5, starts[3] + 3.0, CARD0 + 2.0]
    for (f, t0, t1), st in zip(CLIPS, starts):
        need = round((t1 - t0) * FPS)
        got = 0
        for fr in frames(G + f, t0, t1):
            if got >= need:
                break
            tt = st + got / FPS
            out = overlay(fr, tt).convert('RGB')
            enc.stdin.write(out.tobytes())
            for w in want:
                if abs(tt - w) < 0.5 / FPS:
                    snaps[w] = out
            last, got = fr, got + 1
        while got < need:
            tt = st + got / FPS
            enc.stdin.write(overlay(last, tt).convert('RGB').tobytes())
            got += 1
    for i in range(round(END * FPS)):
        tt = CARD0 + i / FPS
        out = card(last, tt).convert('RGB')
        enc.stdin.write(out.tobytes())
        for w in want:
            if abs(tt - w) < 0.5 / FPS:
                snaps[w] = out
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
    print(final, round(DUR, 2))
