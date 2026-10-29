# Dezembro com Jesus · montagem do kit

Regras completas: `.claude/skills/kit-dezembro-com-jesus/SKILL.md`.

## Situação (29/10/2026)
- **Kit completo montado na opção A** (gibi em cima): 60 páginas A4, 13,1 MB.
- Marca no rodapé confirmada: "Dezembro com Jesus · @paisdarotina".
- 2 Coríntios 8:9 e João 3:16 conferidos pelo Mateus no bibliaonline.com.br. O cartão da noite 13 começa com "Pois" (P maiúsculo).
- **Capa nova** (29/10): `entrada/capa-nova.png`, 1024×1536, enviada pelo Mateus. Se o arquivo existir, o `kit.py` usa ela numa moldura de 118,7 × 178 mm (~219 dpi, nunca abaixo de 200 dpi). Sem ele, volta pra `capa.jpg`.
- Ajustes finais aprovados (29/10): página final com "(Gênesis 1:1; João 3:16)" no passo 1 e "(Lucas 2:11; Hebreus 4:15)" no passo 3 (mudado no `dados.json`), e caixinha "Para economizar tinta" no Como usar.

## Como remontar
Os anexos não estão aqui (produto pago, repositório público). Peça o PDF do pacote ao Mateus.
```bash
mkdir -p entrada && pdfdetach -saveall -o entrada/ pacote-dezembro-com-jesus.pdf && (cd entrada && unzip -q arquivos.zip)
python3 -I limpar_quadros.py entrada/quadrinhos limpos   # tira a moldura colada nos quadros
ln -sfn ../entrada/fontes build/fontes
python3 -I kit.py                                         # -> kit.html (60 páginas)
python3 -m http.server 8765 --bind 127.0.0.1 &            # fontes não carregam por file://
node render.js kit.html Dezembro-com-Jesus-kit-completo.pdf png-kit 900   # PDF + PNG + checagens
python3 -I checar_texto.py Dezembro-com-Jesus-kit-completo.pdf            # texto do PDF x dados.json (25/25)
```
- `pos_a.py`: recorte (`y0`) e balões de cada quadro das noites 2 a 25 (ponta do rabinho em px da imagem limpa). Noite 1 em `posicoes.json["A"]`.
- `sobra.json`: espaço que sobrava no pé de cada página de quadrinho; o `kit.py` passa esse espaço pros quadros. Se mudar texto, rode, veja a sobra no log e ajuste.
- `grade.py` desenha a grade de coordenadas num quadro, pra posicionar balão sem cobrir rosto.
