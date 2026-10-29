# Posições da opção A, noite por noite. y0 = 1ª linha (px da imagem limpa) que aparece no quadro.
# n = (lado, largura) da narração. b = balões na ordem do dados.json:
#   x|xr|xc (fração), by = topo em px da imagem (ou sob=1: logo abaixo da narração), w = largura máx, t = ponta do rabinho (px)
P = {}
P['01'] = [
  dict(y0=None),  # dia 1 já calibrado em posicoes.json
]
P['02'] = [
  dict(y0=135, n=('esq', .7)),
  dict(y0=60, n=('esq', .55), b=[dict(x=.03, sob=1, w=.55, t=(298, 195))]),
  dict(y0=70, n=('esq', .7), b=[dict(x=.03, sob=1, w=.45, t=(172, 228))]),
  dict(y0=80, n=('esq', .7), b=[dict(xr=.97, sob=1, w=.48, t=(425, 318))]),
]
P['03'] = [
  dict(y0=120, n=('esq', .7)),
  dict(y0=100, n=('esq', .7), b=[dict(x=.03, sob=1, w=.5, t=(300, 225))]),
  dict(y0=100, b=[dict(x=.03, by=108, w=.55, t=(292, 230)), dict(x=.03, by=180, w=.42, t=(128, 250))]),
  dict(y0=110, n=('esq', .62), b=[dict(x=.03, sob=1, w=.55, t=(140, 280))]),
]
P['04'] = [
  dict(y0=150, n=('esq', .7)),
  dict(y0=150, b=[dict(x=.03, by=165, w=.48, t=(190, 298))]),
  dict(y0=90, n=('esq', .7), b=[dict(x=.03, sob=1, w=.45, t=(255, 250))]),
  dict(y0=100, n=('esq', .6), b=[dict(xr=.97, sob=1, w=.5, t=(305, 212))]),
]
P['05'] = [
  dict(y0=40, n=('esq', .7), b=[dict(xr=.97, sob=1, w=.45, t=(235, 172))]),
  dict(y0=110, b=[dict(x=.03, by=120, w=.55, t=(150, 236))]),
  dict(y0=160, n=('esq', 1.0), b=[dict(xr=.97, by=200, w=.45, t=(380, 248))]),
  dict(y0=130, n=('esq', .7)),
]
P['06'] = [
  dict(y0=100, n=('esq', .7), b=[dict(xr=.97, sob=1, w=.48, t=(300, 253))]),
  dict(y0=90, b=[dict(x=.03, by=100, w=.55, t=(110, 202)), dict(xr=.97, by=185, w=.38, t=(395, 272))]),
  dict(y0=100, n=('esq', .7)),
  dict(y0=100, n=('esq', .7), b=[dict(xr=.98, by=140, w=.4, t=(280, 222))]),
]
LINHAS = {}  # alturas das 2 linhas do gibi (mm) quando não for 77.6/77.6
LINHAS['07'] = (84, 71.2)
P['07'] = [
  dict(y0=115, n=('esq', .7)),
  dict(y0=118, n=('esq', .6), b=[dict(x=.03, sob=1, w=.45, t=(292, 200))]),
  dict(y0=168, b=[dict(x=.03, by=180, w=.42, t=(236, 255))]),
  dict(y0=140, n=('esq', .55), b=[dict(xr=.97, by=146, w=.42, t=(290, 228))]),
]
P['08'] = [
  dict(y0=110, n=('esq', .7)),
  dict(y0=150, n=('esq', .7), b=[dict(x=.1, sob=1, w=.5, t=(165, 282))]),
  dict(y0=80, b=[dict(xr=.97, by=118, w=.4, t=(345, 206))]),
  dict(y0=130, n=('esq', .55), b=[dict(xr=.97, by=136, w=.42, t=(215, 245))]),
]
P['09'] = [
  dict(y0=120, n=('esq', .7)),
  dict(y0=100, b=[dict(x=.03, by=105, w=.48, t=(250, 200))]),
  dict(y0=80, n=('esq', .7), b=[dict(x=.03, sob=1, w=.45, t=(232, 182))]),
  dict(y0=110, n=('esq', .7)),
]
P['10'] = [
  dict(y0=150, n=('esq', .7)),
  dict(y0=150, b=[dict(xr=.97, by=160, w=.55, t=(370, 272))]),
  dict(y0=170, n=('esq', .6), b=[dict(x=.03, sob=1, w=.52, t=(195, 302))]),
  dict(y0=120, b=[dict(x=.1, by=140, w=.45, t=(215, 298))]),
]
P['11'] = [
  dict(y0=90, n=('esq', .75)),
  dict(y0=60, b=[dict(xr=.97, by=70, w=.48, t=(420, 152))]),
  dict(y0=80, b=[dict(x=.03, by=100, w=.5, t=(235, 216))]),
  dict(y0=130, n=('esq', .7), b=[dict(xr=.97, sob=1, w=.5, t=(265, 290))]),
]
P['12'] = [
  dict(y0=100, n=('esq', .7)),
  dict(y0=60, b=[dict(x=.03, by=70, w=.5, t=(225, 166))]),
  dict(y0=60, n=('esq', .7), b=[dict(x=.03, sob=1, w=.42, t=(333, 185))]),
  dict(y0=110, n=('esq', .75)),
]
P['13'] = [
  dict(y0=110, n=('esq', .7)),
  dict(y0=130, n=('esq', .7)),
  dict(y0=110, b=[dict(x=.03, by=115, w=.5, t=(275, 206))]),
  dict(y0=100, n=('esq', .7)),
]
LINHAS['14'] = (82, 73.2)
P['14'] = [
  dict(y0=140, n=('esq', .7)),
  dict(y0=80, b=[dict(x=.03, by=262, w=.5, t=(330, 432))]),
  dict(y0=150, b=[dict(xr=.99, by=155, w=.38, t=(380, 226))]),
  dict(y0=50, n=('esq', .7), b=[dict(xr=.97, by=150, w=.36, t=(345, 296))]),
]
P['15'] = [
  dict(y0=150, n=('esq', .7)),
  dict(y0=40, b=[dict(x=.36, by=215, w=.42, t=(345, 362))]),
  dict(y0=60, n=('esq', .7)),
  dict(y0=60, b=[dict(x=.03, by=205, w=.45, t=(200, 348))]),
]
P['16'] = [
  dict(y0=150, n=('esq', .7)),
  dict(y0=120, n=('esq', .7), b=[dict(x=.03, sob=1, w=.45, t=(190, 255))]),
  dict(y0=100, b=[dict(xr=.97, by=110, w=.5, t=(232, 240))]),
  dict(y0=110, n=('esq', .7)),
]
P['17'] = [
  dict(y0=130, n=('esq', .7)),
  dict(y0=110, b=[dict(x=.03, by=120, w=.45, t=(115, 250))]),
  dict(y0=100, b=[dict(x=.03, by=115, w=.42, t=(225, 213))]),
  dict(y0=80, n=('esq', .7)),
]
P['18'] = [
  dict(y0=150, n=('esq', .7)),
  dict(y0=110, b=[dict(x=.05, by=130, w=.45, t=(275, 260))]),
  dict(y0=100, b=[dict(x=.03, by=180, w=.52, t=(130, 326))]),
  dict(y0=110, n=('esq', .7)),
]
P['19'] = [
  dict(y0=150, n=('esq', .7)),
  dict(y0=110, b=[dict(x=.03, by=130, w=.4, t=(140, 280))]),
  dict(y0=80, b=[dict(x=.25, by=95, w=.45, t=(220, 172))]),
  dict(y0=150, n=('esq', .7)),
]
P['20'] = [
  dict(y0=170, n=('esq', .75)),
  dict(y0=100, n=('esq', .7)),
  dict(y0=90, b=[dict(x=.03, by=100, w=.42, t=(214, 215))]),
  dict(y0=110, n=('esq', .7)),
]
P['21'] = [
  dict(y0=110, n=('esq', .75)),
  dict(y0=150, b=[dict(x=.05, by=165, w=.5, t=(275, 290))]),
  dict(y0=60, n=('esq', .7)),
  dict(y0=100, n=('esq', .7), b=[dict(xr=.97, sob=1, w=.45, t=(195, 185))]),
]
P['22'] = [
  dict(y0=100, n=('esq', .7)),
  dict(y0=110, b=[dict(x=.03, by=120, w=.45, t=(110, 285))]),
  dict(y0=110, b=[dict(xr=.9, by=130, w=.4, t=(240, 208))]),
  dict(y0=100, n=('esq', .7)),
]
P['23'] = [
  dict(y0=150, b=[dict(x=.03, by=170, w=.45, t=(112, 293))]),
  dict(y0=130, n=('dir', .46), b=[dict(x=.03, by=135, w=.5, t=(382, 282))]),
  dict(y0=100, n=('esq', .7)),
  dict(y0=50, n=('esq', .46), b=[dict(x=.03, sob=1, w=.4, t=(140, 262))]),
]
P['24'] = [
  dict(y0=80, n=('esq', .45)),
  dict(y0=110, n=('esq', .6), b=[dict(xr=.97, by=130, w=.3, t=(360, 222))]),
  dict(y0=110, b=[dict(x=.03, by=140, w=.45, t=(150, 230))]),
  dict(y0=125, n=('esq', .7)),
]
LINHAS['25'] = (87, 68.2)
P['25'] = [
  dict(y0=38, b=[dict(x=.03, by=60, w=.45, t=(310, 92))]),
  dict(y0=60, b=[dict(xr=.97, by=395, w=.45, t=(330, 338))]),
  dict(y0=120, n=('esq', .7)),
  dict(y0=90, n=('esq', .7)),
]
