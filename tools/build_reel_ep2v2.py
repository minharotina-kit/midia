"""Reel ep. 2 com narração + música de fundo, cortes encaixados na fala."""
import subprocess
import sys

from PIL import Image

sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_reel as br
import build_reel_anim as ba

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
U = '/root/.claude/uploads/5d8bda1a-7926-5607-9e1a-eeb000255e05/'
NARR = U + 'f3231c3e-ElevenLabs_2026-10-18T20_21_24_Nathalia_-_Calm__Friendly_pvc_sp100_s50_sb75_v4.mp3'
MUSIC = U + 'dfda338d-marlowemusic-bedtime-613384.mp3'
OUT = S + 'reel/'
RW, RH, FPS, TOP = br.RW, br.RH, br.FPS, br.TOP
DUR = 20.0

# (clipe, início no Reel, fim no Reel, velocidade)
TIMELINE = [
    (S + 'anim2/clip1.mp4', 0.0, 4.3, 1.0),
    (S + 'anim2/clip2.mp4', 4.3, 9.3, 1.0),
    (S + 'anim2/clip3.mp4', 9.3, 13.7, 1.0),
    (S + 'anim2/clip4.mp4', 13.7, DUR, 0.8),
]

ba.TEXTS = [
    (0.0, 4.3, br.txt_head(['20:30.'], TOP, 130)),
    (0.8, 4.3, br.txt_head(['Ainda pulando', 'na cama?'], TOP + 150, 92)),
    (4.4, 7.0, br.txt_head(['A noite dele tem', '3 passos.'], TOP, 92)),
    (7.0, 9.3, br.txt_head(['1. Escovar os dentes'], TOP, 88)),
    (8.1, 9.3, br.txt_hand('Desenrolei!', TOP + 120, 96)),
    (9.35, 13.7, br.txt_head(['2. Uma história'], TOP, 92)),
    (11.56, 13.7, br.txt_hand('os olhinhos já pesando...', TOP + 120, 84)),
    (13.75, DUR, br.txt_head(['3. Luz apagada.'], TOP, 92)),
    (15.85, DUR, br.txt_hand('Boa noite, Bento!', TOP + 120, 96)),
    (17.4, DUR, br.txt_head(['Mostra pro seu filho', 'antes de dormir.'], TOP + 240, 68)),
]


def frames(path, speed):
    vf = f'setpts=PTS/{speed},fps={FPS},scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH}'
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', path, '-vf', vf, '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = RW * RH * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield Image.frombytes('RGB', (RW, RH), b)
    p.wait()


def mix_audio(path):
    fc = (
        '[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=10dB,apad=pad_dur=4,atrim=0:20,'
        'asplit=2[voc][sc];'
        '[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:20,asetpts=PTS-STARTPTS,'
        'volume=-11dB,afade=t=in:d=0.4,afade=t=out:st=18.6:d=1.4[mus];'
        '[mus][sc]sidechaincompress=threshold=0.015:ratio=6:attack=30:release=450:makeup=1[duck];'
        '[voc][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]'
    )
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', NARR, '-i', MUSIC, '-filter_complex', fc,
                    '-map', '[out]', '-ar', '48000', '-t', str(DUR), path], check=True)


if __name__ == '__main__':
    wav = OUT + 'audio-ep2-narracao.wav'
    mix_audio(wav)
    video = OUT + 'reel-ep2v2-sem-audio.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                            '-s', f'{RW}x{RH}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset',
                            'medium', '-crf', '18', '-pix_fmt', 'yuv420p', video], stdin=subprocess.PIPE)
    total = 0
    for path, t0, t1, sp in TIMELINE:
        need = round((t1 - t0) * FPS)
        got, last = 0, None
        for fr in frames(path, sp):
            if got >= need:
                break
            enc.stdin.write(ba.compose(fr, t0 + got / FPS).tobytes())
            last, got = fr, got + 1
        while got < need:
            enc.stdin.write(ba.compose(last, t0 + got / FPS).tobytes())
            got += 1
        total += need
    enc.stdin.close()
    enc.wait()
    final = OUT + 'reel-ep2.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '192k', '-shortest', '-movflags', '+faststart', final], check=True)
    print('ok', final, total)
