import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
from PIL import Image, ImageDraw, ImageFont
from compose import (slide_cena, headline, body, footer, fit_cover, W, H, HAND, ACCENT, INK)

S = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/'
C = S + 'zip-cenas/Bento_Ep1_Cena_0%d.png'
OUT = S + 'ep1/'
import os
os.makedirs(OUT, exist_ok=True)
T = 7

slide_cena(C % 1, OUT + 'ep1-01.jpg', ['06:50.', 'Ainda de pijama?'], tag='A Rotina do Bento · ep. 1',
           page=1, total=T, anchor_y=0.0, title_size=96)
slide_cena(C % 2, OUT + 'ep1-02.jpg', ['Sem saber o que vem depois...'],
           hand='o Bento vira bolinha e sai rolando!', page=2, total=T, anchor_y=0.25, title_size=80)
slide_cena(C % 3, OUT + 'ep1-03.jpg', ['A manhã dele tem', '3 passos.'],
           sub='Sempre os mesmos. Sempre na mesma ordem.', page=3, total=T, anchor_y=0.0, title_size=80)
slide_cena(C % 4, OUT + 'ep1-04.jpg', ['1. Abrir a janela', '2. Lavar o rosto', '3. Vestir a roupa'],
           hand='A cada passo: Desenrolei!', page=4, total=T, anchor_y=0.12, title_size=76, fade=470)
slide_cena(C % 5, OUT + 'ep1-05.jpg', ['07:09. Deu tempo!'],
           sub='A van buzinou e o Bento já estava na porta. Bi-bi!', page=5, total=T, anchor_y=0.0,
           title_size=90)

# fundo de papel com a cor da cena 6
c6 = Image.open(C % 6).convert('RGB')
paper = c6.getpixel((20, 20))


def base():
    return Image.new('RGBA', (W, H), paper + (255,))


# slide 6: por que funciona + os 3 desenhos da parede (cena 3)
im = base()
y = headline(im, ['Por que funciona?'], 100, size=82, highlight=1)
y = body(im, 'A Academia Americana de Pediatria diz que crianças se saem melhor com rotinas '
             'regulares, previsíveis e consistentes.', y + 20, size=42)
y = body(im, 'Quando a ordem é sempre a mesma, a criança sabe o que vem depois.', y + 16, size=42)
c3 = Image.open(C % 3).convert('RGB')
crop = c3.crop((120, 260, 1024, 1330))          # Bento olhando os 3 desenhos
box_h = H - 130 - (y + 40)
s_ = box_h / crop.height
crop = crop.resize((round(crop.width * s_), box_h), Image.LANCZOS)
mask = Image.new('L', crop.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, crop.width, crop.height), radius=40, fill=255)
im.paste(crop, ((W - crop.width) // 2, y + 40), mask)
footer(ImageDraw.Draw(im), 6, T)
im.convert('RGB').save(OUT + 'ep1-06.jpg', quality=92)

# slide 7: pedido + Bento acenando
im = base()
y = headline(im, ['Salva pra mostrar pro seu filho amanhã de manhã.'], 100, size=74, highlight=0)
b = c6.crop((120, 300, 1000, 1360))
b = b.resize((round(b.width * 0.78), round(b.height * 0.78)), Image.LANCZOS)
im.paste(b, ((W - b.width) // 2 + 20, H - 120 - b.height))
d = ImageDraw.Draw(im)
f = ImageFont.truetype(HAND, 72)
t = 'Amanhã tem mais Bento!'
d.text(((W - d.textlength(t, font=f)) / 2, y + 6), t, font=f, fill=ACCENT)
footer(ImageDraw.Draw(im), 7, T)
im.convert('RGB').save(OUT + 'ep1-07.jpg', quality=92)

# foto do perfil (quadrada)
p = c6.crop((150, 280, 1000, 1130)).resize((1080, 1080), Image.LANCZOS)
p.save(OUT + 'foto-perfil-bento.jpg', quality=92)

# folha de contato
ims = [Image.open(OUT + 'ep1-0%d.jpg' % i).resize((360, 450)) for i in range(1, 8)]
sheet = Image.new('RGB', (360 * 4 + 50, 450 * 2 + 30), 'white')
for i, x in enumerate(ims):
    sheet.paste(x, (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save(S + 'ep1-contato.jpg', quality=85)
print('ok')
