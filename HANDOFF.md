# Passagem de bastão · @paisdarotina (26/10/2026)

Leia isto primeiro ao continuar o trabalho do Instagram @paisdarotina numa conversa nova.

## Perfil hoje
- Instagram @paisdarotina (antes @minharotina.kit). Conta Windsor: 17841417730198109.
- Nome: "Rotina Infantil pros Pais". Foto: sol e lua (`marca/foto-perfil-sol-lua.jpg`). Bio neutra.
- 5 seguidores. Os 3 posts do kit (13/10) foram arquivados.

| Post | Views | Alcance | Pulou no começo | Tempo médio |
|---|---|---|---|---|
| Família Tatu, parte 1 (3D) | 402 | 296 | 46% | 11 s de 24 |
| Bento ep. 1 (2D) | 239 | 192 | 62% | 6,4 s |
| Bento ep. 2 (2D) | 152 | 121 | 54% | 7,7 s |
| Informativo "3 motivos" | 26 | 18 | 71% | 7,2 s |

## Regras do Mateus (valem sempre)
- Fala curta e visual. Só "mano" de gíria. Sem bajulação.
- **Nunca repetir conteúdo:** nada de recorte de episódio antigo, nem cenas/imagens já usadas. Cada post tem imagem nova.
- **Música muda em todo vídeo.** A voz (Nathalia, `XLCZh6aNZcwLn60NRLg5`) pode repetir.
- Família Tatu (novelinha 3D, estilo frutinha) é o formato que ganhou. O informativo de papel saiu da grade.
- Horários: 12h e 20h, todo dia. Ele aprovou agendar automático; mande a prévia e ele pode cancelar até a hora.
- Não prometer "parte X amanhã" sem os clipes na mão.
- Marca anônima, sem dados pessoais, sem comentar em contas dos outros.

## Agendado
- 26/10 20h: Reel "Faz hoje: 3 coisas antes de dormir" (agendado na conversa antiga; publica sozinho).
- 12h: a definir. Plano: gerar imagem/clipe/música novos com o conector completo do ElevenLabs.

## Família Tatu
- Página com todos os prompts das partes 2 a 5: https://claude.ai/artifact/C9vah7DYV78AyL7CFhbrYS
- Parte 2: clipes do Mateus até terça 27/10 17h → sai 20h. Partes 3 a 5: até quarta 17h.
- Referências: `cenas/familia-3d/pais-tatu.jpg`, `cenas/familia-3d/bento-3d.jpg`. Clipes brutos da parte 1: `cenas/familia-3d/clipes-parte1/`.
- Grok fala português do Brasil direito. Saída 720×1264, 24 qps, 10 s.

## Ferramentas
- Publicar: Windsor `create_video_post` (publica na hora) → agende com `send_later` pra 1 min antes.
- Hospedar: este repositório via jsDelivr fixado no commit. **Arquivo até 20 MB** (exportar crf 21, maxrate 5M).
- Rede liberada: api.elevenlabs.io e storage.googleapis.com (baixar narração do ElevenLabs funciona). Pixabay bloqueia robô (Cloudflare): não dá pra pegar música de lá.
- Música própria: `tools/musica.py <ninar|ukulele|piano|xilo> <segundos> <semente> saida.wav` (original, sem direitos; semente diferente a cada vídeo). Mistura com `tools/remix.py`: voz +10 dB, música −13 dB com ducking, −14 LUFS.
- Conector completo do ElevenLabs (imagem, vídeo, música): instalado na conta em 26/10, só carrega em conversa nova. Teste primeiro com `creative_get_flow_node_types`.
- Scripts de montagem em `tools/` (`build_tatu_ep1.py` é o molde do episódio; `build_reel_noite.py` o do Reel narrado). Fontes em `fonts/` (OFL). Os scripts apontam pra pasta de rascunho antiga: troque `S` em `build_reel_info.py` pela pasta da sessão nova e copie `fonts/ttf` pra lá.
