# Dezembro com Jesus · montagem do kit

Regras completas: `.claude/skills/kit-dezembro-com-jesus/SKILL.md`.

## Situação (29/10/2026)
- Prévia enviada ao Mateus: dia 1 nas opções A e B, Hora de pintar 1 e "Por que Jesus veio?" (`previas/`).
- **Esperando ele escolher A ou B** antes de montar as 25 noites.
- Marca no rodapé "Dezembro com Jesus · @paisdarotina": falta ele confirmar.
- bibliaonline.com.br bloqueado na rede da sessão: 2 Coríntios 8:9 e João 3:16 ainda sem conferência no site.

## Como remontar
Os anexos não estão aqui (produto pago). Peça o PDF do pacote ao Mateus.
```bash
mkdir -p entrada && pdfdetach -saveall -o entrada/ pacote-dezembro-com-jesus.pdf && (cd entrada && unzip -q arquivos.zip)
python3 -I limpar_quadros.py entrada/quadrinhos limpos   # tira a moldura colada nos quadros
ln -sfn ../entrada/fontes build/fontes
python3 -I gerar.py previa                                # -> previa.html
python3 -m http.server 8765 --bind 127.0.0.1 &            # fontes não carregam por file://
node render.js previa.html previa.pdf png 1240            # PDF + PNG por página + checagens
```
- `posicoes.json`: recorte e balões de cada quadro (ponta do rabinho em px da imagem limpa). `grade.py` desenha a grade de coordenadas.
