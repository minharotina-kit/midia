import json, re, subprocess, numpy as np
SR = 48000
js = open('timing.js').read()
LINES = json.loads(re.search(r'LINES=(.*?);\n', js).group(1)); SHOTS = json.loads(re.search(r'SHOTS=(.*?);\n', js).group(1)); DUR = float(re.search(r'DUR=([\d.]+)', js).group(1))
wt = lambda l, i: LINES[l]['words'][min(i, len(LINES[l]['words']) - 1)][2]
S = lambda k: SHOTS[k]['t0']
N = int((DUR + .5) * SR); bed = np.zeros(N); fx = np.zeros(N)
rs = np.random.RandomState(3)
def put(buf, t, x, g=1.0):
    i = int(t * SR); j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
def env(n, a=.005, d=.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def tone(f, dur, d=.2, a=.004):
    n = int(dur * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(np.broadcast_to(f, (n,)) if np.ndim(f) == 0 else f) / SR
    return np.sin(ph) * env(n, a, d)
def noise(dur, d=.1): n = int(dur * SR); return rs.randn(n) * env(n, .002, d)
def lp(x, k):  # média móvel simples
    return np.convolve(x, np.ones(k) / k, mode='same')
def cat(*xs):
    o = np.zeros(max(len(x) for x in xs))
    for x in xs: o[:len(x)] += x
    return o
def whoosh(dur=.35):
    n = int(dur * SR); x = rs.randn(n); t = np.linspace(0, 1, n)
    y = lp(x, 6) - lp(x, 40); return y * np.sin(np.pi * t) ** 2 * .9
def thud(): return cat(tone(np.linspace(140, 45, int(.35 * SR)), .35, .12) * 1.2, lp(noise(.08, .02), 4) * .5)
def clink(f=2400): return cat(tone(f, .25, .08) * .5, tone(f * 1.5, .2, .05) * .25)
def popp(f=700): return tone(np.linspace(f, f * 1.8, int(.09 * SR)), .09, .05) * .6
def ding(f): return cat(tone(f, 1.2, .5), .4 * tone(f * 2, 1.0, .3)) * .5
# ----- trilha (pulso 100 bpm) até o meme -----
bpm = 100; beat = 60 / bpm; tend = S(9) - .05
notes = [55, 55, 65.4, 49]  # lá, lá, dó, sol (graves)
b = 0
while b * beat < tend:
    t0 = b * beat
    put(bed, t0, tone(np.linspace(110, 48, int(.25 * SR)), .25, .09), .9)      # bumbo
    put(bed, t0 + beat / 2, lp(noise(.06, .015), 2) - lp(noise(.06, .015), 30), .18)  # chimbal
    if b % 2 == 1: put(bed, t0, lp(noise(.18, .06), 3), .22)                   # caixa leve
    f = notes[(b // 4) % 4]; put(bed, t0, cat(tone(f, beat * .9, .35, .01), .3 * tone(f * 2, beat * .9, .25)), .55)
    if b % 4 == 0:
        for m in (2, 2.52, 3):  # acorde suave
            put(bed, t0, tone(f * m * 2, beat * 3.8, 1.2, .08), .07)
    b += 1
bed[int(tend * SR):] *= np.exp(-np.arange(N - int(tend * SR)) / SR / .15)
# ----- efeitos -----
for k in range(1, len(SHOTS)): put(fx, S(k) - .12, whoosh(), .35)
put(fx, 1.55, thud(), .9)                          # carimbo NEGADO
for t in [wt(1, 6)]: put(fx, t - .1, popp(500), .6)  # contador 1/3
put(fx, S(1) + .5, popp(600), .5); put(fx, S(1) + 1.3, popp(800), .5)
for i in range(3): put(fx, S(2) + .1 + i * .18, thud(), .35)          # blocos subindo
put(fx, S(2) + 1.0, tone(np.linspace(300, 900, int(.3 * SR)), .3, .15), .3)  # pulo
for i in range(3): put(fx, wt(2, 11) + i * .15, popp(900 + i * 200), .55)
put(fx, wt(2, 12), thud(), .7)
for i in range(10): put(fx, S(3) + .15 + i * .175, clink(2200 + i * 90), .45)  # moedas
put(fx, S(3) + .05, popp(500), .5)
put(fx, wt(4, 18), whoosh(.6), .5); put(fx, wt(4, 18) + .7, clink(1800), .5)
put(fx, wt(4, 19), thud(), .7)
hit = wt(5, 3) + .05; put(fx, hit, thud(), 1.4); put(fx, hit, lp(noise(.05, .01), 2), .8)  # martelo
put(fx, wt(5, 7), thud(), .7)
put(fx, S(6) + .05, popp(500), .5)
put(fx, S(7) + .05, thud(), .7)
for j in range(11): put(fx, S(7) + .2 + j * .42, lp(noise(.05, .012), 5), .35)  # passos
put(fx, S(7) + 4.5, tone(np.linspace(220, 160, int(.5 * SR)), .5, .2), .15)        # porta
for w in [(7, 3), (7, 12), (7, 15), (8, 9)]: put(fx, wt(*w), popp(750), .5)
put(fx, wt(9, 2) - .05, thud(), .9); put(fx, wt(9, 2), clink(1200), .4)              # cadeado
for i in range(5): put(fx, wt(9, 5) + i * .14, popp(600 + i * 120), .5)              # CRAS montando
put(fx, wt(9, 7), thud(), .6)
# meme: gota, assobio descendo, óculos, confete
put(fx, S(9) + .5, popp(1200), .3)
sw = int(.6 * SR); put(fx, wt(10, 6) - .05, tone(np.geomspace(1400, 260, sw), .6, 2.0, .02) * np.linspace(1, .6, sw), .35)
put(fx, wt(10, 5) + .15, clink(3000), .5)
put(fx, wt(10, 6) + .12, cat(noise(.4, .15) * .3, tone(np.linspace(500, 1500, int(.35 * SR)), .35, .25) * .5), .6)
# CTA: ding-dong da senha + festa
put(fx, S(10) + .45, ding(988), .6); put(fx, S(10) + .75, ding(784), .6)
put(fx, S(10) + 1.6, cat(noise(.4, .15) * .3, tone(np.linspace(500, 1500, int(.35 * SR)), .35, .25) * .5), .6)
for i, c in enumerate('Me disseram que autismo'): put(fx, S(10) + 2.1 + i * .095, lp(noise(.02, .005), 2), .12)
def wav(name, x):
    x = (x / max(1e-9, np.abs(x).max()) * .7).astype(np.float32)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', name], input=x.tobytes(), check=True)
wav('out/bed.wav', bed); wav('out/fx.wav', fx)
open('out/meme_t.txt', 'w').write(f'{S(9) - .05:.3f} {DUR:.3f}')
print('ok', S(9), DUR)
