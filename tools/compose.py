"""Monta slides do @minharotina.kit: imagem da cena + texto por cima.

Uso como módulo: from compose import slide_cena, slide_texto
"""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/fonts/ttf/'
TITLE = FONTS + 'Fredoka-Bold.ttf'
BODY = FONTS + 'Nunito-SemiBold.ttf'
HAND = FONTS + 'Caveat-Bold.ttf'

INK = (74, 44, 26)          # marrom escuro
ACCENT = (178, 74, 38)      # terracota
PAPER = (251, 241, 228)     # creme
HIGHLIGHTS = [(247, 201, 168), (252, 226, 160), (214, 230, 200), (205, 223, 240)]
W, H = 1080, 1350


def fit_cover(img, w, h, anchor_y=0.5):
    """Recorta e redimensiona a imagem para preencher w x h."""
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = round((img.height - h) * anchor_y)
    return img.crop((x, y, x + w, y + h))


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def brush(im, box, color, seed=0):
    """Mancha de pincel suave atrás do texto."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(7):
        jx, jy = rnd.randint(-10, 10), rnd.randint(-6, 6)
        d.rounded_rectangle((x0 + jx, y0 + jy + i, x1 + jx, y1 + jy - i), radius=26,
                            fill=color + (120,))
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    im.alpha_composite(layer)


def top_fade(im, height, color=PAPER, strength=235):
    grad = Image.new('L', (1, height))
    for y in range(height):
        grad.putpixel((0, y), int(strength * (1 - y / height) ** 1.4))
    mask = grad.resize((im.width, height))
    layer = Image.new('RGBA', (im.width, height), color + (0,))
    layer.putalpha(mask)
    im.alpha_composite(layer, (0, 0))


def footer(d, page, total):
    f = ImageFont.truetype(BODY, 30)
    d.text((64, H - 78), '@minharotina.kit', font=f, fill=INK)
    t = f'{page}/{total}'
    d.text((W - 64 - d.textlength(t, font=f), H - 78), t, font=f, fill=INK)


def headline(im, lines, y, size=88, highlight=0, max_w=940):
    """Título em linhas, cada linha com mancha de pincel atrás."""
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(TITLE, size)
    out = []
    for text in lines:
        for ln in wrap(d, text, f, max_w):
            out.append(ln)
    for i, ln in enumerate(out):
        tw = d.textlength(ln, font=f)
        x = (W - tw) / 2
        brush(im, (x - 26, y + 12, x + tw + 26, y + size + 14),
              HIGHLIGHTS[(highlight + i) % len(HIGHLIGHTS)], seed=i + y)
        d = ImageDraw.Draw(im)
        d.text((x, y), ln, font=f, fill=INK)
        y += int(size * 1.12)
    return y


def body(im, text, y, size=40, color=INK, max_w=900, font=BODY, align='center'):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(font, size)
    for ln in wrap(d, text, f, max_w):
        tw = d.textlength(ln, font=f)
        x = (W - tw) / 2 if align == 'center' else (W - max_w) / 2
        d.text((x, y), ln, font=f, fill=color)
        y += int(size * 1.3)
    return y


def slide_cena(src, out, title, sub=None, tag=None, page=1, total=7, anchor_y=0.35,
               fade=430, hand=None, title_size=88):
    im = fit_cover(Image.open(src).convert('RGB'), W, H, anchor_y).convert('RGBA')
    top_fade(im, fade)
    y = 70
    d = ImageDraw.Draw(im)
    if tag:
        f = ImageFont.truetype(BODY, 30)
        tw = d.textlength(tag, font=f)
        d.rounded_rectangle(((W - tw) / 2 - 24, y, (W + tw) / 2 + 24, y + 54), radius=27,
                            fill=PAPER, outline=(226, 184, 146), width=3)
        d.text(((W - tw) / 2, y + 9), tag, font=f, fill=ACCENT)
        y += 84
    y = headline(im, title if isinstance(title, list) else [title], y, size=title_size)
    if sub:
        y = body(im, sub, y + 6, size=40)
    if hand:
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(HAND, 70)
        for ln in wrap(d, hand, f, 860):
            tw = d.textlength(ln, font=f)
            d.text(((W - tw) / 2, y + 4), ln, font=f, fill=ACCENT)
            y += 74
    bottom = Image.new('RGBA', (W, 150), PAPER + (0,))
    g = Image.new('L', (1, 150))
    for yy in range(150):
        g.putpixel((0, yy), int(200 * (yy / 150) ** 1.6))
    bottom.putalpha(g.resize((W, 150)))
    im.alpha_composite(bottom, (0, H - 150))
    footer(ImageDraw.Draw(im), page, total)
    im.convert('RGB').save(out, quality=92)


def slide_texto(bento_src, out, title, paragraphs, page, total, hand=None, fonte=None,
                bento_box=(330, 820, 750, 1240)):
    """Slide de texto em papel creme com o Bento pequeno embaixo."""
    im = Image.new('RGBA', (W, H), PAPER + (255,))
    y = headline(im, title if isinstance(title, list) else [title], 110, size=78, highlight=1)
    for p in paragraphs:
        y = body(im, p, y + 18, size=40)
    if fonte:
        y = body(im, fonte, y + 10, size=30, color=ACCENT)
    if hand:
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(HAND, 74)
        tw = d.textlength(hand, font=f)
        d.text(((W - tw) / 2, y + 10), hand, font=f, fill=ACCENT)
    if bento_src:
        b = Image.open(bento_src).convert('RGB')
        bx0, by0, bx1, by1 = bento_box
        b = fit_cover(b, bx1 - bx0, by1 - by0, 0.5)
        mask = Image.new('L', b.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, b.width, b.height), fill=255)
        im.paste(b, (bx0, by0), mask)
    footer(ImageDraw.Draw(im), page, total)
    im.convert('RGB').save(out, quality=92)
