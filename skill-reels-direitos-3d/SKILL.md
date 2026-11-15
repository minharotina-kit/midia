---
name: reels-direitos-3d
description: Use para produzir os Reels 3D da série "direitos do autista" do @paisdarotina (instituição nega um direito → 3 desculpas → o que diz a lei → meme → pedido de comentário), do roteiro com fonte até o MP4 1080x1920 com voz, legenda e trilha.
---

# Reels 3D: série "direitos do autista" (@paisdarotina)

Perfil sem rosto para pais de crianças autistas, que mistura fé cristã e informação.
Cada vídeo mostra **uma instituição negando um direito** (escola, plano de saúde, fila, INSS, creche...) e desmonta **3 desculpas**, com a lei na tela.
Os que mais deram certo: matrícula recusada (42 mil views) e plano de saúde negando terapia.
O que **não** funciona: "e se acontecer" (ex.: pilha engolida) e assunto morno.

## 1. Formato que funciona (não mudar)
- **40 a 50 s**, 30 fps, 1080x1920.
- **Gancho em 0 s**: a frase da desculpa, em vermelho, dita pelo atendente (ex.: *"Autismo leve não dá BPC."*).
- **3 desculpas**, cada uma com:
  - contador "DESCULPA 1/3";
  - balão com a fala do atendente;
  - resposta com a lei;
  - cartão com o nome da lei;
  - carimbo verde batendo.
- **"O que quase ninguém sabe"**: um detalhe extra, útil e verdadeiro.
- **MEME OBRIGATÓRIO**, pedido fixo do Mateus: um toque engraçado no meio e outro no fim, para o povo rir e comentar. Exemplos que já usamos:
  - esqueleto na sala de espera com a plaquinha "ESPERANDO A PERÍCIA";
  - "Se o atendente insistir... mostra esse vídeo." O atendente sua e escorrega pra debaixo da mesa, e a criança põe óculos pixelado "deal with it";
  - no fim, o painel chama a senha do esqueleto e ele levanta comemorando.
- **Pedido de comentário engraçado no fim**: "Comenta a desculpa que te deram. A mais absurda vira vídeo." Na tela aparece uma caixa de comentário sendo digitada.
- **Vídeo diferente a cada parte**:
  - cenário NOVO (supermercado, agência do INSS, sala de casa, creche, posto de saúde...);
  - personagens de **corpo inteiro** andando, pulando e gesticulando;
  - objetos que **se montam** na tela (blocos subindo, moedas empilhando, prédio se montando peça por peça);
  - **corte a cada 2 a 4 s**, com subcortes de câmera dentro dos planos longos.
  - Nunca repetir o mesmo enquadramento de "cabeça atrás de um guichê".

## 2. Fatos: só com fonte
- Todo número, lei e prazo tem que vir de fonte oficial (gov.br, planalto, STF/STJ, ANS, cartilha do órgão) ou de um escritório que cite a lei. Se não achar fonte, **corta do roteiro**.
- Escrever datas e números como se fala: "dois mil e doze", "trinta dias".
- Legenda do post:
  - as 3 desculpas com a lei de cada uma;
  - o "quase ninguém sabe";
  - um **versículo bíblico** (não repetir o da parte anterior);
  - a linha do meme e o pedido de comentário;
  - "Segue @paisdarotina pra Parte N.";
  - as fontes;
  - **"Informação, não orientação jurídica."**;
  - 5 hashtags.

## 3. Voz (ElevenLabs)
- Voz **Lax**, `voice_id tS45q0QcrDHqHoaWdCDR`, modelo `eleven_v4`. A narração toda numa tomada só, um parágrafo por frase.
- Abrir com uma tag de tom: `[firme, indignado, ritmo rápido de Reels]`. Antes do meme, `[tom debochado]`; antes do pedido de comentário, `[animado]`.
- Siglas escritas do jeito que se fala:
  - BPC → "bê pê cê"
  - INSS → "i ene esse esse"
  - STF → "ésse tê éfe"
  - CRAS → "Crás"
  - 135 → "cento e trinta e cinco"
- Custa cerca de 1 crédito por caractere (uns 850 por vídeo). Gera 1 tomada (`generations_count: 1`) se o crédito estiver curto.
- Baixa o mp3 e converte: `ffmpeg -i t1.mp3 -ar 48000 -ac 1 voz/t1.wav`.
- Transcreve com `eleven_scribe_v1` (custa 0) e salva o `words.json` em `voz/`.

## 4. Pipeline (arquivos nesta pasta, em `motor/`)
Estrutura: `projeto/` com `node_modules/three` (`npm i three@0.160.0`), `fonts/ttf/` (Fredoka-Bold, Nunito-ExtraBold) e a pasta do vídeo (ex.: `creche/`).

1. **`build_timing.py`**:
   - Edita `RAW`: uma linha por frase, `*palavra*` = destaque colorido, terceiro campo = última palavra falada da frase, sem acento.
   - Edita `GROUPS`: quais frases entram em cada plano.
   - Rodar `python3 build_timing.py` gera o `timing.js` (tempo de cada palavra, planos e duração).
2. **`index.html`**: legenda palavra por palavra, contador, balão, cartão da lei, carimbo, pílulas, caixa de comentário e "SEGUE". Normalmente nem precisa mexer.
3. **`scene.js`** (Three.js): é aqui que o vídeo muda de cara.
   - **Reaproveitar sempre:**
     - `person()`: boneco de corpo inteiro com cabelo, óculos, fone, crachá e opção `bone:true` para esqueleto;
     - `pose()`: andar (`walk`), sentar (`sit`), braços (`aL`/`aR` = [frente, lado]), cotovelo, cabeça, boca (`jaw`), pulo (`y`);
     - `sign()`: placas com texto;
     - `pill()`, `setStamp()`, `setCard()`, `setBubble()`, `setCounter()`;
     - `confetti()`, `camAt()` com subcortes e tremida de câmera (`SH`).
   - **Trocar a cada vídeo:** o bloco do cenário ("AGÊNCIA" e "SALA" no exemplo do BPC), os objetos, a lista `CAMS` (uma por plano: `[início, posA, posB, olharA, olharB, fov, fim]`) e o `update(t)` com o que acontece em cada plano `k`. Tempo de palavra: `wt(linha, índice)`.
   - Regra de ouro: `renderAt(t)` precisa ser **função pura do tempo**. Tudo é recalculado a cada quadro, sem estado guardado de um quadro pro outro.
4. **Servidor + fotos de teste**:
   - na pasta `projeto/`: `python3 -m http.server 8765`;
   - na pasta do vídeo: `node shoot.mjs stills 1.7,3.6,8.5,...`;
   - montar uma folha de contato e **olhar**: câmera dentro de boneco, cabeça cortada, placa fora do quadro, pílula em cima da legenda.
   - Corrigir e repetir até ficar bom. Só então renderizar.
5. **Render**: 2 processos em paralelo (a máquina tem 2 CPUs):
   - `node shoot.mjs video 0 700 out/a.mp4 &`
   - `node shoot.mjs video 700 FIM out/b.mp4`
   - FIM = DUR×30.
6. **Som**:
   - `snd.py` cria a batida (100 bpm) e os efeitos: whoosh no corte, baque no carimbo, moedas, ding, assobio descendo no meme, festa.
   - Os momentos vêm do `timing.js`. Ajusta a lista de efeitos para os eventos do vídeo novo.
   - `mix.sh` mistura voz (-16 LUFS), batida, efeitos e uma música engraçada (Pixabay) só no trecho do meme e do pedido de comentário. Meta final: **-14 LUFS**, pico ≤ -1,5 dB.
7. **Juntar**:
```
ffmpeg -f concat -safe 0 -i lista.txt -c copy out/v.mp4
ffmpeg -i out/v.mp4 -i out/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```
   Depois tira 6 quadros do final e confere de novo.

## 5. Publicar
O vídeo vai pro repositório GitHub `minharotina-kit/midia`, numa pasta `AAAA-MM-DD-tema/` com a `legenda.txt`. Depois:
- **Com o conector Windsor:** `execute_action(connector="instagram", account="17841417730198109", action="create_video_post", params={video_url: <raw.githubusercontent.com do commit>, caption, share_to_feed: true})`. Para conferir, usar `get_data` com os campos date, media_type e media_permalink e `date_preset` "last_1dT".
- **Sem conector:** entregar o MP4 e a legenda pro Mateus postar.
- Horários: **12h e 20h** (horário de Brasília).

## 6. Como falar com o Mateus
- Direto, sem elogio exagerado. "Mano" pode; outras gírias tipo "parceiro" não.
- Quando faltar crédito ou algo der errado, falar na hora, em uma frase, com as opções.
