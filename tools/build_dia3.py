import os
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
from PIL import Image, ImageDraw, ImageFont
from compose import (slide_cena, headline, body, footer, fit_cover, top_fade, W, H, HAND, BODY,
                     ACCENT, INK, PAPER)

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
C = S + 'zip-cenas/Bento_Ep1_Cena_0%d.png'
OUT = S + 'dia3/'
os.makedirs(OUT, exist_ok=True)
T = 5
c6 = Image.open(C % 6).convert('RGB')
paper = c6.getpixel((20, 20))


def pill(d, text, cx, y, fill, color=INK, size=40):
    f = ImageFont.truetype(BODY.replace('SemiBold', 'ExtraBold'), size)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((cx - tw / 2 - 26, y, cx + tw / 2 + 26, y + size + 26), radius=(size + 26) // 2,
                        fill=fill)
    d.text((cx - tw / 2, y + 10), text, font=f, fill=color)


# 1. capa dividida
sem = fit_cover(Image.open(C % 7).convert('RGB'), W // 2, H, 0.0)
com = fit_cover(Image.open(C % 8).convert('RGB'), W // 2, H, 0.0)
im = Image.new('RGBA', (W, H))
im.paste(sem, (0, 0))
im.paste(com, (W // 2, 0))
top_fade(im, 470)
d = ImageDraw.Draw(im)
d.line((W // 2, 330, W // 2, H), fill=(255, 250, 242), width=8)
y = headline(im, ['A mesma manhã.'], 80, size=96)
d = ImageDraw.Draw(im)
pill(d, 'Sem rotina', W // 4, y + 30, (240, 196, 180))
pill(d, 'Com rotina', 3 * W // 4, y + 30, (205, 228, 196))
bottom = Image.new('RGBA', (W, 150), PAPER + (0,))
g = Image.new('L', (1, 150))
for yy in range(150):
    g.putpixel((0, yy), int(200 * (yy / 150) ** 1.6))
bottom.putalpha(g.resize((W, 150)))
im.alpha_composite(bottom, (0, H - 150))
footer(ImageDraw.Draw(im), 1, T)
im.convert('RGB').save(OUT + 'dia3-01.jpg', quality=92)

# 2 e 3. cada lado
slide_cena(C % 7, OUT + 'dia3-02.jpg', ['Sem rotina'],
           sub='07:05. Uma meia só, mochila aberta no chão, torrada voando. Ninguém sabe o que vem depois.',
           page=2, total=T, anchor_y=0.0, title_size=92, fade=500)
slide_cena(C % 8, OUT + 'dia3-03.jpg', ['Com rotina'],
           sub='06:55. Roupa vestida, mochila pronta, café sem pressa. Ele sabe o próximo passo.',
           page=3, total=T, anchor_y=0.0, title_size=92, fade=500)

# 4. o que mudou
im = Image.new('RGBA', (W, H), paper + (255,))
y = headline(im, ['O que mudou?', 'Só a ordem.'], 90, size=82, highlight=1)
y = body(im, 'A Academia Americana de Pediatria indica 3 coisas que diminuem a briga da manhã:', y + 20,
         size=40)
d = ImageDraw.Draw(im)
fnum = ImageFont.truetype(HAND, 78)
itens = ['Deixar tudo pronto na noite anterior.', 'Acordar com bom humor.',
         'Dar escolhas simples: "essa camiseta ou aquela?"']
fb = ImageFont.truetype(BODY, 42)
y += 24
for i, t in enumerate(itens, 1):
    d.text((110, y - 14), str(i), font=fnum, fill=ACCENT)
    yy = y
    from compose import wrap
    for ln in wrap(d, t, fb, 800):
        d.text((180, yy), ln, font=fb, fill=INK)
        yy += 54
    y = yy + 26
b = c6.crop((120, 300, 1000, 1360))
s_ = (H - 110 - y) / b.height
s_ = min(s_, 0.42)
b = b.resize((round(b.width * s_), round(b.height * s_)), Image.LANCZOS)
im.paste(b, ((W - b.width) // 2, H - 110 - b.height))
footer(ImageDraw.Draw(im), 4, T)
im.convert('RGB').save(OUT + 'dia3-04.jpg', quality=92)

# 5. pedido de envio
im = Image.new('RGBA', (W, H), paper + (255,))
y = headline(im, ['Manda pra mãe que vive a manhã corrida.'], 100, size=76)
d = ImageDraw.Draw(im)
f = ImageFont.truetype(HAND, 72)
t = 'Amanhã tem mais Bento!'
d.text(((W - d.textlength(t, font=f)) / 2, y + 6), t, font=f, fill=ACCENT)
b = c6.crop((120, 300, 1000, 1360))
b = b.resize((round(b.width * 0.78), round(b.height * 0.78)), Image.LANCZOS)
im.paste(b, ((W - b.width) // 2 + 20, H - 120 - b.height))
footer(ImageDraw.Draw(im), 5, T)
im.convert('RGB').save(OUT + 'dia3-05.jpg', quality=92)

ims = [Image.open(OUT + 'dia3-0%d.jpg' % i).resize((360, 450)) for i in range(1, 6)]
sheet = Image.new('RGB', (370 * 5 + 10, 470), 'white')
for i, x in enumerate(ims):
    sheet.paste(x, (10 + i * 370, 10))
sheet.save(S + 'dia3-contato.jpg', quality=85)
print('ok')
