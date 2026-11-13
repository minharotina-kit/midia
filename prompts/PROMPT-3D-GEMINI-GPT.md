# Prompt mestre: vídeo 3D low-poly (Gemini / GPT)

Você vai criar um vídeo vertical 3D (Reels/TikTok, 9:16) em UM arquivo HTML com Three.js, no estilo low-poly de dia dos vídeos virais de "história em 3D". Eu vou gravar a tela, então o HTML precisa tocar sozinho do começo ao fim com cara de vídeo profissional. Leia tudo antes de começar.

TEMA: [escreva aqui o tema]
DURAÇÃO: [45 a 60 s]
NARRAÇÃO: [cole o texto; se tiver o tempo de cada palavra, cole também]
@ NO FINAL: [seu @]

## ETAPA 1 — ANTES DO CÓDIGO, me mostre:
1. Roteiro em frases curtas (máx. 14 palavras). Gancho nos primeiros 2 s: algo que todo mundo já viveu ou acredita, ou uma pergunta que dá vontade de ver o fim. Estrutura: gancho → problema → tentativa que falha → segunda falha → virada (o segredo) → resultado com número → fechamento + chamada pra comentar/compartilhar.
2. Tabela de tomadas: nº | início–fim (s) | frase | câmera (de onde, pra onde olha, movimento) | o que os personagens fazem | textos na tela (legenda, etiquetas, contador, carimbo).
Regra: cada frase tem uma AÇÃO visível. Se a narração diz "a água vaza", a câmera está a 2–3 m do vazamento mostrando jatos d'água.

## ETAPA 2 — CÓDIGO (regras obrigatórias)

### Arquitetura
- Three.js 0.160.0 via importmap: https://unpkg.com/three@0.160.0/build/three.module.js e addons em https://unpkg.com/three@0.160.0/examples/jsm/. Nada de imagem ou modelo externo: tudo procedural.
- Palco fixo 720×1280 (canvas + camadas HTML por cima), escalado com CSS pra ocupar a tela do celular, fundo preto fora do palco.
- Tudo sai de uma função pura renderAt(t), t em segundos: câmera, personagens, objetos e textos calculados só a partir de t. Proibido: física acumulada, Math.random sem semente (use rng com seed), estado que depende do frame anterior. No início de cada frame, resete as poses.
- Player: botão grande ▶ que some ao tocar; no fim congela no último quadro. URL ?t=12.5 abre parado no segundo 12,5. Teclas ← → andam 0,1 s.
- No topo do código: LINES (frases com t0 e tempo de cada palavra; sem áudio, estime 2,6 palavras/s + 0,25 s de pausa entre frases) e SHOTS (t0, t1, câmera de/para, alvo de/para).

### Visual (o que deixa top)
- Renderer: antialias, outputColorSpace sRGB, toneMapping ACESFilmic, exposure 1.08, sombras PCFSoft.
- Céu: esfera grande com degradê vertical (horizonte #c4e4fb → topo #2f86e8) + fog da cor do horizonte (38 a 125). Nuvens = grupos de icosaedros brancos; morros = cones grandes verde-acinzentados ao fundo.
- Luz: HemisphereLight(#e8f3ff, #8fb56a, 1.15) + sol DirectionalLight(#fff0d0, 2.7) com sombra 2048 px. Todo objeto projeta e recebe sombra.
- Pós: EffectComposer + UnrealBloomPass(0.16, 0.5, 1.15) + OutputPass. Bloom só no que brilha.
- MeshStandardMaterial, roughness 0.9, flatShading true, cores saturadas e harmônicas (paleta no topo).
- Mundo SEM BORDA: chão 400×400, manchas de grama em 2 tons, 1.000+ tufos instanciados (cones de 4 lados), flores, pedras, árvores low-poly (tronco + 3–4 icosaedros) até o horizonte. Nunca aparece fim do cenário, ilha flutuando ou fundo vazio.
- Água: plano com ondulação nos vértices em função de t, 2 tons, espuma nas bordas; vazamento = jatos de partículas instanciadas em parábola.
- Física de mentira mas crível: nada flutua nem atravessa outro objeto; tudo apoiado; objeto carregado fica preso na mão/boca.

### Personagem (obrigatório)
- Protagonista com ROSTO em todos os shots: cabeça grande (1,3–1,5×), olhos grandes (esfera branca + pupila preta + pontinho de brilho), sobrancelhas, bochecha rosada, boca. Animal também (castor: corpo marrom ovalado, dentes da frente, rabo achatado escuro, patinhas).
- Animação procedural: andar (pernas e braços em seno), respirar, piscar a cada 3–4 s, cabeça vira pro que importa, reações (pulo, braços pra cima, susto).
- Personagens secundários quando a história pedir.

### Câmera e cortes
- Um shot por frase (3–8 s). Em todo shot a câmera se move: posição e alvo de A→B com easeInOutCubic (push-in lento, arco lateral ou subida). Nunca parada, nunca tremida.
- Câmera perto e baixa: 2–6 m do assunto, na altura do personagem. Plano geral com assunto pequeno só no 1º shot, e já fechando.
- Enquadramento 9:16: assunto com 40–60% da altura da tela, entre 30% e 80% da altura. Faixa de cima (0–25%) é da legenda; faixa de baixo (88–100%) é da fonte/CTA.
- Varie o ângulo a cada shot (frente, 3/4, por cima do ombro, close no detalhe). Corte com mergulho no preto de 0,07 s.

### Texto na tela (HTML por cima do canvas)
- Legenda no topo (top 150 px, largura 660 px): Poppins 900 (Google Fonts), MAIÚSCULAS, 38–50 px, branco com contorno escuro de 4 px (-webkit-text-stroke + paint-order: stroke fill) e sombra. Cada palavra aparece no seu tempo com escala 0,6→1 e leve overshoot. Palavras-chave coloridas (#ffd24a, #4fd0ff, #ff5a68, #3dffa0).
- Etiquetas presas aos objetos 3D: projete a posição 3D pra tela a cada frame (vector.project(camera)); fundo escuro 90%, borda colorida 2 px, 21 px, nunca acima de 26% da tela.
- Contador no topo que muda nos momentos certos ("TENTATIVA 2/3", "ÁGUA PERDIDA 37%", "ETAPA 3/5"), números subindo animados.
- Carimbo no clímax: 60 px, borda 6 px, entra com escala 1,9→1 em 0,16 s, girado −6°.
- Base: faixa pequena de fonte (15 px) quando citar fato; no final, o @.
- Proibido: caixa de texto fixa embaixo com frase genérica.

## ETAPA 3 — AUTOCHECAGEM (responda item por item)
1. Algum objeto flutua ou atravessa outro?
2. Aparece borda do mundo ou fundo vazio em algum ângulo?
3. O protagonista com rosto aparece em todo shot?
4. A legenda cobre o assunto em algum momento?
5. A câmera se move em todos os shots?
6. Toda frase tem uma ação visível?
7. O texto é legível em qualquer fundo?
8. Roda liso a 30 fps no celular (InstancedMesh pro que se repete, só o sol com sombra)?
Se algum item falhar, corrija antes de entregar. Entregue o HTML completo num bloco só.

---

# Prompt de correção (quando vier vago)

Ficou vago. Refaz sem mudar o roteiro:
- Câmera a 2–4 m do assunto, na altura do personagem, com push-in em todo shot; o assunto ocupando metade da altura da tela.
- Mostra o personagem com rosto (olhos grandes) fazendo a ação de cada frase.
- Tira tudo que flutua ou atravessa; apoia cada peça.
- Enche o fundo até o horizonte (grama, árvores, morros, nuvens); nunca a borda do cenário.
- Sombra do sol, céu em degradê, ACES, bloom fraco.
- Legenda palavra por palavra no topo, etiquetas presas nos objetos, contador e carimbo no clímax.
Depois roda a autochecagem de novo e me entrega o HTML completo.
