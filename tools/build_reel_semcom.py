"""Reel 'sem rotina x com rotina' com as cenas 7 e 8, texto e caixinha de música."""
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_reel as br

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
C = S + 'zip-cenas/Bento_Ep1_Cena_0%d.png'
OUT = S + 'reel/'
RW, RH, FPS, TOP = br.RW, br.RH, br.FPS, br.TOP
DUR = 18.5
br.SRC = {i: Image.open(C % i).convert('RGB') for i in (7, 8)}


def split_frame():
    im = Image.new('RGB', (RW, RH))
    for k, x in ((7, 0), (8, RW // 2)):
        s = br.SRC[k]
        sc = RH / s.height
        w = round(s.width * sc)
        r = s.resize((w, RH), Image.LANCZOS)
        cx = int(0.45 * w)
        r = r.crop((cx - RW // 4, 0, cx + RW // 4, RH))
        im.paste(r, (x, 0))
    ImageDraw.Draw(im).line((RW // 2, 700, RW // 2, RH), fill=(255, 250, 242), width=8)
    return im


SPLIT = split_frame()
br.SEGS = [
    ('split', 0.0, 3.4, 1.0, 1.0, 0.5, 0.5, 0.5),
    (7, 3.4, 7.6, 1.00, 1.10, 0.45, 0.45, 0.55),
    (8, 7.6, 11.8, 1.10, 1.00, 0.45, 0.45, 0.55),
    ('papel', 11.8, 16.0, 1.0, 1.0, 0.5, 0.5, 0.5),
    ('split', 16.0, DUR, 1.0, 1.0, 0.5, 0.5, 0.5),
]
br.TEXTS = [
    (0.0, 3.4, br.txt_head(['A mesma manhã.'], TOP, 104)),
    (0.6, 3.4, br.txt_hand('sem rotina  ×  com rotina', TOP + 140, 84)),
    (3.55, 7.6, br.txt_head(['Sem rotina'], TOP, 104)),
    (4.3, 7.6, br.txt_body('07:05. Meia perdida, mochila aberta, torrada voando.', TOP + 140, 50)),
    (7.75, 11.8, br.txt_head(['Com rotina'], TOP, 104)),
    (8.5, 11.8, br.txt_body('06:55. Roupa vestida, mochila pronta, café sem pressa.', TOP + 140, 50)),
    (11.95, 16.0, br.txt_head(['O que mudou?', 'Só a ordem.'], TOP + 20, 92)),
    (12.9, 16.0, br.txt_body('Deixar tudo pronto na noite anterior, acordar com bom humor e dar escolhas '
                             'simples.', TOP + 250, 44)),
    (13.8, 16.0, br.txt_body('Academia Americana de Pediatria', TOP + 470, 34)),
    (16.15, DUR, br.txt_head(['Manda pra mãe que vive', 'a manhã corrida.'], TOP, 88)),
]

_orig_scene = br.scene_frame


def scene_frame(seg, t):
    if seg[0] == 'split':
        return SPLIT.copy()
    return _orig_scene(seg, t)


br.scene_frame = scene_frame

if __name__ == '__main__':
    br.DUR = DUR
    wav = OUT + 'musica-semcom.wav'
    br.musica(wav)
    video = OUT + 'reel-semcom-sem-audio.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                          '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)):
        p.stdin.write(br.frame_at(fi / FPS).tobytes())
    p.stdin.close()
    p.wait()
    final = OUT + 'reel-sem-com-rotina.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-af',
                    'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
                    '-shortest', '-movflags', '+faststart', final], check=True)
    ims = [br.frame_at(t).resize((270, 480)) for t in (0.2, 1.5, 5.5, 9.5, 14.5, 17.5)]
    sheet = Image.new('RGB', (280 * len(ims) + 10, 500), 'white')
    for i, x in enumerate(ims):
        sheet.paste(x, (10 + i * 280, 10))
    sheet.save(S + 'semcom-contato.jpg', quality=85)
    print('ok', final)
