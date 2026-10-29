"""Monta o kit completo (opção A) em kit.html.

uso: python3 -I kit.py
- recorta cada quadro na janela que aparece (final/quadros) pra o PDF ficar leve;
- posições: pos_a.py (noites 2 a 25) e posicoes.json["A"] (noite 1).
"""
import json, os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar as G
from gerar import D, e, ico, rodape

AQUI = G.AQUI
exec(open(os.path.join(AQUI, 'pos_a.py'), encoding='utf-8').read())  # define P e LINHAS
POS1 = G.POS['A']
LARG = (186 - 2.8) / 2          # largura do quadro (mm)
BORDA = 1.2                     # 2 × 0,6 mm de moldura
OUT = os.path.join(AQUI, 'final', 'quadros')
os.makedirs(OUT, exist_ok=True)

CAPA_NOVA = 'entrada/capa-nova.png'   # quando chegar, é só pôr o arquivo aqui e rodar de novo
CAPA = CAPA_NOVA if os.path.exists(os.path.join(AQUI, CAPA_NOVA)) else 'entrada/capa.jpg'
DPI_MIN = 200                          # a moldura nunca fica maior que a imagem aguenta a 200 dpi


def capa_src():
    if CAPA != CAPA_NOVA:
        return CAPA
    dst = os.path.join(AQUI, 'final', 'capa-nova.jpg')  # JPG 92 no PDF: o PNG pesaria o dobro
    Image.open(os.path.join(AQUI, CAPA)).convert('RGB').save(dst, quality=92, optimize=True)
    return 'final/capa-nova.jpg'


def moldura_capa():
    if CAPA != CAPA_NOVA:
        return ''  # capa provisória: tamanho aprovado (104 × 156 mm)
    w, h = Image.open(os.path.join(AQUI, CAPA)).size
    larg = min(w / DPI_MIN * 25.4, 122.0, 178.0 * w / h)  # 178 mm é a altura que cabe na capa
    return f' style="width:{larg:.1f}mm;height:{larg * h / w:.1f}mm"'


def versiculo(txt):
    return txt[0].upper() + txt[1:] if txt[:1].islower() else txt


SOBRA = json.load(open(os.path.join(AQUI, 'sobra.json'))) if os.path.exists(os.path.join(AQUI, 'sobra.json')) else {}


def linhas(nn):
    base = tuple(POS1['_linhas']) if nn == '01' else LINHAS.get(nn, (77.6, 77.6))
    extra = max(0, SOBRA.get(nn, 0) - 3) / 2  # enche a página: o que sobrou no pé vai pros quadros
    return (round(base[0] + extra, 1), round(base[1] + extra, 1))


def spec(nn, q):
    """Converte a posição do quadro pra um formato só: y0 em px, balões com y em fração da janela."""
    nome = f'noite-{nn}-q{q}.jpg'
    w, h = G.CORTES[nome]['tamanho']
    alt = linhas(nn)[0 if q <= 2 else 1]
    vis = min(h, round(w * (alt - BORDA) / (LARG - BORDA)))
    if nn == '01':
        p = POS1[f'noite-01-q{q}']
        y0 = round(p.get('oy', .5) * (h - vis))
        narra = p.get('narra', {})
        n = (narra.get('lado', 'esq'), narra.get('w', .7))
        bs = [dict(b) for b in p.get('baloes', [])]
    else:
        p = P[nn][q - 1]
        y0 = p['y0']
        n = p.get('n', ('esq', .7))
        bs = [dict(b) for b in p.get('b', [])]
    y0 = max(0, min(y0, h - vis))
    for b in bs:
        if 'by' in b:
            b['y'] = round((b.pop('by') - y0) / vis, 4)
        if 't' in b:
            b['t'] = (b['t'][0], b['t'][1] - y0)
    return nome, w, h, y0, vis, n, bs


def quadro(nn, qd):
    nome, w, h, y0, vis, (lado, larg), bs = spec(nn, qd['q'])
    dst = os.path.join(OUT, nome)
    Image.open(os.path.join(AQUI, 'limpos', nome)).crop((0, y0, w, y0 + vis)).save(dst, quality=85, optimize=True)
    narra = ''
    if qd.get('narra'):
        narra = f'<div class="narra {lado}" style="max-width:{larg * 100:.0f}%">{e(qd["narra"])}</div>'
    bals = []
    for i, (quem, fala) in enumerate(qd.get('baloes', [])):
        bp = bs[i] if i < len(bs) else {}
        attrs = [f'data-{a}="{bp[a]}"' for a in ('x', 'xr', 'xc', 'y', 'w', 'dy', 'lado') if a in bp]
        if bp.get('sob') or 'y' not in bp:
            attrs.append('data-sob="1"')
        if not any(a in bp for a in ('x', 'xr', 'xc')):
            attrs.append('data-x="0.05"')
        if 't' in bp:
            attrs.append(f'data-tx="{bp["t"][0]}" data-ty="{bp["t"][1]}"')
        bals.append(f'<div class="bal" data-quem="{e(quem)}" {" ".join(attrs)}>{e(fala)}</div>')
    return (f'<div class="pn" data-k="{nome[:-4]}" data-ox="0.5" data-oy="0.5">'
            f'<div class="art"><img src="final/quadros/{nome}" alt="">{narra}</div>{"".join(bals)}</div>')


def pagina_quadrinho(n):
    nn = f'{n["n"]:02d}'
    r1, r2 = linhas(nn)
    ler = f'<div class="pill">{ico("livro")}Ler na Bíblia: <b>{e(n["leitura"])}</b></div>'
    gibi = (f'<div class="gibi" style="grid-template-rows:{r1}mm {r2}mm;height:{r1 + r2 + 2.8:.1f}mm">'
            + ''.join(quadro(nn, q) for q in n['quadros']) + '</div>')
    palavra = (f'<div class="card palavra"><div class="card-t">Palavra de Deus · <b>{e(n["verso"])}</b></div>'
               f'<p>“{e(versiculo(n["versiculo"]))}”</p></div>')
    ensina = (f'<div class="card ensina"><div class="card-t">{ico("luz")}O que Deus nos ensina hoje</div>'
              f'<p>{e(n["mensagem"])}</p></div>')
    conversa = (f'<div class="card conversa"><div class="card-t">{ico("balao")}Pra conversar</div>'
                f'<p>{e(n["conversa"])}</p></div>')
    longo = ' titulo-longo' if len(n['tema']) + len(n['leitura']) > 44 else ''
    return (f'<section class="page layA{longo}" data-pg="quadrinho-{nn}">'
            f'{G.topo_dia(n, n["tema"], ler)}<div class="corpo">{gibi}<div class="textos">{palavra}{ensina}{conversa}</div></div>'
            f'{rodape()}</section>')


def faiscas(qtd, cor, semente):
    import random
    r = random.Random(semente)
    out = []
    while len(out) < qtd:
        x, y, s = r.uniform(2, 98), r.uniform(1, 99), r.uniform(1.6, 4.2)
        if 9 < x < 91 and 2 < y < 90:
            continue
        out.append(f'<svg class="faisca" style="left:{x:.1f}%;top:{y:.1f}%;width:{s:.1f}mm;height:{s:.1f}mm" viewBox="0 0 24 24">'
                   f'<path d="M12 0l2.4 9.6L24 12l-9.6 2.4L12 24l-2.4-9.6L0 12l9.6-2.4z" fill="{cor}"/></svg>')
    return ''.join(out)


def pagina_capa():
    selos = ''.join(f'<span class="selo-c">{ico(i, "#fcf2d8")}{e(t)}</span>' for i, t in (
        ('livro', '25 histórias em quadrinhos'), ('lapis', 'Páginas para pintar'), ('estrela-belem', 'Presépio de montar')))
    return (f'<section class="page capa" data-pg="capa"><div class="ceu">{faiscas(38, "#f3d98a", 7)}</div>'
            f'<h1>Dezembro<br><span>com Jesus</span></h1>'
            f'<p class="promessa">Ensine seu filho sobre Jesus em 24 noites</p>'
            f'<div class="moldura"{moldura_capa()}><img src="{capa_src()}" alt=""></div>'
            f'<div class="selos">{selos}</div>'
            f'<div class="marca-c">@paisdarotina</div></section>')


def pagina_como_usar():
    passos = [
        ('calendario', 'Imprima e cole o calendário', ' na geladeira, na altura dos olhos da criança.'),
        ('livro', 'Toda noite, leiam o quadrinho do dia juntos.', ' Quem ainda não lê acompanha pelos desenhos; quem já lê pode ler as falas.'),
        ('balao', 'Leia a Palavra de Deus e a mensagem', ', e façam a pergunta do “Pra conversar”.'),
        ('lapis', 'Hora de pintar:', ' façam o desafio, orem juntos, e a criança pinta o desenho e a casinha do dia.'),
        ('casa', 'Monte o presépio no caminho:', ' nas noites 12 e 13 vocês começam. Na noite 24, o menino Jesus chega na manjedoura.'),
    ]
    lis = ''.join(f'<li><div class="num">{i + 1}</div><div class="ic">{ico(ic, "#2e6b4f")}</div>'
                  f'<p><b>{e(t)}</b>{e(r)}</p></li>' for i, (ic, t, r) in enumerate(passos))
    precisa = ('<div class="card c-desafio"><div class="card-t">' + ico('estrela') + 'O que você vai precisar</div>'
               '<p>Impressora (ou uma gráfica rápida), lápis de cor ou giz de cera, tesoura sem ponta e cola. '
               'Papel mais grosso deixa o presépio firme.</p></div>')
    perdeu = ('<div class="card c-lembra"><div class="card-t">' + ico('coracao') + 'Perdeu uma noite?</div>'
              '<p>Tudo bem. Façam duas no dia seguinte, ou fiquem só com a história e a oração.</p></div>')
    return (f'<section class="page como creme" data-pg="como-usar">'
            f'<header class="cab-pg"><div class="kicker">Para os pais</div><h1>Como usar</h1>'
            f'<p class="lead">Dez minutinhos por noite, de 1 a 24 de dezembro. Sem pressa e sem precisar ser perfeito.</p></header>'
            f'<ol class="passos-uso">{lis}</ol><div class="duas">{precisa}{perdeu}</div>'
            f'<div class="tinta">{ico("celular", "#3d5a8c")}<p><b>Para economizar tinta:</b> os quadrinhos podem ser lidos no celular '
            f'ou no tablet. Imprima só as páginas de pintar, o calendário e o presépio.</p></div>'
            f'{rodape("<span></span>")}</section>')


def casinha(x, y, n, w=25):
    h = w * 1.05
    tel = h * .42
    corpo = h - tel
    num = (f'<text x="{x + w / 2:.2f}" y="{y + tel + corpo * .62:.2f}" text-anchor="middle" '
           f'font-family="Fredoka" font-weight="700" font-size="{w * .36:.2f}" fill="#2a2f4a">{n}</text>')
    porta_w = w * .2
    return (f'<g class="casa">'
            f'<path d="M{x - 1.2:.2f},{y + tel:.2f} L{x + w / 2:.2f},{y:.2f} L{x + w + 1.2:.2f},{y + tel:.2f} Z"/>'
            f'<rect x="{x:.2f}" y="{y + tel:.2f}" width="{w:.2f}" height="{corpo:.2f}" rx="1"/>'
            f'<rect x="{x + w * .72:.2f}" y="{y + tel - tel * .62:.2f}" width="{w * .1:.2f}" height="{tel * .45:.2f}" class="chamine"/>'
            f'<path d="M{x + w * .5 - porta_w / 2:.2f},{y + h:.2f} v-{corpo * .3:.2f} a{porta_w / 2:.2f},{porta_w / 2:.2f} 0 0 1 {porta_w:.2f},0 v{corpo * .3:.2f}" class="porta"/>'
            f'{num}</g>')


def pagina_calendario():
    W, H = 186, 214
    cols, w = 6, 25
    gx = (W - cols * w) / (cols - 1)
    pts, casas = [], []
    for i in range(24):
        r, c = divmod(i, cols)
        if r % 2:
            c = cols - 1 - c
        x = c * (w + gx)
        y = 4 + r * 45
        casas.append(casinha(x, y, i + 1, w))
        pts.append((x + w / 2, y + w * 1.05 * .7))
    ex, ey = W / 2, 4 + 4 * 45 + 14
    pts.append((ex, ey))
    caminho = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    R, r = 17, 7.2
    import math
    est = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = R if k % 2 == 0 else r
        est.append(f'{ex + rr * math.cos(ang):.2f},{ey + rr * math.sin(ang):.2f}')
    estrela = (f'<polygon points="{" ".join(est)}" class="estrela"/>'
               f'<text x="{ex:.2f}" y="{ey + 3.4:.2f}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="9" fill="#8a6510">25</text>'
               f'<text x="{ex + 24:.2f}" y="{ey + 2:.2f}" font-family="Fredoka" font-weight="700" font-size="7.5" fill="#c8463d">Natal!</text>')
    svg = (f'<svg class="mapa" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">'
           f'<path d="{caminho}" class="trilha"/>{"".join(casas)}{estrela}</svg>')
    return (f'<section class="page calendario" data-pg="calendario">'
            f'<header class="cab-pg"><div class="kicker">Para colar na geladeira</div><h1>Meu caminho até o Natal</h1>'
            f'<p class="lead">Toda noite, pinte a casinha do dia. Na noite 25, pinte a estrela!</p></header>'
            f'<div class="familia">Família: <span></span></div>{svg}'
            f'{rodape("<span></span>")}</section>')


def pagina_personagens():
    l1 = [('Maria', 'mãe de Jesus', 8.5), ('José', 'marido de Maria', 22.8), ('Menino Jesus', 'o Filho de Deus', 39.7),
          ('Anjo Gabriel', 'mensageiro de Deus', 57.3), ('Isaías', 'o profeta', 76.2), ('Zacarias', 'pai de João', 91.4)]
    l2 = [('Isabel', 'mãe de João, parente de Maria', 8.5), ('Os magos', 'sábios do Oriente que seguiram a estrela', 40.4),
          ('Jesus', 'o Salvador, já adulto', 73.6), ('Pastorzinho', 'um dos pastores de Belém', 91.4)]
    def nomes(lst):
        return ''.join(f'<div class="nome" style="left:{x}%"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b, x in lst)
    return (f'<section class="page personagens creme" data-pg="personagens">'
            f'<header class="cab-pg"><div class="kicker">Quem aparece nas histórias</div><h1>Conheça os personagens</h1></header>'
            f'<div class="fileira"><div class="recorte" style="aspect-ratio:1536/490"><img src="entrada/personagens.jpg" style="top:0" alt=""></div>'
            f'<div class="nomes">{nomes(l1)}</div></div>'
            f'<div class="fileira"><div class="recorte" style="aspect-ratio:1536/534"><img src="entrada/personagens.jpg" style="top:-91.76%" alt=""></div>'
            f'<div class="nomes">{nomes(l2)}</div></div>'
            f'<div class="card ensina tambem"><div class="card-t">{ico("estrela")}Também aparecem nas histórias</div>'
            f'<p>O imperador César Augusto, o velho Simeão, Zaqueu, o bom samaritano, o pai e o filho que voltou para casa, '
            f'o menino dos cinco pães e dois peixinhos, e os dez homens que Jesus curou.</p></div>'
            f'{rodape("<span></span>")}</section>')


def pagina_presepio(i, titulo):
    return (f'<section class="page presepio" data-pg="presepio-{i}">'
            f'<header class="cab-pg esq"><div class="kicker">Presépio de montar · Folha {i} de 3</div><h1>{e(titulo)}</h1>'
            f'<p class="instr">{ico("lapis", "#8a6510")}Pinte, recorte na linha de fora e dobre a aba tracejada para a figura ficar em pé.</p></header>'
            f'<div class="folha"><img src="entrada/presepio/presepio-{i}.png" alt=""></div>'
            f'{rodape("<span></span>")}</section>')


def pagina_cartoes():
    est = ('<svg viewBox="0 0 24 24"><path d="M12 2.2l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.1l-5.9 3.1 1.2-6.5L2.5 9.1l6.6-.9z"/></svg>')
    def cartao(s):
        return (f'<div class="cartao"><div class="fn"><span class="e1">{est}</span>Feliz Natal!<span class="e2">{est}</span></div>'
                f'<div class="lin"><span>Para:</span><i></i></div>'
                f'<div class="lin"><span>Obrigado por</span><i></i></div><div class="lin"><i></i></div>'
                f'<div class="lin"><span>De:</span><i></i></div>'
                f'<div class="desenhe">Faça um desenho aqui</div></div>')
    return (f'<section class="page cartoes" data-pg="cartoes">'
            f'<header class="cab-pg"><div class="kicker">Para a noite 23</div><h1>Cartões de gratidão para pintar</h1>'
            f'<p class="lead">Pinte, recorte na linha tracejada e entregue para alguém.</p></header>'
            f'<div class="grade-c">{"".join(cartao(s) for s in (3, 11, 19, 27))}</div>'
            f'{rodape("<span></span>")}</section>')


def pagina_certificado():
    estrelas = ''.join(f'<div class="est"><svg viewBox="0 0 24 24"><path d="M12 2.2l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.1l-5.9 3.1 1.2-6.5L2.5 9.1l6.6-.9z"/></svg><span>{i}</span></div>'
                       for i in range(1, 26))
    return (f'<section class="page certificado" data-pg="certificado"><div class="moldura-c">'
            f'<div class="kicker">Certificado</div><h1>Nós completamos o<br>Dezembro com Jesus!</h1>'
            f'<p class="txt">Foram 24 noites de histórias, conversas e orações em família, esperando juntos o nascimento de Jesus.</p>'
            f'<div class="familia">Família: <span></span></div>'
            f'<div class="estrelas">{estrelas}</div><p class="pinte">Pinte uma estrelinha para cada noite que vocês fizeram.</p>'
            f'<div class="assina"><div><i></i><span>Pais</span></div><div><i></i><span>Criança</span></div></div>'
            f'<div class="natal">Natal de 2026</div></div>{rodape("<span></span>")}</section>')


def documento(paginas, titulo):
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>{e(titulo)}</title><link rel="stylesheet" href="build/estilo.css"></head><body>'
            + ''.join(paginas) + '<script src="build/baloes.js"></script></body></html>')


if __name__ == '__main__':
    os.makedirs(os.path.join(AQUI, 'final', 'pintar'), exist_ok=True)
    for n in D['noites']:
        dst = os.path.join(AQUI, 'final', n['desenho_pintar'])
        if not os.path.exists(dst):
            Image.open(os.path.join(AQUI, 'entrada', n['desenho_pintar'])).convert('L').save(dst, optimize=True)
    G.PINTAR_DIR = 'final/'
    pgs = [pagina_capa(), pagina_como_usar(), pagina_calendario(), pagina_personagens()]
    for n in D['noites']:
        pgs += [pagina_quadrinho(n), G.pagina_pintar(n)]
    pgs += [G.pagina_final(),
            pagina_presepio(1, 'A família de Jesus'), pagina_presepio(2, 'Os animais e o pastor'),
            pagina_presepio(3, 'Os magos e o estábulo'), pagina_cartoes(), pagina_certificado()]
    open(os.path.join(AQUI, 'kit.html'), 'w', encoding='utf-8').write(documento(pgs, 'Dezembro com Jesus'))
    print('kit.html:', len(pgs), 'páginas')
