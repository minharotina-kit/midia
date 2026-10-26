"""Curto das 12h (POV) feito com clipes da Família Tatu. Uso: python3 build_pov_tatu.py <config.json>

config: {"name": ..., "clips": [[arquivo, t0, t1, texto_topo, legenda_ou_null, [l0, l1]], ...],
         "card": ["linha 1", "linha 2"], "music": arquivo.wav, "end": 2.2}
"""
import json
import subprocess
import sys

from PIL import Image, ImageEnhance

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_tatu_ep1 as te
from build_reel_info import ease, text_sprite, with_alpha

S, G, OUT = te.S, te.G, te.OUT
RW, RH, FPS = te.RW, te.RH, te.FPS
WHITE, NAVY, CORAL = te.WHITE, te.NAVY, te.CORAL


def top_text(lines):
    hl = te.strong(te.headline(lines, 92, (252, 226, 160), 31))
    return hl


def run(cfg):
    clips = cfg['clips']
    END = cfg.get('end', 2.2)
    starts, t = [], 0.0
    for c in clips:
        starts.append(t)
        t += c[2] - c[1]
    CARD0 = t
    DUR = CARD0 + END
    tops = [top_text(c[3]) for c in clips]
    caps = [(te.pill(c[4], NAVY) if c[4] else None) for c in clips]
    card_h = te.strong(te.headline(cfg['card'], 96, (247, 201, 168), 22))
    card_f = text_sprite('@paisdarotina', te.BODYB, 44, WHITE + (255,), 4, (30, 30, 50, 255))

    def overlay(im, k, local):
        im = im.convert('RGBA')
        br, tx = tops[k]
        x = (RW - br.width) // 2
        w = ease((local + 0.1) / 0.4)
        im.alpha_composite(br.crop((0, 0, max(1, int(br.width * w)), br.height)), (x, 290))
        im.alpha_composite(with_alpha(tx, min(1, w * 1.5)), (x, 290))
        if caps[k] is not None:
            l0, l1 = clips[k][5]
            if l0 <= local < l1:
                a = min(ease((local - l0) / 0.12), ease((l1 - local) / 0.12))
                sp = caps[k]
                im.alpha_composite(with_alpha(sp, a), ((RW - sp.width) // 2, 1330))
        return im

    def card(last, local):
        z = 1.0 + 0.05 * (local / END)
        w, h = RW / z, RH / z
        im = last.resize((RW, RH), Image.BICUBIC, box=((RW - w) / 2, (RH - h) * 0.4, (RW + w) / 2, (RH - h) * 0.4 + h))
        im = ImageEnhance.Brightness(im).enhance(1 - 0.5 * ease(local / 0.35)).convert('RGBA')
        br, tx = card_h
        x = (RW - br.width) // 2
        wv = ease((local - 0.05) / 0.4)
        if wv > 0:
            im.alpha_composite(br.crop((0, 0, max(1, int(br.width * wv)), br.height)), (x, 520))
            im.alpha_composite(with_alpha(tx, min(1, wv * 2)), (x, 520))
        k = ease((local - 0.5) / 0.3)
        if k > 0:
            im.alpha_composite(with_alpha(card_f, k), ((RW - card_f.width) // 2, 1380))
        return im

    # áudio: falas dos clipes + música baixa que abaixa quando alguém fala
    name = cfg['name']
    voice = OUT + name + '-voz.wav'
    parts, fc, labels = [], '', []
    for i, c in enumerate(clips):
        parts += ['-i', G + c[0]]
        fc += (f'[{i}:a]atrim={c[1]}:{c[2]},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,'
               f'afade=t=in:d=0.04,afade=t=out:st={c[2] - c[1] - 0.06}:d=0.06[a{i}];')
        labels.append(f'[a{i}]')
    fc += ''.join(labels) + f'concat=n={len(labels)}:v=0:a=1,apad=pad_dur={END + 1}[out]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *parts, '-filter_complex', fc, '-map', '[out]',
                    '-t', str(DUR), '-ar', '48000', voice], check=True)
    wav = OUT + name + '.wav'
    fo = DUR - 1.2
    fc2 = (f'[0:a]volume=4dB,asplit=2[voc][sc];'
           f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=PTS-STARTPTS,volume=-12dB,'
           f'afade=t=in:d=0.2,afade=t=out:st={fo}:d=1.2[mus];'
           '[mus][sc]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=400:makeup=1[duck];'
           '[voc][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', voice, '-i', cfg['music'], '-filter_complex', fc2,
                    '-map', '[out]', '-ar', '48000', '-t', str(DUR), wav], check=True)

    video = OUT + name + '-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                            '-crf', '20', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    snaps, last = [], None
    for k, (c, st) in enumerate(zip(clips, starts)):
        need = round((c[2] - c[1]) * FPS)
        got = 0
        for fr in te.frames(G + c[0], c[1], c[2]):
            if got >= need:
                break
            out = overlay(fr, k, got / FPS).convert('RGB')
            enc.stdin.write(out.tobytes())
            if got == int(need * 0.6):
                snaps.append(out)
            last, got = fr, got + 1
        while got < need:
            enc.stdin.write(overlay(last, k, got / FPS).convert('RGB').tobytes())
            got += 1
    for i in range(round(END * FPS)):
        out = card(last, i / FPS).convert('RGB')
        enc.stdin.write(out.tobytes())
        if i == round(END * FPS) - 5:
            snaps.append(out)
    enc.stdin.close()
    enc.wait()
    final = OUT + name + '.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-c:v', 'libx264', '-crf', '21',
                    '-maxrate', '5M', '-bufsize', '10M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', final], check=True)
    ims = [x.resize((270, 480)) for x in snaps]
    sheet = Image.new('RGB', (280 * len(ims) + 10, 500), 'white')
    for i, x in enumerate(ims):
        sheet.paste(x, (10 + i * 280, 10))
    sheet.save(S + name + '-contato.jpg', quality=85)
    print(final, round(DUR, 2))


if __name__ == '__main__':
    run(json.load(open(sys.argv[1])))
