---
name: kit-dezembro-com-jesus
description: Use para montar, revisar ou corrigir o kit imprimível Dezembro com Jesus (quadrinho do dia, Hora de pintar, calendário, presépio, cartões e certificado), com as regras de Bíblia (ARA, linguagem cristã), visual e checagens.
---

# Pacote de produção · Dezembro com Jesus

**Para o Claude que recebeu este PDF.** O Mateus vai só te mandar este arquivo, sem explicar nada. Tudo o que você precisa está aqui: o pedido, as regras, os textos prontos e, anexados dentro do PDF, as imagens, as fontes e os dados. Leia tudo antes de começar.

## 1. Quem é o Mateus e como falar com ele

- Ele vende produtos digitais para mães com uma **marca anônima**. Nunca use nome de pessoa no produto.
- Fale em português do Brasil, com frases curtas e diretas, em formato visual (listas curtas, tabelas). Sem elogio e sem enrolação. Pode chamar de "mano".
- Ele é cristão e quer o produto **fiel à Bíblia**.
- Ele já recusou duas versões porque ficaram "robotizadas" e "fracas". O padrão dele é alto: um material bonito, completo, que pareça produto de verdade.

## 2. Passo 0: pegar os arquivos anexados

Este PDF tem 3 anexos dentro dele: `arquivos.zip`, `dados.json` e `SKILL.md`.

```bash
mkdir -p entrada && pdfdetach -saveall -o entrada/ pacote-dezembro-com-jesus.pdf
# sem poppler:
python3 -c "import pypdf,os; r=pypdf.PdfReader('pacote-dezembro-com-jesus.pdf'); [open('entrada/'+k,'wb').write(v[0]) for k,v in r.attachments.items()]"
cd entrada && unzip -q arquivos.zip
```

Se não achar o PDF no disco (`find / -name "pacote-dezembro*" 2>/dev/null`), peça ao Mateus pra anexar de novo ou arrastar o arquivo pra pasta de trabalho. Sem os anexos não tem como montar.

Depois copie `SKILL.md` para `.claude/skills/kit-dezembro-com-jesus/SKILL.md` na pasta de trabalho. Assim as próximas conversas já sabem as regras.

| Pasta ou arquivo | O que tem |
|---|---|
| `quadrinhos/noite-NN-qK.jpg` | 100 quadros coloridos **sem texto** (25 noites × 4). q1 = em cima à esquerda, q2 = em cima à direita, q3 = embaixo à esquerda, q4 = embaixo à direita. 497×751 px (2:3). O terço de cima de cada quadro foi deixado mais vazio para os balões. |
| `pintar/noite-NN.png` | 25 desenhos de colorir em linha preta (1254×1254). |
| `presepio/presepio-1..3.png` | 3 folhas do presépio de montar (1024×1536). |
| `capa.jpg` | Ilustração colorida da capa (presépio). |
| `personagens.jpg` | Folha com todos os personagens (1536×1024). |
| `fontes/` | Fredoka 600/700 (títulos), Atkinson Hyperlegible 400/700 (texto), Comic Neue 400/700 (balões). |
| `referencias/album-base-atual-02.jpg` | Como o álbum está hoje. É **só o esqueleto**: o Mateus não aprovou. |
| `referencias/hora-de-pintar-aprovada-2.jpg` | A página "Hora de pintar" que o Mateus **aprovou**. Siga essa estrutura. |
| `dados.json` | Todos os textos de cada noite: tema, leitura, versículo (ARA, já conferido), narração e falas de cada quadro, mensagem do dia, pergunta, frase pra guardar, desafio, oração, "Você lembra?". Também tem a página final e a lista de versículos a conferir. |

## 3. O pedido do Mateus

Montar o kit **completo** "Dezembro com Jesus" num PDF só, pronto pra vender (R$ 19,90) e imprimir em casa. É para pais lerem com filhos de 3 a 8 anos, de 1 a 24 de dezembro, com um bônus no dia 25.

O que ele pediu, nas palavras dele, resumido:
1. **Cara de gibi de verdade.** Hoje cada página tem 4 quadros enormes e parece "4 figuras", não um quadrinho. Ele quer **quadros menores**, com cara de revista em quadrinhos.
2. **Uma mensagem por dia** que ensina mais de Deus e de Jesus: o que é o Natal, por que Jesus veio, por que Jesus morreu. Cada dia puxa o versículo e vai crescendo até a cruz e a ressurreição. As mensagens já estão escritas em `dados.json` (campo `mensagem`).
3. **Juntar tudo num PDF só**: quadrinho, página de pintar, calendário, presépio, cartões e certificado.

## 4. Regras de conteúdo (não negociáveis)

- **Só o que a Bíblia diz.** A linguagem é cristã (evangélica): nada de tradição que vai além da Bíblia.
  - Jesus é o único Salvador. A salvação vem pela graça, por meio da fé.
  - A oração é direta a Deus e termina "em nome de Jesus". Uma oração dirigida a Jesus pode terminar só com "Amém".
  - Maria aparece como a Bíblia mostra: a serva do Senhor que confiou em Deus. Sem títulos ("Nossa Senhora"), sem oração a ela, sem santos.
- **Nada contra outra igreja.** O texto só mostra a Bíblia. Um católico lê e não encontra ataque.
- **Os magos:** a Bíblia não diz quantos eram. Nunca escreva "três reis" nem "três magos" em texto (nos desenhos pode ter três).
- **Animais no nascimento:** a Bíblia fala da manjedoura, não de boi e jumento. Os desenhos podem mostrar bichos, mas o texto nunca diz "a Bíblia diz que tinha boi".
- **Versículos na Almeida Revista e Atualizada (ARA)**, com livro, capítulo e versículo exatos. Os de `dados.json` já foram conferidos em bibliaonline.com.br.
  - Confira os que estão em `conferir` antes de usar: abra `https://www.bibliaonline.com.br/ara/<livro>/<capítulo>` e copie o texto exato.
  - Reticências (…) marcam um trecho do versículo.
  - Crédito no rodapé: "Textos bíblicos: Almeida Revista e Atualizada (ARA), Sociedade Bíblica do Brasil."
- **Não reescreva os textos de `dados.json`.** Se achar erro de português ou de Bíblia, corrija e avise o Mateus no fim, dizendo o que mudou.
- Nada de cena pesada: a cruz é falada com delicadeza, sem sangue e sem detalhe de sofrimento.
- Marca no rodapé: "Dezembro com Jesus · @paisdarotina". Confirme com o Mateus na primeira prévia.

## 5. Estrutura do kit (ordem das páginas)

| Página | Conteúdo |
|---|---|
| 1 | **Capa**: `capa.jpg` grande, título "Dezembro com Jesus", promessa "Ensine seu filho sobre Jesus em 24 noites" e selos "25 histórias em quadrinhos · Páginas para pintar · Presépio de montar". |
| 2 | **Como usar** (texto na seção 8). |
| 3 | **Meu caminho até o Natal**: calendário para a geladeira, 24 casinhas numeradas para pintar e uma estrela grande no fim (25). Linha "Família: ____". |
| 4 | **Conheça os personagens**: `personagens.jpg` e os nomes. |
| 5 a 54 | **Os 25 dias, 2 páginas cada**: (A) Quadrinho do dia, (B) Hora de pintar. |
| 55 | **Por que Jesus veio? O maior presente de todos** (`final` em `dados.json`). |
| 56 a 58 | **Presépio de montar**, 3 folhas. |
| 59 | **Cartões de gratidão para pintar** (4 cartões: "Feliz Natal! Para: __ Obrigado por __ De: __"), usados na noite 23. |
| 60 | **Certificado**: "Nós completamos o Dezembro com Jesus!", "Foram 24 noites de histórias, conversas e orações em família, esperando juntos o nascimento de Jesus.", "Família: ____", "Natal de 2026" e 25 estrelinhas. |

## 6. Página A do dia: "Quadrinho do dia"

**Objetivo:** a página parece uma página de gibi infantil de verdade, e ainda sobra espaço para a Palavra de Deus e a mensagem.

**Elementos, de cima para baixo:**
1. **Topo compacto:** selo vermelho com o número do dia, "Dia 1 · 1º de dezembro", o título do tema (Fredoka 700) e "Ler na Bíblia: …". No dia 25, o selo é dourado e diz "Bônus · 25 de dezembro".
2. **O quadrinho** com os 4 quadros da noite, ocupando **cerca de 55% a 60% da altura útil**.
   - Moldura preta fina (0,6 mm) e cantos levemente arredondados.
   - Espaço branco de 2,5 a 3 mm entre os quadros.
   - O balão pode passar um pouco da borda do quadro, como em gibi.
3. **Palavra de Deus:** cartão com a referência e o versículo (campo `versiculo`).
4. **O que Deus nos ensina hoje:** a mensagem do dia (campo `mensagem`), em letra boa de ler (Atkinson, 10,5 a 11 pt).
5. **Pra conversar:** a pergunta (campo `conversa`).
6. **Rodapé:** crédito da ARA e a marca.

**Como fazer o quadrinho parecer gibi:**
- **Narração** (campo `narra`) numa **caixinha amarela clara retangular** (recordatório), presa no canto de cima do quadro.
- **Falas** (campo `baloes`, pares [quem fala, fala]) em **balão branco com contorno preto e rabinho apontando para quem fala**.
  - O nome de quem fala vai pequeno, em caixa alta, em cima da fala, ou fica implícito pelo rabinho. Teste e escolha o mais claro.
  - Fonte Comic Neue Bold, **nunca menor que 8,5 pt**.
- Para saber para onde o rabinho aponta, **olhe cada quadro** e veja onde está o personagem. Guarde as posições num `posicoes.json` (quadro → lado do balão e ponto do rabinho).
- **Nenhum balão cobre rosto.** Use o terço de cima (que está mais vazio).
- **Corte** dos quadros (object-fit: cover): pode cortar das bordas para ajustar a proporção, mas **nunca corte cabeça, rosto ou o personagem principal**.
- Os 4 quadros podem ter tamanhos diferentes (por exemplo, um quadro largo e dois menores), desde que a ordem de leitura fique óbvia: esquerda para a direita, de cima para baixo.

**Faça 2 opções do dia 1** e mostre as duas ao Mateus:
- **Opção A, "gibi em cima":** os 4 quadros numa grade 2×2 menor, em cima. Palavra de Deus, mensagem e pergunta embaixo, na largura toda.
- **Opção B, "gibi com coluna":** os 4 quadros à esquerda (cerca de 60% da largura). À direita, uma coluna com Palavra de Deus, mensagem e pergunta.

Ele escolhe uma, e você aplica nas 25 noites.

## 7. Página B do dia: "Hora de pintar!" (já aprovada)

Siga `referencias/hora-de-pintar-aprovada-2.jpg`:
- **Topo:** círculo vermelho com o número, "Noite 1 · 1º de dezembro", "Hora de pintar!" e o selo "Para a criança".
- **Bloco amarelo:** "Para guardar no coração" com a frase do campo `guardar`, e embaixo "Para ler na Bíblia com a família: …" (campo `leitura`).
- **O desenho** `pintar/noite-NN.png` grande, num quadro branco de cantos arredondados.
- **Três cartões lado a lado:**
  - **Desafio do dia** (amarelo, campo `desafio`);
  - **Vamos orar** (rosa, campo `oracao`);
  - **Você lembra?** (verde, campo `lembra`), com "Resposta: …" (campo `resposta`).
- **Rodapé:** quadradinho "Pintei a casinha N no calendário" e a marca.
- Fundo branco: é a página que a criança pinta. Economize tinta.

## 8. Textos das outras páginas

**Como usar**: "Dez minutinhos por noite, de 1 a 24 de dezembro. Sem pressa e sem precisar ser perfeito." Em 5 passos:
1. **Imprima e cole o calendário** na geladeira, na altura dos olhos da criança.
2. **Toda noite, leiam o quadrinho do dia juntos.** Quem ainda não lê acompanha pelos desenhos; quem já lê pode ler as falas.
3. **Leia a Palavra de Deus e a mensagem**, e façam a pergunta do "Pra conversar".
4. **Hora de pintar:** façam o desafio, orem juntos, e a criança pinta o desenho e a casinha do dia.
5. **Monte o presépio no caminho:** nas noites 12 e 13 vocês começam. Na noite 24, o menino Jesus chega na manjedoura.

Depois, duas caixas:
- **"O que você vai precisar":** impressora (ou uma gráfica rápida), lápis de cor ou giz de cera, tesoura sem ponta e cola. Papel mais grosso deixa o presépio firme.
- **"Perdeu uma noite?":** tudo bem. Façam duas no dia seguinte, ou fiquem só com a história e a oração.

**Presépio**: "Pinte, recorte na linha de fora e dobre a aba tracejada para a figura ficar em pé."
- Folha 1: "A família de Jesus" (Maria, José, o menino Jesus, o anjo e a estrela).
- Folha 2: "Os animais e o pastor".
- Folha 3: "Os magos e o estábulo". Nunca "os três magos".

**Por que Jesus veio?**: use `final` de `dados.json`. São 5 passos curtos, cada um com um ícone simples e a referência:
1. Deus ama você
2. Todos nós erramos
3. Jesus nasceu
4. Jesus morreu e ressuscitou
5. Um presente de graça

Depois vem João 3:16 em destaque e a caixa "Para quem quer seguir Jesus" com a oração. Pode usar 1 ou 2 quadros já existentes (por exemplo, `noite-24-q4` e `noite-17-q4`). **Não desenhe a cruz com IA.** Se quiser um símbolo, use uma cruz simples de traço e um sol nascendo (ressurreição), em SVG.

## 9. Visual

- **A4 em pé**, margem de 12 mm, sem sangria.
- **Cores:**

| Cor | Hex |
|---|---|
| tinta | #2a2f4a |
| tinta clara | #585d76 |
| verde | #2e6b4f |
| verde claro | #e6f2eb |
| vermelho | #c8463d |
| vermelho claro | #fbe9e6 |
| dourado | #d9a521 |
| dourado claro | #fcf2d8 |
| azul claro | #e7eefa |
| creme | #fffaf0 |

- **Fontes:**
  - Fredoka 600/700 nos títulos;
  - Atkinson Hyperlegible 400/700 no texto;
  - Comic Neue 700 nos balões e na narração.
  - Use os arquivos de `fontes/` com `@font-face` e sirva a pasta por `python3 -m http.server`: abrindo por `file://`, o Chromium bloqueia as fontes.
- **Fundo das páginas internas** branco ou creme bem claro. Só a capa pode ter fundo escuro.
- Montagem: HTML e CSS, depois PDF com Playwright e Chromium (`page.pdf`, `printBackground: true`). Sem Playwright, use WeasyPrint.

## 10. Ordem de trabalho

1. Extraia os anexos e confira as quantidades: 100 quadros, 25 desenhos de pintar, 3 presépios, capa e personagens.
2. Confira na ARA os versículos da lista `conferir` e coloque o texto exato onde for citado (noite 13 e página final).
3. **Prévia para o Mateus:**
   - Monte o dia 1 nas opções A e B, a página B do dia 1 e a página "Por que Jesus veio?".
   - Gere PNG de cada uma e mostre.
   - **Espere ele escolher** antes de montar o resto, porque isso economiza crédito.
4. Monte o kit inteiro com a opção escolhida.
5. Faça as checagens (seção 11) e corrija o que falhar.
6. Entregue (seção 12).

## 11. Checagens antes de entregar

- **Nada vaza da página:** meça cada página com `getBoundingClientRect` e confira se o conteúdo termina antes do rodapé.
- **Texto igual ao `dados.json`:**
  - extraia com `pdftotext` e compare por código, noite por noite;
  - entram tema, versículo, narração, falas, mensagem, pergunta, frase, desafio, oração e "Você lembra?";
  - a conferência precisa dar 25/25.
- **Olhe todas as páginas:** gere folhas de contato (6 a 8 páginas por imagem) e verifique se algum balão cobre rosto, se algum corte cortou cabeça e se alguma fonte caiu para a padrão.
- `pdffonts`: todas as fontes embutidas.
- **Tamanho:** até 15 MB. Se passar, recomprima os JPG dos quadros (qualidade 85).
- **Número de páginas:** cerca de 60, conforme a seção 5.

## 12. Entrega

- `Dezembro-com-Jesus-kit-completo.pdf`.
- Pasta `previas/` com PNG (1080 px de largura) da capa, das 2 páginas do dia 1, de uma página de pintar e da página "Por que Jesus veio?", para a página de venda e os anúncios.
- Mensagem curta pro Mateus com:
  - o que ficou pronto;
  - quantas páginas e o tamanho do arquivo;
  - o que você corrigiu nos textos (se corrigiu);
  - 1 ou 2 pontos pra ele olhar com atenção.
