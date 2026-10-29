"""Confere o texto do PDF contra o dados.json, noite por noite."""
import json, re, subprocess, sys
pdf = sys.argv[1]
D = json.load(open('entrada/dados.json', encoding='utf-8'))
norm = lambda s: re.sub(r'\s+', ' ', s.replace('­', '')).strip().lower()
def pagina(i):
    return norm(subprocess.run(['pdftotext', '-raw', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout)
ok_noites, falhas = 0, []
for n in D['noites']:
    pq, pp = 5 + 2 * (n['n'] - 1), 6 + 2 * (n['n'] - 1)
    tq, tp = pagina(pq), pagina(pp)
    campos = [('tema', tq, n['tema']), ('leitura', tq, n['leitura']), ('verso', tq, n['verso']), ('versiculo', tq, n['versiculo']),
              ('mensagem', tq, n['mensagem']), ('conversa', tq, n['conversa']),
              ('guardar', tp, n['guardar']), ('desafio', tp, n['desafio']), ('oracao', tp, n['oracao']),
              ('lembra', tp, n['lembra']), ('resposta', tp, n['resposta'])]
    for q in n['quadros']:
        if q['narra']:
            campos.append((f'narra q{q["q"]}', tq, q['narra']))
        for quem, fala in q['baloes']:
            campos.append((f'fala q{q["q"]} {quem}', tq, fala))
    erros = [c for c, t, v in campos if norm(v) not in t]
    if erros:
        falhas.append((n['n'], erros))
    else:
        ok_noites += 1
f = D['final']; tf = pagina(55)
extra = [x for x in [f['titulo'], f['sub'], f['versiculo_conferir'], f['oracao']] + [p for passo in f['passos'] for p in passo] if norm(x) not in tf]
print(f'noites: {ok_noites}/25')
for n, e in falhas: print('  noite', n, e)
print('página final:', 'ok' if not extra else extra)
