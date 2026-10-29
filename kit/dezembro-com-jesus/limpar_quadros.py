"""Tira a moldura branca + linha preta que veio "assada" em alguns lados dos quadros.

Cada lado: anda da borda pra dentro; aceita uma faixa branca e depois uma linha
escura curta (até 5 px). Se achou moldura, corta até o fim dela + 6 px (pra
sumir o canto arredondado). Se o lado já começa no desenho, não corta.
"""
import glob, json, os, sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)


def classe(vals):
    w = sum(v > 238 for v in vals) / len(vals)
    d = sum(v < 70 for v in vals) / len(vals)
    return 'W' if w > 0.85 else ('D' if d > 0.85 else '.')


def corte(im, lado):
    w, h = im.size
    px = im.load()
    perfil = ''
    for d in range(0, 26):
        if lado == 'L': vals = [px[d, y] for y in range(h // 5, 4 * h // 5, 4)]
        if lado == 'R': vals = [px[w - 1 - d, y] for y in range(h // 5, 4 * h // 5, 4)]
        if lado == 'T': vals = [px[x, d] for x in range(w // 5, 4 * w // 5, 4)]
        if lado == 'B': vals = [px[x, h - 1 - d] for x in range(w // 5, 4 * w // 5, 4)]
        perfil += classe(vals)
    i = 0
    while i < len(perfil) and perfil[i] == 'W':
        i += 1
    brancos = i
    k = 0
    while k < 3 and i < len(perfil) and perfil[i] == '.' and 'D' in perfil[i + 1:i + 3]:
        i += 1  # pixel de transição (antialias)
        k += 1
    j = i
    while j < len(perfil) and perfil[j] == 'D':
        j += 1
    escuros = j - i
    if escuros and escuros <= 5:
        return j + 6, perfil
    if brancos:
        return brancos + 6, perfil
    return 0, perfil


rel = {}
for f in sorted(glob.glob(os.path.join(src, '*.jpg'))):
    im = Image.open(f).convert('RGB')
    g = im.convert('L')
    c = {l: corte(g, l)[0] for l in 'LRTB'}
    w, h = im.size
    out = im.crop((c['L'], c['T'], w - c['R'], h - c['B']))
    nome = os.path.basename(f)
    out.save(os.path.join(dst, nome), quality=92)
    rel[nome] = {'corte': c, 'tamanho': out.size}

json.dump(rel, open(os.path.join(dst, '_cortes.json'), 'w'), indent=1)
print(len(rel), 'quadros limpos')
