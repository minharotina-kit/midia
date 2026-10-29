import sys
from PIL import Image, ImageDraw, ImageFont
fs = sys.argv[2:]; out = sys.argv[1]
ims = [Image.open(f).convert('RGB') for f in fs]
W = sum(i.size[0] for i in ims) + 12 * len(ims); H = max(i.size[1] for i in ims)
c = Image.new('RGB', (W, H), 'white'); x0 = 0
fnt = ImageFont.truetype('/home/user/midia/fonts/ttf/Fredoka-Bold.ttf', 13)
for im in ims:
    d = ImageDraw.Draw(im)
    for g in range(0, max(im.size), 50):
        col = (255, 0, 0) if g % 100 == 0 else (255, 150, 150)
        d.line([(g, 0), (g, im.size[1])], fill=col, width=1)
        d.line([(0, g), (im.size[0], g)], fill=col, width=1)
        if g % 100 == 0:
            d.text((g + 2, 2), str(g), fill=(255, 255, 0), font=fnt, stroke_width=2, stroke_fill=(0,0,0))
            d.text((2, g + 2), str(g), fill=(255, 255, 0), font=fnt, stroke_width=2, stroke_fill=(0,0,0))
    c.paste(im, (x0, 0)); x0 += im.size[0] + 12
c.save(out, quality=85)
