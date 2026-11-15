import json, re, unicodedata
OFF = 0.15  # silêncio antes da primeira palavra
Y, C, R, G, P = '#ffd24a', '#4fd0ff', '#ff5a68', '#3dffa0', '#ff8ec4'
RAW = [
    ('*"Autismo* *leve* *não* *dá* *BPC."*', R, ['ce']),
    ('Ouviu isso no *INSS?* É a desculpa *número* *um.*', Y, ['um']),
    ('Desde *2012,* autista é *pessoa* *com* *deficiência* por lei. E *não* *existe* *grau* *mínimo.*', G, ['minimo']),
    ('Desculpa dois: *"a* *renda* *passou* *do* *limite."*', C, ['limite']),
    ('Mas o BPC de outro filho, ou a aposentadoria de até *1* *salário* de um idoso da casa, *não* *entra* *na* *conta.*', G, ['conta']),
    ('E o STF já decidiu: esse limite *não* *é* *absoluto.*', G, ['absoluto']),
    ('Desculpa três: *"negado,* *não* *tem* *o* *que* *fazer."*', C, ['fazer']),
    ('Tem sim. São *30* *dias* pra recorrer na *Junta* *de* *Recursos,* pelo *Meu* *INSS* ou no *135.*', G, ['cinco']),
    ('E o que quase ninguém sabe: o *CadÚnico* vence a cada *2* *anos.*', Y, ['anos']),
    ('Cadastro vencido *bloqueia* *o* *benefício.* Atualiza no *CRAS.*', Y, ['cras']),
    ('Se o atendente insistir... *mostra* *esse* *vídeo.*', P, ['video']),
    ('Comenta a desculpa que te deram. A mais absurda *vira* *vídeo.*', Y, ['video']),
]
GROUPS = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 9], [10, 10], [11, 11]]

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))

W = [w for w in json.load(open('voz/words.json'))['words'] if w.get('type', 'word') == 'word' and not w['text'].startswith('[') and not w['text'].endswith(']')]
cur, lines = 0, []
for txt, color, ends in RAW:
    j = cur
    while norm(W[j]['text']) not in ends: j += 1
    seg = W[cur:j + 1]; cur = j + 1
    # tempo por caractere ao longo das palavras faladas
    marks = []; tot = 0
    for w in seg:
        n = max(1, len(norm(w['text']))); marks.append((tot, w['start'], tot + n, min(w['end'], w['start'] + 0.12 * n + .1))); tot += n
    def at(frac):
        c = frac * tot
        for c0, s, c1, e in marks:
            if c <= c1: return s + (e - s) * (c - c0) / (c1 - c0)
        return marks[-1][3]
    disp = txt.split(' '); dn = [max(1, len(norm(d))) for d in disp]; dt = sum(dn); acc = 0; words = []
    for d, n in zip(disp, dn):
        k = d.startswith('*') and d.endswith('*'); d = d.strip('*')
        words.append([d, color if k else None, round(at(acc / dt) + OFF, 3)]); acc += n
    lines.append({'t0': round(seg[0]['start'] + OFF, 3), 'a1': round(marks[-1][3] + OFF, 3), 'words': words, 'color': color})
DUR = round((lines[-1]['a1'] + 3.0) * 30) / 30
for i, L in enumerate(lines): L['t1'] = lines[i + 1]['t0'] if i + 1 < len(lines) else DUR
shots = []
for i, (a, b) in enumerate(GROUPS):
    t0 = 0 if i == 0 else round((lines[a]['t0'] - .1) * 30) / 30
    shots.append({'a': a, 'b': b, 't0': t0})
for i, s in enumerate(shots): s['t1'] = shots[i + 1]['t0'] if i + 1 < len(shots) else DUR
open('timing.js', 'w').write('export const LINES=%s;\nexport const SHOTS=%s;\nexport const DUR=%s;\nexport const OFF=%s;\n' % (json.dumps(lines, ensure_ascii=False), json.dumps(shots), DUR, OFF))
for i, L in enumerate(lines): print(i, L['t0'], L['a1'], ' '.join(w[0] for w in L['words']))
print('shots', [(s['t0'], round(s['t1'] - s['t0'], 2)) for s in shots], 'DUR', DUR)
