"""Episódio da Família Tatu com narradora estilo "Todo Mundo Odeia o Chris".

Os clipes chegam com as falas dos personagens. A narradora entra em quadros congelados (freeze) ou por cima
de trechos sem fala. Uso: python3 build_tatu_narrado.py config.json

config:
{ "name": "...", "dir": "pasta dos clipes", "title": ["Família Tatu"], "subtitle": "Parte 2 · ...",
  "segments": [
     {"clip": "c1.mp4", "t0": 0, "t1": 3.8, "caps": [[l0, l1, "texto", "mae|pai|bento|vovo"]],
      "narr": [[local_t, "n1"]]},
     {"freeze": "c1.mp4", "at": 3.8, "dur": 2.4, "narr": [[0.25, "n2"]],
      "src": [[0.2, 2.4, "Academia Americana de Pediatria"]]},
     {"card": 3.4, "lines": ["Parte 3:", "A Manhã do Papai"], "when": "amanhã, 20h", "narr": [[0.3, "n7"]]}
  ],
  "narr": {"n1": ["arquivo.wav", "legenda da narradora"]},
  "music": "musica.mp3", "music_start": 0, "music_db": -16 }

"src": selo "FONTE" no alto da tela enquanto a narradora fala um dado real (só fatos do BANCO-DE-FONTES.md).
"""
import json
import subprocess
import sys

from PIL import Image, ImageEnhance

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_tatu_ep1 as te
from build_reel_info import ease, text_sprite, with_alpha

S, OUT = te.S, te.OUT
RW, RH, FPS = te.RW, te.RH, te.FPS
WHITE, NAVY, CORAL = te.WHITE, te.NAVY, te.CORAL
GREEN = (58, 120, 84)
PURPLE = (112, 84, 150)
COLORS = {'pai': NAVY, 'mae': CORAL, 'bento': GREEN, 'vovo': PURPLE}
NARR_FILL = (255, 236, 170, 255)


def narr_sprite(text):
    """Legenda da narradora: amarelinha, sem caixa, com contorno, em até 2 linhas."""
    words = text.split()
    if len(text) <= 26:
        lines = [text]
    else:  # quebra em 2 linhas do tamanho mais parecido possível
        best = min(range(1, len(words)), key=lambda i: abs(len(' '.join(words[:i])) - len(' '.join(words[i:]))))
        lines = [' '.join(words[:best]), ' '.join(words[best:])]
    sps = [text_sprite(l, te.BODYB, 54, NARR_FILL, 6, (24, 22, 40, 255)) for l in lines]
    w = max(s.width for s in sps)
    h = sum(s.height for s in sps) + 6 * (len(sps) - 1)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    y = 0
    for s in sps:
        im.alpha_composite(s, ((w - s.width) // 2, y))
        y += s.height + 6
    return im


def src_sprite(text):
    """Selo da fonte: cartão creme com "FONTE" em coral e a instituição em azul-marinho."""
    from PIL import ImageDraw
    a = text_sprite('FONTE', te.BODYB, 30, CORAL + (255,))
    b = text_sprite(text, te.BODYB, 42, NAVY + (255,))
    w = max(a.width, b.width) + 56
    h = a.height + b.height + 34
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=26, fill=(255, 248, 232, 240),
                                         outline=CORAL + (255,), width=3)
    im.alpha_composite(a, ((w - a.width) // 2, 14))
    im.alpha_composite(b, ((w - b.width) // 2, 14 + a.height + 6))
    return im


def probe_dur(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def grab_frame(path, t):
    vf = f'scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}'
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(max(0, t - 0.06)), '-i', path, '-map', '0:v:0',
                        '-frames:v', '1', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True, check=True)
    return Image.frombytes('RGB', (RW, RH), r.stdout[:RW * RH * 3])


def run(cfg):
    D = cfg['dir'].rstrip('/') + '/'
    name = cfg['name']
    narr = {k: (v[0], v[1], probe_dur(v[0])) for k, v in cfg['narr'].items()}
    nsp = {k: narr_sprite(v[1]) for k, v in narr.items()}
    title = te.strong(te.headline(cfg.get('title', ['Família Tatu']), 104, (252, 226, 160), 21))
    subt = text_sprite(cfg['subtitle'], te.HAND, 76, WHITE + (255,), 5, (40, 30, 30, 255))
    handle = text_sprite('Segue pra não perder · @paisdarotina', te.BODYB, 38, WHITE + (255,), 4, (30, 30, 50, 255))

    # linha do tempo
    t = 0.0
    segs = []
    for sg in cfg['segments']:
        if 'clip' in sg:
            d = sg['t1'] - sg['t0']
        elif 'freeze' in sg:
            d = sg['dur']
        else:
            d = sg['card']
        segs.append((t, d, sg))
        t += d
    DUR = t
    narr_events = []  # (início global, chave)
    caps = []         # (início, fim, sprite)
    srcs = []         # selos de fonte (início, fim, sprite)
    for st, d, sg in segs:
        for lt, key in sg.get('narr', []):
            narr_events.append((st + lt, key))
        for l0, l1, txt, who in sg.get('caps', []):
            caps.append((st + l0, st + l1, te.pill(txt, COLORS[who])))
        for l0, l1, txt in sg.get('src', []):
            srcs.append((st + l0, st + l1, src_sprite(txt)))
    ncaps = [(t0, t0 + narr[k][2] + 0.15, nsp[k]) for t0, k in narr_events]

    def overlay(im, tt, freeze=False):
        im = im.convert('RGBA')
        tl = cfg.get('title_until', 2.6)
        if tt < tl:
            q = ease((tl - tt) / 0.3)
            br, tx = title
            x = (RW - br.width) // 2
            w = ease((tt + 0.15) / 0.45)
            im.alpha_composite(with_alpha(br.crop((0, 0, max(1, int(br.width * w)), br.height)), q), (x, 270))
            im.alpha_composite(with_alpha(tx, q), (x, 270))
            k = min(1.0, ease((tt - 0.3) / 0.3)) * q
            if k > 0:
                im.alpha_composite(with_alpha(subt, k), ((RW - subt.width) // 2, 410))
        for a0, a1, sp in caps:
            if a0 <= tt < a1:
                a = min(ease((tt - a0) / 0.1), ease((a1 - tt) / 0.1))
                im.alpha_composite(with_alpha(sp, a), ((RW - sp.width) // 2, 1330))
        for a0, a1, sp in ncaps:
            if a0 <= tt < a1:
                a = min(ease((tt - a0) / 0.12), ease((a1 - tt) / 0.15))
                y = 1180 if not any(c0 <= tt < c1 for c0, c1, _ in caps) else 1080
                im.alpha_composite(with_alpha(sp, a), ((RW - sp.width) // 2, y - sp.height // 2))
        for a0, a1, sp in srcs:
            if a0 <= tt < a1:
                a = min(ease((tt - a0) / 0.25), ease((a1 - tt) / 0.2))
                im.alpha_composite(with_alpha(sp, a), ((RW - sp.width) // 2, int(240 - (1 - a) * 24)))
        return im

    def freeze_img(base, local, d):
        z = 1.0 + 0.04 * ease(local / max(d, 0.1))
        w, h = RW / z, RH / z
        im = base.resize((RW, RH), Image.BICUBIC, box=((RW - w) / 2, (RH - h) * 0.45, (RW + w) / 2, (RH - h) * 0.45 + h))
        k = ease(local / 0.15)
        im = ImageEnhance.Color(im).enhance(1 - 0.25 * k)
        if local < 0.08:  # flashzinho de "pausa"
            im = ImageEnhance.Brightness(im).enhance(1.25)
        return im

    def card_img(base, local, d, sg):
        z = 1.0 + 0.05 * (local / d)
        w, h = RW / z, RH / z
        im = base.resize((RW, RH), Image.BICUBIC, box=((RW - w) / 2, (RH - h) * 0.35, (RW + w) / 2, (RH - h) * 0.35 + h))
        im = ImageEnhance.Brightness(im).enhance(1 - 0.5 * ease(local / 0.4)).convert('RGBA')
        hl = te.strong(te.headline(sg['lines'], 96, (247, 201, 168), 22))
        br, tx = hl
        x = (RW - br.width) // 2
        wv = ease((local - 0.1) / 0.45)
        if wv > 0:
            im.alpha_composite(br.crop((0, 0, max(1, int(br.width * wv)), br.height)), (x, 330))
            im.alpha_composite(with_alpha(tx, min(1, wv * 2)), (x, 330))
        when = text_sprite(sg['when'], te.HAND, 92, WHITE + (255,), 6, (30, 30, 50, 255))
        k = ease((local - 0.6) / 0.3)
        if k > 0:
            im.alpha_composite(with_alpha(when, k), ((RW - when.width) // 2, int(640 + (1 - k) * 20)))
        k2 = ease((local - 1.0) / 0.3)
        if k2 > 0:
            im.alpha_composite(with_alpha(handle, k2), ((RW - handle.width) // 2, 1500))
        return im

    # ---------- áudio ----------
    parts, fc, labels = [], '', []
    idx = 0
    for st, d, sg in segs:
        if 'clip' in sg:
            parts += ['-i', D + sg['clip']]
            fc += (f'[{idx}:a]atrim={sg["t0"]}:{sg["t1"]},asetpts=PTS-STARTPTS,aresample=48000,'
                   f'aformat=channel_layouts=stereo,volume={sg.get("db", 0)}dB,afade=t=in:d=0.03,'
                   f'afade=t=out:st={d - 0.05}:d=0.05[s{idx}];')
        else:
            parts += ['-f', 'lavfi', '-t', str(d), '-i', 'anullsrc=r=48000:cl=stereo']
            fc += f'[{idx}:a]anull[s{idx}];'
        labels.append(f'[s{idx}]')
        idx += 1
    fc += ''.join(labels) + f'concat=n={len(labels)}:v=0:a=1[dia];'
    nlabels = []
    for j, (t0, key) in enumerate(narr_events):
        parts += ['-i', narr[key][0]]
        fc += (f'[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={cfg.get("narr_db", 9)}dB,'
               f'adelay={int(t0 * 1000)}|{int(t0 * 1000)},apad=whole_dur={DUR}[n{j}];')
        nlabels.append(f'[n{j}]')
        idx += 1
    if nlabels:
        fc += ''.join(nlabels) + f'amix=inputs={len(nlabels)}:normalize=0[nar];'
        fc += '[dia][nar]amix=inputs=2:normalize=0,asplit=2[voz][sc];'
    else:
        fc += '[dia]asplit=2[voz][sc];'
    parts += ['-ss', str(cfg.get('music_start', 0)), '-i', cfg['music']]
    fo = DUR - 1.3
    fc += (f'[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=PTS-STARTPTS,'
           f'volume={cfg.get("music_db", -16)}dB,afade=t=in:d=0.3,afade=t=out:st={fo}:d=1.3[mus];'
           '[mus][sc]sidechaincompress=threshold=0.02:ratio=5:attack=25:release=400:makeup=1[duck];'
           '[voz][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
    wav = OUT + name + '.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *parts, '-filter_complex', fc, '-map', '[out]',
                    '-ar', '48000', '-t', str(DUR), wav], check=True)

    # ---------- vídeo ----------
    video = OUT + name + '-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    snaps = []
    last = None
    for st, d, sg in segs:
        n = round(d * FPS)
        if 'clip' in sg:
            got = 0
            for fr in te.frames(D + sg['clip'], sg['t0'], sg['t1']):
                if got >= n:
                    break
                tt = st + got / FPS
                out = overlay(fr, tt).convert('RGB')
                enc.stdin.write(out.tobytes())
                if got == n // 2:
                    snaps.append(out)
                last, got = fr, got + 1
            while got < n:
                enc.stdin.write(overlay(last, st + got / FPS).convert('RGB').tobytes())
                got += 1
        elif 'freeze' in sg:
            base = grab_frame(D + sg['freeze'], sg['at'])
            for i in range(n):
                out = overlay(freeze_img(base, i / FPS, d), st + i / FPS, True).convert('RGB')
                enc.stdin.write(out.tobytes())
                if i == n // 2:
                    snaps.append(out)
            last = base
        else:
            base = last
            for i in range(n):
                out = overlay(card_img(base, i / FPS, d, sg), st + i / FPS).convert('RGB')
                enc.stdin.write(out.tobytes())
                if i == n - 8:
                    snaps.append(out)
    enc.stdin.close()
    enc.wait()
    final = OUT + name + '.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-c:v', 'libx264', '-crf', '22',
                    '-maxrate', '4500k', '-bufsize', '10M', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                    '-b:a', '192k', '-shortest', '-movflags', '+faststart', final], check=True)
    ims = [x.resize((216, 384)) for x in snaps]
    cols = min(6, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 222 + 6, rows * 390 + 6), 'white')
    for i, x in enumerate(ims):
        sheet.paste(x, (6 + (i % cols) * 222, 6 + (i // cols) * 390))
    sheet.save(S + name + '-contato.jpg', quality=85)
    print(final, round(DUR, 2))


if __name__ == '__main__':
    run(json.load(open(sys.argv[1])))
