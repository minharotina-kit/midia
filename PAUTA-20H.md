# Pauta das 20h · Família Tatu com dados

**Pedido do Mateus (26/10):** a novela das 20h também leva dados reais, a partir da parte 3. As partes já feitas (parte 2, 27/10) não mudam.

## Como entra o dado (sem quebrar a história)
- A narradora (Nathalia, estilo Chris) solta o dado num quadro congelado, como comentário da cena: "Fato: a Academia Americana de Pediatria orienta... O Papai não leu essa parte."
- Enquanto ela fala, aparece no alto o selo **FONTE · nome da instituição** (`"src"` no config do `build_tatu_narrado.py`).
- 1 ou 2 dados por parte, nunca mais. A graça continua sendo a história.
- Só fatos do `BANCO-DE-FONTES.md`, do jeito da coluna "Como falar".
- Legenda do post termina com "Fonte: ...".
- Não repetir o mesmo dado que saiu no 12h do mesmo dia ou da véspera.

## Partes 3 a 5
| Parte | Cena do dado | Dado | Fonte |
|---|---|---|---|
| 3 · A Manhã do Papai (Qua 28) ✅ agendada | Mochila aberta, Papai congelado com o sapato | "Pra manhã andar melhor, deixe o máximo de coisas prontas na noite anterior." | AAP, *The Importance of Family Routines* |
| 3 (opcional) | Meia sumida / camisetas | "Criança se dá melhor quando a rotina é regular, previsível e sempre igual." | AAP (mesma página) |
| 4 · O Quadro da Geladeira (Qui 29) ✅ agendada | Papai com as duas camisetas | "Essa ou aquela? Dar escolha evita a briga de última hora." | AAP (mesma página) + CDC: poucas escolhas simples |
| 4 (opcional) | Bento batendo na mão do Papai na porta | "Um abraço e um tchau na porta fazem diferença: a criança começa o dia bem." | AAP (mesma página) |
| 5 · A Vovó Chegou (Sex 30) ✅ agendada | Vovó cria o cartão novo | "Rotina rígida demais, sem escolha nenhuma, cansa. Dá pra ajustar e continuar previsível." | AAP (mesma página) |
| 5 (opcional) | Mamãe mostrando o quadro pra Vovó | "Mudou a rotina? Combina com calma, explica o motivo e se é por pouco tempo." | CDC, *Tips for Relying on Routines and Rules* |

Temporada 2 (a partir de 31/10): cada episódio nasce com 1 dado do banco já escolhido no roteiro.

## Feito
- Parte 3: `2026-10-28-tatu-parte3/` (commit de2eeb2), agendada 28/10 22:59Z. Música: comedy-comedy-music-614068. Dado: AAP, noite anterior.
- Parte 4: `2026-10-29-tatu-parte4/`, agendada 29/10 22:59Z. Música: comedy-bgm-funny-background-music-583242. Dado: AAP, oferecer escolha.
- Parte 5 (fim da temporada 1): `2026-10-30-tatu-parte5/`, agendada 30/10 22:59Z. Música: comedy-cartoon-funny-background-music-365347. Dado: AAP, previsível sim, rígida demais entedia. Cartão final: "Temporada 2 em breve".
- Músicas de comédia já usadas: funny-bouncy-cartoon-mischief (parte 2), comedy-comedy-music-614068 (parte 3), comedy-bgm-funny-background-music-583242 (parte 4), comedy-cartoon-funny-background-music-365347 (parte 5). Sobram: funny-playful-262598, funny-funny-music-595118, funny-funny-music-611043, comedy-comedy-music-585937, comedy-cartoon-funny-background-music-482003.
