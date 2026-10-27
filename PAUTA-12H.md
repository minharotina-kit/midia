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
5. **Mistura com ganho fixo** (lição de 27/10): o loudnorm dinâmico na voz abaixou o fim da frase e a música cobriu "dia difícil". Agora: medir a voz e a música (ebur128), aplicar volume fixo pra -16 e -27, somar, ganho fixo pra -14 e limitador. Final de frase baixinho: subir uns +8 dB só naquele trecho. Sempre transcrever o áudio final pra conferir que nenhuma palavra sumiu.
6. **Música emocional**, que ele prefere à alegre. Volume fixo, sem ducking (o sobe e desce pareceu defeito): música `loudnorm I=-27`, voz `I=-16`, total -14 LUFS.
7. Exporto em até 20 MB, subo em `AAAA-MM-DD-.../`, agendo com `send_later` pra 11h59 e mando a prévia.

## Temas
**Pedido do Mateus (26/10):** cada vídeo com dados reais e fontes fortes, de várias áreas (pediatria brasileira, OMS, pediatria americana, CDC, Harvard, estudos com milhares de crianças), dizendo o nome da instituição na tela e na voz. Tudo vem do `BANCO-DE-FONTES.md`. Misturar pelo menos 2 fontes diferentes por vídeo.

| Dia | Tema | Pontos e fontes (ver BANCO-DE-FONTES.md) | Paleta |
|---|---|---|---|
| Ter 27/10 ✅ | 3 erros na hora de dormir | horário fixo · ritual calmo · mesma ordem (AAP) | noite azul |
| Qua 28/10 ✅ agendado | Elogio e bronca: o que a ciência diz | em vez de só "muito bem", descrever o que ele fez (CDC) · palmada não ensina, e grito também não (AAP 2018) · o que funciona: elogiar o bom comportamento e ser constante (AAP 2018) | nascer do sol (pêssego) |
| Qui 29/10 | Mito ou verdade? | "Fim de semana pode dormir qualquer hora" MITO (SBP 2021) · "Tela antes de dormir relaxa" MITO (SBP 2021: 1 h antes, melatonina) · "Rotina ajuda o comportamento" VERDADE (UCL 2013, 10 mil crianças) | verde e coral com carimbos |
| Sex 30/10 | O que a ciência descobriu sobre rotina de dormir | 10.085 crianças (Mindell 2015) · 405 famílias, 3 semanas, mães de melhor humor (Mindell 2009) · 10 mil crianças em Londres, efeito reversível (Kelly 2013) | lua e verde-água, contadores e gráficos |
| Sáb 31/10 | Depois da escola: 3 coisas que ajudam | 3 horas de movimento por dia (OMS) · brincar constrói o cérebro (AAP 2018) · tela desligada 1 a 2 h antes de dormir (SBP 2020) | tarde no parque |
| Dom 01/11 | O cérebro do seu filho e o "vai e volta" | mais de 1 milhão de conexões por segundo (Harvard) · responder quando ele puxa conversa (Harvard) · ler em voz alta todo dia (AAP 2014 + Cincinnati 2015) | lilás |

**Troca em 26/10:** "Manhã sem briga" saiu da quarta porque os mesmos dados (véspera, escolhas, despedida) entram na Família Tatu partes 3 e 4 (ver `PAUTA-20H.md`). Não repetir dado entre 12h e 20h do mesmo dia ou da véspera.

**Próxima semana (já com fonte):** quanto seu filho precisa dormir por idade (AASM/AAP 2016 + OMS) · telas por idade (SBP 2020 + OMS + CDC: TV fora do quarto) · ritual de até 30 minutos (SBP 2021) · refeição é afeto, sem tela (Ministério da Saúde + SBP) · birra pra dormir é comum até uns 4 anos (SBP 2018) · ler em voz alta desde bebê (AAP 2014). Conferir antes se a novela já usou o dado.

## Músicas
- Já usadas: kids happy (amostra 1), kids-kids-happy (amostra 2), gentle baby sleep lullaby dream (Ter 27), lullaby-baby-sleeping (Qua 28).
- Sobra de ninar/emocional: só music-box-sleep-lullaby (pra quinta). Sexta em diante precisa de música nova do Mateus. As de comédia ficam pra Família Tatu.
- Pedi a ele: buscas "emotional piano", "heartwarming", "sentimental", "inspiring emotional".
