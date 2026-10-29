# Pauta das 12h · @paisdarotina

Formato: informativo em motion design 2D, feito 100% por mim, com 20 a 25 s, 1080×1920.
Regras: nunca repetir tema, desenho ou música. Cada vídeo tem paleta e ilustrações próprias. Legenda sem a linha "feito com IA".

## Como produzir (receita aprovada pelo Mateus em 26/10)
1. **Roteiro** com pergunta-gancho, 3 pontos e um pedido ("Salva..." ou "Manda pra..."). Cada frase num parágrafo.
2. **Voz:** Amandinha (`r2fkFV8WAqXq2AqBpgJT`), eleven_multilingual_v2. Baixo pelo storage.googleapis.com.
3. **Calma:** transcrevo (scribe), corto nas frases, ponho pausas (0,25 a 0,45 s; maior entre pontos) e desacelero 10% (`atempo=0.9`). Ele achou a primeira versão rápida demais.
4. **Visual:** `tools/motion/info-2710-v2.html` é o molde (GSAP + Playwright, `render.js`).
   - Transição 3D suave: a cena vai pra trás e a próxima chega de baixo girando, com `transformPerspective` por cena e **sem preserve-3d** (dá corte no texto).
   - Câmera com zoom lento e fundo que desce a cada troca. Sem tremidas rápidas.
5. **Ferramentas:** `tools/pausas.py` (cortes, pausas e atempo 0,9, gera o cues.json) e `tools/mix12h.sh` (mistura com ganho fixo). Palavra fraca (ex.: "Mito." solto): suba +5 dB só nela antes da mistura.
6. **Mistura com ganho fixo** (lição de 27/10): o loudnorm dinâmico na voz abaixou o fim da frase e a música cobriu "dia difícil". Agora: medir a voz e a música (ebur128), aplicar volume fixo pra -16 e -27, somar, ganho fixo pra -14 e limitador. Final de frase baixinho: subir uns +8 dB só naquele trecho. Sempre transcrever o áudio final pra conferir que nenhuma palavra sumiu.
7. **Música emocional**, que ele prefere à alegre. Volume fixo, sem ducking (o sobe e desce pareceu defeito): música `loudnorm I=-27`, voz `I=-16`, total -14 LUFS.
8. Exporto em até 20 MB, subo em `AAAA-MM-DD-.../`, agendo com `send_later` pra 11h59 e mando a prévia.

## Temas
**Pedido do Mateus (26/10):** cada vídeo com dados reais e fontes fortes, de várias áreas (pediatria brasileira, OMS, pediatria americana, CDC, Harvard, estudos com milhares de crianças), dizendo o nome da instituição na tela e na voz. Tudo vem do `BANCO-DE-FONTES.md`. Misturar pelo menos 2 fontes diferentes por vídeo.

| Dia | Tema | Pontos e fontes (ver BANCO-DE-FONTES.md) | Paleta |
|---|---|---|---|
| Ter 27/10 ✅ | 3 erros na hora de dormir | horário fixo · ritual calmo · mesma ordem (AAP) | noite azul |
| Qua 28/10 ✅ agendado | Elogio e bronca: o que a ciência diz | palmada não ensina autocontrole, grito não melhora o comportamento (AAP 2018) · o que funciona: elogiar o comportamento bom, combinar regras antes, cumprir sempre (AAP 2018) · descrever o que ele faz ajuda a autoestima (CDC) · `2026-10-28-info-elogio-bronca/`, molde `tools/motion/info-2810.html` | nascer do sol (pêssego) |
| Qui 29/10 ✅ agendado | Mito ou verdade? | "Fim de semana pode dormir qualquer hora" MITO (SBP 2021 + governo da Austrália 2021) · "Tela antes de dormir relaxa" MITO (SBP 2021 + Sociedade Canadense de Pediatria 2017: 1 h antes) · "Birra pra dormir é normal até uns 4 anos" VERDADE (SBP 2018; luz baixa e banho morno) · troquei o VERDADE da UCL 2013 porque Kelly 2013 entra na sexta · `2026-10-29-info-mito-verdade/`, molde `tools/motion/info-2910.html` | verde e coral com carimbos, termina de noite com o Bento na cama |
| Sex 30/10 ✅ agendado | O que a ciência descobriu sobre rotina de dormir | 10.085 crianças (Mindell 2015, Saint Joseph's University, EUA) · 405 famílias, 3 semanas, mães de melhor humor (Mindell 2009, divulgado pela Academia Americana de Medicina do Sono) · 10 mil crianças em Londres, efeito reversível (Kelly 2013, UCL, Reino Unido) · `2026-10-30-info-ciencia-rotina/`, molde `tools/motion/info-3010.html` (contadores calculados no seek, gráficos marcados "ilustração") · música: piano próprio, semente 3010 | noite verde-água com lua, Bento cientista no fim |
| Sáb 31/10 | Depois da escola: o que 3 instituições recomendam | 3 horas de movimento por dia até os 4 anos (OMS) · de 3 a 5 anos, 1 hora disso é brincadeira intensa, e nada de ficar preso mais de 1 hora seguida no carrinho ou cadeirinha (governo da Austrália, 2021) · brincar constrói o cérebro (Academia Americana de Pediatria, 2018) | tarde no parque |
| Dom 01/11 | O cérebro do seu filho e o "vai e volta" | mais de 1 milhão de conexões por segundo nos primeiros anos (Harvard) · responder quando ele puxa conversa constrói o cérebro (Harvard) · ler em voz alta todo dia desde bebê (Academia Americana de Pediatria, 2014) · quem ouve mais histórias em casa ativa mais as áreas da imaginação (Hospital Infantil de Cincinnati, 2015) | lilás |

**Troca em 26/10:** "Manhã sem briga" saiu da quarta porque os mesmos dados (véspera, escolhas, despedida) entram na Família Tatu partes 3 e 4 (ver `PAUTA-20H.md`). Não repetir dado entre 12h e 20h do mesmo dia ou da véspera.

**Pedido do Mateus (27/10):** muitas fontes, de vários países ("do céu ao limite"). Cada vídeo mistura pelo menos 3 instituições, de preferência de países diferentes. Fatos novos na seção "Mundo" do `BANCO-DE-FONTES.md`.

### Semana de 02 a 08/11 (RASCUNHO: só vale depois da revisão dos números, domingo 01/11 às 21h)
| Dia | Tema | Pontos e fontes | Paleta |
|---|---|---|---|
| Seg 02/11 | Quanto seu filho precisa dormir? | 1–2 anos: 11 a 14 h · 3–5 anos: 10 a 13 h (Academia Americana de Medicina do Sono, com a pediatria americana, 2016) · a OMS confirma (2019) · sempre nos mesmos horários de dormir e acordar (governo da Austrália, 2021) | azul-marinho e estrelas, gráfico de barras por idade |
| Ter 03/11 | Telas por idade: o que 4 países dizem | Brasil: menos de 2 anos, nada; 2 a 5, até 1 h (SBP 2020) · Alemanha: 3 a 6 anos, até 30 min (diretriz nacional 2023) · França: sem TV antes dos 3 (regra 3-6-9-12, Santé.fr) · OMS: até 4 anos, no máximo 1 h | mapa-múndi com bandeirinhas |
| Qua 04/11 | O autocontrole se treina brincando | não nasce pronto, é como uma torre de controle de aeroporto (Harvard) · faz de conta, contar histórias, dança da estátua, separar por cor e depois por forma (Harvard) · brincar ajuda nas funções executivas (Academia Americana de Pediatria, 2018) | amarelo e azul, aviãozinho e torre |
| Qui 05/11 | Na mesa, sem tela | refeição é momento de afeto em família (Guia Alimentar, Ministério da Saúde, 2019) · sem tela nas refeições (SBP 2020) · rotina da refeição: lavar as mãos e pôr a mesa juntos (CDC) | terracota e verde-oliva |
| Sex 06/11 | O pai que brinca faz diferença | pais que brincavam mais com o bebê aos 3 meses tiveram filhos com melhores testes aos 2 anos (Imperial College London, 2017) · pai calmo na hora do livro também ajudou (mesmo estudo) · brincar fortalece o vínculo com os pais (Academia Americana de Pediatria, 2018) | azul-petróleo e laranja |
| Sáb 07/11 | Canção de ninar funciona? | bebês relaxam com canção de ninar até em outra língua: coração e pupila desaceleram (Harvard, 2020) · ritual calmo de até 30 minutos (SBP 2021) · "escova, livro, cama" (CDC) | rosa-chá e lua |
| Dom 08/11 | a definir no domingo 01/11, com os números da semana | fonte nova, pesquisada e conferida antes | — |

Regra: o dado do 12h não pode ser o mesmo da Família Tatu do mesmo dia ou da véspera (ver `PAUTA-20H.md`, temporada 2).

## Músicas
- Já usadas: kids happy (amostra 1), kids-kids-happy (amostra 2), gentle baby sleep lullaby dream (Ter 27), lullaby-baby-sleeping (Qua 28), music-box-sleep-lullaby (Qui 29).
- **Acabaram as emocionais.** Sexta em diante: música nova do Mateus ou o piano próprio (`tools/musica.py piano`, semente nova). Sex 30: piano semente 3010. As de comédia ficam pra Família Tatu.
- Pedi a ele: buscas "emotional piano", "heartwarming", "sentimental", "inspiring emotional".
