"""Reel animado do ep. 1: 4 clipes do Higgsfield (5 s cada) + texto + caixinha de música."""
import subprocess
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_reel as br

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
CLIPS = [S + f'anim2/clip{i}.mp4' for i in (1, 2, 3, 4)]
OUT = S + 'reel/'
RW, RH, FPS = 1080, 1920, 30
SEG = 5.0
DUR = SEG * len(CLIPS)
TOP = br.TOP

TEXTS = [
    (0.0, 5.0, br.txt_head(['20:30.'], TOP, 130)),
    (0.8, 5.0, br.txt_head(['Ainda pulando', 'na cama?'], TOP + 150, 92)),
    (5.15, 10.0, br.txt_head(['1. Escovar os dentes'], TOP, 88)),
    (6.6, 10.0, br.txt_hand('Desenrolei!', TOP + 120, 96)),
    (10.15, 15.0, br.txt_head(['2. Uma história'], TOP, 92)),
    (11.6, 15.0, br.txt_hand('os olhinhos já pesando...', TOP + 120, 84)),
    (15.15, DUR, br.txt_head(['3. Luz apagada.'], TOP, 92)),
    (16.2, DUR, br.txt_hand('Boa noite, Bento!', TOP + 120, 96)),
    (17.4, DUR, br.txt_head(['Mostra pro seu filho', 'antes de dormir.'], TOP + 240, 68)),
]


def frames(path):
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', path, '-vf',
                          f'fps={FPS},scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = RW * RH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombytes('RGB', (RW, RH), b)
    p.wait()


def compose(im, t):
    im = im.convert('RGBA')
    im.alpha_composite(br.fade)
    for (a0, a1, lay) in TEXTS:
        if a0 <= t < a1:
            k = 1.0 if a0 == 0 else min(1.0, (t - a0) / 0.22)
            if k < 1:
                l2 = lay.copy()
                l2.putalpha(lay.getchannel('A').point(lambda v, k=k: int(v * k)))
                tmp = br.layer()
                tmp.alpha_composite(l2, (0, int((1 - k) * 24)))
                im.alpha_composite(tmp)
            else:
                im.alpha_composite(lay)
    return im.convert('RGB')


if __name__ == '__main__':
    br.DUR = DUR
    wav = OUT + 'musica-ep2.wav'
    br.musica(wav)
    video = OUT + 'reel-ep2-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset',
                            'medium', '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    snaps = {}
    for ci, c in enumerate(CLIPS):
        n_seg = int(SEG * FPS)
        last = None
        for fi, fr in enumerate(frames(c)):
            if fi >= n_seg:
                break
            t = ci * SEG + fi / FPS
            out = compose(fr, t)
            enc.stdin.write(out.tobytes())
            last = fr
            if fi in (5, 75):
                snaps[f'{t:04.1f}'] = out
        while fi < n_seg - 1:                       # completa se o clipe vier mais curto
            fi += 1
            t = ci * SEG + fi / FPS
            enc.stdin.write(compose(last, t).tobytes())
    enc.stdin.close()
    enc.wait()
    final = OUT + 'reel-ep2.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav,
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-ar', '44100', '-shortest', '-movflags', '+faststart', final], check=True)
    ims = [v.resize((270, 480)) for k, v in sorted(snaps.items())]
    sheet = Image.new('RGB', (280 * len(ims) + 10, 500), 'white')
    for i, x in enumerate(ims):
        sheet.paste(x, (10 + i * 280, 10))
    sheet.save(S + 'ep2-contato.jpg', quality=85)
    print('ok', final)
