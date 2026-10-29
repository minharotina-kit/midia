"""Gera o HTML do kit Dezembro com Jesus a partir do dados.json.

uso: python3 -I gerar.py previa   -> build/previa.html (dia 1 em A e B, pintar 1, Por que Jesus veio?)
"""
import html, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(AQUI, 'entrada', 'dados.json'), encoding='utf-8'))
POS = json.load(open(os.path.join(AQUI, 'posicoes.json'), encoding='utf-8'))
CORTES = json.load(open(os.path.join(AQUI, 'limpos', '_cortes.json'), encoding='utf-8'))
MARCA = 'Dezembro com Jesus · @paisdarotina'
PINTAR_DIR = 'entrada/'
ARA = D['credito_biblico']

def e(s):
    # palavra com hífen (chamá-lo, mostrem-se) não quebra no meio
    return re.sub(r'(\w+(?:-\w+)+)', r'<span class="nw">\1</span>', html.escape(s, quote=True))


def ico(nome, cor='currentColor'):
    p = {
        'livro': '<path d="M4 5.5C4 4.7 4.7 4 5.5 4H11v15H5.5C4.7 19 4 18.3 4 17.5z"/><path d="M20 5.5c0-.8-.7-1.5-1.5-1.5H13v15h5.5c.8 0 1.5-.7 1.5-1.5z"/>',
        'luz': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.6.5 1 1.2 1 2V16h5.2v-.2c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z"/>',
        'balao': '<path d="M4 5h16v10H9l-4 4v-4H4z"/>',
        'estrela': '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8L3.5 9.7l5.9-.8z"/>',
        'coracao': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
        'lapis': '<path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/>',
        'presente': '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M3 9h18v3H3zM12 9v11"/><path d="M12 9c-2-4-6-4-6-1.5S10 9 12 9zM12 9c2-4 6-4 6-1.5S14 9 12 9z"/>',
        'coracao-partido': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/><path d="M12 7.4l-1.6 3.6 2.6 2-1.8 3.6"/>',
        'estrela-belem': '<path d="M12 2.5l1.9 7.6 7.6 1.9-7.6 1.9-1.9 7.6-1.9-7.6-7.6-1.9 7.6-1.9z"/>',
        'calendario': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4M8 14h2M14 14h2M8 17h2"/>',
        'casa': '<path d="M3.5 11L12 4l8.5 7"/><path d="M5.5 9.5V20h13V9.5"/><path d="M10 20v-5h4v5"/>',
        'tesoura': '<circle cx="6" cy="7" r="2.6"/><circle cx="6" cy="17" r="2.6"/><path d="M8.2 8.4L20 17M8.2 15.6L20 7"/>',
        'cruz-sol': '<path d="M2.5 20.5h19"/><path d="M6 20.5a6 6 0 0 1 12 0"/><path d="M12 2.5v13M8 6.5h8"/><path d="M3.2 14.6l1.6.9M20.8 14.6l-1.6.9M7.2 10.6l.9 1.4M16.8 10.6l-.9 1.4"/>',
    }[nome]
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{cor}" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round">{p}</svg>')


def rodape(esq=None):
    esq = esq if esq is not None else f'<span>{e(ARA)}</span>'
    return f'<footer class="rodape">{esq}<span class="marca">{e(MARCA)}</span></footer>'


def topo_dia(n, titulo, direita):
    if n['bonus']:
        selo = '<div class="selo ouro">25</div>'
        kicker = f'<div class="kicker ouro">Bônus · {e(n["data"])}</div>'
    else:
        selo = f'<div class="selo">{n["n"]}</div>'
        kicker = f'<div class="kicker">Dia {n["n"]} · {e(n["data"])}</div>'
    return (f'<header class="topo">{selo}<div class="topo-txt">{kicker}<h1>{e(titulo)}</h1></div>'
            f'{direita}</header>')


def quadro(q, pos):
    nome = os.path.basename(q['arquivo'])
    k = nome[:-4]
    p = pos.get(k, {})
    c = CORTES[nome]['corte']
    narra = ''
    if q.get('narra'):
        nl = p.get('narra', {})
        narra = (f'<div class="narra {nl.get("lado", "esq")}" style="max-width:{nl.get("w", 0.7) * 100:.0f}%">'
                 f'{e(q["narra"])}</div>')
    bals = []
    for i, (quem, fala) in enumerate(q.get('baloes', [])):
        bp = (p.get('baloes') or [{}] * 9)[i] if i < len(p.get('baloes', [])) else {}
        attrs = []
        for a in ('x', 'xr', 'xc', 'y', 'w', 'dy', 'lado'):
            if a in bp:
                attrs.append(f'data-{a}="{bp[a]}"')
        if bp.get('sob') or not any(a in bp for a in ('y',)):
            attrs.append('data-sob="1"')
        if not any(a in bp for a in ('x', 'xr', 'xc')):
            attrs.append('data-x="0.05"')
        if 't' in bp:
            attrs.append(f'data-tx="{bp["t"][0]}" data-ty="{bp["t"][1]}"')
        quem_html = f'<span class="quem">{e(quem)}</span>' if bp.get('nome') else ''
        bals.append(f'<div class="bal" data-quem="{e(quem)}" {" ".join(attrs)}>{quem_html}{e(fala)}</div>')
    return (f'<div class="pn" data-k="{k}" data-ox="{p.get("ox", 0.5)}" data-oy="{p.get("oy", 0.5)}">'
            f'<div class="art"><img src="limpos/{nome}" alt="">{narra}</div>{"".join(bals)}</div>')


def pagina_quadrinho(n, lay):
    pos = POS[lay]
    ler = f'<div class="pill">{ico("livro")}Ler na Bíblia: <b>{e(n["leitura"])}</b></div>'
    gibi_style = ''
    if lay == 'A' and pos.get('_linhas'):
        r1, r2 = pos['_linhas']
        gibi_style = f' style="grid-template-rows:{r1}mm {r2}mm"'
    gibi = f'<div class="gibi"{gibi_style}>' + ''.join(quadro(q, pos) for q in n['quadros']) + '</div>'
    palavra = (f'<div class="card palavra"><div class="card-t">Palavra de Deus · <b>{e(n["verso"])}</b></div>'
               f'<p>“{e(n["versiculo"])}”</p></div>')
    ensina = (f'<div class="card ensina"><div class="card-t">{ico("luz")}O que Deus nos ensina hoje</div>'
              f'<p>{e(n["mensagem"])}</p></div>')
    conversa = (f'<div class="card conversa"><div class="card-t">{ico("balao")}Pra conversar</div>'
                f'<p>{e(n["conversa"])}</p></div>')
    if lay == 'A':
        textos = f'<div class="textos">{palavra}{ensina}{conversa}</div>'
    else:
        faixa = (f'<div class="card conversa faixa"><div class="card-t">{ico("balao")}Pra conversar</div>'
                 f'<p>{e(n["conversa"])}</p><div class="linhas-t">Se quiser, escrevam aqui o que a família respondeu:</div>'
                 f'<div class="linhas"></div></div>')
        textos = f'<div class="textos">{palavra}{ensina}</div>{faixa}'
    return (f'<section class="page lay{lay}" data-pg="quadrinho-{n["n"]:02d}-{lay}">'
            f'{topo_dia(n, n["tema"], ler)}<div class="corpo">{gibi}{textos}</div>{rodape()}</section>')


def pagina_pintar(n):
    pill = f'<div class="pill">{ico("lapis")}Para a criança</div>'
    if n['bonus']:
        topo = (f'<header class="topo"><div class="selo ouro">25</div><div class="topo-txt">'
                f'<div class="kicker ouro">Bônus · {e(n["data"])}</div><h1>Hora de pintar!</h1></div>{pill}</header>')
    else:
        topo = (f'<header class="topo"><div class="selo">{n["n"]}</div><div class="topo-txt">'
                f'<div class="kicker">Noite {n["n"]} · {e(n["data"])}</div><h1>Hora de pintar!</h1></div>{pill}</header>')
    bloco = (f'<div class="bloco">{ico("luz", "#8a6510")}<div><div class="t">Para guardar no coração</div>'
             f'<div class="frase">{e(n["guardar"])}</div>'
             f'<div class="ler">Para ler na Bíblia com a família: {e(n["leitura"])}</div></div></div>')
    desenho = f'<div class="desenho"><img src="{PINTAR_DIR}{n["desenho_pintar"]}" alt=""></div>'
    tres = (f'<div class="tres">'
            f'<div class="card c-desafio"><div class="card-t">{ico("estrela")}Desafio do dia</div><p>{e(n["desafio"])}</p></div>'
            f'<div class="card c-orar"><div class="card-t">{ico("coracao")}Vamos orar</div><p>{e(n["oracao"])}</p></div>'
            f'<div class="card c-lembra"><div class="card-t">{ico("luz")}Você lembra?</div><p>{e(n["lembra"])}</p>'
            f'<div class="resp">Resposta: {e(n["resposta"])}</div></div></div>')
    casinha = 'a estrela' if n['bonus'] else f'a casinha {n["n"]}'
    esq = f'<span class="check"><i></i>Pintei {casinha} no calendário</span>'
    return (f'<section class="page pintar" data-pg="pintar-{n["n"]:02d}">{topo}{bloco}{desenho}{tres}'
            f'{rodape(esq)}</section>')


def pagina_final():
    f = D['final']
    icos = [('coracao', '#c8463d', '#fbe9e6'), ('coracao-partido', '#585d76', '#eceaf0'),
            ('estrela-belem', '#8a6510', '#fcf2d8'), ('cruz-sol', '#2e6b4f', '#e6f2eb'),
            ('presente', '#3d5a8c', '#e7eefa')]
    passos = ''.join(
        f'<li class="passo"><div class="ico" style="background:{bg}"><span class="n">{i + 1}</span>{ico(nm, cor)}</div>'
        f'<div><h3>{e(t)}</h3><p>{e(txt)} <span class="ref">({e(ref)})</span></p></div></li>'
        for i, ((t, txt, ref), (nm, cor, bg)) in enumerate(zip(f['passos'], icos)))
    fotos = ('<div class="fotos"><div class="art"><img src="limpos/noite-24-q4.jpg" style="object-position:50% 62%" alt=""></div>'
             '<div class="art"><img src="limpos/noite-17-q4.jpg" style="object-position:50% 40%" alt=""></div></div>')
    jo = (f'<div class="card palavra jo316"><div class="card-t">Palavra de Deus · <b>{e(f["versiculo_ref"])}</b></div>'
          f'<p>“{e(f["versiculo_conferir"])}”</p></div>')
    seguir = (f'<div class="seguir"><div class="card-t">{ico("coracao")}{e(f["oracao_titulo"])}</div>'
              f'<p>{e(f["oracao"])}</p></div>')
    return (f'<section class="page final creme" data-pg="por-que-jesus-veio">'
            f'<div class="cab"><div class="kicker">{e(f["sub"])}</div><h1>{e(f["titulo"])}</h1></div>'
            f'{fotos}<ol class="passos">{passos}</ol>{jo}{seguir}{rodape()}</section>')


def documento(paginas, titulo):
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>{e(titulo)}</title><link rel="stylesheet" href="build/estilo.css"></head><body>'
            + ''.join(paginas) + '<script src="build/baloes.js"></script></body></html>')


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'previa'
    n1 = D['noites'][0]
    if modo == 'previa':
        pgs = [pagina_quadrinho(n1, 'A'), pagina_quadrinho(n1, 'B'), pagina_pintar(n1), pagina_final()]
        open(os.path.join(AQUI, 'previa.html'), 'w', encoding='utf-8').write(documento(pgs, 'Prévia · Dezembro com Jesus'))
        print('previa.html ok')
