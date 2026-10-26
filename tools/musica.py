"""Trilha original feita em código (sem direitos de terceiros). Cada semente/estilo dá uma música diferente.

Uso: python3 musica.py <estilo> <segundos> <semente> <saida.wav>
estilos: ninar (caixinha de música), ukulele (dia, alegre), piano (calmo), xilo (brincalhão)
"""
import sys

import numpy as np

SR = 44100
rng = None

MAJOR = [0, 2, 4, 5, 7, 9, 11]
PROGS = [[0, 5, 3, 4], [0, 3, 4, 0], [0, 4, 5, 3], [5, 3, 0, 4], [0, 3, 5, 4], [0, 5, 1, 4]]


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def chord(root_midi, degree):
    tri = [degree, degree + 2, degree + 4]
    out = []
    for d in tri:
        o, s = divmod(d, 7)
        out.append(root_midi + 12 * o + MAJOR[s])
    return out


def scale_note(root_midi, d):
    o, s = divmod(d, 7)
    return root_midi + 12 * o + MAJOR[s]


def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.2, length=None):
    t = np.arange(n) / SR
    e = np.ones(n)
    an, dn = int(a * SR), int(d * SR)
    e[:an] = np.linspace(0, 1, max(1, an))[:an]
    e[an:an + dn] = np.linspace(1, s, max(1, dn))[:len(e[an:an + dn])]
    e[an + dn:] = s
    rn = int(r * SR)
    if rn and rn < n:
        e[-rn:] *= np.linspace(1, 0, rn)
    return e


def pluck(f, dur, bright=0.5, damp=0.996):
    """Karplus-Strong: corda dedilhada (soa como ukulele/violão)."""
    n = int(dur * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    # suaviza o ataque pra ficar menos metálico
    for _ in range(int((1 - bright) * 4)):
        buf = 0.5 * (buf + np.roll(buf, 1))
    from scipy.signal import lfilter
    x = np.zeros(n)
    x[:p] = buf
    a = np.zeros(p + 2)
    a[0], a[p], a[p + 1] = 1, -0.5 * damp, -0.5 * damp
    out = lfilter([1.0], a, x)
    return out * np.minimum(1, np.linspace(30, 0, n)) * 0.9


def bell(f, dur, decay=2.2):
    """Caixinha de música / celesta."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)
         + 0.15 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 9))
    return s * np.exp(-t * decay) * np.minimum(1, t * 400)


def marimba(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 3.9 * f * t) * np.exp(-t * 25)
    return s * np.exp(-t * 7) * np.minimum(1, t * 600)


def epiano(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    mod = np.sin(2 * np.pi * f * t) * 1.2 * np.exp(-t * 3)
    s = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 1.6)
    return s * np.minimum(1, t * 300)


def bass(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 2 * f * t)
    return s * env_adsr(n, 0.01, 0.2, 0.5, 0.15)


def shaker(dur):
    n = int(dur * SR)
    s = rng.normal(0, 1, n)
    s = np.diff(s, prepend=0)  # agudo
    return s * np.exp(-np.arange(n) / SR * 40)


def kick(dur=0.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 110 * np.exp(-t * 18) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def reverb(x, size=1.6, mix=0.25):
    n = int(size * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * (5 / size))
    ir[0] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + n
    nfft = 1 << (L - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:len(x)]
    return (1 - mix) * x + mix * wet


def add(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[:j - i] * gain


def melody_line(root, prog, bars, beats_per_bar, rhythm):
    """Melodia simples: notas do acorde nos tempos fortes, passos na escala no meio."""
    notes = []
    cur = 7 + rng.integers(0, 3) * 2  # começa na oitava de cima
    for b in range(bars):
        deg = prog[b % len(prog)]
        chord_degs = [deg + 7, deg + 9, deg + 11]
        pattern = rhythm[b % len(rhythm)]
        for (pos, ln) in pattern:
            if pos == 0:
                cur = min(chord_degs, key=lambda d: abs(d - cur))
            else:
                cur += int(rng.choice([-1, 1, -1, 1, 2, -2, 0]))
                cur = int(np.clip(cur, 5, 14))
            notes.append((b * beats_per_bar + pos, ln, scale_note(root, cur)))
    return notes


def build(style, seconds, seed):
    global rng
    rng = np.random.default_rng(seed)
    root = 60 + int(rng.choice([0, 2, 5, 7, -3]))  # Dó, Ré, Fá, Sol, Lá
    prog = PROGS[int(rng.integers(0, len(PROGS)))]
    if style == 'ninar':
        bpm, bpb = int(rng.integers(66, 78)), 3
    elif style == 'ukulele':
        bpm, bpb = int(rng.integers(100, 118)), 4
    elif style == 'piano':
        bpm, bpb = int(rng.integers(76, 90)), 4
    else:
        bpm, bpb = int(rng.integers(108, 124)), 4
    beat = 60 / bpm
    bar = beat * bpb
    bars = int(np.ceil(seconds / bar)) + 1
    buf = np.zeros(int((bars * bar + 3) * SR))

    if bpb == 3:
        rhythm = [[(0, 1), (1, 1), (2, 1)], [(0, 2), (2, 1)], [(0, 1), (1, 1), (2, 1)], [(0, 3)]]
    else:
        rhythm = [[(0, 1), (1, 0.5), (1.5, 0.5), (2, 1), (3, 1)], [(0, 1.5), (1.5, 0.5), (2, 2)],
                  [(0, 0.5), (0.5, 0.5), (1, 1), (2, 1), (3, 1)], [(0, 3), (3, 1)]]
    # melodia entra só na 3ª volta pra deixar espaço pra voz no começo
    mel = melody_line(root + 12, prog, bars, bpb, rhythm)

    for b in range(bars):
        deg = prog[b % len(prog)]
        ch = chord(root - 12, deg)
        t0 = b * bar
        # baixo
        add(buf, bass(midi_hz(ch[0]), bar * 0.95), t0, 0.10)
        if style == 'ninar':
            for k in range(3):  # arpejo de caixinha
                add(buf, bell(midi_hz(ch[k % 3] + 12), 2.5, 2.8), t0 + k * beat, 0.16)
        elif style == 'ukulele':
            strum = [0, 1, 1.5, 2.5, 3]
            for s in strum:
                for i, m in enumerate(sorted(ch + [ch[0] + 12])):
                    add(buf, pluck(midi_hz(m + 12), beat * 1.6, 0.6), t0 + s * beat + i * 0.012, 0.14)
            for q in range(bpb * 2):
                add(buf, shaker(0.08), t0 + q * beat / 2, 0.02 if q % 2 else 0.035)
            add(buf, kick(), t0, 0.08)
            add(buf, kick(), t0 + 2 * beat, 0.06)
        elif style == 'piano':
            for k, m in enumerate(ch):
                add(buf, epiano(midi_hz(m + 12), bar * 1.1), t0 + k * 0.02, 0.13)
            add(buf, epiano(midi_hz(ch[1] + 24), beat * 1.5), t0 + 2.5 * beat, 0.07)
        else:  # xilo
            for q in range(bpb * 2):
                m = ch[[0, 1, 2, 1][q % 4]] + 12
                add(buf, marimba(midi_hz(m), 0.5), t0 + q * beat / 2, 0.13)
            add(buf, kick(), t0, 0.07)
            for q in range(bpb):
                add(buf, shaker(0.06), t0 + q * beat + beat / 2, 0.03)

    lead = {'ninar': lambda f, d: bell(f, d + 1.2, 2.0), 'ukulele': lambda f, d: pluck(f, d + 0.4, 0.8),
            'piano': lambda f, d: epiano(f, d + 0.6), 'xilo': lambda f, d: marimba(f, d + 0.3)}[style]
    lg = {'ninar': 0.2, 'ukulele': 0.2, 'piano': 0.16, 'xilo': 0.18}[style]
    for pos, ln, m in mel:
        if pos < bpb * 2:  # 2 primeiros compassos sem melodia
            continue
        add(buf, lead(midi_hz(m), ln * beat), pos * beat, lg)

    buf = reverb(buf, 2.2 if style in ('ninar', 'piano') else 1.2, 0.3 if style in ('ninar', 'piano') else 0.18)
    from scipy.signal import butter, sosfilt
    buf = sosfilt(butter(2, 90, 'highpass', fs=SR, output='sos'), buf)
    buf = buf[:int(seconds * SR)]
    fi, fo = int(0.3 * SR), int(1.5 * SR)
    buf[:fi] *= np.linspace(0, 1, fi)
    buf[-fo:] *= np.linspace(1, 0, fo)
    buf /= np.max(np.abs(buf)) + 1e-9
    buf *= 0.85
    info = dict(style=style, bpm=bpm, root=root, prog=prog, seed=seed)
    return buf, info


def save(path, x):
    import wave
    st = np.stack([x, np.roll(x, int(0.011 * SR)) * 0.96], 1)  # estéreo leve
    pcm = (np.clip(st, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == '__main__':
    style, secs, seed, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    x, info = build(style, secs, seed)
    save(out, x)
    print(out, info)
