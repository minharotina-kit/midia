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
5. **Música emocional**, que ele prefere à alegre. Volume fixo, sem ducking (o sobe e desce pareceu defeito): música `loudnorm I=-27`, voz `I=-16`, total -14 LUFS.
6. Exporto em até 20 MB, subo em `AAAA-MM-DD-.../`, agendo com `send_later` pra 11h59 e mando a prévia.

## Temas (só com fonte da seção 5 da variacao-conteudo-rotina)
| Dia | Tema | Pontos | Fonte | Paleta |
|---|---|---|---|---|
| Ter 27/10 ✅ | 3 erros na hora de dormir | horário fixo · ritual calmo · mesma ordem | AAP | noite azul |
| Qua 28/10 | Manhã sem briga: 3 truques | 2 opções ("essa ou aquela?") · acordar com calma, de bom humor · despedida curta | AAP | nascer do sol (pêssego) |
| Qui 29/10 | Mito ou verdade: rotina tem que ser rígida? | rígida demais cansa (MITO) · previsível ajuda (VERDADE) · escolhas simples ajudam (VERDADE) | AAP | verde e coral com carimbos |
| Sex 30/10 | 10.085 crianças: o que um estudo achou | dormiam mais cedo · pegavam no sono mais rápido · acordavam menos | Mindell e colegas, Sleep 2015 | lua e verde-água, gráficos |
| Sáb 31/10 | Depois da escola: 3 coisas que ajudam | brincar e se mexer · refeição em família sem tela · noite calma | AAP | tarde no parque |
| Dom 01/11 | Previsível acalma: saber o que vem depois | quadro com desenhos · mesma sequência · avisar antes de mudar | AAP | lilás |

## Músicas
- Já usadas: kids happy (amostra 1), kids-kids-happy (amostra 2), gentle baby sleep lullaby dream (Ter 27, publicada).
- Sobram de ninar/emocionais: music-box-sleep-lullaby, lullaby-baby-sleeping. As de comédia ficam pra Família Tatu.
- Pedi a ele: buscas "emotional piano", "heartwarming", "sentimental", "inspiring emotional".
